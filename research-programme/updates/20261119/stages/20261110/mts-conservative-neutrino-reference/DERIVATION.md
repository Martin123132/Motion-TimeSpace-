# A conservative thermal-neutrino reference from one distribution

## Scope and origin

This is a numerical representation of the retained collisionless thermal
neutrino sector, shared by cold and MTS calculations. It is not an MTS
population prescription, a new interaction or a refit of cosmological data.
The distribution below approximates, rather than equals, the continuous
Fermi-Dirac distribution. The production action, bank and grids are untouched.

The preceding mts-residual-species-budget-20261110 stage checked the actual
native full momentum hierarchy and derived its source defect. Its
DERIVATION.md and check_neutrino.py establish the conventions used here;
neutrino-prediction-result.json checks them against captured native rows.
The upstream numerical definitions are in
condensate-origin-20261003/native-heavy-matching-20261007/native/fortran/massive_neutrinos.f90.
Those paths are relative to post-checkpoint-work and are verified in the seal.

Use conformal time, c=1, and scaled stresses 8 pi G a^2 times physical
stress. H means conformal H, not the physical expansion rate. H and k
have units Mpc^-1; scaled stresses have units Mpc^-2. Let q be dimensionless
comoving momentum, mu=a m_nu/T_nu0, epsilon=sqrt(q^2+mu^2), and
C=7 pi^4/120. The common normalization A below has units Mpc^-2 and is
inherited, not fitted. Neither m_nu nor T_nu0 is changed by the construction.

## One positive distribution, not two unmatched integrations

For fixed positive nodes q_i and weights B_i define

    f_h(q) = 4C sum_i [B_i/q_i^4] Theta(q_i-q),
    -f_h'(q) = 4C sum_i [B_i/q_i^4] delta(q-q_i).

The derivative is distributional. Integrals, not pointwise slopes at a jump,
define its stress moments. For a monotone thermal f, the reference rule

    B_i = w_i q_i^4 [-f'(q_i)]/(4C)

approximates f(q)=integral_q^infinity [-f'(s)] ds with positive quadrature.
Here f(q)=1/(exp(q)+1). Positivity of B_i gives a nonnegative monotone
f_h; its maximum is 4C sum B_i/q_i^4, checked against the fermionic
occupation upper bound 1. This check alone does not make f_h exactly thermal.

The native five-node rule is also tested as supplied, including its REAL32
literal promotion. No normalization or weight is adjusted to cancel a
measured residual. Separate Gauss rules use 16,32,64 nodes on [0,60],
fixed before testing. Their finite upper tail is part of the numerical
approximation and is included in comparison with continuum integration
over [0,infinity).

## Density, pressure and derivatives

Define

    I_rho(q,mu) = integral_0^q s^2 sqrt(s^2+mu^2) ds
      = [q epsilon(2q^2+mu^2)-mu^4 asinh(q/mu)]/8,
    I_p(q,mu) = integral_0^q s^4/sqrt(s^2+mu^2) ds
      = [q epsilon(2q^2-3mu^2)+3mu^4 asinh(q/mu)]/8,
    T(q,mu) = integral_0^q mu^2 s^4/(s^2+mu^2)^(3/2) ds
      = mu^2 q epsilon/2 -3mu^4 asinh(q/mu)/2 +mu^4 q/epsilon.

At mu=0, both I integrals are q^4/4 and T=0. At small q/mu,
shell_model.py uses convergent binomial series to avoid subtracting large
nearly equal terms. Independent 60-decimal integration checks both sides
of that switch. On this Windows runtime numpy.longdouble has only a
52-bit explicit significand: it is not presented as extended precision.

With calligraphic names suppressed, the dimensionless moments are

    R_h = 4 sum B_i I_rho(q_i,mu)/q_i^4,
    P_h = (4/3) sum B_i I_p(q_i,mu)/q_i^4,
    S_h = R_h+P_h = (4/3) sum B_i epsilon_i/q_i.

Their analytic log-mass derivatives are

    mu dR_h/dmu = R_h-3P_h,
    mu dP_h/dmu = -(4/3) sum B_i T(q_i,mu)/q_i^4,
    mu dS_h/dmu = (4/3) sum B_i mu^2/(q_i epsilon_i).

Physical scaled moments are R=A R_h/a^2, P=A P_h/a^2.
Because mu'=H mu and a'=H a, these imply exactly

    R' = -H(R+3P).

This identity is valid for any fixed positive shell rule. Accurate
approximation to the thermal continuum is a SEPARATE test; conservation
cannot rescue an inaccurate coarse rule.

## The same distribution supplies the perturbation source

Use the retained linear multipole normalization, represented on the shell
support by delta f=-(q f_h'/4) F. Then its source moments are

    d_i=A B_i/(a^2 v_i), j_i=A B_i/a^2, p_i=A B_i v_i/a^2,
    v_i=q_i/epsilon_i,
    D=sum d_i F0_i, Q=sum j_i F1_i,
    P_pert=(1/3)sum p_i F0_i, Pi=sum p_i F2_i.

Thus j_i^2=d_i p_i,
d_i'=-H(1+v_i^2)d_i, j_i'=-2Hj_i. The already checked native collisionless
monopole/dipole equations are

    F0_i'=-k(4z/3+v_i F1_i),
    F1_i'=k v_i(F0_i-2F2_i)/3.

Substitution, for arbitrary multipoles, gives

    D'+H(D+3P_pert)+kQ+kzS = kz[S-(4/3)sum d_i],
    Q'+2HQ-kP_pert+(2k/3)Pi = 0.

Now S=A S_h/a^2=(4/3)sum d_i follows from f_h, so the energy defect
vanishes identically as well. It is not declared zero or subtracted after
measurement. Eight primitive/background identities and five kinetic
identities are symbolically checked; manufactured multipoles and a
one-sided weight mutation test the implementation separately.

This statement concerns the full collisionless momentum hierarchy used
by the retained capture, not a fluid closure or relativistic-tail switch.
It does not validate an angular truncation or the entire coupled evolution.

## Relativistic and nonrelativistic limits

At mu=0, R_h=sum B_i and P_h=R_h/3. For mu much larger than all nodes,

    R_h/mu -> (4/3)sum B_i/q_i,
    mu P_h -> (4/15)sum B_i q_i.

The first coefficient is the represented particle-number normalization.
Its quadrature error is not permission to retune the physical mass or
abundance. A production bridge must expose any normalization convention
inherited from the native mass/density initialization.

## What transfers to the retained calculation

The mismatch mechanism is removed analytically for this shared reference.
It has not been removed from the saved production trajectories. Applying
it requires the same moments and derivatives in background H/H', slow-field
evolution, native source weights, and canonical carrier coefficients.
Mixing a shell source with the old spline background would reintroduce
exactly the inconsistency diagnosed in the preceding stage.

The new reference passes sampled continuum checks for both retained cold
and heavy backgrounds. These are not new galaxy/cosmology fits or a uniform
all-temperature error certificate. See RESULTS.md and NEXT.md for the
bounded production-interface test rather than another residual-polishing sweep.
