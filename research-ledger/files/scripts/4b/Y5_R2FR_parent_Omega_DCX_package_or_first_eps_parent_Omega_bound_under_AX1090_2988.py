from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICRO_COEFF = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2988"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2988-Y5-R2FR-parent-Omega-DCX-package-or-first-eps-parent-Omega-bound-under-AX1090.md"

SRC_2987_DOC = ROOT / "2987-Y5-R2FR-parent-generator-transformation-law-or-first-epsilon-VWEP-component-bound-under-AX1090.md"
SRC_2987_LAW = RESIDUALS / "P8_Y5_R2FR_2987_PARENT_GENERATOR_LAW_ATTEMPT.csv"
SRC_2987_EPS = RESIDUALS / "P8_Y5_R2FR_2987_EPS_V_GENERATOR_COMPONENT_BOUND_NONCLAIM.csv"
SRC_2987_NEXT = RESIDUALS / "P8_Y5_R2FR_2987_NEXT_TARGET.csv"
SRC_2671_CERT = RESIDUALS / "P8_Y5_R2FR_VERTICAL_FIRST_CLASS_2671_CERTIFICATE_AUDIT.csv"
SRC_2671_OMEGA = RESIDUALS / "P8_Y5_R2FR_VERTICAL_FIRST_CLASS_2671_OMEGA_BRIDGE_AUDIT.csv"
SRC_2590_CONTRACT = RESIDUALS / "P8_Y5_VERTICAL_QV_2590_EXTRACTION_CONTRACT.csv"
SRC_2590_KERNEL = RESIDUALS / "P8_Y5_VERTICAL_QV_2590_KERNEL_CHARGE_ROWS.csv"
SRC_2590_SECTOR = RESIDUALS / "P8_Y5_VERTICAL_QV_2590_SECTOR_PIECE_LEDGER.csv"
SRC_2902_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2902_VERTICAL_QV_EXTRACTION_CONTRACT.csv"
SRC_2902_KERNEL = RESIDUALS / "P8_Y5_R2FR_2902_VERTICAL_QV_KERNEL_CHARGE_ROWS.csv"
SRC_2903_SECTOR = RESIDUALS / "P8_Y5_R2FR_2903_VERTICAL_SECTOR_VARIATION_LEDGER.csv"
SRC_591_OMEGA = RESIDUALS / "P8_Y5_R10_591_PARENT_OMEGA_CANDIDATE.csv"
SRC_591_DC = RESIDUALS / "P8_Y5_R10_591_DC_OPERATOR_FORMULA.csv"
SRC_591_DCDAGGER = RESIDUALS / "P8_Y5_R10_591_DCDAGGER_FORMULA.csv"
SRC_591_CMP = RESIDUALS / "P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv"
SRC_2668_GATE = RESIDUALS / "P8_Y5_R10_LX_THETA_OMEGA_OWNER_2668_OWNER_GATE.csv"
SRC_2668_AUDIT = RESIDUALS / "P8_Y5_R10_LX_THETA_OMEGA_OWNER_2668_OWNER_PROOF_AUDIT.csv"
SRC_2668_TEMPLATE = RESIDUALS / "P8_Y5_R10_LX_THETA_OMEGA_OWNER_2668_OMEGA_COMPONENT_TEMPLATE_NONCLAIM.csv"
SRC_1038 = RESIDUALS / "P8_Y5_R10_1038_OMEGA_DCX_CLOSURE_AUDIT.csv"
SRC_2108 = RESIDUALS / "P8_Y5_PARENT_QLOC_2108_OMEGA_DCX_EXECUTION_GATE.csv"
SRC_2867 = RESIDUALS / "P8_Y5_R2FR_2867_DCDAGGER_OMEGA_GATE.csv"
SRC_2952 = RESIDUALS / "P8_Y5_R2FR_2952_VERTICAL_GENERATOR_AUDIT.csv"

LIVE_C_PARENT = MICRO_COEFF / "C_parent_WEP_slot_import.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2988_SOURCE_REGISTER.csv",
    "package": RESIDUALS / "P8_Y5_R2FR_2988_PARENT_OMEGA_DCX_PACKAGE_AUDIT.csv",
    "execution": RESIDUALS / "P8_Y5_R2FR_2988_OMEGA_DCX_EXECUTION_MATRIX.csv",
    "epsilon": RESIDUALS / "P8_Y5_R2FR_2988_FIRST_EPS_PARENT_OMEGA_DCX_BOUND_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2988_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2988_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2988_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2988_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2988_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "package_copy": PARENT_ACTION / "parent_Omega_DCX_package_2988_NOT_SIGNED.csv",
    "epsilon_copy": LOCAL_BOUNDS / "eps_parent_Omega_DCX_bound_2988_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2988_parent_Lagrangian_Theta_or_epsilon_theta_next_NONCLAIM.csv",
}

for directory in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def add(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, out_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in out_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2988_00_2987_doc", SRC_2987_DOC, ["NEXT2987_0_2988", "Theta/Omega"], "2987 handoff"),
        ("SRC2988_01_2987_law", SRC_2987_LAW, ["LAW2987_2_raise_index", "NOT_PARENT_SIGNED_STAGE_EPS_V_GENERATOR_BOUND"], "parent generator law verdict"),
        ("SRC2988_02_2987_eps", SRC_2987_EPS, ["EVG2987_02_omega", "eps_DCX_operator"], "eps_v_generator component split"),
        ("SRC2988_03_2987_next", SRC_2987_NEXT, ["NEXT2987_0_2988", "eps_parent_Omega"], "selected 2988 target"),
        ("SRC2988_04_2671_cert", SRC_2671_CERT, ["VFC2671_1_parent_symplectic_package", "MISSING_PARENT_OMEGA"], "vertical first-class certificate"),
        ("SRC2988_05_2671_omega", SRC_2671_OMEGA, ["OMB2671_3_verdict", "OMEGA_BRIDGE_NOT_CLAIM_READY"], "Omega bridge audit"),
        ("SRC2988_06_2590_contract", SRC_2590_CONTRACT, ["VQC2590_7_verdict", "QV_EXTRACTION_CONTRACT_READY_PARENT_UNSIGNED"], "vertical Qv extraction contract"),
        ("SRC2988_07_2590_kernel", SRC_2590_KERNEL, ["VQL2590_0_kernel_charge", "MISSING_THETA_PARENT"], "kernel charge leakage rows"),
        ("SRC2988_08_2590_sector", SRC_2590_SECTOR, ["QVP2590_6_total", "TOTAL_NOT_PROMOTED"], "sector Qv piece ledger"),
        ("SRC2988_09_2902_contract", SRC_2902_CONTRACT, ["VQC2902_7_verdict", "FAIL_CURRENT_MTS_QV_NOT_EXTRACTED"], "updated vertical Qv extraction contract"),
        ("SRC2988_10_2902_kernel", SRC_2902_KERNEL, ["VQL2902_TOTAL", "COMPONENTS_MISSING"], "updated kernel charge rows"),
        ("SRC2988_11_2903_sector", SRC_2903_SECTOR, ["VSL2903_6_total", "TOTAL_NOT_PROMOTED"], "updated sector variation ledger"),
        ("SRC2988_12_591_omega", SRC_591_OMEGA, ["OM591_4_reduced_Omega", "not_constructed"], "parent Omega candidate"),
        ("SRC2988_13_591_dc", SRC_591_DC, ["DC591_4_boundary_pairing", "edge_risk_explicit"], "DC operator formula"),
        ("SRC2988_14_591_dcdagger", SRC_591_DCDAGGER, ["DCA591_4_compare_to_Omega_flat", "not_closed_without_parent_PJ_and_Omega"], "DCdagger formula"),
        ("SRC2988_15_591_cmp", SRC_591_CMP, ["CMP591_5_verdict", "formula_progress_but_no_certificate"], "Omega/DCdagger comparison"),
        ("SRC2988_16_2668_gate", SRC_2668_GATE, ["LOG2668_7_verdict", "LX_THETA_OMEGA_OWNER_NOT_CLAIM_READY"], "L_X/Theta/Omega owner gate"),
        ("SRC2988_17_2668_audit", SRC_2668_AUDIT, ["LTO2668_8_verdict", "LX_THETA_OMEGA_OWNER_NOT_PARENT_DERIVED"], "L_X owner proof audit"),
        ("SRC2988_18_2668_template", SRC_2668_TEMPLATE, ["OMG2668_5_absolute_envelope", "NOT_COMPUTED_COMPONENTS_MISSING"], "Omega component template"),
        ("SRC2988_19_1038", SRC_1038, ["ODC1038_8_verdict", "FAIL_CURRENT_CLAIM_NO_POLE_NOT_CLOSED"], "Omega/DCX closure audit"),
        ("SRC2988_20_2108", SRC_2108, ["OEX2108_7_verdict", "FAIL_CURRENT_CLAIM"], "Omega/DCX execution gate"),
        ("SRC2988_21_2867", SRC_2867, ["DCO2867_6_verdict", "FAIL_CURRENT_CLAIM"], "DCdagger/Omega gate"),
        ("SRC2988_22_2952", SRC_2952, ["VNP2952_11_verdict", "VERTICAL_FIRST_CLASS_NOPOLE_NOT_DERIVED"], "vertical generator audit"),
    ]
    return [
        add(
            {
                "source_id": source_id,
                "source_path": str(path),
                "role": role,
                "required_anchors": ";".join(needles),
                "exists": path.exists(),
                "anchors_found": anchors(path, needles),
            }
        )
        for source_id, path, needles, role in specs
    ]


def package_rows() -> list[dict[str, Any]]:
    data = [
        (
            "PKG2988_0_parent_L",
            "parent Lagrangian density",
            "L_parent on the full local branch field set, before quotient, readout, source masks or boundary fitting.",
            "MISSING_TOTAL_PARENT_ACTION",
            "without L_parent, Theta_parent and C_X are notation",
            "eps_parent_L",
        ),
        (
            "PKG2988_1_Theta",
            "parent symplectic potential",
            "delta L_parent = E_A delta Phi^A + dTheta_parent(Phi;delta Phi).",
            "MISSING_THETA_PARENT",
            "no full-sector Theta exists for geometry, extra, projector, matter/source and boundary pieces together",
            "eps_parent_Theta",
        ),
        (
            "PKG2988_2_Omega",
            "parent symplectic two-form",
            "Omega_parent = delta Theta_parent on the declared parent field domain.",
            "MISSING_PARENT_OMEGA",
            "Omega cannot raise DCdagger into v_X until it is explicit and closed on the branch",
            "eps_parent_Omega",
        ),
        (
            "PKG2988_3_CX",
            "parent X constraint/source operator",
            "C_X^nu[Phi] is parent-owned, with tensor/density convention and fixed domain.",
            "MISSING_CX_OPERATOR",
            "C_X=-nabla P+J_eff remains a formula template, not an owned parent operator",
            "eps_CX_operator",
        ),
        (
            "PKG2988_4_DCX",
            "linearized operator DC_X",
            "DC_X maps parent field variations into the X constraint covector with boundary pairing declared.",
            "MISSING_DCX_OPERATOR",
            "adjoint depends on density convention, parent P/J dependence and boundary pairing",
            "eps_DCX_operator",
        ),
        (
            "PKG2988_5_QX_boundary",
            "boundary charge and differentiability",
            "delta Q_X cancels the DC boundary covector and Q_X is zero, exact, proper or source-bounded on compact local branch.",
            "MISSING_QX_BOUNDARY_PAIRING",
            "edge/source charge can survive if B_DC is not cancelled",
            "eps_QX_boundary",
        ),
        (
            "PKG2988_6_inverse_domain",
            "reduced Omega inverse",
            "Omega_parent has a reduced inverse after ordinary gauge quotient and no-stabilizer proof.",
            "REDUCED_OMEGA_INVERSE_MISSING",
            "DCdagger remains a covector, not the generator",
            "eps_raise_index",
        ),
        (
            "PKG2988_7_sector_total",
            "sector-complete sum",
            "EH, boundary, extra motion/time, projector/source-measure, matter/source and constraint pieces close in one branch.",
            "TOTAL_SECTOR_PACKAGE_NOT_PROMOTED",
            "EH reference alone cannot stand in for total MTS parent action",
            "eps_sector_total",
        ),
        (
            "PKG2988_8_verdict",
            "parent Omega/DCX package",
            "PKG2988_0 through PKG2988_7 are signed together.",
            "NOT_PARENT_SIGNED_STAGE_EPS_PARENT_OMEGA_DCX",
            "package is exact as a derivation route but not executable for current MTS",
            "eps_parent_Omega_DCX_abs",
        ),
    ]
    return [
        add(
            {
                "package_id": package_id,
                "object": obj,
                "required_statement": statement,
                "current_status": status,
                "blocking_gap": gap,
                "fallback_symbol": fallback,
                "parent_signed": False,
                "theorem_zero_adopted": False,
            }
        )
        for package_id, obj, statement, status, gap, fallback in data
    ]


def execution_rows() -> list[dict[str, Any]]:
    data = [
        (
            "EXE2988_0_variation_identity",
            "delta L = E delta Phi + dTheta",
            "required before any Noether/Hamiltonian generator can be extracted",
            "BLOCKED_MISSING_PARENT_L_AND_THETA",
        ),
        (
            "EXE2988_1_omega_flat",
            "Omega_flat(v_X) = (DC_X)^dagger epsilon",
            "field-by-field equality must hold for every retained parent field",
            "NOT_COMPARABLE_WITHOUT_OMEGA_AND_DCX",
        ),
        (
            "EXE2988_2_raise_index",
            "v_X = Omega^{-1}[(DC_X)^dagger epsilon]",
            "reduced inverse, gauge quotient, domain and stabilizer theorem required",
            "REDUCED_INVERSE_NOT_AVAILABLE",
        ),
        (
            "EXE2988_3_boundary",
            "delta G_X = Omega(delta Phi,v_X) with boundary cancellation",
            "delta Q_X must cancel B_DC and local Q_X/K_boundary must be zero/proper/exact or bounded",
            "BOUNDARY_DIFFERENTIABILITY_NOT_CLOSED",
        ),
        (
            "EXE2988_4_sector_charge",
            "Theta_parent and Q_v are sum of sector pieces",
            "each sector piece needs theorem-zero, fixed convention or source-backed bound",
            "SECTOR_TOTAL_COMPONENTS_MISSING",
        ),
        (
            "EXE2988_5_no_claim",
            "execute generator certificate for local GR",
            "requires all execution rows to pass in one branch",
            "FAIL_CURRENT_MTS_DO_NOT_PROMOTE",
        ),
    ]
    return [
        add(
            {
                "execution_id": execution_id,
                "test": test,
                "why_needed": why,
                "current_status": status,
                "execution_passed": False,
            }
        )
        for execution_id, test, why, status in data
    ]


def epsilon_rows() -> list[dict[str, Any]]:
    data = [
        (
            "EOD2988_00_definition",
            "eps_parent_Omega_DCX_abs",
            "absolute envelope for missing parent Omega/DCX package",
            "eps_parent_Omega_DCX_abs <= sum(EOD2988_01..10); no cancellation, no readout deletion",
            "mixed_symplectic_covector_norm",
            "package not parent-signed",
            "PKG2988_8_verdict",
        ),
        ("EOD2988_01_L", "eps_parent_L", "missing total parent Lagrangian", "bounds failure of total action density before variation", "action_density_norm", "L_parent not sourced", "VQC2902_0_parent_variation"),
        ("EOD2988_02_Theta", "eps_parent_Theta", "missing symplectic potential", "bounds missing Theta_parent contribution in delta L", "symplectic_potential_norm", "Theta_parent absent across sectors", "VQL2902_1_theta_piece"),
        ("EOD2988_03_Omega", "eps_parent_Omega", "missing symplectic two-form", "bounds missing Omega=delta Theta closure/inverse input", "symplectic_two_form_norm", "Omega_parent missing", "EVG2987_02_omega"),
        ("EOD2988_04_CX", "eps_CX_operator", "missing parent C_X operator", "bounds unowned constraint/source operator C_X", "constraint_covector_norm", "C_X formula not owned", "DC591_0_constraint_definition"),
        ("EOD2988_05_DCX", "eps_DCX_operator", "missing linearized DC_X and adjoint", "bounds missing DC_X, DCdagger and boundary pairing", "covector_operator_norm", "DC_X not parent-owned", "EVG2987_03_DCX"),
        ("EOD2988_06_PJ", "eps_PJ_owner", "P/J momentum-source ownership gap", "bounds mismatch between P,J in DC_X and Theta/Omega momenta", "momentum_source_norm", "P and J not derived from same parent Noether current", "CMP591_1_current_MTS_P_owner;CMP591_2_current_MTS_J_owner"),
        ("EOD2988_07_boundary", "eps_QX_boundary", "boundary differentiability and Q_X gap", "bounds uncancelled B_DC, Q_X and K_boundary", "boundary_charge_norm", "delta Q_X cancellation and zero/proper charge not shown", "DCA591_3_boundary_adjoint"),
        ("EOD2988_08_inverse", "eps_raise_index", "Omega inverse/reduced-domain gap", "bounds covector-to-vector raising error", "operator_norm", "reduced Omega inverse missing", "OMB2671_1_inverse_rule"),
        ("EOD2988_09_sector", "eps_sector_total", "sector-complete Theta/Qv/Cv gap", "bounds missing non-EH and constraint sector pieces", "sector_charge_norm", "sector total not promoted", "QVP2902_6_total"),
        ("EOD2988_10_integrability", "eps_Hv_integrability", "Hamiltonian integrability/curl gap", "bounds field-space curl of the surface Hamiltonian variation", "dimensionless_curl_norm", "field-space curl and surface class not tested", "VQL2902_5_integrability"),
        ("EOD2988_11_total", "eps_parent_Omega_DCX_total", "first source-ready Omega/DCX total", "absolute no-cancellation total of all EOD2988 heads", "mixed_declared_by_projection", "no component has numeric/theorem-zero status", "EOD2988_00_definition"),
    ]
    return [
        add(
            {
                "epsilon_id": eps_id,
                "symbol": symbol,
                "definition": definition,
                "bound_interface": formula,
                "units": units,
                "current_value": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "lower_bound": "0",
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "source_anchor": anchor,
                "why_nonclaim": why,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "source_ready_template": True,
                "no_cancellation_policy": True,
            }
        )
        for eps_id, symbol, definition, formula, units, why, anchor in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE2988_0_L_parent", "total parent Lagrangian exists", False, "MISSING_TOTAL_PARENT_ACTION"),
        ("GATE2988_1_Theta", "Theta_parent derived from delta L_parent", False, "MISSING_THETA_PARENT"),
        ("GATE2988_2_Omega", "Omega_parent=delta Theta_parent on full branch", False, "MISSING_PARENT_OMEGA"),
        ("GATE2988_3_CX_DCX", "C_X and DC_X extracted with fixed convention", False, "MISSING_CX_DCX_OPERATOR"),
        ("GATE2988_4_boundary", "Q_X cancels boundary pairing and local charge is zero/proper/exact/bounded", False, "MISSING_QX_BOUNDARY"),
        ("GATE2988_5_inverse", "reduced Omega inverse and no-stabilizer theorem exist", False, "REDUCED_OMEGA_INVERSE_MISSING"),
        ("GATE2988_6_sector_total", "all sector Theta/Qv/Cv pieces close in one branch", False, "SECTOR_TOTAL_NOT_PROMOTED"),
        ("GATE2988_7_promote", "promote parent Omega/DCX package", False, "all previous gates must pass"),
    ]
    return [
        add(
            {
                "gate_id": gate_id,
                "promotion_gate": gate,
                "condition_passed": passed,
                "status": status,
                "promotion_allowed_now": False,
            }
        )
        for gate_id, gate, passed, status in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "decision_id": "DEC2988_0_route_confirmed",
                "decision": "The parent Omega/DCX route is the right route, but still not executable.",
                "because": "the covector-to-generator map is category-correct only after L_parent, Theta, Omega, C_X, DC_X, Q_X and reduced inverse are all owned.",
                "next_action": "stop trying to promote V_WEP until the parent variation identity is filled.",
            }
        ),
        add(
            {
                "decision_id": "DEC2988_1_nonclaim_bound",
                "decision": "Stage eps_parent_Omega_DCX_abs as the first package-level leakage envelope.",
                "because": "every critical subobject is either missing or only a formal template, so an honest bound ledger is better than closure language.",
                "next_action": "source or derive the first component, starting with L_parent/Theta sector extraction.",
            }
        ),
        add(
            {
                "decision_id": "DEC2988_2_next",
                "decision": "Next target is parent Lagrangian/Theta sector extraction or first epsilon_theta_piece row.",
                "because": "Theta_parent is the first domino; Omega and Q_v cannot be real until delta L_parent is sector-complete.",
                "next_action": "build 2989 around L_parent sector split and Theta_piece source rows.",
            }
        ),
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "next_id": "NEXT2988_0_2989",
                "priority": "selected_primary",
                "next_doc": "2989-Y5-R2FR-parent-Lagrangian-Theta-sector-extraction-or-first-epsilon-theta-piece-bound-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_parent_Lagrangian_Theta_sector_extraction_or_first_epsilon_theta_piece_bound_under_AX1090_2989.py",
                "objective": "Try to derive a sector-complete parent variation identity delta L_parent=E delta Phi+dTheta_parent; if not, create source-ready epsilon_theta_piece rows for EH, boundary, extra, projector/source-measure, matter/source and constraint sectors.",
                "include": "L_parent sector split;Theta_EH;Theta_boundary;Theta_extra;Theta_projector;Theta_matter_source;constraint C_v;M_ref normalization;epsilon_theta_piece_missing",
                "exclude": "C_parent import;Omega promotion;V_WEP promotion;local-GR claim;theorem-zero promotion;GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [add({"copy_id": key, "path": str(path), "exists": path.exists()}) for key, path in BRANCH_OUTPUTS.items()]


def validation(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    csv_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
    generated = [*csv_paths, DOC]
    formal_count = sum(1 for path in FORMALIZATION.rglob("*2988*") if path.is_file()) if FORMALIZATION.exists() else 0
    package_not_signed = any(row["package_id"] == "PKG2988_8_verdict" and row["current_status"] == "NOT_PARENT_SIGNED_STAGE_EPS_PARENT_OMEGA_DCX" for row in all_rows["package"])
    execution_blocked = any(row["execution_id"] == "EXE2988_5_no_claim" and row["current_status"] == "FAIL_CURRENT_MTS_DO_NOT_PROMOTE" for row in all_rows["execution"])
    epsilon_nonclaim = all(
        row["current_value"] == "MISSING_SOURCE_BACKED_UPPER_BOUND"
        and not row["finite_value_present"]
        and row["source_ready_template"]
        and not row["valid_for_claim"]
        for row in all_rows["epsilon"]
    )
    checks = [
        ("VAL2988_0_sources_exist", all(row["exists"] for row in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2988_1_anchors_found", all(row["anchors_found"] for row in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2988_2_package_not_signed", package_not_signed, "parent Omega/DCX package not signed", True),
        ("VAL2988_3_execution_blocked", execution_blocked, "Omega/DCX execution matrix blocks promotion", True),
        ("VAL2988_4_eps_source_ready_nonclaim", epsilon_nonclaim, "eps_parent_Omega_DCX rows source-ready but nonclaim", True),
        ("VAL2988_5_gates_blocked", all(not row["condition_passed"] and not row["promotion_allowed_now"] for row in all_rows["gates"]), "all promotion gates blocked", True),
        ("VAL2988_6_no_live_cparent", not LIVE_C_PARENT.exists(), "C_parent_WEP_slot_import.csv not created or promoted", True),
        ("VAL2988_7_next_written", any(row["next_id"] == "NEXT2988_0_2989" for row in all_rows["next"]), "2989 next target written", True),
        ("VAL2988_8_branches_exist", all(row["exists"] for row in all_rows["branches"]), "branch copies exist", True),
        ("VAL2988_9_csvs_parse", all(csv_ok(path) for path in csv_paths), "all generated CSVs parse", True),
        ("VAL2988_10_outputs_under_post", all(under(path, ROOT) for path in generated), "all generated outputs under post-checkpoint-work", True),
        ("VAL2988_11_formalization_clean", formal_count == 0, f"no 2988 outputs in formalization-workbench (count={formal_count})", True),
        ("VAL2988_12_doc_written", DOC.exists(), "2988 markdown checkpoint exists", True),
    ]
    out_rows = [add({"validation_id": check_id, "passed": bool(passed), "check": check, "required": required}) for check_id, passed, check, required in checks]
    out_rows.append(add({"validation_id": "VAL2988_OVERALL", "passed": all(row["passed"] for row in out_rows), "check": "2988 validation overall", "required": True}))
    return out_rows


def esc(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(out_rows: list[dict[str, Any]], cols: list[str]) -> str:
    if not out_rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(cols) + " |",
            "| " + " | ".join("---" for _ in cols) + " |",
            *["| " + " | ".join(esc(row.get(col, "")) for col in cols) + " |" for row in out_rows],
        ]
    )


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    outputs = [{"output": key, "path": str(path), "exists": path.exists()} for key, path in OUTPUTS.items() if key != "validation"]
    branches = [{"copy": key, "path": str(path), "exists": path.exists()} for key, path in BRANCH_OUTPUTS.items()]
    DOC.write_text(
        f"""# 2988 - Parent Omega/DCX Package or First eps_parent_Omega Bound

Status: `Y5_R2FR_2988_parent_Omega_DCX_route_exact_but_not_executable_eps_parent_Omega_DCX_bound_staged_nonclaim`

Claim ceiling: `no_parent_Omega_DCX_package_no_parent_generator_promotion_no_VWEP_promotion_no_Cparent_DERIVED_ZERO_no_Cparent_import_no_local_GR_no_Newton_no_WEP_no_R10_no_PPN_no_clock_no_orbital_no_public_claim`

## Summary

- The mathematical road is now nailed down: `delta L_parent=E delta Phi+dTheta_parent`, `Omega_parent=delta Theta_parent`, `C_X/DC_X` from the same parent action, and `v_X=Omega_parent^-1[(DC_X)^dagger epsilon]`.
- The current corpus still lacks the sector-complete parent `L`, `Theta`, `Omega`, `C_X`, `DC_X`, `Q_X` boundary pairing and reduced inverse.
- Therefore the generator cannot be promoted; `DCdagger` remains a covector bookkeeping object until the parent symplectic package exists.
- This checkpoint stages `eps_parent_Omega_DCX_abs` as an explicit no-cancellation package bound, with the first concrete subrows ready for sourcing.

## Generated Outputs

{table(outputs, ["output", "path", "exists"])}

## Branch Copies

{table(branches, ["copy", "path", "exists"])}

## Parent Omega/DCX Package Audit

{table(all_rows["package"], ["package_id", "object", "current_status", "blocking_gap", "fallback_symbol"])}

## Omega/DCX Execution Matrix

{table(all_rows["execution"], ["execution_id", "test", "current_status", "why_needed", "execution_passed"])}

## First eps_parent_Omega/DCX Bound Rows

{table(all_rows["epsilon"], ["epsilon_id", "symbol", "definition", "bound_interface", "current_value", "why_nonclaim"])}

## Promotion Gates

{table(all_rows["gates"], ["gate_id", "promotion_gate", "condition_passed", "status", "promotion_allowed_now"])}

## Decision Ledger

{table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Validation

{table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
""",
        encoding="utf-8",
    )


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(),
        "package": package_rows(),
        "execution": execution_rows(),
        "epsilon": epsilon_rows(),
        "gates": gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])
    shutil.copyfile(OUTPUTS["package"], BRANCH_OUTPUTS["package_copy"])
    shutil.copyfile(OUTPUTS["epsilon"], BRANCH_OUTPUTS["epsilon_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    print(f"2988 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
