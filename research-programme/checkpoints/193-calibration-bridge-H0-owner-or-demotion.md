# 193 - Calibration Bridge H0 Owner or Demotion

Private theory checkpoint. This is not a public CMB claim.

## 1. Trigger

Checkpoint 192 partially derived the sign and scale of the same-density CMB
H0 compensation from the FLRW distance response:

```text
MTS positive late memory term -> lower D_A(z*) -> lower H0 compensates theta*.
```

But it left a harder ownership problem:

```text
the late-reference H0 and the same-density CMB-profile H0 are not the same.
```

So this checkpoint asks:

```text
Can a parent calibration rule connect them, or must one branch be demoted?
```

## 2. Machine Artifact

Script:

```text
scripts/calibration_bridge_H0_owner_or_demotion.py
```

Run:

```text
runs/20260601-000010-calibration-bridge-H0-owner-or-demotion
```

Command:

```text
python scripts/calibration_bridge_H0_owner_or_demotion.py --timestamp 20260601-000010
```

Status:

```text
calibration_H0_half_memory_bridge_numeric_candidate_parent_owner_missing
```

Claim ceiling:

```text
H0_calibration_bridge_internal_candidate_only_no_parent_owner_no_CMB_claim
```

## 3. H0 Split

The current internal numbers are:

| object | value |
|---|---:|
| late-reference H0 | `68.42175693081872` |
| same-density CMB-profile H0 | `65.92050790786743` |
| ratio `H_CMB/H_late` | `0.9634436598072116` |
| split | `2.501249022951285 km/s/Mpc` |

Therefore:

```text
a single unmodified H0 owner is rejected for the current branch.
```

That does not kill the branch. It means the theory must derive a calibration
map or explicitly demote either the late reference or the same-density CMB
route.

## 4. Half-Memory Bridge

The locked memory amplitude is:

```text
B_mem = 2/27 = 0.07407407407407407.
```

The best bridge candidate is:

```text
H_CMB = H_late exp(-B_mem/2).
```

Numerically:

| candidate | predicted CMB H0 | error vs CMB profile | status |
|---|---:|---:|---|
| `H_CMB = H_late` | `68.42175693081872` | `2.501249022951285` | rejected |
| `H_CMB = H_late (1 - B_mem/2)` | `65.88761778523285` | `-0.03289012263458346` | linear sidecar |
| `H_CMB = H_late exp(-B_mem/2)` | `65.93397224868876` | `0.013464340821329301` | best candidate |
| `H_CMB = H_late/(1+B_mem/2)` | `65.97812275471804` | `0.05761484685061191` | weaker sidecar |
| `H_CMB = H_late (1 - B_mem)` | `63.35347863964696` | `-2.567029268220473` | rejected |
| `H_CMB = H_late exp(-B_mem)` | `63.536642312275106` | `-2.383865595592326` | rejected |

This is the first really clean calibration clue:

```text
the H0 split looks like a half-memory clock/rate renormalization.
```

But it is not parent-derived yet.

## 5. B_mem Ratio Readout

If the ratio is inverted as a half-memory exponential law:

```text
B_inferred = -2 ln(H_CMB/H_late).
```

Then:

| estimator | inferred B | locked B | delta |
|---|---:|---:|---:|
| exponential half-memory | `0.07448253469982279` | `0.07407407407407407` | `0.0004084606257487161` |
| linear half-memory | `0.07311268038557683` | `0.07407407407407407` | `-0.0009613936884972363` |

So the bridge does not merely fit an arbitrary number. It almost reads back
the existing locked `2/27` amplitude.

That is promising, but still closure-level:

```text
near equality is not derivation.
```

## 6. Parent Contract

To promote this bridge, a future parent action must supply all of the following:

| contract | required object | acceptance condition |
|---|---|---|
| clock map variable | scalar or functional `C` with saturated change `B_mem` | parent action yields `H_obs = H_parent exp(-C/2)` or equivalent |
| observer-map variation | matter clock/ruler response to memory normalization | factor `1/2` is derived, not chosen because it fits H0 |
| late/CMB domain rule | rule deciding why late and CMB-inferred H0 use different calibrations | same rule preserves SN/BAO/H(z) and CMB without branch switching |
| local silence | local clock map must not violate PPN/clock constraints | local fixed point suppresses the calibration locally |
| fixed amplitude owner | derivation of `B_mem=2/27` | bridge inherits `B_mem` from theory rather than empirical lock |

If these cannot be derived, the half-memory bridge remains a closure.

## 7. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| half-memory exponential bridge matches H0 split | pass |
| H0 ratio infers locked `B_mem` | pass |
| parent clock map derived | fail |
| single H0 owner allowed | fail |
| official likelihood | not run |
| support claim allowed | fail |

## 8. Decision

Decision:

```text
calibration_H0_half_memory_bridge_numeric_candidate_parent_owner_missing
```

Meaning:

```text
The late-reference and CMB-profile H0 values are numerically connected by a
half-memory factor, especially exp(-B_mem/2). This is a serious theorem target,
not a proof.
```

Current theory status:

```text
do not demote the same-density CMB branch yet;
do reject single-H0 ownership for the current branch;
promote the half-memory clock map to the next derivation target;
do not make a CMB support claim.
```

Next target:

```text
194-half-memory-clock-map-derivation-attempt.md
```
