# Independent live continuum GR oracle at fixed material width

Private continuation, 15 September 2026. This is a derivation and controlled numerical comparison, not an empirical or unrestricted-GR claim. Earlier executed scripts, failures and seals are unchanged.

## What this step actually adds

The previous independent continuum benchmark prescribed Schwarzschild geometry. Here scalar radiation, the moving positive-width source distribution, and their common radial mass and lapse evolve together. The independent oracle does not use the repaired finite action's mass matrix, Gram factors, field/source covectors or discrete current as its equations.

There is a useful exact simplification: scaled canonical wave variables remove the need to guess a metric time derivative in the wave equation. They also make the radial mass solve independent of the lapse at fixed canonical data. We derive this before using it. General-purpose Chebyshev integration machinery is shared, not the finite-action physics assembly.

**Result:** the independent live continuum reference is now qualified for this short fixed-width comparison, and the conditional interior angular implication is derived. Both finite-action branches approach that reference as the grid is refined. Neither yet meets the strict0.5% waveform target on the saved17/33/65 grids. The65-node MTS force error is6.06%, reference7.58%; force errors are not monotone across these grid phases. This is genuine progress on the GR connection, not a full-parent or observational claim.

### Completed numerical results

The finest continuum run uses degree512 (513 points on each side, nine material labels), radial degree18, radial spacing.025 and label quadrature12. It evolves to t=.02 in35.3 minutes with7888 RHS evaluations on one core. Independent diagnostics: mass radial residual3.00e-9, lapse radial residual6.47e-10, temporal mass/current error4.20e-9, proper-clock acceleration error3.95e-10, unprojected exterior-mass drift3.38e-12. These are normalized numerical errors, not observational bounds.

The384-to512 comparison gives maximum matched one-sided field difference8.78367e-7 (passes the unchanged2e-6 absolute threshold); physical relative L2 difference9.16970e-6, or0.000917%; physical absolute L2 difference1.013e-7. The physical integral includes the source-position gap. The independent radiation-force comparison differs by2.243e-9, or0.007752% of the maximum continuum force. No global sup convergence across translated jumps is claimed.

| Finite branch | Nodes | Worst physical field error | Final physical field error | Final radiation-force error |
|---|---:|---:|---:|---:|
| Reference |17|29.8861%|29.2235%|63.89%|
| MTS |17|30.0438%|30.0438%|146.24%|
| Reference |33|15.3835%|14.9701%|7.29%|
| MTS |33|15.3835%|15.0598%|1.99%|
| Reference |65|7.77931%|7.50948%|7.58%|
| MTS |65|7.77931%|7.52305%|6.06%|

The identical worst norms at33/65 arise from the common INITIAL interpolation, not identical evolved fields. Both waveform sequences improve approximately linearly with cell size, but this is a sampled refinement result, not an all-mesh theorem. The favorable33-node MTS force value is not selected as a headline pass: it worsens at65, and all rows remain visible.

The coarsest MTS run fails the velocity gate:2.70647e-5 exceeds2e-5; reference17 passes it. That failed comparison is retained. A separate continuation tests33/65 with EXACTLY the same source/clock gates; both branches pass there. At65, maximum position/velocity/clock errors are1.114e-8/8.712e-7/6.100e-9 for reference and1.575e-8/1.408e-6/5.619e-9 for MTS. Final field-norm changes under material quadrature6-to10 are below1.572e-8. This does not turn the failed17-node MTS case into a pass.

All own numerical jobs are finished. Five failed attempts are preserved: oversized trial step; coarse characteristic-variable control; misaligned global sup comparison; genuinely under-resolved aligned comparison; coarsest MTS velocity test. Final integrity sealing follows this saved numerical state.

## 1. Definitions and unchanged preparation

Use the existing polar metric

\[
 ds^2=-N^2dt^2+U^{-2}dR^2+R^2d\Omega^2,\qquad U^2=1-2\mu/R,
\]

on the untrapped, positive-lapse branch. Define

\[
 s=NU,\quad H=\phi_R,\quad W=\phi_t,\quad P=W/s,\quad \chi_\pm=P\pm H.
\]

Here P is a scaled scalar momentum; it is NOT the finite source momentum P_b or a parent gravitational variable. The momentum density of the radial scalar action is R²P.

Labels z lie in [-1/2,1/2], with w(z)=6(z+1/2)(1/2-z), integral w dz=1. Each label has a source position b(z,t), material momentum p(z,t), and two scalar domains meeting at its zero-trace moving source. The common metric sees continuously averaged densities, not products of unresolved delta functions. Write brackets for integral w dz at fixed physical R, extending each field by zero outside its own outer domain. Ordered sources give

\[
 d_b(R)=\frac{w(z_b)}{b_z(z_b)},\qquad b(z_b,t)=R;
\]

the density vanishes outside the source support. The material energy is E=sqrt(S²+U²p²), evaluated at its own source.

Keep the previous repaired-live preparation EXACTLY at the analytic level: base domain [5.2,6.8], shifted by epsilon*z; epsilon=.02; b(z,0)=6.03+epsilon*z; V(z,0)=.03; S=.03; inner mass .7; kappa=.1. The original compact quintic profile is phi=.01*x*envelope(|x|), x=R-b(z,0), envelope1 up to .2 and quintic transition to0 by .55. W=-.03 H. The different discretizations approximate that same analytic preparation; their interpolated functions and initial total masses are not claimed identical. No rescaling is used to hide this initial error.

All numerical controls are normalized, not measured physical parameters. The finite width remains positive and fixed. This is not the newer unequal-slope static-background preparation, not the one-sided Israel shell, and not a zero-width result. The old initial preparation satisfies the first moving trace condition but is not newly tuned for higher-order compatibility.

## 2. Exact canonical-scaled continuum equations

The scalar action is integral[(R²/s)W²-R²sH²]/2. Its Euler equation and mixed-derivative identity give

\[
 P_t=\frac1{R^2}\partial_R(R^2sH)
     =sH_R+(s_R+2s/R)H,\qquad H_t=\partial_R(sP).
\]

Consequently

\[
 (\chi_+)_t=s(\chi_+)_R+s_R\chi_++\frac{s}{R}(\chi_+-\chi_-),
\]
\[
 (\chi_-)_t=-s(\chi_-)_R-s_R\chi_-+\frac{s}{R}(\chi_+-\chi_-).
\tag{1}
\]

There is no omitted s_t: the change of variables absorbs it in the canonical density. At a moving numerical mesh point add v_grid*partial_R chi to (1); this is coordinate transport, not new physics.

At each source, V=N U²p/E and r=V/s=Up/E. The trace equation W+VH=0 gives the incoming data

\[
 \chi_+^-=-\frac{1-r}{1+r}\chi_-^-,\qquad
 \chi_-^+=-\frac{1+r}{1-r}\chi_+^+.
\tag{2}
\]

Eliminating these endpoints enforces the physical boundary condition, not an energy correction or arbitrary state projection. At the fixed outer endpoints H=0 gives chi_plus=chi_minus. This reflecting outer choice matches the finite-action control and carries no scalar energy flux through the endpoints.

## 3. Live constraints and source force

Set T=<P²+H²>, J=<PH>. Then rho_bar=U²T/2 and the existing continuum radial equations become

\[
 \mu_R=\kappa\frac{R^2U^2}{2}T+\kappa U E d_b,
\]
\[
 (\log N)_R=\frac{\mu}{R^2U^2}+\kappa\frac R2 T
               +\kappa\frac{Up^2}{R E}d_b.
\tag{3}
\]

The first equation has no lapse at fixed P,H,p. Solve it with the inner mass fixed, then integrate the second and impose N_out=U_out. Unlike normalizing a velocity-loaded radial solve afterwards, this is a legitimate canonical solve. Boundary values (2) depend on U through r and are included in the mass fixed point.

Combining (3) with (log U)_R=mu/(R²U²)-mu_R/(RU²) gives the exact cancellation

\[
 \frac{s_R}{s}=\frac{2\mu}{R^2U^2}-\kappa\frac{S^2d_b}{RUE}.
\tag{4}
\]

Explicit wave terms cancel from this combination, NOT from the gravitational solution: mu and N still include the waves. The independent implementation uses derivatives of the reconstructed metric; the cancellation is checked symbolically rather than used to suppress a residual.

With DeltaH²=H_minus²-H_plus² and the pressure force derived in the previous checkpoint,

\[
 F_\phi=\frac{b^2NU}{2}(1-r^2)\Delta H^2,
\]
\[
 \dot p=-N E(\log N)_R-\frac{NU^2p^2}{E}(\log U)_R+F_\phi
       =-\frac{N\mu}{b^2}\left(\frac E{U^2}+\frac{p^2}E\right)
        -\kappa\frac{NbS^2}{2E}T+F_\phi.
\tag{5}
\]

The explicit local source-density force cancels. Its integrated gravitational mass does NOT disappear. The code uses the unreduced metric-gradient expression in (5); the reduced law is an algebraic cross-check. Proper clocks advance at ell=N S/E.

## 4. Independent temporal and proper-clock checks

The stress-derived temporal mass equation is

\[
 \mu_t=\kappa NU^3\left(R^2J-pd_b\right).
\tag{6}
\]

We do not evolve or project mu with (6). Instead differentiate four independently re-solved radial constraint states along the actual wave/source RHS and compare with (6) at fixed physical radii, including inside the source band.

The source-frame wave density is

\[
 \langle\rho_\phi^{(u)}\rangle
 =\frac{U^2}{2(1-r^2)}\{(1+r^2)T+4rJ\}\ge0.
\]

The sum-of-squares origin is <(P+rH)²+(H+rP)²>. Using b_tau=U²p/S, the prior proper acceleration law is

\[
 b_{\tau\tau}=-\frac{\mu}{b^2}-\kappa b\langle\rho_\phi^{(u)}\rangle
                 +\frac{U^2}{S\ell}F_\phi.
\tag{7}
\]

Differentiate actual proper speeds from neighboring solved states, then compare to (7). The zero-wave case is checked separately against an independent proper-time ODE b_tautau=-mu_initial/b² with advected source mass. The zero-coupling case is compared to the earlier independent solver in variables f_plus/minus=W+/-sH, not only to another invocation of the new code.

## 5. Conditional interior angular completion, not an extra axiom

There is an analytic step beyond checking the three radial/temporal Einstein components. Let E^mu_nu=G^mu_nu-2*kappa*T^mu_nu in the present normalization, with E^R_t=-N²U²E^t_R from symmetry. Direct evaluation of the full polar metric connection gives

\[
 \nabla_\mu E^\mu{}_R=
 \partial_t E^t{}_R+\partial_R E^R{}_R
 +\left(\frac{N_t}N-\frac{U_t}U\right)E^t{}_R
 +\left(\frac{N_R}N+\frac2R\right)E^R{}_R
 -\frac{N_R}N E^t{}_t-\frac2R E^\theta{}_\theta.
\tag{8}
\]

The missing premise is total matter conservation at the moving interface, not merely the name Bianchi. It can be established for this chosen continuum action. Write densitized stress with radial volume factor D=N R²/U and jump convention Delta=left-minus-right. Differentiating the moving scalar domains gives the covariant radial and temporal interface divergences

\[
 D\nabla_\mu T^\mu{}_{R,\phi}=-F_\phi\delta(R-b),\qquad
 D\nabla_\mu T^\mu{}_{t,\phi}=V F_\phi\delta(R-b).
\tag{9}
\]

These follow directly from W_minus/plus=-V H_minus/plus, not from assigning a compensating current. The proper-time source action has D*T_source^t_R=p*delta(R-b). Its divergence is (p_dot-F_gravity)*delta=F_phi*delta by (5); constant source rest mass makes the temporal component minus V times this radial force. Thus the interface divergences cancel in both components. Ordinary bulk scalar conservation holds away from the source. The fixed label weight and common metric allow this weak conservation identity to be averaged linearly over z.

Contracted Bianchi then gives div(E)=0. If the exact radial mass/lapse constraints and temporal mass equation hold, E^t_t=E^R_R=E^t_R=0 throughout the regular interior. Equation(8), for R>0, forces E^theta_theta=E^varphi_varphi=0. **The angular Einstein component follows conditionally for this continuum spherical interior; it need not be supplied as a separate closure axiom.** This is an analytic implication, not an assertion that sampled numerical residuals vanish exactly.

Scope matters: this does not prove unrestricted GR, derive the chosen material/reflectivity law uniquely from the MTS parent, establish convergence of the repaired finite action to this continuum system, or supply exterior boundary supports. Finite reflecting annular boundaries can require their own stress/support completion. The identity is an interior result, including the weak moving source interfaces, not a global black-hole spacetime completion.

## 6. Numerical scope, failures and next decision

Material-label polynomial collocation is an approximation, not exact finite-label Galerkin variation. Density quadrature splits at physical layer-domain boundaries and the inverse moving source map. Label, radial and time refinements are required, as is scalar spatial refinement. A successful local mass-current test by itself is not a waveform accuracy proof.

The first degree384 attempt allowed an oversized internal Runge-Kutta trial to leave the regular metric domain before a trajectory was saved. The failed status is retained. A new attempt caps the first and maximum timestep in proportion to inverse scalar degree squared and saves every accepted .005 interval. It changes no continuum equations, controls, or acceptance tolerances. An unphysical rejected numerical trial is not evidence of physical horizon formation.

The first degree64 comparison between different characteristic variables misses the 2e-8 field agreement gate (1.04645e-7) despite source agreement3.51e-12. This failure is retained and tested under spatial refinement, rather than weakening the gate. At finite polynomial degree, differentiating a metric-times-field product does not obey the continuum product rule exactly; the separate commutator calculation diagnoses this effect explicitly.

The diagnosis is constructive. On each source-fitted domain let D_R be the collocation derivative and v_grid its velocity. Converting the canonical chi evolution to f=s*chi differs from discretizing the f equation directly by

\[
 (v_{grid}\pm s)\{D_R(s\chi_\pm)-sD_R\chi_\pm-s_R\chi_\pm\}.
\]

This exact finite-operator identity holds to2.73e-14 in the independent check. The product defect shrinks from6.97e-6 atdegree64 to7.63e-7 atdegree192. Evolving the degree192 zero-coupling control gives maximum field difference3.90e-9 and source difference5.32e-14 across three layers, passing the ORIGINAL2e-8/2e-9 gates. The separate dust control passes five independent proper-clock orbit checks. We do not redefine finite collocation as an exact continuum product calculus.

The paired comparison uses the saved repaired reference/MTS live trajectories at17,33,65 nodes, same width/coupling/preparation and time interval. It samples physical W,H, splitting BOTH source positions, and separately reports mass, lapse, source position, velocity, clock and radiation-force errors. Radiation force includes the derivative of field-carried source momentum: F_h=L_b_wave-dot(zeta_h), not L_b_wave alone. No Gram row or coefficient is dropped.

Additional honest failure: the completed degree384 trajectory passed its radial/current/proper-acceleration checks but failed the global pointwise refinement test. A gradient jump sampled between source positions differing by only~6e-12 produces an error~1.04e-4 even as those positions converge. For a jump J translated by delta, the global sup error is |J|, while the squared L2 error is J²|delta|. We therefore distinguish matched one-sided traces from an integrated physical norm that INCLUDES, rather than masks, the gap. This is a change of comparison metric with an explicit mathematical reason, not an unchanged global-sup claim.

The first corrected comparison also failed, for a genuine resolution reason: the192-versus384 aligned error is7.50057e-6, above2e-6, dominated by the original compact quintic initial preparation. Its physical relative L2 error is6.16134e-5, but that does not erase the failed pointwise gate. The next degree512 refinement (513 points per side) keeps the same equations, preparation, source width, label/radial choices, and2e-6 one-sided threshold.

To make that computation affordable we tested exact factorizations of the density interpolation. Only incoming source endpoint values change during the radial fixed point, so their linear contributions can be updated without rebuilding the whole interpolation. All polynomial degrees and weights remain. The first coefficient-space factorization agrees but is slower at the tested large grid; it is retained as such. The subsequent barycentric implementation agrees with the original flow to4.13e-16, geometry to1.12e-16 and sampled density to2.06e-18 across six initial/final cases. This is numerical equivalence, not a new physical approximation or removal of modes.

### Next concrete calculation

Do NOT repeat continuum-force, local-current or angular-closure acquisition audits. The next task is an efficient sparse implementation of the REPAIRED LIVE finite action and its continuously averaged density assembly, with small-grid equivalence tests against the existing dense implementation before new evolution. Retain every Gram factor and the moving field-carried source momentum. The current dense averaged density tables become memory-expensive at large node counts; do not simply launch a very large dense run.

Then compare finer finite grids against the now-saved512 continuum trajectory, retaining the same analytic preparation, fixed width and time interval. Include several source-cell phases at similar resolutions because the force errors above are not monotone. Changing node counts while keeping physical endpoints and preparation fixed is preferable to moving the physical source to improve a result. Pre-check no-crossing margins; derive transfer before crossing or an arbitrary long-time refinement. Targets remain0.5% physical waveform error and a resolved physical radiation force, not conservation alone. Uniform convergence, parent uniqueness and exterior/global completion remain separate tasks.

The strict0.5% waveform target remains explicit; evidence of refinement is not relabeled as passing it. The conditional continuum angular implication above is distinct from a finite-action angular/convergence theorem. Full GR/PPN, parent uniqueness, cell-crossing transfer, an all-mesh/long-time theorem, zero width, and observational fits remain unproved here.

## Sources and reproducibility

Local derivational parents: `DERIVATION-20260915-continuum-radiation-force-and-independent-GR-benchmark.md` and `DERIVATION-20260915-repaired-live-canonical-geometry-and-current.md`. The new force and finite-width material construction come from those explicit conditional actions, not from a newly imported external result.

External bulk-context cross-check: Guo, Hu, Wang and Shao, *New results on the dynamics of critical collapse*, Chinese Physics C48(2024)065104, [DOI10.1088/1674-1137/ad361c](https://doi.org/10.1088/1674-1137/ad361c). The publisher record and scalar/polar-coordinate description were inspected2026-09-15; a follow-up full-page fetch timed out. This is background for the standard spherical Einstein-scalar formulation, not evidence for our added moving material law or MTS completion. No numerical values are imported from it.

New code: `scripts/derive_annular_live_scaled_characteristics_20260915.py`, `scripts/annular_live_continuum_characteristics_20260915.py`, `scripts/verify_annular_live_continuum_snapshot_20260915.py`, `scripts/run_annular_live_continuum_evolution_20260915.py`, `scripts/annular_live_continuum_comparison_tools_20260915.py`, `scripts/run_annular_live_continuum_refined_20260915.py`, `scripts/run_annular_live_continuum_refined_v2_20260915.py`, `scripts/verify_annular_live_oracle_independent_controls_20260915.py`, `scripts/verify_annular_live_oracle_controls_refined_20260915.py`, `scripts/derive_annular_characteristic_product_defect_20260915.py`, `scripts/derive_annular_continuum_angular_closure_20260915.py`, `scripts/compare_annular_repaired_live_continuum_20260915.py`.

All statuses and raw trajectories are stored below source-intake/navier-stokes/20260914, with unique attempt directories. Final integrity seal: `source-intake/navier-stokes/20260914/annular-independent-live-continuum-final-integrity.json` (only authoritative once complete). No GitHub action. Protected formalization-workbench remains untouched.

Additional comparison/refinement implementations: `scripts/annular_live_jump_aware_comparison_20260915.py`, `scripts/qualify_annular_live_oracle_jump_aware_20260915.py`, `scripts/annular_live_continuum_fast_20260915.py`, `scripts/verify_annular_live_continuum_factorization_20260915.py`, `scripts/annular_live_barycentric_20260915.py`, `scripts/verify_annular_live_barycentric_20260915.py`, `scripts/run_annular_live_continuum_degree512_20260915.py`, `scripts/compare_annular_repaired_live_continuum_v2_20260915.py`, `scripts/compare_annular_repaired_live_continuum_v3_20260915.py`, `scripts/seal_annular_independent_live_continuum_20260915.py`.

Primary final numerical statuses: `source-intake/navier-stokes/20260914/annular-live-continuum-degree512-attempt01/status.json` and `source-intake/navier-stokes/20260914/annular-repaired-live-continuum-comparison-attempt03/status.json`. Conditional angular proof: `source-intake/navier-stokes/20260914/annular-continuum-angular-closure-attempt01/status.json`. Earlier failed comparisons stay at their original attempt paths and are inherited in the final seal.
