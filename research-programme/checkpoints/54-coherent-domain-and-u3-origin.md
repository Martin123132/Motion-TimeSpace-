# Coherent Domain And u3 Origin

## 1. Purpose

This file follows:

```text
53-coherent-projection-local-silence-gate.md
```

The previous checkpoint retained:

```text
P_coh[Theta]^i_j = (1/3)<theta>_D delta^i_j
<theta>_D = d ln V_D/dtau
```

but left two rescue-knob risks:

```text
the domain D;
the transition scale u_3.
```

This checkpoint asks:

```text
Can D and u_3 be made structural rather than chosen to save the model?
```

Short answer:

```text
D has a plausible non-arbitrary contract as a maximal coherent volume-flow
domain. u_3 has a surprisingly close structural candidate, u_3 = 1/4, but this
is not yet a derivation.
```

This is a “hold on, that is interesting” result, not a victory parade.

## 2. Machine Run

Implemented:

```text
scripts/coherent_domain_and_u3_origin.py
```

Successful run:

```text
runs/20260531-103455-coherent-domain-and-u3-origin/status.json
```

Readout:

```text
domain_contract_partial_u3_quarter_candidate_not_derived
```

Generated:

```text
runs/20260531-103455-coherent-domain-and-u3-origin/results/source_checkpoint_register.csv
runs/20260531-103455-coherent-domain-and-u3-origin/results/domain_candidate_ledger.csv
runs/20260531-103455-coherent-domain-and-u3-origin/results/u3_candidate_ledger.csv
runs/20260531-103455-coherent-domain-and-u3-origin/results/u3_quarter_shape_comparison.csv
runs/20260531-103455-coherent-domain-and-u3-origin/results/origin_route_ledger.csv
runs/20260531-103455-coherent-domain-and-u3-origin/results/gate_results.csv
runs/20260531-103455-coherent-domain-and-u3-origin/results/decision.csv
```

## 3. Best Domain Candidate

The retained domain rule is:

```text
D = maximal coherent volume-flow domain.
```

Meaning:

```text
D is the largest connected domain over which <theta>_D has one coherent sign
and stable averaging.
```

This gives:

```text
FLRW: the homogeneous slice or causal patch is coherent, so <theta>_D = 3H.
Local bound systems: stable physical volume gives <theta>_D approximately 0.
```

So the rule is not:

```text
choose a smoothing scale that dodges local tests.
```

It is:

```text
coherent volume growth sources this scalar memory channel; volume-stable bound
domains do not.
```

That is a reasonable contract. The missing theorem is the parent boundary rule.

## 4. Rejected Domain Routes

Rejected or insufficient:

```text
fixed smoothing scale domain       rejected rescue knob
no-domain pointwise projection     unsafe for local dynamics
causal horizon domain              too broad for local silence by itself
```

Still plausible:

```text
turnaround or virial boundary domain
```

but only if the parent theory can define the bound/unbound split without
importing Newtonian or GR assumptions as the hidden engine.

## 5. u3 Candidate

The current fitted/closure value is:

```text
u_3 = 0.2429466120286312
N50 = 0.21500703361675252
```

The new structural candidate is:

```text
u_3 = 1/4 = 0.25.
```

Interpretation:

```text
one over a 3+1 coherent spacetime-cell count.
```

Numerically:

```text
frac_delta_u3_quarter_vs_fit = 0.029032666528963875
N50_quarter = 0.22124926112512944
frac_delta_N50_quarter_vs_fit = 0.029032666528963927
max_abs_delta_F_quarter_vs_fit_on_sample = 0.029343125585349572
```

That is close enough to deserve a fixed-row smoke test.

But it is not a derivation. Right now:

```text
u_3 = 1/4
```

is a structural candidate, not a theorem.

## 6. Rejected u3 Routes

The simple alternatives are worse:

```text
u_3 = 1/3       spatial-cell third; poor match
u_3 = 1/6       six-face cell; poor match
u_3 = 1/8       half-spacetime-cell; poor match
fitted u_3      works but is not derivation
```

So the quarter route is currently the only interesting non-fitted scale
candidate in this narrow search.

## 7. Gate Verdict

Gate result:

```text
domain_rule_nonarbitrary          pass_partial
domain_rule_parent_derived        fail
u3_quarter_near_lock_identified   pass_partial
u3_parent_derived                 fail
u3_quarter_empirically_checked    open
local_silence_preserved           pass_conditional
support_claim_allowed             fail
```

The branch now has a sharper discipline:

```text
do not keep fitted u_3 forever if u_3 = 1/4 can survive;
do not claim u_3 = 1/4 unless the fixed-quarter branch survives the same tests.
```

## 8. Decision

Decision:

```text
coherent_domain_u3_status = partial_contract_with_quarter_candidate_not_derivation
```

Meaning:

```text
D is now a coherent-volume-flow contract, not arbitrary smoothing;
u_3 has a near structural candidate at 1/4;
the quarter candidate must be tested without refitting;
no parent derivation or empirical support claim is allowed yet.
```

This is exactly where testing becomes useful again. We now have a concrete
less-free branch:

```text
keep p = 3;
keep the coherent-volume interpretation;
replace fitted u_3 with u_3 = 1/4;
compare against the fitted C2 branch.
```

## 9. Next Target

Create:

```text
55-u3-quarter-lock-smoke.md
```

Purpose:

```text
freeze u_3 = 1/4 and run a short no-refit smoke comparison against the current
C2 fitted-u_3 branch.
```

Pass condition:

```text
the fixed-quarter branch does not materially damage the late-background,
growth, CMB-distance, and H(z) guardrails relative to fitted C2.
```

Fail condition:

```text
u_3 = 1/4 significantly worsens the internal guardrails, meaning the quarter
route remains a cute numerology candidate rather than a viable lock.
```
