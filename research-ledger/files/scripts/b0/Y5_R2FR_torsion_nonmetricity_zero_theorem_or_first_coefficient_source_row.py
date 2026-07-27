from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1832"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
P4_RUN = ROOT / "runs" / "20260602-141500-metric-compatibility-Levi-Civita-or-R11-connection-row" / "results"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1832-Y5-R2FR-torsion-nonmetricity-zero-theorem-or-first-coefficient-source-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1832_0_1831_next",
        "source_key": "1831_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1831_NEXT_TARGET.csv",
        "needles": ["NEXT1831_0_primary", "selected"],
        "role": "1831 selects torsion/nonmetricity zero theorem or first coefficient source row.",
    },
    {
        "source_id": "SRC1832_1_1831_validation",
        "source_key": "1831_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1831_VALIDATION.csv",
        "needles": ["VAL1831_OVERALL", "PASS"],
        "role": "confirms 1831 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1832_2_1831_inventory",
        "source_key": "1831_field_inventory",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1831_FIELD_INVENTORY_CERTIFICATE_ATTEMPT.csv",
        "needles": ["FIC1831_7_certificate_verdict", "PARENT_FIELD_INVENTORY_CERTIFICATE_NOT_PROVEN"],
        "role": "parent field-inventory certificate did not close.",
    },
    {
        "source_id": "SRC1832_3_1831_P4_row",
        "source_key": "1831_first_P4_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1831_P4_FIRST_ROW_ACQUISITION_LEDGER.csv",
        "needles": ["P4N1831_0_combined_TQ", "NOT_FILLED_NO_PARENT_NUMERIC_SOURCE"],
        "role": "torsion/nonmetricity combined row is identified but not numerically sourced.",
    },
    {
        "source_id": "SRC1832_4_P4_routes",
        "source_key": "P4_compatibility_routes",
        "source_path": P4_RUN / "compatibility_theorem_routes.csv",
        "needles": ["P4_R3_metric_affine_zero_Q_zero_T_theorem", "not_supplied"],
        "role": "P4 route audit already names the metric-affine T/Q zero theorem gap.",
    },
    {
        "source_id": "SRC1832_5_P4_gates",
        "source_key": "P4_gate_results",
        "source_path": P4_RUN / "gate_results.csv",
        "needles": ["torsion_zero_derived", "nonmetricity_zero_derived"],
        "role": "P4 gates record torsion and nonmetricity zero failures.",
    },
    {
        "source_id": "SRC1832_6_P4_templates",
        "source_key": "P4_R11_templates",
        "source_path": P4_RUN / "P4_R11_template_rows.csv",
        "needles": ["torsion_nonmetricity_combined", "fill_numeric_or_zero"],
        "role": "template schema for first coefficient rows.",
    },
    {
        "source_id": "SRC1832_7_P4_demotions",
        "source_key": "P4_demotions",
        "source_path": P4_RUN / "connection_operator_demotions.csv",
        "needles": ["torsion_nonmetricity_combined", "fill P4 R11 combined connection row"],
        "role": "operator family and theorem-zero condition for combined T/Q row.",
    },
    {
        "source_id": "SRC1832_8_1561_ansatz",
        "source_key": "1561_minimal_parent_ansatz",
        "source_path": ROOT / "1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
        "needles": ["ANS1561_A_EH_lambdaR_silent", "NOT_ADOPTED_CURRENT_MTS_DERIVATION"],
        "role": "EH-style repair ansatz exists but is not current MTS parent action.",
    },
    {
        "source_id": "SRC1832_9_1045_matter",
        "source_key": "1045_connection_stack",
        "source_path": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
        "needles": ["QG1045_2_connection_stack", "CONDITIONAL_CONNECTION_CAVEAT"],
        "role": "matter connection independence is conditional, not parent-signed.",
    },
    {
        "source_id": "SRC1832_10_512_symbols",
        "source_key": "512_symbol_map",
        "source_path": ROOT / "512-match-MTS-symbols-to-local-GR-action-blocks.md",
        "needles": ["q_loc^nu", "plateau_axiom_forbidden"],
        "role": "local residual cannot be removed by an inserted plateau axiom.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1832_SOURCE_REGISTER.csv",
    "TQ_zero_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1832_TQ_ZERO_THEOREM_ATTEMPT.csv",
    "route_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1832_PALATINI_METRIC_AFFINE_ROUTE_AUDIT.csv",
    "coefficient_source": RESIDUALS / "P8_Y5_PARENT_QLOC_1832_FIRST_COEFFICIENT_SOURCE_ROW.csv",
    "distortion_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1832_DISTORTION_EQUATION_CONTRACT.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1832_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1832_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1832_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing_needles = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and not missing_needles,
                "missing_needles": ";".join(missing_needles),
                "role": source["role"],
            }
        )
    return rows


def TQ_zero_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "TQ1832_0_distortion_identity",
            "claim_piece": "distortion tensor normal form",
            "statement": "Write Gamma^lambda_{mu nu} = {lambda}_{mu nu}[g] + C^lambda_{mu nu}; torsion and nonmetricity are algebraic projections of C.",
            "current_status": "EXACT_KINEMATIC_IDENTITY",
            "blocker": "identity alone does not force C=0",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "TQ1832_1_positive_connection_operator",
            "claim_piece": "metric-affine zero theorem",
            "statement": "If the parent variation gives M_C C = 0 with positive/invertible M_C and no source, boundary, or projective kernel, then C=0 and therefore T=Q=0.",
            "current_status": "EXACT_CONDITIONAL_LEMMA_ONLY",
            "blocker": "MTS parent action has not supplied M_C, positivity, or source silence",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "TQ1832_2_metric_only_route",
            "claim_piece": "metric/coframe-only branch",
            "statement": "If there is no independent C variable, T=Q=0 is kinematic because Gamma is Gamma_LC[g] or omega[e_obs].",
            "current_status": "BLOCKED_BY_1831",
            "blocker": "parent field-inventory certificate is not proven",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "TQ1832_3_Palatini_EH_route",
            "claim_piece": "Palatini EH no-hypermomentum branch",
            "statement": "EH Palatini variation can drive Levi-Civita compatibility up to projective freedom when matter carries no Gamma charge.",
            "current_status": "CONDITIONAL_REPAIR_ROUTE_ONLY",
            "blocker": "EH parent adoption, no-hypermomentum, and projective silence are unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "TQ1832_4_source_term",
            "claim_piece": "hypermomentum/source silence",
            "statement": "A nonzero Delta_matter or source/readout Gamma current makes M_C C = Delta rather than zero.",
            "current_status": "SOURCE_CHANNEL_RETAINED",
            "blocker": "matter, light, spin, source and readout independence from Gamma are not parent-derived",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "TQ1832_5_projective_boundary",
            "claim_piece": "projective and boundary kernel",
            "statement": "Even if the bulk equation kills most of C, projective trace or boundary-supported connection modes must be fixed, gauged, or mapped.",
            "current_status": "KERNEL_NOT_FIXED",
            "blocker": "projective invariance and boundary/source support are not fully parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "TQ1832_6_verdict",
            "claim_piece": "T=Q=0 theorem for current MTS",
            "statement": "TQ1832_1 through TQ1832_5 would have to close in one parent variation.",
            "current_status": "TQ_ZERO_THEOREM_NOT_PROVEN_CURRENT_CORPUS",
            "blocker": "distortion operator, source silence, projective/boundary control and parent action adoption are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def route_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "ROUTE1832_0_metric_only",
            "route": "no independent distortion variable",
            "would_buy": "kinematic Levi-Civita compatibility",
            "current_status": "BLOCKED_BY_FIELD_INVENTORY",
            "missing_input": "parent grammar excluding independent Gamma/omega/C",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "ROUTE1832_1_Palatini",
            "route": "Palatini EH with no hypermomentum",
            "would_buy": "C=0 up to harmless projective mode",
            "current_status": "BLOCKED_BY_OPEN_EH_AND_MATTER_PREMISES",
            "missing_input": "MTS-owned EH block, matter Gamma-independence, projective gauge/readout proof",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "ROUTE1832_2_metric_affine_mass",
            "route": "positive algebraic distortion mass/operator",
            "would_buy": "C=0 dynamically even if C exists in parent fields",
            "current_status": "NOT_SUPPLIED",
            "missing_input": "explicit M_C, sign, kernel, boundary condition and source term",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "ROUTE1832_3_empirical_vector",
            "route": "retain C as P4/R11 residual vector",
            "would_buy": "testable modified-gravity branch rather than theorem-zero GR",
            "current_status": "SCHEMA_READY_NO_NUMERIC_INPUTS",
            "missing_input": "c_T/c_Q/c_TQ values or bounds plus weak-field map",
            "valid_for_claim": False,
        },
    ]


def coefficient_source_rows() -> list[dict[str, Any]]:
    source_path = P4_RUN / "P4_R11_template_rows.csv"
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "COEF1832_0_c_T",
            "coefficient_symbol": "c_T",
            "operator": "T^lambda_{mu nu} T_lambda^{mu nu} plus chosen irreducible torsion decomposition",
            "coefficient_value": "MISSING_PARENT_VALUE_OR_ZERO_THEOREM",
            "coefficient_units": "MISSING_UNITS",
            "normalization": "MISSING_EH_OR_CONNECTION_SCALE_NORMALIZATION",
            "weak_field_map": "MISSING_TORSION_TO_PPN_WEP_CLOCK_MAP",
            "source_file": str(source_path),
            "source_exists": source_path.exists(),
            "derivation_status": "TEMPLATE_ONLY_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "COEF1832_1_c_Q",
            "coefficient_symbol": "c_Q",
            "operator": "Q_lambda_mu_nu Q^lambda_mu_nu plus Weyl/shear split",
            "coefficient_value": "MISSING_PARENT_VALUE_OR_ZERO_THEOREM",
            "coefficient_units": "MISSING_UNITS",
            "normalization": "MISSING_CLOCK_ROD_OR_EH_NORMALIZATION",
            "weak_field_map": "MISSING_NONMETRICITY_TO_CLOCK_LIGHTCONE_MAP",
            "source_file": str(source_path),
            "source_exists": source_path.exists(),
            "derivation_status": "TEMPLATE_ONLY_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "COEF1832_2_c_TQ",
            "coefficient_symbol": "c_TQ",
            "operator": "allowed torsion/nonmetricity mixed contraction after symmetry decomposition",
            "coefficient_value": "MISSING_PARENT_VALUE_OR_ZERO_THEOREM",
            "coefficient_units": "MISSING_UNITS",
            "normalization": "MISSING_OPERATOR_BASIS",
            "weak_field_map": "MISSING_MIXED_OPERATOR_MAP",
            "source_file": str(source_path),
            "source_exists": source_path.exists(),
            "derivation_status": "TEMPLATE_ONLY_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def distortion_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "DC1832_0_variable",
            "needed_object": "C^lambda_{mu nu} = Gamma^lambda_{mu nu} - Gamma_LC^lambda_{mu nu}[g]",
            "must_supply": "whether C is absent, auxiliary, dynamical, gauge/projective, or residual",
            "current_status": "NOT_PARENT_OWNED",
            "next_action": "derive C from parent field inventory or declare P4 residual vector",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "DC1832_1_equation",
            "needed_object": "M_C C = Delta_Gamma + B_boundary + P_projective",
            "must_supply": "M_C, source current Delta_Gamma, boundary term and projective kernel",
            "current_status": "MISSING_EQUATION",
            "next_action": "write parent variation with respect to C/Gamma",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "DC1832_2_zero_gate",
            "needed_object": "C=0 sufficient conditions",
            "must_supply": "M_C invertible/positive, Delta_Gamma=0, B_boundary=0, projective kernel fixed or invisible",
            "current_status": "CONDITIONAL_ONLY",
            "next_action": "prove each clause or keep coefficients",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "DC1832_3_observable_gate",
            "needed_object": "P4 residual vector",
            "must_supply": "projection of C into WEP, PPN, clock, lightcone, orbital and R10 rows",
            "current_status": "MISSING_OBSERVABLE_MAP",
            "next_action": "do not score until weak-field map and units are real",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1832_0_TQ_theorem_result",
            "decision": "TQ_ZERO_THEOREM_NOT_PROVEN_CURRENT_CORPUS",
            "reason": "the exact distortion lemma exists, but the parent does not supply the C-equation, source silence, projective/boundary control, or adopted EH/metric-affine action",
            "next_action": "do not claim Levi-Civita compatibility",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1832_1_coefficient_result",
            "decision": "FIRST_COEFFICIENT_ROW_REMAINS_TEMPLATE_ONLY",
            "reason": "c_T, c_Q and c_TQ have no parent values, units, normalization, or observable maps yet",
            "next_action": "hunt distortion equation owner before trying numeric bounds",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1832_2_best_next",
            "decision": "DISTORTION_EQUATION_OWNER_NEXT",
            "reason": "the cleanest next move is to derive or reject M_C C = Delta_Gamma + boundary + projective at the parent-action level",
            "next_action": "1833-Y5-R2FR-distortion-equation-owner-or-hypermomentum-source-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1832_0_primary",
            "next_target": "1833-Y5-R2FR-distortion-equation-owner-or-hypermomentum-source-row.md",
            "script": "scripts/Y5_R2FR_distortion_equation_owner_or_hypermomentum_source_row.py",
            "objective": "derive the parent distortion equation M_C C = Delta_Gamma + boundary + projective; if not, source the hypermomentum/source row instead",
            "selection_status": "selected",
            "success_condition": "distortion zero theorem is parent-signed, or source/current rows remain explicit nonclaim residuals",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1832_1_secondary",
            "next_target": "1833b-Y5-R2FR-P4-observable-map-skeleton.md",
            "script": "scripts/Y5_R2FR_P4_observable_map_skeleton.py",
            "objective": "build only the observable map skeleton for P4 residuals after the distortion equation owner is known",
            "selection_status": "held_secondary",
            "success_condition": "WEP/PPN/clock/lightcone channels are mapped without placeholder coefficients",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "TQ_zero_attempt": TQ_zero_attempt_rows(),
        "route_audit": route_audit_rows(),
        "coefficient_source": coefficient_source_rows(),
        "distortion_contract": distortion_contract_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_csvs(paths: list[Path]) -> None:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            directory.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, directory / path.name)


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open("r", encoding="utf-8", newline="") as handle:
                list(csv.DictReader(handle))
    except Exception:
        return False
    return True


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    guarded_keys = {"valid_for_claim", "claim_allowed"}
    for rows in rows_map.values():
        for row in rows:
            for guarded_key in guarded_keys.intersection(row):
                if str(row[guarded_key]).lower() == "true":
                    return False
    return True


def missing_rows_nonclaim(rows: list[dict[str, Any]]) -> bool:
    for row in rows:
        if any("MISSING_" in str(value) for value in row.values()) and str(row["valid_for_claim"]).lower() == "true":
            return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        name = path.name
        if "1832-Y5-R2FR" in name or name.startswith("P8_Y5_PARENT_QLOC_1832") or name.startswith("P8_Y5_BRR545_1832"):
            return False
    return True


def branch_copies_exist(paths: list[Path]) -> bool:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            if not (directory / path.name).exists():
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]], copied_paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    output_paths = [OUTPUTS[key] for key in rows_map.keys()]
    checks: list[tuple[str, bool, str]] = [
        ("VAL1832_0_sources_exist", all(str(row["exists"]).lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL1832_1_needles_present", all(str(row["needles_present"]).lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL1832_2_distortion_identity_written",
            any(row["attempt_id"] == "TQ1832_0_distortion_identity" and row["current_status"] == "EXACT_KINEMATIC_IDENTITY" for row in rows_map["TQ_zero_attempt"]),
            "distortion identity is written",
        ),
        (
            "VAL1832_3_TQ_zero_not_promoted",
            any(row["attempt_id"] == "TQ1832_6_verdict" and row["current_status"] == "TQ_ZERO_THEOREM_NOT_PROVEN_CURRENT_CORPUS" for row in rows_map["TQ_zero_attempt"]),
            "T/Q zero theorem is not promoted",
        ),
        (
            "VAL1832_4_routes_nonclaim",
            all(row["valid_for_claim"] is False for row in rows_map["route_audit"]),
            "all route audit rows remain nonclaim",
        ),
        (
            "VAL1832_5_coefficients_template_only",
            all(row["derivation_status"] == "TEMPLATE_ONLY_NONCLAIM" and row["valid_for_claim"] is False for row in rows_map["coefficient_source"]),
            "coefficient rows remain template-only nonclaim",
        ),
        (
            "VAL1832_6_missing_rows_nonclaim",
            missing_rows_nonclaim(rows_map["coefficient_source"]) and missing_rows_nonclaim(rows_map["distortion_contract"]),
            "rows with missing markers remain valid_for_claim=false",
        ),
        (
            "VAL1832_7_distortion_contract_written",
            any(row["contract_id"] == "DC1832_1_equation" and row["current_status"] == "MISSING_EQUATION" for row in rows_map["distortion_contract"]),
            "distortion equation contract is written",
        ),
        (
            "VAL1832_8_decision_next",
            any(row["decision_id"] == "DEC1832_2_best_next" and row["decision"] == "DISTORTION_EQUATION_OWNER_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects distortion equation owner next",
        ),
        (
            "VAL1832_9_next_selected",
            any(row["route_id"] == "NEXT1832_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1832_10_no_claim_flags", no_claim_flags(rows_map), "no generated claim flags are true"),
        ("VAL1832_11_csv_parse", csv_parse_ok(output_paths), "all generated 1832 CSVs parse"),
        ("VAL1832_12_branch_copies", branch_copies_exist(copied_paths), "branch/quarantine/queue copies exist"),
        ("VAL1832_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1832_14_formalization_untouched", no_formalization_outputs(), "no 1832 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1832_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1832 torsion/nonmetricity zero theorem or first coefficient source row checkpoint",
        }
    )
    return rows


def markdown_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1832 Y5 R2FR torsion-nonmetricity zero theorem or first coefficient source row",
            "",
            "**Progress:** 1832 rewrites the connection problem in the cleanest local variable: the distortion tensor `C = Gamma - Gamma_LC[g]`. Torsion and nonmetricity are then algebraic projections of `C`, so the exact target becomes `C=0` rather than a vague Levi-Civita wish.",
            "",
            "**Current verdict:** no `T=Q=0` theorem for current MTS. The conditional lemma is exact: if the parent variation gives an invertible positive `M_C C = 0` with no source, boundary, or projective kernel, then `T=Q=0`. Current MTS does not yet supply `M_C`, source silence, projective/boundary control, or an adopted EH/metric-affine parent action. The first coefficient rows remain template-only and nonclaim.",
            "",
            "**Claim ceiling:** no Levi-Civita compatibility claim, no P4 pass, no coefficient value, no weak-field score, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1832.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Torsion / Nonmetricity Zero Theorem Attempt",
            markdown_table(rows_map["TQ_zero_attempt"], ["attempt_id", "claim_piece", "statement", "current_status", "blocker", "claim_allowed", "valid_for_claim"]),
            "",
            "## Palatini / Metric-Affine Route Audit",
            markdown_table(rows_map["route_audit"], ["route_id", "route", "would_buy", "current_status", "missing_input", "valid_for_claim"]),
            "",
            "## First Coefficient Source Row",
            markdown_table(rows_map["coefficient_source"], ["row_id", "coefficient_symbol", "operator", "coefficient_value", "coefficient_units", "normalization", "weak_field_map", "source_file", "source_exists", "derivation_status", "valid_for_claim"]),
            "",
            "## Distortion Equation Contract",
            markdown_table(rows_map["distortion_contract"], ["contract_id", "needed_object", "must_supply", "current_status", "next_action", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a useful narrowing. The local-GR branch is not dying; it is demanding the missing equation. If MTS can derive the distortion equation and show its source side vanishes, GR compatibility follows in a very respectable way. If not, `C` becomes a residual vector with coefficients and bounds. That is still a field-theory route, but it is no longer a theorem-zero route.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    nonvalidation_paths: list[Path] = []
    for key, rows in rows_map.items():
        path = OUTPUTS[key]
        write_csv(path, rows)
        nonvalidation_paths.append(path)
    copy_csvs(nonvalidation_paths)
    validation_rows = build_validation(rows_map, nonvalidation_paths)
    write_csv(OUTPUTS["validation"], validation_rows)
    copy_csvs([OUTPUTS["validation"]])
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1832 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
