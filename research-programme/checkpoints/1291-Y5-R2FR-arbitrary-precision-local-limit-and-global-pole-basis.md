# 5275 — Arbitrary-precision local limit and global pole basis

## Question

Checkpoint 5274 showed that the fixed-displacement double-precision pole
classifier changed its answer for MC02, MC03, MC07, and MC08. This
checkpoint evaluates the defining local coefficient directly:

`C_2 = lim_(delta -> 0) delta^2 I(z_0 + delta)`.

The limit is evaluated at `80` decimal digits and at
three displacement scales, with direct and endpoint-subtraction
summands kept separate.

## Result

The apparent component exchange was numerical, not topological.

- Generic double-pole basis (8):
  `MC02, MC03, MC04, MC07, MC08, MC12, MC14, MC15`.
- Generic simple-pole complement (7):
  `MC01, MC05, MC06, MC09, MC10, MC11, MC13`.
- Direct-owned doubles:
  `MC02, MC03, MC04, MC07, MC08, MC12`.
- Endpoint-subtraction-owned doubles:
  `MC14, MC15`.
- Hidden by the 5239 source-event material floor:
  `MC02, MC08`.
- Double-precision disagreements:
  **12** of
  **150** local limits.

MC02 and MC08 have small but nonzero direct-sector double coefficients.
The regular background dominates at the old fixed displacement, causing
the old scaling estimate to report a lower pole. The arbitrary-precision
coefficient stabilizes as the displacement is reduced.

## Numerical controls

- Events: `P000, P001, P004, P024, P046`.
- Regulators: `E040, E020`.
- Maximum refined collision residual:
  `4.68360125429e-79`.
- Maximum root-refinement chordal displacement:
  `3.32846471249e-14`.
- Maximum double-coefficient relative change:
  `5.79448296466e-13`.

## Acceptance gates

- `all_component_classifications_stable`: **PASS**
- `all_roots_refined`: **PASS**
- `all_transport_paths_pass`: **PASS**
- `claims_locked_false`: **PASS**
- `complete_limit_matrix`: **PASS**
- `direct_double_owner_set_closes`: **PASS**
- `double_coefficients_converge`: **PASS**
- `eight_generic_double_components`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `hidden_source_components_identified`: **PASS**
- `parent_5274_accepted`: **PASS**
- `seven_generic_simple_components`: **PASS**
- `subtraction_double_owner_set_closes`: **PASS**

Validation: **PASS**.

## Claim boundary

This replaces the source-event six-component list with an
eight-component *generic* pole basis and licenses only an
eight-component cubature smoke. Five events and two regulators do not
constitute a global pointwise theorem. No final phase-space coefficient,
UV coefficient, local-GR result, or full-MTS claim follows.

## Next derivation

Build the denominator-incidence proof. Show term by term that the seven
complement components cannot contain two simultaneous denominator
factors, while the six direct-owned and two subtraction-owned basis
components possess a generically nonzero double coefficient. This turns
the sampled generic basis into an analytic almost-everywhere statement.
