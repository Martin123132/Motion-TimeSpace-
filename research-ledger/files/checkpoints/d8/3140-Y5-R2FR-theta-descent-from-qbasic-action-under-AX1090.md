# 3140 - Theta Descent from q-Basic Action under AX1090

Private checkpoint. This follows 3139 by trying to derive:

```text
Theta_parent(delta Phi) - q^* Thetabar(Dq delta Phi) = d beta(delta Phi)
```

rather than treating presymplectic-potential descent as an independent axiom.

## Result

3139 had two apparently separate local-GR kernel premises:

```text
KNO3139_1:
L_parent is basic over Q_obs up to an exact boundary primitive.

KNO3139_2:
Theta_parent descends as q^*Thetabar plus an exact term.
```

3140 collapses these into one stronger condition.

If the parent Lagrangian is strongly q-basic as a local n-form:

```text
L_parent(Phi) = q^* Lbar(Q_obs) + dB(Phi),
```

then variation gives:

```text
delta L_parent
= q^*(Ebar_A Dq^A[delta Phi] + d Thetabar(Dq delta Phi))
  + d delta B.
```

Therefore one may choose the parent presymplectic potential as:

```text
Theta_parent(delta Phi)
= q^*Thetabar(Dq delta Phi) + delta B + dY.
```

So:

```text
Theta_parent - q^*Thetabar = delta B + dY.
```

This is the desired theta-descent relation, modulo the standard horizontal-exact ambiguity in the presymplectic potential.

## What Actually Closes

The following conditional theorem is now exact:

```text
strong q-basic Lagrangian descent
=> presymplectic-potential descent.
```

So theta descent is not a separate miracle. It is forced if the parent action really descends at the local-form level.

For a vertical representative direction:

```text
v in ker(Dq),
```

the quotient term vanishes:

```text
q^*Thetabar(Dq[v]) = 0,
```

leaving:

```text
Theta_parent(v) = delta_v B + dY(v).
```

Then:

```text
omega_parent(v,delta)
```

is boundary-exact, up to variation of the boundary primitive.

This improves the 3139 kernel-null route:

```text
basic action + theta descent + boundary silence
```

becomes:

```text
strong q-basic action + boundary silence.
```

One independent closure-looking clause has been removed.

## What Still Does Not Close

This is not yet a local-GR proof because the current corpus has not parent-signed:

```text
L_parent = q^*Lbar(Q_obs, Rep(Q_obs), sources) + dB
```

for the total action.

The existing sources give skeletons and conditional support:

| source route | status |
|---|---|
| topological projector action skeleton | conditional local stress route |
| quotient configuration principle | conditional presymplectic quotient route |
| primitive relational quotient action | candidate parent-action sketch |
| quotient descent audit | failed for full parent derivation |
| kernel certificate audit | failed for full parent certificate |

So the bottleneck has moved, not vanished.

The exact remaining hard premise is:

```text
strong q-basic total action
```

including:

```text
geometry,
projector/domain sector,
ordinary matter,
clock/mass/charge labels,
source currents,
and boundary terms.
```

## Obstructions Still Alive

The theorem fails if any of these survive:

| obstruction | damage |
|---|---|
| Euler-only descent | equations descend, but theta/charges keep hidden dependence |
| `A(X)R` or `F(sigma)R` | EH prefactor is nonbasic |
| nonzero boundary primitive charge | boundary-exact is not boundary-zero |
| Hodge/metric projector | projector has bulk metric variation |
| matter appended after quotienting | clocks/sources do not inherit q-basicness |
| readout-only EFT | `Q_obs` is postprocessing, not variational quotient |

The important one is the first:

```text
matching equations is not enough.
```

The parent action must descend as a local form, otherwise the symplectic structure can still see the hidden variables.

## Clock/Flow Consequence

This keeps the “internal time may look weird” branch alive but disciplined.

The condition is now:

```text
if internal flow is a vertical q-kernel direction
and the total action is strongly q-basic,
then observed clocks can still read GR time through Q_obs/Rep(Q_obs).
```

If the action is only equation-level or readout-level q-basic, the internal flow may carry hidden charge and must be treated as physical residual, not gauge.

## Claim Gate

| gate | status |
|---|---|
| theta descent from strong q-basic action | `pass_conditional_theorem` |
| strong q-basic total action parent-signed | `fail_for_claim` |
| boundary-exact to zero charge | `fail_for_claim` |
| local GR/Newton/PPN kernel claim | `not_claim_ready` |

## Why This Matters

This is a genuine tightening of the GR-reduction route.

Before:

```text
prove action descent
and prove theta descent.
```

After:

```text
prove strong local-form action descent.
```

Theta descent then follows automatically.

That is exactly the kind of simplification we want: fewer independent assumptions, more derived structure.

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3140_INPUTS.csv` |
| theorem | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3140_THETA_DESCENT_THEOREM.csv` |
| premise collapse | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3140_PREMISE_COLLAPSE_MATRIX.csv` |
| obstruction ledger | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3140_THETA_OBSTRUCTION_LEDGER.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3140_DECISION.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3140_GATE.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3140_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3140_theta_descent_from_qbasic_action.py` |

## Next Target

The broad local-GR route now has one best next target:

```text
3141:
try to construct the strong q-basic total action clause
L_parent = q^*Lbar(Q_obs, Rep(Q_obs), sources) + dB.
```

That is the direct route to GR/Newton reduction.

But if we want the cleaner short punch instead of another broad action audit, the better tactical fork is:

```text
EM/Poynting route:
unique Maxwell F^2
+ charge lattice inheritance
+ Hilbert stress/source current owner.
```

That fork attacks:

```text
b_alpha,
EM stress,
Poynting vector readout,
and calibrated source coupling.
```

Both routes are aligned. The broad route is more fundamental; the EM route is narrower and may produce a testable win faster.
