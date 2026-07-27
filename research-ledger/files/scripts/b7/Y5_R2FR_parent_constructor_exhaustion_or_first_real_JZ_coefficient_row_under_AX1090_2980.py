from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
MICRO_QUAR = ROOT / "source-intake" / "microscope" / "quarantine"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2980"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2980-Y5-R2FR-parent-constructor-exhaustion-or-first-real-JZ-coefficient-row-under-AX1090.md"

SRC_2979_DOC = ROOT / "2979-Y5-R2FR-no-marker-source-covector-theorem-or-JZ-component-coefficient-acquisition-under-AX1090.md"
SRC_2979_NEXT = RESIDUALS / "P8_Y5_R2FR_2979_NEXT_TARGET.csv"
SRC_2979_THEOREM = RESIDUALS / "P8_Y5_R2FR_2979_NO_MARKER_SOURCE_COVECTOR_THEOREM_ATTEMPT.csv"
SRC_2979_CONSTRUCTOR = RESIDUALS / "P8_Y5_R2FR_2979_PARENT_CONSTRUCTOR_EXHAUSTION_GATE.csv"
SRC_2979_COEFFICIENTS = RESIDUALS / "P8_Y5_R2FR_2979_JZ_COMPONENT_COEFFICIENT_LEDGER_NONCLAIM.csv"
SRC_2979_RUNNER = RESIDUALS / "P8_Y5_R2FR_2979_JZ_COEFFICIENT_PROMOTION_RULES.csv"
SRC_2979_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2979_VALIDATION.csv"

SRC_2940_CHAIN = PARENT_ACTION / "Minimal_parent_current_chain_action_synthesis_2940_NONCLAIM.csv"
SRC_2970_SIGNATURE = PARENT_ACTION / "parent_quotient_basic_matter_signature_attempt_2970_NOT_DERIVED.csv"
SRC_2911_QMAP = PARENT_ACTION / "Parent_qmap_kernel_attempt_2911_NONCLAIM.csv"
SRC_2300_SLOT = BETA_DOCS / "Q_PARENT_SLOT_NORMAL_FORM_2300_NONCLAIM.csv"
SRC_2771_LABEL = BETA_DOCS / "PARENT_CATEGORY_LABEL_FORGETTING_2771_NONCLAIM.csv"
SRC_2318_ARENA = BETA_DOCS / "PARENT_COEFFICIENT_FUNCTOR_ARENA_GATES_2318_NONCLAIM.csv"
SRC_2760_NOHOM = BETA_DOCS / "NO_HIDDEN_VISIBLE_HOM_LOCAL_ARENA_IMPACT_2760_NONCLAIM.csv"
SRC_2327_GM = BETA_DOCS / "SOURCE_GM_UNIVERSALITY_ATTEMPT_2327_NONCLAIM.csv"
SRC_2971_SPLIT = LOCAL_BOUNDS / "DqZ_JA_subcoefficient_split_2971_NONCLAIM.csv"
SRC_2970_COEF = LOCAL_BOUNDS / "DqZ_JA_first_leakage_coefficients_2970_NONCLAIM.csv"
SRC_2971_ACQ = PARENT_ACTION / "first_DqZ_JA_leakage_coefficient_acquisition_2971_NOT_DERIVED.csv"
SRC_2892_NEUTRALITY = SOURCE_WEIGHT / "RAB_PARENT_ACTION_SOURCE_NEUTRALITY_SCHEMA_2892_NONCLAIM.csv"
SRC_2893_BETA = SOURCE_WEIGHT / "RAB_BETA_SOURCE_NO_SOURCE_SLOT_UPDATE_2893_NONCLAIM.csv"
SRC_2522_ZERO = RESIDUALS / "P8_Y5_NO_SHADOW_2522_MATTER_MEMORY_DIRECT_ZERO_AUDIT.csv"
SRC_2522_DRY = RESIDUALS / "P8_Y5_NO_SHADOW_2522_DRYRUN_RESULTS.csv"
SRC_2618_SHADOW = RESIDUALS / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_SHADOW_COEFFICIENT_PACK.csv"
SRC_1839_SHADOW_BAN = MICRO_QUAR / "1839" / "P8_Y5_PARENT_QLOC_1839_SOURCE_SHADOW_BAN_ATTEMPT.csv"
SRC_1839_SHADOW_STATUS = MICRO_QUAR / "1839" / "P8_Y5_PARENT_QLOC_1839_SOURCE_MAP_NORMAL_FORM_STATUS.csv"
SRC_1479_BOUNDS = MICRO_QUAR / "1479" / "COMPONENT_DELTA_W_BOUND_PACK_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2980_SOURCE_REGISTER.csv",
    "constructor": RESIDUALS / "P8_Y5_R2FR_2980_PARENT_GENERATE_EXHAUSTION_ATTEMPT.csv",
    "coefficient_audit": RESIDUALS / "P8_Y5_R2FR_2980_FIRST_REAL_JZ_COEFFICIENT_PROMOTION_AUDIT.csv",
    "candidate_scan": RESIDUALS / "P8_Y5_R2FR_2980_COEFFICIENT_CANDIDATE_SCAN_NONCLAIM.csv",
    "promotion": RESIDUALS / "P8_Y5_R2FR_2980_PROMOTION_RULES.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2980_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2980_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2980_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2980_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2980_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "constructor_copy": PARENT_ACTION / "parent_constructor_exhaustion_attempt_2980_NOT_DERIVED.csv",
    "coefficient_copy": LOCAL_BOUNDS / "first_real_JZ_coefficient_promotion_audit_2980_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2980_single_action_density_line_or_deltawe_deproxy_next_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
    except Exception:
        return False
    return True


def anchors_present(path: Path, anchors: list[str]) -> bool:
    text = read_text(path)
    return path.exists() and all(anchor in text for anchor in anchors)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2980_0_2979_doc", SRC_2979_DOC, ["Status:", "ParentGenerate", "Validation overall"], "2979 markdown handoff"),
        ("SRC2980_1_2979_next", SRC_2979_NEXT, ["NEXT2979_0_2980", "one real source-backed J_Z"], "selected 2980 target"),
        ("SRC2980_2_2979_theorem", SRC_2979_THEOREM, ["NMC2979_3_countermodel", "NMC2979_8_verdict"], "no-marker theorem verdict"),
        ("SRC2980_3_2979_constructor", SRC_2979_CONSTRUCTOR, ["PCX2979_0_parent_constructor", "PCX2979_8_same_branch"], "constructor exhaustion gates"),
        ("SRC2980_4_2979_coefficients", SRC_2979_COEFFICIENTS, ["JZC2979_2_delta_w_e_proxy", "JZC2979_8_Jdirect_marker", "JZC2979_13_Y6"], "J_Z coefficient ledger"),
        ("SRC2980_5_2979_runner", SRC_2979_RUNNER, ["RUN2979_0_no_missing", "RUN2979_4_proxy_policy", "RUN2979_5_claim_gate"], "promotion rules"),
        ("SRC2980_6_2979_validation", SRC_2979_VALIDATION, ["VAL2979_OVERALL"], "2979 validation"),
        ("SRC2980_7_2940_chain", SRC_2940_CHAIN, ["SYN2940_0_total_spine", "SYN2940_8_verdict"], "minimal parent current-chain action"),
        ("SRC2980_8_2970_signature", SRC_2970_SIGNATURE, ["SIG2970_7_no_source_slot", "SIG2970_8_verdict"], "parent quotient/basic matter signature"),
        ("SRC2980_9_2911_qmap", SRC_2911_QMAP, ["QMAP2911_2_Dq_source", "QMAP2911_7_verdict"], "q map source kernel"),
        ("SRC2980_10_2300_slot", SRC_2300_SLOT, ["QSLOT2300_6_epsilon_source_scalar", "QSLOT2300_9_tail_q"], "parent slot normal form"),
        ("SRC2980_11_2771_label", SRC_2771_LABEL, ["NSS2771_0_absent_slot", "NSS2771_2_relative_weight"], "category/source label forgetting"),
        ("SRC2980_12_2318_arena", SRC_2318_ARENA, ["ARENA2318_0_local_GR", "ARENA2318_3_R10"], "coefficient functor arena gates"),
        ("SRC2980_13_2760_nohom", SRC_2760_NOHOM, ["ARENA2760_1_local_GR", "ARENA2760_5_orbital"], "no-hidden-visible-Hom impact"),
        ("SRC2980_14_2327_gm", SRC_2327_GM, ["UGM2327_2_no_source_only_species_slot", "UGM2327_6_verdict"], "source GM universality attempt"),
        ("SRC2980_15_2971_split", SRC_2971_SPLIT, ["SPL2971_14_J_Z_vertex", "SPL2971_17_J_species_weight", "SPL2971_24_J_domain_current"], "subcoefficient split"),
        ("SRC2980_16_2970_coef", SRC_2970_COEF, ["COEF2970_4_J_direct", "COEF2970_9_total"], "first leakage coefficients"),
        ("SRC2980_17_2971_acq", SRC_2971_ACQ, ["ACQ2971_4_J_direct", "ACQ2971_9_total"], "coefficient acquisition status"),
        ("SRC2980_18_2892_neutrality", SRC_2892_NEUTRALITY, ["PAS2892_1_quotient_action", "PAS2892_5_result"], "source-neutrality schema"),
        ("SRC2980_19_2893_beta", SRC_2893_BETA, ["BZ2893_3_no_source_only_slot", "BZ2893_6_verdict"], "beta no-source-slot update"),
        ("SRC2980_20_2522_zero", SRC_2522_ZERO, ["JDZ2522_3_source_prefactor", "JDZ2522_7_verdict"], "direct source zero audit"),
        ("SRC2980_21_2522_dry", SRC_2522_DRY, ["DRY2522_2_no_source_slot_repeat", "DRY2522_4_numeric_Jdirect_without_bundle"], "direct source dry-run refusals"),
        ("SRC2980_22_2618_shadow", SRC_2618_SHADOW, ["SCP2618_0_delta_w_shadow", "SCP2618_5_nonclaim_lock"], "shadow coefficient pack"),
        ("SRC2980_23_1839_shadow_ban", SRC_1839_SHADOW_BAN, ["SSB1839_1_shadow_trichotomy", "SSB1839_3_current_verdict"], "source shadow ban attempt"),
        ("SRC2980_24_1839_shadow_status", SRC_1839_SHADOW_STATUS, ["SMNF1839_2_shadow_residuals", "SMNF1839_3_GR_left_hand"], "source map normal-form status"),
        ("SRC2980_25_1479_bounds", SRC_1479_BOUNDS, ["CBP1479_1_delta_w_e", "CBP1479_8_zeta_A"], "delta-w component proxy pack"),
    ]
    return [
        add_common(
            {
                "source_id": source_id,
                "source_path": str(path),
                "role": role,
                "required_anchors": ";".join(anchors),
                "exists": path.exists(),
                "anchors_found": anchors_present(path, anchors),
            }
        )
        for source_id, path, anchors, role in specs
    ]


def constructor_rows() -> list[dict[str, Any]]:
    rows = [
        ("PG2980_0_parent_generate", "derive ParentGenerate image from MTS primitives", "ParentGenerate[Q_obs,Psi,theta_rep,universal constants,boundary proper terms] exhausts admissible ordinary source action slots", "NOT_DERIVED", "SYN2940 is a finite spine, not a derived parent action"),
        ("PG2980_1_Qvis_basic", "Q_vis and q are parent-owned before matter/readout", "q: Phi_parent -> Q_vis plus q|C_Z=qbar(Q_vis) with no hidden representative labels", "NOT_PARENT_SIGNED", "SIG2970/QMAP2911 keep q source kernel and Q_vis constructor unsigned"),
        ("PG2980_2_no_source_target", "no source-only coefficient target exists", "Coeff_source-only not in Obj(Language_parent)", "CONDITIONAL_ONLY", "no-Hom signatures exist but not constructor-derived"),
        ("PG2980_3_source_label_forgetting", "source labels forgotten before coupling", "q_src({(T_A,A)})=T_total before kappa/GM coupling", "NOT_PARENT_SIGNED", "NSS2771 keeps relative weights as live countermodel"),
        ("PG2980_4_single_action_density", "one ordinary-matter action-density line", "ordinary matter generated by a single parent measure/hbar/action density line", "NOT_PARENT_SIGNED", "direct-sum action weights remain legal unless the action-line owner is proved"),
        ("PG2980_5_species_blind_measure", "species-blind measure and Jacobian", "D_A log mu_parent = D_A log J_measure = 0 for source-only labels", "NOT_PARENT_SIGNED", "measure/action scale owner still required"),
        ("PG2980_6_source_neutrality", "ordinary source branch is quotient-neutral", "S_matter=Sbar[Q_vis,Psi,theta_pub] and no source prefactor/source pole/source boundary charge", "SUFFICIENT_CONDITIONAL_SCHEMA_ONLY", "PAS2892 is a schema, not a parent derivation"),
        ("PG2980_7_same_branch", "all constructor clauses close in one branch", "PG2980_0 through PG2980_6 parent-signed together", "NOT_CLOSED", "separate conditional theorems do not exhaust the constructor"),
    ]
    return [
        add_common(
            {
                "constructor_id": constructor_id,
                "required_piece": required_piece,
                "formal_requirement": formal_requirement,
                "status": status,
                "blocking_gap": blocking_gap,
                "constructor_exhausted": False,
            }
        )
        for constructor_id, required_piece, formal_requirement, status, blocking_gap in rows
    ]


def coefficient_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("PROM2980_0_delta_w_e", "delta_w_e", "8.948213306283e-11", "dimensionless", "REJECT_PROMOTION_PROXY_ONLY", "unit-kernel WEP proxy lacks MTS parent component map, tau/source/readout/product convention", "CBP1479_1_delta_w_e"),
        ("PROM2980_1_J_direct", "J_direct", "MISSING_SOURCE_BACKED_UPPER_BOUND", "source_normalized", "REJECT_PROMOTION_MISSING_VALUE", "direct Z/source vertex, source-prefactor and endpoint rows all have MISSING upper bounds", "COEF2970_4_J_direct;SPL2971_14_J_Z_vertex"),
        ("PROM2980_2_J_spurion", "J_spurion", "MISSING_SOURCE_BACKED_UPPER_BOUND", "source_normalized", "REJECT_PROMOTION_MISSING_VALUE", "species weights, measure Jacobian and marker return are all missing bounds", "COEF2970_5_J_spurion;SPL2971_17_J_species_weight"),
        ("PROM2980_3_J_nonH", "J_nonH", "MISSING_SOURCE_BACKED_UPPER_BOUND", "source_normalized", "REJECT_PROMOTION_MISSING_VALUE", "non-Hilbert/torsion/worldtube/domain current rows are not source-backed", "COEF2970_6_J_nonH;SPL2971_21_J_nonHilbert_current"),
        ("PROM2980_4_delta_w_shadow", "delta_w_shadow", "MISSING_NORMAL_FORM_ZERO_OR_BOUND", "dimensionless_or_arena_normalized", "REJECT_PROMOTION_MISSING_NORMAL_FORM", "source-shadow trichotomy exists but every shadow channel needs zero theorem, reclassification or bound", "SCP2618_0_delta_w_shadow;SMNF1839_2_shadow_residuals"),
        ("PROM2980_5_Jreadout_PiM", "J_readout/J_PiM", "MISSING_COMPONENT_VALUES", "memory_source_units_or_dimensionless", "REJECT_PROMOTION_MISSING_PROJECTION", "readout/material/PiM components lack values, units and arena projection maps", "JZC2979_10_Jreadout_material;JZC2979_11_JPiM_extra"),
        ("PROM2980_6_Y5Y6", "eps_JZ_Y5/eps_JZ_Y6", "MISSING_Y5_ZERO_OR_BOUND;MISSING_Y6_ZERO_OR_BOUND", "source norm", "REJECT_PROMOTION_HARD_BLOCK", "source-normalization and extra-stress channels still lack theorem-zero or finite coefficients", "JZC2979_12_Y5;JZC2979_13_Y6"),
        ("PROM2980_7_total", "eps_JZ_total", "MISSING_COMPONENT_VALUES", "source norm", "NO_FIRST_REAL_JZ_ROW_PROMOTED", "no candidate has non-proxy value, units, source path, same-branch lock and parent projection", "RUN2979_0_no_missing;RUN2979_5_claim_gate"),
    ]
    return [
        add_common(
            {
                "promotion_id": promotion_id,
                "symbol": symbol,
                "candidate_value": candidate_value,
                "units": units,
                "promotion_status": promotion_status,
                "reason": reason,
                "source_anchor": source_anchor,
                "accepted_for_scoring": False,
            }
        )
        for promotion_id, symbol, candidate_value, units, promotion_status, reason, source_anchor in rows
    ]


def candidate_scan_rows() -> list[dict[str, Any]]:
    rows = [
        ("SCAN2980_0_real_numeric", "real non-proxy finite value", "none found", "NO_PROMOTABLE_ROW", "the only explicit numeric component is delta_w_e proxy, quarantined by parent-basis/projection gaps"),
        ("SCAN2980_1_theorem_zero", "parent theorem-zero row", "none found", "NO_PROMOTABLE_ROW", "all no-source/no-Hom/source-neutrality rows are conditional schemas or unsigned contracts"),
        ("SCAN2980_2_direct_source", "J_direct source-backed value", "none found", "NO_PROMOTABLE_ROW", "DqZ/J_A split rows keep MISSING_SOURCE_BACKED_UPPER_BOUND"),
        ("SCAN2980_3_shadow", "shadow-current coefficient", "none found", "NO_PROMOTABLE_ROW", "source-shadow basis is inventory-ready, not zeroed/bounded"),
        ("SCAN2980_4_readout_pim", "readout/PiM component value", "none found", "NO_PROMOTABLE_ROW", "material/readout/PiM maps require values, units and arena projections"),
        ("SCAN2980_5_y5y6", "Y5/Y6 finite or theorem-zero", "none found", "NO_PROMOTABLE_ROW", "source-normalization/extra-stress remain the hard channels"),
    ]
    return [
        add_common(
            {
                "scan_id": scan_id,
                "candidate_class": candidate_class,
                "best_current_value": best_current_value,
                "scan_status": scan_status,
                "why_not_promoted": why_not_promoted,
            }
        )
        for scan_id, candidate_class, best_current_value, scan_status, why_not_promoted in rows
    ]


def promotion_rule_rows() -> list[dict[str, Any]]:
    rows = [
        ("PR2980_0_no_proxy", "proxy rows cannot score", "numeric values from unit-kernel/quarantine rows remain smoke-only until parent projection exists", True),
        ("PR2980_1_source_backed", "source-backed value or theorem-zero required", "finite row must have source path, units, extraction/derivation method and no MISSING markers", False),
        ("PR2980_2_same_branch", "same branch lock required", "coefficient, projection, q/Z normalization and source convention must belong to the same parent branch", False),
        ("PR2980_3_units", "eps_JZ norm conversion required", "dimensionless source weights must map into q_loc/source norm through declared kernel", False),
        ("PR2980_4_no_cancellation", "absolute envelope retained", "component signs cannot cancel unless parent identity proves it", True),
        ("PR2980_5_claim", "no promotion this checkpoint", "constructor not exhausted and no real J_Z coefficient row passes", False),
    ]
    return [
        add_common(
            {
                "rule_id": rule_id,
                "rule": rule,
                "requirement": requirement,
                "passed_now": passed_now,
            }
        )
        for rule_id, rule, requirement, passed_now in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2980_0_constructor_exhaustion", "ParentGenerate/no-Hom exclusion derived", False, "constructor image not exhausted", False),
        ("CG2980_1_first_JZ", "first real J_Z coefficient promoted", False, "no non-proxy source-backed row passes", False),
        ("CG2980_2_JZ_zero", "J_Z theorem-zero", False, "no-marker/source-neutrality route remains conditional", False),
        ("CG2980_3_q_loc", "q_loc local residual suppressed", False, "J_Z/B_Z/DeltaK coefficient rows retained", False),
        ("CG2980_4_local_GR", "local GR/Newton reduction", False, "local source-current suppression not derived", False),
        ("CG2980_5_empirical", "R10/PPN/clock/orbital/WEP claims", False, "no promoted coefficient/theorem-zero", False),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "claim_allowed": allowed,
            }
        )
        for gate_id, claim, passed, status, allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2980_0_constructor",
            "decision": "Do not claim ParentGenerate exhaustion.",
            "because": "the corpus has a finite parent-action spine and conditional grammar clauses, not a derived constructor image.",
            "next_action": "narrow to the smallest constructor clause: single ordinary-matter action-density line plus species-blind measure",
        },
        {
            "decision_id": "DEC2980_1_coefficient",
            "decision": "Do not promote a first real J_Z coefficient row.",
            "because": "all candidates are missing, conditional, or proxy-only; delta_w_e is numeric but not on the MTS parent basis.",
            "next_action": "deproxy delta_w_e only after parent component map/tau/source/readout convention exists",
        },
        {
            "decision_id": "DEC2980_2_not_loop",
            "decision": "Avoid repeating the broad no-source-slot theorem.",
            "because": "2979 and older 2508 already identify that as wheel-spinning without new constructor evidence.",
            "next_action": "attack one action-density-line/measure clause or one coefficient row, not the whole grammar at once",
        },
        {
            "decision_id": "DEC2980_3_status",
            "decision": "Keep the coupling lock as the active local-GR bottleneck.",
            "because": "this is the exact route by which source normalization can spoil q_loc suppression and therefore the GR/Newton limit.",
            "next_action": "carry eps_JZ in the absolute q_loc envelope",
        },
    ]
    return [add_common(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "next_id": "NEXT2980_0_2981",
            "priority": "selected_primary",
            "next_doc": "2981-Y5-R2FR-single-action-density-line-and-species-blind-measure-or-deltawe-deproxy-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_single_action_density_line_and_species_blind_measure_or_deltawe_deproxy_under_AX1090_2981.py",
            "objective": "Try to parent-sign the smallest constructor clause: one ordinary-matter action-density line with one species-blind measure/hbar; if not, deproxy delta_w_e by requiring parent component map, tau/source/readout convention and source path.",
            "include": "single action density line;species-blind measure;hbar/action scale;connected matter graph;source-label forgetting;delta_w_e deproxy checklist;no proxy promotion",
            "exclude": "broad no-source-slot loop;B_Z full boundary proof;full K_metric certificate;R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits",
        }
    ]
    return [add_common(row) for row in rows]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        add_common({"copy_id": key, "path": str(path), "exists": path.exists()})
        for key, path in BRANCH_OUTPUTS.items()
    ]


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC]
    csv_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
    formalization_2980_count = 0
    if FORMALIZATION.exists():
        formalization_2980_count = sum(1 for path in FORMALIZATION.rglob("*2980*") if path.is_file())
    checks = [
        ("VAL2980_0_sources_exist", all(row["exists"] for row in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2980_1_anchors_found", all(row["anchors_found"] for row in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2980_2_constructor_not_derived", any(row["constructor_id"] == "PG2980_7_same_branch" and row["status"] == "NOT_CLOSED" for row in all_rows["constructor"]), "ParentGenerate exhaustion remains unclaimed", True),
        ("VAL2980_3_no_first_JZ", any(row["promotion_id"] == "PROM2980_7_total" and row["promotion_status"] == "NO_FIRST_REAL_JZ_ROW_PROMOTED" for row in all_rows["coefficient_audit"]), "no first real J_Z row promoted", True),
        ("VAL2980_4_proxy_rejected", any(row["promotion_id"] == "PROM2980_0_delta_w_e" and row["promotion_status"] == "REJECT_PROMOTION_PROXY_ONLY" for row in all_rows["coefficient_audit"]), "delta_w_e proxy rejected for scoring", True),
        ("VAL2980_5_scan_no_promote", all(row["scan_status"] == "NO_PROMOTABLE_ROW" for row in all_rows["candidate_scan"]), "candidate scan found no promotable row", True),
        ("VAL2980_6_rules_block_claim", any(row["rule_id"] == "PR2980_5_claim" and row["passed_now"] is False for row in all_rows["promotion"]), "promotion rule blocks claim", True),
        ("VAL2980_7_claims_blocked", all(row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates blocked", True),
        ("VAL2980_8_next_target_written", any(row["next_id"] == "NEXT2980_0_2981" for row in all_rows["next"]), "2981 narrow action-density/deproxy target selected", True),
        ("VAL2980_9_branches_exist", all(row["exists"] for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2980_10_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2980_11_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2980_12_formalization_clean", formalization_2980_count == 0, f"no 2980 outputs were written to formalization-workbench (count={formalization_2980_count})", True),
        ("VAL2980_13_doc_written", DOC.exists(), "2980 markdown checkpoint exists", True),
    ]
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": bool(passed),
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(add_common({"validation_id": "VAL2980_OVERALL", "passed": overall, "check": "2980 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    output_rows = [
        {"output": key, "path": str(path), "exists": path.exists()}
        for key, path in OUTPUTS.items()
        if key != "validation"
    ]
    branch_rows = [
        {"copy": key, "path": str(path), "exists": path.exists()}
        for key, path in BRANCH_OUTPUTS.items()
    ]
    text = f"""# 2980 - Parent Constructor Exhaustion or First Real J_Z Coefficient Row

Status: `Y5_R2FR_2980_parent_constructor_not_exhausted_first_real_JZ_row_not_promoted_deltawe_proxy_rejected_next_narrow_action_line_or_deproxy_nonclaim`

Claim ceiling: `no_parent_generate_exhaustion_no_first_real_JZ_coefficient_no_JZ_zero_no_q_loc_zero_no_local_GR_no_Newton_no_R10_no_PPN_no_clock_no_orbital_no_WEP_no_public_claim`

## Summary

- The parent-constructor route does not close: `SYN2940` gives a finite action spine, but not a derived `ParentGenerate` image/no-Hom theorem.
- The coefficient route also does not close: no non-proxy, source-backed `J_Z` component row has values, units, projection, and same-branch ownership.
- The existing electron `delta_w_e = 8.948213306283e-11` row stays useful as a smoke/proxy row only; it is not an MTS parent-basis coefficient.
- This checkpoint prevents a loop: broad no-source-slot language is no longer enough unless new constructor-exhaustion evidence appears.
- Best next move is narrower: prove one ordinary-matter action-density line with a species-blind measure, or deproxy `delta_w_e` with a real parent map.

## Generated Outputs

{md_table(output_rows, ["output", "path", "exists"])}

## Branch Copies

{md_table(branch_rows, ["copy", "path", "exists"])}

## ParentGenerate Exhaustion Attempt

{md_table(all_rows["constructor"], ["constructor_id", "required_piece", "formal_requirement", "status", "blocking_gap", "constructor_exhausted"])}

## First Real J_Z Coefficient Promotion Audit

{md_table(all_rows["coefficient_audit"], ["promotion_id", "symbol", "candidate_value", "units", "promotion_status", "reason", "accepted_for_scoring"])}

## Candidate Scan

{md_table(all_rows["candidate_scan"], ["scan_id", "candidate_class", "best_current_value", "scan_status", "why_not_promoted"])}

## Promotion Rules

{md_table(all_rows["promotion"], ["rule_id", "rule", "requirement", "passed_now"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "constructor": constructor_rows(),
        "coefficient_audit": coefficient_audit_rows(),
        "candidate_scan": candidate_scan_rows(),
        "promotion": promotion_rule_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    shutil.copyfile(OUTPUTS["constructor"], BRANCH_OUTPUTS["constructor_copy"])
    shutil.copyfile(OUTPUTS["coefficient_audit"], BRANCH_OUTPUTS["coefficient_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_copy_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2980 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
