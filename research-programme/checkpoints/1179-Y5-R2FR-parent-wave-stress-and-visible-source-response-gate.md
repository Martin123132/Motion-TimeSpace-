# 5163 - Parent wave stress and visible-source response gate

Marker: `MTS_5163_PARENT_WAVE_AND_VISIBLE_SOURCE_RESPONSE_GATE`.

Date: `2026-07-20`.

## Decision

Checkpoint 5162 rejected ordinary free collisionless collapse as the source
of the resolved parent transition. Checkpoint 5163 now varies the terms that
the existing parent actually owns rather than inventing a galaxy force.

The canonical Madelung stress is derived exactly. For
`n_q=x^q/(1+x^q)` and the density implied by its circular-speed support,

```text
eta_Q(R_n)=C_q [hbar/(m v_infinity R_n)]^2,
C_q=q(2q^4+6q^3+9q^2+12q+8)/[2(q+2)^3].
```

At the frozen `1e-20 eV` mass its UGC09133 value is
`2.1752123578548805e-09`. Requiring every current halo mapping
to remain above the instantaneous equality Jeans mass gives the weaker
universal floor `8.882479043701029e-23 eV`; even there the
UGC09133 wave fraction is only `2.7569778620807335e-05`.
Canonical wave pressure therefore cannot supply the order-one transition
change by itself on this branch.

The already-derived essential `X^2` and Weyl-kinetic operators are smaller
still. Their largest conservative fractional transition envelopes are
`1.1641800018388254e-116` and
`4.3844376752694736e-234`. No unsigned coefficient was inserted.

## Visible-source correction

The numerical audit exposes a different omission: checkpoint 5162 evolved
the cosmic total-matter field but did not include the condensed UGC09133
baryonic source. The parent already couples that source through the same
Einstein residue used for local GR and Newton. With the locked
`ML_disk=0.5`, `ML_bulge=0.7` convention, the measured baryonic acceleration
at `R_n` is `0.9031622469349835` times the target
motion acceleration. It is not perturbatively small.

A spherical circular-orbit adiabatic invariant was therefore used as a
controlled upper-response bracket,

```text
r_i M_X,i(r_i)/f_X
 =r_f[M_X,i(r_i)+epsilon_ad M_b,eq(r_f)].
```

`epsilon_ad` is explicitly a sensitivity coordinate, not a new coupling.
The zero-response rows reproduce checkpoint 5162. Full response moves the
fine-grid transition from `q=3.688824512640322` to
`q=0.122574399396473` and changes the no-refit velocity-
squared RMSE from `0.42140386547507747` to
`0.145472021520355` dex. The response therefore crosses
the parent `q`; the inverse crossing occurs at
`epsilon_ad=0.051006101448935366`, but that value is not
promoted because solving for it uses the target exponent.

This is the important result: the known universal visible coupling has enough
leverage to change the failed transition, whereas the canonical wave and
known local gradient terms do not. The adiabatic bracket does not derive the
assembly history and does not jointly select the parent profile. The next
calculation must evolve visible and motion components together under the same
Poisson/Einstein source, with the baryon fraction and initial covariance fixed
before reading `q`. It may not turn the inverse efficiency into a fitted
coupling.

## Claim boundary

```text
canonical parent wave stress derived                 = yes;
canonical wave stress sufficient at frozen mass      = no;
known essential gradient operators sufficient        = no;
condensed visible source omitted by 5162              = yes;
same-G_N visible source has transition leverage       = yes;
adiabatic response selects q without inversion        = no;
coupled baryon-motion assembly derived                = no;
local GR/Newton/Maxwell branch modified               = no;
galaxy or full-MTS claim                              = false.
```

All `24` validation rows pass. All outputs remain
nonclaim. Source hashes are unchanged; the protected `formalization-workbench`
digest is `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. The galaxy source
was read-only and no GitHub action occurred.
