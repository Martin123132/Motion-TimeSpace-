> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The wave predicts the momentum response to specified gravity; the old reference was not measuring that response

**With the two previously frozen gravity histories imposed, the unmodified momentum forecast passes at both gravity steps.** Both wave twins start with the same native field perturbation and canonical velocity and use the same microscopic forcing. Identical gravity produces exactly zero difference, both directly and in the two absolute evolutions. The separate test of what gravity the native system generates from its saved stress change gives a very different answer.

| 89.1485038031–89.6 conformal Mpc; four source subdivisions | Coarse gravity (p16) | Fine gravity (p32) |
|---|---:|---:|
| Imposed gravity: paired momentum-change RMS (retained units) | 1.025956 × 10⁻²⁰ | 1.025806 × 10⁻²⁰ |
| Full frozen forecast: complex RMS error vs paired change | **0.006400%** | **0.001880%** |
| Frozen geometry-only component: error vs same change | 0.00002245% | 0.00002245% |
| Coupled native pair: current-change RMS from own 77-bin stress change | 3.504947 × 10⁻³⁴ | 1.670240 × 10⁻³⁴ |
| Old unpaired wave-minus-archive reference RMS | 4.327479 × 10⁻²² | 5.346500 × 10⁻²³ |

The full forecast also passes the unchanged 0.5% test on the first kinetic cycle (0.0351% / 0.0104%) and on the later window (0.00574% / 0.00168%). No launch displacement was applied to the twins. The slight difference between the full and geometry-only scores is expected: only the former includes the earlier inferred launch offset. The imposed experiment shares the forecast's metric inputs, not its oscillator solver, background replay or initial perturbation estimate. It checks the wave response, **not** the accuracy or independent origin of the imposed gravity.

## Why the old subtraction misled us

For the independent native reference we changed only the retained wave-stress increment in the 90-variable system. The initial state (including the metric), external microscopic fields and held forcing were otherwise identical. We propagated the difference from zero. Background velocity and the additive heavy current are common, so the current change is k²v times the field difference. A separate two-variable wave integration on the resulting native metric difference reproduces the full-system result. Native equal-input nulls are exactly zero. Direct subtraction of the two absolute physical-size field histories loses the signal (100% error); a predeclared amplified-source numerical control, scaled back down, verifies the direct equation to 0.0425% / 0.1209% on the primary sources. The amplified result is not the reported physical current.

The earlier difference equals **the paired stress response plus the discrepancy between the held-stress twin and the separately archived original wave**. That identity closes to better than 0.000002% of the old signal on every run. The latter discrepancy accounts for essentially the whole old reference: on the fine clock the paired stress response has only 3.1 × 10⁻¹⁰ percent of its RMS magnitude. This does not assign the entire archival discrepancy to a specific integration error.

**Convergence separates the input from the solver.** The imposed reference changes by 0.02191% between gravity grids. For the coupled native pair, holding *either* stress history fixed gives less than 2.1 × 10⁻¹⁰% grid error. Using each grid's separately computed stress history instead changes the response by **186.10%** relative to the fine result. Changing only the stress on one grid reproduces that difference. Thus the integrator passes at fixed input, but the physical native stress response has no grid-converged size in these saved inputs. It does not explain the imposed ∼10⁻²⁰ response. The two experiments apply different disturbances; failing their cross-comparison is not a failed prediction under identical forcing.

## Which part of gravity drives the momentum?

On fixed background, eliminating the canonical velocity from the paired field equations gives

    Δf″ + 2H Δf′ + (k²+ω²) Δf
      = 3v ΔΦ′ + v ΔΨ′ − 2ω²b ΔΨ + (v′+2Hv+ω²b)(3ΔΦ+ΔΨ),
    Δf′ at the switch = v(3ΔΦ+ΔΨ) at the switch.

Here H is the conformal expansion rate, ω=am, and the final term measures the interpolation defect of the stored background. The absolute value of a constant curvature offset cancels from the bulk equation for an exact background; it still affects the initial physical slope if the canonical velocities are equal. An independent integration of the five terms reproduces the response on both gravity grids. On the fine imposed history the **lapse-value term −2ω²b ΔΨ** supplies +106.14% along the final current-change waveform; the curvature-rate and lapse-rate terms oppose it (−4.61%, −1.54%). The initial slope supplies +0.013%. On the fine native stress-driven history the lapse-value share is +97.50%. These are signed projections, not energy fractions or independent observations.

**Next test:** give the averaged metric equations and the native equations the *same* frozen stress perturbation (first the fine input, then the coarse input as a control), with zero initial departure within each branch. Predict ΔΨ on the averaged side before scoring the native lapse. Separate the contribution from curvature from the shear term in the metric constraint, then carry those contributions into heavy momentum. That tests who generates the lapse difference, rather than testing again how a wave responds to gravity we supply. The previous photon result, reviewed paper and production history are unchanged.

[Protocol](PROTOCOL.md) · [Native twin controls](evidence-001.zip) (archive member: `native-controls.csv`) · [Imposed-gravity controls](evidence-001.zip) (archive member: `imposed-controls.csv`) · Sealed paired references (not bundled here) · [Frozen forecast scores](evidence-001.zip) (archive member: `frozen-comparisons.csv`) · [Fixed-input and own-input convergence](evidence-001.zip) (archive member: `convergence.csv`) · [Old reference ledger](evidence-001.zip) (archive member: `old-reference-ledger.csv`) · [Metric-term decomposition](evidence-001.zip) (archive member: `metric-term-ledger.csv`).

Reproduction in a fresh sibling directory with the same sealed parents: run twin_stage.py, native_pair.py, metric_pair.py, score_pair.py, metric_work_terms.py and verify_twins.py. No photon propagation, likelihood, fitting or publication was performed.
