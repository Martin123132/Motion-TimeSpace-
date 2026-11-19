# Which local entrypoints are authoritative

The stage was developed while its single-worker numerical checks ran.
Early `sources` snapshots include future helper drafts that were not
executed by that earlier worker. The final audit checks the transitive
local import closure of each executed entrypoint and requires all those
files to match the run's recorded hashes. It separately records changes
to unconsumed drafts rather than pretending an unrelated draft was part
of an earlier test. Upstream scientific sources keep their sealed hashes.

Executed scientific entrypoints:
- `probe_fibre.py`, `collect_mean.py`, `qualify_full.py`, `check_mean.py`.
- `collect_drift.py`: original half-family precision failure, preserved.
- `diagnose_drift.py`: localization diagnostic, not a pass claim.
- `repair_saved.py`: stable-row repair; original derivative width still
  fails in the Poisson branch, so its overall result is not accepted.
- `refine_drift.py`: accepted half-family controlled refinement, reusing
  the stable central packet and larger derivative offsets.
- `check_external_jet.py`: source-backed diagnostic on both models.
- `collect_stable_v2.py`: the same stable equations and qualified
  derivative widths for the two remaining inherited wavenumbers.

Final audit entrypoint: `audit_phase_v4.py`.
Final process/integrity seal entrypoint: `seal_stage_v3.ps1`.

The earlier `audit_phase.py`, `audit_phase_v2.py`, `audit_phase_v3.py`,
`seal_stage.ps1` and `seal_stage_v2.ps1` are unexecuted development
versions. Do not use them as the current acceptance route. The main
entrypoint of `collect_stable.py` is also superseded, although its
`live_rows` function is imported and tested by `refine_drift.py`.
`stable_analysis.py` is the original helper; the remaining-wavelength
runs use `stable_analysis_v2.py` with the qualified derivative widths.

No drafts are published by this stage. A later public export should use
the accepted result manifest and tested dependency closure, not blindly
copy every Python file or promote the two preserved failed result files.
