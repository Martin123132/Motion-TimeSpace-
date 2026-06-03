# 300 - Boundary-State Local Silence Theorem Attempt

Private derivation checkpoint. This is not a public local-GR, PPN, cosmology, CMB, or parent-field-theory claim.

## Purpose

Checkpoint 299 said the next honest theory target was:

```text
derive the boundary-state theorem:
local bound domains have rho_D=0 and/or [J_B]=0,
FLRW domains have rho_D>0 and nontrivial [J_B].
```

This checkpoint attempts that theorem.

Short answer:

```text
the theorem is not derived.
```

But:

```text
the exact boundary-state criterion is now much sharper.
```

## IR Boundary-Bath Selector

Define an MTS boundary-bath spectral strength:

```text
b_D = lim_{omega -> 0+} rho_D(omega)/omega.
```

Define the relative boundary-current class norm:

```text
c_D = ||[J_B]_D||.
```

The best selector target is:

```text
sigma_D = Theta(b_D) Theta(c_D).
```

or, for future numerical stress tests:

```text
sigma_D = b_D c_D / (b_D c_D + mu_*^2).
```

The local silence target is:

```text
b_D=0 and/or c_D=0
=> sigma_D=0.
```

The FLRW activity target is:

```text
b_D>0 and c_D>0
=> sigma_D nonzero.
```

This is the cleanest selector so far because it is:

```text
boundary-state based,
relative-class based,
not a naive curvature threshold.
```

## Conditional Theorem

The conditional theorem is:

```text
If a local bound domain is closed/gapped in the MTS boundary-bath channel
and has trivial relative boundary-current class,
then the open sector is exactly silent locally.
```

Why:

```text
b_D=0 and/or c_D=0
=> sigma_D=0
=> Gamma_D=N_D=Lambda_D=0
=> epsilon_loc=0.
```

So:

```text
local PPN residual from this open sector is zero at the effective level.
```

This is good.

It is still conditional.

## FLRW Activity Condition

The FLRW branch survives if the coherent cosmological domain has:

```text
b_D>0,
c_D>0.
```

That means:

```text
an open/gapless boundary bath
plus a nontrivial relative memory class.
```

Then:

```text
sigma_D nonzero,
```

and the open sector can remain active cosmologically.

This is the desired separation:

```text
local bound systems silent,
FLRW coherent domain active.
```

But the parent theory has not proved the split.

## Edge Cases

This theorem target has important traps:

| Edge case | Risk | Status |
|---|---|---|
| ordinary environmental dissipation | nonzero ordinary bath may mimic `rho_D` | must define MTS bath channel |
| black holes / local horizons | local horizon bath may be nonzero | separate branch needed |
| galaxies / clusters | bound but not laboratory-local | do not erase galaxy phenomenology |
| time-dependent local systems | low-frequency radiation may exist | local-bound runner needed |

The selector must not mean:

```text
any bath activates MTS.
```

It must mean:

```text
the specific MTS boundary bath channel activates MTS.
```

That distinction is mandatory.

## What Failed

The parent stack still does not prove:

```text
local bound domains are closed/gapped in the MTS bath channel,
[J_B]_local=0,
FLRW coherent domains are open/gapless,
[J_B]_FLRW is nontrivial.
```

Therefore:

```text
sigma_D remains a selector contract.
```

And:

```text
local GR is not promoted.
```

## Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | attempt traceable |
| IR bath selector defined | pass | theorem target precise |
| local closed/gapped implies silence | conditional pass | exact sufficient condition |
| FLRW open/nontrivial implies active | conditional pass | cosmology not automatically killed |
| boundary state parent-derived | fail | no local/FLRW split theorem |
| edge cases closed | fail | ordinary baths/horizons/galaxies remain |
| PPN bound verified | fail | no `epsilon_loc` run |
| `B_mem` parent-derived | fail | amplitude still closure |

## Decision

Decision:

```text
boundary_state_theorem_not_derived_IR_bath_separation_contract_written
```

Meaning:

```text
the boundary-state theorem is now precise,
but not parent-derived.
```

What improved:

```text
the selector is no longer just sigma_D by fiat.
```

It is:

```text
sigma_D = function(IR MTS bath strength, relative boundary-current class).
```

What did not improve:

```text
the parent theory has not proved the local/FLRW boundary-state split.
```

So:

```text
local GR remains unpromoted,
and 2/27 remains a locked closure/theorem target.
```

Boxing-score version:

```text
We found the rule the referee would need:
only the MTS boundary bath plus nontrivial relative class activates the punch.
But the referee has not yet agreed this is the official rulebook.
Good law shape. Not law yet.
```

## Machine Artifacts

Script:

```text
scripts/boundary_state_local_silence_theorem_attempt.py
```

Run:

```text
runs/20260601-000123-boundary-state-local-silence-theorem-attempt
```

Output files:

```text
runs/20260601-000123-boundary-state-local-silence-theorem-attempt/results/source_register.csv
runs/20260601-000123-boundary-state-local-silence-theorem-attempt/results/spectral_selector.csv
runs/20260601-000123-boundary-state-local-silence-theorem-attempt/results/domain_class_tests.csv
runs/20260601-000123-boundary-state-local-silence-theorem-attempt/results/theorem_attempts.csv
runs/20260601-000123-boundary-state-local-silence-theorem-attempt/results/edge_cases.csv
runs/20260601-000123-boundary-state-local-silence-theorem-attempt/results/promotion_gates.csv
runs/20260601-000123-boundary-state-local-silence-theorem-attempt/results/next_targets.csv
runs/20260601-000123-boundary-state-local-silence-theorem-attempt/results/decision.csv
```

## Next Step

Because the boundary-state theorem stayed conditional, the next honest move is:

```text
build the local-bound runner for epsilon_loc.
```

It should test:

```text
epsilon_loc = |sigma_D Lambda_open Tr(P_iso q_r)|
```

and report whether:

```text
sigma_D=0 exactly
```

or whether the residual must be bounded against PPN-style constraints.
