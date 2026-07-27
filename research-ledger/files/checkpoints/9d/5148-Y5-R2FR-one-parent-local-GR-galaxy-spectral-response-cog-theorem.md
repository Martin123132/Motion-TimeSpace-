# 5148 - One-parent local-GR/galaxy spectral-response cog theorem

Marker: `MTS_5148_ONE_PARENT_LOCAL_GR_GALAXY_SPECTRAL_RESPONSE_COG_THEOREM`.

Date: `2026-07-20`.

## Decision

This checkpoint constructs a concrete bridge instead of recording another
missing coefficient. The already selected parent has one universal metric
source and an exact reflection-even `psi=0` local branch. Its physical Hessian
can therefore have a state-dependent block form

```text
Gamma2 = 1/2 (h,chi) [[K_h,B],[B_dagger,K_chi]] (h,chi)^T + h.T/2.
```

Eliminating the motion response gives the exact Schur complement

```text
K_eff = K_h - B K_chi^-1 B_dagger.
```

On the certified local branch `B=0`, so the Einstein/Newton/Mercury cog is
unchanged. A nonzero motion state may instead give `B!=0`; this is a branch of
the same action, not a second gravitational coupling.

## Spectral response derived from the two required cogs

Let `y=mu/k` and define

```text
n_q(y) = y^q/(1+y^q),
d n_q/d ln y = q n_q(1-n_q).
```

Flat outer rotation requires a static `1/k^3` response, while the locked MTS
inner support requires the extra circular-speed term to start as `r^q`.
Within the no-new-scale monomial class `C=y^a n_q^b`, the low-frequency
plateau fixes `a=1` and the inner `r^q` power then fixes `b=1`. The unique
minimal member of that declared class is therefore

```text
C_q(y) = y n_q(y) = y^(1+q)/(1+y^q),
D_h(k) = D_GR(k)[1+A C_q(mu/k)].
```

Thus `C_q~(mu/k)^(1+q)` at high frequency and `C_q~mu/k` at low
frequency. The corresponding required Schur complement is

```text
Sigma/K_h = A C_q/(1+A C_q),
K_eff = K_h/(1+A C_q).
```

For `A>=0` the Euclidean static kernel has no new zero. A causal retarded CTP
realization is still required before this becomes a parent-derived physical
law.

## Real-space theorem

For a point-source Green function the extra circular speed is

```text
Delta V^2(r) = [2 A G M mu/pi] S_q(mu r),
S_q(x) = 1-(q/x) integral_0^infinity du (sin u/u)
         (x/u)^(1+q)/[1+(x/u)^q]^2.
```

It obeys `S_q(x)->1` at large `x` and
`S_q(x)=0.7907858771245267 x^q+...` for the locked
`q=0.77`. Hence the same response is negligible relative to Newton
at short distance but gives a flat plateau at long distance.

After one global spectral-to-real scale conversion
`mu L_eff=2.921396974200681`, this support approximates the
galaxy lab's `1-exp[-(r/L_eff)^q]` with RMSE
`0.0616004223044119` over `10^-3 <= r/L_eff <= 10^1.5`.

## Read-only 175-galaxy smoke

Using the galaxy lab's own locked constants and exact `L_eff` construction,
the outer baryonic proxy `GM_proxy=Vbar_out^2 r_out` implies

```text
A_i = pi Gamma0 L_eff^2/(2 mu L_eff GM_proxy).
```

Across all `175` LTGs, `A` has geometric mean
`1.0691523388681814`, median
`1.109102407624266`, and 16--84 percent range
`[0.5320173994224269,2.171141304980281]`;
`116/175` rows lie within a factor two of
unity. The log relation has Pearson `r=0.9308544875726481` and
slope `0.8009552174166118 +/- 0.023903426418726347`.

This is promising interface evidence, not a galaxy claim. `Vbar_out^2 r_out`
is only a spherical mass proxy for disk data, the scatter is material, and
`A` and `mu` have not yet been calculated from the parent CTP state.

## Local suppression and Poynting

Combining the largest inferred `A` with the smallest `L_eff` gives a deliberately
conservative Mercury static-kernel correction of
`2.1134587844508184e-14`, far below the checkpoint's `1e-5`
smoke ceiling. This does not replace a covariant PPN calculation, but it proves
that the candidate response has the required UV suppression rather than
breaking Mercury to repair galaxies.

The Poynting vector remains part of the one Hilbert source. Checkpoint 4952
already proves that stationary/DC flux does not create motion pairs, so it is
not smuggled in as an activation source. Time-dependent electromagnetic or
gravitational flux can matter only if the next retarded CTP self-energy
calculation derives it.

## Claim boundary and next derivation

Derived here:

- the unique minimal spectral factor within the declared `y^a n_q^b` class
  satisfying the selected inner and outer power requirements;
- exact logistic phase flow;
- exact static Schur-complement target and Euclidean positivity;
- the real-space support transform and short/long-distance limits;
- a read-only 175-galaxy amplitude/shape smoke and conservative local bound.

Not yet derived:

- `B K_ret^-1 B_dagger` from the actual occupied motion CTP Hessian;
- the state law fixing `A` and `mu` from source history without per-galaxy
  fitting;
- the locked numeric `q=0.77` from the parent, since the direct 4948
  one-point exponent failed;
- causal spectral positivity, full lensing/slip and PPN projections.

The next target is therefore one calculation: evaluate the retarded
state-dependent motion polarization and test whether its transverse metric
self-energy has the required `A C_q/(1+A C_q)` form. If it does not, this
route is rejected rather than retained as closure.

The protected `formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No GitHub or galaxy-repo
write occurred.
