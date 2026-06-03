# 212 - Composite GK Local BAO Galaxy Safety Gate

Private theory checkpoint. This is not a public local-GR, SPARC/galaxy, BAO,
CMB, or field-theory completion claim.

## 1. Trigger

Checkpoint 211 left the fixed closure:

```text
L_cg^-2 = L_H^-2 + G_K^2
```

with:

```text
alpha_K = 1
M_AB = fixed diagonal closure
```

The next question is not whether this is derived. It is not.

The next question is whether this fixed closure is immediately killed when we
ask it to face three arenas at once:

```text
local suppression,
BAO smoothness,
galaxy viability.
```

## 2. Machine Artifact

Script:

```text
scripts/composite_GK_local_BAO_galaxy_safety_gate.py
```

Run:

```text
runs/20260601-000029-composite-GK-local-BAO-galaxy-safety-gate
```

Command:

```text
python scripts/composite_GK_local_BAO_galaxy_safety_gate.py --timestamp 20260601-000029
```

Status:

```text
composite_GK_gradient_proxies_survive_local_BAO_galaxy_domain_owner_missing
```

Claim ceiling:

```text
composite_GK_proxy_safety_no_local_GR_galaxy_or_BAO_promotion
```

## 3. Shared Rule Tested

The same fixed closure was used in every arena:

```text
L_cg = [L_H^-2 + G_K^2]^-1/2.
```

Worst-case linear memory-gradient proxy:

```text
Delta C ~= B_mem L_test / L_cg.
```

with:

```text
B_mem = 2/27.
```

This is deliberately conservative. It is a proxy gate, not a field equation or
full observable likelihood.

## 4. BAO Threshold

From checkpoint 205, the `150 Mpc` BAO shape bound is:

```text
Delta C < 0.005539695284669133.
```

For a full linear `B_mem` spread over `L_cg`, this requires:

```text
L_cg > 2005.7260445101792 Mpc
```

or:

```text
G_K < 0.00044481968851035176 Mpc^-1.
```

That is a very useful hard number.

It means:

```text
smooth BAO domains must be genuinely smooth.
```

Gpc/BAO-scale transition domains are correctly rejected as smooth BAO
common-mode branches.

## 5. Arena Readout

Key proxy outcomes:

| branch | proxy result |
|---|---|
| exact FLRW | safe Hubble-cap branch |
| smooth BAO late domain | passes BAO gradient proxy |
| Gpc transition domain | fails as smooth BAO |
| BAO-scale transition | fails hard as smooth BAO |
| solar-system Weyl branch | passes local gradient proxy |
| Earth-surface Weyl branch | passes local gradient proxy |
| Milky-Way-like Weyl proxy | not killed by internal gradient proxy |

The good news:

```text
there is no immediate gradient contradiction between local, BAO, and galaxy
proxy use of the fixed formula.
```

The warning:

```text
this only works if G_K is a domain functional.
```

If local or galaxy curvature is forced into the smooth BAO domain, BAO fails by
enormous factors.

## 6. Galaxy Proxy

Representative Weyl-only galaxy proxies were tested.

The internal radius-gradient proxy passes for:

```text
dwarf_3kpc,
milky_way_8kpc,
outer_spiral_30kpc,
massive_ETG_5kpc,
cluster_1Mpc.
```

This does not prove the galaxy branch.

It only says:

```text
the fixed composite G_K closure is not immediately killed by internal
galaxy-scale smoothness.
```

The real galaxy question remains:

```text
does this closure preserve the actual rotation/acceleration phenomenology when
connected to the galaxy pipeline?
```

That has not been run here.

## 7. Domain Separation Is Mandatory

The gate found a sharp structural condition:

```text
BAO smooth branch:
G_K < 4.4481968851035176e-4 Mpc^-1.
```

But local and galaxy Weyl estimates are much larger.

Therefore:

```text
local, galaxy, and BAO cannot all be the same representative domain.
```

That is not a contradiction if the parent theory derives domain selection.

It is a problem if domain choice remains manual.

So the live blocker is now:

```text
derive the domain selector, or freeze it honestly as closure.
```

## 8. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| smooth BAO gradient proxy | pass |
| transition BAO rejection | pass |
| local Weyl gradient proxy | pass |
| galaxy internal gradient proxy | conditional pass |
| single formula across arenas | conditional pass |
| parent domain selector derived | fail |
| local-GR / galaxy empirical promotion | fail |

## 9. Decision

Decision:

```text
composite_GK_gradient_proxies_survive_local_BAO_galaxy_domain_owner_missing
```

Meaning:

```text
the fixed composite G_K closure survives the first three-arena gradient
sanity gate, but only as closure.
```

No promotion is allowed because:

```text
q_loc / PPN residuals are not derived,
SPARC/ETG observables are not tested,
and the domain selector is still not parent-owned.
```

## 10. Next Target

Next target:

```text
213-fixed-GK-domain-selector-contract.md
```

The exact next question:

```text
Can the domain selector be stated as a zero-knob contract that separates
local, galaxy, and BAO representatives before any empirical scoring?
```
