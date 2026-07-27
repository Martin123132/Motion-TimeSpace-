# 3143 - Same-Current Owner from Action Variation under AX1090

Private checkpoint. This follows 3142 by taking the proof-facing fork:

```text
same T_Q current owner theorem,
J_Q = delta S_matter / delta A_Q,
with no q_A(Xhat), c_A(Xhat), w_A, kappa_A, or post-readout current weights.
```

## Result

3143 proves the exact conditional theorem:

```text
q-basic matter action
+ fixed charge labels
+ variation-before-readout current definition
+ no hidden/source current weights
=> same-current owner
=> delta_J = 0.
```

Define the visible EM current by varying the same matter action that couples to the visible connection:

```text
J_Q^mu
:= (1/mu_obs) delta S_matter / delta A_Q_mu.
```

If:

```text
S_matter = Sbar_matter[q(Phi), Psi, A_Q(q), n_A, theta_A],
Dq[v] = 0,
Lie_v n_A = 0,
Lie_v theta_A = 0,
Lie_v A_Q = 0,
Lie_v mu_obs = 0,
```

and the parent grammar forbids:

```text
c_A(Xhat) A_Q J_A,
q_A(Xhat) A_Q J_A,
w_A S_A,
kappa_A T_A,
post-variation current selectors,
radiative/readout current re-entry,
```

then:

```text
Lie_v J_Q^mu = 0.
```

So:

```text
delta_J = 0,
beta_source_alpha = 0 for this channel,
Delta_T_EM^J = 0,
Delta(GM)_J = 0.
```

## What Actually Closes

The derivation route is sharper than a Ward identity.

Ward conservation gives:

```text
nabla_mu J_Q^mu = 0.
```

But same-current ownership needs:

```text
Lie_v J_Q^mu = 0.
```

The latter follows only when `J_Q` is the functional derivative of one q-basic matter action before readout:

```text
Lie_v J_Q^mu
= Lie_v[(1/mu_obs) delta S_matter / delta A_Q_mu]
= (1/mu_obs) delta(Lie_v S_matter)/delta A_Q_mu
  + zero readout terms
= 0.
```

This is the missing normalization statement. It does not merely say the current is conserved; it says the hidden representative direction cannot reweight the current.

## What Still Does Not Close

The current corpus does not yet parent-sign the grammar exclusion:

```text
no c_A(Xhat),
no q_A(Xhat),
no w_A,
no kappa_A,
no post-readout current selector,
no radiative current re-entry.
```

So:

```text
delta_J = 0
```

is not promoted as an MTS theorem.

The exact remaining blocker is now:

```text
prove those slots are untypeable in the parent action,
or keep delta_J as a finite residual.
```

## Projection Classification

If `delta_J` survives, its physical effect depends on where it enters.

| insertion stage | material Coulomb | source GM | WEP | R10 | classification |
|---|---|---|---|---|---|
| q-basic/forbidden | no | no | no | no | `ZERO_BY_ACTION_VARIATION` |
| before Maxwell solve / Hilbert variation | yes | yes | yes if differential | yes if source/test legs exist | `FINITE_BEFORE_VARIATION_PROJECTS_BOTH` |
| universal calibrated current unit | raw yes, observable no | raw yes, observable no | no unless differential | no unless source/test differs | `FINITE_CALIBRATION_ONLY` |
| post-variation readout selector | maybe | no | maybe | maybe | `FINITE_READOUT_ONLY_NO_GM` |
| radiative/source threshold | yes if action-level | yes if stress changes | maybe | maybe | `FINITE_EFFECTIVE_ACTION_AMBIGUOUS` |

This prevents the two bad shortcuts:

```text
delta_J is automatically harmless because calibration.
```

and:

```text
any delta_J automatically ruins local GR.
```

The insertion stage decides the observable.

## Finite Residual Rows

If the parent grammar cannot kill the current weights, retain:

| residual | meaning |
|---|---|
| `delta_J` | hidden source/test current normalization derivative |
| `C_J_TA6V_minus_PtRh10` | one-channel Coulomb/material response from 3122 smoke convention |
| `abs(delta_J)_one_channel_envelope` | `7.035851579866e-13` smoke envelope, nonclaim |
| `Delta_GM_J` | source-mass/orbital GM residual if current changes EM stress before Hilbert variation |
| `beta_source_alpha` | WEP/R10 source-test alpha current normalization residual |

The 3122 numerical envelope is useful pressure, not evidence of an MTS prediction. It assumes:

```text
one Coulomb material channel,
tau_EM=1,
C_relax=0,
no cancellation,
TA6V-PtRh10 smoke convention,
and no source-GM/R10 projection claim.
```

## Claim Gate

| gate | status |
|---|---|
| same-current owner from action variation | `pass_conditional_theorem` |
| parent grammar forbids all hidden current/source slots | `fail_for_claim` |
| `delta_J` / `beta_source_alpha` zero | `not_claim_ready` |
| finite `delta_J` product prediction | `not_claim_ready` |

## Why This Matters

This is a real coupling advance.

The theory no longer says:

```text
there is a conserved current, so source coupling is fine.
```

It says:

```text
the current must be the functional derivative of the same q-basic matter action,
before readout,
with no hidden current/source weights.
```

That is the exact parent-action route to calibrated EM current normalization. It also connects directly to the local-GR/Newton source problem because a before-variation current weight changes:

```text
F[J],
T_EM[J],
material Coulomb response,
source GM,
WEP/R10 source-test products.
```

So yes: the coupling really is one of the key throats.

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3143_INPUTS.csv` |
| same-current theorem | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3143_SAME_CURRENT_OWNER_THEOREM.csv` |
| projection classifier | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3143_DELTAJ_PROJECTION_CLASSIFICATION.csv` |
| residual rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3143_CURRENT_OWNER_ZERO_OR_RESIDUAL_ROWS.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3143_GATE.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3143_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3143_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3143_same_current_owner_action_variation.py` |

## Next Target

The next target is now precise:

```text
3144:
prove the no-c_A/no-source-prefactor parent grammar,
or select the finite delta_J insertion branch.
```

Direct target:

```text
Allowed[S_parent]
contains no source-only slot c_A(Xhat) A_Q J_A
and no w_A S_A
unless the coefficient is fixed representation/current data.
```

If that proof fails, stop trying to zero `delta_J` and choose one finite branch:

```text
before-variation,
readout-only,
calibration-only,
or effective-action.
```

Then continue coefficient/source-bound filling without pretending it is a theorem-zero.
