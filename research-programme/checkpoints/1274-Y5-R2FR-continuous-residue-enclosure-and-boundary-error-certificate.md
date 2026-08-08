# 5258 — Continuous residue enclosure and boundary-error certificate

## Purpose

Checkpoint 5257 supplied a finite lower-point construction of the active
numerator and derived its contour orientation. The missing step was a
continuous, outward-rounded bound over every generation-two transition
bracket. This checkpoint constructs that bound.

This is a private mathematical certificate for the boundary-location error
only. It does not certify the completed outer integral, the numeric UV
coefficient, local GR, or full MTS.

## Exact moving branch

For each active MC12 or MC04 row, the pole \(z_\epsilon(x)\) remains the
selected root of the exact checkpoint-5256 quadratic

\[
Q_\epsilon(z,x)=a_\epsilon z^2+b_\epsilon(x)z+c_\epsilon(x)=0.
\]

The raw interval quadratic formula is dependency-heavy on these steep
branches. The runner therefore starts from its natural interval enclosure and
contracts it with the exact implicit derivative

\[
\frac{dz}{dx}
=-\frac{b_\epsilon'(x)z+c_\epsilon'(x)}
{2a_\epsilon z+b_\epsilon(x)}.
\]

Every retained box has a nonzero quadratic discriminant and a nonzero channel
derivative. Across the final run,

\[
\inf |\Delta_Q|=2.8324128239\times10^{-2},
\qquad
\inf |D'_\epsilon|=1.9583087455\times10^{-1}.
\]

## Correlation-preserving event geometry

The complex azimuthal rotation is evaluated in light-cone transverse
coordinates,

\[
p_+=p_x+i p_y,\qquad p_-=p_x-i p_y,
\]

so that

\[
p_+\mapsto u\,p_+,\qquad p_-\mapsto u^{-1}p_-.
\]

The event builder carries \(p_\pm\) directly into the rotation. It does not
construct \(p_x,p_y\), lose their common dependence, and then reconstruct
\(p_\pm\). This reduced the deepest required MC04 refinement from ten binary
levels to five.

Complex null momenta use a four-chart spinor atlas. In addition to the
\(E\pm p_z\) charts, the runner can pivot on \(p_x\mp i p_y\). This removes a
coordinate singularity that occurs when both diagonal bispinor entries vanish
while an off-diagonal entry remains nonzero.

## Exact double-pole regularization

Let \(u_*(x)\) be the moving global collision root and
\(d=u-u_*(x)\). The directly bounded function is

\[
G_\epsilon(x,d)=d^2 F_\epsilon(x,u_*(x)+d).
\]

The parent topology and exact collision equation identify three coincident
root labels:

\[
\begin{aligned}
\text{direct:}g_{\rm hard}:\mathrm{minus\_u}&=u_*,\\
\text{direct:}g_3:\mathrm{plus\_u}&=u_*,\\
\text{subtraction:soft}:\mathrm{plus\_u}&=u_*.
\end{aligned}
\]

The \(g_3\) and soft identities follow directly from

\[
u_*=\xi\,\frac{1+z}{\sqrt{1-z^2}},
\]

and the hard identity is the checkpoint-5256 collision equation. The two
active spinor factors are cancelled algebraically against \(d^2\) before
interval evaluation. Common MHV numerator and denominator factors are also
cancelled before division.

This rewrite is not a fitted replacement. At a nonzero complex displacement,
the regularized expression is compared with \(d^2\) times the original parent
factorized amplitude for all eight active rows. The maximum relative
difference is

\[
5.8973536438\times10^{-11}.
\]

## Interval root catalogue

For a lightlike momentum, define

\[
\xi=\sqrt{\frac{1-t}{1+t}},\qquad
h=\frac{p_+}{E+p_z},\qquad
\bar h=\frac{p_-}{E+p_z}.
\]

The complete four-root catalogue used by the parent construction is

\[
u_+=\frac{\xi}{h},\qquad
v_+=\frac{\bar h}{\xi},\qquad
u_-=-\frac{1}{\xi h},\qquad
v_-=-\xi\bar h.
\]

The runner encloses these roots for \(g_1,g_2,g_3\), the soft direction, and
the decay direction: twenty roots per interval box. It removes only the three
parent-derived active identities above. Every other root must remain a
strictly positive interval distance from \(u_*\).

The final 976-box run proves

\[
\inf_{x,\;r\notin\mathcal A}|r(x)-u_*(x)|
=8.9946990242\times10^{-6}>0.
\]

If \(\delta\) is this lower separation in a box, the certified catalogue
radius is \(\rho=0.02\delta\), the outer Cauchy radius is
\(R=0.2\rho\), and the sampling radius is \(r=R/2\). Thus the contour remains
strictly inside the non-active-root-free disk.

## Cauchy enclosure

For \(N\) shifted trapezoidal nodes on the inner circle, the constant
coefficient is enclosed by the interval node average plus the analytic alias
tail

\[
\left|C-C_N\right|
\le
M_R\,
\frac{(r/R)^N}{1-(r/R)^N},
\]

where \(M_R\) is the interval supremum on an adaptively split outer circle.
Both the outer coordinate and difficult phase arcs are bisected until every
denominator is separated.

The oriented numerator and residue are then

\[
N_\epsilon(x)
=\sigma_{\rm loc}\Delta w\,
\frac{\widetilde C_\epsilon(x)}
{w_*(x)u_*(x)J_{\rm coll}(x)},
\qquad
R_\epsilon(x)=\frac{N_\epsilon(x)}{D'_\epsilon(x)}.
\]

## Certified transition bounds

The physical half-residue inequality is

\[
\sup|\Delta f|
\le 0.016\left(2\sup|R_{20}|+\sup|R_{40}|\right),
\]

and the bracket-location contribution obeys

\[
|\delta I_{\rm boundary}|
\le \frac14\,\Delta x\,\sup|\Delta f|.
\]

The coarse base partition has 16 boxes per transition and regulator. Adaptive
refinement expands the full run to 976 certified boxes.

| transition | adaptive boxes | max depth | \(\sup|R_{20}|\) | \(\sup|R_{40}|\) | \(\sup|\Delta f|\) | boundary error upper |
|---|---:|---:|---:|---:|---:|---:|
| I01_T00 | 32 | 0 | 9,657,995.41 | 9,670,444.29 | 463,782.96 | 1,563.01 |
| I01_T01 | 280 | 4 | 7,068,799.95 | 7,088,409.91 | 339,616.16 | 1,144.55 |
| I06_T00 | 632 | 5 | 28,421,262.37 | 28,585,847.77 | 1,366,853.96 | 4,606.49 |
| I06_T01 | 32 | 0 | 9,657,998.90 | 9,670,451.40 | 463,783.19 | 1,563.01 |

The D01A/D06B reflected branches agree at the sub-part-per-million level in
the outward-rounded envelope.

## Result

The previous statement

`continuous_residue_envelope_complete=false`

is replaced by

`continuous_residue_envelope_complete=true`.

This is a real derivational advance: the continuous chamber supremum is no
longer inferred from dense samples. The exact denominator, factorized
numerator, contour orientation, active-pole cancellation, non-active-root
separation, and Cauchy tail are all represented in the certificate.

## Utility boundary

The certificate is deliberately conservative. Its current boundary-location
errors are much larger than the equal per-boundary budget
\(0.6052369605\). Therefore it closes the existence/proof gate but not the
practical stopping gate for the outer calculation.

The following remain false:

- `outer_boundary_budget_met`;
- `valid_for_numeric_UV_claim`;
- `valid_for_local_GR_claim`;
- `valid_for_full_MTS_claim`.

No local-GR conclusion follows merely from proving that this residue envelope
is finite.

## Next exact target

Run a utility/handoff gate against the checkpoint-5256 outer error budget.
Quantify the certified inflation over the sampled envelope and decide between:

1. tighter centered/Taylor interval forms for the regularized amplitude;
2. targeted extra topology bisections;
3. a hybrid in which only the high-inflation chambers are re-enclosed.

The GR-linked handoff remains blocked until the certified boundary budget is
small enough to preserve the outer coefficient.

## Machine-readable evidence

- `source-intake/functional_rg/5258/interval_residue_boxes.csv`
- `source-intake/functional_rg/5258/interval_transition_envelopes.csv`
- `source-intake/functional_rg/5258/regularized_factorization_crosscheck.csv`
- `source-intake/functional_rg/5258/interval_residue_validation.csv`
- `source-intake/functional_rg/5258/interval_residue_result.json`
- `scripts/Y5_R2FR_5258_interval_residue_enclosure_pilot.py`
