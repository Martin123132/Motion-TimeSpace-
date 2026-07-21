# 5111 - E020-primary control-extension runner

The restartable control-only runner is implemented, dry-run validated and
complete. All 180 predeclared controls converge.

The locked scope is exactly 180 jobs: twelve low seeds (`507611..507622`), fifteen arguments per seed, `E020` only, and `primary24` only. All 120 existing high-source jobs are present and converged. None of the 180 target jobs exists in or overlaps the protected v12 run.

The runner writes to a separate run directory. It can reuse 179 verified `E040` source topologies read-only; the one source row whose top-level crossing gate is false is deliberately not copied and will be reconstructed through the ordinary fail-closed topology path. The protected v12 run and `formalization-workbench` are hash guarded before and after every invocation.

Resume accepts only `COMPLETED_CONVERGED` rows with the exact config digest. Wrong-digest, unconverged, and failed rows are rejected. The wall-cap contract accepts at most four hours per invocation and stops on the first failed or unconverged job. Execution remains explicit (`--mode run`) and default-off.

Dry-run result:

- execution authorized: `true`;
- execution started: `false`;
- jobs: `180/180` unique;
- reusable topologies: `179`;
- guarded reconstruction: `1`;
- validation: `19/19` passed;
- run directory created: `false`.

The projected incremental calculation is still approximately `5.02 h`, so it should be split across resumable invocations. Completion would authorize checkpoint 5112 analysis, not an independent efficiency or MTS physics claim, because the v12 high data selected this estimator route.

Outputs:

- `scripts/Y5_R2FR_5111_E020_primary_control_extension_runner.py`
- `source-intake/functional_rg/5111/E020_primary_control_extension_activation.json`
- `source-intake/functional_rg/5111/E020_primary_control_extension_dry_run.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5111_VALIDATION.csv`

## Numerical execution and residue correction

The first numerical invocation stopped on a stable nonzero outer recoil
collision that contradicted the generalized 5084 zero theorem. Checkpoint
5112 isolated the direct component at arbitrary precision, retained the
nonzero, rejected the broad theorem and replaced prior zero uses with exact
event-local certificates.

Checkpoints 5113 and 5114 resolved later cross-additive ambiguities with a
fail-closed, source-separated arbitrary-precision classifier rather than more
label-based zero assumptions. Checkpoint 5115 extended that numerical
classifier to same-source direct `g1/g2` opposite-ownership pairs and retained
the first such stable nonzero value. No tolerance was relaxed.

Checkpoint 5116 recovered the run after an outer shell timeout at schedule
74. The next row then ran to completion but exhausted the adaptive integral
cap. Checkpoint 5117 derived and independently certified the applicable
same-orientation Cauchy cluster contour at 24 and 48 residue nodes. Their
values agree to `2.9371898151125674e-12`; both pass the unchanged `5e-5`
production convergence gate. The production replay converges in `93.17 s`
without relaxing any control.

Checkpoint 5118 reconciles the second capped continuation at `126/180`.
Checkpoint 5119 then proves that the S507622 projective cluster root is
independent of all fifteen finite E020 arguments. Its maximum factor-root
mismatch is `2.1965717747241423e-13`, with same-source separation
`0.003127198980147923`. The failed A00 row and the final fourteen jobs then
converge.

Final matrix state:

- `180/180` exact-digest jobs converged;
- `0` failed or unconverged;
- `0` missing;
- last row: schedule 180,
  `E020__S507622_N0000__A14__primary24`;
- status: `COMPLETE`.

Checkpoint 5120 executes the fixed-beta analysis. Its score
`1.5148246022524876` fails the locked `0.8` threshold while accepted runtime
`9.860421870944458 h` passes the ten-hour cap. Checkpoint 5121 attributes the
failure to broadly larger independent-control variance; no single-row
deletion or allocation allowed by the original budget rescues it. The
control route is rejected, while the completed matrices remain valid.
