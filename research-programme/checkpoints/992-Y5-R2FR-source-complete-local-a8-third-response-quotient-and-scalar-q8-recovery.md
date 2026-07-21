# 4976 - Source-complete local a8 third-response quotient and scalar q8 recovery

Marker: `PPC4161_SCALAR_COMPLETE_LOCAL_A8_RESPONSE_4976`  
Runner marker: `MTS_4976_SCALAR_COMPLETE_LOCAL_A8_RESPONSE`

## Decision

The checkpoint-4975 `q^8` leakage is closed rather than fitted. The local
Barvinsky--Vilkovisky `a4` coefficient supplies the complete minimal-scalar
third-response sector at mass dimension eight through cubic curvature. After
setting the bundle curvature to zero and `P=R/6`, it contains two quadratic
four-derivative operators and fifteen consolidated cubic two-derivative
operators. Their coefficients are copied from twenty-five source terms and
are never inferred from the determinant response.

The source-fixed vector reproduces the independently calculated scalar
determinant `q^8` response on all twelve original geometries with relative
residual

```text
1.7200056164357514e-15.
```

Eight new geometries, absent from the construction and from checkpoint 4975,
give relative residual `2.8706094306143018e-15`. The local response matrix
agrees between `N=6` and `N=8` grids to `3.879527387949945e-15`. This is a
source-derived recovery, not a saturated regression.

The result closes the free-scalar local `a8` response. It does not by itself
derive the massless nonlocal logarithm, interacting motion, graviton/ghost
kernels, a physical four-graviton amplitude, exact all-operator compact GR,
or full MTS.

## 1. Local minimal-scalar a8

The primary source uses

```text
H=Box+(P-R/6),
R^mu_(alpha nu beta)=partial_nu Gamma^mu_(alpha beta)-partial_beta Gamma^mu_(alpha nu)+... .
```

For the free minimal scalar, `H=Box`, so `P=R/6` and the internal bundle
curvature vanishes. On the closed periodic four-torus, the quadratic part is

```text
integral sqrt(g) [
  (11/30240) R Box^2 R
 +(1/15120) R_mn Box^2 R^mn
].
```

Self-adjointness gives the implemented forms `(Box R)^2` and
`(Box R_mn)(Box R^mn)`. The new covariant-Laplacian engine independently
reproduces

```text
integral R Box R             = -integral (nabla R)^2,
integral R_mn Box R^mn       = -integral (nabla R_mn)^2
```

against the established checkpoint-4911 templates with relative residual
`2.8761843232752394e-15`.

The fifteen cubic operators and their source-fixed coefficients are

```text
C1  R^2 Box R                                      211/907200
C2  R R^mn nabla_m nabla_n R                        1/6480
C3  R^mn nabla_m R nabla_n R                      -11/453600
C4  R nabla^m R^na nabla_n R_ma                    -1/5400
C5  R R^mn Box R_mn                               -13/75600
C6  (Box R) R_mn R^mn                              -1/21600
C7  (Box R) R_mnab R^mnab                          17/100800
C8  R R^mnab nabla_m nabla_a R_nb                   1/2700
C9  (Box R_ab) R^a_mnl R^b_mnl                      1/6300
C10 R_ls nabla^l R^mnab nabla^s R_mnab             -1/25200
C11 R^manb nabla_m R_nl nabla^l R_ab                -1/6300
C12 R^abmn nabla_a R_bl nabla_m R_n^l               -2/4725
C13 R^mn nabla_a R_bm nabla^b R_n^a                  1/37800
C14 R^mn nabla_m R^ab nabla_n R_ab                  -1/9450
C15 (Box R^m_a) R^a_b R^b_m                         -1/7560.
```

Quartic-curvature terms in the exact `a8` coefficient start at fourth metric
order around flat space and therefore cannot contribute to this third
response.

## 2. Convention lock

The earlier checkpoint-4911 cubic sign note applied to its Vassilevich
source. It cannot be transferred to a different source by name alone. The
Barvinsky--Vilkovisky convention at local source lines 198--202 is exactly
the convention implemented by the geometry engine:

```text
R^r_(s m n)=partial_m Gamma^r_(n s)-partial_n Gamma^r_(m s)+... .
```

Consequently the quadratic and cubic source coefficients both enter with
the displayed sign. Applying the old source's sign would fail the independent
determinant response; using the convention stated by the present source
closes it geometry by geometry.

## 3. Enlarged quotient

The twenty-geometry response matrix has shape `20 x 17`, rank `15`, and
nullity `2`. The nullity does not represent two fitted physical parameters.
It is exhausted by integrated geometric identities.

The first is closed-manifold integration by parts plus the contracted Bianchi
identity:

```text
C2+C3-C1/4=0.
```

The second is the four-dimensional five-index-antisymmetrization/
Gauss--Bonnet descendant identified in source Appendix A.35--A.39:

```text
4 C3-8 C4-8 C5+4 C6-C7+8 C8+4 C9
 +16 C11+16 C12-16 C13=0.
```

Their executable relative residuals are below `1.31e-16`. Hence the tested
integrated quotient has fifteen independent directions, exactly matching its
measured rank.

## 4. Independent determinant recovery

Checkpoint 4975 supplies the independently integrated Taylor response. The
heat-kernel target in the current normalization is

```text
a8,target=-2(4pi)^2 W_123,8.
```

The source prediction is

```text
a8,prediction=M_quadratic c_quadratic+M_cubic c_cubic.
```

No least-squares coefficient appears. On the original twelve geometries,

```text
quadratic-only relative residual = 0.23819731015224466,
cubic-only relative residual     = 0.7741989278317071,
complete relative residual       = 1.7200056164357514e-15.
```

The two incomplete pieces complement one another exactly. This explains the
checkpoint-4975 `3.021408%` leakage: the restricted
`diag(sum_i q_i^2) M6` image omitted required local `a8` directions; neither
the determinant nor the numerical pipeline was inconsistent.

The eight fresh geometries `G12--G19` independently repeat the determinant
integration at radial order 24 and angular order 10. Their largest absolute
residual is `8.326672684688674e-17`.

## 5. What is and is not closed

```text
free-scalar q6 control                         = exact;
free-scalar complete local q8/a8 response      = source-derived and exact;
dimension-eight integrated quotient rank       = 15;
dimension-eight integrated quotient nullity    = 2 geometric identities;
restricted sigma1-dressed q6 image             = superseded as incomplete;
checkpoint-4975 projected C3 estimator          = remains diagnostic only;
free-scalar q8 PT-m3 component kernel           = retained exact;
finite-momentum nonlocal scalar form factors    = next target;
controlled massless logarithm                   = open;
interacting motion/graviton/ghost responses     = open;
exact all-operator compact GR                   = false;
full MTS                                        = false.
```

The local recovery does not make a unique physical `C3` derivative. The two
integrated identities and on-shell equation-of-motion reductions mean that
such a label depends on the chosen off-shell basis. The invariant advance is
the complete source-fixed response vector.

## 6. Next calculation

Checkpoint 4977 should stop extending the local Taylor series one order at a
time. The acquired Barvinsky--Vilkovisky material contains the full
third-order nonlocal form factors. The next calculation is to specialize
those form factors to the minimal scalar, reconstruct the finite-momentum
third response, compare it directly with the determinant away from `q=0`,
and only then take the controlled massless limit and extract its logarithmic
part. That is the shortest route from this exact local germ to the physical
nonlocal scalar kernel.

No GitHub action or public claim is authorized.

## Outputs

- `post-checkpoint-work/scripts/Y5_R2FR_4976_scalar_complete_local_a8_response.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4976_scalar_complete_local_a8_response_validation.py`
- `post-checkpoint-work/source-intake/functional_rg/4976/C3_scalar_local_a8_operator_basis.csv`
- `post-checkpoint-work/source-intake/functional_rg/4976/C3_scalar_local_a8_source_term_ledger.csv`
- `post-checkpoint-work/source-intake/functional_rg/4976/C3_scalar_local_a8_response_matrix.csv`
- `post-checkpoint-work/source-intake/functional_rg/4976/C3_scalar_local_a8_recovery.csv`
- `post-checkpoint-work/source-intake/functional_rg/4976/C3_scalar_local_a8_out_of_sample.csv`
- `post-checkpoint-work/source-intake/functional_rg/4976/C3_scalar_local_a8_quotient.csv`
- `post-checkpoint-work/source-intake/functional_rg/4976/C3_scalar_local_a8_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4976/C3_scalar_complete_local_a8_results.json`

The runner passes `8/8` internal gates. The independent validator passes
`31/31`; validation CSV SHA256 is
`3e95b382210b5ef40fa873c193a347ae984f23a5fd40487b888b6205ba61d66a`.
