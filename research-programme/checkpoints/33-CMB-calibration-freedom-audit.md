# CMB Calibration Freedom Audit

## 1. Purpose

This file follows:

```text
32-repaired-score-readout-and-decision.md
```

The question is:

```text
If baselines and C0/MTS receive fair CMB calibration freedom, does the repaired
CMB-distance verdict still uniquely kill the locked C0/MTS shape?
```

Short answer:

```text
no. Fixed-background CMB disfavors C0/MTS, but equal CMB calibration freedom
removes the apparent catastrophic CMB problem. This creates a secondary closure
branch, not evidence, because the parent early-time/CMB limit is not derived.
```

## 2. Machine Run

Implemented:

```text
scripts/CMB_calibration_freedom_audit.py
```

Successful run:

```text
runs/20260531-003140-CMB-calibration-freedom-audit/status.json
```

Readout:

```text
CMB_calibration_freedom_changes_C0_status_but_parent_limit_missing
```

## 3. Core Result

Fixed repaired C0/MTS CMB-distance score:

```text
chi2 = 295.0481129416254
```

Equal two-parameter CMB calibration:

```text
C0 equal h0/omega delta AIC = 0.000000005739688724304415
```

Native frozen-shape C0 calibration:

```text
C0 native calibrated delta AIC = 1.999999999305702
```

So the CMB-distance prior alone is not a decisive C0 killer once calibration is
treated symmetrically.

## 4. Interpretation Lock

Demoted:

```text
fixed no-SH0ES C0/MTS growth+CMB support branch.
```

Retained:

```text
CMB-calibrated C0/MTS as secondary closure-only diagnostic;
growth-only behavior as near-competitive subdiagnostic.
```

Still forbidden:

```text
C0 support claim;
C0 death claim;
public CMB claim;
shape-free CMB tuning as evidence.
```

## 5. What Is Missing

The missing piece is now sharper:

```text
derive why H0, omega_m0, and b_mem may be recalibrated for CMB without breaking
the SN/BAO/growth branch, or demote CMB-calibrated success to phenomenology.
```

Also still needed:

```text
official Planck/ACT likelihood upgrade before any public CMB claim.
```

## 6. Next Target

Create:

```text
34-CMB-compatible-MTS-limit-contract.md
```

Purpose:

```text
state the exact parent-action/early-time conditions required for calibrated
CMB success to become more than a fitted closure branch.
```
