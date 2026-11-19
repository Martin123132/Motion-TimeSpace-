> Public reading copy. Machine-specific or private operational passages are omitted; original and public SHA-256 values are recorded separately.

# Final-panel continuation: 137 segments independently checked

Date: 2026-11-10. Previous goal turn delivered verified progress; this turn adds source calculations to the same retained third-cell problem. The broad MTS goal remains active and unmet.

## Completed calculation

- Starting coverage: 98 of 158 MTS segments, 1,730 of 2,750 frozen nodes.
- Batches 12--16 completed, adding 39 segments and 663 nodes. Selected ordinal 105 was reused.
- Current coverage: **137/158 segments; 2,393/2,750 nodes; 86.50642769302449% of the cell's dN width**.
- Completed ordinals: 0--135 and 157. Remaining: **136--156, 21 segments / 357 nodes**.
- The campaign ended normally at its safe check-in boundary, 2026-11-10 01:36:28 UTC. Its conservative runtime gate retained time for independent checks and cleanup. It was not a failed or abandoned calculation.
- Original physical bank, source histories, physical grids, units, arithmetic, algebra gate 1e-10 and numerical gate 2e-5 are unchanged. This work refines source integration on the already frozen segment-aligned nodes; it does not alter the physical model.

The first unfinished segment, 96, was independently qualified before production; its 17 nodes were reused within batch 12. All production batches use the original source implementation. Both earlier catalogues are included; no earlier completed interval is silently dropped.

## Heavy-flow component: independent validation

Evidence: `completed-audit/result.json`.

- All completed segments pass all four heavy-flow branch/output comparisons.
- 38,288 high-precision scalar cases checked independently; binary-rounded disagreement is zero.
- Maximum forward-map discrepancy: 1.059272396363778e-15.
- Independent quadrature discrepancy normalized by the absolute term sum: 2.219234912718689e-16.
- Summed diagnostic triangle divided by the original whole-cell source budgets:

| Branch | Pi | delta_massless |
|---|---:|---:|
| GR | 1.743804174415061e-8 | 2.2755972938434962e-8 |
| Poisson-spatial | 1.0871348607319864e-8 | 1.3497468962369955e-8 |

Both saved scalar background flow defects remain explicit. Neither is zeroed or replaced using the background equations of motion. These are checked numerical indicators for computed coverage, not rigorous bounds on the missing 21 segments.

## Full source: baseline and MTS

Evidence: `balanced/all-source-projection-01/result.json`, `heavy-coverage.npz` and `cold-coverage.npz`.

All ten outputs are reconstructed in both branches: Phi, Psi, D, Q, Pi, theta_c, delta_c, delta_b, delta_gamma and delta_massless. The direct integration measure is dN, without an extra phase-grid Jacobian. The physical clock and phase remain in the source.

Maximum diagnostics across the 20 comparisons, divided by their corresponding source budgets:

| Diagnostic | MTS, 137 segments | Baseline, both segments |
|---|---:|---:|
| quadrature | 0.0000026976872636734154 | 0.03854239926015293 |
| budget | 0.000001073517555100301 | 0.16258192921150677 |
| current | 8.002636255271902e-15 | 3.213346506912938e-14 |
| phase | 5.4250955421389464e-8 | 0 |
| cross | 1.889725732795171e-22 | 0 |
| current_and_phase | 5.4250956105917334e-8 | 3.213346506912938e-14 |
| adjoint_interpolation | 7.77367975444137e-11 | 7.208330826962063e-11 |
| adjoint_steps | 5.834526074436618e-14 | 1.4105972591148826e-14 |

**MTS: 20/20 comparisons pass on the completed domain.** The largest diagnostic is 2.6976872636734154e-6, below the unchanged 2e-5 gate. The prior partial result's largest diagnostic was 2.651187109486521e-6; the change is reported, not misrepresented as monotone convergence.

**Baseline: 0/20 strict relative comparisons pass**, as before. Its complete two-segment result is unchanged. These flags are retained; no tolerance is relaxed and no baseline pass is claimed. Its absolute-scale quantities remain tiny:

| Maximum absolute-scale quantity | MTS | Baseline |
|---|---:|---:|
| Absolute signed correction / saved reference | 2.500369543890779e-7 | 1.3590630188878761e-14 |
| Source budget / saved reference | 2.5014366535613855e-7 | 1.858978573401904e-14 |
| Summed diagnostic triangle / saved reference | 1.9271215376182e-14 | 1.2922693724365293e-16 |

The small baseline denominator makes the relative diagnostics sensitive. This is not evidence of a physical failure of GR. The absolute-scale and relative results must remain together in subsequent comparisons; a numerical diagnostic is not an observational fit result.

Independent full-source contractions agree within 1.978978956396609e-15 for MTS and 1.3175335514196428e-15 for baseline. Independent integral discrepancies are 2.2204312867123575e-16 and 2.068734174983479e-16. The all-source projection reuses saved packets; no additional native source or background evolution is computed.

## Provenance, scope and closeout

[Operational or machine-specific passage omitted from public reading copy.]

[Operational or machine-specific passage omitted from public reading copy.]

Their closeout hashes are respectively:
- `6adfd720a0ccb4ccd50683422404ca4e20444e6cbe51683d92554d699e71074d`
- `3768ecafded183a8f0917892b67cefb59470ed2efef53d3d50d4874a874bd9d7`

The preflight verifies both inherited catalogues, their sealed batch records, the original freeze, exact remaining work and unchanged audit/projection mathematics. The earlier import-order repair is already incorporated; no failed numerical attempt occurred in this stage. Expected terminal attempts: 15, all exit 0.

`seal_stage.ps1` verifies scientific input/source hashes, exact worker identities and terminal receipts, then records `closeout.json` and `CLEANUP.json`. Those receipts establish successful sealing and process cleanup. No GitHub action, subagent, compiler or unrelated-process change is involved.

The remaining 21 segments are needed before a full-cell conclusion. See `NEXT.md` for the exact restart and downstream qualification/accumulation sequence.

