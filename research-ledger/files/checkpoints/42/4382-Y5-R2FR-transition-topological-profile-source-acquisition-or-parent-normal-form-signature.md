# 4382: topological profile source acquisition or parent normal-form signature

Marker: `PPC4161_TRANSITION_TOPOLOGICAL_PROFILE_SOURCE_ACQUISITION_OR_PARENT_NORMAL_FORM_SIGNATURE_4382`

## What changed

- Tried the parent normal-form proof route and kept it unsigned rather than overclaiming.
- Derived the center-offset envelope `E_1^top <= 4 sqrt(pi)b/R`, `E_2^top <= 6 sqrt(pi)(b/R)^2`.
- Applied that envelope to every 4378 topological support row.
- Converted the next target into a precise demand: parent-center lock `b=0`, or first real `b/R` / profile input.

## Decision

| decision_id | decision | summary | next_target | why_next |
| --- | --- | --- | --- | --- |
| DEC4382_0 | PARENT_NORMAL_FORM_UNSIGNED_PROFILE_SOURCE_MISSING_CENTER_OFFSET_ENVELOPE_DERIVED_NONCLAIM | 4382 attempts the parent normal-form signature and keeps it unsigned: no current parent file proves radial defect, common-center isotropy, or Laplacian-null representative for the raw topological/Hamiltonian density. Instead of stopping there, it derives the separated-center envelope law. Dipole leakage obeys E_1^top <= 4 sqrt(pi) b/R and quadrupole leakage obeys E_2^top <= 6 sqrt(pi) (b/R)^2, then applies these laws to every 4378 Sun/Mercury/Venus/Earth/Mars and Earth/Moon support row. The result is a concrete required center-lock/profile-input interface, not a claim. | 4383-Y5-R2FR-transition-parent-center-lock-or-first-real-profile-input-pack.md | The next useful object is now specific: either prove b=0 by parent center lock or supply the first real b/R or rho_H/rho_top profile input. |

## Next target

| next_id | target | question | preferred_route | fallback_route | avoid |
| --- | --- | --- | --- | --- | --- |
| NT4382_0 | 4383-Y5-R2FR-transition-parent-center-lock-or-first-real-profile-input-pack.md | Can the parent lock the topological/Hilbert profile centers together, or can a real profile/offset value be supplied? | derive parent center lock b=0 before readout from source-readout descent and Hilbert/topological profile ownership. | fill first b/R or rho_H/rho_top profile input and run the center-offset/profile quadrature rows. | claiming from symbolic envelope rows, synthetic smoke data, old q_loc surrogates, total charge or metric-nullity. |
