# 5186 - FLRW Bogoliubov neutral-vacuum production and abundance no-go

Marker: `MTS_5186_FLRW_BOGOLIUBOV_NEUTRAL_VACUUM_PRODUCTION_GATE`.

Date: `2026-07-23`.

## Decision

Checkpoint 5185 selected the time-dependent Bogoliubov route because the
stationary interaction route is dynamically inert. This checkpoint carries that
route through the actual checkpoint-5156 mode operator and the three
checkpoint-5157 masses. It does not stop at saying that a state is missing.

```text
THE_CHECKPOINT_5156_PARENT_HESSIAN_REDUCES_DEEP_IN_RADIATION_DOMINATION_TO_ONE_UNIVERSAL_MODE_EQUATION_U_KAPPA_DOUBLE_PRIME_PLUS_KAPPA_SQUARED_PLUS_Y_SQUARED_TIMES_U_KAPPA_EQUALS_ZERO_THE_HALF_LINE_CONFORMAL_HAMILTONIAN_GROUND_STATE_AND_THE_EXACT_SYMMETRIC_ADIABATIC_CROSSING_BOTH_PRODUCE_FINITE_REFLECTION_EVEN_NEUTRAL_SQUEEZED_PAIRS_WITH_NO_FITTED_GALAXY_PARAMETER_BUT_THE_LARGER_OF_THEIR_PRESENT_ABUNDANCES_IS_BETWEEN_EIGHTY_NINE_AND_NINETY_SIX_ORDERS_BELOW_THE_LOCKED_OMEGA_X_TARGET_FOR_ALL_THREE_MASSES_FINITE_START_AND_ADIABATIC_ORDER_TESTS_CONFIRM_THAT_THE_INFRARED_COVARIANCE_DEPENDS_ON_A_VACUUM_OR_COSMOGENESIS_BOUNDARY_LAW_WHILE_THE_ULTRAVIOLET_NUMBER_INTEGRAL_IS_CONVERGENT_THE_FREE_FLRW_PARENT_THEREFORE_TRANSFERS_ANY_CHOSEN_STATE_BUT_DOES_NOT_SELECT_THE_REQUIRED_NEUTRAL_OCCUPATION_NORMALIZATION_AN_ARBITRARILY_SQUEEZED_STATE_OR_THE_CHECKPOINT_5152_MISALIGNMENT_AMPLITUDE_CAN_SUPPLY_OMEGA_X_ONLY_AS_INITIAL_STATE_DATA_SO_THE_VACUUM_PRODUCTION_ROUTE_IS_REJECTED_AS_THE_ABUNDANCE_OWNER_AND_THE_GALAXY_OCCUPIED_STATE_IS_DEMOTED_TO_AN_EXPLICIT_CONDITIONAL_COSMOLOGICAL_INITIAL_CONDITION_UNLESS_A_SEPARATE_PARENT_OWNED_NONADIABATIC_COSMOGENESIS_EVENT_IS_DERIVED
```

The result is constructive but negative:

```text
neutral Bogoliubov pair spectrum     = derived;
Gaussian pair covariance             = derived after a boundary choice;
Omega_X normalization from free FLRW = rejected by 89--96 orders;
unique vacuum/cosmogenesis boundary  = not supplied by the parent action.
```

This is not a no-go against every possible cosmogenesis sector. It is a no-go
against assigning the required abundance to the currently locked free FLRW
Hessian or to stationary visible-matter/Poynting noise.

## 1. Parent mode equation

Checkpoint 5156 gives the canonical minimally coupled motion mode

```text
v_k''+[k^2+a^2 m_gap^2-a''/a]v_k=metric-constraint source.
```

For the neutral vacuum-production branch `bar(psi)=0`. The mixed quadratic
Hessian vanishes exactly,

```text
delta^2 S/(delta g_mn delta psi)|_bar(psi)=0=0,
```

because the scalar Hilbert stress begins at order `(delta psi)^2`. The
`metric-constraint source` is therefore zero for the free production mode;
metric response re-enters through the `h psi psi` vertex already derived in
checkpoint 4952.

All three locked masses begin coherent oscillation deep in radiation
domination. The largest source-computed transition shift is only
`9.301897e-05` in `H`, and the largest
non-radiation fraction at `H=m_gap` is
`2.435547e-04`. Therefore the
source-backed leading production problem has

```text
a(eta)=s eta,
s=H0 sqrt(Omega_r),
a''=0,

v_k''+[k^2+m^2 s^2 eta^2]v_k=0.
```

Define

```text
a_osc=sqrt(s/m),
y=a/a_osc=sqrt(m s) eta,
kappa=k/sqrt(m s),
u_kappa=(m s)^(1/4) v_k.
```

The complete mass dependence factors out:

```text
u_kappa,yy+(kappa^2+y^2)u_kappa=0.
```

This universal reduction reproduces every locked `a_osc` row with maximum
relative residual `0.000e+00`.

## 2. Half-line radiation prescription

One parameter-free but non-parent-owned boundary prescription is the
instantaneous conformal Hamiltonian ground state at the radiation boundary:

```text
u_kappa(0)=1/sqrt(2 kappa),
u_kappa,y(0)=-i kappa u_kappa(0).
```

At late adiabatic time,

```text
u_kappa=alpha_kappa f_kappa+beta_kappa f_kappa*,
|alpha_kappa|^2-|beta_kappa|^2=1,
n_kappa=|beta_kappa|^2,
|c_kappa|^2=n_kappa(n_kappa+1).
```

The numerical Wronskian residual is at most
`4.990e-08`. The spectrum has controlled
integrable ends:

```text
kappa -> 0:      n_kappa ~ 0.238944065/kappa,
kappa -> infinity: n_kappa ~ 1/(64 kappa^8).
```

The universal comoving number coefficient is

```text
I_half = integral_0^infinity dkappa kappa^2 n_kappa
       = 0.0295135357473,

C_half = I_half/(2 pi^2)
       = 0.00149517318769.
```

The result is stable over projection times `y=15--30`; their fractional spread
is below `2e-5`.

## 3. Exact analytic crossing check

A second calculable comparator extends the same oscillator smoothly from
`y=-infinity` to `y=+infinity` and chooses the adiabatic in-vacuum. Its exact
Landau-Zener/Schwinger spectrum is

```text
n_kappa=exp(-pi kappa^2),

I_sym=1/(4 pi),
C_sym=1/(8 pi^3)=0.00403144180415.
```

The numerical quadrature reproduces the analytic integral with fractional
residual
`3.570e-07`.
The smooth negative-to-positive `y` extension is not part of the MTS parent, so
this is a cross-check rather than a hidden cosmogenesis axiom.

## 4. Vacuum and start-time robustness

Finite-start WKB-0 prescriptions span coefficients

```text
2.246590035e-05
 <= C_start <=
0.00354024826478.
```

The spread is real: low-`kappa` modes have no parent-selected adiabatic region.
At the radiation boundary the first adiabatic diagnostic vanishes, but the
second behaves as `omega''/omega^3=1/kappa^4`; at finite start the first
diagnostic is also nonadiabatic in the infrared. The action fixes the transfer
operator and Wronskian, not the infrared density matrix.

The ultraviolet conclusion is cleaner. Replacing the order-zero initial
frequency by

```text
W_2(0)=kappa-1/(4 kappa^3)
```

suppresses the high-`kappa` tail, while the integrated abundance verdict is
unchanged because the target shortfall is almost ninety orders even at the
largest mass.

## 5. Three-mass abundance

For any universal spectrum coefficient `C_n`,

```text
k_star=sqrt(m s)=m a_osc,
n_0=C_n k_star^3,
rho_0=m n_0,
rho_osc=C_n m^4.
```

The locked target is

```text
rho_X0=3 Omega_X Mbar_Pl^2 H0^2,
Omega_X=0.2657568086361595.
```

| Mass row | `m_gap` (eV) | `k_star` (Mpc^-1) | largest declared vacuum / target | required enhancement |
|---|---:|---:|---:|---:|
| `ten_times_WKB_floor` | `2.816692e-21` | `30.6501` | `8.748509e-96` | `1.143052e+95` |
| `benchmark_1e_minus20_eV` | `1.000000e-20` | `57.7514` | `2.077714e-94` | `4.812982e+93` |
| `benchmark_1e_minus18_eV` | `1.000000e-18` | `577.514` | `2.077714e-89` | `4.812982e+88` |

The largest target fraction is only
`2.077714e-89`. Even the
most favorable locked mass therefore requires at least
`4.812982e+88` times more occupation than
the largest declared vacuum-production comparator. This is not a tunable
order-one coefficient problem.

The scalings independently verify the reduction:

```text
n_0 proportional to m^1.5,
rho_0 proportional to m^2.5,
rho_osc proportional to m^4.
```

## 6. What survives

The produced state is a valid neutral, reflection-even, pure squeezed Gaussian
state. It preserves the checkpoint-5158 charge result and can enter the
checkpoint-5185 conserved 2PI stress. What fails is its normalization:

```text
correct tensor and Ward structure = yes;
enough particles for Omega_X      = no;
unique low-k covariance           = no.
```

An arbitrary finite Hadamard infrared squeeze can mathematically fill the
abundance, and the checkpoint-5152 homogeneous amplitude can do the same.
Neither is generated by the current action. Calling either one derived would
only rename initial-state data.

## 7. Route disposition

The occupied-state galaxy branch remains internally usable as a conditional
cosmological branch:

```text
input: one global abundance/amplitude datum plus a declared primordial
       covariance;
transfer: parent FLRW Hessian, radiation transfer, Vlasov/SP evolution and
          conserved Hilbert stress;
claim ceiling: no parent-derived dark-sector abundance or covariance.
```

The only re-entry route for a derived abundance is a real parent-owned
nonadiabatic cosmogenesis event with a specified background, in-vacuum or
density matrix, and no fitted `Omega_X`. No reheating field or transition is
invented here.

## 8. Reproduction

Run:

```powershell
& "D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\.venv-score\Scripts\python.exe" "D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_5186_FLRW_Bogoliubov_neutral_vacuum_production_and_abundance_gate.py"
```

Outputs:

- `source-intake/functional_rg/5186/universal_radiation_Bogoliubov_spectrum.csv`
- `source-intake/functional_rg/5186/three_mass_Bogoliubov_spectra.csv`
- `source-intake/functional_rg/5186/three_mass_vacuum_abundance_gate.csv`
- `source-intake/functional_rg/5186/vacuum_prescription_and_start_time_sensitivity.csv`
- `source-intake/functional_rg/5186/adiabatic_UV_and_background_robustness.csv`
- `source-intake/functional_rg/5186/neutral_Gaussian_covariance_gate.csv`
- `source-intake/functional_rg/5186/neutral_source_selection_route_decision.csv`
- `source-intake/functional_rg/5186/source_provenance.csv`
- `source-intake/functional_rg/5186/FLRW_Bogoliubov_neutral_production_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5186_VALIDATION.csv`

Locked local inputs:

- `checkpoint_4952_document`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4952-Y5-R2FR-visible-matter-graviton-CTP-noise-kernel-to-motion-pair-source-and-frequency-support-or-composite-route-rejection.md`
- `checkpoint_5152_document`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\5152-Y5-R2FR-primordial-motion-occupation-dust-limit-Jeans-window-and-formation-source-arbitration.md`
- `checkpoint_5152_background`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5152\primordial_motion_background.csv`
- `checkpoint_5156_document`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\5156-Y5-R2FR-FLRW-Hessian-Gaussian-state-single-clock-adiabatic-radiation-transfer-and-patch-collapse-gate.md`
- `checkpoint_5156_Hessian`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5156\FLRW_parent_Hessian_reduction.csv`
- `checkpoint_5157_masses`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5157\three_mass_state_preparation_numbers.csv`
- `checkpoint_5158_document`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\5158-Y5-R2FR-clock-charge-source-symmetry-no-go-and-neutral-state-pivot.md`
- `checkpoint_5185_document`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\5185-Y5-R2FR-occupied-state-2PI-interaction-stress-and-collision-gate.md`

Primary references:

- Parker particle creation: https://link.aps.org/doi/10.1103/PhysRev.183.1057
- Gravitational relic-production methodology: https://arxiv.org/abs/hep-ph/9802238
- Planck parameter source inherited through 5152/5156: https://arxiv.org/abs/1807.06209

All validation rows pass. The formalization workbench and checkpoint-5176
ensemble remain locked. No GitHub action occurred.
