# 4095 - Yloc No-Linear-Source Symmetry Or Source-Current Bound

## Purpose

4094 reduced the nonprojector `R11` obstruction to a sharp local question: can the parent theory prove `Y_loc=0`, rather than assuming a local-vacuum plateau? 4095 attacks the hardest part of that proof: forbidding the linear source and boundary terms that would drive `Y_loc` away from zero.

- Decision: `EXCHANGE_DOUBLET_PARENTIZATION_SELECTED_AS_BEST_NO_LINEAR_SOURCE_ROUTE_COMPONENT_MAP_AND_EVEN_SOURCE_ROWS_STILL_UNSIGNED`
- Public `Y_loc=0` claim: `false`
- Public local-GR/R11/gamma-beta claim: `false`

## The Forward Route

The best route is not a bare `Y_loc -> -Y_loc` rule. The cleaner route is exchange-doublet parentization:

```text
R_+^A <-> R_-^A
Z^A = (R_+^A - R_-^A)/2
R_even^A = (R_+^A + R_-^A)/2
S[Z] = S[-Z]  =>  J_Z = 0
B_Z = 0, M_AB > 0, Z^A = Y_loc^A  =>  Y_loc^A = 0
```

This is a real derivation target: if the parent action owns the doublets, matter sees only the even quotient, the boundary has no odd charge, and `Z^A` is the physical local residual, then the 4094 `Sigma_loc` double-zero mechanism activates.

## What Actually Improved

- The local branch now has a specific mechanism to chase, not a vague plateau axiom.
- `Y2` boundary flux and `Y3` domain vector look like plausible exchange-odd rows.
- `Y5` source normalization and `Y6` stress/Bianchi are the hard test: they are not naturally killed by oddness because even measured-GM/source/stress pieces can survive.
- A fallback source-current bound contract now exists, so a failed derivation turns into coefficient targets rather than hand-waving.

## No Claim Yet

This checkpoint does not prove local GR. It advances the proof path and blocks overclaiming. The unsigned clauses are exact exchange, even matter readout, zero odd boundary charge, the component identity `Z^A=Y_loc^A`, and even-source/stress accounting.

## Next Target

`4096-Y5-R2FR-exchange-doublet-component-map-or-even-source-normalization-split.md` should try to prove the component map directly. If `Y5` and `Y6` do not derive, they must become explicit bound/closure rows immediately rather than another long loop.

## Outputs

- `P8_Y5_R2FR_4095_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4095_NO_LINEAR_SOURCE_GATE.csv`
- `P8_Y5_R2FR_4095_EXCHANGE_DOUBLET_PARENTIZATION.csv`
- `P8_Y5_R2FR_4095_YLOC_COMPONENT_VERDICT.csv`
- `P8_Y5_R2FR_4095_SOURCE_CURRENT_BOUND_CONTRACT.csv`
- `P8_Y5_R2FR_4095_R11_IMPACT_UPDATE.csv`
- `P8_Y5_R2FR_4095_DECISION_GATE.csv`
- `P8_Y5_R2FR_4095_CLAIM_GATE.csv`
- `P8_Y5_R2FR_4095_NEXT_TARGET.csv`
- `P8_Y5_R2FR_4095_STATUS.csv`
- `P8_Y5_BRR545_4095_VALIDATION.csv`
