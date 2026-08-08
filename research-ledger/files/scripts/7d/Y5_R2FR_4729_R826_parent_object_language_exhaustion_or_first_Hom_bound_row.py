from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4729"
CLAIM_ID = "L-571"
MARKER = "PPC4161_R826_PARENT_OBJECT_LANGUAGE_EXHAUSTION_OR_FIRST_HOM_BOUND_ROW_4729"
PACKET_MARKER = "PPC4161_PACKET_R826_PARENT_OBJECT_LANGUAGE_EXHAUSTION_OR_FIRST_HOM_BOUND_ROW_4729"
DECISION = "R826_OBJECT_LANGUAGE_INVENTORY_WRITTEN_EXHAUSTION_UNSIGNED_FIRST_HR826_HOM_BOUND_ROW_CREATED_NONCLAIM"
NEXT_TARGET = "4730-Y5-R2FR-HR826-hidden-scalar-target-exclusion-or-first-bound-input-pack.md"

DOC_PATH = POST / "4729-Y5-R2FR-R826-parent-object-language-exhaustion-or-first-Hom-bound-row.md"
FORMAL_PATH = FORMAL / "745-PPC4161-R826-parent-object-language-exhaustion-or-first-Hom-bound-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4729_SOURCE_REGISTER.csv"
INVENTORY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4729_R826_PARENT_OBJECT_INVENTORY.csv"
EXHAUSTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4729_R826_EXHAUSTION_THEOREM.csv"
HOM_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4729_FIRST_HR826_HOM_BOUND_ROW.csv"
B826_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4729_HR826_TO_B826_BOUND_PROPAGATION.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4729_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4729_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4729_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4729_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4729_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4729_VALIDATION.csv"


SOURCE_SPECS = [
    ("SRC4729_0", POST / "CURRENT_LOCAL_RESUME.md", "4729-Y5-R2FR-R826-parent-object-language-exhaustion-or-first-Hom-bound-row.md", "4728 handoff target."),
    ("SRC4729_1", POST / "4728-Y5-R2FR-B826-no-source-slot-common-measure-proof-or-root-coercivity-bound.md", "parent object language", "4728 frames object-language exhaustion as the next blocker."),
    ("SRC4729_2", SOURCE_DIR / "P8_Y5_R2FR_4728_NEXT_TARGET.csv", "4729-Y5-R2FR-R826-parent-object-language-exhaustion-or-first-Hom-bound-row.md", "machine handoff into 4729."),
    ("SRC4729_3", SOURCE_DIR / "P8_Y5_R2FR_4728_R826_NO_SOURCE_SLOT_THEOREM.csv", "NS4728_2_absent_target", "4728 no-target theorem."),
    ("SRC4729_4", SOURCE_DIR / "P8_Y5_R2FR_4728_COMMON_MEASURE_CLAUSE_AUDIT.csv", "CLAUSE4728_0_parent_object_language", "4728 clause audit."),
    ("SRC4729_5", SOURCE_DIR / "P8_Y5_R2FR_4728_R826_COUNTERMODEL_AND_BOUND_ROWS.csv", "CMB4728_4_B826_bound", "4728 first Hom bound demand."),
    ("SRC4729_6", SOURCE_DIR / "P8_Y5_R2FR_4704_PARENT_GENERATOR_OBJECT_LANGUAGE.csv", "OBJ4704_0_parent_Maxwell_norm", "parent generator/object-language pattern."),
    ("SRC4729_7", SOURCE_DIR / "P8_Y5_R2FR_4704_VISIBLE_IMAGE_PROOF_ATTEMPT.csv", "VIP4704_3_reduced_exact_bottleneck", "visible image/exhaustion bottleneck."),
    ("SRC4729_8", SOURCE_DIR / "P8_Y5_R2FR_4704_CLAIM_BLOCKERS.csv", "BLK4704_0_parent_scalar_functional_exhaustion", "parent scalar-functional exhaustion blocker."),
    ("SRC4729_9", SOURCE_DIR / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv", "ODT2659_1_exact_typed_theorem", "exact typed no-Hom theorem."),
    ("SRC4729_10", SOURCE_DIR / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_COUNTERMODEL_LEDGER.csv", "CM2659_5_post_readout_selector", "no-Hom countermodels."),
    ("SRC4729_11", SOURCE_DIR / "P8_Y5_HOM_EXCLUSION_GATE_2613_HOM_EXCLUSION_THEOREM_ATTEMPT.csv", "HOM2613_1_conditional_meta_theorem", "no-source-only Hom meta-theorem."),
    ("SRC4729_12", SOURCE_DIR / "P8_Y5_HOM_EXCLUSION_GATE_2613_INVARIANT_ALGEBRA_HOM_AUDIT.csv", "IH2613_7_verdict", "invariant algebra generator debts."),
    ("SRC4729_13", SOURCE_DIR / "P8_Y5_SOURCE_PREF_OBJECTLANG_2650_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_ATTEMPT.csv", "NSP2650_1_exact_if_grammar_signed", "source-prefactor object-language theorem."),
    ("SRC4729_14", SOURCE_DIR / "P8_Y5_SOURCE_PREF_OBJECTLANG_2650_SOURCE_PREFACTOR_TYPING_GATE.csv", "TYP2650_1_no_species_to_source_coeff", "typing gate for coefficient targets."),
    ("SRC4729_15", SOURCE_DIR / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NO_SOURCE_PREFACTOR_PROOF_ATTEMPT.csv", "NSP2615_1_same_action_filter", "same-action filter."),
    ("SRC4729_16", SOURCE_DIR / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv", "THO2615_3_source_shadow_ban", "source-shadow ban contract."),
    ("SRC4729_17", SOURCE_DIR / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv", "NEC2615_2_weight_collapse", "Noether exchange collapse theorem."),
    ("SRC4729_18", SOURCE_DIR / "P8_Y5_R2FR_4707_FACTORIZATION_SIGNATURE_AUDIT.csv", "FSIG4707_3_no_hidden_visible_F2", "factorization signature audit."),
    ("SRC4729_19", SOURCE_DIR / "P8_Y5_R2FR_4708_RADIOUT_NATURALITY_THEOREM_ROWS.csv", "RRN4708_1_observed_readout_zero", "readout naturality theorem."),
    ("SRC4729_20", SOURCE_DIR / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv", "T509_2_no_extra_mass_channel", "source-measure extra-channel guard."),
    ("SRC4729_21", SOURCE_DIR / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_2_MTS_transfer_condition", "worldtube transfer condition."),
    ("SRC4729_22", SOURCE_DIR / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv", "HSM541_4_zero_extra_source_channels", "Hamiltonian source-measure extra-channel contract."),
    ("SRC4729_23", SOURCE_DIR / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_RESIDUAL_INPUTS.csv", "HSI541_3_mu_extra_vector", "extra source channel residual inputs."),
    ("SRC4729_24", SOURCE_DIR / "P8_Y5_R2FR_4727_FIRST_B826_FINITE_SOURCE_ROW.csv", "B8264727_0_master", "B826 finite source row."),
    ("SRC4729_25", SOURCE_DIR / "P8_Y5_R2FR_4728_ROOT_COHERCIVITY_BRIDGE_ROWS.csv", "RCB4728_3_B826_insert", "B826 root-coercivity insertion."),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    separator = "\n\n" if existing and not existing.endswith("\n\n") else ""
    write_text(path, existing + separator + block.rstrip() + "\n")


def source_path(source_id: str) -> str:
    for row_id, path, _needle, _role in SOURCE_SPECS:
        if row_id == source_id:
            return str(path)
    raise KeyError(source_id)


def source_register(ts: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
    return rows


def inventory_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("INV4729_0_q_obs_geometry", "allowed", "q_obs(Phi), e_obs/g_obs and fixed local branch data", "R826 may depend on observed quotient geometry.", "ALLOWED_QBASIC", "SRC4729_3"),
        ("INV4729_1_fixed_representation", "allowed", "theta_fixed, fixed representation constants, fixed calibration convention", "Fixed data can appear without vertical derivative.", "ALLOWED_IF_FIXED", "SRC4729_18"),
        ("INV4729_2_common_measure", "allowed_if_parent_signed", "one common source/action measure after variation", "Common measure is allowed only if it is not a pre-variation hidden/source selector.", "CONDITIONAL_COMMON_MEASURE", "SRC4729_20"),
        ("INV4729_3_hidden_scalar_target", "forbidden_if_exhausted", "I_hid or representative hidden scalar into R826 coefficient", "Would create D_v R826 and keep B826 live.", "FORBIDDEN_TARGET_UNSIGNED", "SRC4729_6"),
        ("INV4729_4_readout_target", "forbidden_if_exhausted", "ReadoutSelector/apparatus/material map into R826 coefficient", "Would re-enter after the parent action unless readout naturality signs.", "FORBIDDEN_TARGET_UNSIGNED", "SRC4729_19"),
        ("INV4729_5_domain_boundary_target", "forbidden_if_exhausted", "BoundaryClass, WorldtubeMask, support/domain selector into R826", "Would move the source slot into a domain/boundary coefficient.", "FORBIDDEN_TARGET_UNSIGNED", "SRC4729_21"),
        ("INV4729_6_source_shadow_target", "forbidden_if_exhausted", "separate source-shadow functional or non-Hilbert source current", "Same-action filter helps, but source-shadow ban is not parent-signed.", "FORBIDDEN_TARGET_UNSIGNED", "SRC4729_16"),
        ("INV4729_7_block_weight_target", "finite_if_survives", "disconnected source/exchange block weight", "Noether collapse reduces arbitrary species weights to block weights, but block connectivity is unsigned.", "FINITE_BLOCK_WEIGHT_SURVIVES", "SRC4729_17"),
        ("INV4729_8_extra_mass_channel", "finite_if_survives", "Delta_nonEH, Delta_extra, Delta_PiM, Delta_frame, Delta_boundary", "Mass/source channels can carry R826-like source dependence unless zeroed or bounded.", "EXTRA_CHANNELS_SURVIVE", "SRC4729_22"),
        ("INV4729_9_verdict", "decision", "R826 parent object inventory", "Allowed/forbidden inventory is now explicit; exhaustion itself is not signed.", "INVENTORY_WRITTEN_EXHAUSTION_UNSIGNED", "SRC4729_4"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "inventory_id": inventory_id,
            "role": role,
            "object_or_sort": obj,
            "meaning": meaning,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for inventory_id, role, obj, meaning, status, source_id in specs
    ]


def exhaustion_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("EXH4729_0_exact_statement", "R826 object-language exhaustion", "Allowed_R826 = q^*A_Q plus A_fixed plus parent-signed common measure; Forbidden_R826 = hidden scalar, readout/material, boundary/domain, source-shadow and extra mass-channel targets.", "If this inventory is parent-signed, D_v R826=0 for v in ker(Dq_obs).", "EXACT_CONDITIONAL_THEOREM", "SRC4729_9"),
        ("EXH4729_1_chain_rule", "q-basic component", "D_v Rbar_826(q_obs,theta_fixed)=0", "Ordinary chain rule closes the allowed component.", "DERIVED_CHAIN_RULE", "SRC4729_3"),
        ("EXH4729_2_absent_target", "forbidden target component", "No Hom(H_hidden/readout/domain/source-shadow, Coeff_R826) except CommonConst.", "This removes nonconstant vertical maps by typing.", "NO_HOM_CONDITIONAL", "SRC4729_11"),
        ("EXH4729_3_same_action_filter", "source-shadow filter", "R826 cannot be generated from a source-only functional that is not in S_matter before variation.", "Same-action principle blocks shadow source duplication if parent grammar signs it.", "PARTIAL_FILTER_DERIVED", "SRC4729_15"),
        ("EXH4729_4_exchange_block_filter", "block-weight refinement", "Bianchi/Noether exchange collapses relative weights inside connected exchange components.", "This reduces possible source targets but does not prove one connected ordinary block.", "DERIVED_REFINEMENT_NOT_EXHAUSTION", "SRC4729_17"),
        ("EXH4729_5_exhaustion_verdict", "claim verdict", "Current evidence does not prove parent object-language exhaustion for R826.", "The zero proof remains exact conditional; finite Hom row is required.", "EXHAUSTION_NOT_SIGNED", "SRC4729_8"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "target": target,
            "statement": statement,
            "meaning": meaning,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for theorem_id, target, statement, meaning, status, source_id in specs
    ]


def hom_bound_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("HR8264729_0_total", "H_R826_total", "sup_local |D_v R_826|", "H_hidden_R826 + H_readout_R826 + H_domain_R826 + H_source_shadow_R826 + H_block_R826 + H_extra_mass_R826 + H_rad_R826", "R826 derivative norm", "MISSING_COMPONENT_VALUES", "SRC4729_5"),
        ("HR8264729_1_hidden_scalar", "H_hidden_R826", "sup |D_v R_hidden(I_hid)|", "0 if no hidden scalar target signs; otherwise source numeric/symbolic bound.", "R826 derivative norm", "MISSING_HIDDEN_TARGET_EXCLUSION_OR_VALUE", "SRC4729_10"),
        ("HR8264729_2_readout", "H_readout_R826", "sup |D_v delta_R_readout|", "0 if readout naturality signs; otherwise finite readout/apparatus/material row.", "R826 derivative norm", "MISSING_READOUT_NATURALITY_OR_VALUE", "SRC4729_19"),
        ("HR8264729_3_domain", "H_domain_R826", "sup |D_v delta_R_domain|", "0 if boundary/domain/worldtube target exclusion signs; otherwise finite domain/source-support row.", "R826 derivative norm", "MISSING_DOMAIN_EXCLUSION_OR_VALUE", "SRC4729_21"),
        ("HR8264729_4_source_shadow", "H_source_shadow_R826", "sup |D_v delta_R_source_shadow|", "0 if same-action source-shadow ban signs; otherwise finite non-Hilbert/source-current row.", "R826 derivative norm", "MISSING_SOURCE_SHADOW_BAN_OR_VALUE", "SRC4729_16"),
        ("HR8264729_5_block_weight", "H_block_R826", "sup |D_v delta_R_block|", "0 if ordinary matter is one connected exchange block; otherwise finite block-weight row.", "R826 derivative norm", "MISSING_EXCHANGE_CONNECTIVITY_OR_BLOCK_VALUE", "SRC4729_17"),
        ("HR8264729_6_extra_mass", "H_extra_mass_R826", "sup |D_v delta_R_extra_mass|", "0 if extra mass/source channels vanish; otherwise finite Delta_extra channel vector.", "R826 derivative norm", "MISSING_EXTRA_CHANNEL_ZERO_OR_VALUE", "SRC4729_23"),
        ("HR8264729_7_acceptance", "valid_for_claim", "claim switch for H_R826_total", "true only if all component zeros are parent-signed or all component values are source-backed with units.", "boolean", "FALSE_NOW", "SRC4729_5"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "definition": definition,
            "bound_or_formula": formula,
            "units": units,
            "current_status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for row_id, quantity, definition, formula, units, status, source_id in specs
    ]


def b826_bound_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("BPROP4729_0_Rm_bound", "R_m", "|R_m| <= H_R826_total + C_root(|J_root|+|B_root|+|Pi_coker R_826|)", "combines Hom object-language failure with root-coercivity fallback", "SRC4729_25"),
        ("BPROP4729_1_B826_bound", "B_826", "|B_826| <= |a_F| L_cg^-2 [H_R826_total + C_root(|J_root|+|B_root|+|Pi_coker R_826|)]", "first usable finite B826 source-bound formula once rows are sourced", "SRC4729_24"),
        ("BPROP4729_2_Bmem_insert", "B_mem_eff", "|B_mem_eff| <= |B_826| + |B_Weyl| + |B_Y5| + |B_Y6| + |B_boundary| + |B_readout|", "B826 is only one component; no cancellation with other components", "SRC4729_5"),
        ("BPROP4729_3_next", "next data need", "fill HR8264729_1 hidden scalar target exclusion/value first", "hidden scalar target is the first and cleanest parent object-language fork", "SRC4729_6"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "propagation_id": propagation_id,
            "target": target,
            "formula": formula,
            "meaning": meaning,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for propagation_id, target, formula, meaning, source_id in specs
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4729_0_sources_verified", "All 4729 source paths exist and needles are found.", True, "NONE"),
        ("GATE4729_1_inventory_written", "R826 allowed/forbidden object inventory is written.", True, "INVENTORY_ONLY_NOT_CLAIM"),
        ("GATE4729_2_exhaustion_signed", "R826 parent object language is exhausted by q-basic/fixed/common-measure data.", False, "EXHAUSTION_UNSIGNED"),
        ("GATE4729_3_hidden_scalar_target_excluded", "Hidden scalar target into R826 is parent-forbidden.", False, "HIDDEN_TARGET_UNSIGNED"),
        ("GATE4729_4_readout_domain_targets_excluded", "Readout/domain/worldtube targets into R826 are parent-forbidden.", False, "READOUT_DOMAIN_UNSIGNED"),
        ("GATE4729_5_source_shadow_block_closed", "source-shadow, block-weight and extra mass channels are zero or bounded.", False, "SOURCE_CHANNELS_LIVE"),
        ("GATE4729_6_HR826_bound_sourced", "H_R826 components are source-backed or theorem-zero.", False, "HR826_VALUES_MISSING"),
        ("GATE4729_7_B826_claim_row_ready", "B826 is zero or finite-bound claim-grade.", False, "B826_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "condition": condition,
            "passed": passed,
            "blocker": blocker,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for gate_id, condition, passed, blocker in specs
    ]


def firewall_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4729_0_inventory_not_signature", "An object inventory is not a parent signature; do not promote exhaustion from listing allowed/forbidden sorts."),
        ("FW4729_1_no_syntax_by_decree", "Do not forbid hidden/readout/domain targets by notation only; source a parent grammar clause or keep H_R826."),
        ("FW4729_2_no_same_action_overreach", "Same-action filtering does not exclude disconnected real matter subactions or source-shadow functionals by itself."),
        ("FW4729_3_no_exchange_graph_overreach", "Noether exchange collapse kills weights only on connected exchange components; disconnected blocks survive."),
        ("FW4729_4_no_common_measure_smuggle", "Common measure cannot replace source/worldtube/boundary/domain proof."),
        ("FW4729_5_no_component_cancellation", "Do not cancel H_R826 components or Bmem components against one another without a parent identity."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for firewall_id, rule in specs
    ]


def decision_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derivation_result": "R826 object-language exhaustion is now an exact conditional theorem with explicit allowed and forbidden targets",
            "nonclaim_result": "hidden scalar, readout/domain, source-shadow, block-weight and extra mass-channel exclusions remain unsigned",
            "finite_row_result": "first H_R826_total Hom-bound row and propagation to |B826| are created nonclaim",
            "local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": ts,
        }
    ]


def status_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4729_0_local_only",
            "status": "local_files_only_no_github_action",
            "detail": "Generated under post-checkpoint-work and formalization-workbench only.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4729_1_science_verdict",
            "status": "R826_inventory_written_HR826_bound_created",
            "detail": "The branch moved from broad object-language blocker to explicit H_R826 component rows.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "The first live H_R826 component is the hidden scalar target. Either prove parent object language excludes I_hid -> R826, or fill H_hidden_R826 as the first bound input.",
            "first_task": "Attempt hidden-scalar target exclusion for R826 using no-Hom/object-language exhaustion.",
            "fallback_task": "Create the first source-backed H_hidden_R826 bound input row with units and assumptions.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    ts: str,
    inventory: list[dict[str, Any]],
    exhaustion: list[dict[str, Any]],
    hom_bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4729 - R826 Parent Object-Language Exhaustion or First Hom Bound Row

Generated: `{ts}`

## Purpose

4729 attacks the object-language fork created by 4728: either parent-sign the allowed/forbidden arguments of `R_826`, or create the first finite `H_R826` Hom-bound row.

## What Actually Moved

- The `R_826` parent object inventory is now explicit.
- Allowed objects are `q_obs` geometry, fixed representation data, and a parent-signed common measure.
- Forbidden targets are hidden scalar, readout/material, boundary/domain, source-shadow, disconnected block-weight and extra mass/source channels.
- Exhaustion is not signed: the current corpus gives theorem shape and filters, not a complete parent object-language proof.
- The first finite row now exists: `H_R826_total = H_hidden_R826 + H_readout_R826 + H_domain_R826 + H_source_shadow_R826 + H_block_R826 + H_extra_mass_R826 + H_rad_R826`.

## Object Inventory

{bullets(inventory, "inventory_id", "status")}

## Exhaustion Theorem

{bullets(exhaustion, "theorem_id", "status")}

## First Hom Bound Row

{bullets(hom_bounds, "row_id", "current_status")}

## Gates

{bullets(gates, "gate_id", "blocker")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 745 - R826 Parent Object-Language Exhaustion or First Hom Bound Row

Generated: `{ts}`

## Result

The exact exhaustion theorem is now written as:

`Allowed_R826 = q^*A_Q + A_fixed + parent-signed common measure`.

Every nonconstant map from hidden scalar, readout/material, boundary/domain, source-shadow, disconnected block-weight or extra mass/source channels into `R_826` must be parent-forbidden. Current evidence does not sign that exhaustion.

## Finite Fallback

`H_R826_total = H_hidden_R826 + H_readout_R826 + H_domain_R826 + H_source_shadow_R826 + H_block_R826 + H_extra_mass_R826 + H_rad_R826`.

Then

`|B_826| <= |a_F| L_cg^-2 [H_R826_total + C_root(|J_root|+|B_root|+|Pi_coker R_826|)]`.

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(ts: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Derivation gain: the `R_826` object-language fork is now explicit: allowed q-basic/fixed/common-measure arguments versus forbidden hidden/readout/domain/source-shadow/block/extra-channel targets.
- Finite row: `H_R826_total` component bound row and propagation into `|B_826|` are staged nonclaim.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: converts parent object-language exhaustion from a broad blocker into explicit `H_R826` component rows and a concrete next hidden-scalar target exclusion/bound fork.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{ts}`

## Latest completed checkpoint

`{DOC_PATH.name}`

## Decision

`{DECISION}`

## What moved forward

- The `R_826` parent object inventory is explicit.
- Exhaustion remains unsigned, but the first finite `H_R826_total` Hom-bound row now exists.
- The bound propagates into `|B_826| <= |a_F| L_cg^-2 [H_R826_total + root-coercive tail]`.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def add_claim_once(ts: str) -> None:
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_bridge",
        "claim": "4729 writes the R826 parent object inventory and creates the first H_R826 Hom-bound row; object-language exhaustion remains unsigned, so B826 is nonclaim.",
        "current_evidence": "Generated source register, R826 parent object inventory, exhaustion theorem rows, first H_R826 Hom-bound row, H_R826-to-B826 propagation, gates, firewalls, decision, status, next target and validation.",
        "status": "R826_inventory_written_HR826_bound_created_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating an inventory or same-action filter as a parent-signed exclusion of hidden/readout/domain/source targets.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "H_R826 hidden/readout/domain/source-shadow/block/extra-channel components remain unsourced or unsigned.",
        "title": "R826 parent object-language exhaustion or first Hom bound row",
        "notes": f"{MARKER}; {DECISION}; generated {ts}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def parse_csv(path: Path) -> bool:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def validation_rows(
    sources: list[dict[str, Any]],
    inventory: list[dict[str, Any]],
    exhaustion: list[dict[str, Any]],
    hom_bounds: list[dict[str, Any]],
    b826_bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    ts: str,
) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER_CSV,
        INVENTORY_CSV,
        EXHAUSTION_CSV,
        HOM_BOUND_CSV,
        B826_BOUND_CSV,
        GATES_CSV,
        FIREWALL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_TARGET_CSV,
    ]
    inventory_status = ";".join(row["status"] for row in inventory)
    exhaustion_status = ";".join(row["status"] for row in exhaustion)
    hom_status = ";".join(row["current_status"] for row in hom_bounds)
    b826_formula = ";".join(row["formula"] for row in b826_bounds)
    checks = [
        ("VAL4729_0_sources_exist", all(bool(row["exists"]) for row in sources), "all cited 4729 source paths exist"),
        ("VAL4729_1_needles_found", all(bool(row["needle_found"]) for row in sources), "all cited 4729 source needles found"),
        ("VAL4729_2_inventory_written", "ALLOWED_QBASIC" in inventory_status and "FORBIDDEN_TARGET_UNSIGNED" in inventory_status, "allowed and forbidden R826 object inventory rows written"),
        ("VAL4729_3_exhaustion_not_promoted", "EXACT_CONDITIONAL_THEOREM" in exhaustion_status and "EXHAUSTION_NOT_SIGNED" in exhaustion_status, "exhaustion theorem is conditional and not promoted"),
        ("VAL4729_4_first_HR826_row_created", "MISSING_COMPONENT_VALUES" in hom_status and "MISSING_HIDDEN_TARGET_EXCLUSION_OR_VALUE" in hom_status, "first H_R826 Hom-bound row and hidden component row created"),
        ("VAL4729_5_B826_propagation_written", "H_R826_total" in b826_formula and "|B_826|" in b826_formula, "H_R826 bound propagates to B826"),
        ("VAL4729_6_claim_gates_closed", all(not bool(row["claim_allowed"]) for row in gates) and not any(row["passed"] for row in gates if row["gate_id"] not in {"GATE4729_0_sources_verified", "GATE4729_1_inventory_written"}), "all broad claim gates remain closed; inventory gate is not claim"),
        ("VAL4729_7_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4729_8_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4729_9_claim_row_added", CLAIM_ID in read_text(CLAIMS_PATH), "claims register contains L-571"),
        ("VAL4729_10_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4730 next target"),
        ("VAL4729_11_csv_parse", all(parse_csv(path) for path in csv_paths), "all generated 4729 CSV files parse cleanly"),
        ("VAL4729_12_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
    ]
    overall = all(result for _check_id, result, _detail in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "timestamp_utc": ts,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4729_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "4729 R826 parent object-language exhaustion or first Hom-bound validation",
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()
    cleanup_pycache()
    sources = source_register(ts)
    inventory = inventory_rows(ts)
    exhaustion = exhaustion_rows(ts)
    hom_bounds = hom_bound_rows(ts)
    b826_bounds = b826_bound_rows(ts)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(INVENTORY_CSV, inventory)
    write_csv(EXHAUSTION_CSV, exhaustion)
    write_csv(HOM_BOUND_CSV, hom_bounds)
    write_csv(B826_BOUND_CSV, b826_bounds)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(ts, inventory, exhaustion, hom_bounds, gates)
    update_spine_packet_resume(ts)
    add_claim_once(ts)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, inventory, exhaustion, hom_bounds, b826_bounds, gates, ts))


if __name__ == "__main__":
    main()
