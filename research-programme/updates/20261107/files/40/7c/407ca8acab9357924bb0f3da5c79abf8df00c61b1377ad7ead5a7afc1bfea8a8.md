# Stage69 sources and ownership

Consulted 7 October 2026. No new observational data were downloaded.

- Ma and Bertschinger, Cosmological Perturbation Theory in the Synchronous
  and Conformal Newtonian Gauges (1995):
  https://arxiv.org/abs/astro-ph/9506072
  Gauge conventions, species equations and regular first-order initial data.
- Pitrou, The radiative transfer at second order: a full treatment of the
  Boltzmann equation with polarization (2009 revision):
  https://arxiv.org/html/0809.3036v2
  Screen transport, changes of frame, collision moments, thermal/recoil
  distinction. Existing physics, not a claim of a new scattering theory.
- NIST CODATA 2022:
  https://physics.nist.gov/cuu/Constants/Table/allascii.txt
  Reuse the saved Stage67 source and its constants:
  `../thomson-source-coupling-20261007/sources/nist-codata-2022.txt` and
  `../thomson-source-coupling-20261007/results/calibration/status.json`.
- Official Geant4 Compton-scattering reference, already sourced in Stage67:
  https://geant4.web.cern.ch/documentation/dev/prm_html/PhysicsReferenceManual/electromagnetic/gamma_incident/compton/compton.html
  Its free-electron Klein-Nishina law supplies a recoil diagnostic, not a
  full thermal-Compton implementation.

Read-only local derivation/calibration dependencies:

- `../adiabatic-boundary-and-screen-transport-20261007/boundary_common.py`
- `../adiabatic-boundary-and-screen-transport-20261007/derive_matter_correction.py`
- `../adiabatic-boundary-and-screen-transport-20261007/results/stage-integrity.json`
- `../thomson-source-coupling-20261007/collision_common.py`
- `../thomson-source-coupling-20261007/runs/backgrounds/heavy.npz`
- `../thomson-source-coupling-20261007/runs/backgrounds/cold.npz`
- `../einstein-constraints-and-kinetic-response-20261007/constraint_common.py`
- `../einstein-constraints-and-kinetic-response-20261007/runs/native/heavy.npz`
- `../einstein-constraints-and-kinetic-response-20261007/runs/native/cold.npz`
- `../full-history-source-precision-20261007/runs/sources/unmatched-base.npz`
- `../full-history-source-precision-20261007/runs/sources/cold-base.npz`
- `../native-heavy-matching-20261007/native/fortran/constants.f90`
- `../native-heavy-matching-20261007/native/fortran/results.f90`
- `../native-heavy-matching-20261007/native/fortran/equations.f90`
- `../native-heavy-matching-20261007/native/camb/cambdll.dll`

The native comparison is an independently evolved first-order numerical
reference, NOT observed sky data and NOT an independent second-order code.
The latest reported actual data-fit authority remains
`../full-history-source-precision-20261007/results/production-primary-refit/status.json`.
