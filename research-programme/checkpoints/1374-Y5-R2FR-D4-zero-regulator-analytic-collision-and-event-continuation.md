# 5358: D4 zero-regulator analytic collision and event continuation

## Decision

`D4_ZERO_REGULATOR_COLLISION_AND_EIGHT_EVENT_CONTINUATION_PASS__DERIVE_ENDPOINT_COEFFICIENT_LIMIT`

The old all-events simple-collision-root premise is not correct: `E01` and `E04` are double roots.  This does not kill the branch.  The parent collision discriminant is an exact square, so the selected root has an explicit analytic expression through both crossings.

## Exact reduction

With `R=sqrt(1-e)`, signed soft cosine `c`, signed decay cosine `d`, `Q=w^2=(1-t)/(1+t)`, and `t=-9+i epsilon`, the representative collision equation is

`y F=A y^2+B y+C`,

and its discriminant obeys

`B^2-4AC=(1-c^2) P14^2/4`.

The finite-regulator parent branch is exactly the minus branch

`y_-=sqrt(1-c^2)(1+d)F1/[sqrt(1-d^2)(1+c)F2]`,

while the nonsingular `g3` chart fixes `z=w(1+c)/sqrt(1-c^2)`.  Therefore the two `s14` double roots are analytic crossings, not generic square-root branch points.

The three material surfaces reduce to

- `s14=4 Q R P14/(F1 F2)`;
- `s01=4 R P01/(F1 F2)`;
- `s13=4 e R(1+Q) P13/(F1 F2)`.

Each `Pj` is at most quadratic in `R`.  At `Q=-5/4` the eight events are solved by `Pj=H=0` for support contacts or `Pj(R=0.01)=0` for energy-endpoint exits.

## Zero-regulator events

| event | surface | class | |c| | e | margin slope |
|---|---|---|---:|---:|---:|
| E01 | direct:L:s14 | DESINGULARIZED_ANALYTIC_DOUBLE_ROOT | 0.75346522468300165363476755521417634 | 0.77318732859473890651318695395162713 | 2.2970580854711887298989174904101346 |
| E02 | direct:L:s01 | SIMPLE_COLLISION_ROOT | 0.80888852291623941992885205013033255 | 0.95218980121602248542332096666117173 | 1.6463094445089550867030975703751584 |
| E03 | direct:shared:s13 | SIMPLE_COLLISION_ROOT | 0.8504557785095030480999568399891138 | 0.94850606201710205279721620707483208 | 15.591289893556649558755228429561677 |
| E04 | direct:L:s14 | DESINGULARIZED_ANALYTIC_DOUBLE_ROOT | 0.85571349449099163869045523026325434 | 0.9999 | -0.17712356922513881094085390171700463 |
| E05 | direct:L:s01 | SIMPLE_COLLISION_ROOT | 0.85511152626562415547366374942856675 | 0.9999 | -0.11514163564461726438843204458209198 |
| E06 | direct:shared:s13 | SIMPLE_COLLISION_ROOT | 0.8565604503966873969396805050472519 | 0.9999 | -0.73894135002562328675296119418582311 |
| E07 | direct:shared:s13 | SIMPLE_COLLISION_ROOT | 0.85715641656853537085427144632163334 | 0.9999 | 0.6151667986292799979868349115610215 |
| E08 | direct:shared:s13 | SIMPLE_COLLISION_ROOT | 0.87086393241273253874544114360198057 | 0.77703893377502144769093128536730451 | -35.051056537408997380231424884283743 |

## What is proved here

- Parent coefficient reconstruction maximum relative error: `1.387518264031467e-15`.
- Perfect-square identity maximum relative error: `2.653626254071893e-15`.
- Seven-rung material-polynomial maximum residual: `1.1353296308011294e-07`.
- Minimum material `R` Jacobian: `0.0603990028056579`.
- Minimum event/support Jacobian: `0.06632071938384687`.
- Minimum support-margin slope magnitude: `0.11514163564461727`.
- Six events have ordinary simple collision roots; `E01` and `E04` use the exact desingularized double-root branch.

## Claim boundary

This closes the local collision/event-geometry obstruction behind checkpoint 5357.  It does **not** yet prove the endpoint coefficient limit or the integrated D4 regulator-zero limit: the direct zero-limit of the endpoint numerator/residue factors still has to be derived.

No local-GR, UV, full phase-space, or full-MTS claim is made.
