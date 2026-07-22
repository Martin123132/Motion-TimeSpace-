# 5176 - Predeclared paired high-mode seed ensemble

Marker: MTS_5176_PREDECLARED_PAIRED_HIGH_MODE_SEED_ENSEMBLE.

Date: 2026-07-21.

## Decision discipline

Checkpoint 5175 showed a resolved MTS/CDM difference in one newly resolved
high-mode realization. This checkpoint freezes the required ensemble before
looking at another realization. The already observed seed 517500409 is a
pilot and is excluded from confirmatory statistics.

The protocol hash is 64529978cc452b302a5f09f52fff4be7af2ae8ef5cd64f29a8352005925fb7e7. It locks all checkpoint
5175 physics, grids, spectra, low modes, source history, score, numerical
envelopes and stopping rules. Each invocation runs only the next scheduled
seed, so a completed seed remains below the four-hour cap and interrupted
work can resume from phase caches.

## Frozen seed schedule

- 01 -> 3240854344
- 02 -> 2557716234
- 03 -> 2077240922
- 04 -> 3997337815
- 05 -> 1601888544
- 06 -> 1077884374
- 07 -> 3363819115
- 08 -> 3861952803
- 09 -> 2049864674
- 10 -> 2453975482
- 11 -> 2202452999
- 12 -> 1993157507

No seed may be skipped, replaced, reordered or selected after inspecting an
outcome. The six-seed point is descriptive only. Model preference is assessed
once, after all 12 confirmatory seeds.

## Locked estimands and rule

D_q=d_q(MTS)-d_q(CDM) and D_R=RMSE(MTS)-RMSE(CDM). Positive values favor CDM;
negative values favor MTS. A seed is a joint win only if both advantages
exceed their inherited numerical envelopes in the same direction.

At the final seed, both paired means and deterministic 95 percent bootstrap
intervals must have the same nonzero sign, both exact two-sided sign-flip
tests must pass p<=0.05, and the joint-win sign test must pass the same
threshold. Otherwise the result is a statistical draw or metric split. This
rule treats MTS and CDM symmetrically and does not require either theory to
win by a large information-criterion margin.

## Current execution state

Completed confirmatory seeds: 1 of
12.

- q-band-distance statistic: mean=0.0, median=0.0, bootstrap95=[None,None], exact sign-flip p=None
- RMSE statistic: mean=-0.0053882279920328124, median=-0.0053882279920328124, bootstrap95=[None,None], exact sign-flip p=None
- joint outcomes: CDM 0, MTS
  0, tie/split 1
- current verdict: INCOMPLETE_PREDECLARED_ENSEMBLE_NO_PREFERENCE_ALLOWED
- route decision: LOCKED_CONFIRMATORY_ENSEMBLE_IN_PROGRESS_1_OF_12_PILOT_EXCLUDED_NO_MODEL_PREFERENCE_ALLOWED

Until all twelve seeds complete, no model-preference statement is allowed.
Even a final preference would apply only to this locked UGC09133 formation
gate, not to the full theory.

All 12 current validations pass. Every row remains nonclaim,
the protected formalization-workbench digest remains
b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758, and no GitHub action was
performed by checkpoint 5176.
