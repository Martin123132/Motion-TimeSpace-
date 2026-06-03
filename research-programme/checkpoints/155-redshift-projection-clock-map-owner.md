# 155 - Redshift Projection Clock-Map Owner

Private bridge-owner checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 154 left the BAO bridge in a useful but dangerous state:

```text
anisotropic/projective BAO route live;
parent observer-map owner missing;
Q^nu still deferred.
```

The next question is sharper:

```text
Can the scalar BAO redshift remap z_true = z_obs + zeta(z)
be owned by an MTS clock/observer map,
or is it only a fitted redshift closure?
```

Short answer:

```text
the required clock map is small and smooth enough to be a serious theorem target;
the existing locked memory activation does not derive it;
projection remains conditional, not promoted.
```

This is a live route, but it is not yet physics. It is footwork with no signed observer functional yet.

## 2. Machine Artifact

Script:

```text
scripts/redshift_projection_clock_map_owner.py
```

Run:

```text
runs/20260531-235959-redshift-projection-clock-map-owner
```

Generated:

```text
source_register.csv
clock_redshift_target.csv
clock_map_derivation_chain.csv
locked_memory_shape_comparison.csv
closure_fit_comparison.csv
clock_owner_route_matrix.csv
owner_contract.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
redshift_clock_map_target_quantified_not_parent_derived_projection_retained_conditional
```

Claim ceiling:

```text
redshift_clock_map_owner_not_promoted_no_BAO_CMB_support_claim
```

## 3. Clock-Map Relation

Use the observer-clock ansatz:

```text
1 + z_obs = (1 + z_FLRW) exp(Theta_clock).
```

For a small clock map:

```text
zeta = z_true - z_obs = -(1 + z_obs) Theta_clock + O(Theta_clock^2).
```

Therefore the BAO remap target from checkpoint 154 fixes:

```text
Theta_required(z) = -zeta(z)/(1+z).
```

Important caveat:

```text
a homogeneous universal lapse alone is gauge;
the clock map becomes physical only if the parent theory specifies
observer/matter clock coupling or a relative calibration map.
```

So this checkpoint is not allowed to claim:

```text
we changed the lapse, therefore BAO is solved.
```

It may only claim:

```text
this is the exact clock-map target a future parent action must derive.
```

## 4. Required Target

Machine target:

```text
max |Theta_clock|required = 0.0037397117654248964
max |zeta|required        = 0.012453240178864905
target clock sign crossing = true
```

Selected rows:

| z | zeta required | Theta required | Theta / B_mem |
|---:|---:|---:|---:|
| 0.510 | -0.0049074599105926806 | 0.0032499734507236296 | 0.043874641584769 |
| 0.706 | -0.0053842576907261385 | 0.003156071331023528 | 0.04260696296881763 |
| 0.934 | -0.005077215498300127 | 0.002625240691985588 | 0.03544074934180544 |
| 1.321 | -0.0026877365434193165 | 0.0011580079894094428 | 0.015633107857027477 |
| 1.484 | -0.001054547385704468 | 0.00042453598458311916 | 0.005731235791872109 |
| 2.330 | 0.012453240178864905 | -0.0037397117654248964 | -0.05048610883323611 |

Readout:

```text
the amplitude is tiny;
the shape is not wild;
but it changes sign.
```

That sign crossing is the whole fight. A monotone positive activation is not enough.

## 5. Existing Memory Shapes

The auditor tested the obvious locked shapes with both:

```text
u3 = 0.2429466120286312
u3 = 1/4
```

against:

```text
B_mem F(N),
B_mem [1-F(N)],
B_mem dF/dN,
B_mem d2F/dN2,
B_mem N/u3.
```

Result:

```text
single locked memory activation does not own the BAO redshift map.
```

Examples:

| candidate | sign matches | predicted sign crossing | status |
|---|---:|---|---|
| u3_fit_Bmem_times_F | 5/6 | no | fail_sign_structure |
| u3_fit_Bmem_times_tail_1_minus_F | 3/6 | no | fail_sign_structure |
| u3_fit_Bmem_times_dF_dN | 3/6 | no | fail_sign_structure |
| u3_fit_Bmem_times_N_over_u3 | 5/6 | no | fail_sign_structure |
| u3_quarter_Bmem_times_F | 5/6 | no | fail_sign_structure |
| u3_quarter_Bmem_times_N_over_u3 | 5/6 | no | fail_sign_structure |

This does not kill the projection route. It kills the cheap version:

```text
just reuse F(N) and call it a clock map.
```

## 6. Closure Fits

The target is smooth enough that simple redshift closures can fit it:

| closure | RMS theta residual | max theta residual | sign matches | status |
|---|---:|---:|---:|---|
| affine_in_load_N_closure | 0.0007235770095008313 | 0.0009748974723691466 | 5/6 | fail_sign_structure |
| quadratic_in_load_N_closure | 0.000039642300236917174 | 0.00004812631199293312 | 6/6 | fit_shape_but_unowned |

This is the key split:

```text
mathematically easy to fit;
physically not owned.
```

A quadratic in load `N` is not a field theory. It is a diagnostic that tells us the target is smooth, not that MTS has derived it.

## 7. Owner Route Matrix

| route | status | readout |
|---|---|---|
| universal homogeneous lapse | rejected_as_owner_alone | gauge unless coupling/calibration is specified |
| relative observer coframe clock map | live_theorem_target | cleanest physical route if derived |
| signed domain-boundary functional | live_but_unbuilt | needed because target changes sign |
| ad hoc redshift relabel | closure_only | BAO patch unless retested everywhere |
| Q^nu exchange fallback | deferred_high_risk | still not forced |

The surviving theorem target is:

```text
Theta_clock = B_mem C_clock[Q_coh, D],
```

where `C_clock` must be a signed observer/coframe/domain-boundary functional.

It must satisfy:

```text
B_mem -> 0 implies Theta_clock = zeta = 0;
stationary or virialized domains imply Theta_clock -> 0 locally;
the same map must be used for BAO, SN, H(z), CMB, and local clocks.
```

## 8. Gates

Machine gate result:

| gate | status | evidence |
|---|---|---|
| source_paths_exist | pass | all cited source artifacts exist |
| clock_target_quantified | pass | zeta translated into Theta_clock |
| locked_memory_shape_owner | fail | no single locked memory shape owns the target |
| smooth_closure_exists | pass_diagnostic_only | one regression closure matches all signs |
| observer_clock_parent_owner | fail_missing | no signed C_clock theorem yet |
| projection_route_status | retained_conditional | small target, not claimable |

So the scorecard is:

```text
projection route survives the round;
existing activation does not win the round;
parent clock theorem is now the mandatory next punch.
```

## 9. Decision

Current fair status:

```text
redshift_clock_map_target_quantified_not_parent_derived_projection_retained_conditional
```

Meaning:

```text
the BAO redshift/clock target is percent-level and smooth;
it is plausible enough to keep working on;
but current MTS machinery does not derive it;
there is no BAO bridge promotion;
there is no CMB support claim;
there is no local-GR promotion.
```

The important improvement is that the missing object is now exact:

```text
derive a signed observer/coframe/domain-boundary scalar C_clock[Q_coh,D]
that produces the required Theta_clock(z).
```

Fail condition:

```text
if C_clock can only be chosen after seeing the BAO rows,
the projection route becomes an explicit closure benchmark.
```

## 10. Next Target

Next checkpoint:

```text
156-clock-projection-functional-theorem-or-demotion.md
```

Task:

```text
construct the signed C_clock theorem from the observer coframe / coherent domain boundary,
or demote the projection route to closure-only and return to Q^nu / full Boltzmann inference.
```

This is the correct level of grim: not a knockout, not a collapse. We have found the exact opponent. Now the theory has to throw the punch itself.
