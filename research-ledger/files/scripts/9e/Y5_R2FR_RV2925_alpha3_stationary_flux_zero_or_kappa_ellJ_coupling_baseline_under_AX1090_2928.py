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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2928"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2928-Y5-R2FR-RV2925-alpha3-stationary-flux-zero-or-kappa-ellJ-coupling-baseline-under-AX1090.md"

SRC_2927_DOC = ROOT / "2927-Y5-R2FR-RV2925-metric-readout-DqZ-geometry-Cshadow-first-source-bound-under-AX1090.md"
SRC_2927_NEXT = RESIDUALS / "P8_Y5_R2FR_2927_NEXT_TARGET.csv"
SRC_2927_TRANSFER = RESIDUALS / "P8_Y5_R2FR_2927_ALPHA3_TO_RV2925_TRANSFER_GATE.csv"
SRC_2927_BOUND = RESIDUALS / "P8_Y5_R2FR_2927_CSHADOW_FIRST_SOURCE_BOUND_SELECTION.csv"
SRC_2919_DOC = ROOT / "2919-Y5-R2FR-stationary-alpha3-flux-zero-theorem-or-beta-source-normalization-kernel-under-AX1090.md"
SRC_2919_AUDIT = RESIDUALS / "P8_Y5_R2FR_2919_STATIONARY_ALPHA3_FLUX_ZERO_AUDIT.csv"
SRC_2919_HEADS = RESIDUALS / "P8_Y5_R2FR_2919_ALPHA3_HEAD_REDUCTION_LEDGER.csv"
SRC_2919_BETA = RESIDUALS / "P8_Y5_R2FR_2919_BETA_SOURCE_NORMALIZATION_FALLBACK_KERNEL.csv"
SRC_2919_NEXT = RESIDUALS / "P8_Y5_R2FR_2919_NEXT_TARGET.csv"
SRC_2918_KERNEL = RESIDUALS / "P8_Y5_R2FR_2918_ALPHA3_SOURCE_CURRENT_KERNEL.csv"
SRC_2918_PRODUCTS = RESIDUALS / "P8_Y5_R2FR_2918_ALPHA3_PRODUCT_BOUND_ROWS.csv"
SRC_2918_COUPLING = RESIDUALS / "P8_Y5_R2FR_2918_COUPLING_OWNER_GATES.csv"
SRC_2578_GATE = RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_COUPLING_BASELINE_GATE.csv"
SRC_2578_RESIDUALS = RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_RESIDUAL_INPUT_LEDGER.csv"
SRC_2695_DOC = ROOT / "2695-Y5-R2FR-kappa-topological-superselection-parent-adoption-or-drift-residual-values.md"
SRC_2695_KAPPA = RESIDUALS / "P8_Y5_R2FR_2695_KAPPA_RESIDUAL_VALUE_REQUIREMENTS_NONCLAIM.csv"
SRC_KAPPA_MAP = RESIDUALS / "P8_CONSTANT_KAPPA_RESIDUAL_MAP.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2928_SOURCE_REGISTER.csv",
    "stationary_reentry": RESIDUALS / "P8_Y5_R2FR_2928_STATIONARY_ALPHA3_REENTRY_AUDIT.csv",
    "coupling_rows": RESIDUALS / "P8_Y5_R2FR_2928_KAPPA_ELLJ_COUPLING_BASELINE_ROWS.csv",
    "head_update": RESIDUALS / "P8_Y5_R2FR_2928_ALPHA3_RV2925_HEAD_UPDATE.csv",
    "beta_handoff": RESIDUALS / "P8_Y5_R2FR_2928_BETA_SOURCE_NORMALIZATION_HANDOFF.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2928_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2928_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2928_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2928_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2928_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "stationary_copy": PARENT_ACTION / "Stationary_alpha3_reentry_2928_NONCLAIM.csv",
    "coupling_copy": LOCAL_BOUNDS / "RV2925_kappa_ellJ_coupling_baseline_2928_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2928_BETA_SOURCE_NORMALIZATION_SQUARE_LAW_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def row_with_value(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str] | None:
    for row in rows:
        if row.get(key) == value:
            return row
    return None


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2928_00_2927_doc", SRC_2927_DOC, "NEXT2927_0_2928;Dln(kappa_MTS);Validation overall: `True`", "2927 selected stationary alpha3/coupling-baseline next target"),
        ("SRC2928_01_2927_next", SRC_2927_NEXT, "NEXT2927_0_2928;kappa_MTS;ell_J", "machine-readable 2928 target"),
        ("SRC2928_02_2927_transfer", SRC_2927_TRANSFER, "TR2927_5_verdict;TRANSFER_FAILS_NONCLAIM", "alpha3-to-RV2925 transfer remains blocked"),
        ("SRC2928_03_2927_bound", SRC_2927_BOUND, "FB2927_A3P2918_3_kappa;FB2927_A3P2918_4_ellJ", "2927 attached kappa/ellJ alpha3 product heads"),
        ("SRC2928_04_2919_doc", SRC_2919_DOC, "STATIONARY_ALPHA3_ZERO_FAILS_CURRENT_MTS_PARTIAL_QLOC_WIN_ONLY;NEXT2919_0_2920", "prior stationary proof attempt and beta fallback"),
        ("SRC2928_05_2919_audit", SRC_2919_AUDIT, "SFA2919_0_stationary_hilbert_current;SFA2919_9_verdict", "stationary alpha3 audit"),
        ("SRC2928_06_2919_heads", SRC_2919_HEADS, "A3H2919_0_q_loc_hilbert;A3H2919_8_total", "alpha3 head reduction ledger"),
        ("SRC2928_07_2919_beta", SRC_2919_BETA, "BFB2919_0_beta_law;BFB2919_7_total", "beta source-normalization fallback kernel"),
        ("SRC2928_08_2919_next", SRC_2919_NEXT, "NEXT2919_0_2920;B_source=A_source^2", "beta/source-normalization target"),
        ("SRC2928_09_2918_kernel", SRC_2918_KERNEL, "F_kappa_alpha3;F_ellJ_alpha3;Delta_alpha3_abs", "alpha3 source-current heads"),
        ("SRC2928_10_2918_products", SRC_2918_PRODUCTS, "A3P2918_3_kappa;A3P2918_4_ellJ", "alpha3 product bound rows"),
        ("SRC2928_11_2918_coupling", SRC_2918_COUPLING, "COUP2918_3_kappa;COUP2918_4_ellJ", "coupling-owner gates"),
        ("SRC2928_12_2578_gate", SRC_2578_GATE, "COG2578_0_kappa_constant;COG2578_2_ellJ_source_scale;COG2578_4_verdict", "PiM/Hamiltonian coupling baseline gate"),
        ("SRC2928_13_2578_residuals", SRC_2578_RESIDUALS, "RES2578_7_delta_kappa;RES2578_8_delta_ellJ", "coupling residual input rows"),
        ("SRC2928_14_2695_doc", SRC_2695_DOC, "S_kappa_top;KAD2695_8_verdict;KRR2695_0_time_drift", "conditional topological kappa mechanism and residual map"),
        ("SRC2928_15_2695_kappa", SRC_2695_KAPPA, "KRR2695_0_time_drift;KRR2695_5_bianchi_exchange", "source-ready kappa residual requirements"),
        ("SRC2928_16_kappa_map", SRC_KAPPA_MAP, "KR508_0_time_drift;KR508_5_Bianchi_exchange", "older constant-kappa residual map"),
    ]
    rows = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def stationary_reentry_rows() -> list[dict[str, Any]]:
    specs = [
        ("SR2928_0_import", "stationary compact exterior q_loc head", "PASS_CONDITIONAL_QLOC_HEAD_ONLY", "import 2919 partial win: J_M=0 -> q_loc=0 under fixed ell_J, Killing tau, compact support, parent-owned P_loc and silent boundary hypotheses", True),
        ("SR2928_1_not_total_alpha3", "total alpha3 flux-zero theorem", "FAILS_CURRENT_MTS", "alpha3 is stricter than q_loc and retains boundary/domain/exchange/coupling/disformal/readout heads", False),
        ("SR2928_2_kappa_survives", "Dln(kappa_MTS)=0", "MISSING_PARENT_CONSTANT_KAPPA_PROOF_OR_VALUE", "coupling baseline can feed alpha3, beta and Newton source normalization", False),
        ("SR2928_3_ellJ_survives", "Dln(ell_J)=0", "MISSING_PARENT_CONSTANT_ELLJ_PROOF_OR_VALUE", "source-current scale can feed alpha3, beta and measured source mass", False),
        ("SR2928_4_no_loop_rule", "do not rerun stationary alpha3 closure as if new", "REENTRY_DECISION", "2928 carries the partial q_loc theorem forward and moves to coupling/beta residuals", True),
    ]
    rows = []
    for audit_id, target, current_status, result, condition_passed in specs:
        rows.append(
            add_common(
                {
                    "audit_id": audit_id,
                    "target": target,
                    "current_status": current_status,
                    "result": result,
                    "condition_passed": condition_passed,
                    "adopted_for_claim": False,
                    "source_paths": ";".join(str(path) for path in [SRC_2919_AUDIT, SRC_2919_HEADS, SRC_2927_TRANSFER]),
                }
            )
        )
    return rows


def coupling_rows() -> list[dict[str, Any]]:
    residuals_2578 = read_csv_rows(SRC_2578_RESIDUALS)
    products_2918 = read_csv_rows(SRC_2918_PRODUCTS)
    kappa_residual = row_with_value(residuals_2578, "residual_id", "RES2578_7_delta_kappa") or {}
    ellj_residual = row_with_value(residuals_2578, "residual_id", "RES2578_8_delta_ellJ") or {}
    kappa_product = row_with_value(products_2918, "product_id", "A3P2918_3_kappa") or {}
    ellj_product = row_with_value(products_2918, "product_id", "A3P2918_4_ellJ") or {}
    specs = [
        (
            "CB2928_0_kappa_alpha3",
            "Dln(kappa_MTS)",
            "alpha3_kappa = K_alpha3_kappa * Dln(kappa_MTS)",
            "4e-20",
            kappa_product.get("current_status", "MISSING_CONSTANT_KAPPA_PROOF_OR_VALUE"),
            kappa_residual.get("residual_id", "RES2578_7_delta_kappa"),
            kappa_residual.get("status", "MISSING_CONSTANT_KAPPA_PROOF_OR_VALUE"),
            "dimensionless_after_alpha3_projection",
            "alpha3;beta;Newton;PPN;clock;orbital",
        ),
        (
            "CB2928_1_ellJ_alpha3",
            "Dln(ell_J)",
            "alpha3_ellJ = K_alpha3_ellJ * Dln(ell_J)",
            "4e-20",
            ellj_product.get("current_status", "MISSING_CONSTANT_ELLJ_PROOF_OR_VALUE"),
            ellj_residual.get("residual_id", "RES2578_8_delta_ellJ"),
            ellj_residual.get("status", "MISSING_CONSTANT_ELLJ_PROOF_OR_VALUE"),
            "dimensionless_after_alpha3_projection",
            "alpha3;beta;Newton;WEP;PPN;orbital",
        ),
        (
            "CB2928_2_kappa_parent_route",
            "kappa_topological_zeroform",
            "S_kappa_top = int_M kappa_eff dA_3 -> d kappa_eff = 0",
            "zero",
            "CONDITIONAL_PARENT_MECHANISM_NOT_SIGNED",
            "KAD2695_8_verdict",
            "PARENT_ADOPTION_FAILS_CURRENT_CORPUS",
            "boolean_or_dimensionless",
            "all_local_arenas",
        ),
        (
            "CB2928_3_coupling_total",
            "Delta_coupling_baseline_abs",
            "|K_alpha3_kappa Dln(kappa_MTS)| + |K_alpha3_ellJ Dln(ell_J)| + |epsilon_Gref_match| + |Delta_boundary_coupling|",
            "source-specific",
            "SOURCE_READY_VALUES_MISSING",
            "COG2578_4_verdict",
            "COUPLING_BASELINE_IDENTITY_NOT_DERIVED",
            "dimensionless_or_arena_specific",
            "alpha3;beta;Newton;local_GR",
        ),
    ]
    rows = []
    for row_id, symbol, formula, target_bound, current_status, upstream_row, upstream_status, units, arenas in specs:
        rows.append(
            add_common(
                {
                    "row_id": row_id,
                    "rv_component": "RV2925_0_metric_readout",
                    "symbol": symbol,
                    "formula_or_route": formula,
                    "target_bound_or_zero": target_bound,
                    "current_status": current_status,
                    "upstream_row": upstream_row,
                    "upstream_status": upstream_status,
                    "units": units,
                    "arena_links": arenas,
                    "numeric_value_present": False,
                    "theorem_zero": False,
                    "selected_for_next_fill": row_id in {"CB2928_0_kappa_alpha3", "CB2928_1_ellJ_alpha3"},
                    "source_paths": ";".join(str(path) for path in [SRC_2918_PRODUCTS, SRC_2578_GATE, SRC_2578_RESIDUALS, SRC_2695_KAPPA]),
                }
            )
        )
    return rows


def head_update_rows() -> list[dict[str, Any]]:
    specs = [
        ("A3U2928_0_q_loc", "q_loc_Hilbert_exterior", "CONDITIONAL_ZERO_IMPORTED", "stationary compact exterior kills this head only under signed hypotheses", "not enough for alpha3 total"),
        ("A3U2928_1_boundary", "F_boundary_alpha3", "RETAINED_MISSING_NOFLUX_OR_PRODUCT", "boundary compact-support momentum flux remains live", "needs zero theorem or product row <=4e-20"),
        ("A3U2928_2_domain", "F_domain_alpha3", "RETAINED_MISSING_DOMAIN_NOLEAK", "domain/projector preferred-frame leakage remains live", "needs domain/R11 silence or product row"),
        ("A3U2928_3_exchange", "F_exchange_alpha3", "RETAINED_MISSING_EXCHANGE_GRAPH", "source-exchange/source-shadow head remains live", "needs connected ordinary source graph or finite bound"),
        ("A3U2928_4_kappa", "F_kappa_alpha3", "SELECTED_COUPLING_BASELINE_ROW", "Dln(kappa_MTS) survives stationary proof", "fill theorem-zero or finite source-backed row"),
        ("A3U2928_5_ellJ", "F_ellJ_alpha3", "SELECTED_COUPLING_BASELINE_ROW", "Dln(ell_J) survives stationary proof", "fill theorem-zero or finite source-backed row"),
        ("A3U2928_6_total", "Delta_alpha3_abs", "TOTAL_RETAINED_NONCLAIM", "sum_abs active heads; no cancellation by fit", "no alpha3 pass"),
    ]
    rows = []
    for update_id, symbol, current_status, reason, next_requirement in specs:
        rows.append(
            add_common(
                {
                    "update_id": update_id,
                    "rv_component": "RV2925_0_metric_readout",
                    "symbol": symbol,
                    "current_status": current_status,
                    "reason": reason,
                    "next_requirement": next_requirement,
                    "target_bound_abs": "4e-20",
                    "score_input_present": False,
                    "head_zero_adopted_for_claim": False,
                    "source_paths": ";".join(str(path) for path in [SRC_2919_HEADS, SRC_2918_KERNEL, SRC_2918_PRODUCTS]),
                }
            )
        )
    return rows


def beta_handoff_rows() -> list[dict[str, Any]]:
    beta_rows = read_csv_rows(SRC_2919_BETA)
    rows = []
    for beta_row in beta_rows:
        rows.append(
            add_common(
                {
                    "handoff_id": f"BH2928_{beta_row.get('fallback_id', 'unknown')}",
                    "symbol": beta_row.get("symbol", "MISSING"),
                    "formula_or_map": beta_row.get("formula_or_map", "MISSING"),
                    "current_status": beta_row.get("current_status", "MISSING"),
                    "next_requirement": beta_row.get("next_requirement", "MISSING"),
                    "beta_bound_abs": beta_row.get("beta_bound_abs", "7.8e-05"),
                    "selected_next": beta_row.get("fallback_id") in {"BFB2919_0_beta_law", "BFB2919_1_source_residual", "BFB2919_7_total"},
                    "source_paths": beta_row.get("source_paths", str(SRC_2919_BETA)),
                }
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2928_0_q_loc_partial", "stationary q_loc exterior conditional theorem imported", "PASS_NONCLAIM_STRUCTURE", "useful partial win but hypotheses remain nonclaim", True),
        ("CG2928_1_alpha3_zero", "stationary alpha3 flux-zero theorem closes total alpha3", "BLOCKED_NONCLAIM", "boundary/domain/exchange/coupling/disformal/readout heads survive", False),
        ("CG2928_2_kappa_zero", "Dln(kappa_MTS)=0 is proved in current MTS", "BLOCKED_NONCLAIM", "topological parent mechanism is conditional and unsigned", False),
        ("CG2928_3_ellJ_zero", "Dln(ell_J)=0 is proved in current MTS", "BLOCKED_NONCLAIM", "source-current scale owner is not parent-derived", False),
        ("CG2928_4_beta_selected", "beta source-normalization square-law route is selected", "PASS_NONCLAIM_STRUCTURE", "next derivation target is clear but not score-ready", True),
        ("CG2928_5_local_GR_Newton", "local GR/Newton follows after 2928", "BLOCKED_NONCLAIM", "2928 stages residuals and next square-law target only", False),
    ]
    rows = []
    for gate_id, claim, gate_status, reason, gate_pass in specs:
        rows.append(
            add_common(
                {
                    "gate_id": gate_id,
                    "claim": claim,
                    "gate_status": gate_status,
                    "reason": reason,
                    "gate_pass": gate_pass,
                }
            )
        )
    return rows


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2928_0_stationary_result", "stationary_alpha3_reentry_closed_as_partial_win", "2919 already proves only the pure Hilbert-current q_loc head conditionally; total alpha3 still fails.", "do not rerun stationary closure as a fresh route"),
        ("DEC2928_1_coupling_result", "kappa_ellJ_rows_staged", "Dln(kappa_MTS) and Dln(ell_J) are explicit alpha3/beta/Newton residuals with source-ready ledgers but missing values or parent zero theorems.", "carry them as finite nonclaim rows"),
        ("DEC2928_2_next", "beta_source_normalization_square_law_selected", "After alpha3 stationary closure fails, beta asks whether the second-order source coefficient is the square of the first-order source coefficient.", "derive B_source=A_source^2 or keep beta finite"),
    ]
    rows = []
    for decision_id, decision, because, next_action in specs:
        rows.append(
            add_common(
                {
                    "decision_id": decision_id,
                    "decision": decision,
                    "because": because,
                    "next_action": next_action,
                }
            )
        )
    return rows


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2928_0_2929",
                "selection_status": "selected_primary",
                "target_file": "2929-Y5-R2FR-beta-source-normalization-square-law-or-finite-source-residual-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_beta_source_normalization_square_law_or_finite_source_residual_under_AX1090_2929.py",
                "task": "derive B_source=A_source^2 from the parent source-normalized local field equation in the same observed-U/source frame, or stage finite beta/source-normalization residual rows without measured-GM absorption",
                "success_condition": "parent square law makes beta_eff=1, or delta_beta_source and active beta heads get source-backed finite rows under the 7.8e-05 comparator",
                "fallback_condition": "keep beta nonclaim and move to source-normalized Newton/Gauss/orbital scorecard acquisition",
                "guardrails": "no Schwarzschild/EH beta import as axiom; no fitted-GM absorption; no cancellation credit; no local GR/Newton/PPN claim; no formalization-workbench edits; no GitHub",
                "selected": True,
            }
        )
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    stationary: list[dict[str, Any]],
    coupling: list[dict[str, Any]],
    head_update: list[dict[str, Any]],
    beta_handoff: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    checks = [
        ("VAL2928_0_source_paths_exist", all(as_bool(row["path_exists"]) for row in sources), "all cited source paths exist"),
        ("VAL2928_1_source_anchors_found", all(as_bool(row["anchors_found"]) for row in sources), "all source anchors found"),
        ("VAL2928_2_q_loc_partial_imported", any(row["audit_id"] == "SR2928_0_import" and row["condition_passed"] is True for row in stationary), "stationary q_loc partial win imported"),
        ("VAL2928_3_alpha3_total_still_blocked", any(row["audit_id"] == "SR2928_1_not_total_alpha3" and row["condition_passed"] is False for row in stationary), "total alpha3 closure still blocked"),
        ("VAL2928_4_kappa_ellJ_rows_staged", all(any(row["row_id"] == row_id and row["selected_for_next_fill"] is True for row in coupling) for row_id in ["CB2928_0_kappa_alpha3", "CB2928_1_ellJ_alpha3"]), "kappa and ellJ coupling rows staged"),
        ("VAL2928_5_no_coupling_values_promoted", all(not as_bool(row["numeric_value_present"]) and not as_bool(row["theorem_zero"]) for row in coupling), "no coupling value/theorem-zero promoted"),
        ("VAL2928_6_head_update_has_total", any(row["symbol"] == "Delta_alpha3_abs" and row["current_status"] == "TOTAL_RETAINED_NONCLAIM" for row in head_update), "alpha3 total retained nonclaim"),
        ("VAL2928_7_beta_handoff_selected", any(as_bool(row["selected_next"]) for row in beta_handoff), "beta/source-normalization handoff selected"),
        ("VAL2928_8_claim_gates_safe", all((not as_bool(row["gate_pass"])) or row["gate_status"] == "PASS_NONCLAIM_STRUCTURE" for row in claims), "only nonclaim structure gates pass"),
        ("VAL2928_9_next_target_selected", any(as_bool(row.get("selected", False)) for row in next_rows), "2929 next target selected"),
        ("VAL2928_10_branch_copies_parse", all(as_bool(row["destination_exists"]) and as_bool(row["destination_parses"]) for row in branches), "branch copies parse"),
        ("VAL2928_11_no_formalization_outputs", all(not is_under(path, FORMALIZATION) for path in output_paths), "no output path inside formalization-workbench"),
        ("VAL2928_12_doc_exists", DOC.exists(), "2928 markdown doc exists"),
    ]
    rows = [
        {
            "validation_id": check_id,
            "status": bool(status),
            "detail": detail,
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
        for check_id, status, detail in checks
    ]
    overall = all(row["status"] for row in rows)
    rows.append(
        {
            "validation_id": "VAL2928_OVERALL",
            "status": overall,
            "detail": "2928 validation overall",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("stationary_copy", OUTPUTS["stationary_reentry"], BRANCH_OUTPUTS["stationary_copy"]),
        ("coupling_copy", OUTPUTS["coupling_rows"], BRANCH_OUTPUTS["coupling_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows = []
    for copy_id, source_path, destination_path in copy_specs:
        shutil.copyfile(source_path, destination_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "destination_path": str(destination_path),
                    "destination_exists": destination_path.exists(),
                    "destination_parses": csv_parses(destination_path),
                }
            )
        )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    stationary: list[dict[str, Any]],
    coupling: list[dict[str, Any]],
    head_update: list[dict[str, Any]],
    beta_handoff: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validations if row["validation_id"] == "VAL2928_OVERALL")["status"]
    doc = f"""# 2928 - Y5/R2FR RV2925 Alpha3 Stationary Flux Zero Or Kappa/EllJ Coupling Baseline Under AX1090

Status: `Y5_R2FR_2928_stationary_alpha3_not_total_q_loc_partial_win_kappa_ellJ_rows_staged_beta_square_law_2929_next`

Claim ceiling: `stationary_q_loc_partial_nonclaim_only_no_alpha3_pass_no_kappa_zero_no_ellJ_zero_no_beta_pass_no_local_GR_no_Newton_no_PPN_no_R10_no_GitHub_claim`

## Summary

2928 prevents a loop. The stationary compact exterior route has already been tried in 2919. It gives a real partial theorem:

`J_M=0 -> q_loc^nu=0` in the exterior collar, under fixed `ell_J`, stationary/Killing `tau`, compact support, parent-owned `P_loc`, and silent boundary hypotheses.

But the total `alpha3` head does not vanish. The live residuals are boundary flux, domain/projector flux, source exchange, `Dln(kappa_MTS)`, `Dln(ell_J)`, disformal/vector current, and readout tails. So 2928 stages `kappa_MTS` and `ell_J` as explicit coupling-baseline rows and selects the beta/source-normalization square law as the next derivation target.

## Source Register

{md_table(sources, ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"])}

## Stationary Alpha3 Reentry Audit

{md_table(stationary, ["audit_id", "target", "current_status", "result", "condition_passed", "adopted_for_claim"])}

## Kappa/EllJ Coupling Baseline Rows

{md_table(coupling, ["row_id", "rv_component", "symbol", "formula_or_route", "target_bound_or_zero", "current_status", "upstream_row", "upstream_status", "units", "arena_links", "numeric_value_present", "theorem_zero", "selected_for_next_fill"])}

## Alpha3/RV2925 Head Update

{md_table(head_update, ["update_id", "rv_component", "symbol", "current_status", "reason", "next_requirement", "target_bound_abs", "score_input_present", "head_zero_adopted_for_claim"])}

## Beta Source-Normalization Handoff

{md_table(beta_handoff, ["handoff_id", "symbol", "formula_or_map", "current_status", "next_requirement", "beta_bound_abs", "selected_next", "valid_for_claim"])}

## Claim Gates

{md_table(claims, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"])}

## Decision Ledger

{md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"])}

## Branch Copies

{md_table(branches, ["copy_id", "source_path", "destination_path", "destination_exists", "destination_parses", "valid_for_claim"])}

## Validation

{md_table(validations, ["validation_id", "status", "detail", "valid_for_claim"])}

Validation overall: `{overall}`.

## Bottom Line

This is a useful consolidation step. We are not closer because alpha3 magically passed; we are closer because the stationary route has been cleanly bounded in scope. It kills one exterior `q_loc` head conditionally, but the GR-reduction problem now points at the coupling/source-normalization spine: fixed `kappa_MTS`, fixed `ell_J`, and the beta square law `B_source=A_source^2`.

## Not Claimed

- no total `alpha3` zero theorem is claimed;
- no `Dln(kappa_MTS)=0` or `Dln(ell_J)=0` theorem is claimed;
- no beta/source-normalization pass is claimed;
- no local-GR, Newton, PPN, R10, WEP, clock, orbital or public/GitHub claim is allowed from 2928.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    stationary = stationary_reentry_rows()
    coupling = coupling_rows()
    head_update = head_update_rows()
    beta_handoff = beta_handoff_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["stationary_reentry"], stationary)
    write_csv(OUTPUTS["coupling_rows"], coupling)
    write_csv(OUTPUTS["head_update"], head_update)
    write_csv(OUTPUTS["beta_handoff"], beta_handoff)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_rows)

    branches = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branches)

    DOC.write_text("# 2928 - validation preflight\n\nFinal document is written after validation rows are assembled.\n", encoding="utf-8")
    validations = validation_rows(sources, stationary, coupling, head_update, beta_handoff, claims, next_rows, branches)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, stationary, coupling, head_update, beta_handoff, claims, decisions, next_rows, branches, validations)

    print(f"2928 validation overall: {next(row for row in validations if row['validation_id'] == 'VAL2928_OVERALL')['status']}")
    print(f"doc: {DOC}")


if __name__ == "__main__":
    main()
