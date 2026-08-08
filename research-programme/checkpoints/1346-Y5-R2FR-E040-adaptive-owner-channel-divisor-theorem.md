# 5330 - E040 adaptive owner-channel divisor theorem

## Resolvent route

The proposed transfer-function shortcut is rejected for the actual E040
object.  The owner denominator `F_X` is a scalar physical pair invariant, and
the selected response `C_X` is a winding-weighted KLT/soft-subtracted collision
residue.  The implementation does not construct `C_X=c^dagger M^-1 b`, so a
left/right zero-mode overlap would be an invented representation rather than a
derivation.

## Correct theorem

Let `F(E,x)` and `N(E,x)` be jointly analytic near a simple owner branch
`F(E_p(x),x)=0`, with `partial_E F != 0`.  The implicit-function theorem makes
`E_p(x)` analytic.  Local analytic division gives

```text
N(E,x) = F(E,x) Q(E,x) + r(x),
r(x)   = N(E_p(x),x).
```

Therefore

```text
C(E,x) = Q(E,x) + r(x)/F(E,x),
Res[C(E,x) dE, E_p(x)] = r(x)/partial_E F(E_p(x),x).
```

The pole is removable exactly when `r(x)=0`; it is material when `r(x)!=0`.
Under any nonsingular analytic energy coordinate `E=phi(xi,x)`, the residue of
the one-form is invariant and the zero/nonzero classification is unchanged.
This is the coordinate-transfer statement that the adaptive controller needs.

The theorem does not license extrapolation from finitely many coordinates.
Until an exact identity `r(x)=0` is derived for a whole family, every newly
encountered adaptive coordinate must execute the same divisor test.  The
classifier is therefore algorithmic and transferable, not a node exception
list.

## Live adaptive test

- current unresolved descendants: `30`;
- certified: `30`;
- removable bounded-zero: `21`;
- stable material: `9`;
- maximum removable residue envelope:
  `5.56243897158e-09`;
- maximum material residue relative spread:
  `4.14071207473e-05`.

- `MC04_SM_DM / MC04_P01 / direct:L:s14`: `4` adaptive rows, class `MATERIAL`, resolved-history agreement `True`.
- `MC04_SP_DM / MC04_P02 / direct:R:s01`: `21` adaptive rows, class `REMOVABLE`, resolved-history agreement `True`.
- `MC04_SP_DP / MC04_P01 / direct:shared:s13`: `5` adaptive rows, class `MATERIAL`, resolved-history agreement `True`.

Validation: **PASS**.

## Claim boundary

Checkpoint 5330 certifies the preserved 30-pole E040 seed and provides the
reusable local divisor algorithm.  Evolving controller aggregates do not mutate
that source-bound seed, while every unseen coordinate still executes the full
divisor test.  It does not yet complete the
E040 integral, the seven-rung regulator-zero limit, the decay-angle integral,
the UV coefficient, local GR, or full MTS.  No future coordinate is classified
without running the divisor controls unless a separate exact family identity
is proved.
