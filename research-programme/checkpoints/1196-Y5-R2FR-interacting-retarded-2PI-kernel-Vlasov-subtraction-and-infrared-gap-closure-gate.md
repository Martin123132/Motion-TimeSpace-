# 5180 - Interacting retarded 2PI kernel, Vlasov subtraction and infrared gap-closure gate

Marker: `MTS_5180_INTERACTING_RETARDED_2PI_VLASOV_SUBTRACTION_GAP_GATE`.

Date: `2026-07-23`.

## Decision

This checkpoint performs the interaction calculation left open at 5179. The
trajectory-normalized `X2-X3` retarded CTP kernel is now explicit, the
collisionless Vlasov response is subtracted algebraically, and the remaining
collision and spectral pieces are tested against the checkpoint-5149
requirement

```text
1-zeta(k) proportional |k|.
```

The result is sharper than a weak-rate failure. Every field in the
shift-symmetric `X2` and `X3` vertices is differentiated. Consequently every
two-point self-energy constructed from them obeys the exact external-leg
identity

```text
Sigma_X2-X3(p)=p_mu p_nu Pi^mu_nu(p).
```

If the occupied state clusters exponentially, `Pi` is analytic at zero
momentum. The interactions can then renormalize kinetic coefficients but
cannot generate an additive gap cancellation or an `|k|` term. The controlled
interaction repair is closed. A genuinely critical occupied state remains
possible only if the parent derives the required power-law correlation tail;
that state is not claimed here.

## 1. Exact `X2-X3` CTP kernel

For

```text
L_int=(c_ess/4)(partial psi.partial psi)^2
     +(e_ess/8)(partial psi.partial psi)^3,
```

functional differentiation gives

```text
V4=2 c_ess sum_(3 pairings)(p_i.p_j)(p_k.p_l),
V6=6 e_ess sum_(15 pairings)
          (p_i.p_j)(p_k.p_l)(p_m.p_n).
```

The coefficients follow from `2^2 2! (c_ess/4)=2c_ess` and
`2^3 3! (e_ess/8)=6e_ess`; they are not fitted.

The 2PI hierarchy through the first nonlocal graph is

```text
Gamma2_X2,H=(1/8) integral_C V4 G G,
Gamma2_X2,B=(1/48) integral_C V4(x) G(x,y)^4 V4(y),

Gamma2_X3,H=(1/48) integral_C V6 G G G,
Gamma2_X3,B=(1/1440) integral_C V6(x) G(x,y)^6 V6(y).
```

Opening one line produces self-energy factors `1/6` and `1/120`. In the
equal-coordinate shorthand used by the primary 2PI source,

```text
Sigma_F,4
 =-(V4 V4/6)[F^3-(3/4)F rho^2],

Sigma_rho,4
 =-(V4 V4/6)[3 rho F^2-(1/4)rho^3],

Sigma_F,6
 =-(V6 V6/120)
   [F^5-(5/2)F^3 rho^2+(5/16)F rho^4],

Sigma_rho,6
 =-(V6 V6/120)
   [5 rho F^4-(5/2)rho^3 F^2+(1/16)rho^5],

Sigma_R=theta(x0-y0) Sigma_rho.
```

The full momentum kernels retain the derivative vertices and sum the distinct
placements of `F` and `rho`. The displayed coefficients are generated
directly from `(F-i rho/2)^n` and `(F+i rho/2)^n`.

At first order `X3` changes the four-leg kernel only through

```text
V4_bar=V4+(1/2)Tr_G V6+...,
```

where `choose(6,2)4!/6!=1/2`. The mixed `c_ess e_ess` basketball is therefore
inside `V4_bar^2`; the first direct nonlocal `X3` self-energy has five
internal lines.

In vacuum the three-line and five-line cuts begin at `3m_gap` and `5m_gap`.
An occupied medium admits low-frequency scattering cuts, but these must be
split into collisionless transport and an interacting residual before they
can be counted as new physics.

## 2. Exact Vlasov subtraction

Write the Wigner equation as

```text
(partial_t+v.grad_x+F.grad_p)f=C22[f]+... .
```

With

```text
R0=[-i omega+L_Vlasov]^-1,
RC=[-i omega+L_Vlasov+C22]^-1,
```

the new interacting response is not `RC`; checkpoint 5171 and the nonlinear
particle evolution already contain `R0`. The exact remainder is

```text
RC-R0=-RC C22 R0.
```

A rational three-state collision Laplacian verifies this identity with
exact residual `0` and
verifies `C22 1=0` with exact residual
`0`. This is an algebra
check, not a fit.

Checkpoint 4953 supplies the continuum invariants

```text
integral dPi C22=0,
integral dPi p^nu C22=0.
```

Detailed balance also gives `C22[f_BE]=0`. Collisions relax nonconserved
distortions and alter finite-frequency widths; they do not select a new static
equilibrium distribution or manufacture missing source stress. The fixed
UGC09133 Vlasov benchmark has dielectric eigenvalue
`0.55222325794240468`, below its static pole.

## 3. Infrared theorem

Let the equal-time projected connected stress kernel obey

```text
|C_TT(r)|<=C0 exp(-r/xi).
```

All moments are finite, so dominated convergence gives

```text
chi(k)=chi0+chi2 k^2+chi4 k^4+... .
```

The exact benchmark

```text
C(r)=C0 exp(-r/xi)
```

has

```text
chi(k)=8 pi C0 xi^3/(1+k^2 xi^2)^2
      =chi0[1-2(k xi)^2+3(k xi)^4-...].
```

The executed low-momentum departure slope is
`1.9999832907953505`, converging to `2`, whereas
checkpoint 5149 requires slope `1`. Even an exact cancellation of the `k^2`
coefficient leaves `k^4`, not `|k|`.

The surviving state target is now concrete. In three spatial dimensions, a
nonlocal determinant term proportional to `|k|` corresponds, after contact
subtraction, to an equal-time `r^-4` kernel. The checkpoint-5149
susceptibility `C_q~mu/|k|` corresponds to an `r^-2` tail. A future state
derivation must produce those tails, not merely a large local coefficient.

## 4. Quantitative occupied-state bound

The dynamic-`N=8` trajectory normalization is

```text
c_ess=-7.2878119824619069e-111 eV^-4,
r3=e_ess/(2 c_ess^2)=12474921.033335365
```

in the checkpoint-4957/4958 convention. Across all
`173` positive-target SPARC rows,

```text
max |c_ess| rho
 =2.5585013084621188e-115,

min local enhancement needed for the locked fraction
 =3.9942868661138966e+114,

max |e_ess rho^2|/|c_ess rho|
 =2 r3 |c_ess rho|
 =6.3834203573500277e-108.
```

For a narrow high-occupancy shell, checkpoint 4953 gives

```text
sigma22=7 c_ess^2 E^6/(5 pi),
rho~f E^4,
Gamma22~(f E^3) sigma22 f,
Gamma22/E~[7/(5 pi)](c_ess rho)^2.
```

The second factor of `f` is the generous final-state Bose stimulation. For
the profile comparison, grant the microscopic frequency `E=m`, which is much
larger than the profile streaming quantum, and replace the exact angular
coefficient by a general finite controlled coefficient:

```text
Gamma_coll/m=C_coll (c_ess rho)^2.
```

Using the profile streaming frequency `omega_profile` and granting the unit
coefficient comparator,

```text
max Gamma_coll/omega_profile
 =7.2676450871045508e-224.
```

Closing the locked deficit would require

```text
C_coll>=1.4061484911334452e+223.
```

The exact two-body angular coefficient is finite,
`7/(5 pi)=0.44563384065730693`, and the full
controlled phase-space kernel cannot provide a
coefficient of this magnitude. If occupation correlations make such a
coefficient effectively divergent, the calculation has left the controlled
quasiparticle branch and entered precisely the strong critical-state route.

## 5. Scope

```text
first nonlocal X2 retarded kernel                 = derived;
first direct nonlocal X3 retarded kernel          = derived;
CTP F/rho coefficients                            = derived exactly;
collisionless Vlasov response                     = subtracted exactly;
collision number and four-momentum zero modes     = retained exactly;
regular clustering X2-X3 gap closure              = rejected;
regular clustering |k| determinant                = rejected;
controlled collision/static repair                = rejected quantitatively;
parent-derived critical occupied state             = open, not claimed;
local GR/Newton/Maxwell branch                     = unchanged;
galaxy bridge or full MTS                          = not claimed.
```

Route decision:
`THE_TRAJECTORY_NORMALIZED_X2_X3_CTP_KERNEL_HAS_NOW_BEEN_WRITTEN_EXPLICITLY_THE_X2_BASKETBALL_AND_X3_FIVE_LINE_GRAPHS_ARE_THE_FIRST_NONLOCAL_SELF_ENERGIES_AND_THEIR_STATISTICAL_SPECTRAL_POLYNOMIALS_ARE_FIXED_BY_CTP_COMBINATORICS_AFTER_SUBTRACTING_THE_ALREADY_COUNTED_VLASOV_RESOLVENT_THE_REMAINING_COLLISION_OPERATOR_ANNIHILATES_NUMBER_AND_MOMENTUM_MODES_AND_IS_PARAMETRICALLY_TOO_SMALL_MORE_STRONGLY_SHIFT_SYMMETRY_FORCES_AN_EXTERNAL_MOMENTUM_ON_EACH_SELF_ENERGY_LEG_SO_ANY_REGULAR_EXPONENTIALLY_CLUSTERING_OCCUPIED_STATE_PRODUCES_ONLY_AN_ANALYTIC_K_SQUARED_SERIES_AND_CANNOT_ERASE_A_GAP_OR_GENERATE_THE_REQUIRED_ABSOLUTE_K_DETERMINANT_THE_PERTURBATIVE_INTERACTION_REPAIR_IS_THEREFORE_CLOSED_WHILE_A_PARENT_DERIVED_CRITICAL_STATE_WITH_THE_REQUIRED_POWER_LAW_TAIL_REMAINS_OPEN_AND_NOT_CLAIMED`.

The next calculation is not another weak loop. Construct the smallest
positive parent-derived critical occupied state compatible with the complete
even boundary hierarchy, calculate its equal-time and retarded stress kernel,
and test:

1. the `r^-4` determinant-tail coefficient and `r^-2` susceptibility tail;
2. the checkpoint-5149 unit-mixing normalization;
3. the full metric-motion spectral and gradient eigenvalues;
4. formation from the parent without an inserted occupation law.

If no such state exists, the galaxy bridge cannot come from the present
single shift-symmetric motion-scalar realization.

All `36` validation rows pass. The protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758` and checkpoint 5176 remains
`254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b`. No GitHub action occurred.
