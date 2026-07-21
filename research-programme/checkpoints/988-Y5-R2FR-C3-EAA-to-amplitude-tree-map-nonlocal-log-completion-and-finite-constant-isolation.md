# 4972 - C3 EAA-to-amplitude map and nonlocal log completion

Marker: `MTS_4972_C3_EAA_TO_AMPLITUDE_MATCHING`.

Formal marker: `PPC4161_C3_EAA_AMPLITUDE_CONVERSION_4972`.

Status: private source-executed derivation checkpoint. No GitHub action and no
full-MTS or complete-amplitude claim.

## 1. Decision

Checkpoint 4972 makes three calculational advances beyond 4971:

1. the local parent `G_C3 C^3` coefficient is mapped exactly into the Abreu
   finite-amplitude normalization;
2. the complete logarithmic part of the missing nonlocal conversion is fixed
   by RG consistency;
3. the residual obstruction is proved to be exactly one additive finite
   matching constant, not an unspecified function or another field-content
   audit.

The exact tree-level map is

```text
r_C3 := G_C3/G_N,
c_tree = 32 pi^3 r_C3,
A_Bern,tree = -r_C3.
```

The loop-completed physical coordinate is therefore

```text
c_phys(mu_m)=32 pi^3 r_C3^S+delta_c_fin(mu_m).
```

The current local parent calculates `r_C3^S`; it does not yet calculate the
finite nonlocal conversion `delta_c_fin`. Setting `delta_c_fin=0` is retained
as the published local-EFT/Planck-transition prescription only, not promoted
to an exact MTS amplitude prediction.

## 2. Exact action normalization

The selected EAA action contains

```text
L_EAA superset G_C3 C^3.
```

The source-exact amplitude action contains

```text
L_R3 = [c_R3/(4 pi)^4] (kappa/2)^2 Riemann^3,
kappa^2=32 pi G_N.
```

Consequently

```text
[c_R3/(4 pi)^4](kappa/2)^2
  =c_R3 G_N/(32 pi^3).
```

On Ricci-flat four-dimensional backgrounds `C^3=Riemann^3`. Equating the
coefficients gives

```text
c_R3=32 pi^3 G_C3/G_N.
```

The physical finite amplitude depends on

```text
c=c_R3-c_GB/2.
```

Gauss-Bonnet has no strict-four-dimensional tree amplitude, so the essential
tree representative is `c_GB=0`. With the 4971 orientation
`A_Bern=-c/(32 pi^3)`, this proves

```text
A_Bern,tree=-G_C3/G_N.
```

This is an exact normalization bridge. It is not the claim that the finite
loop conversion vanishes.

## 3. Current-parent local-EFT anchor

Checkpoint 4963 selected the finite natural-source envelope

```text
-2.2051899226020373e-5
  <= r_C3^S <=
-2.1871820879230358e-5.
```

The exact tree map gives

```text
-0.021879913239298467
  <= c_tree <=
-0.021701239349867996,

2.1871820879230358e-5
  <= A_Bern,tree <=
2.2051899226020373e-5.
```

Under the explicit source prescription `delta_c_fin=0` at the matching scale,

```text
lambda/mu_m=exp[240 c_tree/N].
```

This yields

```text
SM45, N=-60:
  1.0906839291413455 <= lambda/mu_m <= 1.0914637147218345,

SM45 plus one active motion scalar, N=-59:
  1.0922898012387003 <= lambda/mu_m <= 1.0930839759141602.
```

These are calculated local-EFT matching estimates. They supersede the 4971
zero-offset diagnostic rows, but they remain conditional because
`delta_c_fin` is not derived.

At `s=1`, `t=u=-1/2`, so `stu=1/4`, the exact local C3 insertion predicts

```text
Delta R_pppp = 0.32551859024801993 to 0.32819869858947703,
Delta R_mppp = 0.032551859024801996 to 0.03281986985894770.
```

Every branch satisfies `Delta R_pppp=10 Delta R_mppp` and both helicities
recover the same `A_Bern,tree`.

## 4. Derived nonlocal logarithmic completion

The local source coordinate has the infrared form

```text
r_C3(k)=A_C3^S+B_C3 ln g(k)+...,
g(k) proportional to k^2,

dr_C3/dlnk=2 B_C3,
dc_local/dlnk=64 pi^3 B_C3.
```

The locked parent interval is

```text
B_C3=-1.8391896949746814e-5
     to -1.8391896949719536e-5,

dc_local/dlnk=-0.036496911711962364
              to -0.036496911711908234.
```

The physical amplitude requires

```text
dc_phys/dlnmu=-N/240.
```

Therefore the nonlocal form-factor contribution is not arbitrary. Its exact
required logarithmic slope is

```text
d(delta_c_NL)/dlnmu
  =-N/240-64 pi^3 B_C3.
```

Numerically,

```text
SM45:
  d(delta_c_NL)/dlnmu
    =0.2864969117119082 to 0.28649691171196234,

SM45 plus motion:
  d(delta_c_NL)/dlnmu
    =0.28233024504524157 to 0.28233024504529570.
```

Adding these rows to the local slope reproduces the exact physical state-count
running in all four endpoint checks.

## 5. Finite-constant no-go theorem

At one scale, the two helicity shifts depend on the same combination

```text
c_phys=32 pi^3 r_C3^S+delta_c_fin.
```

The two-helicity coefficient matrix for unknowns
`(r_C3^S,delta_c_fin)` has rank one and nullity one. Its exact null direction
is

```text
delta r_C3^S=epsilon,
delta(delta_c_fin)=-32 pi^3 epsilon.
```

Thus the factor-ten helicity test can detect a wrong operator or projection,
but it cannot split the local Wilson coefficient from the finite nonlocal
conversion. RG consistency fixes the logarithmic slope and leaves the same
single additive constant. This proves that no further manipulation of the
existing zero-momentum local trajectory can determine the complete anchor.

## 6. External truncation comparators

The acquired pure-gravity calculations do not agree on the finite local
coordinate:

```text
2509 natural-regulator branch: r_C3=+3.024098389340624e-6,
2312 minimal-essential branch: r_C3=-3.988e-6.
```

The newer source explicitly distinguishes FRG `k`-running from physical
momentum running and says the latter resides in form factors. These rows are
kept as external truncation comparators, not averaged into the MTS parent and
not used as a bound on `delta_c_fin`.

## 7. Claim boundary

```text
EAA-to-Abreu tree normalization             = exact;
finite local parent r_C3 envelope            = calculated;
dual-helicity local amplitude insertion      = calculated;
factor-ten identity                          = pass;
physical nonlocal logarithmic slope          = derived;
finite conversion identifiability            = rank one/nullity one;
source-prescription lambda estimate           = calculated conditional;
delta_c_fin from full parent form factor      = open;
complete physical four-graviton amplitude     = open;
leading local GR/Newton/Maxwell branch        = retained;
exact all-operator compact GR                 = false;
full MTS                                      = false.
```

## 8. Next calculation

Checkpoint 4973 should calculate the one object still capable of changing the
anchor: the finite part of the momentum-dependent C3 form factor. Build the
projected flow `F_C3,k(s,t,u)` with the UV fixed-point boundary, integrate it
to `k=0`, require the 4972 logarithmic slope and the 4971 factor-ten helicity
identity, and read `delta_c_fin` at one declared subtraction point. If the
cubic nonlocal kernel cannot be constructed from the retained parent, the
honest endpoint is one explicit matched amplitude datum `lambda`, not another
local-flow rerun.

## 9. Outputs

- `post-checkpoint-work/scripts/Y5_R2FR_4972_C3_EAA_to_amplitude_matching.py`
- `post-checkpoint-work/source-intake/functional_rg/4972/C3_EAA_to_amplitude_normalization.csv`
- `post-checkpoint-work/source-intake/functional_rg/4972/C3_local_anchor_estimates.csv`
- `post-checkpoint-work/source-intake/functional_rg/4972/C3_nonlocal_log_completion.csv`
- `post-checkpoint-work/source-intake/functional_rg/4972/C3_finite_conversion_identifiability.csv`
- `post-checkpoint-work/source-intake/functional_rg/4972/C3_helicity_matching_predictions.csv`
- `post-checkpoint-work/source-intake/functional_rg/4972/C3_EAA_to_amplitude_matching_results.json`

Validation passes `20/20` checks in
`post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4972_VALIDATION.csv`.
Validation SHA256:
`47230465dc6ce29d0806bd6f75144505bd6392dad02d1a06d1c2d3efb1d77f70`.
