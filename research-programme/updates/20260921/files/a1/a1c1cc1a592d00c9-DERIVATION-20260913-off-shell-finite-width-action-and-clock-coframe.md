# Off-shell finite-width scalar action and its clock/coframe coupling

Private, 2026-09-13 (Europe/London). This is a new scalar-bulk
regularization candidate attached to the existing gravitational action,
not a completed global initial/boundary-value problem or a GR-limit pass.

## 1. Outcome

We now have an explicit OFF-SHELL action containing both the kinetic
and transported spatial terms, rather than an average inserted into
one constraint equation. It retains variations through the layer,
including scalar shape variations invisible to the old point samples.

The clock/radial coupling is supplied by the existing metric coframe:
it is not a new fitted coefficient. The derivation also identifies the
mixed metric/scalar symplectic term lost if proper scalar velocity is
mistaken for a canonical momentum.

The construction passes action-variation, temporal-boundary, finite
time-coordinate covariance, and independent proper-clock integration
checks for both the GR base and the same base plus MTS Gram terms.
This does NOT show that its constrained initial data propagate yet.
That is the next calculation.

## 2. Exact coframe decomposition

The parent branch has Lambda=m_chi=b2=b3=0, kappa=.1 and

    U=sqrt(1-2mu/R),  beta=kappa N U^3 P,
    d=1-kappa^2 U^4 P^2 > 0,
    c=kappa U P/(N d).

Here beta is the metric shift, P the metric momentum coordinate, and p
below the scalar auxiliary momentum. They must not be conflated.

Define the threading clock and radial factors

    ell=N sqrt(d),          a=1/(U sqrt(d)).
                                                               (1)

The parent metric is exactly

    ds^2 = -ell^2 (dt-c dR)^2 + a^2 dR^2 + R^2 dOmega^2.

Thus the already derived scalar coefficients become

    C=R^2 ell/a,             B=R^4/C=R^2 a/ell.          (2)

The factor U appearing in the preceding interface calculation is the
P=0 limit of the inverse radial coframe, 1/a. It is not a second
independent clock, nor an extra coupling parameter.

For a stationary observer d tau=ell dt. Equation (2) distinguishes the
proper clock from the coefficient C, which also contains radial
geometry. All formulas here assume the positive chart U,ell,a,d>0.

Sources:
`scripts/annular_nonlinear_history_20260912.py`,
`scripts/annular_covariant_scalar_action_20260912.py`,
`scripts/annular_adm_mixed_action_20260909.py`.

## 3. Why translate a whole stencil?

Moving only one sample while retaining the old MTS coefficients does
not preserve the polynomial cancellations those coefficients encode.
In the explicit check, a single-node displacement makes the MTS Gram
factor applied to R^2 about .0332 instead of zero.

A common radial translation r_i(z)=r_i+delta z preserves every spacing,
every factor B_fi and S_fi, the original h and kinetic weights, and all
constant/linear/quadratic cancellations of the Gram factors. Translation
errors in that kernel test are below 1.5e-14.

Therefore use a normalized positive fixed regulator w(z), z in
[-1/2,1/2], and average COMPLETE translated scalar actions:

    S_trial = S_gravity,parent + integral w(z) S_scalar[z] dz.
                                                               (3)

The default tested weight is symmetric. The asymmetric weight is a
control for the correct nonzero first translation moment, not a
preferred displacement of the physical sources.

This intentionally broadens the point-supported matter sampling. It
does not change h, rescale the MTS coefficients, remove the Gram sector
in a mesh limit, or fit the regulator to C1.

Translation is a specific regularization choice, not a proof that the
parent uniquely selects that regulator. For finite width the support
extends beyond the original end nodes by at most delta/2. The test uses
manufactured histories on that extended chart; it does NOT transplant
the old external radial source/clock conditions to shifted surfaces.
Those ports still need a compatible treatment before a global solution.

## 4. Complete scalar action before field equations

For each translated copy let its factor anchor be
a_f(z)=sum_i S_fi r_i(z). The symbol a_f is an anchor radius, distinct
from the radial coframe a in (1). Define

    T_fi,R=c(T_fi,R),       T_fi(s,a_f)=s,
    J_fi=partial_s T_fi,
    A_f=sum_i B_fi chi_i(T_fi),
    D_f=sum_i S_fi J_fi C_i(T_fi).

With the same original factor matrices and weights,

    S_scalar[z]
      = sum_i integral dt omega_i
          {p_i chi_i,t - C_i p_i^2/(2 r_i(z)^4)}
        - sum_f integral ds A_f^2 D_f/(2h).             (4)

Eliminating the auxiliary p_i gives p_i=B_i chi_i,t and recovers the
second-order kinetic term omega_i B_i chi_i,t^2/2. The spatial history
term is NOT added a second time through the old local shift coupling.

The fields chi_i(z,t),p_i(z,t) are retained through the layer. This is a
larger scalar phase space than the old 17 point pairs, not a secretly
equivalent change of basis. For delta<h the radial source layers are
disjoint, so these profiles can equivalently be regarded as fields on
their separate small radial intervals. No scalar degrees in the gaps
are inferred from this representation.

Point-action recovery requires a smooth, compatible limit of these
profiles. Arbitrary fine layer modes cannot be silently discarded.

For fixed regulator and positive regular histories, variation commutes
with the z integral. The gravitational bulk action is unchanged, while
all new scalar metric/scalar variations are taken from (4).

## 5. Clock and temporal-boundary variations are retained

For one copy define Y_fi=delta T_fi. It solves

    Y_R=c_t Y+delta c,       Y(anchor)=0.

The spatial variation after integration by parts in anchor time has
the following components:

    -sum_fi A_f D_f B_fi delta chi_i /h,
    -sum_fi A_f^2 S_fi J_fi delta C_i /(2h),
    +sum_fi I_fi Y_fi,

where

    I_fi=A_f {S_fi C_i A_f,s - B_fi chi_i,t D_f}/h.

It also has the temporal endpoint term

    [-sum_fi A_f^2 S_fi C_i Y_fi/(2h)]_initial^final.    (5)

The kinetic term separately supplies
[sum_i omega_i p_i delta chi_i]_initial^final.
Both are averaged with w. Neither is set to zero merely because it is
numerically inconvenient. These are scalar-sector temporal terms, not
a derivation of new physical radial ports.

The tests vary mu, N, P, chi and all four together, retaining the
induced changes in C, c, T and J. The differentiated action agrees with
the directly assembled variation; its integrated-by-parts version
agrees only when the temporal terms are retained.

## 6. Proper-clock form, without identifying different maps

Let d tau_i=ell_i dt_i at a node and d tau_f=ell_f ds at a factor anchor.
The interaction's proper-clock transfer is

    J_proper,fi = ell_i(T_fi) J_fi / ell_f(s).
                                                               (6)

It is derived from the horizontal map. It is not assumed to equal one,
nor to identify two sides of a physical interface.

In these clock parameters, (4) has kinetic part

    integral d tau_i omega_i
       {p_i dchi_i/dtau_i - p_i^2/(2 r_i^2 a_i)},

and spatial part

    -integral d tau_f A_f^2/(2h)
        sum_i S_fi J_proper,fi r_i^2/a_i.               (7)

Equations (6)-(7) retain exactly the radial factor that was missing
when C was interpreted as a pure clock density.

An independent check integrates the action with proper time as the
integration parameter: it solves dt/dtau=1/ell and accumulates (7),
using the analytically soluble horizontal transport as an independent
reference. The physical coordinate-time endpoints are the same as in
the coordinate calculation. Changing variables does not mean holding
field-dependent proper-time endpoints fixed during subsequent variation.

For the auxiliary kinetic pair, a separately parametrized clock t(s)
gives L=omega p chi' - t' H_kin. Its off-shell reparametrization identity

    t' E_t + chi' E_chi + p' E_p = 0

is checked symbolically. This is not a claim that independently chosen
external source histories have been derived.

## 7. The mixed symplectic term

The kinetic temporal potential remains

    Theta_kin,delta=integral w(z) sum_i omega_i p_i delta chi_i dz.

If one rewrites p_i=r_i^2 a_i v_i, where
v_i=dchi_i/dtau_i on the auxiliary equation, its two-form contains

    omega_i r_i^2 {
        a_i delta v_i wedge delta chi_i
        + v_i delta a_i wedge delta chi_i
    }.                                                  (8)

The second term is essential. At P=0,

    partial_mu a = 1/(R U^3),

so it directly couples metric and scalar variations. Treating v_i as
a canonical momentum with a fixed measure loses this term. Keeping
p_i as the auxiliary canonical coordinate avoids that mistake.

Theta_kin is NOT asserted to be the whole symplectic structure of the
history-dependent theory. The gravitational and spatial transport
boundary terms, including (5), remain present. This checkpoint does
not prove a local Hamiltonian formulation, a degree-of-freedom count,
or ghost/causal stability for the full nonlocal action.

## 8. Matter energy is now live, rather than prescribed by hand

On the zero-shift histories used in the source-force control, define

    e_i(z,t)=omega_i p_i^2/(2 r_i(z)^2)
             +r_i(z)^2 sum_f S_fi A_f^2/(2h).            (9)

Both p and chi remain variables of the action. The direct P=0 metric
variation is

    delta S_scalar
      = integral dz w integral dt sum_i
          {N_i e_i delta mu_i/(r_i U_i)
            -U_i e_i delta N_i}                         (10)

for these metric variations; the general clock/transport contributions
are those in section5.

The tests reconstruct (9) from the live scalar histories and check (10)
against the full action, not against a frozen source table. Agreement
is below 2.2e-19 in the eight controls.

For a disjoint translated layer around r_i, the corresponding bare
energy density is

    epsilon_delta(R,t)
      = sum_i w((R-r_i)/delta) e_i((R-r_i)/delta,t)/delta.
                                                               (11)

Here e_i depends on the whole SAME translated stencil, not an isolated
local value of chi. Equation (11) preserves those physical separations.
It is positive in the tested quadratic/positive-Gram sector.

This provides an action-owned replacement for the previous prescribed
e*w/width. Its use in a newly solved initial jet must retain all the
transport terms, particularly when P=0 but P1 is nonzero. This run
checks (10) on zero-shift histories, not a new coupled initial solution.

When canonical matter profiles remain uniformly smooth as delta shrinks,
(9) tends to the original nodal e_i. Under those additional solution-limit
conditions, the preceding logarithmic-trace calculation becomes a
candidate asymptotic consequence. The mean is still NOT inserted into
the off-shell action.

## 9. Results and limits of the evidence

The completed matched run has 60 validation checks.

- Ten complete action-variation comparisons: maximum error 1.52e-12.
- Temporal adjoint identities: discrepancies at floating-point rounding.
- Independent proper-clock action integrals: differences below 1.56e-15.
- Finite time-coordinate covariance checked in each of six translated
  samples per branch, including kinetic and all spatial factors.
- Six-to-eight-point smearing quadrature and fourteen-to-eighteen-point
  time quadrature agree within the recorded validation threshold.
- Dropping J is detected. Both types of temporal boundary term are
  nonzero in suitable tests.
- All matrices, h and kinetic weights are retained; no source amplitude
  or physical coefficient is tuned.

A deliberately constructed scalar variation vanishes at every old node
for every time, but not through a layer. The old point action sees a
variation near 3e-31; the new finite-width action sees approximately
1.56022e-4 in both branches. This is concrete evidence that off-shell
layer information has not been replaced by endpoint values. It is also
a warning that the layer phase cannot simply be declared identical to
the old finite phase.

The failed first run is preserved. It required a finite asymmetric
smearing to differ from the point action by less than 1e-8, neglecting
the regulator's first translation moment. For beta23 that moment is
-0.1, so

    S_delta=S_0 + delta <z> partial_shift S_0 + O(delta^2).

The corrected runner computes the shift slope independently. It records
the raw finite-width differences (about 2.14e-8 for the action and
3.42e-8 for its variation at the smallest asymmetric test width), and
verifies the predicted first-order displacement. The remaining error
is below 8.6e-14. Symmetric smearing has no such first-order term.

No physical C1 tolerance was changed. Recovering the point action as
delta tends to zero does NOT fix that action's old propagation error.
The earlier 79/177 comparison results and failed full first-jet gate
remain unchanged.

These checks concern a quadratic scalar bulk extension in a
manufactured spacetime. They do not establish full radial diffeomorphism
invariance, a preferred microscopic smearing law, physical boundary
conditions, a coupled evolution, or the MTS-to-GR/Newton limit.

## 10. Next calculation, not another mean prescription

Use the explicit action to derive the averaged scalar force and
horizontal current profile on a shared metric. Then construct constrained
P=0 bulk initial data from the live energy density (11), retaining the
layer matter degrees of freedom.

Test compactly supported C0/C1 identities first, with identical GR/MTS
tolerances and no fitted forces. Only after that tackle the enlarged
support's physical radial clock/source ports and full C2/evolution.
Do not project away layer modes, substitute the on-shell logarithmic
mean, or claim that old boundary certificates transfer.

This is the route from the constructed action to an actual propagation
test; no new successful propagation result is claimed in this note.

## 11. Evidence

Predecessor:
`DERIVATION-20260912-interface-logarithmic-trace-and-distinct-clock-maps.md`.

Implementation:
`scripts/annular_finite_width_full_scalar_20260913.py`,
`scripts/derive_annular_finite_width_full_scalar_moments_20260913.py`,
`scripts/verify_annular_finite_width_full_scalar_20260913.py`.

Completed run:
`source-intake/navier-stokes/20260913/annular-finite-width-full-scalar-attempt02/status.json`.

Preserved failed validator:
`source-intake/navier-stokes/20260913/annular-finite-width-full-scalar-attempt01/status.json`.

The final integrity record is annular-finite-width-full-scalar-final-integrity.json
in the same intake directory, with its immutable resume snapshot.
All changes remain in post-checkpoint-work. The protected workbench check
is an mtime scan from the start of this turn, not a content snapshot.
No GitHub changes or subagents; one BelowNormal single-core worker.
