# 4970 - weak-scale Wilsonian-to-on-shell C3 splice and p8 matching transfer

Marker: `MTS_4970_WEAK_SCALE_C3_P8_MATCHING`.

Formal marker: `PPC4161_WEAK_SCALE_C3_P8_MATCHING_4970`.

Date: `2026-07-13`.

Status: private analytic and executable checkpoint. This checkpoint derives
the form and scale transport of the weak-branch matching coordinates. It does
not calculate their absolute finite anchor, set the primitive three-loop
vector to zero, or claim a complete four-graviton amplitude or full MTS.

## 1. Constant-offset no-go

Let `t=ln(k/k_seed)`, let `A_F(t)` be the functional trajectory coordinate,
and let `A_OS(t)` be the pure-Einstein on-shell coefficient. A constant finite map
on one common interval,

```text
A_OS(t)=A_F(t)+delta_A,
```

would imply `dA_OS/dt=dA_F/dt`. The source-locked slopes instead satisfy

```text
dA_F/dt in
[-3.678379389949363e-5,-3.678379389943907e-5],

beta_A^OS=dA_OS/dt
         =1/(3840 pi^3)
         =8.398837091979034e-6.
```

Here `N_b-N_f=2` counts the two physical graviton helicities, so
`beta_A^OS=(N_b-N_f)/(7680pi^3)`. Photons, the motion scalar and visible
matter are not included in this 4970 branch. They require a threshold-resolved
field-content extension before this splice can represent the full parent.

The displayed slopes have opposite sign. Therefore no constant finite coefficient shift can
identify the two running coordinates over an interval. This is a strict
no-go for that proposed map, not a no-go for matching.

## 2. Piecewise weak-branch splice

At a declared matching time `t_m` the most general linear weak branch used
here is

```text
A_OS(t)=A_F(t_m)+delta_A_m+beta_A^OS(t-t_m),  t<=t_m,

delta_A(t)=A_OS(t)-A_F(t).
```

The pure-Einstein beta function replaces the functional C3 beta below `t_m`
on this declared vacuum branch. It is not added to it. Because the 4969 known-source trajectory already contains
the functional `-12 A_F` contribution to `B_minus`, the correction obeys

```text
d delta_Bminus/dt
 =H_B delta_Bminus-12 delta_A+xi_minus/(32 pi^3),

d delta_Bplus/dt
 =H_B delta_Bplus+xi_plus/(32 pi^3),

H_B=6-3 beta_g/g,

delta_Bminus(t_m)=delta_Bminus_m,
delta_Bplus(t_m)=delta_Bplus_m.
```

Thus `B_matched=B_functional+delta_B` is a replacement construction and does
not double count the functional and on-shell C3 sources.

## 3. Finite matching vector and rank

The retained finite and primitive coordinates are

```text
theta_match=
(delta_A_m,delta_Bminus_m,delta_Bplus_m,xi_minus,xi_plus).
```

For the dynamic N8 trajectory at `g_match=1e-2`, the endpoint transfer is

```text
delta A_end / delta_A_m              = 1,
delta Bminus_end / delta_A_m         = 109.58139954161231,
delta Bminus_end / delta_Bminus_m    = 0.7782765647321441,
delta Bplus_end / delta_Bplus_m      = 0.7782765647321441,
delta Bminus_end / xi_minus          = -0.009203563230610664,
delta Bplus_end / xi_plus            = -0.009203563230610664.
```

The map from five matching coordinates to
`(A_C3,B_minus,B_plus)_end` has rank three and nullity two. The p8
boundary/primitive submatrix has rank two for four coordinates. One endpoint
therefore cannot distinguish a constant same-channel boundary from primitive
running. Scale-resolved amplitudes or a parent finite matching calculation
are required.

## 4. Zero-offset scan is not a prediction

Setting all finite and primitive coordinates to zero defines a useful
continuity prescription, not a theorem. At the dynamic N8
`g_match=1e-2` anchor it gives

```text
A_OS,end                    = -1.2155562513774108e-5,
replacement delta_Bminus   = -0.0227242404519213,
B_minus,matched,end         =  0.0032416031082646117,
B_plus,matched,end          =  0.0016045316920960777,
B_C,matched,end             =  0.0024230674001803447,
B_t,matched,end             = -0.000818535708084267.
```

Across `g_match=1e-2,...,1e-6`, the largest raw relative endpoint spread is
`1.0628890923681904`. That large dependence rejects any attempt to treat
zero offsets at every independently chosen matching point as physical
evidence.

## 5. Matching-scale invariance fixes offset running

The arbitrary matching point must not change a physical endpoint. Demanding
that one underlying matched trajectory be represented at every `t_m` gives

```text
d delta_A_m/dt_m
 =beta_A^OS-dA_F/dt_m,

d delta_Bminus_m/dt_m
 =H_B(t_m) delta_Bminus_m-12 delta_A_m,

d delta_Bplus_m/dt_m
 =H_B(t_m) delta_Bplus_m.
```

These are not fitted equations. They follow by evaluating the same
piecewise solution at a shifted matching surface. The executable test chooses
the `g_match=1e-2` zero-offset branch only as a reference convention and
transports its coordinates to four later matching surfaces. For dynamic N8,
the transported coordinates at `g_match=1e-6` are

```text
delta_A_m      = -2.05613866731248e-4,
delta_Bminus_m = -5.61252066688603e-3.
```

All twenty scheme/order/scale endpoint representations then agree with their
respective anchors to maximum absolute residual
`1.1533436098526417e-11`. The order-unity raw variation is therefore
identified as coordinate/surface dependence and removed by the derived
matching-coordinate flow.

This result does not determine the reference anchor. Choosing zero at the
anchor remains a convention until a finite amplitude calculation fixes it.

## 6. Decision

```text
constant finite C3 shift over an interval       = rejected;
piecewise beta replacement                      = derived;
C3 double counting                              = excluded;
five-coordinate matching transfer               = calculated;
endpoint transfer rank                          = 3;
endpoint parameter nullity                      = 2;
raw zero-offset match-scale dependence          = exposed;
matching-coordinate RG transport                = derived;
transported endpoint invariance                  = pass;
absolute finite matching anchor                 = open;
primitive xi_minus and xi_plus                   = open;
complete physical four-graviton amplitude       = open;
full-parent matter/photon threshold beta         = open;
exact all-operator compact GR                    = false;
full MTS                                         = false.
```

This is a genuine matching result: the arbitrary splice scale is no longer a
hidden free choice. The remaining freedom is localized to one finite anchor
vector plus the primitive three-loop vector rather than being spread across
the trajectory.

## 7. Next calculation

Checkpoint 4971 should first generalize the Bern coefficient to the actual
parent field inventory and prove which thresholds decouple. It should then
calculate the pure-Einstein anchor rather than audit it again. At one common
subtraction scale it should:

1. expand the parent and physical helicity amplitudes at fixed nonforward
   kinematics;
2. subtract Einstein exchange, the known nonlocal logarithms, and the
   already-derived C3/CFF/O4 pieces;
3. use the six-derivative all-plus coefficient to determine
   `delta_A_m`;
4. use the independent eight-derivative same- and mixed-helicity remainders
   to determine `delta_Bminus_m` and `delta_Bplus_m`;
5. use scale dependence or the direct three-loop single pole to separate
   `xi_minus,xi_plus` from the finite p8 boundary.

If the parent truncation cannot supply those finite amplitude remainders,
the anchor remains an explicit EFT input. It must not be set to zero merely
because the transport equations are now known.

No GitHub action is authorized by this checkpoint.

## 8. Outputs

- `post-checkpoint-work/scripts/Y5_R2FR_4970_weak_scale_C3_p8_matching.py`
- `post-checkpoint-work/source-intake/functional_rg/4970/C3_matching_contract.csv`
- `post-checkpoint-work/source-intake/functional_rg/4970/C3_weak_branch_splice_scan.csv`
- `post-checkpoint-work/source-intake/functional_rg/4970/C3_p8_matching_transfer_matrix.csv`
- `post-checkpoint-work/source-intake/functional_rg/4970/C3_matching_scale_sensitivity.csv`
- `post-checkpoint-work/source-intake/functional_rg/4970/C3_matching_offset_RG_transport.csv`
- `post-checkpoint-work/source-intake/functional_rg/4970/C3_p8_finite_matching_results.json`

## 9. Validation

`P8_Y5_BRR545_4970_VALIDATION.csv` passes `30/30` deterministic checks.
SHA256:
`fc06ce49ae48127ef407638a762aa8944028d15b365da71c5533e426b7d8ba1f`.

The gate checks source, runner and output hashes; script syntax; CSV schemas
and finite values; the constant-shift no-go; all scan, transfer, sensitivity
and transport row counts; no-double-counting labels; rank and nullity;
zero-offset nonclaim status; explicit `N_b-N_f=2` pure-Einstein scope;
RG-transported endpoint invariance; register and
handoff propagation; the corrected `B_t=(B_plus-B_minus)/2` convention;
placeholder absence; bytecode absence; and the retained false full-MTS flag.
