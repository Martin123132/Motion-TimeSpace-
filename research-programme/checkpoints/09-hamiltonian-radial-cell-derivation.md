# Hamiltonian Radial-Cell Derivation

## 1. Purpose

This file follows:

```text
08-phase-volume-reciprocity-origin.md
```

The question is:

```text
Can the local Hamiltonian / mass-shell structure derive the radial t-r
phase-cell constraint T sqrt(S)=1, rather than merely tolerate it?
```

Short answer:

```text
not yet. The Hamiltonian route sharpens the missing theorem, but does not
derive it by itself.
```

## 2. Machine Run

Implemented:

```text
scripts/hamiltonian_radial_cell_derivation.py
```

Successful run:

```text
runs/20260530-225948-hamiltonian-radial-cell-derivation/status.json
```

Readout:

```text
hamiltonian_radial_cell_sharpened_not_parent_derived
```

Next target:

```text
10-observer-map-symplectic-contract.md
```

## 3. Scaffold Algebra

Use the static local radial scaffold:

```text
ds^2 = -T^2 c^2 dt^2 + S dr^2 + r^2 dOmega^2
T^2 = 1 - L
S_p = (1-L)^(-p)
```

The radial mass shell is:

```text
-(E/T)^2 + (p_r/sqrt(S))^2 + m^2 c^2 = 0.
```

So the local observer variables are:

```text
E_local = E/T
p_local = p_r/sqrt(S)
```

The radial clock-routing cell factor is:

```text
J_tr = T sqrt(S) = (1-L)^((1-p)/2).
```

For variable load `L`, the condition:

```text
J_tr = 1
```

requires:

```text
p = 1.
```

So the desired radial-cell rule still cleanly selects the GR lane.

## 4. Crucial Obstruction

Ordinary Hamiltonian / Liouville preservation is too weak.

The full radial phase cell gives:

```text
(d tau d ell)(dE_local dp_local)
= (T sqrt(S)) * (1/(T sqrt(S))) * (dt dr dE dp_r)
= dt dr dE dp_r.
```

That cancellation is automatic for every `p`.

Therefore:

```text
generic symplectic or Liouville phase-volume preservation does not derive p=1.
```

The null relation:

```text
dr/dt = c T/sqrt(S)
```

also works for any `p`, so null propagation alone does not derive reciprocity.

The Newtonian slow-particle limit fixes the clock/load side `T^2=1-L` first,
but does not fix the spatial routing exponent `p` at leading order.

## 5. Current Interpretation

The strongest local route is now very specific:

```text
the parent theory must preserve the radial t-r observer cell separately,
or impose the equivalent nonpropagating constraint ln(T^2 S)=0.
```

This is better than a vague volume argument because the wrong generic options
have been eliminated.

But it is not yet a parent derivation.

The missing theorem is now:

```text
why the radial observer cell is separately conserved, rather than only the full
canonical phase volume.
```

## 6. Gate Verdict

Passes:

```text
source 08 complete;
mass-shell scaffold written;
separate radial cell gives p=1 exactly;
generic phase-volume and Liouville routes rejected.
```

Fails:

```text
Hamiltonian law derives separate radial cell;
null propagation derives p=1;
observer-map parent origin;
promotion to main workbench.
```

Status:

```text
local GR branch remains promising but conditional;
no promotion is allowed yet.
```

## 7. Next Target

Create:

```text
10-observer-map-symplectic-contract.md
```

Purpose:

```text
write the exact contract a future parent action must satisfy to make the
radial observer cell a theorem instead of a closure axiom.
```

That contract should demand:

```text
1. a defined clock-load coframe;
2. a defined radial routing coframe;
3. a variational source for ln(T^2 S)=0 or T sqrt(S)=1;
4. no exterior reciprocal hair;
5. PPN gamma=1 and beta=1 in the local limit;
6. no hidden import of Schwarzschild or Einstein vacuum equations.
```
