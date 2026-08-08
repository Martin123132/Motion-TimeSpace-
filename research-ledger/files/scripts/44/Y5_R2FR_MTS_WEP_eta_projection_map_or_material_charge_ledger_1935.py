from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1935"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1935-Y5-R2FR-MTS-WEP-eta-projection-map-or-material-charge-ledger.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

ETA_BOUND_ABS = 2.7e-15
ETA_CENTRAL = -1.5e-15
ETA_COMBINED_SIGMA = 2.745906043549196e-15

SOURCES = {
    "1934_doc": ROOT / "1934-Y5-R2FR-WEP-source-weight-first-finite-row-acquisition-nonclaim.md",
    "1934_validation": OUT / "P8_Y5_BRR545_1934_VALIDATION.csv",
    "1934_bound": OUT / "P8_Y5_PARENT_QLOC_1934_WEP_SOURCE_WEIGHT_BOUND_ROW.csv",
    "1934_requirements": OUT / "P8_Y5_PARENT_QLOC_1934_MTS_WEP_PROJECTION_REQUIREMENTS.csv",
    "1934_smoke": OUT / "P8_Y5_PARENT_QLOC_1934_WEP_SOURCE_WEIGHT_NONCLAIM_SMOKE_ROW.csv",
    "1934_claims": OUT / "P8_Y5_PARENT_QLOC_1934_CLAIM_GATE.csv",
    "1934_next": OUT / "P8_Y5_PARENT_QLOC_1934_NEXT_TARGET.csv",
    "1933_closure": OUT / "P8_Y5_PARENT_QLOC_1933_MINIMAL_CLOSURE.csv",
    "1933_residuals": OUT / "P8_Y5_PARENT_QLOC_1933_FIBER_RESIDUAL_LEDGER.csv",
}

NEEDLES = {
    "1934_doc": ["WEP1934_0_MICROSCOPE_TiPt_eta", "REQ1934_0_projection_map", "VAL1934_OVERALL"],
    "1934_validation": ["VAL1934_OVERALL", "PASS"],
    "1934_bound": ["WEP1934_0_MICROSCOPE_TiPt_eta", "2.7e-15"],
    "1934_requirements": ["REQ1934_0_projection_map", "REQ1934_5_acceptance_rule"],
    "1934_smoke": ["SMOKE1934_0_MTS_WEP_source_weight_placeholder", "MISSING_TAU_WEP"],
    "1934_claims": ["CG1934_1_mts_projection", "FAIL_BLOCKED"],
    "1934_next": ["NEXT1934_0_primary", "eta-projection"],
    "1933_closure": ["CLOS1933_0_minimal_descent_clause", "CLOS1933_1_preservation_clause"],
    "1933_residuals": ["RES1933_1_source_weight", "ACTIVE_IF_DESCENT_UNSIGNED"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1935_SOURCE_REGISTER.csv",
    "eta_projection_theorem": OUT / "P8_Y5_PARENT_QLOC_1935_WEP_ETA_PROJECTION_THEOREM.csv",
    "mts_projection_contract": OUT / "P8_Y5_PARENT_QLOC_1935_MTS_WEP_PROJECTION_CONTRACT.csv",
    "product_bound": OUT / "P8_Y5_PARENT_QLOC_1935_WEP_PRODUCT_BOUND_TARGET.csv",
    "material_charge_ledger": OUT / "P8_Y5_PARENT_QLOC_1935_MATERIAL_CHARGE_LEDGER.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1935_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1935_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1935_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1935_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1935_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_projection": SOURCE_WEIGHT_DOCS / "MTS_WEP_ETA_PROJECTION_CONTRACT_1935_NONCLAIM.csv",
    "microscope_product_bound": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1935_WEP_PRODUCT_BOUND_TARGET_NONCLAIM.csv",
    "material_queue": QUEUE / "JR1935_SOURCE_WEIGHT_UNIVERSALITY_OR_MATERIAL_CHARGE_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1935_CLAIM_GATE.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_key, source_path in SOURCES.items():
        path_exists = source_path.exists()
        source_text = read_text(source_path) if path_exists else ""
        missing_needles = [needle for needle in NEEDLES[source_key] if needle not in source_text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": source_key,
                "source_path": str(source_path),
                "needed_for": "1935 MTS WEP eta projection map or material charge ledger",
                "needles": ";".join(NEEDLES[source_key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path_exists and not missing_needles else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing_needles),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def eta_projection_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "ETA1935_0_definition",
            "statement": "For two test bodies A,B, eta_AB=2(a_A-a_B)/(a_A+a_B).",
            "derivation_status": "DEFINITION",
            "formula": "eta_AB = 2(a_A-a_B)/(a_A+a_B)",
            "use": "common observable used by MICROSCOPE",
            "remaining_debt": "none for observable definition",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "ETA1935_1_residual_projection_exact",
            "statement": "If a_A=a_GR(1+epsilon_A) and a_B=a_GR(1+epsilon_B), then eta_AB=2(epsilon_A-epsilon_B)/(2+epsilon_A+epsilon_B).",
            "derivation_status": "EXACT_ALGEBRAIC_PROJECTION",
            "formula": "eta_AB = 2(epsilon_A-epsilon_B)/(2+epsilon_A+epsilon_B)",
            "use": "maps any MTS differential acceleration residual to MICROSCOPE eta",
            "remaining_debt": "derive epsilon_A and epsilon_B from MTS source-weight variables",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "ETA1935_2_linear_limit",
            "statement": "For |epsilon_A|,|epsilon_B| << 1, eta_AB = epsilon_A-epsilon_B + O(epsilon^2).",
            "derivation_status": "CONTROLLED_LINEAR_LIMIT",
            "formula": "eta_AB ~= epsilon_A - epsilon_B",
            "use": "turns the MICROSCOPE bound into a first product target",
            "remaining_debt": "small-residual regime must be justified for any numeric MTS row",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "ETA1935_3_universal_part_cancels",
            "statement": "A composition-independent residual epsilon_A=epsilon_B cancels from eta_AB.",
            "derivation_status": "EXACT_CANCELLATION",
            "formula": "epsilon_A=epsilon_B => eta_AB=0",
            "use": "separates measured-G/common-source effects from WEP-violating composition differences",
            "remaining_debt": "prove MTS source coupling is universal or bound the differential part",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "ETA1935_4_mts_source_weight_form",
            "statement": "If epsilon_A=tau_WEP*S_Earth*W_A and epsilon_B=tau_WEP*S_Earth*W_B, then eta_TiPt=2*tau_WEP*S_Earth*DeltaW/(2+tau_WEP*S_Earth*SigmaW).",
            "derivation_status": "CONDITIONAL_MTS_PROJECTION_CONTRACT",
            "formula": "eta_TiPt = 2 P DeltaW/(2+P SigmaW), P=tau_WEP*S_Earth",
            "use": "names the missing product needed for an MTS WEP smoke test",
            "remaining_debt": "W_A, W_B, tau_WEP, S_Earth, and arena conventions are not yet derived",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def mts_projection_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "CON1935_0_acceleration_residual_owner",
            "object": "epsilon_A = delta a_A/a_GR",
            "required_definition": "MTS must define the fractional acceleration residual for each material body in the MICROSCOPE arena.",
            "current_status": "SYMBOLIC_ONLY",
            "claim_blocker": "no MTS equation yet maps source-weight residuals to acceleration residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "CON1935_1_material_weight_difference",
            "object": "DeltaW_TiPt = W_Ti - W_Pt",
            "required_definition": "Define MTS material/source-weight charges for Ti alloy and Pt alloy, including composition convention.",
            "current_status": "MISSING_MATERIAL_CHARGES",
            "claim_blocker": "cannot evaluate eta_pred without material charges",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "CON1935_2_universal_weight_sum",
            "object": "SigmaW_TiPt = W_Ti + W_Pt",
            "required_definition": "Define denominator correction for the exact projection, or prove small-residual regime.",
            "current_status": "MISSING_DENOMINATOR_CONTROL",
            "claim_blocker": "linear eta ~= P DeltaW requires |P SigmaW| << 2",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "CON1935_3_transfer_factor",
            "object": "P_WEP = tau_WEP*S_Earth",
            "required_definition": "Derive or source the WEP transfer factor from MTS source field and Earth/orbit arena.",
            "current_status": "MISSING_TAU_WEP_AND_SOURCE_ENVIRONMENT",
            "claim_blocker": "cannot convert material weight difference into an acceleration residual",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "CON1935_4_acceptance_rule",
            "object": "abs(eta_pred) <= eta_bound_abs",
            "required_definition": f"Use eta_bound_abs={ETA_BOUND_ABS:.3e} unless a stricter confidence convention is selected.",
            "current_status": "BOUND_READY_PROJECTION_BLOCKED",
            "claim_blocker": "bound exists but eta_pred is not numeric",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def product_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "product_id": "PB1935_0_linear_WEP_product_target",
            "product_symbol": "P_WEP*DeltaW_TiPt",
            "linear_formula": "eta_TiPt ~= P_WEP*DeltaW_TiPt",
            "bound_abs": ETA_BOUND_ABS,
            "bound_units": "dimensionless",
            "source_bound_id": "WEP1934_0_MICROSCOPE_TiPt_eta",
            "validity_conditions": "|epsilon_Ti|,|epsilon_Pt| << 1; denominator correction negligible; source/environment convention fixed",
            "numeric_prediction_available": False,
            "comparison_status": "BOUND_READY_MTS_PRODUCT_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "product_id": "PB1935_1_exact_WEP_product_contract",
            "product_symbol": "P_WEP, DeltaW_TiPt, SigmaW_TiPt",
            "linear_formula": "eta_TiPt = 2 P_WEP DeltaW_TiPt/(2+P_WEP SigmaW_TiPt)",
            "bound_abs": ETA_BOUND_ABS,
            "bound_units": "dimensionless",
            "source_bound_id": "WEP1934_0_MICROSCOPE_TiPt_eta",
            "validity_conditions": "denominator nonzero; all symbols sourced/derived; sign convention fixed",
            "numeric_prediction_available": False,
            "comparison_status": "EXACT_SCHEMA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def material_charge_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("MAT1935_0_Ti_alloy", "Titanium alloy test mass", "W_Ti", "MISSING_MTS_MATERIAL_CHARGE"),
        ("MAT1935_1_Pt_alloy", "Platinum alloy test mass", "W_Pt", "MISSING_MTS_MATERIAL_CHARGE"),
        ("MAT1935_2_DeltaW", "composition-difference charge", "DeltaW_TiPt=W_Ti-W_Pt", "MISSING_DIFFERENCE_CHARGE"),
        ("MAT1935_3_SigmaW", "denominator/sum charge", "SigmaW_TiPt=W_Ti+W_Pt", "MISSING_SUM_CHARGE"),
        ("MAT1935_4_Earth_source", "Earth/source environment", "S_Earth or equivalent MTS source profile", "MISSING_SOURCE_ENVIRONMENT"),
        ("MAT1935_5_tau_WEP", "WEP transfer normalization", "tau_WEP", "MISSING_TRANSFER_NORMALIZATION"),
        ("MAT1935_6_universality_theorem", "GR/Newton-compatible source universality", "DeltaW_AB=0 for ordinary matter, or bounded finite residual", "MISSING_SOURCE_UNIVERSALITY_THEOREM"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "material_id": material_id,
            "object": obj,
            "symbol_or_relation": symbol,
            "status": status,
            "needed_for": "numeric eta_TiPt prediction and WEP/source coupling gate",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for material_id, obj, symbol, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1935_0_eta_projection_algebra", "Eötvös eta projection from acceleration residuals is derived", "PASS_NONCLAIM", "exact algebraic projection recorded"),
        ("CG1935_1_mts_acceleration_residual", "MTS defines epsilon_A for MICROSCOPE bodies", "FAIL_BLOCKED", "MTS acceleration residual owner missing"),
        ("CG1935_2_material_charges", "Ti/Pt MTS material charges are derived or sourced", "FAIL_BLOCKED", "W_Ti and W_Pt missing"),
        ("CG1935_3_tau_source_environment", "tau_WEP and Earth/source environment are fixed", "FAIL_BLOCKED", "transfer factor P_WEP missing"),
        ("CG1935_4_numeric_WEP_comparison", "numeric eta_pred can be compared to MICROSCOPE", "FAIL_BLOCKED", "product target exists but inputs are symbolic"),
        ("CG1935_5_local_GR_Newton", "local GR/Newton source coupling is derived", "FAIL_BLOCKED", "requires source universality theorem or bounded finite residuals"),
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
            "decision_id": "DEC1935_0_projection_status",
            "decision": "ETA_PROJECTION_ALGEBRA_DERIVED_NONCLAIM",
            "rationale": "The Eötvös map from acceleration residuals to eta is exact and can host future MTS predictions.",
            "next_action": "derive or source the material/source-weight residuals entering epsilon_A",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1935_1_best_next_route",
            "decision": "SOURCE_UNIVERSALITY_OR_MATERIAL_CHARGE_NEXT",
            "rationale": "For GR/Newton reduction, the clean win is a source universality theorem; fallback is finite Ti/Pt material charges.",
            "next_action": "try to prove DeltaW_AB=0 for ordinary matter from Hilbert/source coupling, otherwise build material charge rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1935_0_primary",
            "selection_status": "selected",
            "target_doc": "1936-Y5-R2FR-source-weight-universality-theorem-or-TiPt-material-charge-ledger.md",
            "target_script": "scripts/Y5_R2FR_source_weight_universality_or_TiPt_material_charge_ledger_1936.py",
            "objective": "derive source-weight universality for ordinary matter, DeltaW_AB=0, from the parent/Hilbert source coupling; if unsigned, build Ti/Pt material-charge requirements for the MICROSCOPE eta projection",
            "success_condition": "a source universality theorem sufficient to kill WEP composition residuals, or a nonclaim Ti/Pt material-charge ledger with MTS eta comparison still blocked",
            "do_not": "do not absorb composition dependence into measured G, set tau_WEP=1, invent W_Ti/W_Pt, claim WEP pass, claim local GR, or modify formalization-workbench",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1935_0_project_position",
            "status": "WEP_PROJECTION_MAP_DERIVED_SYMBOLICALLY",
            "summary": "1935 turns the MICROSCOPE bound into an exact symbolic MTS comparison contract.",
            "strongest_result": "eta_AB=2(epsilon_A-epsilon_B)/(2+epsilon_A+epsilon_B), and eta_TiPt=2 P DeltaW/(2+P SigmaW) under the MTS source-weight ansatz",
            "missing_piece": "derive epsilon_A from MTS source coupling, including W_Ti, W_Pt, tau_WEP, and Earth/source profile",
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
    write_csv(BRANCH_COPIES["source_weight_projection"], rows_by_name["mts_projection_contract"])
    write_csv(BRANCH_COPIES["microscope_product_bound"], rows_by_name["product_bound"])
    write_csv(BRANCH_COPIES["material_queue"], rows_by_name["material_charge_ledger"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for artifact in FORMALIZATION.rglob("*1935*") if artifact.is_file())


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

    add("VAL1935_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"]), "all local source paths exist and needles found")
    add("VAL1935_01_eta_theorem", any(row["derivation_status"] == "EXACT_ALGEBRAIC_PROJECTION" for row in rows_by_name["eta_projection_theorem"]) and any(row["derivation_status"] == "CONDITIONAL_MTS_PROJECTION_CONTRACT" for row in rows_by_name["eta_projection_theorem"]), "exact eta projection and conditional MTS projection recorded")
    add("VAL1935_02_contract", len(rows_by_name["mts_projection_contract"]) == 5 and all("claim_blocker" in row for row in rows_by_name["mts_projection_contract"]), "projection contract names all blockers")
    add("VAL1935_03_product_bound", len(rows_by_name["product_bound"]) == 2 and all(float(row["bound_abs"]) > 0 for row in rows_by_name["product_bound"]), "linear and exact product target rows have positive dimensionless bound")
    add("VAL1935_04_material_ledger", len(rows_by_name["material_charge_ledger"]) == 7 and all(str(row["status"]).startswith("MISSING_") for row in rows_by_name["material_charge_ledger"]), "material/source/tau/universality blockers recorded")
    add("VAL1935_05_claim_gates", any(row["status"] == "PASS_NONCLAIM" for row in rows_by_name["claim_gate"]) and all(str(row["claim_allowed"]) == "False" for row in rows_by_name["claim_gate"]), "only algebra gate passes as nonclaim; all claim flags false")
    add("VAL1935_06_decision", any(row["decision"] == "SOURCE_UNIVERSALITY_OR_MATERIAL_CHARGE_NEXT" for row in rows_by_name["decision"]), "source universality/material charge selected next")
    add("VAL1935_07_next_target", rows_by_name["next_target"][0]["target_doc"].startswith("1936-Y5-R2FR-source-weight-universality"), "1936 source universality target selected")
    add("VAL1935_08_claim_flags_safe", all(str(row.get("valid_for_claim")) == "False" and str(row.get("claim_allowed")) == "False" for rows in rows_by_name.values() for row in rows), "claim flags all false")

    csv_ok = True
    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        try:
            csv_ok = csv_ok and bool(parse_csv(output_path))
        except Exception:
            csv_ok = False
    add("VAL1935_09_csv_parse", csv_ok, "all generated CSVs parse with rows")
    add("VAL1935_10_branch_copies", all(path.exists() and bool(parse_csv(path)) for path in BRANCH_COPIES.values()), "; ".join(str(path) for path in BRANCH_COPIES.values()))
    add("VAL1935_11_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent")
    formalization_count = formalization_artifact_count()
    add("VAL1935_12_formalization_untouched", formalization_count == 0, f"formalization_1935_artifact_count={formalization_count}")

    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        {
            "validation_id": "VAL1935_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "1935 MTS WEP eta projection map or material charge ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1935 Y5 R2FR: MTS WEP Eta Projection Map or Material Charge Ledger",
        "",
        "## Verdict",
        "",
        "1935 derives the exact algebraic bridge from an MTS fractional acceleration residual to the MICROSCOPE Eötvös observable. This is a real improvement: the WEP row is no longer just a bound ledger; it now has a symbolic comparison contract.",
        "",
        "The important formula is `eta_AB = 2(epsilon_A-epsilon_B)/(2+epsilon_A+epsilon_B)`. Under the provisional MTS source-weight form `epsilon_A=P_WEP W_A`, this becomes `eta_TiPt = 2 P_WEP DeltaW_TiPt/(2+P_WEP SigmaW_TiPt)`. The formula is derived; the MTS material charges and transfer factor are not.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Eta Projection Theorem",
        "",
        markdown_table(rows_by_name["eta_projection_theorem"]),
        "",
        "## MTS Projection Contract",
        "",
        markdown_table(rows_by_name["mts_projection_contract"]),
        "",
        "## Product Bound Target",
        "",
        markdown_table(rows_by_name["product_bound"]),
        "",
        "## Material Charge Ledger",
        "",
        markdown_table(rows_by_name["material_charge_ledger"]),
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
        "source_register": source_register_rows(),
        "eta_projection_theorem": eta_projection_theorem_rows(),
        "mts_projection_contract": mts_projection_contract_rows(),
        "product_bound": product_bound_rows(),
        "material_charge_ledger": material_charge_ledger_rows(),
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
