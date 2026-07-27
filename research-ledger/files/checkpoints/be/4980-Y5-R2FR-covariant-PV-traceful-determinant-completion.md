# 4980 - Covariant PV traceful determinant completion

Formal marker: `PPC4161_COVARIANT_PV_TRACEFUL_SCALAR_COMPLETION_4980`.

## Decision

Checkpoint 4980 closes the traceful finite contact left open by checkpoint
4979 for the complete one-loop free minimal-scalar determinant. The missing
term is derived with a four-dimensional covariant Pauli--Villars regulator,
not fitted to G03 or G04 and not supplied as a plateau or closure axiom.

The result is deliberately scoped:

```text
covariant massive-regulator response                    = derived;
q4 coefficient before large cancellations               = analytic;
PV power-divergence cancellations                        = exact;
common finite scheme                                     = fixed by 48 two-point controls;
old traceful controls G03/G04                            = matched;
fresh traceful controls G05/G06                          = matched;
regulator-mass independence                              = passed;
complete free-scalar traceful finite determinant         = promoted;
interacting motion/graviton/ghost determinant            = open;
full MTS                                                  = false.
```

This supersedes only the `TraceContactResidual4979_MTS` open status. It does
not alter the already matched transverse-traceless kernel and does not turn a
free matter-loop control into a parent MTS result.

## 1. Covariant four-dimensional regulator

For the densitized inverse metric

```text
H^(mu nu)=sqrt(g) g^(mu nu),
```

the massive scalar operator is

```text
A_m[H]=-partial_mu H^(mu nu) partial_nu + m^2 sqrt(g[H]).
```

Unlike the massless operator, its determinant-volume term has exact first,
pair, and triple metric contacts. For polarizations `h_i`,

```text
rho_i       =(1/2) tr(h_i),
rho_ij      =(1/4)tr(h_i)tr(h_j)-(1/2)tr(h_i h_j),
rho_123     =(1/2)tr(h1 h2 h3+h1 h3 h2)
              -(1/4)sum_cyclic tr(h_i h_j)tr(h_k)
              +(1/8)tr(h1)tr(h2)tr(h3).
```

These contacts are not optional additions. They are the metric derivatives
of the same parent mass term and supply the trace/longitudinal Ward contact
that is invisible on transverse-traceless external fields.

The regulator multiplet is

```text
c_j        =(1,-3,3,-1),
m_j^2/M^2  =(0,1,2,3).
```

It obeys

```text
sum_j c_j = sum_j c_j m_j^2 = sum_j c_j m_j^4 = 0
```

exactly. Thus quartic, quadratic, and logarithmic power-divergent moments
cancel before a finite scheme is selected.

## 2. Analytic `q^4` extraction

Let all external momenta scale as `q_i -> lambda q_i` and set
`x=lambda^2`. For a massive triangle,

```text
D=m^2+x Delta,
C_i=m^2 rho_i+x c_i,
b_i -> sqrt(x) b_i.
```

The Gaussian numerator moments become finite polynomials

```text
E0(x): degree 3,
E1(x): degree 2,
E2(x): degree 1,
E3(x): degree 0.
```

Expanding `D^-1`, `log(mu^2/D)`, `D`, and `D^2` only through `x^2`
therefore extracts the complete `q^4` coefficient before summing large
`q^0` and `q^2` pieces. Per cyclic orientation the finite triangle is

```text
(4pi)^-2 int_simplex [
 E0/(2D)
 +E1/4 log(mu^2/D)
 +E2 D/8(-log(mu^2/D)-1)
 +E3 D^2/32(log(mu^2/D)+3/2)].
```

For a pair seagull with remaining source `i` and pair `jk`,

```text
(4pi)^-2 m^2 rho_jk int_0^1 dt [
 -(1/2) C_i log(mu^2/D)
 +(1/4)tr(h_i)D(log(mu^2/D)+1)].
```

The triple volume contact is momentum independent and has zero `q^4`
coefficient. The analytic extraction was checked against the unexpanded
massive determinant on G05 and G06 at maximum relative residual
`8.542529657987046e-09`; the direct polynomial-fit residual is
`1.6683910305336686e-14`.

## 3. Two-point scheme fixed before three points

The strictly four-dimensional massless two-point moments are analytic. With
`s=t(1-t)`,

```text
int_0^1 s^2 dt                         =1/30,
int_0^1 s^2 log(s) dt                  =-47/900,
int_0^1 s(1-2t)^2 log(s) dt            =-31/450.
```

Forty-eight random two-point controls then project the complete PV sum onto

```text
Ricci log(q^2/mu^2) Ricci,
Ricci^2,
R log(q^2/mu^2) R,
R^2.
```

Across `M=(3,5,10,20,40,80)`, the worst covariant fit residual is
`1.199081222067133e-14`; the universal `1/60` and `1/120` logarithmic
coefficients agree to `2.0608514894604042e-14`.

The bare PV local coefficients collapse to the exact rule

```text
C_Ricci^PV(M)=-23/450-log(3M^2/8)/60,
C_R^PV(M)    =-1/1800-log(3M^2/8)/120.
```

Consequently the counterterm that maps the covariant PV determinant to the
checkpoint-4979 common scheme is fixed uniquely by two-point data:

```text
Delta W_ct=[1/(2(4pi)^2)] log(3M^2/8)
           int sqrt(g)[Ricci^2/60+R^2/120].
```

The fitted local slopes are `-1/30` and `-1/60` with maximum relative
residual `3.747002708109889e-15`. No three-point target enters this rule.

## 4. Withheld traceful predictions

For every geometry the prediction is

```text
W_ren,123(M)=W_massless,triangle,123
             +sum_(j=1)^3 c_j[W_massive triangle+pair]_(m_j),123
             +Delta W_ct,123(M).
```

The target remains the independently acquired source convention

```text
W_target,123=UV_shell,123-(-W_source,123).
```

G03 and G04 are the original withheld traceful controls. G05 and G06 were
generated from the checkpoint-4978 source action only after the regulator
and two-point scheme rule were fixed. Their `N=4` and `N=6` source responses
agree to `1.571374938064053e-15`.

At representative `M=20`:

| geometry | class | renormalized PV `W` | fixed source target | relative residual |
|---|---|---:|---:|---:|
| G03 | old withheld | `+4.018630749117548e-05` | `+4.018630738550688e-05` | `2.6294677670849094e-09` |
| G04 | old withheld | `-1.2187460875883881e-04` | `-1.21874608583716e-04` | `1.4369097615636668e-09` |
| G05 | fresh withheld | `-1.5315703618835124e-05` | `-1.5315703541432477e-05` | `5.053809379484762e-09` |
| G06 | fresh withheld | `+1.5522099653333618e-05` | `+1.5522099446171368e-05` | `1.334627751534948e-08` |

Across all six regulator masses, the maximum absolute discrepancy is
`2.07162845905495e-13` and the maximum relative discrepancy is
`1.33463159322647e-08`. The maximum renormalized regulator-mass spread is
`1.20489417624365e-13`; the massive low/high simplex difference is
`3.4329033736276404e-14`.

The old 4979 product-continuation mismatch was therefore not evidence that
the nonlocal scalar response failed. It was evidence that the chosen
traceful continuation omitted the covariant regulator contacts. The PV
construction supplies those contacts from the parent massive action and
then removes its local scale dependence with the already fixed two-point
scheme.

## 5. Scope and next target

The runner passes `16/16` gates and the independent validator passes
`60/60`. This promotes

```text
valid_for_covariant_PV_q4_contact_derivation=true,
valid_for_complete_free_scalar_traceful_common_scheme_finite_determinant_match=true.
```

It retains

```text
valid_for_interacting_motion_graviton_ghost_kernel=false,
valid_for_full_MTS_claim=false.
```

The next useful calculation is not another scalar continuation. It is to
transfer this exact regulator/contact architecture to the parent
motion--graviton--ghost Hessian: derive each massive regulator operator,
its measure/coframe contacts, its signed supertrace coefficients, and its
two-point common-scheme map before evaluating the parent three-point kernel.

No GitHub action.
