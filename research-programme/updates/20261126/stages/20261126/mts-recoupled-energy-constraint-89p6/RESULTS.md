> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Momentum and density disagree for the isolated 77-bin feedback response

**The fixed-stress response fails the time-time Einstein constraint on both the recoupled branch and the resolved-wave control.** This is the same single retained mode (k = 0.3368801 per conformal Mpc), from the switch at 89.1485038031 to 89.6. The heavy wave still passes the preceding current and energy-balance tests. This test asks a different question: can the *entire incremental source packet* and the ordinary matter it moves produce the same curvature via the energy and momentum equations, with no change in the externally held geometry source U?

| Full window; fine gravity / four subdivisions | Fine stress: recoupled | Fine stress: resolved | Coarse stress: recoupled | Coarse stress: resolved |
|---|---:|---:|---:|---:|
| RMS difference of the two curvature readouts / RMS momentum-driven Φ | 1,443.37 × | 1,443.37 × | 1,934.44 × | 1,934.44 × |
| Error in the frozen required imposed density, relative to the archived density | 100.6811% | 100.6811% | 100.6222% | 100.6222% |
| Constraint residual / sum of individual term RMS sizes | 99.9924% | 99.9924% | 99.9940% | 99.9940% |

The first ratio is large partly because the momentum-driven metric *change* is tiny. On fine stress its native RMS is 7.788 × 10⁻³²; the density-route RMS is 1.123 × 10⁻²⁸. The third row checks a different denominator: the residual is also large on the scale of the source terms themselves. The two branches' residuals differ by just 0.0000290% of the native residual on fine stress (0.0000271% on coarse stress). This shared failure is not evidence against the wave-current replacement relative to its resolved control, nor is it a test of an absolute cosmological solution or observational fit.

## What was compared

The retained Hamiltonian form is BΦ + E_can/2 + 3HJ/(2k²) = U, with B=k²+V/2. Here the two histories being differenced within each branch have the same supplied U and Fq. V accounts for metric-volume contributions exactly once, with 3v_heavy² rather than the obsolete averaged-heavy density coefficient. Independently, the physical-density form is k²Φ + D_total/2 + 3H(Φ′+HΨ), with D_total=E_can+VΦ. We used the sealed physical heavy density directly in this check.

The photon–baryon, collisionless, cold and light-scalar equations were independently replayed in each saved metric; the heavy terms came from the preceding sealed calculation. The required imposed energy was frozen with the imposed momentum retained **before scoring against the supplied energy**. It was not fitted or substituted. In all 48 combinations of branch, stress, window and integration grid, neither the curvature nor imposed-density result met 0.5%. All 72 fixed-input refinement comparisons pass; the worst is below 1.9 × 10⁻⁹%. The independent momentum integration, responsive shear and the two energy forms pass their controls, as do the exact zero input and the manufactured 1% incompatibility.

On the fine resolved run the imposed density alone contributes **99.3235% of the signed projection along the residual**, the imposed momentum contributes 0.6102%, and the metric term 0.0656%. These are not energy fractions. The required imposed density RMS is 1.753 × 10⁻³¹, compared with the archived 2.554 × 10⁻²⁹ in the same units. Neither a closer heavy-wave approximation nor finer time stepping is the first place to look.

## Why this particular packet carries that much density

The saved packet was originally a **single feedback iteration**, not a free-standing stress solved on the new incremental metric. Its 77 massive momentum bins were driven by an earlier change in the ordinary collisionless angular history and lapse. We tested the density consequence using the original generator and driving history, without rerunning 77 bins, fitting a normalization, or changing either source file.

For comoving momentum q, energy ε=√(q²+(am)²), speed v_q=q/ε and retained monopole lag L₀, the generator actually uses L₀′=−k[v_q L₁+(v_q−1)n₁,old]. With weight w=q² expit(−q) expit(q), C the saved normalization, and R the ratio of the packet and generator energy normalizations, the integrated moment obeys

    (a² E/R)′ = (a²/R)[(a′/a) T − J]
                + k C n₁,old ∫ w q²(ε−q) d ln q .

Here T is the *fourth* saved moment (mass trace), J includes the longitudinal k factor, and entry E=0. The last term has a plus sign from v_q−1. Replaying the old ordinary angular system reproduces its recorded driver peak; it supplies n₁,old, not a dipole inferred from the density target. Integrating only this moment equation with the saved current and trace reconstructs the dense archived energy to **0.0000393%** on fine stress and **0.0000172%** on coarse stress. Omitting the old dipole source gives **100.18% / 100.15%** errors. Using only the 11 retained knots instead of the dense stress archive changes the energy by 0.0437% / 0.0192%, far too little to explain the constraint miss.

The ordinary dipole induced by the isolated packet is less than 8 × 10⁻⁹ **percent** of the old driver's RMS. In a diagnostic that changes only that dipole while retaining the packet current and trace, the density still misses the gravitationally required density by **73.4% / 75.1%** on the required density's own scale. So the archived density is understandable from its original preparation; editing just its monopole source does not repair the mixed calculation. This is an attribution check, not a new self-consistent solution.

## Next local test

Return to the two **nonzero prepared histories** whose difference originally drove the 77 bins. Reconstruct the density constraint of each on the same initial slice (including its own U), then carry their ordinary angular moments, metric and massive stress at the same iteration order. Keep the prepared driving contribution distinct from its induced response; compare the difference of the two complete constraints with this isolated-packet result. An unforced all-zero restart or solving for a new U from the desired answer would not be a test. No new time interval, photon visibility calculation or tuning is needed first.

[Protocol](PROTOCOL.md) · Frozen required densities (not bundled here) · [Constraint results](evidence-001.zip) (archive member: `constraint-scores.csv`) · [Signed sector contributions](evidence-001.zip) (archive member: `residual-ledger.csv`) · [Independent form checks](evidence-001.zip) (archive member: `form-controls.csv`) · [Branch comparison](evidence-001.zip) (archive member: `branch-comparison.csv`) · [Fixed-input refinement](evidence-001.zip) (archive member: `refinement.csv`) · [Original-driver energy check](evidence-001.zip) (archive member: `packet-balance.csv`).

Reproduce in a fresh sibling directory with the same sealed inputs, using the retained Python with -B and one numerical thread: ham_stage.py, ham_forecast.py, ham_test.py, packet_energy.py, ham_verify.py. No parent source, observational dataset, production history, paper or public repository was changed.
