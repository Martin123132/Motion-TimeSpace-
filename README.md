# Motion-TimeSpace Research Programme

Motion-TimeSpace (MTS) is an open, work-in-progress research programme exploring whether motion, time, space, memory, and observed gravitational and cosmological structure can be organized into one disciplined field-theoretic framework.

This repository is not presented as a completed theory of physics. It is a public research workbench containing derivation attempts, failed routes, claim ceilings, numerical gates, empirical scorecards, and reproducible scripts.

## Current Status

The project now has five connected layers:

1. **Parent and infrared branch** - one explicit CTP translation-gauge/coframe parent action contains the metric/coframe, visible matter, canonical `U(1)`, and reflection-even motion sector. The coframe is an honest parent premise rather than something falsely derived from four scalar clocks.
2. **Local GR/Newton/Maxwell branch** - on the source-selected `chi=0`, locally silent state, the complete nonlinear two-derivative restriction is exactly GR + Lambda + Standard Model + Maxwell. The same action yields Newtonian mechanics, geodesics, lensing, Lorentz force, Maxwell stress, Poynting flux, and the full ten-parameter GR PPN vector without arena retuning.
3. **Higher-operator branch** - calculated scalar, curvature-photon, nonlocal, and propagation residuals are separated from the exact two-derivative theorem. The first canonical MTS-specific `p8` coefficient remains unresolved. Its D4 programme now has derived endpoint coefficients, pole/contour clearance certificates, and a resumable interval proof for the regular-away contribution; the full regular-away integral is not yet closed.
4. **Cosmology and large-scale motion** - a direct parent-scalar SN+BAO+growth+compressed-CMB programme has been executed, while mass/state selection and the occupied retarded response remain open. A single elementary mass cannot simultaneously be the fitted homogeneous cosmology pole and the conditional galactic collective scale.
5. **Empirical branches** - the preregistered 12-seed galaxy-formation comparison is complete. Its `q` component is MTS-directed, its RMSE component is unresolved, and the locked result is a statistical draw/metric split rather than model preference.

The 2026-09-09 update extends the contiguous public record through checkpoint
`1530`, corresponding to private checkpoint `5514`. It adds the D4 audit
through the latest complete private checkpoint, reader-facing field-theoretic
derivation notes, and two sealed annular source packages. Large run products,
the incomplete `5515` frontier, and third-party/source caches remain excluded.

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
- `docs/status/STATUS-2026-08-29.md` - historical status snapshot from the previous upload.
- `docs/status/PUBLICATION-NOTES-2026-08-29.md` - historical scope, integrity checks, and exclusions from the previous upload.
- `docs/status/STATUS-2026-09-09.md` - current reader-facing WIP status.
- `docs/status/PUBLICATION-NOTES-2026-09-09.md` - exact current update scope, omissions, and claim boundary.
- `research-programme/catalogue/README.md` - bounded direct-link catalogues for large artifact folders.
- `docs/theory-gates/LOCAL-GR-NEWTON-GATES.md` - the updated local-limit gate map.
- `research-programme/checkpoints/1203-Y5-R2FR-canonical-local-parent-action-Hessian-source-residue-and-scale-setting-theorem.md` - consolidated local action and scale-setting theorem.
- `research-programme/checkpoints/1217-Y5-R2FR-source-complete-coframe-variation-full-PPN-calibration-and-local-state-silence-theorem.md` - source-complete coframe variation and full PPN gate.
- `research-programme/checkpoints/1219-Y5-R2FR-one-canonical-translation-gauge-parent-action-cross-coupling-and-branch-reduction-theorem.md` - common parent action.
- `research-programme/checkpoints/1224-Y5-R2FR-common-minimal-motion-trajectory-canonical-Z-quotient-absolute-scale-covariance-and-local-GR-selection.md` - selected common motion trajectory.
- `research-programme/checkpoints/1227-Y5-R2FR-selected-trajectory-exact-GR-Maxwell-consistent-truncation-universal-source-and-matched-GRSM-excess-theorem.md` - strongest current local GR/Newton/Maxwell theorem.
- `research-programme/checkpoints/1261-Y5-R2FR-reciprocal-projective-chamber-boundary-tracker.md` - replacement topology contract.
- `research-programme/checkpoints/1360-Y5-R2FR-closed-parent-local-vacuum-attractor-no-go-and-minimal-reduced-dynamics-contract.md` - exact limit on closed-parent local-state preparation.
- `research-programme/checkpoints/1375-Y5-R2FR-D4-zero-regulator-endpoint-coefficient-limit.md` - analytic zero-regulator endpoint coefficient.
- `research-programme/checkpoints/1412-Y5-R2FR-D4-deformed-contour-regular-away-W3.md` - active regular-away contour proof ledger.
- `research-programme/checkpoints/1429-Y5-R2FR-D4-left-second-soft-mixed-angle-subcover-gate.md` - exact finite-cover interval-dependency repair.
- `research-programme/checkpoints/1433-Y5-R2FR-D4-v43-right-connector-frontier-expansion-gate.md` - previous-upload verified frontier; the current public range continues through checkpoint `1530`.
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
|   |-- catalogue/
|   |-- checkpoints/
|   |-- protocols/
|   |-- reproducibility/
|   |-- scripts/
|   |-- source-intake/
|   `-- derivations/
|-- tools/
|-- data/
`-- archive/
    `-- legacy-pre-formalization-2026-06/
```

## Reproducibility Notes

Public checkpoint filenames use a compact sequence, while document titles and
generated artifact names retain their original private checkpoint IDs for
provenance. The established offset is `3984`; this update adds private
checkpoints `5418-5514` as public checkpoints `1434-1530`.

The repository includes source scripts, compact residual/register artifacts,
reader-facing derivation notes, two sealed annular source packages, and a
transitive reproducibility capsule, but not
large third-party datasets, virtual environments, the incomplete `5515`
frontier, or raw generated run/cache folders. Local machine paths retained in
historical artifacts are provenance records, not portable execution paths.

GitHub can cap the visible entries in very large flat folders and pull-request
file lists. The generated catalogue shards and SHA-256 publication inventory
provide direct access and completeness checks without changing historical
paths. New export directories are bounded; legacy flat directories may remain
larger than 1,000 entries.

### Windows Checkout

The preserved legacy archive contains relative paths up to 232 characters.
A clone into a long Windows parent path can therefore hit the older 260-
character checkout limit even though every Git object was downloaded. Use a
short destination such as `D:\MTS`, or enable Git's long-path handling for
that clone:

```powershell
git -c core.longpaths=true clone https://github.com/Martin123132/Motion-TimeSpace-.git D:\MTS
```

## Research Ethos

This work is deliberately conservative about claims. A branch can be useful, promising, or competitive without being promoted to a completed theory. Promotion requires derivation, consistency with known limits, and empirical robustness against matched baselines.
