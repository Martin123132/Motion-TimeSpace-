# 5257 — Lower-point factorized active numerator and orientation sign

## Purpose

Checkpoint 5256 derived the active MC12/MC04 denominator exactly, but the
continuous residue envelope still required a non-singular construction of the
numerator. This checkpoint removes the direct five-point pole fit from that
construction. It also derives the local residue orientation from the parent
contour ownership rather than selecting the sign by comparison with the fitted
answer.

This is a private derivation checkpoint. It does not certify the full outer
integral, the numeric UV coefficient, local GR, or full MTS.

## Exact denominator input

For each supported active row, checkpoint 5256 supplies the exact quadratic
branch \(z_\epsilon(x)\), the relative root \(w_*\), the global root \(u_*\),
and the collision Jacobian \(J_{\rm coll}\). The eight supported rows are:

- MC12 at `D01A` and `D01B`, for \(\epsilon=0.02,0.04\);
- MC04 at the prior active endpoint `C06A` and at `D06B`, for
  \(\epsilon=0.02,0.04\).

`D06A` is correctly absent because its generation-two midpoint has no active
causal residue.

The denominator cross-check passes all source, root, discriminant, collision,
and reflection gates. Its largest exact-to-fitted channel-derivative relative
error is \(4.1259704\times10^{-5}\), while the minimum quadratic discriminant
magnitude is \(2.8369840\times10^{-2}\). Thus these sampled branches are simple
and separated.

## Lower-point factorization

Let \(D=(p_0+p_i)^2\) be the active left hard channel, with \(i=2\) for MC12
and \(i=1\) for MC04. Tree factorization gives

\[
\lim_{D\to0} D\,K^{c}_{5,L}
=
M^{c}_{3,L}(p_0,p_i,-P)\,
K^{c;i}_{4,L}(P,p_j,p_k,p_4),
\qquad P=p_0+p_i .
\]

For the scalar-graviton parent gauge residue used here,

\[
A_3=\sqrt 2\,p_0\!\cdot\!\epsilon_i,
\qquad
M_3=2(p_0\!\cdot\!\epsilon_i)^2 .
\]

Therefore the direct double-copy numerator can be evaluated entirely with
finite lower-point objects:

\[
[D H_{\rm hhh}]_*
=
\frac{1}{6}\sum_{a,c}
M^{c,a}_{3,L}\,
K^{c,a;i}_{4,L}\,
K^{1-c,a}_{5,R}.
\]

No product containing the active \(1/D\) pole is evaluated numerically.

## Finite Cauchy coefficient

After including the finite soft weight and multiplier, define

\[
\widetilde C_\epsilon(x)
=
\frac{1}{2\pi i}\oint
\frac{(u-u_*)^2\,F_\epsilon(u,x)}{u-u_*}\,du .
\]

The runner evaluates this coefficient on two nested circles. The maximum
relative radius-change residual over all eight rows is

\[
4.2309033\times10^{-12}.
\]

This demonstrates that the factorized object is finite and isolates the
intended double-pole coefficient at the sampled points.

## Orientation sign from the parent contour

The local double-residue identity is

\[
N_\epsilon(x)
=
\sigma_{\rm loc}\,
\Delta w\,
\frac{\widetilde C_\epsilon(x)}
{w_*u_*J_{\rm coll}},
\]

where \(\Delta w\) is the transported winding difference and
\(\sigma_{\rm loc}=+1\) when the first member of the representative collision
pair is owned by the chamber, otherwise \(-1\).

The runner reconstructs each parent problem, rebuilds its current component
topology, and calls the same chamber-ownership map used by the parent contour
calculation. For every supported row:

- the representative pair is `hard:minus_u | direct:g3:plus_u`;
- exactly one member is owned;
- the owned member is `direct:g3:plus_u`;
- hence \(\sigma_{\rm loc}=-1\).

The sign is consequently derived from the parent contour. It is not selected
by minimizing the discrepancy with the old fitted numerator.

## Numerical cross-check

With 32 Cauchy nodes:

- all 8 rows pass;
- maximum oriented numerator relative error:
  \(1.3064347\times10^{-7}\);
- maximum coefficient radius instability:
  \(4.2309033\times10^{-12}\);
- maximum exact global-collision residual:
  \(4.4408921\times10^{-16}\);
- all orientation ownership tests are unique and source reconstructed.

The parent-topology representative root is evaluated at the real fit centre,
whereas the exact quadratic pole carries the complex regulator. Their maximum
relative displacement is \(3.9791438\times10^{-3}\); the ownership is discrete,
unique, and unchanged throughout this separated neighbourhood.

## Result

The sampled active numerator no longer depends on a singular outer polynomial
fit. It is reproduced by a finite lower-point factorization with a
parent-derived contour orientation.

This closes two real gaps:

1. the active denominator is analytic and simple;
2. the active numerator and its sign have a finite, lower-point construction.

It does **not** yet close the continuous chamber bound.

## Claim boundary

The following remain false:

- `outward_rounded_numerator_enclosure_complete`;
- `continuous_residue_envelope_complete`;
- `valid_for_numeric_UV_claim`;
- `valid_for_local_GR_claim`;
- `valid_for_full_MTS_claim`.

The calculation is a high-accuracy smoke validation, not an interval proof.

## Next exact target

Construct an adaptive chamber enclosure for

\[
R_\epsilon(x)=\frac{N_\epsilon(x)}{D'_\epsilon(x)}
\]

using:

1. the exact quadratic denominator branch and discriminant separation;
2. the finite lower-point Cauchy numerator;
3. the derived fixed orientation \(\sigma_{\rm loc}=-1\);
4. explicit subdivision error bounds in the outer coordinate.

The next checkpoint must bound the function between samples. It must not
rename a dense scan as a supremum proof.

## Machine-readable evidence

- `source-intake/functional_rg/5256/exact_active_denominator_crosscheck.csv`
- `source-intake/functional_rg/5256/exact_active_denominator_validation.csv`
- `source-intake/functional_rg/5256/exact_active_denominator_result.json`
- `source-intake/functional_rg/5257/factorized_active_numerator_smoke.csv`
- `source-intake/functional_rg/5257/factorized_active_numerator_validation.csv`
- `source-intake/functional_rg/5257/factorized_active_numerator_result.json`
- `scripts/Y5_R2FR_5256_exact_active_denominator_crosscheck.py`
- `scripts/Y5_R2FR_5257_lower_point_factorized_active_numerator_smoke.py`
