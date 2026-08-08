# 3123 - Current-Owner Action Variation or `delta_J` Projection Exclusion under AX1090

Private checkpoint. This follows 3122 by trying to prove same-current ownership from action variation, not from Ward conservation alone, then classifying exactly where `delta_J` projects if the proof clause fails.

## Verdict

The action-variation route is real and sharper than the earlier Ward-current statement:

```text
J_Q^mu := (1/sqrt(-g_pub)) delta S_matter / delta A_Q_mu.
```

If the parent/local action satisfies:

```text
S_matter = sum_A S_A[Psi_A, e_pub(q), A_Q(q), n_A, theta_A],
Dq[v] = 0,
Lie_v e_pub = 0,
Lie_v A_Q = 0,
Lie_v n_A = 0,
Lie_v theta_A = 0,
no c_A(y), q_A(y), w_A(y), kappa_A(y), post-variation selector,
and radiative/readout closure preserves the same functional derivative,
```

then:

```text
Lie_v J_Q^mu = 0.
```

So:

```text
delta_J = 0,
C_J = 0,
Delta_T_EM^J = 0,
Delta(GM)_J = 0.
```

This is a genuine derivation path. But it is not yet a promoted MTS theorem because the corpus still leaves `T_Q`, the no-`c_A(y)` slot, no source-only matter weights, unique `F_Q^2`, and radiative/readout closure unsigned.

If the action-variation proof fails, the projection classification is now sharp:

```text
before-variation/current-source insertion -> material Coulomb + source GM + R10 + possible WEP;
universal calibrated insertion -> raw normalization only, no differential observable unless time/source dependent;
post-variation readout selector -> readout/material/R10 possible, but no EM Hilbert stress/source GM;
forbidden/q-basic insertion -> no projection anywhere.
```

## Source Register

| source_id | path | role |
|---|---|---|
| PAC990 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv` | parent action clauses, including matter functor and EM lock |
| EMLOCK988 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv` | EM lock/current owner blockers |
| ELA989 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv` | current-owner and no-alpha-vertex signature audit |
| 3119 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3119-Y5-R2FR-same-current-owner-or-deltaJ-source-test-residual-priority-under-AX1090.md` | same-current theorem attempt and countermodels |
| 3121 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3121-Y5-R2FR-deltaJ-source-calibration-DeltaGM-bridge-under-AX1090.md` | source `GM` bridge and WEP/source separation |
| 3122 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3122-Y5-R2FR-current-owner-descent-or-CJ-source-coefficient-fill-under-AX1090.md` | first finite `C_J` material coefficient fill |
| 3123-input | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3123_DELTAJ_PROJECTION_CLASSIFIER_INPUTS.csv` | projection classifier inputs |
| 3123-runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3123_deltaJ_projection_classifier.py` | executable projection classifier |

## Action-Variation Proof Attempt

Define the public current by variation before readout:

```text
J_Q^mu(x) := (1/sqrt(-g_pub)) delta S_matter / delta A_Q_mu(x).
```

Let `v` be a compact local vertical generator:

```text
Dq[v] = 0.
```

If:

```text
S_matter = Sbar_matter[q(Phi), Psi, A_Q(q(Phi)), n_A, theta_A],
```

with fixed representation data:

```text
Lie_v n_A = 0,
Lie_v theta_A = 0,
```

then:

```text
Lie_v S_matter = 0,
Lie_v A_Q = 0,
Lie_v sqrt(-g_pub) = 0.
```

Because the current is the functional derivative of the same q-basic action:

```text
Lie_v J_Q^mu
= Lie_v [(1/sqrt(-g_pub)) delta S_matter / delta A_Q_mu]
= (1/sqrt(-g_pub)) delta (Lie_v S_matter) / delta A_Q_mu
  + commutator terms from Lie_v A_Q and Lie_v g_pub
= 0.
```

The important point:

```text
This proves normalization ownership, not merely conservation.
```

Ward identity gives:

```text
nabla_mu J_Q^mu = 0.
```

Action-variation descent gives:

```text
Lie_v J_Q^mu = 0.
```

That is the missing statement needed for local Maxwell/GR source coupling.

## Why It Still Does Not Promote

The proof fails if the parent matter action contains any of:

```text
S_int = sum_A n_A c_A(y) integral A_Q_mu J_A^mu,
S_matter = sum_A w_A(y) S_A,
Q_*(y) n_A as hidden charge-base normalization,
J_Q selected after material/readout projection,
S_eff regenerating delta J_rad(y).
```

These are not logical impossibilities. The current corpus has not forbidden them by parent action grammar or quotient typing. Therefore:

```text
action-variation theorem = exact conditional;
MTS current-owner claim = not yet promoted.
```

## Projection Classification

If `delta_J` survives, its physical meaning depends on where it is inserted.

| insertion class | projects to material Coulomb? | projects to source `GM`? | projects to WEP? | projects to R10? | reason |
|---|---:|---:|---:|---:|---|
| q-basic/forbidden | no | no | no | no | action variation gives `Lie_v J_Q=0` |
| before Maxwell solve / before Hilbert variation | yes | yes | yes if differential | yes | `F[J]` and `T_EM[J]` change |
| universal calibrated current unit | raw yes, observable no | raw yes, observable no | no | no unless source/test convention differs | common unit is absorbed by calibration |
| post-variation readout selector | maybe | no | maybe | maybe | measured charge/readout changes but Hilbert stress does not |
| radiative/source threshold | yes if effective action before variation | yes if stress changes | maybe | maybe | depends on whether it re-enters the action or only the readout |

This prevents two opposite mistakes:

```text
1. claiming delta_J is harmless because it can be calibrated;
2. claiming every delta_J immediately violates local GR/WEP.
```

The location of the insertion decides the observable.

## Runner Result

3123 adds:

| artifact | path |
|---|---|
| input table | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3123_DELTAJ_PROJECTION_CLASSIFIER_INPUTS.csv` |
| output table | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3123_DELTAJ_PROJECTION_CLASSIFIER_OUTPUT.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3123_VALIDATION.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3123_ACTION_VARIATION_GATE.csv` |

The runner classifies each case as:

```text
ZERO_BY_ACTION_VARIATION
FINITE_BEFORE_VARIATION_PROJECTS_BOTH
FINITE_CALIBRATION_ONLY
FINITE_READOUT_ONLY_NO_GM
FINITE_EFFECTIVE_ACTION_AMBIGUOUS
```

and keeps every row nonclaim until the parent action signs the required clauses.

## Claim Status

No local-GR, Maxwell, WEP, R10, source-`GM`, PPN, orbital, derived-`G`, or unification claim follows from 3123.

The internal advance is:

```text
same-current owner now has a functional-derivative proof route;
Ward conservation is no longer being asked to do the wrong job;
delta_J projection is classified by insertion stage;
the finite C_J branch is not allowed to blur material response, source GM, and calibration.
```

## Next Target

Write:

```text
3124-Y5-R2FR-no-cA-slot-parent-grammar-or-deltaJ-finite-branch-selection-under-AX1090.md
```

Direct target:

1. try to prove the parent matter grammar has no `c_A(y) A_Q J_A` slot;
2. if that fails, select the finite branch by insertion stage: before-variation, readout-only, calibration-only, or effective-action;
3. only then continue coefficient/source-bound filling.
