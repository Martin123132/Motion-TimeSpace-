# Isolated Likelihood Preflight Wrapper

## 1. Purpose

This file follows:

```text
25-cosmology-preflight-safe-run-or-wrapper.md
```

The question is:

```text
Can the likelihood preflight read the new post-checkpoint parser-smoke output,
instead of relying on the legacy parser-162 status in the main workbench?
```

Short answer:

```text
yes. A post-checkpoint wrapper now reads the new parser output and locks the
likelihood contract without scoring.
```

## 2. Machine Run

Implemented:

```text
scripts/isolated_likelihood_preflight_wrapper.py
```

Successful run:

```text
runs/20260531-000031-isolated-likelihood-preflight-wrapper/status.json
```

Readout:

```text
isolated_likelihood_preflight_locked_no_score_scoring_still_blocked
```

Parser status consumed:

```text
runs/20260530-235530-cosmology-preflight-safe-run/parser-smoke-no-score/status.json
```

## 3. What It Locks

The wrapper writes:

```text
parameter_sources.csv
baseline_parity_contract.csv
nuisance_treatment_contract.csv
information_criteria_rules.csv
output_contract.csv
abort_conditions.csv
wrapper_dependency_report.csv
likelihood_preflight_gate_criteria.csv
```

It imports the locked model list:

```text
LCDM;
wCDM;
CPL;
MTS_C0_minimal_smooth_memory.
```

## 4. Gate Verdict

Passes:

```text
post-checkpoint parser status passed;
models locked;
config has score_allowed=false;
baseline parity locked;
information rules locked;
forbidden score artifacts absent;
first scoring remains blocked by post-checkpoint contract.
```

Still blocked:

```text
fit_allowed_now;
first_scoring_run_allowed_next;
scoring_run_allowed_now;
long_run_allowed_now;
empirical_claim_allowed_now.
```

## 5. Meaning

This is a useful pipeline upgrade:

```text
the growth/CMB preflight chain is now internally post-checkpoint-consistent up
to the no-score likelihood-contract stage.
```

But it is still not evidence:

```text
no chi2, AIC, BIC, growth prediction, CMB score, or comparative verdict was
computed.
```

## 6. Next Target

Create:

```text
27-strict-cosmology-numeric-lock.md
```

Purpose:

```text
lock the actual strict branch numerical choices before any score: b_mem_pre,
F_pre(N), activation sign/range policy, and baseline priors.
```
