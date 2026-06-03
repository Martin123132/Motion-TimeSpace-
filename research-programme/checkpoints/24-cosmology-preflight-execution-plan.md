# Cosmology Preflight Execution Plan

## 1. Purpose

This file follows:

```text
23-strict-cosmology-branch-contract.md
```

The question is:

```text
What exactly can be run next without accidentally starting a scoring run,
mutating the main workbench, or turning a diagnostic into a claim?
```

Short answer:

```text
data-source audit and parser smoke are safe next steps. Likelihood preflight is
conditional because the existing script reads the legacy parser-162 status.
Scoring remains blocked.
```

## 2. Machine Run

Implemented:

```text
scripts/cosmology_preflight_execution_plan.py
```

Successful run:

```text
runs/20260530-235416-cosmology-preflight-execution-plan/status.json
```

Readout:

```text
cosmology_preflight_execution_plan_written_no_commands_executed
```

Commands executed:

```text
false
```

## 3. Safe Commands

Allowed now:

```text
data_source_audit:
audit only; no fit.

parser_smoke_no_score:
parser and covariance-shape check only; --no-score required.
```

Conditional:

```text
likelihood_preflight_no_score:
allowed only as a legacy contract check unless the parser-status dependency is
patched into an isolated post-checkpoint wrapper.
```

Blocked:

```text
first_scoring_run;
cosmology_likelihood_smoke;
full robustness scoring;
any public/private evidence claim above L0_control.
```

## 4. Generated Files

The run wrote:

```text
preflight_source_availability.csv
preflight_command_plan.csv
strict_numeric_lock_needed.csv
preflight_artifact_contract.csv
preflight_gate_criteria.csv
preflight_decision.csv
safe_preflight_commands.ps1
```

The PowerShell file prints commands only. It does not execute them.

## 5. Important Finding

The existing likelihood preflight script is usable as a contract check, but:

```text
growth_CMB_likelihood_preflight.py reads the legacy parser_162 status from the
main workbench.
```

So the next clean move is either:

```text
run only data_source_audit and parser_smoke_no_score now;
or create an isolated post-checkpoint likelihood wrapper before running all
three preflight stages as one chain.
```

## 6. Gate Verdict

Passes:

```text
source 23 complete;
preflight scripts exist;
parser config exists;
score commands blocked;
this stage executed no commands;
legacy dependency flagged.
```

Fails:

```text
empirical claim allowed now.
```

Status:

```text
safe command plan exists;
safe short preflight can be run next;
scoring still blocked.
```

## 7. Next Target

Create:

```text
25-cosmology-preflight-safe-run-or-wrapper.md
```

Purpose:

```text
either execute the two safe no-score steps, or build a post-checkpoint wrapper
so the likelihood preflight reads the new parser-smoke output instead of the
legacy parser-162 status.
```
