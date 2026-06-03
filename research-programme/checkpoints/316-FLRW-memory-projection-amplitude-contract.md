# 316 - FLRW Memory Projection Amplitude Contract

Private derivation checkpoint. This is not a public cosmology, CMB, local-GR, or parent-field-theory claim.

## Purpose

Checkpoint 315 made the empirical problem sharper:

```text
B_mem is nonzero,
close to 2/27,
stable across DESI DR2/DR1 in the full-cov no-SH0ES fitted branch,
and not prior-edge driven.
```

This checkpoint asks what can actually be derived now.

Short answer:

```text
FLRW shape: conditionally derived.
LCDM background limit: derived.
memory source budget: derived for supplied B_mem.
B_mem = 2/27: not parent-derived.
```

So the branch improves as a field-theory contract, but the amplitude still does not get a passport.

## Terminology Repair

There are two nearby branches and we must not blur them:

| Branch | Fixed | Fitted | Meaning |
|---|---|---|---|
| shape-fixed / B-fitted | `p=3`, `u3=1/4` | `B_mem` | latest full-cov no-SH0ES score branch |
| fully-fixed `2/27` | `p=3`, `u3=1/4`, `B_mem=2/27` | no memory amplitude | strict closure theorem-target branch |

The first asks:

```text
where does the data want the amplitude?
```

The second asks:

```text
does the sharp theorem target survive without an extra amplitude hand?
```

Both are useful. Only the second is the disciplined no-amplitude lead branch.

## Conditional Projection Theorem

Assume a parent FLRW coherent-load tensor exists:

```text
Q^i_j = X_FLRW delta^i_j.
```

Then:

```text
I_M = det(Q) = X_FLRW^3.
```

If the no-clock projection later derives:

```text
X_FLRW = N/u3,
```

with:

```text
N = ln(a0/a) = ln(1+z),
```

then:

```text
F(N) = 1 - exp[-(N/u3)^3].
```

This gives:

```text
p = 3
```

from the determinant of a three-direction isotropic load, not from a fitted exponent.

For:

```text
u3 = 1/4,
```

the endpoint expansion is:

```text
F(0)=0,
F'(0)=0,
F''(0)=0,
F'''(0)=384.
```

So the memory source has the required double zero at the local endpoint:

```text
S_mem(0)=0,
S_mem'(0)=0.
```

That is a real derivation of the shape conditional on `Q` and `X_FLRW`.

It is not a derivation of the amplitude.

## Conservation Law

Use:

```text
Omega_mem(N) = B_mem F(N).
```

Then the memory source is:

```text
S_mem(N) = dOmega_mem/dN = B_mem F'(N).
```

Therefore:

```text
integral_0^infinity S_mem dN = B_mem.
```

So `B_mem` is exactly the integrated memory-source budget.

For a conserved effective stress with `N=ln(a0/a)`:

```text
rho_mem' = 3(rho_mem + p_mem),
```

hence:

```text
p_mem = -rho_mem + rho_mem'/3.
```

This proves that a supplied `B_mem F(N)` can be made into a conserved effective FLRW stress.

It also proves the limit of this method:

```text
Bianchi fixes pressure response.
Bianchi does not fix B_mem.
```

## LCDM Limit

The projected background equation is:

```text
E_MTS^2(N) = Omega_m exp(3N) + 1 - Omega_m + B_mem F(N).
```

Therefore:

```text
B_mem -> 0
```

gives:

```text
E_LCDM^2(N) = Omega_m exp(3N) + 1 - Omega_m.
```

This is exact at background level.

The numerical runner already verifies the same thing:

```text
MTS_Bmem_zero collapses onto LCDM.
```

So the negative control is a true background limit, not just a coding coincidence.

## Amplitude Contract

The clean parent amplitude law would be:

```text
B_mem = kappa_mem Tr(P_active) / dim(V_cell).
```

To derive:

```text
B_mem = 2/27,
```

the parent theory must prove:

```text
dim(V_cell)=27,
Tr(P_active)=2,
kappa_mem=1.
```

Current status:

| Requirement | Status | Why |
|---|---|---|
| `p=3` | conditional | determinant route gives cubic shape |
| `u3=1/4` | conditional/open | no-clock cell route exists but is not a parent theorem |
| `dim(V_cell)=27` | not derived | needs a real ternary-per-spatial-leg cell theorem |
| `rank(P_active)=2` | not derived | scalar FLRW symmetry alone does not pick rank two |
| `kappa_mem=1` | not derived | Bianchi/topology do not fix stress normalization |
| `B_mem=2/27` | closure target | requires all three amplitude clauses |

This is the exact contract a future parent action must satisfy.

## Empirical Alignment

The latest fitted shape-fixed values imply:

| Branch | Fitted `B_mem` | Implied `kappa_mem = B_mem / (2/27)` |
|---|---:|---:|
| DESI DR2 full-cov no-SH0ES | 0.074533 | 1.006198 |
| DESI DR1 full-cov no-SH0ES | 0.073418 | 0.991149 |

That is very interesting.

It says:

```text
the fitted amplitude lands within about 1 percent of the strict 2/27 target.
```

But it does not derive the target.

Allowed language:

```text
2/27 is empirically well-aligned with the latest fitted amplitude and remains a sharp theorem target.
```

Forbidden language:

```text
2/27 is derived.
```

## No-Go Lemmas

The current work rules out three tempting cheats:

| Cheat | Why It Fails | What Survives |
|---|---|---|
| Bianchi derives `B_mem` | continuity scales with supplied `B_mem` | pressure consistency |
| determinant derives `B_mem` | `det(Q)` gives cubic shape, not stress normalization | conditional `p=3` |
| topology derives bulk stress | metric-independent topology has no bulk metric variation | local silence/channel counting |

The key remaining debt is:

```text
kappa_mem.
```

If `kappa_mem` is not derived, then:

```text
B_mem = 2/27
```

stays a closure target even if rank `2/27` is later derived.

## Decision

Decision:

```text
FLRW_memory_projection_contract_conditionally_derived_LCDM_limit_proved_Bmem_parent_derivation_still_fails
```

Claim ceiling:

```text
conditional_FLRW_projection_contract_no_parent_amplitude_promotion
```

Meaning:

```text
we have a cleaner field-theory spine for the FLRW branch,
but the amplitude still has to be earned by a parent stress-normalization theorem.
```

Boxing translation:

```text
We landed the jab clean:
shape, conservation, source budget, and LCDM limit.
The title shot still waits on kappa_mem.
```

## Next Target

Theory next:

```text
derive kappa_mem=1 from a metric-variation/Ward identity,
or permanently label 2/27 as closure-only.
```

Empirical next:

```text
run the fully-fixed 2/27 branch through the same full-cov no-SH0ES DR2/DR1 release matrix,
with LCDM, wCDM, and CPL under the same nuisance and covariance policy.
```

## Machine Artifacts

Script:

```text
scripts/FLRW_memory_projection_amplitude_contract.py
```

Run:

```text
runs/20260601-000143-FLRW-memory-projection-amplitude-contract
```

Output files:

```text
runs/20260601-000143-FLRW-memory-projection-amplitude-contract/results/source_register.csv
runs/20260601-000143-FLRW-memory-projection-amplitude-contract/results/mathematical_identities.csv
runs/20260601-000143-FLRW-memory-projection-amplitude-contract/results/amplitude_budget.csv
runs/20260601-000143-FLRW-memory-projection-amplitude-contract/results/conservation_LCDM_limit_checks.csv
runs/20260601-000143-FLRW-memory-projection-amplitude-contract/results/theorem_contract_clauses.csv
runs/20260601-000143-FLRW-memory-projection-amplitude-contract/results/no_go_lemmas.csv
runs/20260601-000143-FLRW-memory-projection-amplitude-contract/results/gate_results.csv
runs/20260601-000143-FLRW-memory-projection-amplitude-contract/results/decision.csv
```
