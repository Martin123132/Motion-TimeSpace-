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

CHECKPOINT = "2987"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2987-Y5-R2FR-parent-generator-transformation-law-or-first-epsilon-VWEP-component-bound-under-AX1090.md"

SRC_2986_DOC = ROOT / "2986-Y5-R2FR-q-vX-action-descent-certificate-or-epsilon-VWEP-leakage-bound-under-AX1090.md"
SRC_2986_CERT = RESIDUALS / "P8_Y5_R2FR_2986_QVX_ACTION_DESCENT_CERTIFICATE_AUDIT.csv"
SRC_2986_EPS = RESIDUALS / "P8_Y5_R2FR_2986_EPSILON_VWEP_BOUND_ROWS_NONCLAIM.csv"
SRC_2986_NEXT = RESIDUALS / "P8_Y5_R2FR_2986_NEXT_TARGET.csv"
SRC_VWEP_MAP_MICRO = MICRO_COEFF / "V_WEP_field_by_field_action_map.csv"
SRC_VWEP_CANDIDATE_MICRO = MICRO_COEFF / "V_WEP_generator_candidate.csv"
SRC_FIELD_590 = RESIDUALS / "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv"
SRC_DCDAGGER_590 = RESIDUALS / "P8_Y5_R10_590_DCDAGGER_VERTICAL_MAP.csv"
SRC_VWEP_CONTRACT_1485 = RESIDUALS / "P8_Y5_R10_1485_V_WEP_GENERATOR_CONTRACT.csv"
SRC_VWEP_FIELD_1449 = RESIDUALS / "P8_Y5_R10_1449_FIELD_BY_FIELD_VWEP_ACTION_MAP.csv"
SRC_VWEP_DOMAIN_1448 = RESIDUALS / "P8_Y5_R10_1448_VWEP_DOMAIN_PROOF_ATTEMPT.csv"
SRC_LIFT_1045 = RESIDUALS / "P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv"
SRC_QVX_1023 = RESIDUALS / "P8_Y5_R10_1023_QVX_CERTIFICATE.csv"
SRC_VERTICAL_2952 = RESIDUALS / "P8_Y5_R2FR_2952_VERTICAL_GENERATOR_AUDIT.csv"
SRC_VERTICAL_PARENT_2952 = PARENT_ACTION / "vertical_generator_audit_2952_NOT_DERIVED.csv"
SRC_CONSTRUCTION_2892 = RESIDUALS / "P8_Y5_R2FR_2892_VERTICAL_GENERATOR_CONSTRUCTION_ATTEMPT.csv"
SRC_DERIVATION_2867 = RESIDUALS / "P8_Y5_R2FR_2867_VERTICAL_GENERATOR_DERIVATION_GATE.csv"
SRC_BASIS_2911 = RESIDUALS / "P8_Y5_R2FR_2911_KERNEL_BASIS_ATTEMPT.csv"
SRC_ACTION_IMAGE_2913 = RESIDUALS / "P8_Y5_R2FR_2913_ACTION_IMAGE_AND_GENERATOR_GATE.csv"
SRC_FACTOR_2972 = RESIDUALS / "P8_Y5_R2FR_2972_DQZ_FACTOR_AUDIT.csv"
SRC_EPSQ_2972 = RESIDUALS / "P8_Y5_R2FR_2972_FIRST_EPSQ_SUBROWS_NONCLAIM.csv"

LIVE_C_PARENT = MICRO_COEFF / "C_parent_WEP_slot_import.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2987_SOURCE_REGISTER.csv",
    "law": RESIDUALS / "P8_Y5_R2FR_2987_PARENT_GENERATOR_LAW_ATTEMPT.csv",
    "field_map": RESIDUALS / "P8_Y5_R2FR_2987_FIELD_BY_FIELD_TRANSFORMATION_AUDIT.csv",
    "epsilon": RESIDUALS / "P8_Y5_R2FR_2987_EPS_V_GENERATOR_COMPONENT_BOUND_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2987_GENERATOR_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2987_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2987_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2987_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2987_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "law_copy": PARENT_ACTION / "parent_generator_transformation_law_2987_NOT_SIGNED.csv",
    "epsilon_copy": LOCAL_BOUNDS / "eps_v_generator_component_bound_2987_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2987_first_epsilon_component_or_parent_omega_next_NONCLAIM.csv",
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
        ("SRC2987_00_2986_doc", SRC_2986_DOC, ["NEXT2986_0_2987", "field-by-field parent transformation law"], "2986 handoff"),
        ("SRC2987_01_2986_cert", SRC_2986_CERT, ["QVX2986_2_vX_vertical_generator", "NOT_PARENT_SIGNED_STAGE_EPSILON_VWEP"], "2986 certificate verdict"),
        ("SRC2987_02_2986_eps", SRC_2986_EPS, ["EPSV2986_03_generator", "eps_v_generator"], "2986 generator leakage row"),
        ("SRC2987_03_2986_next", SRC_2986_NEXT, ["NEXT2986_0_2987", "first source-ready epsilon_VWEP component"], "selected 2987 target"),
        ("SRC2987_04_micro_vwep_map", SRC_VWEP_MAP_MICRO, ["parent_configuration", "MISSING_ACTUAL_PARENT_TRANSFORMATION_LAW"], "current V_WEP field map"),
        ("SRC2987_05_micro_vwep_candidate", SRC_VWEP_CANDIDATE_MICRO, ["VWEP1448_0_candidate", "CANDIDATE_ONLY_NOT_PARENT_SIGNED"], "current V_WEP candidate"),
        ("SRC2987_06_590_field_map", SRC_FIELD_590, ["metric_or_coframe", "boundary_edge"], "legacy field-by-field vertical action map"),
        ("SRC2987_07_590_dcdagger", SRC_DCDAGGER_590, ["DVM590_4_raise_index", "not_available_until_reduced_Omega_is_explicit"], "DCdagger to vertical generator map"),
        ("SRC2987_08_1485_contract", SRC_VWEP_CONTRACT_1485, ["VGEN1485_4_verdict", "GENERATOR_CONTRACT_ONLY"], "V_WEP generator contract"),
        ("SRC2987_09_1449_field_map", SRC_VWEP_FIELD_1449, ["parent_configuration", "MISSING_ACTUAL_PARENT_TRANSFORMATION_LAW"], "field-by-field V_WEP map"),
        ("SRC2987_10_1448_domain", SRC_VWEP_DOMAIN_1448, ["VDP1448_6_verdict", "FAIL_CURRENT_CLAIM_DOMAIN_NOT_SIGNED"], "V_WEP domain proof"),
        ("SRC2987_11_1045_lift", SRC_LIFT_1045, ["VLG1045_4_verdict", "FAIL_CURRENT_CLAIM_VERTICAL_LIFT_NOT_SIGNED"], "matter lift gate"),
        ("SRC2987_12_1023_qvx", SRC_QVX_1023, ["QVC1023_4_vertical_action", "actual MTS parent transformation law"], "q/v_X certificate vertical-action clause"),
        ("SRC2987_13_2952_vertical", SRC_VERTICAL_2952, ["VNP2952_11_verdict", "VERTICAL_FIRST_CLASS_NOPOLE_NOT_DERIVED"], "vertical first-class audit"),
        ("SRC2987_14_2952_parent_copy", SRC_VERTICAL_PARENT_2952, ["VNP2952_11_verdict", "VERTICAL_FIRST_CLASS_NOPOLE_NOT_DERIVED"], "parent-action copy of vertical audit"),
        ("SRC2987_15_2892_construction", SRC_CONSTRUCTION_2892, ["VGC2892_5_verdict", "CONSTRUCTION_CONDITIONAL_CLOSURE_IF_USED_NOW"], "vertical generator construction attempt"),
        ("SRC2987_16_2867_derivation", SRC_DERIVATION_2867, ["VGEN2867_6_verdict", "FAIL_CURRENT_CLAIM"], "vertical generator derivation gate"),
        ("SRC2987_17_2911_basis", SRC_BASIS_2911, ["KB2911_8_verdict", "FINITE_DQZ_AND_KERNEL_ESCAPE_ROWS_REQUIRED"], "kernel basis attempt"),
        ("SRC2987_18_2913_action_image", SRC_ACTION_IMAGE_2913, ["AIG2913_5_current_verdict", "ACTION_IMAGE_NOT_PARENT_SIGNED"], "action image and generator gate"),
        ("SRC2987_19_2972_factor", SRC_FACTOR_2972, ["FAC2972_5_verdict", "NOT_SOURCE_BACKED_SPLIT_REQUIRED"], "DqZ factor audit"),
        ("SRC2987_20_2972_epsq", SRC_EPSQ_2972, ["EPSQ2972_00_eps_q_declaration", "MISSING_SOURCE_BACKED_UPPER_BOUND"], "epsq subrow ledger"),
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


def law_rows() -> list[dict[str, Any]]:
    data = [
        (
            "LAW2987_0_target",
            "actual parent generator",
            "v_X/V_WEP should be a vector field on the parent configuration/phase space, defined before readout and empirical projection.",
            "TARGET_SHARP",
            "not enough by itself; this row only states the target",
            False,
        ),
        (
            "LAW2987_1_hamiltonian_formula",
            "Hamiltonian/momentum-map route",
            "G_X[epsilon]=int_Sigma epsilon_nu C_X^nu+Q_X and delta G_X[delta Phi]=Omega_parent(delta Phi,v_X).",
            "EXACT_CONDITIONAL_FORMULA",
            "parent Theta/Omega, C_X, DC_X, Q_X and boundary pairing are missing",
            False,
        ),
        (
            "LAW2987_2_raise_index",
            "DCdagger to vector correction",
            "v_X=Omega_parent^{-1}[(DC_X)^dagger epsilon] on a reduced nondegenerate domain.",
            "CATEGORY_CORRECT_CONDITIONAL",
            "DCdagger is only a covector until the parent symplectic form is explicit and invertible",
            False,
        ),
        (
            "LAW2987_3_candidate_field_action",
            "candidate coordinate action",
            "delta_v q=0, delta_v Obs(q)=0, delta_v hidden representative nonzero, delta_v matter/constants/source/boundary zero or owned.",
            "CANDIDATE_TRANSFORMATION_LAW",
            "parent field chart, q map, hidden/visible split and all non-geometry lifts are unsigned",
            False,
        ),
        (
            "LAW2987_4_no_tautology_guard",
            "projection-by-declaration guard",
            "Putting observed variables inside q by hand cannot prove v_X is a parent gauge direction.",
            "GUARD_ACTIVE",
            "prevents false local-GR/Newton proof",
            False,
        ),
        (
            "LAW2987_5_verdict",
            "current parent generator law",
            "No actual parent transformation law is signed in the current corpus.",
            "NOT_PARENT_SIGNED_STAGE_EPS_V_GENERATOR_BOUND",
            "move to eps_v_generator component bound rows",
            False,
        ),
    ]
    return [
        add(
            {
                "law_id": law_id,
                "object": obj,
                "statement": statement,
                "current_status": status,
                "blocking_gap": gap,
                "parent_signed": signed,
                "theorem_zero_adopted": False,
            }
        )
        for law_id, obj, statement, status, gap, signed in data
    ]


def field_map_rows() -> list[dict[str, Any]]:
    data = [
        (
            "FM2987_0_parent_chart",
            "Phi_parent",
            "delta_v Phi_parent := V_WEP[Phi]",
            "MISSING_PARENT_FIELD_CHART",
            "no signed configuration/phase-space chart containing all geometry, hidden, matter, source and boundary variables",
            "eps_parent_chart",
        ),
        (
            "FM2987_1_geometry",
            "metric/coframe/connection",
            "delta_v e_obs = delta_v g_obs = delta_v omega_obs = 0 by Dq[v]=0, or Lie/local-Lorentz candidate before quotient",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "observed coframe is q-basic only conditionally and parent Omega is missing",
            "eps_geometry_action",
        ),
        (
            "FM2987_2_hidden_representatives",
            "Xhat/memory/projector/domain variables",
            "delta_v hidden variables moves only inside the q fibre",
            "UNMAPPED_PARENT_FIELD_COMPONENTS",
            "hidden-to-visible coefficient Hom/no-shadow theorem not derived",
            "eps_hidden_action",
        ),
        (
            "FM2987_3_matter_fields",
            "ordinary matter fields Psi_A",
            "delta_v Psi_A=0 or owned gauge/diffeomorphism/local-Lorentz lift",
            "LIFT_OPTIONS_AVAILABLE_NOT_PARENT_ASSIGNED",
            "species-complete matter bundle functor missing",
            "eps_matter_lift",
        ),
        (
            "FM2987_4_constants_em",
            "alpha_EM, masses, charges, clock/material constants",
            "delta_v theta_A=0 and delta_v alpha_EM=0 if fixed/superselected q-basic data",
            "CONDITIONAL_OWNER_NOT_SIGNED",
            "constant/EM/current lattice owner not signed",
            "eps_constants_em",
        ),
        (
            "FM2987_5_source_weights",
            "source/current/action weights",
            "delta_v source labels and species weights vanish because no such parent slot exists",
            "SOURCE_SLOT_COUNTERMODEL_SURVIVES",
            "no-source-only grammar and source-label forgetting not derived",
            "eps_source_slot",
        ),
        (
            "FM2987_6_boundary_readout",
            "boundary, support, readout and projector fields",
            "delta_v boundary/readout is zero, proper, exact or retained as explicit finite bound",
            "BOUNDARY_READOUT_NOT_SIGNED",
            "Q_X, B_X primitive, support collar and projector orthogonality remain open",
            "eps_boundary_readout",
        ),
        (
            "FM2987_7_rank_bracket",
            "rank, bracket and stabilizer",
            "v_X lies in a regular first-class kernel distribution with no proper physical stabilizer",
            "RANK_BRACKET_NOT_COMPUTED",
            "constraint rank, bracket closure and no-stabilizer theorem are missing",
            "eps_rank_bracket",
        ),
        (
            "FM2987_8_verdict",
            "field-by-field transformation law",
            "all field rows are parent-signed in one branch",
            "FIELD_MAP_NOT_SIGNED",
            "use eps_v_generator_abs instead of claiming V_WEP is physical parent vertical generator",
            "eps_v_generator_abs",
        ),
    ]
    return [
        add(
            {
                "map_id": map_id,
                "field_block": block,
                "candidate_action": action,
                "current_status": status,
                "blocking_gap": gap,
                "fallback_symbol": fallback,
                "map_satisfied": False,
                "parent_signed": False,
            }
        )
        for map_id, block, action, status, gap, fallback in data
    ]


def epsilon_rows() -> list[dict[str, Any]]:
    data = [
        (
            "EVG2987_00_definition",
            "eps_v_generator",
            "field-by-field parent generator mismatch",
            "||V_physical - V_parent_kernel||_V <= eps_v_generator_abs",
            "field_norm",
            "V_WEP remains candidate, not parent-owned vector field",
            "V_WEP_field_by_field_action_map",
        ),
        ("EVG2987_01_chart", "eps_parent_chart", "parent chart/domain missing", "eps_parent_chart bounds failure to define V on all parent fields", "field_chart_norm", "configuration/phase chart not signed", "VNP2952_4_field_action"),
        ("EVG2987_02_omega", "eps_parent_Omega", "parent symplectic package missing", "eps_parent_Omega bounds missing Theta/Omega contribution in v=Omega^-1 DCdagger", "symplectic_norm", "Theta/Omega not explicit", "VNP2952_1_parent_omega"),
        ("EVG2987_03_DCX", "eps_DCX_operator", "constraint linearization missing", "eps_DCX_operator bounds missing C_X/DC_X covector extraction", "covector_norm", "C_X and DC_X not written from parent action", "VNP2952_2_DCX_operator"),
        ("EVG2987_04_raise", "eps_raise_index", "Omega inverse/reduced-domain gap", "eps_raise_index bounds the gap between DCdagger covector and raised vector field", "operator_norm", "reduced nondegenerate Omega not available", "DVM590_4_raise_index"),
        ("EVG2987_05_geometry", "eps_geometry_action", "geometry/coframe action gap", "eps_geometry_action bounds unowned metric/coframe vertical action", "geometry_norm", "standard candidate not parent declared", "metric_or_coframe"),
        ("EVG2987_06_hidden", "eps_hidden_action", "hidden representative action gap", "eps_hidden_action bounds hidden-to-visible representative leakage", "hidden_field_norm", "memory/projector/domain transformation law unmapped", "domain_memory_projector_fields"),
        ("EVG2987_07_matter", "eps_matter_lift", "ordinary matter lift gap", "eps_matter_lift bounds non-owned physical matter lift response", "matter_norm", "species-complete lift not assigned", "VLG1045_4_verdict"),
        ("EVG2987_08_constants", "eps_constants_em", "constant/EM marker action gap", "eps_constants_em bounds Lie_v theta and alpha/current-lattice leakage", "dimensionless_or_clock_em_norm", "constant/EM owner not signed", "matter_constants_and_spectra"),
        ("EVG2987_09_source", "eps_source_slot", "source-weight/source-label action gap", "eps_source_slot bounds pre-action source prefactor or source-only label reentry", "source_norm", "source slot countermodel survives", "source_coupling"),
        ("EVG2987_10_boundary", "eps_boundary_readout", "boundary/readout action gap", "eps_boundary_readout bounds Q_X/B_X/support/projector leakage", "boundary_readout_norm", "boundary/readout not parent signed", "boundary_domain_readout"),
        ("EVG2987_11_rank", "eps_rank_bracket", "rank/bracket/stabilizer gap", "eps_rank_bracket bounds failure of regular first-class kernel distribution", "rank_bracket_norm", "rank and bracket closure not computed", "VNP2952_7_bracket_closure"),
        ("EVG2987_12_total", "eps_v_generator_abs", "absolute no-cancellation generator envelope", "eps_v_generator_abs <= sum EVG2987_01..11; no cancellations or readout deletion", "field_norm_mixed", "no component has source-backed finite value or theorem-zero status", "EVG2987_00_definition"),
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
        ("GATE2987_0_parent_chart", "parent field chart/domain exists", False, "missing chart/domain owner"),
        ("GATE2987_1_omega", "parent Theta/Omega and reduced inverse exist", False, "Omega package missing"),
        ("GATE2987_2_DCX", "C_X, DC_X and boundary pairing extracted", False, "operator not written from parent action"),
        ("GATE2987_3_field_map", "field-by-field transformation law signed", False, "geometry/matter/source/boundary blocks unsigned"),
        ("GATE2987_4_Dq_kernel", "Dq[V_WEP]=0 over an open branch", False, "Dq matrix, basis and norms missing"),
        ("GATE2987_5_matter_source", "matter/source lift and no-slot grammar signed", False, "countermodels remain legal"),
        ("GATE2987_6_boundary_rank", "boundary charge, bracket and rank close", False, "edge charge and first-class closure missing"),
        ("GATE2987_7_promote", "promote V_WEP as actual parent generator", False, "all previous gates must pass"),
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
                "decision_id": "DEC2987_0_formula_kept",
                "decision": "Keep v_X=Omega^{-1}[(DC_X)^dagger epsilon] as the correct mathematical route.",
                "because": "it fixes the previous category error: DCdagger is a covector, not the generator itself.",
                "next_action": "source the parent Omega/DC_X package or carry eps_parent_Omega and eps_DCX_operator.",
            }
        ),
        add(
            {
                "decision_id": "DEC2987_1_no_generator_promotion",
                "decision": "Do not promote V_WEP/v_X as the actual parent generator.",
                "because": "the field chart, Omega inverse, field map, matter lift, source slot, boundary charge and rank/bracket gates are all unsigned.",
                "next_action": "use eps_v_generator_abs as the first explicit component of epsilon_VWEP.",
            }
        ),
        add(
            {
                "decision_id": "DEC2987_2_next",
                "decision": "Next attack should be parent Omega/DC_X ownership or first finite eps_parent_Omega row.",
                "because": "without Omega/DC_X the generator cannot become more than a symbolic field-map wish list.",
                "next_action": "attempt the parent symplectic package first, then stage a finite Omega/DC_X leakage row if it fails.",
            }
        ),
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "next_id": "NEXT2987_0_2988",
                "priority": "selected_primary",
                "next_doc": "2988-Y5-R2FR-parent-Omega-DCX-package-or-first-eps-parent-Omega-bound-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_parent_Omega_DCX_package_or_first_eps_parent_Omega_bound_under_AX1090_2988.py",
                "objective": "Try to derive the parent Theta/Omega plus C_X/DC_X package that raises DCdagger into the actual generator; if it fails, create the first finite-source template for eps_parent_Omega/eps_DCX_operator.",
                "include": "delta L=E delta Phi+dTheta;Omega=dTheta;C_X;DC_X;Q_X boundary pairing;Omega inverse domain;eps_parent_Omega;eps_DCX_operator",
                "exclude": "C_parent import;V_WEP promotion;local-GR claim;theorem-zero promotion;GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [add({"copy_id": key, "path": str(path), "exists": path.exists()}) for key, path in BRANCH_OUTPUTS.items()]


def validation(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    csv_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
    generated = [*csv_paths, DOC]
    formal_count = sum(1 for path in FORMALIZATION.rglob("*2987*") if path.is_file()) if FORMALIZATION.exists() else 0
    law_not_signed = any(row["law_id"] == "LAW2987_5_verdict" and row["current_status"] == "NOT_PARENT_SIGNED_STAGE_EPS_V_GENERATOR_BOUND" and not row["parent_signed"] for row in all_rows["law"])
    field_map_blocked = any(row["map_id"] == "FM2987_8_verdict" and row["current_status"] == "FIELD_MAP_NOT_SIGNED" and not row["map_satisfied"] for row in all_rows["field_map"])
    epsilon_nonclaim = all(
        row["current_value"] == "MISSING_SOURCE_BACKED_UPPER_BOUND"
        and not row["finite_value_present"]
        and row["source_ready_template"]
        and not row["valid_for_claim"]
        for row in all_rows["epsilon"]
    )
    checks = [
        ("VAL2987_0_sources_exist", all(row["exists"] for row in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2987_1_anchors_found", all(row["anchors_found"] for row in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2987_2_law_not_signed", law_not_signed, "parent generator transformation law not signed", True),
        ("VAL2987_3_field_map_blocked", field_map_blocked, "field-by-field map remains blocked", True),
        ("VAL2987_4_eps_source_ready_nonclaim", epsilon_nonclaim, "eps_v_generator component rows source-ready but nonclaim", True),
        ("VAL2987_5_gates_blocked", all(not row["condition_passed"] and not row["promotion_allowed_now"] for row in all_rows["gates"]), "all generator promotion gates blocked", True),
        ("VAL2987_6_no_live_cparent", not LIVE_C_PARENT.exists(), "C_parent_WEP_slot_import.csv not created or promoted", True),
        ("VAL2987_7_next_written", any(row["next_id"] == "NEXT2987_0_2988" for row in all_rows["next"]), "2988 next target written", True),
        ("VAL2987_8_branches_exist", all(row["exists"] for row in all_rows["branches"]), "branch copies exist", True),
        ("VAL2987_9_csvs_parse", all(csv_ok(path) for path in csv_paths), "all generated CSVs parse", True),
        ("VAL2987_10_outputs_under_post", all(under(path, ROOT) for path in generated), "all generated outputs under post-checkpoint-work", True),
        ("VAL2987_11_formalization_clean", formal_count == 0, f"no 2987 outputs in formalization-workbench (count={formal_count})", True),
        ("VAL2987_12_doc_written", DOC.exists(), "2987 markdown checkpoint exists", True),
    ]
    out_rows = [add({"validation_id": check_id, "passed": bool(passed), "check": check, "required": required}) for check_id, passed, check, required in checks]
    out_rows.append(add({"validation_id": "VAL2987_OVERALL", "passed": all(row["passed"] for row in out_rows), "check": "2987 validation overall", "required": True}))
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
        f"""# 2987 - Parent Generator Transformation Law or First epsilon_VWEP Component Bound

Status: `Y5_R2FR_2987_parent_generator_formula_correct_but_not_signed_eps_v_generator_component_bound_staged_nonclaim`

Claim ceiling: `no_parent_generator_transformation_law_no_VWEP_promotion_no_Cparent_DERIVED_ZERO_no_Cparent_import_no_local_GR_no_Newton_no_WEP_no_R10_no_PPN_no_clock_no_orbital_no_public_claim`

## Summary

- The right mathematical map is clear: `DCdagger` is a field-space covector and the actual generator would be `v_X = Omega_parent^{-1}[(DC_X)^dagger epsilon]`.
- The current corpus still lacks the parent `Theta/Omega`, `C_X/DC_X`, reduced inverse, field-by-field action, boundary charge and rank/bracket closure needed to sign that map.
- So `V_WEP` remains a typed candidate, not the actual parent generator.
- The useful progress is that `eps_v_generator` is now split into source-ready nonclaim components rather than being one vague residual.

## Generated Outputs

{table(outputs, ["output", "path", "exists"])}

## Branch Copies

{table(branches, ["copy", "path", "exists"])}

## Parent Generator Law Attempt

{table(all_rows["law"], ["law_id", "object", "current_status", "blocking_gap", "parent_signed"])}

## Field-by-Field Transformation Audit

{table(all_rows["field_map"], ["map_id", "field_block", "current_status", "blocking_gap", "fallback_symbol", "map_satisfied"])}

## eps_v_generator Component Bound

{table(all_rows["epsilon"], ["epsilon_id", "symbol", "definition", "bound_interface", "current_value", "why_nonclaim"])}

## Generator Promotion Gates

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
        "law": law_rows(),
        "field_map": field_map_rows(),
        "epsilon": epsilon_rows(),
        "gates": gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])
    shutil.copyfile(OUTPUTS["law"], BRANCH_OUTPUTS["law_copy"])
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
    print(f"2987 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
