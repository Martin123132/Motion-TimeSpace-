# 5267 — Topology-aware soft-energy component runner

## Question

Checkpoint 5266 falsified energy integration outside a finite inner-contour quadrature: its narrow pole ladder changed violently with inner order. The required replacement is to resolve the exact material components, their causal topology, and their energy poles before applying any finite soft-energy quadrature.

## Exact measure

The parent generator uses

`x = u_E`, `c_s = 2u_s - 1`, `c_d = 2u_d - 1`,

so

`du_E du_s du_d = dx (dc_s/2)(dc_d/2)`.

The soft-energy Jacobian is exactly `1`; the angular Jacobian `1/4` remains pending until the two angular outer integrals are restored.

## Topology construction

The physical branch object is the unordered reciprocal projective pair `{z_rep,z_rec}`, not either chart label alone. Continuation uses the pair-set chordal bottleneck on `CP1`. A local homotopy mesh is refined until every pair-set step is at most `0.05` and every reciprocal product residual is at most `2e-08`. Winding integers must agree at consecutive base resolutions, with accepted base resolution at least `4096`.

This repairs the low-energy MC03/MC07 chart exchange without changing the physical branch. Across the accepted E040 interval map, the maximum pair-set step is `0.0249929504335` and the maximum reciprocal residual is `2.83003589551e-12`.

## Exact energy pole

Both regulators contain one active geometric pole, owned by `MC04` (`direct:g1:minus/direct:g3:plus`):

| Regulator | center | pole | residue | slopes | numerator residual |
|---|---:|---:|---:|---:|---:|
| E040 | 0.834525421842 | 0.834525446509 + 9.54081048289e-05 i | -893.013203256 + 17.8799676656 i | -0.981919171, -1.01841813 | 2.18112e-09 |
| E020 | 0.834525736621 | 0.834525742788 + 4.77047112324e-05 i | -893.115006856 + 8.94015979653 i | -0.982082141, -1.01825237 | 2.18196e-09 |

Both two-sided fits pass the `-1` Laurent-slope and numerator-polynomial gates.

## Energy-first integral

The logarithmic pole term is removed analytically before numerical quadrature. Smooth topology intervals are panelized to maximum width `0.025` rather than weakening the low-order gate.

For the regulator combination `2 E020 - E040`, including the inherited kernel and A00 factors but not the pending angular Jacobian, the 512-node reference is

`I_E = -36.8618887518162 -12.5530499811092 i`.

The subtracted relative errors are:

| Composite Gauss order | relative error |
|---:|---:|
| 32 | 0.00216509186388 |
| 128 | 3.19519009683e-06 |
| 512 | 0 |

The raw 32-node error is `0.333216480816`, so the accepted convergence is specifically produced by topology-aware component subtraction.

## Decision

`ACCEPT_FIXED_ANGLE_ENERGY_FIRST_RULE__RETURN_TO_ANGULAR_OUTER_INTEGRATION`

Validation passed: `true`.

This accepts an order-independent, fixed-angle soft-energy rule. It does **not** yet accept a full phase-space coefficient, numeric UV fixed point, local-GR limit, or full MTS theory.

## Next derivation

Restore the two angular outer integrations while retaining this ordering:

1. resolve angular topology chambers;
2. transport the already-subtracted energy component rule within each chamber;
3. apply the exact angular Jacobian `1/4`;
4. bound `x<10^-4` and `1-x<10^-4` endpoint caps;
5. test angular and regulator convergence before interpreting a coefficient.

## Artifacts

- Runner: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_5267_topology_aware_soft_energy_component_runner.py`
- Combined result: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5267\energy_first_two_regulator_result.json`
- Combined convergence: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5267\energy_first_two_regulator_convergence.csv`
- E040 worker: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5267\workers\E040\regulator_result.json`
- E020 worker: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5267\workers\E020\regulator_result.json`
- Validation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5267\energy_first_validation.csv`
