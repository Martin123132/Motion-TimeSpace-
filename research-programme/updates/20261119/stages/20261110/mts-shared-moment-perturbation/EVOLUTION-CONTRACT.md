# Frozen paired forward control

Run cold and canonical-heavy MTS at 32 and 64 momentum nodes, retaining angular cutoff 16, k=5/Mpc, z=10 start and the saved Delta ln(a)=0.001 interval. Use the frozen controlled thermal seed and live D0 preparation from PREPARATION-CONTRACT.md. The latter preserves the seed's physical Newtonian heavy density/current, not necessarily its synchronous coordinates after metric feedback.

Use the previously tested fourth-order commutator-free exponential scheme at 64 and 128 conformal-time steps for each case. Keep all four canonical heavy coordinates. Normalize with the already saved initial-state scales; no fitted damping, state projection or changed tolerances. First run is checkpointed to measure cost, not to select a physical result. Store every step and compare at nine common scale-factor positions. Conformal-time sample alignment between 32/64 grids is performed through the saved background clock, not by equating their different clock spans. Step refinement at identical node count uses exactly common step boundaries.

Acceptance: finite states, deterministic provenance and original-source preservation; maximum normalized state refinement <=2e-5; physical readout comparison across momentum rules <=2e-5 relative to the maximum absolute amplitude over the paired nine-point histories for each readout. Tiny readouts are not divided by unrelated large fields. If a readout is zero throughout, require exact equality. Report absolute differences alongside every relative comparison. No extrapolated accuracy claim follows from one refinement pair.

Independently evaluate Phi'+H Psi-Q/(2k) and the retained constraint/source budget at nine probes with 16/32 derivative stencils. Metric gate remains 2e-5; algebra gate remains 1e-10. Keep a failing physical diagnostic distinct from numerical/provenance validation. Do not claim a uniform-in-time enclosure from samples.

Each process uses one thread, CPU4, below-normal priority; writes unique restart packets at eight-step boundaries and yields at a safe boundary before its 900-second deadline. No worker may resume a failed receipt automatically. Source model, preparation and contract hashes must match on every continuation. A deliberately saved bounded chunk is not a failed-run retry. No simultaneous workers or new native captures.

This is a separate matched-distribution reference. Original production bank/grid/background and tolerance files stay unchanged. It is not primordial evolution, a new cosmology fit or a galaxy occupation prescription.
