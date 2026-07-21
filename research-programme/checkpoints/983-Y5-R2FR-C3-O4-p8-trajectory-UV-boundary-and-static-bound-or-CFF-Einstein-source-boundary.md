# 4967 - `C3+O4` p8 trajectory, UV boundary and static compact bound

Date: `2026-07-13`.

**Canonical correction:** checkpoint 4969 proves that `B=v/g^3` requires
`beta_B=[6-3beta_g/g]B+source`, not `[4-2beta_g/g]B+source`. The C3/O4
source derivations remain retained, but the fixed boundary, `diag(4,4)`
statement and numerical trajectory in this file are superseded by 4969.

Marker: `MTS_4967_P8_GR_TRAJECTORY_AND_STATIC_BOUND`.

Status: private analytic, primary-source-locked and numerically executed
checkpoint. This checkpoint extends the existing `N=6,N=8` GR-connected
functional trajectories by the complete two-coordinate Ricci-flat `p8`
target and calculates every `C3` and `O4` source currently fixed by the
parent Hessian and primary on-shell amplitudes. It derives a UV-regular
source-truncated boundary and the resulting compact static correction. It
does not include the unprojected photon/`CFF` or three-loop pure-Einstein
`p8` sources, so it is not the full finite parent vector or full MTS.

## 1. Primary `C3 -> R4` source and exact MTS normalization

Baratella et al. define

```text
gamma_i=dC_i/d ln mu
```

and obtain at leading one loop

```text
dC_R4/d ln mu       =-C_R3/(8pi^2),
dC_R4prime/d ln mu  =0.
```

The second equality is a helicity selection rule, not an assumed zero. The
4965 action/amplitude normalization gives

```text
kappa^2=32piG,
M_P^2=1/(8piG),
kappa=2/M_P,

C_R3     =(3/(4pi)) A_C3,
C_R4     =B_minus/(128pi^3),
C_R4prime=B_plus /(128pi^3).
```

Therefore the exact transfer into the MTS p8 coordinates is

```text
dB_minus/d ln k=-12 A_C3,
dB_plus /d ln k=0,

dB_C/d ln k=-6 A_C3,
dB_t/d ln k=+6 A_C3.
```

Here `A_C3(k)=h_C3(k)/g(k)` is the running local coordinate in the locked
source scheme. It is not the finite subtracted `A_C3^S` by itself and is not
a complete local-plus-nonlocal physical amplitude.

## 2. Quadratic `O4` Wilsonian source

For a locally constant `Q=C_mnrs C^mnrs`, the canonically normalized scalar
Hessian inside the optimized Type-II cutoff is

```text
Delta_k=k^2+m_psi^2+2w_O4 Q p^2,
R_k/Z_psi=(k^2-p^2) theta(k^2-p^2).
```

The `Q^2` term in the Wetterich trace is

```text
2w_O4^2 Q^2 integral_[p<k]
 [2k^2-eta_psi(k^2-p^2)]p^4/(k^2+m_psi^2)^3.
```

Using

```text
I4=integral p^4=k^8/(64pi^2),
I6=integral p^6=k^10/(80pi^2),
```

gives the exact optimized-cutoff weight

```text
d c_Q2/dt
 =w_O4^2 k^4(1-eta_psi/10)
  /[16pi^2(1+m_psi^2/k^2)^3].
```

For `v_C=k^6b_C`, `B_C=v_C/g^3` and the massless 4957 trajectory,

```text
source(beta_vC)
  =g u_O4^2(1-eta_psi/10)/pi,

source(beta_BC)
  =u_O4^2(1-eta_psi/10)/(pi g^2),

source(beta_Bt)=0.
```

This is a Wilsonian power source. It is distinct from the massive logarithm
derived at 4966 and does not turn a subtraction convention into a physical
zero.

## 3. Extended p8 beta system and UV regularity

For either p8 coordinate `B_i=v_i/g^3`, the homogeneous flow is

```text
beta_Bi=[4-2 beta_g/g]B_i+source_i.
```

At the non-Gaussian fixed point `beta_g=0`. The p8 stability subblock is

```text
M_p8=diag(4,4).
```

Both directions are irrelevant in the convention used by the 4957
stability analysis. The source-truncated extension therefore adds no
relevant parameter, and regularity fixes

```text
B_C*=-(source_C3,C*+source_O4,C*)/4,
B_t*=-source_C3,t*/4.
```

All twelve fixed-point residuals are zero to floating-point precision. The
combined fixed values are approximately

```text
dynamic eta_N:
  B_C*= 2.92722171972e-5,
  B_t*=-4.50270541265e-5;

reference eta_N=0:
  B_C*= 2.93310148560e-5,
  B_t*=-4.50108727086e-5.
```

This removes an independent finite boundary only inside the declared
triangular `C3+O4` source truncation. An omitted source shifts the fixed
values without creating a new free coordinate if the positive p8
eigenvalues survive.

## 4. Four GR-connected integrations

The p8 system is integrated on the existing `N=6,N=8` dynamic-`eta_N` and
reference-`eta_N=0` trajectories. At `N=8`, the separate and combined
endpoints are

```text
                                     dynamic eta_N       reference eta_N=0
C3 only B_C                         0.0130633704101      0.0130627606840
C3 only B_t                        -0.0130633704101     -0.0130627606840
O4 squared only B_C                -1.33018662522e-5    -1.32768598047e-5
O4 squared only B_t                 0                    0
C3+O4 B_C                           0.0130500685321      0.0130494838053
C3+O4 B_t                          -0.0130633704013     -0.0130627606655
```

The combined helicity result is therefore approximately

```text
B_minus=0.0261134,
B_plus =-1.33e-5.
```

The `C3` source fills the same-helicity channel and `O4^2` fills both
helicity channels. Superposition is recovered numerically. The largest
combined `N=6 -> N=8` relative displacement is

```text
4.44154420413e-8.
```

The N8 scheme spread in `B_C`, `B_t` and `B_minus` is below `4.67e-5`.
The small `B_plus` difference is `1.88e-3` relative because that channel is
the difference of the two much larger `C3` coordinates; its absolute spread
is only `2.50e-8`.

## 5. Massive-threshold transfer law

The Bern-Kosmopoulos-Zhiboedov large-mass amplitudes are converted into one
common MTS transfer law for every supplied real minimally coupled spin:

```text
B_i^threshold=sum_s n_s c_i^(s)/(8pi mu_s^4),
mu_s=m_s l_P.
```

The exact rational `(c_C,c_t)` pairs are

```text
spin 0:   (11/75600,   1/75600),
spin 1/2: (47/302400,127/302400),
spin 1:   (1/700,     13/12600),
spin 3/2: (1217/151200,1297/151200),
spin 2:   (1009/7560, 251/1890).
```

This is now an exact spectrum-to-p8 map, not a placeholder. A numerical
total still requires the parent-owned masses and multiplicities.

## 6. Exact static compact correction

The 4966 Schwarzschild response is applied to the two N8 combined
endpoints:

```text
Delta A=128B_Cchi^3(8-11M/r),
Delta B=128B_Cchi^3(36-67M/r),
chi=l_P^2M/r^3.
```

Across all eleven inherited neutron-star, benchmark and black-hole rows,
the largest calculated source-truncated metric residual is

```text
9.23777701892e-234
```

on the near-turning SLY4 star. The corresponding one-percent exact-response
coefficient budget is

```text
|B_C|<1.41268494632e229,
```

so the candidate-to-budget ratio is `9.24e-232`. This enormous margin is a
consequence of Planck-curvature suppression, not evidence that every omitted
coefficient is zero.

## 7. Locality-safe motion-scalar threshold bound

For the minimal massive motion scalar,

```text
B_C^psi=11/(604800pi J_gap^2),
B_t^psi= 1/(604800pi J_gap^2),
J_gap=mu_psi^2.
```

Let

```text
rho=J_gap/chi.
```

The local large-mass expansion is controlled when `rho` is large. Direct
substitution into the exact static response eliminates the apparent
`1/J_gap^2` growth:

```text
Delta A_psi
 =[128*11/(604800pi)] chi(8-11M/r)/rho^2,

Delta B_psi
 =[128*11/(604800pi)] chi(36-67M/r)/rho^2.
```

At the declared strict gate `rho>=10`, the largest inherited-object value is

```text
max(|Delta A_psi|,|Delta B_psi|)=8.57656495653e-83.
```

Thus the massive scalar cannot create a large local compact correction while
its own local derivative expansion is valid. For `rho<1`, the local p8
expansion is not the correct observable and the nonlocal determinant must be
used instead.

## 8. Decision

```text
C3 -> p8 one-loop source map                 = derived;
O4 squared optimized p8 source               = derived;
p8 source-truncated fixed boundary           = derived;
new relevant p8 parameters                   = zero;
four GR-connected p8 trajectories            = integrated;
N6/N8 order convergence                      = pass;
exact source-truncated static correction      = bounded and negligible;
massive-spin threshold transfer law          = derived;
locality-safe motion-scalar compact bound     = derived;
photon/CFF p8 source                          = open;
three-loop pure-Einstein p8 source            = open;
full finite parent [B_C,B_t]                  = open;
selected static compact GR through p6         = retained;
exact all-operator compact GR                 = false;
full MTS                                      = false.
```

The next target is the four-graviton photon/`CFF` p8 helicity projector. It
is the lowest-loop omitted parent source and must be calculated before the
source-truncated finite vector can be promoted. Do not replace it by zero,
identify the running local `h_C3/g` with a complete physical amplitude, or
perform any GitHub action.

## 9. Outputs

- `post-checkpoint-work/source-intake/functional_rg/4967/p8_functional_source_audit.csv`
- `post-checkpoint-work/source-intake/functional_rg/4967/p8_amplitude_normalization_map.csv`
- `post-checkpoint-work/source-intake/functional_rg/4967/p8_massive_spin_threshold_transfer.csv`
- `post-checkpoint-work/source-intake/functional_rg/4967/p8_extended_fixed_point.csv`
- `post-checkpoint-work/source-intake/functional_rg/4967/p8_GR_connected_trajectory.csv`
- `post-checkpoint-work/source-intake/functional_rg/4967/p8_IR_endpoint_convergence.csv`
- `post-checkpoint-work/source-intake/functional_rg/4967/p8_static_compact_response.csv`
- `post-checkpoint-work/source-intake/functional_rg/4967/p8_motion_scalar_locality_bound.csv`
- `post-checkpoint-work/source-intake/functional_rg/4967/p8_finite_boundary_decision.csv`
- `post-checkpoint-work/source-intake/functional_rg/4967/p8_GR_trajectory_and_static_bound_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4967/PROVENANCE.md`

Formal marker: `PPC4161_C3_O4_P8_TRAJECTORY_STATIC_BOUND_4967`.

Validation: `P8_Y5_BRR545_4967_VALIDATION.csv` passes `22/22`, SHA256
`5261c9e6d087d6114e012da9b5b6afc677b9226e7272c9edd5e6d5c46745f273`.
