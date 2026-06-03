# 232 - Parent Pmem Projector or Source Identity Variation

Private local-derivation checkpoint. This is not a public local-GR, PPN,
clock, WEP, or field-theory completion claim.

## 1. Trigger

Checkpoint 231 gave a real topological lever:

```text
after projecting away mass flux and tangential shear,
relative H^2 on the compact shell vanishes,
so closed memory flux is exact.
```

But the open row was obvious:

```text
who owns P_mem?
```

This checkpoint tries to make `P_mem` less like a post-hoc filter.

## 2. Machine Artifact

Script:

```text
scripts/parent_Pmem_projector_or_source_identity_variation.py
```

Run:

```text
runs/20260601-000049-parent-Pmem-projector-or-source-identity-variation
```

Command:

```text
python scripts/parent_Pmem_projector_or_source_identity_variation.py --timestamp 20260601-000049
```

Status:

```text
Pmem_charge_projector_candidate_and_projected_source_identity_template_parent_symplectic_owner_open_no_promotion
```

Claim ceiling:

```text
Pmem_projector_candidate_no_parent_symplectic_or_local_GR_promotion
```

## 3. Minimal Non-Cheating Projector

The projector cannot be:

```text
delete whatever breaks PPN.
```

It must preserve the real exterior mass charge and only act on the memory
exchange sector.

The minimal candidate is:

```text
P_mem = 1 - Pi_M - Pi_TF - Pi_matter.
```

where:

| piece | role |
|---|---|
| `Pi_M` | extracts absolute `S^2` harmonic flux and stores it as `M_eff` |
| `Pi_TF` | extracts trace-free/tangential shell shear |
| `Pi_matter` | forbids direct matter/clock coupling |
| `P_mem` | leaves only relative memory exchange current |

So:

```text
mass charge -> M_eff,
shear -> not local memory,
matter/clock coupling -> forbidden,
relative memory -> J_rel.
```

That is the non-cheating split.

It respects the checkpoint-231 topology:

```text
absolute H^2 is not erased;
relative H^2 does the exactness work.
```

## 4. Projected Source Identity Template

The source-identity template becomes:

```text
S_X =
- int sqrt(-g) X_nu [
  nabla_mu P[Y]^{mu nu}
  - S_L^nu
  - d_rel(P_mem J_rel)^nu
]
+ boundary.
```

Varying `X_nu` gives:

```text
nabla_mu P[Y]^{mu nu}
= S_L^nu + d_rel(P_mem J_rel)^nu.
```

With:

```text
P^{mu nu}=Khat^{mu nu}-Gamma_eff g^{mu nu},
```

this gives:

```text
nabla_mu Khat^{mu nu} - nabla^nu Gamma_eff
= S_L^nu + d_rel(P_mem J_rel)^nu.
```

Then in compact exterior vacuum:

```text
S_L^nu = 0,
P_mem J_rel = d_rel A_rel,
d_rel(P_mem J_rel)=0,
q_loc^nu = 0.
```

This is a coherent chain.

It is still a template.

## 5. What Improved

Before this checkpoint:

```text
P_mem was a required projector.
```

After this checkpoint:

```text
P_mem is the unique minimal charge/shear/matter decomposition candidate:
P_mem = 1 - Pi_M - Pi_TF - Pi_matter.
```

That is better because it prevents the dirty move:

```text
erase mass flux and call it memory silence.
```

Instead:

```text
mass survives as M_eff;
only relative memory enters the exact cohomology channel.
```

## 6. What Still Fails

The projector is not yet parent-derived.

Still missing:

```text
the parent boundary symplectic metric,
the parent constraint that defines Pi_M,
the parent scalar-boundary theorem that fully defines Pi_TF,
the matter action that defines Pi_matter,
the X no-hair constraint algebra,
the local Einstein-Hilbert exterior operator.
```

So this checkpoint does not promote:

```text
q_loc = 0,
beta = 1,
local GR,
PPN safety.
```

It promotes only the quality of the target.

## 7. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| `P_mem` minimal decomposition candidate written | pass |
| mass class preserved rather than erased | pass |
| projected source-identity template written | pass |
| beta route strengthened | pass |
| parent boundary symplectic projector derived | fail |
| source identity parent-derived | fail |
| local GR or PPN promoted | fail |

The win is real.

The belt still stays on the table.

## 8. Decision

Decision:

```text
Pmem_charge_projector_candidate_and_projected_source_identity_template_parent_symplectic_owner_open_no_promotion
```

Meaning:

```text
a minimal non-cheating P_mem candidate now exists: keep the absolute S^2
harmonic flux as M_eff, remove trace-free/tangential shear, forbid direct
matter/clock coupling, and send only the remaining relative memory current into
the exact cohomology channel.
```

Main gain:

```text
P_mem is now a named charge/shear decomposition candidate rather than an
arbitrary eraser.
```

Main failure:

```text
parent symplectic ownership of the projector and source identity is still
missing.
```

## 9. Next Target

Create:

```text
233-boundary-symplectic-metric-or-local-EH-operator.md
```

Purpose:

```text
derive the boundary symplectic/inner-product structure that makes
Pi_M, Pi_TF, Pi_matter, and P_mem canonical,
or pivot to deriving the local Einstein-Hilbert exterior operator.
```

Pass condition:

```text
P_mem is an orthogonal complement under a parent-derived boundary metric.
```

or:

```text
the exterior metric equation reduces to G_mu_nu = 0.
```

Fail condition:

```text
P_mem remains a convenient projection with no parent owner.
```
