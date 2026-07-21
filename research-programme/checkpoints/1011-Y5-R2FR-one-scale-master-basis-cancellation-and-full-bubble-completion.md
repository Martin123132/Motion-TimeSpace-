# 4995 — One-scale master-basis cancellation and finite bubble completion

**Checkpoint marker:** `MTS_4995_ONE_SCALE_MASTER_BASIS_AND_FULL_BUBBLE_COMPLETION`  
**Date:** 2026-07-14  
**Claim status:** private derivation checkpoint; not a full MTS, local-GR, or complete one-loop-amplitude claim.

## Result

The apparent mixed-cut pole found in 4994 is **not an amplitude singularity**. The exact massless one-scale master relation is

```text
I2^D(x) = (D-4)x/[2(D-3)] I3^D(x).
```

Therefore `T I3 + C I2` has a one-parameter coordinate freedom. A pole in `C(D)` can be cancelled exactly by an evanescent shift of `T(D)` without changing the cut. At the exceptional anchor `(t,u)=(1,2)` the transformed coefficient is

```text
T_hat(D) = (5*D**3 - 244*D**2 + 532*D - 80)/(8*(D - 3)*(D - 2)*(D - 1)),   C_hat = -4,
lim[D->4] T_hat = -32.
```

At the generic anchor `(t,u)=(2,3)`:

```text
T_hat(D) = 81*(18*D**3 - 339*D**2 + 682*D - 112)/(32*(D - 3)*(D - 2)*(D - 1)),   C_hat = -81,
lim[D->4] T_hat = -5589/8.
```

Both limits equal the independently completed strict-4D triangle coefficient. Exact rational reconstruction used at least five fit points and at least three held-out dimensions for every coefficient.

## Finite bubble convention

The individual triangle and bubble coefficients are basis coordinates, not observables. In the finite four-dimensional Dunbar convention fixed by the 4994 crossed-channel values, the absence of a constant IR pole and of an on-shell two-scalar/two-graviton UV counterterm imposes

```text
C_s + C_t + C_u = 0.
```

This gives

```text
C_s = t**2*u**2*(t**2 + u**2)/4
C_t = -t**4*u**2/4
C_u = -t**2*u**4/4
C_s^(scalar) = -t*u*(2*t**4 - 11*t**3*u - 11*t*u**3 + 2*u**4)/32
C_s^(hh) = t*u*(2*t**4 - 3*t**3*u - 3*t*u**3 + 2*u**4)/32
```

The strict-4D scalar-cut value `C_s^(scalar)=0` from the preliminary reducer is therefore not promoted to the amplitude coefficient: taking `D=4` before the Laurent expansion erased the finite evanescent redistribution. This is a basis-ordering issue, not a failed cut.

## Source control

- Dunbar–Norridge defines the box/triangle/bubble basis and isolates the remaining finite `d J2` ambiguity in `post-checkpoint-work/source-intake/functional_rg/4986/sources/dunbar_norridge/9512084.tex` (around source lines 1549–1650).
- The same source identifies the one-loop scalar-gravity counterterm as `(D phi.D phi)^2`, first affecting four external scalars (around lines 1656–1680).
- Accettulli Huber et al. prove by a `D`-dimensional field redefinition that `R^2`/`R_mu_nu^2` terms do not produce EH two-scalar/`n`-graviton corrections in `post-checkpoint-work/source-intake/functional_rg/4995/sources/accettulli_huber_1911.10108/errequadro.tex` (around lines 601–646), with the on-shell contact/factorisation argument around lines 720–803.
- Boels–Luo warns that dimension-dependent master choices and `mu^2` sectors matter in `post-checkpoint-work/source-intake/functional_rg/4992/sources/boels_luo_1710.10208/LoopsFromTrees_v2.tex`.

All source-lock clauses passed: `True`.

## What is genuinely still open

1. The cut-free/nonlocal finite rational coefficient `d J2` is not fixed by four-dimensional cuts.
2. The complete outer one-loop `phi phi h h` kernel cannot be claimed until that rational/evanescent remainder is derived by a genuinely `D`-dimensional reconstruction or an independent amplitude source.
3. No local-GR, Newton, or full-MTS claim follows from this checkpoint alone.

The next mathematical target is therefore narrow and concrete: determine `d J2`, then assemble the permutation-complete cut kernel. It is no longer “find the missing bubble.”
