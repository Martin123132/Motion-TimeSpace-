# 273 - `Cperp` Relative Exactness for the C-Sector

Private derivation checkpoint. This is not a public local-GR, CMB, BAO, or unified-field claim.

## Purpose

Checkpoint 272 left the decisive burden:

```text
derive Cperp relative exactness for the C-sector,
or label the projected metric as closure.
```

This checkpoint tests whether the `J_rel` relative-cohomology exactness result transfers to `Cperp`.

## Machine Artifact

Script:

```text
scripts/Cperp_relative_exactness_C_sector.py
```

Run:

```text
runs/20260601-000091-Cperp-relative-exactness-C-sector
```

Status:

```text
Cperp_scalar_relative_exactness_not_derived_projected_metric_demoted_to_explicit_closure
```

Claim ceiling:

```text
Cperp_exactness_failed_internal_closure_label_no_local_GR_or_unification_promotion
```

## Main Result

The exactness transfer fails for the current scalar C-sector.

Checkpoint 231 had a real cohomology win for:

```text
J_rel
```

because `J_rel` is a projected flux/current-like form. On the compact exterior shell:

```text
H^2(Sigma_ext, partial Sigma_ext) = 0
```

after ordinary mass flux and shear are projected away.

That does **not** automatically apply to:

```text
Cperp
```

because `Cperp` is currently a scalar / 0-form representative.

## Degree Audit

| Object | Degree | Verdict |
|---|---|---|
| `J_rel` memory flux | 2-form/current-like | conditional exactness route exists |
| `Cperp` scalar | 0-form | arbitrary residual exactness not proved |
| `eta_perp` scalar shift | 0-form parameter | not de Rham-exact in the needed sense |
| `dCperp` | exact 1-form | insufficient; gradients can still be physical |
| lifted `C` connection/holonomy | form/current sector | future theorem route |

The key issue:

```text
H^0(D, partial D) = 0
```

does not mean:

```text
any scalar residual profile is gauge.
```

It means boundary-zero closed scalar classes are trivial.

That is far too narrow to prove arbitrary local `Cperp` residual shifts are gauge.

## What Fails

Three attempted transfers fail:

```text
1. J_rel exactness -> Cperp exactness
```

fails because flux/current cohomology is not scalar representative cohomology.

```text
2. relative H^0 triviality -> Cperp gauge
```

fails because it only kills closed boundary-zero scalar classes.

```text
3. dCperp exactness -> no physical Cperp
```

fails because exact gradients can still be physical if the action contains gradient energy, forces, or matter coupling.

Therefore:

```text
Cperp scalar relative exactness is not derived.
```

## Closure Demotion

The projected matter metric:

```text
exp(P_D C) g_munu
```

must now be labelled:

```text
explicit effective closure
```

for the current scalar C-sector.

Allowed:

```text
use it as a disciplined local-silence / BAO common-mode effective branch.
```

Forbidden:

```text
claim it is a parent-derived matter coupling,
claim local GR is derived from it,
claim Cperp is gauge.
```

This is not a dead end for the whole programme.

It is a clean demotion of one route.

## Future Theorem Route

There is still a possible harder route:

```text
lift the C-sector from a scalar representative
to a form / connection / holonomy / boundary-class sector.
```

Then `C_D` could arise as:

```text
a boundary/domain integral,
a holonomy,
or a relative class observable,
```

while local residuals become exact representatives.

But that would be a new theorem route, not something already proved.

Required future contracts:

| Contract | Status |
|---|---|
| lift `C` to form/holonomy class | future route |
| local residual exactness | not derived |
| FLRW nonzero class survives | conditional previous |
| matter couples to class observable | closure currently |
| domain variation / Bianchi | open |
| amplitude reduction | not derived |

## Decision

Decision:

```text
Cperp_scalar_relative_exactness_not_derived_projected_metric_demoted_to_explicit_closure
```

Meaning:

```text
The current scalar Cperp sector does not inherit the Jrel relative-cohomology
exactness theorem.
```

Therefore:

```text
exp(P_D C)g must be labelled an explicit effective closure
unless a future lifted form/holonomy C-sector derives Cperp exactness.
```

## Current Theory Status

This is a setback for the strongest local derivation route, but it is also a discipline win.

We now know:

```text
projected metric selector:
  effective closure in current scalar C-sector.

ordinary exp(C)g metric:
  rejected as lead because it sources Cperp.

future exact route:
  requires lifted C-sector, not scalar Cperp.
```

So the local branch is not dead, but it is no longer allowed to masquerade as derived local GR.

## Next Target

Two honest next moves exist:

```text
1. Lifted C-sector route:
   attempt to derive C_D as form/holonomy/boundary class.

2. Empirical closure route:
   keep exp(P_D C)g explicitly closure-labelled and test the effective branch.
```

Given the goal of a serious testable framework, the next practical move is probably:

```text
write a local/cosmology status ledger separating derived, conditional, closure, and failed routes,
then choose whether to keep deriving or start empirical closure tests.
```

## Claim Gates

| Gate | Result |
|---|---|
| transfer `J_rel` exactness to `Cperp` | fail |
| relative `H^0` scalar gate | fail for arbitrary profiles |
| `dCperp` exact 1-form gate | insufficient |
| first-class constraint gate | not derived |
| projected metric closure policy | demote |
| local-GR/unification promotion | forbidden |

## Validation

- Script compiles in `.venv-score`.
- Run completed and wrote `DONE.txt`.
- CSV outputs parse cleanly.
- Cited source paths exist.
- No changes were made to `formalization-workbench`.
- Claim ceiling remains internal only; no local-GR or unification promotion is allowed.
