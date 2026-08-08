from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3813"
BRANCH = "MTS_R2FR_Y5_RBRIDGE_MATTER_GLUE_NO_SOURCE_SLOT_OR_FINITE_SOURCE_NORMALIZER_ROW_3813"
PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
MICRO = PCW / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
DOC_PATH = PCW / "3813-Y5-R2FR-Rbridge-matter-glue-no-source-slot-or-finite-source-normalizer-row.md"
SCRIPT_PATH = PCW / "scripts" / "Y5_R2FR_3813_Rbridge_matter_glue_no_source_slot_or_finite_source_normalizer_row.py"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3812 = PCW / "3812-Y5-R2FR-parent-transport-source-normalizer-or-same-vector-DD-branch-bridge.md"
P_3488 = PCW / "3488-Y5-R2FR-no-source-only-matter-grammar-or-finite-Jq-coefficient-row.md"
P_3489 = PCW / "3489-Y5-R2FR-connected-matter-category-certificate-or-Jspurion-bound-source.md"
P_3490 = PCW / "3490-Y5-R2FR-species-blind-measure-current-owner-or-product-bound-upgrade.md"
P_2677 = PCW / "2677-Y5-R2FR-no-species-action-weight-object-language-or-wA-JA-bound.md"

CSV_3812_RBRIDGE = OUT / "P8_Y5_R2FR_3812_RBRIDGE_RESIDUAL_CARRYFORWARD.csv"
CSV_3812_NEXT = OUT / "P8_Y5_R2FR_3812_NEXT_TARGET.csv"
CSV_3475_MATRIX = OUT / "P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv"
CSV_3488_PROOF = OUT / "P8_Y5_R2FR_3488_CONDITIONAL_NO_SOURCE_PROOF.csv"
CSV_3488_FINITE = OUT / "P8_Y5_R2FR_3488_FINITE_JSPURION_COEFFICIENT_ROWS.csv"
CSV_3489_CERT = OUT / "P8_Y5_R2FR_3489_CERTIFICATE_LEDGER.csv"
CSV_3489_JSP = OUT / "P8_Y5_R2FR_3489_JSPURION_PRODUCT_BOUND_ROWS.csv"
CSV_3490_THEOREM = OUT / "P8_Y5_R2FR_3490_THEOREM_LEDGER.csv"
CSV_3490_PRODUCTS = OUT / "P8_Y5_R2FR_3490_MEASURE_CURRENT_PRODUCT_BOUNDS.csv"
CSV_1452_COMMON = MICRO / "common_measure_current_theorem_attempt_1452.csv"
CSV_1461_SOURCE = MICRO / "C_parent_WEP_source_factorization_signing_decision_1461.csv"
CSV_1464_CONNECTED = MICRO / "connected_matter_category_proof_attempt_1464.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3813_SOURCE_REGISTER.csv",
    "zero_contract": OUT / "P8_Y5_R2FR_3813_MATTER_GLUE_ZERO_THEOREM_CONTRACT.csv",
    "decomposition": OUT / "P8_Y5_R2FR_3813_RMATTER_GLUE_DECOMPOSITION.csv",
    "product_bounds": OUT / "P8_Y5_R2FR_3813_SOURCE_PRODUCT_BOUND_ROWS.csv",
    "visible_map": OUT / "P8_Y5_R2FR_3813_RVISIBLE_COEFF_GLUE_MAP.csv",
    "updates": OUT / "P8_Y5_R2FR_3813_RESIDUAL_STATUS_UPDATES.csv",
    "gates": OUT / "P8_Y5_R2FR_3813_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3813_DECISION_ROWS.csv",
    "next_target": OUT / "P8_Y5_R2FR_3813_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3813_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3813_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3813_0_3812_doc", P_3812, "Attack the source-ownership bottleneck", "3812 selected R_bridge matter-glue source ownership as next target"),
    ("SRC3813_1_3488_doc", P_3488, "connected ordinary-matter category", "3488 conditional no-source-only matter grammar"),
    ("SRC3813_2_3489_doc", P_3489, "PRODUCT_BOUNDED_NOT_ISOLATED", "3489 connected graph certificate and J_spurion product bounds"),
    ("SRC3813_3_3490_doc", P_3490, "epsilon_species_measure", "3490 species-blind measure/current owner and product bounds"),
    ("SRC3813_4_2677_doc", P_2677, "No Species Action Weight", "2677 root object-language audit"),
    ("SRC3813_5_3812_rbridge", CSV_3812_RBRIDGE, "RBC3812_R_matter_glue", "3812 R_bridge residual carryforward"),
    ("SRC3813_6_3812_next", CSV_3812_NEXT, "3813-Y5-R2FR-Rbridge-matter-glue-no-source-slot-or-finite-source-normalizer-row.md", "3812 machine handoff"),
    ("SRC3813_7_3475_matrix", CSV_3475_MATRIX, "MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10", "WEP bound rows for finite source-product residuals"),
    ("SRC3813_8_3488_proof", CSV_3488_PROOF, "NSG3488_2_connected_naturality", "conditional no-source theorem proof rows"),
    ("SRC3813_9_3488_finite", CSV_3488_FINITE, "epsilon_source_reentry", "finite fallback coefficients including source reentry"),
    ("SRC3813_10_3489_cert", CSV_3489_CERT, "CERT3489_1_parent_graph_owner", "parent graph ownership status"),
    ("SRC3813_11_3489_jsp", CSV_3489_JSP, "JSPB3489_0_MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10", "J_spurion source-product bounds"),
    ("SRC3813_12_3490_theorem", CSV_3490_THEOREM, "THM3490_0_common_measure_owner_conditional", "common measure/current conditional theorem"),
    ("SRC3813_13_3490_products", CSV_3490_PRODUCTS, "MEASB3490_epsilon_species_measure_0_MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10", "measure/current source-product bounds"),
    ("SRC3813_14_1452_common", CSV_1452_COMMON, "CMT1452_0_target", "common measure/current owner proof attempt"),
    ("SRC3813_15_1461_source", CSV_1461_SOURCE, "SIGN1461_0_source_factorization", "source-label forgetting signing decision"),
    ("SRC3813_16_1464_connected", CSV_1464_CONNECTED, "CON1464_1_naturality_lemma", "connected category naturality lemma"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def zero_contract_rows(timestamp: str) -> list[dict[str, Any]]:
    clauses = [
        (
            "ZC3813_0_single_action_density_line",
            "ordinary matter is represented by one parent action-density line and one common action scale",
            "independent w_A(q), hbar_A(q), or sector action-scale slots",
            "relative species action weights vanish; any common scalar is not a WEP composition contrast",
            "3488/2677 conditional target; 1452 says owner not parent-signed",
            "unsigned",
        ),
        (
            "ZC3813_1_connected_naturality",
            "ordinary matter category is connected by parent-owned nonzero morphisms on the action-density/source functor",
            "disconnected component source weights",
            "naturality forces w_B F(f)=F(f) w_A, hence w_A=w_B across ordinary matter",
            "1464 exact naturality lemma plus 3489 template connected graph",
            "conditional_exact_graph_owner_unsigned",
        ),
        (
            "ZC3813_2_species_blind_measure",
            "parent measure/current normalization is species-blind and varied before readout",
            "species Jacobian J_A and current-rescaling c_A slots",
            "Delta ln J_AB=0 and Delta ln c_AB=0 for ordinary species pairs",
            "3490 common measure/current theorem target",
            "unsigned",
        ),
        (
            "ZC3813_3_hilbert_current_owner",
            "the local matter source is the Hilbert variation of the common matter action before source/readout selectors",
            "species-dependent non-Hilbert bypass zeta_A J_NH,A",
            "epsilon_nonHilbert_current=0",
            "3490 Hilbert-current conditional subtheorem",
            "unsigned",
        ),
        (
            "ZC3813_4_source_label_forgetting",
            "source/readout functor forgets species labels before source normalization and boundary/domain sectors do not reintroduce them",
            "post-quotient source-label reentry and source-only spurions",
            "epsilon_source_reentry=0 and the source-only part of R_visible_coeff is removed",
            "3488/1461 source-label forgetting dependency",
            "unsigned",
        ),
        (
            "ZC3813_5_zero_theorem_result",
            "all zero-contract clauses hold simultaneously",
            "R_matter_glue source-only residual and R_visible_coeff source-only residual",
            "R_matter_glue^AB=0 and R_visible_coeff^source-only=0, leaving DD composition charges and universal R_G_kappa separate",
            "new 3813 fused theorem from 3488-3490",
            "theorem_constructed_not_parent_signed",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "clause_id": clause_id,
            "premise": premise,
            "forbids": forbids,
            "effect_if_signed": effect,
            "source_basis": basis,
            "current_status": status,
            "valid_for_claim": "false",
        }
        for clause_id, premise, forbids, effect, basis, status in clauses
    ]


def decomposition_rows(timestamp: str) -> list[dict[str, Any]]:
    pieces = [
        (
            "RMG3813_0_J_spurion",
            "epsilon_J_spurion",
            "source/species prefactor contrast after quotient/readout",
            "R_matter_glue;R_visible_coeff",
            "single density line plus connected naturality plus source-label forgetting",
            "3489 product bounds",
            "PRODUCT_BOUNDED_NOT_ISOLATED",
        ),
        (
            "RMG3813_1_species_measure",
            "epsilon_species_measure",
            "species-dependent measure Jacobian contrast",
            "R_matter_glue",
            "species-blind parent measure/path measure",
            "3490 product bounds",
            "PRODUCT_BOUNDED_NOT_ISOLATED",
        ),
        (
            "RMG3813_2_current_rescaling",
            "epsilon_current_rescaling",
            "species/source-current normalization contrast",
            "R_matter_glue;R_readout_PPN",
            "common Hilbert source current varied before readout",
            "3490 product bounds",
            "PRODUCT_BOUNDED_NOT_ISOLATED",
        ),
        (
            "RMG3813_3_nonHilbert_current",
            "epsilon_nonHilbert_current",
            "species-dependent non-Hilbert source bypass",
            "R_visible_coeff;R_readout_PPN",
            "Hilbert current owner plus no non-Hilbert projected source",
            "3490 product bounds",
            "PRODUCT_BOUNDED_NOT_ISOLATED",
        ),
        (
            "RMG3813_4_source_reentry",
            "epsilon_source_reentry",
            "source/readout label reentry after quotienting",
            "R_projector;R_readout_PPN;R_visible_coeff",
            "source-label forgetting and boundary/domain no-reentry",
            "new 3813 WEP source-product rows",
            "PRODUCT_BOUNDED_NOT_ISOLATED",
        ),
        (
            "RMG3813_5_common_scalar",
            "w_common_or_kappa_common",
            "common ordinary-matter scalar after connectedness",
            "R_G_kappa;source normalization",
            "universal coupling/normalization owner",
            "not a WEP composition residual",
            "MOVED_OUT_OF_RMATTER_GLUE_IF_CONNECTED",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "residual_piece_id": piece_id,
            "symbol": symbol,
            "definition": definition,
            "feeds_residual": feeds,
            "zero_condition": zero_condition,
            "finite_fallback": fallback,
            "current_status": status,
            "valid_for_claim": "false",
        }
        for piece_id, symbol, definition, feeds, zero_condition, fallback, status in pieces
    ]


def wep_rows() -> list[dict[str, str]]:
    return [row for row in read_csv(CSV_3475_MATRIX) if row["row_type"] == "WEP_material_difference"]


def source_product_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    channel_specs = [
        ("epsilon_J_spurion", "R_matter_glue + R_visible_coeff", "source/species prefactor contrast", "3489"),
        ("epsilon_species_measure", "R_matter_glue", "species measure Jacobian contrast", "3490"),
        ("epsilon_current_rescaling", "R_matter_glue + R_readout_PPN", "source-current normalization contrast", "3490"),
        ("epsilon_nonHilbert_current", "R_visible_coeff + R_readout_PPN", "non-Hilbert source bypass contrast", "3490"),
        ("epsilon_source_reentry", "R_projector + R_readout_PPN + R_visible_coeff", "post-quotient source label reentry contrast", "3813_new"),
        ("R_matter_glue_total", "R_matter_glue", "total matter-glue source-product envelope under residual-isolation smoke branch", "3813_new"),
    ]
    rows: list[dict[str, Any]] = []
    for wep_index, row in enumerate(wep_rows()):
        for symbol, residual_slot, definition, source_basis in channel_specs:
            rows.append(
                {
                    "timestamp_utc": timestamp,
                    "branch_id": BRANCH,
                    "checkpoint_id": CHECKPOINT,
                    "product_bound_id": f"PB3813_{symbol}_{wep_index}_{row['aug_row_id']}",
                    "symbol": symbol,
                    "residual_slot": residual_slot,
                    "arena": row["arena"],
                    "observable_row": row["aug_row_id"],
                    "product_symbol": f"abs(S_E^q) * abs(Delta_{symbol}_AB)",
                    "bound_value": row["bound"],
                    "bound_units": row["bound_units"],
                    "derivation": f"If {definition} enters the WEP residual as eta_AB includes S_E^q Delta_{symbol}_AB, then the measured eta bound source-bounds this product. This does not isolate {symbol} without a lower bound on abs(S_E^q).",
                    "source_path": row["source_path"],
                    "source_basis": source_basis,
                    "isolates_coefficient": "false",
                    "valid_for_claim": "false",
                }
            )
    return rows


def visible_map_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "map_id": "RVC3813_0_source_only_visible_coeff",
            "visible_residual_piece": "source-only part of R_visible_coeff",
            "shares_zero_contract_with": "epsilon_J_spurion;epsilon_nonHilbert_current;epsilon_source_reentry",
            "zero_result_if_signed": "no independent source/species prefactor can masquerade as a visible coefficient leak",
            "remaining_visible_coeff_work": "EM-lock, mass-owner, alpha/readout and radiative coefficient routes remain separate from source-only matter glue",
            "current_status": "SOURCE_ONLY_COMPONENT_MAPPED_PRODUCT_BOUNDED_NOT_CLAIMED",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "map_id": "RVC3813_1_DD_charge_preservation",
            "visible_residual_piece": "DD composition charges Q_i^A",
            "shares_zero_contract_with": "not_zeroed",
            "zero_result_if_signed": "DD charges survive as representation-dependent mass/binding sensitivities, not source-only spurions",
            "remaining_visible_coeff_work": "parent map from DD charges to MTS q-current still requires R_bridge ownership",
            "current_status": "PRESERVED_NOT_DELETED",
            "valid_for_claim": "false",
        },
    ]


def updates_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "update_id": "UP3813_0_R_matter_glue",
            "residual": "R_matter_glue",
            "old_status": "CONDITIONAL_NOT_GLUED",
            "new_status": "ZERO_THEOREM_CONTRACT_BUILT_AND_SOURCE_PRODUCT_BOUNDED_NOT_ISOLATED",
            "evidence": "3813 zero contract plus PB3813 source-product rows",
            "claim_effect": "success gate met at product-bound level, but no local-GR/source-coupling claim",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "update_id": "UP3813_1_R_visible_coeff_source_only",
            "residual": "R_visible_coeff source-only component",
            "old_status": "GUARD_ONLY_RETAINED",
            "new_status": "SOURCE_ONLY_COMPONENT_MAPPED_TO_MATTER_GLUE_CONTRACT_AND_PRODUCT_BOUNDS",
            "evidence": "RVC3813 map plus epsilon_J_spurion/nonHilbert/source_reentry product rows",
            "claim_effect": "only source-only visible leakage is narrowed; EM/mass/readout coefficient owners remain separate",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "update_id": "UP3813_2_source_amplitude",
            "residual": "abs(S_E^q)",
            "old_status": "MISSING_PARENT_SOURCE_CURRENT_NORMALIZATION",
            "new_status": "NOW_THE_MAIN_ISOLATION_BOTTLENECK",
            "evidence": "all 3813 bounds constrain abs(S_E^q)*epsilon products, not isolated epsilons",
            "claim_effect": "next target should attack source-amplitude lower/normalization theorem",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(timestamp: str, grouped: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    product_bound_count = len(grouped["product_bounds"])
    source_reentry_rows = [row for row in grouped["product_bounds"] if row["symbol"] == "epsilon_source_reentry"]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": "GATE3813_0_zero_contract_constructed",
            "requirement": "write exact matter-glue/no-source-only zero theorem contract",
            "passed": "true",
            "evidence": "ZC3813 clauses fuse 3488 connected no-source theorem and 3490 common measure/current theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": "GATE3813_1_parent_premises_signed",
            "requirement": "single density line, parent graph ownership, species-blind measure, Hilbert current and source-label forgetting are parent-signed",
            "passed": "false",
            "evidence": "1452/1461/1464 signing ledgers keep these clauses unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": "GATE3813_2_source_product_bounds_created",
            "requirement": "finite source-product residual rows exist with units",
            "passed": bool_text(product_bound_count >= 12),
            "evidence": f"{product_bound_count} product rows from two WEP arenas and six residual channels",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": "GATE3813_3_source_reentry_new_bound",
            "requirement": "source-label reentry is no longer missing-only; it has WEP source-product rows",
            "passed": bool_text(len(source_reentry_rows) == 2),
            "evidence": "epsilon_source_reentry product rows are generated for MICROSCOPE and EotWash",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": "GATE3813_4_source_amplitude_isolates_residuals",
            "requirement": "parent-owned lower/nonzero theorem for abs(S_E^q) isolates residual coefficients",
            "passed": "false",
            "evidence": "all source-product rows explicitly keep isolates_coefficient=false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "decision_id": "DEC3813_0_zero_route",
            "decision": "Use the fused matter-glue zero contract as the exact theorem target.",
            "reason": "3488 proves the connected no-source theorem shape and 3490 proves the common measure/current shape; together they zero source-only matter glue if parent-signed.",
            "next_action": "try to sign source-amplitude/current normalization rather than rerunning WEP rank rows",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "decision_id": "DEC3813_1_finite_route",
            "decision": "Promote R_matter_glue from vague blocker to source-product-bounded residual.",
            "reason": "WEP eta bounds now constrain abs(S_E^q) times J_spurion, species-measure, current-rescaling, non-Hilbert, source-reentry and total matter-glue envelopes.",
            "next_action": "derive a lower/nonzero theorem for abs(S_E^q) or keep product-level residuals only",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "decision_id": "DEC3813_2_no_overclaim",
            "decision": "Do not claim local source coupling from 3813.",
            "reason": "The zero theorem is not parent-signed and the finite rows are products, not isolated coefficient bounds.",
            "next_action": "3814 should attack source-amplitude lower/normalization or worldtube current owner",
            "valid_for_claim": "false",
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_doc": "3814-Y5-R2FR-source-amplitude-lower-bound-or-worldtube-current-normalization-theorem.md",
            "target_script": "scripts/Y5_R2FR_3814_source_amplitude_lower_bound_or_worldtube_current_normalization_theorem.py",
            "objective": "Attack the isolation bottleneck exposed by 3813: derive a parent-owned lower/nonzero theorem or normalization rule for abs(S_E^q), preferably from the worldtube current definition and denominator, or state the exact finite residual product level that remains.",
            "success_gate": "A parent-owned source-amplitude lower/normalization theorem is produced, or the product-bound residual runner is upgraded so every source-product row has an explicit residual-isolation policy.",
            "avoid": "do not set S_E^q=1; do not isolate epsilon coefficients without a source-amplitude lower bound; do not edit formalization-workbench; do not use GitHub",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_RMATTER_GLUE_ZERO_CONTRACT_AND_SOURCE_PRODUCT_BOUNDS_BUILT",
            "summary": "3813 fuses the no-source-only matter grammar into an exact conditional zero theorem for R_matter_glue/R_visible_coeff source-only leakage, and creates finite WEP source-product bound rows for J_spurion, species measure, current rescaling, non-Hilbert current, source reentry, and total matter glue. This meets the product-bound success gate but does not isolate coefficients without abs(S_E^q).",
            "valid_for_claim": "false",
        }
    ]


def row_bullet(row: dict[str, Any], key_fields: list[str]) -> str:
    label = " ".join(f"`{row[field]}`" for field in key_fields if row.get(field))
    rest = "; ".join(
        f"{key}: {value}"
        for key, value in row.items()
        if key not in key_fields and key not in {"timestamp_utc", "branch_id", "checkpoint_id"}
    )
    return f"- {label}: {rest}"


def write_markdown(grouped: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3813 - RBridge Matter Glue No-Source Slot Or Finite Source Normalizer Row",
        "",
        "## Status",
        "",
        "`PASS_NONCLAIM_RMATTER_GLUE_ZERO_CONTRACT_AND_SOURCE_PRODUCT_BOUNDS_BUILT`.",
        "",
        "3813 turns `R_matter_glue` from a named hole into a theorem-or-product-bound branch.",
        "",
        "The theorem route is exact but conditional: one parent action-density line, connected ordinary-matter naturality, species-blind measure/current ownership, Hilbert variation before readout, and source-label forgetting together give `R_matter_glue^AB = 0` for source-only species glue. DD composition charges survive; they are not being deleted.",
        "",
        "The finite route now has concrete rows: WEP bounds source-bound `abs(S_E^q) * abs(Delta epsilon_AB)` for `epsilon_J_spurion`, `epsilon_species_measure`, `epsilon_current_rescaling`, `epsilon_nonHilbert_current`, new `epsilon_source_reentry`, and a total `R_matter_glue` envelope. These are product bounds, not isolated coefficient bounds.",
        "",
        "No local-GR, WEP, Newton, EM, clock, or calibrated source-coupling claim is made.",
        "",
    ]
    sections = [
        ("Source Register", "sources", ["source_id"]),
        ("Matter Glue Zero Theorem Contract", "zero_contract", ["clause_id"]),
        ("Rmatter Glue Decomposition", "decomposition", ["residual_piece_id", "symbol"]),
        ("Source Product Bound Rows", "product_bounds", ["product_bound_id", "symbol"]),
        ("Rvisible Coeff Glue Map", "visible_map", ["map_id"]),
        ("Residual Status Updates", "updates", ["update_id"]),
        ("Claim Gates", "gates", ["gate_id"]),
        ("Decision Rows", "decisions", ["decision_id"]),
        ("Next Target", "next_target", ["target_doc"]),
        ("Validation", "validation", ["check_id", "result"]),
    ]
    for title, key, key_fields in sections:
        lines.append(f"## {title}")
        for row in grouped[key]:
            lines.append(row_bullet(row, key_fields))
        lines.append("")
    DOC_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def update_spine() -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    lines = text.splitlines()
    if lines and lines[0].startswith("# Local GR Coupling Spine - Current State After "):
        lines[0] = "# Local GR Coupling Spine - Current State After 3813"
        text = "\n".join(lines) + "\n"

    paragraph = (
        "`3813` fuses the no-source-only matter grammar into a concrete `R_matter_glue` branch. "
        "The zero route is now exact as a conditional theorem: a single parent action-density line, connected ordinary-matter naturality, species-blind measure/current ownership, Hilbert source variation before readout, and source-label forgetting remove source-only species glue while preserving DD composition charges. "
        "The finite route is also stronger: WEP rows now source-bound `abs(S_E^q)` times `epsilon_J_spurion`, `epsilon_species_measure`, `epsilon_current_rescaling`, `epsilon_nonHilbert_current`, `epsilon_source_reentry`, and a total `R_matter_glue` envelope, but none are isolated without a source-amplitude lower/normalization theorem."
    )
    if "`3813` fuses the no-source-only matter grammar" not in text:
        marker = "`3812` turns the 3811 coupling bottleneck"
        idx = text.find(marker)
        if idx >= 0:
            next_blank = text.find("\n\n", idx)
            if next_blank >= 0:
                text = text[: next_blank + 2] + paragraph + "\n\n" + text[next_blank + 2 :]

    bullet = "- `3813 matter-glue branch`: `R_matter_glue` now has an exact conditional zero theorem and finite WEP source-product rows; the remaining blocker is isolating products through `abs(S_E^q)`."
    if bullet not in text:
        anchor = "- `3812 transport/source bridge`: WEP row normalizer factors are now numeric times `abs_S_Eq_inv`; same-vector DD is executable and forbids the old WEP-linear-rank shortcut."
        text = text.replace(anchor, anchor + "\n" + bullet)

    nonclaim = "- The 3813 matter-glue branch is nonclaim: theorem-zero clauses are not parent-signed, and source-product rows do not isolate residual coefficients without a parent-owned `abs(S_E^q)` lower/normalization theorem."
    if nonclaim not in text:
        anchor = "- The 3812 transport/source bridge is nonclaim: WEP normalizer factors are real, but `S_E^q`, clock transport normalizers, and `R_bridge` source-ownership residuals remain unsigned."
        text = text.replace(anchor, anchor + "\n" + nonclaim)

    old_target = (
        "`3813-Y5-R2FR-Rbridge-matter-glue-no-source-slot-or-finite-source-normalizer-row.md`\n\n"
        "Target: attack the source-ownership bottleneck exposed by 3812. Prove the ordinary-matter functor/no-source-only-slot theorem that sets `R_matter_glue` and `R_visible_coeff` to zero, or extract the first finite parent source-normalizer residual row.\n\n"
        "This is the best next move because WEP row normalizer geometry is no longer the main ambiguity. The remaining lift is to make `S_E^q` parent-owned, or bound the residuals in `S_E^q = Q_Earth dot C + R_bridge`."
    )
    new_target = (
        "`3814-Y5-R2FR-source-amplitude-lower-bound-or-worldtube-current-normalization-theorem.md`\n\n"
        "Target: attack the isolation bottleneck exposed by 3813. Derive a parent-owned lower/nonzero theorem or normalization rule for `abs(S_E^q)`, preferably from the worldtube current definition and denominator, or state the exact finite residual product level that remains.\n\n"
        "This is the best next move because many source residuals are now product-bounded with WEP units. The next decisive question is whether those products can be isolated without setting `S_E^q=1` by hand."
    )
    if old_target in text:
        text = text.replace(old_target, new_target)

    artifacts = [
        "P8_Y5_R2FR_3813_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_3813_MATTER_GLUE_ZERO_THEOREM_CONTRACT.csv",
        "P8_Y5_R2FR_3813_RMATTER_GLUE_DECOMPOSITION.csv",
        "P8_Y5_R2FR_3813_SOURCE_PRODUCT_BOUND_ROWS.csv",
        "P8_Y5_R2FR_3813_RVISIBLE_COEFF_GLUE_MAP.csv",
        "P8_Y5_R2FR_3813_RESIDUAL_STATUS_UPDATES.csv",
        "P8_Y5_R2FR_3813_CLAIM_GATES.csv",
        "P8_Y5_R2FR_3813_DECISION_ROWS.csv",
        "P8_Y5_R2FR_3813_NEXT_TARGET.csv",
        "P8_Y5_R2FR_3813_STATUS.csv",
        "P8_Y5_BRR545_3813_VALIDATION.csv",
    ]
    for artifact in artifacts:
        entry = f"- `source-intake\\mts_residuals\\{artifact}`"
        if entry not in text:
            text = text.rstrip() + "\n" + entry + "\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def cleanup_pycache() -> None:
    pycache = PCW / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    for key, path in OUTPUTS.items():
        if key != "validation":
            if not path.exists():
                raise AssertionError(f"missing output {path}")
            read_csv(path)
    fwb_hits = list(FWB.rglob("*3813*")) if FWB.exists() else []
    pycache = PCW / "scripts" / "__pycache__"
    spine_text = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    bad_chars_clean = all("\ufffd" not in read_text(path) for path in [DOC_PATH, SCRIPT_PATH, SPINE_PATH] if path.exists())
    checks = [
        ("sources_exist", all(row["exists"] == "true" for row in grouped["sources"]), "every cited source path exists"),
        ("needles_found", all(row["needle_found"] == "true" for row in grouped["sources"]), "every cited source needle was found"),
        ("csv_outputs_parse", True, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3813 markdown document written"),
        ("zero_contract_present", any(row["clause_id"] == "ZC3813_5_zero_theorem_result" for row in grouped["zero_contract"]), "fused matter-glue zero theorem result emitted"),
        ("source_product_bounds_created", len(grouped["product_bounds"]) == 12, "twelve source-product rows generated across two WEP arenas"),
        ("source_reentry_no_longer_missing_only", sum(row["symbol"] == "epsilon_source_reentry" for row in grouped["product_bounds"]) == 2, "source reentry has product-bound rows"),
        ("rmatter_glue_success_gate", any(row["symbol"] == "R_matter_glue_total" and row["bound_units"] == "dimensionless_eta" for row in grouped["product_bounds"]), "R_matter_glue has finite source-product rows with units"),
        ("coefficients_not_isolated", all(row["isolates_coefficient"] == "false" for row in grouped["product_bounds"]), "product rows do not over-isolate coefficients"),
        ("parent_claim_blocked", any(row["gate_id"] == "GATE3813_1_parent_premises_signed" and row["passed"] == "false" for row in grouped["gates"]), "parent theorem-zero premises remain blocked"),
        ("claims_closed", all(row["claim_allowed"] == "false" for row in grouped["gates"]), "no claim gate allows a claim"),
        ("spine_updated", "Current State After 3813" in spine_text and "3814-Y5-R2FR-source-amplitude-lower-bound-or-worldtube-current-normalization-theorem.md" in spine_text, "live spine updated to 3813 and 3814 target"),
        ("formalization_clean", not fwb_hits, "no 3813 files written under formalization-workbench"),
        ("pycache_removed", not pycache.exists(), "scripts __pycache__ removed"),
        ("bad_chars_clean", bad_chars_clean, "new doc/script/spine contain no mojibake replacement characters"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "zero_contract": zero_contract_rows(timestamp),
        "decomposition": decomposition_rows(timestamp),
        "product_bounds": source_product_bound_rows(timestamp),
        "visible_map": visible_map_rows(timestamp),
        "updates": updates_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = gate_rows(timestamp, grouped)
    grouped["validation"] = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": "pending",
            "result": "PASS",
            "detail": "placeholder before final validation",
        }
    ]
    for key, path in OUTPUTS.items():
        if key != "validation":
            write_csv(path, grouped[key])
    write_markdown(grouped)
    update_spine()
    cleanup_pycache()
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    write_markdown(grouped)
    cleanup_pycache()
    failed = [row for row in grouped["validation"] if row["result"] != "PASS"]
    print(grouped["status"][0]["status"])
    print(f"wrote {DOC_PATH}")
    if failed:
        raise SystemExit(f"validation failed: {failed}")


if __name__ == "__main__":
    main()
