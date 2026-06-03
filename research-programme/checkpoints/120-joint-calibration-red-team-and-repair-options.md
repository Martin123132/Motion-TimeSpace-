# 120 - Joint Calibration Red-Team and Repair Options

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 119 found a mixed joint late+CMB result:

```text
3 of 4 broad-r_d gates were competitive draws;
1 of 4 was a hard loss by the predeclared sector-degradation gate.
```

The failing gate was:

```text
LCDM compressed prior table
strict_full4 CMB vector
late chi2 penalty = 6.515760594759968
hard cutoff = 6
```

This checkpoint red-teams that one failure.

## 2. Short Verdict

```text
red_team_status =
joint_calibration_red_team_mixed_result_confirmed_not_promoted
```

```text
theory_promotion_allowed =
false
```

Plain English:

```text
The mixed result is real enough to respect. It is not an optimizer wobble, not
an r_d-prior edge trick, and not a clean pass.
```

The failure is narrow:

```text
0.5157605947599677 chi2 beyond the predeclared hard cutoff.
```

But the cutoff was declared before the red-team pass, so we do not move it.

Boxing-score version:

```text
This is one of those rounds where you want to argue with the judge, but the
card was signed before the bell. We mark it mixed, not won.
```

## 3. Machine Artifact

Script:

```text
research-programme\scripts\joint_calibration_red_team.py
```

Run:

```text
research-programme\runs\20260531-165759-joint-calibration-red-team
```

Generated:

```text
source_register.csv
gate_failure_audit.csv
sector_penalty_decomposition.csv
rd_prior_sensitivity.csv
compressed_prior_sensitivity.csv
targeted_refit.csv
repair_options.csv
decision.csv
status.json
```

## 4. Gate Failure Audit

| Prior table | Score mode | Gate | Late penalty | Margin vs hard cutoff | CMB penalty | Failure driver |
|---|---|---|---:|---:|---:|---|
| `wCDM` | `strict_full4` | competitive draw | 5.555606933888157 | -0.4443930661118429 | 1.9961220167282194 | none |
| `wCDM` | `marginal_R_lA` | competitive draw | 2.4389036590080195 | -3.5610963409919805 | 2.5602094418485497 | none |
| `LCDM` | `strict_full4` | hard loss sector degradation | 6.515760594759968 | +0.5157605947599677 | 2.172789216061106 | late sector degradation |
| `LCDM` | `marginal_R_lA` | competitive draw | 2.8118540022107936 | -3.1881459977892064 | 2.890375607071273 | none |

Readout:

```text
only one gate fails;
the failure is narrow;
the failure is late-sector, not CMB-sector.
```

## 5. Sector Penalty Decomposition

The late penalty is:

```text
SN penalty + BAO penalty
```

against the T7 alpha-free late locked branch.

| Prior table | Score mode | SN penalty | BAO penalty | Late penalty | BAO fraction |
|---|---|---:|---:|---:|---:|
| `wCDM` | `strict_full4` | 1.4523634118606878 | 4.10324352202732 | 5.555606933888008 | 0.7385770035310484 |
| `wCDM` | `marginal_R_lA` | 0.7125431209999533 | 1.7263605380079454 | 2.4389036590078987 | 0.7078428586679792 |
| `LCDM` | `strict_full4` | 1.6746700647720445 | 4.84109052998793 | 6.515760594759975 | 0.7429816457469559 |
| `LCDM` | `marginal_R_lA` | 0.8035377528528898 | 2.0083162493577635 | 2.8118540022106533 | 0.7142320503763154 |

This is the key physical read:

```text
the red gate is mostly BAO absolute-calibration tension.
```

It is not mainly SN shape.

It is not mainly the CMB chi2 itself.

The joint map is paying a BAO cost when:

```text
alpha_BAO
```

is no longer free and must equal:

```text
c / (100 h r_d).
```

## 6. r_d Prior Sensitivity

The broad prior was:

```text
80 <= r_d <= 200 Mpc
```

The physical sensitivity prior was:

```text
130 <= r_d <= 160 Mpc
```

The two runs land on the same solution to numerical precision:

| Prior table | Score mode | Delta Omega_m | Delta h | Delta r_d | Delta chi2 |
|---|---|---:|---:|---:|---:|
| `wCDM` | `strict_full4` | -7.889740494260167e-08 | 5.56723466216269e-08 | -1.728434713754723e-05 | -8.208189683500677e-11 |
| `wCDM` | `marginal_R_lA` | 0 | 0 | 0 | 0 |
| `LCDM` | `strict_full4` | 0 | 0 | 0 | 0 |
| `LCDM` | `marginal_R_lA` | 1.8403937113165014e-07 | -1.365333632818988e-07 | 4.3513083767265925e-06 | 1.1555130186025053e-09 |

Readout:

```text
the mixed result is not caused by weird r_d freedom.
```

The joint solution wants:

```text
r_d about 146.5 Mpc,
```

which is physically normal.

## 7. Compressed-Prior Sensitivity

The strict full-four vector is more sensitive to compressed-prior table choice:

| Score mode | Delta Omega_m LCDM-wCDM | Delta h LCDM-wCDM | Delta r_d LCDM-wCDM | Delta chi2 LCDM-wCDM |
|---|---:|---:|---:|---:|
| `marginal_R_lA` | 0.0009448114501360294 | -0.0007729018420786771 | 0.06722679247710062 | 0.7031165092284937 |
| `strict_full4` | 0.001639381885898794 | -0.0011865568133350157 | 0.08791036455608037 | 1.1368208597825742 |

Readout:

```text
compressed-prior model dependence is a live suspect.
```

But it is not an excuse to promote the branch, because the LCDM strict full-four table was mandatory in the contract.

## 8. Targeted Refit

The failing branch was refit directly:

```text
rd_prior_mode = broad
prior_table = LCDM
score_mode = strict_full4
model = MTS_locked_2over27
max_iter = 160
```

Result:

```text
chi2_SN = 1458.7735004752776
chi2_BAO = 13.010665920280031
chi2_CMB = 2.1727892176246355
late penalty = 6.515760594759968
late margin = 0.5157605947599677
```

Readout:

```text
not a simple numerical optimizer wobble.
```

## 9. Repair Options

| Option | Status | Readout |
|---|---|---|
| numerical optimizer issue | not primary suspect | broad/physical runs match and targeted refit reproduces the failing branch |
| compressed-prior model dependence | live suspect | only LCDM strict full-four table triggers the hard sector gate |
| BAO absolute calibration tension | live suspect | late penalty is dominated by BAO degradation after alpha is tied to h and r_d |
| threshold too hard | do not move goalposts | hard cutoff was predeclared at 6 and failure is +0.516 beyond it |
| parent calibration relation | needed for promotion | must derive shared relation among h, r_d, BAO alpha, SN offset, and Omega_m0 |

## 10. Decision

Status:

```text
joint_calibration_red_team_mixed_result_confirmed_not_promoted
```

Allowed statement:

```text
The joint calibration bridge is close and physically sane, but one mandatory
strict compressed-prior gate still fails.
```

Allowed statement:

```text
The failure is mostly a BAO absolute-calibration penalty, not an r_d-edge trick
or a direct CMB chi2 catastrophe.
```

Forbidden statement:

```text
MTS passes joint cosmology.
```

Forbidden statement:

```text
The red gate can be ignored because it is only 0.516 chi2 over the cutoff.
```

Forbidden statement:

```text
The parent theory has derived the calibration bridge.
```

## 11. Strategic Meaning

The current empirical status is now sharper:

```text
SN+BAO locked amplitude: strong.
BAO-only locked amplitude: good.
CMB-only compressed distance: non-discriminating draw.
simple late-to-CMB Omega_m transfer: fail.
joint h-r_d calibration: mixed, close, not promoted.
```

The next thing worth trying is not another free fit.

The next thing worth trying is:

```text
derive or reject a shared calibration relation.
```

Specifically:

```text
alpha_BAO = c/(100 h r_d)
```

is where the bridge pays most of its penalty.

So the parent framework must say whether `h`, `r_d`, and the BAO ruler are:

```text
independent phenomenological calibration knobs,
or constrained by a deeper MTS normalization.
```

## 12. Next Target

Create:

```text
121-shared-calibration-relation-derivation-attempt.md
```

Purpose:

```text
attempt to derive the minimum shared calibration relation among h, r_d,
BAO alpha, SN offset, and Omega_m0 that could reduce the BAO-dominated joint
penalty without adding private rescue freedom.
```

If no relation can be derived, the honest label becomes:

```text
locked 2/27 late-time empirical closure with unresolved absolute-calibration
bridge to CMB/BAO.
```
