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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1831"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
P4_RUN = ROOT / "runs" / "20260602-141500-metric-compatibility-Levi-Civita-or-R11-connection-row" / "results"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1831-Y5-R2FR-parent-field-inventory-certificate-or-first-P4-numeric-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1831_0_1830_next",
        "source_key": "1830_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1830_NEXT_TARGET.csv",
        "needles": ["NEXT1830_0_primary", "selected"],
        "role": "1830 selects parent field-inventory certificate or first P4 numeric row.",
    },
    {
        "source_id": "SRC1831_1_1830_validation",
        "source_key": "1830_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1830_VALIDATION.csv",
        "needles": ["VAL1830_OVERALL", "PASS"],
        "role": "confirms 1830 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1831_2_1830_grammar",
        "source_key": "1830_grammar",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1830_NO_INDEPENDENT_CONNECTION_GRAMMAR_ATTEMPT.csv",
        "needles": ["NIC1830_6_verdict", "NO_INDEPENDENT_CONNECTION_GRAMMAR_NOT_PROVEN"],
        "role": "prior grammar attempt did not prove no independent connection.",
    },
    {
        "source_id": "SRC1831_3_1830_P4_contract",
        "source_key": "1830_P4_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1830_P4_ROW_FILL_CONTRACT.csv",
        "needles": ["P4F1830_0_combined_TQ", "MISSING_COEFFICIENTS_AND_MAPS"],
        "role": "first executable P4 row is torsion/nonmetricity combined and remains unfilled.",
    },
    {
        "source_id": "SRC1831_4_1829_metric_lemma",
        "source_key": "1829_metric_only_lemma",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1829_METRIC_ONLY_CONNECTION_THEOREM_ATTEMPT.csv",
        "needles": ["MOC1829_1_exact_lemma", "MOC1829_6_verdict"],
        "role": "exact metric-only Levi-Civita lemma exists, but premise is not parent-signed.",
    },
    {
        "source_id": "SRC1831_5_P4_gate",
        "source_key": "P4_gate_tests",
        "source_path": P4_RUN / "P4_gate_tests.csv",
        "needles": ["independent_connection_absence_gate", "fail_open"],
        "role": "P4 gate shows independent connection absence remains fail-open.",
    },
    {
        "source_id": "SRC1831_6_P4_demotions",
        "source_key": "P4_demotions",
        "source_path": P4_RUN / "connection_operator_demotions.csv",
        "needles": ["torsion_nonmetricity_combined", "not_forbidden"],
        "role": "operator families to retain if no parent inventory certificate closes.",
    },
    {
        "source_id": "SRC1831_7_1542_qdef",
        "source_key": "1542_q_definition",
        "source_path": ROOT / "1542-Y5-q-definition-or-Dqvm-coupling-coefficient-source-pack.md",
        "needles": ["QDEF1542_1_minimal_visible_candidate", "CANDIDATE_ONLY"],
        "role": "q_loc visible geometry candidate includes omega_obs but remains candidate-only.",
    },
    {
        "source_id": "SRC1831_8_1045_matter",
        "source_key": "1045_matter_functor",
        "source_path": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
        "needles": ["MFS1045_2_matter_bundle_functor", "QG1045_2_connection_stack"],
        "role": "matter functor conditionally uses omega[e_obs] but leaves independent connection caveat.",
    },
    {
        "source_id": "SRC1831_9_1155_coframe",
        "source_key": "1155_geometry_stack",
        "source_path": ROOT / "1155-Y5-R10-single-observed-coframe-source-frame-owner-or-frame-residual-row.md",
        "needles": ["COF1155_3_geometry_stack", "NOT_PARENT_SIGNED"],
        "role": "single geometry stack descent is still not parent-signed.",
    },
    {
        "source_id": "SRC1831_10_512_symbols",
        "source_key": "512_symbol_map",
        "source_path": ROOT / "512-match-MTS-symbols-to-local-GR-action-blocks.md",
        "needles": ["Gamma_eff", "no_symbol_fully_promotes_local_GR"],
        "role": "Gamma_eff/K_hat/q_loc residual remains hard local-GR obstruction.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1831_SOURCE_REGISTER.csv",
    "field_inventory": RESIDUALS / "P8_Y5_PARENT_QLOC_1831_FIELD_INVENTORY_CERTIFICATE_ATTEMPT.csv",
    "P4_first_row": RESIDUALS / "P8_Y5_PARENT_QLOC_1831_P4_FIRST_ROW_ACQUISITION_LEDGER.csv",
    "P4_map_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1831_P4_WEAK_FIELD_MAP_CONTRACT.csv",
    "anti_smuggling_guard": RESIDUALS / "P8_Y5_PARENT_QLOC_1831_ANTI_SMUGGLING_GUARD.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1831_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1831_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1831_VALIDATION.csv",
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


def field_inventory_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "inventory_id": "FIC1831_0_conditional_theorem",
            "certificate_clause": "metric/coframe-only parent theorem",
            "mathematical_test": "configuration variables are e_obs or g_obs plus matter; omega/Gamma is only omega[e_obs]",
            "current_evidence": "MOC1829_1_exact_lemma",
            "status": "EXACT_CONDITIONAL_LEMMA_ONLY",
            "blocker": "parent field inventory is not signed for MTS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "inventory_id": "FIC1831_1_visible_q_inventory",
            "certificate_clause": "q_loc owns visible geometry before local tests",
            "mathematical_test": "q_loc(Phi) contains e_obs, g_obs, omega_obs, theta_vis and no hidden post-readout connection deletion",
            "current_evidence": "QDEF1542_1_minimal_visible_candidate",
            "status": "CANDIDATE_ONLY",
            "blocker": "q_loc is not a parent-signed quotient with field-by-field derivative",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "inventory_id": "FIC1831_2_connection_slot_absence",
            "certificate_clause": "no independent Gamma/omega slot",
            "mathematical_test": "parent action and source/readout grammar never vary an independent connection",
            "current_evidence": "P4 independent_connection_absence_gate fail_open",
            "status": "NOT_CERTIFIED",
            "blocker": "no source derives connection Euler equation or excludes independent connection variable",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "inventory_id": "FIC1831_3_omega_derivative_only",
            "certificate_clause": "omega_obs is derivative-only in all sectors",
            "mathematical_test": "all matter, light, spin, clock, source and readout sectors use omega[e_obs] only",
            "current_evidence": "MFS1045_2 and QG1045_2",
            "status": "CONDITIONAL_CONNECTION_CAVEAT",
            "blocker": "matter functor is not parent-constructed and independent connection requires its own row",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "inventory_id": "FIC1831_4_no_hypermomentum",
            "certificate_clause": "no independent connection charge",
            "mathematical_test": "delta S_matter / delta Gamma vanishes except through omega[e_obs]",
            "current_evidence": "P4 hypermomentum demotion row",
            "status": "FAIL_OPEN",
            "blocker": "spin, source and readout hypermomentum channels remain legal",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "inventory_id": "FIC1831_5_single_geometry_stack",
            "certificate_clause": "measure/coframe/connection/derivative stack descends together",
            "mathematical_test": "mu, e, g, omega and D are functions of the same q(Phi) or owned exact/gauge data",
            "current_evidence": "COF1155_3_geometry_stack",
            "status": "NOT_PARENT_SIGNED",
            "blocker": "connection force can re-enter local source current",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "inventory_id": "FIC1831_6_residual_symbol_reconciliation",
            "certificate_clause": "Gamma_eff/K_hat/q_loc reconciled with inventory",
            "mathematical_test": "Gamma_eff and K_hat are metric/coframe/boundary functionals or q_loc/P4 residuals",
            "current_evidence": "512 Gamma_eff/K_hat/q_loc map",
            "status": "RESIDUAL_BRANCH_RETAINED",
            "blocker": "q_loc Ward residual is not action-varied to zero",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "inventory_id": "FIC1831_7_certificate_verdict",
            "certificate_clause": "parent field-inventory certificate",
            "mathematical_test": "FIC1831_1 through FIC1831_6 all close in one parent grammar",
            "current_evidence": "all 1831 field-inventory rows",
            "status": "PARENT_FIELD_INVENTORY_CERTIFICATE_NOT_PROVEN",
            "blocker": "independent connection, hypermomentum and geometry-stack descent are still unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def P4_first_row_rows() -> list[dict[str, Any]]:
    source_path = P4_RUN / "connection_operator_demotions.csv"
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4N1831_0_combined_TQ",
            "parent_contract_row": "P4F1830_0_combined_TQ",
            "operator_family": "torsion_nonmetricity_combined",
            "operator_form": "c_T T^2 + c_Q Q^2 + c_TQ<T,Q> + matter connection couplings",
            "coefficient_value": "MISSING_PARENT_COEFFICIENT",
            "units": "MISSING_UNITS",
            "operator_normalization": "MISSING_NORMALIZATION",
            "weak_field_map": "MISSING_TQ_TO_PPN_WEP_CLOCK_MAP",
            "observable_links": "R0;R1;R2;R11;PPN;WEP;clock;orbital;R10",
            "source_path": str(source_path),
            "source_exists": source_path.exists(),
            "provenance_status": "SOURCE_IDENTIFIES_OPERATOR_NOT_COEFFICIENT",
            "numeric_fill_status": "NOT_FILLED_NO_PARENT_NUMERIC_SOURCE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4N1831_1_axial_spin_hold",
            "parent_contract_row": "P4F1830_1_axial_spin",
            "operator_family": "axial_torsion_spin_coupling",
            "operator_form": "S_mu psi_bar gamma^mu gamma5 psi or equivalent spin-torsion coupling",
            "coefficient_value": "MISSING_SPIN_TORSION_SOURCE",
            "units": "MISSING_UNITS",
            "operator_normalization": "MISSING_NORMALIZATION",
            "weak_field_map": "MISSING_SPIN_LIGHT_CLOCK_MAP",
            "observable_links": "WEP;clock;spin;light;PPN",
            "source_path": str(source_path),
            "source_exists": source_path.exists(),
            "provenance_status": "SOURCE_IDENTIFIES_OPERATOR_NOT_COEFFICIENT",
            "numeric_fill_status": "HELD_AFTER_COMBINED_TQ",
            "valid_for_claim": False,
        },
    ]


def P4_map_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "map_id": "P4M1831_0_parent_variation",
            "required_input": "parent variation with independent connection retained or theorem-zeroed",
            "required_output": "Euler equation for T, Q, projective residue and hypermomentum",
            "current_status": "MISSING_PARENT_VARIATION",
            "acceptance_gate": "no Levi-Civita import; derive T=Q=0 or keep coefficients",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "P4M1831_1_operator_normalization",
            "required_input": "chosen norm and index conventions for T^lambda_mu_nu and Q_lambda_mu_nu",
            "required_output": "dimensioned c_T, c_Q, c_TQ rows",
            "current_status": "MISSING_NORMALIZATION",
            "acceptance_gate": "units and signs are explicit before comparing to bounds",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "P4M1831_2_weak_field_projection",
            "required_input": "linearized metric/coframe plus torsion/nonmetricity perturbations",
            "required_output": "PPN/WEP/clock/lightcone residual vector",
            "current_status": "MISSING_WEAK_FIELD_MAP",
            "acceptance_gate": "observable channels are not selected after seeing data",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "P4M1831_3_bounds",
            "required_input": "R10, PPN, clock, orbital and WEP source-backed bounds in compatible units",
            "required_output": "abs(predicted residual) <= bound for each arena",
            "current_status": "MISSING_BOUND_PROJECTION",
            "acceptance_gate": "branch cannot claim pass while coefficient or bound rows contain missing markers",
            "valid_for_claim": False,
        },
    ]


def anti_smuggling_guard_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "guard_id": "ASG1831_0_no_EH_shortcut",
            "guard": "do not import EH/Levi-Civita as the parent proof",
            "reason": "that would assume the GR reduction branch being tested",
            "status": "ACTIVE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "ASG1831_1_no_hidden_Gamma_delete",
            "guard": "do not delete Gamma/omega after a local test fails",
            "reason": "field inventory must be declared by the parent action before readout",
            "status": "ACTIVE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "ASG1831_2_no_zero_by_silence",
            "guard": "do not set torsion, nonmetricity, projective residue or hypermomentum to zero by omission",
            "reason": "all four are live escape routes unless theorem-zero or source-bounded",
            "status": "ACTIVE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "ASG1831_3_no_numeric_placeholder",
            "guard": "do not use placeholder coefficients as first P4 numeric rows",
            "reason": "a numeric row must have units, normalization, source path and weak-field map",
            "status": "ACTIVE",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1831_0_certificate_result",
            "decision": "PARENT_FIELD_INVENTORY_CERTIFICATE_NOT_PROVEN",
            "reason": "visible q/e/omega language exists, but independent connection absence, hypermomentum silence and geometry-stack descent are not parent-signed",
            "next_action": "do not claim Levi-Civita compatibility or local GR",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1831_1_first_P4_row_result",
            "decision": "FIRST_P4_NUMERIC_ROW_NOT_FILLED",
            "reason": "the corpus identifies torsion/nonmetricity as the first row, but gives no parent coefficient, units, normalization or weak-field projection",
            "next_action": "hunt either theorem-zero T=Q=0 from parent connection variation or source first c_T/c_Q/c_TQ row",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1831_2_best_next",
            "decision": "P4_TQ_ZERO_THEOREM_OR_COEFFICIENT_SOURCE_HUNT_NEXT",
            "reason": "this is now the least handwavy route: prove torsion/nonmetricity never exist, or make their residual vector empirical",
            "next_action": "1832-Y5-R2FR-torsion-nonmetricity-zero-theorem-or-first-coefficient-source-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1831_0_primary",
            "next_target": "1832-Y5-R2FR-torsion-nonmetricity-zero-theorem-or-first-coefficient-source-row.md",
            "script": "scripts/Y5_R2FR_torsion_nonmetricity_zero_theorem_or_first_coefficient_source_row.py",
            "objective": "try to prove T=Q=0 from the parent connection variation; if not, source the first c_T/c_Q/c_TQ coefficient row with units and weak-field map",
            "selection_status": "selected",
            "success_condition": "theorem-zero for torsion/nonmetricity is parent-signed, or first coefficient row remains nonclaim but source-ready",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1831_1_secondary",
            "next_target": "1832b-Y5-R2FR-hypermomentum-spin-source-row.md",
            "script": "scripts/Y5_R2FR_hypermomentum_spin_source_row.py",
            "objective": "separately source or theorem-zero the spin/hypermomentum escape route",
            "selection_status": "held_secondary",
            "success_condition": "spin/hypermomentum channel has either a parent no-Gamma theorem or a residual row",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "field_inventory": field_inventory_rows(),
        "P4_first_row": P4_first_row_rows(),
        "P4_map_contract": P4_map_contract_rows(),
        "anti_smuggling_guard": anti_smuggling_guard_rows(),
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


def P4_missing_rows_nonclaim(rows: list[dict[str, Any]]) -> bool:
    for row in rows:
        has_missing_marker = any("MISSING_" in str(value) for value in row.values())
        if has_missing_marker and str(row["valid_for_claim"]).lower() == "true":
            return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        name = path.name
        if "1831-Y5-R2FR" in name or name.startswith("P8_Y5_PARENT_QLOC_1831") or name.startswith("P8_Y5_BRR545_1831"):
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
        ("VAL1831_0_sources_exist", all(str(row["exists"]).lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL1831_1_needles_present", all(str(row["needles_present"]).lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL1831_2_conditional_theorem_preserved",
            any(row["inventory_id"] == "FIC1831_0_conditional_theorem" and row["status"] == "EXACT_CONDITIONAL_LEMMA_ONLY" for row in rows_map["field_inventory"]),
            "exact metric/coframe-only theorem is preserved as conditional only",
        ),
        (
            "VAL1831_3_certificate_not_promoted",
            any(row["inventory_id"] == "FIC1831_7_certificate_verdict" and row["status"] == "PARENT_FIELD_INVENTORY_CERTIFICATE_NOT_PROVEN" for row in rows_map["field_inventory"]),
            "parent field-inventory certificate is not promoted",
        ),
        (
            "VAL1831_4_first_P4_row_staged",
            any(row["row_id"] == "P4N1831_0_combined_TQ" and row["numeric_fill_status"] == "NOT_FILLED_NO_PARENT_NUMERIC_SOURCE" for row in rows_map["P4_first_row"]),
            "first P4 torsion/nonmetricity row is staged but not numerically filled",
        ),
        (
            "VAL1831_5_missing_rows_nonclaim",
            P4_missing_rows_nonclaim(rows_map["P4_first_row"]) and P4_missing_rows_nonclaim(rows_map["P4_map_contract"]),
            "rows with missing markers remain valid_for_claim=false",
        ),
        (
            "VAL1831_6_P4_map_contract_written",
            any(row["map_id"] == "P4M1831_2_weak_field_projection" for row in rows_map["P4_map_contract"]),
            "P4 weak-field map contract is written",
        ),
        (
            "VAL1831_7_guards_active",
            all(row["status"] == "ACTIVE" and row["valid_for_claim"] is False for row in rows_map["anti_smuggling_guard"]),
            "anti-smuggling guards are active",
        ),
        (
            "VAL1831_8_decision_next",
            any(row["decision_id"] == "DEC1831_2_best_next" and row["decision"] == "P4_TQ_ZERO_THEOREM_OR_COEFFICIENT_SOURCE_HUNT_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects torsion/nonmetricity zero theorem or first coefficient source row next",
        ),
        (
            "VAL1831_9_next_selected",
            any(row["route_id"] == "NEXT1831_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1831_10_no_claim_flags", no_claim_flags(rows_map), "no generated claim flags are true"),
        ("VAL1831_11_csv_parse", csv_parse_ok(output_paths), "all generated 1831 CSVs parse"),
        ("VAL1831_12_branch_copies", branch_copies_exist(copied_paths), "branch/quarantine/queue copies exist"),
        ("VAL1831_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1831_14_formalization_untouched", no_formalization_outputs(), "no 1831 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1831_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1831 parent field-inventory certificate or first P4 numeric row checkpoint",
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
            "# 1831 Y5 R2FR parent field-inventory certificate or first P4 numeric row",
            "",
            "**Progress:** 1831 tries the cleanest GR-reduction route one more time: certify that the parent field inventory has no independent connection/hypermomentum slot. The exact conditional theorem is real, but the certificate still does not close for the present corpus.",
            "",
            "**Current verdict:** no Levi-Civita/local-GR claim yet. The corpus contains candidate visible geometry and conditional `omega[e_obs]` language, but it does not prove independent connection absence, no hypermomentum, or single geometry-stack descent. The first P4 row is identified as torsion/nonmetricity combined, but it cannot be numerically filled without parent coefficients, units, normalization, and weak-field projection.",
            "",
            "**Claim ceiling:** no P4 pass, no `c2` score, no local GR/Newton promotion, no placeholder numeric row, no GitHub action, and no `formalization-workbench` edit is allowed from 1831.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Parent Field-Inventory Certificate Attempt",
            markdown_table(rows_map["field_inventory"], ["inventory_id", "certificate_clause", "mathematical_test", "current_evidence", "status", "blocker", "claim_allowed", "valid_for_claim"]),
            "",
            "## First P4 Row Acquisition Ledger",
            markdown_table(rows_map["P4_first_row"], ["row_id", "parent_contract_row", "operator_family", "operator_form", "coefficient_value", "units", "operator_normalization", "weak_field_map", "observable_links", "source_path", "source_exists", "provenance_status", "numeric_fill_status", "valid_for_claim"]),
            "",
            "## P4 Weak-Field Map Contract",
            markdown_table(rows_map["P4_map_contract"], ["map_id", "required_input", "required_output", "current_status", "acceptance_gate", "valid_for_claim"]),
            "",
            "## Anti-Smuggling Guard",
            markdown_table(rows_map["anti_smuggling_guard"], ["guard_id", "guard", "reason", "status", "valid_for_claim"]),
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
            "This is not a dead end; it is the branch becoming honest. If MTS can prove the parent has only metric/coframe geometry, GR compatibility drops out cleanly. If not, the theory must carry a P4 residual vector and beat local tests by sourced coefficients. The next pressure point is therefore torsion/nonmetricity: either derive `T=Q=0` from the parent variation, or make `c_T,c_Q,c_TQ` real rows with units and observable maps.",
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
    print(f"1831 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
