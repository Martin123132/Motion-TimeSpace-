# 135 - High-Sound-Speed or Auxiliary Memory Owner

Private theorem / EFT-owner checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 134 showed:

```text
subhorizon memory perturbation corrections are numerically negligible for the
checkpoint-130 SDSS/eBOSS growth rows if the parent stress has high sound speed
or an equivalent smoothing mechanism.
```

But that was still conditional.

This checkpoint asks:

```text
Can we give the memory sector a concrete high-sound-speed owner, or must it be
left as an auxiliary/geometric constraint target?
```

## 2. Machine Artifact

Script:

```text
research-programme\scripts\high_sound_speed_or_auxiliary_memory_owner.py
```

Run:

```text
research-programme\runs\20260531-192900-high-sound-speed-or-auxiliary-memory-owner
```

Generated:

```text
source_register.csv
canonical_reconstruction.csv
mechanism_ledger.csv
reconstruction_summary.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
effective_high_sound_speed_owner_exists_parent_derivation_missing
```

Claim ceiling:

```text
effective_high_sound_speed_owner_not_parent_derivation
```

## 3. Effective Canonical Owner

The locked memory background is:

```text
rho_mem / rho_crit0 = 1 - Omega_m0 + B_mem A(N)
N = ln(1+z)
B_mem = 2/27
```

with:

```text
A(N) = 1 - exp[-(N/u3)^3]
u3 = 1/4
```

The effective equation of state is:

```text
1 + w_mem = B_mem A_N / [3 rho_mem]
```

Since:

```text
1 + w_mem >= 0
```

the background can be represented by a canonical scalar owner:

```text
S_mem = integral sqrt(-g) [-1/2 (partial phi)^2 - V(phi)]
```

with:

```text
K / rho_crit0 = rho_mem (1+w_mem) / 2
V / rho_crit0 = rho_mem (1-w_mem) / 2
dphi/dN = sqrt[3 Omega_mem(a) (1+w_mem)]
```

For a canonical scalar:

```text
c_s^2 = 1
```

so the high-sound-speed suppression used in checkpoint 134 has a concrete effective-field owner.

## 4. Reconstruction Checks

Reconstruction summary:

| Check | Value | Readout |
|---|---:|---|
| field excursion `0 <= z <= 3` | `0.14537206381984683 Mpl` | small sub-Planckian |
| minimum `w_mem` | `-1.0` | non-phantom |
| maximum `1+w_mem` | `0.15878320641320592` | mild roll |
| maximum canonical `K/rho_crit0` | `0.058044913849524114` | positive kinetic |
| minimum canonical `V/rho_crit0` | `0.6656836460168841` | positive potential |
| maximum `|dphi/dN|` | `0.5166995841704753 Mpl` | finite roll |
| failed reconstruction checks | `0` | pass |

Peak rolling occurs around:

```text
z ~= 0.24
w_mem ~= -0.8412
```

This is exactly the activation interval. Outside it, the field freezes and the memory sector behaves close to `w=-1`.

## 5. What This Buys Us

This gives a real effective stress owner:

```text
T_mem^munu = partial^mu phi partial^nu phi
             - g^munu [1/2 (partial phi)^2 + V(phi)]
```

For this owner:

```text
no ghost: K >= 0
no gradient instability: c_s^2 = 1
subhorizon perturbations: suppressed
Bianchi conservation: automatic if minimally coupled
```

So checkpoint 130 is no longer merely:

```text
pretend memory is smooth.
```

It can be interpreted as:

```text
the late-time subhorizon limit of an effective high-sound-speed memory scalar.
```

That is a meaningful upgrade.

## 6. What This Does Not Buy Us

This is not yet a parent MTS derivation.

Reason:

```text
V(phi) was reconstructed from the locked background A(N).
```

Therefore it does not derive:

```text
B_mem = 2/27
p = 3
u3 = 1/4
the memory determinant I_M
the S_cell owner
the auxiliary/geometric exact smooth constraint
```

It is an effective-field owner for the stress and sound speed, not the fundamental action that predicts the locked branch.

So the claim ceiling remains:

```text
effective EFT support, not fundamental derivation.
```

## 7. Mechanism Ledger

| Mechanism | Verdict | Meaning |
|---|---|---|
| canonical reconstructed memory scalar | best effective owner, not parent derivation | gives `c_s^2=1` and a healthy reconstructed stress |
| k-essence memory scalar | open, more flexible, less clean | can tune sound speed but risks becoming a function-fitting knob |
| auxiliary constrained memory | best exact route, not derived | could remove the scalar mode completely |
| geometric divergence-free counterstress | open but heavy | could evade perfect-fluid obstruction if a true identity exists |
| controlled exchange `Q^nu` | last resort | dangerous unless parent-derived and locally silent |

Current best split:

```text
Use canonical reconstruction as the effective late-time owner.
Keep auxiliary/geometric memory as the exact parent-theory target.
```

## 8. Gates

Gate results:

| Gate | Status | Evidence |
|---|---|---|
| canonical background reconstruction | pass | failed reconstruction checks = `0` |
| high-sound-speed owner | pass effective | canonical scalar has rest-frame `c_s^2=1` |
| field excursion reasonable | pass | `Delta phi/Mpl = 0.145372` from `z=0` to `z=3` |
| parent derivation of `p,u3,B_mem` | fail | potential is reconstructed from locked `A(a)` |
| exact auxiliary smoothness | open | auxiliary/geometric route still lacks Bianchi/boundary owner |
| growth proxy status | retained not promoted | effective owner explains safety, not origin |

## 9. Interpretation

This is the cleanest growth-sector position so far.

We now have three layers:

### Empirical Layer

```text
locked 2/27 background scores competitively in SN+BAO, BAO-only, BAO+H(z),
and the first SDSS/eBOSS growth gate.
```

### Effective-Field Layer

```text
a canonical reconstructed memory scalar can own the background stress with
c_s^2=1, positive kinetic energy, positive potential, and small field excursion.
```

### Parent-Theory Layer

```text
still missing: derivation of the potential / activation / amplitude from
S_cell and S_stress.
```

Boxing-score version:

```text
We found a legal glove, not the whole training camp.
The growth jab now has an effective-field hand behind it.
But the parent theory still has to explain why that hand exists.
```

## 10. Decision

Decision:

```text
high_sound_speed_owner_status =
effective_owner_exists_parent_derivation_missing
```

Meaning:

```text
checkpoint 130 can be treated as a robust late-time subhorizon EFT target;
checkpoint 134 explains why corrections are tiny;
this checkpoint supplies a healthy canonical owner for that suppression;
but the locked branch remains closure-level until the parent action predicts it.
```

Do not promote growth as derived MTS perturbation theory.

Do not demote the growth branch.

Promote the task itself:

```text
derive V(phi), or an equivalent auxiliary/geometric memory constraint, from
S_cell/S_stress rather than reconstructing it.
```

## 11. Next Target

Create:

```text
136-memory-action-potential-owner-attempt.md
```

Purpose:

```text
try to derive the reconstructed V(phi), or an equivalent non-propagating memory
constraint, from the existing determinant/cell memory structure.
```

Pass condition:

```text
show that I_M = det(Q_coh), X_FLRW = 4N, and the memory stress action imply the
same effective potential/background without fitting V(phi) after the fact.
```

Fail condition:

```text
V(phi) remains merely reconstructed from A(N), in which case the growth sector
is an effective closure benchmark rather than a derived parent-theory sector.
```
