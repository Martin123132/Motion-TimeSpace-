# 3943 - MHref Positive Same-Frame Reference Charge or Rkernel Source Row

Timestamp: `2026-07-01T12:55:54+00:00`

## Result

3943 locks the denominator/reference-charge problem into a proper source contract.

The denominator is:

`M_H_ref := c^-2*(H_tau[S_link;Phi_source]-H_ref[branch])`.

It is not `mu_fit/G_*`, not orbital `GM`, and not a readout calibration knob.

## Conditional Theorems

Positive denominator route:

`M_H_ref >= M_EH*(1-epsilon_abs)`, where `epsilon_abs=sum_i |Delta_i|/(G_* M_EH)`.

So if `M_EH>0` and `epsilon_abs<1`, then `M_H_ref>0` without importing orbital GM.

Homogeneous reference-charge anchor:

`W_source=empty and J_H=0 and Z_ref_selector and Z_no_boundary_mass and Z_same_tau_surface => H_tau[u_hom]-H_ref[u_hom]=0`.

Therefore:

`Z_ref_charge and M_H_ref>0 and Z_no_incoming and Z_same_tau_surface and Z_no_extra_boundary_charge => R_kernel/M_H_ref=0`.

## Current Verdict

- Progress: `M_H_ref` is now a strict same-frame Hamiltonian source denominator.
- Progress: the homogeneous reference-charge zero is a conditional empty-source theorem, not a calibration trick.
- Blocker: no claim-grade `M_EH`, `epsilon_abs`, `M_H_ref_lower`, or boundary/reference component row is filled yet.
- Public claim: blocked.

## Source Register

- Source rows found: `17/17`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3943_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3943_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3943_MHREF_REFERENCE_CHARGE_THEOREM.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3943_MHREF_SOURCE_ROW_TEMPLATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3943_HOMOGENEOUS_REFERENCE_ANCHOR.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3943_RKERNEL_FIRST_BOUND_ROW.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3943_CLAIM_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3943_NEXT_TARGET.csv`

## Next Target

`3944-Y5-R2FR-MHref-source-energy-comparator-and-residual-lower-bound-row.md`
