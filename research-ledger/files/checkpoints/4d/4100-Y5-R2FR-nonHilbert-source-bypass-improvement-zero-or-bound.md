# 4100 - Non-Hilbert Source Bypass Improvement Zero Or Bound

## Purpose

4099 made source-weight rows an official fallback and exposed the next density/source-current gate: non-Hilbert source bypass. 4100 separates the narrow exact-improvement zero from the live bypass channels.

- Decision: `EXACT_DMU_IMPROVEMENT_ZERO_ACCEPTED_AS_PARTIAL_THEOREM_TOTAL_NONHILBERT_BYPASS_RETAINS_OFFICIAL_ABSOLUTE_SUM_FALLBACK`
- Public density/source-current claim: `false`
- Public Newton/local-GR claim: `false`

## Partial Theorem

A genuine exact improvement can be silent only in the classified case:

```text
L' = L + dmu
fixed tau, fixed surface, no corner/topological remainder, no readout dependence
delta(i_tau mu) - i_tau(delta mu) = 0
```

This is useful, but narrow. It only handles `E_improvement` subcases.

## Live Non-Hilbert Channels

```text
J_active = J_H + J_NH
J_NH = J_spin/torsion + J_boundary/worldtube + J_readout
     + J_improvement + J_shadow/projector + J_decoupled
```

Total silence requires every component to vanish or be bounded. Until then:

```text
epsilon_current_owner_NH_abs = sum_abs(E_i)
```

with no cancellation between unsigned channels.

## Next Target

`4101-Y5-R2FR-spin-torsion-hypermomentum-silence-or-P4-bound.md` should take the clean GR-like fork: either no independent `Gamma_ind/omega_ind` appears in the local source/readout action, or the theory carries official P4 spin/torsion/hypermomentum residual coefficients.

## Outputs

- `P8_Y5_R2FR_4100_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4100_NONHILBERT_BYPASS_THEOREM.csv`
- `P8_Y5_R2FR_4100_COMPONENT_GATES.csv`
- `P8_Y5_R2FR_4100_OFFICIAL_FALLBACK_ROWS.csv`
- `P8_Y5_R2FR_4100_DENSITY_IMPACT.csv`
- `P8_Y5_R2FR_4100_DECISION_GATE.csv`
- `P8_Y5_R2FR_4100_CLAIM_GATE.csv`
- `P8_Y5_R2FR_4100_NEXT_TARGET.csv`
- `P8_Y5_R2FR_4100_STATUS.csv`
- `P8_Y5_BRR545_4100_VALIDATION.csv`
