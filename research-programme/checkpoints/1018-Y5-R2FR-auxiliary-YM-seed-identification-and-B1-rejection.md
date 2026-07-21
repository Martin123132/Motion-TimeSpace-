# 5002 — Auxiliary Yang–Mills seed identification and B1 rejection

## Result

The physical minimal Yang–Mills seed in the checked `GluonsSymms.txt` auxiliary ordering is its **second** list element, not its first:

```text
GluonsSymms element 2 = 8 s t A_YM(1,2,3,4).
```

This identity was established by an independent color-ordered Feynman-rule reconstruction, not by trusting the basis label. Both cubic channels and the quartic vertex were included, and all four exact Ward replacements vanish. Across six generic transverse samples, element 2 has the constant ratio `8`; element 1 has varying ratios and is therefore a different gauge-invariant tensor.

## Consequence

The element-1 `hh` branch generated during 5000–5001 is a useful diagnostic but is not the minimal Einstein/Yang–Mills shared cut. It must not supersede the independently closed 4998 boxes. Those outputs are quarantined before the physical element-2 reconstruction is rerun.

## Source-label caution

The paper narrative names a minimal tensor `B_1 = s t A_YM`, but this does not license identifying it with the first raw auxiliary-list position. The executable identity above fixes the auxiliary ordering and normalization directly.

## Claim boundary

This checkpoint corrects an internal cut seed. It does not by itself close the remaining generic-dimensional evanescent coefficient or the outer MTS kernel.

- Comparison: `post-checkpoint-work/source-intake/functional_rg/5002/auxiliary_yang_mills_seed_comparison.csv`
- Gates: `post-checkpoint-work/source-intake/functional_rg/5002/auxiliary_yang_mills_seed_identification_gate.csv`
- Result: `post-checkpoint-work/source-intake/functional_rg/5002/auxiliary_yang_mills_seed_identification_results.json`
