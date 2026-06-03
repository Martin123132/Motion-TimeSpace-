# 326 — Radial-Memory Parent-Action Contract

Private derivation checkpoint. This is not a public GR, PPN, CMB, cosmology, or unified-field claim.

## Purpose

Checkpoint 325 says the locked `2/27` branch remains worth protecting:

```text
no-CMB BAO+H(z) = stable competitive draw vs LCDM,
edge-clean for locked MTS and LCDM,
no SN or CMB support inserted.
```

This checkpoint asks the derivation question directly:

```text
Can the radial memory kernel and amplitude be derived now?
```

Short answer:

```text
conditional kernel derivation: yes
conditional trace amplitude: yes
parent action derivation: no
```

So this is real progress, but not a promotion.

## Machine Artifact

Script:

```text
scripts/radial_memory_parent_action_contract.py
```

Run:

```text
runs/20260601-153000-radial-memory-parent-action-contract
```

Status:

```text
radial_memory_kernel_conditional_survival_action_contract_not_parent_derived
```

Claim ceiling:

```text
conditional_radial_memory_contract_no_GR_CMB_or_Bmem_promotion
```

## Kernel Derivation Attempt

The locked empirical branch uses:

```text
A(y) = 1 - exp[-(y/u3)^3],
y = ln(1+z),
u3 = 1/4.
```

This can be derived conditionally from a survival/first-activation law:

```text
dA/dy = (1-A) dH/dy,
H(y) = (y/u3)^3.
```

Then:

```text
A(y) = 1 - exp[-H(y)]
     = 1 - exp[-(y/u3)^3].
```

That is a proper mathematical origin for the exponential form if the parent action supplies a cumulative cubic hazard `H(y)`.

What is not derived yet:

```text
why H is cubic,
why u3=1/4,
why this hazard belongs only to the MTS/FLRW memory sector.
```

## Local-in-y Silence

For `u3=1/4`:

```text
A(y) = 64 y^3 + O(y^6).
```

The artifact verifies:

| Quantity | Value | Status |
|---|---:|---|
| `A(0)` | 0 | pass |
| `A'(0)` | 0 | pass |
| `A''(0)` | 0 | pass |
| `A'''(0)` | 384 | pass |

This gives a clean double-zero:

```text
A(0)=A'(0)=A''(0)=0.
```

Meaning:

```text
the first late-time radial-memory deformation is cubic in y=ln(1+z).
```

This is useful, but it is not a local PPN proof. It is only a background/kernel smoothness result unless the parent action also proves local ordinary-bath annihilation.

## Amplitude Trace

Use the conditional active projector:

```text
P_active = P_M,singlet tensor P_T,singlet tensor P_screen.
```

The artifact verifies:

| Object | Dimension | Trace | Rank | Normalized Trace |
|---|---:|---:|---:|---:|
| `P_M_singlet` | 3 | 1 | 1 | 1/3 |
| `P_T_singlet` | 3 | 1 | 1 | 1/3 |
| `P_screen` | 3 | 2 | 2 | 2/3 |
| `P_active` | 27 | 2 | 2 | 2/27 |
| bad spatial lift | 27 | 18 | 18 | 2/3 |
| scalar trace lift | 27 | 1 | 1 | 1/27 |

So the conditional amplitude route is:

```text
B_mem = kappa_mem Tr(P_active)/dim(V_cell)
      = kappa_mem * 2/27.
```

If the parent action proves:

```text
dim(V_cell)=27,
P_active=P_M,singlet tensor P_T,singlet tensor P_screen,
kappa_mem=1,
```

then:

```text
B_mem = 2/27.
```

But `kappa_mem=1` is still not parent-derived.

## Conservation/Bianchi Check

Treat the memory contribution as:

```text
rho_mem / rho_crit0 = B_mem A(y).
```

Bianchi compatibility requires an effective pressure:

```text
p_mem / rho_crit0 = -B_mem A(y) + (B_mem/3) dA/dy.
```

The artifact verifies:

```text
p_mem -> 0 as y -> 0,
p_mem -> -B_mem as y -> infinity.
```

This means the background memory term can be written as a conserved effective stress if the pressure term is included.

Important caution:

```text
w_mem = p_mem/rho_mem
```

is not a useful variable exactly at `y=0`, because `rho_mem=0` there. The pressure itself is finite; the ratio is the bad variable.

## Gate Results

| Gate | Status |
|---|---|
| source paths exist | pass |
| `P_active` idempotent | pass |
| `P_active` trace = 2 | pass |
| `P_active` normalized trace = 2/27 | pass |
| bad spatial lift rejected as 2/3 | pass |
| survival kernel double-zero | pass |
| effective pressure finite | pass |
| `dim(V_cell)=27` parent-derived | fail |
| `kappa_mem=1` parent-derived | fail |
| `u3=1/4` parent-derived | fail |
| `C_D` parent-derived | fail |
| `[K_boundary,A_D]=0` parent-derived | fail |
| local PPN residual zero derived | fail |
| promotion allowed | fail |

## What This Actually Derives

This checkpoint derives the exact conditional chain:

```text
parent cubic cumulative hazard H(y)=(y/u3)^3
=> A(y)=1-exp[-H(y)]
=> A(y)=1-exp[-(y/u3)^3].
```

and:

```text
S3 singlet motion channel
+ S3 singlet time/history channel
+ transverse screen channel
=> Tr(P_active)/27 = 2/27.
```

Together:

```text
E^2(z) = E_LCDM^2(z) + B_mem A(ln(1+z))
```

becomes a field-theory target rather than a naked fit function.

## What Still Fails

The parent action still has to throw the punch itself:

```text
derive the cubic hazard,
derive u3=1/4,
derive kappa_mem=1,
derive C_D,
derive [K_boundary,A_D]=0,
derive local ordinary-bath annihilation,
derive zero PPN residual without a plateau axiom.
```

The most important missing object is still:

```text
J_C.
```

We need a parent current/charge/holonomy such that:

```text
J_C -> C_D,
A_D = C_D^\dagger C_D,
[K_boundary,A_D]=0,
C_D B_ord = 0,
C_D B_FLRW != 0,
H_FLRW(y) = (y/u3)^3.
```

## Decision

Decision:

```text
radial_memory_kernel_conditional_survival_action_contract_not_parent_derived
```

Allowed language:

```text
The locked radial-memory kernel has a clean conditional survival-law derivation and a clean conditional 2/27 trace-amplitude route.
```

Forbidden language:

```text
MTS derives B_mem=2/27.
MTS derives local GR.
MTS passes PPN.
MTS derives CMB compatibility.
```

## Boxing Readout

This is a good technical round.

Not a knockout. Not a title.

But we did land something:

```text
the exponential memory shape is no longer just "because it fits";
it is the unique survival activation for a cumulative cubic hazard.
```

The judges still need to see where the hazard comes from.

## Next Target

Two honest next routes:

```text
Route A: keep deriving.
Find a parent current J_C whose FLRW projection produces H(y)=(y/u3)^3
and whose local projection annihilates ordinary baths.

Route B: keep testing.
Run growth/fsigma8 as the next external judge of the locked background.
```

Default recommendation:

```text
attempt Route A once more, focused only on J_C.
If J_C does not appear, move to growth.
```

## Output Files

```text
runs/20260601-153000-radial-memory-parent-action-contract/status.json
runs/20260601-153000-radial-memory-parent-action-contract/results/source_register.csv
runs/20260601-153000-radial-memory-parent-action-contract/results/projector_trace_algebra.csv
runs/20260601-153000-radial-memory-parent-action-contract/results/activation_kernel.csv
runs/20260601-153000-radial-memory-parent-action-contract/results/theorem_clauses.csv
runs/20260601-153000-radial-memory-parent-action-contract/results/gate_results.csv
runs/20260601-153000-radial-memory-parent-action-contract/results/decision.csv
```
