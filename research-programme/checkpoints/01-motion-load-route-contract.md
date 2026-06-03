# Motion-Load Route Contract

## 1. Core Question

Can the theory be simplified by making:

```text
motion-load, clock residue, and spatial routing
```

more primitive than the earlier motion-field formulation?

If yes, the previous variables become effective accounting variables.

If no, this folder remains a failed exploratory branch and the main workbench is
unchanged.

## 2. Primitive Scaffold To Test

Starting equations:

```text
c^2 = v_space^2 + v_clock^2 + v_load^2
d tau/dt = v_clock/c
d tau/dt = sqrt(1 - v^2/c^2 - v_load^2/c^2)
v_load^2 = 2GM/r
```

Routing response:

```text
L(r) = 2GM/(rc^2)
T(r) = sqrt(1-L)
S_p(r) = 1/(1-L)^p
```

GR-like weak-field recovery appears at:

```text
p = 1
```

The contract is to derive `p=1`, not fit it.

## 3. Required Local-GR Gate

The route must produce a metric or PPN map with:

```text
gamma = 1
beta = 1
```

or an explicitly equivalent weak-field limit.

Required recoveries:

```text
GPS clock rates;
solar light bending;
Mercury perihelion;
Shapiro delay;
Newtonian limit.
```

Failure condition:

```text
if p=1 is simply inserted, this is only a reinterpretation of GR, not a
fundamental derivation.
```

## 4. Required Mapping To Previous Work

The route must say what happens to:

```text
Gamma_eff
K_hat
q_loc^nu
b_mem
Omega_Gamma
L_cg
```

Preferred mapping:

```text
these become emergent bookkeeping variables for load/routing/memory, not
independent primitives.
```

## 5. Required Local-Screening Gate

The route-clean closure from the new PDF may be tested as a candidate:

```text
A_B =
  [A_curv/(A_curv+5)]^1.5
  [I_mat/(I_mat+0.3)]^0.5
  [0.02/(E_theta+0.02)]
  P_mem

N = E sqrt(A_B)
M_tr,loc = A_B [
  M_base(1-A_B) exp(-E sqrt(A_B))
  + M0 A_B(1-A_B)^3
]
```

But it cannot be promoted unless the powers, thresholds, and route projector are
derived or sharply constrained.

## 6. Required Cosmology/Galaxy Gate

The route must not erase the earlier empirical discipline.

It must explain whether:

```text
b_mem = integrated residual motion-load;
galaxy Lambda_mem = residual extended routing/load;
C0 = old closure benchmark only;
strict cosmology branch = new motion-load branch.
```

No new cosmology support claim is allowed until the amplitude is predicted
before fitting.

## 7. Promotion Criteria

Promote this route back into the main workbench only if:

```text
1. p=1 or gamma=1 is derived from motion-load/routing structure;
2. beta=1 or equivalent second-order weak-field consistency is obtained;
3. local screening has a non-fitted route law;
4. b_mem or its replacement is predicted as a load/routing amplitude;
5. the route simplifies at least two old sectors without weakening tests.
```

Otherwise:

```text
mark this folder as failed/parked and resume the original workbench path.
```
