# 263 - Post-Scale-Lock CMB Bridge Readiness Gate

Private CMB/readiness checkpoint. This is not a public CMB claim, not an
official likelihood run, and not a parent-action promotion.

The scale-lock route is now closure-locked, so this checkpoint re-judges the
CMB bridge under the stricter policy:

```text
B_mem = 2/27 is fixed closure,
H_star = H0 is closure,
half-memory H0 bridge is a theorem target,
not a derived parent result.
```

## 1. Trigger

Checkpoint 262 ended the repeated scale-lock loop:

```text
H_star = H0 is not parent-derived.
```

So the next useful question is:

```text
does the CMB route remain worth disciplined testing,
once all scale/amplitude claims are kept at closure level?
```

## 2. Machine Artifact

Script:

```text
scripts/post_scale_lock_CMB_bridge_readiness_gate.py
```

Run:

```text
runs/20260601-000081-post-scale-lock-CMB-bridge-readiness-gate
```

Command:

```text
python scripts/post_scale_lock_CMB_bridge_readiness_gate.py --timestamp 20260601-000081
```

Status:

```text
post_scale_lock_CMB_bridge_ready_for_matched_mock_or_official_preflight_no_CMB_claim
```

Claim ceiling:

```text
CMB_bridge_readiness_only_no_official_likelihood_or_parent_promotion
```

## 3. Post-Scale-Lock Policy

Current policy:

```text
B_mem amplitude:
  fixed closure theorem-target only.

H_star scale-lock:
  closure-locked, not parent-derived.

half-memory H0 bridge:
  numeric theorem target.

same-density CMB branch:
  promising mock-likelihood proxy only.

locked-Omega_m CMB branch:
  pressure branch.
```

This prevents the CMB route from quietly borrowing the scale-lock as if it had
been derived.

## 4. Imported CMB Evidence

The checkpoint imports the earlier mock scorecard:

```text
same physical densities, TT+EE:
  chi2_proxy = 0.005343819550079403
  verdict = competitive proxy

locked Omega_m, TT+EE:
  chi2_proxy = 81.73575719923768
  verdict = fails proxy badly
```

So the CMB split remains:

```text
same-density profiled branch:
  worth stricter CMB testing.

locked-Omega_m branch:
  not ready for CMB claim; derive compensation or demote.
```

## 5. Half-Memory Bridge

The checkpoint preserves the key clue from 193:

```text
H_CMB = H_late exp(-B_mem/2)
```

is the best current bridge candidate.

It nearly matches the internal late/CMB H0 split and infers back a `B` very
close to the locked value.

But:

```text
the factor 1/2,
the endpoint clock map,
the local silence mechanism,
and B_mem itself
```

are not parent-derived enough for promotion.

So this bridge is:

```text
serious theorem target,
not evidence.
```

## 6. Claim Gates

Gate readout:

```text
endpoint rule exists:
  partial pass.

half-memory numeric match:
  pass as clue.

same-density mock competitive:
  pass as proxy.

locked-Omega_m mock competitive:
  fail.

official likelihood:
  not run.

parent clock map derived:
  fail.
```

Therefore:

```text
no CMB support claim is allowed.
```

## 7. Official Likelihood Readiness

Before any serious CMB score is read, the pipeline must satisfy:

```text
LCDM baseline reproduction,
same data/covariance rules,
official Planck/ACT/SPT likelihood or explicitly labelled matched proxy,
parent/effective perturbation contract,
claim gate that forbids theta/H0 profiling as theory evidence.
```

The current status is:

```text
readiness only.
```

## 8. Next Test Matrix

Ranked next tests:

```text
1. matched_mock_likelihood_refresh
   rerun same-density branch under post-scale-lock policy.

2. official_likelihood_preflight
   check CAMB/CLASS/Cobaya/Planck-lite availability and LCDM baseline.

3. half_memory_clock_map_derivation
   derive or reject H_obs = H_parent exp(-DeltaC/2).

4. BAO_rd_bridge_crosscheck
   ensure the CMB endpoint rule does not break BAO drag-ruler treatment.
```

Best immediate move:

```text
matched mock refresh or official likelihood preflight,
but with claim gates written first.
```

## 9. Decision

Decision:

```text
post_scale_lock_CMB_bridge_ready_for_matched_mock_or_official_preflight_no_CMB_claim
```

Meaning:

```text
the CMB route remains alive, but only as disciplined readiness/proxy testing.
```

Allowed:

```text
same-density CMB branch deserves stricter testing.
half-memory bridge is a serious theorem target.
```

Forbidden:

```text
MTS passes CMB,
official likelihood support exists,
H0 bridge is parent-derived,
B_mem=2/27 is parent-owned.
```

## 10. Next Target

Create either:

```text
264-post-scale-lock-CMB-matched-mock-refresh.md
```

or:

```text
264-official-CMB-likelihood-preflight.md
```

My recommendation:

```text
do official-likelihood preflight first if the environment has the tools;
otherwise do a matched mock refresh with very explicit proxy labels.
```

Reason:

```text
the CMB route is promising enough to keep testing,
but dangerous enough that every score needs a claim gate attached.
```
