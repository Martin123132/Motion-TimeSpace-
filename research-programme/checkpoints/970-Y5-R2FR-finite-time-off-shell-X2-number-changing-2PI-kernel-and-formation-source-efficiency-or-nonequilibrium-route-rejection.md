# 4954 - Finite-time `X2`, mandatory `X3` and number-change decision

Date: 2026-07-13

Marker: `MTS_OFFSHELL_X2_X3_NUMBER_CHANGE_DECISION_4954`.

Status: private analytic, primary-source-locked, independently reproducible
and data-executed checkpoint. This checkpoint calculates the finite-time
number-changing route left open at 4953. It derives the pre-Boltzmann memory
channels, a UV-finite smooth-preparation bound, the complete leading
tree-level `2->4` amplitude structure, and the controlled formation envelope.
It rejects neither arbitrary strongly off-shell dynamics nor direct
profile-frequency formation emission. The stationary 4947 local
GR/Newton/Maxwell branch remains unchanged.

## 1. What finite time restores

The source-locked three-loop 2PI derivation contains four sign channels before
the infinite-time and on-shell reductions:

```text
I:    0<->4, DeltaE=Ep+Eq+Ek+Es,
II:   1<->3, DeltaE=Ep+Eq+Ek-Es,
III:  2<->2, DeltaE=Ep+Eq-Ek-Es,
IV:   3<->1, DeltaE=Ep-Eq-Ek-Es.
```

For a preparation interval `T=t-t0`, every channel carries

```text
K_T(DeltaE)=int_0^T du cos(DeltaE u)=sin(DeltaE T)/DeltaE,
|G_T(DeltaE)|^2=4 sin^2(DeltaE T/2)/DeltaE^2.
```

Only channel III survives the strict infinite-time on-shell limit. This
reconstructs the precise loophole in the 4953 collision-invariant theorem:
finite preparation admits transient `0<->4` and `1<->3`, while a finite
spectral width admits persistent number change. The source also makes a
necessary distinction: merely retaining finite `t0` after imposing a
quasiparticle ansatz does not restore the full off-shell theory. A genuinely
broad state requires the unequal-time 2PI equations.

The 4952 source and the self-energy remain separate terms,

```text
p^mu nabla_mu f=C_2PI[f]+S_pair.
```

Thus a memory kernel redistributes or multiplies what the parent source emits;
it does not manufacture the still-unsolved formation stress spectrum.

## 2. Smooth `1<->3` preparation bound

A sharp switch is not an admissible prediction for the derivative theory. For
a box interval, `|G_T|^2~DeltaE^-2`; at fixed incoming energy and large final
momentum `Lambda`, the `X2` derivative vertex leaves a radial tail proportional
to

```text
c_ess^2 E Lambda^6 dLambda.
```

The result is UV divergent and depends on the unphysical switch. It cannot be
used as a formation enhancement.

Use instead the declared smooth preparation

```text
g(t)=exp[-t^2/(2 tau^2)],
|g_tilde(DeltaE)|^2=2 pi tau^2 exp[-tau^2 DeltaE^2].
```

For three massless near-collinear daughters with `sum_i x_i=1` and
`sum_i k_perp,i=0`, expansion about the on-shell collinear surface gives

```text
DeltaE=sum_i |k_perp,i|^2/(2 x_i E),
M_13=2 g_X2 Ahat/(E tau)^2,
g_X2=c_ess E^4.
```

The second equation is the derivative-interaction Adler/collinear zero. The
four-transverse-dimensional quadratic form has

```text
det M_2=1/(x1 x2 x3),
int_0^infinity r^11 exp(-r^4/4)dr=32.
```

Its whitening Jacobian cancels the apparent simplex singularity. The resulting
single-preparation probability is

```text
P_13=C_13 g_X2^2/(E tau)^4+O[(E tau)^-6],
C_13=<Ahat^2>/(24 pi^3).
```

Four independently scrambled `2^18`-point Sobol integrations give

```text
<Ahat^2> = 0.00451408802205 +/- 1.18e-7,
C_13     = 6.06609438657e-6 +/- 1.58e-10.
```

Using the 4953 perturbative-unitarity ceiling `|g_X2|<=3pi/5`,

```text
P_13<=2.15531826678e-5/(E tau)^4.
```

This is a controlled finite-preparation statement. A persistent width
`delta=Gamma/E<<1` has the same derivative suppression per coherence interval,
`Delta N~C_13 g_X2^2 delta^4`. Taking `delta~1` exits the quasiparticle
expansion rather than producing a controlled large answer.

## 3. First on-shell multiplier and mandatory `X3`

The first generic on-shell number-changing process has six external legs. Two
`X2` vertices produce ten unordered `3+3` exchange partitions,

```text
M_6,exchange
 =sum_(10 partitions A|B)
   V4(A,-K_A)V4(B,K_A)/K_A^2.
```

But this is not the complete amplitude at that derivative order. The next
shift-symmetric parent coordinate

```text
L_3=d_3 X^3=d_3(partial psi . partial psi)^3/8
```

contributes the contact term

```text
M_6,contact
 =6 d_3 sum_(15 perfect matchings)
   (ki.kj)(kk.kl)(km.kn).
```

Both `d_3` and `c_ess^2` have mass dimension `-8`, so omitting `d_3` would be
an inconsistent parent truncation. With

```text
r_3=d_3/c_ess^2,
Phi_4(s)=s^2/(24576 pi^5),
```

eight independently scrambled `2^16`-event massless RAMBO integrations give,
under the declared amplitude and identical-final-state normalization,

```text
sigma_24=c_ess^4 E^14 [C0+C1 r_3+C2 r_3^2],
C0= 2.02036932285e-6,
C1=-2.09476933861e-6,
C2= 5.44434863692e-7.
```

The phase-integrated minimum is

```text
r_3,min=1.92380161366,
C_min=5.40900592435e-9>0.
```

Thus the contact term can strongly interfere but cannot cancel the entire
integrated tree rate. For the exchange piece alone,

```text
sigma_24/sigma_22
 =4.53369815872e-6 g_X2^2.
```

These coefficients are deterministic QMC estimates, not claimed closed-form
constants. Their role is more important than their last digits: the leading
number-changing calculation exposes a new parent-owned coordinate instead of
permitting a one-parameter `c_ess` cascade.

## 4. Formation and local execution

The 1050 source-locked 4953 injection rows were re-evaluated. For each galaxy,

```text
tau_dyn=R/v,
y=E_inj tau_dyn/hbar,
M_remaining=max[1,(E_inj/E_R)/1090.92].
```

All `692` positive-target high-frequency rows fail the Gaussian preparation
bound. The largest probability is `3.12564424478e-58`, while the smallest
required logarithmic multiplicity is `14.9116937188`.

A second deliberately generous controlled-EFT envelope was then applied. With
the one-shell occupancy proxy

```text
f_shell=2 pi^2 rho_psi/E_inj^4,
```

the high-occupancy branch enforces the derivative-background condition
`|c_ess|rho_psi<=1`, and the dilute branch grants a unit dimensionless
six-point amplitude:

```text
high occupancy: log G_N<=2y min(1,E^4/rho_psi)^2,
dilute:         log G_N<=2(rho_psi/E^4)y.
```

This envelope is far more permissive than the calculated exchange rate. Its
largest high-frequency value is nevertheless only `0.0386923108`; all
`692/692` rows remain below their required multiplicity. The result rejects
the controlled perturbative/background route, not an arbitrary
nonperturbative six-point spectral function.

For the sourced compact comparators, a single smooth preparation over ten
gigayears gives

```text
white dwarf P_13<=5.45521e-70,
neutron star P_13<=8.48875e-89.
```

A periodic stationary object is not a repeated sudden switch. Persistent
compact emission therefore remains part of the same full spectral 2PI problem
and must still respect the 4953 galaxy/local efficiency hierarchy.

## 5. Decision

```text
finite-time four-channel 2PI kernel             = derived;
sharp-switch enhancement                        = rejected as UV-sensitive;
smooth finite-preparation 1<->3 route           = rejected on 692/692 rows;
two-X2 on-shell 2->4 exchange                   = derived;
mandatory same-order X3 contact                 = derived and parent-unsolved;
controlled high-frequency six-point route       = rejected on 692/692 rows;
strong nonquasiparticle X2-X3 2PI route          = open;
direct profile-frequency formation amplitude    = open;
4947 local GR/Newton/Maxwell branch              = retained;
full MTS galaxy unification                      = false.
```

This checkpoint is forward movement rather than another missing-input ledger:
it closes both controlled number-changing escapes left by 4953 and identifies
the exact next parent coordinate. The surviving route is narrower and harder:
the parent must predict the full six-derivative shift sector, including `d_3`,
and that flow must justify a genuinely broad nonequilibrium spectral state.

## 6. Artifacts

- `post-checkpoint-work/scripts/Y5_R2FR_4954_offshell_X2_X3_number_change_gate.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4954_offshell_X2_X3_number_change_validation.py`
- `post-checkpoint-work/source-intake/functional_rg/4954/PROVENANCE.md`
- `post-checkpoint-work/source-intake/functional_rg/4954/offshell_X2_X3_number_change_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4954/finite_time_2PI_preBoltzmann_kernel.csv`
- `post-checkpoint-work/source-intake/functional_rg/4954/gaussian_13_collinear_coefficient.csv`
- `post-checkpoint-work/source-intake/functional_rg/4954/gaussian_13_collinear_QMC_replicates.csv`
- `post-checkpoint-work/source-intake/functional_rg/4954/X2_X3_24_amplitude_completion.csv`
- `post-checkpoint-work/source-intake/functional_rg/4954/X2_X3_24_phase_space_QMC_replicates.csv`
- `post-checkpoint-work/source-intake/functional_rg/4954/SPARC_finite_time_and_controlled_24_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4954/local_compact_offshell_preparation_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4954/offshell_X2_X3_route_decision.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4954_VALIDATION.csv`

## Next target

`4955-Y5-R2FR-six-derivative-shift-sector-X3-parent-flow-and-number-changing-fixed-ratio-or-strong-2PI-route-rejection.md`

Derive the full parent six-derivative shift-symmetric scalar block and its
flow, including the coefficient `d_3` that enters the six-point amplitude at
the same order as `c_ess^2`. Determine whether a GR-connected trajectory fixes
`r_3=d_3/c_ess^2` and remains inside a controlled spectral domain. Only if the
parent predicts a broad state should the full unequal-time `X2-X3` 2PI system
be solved. Do not fit `d_3`, insert a width, or revive the closed finite-time
routes.
