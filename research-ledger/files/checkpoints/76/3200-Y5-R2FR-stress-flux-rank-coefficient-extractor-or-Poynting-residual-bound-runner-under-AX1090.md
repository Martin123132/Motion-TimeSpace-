# 3200 - Stress-Flux Rank Coefficient Extractor Or Poynting Residual Bound Runner Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, Maxwell derivation, EM unification claim, rank-four proof, R10 pass, clock pass, orbital pass, or public-facing result.

## Result

3200 separates two jobs that were getting tangled:

```text
Poynting flux: quiet local zero/bound channel.
Rank-four J_Aa: parent MTS/matter stress-flux problem.
```

This is a useful narrowing. The Poynting vector belongs in the stress-energy flux story, but in quiet local PPN-style tests it should usually vanish or be small. If it were large and unsuppressed, it would damage local-GR safety rather than fix it.

## Poynting Zero Or Bound Law

- `PZT3200_00`: `quiet_static_no_radiation_no_magnetic_flux` - S = E x H gives n dot S = 0, so T_EM^{0i} contributes no normal energy flux Caveat: zero Poynting energy flux does not imply zero Maxwell spatial stress or zero EM self-energy
- `PZT3200_01`: `electrostatic_bound_field` - Poynting flux can vanish while T_EM^{ij} and energy density remain nonzero Caveat: composition/EM self-energy still belongs in WEP/PPN source-coupling bounds
- `PZT3200_02`: `static_crossed_fields_or_circulating_field_momentum` - |n dot S| <= |E||H| supplies a finite residual bound Caveat: circulating Poynting flow is not automatically a source of four independent C1 mismatch responses
- `PZT3200_03`: `radiative_or_time_dependent_EM` - Poynting flux is live and must be source-backed/bounded Caveat: using radiation flux to repair local static GR would be the wrong limit

The clean quiet theorem target is:

```text
if H_radiative = 0 and n dot(E x H_static) = 0,
then n dot S = 0 for the Poynting subchannel.
```

This does **not** zero full EM stress-energy. Electrostatic self-energy and Maxwell spatial stress remain separate source-coupling/WEP concerns.

## J_Aa Extractor

The four local gluing mismatch slots are:

```text
z = (Delta_F_L, Delta_Fprime_L, Delta_F_R, Delta_Fprime_R).
```

3200 stages all 16 coefficient slots:

```text
J_Aa = partial C_A / partial z^a at z=0.
```

Template rows staged: 16.

But every row is still `MISSING_PARENT_COEFFICIENT`; that is honest because no parent stress-flux evaluator exists yet.

## Rank Audit

- `RCA3200_00_quiet_Poynting_only`: rank `0`, passes rank-four `false` - Poynting theorem-zero channel cannot own rank-four local gluing
- `RCA3200_01_single_live_Poynting_flux`: rank `1`, passes rank-four `false` - a single energy-flux channel gives at most rank one
- `RCA3200_02_symmetric_matter_shell`: rank `2`, passes rank-four `false` - symmetric left/right response duplicates rows and cannot prove rank four
- `RCA3200_03_full_parent_flux_toy`: rank `4`, passes rank-four `true` - rank four is mathematically possible if parent MTS/matter stress supplies four independent coefficients

The only rank-four row is a conditional toy target, not evidence. It shows the shape needed, not that MTS already owns it.

## Bound Runner

- `PBR3200_00`: `normal_Poynting_flux_density` - |n dot S| <= |E| |H|
- `PBR3200_01`: `dimensionless_EM_flux_residual` - B_EM <= |tau_EM| S_normal_bound / M_H_ref
- `PBR3200_02`: `quiet_zero_certificate` - if H_radiative=0 and n dot(E x H_static)=0 then B_obs_EM_Poynting_over_MH=0 for the Poynting subchannel

## Decision

`POYNTING_DEMOTED_FROM_RANK_OWNER_TO_ZERO_OR_BOUND_CHANNEL`.

Claim status: `NO_LOCAL_GR_MAXWELL_PPN_OR_RANK4_CLAIM`.

Decision: quiet local Poynting is a theorem-zero/bound target, while rank-four J_Aa must come from parent MTS/matter stress-flux coefficients

Best next route: target K_hat/T_MTS plus matter-source flux as the possible four-channel owner; keep Poynting in the residual ledger

Next target:

```text
3201-Y5-R2FR-MTS-matter-stress-flux-four-channel-owner-or-rank-no-go-under-AX1090
```

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3200_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3200_POYNTING_ZERO_OR_BOUND_THEOREM.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3200_STRESS_FLUX_J_COEFFICIENT_TEMPLATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3200_RANK_CONTRIBUTION_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3200_POYNTING_BOUND_RUNNER_SCHEMA.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3200_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3200_VALIDATION.csv`

## Validation

- `VAL3200_00_inputs_exist`: `true` - inputs=8
- `VAL3200_01_poynting_zero_cases_recorded`: `true` - cases=4
- `VAL3200_02_j_template_complete`: `true` - 4 components x 4 mismatch slots
- `VAL3200_03_quiet_poynting_rank_zero`: `true` - Poynting theorem-zero channel cannot own rank-four local gluing
- `VAL3200_04_full_rank_only_conditional`: `true` - rank four is mathematically possible if parent MTS/matter stress supplies four independent coefficients
- `VAL3200_05_bound_schema_ready`: `true` - finite bound plus quiet zero certificate
- `VAL3200_06_no_claim_leak`: `true` - no local-GR, Maxwell, PPN, or rank-four claim
- `VAL3200_07_csv_parse`: `true` - P8_Y5_R2FR_3200_INPUTS.csv;P8_Y5_R2FR_3200_POYNTING_ZERO_OR_BOUND_THEOREM.csv;P8_Y5_R2FR_3200_STRESS_FLUX_J_COEFFICIENT_TEMPLATE.csv;P8_Y5_R2FR_3200_RANK_CONTRIBUTION_AUDIT.csv;P8_Y5_R2FR_3200_POYNTING_BOUND_RUNNER_SCHEMA.csv;P8_Y5_R2FR_3200_DECISION.csv

All generated rows remain `valid_for_claim=false`.
