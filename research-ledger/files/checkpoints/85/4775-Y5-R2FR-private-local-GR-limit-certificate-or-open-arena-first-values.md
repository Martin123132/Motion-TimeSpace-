# 4775 — Private Local-GR Limit Certificate or Open-Arena First Values

Generated: `2026-07-08T03:47:32+00:00`

## Result

4775 consolidates the newest local result:

```text
Qbar_XH_abs = 0_private_C_static_iso_denominator_locked
```

with the earlier GR selector chain. The clean statement is:

```text
MTS now has a disciplined private/effective local-GR branch.
```

Inside the branch:

```text
G_mu_nu[g_obs] + Lambda_eff g_obs_mu_nu = kappa_eff T_H_mu_nu
nabla^2 Phi_N = 4*pi*G_cal*rho_H
nabla_mu F^mu_nu = J^nu
Delta_PPN = 0
G_cal = c^4*kappa_eff/(8*pi)
```

But this is still not:

```text
a public parent-action derivation of GR,
a prediction of the numerical value of G,
or an empirical R10/PPN/orbital/clock pass.
```

## Private Local-GR Certificate

| certificate_id | object | statement | status |
| --- | --- | --- | --- |
| CERT4775_0_branch | private branch definition | B_loc^private := C_static_iso_private ∩ PPC4161-TK-HQ ∩ MEH_private_selector ∩ B_GR_selector | PRIVATE_LIMIT_BRANCH_DEFINED |
| CERT4775_1_GR_equation | local Einstein-form field equation | If B_GR_selector is active, G_mu_nu[g_obs]+Lambda_eff g_obs_mu_nu = kappa_eff T_H_mu_nu + E_fail_mu_nu. | CONDITIONAL_EINSTEIN_FORM |
| CERT4775_2_residual_zero | private compact residual | Inside B_loc^private, Qbar_XH_abs=0_private_C_static_iso_denominator_locked and tail/source projector defects are routed to zero. | PRIVATE_RESIDUAL_ZERO_CERTIFIED |
| CERT4775_3_conservation | Bianchi and source conservation | D_A kappa_eff=0, common Hilbert source and Maxwell/matter exchange give nabla_mu T_H^mu_nu=0 in the branch. | CONSERVATION_GATE_PRIVATE |
| CERT4775_4_Newton | Newtonian limit | Weak/static/slow EH 00 equation gives nabla^2 Phi_N=4*pi*G_cal*rho_H and a=-grad Phi_N. | NEWTON_LIMIT_PRIVATE_CALIBRATED_G |
| CERT4775_5_Maxwell | Maxwell and Poynting ownership | Common Hodge variation gives nabla_mu F^mu_nu=J^nu and Poynting is T_EM boundary/Hilbert flux, not a hidden background source. | MAXWELL_HODGE_STRESS_PRIVATE |
| CERT4775_6_PPN | local static PPN branch | EH metric block with no extra local source/readout couplings gives Delta_PPN=(gamma-1,beta-1,alpha_i,xi,zeta_i,Gdot/G)=0. | PPN_VECTOR_ZERO_PRIVATE_SELECTOR |
| CERT4775_7_claim_status | claim ceiling | public_local_GR_claim=false; numeric_G_prediction=false; open_arena_pass=false; parent_unique_branch=false. | NONCLAIM_FIREWALL_ACTIVE |

## Newton / Maxwell / PPN Limit Map

| map_id | limit_sector | private_branch_output | open_arena_residual |
| --- | --- | --- | --- |
| LM4775_0_field_equation | local GR | G_mu_nu+Lambda_eff g_mu_nu=kappa_eff T_H_mu_nu | E_fail_mu_nu reappears if any selector clause fails |
| LM4775_1_Newton_Poisson | Newtonian mechanics | nabla^2 Phi_N=4*pi*G_cal*rho_H | open branch keeps +(c^2/2)E_00 |
| LM4775_2_orbital | orbital acceleration | a_r=-G_cal*M_H^dress/r^2 plus standard multipoles | profile, boundary and E_00 integrals become explicit residuals |
| LM4775_3_Maxwell | EM field equations | nabla_mu F^mu_nu=J^nu; nabla_mu T_EM^mu_nu=-F_nu_lambda J^lambda | radiative/Poynting flux must be boundary or external sector |
| LM4775_4_PPN | PPN vector | Delta_PPN=(gamma-1,beta-1,alpha_i,xi,zeta_i,Gdot/G)=0 | open branch uses Pi_PPN residual transfer matrix |
| LM4775_5_G | calibrated coupling | G_cal=c^4*kappa_eff/(8*pi) | numeric G derivation/calibration remains a separate source-normalization target |

## Open-Arena First Values

| value_id | quantity | required_first_value | status |
| --- | --- | --- | --- |
| FV4775_0_Gcal | G_cal/kappa_eff normalization | units, convention and one calibration source row | MISSING_CALIBRATION_SOURCE_ROW |
| FV4775_1_MH_dress | M_H^dress | Hamiltonian worldtube mass or accepted comparator mass with same-frame units | MISSING_SOURCE_BACKED_MASS_ROW |
| FV4775_2_E00 | E_00 residual | bound or measured envelope for local non-EH/open residual in the observed metric frame | MISSING_OPEN_ARENA_E00_BOUND |
| FV4775_3_boundary_flux | F_boundary/Poynting/radiation flux | boundary flux ledger separating Hilbert EM flux from external/apparatus/radiative injection | MISSING_BOUNDARY_FLUX_LEDGER |
| FV4775_4_PPN_transfer | Pi_PPN residual transfer matrix | map from residual fields/readout drift to gamma,beta,alpha_i,xi,zeta_i,Gdot/G | MISSING_PPN_TRANSFER_MATRIX |
| FV4775_5_R10_alpha | alpha(lambda) local fifth-force row | source-backed amplitude and bound curve pair with no placeholder parent coefficients | MISSING_R10_NUMERIC_ROW |
| FV4775_6_orbital_profile | orbital profile/multipole residual | source profile, compact support, exterior surface and multipole/error budget | MISSING_ORBITAL_PROFILE_ROW |

## No-Circularity Audit

| audit_id | anti_circularity_rule | status |
| --- | --- | --- |
| NC4775_0_GR_not_assumed_public | B_GR selector is used as a sufficient effective branch, not claimed as globally parent-derived | PASS_PRIVATE_DISCIPLINE |
| NC4775_1_G_not_predicted | G_cal is calibrated; no numerical G prediction is inferred from M_lower positivity | PASS_FIREWALL |
| NC4775_2_Qbar_scope | Qbar_XH=0 is limited to the compact stationary collar denominator-locked branch | PASS_SCOPE_LOCK |
| NC4775_3_Maxwell_scope | Poynting vector is accounted as EM Hilbert/boundary flux, not promoted to a separate hidden background field | PASS_NO_SIDE_CHANNEL |
| NC4775_4_Newton_scope | Newtonian limit follows from EH weak-field equation with calibrated G and explicit residual E_00 | PASS_RESIDUAL_EXPLICIT |

## Residual Vector Policy

| policy_id | trigger | residual_name | required_route |
| --- | --- | --- | --- |
| RP4775_0_parent | parent selector unsigned | E_parent_selector | keep effective-branch language; do not claim global parent derivation |
| RP4775_1_EH | EH/local metric selector fails | E_EH_IR | route to non-EH operator coefficients and linearized residual tensor |
| RP4775_2_source | Hilbert source/common readout fails | E_source_label + E_readout | route to WEP/source-coupling residual vector |
| RP4775_3_boundary | radiation/Poynting/boundary flux is open | E_boundary_flux | score as boundary/external flux instead of zeroing it |
| RP4775_4_PPN | static private selector fails for PPN | Delta_PPN_open | use transfer matrix and source-backed bounds |
| RP4775_5_R10 | tail/source coefficients are nonzero or unsourced | alpha_tail(lambda) | compare with real alpha(lambda) bound curve only after numeric source rows exist |

## Route Selection

| route_id | route | selection_status |
| --- | --- | --- |
| RT4775_0_Gcal_first | Gcal normalization / source calibration first-value pack | SELECTED_NEXT |
| RT4775_1_PPN_open | open-arena PPN transfer matrix | QUEUED_AFTER_GCAL |
| RT4775_2_parent_unique | single parent action selector signature | LONGER_THEORY_TARGET |

## Decision

`PRIVATE_LOCAL_GR_LIMIT_CERTIFICATE_ASSEMBLED_FROM_4774_QBAR_LOCK_AND_4649_GR_SELECTOR_OPEN_ARENA_VALUES_AND_PARENT_SIGNATURE_STILL_REQUIRED_NONCLAIM`

## Next Target

`4776-Y5-R2FR-Gcal-normalization-or-open-arena-first-value-pack.md`
