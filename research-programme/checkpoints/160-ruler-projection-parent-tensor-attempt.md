# 160 - Ruler Projection Parent Tensor Attempt

Private parent-theory checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 159 set the no-smuggling rule:

```text
BAO may only get a special response if the response is a two-point ruler
transport, not a hidden universal metric/clock deformation.
```

This checkpoint tries to construct the missing object:

```text
R^A_B[D,Q].
```

Short answer:

```text
we can construct the right algebraic parent tensor shape;
we have not yet derived the source law that fills it.
```

That is progress, but not promotion.

## 2. Machine Artifact

Script:

```text
scripts/ruler_projection_parent_tensor_attempt.py
```

Run:

```text
runs/20260531-235959-ruler-projection-parent-tensor-attempt
```

Generated:

```text
source_register.csv
projection_target_decomposition.csv
single_scalar_restriction_tests.csv
tensor_candidate_ledger.csv
source_law_targets.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
ruler_parent_tensor_decomposition_found_source_law_missing
```

Claim ceiling:

```text
ruler_parent_tensor_attempt_no_bridge_promotion
```

## 3. Candidate Parent Tensor

Use the observer spatial projector:

```text
h^A_B = P_perp^A_B + n^A n_B.
```

The cleanest radial/screen two-point transport tensor is:

```text
R^A_B = delta^A_B + T_D h^A_B + S_D(n^A n_B - h^A_B/3).
```

This gives:

```text
Pi_perp     = T_D - S_D/3
Pi_parallel = T_D + 2S_D/3.
```

Therefore:

```text
T_D = (2Pi_perp + Pi_parallel)/3
S_D = Pi_parallel - Pi_perp.
```

This matters because it is one tensor, not two disconnected BAO knobs.

But it only becomes physics if `T_D` and `S_D` are derived from:

```text
X_D, F_D, coherent-domain boundary/coframe invariants, or a parent transport
law fixed before BAO scoring.
```

## 4. Target Decomposition

Using the projection target from checkpoint 154:

| z | `Pi_perp` | `Pi_parallel` | `T_D` | `S_D` | readout |
|---:|---:|---:|---:|---:|---|
| 0.510 | -0.008172255615070512 | -0.0013682247495176991 | -0.005904245326552908 | 0.0068040308655528126 | same-sign low-z row |
| 0.706 | -0.0060951084586147175 | 0.002608091718097727 | -0.003194041733043903 | 0.008703200176712445 | opposed-sign row |
| 0.934 | -0.004042918437361043 | 0.006227888905899537 | -0.0006193159896075162 | 0.01027080734326058 | opposed-sign row |
| 1.321 | -0.0013461203206346362 | 0.0104068491524143 | 0.0025715361703816755 | 0.011752969473048935 | opposed-sign row |
| 1.484 | -0.0004489595015024772 | 0.011628614405088555 | 0.0035768984673612003 | 0.012077573906591033 | opposed-sign row |
| 2.330 | 0.00274552305479836 | 0.015182831800200747 | 0.006891292636599156 | 0.012437308745402387 | same-sign high-z row |

Two facts jump out:

```text
T_D changes sign: -0.005904245326552908 -> +0.006891292636599156.
S_D stays positive: +0.0068040308655528126 -> +0.012437308745402387.
```

So the target is not just "add one scalar".

It looks like:

```text
a sign-changing trace/ruler strain
+
a positive screen/radial quadrupole transport.
```

## 5. What Fails

The machine restriction tests are blunt:

| route | constraint | result |
|---|---|---|
| pure isotropic scalar | `Pi_parallel = Pi_perp` | fail |
| pure trace-free quadrupole | `Pi_parallel = -2Pi_perp` | fail |
| best fixed-ratio scalar | `Pi_parallel = k Pi_perp` | fail |
| trace + quadrupole tensor | `R = I + T h + S(n n - h/3)` | algebraic pass; source laws missing |
| one scalar plus derivative | `T,S` from one transport scalar and radial derivative | open theorem target |

This is the most useful part of the checkpoint:

```text
one scalar amplitude alone is too small a glove;
two arbitrary BAO functions are too dirty;
one tensor with trace + quadrupole is the clean middle route.
```

## 6. Important Interpretation

The quadrupole here must not mean:

```text
the FLRW universe has a physical preferred direction.
```

It has to mean:

```text
the observed BAO ruler has different radial and screen response because it is a
two-point observable in an observer coframe.
```

That is allowed in principle because BAO has:

```text
radial separation inferred through redshift interval,
transverse separation inferred through angular interval.
```

But if this tensor is secretly:

```text
delta g_mu_nu,
a photon-geodesic deformation,
or a global redshift clock map,
```

then SN, H(z), lensing, and local clocks must inherit it. That route is already demoted by checkpoints 157-159.

## 7. Source-Law Targets

The future parent action must now derive one of these:

| target | symbol | required profile | status |
|---|---|---|---|
| trace ruler strain | `T_D(z)` | sign-changing, about `[-0.0059, +0.0069]` | not derived |
| screen/radial quadrupole | `S_D(z)` | positive, about `[+0.0068, +0.0124]` | not derived |
| pair-vs-one-point split | `delta D_L_SN=0`, `delta ell_BAO != 0` | SN/H(z) null but BAO active | not derived |
| pre-data shape lock | `T_D,S_D = functions[X_D,F_D,...]` | no row-wise fitting | not derived |

The promising escape hatch is:

```text
T_D and S_D may not need to be two independent fields.
```

They might come from:

```text
one ruler-transport scalar plus its radial/screen derivative response.
```

But that has to be derived as a two-point ruler operator, not reused as a global clock map.

## 8. Gates

| gate | status | readout |
|---|---|---|
| source paths | pass | all required sources exist |
| tensor decomposition | pass algebraic | one tensor can represent the target |
| pure isotropic scalar | fail | cannot handle radial/transverse split |
| pure trace-free quadrupole | fail | target has nonzero sign-changing trace |
| one parent tensor | conditional pass | tensor object exists; source laws missing |
| source-law derivation | fail open | `T_D`, `S_D`, or scalar+derivative law not derived |
| SN/H(z) immunity | fail open | one-point null response still theorem target |
| promotion | fail | no bridge/local-GR/CMB claim |

## 9. Decision

Current fair status:

```text
ruler_parent_tensor_decomposition_found_source_law_missing
```

Meaning:

```text
we have a clean algebraic tensor target;
pure scalar and pure trace-free versions fail;
the viable route needs trace plus screen/radial quadrupole structure;
the parent theory must derive the trace/quadrupole source law before this is a
field-theory bridge.
```

Boxing-card readout:

```text
This is not a knockout.
But it is a cleaner stance.
We are not swinging random BAO patches now;
we have a specific combination to train:
trace footwork plus radial/screen counterpunch.
```

## 10. Next Target

Create:

```text
161-trace-quadrupole-source-law-attempt.md
```

Task:

```text
derive T_D and S_D from coherent-domain/coframe ruler transport, or show that
only an empirical closure can supply them.
```

Pass condition:

```text
a pre-data formula predicts the sign-changing T_D and positive S_D profiles,
keeps B_mem -> 0 identity, keeps local silence, and derives SN/H(z) immunity.
```

Fail condition:

```text
T_D and S_D can only be chosen after looking at DESI rows.
```
