# 4953 - Formation spectrum, `X2` kinetic cascade and local-injection decision

Date: 2026-07-13

Marker: `MTS_FORMATION_X2_CASCADE_LOCAL_INJECTION_DECISION_4953`.

Status: private analytic, primary-source-locked, symbolically derived and
data-executed checkpoint. This checkpoint performs the cascade calculation
selected at 4952. It does not merely report an unknown redistribution rate.
The leading on-shell `X2` collision kernel is now exact, and its collision
invariants prove that it cannot multiply a high-frequency pair population
into the enormous number of galaxy-profile quanta. The proof holds for every
value of `c_ess`. Finite-time/off-shell number change and direct
profile-frequency formation emission remain separate, explicitly bounded
routes. The 4947 stationary local GR/Newton/Maxwell branch is retained.

## 1. Exact `X2` scattering kernel

Checkpoint 4941 reduced the gravity-generated four-derivative scalar block to
the essential coordinate

```text
L_int=c_ess X^2=(c_ess/4)(partial psi . partial psi)^2,
c_ess=c+8 pi g(ctilde+d),
beta_c,ess|0=16g^2.
```

The beta function proves that gravity generates the coordinate; it does not
fix its infrared value. Differentiating the interaction four times gives the
massless identical-scalar amplitude

```text
M_22=(c_ess/2)(s^2+t^2+u^2).
```

In the centre-of-mass frame,

```text
t=-s(1-cos theta)/2,
u=-s(1+cos theta)/2,
M_22=c_ess s^2(3+cos^2 theta)/4.
```

Including the identical-final-state factor and integrating the full angular
kernel gives

```text
sigma_22
 =(1/2) int dOmega |M_22|^2/(64 pi^2 s)
 =7 c_ess^2 s^3/(320 pi)
 =7 c_ess^2 E^6/(5 pi),       s=4E^2.
```

With `M=16 pi sum_l(2l+1)a_l P_l`, the s-wave is

```text
a_0=5 c_ess s^2/(96 pi).
```

Tree-level perturbative unitarity therefore requires

```text
|c_ess|s^2<=48 pi/5,
|c_ess|E^4<=3 pi/5             for head-on equal-energy quanta.
```

These coefficients were derived with SymPy and independently recomputed by
the validator. The massless limit is the most permissive redistribution case;
a motion gap only adds thresholds.

## 2. Covariant collision integral and exact invariants

In the on-shell quasiparticle and leading-gradient limit, the 4952 source and
the `X2` collision term enter as

```text
p^mu nabla_mu f_1=C_cov,22[f_1]+S_pair,1,

C_cov,22[f_1]
 =(1/2!) int dPi_2 dPi_3 dPi_4
   (2pi)^4 delta4(p_1+p_2-p_3-p_4) |M_22|^2
   [(1+f_1)(1+f_2)f_3f_4
    -f_1f_2(1+f_3)(1+f_4)].
```

The displayed `1/2!` is for identical final quanta. Conventions that move
common factors between `C_cov` and coordinate time do not affect the
invariants. Relabeling incoming and outgoing variables gives, for any weight
`W`,

```text
int dPi_1 W_1 C_cov,22
 proportional to
 int dPi_1...dPi_4 delta4 |M_22|^2
 [W_3+W_4-W_1-W_2] [gain-loss].
```

Hence

```text
W=1:      int dPi C_cov,22=0,
W=p^nu:   int dPi p^nu C_cov,22=0.
```

The leading `X2` Boltzmann kernel conserves both quasiparticle number and
stress energy for every `c_ess`, occupancy and Bose enhancement. It can
isotropize or exchange momentum; it cannot turn a small number of energetic
pairs into the required huge number of low-energy quanta. Its stationary
Bose distribution may retain a nonzero chemical potential, which is the same
failure seen in the source 2PI-to-Boltzmann comparison.

This is exact only for the declared on-shell `2<->2` kernel, not for the full
quantum theory. A single `X2` vertex has no generic on-shell number-changing
cut: `0->4` is energy-forbidden, massive `1->3` is below threshold, and the
massless collinear set has zero phase-space measure and `s=t=u=0`. The first
generic on-shell multiplier is two-vertex `2->4`:

```text
M_24~c_ess^2 E^6,
sigma_24/sigma_22~O[(c_ess E^4)^2].
```

Finite-time and finite-width `1<->3` terms exist before the quasiparticle
limit. They are not rejected by the collision-invariant theorem and require a
full off-shell 2PI kernel rather than an inserted cascade law.

## 3. Formation-spectrum number bound

Insert a time-dependent formation stress spectrum into the already-derived
4952 parent kernel:

```text
dGamma
 =(kappa^4/16)(1/2!)dPi dPi'
   [V P S_m^em(q) P V]/|q^2+i0|^2.
```

If `omega` is the total angular frequency carried by a pair, its emitted
energy and quantum-number moments obey

```text
dE_psi=hbar omega dN_pair,
dN_quanta=2 dE_psi/(hbar omega).
```

For a target profile quantum

```text
E_R=hbar c/R,
```

any number-conserving redistribution obeys the source-independent ceiling

```text
N_final/N_R
 <=int [2E_R/(hbar omega)] dE_psi/E_required.
```

For monochromatic injection with one-quantum energy `E_inj`,

```text
F_N<=min(1,E_R/E_inj).
```

Even free cosmological redshift cannot increase particle number. Granting the
entire recombination-to-present expansion, much more than is available after
galaxy formation, gives

```text
z_star=1089.92,
A_max=1+z_star=1090.92,
F_N,redshift<=min(1,A_max E_R/E_inj).
```

The value is taken from the Planck 2018 parameter table. It is deliberately
used as an upper envelope, not as an MTS cosmological fit.

## 4. Public 175-galaxy execution

The source-locked 4949 occupation diagnostic contains `175` public outer LTG
rows, of which `173` have a positive outer residual target. Six injection
energies were tested per row:

```text
direct E_R;
minimum 4952 high-harmonic profile pair;
J2211+1136 white-dwarf fundamental pair quantum;
716-Hz neutron-star fundamental pair quantum;
1 GeV;
10^20 eV.
```

All `692=173x4` positive-target high-frequency rows fail even after the full
`A_max=1090.92` redshift grant. Representative required stretch ranges are

```text
white dwarf:   3.26482e9  to 4.98046e11;
neutron star:  1.64381e14 to 2.50762e16;
1 GeV:         1.11025e35 to 1.69368e37;
10^20 eV:      1.11025e46 to 1.69368e48.
```

Direct injection at `E_R` passes the number gate on all `173` positive
targets. The minimum exact 4952 support harmonic also has
`E_inj/E_R=1.00000014...1.00048214`, so it passes the number/redshift gate.
That is not a cascade rescue: it returns to the unresolved formation-stress
amplitude at harmonics of order `10^3-10^4`.

Thus the result is sharp:

```text
high-frequency formation + X2 2-to-2 cascade = rejected;
direct profile-frequency formation emission   = still open.
```

## 5. Natural coefficient and compact comparison

For orientation only, take the deliberately generous gravitational Wilson
comparator

```text
|c_ess|=1/Mbar_Pl^4,
Mbar_Pl=2.435e27 eV.
```

This is not the solved MTS infrared coefficient. The interaction-strength
coordinate is `g_X2=|c_ess|E^4`. Even at `10^20 eV`,

```text
g_X2=2.84449e-30,
sigma_22=1.40398e-113 m^2,
sigma_24/sigma_22~8.09111e-60
```

before four-body phase-space suppression. Across the positive galaxy rows,
the maximum ten-gigayear secular comparator

```text
|c_ess| rho_psi omega_R t
```

is `4.31230e-108`. The coefficient required merely for an order-one nonlinear
phase has median `14.3142 eV^-4`, corresponding to a median derivative-EFT
cutoff of `0.514112 eV`; even such a large coefficient cannot evade the exact
`2->2` number invariant.

For a deliberately maximal local challenge, the script assigns `100%` of the
uniform-sphere rotational energy to motion modes for the sourced white dwarf
and the `716-Hz`, `16-km`, high-mass neutron-star comparator. This is not an
emission claim. It asks what source-efficiency hierarchy a universal
coefficient would require. The natural secular comparators are

```text
white dwarf: 5.76485e-75,
neutron star: 2.32582e-58.
```

If galaxy and local systems had equal injection efficiencies, no universal
coefficient is strong on any positive galaxy phase scale while weak on either
compact comparator. The median necessary local-to-galaxy injection-efficiency
ceilings are

```text
epsilon_WD/epsilon_gal <3.44705e-37,
epsilon_NS/epsilon_gal <8.54397e-54.
```

These are conditional source-calibration requirements, not observational
bounds: the assumed local `100%` conversion is intentionally extreme. A
surviving off-shell source must derive the suppression rather than assign it.

## 6. Decision

```text
exact massless X2 2-to-2 amplitude             = derived;
exact sigma_22 and s-wave unitarity domain     = derived;
on-shell C_22 number collision invariant       = exact;
on-shell C_22 stress collision invariant       = exact;
leading X2 multiplicity cascade                = rejected for every c_ess;
high-frequency injection plus maximal redshift = rejected on 692/692 rows;
direct profile-frequency formation source      = open amplitude calculation;
off-shell 1<->3 and on-shell 2->4              = open parent kernel;
Planck-natural X2 comparator                    = far too weak, not a coefficient proof;
equal-efficiency galaxy/local phase window      = false under maximal comparator;
4947 local GR/Newton/Maxwell branch             = retained;
full MTS galaxy unification                     = false.
```

This is a substantive route decision. The vague phrase "perhaps an `X2`
cascade" is no longer available. Only direct low-frequency formation
emission or a quantitatively derived off-shell number-changing kernel can
continue this composite route.

## 7. Artifacts

- `post-checkpoint-work/scripts/Y5_R2FR_4953_formation_X2_cascade_and_injection_gate.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4953_formation_X2_cascade_and_injection_validation.py`
- `post-checkpoint-work/source-intake/functional_rg/4953/PROVENANCE.md`
- `post-checkpoint-work/source-intake/functional_rg/4953/formation_X2_cascade_and_injection_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4953/X2_scattering_kernel.csv`
- `post-checkpoint-work/source-intake/functional_rg/4953/X2_collision_invariant_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4953/formation_spectral_number_bound.csv`
- `post-checkpoint-work/source-intake/functional_rg/4953/SPARC_formation_injection_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4953/SPARC_X2_nonlinearity_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4953/local_compact_X2_injection_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4953/X2_number_change_scaling.csv`
- `post-checkpoint-work/source-intake/functional_rg/4953/formation_X2_composite_route_decision.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4953_VALIDATION.csv`

## Next target

`4954-Y5-R2FR-finite-time-off-shell-X2-number-changing-2PI-kernel-and-formation-source-efficiency-or-nonequilibrium-route-rejection.md`

Derive the finite-time/off-shell `1<->3` memory kernel and the first on-shell
`2<->4` number-changing contribution from the parent `X2` vertex. Contract the
result with the 4952 formation stress source and enforce the 4953 galaxy/local
efficiency ceilings. Reject the remaining formation route if its universal
coefficient cannot generate the required number within formation time without
an inserted local switch. Do not revive the now-rejected `2<->2` cascade.
