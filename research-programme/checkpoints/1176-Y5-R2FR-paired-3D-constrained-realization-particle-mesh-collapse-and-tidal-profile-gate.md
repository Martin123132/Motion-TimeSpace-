# 5160 - Paired 3-D constrained-realization particle-mesh collapse and tidal-profile gate

Marker: `MTS_5160_PAIRED_3D_CONSTRAINED_PM_COLLAPSE_GATE`.

Date: `2026-07-20`.

## Decision

Checkpoint 5160 executes the nonspherical route demanded by checkpoint 5159.
It retains the residual Gaussian covariance, conditions the same one-sigma
UGC09133 Lagrangian patch, evolves antithetic phase realizations under the
same periodic Vlasov--Poisson law and measures a three-dimensional halo centre
after tidal evolution. No profile parameter is read back into the run.

The result is an outer-halo comparator, not a wave-core calculation. Every
transition radius `R_n` lies below the declared three-force-cell resolution
floor, so no numerical `q_parent` verdict is permitted.

## 1. Exact paired constraint

For a raw Gaussian field `delta_r` and top-hat functional `C`, the implemented
Hoffman--Ribak residual is

```text
delta_res=delta_r-C[delta_r] Cov(delta,C)/Var(C),
C[delta_res]=0.
```

The continuous source-backed conditional mean is then added with signs
`+delta_res` and `-delta_res`. Their mean is exactly the constrained mean.
Across the generated states, the maximum constraint error is
`1.9984014443252818e-15`, pair-mean error is
`1.7763568394002505e-15` and residual antisymmetry error is
`7.105427357601002e-15`.

The finite periodic box contains between
`0.6495241258577271` and
`0.6495246277745004` of the full top-hat sigma. Missing
long covariance is carried only by the source-integrated conditional mean;
the residual realization is not falsely labelled a complete cosmological
volume.

## 2. Three-dimensional equations executed

Zel'dovich positions and canonical momenta are generated from the full 3-D
density field. The KDK particle mesh evolves

```text
dx/da=P/(a^3 E),
dP/da=F/(a^2 E),
nabla^2 chi=(3/2) Omega_m delta,
F=-nabla chi.
```

CIC assignment and interpolation use the same periodic mesh. The main matrix
contains `14` runs and
`652738560` particle-step updates. The homogeneous
force control is `0.0`. The longest tested
mode follows continuum growth with relative error
`0.012598070153085006`. The second mode follows the
independently integrated finite-mesh response with error
`0.0013624899655244604`; its separately recorded
continuum attenuation is
`0.04863231844988414`. This distinction avoids
mistaking the derived CIC/central-difference transfer for a cosmological-force
failure.

## 3. No-refit outer profile

The paired mean is scored against both frozen parent mappings. Resolved profile
bins range from `5` to
`17`. The base three-mass fixed-edge
motion-mass ratio spans `1.202754725648407` to
`1.2053421213544837` and the finite velocity log-RMSE
spans `0.031930603618896485` to
`0.03252198583060008` dex.

The compact-edge threshold passes in
`0` of `14` scores.
The smallest paired exterior/interior excess-density ratio is
`0.3094561286744944`.

These numbers are used only if the paired force/time convergence gate closes.
That gate is `PASS`: its fixed-edge mass-ratio span
is `0.08275028605275514` and its exterior-ratio span
is `0.03606682726265903`. Quantitative outer-profile
claims remain `CONDITIONAL_OUTER_RESULT`.

The pass is deliberately narrower than full particle convergence: it covers
force and time controls at fixed `64^3` particle phases. The `96^3` run adds
short modes and is recorded as non-phase-matched, so it cannot be used as a
strict one-variable convergence comparison. A nested shared-mode realization
is still required before the conditional outer result can be called universal.

## 4. What this proves and does not prove

The calculation removes the exact `L=0` obstruction of the radial mean:
nonspherical residual modes generate tidal forces and nonradial particle
motion. It does not prove an isotropic Eddington distribution, a universal
attractor or a wave core. The paired realization is one antithetic control,
not a sufficient cosmic-variance ensemble.

```text
paired residual covariance retained                  = yes;
three-dimensional tidal evolution executed           = yes;
profile parameters fitted after evolution             = no;
q_parent transition resolved                          = no;
outer profile convergence gate                        = PASS;
compact p=2 edge selected                              = NOT_SELECTED_AT_RESOLVED_PM_SCALE;
wave/density-matrix core selected                      = no;
parent primordial covariance derived                  = no.
```

## 5. Machine-cog verdict

The simulation changes only the nonzero cosmological state. The action,
metric rank, `G_N`, visible matter coupling and Maxwell/Poynting Hilbert source
remain untouched. The same Cartesian zero state therefore retains the local
GR/Newton/Mercury cog while the occupied branch is tested for galactic
formation.

This is the single-machine criterion: no arena-specific law is switched on.
The same parent equations must leave the Mercury cog turning and generate any
galactic activation only through their nonzero state and inherited scales.

If the outer convergence gate fails, the next step is numerical repair before
any theory inference. If it closes but the edge fails, the free collisionless
parent does not derive the checkpoint-5154 compact edge and the missing parent
interaction must be identified explicitly. A wave zoom is legitimate only
after that outer arbitration.

Primary method references:

- constrained Gaussian fields: https://arxiv.org/abs/astro-ph/9507024
- particle mesh evolution: https://arxiv.org/abs/1603.00476
- FDM transfer: https://arxiv.org/abs/astro-ph/0003365

All `31` validations pass. Every row remains
nonclaim. The protected `formalization-workbench` digest is
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. Galaxy sources were
read-only and no GitHub action occurred.
