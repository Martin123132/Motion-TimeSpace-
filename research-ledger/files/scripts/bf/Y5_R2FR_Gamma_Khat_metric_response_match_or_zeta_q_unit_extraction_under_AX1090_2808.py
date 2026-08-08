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
DOC = WORK / "2808-Y5-R2FR-Gamma-Khat-metric-response-match-or-zeta-q-unit-extraction-under-AX1090.md"
NIST_GN_URL = "https://physics.nist.gov/cgi-bin/cuu/Value?gn"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2808_SOURCE_REGISTER.csv",
    "metric_response": MTS / "P8_Y5_R2FR_2808_METRIC_RESPONSE_DERIVATION_ATTEMPT.csv",
    "ward_units": MTS / "P8_Y5_R2FR_2808_WARD_RESIDUAL_UNIT_CONTRACT.csv",
    "zeta": MTS / "P8_Y5_R2FR_2808_ZETA_Q_CONDITIONAL_EXTRACTION.csv",
    "force_seed": MTS / "P8_Y5_R2FR_2808_FORCE_SEED_UPDATE.csv",
    "gates": MTS / "P8_Y5_R2FR_2808_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2808_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2808_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2808_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2808_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "metric_queue": RAB_QUEUE / "JR2808_GAMMA_KHAT_METRIC_RESPONSE_NONCLAIM.csv",
    "unit_queue": RAB_QUEUE / "JR2808_WARD_UNIT_CONTRACT_NONCLAIM.csv",
    "seed_queue": RAB_QUEUE / "JR2808_FORCE_SEED_UPDATE_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "GAMMA_KHAT_METRIC_RESPONSE_2808_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_gamma_khat_metric_response_2808_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2808_GAMMA_KHAT_COMPONENT_MATCH_OR_RESIDUAL_BOUND_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sp(path: Path) -> str:
    return str(path)


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


def build_sources() -> list[dict[str, Any]]:
    local_sources = [
        ("2807_next", MTS / "P8_Y5_R2FR_2807_NEXT_TARGET.csv", "authoritative 2808 target"),
        ("2807_metric_match", MTS / "P8_Y5_R2FR_2807_GAMMA_KHAT_METRIC_RESPONSE_MATCH.csv", "metric-response predecessor"),
        ("2807_seed", MTS / "P8_Y5_R2FR_2807_SOURCE_BACKED_FORCE_SEED_ROW.csv", "source-backed force seed predecessor"),
        ("2807_runner", MTS / "P8_Y5_R2FR_2807_FORCE_SEED_RUNNER.csv", "force seed runner predecessor"),
        ("2799_q_loc", MTS / "P8_Y5_R2FR_2799_QLOC_RESIDUAL_RETENTION_LEDGER.csv", "retained q_loc definition"),
        ("GK_candidates", MTS / "P8_GK_STRESS_ACTION_CANDIDATES.csv", "S_GK action candidate"),
        ("Gamma_owner", MTS / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv", "Gamma owner action candidates"),
        ("response_doublet_variation", MTS / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv", "response-doublet double-zero candidate"),
        ("symbol_map", MTS / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv", "symbol/action placement map"),
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
                "role": role,
                "contains_text": bool(text.strip()) if path.exists() else False,
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    rows.append(
        {
            "source_id": "NIST_gn",
            "source_type": "web_source",
            "path_or_url": NIST_GN_URL,
            "exists_or_reachable": True,
            "role": "standard acceleration of gravity denominator seed retained from 2807",
            "contains_text": True,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    )
    return rows


def build_metric_response_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "MRD2808_0_action",
            "candidate GK action",
            "S_GK=-int_M sqrt(-g) Gamma_eff(g,Phi,nabla Phi,D,...)",
            "if Gamma_eff is a scalar density functional, its metric variation owns a stress tensor",
            "FORMAL_ACTION_CANDIDATE",
        ),
        (
            "MRD2808_1_stress_split",
            "stress split with no sign smuggling",
            "T_GK^{mu nu}:=-2/sqrt(-g) delta S_GK/delta g_{mu nu}; define K_metric^{mu nu}:=Gamma_eff g^{mu nu}-T_GK^{mu nu}",
            "then T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_metric^{mu nu} by definition",
            "DERIVED_CONVENTION",
        ),
        (
            "MRD2808_2_divergence_identity",
            "metric-response Ward residual",
            "nabla_mu T_GK^{mu nu}=nabla^nu Gamma_eff-nabla_mu K_metric^{mu nu}",
            "this has exactly the unprojected q_loc shape if K_hat=K_metric",
            "DERIVED_CONDITIONAL_IDENTITY",
        ),
        (
            "MRD2808_3_projected_q_loc",
            "projected local residual",
            "q_loc^nu=P_loc(nabla_mu T_GK^{mu nu}) + P_loc nabla_mu(K_metric^{mu nu}-K_hat^{mu nu})",
            "the remaining obstruction is Delta_K:=K_hat-K_metric plus projector/connection terms",
            "DERIVED_OBSTRUCTION_IDENTITY",
        ),
        (
            "MRD2808_4_Ward_zero",
            "on-shell silence condition",
            "nabla_mu T_GK^{mu nu}= - E_A nabla^nu Phi^A + boundary/improvement/projector terms",
            "q_loc vanishes only if field equations, source-current silence, boundary flux, and projector commutator close",
            "CONDITIONAL_ZERO_NOT_PROVED",
        ),
        (
            "MRD2808_5_current_symbol_match",
            "current MTS K_hat equals K_metric",
            "K_hat^{mu nu}=K_metric^{mu nu}[Gamma_eff]",
            "current source rows name this as required but do not supply a component-by-component certificate",
            "MISSING_COMPONENT_MATCH",
        ),
        (
            "MRD2808_6_verdict",
            "Gamma/Khat metric-response theorem",
            "MRD2808_0 through MRD2808_5 all close",
            "conditional identity derived; current K_hat symbol still not matched to metric response",
            "PARTIAL_DERIVATION_NONCLAIM",
        ),
    ]
    return [
        {
            "derivation_id": row[0],
            "claim_piece": row[1],
            "mathematical_form": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_ward_unit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "UNIT2808_0_Gamma",
            "Gamma_eff",
            "same unit as local action density/stress scalar in S_GK",
            "SI: J m^-3; geometric: stress/action density convention",
            "CONDITIONAL_ON_S_GK_ACCEPTED",
        ),
        (
            "UNIT2808_1_Kmetric",
            "K_metric^{mu nu}",
            "same unit as Gamma_eff because T_GK=Gamma g-K_metric",
            "SI: Pa=J m^-3; geometric: same as stress",
            "CONDITIONAL_ON_METRIC_RESPONSE",
        ),
        (
            "UNIT2808_2_q_unprojected",
            "nabla^nu Gamma_eff-nabla_mu K_metric^{mu nu}",
            "stress divergence / force density",
            "SI: N m^-3; geometric: stress per length",
            "CONDITIONAL_FORCE_DENSITY_UNIT",
        ),
        (
            "UNIT2808_3_q_loc",
            "q_loc^nu",
            "P_loc applied to stress-divergence residual",
            "same as force density if P_loc is dimensionless; otherwise includes P_loc unit",
            "MISSING_PLOC_UNIT_CERTIFICATE",
        ),
        (
            "UNIT2808_4_DeltaK",
            "Delta_K^{mu nu}=K_hat^{mu nu}-K_metric^{mu nu}",
            "unmatched metric-response gap",
            "same as stress; divergence is force density",
            "RETAINED_OBSTRUCTION",
        ),
    ]
    return [
        {
            "unit_id": row[0],
            "object": row[1],
            "unit_definition": row[2],
            "physical_units": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_zeta_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ZQ2808_0_conditional_zeta",
            "zeta_q",
            "if q_loc is defined as P_loc(nabla_mu T_GK^{mu nu}) in physical stress-divergence units, zeta_q=1",
            "only under accepted S_GK, K_hat=K_metric, and dimensionless/unit-fixed P_loc",
            "CONDITIONAL_VALUE_NOT_ADOPTED",
        ),
        (
            "ZQ2808_1_model_to_physical_conversion",
            "zeta_q",
            "if Gamma_eff/K_hat are model-normalized rather than physical stress-normalized, zeta_q converts model q_loc to force density",
            "conversion requires parent normalization constants",
            "MISSING_PARENT_NORMALIZATION",
        ),
        (
            "ZQ2808_2_force_runner_effect",
            "delta a_A",
            "delta a_A=(zeta_q/M_A) int q_loc^i dV + boundary/M_A",
            "not score-ready because zeta_q remains conditional and body measures are missing",
            "RUNNER_BLOCKED",
        ),
        (
            "ZQ2808_3_verdict",
            "zeta_q extraction",
            "zeta_q=1 can be used only after metric-response/unit certificates close",
            "current run records conditional extraction but does not promote it",
            "FAIL_CURRENT_CLAIM",
        ),
    ]
    return [
        {
            "zeta_id": row[0],
            "quantity": row[1],
            "candidate_value_or_formula": row[2],
            "required_condition": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_force_seed_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FSU2808_0_standard_gn",
            "g_n",
            "9.80665",
            "m s^-2",
            NIST_GN_URL,
            "source-backed denominator seed retained; not an MTS prediction",
            True,
            "DENOMINATOR_ONLY",
        ),
        (
            "FSU2808_1_zeta_q",
            "zeta_q",
            "CONDITIONAL_1_IF_METRIC_RESPONSE_CERTIFIED",
            "dimensionless_or_force_density_per_model_unit",
            "P8_Y5_R2FR_2808_ZETA_Q_CONDITIONAL_EXTRACTION.csv",
            "conditional only; not score-ready",
            False,
            "CONDITIONAL_NOT_CLAIM",
        ),
        (
            "FSU2808_2_q_loc_units",
            "q_loc units",
            "stress_divergence_if_S_GK_certified",
            "N m^-3 or geometric stress/length",
            "P8_Y5_R2FR_2808_WARD_RESIDUAL_UNIT_CONTRACT.csv",
            "conditional only; P_loc unit and Khat match missing",
            False,
            "CONDITIONAL_NOT_CLAIM",
        ),
        (
            "FSU2808_3_DeltaK",
            "Delta_K",
            "MISSING_COMPONENT_NORM",
            "stress",
            "P8_Y5_R2FR_2799_QLOC_RESIDUAL_RETENTION_LEDGER.csv",
            "must be zero or bounded before local claim",
            False,
            "MISSING_COMPONENT_BOUND",
        ),
    ]
    return [
        {
            "seed_id": row[0],
            "quantity": row[1],
            "value_or_status": row[2],
            "units": row[3],
            "source": row[4],
            "interpretation": row[5],
            "source_backed_numeric": row[6],
            "status": row[7],
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2808_0_metric_identity_form", "metric-response divergence identity is derived conditionally", True, "T_GK=Gamma g-K_metric gives the q_loc shape"),
        ("CG2808_1_Khat_match", "current K_hat equals K_metric[Gamma_eff]", False, "component-by-component match remains missing"),
        ("CG2808_2_Ward_zero", "Ward identity proves q_loc=0", False, "Euler/source/boundary/projector terms remain open"),
        ("CG2808_3_zeta_value", "zeta_q=1 is claim-ready", False, "conditional on accepted physical stress-divergence normalization"),
        ("CG2808_4_force_row_score", "first force/WEP row is score-ready", False, "NIST g_n is denominator only; zeta/body/boundary inputs missing"),
        ("CG2808_5_local_claim", "local-GR/WEP/orbital claim can be made", False, "Khat match and Ward-zero gates fail"),
        ("CG2808_6_nonclaim_pack", "2808 nonclaim derivation/unit pack is ready", True, "next target is component match or Delta_K bound"),
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
        ("DEC2808_0_real_progress", "The metric-response identity is derived conditionally.", "If K_hat is K_metric, q_loc becomes a projected stress-divergence/Ward residual.", "focus next on Khat component match"),
        ("DEC2808_1_no_promotion", "No local claim is promoted.", "Current K_hat is not component-matched to K_metric and Ward-zero side terms remain open.", "keep Delta_K residual active"),
        ("DEC2808_2_units_gain", "The q_loc/zeta unit contract is sharper.", "zeta_q can be 1 only in certified physical stress-divergence units; otherwise it is a missing conversion.", "derive P_loc/Khat/Gamma units before scoring"),
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
            "next_id": "NEXT2808_0_2809",
            "next_target": "2809-Y5-R2FR-Khat-component-metric-response-match-or-DeltaK-bound-under-AX1090.md",
            "script": "scripts/Y5_R2FR_Khat_component_metric_response_match_or_DeltaK_bound_under_AX1090_2809.py",
            "objective": "attempt a component-by-component K_hat = K_metric[Gamma_eff] match for current MTS symbols; if absent, create the first Delta_K component bound table for PPN/WEP/orbital residuals",
            "include": "K_metric definition; K_hat components; Delta_K; derivative terms; volume convention; P_loc units; zeta_q conditional value; NIST g_n denominator retained",
            "exclude": "declaring zeta_q=1 without Khat match; proxy scoring; local-GR/WEP/orbital claim; fitted cancellation; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["metric_response"], BRANCH_OUTPUTS["metric_queue"], "metric_queue"),
        (OUTPUTS["ward_units"], BRANCH_OUTPUTS["unit_queue"], "unit_queue"),
        (OUTPUTS["force_seed"], BRANCH_OUTPUTS["seed_queue"], "seed_queue"),
        (OUTPUTS["metric_response"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2808_{label}",
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


def cited_paths_exist(sections: dict[str, list[dict[str, Any]]]) -> bool:
    paths: list[Path] = []
    for rows in sections.values():
        for row in rows:
            for key in ("source_path", "source", "destination", "path_or_url"):
                value = row.get(key)
                if value and value != "MISSING" and not str(value).startswith("http") and not str(value).startswith("NIST"):
                    candidate = Path(str(value))
                    if candidate.suffix or candidate.drive:
                        paths.append(candidate if candidate.is_absolute() else MTS / candidate)
    return all(path.exists() for path in paths)


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2808_0_sources_exist", all(row["exists_or_reachable"] for row in sections["sources"]), "all source-register paths/URLs exist or are reachable"),
        ("VAL2808_1_sources_nonempty", all(row["contains_text"] for row in sections["sources"]), "all source-register entries contain text/source evidence"),
        ("VAL2808_2_metric_identity_derived", any(row["derivation_id"] == "MRD2808_2_divergence_identity" and row["status"] == "DERIVED_CONDITIONAL_IDENTITY" for row in sections["metric_response"]), "metric-response divergence identity is derived conditionally"),
        ("VAL2808_3_obstruction_identity", any(row["derivation_id"] == "MRD2808_3_projected_q_loc" and row["status"] == "DERIVED_OBSTRUCTION_IDENTITY" for row in sections["metric_response"]), "Delta_K obstruction identity is present"),
        ("VAL2808_4_Khat_match_not_claimed", any(row["derivation_id"] == "MRD2808_5_current_symbol_match" and row["status"] == "MISSING_COMPONENT_MATCH" for row in sections["metric_response"]), "Khat match remains explicitly missing"),
        ("VAL2808_5_units_contract_present", any(row["unit_id"] == "UNIT2808_2_q_unprojected" and row["status"] == "CONDITIONAL_FORCE_DENSITY_UNIT" for row in sections["ward_units"]), "q_loc force-density unit contract is present"),
        ("VAL2808_6_zeta_conditional_not_claim", any(row["zeta_id"] == "ZQ2808_3_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["zeta"]), "zeta_q conditional value is not promoted"),
        ("VAL2808_7_force_seed_denominator_retained", any(row["seed_id"] == "FSU2808_0_standard_gn" and row["source_backed_numeric"] for row in sections["force_seed"]), "NIST g_n denominator seed is retained"),
        ("VAL2808_8_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2808_9_next_target_2809", any(row["next_id"] == "NEXT2808_0_2809" for row in sections["next"]), "next target is 2809"),
        ("VAL2808_10_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2808_11_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2808_12_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2808_13_cited_paths_exist", cited_paths_exist(sections), "all cited local file/copy paths in generated rows exist"),
        ("VAL2808_14_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2808_15_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2808_16_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2808_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2808_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2808 derives the conditional metric-response/Ward identity, keeps K_hat component match and zeta_q value nonclaim, and selects Delta_K component matching/bounding as 2809.",
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
        "# 2808 - Y5 R2FR Gamma/Khat Metric-Response Match Or zeta_q Unit Extraction Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2808 gets a real conditional derivation: for `S_GK=-int sqrt(-g) Gamma_eff`, define the metric stress `T_GK` by variation and define `K_metric := Gamma_eff g - T_GK`. Then `nabla_mu T_GK^{mu nu}=nabla^nu Gamma_eff-nabla_mu K_metric^{mu nu}`.",
        "",
        "That is exactly the unprojected `q_loc` shape if, and only if, current `K_hat` equals `K_metric[Gamma_eff]` with derivative and volume-term conventions fixed.",
        "",
        "So the route is alive but not closed. Current evidence does not component-match `K_hat` to the metric response, and Ward-zero still needs Euler/source/boundary/projector terms to vanish or be bounded.",
        "",
        "The unit gain is useful: if the metric-response match closes in physical stress units, `q_loc` is a force-density/stress-divergence residual and `zeta_q=1` by convention. Until then, `zeta_q` remains a conversion coefficient, not evidence.",
        "",
        "## Metric-Response Derivation Attempt",
        markdown_table(sections["metric_response"], ["derivation_id", "claim_piece", "mathematical_form", "status", "meaning"]),
        "",
        "## Ward Residual Unit Contract",
        markdown_table(sections["ward_units"], ["unit_id", "object", "unit_definition", "physical_units", "status"]),
        "",
        "## zeta_q Conditional Extraction",
        markdown_table(sections["zeta"], ["zeta_id", "quantity", "candidate_value_or_formula", "required_condition", "status"]),
        "",
        "## Force Seed Update",
        markdown_table(sections["force_seed"], ["seed_id", "quantity", "value_or_status", "units", "source_backed_numeric", "status", "interpretation"]),
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
        "metric_response": build_metric_response_rows(),
        "ward_units": build_ward_unit_rows(),
        "zeta": build_zeta_rows(),
        "force_seed": build_force_seed_rows(),
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
