# 4156 - Pi_M/H_tau Same-Charge Glue Or Radial Source Residual

Timestamp UTC: `2026-07-02T11:22:01+00:00`  
Branch: `MTS_R2FR_Y5_PIM_HTAU_SAME_CHARGE_GLUE_4156`  
Decision: `PIM_HTAU_SAME_CHARGE_GLUE_REDUCED_TO_PARENT_CONSTRAINT_MAP_KERNEL_UNSIGNED_RADIAL_RESIDUAL_ROWS_READY`

## Purpose
4155 locked the source-measure/Poynting accounting conditionally. The remaining source-mass bottleneck is whether:

`M_H[Pi_M J_H_total]`

is the same object as

`H_tau[S_outer]-H_ref`.

## Non-Circular Route
Do not define `Pi_M` from fitted orbital `GM`.

Define the target:

`Delta_PiM := M_H[Pi_M J_H_total] - (H_tau[S_outer]-H_ref)`.

The selected route is:

`Pi_M^C := D_N[C_tau]|_{J_H[tau]}`.

That is, `Pi_M` is the parent constraint Dirichlet-to-Neumann / boundary-charge pushforward from Hilbert source current to exterior Hamiltonian charge.

## Same-Charge Theorem
The conditional theorem is:

`Pi_M^C J_H = J_M_top + dB_zero`

and

`M_H[Pi_M^C J_H]=H_tau[S_outer]-H_ref`

if:

- the parent exterior constraint map is unique;
- no homogeneous unsourced `1/r` mass kernel survives;
- `Pi_M^C` is a fixed chain map on the Hilbert current complex;
- `H_tau` is integrable as a covariant phase-space charge;
- reference subtraction is fixed and q-basic;
- linked surfaces, frame, units, and `tau` are parent-owned before readout;
- extra, boundary, symplectic, and EM fluxes are owned or bounded.

## Radial Residual Branch
The radial/source residual is:

`M_H(S2)-M_H(S1)=int_A d(Pi_M^C J_H)`.

If same-charge glue fails, retain:

`epsilon_charge <= |C_M|+|C_curl|+|I_commutator|+|R_eq|+|C_ref|+|C_frame|+|C_units|+|R_kernel|+|R_extra|+|R_symp|+|R_boundary|+|R_EM_flux|+|epsilon_G_norm|+|epsilon_PPN_source|`.

No cancellation credit is allowed unless a parent identity proves it.

## Current Verdict
| Gate | Result | Meaning |
|---|---|---|
| parent constraint-map route | SELECTED | non-circular `Pi_M` construction |
| chain-map closure | CONDITIONAL | `[d,Pi_M^C]J_H=0` if parent fixed |
| H_tau integrability | CONDITIONAL | curl/corner/reference terms must vanish |
| homogeneous mass kernel | UNSIGNED | next sharp blocker |
| radial source residual | EMITTED | no fitted-GM laundering |
| Newton/local GR | NOT CLAIMED | source glue still conditional |

## Outputs
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4156_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4156_CONSTRAINT_MAP_GLUE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4156_ZERO_THEOREM_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4156_RESIDUAL_VECTOR.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4156_RADIAL_SOURCE_ROWS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4156_NEWTON_IMPACT.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4156_DECISION_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4156_STATUS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4156_NEXT_TARGET.csv`

## Next Target
- `4157-Y5-R2FR-constraint-Green-kernel-zero-or-homogeneous-mass-residual.md`
- Prove the exterior constraint Green map has no homogeneous unsourced `1/r` mass mode, or retain `R_kernel` as explicit radial/source residual.
