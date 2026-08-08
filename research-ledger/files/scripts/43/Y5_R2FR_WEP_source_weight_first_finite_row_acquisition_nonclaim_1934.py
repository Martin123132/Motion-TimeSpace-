from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1934"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1934-Y5-R2FR-WEP-source-weight-first-finite-row-acquisition-nonclaim.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

ETA_CENTRAL = -1.5e-15
ETA_STAT_SIGMA = 2.3e-15
ETA_SYST_SIGMA = 1.5e-15
ETA_COMBINED_SIGMA = math.sqrt(ETA_STAT_SIGMA**2 + ETA_SYST_SIGMA**2)
ETA_REPORTED_NO_VIOLATION_LEVEL = 2.7e-15
PT_PT_NULL_SIGMA = 1.1e-15

LOCAL_SOURCES = {
    "1933_doc": ROOT / "1933-Y5-R2FR-coefficient-descent-typing-proof-or-finite-source-row-selection.md",
    "1933_validation": OUT / "P8_Y5_BRR545_1933_VALIDATION.csv",
    "1933_selection": OUT / "P8_Y5_PARENT_QLOC_1933_FINITE_ROW_SELECTION.csv",
    "1933_closure": OUT / "P8_Y5_PARENT_QLOC_1933_MINIMAL_CLOSURE.csv",
    "1933_claims": OUT / "P8_Y5_PARENT_QLOC_1933_CLAIM_GATE.csv",
    "1933_next": OUT / "P8_Y5_PARENT_QLOC_1933_NEXT_TARGET.csv",
}

NEEDLES = {
    "1933_doc": ["SEL1933_1_WEP_source_weight", "VAL1933_OVERALL"],
    "1933_validation": ["VAL1933_OVERALL", "PASS"],
    "1933_selection": ["SEL1933_1_WEP_source_weight", "SELECTED_FIRST_FINITE_ROW"],
    "1933_closure": ["CLOS1933_0_minimal_descent_clause", "EXPLICIT_CLOSURE_UNLESS_PARENT_SIGNED"],
    "1933_claims": ["CG1933_3_WEP_finite_row", "FAIL_BLOCKED"],
    "1933_next": ["NEXT1933_0_primary", "WEP-source-weight"],
}

WEB_SOURCES = [
    {
        "web_source_id": "WEB1934_0_MICROSCOPE_PRL",
        "title": "MICROSCOPE mission: final results of the test of the Equivalence Principle",
        "url": "https://arxiv.org/abs/2209.15487",
        "doi": "https://doi.org/10.1103/PhysRevLett.129.121102",
        "journal_reference": "Phys. Rev. Lett. 129, 121102 (2022)",
        "used_for": "modern WEP mission anchor and Ti/Pt eta result",
        "extraction_method": "web_browse_arxiv_abstract_2026-06-19",
        "confidence": "high",
    },
    {
        "web_source_id": "WEB1934_1_MICROSCOPE_CQG",
        "title": "Result of the MICROSCOPE Weak Equivalence Principle test",
        "url": "https://arxiv.org/abs/2209.15488",
        "doi": "https://doi.org/10.1088/1361-6382/ac84be",
        "journal_reference": "Class. Quantum Grav. 39, 204009 (2022)",
        "used_for": "eta definition, combined 2.7e-15 level, same-material null check",
        "extraction_method": "web_browse_arxiv_abstract_2026-06-19",
        "confidence": "high",
    },
]

OUTPUTS = {
    "local_source_register": OUT / "P8_Y5_PARENT_QLOC_1934_LOCAL_SOURCE_REGISTER.csv",
    "web_source_register": OUT / "P8_Y5_PARENT_QLOC_1934_WEB_SOURCE_REGISTER.csv",
    "wep_bound_row": OUT / "P8_Y5_PARENT_QLOC_1934_WEP_SOURCE_WEIGHT_BOUND_ROW.csv",
    "mts_projection_requirements": OUT / "P8_Y5_PARENT_QLOC_1934_MTS_WEP_PROJECTION_REQUIREMENTS.csv",
    "nonclaim_smoke_row": OUT / "P8_Y5_PARENT_QLOC_1934_WEP_SOURCE_WEIGHT_NONCLAIM_SMOKE_ROW.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1934_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1934_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1934_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1934_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1934_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_bound": SOURCE_WEIGHT_DOCS / "MICROSCOPE_WEP_SOURCE_WEIGHT_BOUND_ROW_1934_NONCLAIM.csv",
    "microscope_bound": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1934_WEP_BOUND_ROW_NONCLAIM.csv",
    "projection_queue": QUEUE / "JR1934_MTS_WEP_PROJECTION_MAP_ACQUISITION_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1934_CLAIM_GATE.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def local_source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_key, source_path in LOCAL_SOURCES.items():
        path_exists = source_path.exists()
        source_text = read_text(source_path) if path_exists else ""
        missing_needles = [needle for needle in NEEDLES[source_key] if needle not in source_text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": source_key,
                "source_path": str(source_path),
                "needed_for": "1934 WEP source-weight first finite nonclaim row",
                "needles": ";".join(NEEDLES[source_key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path_exists and not missing_needles else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing_needles),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def web_source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            **source,
            "status": "WEB_SOURCE_RECORDED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for source in WEB_SOURCES
    ]


def wep_bound_row() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_id": "WEP1934_0_MICROSCOPE_TiPt_eta",
            "observable": "eta_Ti_Pt",
            "definition": "eta(A,B)=2(a_A-a_B)/(a_A+a_B)",
            "test_masses": "Titanium alloy; Platinum alloy",
            "central_value": ETA_CENTRAL,
            "stat_sigma": ETA_STAT_SIGMA,
            "syst_sigma": ETA_SYST_SIGMA,
            "combined_sigma_quadrature": ETA_COMBINED_SIGMA,
            "reported_no_violation_level_abs_eta": ETA_REPORTED_NO_VIOLATION_LEVEL,
            "same_material_null_sigma_PtPt": PT_PT_NULL_SIGMA,
            "units": "dimensionless",
            "source_url": "https://arxiv.org/abs/2209.15488",
            "source_doi": "https://doi.org/10.1088/1361-6382/ac84be",
            "crosscheck_url": "https://arxiv.org/abs/2209.15487",
            "crosscheck_doi": "https://doi.org/10.1103/PhysRevLett.129.121102",
            "extraction_status": "SOURCE_BACKED_OBSERVABLE_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
            "claim_blocker": "MTS source-weight-to-eta projection and material charges are not yet derived",
            "generated_utc": GENERATED_UTC,
        }
    ]


def mts_projection_requirement_rows() -> list[dict[str, Any]]:
    requirements = [
        ("REQ1934_0_projection_map", "derive eta_pred from MTS source-weight residual", "eta_pred = P_WEP[Delta w_TiPt, tau_WEP, source field, Earth composition]", "MISSING_MTS_PROJECTION_MAP"),
        ("REQ1934_1_material_charges", "define MTS charges for Ti alloy and Pt alloy", "Delta Q_TiPt or equivalent composition sensitivity", "MISSING_MATERIAL_CHARGE_LEDGER"),
        ("REQ1934_2_tau_WEP", "derive or source tau_WEP normalization", "dimensionless transfer from local source residual to differential acceleration", "MISSING_TAU_WEP"),
        ("REQ1934_3_environment_source", "define Earth/source environment entering the WEP test", "source field, gradient, orbital configuration, screening/plateau assumptions", "MISSING_ARENA_SOURCE_MODEL"),
        ("REQ1934_4_sign_units", "fix sign and unit convention", "eta_pred must be dimensionless and comparable to MICROSCOPE eta", "MISSING_UNIT_SIGN_CONTRACT"),
        ("REQ1934_5_acceptance_rule", "define bound comparison rule", "abs(eta_pred) <= selected eta bound with declared confidence level", "MISSING_ACCEPTANCE_RULE"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "requirement_id": requirement_id,
            "needed_input": needed_input,
            "target_formula_or_object": target_formula,
            "status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for requirement_id, needed_input, target_formula, status in requirements
    ]


def nonclaim_smoke_row() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "smoke_id": "SMOKE1934_0_MTS_WEP_source_weight_placeholder",
            "observable": "eta_Ti_Pt",
            "eta_bound_abs": ETA_REPORTED_NO_VIOLATION_LEVEL,
            "eta_bound_units": "dimensionless",
            "mts_prediction_symbolic": "eta_pred = P_WEP(Delta_w_TiPt, tau_WEP, Q_Earth, local_source_profile)",
            "Delta_w_TiPt": "MISSING_MTS_SOURCE_WEIGHT_DIFFERENCE",
            "tau_WEP": "MISSING_TAU_WEP",
            "Q_Earth": "MISSING_SOURCE_ENVIRONMENT",
            "local_source_profile": "MISSING_LOCAL_PROFILE",
            "comparison_status": "SCHEMA_READY_NUMERIC_CLAIM_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "claim_blocker": "symbolic MTS inputs are placeholders",
            "generated_utc": GENERATED_UTC,
        }
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1934_0_source_bound", "MICROSCOPE WEP observable bound is source-backed", "PASS_NONCLAIM", "real eta bound row recorded with URL and DOI"),
        ("CG1934_1_mts_projection", "MTS predicts eta_Ti_Pt numerically", "FAIL_BLOCKED", "projection map and material charges missing"),
        ("CG1934_2_tau_WEP", "tau_WEP is derived or sourced", "FAIL_BLOCKED", "tau_WEP remains missing"),
        ("CG1934_3_WEP_pass", "MTS passes MICROSCOPE WEP", "FAIL_BLOCKED", "no numeric eta_pred comparison allowed"),
        ("CG1934_4_local_GR_Newton", "local GR/Newton source coupling is derived", "FAIL_BLOCKED", "WEP row is evidence plumbing, not source-coupling theorem"),
        ("CG1934_5_public_claim", "1934 supports public WEP/local-GR claim", "FAIL_BLOCKED", "all MTS rows remain claim=false"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1934_0_bound_acquired",
            "decision": "MICROSCOPE_TIPT_BOUND_ACQUIRED_NONCLAIM",
            "rationale": "This is the cleanest modern WEP source bound for composition-dependent acceleration.",
            "next_action": "derive the MTS WEP projection map before any pass/fail comparison",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1934_1_claim_status",
            "decision": "NO_WEP_OR_LOCAL_GR_CLAIM",
            "rationale": "A real experimental bound does not become an MTS test until eta_pred is derived from MTS quantities.",
            "next_action": "build material charge and tau_WEP requirements ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1934_0_primary",
            "selection_status": "selected",
            "target_doc": "1935-Y5-R2FR-MTS-WEP-eta-projection-map-or-material-charge-ledger.md",
            "target_script": "scripts/Y5_R2FR_MTS_WEP_eta_projection_map_or_material_charge_ledger_1935.py",
            "objective": "derive eta_pred for MICROSCOPE Ti/Pt from MTS source-weight residuals, or create a material-charge/tau_WEP ledger that keeps the WEP comparison blocked",
            "success_condition": "a symbolic-to-numeric MTS WEP projection contract with all needed inputs named, or an explicit blocker ledger with claim=false",
            "do_not": "do not set tau_WEP=1, invent Ti/Pt material charges, absorb Delta w into measured G, claim WEP pass, claim local GR, or modify formalization-workbench",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1934_0_project_position",
            "status": "REAL_WEP_BOUND_ACQUIRED_NONCLAIM",
            "summary": "1934 adds a source-backed MICROSCOPE Ti/Pt eta bound but does not treat it as an MTS pass.",
            "strongest_result": f"eta_TiPt central={ETA_CENTRAL:.3e}, combined_sigma={ETA_COMBINED_SIGMA:.3e}, reported level={ETA_REPORTED_NO_VIOLATION_LEVEL:.3e}",
            "missing_piece": "MTS eta projection map, Ti/Pt material charges, tau_WEP, and acceptance rule",
            "claim_position": "WEP/local-GR/Newton claims remain blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def copy_branch_artifacts(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    write_csv(BRANCH_COPIES["source_weight_bound"], rows_by_name["wep_bound_row"])
    write_csv(BRANCH_COPIES["microscope_bound"], rows_by_name["wep_bound_row"])
    write_csv(BRANCH_COPIES["projection_queue"], rows_by_name["mts_projection_requirements"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for artifact in FORMALIZATION.rglob("*1934*") if artifact.is_file())


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validation_rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        validation_rows.append(
            {
                "validation_id": validation_id,
                "status": "PASS" if status else "FAIL",
                "detail": detail,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    add("VAL1934_00_local_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["local_source_register"]), "all local source paths exist and needles found")
    add("VAL1934_01_web_sources", len(rows_by_name["web_source_register"]) == 2 and all(str(row["url"]).startswith("https://arxiv.org/abs/2209.154") for row in rows_by_name["web_source_register"]), "MICROSCOPE web sources recorded with arXiv URLs")
    bound = rows_by_name["wep_bound_row"][0]
    bound_ok = float(bound["reported_no_violation_level_abs_eta"]) > 0 and bound["units"] == "dimensionless" and "doi.org" in bound["source_doi"]
    add("VAL1934_02_bound_row", bound_ok, "positive dimensionless eta bound with DOI recorded")
    add("VAL1934_03_projection_requirements", len(rows_by_name["mts_projection_requirements"]) == 6 and all(str(row["status"]).startswith("MISSING_") for row in rows_by_name["mts_projection_requirements"]), "MTS projection blockers explicitly named")
    smoke = rows_by_name["nonclaim_smoke_row"][0]
    add("VAL1934_04_nonclaim_smoke", smoke["comparison_status"] == "SCHEMA_READY_NUMERIC_CLAIM_BLOCKED" and "MISSING_" in smoke["Delta_w_TiPt"], "smoke row remains symbolic and blocked")
    add("VAL1934_05_claim_gates", any(row["status"] == "PASS_NONCLAIM" for row in rows_by_name["claim_gate"]) and all(row["claim_allowed"] is False for row in rows_by_name["claim_gate"]), "only source-bound gate passes as nonclaim; all claim flags false")
    add("VAL1934_06_decision", any(row["decision"] == "MICROSCOPE_TIPT_BOUND_ACQUIRED_NONCLAIM" for row in rows_by_name["decision"]), "bound acquired decision recorded")
    add("VAL1934_07_next_target", rows_by_name["next_target"][0]["target_doc"].startswith("1935-Y5-R2FR-MTS-WEP-eta-projection"), "1935 MTS WEP projection target selected")
    add("VAL1934_08_claim_flags_safe", all(str(row.get("valid_for_claim")) == "False" and str(row.get("claim_allowed")) == "False" for rows in rows_by_name.values() for row in rows), "claim flags all false")

    csv_ok = True
    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        try:
            csv_ok = csv_ok and bool(parse_csv(output_path))
        except Exception:
            csv_ok = False
    add("VAL1934_09_csv_parse", csv_ok, "all generated CSVs parse with rows")
    add("VAL1934_10_branch_copies", all(path.exists() and bool(parse_csv(path)) for path in BRANCH_COPIES.values()), "; ".join(str(path) for path in BRANCH_COPIES.values()))
    add("VAL1934_11_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent")
    formalization_count = formalization_artifact_count()
    add("VAL1934_12_formalization_untouched", formalization_count == 0, f"formalization_1934_artifact_count={formalization_count}")

    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        {
            "validation_id": "VAL1934_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "1934 WEP source-weight first finite row acquisition nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1934 Y5 R2FR: WEP Source-Weight First Finite Row Acquisition Nonclaim",
        "",
        "## Verdict",
        "",
        "1934 acquires a real source-backed MICROSCOPE Ti/Pt WEP bound as the first finite source-weight row. This is **not** an MTS WEP pass: the MTS projection from source-weight residuals to `eta_TiPt` is still missing.",
        "",
        f"Recorded bound: `eta_TiPt = {ETA_CENTRAL:.3e}` with statistical sigma `{ETA_STAT_SIGMA:.3e}`, systematic sigma `{ETA_SYST_SIGMA:.3e}`, quadrature sigma `{ETA_COMBINED_SIGMA:.3e}`, and reported no-violation level `{ETA_REPORTED_NO_VIOLATION_LEVEL:.3e}`.",
        "",
        "## Local Source Register",
        "",
        markdown_table(rows_by_name["local_source_register"]),
        "",
        "## Web Source Register",
        "",
        markdown_table(rows_by_name["web_source_register"]),
        "",
        "## WEP Bound Row",
        "",
        markdown_table(rows_by_name["wep_bound_row"]),
        "",
        "## MTS Projection Requirements",
        "",
        markdown_table(rows_by_name["mts_projection_requirements"]),
        "",
        "## Nonclaim Smoke Row",
        "",
        markdown_table(rows_by_name["nonclaim_smoke_row"]),
        "",
        "## Claim Gate",
        "",
        markdown_table(rows_by_name["claim_gate"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows_by_name["decision"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows_by_name["next_target"]),
        "",
        "## Project Status Snapshot",
        "",
        markdown_table(rows_by_name["status_snapshot"]),
        "",
        "## Validation",
        "",
        markdown_table(rows_by_name["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_COEFFS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)

    rows_by_name = {
        "local_source_register": local_source_register_rows(),
        "web_source_register": web_source_register_rows(),
        "wep_bound_row": wep_bound_row(),
        "mts_projection_requirements": mts_projection_requirement_rows(),
        "nonclaim_smoke_row": nonclaim_smoke_row(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "status_snapshot": status_snapshot_rows(),
    }

    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        write_csv(output_path, rows_by_name[output_key])

    copy_branch_artifacts(rows_by_name)
    remove_pycache()
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
