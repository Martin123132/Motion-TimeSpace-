# CMB-Compatible MTS Limit Contract

## 1. Purpose

This file follows:

```text
33-CMB-calibration-freedom-audit.md
```

The question is:

```text
What exactly must be derived before the CMB-calibrated branch can count as
physics rather than fitted closure?
```

Short answer:

```text
the calibrated branch is locked as closure-only. It cannot support MTS until
the parent theory derives the early-time memory limit, the calibration-variable
map, and the joint growth/CMB limit.
```

## 2. Machine Run

Implemented:

```text
scripts/CMB_compatible_MTS_limit_contract.py
```

Successful run:

```text
runs/20260531-003434-CMB-compatible-MTS-limit-contract/status.json
```

Readout:

```text
CMB_compatible_MTS_limit_contract_locked_parent_derivation_required
```

## 3. Branch Status

Fixed no-SH0ES C0 growth+CMB:

```text
demoted.
```

Equal two-parameter CMB calibration:

```text
non-discriminating compressed distance-prior stress test.
```

Native C0 CMB-calibrated frozen shape:

```text
secondary closure only.
```

Shape-free CMB-calibrated branch:

```text
stress only.
```

Official CMB likelihood:

```text
not implemented.
```

## 4. Required Conditions

The parent limit must specify:

```text
memory decoupling or absorption at z_star;
sound-horizon convention and early radiation content;
shift-parameter matter/H0 definition;
acoustic-scale consistency;
perturbation closure or perturbation derivation.
```

## 5. Derivation Obligations

Before CMB success can count, derive or bound:

```text
Omega_Gamma(z_star) treatment;
H0, Omega_m0, and b_mem parameter map;
joint growth/CMB limit with one parameter set;
official CMB likelihood upgrade path.
```

## 6. Claim Lock

Still blocked:

```text
C0 support claim;
C0 death claim;
public CMB claim.
```

Reason:

```text
calibration freedom changes the internal CMB-distance result, but the parent
early-time/calibration derivation is missing.
```

## 7. Next Target

Create:

```text
35-early-time-decoupling-or-calibration-derivation.md
```

Purpose:

```text
attempt the derivation: either show memory decouples/absorbs consistently at
recombination, or formally demote CMB-calibrated success to phenomenology.
```
