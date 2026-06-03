# Isolated Growth/CMB First Score Runner

## 1. Purpose

This file follows:

```text
27-strict-cosmology-numeric-lock.md
```

The question is:

```text
What happens when the locked no-SH0ES background values are pushed through the
first growth/CMB holdout score, using an isolated post-checkpoint runner?
```

Short answer:

```text
the runner works, but the strict C0/MTS branch is not preferred in this first
internal growth/CMB score. The damage comes from the compressed CMB-distance
piece, not the growth rows.
```

## 2. Machine Run

Implemented:

```text
scripts/isolated_growth_CMB_first_score_runner.py
```

Python environment:

```text
.venv-score
```

Successful run:

```text
runs/20260531-001059-isolated-growth-CMB-first-score-runner/status.json
```

Readout:

```text
isolated_C0_not_preferred_first_growth_CMB_score
```

## 3. Main Result

Best models:

```text
best chi2: wCDM
best AIC: wCDM
best BIC: wCDM
```

C0/MTS deltas versus the best baseline:

```text
Delta chi2 = 3387.9395823425457
Delta AIC = 3387.9395823425457
Delta BIC = 3387.9395823425457
```

This is not a close miss.

## 4. Dataset Split

Growth side:

```text
LCDM chi2_growth_primary = 15.682412358967213
wCDM chi2_growth_primary = 14.463332089064483
CPL chi2_growth_primary = 17.110842020618023
C0 chi2_growth_primary = 14.930776159766813
```

So growth alone is not the disaster.

CMB-distance side:

```text
LCDM chi2_CMB_distance = 4407.998873355444
wCDM chi2_CMB_distance = 4353.692891884779
CPL chi2_CMB_distance = 7696.884217330755
C0 chi2_CMB_distance = 7741.165030156622
```

The compressed CMB-distance approximation is dominating the verdict.

## 5. Interpretation Lock

Allowed language:

```text
the isolated runner executed;
the first internal score disfavors this locked C0/MTS branch;
growth rows are roughly competitive;
compressed CMB-distance treatment must be audited before any big conclusion.
```

Forbidden language:

```text
MTS is dead;
MTS is supported;
this proves/disproves the parent theory;
this is a public cosmology result.
```

## 6. Next Target

Create:

```text
29-growth-CMB-score-readout-and-robustness-gate.md
```

Purpose:

```text
separate real C0/MTS tension from possible CMB-distance-prior approximation or
pipeline issues, and decide whether to repair, rerun, or demote this branch.
```
