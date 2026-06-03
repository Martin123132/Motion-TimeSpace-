# Motion-Load Local GR Reduction

## 1. Purpose

This file follows:

```text
01-motion-load-route-contract.md
```

The question is:

```text
Can the motion-load scaffold recover the local weak-field GR lane without
promoting the new route too early?
```

Short answer:

```text
yes conditionally, but not yet fundamentally.
```

The route gives a clean conditional reduction if reciprocal clock/spatial
routing is accepted:

```text
T^2 S = 1.
```

But that reciprocity is not yet derived from a parent action or conservation
principle.

## 2. Machine Run

Implemented:

```text
scripts/motion_load_local_GR_reduction.py
```

Successful run:

```text
runs/20260530-223507-motion-load-local-GR-reduction/status.json
```

Readout:

```text
motion_load_local_GR_reduction_conditional_not_promoted
```

Next target:

```text
03-reciprocal-routing-parent-origin.md
```

## 3. Scaffold Tested

Clock/load side:

```text
c^2 = v_space^2 + v_clock^2 + v_load^2
d tau/dt = sqrt(1 - v^2/c^2 - v_load^2/c^2)
v_load^2 = 2GM/r
```

Weak-field load:

```text
L = 2GM/(rc^2) = 2U/c^2
T^2 = 1 - L
```

Routing side:

```text
S_p = (1-L)^(-p)
```

Weak-field spatial coefficient:

```text
S_p = 1 + 2p U/c^2 + ...
```

So the PPN spatial-curvature proxy is:

```text
gamma = p.
```

## 4. Conditional Derivation Of p = 1

If the clock residue and spatial routing are reciprocal:

```text
T^2 S = 1
```

then:

```text
S = 1/T^2 = 1/(1-L)
```

and therefore:

```text
p = 1.
```

This is the important simplification.

It means local GR recovery can be read as:

```text
mass-load reduces clock capacity;
the lost clock capacity is reciprocally carried as spatial routing;
the reciprocal lock gives gamma = 1.
```

But the reciprocal lock itself still needs a parent origin.

## 5. Numerical Checks

The same scaffold gives:

```text
GPS net = 38.60879935757566 microseconds/day
solar light bending at p=1 = 1.7512432813682448 arcsec
Mercury perihelion at p=1 = 42.98201260912118 arcsec/century
Shapiro delay at p=1 = 119.4750358485562 microseconds
```

These are the correct weak-field lanes.

The gate result is:

```text
GPS_clock_scale = pass
light_bending_full_lane = pass
Mercury_full_lane = pass
Shapiro_full_lane = pass
derive_p_equals_1 = conditional_pass
parent_origin_of_reciprocity = fail
promotion_to_main_workbench = fail
```

## 6. Beta / Second-Order Warning

The first-order map is clean:

```text
gamma = p
p = 1 if T^2 S = 1
```

The second-order map is not yet fundamental.

If `p=1` is treated as the exact Schwarzschild-form reciprocal completion, then
the usual local GR result has:

```text
beta = 1.
```

But this is conditional on accepting the exact reciprocal metric completion.

So the honest status is:

```text
beta completion = conditional, not parent-derived.
```

## 7. Interpretation

This route is worth pursuing.

It may make the old motion-field formulation emergent:

```text
Gamma_eff, K_hat, q_loc^nu, b_mem, Omega_Gamma, and L_cg
```

can potentially become bookkeeping variables for:

```text
load;
routing;
residual memory;
coarse-grained nonlocal response.
```

But no main-workbench promotion is allowed yet.

The current status is:

```text
motion-load local GR reduction = conditional success;
parent origin of reciprocal routing = missing;
main route remains protected.
```

## 8. Next Target

Create:

```text
03-reciprocal-routing-parent-origin.md
```

Purpose:

```text
derive or reject T^2 S = 1 from a parent principle. Candidate sources include
null-cone preservation, action reciprocity, determinant balance, or conserved
motion-capacity flux.
```
