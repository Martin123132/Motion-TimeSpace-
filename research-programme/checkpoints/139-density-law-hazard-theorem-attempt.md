# 139 - Density Law Hazard Theorem Attempt

Private theorem checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 138 derived the pressure kernel conditionally:

```text
p_M = -rho_M + (1/3) d rho_M / dN_D.
```

That moved the bottleneck to the density law:

```text
rho_M(N_D) = rho_Lambda + B_mem[1-exp(-(N_D/u3)^3)].
```

This checkpoint asks:

```text
Can the exponential activation shape be derived rather than inserted?
```

Short answer:

```text
yes, conditionally, as an additive-hazard survival law.
```

But:

```text
B_mem = 2/27 is still not derived.
```

## 2. Machine Artifact

Script:

```text
research-programme\scripts\density_law_hazard_theorem_attempt.py
```

Run:

```text
research-programme\runs\20260531-203000-density-law-hazard-theorem-attempt
```

Generated:

```text
source_register.csv
hazard_derivation_chain.csv
activation_shape_tests.csv
survival_composition_tests.csv
alternative_law_ledger.csv
amplitude_route_ledger.csv
summary.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
density_hazard_shape_derived_conditionally_amplitude_not_derived
```

Claim ceiling:

```text
hazard_density_shape_conditional_amplitude_not_derived
```

## 3. Hazard Derivation

Assume a cumulative coherent exposure:

```text
I_M
```

with additive independent increments:

```text
I(D_1 union D_2) = I(D_1) + I(D_2).
```

Let:

```text
S(I)
```

be the unactivated survival fraction.

Independent increments require:

```text
S(I_1 + I_2) = S(I_1) S(I_2)
S(0) = 1
```

With continuity and monotonicity, the solution is:

```text
S(I) = exp(-kappa I).
```

Absorb `kappa` into the dimensionless exposure:

```text
I_M = kappa I.
```

Then:

```text
A(I_M) = 1 - S(I_M) = 1 - exp(-I_M).
```

So the exponential saturation is not arbitrary if the exposure is a true additive hazard.

## 4. Locked Branch Chain

The conditional MTS chain is:

```text
I_M = det(Q)
Q^i_j = X delta^i_j
I_M = X^3
X = 4N_D = N_D/u3
u3 = 1/4
```

therefore:

```text
I_M = (N_D/u3)^3
```

and:

```text
A(N_D) = 1 - exp[-(N_D/u3)^3].
```

This gives the shape of:

```text
rho_M = rho_Lambda + B_mem A(N_D).
```

But it only gives the shape.

It does not give:

```text
B_mem = 2/27.
```

## 5. Numerical / Logical Checks

The audit checked the activation law on the same 701-point grid used by checkpoint 138.

| Check | Value |
|---|---:|
| rows checked | `701` |
| max hazard-rate error | `0.0` |
| max survival-composition error | `6.938893903907228e-18` |
| bounded failures | `0` |
| monotone failures | `0` |
| endpoint failures | `0` |
| `A(z=3)` | `1.0` |

So:

```text
A=1-exp(-I_M)
```

passes the hazard, boundedness, monotonicity, and endpoint regularity checks.

## 6. Alternative Laws

| Law | Verdict |
|---|---|
| `1-exp(-I)` | retained conditional unique shape |
| `I` | rejected: unbounded, not survival law |
| `I/(1+I)` | rejected: no independent-increment composition |
| `tanh(I)` | rejected: no hazard composition |
| shifted logistic | rejected: extra shape without parent need |

This is a useful narrowing:

```text
if the parent object is additive exposure,
then exponential survival is the clean law.
```

## 7. What This Fixes

Before this checkpoint:

```text
the pressure kernel was conditionally derived,
but rho_M(N_D) still looked inserted.
```

After this checkpoint:

```text
the activation shape is theorem-shaped:
additive exposure + survival composition -> exponential saturation.
```

So the density law is now split:

```text
shape: conditionally derived;
amplitude: not derived.
```

That is a better position.

## 8. What Still Fails

The branch is still not a complete parent derivation.

Open/failing pieces:

```text
Q^i_j parent action;
coherent-domain selector D;
safe boundary current J_rel;
3+1 cell normalization u3=1/4;
normalized amplitude B_mem=2/27;
local N_D=0 and delta N_D=0 theorem;
full perturbation action.
```

Most importantly:

```text
hazard law cannot derive B_mem.
```

It fixes:

```text
how the release saturates.
```

It does not fix:

```text
how much total charge is released.
```

## 9. Gates

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | source register checked |
| survival law from additive hazard | pass conditional | hazard error `0`, composition error `6.94e-18` |
| activation shape regular | pass | no bounded/monotone/endpoint failures |
| `p=3` from determinant | pass conditional | if `Q^i_j=X delta^i_j` |
| `u3=1/4` from 3+1 cell | pass conditional | only if parent-owned |
| density shape derived | pass conditional | once `B_mem` is supplied |
| `B_mem` amplitude derived | fail | hazard law does not fix total charge |
| domain/boundary owner | open | additive exposure and local silence still need action owner |
| parent field theory promoted | fail | shape is not whole theory |

## 10. Decision

Decision:

```text
density_hazard_shape_derived_conditionally_amplitude_not_derived
```

Meaning:

```text
the exponential density shape is no longer just a convenient curve
if the memory exposure is an additive hazard.
```

Boxing-score version:

```text
That was another points-scoring counter.
The shape now has footwork.
But the amplitude is still standing there asking for its birth certificate.
```

## 11. Next Target

The bottleneck is now sharply:

```text
B_mem = 2/27.
```

The only serious theory route remains:

```text
derive a normalized boundary charge:
DeltaR = Q_boundary / Q_* = 2/9
and B_mem = DeltaR / 3 = 2/27.
```

If that cannot be derived, the honest statement becomes:

```text
MTS has a strong locked empirical EFT branch with derived/conditional shape
mechanics, but amplitude remains empirical closure.
```

