# Vacuum Reciprocity Action Contract

## 1. Purpose

This file follows:

```text
03-reciprocal-routing-parent-origin.md
```

The question is:

```text
What exact theorem must a motion-load parent action satisfy to derive
T^2 S = 1 without smuggling in GR?
```

Short answer:

```text
derive vacuum silence of the reciprocal strain mode.
```

The contract is locked, but not satisfied.

## 2. Machine Run

Implemented:

```text
scripts/vacuum_reciprocity_action_contract.py
```

Successful run:

```text
runs/20260530-224152-vacuum-reciprocity-action-contract/status.json
```

Readout:

```text
vacuum_reciprocity_action_contract_locked_not_satisfied
```

Next target:

```text
05-reciprocity-theorem-attempt.md
```

## 3. Variables

Use the static spherical exterior ansatz:

```text
ds^2 = -A(r)c^2dt^2 + B(r)dr^2 + r^2dOmega^2
```

with motion-load interpretation:

```text
A = T^2
B = S
```

Define the reciprocal strain:

```text
R_AB = ln(A B) = ln(T^2 S).
```

The desired local GR routing result is:

```text
R_AB = 0
AB = 1
T^2 S = 1
p = 1.
```

## 4. Required Parent Theorem

The parent action must vary `R_AB` and produce:

```text
d/dr [ W(r,L,fields) dR_AB/dr ] = J_R
```

with:

```text
W > 0
J_R = 0 in local vacuum
finite exterior reciprocal flux
R_AB(infinity) = 0.
```

Then:

```text
dR_AB/dr = 0
R_AB = 0
AB = 1.
```

That would derive reciprocal routing without fitting `p`.

## 5. Forbidden Imports

Not allowed:

```text
assume Schwarzschild metric;
assume Einstein vacuum equations;
fit p from light bending;
hide a local source J_R.
```

Allowed replacement:

```text
derive the reciprocal-strain equation from motion-load variables and show
vacuum source silence.
```

## 6. Why This Matters

If this theorem succeeds, the local GR route becomes much cleaner:

```text
mass-load fixes clock residue;
vacuum reciprocity fixes spatial routing;
p=1 follows;
gamma=1 follows.
```

If it fails:

```text
p=1 remains a postulate;
the motion-load route is a reinterpretation of GR, not a derivation;
the branch cannot be promoted back into the main workbench.
```

## 7. Gate Verdict

Passes:

```text
source 03 complete;
reciprocal mode identified;
no-smuggling rules locked.
```

Fails:

```text
action theorem proved;
promotion to main workbench.
```

Status:

```text
contract locked, theorem not satisfied.
```

## 8. Next Target

Create:

```text
05-reciprocity-theorem-attempt.md
```

Purpose:

```text
attempt the reciprocal-strain theorem. Either derive d(W R_AB')/dr=0 with
vacuum source silence, or demote reciprocal routing to a postulate and keep the
motion-load route unpromoted.
```
