# 4969 - p8 canonical repair, pure-Einstein iterated source and primitive response

Marker: `MTS_4969_P8_CANONICAL_EINSTEIN_RESPONSE`.

Formal marker: `PPC4161_P8_CANONICAL_EINSTEIN_SPLIT_4969`.

Date: `2026-07-13`.

Status: private analytic and executable checkpoint. This checkpoint repairs
the p8 canonical scaling used in 4967-4968, derives the exact part of the
pure-Einstein three-loop structure fixed by lower-order amplitudes, isolates
the genuinely primitive simple-pole vector, and propagates all pieces as
separate responses. It does not set the primitive vector to zero and does not
claim a complete finite p8 amplitude or full MTS. The source normalization was
reaudited on 2026-07-13: the canonical repair survives, while the physical
Einstein `R3` coefficient and its iterated response are corrected below.

## 1. Canonical normalization repair

The retained p8 action is

```text
S=(16pi G)^-1 int sqrt(-g)[R+b_i O8_i],
[O8]=8, [b_i]=-6.
```

Define

```text
g=k^2G,
v_i=k^6b_i,
B_i=b_i/G^3=v_i/g^3.
```

If `beta_vi=6v_i+F_i`, the chain rule gives

```text
beta_Bi
 =beta_vi/g^3-3(beta_g/g)B_i
 =[6-3beta_g/g]B_i+F_i/g^3.
```

Therefore the formula `[4-2beta_g/g]B_i`, used in the trajectory part of
4967-4968, corresponds to `v/g^2` and is inconsistent with the declared
`B=v/g^3` normalization. At the non-Gaussian fixed point the corrected
triangular p8 block is

```text
M_p8=diag(6,6),
B_i*=-source_i*/6.
```

Both directions remain irrelevant in the convention of the parent stability
analysis, so the relevant-parameter count is unchanged. The C3, O4 and CFF
amplitude/source derivations in 4967-4968 are not removed; only their
homogeneous p8 propagation and fixed boundary are superseded.

## 2. Exact three-loop split

Bern et al.'s direct action-normalized physical running gives, for the two
pure-GR graviton states,

```text
dc_R3/dL=(kappa/2)^2*2/[240(4pi)^4],
C_R3=24c_R3/kappa^2=(3/(4pi))A_C3,
dC_R3/dL=1/[20(4pi)^4],
dA_C3/dL=1/(3840pi^3).
```

Two primary-source comparators do not numerically agree with that direct
translation. Baratella et al. print `1/[2(4pi)^4]` in their amplitude
coordinate, ten times the Bern-mapped value under their stated three-point
normalization. The 2026 published FRG article prints `1/(7680pi^3)`, one half
of the Bern action-normalized `A_C3` source. These coefficients are retained
as explicit normalization discrepancies; they are neither averaged nor added
as a second multiplicative beta term. The physical branch below uses the
direct Bern action/log-amplitude equation.

The one-insertion helicity mixing is

```text
dC_R4/dL=-C_R3/(8pi^2),
dC_R4prime/dL=0.
```

Writing the genuinely primitive three-loop simple-pole coefficients as

```text
p_minus=xi_minus/(4pi)^6,
p_plus =xi_plus /(4pi)^6,
```

the exact RG solution is

```text
C_R4(L)=C_R4(0)-C_R3(0)L/(8pi^2)
         -beta_C_R3 L^2/(16pi^2)+p_minus L,

C_R4prime(L)=C_R4prime(0)+p_plus L.
```

Using `C_R4=B_minus/(128pi^3)` and
`C_R4prime=B_plus/(128pi^3)` gives

```text
B_minus(L)=B_minus(0)-12A_C3(0)L
            -L^2/(640pi^3)+xi_minus L/(32pi^3),

B_plus(L)=B_plus(0)+xi_plus L/(32pi^3).
```

Thus the RG-forced pure-Einstein iterated vector is

```text
[Delta B_C,Delta B_t]=[-1,+1]L^2/(1280pi^3),
Delta B_plus=0.
```

Solodukhin's pole recurrence independently makes the logical split explicit:

```text
V_2,3=(2/3)v_1,2 V_1,3^(2),
V_3,3=0,
V_1,3^(0)=new single-pole input.
```

The higher-pole/iterated part is fixed by lower orders. The primitive
single-pole vector is not fixed by the recurrence. A targeted primary-source
sweep found no explicit calculated pure-Einstein three-loop four-graviton
single-pole coefficient to import; absence from the sweep is not a zero
theorem.

## 3. Functional-to-on-shell matching gate

The existing natural-Type-II trajectory has the asymptotic fit

```text
dA_C3/dlnk in
[-3.67837938995e-5,-3.67837938994e-5].
```

The physical pure-GR on-shell result is

```text
dA_C3/dlnmu=+8.39883709198e-6.
```

These are different schemes and the parent also contains the motion sector,
so the sign and magnitude mismatch is not by itself a contradiction. It does
mean that the 4967 functional C3 source cannot be called the exact pure-GR
double logarithm. Adding both would double count before a finite
Wilsonian-to-on-shell matching calculation. Checkpoint 4969 therefore keeps
the exact on-shell contribution as a separate linear response.

## 4. Canonical-repaired known-source trajectory

The known C3, O4-squared and CFF-squared sources were reintegrated with

```text
beta_BC=[6-3beta_g/g]B_C
        -6h_C3/g
        +u_O4^2(1-eta_psi/10)/(pi g^2)
        -79g_CFF^2/(280pi g^2),

beta_Bt=[6-3beta_g/g]B_t
        +6h_C3/g
        -79g_CFF^2/(280pi g^2).
```

All four `N=6,N=8` integrations succeed. The corrected N8 bracket is

```text
0.0137843312491 <= B_C <= 0.0137851876261,
-0.0121806559340 <= B_t <= -0.0121803370306,

0.0259646682797 <= B_minus <= 0.0259658435602,
0.00160399421857 <= B_plus <= 0.00160453169210.
```

The maximum N6-to-N8 relative displacement is
`4.78786867955e-8`. Relative to 4968, the canonical repair changes the N8
coordinates by at most `1.476e-4` in absolute value.

## 5. Exact IR response of the missing pieces

For a declared weak-gravity matching point, the code integrates the exact
linear Green functions for

```text
dA_EH/dt=1/(3840pi^3),
d(delta B_minus)/dt=H_B delta B_minus-12A_EH
                    +xi_minus/(32pi^3),
d(delta B_plus)/dt =H_B delta B_plus
                    +xi_plus/(32pi^3),
H_B=6-3beta_g/g.
```

At `g_match=10^-2`, the two N8 schemes agree to the displayed precision:

```text
Delta ln k                         =-9.2521922,
iterated Delta B_minus             =-0.0043074735,
iterated Delta B_plus              =0,
Delta B_minus per xi_minus         =-0.0092035633,
Delta B_plus per xi_plus           =-0.0092035633,
matching-boundary transfer         =0.77827655.
```

The iterated response differs from the fixed-G analytic double logarithm by
only `0.147%`; at `g_match=10^-6` the difference falls below `5.7e-7`.
This validates the weak-gravity transfer while displaying its matching-scale
dependence rather than hiding it in a fitted endpoint.

The response is physically important for four-graviton helicity predictions:
at the earliest declared match it is about 17 percent of the known-source
`B_minus` endpoint and cannot be silently dropped. It is nevertheless harmless
for the inherited static compact gate.
The canonical-repaired known-source metric response remains below

```text
9.75814718068e-234.
```

Even one primitive helicity coefficient would need
`|xi|~3.07e231` to saturate the strictest static row at the earliest declared
matching point. Static compact data therefore cannot determine this
three-loop vector. Conditional Planck-energy contact partial-wave budgets are
also emitted with the Baratella/Jacob-Wick normalization; they are diagnostics,
not evidence that the EFT is valid at `E=M_P`.

## 6. Decision

```text
p8 canonical chain rule                    = repaired;
p8 fixed subblock                          = diag(6,6);
new relevant p8 parameters                 = zero;
pure-GR R3 physical running                = source locked;
cross-source R3 normalization discrepancies = explicit, not averaged;
R3-to-R4 helicity mixing                   = source locked;
pure-GR iterated three-loop double log     = derived;
primitive three-loop rank-two vector       = isolated, not zeroed;
canonical-repaired known-source trajectory = integrated;
N6/N8 convergence                          = pass;
static compact known-source gate           = pass;
functional/on-shell C3 finite matching     = open;
primitive xi_minus and xi_plus             = open;
full finite parent p8 vector               = open;
exact all-operator compact GR              = false;
full MTS                                   = false.
```

The next calculation should perform the weak-scale
Wilsonian-to-on-shell `C_R3` matching and construct the corresponding two
four-graviton matching constants. If the primitive three-loop amplitude
cannot be calculated, `xi_minus,xi_plus` must remain explicit physical EFT
coordinates rather than being silently set to zero.

No GitHub action is authorized by this checkpoint.

## 7. Outputs

- `post-checkpoint-work/scripts/Y5_R2FR_4969_p8_canonical_Einstein_split.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4969_p8_corrected_trajectory_and_primitive_response.py`
- `post-checkpoint-work/source-intake/functional_rg/4969/p8_canonical_scaling_repair.csv`
- `post-checkpoint-work/source-intake/functional_rg/4969/pure_Einstein_iterated_primitive_split.csv`
- `post-checkpoint-work/source-intake/functional_rg/4969/functional_to_onshell_C3_matching_diagnostic.csv`
- `post-checkpoint-work/source-intake/functional_rg/4969/p8_canonical_repaired_fixed_point.csv`
- `post-checkpoint-work/source-intake/functional_rg/4969/p8_canonical_repaired_GR_connected_trajectory.csv`
- `post-checkpoint-work/source-intake/functional_rg/4969/pure_Einstein_IR_matching_response.csv`
- `post-checkpoint-work/source-intake/functional_rg/4969/primitive_and_matching_boundary_budget.csv`
- `post-checkpoint-work/source-intake/functional_rg/4969/p8_canonical_repaired_static_compact_response.csv`
- `post-checkpoint-work/source-intake/functional_rg/4969/p8_corrected_trajectory_primitive_response_results.json`

## 8. Validation

`P8_Y5_BRR545_4969_VALIDATION.csv` passes `26/26` deterministic checks.
SHA256: `3fb709b4a3771f1dd6d22fb22d8711c04e59648de1d224d59f0ff907c5ee43bc`.

The gate checks primary-source and result hashes, script syntax, canonical
normalization, exact iterated coefficients, primitive rank, all four fixed
points and trajectories, N6/N8 convergence, compact response, canonical
register rows, 4967-4968 supersession banners, placeholder absence in new
outputs, and absence of bytecode/search-dump debris. Claim promotion remains
false and no GitHub action occurred.
