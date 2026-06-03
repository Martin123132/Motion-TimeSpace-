# Observer-Map Symplectic Contract

## 1. Purpose

This file follows:

```text
09-hamiltonian-radial-cell-derivation.md
```

The question is:

```text
What exact contract must a future parent action satisfy before the local
motion-load branch is allowed to claim derived GR reduction?
```

Short answer:

```text
the contract can now be stated sharply, but it is not yet satisfied.
```

## 2. Machine Run

Implemented:

```text
scripts/observer_map_symplectic_contract.py
```

Successful run:

```text
runs/20260530-230334-observer-map-symplectic-contract/status.json
```

Readout:

```text
observer_map_contract_written_not_satisfied
```

Next target:

```text
11-cell-current-origin-attempt.md
```

## 3. Observer Map

The local observer coframe must be defined before any PPN claim:

```text
theta_0 = T c dt
theta_1 = sqrt(S) dr
```

The dual local momenta are:

```text
E_hat = E/T
p_hat = p_r/sqrt(S)
```

The local radial configuration-cell Jacobian is:

```text
J_q = T sqrt(S)
```

The dual momentum-cell Jacobian is:

```text
J_p = 1/(T sqrt(S)).
```

The reciprocal strain is:

```text
R_AB = ln(T^2 S) = 2 ln(J_q).
```

Therefore:

```text
R_AB = 0
<=> T^2 S = 1
<=> T sqrt(S) = 1
<=> p = 1 for S_p=(1-L)^(-p).
```

## 4. Core Contract

A future parent action may pass only if it produces the local vacuum equation:

```text
R_AB = ln(T^2 S) = 0
```

without using:

```text
Schwarzschild AB=1;
Einstein vacuum equations;
fitted light-bending p=1;
generic Liouville preservation;
hidden reciprocal source neutrality.
```

The acceptable parent routes are narrow:

```text
1. a genuine constraint whose multiplier has a parent origin;
2. a conserved cell current with a no-charge theorem;
3. a gauge redundancy of observer splitting that is not merely a coordinate trick.
```

The unacceptable routes are:

```text
1. kinetic reciprocal strain with exterior Q_R/r hair;
2. generic phase-volume preservation;
3. importing GR field equations;
4. fitting p to local tests.
```

## 5. Why Symplectic Preservation Is Not Enough

The full radial phase cell is:

```text
J_q J_p = (T sqrt(S)) * (1/(T sqrt(S))) = 1.
```

This is true for every `p`.

So the parent theory must do more than preserve canonical phase volume.

It must preserve or constrain the radial observer configuration cell separately:

```text
J_q = 1.
```

That is the exact missing theorem.

## 6. Open Gates

The contract run leaves these gates open:

```text
source_neutrality;
lambda_origin;
beta_completion;
no_GR_import.
```

The promotion gate fails:

```text
promotion_to_main_workbench = fail.
```

So the local branch is not dead, but it remains conditional.

## 7. PPN Completion Requirements

The minimum local-GR completion must prove:

```text
Newtonian limit:
T^2 = 1 - 2U/c^2 + correct weak-field acceleration.

PPN gamma:
gamma - 1 = 0 after R_AB=0.

PPN beta:
beta - 1 = 0 in a valid PPN coordinate construction.

Equivalence principle:
all matter sectors couple to the same observer coframe.

Conservation:
field equations imply a Bianchi-like consistency identity.
```

This matters because `gamma=1` alone is not enough to claim GR reduction.

## 8. Verdict

The local motion-load route now has a precise no-smuggling contract:

```text
derive R_AB=0 from the parent theory, forbid reciprocal hair, prove beta and
conservation, and do not import GR.
```

Current status:

```text
contract written;
contract not satisfied;
main-workbench promotion not allowed.
```

## 9. Next Target

Create:

```text
11-cell-current-origin-attempt.md
```

Purpose:

```text
attempt to derive lambda_R or R_AB=0 from a conserved radial observer-cell
current, and either close the lambda-origin gate or demote the route to an
explicit closure.
```
