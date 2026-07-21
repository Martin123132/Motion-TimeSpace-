# 4729 - R826 Parent Object-Language Exhaustion or First Hom Bound Row

Generated: `2026-07-07T22:42:17+00:00`

## Purpose

4729 attacks the object-language fork created by 4728: either parent-sign the allowed/forbidden arguments of `R_826`, or create the first finite `H_R826` Hom-bound row.

## What Actually Moved

- The `R_826` parent object inventory is now explicit.
- Allowed objects are `q_obs` geometry, fixed representation data, and a parent-signed common measure.
- Forbidden targets are hidden scalar, readout/material, boundary/domain, source-shadow, disconnected block-weight and extra mass/source channels.
- Exhaustion is not signed: the current corpus gives theorem shape and filters, not a complete parent object-language proof.
- The first finite row now exists: `H_R826_total = H_hidden_R826 + H_readout_R826 + H_domain_R826 + H_source_shadow_R826 + H_block_R826 + H_extra_mass_R826 + H_rad_R826`.

## Object Inventory

- `INV4729_0_q_obs_geometry`: ALLOWED_QBASIC
- `INV4729_1_fixed_representation`: ALLOWED_IF_FIXED
- `INV4729_2_common_measure`: CONDITIONAL_COMMON_MEASURE
- `INV4729_3_hidden_scalar_target`: FORBIDDEN_TARGET_UNSIGNED
- `INV4729_4_readout_target`: FORBIDDEN_TARGET_UNSIGNED
- `INV4729_5_domain_boundary_target`: FORBIDDEN_TARGET_UNSIGNED
- `INV4729_6_source_shadow_target`: FORBIDDEN_TARGET_UNSIGNED
- `INV4729_7_block_weight_target`: FINITE_BLOCK_WEIGHT_SURVIVES
- `INV4729_8_extra_mass_channel`: EXTRA_CHANNELS_SURVIVE
- `INV4729_9_verdict`: INVENTORY_WRITTEN_EXHAUSTION_UNSIGNED

## Exhaustion Theorem

- `EXH4729_0_exact_statement`: EXACT_CONDITIONAL_THEOREM
- `EXH4729_1_chain_rule`: DERIVED_CHAIN_RULE
- `EXH4729_2_absent_target`: NO_HOM_CONDITIONAL
- `EXH4729_3_same_action_filter`: PARTIAL_FILTER_DERIVED
- `EXH4729_4_exchange_block_filter`: DERIVED_REFINEMENT_NOT_EXHAUSTION
- `EXH4729_5_exhaustion_verdict`: EXHAUSTION_NOT_SIGNED

## First Hom Bound Row

- `HR8264729_0_total`: MISSING_COMPONENT_VALUES
- `HR8264729_1_hidden_scalar`: MISSING_HIDDEN_TARGET_EXCLUSION_OR_VALUE
- `HR8264729_2_readout`: MISSING_READOUT_NATURALITY_OR_VALUE
- `HR8264729_3_domain`: MISSING_DOMAIN_EXCLUSION_OR_VALUE
- `HR8264729_4_source_shadow`: MISSING_SOURCE_SHADOW_BAN_OR_VALUE
- `HR8264729_5_block_weight`: MISSING_EXCHANGE_CONNECTIVITY_OR_BLOCK_VALUE
- `HR8264729_6_extra_mass`: MISSING_EXTRA_CHANNEL_ZERO_OR_VALUE
- `HR8264729_7_acceptance`: FALSE_NOW

## Gates

- `GATE4729_0_sources_verified`: NONE
- `GATE4729_1_inventory_written`: INVENTORY_ONLY_NOT_CLAIM
- `GATE4729_2_exhaustion_signed`: EXHAUSTION_UNSIGNED
- `GATE4729_3_hidden_scalar_target_excluded`: HIDDEN_TARGET_UNSIGNED
- `GATE4729_4_readout_domain_targets_excluded`: READOUT_DOMAIN_UNSIGNED
- `GATE4729_5_source_shadow_block_closed`: SOURCE_CHANNELS_LIVE
- `GATE4729_6_HR826_bound_sourced`: HR826_VALUES_MISSING
- `GATE4729_7_B826_claim_row_ready`: B826_NONCLAIM

## Decision

`R826_OBJECT_LANGUAGE_INVENTORY_WRITTEN_EXHAUSTION_UNSIGNED_FIRST_HR826_HOM_BOUND_ROW_CREATED_NONCLAIM`

## Next Target

`4730-Y5-R2FR-HR826-hidden-scalar-target-exclusion-or-first-bound-input-pack.md`
