# 208 - Domain Representative Selection Law

Private theory checkpoint. This is not a public BAO, local-GR, or CMB claim.

## 1. Trigger

Checkpoint 207 made the domain projector formally variational:

```text
C = C_D + C_perp,
integral_D sqrt(h) W_D C_perp = 0.
```

But it still did not select the physical representative:

```text
local bound domains -> trivial relative class,
FLRW domains -> nontrivial coherent class,
BAO domains -> late common-mode smooth class.
```

This checkpoint asks whether that representative choice can be turned into a
predeclared selection law rather than chosen because it helps the fit.

## 2. Machine Artifact

Script:

```text
scripts/domain_representative_selection_law.py
```

Run:

```text
runs/20260601-000025-domain-representative-selection-law
```

Command:

```text
python scripts/domain_representative_selection_law.py --timestamp 20260601-000025
```

Status:

```text
domain_representative_law_conditionally_selects_ideal_branches_parent_domain_scale_missing
```

Claim ceiling:

```text
representative_selection_law_internal_only_no_domain_or_local_GR_promotion
```

## 3. Candidate Law

The useful invariant remains:

```text
C_coh[D] =
<theta>_D^2 /
(<theta^2>_D + <sigma^2>_D + <omega^2>_D + eps_D).
```

Representative readout:

| branch | `C_coh` | readout |
|---|---:|---|
| stationary local bound bulk | `0.0` | trivial/local memory-off |
| quiet Minkowski limit | `0.0` | trivial/local memory-off |
| ideal FLRW | `1.0` | coherent memory-on |
| linear FLRW scalar perturbation | `0.9999019800039208` | coherent, first-order safe |
| BAO late smooth domain | `0.99930048965724` | late common-mode candidate |
| collapsed merger/wall | `0.016000000000000004` | boundary/transition, not promoted |

So the ideal local/FLRW split is no longer just verbal:

```text
C_coh -> 0 selects trivial local class,
C_coh -> 1 selects coherent FLRW class.
```

## 4. Perturbation Safety

Checkpoint 132 gave the important cancellation:

```text
delta C_coh^(1) = 0
```

around FLRW bulk perturbations.

That means the representative is stable at first order:

```text
linear scalar expansion perturbations do not immediately create an independent
memory clustering representative.
```

This is useful for growth/CMB discipline, but it is still conditional because
the full gauge-invariant stress variation is not complete.

## 5. BAO Domain Precommitment

The non-cheaty BAO move is:

```text
the projector domain is not 150 Mpc because BAO likes it.
```

Instead use the predeclared FLRW coherence scale from the `L_cg` rule:

```text
L_D = L_cg = [L_H^-2 + alpha_K G_K^2]^-1/2.
```

For homogeneous FLRW:

```text
G_K = 0,
L_D = L_H = c/H.
```

Numerically:

```text
L_D = 4440.715463763339 Mpc.
```

A `150 Mpc` BAO patch is then a subdomain:

```text
150 / L_D = 0.03377834072550116.
```

The smooth-memory check gives:

```text
0.5 B_mem (150 Mpc / L_D) = 0.001251049656500043,
```

which is below the checkpoint-205 `Delta chi2 < 1` BAO leakage tolerance.

The zero-mode dilution check gives:

```text
B_mem (150 Mpc / L_D)^3 = 2.8548360218040578e-06,
```

which is below both local and BAO `Delta C` gates.

This is the best current BAO representative route:

```text
BAO is tested inside a predeclared Hubble-cap smooth domain,
not used to choose the domain.
```

## 6. What Is Gained

| representative | result |
|---|---|
| local stationary/quiet | conditionally selects trivial class |
| FLRW coherent | conditionally selects nontrivial memory class |
| linear FLRW perturbations | first-order stable |
| BAO late common-mode | conditionally predeclared by Hubble-cap `L_cg` |
| transition boundary | still open |
| non-FLRW bound domain scale | still open |

This is movement: the domain representative is no longer arbitrary in the ideal
limits.

## 7. What Still Fails

The current law does not yet prove:

```text
L_cg
```

from a microscopic parent action.

It also does not derive:

```text
J_rel
```

as the physical transition-boundary representative.

And it does not complete:

```text
B_mem amplitude,
C transition law,
local GR / PPN derivation.
```

So the representative law is a conditional selection ledger, not a promoted
field-theory theorem.

## 8. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| ideal local representative selected | conditional pass |
| ideal FLRW representative selected | conditional pass |
| linear FLRW perturbation safe | conditional pass |
| BAO late-common-mode representative predeclared | conditional pass |
| domain scale parent-derived | fail |
| boundary/transition representative selected | fail |
| local GR or BAO support claim allowed | fail |

## 9. Decision

Decision:

```text
domain_representative_law_conditionally_selects_ideal_branches_parent_domain_scale_missing
```

Meaning:

```text
local/FLRW/BAO representatives are no longer free verbal choices; they now have
a conditional selection ledger.
```

Best live law:

```text
C_coh branch readout plus predeclared L_D = L_cg Hubble-cap in FLRW.
```

But:

```text
L_cg/domain scale, boundary representative, and transition law are not
parent-derived.
```

Current theory status:

```text
representative selection improved;
domain scale remains the next hard theorem burden;
no local-GR or BAO promotion yet.
```

Next target:

```text
209-Lcg-domain-scale-parent-derivation-or-demotion.md
```
