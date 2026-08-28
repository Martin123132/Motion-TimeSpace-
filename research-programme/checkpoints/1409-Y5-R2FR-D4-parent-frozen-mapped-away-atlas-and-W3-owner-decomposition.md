# 5393: D4 parent-frozen mapped-away atlas and W3 owner decomposition

## Decision

**PARENT_FROZEN_MAPPED_ATLAS_AND_W3_OWNER_REDUCTION_CERTIFIED__PROCEED_TO_INTERVAL_ENCLOSURES**

This checkpoint does not claim `W3`. It replaces the seven incompatible
adaptive finite-rung leaf sets by one regulator-independent atlas inherited
from the parent topology contract and the eight fixed 5379 event tubes.

## Exact common map

For every frozen x-cell `X=[x_lo,x_hi]` and every active parent energy
chamber `C=[E_L(x),E_U(x)]`, use

```text
x = x_mid + (x_hi-x_lo) xi/2
E = (E_L(x)+E_U(x))/2 + (E_U(x)-E_L(x)) eta/2
J = (x_hi-x_lo)(E_U(x)-E_L(x))/4
(xi,eta) in [-1,1]^2.
```

The source topology certificate fixes the ordering of `E_L,E_U` over each
parent panel. Subdivision by fixed event-tube boundaries therefore preserves
the chamber map rather than introducing a regulator-dependent cubature tree.

## Pole subtraction

On an away cell the invariant decomposition is

```text
f = f_reg + sum_b rho_b/(E-p_b),
P_b = rho_b [Log(E_U-p_b)-Log(E_L-p_b)].
```

The raw real-energy integrand cannot be bounded directly on a complex
epsilon Cauchy circle: a displaced material pole can cross the real path.
The regular term and exact pole primitive must be enclosed separately.

## Complete owner table

- `B01`: `MC04_SM_DM` / `direct:L:s14` -> `MATERIAL_SIMPLE_POLE`; observed rows `756`.
- `B02`: `MC04_SM_DM` / `direct:shared:s13` -> `MATERIAL_SIMPLE_POLE`; observed rows `252`.
- `B03`: `MC04_SP_DP` / `direct:L:s01` -> `MATERIAL_SIMPLE_POLE`; observed rows `420`.
- `B04`: `MC04_SP_DP` / `direct:shared:s13` -> `MATERIAL_SIMPLE_POLE`; observed rows `504`.
- `B05`: `MC04_SM_DM` / `direct:R:s01` -> `REMOVABLE_ZERO_RESIDUE_POLE`; observed rows `21`.
- `B06`: `MC04_SP_DM` / `direct:R:s01` -> `REMOVABLE_ZERO_RESIDUE_POLE`; observed rows `84`.

Every inside-support geometric pole row across all seven stored regulator
rungs maps to exactly one of these six analytic owners.

## Counts

- parent topology panels: `13`;
- frozen x-cells: `29` (`21` away, `8` event);
- mapped active cells: `67`;
- observed inside-support poles assigned: `2037` / `2037`;
- maximum parent boundary reproduction error: `0`;
- minimum mapped midpoint energy width: `0.000134827250264`.

## Remaining calculation

The next checkpoint must interval-enclose three finite owner families:
`W_AWAY_REGULAR_2D`, `W_AWAY_POLE_PRIMITIVE_1D`, and
`W_EVENT_LOCAL_REMAINDER`. Only their sum supplies a numeric `W3`; only
then may `M_D4=max(H3,G3+W3)/6` be formed.

No outer-regulator, full-angular, UV, local-GR, or full-MTS claim follows.
