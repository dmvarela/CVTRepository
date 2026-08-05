from __future__ import annotations

import argparse, hashlib, json, math, time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit, logit
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

SEED = 20260814
HASHES = {
    "training.csv": "31a23de52adf5914929c5c56f3dd7ff6ded03ac9daf42e96f9269006371b512b",
    "validation.csv": "b2b70e5bb8624ee5300c37d8750ace3b63e3cb5e3f727c15f6abc164da38467f",
}
GATES = ["g_b", "g_q", "g_c_probe_sham_adjusted_primary", "g_s"]
C_SENS = {
    "primary": "g_c_probe_sham_adjusted_primary",
    "dose_2_5x": "g_c_probe_sham_adjusted_2_5x_dose",
    "direct": "g_c_direct_structural_composite",
}
FAMILIES = ["constant", "pulse", "ramp", "shock_tail"]
SCHEDULE = ["peak_source_concentration", "peak_permeability", "active_duration", "pulse_count", "scheduled_peak_intact_flux", "scheduled_intact_dose"]
INITIAL = ["initial_c_a", "initial_p_fraction", "initial_u_fraction", "initial_d", "initial_s_fraction", "initial_q", "param_h"]
MARGINS = ["productive_headroom", "buffer_headroom", "damage_margin", "integrity_margin", "reserve_fraction", "free_load_margin"]
POSITIVE = [
    "param_p_cap", "param_u_max", "param_k_p", "param_k_b", "param_k_rel", "param_k_e", "param_s_max", "param_r_s", "param_k_rep", "param_r_q", "param_c_safe", "param_u_safe", "param_c_q", "param_j_safe", "param_k_s", "param_k_q", "param_s_export", "param_k_rep_half", "param_k_qs", "param_k_d1", "param_k_d2", "param_k_d3", "param_a_p", "param_a_e", "param_a_b", "param_a_r", "param_b_d", "param_b_l"
]
L2 = [0.0, 1e-4, 1e-3, 1e-2, 1e-1, 1.0]
TAUS = [0.02, 0.05, 0.10, 0.20, 0.50]
BOOST = [
    dict(max_leaf_nodes=l, learning_rate=r, max_iter=i, min_samples_leaf=m)
    for l in [7, 15, 31] for r in [0.03, 0.10] for i in [100, 300] for m in [20, 50]
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(data: Path) -> None:
    for name, expected in HASHES.items():
        got = sha(data / name)
        if got != expected:
            raise ValueError(f"Stage 3.1 hash mismatch for {name}: {got}")


def splits(frame: pd.DataFrame):
    strata = frame.hosted.astype(int).astype(str) + "::" + frame.forcing_family.astype(str)
    return list(StratifiedKFold(5, shuffle=True, random_state=SEED).split(np.zeros(len(frame)), strata))


def gates(frame: pd.DataFrame, c: str = C_SENS["primary"]) -> np.ndarray:
    return frame[["g_b", "g_q", c, "g_s"]].to_numpy(float)


def pairwise(x: np.ndarray) -> np.ndarray:
    return np.column_stack([x] + [x[:, i] * x[:, j] for i in range(4) for j in range(i + 1, 4)])


def fit_map(z, y, positive=True, l2=1e-6):
    z, y = np.asarray(z, float), np.asarray(y, float)
    p0 = float(np.clip(y.mean(), 1e-8, 1 - 1e-8))
    def fg(v):
        a, b = v; eta = a + b * z; p = expit(eta); r = p - y
        f = np.sum(np.logaddexp(0, eta) - y * eta) + .5 * l2 * (a*a + b*b)
        g = np.array([r.sum() + l2*a, np.dot(r, z) + l2*b])
        return f, g
    result = minimize(lambda v: fg(v)[0], [logit(p0), 1.0], jac=lambda v: fg(v)[1], method="L-BFGS-B", bounds=[(None,None),(0,None)] if positive else None)
    if not result.success: raise RuntimeError(result.message)
    return float(result.x[0]), float(result.x[1])


def scalar_cv(z, y, fold):
    values=[]
    for tr, va in fold:
        a,b=fit_map(z[tr],y[tr],True); p=expit(a+b*z[va]); values.append(np.mean((p-y[va])**2))
    return float(np.mean(values))


def fit_mono(x, y, l2):
    y=np.asarray(y,float); p0=float(np.clip(y.mean(),1e-8,1-1e-8)); k=x.shape[1]
    def fg(v):
        a=v[0]; b=v[1:]; eta=a+x@b; p=expit(eta); r=p-y
        f=np.sum(np.logaddexp(0,eta)-y*eta)+.5*l2*np.dot(b,b)
        return f,np.r_[r.sum(),x.T@r+l2*b]
    result=minimize(lambda v:fg(v)[0],np.r_[logit(p0),np.full(k,.1)],jac=lambda v:fg(v)[1],method="L-BFGS-B",bounds=[(None,None)]+[(0,None)]*k,options={"maxiter":1000})
    if not result.success: raise RuntimeError(result.message)
    return float(result.x[0]),result.x[1:]


def mono_cv(x,y,fold,l2):
    out=[]
    for tr,va in fold:
        a,b=fit_mono(x[tr],y[tr],l2); out.append(np.mean((expit(a+x[va]@b)-y[va])**2))
    return float(np.mean(out))


def preprocessor(columns, log_columns):
    log_columns=[c for c in columns if c in log_columns]; raw=[c for c in columns if c not in log_columns]
    blocks=[]
    if raw: blocks.append(("raw",StandardScaler(),raw))
    if log_columns: blocks.append(("log",Pipeline([("log",FunctionTransformer(np.log,feature_names_out="one-to-one")),("scale",StandardScaler())]),log_columns))
    blocks.append(("family",OneHotEncoder(categories=[FAMILIES],drop=["constant"],handle_unknown="ignore",sparse_output=False),["forcing_family"]))
    return ColumnTransformer(blocks,verbose_feature_names_out=False)


def log_model(l2):
    return LogisticRegression(C=1e6 if l2==0 else 1/l2,solver="lbfgs",max_iter=3000,random_state=SEED)


def model_cv(frame,y,fold,columns,logs,l2,boost=None):
    values=[]
    for tr,va in fold:
        prep=preprocessor(columns,logs); xt=prep.fit_transform(frame.iloc[tr]); xv=prep.transform(frame.iloc[va])
        model=HistGradientBoostingClassifier(loss="log_loss",random_state=SEED,**boost) if boost else log_model(l2)
        model.fit(xt,y[tr]); p=model.predict_proba(xv)[:,1]; values.append(np.mean((p-y[va])**2))
    return float(np.mean(values))


def choose(rows, tie=.0005, key=lambda r:(-r.get("l2",0),)):
    best=min(r["cv_brier"] for r in rows); tied=[r for r in rows if r["cv_brier"]-best<tie]
    return min(tied,key=key)


def softmin(x,tau):
    m=x.min(1,keepdims=True); return m[:,0]-tau*np.log(np.mean(np.exp(-(x-m)/tau),axis=1))


def threshold_tune(x,y,fold):
    q=np.quantile(x,np.arange(.1,1,.1),axis=0); mesh=np.meshgrid(*[q[:,i] for i in range(4)],indexing="ij"); combos=np.column_stack([a.ravel() for a in mesh]); total=np.zeros(len(combos))
    for tr,va in fold:
        zt=np.min(x[tr,:,None]-combos.T[None,:,:],axis=1); zv=np.min(x[va,:,None]-combos.T[None,:,:],axis=1)
        yy=y[tr,None]; a=np.full(len(combos),logit(np.clip(y[tr].mean(),1e-8,1-1e-8))); b=np.ones(len(combos))
        for _ in range(8):
            eta=a[None,:]+zt*b[None,:]; p=expit(eta); r=p-yy; w=p*(1-p)
            ga=r.sum(0)+1e-6*a; gb=(r*zt).sum(0)+1e-6*b; haa=w.sum(0)+1e-6; hab=(w*zt).sum(0); hbb=(w*zt*zt).sum(0)+1e-6; det=np.maximum(haa*hbb-hab*hab,1e-12)
            da=(hbb*ga-hab*gb)/det; db=(-hab*ga+haa*gb)/det; a-=np.clip(da,-5,5); b=np.maximum(0,b-np.clip(db,-5,5))
        total+=np.mean((expit(a[None,:]+zv*b[None,:])-y[va,None])**2,axis=0)
    total/=len(fold); best=total.min(); tied=np.flatnonzero(total-best<.0005); center=np.median(x,axis=0); idx=int(tied[np.argmin(np.abs(combos[tied]-center).sum(1))])
    return combos[idx],float(total[idx]),int(len(combos))


def scalar_candidate(name,cal,score,meta,input_count=4,thresholds=0,hyper=0):
    a,b=fit_map(score(cal),cal.hosted.to_numpy(int),True)
    return dict(name=name,family="CVT",input_count=input_count,coeff=0,thresholds=thresholds,hyper=hyper,cal=2,meta={**meta,"calibration":[a,b]},predict=lambda f:expit(a+b*score(f)))


def mono_candidate(name,fit,cal,l2,use_pair):
    xf=pairwise(gates(fit)) if use_pair else gates(fit); xc=pairwise(gates(cal)) if use_pair else gates(cal); a,b=fit_mono(xf,fit.hosted.to_numpy(int),l2); ca,cb=fit_map(a+xc@b,cal.hosted.to_numpy(int),False)
    def pred(f):
        x=pairwise(gates(f)) if use_pair else gates(f); return expit(ca+cb*(a+x@b))
    return dict(name=name,family="CVT",input_count=4,coeff=len(b)+1,thresholds=0,hyper=1,cal=2,meta={"l2":l2,"intercept":a,"coef":b.tolist(),"calibration":[ca,cb]},predict=pred)


def baseline_candidate(name,fit,cal,columns,logs,l2=None,boost=None):
    prep=preprocessor(columns,logs); xf=prep.fit_transform(fit); xc=prep.transform(cal); y=fit.hosted.to_numpy(int)
    model=HistGradientBoostingClassifier(loss="log_loss",random_state=SEED,**boost) if boost else log_model(l2)
    model.fit(xf,y); raw=lambda x: logit(np.clip(model.predict_proba(x)[:,1],1e-8,1-1e-8)) if boost else model.decision_function(x); ca,cb=fit_map(raw(xc),cal.hosted.to_numpy(int),False)
    names=list(prep.get_feature_names_out()); leaves=0
    if boost:
        leaves=sum(int(np.sum(tree.nodes["is_leaf"])) for iteration in model._predictors for tree in iteration)
    def pred(f): return expit(ca+cb*raw(prep.transform(f)))
    return dict(name=name,family="baseline",input_count=len(names),coeff=leaves if boost else len(names)+1,thresholds=0,hyper=4 if boost else 1,cal=2,meta={"features":names,"l2":l2,"boost":boost,"leaves":leaves,"calibration":[ca,cb]},predict=pred)


def metrics(y,p):
    z=logit(np.clip(p,1e-8,1-1e-8)); ci,cs=fit_map(z,y,False,1e-8); order=np.argsort(p); chunks=np.array_split(order,10); ece=sum(len(c)/len(y)*abs(p[c].mean()-y[c].mean()) for c in chunks)
    def th(t):
        mask=p>=t; n=int(mask.sum()); return {"count":n,"coverage":float(mask.mean()),"false_safe_rate":float(np.mean(y[mask]==0)) if n else math.nan,"informative":n>=50}
    return {"brier":float(brier_score_loss(y,p)),"log_loss":float(log_loss(y,p,labels=[0,1])),"auroc":float(roc_auc_score(y,p)),"average_precision":float(average_precision_score(y,p)),"calibration_intercept":ci,"calibration_slope":cs,"ece":float(ece),"high":th(.8),"ordinary":th(.5)}


def bootstrap(frame,preds,n=2000):
    y=frame.hosted.to_numpy(float); names=list(preds); sq=np.column_stack([(preds[k]-y)**2 for k in names]); groups=[np.asarray(v) for v in frame.groupby(["hosted","forcing_family"]).indices.values()]; rng=np.random.default_rng(SEED+1); draws=np.empty((n,len(names)))
    for i in range(n):
        idx=np.concatenate([rng.choice(g,len(g),replace=True) for g in groups]); draws[i]=sq[idx].mean(0)
    cis={names[j]:np.quantile(draws[:,j],[.025,.975]).tolist() for j in range(len(names))}; diffs={(a,b):np.quantile(draws[:,i]-draws[:,j],[.025,.975]).tolist() for i,a in enumerate(names) for j,b in enumerate(names) if i!=j}
    return cis,diffs


def select(models,rows,diffs,order):
    best=min(models,key=lambda m:rows[m["name"]]["brier"]); tied=[]
    for m in models:
        if m is best or abs(rows[m["name"]]["brier"]-rows[best["name"]]["brier"])<.002 or diffs[m["name"],best["name"]][0]<=0<=diffs[m["name"],best["name"]][1]: tied.append(m)
    def key(m):
        h=rows[m["name"]]["high"]; fs=h["false_safe_rate"] if h["informative"] else math.inf; total=m["coeff"]+m["thresholds"]+m["hyper"]+m["cal"]
        return fs,total,order.index(m["name"])
    return min(tied,key=key)["name"]


def run(data_dir: str|Path, output_dir: str|Path, bootstrap_n=2000):
    data=Path(data_dir); out=Path(output_dir); out.mkdir(parents=True,exist_ok=True); verify(data)
    training=pd.read_csv(data/"training.csv"); validation=pd.read_csv(data/"validation.csv"); fit=training[training.training_subset=="fit"].reset_index(drop=True); cal=training[training.training_subset=="calibration"].reset_index(drop=True); y=fit.hosted.to_numpy(int); fold=splits(fit); x=gates(fit); tuning={}; models=[]
    defs={"CVT-1-product":lambda z:np.prod(z,1),"CVT-2-minimum":lambda z:np.min(z,1),"CVT-3-geometric":lambda z:np.prod(z,1)**.25}
    for name,fn in defs.items():
        cv=scalar_cv(fn(x),y,fold); tuning[name]={"cv_brier":cv}; models.append(scalar_candidate(name,cal,lambda f,fn=fn:fn(gates(f)),tuning[name]))
    grid=[{"tau":t,"cv_brier":scalar_cv(softmin(x,t),y,fold)} for t in TAUS]; chosen=choose(grid,key=lambda r:(-r["tau"],)); tuning["CVT-4-softmin"]={"grid":grid,"selected":chosen}; models.append(scalar_candidate("CVT-4-softmin",cal,lambda f,t=chosen["tau"]:softmin(gates(f),t),tuning["CVT-4-softmin"],hyper=1))
    thresholds,cv,count=threshold_tune(x,y,fold); tuning["CVT-5-direct-constraint"]={"thresholds":thresholds.tolist(),"cv_brier":cv,"candidate_count":count}; models.append(scalar_candidate("CVT-5-direct-constraint",cal,lambda f,t=thresholds:np.min(gates(f)-t,1),tuning["CVT-5-direct-constraint"],thresholds=4))
    for name,use_pair in [("CVT-6-monotone-main-effects",False),("CVT-7-monotone-pairwise",True)]:
        xx=pairwise(x) if use_pair else x; grid=[{"l2":v,"cv_brier":mono_cv(xx,y,fold,v)} for v in L2]; chosen=choose(grid); tuning[name]={"grid":grid,"selected":chosen}; models.append(mono_candidate(name,fit,cal,chosen["l2"],use_pair))
    pcal=float(cal.hosted.mean()); models.append(dict(name="BL-0-prevalence",family="baseline",input_count=0,coeff=0,thresholds=0,hyper=0,cal=1,meta={"probability":pcal},predict=lambda f,p=pcal:np.full(len(f),p)))
    specs={"BL-1-forcing-only":SCHEDULE,"BL-2-transport-only":SCHEDULE+["initial_c_a"],"BL-3-mechanistic-margins":SCHEDULE+MARGINS,"BL-4-raw-initial-state":SCHEDULE+INITIAL,"BL-5-full-native-logistic":list(dict.fromkeys(SCHEDULE+INITIAL+POSITIVE+["param_h"]))}
    for name,cols in specs.items():
        grid=[{"l2":v,"cv_brier":model_cv(fit,y,fold,cols,POSITIVE,v)} for v in L2]; chosen=choose(grid); tuning[name]={"grid":grid,"selected":chosen}; models.append(baseline_candidate(name,fit,cal,cols,POSITIVE,l2=chosen["l2"]))
    cols=specs["BL-5-full-native-logistic"]; grid=[{**b,"cv_brier":model_cv(fit,y,fold,cols,POSITIVE,0,boost=b)} for b in BOOST]; chosen=choose(grid,key=lambda r:(r["max_leaf_nodes"],r["max_iter"],-r["min_samples_leaf"],r["learning_rate"])); setting={k:chosen[k] for k in ["max_leaf_nodes","learning_rate","max_iter","min_samples_leaf"]}; tuning["BL-6-full-native-gradient-boosting"]={"grid":grid,"selected":chosen}; models.append(baseline_candidate("BL-6-full-native-gradient-boosting",fit,cal,cols,POSITIVE,boost=setting))
    predictions={m["name"]:m["predict"](validation) for m in models}; yv=validation.hosted.to_numpy(int); rows={n:metrics(yv,p) for n,p in predictions.items()}; cis,diffs=bootstrap(validation,predictions,bootstrap_n)
    cvt=[m for m in models if m["family"]=="CVT"]; base=[m for m in models if m["family"]=="baseline"]; cvt_order=["CVT-2-minimum","CVT-1-product","CVT-3-geometric","CVT-4-softmin","CVT-5-direct-constraint","CVT-6-monotone-main-effects","CVT-7-monotone-pairwise"]; base_order=["BL-0-prevalence","BL-1-forcing-only","BL-2-transport-only","BL-3-mechanistic-margins","BL-4-raw-initial-state","BL-5-full-native-logistic","BL-6-full-native-gradient-boosting"]
    best_cvt=select(cvt,rows,diffs,cvt_order); best_base=select(base,rows,diffs,base_order); best_simple=min(base_order[:3],key=lambda n:rows[n]["brier"]); best_native=min(base_order[-2:],key=lambda n:rows[n]["brier"]); lookup={m["name"]:m for m in models}
    inc_ci=diffs[best_cvt,best_simple]; comp_ci=diffs[best_cvt,best_native]; inc_abs=rows[best_simple]["brier"]-rows[best_cvt]["brier"]; inc_rel=inc_abs/rows[best_simple]["brier"]; comp=rows[best_cvt]["brier"]-rows[best_native]["brier"]; input_fraction=lookup[best_cvt]["input_count"]/max(1,lookup[best_native]["input_count"])
    sensitivity={}
    selected=lookup[best_cvt]
    for label,col in C_SENS.items():
        tmp=validation.copy(); tmp["g_c_probe_sham_adjusted_primary"]=tmp[col]; sensitivity[label]=metrics(yv,selected["predict"](tmp))
    direct=np.asarray(tuning["CVT-5-direct-constraint"]["thresholds"]); gv=gates(validation); allpass=(gv>=direct).all(1); hosted=yv==1
    selection={"best_cvt":best_cvt,"best_baseline":best_base,"best_simple_baseline":best_simple,"best_native_baseline":best_native,"incremental_value":{"absolute_improvement":inc_abs,"relative_improvement":inc_rel,"ci":inc_ci,"passes":bool(inc_abs>=.005 and inc_rel>=.02 and inc_ci[1]<0)},"predictive_compression":{"brier_disadvantage":comp,"ci":comp_ci,"input_fraction":input_fraction,"passes":bool(comp<=.005 and comp_ci[1]<=.01 and input_fraction<=1/3)},"counterexamples":{"thresholds":direct.tolist(),"hosted_with_failed_gate":int(np.sum(hosted&~allpass)),"hosted_total":int(hosted.sum()),"nonhosted_all_gates_pass":int(np.sum(~hosted&allpass)),"all_gates_0_8_nonhosted":int(np.sum(~hosted&(gv>=.8).all(1)))},"sensitivity":sensitivity,"validation_opened_once":True,"final_test_generated":False,"final_test_opened":False}
    table=[]
    for m in models:
        r=rows[m["name"]]; table.append({"model":m["name"],"family":m["family"],"brier":r["brier"],"brier_ci_lower":cis[m["name"]][0],"brier_ci_upper":cis[m["name"]][1],"log_loss":r["log_loss"],"auroc":r["auroc"],"average_precision":r["average_precision"],"calibration_intercept":r["calibration_intercept"],"calibration_slope":r["calibration_slope"],"ece":r["ece"],"high_confidence_count":r["high"]["count"],"high_confidence_coverage":r["high"]["coverage"],"high_confidence_false_safe":r["high"]["false_safe_rate"],"input_variables":m["input_count"],"total_fitted_scalars":m["coeff"]+m["thresholds"]+m["hyper"]+m["cal"]})
    pd.DataFrame(table).sort_values(["family","brier"]).to_csv(out/"validation_metrics.csv",index=False); (out/"selection.json").write_text(json.dumps(selection,indent=2)); (out/"tuning.json").write_text(json.dumps(tuning,indent=2)); (out/"model_metadata.json").write_text(json.dumps({m["name"]:{k:v for k,v in m.items() if k not in {"predict"}} for m in models},indent=2)); pd.DataFrame({"row_id":validation.row_id,"hosted":yv,"forcing_family":validation.forcing_family,**predictions}).to_csv(out/"validation_predictions.csv",index=False)
    lock={"stage":"3.2","best_cvt":best_cvt,"best_baseline":best_base,"training_sha256":HASHES["training.csv"],"validation_sha256":HASHES["validation.csv"],"selection_sha256":sha(out/"selection.json"),"tuning_sha256":sha(out/"tuning.json"),"metrics_sha256":sha(out/"validation_metrics.csv"),"predictions_sha256":sha(out/"validation_predictions.csv"),"final_test_opened":False,"confirmatory_test_authorized":False}; (out/"model_lock_manifest.json").write_text(json.dumps(lock,indent=2)); return selection


def main():
    p=argparse.ArgumentParser(); p.add_argument("--data",default="results/stage3_1"); p.add_argument("--output",default="results/stage3_2"); p.add_argument("--bootstrap-resamples",type=int,default=2000); a=p.parse_args(); print(json.dumps(run(a.data,a.output,a.bootstrap_resamples),indent=2))

if __name__=="__main__": main()
