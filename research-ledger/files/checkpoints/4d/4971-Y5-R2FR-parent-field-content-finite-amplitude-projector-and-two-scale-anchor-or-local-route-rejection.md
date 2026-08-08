# 4971 - parent field content, finite amplitude projector and two-scale anchor

Marker: `MTS_4971_PARENT_FIELD_CONTENT_TWO_SCALE_ANCHOR`.

Formal marker: `PPC4161_PARENT_FIELD_CONTENT_AMPLITUDE_ANCHOR_4971`.

Date: `2026-07-13`.

Status: private analytic, source-acquired and executable checkpoint. This
checkpoint replaces the pure-Einstein-only field count by explicit parent
branches, derives the exact finite six-derivative amplitude projector from
the current published two-loop ancillary files, proves a full-rank two-scale
eight-derivative matching route, and decides whether the present local
functional trajectory can calculate the absolute anchor. It does not claim a
complete parent amplitude, set the remaining physical scale by convention, or
promote full MTS.

## 1. Parent field content changes the on-shell source

For a massless theory minimally coupled to gravity, the Bern state-count law
in the retained `A_Bern` convention is

```text
N=N_b-N_f=2+N_s+2N_V-4N_D+N_motion,
beta_A=dA_Bern/dln(mu)=N/(7680*pi^3).
```

The adopted GR plus Standard Model parent therefore gives

```text
SM45:             N=-60, beta_A=-0.00025196511275937106,
SM45 plus motion: N=-59, beta_A=-0.00024776569421338155.
```

The smallest tested matching scale is `1.22089e16 GeV`, above all Standard
Model mass thresholds. The high-scale splice must therefore use the full
active parent bracket, not the checkpoint-4970 `N=2` pure-Einstein comparator.
The current functional slope corresponds to

```text
N_eff=-8.75925881086,
```

so the present local trajectory is not already the completed GR plus SM
on-shell flow. This agrees with the recorded omission of full interacting
visible-matter Hessians from the functional truncation.

## 2. Full-parent C3-induced splice

The checkpoint-4970 replacement and matching-coordinate transport remain
valid after replacing the branch beta function:

```text
A_OS(t)=A_F(t_m)+delta_A_m+beta_A(t-t_m),

d delta_A_m/dt_m=beta_A-dA_F/dt_m,

d delta_Bminus_m/dt_m
 =H_B(t_m)delta_Bminus_m-12delta_A_m,

d delta_Bplus_m/dt_m
 =H_B(t_m)delta_Bplus_m.
```

Forty SM45/SM45-plus-motion scheme/order/scale scans and forty transported
representations were executed. The maximum transported endpoint residual is

```text
3.70703467922e-11.
```

This part is only the iterated C3-induced p8 response. Direct full-SM and
motion p8 threshold terms are not silently set to zero.

## 3. Exact finite E6 amplitude projector

The exact arXiv v2 source bundle for Abreu et al., *The Two-Loop
Four-Graviton Scattering Amplitudes*, was acquired with its corrected finite
remainders and ancillary Mathematica files. The physical finite coupling in
those remainders is

```text
c(mu)=c_R3(mu)-c_GB(mu)/2.
```

Writing `u=-s-t` and subtracting the complete `c=0` Einstein remainder gives
the source-exact coupling pieces

```text
Delta R_pppp=-60 c(mu) s t u,
Delta R_mppp= -6 c(mu) s t u.
```

The Bern-oriented MTS coordinate is related to the amplitude convention by

```text
A_Bern=-c(mu)/(32*pi^3).
```

Consequently the previously generic E6 projector is now explicit:

```text
A_Bern=Delta R_pppp/[1920*pi^3*s*t*u],

A_Bern=Delta R_mppp/[192*pi^3*s*t*u].
```

The two helicities obey the independent consistency identity

```text
Delta R_pppp=10 Delta R_mppp.
```

Thus a future parent calculation cannot merely return an arbitrary number:
the all-plus and single-minus projections must agree. In the all-plus source,
the finite local coefficient after logarithmic and absorptive subtraction is

```text
117617/21600=5.445231481481481
```

at `c=0`. It is part of the known Einstein subtraction, not an MTS Wilson
coefficient.

## 4. The anchor is one physical RG-invariant scale

The amplitude and Bern-oriented conventions are reconciled by

```text
dc/dln(mu)=-N/240,
dA_Bern/dln(mu)=N/(7680*pi^3)=beta_A.
```

Introducing the physical scale `lambda` gives

```text
c(mu)=(N/240)ln(lambda/mu),
A_Bern(mu)=beta_A ln(mu/lambda),
lambda/mu=exp[-A_Bern(mu)/beta_A].
```

The absolute C3 anchor is therefore not an arbitrary function or a cloud of
untracked constants. It is exactly one RG-invariant scale `lambda` once the
finite parent remainder is known.

For orientation only, imposing the unproved zero-offset identification at
`g_match=1e-2` gives

```text
SM45:             lambda/mu in [1.2970894,1.2971420],
SM45 plus motion: lambda/mu in [1.3028207,1.3028744].
```

These rows are labelled
`ZERO_OFFSET_SCALE_DIAGNOSTIC_NOT_A_MATCHING_RESULT`; they are not promoted.

## 5. Exact local-route decision

Running data alone solve

```text
delta_A_m(t)=beta_A*t-A_F(t)+C_A,
```

and have rank zero for the integration constant. The newly acquired
amplitude supplies the exact projector for `C_A`, but it supplies the pure
Einstein remainder, not the finite MTS parent four-graviton remainder in the
same subtraction convention.

The local functional source itself states that reproducing the perturbative
two-loop coefficient generally requires an infinite derivative expansion.
The present local `C3` trajectory therefore cannot be substituted for the
missing momentum-dependent parent vertex. This is an exact scoped rejection:

```text
derive the anchor from current local running alone = rejected;
derive the anchor from a finite parent amplitude   = explicit route retained.
```

This is progress beyond an omission ledger. The missing calculation is now
one specific finite Wilsonian-to-amplitude conversion, checked in two
helicities, and its output is one physical scale.

## 6. Full-rank p8 route

At `g_match=1e-2`, the p8 boundary and primitive responses were evaluated at
`g=1e-8` and `g=1e-10`. For the dynamic N8 branch,

```text
H1=0.7782767501404041, P1=-0.006882784167014846,
H2=0.7782765646238787, P2=-0.009203563230632102,
det[[H1,P1],[H2,P2]]=-0.0018062096642961314.
```

All four scheme/order matrices have full rank five for the complete matching
vector and rank four for the p8 subvector. In either helicity channel,

```text
delta_B_m=(y1*P2-y2*P1)/(H1*P2-H2*P1),
xi=(H1*y2-H2*y1)/(H1*P2-H2*P1).
```

One E6 remainder plus same- and mixed-helicity E8 remainders at two distinct
scales therefore determine all five matching coordinates after the declared
known subtractions. One-scale p8 data remain underidentified.

## 7. Decision

```text
full-parent massless state-count law       = derived;
4970 pure-Einstein beta as full parent     = rejected;
SM45 and SM45-plus-motion C3 splices       = calculated;
matching-surface transport                 = pass;
finite all-plus E6 projector               = source-exact;
finite single-minus E6 cross-check         = source-exact;
E6 anchor free object                      = one physical scale lambda;
current local-running-only anchor          = rejected;
finite parent amplitude route              = explicit and open;
two-scale p8 matching matrix               = full rank;
direct full-SM/motion p8 thresholds        = open;
complete physical four-graviton amplitude  = open;
leading local GR/Newton/Maxwell branch      = retained;
exact all-operator compact GR              = false;
full MTS                                   = false.
```

## 8. Next target

Checkpoint 4972 should calculate rather than reaudit the one remaining E6
conversion. Construct the momentum-dependent parent `C3` three-/four-graviton
1PI vertex or the equivalent nonlocal form factor in the same regulator and
field convention as the selected functional trajectory. Project both `++++`
and `-+++`, subtract the source-locked `c=0` Einstein remainders, and require
the factor-ten identity. If that finite conversion cannot be calculated from
the parent action, retain `lambda` as one explicit physical EFT input instead
of inventing a zero. Then use the already-derived two-scale p8 inversions.

Do not reopen the p8 canonical repair, repeat the state-count audit, or perform
GitHub action.

## 9. Outputs

- `post-checkpoint-work/scripts/Y5_R2FR_4971_parent_field_content_and_two_scale_anchor_projector.py`
- `post-checkpoint-work/source-intake/functional_rg/4971/Bern_R3_field_content_branches.csv`
- `post-checkpoint-work/source-intake/functional_rg/4971/C3_parent_field_content_mismatch.csv`
- `post-checkpoint-work/source-intake/functional_rg/4971/C3_full_parent_splice_scan.csv`
- `post-checkpoint-work/source-intake/functional_rg/4971/C3_full_parent_matching_transport.csv`
- `post-checkpoint-work/source-intake/functional_rg/4971/C3_finite_amplitude_projector.csv`
- `post-checkpoint-work/source-intake/functional_rg/4971/C3_anchor_scale_contract.csv`
- `post-checkpoint-work/source-intake/functional_rg/4971/C3_two_scale_helicity_projector.csv`
- `post-checkpoint-work/source-intake/functional_rg/4971/C3_local_anchor_identifiability.csv`
- `post-checkpoint-work/source-intake/functional_rg/4971/C3_parent_matching_and_anchor_results.json`

Validation is recorded in
`post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4971_VALIDATION.csv`.
All `24/24` checks pass. Validation SHA256:
`6a16885d61f34c2ea57ee29db096bc22abe68cd9d5cc78e5fa9fe3051e9ebd31`.
