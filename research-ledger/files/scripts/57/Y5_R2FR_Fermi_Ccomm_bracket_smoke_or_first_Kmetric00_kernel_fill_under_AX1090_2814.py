from __future__ import annotations

import csv
import math
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
DOC = WORK / "2814-Y5-R2FR-Fermi-Ccomm-bracket-smoke-or-first-Kmetric00-kernel-fill-under-AX1090.md"

TARGET_Q_PROJECTOR = 1.1723321502596888e-05

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2814_SOURCE_REGISTER.csv",
    "assumptions": MTS / "P8_Y5_R2FR_2814_FERMI_BRACKET_ASSUMPTIONS.csv",
    "bracket": MTS / "P8_Y5_R2FR_2814_FERMI_CCOMM_BRACKET_SMOKE.csv",
    "requirements": MTS / "P8_Y5_R2FR_2814_REQUIRED_INPUTS_TO_SCORE.csv",
    "kmetric": MTS / "P8_Y5_R2FR_2814_KMETRIC00_KERNEL_FALLBACK_LEDGER.csv",
    "gates": MTS / "P8_Y5_R2FR_2814_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2814_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2814_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2814_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2814_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "bracket_queue": RAB_QUEUE / "JR2814_FERMI_CCOMM_BRACKET_SMOKE_NONCLAIM.csv",
    "requirements_queue": RAB_QUEUE / "JR2814_REQUIRED_INPUTS_TO_SCORE_NONCLAIM.csv",
    "kmetric_queue": RAB_QUEUE / "JR2814_KMETRIC00_KERNEL_FALLBACK_LEDGER_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "FERMI_CCOMM_BRACKET_SMOKE_2814_NONCLAIM.csv",
    "local_bound_copy": LOCAL_BOUNDS / "Fermi_Ccomm_bracket_smoke_2814_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_Fermi_Ccomm_bracket_2814_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2814_NEXT_NUMERIC_INPUT_OR_KMETRIC_KERNEL.csv",
}

SRC_2813_NEXT = MTS / "P8_Y5_R2FR_2813_NEXT_TARGET.csv"
SRC_2813_CCOMM = MTS / "P8_Y5_R2FR_2813_FIRST_CCOMM_ANALYTIC_SOURCE_ROW.csv"
SRC_2813_QBOUND = MTS / "P8_Y5_R2FR_2813_QDELTAK_BOUND_WITH_FERMI_CCOMM.csv"
SRC_1209_PRESSURE = MTS / "P8_Y5_R10_1209_PRESSURE_SMOKE_SCHEMA.csv"
SRC_1209_UNIFIED = MTS / "P8_Y5_R10_1209_UNIFIED_SOURCE_PACK.csv"
SRC_1209_FERMI = MTS / "P8_Y5_R10_1209_FERMI_DOMAIN_DERIVATION.csv"
SRC_1209_DOMAIN = MTS / "P8_Y5_R10_1209_DOMAIN_MOTION_PROJECTOR_STRESS_AUDIT.csv"
SRC_1289_DERIV = MTS / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv"
SRC_1289_DELTAK = MTS / "P8_Y5_R10_1289_DELTAK00_COMPARISON_TEMPLATE.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sp(path: Path) -> str:
    return str(path)


def ensure_dirs() -> None:
    directories = {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}
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


def build_sources() -> list[dict[str, Any]]:
    local_sources = [
        ("2813_next", SRC_2813_NEXT, "authoritative 2814 target"),
        ("2813_ccomm_row", SRC_2813_CCOMM, "analytic C_comm_parallel Fermi row"),
        ("2813_qbound", SRC_2813_QBOUND, "q_DeltaK bound with Fermi C_comm"),
        ("1209_pressure_schema", SRC_1209_PRESSURE, "q_projector pressure target and blocker policy"),
        ("1209_unified_pack", SRC_1209_UNIFIED, "required source inputs for Fermi bracket"),
        ("1209_fermi_derivation", SRC_1209_FERMI, "Fermi-domain derivation source"),
        ("1209_domain_audit", SRC_1209_DOMAIN, "domain-motion/projector-stress guard source"),
        ("1289_derivative_kernel", SRC_1289_DERIV, "Kmetric00 kernel fallback source"),
        ("1289_delta_template", SRC_1289_DELTAK, "DeltaK00 comparison template"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role in local_sources:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_file",
                "path_or_url": sp(path),
                "exists_or_reachable": path.exists(),
                "contains_text": bool(text.strip()) if path.exists() else False,
                "role": role,
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def build_assumption_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ASM2814_0_smoke_not_evidence",
            "bracket values are diagnostic parameter probes",
            "not source-backed local measurements; not evidence for local-GR/WEP/PPN recovery",
            SRC_1209_PRESSURE,
            "PSC1209_4_blocker_policy",
        ),
        (
            "ASM2814_1_clean_branch",
            "clean Fermi branch assumes coframe/domain/projector-stress guards are zero or separately bounded",
            "if any guard remains MISSING, claim_allowed stays false",
            SRC_1209_PRESSURE,
            "PSC1209_1_full_projector_budget",
        ),
        (
            "ASM2814_2_target",
            f"q_projector target is {TARGET_Q_PROJECTOR:.16e}",
            "inherited from the 1208/1209 pressure schemas; used only for required C_P*G_res budget",
            SRC_1209_PRESSURE,
            "PSC1209_0_clean_fermi_projector",
        ),
        (
            "ASM2814_3_curvature_bundle",
            "curvature_bundle := Riemann_norm + L_D*nabla_Riemann_norm",
            "the smoke grid uses this bundle so the second-order Fermi term is not silently dropped",
            SRC_2813_CCOMM,
            "FSR2813_0_Ccomm_parallel_Fermi",
        ),
    ]
    return [
        {
            "assumption_id": row[0],
            "assumption": row[1],
            "effect": row[2],
            "source_path": sp(row[3]),
            "source_anchor": row[4],
            "anchor_found": anchor_found(row[3], row[4]),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_bracket_rows() -> list[dict[str, Any]]:
    scenarios = [
        ("FB2814_0_tiny_lab", 1.0e-1, 1.0e-26, 1.0, "tiny finite lab domain; weak curvature bundle"),
        ("FB2814_1_meter_lab", 1.0, 1.0e-24, 10.0, "meter-scale domain; conservative curvature-bundle smoke"),
        ("FB2814_2_large_lab", 10.0, 1.0e-23, 10.0, "larger local domain; still diagnostic"),
        ("FB2814_3_strong_curvature", 1.0, 1.0e-18, 100.0, "stress test with much larger curvature bundle"),
        ("FB2814_4_big_domain_stress", 1.0e3, 1.0e-18, 100.0, "large-domain stress probe"),
        ("FB2814_5_extreme_fail_probe", 1.0e3, 1.0e-12, 100.0, "deliberately harsh probe to expose scaling"),
    ]
    rows = []
    for scenario_id, domain_radius_m, curvature_bundle_m2, c_fermi_eff, note in scenarios:
        ccomm_parallel = c_fermi_eff * domain_radius_m * curvature_bundle_m2
        required_cpgres = math.inf if ccomm_parallel == 0 else TARGET_Q_PROJECTOR / ccomm_parallel
        rows.append(
            {
                "scenario_id": scenario_id,
                "domain_radius_LD_m": f"{domain_radius_m:.6e}",
                "curvature_bundle_m_minus_2": f"{curvature_bundle_m2:.6e}",
                "C_Fermi_eff": f"{c_fermi_eff:.6e}",
                "Ccomm_parallel_m_minus_1": f"{ccomm_parallel:.6e}",
                "target_q_projector": f"{TARGET_Q_PROJECTOR:.16e}",
                "required_CPloc_times_Gres_max_if_guards_zero": f"{required_cpgres:.6e}",
                "interpretation": "diagnostic_only_large_required_budget_is_not_claim_evidence",
                "note": note,
                "score_ready": False,
                "claim_allowed": False,
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def build_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("REQ2814_0_LD", "L_D", "domain radius/diameter in the same norm as curvature", "m", SRC_1209_UNIFIED, "USP1209_1_LD", "MISSING_LENGTH_SCALE"),
        ("REQ2814_1_Riemann", "Riemann_norm", "curvature supremum over the local Fermi domain", "m^-2", SRC_1209_UNIFIED, "USP1209_2_Riemann", "MISSING_CURVATURE_PROFILE"),
        ("REQ2814_2_nablaR", "nabla_Riemann_norm", "curvature-gradient supremum over the local Fermi domain", "m^-3", SRC_1209_UNIFIED, "USP1209_3_nablaR", "MISSING_CURVATURE_GRADIENT_PROFILE"),
        ("REQ2814_3_CFermi", "C_Fermi;C_Fermi2", "norm constants for Fermi projector drift estimate", "dimensionless", SRC_1209_UNIFIED, "USP1209_4_CFermi", "MISSING_OPERATOR_CONSTANTS"),
        ("REQ2814_4_CP_Gres", "C_P;G_res_norm", "same-norm multiplier and local residual norm needed to score q_projector", "norm-defined", SRC_1209_UNIFIED, "USP1209_6_CP", "MISSING_OPERATOR_CONSTANT_AND_GRES"),
        ("REQ2814_5_guards", "domain_motion_Linf;projector_stress_Linf", "guard terms that must be zero or bounded in the same local domain", "m^-1 or norm-defined", SRC_1209_DOMAIN, "DMP1209_4_total_epsilon_status", "MISSING_DOMAIN_STRESS_GUARDS"),
        ("REQ2814_6_DeltaK", "||Delta_K|| and D_Delta", "component residual norm and derivative envelope multiplying operator constants", "stress and force-density", SRC_2813_QBOUND, "QBF2813_1_updated_bound", "MISSING_DELTAK_COMPONENT_NORMS"),
    ]
    return [
        {
            "requirement_id": row[0],
            "quantity": row[1],
            "definition": row[2],
            "units": row[3],
            "source_path": sp(row[4]),
            "source_anchor": row[5],
            "status": row[6],
            "anchor_found": anchor_found(row[4], row[5]),
            "numeric_value": "MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_kmetric_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KMF2814_0_kernel_template",
            "Kmetric_chain^{00}",
            "symbolic derivative kernel exists",
            SRC_1289_DERIV,
            "KDR1289_0_Gamma_m_L_chain_kernel_00",
            "Kmetric_chain^{00}=C_sign[L_cg^-2 F_prime(m) M_m^{00}-2 L_cg^-3 F(m) M_L^{00}] plus K_conn^{00}+K_domain^{00}+K_boundary^{00}",
            "PARTIAL_KERNEL_TEMPLATE_AVAILABLE",
            "MISSING_C_SIGN;MISSING_M_m_00;MISSING_M_L_00;MISSING_K_CONN_00;MISSING_K_DOMAIN_00;MISSING_K_BOUNDARY_00",
        ),
        (
            "KMF2814_1_zero_gate",
            "Kmetric_chain^{00}=0",
            "conditional zero gate exists but is not derived",
            SRC_1289_DERIV,
            "KDR1289_1_local_zero_condition_for_chain_kernel",
            "zero needs locked local fixed point, F_prime(m_*)=0, L_cg silence, and boundary/no-flux terms",
            "ZERO_GATE_CONDITIONAL_NOT_DERIVED",
            "MISSING_PARENT_LOCK_TO_m_STAR;MISSING_LCG_METRIC_SILENCE;MISSING_BOUNDARY_NO_FLUX",
        ),
        (
            "KMF2814_2_fallback_decision",
            "Kmetric route",
            "not filled numerically in 2814 because the Fermi bracket row exists",
            SRC_1289_DELTAK,
            "DTC1289_2_DeltaK00_template",
            "DeltaK00 template remains available as the tensor fallback if Fermi inputs cannot be sourced",
            "FALLBACK_RETAINED_NONCLAIM",
            "next tensor target should fill C_sign or one of M_m^{00}/M_L^{00}/K_conn/K_domain/K_boundary",
        ),
    ]
    return [
        {
            "fallback_id": row[0],
            "quantity": row[1],
            "finding": row[2],
            "source_path": sp(row[3]),
            "source_anchor": row[4],
            "formula_or_statement": row[5],
            "status": row[6],
            "missing_before_claim": row[7],
            "anchor_found": anchor_found(row[3], row[4]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2814_0_bracket_run", "Fermi C_comm bracket smoke was run", True, "diagnostic grid exists"),
        ("CG2814_1_formula_source_backed", "Fermi C_comm formula is source-backed", True, "2813/1209 anchors are present"),
        ("CG2814_2_numeric_evidence", "bracket rows are physical evidence", False, "values are diagnostic probes, not sourced measurements"),
        ("CG2814_3_claim_ready_Ccomm", "C_comm_parallel is score-ready", False, "L_D, curvature, C_Fermi and guards remain unsourced"),
        ("CG2814_4_local_score", "local arena score can run", False, "C_P/G_res, Delta_K norms, guards and arena maps remain missing"),
        ("CG2814_5_Kmetric_fallback", "Kmetric00 fallback is staged", True, "1289 kernel template is cited"),
        ("CG2814_6_local_claim", "local-GR/WEP/PPN/orbital claim can be made", False, "no numeric/theorem-zero pass"),
        ("CG2814_7_nonclaim_pack", "2814 nonclaim bracket pack is ready", True, "next target is source one numeric bracket input or fill one Kmetric kernel"),
    ]
    return [
        {
            "gate_id": row[0],
            "claim": row[1],
            "gate_pass": row[2],
            "reason": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2814_0_bracket_useful",
            "The Fermi bracket is useful but not evidence.",
            "It shows the scaling of required C_Ploc*G_res against local domain and curvature assumptions.",
            "source one real bracket input next",
        ),
        (
            "DEC2814_1_missing_guards_dominate",
            "The main blockers are now concrete input rows.",
            "L_D, curvature bundle, C_Fermi, C_P/G_res and domain/projector-stress guards are all named.",
            "do not score until every guard is source-backed or theorem-zero",
        ),
        (
            "DEC2814_2_kmetric_fallback",
            "Kmetric^{00} remains the tensor fallback.",
            "1289 already has a partial chain-kernel template, but no kernel coefficient is filled.",
            "if numeric Fermi sourcing stalls, fill C_sign or one kernel row",
        ),
    ]
    return [
        {
            "decision_id": row[0],
            "decision": row[1],
            "because": row[2],
            "next_action": row[3],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2814_0_2815",
            "next_target": "2815-Y5-R2FR-source-one-Fermi-input-or-fill-Kmetric00-chain-kernel-under-AX1090.md",
            "script": "scripts/Y5_R2FR_source_one_Fermi_input_or_fill_Kmetric00_chain_kernel_under_AX1090_2815.py",
            "objective": "source one real numeric/bounded Fermi bracket input, preferably L_D plus a conservative curvature norm, or fill one Kmetric^{00} chain-kernel input such as C_sign, M_m^{00}, M_L^{00}, K_conn^{00}, K_domain^{00}, or K_boundary^{00}",
            "include": "actual source path; units; norm convention; domain definition; guard status; no measured-G absorption; Kmetric kernel fallback",
            "exclude": "treating bracket grid as evidence; optimistic hand-picked numbers; local-GR/WEP/PPN/orbital claim; promoting KL00 to live Khat00; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["bracket"], BRANCH_OUTPUTS["bracket_queue"], "bracket_queue"),
        (OUTPUTS["requirements"], BRANCH_OUTPUTS["requirements_queue"], "requirements_queue"),
        (OUTPUTS["kmetric"], BRANCH_OUTPUTS["kmetric_queue"], "kmetric_queue"),
        (OUTPUTS["bracket"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["bracket"], BRANCH_OUTPUTS["local_bound_copy"], "local_bound_copy"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2814_{label}",
                "source": sp(source),
                "destination": sp(destination),
                "exists": destination.exists(),
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def formalization_untouched_since_run() -> bool:
    if not FORMALIZATION.exists():
        return True
    threshold = RUN_STARTED_UTC.timestamp()
    return not any(path.is_file() and path.stat().st_mtime >= threshold for path in FORMALIZATION.rglob("*"))


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


def local_path_tokens(value: Any) -> list[Path]:
    if not value:
        return []
    paths: list[Path] = []
    for token in str(value).split(";"):
        token = token.strip()
        if not token or token == "MISSING" or token.startswith("http"):
            continue
        candidate = Path(token)
        if not candidate.is_absolute():
            candidate = WORK / candidate
        if candidate.suffix or candidate.drive:
            paths.append(candidate)
    return paths


def cited_paths_exist(sections: dict[str, list[dict[str, Any]]]) -> bool:
    paths: list[Path] = []
    for rows in sections.values():
        for row in rows:
            for key in ("source_path", "source_paths", "source", "destination", "path_or_url"):
                paths.extend(local_path_tokens(row.get(key)))
    return all(path.exists() for path in paths)


def bracket_rows_numeric(rows: list[dict[str, Any]]) -> bool:
    for row in rows:
        for key in ("domain_radius_LD_m", "curvature_bundle_m_minus_2", "C_Fermi_eff", "Ccomm_parallel_m_minus_1", "required_CPloc_times_Gres_max_if_guards_zero"):
            value = float(row[key])
            if not math.isfinite(value) or value <= 0:
                return False
    return True


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2814_0_sources_exist", all(row["exists_or_reachable"] for row in sections["sources"]), "all source-register local paths exist"),
        ("VAL2814_1_sources_nonempty", all(row["contains_text"] for row in sections["sources"]), "all source-register entries contain text/source evidence"),
        ("VAL2814_2_assumption_anchors", all(row["anchor_found"] for row in sections["assumptions"]), "all bracket assumption anchors were found"),
        ("VAL2814_3_bracket_numeric", bracket_rows_numeric(sections["bracket"]), "diagnostic bracket rows are finite positive numbers"),
        ("VAL2814_4_bracket_nonclaim", all(row["score_ready"] is False and row["claim_allowed"] is False for row in sections["bracket"]), "bracket rows are nonclaim smoke rows"),
        ("VAL2814_5_requirements_anchored", all(row["anchor_found"] for row in sections["requirements"]), "all required-input anchors were found"),
        ("VAL2814_6_kmetric_fallback_anchored", all(row["anchor_found"] for row in sections["kmetric"]), "Kmetric fallback anchors were found"),
        ("VAL2814_7_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2814_8_next_target_2815", any(row["next_id"] == "NEXT2814_0_2815" for row in sections["next"]), "next target is 2815"),
        ("VAL2814_9_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2814_10_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2814_11_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2814_12_cited_paths_exist", cited_paths_exist(sections), "all cited local file/copy paths in generated rows exist"),
        ("VAL2814_13_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2814_14_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2814_15_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2814_16_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2814_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2814 runs a conservative nonclaim Fermi C_comm bracket smoke map, preserves guard blockers, and stages Kmetric00 kernel fallback.",
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
        "# 2814 - Y5 R2FR Fermi Ccomm Bracket Smoke Or First Kmetric00 Kernel Fill Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2814 runs the first conservative Fermi `C_comm_parallel` bracket smoke map. This is diagnostic plumbing, not evidence: the grid values are probes, while the formula source is the real 1209 Fermi-domain bound.",
        "",
        "The bracket is encouraging only as scaling intuition: for many diagnostic finite-domain/curvature bundles the required `C_Ploc*G_res` budget is large. But the branch remains blocked because `L_D`, curvature norms, `C_Fermi`, `C_Ploc`, `G_res`, domain motion, projector stress, and `Delta_K` component norms are not source-backed.",
        "",
        "The `Kmetric^{00}` fallback is also staged. 1289 already supplies the symbolic chain-kernel template, so if Fermi numeric sourcing stalls the next tensor-side move is to fill `C_sign`, `M_m^{00}`, `M_L^{00}`, `K_conn^{00}`, `K_domain^{00}`, or `K_boundary^{00}`.",
        "",
        "## Fermi Bracket Assumptions",
        markdown_table(sections["assumptions"], ["assumption_id", "assumption", "effect", "anchor_found"]),
        "",
        "## Fermi Ccomm Bracket Smoke",
        markdown_table(sections["bracket"], ["scenario_id", "domain_radius_LD_m", "curvature_bundle_m_minus_2", "C_Fermi_eff", "Ccomm_parallel_m_minus_1", "required_CPloc_times_Gres_max_if_guards_zero"]),
        "",
        "## Required Inputs To Score",
        markdown_table(sections["requirements"], ["requirement_id", "quantity", "units", "status", "anchor_found"]),
        "",
        "## Kmetric00 Kernel Fallback",
        markdown_table(sections["kmetric"], ["fallback_id", "quantity", "finding", "status", "missing_before_claim"]),
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
        "assumptions": build_assumption_rows(),
        "bracket": build_bracket_rows(),
        "requirements": build_requirement_rows(),
        "kmetric": build_kmetric_rows(),
    }
    sections["gates"] = build_gate_rows()
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
