# Motion-TimeSpace Research Programme

Motion-TimeSpace (MTS) is an open, work-in-progress research programme exploring whether motion, time, space, memory, and observed gravitational and cosmological structure can be organized into one disciplined field-theoretic framework.

This repository is not presented as a completed theory of physics. It is a public research workbench containing derivation attempts, failed routes, claim ceilings, numerical gates, empirical scorecards, and reproducible scripts.

## Current Status

The project now has five connected layers:

1. **Parent and infrared branch** - one explicit CTP translation-gauge/coframe parent action contains the metric/coframe, visible matter, canonical `U(1)`, and reflection-even motion sector. The coframe is an honest parent premise rather than something falsely derived from four scalar clocks.
2. **Local GR/Newton/Maxwell branch** - on the source-selected `chi=0`, locally silent state, the complete nonlinear two-derivative restriction is exactly GR + Lambda + Standard Model + Maxwell. The same action yields Newtonian mechanics, geodesics, lensing, Lorentz force, Maxwell stress, Poynting flux, and the full ten-parameter GR PPN vector without arena retuning.
3. **Higher-operator branch** - calculated scalar, curvature-photon, nonlocal, and propagation residuals are separated from the exact two-derivative theorem. The first canonical MTS-specific `p8` coefficient remains unresolved.
4. **Cosmology and large-scale motion** - a direct parent-scalar SN+BAO+growth+compressed-CMB programme has been executed, while mass/state selection and the occupied retarded response remain open. A single elementary mass cannot simultaneously be the fitted homogeneous cosmology pole and the conditional galactic collective scale.
5. **Empirical branches** - the preregistered 12-seed galaxy-formation comparison is complete. Its `q` component is MTS-directed, its RMSE component is unresolved, and the locked result is a statistical draw/metric split rather than model preference.

The July 24 update refreshes public checkpoint `1192` with its completed
12-seed result and adds checkpoints `1193` through `1230`, corresponding to
private checkpoints `5177` through `5214`. The contiguous record includes
negative results, corrected sign errors, parent-action derivations,
cosmological robustness tests, the exact selected local-GR truncation, and the
current nonclaim two-loop estimator work. Large run products and
third-party/source caches remain excluded.

The strongest honest claim is:

> MTS now contains an explicit parent action with an exact selected nonlinear
> two-derivative reduction to GR + Lambda + Standard Model + Maxwell, including
> Newtonian mechanics and all ten GR PPN values. It does not yet derive the
> parent coframe/visible ontology from motion, time, and space alone, establish
> all-operator or strong-field completeness, derive the occupied galactic
> response law, fix the absolute gravitational/vacuum scales internally, or
> demonstrate overall empirical preference over standard baselines.

## Start Here

- `CLAIM_CEILING.md` - the current claim boundary.
- `docs/status/STATUS-2026-07-24.md` - concise current status and open problems.
- `docs/status/PUBLICATION-NOTES-2026-07-24.md` - exact update scope and exclusions.
- `docs/theory-gates/LOCAL-GR-NEWTON-GATES.md` - the updated local-limit gate map.
- `research-programme/checkpoints/1203-Y5-R2FR-canonical-local-parent-action-Hessian-source-residue-and-scale-setting-theorem.md` - consolidated local action and scale-setting theorem.
- `research-programme/checkpoints/1217-Y5-R2FR-source-complete-coframe-variation-full-PPN-calibration-and-local-state-silence-theorem.md` - source-complete coframe variation and full PPN gate.
- `research-programme/checkpoints/1219-Y5-R2FR-one-canonical-translation-gauge-parent-action-cross-coupling-and-branch-reduction-theorem.md` - common parent action.
- `research-programme/checkpoints/1224-Y5-R2FR-common-minimal-motion-trajectory-canonical-Z-quotient-absolute-scale-covariance-and-local-GR-selection.md` - selected common motion trajectory.
- `research-programme/checkpoints/1227-Y5-R2FR-selected-trajectory-exact-GR-Maxwell-consistent-truncation-universal-source-and-matched-GRSM-excess-theorem.md` - strongest current local GR/Newton/Maxwell theorem.
- `research-programme/checkpoints/1230-Y5-R2FR-A00-identical-graviton-permutation-control-variate.md` - latest coefficient-free estimator theorem and nonclaim gate.
- `research-programme/protocols/1192/README.md` - frozen protocol and complete compact 12-seed outcome.

## Repository Layout

```text
.
|-- CLAIM_CEILING.md
|-- PROJECT_MAP.md
|-- docs/
|   |-- status/
|   `-- theory-gates/
|-- research-programme/
|   |-- checkpoints/
|   |-- protocols/
|   |-- scripts/
|   `-- source-intake/
|-- tools/
|-- data/
`-- archive/
    `-- legacy-pre-formalization-2026-06/
```

## Reproducibility Notes

Public checkpoint filenames use a compact sequence, while document titles and
generated artifact names retain their original private checkpoint IDs for
provenance. The established offset is `3984`; this update maps private
checkpoints `5176-5214` to public checkpoints `1192-1230`.

The repository includes source scripts and compact residual/register artifacts, but not large third-party datasets, virtual environments, raw generated run folders, or the local `functional_rg` source cache. Local machine paths retained in historical artifacts are provenance records, not portable execution paths.

## Research Ethos

This work is deliberately conservative about claims. A branch can be useful, promising, or competitive without being promoted to a completed theory. Promotion requires derivation, consistency with known limits, and empirical robustness against matched baselines.
