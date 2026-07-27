# 3946 - Total Source Domain Closedness And Energy Condition Or First M_EH Value

Timestamp: `2026-07-01T13:18:27+00:00`

## Result

3946 turns source closedness into a conservation-current theorem.

Define the same-frame total Hilbert energy current:

`J_tau^a := -T_total^{a b} tau_b`.

Then:

`nabla_a J_tau^a = -(nabla_a T_total^{a b}) tau_b - T_total^{a b} nabla_(a tau_b)`.

Integrated over the source worldtube:

`E_tau[Sigma_2]-E_tau[Sigma_1] = -Phi_wall[J_tau] + integral_Omega R_div dV`.

So a closed stationary source is not an axiom. It is the condition:

`Phi_wall = 0`, total Ward/Bianchi residuals vanish, `tau` is stationary/Killing to the required order, and no EM tail/Poynting/apparatus/theta channel is unassigned.

## Poynting / Wave Clause

Poynting flux now has a precise role:

- stationary/circulating field momentum can be inside `T_total`;
- radiative or crossing Poynting flux is `Phi_wall` / `epsilon_Poynting_flux`;
- MTS cannot claim local-GR source positivity while hiding this flux.

## M_EH Positivity Gate

The exact route is now:

`Z_MEH_positive := Z_closed_domain and Z_energy_condition and Z_nonzero_support and Z_sourceblind_ref`.

The finite fallback is:

`M_EH >= c^-2 E_pos*(1-epsilon_neg-epsilon_closed)`.

This means negative binding/stabilizer/material sectors must be theorem-owned or bounded. No magic roof-ladder trick.

## Current Verdict

- Progress: conservation-current/domain theorem derived.
- Progress: Poynting flux converted into an explicit wall/flux residual.
- Progress: M_EH positivity reduced to `DEC/WEC/positive-energy theorem` or `epsilon_neg+epsilon_closed<1`.
- Blocker: source-domain residual components are not numeric/theorem-zero yet.
- Blocker: total Hilbert source positive-energy condition is not parent-signed yet.
- Public claim: blocked.

## Source Register

- Source rows found: `16/16`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3946_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3946_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3946_CONSERVATION_CURRENT_THEOREM.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3946_TOTAL_SOURCE_DOMAIN_CERTIFICATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3946_ENERGY_CONDITION_CERTIFICATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3946_POYNTING_AND_WALL_FLUX_BOUND_LAW.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3946_MEH_POSITIVITY_CERTIFICATE_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3946_CLAIM_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3946_NEXT_TARGET.csv`

## Next Target

`3947-Y5-R2FR-total-Hilbert-source-positive-energy-or-negative-sector-bound.md`
