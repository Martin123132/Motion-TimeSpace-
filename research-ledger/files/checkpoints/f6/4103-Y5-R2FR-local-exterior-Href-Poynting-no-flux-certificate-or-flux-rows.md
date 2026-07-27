# 4103 - Local exterior Href/Poynting no-flux certificate or flux rows

## Verdict
4103 moves the Poynting/Hamiltonian exterior gate forward instead of merely restating it. The public EM flux anchor is conditionally filled: for a stationary asymptotic public Maxwell branch with no radiative `O(R^-1)` field, `Phi_infty=0` because `n.(E x H)=O(R^-5)` and the sphere area is `O(R^2)`.

Carrying 3583/3584 forward, the same-package geometry problem collapses to one object: `E_stat=(D_ext,K,r,W_source,Sigma_tau,S_in,S_out,Phi_infty)`. If the parent exterior equations/data are `K`-invariant and the exterior solution is unique modulo gauge with no radiative homogeneous kernel, `E_stat` follows. If not, the honest residual is `epsilon_Estat`.

So the reduced annulus residual is now `R_ann_abs = C_EM_surface_gauge_abs + epsilon_Estat`. `H_ref` also gains internal credit: fixed-reference derivative silence is retained, but `M_H_ref` positivity and full `H_tau` curl remain open.

Decision: `POYNTING_ANCHOR_ZERO_CARRIED_ESTAT_UNIQUENESS_ROUTE_REANCHORED_HREF_INTERNAL_LOCK_RETAINED_DENOMINATOR_AND_HOMOGENEOUS_MODE_OPEN`

## What Closed Conditionally
- `Phi_anchor_abs=0` on the stationary asymptotic no-radiation public EM branch.
- Poynting transport is a theorem in a stationary source-free collar.
- Same-tau/surface/worldtube/no-seam clauses reduce to one `E_stat` certificate.
- `H_ref` source/readout derivative silence is internally signed in the fixed-reference candidate branch.

## What Remains Live
- `E_stat` is not parent-derived yet: uniqueness/no-homogeneous-mode, source-current ownership, and extra-field silence remain unsigned.
- `C_EM_surface_gauge_abs` remains a live gauge/corner residual.
- `M_H_ref_lower>0` still needs `M_EH` and residual component rows.
- Local GR/Newton/Maxwell/PPN claims remain blocked.

## Outputs
- `P8_Y5_R2FR_4103_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4103_LOCAL_EXTERIOR_CERTIFICATE.csv`
- `P8_Y5_R2FR_4103_PACKAGE_ACTIVATION.csv`
- `P8_Y5_R2FR_4103_HREF_DENOMINATOR_ROWS.csv`
- `P8_Y5_R2FR_4103_FLUX_RESIDUAL_STACK.csv`
- `P8_Y5_R2FR_4103_DECISION_GATE.csv`
- `P8_Y5_R2FR_4103_CLAIM_GATE.csv`
- `P8_Y5_R2FR_4103_NEXT_TARGET.csv`
- `P8_Y5_R2FR_4103_STATUS.csv`
- `P8_Y5_BRR545_4103_VALIDATION.csv`

## Next target
- `4104-Y5-R2FR-no-homogeneous-exterior-mode-or-extra-hair-epsilon-row.md`
- Objective: prove no radiative/time-dependent homogeneous exterior mode or retained extra-field hair survives the local stationary boundary class, or write `epsilon_hom_mode` and `epsilon_extra_hair` rows.
