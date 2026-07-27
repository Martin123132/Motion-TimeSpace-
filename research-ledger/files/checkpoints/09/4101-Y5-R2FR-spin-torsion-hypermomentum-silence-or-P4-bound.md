# 4101 - Spin/torsion/hypermomentum silence or P4 bound

## Verdict
4101 re-anchors the old spin/torsion result into the current 4100 chain: the local LC/no-independent-affine branch is now the clean private branch, and `E_spin` is zero inside that branch by variable absence.

That is real progress, but not a public local-GR claim. The still-missing leap is the selector: why the full parent MTS theory must choose this compact local LC branch rather than an affine/torsion/nonmetricity counterbranch. If that selector cannot be derived, the P4 queue is the honest fallback.

Decision: `LOCAL_LC_NO_INDEPENDENT_AFFINE_BRANCH_REANCHORED_E_SPIN_ZERO_INSIDE_BRANCH_SELECTOR_OR_P4_REQUIRED`

## Exact fork
- Route A: `Gamma_ind` and `omega_ind` are not variables of `S_loc^LC`; then `delta_Gamma S_i=0` sectorwise.
- Route B: an independent affine/spin connection is present; then `E_spin` must remain as explicit P4 residuals.
- No route is allowed where the affine coupling is unstated and then silently ignored.

## What is actually closed
- Matter/spin: closed inside the LC branch because spin transport uses `omega_LC[e_obs]`.
- EM/Poynting: affine-Gamma silent inside the LC branch; Poynting stress is Hilbert/coframe-owned, while `lambda_A/alpha` remains a separate coupling target.
- Source current: `delta_Gamma(Pi_M J_H)=0` only when `J_H` is Hilbert-owned and `Pi_M` is `q/e_obs/tau` natural.
- Projective trace: absent in the LC branch, not merely gauge-waved away.

## Not claimed
- No public local-GR, Newton, R10, WEP, clock, orbital or PPN pass follows from this checkpoint alone.
- No affine/torsion branch is numerically bounded yet.
- `B_LC_selector`, `K_spin`, `c_A`, `c_T`, `c_Q`, `K_projector_comm` and `D_X ln(lambda_A)` remain nonclaim rows.

## Outputs
- `P8_Y5_R2FR_4101_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4101_CONNECTION_FORK_THEOREM.csv`
- `P8_Y5_R2FR_4101_LC_BRANCH_SIGNATURE.csv`
- `P8_Y5_R2FR_4101_SECTOR_GAMMA_SLOT_VERDICT.csv`
- `P8_Y5_R2FR_4101_P4_FALLBACK_QUEUE.csv`
- `P8_Y5_R2FR_4101_DECISION_GATE.csv`
- `P8_Y5_R2FR_4101_CLAIM_GATE.csv`
- `P8_Y5_R2FR_4101_NEXT_TARGET.csv`
- `P8_Y5_R2FR_4101_STATUS.csv`
- `P8_Y5_BRR545_4101_VALIDATION.csv`

## Next target
- `4102-Y5-R2FR-local-LC-branch-selector-or-Kspin-P4-map.md`
- Objective: derive the local LC branch selector first; if that fails, source `K_spin` and the first affine torsion/nonmetricity coefficient map.
