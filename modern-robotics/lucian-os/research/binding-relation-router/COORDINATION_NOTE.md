# Coordination note

This research line is owned by the KERNEL workstream under the cross-chat coordination protocol.

Canonical coordination surfaces:
- `00_START_HERE/` on the active navigation branch / PR #51 until landed
- GitHub issue #53 `[Lucian OS] Coordination Hub`

The Binding Relation Router and Structural Traversal work should be treated as source material for the minimal kernel vertical slice, not as a separate competing architecture.

Current integration boundary:

```text
ProblemFrame / semantic task representation
-> requirement / binding relation
-> capability + competence evidence
-> routing disposition
-> authority state
-> action proposal or HOLD / ESCALATE / REFUSE
-> verification / provenance handoff
```

Do not expand this research line into mixed-blocker BRR-003 or another large conceptual layer while the Control Room's current priority is kernel integration, unless a new discriminating dependency is explicitly accepted through the coordination layer.
