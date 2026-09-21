# A conforming force lift: numerical controls, a derived residual bound, and targeted refinement

2026-09-18. Private continuation of `DERIVATION-20260918-P2-independent-continuum-bridge.md`.
Status: complete numerical and algebraic checkpoint; no force-convergence or full-GR claim.
All numbers use the existing annular test's normalization, not newly inferred SI observables.

## 1. Question and answer

The previous short-horizon waveform gates passed at base_count65, but the force gates did not.
Before paying for another trajectory, this stage asks whether that discrepancy is integration
precision, and then derives a residual representation that identifies where the discrepancy lives.

The held-state precision changes are far too small to explain the observed force errors. A new
conforming test function removes the large internal-edge cancellation analytically. It leaves
gradient-jump/source lifting work, the scalar Euler residual, and a combined Gram contribution.
Every physical force and Gram term is retained. This is not a force correction or a change of
initial conditions to erase an unfavourable result.

## 2. Matched saved-state numerical controls

Use reference65 at t=0 and MTS65 at t=0.001, their respective worst sampled force states.
Interpolate BOTH saved canonical coordinates and momenta when raising the material degree.
Check preservation at101 material labels, then solve the coupled canonical/radial inverse anew.

Baseline settings are material degree14, radial degree18, action quadrature32, label quadrature20.
Each branch receives eight settings: baseline; action48; action64; label28; radial26;
material18; material22; and material22/radial26/action64/label28 together.

|Saved state|baseline force error|largest tested force change|
|---|---:|---:|
|reference65, t=0|-5.813571175e-7|4.016478684e-10|
|MTS65, t=0.001|-4.475569869e-7|4.004721546e-10|

The largest changes come from the action quadrature. Increasing radial and material degrees
changes these forces only around floating-point precision. All16 canonical/radial inversions,
polynomial-transfer checks and broken-traction checks pass. The tested changes are below the
pre-existing2e-9 extraction-control threshold and below0.1% of the corresponding force errors.
They do NOT form a certified numerical error bound. Transferring an already-evolved polynomial
does not certify an independently evolved higher-material-degree trajectory. No time evolution,
time-tolerance refinement, or new physical fit occurs in this comparison.

Sources: `scripts/budget_annular_P2_saved_force_20260918.py`,
`source-intake/navier-stokes/20260914/annular-P2-saved-force-budget-reference-attempt01/status.json`,
`source-intake/navier-stokes/20260914/annular-P2-saved-force-budget-MTS-attempt01/status.json`.

## 3. Derive the conforming lifting identity

Retain the earlier definitions, at the central material label:

    C=R^2 N U, K=R^4/C, H=phi_R, W=phi_t at fixed R,
    E=partial_t(K W)-partial_R(C H) inside each element,
    c=partial_b R, V=bdot, v_j=c_j V,
    F_h=L_b(wave)-d/dt(field momentum conjugate to b),
    P_h=(C_b-K_b V^2)(H_left^2-H_right^2)/2.

The derived broken-traction identity is

    F_h-P_h = integral c H E dR
              +sum_(internal j != source) c_j (C_j-K_j v_j^2)
                       (H_left,j^2-H_right,j^2)/2
              +F_Gram,shape.                                      (1)

Choose a continuous, source-zero P2 function v_h. At an ordinary vertex set
v_h=c(H_left+H_right)/2; at each element midpoint set v_h=cH; set its source
and both outer-endpoint values to zero. Let v denote its free nodal values.
This is an admissible instantaneous scalar variation, not a new evolved field.

The moving-node trace phi_t+v_j phi_R is continuous. Consequently the distributional
Euler traction at an internal vertex is

    J_j=[C H+v_j K W]_(left-right)
       =(C_j-K_j v_j^2)(H_left,j-H_right,j).

Writing e_i=dot(p_i)-L_(phi_i), the scalar weak identity is

    v dot e = integral v_h E dR + sum_j v_h(R_j) J_j + DE_Gram[v_h]. (2)

Equation(2) is valid off shell: e is not assumed zero. At the source and outer
boundaries v_h=0, so no omitted boundary force is hidden in this subtraction.
At every other internal edge, the term in(1) equals v_h(R_j) J_j exactly.
Subtracting(2) from(1), with rho=cH-v_h, therefore gives

    F_h-P_h = v dot e + sum_elements integral rho E dR
              + F_Gram,shape - DE_Gram[v_h].                       (3)

For the EXISTING lifted Gram factor B, nodal sampling S, base spacing h_G,
nodal Jacobian J and nodal coefficient C,

    E_Gram = [S(C/J)] dot (B phi)^2 / (2 h_G),
    DE_Gram[v_h] = [S(C/J)] dot ((B phi)*(B v)) / h_G.               (4)

No assumption of small Gram work enters this identity. In particular the explicit shape
term alone is NOT the full Gram contribution to the projected residual. The actual Gram
accelerations also remain inside E. Nothing is projected out of the evolved equations.

### Exact element formula and bound

On each physical element c is affine and H is affine, so cH is quadratic. Since rho
vanishes at the midpoint, its only coefficients are its endpoint mismatches a_L,a_R:

    rho(x)=a_L (1-x)(1-2x)+a_R x(2x-1), 0<=x<=1,
    integral_element rho^2 dR = h_e(2a_L^2+2a_R^2-a_L a_R)/15.     (5)

At an ordinary vertex these mismatches are opposite halves of c times the gradient
jump. At the physical source they are the full one-sided H, since c=1 and v_h=0.
The source contribution therefore cannot be discarded just because neighbouring
gradient jumps are small.

Cauchy-Schwarz gives the exact conditional inequality

    |F_h-P_h| <= |v dot e|
        +sum_e sqrt(h_e(2a_L^2+2a_R^2-a_L a_R)/15) ||E||_(L2,e)
        +|F_Gram,shape-DE_Gram[v_h]|.                              (6)

To bound F_h-F_ref, add |P_h-F_ref|, or control the signed combination directly.
Small waveform energy error alone is still insufficient: source derivative traces,
the weighted Euler residual, and Gram work require control. Equation(6) does not
assert any of them already converge uniformly. Numerical quadrature evaluations
below are not interval-certified enclosures of the exact integrals.

## 4. Independent algebra and live-state checks

`scripts/derive_annular_P2_conforming_force_lift_20260918.py` verifies(5) symbolically,
checks(3) both off shell and on saved live states, checks(4) against a complex variation,
and tests the elementwise bound and integration32 versus48.

Four manufactured cases use arbitrary accelerations and an analytically time-dependent
metric, rather than satisfying the equations to make the identity pass. Negative controls
detect incorrectly omitting v dot e or the Gram variation. The manufactured metric is only
a test fixture, not a physical Einstein solution. All four off-shell identities close within
4.34e-18. Together with the four live cases there are eight new verified lifting identities.

|Saved65 case|lifting bulk work|combined Gram work|computed bound(6)|
|---|---:|---:|---:|
|reference, t=0|-5.811472468e-7|0|2.770564687e-6|
|reference, t=.004|-1.979362530e-7|0|2.375387409e-6|
|MTS, t=.001|-9.423813319e-7|-7.472748905e-7|4.803059541e-6|
|MTS, t=.004|-1.646417085e-6|-3.685894933e-6|9.073485464e-6|

The scalar weak pairing is near roundoff. The live force identities close within2.10e-10,
consistent with the independently measured action-quadrature sensitivity; increasing the
identity's own integration order makes a negligible change. These are not exact decimal-zero
identities for the quadrature-discretized code.

The old absolute-term estimates were about1.5e-3. The new bounds are much tighter, but
still do not certify the force accuracy target. At final MTS65, the approximately-5.3325e-6
defect continues to cancel the approximately+4.9715e-6 trace/geometry mismatch. The actual
remaining error is about-3.6105e-7. Neither deleting a term nor forbidding that cancellation
would be a valid convergence argument.

The element ledger identifies BOTH source-adjacent and outer wave-profile contributions.
At reference t=0, the source-near lifting sum is-3.2285e-7, but several transition-profile
elements individually contribute around1.4e-7. At final reference, the source-near sum
is only-1.4030e-8: concentrating all refinement on the source would miss the main remaining
bulk contributions. At final MTS the source-near sum is-1.4117e-6 and the Gram combination
is substantial; this is not simply the reference residual with a negligible extra term.

Evidence:
`source-intake/navier-stokes/20260914/annular-P2-conforming-force-lift-manufactured-attempt01/status.json`,
`source-intake/navier-stokes/20260914/annular-P2-conforming-force-lift-saved-attempt01/status.json`.

## 5. Initial-only refinement probes

Compare uniform base_count129 against source-only8-to16 subdivisions at base_count65,
in BOTH branches. Reprepare the same analytic initial profile;
do not transfer an old spatial polynomial and call it newly resolved data. The global
refinement changes the MTS Gram base spacing, whereas source-only refinement keeps it.
Neither experiment certifies an evolved force curve.

|Initial preparation|scalar nodes|reference force error|MTS force error|
|---|---:|---:|---:|
|existing base65/source8|158|-5.813571175e-7|-2.600534471e-7|
|base65/source16|190|-4.199267840e-7|-9.861711261e-8|
|base129/source8|286|-1.714772001e-7|-1.217518503e-7|

Global refinement reduces the initial reference error by70.5% and the MTS error by53.2%.
It also nearly removes the reference bulk contribution away from the source: its remaining
source-near lifting work is-1.6142e-7, versus total lifting work-1.7158e-7. Source-only
refinement halves the initial source-near work but leaves the reference bulk error in place.

The smaller source16 MTS error is not evidence that source-only refinement is generally
better: its lifting bulk work-4.9407e-7 cancels combined Gram work+3.9567e-7. With global129,
these are-1.7437e-7 and+5.2516e-8. The comparison remains a discretization diagnostic,
not a physical competition won by MTS.

Both global129 initial errors are below the2e-7 absolute threshold, but all four NEW rows
still exceed0.5% of the existing short-horizon reference peak, namely2.7005981e-8.
Thus no combined force target is passed, even at the single initial instant. No evolved
waveform or peak-force gate is upgraded by these static tests.

Source: `scripts/probe_annular_P2_force_refinement_20260918.py`.
Evidence: `source-intake/navier-stokes/20260914/annular-P2-initial-force-refinement-source16-attempt01/status.json`,
`source-intake/navier-stokes/20260914/annular-P2-initial-force-refinement-uniform129-attempt01/status.json`.

## 6. Scope and next action

The mathematical advance is(3)-(6): an admissible weak test function analytically cancels
the internal-edge work and exposes computable source/gradient-jump and Gram terms. The
numerical advance is a matched precision budget and an actionable spatial error map.

The old failed full-horizon force gates remain failed. The previous six combined short-horizon
accuracy rows remain false. This stage proves neither full GR recovery, a unique covariant
parent action, local PPN agreement, a black-hole theorem, nor an observational MTS preference.
All work stays private and inside post-checkpoint-work; no GitHub or galaxy-repo changes.

Next: choose JOINT bulk/source refinement using the tested local contributions, checking
the source-induced step-size cost before another trajectory. Global129/source8 alone is
already known to miss the combined force target at t=0; do not blindly re-evolve it and
expect that maximum-error gate to pass. Then test a justified resolution's actual short
trajectory with saved intermediate states. Keep time and material evolution
uncertainty distinct from the held-state controls here. Do not repeat a radial-representation
repair or replace the finite source force by continuum pressure. The earlier flat-background
corner analysis in `DERIVATION-20260917-initial-corner-response-and-frozen-action-prediction.md`
is retained, not rediscovered as new work; it is not automatically a live-geometry estimate.
