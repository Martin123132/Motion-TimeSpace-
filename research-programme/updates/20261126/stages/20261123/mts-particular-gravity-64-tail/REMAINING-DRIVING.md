> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# What can be bounded beyond 64 conformal Mpc without evolving another matter interval?

Scope: only the not-yet-included curvature-zero particular gravitational source, in this retained finite-angular photon/baryon system and for its longest mode. The launch and the regular drive have already been propagated. The tail is the extra response that has zero initial state when this additional source is switched on. Unknown particular forcing after 64 has **not** been set equal to zero in the bound. The precomputed homogeneous scattering medium extends to the end of the window.

## 1. A non-amplifying energy norm for photon transport

In conformal time the retained state satisfies
$$
z'=(kA+\kappa D+(\kappa/R)C+\mathcal H L)z+f,\qquad
f=(4\Phi',4k\Psi/3,4k\Psi/3,0,\ldots).
$$
In order, the first three slots are photon energy, baryon velocity variable and photon current. Here R is the baryon loading and opacity κ is nonnegative. Matrices are exactly those of the saved transport operator (not bundled here).

Choose the diagonal energy matrix W with weights 1, 3R and 3 in these first slots, 5 and 30 for the two quadrupoles. Continue each angular chain by w_next = −w_prev A_prev,next/A_next,prev. All weights are positive and WA is skew-symmetric. Collision recoil and drag give the pair quadratic form −3κ|b−j|²; the quadrupole block in the weighted form is κ times [−4.5,3;3,−12], negative definite. Higher collision moments damp. Expansion plus the changing baryon weight contributes 3(R′−2ℋR)|b|² to the derivative of squared norm. We checked 2ℋR−R′ > 0 throughout both saved cubic media, not just at the sample times: cubic Bernstein control values bracket ℋ and R, and the differentiated controls bracket R′. Thus the homogeneous propagator is contractive **between its time-dependent energy norms**. The two-component observable (energy,current) has ordinary norm at most the state norm.

Duhamel's formula and the triangle inequality give the following branch bound at a readout time T:
$$
\lVert y_{\rm tail}(T)\rVert_2\leq\int_{64}^{T} S(\eta)\,d\eta,\qquad
S=4\sqrt{|\Phi'|^2+\tfrac{k^2}{3}(1+R)|\Psi|^2}.
$$
Use zero if T < 64. This does not require a damping ansatz or a chosen phase. Each branch has its own medium. For the difference, adding the two branch bounds is conservative; applying a single propagator to the difference of the metric sources would generally be wrong.

For a constant source cap M in both branches, the continuous window gain in each branch is the visibility-weighted RMS of (η−64)₊, and the peak gain is its value at the common peak scale. The saved scoring code interpolates photon *readouts* on the scale-factor grid. To also cover this interpolation, form its not-a-knot B-spline collocation matrix B and the comparison matrix K = diag(B) − |offdiag(B)|. We check K has positive diagonal, nonpositive off-diagonals and a positive witness with K v > 0, so its inverse is nonnegative. A verified supersolution K u ≥ nodal envelope bounds the vector-valued spline coefficients in magnitude. Evaluating the nonnegative spline basis on u gives conservative scored gains, including any interpolation overshoot. Floating calculations use slack; this is an analytic inequality for the retained continuous operator and its sampled readout, not a formal roundoff proof for the time solver.

**Backtest:** for each of the six measured intervals and both branches, bracket the actual cubics for Φ′ and Ψ by the maxima of the magnitudes of their Bernstein controls, sum the segment bounds on ∫S, and compare with the largest saved isolated photon readout. See [12 backtests](evidence-001.zip) (archive member: `tail-bound-backtest.csv`) and [medium/gain checks](evidence-001.zip) (archive member: `tail-propagation-gains.csv`). A passing inequality need not be tight.

## 2. A sharper bound for the MTS-minus-baseline difference

Work at equal scale factor a, β_j = dη_j/da, C_j = β_j(kA+κ_j D+κ_j C/R_j+ℋ_j L), and s_j = β_j f_j times its **own** η_j ≥ 64 switch. Start both extra responses at zero at the earlier switch. Then
$$
(\delta z)_{,a}=C_h\delta z+(C_h-C_c)z_c+(s_h-s_c).
$$
Let Dₛ = ∫||s_h−s_c||_{W_h} da and I_c = ∫||s_c||_{W_c} da, out to the last readout. Contraction gives ||z_c|| ≤ I_c and consequently
$$
\sup_a\lVert\delta y\rVert_2\le D_s+\epsilon_{\rm med}I_c,\qquad
\epsilon_{\rm med}=\int \lVert C_h-C_c\rVert_{W_c\to W_h}\,da
\quad\text{or any upper bound on this integral.}
$$
This retains the possibility of common-mode cancellation **without assuming it**. For the saved scoring spline use its constant-envelope gain to multiply the right-hand side. In [the medium calculation](evidence-001.zip) (archive member: `paired_tail64.py`), both background clocks are cubic on the same scale-factor cells. Compose the native rate cubics with those clocks in normalized cell coordinates. Bound differences of the resulting polynomials by their Bernstein controls; for the recoil ratio, bound the cross-multiplied numerator and divide by positive loading lower bounds. Sum the separate operator norms (bounded by the square root of the 1- and infinity-norm product after weighting). The entire cell containing the first switch is included, and coefficient arithmetic has a numerical safety margin. [Medium-only coefficients](evidence-001.zip) (archive member: `paired-tail-medium-mismatch.csv`) are independent of the late matter solution. **They multiply a source integral; they are not the size of the missing signal.**

For the post-64 medium, ε_med ≤ **0.0551** in both retained angular controls (128 and 192). For an end-to-end check, applied the same derivation to the already completed 57.6–64.0 source, propagated through the saved medium. We bounded the integral of the *paired* forcing directly: use local midpoint differences enlarged by derivative bounds on the source cubics and clocks, and include single-branch switch cells separately. The relevant medium integral now starts at 57.6 and has upper bound **0.1767**. With 128 subdivisions per intersecting scale-factor cell, the paired bound on the maximum nodal difference is **2.27e-12** (rounded up), versus **9.39e-12** from adding the separate bounds. The measured maximum is **9.53e-13**. This is a retrospective test on one known input, not a bound of the same size for the unknown tail. [Backtest and refinement](evidence-001.zip) (archive member: `paired-tail-backtest.csv`).

## 3. An alternative that needs no later potential derivatives

For an exact metric set u = z − 4[Φ(η)−Φ(64)] e₀ on the active tail. Its launch is still zero. Its monopole drive vanishes; the baryon and photon acceleration slots now see 4kΨ/3 and 4k[Ψ+Φ−Φ(64)]/3 respectively. Restoring the observable's monopole at the readout gives

$$
\|y_{\rm tail}(T)\|_2\le 4|\Delta\Phi(T)|+
\frac{4k}{\sqrt{3}}\int_{64}^T
\sqrt{R|\Psi|^2+|\Psi+\Delta\Phi|^2}\,d\eta .
$$

Thus bounds on the *amplitudes* of the lapse and the potential excursion are sufficient even for rapid oscillations; this route does not require guessing a frequency or bounding Φ′. For the six retrospective intervals, the bound also includes 4∫|Φ′ from the constraint minus the derivative of the stored Φ spline|. This separates the numerical derivative defect from the continuum identity. Cubic Bernstein coefficients bound both the lapse-plus-excursion and the derivative defect. See [amplitude-only backtests](evidence-001.zip) (archive member: `amplitude-tail-backtest.csv`) and [equal amplitude caps](evidence-001.zip) (archive member: `amplitude-tail-budgets.csv`). These are sufficient caps, not measured late potentials.

## 4. What the matter equations must supply

On the retained constraint branch, include the finite-bin contributions in total energy E, longitudinal momentum J and shear Π, in code conventions. Put Aₑ = U−E/2, Aₛ = Π−Q, F = −J/(2k²), and d = k²+Jac/2. Then
$$
\Phi=(A_e+3\mathcal H F)/d,\quad
\Psi=\Phi+A_s/k^2,\quad \Phi'=-F-\mathcal H\Psi+F_q.
$$
Thus bounds on **four combinations**, |Aₑ|, |J|, |Aₛ|, |Fq|, with a positive lower bound on d and a known background, suffice: bound |Φ| by (|Aₑ|+3ℋ|F|)/d, then |Ψ| by that plus |Aₛ|/k², and |Φ′| by |F|+ℋ|Ψ|+|Fq|. Insert into S. A sharper route keeps paired source differences rather than first bounding the branches separately. [Endpoint reconstruction](evidence-001.zip) (archive member: `tail-constraint-endpoint.csv`) tests these expressions directly from the saved fluids, scalar states, quadratic inputs and returned 77-bin stresses at 64, separately from reading stored Φ, Ψ and Φ′. See the retained constraint equations (not bundled here) and finite-stress injection (not bundled here).

**Why a number for the physical tail does not follow from the endpoint alone.** In the photon problem one can add a smooth compactly supported lapse pulse strictly after 64, leaving every saved metric value and endpoint derivative unchanged. A pulse just before a readout couples directly to its current (the retarded propagator approaches the identity). Scaling the pulse scales the response. This is a counterexample to an endpoint-only *photon* bound, not permission to add arbitrary pulses to the full MTS equations. The coupled model must control the future forcing. The reviewed source coverage (not bundled here) distinguishes the full-time same-k **regular** solution from the 77-bin **particular** source and from later runs with different preparations. The small native interpolation padding at 64 is not a later coupled solution or a full-window envelope.

**Decision rule.** [Source budgets](evidence-001.zip) (archive member: `tail-source-budgets.csv`) give sufficient uniform caps and a sufficient budget for Dₛ+ε_med I_c for a tail smaller than 0.5% of each retained signed readout (RMS or peak, not 0.5 percentage points of launch). [The verdict](evidence-001.zip) (archive member: `tail-verdict.json`) separates these conditional tests from a physical certificate. Large instantaneous values can rule out that particular uniform-cap test; they do not prove a large integrated tail. The next useful object is a full-range *inequality* for those paired constraint sources, not another inference from the six observed signs.
