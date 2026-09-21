# Boundary-response memory correction without differentiating the clock again

Private continuation, 2026-09-10 (Europe/London). No GitHub action.

## 1. What is constructed, and what remains conditional

The derived endpoint source can be removed from the corrected energy equation
by retaining its causal response in a comparison variable. This is an analysis
device determined by the existing equations and endpoint data, NOT a new
physical field, phenomenological memory coefficient, fit, or changed boundary
condition. The response still carries energy and must be bounded.

Results:

- Exact moving-coefficient boundary-memory correction and energy identity.
- A mesh-independent response bound for frozen M,K and bounded-variation
  endpoint input. This is an analytic bound, not an extrapolation of three meshes.
- A conditional moving-coefficient extension using an explicit two-column
  transport defect F_B=B_t-D_h B. It needs no beta_t in the corrector ODE.
- Derivation of a uniform mass-norm bound on B and B_t from the original mass
  projection; F_B is sourced and measured, but not yet uniformly bounded.
- Independent finite-time input Gramian and nonzero-time-history controls.

Validation: 237 memory/energy checks +67 moving-transport checks =304 passing
checks on 18 unchanged saved states, six frozen coefficient controls and one
manufactured moving two-mode system sampled at three times. These are numerical
identity/control checks, not new empirical physics successes.

Not proved: a uniform bound on the ACTUAL beta history's total variation;
a uniform bound on F_B and the moving transport forms; an integrated actual
corrector history; uniform remaining-source estimates; box persistence;
full nonlinear/DAE/local-GR or horizon closure. No new trajectory is generated.

## 2. Exact correction on the actual moving coefficient path

Use the definitions and derived endpoint law from
`DERIVATION-20260910-paired-variational-work-and-graph-energy-correction.md`.
In particular g=Ld-M^-1 F_b, h=Lz, L=M^-1 K,
D_g=C-A, D_h=C-A-L A L^-1, and E_H=(g^T K g+h^T M h)/2.

Let ell_map be the original two-column affine endpoint lift, and define

    B=M^-1 (M_full ell_map)_I,
    beta_end=(beta(a+),beta(b-)),
    b=B beta_end+b_reg,
    b_reg=Pi_h(beta-ell_beta)+Gram_part+quadrature_part.

All three pieces of b_reg remain. No free endpoint slope is fixed.
The original equations along their coefficient path are

    g_t=h+D_g g+B beta_end+b_reg,
    h_t=-L g+D_h h+r.

Define the zero-initial-data comparison response (g_b,h_b) by

    g_b,t=h_b+D_g g_b+B beta_end,
    h_b,t=-L g_b+D_h h_b.

This uses the original beta values themselves, not their time derivative.
It changes neither the physical state nor its endpoint histories. Once that
state path is specified it is a linear driven comparison problem, not an
additional freely chosen dynamical sector.

Subtract it: g_c=g-g_b, h_c=h-h_b. Then EXACTLY

    g_c,t=h_c+D_g g_c+b_reg,
    h_c,t=-L g_c+D_h h_c+r.

The positive corrected energy and its explicit correction are

    E_c=(g_c^T K g_c+h_c^T M h_c)/2,
    E_b=(g_b^T K g_b+h_b^T M h_b)/2,
    E_c=E_H+Delta_b,
    Delta_b=E_b-g^T K g_b-h^T M h_b.

The exact identity is

    E_c'=g_c^T R_g g_c+h_c^T R_h h_c+g_c^T K b_reg+h_c^T M r.

The same finite-mesh G_H from the previous derivation therefore gives

    E_c' <= G_H E_c+sqrt(2 E_c)*sqrt(||b_reg||_K^2+||r||_M^2).

Crucially, the original energy is NOT identified with E_c. The triangle bound is

    sqrt(E_H) <= sqrt(E_c)+sqrt(E_b).

If E_b is uncontrolled, the correction has only reorganized the difficulty.
The following bounds address that response explicitly rather than deleting it.

At N64 the actual remaining source norm is 0.00443305 (GR), 0.00444128 (Gram),
versus the unsplit configuration source norms 4.99672 and 5.03021. These are
instantaneous data diagnostics, not proof that b_reg is uniformly H1 between
samples or across all meshes. Its internal derivative jumps still matter.

The local correction tests use a frozen constant-input response as an arbitrary
comparison VALUE at each saved state, with its derivative set by the ACTUAL
moving comparison equations. Complex directional differentiation independently
checks the identity. This validates the local algebra for a comparison jet;
it is NOT an integration of the actual comparison history from time zero.

## 3. A genuinely uniform frozen-coefficient response bound

Freeze positive M,K, keeping the actual Gram term in K. Choose M-orthonormal
modes K V=M V Omega^2, V^T M V=I. Write B_hat=V^T M B. In energy coordinates
Y=(Omega V^T M g_b,V^T M h_b), the response to a constant endpoint vector beta is

    Y(t) = ( sin(Omega t) B_hat beta,
             [cos(Omega t)-I] B_hat beta ).

For every frequency and every t,

    sin^2(omega t)+(cos(omega t)-1)^2 <=4.

Thus

    E_b(t) <=2||B beta||_M^2.

Since B is the actual weighted orthogonal mass projection of the affine lift,

    ||B beta||_M^2 <=Q[m ell_beta^2]
                   <=m_max*(length/2)*|beta|^2.

Gauss4 integrates the affine square exactly. The final constant is independent
of the mesh, the stiffness spectrum and the positive Gram contribution:

    E_b(t) <=m_max*length*|beta|^2.

Here m_max=60025/1024 and length=1/4 are inherited coefficient-box bounds.
This statement is uniform only on the stated positive coefficient box, not
through c=0 or a horizon. It does not assert frozen geometry is a new solution.

For beta of bounded variation, superpose step responses R(t) with ||R(t)||<=2:

    Y(t)=R(t)B_hat beta(0)+integral_(0,t] R(t-s)B_hat d beta(s),
    E_b(t) <=m_max*length*(|beta(0)|+TV_[0,t](beta))^2.

This covers absolutely continuous, piecewise smooth and finite-jump BV inputs.
It requires a bound on variation, not an unspoken assumption that beta is
constant. No high-frequency endpoint input is declared harmless without it.
Replacing a derivative by a BV requirement does NOT establish the temporal
regularity of the actual parent source for free.

At duration 0.01, holding each final snapshot's derived beta constant solely
as a control gives:

|Intervals|GR response energy|Gram response energy|Uniform bound, approximately|
|---|---:|---:|---:|
|16|0.000240058|0.000245122|0.01182|
|32|0.000267987|0.000279575|0.01182|
|64|0.000280342|0.000276373|0.01182|

The artificial h^(-1/2) growth of the instantaneous projected source norm is
absent from this proved response bound. That does not remove real endpoint
work or prove a corresponding bound on the full moving physical solution.

## 4. Conditional nonautonomous bound and the exact remaining transport term

Let the state norm be ||(u,v)||_t=sqrt(u^T K(t)u+v^T M(t)v). Let U(t,s) be the
homogeneous evolution of the moving graph system, and suppose its energy
transport obeys G_H(t)<=Gamma(t), so that

    ||U(t,s)||_(s to t)<=P(t,s)=exp(integral_s^t Gamma/2).

Define J(t) beta=(0,B(t) beta) and

    F_B=B_t-D_h B.

The original endpoint injection (B beta,0) equals the homogeneous generator
acting on J beta, minus (0,D_h B beta). Integrating by parts with respect to the
BV input, rather than differentiating it inside the corrector equation, gives

    (g_b,h_b)(t)=U(t,0)J(0)beta(0)-J(t)beta(t)
       +integral_0^t U(t,s)(0,F_B(s)beta(s)) ds
       +integral_(0,t] U(t,s)J(s) d beta(s).

Set b_star=sqrt(m_max*length/2). If ||F_B(s)||_(R2 to M(s))<=f_star(s), then

    sqrt(2 E_b(t)) <= b_star*(|beta(t)|+P(t,0)|beta(0)|
                                  +integral_(0,t] P(t,s)|d beta|(s))
                  +integral_0^t P(t,s) f_star(s)|beta(s)| ds.

This is a mesh-uniform moving response bound IF Gamma, f_star and the input's
variation have mesh-uniform bounds. Those hypotheses have not yet been proved
for the full actual coefficient path. The theorem does not replace them with
their sampled values or confuse a sample variation with an upper bound.

B_t itself is directly derived from the mass projection:

    B_t=M^-1[(M_full,t ell_map)_I-M_t B],
    ||B_t||_(R2 to M) <=2||theta||_infinity*b_star.

The inequality follows from ||M^-1 M_t||_M<=||theta||_infinity and contraction
of the mass projection applied to theta times the affine lift. This part uses
only first metric rates. The remaining D_h B is evaluated as the actual
two-column matrix action, not replaced by a blanket high-order operator norm.

Measured final-state M-operator norms:

|Intervals|GR ||F_B|| |Gram ||F_B|| |
|---|---:|---:|
|16|0.002132087|0.002113370|
|32|0.001810342|0.001811056|
|64|0.001688755|0.001689757|

Measured ||B_t|| is between about 1e-8 and 1.4e-7 in these final states.
These data are consistent with a bounded defect but are not its proof.

An independent manufactured moving system checks the integration-by-parts
identity and its bound: M=(1+0.1t)I, K=(1+0.1t)diag(2,8),
B=(1+0.03t)B0, and affine beta(t). Here D_g=0,
D_h=-[0.1/(1+0.1t)]I, and Gamma<=0.1 is an analytic bound.
On 0<=t<=1, ||B||<=sqrt(1.1)*1.03||B0|| and
||F_B||<=sqrt(1.1)*(0.03+0.1*1.03)||B0||. Direct integration of the driven
system agrees with the separately integrated transformed system. This is a
manufactured control, not an MTS run to t=1.

## 5. The L2-input-only shortcut was also tested, not assumed

For a frozen pair the exact map from an arbitrary L2 endpoint input to final
energy coordinates has controllability Gramian

    W(T)=integral_0^T H(s)H(s)^T ds,
    H(s)=(cos(Omega s) Omega B_hat; -sin(Omega s) Omega B_hat).

The squared input gain is lambda_max(W). The code evaluates the sine/cosine
integrals analytically, including their removable zero-frequency differences,
and independently checks the T=0.01 result by high-order time quadrature.

|Intervals|GR gain at T=.01 / .1 / 1|Gram gain at T=.01 / .1 / 1|
|---|---:|---:|
|16|62.34 /115.19 /501.15|63.62 /119.99 /507.97|
|32|76.20 /156.57 /600.26|78.77 /177.99 /703.36|
|64|86.42 /218.97 /919.16|84.53 /261.50 /1033.77|

T denotes the inherited dimensionless control duration, not additional
physical evolution. These gains grow on the tested refinements, especially
for the longer horizons. They neither prove nor disprove a uniform all-mesh
L2 bound. No such bound is claimed from this test.

A sufficient spectral condition was derived rather than guessed. Partition
the positive frequency axis into intervals of width Delta, and define

    D_Delta=max_bands sum_(omega_j in band) ||omega_j B_hat[j,:]||^2.

The elementary interval Sobolev estimate on the Fourier transform of an input
supported on [0,T], followed by Plancherel, gives

    lambda_max(W(T)) <=4*pi*D_Delta*(Delta^-1+Delta*T^2).

The interval estimate is sup|F|^2<=2/Delta integral|F|^2
+2Delta integral|F'|^2; Plancherel supplies the factor 2pi, and
||F'||_L2<=T||F||_L2. Vector-valued inputs use the same argument.
The measured band weights do not yet supply a mesh-uniform spectral bound.
The frozen BV route already has a uniform proof and is the preferred current
route, rather than silently treating this L2-only alternative as established.

## 6. Next derivation

The actual correction is now constructed. Next derive a uniform bound for the
specific two-column defect F_B=B_t-D_h B from the actual constraint rows and
metric derivative jumps. In the same argument bound the paired moving forms
R_g,R_h; do not substitute a large all-directions operator estimate when the
source couples only through two endpoint columns.

Then control the time regularity of the derived beta_end, using the original
endpoint histories and metric/source equations. BV is a precise requirement,
not an excuse to skip a derivation. If proving it simply recreates the
uncontrolled theta_tt ladder, assess the explicit spectral/hidden-regularity
route rather than assuming that difficulty is solved.

Only after these and the remaining-source bounds close should the actual
comparison history be integrated with a new physical trajectory and box
persistence attempted. The present calculations do not require a new long run.

## 7. Files and integrity

New immutable helper and runners:

- `scripts/annular_boundary_memory_energy_20260910.py`
- `scripts/derive_annular_boundary_memory_energy_20260910.py`
- `scripts/derive_annular_boundary_memory_transport_20260910.py`

Results:

- `source-intake/navier-stokes/20260910/annular-boundary-memory-energy-derived/status.json`
- `source-intake/navier-stokes/20260910/annular-boundary-memory-transport-derived/status.json`
- `source-intake/navier-stokes/20260910/annular-boundary-memory-energy-final-integrity.json`

The transport runner's seal phase owns the combined final seal. Do not also
invoke the earlier memory runner's seal phase. Completed evidence directories
are immutable; derive phases require fresh output destinations.

All inherited source/trajectory hashes are checked unchanged. No bytecode cache,
Git action, subagent or shared-process shutdown. Computations run as one
single-core BelowNormal Python worker at a time. The protected workbench check
is an mtime scan since 2026-09-10T00:19:00Z, not a full pre-turn hash baseline.
All work remains private after the existing publication bookmark.
