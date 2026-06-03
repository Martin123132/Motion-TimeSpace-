# 264 — Official CMB Likelihood Preflight

## Purpose

This checkpoint tests whether the post-scale-lock CMB route is ready for an **official likelihood comparison**, not whether MTS is supported by CMB.

The rule is strict:

```text
Boltzmann engine smoke < LCDM official baseline reproduction < MTS branch CMB readout
```

If the LCDM official baseline has not been reproduced through real likelihood assets, the MTS CMB branch stays blocked.

## Run

- Runner: `scripts/official_CMB_likelihood_preflight.py`
- Run directory: `runs/20260601-000082-official-CMB-likelihood-preflight`
- Python environment: `.venv-score`
- Fixed lead branch label: `MTS_2over27_no_clock_u3quarter`
- Fixed memory coefficient tracked: `B_mem = 2/27 = 0.07407407407407407`
- Claim ceiling: `official_CMB_preflight_only_no_likelihood_score_no_MTS_CMB_claim`

## Outputs

The run writes:

- `results/source_register.csv`
- `results/engine_inventory.csv`
- `results/official_likelihood_asset_inventory.csv`
- `results/official_likelihood_readiness.csv`
- `results/LCDM_engine_smoke.csv`
- `results/LCDM_engine_smoke_summary.csv`
- `results/LCDM_spectra_sample.csv`
- `results/LCDM_engine_smoke_spectra_sample.csv`
- `results/baseline_reproduction_gate.csv`
- `results/baseline_reproduction_gates.csv`
- `results/next_command_plan.csv`
- `results/command_plan.csv`
- `results/claim_gate_results.csv`
- `results/decision.csv`
- `status.json`
- `DONE.txt`

## Result

### Engine inventory

CAMB is available and passes a tiny LCDM spectra smoke:

- `camb`: available, version `1.6.6`
- `classy`: unavailable
- `CLASS` executable: unavailable
- `cobaya`: unavailable
- `clik`: unavailable
- `candl`: unavailable
- `montepython`: unavailable

The LCDM smoke uses:

```text
H0 = 67.5
ombh2 = 0.02237
omch2 = 0.12
tau = 0.0544
As = 2.1e-9
ns = 0.965
lmax = 64
```

It produces finite CAMB spectra with shape `(111, 4)`.

### Official likelihood readiness

The official likelihood route is **not score-ready**:

- No configured Planck/ACT/SPT likelihood assets were found.
- No `clik`, `candl`, `cobaya`, `montepython`, or CLASS likelihood runner is available.
- LCDM official baseline reproduction was not attempted.
- MTS CMB likelihood scoring is blocked.

### Gate result

| Gate | Status | Meaning |
|---|---:|---|
| Boltzmann engine available | pass | CAMB can generate tiny LCDM spectra |
| Official likelihood assets available | fail | no real Planck/ACT/SPT likelihood assets found |
| LCDM official baseline reproduction | not attempted | required before MTS CMB scoring |
| MTS CMB score allowed | blocked | no CMB support claim allowed |

## Decision

Status:

```text
official_CMB_preflight_CAMB_engine_smoke_passed_official_likelihood_assets_missing_no_CMB_claim
```

Meaning:

CAMB is usable for spectra and controlled proxy/matched-mock work, but the official CMB route is not ready for model-selection claims. Any CMB discussion must remain labelled as engine/proxy/bridge work until a real LCDM official likelihood baseline is reproduced.

## Theory consequence

This checkpoint does **not** damage the theory. It only says the CMB referee has not entered the ring yet.

For the derivation programme:

1. `B_mem = 2/27` remains locked as empirical closure / theorem target, not parent-derived.
2. `Hstar = H0` remains scale-lock closure / boundary theorem target, not parent-derived.
3. The half-memory CMB bridge remains a clue/theorem target, not evidence.
4. No CMB promotion is allowed from proxy spectra.
5. The valid next derivation target is still the missing parent bridge: why the late coherent memory sector should project into the CMB/BAO calibration map without becoming a local fifth force.

## Next step

Two honest routes remain:

### Route A — official route

Install/configure official likelihood assets and reproduce LCDM first.

Required before MTS CMB scoring:

```text
Planck/ACT/SPT likelihood assets + likelihood interface + LCDM reference reproduction
```

### Route B — derivation/proxy route

Continue with labelled proxy work:

```text
post-scale-lock matched-mock refresh
```

This is allowed only as a bridge diagnostic, not a CMB claim.

## Validation

- Script compiles with `.venv-score`.
- Run completed and wrote `DONE.txt`.
- CSV outputs are parseable.
- Source paths in `source_register.csv` exist except intentionally absent CMB likelihood data roots.
- No files outside `post-checkpoint-work` were modified.
- `formalization-workbench` remains unchanged after the protected cutoff.
