# Boundary-compatible evolution: can the extra energy remain small?

Private work, 14 September2026. This checkpoint moves from manufactured radial constraints to genuine time evolution on changing physical grids. It uses a deliberately stationary boundary source and a nonzero evolving bulk pulse. It is not the earlier driven-apparatus history, a horizon test, or a full GR-limit theorem.

## 1. Preparation before propagation

The previous manufactured profiles were suitable for matched static constraints, but did not enforce temporal compatibility at the ends. Evolving them without correcting that would conflate a preparation error with a theory failure.

Use the same initial scalar and free canonical momentum, reservoir, seed and clock in both branches:

    R_i in[5,6]; count33,65,129; h=1/(count-1); width=h/2;
    y=(R-5.5)/.3;
    b(R)=exp(1-1/(1-y^2)) for |y|<1, otherwise0;
    chi=.02b(R); p_free=.004R^2 b(R);
    source D(theta)=0, v=0, a=0, E=.003, theta(0)=0;
    lower mass seed=.8; outer N/U=1 at R=6; kappa=.1.

The pulse is smooth with compact support inside[5.2,5.8], so the initial endpoint values, rates and forces vanish on both branches, including all factor stencils incident at the endpoints for count>=33. This does not assert an exactly unchanging endpoint neighbourhood for every future time: the free end is evolved and the source end has its specified reaction. No artificial continuum domain-of-dependence property is assigned to a finite spatial lattice.

The stationary source still has its proper clock and reservoir in the equations. Its canonical momentum is0, reaction rho=-Gchi_right and energy rate E'=-rho v=0. Removing its zero-work terms from the computational RHS is an exact specialization, independently compared against the original complete source RHS; it is not a frozen metric approximation. Mass and lapse are solved from the actual changing fields on every RHS call.

The nearest-neighbour “GR control” is the same candidate system without the extra Gram factor. This name is not certification of its entire physical continuum interpretation.

## 2. Exact extra-energy evolution identity

For each translated layer z, R_i(z)=R_i+width*z is fixed in the horizontal chart. Let B_G,S be the actual extra factors and convex coefficient sampling from the previous action. Define

    E_G[chi]=(1/(2h)) integral W(z) sum_f D_f(z) (B_G chi)_f^2 dz,
    D_f(z)=sum_i S_fi R_i(z)^2.

This is the positive density integral entering the radial comparison, not the full lapse-weighted Hamiltonian. With the **actual** coordinate scalar rate q=chi_tau, including the boundary source rate,

    dE_G/dtau=(1/h) integral W sum_f D_f (B_G chi)_f(B_G q)_f dz,
    |dE_G/dtau|<=2 sqrt(E_G[chi]) sqrt(E_G[q]).

Because this is a fixed weighted quadratic norm, the integral triangle inequality gives, also through any zeros of E_G,

    sqrt(E_G(t))<=sqrt(E_G(0))+integral_0^t sqrt(E_G[q(s)]) ds.

No time derivative of N or U is omitted: they enter q, while the weight in this particular density is R^2, not R^2NU. Differentiating the latter action weight would be a different identity.

If E_G(0)<=C0*h^4 and integral_0^T sqrt(E_G[q])/h^2 is uniformly bounded, this identity proves E_G(t)=O(h^4) uniformly for0<=t<=T. The identity is derived; a bound on that integral for all sufficiently fine physical grids is **not** established just by evaluating finitely many trajectories.

## 3. A local discrete product criterion, retaining gravity

At every node q=c p, where c=NU/R^2 and source p=R^2v/U. For the forward difference Delta, direct expansion gives

    Delta^3(cp)_i =
      c_(i+3) Delta^3p_i
      +3(Delta c)_(i+2) Delta^2p_i
      +3(Delta^2c)_(i+1) Delta p_i
      +(Delta^3c)_i p_i.

Let T0,T1,T2,T3 be these four arrays. Define each layer's local product norm

    B_h(z)=sum_(a=0..3) sqrt(h)*||T_a||_ell2/h^3,
    B_h=(integral W B_h(z)^2 dz)^(1/2).

The established Gram norm<=1/8 implies

    sqrt(E_G[q])/h^2 <= (Rmax/4)
        (integral W h||Delta^3q/h^3||_ell2^2 dz)^(1/2)
      <= (Rmax/4) B_h.

Consequently the sufficient propagation estimate can be written entirely in terms of actual finite-difference products:

    sqrt(E_G(t))/h^2 <= sqrt(E_G(0))/h^2
                       +(Rmax/4) integral_0^t B_h(s) ds.

This does not require assuming a globally bounded third derivative of the metric coefficient by itself. Keeping the **local products** matters: the stationary source collar can make coefficient differences large where the scalar momentum is zero or tiny. Replacing the product by a global coefficient maximum times a bulk momentum norm may create a spurious divergent bound.

Conversely, a uniform bound on B_h is not free. The identity locates the coupled momentum/metric quantities that must be controlled; it does not prove their uniform propagation. A moving source may contribute non-negligible momentum in the collar and must be treated separately.

## 4. Conditional regular-chart barrier

The compact pulse obeys |b'|<=8/(.3e), since t^2 exp(1-t)<=4/e for t>=1. Therefore

    integral |chi'|^2 <= .6 [ .02*8/(.3e) ]^2.

For the third-difference Gram term,

    ||Delta^3chi||<=4||Delta chi||,
    E_G<=Rmax^2 integral |chi'|^2.

Together with the nearest-neighbour energy bound Rmax^2||chi'||^2/2, the momentum bound Rmax^2(.004)^2/2 and source energy .003, this yields an h-independent upper bound on the initial full-support mass. The script records its numerical value.

For an exact solution while the chart is regular, stationary-source E remains nonnegative; all scalar energies are positive and enclosed mass is monotone in radius. The previously derived full-support mass conservation then implies

    M(R,t)<=M_total(0),
    F(R,t)>=1-2M_total(0)/r_min.

The initial uniform bound with r_min=4.9,Rmax=6.1 exceeds the chosen floor F=.5. This prevents a horizon from appearing inside this small-data regular-annulus experiment **conditional on existence and the exact conservation law**. It is not a proof of global existence, regularity of all matter derivatives or astrophysical black-hole behaviour. Numerical radial and mass-conservation errors are checked separately.

The conservative numerical values are M_total<=.92924691076440 and F>=.62071554662678. The lapse bound below is N>=.62571335348844.

The same argument bounds the interior lapse away from zero. Let Mstar bound the conserved full-support mass, Mseed=.8, r=4.9, b=6 and f=.5. Since k=0 and positive reservoir energy cannot cancel scalar energy, kappa*integral e<=(Mstar-Mseed)/f. Integrating the lapse equation from R to b gives

    sqrt(f) exp[-Mstar(1/r-1/b)/f -(Mstar-Mseed)/(rf)] <= N(R) <= 1

inside the normalization radius. Beyond b the lapse is nondecreasing, so this lower bound also covers the retained outer half-collar. This supplies conditional nondegenerate geometry/clock factors, not bounds on all their spatial derivatives.

## 5. Do not confuse direct corrections with different trajectories

The two branches start with identical data, but evolve into generally different states Y1(t),Y0(t). Define a no-extra-Gram shadow constraint using the MTS state Y1(t), without changing that state:

    G1[Y1]-G0[Y0] =
       (G1[Y1]-G0[Y1]) + (G0[Y1]-G0[Y0]).

Here G denotes mass and log-lapse profiles. The first term is the direct Gram geometry correction and obeys the previous exact matched-data bounds. The second is the data-response contribution. It cannot be deleted or bounded by the static theorem without further stability information.

Thus even successful small-E_G propagation controls only part of full dynamical convergence. The experiment records both contributions and the actual total difference. A uniform coupled stability/relative-energy estimate remains needed to replace the finite-grid comparison by a theorem.

The data-response contribution also admits an explicit energy bound. Let E0[chi,p] be the common nearest-neighbour potential plus free canonical kinetic density integral, with the same positive R^2, node and layer weights. Let

    Eerr=E0[chi1-chi0,p1-p0].

Here source p is zero, both reservoirs are the same constant, and source k=0. Factoring each quadratic density difference and applying Cauchy--Schwarz gives

    integral |e1-e0|
      <= E_G[chi1] + sqrt(Eerr)(sqrt(E0[Y1])+sqrt(E0[Y0])) =: J.

The same finite mass subtraction holds with a signed density difference on its RHS. Its integrating factor still has nonnegative damping, so

    ||M1-M0||_infinity <= kappa Fmax J.

The absolute log-lapse bound follows from section4 of the previous geometry note with E_G replaced by J and K=0. This is a bound on the **actual different trajectories**, not only the shadow comparison. It shows precisely what an energy-based stability argument must add: control Eerr as well as the extra energy. For example, Eerr=O(h^4) would imply an O(h^2) geometric error bound by this estimate, not automatically O(h^4). The norm bound is sufficient and need not give the sharp observed convergence rate.

## 6. Numerical and provenance status

The declared interval is tau0..06 in pilot units, not seconds. Physical h and width vary, numerical layer degree8 is held fixed for the main pass; higher layer degree and independent time integration are separate validation controls.

Two pilot attempts remain preserved:

- pilot-attempt01: runner variable shadowed the wall-clock module, before any physical solve. Corrected in a new runner version.
- pilot-attempt02: the energy-rate balance passed, but16vs32-point fixed temporal quadrature of sqrt(E_G[q]) differed by5.149e-7 and failed the1e-9 gate. Version3 keeps that gate, refines with adaptive quadrature when needed, and records both the original discrepancy and the accepted error estimate.
- pilot-attempt03:28 checks pass for both33-node branches. This is a pilot result, not the complete refinement result.

The main pass completes78 checks and six trajectories. The table uses MTS energy diagnostics and the **actual different-trajectory** mass/lapse differences:

|Nodes|Maximum saved-sample E_G|MTS final E_G|Final max mass gap|Final max log-lapse gap|
|---|---|---|---|---|
|33|7.6717543e-4|3.2236015e-4|5.6042797e-5|2.7849805e-5|
|65|1.1901060e-4|5.6300690e-5|1.2352730e-5|4.9897236e-6|
|129|1.0653327e-5|5.1746357e-6|1.3826692e-6|5.3697325e-7|

Every trajectory has17 saved times. The maximum in that sample set is the initial energy; no unsampled-time monotonicity assertion is made. The integrated norm inequality supplies a separate conservative control. For the GR-control trajectories E_G is evaluated only as a diagnostic functional, not added to that branch's action or mass equation.

The energy refinement orders are2.6885 then3.4817. Final mass-gap orders are2.1817 then3.1593; log-lapse orders2.4806 then3.2160. The maximum scalar/momentum pair differences are.42164,.19715,.06009, with slower orders1.0967,1.7141. These grids therefore show decreasing dynamical differences but do **not** establish fourth-order convergence of the evolving solutions.

The normalized maximum E_G/h^4 rises804.44->1996.67->2859.73; the sampled MTS velocity Gram energy divided by h^4 rises1.005e6->5.673e6->1.210e7. A grid-independent plateau has not been demonstrated. It would be wrong to report the conditional propagation criterion as an already closed uniform estimate. The compact pulse can require further spatial resolution, but that explanation itself is not a substitute for proving the bound.

The largest main mass drift is8.105e-15. Source energy is constant by its exact zero-work specialization, not adjusted after the calculation. At129 nodes the direct mass-correction maximum is7.5454e-7 while the data-response maximum is1.1904e-6; these maxima need not occur at the same place/time. The latter contribution is significant and remains in all reported total differences.

Independent verification completes78 checks:

- Layer degree8vs12 plus tighter time integration changes common scalar/momentum profiles by at most1.925e-9 and geometry profiles by at most4.885e-15.
- A separate RK4 integration at65 nodes,128/256 steps, agrees with the main state to3.355e-9; its step-refinement difference is4.990e-8, and geometry error1.073e-13.
- The live mass Ward identity agrees to1.735e-17. Independent directional energy differentiation, local product identities, source work and all array/hash checks pass.
- The density-error bounds on the actual different trajectories pass at initial, midpoint and final times on all three grids.

The final base-energy error Eerr is2.8401598e-4,8.3343960e-5,5.6550129e-6, with refinement orders1.7688 and3.8815. This is substantially faster on the finer pair than the maximum pointwise momentum difference; they are different norms and should not be conflated. One nearly fourth-order pair is evidence for the energy-based route, not an asymptotic theorem.

The coefficient-only third-difference maximum grows approximately64-fold from33 to129 nodes, as expected for this shrinking source collar. At final time the MTS norm of the actual local product (Delta^3c)*p/h^3 instead changes only.0012744->.0013477. This supports retaining the local products rather than imposing an unnecessarily strong coefficient-only smoothness condition. The bulk momentum third-difference term still needs uniform control or the augmented-error alternative below.

Final integrity sealing follows these checks. No physical or uniform convergence claim is authorized by these numerical validations.

## 7. Exact augmented-error balance: the next estimate has a concrete target

The actual scalar equations provide a more useful target than separately assuming smoothness of the MTS velocity. Work at each layer with free canonical variables pi=Omega*p, Omega=diag(node weights); the fixed source value and momentum are zero. Let

    A_j=diag(N_j U_j/(omega_i R_i^2)),
    K0_j=B0^T diag(S0(R^2 N_j U_j)) B0/h,
    KG_1=BG^T diag(SG(R^2 N_1 U_1)) BG/h,

restricted to free indices. Each stiffness is symmetric. The two actual trajectories obey

    chi_j'=A_j pi_j,
    pi_0'=-K0_0 chi_0,
    pi_1'=-(K0_1+KG_1)chi_1.

Set dchi=chi_1-chi_0, dpi=pi_1-pi_0, dA=A_1-A_0, dK0=K0_1-K0_0, q0=A_0 pi_0. Define the nonnegative augmented energy, integrated over W,

    Rerr=1/2 integral W [dpi^T A_1 dpi + dchi^T K0_1 dchi + chi_1^T KG_1 chi_1] dz.

It contains both the ordinary state error and the MTS correction. Uniform positive N,U make it comparable to the density energies Eerr+E_G already used above.

Substituting the two equations and cancelling the symmetric base-stiffness terms yields the **exact** identity

    Rerr' = integral W [
        chi_1^T KG_1 q0
        + chi_1^T KG_1 dA pi_0
        - dpi^T A_1 dK0 chi_0
        + dchi^T K0_1 dA pi_0
        + (1/2)dpi^T A_1' dpi
        + (1/2)dchi^T K0_1' dchi
        + (1/2)chi_1^T KG_1' chi_1 ] dz.

For example, the cancellation of the two high-order force terms is

    -dpi^T A_1 KG_1 chi_1 + chi_1^T KG_1 A_1 pi_1
       = chi_1^T KG_1 A_1 pi_0.

No live metric derivative or inter-branch metric difference is discarded in the displayed identity. Stationary boundary reaction does no work; this expression must be extended if the source protocol or its work changes.

The three coefficient-rate terms already have a useful common bound. If eta(t) bounds |partial_t log(N_1 U_1)| over all participating nodes/layers, positivity and convex coefficient sampling imply

    |coefficient-rate contribution| <= eta(t) Rerr.

This follows separately for the positive diagonal A_1 and each positive weighted-square stiffness factor. No inverse power of h enters this form estimate. A uniform bound on eta itself and a bound on the three inter-branch backreaction terms still have to be supplied; finite coefficient rates are not the same as a uniform-in-h theorem.

**Restricted comparison, not the live result:** if both branches were assigned the same constant geometry, dA=dK0=0 and the matrix derivatives vanish. With VG[v]=(1/2)integral W v^T KG v, Cauchy--Schwarz would then give

    |Rerr'|<=2 sqrt(Rerr) sqrt(VG[q0]),
    sqrt(Rerr(t))<=sqrt(Rerr(0))+integral_0^t sqrt(VG[q0]) ds.

That limited result controls both errors using the **reference** velocity, without assuming an independent MTS H3 theorem. We have NOT assigned a common frozen geometry to the live experiments. Their extra backreaction and coefficient-rate terms remain explicitly above.

The exact balance has now also been replayed on all three grids at times0,.03,.06:30 checks pass. An independent complex directional derivative of Rerr agrees with the sum of all seven terms to4.164e-17. Omitting the live backreaction/coefficient terms changes the rate by as much as1.034e-6; those terms are resolved, not silently set to zero. The reference Gram pairing satisfies its Cauchy bound in each case.

Final Rerr values are4.2971156e-4,9.8942825e-5,7.6727878e-6. These positive quantities include both the changing-state error and the live extra action term; they are not the same functional as E_G alone.

The next derivation should control the remaining live terms by a **uniform relative-energy estimate**, using the radial density-difference bound rather than a crude operator norm growing like1/h^2. The algebra and its implementation are now checked. A bound of the required uniform strength is not yet claimed.

## Source owners

- `scripts/annular_horizontal_clock_evolution_20260913.py` — original live mass/lapse/current/source equations.
- `scripts/annular_gram_joint_action_20260909.py` — extra Gram factors.
- `DERIVATION-20260914-Gram-bound-to-radial-geometry.md` — exact matched-data geometry theorem.
- `scripts/annular_compatible_h_evolution_20260914.py` — new compatible preparation and exact stationary-source specialization.
- `scripts/annular_gram_velocity_commutator_20260914.py` — adaptive energy integral and local product identity.
- `scripts/run_annular_compatible_h_evolution_v3_20260914.py` — active runner; older attempted runners are preserved.
- `source-intake/navier-stokes/20260914/annular-compatible-h-evolution-main-attempt01/status.json` — main execution authority.
- `scripts/verify_annular_compatible_h_evolution_20260914.py` and `source-intake/navier-stokes/20260914/annular-compatible-h-evolution-independent-attempt01/status.json` — independent evolution/product/geometry checks.
- `scripts/replay_annular_augmented_error_balance_20260914.py` and `source-intake/navier-stokes/20260914/annular-augmented-error-balance-attempt01/status.json` — exact live energy-error balance replay.
- `source-intake/navier-stokes/20260914/annular-compatible-h-evolution-final-integrity.json` — final authority; require state=complete and all checks passing.
