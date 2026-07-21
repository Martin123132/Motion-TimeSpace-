# 4986 - Common-scheme logarithmic invariant and local metric exterior bounds

Date: 2026-07-14

Marker: `MTS_4986_COMMON_SCHEME_LOG_INVARIANT_LOCAL_METRIC_BOUNDS`.

> **4990 amplitude-scheme correction.** The original `16` running
> coefficient is retained only as a Type-I/Litim FRG coordinate. The active
> perturbative on-shell orbit uses `beta_C=203/10`; consequently the double
> logarithm and fixed-p4 invariant below are corrected to
> `203/(20pi)` and `3S_2L-(203/10)rho_mix`. The one-loop `F_1,log` is
> unchanged.

Status: private analytic, primary-source-locked, generated and independently
validated checkpoint. This checkpoint reconstructs the complete nonlocal
one-loop `X2 -> O2` logarithm, derives the full RG-forced two-loop double-log
kernel, replaces the nonphysical raw `S_2L` target by an exact finite-scheme
invariant, and turns the retained `C3` and parent-determinant metric terms into
explicit exterior bounds. It does not calculate the remaining two-loop
primitive, finite trajectory boundary, complete quantum potential, exact
all-operator local GR, or full MTS.

## 1. Source outcome and amplitude boundary

The archived Dunbar-Norridge calculation supplies the complete
cut-constructible logarithmic part of the one-loop four-scalar
Einstein-gravity amplitude. It explicitly includes scalar and graviton
intermediate states, recovers the `203/(320 epsilon)(D phi)^4` counterterm,
and states the residual freedom as finite rational momentum polynomials.
Bern et al. supply the four-dimensional unitarity method for extracting
two-loop renormalization-scale dependence without promoting evanescent
poles.

Those sources do not supply the complete two-loop four-scalar amplitude
needed here. Unlike the all-plus four-graviton control, scalar scattering
has nontrivial mixed one-loop amplitudes and generally nonvanishing
three-particle cuts. Therefore a raw pole, the pure-gravity all-plus result,
or an assumed vanishing three-particle cut cannot fill the scalar primitive.

## 2. Complete crossing logarithm basis

The checkpoint-4985 `s`-channel polynomial reduces exactly because

```text
P2((t-u)/s)=1-6tu/s^2,

P_s=s^3[-55/36-(1/180)P2((t-u)/s)]
   =-(23/15)s^3+(1/30)stu.
```

Crossing and `s+t+u=0` give

```text
sum_cyclic P_s=-(9/2)stu,
s^3+t^3+u^3=3stu.
```

The complete crossing-symmetric single-log basis at degree six is

```text
L_A=sum_cyclic s^3 ln(-s/mu^2),
L_B=stu sum_cyclic ln(-s/mu^2),

dL_A/dlnmu=dL_B/dlnmu=-6stu.
```

Consequently `L_A-L_B` is scale invariant. Scale running can determine only
the sum of the two channel coefficients; the orthogonal ratio-log shape
requires the full amplitude.

Twelve generated rational events and `344` independent rational events
reproduce both the channel reduction and crossing identity with exact zero
residual.

## 3. Full one-loop mixed nonlocal logarithm

In the checkpoint-4985 conventions,

```text
A_X2=(u_X2/2)(s^2+t^2+u^2),
u_X2=4c_ess,
A_O2=-3w stu,
B_gc=-6/pi.
```

The complete logarithmic amplitude linear in `g c_ess` is

```text
F_1,log=(2/pi)[(23/15)L_A-(1/30)L_B],

dF_1,log/dlnmu=-(18/pi)stu=3B_gc stu.
```

This is stronger than the local beta projection in 4985: it fixes the full
nonlocal channel shape. Crossing symmetry permits one finite local rational
coordinate at this order,

```text
F_1=F_1,log+rho_mix stu.
```

The `rho_mix` term is not set to zero by the cut calculation. It is the
finite common-scheme datum which must transform together with the local
`O2` coordinate.

## 4. RG-forced two-loop double logarithm

Strip the common dimensional prefactor and define

```text
C=c/g^2,
W=w/g^3,
dC/dlnmu=203/10,
dW/dlnmu=B_gc C+S_2L.
```

The reduced degree-six amplitude is

```text
R=-3W stu+C F_1+F_2.
```

RG invariance requires

```text
dF_1/dlnmu=3B_gc stu,
dF_2/dlnmu=3S_2L stu-(203/10)F_1.
```

Introduce

```text
Q_A=sum_cyclic s^3 ln^2(-s/mu^2),
Q_B=stu sum_cyclic ln^2(-s/mu^2),

dQ_A/dlnmu=-4L_A,
dQ_B/dlnmu=-4L_B.
```

The complete forced double-log kernel is then

```text
F_2,double=(203/(20pi))[(23/15)Q_A-(1/30)Q_B],

dF_2,double/dlnmu=-(203/10)F_1,log.
```

This is the physical channel completion of the S-matrix trajectory
coefficient `-609/(10pi)`. Under
`ln(-s/mu^2) -> ln(-s/mu0^2)-2t`, the three apparent
quadratic-log contributions are

```text
local -3Wstu:       +1827 stu t^2/(10pi),
running C times F1: -1827 stu t^2/(5pi),
F2,double:          +1827 stu t^2/(10pi),
sum:                       0.
```

The local-coordinate `-609/(10pi)` term is therefore necessary but is not the
whole two-loop double-log amplitude.

## 5. Exact finite-scheme invariant

The finite coordinate change inherited from 4985 is

```text
w'=w+alpha g c,
S_2L'=S_2L+(203/10)alpha.
```

Amplitude invariance simultaneously requires

```text
F_1'=F_1+3alpha stu,
rho_mix'=rho_mix+3alpha.
```

Therefore

```text
I_2L=3S_2L-(203/10)rho_mix,
I_2L'=I_2L
```

is exact. Raw `S_2L` is not the physical target.

Writing the remaining two-loop single logarithm as

```text
F_2,single=A_2 L_A+B_2 L_B
```

gives

```text
A_2+B_2=-I_2L/6,
J_2L=A_2-B_2,

F_2,single=-(I_2L/12)(L_A+L_B)
             +(J_2L/2)(L_A-L_B).
```

Thus the unresolved two-loop calculation has been reduced to two physical
numbers: the scale coefficient `I_2L` and the scale-invariant angular
coefficient `J_2L`. The finite trajectory boundary `C_w` remains a separate
UV datum.

Forty-eight generated and `96` independent random controls evolve the full
reduced logarithmic amplitude under both RG running and arbitrary finite
scheme changes. The largest generated full-RG residual is `8.84e-14`; the
largest independent full-RG residual is below `3e-12`.

## 6. `C3` exterior compactness bound

Checkpoint 4963 selected

```text
|a_+|<=7.564067676419907e-143 m^4
```

in its locked finite source scheme, with exterior response

```text
|Delta Phi/Phi_N|=20|a_+|M^2/r^6,
|Delta a/a_N|    =140|a_+|M^2/r^6.
```

For every exterior point satisfying `r>=2M`,

```text
M^2/r^6<=1/(4r^4),

|Delta Phi/Phi_N|<=5|a_+|/r^4,
|Delta a/a_N|    <=35|a_+|/r^4.
```

This removes the source mass from the conservative bound. At the shortest
`52 micrometre` benchmark,

```text
selected |Delta Phi/Phi_N| <=5.17263740083e-125,
selected |Delta a/a_N|     <=3.62084618058e-124.
```

The inherited raw-running safety envelope gives
`|Delta a/a_N|<=4.24865650783e-122` at that scale. It is not promoted to a
physical amplitude because its scale dependence must cancel against the
nonlocal `p6` form factor. Reaching a one-percent acceleration correction at
`52 micrometres` would require

```text
|a_+|/l_P^4 >=3.06129920581e118,
```

which quantifies the required amplification without assuming that the
unknown complete amplitude vanishes.

## 7. Parent determinant exterior tail

The checkpoint-4981 quadratic logarithm separates into

```text
Gamma_log=(4pi)^-2 int sqrt(g)[
  a Ricci_mn log(-Box/mu^2) Ricci^mn
 +b R log(-Box/mu^2)R],

gravity+ghost:           a=7/20,    b=1/120, a+b=43/120;
massless motion scalar:  a=1/120,   b=1/240, a+b=1/80;
parent massless endpoint:a=43/120,  b=1/80,  a+b=89/240.
```

The last row is the `m_gap r << 1` massless-log endpoint. The physical
motion-sector mass threshold has not been sourced, so it cannot be used as
the parent coefficient at arbitrary infrared separation.

For conserved static sources, the transverse spin projectors give

```text
K_2=(a/2)q^4 log,
K_0=2(a+3b)q^4 log,

T P_2 T=2T00^2/3,
T P_0 T=T00^2/3,
D_0 proportional to P_2-(1/2)P_0.
```

For each sector the normalized source contraction is `a+b`. The
gravity-plus-ghost result is therefore

```text
delta A_grav/A_tree=-[43/(60pi)]l_P^2 q^2 ln(q^2/mu^2),
|Delta Phi_grav/Phi_N|=[43/(30pi)]l_P^2/r^2,
|Delta a_grav/a_N|=[43/(10pi)]l_P^2/r^2.
```

At the parent massless endpoint, including the EH and `(4pi)^-2`
normalization gives

```text
delta A/A_tree
 =-[2(a+b)/pi]l_P^2 q^2 ln(q^2/mu^2)
 =-[89/(120pi)]l_P^2 q^2 ln(q^2/mu^2).
```

For `r>0`,

```text
Fourier[1/q^2]=1/(4pi r),
Fourier[ln(q^2/mu^2)]=-1/(2pi r^3),
```

where the `mu` term is source contact. Hence the parent massless-endpoint
two-point tail is

```text
|Delta Phi_det/Phi_N|=[89/(60pi)]l_P^2/r^2,
|Delta a_det/a_N|    =[89/(20pi)]l_P^2/r^2.
```

At `52 micrometres`,

```text
|Delta Phi_grav/Phi_N|=4.40768364970e-62,
|Delta a_grav/a_N|    =1.32230509491e-61,
|Delta Phi_det/Phi_N|=4.56144005608e-62,
|Delta a_det/a_N|    =1.36843201682e-61.
```

The gravity-plus-ghost tail is explicit. The `89/240` result is only the
parent massless-log endpoint; the physical motion contribution requires a
thresholded form factor derived from the parent `m_gap`. Both are two-point
or vacuum-polarization subsets, not the complete one-loop source-source
potential. Finite local `R^2` and `Ricci^2` coordinates are analytic in
momentum and contribute only source contacts at first EFT order; they vanish
distributionally for separated exterior points but not inside overlapping
source support.

## 8. Physics decision

```text
complete mixed one-loop nonlocal log shape        = derived;
full RG-forced two-loop double-log kernel         = derived;
raw S_2L as physical target                       = rejected;
scheme-invariant I_2L definition                  = derived exactly;
numeric I_2L                                      = open;
numeric angular J_2L                              = open;
finite trajectory datum C_w                       = open;
finite local p4 separated-source exterior effect = contact zero;
gravity determinant two-point tail                = derived and bounded;
parent massless-log determinant endpoint          = derived and bounded;
physical motion m_gap threshold form factor       = open;
selected local C3 exterior contribution           = derived and bounded;
complete physical C3 amplitude                    = open;
known p4/p6 pure-metric residual classes          = separated and bounded;
exact all-operator local GR                       = false;
full MTS                                          = false.
```

The live runner records `13` closed and `6` explicit open/nonclaim gates.
The independent validator passes `109/109` checks.

## 9. Artifacts

- `post-checkpoint-work/scripts/Y5_R2FR_4986_common_scheme_log_invariant_and_local_metric_bounds.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4986_common_scheme_log_invariant_and_local_metric_bounds_validation.py`
- `post-checkpoint-work/source-intake/functional_rg/4986/O2_crossing_log_basis_and_scheme_invariant.csv`
- `post-checkpoint-work/source-intake/functional_rg/4986/O2_exact_kinematic_reconstruction.csv`
- `post-checkpoint-work/source-intake/functional_rg/4986/O2_full_logarithmic_RG_checks.csv`
- `post-checkpoint-work/source-intake/functional_rg/4986/C3_exterior_compactness_bounds.csv`
- `post-checkpoint-work/source-intake/functional_rg/4986/determinant_exterior_tail_bounds.csv`
- `post-checkpoint-work/source-intake/functional_rg/4986/pure_metric_contact_and_claim_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4986/common_scheme_log_and_local_metric_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4986/common_scheme_log_and_local_metric_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4986/PROVENANCE.md`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4986_VALIDATION.csv`

## Next target

Checkpoint 4987 should calculate `I_2L` and `J_2L` directly from the
renormalized two-loop four-scalar discontinuities in this same amplitude
scheme. It must assemble the required renormalized `4phi` and `2phi2h`
one-loop amplitudes, the `X^2` counterterm insertion, both two-particle and
three-particle cuts, and the universal soft subtraction before projecting
onto `L_A` and `L_B`. It should not calculate a raw `S_2L` in isolation or
assume the scalar three-particle cut vanishes.
