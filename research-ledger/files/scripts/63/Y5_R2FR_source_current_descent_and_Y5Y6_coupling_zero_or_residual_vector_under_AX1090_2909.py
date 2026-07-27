from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2909-Y5-R2FR-source-current-descent-and-Y5Y6-coupling-zero-or-residual-vector-under-AX1090.md"

SRC_2908_DOC = ROOT / "2908-Y5-R2FR-minimal-parent-action-skeleton-for-q_loc-source-bridge-and-Y5Y6-coupling-under-AX1090.md"
SRC_2908_NEXT = RESIDUALS / "P8_Y5_R2FR_2908_NEXT_TARGET.csv"
SRC_2908_COUPLING = RESIDUALS / "P8_Y5_R2FR_2908_Y5Y6_COUPLING_OWNER_AUDIT.csv"
SRC_2908_VARIATION = RESIDUALS / "P8_Y5_R2FR_2908_VARIATION_AND_QLOC_DERIVATION.csv"
SRC_1620_DOC = ROOT / "1620-Y5-R2FR-parent-signature-map-and-source-current-zero-or-q_loc-bound-fill.md"
SRC_1620_CHAIN = RESIDUALS / "P8_Y5_PARENT_QLOC_1620_CHAIN_RULE_SOURCE_CURRENT_ZERO_ATTEMPT.csv"
SRC_1620_BRIDGE = RESIDUALS / "P8_Y5_PARENT_QLOC_1620_PARENT_SIGNATURE_BRIDGE_CONTRACT.csv"
SRC_1620_BOUNDS = RESIDUALS / "P8_Y5_PARENT_QLOC_1620_SOURCE_CURRENT_BOUND_FILL_ROWS.csv"
SRC_1574_PREMISE = RESIDUALS / "P8_Y5_PARENT_QLOC_1574_RAB_MATTER_DESCENT_PREMISE_MATRIX.csv"
SRC_1575_VERTICAL = RESIDUALS / "P8_Y5_PARENT_QLOC_1575_RAB_VERTICAL_GENERATOR_SIGNATURE_ATTEMPT.csv"
SRC_1575_DESCENT = RESIDUALS / "P8_Y5_PARENT_QLOC_1575_RAB_MATTER_DESCENT_SIGNATURE.csv"
SRC_1086_SOURCE_CURRENT = RESIDUALS / "P8_Y5_R10_1086_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv"
SRC_1415_OWNER = RESIDUALS / "P8_Y5_R10_1415_SOURCE_CURRENT_OWNER_ATTEMPT.csv"
SRC_1416_BAN = RESIDUALS / "P8_Y5_R10_1416_SOURCE_SLOT_CURRENT_RESCALING_BAN_ATTEMPT.csv"
SRC_992_DESCENT = RESIDUALS / "P8_Y5_R10_992_SOURCE_CURRENT_DESCENT_THEOREM_GATE.csv"
SRC_2611_CHAIN = RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_CHAIN_RULE_DECOMPOSITION.csv"
SRC_2611_PREMISE = RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv"
SRC_2611_WORLD = RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_MATTER_WORLDTUBE_DESCENT_ATTEMPT.csv"
SRC_2612_DIRECT = RESIDUALS / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_DIRECT_VERTEX_AND_NO_MARKER_AUDIT.csv"
SRC_2643_GATE = RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_PARENT_SIGNATURE_THEOREM_GATE.csv"
SRC_2643_LEAKS = RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_DQZ_JH_LEAK_BOUND_ROWS.csv"
SRC_2643_ARENA = RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_ARENA_LEAK_MAP.csv"
SRC_2643_NEXT = RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_NEXT_TARGET.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2909_SOURCE_REGISTER.csv",
    "proof": RESIDUALS / "P8_Y5_R2FR_2909_SOURCE_CURRENT_DESCENT_PROOF_ATTEMPT.csv",
    "coupling": RESIDUALS / "P8_Y5_R2FR_2909_Y5Y6_COUPLING_ZERO_AUDIT.csv",
    "residuals": RESIDUALS / "P8_Y5_R2FR_2909_SOURCE_CURRENT_Y5Y6_RESIDUAL_VECTOR.csv",
    "arenas": RESIDUALS / "P8_Y5_R2FR_2909_ARENA_LEAK_MAP.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2909_RUNNER_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2909_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2909_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2909_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2909_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2909_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "proof_copy": RAB_QUEUE / "JR2909_SOURCE_CURRENT_DESCENT_PROOF_ATTEMPT_NONCLAIM.csv",
    "residual_copy": LOCAL_BOUNDS / "Source_current_Y5Y6_residual_vector_2909_NONCLAIM.csv",
    "next_copy": PARENT_ACTION / "Qvis_no_source_slot_or_finite_vector_next_2909_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2909_00_2908_doc", SRC_2908_DOC, "NEXT2908_0_2909;source-current descent and Y5/Y6 coupling zero", "handoff selecting source-current/Y5Y6 proof"),
        ("SRC2909_01_2908_next", SRC_2908_NEXT, "NEXT2908_0_2909;J_M is the parent Hilbert/worldtube source current", "machine-readable 2909 target"),
        ("SRC2909_02_2908_coupling", SRC_2908_COUPLING, "CPL2908_2_JM_source_current;CPL2908_3_JZ_source_zero;CPL2908_TOTAL", "Y5/Y6 coupling owner audit"),
        ("SRC2909_03_2908_variation", SRC_2908_VARIATION, "VAR2908_0_delta_A_q_loc;VAR2908_3_delta_matter_source;VAR2908_7_verdict", "q_loc variation and matter source gap"),
        ("SRC2909_04_1620_doc", SRC_1620_DOC, "`J_Z=0` follows by exact chain rule;Current MTS does not yet satisfy those premises", "prior source-current zero verdict"),
        ("SRC2909_05_1620_chain", SRC_1620_CHAIN, "CR1620_1_zero_lemma;CR1620_5_verdict", "exact conditional J_Z chain-rule lemma"),
        ("SRC2909_06_1620_bridge", SRC_1620_BRIDGE, "BRC1620_0_Z_map;BRC1620_6_verdict", "parent signature bridge clauses"),
        ("SRC2909_07_1620_bounds", SRC_1620_BOUNDS, "SCB1620_0_JZ_bulk;SCB1620_4_PPN_source_lock", "source-current fallback bound rows"),
        ("SRC2909_08_1574_premise", SRC_1574_PREMISE, "RPM1574_0_R_vertical;RPM1574_5_verdict", "matter descent premise matrix"),
        ("SRC2909_09_1575_vertical", SRC_1575_VERTICAL, "VERT1575_1_generator;VERT1575_5_verdict", "vertical generator signature"),
        ("SRC2909_10_1575_descent", SRC_1575_DESCENT, "MDS1575_0_action_form;MDS1575_5_verdict", "matter descent signature"),
        ("SRC2909_11_1086_source_current", SRC_1086_SOURCE_CURRENT, "SCZ1086_1_Hilbert_current_owner;SCZ1086_5_verdict", "source-current zero theorem attempt"),
        ("SRC2909_12_1415_owner", SRC_1415_OWNER, "SCO1415_1_object_language;SCO1415_6_verdict", "source-current owner attempt"),
        ("SRC2909_13_1416_ban", SRC_1416_BAN, "BAN1416_1_locality_covariance;BAN1416_6_verdict", "source-slot current rescaling ban attempt"),
        ("SRC2909_14_992_descent", SRC_992_DESCENT, "SCD992_2_Hilbert_current_definition;SCD992_6_verdict", "Hamiltonian/PiM source-current descent gate"),
        ("SRC2909_15_2611_chain", SRC_2611_CHAIN, "CR2611_0_variation_identity;CR2611_6_direct_vertex", "six-term matter descent decomposition"),
        ("SRC2909_16_2611_premise", SRC_2611_PREMISE, "PRE2611_0_q_map;PRE2611_8_verdict", "matter descent premise audit"),
        ("SRC2909_17_2611_world", SRC_2611_WORLD, "MWD2611_1_conditional_theorem;MWD2611_4_current_verdict", "matter/worldtube descent attempt"),
        ("SRC2909_18_2612_direct", SRC_2612_DIRECT, "DV2612_1_wA;DV2612_5_verdict", "direct matter/source grammar audit"),
        ("SRC2909_19_2643_gate", SRC_2643_GATE, "QVIS2643_0_chain_rule_theorem;QVIS2643_6_verdict", "common descent DqZ/JH theorem gate"),
        ("SRC2909_20_2643_leaks", SRC_2643_LEAKS, "LEAK2643_0_eps_JH_Z_abs;LEAK2643_6_master_policy", "finite JH/DqZ leak rows"),
        ("SRC2909_21_2643_arena", SRC_2643_ARENA, "AM2643_0_Newton;AM2643_4_clock_EM", "arena leak map"),
        ("SRC2909_22_2643_next", SRC_2643_NEXT, "NEXT2643_0_selected;no direct Z slot", "older next route for Qvis grammar"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        anchors_found, missing_anchors = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": anchors_found,
                    "missing_anchors": missing_anchors,
                }
            )
        )
    return rows


def proof_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PROOF2909_0_JZ_chain_rule_identity",
            "J_Z",
            "delta_v S_matter = D Sbar[Dq(v)] + sum_a J_theta^a Lie_v theta_a + J_direct[v] + delta_v B",
            "If Dq(v_Z)=0, Lie_v theta=0, J_direct=0, and delta_v B=0/proper, then J_Z=0.",
            "EXACT_CONDITIONAL_THEOREM",
            "premises are not parent-signed for current MTS",
            SRC_1620_CHAIN,
        ),
        (
            "PROOF2909_1_JM_Hilbert_owner",
            "J_M^nu",
            "J_M is identified with the Hilbert/worldtube matter current only after S_matter descends through one public observed coframe and one current owner",
            "Then the current in the q_loc Euler equation is a physical source current, not fitted GM.",
            "CONDITIONAL_STANDARD_IDENTITY_NOT_PARENT_SIGNED",
            "object-language, current owner, source worldtube, Pi_M and readout product are missing",
            SRC_1415_OWNER,
        ),
        (
            "PROOF2909_2_external_vacuum",
            "J_M^nu local exterior",
            "If W_source=closure(supp J_H[tau]) is parent-owned and S_ext excludes W_source, then J_M=0 on S_ext up to explicit boundary tails",
            "Together with q_loc=P_loc J_M this gives local vacuum q_loc=0.",
            "CONDITIONAL_WORLDTUBE_LEMMA",
            "worldtube support, tau, J_H descent and boundary tails are unsigned",
            SRC_2611_WORLD,
        ),
        (
            "PROOF2909_3_no_source_slot",
            "source weights/direct vertices",
            "A no-source-slot object language must forbid w_A(Z)S_A, direct V_m[Z], hidden frames and marker/source weights",
            "Then source-current zero cannot be beaten by pre-action weights.",
            "COUNTERMODEL_SURVIVES",
            "locality/covariance/additivity do not ban pre-action source weights",
            SRC_1416_BAN,
        ),
        (
            "PROOF2909_4_DqZ_visible_descent",
            "Dq_Z and observed maps",
            "If Q_vis is parent-owned and v_Z in ker(Dq), observed coframe/source/readout derivatives vanish by chain rule",
            "DObs(v_Z)=0 and ordinary matter/source readouts cannot see Z.",
            "CHAIN_RULE_EXACT_OBSERVED_MAP_UNSIGNED",
            "q map, Z basis, source/readout functor and boundary/projector map are missing",
            SRC_2643_GATE,
        ),
        (
            "PROOF2909_5_JZ_application",
            "current MTS J_Z",
            "Apply PROOF2909_0 to current MTS residual basis",
            "Does not fire because verticality, matter descent, no-marker, direct-slot exclusion, boundary and PPN/source lock remain open.",
            "SOURCE_CURRENT_ZERO_NOT_DERIVED_CURRENT_MTS",
            "J_Z stays as residual row",
            SRC_1620_CHAIN,
        ),
        (
            "PROOF2909_6_JM_application",
            "current MTS J_M",
            "Apply Hilbert/worldtube owner theorem to the J_M in the 2908 q_loc action",
            "Does not fire because current MTS has not signed single public metric/current owner, worldtube support, Pi_M equality or no-source weights.",
            "JM_SOURCE_DESCENT_NOT_DERIVED_CURRENT_MTS",
            "J_M stays as residual row",
            SRC_2908_COUPLING,
        ),
        (
            "PROOF2909_7_verdict",
            "source-current descent",
            "The descent proof exists as exact conditional mathematics but is not a current-MTS theorem",
            "Use residual vector rows until Q_vis/no-source-slot/source-worldtube clauses are parent-signed.",
            "CONDITIONAL_THEOREM_CLOSED_APPLICATION_BLOCKED",
            "no local GR/Newton claim",
            SRC_2643_GATE,
        ),
    ]
    return [
        add_common(
            {
                "proof_id": proof_id,
                "target": target,
                "mathematical_statement": mathematical_statement,
                "would_prove": would_prove,
                "current_status": current_status,
                "blocking_gap": blocking_gap,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "theorem_closed_conditionally": current_status in {"EXACT_CONDITIONAL_THEOREM", "CONDITIONAL_WORLDTUBE_LEMMA"},
                "application_to_current_mts": False,
                "parent_signed": False,
            }
        )
        for proof_id, target, mathematical_statement, would_prove, current_status, blocking_gap, source_path in specs
    ]


def coupling_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "YCZ2909_0_Y5_GM_transfer",
            "epsilon_Y5_GM_transfer",
            "Y5 source normalization is owned only if J_M=J_H/worldtube current, Pi_M equality holds, and orbital GM is output not input",
            "BLOCKED_NONCLAIM",
            "J_M/PiM/worldtube equality is not parent-signed",
            SRC_2908_COUPLING,
        ),
        (
            "YCZ2909_1_Y5_mu_extra",
            "epsilon_Y5_mu_extra_vector",
            "Y5 extra source offsets vanish only if no-source-slot, no-marker, fixed constants, boundary silence and common metric clauses close",
            "BLOCKED_NONCLAIM",
            "direct matter/source grammar and boundary rows remain open",
            SRC_2611_PREMISE,
        ),
        (
            "YCZ2909_2_JZ_zero",
            "J_Z",
            "response-doublet source current is zero by chain rule only under DqZ=0, no-marker, no direct vertex and boundary silence",
            "EXACT_CONDITIONAL_NOT_APPLIED",
            "DqZ and object-language premises are unsigned",
            SRC_1620_CHAIN,
        ),
        (
            "YCZ2909_3_Y6_stress_zero",
            "epsilon_extra_odd_source_Y6",
            "Y6 stress is silent only if actual MTS residuals map to the positive normal form and J_Z/boundary sources vanish",
            "BLOCKED_NONCLAIM",
            "normal form exists but parent signature and metric stress map are not current theorems",
            SRC_2908_COUPLING,
        ),
        (
            "YCZ2909_4_projector_stress",
            "epsilon_Y6_projector_stress",
            "P_loc/Pi_M stress must be parent-owned, zero/exact, or source-bounded",
            "BLOCKED_NONCLAIM",
            "projector owner and Pi_M equality remain open",
            SRC_992_DESCENT,
        ),
        (
            "YCZ2909_5_boundary_flux",
            "epsilon_boundary_worldtube_flux",
            "bulk source-current descent does not remove boundary/worldtube flux",
            "BLOCKED_NONCLAIM",
            "boundary no-flux/proper-boundary theorem is not signed",
            SRC_1620_BOUNDS,
        ),
        (
            "YCZ2909_6_observable_lock",
            "epsilon_Y5Y6_observable_projection",
            "source-current zero must be locked to Newton, PPN, R10, WEP, clock and orbital observables with units",
            "BLOCKED_NONCLAIM",
            "arena projection rows are schemas with missing values",
            SRC_2643_ARENA,
        ),
        (
            "YCZ2909_7_verdict",
            "Y5Y6 coupling zero",
            "Y5/Y6 coupling-zero route remains alive but not promoted",
            "Y5Y6_ZERO_NOT_DERIVED_RESIDUAL_VECTOR_REQUIRED",
            "source-current descent application fails current-MTS parent signatures",
            SRC_2908_COUPLING,
        ),
    ]
    return [
        add_common(
            {
                "coupling_gate_id": coupling_gate_id,
                "symbol": symbol,
                "zero_condition": zero_condition,
                "current_status": current_status,
                "blocking_gap": blocking_gap,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "theorem_zero_adopted": False,
                "parent_signed": False,
                "accepted_for_scoring": False,
            }
        )
        for coupling_gate_id, symbol, zero_condition, current_status, blocking_gap, source_path in specs
    ]


def residual_rows() -> list[dict[str, Any]]:
    specs = [
        ("RES2909_0_JM_descent", "epsilon_JM_descent_abs", "failure of J_M to be the parent Hilbert/worldtube current in the q_loc Euler equation", "source-current-normalized", "MISSING_PARENT_SOURCE_CURRENT_DESCENT", SRC_2908_COUPLING, "Newton;source_mass;orbital;PPN"),
        ("RES2909_1_JZ_bulk", "J_Z", "bulk source current along the response-doublet/local residual direction", "action_variation_or_source_current_units", "MISSING_PARENT_DESCENT_OR_NUMERIC_BOUND", SRC_1620_BOUNDS, "PPN;R10;WEP;local_GR"),
        ("RES2909_2_DqZ", "Dq_Z_norm", "quotient derivative leakage of the residual direction into visible variables", "operator_norm", "MISSING_COMPUTABLE_Q_MAP_Z_BASIS_AND_NORMS", SRC_2643_LEAKS, "all_local_arenas"),
        ("RES2909_3_source_weight", "Delta_w_abs", "pre-action source-only species/current weight seam", "dimensionless", "PARENT_OBJECT_LANGUAGE_NO_SOURCE_SLOT_UNSIGNED", SRC_2643_LEAKS, "WEP;Newton_GM;PPN;R10"),
        ("RES2909_4_theta_marker", "epsilon_theta_marker", "material constants, EM/clock standards or marker labels change along Z", "source-normalized_or_arena_specific", "NO_MARKER_THEOREM_NOT_PARENT_SIGNED", SRC_2643_LEAKS, "WEP;clock;EM;R10;PPN"),
        ("RES2909_5_direct_vertex", "A_direct_matter", "direct matter/source/worldtube vertex depending on Z outside q", "action_variation_units", "MISSING_NO_DIRECT_MATTER_X_VERTEX_THEOREM", SRC_2612_DIRECT, "source_mass;WEP;PPN"),
        ("RES2909_6_boundary", "epsilon_boundary_worldtube_flux", "matter/worldtube/boundary flux under vertical variation", "flux_or_action_boundary_units", "MISSING_BOUNDARY_NOFLUX_OR_ABSOLUTE_TAIL_BOUND", SRC_2611_CHAIN, "clock;orbital;PPN;local_GR"),
        ("RES2909_7_Y5_GM", "epsilon_Y5_GM_transfer", "failure of parent source current/Pi_M/worldtube/orbital readout chain", "dimensionless_after_true_source_norm", "MISSING_JM_PIM_WORLDTUBE_EQUALITY", SRC_2908_COUPLING, "Newton;source_mass;PPN"),
        ("RES2909_8_Y5_mu", "epsilon_Y5_mu_extra_vector", "source-normalization offsets from nonEH/boundary/radial/time/species/calibration channels", "dimensionless_after_true_source_norm", "EIGHT_CHANNEL_MU_EXTRA_VECTOR_STILL_OPEN", SRC_2908_COUPLING, "Newton;PPN;R10;WEP"),
        ("RES2909_9_Y6_stress", "epsilon_extra_odd_source_Y6", "extra-stress channel that can survive source-current descent", "dimensionless_after_true_source_norm", "MISSING_Y6_STRESS_PARENT_SIGNATURE", SRC_2908_COUPLING, "Bianchi;PPN;local_GR"),
        ("RES2909_10_projector", "epsilon_Y6_projector_stress", "projector/readout stress and Pi_M variation leakage", "dimensionless_source_stress_leakage", "MISSING_PROJECTOR_VARIATION_ZERO_OR_BOUND", SRC_2908_COUPLING, "source_mass;R11;PPN"),
        ("RES2909_11_observable", "epsilon_Y5Y6_observable_projection", "missing arena projection and units for q_loc/Z/Y5/Y6 residuals", "mixed_projection_units", "MISSING_OBSERVABLE_PROJECTION_AND_UNITS", SRC_2908_COUPLING, "PPN;R10;clock;orbital;Newton"),
        ("RES2909_TOTAL", "epsilon_source_current_Y5Y6_total", "absolute no-cancellation envelope over all source-current, Y5, Y6, boundary, projector and observable leaks", "dimensionless_gate", "COMPONENTS_MISSING", SRC_2908_COUPLING, "PPN;R10;clock;orbital;Newton;local_GR"),
    ]
    return [
        add_common(
            {
                "residual_id": residual_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "current_value": current_value,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "observable_link": observable_link,
                "parent_signed": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for residual_id, symbol, definition, units, current_value, source_path, observable_link in specs
    ]


def arena_rows() -> list[dict[str, Any]]:
    specs = [
        ("ARENA2909_0_Newton", "Newton/GM/orbital", "Delta_GM <= Pi_GM(eps_JM + eps_JH_Z + E_DqZ_GM + source_weight + boundary)", "FITTED_GM_GUARD_ACTIVE", "common-mode GM theorem; source map; DqZ norm; orbital projection"),
        ("ARENA2909_1_PPN", "PPN gamma/beta/preferred-frame", "Delta_PPN <= Pi_PPN(eps_JM + eps_JH_Z + E_DqZ_PPN + b_g bridge + Y6 stress)", "SCHEMA_READY_VALUES_MISSING", "b_g, x_U, no-other-channel proof, PPN vector projection"),
        ("ARENA2909_2_WEP", "WEP/composition", "eta_AB <= Pi_WEP(Delta_w_abs + eps_theta_marker + E_DqZ_WEP + readout marker tail)", "NO_MARKER_AND_NO_SOURCE_SLOT_UNSIGNED", "object-language no-source-slot theorem or finite Delta_w vector"),
        ("ARENA2909_3_R10", "R10/contact/source-test", "alpha/lambda rows remain nonclaim unless finite principal symbol, source/test charge split and real bound curve exist", "STRICT_ALPHA_LAMBDA_REJECTED_FOR_CLAIM", "finite projection, source/test charge split, real bound curve"),
        ("ARENA2909_4_clock_EM", "clock/time/EM", "Delta_clock/alpha_EM <= Pi_theta(eps_theta_marker + E_DqZ_clock/EM + readout standard leak)", "THETA_MARKER_DESCENT_UNSIGNED", "theta ownership; EM/fine-structure readout map; clock standard quotient descent"),
    ]
    return [
        add_common(
            {
                "arena_id": arena_id,
                "arena": arena,
                "leak_path": leak_path,
                "current_status": current_status,
                "missing_inputs": missing_inputs,
                "source_path": str(SRC_2643_ARENA),
                "source_path_exists": SRC_2643_ARENA.exists(),
                "accepted_for_scoring": False,
            }
        )
        for arena_id, arena, leak_path, current_status, missing_inputs in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2909_0_sources", "SOURCE_CONTEXT_READY", "2908/1620/2611/2643 descent and Y5Y6 rows", 4, "source-current descent attempt is anchored"),
        ("RUN2909_1_JZ_theorem", "EXACT_CONDITIONAL_JZ_ZERO_LEMMA_RECORDED", "DqZ=0; theta silent; no direct source slot; boundary proper", 1, "chain-rule zero theorem exists conditionally"),
        ("RUN2909_2_JM_owner", "JM_HILBERT_OWNER_NOT_DERIVED", "single public metric/current owner; worldtube; Pi_M; no weights", 0, "J_M remains residual for current MTS"),
        ("RUN2909_3_Y5Y6", "Y5Y6_ZERO_NOT_DERIVED", "Y5 GM transfer; Y5 mu; J_Z; Y6 stress; projector; boundary", 0, "coupling-zero application does not close"),
        ("RUN2909_4_residual_vector", "RESIDUAL_VECTOR_STAGED_NONCLAIM", "epsilon_source_current_Y5Y6_total and component rows", 0, "fallback rows are explicit but unfilled"),
        ("RUN2909_5_next", "QVIS_NO_SOURCE_SLOT_SELECTED_NEXT", "Q_vis object-language/no-source-slot or finite vector validator", 0, "this is the narrowest missing premise upstream of J_M/J_Z"),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "status": status,
                "required_components": required_components,
                "components_evaluable": components_evaluable,
                "reason": reason,
                "runner_ready": False,
            }
        )
        for runner_id, status, required_components, components_evaluable, reason in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2909_0_chain_rule", "J_Z chain-rule zero theorem exists", "PASS_CONDITIONAL_THEOREM_ONLY", "exact if descent premises close", True),
        ("CG2909_1_JZ_current", "J_Z=0 for current MTS", "BLOCKED_NONCLAIM", "DqZ, no-marker, no-direct-slot, matter descent and boundary are unsigned", False),
        ("CG2909_2_JM_current", "J_M is the parent Hilbert/worldtube current", "BLOCKED_NONCLAIM", "source-current owner, worldtube, Pi_M and no source weights remain open", False),
        ("CG2909_3_Y5_zero", "Y5 source-normalization coupling is zero", "BLOCKED_NONCLAIM", "GM transfer and mu_extra channels remain open", False),
        ("CG2909_4_Y6_zero", "Y6 extra stress/source coupling is zero", "BLOCKED_NONCLAIM", "response-doublet parent signature, stress map and boundary remain open", False),
        ("CG2909_5_residual_vector_score", "source-current/Y5Y6 residual vector is score-ready", "BLOCKED_NONCLAIM", "component values, units and arena projections are missing", False),
        ("CG2909_6_local_GR_Newton", "local GR/Newton follows after 2909", "BLOCKED_NONCLAIM", "source-current descent application failed and residual vector is unfilled", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": gate_status,
                "reason": reason,
                "gate_pass": gate_pass,
                "accepted_for_local_gr": False,
            }
        )
        for gate_id, claim, gate_status, reason, gate_pass in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2909_0_theorem_kept", "KEEP_CHAIN_RULE_SOURCE_CURRENT_ZERO_THEOREM", "J_Z=0 is exact conditional mathematics, not vibes", "use as proof contract"),
        ("DEC2909_1_application_blocked", "DO_NOT_PROMOTE_JM_OR_JZ", "current MTS does not sign Q_vis/DqZ/matter descent/no-marker/boundary/worldtube clauses", "local GR/Newton remains blocked"),
        ("DEC2909_2_residual_vector", "STAGE_SOURCE_CURRENT_Y5Y6_RESIDUAL_VECTOR", "every surviving source/coupling leak is now explicit and no-cancellation", "future tests can bound, not hide, the couplings"),
        ("DEC2909_3_next", "QVIS_OBJECT_LANGUAGE_NO_SOURCE_SLOT_SELECTED", "no-source-slot grammar is the shortest upstream route to close both J_M and J_Z", "29010/2910 should try Q_vis grammar or finite vector validator"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "effect": effect,
            }
        )
        for decision_id, decision, reason, effect in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2909_0_2910",
                "selection_status": "selected_primary",
                "target_file": "2910-Y5-R2FR-Qvis-object-language-no-source-slot-or-finite-JH-DqZ-Y5Y6-vector-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_Qvis_object_language_no_source_slot_or_finite_JH_DqZ_Y5Y6_vector_under_AX1090_2910.py",
                "task": "try to parent-sign the Q_vis object-language rule: ordinary matter/readouts are functors of visible quotient data only, with no direct Z slot, no source-only weights, no marker theta leakage and source/readout descent",
                "success_condition": "Q_vis grammar makes DqZ/JH leaks, no-source-slot seams, J_M/J_Z source-current leaks and Y5/Y6 source couplings theorem-zero in one branch",
                "fallback_condition": "build finite JH/DqZ/Y5Y6 residual vector validator with units and arena projection placeholders left nonclaim",
                "guardrails": "no empirical scoring; no source-weight absorption into G_N; no invented no-marker axiom; no MHref retry; no local-GR/Newton claim; no GitHub; no formalization-workbench edits",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    specs = [
        ("BR2909_0_proof_copy", OUTPUTS["proof"], BRANCH_OUTPUTS["proof_copy"], "RAB queue copy of source-current descent proof attempt"),
        ("BR2909_1_residual_copy", OUTPUTS["residuals"], BRANCH_OUTPUTS["residual_copy"], "local-bounds copy of source-current/Y5Y6 residual vector"),
        ("BR2909_2_next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"], "parent-action copy of 2910 Qvis/no-source-slot target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in specs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def formalization_touched() -> bool:
    if not FORMALIZATION.exists():
        return False
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for candidate in FORMALIZATION.rglob("*"):
        try:
            if candidate.is_file() and candidate.stat().st_mtime >= start_timestamp:
                return True
        except OSError:
            return True
    return False


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows_data = all_rows["sources"]
    proof_rows_data = all_rows["proof"]
    coupling_rows_data = all_rows["coupling"]
    residual_rows_data = all_rows["residuals"]
    arena_rows_data = all_rows["arenas"]
    runner_rows_data = all_rows["runner"]
    claim_rows_data = all_rows["claims"]
    next_rows_data = all_rows["next"]
    branch_rows_data = all_rows["branches"]
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    required_residuals = {
        "epsilon_JM_descent_abs",
        "J_Z",
        "Dq_Z_norm",
        "Delta_w_abs",
        "epsilon_theta_marker",
        "A_direct_matter",
        "epsilon_boundary_worldtube_flux",
        "epsilon_Y5_GM_transfer",
        "epsilon_Y5_mu_extra_vector",
        "epsilon_extra_odd_source_Y6",
        "epsilon_Y6_projector_stress",
        "epsilon_Y5Y6_observable_projection",
        "epsilon_source_current_Y5Y6_total",
    }
    found_residuals = {row["symbol"] for row in residual_rows_data}
    checks = [
        ("VAL2909_0_sources_exist", all(row["path_exists"] for row in source_rows_data), "all registered source paths exist"),
        ("VAL2909_1_source_anchors", all(row["anchors_found"] for row in source_rows_data), "all registered source anchors were found"),
        ("VAL2909_2_proof_rows_complete", len(proof_rows_data) == 8 and any(row["proof_id"] == "PROOF2909_7_verdict" for row in proof_rows_data), "source-current proof attempt has all clauses"),
        ("VAL2909_3_chain_rule_conditional", any(row["proof_id"] == "PROOF2909_0_JZ_chain_rule_identity" and row["theorem_closed_conditionally"] for row in proof_rows_data), "J_Z chain-rule theorem is recorded as conditional"),
        ("VAL2909_4_application_not_promoted", all(not row["application_to_current_mts"] and not row["parent_signed"] for row in proof_rows_data), "proof rows do not promote current-MTS claim"),
        ("VAL2909_5_coupling_audit_complete", len(coupling_rows_data) == 8 and any(row["coupling_gate_id"] == "YCZ2909_7_verdict" for row in coupling_rows_data), "Y5/Y6 coupling-zero audit is complete"),
        ("VAL2909_6_residual_symbols_present", required_residuals <= found_residuals, "source-current/Y5Y6 residual symbols are present"),
        ("VAL2909_7_residual_rows_nonclaim", all(not row["valid_for_claim"] and not row["accepted_for_scoring"] for row in residual_rows_data), "residual vector remains non-score-ready and nonclaim"),
        ("VAL2909_8_arena_map_complete", len(arena_rows_data) == 5 and all(not row["accepted_for_scoring"] for row in arena_rows_data), "arena leak map covers Newton/PPN/WEP/R10/clock_EM and remains nonclaim"),
        ("VAL2909_9_runner_refuses_claim", any(row["runner_id"] == "RUN2909_4_residual_vector" and row["status"] == "RESIDUAL_VECTOR_STAGED_NONCLAIM" for row in runner_rows_data), "runner stages residual vector rather than claim"),
        ("VAL2909_10_claim_gates_safe", all(not row["claim_allowed"] for row in claim_rows_data) and any(row["gate_id"] == "CG2909_6_local_GR_Newton" and row["gate_status"] == "BLOCKED_NONCLAIM" for row in claim_rows_data), "claim gates keep local GR/Newton blocked"),
        ("VAL2909_11_next_target_2910", any(row["route_id"] == "NEXT2909_0_2910" and row["selected"] for row in next_rows_data), "2910 Qvis/no-source-slot target selected"),
        ("VAL2909_12_branch_copies_exist", all(row["exists"] for row in branch_rows_data), "branch copies were written"),
        ("VAL2909_13_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs), "all generated CSV outputs parse cleanly"),
        ("VAL2909_14_formalization_untouched_during_run", not formalization_touched(), "formalization-workbench was not touched during this run"),
    ]
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL2909_OVERALL", overall, "2909 validation overall"))
    return [
        {
            "check_id": check_id,
            "passed": passed,
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "/")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def write_doc(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2909 - Y5 R2FR Source-Current Descent and Y5Y6 Coupling Zero or Residual Vector Under AX1090",
        "",
        f"Run: `runs/{SCRIPT_START_UTC.strftime('%Y%m%d-%H%M%S')}-Y5-R2FR-source-current-descent-and-Y5Y6-coupling-zero-or-residual-vector-under-AX1090`",
        "Status: `Y5_R2FR_2909_source_current_descent_exact_conditional_application_blocked_residual_vector_staged_2910_next`",
        "Claim ceiling: `source_current_descent_residual_vector_nonclaim_only_no_JM_owner_no_JZ_zero_no_Y5Y6_zero_no_Newton_no_PPN_no_R10_no_local_GR_no_GitHub_claim`",
        "",
        "## Summary",
        "",
        "2909 tries the proof route first. The clean result is that the `J_Z=0` theorem is real as conditional mathematics: matter variation along a residual direction splits into quotient, constants/markers, direct vertices and boundary terms, and it vanishes if all those terms are zero.",
        "",
        "The current MTS corpus still does not fire the theorem. `Dq[Z]=0`, matter descent, no pre-action source weights, no marker/theta leakage, boundary silence, worldtube ownership, and the Newton/PPN/R10 observable lock remain unsigned.",
        "",
        "So this checkpoint does not kill the programme; it names the source bill. The `q_loc` action route from 2908 is still useful, but `J_M`, `J_Z`, Y5 source normalization and Y6 extra stress now sit in a single non-cancellation residual vector until the `Q_vis` object-language/no-source-slot theorem is signed.",
        "",
        "## Source Register",
        "",
        md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## Source-Current Descent Proof Attempt",
        "",
        md_table(all_rows["proof"], ["proof_id", "target", "current_status", "mathematical_statement", "would_prove", "blocking_gap", "valid_for_claim"]),
        "",
        "## Y5/Y6 Coupling Zero Audit",
        "",
        md_table(all_rows["coupling"], ["coupling_gate_id", "symbol", "zero_condition", "current_status", "blocking_gap", "valid_for_claim"]),
        "",
        "## Source-Current Y5/Y6 Residual Vector",
        "",
        md_table(all_rows["residuals"], ["residual_id", "symbol", "definition", "units", "current_value", "observable_link", "valid_for_claim"]),
        "",
        "## Arena Leak Map",
        "",
        md_table(all_rows["arenas"], ["arena_id", "arena", "leak_path", "current_status", "missing_inputs", "valid_for_claim"]),
        "",
        "## Runner Status",
        "",
        md_table(all_rows["runner"], ["runner_id", "status", "required_components", "components_evaluable", "reason", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(all_rows["claims"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(all_rows["decision"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(all_rows["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(all_rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(all_rows["validation"], ["check_id", "passed", "detail", "generated_utc"]),
        "",
        "## Working Read",
        "",
        "This is the right sort of failure: not vague, not fatal, and not cosmetic. The source-current zero proof exists, but the object-language/no-source-slot signature is the lock. If 2910 can show ordinary matter and readouts are functors of `Q_vis` only, then `J_M/J_Z` can start collapsing into theorem-zero rows. If not, the residual vector is ready to become the honest local-test interface.",
        "",
        "## Forbidden Claims From 2909",
        "",
        "- `J_M` is the current MTS parent Hilbert/worldtube source current.",
        "- `J_Z=0` is proved for current MTS.",
        "- Y5 source normalization or Y6 extra stress is theorem-zero.",
        "- The residual vector is score-ready or numeric.",
        "- Source-normalized Newton, PPN, R10, clock, orbital or local GR is proved.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {}
    all_rows["sources"] = source_register_rows()
    all_rows["proof"] = proof_rows()
    all_rows["coupling"] = coupling_rows()
    all_rows["residuals"] = residual_rows()
    all_rows["arenas"] = arena_rows()
    all_rows["runner"] = runner_rows()
    all_rows["claims"] = claim_gate_rows()
    all_rows["decision"] = decision_rows()
    all_rows["next"] = next_rows()

    for key in ["sources", "proof", "coupling", "residuals", "arenas", "runner", "claims", "decision", "next"]:
        write_csv(OUTPUTS[key], all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_doc(all_rows)

    overall = next(row["passed"] for row in all_rows["validation"] if row["check_id"] == "VAL2909_OVERALL")
    print(f"2909 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()
