# 4935 - GR-connected minimal trajectory and motion-sector entry

Marker: `MTS_GR_CONNECTED_MINIMAL_TRAJECTORY_MOTION_ENTRY_4935`.

Date: `2026-07-12`.

Status: private executed trajectory and parent-Hessian checkpoint. The
source-complete minimal `C3-CFF-F4` point has a regular Gaussian/GR infrared
separatrix. The actual MTS motion action is then varied and its entry
coordinates are derived. The enlarged motion-MTS fixed point and trajectory
are not yet solved, so no full-MTS or local-GR/Newton/Maxwell claim follows.

## 1. Decisive trajectory result

Checkpoint 4934 established the source-complete minimal fixed point

```text
x*=(g,g_plus,g_minus,g_CFF,h_C3)
  =(0.1305603732179711,
    0.3470041701608080,
    3.244460421436017,
    0.0037300003823489045,
    3.947320506281829e-6).
```

Its sole negative-real beta eigenvalue is

```text
lambda_rel=-1.890832345405438,
theta_rel=+1.890832345405438.
```

The relevant eigenvector is normalized so that its largest coordinate-
relative component equals one:

```text
v_rel={
 0.0642046886444,
 0.347004170161,
 3.00608502314,
 0.00189524252035,
 1.28265668617e-6}.
```

For RG time `t=ln(k/k_seed)`, the negative-sign deformation

```text
x(0)=x*-epsilon v_rel
```

is integrated toward decreasing `t`. Every tested seed

```text
epsilon={1e-4,3e-5,1e-5,3e-6,1e-6}
```

reaches `g=1e-10` with finite coordinates and positive Newton coupling. The
opposite sign does not approach the Gaussian point: it reaches the declared
scaled-norm stop with

```text
g=0.856202,
g_plus=34.7004,
g_minus=222.845.
```

Thus the completed minimal point retains the expected two-branch structure:
one regular Gaussian/GR separatrix and one runaway branch.

## 2. Infrared scaling

The endpoint of the smallest-seed branch is

```text
(g,g_plus,g_minus,g_CFF,h_C3)
 =(1.00000000000e-10,
   2.00015675637e-19,
   9.37433997945e-18,
   2.76938422997e-12,
   4.00764937220e-14).
```

The endpoint logarithmic beta ratios are

```text
beta_g/g           =1.99999999839,
beta_gplus/g_plus  =3.99999999623,
beta_gminus/g_minus=3.92205673199,
beta_CFF/g_CFF     =1.99999999843,
beta_h/h           =1.90843739987.
```

The noncanonical last two values are not failed scaling. `g_minus` and `h_C3`
contain the expected resonant logarithms. On the zero-interaction Gaussian
ray the executed system gives

```text
beta_g/g ->2,
beta_plus/g^2 ->0,
beta_minus/g^2 ->-1096/15,
beta_h/g ->c_C3=-3.669491731602941e-5.
```

Therefore

```text
g_minus/g^2
 =f_minus-(548/15)ln(c_l g)+o(1),

h_C3/g
 =A_C3+(c_C3/2)ln g+o(1),

c_C3/2=-1.8347458658014704e-5.
```

The photon logarithm is recovered numerically to better than `1e-12` in its
source coefficient. The combined C3 logarithmic source is `8.53488` times the
pure-gravity source-scheme coefficient; this is a derived photon-completed
effect, not a fitted infrared constant.

## 3. Predicted minimal Wilson endpoint

Using the source definitions

```text
W_plus =lim g_plus/(16pi g)^2,

W_minus=lim [g_minus/g^2+(548/15)ln(16pi g)]/(16pi)^2,

W_C    =lim g_CFF/(16pi g),
```

and subtracting the derived C3 logarithm gives

```text
W_plus          =0.007916337891619754,
W_minus(c_l=16pi)=0.09472565630613844,
W_C             =0.000550951486900825,
A_C3            =-2.1700910782992792e-5.
```

Relative to the external four-derivative FP1 endpoint quoted in checkpoint
4932, the completed minimal trajectory moves

```text
W_plus  by -0.04624 percent,
W_minus by -0.81083 percent,
W_C     by +0.17300 percent.
```

The explicit six-derivative completion therefore preserves the photon
endpoint at the sub-percent level while predicting its own C3 finite
constant. This is stronger than comparing ultraviolet coordinate ratios.

## 4. Seed and numerical robustness

Across the five seed amplitudes, maximum endpoint differences relative to the
smallest-seed result are

```text
W_plus   8.69e-10,
W_minus  7.82e-10,
W_C      1.09e-9,
A_C3     6.70e-6
```

in relative units. The larger C3 spread is caused by subtraction of a large
logarithm from the small finite remainder and remains below `7e-6`.

The raw `20 x 20` projection condition number grows to `1.8849e21` because
the canonical coordinates carry very different powers of `g` in the
infrared. This is a scaling artefact that must still be reported. Iterative
row/column equilibration gives

```text
max kappa_2(A_equilibrated)=210.5102,
endpoint kappa_2(A_equilibrated)=13.9606,
max backward relative solve residual=1.3233e-16.
```

The Wilson convergence, equilibrated condition and backward residual together
support the numerical trajectory. The raw condition number must not be quoted
alone as either proof of failure or proof of accuracy.

## 5. Actual MTS motion action

The parent action selected in checkpoint 4916 contains the canonically
normalized motion scalar

```text
S_psi
 =-1/2 integral H^{mu nu} partial_mu psi partial_nu psi
  -integral sqrt(-g) V(psi),

V(psi)=(3/4)g_psi |psi|^(4/3).
```

The old coefficient `M_N` is a field-coordinate redundancy. The canonical
`g_psi` is invariant and physical. For `psi !=0`, exact variation gives

```text
V'(psi)=g_psi sign(psi)|psi|^(1/3),

V''(psi)=g_psi/[3|psi|^(2/3)].
```

The only classical stationary point is `psi_0=0`, but

```text
lim_(psi->0) V''(psi)=+infinity.
```

This rejects a tempting shortcut: the motion field cannot be appended to the
functional trace as a standard bare finite-mass scalar obtained by evaluating
the fractional potential Hessian at its vacuum.

## 6. Renormalized 1PI entry and relevant scale

The valid motion entry is the renormalized two-point operator

```text
Gamma_psi,k^(2)
 =Z_psi,k[-Box_g+m_psi,k^2]
  +curvature and higher-derivative terms.
```

The physical mass-gap scaling is

```text
m_gap=c_m g_psi^(3/8).
```

Because `[psi]=1` in four dimensions,

```text
[g_psi]=8/3,

gtilde_psi=k^(-8/3)g_psi,

w_psi=m_gap^2/k^2
     =c_m^2 gtilde_psi^(3/4).
```

At the Gaussian motion point the canonical flow is

```text
beta_gtilde=-(8/3)gtilde_psi,

beta_w=-2w_psi.
```

Hence the motion scale has positive critical exponent `8/3` in the potential
coordinate or `2` in the mass-squared coordinate. After the overall Newton
scale is fixed, this is a second physical relevant scale unless one of two
things happens:

1. the coupled gravity-motion flow has an interacting motion fixed point that
   fixes it;
2. a parent identity derives `g_psi/G_N^(-4/3)` or equivalently
   `m_gap/M_Pl`.

The existing corpus has not yet supplied either result. This is now the
precise predictivity question, not an unspecified “motion coupling” gap.

## 7. Exact minimal threshold entry

For the natural optimized scalar regulator and dimensionless mass
`w_psi=m_gap^2/k^2`, the subcutoff denominator gives

```text
D_psi(w)=1/(1+w).
```

The inherited one-real-scalar contributions are

```text
Delta beta_g
 =g^2/[6pi(1+w_psi)],

c6_scalar=1/[30240(4pi)^2],

Delta beta_h
 =eta_psi c6_scalar/(1+w_psi).
```

Thus the motion field becomes one real massless spectator in the UV
`w_psi->0`, while it decouples as `k^2/m_gap^2` in the infrared. At
`eta_psi=0` its minimal optimized trace has no direct C3 row, reproducing the
earlier exact spectator zero.

This threshold block is derived, but it is not the entire interacting motion
flow.

## 8. Unique six-derivative motion portal

The source-locked CP-even shift-symmetric six-derivative quotient contains
five operators. At a constant motion background, the motion-field quadratic
Hessians of `O1`, `O2` and `O5` vanish by field degree. The unique nonzero
motion portal is

```text
O4=C_abcd C^abcd (nabla psi)^2.
```

With action convention

```text
S_O4=u_O4 integral sqrt(g) C^2(nabla psi)^2,
```

its exact scalar Hessian contribution is

```text
Delta Gamma_psi^(2)
 =-2u_O4 nabla_mu[C^2 nabla^mu].
```

The dimensionless coordinate is `utilde_O4=k^4u_O4`, with canonical beta
eigenvalue `+4` before additive gravity terms. It is irrelevant at the
Gaussian point but can acquire a nonzero interacting fixed-point value and
mix into the C3 rows. Its beta function cannot be replaced by `u_O4=0` merely
because the matching action starts minimally.

## 9. What is now proved

```text
source-complete minimal ultraviolet point     = retained;
one regular minimal Gaussian/GR separatrix    = derived;
opposite relevant branch                      = runaway in executed domain;
minimal IR Wilson endpoint                    = calculated;
five-seed trajectory convergence              = passed;
Gaussian canonical and logarithmic scaling    = recovered;
actual parent motion Hessian                  = varied;
bare fractional-vacuum Hessian                = unusable infinity;
renormalized 1PI mass entry                   = required and formulated;
minimal massive threshold                     = derived;
motion scale critical exponent                = +8/3 or +2;
unique six-derivative motion portal            = O4;
enlarged motion fixed point and trajectory     = not calculated;
full MTS/local GR/Newton/Maxwell               = not promoted.
```

The minimal gravity-photon-C3 system is no longer blocked by the existence of
an infrared GR branch. The next uncertainty is whether the actual motion
sector preserves one-parameter predictivity or introduces a second free
physical scale.

## 10. Next derivation

The next target is

`4936-Y5-R2FR-motion-1PI-mass-and-O4-functional-trace-projection-or-two-scale-predictivity-gate.md`.

It must:

1. define the renormalized motion `Gamma_psi^(2)` in the same natural source
   scheme;
2. calculate `beta_gtilde_psi` or `beta_w`, `eta_psi` and `beta_uO4` rather
   than freezing them;
3. insert their affine trace contributions into the canonical selected rows;
4. solve the enlarged common zero and count relevant directions;
5. integrate every surviving GR-connected branch.

If the motion scale remains relevant, the theory has a two-scale predictive
boundary unless a parent identity fixes `m_gap/M_Pl`. If it becomes
irrelevant at an interacting motion point, the stronger one-scale MTS route
survives.

## 11. Artifacts

- `scripts/Y5_R2FR_4935_completed_fixed_point_trajectory.py`.
- `scripts/Y5_R2FR_4935_motion_sector_entry.py`.
- `source-intake/functional_rg/4935/completed_fixed_point_trajectory_results.json`:
  SHA-256 `8793e369ba0a9726c43dc64fe454ba87f88876832eca0ba9b79f07b171d1e222`.
- `source-intake/functional_rg/4935/completed_fixed_point_GR_branch_trace.csv`:
  SHA-256 `9244de9c6414ea78bc0c72a12010aca273831417f76e97c54212faf5337ea643`.
- `source-intake/functional_rg/4935/motion_sector_entry_results.json`:
  SHA-256 `ba3dfdaacfb1e3d00282d82c4b4656a937e033cb9145e94c71b81e9c42a54240`.
- `source-intake/functional_rg/4935/motion_sector_entry_operator_table.csv`:
  SHA-256 `50f6a5481e3e1a94df12469ce13fa0a88450770a5930226eec928f8e9bafc3d6`.

