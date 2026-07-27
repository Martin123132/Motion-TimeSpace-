# 3134 - Parent Quotient Map and Matter Pullback Reduction under AX1090

Private checkpoint. This follows 3133 by writing the actual candidate quotient map target instead of treating `q` as a magic eraser.

## Candidate Map

The minimal parent chart is:

```text
Conf_parent =
{e,g,omega,A_obs,Psi_A,theta_A,Z/Xhat,domain-memory-boundary data, source/worldtube class}.
```

The candidate quotient is:

```text
q: Conf_parent -> Q_obs
```

with:

```text
q(Phi) = (e_obs, g_obs, omega_obs, A_obs, mu_obs, tau_obs, theta_rep, boundary_class_obs).
```

The vertical condition is:

```text
Dq[v_X] = 0
```

on an open local branch, not merely after fitting.

## Matter Pullback

The q-basic matter target is:

```text
S_matter[Phi,Psi;theta] = Sbar[q(Phi), Psi, theta].
```

Then:

```text
delta_v S_matter =
(delta Sbar / delta q) Dq[v]
+ (partial Sbar / partial theta) Lie_v(theta).
```

So if:

```text
Dq[v] = 0
Lie_v(theta) = 0
```

then:

```text
delta_v S_matter = 0.
```

This part is real algebra. It is not enough by itself.

## Reduction Matrix

3134 separates what actually closes from what does not:

```text
formal pass:
- chain-rule variation;
- Hilbert current uniqueness after one common action is fixed.

still fails for claim:
- parent q object;
- open-branch v_X in ker(Dq);
- q-basic ordinary matter functor;
- no source-only species/action-weight slot;
- local GR/Newton implication.
```

That is progress: we no longer have a vague missing coupling; we have a precise proof reduction and a finite leakage fallback.

## Verdict

The quotient route is not promoted.

```text
parent_signed = false
claim_allowed = false
valid_for_claim = false
```

The reason is sharp:

```text
the algebraic chain rule closes conditionally,
but the parent action has not signed q, v_X, matter functor, theta silence,
source-slot exclusion, and boundary/readout no-reentry in one branch.
```

## Leakage Carry-Forward

Because the parent signature is not closed, 3134 carries the 2970 leakage heads forward:

```text
eps_q_parent,
eps_constraint,
eps_factorization,
eps_theta_basic,
J_direct,
J_spurion,
J_nonH,
C_Obs_e,
C_shadow_abs,
DqZ_JA_first_leakage_total.
```

Every one remains:

```text
valid_for_claim = false.
```

## Runner Artifacts

| artifact | path |
|---|---|
| input rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3134_QUOTIENT_MAP_INPUTS.csv` |
| quotient attempt | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3134_QUOTIENT_MAP_ATTEMPT.csv` |
| proof reduction | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3134_PROOF_REDUCTION_MATRIX.csv` |
| leakage fallback | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3134_FINITE_LEAKAGE_CARRY_FORWARD.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3134_GATE.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3134_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3134_parent_quotient_map_matter_pullback_reduction.py` |

## Next Target

3135 should attack the most dangerous surviving clause:

```text
no source-only species/action-weight slot.
```

If that theorem closes, `J_spurion` and much of the WEP/source current obstruction collapses. If it does not, the next honest move is:

```text
fill the first finite leakage bound row, probably J_spurion or J_direct.
```
