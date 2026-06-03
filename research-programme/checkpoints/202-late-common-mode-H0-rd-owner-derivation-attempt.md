# 202 - Late Common-Mode H0-r_d Owner Derivation Attempt

Private theory checkpoint. This is not a public BAO claim.

## 1. Trigger

Checkpoint 201 selected:

```text
late common-mode H0-r_d alpha
```

as the BAO theorem target, and demoted:

```text
CMB-profile / half-memory endpoint-jump alpha
```

for BAO.

This checkpoint asks whether that selection has a real derivation route.

## 2. Machine Artifact

Script:

```text
scripts/late_common_mode_H0_rd_owner_derivation_attempt.py
```

Run:

```text
runs/20260601-000019-late-common-mode-H0-rd-owner-derivation-attempt
```

Command:

```text
python scripts/late_common_mode_H0_rd_owner_derivation_attempt.py --timestamp 20260601-000019
```

Status:

```text
late_common_mode_BAO_owner_partially_derived_ruler_transport_parent_missing
```

Claim ceiling:

```text
BAO_late_common_mode_derivation_internal_only_transport_parent_missing
```

## 3. Core Distinction

The useful distinction is:

```text
CMB is a photon endpoint problem.
BAO is a late matter-ruler readout problem.
```

For CMB, the observer compares an early acoustic pattern to a late observer:

```text
Delta C_CMB ~= C_obs - C_emit ~= B_mem.
```

For BAO, the drag scale is generated early, but the observed object is not a
photon arriving from the drag epoch. The observed object is:

```text
a late galaxy/matter correlation separation carrying a fossil comoving ruler.
```

So the BAO ruler is read out in the late survey frame.

## 4. Partial Derivation

The chain is:

| step | result | status |
|---:|---|---|
| 1 | `r_d = integral c_s/H dz` defines the early acoustic scale | standard background ruler |
| 2 | after drag, the BAO scale is transported as a comoving matter-correlation imprint | physical observer-map argument |
| 3 | late BAO survey reads both `D_X` and the ruler in late matter units | conditional conformal-unit algebra |
| 4 | `tilde_D_X / tilde_r_d = D_X / r_d` | conditional ratio theorem |
| 5 | CMB differs because it has an early-to-late endpoint contrast | domain distinction |
| 6 | parent theory must derive comoving ruler transport | missing |

The key formula remains:

```text
tilde_D_X = exp(C_obs/2) D_X,
tilde_r_d^late = exp(C_obs/2) r_d,
tilde_D_X / tilde_r_d^late = D_X/r_d.
```

This is why BAO wants late common-mode alpha.

## 5. What Is Actually Derived

Derived or partially derived:

| theorem piece | status |
|---|---|
| BAO is not a direct early photon endpoint | partial pass |
| late conformal unit cancels in `D_X/r_d` | partial pass |
| CMB endpoint alpha is demoted for BAO | pass as domain gate |
| late `H0-r_d` alpha is selected | theorem target |

Still open:

```text
local silence consistency.
parent fossil-ruler transport.
release-independent alpha prediction.
```

## 6. Parent Transport Contract

To promote this, the parent framework must derive:

| contract | mathematical form | why it matters |
|---|---|---|
| fossil ruler transport | `D_t r_d^comoving = 0` after drag | prevents BAO ruler from inheriting the wrong endpoint memory |
| late matter-unit projection | `tilde_r_d^late = exp(C_obs/2) r_d` | makes common-mode cancellation real |
| radial drift silence | `dot_C/H` below BAO tolerance | protects `D_H/r_d` |
| domain selector | classify photon endpoints vs late matter-ruler readouts | prevents post-hoc branch switching |
| release-independent alpha | `alpha_BAO = c/(H0_late r_d^late)` | turns alpha from nuisance to prediction |

This is the next real theorem burden.

## 7. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| BAO late-readout distinction written | pass |
| CMB endpoint branch separated from BAO | pass |
| parent fossil-ruler transport derived | fail |
| release-independent alpha prediction derived | fail |
| BAO support claim allowed | fail |

## 8. Decision

Decision:

```text
late_common_mode_BAO_owner_partially_derived_ruler_transport_parent_missing
```

Meaning:

```text
The BAO late common-mode H0-r_d owner has a plausible derivation route:
BAO is a late matter-correlation readout of a fossil comoving ruler, so the
conformal late matter unit cancels in D_X/r_d.
```

But:

```text
the parent transport equation and release-independent alpha prediction remain
missing.
```

Current theory status:

```text
BAO is not dead;
BAO is not promoted;
the next target is the fossil-ruler transport equation.
```

Next target:

```text
203-fossil-ruler-transport-equation-attempt.md
```
