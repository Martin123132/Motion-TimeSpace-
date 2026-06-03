# 207 - Domain-Projector Action and Bianchi Identity

Private theory checkpoint. This is not a public BAO, local-GR, or CMB claim.

## 1. Trigger

Checkpoint 206 narrowed `C`-silence to a coherent zero-mode/domain-projector
route:

```text
C(x) = C_D(t) + C_perp(x),
```

with local trace modes projected out or heavily suppressed.

The remaining danger was:

```text
Pi_D[J](x) = <J>_D
```

could just be a helpful average inserted after the fact.

This checkpoint asks:

```text
Can Pi_D be written as an action-level projector with Bianchi-safe stress
accounting?
```

## 2. Machine Artifact

Script:

```text
scripts/domain_projector_action_and_Bianchi_identity.py
```

Run:

```text
runs/20260601-000024-domain-projector-action-and-Bianchi-identity
```

Command:

```text
python scripts/domain_projector_action_and_Bianchi_identity.py --timestamp 20260601-000024
```

Status:

```text
domain_projector_action_formal_Bianchi_conditional_representative_missing
```

Claim ceiling:

```text
domain_projector_formal_action_only_no_BAO_local_GR_promotion
```

## 3. Main Result

The external average route is rejected:

```text
set C_D = <C>_D after solving the equations
```

has no action and no Bianchi discipline.

The best formal route is:

```text
C = C_D + C_perp,
```

with constraints:

```text
delta_lambdaPi S -> C - C_D - C_perp = 0,
```

and:

```text
delta_LambdaD S -> integral_D sqrt(h) W_D C_perp = 0.
```

This upgrades `Pi_D` from:

```text
a hand average
```

to:

```text
a formal variational constraint candidate.
```

That is progress, but it is not promotion.

## 4. Bianchi Accounting

If the total action varies:

```text
C_D,
C_perp,
domain labels X^A,
domain weight W_D,
lambda_Pi,
chi_D,
J_rel,
boundary terms,
metric/coframe,
matter fields,
```

then diffeomorphism invariance gives the formal Noether identity:

```text
nabla_mu T_total^{mu nu} = 0
```

on shell.

But this only works if the auxiliary/projector/domain stresses are retained:

```text
T_total =
T_matter + T_C + T_Pi + T_D + T_chi + T_rel + T_boundary.
```

The forbidden shortcut is:

```text
use Pi_D in the equations but drop T_Pi, T_D, or T_boundary.
```

That would hide an external force and fake conservation.

## 5. What Is Actually Gained

| item | result |
|---|---|
| external projector | rejected |
| formal `C_D + C_perp` projector action | conditional pass |
| zero-domain-average residual constraint | conditional pass |
| Noether/Bianchi identity | conditional pass if all fields/stresses are varied |
| physical representative selection | fail |
| non-tuned domain scale | fail |

So:

```text
Bianchi closure can be made formal;
physical domain selection is still missing.
```

## 6. Remaining Blocker

Formal conservation does not choose the real-world representative.

It does not prove:

```text
local bound domains -> trivial relative class,
FLRW coherent domains -> nontrivial memory class,
BAO survey domains -> late common-mode smooth class.
```

Nor does it derive:

```text
L_D = F[L_cg, chi_D, Q, J_rel]
```

before empirical scoring.

This means the branch still risks:

```text
domain scale as a rescue knob.
```

The next theorem burden is not just conservation. It is:

```text
representative selection.
```

## 7. Forbidden Shortcuts

| shortcut | reason rejected |
|---|---|
| insert `Pi_D` after solving | external projector, not variational |
| freeze domain boundary during metric variation | hides boundary exchange stress |
| claim Noether identity selects the physical representative | conservation is not selection |
| choose `L_D` from BAO success | data-tuned rescue knob |
| drop auxiliary stress because the field is nondynamical | auxiliary stress is conservation bookkeeping |

## 8. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| external projector rejected | pass |
| formal projector action written | conditional pass |
| Noether/Bianchi accounting closed | conditional pass |
| physical representative selected | fail |
| domain scale not tuned to data | fail |
| local GR or BAO support claim allowed | fail |

## 9. Decision

Decision:

```text
domain_projector_action_formal_Bianchi_conditional_representative_missing
```

Meaning:

```text
Pi_D can be upgraded from a hand average to a formal variational constraint
candidate, and Bianchi closure is conditionally available if all projector,
domain, auxiliary, and boundary stresses are retained.
```

But:

```text
the physical representative and non-tuned domain scale are still missing.
```

Current theory status:

```text
C-screening route improved;
Bianchi gremlin fenced but not slain;
no local-GR or BAO promotion yet.
```

Next target:

```text
208-domain-representative-selection-law.md
```
