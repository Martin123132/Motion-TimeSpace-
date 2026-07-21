# 5018 — hh Legendre-resolvent/Hadamard crossing completion

## What changed

The corrected two-helicity state sum explains why checkpoint 5016 passed its physical tower check while failing numerically after crossing: it had duplicated one helicity assignment. More importantly, brute-force continuation is unnecessary. The exact checkpoint-5008 tower contains

```text
N_J^2=(J-4)!/(J+4)!
     =1/[lambda_J(lambda_J-2)(lambda_J-6)(lambda_J-12)].
```

Therefore its crossed sum is the Green function of `L(L-2)(L-6)(L-12)`. Partial fractions reduce it to four Legendre resolvents. Their apparent poles at degrees `0,1,2,3` disappear because the source enters through `d_w^4 P_J` and `P_l''''=0` for all four degrees.

On the `z>1` exterior sheet the resulting fourth-derivative kernel is

```text
K4(z,w)= z(5z^2-3)/[96(w-1)]
        -(z-1)(5z^2+2z-1)/[96(w-1)^2]
        +(z-1)^2(2z+1)/[48(w-1)^3]
        -(z-1)^3/[48(w-1)^4].
```

The last two terms require a finite-part prescription. The Hadamard prescription is written explicitly in `post-checkpoint-work/source-intake/functional_rg/5018/hh_Hadamard_endpoint_moments.csv` rather than hidden in a numerical contour.

## Completed hh crossing

The independent endpoint checksum is decisive: the exterior result at `z=1` differs from the exact `J<=40` endpoint sum by `-3.571e-04`, inside the earlier empirical `J>40` estimate `3.953e-04`.

| z | physical direct J<=40 | cyclic hh/G^3 | conservative error |
|---:|---:|---:|---:|
| -0.6 | 4.638665 | 19.060168 | 0.0004 |
| -0.3 | -0.96136613 | 76.1925321 | 0.0004 |
| 0 | -4.1810736 | 93.8836231 | 0.0004 |
| 0.3 | -0.96136613 | 76.1925321 | 0.0004 |
| 0.6 | 4.638665 | 19.060168 | 0.0004 |

This supersedes checkpoint 5016's high-variance crossed `hh` central values. It does not supersede its physical integral reconstruction.

## Matched hhh target

With scalar, exact-Hadamard `hh`, graph-complete `phi phi h`, and the global `D1 ReF1` term fixed, the missing `hhh` object is now a precise crossing-complete functional target modulo local `stu`:

| z | known master without hhh | known nonlocal residual | required hhh nonlocal |
|---:|---:|---:|---:|
| -0.6 | 45.88894 | -57.421896 | 28.710948 |
| -0.3 | 164.91394 | 18.018846 | -9.0094229 |
| 0 | 202.33084 | 40.907656 | -20.453828 |
| 0.3 | 164.77696 | 17.881868 | -8.9409342 |
| 0.6 | 45.768191 | -57.542644 | 28.771322 |

The raw 5017 KLT smoke does not implement the crossed Hadamard/Feynman contour:

| z | raw hhh nonlocal | required matched hhh | raw-required |
|---:|---:|---:|---:|
| -0.6 | 0.47436689 | 28.710948 | -28.236581 |
| -0.3 | -0.11222603 | -9.0094229 | 8.8971968 |
| 0 | -0.40298564 | -20.453828 | 20.050842 |
| 0.3 | -0.11219608 | -8.9409342 | 8.8287381 |
| 0.6 | 0.47439836 | 28.771322 | -28.296924 |

That discrepancy is not called a theory failure. It identifies the next derivation precisely: deform the finite-`x` azimuth contour, include every pole-crossing residue, and then recompute the KLT real cut. A local finite scheme change cannot remove a nonlocal mismatch, and no coefficient may be fitted to the target.

## Status

- Opposite-helicity state sum: **repaired**.
- Divergent crossed Legendre series: **replaced by an exact resolvent reduction**.
- Exterior `hh` function and cyclic `hh` contribution: **completed in the declared Hadamard scheme**.
- Crossing-complete matched `hhh` nonlocal target: **derived**.
- Matched graph-complete `hhh`, final locality, numeric UV invariant, local GR, and full MTS: **not yet claimed**.

Next: derive the finite-`x` crossed `hhh` contour residues at amplitude/integrand level, not by fitting the five target numbers, and rerun the complex-safe KLT integral.
