# 200 - BAO Strict-Alpha Shape Stress or Parent H0-r_d Contract

Private theory checkpoint. This is not a public BAO claim.

## 1. Trigger

Checkpoint 199 decided:

```text
BAO alpha is fair as a shared empirical nuisance,
but it is not parent-owned.
```

The next discipline step is:

```text
fix alpha from predeclared H0-r_d candidates and score the same BAO shape
against the same baselines.
```

This tests whether alpha is merely convenient or whether fixed parent-like
calibrations immediately wreck BAO.

## 2. Machine Artifact

Script:

```text
scripts/BAO_strict_alpha_shape_stress_or_parent_H0_rd_contract.py
```

Run:

```text
runs/20260601-000017-BAO-strict-alpha-shape-stress-or-parent-H0-rd-contract
```

Command:

```text
python scripts/BAO_strict_alpha_shape_stress_or_parent_H0_rd_contract.py --timestamp 20260601-000017 --max-iter 160
```

Status:

```text
BAO_strict_alpha_stress_run_parent_H0_rd_contract_still_missing
```

Claim ceiling:

```text
strict_alpha_BAO_stress_internal_only_no_parent_alpha_no_support_claim
```

## 3. Test Design

The run performed:

```text
2 releases x 5 fixed-alpha candidates x 6 model branches = 60 fits.
```

Releases:

```text
DESI_DR2_primary,
DESI_DR1_primary.
```

Model branches:

```text
LCDM,
wCDM,
CPL,
MTS_locked_2over27,
MTS_Bmem_zero,
MTS_fitted_Bmem_diagnostic.
```

Fixed-alpha candidates:

| candidate | alpha |
|---|---:|
| late-reference H0 with `rdrag` | `29.785829426978175` |
| same-density CMB-profile H0 with `rdrag` | `30.916005439216264` |
| half-memory H0 with `rdrag` | `30.909692098462312` |
| DR2 locked-fit alpha readback | `30.02925466330115` |
| DR1 locked-fit alpha readback | `29.937985423791293` |

Important:

```text
the same fixed alpha is applied to the baselines and MTS.
```

So this is not an MTS-only rescue test.

## 4. Locked Branch Scorecard

For `MTS_locked_2over27`:

| release | alpha candidate | locked chi2 | delta chi2 vs shared-alpha locked fit | verdict |
|---|---|---:|---:|---|
| DR1 | DR1 locked readback | `11.891978971059944` | `0.0000000000001563194` | survives |
| DR1 | DR2 locked readback | `11.954018603617627` | `0.0620396325578394` | survives |
| DR1 | late-reference H0 | `12.06745247080012` | `0.17547349974033288` | survives |
| DR1 | half-memory H0 | `18.49515525337799` | `6.603176282318204` | pressure |
| DR1 | CMB-profile H0 | `18.57823688124529` | `6.6862579101855015` | pressure |
| DR2 | DR2 locked readback | `8.162376305146172` | `0.0000000000001101341` | survives |
| DR2 | DR1 locked readback | `8.345904461475968` | `0.18352815632990627` | survives |
| DR2 | late-reference H0 | `9.4818649814852` | `1.3194886763391391` | soft warning |
| DR2 | half-memory H0 | `24.12651829368076` | `15.9641419885347` | pressure |
| DR2 | CMB-profile H0 | `24.349233835616754` | `16.186857530470693` | pressure |

Readout:

```text
BAO tolerates readback/late-ish alpha.
BAO strongly dislikes the CMB-profile or half-memory H0 alpha.
```

This is not necessarily bad for the endpoint theory. It says:

```text
BAO wants the late common-mode calibration, not the CMB endpoint-jump H0.
```

That is exactly the kind of domain split the endpoint rule was trying to make.

## 5. Against Baselines

The fixed-alpha locked branch remains competitive against the same-alpha
baselines in several cases.

Examples:

| release | alpha candidate | delta chi2 vs LCDM same alpha | delta chi2 vs wCDM same alpha | delta chi2 vs CPL same alpha |
|---|---|---:|---:|---:|
| DR2 | DR2 locked readback | `-7.47860164467048` | `-0.8807316791137474` | `-0.5688354453000919` |
| DR2 | DR1 locked readback | `-5.551178724830306` | `-0.7454934004650049` | `-0.5911645532923071` |
| DR2 | late-reference H0 | `-2.252285650365277` | `0.17292593525346334` | `0.1869772574670403` |
| DR1 | DR1 locked readback | `-2.8611954583165122` | `-0.9748660389236488` | `0.2201194459472955` |
| DR1 | late-reference H0 | `-1.7045505868281818` | `-0.692697868118545` | `0.18493336998036902` |

So the strict-alpha test does not reveal a simple MTS-specific collapse.

But:

```text
CMB-profile alpha and half-memory alpha create large strict-alpha pressure
relative to the shared-alpha locked branch.
```

## 6. Interpretation

This is the cleanest current BAO story:

```text
BAO is compatible with the endpoint-clock route only if BAO is a late
common-mode calibration channel.
```

That means:

```text
BAO should not use the same alpha as the CMB-profile/half-memory H0 branch.
```

This supports the domain-rule idea:

| observable class | calibration rule |
|---|---|
| CMB acoustic angle | sees early-to-late endpoint memory jump |
| BAO ratios | use late common-mode ruler calibration |
| local/SN ladder | common-mode late calibration if local silence holds |

But this remains conditional. The parent action has not derived the H0-r_d
assignment.

## 7. Parent Contract

To promote this from stress-test logic to theory:

| contract | status |
|---|---|
| fixed-alpha branch choice | missing |
| shared-alpha scorecard policy | implemented empirically |
| strict-alpha survival | tested here |
| no cherry-picked alpha | guardrail active |

The next parent question is:

```text
Can the theory derive why BAO uses the late common-mode alpha rather than the
CMB endpoint-jump alpha?
```

If yes, BAO becomes much cleaner.

If no, BAO remains empirical closure-only.

## 8. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| fixed-alpha candidates scored against same baselines | pass |
| at least one strict-alpha branch survives diagnostic | pass |
| strict-alpha pressure recorded | warning |
| parent H0-r_d alpha derived | fail |
| BAO support claim allowed | fail |

## 9. Decision

Decision:

```text
BAO_strict_alpha_stress_run_parent_H0_rd_contract_still_missing
```

Meaning:

```text
Fixed-alpha BAO shape stress has been run fairly. Readback/late-ish alpha
branches survive or soften only mildly, while CMB-profile/half-memory alpha
branches are pressured. This is consistent with a late common-mode BAO domain,
but the parent H0-r_d assignment is still missing.
```

Current theory status:

```text
BAO remains empirically usable;
BAO should not be claimed as parent-predicted;
the next job is to decide whether the endpoint theory can derive the late
common-mode H0-r_d owner.
```

Next target:

```text
201-BAO-strict-alpha-results-and-H0-rd-owner-decision.md
```
