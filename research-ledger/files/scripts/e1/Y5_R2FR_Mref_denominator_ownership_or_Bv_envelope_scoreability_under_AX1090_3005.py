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
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3005"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3005-Y5-R2FR-Mref-denominator-ownership-or-Bv-envelope-scoreability-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3005_SOURCE_REGISTER.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3005_MREF_DENOMINATOR_OWNERSHIP_AUDIT.csv",
    "denominators": RESIDUALS / "P8_Y5_R2FR_3005_DENOMINATOR_ACQUISITION_ROWS.csv",
    "scoreability": RESIDUALS / "P8_Y5_R2FR_3005_BV_ENVELOPE_SCOREABILITY_ROWS.csv",
    "rebase": RESIDUALS / "P8_Y5_R2FR_3005_BV_REBASE_AFTER_MREF_DENOMINATOR.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3005_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3005_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3005_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3005_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3005_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "audit_copy": PARENT_ACTION / "Mref_denominator_ownership_3005_NOT_SIGNED.csv",
    "score_copy": LOCAL_BOUNDS / "Bv_envelope_scoreability_rows_3005_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3005_PARENT_THETA_QTAU_HTAU_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def missing_anchors(path: Path, needles: list[str]) -> str:
    haystack = text(path)
    return "; ".join(needle for needle in needles if needle not in haystack)


def base(row: dict[str, Any]) -> dict[str, Any]:
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


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


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


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [str(output_row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


SOURCE_SPECS = [
    (
        "SRC3005_00_3004_next",
        RESIDUALS / "P8_Y5_R2FR_3004_NEXT_TARGET.csv",
        ["NEXT3004_0_3005", "M_ref/M_H_ref"],
        "3004 selects denominator ownership as the next Bv bottleneck.",
    ),
    (
        "SRC3005_01_3004_rebase",
        RESIDUALS / "P8_Y5_R2FR_3004_BV_REBASE_AFTER_PROJECTOR_BOUNDARY.csv",
        ["REB3004_5_Bv_remainder", "MISSING_MREF_DENOMINATOR_BOUND"],
        "3004 rebase leaves M_ref denominator as the sharp remaining Bv scoring debt.",
    ),
    (
        "SRC3005_02_2596_denominator_rows",
        RESIDUALS / "P8_Y5_MHREF_2596_DENOMINATOR_ROWS.csv",
        ["MHD2596_3_theta", "MHD2596_4_Qtau", "MHD2596_5_MHref"],
        "2596 has strict denominator rows for theta, Q_tau and M_H_ref.",
    ),
    (
        "SRC3005_03_2596_claim_gates",
        RESIDUALS / "P8_Y5_MHREF_2596_CLAIM_GATES.csv",
        ["CG2596_2_orbital_GM", "REJECTED_SHORTCUT"],
        "2596 rejects orbital GM as denominator input.",
    ),
    (
        "SRC3005_04_2596_decision",
        RESIDUALS / "P8_Y5_MHREF_2596_DECISION_LEDGER.csv",
        ["DEC2596_1_no_denominator_claim", "MHREF_TAU_SURFACE_LOCK_NOT_DERIVED"],
        "2596 records the denominator lock as not derived.",
    ),
    (
        "SRC3005_05_2597_acquisition",
        RESIDUALS / "P8_Y5_TAU_IDENTITY_2597_MHREF_SOURCE_ACQUISITION_ROWS.csv",
        ["MHA2597_7_MHref", "MISSING_POSITIVE_SAME_FRAME_MHREF"],
        "2597 source acquisition rows keep M_H_ref missing.",
    ),
    (
        "SRC3005_06_2595_components",
        RESIDUALS / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv",
        ["GMC2595_4_MHref", "MISSING_M_H_REF"],
        "2595 lists M_H_ref as denominator for PiM/GM transfer.",
    ),
    (
        "SRC3005_07_1006_theorem_audit",
        RESIDUALS / "P8_Y5_R10_1006_MHREF_DENOMINATOR_THEOREM_AUDIT.csv",
        ["MHA1006_6_theorem_verdict", "fail_current_claim"],
        "1006 audits positive same-frame M_H_ref and refuses current claim.",
    ),
    (
        "SRC3005_08_1017_schema",
        RESIDUALS / "P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv",
        ["MHR1017_0_M_H_ref_denominator", "MISSING_STABLE_MH_REF"],
        "1017 first-row schema requires stable M_H_ref with source paths and units.",
    ),
    (
        "SRC3005_09_2938_contract",
        RESIDUALS / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv",
        ["REF2938_0_MHref_definition", "REF2938_4_no_laundering"],
        "2938 defines M_H_ref and installs no-laundering guardrail.",
    ),
    (
        "SRC3005_10_2947_runner",
        RESIDUALS / "P8_Y5_R2FR_2947_MHREF_PIM_FIRST_ROW_RUNNER_ROWS.csv",
        ["RUN2947_1_MHref", "MISSING_H_TAU_H_REF_MHREF"],
        "2947 keeps the M_H_ref first row unfilled.",
    ),
    (
        "SRC3005_11_2666_template",
        RESIDUALS / "P8_Y5_R10_MHREF_DENOMINATOR_2666_DENOMINATOR_ROW_TEMPLATE_NONCLAIM.csv",
        ["DROW2666_0_M_H_ref", "MISSING_STABLE_MH_REF"],
        "2666 stages the denominator row as a nonclaim template.",
    ),
    (
        "SRC3005_12_2666_decision",
        RESIDUALS / "P8_Y5_R10_MHREF_DENOMINATOR_2666_DECISION_LEDGER.csv",
        ["DEC2666_0_derivation_status", "M_H_ref is not derived"],
        "2666 records denominator derivation as still missing.",
    ),
    (
        "SRC3005_13_HSM_contract",
        RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        ["HSM541_1_integrable_charge", "HSM541_5_Gauss_orbital_readout"],
        "Hamiltonian source-measure contract states integrable charge and Gauss/orbital readout requirements.",
    ),
    (
        "SRC3005_14_worldtube",
        RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        ["T510_1_worldtube_source_measure", "definition_not_yet_locked"],
        "worldtube theorem defines dressed Hamiltonian source mass but says definition is not locked.",
    ),
    (
        "SRC3005_15_PG_contract",
        RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        ["PG0_Hamiltonian_charge_input", "PG10_retained_residual_fallback"],
        "Poisson/Gauss contract keeps calibration downstream of Hamiltonian source charge.",
    ),
    (
        "SRC3005_16_boundary_status",
        RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
        ["M_H_ref", "missing_claim_valid_source_or_zero_theorem"],
        "boundary/reference first-row status finds no claim-valid M_H_ref row.",
    ),
    (
        "SRC3005_17_edge_acquisition",
        RESIDUALS / "P8_Y5_R10_673_EDGE_COEFFICIENT_ACQUISITION_LEDGER.csv",
        ["ECA673_5_M_H_ref", "MISSING_SOURCE_BACKED_M_H_REF_FOR_CURRENT_BRANCH"],
        "edge coefficient ledger also requires source-backed M_H_ref.",
    ),
    (
        "SRC3005_18_Newton_claim_gate",
        RESIDUALS / "P8_Y5_R10_991_CLAIM_GATE.csv",
        ["CG991_1_Newton_source", "orbital GM substitution is forbidden"],
        "Newton source gate forbids using observed GM to define the source denominator.",
    ),
]


def source_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "required_anchors": "; ".join(needles),
                "anchors_found": anchors(path, needles),
                "missing_anchors": missing_anchors(path, needles),
                "role": role,
            }
        )
        for source_id, path, needles, role in SOURCE_SPECS
    ]


def audit_rows() -> list[dict[str, Any]]:
    data = [
        (
            "MDA3005_0_system_worldtube",
            "system/source worldtube/support is fixed before readout",
            "MISSING_SYSTEM_ID_WORLD_TUBE_SUPPORT",
            "anonymous denominator rows cannot prove a source-transfer theorem",
            "MHD2596_0_system;MHR1519_0_system",
        ),
        (
            "MDA3005_1_same_frame",
            "q/e_obs/coframe is parent-owned and shared by source, clock, boundary and orbit",
            "MISSING_PARENT_Q_OBS_E_OWNER",
            "otherwise source mass and orbital/readout mass can live in different frames",
            "MHD2596_1_coframe;OCF1519_6_MHref_denominator",
        ),
        (
            "MDA3005_2_tau_lock",
            "one tau generator controls source charge, clock, orbit, boundary and readout",
            "MISSING_TAU_LOCK",
            "mixed time conventions can manufacture denominator agreement",
            "MHD2596_2_tau;MHA1006_2_tau_frame_lock",
        ),
        (
            "MDA3005_3_theta_Qtau",
            "theta_MTS and Q_tau^MTS are extracted from the full parent action",
            "MISSING_THETA_QTAU_PARENT_SOURCE",
            "EH-only charge cannot normalize an MTS residual envelope",
            "MHD2596_3_theta;MHD2596_4_Qtau;ACQ1519_1_theta_Qtau_piece_table",
        ),
        (
            "MDA3005_4_integrability",
            "delta H_tau has zero field-space curl or sourced bound with fixed reference",
            "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO",
            "without integrability H_tau is not a state function denominator",
            "DROW2666_1_integrability_curl;HSM541_1_integrable_charge",
        ),
        (
            "MDA3005_5_fixed_Href",
            "H_ref/reference subtraction is fixed before source/readout fitting",
            "MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO",
            "a moving reference can absorb boundary/source residuals",
            "MHR1519_6_Href;REF2938_0_MHref_definition",
        ),
        (
            "MDA3005_6_positive_MHref",
            "M_H_ref=H_tau[S_outer]-H_ref is finite, positive, same-frame and sourced",
            "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "negative/zero/unsourced denominator cannot score a residual bound",
            "MHD2596_5_MHref;MHA2597_7_MHref;GMC2595_4_MHref",
        ),
        (
            "MDA3005_7_surface_homology",
            "S1/S2/A_ext/radii/homology class are fixed before readout",
            "MISSING_SURFACE_HOMOLOGY_LOCK",
            "post-readout surfaces can erase equality or commutator residuals",
            "MHD2596_6_surfaces;MH1518_1_S1;MH1518_2_S2;MH1518_3_annulus",
        ),
        (
            "MDA3005_8_PiM_Hilbert_bridge",
            "Pi_M Hilbert current equals the same Hamiltonian source charge in the same frame",
            "MISSING_HILBERT_TO_HTAU_MAP",
            "closed topological/projected charge can be the wrong source mass",
            "RUN2947_2_PiM_Hilbert;HSM541_0_adopt_Hamiltonian_PiM",
        ),
        (
            "MDA3005_9_Poisson_Gauss_downstream",
            "Hamiltonian source charge later derives Poisson/Gauss/orbital GM",
            "DOWNSTREAM_NOT_DENOMINATOR_INPUT",
            "observed GM tests the derived bridge; it cannot define M_H_ref",
            "PG0_Hamiltonian_charge_input;CG991_1_Newton_source",
        ),
        (
            "MDA3005_10_anti_circularity",
            "orbital GM, EH-only charge, post-readout frames and fitted references are rejected",
            "GUARDRAIL_INSTALLED_NONCLAIM",
            "anti-circularity is installed, but it is not a denominator value",
            "CG2596_2_orbital_GM;REF2938_4_no_laundering;DEC2549_1_orbital_GM_refused",
        ),
        (
            "MDA3005_11_verdict",
            "current MTS owns a positive same-frame Bv denominator",
            "DENOMINATOR_NOT_DERIVED_ROWS_STAGED",
            "no current parent-signed H_tau/H_ref/M_H_ref value or theorem-zero exists",
            "all rows above",
        ),
    ]
    return [
        base(
            {
                "audit_id": audit_id,
                "denominator_clause": denominator_clause,
                "current_status": current_status,
                "failure_mode": failure_mode,
                "source_anchors": source_anchors,
                "parent_signed_now": False,
                "finite_denominator_now": False,
            }
        )
        for audit_id, denominator_clause, current_status, failure_mode, source_anchors in data
    ]


def denominator_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DEN3005_0_system",
            "system_worldtube_lock",
            "unique system_id/source worldtube/source support shared by J_H,Q_tau,Pi_M,S1/S2,A_ext,readout",
            "identifier_and_support_metadata",
            "MISSING_SYSTEM_ID;MISSING_WORLDTUBE_ID;MISSING_SOURCE_SUPPORT_LOCK",
            "MHD2596_0_system;MHR1519_0_system",
        ),
        (
            "DEN3005_1_coframe",
            "e_obs_coframe_lock",
            "observed coframe fixed by q/Obs_e before source, boundary, clock and orbital readout",
            "certificate",
            "MISSING_COFRAME_ID;MISSING_PARENT_Q_OBS_E_OWNER",
            "MHD2596_1_coframe;OCF1519_6_MHref_denominator",
        ),
        (
            "DEN3005_2_tau",
            "tau_frame_lock",
            "same tau for source, charge, clocks, orbit, boundary and readout",
            "certificate",
            "MISSING_TAU_LOCK",
            "MHD2596_2_tau;MHA1006_2_tau_frame_lock",
        ),
        (
            "DEN3005_3_theta",
            "theta_MTS_source",
            "full parent symplectic potential including EH, boundary, extra, projector and matter/source sectors",
            "equation_source",
            "MISSING_THETA_MTS_SOURCE",
            "MHD2596_3_theta;ACQ1519_1_theta_Qtau_piece_table",
        ),
        (
            "DEN3005_4_Qtau",
            "Q_tau_MTS_source",
            "total parent Hamiltonian/Noether charge form for tau",
            "charge_form_source",
            "MISSING_Q_TAU_MTS_SOURCE",
            "MHD2596_4_Qtau;DROW2666_0_M_H_ref",
        ),
        (
            "DEN3005_5_Htau",
            "H_tau_outer",
            "integrable surface Hamiltonian charge on outer linked surface",
            "mass_or_energy_units",
            "MISSING_H_TAU",
            "MHR1519_5_Htau;HSM541_1_integrable_charge",
        ),
        (
            "DEN3005_6_Href",
            "H_ref_fixed",
            "fixed reference/counterterm selected before source/readout fitting",
            "mass_or_energy_units",
            "MISSING_H_REF;MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO",
            "MHR1519_6_Href;DROW2666_2_reference_shift",
        ),
        (
            "DEN3005_7_MHref",
            "M_H_ref",
            "positive finite H_tau[S_outer]-H_ref in same e_obs/tau/source branch, not orbital GM",
            "mass_or_energy_units",
            "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "MHD2596_5_MHref;MHA2597_7_MHref;RUN2947_1_MHref",
        ),
        (
            "DEN3005_8_surface_homology",
            "surface_homology_lock",
            "S1/S2/A_ext/r1/r2/homology/source-free exterior fixed before readout",
            "surface_and_topology_metadata",
            "MISSING_SURFACE_HOMOLOGY",
            "MHD2596_6_surfaces;MH1518_3_annulus",
        ),
        (
            "DEN3005_9_integrability",
            "delta_H_tau_curl",
            "field-space curl/integrability defect of H_tau with fixed reference",
            "dimensionless_or_charge_curl_units",
            "MISSING_INTEGRABILITY_CERTIFICATE",
            "MHD2596_7_integrability;DROW2666_1_integrability_curl",
        ),
        (
            "DEN3005_10_PiM_Hilbert",
            "PiM_Hilbert_equality",
            "Pi_M J_H equals same-frame Hamiltonian source charge, not post-readout topological mask",
            "mass_or_charge_units",
            "MISSING_HILBERT_TO_HTAU_MAP",
            "RUN2947_2_PiM_Hilbert;HSM541_0_adopt_Hamiltonian_PiM",
        ),
        (
            "DEN3005_11_no_laundering",
            "anti_circularity_certificate",
            "orbital GM/EH-only charge/fitted reference/post-readout surface are rejected as denominator fillers",
            "guardrail_certificate",
            "GUARDRAIL_INSTALLED_NONCLAIM",
            "REF2938_4_no_laundering;CG2596_2_orbital_GM;CG991_1_Newton_source",
        ),
    ]
    return [
        base(
            {
                "denominator_id": denominator_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "current_value": current_value,
                "source_anchors": source_anchors,
                "finite_numeric_value_present": False,
                "positive_same_frame_now": False,
                "orbital_GM_imported": False,
            }
        )
        for denominator_id, symbol, definition, units, current_value, source_anchors in data
    ]


def scoreability_rows() -> list[dict[str, Any]]:
    data = [
        ("BVS3005_0_exact_fixed", "epsilon_Bv_exact_fixed_primitive", "0", "M_ref not required for the exact/fixed component itself, but full Bv still needs denominator", "COMPONENT_CLOSED_NOT_FULL_ENVELOPE"),
        ("BVS3005_1_tau_surface", "epsilon_Bv_tau_surface_commutator_total_abs", "COMPONENTS_MISSING_NO_FINITE_VALUE", "M_ref/M_H_ref missing", "NOT_SCOREABLE"),
        ("BVS3005_2_corner_topological", "epsilon_Bv_corner_topological_total_abs", "MISSING_SOURCE_BACKED_UPPER_BOUND", "M_ref/M_H_ref missing", "NOT_SCOREABLE"),
        ("BVS3005_3_unfixed_reference", "epsilon_Bv_unfixed_reference", "MISSING_SOURCE_BACKED_UPPER_BOUND", "M_ref/M_H_ref missing", "NOT_SCOREABLE"),
        ("BVS3005_4_projector_boundary", "epsilon_Bv_projector_boundary", "MISSING_SOURCE_BACKED_UPPER_BOUND", "M_ref/M_H_ref missing", "NOT_SCOREABLE"),
        ("BVS3005_5_denominator", "M_ref_or_M_H_ref", "MISSING_POSITIVE_SAME_FRAME_MHREF", "denominator source/positivity/integrability missing", "NOT_SCOREABLE"),
        ("BVS3005_6_total_envelope", "epsilon_Bv_ambiguity_abs_envelope", "NOT_COMPUTED", "numerator components and denominator are not jointly claim-valid", "NO_BV_SCORE_ALLOWED"),
    ]
    return [
        base(
            {
                "score_id": score_id,
                "quantity": quantity,
                "current_value": current_value,
                "denominator_status": denominator_status,
                "scoreability_status": scoreability_status,
                "claim_blocker": "MISSING_NUMERATOR_OR_DENOMINATOR_CLAIM_VALID_ROW",
            }
        )
        for score_id, quantity, current_value, denominator_status, scoreability_status in data
    ]


def rebase_rows() -> list[dict[str, Any]]:
    data = [
        ("REB3005_0_exact_fixed", "epsilon_Bv_exact_fixed_primitive", "0", "closed only as exact/fixed component by 2999"),
        ("REB3005_1_tau_surface", "epsilon_Bv_tau_surface_commutator_total_abs", "COMPONENTS_MISSING_NO_FINITE_VALUE", "explicit residual closure by 3001"),
        ("REB3005_2_corner_topological", "epsilon_Bv_corner_topological_total_abs", "MISSING_SOURCE_BACKED_UPPER_BOUND", "classified and staged by 3002"),
        ("REB3005_3_unfixed_reference", "epsilon_Bv_unfixed_reference", "MISSING_SOURCE_BACKED_UPPER_BOUND", "conditional selector only; staged by 3003"),
        ("REB3005_4_projector_boundary", "epsilon_Bv_projector_boundary", "MISSING_SOURCE_BACKED_UPPER_BOUND", "conditional chain-map/silence route only; staged by 3004"),
        ("REB3005_5_denominator", "M_ref_or_M_H_ref", "MISSING_POSITIVE_SAME_FRAME_MHREF", "3005 consolidates denominator ownership as not derived; acquisition rows staged"),
        ("REB3005_6_Bv_envelope", "epsilon_Bv_ambiguity_abs_envelope", "NOT_SCOREABLE", "Bv cannot be numerically scored without numerator rows plus source-backed denominator"),
        ("REB3005_7_kernel", "epsilon_kernel_charge_public_SRNG_rebased_3005", "MISSING_THETA_PARENT_QV_BV_REMAINDER_CV_ZERO_FLUX_MREF", "full kernel charge remains open"),
    ]
    return [
        base({"rebase_id": rebase_id, "symbol": symbol, "current_value": current_value, "status": status})
        for rebase_id, symbol, current_value, status in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE3005_0_sources", "3005 source anchors exist", "PASS", True, False, "all required source anchors are present"),
        ("GATE3005_1_denominator_owned", "positive same-frame M_ref/M_H_ref exists", "BLOCKED_NONCLAIM", False, False, "H_tau/H_ref/M_H_ref, theta, Q_tau, surfaces, tau and integrability are missing"),
        ("GATE3005_2_orbital_GM_rejected", "observed orbital GM imported as denominator", "REJECTED_SHORTCUT_PASS", True, False, "orbital GM is downstream test/readout, not denominator proof input"),
        ("GATE3005_3_Bv_scoreable", "Bv residual envelope is scoreable", "FAIL_CLOSED", False, False, "claim-valid numerator rows and denominator row are absent"),
        ("GATE3005_4_full_Bv_zero", "epsilon_Bv_ambiguity=0", "FAIL_CLOSED", False, False, "residual components and denominator remain open"),
        ("GATE3005_5_local_claims", "local GR/Newton/PPN/WEP/R10 claim allowed", "FAIL_CLOSED", False, False, "parent Hamiltonian/source charge bridge remains upstream"),
    ]
    return [
        base(
            {
                "gate_id": gate_id,
                "gate": gate,
                "gate_status": gate_status,
                "condition_passed": condition_passed,
                "promotion_allowed_now": promotion_allowed_now,
                "reason": reason,
            }
        )
        for gate_id, gate, gate_status, condition_passed, promotion_allowed_now, reason in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DEC3005_0_conditional_route",
            "Keep the denominator theorem as a strict conditional route.",
            "If theta_MTS, Q_tau, H_tau integrability, fixed H_ref, same frame, fixed surfaces and positivity are all parent-signed, M_H_ref can normalize Bv rows.",
            "retain as parent-action requirement, not current theorem",
        ),
        (
            "DEC3005_1_no_denominator_value",
            "Do not assign M_ref/M_H_ref a live value.",
            "No source-backed positive same-frame H_tau-H_ref value or theorem exists; observed GM would be circular.",
            "denominator acquisition rows remain nonclaim",
        ),
        (
            "DEC3005_2_no_score",
            "Do not score the Bv envelope.",
            "A denominator alone would not close numerator rows, and current denominator is also missing.",
            "Bv envelope remains explicit residual closure",
        ),
        (
            "DEC3005_3_next",
            "Move upstream to parent theta/Q_tau/H_tau extraction.",
            "The denominator cannot be derived until the parent Hamiltonian current owner is derived.",
            "3006 should attack theta_MTS/Q_tau/H_tau from the parent action or stage sector charge owner rows",
        ),
    ]
    return [
        base({"decision_id": decision_id, "decision": decision, "rationale": rationale, "next_effect": next_effect})
        for decision_id, decision, rationale, next_effect in data
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "next_id": "NEXT3005_0_3006",
                "priority": "selected_primary",
                "target_doc": "3006-Y5-R2FR-parent-theta-Qtau-Htau-extraction-or-Hamiltonian-current-owner-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_parent_theta_Qtau_Htau_extraction_or_Hamiltonian_current_owner_under_AX1090_3006.py",
                "mission": "Attack the upstream parent Hamiltonian-current owner: derive theta_MTS, Q_tau^MTS and H_tau from the parent action/sector ledger, or stage sector-by-sector charge owner rows with source paths and no EH-only import.",
                "success_condition": "theta_MTS/Q_tau/H_tau become parent-signed enough to feed M_H_ref, or a complete nonclaim sector-charge acquisition ledger is produced",
                "fallback_if_fail": "keep M_ref/M_H_ref denominator as explicit closure-only and move to minimal parent action sector grammar",
                "guardrails": "no EH-only charge import; no orbital-GM denominator; no full Bv zero claim; no epsilon_kernel_charge claim; no local-GR/Newton/PPN/WEP/R10 claim; no GitHub; no formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "copy_id": copy_id,
                "path": str(path),
                "path_exists": path.exists(),
                "row_count": len(rows(path)),
                "csv_parse_ok": csv_ok(path),
                "claim_flags_present": any(boolish(row.get("valid_for_claim")) or boolish(row.get("claim_allowed")) for row in rows(path)),
            }
        )
        for copy_id, path in BRANCH_OUTPUTS.items()
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    denominators: list[dict[str, Any]],
    scoreability: list[dict[str, Any]],
    rebase: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    generated_rows = sources + audit + denominators + scoreability + rebase + gates + decisions + next_target + branches
    targeted_formalization_hits = []
    if FORMALIZATION.exists():
        patterns = [
            "*Y5_R2FR_3005*",
            "*3005-Y5-R2FR*",
            "*Mref_denominator_ownership_3005*",
            "*Bv_envelope_scoreability_rows_3005*",
            "*JR3005_PARENT_THETA_QTAU_HTAU*",
        ]
        for pattern in patterns:
            targeted_formalization_hits.extend(FORMALIZATION.rglob(pattern))

    allowed_non_numeric_values = {"GUARDRAIL_INSTALLED_NONCLAIM", "NOT_COMPUTED", "NOT_SCOREABLE", "0"}
    checks = [
        ("VAL3005_00_sources_exist", all(boolish(row["path_exists"]) for row in sources), "every cited source path exists", True),
        ("VAL3005_01_source_anchors", all(boolish(row["anchors_found"]) for row in sources), "every source has required anchors", True),
        ("VAL3005_02_denominator_not_promoted", any(row["audit_id"] == "MDA3005_11_verdict" for row in audit) and not any(boolish(row["finite_denominator_now"]) for row in audit), "denominator ownership remains not derived", True),
        ("VAL3005_03_missing_denominator_clauses", all(expected in {row["current_status"] for row in audit} for expected in {"MISSING_THETA_QTAU_PARENT_SOURCE", "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO", "MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO", "MISSING_POSITIVE_SAME_FRAME_MHREF", "MISSING_SURFACE_HOMOLOGY_LOCK", "MISSING_HILBERT_TO_HTAU_MAP"}), "denominator audit preserves missing parent/source clauses", True),
        ("VAL3005_04_denominator_rows_nonclaim", len(denominators) == 12 and all(not boolish(row["valid_for_claim"]) and not boolish(row["claim_allowed"]) for row in denominators), "denominator acquisition rows are staged and nonclaim", True),
        ("VAL3005_05_no_finite_denominator_fabricated", all(str(row.get("current_value", "")).startswith("MISSING") or str(row.get("current_value", "")) in allowed_non_numeric_values for row in denominators), "no finite M_ref/M_H_ref value fabricated", True),
        ("VAL3005_06_Bv_score_blocked", len(scoreability) == 7 and any(row["scoreability_status"] == "NO_BV_SCORE_ALLOWED" for row in scoreability), "Bv envelope remains not scoreable", True),
        ("VAL3005_07_local_claims_blocked", all(row["promotion_allowed_now"] is False for row in gates), "no local GR/Newton/PPN/WEP/R10 promotion allowed", True),
        ("VAL3005_08_next_target_theta_Qtau", len(next_target) == 1 and "theta_MTS" in next_target[0]["mission"] and "Q_tau" in next_target[0]["mission"], "3006 selects parent theta/Q_tau/H_tau extraction next", True),
        ("VAL3005_09_branch_copies", len(branches) == 3 and all(boolish(row["path_exists"]) and boolish(row["csv_parse_ok"]) for row in branches) and not any(boolish(row["claim_flags_present"]) for row in branches), "branch copies exist, parse, and carry no claim flags", True),
        ("VAL3005_10_csv_parse", all(csv_ok(path) for path in OUTPUTS.values() if path.suffix == ".csv"), "all 3005 CSV outputs parse cleanly", True),
        ("VAL3005_11_paths_under_post_checkpoint", all(under(path, ROOT) for path in output_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL3005_12_formalization_untouched", len(targeted_formalization_hits) == 0, "no targeted 3005 files exist under formalization-workbench", True),
        ("VAL3005_13_no_claim_flags", not any(boolish(row.get("valid_for_claim")) or boolish(row.get("claim_allowed")) for row in generated_rows), "all generated rows remain valid_for_claim=false and claim_allowed=false", True),
    ]
    preliminary = [
        base({"validation_id": validation_id, "passed": passed, "detail": detail, "required": required})
        for validation_id, passed, detail, required in checks
    ]
    overall = all(boolish(row["passed"]) for row in preliminary if boolish(row["required"]))
    preliminary.append(
        base(
            {
                "validation_id": "VAL3005_OVERALL",
                "passed": overall,
                "detail": "3005 refuses M_ref/M_H_ref denominator promotion, blocks Bv envelope scoring, and selects parent theta/Q_tau/H_tau extraction next",
                "required": True,
            }
        )
    )
    return preliminary


def write_doc(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    denominators: list[dict[str, Any]],
    scoreability: list[dict[str, Any]],
    rebase: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# 3005 - Y5/R2FR Mref Denominator Ownership Or Bv Envelope Scoreability Under AX1090

Status: `Y5_R2FR_3005_Mref_MHref_denominator_not_promoted_Bv_envelope_not_scoreable_3006_next`

Generated: `{RUN_UTC}`

## Current Verdict

3005 attacks the common denominator problem: `M_ref` or `M_H_ref` must be a positive same-frame parent Hamiltonian/source charge, not a number borrowed from observed orbital `GM`.

The exact route is clear. If the parent action supplies `theta_MTS`, `Q_tau^MTS`, an integrable `H_tau`, a fixed `H_ref`, one observed `q/e_obs/tau` branch, fixed source worldtube/surfaces, and a positive finite `H_tau[S_outer]-H_ref`, then `M_H_ref` can normalize the Bv residual envelope.

Current MTS does not yet sign that stack. So 3005 refuses the denominator value and refuses to score `epsilon_Bv_ambiguity_abs_envelope`. This is annoying but healthy: the denominator is now explicitly upstream of parent Hamiltonian-current ownership rather than silently imported from Newtonian readout.

## Source Register

{md_table(sources, ["source_id", "path_exists", "anchors_found", "missing_anchors", "role"])}

## M_ref / M_H_ref Ownership Audit

{md_table(audit, ["audit_id", "denominator_clause", "current_status", "failure_mode", "source_anchors"])}

## Denominator Acquisition Rows

{md_table(denominators, ["denominator_id", "symbol", "definition", "units", "current_value", "source_anchors"])}

## Bv Envelope Scoreability Rows

{md_table(scoreability, ["score_id", "quantity", "current_value", "denominator_status", "scoreability_status", "claim_blocker"])}

## Bv Rebase After 3005

{md_table(rebase, ["rebase_id", "symbol", "current_value", "status"])}

## Promotion Gates

{md_table(gates, ["gate_id", "gate", "gate_status", "condition_passed", "promotion_allowed_now", "reason"])}

## Decision Ledger

{md_table(decisions, ["decision_id", "decision", "rationale", "next_effect"])}

## Next Target

{md_table(next_target, ["next_id", "target_doc", "mission", "success_condition", "guardrails"])}

## Branch Copies

{md_table(branches, ["copy_id", "path", "path_exists", "row_count", "csv_parse_ok", "claim_flags_present"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "required"])}

## Plain-English Takeaway

This is a boring-looking but high-value gate. If we let `M_ref` be measured `GM`, the theory can accidentally use Newton to prove Newton. 3005 says no: first derive the Hamiltonian/source charge from the parent action, then use observed `GM` only as a test of the bridge. The next fight is therefore not another boundary residual; it is the parent `theta_MTS/Q_tau/H_tau` owner.

## Forbidden Claims From 3005

- `M_ref` or `M_H_ref` has a finite sourced value.
- `M_H_ref=H_tau-H_ref` is positive same-frame in current MTS.
- Observed orbital `GM` can define the denominator.
- `epsilon_Bv_ambiguity_abs_envelope` is scoreable.
- `epsilon_Bv_ambiguity=0`.
- `epsilon_kernel_charge_public_SRNG=0`.
- Local GR/Newton/PPN/WEP/R10 pass.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    sources = source_rows()
    audit = audit_rows()
    denominators = denominator_rows()
    scoreability = scoreability_rows()
    rebase = rebase_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["denominators"], denominators)
    write_csv(OUTPUTS["scoreability"], scoreability)
    write_csv(OUTPUTS["rebase"], rebase)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    shutil.copyfile(OUTPUTS["audit"], BRANCH_OUTPUTS["audit_copy"])
    shutil.copyfile(OUTPUTS["scoreability"], BRANCH_OUTPUTS["score_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)
    validation = validation_rows(sources, audit, denominators, scoreability, rebase, gates, decisions, next_target, branches)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, audit, denominators, scoreability, rebase, gates, decisions, next_target, branches, validation)

    overall = next(row for row in validation if row["validation_id"] == "VAL3005_OVERALL")
    if not boolish(overall["passed"]):
        raise SystemExit("3005 validation failed; see P8_Y5_BRR545_3005_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"validation {overall['passed']}: {overall['detail']}")


if __name__ == "__main__":
    main()
