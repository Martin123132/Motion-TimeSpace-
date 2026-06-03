# Constrained Parent-Action Skeleton

## 1. Purpose

This file follows:

```text
18-parent-action-or-empirical-pillar-decision.md
```

The question is:

```text
Can we write the minimal parent-action skeleton that could, in principle, turn
the local closure R_AB=0 into a theorem?
```

Short answer:

```text
we can write the skeleton and the exact contract, but it is still not a
derivation. The current action uses a closure multiplier.
```

## 2. Machine Run

Implemented:

```text
scripts/constrained_parent_action_skeleton.py
```

Successful run:

```text
runs/20260530-233405-constrained-parent-action-skeleton/status.json
```

Readout:

```text
constrained_parent_action_skeleton_contract_not_derivation
```

Next target:

```text
20-empirical-pillar-test-queue.md
```

## 3. Minimal Field Set

The skeleton needs:

```text
e^A_mu:
observer coframe / metric carrier.

C(x):
clock-capacity or load-response scalar.

P_parallel:
local radial/transport projector.

R_AB:
reciprocal strain, reducing locally to ln(T^2 S).

lambda_R:
multiplier or constrained-sector reaction field.

Psi_matter:
all matter fields coupled to the same coframe.

M_cosmo_or_memory:
placeholder for cosmology/memory sector.
```

Important:

```text
P_parallel is the covariance bottleneck.
```

Until the transport direction has a parent origin, the radial cell rule is not
a fully covariant theorem.

## 4. Skeleton Action

Schematic structure:

```text
S = S_geom
  + S_load
  + S_projector
  + S_R_constraint
  + S_matter
  + S_cosmo_memory
```

With:

```text
S_R_constraint = integral sqrt(-g) lambda_R R_AB.
```

Variation gives:

```text
delta lambda_R -> R_AB = 0.
```

But the label is:

```text
closure_term.
```

So this is not yet a parent derivation.

The forbidden term remains:

```text
S_R_kinetic = integral sqrt(-g) W (grad R_AB)^2 / 2.
```

because it reintroduces:

```text
Q_R/r reciprocal hair.
```

## 5. Required Variations

The skeleton must eventually supply:

```text
delta_C:
load equation giving C^2=1-2U/c^2 locally and cosmological memory globally.

delta_e:
coframe/metric equation with conservation identity.

delta_P_parallel:
physical transport/routing direction and t-r cell selection.

delta_Psi_matter:
matter equations on a universal coframe.
```

Current status:

```text
these are targets, not derivations.
```

## 6. Local Limit Gates

The local gates are:

```text
Newtonian clock limit:
C^2 = T^2 = 1 - 2U/c^2.

reciprocity:
R_AB=0 -> T^2 S=1.

PPN gamma:
gamma=1, conditional on R_AB=0.

PPN beta:
beta=1, still open.

universal matter coupling:
epsilon_matter=0, currently postulated.

no reciprocal charge:
Q_R=0, satisfied only if R_AB has no kinetic hair.
```

## 7. Cosmology Bridge

The skeleton must later explain:

```text
how C(x) becomes a homogeneous C(t) or memory variable;
how local R_AB=0 does not erase cosmological memory effects;
how C0/M-branch parameters map to action variables;
how conservation/Bianchi-like identities survive;
why action-derived parameters avoid edge-hitting priors.
```

This bridge is open.

## 8. Gate Verdict

Passes:

```text
source 18 complete;
fields defined;
closure labels explicit.
```

Conditional pass:

```text
Q_R hair removed only by forbidding R_AB kinetic terms.
```

Fails:

```text
R_AB=0 parent-derived;
beta completion derived;
universal matter coupling derived;
cosmology bridge derived;
main workbench mutation allowed.
```

Status:

```text
useful contract, not derivation.
```

## 9. Next Target

Create:

```text
20-empirical-pillar-test-queue.md
```

Purpose:

```text
use this skeleton to organize empirical pillars without overclaiming: local PPN,
cosmology, galaxies, EM/time, and orbital systems each get a readiness/risk
queue and a clear claim limit.
```
