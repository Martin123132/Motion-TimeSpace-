# 331 — Trace-Normalized Hamiltonian Amplitude Contract

Private derivation checkpoint. This is not a public cosmology, CMB, local-GR, PPN, perturbation-theory, or unified-field claim.

## Purpose

Checkpoint 330 fixed an important scoring-contract bug:

```text
the primary branch now really locks B_mem = 2/27,
instead of fitting B_mem while only fixing p=3 and u3=1/4.
```

The corrected release split then gave a sharper theory question:

```text
why does the fitted diagnostic amplitude sit so close to 2/27?
```

This checkpoint tries to derive as much as possible without cheating.

Short answer:

```text
the exact amplitude factorization is derived,
the empirical kappa window is now tight,
but the parent theorem still has two missing locks.
```

## Machine Artifact

Script:

```text
scripts/trace_normalized_Hamiltonian_amplitude_contract.py
```

Run:

```text
runs/20260601-181000-trace-normalized-Hamiltonian-amplitude-contract
```

Status:

```text
trace_normalized_Hamiltonian_contract_written_unit_amplitude_not_parent_derived
```

Claim ceiling:

```text
conditional_amplitude_contract_no_parent_Bmem_promotion
```

## The Derived Factorization

Assume the memory term is not a free potential, but a trace-normalized Hamiltonian current:

```text
rho_mem = epsilon_H (3 M_Pl^2 H_star^2) q_trace F(N).
```

with:

```text
q_trace = Tr(P_active)/dim(V_cell),
N = ln(1+z),
F(0)=0,
F(infinity)=1.
```

Divide by:

```text
rho_c0 = 3 M_Pl^2 H0^2.
```

Then the dimensionless amplitude must factor as:

```text
B_mem = q_trace epsilon_H (H_star/H0)^2.
```

For the current active-trace contract:

```text
q_trace = 2/27.
```

Therefore:

```text
B_mem = 2/27
```

follows exactly if and only if:

```text
epsilon_H = 1,
H_star = H0,
q_trace = 2/27.
```

That is the cleanest current theorem statement.

It is a real derivation of the amplitude structure, but not yet a parent derivation of the locked amplitude.

## What Is New After 330

The corrected release split lets us compare:

```text
locked amplitude:
  B_mem = 2/27

diagnostic fitted amplitude:
  B_mem free with p=3, u3=1/4
```

under the same full-covariance, no-SH0ES SN+BAO wrapper.

| Release | locked `B_mem` | fitted `B_mem` | fitted `kappa` | `kappa-1` | locked-fitted chi2 |
|---|---:|---:|---:|---:|---:|
| DR2 | 0.0740740741 | 0.0745331916 | 1.0061980866 | +0.0061980866 | +0.0001917938 |
| DR1 | 0.0740740741 | 0.0734184619 | 0.9911492352 | -0.0088507648 | +0.0002839167 |

So the free diagnostic says:

```text
kappa is within one percent of unity on both DESI releases.
```

And the locked branch beats the fitted-amplitude diagnostic by information criteria:

| Release | locked-fitted AIC | locked-fitted BIC |
|---|---:|---:|
| DR2 | -1.9998082062 | -7.4004287836 |
| DR1 | -1.9997160833 | -7.3997256004 |

Meaning:

```text
the data do not pay for kappa freedom.
```

This is the strongest current reason to keep `2/27` as the lead branch.

But it is still empirical discipline, not parent ownership.

## The No-Go Result

The factorization exposes the exact failure modes.

If:

```text
rho_mem -> lambda rho_mem,
```

then:

```text
B_mem -> lambda B_mem.
```

Bianchi, pressure consistency, and the scoring pipeline all still work.

So stress-form variation alone cannot derive:

```text
epsilon_H = 1.
```

Likewise, if:

```text
H_star -> xi H_star,
```

then:

```text
B_mem -> xi^2 B_mem.
```

So the geometric route still requires:

```text
H_star = H0.
```

Finally:

```text
F(0)=0
```

means the present Friedmann normalization:

```text
E(0)=1
```

cannot fix the memory amplitude, because the memory term is absent at `N=0`.

This blocks the easy circular derivation.

## Gate Results

| Gate | Result |
|---|---|
| source paths exist | pass |
| locked DR1/DR2 split edge-clean | pass |
| zero-memory reproduces `LCDM` | pass |
| fitted amplitude within one percent of locked | pass |
| locked beats fitted-amplitude branch by AIC/BIC | pass |
| factorization `B_mem=q_trace epsilon_H (H_star/H0)^2` | pass |
| `epsilon_H=1` parent-derived | fail |
| `H_star=H0` parent-derived | fail |
| rank-27/rank-2 parent theorem | fail |
| `B_mem=2/27` parent promotion | fail |

## What This Actually Wins

This is not a dead end.

It is a much cleaner map of the door:

```text
old problem:
  why 2/27?

new problem:
  derive q_trace = 2/27,
  derive epsilon_H = 1,
  derive H_star = H0.
```

The best current interpretation is:

```text
q_trace is the channel fraction,
epsilon_H is the Hamiltonian-current normalization,
H_star/H0 is the scale-lock.
```

So the hidden amplitude is no longer vague. It is:

```text
kappa_mem = epsilon_H (H_star/H0)^2.
```

The corrected SN+BAO wrapper says:

```text
kappa_mem ≈ 1
```

to within about one percent across DR1/DR2.

The theory still has to explain why.

## What It Does Not Decide

This checkpoint does not derive:

```text
B_mem = 2/27,
epsilon_H = 1,
H_star = H0,
rank(P_active)=2 from the parent action,
dim(V_cell)=27 from the parent action,
the CMB bridge,
MTS perturbations,
local GR,
PPN silence.
```

It also does not promote the empirical result into:

```text
MTS beats LCDM as a final cosmology claim.
```

The correct private standing is:

```text
the locked 2/27 branch is now empirically well-motivated and algebraically sharp,
but parent ownership still requires a Hamiltonian trace-current theorem.
```

## Next Derivation Target

The next derivation should not refit kappa.

It should attack:

```text
derive_parent_Hamiltonian_trace_current
```

The theorem target is:

```text
the parent action contains a normalized projector trace of the same Hamiltonian constraint that defines rho_c0,
with no independent lambda_mem.
```

If that works:

```text
epsilon_H = 1
```

is no longer closure.

If it fails:

```text
B_mem = 2/27
```

stays exactly where it currently belongs:

```text
a strong empirical closure/theorem target,
not a derived amplitude.
```
