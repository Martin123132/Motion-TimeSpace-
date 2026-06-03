# 213 - Fixed GK Domain Selector Contract

Private theory checkpoint. This is not a public local-GR, galaxy, BAO, CMB, or
field-theory completion claim.

## 1. Trigger

Checkpoint 212 found that the fixed composite `G_K` closure survives first-pass
gradient proxies across:

```text
local,
BAO,
galaxy.
```

But that survival only makes sense if the theory has a lawful domain selector.

The next question is:

```text
Can the selector be stated without using arena labels by hand?
```

## 2. Machine Artifact

Script:

```text
scripts/fixed_GK_domain_selector_contract.py
```

Run:

```text
runs/20260601-000030-fixed-GK-domain-selector-contract
```

Command:

```text
python scripts/fixed_GK_domain_selector_contract.py --timestamp 20260601-000030
```

Status:

```text
domain_selector_contract_written_x_gate_insufficient_extended_load_invariant_missing
```

Claim ceiling:

```text
domain_selector_contract_no_parent_selection_or_galaxy_promotion
```

## 3. Useful Dimensionless Gates

Define:

```text
x = R_D / L_cg.
```

The local gradient proxy gives:

```text
x_local = 4.6e-5 / (2/27)
        = 0.000621.
```

The BAO shape proxy gives:

```text
x_BAO = 0.005539695284669133 / (2/27)
      = 0.07478588634303329.
```

These are useful because they are inherited from previous gates, not freshly
chosen thresholds.

## 4. Selector Contract

A zero-knob selector would need four branches:

| branch | required non-fit inputs |
|---|---|
| smooth fossil ruler | high `C_coh`, fossil-ruler matter labels, `x_150 < x_BAO`, low boundary current |
| local PPN shell | compact-source/vacuum-shell morphology, `x_local < 0.000621`, `q_loc` projected out |
| extended galaxy load | bound extended-load morphology, nontrivial routing/load support, internal `x < x_BAO` |
| transition/wall | failed smoothness, high boundary current, or large shear/transition signal |

This is a contract, not a derivation.

## 5. Stress Test Result

The simple `x` gates are not enough.

They correctly help with:

```text
BAO smooth versus transition,
solar/Earth local shells.
```

But they can misread low-`x` extended loads.

The key failure is:

```text
dwarf_3kpc
```

because a low-radius-over-coherence value can look local by `x` alone, even
though it should be treated as an extended galaxy/load domain.

That means the selector needs another invariant.

## 6. Missing Invariant

The missing object is:

```text
compact-source / vacuum-shell
versus
extended-load / disk-support
```

In MTS language, the natural owners are:

```text
Q
J_rel
matter-support topology
load anisotropy.
```

Without one of those, the theory would be choosing:

```text
local,
galaxy,
BAO
```

by hand.

That is not acceptable for promotion.

## 7. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| dimensionless `x` gates derived from existing bounds | pass |
| `x`-only selector sufficient | fail |
| morphology-augmented contract classifies stress cases | conditional pass |
| compact-vs-extended morphology invariant derived | fail |
| domain selector ready for empirical scoring | fail |

## 8. Decision

Decision:

```text
domain_selector_contract_written_x_gate_insufficient_extended_load_invariant_missing
```

Meaning:

```text
the domain-selector contract is now explicit and testable, but a simple
coherence-length rule is not enough.
```

The next theorem target is:

```text
derive a compact-vs-extended load invariant.
```

## 9. Next Target

Next target:

```text
214-compact-vs-extended-load-invariant-attempt.md
```

The exact question:

```text
Can Q, J_rel, or matter-support topology distinguish local compact PPN shells
from extended galaxy load domains without using hand labels?
```
