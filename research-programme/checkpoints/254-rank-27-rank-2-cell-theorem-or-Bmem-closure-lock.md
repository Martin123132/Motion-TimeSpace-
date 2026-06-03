# 254 - Rank-27 Rank-2 Cell Theorem or Bmem Closure Lock

Private derivation checkpoint. This is not a derivation of `B_mem = 2/27`,
not a cosmology pass, not a CMB pass, and not local-GR promotion.

## 1. Trigger

Checkpoint 253 sharpened the missing amplitude theorem:

```text
B_mem = 2/27 would follow if
dim(V_cell)=27,
rank(P_active)=2,
kappa_mem=1.
```

This checkpoint tries to derive those three ingredients rather than letting a
nice number seduce the work. We like the number. We do not marry the number
without a prenup.

## 2. Machine Artifact

Script:

```text
scripts/rank_27_rank_2_cell_theorem_or_Bmem_closure_lock.py
```

Run:

```text
runs/20260601-000071-rank-27-rank-2-cell-theorem-or-Bmem-closure-lock
```

Command:

```text
python scripts/rank_27_rank_2_cell_theorem_or_Bmem_closure_lock.py --timestamp 20260601-000071
```

Status:

```text
rank_27_rank_2_theorem_not_derived_Bmem_2over27_locked_as_empirical_closure_target_until_cell_rank_and_stress_normalization_owner_exists
```

Claim ceiling:

```text
Bmem_2over27_closure_lock_no_parent_amplitude_derivation
```

## 3. Attempted Derivation

The pieces behave differently:

| piece | status |
|---|---|
| `p=3` | conditional shape route survives |
| `u3=1/4` | conditional 3+1 cell route survives |
| `dim(V_cell)=27` | not derived |
| `rank(P_active)=2` | not derived |
| `kappa_mem=1` | not derived |

The useful distinction is:

```text
three spatial dimensions can explain a cubic shape,
but they do not automatically explain a 27-dimensional cell state space.
```

## 4. No-Go Lemmas

Projector arithmetic alone is too weak:

```text
P^2 = P
```

only says eigenvalues are `0` or `1`. It does not choose the dimension of the
space or the rank of the active subspace.

FLRW scalar symmetry is also too weak:

```text
strict homogeneous isotropic background -> one scalar exchange channel.
```

So rank `2` does not come from scalar FLRW symmetry alone.

Three spatial dimensions help with:

```text
det(Q) -> X^3.
```

They do not by themselves give:

```text
3^3 = 27.
```

To get `27`, the parent theory has to prove a ternary cell state per spatial
leg. To get `2`, it has to prove two active exchange classes without sneaking
in a clock, tensor-sector mismatch, or pair-ruler sidecar.

## 5. Sufficient Theorem Contract

The theorem would be:

```text
V_cell is parent-defined and metric-independent,
dim(V_cell)=27,
P_active^2=P_active,
Tr(P_active)=2,
kappa_mem=1,
same P_D remains locally topological and bulk-stress silent.
```

Then:

```text
B_mem = kappa_mem Tr(P_active)/dim(V_cell) = 2/27.
```

That is a clean theorem target. It is not yet a theorem.

## 6. Closure Lock

After this pass, the correct status is:

```text
B_mem = 2/27 is locked as an empirical closure theorem-target.
```

Meaning:

```text
use it as the disciplined lead branch,
test it hard,
do not claim it is parent-derived.
```

This is not a retreat. It prevents the theory from cheating while preserving
the best sharp target.

## 7. What To Attack Next

The next most valuable derivation is not more rank poetry. It is:

```text
kappa_mem.
```

Reason:

```text
even a perfect rank fraction is just bookkeeping until a stress/exchange law
maps it into H^2/H0^2.
```

So the next target should be the memory stress-exchange normalization. If that
fails, `kappa_mem` is the hidden amplitude and `B_mem` stays fitted.

## 8. Claim Policy

Allowed:

```text
2/27 is a precise theorem target.
```

Allowed:

```text
2/27 is closure-locked for the lead branch.
```

Forbidden:

```text
B_mem = 2/27 is derived,
MTS passes cosmology,
MTS passes CMB,
local GR is derived.
```

Not supported:

```text
the branch is dead.
```

## 9. Decision

Decision:

```text
rank_27_rank_2_theorem_not_derived_Bmem_2over27_locked_as_empirical_closure_target_until_cell_rank_and_stress_normalization_owner_exists
```

Meaning:

```text
p=3 and u3=1/4 still have conditional structural routes. The amplitude number
2/27 is now an honest closure target, not a claimed derivation.
```

Boxing translation:

```text
nice footwork, clean guard, no knockout. Keep the scorecard honest.
```

## 10. Next Target

Next:

```text
255-memory-stress-exchange-normalization-or-kappa-mem-free.md
```

Purpose:

```text
try to derive the sign and normalization of the memory stress/exchange term.
If kappa_mem cannot be fixed, then no rank theorem can promote B_mem from
closure to parent-derived amplitude.
```
