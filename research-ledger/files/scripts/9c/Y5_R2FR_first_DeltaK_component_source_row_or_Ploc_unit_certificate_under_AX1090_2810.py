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
DOC = WORK / "2810-Y5-R2FR-first-DeltaK-component-source-row-or-Ploc-unit-certificate-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2810_SOURCE_REGISTER.csv",
    "ploc_unit": MTS / "P8_Y5_R2FR_2810_PLOC_UNIT_CERTIFICATE.csv",
    "deltak00": MTS / "P8_Y5_R2FR_2810_DELTAK00_SOURCE_ATTEMPT.csv",
    "qdelta_units": MTS / "P8_Y5_R2FR_2810_QDELTAK_UNIT_UPDATE.csv",
    "force_link": MTS / "P8_Y5_R2FR_2810_FORCE_DENOMINATOR_LINK.csv",
    "gates": MTS / "P8_Y5_R2FR_2810_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2810_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2810_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2810_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2810_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "ploc_queue": RAB_QUEUE / "JR2810_PLOC_UNIT_CERTIFICATE_NONCLAIM.csv",
    "deltak00_queue": RAB_QUEUE / "JR2810_DELTAK00_SOURCE_ATTEMPT_NONCLAIM.csv",
    "unit_beta_doc": BETA_DOCS / "PLOC_QDELTAK_UNIT_UPDATE_2810_NONCLAIM.csv",
    "local_bound_copy": LOCAL_BOUNDS / "Ploc_unit_certificate_2810_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_Ploc_unit_certificate_2810_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2810_PLOC_NORM_OR_DELTAK00_NEXT.csv",
}


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
        ("2809_next", MTS / "P8_Y5_R2FR_2809_NEXT_TARGET.csv", "authoritative 2810 target"),
        ("2809_delta_bound", MTS / "P8_Y5_R2FR_2809_DELTAK_COMPONENT_BOUND_TABLE.csv", "Delta_K component split predecessor"),
        ("2809_derivative", MTS / "P8_Y5_R2FR_2809_DELTAK_DERIVATIVE_BOUND_INTERFACE.csv", "q_DeltaK derivative interface predecessor"),
        ("2809_gates", MTS / "P8_Y5_R2FR_2809_CLAIM_GATES.csv", "2809 claim-gate status"),
        ("2808_units", MTS / "P8_Y5_R2FR_2808_WARD_RESIDUAL_UNIT_CONTRACT.csv", "q_loc/P_loc unit predecessor"),
        ("2808_metric_response", MTS / "P8_Y5_R2FR_2808_METRIC_RESPONSE_DERIVATION_ATTEMPT.csv", "metric-response identity predecessor"),
        ("2807_force_seed", MTS / "P8_Y5_R2FR_2807_SOURCE_BACKED_FORCE_SEED_ROW.csv", "source-backed g_n denominator seed"),
        ("field_sort_2485", LOCAL_BOUNDS / "Parent_field_sort_table_2485_NONCLAIM.csv", "P_loc as projector/readout map"),
        ("quotient_sort_2570", LOCAL_BOUNDS / "Parent_field_sort_quotient_attempt_2570_NONCLAIM.csv", "fixed-before-variation P_loc obstruction"),
        ("q_loc_law_2554", LOCAL_BOUNDS / "Qloc_local_vacuum_law_2554_NONCLAIM.csv", "conditional q_loc=P_loc J_M law"),
        ("sigma_delta_2603", LOCAL_BOUNDS / "SigmaX_tail_law_bridge_2603_NONCLAIM.csv", "Delta_K projected-divergence schema"),
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


def build_ploc_unit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PLC2810_0_domain",
            "P_loc domain/codomain",
            "P_loc^nu_rho : F^rho -> F^nu on the same local residual vector/force-density bundle",
            "same-domain endomorphism",
            "dimensionless operator if this parent typing is signed",
            "CONDITIONAL_UNIT_CERTIFICATE",
            "source-intake/local_bounds/Parent_field_sort_table_2485_NONCLAIM.csv;source-intake/local_bounds/Parent_field_sort_quotient_attempt_2570_NONCLAIM.csv",
        ),
        (
            "PLC2810_1_idempotent",
            "projector algebra",
            "P_loc^nu_sigma P_loc^sigma_rho = P_loc^nu_rho",
            "idempotence forbids physical units unless a compensating unitful inverse is inserted",
            "dimensionless at algebra level; parent signature still needed",
            "CONDITIONAL_UNIT_CERTIFICATE",
            "source-intake/local_bounds/Parent_field_sort_table_2485_NONCLAIM.csv",
        ),
        (
            "PLC2810_2_qDelta_units",
            "q_DeltaK unit propagation",
            "q_DeltaK^nu = P_loc^nu_rho nabla_mu Delta_K^{mu rho}",
            "if Delta_K has stress units and P_loc is dimensionless, q_DeltaK has stress/length = force-density units",
            "unit route sharpened but not a numeric bound",
            "DERIVED_UNIT_CHAIN_NONCLAIM",
            "source-intake/mts_residuals/P8_Y5_R2FR_2809_DELTAK_DERIVATIVE_BOUND_INTERFACE.csv",
        ),
        (
            "PLC2810_3_norm",
            "operator norm",
            "||P_loc|| = 1 only for a parent-signed orthogonal projector in a fixed positive local inner product",
            "idempotent alone does not imply norm one for non-orthogonal projectors",
            "retain C_Ploc as dimensionless unknown",
            "NORM_NOT_CERTIFIED",
            "source-intake/local_bounds/Parent_field_sort_quotient_attempt_2570_NONCLAIM.csv",
        ),
        (
            "PLC2810_4_commutator",
            "projector derivative",
            "[P_loc,nabla]Delta_K = (nabla P_loc)Delta_K plus connection/domain terms",
            "zero only if P_loc is covariantly fixed/parallel on the local collar",
            "retain projector commutator residual",
            "COMMUTATOR_NOT_ZEROED",
            "source-intake/mts_residuals/P8_Y5_R2FR_2809_DELTAK_DERIVATIVE_BOUND_INTERFACE.csv;source-intake/local_bounds/Readout_reentry_audit_2523_NONCLAIM.csv",
        ),
        (
            "PLC2810_5_verdict",
            "P_loc certificate verdict",
            "P_loc can be treated as dimensionless only as a typed same-domain local projector; its norm and commutator remain unsigned",
            "one useful unit obstruction is reduced, but no observable score is unlocked",
            "UNIT_ONLY_PROGRESS_NORM_BLOCKED",
            "PARTIAL_PASS_NONCLAIM",
            "source-intake/mts_residuals/P8_Y5_R2FR_2808_WARD_RESIDUAL_UNIT_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R2FR_2809_DELTAK_COMPONENT_BOUND_TABLE.csv",
        ),
    ]
    return [
        {
            "certificate_id": row[0],
            "item": row[1],
            "statement": row[2],
            "reason": row[3],
            "result": row[4],
            "status": row[5],
            "source_paths": row[6],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_deltak00_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DK002810_0_definition",
            "Delta_K^{00}",
            "Delta_K^{00}=K_hat^{00}-K_metric^{00}",
            "definition available from 2808/2809",
            "SCHEMA_PRESENT",
            "need actual K_hat^{00} expression",
        ),
        (
            "DK002810_1_Kmetric00",
            "K_metric^{00}",
            "K_metric^{00}=Gamma_eff g^{00}-T_GK^{00}",
            "defined by metric variation of S_GK, conditional on Gamma_eff scalar/action-density convention",
            "CONDITIONAL_EXPRESSION",
            "need Gamma_eff functional and T_GK component variation",
        ),
        (
            "DK002810_2_Khat00",
            "K_hat^{00}",
            "current MTS K_hat energy component",
            "no source-backed component expression found in current 2808/2809 evidence",
            "MISSING_COMPONENT_SOURCE",
            "derive from parent action or source from corpus",
        ),
        (
            "DK002810_3_boundary00",
            "00 boundary/improvement contribution",
            "Delta_K^{00}_boundary",
            "boundary/reference convention is not fixed",
            "MISSING_BOUNDARY_CONVENTION",
            "source no-flux/reference class or keep as residual",
        ),
        (
            "DK002810_4_derivative00",
            "partial_mu Delta_K^{mu0}",
            "time/radial/angular/connection derivative terms",
            "derivative constants remain missing",
            "MISSING_DERIVATIVE_BOUND",
            "need C_t, C_r, C_ang, C_conn, and source profile scale",
        ),
        (
            "DK002810_5_verdict",
            "first concrete DeltaK00 row",
            "not available yet",
            "P_loc unit work is cleaner than inventing a DeltaK00 component",
            "FAIL_CURRENT_CLAIM",
            "next attempt should target P_loc norm/commutator or derive K_hat^{00}",
        ),
    ]
    return [
        {
            "attempt_id": row[0],
            "quantity": row[1],
            "candidate_expression": row[2],
            "evidence": row[3],
            "status": row[4],
            "next_input_needed": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_qdelta_unit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QDU2810_0_DeltaK",
            "Delta_K^{mu nu}",
            "stress",
            "from K_hat/K_metric stress-density convention",
            "CONDITIONAL_ON_GAMMA_KHAT_NORMALIZATION",
        ),
        (
            "QDU2810_1_divergence",
            "nabla_mu Delta_K^{mu nu}",
            "stress per length = force density",
            "covariant derivative adds inverse length plus connection terms",
            "CONDITIONAL_FORCE_DENSITY_UNIT",
        ),
        (
            "QDU2810_2_Ploc",
            "P_loc nabla_mu Delta_K^{mu nu}",
            "same as force density if P_loc is same-domain dimensionless",
            "2810 unit certificate supports dimensionless P_loc but not norm one",
            "PLOC_UNIT_ONLY_PARTIAL_PASS",
        ),
        (
            "QDU2810_3_commutator",
            "[P_loc,nabla]Delta_K",
            "force density if nabla P_loc has inverse-length unit",
            "must be retained unless P_loc is covariantly fixed",
            "COMMUTATOR_RETAINED",
        ),
        (
            "QDU2810_4_acceleration",
            "delta a_A",
            "m s^-2 after zeta_q/M_A integral conversion",
            "requires zeta_q=1 physical units, body measure M_A, boundary terms, and no measured-G absorption",
            "NOT_SCORE_READY",
        ),
    ]
    return [
        {
            "unit_id": row[0],
            "quantity": row[1],
            "unit_result": row[2],
            "reason": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_force_link_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FL2810_0_gn",
            "g_n",
            "9.80665",
            "m s^-2",
            "source-intake/mts_residuals/P8_Y5_R2FR_2807_SOURCE_BACKED_FORCE_SEED_ROW.csv",
            "source-backed denominator retained",
            "usable only after q_DeltaK/zeta/body measures become physical acceleration inputs",
        ),
        (
            "FL2810_1_force_density_to_accel",
            "delta a_A/g_n",
            "MISSING",
            "dimensionless",
            "source-intake/mts_residuals/P8_Y5_R2FR_2810_QDELTAK_UNIT_UPDATE.csv",
            "blocked",
            "needs zeta_q, body integral, boundary norm, and source frame",
        ),
        (
            "FL2810_2_no_measured_G_absorption",
            "normalization guard",
            "ACTIVE",
            "policy",
            "source-intake/mts_residuals/P8_Y5_R2FR_2809_NEXT_TARGET.csv",
            "guard retained",
            "DeltaK cannot be hidden by refitting measured G/GM",
        ),
    ]
    return [
        {
            "link_id": row[0],
            "quantity": row[1],
            "value": row[2],
            "units": row[3],
            "source_path": row[4],
            "status": row[5],
            "limitation": row[6],
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2810_0_Ploc_unit_attempted", "P_loc unit certificate attempted", True, "unit typing is now explicit"),
        ("CG2810_1_Ploc_dimensionless_conditional", "P_loc dimensionless if same-domain projector typing is accepted", True, "conditional unit-only result; not a physical claim"),
        ("CG2810_2_Ploc_norm_one", "||P_loc||=1 is certified", False, "orthogonality/fixed positive inner product not parent-signed"),
        ("CG2810_3_Ploc_commutator_zero", "[P_loc,nabla]=0 is certified", False, "covariantly fixed projector not signed"),
        ("CG2810_4_DeltaK00_component", "DeltaK00 component row is sourced", False, "K_hat^{00} and boundary/derivative pieces missing"),
        ("CG2810_5_force_score", "q_DeltaK can be converted to acceleration score", False, "zeta_q/body measure/boundary terms still missing"),
        ("CG2810_6_local_claim", "local-GR/WEP/PPN/orbital claim can be made", False, "unit-only progress is insufficient"),
        ("CG2810_7_nonclaim_pack", "2810 nonclaim unit certificate pack is ready", True, "next target is P_loc norm/commutator or DeltaK00 source"),
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
            "DEC2810_0_take_unit_route",
            "The safest 2810 leap is the P_loc unit certificate, not a guessed DeltaK00 number.",
            "The corpus supports P_loc as a projector/readout map, but not a sourced K_hat^{00} component.",
            "promote unit-only progress and keep DeltaK00 missing",
        ),
        (
            "DEC2810_1_progress",
            "q_DeltaK units are now sharper.",
            "If Delta_K has stress units and P_loc is a same-domain dimensionless projector, q_DeltaK is a force-density residual.",
            "use this as a future runner unit contract",
        ),
        (
            "DEC2810_2_blocker",
            "The norm and commutator are still the real problem.",
            "Idempotence alone does not prove ||P_loc||=1 and does not make [P_loc,nabla] vanish.",
            "attack P_loc orthogonality/parallel transport next",
        ),
        (
            "DEC2810_3_no_claim",
            "No local-GR or WEP claim is unlocked.",
            "Delta_K components, zeta_q, body measures, and boundary terms remain missing.",
            "keep all claim flags false",
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
            "next_id": "NEXT2810_0_2811",
            "next_target": "2811-Y5-R2FR-Ploc-norm-commutator-certificate-or-first-DeltaK00-source-under-AX1090.md",
            "script": "scripts/Y5_R2FR_Ploc_norm_commutator_certificate_or_first_DeltaK00_source_under_AX1090_2811.py",
            "objective": "try to prove P_loc is orthogonal/covariantly fixed so ||P_loc||=1 and [P_loc,nabla]=0; otherwise source a real K_hat^{00} row or keep DeltaK00 as explicit residual",
            "include": "P_loc inner product; idempotent versus orthogonal projector; nabla P_loc; local collar frame; DeltaK00 Khat/Kmetric components; no measured-G absorption",
            "exclude": "declaring P_loc norm one from idempotence; declaring commutator zero by notation; proxy scoring; local-GR/WEP/PPN/orbital claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["ploc_unit"], BRANCH_OUTPUTS["ploc_queue"], "ploc_queue"),
        (OUTPUTS["deltak00"], BRANCH_OUTPUTS["deltak00_queue"], "deltak00_queue"),
        (OUTPUTS["qdelta_units"], BRANCH_OUTPUTS["unit_beta_doc"], "unit_beta_doc"),
        (OUTPUTS["ploc_unit"], BRANCH_OUTPUTS["local_bound_copy"], "local_bound_copy"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2810_{label}",
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
        ("VAL2810_0_sources_exist", all(row["exists_or_reachable"] for row in sections["sources"]), "all source-register local paths exist"),
        ("VAL2810_1_sources_nonempty", all(row["contains_text"] for row in sections["sources"]), "all source-register entries contain text/source evidence"),
        ("VAL2810_2_ploc_unit_certificate_present", any(row["certificate_id"] == "PLC2810_5_verdict" and row["status"] == "PARTIAL_PASS_NONCLAIM" for row in sections["ploc_unit"]), "P_loc unit-only certificate verdict is present"),
        ("VAL2810_3_ploc_norm_blocked", any(row["certificate_id"] == "PLC2810_3_norm" and row["status"] == "NORM_NOT_CERTIFIED" for row in sections["ploc_unit"]), "P_loc norm-one is not smuggled"),
        ("VAL2810_4_commutator_blocked", any(row["certificate_id"] == "PLC2810_4_commutator" and row["status"] == "COMMUTATOR_NOT_ZEROED" for row in sections["ploc_unit"]), "P_loc commutator is retained"),
        ("VAL2810_5_DeltaK00_missing", any(row["attempt_id"] == "DK002810_5_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["deltak00"]), "DeltaK00 source attempt safely fails"),
        ("VAL2810_6_qdelta_unit_update", any(row["unit_id"] == "QDU2810_2_Ploc" and row["status"] == "PLOC_UNIT_ONLY_PARTIAL_PASS" for row in sections["qdelta_units"]), "q_DeltaK unit update records P_loc unit-only progress"),
        ("VAL2810_7_force_denominator_retained", any(row["link_id"] == "FL2810_0_gn" and row["value"] == "9.80665" for row in sections["force_link"]), "NIST g_n denominator seed is retained via 2807 source row"),
        ("VAL2810_8_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2810_9_next_target_2811", any(row["next_id"] == "NEXT2810_0_2811" for row in sections["next"]), "next target is 2811"),
        ("VAL2810_10_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2810_11_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2810_12_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2810_13_cited_paths_exist", cited_paths_exist(sections), "all cited local file/copy paths in generated rows exist"),
        ("VAL2810_14_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2810_15_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2810_16_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2810_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2810_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2810 certifies P_loc as unit-dimensionless only under same-domain projector typing, blocks norm/commutator promotion, and keeps DeltaK00 unsourced.",
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
        "# 2810 - Y5 R2FR First DeltaK Component Source Row Or Ploc Unit Certificate Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2810 takes the least-cheatable route. It does not invent a `Delta_K^{00}` component. The current files define `Delta_K^{00}=K_hat^{00}-K_metric^{00}`, but they still do not provide the actual `K_hat^{00}` component, boundary convention, or derivative constants.",
        "",
        "The real gain is a unit-only `P_loc` certificate: if `P_loc^nu_rho` is a same-domain local projector on the residual vector/force-density bundle, then it is dimensionless and `P_loc nabla_mu Delta_K^{mu nu}` has the same force-density unit as the unprojected stress divergence.",
        "",
        "That is useful but not enough. `||P_loc||=1` is not proven by idempotence alone, and `[P_loc,nabla]=0` is not proven by notation. Both remain live residual coefficients. No local-GR, WEP, PPN, orbital, clock, or source-normalization claim is made.",
        "",
        "## P_loc Unit Certificate",
        markdown_table(sections["ploc_unit"], ["certificate_id", "item", "statement", "status", "result"]),
        "",
        "## DeltaK00 Source Attempt",
        markdown_table(sections["deltak00"], ["attempt_id", "quantity", "candidate_expression", "status", "next_input_needed"]),
        "",
        "## q_DeltaK Unit Update",
        markdown_table(sections["qdelta_units"], ["unit_id", "quantity", "unit_result", "status", "reason"]),
        "",
        "## Force Denominator Link",
        markdown_table(sections["force_link"], ["link_id", "quantity", "value", "units", "status", "limitation"]),
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
        "ploc_unit": build_ploc_unit_rows(),
        "deltak00": build_deltak00_rows(),
        "qdelta_units": build_qdelta_unit_rows(),
        "force_link": build_force_link_rows(),
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
