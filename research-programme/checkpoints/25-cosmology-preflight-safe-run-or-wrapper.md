# Cosmology Preflight Safe Run

## 1. Purpose

This file follows:

```text
24-cosmology-preflight-execution-plan.md
```

The question is:

```text
Can we run the safe no-score checks now, while keeping scoring and claims
blocked?
```

Short answer:

```text
yes. The data-source audit and parser smoke ran under post-checkpoint output
folders only. No data fit, likelihood score, or claim was produced.
```

## 2. Commands Run

Run root:

```text
runs/20260530-235530-cosmology-preflight-safe-run
```

Executed:

```text
data_source_audit:
growth_CMB_data_source_audit.py

parser_smoke_no_score:
growth_CMB_parser_smoke_dry_run.py --no-score
```

Not executed:

```text
likelihood_preflight_no_score;
first_scoring_run;
cosmology_likelihood_smoke;
full robustness scoring.
```

## 3. Machine Readout

Implemented:

```text
scripts/cosmology_preflight_safe_run_readout.py
```

Successful readout run:

```text
runs/20260530-235656-cosmology-preflight-safe-run-readout/status.json
```

Readout:

```text
cosmology_preflight_safe_run_two_steps_passed_no_score_likelihood_wrapper_needed
```

## 4. Results

Data-source audit:

```text
growth_CMB_data_source_audit_complete_acquisition_needed
```

Meaning:

```text
preferred growth and CMB sources are identified, no fit was run, and the old
workbench chain still wants a source-acquisition manifest before scoring.
```

Parser smoke:

```text
growth_CMB_parser_smoke_dry_run_passed_no_score
```

Parser facts:

```text
inventory rows: 9;
covariance checks: 9;
failed covariance checks: 0;
forbidden artifacts: none.
```

## 5. Gate Verdict

Passes:

```text
source audit did no fit;
parser --no-score flag was required and present;
config has score_allowed=false;
growth branches stayed separate;
all covariance shapes passed;
no forbidden artifacts appeared.
```

Still blocked:

```text
fit_allowed_now;
scoring_run_allowed_now;
long_run_allowed_now;
empirical_claim_allowed_now.
```

## 6. Important Finding

The safe checks are good news for the pipeline, but the chain is not fully
post-checkpoint-isolated yet:

```text
growth_CMB_likelihood_preflight.py still reads the legacy parser_162 status
from formalization-workbench.
```

So we should not run the likelihood preflight as if it consumed this new parser
output until we either patch a wrapper or explicitly label it a legacy contract
check.

## 7. Next Target

Create:

```text
26-isolated-likelihood-preflight-wrapper.md
```

Purpose:

```text
make a post-checkpoint likelihood preflight wrapper that reads this new parser
smoke output, then still stops before any scoring run.
```
