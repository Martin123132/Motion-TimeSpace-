# Calibrated Background Backreaction Guardrail

## 1. Purpose

This file follows:

```text
38-calibrated-closure-holdout-contract.md
```

The question is:

```text
After freezing the native CMB-calibrated C0 row, does it catastrophically wreck
the no-SH0ES late-background SN/BAO fit?
```

Short answer:

```text
no. The frozen CMB-calibrated row worsens late-background chi2 versus the locked
C0 no-SH0ES row by only 2.985. This passes the backreaction guardrail, but it
is not evidence because the row was CMB-trained and the late-background data are
not a fresh independent holdout.
```

## 2. Machine Run

Implemented:

```text
scripts/calibrated_background_backreaction_guardrail.py
```

Successful run:

```text
runs/20260531-005921-calibrated-background-backreaction-guardrail/status.json
```

Readout:

```text
calibrated_background_backreaction_guardrail_passes_not_evidence
```

## 3. Scores

Locked C0 no-SH0ES fit:

```text
chi2_SN = 1456.0079547123808
chi2_BAO = 12.241947710238785
chi2_total = 1468.2499024226195
```

Frozen native CMB-calibrated C0 row:

```text
chi2_SN = 1456.1748357911465
chi2_BAO = 15.06012928034503
chi2_total = 1471.2349650714916
```

Deltas versus locked C0:

```text
delta chi2_SN = 0.16688107876575486
delta chi2_BAO = 2.818181570106246
delta chi2_total = 2.9850626488721446
```

So the CMB-calibrated row is not a late-background disaster.

## 4. Baseline Context

Best fixed baseline in this guardrail:

```text
CPL_fixed_fit chi2_total = 1467.733029423899
```

Frozen native CMB-calibrated row:

```text
delta chi2_total versus best fixed baseline = 3.501935647592518
```

This is near the fitted baseline pack, but cannot be used for model selection.

## 5. Gate Result

Passed:

```text
source 38 complete;
frozen native row evaluated;
total backreaction not catastrophic versus locked C0;
SN backreaction not catastrophic versus locked C0;
BAO backreaction not catastrophic versus locked C0.
```

Failed by design:

```text
model-selection claim;
support claim.
```

## 6. Decision

Allowed language:

```text
the frozen CMB-calibrated C0 closure row passes a late-background backreaction
guardrail: it fixes the compressed CMB-distance block, keeps growth close, and
does not catastrophically spoil no-SH0ES SN/BAO.
```

Forbidden language:

```text
the calibrated row is evidence;
the calibrated row beats CPL/LCDM/wCDM;
MTS is supported by CMB;
the parent map is derived.
```

## 7. Status Upgrade

Before this run:

```text
CMB-calibrated closure row retained only because growth stayed close.
```

After this run:

```text
CMB-calibrated closure row also passes late-background backreaction.
```

Still true:

```text
fresh independent holdout or official CMB likelihood is required before any
evidence language.
```

## 8. Next Target

Create:

```text
40-fresh-holdout-or-official-likelihood-roadmap.md
```

Purpose:

```text
choose the next genuinely stronger test: fresh growth/RSD data, official
CMB spectra/lensing with fixed parameters, or a parent calibration-map repair.
```
