# A localized Gram reaction and a derived force-consistency mesh law

Private continuation of `DERIVATION-20260919-bulk-Gram-source-jump-scaling-and-evolution.md`. No action term, physical coupling, source profile, or old result is replaced. This stage does not establish the full GR limit.

## What has actually moved forward

The previous global energy bound could not explain a force of order 1e-8: its bound was about 0.014. Keeping every row, the new bound is 8.24e-8. The live force contribution is concentrated in seven source-straddling rows. Their response has an exact scalar reaction decomposition, and its amplification is explained by an independently derived P2 mass-projection trace law.

More importantly, there is now a FORCE result rather than just an energy scaling: for a precisely specified constant-weight, source-local piecewise-quadratic fixture, the extra projected Gram force tends to zero when h -> 0 and h^2/delta_min -> 0. Energy can tend to zero while force stays finite or diverges if the source cells shrink too quickly relative to the wider stencil. Independent mass solves verify both the recovery sequence and counterexamples. A second test retains the two wave fronts and confirms the source-force law only after the WHOLE source stencil fits inside those fronts.

These are mathematical and numerical consistency results for a defined part of the discretization, not new observational evidence. No new live trajectory was evolved. The previously measured MTS endpoint discrepancy remains 7.30384e-9, or 13.58% of the instantaneous continuum force, over the short 4e-5 interval. Its full evolving, variable-geometry recovery is still open.

## 1. Localize without removing any row

Use the existing definitions B=D-r j^T, r=D(x-b)_+, W>0, v=M^-1 a. At fixed actual live geometry and tangent, the explicit Gram drive is

    J_G = -partial_b E_G + (Bv)^T W(Bu).

Partition rows into S, whose ORIGINAL D stencil touches both sides of the source, and R, all remaining rows. This is a support test, not a magnitude threshold. In particular, floating-point hinge tails and all mixed terms remain in the calculation. With f=Bu, g=Bv and s_i=-W_b,i f_i^2/2,

    |J_G| <= sum_i |s_i| + sum_i |W_i f_i g_i|
          <= sum_i |s_i| + ||f_S||_W ||g_S||_W + ||f_R||_W ||g_R||_W.

The same shape prefix is used when comparing these bounds with global Cauchy; comparing different prefixes would not establish the stated ordering. Complex differentiation of the original row weights supplies W_b. The helper also checks a finite-state mass bound: if d_i=M_ii-sum_(j!=i)|M_ij|>0, then ||M^-1 a||_infinity <= max_i |a_i|/d_i. This follows by applying the largest-component argument to Mv=a; it is not an assumed uniform property of all future states.

|Actual evolved MTS endpoint|257 / cap 2e-5|513 / cap 1e-5|
|---|---:|---:|
|Source rows|7|7|
|Remaining rows|502|1014|
|Source projected work|-4.72718529e-8|-5.76487736e-8|
|Remaining projected work|+1.10109830e-8|+6.22761020e-10|
|Explicit shape force|-2.32377300e-9|-1.48020462e-10|
|Total explicit J_G|-3.85846429e-8|-5.71740331e-8|
|Absolute-row bound|1.84581663e-7|6.65840621e-8|
|Partitioned Cauchy bound|3.11334847e-7|8.24203214e-8|
|Global same-prefix bound|4.66409385e-2|1.38811851e-2|

The tighter bound is useful, but it does NOT show that the extra force is small enough. Both reference endpoints give exactly zero Gram drive. The observed projection maxima are about 0.01146, with finite-state diagonal-margin bounds about 0.0500.

Sources: `scripts/annular_P2_Gram_row_bounds_20260919.py`, `scripts/derive_annular_P2_local_Gram_bound_20260919.py`, `source-intake/navier-stokes/20260914/annular-P2-local-Gram-bound-attempt01/status.json`. All 27 implementation checks pass.

## 2. Exact source reaction, not a fitted coupling

On S alone define

    mu = r^T W r,
    lambda = r^T W f,
    gamma = r^T W g / mu,
    f_perp = f - (lambda/mu) r,
    g_perp = g - gamma r.

Weighted orthogonality gives the EXACT decomposition

    J_S = lambda gamma + R_perp,
    R_perp = f_perp^T W g_perp,
    |R_perp| <= ||f_perp||_W ||g_perp||_W.

Let Delta=j^T u and Delta_star=(r^T W D u)/mu, with the numerator restricted to S. Then

    lambda = mu (Delta_star-Delta),
    gamma = (r^T W D v)/mu - j^T v.

It would be WRONG to replace lambda by -mu Delta on these actual states: their D u is not zero. The earlier unresolved-front fixture had that special property; a general moving-coordinate state does not.

|Actual source reaction|257|513|
|---|---:|---:|
|mu|0.0134708994|0.00343928019|
|Delta_star-Delta|-9.12671076e-10|-1.86833149e-9|
|lambda|-1.22945002e-11|-6.42571548e-12|
|gamma|3844.959292|8971.572712|
|lambda gamma|-4.72718529e-8|-5.76487736e-8|
|R_perp|-8.29280e-21|+1.43406e-22|
|Bound on the remainder|1.13127e-20|2.19037e-22|

The near rank-one behaviour is observed, not imposed. The algebra remains valid with a nonzero perpendicular remainder. A shrinking multiplier is not sufficient for vanishing force when its conjugate direction grows.

## 3. Derive the amplification from the mass projection

This subsection assumes constant positive kinetic weight on each half mesh and source-zero P2 functions. It does not assume those coefficients are constant in the parent problem.

Let eta=1-P_h 1 on a half mesh, including eta(source)=1 when writing the extended nodal values. Eliminating each P2 midpoint from the mass minimization gives

    eta_mid = -(eta_left+eta_right)/8,
    M_condensed = delta/24 * [[3,-1],[-1,3]].

At a free far endpoint the last vertex ratio is 1/3. Back-substitution through positive element lengths gives ratios

    r_k = delta_previous / [3(delta_previous+delta_next)-delta_next r_(k+1)].

Thus 0<r_k<=1/3 and the source trace coefficient is

    kappa=(7+3 r_1)/2,       3.5<kappa<=4.

On a uniform half-line, r=3-2sqrt(2) and kappa=8-3sqrt(2). For geometric source grading delta,delta,2delta,4delta,..., the tail ratio solves 2r^2-9r+1=0. This yields

    kappa_graded=(311-3sqrt(73))/76 = 3.7548419574216765.

This is derived, not fitted. Eight independent assembled P2 mass solves reproduce the finite graded recurrence. For locally constant physical field traces H_L/H_R, the leading prediction for gamma is kappa_L H_L/delta_L + kappa_R H_R/delta_R. On the two saved live states its relative discrepancies are 9.26e-8 and 1.63e-6. Those comparisons are diagnostics, not a uniform variable-coefficient theorem or acceptance gate.

Sources for sections 2-3: `scripts/derive_annular_P2_Gram_source_reaction_20260919.py`, `source-intake/navier-stokes/20260914/annular-P2-Gram-source-reaction-attempt01/status.json`, and `scripts/derive_annular_P2_Gram_recovery_budget_20260919.py` for the exact geometric asymptote. The reaction runner passes 27 checks.

## 4. A force-consistency law and a counterexample

Take a constant-weight local projection with rigid source translation, so the explicit weight shape derivative is zero IN THIS FIXTURE. The source is interior, phase theta in its uniform base cell, and sufficiently far from the outer Gram closures. Scalar elements fit the source, with source-adjacent lengths delta_L/delta_R. On each side prescribe the exact quadratic

    u(x)=H_L x + b_L x^2/2 + DeltaH x_+ + DeltaB x_+^2/2,
    DeltaH=H_R-H_L,         DeltaB=b_R-b_L.

P2 represents this function exactly. Removing its exact derivative hinge gives Bu=(DeltaB/2) D(x_+^2). Let eta_L/eta_R be the mass-projection defects of section 3, supported on their respective halves. The kinetic projection is exactly

    v=-u' + H_L eta_L + H_R eta_R.

This equality uses extended source values that cancel to zero; neither nonzero source trace is incorrectly treated as a source-zero FE function by itself. With K_H=kappa_L H_L/delta_L+kappa_R H_R/delta_R,

    Bv = K_H r - DeltaH D(1_(x>0)) + D(H_L eta_L+H_R eta_R).

The three interior third-difference vectors for hinge, quadratic hinge and step are respectively

    l=(1-theta, 2theta-1, -theta),
    q=((1-theta)^2, 1+2theta-2theta^2, theta^2),
    p=(1,-2,1).

Their Gram metric has diagonal 10/144 and neighbouring entries -1/144. Exact contraction gives

    T(theta) = -17 theta(theta-1)(2theta-1)/72,
    U(theta) = (34theta^2-34theta-5)/72,
    V(theta) = (34theta^4-68theta^3+34theta^2+9)/72.

Writing d2=D(x_+^2) and tail=H_L eta_L+H_R eta_R, the WHOLE projected Gram force and energy are

    J_G = DeltaB/2 * [K_H h^2 T(theta) - DeltaH h U(theta) + d2^T Dtail/h],
    E_G = DeltaB^2 h^3 V(theta)/8.

No source reaction is removed. The condensed positive tridiagonal recurrence bounds vertex defects by 1; midpoint magnitudes are at most 1/4. Only finitely many d2 rows are nonzero. Consequently the tail term is bounded by a constant times h max(|H_L|,|H_R|), uniformly in the amount of source grading. Bounded traces and curvatures therefore imply

    |J_G| <= C1 h^2/delta_min + C2 h.

The constants depend on the stated profile and bounded coefficients, not on inventing a fitted source force. Hence h -> 0 together with h^2/delta_min -> 0 is SUFFICIENT for this source-local force contribution to vanish. It is not necessary in every exceptional case: theta=1/2 makes T=0, and special trace/curvature cancellations can also suppress the leading term. A symmetric-cell success cannot establish a universal limit.

Numerical counterexamples use the SAME profile and phase across all meshes: theta=0.6, H_L=0.01, H_R=0.012, b_L=-0.8, b_R=-1.1; source lengths are theta h^p/8 and (1-theta)h^p/8. No coefficient is fitted to a parent result. At h=1/512 all three sequences have E_G=1.27572566e-11, yet:

|Source grading|Projected Gram force|Asymptotic behaviour from exact law|
|---|---:|---|
|p=1|-4.76465636e-6|vanishes proportional to h|
|p=2|-2.38318013e-3|tends to nonzero -0.00238307303|
|p=3|-1.22013350|grows proportional to 1/h|

The nonzero coefficient follows independently from the closed geometric kappa, not a regression. These are admissible frozen local test functions, not solutions of the evolving parent. They disprove the inference "small Gram energy alone guarantees small source force"; they do not disprove MTS or establish a bad continuum limit for every mesh path.

Source: `scripts/derive_annular_P2_Gram_force_mesh_law_20260919.py`, `source-intake/navier-stokes/20260914/annular-P2-Gram-force-mesh-law-attempt01/status.json`. All 69 checks pass, including 21 mesh/profile cases, exact polynomial identities, independent mass projections, and the symmetric-phase control.

## 5. Retain the actual two-front structure in the local fixture

The previous constant-coefficient corner response has fronts at -(s+V)t and (s-V)t. The new test adds the SAME response to a linear background and fits the two fronts in the scalar P2 mesh; the wider Gram stencil STILL samples the original uniform base vertices. This is a controlled consistency test, not the parent mesh or a new live integration.

The original seven source-row stencils occupy

    [-(3+theta)h, (4-theta)h].

Therefore the source-polynomial law applies only if that ENTIRE interval lies strictly inside the two fronts. Resolving just the two fine source cells is insufficient. Once resolved, the source term follows section 4; front stencils elsewhere remain included in the full sum.

Using s=0.77,V=0.03,D0=1,background gradient=0.01 and normalized t=1, theta=0.6:

|h|Whole source stencil inside fronts?|Total projected Gram force|Source force / h|
|---|---|---:|---:|
|4|no|-4.01212391|-1.00303098|
|2|no|-4.06872313|-2.03436156|
|1|no|-3.60747711|-3.61096276|
|1/4|no|-0.01944202|-0.07842749|
|1/8|yes|-0.01496766|-0.12270861|
|1/16|yes|-0.00773190|-0.12270861|
|1/32|yes|-0.00380054|-0.12270861|
|1/64|yes|-0.00191734|-0.12270861|

The exact local source-force formula agrees after the stencil is resolved and fails decisively before it is resolved, as it should. All remaining/front rows are retained. Their signs and phases vary; the total result need not be monotone before the asymptotic regime. Matching a single coarse force is not enough.

At the old fixture time 4e-5, the actual 513 layout's h=0.003125 is about 359 times larger than the fixed-phase whole-stencil limit 8.70588e-6. These are PRESCRIBED FIXTURE front speeds, not a measured bound on the evolving parent's characteristics. A phase-safe uniform refinement of the 1.6-wide parent interval would require at least 262145 base vertices among the power-of-two hierarchy. No such expensive live job has been launched or authorized by this estimate. It shows why another blind source-cell halving is not a sensible next test.

Source: `scripts/test_annular_P2_front_projected_Gram_20260919.py`, `source-intake/navier-stokes/20260914/annular-P2-front-projected-Gram-attempt01/status.json`. All 24 checks pass. Time normalization here is a local fixture scaling; this table is not in SI units or the parent's force normalization.

## 6. Do not confuse an extra-term bound with the full GR limit

The actual reduced force is F=(J-q G)/(1+q), q=Q/I. Let P denote the independently computed continuum comparator, J_rem the actual remaining drive, and J_R the remaining projected Gram rows. The complete error identity is

    F-P = [J_rem + lambda gamma - P
           + F_shape + R_perp + J_R - q(G+P)]/(1+q).

This identity keeps the actual geometry response inside J_rem. It does NOT evolve a theory with Gram subtracted, set its reaction equal to missing GR traction, or require separate vanishing in every possible weak/concentrated limit. Such an alternative weak limit would itself need a derivation for the full metric/source equations and test class. A direct strong recovery route instead controls the extra work and proves convergence of the remaining traction.

The evaluated absolute-row bound on this full error is about 1.41186e-7 at 257 and 1.69955e-8 at 513, compared with observed errors 1.25639e-8 and 7.30384e-9. Thus the bounds improve but do not yet establish the desired limit. Both reference controls are included, with discrepancies around 4.4e-10. Floating-point closure residuals up to 7.5e-16 must be added when comparing the evaluated algebraic bound with the independently reconstructed force; these are not interval-arithmetic or continuous-time certificates.

Source: `scripts/derive_annular_P2_Gram_recovery_budget_20260919.py`, `source-intake/navier-stokes/20260914/annular-P2-Gram-recovery-budget-attempt01/status.json`. All 19 checks pass. Their scope is algebraic closure, exact local asymptotes, and source-support validation.

## 7. Next substantive step and preservation boundary

We have replaced an unusable global bound with a localized live calculation, derived the source amplification rather than fitting it, and proved/tested a mesh-dependent local force-consistency condition. The next task is to extend that condition to the ACTUAL positive variable coefficients, non-rigid source pullback and live metric response, and qualify a feasible front-resolved discretization before running another costly coupled evolution. The t -> 0 initial layer requires its own compatibility/uniform-time argument; a fixed-positive-time stencil condition alone cannot settle it.

Do not quietly replace the inherited uniform Gram rule with a nonuniform one: any such construction must be derived from its action and independently checked first. Do not remove high-frequency modes, tune a multiplier, repeat fixed-bulk source halving, or promote a prescribed local fixture into the parent solution.

This checkpoint has 166 implementation checks across five executed validators. Historical failures and all prior completed evidence are retained, including the inherited 37 failed executions. No new failed execution occurred. The integrity seal, compact CSV and immutable resume snapshot are produced by `scripts/seal_annular_P2_Gram_force_mesh_20260919.py`. The protected-workbench check is an mtime scan since 05:36:32UTC, not a pre-turn whole-tree hash baseline. No GitHub, subagents, observational claim, full-interval pass, or full GR/Newton/Maxwell completion is asserted.
