# Paired matched-distribution perturbations completed

Date: 2026-11-10. Private extension of the retained parent, not a replacement action or an observational fit.

## What changed scientifically

The previously identified thermal-neutrino inconsistency is now removed at the operator level. Background and perturbation stresses use the same positive distribution. The resulting discrete energy and momentum equations are derived in DERIVATION.md and tested coefficient by coefficient, including live metric feedback, for both the cold comparison and the canonical MTS heavy field. This is an actual source construction and coupled evolution, not another missing-input ledger.

The actual canonical scalar is retained with all four real coordinates. Its own sources determine the metric and the remaining species respond. The reference has 550/1094 cold states and 554/1098 canonical-heavy states for 32/64 momentum nodes; angular cutoff remains 16.

## Verified results

- Original native five-node reconstruction: all tested full matrix rows agree to <=4.434e-16; source rows <=5.342e-16. Original canonical matrix agrees to <=5.861e-16. This was checked before new-grid evolution.
- Twelve arbitrary-state operator checks (two models, two rules, three background points): neutrino energy row error <=4.476e-16 and momentum row error <=2.160e-16. The independent background density-plus-pressure is used, not merely asserted to equal the perturbation sum.
- Four controlled initial preparations pass. The canonical live-D0 solve has condition number about 1.0004094, normalized constraint error <=1.351e-16 and derivative-stencil change <=2.627e-26. These are conditional preparations, not unique cosmological or galactic population predictions.
- Eight complete paired evolutions: cold/MTS x 32/64 momentum rules x 64/128 time steps. All 96 eight-step restart packets are contiguous and hash-linked. Maximum normalized state refinement is 2.832e-13 over common saved time boundaries; common-scale-factor refinement <=2.516e-13. At this simple probe these are small refinement differences, not certified absolute errors.
- Independently differentiated metric residual E_Phi=Phi'+H Psi-Q/(2k): maximum normalized error 2.433e-10 across nine common-scale-factor probes and two derivative stencils. All cases pass the unchanged 2e-5 gate. Maximum Hamiltonian constraint error 1.759e-15; source/metric budget identity error 2.821e-16. Finite probes do not establish a uniform enclosure.
- Canonical heavy energy/current normalized residuals <=2.186e-11 / 4.706e-9; background differential residual <=1.080e-11 on these probes.

## Numerical comparisons in physical readouts

| Comparison | Cold | Canonical MTS |
|---|---:|---:|
| 32/64 momentum rule: largest relative source-readout difference | 5.355e-8 | 5.352e-8 |
| 32/64 momentum rule: metric potentials | <=4.713e-10 | <=4.713e-10 |
| 64/128 time steps: largest relative physical-readout difference | <=5.205e-15 | <=1.786e-9 |

Each relative readout comparison uses that readout's maximum absolute amplitude across the paired nine-point history, not a pointwise division through zero or normalization by a larger unrelated field. Absolute differences and denominators remain in validation.json and source-stability-result.json. The time-step-sensitive MTS readout is heavy pressure, with absolute change <=4.917e-29 Mpc^-2; its direct check prevents a state norm from hiding cancellation error. All pass 2e-5.

389 implementation, provenance, refinement and cleanup checks pass, plus 26 physical-source time-refinement checks. These counts are verification bookkeeping, not hundreds of independent physical discoveries.

## What the result does and does not compare

The same controlled thermal dilation prescription, Theta=1e-6, is applied to both backgrounds and both rules. No five-to-64-node initial history interpolation is used. This is a late initial-value control at z=10 over Delta ln(a)=0.001 and k=5/Mpc, not a replay of the saved primordial history. In particular, the small metric error here cannot be divided into the previous history's error and advertised as a like-for-like improvement factor: the prepared perturbation states differ. The eliminated enthalpy mismatch is supported by the operator derivation independently of that numerical comparison.

Retained thermal inputs remain approximate: their fresh initialization differs from captured native opacity/sound-speed context by up to 1.418e-6 in cold and 3.685e-7 in heavy; the 33-node interpolation itself agrees with independent interleaved values to <=7.46e-14. Original 2e-5 gates remain unchanged. Angular cutoff, leading late radiation approximation, W2 carrier and late heavy-background approximation are inherited; no accuracy claim is made outside their regime. The historical full-span archival discrepancy remains separate.

Original parent action, G, production bank, grids, masses, thermal normalization, earlier checkpoints and Galaxy files were not changed. No parameters were fitted and no observational improvement is claimed. Galaxy07 remains an attributed independent update: five partial measured radial profiles are useful baryonic inputs, not complete 3D geometry or a parent-derived occupation prescription.

## Reproduce and continue

All work is in this folder. run_forward.py records exact source/model hashes and eight-step restarts. evaluate_forward.py reuses those packets, advancing only the final short substep to common scale-factor probes; it never interpolates fast canonical states. check_source_stability.py reuses those aligned states. Existing exclusive receipts prevent accidental overwrite or automatic failed-run retry. Read NEXT.md before launching any new calculation.

closeout.json seals the stage after validation. CLEANUP-VERIFIED.json verifies inherited/artifact hashes and exact worker exits. No GitHub action, relay, timer, additional application, server, browser, subagent or unrelated-process intervention occurred. No task-owned numerical job is left running at handoff.
