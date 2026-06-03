# 106 - Canonical R Cosmology Robustness Summary

## Verdict

`survives_as_competitive_empirical_closure_not_promoted`.

The canonical `R` closure branch went the distance on the SN+BAO background scorecard. It is not a knockout, and it is not yet a field-theory promotion. But it is absolutely still on its feet: the primary full-covariance branch is edge-free, competitive against fitted baselines, and not displaced by the simple shape-ablation tests.

Boxing translation: MTS did not Mike Tyson the card. It fought a Mayweather-style round set - slipped, countered, won some clean parsimony exchanges, took a warning on BAO release sensitivity, and finished as a live contender rather than a corpse.

## Authoritative summary run

`runs/20260531-144900-canonical-R-cosmology-robustness-summary`

Key ledgers:

- `results/decision.csv`
- `results/robustness_gates.csv`
- `results/primary_score_extract.csv`
- `results/instability_register.csv`
- `results/claim_ceiling_register.csv`
- `results/next_theory_gate.csv`
- `results/source_checkpoint_register.csv`

## Round card

| Test | Verdict | Positive read | Warning |
|---|---|---|---|
| T1 primary full-covariance | `T1_clean_points_survival_not_promotion` | Edge-free full-sample DR2 branch; beats `wCDM` narrowly and `CPL` by parsimony | Loses weakly to `LCDM` on BIC; amplitude fitted |
| T2 ablations | `T2_fixed_shape_survives_ablation` | Free `p` and `u3` do not displace the fixed branch by AIC/BIC | `p=3`, `u3=1/4` still need derivation |
| T3 diagonal covariance | `T3_diagonal_preserves_or_strengthens_pattern` | Diagonal covariance preserves or strengthens the pattern | Full covariance remains primary; `B_mem` shifts about 32% |
| T4 small sample | `T4_reproduces_small_sample_instability_but_fixed_pattern_survives` | Fixed branch remains edge-free and qualitatively survives | CPL and fitted-`u3` edge-hit; diagnostic only |
| T5 SH0ES pressure | `T5_SH0ES_pressure_neutral_stress_only` | SH0ES pressure barely changes the matched scorecard | It is neutral stress evidence, not special support |
| T6 BAO release | `T6_DR1_weaker_release_warning_not_reversal` | DR1 preserves the `wCDM` win and `CPL` parsimony round | DR1 weakens the LCDM/AIC round; do not cherry-pick DR2 |

## Primary numerical spine

The full-covariance T1 branch gives the cleanest current scorecard:

| Reference | Delta chi2 | Delta AIC | Delta BIC | Readout |
|---|---:|---:|---:|---|
| `LCDM` | -5.259659 | -3.259659 | +2.140962 | split points win, not BIC promotion |
| `wCDM` | -0.169201 | -0.169201 | -0.169201 | razor-thin equal-parameter points win |
| `CPL` | +0.167536 | -1.832464 | -7.233085 | parsimony points win |
| zero-memory control | -5.259659 | -3.259659 | +2.140962 | nonzero memory signal, not BIC decisive |

This is the fair scientific read: MTS is competitive. It does not need to smash the baselines to remain interesting, because the physics ambition is different. But it cannot claim more than the evidence supports.

## Instability register

The current instabilities are quarantined rather than ignored:

- `CPL` repeatedly hits the `wa=-2` lower prior edge in small-sample/stress branches.
- `MTS_fitted_u3` repeatedly hits the `u3=0.05` lower edge and high `B_mem` edge in small-sample branches.
- The fixed canonical branch is edge-free across the tested T1-T6 branches.
- DR1 weakens the LCDM/AIC round, so BAO-release dependence must stay on the public warning label.

## Claim ceiling

Allowed:

- `canonical_R_closure` is a competitive empirical SN+BAO background closure contender.
- MTS survives this robustness card on points, especially against `wCDM`/`CPL`-style baselines.

Forbidden:

- MTS predicts the cosmological amplitude from first principles.
- The canonical `R` closure is already a unified field theory.
- The cosmology branch proves local GR/PPN recovery.

The exact ceiling is:

`empirical_closure_scorecard_only`.

## Next theory gate

The next work should not be another blind data run. The branch has earned theory work. The priority is:

1. Derive `B_mem` or equivalent `DeltaR` amplitude from the parent action.
2. Derive the canonical `R` normalization and `a_F=1` ruler rather than declaring it.
3. Recover `p=3` and `u3=1/4` from the FLRW memory projection or demote them to explicit closure constants.
4. Prove the same parent structure gives local GR/Newton/PPN silence without a smuggled plateau axiom.

If those gates pass, this becomes much more serious than a curve-fit. If they fail, the honest status is still useful: a disciplined empirical closure branch with a strong enough scorecard to keep studying, but not a derived unified field theory.

## Bottom line

How grim is it? Not grim. Also not crowned.

The fair standing is: MTS has a live cosmology closure branch that survives strict-enough first robustness, wins or holds several important rounds, and carries clear warning labels. The fastest way to improve the work now is to turn the fitted amplitude and normalization into derived quantities while preserving the local GR limit.
