# 5418: v43 right-connector depth-17 sibling probe

## Decision

**PASS FOR BOTH DIRECT DEPTH-17 BOX CERTIFICATES ONLY.**

Both pending siblings close under the unchanged v43 production evaluator. They are now eligible for a short resume run that commits them into the adaptive ledger; this probe does not mutate or replace that ledger.

## Exact probes

- `LLDRDLDLDRDRDRDLD`: **PASS**, denominator `0.00039811219512990128`, Jacobian `11.247125919617027`; elapsed `60.383 s`.
- `LLDRDLDLDRDRDRDLU`: **PASS**, denominator `0.00061355607710515713`, Jacobian `3.9339400111296587`; elapsed `71.904 s`.

## State discipline

The production status, adaptive state, and accepted-row ledger are hash-identical before and after both probes. No probe row is represented as a committed production transition.

## Claim boundary

Regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.
