# Calibrated Closure Candidate Ledger

## 1. Purpose

This file follows:

```text
41-calibrated-Hz-covariance-guardrail.md
```

The question is:

```text
After the post-checkpoint CMB calibration route survived several fixed-row
guardrails, what exactly is its honest status?
```

Short answer:

```text
retained as a frozen closure candidate;
not evidence;
not a parent-derived cosmology branch;
not public-claim ready.
```

This is a good result, but it has to stay in the correct box.

## 2. Machine Run

Implemented:

```text
scripts/calibrated_closure_candidate_ledger.py
```

Successful run:

```text
runs/20260531-011514-calibrated-closure-candidate-ledger/status.json
```

Readout:

```text
calibrated_closure_candidate_retained_not_evidence_promotion_gates_locked
```

Generated ledgers:

```text
runs/20260531-011514-calibrated-closure-candidate-ledger/results/source_checkpoint_register.csv
runs/20260531-011514-calibrated-closure-candidate-ledger/results/survived_guardrail_ledger.csv
runs/20260531-011514-calibrated-closure-candidate-ledger/results/missing_promotion_gates.csv
runs/20260531-011514-calibrated-closure-candidate-ledger/results/claim_language_ledger.csv
runs/20260531-011514-calibrated-closure-candidate-ledger/results/promotion_ladder.csv
runs/20260531-011514-calibrated-closure-candidate-ledger/results/decision.csv
```

## 3. Survived Guardrail Ledger

The frozen native CMB-calibrated C0 row has survived:

```text
recombination background memory bound;
compressed CMB distance calibration;
same-parameter growth stress;
late SN/BAO background backreaction;
row-locked H(z) covariance guardrail;
b_mem parent-amplitude corridor plausibility.
```

Key numbers:

```text
fractional memory contribution to H^2 at recombination = 1.6885841317095195e-10
native CMB-calibrated compressed-CMB chi2 = 3.4632081390356074e-10
growth primary delta chi2 vs locked C0 = +0.389648858052432
growth full-shape delta chi2 vs locked C0 = +0.9885129727912112
late SN/BAO total delta chi2 vs locked C0 = +2.9850626488721446
H(z) suggested-covariance delta chi2 vs locked C0 = -0.25942486815474197
H(z) suggested-covariance delta chi2 vs best baseline = +0.005678777990450357
native CMB-calibrated b_mem corridor at eta = 1 gives a_F DeltaR = 0.08125547932083872
```

Interpretation:

```text
the frozen calibrated row does not immediately collapse under the internal
guardrail stack.
```

That is the strongest allowed statement.

## 4. Why It Is Still Not Evidence

Forbidden upgrade:

```text
MTS is supported by CMB;
the calibrated row beats LCDM/wCDM/CPL;
the parent theory derives the cosmology branch;
local GR is solved;
public claim.
```

Reasons:

```text
the compressed CMB distance score was calibrated;
H(z) is reused/semi-fresh rather than a clean independent holdout;
official spectra/lensing likelihood has not been run;
perturbation variables are not locked;
H0, Omega_m0, and b_mem are not derived from parent invariants;
local GR/PPN reduction is still an open promotion gate.
```

Allowed wording:

```text
the frozen CMB-calibrated closure candidate survived internal guardrails.
```

## 5. Missing Promotion Gates

Still missing:

```text
parent H0/Omega_m0/b_mem map;
official CMB spectra/lensing fixed-parameter likelihood;
parent perturbation and early-universe contract;
fresh external growth/RSD holdout;
independent predeclaration and falsification rule;
local GR/PPN reduction.
```

These are not cosmetic gaps. They decide whether this branch becomes physics
or stays a useful closure benchmark.

## 6. Promotion Ladder

Current stage:

```text
stage 0: closure_candidate
status: retained
claim level: internal closure candidate only
```

Next stages:

```text
stage 1: fresh independent holdout;
stage 2: official CMB stress;
stage 3: parent map derivation;
stage 4: theory promotion.
```

The branch cannot skip stages.

## 7. Decision

Decision:

```text
calibrated_closure_candidate_retained_not_evidence
```

Meaning:

```text
worth carrying forward;
not worth claiming;
not dead;
not promoted.
```

This is actually the productive middle: it gives us a real target to sharpen
without pretending the hard parts are solved.

## 8. Validation

Validation passed:

```text
13 source files checked;
6 survived-guardrail rows written;
6 missing-promotion-gate rows written;
6 claim-language rows written;
5 promotion-ladder rows written;
3 decision rows written;
script py_compile passed;
top-level formalization-workbench files unchanged.
```

The latest top-level `formalization-workbench` modification times remain on
2026-05-29, so this checkpoint stayed inside `post-checkpoint-work`.

## 9. Next Target

Create:

```text
43-official-CMB-perturbation-contract.md
```

Purpose:

```text
define exactly what the frozen closure candidate must supply before any
official CMB spectra/lensing stress is meaningful: perturbation variables,
observable mapping, no-new-knob rules, pass/fail thresholds, and what counts
as demotion.
```

This is the next serious step because local guardrails are mostly exhausted.
The next test must either become more official or more independent.
