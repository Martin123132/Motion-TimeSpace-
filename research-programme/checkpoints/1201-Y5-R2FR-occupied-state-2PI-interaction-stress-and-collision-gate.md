# 5185 - Occupied-state 2PI interaction stress and collision gate

Marker: `MTS_5185_OCCUPIED_STATE_2PI_INTERACTION_STRESS_COLLISION_GATE`.

Date: `2026-07-23`.

## Decision

Checkpoint 5184 rejected a regular classical stationary motion background but
left the occupied two-point state alive. Checkpoint 5185 now derives the
interaction stress of that state from the parent-owned essential `X^2/X^3`
vertices. It does not write down a phenomenological response kernel.

```text
THE_PARENT_ESSENTIAL_X2_AND_X3_VERTICES_DO_GENERATE_AN_EXACT_DIFFEOMORPHISM_CONSERVING_OCCUPIED_STATE_2PI_STRESS_THE_FIRST_HARTREE_PACKET_IS_LOCAL_AND_ITS_METRIC_AND_GAP_VARIATIONS_ARE_FIXED_GAUSSIAN_MOMENT_POLYNOMIALS_THE_FIRST_GENUINELY_NONLOCAL_X2_BASKETBALL_HAS_THE_EXACT_ALL_CROSS_TOPOLOGY_EIGHT_I2_SQUARED_PLUS_SIXTEEN_I4_AND_CAN_SUPPORT_A_CONSERVING_COLLISION_KERNEL_AFTER_CTP_CONTINUATION_BUT_THE_FREE_VLASOV_SUSCEPTIBILITY_MUST_BE_SUBTRACTED_BECAUSE_IT_WAS_ALREADY_EVOLVED_THE_SOURCE_LOCKED_IR_COEFFICIENTS_BOUND_THE_NEW_HARTREE_OPERATOR_NORM_BELOW_FOUR_TIMES_TEN_TO_THE_MINUS_116_AND_THE_MOST_GENEROUS_COHERENT_ACCUMULATION_OVER_TEN_TO_THE_18_SECONDS_BELOW_SIX_TIMES_TEN_TO_THE_MINUS_101_THE_INDEPENDENT_TWO_TO_TWO_COLLISION_EXPOSURE_IS_BELOW_TEN_TO_THE_MINUS_281_EVEN_AT_THE_LARGEST_LOCKED_MASS_THE_KNOWN_INTERACTING_STATE_STRESS_THEREFORE_HAS_THE_RIGHT_WARD_AND_VACUUM_STRUCTURE_BUT_CANNOT_MOVE_THE_GALAXY_PROFILE_AN_UNKNOWN_O2_COEFFICIENT_WOULD_REQUIRE_AN_UNCONTROLLED_TEN_TO_THE_28_ENHANCEMENT_TO_REACH_AN_ORDER_ONE_SIXPOINT_KERNEL_SO_IT_IS_NOT_A_CONTROLLED_RESCUE_THE_NEXT_CONSTRUCTIVE_TARGET_IS_SOURCE_SELECTION_OF_THE_NEUTRAL_OCCUPIED_STATE_FROM_THE_PARENT_TIME_DEPENDENT_CTP_BOGOLIUBOV_KERNEL
```

The outcome has one structural success and one quantitative failure:

```text
Ward-conserving, vacuum-silent interaction stress = derived;
strength needed for galactic redistribution       = absent by >100 orders.
```

## 1. State variable and renormalized scope

Let the finite occupied-state gradient covariance be

```text
C_mn(x)
 =[nabla_m nabla_n' F_state(x,x')]_(x'=x),

A^m_n=g^ma C_an,
t_n=Tr(A^n).
```

`C_mn` is the Hadamard/vacuum-subtracted finite state part. Other covariant
subtraction schemes differ by local vacuum counterterms already assigned to
the parent `P(X)` trajectory. The state-dependent functional is

```text
Delta Gamma_2[F]
 =Gamma_2[G_vac+F]-Gamma_2[G_vac]-local counterterms,
```

so every state interaction contribution vanishes exactly when `F=0`. The
checkpoint-4960 local GR/Newton/Maxwell vacuum is therefore not reopened.

## 2. Exact Gaussian Hartree functional

For a Gaussian reflection-even state, the moment-generating function gives

```text
<X^2> = M2 = t1^2+2t2,

<X^3> = M3 = t1^3+6t1t2+8t3.
```

The first 2PI/Hartree interaction density is therefore

```text
L_H
 =c2(t1^2+2t2)
  +c3(t1^3+6t1t2+8t3),

c2=A2 G_N^2,
c3=A3 G_N^4.
```

This is an action result, not an equation-of-state ansatz.

## 3. Exact Hilbert stress

Define

```text
C1_mn=C_mn,
C2_mn=C_ma g^ab C_bn,
C3_mn=C_ma g^ab C_bc g^cd C_dn.
```

At a stationary 2PI propagator, the implicit metric variation of `G` drops
out. Explicit variation gives

```text
Theta2_mn
 =c2[
    4t1 C1_mn
   +8C2_mn
   -g_mn(t1^2+2t2)
   ],

Theta3_mn
 =c3[
    (6t1^2+12t2)C1_mn
   +24t1C2_mn
   +48C3_mn
   -g_mn(t1^3+6t1t2+8t3)
   ].
```

Two exact algebraic checks are useful:

```text
Theta2^m_m=0,
Theta3^m_m=2c3 M3
```

in four dimensions. A `5000`-
sample independent directional finite-difference test gives maximum relative
residual
`2.276e-14`.

## 4. Exact Hartree gap tensor

The same functional, varied with respect to `C_mn`, gives

```text
Z_H^mn
 =g^mn
  +4c2[t1g^mn+2C^mn]
  +6c3[
      (t1^2+2t2)g^mn
     +4t1C^mn
     +8(C2)^mn
     ].
```

Thus the Hartree stress and state propagation are not independently tunable.
The packet is local in the coincidence covariance. Its direct metric Hessian
is a contact term. Its indirect response dresses the free susceptibility:

```text
chi_H=(1-chi0 f_H)^-1 chi0,

Delta chi
 =chi_H-chi0
 =chi0 f_H(1-chi0 f_H)^-1 chi0.
```

Checkpoint 5171 already derived and evolved `chi0`, the classical Vlasov
piece. Only `Delta chi` is new.

## 5. First genuinely nonlocal 2PI topology

For the `X^2-X^2` basketball define

```text
D_mn'(x,y)=nabla_m^x nabla_n'^y G(x,y),

I2=Tr[g_x^-1 D g_y^-1 D^T],

I4=Tr[(g_x^-1 D g_y^-1 D^T)^2].
```

The 24 Wick contractions in which all four lines cross between the two
vertices sum exactly to

```text
8 I2^2+16 I4.
```

The Euclidean cumulant magnitude is therefore

```text
Gamma_2,basketball
 =-4c2^2 integral_(x,y)[I2^2+2I4],
```

with the retarded/noise components obtained by the standard CTP continuation.
This is the first genuinely nonlocal self-energy and `2<->2` collision
kernel. The explicit combinatorial check over
`128` random cross-covariances
has maximum relative residual
`4.133e-14`.

The `X^3`, `X^2` exchange and curvature-completed six-point vertices similarly
generate `2<->4` and inverse collision kernels. Checkpoint 4959 already proves
that their known amplitude is nonzero.

## 6. Ward identity, compensation and double counting

A covariant Phi-derivable 2PI truncation satisfies

```text
delta Gamma/delta G=0,
delta Gamma/delta <psi>=0

 => nabla_mu T^mu_nu=0.
```

The collision kernel therefore has the correct energy-momentum zero mode and
can in principle produce a compensated redistribution. This is a real
structural hit.

Explicitly, its `2<->2` projection has the standard parent-amplitude form

```text
C_22[f1]
 =integral dPi_234
   delta^4(p1+p2-p3-p4)|M_22|^2
   [f3f4(1+f1)(1+f2)-f1f2(1+f3)(1+f4)].
```

Multiplication by `p1^nu`, integration over `p1`, and relabelling incoming
and outgoing legs gives

```text
integral dPi_1 p1^nu C_22[f1]=0
```

exactly because the four-momentum delta function sets
`p1+p2-p3-p4=0`. The `2<->4` channel does not conserve particle number, but
the same argument conserves total four-momentum. The required compensation
is therefore structurally available; only its rate remains to be tested.

It does not authorize adding the checkpoint-5171 kernel again:

```text
Pi_total=Pi_free/Vlasov+Pi_Hartree+Pi_basketball+Pi_collision,

Pi_new=Pi_total-Pi_free/Vlasov.
```

The free term was already evolved nonlinearly in checkpoints 5164--5169.
Scoring it twice would be a false improvement.

## 7. Source-locked physical size

The endpoint coefficients and conservative four-dimensional covariance-norm
bounds are:

| scheme | `c2` (`eV^-4`) | `c3` (`eV^-8`) | `||delta Z||` ceiling |
|---|---:|---:|---:|
| dynamic `eta_N` | -7.283939259579509e-111 | 1.323733110599660e-223 | 3.492540005516476e-116 |
| reference `eta_N=0` | -7.207628856092619e-111 | 1.323733096741495e-223 | 3.455950307618521e-116 |

The bounds use

```text
||delta Z_X2|| <=24 |c2| rho,
||delta Z_X3|| <=288|c3|rho^2,

||Theta_X2||/rho <=48|c2|rho,
||Theta_X3||/rho <=480|c3|rho^2.
```

The maximum source-locked results are

```text
interaction kinetic norm ceiling
 =3.492540005516476e-116,

Hartree stress fraction ceiling
 =6.985080011032952e-116,

required transition correction
 =1.644003838438572e+00.
```

The `X^2` calculation independently reproduces the checkpoint-5163
`8|c2|rho` envelope with maximum relative residual
`0.000e+00`.

The exact resolvent inequality gives

```text
||Delta chi||/||chi0||
 <=epsilon_H/(1-epsilon_H),
```

which is numerically the same tiny order. The interaction has the right
conservation structure but cannot generate the required profile amplitude.

## 8. Time accumulation and collision bound

To avoid dismissing a small instantaneous term that might accumulate, use the
deliberately generous exposure

```text
T=1e18 s,
omega_max=m_gap/hbar.
```

The Duhamel interaction phase ceiling is

```text
epsilon_H omega_max T
 <=5.306102337726383e-101
```

across all three locked masses. Galactic orbital frequencies are much smaller
than `m_gap/hbar`, so this overstates rather than understates the available
evolution.

An independent particle estimate uses the conservative derivative-amplitude
bound

```text
|M_2to2|<=64|c2|m^4,

sigma_2to2
 <=(256/pi)c2^2 m^6,

Gamma<= (rho/m) sigma v,
v<=1.
```

The largest exposure is

```text
log10(N_collisions per particle)
 <=-281.881979211639532.
```

This is not a marginal failure. Neither coherent Bose-enhanced mean-field
evolution nor incoherent two-body scattering can move an order-one fraction
of the state.

## 9. The open O2 coefficient is not a controlled rescue

Checkpoint 4959 leaves the `O2` momentum coefficient as a separate flow
calculation. Its natural co-leading reference is `W_O2/g^2` near `2.85`.
The directly measured `O2` projector Gram norm gives the exact coefficient
needed for a unit **O2-only** integrated kernel:

```text
W_O2/g^2
 ~1.335831664599493e+29.
```

The minimum enhancement over the natural co-leading reference is
`4.689488579429405e+28`. That is more than
28 orders and would destroy the perturbative derivative hierarchy. The exact
`O2` flow remains useful for theory completeness, but it is not a controlled
galaxy rescue and is not promoted here.

## 10. Route decision and next derivation

```text
Gaussian Hartree moments and stress               = derived;
Hartree gap tensor                                = derived;
X2 nonlocal basketball topology                   = derived;
Ward conservation and compensated zero mode       = retained;
vacuum silence                                    = exact state difference;
free Vlasov susceptibility                        = subtracted as already counted;
known X2/X3 interaction strength                   = decisively insufficient;
unknown O2 as controlled rescue                    = rejected;
local GR/Newton/Maxwell zero state                 = retained;
galaxy or full-MTS claim                           = false.
```

The next constructive target is checkpoint 5186: derive the neutral
occupied-state normalization and primordial covariance from the parent's
time-dependent CTP/Bogoliubov kernel. Neutral pair production can populate
total occupation without producing the signed `U(1)` charge rejected at
checkpoint 5157. The calculation must predict `beta_k`, abundance and
covariance for the three locked masses without fitting `Y_X`, `C_n` or a
galaxy profile.

## 11. Audit

All `34` validations pass. Every evidence row
remains `valid_for_claim=false`. The protected `formalization-workbench`
digest remains `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758` and the
checkpoint-5176 ensemble remains
`254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b`. No GitHub action occurred.

Generated files:

- `source-intake/functional_rg/5185/gaussian_2PI_Hartree_moments_stress_and_kinetic_tensor.csv`
- `source-intake/functional_rg/5185/X2_basketball_nonlocal_topology.csv`
- `source-intake/functional_rg/5185/Ward_vacuum_and_Vlasov_subtraction_ledger.csv`
- `source-intake/functional_rg/5185/parent_interaction_physical_bounds.csv`
- `source-intake/functional_rg/5185/interaction_time_and_collision_bounds.csv`
- `source-intake/functional_rg/5185/occupied_state_interaction_route_decision.csv`
- `source-intake/functional_rg/5185/source_provenance.csv`
- `source-intake/functional_rg/5185/occupied_state_2PI_interaction_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5185_VALIDATION.csv`
