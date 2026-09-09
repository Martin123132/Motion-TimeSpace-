# 5459: D4 TOP left external-41 projective edge transplant

## Decision

**TOP_PARENT_AMPLITUDE_COVER_CERTIFIED_BY_LEFT_EXTERNAL41_SUBCOVER__RESUME_OUTER_SMOKE**

## Derived repair

Checkpoint 5458 removed the first-spinor pivot obstruction but preserved 133 failures of the same left-cut edge. The failed edge is not the right-cut external-41 object treated by checkpoints 5430-5431. On the left cut, `p4=(-1,0,0,+1)` has exact rational spinors `lambda4=(0,-2)` and `tilde_lambda4=(0,1)`. Therefore `<1,4>=-2 p1_plus` in the plus family and `<1,4>=-2 p1_antiholomorphic` in the minus family; the matching square edges follow from the same two-component determinants.

Parent revision v51 evaluates those exact determinants on a finite subcover of each already-certified checkpoint-5457 projective cell. When the coarse normalization obscures an edge, it rebuilds the complete first-spinor pair in one surviving projective family before any amplitude factor is evaluated. It installs an edge-only fallback only when the family is unchanged. No pole is deleted, no fitted parameter is introduced, and the amplitude is unchanged.

## Result

Rerun cells completed: `133/133`; passed: `133`; failed: `0`.
Combined TOP cells certified: `512/512`. Minimum projective margin: `0.03841034412596338`. Minimum amplitude denominator: `4.508362136008378e-05`.

## Claim boundary

A complete pass closes only the E01/U017 TOP parent-amplitude box. The remaining checkpoint-5456 outer representatives, full event-cell cover, event-local W3, regulator limit, local GR and full MTS claims remain open.
