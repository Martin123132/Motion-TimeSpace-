# 136 - Memory Action Potential Owner Attempt

Private theorem / EFT-owner checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 135 showed that the locked memory background can be represented by a healthy canonical scalar with:

```text
c_s^2 = 1
K >= 0
V > 0
Delta phi ~= 0.145 Mpl from z=0 to z=3
```

That gave the growth route a legal effective-field owner.

This checkpoint asks the harder question:

```text
Can the MTS memory variables own that potential non-circularly,
or are we still reconstructing an EFT from the desired background?
```

## 2. Machine Artifact

Script:

```text
research-programme\scripts\memory_action_potential_owner_attempt.py
```

Run:

```text
research-programme\runs\20260531-194000-memory-action-potential-owner-attempt
```

Generated:

```text
source_register.csv
potential_map_reconstruction.csv
action_candidate_ledger.csv
noncircularity_tests.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
potential_map_reconstructed_parent_action_not_derived
```

Claim ceiling:

```text
potential_map_reconstructed_not_parent_action
```

## 3. Exact Reconstruction Identities

Use the determinant-style activation candidate:

```text
I_M = (N/u3)^3
N = ln(1+z)
u3 = 1/4
A = 1 - exp(-I_M)
B_mem = 2/27
```

Then:

```text
rho_mem / rho_crit0 = 1 - Omega_m0 + B_mem A
E^2 = Omega_m0 exp(3N) + rho_mem
```

The canonical scalar reconstruction gives:

```text
K / rho_crit0 = B_mem A_N / 6
V / rho_crit0 = rho_mem - K
dphi/dN = sqrt(B_mem A_N / E^2)
```

This exactly reproduces checkpoint 135 numerically:

| Test | Result |
|---|---:|
| rows checked | `701` |
| max formula error | `1.1102230246251565e-16` |
| missing cited sources | `0` |
| `V(phi)` monotonic/single-valued failures | `0` |

So the reconstruction is internally clean.

## 4. Where the Parent Derivation Fails

The determinant variable helps, but it does not yet solve the parent-action problem.

Reason:

```text
I_M -> A(N)
```

owns the activation map only after we have already supplied:

```text
p = 3
u3 = 1/4
B_mem = 2/27
```

It also does not own the pressure by itself.

A pure potential:

```text
S = integral sqrt(-g)[-U(I_M)]
U = rho_Lambda + B_mem(1-exp(-I_M))
```

would give:

```text
K = 0
w = -1
```

so it cannot reproduce the required activation pressure.

The canonical scalar fixes this:

```text
S = integral sqrt(-g)[-1/2(partial phi)^2 - V(phi)]
```

but only because `phi(N)` and `V(phi)` are reconstructed from the locked background.

That is EFT ownership, not parent prediction.

## 5. Bare `I_M` Kinetic Metric Problem

One tempting route is:

```text
S = integral sqrt(-g)[-1/2 G(I_M)(partial I_M)^2 - U(I_M)]
```

with:

```text
G(I_M) = (dphi/dI_M)^2
```

This is formally possible, but not clean.

The audit found:

```text
finite sample min G(I_M) = 8.81902212145948e-80
finite sample max G(I_M) = 98.18908486386819
endpoint limit = singular
```

The endpoint issue is structural:

```text
dI_M/dN -> 0 faster than dphi/dN as N -> 0
```

so using bare `I_M` as the scalar coordinate makes the kinetic metric singular at the present endpoint.

This does not kill the canonical EFT.

It does kill the naive claim:

```text
det(Q) alone is the smooth parent scalar.
```

## 6. Action Candidate Ledger

| Candidate | Verdict |
|---|---|
| determinant activation only | useful variable, not parent action |
| potential-only `U(I_M)` | rejected as full owner because `K=0` forces `w=-1` |
| canonical reconstructed `phi` | best EFT owner, not fundamental origin |
| `I_M` kinetic metric | not clean because reconstructed and endpoint-singular |
| auxiliary constraint | theorem target, not yet constructed |
| geometric counterstress | heavy route if auxiliary route fails |

## 7. Gates

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | source register checked |
| formula reconstruction | pass | max error `1.1102230246251565e-16` |
| `V(phi)` single-valued | pass | no monotonic or duplicate-potential conflicts |
| canonical EFT owner | pass effective | owns stress and `c_s^2=1` |
| determinant activation owner | partial | owns activation after `p,u3` are supplied |
| bare `I_M` action regular | fail | endpoint kinetic metric singular |
| parent action non-circularity | fail | `V(phi)` and `G(I_M)` are reconstructed |
| `B_mem` amplitude derivation | fail | `2/27` is still inserted |
| exact local-GR transfer | open | cosmological EFT health is not PPN proof |

## 8. Decision

The result is good, but not magical.

We have:

```text
a clean EFT glove
```

not yet:

```text
the parent training camp that manufactures the glove.
```

Boxing-score version:

```text
MTS stays in the round.
The growth-sector hand is legal.
But the referee will not let us claim the glove was forged by the parent action
until the action actually produces p, u3, B_mem, V(phi), and local silence.
```

Decision:

```text
potential_map_reconstructed_parent_action_not_derived
```

Meaning:

```text
checkpoint 130 remains supported as a late-time subhorizon EFT target;
checkpoint 135 remains a healthy effective owner;
this checkpoint blocks the naive determinant-only parent derivation.
```

## 9. Next Target

The next serious derivation route is not to keep polishing the reconstructed `V(phi)`.

It is:

```text
construct an auxiliary/geometric memory action where I_M is constrained by
C_coh / Q / cell-boundary data, and where the resulting stress is conserved
and locally silent.
```

If that cannot be built, the honest demotion is:

```text
locked 2/27 memory = empirical EFT closure branch,
not derived parent field theory.
```

