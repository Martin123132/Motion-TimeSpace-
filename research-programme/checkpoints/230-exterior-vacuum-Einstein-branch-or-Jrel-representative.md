# 230 - Exterior Vacuum-Einstein Branch or Jrel Representative

Private local-derivation checkpoint. This is not a public local-GR, PPN,
clock, WEP, or field-theory completion claim.

## 1. Trigger

Checkpoint 229 sharpened beta:

```text
beta = 1
```

is not obtained from no-slip alone.

It follows if the compact exterior branch is:

```text
q_loc = 0,
no exterior memory hair,
vacuum Einstein outside the shell.
```

This checkpoint tries to write that branch exactly enough that the remaining
blocker cannot hide.

## 2. Machine Artifact

Script:

```text
scripts/exterior_vacuum_Einstein_branch_or_Jrel_representative.py
```

Run:

```text
runs/20260601-000047-exterior-vacuum-Einstein-branch-or-Jrel-representative
```

Command:

```text
python scripts/exterior_vacuum_Einstein_branch_or_Jrel_representative.py --timestamp 20260601-000047
```

Status:

```text
exterior_vacuum_Einstein_sufficient_contract_written_Jrel_representative_open_beta_not_promoted
```

Claim ceiling:

```text
exterior_vacuum_sufficient_contract_no_parent_local_GR_or_PPN_promotion
```

## 3. Exterior qloc Route

For the compact exterior:

```text
E = {r > R_shell}.
```

Ordinary matter is absent there:

```text
S_L^nu = 0.
```

If the checkpoint-221 source identity holds:

```text
nabla_mu Khat^{mu nu} - nabla^nu Gamma_eff
= S_L^nu + d_rel J_rel^nu,
```

then:

```text
q_loc^nu =
P_loc(nabla^nu Gamma_eff - nabla_mu Khat^{mu nu})
= -P_loc d_rel J_rel^nu.
```

So the exterior problem is exactly:

```text
P_loc d_rel J_rel^nu = 0.
```

The non-cheating sufficient route is:

```text
J_rel = d_rel A_rel
```

in the projected local memory sector.

Then:

```text
d_rel J_rel = d_rel^2 A_rel = 0,
```

and:

```text
q_loc^nu = 0.
```

This is the clean route.

It is not a parent derivation yet, because the parent theory has not selected:

```text
the projected memory current type,
the exact local representative,
the boundary primitive A_rel,
the X/no-hair constraint algebra.
```

## 4. Crucial Separation

The exterior shell encloses ordinary mass.

So ordinary gravitational Gauss flux is not zero.

Therefore:

```text
J_rel cannot be ordinary mass flux.
```

It must be:

```text
memory/domain-exchange current only.
```

This matters because if `J_rel` secretly includes the enclosed mass charge,
then exactness fails and the local branch breaks.

So the rule is:

```text
mass charge -> M_eff,
memory exchange -> J_rel.
```

Only the memory exchange current is allowed to be exact/trivial in the local
exterior sector.

## 5. Exterior Vacuum-Einstein Contract

The exact sufficient branch is:

```text
r > R_shell:
S_L^nu = 0,
J_rel = d_rel A_rel,
d_rel J_rel = 0,
q_loc^nu = 0,
T_memory_mu_nu = 0 except M -> M_eff,
X/J_rel/V_def carry no exterior propagating hair,
G_mu_nu = 0.
```

Then the exterior is Schwarzschild:

```text
ds^2 = -(1 - 2GM_eff/r)dt^2
+ (1 - 2GM_eff/r)^-1 dr^2
+ r^2 dOmega^2.
```

In PPN/isotropic expansion:

```text
g_00 = -1 + 2U - 2U^2 + O(U^3),
```

so:

```text
beta = 1.
```

That is the exact route.

But the route still imports:

```text
G_mu_nu = 0
```

as the exterior local metric operator.

So this checkpoint does not prove local GR.

It proves the exact contract a future parent action must satisfy.

## 6. What Improved

Before this checkpoint, beta was:

```text
open second-order coefficient.
```

After this checkpoint, beta is:

```text
conditional Schwarzschild consequence of exterior no-hair/vacuum-Einstein
branch.
```

That is better.

It means the next derivation target is not vague:

```text
derive the J_rel cohomology/projector,
or derive the local Einstein-Hilbert exterior limit.
```

## 7. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| exterior `q_loc` sufficient route written | pass |
| ordinary mass flux separated from `J_rel` | pass |
| beta conditional consequence identified | pass |
| `J_rel` exact representative parent-derived | fail |
| exterior vacuum-Einstein branch parent-derived | fail |
| local GR or PPN promoted | fail |

The pass rows define the contract.

The fail rows keep the belt off the waist.

## 8. Decision

Decision:

```text
exterior_vacuum_Einstein_sufficient_contract_written_Jrel_representative_open_beta_not_promoted
```

Meaning:

```text
the exterior beta route is now an exact sufficient contract. If the source
identity holds, J_rel is exact/trivial in the projected local memory sector,
ordinary mass flux is not J_rel, exterior memory stress vanishes except for
M_eff, and the local metric operator is vacuum Einstein, then the exterior is
Schwarzschild and beta=1.
```

Main gain:

```text
beta is no longer a floating coefficient.
```

Main failure:

```text
the exact J_rel representative and exterior Einstein-Hilbert branch are still
not derived.
```

Current status:

```text
local gamma/slip route conditionally strengthened;
beta route exactly contracted;
local GR still unpromoted;
PPN still unpromoted.
```

## 9. Next Target

Create:

```text
231-Jrel-cohomology-projector-or-local-EH-limit.md
```

Purpose:

```text
choose the next hard derivation: either prove the projected local memory
cohomology makes J_rel exact/trivial, or prove the parent local metric operator
reduces to the Einstein-Hilbert vacuum operator outside compact collars.
```

Pass condition:

```text
J_rel is forced into the exact local memory-exchange class
```

or:

```text
the parent action reduces to G_mu_nu = 0 outside compact collars.
```

Fail condition:

```text
the exterior branch is called GR just because it has been made quiet by
contracts.
```
