# 5274 — Full safe-component materiality and mask-insertion audit

## Scope

Checkpoint 5273 reduced the six transported material components to exact
Boolean masks. Before volume cubature, this checkpoint checks two possible
failure modes:

1. whether differentiating the mask creates unaccounted surface-delta
   terms;
2. whether any of the nine safe components that vanished at the source
   event become double-pole material components elsewhere.

## Mask insertion

The sourced parent assembly is

`dynamic_multiplier * component_contribution`,

followed by a linear sum over components. No derivative acts on the
multiplier or the exact Boolean replacement. Therefore this integrand
contains no mask-generated surface-delta term. This conclusion applies to
the current parent integrand; it is not a claim about a different future
observable that explicitly differentiates the occupation.

## Full safe-component audit

- Safe components: **15**.
- Source-material components: **6**.
- Source-zero components: **9**.
- Target events: **48**.
- Regulator/path audits: **96**.
- Pole-order rows: **1440**.
- Source-labelled material components stable under the finite-difference classifier: **4/6**.
- Source-labelled zero components stable under the finite-difference classifier: **7/9**.
- Classification-unstable IDs: **MC02, MC03, MC07, MC08**.
- Maximum projective transport step: `0.0495702146915`.
- Maximum reciprocal residual: `4.22268460434e-12`.

The instability is not interpreted as physical branch creation or
annihilation. The parent classifier estimates pole order at fixed
double-precision displacements. A small double-pole coefficient can be
hidden by the regular background at those displacements, so the four
unstable IDs require an arbitrary-precision local limit.

## Acceptance gates

- `all_fifteen_mask_derivations_close`: **PASS**
- `all_transport_paths_pass`: **PASS**
- `both_regulators_audited`: **PASS**
- `claims_locked_false`: **PASS**
- `classification_instability_localized`: **PASS**
- `complete_two_regulator_component_audit`: **PASS**
- `fixed_six_component_basis_rejected`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `mask_is_purely_multiplicative`: **PASS**
- `no_higher_pole_detected`: **PASS**
- `parent_5273_accepted`: **PASS**

Validation: **PASS**.

## Claim boundary

Passing this checkpoint rejects, rather than licenses, a fixed
six-component cubature. It does not turn forty-eight sampled events into
an analytic global structural-zero theorem, nor does it claim the final
phase-space coefficient, UV coefficient, local GR, or the full MTS
theory.

## Next target

Evaluate the local coefficient limit with arbitrary precision, separated
into direct and endpoint-subtraction summands, for all fifteen components.
Only after that limit resolves the four unstable IDs may the global
cubature basis be selected.
