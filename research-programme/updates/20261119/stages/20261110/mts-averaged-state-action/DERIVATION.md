# Averaged phase-pressure action and its parent normalization

## 1. Retained equations, no new closure

Use conformal H=a'/a, mu=am, Fourier k>0, and the saved Newtonian metric
Phi,Psi. Let delta be the heavy proper energy-density contrast, u=theta/k,
and Pi=delta pressure/rho. The retained average has dust-like background
density and the specified linear pressure:

    r(k,a) = (k/mu)^2/(sqrt(1+(k/mu)^2)+1)^2,
    Pi = r(delta+3H u/k).
    delta' = -k u +3Phi' -3H Pi,
    u' = -H u +k(Psi+Pi).

These follow from the actual MTSTwoField.f90 averaged equations and the
established gauge map, not a new fit or a substitute galaxy law. In particular

    delta_N=delta_S-3H alpha, u_N=u_S+k alpha,
    alpha'+H alpha=Psi,
    k z = k^2 alpha-3Phi'-3H'alpha-3H alpha'.

The pressure combination is gauge invariant in this retained background.
The imported general gauge/conservation principles are those of
[Ma and Bertschinger 1995, section4](https://arxiv.org/html/astro-ph/9506072v1#S4).
The r coefficient and this specialization belong to the retained model,
not to that paper.

## 2. A quadratic action that generates the retained evolution

Set d=delta-3Phi and S=-mu u/k. Because mu'=H mu, metric time derivatives
drop out:

    R=d+3Phi-3H S/mu,
    d' = k^2 S/mu -3H r R,
    S' = -mu(Psi+r R).

The physical current and the energy contrast remain recoverable without a
small-phase expansion. An equation-level action for each real Fourier
quadrature is

    I_equations = integral [ S d' - K(d,S,tau) ] d tau,
    K = mu*r/2 * (d+3Phi-3H S/mu)^2
        + k^2/(2mu) * S^2 + mu*Psi*d.

Pure functions of time can be removed only with the same energy bookkeeping.
K has units inverse Mpc in the chosen normalization. A global density/volume
prefactor is not determined by solving the two evolution equations.

The unforced Hessian is

    G = [[mu*r, -3H*r],
         [-3H*r, (k^2+9H^2*r)/mu]].

Its determinant is k^2*r. At fixed coefficients, r>0 gives a positive-definite
matter Hessian and a stable oscillation with frequency

    Omega = k sqrt(r) = mu(sqrt(1+(k/mu)^2)-1).

This concerns the matter subsystem on a supplied metric, not a proof of
stability after self-gravitating metric feedback or nonlinear collapse.
For a cold classical control set r=0. Then K=k^2 S^2/(2mu)+mu Psi d;
the reference mu is only a velocity-potential scaling, and its dust equations
are independent of that convention.

At leading small k/mu and weak expansion corrections, r~k^2/(4mu^2).
The Hamiltonian reduces to the quadratic Madelung/Schrodinger energy,
but removing the H/metric terms changes the retained pressure source.

## 3. Check physical normalization against the parent, not just the equations

An equation-level action can be multiplied by a constant for each k without
changing its trajectories. That freedom cannot be used to calibrate physical
occupation. Pull back the canonical real-field pair instead.

For constant a and flat metric, use the conformally canonical real field
q=a*phi_parent (common parent normalization factors are understood). In the
following sideband equations the symbol phi denotes this q, not the
Planck-normalized field column in the saved packet. Use its
homogeneous carrier F cos(mu tau). A positive-frequency sideband of frequency
omega=sqrt(mu^2+k^2) has

    delta phi = F[R_b cos(mu tau)+I_b sin(mu tau)],
    delta pi  = F*omega[I_b cos(mu tau)-R_b sin(mu tau)],
    R_b'= (omega-mu) I_b, I_b'=-(omega-mu) R_b.

These are linear perturbations; spatial standing-wave normalization cancels
from the ratios below. Project quadratic cross terms onto the difference
frequency, explicitly discarding their sum-frequency component. This is the
specified fast-carrier projection, not the full instantaneous stress:

    delta = (omega+mu)/mu * R_b,
    Pi = (omega-mu)/mu * R_b = r delta,
    S = I_b.

The exact pulled-back symplectic form for that sideband is

    d(delta phi) wedge d(delta pi) = F^2*omega dR_b wedge dI_b
      = nbar * W(k) d(delta) wedge dS,
    nbar = mu F^2/2,
    W(k) = 2omega/(omega+mu) = 1+r.

The common homogeneous normalization is shown in these rescaled flat units.
It does not select the population of a halo. The ordinary canonical
annihilation-amplitude coordinates are

    Z = sqrt(omega/mu) (R_b+i I_b),
    Re Z = sqrt(1-r^2) delta/2,
    Im Z = sqrt(omega/mu) S.

Thus a density/velocity phase pair and a number-normalized canonical complex
amplitude agree only at leading NR order. Their distinction is derived from
the retained quadratic real field, without fitting a new coefficient.

In this flat setting the excitation Hamiltonian above the carrier is exactly

    K_parent/nbar = (omega-mu)|Z|^2 = W*K_equations.

Multiplying both the symplectic and Hamilton terms by W therefore matches the
flat parent. Correct dispersion alone would not have fixed this normalization.

## 4. Expansion exposes a specific matching condition

Instantaneously promoting the flat W to W(a,k) gives

    d r/d ln a = -2r/sqrt(1+(k/mu)^2),
    W'/W = -2H*r/[sqrt(1+(k/mu)^2)*(1+r)].

For any time-dependent linear variational system with symplectic form W*J,
preservation requires

    W' J + W(A^T J + J A)=0,
    trace(A)=-W'/W.

The retained (d,S) system has trace(A)=0. It therefore cannot also preserve
this *naively instantaneous* parent weight exactly when W' is nonzero.
This is a precise mismatch between that proposed state/action map and the
retained averaged closure, not a no-go theorem for the parent action.

Adding -(W'/2W) times the identity to A would fix the trace but would not
derive the correct physics: arbitrary traceless additions remain possible.
We do NOT do that. The next reduction must obtain the slow-time canonical
connection and fast/negative-frequency mixing from the real-field action.
Alternatively a rigorously bounded truncation may suffice for a declared
formation test. The present diagnostic quantifies a necessary matching
condition; it is not a total error bound.

The coefficient W-1=r and its rate follow from this flat/instantaneous
comparison. Curved-space metric-gradient terms are not determined by
multiplying the old -3Phi spatial-measure correction by a guessed filter.
The two corrections remain separately scoped.

## 5. Controlled propagation and work

For a short source-held probe use s=ln(a/a0), Delta s=.001,
H(s)=H0, Phi(s)=Phi0, Psi(s)=Psi0, a=a0 exp(s). This prescribed background
is not the full saved cosmology. Solve the fluid and Hamilton systems
independently with the same initial transfer states, not a fitted realization.

The explicit derivative at fixed d,S for this probe is

    partial_s K =
      mu*(r+partial_s r)*R^2/2 +3H*r*R*S
      -k^2*S^2/(2mu)+mu*Psi*d.

Hamilton evolution gives dK/ds=partial_s K. Work must accompany changing
coefficients; conserved energy is not expected on a varying background.
An implicit-midpoint step preserves the frozen mid-step quadratic Hamiltonian
and its symplectic map. Compare its refinement to independent DOP853 evolution.

No phase is replaced by1+iS. These are linear transfer states; evaluating
exp(iS) is a coordinate representation, not a derived nonlinear cosmological
completion. The current stage does not generate a galaxy or a random box.
