# 4977 - Massless minimal-scalar nonlocal form factors and log location

Marker: `PPC4161_MASSLESS_SCALAR_NONLOCAL_FORM_FACTORS_4977`  
Runner marker: `MTS_4977_MASSLESS_SCALAR_NONLOCAL_FORM_FACTORS`

## Decision

The free minimal-scalar calculation has crossed from a finite local Taylor
germ to the source-complete massless finite-momentum cubic-curvature action.
After setting `P=R/6` and the internal bundle curvature to zero, eighteen of
the twenty-nine Barvinsky--Vilkovisky form factors survive and consolidate
into eleven minimal-scalar curvature channels. Their coefficients are
functions of the three external boxes; no coefficient is fitted.

The source supplies two independent representations of every form factor:
an alpha-simplex integral and an explicit triangle/log-ratio expression.
Only the source-prescribed symmetrized form factors are meaningful. Across
three nondegenerate Euclidean momentum triples and all eighteen surviving
indices, the two representations agree with maximum relative difference

```text
8.640926257429126e-13.
```

The eleven reduced minimal-scalar channels agree to
`5.1542112619360135e-12`. A singularity-resolved six-sector simplex rule
agrees between orders 24 and 40 to `6.087422302519344e-14`.

This closes the massless scalar cubic-curvature form factors. It does not yet
close the full third metric response, because the latter also receives the
third variation of the quadratic nonlocal curvature action, including the
metric variation of `log(-Box/mu^2)`.

## 1. Source specialization

For the source operator

```text
H=Box+(P-R/6),
```

the free minimally coupled scalar has

```text
P=R/6,
calR_mn=0.
```

The surviving source indices are

```text
1,4,5,6,9,10,11,15,16,17,22,23,24,25,26,27,28,29.
```

After identical structures are consolidated, the eleven channels are

```text
S01 R1 R2 R3:
    Gamma9+(1/6)Gamma4+(1/36)Gamma6+(1/216)Gamma1
S02 Ricci1.Ricci2 R3:
    Gamma11+(1/6)Gamma5
S03 Ricci1 Ricci2 Ricci3:
    Gamma10
S04 Ricci1 grad(R2) grad(R3):
    Gamma22+(1/6)Gamma15
S05 grad(Ricci1) grad(Ricci2) R3:
    Gamma23+(1/6)Gamma16
S06 Ricci1 Hess(R2) R3:
    (1/36)Gamma17
S07 Ricci1 grad(Ricci2) grad(Ricci3):
    Gamma24
S08 Ricci1 cross-grad(Ricci2,Ricci3):
    Gamma25
S09 Hess(Ricci1) Hess(Ricci2) R3:
    Gamma27+(1/6)Gamma26
S10 grad(Ricci1) grad(Ricci2) Hess(Ricci3):
    Gamma28
S11 Hess(Ricci1) Hess(Ricci2) Hess(Ricci3):
    Gamma29.
```

The finite-momentum action is therefore

```text
-W_scalar^(3)=1/[2(4pi)^2] integral sqrt(g)
  sum_A F_A(-Box1,-Box2,-Box3) I_A+O(curvature^4),
```

where the eleven `F_A` are the combinations above. This is a complete
cubic-curvature representation, not yet the complete third variation with
respect to the metric.

## 2. Two-representation identity

The alpha source writes

```text
Gamma_i=<dff_i/(-Omega)>_3+tr_i
 +sum_(m<n) lh_mni log(Box_m/Box_n)/(Box_m-Box_n),
```

while the explicit source writes

```text
Gamma_i=rf_i Gamma_basic+rt_i
 +sum_(m<n) rl_mni log(Box_m/Box_n)
 +sum_(m<n) lh_mni log(Box_m/Box_n)/(Box_m-Box_n),
```

with

```text
Gamma_basic=integral_simplex
 [-a1 a2 Box3-a1 a3 Box2-a2 a3 Box1]^-1.
```

The source warns that unsymmetrized representatives may differ by terms
which vanish after symmetrization. The first attempted direct comparison
correctly failed that invalid test. Implementing equations (2.46)--(2.74)
for each index reduces the maximum discrepancy to `8.64e-13`.

The form factors obey the massless homogeneity law

```text
Gamma_i(lambda Box1,lambda Box2,lambda Box3)
 =lambda^[-1-d_i/2] Gamma_i(Box1,Box2,Box3),
```

where `d_i` is the number of explicit derivatives in the associated cubic
structure. The measured maximum residual at `lambda=7` is
`2.1716118327804244e-11`.

## 3. Independent determinant normalization

The potential-only channel provides a direct check not dependent on the
metric-curvature reconstruction. The source has

```text
Gamma1=Gamma_basic/3.
```

The mixed coefficient of three distinct scalar potentials in the source
`-W` convention is

```text
6 Gamma1/[2(4pi)^2]=Gamma_basic/(4pi)^2.
```

Direct expansion of the free scalar determinant gives the massless triangle

```text
integral d^4p/(2pi)^4
  1/[p^2(p+q1)^2(p-q3)^2]
 =Gamma_basic/(16pi^2)
 =Gamma_basic/(4pi)^2.
```

The maximum numerical normalization residual is
`2.1842604679129222e-16`.

## 4. Exact location of the massless logarithm

The cubic `Gamma_i` contain no arbitrary scale. They use only the basic
triangle, rational box functions, `log(Box_m/Box_n)`, and divided log ratios.
Consequently there is no independent absolute `mu` logarithm in the
cubic-curvature form factors.

For the minimal scalar, the quadratic action contains

```text
-W_scalar,log^(2)=1/[2(4pi)^2] integral sqrt(g) [
 -(1/60) Ricci_mn log(-Box/mu^2) Ricci^mn
 -(1/120) R log(-Box/mu^2) R
].
```

The second coefficient follows exactly from

```text
gamma2+gamma3/6+gamma4/36.
```

Therefore the absolute logarithmic part of the full third metric response is
not missing or zero: it is inherited from the third metric variation of this
quadratic nonlocal action. The cubic-curvature channels supply the remaining
scale-free finite-momentum pieces.

## 5. What is and is not closed

```text
free-scalar local q6 response                  = exact;
free-scalar complete local q8/a8 response      = exact;
massless scalar cubic-curvature form factors   = source-complete;
minimal-scalar reduced channels                = 11;
alpha versus explicit source identity          = validated;
potential determinant normalization            = exact;
quadratic massless logarithm                    = derived exactly;
independent cubic absolute mu-log               = absent by source theorem;
full third metric response                      = open;
interacting motion/graviton/ghost responses     = open;
exact all-operator compact GR                   = false;
full MTS                                        = false.
```

## 6. Next calculation

Checkpoint 4978 should calculate the third flat-background metric variation
of the two exact quadratic nonlocal functionals, including variation of the
measure, curvatures, index contractions, and the operator
`log(-Box/mu^2)`. It should then add the eleven cubic-curvature channels and
compare the assembled finite-momentum metric response with the direct scalar
determinant. That is the shortest remaining route to a complete free-scalar
massless `TTT` kernel.

No GitHub action or full-MTS claim is authorized.

## Outputs

- `post-checkpoint-work/scripts/Y5_R2FR_4977_massless_scalar_nonlocal_form_factor_evaluator.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4977_massless_scalar_nonlocal_form_factor_validation.py`
- `post-checkpoint-work/source-intake/functional_rg/4977/C3_massless_scalar_structure_map.csv`
- `post-checkpoint-work/source-intake/functional_rg/4977/C3_massless_scalar_form_factor_manifest.csv`
- `post-checkpoint-work/source-intake/functional_rg/4977/C3_massless_scalar_form_factor_crosscheck.csv`
- `post-checkpoint-work/source-intake/functional_rg/4977/C3_massless_scalar_reduced_channel_values.csv`
- `post-checkpoint-work/source-intake/functional_rg/4977/C3_massless_scalar_scale_homogeneity.csv`
- `post-checkpoint-work/source-intake/functional_rg/4977/C3_massless_scalar_potential_triangle.csv`
- `post-checkpoint-work/source-intake/functional_rg/4977/C3_massless_scalar_quadratic_log.csv`
- `post-checkpoint-work/source-intake/functional_rg/4977/C3_massless_scalar_nonlocal_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4977/C3_massless_scalar_nonlocal_results.json`

The runner passes `11/11` internal gates. The independent validator passes
`45/45`; validation CSV SHA256 is
`9d9fe23ddce5a18aea107342fbf59ad5df9c3079fff86062e5be1cc9b40c934e`.
