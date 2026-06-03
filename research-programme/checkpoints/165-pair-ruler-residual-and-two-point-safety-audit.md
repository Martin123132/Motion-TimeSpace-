# 165 - Pair Ruler Residual And Two-Point Safety Audit

Private residual/safety checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 164 found:

```text
fixed pair-ruler MTS survives the smoke run;
it beats LCDM by BIC;
it remains a competitive draw against no-clock MTS;
but it does not beat no-clock MTS.
```

This checkpoint asks:

```text
where exactly does the pair-ruler branch lose the small amount of chi2,
and what safety tests are mandatory before this can ever become a bridge?
```

Short answer:

```text
the route stays live but not leading;
the pressure is low-z transverse and high-z radial;
growth/RSD, lensing, and CMB-ruler safety are now mandatory gates.
```

## 2. Machine Artifact

Script:

```text
scripts/pair_ruler_residual_and_two_point_safety_audit.py
```

Run:

```text
runs/20260531-235959-pair-ruler-residual-and-two-point-safety-audit
```

Generated:

```text
source_register.csv
chi2_pressure_summary.csv
bao_row_delta_vs_controls.csv
bao_observable_pressure_summary.csv
worst_row_pressure.csv
two_point_safety_test_matrix.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
pair_ruler_survives_but_residual_pressure_and_two_point_safety_open
```

Claim ceiling:

```text
pair_ruler_residual_safety_audit_no_bridge_promotion
```

## 3. Chi2 Pressure

Against LCDM:

```text
delta chi2_SN = -1.4786068795622214
delta chi2_BAO = -2.2733222645228803
delta chi2_total = -3.7519291440848974
delta BIC = -3.7519291440848974
```

So the pair-ruler branch genuinely improves the smoke score versus LCDM.

Against no-clock MTS `u3=1/4`:

```text
delta chi2_SN = +1.0071949298082927
delta chi2_BAO = +0.4948169792251207
delta chi2_total = +1.5020119090336266
delta BIC = +1.5020119090336266
```

So no-clock MTS remains the cleaner empirical control.

This is not grim. It is a draw with a useful diagnostic:

```text
the pair transport helps enough to beat LCDM,
but its fixed shape is not yet better than the simpler no-clock background.
```

## 4. Row Pressure

Worst rows versus no-clock MTS:

| rank | z | observable | delta contribution | diagnosis |
|---:|---:|---|---:|---|
| 1 | 0.51 | `DM_over_rs` | +0.8132064813511022 | low-z transverse overcorrection / shared-alpha tension |
| 2 | 2.33 | `DH_over_rs` | +0.38691329510643113 | high-z radial overcorrection |
| 3 | 1.321 | `DM_over_rs` | +0.011701713829466998 | small transverse pressure |

Rows helped versus no-clock:

```text
10 rows improved;
3 rows worsened.
```

Observable-level summary versus no-clock:

| observable | sum delta contribution | readout |
|---|---:|---|
| `DM_over_rs` | +0.46463893568136216 | net worse |
| `DH_over_rs` | +0.030318728627017455 | near-neutral/slightly worse |
| `DV_over_rs` | -0.00014068508325613244 | neutral/slightly better |

So the main issue is not broad collapse. It is:

```text
low-z transverse shape pressure,
plus one high-z radial pressure row.
```

## 5. Interpretation

The fixed pair-ruler law is doing real work:

```text
it improves 10/13 BAO residual rows versus no-clock.
```

But the rows it worsens matter enough that the total BAO chi2 still worsens:

```text
delta chi2_BAO vs no-clock = +0.4948169792251207.
```

This suggests one of three possibilities:

```text
1. the fixed trace/quadrupole source law is close but needs a parent-constrained row-shape correction;
2. the pair-ruler branch is a real subroute but not the leading empirical branch;
3. the branch is a closure unless growth/lensing/two-point safety gives independent support.
```

The forbidden move is:

```text
fit a projection amplitude just to fix these rows.
```

That would turn it back into a BAO repair patch.

## 6. Two-Point Safety Matrix

Mandatory next gates:

| test arena | status | next action |
|---|---|---|
| BAO row residuals | active next | row/split audit and possible source-law repair |
| growth/RSD | open mandatory | define fixed pair response for `fσ8`/RSD or prove suppression |
| lensing correlations | open mandatory | prove null response or derive a lensing response |
| CMB sound horizon | open mandatory | late-turn-on or Boltzmann-interface proof |
| local/PPN | conditional | connect compensated kernel to bound-domain `X_D=0` |
| SN/H(z) | warning, not failure | profile `Omega_m` or run fixed no-clock-`Omega_m` split |

The important discipline:

```text
two-point observables are not automatically null.
```

If the operator is a connected pair operator, growth/RSD/lensing may have opinions. We need to ask them rather than hide from them.

## 7. Gates

| gate | status | readout |
|---|---|---|
| survives LCDM | pass | delta BIC `-3.7519291440848974` |
| beats no-clock control | fail draw only | delta BIC `+1.5020119090336266` |
| row pressure identified | pass | worst row `z=0.51 DM_over_rs` |
| row balance | mixed | 10 improved, 3 worsened vs no-clock |
| two-point safety | fail open | growth/RSD, lensing, CMB safety untested |
| source-law repair | open | low-z transverse and high-z radial pressure need a derived repair if any |
| promotion | fail | no bridge/local-GR/CMB claim |

## 8. Decision

Current fair status:

```text
pair_ruler_survives_but_residual_pressure_and_two_point_safety_open
```

Meaning:

```text
the branch is alive;
it is not the leading empirical branch;
no-clock MTS remains cleaner;
pair-ruler needs either a parent-constrained row-shape repair or independent
two-point-observable support.
```

Boxing-card readout:

```text
Pair-ruler wins rounds against LCDM, but no-clock MTS edges it on cleaner scoring.
The judges are not throwing it out.
But if it wants the belt, it needs either a cleaner jab at low-z DM/high-z DH,
or it needs to show the same footwork in growth/lensing.
```

## 9. Next Target

Create:

```text
166-pair-ruler-row-repair-or-demotion-gate.md
```

Task:

```text
try a parent-constrained row-shape repair, or freeze pair-ruler as a non-leading
closure while prioritizing the no-clock branch and two-point safety tests.
```

Pass condition:

```text
any repair must be derived from the pair-kernel/source-law structure and must
not add a fitted projection amplitude.
```

Fail condition:

```text
the only repair is to tune the BAO projection after seeing row residuals.
```
