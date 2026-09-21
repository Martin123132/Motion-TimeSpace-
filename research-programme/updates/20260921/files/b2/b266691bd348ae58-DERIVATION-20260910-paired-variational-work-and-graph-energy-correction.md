# Paired variational work, graph energy, and a derived endpoint-source law

Private continuation, 2026-09-10 (Europe/London). No publication action.

## 1. Result and limits

This step does not assume the troublesome surface or scalar-residual work is
zero. It derives its exact representation through the actual free variational
rows, including every released slope, original endpoint histories, and Gram
stiffness. It then derives the evolution identity for precisely the higher
spatial radius H already used by the second-metric-source bound.

The main results are:

1. An exact signed pairing of outer flux, interfaces, reconstructed scalar
   residual and quadrature work, obtained with an explicit mass-Riesz test.
2. A positive boundary-adapted graph energy H^2/2 whose principal terms cancel
   exactly when paired. Its homogeneous frozen-coefficient version is conserved.
3. A finite-mesh moving-coefficient energy inequality, not a mesh-uniform theorem.
4. A quantitative obstruction to uniformly bounding the H1 projection of data
   with nonzero endpoint trace into the zero-endpoint test space.
5. A bulk formula beta(R) and one-sided endpoint values beta(a), beta(b), derived
   from the original boundary forcing, first/second metric jets and the actual
   elliptic solve. These replace diagnostic fitted endpoint coefficients.
6. An exact source split into this derived endpoint lift, zero-trace volume
   remainder, Gram contribution and retained quadrature remainder.

Validation: 411 paired/graph checks +75 projection checks +147 source-law checks
=633 passing checks. All use the same 18 saved states; there are six frozen
operator controls and six pairs of constant/zero-trace projection controls.
They are identities and diagnostics, not 633 independent empirical tests.

There is still NO mesh-uniform moving-energy propagation, box persistence,
full shift/DAE/nonlinear theorem, local-GR claim or horizon claim. The small
measured bulk growth coefficient is not a proof of stability between samples.

## 2. Fixed setting and inherited quantities

The canonical branch, annulus, coefficient box, positive Gauss4 quadrature,
staggered piecewise-linear mass, nodal piecewise-linear lapse and C1 cubic
released-slope scalar space are unchanged from
`DERIVATION-20260909-spatial-clock-energy-with-retained-interfaces.md`.
All formulas retain the inherited dimensionless coordinate/time conventions.

Let x be the full scalar coefficient vector, y=x_t, a=x_tt. Let I contain all
free scalar rows, including EVERY slope; B contains only the two prescribed
scalar value rows. Full matrices are denoted M_full,K_full. A matrix without
the suffix is the I,I restriction. K includes the actual Gram term when present.
Both M and K are positive definite on I; K_full has the constant-field null mode.

Let ell be the same affine lift of the two original endpoint scalar histories,
d=(x-ell)_I and z=(y-ell_t)_I. No endpoint slope is prescribed. The actual rows are

    M z_t + M_t z + K d = F_b + e,
    F_b = -(M_full ell_tt + M_full,t ell_t + K_full ell)_I.

Here e is the retained free scalar Euler residual (the nonlinear contribution
is zero in this canonical branch). F_b,t is the existing analytic second-jet
boundary-force derivative, not a finite-difference estimate invented here.

Source implementations:
`scripts/annular_first_derivative_energy_20260909.py`,
`scripts/annular_boundary_adapted_energy_20260909.py`,
`scripts/annular_H1_clock_energy_20260909.py`,
`scripts/annular_metric_flux_jets_20260909.py`.

## 3. Exact pairing through the weak equation

On each open reconstruction segment let c=N sqrt(F), theta=c_t/c, v=y/c,
w=chi_R. Define full symmetric quadratic forms

    S = sum(k=0..2) D^(k+1)^T Q_(1/c) D^(k+1),
    T = sum(k=0..2) [D^k(c^-1 .)]^T Q_(1/c) [D^k(c^-1 .)],
    E_sp = (x^T S x + y^T T y)/2.

These are the ACTUAL broken spatial energy forms, not replacements for M,K.
Their coefficient derivatives include spatial derivatives of theta through
order two, but no theta_t or higher time jets. In implementation their action
is evaluated in factored quadrature form to avoid subtracting very large
assembled third-derivative matrix entries.

Set t=M^-1(Ty)_I. This coefficient vector is an allowed zero-endpoint test
function; its slopes are free. The exact full free-row residual is

    e=(M_full a + M_full,t y + K_full x)_I.

Substitution of the free acceleration gives

    E_sp' = W_principal + W_clock + W_endpoint + W_error,
    W_principal = y^T S x - t^T(K_full x)_I,
    W_clock = (x^T S_t x+y^T T_t y)/2 - t^T(M_full,t y)_I,
    W_endpoint = [(Ty)_B-M_full[B,I]t]^T a_B,
    W_error = t^T e.

In particular the previously retained pair satisfies

    Outer + Interface + ResidualWork + delta_Q
       = W_principal + W_clock + W_endpoint + W_error - ReactionWork.

This is not a statement that residual work is numerical error. Its large
weak-to-strong projection component is incorporated into the first three work
terms. The free Euler error is only W_error. Prescribed endpoint velocities
remain in x,y and the principal/clock work; endpoint acceleration appears
explicitly. There is no silent homogeneous-boundary substitution on saved states.

Largest discrepancy with the old signed segment pairing over the 18 states:
4.01e-10. The old physical shift residual and mismatch are copied unchanged.

## 4. Constructive graph-energy correction and exact H transfer

Define, with the existing F_b,

    L=M^-1 K, A=M^-1 M_t, C=M^-1 K_t K^-1 M,
    f=M^-1 F_b, g=Ld-f, h=Lz,
    D_g=C-A, D_h=C-A-L A L^-1,
    b=Cf-M^-1 F_b,t, r=L M^-1 e.

Direct differentiation of the actual rows yields

    g_t = h + D_g g + b,
    h_t = -L g + D_h h + r.

Consequently

    E_H = (g^T K g+h^T M h)/2 = H^2/2,
    E_H' = g^T R_g g + h^T R_h h + g^T K b + h^T M r,
    R_g = sym(K D_g)+K_t/2,
    R_h = sym(M D_h)+M_t/2.

The principal cancellation is the algebraic equality g^T K h-h^T K g=0.
It uses symmetry of the complete K, INCLUDING Gram. It does not require zero
derivative jumps or a continuum integration-by-parts approximation.

This is exactly the H in
`DERIVATION-20260909-second-metric-source-and-clock-acceleration-bound.md`,
not a new regularity radius given the same letter. All 18 stored H values and
adapted graph vectors agree. The energy is positive in the shifted (g,h)
variables; it does not by itself control the boundary lift or the entire
nonlinear geometric state.

An explicit correction to the old energy is Delta=E_H-E_sp. Its derivative is
computed from the two independent identities, so that

    E_sp' + Delta' = E_H'.

This is a constructed correction, NOT a proof that the two uncorrected norms
are uniformly equivalent. No such equivalence is claimed.

For any fixed positive M,K define the finite-dimensional quantities

    G_H=max(0,2 lambda_max(R_g,K),2 lambda_max(R_h,M)),
    B_H=sqrt(b^T K b+r^T M r).

Then the analytic matrix inequality is

    E_H' <= G_H E_H + sqrt(2 E_H) B_H.

The eigenvalues reported by the runner are floating-point diagnostics, not
interval-certified bounds over a state box or all meshes. Independence of mesh
must still be proved for the MOVING transport forms and the source treatment.
This graph identity uses existing F_b,t and therefore theta_t; it does not add
theta_tt or a new sequence of metric time differentiations.

## 5. Why the old raw energy could be misleading

For frozen M,K and homogeneous fixed endpoints, set S0=S[I,I], T0=T[I,I].
The raw energy derivative is z^T D d, with D=S0-T0 L. Its sharp positive
instantaneous logarithmic rate is

    sigma_max(T0^(-1/2) D S0^(-1/2)).

Cholesky whitening constructs an explicit witness attaining that rate; swapping
the sign of one component reverses it. The graph energy, in contrast, has exact
zero frozen principal rate. This is an operator control, not a constrained
coupled solution or evidence of a physical unstable mode. It does not explain
away every rate observed on the real trajectories.

At each branch's final saved geometry:

| Intervals | Raw frozen GR rate | Raw frozen Gram rate | Graph frozen rate |
|---|---:|---:|---:|
|16|27560.883|27344.201|0 exactly|
|32|110245.915|109641.904|0 exactly|
|64|441065.080|439575.715|0 exactly|

The raw rate approximately quadruples when spacing halves in these controls.
No all-mesh asymptotic theorem is inferred from three resolutions. The same
control is applied to GR and Gram; it is not an MTS-only rejection gate.

For the actual driven, moving, final saved states at t=0.01:

| Intervals/branch | E_H | E_H' | measured G_H | B_H |
|---|---:|---:|---:|---:|
|16 GR|17.701551|1.481224|0.000170943|2.498310|
|16 Gram|21.942616|-0.269310|0.000203418|2.515000|
|32 GR|17.754169|1.672751|0.000205529|3.533285|
|32 Gram|19.809607|0.607312|0.000207261|3.556771|
|64 GR|17.779920|1.649114|0.000236055|4.996715|
|64 Gram|18.797616|1.922501|0.000240158|5.030215|

The maximum measured G_H over all 18 states is 0.000403478. The independent
complex directional differentiation discrepancy for E_H' is at most 1.22e-9.
Different norms have different units/weighting conventions; comparing E_H'
directly against the old E_sp' is not a quantitative stability improvement.

## 6. A proved endpoint-projection obstruction

Let Pi_h be the actual weighted Gauss mass projection into the C1 cubic space
with zero endpoint values. The frequently useful uniform H1 projection estimate
for zero-trace inputs must NOT be applied unchanged to nonzero-trace data.

For u_h=Pi_h 1, epsilon=||1-u_h||_L2 and interval length ell, the trace identity
and Cauchy-Schwarz give

    1 <= epsilon^2/ell + 2 epsilon ||u_h,R||_L2,
    ||u_h,R||_L2 >= (1-epsilon^2/ell)/(2 epsilon).

These unweighted norms are integrated exactly by composite Gauss4, because the
reconstruction is cubic. A C1 cubic ramp with all interior nodal values one,
endpoint values zero, and physical slopes zero gives a comparison function.
On one boundary cell its squared error is h times
integral_0^1(1-3s^2+2s^3)^2 ds =13h/35. Both boundary cells give 26h/35.
Best approximation in the weighted mass norm therefore implies

    epsilon <= C sqrt(h), C=sqrt(26 m_max/(35 m_min)),
    ||u_h,R||_L2 >= [1-C^2 h/ell]/[2 C sqrt(h)].

For sufficiently small h this proves an h^(-1/2) lower growth rate. No interface
or boundary condition has been imposed on the physical solution by this test.
For any fixed smooth input with nonzero trace, convergence in L2 together with
a hypothetical uniform H1 bound would likewise contradict trace continuity of
the weak H1 limit. Thus the issue is structural, not a GR-versus-MTS distinction.

The actual constant-projection derivative norms are 25.3993,35.9200,50.7986 for
16,32,64 intervals. As a counter-control, the zero-trace quadratic
(R-a)(b-R) is projected exactly, with derivative norm sqrt(ell^3/3)=0.0721688
on every mesh and branch.

A preliminary two-dimensional K-orthogonal diagnostic split used projected
affine endpoint lifts. It captures over 99.9999% of the squared configuration
source norm at N64 in both branches; its remainder norm is approximately 0.0044.
Its coefficients were diagnostic best projections, NOT physical parameters.
The next section derives endpoint values independently instead of promoting
those fitted diagnostic values into the theory.

## 7. The actual source beta and its endpoint values are now derived

Let m=R^2/c, p=R^2 c and psi be the actual zero-endpoint elliptic response
whose free coefficients solve K psi_I=F_b. All its slopes remain free.
On open segments define

    a_p=p_R/m=2c^2/R+c c_R,
    a_theta=(p theta)_R/m=a_p theta+c^2 theta_R,
    beta = -a_theta(psi_R+ell_R)-c^2 theta psi_RR
           -a_p ell_tR-2theta ell_tt+(theta^2-theta_t)ell_t.

Here theta_t comes from the ALREADY SAVED exact second metric jet:

    theta_t=N_tt/N-(N_t/N)^2-mu_tt/(R F)-2mu_t^2/(R^2 F^2).

All coefficients are therefore determined by original states, endpoint
histories and parent matrices. No optimizer supplies beta(a) or beta(b).

To derive the formula, differentiate the original affine-lift force:

    -F_b,t=(2M_full,t ell_tt+M_full,tt ell_t
             +K_full,t ell+K_full ell_t)_I.

Use M_t density=-m theta, M_tt density=m(theta^2-theta_t),
and integrate the bulk flux p theta(psi_R+ell_R)+p ell_tR by parts.
The flux is continuous: p,theta,psi_R and the affine lift derivatives are
continuous across the actual partition. The free test values vanish only at
the two outer endpoints. Thus there are no unrecorded interface delta terms
in this particular flux pairing. Its derivative, and beta, are still broken.

If V is the actual value reconstruction restricted to I, the exact finite-Q
source identity is

    b = Pi_h beta + M^-1 (K_Gram,t psi)_I + M^-1 delta_IBP,
    Pi_h beta=M^-1 V^T Q[m beta].

The actual affine Gram actions vanish because the Gram factor annihilates
affine nodal data; this is verified, not assumed for psi. delta_IBP is retained
and independently reconstructed as Q[flux test_R+flux_R test]. The agreement
of the source reconstruction is at most 2.14e-16 in coefficient max norm.

With beta_end=(beta(a+),beta(b-)) and its affine lift ell_beta,

    b = Pi_h ell_beta + Pi_h(beta-ell_beta)
        + M^-1 (K_Gram,t psi)_I + M^-1 delta_IBP.

This is the source split with DERIVED endpoint coefficients. No part is dropped.
At t=0.01:

| Branch/mesh | beta(a+) | beta(b-) | endpoint K norm | zero-trace volume K norm | Gram K norm |
|---|---:|---:|---:|---:|---:|
|GR 16|-0.020308809|-0.019852955|2.498128|0.00442009|0|
|GR 32|-0.020312287|-0.019853695|3.533217|0.00442343|0|
|GR 64|-0.020313336|-0.019852934|4.996728|0.00443302|0|
|Gram 16|-0.020305805|-0.019854307|2.514780|0.00444859|0.000150848|
|Gram 32|-0.020315192|-0.019847726|3.556597|0.00443668|0.000110201|
|Gram 64|-0.020312171|-0.019854542|5.030290|0.00444389|0.000078128|

The endpoint terms carry real signed work, about 1.668 (GR) and 1.942 (Gram)
at N64. They cannot simply be deleted because they account for a growing norm.
Quadrature weak remainder maxima are about 7e-13; after higher graph lifting
their K norms reach approximately 3.4e-8. They remain explicitly nonzero.

Subtracting endpoint traces does NOT prove that beta-ell_beta is globally H1:
psi_RR and reconstructed coefficient derivatives may jump internally. Its
small measured projection norm is evidence for the next analysis, not a
uniform-bound theorem. Likewise these one-sided derived traces do not prove
compatibility with an as-yet unproved continuum limit.

## 8. Next mathematical target, not a missing-input audit

Construct a boundary-aware correction/control for the now-sourced term

    g^T K Pi_h ell_beta,

while preserving the original endpoint histories and released slopes. The
remaining zero-trace volume, Gram and quadrature terms are explicit and must
receive bounds using the actual discrete rows and their jump estimates.
Simultaneously bound the paired moving transport forms R_g,R_h without an
inverse-mesh constant. Do not infer that small sampled generalized eigenvalues
provide that bound.

Do NOT reuse the uniform H1 projection estimate on a nonzero-trace input,
pretend the diagnostic endpoint coefficients are fitted parent parameters,
or differentiate boundary correctors repeatedly without identifying whether
that introduces an uncontrolled theta_tt hierarchy. The beta trace law gives
concrete data for choosing the next correction; it is not yet that correction.

Once the driven graph energy closes uniformly, it supplies the existing H in
the second-metric-source estimate. Combine it with the lower adapted energy
and prove box persistence before a new coupled long evolution. No new
trajectory, empirical data acquisition, calibration or public claim occurs here.

## 9. Reproducibility and integrity

New immutable mathematics helper and runners:

- `scripts/annular_paired_variational_energy_20260910.py`
- `scripts/derive_annular_paired_variational_energy_20260910.py`
- `scripts/derive_annular_boundary_trace_projection_control_20260910.py`
- `scripts/derive_annular_boundary_source_trace_law_20260910.py`

Completed outputs:

- `source-intake/navier-stokes/20260910/annular-paired-variational-energy-derived-attempt03/status.json`
- `source-intake/navier-stokes/20260910/annular-boundary-trace-projection-derived/status.json`
- `source-intake/navier-stokes/20260910/annular-boundary-source-trace-law-derived/status.json`
- `source-intake/navier-stokes/20260910/annular-paired-variational-energy-final-integrity.json`

Run each derive phase only in a fresh destination. The last source-law runner's
seal phase owns the combined final seal; do not run the earlier seal phases.
Python runs single-core BelowNormal with BLAS/OMP thread counts one and -B.
No subagent, shared-process shutdown, Git commit, push or merge was used.

Two failed development runs are preserved, not deleted or counted as passing:
`source-intake/navier-stokes/20260910/annular-paired-variational-energy-derived/status.json`
failed an absolute-zero graph-equation tolerance (5.98e-7 cancellation error);
its replacement compares the actual two equation sides with recorded scales.
`source-intake/navier-stokes/20260910/annular-paired-variational-energy-derived-attempt02/status.json`
exposed loss of precision in assembled third-derivative forms (4.17e-6 rate
discrepancy). The successful implementation evaluates the work in factored
quadrature form rather than loosening that rate tolerance. Executed-script
copies and failure ledgers are retained. These failures concern numerical
evaluation, not a failed physical model test.

The previous final seal, all inherited source/output hashes and all trajectories
are checked unchanged. The frozen formalization-workbench protection check is
an mtime scan since 2026-09-09T23:45:00Z, not a full pre-turn hash baseline.
The combined seal records the actual scan result and absence of bytecode cache.
This is post-publication PRIVATE work after PR14; no automatic publication.
