# 4985 - Metric-frame `O2` zero and partial-wave mixing flow

Date: 2026-07-14

Marker: `MTS_4985_METRIC_FRAME_O2_PARTIAL_WAVE_FLOW`.

> **4990 amplitude-scheme correction.** The expressions `dC/dlnmu=16` and
> `-48/pi` below were obtained by importing the Type-I/Litim Wilsonian
> coefficient into an on-shell amplitude orbit. Checkpoint 4990 separates
> those coordinates. In the perturbative S-matrix scheme the active values
> are `dC/dlnmu=203/10` and `B_gc beta_C/2=-609/(10pi)`. The exact
> `B_gc=-6/pi` mixing result is unchanged.

Status: private analytic, primary-source-locked, symbolically reduced and
independently validated checkpoint. This checkpoint closes the running
metric-frame part of the six-derivative `O2` ambiguity and derives the first
nonzero genuine parent contribution to its flow. It also corrects the loop
order assigned in checkpoint 4959. It does not derive the fixed-common-scheme
two-loop single logarithm, the finite trajectory datum, exact local GR, or
full MTS.

## 1. Infinitesimal running metric frame

The exact finite Einstein-frame map retained at 4958 is

```text
r^3-r+kappa X[d(r^2-1)+ctilde r]=0,
C=(r+kappa d X)/r^2,
A=-kappa ctilde/r,
g_old,mn=Cg_mn+A v_m v_n.
```

Linearization at `ctilde=d=0` gives

```text
delta g_mn
 =kappa[(delta d+delta ctilde/2)X g_mn
        -delta ctilde v_m v_n].
```

For `S_EH=-int sqrt(g)R/kappa`, the Palatini first variation is

```text
delta S_EH
 =(1/kappa)int sqrt(g)G^mn delta g_mn
 -(1/kappa)int sqrt(g)nabla_m Theta^m,

Theta^m=nabla_n delta g^mn-nabla^m(delta g),
```

so the bulk term is exactly

```text
delta S_EH,bulk=-delta d R X
                 -delta ctilde R_mn v^m v^n.
```

It cancels the two redundant Ricci coordinates which the running frame is
defined to remove. The boundary vector reduces to

```text
Theta^m=kappa[-(6 delta d+2 delta ctilde)H^m_n v^n
               -delta ctilde v^m Box psi].
```

Thirty-two fresh Euclidean/Lorentzian local jets reproduce the bulk and
boundary identities at maximum relative residuals `4.89e-15` and
`4.04e-16`. The boundary vector vanishes on the selected `psi=0` collar.

The first variations of the scalar kinetic term and `cX^2` contain only the
already owned algebraic `X^2` and `X^3` coordinates. A Hessian-squared
six-derivative term can first arise from the second EH variation through
terms schematically of type `(nabla delta g)^2`. Therefore

```text
w_frame=w+A_cc ctilde^2+A_cd ctilde d+A_dd d^2+O(3),
partial_ctilde w_frame|0=partial_d w_frame|0=0,
delta beta_wO2|metric frame=0.
```

This does not say that the finite map is `O2`-free away from the zero
surface. It says that its first derivative at the maintained running surface
cannot enter the beta function.

## 2. Correct derivative and loop order

The gravity-EFT power count is

```text
D=2+2L+sum_i(d_i-2).
```

Consequently

```text
one loop, minimal d=2 vertices only:     D=4,
one loop, one d=4 insertion:             D=6,
two loops, minimal d=2 vertices only:    D=6.
```

Four-matter amplitudes can and do diverge at one loop, but that divergence
is at four derivatives. It generates the `X^2` packet, not the
six-derivative `O2` packet. Thus the pure-minimal universal one-loop `O2`
source is exactly zero. The `beta_w=6w+S_O2 g^2` ansatz in section 7 of
checkpoint 4959 is superseded. The genuine six-derivative sources begin as
`g c_ess` and `g^3`.

## 3. Complete one-loop `X2 -> O2` cut

The source-locked one-loop anomalous-dimension formula is evaluated using
two-particle partial waves. At first order in `X^2`, the higher-derivative
side of every cut has four scalar legs. Reflection parity therefore excludes
scalar-graviton intermediate states, and two-graviton states have too few
scalar legs. The scalar-scalar cut is the complete linear-in-`X2` cut.

Use

```text
A_GR=(tu/s+su/t+st/u)/M_P^2,
A_X2=(u_X2/2)(s^2+t^2+u^2),
A_O2=-3 w_O2 s t u,
M_P^-2=8pi G=kappa/2,
u_X2=4c_ess.
```

With `z=(t-u)/s`, the identical-scalar gravity soft subtraction converts the
singular GR amplitude into the finite polynomial

```text
f_GR,reg(z)=-(7+z^2)/4,
f_X2(z)=(3+z^2)/4,
f_O2(z)=-(3/4)(1-z^2).
```

Their exact nonzero partial waves are

```text
                 a0          a2
GR, regularized  -11/6       -1/30
X2                5/6         1/30
O2               -1/2         1/10.
```

The two orderings `GR*X2` and `X2*GR` cancel the statistical factor `1/2`
for identical internal scalars. The `s`-channel mixed polynomial is

```text
-55/36-(1/180)P2[(t-u)/s].
```

Crossing gives the exact identity

```text
sum_cyclic s^3[-55/36-(1/180)P2((t-u)/s)]
 =-(9/2)stu.
```

Twelve rational events and 128 independent validator events reproduce it
with exact zero residual. Comparing the cut with `A_O2=-3wstu` yields

```text
mu d wbar_O2/dmu|X2
 =-3 ubar_X2/(16pi^2 M_P^2),

beta_w|X2=-(3/(2pi))g u_X2
          =-(6/pi)g c_ess.
```

This is a genuine, nonzero parent flow coefficient rather than a target
ledger or a fitted closure.

## 4. Corrected weak trajectory and scheme law

Write the remaining fixed-common-scheme two-loop single-log coefficient as
`S_2L`. The corrected leading flow is

```text
beta_g=2g,
beta_c=4c+(203/10)g^2,
beta_w=6w-(6/pi)gc+S_2L g^3+... .
```

For `t=ln(k/k0)` this integrates exactly to

```text
c/g^2=C_c+(203/10)t,
w/g^3=C_w+(S_2L-6C_c/pi)t-[609/(10pi)]t^2.
```

The quadratic logarithm is not an assumption. It is the RG consistency
coefficient

```text
(A_c B_gc)/2=[(203/10)(-6/pi)]/2=-609/(10pi).
```

There is a resonant finite-scheme freedom at this order:

```text
w'=w+alpha g c
  => B_gc'=B_gc=-6/pi,
     S_2L'=S_2L+(203/10)alpha.
```

Hence the mixed coefficient and the double logarithm are invariant, while
an isolated local `g^3` coefficient is not. The remaining physical target is
the fixed-common-scheme renormalized single-log amplitude plus its finite
matching condition, not a scheme-free decimal called `S_2L`.

## 5. Local and amplitude consequences

The corrected flow does not reopen the selected local scalar branch:

```text
O2=X H_mn H^mn has scalar degree four,
psi=0 => E_psi=T_mn=J_psi=0 for arbitrary w_O2.
```

Its flat `p2` metric Hessian also vanishes there, so this packet still leaves
the leading Einstein/Newton/metric-Maxwell branch unchanged. Pure-metric
`C^3` and determinant/Jacobian responses remain and prevent an all-operator
PPN or exact-GR promotion.

The coefficient-independent 4959 six-point result is unchanged: minimizing
over every real `w_O2` leaves a strictly positive integrated rate, with the
smallest imported kernel `1.281894138887e-61`. What changes is the source
order. A universal `g^2` `O2` term is rejected; the natural weak trajectory
is `g^3` times boundary, single-log and derived double-log data. A numerical
interference prediction still requires the common-scheme single logarithm
and the trajectory datum `C_w`.

## 6. Physics decision

```text
metric-frame infinitesimal map                  = derived;
metric-frame O2 beta connection                 = exactly zero;
pure-minimal one-loop p6 source                 = exactly zero;
one-loop X2-to-O2 mixing                        = derived exactly;
mixed coefficient B_gc                         = -6/pi;
S-matrix trajectory double logarithm            = -609/(10pi);
historical Type-I/Litim coordinate result       = -48/pi, not used on shell;
fixed-common-scheme two-loop single logarithm   = open;
finite trajectory datum C_w                     = open;
arbitrary-O2 positive six-point lower bound     = retained;
selected local scalar packet                    = source silent;
pure-metric nonlinear/quantum residuals         = retained;
exact all-operator local GR                     = false;
full MTS                                        = false.
```

The live runner closes `14` derived gates and records `4` intended open
nonclaim gates. The independent validator passes `98/98` checks.

## 7. Artifacts

- `post-checkpoint-work/scripts/Y5_R2FR_4985_metric_frame_O2_partial_wave_flow.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4985_metric_frame_O2_partial_wave_flow_validation.py`
- `post-checkpoint-work/source-intake/functional_rg/4985/PROVENANCE.md`
- `post-checkpoint-work/source-intake/functional_rg/4985/metric_frame_infinitesimal_bulk_cancellation.csv`
- `post-checkpoint-work/source-intake/functional_rg/4985/metric_frame_boundary_jet_checks.csv`
- `post-checkpoint-work/source-intake/functional_rg/4985/metric_frame_O2_connection_zero.csv`
- `post-checkpoint-work/source-intake/functional_rg/4985/O2_loop_power_counting.csv`
- `post-checkpoint-work/source-intake/functional_rg/4985/O2_partial_wave_projection.csv`
- `post-checkpoint-work/source-intake/functional_rg/4985/O2_crossing_projector_checks.csv`
- `post-checkpoint-work/source-intake/functional_rg/4985/O2_source_decomposition.csv`
- `post-checkpoint-work/source-intake/functional_rg/4985/O2_corrected_flow_and_trajectory.csv`
- `post-checkpoint-work/source-intake/functional_rg/4985/local_GR_p6_consequence.csv`
- `post-checkpoint-work/source-intake/functional_rg/4985/metric_frame_O2_flow_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4985/metric_frame_O2_flow_results.json`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4985_VALIDATION.csv`

## Next target

Checkpoint 4986 should calculate the fixed-common-scheme renormalized
two-loop four-scalar `stu log(mu)` coefficient, with all one-loop `X^2`,
redundant, evanescent and soft subdivergences subtracted in the same amplitude
scheme used here. In parallel it should convert the already isolated
pure-metric `C^3` and determinant kernels into explicit weak/local bounds.
Only the complete renormalized amplitude may fix the single logarithm; do not
promote a raw two-loop pole, refit `S_2L`, or disturb the exact selected
`psi=0` branch.
