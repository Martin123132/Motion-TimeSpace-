# 3117 - EM Coupling Owner No-Extra-F2 or Alpha Residual Bound Priority under AX1090

Private checkpoint. This is a derivation-first refinement of the EM coupling problem left by 3116.

## Verdict

The EM coupling debt splits into two different problems:

```text
Problem A: derive the numerical value of alpha_EM.
Problem B: prove that alpha_EM/current/Hodge do not vary along hidden local MTS directions.
```

Problem A is still open and may require parent gauge norm, level/index, charge lattice normalization, or a deeper microstructure theorem.

Problem B is the local-GR/Maxwell requirement. It is weaker and more reachable:

```text
local GR + Maxwell does not require deriving alpha_EM's number;
it requires alpha_EM, current normalization, and Hodge/readout to be universal public data
with no hidden local derivative.
```

Therefore a constant visible Maxwell counterterm:

```text
lambda_0 F_Q^2
```

blocks a predictive derivation of the number `alpha_EM`, but it does **not** by itself create a local fifth-force/clock/WEP/R10 residual if it is universal and hidden-independent.

The dangerous terms are:

```text
f_X(X) F_Q^2,
delta lambda_rad(X) F_Q^2,
q_A(X) A_Q J_A,
delta_*[X],
alpha_readout(q,X).
```

Those create `b_alpha`, `delta_J`, `delta_star`, clock/spectral and constitutive residuals.

This is the main improvement over the older 1057-1100 alpha chain: stop treating "alpha value not derived" and "hidden alpha variation not controlled" as the same failure.

## Source Register

| source_id | path | role |
|---|---|---|
| 1057 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md` | unique Maxwell subblock and counterterm ledger |
| 1058 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md` | visible operator-domain exhaustion and alpha counterterm prior |
| 1098 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1098-Y5-R10-ordinary-constant-owner-action-signature-or-source-backed-coefficient-prior.md` | ordinary constant owner signature |
| 1099 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md` | alpha owner/no-extra-`F^2` theorem attempt |
| 1100 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md` | `T_Q`, charge lattice and gauge norm signature |
| 3114 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3114-Y5-R2FR-strict-local-quotient-parent-signature-checklist-under-AX1090.md` | strict local q-basic action route |
| 3115 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3115-Y5-R2FR-local-vertical-Noether-generator-certificate-under-AX1090.md` | vertical Noether certificate |
| 3116 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3116-Y5-R2FR-public-Hodge-Maxwell-stress-lock-or-constitutive-residual-vector-under-AX1090.md` | public Hodge/Maxwell stress lock |

## Alpha Decomposition

Use a local public Maxwell sector:

```text
S_EM = -1/4 integral sqrt(-g_pub) Z_A F_Q^2 + S_int[A_Q,J_Q].
```

Write the observed inverse coupling ledger as:

```text
Z_A
= Z_parent(q,T_Q,N_Q,C_P)
 + lambda_0
 + f_X(y)
 + delta lambda_rad(q,y,mu)
 + delta Z_readout(q,y).
```

Here:

```text
Z_parent       := coefficient inherited from parent public gauge norm;
lambda_0       := universal hidden-independent visible counterterm;
f_X(y)         := hidden/private coefficient function;
delta lambda_rad := effective/radiative hidden-dependent threshold;
delta Z_readout  := post-variation readout/spectral map correction.
```

The local hidden alpha residual is:

```text
b_alpha := Lie_v ln alpha_obs
        = - Lie_v ln Z_A
          + Lie_v ln R_alpha_readout
          + current/charge-normalization terms.
```

Therefore:

```text
Lie_v lambda_0 = 0
```

for a true universal constant. It changes the calibrated value of `alpha_EM`, but it does not produce a hidden local derivative.

By contrast:

```text
Lie_v f_X(y) != 0
or
Lie_v delta lambda_rad(q,y,mu) != 0
or
Lie_v delta Z_readout(q,y) != 0
```

creates a real local residual.

## Theorem 1 - Local Alpha-Silence from Strict Quotient Descent

**Claim.** In the compact local strict-quotient branch, if:

```text
1. private directions are first-class vertical gauge directions;
2. the local parent action is q-basic up to pure gauge/topological/fixed-boundary terms;
3. A_Q, *_pub, J_Q and ordinary spectral readout factor through q_parent or fixed representation data;
4. hidden-visible coefficient maps into F_Q^2 are absent or constant;
5. radiative/readout reduction preserves q-basicity;
```

then:

```text
b_alpha = 0,
delta_J = 0,
delta_star = 0,
Delta_T_EM(hidden) = 0
```

through compact local order.

**Proof.**

For every compact local vertical generator `v`:

```text
Dq_parent[v] = 0.
```

If the local action and readout are q-basic:

```text
S_EM = Sbar_EM[q_parent(Phi), A_Q, theta_rep],
alpha_obs = alphabar[q_parent(Phi), theta_rep],
J_Q = Jbar_Q[q_parent(Phi), Psi, theta_rep],
*_pub = *bar[q_parent(Phi)].
```

Then the chain rule gives:

```text
Lie_v alpha_obs = D alphabar[Dq_parent[v]] = 0,
Lie_v J_Q = D Jbar_Q[Dq_parent[v]] = 0,
Lie_v *_pub = D *bar[Dq_parent[v]] = 0.
```

Any term `f_X(y)F_Q^2` violates q-basicity unless `Lie_v f_X=0` for every vertical generator. Any source current factor `q_A(y) A_Q J_A` violates matter/readout descent unless `Lie_v q_A=0`. Therefore hidden alpha/current/Hodge residuals are zero inside the strict local branch.

This theorem does not derive the numerical value of `alpha_EM`.

It derives local hidden **silence** if the strict quotient parent signature is signed.

## Theorem 2 - Constant Maxwell Counterterm Is a Calibration Debt, Not a Local Residual

Let:

```text
Z_A = Z_parent + lambda_0,
Lie_v lambda_0 = 0.
```

Then:

```text
b_alpha = -Lie_v ln(Z_parent + lambda_0) = 0
```

if `Z_parent` is also q-basic.

But:

```text
alpha_EM = 1 / (4 pi hbar c Z_A)
```

is not predicted unless `Z_parent` and `lambda_0` are fixed by the parent theory.

So:

```text
constant lambda_0:
  blocks alpha-value derivation;
  does not block local GR+Maxwell residual silence.

hidden f_X(y):
  blocks local residual silence;
  must be forbidden or bounded.
```

This is the operational separation we need going forward.

## Theorem 3 - Same-Current Owner and Source/Test Charge Residual

The interaction term can be written:

```text
S_int = integral A_Q_mu J_Q^mu sqrt(-g_pub) d^4x.
```

If charge labels and current normalization are fixed representation data:

```text
J_Q^mu = sum_A n_A J_A^mu,
Lie_v n_A = 0,
Lie_v J_A^mu = 0 after q-basic matter descent,
```

then:

```text
delta_J := Lie_v ln J_Q = 0.
```

If instead:

```text
J_Q^mu = sum_A n_A q_A(y) J_A^mu,
```

then:

```text
delta_J_A = Lie_v ln q_A(y)
```

is a composition/source/test residual. It enters WEP, R10 material projections and EM source calibration even if `b_alpha=0`.

Therefore `delta_J` is the second priority after `b_alpha` if the EM owner theorem fails.

## Bound Priority If Derivation Fails

The residual priority is:

| priority | residual | why first/next |
|---|---|---|
| 1 | `b_alpha` | strongest existing cross-arena scaffolding: clock product, WEP alpha target, R10 alpha product law |
| 2 | `delta_J` | source/test current normalization can mimic or amplify alpha effects in WEP/R10/source coupling |
| 3 | `delta_star` | hidden Hodge/coframe dependence affects EM stress and light/clock readout, but the exact weak-field projection is less filled |
| 4 | `C_constitutive` | broadest EM propagation/background-flow residual; powerful but needs a dedicated propagation/stress kernel |
| 5 | `Delta_T_EM` / `Delta_S_Poynting` | downstream stress/flux residuals after the upstream EM coefficient/Hodge/current split |

Existing rows already say:

```text
clock: bounds b_alpha * tau_clock_time only;
WEP: needs beta_source_alpha * b_alpha * tau_WEP;
R10: needs K_X(lambda) * beta_s * beta_t + tail and valid bound curve.
```

So no clock/WEP/R10 alpha pass is claimable yet. But the right first finite branch is `b_alpha`, not the broad constitutive tensor.

## Updated EM Decision Gate

| gate | status after 3117 | consequence |
|---|---|---|
| local Maxwell form | conditionally available | public `F=dA_Q` route can be used |
| public Hodge stress | conditional on `*_pub=*bar(q)` | Poynting becomes Hilbert stress flux |
| hidden alpha silence | conditionally derivable from strict q-basic action/readout | does not need numerical alpha derivation |
| alpha numerical value | not derived | acceptable for local GR+Maxwell, open for unification |
| constant `lambda_0 F^2` | calibration debt | blocks alpha prediction, not hidden local residual |
| hidden `f_X(y)F^2` | residual threat | must be forbidden by q-basic/no-hidden-visible theorem or bounded |
| same current owner | unsigned | `delta_J` retained unless charge/current representation data are fixed |
| radiative/readout closure | unsigned | `delta_clock_alpha` retained unless effective readout remains q-basic |

## What This Moves

3117 makes the EM route less grim:

```text
MTS can reduce locally to GR+Maxwell with a calibrated alpha_EM,
the same way GR uses calibrated G,
provided hidden local derivatives of alpha/current/Hodge vanish.
```

Deriving the numerical value of `alpha_EM` remains a deeper unification target, not an immediate local-GR blocker.

The hard local blocker is now narrower:

```text
prove no hidden-dependent F_Q^2/current/Hodge/readout terms in the compact local strict quotient branch,
or bound b_alpha/delta_J/delta_star.
```

## Claim Status

No public alpha, WEP, R10, clock, Maxwell, local-GR, derived-`G`, derived-`alpha`, or unification claim follows from 3117.

The internal advance is:

```text
alpha-value derivation debt separated from hidden-alpha-residual debt;
constant F^2 counterterm demoted to calibration debt;
hidden F^2/current/Hodge terms kept as testable residuals;
b_alpha selected as first finite-bound priority if derivation fails.
```

## Next Target

Write:

```text
3118-Y5-R2FR-no-hidden-visible-coefficient-hom-for-local-EM-or-balpha-product-bound-runner-under-AX1090.md
```

Direct target:

1. try to prove the no-hidden-visible coefficient hom theorem specifically for compact local EM:
   `Hom(C_hid, Coeff(F_Q^2)) = Const` or absent;
2. include radiative/readout closure as a separate clause, not an afterthought;
3. if the theorem fails, produce a `b_alpha` product-bound runner that uses existing clock/WEP/R10 scaffolding but keeps all rows nonclaim until MTS-side `tau`, `beta_source`, `K_X`, and valid bound curves exist.
