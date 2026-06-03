# Load-Tensor Origin Attempt

## 1. Purpose

This file follows:

```text
51-FLRW-memory-current-contract.md
```

The previous checkpoint found the cleanest activation contract:

```text
I_M = det(Q)
Q^i_j|FLRW = X_FLRW delta^i_j
```

This checkpoint asks:

```text
Can Q^i_j be defined before FLRW symmetry is imposed?
```

Short answer:

```text
yes, partially. Q^i_j can be defined kinematically as normalized accumulated
spatial expansion/load, and this gives X_FLRW = N/u_3 in FLRW. But it is not
yet parent-action-derived and it is not locally safe for all dynamical cases.
```

That is a useful move. Not champagne. Maybe a strong tea.

## 2. Machine Run

Implemented:

```text
scripts/load_tensor_origin_attempt.py
```

Successful run:

```text
runs/20260531-034248-load-tensor-origin-attempt/status.json
```

Readout:

```text
load_tensor_has_partial_kinematic_origin_not_parent_action
```

Generated:

```text
runs/20260531-034248-load-tensor-origin-attempt/results/source_checkpoint_register.csv
runs/20260531-034248-load-tensor-origin-attempt/results/load_tensor_origin_candidates.csv
runs/20260531-034248-load-tensor-origin-attempt/results/FLRW_reduction_chain.csv
runs/20260531-034248-load-tensor-origin-attempt/results/local_silence_tests.csv
runs/20260531-034248-load-tensor-origin-attempt/results/parent_gap_register.csv
runs/20260531-034248-load-tensor-origin-attempt/results/gate_results.csv
runs/20260531-034248-load-tensor-origin-attempt/results/decision.csv
```

## 3. Best Candidate

Define the spatial expansion/deformation tensor of the parent time-flow
congruence:

```text
Theta^i_j = h^{i alpha} h_{j beta} nabla_alpha u^beta
```

Then define:

```text
Q^i_j = (1/u_3) integral_t^t0 Theta^i_j d tau.
```

Interpretation:

```text
Q^i_j is a dimensionless accumulated motion/space load tensor.
```

This is important because it defines Q before FLRW symmetry is imposed. The
tensor is not invented by first writing `X^3`.

## 4. FLRW Reduction

In FLRW:

```text
Theta^i_j = H delta^i_j.
```

Therefore:

```text
Q^i_j = (1/u_3) integral_t^t0 H dt delta^i_j.
```

With:

```text
integral_t^t0 H dt = ln(a0/a) = N
```

we get:

```text
Q^i_j = (N/u_3) delta^i_j.
```

So:

```text
X_FLRW = N/u_3.
```

Then the checkpoint-51 determinant route gives:

```text
I_M = det(Q) = (N/u_3)^3
J_M = dI_M/dN = 3 N^2/u_3^3
F = 1 - exp[-(N/u_3)^3].
```

That is the strongest result in this checkpoint:

```text
X_FLRW = N/u_3 is now kinematically derived up to the still-missing scale u_3.
```

## 5. Numerical Lock

The retained closure still uses:

```text
u_3 = 0.2429466120286312
N50 = 0.21500703361675252
dX_FLRW/dN = 4.116130666115856
J_M quadratic coefficient = 209.2130223887545
```

The good news:

```text
the shape route is less arbitrary.
```

The bad news:

```text
u_3 remains borrowed from the C2 closure.
```

So this does not yet derive the transition scale.

## 6. Local Silence

The local result is mixed.

Passes:

```text
Minkowski/inertial local systems: Theta^i_j = 0, so Q = 0.
Stationary static exterior: no coherent volume expansion, so Q is plausibly 0.
```

Promising but not proven:

```text
virialized bound systems may average to zero coherent expansion.
```

Fails or remains open:

```text
full unprojected Q can respond to anisotropic shear/collapse;
gravitational waves or transient local strain are not controlled;
FLRW perturbations still need their own response law.
```

This means the route is not locally safe unless a parent coherent-projection or
screening rule is derived.

## 7. Gate Verdict

Gate result:

```text
Q_defined_before_FLRW_symmetry          pass_partial
FLRW_reduces_to_X_equals_N_over_u3      pass_partial
cubic_exposure_from_determinant         pass_conditional
stationary_local_silence                pass_conditional
anisotropic_dynamic_local_safety        fail_open
u3_parent_predicted                     fail
parent_action_derived                   fail
support_claim_allowed                   fail
```

This is a real narrowing of the problem:

```text
the shape origin now looks plausible;
the scale and local-dynamical safety are the dangerous bits.
```

## 8. Decision

Decision:

```text
load_tensor_origin_status = partial_kinematic_origin_not_parent_action
```

Meaning:

```text
Q^i_j can be defined as accumulated expansion/load before FLRW symmetry;
FLRW then gives Q^i_j = (N/u_3) delta^i_j;
det(Q) gives the p=3 exposure;
stationary local systems are plausibly silent;
dynamic anisotropic local systems are not yet safe;
u_3 and b_mem remain underived.
```

This is not a fail. It is also not a win condition. It is the branch becoming
more surgical.

## 9. Next Target

Create:

```text
53-coherent-projection-local-silence-gate.md
```

Purpose:

```text
derive or reject the coherent projection/screening rule needed so Q^i_j keeps
FLRW expansion memory while suppressing local virialized, anisotropic, and
stationary-system hair.
```

Pass condition:

```text
the parent theory supplies a non-fitted projector or conservation argument that
keeps only coherent expansion load in the memory determinant.
```

Fail condition:

```text
the projector has to be inserted by hand purely to dodge local tests.
```
