# 255 - Memory Stress Exchange Normalization or Kappa Mem Free

Private derivation checkpoint. This is not a derivation of `B_mem = 2/27`,
not a cosmology support claim, not a CMB pass, and not a local-GR claim.

## 1. Trigger

Checkpoint 254 locked:

```text
B_mem = 2/27
```

as a strict empirical closure theorem-target, because the rank-27/rank-2
theorem was not derived.

This checkpoint attacks the deeper problem:

```text
even if the rank fraction is 2/27, why should the stress normalization be 1?
```

Call the missing factor:

```text
kappa_mem.
```

## 2. Machine Artifact

Script:

```text
scripts/memory_stress_exchange_normalization_or_kappa_mem_free.py
```

Run:

```text
runs/20260601-000072-memory-stress-exchange-normalization-or-kappa-mem-free
```

Command:

```text
python scripts/memory_stress_exchange_normalization_or_kappa_mem_free.py --timestamp 20260601-000072
```

Status:

```text
kappa_mem_not_fixed_by_Bianchi_or_topology_Bmem_2over27_requires_separate_stress_normalization_theorem_closure_only
```

Claim ceiling:

```text
kappa_mem_free_until_parent_stress_exchange_normalization_derived
```

## 3. Exact Normalization Split

The honest split is:

```text
q_rank = Tr(P_active)/dim(V_cell) = 2/27
```

and:

```text
Omega_mem(N) = kappa_mem q_rank F(N).
```

Therefore:

```text
B_mem = kappa_mem q_rank.
```

The strict lead branch sets:

```text
kappa_mem = 1.
```

But that is a closure choice unless a parent stress theorem fixes it.

## 4. Bianchi Test

For `N = ln(a0/a)`, a conserved effective memory fluid obeys:

```text
rho_mem' = 3(rho_mem + p_mem).
```

So:

```text
p_mem = -rho_mem + rho_mem'/3.
```

This is useful. It means any supplied `rho_mem(N)` can be made into a
conserved effective stress component with the right pressure.

But the amplitude cancels from the equation of state. Bianchi conservation
does not choose `kappa_mem`.

## 5. Topology Test

The same topological property that protects local N5 says:

```text
delta_g P_D = 0.
```

That is excellent for local bulk-stress silence.

But a purely topological, metric-independent term has no bulk metric variation.
So topology can select a channel, but it cannot by itself produce the FLRW
stress amplitude.

To affect `H^2`, the memory sector needs a metric stress response. That brings
in a normalization/coupling unless the parent action fixes it.

## 6. Verdict

The derivation attempt fails in a useful way:

```text
kappa_mem is not fixed by Bianchi,
kappa_mem is not fixed by topology,
kappa_mem is not fixed by the rank fraction.
```

So:

```text
B_mem = 2/27
```

remains the strict lead closure branch, not a parent prediction.

The ablation branch is:

```text
B_mem = kappa_mem (2/27).
```

That can be tested, but it must be penalized as an extra amplitude.

## 7. What Improved

This checkpoint prevents a subtle cheat:

```text
rank fraction = amplitude.
```

No. The rank fraction can be the channel count. The stress-exchange action must
still explain why the channel count is normalized directly into `H^2/H0^2`.

The theory has a sharper contract now:

```text
derive a unit-normalized exchange current with integral S_unit dN = 1,
or keep kappa_mem free/closure.
```

## 8. Claim Policy

Allowed:

```text
fixed 2/27 is the strict lead closure branch.
```

Allowed:

```text
kappa-free branch can be tested as an ablation.
```

Forbidden:

```text
Bianchi derives kappa_mem,
topology derives B_mem,
MTS derives the cosmology amplitude.
```

## 9. Decision

Decision:

```text
kappa_mem_not_fixed_by_Bianchi_or_topology_Bmem_2over27_requires_separate_stress_normalization_theorem_closure_only
```

Meaning:

```text
the bridge did not collapse, but the toll booth is still there: kappa_mem.
```

Boxing translation:

```text
the jab is legal, but the judges will penalize the extra hand if we use kappa.
```

## 10. Next Target

Next:

```text
256-fixed-2over27-vs-kappa-free-cosmology-test-manifest.md
```

Purpose:

```text
prepare the fair testing manifest: fixed 2/27 strict branch, kappa-free
ablation branch, and standard baselines, all under the same data splits and
same AIC/BIC discipline.
```
