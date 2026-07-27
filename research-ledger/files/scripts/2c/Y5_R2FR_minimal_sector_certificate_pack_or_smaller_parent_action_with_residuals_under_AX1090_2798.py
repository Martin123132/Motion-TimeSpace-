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
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
DOC = WORK / "2798-Y5-R2FR-minimal-sector-certificate-pack-or-smaller-parent-action-with-residuals-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2798_SOURCE_REGISTER.csv",
    "sector_pack": MTS / "P8_Y5_R2FR_2798_MINIMAL_SECTOR_CERTIFICATE_PACK.csv",
    "runner": MTS / "P8_Y5_R2FR_2798_SECTOR_CERTIFICATE_RUNNER.csv",
    "smaller_action": MTS / "P8_Y5_R2FR_2798_SMALLER_PARENT_ACTION_OR_RESIDUAL_ROUTE.csv",
    "residual_map": MTS / "P8_Y5_R2FR_2798_UNCERTIFIED_SECTOR_RESIDUAL_MAP.csv",
    "priority": MTS / "P8_Y5_R2FR_2798_NEXT_SECTOR_PRIORITY_LEDGER.csv",
    "product_candidate": MTS / "P8_Y5_R2FR_2798_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "product_runner": MTS / "P8_Y5_R2FR_2798_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2798_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2798_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2798_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2798_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2798_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2798_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "sector_pack_queue": RAB_QUEUE / "JR2798_MINIMAL_SECTOR_CERTIFICATE_PACK_NONCLAIM.csv",
    "residual_queue": RAB_QUEUE / "JR2798_UNCERTIFIED_SECTOR_RESIDUAL_MAP_NONCLAIM.csv",
    "priority_queue": RAB_QUEUE / "JR2798_NEXT_SECTOR_PRIORITY_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "SECTOR_CERTIFICATE_PACK_2798_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_sector_certificate_pack_2798_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2798_GAMMA_KHAT_QLOC_ACTION_EXISTENCE_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


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


def source_entries() -> list[tuple[str, Path, str]]:
    raw = [
        ("2797_next", MTS / "P8_Y5_R2FR_2797_NEXT_TARGET.csv", "authoritative 2798 target"),
        ("2797_derivation", MTS / "P8_Y5_R2FR_2797_PARENT_OBJECT_DOMAIN_DERIVATION_ATTEMPT.csv", "parent-object circularity verdict"),
        ("2797_budget", MTS / "P8_Y5_R2FR_2797_EXPLICIT_CLOSURE_BUDGET_REGISTER.csv", "AX2796_0 closure budget"),
        ("2710_falsifier", MTS / "P8_Y5_R2FR_2710_IRREDUCIBLE_FALSIFIER_GATE.csv", "sector certificate falsifier"),
        ("2710_normal_form", MTS / "P8_Y5_R2FR_2710_PARENT_OBJECT_NORMAL_FORM.csv", "parent normal form"),
        ("1009_parent_sector_contract", MTS / "P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv", "sector contract anatomy"),
        ("1009_variation_candidates", MTS / "P8_Y5_R10_1009_SECTOR_VARIATION_CANDIDATES.csv", "sector variation candidates"),
        ("1009_runner", MTS / "P8_Y5_R10_1009_SECTOR_VARIATION_RUNNER.csv", "runner refusal reasons"),
        ("1009_decision", MTS / "P8_Y5_R10_1009_DECISION_LEDGER.csv", "hardest-sector decision precedent"),
        ("1009_doc", WORK / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md", "readable sector-contract checkpoint"),
    ]
    return raw


def build_sources() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": role,
            "contains_text": bool(read_text(path).strip()) if path.exists() else False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for source_id, path, role in source_entries()
    ]


def build_sector_pack_rows() -> list[dict[str, Any]]:
    rows = [
        ("SEC2798_0_EH_core", "EH core anchor", "g_obs/coframe,tau", "KNOWN_GR_TEMPLATE", "KNOWN_GR_TEMPLATE", "KNOWN_GR_TEMPLATE", "BOUNDARY_REFERENCE_NOT_PARENT_FIXED", "EH_ANCHOR_ONLY_NOT_TOTAL_PARENT", "INCOMPLETE_PARENT_CERTIFICATE"),
        ("SEC2798_1_universal_matter", "ordinary matter", "psi_A,g_obs/coframe", "CONDITIONAL_HILBERT_VARIATION", "STANDARD_IF_COFAME_OWNED", "MISSING_SOURCE_WARD_AND_NO_SPECIES_WEIGHT", "MISSING_NO_MARKER_BOUNDARY_DOMAIN", "MOMS_DEPENDENT_NOT_PARENT_OWNED", "INCOMPLETE_PARENT_CERTIFICATE"),
        ("SEC2798_2_boundary_reference", "boundary/reference", "boundary metric,normal,B_ref,counterterm class", "MISSING_FIXED_REFERENCE_VARIATION", "MISSING_REFERENCE_STRESS_POLICY", "MISSING_FIXED_BEFORE_READOUT_TAU", "MISSING_ZERO_FIXED_BOUNDARY_FLUX", "UNFIXED_REFERENCE_RESIDUAL", "INCOMPLETE_PARENT_CERTIFICATE"),
        ("SEC2798_3_Gamma_Khat_q_loc", "Gamma/Khat/q_loc residual", "Phi^A,Gamma_eff,K_hat,q_loc,g", "MISSING_HELMHOLTZ_COMPATIBLE_ACTION", "MISSING_T_GK", "MISSING_THETA_Q_TAU", "MISSING_BOUNDARY_NO_FLUX", "RETAIN_QLOC_RESIDUAL_UNTIL_ACTION_EXISTS", "HARDEST_BLOCKER"),
        ("SEC2798_4_domain_projector", "domain/projector selector", "u,h,X,Qcoh,chi_D,lambda_D", "PARTIAL_CLAUSE_ONLY", "MISSING_SELECTOR_STRESS", "MISSING_PROJECTOR_Q_TAU", "MISSING_BOUNDARY_DOMAIN_CLOSURE", "RETAIN_DOMAIN_RESIDUAL", "INCOMPLETE_PARENT_CERTIFICATE"),
        ("SEC2798_5_mass_projector_PiM", "Pi_M/source-measure projector", "Pi_M,J_H,homology,boundary symplectic metric", "MISSING_PARENT_ORIGIN_AND_PRODUCT_VARIATION", "MISSING_PROJECTOR_STRESS", "MISSING_Q_M_SOURCE_EQUALITY", "MISSING_EXTERIOR_CLOSURE", "RETAIN_SOURCE_MEASURE_RESIDUAL", "PARALLEL_BLOCKER"),
        ("SEC2798_6_memory_response", "response doublet/memory sector", "R_plus,R_minus,memory variables", "MISSING_FULL_DOUBLET_VARIATION", "MISSING_MEMORY_STRESS", "MISSING_PPN_LOCK", "MISSING_ZERO_ODD_SOURCE_BOUNDARY", "RETAIN_MEMORY_RESIDUAL", "INCOMPLETE_PARENT_CERTIFICATE"),
        ("SEC2798_7_worldtube_source_glue", "worldtube/source matching", "worldtube W, exterior annulus, Q_M[tau], source measure", "CONDITIONAL_GLUE_ONLY", "MISSING_WORLDTUBE_STRESS", "Q_M_CONDITIONAL_NOT_OWNED", "MISSING_EXTERIOR_ANNULUS_CLOSURE", "RETAIN_SOURCE_GLUE_RESIDUAL", "CORE_MASS_BLOCKER"),
        ("SEC2798_8_total_parent", "total parent action", "all retained sectors", "SUM_OF_UNCERTIFIED_SECTORS", "MISSING_TOTAL_STRESS", "MISSING_THETA_Q_MTS", "MISSING_TOTAL_BOUNDARY_POLICY", "TOTAL_PARENT_SWITCH_REJECTED", "NOT_PROMOTED"),
    ]
    return [
        {
            "sector_id": row[0],
            "sector": row[1],
            "field_list": row[2],
            "first_variation_status": row[3],
            "stress_status": row[4],
            "tau_source_status": row[5],
            "boundary_status": row[6],
            "residual_policy": row[7],
            "certificate_status": row[8],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_runner_rows(sector_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in sector_rows:
        status = row["certificate_status"]
        complete = status == "COMPLETE_PARENT_CERTIFICATE"
        rows.append(
            {
                "runner_id": f"SCR2798_{row['sector_id'].split('_')[-1]}",
                "sector_id": row["sector_id"],
                "certificate_complete": complete,
                "claim_allowed": False,
                "verdict": "REFUSED_INCOMPLETE_PARENT_SECTOR_CERTIFICATE" if not complete else "CERTIFICATE_REVIEW_REQUIRED",
                "primary_blocker": status,
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def build_smaller_action_rows() -> list[dict[str, Any]]:
    rows = [
        ("SPA2798_0_GR_anchor", "S_EH[g_obs]+S_matter[psi,g_obs]+standard boundary", "comparison_anchor_only", "use as GR baseline language and weak-field template", "MTS parent action or derived local-GR reduction", "observed coframe/matter/source ownership missing"),
        ("SPA2798_1_minimal_owned_MTS_core", "S_parent_min = unresolved", "NOT_PROMOTED", "none as claim", "declaring a smaller MTS parent action without sector certificates", "no non-EH sector has complete certificate"),
        ("SPA2798_2_residualized_branch", "EH/matter template plus explicit residual map for every uncertified MTS sector", "NONCLAIM_PRIVATE_SCAFFOLD", "organize tests and residual bounds", "theorem-zero, local-GR, or WEP pass", "source or derive residuals one by one"),
        ("SPA2798_3_verdict", "smaller parent action sufficient for local branch", "SMALLER_PARENT_ACTION_NOT_PROMOTED", "private bookkeeping only", "public or internal claim of derived parent action", "complete sector certificates or reduce to a genuinely owned primitive action"),
    ]
    return [
        {
            "route_id": row[0],
            "candidate_action": row[1],
            "status": row[2],
            "allowed_use": row[3],
            "forbidden_use": row[4],
            "gap": row[5],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_residual_map_rows() -> list[dict[str, Any]]:
    rows = [
        ("RES2798_0_GK_q_loc", "Gamma/Khat/q_loc", "q_loc residual vector; T_GK; Helmholtz obstruction", "R10;WEP;PPN;local_GR", "derive S_GK or retain q_loc residual bound"),
        ("RES2798_1_PiM_source", "Pi_M/source-measure", "M_H_ref/source equality residual", "Newton;PPN;orbital;WEP", "derive projector origin and source-charge equality"),
        ("RES2798_2_boundary_reference", "boundary/reference", "Delta_ref/M_H_ref residual", "R10;PPN;local_GR", "fixed reference and boundary flux certificates"),
        ("RES2798_3_domain_selector", "domain/projector selector", "domain stress/support residual", "WEP;clock;R10", "domain Euler and boundary no-flux certificate"),
        ("RES2798_4_memory_response", "memory/response doublet", "PPN/local residual and cosmology activation cross-check", "PPN;cosmology;local_GR", "full doublet variation and PPN lock"),
        ("RES2798_5_worldtube_glue", "worldtube/source glue", "source mass/readout residual", "Newton;orbital;WEP", "worldtube Noether identity and exterior closure"),
    ]
    return [
        {
            "residual_id": row[0],
            "uncertified_sector": row[1],
            "residual_object": row[2],
            "test_arenas": row[3],
            "next_requirement": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_priority_rows() -> list[dict[str, Any]]:
    rows = [
        ("PRI2798_0_GK_q_loc", "Gamma/Khat/q_loc action-existence", "highest", "local GR/PPN fails if this is bookkeeping stress rather than variational stress with double-zero", "Helmholtz/action-existence test for S_GK or retain q_loc residual"),
        ("PRI2798_1_PiM_source", "Pi_M/source-measure", "parallel", "even a good local residual zero does not identify conserved parent charge with measured GM", "derive projector/source equality or keep source residual"),
        ("PRI2798_2_boundary_reference", "boundary/reference", "high", "reference subtraction can fake local mass/residual silence", "fixed reference and boundary-flux certificates"),
        ("PRI2798_3_matter_MOMS", "ordinary matter/MOMS", "blocked_by_parent_object", "conditional theorem exists but needs parent object/action measure/no-marker", "return after sector owner or finite DD source rows"),
    ]
    return [
        {
            "priority_id": row[0],
            "target": row[1],
            "priority": row[2],
            "why": row[3],
            "next_action": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_product_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "prediction_id": "WEP2798_0_no_claim_product",
            "observable": "eta_AB(lambda)",
            "prediction_status": "NO_NUMERIC_PREDICTION",
            "claim_blocker": "no sector certificate pack completes and smaller parent action is not promoted",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_product_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN2798_0_refuse_sector_gap",
            "valid_prediction_rows": 0,
            "claim_allowed": False,
            "expected_result": "RUNNER_REFUSES_WEP_CLAIM",
            "reason": "sector certificates incomplete and residual route nonclaim",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_comparison_rows() -> list[dict[str, Any]]:
    return [
        {
            "comparison_id": "CMP2798_0_no_numeric_eta",
            "baseline": "WEP/local-GR compatibility",
            "prediction": "MTS R2FR residualized branch",
            "comparison_status": "NOT_RUN_NUMERICALLY",
            "reason": "no score-ready source-backed residual/product row exists",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2798_0_sector_pack", "minimal sector certificate pack complete", False, False, "SEC2798_8_total_parent=NOT_PROMOTED"),
        ("CG2798_1_smaller_parent", "smaller parent action promoted", False, False, "SPA2798_3_verdict=SMALLER_PARENT_ACTION_NOT_PROMOTED"),
        ("CG2798_2_GK_action", "Gamma/Khat/q_loc action-owned", False, False, "SEC2798_3_Gamma_Khat_q_loc=HARDEST_BLOCKER"),
        ("CG2798_3_residual_route", "residual route score-ready", False, False, "residual rows have objects but no source-backed bounds"),
        ("CG2798_4_product_runner", "WEP product runner", True, False, "runner refuses claim safely"),
    ]
    return [
        {
            "gate_id": row[0],
            "claim_component": row[1],
            "gate_pass": row[2],
            "claim_allowed": row[3],
            "reason": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2798_0_pack_verdict", "minimal sector certificate pack does not close", "every non-EH sector lacks at least one required certificate", "do not promote S_parent by sector sum"),
        ("DEC2798_1_smaller_action", "smaller parent action is not promoted", "EH/matter can anchor a GR template but not the MTS parent action", "residualize uncertified sectors"),
        ("DEC2798_2_first_domino", "Gamma/Khat/q_loc is the first sector to attack", "it is the hardest local-GR/PPN blocker and decides whether q_loc is variational stress or residual bookkeeping", "run action-existence/Helmholtz test"),
        ("DEC2798_3_parallel_debt", "Pi_M/source-measure remains parallel", "source mass equality is still needed even if local residuals are cleaned", "keep source-measure gates blocked"),
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
            "next_id": "NEXT2798_0_2799",
            "next_target": "2799-Y5-R2FR-Gamma-Khat-q_loc-action-existence-Helmholtz-or-residual-retention-under-AX1090.md",
            "script": "scripts/Y5_R2FR_Gamma_Khat_q_loc_action_existence_Helmholtz_or_residual_retention_under_AX1090_2799.py",
            "objective": "test whether Gamma_eff/K_hat/q_loc can come from a variational local action with Helmholtz integrability, Euler closure, double-zero, and boundary no-flux; otherwise retain q_loc as an explicit residual vector with source-bound requirements",
            "include": "candidate S_GK[g,Phi]; Helmholtz symmetry; Euler equations; T_GK; double-zero local residual; P_loc ownership; boundary/symplectic no-flux; residual source rows",
            "exclude": "bookkeeping stress; plateau axiom; EH-only import; fitted cancellation; H_tau pass; M_H_ref pass; local-GR/WEP claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["sector_pack"], BRANCH_OUTPUTS["sector_pack_queue"], "sector_pack_queue"),
        (OUTPUTS["residual_map"], BRANCH_OUTPUTS["residual_queue"], "residual_queue"),
        (OUTPUTS["priority"], BRANCH_OUTPUTS["priority_queue"], "priority_queue"),
        (OUTPUTS["sector_pack"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append({"copy_id": f"BC2798_{label}", "source": str(source), "destination": str(destination), "exists": destination.exists(), "valid_for_claim": False, "generated_utc": utc_now()})
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


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2798_0_sources_exist", all(row["exists"] for row in sections["sources"]), "all cited local source paths exist"),
        ("VAL2798_1_sector_pack_complete_shape", {row["sector_id"] for row in sections["sector_pack"]} >= {f"SEC2798_{index}_{name}" for index, name in [(0, "EH_core"), (1, "universal_matter"), (2, "boundary_reference"), (3, "Gamma_Khat_q_loc"), (4, "domain_projector"), (5, "mass_projector_PiM"), (6, "memory_response"), (7, "worldtube_source_glue"), (8, "total_parent")]}, "sector pack includes all required sectors"),
        ("VAL2798_2_no_complete_certificates", not any(row["certificate_complete"] == True for row in sections["runner"]), "no sector certificate is complete"),
        ("VAL2798_3_hardest_blocker_GK", any(row["sector_id"] == "SEC2798_3_Gamma_Khat_q_loc" and row["certificate_status"] == "HARDEST_BLOCKER" for row in sections["sector_pack"]), "Gamma/Khat/q_loc is identified as hardest blocker"),
        ("VAL2798_4_smaller_action_not_promoted", any(row["route_id"] == "SPA2798_3_verdict" and row["status"] == "SMALLER_PARENT_ACTION_NOT_PROMOTED" for row in sections["smaller_action"]), "smaller parent action is not promoted"),
        ("VAL2798_5_residual_map_written", len(sections["residual_map"]) >= 6, "uncertified sector residual map is written"),
        ("VAL2798_6_priority_GK_first", any(row["priority_id"] == "PRI2798_0_GK_q_loc" and row["priority"] == "highest" for row in sections["priority"]), "next priority is Gamma/Khat/q_loc"),
        ("VAL2798_7_product_runner_refuses", any(row["expected_result"] == "RUNNER_REFUSES_WEP_CLAIM" and str(row["claim_allowed"]).lower() == "false" for row in sections["product_runner"]), "product runner refuses claim"),
        ("VAL2798_8_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2798_9_next_target_2799", any(row["next_id"] == "NEXT2798_0_2799" for row in sections["next"]), "next target is 2799"),
        ("VAL2798_10_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2798_11_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2798_12_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2798_13_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2798_14_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2798_15_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2798_16_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append({"validation_id": "VAL2798_OVERALL", "passed": all(row["passed"] for row in rows), "detail": "2798 builds the minimal sector certificate pack, refuses promotion of S_parent by uncertified sector sum, residualizes uncertified sectors, and selects Gamma/Khat/q_loc action-existence as the next highest-leverage blocker.", "generated_utc": utc_now()})
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2798 — Y5 R2FR Minimal Sector Certificate Pack Or Smaller Parent Action With Residuals Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2798 asks whether the parent action can be promoted by certifying its sectors. The answer is no: the EH block is a useful GR anchor, but every MTS/non-EH sector is missing at least one certificate required for a parent action: field ownership, first variation, stress, boundary, tau/source charge, or residual policy.",
        "",
        "Therefore a smaller parent action is **not** promoted. The safe branch is residualized: every uncertified sector stays explicit and nonclaim. The highest-leverage next target is Gamma/Khat/q_loc action existence, because local GR/PPN fails if that sector is bookkeeping stress rather than a variational stress with a double-zero.",
        "",
        "## Minimal Sector Certificate Pack",
        markdown_table(sections["sector_pack"], ["sector_id", "sector", "first_variation_status", "stress_status", "tau_source_status", "boundary_status", "certificate_status"]),
        "",
        "## Sector Certificate Runner",
        markdown_table(sections["runner"], ["runner_id", "sector_id", "certificate_complete", "claim_allowed", "verdict", "primary_blocker"]),
        "",
        "## Smaller Parent Action Or Residual Route",
        markdown_table(sections["smaller_action"], ["route_id", "candidate_action", "status", "allowed_use", "forbidden_use", "gap"]),
        "",
        "## Uncertified Sector Residual Map",
        markdown_table(sections["residual_map"], ["residual_id", "uncertified_sector", "residual_object", "test_arenas", "next_requirement"]),
        "",
        "## Next Sector Priority",
        markdown_table(sections["priority"], ["priority_id", "target", "priority", "why", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
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
        "sector_pack": build_sector_pack_rows(),
    }
    sections["runner"] = build_runner_rows(sections["sector_pack"])
    sections["smaller_action"] = build_smaller_action_rows()
    sections["residual_map"] = build_residual_map_rows()
    sections["priority"] = build_priority_rows()
    sections["product_candidate"] = build_product_candidate_rows()
    sections["product_runner"] = build_product_runner_rows()
    sections["comparisons"] = build_comparison_rows()
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
