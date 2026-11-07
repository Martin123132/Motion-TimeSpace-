# Stage228: particle-owned thermodynamic stress over the saved history

## Scope and provenance

This extends the existing thermal source, not the parent action or the MTS
branch. Stage70 supplies the retained two-field/Friedmann response; Stage75
explicitly approximated the gas as nonrelativistic. Its collision electrons
already have a normalized classical Maxwell-Juttner distribution. The owners
are kernel_common.py:juttner_rule and kinetic_common.py:gas_rule, named in
SOURCES.md. No new population, fitted coefficient or scattering bank is used.

Default calculation: relativistic electrons, the inherited ideal
nonrelativistic H/He ion heat, fully ionized fixed abundances and shared T.
Ion Juttner corrections are a separately labelled extension, evaluated only
as a size diagnostic using the inherited m_H/m_He4 mass convention. Those
constants are atomic masses; they are not claimed to be exact bare-ion
masses. There is no ion momentum population in the electron scattering bank
from which an exact relativistic ion EOS could already have been inferred.
Neither option includes Coulomb interaction free energy, recombination,
quantum degeneracy, pairs or an independently established thermalization rate.

## 1. Stress and heat capacity from the retained electron measure

In the gas rest frame, theta=k_B T/(m c^2), gamma=sqrt(1+p^2/(m c)^2),

    f(p)=n exp(-gamma/theta)/(4 pi (mc)^3 theta K_2(1/theta)).

Use d^3p for number; the stress moments are energy mc^2 gamma and
p^2 c^2/(3 mc^2 gamma). With y=(gamma-1)/theta, the normalized radial
measure is proportional to

    y^(1/2) exp(-y) (1+theta y) sqrt(2+theta y) dy.

This is exactly the saved electron quadrature's measure. Its normalization
follows from the modified-Bessel integral representation. Differentiating
the partition integral at fixed n and mass gives

    u/(nmc^2)=h(theta)=K_1(1/theta)/K_2(1/theta)+3theta-1,
    P=n k_B T,
    c_V/k_B=h'(theta)=Var(gamma)/theta^2=Var(y)>0.

The pressure identity follows independently by integrating the momentum
derivative of p^3 exp(-gamma/theta); the endpoint terms vanish. Thus the
first relativistic correction is in heat, NOT an extra pressure at fixed T.
The EOS describes kinetic heat only; gas rest energy is already in the
retained parent's baryon density and must not be added a second time.

The Bessel expansion gives

    h(theta)=3theta/2+15theta^2/8-15theta^3/8+O(theta^4),
    c_V/k_B=3/2+15theta/4-45theta^2/8+O(theta^3).

The code evaluates these quantities by normalized moments, without subtracting
nearly equal rest energies. Bessel formulas at high precision and a separate
adaptive quadrature check the implementation. These are classical kinetic
identities, not new MTS predictions; their value is making the existing MTS
source interface internally consistent.

## 2. Mixture variables and exact conservation law

Retain s=ln(a/a_start), T_star=T0/a, R=T/T_star, rho_star proportional to a^-4,
and chi=(3/2)n_total k_B T_star/rho_star. Let f_j=n_j/n_total be fixed.
Define

    A(s,R)=(2/3) sum_j f_j h_j(theta_star,j R)/theta_star,j,
    C(s,R)=A_R=(2/3) sum_j f_j h_j'(theta_star,j R),
    A_s at fixed R=A-R C,
    u=chi rho_star A,       P_g=(2/3)chi rho_star R.

NR species have h_j=3theta/2 exactly within that approximation. In particular
A=C=1 at R=1 in the old leading gas model, and generally A=R, C=1.
Write the photon energy rho_gamma=rho_star(1+chi E). The combined heat source
relative to the parent's cold gas/reference radiation is

    q=delta rho/rho_star=chi(E+A),
    p=delta P/rho_star=chi(E/3+2R/3).

The exact homogeneous first law for this EOS is

    E_s+C R_s=(C-2)R,
    q_s-q+3p=0.

It follows from n c_V dT/dt=-3H P_g-Q_gamma and the photon energy equation;
the collision energy transfer cancels, not the gas pressure or initial heat.
Setting R=1+chi g, C=1 recovers the existing gas equation, including its -1
expansion source. A temperature-dependent C changes that gas equation; it
cannot be inserted into Friedmann while leaving the old photon energy untouched.

## 3. A conserved leading source, with initial heat preserved

At leading heat order use R=1, not as an exact thermal-equilibrium axiom but
as the explicit leading member of the saved expansion R=1+O(chi).
Set D(s)=A(s,1)-1. Then delta C=D-D_s. Relative to Stage70,

    delta E(s)=D(0)-D(s)+integral_0^s D(v) dv,
    delta q(s)=chi[D(0)+integral_0^s D(v) dv],
    delta p(s)=chi[D(0)-D(s)+integral_0^s D(v) dv]/3.

The initial gas energy chi D(0) remains. Photon correction starts at zero.
The leading electron coefficient is derived, not fitted:

    D(s)=D0 exp(-s)+O(theta_start^2),
    D0=(5/4) f_e theta_start,
    delta q=chi D0(2-exp(-s)),
    delta p=(2/3)chi D0(1-exp(-s)).

Therefore the combined correction does NOT disappear when photon/gas exchange
is summed. It also does not equal the instantaneous excess gas energy alone.
It is positive throughout this history for the classical electron population.

The same exact conservation completion works along an explicitly prescribed
saved R(s) if D=A(s,R)-R. It requires delta E_s=(C-1)(R-R_s).
That is a conditional energy-completed stress diagnostic, NOT a claim that
the old photon spectrum and R solve the new kinetic equation. A new coupled
solution is the next verification if this term matters. The leading R=1
source is what is propagated here. Saved-R completion ranks the lag correction.

## 4. Reuse the finite-capacity history without cancellation

For the original nonrelativistic gas, E+chi g+W=0 and W_s=1+chi g.
Hence q_heat=chi(1-W); Stage70's q=chi(1-s), p=chi(2-s)/3 includes initial heat.
With I=integral g ds, the finite-capacity contribution is

    delta q_capacity=-chi^2 I,
    delta p_capacity=chi^2(g-I)/3.

Recover I using exactly the saved backward-Euler startup/BDF2 recurrence.
Do not obtain a subleading chi^2 signal by subtracting two float64 O(chi)
answers. Compare an independently integrated piecewise-linear g history and
the saved work/energy balance; report numerical defects separately.
This ranks the capacity term, not a complete second-order gravity result.

## 5. Source coupling to the retained parent

The external q,p above are conserved. For fixed parent field initial data,
the existing homogeneous linear response obeys

    xi=delta Hc/Hc=(rho_star q+sum(pi delta pi/a^2+m^2 phi delta phi))/(2rho0),
    delta phi_s=delta pi/Hc-pi xi/Hc,
    delta pi_s=-2delta pi-a^2 m^2 delta phi/Hc+a^2 m^2 phi xi/Hc.

These are the Stage70 equations, not a newly fitted metric rule. Propagate
normalized source shapes separately so a chi theta correction is not lost in
subtraction. Parent heavy/cold and NR/EOS-corrected sources receive identical
settings. The original Stage70 response is an independent saved limit check.
Initial delta phi=delta pi=0 does NOT imply xi(0)=0: initial heat sources
Friedmann. Independent incoming field/metric perturbations remain additive.

Numerical convergence and signed finite-amplitude variations test this
retained response; they do not independently establish the parent action.

## 6. Local scalar-wave source rows, ready for the same gravity equations

At fixed species fractions, delta_b=delta n/n, delta r=delta R, and
J=ik v+S (S is the scalar spatial expansion rate in synchronous coordinates),

    delta u=chi rho_star(A delta_b+C delta r),
    delta P=(2/3)chi rho_star(R delta_b+delta r),
    B_g=(rho_rest+chi rho_star[A+2R/3])/rho_star.

For photon energy transfer Q_gamma and its perturbation delta Q_gamma,
conformal-time linearization of the SAME gas first law gives

    delta r'=[Hc-2Hc/C-(C_R/C)(R'-Hc R)]delta r
             -2R J/(3C)-(delta Q_gamma-Q_gamma delta_b)/(chi rho_star C),
    B_g v'=-C_F-B_g'v-ik delta P/rho_star.

These reduce to Stage75 at C=1. The density term follows from perturbing
the number of gas particles, not from an optional coupling. Gas stress plus
photon stress cancels the common energy/momentum transfer, preserving the
existing constraint-propagation route. This stage derives/tests the local
thermodynamic rows algebraically; it does not rerun the full scalar wave.
