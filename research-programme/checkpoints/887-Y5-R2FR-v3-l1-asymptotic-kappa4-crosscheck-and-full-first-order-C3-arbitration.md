# 4871 - Third-order dipole tail, quartic surface cross-check and C3 arbitration

Marker: V3_L1_SURFACE_KAPPA4_AND_C3_ARBITRATION_4871

Decision: PARENT_V3_L1_EQUATION_AND_ASYMPTOTIC_CURRENT_DERIVED_FIVE_POINT_FINITE_C_SURFACE_KAPPA4_EQUALS_ONSHELL_L4_TO_TWO_TIMES_TEN_MINUS_EIGHT_ZERO_BOUNDARY_VARIATION_CONFIRMED_REFINED_PARENT_C3_SELECTED_FOR_INTERNAL_CORRESPONDENCE_PRINTED_GUPTA_C3_DEMOTED_TO_EXTERNAL_SOURCE_DISCREPANCY_PRIMITIVE_MTS_OWNERSHIP_STILL_OPEN_PRIVATE_NONCLAIM

## Result

The two decisive checks left by checkpoint 4870 have now been performed rather than parameterized.

First, the physical O(v3), l=1 residual profile is generated directly from the same reduced parent action. If

\[
q(v,R)=q_1(R)+v^2q_3(R)+O(v^4),
\qquad
\bar I_\ae=v^2I_2[q]+v^4I_4[q]+O(v^6),
\]

then the third-order equation is

\[
\boxed{\mathcal H_2[q_1]q_3=-\mathcal E_4[q_1].}
\]

It uses the exact I2 Hessian and exact Euler source of I4; no third-order response coefficient is inserted.

Second, expanding the aether surface current through v3 gives a new asymptotic formula for the quartic compact-body response. Across five finite-compactness points, the surface value agrees with the independently integrated on-shell I4 value to at worst 1.83e-8.

At r=1/3 and C=0.3:

    kappa4_action  = -0.15842313375869
    kappa4_surface = -0.15842312565170
    absolute gap   =  8.11e-9

This closes the direct v3, l=1 cross-check of the checkpoint-4870 stationary-mass result.

The first-sensitivity cubic conflict has also been narrowed and adjudicated for internal MTS work. New symmetric runs at |C|=0.005, 0.0075 and 0.01, each extrapolated from outer radii 100, 200 and 400, give

    a2_parent = -2.6825953696
    a3_parent =  4.9573884008
    conservative parent interval: 4.95 < a3_parent < 4.97

The a2 value reproduces the published exact coefficient -338345/126126=-2.6825951826.

Both arXiv v1 and v2 TeX sources contain the same printed C3 formula and both omit a binary operator immediately before the final 16 alpha1^2 alpha2 term. That ambiguous term vanishes identically on the diagnostic slice r=1/3 because alpha2=0, so the typography alone does not explain the discrepancy. On that slice the interpreted published value decomposes as

    non-c_omega block = 7.8402120755
    c_omega alpha1^3 = 2.9973055267
    sum               = 10.8375176022

Omitting the second surviving term gives 7.8402120755; reversing its sign gives 4.8429065488. Neither intersects the controlled parent interval. The conflict is not repaired by a single obvious omitted or sign-flipped term.

For the selected correspondence action, the parent value is now the internally operative branch because it is derived from the action, its Euler equations, the exact metric Ward identity and the independent asymptotic surface current. The printed C3 expression is retained as an unresolved external-source discrepancy, not silently treated as an exact parent calibration. This is not a claim that the published paper is generally wrong.

## Exact third-order equation

Let q=(a,b) denote the normalized radial and angular dipole profiles and write

\[
I_2[q]=\int dR\,L_2(q,q';R),
\qquad
I_4[q]=\int dR\,L_4(q,q';R).
\]

The leading profile obeys

\[
\mathcal E_2[q_1]\equiv
\frac{d}{dR}\frac{\partial L_2}{\partial q_1'}
-\frac{\partial L_2}{\partial q_1}=0.
\]

Expanding the complete field equation gives

\[
\mathcal E_2[q_1]
+v^2\left(\mathcal H_2[q_1]q_3+\mathcal E_4[q_1]\right)
+O(v^4)=0.
\]

The residual boundary conditions are

\[
a_3(0)=b_3(0),\qquad a_3'(0)=0,
\]

\[
Ra_3'+a_3=0,\qquad Rb_3'+b_3=0
\quad (R\rightarrow\infty).
\]

They impose regularity and a decaying 1/R tail while preserving the already factored exact asymptotic gamma-v normalization.

## Exact surface-current identity

Write

\[
a_1=1+\frac{A_1}{R}+O(R^{-2}),\quad
b_1=1+\frac{B_1}{R}+O(R^{-2}),
\]

\[
a_3=\frac{A_3}{R}+O(R^{-2}),\quad
b_3=\frac{B_3}{R}+O(R^{-2}).
\]

Direct expansion of the aether surface current gives

\[
\mathcal S_v
=-\frac{2}{9(1+r)}
\left[(3r^2+6r+1)A_1+4B_1+C(6r^2+18r+8)\right],
\]

\[
f_{\rm surface}=-\frac{\mathcal S_v}{4C}.
\]

The quartic coefficient is

\[
\mathcal S_{v^3}
=-\frac{2}{45(1+r)}\,\mathcal N_3,
\qquad
\boxed{\kappa_{4,\rm surface}
=-\frac{\mathcal N_3}{360C(1+r)},}
\]

where

\[
\begin{aligned}
\mathcal N_3={}&
(21r^2+48r+1)A_1
+(15r^2+30r+5)A_3\\
&+(-6r^2-48r+34)B_1+20B_3\\
&+C(60r^2+180r+80).
\end{aligned}
\]

The v coefficient exactly reproduces the checkpoint-4869 first-response Ward formula before numerical substitution. The v3 coefficient is therefore an independently normalized quartic observable, not a fitted rescaling of I4.

## Finite-C surface test

All rows use a quadratic 1/Rmax extrapolation from Rmax=100, 200 and 400.

| C | r | kappa4_action | kappa4_surface | absolute gap |
|---:|---:|---:|---:|---:|
| 0.03 | 1/3 | -0.03721686661 | -0.03721684836 | 1.82e-8 |
| 0.10 | 1/3 | -0.09349093713 | -0.09349092351 | 1.36e-8 |
| 0.20 | 1/3 | -0.13584277563 | -0.13584276506 | 1.06e-8 |
| 0.30 | 1/3 | -0.15842313376 | -0.15842312565 | 8.11e-9 |
| 0.30 | 1/12 | -0.04290597289 | -0.04290596141 | 1.15e-8 |

The extrapolated delta-I2[q1;q3] residual is below 5.6e-8 on all five rows. This independently verifies the zero-boundary cancellation used in checkpoint 4870.

## C3 source arbitration

The public co-scaling map is

\[
\alpha_1=-\frac{8rp}{1+r},\qquad
\alpha_2=-\frac{rp(1-3r)}{1+r},\qquad
c_\omega=p(1+r-rp).
\]

At r=1/3, alpha2=0. The external C3/p expression therefore has only two surviving source blocks. The final printed alpha1^2 alpha2 ambiguity vanishes and cannot affect this diagnostic.

| compactness magnitude | a2 estimator | a3 estimator |
|---:|---:|---:|
| 0.0050 | -2.6828144782 | 4.9577807214 |
| 0.0075 | -2.6830884610 | 4.9582810703 |
| 0.0100 | -2.6834722180 | 4.9590001286 |

A quadratic extrapolation in C^2 gives a3_parent=4.9573884008. The conservative interval 4.95 to 4.97 remains disjoint from the interpreted printed value by at least 5.8675.

The internal decision is:

    retain the action-derived parent finite-C response
    use its refined C3 coefficient for internal expansions
    record the printed Gupta C3 coefficient as an unresolved external-source discrepancy
    do not use the printed C3 truncation as an endpoint calibration
    do not claim a correction to the external paper without its unpublished derivation or author confirmation

## Consequence

The finite-compactness f, kappa4, g and D4 chain is now internally closed through two independent asymptotic readouts inside the selected correspondence action. The direct v3, l=1 objection is closed, and the external C3 expression no longer supplies an admissible closure condition for this parent branch.

This still does not derive the correspondence action from the primitive MTS motion/time/space fields. It also does not supply a tabulated-EoS theorem, the solitary-body spin map, or a full local-GR claim.

## Decision

Checkpoint 4871 selects the action-derived compact-response branch for internal MTS development and closes its independent quartic tail check. The next high-value step is to stop extending this compact-body ladder and return to the central ownership problem: derive the selected unit-flow/public-metric correspondence action and universal matter coupling from the primitive MTS variables, or explicitly demote that bridge.

Next: 4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md

Sources: [Yagi et al. 2013](https://arxiv.org/abs/1311.7144); [Gupta et al. 2021](https://arxiv.org/abs/2104.04596); [Foster 2005](https://arxiv.org/abs/gr-qc/0509121).
