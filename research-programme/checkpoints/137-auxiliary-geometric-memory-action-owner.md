# 137 - Auxiliary / Geometric Memory Action Owner

Private theorem / action-owner checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 136 ended with the live fork:

```text
either construct an auxiliary/geometric parent owner,
or demote locked memory to an empirical EFT closure.
```

This checkpoint asks:

```text
Can an auxiliary action remove the propagating memory mode while preserving
conservation, pressure, and local silence?
```

## 2. Machine Artifact

Script:

```text
research-programme\scripts\auxiliary_geometric_memory_action_owner.py
```

Run:

```text
research-programme\runs\20260531-200000-auxiliary-geometric-memory-action-owner
```

Generated:

```text
source_register.csv
constraint_variation_chain.csv
required_pressure_kernel.csv
action_candidate_ledger.csv
noether_bianchi_tests.csv
local_silence_tests.csv
summary.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
auxiliary_constraint_route_sharpened_not_derived
```

Claim ceiling:

```text
auxiliary_geometric_contract_not_parent_derivation
```

## 3. Best Candidate Action

The cleanest exact route is an algebraic auxiliary constraint:

```text
S_aux =
integral sqrt(-g)[
  -rho_M(I_M)
  + lambda_M (I_M - F(C_coh,Q,J_rel))
]
```

where:

```text
C_coh = coherent-domain smoothness invariant
Q = coherent load / determinant variable
J_rel = relative boundary current
```

The variations are:

```text
delta S / delta lambda_M = 0
=> I_M = F(C_coh,Q,J_rel)
```

and:

```text
delta S / delta I_M = 0
=> lambda_M = d rho_M / d I_M
```

So `I_M` has no independent kinetic equation.

That is good:

```text
no propagating memory scalar is introduced.
```

But it is not enough.

## 4. Exact Pressure Requirement

The locked branch needs:

```text
rho_M / rho_crit0 = 1 - Omega_m0 + B_mem A(N)
B_mem = 2/27
```

with:

```text
p_M = -rho_M + (1/3) d rho_M / dN
```

Therefore:

```text
p_M + rho_M = B_mem A_N / 3
```

The audit checked this against the checkpoint-136 potential map:

| Check | Value |
|---|---:|
| rows checked | `701` |
| max identity error | `1.1102230246251565e-16` |
| active pressure rows | `337` |
| peak `p+rho` | `0.1160898276990483` |
| peak redshift | `z ~= 0.24339588919498212` |

This is now the exact missing kernel.

The parent action must produce:

```text
delta_g F(C_coh,Q,J_rel)
```

such that the auxiliary stress supplies:

```text
p+rho = B_mem A_N / 3.
```

If it cannot do that, the auxiliary action is just a silent `w=-1` gate and not the locked memory branch.

## 5. What Works

The auxiliary route gives three useful things:

### No Independent Memory Clustering

Because `I_M` has no kinetic term:

```text
delta I_M = F_C delta C_coh + F_Q delta Q + F_J delta J_rel.
```

Checkpoint 132 already gave:

```text
delta C_coh^(1) = 0
```

around the FLRW bulk branch.

So exact smooth memory is plausible if:

```text
delta F^(1) = 0
```

for coherent-domain perturbations.

### Formal Bianchi Safety

If the full action is covariant:

```text
nabla_mu T_total^munu = 0
```

follows on shell.

The multiplier stress is not optional bookkeeping; it is the exchange carrier that keeps the gated memory source conserved.

### Local Silence Target

The local requirement is now sharp:

```text
F(C_coh,Q,J_rel) = 0
delta F^(1) = 0
```

in bound local domains.

That is much cleaner than saying:

```text
memory just switches off locally.
```

## 6. What Still Fails

The route is not yet derived.

Current failures:

```text
no S_cell/S_stress variation derives the pressure kernel;
B_mem = 2/27 remains inserted;
p = 3 remains inserted;
u3 = 1/4 remains inserted;
local PPN silence is a branch condition, not a theorem;
CMB perturbation behavior is not tested here.
```

So the result is:

```text
exact route sharpened,
not parent theory solved.
```

## 7. Candidate Ledger

| Candidate | Verdict |
|---|---|
| algebraic auxiliary memory | best exact route but still a contract |
| four-form / topological flux | good silence, bad activation pressure |
| BF relative boundary polarization | best topological support, not full stress owner |
| geometric counterstress | heavy route after auxiliary kernel is exhausted |
| controlled exchange `Q^nu` | last resort, not preferred |

The four-form route is useful but not enough:

```text
it naturally gives no local hair,
but tends to behave like w=-1 unless extra metric dependence is added.
```

The auxiliary route is better because:

```text
it can be non-propagating and still carry pressure through constraint variation.
```

But the required pressure variation has to be derived.

## 8. Gates

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | source register checked |
| auxiliary constraint written | pass formal | `I_M=F` and no independent kinetic mode |
| smooth memory mode removed | pass conditional | requires `delta F^(1)=0` |
| activation pressure kernel identified | pass | `p+rho=B_mem A_N/3` |
| activation pressure kernel derived | fail | no parent variation produces it yet |
| total Bianchi conservation | pass formal | full covariant action gives total conservation |
| local PPN silence | open | local `F=0`, `delta F=0` not derived |
| `B_mem,p,u3` derivation | fail | constants still supplied by locked branch |
| growth branch promotion | fail | theorem target, not derived perturbation theory |

## 9. Decision

Decision:

```text
auxiliary_constraint_route_sharpened_not_derived
```

Meaning:

```text
we have the right kind of action skeleton for exact smooth memory,
but not yet the parent theorem that makes it predictive.
```

Boxing-score version:

```text
We found the footwork pattern.
It can slip the perfect-fluid punch.
But it still has to throw the exact pressure counter,
or the judges will mark it as clever defence with no scoring shot.
```

## 10. Next Target

The next derivation target is now precise:

```text
derive the pressure kernel p+rho = B_mem A_N / 3
from a coherent-domain metric variation of F(C_coh,Q,J_rel).
```

Useful clue:

```text
if N is a coherent volume variable, N = -ln a,
then spatial metric variation can generate
p = -rho + (1/3) d rho / dN.
```

That is the next thing to try.

If this kernel cannot be derived, the honest status is:

```text
locked memory remains a healthy empirical EFT closure branch,
not a derived parent field theory.
```

