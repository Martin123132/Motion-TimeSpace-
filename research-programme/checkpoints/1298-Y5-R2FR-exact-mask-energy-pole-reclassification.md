# 5282 — Exact-mask energy-pole reclassification

## Purpose

The 5281 order sequence did not converge and localized the dominant
regular-remainder mass near the old MC12 geometric pole. This checkpoint
reclassifies every sourced 5267 pole with the exact Boolean masks and
fits its true local-limit residue.

## Result

- geometric candidates: `24`;
- exact-active candidates: `8`;
- promoted from old inactive status:
  `6`;
- material pole owners: `['MC04', 'MC12']`;
- removable zero-residue owners:
  `['MC03', 'MC07']`;
- maximum fit residual:
  `2.3067896544e-05`.

The exact mask activates MC03, MC04, MC07, and MC12 at their relevant
centres. True-limit fitting then separates geometry from materiality:
MC03 and MC07 have residues below the material floor, while MC04 and
MC12 carry nonzero simple-pole residues. MC12 was therefore omitted by
the old causal classification and must be restored.

## Acceptance gates

- `MC03_MC07_are_removable_zero_residues`: **PASS**
- `MC12_promoted_from_old_inactive_status`: **PASS**
- `all_active_candidates_fit`: **PASS**
- `claims_locked_false`: **PASS**
- `exact_active_component_set_reproduces`: **PASS**
- `fit_and_coefficient_controls_pass`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `four_exact_active_candidates_per_regulator`: **PASS**
- `material_poles_are_MC04_and_MC12`: **PASS**
- `parent_5280_accepted`: **PASS**

Validation: **PASS**.

## Claim boundary

This closes the fixed-angle active-pole inventory, not the energy
integral. The already computed 4/8/16 nodes must now be reassembled with
both MC04 and MC12 subtracted before convergence can be judged.
