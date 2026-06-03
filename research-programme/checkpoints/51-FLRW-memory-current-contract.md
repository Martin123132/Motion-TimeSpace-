# FLRW Memory-Current Contract

## 1. Purpose

This file follows:

```text
50-parent-activation-law-attempt.md
```

The previous checkpoint showed that:

```text
F(N) = 1 - exp[-(N/u_3)^3]
```

is regularity-selected and conditionally exact if the parent memory current is:

```text
J_M = 3 X_FLRW^2 dX_FLRW/dN.
```

This checkpoint asks the sharper question:

```text
What exact parent object would make that current non-circular?
```

Short answer:

```text
the cleanest contract is a parent 3D load tensor Q^i_j whose FLRW reduction is
Q^i_j = X_FLRW delta^i_j and whose memory exposure is I_M = det(Q).
```

That gives the cubic law without naming p=3 by hand. This is the first properly
interesting little beastie in this branch.

## 2. Machine Run

Implemented:

```text
scripts/FLRW_memory_current_contract.py
```

Successful run:

```text
runs/20260531-033502-FLRW-memory-current-contract/status.json
```

Readout:

```text
FLRW_memory_current_contract_identified_not_derived
```

Generated:

```text
runs/20260531-033502-FLRW-memory-current-contract/results/source_checkpoint_register.csv
runs/20260531-033502-FLRW-memory-current-contract/results/memory_current_variable_contract.csv
runs/20260531-033502-FLRW-memory-current-contract/results/memory_current_equation_contract.csv
runs/20260531-033502-FLRW-memory-current-contract/results/candidate_current_mechanisms.csv
runs/20260531-033502-FLRW-memory-current-contract/results/circularity_tests.csv
runs/20260531-033502-FLRW-memory-current-contract/results/gate_results.csv
runs/20260531-033502-FLRW-memory-current-contract/results/decision.csv
```

## 3. Best Contract Route

Introduce a dimensionless parent load tensor:

```text
Q^i_j
```

On an FLRW background, isotropy requires:

```text
Q^i_j = X_FLRW delta^i_j.
```

Now define the cumulative memory exposure by a parent 3D load-volume invariant:

```text
I_M = det(Q).
```

Then on FLRW:

```text
I_M = det(X_FLRW delta^i_j) = X_FLRW^3.
```

The current follows from the determinant identity:

```text
dI_M/dN = det(Q) Tr(Q^{-1} dQ/dN).
```

Therefore:

```text
J_M = dI_M/dN = 3 X_FLRW^2 dX_FLRW/dN.
```

And if the parent theory later derives:

```text
X_FLRW = N/u_3,
```

then:

```text
J_M = 3 N^2/u_3^3
F = 1 - exp[-(N/u_3)^3].
```

This is a real improvement: p=3 can come from the determinant of a 3D isotropic
load tensor, not just from saying “let it be cubic”.

## 4. Numerical Lock From Current Closure

The current closure values remain:

```text
u_3 = 0.2429466120286312
N50 = 0.21500703361675252
dX_FLRW/dN = 4.116130666115856
J_M quadratic coefficient = 209.2130223887545
F'''(0) = 418.426044777509
```

Interpretation:

```text
J_M starts as 209.2130223887545 N^2 near the endpoint.
```

So the source/current has the double-zero required by the C2 repair:

```text
J_M(0) = 0
J_M'(0) = 0
```

## 5. Non-Circularity Tests

The route only counts if it passes these tests:

```text
do not define I_M as X^3 without an independent reason;
do not define X_FLRW as N/u_3 by fit inheritance;
do not define J_M as the desired answer;
do not add the background term without a Bianchi/conservation owner;
do not let the same current generate local PPN hair.
```

Current status:

```text
I_M = det(Q) guards the cubic from being arbitrary;
Q^i_j itself is not yet derived;
X_FLRW = N/u_3 is not yet derived;
u_3 is not yet predicted;
b_mem is not yet predicted;
conservation ownership is not yet defined.
```

So the contract improves the route, but does not promote it.

## 6. Candidate Mechanisms

The candidate mechanisms are:

```text
isotropic_load_tensor_determinant   best contract candidate, not derivation
exact_three_form_memory_current     plausible but unbuilt
Raychaudhuri_or_expansion_load      partial route for N only
quadratic_hazard_postulate          too circular alone
local_double_zero_unification       consistency principle, not mechanism
```

The determinant route is the one to attack next because it naturally explains
why there are exactly three powers: three equal spatial/load eigen-directions in
the homogeneous isotropic branch.

That is much better than treating p=3 as a fitted exponent with a lab coat.

## 7. Gate Verdict

Gate result:

```text
cubic_memory_current_contract_identified   pass_conditional
parent_load_tensor_defined                 fail
X_FLRW_equals_N_over_u3_derived             fail
u3_parent_predicted                         fail
bmem_parent_predicted                       fail
conservation_owner_defined                  fail
local_silence_contract_defined              open
support_claim_allowed                       fail
```

This is exactly the right kind of mixed result:

```text
not dead;
not proven;
more structured than before.
```

## 8. Decision

Decision:

```text
FLRW_memory_current_status = contract_identified_not_derived
```

Meaning:

```text
p=3 has a plausible parent-current contract through I_M = det(Q);
the parent load tensor Q^i_j is now the central missing object;
deriving Q^i_j would move the cosmology branch closer to real field theory;
failing to derive Q^i_j leaves the branch as a disciplined closure benchmark.
```

This is useful because it narrows the next derivation attempt to one target:

```text
derive or reject Q^i_j.
```

## 9. Next Target

Create:

```text
52-load-tensor-origin-attempt.md
```

Purpose:

```text
attempt to derive Q^i_j from parent motion/time/space variables and show that
its FLRW determinant gives the memory activation while its local stationary
projection stays silent enough for GR/PPN.
```

Pass condition:

```text
Q^i_j can be defined before FLRW symmetry is imposed, reduces to X_FLRW delta^i_j
in cosmology, and has a plausible local-vacuum suppression route.
```

Fail condition:

```text
Q^i_j can only be invented after seeing the desired cubic law.
```
