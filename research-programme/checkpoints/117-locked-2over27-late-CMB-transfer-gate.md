# 117 - Locked 2/27 Late-to-CMB Transfer Gate

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 116 showed:

```text
the locked B_mem=2/27 branch can fit compressed CMB distance priors if h and
Omega_m0 are both fitted inside the CMB-only score.
```

But that test was deliberately easy.

The harder question is:

```text
if the late-time SN+BAO locked branch fixes Omega_m0, can that same Omega_m0
transfer into CMB distance with only h profiled?
```

This checkpoint tests exactly that.

## 2. Short Verdict

```text
late_to_CMB_transfer_status =
locked_2over27_late_to_CMB_transfer_geometry_fail
```

```text
theory_promotion_allowed =
false
```

```text
absolute_calibration_claim_allowed =
false
```

Plain English:

```text
The CMB-only draw was too easy. Once the late-time locked-branch Omega_m0 is
held fixed, compressed CMB distance wants a different Omega_m0.
```

This is not a death blow to the whole programme, but it is a real tension for the current late-to-CMB transfer route.

Boxing-score version:

```text
MTS won the warm-up footwork round, then got caught when the judge forced the
late-time stance to be carried into the CMB round.
```

## 3. Machine Artifact

Script:

```text
research-programme\scripts\locked_2over27_late_CMB_transfer_gate.py
```

Dry-run:

```text
research-programme\runs\20260531-162120-locked-2over27-late-CMB-transfer-dryrun
```

Score run:

```text
research-programme\runs\20260531-162146-locked-2over27-late-CMB-transfer-score
```

Generated:

```text
source_register.csv
late_branch_register.csv
cmb_anchor_register.csv
transfer_profile.csv
transfer_residuals.csv
transfer_gates.csv
decision.csv
status.json
```

## 4. Test Definition

Input late-time branch:

```text
T7 locked B_mem=2/27 SN+BAO robustness matrix.
```

Primary branch:

```text
T1_primary_fullcov_DR2
```

Transfer rule:

```text
hold late-time Omega_m0 fixed;
hold B_mem=2/27 fixed;
hold p=3 and u3=1/4 fixed;
profile only h against compressed CMB distance priors.
```

This is stricter than checkpoint 116 because checkpoint 116 fitted both:

```text
Omega_m0 and h.
```

This checkpoint only profiles:

```text
h.
```

## 5. Primary Late Branch

The primary late-time locked branch has:

| Quantity | Value |
|---|---:|
| `Omega_m_late` | 0.3032827426766658 |
| `B_mem` | 0.07407407407407407 |
| `DeltaR` | 0.2222222222222222 |
| `chi2_SN+BAO` | 1465.2684058007976 |
| `SN rows` | 1624 |
| `BAO rows` | 13 |
| `SN covariance` | full |
| `BAO release` | DESI DR2 primary |

This is the branch that survived the late-time robustness matrix.

## 6. Primary Transfer Result

| Prior table | Score mode | Omega_m late | h profiled | chi2 transfer | Delta chi2 vs CMB-only | CMB-only Omega_m | CMB-only h | Gate |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `wCDM` | `strict_full4` | 0.3032827426766658 | 0.6842175693081872 | 28.710799378334283 | 28.710799376348643 | 0.3295740146787432 | 0.6671371381879377 | fail |
| `wCDM` | `marginal_R_lA` | 0.3032827426766658 | 0.6843110654108914 | 9.782419014701404 | 9.782419013379505 | 0.32957399350906025 | 0.6671371660320761 | fail |
| `LCDM` | `strict_full4` | 0.3032827426766658 | 0.6840855512410924 | 34.934556232153 | 34.93455623058947 | 0.331286732138333 | 0.6659279626767358 | fail |
| `LCDM` | `marginal_R_lA` | 0.3032827426766658 | 0.6841503327564037 | 11.275910367217772 | 11.275910365092967 | 0.3312867941619584 | 0.6659279085720234 | fail |

Readout:

```text
primary_pass_count = 0
primary_soft_count = 0
primary_fail_count = 4
```

The failure is not an h-edge artifact:

```text
h profiled around 0.684, well inside [0.45, 0.90].
```

The failure is an Omega_m transfer tension:

```text
late SN+BAO wants Omega_m0 about 0.303;
CMB-only compressed distance wants Omega_m0 about 0.330-0.331.
```

## 7. What Failed Physically

The locked 2/27 branch can fit:

```text
late SN+BAO shape
```

and it can fit:

```text
CMB compressed distance geometry
```

but not yet with the same Omega_m0 under this simple transfer rule.

That means the current bridge:

```text
late Omega_m0 -> CMB with only h adjusted
```

fails.

The live tension is:

```text
Delta Omega_m0 roughly -0.026 to -0.028
```

from late SN+BAO to CMB-only.

## 8. Why This Still Is Not a Full Death Blow

The late SN+BAO branch used:

```text
SN nuisance offset;
BAO alpha nuisance calibration.
```

That means the late branch did not truly lock:

```text
h
r_d
absolute SN calibration
```

So the current failure says:

```text
simple Omega_m transfer fails.
```

It does not yet say:

```text
no joint late+CMB calibration exists.
```

The next test must tie the nuisance structure together instead of letting each arena have separate calibration freedom.

## 9. Decision

Status:

```text
late_to_CMB_geometry_transfer_fails_current_locked_branch
```

Allowed statement:

```text
The locked 2/27 branch has a real late-to-CMB Omega_m transfer tension under
the simple h-profiled transfer gate.
```

Forbidden statement:

```text
MTS is ruled out by CMB.
```

Forbidden statement:

```text
MTS passes CMB.
```

Forbidden statement:

```text
The parent theory predicts the required late-to-CMB calibration map.
```

## 10. Strategic Meaning

This is useful, even though it is a red result.

The empirical picture is now sharper:

```text
SN+BAO locked amplitude: good.
BAO-only locked amplitude: good.
CMB-only compressed distance: calibration draw.
late SN+BAO Omega_m -> CMB transfer: fails.
```

That is not random noise.

It says the key missing object is not another free cosmology score. It is a real calibration/parameter-map bridge:

```text
How do h, r_d, SN offset, BAO alpha, Omega_m0, and B_mem belong to one parent
field-theory parameter set?
```

## 11. Next Target

Create:

```text
118-locked-2over27-joint-late-CMB-calibration-contract.md
```

Purpose:

```text
define a fair joint late+CMB calibration test that ties SN offset, BAO alpha,
h, r_d, Omega_m0, and B_mem together without giving MTS or LCDM private rescue
freedom.
```

If that contract cannot be made fair, the branch must be labelled:

```text
late-time empirical closure with unresolved CMB calibration transfer.
```
