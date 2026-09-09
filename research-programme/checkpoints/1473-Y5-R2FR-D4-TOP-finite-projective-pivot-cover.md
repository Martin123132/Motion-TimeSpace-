# 5457: D4 TOP finite projective-pivot cover

## Decision

**TOP_FINITE_PROJECTIVE_PIVOT_COVER_CERTIFIED__TRANSPLANT_OWNER_CELLS**

## Exact algebra

The four candidate pivots are the light-cone components of one massless momentum. Direct reduction of the source formulas modulo `s_s^2+c_s^2=1` and `s_d^2+c_d^2=1` gives

```text
p_plus p_minus - p_holomorphic p_antiholomorphic = 0.
```

The Groebner remainder is exactly zero. The pivots are therefore a projective atlas, not four unrelated fitted denominators.

## Finite owner cover

The previously blocked `E01__U017__TOP__MAXIMUM_PHYSICAL_PATH_AREA` domain is partitioned into `512` closed `(x,t)` cells. On every cell the unchanged parent selector first chooses the required representative/reciprocal chart set. Every selected chart is then checked on all `4` contour arcs and assigned the pivot with the largest certified lower modulus.

Rows passed: `2048/2048`. The global minimum owned-pivot modulus is `0.03841034412596338` and the minimum unit-circle modulus is `2.3082691498686003`.

## Claim boundary

This proves only the finite projective ownership cover for the first blocked E01/U017 TOP representative. It does not yet transplant those owner cells into the full amplitude evaluator or validate the remaining outer representatives. Event-local W3, the regulator limit, local GR and full MTS remain unclaimed.
