# From the extra Gram energy to the radial mass and lapse

Private derivation, 14 September 2026. This is a new physical-spacing family of **radial constraint solutions**, not a replay of the earlier time evolution at higher numerical resolution. No parameters fitted, no empirical or full-GR claim.

## 1. The result and its scope

For this candidate annular system, with the same scalar profile, free scalar momenta, proper source velocity and reservoir, lower mass seed, and outer clock:

1. Adding the positive Gram term increases enclosed mass and lowers the lapse **inside the normalization radius**.
2. Both changes are bounded by the **integral of the extra Gram density**. Shrinking source collars do not require a uniform pointwise source-density bound.
3. Under uniform integrated base/source bounds and a regular chart, disappearance of the positive extra energy is also **necessary** for the enclosed-mass difference to disappear at a radius enclosing that energy.
4. Uniform H3 control is one sufficient route: the extra energy, mass difference and log-lapse difference are O(h^4). It is not asserted to be the only route.

Thus the earlier action-level bound now reaches the geometry, not just the scalar action. The remaining dynamical question is whether actual evolving, physically prepared solutions satisfy the extra-energy disappearance condition. This note does not assume that they do.

The gamma=0 branch is the candidate's nearest-neighbour, no-extra-Gram control. Calling it the earlier “GR control” does not prove that this entire regulated scalar/apparatus system is continuum GR, that every MTS coupling vanishes, or that the parent theory has acquired its full GR/Newton limit.

## 2. Exact equations and matching convention

Let A be the lower support radius and b the common outer clock-normalization radius. Set F_j=1-2M_j/R and U_j=sqrt(F_j), j=0,1. With kappa>0, write

    M_j' = kappa [ F_j (e_0 + j e_G) + k + U_j sigma ],
    (log N_j)' = M_j/(R^2 F_j) + kappa (e_0 + j e_G + k/F_j)/R.

Here e_0>=0 contains the common nearest-neighbour potential and free scalar kinetic density; e_G>=0 is precisely the added factor potential. The proper-velocity source contributes

    k = (W/width) omega_right R^2 v^2/2,
    sigma = (W/width) E.

The matched quantity is v, NOT the source canonical momentum p_right=R^2 v/U: the latter must change with the geometry. Holding p_right fixed as well would be a different comparison. E is nonnegative; signed reservoirs are outside this theorem. All quantities here are at a single time; no equality of future scalar/source trajectories is implied.

The lower seeds agree, M_1(A)=M_0(A)>=0. At b impose the same positive clock multiplier C:

    N_j(b)=C sqrt(F_j(b)).

This matches the specified boundary normalization N/U=C, not equal values of N(b). If equal boundary lapses were prescribed instead, the boundary log term below would change. The convention used here is the one implemented by the existing solver.

These are the equations in `scripts/annular_horizontal_clock_evolution_20260913.py`, with the source-kinetic split already checked in `scripts/annular_radial_response_20260914.py`. The new implementation uses that original radial collocation solver, with analytically manufactured profiles, not a substituted gravitational law.

## 3. Finite mass comparison: no linearization required

Let d=M_1-M_0. Since U_1-U_0=-2d/[R(U_1+U_0)], exact subtraction gives

    d' + a(R) d = kappa F_1 e_G,      d(A)=0,
    a(R)=kappa [2e_0/R + 2sigma/(R(U_1+U_0))] >= 0.

The integrating-factor identity holds along the two nonlinear solutions:

    d(R)=kappa integral_A^R exp(-integral_s^R a(t)dt) F_1(s)e_G(s) ds.

Although its coefficients depend on those solutions, it is an exact identity, not a frozen-background approximation. If f<=F_j<=Fmax, R>=r>0, and E_G=integral e_G over full support, then

    0 <= d(R) <= D := kappa Fmax E_G.

If R encloses all the extra density, and E_0 and S bound the integrals of e_0 and sigma on [A,R], then

    Aint := kappa [2E_0/r + S/(r sqrt(f))],
    kappa f exp(-Aint) E_G <= d(R) <= kappa Fmax E_G.

This lower bound is important: with uniform f>0, Fmax and Aint, a positive unresolved extra-energy component cannot be hidden by solving the mass constraint. Under these hypotheses d(R)->0 **if and only if** E_G->0. This equivalence concerns this matched, positive-energy radial comparison; not arbitrary solutions, signed corrections, or a global GR-limit theorem.

## 4. Exact lapse comparison and quantitative bounds

Let L=log(N_1/N_0). Algebra, including the proper-source kinetic term, gives

    L' = d(1+2kappa k)/(R^2 F_0 F_1) + kappa e_G/R,
    L(b) = (1/2) log(F_1(b)/F_0(b)).

Consequently, for A<=R<=b,

    L(R) = (1/2)log(F_1(b)/F_0(b))
           - integral_R^b [d(1+2kappa k)/(s^2 F_0 F_1) + kappa e_G/s] ds <= 0.

Use |log F_1-log F_0|<=|F_1-F_0|/f. If K bounds integral_A^b k, then a uniform bound is

    0 <= -L(R) <= B
       := D/(r f) + D/f^2 [1/r - 1/b + 2kappa K/r^2] + kappa E_G/r.

Also

    |F_1-F_0| <= 2D/r,
    |U_1-U_0| <= D/(r sqrt(f)),
    0 <= 1-N_1/N_0 <= 1-exp(-B) <= B.

Nonnegative mass and densities imply N_0(R)<=N_0(b)<=C sqrt(Fmax) inside b, yielding an absolute lapse bound as well. The lapse-sign result is tied to the common outer-clock convention; it is not a clock-normalization-independent observable. Beyond b the reversed radial integral does not have this sign guarantee. For two interior radii, their log clock-ratio correction is L(R_1)-L(R_2), not simply L(R_1).

Only integrated K, E_0 and S enter these estimates. A fixed-energy reservoir density may grow like 1/width without spoiling this static comparison. This does NOT prove a smooth matter limit or harmless dynamical/junction behaviour at a collapsing collar.

## 5. The actual Gram term supplies E_G=O(h^4), conditionally

The immutable action/factor owners are `scripts/annular_covariant_scalar_action_20260912.py`, `scripts/annular_gram_joint_action_20260909.py` and `scripts/sbp4_compatible_second_operator_20260909.py`. The previous proof is in `DERIVATION-20260914-closure-continuation-and-resolution.md` and `scripts/annular_gram_smooth_limit_20260914.py`.

For each translated profile chi_z sampled at R_i+width*z, the local extra density is distributed over the node bands by the nonnegative normalized W(z). Its full integral is

    E_G = integral W(z) [1/(2h) sum_f (sum_i S_fi R_i(z)^2) (B_G chi_z)_f^2] dz.

The third-difference Gram matrix satisfies ||Q(1)||_2<=1/8, with convex coefficient sampling. For each H3 profile the exact repeated-integral identity for Delta_h^3 and Cauchy--Schwarz give

    sum_i |Delta_h^3 chi_z,i|^2 <= 3h^5 ||partial_R^3 chi_z||_L2^2.

Thus, if R<=Rmax,

    E_G <= (3Rmax^2/16) h^4 H,
    H := integral W(z) ||partial_R^3 chi_z||_L2^2 dz.

Uniform H, K, E_0, S, common clock and regular chart constants imply mass and log-lapse differences O(h^4). Geometry convergence here is **between two constraints evaluated on the same data**, not convergence of their different dynamical solutions. No pointwise force convergence, horizon crossing, parent-owned regulator removal or uniform-in-time H3 theorem follows from this calculation.

## 6. Declared physical-spacing test family

This family is a new manufactured constraint test, not a retuning of the earlier saved source/exterior solution:

    fixed node interval [5,6]; count=17,33,65,129;
    h=1/(count-1); width=h/2; z in [-1/2,1/2]; W=6(z+1/2)(1/2-z);
    kappa=.1; lower mass seed=.8 at A_h=5-width/2; clock C=1 at b=6;
    chi(R)=.04 sin(2pi(R-5))+.005(R-5)^3;
    v_free(R)=.012[1+.2 cos(pi(R-5))]; p_free=R^2 v_free;
    v_source(R)=v_free(R); theta_source=0;
    E_source(z)=.003[1+.1 cos(2pi z)].

Gamma=0,.5,1 multiplies the extra energy, implemented by sqrt(gamma) on the extra factors. The source energy and free/kinematic data are identical within each comparison. Gamma is a comparison homotopy, not a fitted physical coupling.

The **physical spacing and collar width change**, while radial numerical degree remains32. Independent degree48 and adaptive radial integration test numerical error separately. Full supports extend slightly beyond [5,6]; the common comparison interval [5,6] is fixed. All extra-factor sampling lies at interior nodes, so b=6 encloses all e_G for these disjoint collars. The nonzero source reservoir collapses toward the outer endpoint; its integral stays .003091189065278..., but its peak grows like1/h.

For this smooth family the translated interval has length1 and

    H=.04^2(2pi)^6/2+.03^2=49.22402671105558.

The cosine cross-term integrates to zero over every translated unit interval. For all h<=1/16, radii lie in [4.9,6.1] and |R-5|<=1.1. A uniform first-derivative estimate is

    ||chi'||^2 <= (.04*2pi)^2+2(.015)^2(1.1)^4.

The base potential is <=Rmax^2||chi'||^2/2, by the first-difference integral identity. Summing all nodal kinetic weights, including the proper-source kinetic split, gives an upper bound Rmax^2(.0144)^2/2. Also S<=.0033. Use the coarsest-grid bound for the extra energy. While F>0, nonnegative mass implies F<=1 and

    M <= .8+.1(E_base+E_G+K+S) <= .919984960338894,
    F >= 1-2(.919984960338894)/4.9 = .6244959345555535 > .5.

A standard continuation barrier therefore prevents reaching F=.5 on any of these finite constraint domains, for every gamma in[0,1]; this is not just a sampled minimum. Lapse positivity follows from its exponential solution and positive outer normalization. The chosen smooth input, not its generation by evolution, is what is controlled.

## 7. Main results — independently verified

All61 main checks pass, eight profile/grid cases with three nonlinear geometry solves each. Pilot units, not physical seconds or metres.

| Nodes | h | Extra integral E_G | max mass difference | max abs log-lapse difference |
|---|---|---|---|---|
|17|.0625|5.8058011e-4|4.0575261e-5|2.1059917e-5|
|33|.03125|3.9354676e-5|2.7490141e-6|1.4267963e-6|
|65|.015625|2.4808623e-6|1.7324088e-7|8.9932311e-8|
|129|.0078125|1.5495310e-7|1.0818727e-8|5.6169981e-9|

These are maxima on the declared common513-point output grid; the inequalities in sections3--5 are the analytic uniform statements. Halving h approaches a factor16 reduction. All cases respect the exact integrated bounds and the conservative analytic H3 bounds. The coefficient gamma=.5 gives the expected intermediate mass/lapse ordering. No experimental accuracy is inferred from these numerical differences.

Measured mass orders are3.88361,3.98806,4.00118; log-lapse orders3.88365,3.98780,4.00097. Independent verification passes88 checks:

- Exact symbolic subtraction reproduces the finite mass and lapse identities, including the reservoir damping and source kinetic terms.
- An independent explicit third-difference/local-energy implementation agrees with the original factor matrices; it does not use their matrix products to reconstruct the density.
- Adaptive DOP853 integration evolves the base mass and the exact **finite difference** directly, avoiding subtraction of nearly equal numerical masses. It agrees with the original separate nonlinear constraint solves: maximum base-mass error2.610e-14; mass-correction error1.081e-14; log-lapse-correction error2.510e-15 across smooth and rough cases.
- Radial degree32vs48 and adaptive tolerance/step refinements are independent of physical h refinement. Maximum degree-refinement difference9.104e-15; maximum adaptive-refinement difference2.487e-14.
- The original state-interpolating geometry agrees with the manufactured-profile override. All saved arrays are finite; all inherited source/evidence hashes match.
- Dropping source damping or the outer-clock normalization produces resolved errors. The source integral stays fixed while its peak increases eightfold; the two-sided integral estimates remain satisfied.

These tests check implementation and examples. The analytic inequalities, rather than finite samples or check counts, support the conditional theorem.

## 8. Bounded energy alone: now a geometric negative control

Replace only chi by chi_i=.04h(-1)^i, constant across each translated layer. Use the same source, momenta, seed, clock, grids and solver in both branches. The smooth-family H3 bound is NOT applied to this sequence.

The base scalar energy is bounded, yet the actual extra integrals increase from .1135700 to .1274386. The mass difference increases from .00801753 to .00899551, and the absolute log-lapse difference from .00412099 to .00462185. This is non-decoupling within the manufactured **radial constraint solutions**, not just an algebraic action example. It is not a dynamically selected mode or observed effective matter.

There is also an analytic barrier/lower bound. Every exact unit-Gram positive margin is >=1/20. With amplitude a=.04, all third differences have magnitude8ah. Convex sampling of R^2 gives

    E_G >= (8/5)a^2 r^2(1-2h) >= (8/5)a^2 r^2(7/8),   h<=1/16.

The norm<=1/8 gives E_G<=4a^2 Rmax^2, and the nearest-neighbour potential <=2a^2 Rmax^2. Add the same kinetic/source integral bounds to obtain a uniform regular-chart barrier. Section3 then supplies a strictly positive, h-independent mass-difference lower bound at b. Thus this sequence cannot acquire the no-extra-Gram geometry merely by taking h smaller. Uniform unweighted H3 control was sufficient, not a consequence of bounded energy.

With r=4.9 and Rmax=6.1 these conservative uniform bounds are E_G>=.0537824, M<=.83643739328, F>=.65859698233, and d(b)>=.00267540618. They hold for the stated rough family at every h=1/(count-1), count>=17, not only the four measured grids.

## 9. What the next derivation should target

The next actual gap is now sharper: derive propagation of small **E_G,h(t)** for h-refined, source-compatible evolving data, or construct a legitimate weak-limit stress if it survives. A proof of uniform H3 would suffice; the two-sided radial comparison shows precisely which weaker energy-disappearance condition would also suffice. Do not demand H3 unnecessarily, and do not promote a static matched-family result to full solution convergence.

Source layers, boundary compatibility, finite-h exterior excitations, and the distinction between common data and trajectories must stay in the equations. A frozen-background linear estimate can be a diagnostic but cannot replace that coupled propagation proof. The original affine inner history remains failed/unimposed as recorded previously.

## Evidence

- New helper: `scripts/annular_gram_geometry_bound_20260914.py`.
- Main runner: `scripts/derive_annular_gram_geometry_bound_20260914.py`.
- Main evidence: `source-intake/navier-stokes/20260914/annular-gram-geometry-bound-attempt01/status.json`.
- Predecessor seal: `source-intake/navier-stokes/20260914/annular-closure-continuation-final-integrity.json`.
- Independent runner: `scripts/verify_annular_gram_geometry_bound_20260914.py`.
- Independent evidence: `source-intake/navier-stokes/20260914/annular-gram-geometry-bound-independent-attempt01/status.json`.
- Completion authority: `source-intake/navier-stokes/20260914/annular-gram-geometry-bound-final-integrity.json`. It must have state=complete and all checks passing before this note is treated as sealed.
