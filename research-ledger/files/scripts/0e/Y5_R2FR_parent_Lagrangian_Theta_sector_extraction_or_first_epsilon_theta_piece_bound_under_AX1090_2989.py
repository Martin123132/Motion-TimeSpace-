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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_COEFF = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2989"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2989-Y5-R2FR-parent-Lagrangian-Theta-sector-extraction-or-first-epsilon-theta-piece-bound-under-AX1090.md"

SRC_2988_DOC = ROOT / "2988-Y5-R2FR-parent-Omega-DCX-package-or-first-eps-parent-Omega-bound-under-AX1090.md"
SRC_2988_NEXT = RESIDUALS / "P8_Y5_R2FR_2988_NEXT_TARGET.csv"
SRC_2988_PACKAGE = RESIDUALS / "P8_Y5_R2FR_2988_PARENT_OMEGA_DCX_PACKAGE_AUDIT.csv"
SRC_2988_EPS = RESIDUALS / "P8_Y5_R2FR_2988_FIRST_EPS_PARENT_OMEGA_DCX_BOUND_NONCLAIM.csv"
SRC_2988_MATRIX = RESIDUALS / "P8_Y5_R2FR_2988_OMEGA_DCX_EXECUTION_MATRIX.csv"
SRC_2903_SECTOR = RESIDUALS / "P8_Y5_R2FR_2903_VERTICAL_SECTOR_VARIATION_LEDGER.csv"
SRC_2903_LEAKS = RESIDUALS / "P8_Y5_R2FR_2903_VERTICAL_SECTOR_QV_PIECE_LEAK_ROWS.csv"
SRC_2902_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2902_VERTICAL_QV_EXTRACTION_CONTRACT.csv"
SRC_2902_KERNEL = RESIDUALS / "P8_Y5_R2FR_2902_VERTICAL_QV_KERNEL_CHARGE_ROWS.csv"
SRC_MIN_BLOCKS = RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"
SRC_RESPONSE_DOUBLET = RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"
SRC_PIM_CONTRACT = RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv"
SRC_NOETHER_CHAIN = RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv"
SRC_2939 = PARENT_ACTION / "Parent_Noether_theta_Qtau_extraction_attempt_2939_NONCLAIM.csv"
SRC_2947_CERT = PARENT_ACTION / "Theta_Qtau_certificate_attempt_2947_NONCLAIM.csv"
SRC_2947_SECTOR = PARENT_ACTION / "Theta_Qtau_sector_charge_matrix_2947_NONCLAIM.csv"
SRC_1009_DOC = ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"
SRC_1760_DOC = ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md"

LIVE_C_PARENT = MICRO_COEFF / "C_parent_WEP_slot_import.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2989_SOURCE_REGISTER.csv",
    "sector_audit": RESIDUALS / "P8_Y5_R2FR_2989_PARENT_LAGRANGIAN_THETA_SECTOR_AUDIT.csv",
    "theta_attempt": RESIDUALS / "P8_Y5_R2FR_2989_THETA_EXTRACTION_ATTEMPT.csv",
    "epsilon": RESIDUALS / "P8_Y5_R2FR_2989_EPSILON_THETA_PIECE_BOUND_ROWS_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2989_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2989_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2989_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2989_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2989_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theta_sector_copy": PARENT_ACTION / "parent_Lagrangian_Theta_sector_extraction_2989_NOT_SIGNED.csv",
    "epsilon_copy": LOCAL_BOUNDS / "epsilon_theta_piece_bound_rows_2989_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2989_sector_Theta_or_epsilon_theta_next_NONCLAIM.csv",
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
        ("SRC2989_00_2988_doc", SRC_2988_DOC, ["Theta_parent", "eps_parent_Omega_DCX_abs"], "2988 narrative handoff"),
        ("SRC2989_01_2988_next", SRC_2988_NEXT, ["NEXT2988_0_2989", "epsilon_theta_piece_missing"], "selected 2989 target"),
        ("SRC2989_02_2988_package", SRC_2988_PACKAGE, ["PKG2988_1_Theta", "MISSING_THETA_PARENT"], "parent package Theta gap"),
        ("SRC2989_03_2988_eps", SRC_2988_EPS, ["EOD2988_02_Theta", "eps_parent_Theta"], "package epsilon Theta row"),
        ("SRC2989_04_2988_matrix", SRC_2988_MATRIX, ["EXE2988_0_variation_identity", "BLOCKED_MISSING_PARENT_L_AND_THETA"], "Omega/DCX execution block"),
        ("SRC2989_05_2903_sector", SRC_2903_SECTOR, ["VSL2903_6_total", "TOTAL_NOT_PROMOTED"], "sector variation ledger"),
        ("SRC2989_06_2903_leaks", SRC_2903_LEAKS, ["VSP2903_TOTAL", "COMPONENTS_MISSING"], "sector leakage rows"),
        ("SRC2989_07_2902_contract", SRC_2902_CONTRACT, ["VQC2902_0_parent_variation", "MISSING_TOTAL_PARENT_ACTION_AND_THETA"], "vertical Qv extraction contract"),
        ("SRC2989_08_2902_kernel", SRC_2902_KERNEL, ["VQL2902_1_theta_piece", "MISSING_SECTOR_THETA_SPLIT"], "theta piece missing row"),
        ("SRC2989_09_min_blocks", SRC_MIN_BLOCKS, ["A511_0_EH_core", "A511_6_metric_readout"], "minimum parent local-GR action blocks"),
        ("SRC2989_10_response_doublet", SRC_RESPONSE_DOUBLET, ["RD516_4_zero_odd_source", "not_derived_hard_block"], "extra response zero-odd-source blocker"),
        ("SRC2989_11_pim_contract", SRC_PIM_CONTRACT, ["PM5_projector_variation_owned", "PM6_flux_closure_requires_Ward_or_Euler"], "projector/source-measure variation owner"),
        ("SRC2989_12_noether_chain", SRC_NOETHER_CHAIN, ["D505_0_local_parent_action_form", "D505_4_zero_premises"], "parent Noether closure chain"),
        ("SRC2989_13_2939", SRC_2939, ["PNE2939_0_master_formula", "PNE2939_6_verdict"], "parent Noether theta/Qtau extraction attempt"),
        ("SRC2989_14_2947_cert", SRC_2947_CERT, ["CERT2947_0_parent_variation", "CERTIFICATE_NOT_DERIVED"], "theta/Qtau certificate attempt"),
        ("SRC2989_15_2947_sector", SRC_2947_SECTOR, ["SEC2947_9_total", "TOTAL_CERTIFICATE_FAILS"], "theta/Qtau sector charge matrix"),
        ("SRC2989_16_1009_doc", SRC_1009_DOC, ["Parent sector contract", "fixed_reference_missing"], "parent current-chain sector contract"),
        ("SRC2989_17_1760_doc", SRC_1760_DOC, ["delta_v S_matter=0", "A_matter"], "matter/worldtube descent contract"),
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


def sector_audit_rows() -> list[dict[str, Any]]:
    data = [
        (
            "TLS2989_0_master_identity",
            "sector-complete parent identity",
            "L_parent = L_EH + L_boundary + L_extra + L_projector/source + L_matter/source + L_constraint",
            "delta L_parent = E_A delta Phi^A + dTheta_parent; Theta_parent=sum_s Theta_s+delta B_ref",
            "EXACT_CONDITIONAL_SHAPE_ONLY",
            "single signed L_parent and sector variations not present together",
            "epsilon_theta_piece_missing",
        ),
        (
            "TLS2989_1_EH",
            "EH/local geometry",
            "S_EH[g_obs;kappa0,Lambda0]",
            "Theta_EH and Q_EH are standard comparator templates only after constant kappa/Lambda and same metric readout are locked",
            "REFERENCE_TEMPLATE_ONLY",
            "EH cannot substitute for non-EH MTS sectors",
            "epsilon_EH_reference_guard",
        ),
        (
            "TLS2989_2_boundary",
            "boundary/reference/improvement",
            "S_GHY + fixed exact/topological B_ref",
            "Theta_boundary=delta B_ref plus corner/improvement convention fixed before readout",
            "MISSING_FIXED_BV_CONVENTION",
            "unfixed boundary improvement can hide or create local charge",
            "epsilon_Bv_ambiguity",
        ),
        (
            "TLS2989_3_extra",
            "extra motion/time/domain/memory",
            "S_extra or response doublet sector",
            "Theta_extra, Q_extra and odd-source silence must be extracted from the same parent block",
            "MISSING_EXTRA_SECTOR_VARIATION_AND_ZERO_ODD_SOURCE",
            "response/doublet positivity and zero odd source are not parent-derived",
            "epsilon_Qv_extra_piece",
        ),
        (
            "TLS2989_4_projector_source_measure",
            "projector/source-measure Pi_M",
            "Pi_M/source-measure parent selector",
            "Theta_projector must include delta Pi_M and source-measure variation terms or prove them harmless",
            "MISSING_PROJECTOR_VARIATION_OWNER",
            "projector algebra alone is not a Ward/Euler closure theorem",
            "epsilon_Qv_projector_piece",
        ),
        (
            "TLS2989_5_matter_source",
            "matter/source/worldtube",
            "S_matter[psi,e_obs(q(Phi))] plus worldtube/source glue",
            "Theta_matter/source vanishes vertically only if matter sees q-only data and hidden source slots are absent",
            "CONDITIONAL_MATTER_DESCENT_NOT_PARENT_SIGNED",
            "legal direct source prefactors/support/worldtube terms remain open",
            "epsilon_Qv_matter_source_piece",
        ),
        (
            "TLS2989_6_constraint_Cv",
            "constraint / C_v total",
            "Euler/Ward/Gauss constraint split across all retained sectors",
            "C_v must be proportional to parent constraints or source-bounded on the same branch",
            "MISSING_COMMON_CONSTRAINT_SPLIT",
            "Noether identity does not by itself set residual current to zero",
            "epsilon_Cv_constraint_missing",
        ),
        (
            "TLS2989_7_Mref",
            "same-frame normalization",
            "M_ref=H_tau-H_ref or equivalent positive charge denominator",
            "all theta-piece residuals require a positive same-frame denominator before scoring",
            "MISSING_POSITIVE_SAME_FRAME_MREF",
            "finite leakage cannot be compared without denominator and surface class",
            "epsilon_Mref_normalization",
        ),
        (
            "TLS2989_8_total",
            "Theta_parent total",
            "sum of all retained local-branch sectors",
            "Theta_parent is promoted only if TLS2989_1..7 are signed together",
            "TOTAL_THETA_NOT_PARENT_SIGNED",
            "sector-complete theta extraction fails in current corpus",
            "epsilon_theta_piece_total_abs",
        ),
    ]
    return [
        add(
            {
                "sector_id": sector_id,
                "sector": sector,
                "candidate_action_block": block,
                "theta_requirement": requirement,
                "current_status": status,
                "blocking_gap": gap,
                "fallback_symbol": symbol,
                "sector_signed": status in {"EXACT_SIGNED"},
                "theta_promotable": False,
            }
        )
        for sector_id, sector, block, requirement, status, gap, symbol in data
    ]


def theta_attempt_rows() -> list[dict[str, Any]]:
    data = [
        (
            "THX2989_0_variation_identity",
            "derive delta L_parent=E delta Phi+dTheta_parent",
            "possible as an exact formal identity for a declared finite-order L_parent",
            "BLOCKED_MISSING_TOTAL_PARENT_ACTION",
            "current work has candidate blocks, not one adopted sector-complete parent Lagrangian",
            False,
        ),
        (
            "THX2989_1_EH_anchor",
            "use EH theta as local comparator",
            "valid only as the GR comparator/reference limit",
            "REFERENCE_ONLY_NOT_TOTAL_MTS_THETA",
            "non-EH extra/projector/matter/source/boundary sectors are not silent",
            False,
        ),
        (
            "THX2989_2_additivity",
            "Theta_parent=sum_s Theta_s+delta B_ref",
            "exact if all sector L_s and B_ref conventions are owned",
            "CONDITIONAL_ADDITIVITY_NOT_EXECUTABLE",
            "Theta_s missing for extra, projector/source-measure, matter/source, constraint and boundary pieces",
            False,
        ),
        (
            "THX2989_3_vertical_insertion",
            "insert local vertical v_X into Theta_parent",
            "i_v Theta_parent supplies the theta part of the kernel Hamiltonian residual",
            "BLOCKED_VX_AND_THETA_UNSIGNED",
            "v_X is not parent-signed and Theta_parent is not sector-complete",
            False,
        ),
        (
            "THX2989_4_surface_residual",
            "form epsilon_theta_piece_missing",
            "abs(int_S i_v Theta_missing)/M_ref",
            "SOURCE_READY_NONCLAIM_INTERFACE",
            "ready for bounded rows but no numeric/theorem-zero source exists",
            False,
        ),
        (
            "THX2989_5_verdict",
            "current Theta_parent extraction",
            "promote only after every sector Theta piece and M_ref are signed in one branch",
            "THETA_PARENT_NOT_DERIVED_STAGE_EPSILON_THETA_PIECE",
            "use explicit epsilon_theta_piece rows rather than local-GR language",
            False,
        ),
    ]
    return [
        add(
            {
                "attempt_id": attempt_id,
                "target": target,
                "exact_statement": statement,
                "current_status": status,
                "blocking_gap": gap,
                "derivation_passed": passed,
            }
        )
        for attempt_id, target, statement, status, gap, passed in data
    ]


def epsilon_rows() -> list[dict[str, Any]]:
    data = [
        (
            "ETH2989_00_definition",
            "epsilon_theta_piece_missing",
            "absolute envelope for missing parent symplectic-potential contribution",
            "epsilon_theta_piece_missing <= sum_abs(ETH2989_01..08); no cancellation, no readout erasure",
            "dimensionless_after_M_ref",
            "Theta_parent sector split not signed",
            "VQL2902_1_theta_piece",
        ),
        (
            "ETH2989_01_EH_guard",
            "epsilon_EH_reference_guard",
            "guard against using EH theta as total MTS theta",
            "1 until all non-EH theta/source/boundary pieces are signed silent/exact/bounded",
            "boolean_or_dimensionless_guard",
            "EH is a reference template only",
            "VSL2903_0_EH_reference",
        ),
        (
            "ETH2989_02_boundary",
            "epsilon_Bv_ambiguity",
            "unfixed boundary/reference/improvement theta leakage",
            "abs(int_S delta B_v_unfixed)/M_ref",
            "dimensionless_boundary_improvement",
            "fixed-before-readout B_v convention missing",
            "VSP2903_1_Bv",
        ),
        (
            "ETH2989_03_extra",
            "epsilon_Qv_extra_piece",
            "extra motion/time/domain/memory theta/current leakage",
            "abs(int_S(Q_v_extra+C_v_extra-i_v Theta_extra))/M_ref",
            "dimensionless_extra_sector_charge",
            "extra sector variation and zero odd source not derived",
            "VSP2903_2_extra",
        ),
        (
            "ETH2989_04_projector",
            "epsilon_Qv_projector_piece",
            "projector/source-measure theta/current leakage",
            "abs(int_S(Q_v_projector+C_v_projector-i_v Theta_projector))/M_ref",
            "dimensionless_projector_source_charge",
            "delta Pi_M/source-measure owner missing",
            "VSP2903_3_projector",
        ),
        (
            "ETH2989_05_matter_source",
            "epsilon_Qv_matter_source_piece",
            "matter/source/worldtube theta/current leakage",
            "abs(int_S(Q_v_matter+C_v_matter-i_v Theta_matter_source))/M_ref",
            "dimensionless_matter_source_charge",
            "matter descent and hidden-source silence not parent-signed",
            "VSP2903_4_matter_source",
        ),
        (
            "ETH2989_06_constraint",
            "epsilon_Cv_constraint_missing",
            "nonconstraint or unbounded C_v leakage in the theta/Hamiltonian surface row",
            "abs(int_S C_v_nonconstraint_or_unbounded)/M_ref",
            "dimensionless_constraint_leakage",
            "common constraint split missing",
            "VSP2903_5_constraint",
        ),
        (
            "ETH2989_07_Mref",
            "epsilon_Mref_normalization",
            "positive same-frame denominator and linked surface class missing",
            "uncertainty in M_ref propagates into every theta-piece residual",
            "dimensionless_normalization_guard",
            "M_ref positive same-frame denominator absent",
            "VQC2902_6_denominator",
        ),
        (
            "ETH2989_08_units_orientation",
            "epsilon_theta_units_orientation",
            "orientation, density weight and units convention for theta surface integral",
            "norm mismatch between theta density, surface form and M_ref",
            "dimensionless_convention_guard",
            "density/orientation convention not fixed across sectors",
            "PKG2988_1_Theta",
        ),
        (
            "ETH2989_09_total",
            "epsilon_theta_piece_total_abs",
            "first source-ready total for missing Theta_parent sector pieces",
            "sum_abs(ETH2989_01..08)",
            "dimensionless_after_M_ref",
            "no component has numeric/theorem-zero source status",
            "ETH2989_00_definition",
        ),
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
        ("GATE2989_0_L_parent", "single sector-complete L_parent adopted before readout", "MISSING_TOTAL_PARENT_ACTION"),
        ("GATE2989_1_EH_limit", "EH theta used only after non-EH silence/exactness is signed", "REFERENCE_TEMPLATE_ONLY"),
        ("GATE2989_2_boundary", "fixed B_v/B_ref convention and zero/proper boundary flux", "MISSING_FIXED_BV_CONVENTION"),
        ("GATE2989_3_extra", "extra response theta and zero odd source derived", "MISSING_EXTRA_THETA_AND_ZERO_ODD_SOURCE"),
        ("GATE2989_4_projector", "delta Pi_M and source-measure theta pieces owned", "MISSING_PROJECTOR_VARIATION_OWNER"),
        ("GATE2989_5_matter", "matter/source/worldtube descent parent-signed", "CONDITIONAL_MATTER_DESCENT_UNSIGNED"),
        ("GATE2989_6_constraint", "C_v total constraint-proportional or source-bounded", "MISSING_COMMON_CONSTRAINT_SPLIT"),
        ("GATE2989_7_Mref", "positive same-frame M_ref and linked surface class", "MISSING_POSITIVE_SAME_FRAME_MREF"),
        ("GATE2989_8_promote", "promote Theta_parent extraction", "all previous gates must pass"),
    ]
    return [
        add(
            {
                "gate_id": gate_id,
                "promotion_gate": gate,
                "condition_passed": False,
                "status": status,
                "promotion_allowed_now": False,
            }
        )
        for gate_id, gate, status in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "decision_id": "DEC2989_0_derivation_attempt",
                "decision": "The Theta route is exact as a conditional field-theory route but not signed for current MTS.",
                "because": "a total parent variation identity exists only after all retained sector action blocks and boundary/reference conventions are owned together.",
                "next_action": "do not promote Omega, V_WEP, C_parent or local GR from this checkpoint.",
            }
        ),
        add(
            {
                "decision_id": "DEC2989_1_residual_interface",
                "decision": "Stage epsilon_theta_piece_missing as the honest residual interface.",
                "because": "EH, boundary, extra, projector/source-measure, matter/source, constraint and M_ref gaps are distinguishable and source-ready.",
                "next_action": "choose the least-scrutiny sector-normal-form branch or start filling the first numeric/source-backed theta row.",
            }
        ),
        add(
            {
                "decision_id": "DEC2989_2_best_next",
                "decision": "Next target should pick the parent sector normal form before another generator leap.",
                "because": "without a branch choice for L_extra/L_projector/L_matter/B_ref/C_v, every later Omega or local-GR proof inherits the same missing Theta term.",
                "next_action": "build 2990 around sector normal-form branch selection or first epsilon_theta numeric source row.",
            }
        ),
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "next_id": "NEXT2989_0_2990",
                "priority": "selected_primary",
                "next_doc": "2990-Y5-R2FR-sector-normal-form-branch-selection-or-first-epsilon-theta-numeric-source-row-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_sector_normal_form_branch_selection_or_first_epsilon_theta_numeric_source_row_under_AX1090_2990.py",
                "objective": "Choose or reject a parent sector normal form for EH, boundary, extra response, projector/source-measure, matter/source and constraint pieces; if the branch cannot be signed, fill the first source-backed epsilon_theta component row without claiming local GR.",
                "include": "sector branch menu;least-scrutiny route;B_ref convention;extra response normal form;projector variation owner;matter q-only descent;C_v split;M_ref denominator",
                "exclude": "C_parent import;Omega promotion;V_WEP promotion;local-GR claim;Newton claim;public/GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [add({"copy_id": key, "path": str(path), "exists": path.exists()}) for key, path in BRANCH_OUTPUTS.items()]


def validation(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    csv_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
    generated = [*csv_paths, DOC]
    formal_count = sum(1 for path in FORMALIZATION.rglob("*2989*") if path.is_file()) if FORMALIZATION.exists() else 0
    theta_total_not_signed = any(
        row["sector_id"] == "TLS2989_8_total" and row["current_status"] == "TOTAL_THETA_NOT_PARENT_SIGNED"
        for row in all_rows["sector_audit"]
    )
    theta_attempt_blocked = any(
        row["attempt_id"] == "THX2989_5_verdict"
        and row["current_status"] == "THETA_PARENT_NOT_DERIVED_STAGE_EPSILON_THETA_PIECE"
        and not row["derivation_passed"]
        for row in all_rows["theta_attempt"]
    )
    epsilon_nonclaim = all(
        row["current_value"] == "MISSING_SOURCE_BACKED_UPPER_BOUND"
        and not row["finite_value_present"]
        and row["source_ready_template"]
        and not row["valid_for_claim"]
        for row in all_rows["epsilon"]
    )
    checks = [
        ("VAL2989_0_sources_exist", all(row["exists"] for row in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2989_1_anchors_found", all(row["anchors_found"] for row in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2989_2_theta_total_not_signed", theta_total_not_signed, "Theta_parent total remains not parent-signed", True),
        ("VAL2989_3_theta_attempt_blocked", theta_attempt_blocked, "Theta extraction verdict blocked and nonclaim", True),
        ("VAL2989_4_eps_source_ready_nonclaim", epsilon_nonclaim, "epsilon_theta rows source-ready but nonclaim", True),
        ("VAL2989_5_gates_blocked", all(not row["condition_passed"] and not row["promotion_allowed_now"] for row in all_rows["gates"]), "all promotion gates blocked", True),
        ("VAL2989_6_no_live_cparent", not LIVE_C_PARENT.exists(), "C_parent_WEP_slot_import.csv not created or promoted", True),
        ("VAL2989_7_next_written", any(row["next_id"] == "NEXT2989_0_2990" for row in all_rows["next"]), "2990 next target written", True),
        ("VAL2989_8_branches_exist", all(row["exists"] for row in all_rows["branches"]), "branch copies exist", True),
        ("VAL2989_9_csvs_parse", all(csv_ok(path) for path in csv_paths), "all generated CSVs parse", True),
        ("VAL2989_10_outputs_under_post", all(under(path, ROOT) for path in generated), "all generated outputs under post-checkpoint-work", True),
        ("VAL2989_11_formalization_clean", formal_count == 0, f"no 2989 outputs in formalization-workbench (count={formal_count})", True),
        ("VAL2989_12_doc_written", DOC.exists(), "2989 markdown checkpoint exists", True),
    ]
    out_rows = [add({"validation_id": check_id, "passed": bool(passed), "check": check, "required": required}) for check_id, passed, check, required in checks]
    out_rows.append(add({"validation_id": "VAL2989_OVERALL", "passed": all(row["passed"] for row in out_rows), "check": "2989 validation overall", "required": True}))
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
        f"""# 2989 - Parent Lagrangian/Theta Sector Extraction or First epsilon_theta Bound

Status: `Y5_R2FR_2989_parent_Lagrangian_Theta_route_exact_but_sector_incomplete_epsilon_theta_piece_staged_nonclaim`

Claim ceiling: `no_Theta_parent_promotion_no_Omega_promotion_no_parent_generator_no_VWEP_promotion_no_Cparent_import_no_local_GR_no_Newton_no_WEP_no_R10_no_PPN_no_clock_no_orbital_no_public_claim`

## Summary

- The exact route is still the right one: declare one parent `L_parent`, vary it as `delta L_parent=E_A delta Phi^A+dTheta_parent`, then build `Omega_parent=delta Theta_parent`.
- This checkpoint tries the first domino directly: sector-complete `Theta_parent` extraction.
- The current corpus only gives an EH reference template plus conditional sector contracts; boundary, extra response, projector/source-measure, matter/source, constraint and `M_ref` pieces are not signed together.
- Therefore `Theta_parent` is not promoted. The honest output is a source-ready nonclaim `epsilon_theta_piece_missing` ledger.

## Generated Outputs

{table(outputs, ["output", "path", "exists"])}

## Branch Copies

{table(branches, ["copy", "path", "exists"])}

## Parent Lagrangian/Theta Sector Audit

{table(all_rows["sector_audit"], ["sector_id", "sector", "current_status", "blocking_gap", "fallback_symbol"])}

## Theta Extraction Attempt

{table(all_rows["theta_attempt"], ["attempt_id", "target", "current_status", "blocking_gap", "derivation_passed"])}

## epsilon_theta Piece Bound Rows

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
        "sector_audit": sector_audit_rows(),
        "theta_attempt": theta_attempt_rows(),
        "epsilon": epsilon_rows(),
        "gates": gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])
    shutil.copyfile(OUTPUTS["sector_audit"], BRANCH_OUTPUTS["theta_sector_copy"])
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
    print(f"2989 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
