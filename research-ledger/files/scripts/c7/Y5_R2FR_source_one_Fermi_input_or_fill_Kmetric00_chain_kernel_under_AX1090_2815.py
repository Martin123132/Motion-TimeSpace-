from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
MTS = WORK / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
DOC = WORK / "2815-Y5-R2FR-source-one-Fermi-input-or-fill-Kmetric00-chain-kernel-under-AX1090.md"

SRC_2814_NEXT = MTS / "P8_Y5_R2FR_2814_NEXT_TARGET.csv"
SRC_2814_REQ = MTS / "P8_Y5_R2FR_2814_REQUIRED_INPUTS_TO_SCORE.csv"
SRC_2814_KMETRIC = MTS / "P8_Y5_R2FR_2814_KMETRIC00_KERNEL_FALLBACK_LEDGER.csv"
SRC_1210_GAPS = MTS / "P8_Y5_R10_1210_SOURCE_GAPS.csv"
SRC_1210_GRID = MTS / "P8_Y5_R10_1210_FERMI_BRACKET_GRID.csv"
SRC_1289_DERIV = MTS / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv"
SRC_1289_EXPANSION = MTS / "P8_Y5_R10_1289_KMETRIC_VARIATION_EXPANSION_NONCLAIM.csv"
SRC_1289_DELTAK = MTS / "P8_Y5_R10_1289_DELTAK00_COMPARISON_TEMPLATE.csv"
SRC_2808_METRIC = MTS / "P8_Y5_R2FR_2808_METRIC_RESPONSE_DERIVATION_ATTEMPT.csv"
SRC_2808_UNITS = MTS / "P8_Y5_R2FR_2808_WARD_RESIDUAL_UNIT_CONTRACT.csv"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2815_SOURCE_REGISTER.csv",
    "fermi_hunt": MTS / "P8_Y5_R2FR_2815_FERMI_INPUT_SOURCE_HUNT.csv",
    "hilbert_sign": MTS / "P8_Y5_R2FR_2815_KMETRIC_HILBERT_SIGN_DERIVATION.csv",
    "kernel_update": MTS / "P8_Y5_R2FR_2815_KMETRIC00_KERNEL_UPDATE.csv",
    "gates": MTS / "P8_Y5_R2FR_2815_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2815_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2815_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2815_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2815_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "fermi_queue": RAB_QUEUE / "JR2815_FERMI_INPUT_SOURCE_HUNT_NONCLAIM.csv",
    "hilbert_queue": RAB_QUEUE / "JR2815_KMETRIC_HILBERT_SIGN_DERIVATION_NONCLAIM.csv",
    "kernel_queue": RAB_QUEUE / "JR2815_KMETRIC00_KERNEL_UPDATE_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2815_NEXT_KERNEL_NORMALIZATION_OR_ZERO_PROOF.csv",
    "beta_doc": BETA_DOCS / "KMETRIC_HILBERT_SIGN_DERIVATION_2815_NONCLAIM.csv",
    "local_bound_copy": LOCAL_BOUNDS / "Kmetric00_hilbert_sign_2815_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_Kmetric_hilbert_sign_2815_nonclaim.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sp(path: Path) -> str:
    return str(path)


def ensure_dirs() -> None:
    directories = {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def anchor_found(path: Path, anchor: str) -> bool:
    return anchor in read_text(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def local_path_tokens(value: Any) -> list[Path]:
    if value is None:
        return []
    tokens = str(value).split(";")
    paths: list[Path] = []
    for token in tokens:
        item = token.strip()
        if not item or item == "MISSING" or item.startswith("http"):
            continue
        candidate = Path(item)
        if not candidate.is_absolute():
            candidate = WORK / item
        if candidate.suffix or candidate.drive:
            paths.append(candidate)
    return paths


def build_sources() -> list[dict[str, Any]]:
    entries = [
        ("SRC2815_0_2814_next", SRC_2814_NEXT, "NEXT2814_0_2815", "handoff target for 2815"),
        ("SRC2815_1_2814_requirements", SRC_2814_REQ, "REQ2814_0_LD", "current required Fermi input ledger"),
        ("SRC2815_2_1210_gaps", SRC_1210_GAPS, "GAP1210_2_real_curvature_profile", "earlier real curvature/domain source gap"),
        ("SRC2815_3_1210_grid", SRC_1210_GRID, "FBG1210_000", "diagnostic grid proving 1210 numbers are smoke only"),
        ("SRC2815_4_2814_kmetric", SRC_2814_KMETRIC, "KMF2814_0_kernel_template", "Kmetric00 fallback handoff"),
        ("SRC2815_5_1289_derivative", SRC_1289_DERIV, "KDR1289_0_Gamma_m_L_chain_kernel_00", "chain-kernel sign slot"),
        ("SRC2815_6_1289_expansion", SRC_1289_EXPANSION, "KVE1289_0_action_convention", "Kmetric action convention row"),
        ("SRC2815_7_1289_delta", SRC_1289_DELTAK, "DTC1289_1_Kmetric_partial", "DeltaK00 partial Kmetric structure"),
        ("SRC2815_8_2808_metric", SRC_2808_METRIC, "MRD2808_1_stress_split", "Hilbert-stress and Kmetric split convention"),
        ("SRC2815_9_2808_units", SRC_2808_UNITS, "UNIT2808_1_Kmetric", "Kmetric unit contract"),
    ]
    return [
        {
            "source_id": source_id,
            "path_or_url": sp(path),
            "anchor": anchor,
            "role": role,
            "path_exists": path.exists(),
            "anchor_found": anchor_found(path, anchor),
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for source_id, path, anchor, role in entries
    ]


def build_fermi_hunt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FIH2815_0_LD",
            "L_D",
            "domain radius/diameter in same norm as curvature",
            "m",
            SRC_2814_REQ,
            "REQ2814_0_LD",
            "MISSING_LENGTH_SCALE",
            "No source-backed local domain definition is present in 1210/2814; smoke-grid L_D values cannot be promoted.",
        ),
        (
            "FIH2815_1_Riemann",
            "Riemann_norm",
            "curvature supremum over explicit local Fermi domain",
            "m^-2",
            SRC_2814_REQ,
            "REQ2814_1_Riemann",
            "MISSING_CURVATURE_PROFILE",
            "1210 only supplies diagnostic curvature probes; no arena/domain/norm source row is score-ready.",
        ),
        (
            "FIH2815_2_nablaR",
            "nabla_Riemann_norm",
            "curvature-gradient supremum over explicit local Fermi domain",
            "m^-3",
            SRC_2814_REQ,
            "REQ2814_2_nablaR",
            "MISSING_CURVATURE_GRADIENT_PROFILE",
            "Second-order Fermi control remains absent, so the curvature bundle cannot be claimed.",
        ),
        (
            "FIH2815_3_CFermi",
            "C_Fermi;C_Fermi2",
            "operator constants for Fermi drift estimate",
            "dimensionless",
            SRC_2814_REQ,
            "REQ2814_3_CFermi",
            "MISSING_OPERATOR_CONSTANTS",
            "No same-norm operator bound is present; use only symbolic/smoke constants.",
        ),
        (
            "FIH2815_4_guards",
            "domain_motion_Linf;projector_stress_Linf",
            "local branch guard terms",
            "norm-defined",
            SRC_2814_REQ,
            "REQ2814_5_guards",
            "MISSING_DOMAIN_STRESS_GUARDS",
            "The clean branch cannot silently set guard terms to zero.",
        ),
        (
            "FIH2815_5_hunt_verdict",
            "real Fermi numeric input",
            "source one score-ready Fermi input",
            "mixed",
            SRC_1210_GAPS,
            "GAP1210_2_real_curvature_profile",
            "NO_REAL_FERMI_INPUT_SOURCED_IN_2815",
            "The honest move is to pivot to the Kmetric00 kernel fallback rather than turn smoke numbers into evidence.",
        ),
    ]
    return [
        {
            "hunt_id": hunt_id,
            "quantity": quantity,
            "definition": definition,
            "units": units,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "numeric_value": "MISSING",
            "source_backed_numeric": False,
            "status": status,
            "finding": finding,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for hunt_id, quantity, definition, units, source_path, anchor, status, finding in rows
    ]


def build_hilbert_sign_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KHS2815_0_stress_split",
            "K_metric^{mu nu}",
            "Given S_GK=-int sqrt(-g) Gamma_eff and T_GK^{mu nu}:=-2/sqrt(-g) delta S_GK/delta g_{mu nu}, define K_metric^{mu nu}:=Gamma_eff g^{mu nu}-T_GK^{mu nu}.",
            "definition",
            "same covariant metric-variation slot as 2808; no Khat equality assumed",
            SRC_2808_METRIC,
            "MRD2808_1_stress_split",
            "SOURCE_BACKED_CONVENTION",
        ),
        (
            "KHS2815_1_pre_kernel_multiplier",
            "C_Hilbert_pre_kernel",
            "For the raw chain variation delta Gamma_chain/delta g_{mu nu}, the 2808 split gives K_metric_chain^{mu nu}=-2 delta Gamma_chain/delta g_{mu nu}.",
            "-2",
            "only valid if M_m^{00} and M_L^{00} are raw metric-response kernels, not already Hilbert-normalized",
            SRC_2808_METRIC,
            "MRD2808_1_stress_split",
            "DERIVED_PRE_KERNEL_SIGN_NONCLAIM",
        ),
        (
            "KHS2815_2_chain_formula_insert",
            "Kmetric_chain^{00}",
            "Kmetric_chain^{00}=(-2)[L_cg^-2 F_prime(m) M_m_raw^{00}-2 L_cg^-3 F(m) M_L_raw^{00}] plus connection/domain/boundary terms.",
            "formal",
            "requires raw-kernel normalization map and same metric slot before exporting C_sign to 1289",
            SRC_1289_DERIV,
            "KDR1289_0_Gamma_m_L_chain_kernel_00",
            "FORMULA_FILLED_UNDER_RAW_KERNEL_CONDITION",
        ),
        (
            "KHS2815_3_export_blocker",
            "C_sign_export",
            "The final 1289 C_sign is still not score-ready because 1289 does not define whether M_m^{00}/M_L^{00} include the Hilbert factor or metric-slot sign.",
            "MISSING_KERNEL_NORMALIZATION_MAP",
            "must distinguish covariant g_{mu nu}, contravariant g^{mu nu}, and Hilbert-normalized kernels",
            SRC_1289_EXPANSION,
            "KVE1289_2_metric_response_kernels",
            "EXPORT_BLOCKED_NOT_CLAIM_READY",
        ),
    ]
    return [
        {
            "row_id": row_id,
            "object": obj,
            "derivation_or_statement": statement,
            "value_or_status": value,
            "conditions": conditions,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "status": status,
            "generated_utc": utc_now(),
        }
        for row_id, obj, statement, value, conditions, source_path, anchor, status in rows
    ]


def build_kernel_update_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KUU2815_0_original_kernel",
            "Kmetric_chain^{00}",
            "2814/1289 kernel template remains structurally valid.",
            "C_sign slot identified; no numeric M_m/M_L/connection/domain/boundary kernels.",
            SRC_2814_KMETRIC,
            "KMF2814_0_kernel_template",
            "PARTIAL_KERNEL_TEMPLATE_AVAILABLE",
            "MISSING_C_SIGN_EXPORT;MISSING_M_m_00;MISSING_M_L_00;MISSING_K_CONN_00;MISSING_K_DOMAIN_00;MISSING_K_BOUNDARY_00",
        ),
        (
            "KUU2815_1_hilbert_progress",
            "C_Hilbert_pre_kernel",
            "The Hilbert multiplier before kernel normalization is derived as -2 under the 2808 stress split.",
            "This is real algebraic progress but not a local-gravity score.",
            SRC_2808_METRIC,
            "MRD2808_1_stress_split",
            "PRE_KERNEL_SIGN_FILLED_NONCLAIM",
            "MISSING_KERNEL_NORMALIZATION_MAP",
        ),
        (
            "KUU2815_2_final_export",
            "C_sign_export",
            "Do not export a final C_sign into the 1289 template until M_m^{00}/M_L^{00} declare raw vs Hilbert-normalized kernels.",
            "Prevents a silent factor-of-minus-two/factor-of-two error.",
            SRC_1289_EXPANSION,
            "KVE1289_2_metric_response_kernels",
            "EXPORT_BLOCKED_BY_NORMALIZATION",
            "MISSING_RAW_KERNEL_DEFINITION;MISSING_METRIC_SLOT_MAP",
        ),
    ]
    return [
        {
            "update_id": update_id,
            "quantity": quantity,
            "finding": finding,
            "consequence": consequence,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "status": status,
            "missing_before_claim": missing,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for update_id, quantity, finding, consequence, source_path, anchor, status, missing in rows
    ]


def build_gate_rows(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    fermi_sourced = any(row["source_backed_numeric"] for row in sections["fermi_hunt"])
    pre_kernel_sign = any(row["row_id"] == "KHS2815_1_pre_kernel_multiplier" and row["value_or_status"] == "-2" for row in sections["hilbert_sign"])
    export_ready = False
    rows = [
        ("CG2815_0_sources_anchored", "2815 source anchors are present", all(row["anchor_found"] for row in sections["sources"]), "all required local anchors were found"),
        ("CG2815_1_real_fermi_input", "one real Fermi numeric input was sourced", fermi_sourced, "no source-backed L_D/curvature/C_Fermi/guard row exists yet"),
        ("CG2815_2_hilbert_pre_kernel_sign", "Hilbert pre-kernel multiplier is derived", pre_kernel_sign, "2808 stress split fixes the raw-chain multiplier as -2"),
        ("CG2815_3_final_Csign_export", "final 1289 C_sign can be exported", export_ready, "M_m/M_L kernel normalization and metric slot are still missing"),
        ("CG2815_4_Kmetric00_score", "Kmetric00 branch can be scored", False, "M_m, M_L, K_conn, K_domain, K_boundary and DeltaK norms remain unsourced"),
        ("CG2815_5_local_claim", "local-GR/WEP/PPN/orbital claim can be made", False, "2815 is algebraic plumbing only; no local branch pass is claimed"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for gate_id, claim, gate_pass, reason in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2815_0_no_fermi_promotion",
            "Do not promote 1210/2814 Fermi smoke values.",
            "They are useful scaling probes but not source-backed local arena inputs.",
            "source a real domain/curvature/norm profile later or keep the branch blocked",
        ),
        (
            "DEC2815_1_tensor_progress",
            "The tensor fallback moved forward by one clean algebraic step.",
            "Under the 2808 Hilbert-stress split, the raw chain metric-response multiplier is -2.",
            "define the raw-vs-Hilbert normalization of M_m^{00} and M_L^{00}",
        ),
        (
            "DEC2815_2_main_risk",
            "The remaining danger is a hidden sign/factor convention, not philosophy.",
            "Exporting C_sign before kernel normalization could bake in a factor-of-two or metric-slot error.",
            "make 2816 a kernel-normalization map or local M_m/M_L zero proof",
        ),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for decision_id, decision, because, next_action in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2815_0_2816",
            "next_target": "2816-Y5-R2FR-Kmetric00-kernel-normalization-map-or-Mm-ML-zero-proof-under-AX1090.md",
            "script": "scripts/Y5_R2FR_Kmetric00_kernel_normalization_map_or_Mm_ML_zero_proof_under_AX1090_2816.py",
            "objective": "define whether M_m^{00} and M_L^{00} are raw metric-response kernels or Hilbert-normalized kernels, then export C_sign safely; if the local fixed-point branch proves M_m^{00}=M_L^{00}=0, record the zero proof instead",
            "include": "metric variation slot; raw/Hilbert kernel normalization; units; source paths; no measured-G absorption; connection/domain/boundary blockers retained",
            "exclude": "promoting KL00 to live Khat00; declaring local-GR/WEP/PPN/orbital pass; using smoke Fermi values as evidence; GitHub; formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["fermi_hunt"], BRANCH_OUTPUTS["fermi_queue"], "fermi_queue"),
        (OUTPUTS["hilbert_sign"], BRANCH_OUTPUTS["hilbert_queue"], "hilbert_queue"),
        (OUTPUTS["kernel_update"], BRANCH_OUTPUTS["kernel_queue"], "kernel_queue"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
        (OUTPUTS["hilbert_sign"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["hilbert_sign"], BRANCH_OUTPUTS["local_bound_copy"], "local_bound_copy"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2815_{label}",
                "source": sp(source),
                "destination": sp(destination),
                "exists": destination.exists(),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def claim_flags_true(sections: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in sections.items():
        if key == "validation":
            continue
        for row in rows:
            if str(row.get("valid_for_claim", "false")).lower() == "true":
                return True
            if str(row.get("claim_allowed", "false")).lower() == "true":
                return True
    return False


def cited_paths_exist(sections: dict[str, list[dict[str, Any]]]) -> bool:
    paths: list[Path] = []
    for rows in sections.values():
        for row in rows:
            for key in ("source_path", "source_paths", "source", "destination", "path_or_url"):
                paths.extend(local_path_tokens(row.get(key)))
    return all(path.exists() for path in paths)


def formalization_untouched_since_run() -> bool:
    if not FORMALIZATION.exists():
        return True
    threshold = RUN_STARTED_UTC.timestamp()
    return not any(path.is_file() and path.stat().st_mtime >= threshold for path in FORMALIZATION.rglob("*"))


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2815_0_sources_exist", all(row["path_exists"] for row in sections["sources"]), "all source-register local paths exist"),
        ("VAL2815_1_source_anchors", all(row["anchor_found"] for row in sections["sources"]), "all source-register anchors were found"),
        ("VAL2815_2_fermi_hunt_anchored", all(row["anchor_found"] for row in sections["fermi_hunt"]), "all Fermi source-hunt anchors were found"),
        ("VAL2815_3_no_fermi_numeric_promoted", all(not row["source_backed_numeric"] for row in sections["fermi_hunt"]), "no Fermi smoke value was promoted to evidence"),
        ("VAL2815_4_hilbert_sign_derived", any(row["row_id"] == "KHS2815_1_pre_kernel_multiplier" and row["value_or_status"] == "-2" for row in sections["hilbert_sign"]), "pre-kernel Hilbert multiplier -2 was recorded"),
        ("VAL2815_5_final_Csign_blocked", any(row["object"] == "C_sign_export" and row["status"] == "EXPORT_BLOCKED_NOT_CLAIM_READY" for row in sections["hilbert_sign"]), "final C_sign export remains blocked"),
        ("VAL2815_6_kernel_update_anchored", all(row["anchor_found"] for row in sections["kernel_update"]), "kernel update anchors were found"),
        ("VAL2815_7_kernel_update_safe", all(not row["score_ready"] and not row["claim_allowed"] for row in sections["kernel_update"]), "kernel updates remain nonclaim"),
        ("VAL2815_8_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2815_9_next_target_2816", any(row["next_id"] == "NEXT2815_0_2816" for row in sections["next"]), "next target is 2816"),
        ("VAL2815_10_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2815_11_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2815_12_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2815_13_cited_paths_exist", cited_paths_exist(sections), "all cited local file/copy paths in generated rows exist"),
        ("VAL2815_14_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2815_15_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2815_16_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2815_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2815_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2815 does not source a real Fermi input, but derives the Hilbert pre-kernel sign -2 for Kmetric00 under the 2808 convention and blocks final C_sign export until kernel normalization is mapped.",
            "generated_utc": utc_now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
        + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2815 - Y5 R2FR Source One Fermi Input Or Fill Kmetric00 Chain Kernel Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2815 tried the cleanest route first: source one real Fermi input from the existing 1210/2814 chain. That route remains blocked. `L_D`, `Riemann_norm`, `nabla_Riemann_norm`, `C_Fermi`, and guard terms are still smoke-grid or missing rows, so no Fermi value is promoted to evidence.",
        "",
        "The fallback tensor route does make a real algebraic step. Under the 2808 Hilbert-stress split, if `M_m^{00}` and `M_L^{00}` are raw metric-response kernels, the chain contribution carries the pre-kernel multiplier `C_Hilbert_pre_kernel=-2`.",
        "",
        "This is not yet the final exported `C_sign` in 1289. The final sign/factor remains blocked until 2816 states whether `M_m^{00}` and `M_L^{00}` are raw kernels or already Hilbert-normalized, and whether the metric slot is covariant or contravariant. No local-GR/WEP/PPN/orbital claim is made.",
        "",
        "## Fermi Input Source Hunt",
        markdown_table(sections["fermi_hunt"], ["hunt_id", "quantity", "status", "source_backed_numeric", "anchor_found", "finding"]),
        "",
        "## Kmetric Hilbert Sign Derivation",
        markdown_table(sections["hilbert_sign"], ["row_id", "object", "value_or_status", "status", "conditions", "anchor_found"]),
        "",
        "## Kmetric00 Kernel Update",
        markdown_table(sections["kernel_update"], ["update_id", "quantity", "status", "missing_before_claim", "anchor_found"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "claim", "gate_pass", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "fermi_hunt": build_fermi_hunt_rows(),
        "hilbert_sign": build_hilbert_sign_rows(),
        "kernel_update": build_kernel_update_rows(),
    }
    sections["gates"] = build_gate_rows(sections)
    sections["decision"] = build_decision_rows()
    sections["next"] = build_next_rows()

    for key, rows in sections.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)
    sections["branches"] = copy_branches()
    write_csv(OUTPUTS["branches"], sections["branches"])
    sections["validation"] = build_validation(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    DOC.write_text(build_doc(sections), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation overall: {sections['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()
