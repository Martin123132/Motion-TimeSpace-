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
DOC = WORK / "2813-Y5-R2FR-first-finite-Ccomm-or-CPloc-source-row-or-Khat00-corpus-hunt-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2813_SOURCE_REGISTER.csv",
    "operator_hunt": MTS / "P8_Y5_R2FR_2813_OPERATOR_SOURCE_HUNT.csv",
    "first_row": MTS / "P8_Y5_R2FR_2813_FIRST_CCOMM_ANALYTIC_SOURCE_ROW.csv",
    "khat_hunt": MTS / "P8_Y5_R2FR_2813_KHAT00_CORPUS_HUNT.csv",
    "qbound": MTS / "P8_Y5_R2FR_2813_QDELTAK_BOUND_WITH_FERMI_CCOMM.csv",
    "gates": MTS / "P8_Y5_R2FR_2813_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2813_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2813_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2813_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2813_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "operator_hunt_queue": RAB_QUEUE / "JR2813_OPERATOR_SOURCE_HUNT_NONCLAIM.csv",
    "first_row_queue": RAB_QUEUE / "JR2813_FIRST_CCOMM_ANALYTIC_SOURCE_ROW_NONCLAIM.csv",
    "khat_hunt_queue": RAB_QUEUE / "JR2813_KHAT00_CORPUS_HUNT_NONCLAIM.csv",
    "qbound_beta_doc": BETA_DOCS / "FERMI_CCOMM_QDELTAK_BOUND_2813_NONCLAIM.csv",
    "local_bound_copy": LOCAL_BOUNDS / "Ccomm_Fermi_analytic_source_row_2813_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_Ccomm_Fermi_row_2813_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2813_NUMERIC_FERMI_BRACKET_OR_KMETRIC_KERNEL_NEXT.csv",
}

SRC_2812_NEXT = MTS / "P8_Y5_R2FR_2812_NEXT_TARGET.csv"
SRC_2812_BOUNDS = MTS / "P8_Y5_R2FR_2812_CPLOC_CCOMM_SOURCE_READY_BOUND_ROWS.csv"
SRC_1208_DOC = WORK / "1208-Y5-R10-Ploc-parallel-projector-or-nablaPloc-bound.md"
SRC_1209_DOC = WORK / "1209-Y5-R10-local-Fermi-domain-curvature-source-pack-or-domain-motion-lock.md"
SRC_1209_FERMI = MTS / "P8_Y5_R10_1209_FERMI_DOMAIN_DERIVATION.csv"
SRC_1209_DOMAIN = MTS / "P8_Y5_R10_1209_DOMAIN_MOTION_PROJECTOR_STRESS_AUDIT.csv"
SRC_1209_UNIFIED = MTS / "P8_Y5_R10_1209_UNIFIED_SOURCE_PACK.csv"
SRC_1287_DOC = WORK / "1287-Y5-R10-RAB-Khat-tracefree-longitudinal-first-component-or-Kmetric-variation.md"
SRC_1289_DOC = WORK / "1289-Y5-R10-RAB-KL00-response-matrix-source-or-Kmetric-derivative-expansion.md"
SRC_1287_KHAT = MTS / "P8_Y5_R10_1287_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv"
SRC_1289_DELTAK = MTS / "P8_Y5_R10_1289_DELTAK00_COMPARISON_TEMPLATE.csv"
SRC_1289_DERIV = MTS / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv"


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
        ("2812_next", SRC_2812_NEXT, "authoritative 2813 target"),
        ("2812_operator_rows", SRC_2812_BOUNDS, "C_Ploc/C_comm source-ready predecessor"),
        ("1208_doc", SRC_1208_DOC, "nabla P_loc reduced to lower geometry rows"),
        ("1209_doc", SRC_1209_DOC, "finite Fermi-domain projector bound checkpoint"),
        ("1209_fermi_derivation", SRC_1209_FERMI, "Fermi C_comm_parallel analytic bound source"),
        ("1209_domain_audit", SRC_1209_DOMAIN, "domain-motion and projector-stress guard rows"),
        ("1209_unified_pack", SRC_1209_UNIFIED, "missing constants and units for Fermi row"),
        ("1287_doc", SRC_1287_DOC, "formal K_L^{00} component checkpoint"),
        ("1289_doc", SRC_1289_DOC, "DeltaK00 comparison template checkpoint"),
        ("1287_khat_component", SRC_1287_KHAT, "formal Khat00 candidate row"),
        ("1289_deltak_template", SRC_1289_DELTAK, "DeltaK00 template and blockers"),
        ("1289_derivative_kernel", SRC_1289_DERIV, "first Kmetric derivative kernel row"),
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


def build_operator_hunt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OPH2813_0_Ccomm_parallel",
            "C_comm_parallel",
            "analytic finite-domain Fermi curvature row found",
            SRC_1209_FERMI,
            "FDL1209_3_clean_freefall_fermi_bound",
            "||nabla P_loc||_Linf(D_L) <= C_Fermi*L_D*||Riemann||_Linf(D_L)+C_Fermi2*L_D^2*||nabla Riemann||_Linf(D_L)",
            "ANALYTIC_SOURCE_ROW_FOUND_NONNUMERIC",
            "needs L_D, Riemann_norm, nabla_Riemann_norm, C_Fermi, C_Fermi2, remainder/domain guards",
        ),
        (
            "OPH2813_1_Ccomm_domain",
            "C_comm_domain",
            "domain-motion bound form found, values missing",
            SRC_1209_DOMAIN,
            "DMP1209_1_non_geodesic_lab_bound",
            "domain_motion_Linf <= C_D*(acceleration_norm+rotation_norm+L_D*Riemann_norm+L_D^2*nabla_Riemann_norm)",
            "BOUND_FORM_FOUND_VALUES_MISSING",
            "needs domain/support map, acceleration/rotation branch, C_D and units",
        ),
        (
            "OPH2813_2_Ccomm_boundary",
            "C_comm_boundary",
            "boundary/projector-stress row remains conditional",
            SRC_1209_DOMAIN,
            "DMP1209_2_projector_stress_zero_branch",
            "projector_stress_Linf=0 only if P_loc/readout/support weights are not independently varied",
            "ZERO_BRANCH_UNSIGNED_VALUES_MISSING",
            "needs boundary/support/readout lock or finite leakage bound",
        ),
        (
            "OPH2813_3_CPloc",
            "C_Ploc",
            "no numeric source row found in current target inputs",
            SRC_2812_BOUNDS,
            "CB2812_0_CPloc",
            "C_Ploc=||P_loc||_phys",
            "NO_NUMERIC_SOURCE_OR_ORTHOGONAL_ZERO_THEOREM",
            "needs orthogonal projector proof or explicit operator norm in physical residual norm",
        ),
        (
            "OPH2813_4_verdict",
            "operator source hunt verdict",
            "first usable row is analytic/source-backed C_comm_parallel, not numeric",
            SRC_1209_DOC,
            "DEC1209_1_best_route",
            "source or bracket G_res_norm and C_P alongside conservative local curvature/domain scale",
            "FIRST_ANALYTIC_ROW_SELECTED_NONCLAIM",
            "next must supply numerical/source-backed Fermi constants or explicit Khat00 kernel pieces",
        ),
    ]
    return [
        {
            "hunt_id": row[0],
            "target_quantity": row[1],
            "finding": row[2],
            "source_path": sp(row[3]),
            "source_anchor": row[4],
            "formula_or_statement": row[5],
            "status": row[6],
            "missing_before_claim": row[7],
            "anchor_found": anchor_found(row[3], row[4]),
            "numeric_value": "MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_first_row_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FSR2813_0_Ccomm_parallel_Fermi",
            "C_comm_parallel",
            "||nabla P_loc||_Linf(D_L)",
            "C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm",
            "m^-1",
            SRC_1209_FERMI,
            "FDL1209_3_clean_freefall_fermi_bound",
            "ANALYTIC_SOURCE_BACKED_FORMULA_NONNUMERIC",
        ),
        (
            "FSR2813_1_LD",
            "L_D",
            "finite Fermi domain radius/diameter",
            "MISSING",
            "m",
            SRC_1209_UNIFIED,
            "USP1209_1_LD",
            "MISSING_LENGTH_SCALE",
        ),
        (
            "FSR2813_2_Riemann",
            "Riemann_norm",
            "supremum norm of local curvature over D_L",
            "MISSING",
            "m^-2",
            SRC_1209_UNIFIED,
            "USP1209_2_Riemann",
            "MISSING_CURVATURE_PROFILE",
        ),
        (
            "FSR2813_3_CFermi",
            "C_Fermi;C_Fermi2",
            "norm constants for Fermi expansion/projector drift estimate",
            "MISSING",
            "dimensionless",
            SRC_1209_UNIFIED,
            "USP1209_4_CFermi",
            "MISSING_OPERATOR_CONSTANTS",
        ),
        (
            "FSR2813_4_guard_terms",
            "domain_motion_Linf;projector_stress_Linf",
            "additive guard terms if not theorem-zero in same domain",
            "MISSING",
            "m^-1 or norm-defined",
            SRC_1209_DOMAIN,
            "DMP1209_4_total_epsilon_status",
            "MISSING_DOMAIN_STRESS_GUARDS",
        ),
    ]
    return [
        {
            "row_id": row[0],
            "quantity": row[1],
            "definition": row[2],
            "value_or_formula": row[3],
            "units": row[4],
            "source_path": sp(row[5]),
            "source_anchor": row[6],
            "status": row[7],
            "anchor_found": anchor_found(row[5], row[6]),
            "numeric_value": "MISSING",
            "source_backed_formula": row[0] == "FSR2813_0_Ccomm_parallel_Fermi",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_khat_hunt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KH2813_0_formal_KL00",
            "K_hat^{00}_candidate",
            "formal tracefree longitudinal candidate found",
            SRC_1287_KHAT,
            "KTC1287_0_flat_Ricci_scalar_KL00",
            "K_L^{00}=2 nabla^0 nabla^0 phi - (1/2)g^{00}Box phi",
            "FORMAL_CANDIDATE_FOUND_NONCLAIM",
            "missing parent origin for phi/A_nu, Ricci/Einstein domain classifier, Green inverse and boundary conditions",
        ),
        (
            "KH2813_1_DeltaK_template",
            "Delta_K^{00}",
            "comparison template found",
            SRC_1289_DELTAK,
            "DTC1289_2_DeltaK00_template",
            "Delta_K^{00}=K_L^{00}-[Kmetric_volume^{00}+Kmetric_chain^{00}+K_conn^{00}+K_domain^{00}+K_boundary^{00}]",
            "TEMPLATE_FOUND_NOT_COMPUTABLE",
            "missing full Kmetric, current Khat match, boundary and response limits",
        ),
        (
            "KH2813_2_Kmetric_kernel",
            "Kmetric_chain^{00}",
            "first derivative kernel row found",
            SRC_1289_DERIV,
            "KDR1289_0_Gamma_m_L_chain_kernel_00",
            "Kmetric chain terms depend on metric response kernels for m and L_cg plus connection/domain/boundary pieces",
            "PARTIAL_KERNEL_FOUND_NOT_COMPUTABLE",
            "missing M_m^{00}, M_L^{00}, K_conn^{00}, K_domain^{00}, K_boundary^{00}, sign convention",
        ),
        (
            "KH2813_3_live_Khat_match",
            "current-MTS K_hat^{00}",
            "no live current-MTS Khat match found in 1287/1289/2810-2812 chain",
            SRC_1289_DELTAK,
            "DTC1289_0_KL_candidate",
            "formal K_L candidate is not yet the sourced current-MTS K_hat",
            "MISSING_CURRENT_MTS_KHAT_MATCH",
            "do not promote formal KL00 to live K_hat^{00}",
        ),
        (
            "KH2813_4_verdict",
            "Khat00 corpus hunt verdict",
            "the corpus is not empty: formal KL00 and DeltaK00 template exist, but live computation remains blocked",
            SRC_1289_DOC,
            "VAL1289_4_DeltaK_template_improved_not_computable",
            "DeltaK00 comparison template is improved but still blocked",
            "CORPUS_HUNT_POSITIVE_NONCLAIM",
            "next tensor route should fill one Kmetric kernel or current-Khat adoption clause",
        ),
    ]
    return [
        {
            "hunt_id": row[0],
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


def build_qbound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QBF2813_0_Fermi_Ccomm_insert",
            "C_comm_parallel analytic insertion",
            "C_comm_parallel <= C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm",
            "uses 1209 Fermi finite-domain row",
            "ANALYTIC_INSERTION_NONNUMERIC",
        ),
        (
            "QBF2813_1_updated_bound",
            "q_DeltaK bound",
            "||q_DeltaK|| <= C_Ploc*D_Delta + (C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm + C_comm_domain + C_comm_boundary)||Delta_K||",
            "operator constants are now partly source-anchored but still not numeric",
            "ROLLED_FORWARD_BOUND_INTERFACE",
        ),
        (
            "QBF2813_2_no_score",
            "local arena score",
            "still blocked by missing L_D/Riemann/C_Fermi/domain/boundary terms, Delta_K component norms, zeta/body measures and arena projection",
            "keeps R10/WEP/PPN/orbital/clock claims blocked",
            "NOT_SCORE_READY",
        ),
    ]
    return [
        {
            "bound_id": row[0],
            "item": row[1],
            "formula": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2813_0_operator_hunt", "operator source hunt was performed", True, "C_comm/C_Ploc target rows inspected"),
        ("CG2813_1_first_analytic_Ccomm", "first source-backed analytic C_comm row exists", True, "Fermi curvature bound row from 1209 is anchored"),
        ("CG2813_2_numeric_Ccomm", "C_comm has numeric score-ready value", False, "L_D, curvature, C_Fermi and guard terms remain missing"),
        ("CG2813_3_CPloc_numeric", "C_Ploc has numeric/source-backed norm value", False, "orthogonal theorem or explicit norm source remains missing"),
        ("CG2813_4_Khat00_hunt", "Khat00 corpus hunt found formal candidate/template", True, "1287/1289 KL00 and DeltaK00 rows are anchored"),
        ("CG2813_5_live_Khat00", "live current-MTS K_hat^{00} is sourced", False, "formal K_L^{00} is not yet current-MTS K_hat^{00}"),
        ("CG2813_6_local_score", "local arena score can run", False, "operator row is analytic nonnumeric and DeltaK components remain incomplete"),
        ("CG2813_7_local_claim", "local-GR/WEP/PPN/orbital claim can be made", False, "no numeric/theorem-zero pass"),
        ("CG2813_8_nonclaim_pack", "2813 nonclaim source/hunt pack is ready", True, "next target is numeric Fermi bracket or Kmetric kernel fill"),
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
            "DEC2813_0_not_empty",
            "The source hunt is not empty.",
            "1209 provides a source-backed analytic finite-domain Fermi bound for C_comm_parallel.",
            "use it as the first nonnumeric operator row",
        ),
        (
            "DEC2813_1_no_numeric_claim",
            "No numeric operator claim is allowed.",
            "The row still lacks local domain size, curvature norm, Fermi constants and domain/boundary guards.",
            "run a conservative bracket/smoke map next",
        ),
        (
            "DEC2813_2_tensor_hunt_positive",
            "The Khat00 corpus hunt found a formal tensor candidate.",
            "1287/1289 provide K_L^{00} and DeltaK00 templates, but not live current-MTS K_hat^{00}.",
            "fill one Kmetric kernel or current-Khat adoption clause after operator bracket",
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
            "next_id": "NEXT2813_0_2814",
            "next_target": "2814-Y5-R2FR-Fermi-Ccomm-bracket-smoke-or-first-Kmetric00-kernel-fill-under-AX1090.md",
            "script": "scripts/Y5_R2FR_Fermi_Ccomm_bracket_smoke_or_first_Kmetric00_kernel_fill_under_AX1090_2814.py",
            "objective": "use the 2813 C_comm_parallel analytic row to run a conservative nonclaim bracket over L_D, Riemann_norm, C_Fermi and G_res/C_P, or fill one Kmetric^{00} kernel input if bracket inputs are absent",
            "include": "Fermi domain radius; curvature norms; C_Fermi/C_Fermi2 ranges; C_Ploc; G_res_norm; domain/boundary guard terms; Kmetric_chain/K_conn/K_domain/K_boundary candidates",
            "exclude": "optimistic hand-picked values as evidence; numeric local-GR/WEP/PPN claim; promoting KL00 to live Khat00; measured-G absorption; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["operator_hunt"], BRANCH_OUTPUTS["operator_hunt_queue"], "operator_hunt_queue"),
        (OUTPUTS["first_row"], BRANCH_OUTPUTS["first_row_queue"], "first_row_queue"),
        (OUTPUTS["khat_hunt"], BRANCH_OUTPUTS["khat_hunt_queue"], "khat_hunt_queue"),
        (OUTPUTS["qbound"], BRANCH_OUTPUTS["qbound_beta_doc"], "qbound_beta_doc"),
        (OUTPUTS["first_row"], BRANCH_OUTPUTS["local_bound_copy"], "local_bound_copy"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2813_{label}",
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


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2813_0_sources_exist", all(row["exists_or_reachable"] for row in sections["sources"]), "all source-register local paths exist"),
        ("VAL2813_1_sources_nonempty", all(row["contains_text"] for row in sections["sources"]), "all source-register entries contain text/source evidence"),
        ("VAL2813_2_operator_anchors_found", all(row["anchor_found"] for row in sections["operator_hunt"]), "all operator-hunt anchors were found"),
        ("VAL2813_3_first_Ccomm_row_present", any(row["row_id"] == "FSR2813_0_Ccomm_parallel_Fermi" and row["source_backed_formula"] for row in sections["first_row"]), "first analytic C_comm row is staged"),
        ("VAL2813_4_no_numeric_fabrication", all(row.get("numeric_value", "MISSING") == "MISSING" for row in sections["operator_hunt"] + sections["first_row"]), "no numeric operator value is fabricated"),
        ("VAL2813_5_khat_anchors_found", all(row["anchor_found"] for row in sections["khat_hunt"]), "Khat00 hunt anchors were found"),
        ("VAL2813_6_live_Khat_not_promoted", any(row["hunt_id"] == "KH2813_3_live_Khat_match" and row["status"] == "MISSING_CURRENT_MTS_KHAT_MATCH" for row in sections["khat_hunt"]), "formal KL00 is not promoted to live Khat00"),
        ("VAL2813_7_qbound_rollforward_present", any(row["bound_id"] == "QBF2813_1_updated_bound" for row in sections["qbound"]), "q_DeltaK Fermi C_comm bound is rolled forward"),
        ("VAL2813_8_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2813_9_next_target_2814", any(row["next_id"] == "NEXT2813_0_2814" for row in sections["next"]), "next target is 2814"),
        ("VAL2813_10_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2813_11_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2813_12_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2813_13_cited_paths_exist", cited_paths_exist(sections), "all cited local file/copy paths in generated rows exist"),
        ("VAL2813_14_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2813_15_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2813_16_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2813_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2813_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2813 stages a source-backed analytic C_comm_parallel Fermi row, records missing numeric inputs, and performs a positive nonclaim Khat00 corpus hunt.",
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
        "# 2813 - Y5 R2FR First Finite Ccomm Or CPloc Source Row Or Khat00 Corpus Hunt Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2813 is a useful positive nonclaim checkpoint. The operator source hunt is not empty: `C_comm_parallel` has an analytic, source-backed Fermi-domain row from 1209.",
        "",
        "It is not numeric and not claim-ready. The row still needs `L_D`, local curvature norms, `C_Fermi/C_Fermi2`, domain-motion and projector-stress guards, plus the shared `C_Ploc/G_res` scoring factors before any local arena can run honestly.",
        "",
        "The targeted `K_hat^{00}` hunt also found real structure: the formal `K_L^{00}` candidate and `Delta_K^{00}` template exist in 1287/1289. But they are not the live current-MTS `K_hat^{00}` and do not compute `Delta_K^{00}` yet.",
        "",
        "## Operator Source Hunt",
        markdown_table(sections["operator_hunt"], ["hunt_id", "target_quantity", "finding", "status", "missing_before_claim"]),
        "",
        "## First C_comm Analytic Source Row",
        markdown_table(sections["first_row"], ["row_id", "quantity", "value_or_formula", "units", "status", "source_anchor"]),
        "",
        "## Khat00 Corpus Hunt",
        markdown_table(sections["khat_hunt"], ["hunt_id", "quantity", "finding", "status", "missing_before_claim"]),
        "",
        "## q_DeltaK Bound With Fermi C_comm",
        markdown_table(sections["qbound"], ["bound_id", "item", "formula", "status"]),
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
        "operator_hunt": build_operator_hunt_rows(),
        "first_row": build_first_row_rows(),
        "khat_hunt": build_khat_hunt_rows(),
        "qbound": build_qbound_rows(),
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
