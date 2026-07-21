# 5052 - unit-Richardson seed jackknife

Marker: `MTS_5052_UNIT_RICHARDSON_SEED_JACKKNIFE`.

**Cost correction:** the jackknife ratios remain valid. Its 32.10-hour runtime
projection is withdrawn because paired seed-mean variance units contain two
events. Checkpoint 5055 is the active execution-cost contract.

The parameter-free real-only control from 5051 was retested after deleting each
independent Owen scramble in turn. No coefficient is refit, so this is a pure
leverage test of the exact `B=1` contract.

All four delete-one panels pass:

- equal-cost score-ratio range: `0.553` to `0.652`;
- worst active-real correction ratios: `0.140`, `0.216`, `0.160`, `0.297`;
- every active real channel improves in every panel;
- all inactive imaginary channels remain exactly unchanged;
- all panels remain below the locked `0.8` efficiency threshold.

The full four-seed score ratio is `0.6663`. The slightly lower delete-one values
show that no single seed manufactures the gain. The statistical design is now
robust enough to lock statistically, but no unit-consistent fresh run is below
the current 10-hour execution cap. No new kernel run is authorized.

## Evidence

- Result: `source-intake/functional_rg/5052/unit_richardson_seed_jackknife.json`
- Panels: `source-intake/functional_rg/5052/unit_richardson_jackknife_panels.csv`
- Components: `source-intake/functional_rg/5052/unit_richardson_jackknife_components.csv`
- Generator: `scripts/Y5_R2FR_5052_unit_richardson_seed_jackknife.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5052_VALIDATION.csv`

No target central value was fitted and no production amplitude, GR, Newton,
Maxwell, or full-MTS claim follows.
