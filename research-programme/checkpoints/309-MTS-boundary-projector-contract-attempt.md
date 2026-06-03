# 309 - MTS Boundary Projector Contract Attempt

Private derivation checkpoint. This is not a public local-GR, PPN, cosmology, galaxy, CMB, or parent-field-theory claim.

## Purpose

Checkpoint 308 showed that the selector theorem needs:

```text
rho_MTS,D = rho[P_MTS B_D, P_MTS B_D].
```

The danger was:

```text
ordinary local EM/matter/environmental baths could fake the MTS boundary bath
and accidentally activate sigma_D.
```

This checkpoint asks:

```text
can P_MTS be made into a precise mathematical contract,
rather than a magic filter inserted to dodge local tests?
```

Short answer:

```text
yes as a conditional projector contract;
no as a parent-derived theorem yet.
```

## Projector Contract

Let `B_D` be the boundary operator/current data on domain `D`.

The candidate is:

```text
P_MTS,D = P_Ward P_coh P_IR P_rel P_ord_perp.
```

The components are:

| Component | Job |
|---|---|
| `P_ord_perp` | removes ordinary EM/matter/environmental bath channels |
| `P_rel` | keeps only non-exact relative boundary-current/memory classes |
| `P_IR` | keeps the MTS IR boundary channel used in `b_D=lim rho/omega` |
| `P_coh` | keeps the coherent scalar/isotropic domain mode |
| `P_Ward` | keeps only modes whose projector/boundary stress is explicitly accounted |

Then:

```text
rho_MTS,D(omega)
= rho[P_MTS,D B_D, P_MTS,D B_D](omega).
```

This is the first clean form of the projector.

## Algebra Conditions

For `P_MTS` to be a real projector:

```text
P_MTS^2 = P_MTS
```

requires:

```text
P_i^2 = P_i,
[P_i,P_j]=0
```

on the admissible boundary subspace, or an equivalent ordered constrained projection theorem.

For the spectral density to be physical:

```text
<P_MTS A,B>_D = <A,P_MTS B>_D
```

requires the parent action to supply:

```text
the boundary inner product / symplectic form,
orthogonality between ordinary and MTS boundary sectors,
self-adjoint component projectors.
```

That is not yet derived.

## What This Fixes

If the contract holds:

```text
P_MTS B_ord = 0
```

for ordinary local EM/matter/environmental bath data.

So ordinary warm laboratories do not automatically activate:

```text
sigma_D.
```

Also:

```text
P_MTS d_rel chi = 0
```

for exact/no-flux local relative currents.

So local relative triviality still gives:

```text
c_D = 0.
```

For FLRW, if the domain carries:

```text
coherent scalar mode,
IR/gapless MTS bath,
nontrivial relative boundary class,
Ward-safe stress accounting,
```

then:

```text
P_MTS B_FLRW != 0.
```

So this projector does not murder the cosmology branch in its sleep.

## Domain Readout

| Domain | Readout | Status |
|---|---|---|
| ordinary warm laboratory | ordinary bath killed if `P_ord_perp` is derived | conditional safe |
| stationary solar-system exterior | silent if relative class and MTS IR bath vanish | conditional safe |
| time-dependent local radiator | safe only if ordinary radiation is projected out and no MTS class appears | edge case |
| black hole / local horizon | may have gapless boundary channel | separate horizon branch |
| galaxy / cluster | may be mixed/nonlocal | empirical/domain branch |
| FLRW coherent domain | retained if coherent/IR/relative/Ward contracts hold | conditional active |

## No-Go Checks

| Claim | Result | Reason |
|---|---|---|
| `P_MTS` can be any useful filter | fail | external projectors are not allowed |
| ordinary bath projection is automatic | fail | needs `P_ord_perp` from parent variables |
| relative cohomology alone defines `P_MTS` | partial | it does not remove generic bath spectra alone |
| fixed-`D` coherent projection is enough | partial | `D` still must be selected |
| projector stress can be omitted | fail | would fake Bianchi conservation |

## Promotion Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | projector attempt is traceable |
| `P_MTS` contract written | pass | projector is no longer vague |
| ordinary bath annihilation defined | conditional pass | generic local baths have an exclusion condition |
| relative exact-current annihilation defined | conditional pass | local trivial class can silence memory activation |
| FLRW retention defined | conditional pass | cosmology is not automatically killed |
| projector idempotence parent-owned | fail | commuting/self-adjoint algebra not derived |
| ordinary/MTS sector split parent-derived | fail | generic bath problem not fully closed |
| domain selection parent-derived | fail | fixed-`D` projection still needs physical `D` |
| Bianchi projector stress parent-closed | conditional pass | formal route exists if stresses are retained |
| selector parent-derived | fail | `sigma_D` still not parent-owned |
| local GR promoted | fail | no PPN/local-GR promotion |
| `B_mem` parent-derived | fail | `2/27` remains empirical closure/theorem target |

## Decision

Decision:

```text
P_MTS_projector_contract_constructed_conditional_not_parent_derived
```

Claim ceiling:

```text
conditional_boundary_projector_contract_no_selector_local_GR_or_Bmem_promotion
```

Meaning:

```text
we now know exactly what P_MTS must be,
but not yet why the parent action forces it.
```

Boxing-score version:

```text
We have the defensive stance written down:
block ordinary bath punches,
keep only relative/coherent/IR memory shots,
and pay the Bianchi tax.
But the stance is still a trained move, not yet a reflex derived from the body mechanics.
```

## Next Step

The sharpest theorem target is now:

```text
derive the ordinary/MTS sector split.
```

Exact contract:

```text
<B_ord, B_MTS>_D = 0
```

or equivalently a parent kinetic/boundary kernel with block structure:

```text
K_boundary =
[
  K_ord      0
  0          K_MTS
].
```

If this works:

```text
ordinary local baths cannot activate sigma_D.
```

If this fails:

```text
P_MTS remains closure-only,
and the better move is empirical holdout testing while local GR stays conditional.
```

## Machine Artifacts

Script:

```text
scripts/MTS_boundary_projector_contract_attempt.py
```

Run:

```text
runs/20260601-000132-MTS-boundary-projector-contract-attempt
```

Output files:

```text
runs/20260601-000132-MTS-boundary-projector-contract-attempt/results/source_register.csv
runs/20260601-000132-MTS-boundary-projector-contract-attempt/results/projector_components.csv
runs/20260601-000132-MTS-boundary-projector-contract-attempt/results/projector_algebra.csv
runs/20260601-000132-MTS-boundary-projector-contract-attempt/results/domain_projection_tests.csv
runs/20260601-000132-MTS-boundary-projector-contract-attempt/results/no_go_tests.csv
runs/20260601-000132-MTS-boundary-projector-contract-attempt/results/promotion_gates.csv
runs/20260601-000132-MTS-boundary-projector-contract-attempt/results/next_targets.csv
runs/20260601-000132-MTS-boundary-projector-contract-attempt/results/decision.csv
```
