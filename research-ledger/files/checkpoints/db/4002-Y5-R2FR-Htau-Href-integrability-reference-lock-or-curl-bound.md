# 4002 - Htau/Href Integrability Reference Lock Or Curl Bound

Timestamp: `2026-07-01T19:25:51+00:00`

## Result

`H_tau` is now treated as a Hamiltonian charge functional, not a name for whatever mass we need.

Define the covariant phase-space one-form

`alpha_tau[delta Phi] := int_S(delta Q_tau^MTS - i_tau Theta_total) - delta H_ref`.

`H_tau` exists path-independently only if

`d_field alpha_tau(delta_1 Phi, delta_2 Phi)=0`.

## Reference Lock

`H_ref=H_ref[Sigma_ref]` is legal only when `Sigma_ref` is fixed by boundary/topology/asymptotic data before source, radius, time, frame, readout, or orbital comparison.

The chain rule gives source-blindness only if `D_source Sigma_ref=0`; fitted mass, observed `GM`, residual sign, and post-hoc counterterms are forbidden inputs.

## Denominator Lock

`M_H_ref := H_tau[S_outer;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs] > 0`.

It must be same-frame, source-backed, unit-declared, and not imported from orbital `GM`.

## Bound If Closure Fails

`Delta_Htau_Href_4002 = |I_X|+|I_projector|+|I_boundary|+|I_ref|+|I_tau|+|I_surface|+|I_Dq|+|Delta_ref|+|C_frame|+|C_units|`.

This is the no-cancellation replacement for saying `H_tau/H_ref is missing`.

## Evaluator Results

- `CASE4002_0_integrable_fixed_reference_zero`: status `CONDITIONAL_ZERO_CLAUSES_UNSIGNED`, Delta `0.000000000000e+00`, zero=True, ref_guard=True, denom_guard=True, claim=False
- `CASE4002_1_parent_current_missing`: status `PARENT_THETA_QTAU_COMPONENTS_NONZERO`, Delta `1.000000000000e-05`, zero=False, ref_guard=True, denom_guard=True, claim=False
- `CASE4002_2_reference_drift`: status `REFERENCE_SELECTOR_DRIFT_NONZERO`, Delta `1.200000000000e-05`, zero=False, ref_guard=True, denom_guard=True, claim=False
- `CASE4002_3_tau_frame_units_leak`: status `TAU_FRAME_UNITS_NONZERO`, Delta `1.700000000000e-05`, zero=False, ref_guard=True, denom_guard=True, claim=False
- `CASE4002_4_fitted_reference_refused`: status `FITTED_REFERENCE_FORBIDDEN`, Delta `0.000000000000e+00`, zero=False, ref_guard=False, denom_guard=True, claim=False
- `CASE4002_5_orbital_denominator_refused`: status `ORBITAL_GM_DENOMINATOR_FORBIDDEN`, Delta `0.000000000000e+00`, zero=False, ref_guard=True, denom_guard=False, claim=False
- `CASE4002_6_missing_parent_rows`: status `MISSING_HTAU_HREF_COMPONENT_VECTOR`, Delta `MISSING`, zero=False, ref_guard=True, denom_guard=True, claim=False

## Verdict

We have the proper derivation contract: closed phase-space one-form plus fixed source-blind reference plus positive same-frame denominator. Current MTS has the route, not the claim.

## Next Target

The sharpest next move is parent current extraction: derive `Theta_total` and `Q_tau^MTS` from one parent action with retained sectors included, or fill the first source-backed curl component row.

- `4003-Y5-R2FR-parent-theta-Qtau-current-chain-or-integrability-source-row.md`
- `scripts/Y5_R2FR_4003_parent_theta_Qtau_current_chain_or_integrability_source_row.py`

## Source Count

- source needles found: `20/20`
