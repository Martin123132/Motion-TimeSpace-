# 5336 - Fold/pair equivalence and incremental ownership gate

Date: `2026-08-06`

Marker: `MTS_5336_FOLD_PAIR_EQUIVALENCE_INCREMENTAL_OWNERSHIP_GATE`.

## Executive result

Checkpoint 5335 found that a square-root fold with an isotropic critical
discriminant `Delta~|k|^2` produces `1/|k|`. The required corpus audit now
shows that this infrared carrier was already derived and parent-owned at
checkpoints 5181 and 5200:

```text
B_0(k)
 =integral d^3p/(2pi)^3
   1/[p^2(p+k)^2]
 =1/(8|k|).
```

Checkpoint 5336 derives the exact connection. After Feynman
parameterization, the pair bubble is itself a square-root fold integral:

```text
B_m(k)
 =1/(8pi) integral_0^1 dx
  [m^2+x(1-x)|k|^2]^(-1/2).
```

At `m=0`,

```text
Delta_pair=x(1-x)|k|^2,

B_0(k)
 =1/[8pi|k|]
  integral_0^1 dx/[sqrt(x)sqrt(1-x)]
 =1/(8|k|).
```

Thus the retarded-history fold and massless pair threshold belong to the same
square-root universality class. They are not the same microscopic mechanism:
the straight retarded-history toy needs a non-injective map, whereas the
parent-owned pair branch point comes from a two-propagator threshold and
requires no superluminal source history.

This is a useful interpretation and consistency check, but it supplies no
new parent ownership. The fold fixes only the common leading infrared carrier.
It cannot determine the missing crossover exponent
`q=0.7698811733853892`, state preparation, amplitude or outer wall.
The CTP/fold side loop is therefore closed unless a genuinely new
parent-owned composite block appears. The active calculation returns to the
checkpoint-5334 D4 outer regulator ladder.

## 1. Exact square-root equivalence

For

```text
B_m(k)
 =integral d^3p/(2pi)^3
  1/[(p^2+m^2)((p+k)^2+m^2)],
```

use

```text
1/(AB)=integral_0^1 dx/[xA+(1-x)B]^2
```

and shift the loop momentum. The three-dimensional integral gives

```text
B_m(k)
 =1/(8pi) integral_0^1 dx
  [m^2+x(1-x)|k|^2]^(-1/2)

 =atan(|k|/(2m))/(4pi|k|).
```

The factor

```text
Delta_pair^(-1/2),
Delta_pair=m^2+x(1-x)|k|^2
```

is the same fold normal form isolated from the retarded history Jacobian.
The executed transformed Gauss-Legendre integral checks 25
`(k,m/k)` cases against the exact result. The maximum relative discrepancy is
`2.0061e-11`, and every massless row satisfies

```text
|k| B_0(k)=1/8
```

with zero floating-point residual.

The exact statement is:

```text
same singularity class and momentum exponent = yes;
same source map or microscopic dynamics       = no.
```

## 2. Why the literal speed condition is not inherited

For the straight history map used by the maths source, a geometric fold
requires

```text
beta=v/u>1.
```

This condition belongs to that particular non-injective worldline-to-field
map. The pair bubble instead obtains its branch point from simultaneous
massless propagation in loop phase space. Its discriminant vanishes at the
two-particle threshold. It does not require an ordinary source to outrun the
parent light cone.

Therefore checkpoint 5335's causality/Cherenkov warning remains mandatory
only for a literal geometric-history realization. It is not an obstruction
to the already-derived pair-threshold carrier.

## 3. The mass gap is the fold offset

The pair discriminant identifies the exact critical offset:

```text
Delta_0=m^2.
```

For fixed `m>0` and `|k|<<m`,

```text
B_m(k)
 =1/(8pi m)-|k|^2/(96pi m^3)+O(k^4),
```

which is analytic in `k^2`. The exact retained fraction is

```text
B_m/B_0
 =(2/pi) atan(|k|/(2m)).
```

The executed values include

```text
m/|k| = 0.001 -> B_m/B_0 = 0.998726762153;
m/|k| = 0.1   -> B_m/B_0 = 0.874334083622;
m/|k| = 1     -> B_m/B_0 = 0.295167235301;
m/|k| = 10    -> B_m/B_0 = 0.0318045025124.
```

Consequently the fold carrier exists only when the environmental composite
gap obeys

```text
m_eff/|k| -> 0.
```

This restates the checkpoint-5181 gap-collapse requirement in the fold
language; it does not derive the collapse.

## 4. Exact q-nonidentifiability theorem

The target response is

```text
C_q(x)=1/[x(1+x^q)],
x=|k|/mu.
```

Its exact logarithmic slope is

```text
d ln C_q/d ln x
 =-1-q x^q/(1+x^q).
```

Therefore

```text
x->0:        slope -> -1;
x->infinity: slope -> -(1+q).
```

Every `0<q<=1` has the same fold-controlled infrared power. The value of `q`
lives in the crossover and ultraviolet tail, not in the leading fold.
Consequently:

```text
derive square-root fold  != derive q.
```

The sourced Gaussian pair power count remains

```text
q_pair=-2 eta_psi
      =0.1306502061216877,
```

whereas

```text
q_target=0.7698811733853892.
```

The shortfall is `0.6392309672637015`, or `83.03%` of the target.
The maximum known interaction norm
`3.492540005516476e-116` cannot be represented as an order-one correction
to this exponent. The fold interpretation does not alter that prior
ownership result.

## 5. Positivity permits a family; it does not select q

Checkpoint 5149 derives the positive Stieltjes density

```text
rho_C(t)
 =mu^(1+q)[mu^q+t^(q/2)cos(pi q/2)]
  /{
    pi sqrt(t)
    [mu^(2q)+2mu^q t^(q/2)cos(pi q/2)+t^q]
   }.
```

For `0<q<=1` it is nonnegative. Checkpoint 5336 samples
`t/mu^2` across 48 decades for five values of `q`, including the sourced
Gaussian-pair value and the target. The minimum sampled density is
`3.1833e-37` and every row is positive.

This proves compatibility, not selection:

```text
causal positive continuum exists for many q values;
positivity alone cannot choose q_target.
```

A retarded-history weight could represent such a continuum only after the
parent density matrix or CTP boundary functional derives that weight.
Choosing `q(tau)` to reproduce the answer would be a closure.

## 6. Incremental value of the extra maths

The read-only maths source now contributes precisely:

```text
zero-flow interpretation:
  supports the derived-state energy-frame language;

retarded Jacobian:
  independently exposes the square-root fold normal form;

fold universality:
  gives a geometric interpretation of the parent massless pair threshold;

multi-history spectroscopy:
  may later test a derived continuum state.
```

It does not contribute:

```text
a second Poynting source;
a new parent field;
the mass-gap collapse;
the occupied-state preparation law;
the crossover exponent q;
the Hilbert-pair normalization;
a galaxy or full-MTS claim.
```

This correction prevents checkpoint 5335 from being overstated while
retaining its genuinely useful interpretation.

## 7. Decision

```text
square-root fold normal form                          = derived;
massless pair bubble as exact fold integral           = derived;
B_0(k)=1/(8|k|)                                      = reproduced;
literal retarded map = pair threshold                 = false;
superluminal history needed by pair threshold         = false;
nonzero mass removes critical branch                  = derived;
leading infrared fold selects q                       = rejected exactly;
positive spectral response selects q                  = rejected exactly;
known Gaussian pair gives q_target                    = false;
history source derives state preparation              = false;
new parent ownership from checkpoint 5335             = false;
existing local GR/Newton/Maxwell branch                = unchanged;
galaxy or full-MTS claim                               = false.
```

The next active action is not another CTP/fold scan. It is the saved
checkpoint-5334 numerical continuation:

```powershell
.\.venv-score\Scripts\python.exe .\scripts\Y5_R2FR_5334_D4_outer_regulator_ladder_controller.py --mode refinement-run --max-runtime-hours 2
```

## Artifacts

- `scripts/Y5_R2FR_5336_fold_pair_equivalence_and_incremental_ownership_gate.py`
- `source-intake/functional_rg/5336/source_register.csv`
- `source-intake/functional_rg/5336/massless_pair_fold_equivalence.csv`
- `source-intake/functional_rg/5336/retarded_fold_vs_pair_threshold.csv`
- `source-intake/functional_rg/5336/mass_gap_criticality_gate.csv`
- `source-intake/functional_rg/5336/fold_q_nonidentifiability.csv`
- `source-intake/functional_rg/5336/positive_spectral_family_nonselection.csv`
- `source-intake/functional_rg/5336/maths_exploration_incremental_value.csv`
- `source-intake/functional_rg/5336/route_decision.csv`
- `source-intake/functional_rg/5336/fold_pair_equivalence_incremental_ownership_result.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5336_VALIDATION.csv`

All `14/14` validation gates pass. The protected formalization-workbench
digest remains
`0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f`.
No GitHub action occurred.
