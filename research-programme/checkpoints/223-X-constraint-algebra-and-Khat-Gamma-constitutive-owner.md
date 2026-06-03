# 223 - X Constraint Algebra and Khat/Gamma Constitutive Owner

Private theory checkpoint. This is not a public local-GR, PPN, galaxy, BAO,
CMB, or field-theory completion claim.

## 1. Trigger

Checkpoint 222 found the only viable `X^nu` route:

```text
first-order constraint field,
no quadratic X kinetic term,
explicit boundary momentum.
```

But two things were still loose:

```text
does the constraint algebra actually remove local X degrees?
is P^{mu nu}=Khat^{mu nu}-Gamma_eff g^{mu nu} parent-owned?
```

This checkpoint attacks those two problems directly.

## 2. Machine Artifact

Script:

```text
scripts/X_constraint_algebra_and_Khat_Gamma_constitutive_owner.py
```

Run:

```text
runs/20260601-000040-X-constraint-algebra-and-Khat-Gamma-constitutive-owner
```

Command:

```text
python scripts/X_constraint_algebra_and_Khat_Gamma_constitutive_owner.py --timestamp 20260601-000040
```

Status:

```text
X_multiplier_zero_dof_route_conditional_P_constitutive_owner_missing_no_local_GR_promotion
```

Claim ceiling:

```text
X_constraint_algebra_partial_constitutive_owner_missing_no_PPN_promotion
```

## 3. Main Result

The independent `P^{mu nu}` route is rejected.

If:

```text
S_X = int sqrt(-g) [
  P^{mu nu} nabla_mu X_nu
  + J_eff^nu X_nu
]
```

and `P^{mu nu}` is independent, then the action avoids a regular `X` kinetic
term but leaves a new problem:

```text
P^{mu nu}
```

is a free tensor unless some parent sector owns it.

That is not good enough. It simply moves the hand insertion from `q_loc` into
`P`.

The best live route is instead:

```text
P^{mu nu} = P^{mu nu}[Y],
```

where `Y` are parent fields.

Then, after integrating by parts:

```text
S_X =
- int sqrt(-g) X_nu [
  nabla_mu P[Y]^{mu nu}
  - J_eff[Y]^nu
]
+ boundary.
```

Now `X_nu` is a pure multiplier, not a local wave.

The constraint is:

```text
C^nu_X =
-nabla_mu P[Y]^{mu nu}
+ J_eff[Y]^nu
approx 0.
```

So the zero-hair route exists conditionally:

```text
X removes no local degrees if it is only a multiplier enforcing C_X^nu.
```

## 4. Constraint Algebra

For the composite route, the local `X` pair is:

```text
X_nu, pi_X^nu.
```

Primary constraint:

```text
pi_X^nu approx 0.
```

Secondary constraint:

```text
C_X^nu approx 0.
```

If the algebra closes:

```text
{C_X^nu(x), C_X^rho(y)}
```

vanishes weakly or closes on existing parent constraints, then `X` contributes
zero local propagating degrees.

That is the pass route.

But the algebra is not yet computed because the parent `Y` symplectic structure
is not specified. This is now the main local-GR blocker.

Current verdict:

```text
zero X degrees: conditional;
constraint closure: not derived.
```

## 5. Constitutive Owner for P

The cleanest ownership contract is a defect potential:

```text
P^{mu nu} =
partial V_def(Y,Z) / partial Z_{mu nu}.
```

Then split:

```text
Gamma_eff = -1/4 trace(P),
Khat^{mu nu} = P^{mu nu} + Gamma_eff g^{mu nu}.
```

This works if `Khat` is the trace-free part and `Gamma_eff` is the trace
response.

That is a good mathematical contract.

But it is not yet a derivation, because the theory has not derived:

```text
V_def,
Z_{mu nu},
the full parent metric M_AB,
or the cross-term policy.
```

The `G_K` norm route helps but does not finish the job. Checkpoints 210 and 211
gave partial geometric ownership of the flow block, but the Weyl, `Q`, `J_rel`,
and cross-term parts remain closure.

## 6. Rejected Routes

Rejected:

```text
free P tensor,
invertible H(P,Y),
direct matter-stress P.
```

Why:

| route | reason |
|---|---|
| free `P` | source identity becomes a named tensor equation |
| invertible `H(P,Y)` | integrating out `P` generically reintroduces `dot(X)^2` or gradient stiffness |
| matter-stress `P` | risks WEP/clock/composition coupling and collapses the memory-sector distinction |

The route must be:

```text
composite P[Y] + multiplier X + owned boundary primitive.
```

No other route is currently clean enough.

## 7. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| independent free `P` rejected | pass |
| composite `P[Y]` multiplier route gives zero `X` dof | conditional pass |
| constraint algebra closed | fail |
| `P` constitutive owner identified | conditional pass |
| `P` constitutive owner derived | fail |
| trace/traceless split fixes `Gamma` and `Khat` | conditional pass |
| PPN margin survives `X` route | conditional pass |
| local GR or PPN promoted | fail |

## 8. Decision

Decision:

```text
X_multiplier_zero_dof_route_conditional_P_constitutive_owner_missing_no_local_GR_promotion
```

Meaning:

```text
X can be made locally harmless only as a pure multiplier imposing a source
constraint on a composite parent tensor P[Y].
```

This is real progress because it rejects the two bad paths:

```text
free tensor P,
regular/invertible X dynamics.
```

But the actual derivation still needs:

```text
closed constraint algebra,
parent defect potential V_def,
parent response deformation Z_{mu nu},
boundary primitive exactness,
explicit stress/Bianchi variation.
```

Current status:

```text
local GR route is sharper but still not derived;
X does not kill the theory yet;
P ownership is now the throat of the bottleneck.
```

## 9. Next Target

Create:

```text
224-defect-potential-Vdef-or-X-route-demotion.md
```

Purpose:

```text
try to construct V_def(Y,Z) and Z_{mu nu} from the existing coherence-defect
blocks, or demote the X-source-identity route to explicit closure support.
```

Pass condition:

```text
P^{mu nu}=partial V_def/partial Z_{mu nu}
```

is derived from parent variables already in the MTS corpus, with the trace and
traceless pieces matching `Gamma_eff` and `Khat`.

Fail condition:

```text
V_def is only a newly named potential chosen to make the source identity work.
```
