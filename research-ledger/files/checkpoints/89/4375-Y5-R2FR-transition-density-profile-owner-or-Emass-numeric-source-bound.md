# 4375: density-profile owner or E_mass numeric source bound

Marker: `PPC4161_TRANSITION_DENSITY_PROFILE_OWNER_OR_EMASS_NUMERIC_SOURCE_BOUND_4375`

## What changed

- Derived the conditional Hilbert density-profile theorem: same `T_H(n,n)/c^2` source density gives `E_profile=0`.
- Kept the source-shadow/topological wrong-distribution countermodel because total mass equality is not profile equality.
- Added the exact Green transfer for retained `sigma_perp`.
- Added `E_profile <= delta_N/K_N(s)` source-density input gates.

## Decision

| decision_id | decision | summary | next_target | why_next |
| --- | --- | --- | --- | --- |
| DEC4375_0 | DENSITY_PROFILE_OWNER_THEOREM_DERIVED_SOURCE_SHADOW_COUNTERMODEL_RETAINED_EPROFILE_BOUND_READY_NONCLAIM | 4375 derives the exact density-profile owner theorem: if the active bulk source density is the same Hilbert T00 density T_H(n,n)/c^2 from the same S_vis/S_src before readout, then rho_eff=rho_H pointwise and E_profile=0. This is stronger and cleaner than total mass equality. The current corpus has private conditional support from 185/226/187/194/191, but the full claim is blocked by the source-shadow/topological wrong-distribution countermodel and by branch-global readout/profile ownership. Fallback is now scoreable: sigma_perp is defined, deltaPhi_profile has a Green integral, and E_profile <= delta_N/K_N(s) is ready once a real profile or theorem-zero certificate exists. | 4376-Y5-R2FR-transition-source-shadow-ban-or-Eprofile-first-source-density-row.md | the source-shadow ban is the exact missing clause between private Hilbert T00 density and claim-grade E_profile=0. |

## Next target

| next_id | target | question | preferred_route | alternate_route | avoid |
| --- | --- | --- | --- | --- | --- |
| NT4375_0 | 4376-Y5-R2FR-transition-source-shadow-ban-or-Eprofile-first-source-density-row.md | Can the source-shadow/topological wrong-distribution countermodel be forbidden, or must E_profile receive its first real density row? | derive no source-shadow density from same-action Hilbert derivative, Noether exchange connectivity, and source-label grammar | fill rho_H/rho_eff profile input rows and score E_profile through the Green/K_N gate | using total charge equality or calibrated visible matter alone as a density-profile proof |
