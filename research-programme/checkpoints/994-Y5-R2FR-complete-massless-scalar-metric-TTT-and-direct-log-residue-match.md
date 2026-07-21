# 4978 - Complete massless scalar metric TTT and direct log-residue match

Marker: `PPC4161_COMPLETE_MASSLESS_SCALAR_METRIC_TTT_4978`  
Runner marker: `MTS_4978_SCALAR_MASSLESS_METRIC_TTT_ASSEMBLER`

## Decision

The free minimal-scalar branch now has a complete source-side one-loop third
metric response about flat Euclidean space. Checkpoint 4978 varies the exact
quadratic nonlocal action, including the metric dependence of
`log(-Box/mu^2)`, and adds all eighteen surviving cubic-curvature form
factors from checkpoint 4977. Nothing in the assembled response is fitted.

Two independent off-shell geometries give

```text
             quadratic          cubic             total braces       -W density
G03       +1.8297813564e-3  +1.4348243658e-3  +3.2646057223e-3  +1.0336678622e-5
G04       -2.9175618347e-2  -3.6234750071e-3  -3.2799093354e-2  -1.0385134253e-4.
```

The `N=6` and `N=8` calculations agree to a worst relative residual of
`7.347384370016319e-15`. A cyclic relabeling of all three external sources
leaves the response invariant to `4.740247980655725e-16`.

The scheme-independent logarithmic residue is independently recovered from
the direct scalar determinant. The worst source-versus-determinant residual
on G03 and G04 is `4.4597437902582106e-11`.

This closes the source-side free-scalar massless metric `TTT` kernel and its
direct logarithmic residue. It does not yet provide a separately
renormalized direct-determinant comparison of the scheme-dependent finite
constant, nor any interacting-motion, graviton, ghost, exact compact-GR, or
full-MTS result.

## 1. Quadratic nonlocal third response

Checkpoint 4977 fixed

```text
-W_scalar^(2)=1/[2(4pi)^2] integral sqrt(g) [
 Ricci_mn (-1/60 log(-Box/mu^2)+4/225) Ricci^mn
 +R (-1/120 log(-Box/mu^2)-29/1800) R].
```

At third metric order, the nonlocal part requires only the first Frechet
derivative of `log A`, with `A=-Box`. In the flat Fourier eigenbasis,

```text
[D log(A0)[delta A]]_(p q)
 =log^[1](p^2,q^2) (delta A)_(p q),

log^[1](x,y)=(log x-log y)/(x-y),
log^[1](x,x)=1/x.
```

The implementation includes

```text
delta sqrt(g),
delta R and delta^2 R,
delta Ricci and delta^2 Ricci,
inverse-metric contractions,
delta(-Box) on scalars,
delta(-Box) on covariant rank-two tensors,
connection terms in the Ricci rough Laplacian.
```

Freezing the box is not an admissible approximation. On G03, the omitted
operator-variation pieces would be

```text
Delta[R log(-Box) R]             = -0.17169907109500238,
Delta[Ricci log(-Box) Ricci]     = -0.2308054155498826.
```

On G04 the Ricci correction is `+0.49990511548917427`. These are larger than
the final weighted response because substantial source-fixed cancellations
occur.

## 2. Cubic-curvature response

For every one of the eighteen surviving indices

```text
1,4,5,6,9,10,11,15,16,17,22,23,24,25,26,27,28,29,
```

the calculation constructs the linearized scalar and Ricci curvatures,
their first and second derivatives where required, evaluates the
source-symmetrized finite-momentum `Gamma_i`, and sums all six assignments of
the three external sources to labels `1,2,3`.

Because an explicit curvature starts at first metric order, quartic and
higher curvature terms cannot contribute to a third flat-background metric
response. The quadratic and cubic sectors therefore exhaust the source
effective action at this response order.

The full source-side mixed response is

```text
(-W)_123=1/[2(4pi)^2] [
 Q_Ricci,123(mu)+Q_R,123(mu)+sum_i C_i,123].
```

Both the quadratic and cubic pieces are numerically nonzero on both test
geometries; neither can be discarded.

## 3. Exact mu identity

Define the local anomaly response inside the braces by

```text
A_local,123=-(1/60)[integral sqrt(g) Ricci^2]_123
             -(1/120)[integral sqrt(g) R^2]_123.
```

Directly rebuilding the logarithmic operators at `2 mu` gives

```text
Q_123(2mu)-Q_123(mu)=-2 log(2) A_local,123.
```

The maximum residual across both geometries and both grids is
`8.57113232561267e-16`. Zero-mode leakage is below
`1.3212924122348244e-16`, and the maximum imaginary residue is
`1.3354713907747593e-16`.

## 4. Independent direct-determinant logarithmic residue

The direct continuum scalar determinant supplies an independent comparison.
At radial loop momentum `Lambda`, its mixed `q^4` shell is

```text
D_123(Lambda)=1/4 Re[e^(i sum phi)] Lambda^4
 integral_(S3) dOmega W_123,4(Lambda n)/(2pi)^4.
```

The factor `1/4` converts the complex plane-wave response to the real cosine
normalization used by the geometric engine. Power-suppressed terms are
removed by a quadratic extrapolation in `1/Lambda^2`. The source predicts

```text
lim_(Lambda->infinity) D_123(Lambda)
 =2/[2(4pi)^2] A_local,123.
```

The two comparisons are

```text
G03 direct      5.0522986005256834e-5
G03 source      5.0522986007510030e-5
relative        4.4597437902582106e-11

G04 direct     -2.2572595111185363e-4
G04 source     -2.2572595111696372e-4
relative        2.2638463850198210e-11.
```

This is not a fitted normalization: the direct determinant uses the
checkpoint-4912 loop vertices, while the source prediction uses the
covariant quadratic action and the independently calculated local geometric
responses.

## 5. What is and is not closed

```text
free-scalar local q6 and q8/a8                 = exact;
massless scalar 18 cubic form factors          = source-complete;
quadratic nonlocal metric third variation      = derived;
delta log(-Box) scalar and tensor terms         = retained;
complete source-side free-scalar metric TTT     = derived;
N6/N8 and source-permutation checks             = pass;
direct determinant logarithmic residue          = matched;
scheme-dependent finite determinant comparator  = open;
interacting motion/graviton/ghost kernels        = open;
exact all-operator compact GR                    = false;
full MTS                                         = false.
```

## 6. Next calculation

Checkpoint 4979 should construct an independent finite determinant
comparator in the same renormalization convention. The clean route is to
subtract the analytically derived ultraviolet `q^0`, `q^2`, and `q^4`
asymptotic shells from the direct radial integrand, integrate the convergent
remainder, and restore the same `mu`-dependent local counterterms used by the
Barvinsky--Vilkovisky action. The result must reproduce both the G03 and G04
finite responses without fitting a geometry-dependent constant.

No GitHub action or full-MTS claim is authorized.

## Outputs

- `post-checkpoint-work/scripts/Y5_R2FR_4978_scalar_massless_metric_TTT_assembler.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4978_scalar_massless_metric_TTT_validation.py`
- `post-checkpoint-work/source-intake/functional_rg/4978/scalar_TTT_quadratic_log_response.csv`
- `post-checkpoint-work/source-intake/functional_rg/4978/scalar_TTT_cubic_channel_response.csv`
- `post-checkpoint-work/source-intake/functional_rg/4978/scalar_TTT_assembled_response.csv`
- `post-checkpoint-work/source-intake/functional_rg/4978/scalar_TTT_scale_mu_Ward_identity.csv`
- `post-checkpoint-work/source-intake/functional_rg/4978/scalar_TTT_direct_determinant_UV_log_residue.csv`
- `post-checkpoint-work/source-intake/functional_rg/4978/scalar_TTT_assembly_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4978/scalar_TTT_assembly_results.json`

The runner passes `14/14` internal gates. The independent validator passes
`51/51`; validation CSV SHA256 is
`f27e596afa07308c6a09db1a58fc9d6ed40d2497a599a3bebd06af2d31a445b0`.
