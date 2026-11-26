> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# What cancels the heavy wave's work at the switch?

25 November 2026 · 89.148503803–89.6 conformal Mpc · same native and matched histories, one-cycle filter, 77-bin gravity inputs, photon launch and comparison bands. **Averaging the heavy field alone does not predict the signed photon discrepancy. The opposing term in the local work budget is the rest of the metric constraint, not a change in the supplied U.** This is a conditional comparison of two representations on the saved history, not a new fit or a change to a restart.

| Quarter-cell calculation | Coarse gravity | Fine gravity |
|---|---:|---:|
| Full heavy mapping: RMS error against its own local heavy work difference | 0.16915% | 0.16916% |
| Same mapping: joint photon error against the heavy component alone | 0.69067% | 0.69092% |
| Order of operations alone: joint photon error against the heavy component alone | 25.236% | 25.239% |
| Heavy term, RMS in units of net signed source-work RMS | 129.911 | 129.829 |
| Remaining metric term, same units | 129.928 | 129.846 |
| Actual matched-minus-wave joint photon discrepancy, % of the original matched momentum-route correction | 0.577973% | 0.577985% |

**Derivation.** In the retained variables the heavy share of the local constraint is W_h = ρe/2 + 3ρHj/(2k²), including its share of DΦ. On the matched side e = h_f + 3Φ and j = h_w. Differentiating and using e′ = 3Φ′ − j − 3Hp + S_e, j′ = −Hj + k²(p + Ψ) + S_j gives

    W_h′ = ρ′e/2 + ρ(3Φ′ − j + S_e)/2
         + 3{[(ρH)′ − ρH²]j + ρH(k²Ψ + S_j)}/(2k²).

The instantaneous pressure terms cancel identically, including an additive test change in pressure (numerical residual below 6e−16 relative to the constituent rate scale). Pressure can still affect later states. In particular the retained closure pressure and filtered native pressure are not interchangeable; agreement was not assumed.

**Blind prediction.** Filter in the original stress phase, over a trailing π with initial missing history held at entry. The native route integrates the field-equation derivative of *weighted* work, including changing background and external energy/current; the matched route starts from filtered native e,j at each original left knot and evolves them across the cell with retained external work and common native metric drivers. No intermediate reset. Filtered native work integrated from rates agrees with independently filtered saved weighted work to 0.00519% coarse / 0.000654% fine in peak rate relative to its peak. Before scoring we froze both ΔA(W_native) − ΔW_matched and the complete heavy map ΔW_native − ΔW_matched. In photon space the latter divides the two route impulses by their own right-end D before subtraction. Neither forecast uses the total deficit or rescales an amplitude.

**Where the subtraction happens.** Split the signed work residual into supplied U difference plus wave-required minus matched-required work. Assign 3ḣ²Φ/2 on the native branch (ḣ denotes the retained heavy-field velocity) or 3ρΦ/2 on the matched branch to heavy matter; the remaining metric term is Δ[(D−D_h)Φ]. With this fixed split the fine-step metric term projects at −1.000102 times the heavy term along the latter's direction. Ordinary/nonheavy energy and current together have 0.276 times the *net* local RMS, and supplied U difference has only 0.00199 times that RMS. This is measured accounting, not a prediction of the metric response or an identification of two independently observable forces.

**What scattering sees.** On the fine step the observed heavy and complementary photon components have joint sizes 99.801% and 99.230% of the original small momentum correction. Subtracting signed complex histories, not their magnitudes, leaves 0.577985%. The order-only forecast gives 80.008% on that scale, not a small repair. The complete heavy map predicts 100.467%, with a 0.69092% vector error *relative to the actual heavy component*; that misses the 0.5% gate at both gravity steps. The projected error in its native-work part is only 0.00000041% of the original momentum correction; nearly all the 0.68954% error on that scale is on the averaged/matched side. The unaltered fine-step total energy and current gaps are 0.578207% and 0.577214%; the separate 0.163%-of-original-launch size limit still passes. No physical corrections applied.

**Next test.** Derive the changes of W_h and (D−D_h)Φ *as a pair*, with the potential advanced by the retained momentum equation, not inferred by subtracting heavy work from the observed total. Use the same left states, clock, and bins; freeze both the pair's sum and its photon projection before comparison. Keep ordinary energy/current and supplied U differences as separate controls. This distinguishes a real cancellation in the coupled evolution from a cancellation reconstructed after seeing the answer.

[Protocol](PROTOCOL.md) · [local work errors](evidence-001.zip) (archive member: `local-work.csv`) · [signed partition](evidence-001.zip) (archive member: `partition.csv`) · [photon comparison](evidence-001.zip) (archive member: `photon-scores.csv`) · [component sizes](evidence-001.zip) (archive member: `photon-terms.csv`) · [accuracy controls](evidence-001.zip) (archive member: `photon-accuracy.csv`) · [unchanged gates](evidence-001.zip) (archive member: `unchanged-gates.csv`) · [freeze receipt](evidence-001.zip) (archive member: `frozen.json`).
