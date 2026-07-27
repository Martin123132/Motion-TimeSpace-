# 5013 — direct-channel D1 support and three-particle locality sum rule

## Result

The suspected missing global `D1 ReF1` term has now been put in the correct channel object. The physical real kernel at `mu^2=s` does have an infinite even-spin expansion, but checkpoint 5011 is a direct `s`-channel discontinuity calculation. Only the `ln(-s)` coefficient can enter that sum:

```text
Disc_s F1/(-2 pi i s^3)
  = (2/pi)[23/15-x(1-x)/30]
  = 55/(18pi)+P2(z)/(90pi).
```

Therefore

```text
Pi_J Disc_s(D1 F1)=0,  J>=4.
```

Adding the full real-angle `F1` tower to the direct cut would mix a crossing-complete real amplitude with one channel discontinuity. That tempting rescue is rejected exactly, rather than tested numerically.

## Exact high-spin reduction

For the full real kernel, the useful distinction is explicit. For even `J>=4`,

```text
int_0^1 dx x^m P_J(1-2x) ln x
 =(-1)^(m+1)(m!)^2 (J-m-1)!/(J+m+1)!,

f_J^real
 =-[2/(15pi)] [lambda_J^2-14lambda_J+1680]
   (J-4)!/(J+4)!,
lambda_J=J(J+1).
```

Those nonzero moments belong to the real crossing object, not the direct cut. The renormalized direct discontinuity must be a degree-six local polynomial and hence has no `J>=4` support. Since the direct `D1` term also has no such support, locality gives the exact all-spin sum rule

```text
D_hhh,J + D_phiphih,J = -D_hh,J,  even J>=4.
```

This fixes the entire infinite high-spin three-particle tower in terms of the completed checkpoint-5008 `hh` kernel. It does not pretend that the five-point integral has independently verified the relation.

| J | D_hh/G^3 | required (D_hhh+D_phiphih)/G^3 | direct D1 high-spin |
|---:|---:|---:|---:|
| 4 | -1.321062236 | 1.321062236 | 0 |
| 6 | -0.08059671111 | 0.08059671111 | 0 |
| 8 | -0.01368153444 | 0.01368153444 | 0 |
| 10 | -0.003581392931 | 0.003581392931 | 0 |
| 12 | -0.001210158137 | 0.001210158137 | 0 |

## What remains

The independent numerical primitive is no longer an uncontrolled infinite tower. Odd modes vanish by crossing, every even `J>=4` mode is fixed by locality, and only two three-particle numbers remain:

```text
D_hhh+phiphih,J=0,
D_hhh+phiphih,J=2.
```

The next calculation must construct one channel-consistent finite-`x` subtraction and evaluate those two low angular-first integrals. `J=4` is retained as a non-fitted validation mode: it must reproduce `1.32106223583` in `G^3` normalization.

Numeric `K_mu`, `K_ang`, local GR, and full MTS are not claimed.
