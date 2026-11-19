> Public reading copy. Machine-specific or private operational passages are omitted; original and public SHA-256 values are recorded separately.

# Full-cell flow continuation: verified covered-domain result

Date: 2026-11-09. Local continuation of the frozen third-cell calculation; no physical model, source history, scattering bank, physical grid or tolerance was changed.

## Result and coverage

- The inherited stage had 43 of 158 MTS background segments and 795 frozen source nodes.
- Batches 05 through 11 completed normally, adding 55 segments and 935 nodes.
- Independently verified total: **98 of 158 segments, 1,730 of 2,750 nodes**, covering **61.66060630574721% of the cell's dN width**.
- Completed ordinals are 0 through 95, plus 105 and 157. Ordinal 52 was already inherited and was reused, not recalculated.
- Remaining: ordinals 96 through 104 and 106 through 156, or **60 segments / 1,020 nodes**.
- The campaign stopped at its safe check-in boundary at 22:45:44 UTC. No further native batch was started.
- The subsequent independent audit finished normally at 22:48:01 UTC. Following the reported app crash, its start/end receipts, output and process identity were checked before continuing; it was not relaunched.

## What was actually calculated

The saved physical source and its controls were evaluated on the parent's already frozen, segment-aligned quadrature nodes. The heavy-field flow defect was retained explicitly, including both scalar background equation defects. It was neither zeroed nor replaced by an on-shell value.

The completed catalogue is the union of parent batches 00--04, current batches 05--11 and the previously saved selected panels. The independent audit checks catalogue coverage and duplicate segments. Both source branches and all ten outputs are then reconstructed from the saved packets using the original adjoints.

The integration measure is dN. No extra phase-grid Jacobian is introduced into this direct dN integral. The physical clock and phase history remain in the source.

No physical background evolution was rerun and the all-source projection made no new native source calls.

## Independent heavy-flow checks

Evidence: `completed-audit/result.json` and its hashed packets.

- 27,680 independently evaluated high-precision scalar cases; binary-rounded arithmetic disagreement: 0.
- Maximum forward-map discrepancy: 1.059272396363778e-15.
- Independent quadrature discrepancy, normalized by absolute term sum: 2.219234912718689e-16.
- Every completed segment passes all four recorded heavy-flow branch/output comparisons.
- Summed triangle indicators divided by the original whole-cell source budgets:

| Branch | Pi | delta_massless |
|---|---:|---:|
| GR | 1.2951503031087459e-8 | 1.6959507035514972e-8 |
| Poisson-spatial | 8.074463044518533e-9 | 1.0059501006178166e-8 |

These are numerical indicators on the completed coverage, not bounds on the still uncomputed segments.

## Full saved source, not just its flow component

Evidence: `balanced/all-source-projection-01/result.json`, `heavy-coverage.npz` and `cold-coverage.npz`.

Ten outputs are checked in each of the GR and Poisson-spatial branches: Phi, Psi, D, Q, Pi, theta_c, delta_c, delta_b, delta_gamma and delta_massless.

The unchanged numerical gate is 2e-5; the independent algebra gate is 1e-10. The diagnostics below are maxima across the 20 comparisons, normalized by each corresponding covered-domain source budget.

| Diagnostic | MTS, 98 segments | Baseline, both segments |
|---|---:|---:|
| Signed quadrature change | 2.651187109486521e-6 | 3.854239926015293e-2 |
| Budget quadrature change | 1.496043133606086e-6 | 1.6258192921150677e-1 |
| Current control | 7.49139516805498e-15 | 3.213346506912938e-14 |
| Phase control | 1.5100592617634448e-8 | 0 |
| Cross control | 2.4130861552355236e-23 | 0 |
| Combined current/phase control | 1.5100591885685836e-8 | 3.213346506912938e-14 |
| Adjoint interpolation control | 8.672266474507579e-11 | 7.208330826962063e-11 |
| Adjoint step control | 5.480352656689647e-14 | 1.4105972591148826e-14 |

**MTS: 20/20 numerical comparisons pass on the completed domain.** Its largest diagnostic increased from 1.8040459342785281e-6 in the previous partial domain to 2.651187109486521e-6; this remains below the unchanged gate. This is not a monotone-convergence claim and does not qualify the uncomputed remainder.

**Baseline: 0/20 pass the same strict relative tests.** These flags are preserved, not waived. Its maximum absolute signed correction divided by the saved reference scale is only 1.3590630188878761e-14, and its maximum summed diagnostic indicator divided by that scale is 1.2922693724365293e-16. A small denominator makes the relative result sensitive; these numbers do not by themselves establish a physical failure of the baseline or justify changing the tolerance.

For comparison, the MTS maximum absolute signed correction/reference is 1.7655769787635005e-7; its maximum budget/reference is 1.7661595251768032e-7; its maximum summed diagnostic indicator/reference is 1.4254751345236432e-14. These are correction/error-budget quantities for this saved calculation, not observational fit improvements.

The independent full-source contraction discrepancies are 1.978978956396609e-15 (MTS) and 1.3175335514196428e-15 (baseline). Independent integral discrepancies are 2.2204312867123575e-16 and 2.068734174983479e-16, respectively.

## Provenance and startup repair

[Operational or machine-specific passage omitted from public reading copy.]

Its closeout SHA-256 is `6adfd720a0ccb4ccd50683422404ca4e20444e6cbe51683d92554d699e71074d`.

The first probe attempt failed before physics evaluation because the wrapper imported the inherited helper before establishing its module path. Its original script, error log and exit-1 receipt are retained. The diagnosed repair uses `run_probe_v2.py` and the version-2 production wrappers; it changes import order only. See `IMPORT-REPAIR.md`.

There are 20 recorded stage attempts: 19 exit 0, and that one explicitly diagnosed startup failure. An unsuccessful startup is not counted as a successful scientific calculation.

## Closeout and next work

`seal_stage.ps1` verifies recorded source/input hashes, exact worker identities and terminal states, and records the manifest and cleanup in `closeout.json` and `CLEANUP.json`. Those receipts, rather than this prose, establish whether sealing completed.

The next continuation must reuse both completed stage catalogues, start at ordinal 96 / batch 12, and preserve the original frozen node selection. See `NEXT.md`.

Full-cell qualification and accumulation remain pending until the remaining segments and controls are checked. Once qualified, add the new third-cell result to the saved **two-cell** accumulation, not to an already three-cell total. Local work only; no GitHub action.

