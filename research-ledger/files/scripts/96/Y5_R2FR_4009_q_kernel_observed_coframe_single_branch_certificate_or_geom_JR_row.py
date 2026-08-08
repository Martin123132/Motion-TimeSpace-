from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4009"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4009-Y5-R2FR-q-kernel-observed-coframe-single-branch-certificate-or-geom-JR-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4009_SOURCE_REGISTER.csv",
    "q_attempt": SRC / "P8_Y5_R2FR_4009_Q_KERNEL_ATTEMPT.csv",
    "coframe": SRC / "P8_Y5_R2FR_4009_OBSERVED_COFRAME_DESCENT_CERTIFICATE.csv",
    "geom": SRC / "P8_Y5_R2FR_4009_GEOM_JR_ROWS.csv",
    "branch": SRC / "P8_Y5_R2FR_4009_SINGLE_BRANCH_GATE.csv",
    "cases": SRC / "P8_Y5_R2FR_4009_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4009_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4009_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4009_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4009_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4009_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4009_VALIDATION.csv",
}

NEXT_DOC = "4010-Y5-R2FR-boundary-worldtube-nohair-or-JR-boundary-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4010_boundary_worldtube_nohair_or_JR_boundary_row.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4009_00_handoff", SRC / "P8_Y5_R2FR_4008_NEXT_TARGET.csv", "NEXT4008_0", "4008 handoff"),
        ("SRC4009_01_variation", SRC / "P8_Y5_R2FR_4008_NO_HOM_WEIGHT_REJECTION_PROOF.csv", "NOHOM4008_1_variation", "4008 variation formula"),
        ("SRC4009_02_jr_ord", SRC / "P8_Y5_R2FR_4008_JR_COEFFICIENT_PACK.csv", "JRCP4008_4_J_R_ord", "4008 J_R ordinary matter envelope"),
        ("SRC4009_03_q2570", SRC / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv", "DQ2570_3_RAB", "R_AB Dq ledger"),
        ("SRC4009_04_fsig", SRC / "P8_Y5_FIELD_QUOTIENT_2570_FIELD_SIGNATURE_ATTEMPT.csv", "FSIG2570_3_RAB_auxiliary", "R_AB field signature"),
        ("SRC4009_05_matter_descent", SRC / "P8_Y5_FIELD_QUOTIENT_2570_MATTER_DESCENT_GATE.csv", "MD2570_0_chain_rule", "matter chain rule"),
        ("SRC4009_06_qmap_public", SRC / "P8_EM_actual_q_map_vertical_basis_candidate.csv", "QMAP3517_0_public_geometry", "public geometry q map"),
        ("SRC4009_07_qmap_rab", SRC / "P8_EM_actual_q_map_vertical_basis_candidate.csv", "QMAP3517_7_RAB_auxiliary", "R_AB q map status"),
        ("SRC4009_08_q1270_full", SRC / "P8_Y5_R10_1270_RAB_QUOTIENT_SORT_DERIVATION_ATTEMPT.csv", "QSR1270_1_observed_full_metric", "full metric countermodel"),
        ("SRC4009_09_q1270_aux", SRC / "P8_Y5_R10_1270_RAB_QUOTIENT_SORT_DERIVATION_ATTEMPT.csv", "QSR1270_3_auxiliary_before_q", "auxiliary before q route"),
        ("SRC4009_10_dq1270_full", SRC / "P8_Y5_R10_1270_DQ_KERNEL_TEST_MATRIX.csv", "DQ1270_0_full_metric_readout", "Dq full readout fail"),
        ("SRC4009_11_dq1270_constraint", SRC / "P8_Y5_R10_1270_DQ_KERNEL_TEST_MATRIX.csv", "DQ1270_1_fixed_reciprocity_readout", "constraint readout"),
        ("SRC4009_12_route1270", SRC / "P8_Y5_R10_1270_RAB_ROUTE_SELECTION_AFTER_QUOTIENT_TEST.csv", "ROUTE1270_1_auxiliary_compatibility", "auxiliary route selected"),
        ("SRC4009_13_fmap_A", SRC / "P8_Y5_R10_1271_FIELD_BY_FIELD_QRAB_VR_MAP.csv", "FMAP1271_0_lapse_A", "lapse readout"),
        ("SRC4009_14_fmap_B", SRC / "P8_Y5_R10_1271_FIELD_BY_FIELD_QRAB_VR_MAP.csv", "FMAP1271_1_radial_B", "radial readout"),
        ("SRC4009_15_fmap_R", SRC / "P8_Y5_R10_1271_FIELD_BY_FIELD_QRAB_VR_MAP.csv", "FMAP1271_2_RAB", "R_AB field map"),
        ("SRC4009_16_fmap_matter", SRC / "P8_Y5_R10_1271_FIELD_BY_FIELD_QRAB_VR_MAP.csv", "FMAP1271_7_matter_action", "matter coframe map"),
        ("SRC4009_17_fmap_aux", SRC / "P8_Y5_R10_1271_FIELD_BY_FIELD_QRAB_VR_MAP.csv", "FMAP1271_9_aux_reduced_readout", "aux reduced readout"),
        ("SRC4009_18_inv_fail", SRC / "P8_Y5_R10_1271_OBSERVED_INVARIANCE_TEST.csv", "INV1271_0_all_observed_fields", "observed invariance failure"),
        ("SRC4009_19_inv_aux", SRC / "P8_Y5_R10_1271_OBSERVED_INVARIANCE_TEST.csv", "INV1271_3_auxiliary_elimination", "auxiliary elimination pass conditional"),
        ("SRC4009_20_route1271", SRC / "P8_Y5_R10_1271_ROUTE_DECISION_AFTER_FIELD_MAP.csv", "RD1271_1_auxiliary_route", "1271 route decision"),
        ("SRC4009_21_aux_target", SRC / "P8_Y5_R10_1271_AUXILIARY_PARENT_NECESSITY_TARGET.csv", "AUXN1271_4_theorem_target", "auxiliary theorem target"),
        ("SRC4009_22_cell_identity", SRC / "P8_Y5_R2FR_4005_AUXILIARY_NECESSITY_PROOF_ATTEMPT.csv", "AN4005_0_cell_two_form_identity", "R_AB cell identity"),
        ("SRC4009_23_all_subdomain", SRC / "P8_Y5_R2FR_4005_AUXILIARY_NECESSITY_PROOF_ATTEMPT.csv", "AN4005_1_all_subdomain_cell_charge", "all-subdomain cell lock"),
        ("SRC4009_24_cell_packet", SRC / "P8_Y5_R2FR_4006_PARENT_INSERTION_PACKET.csv", "PIP4006_1_action", "4006 cell action"),
        ("SRC4009_25_no_deriv", SRC / "P8_Y5_R2FR_4006_PARENT_INSERTION_PACKET.csv", "PIP4006_2_no_derivative_language", "4006 no derivative grammar"),
        ("SRC4009_26_delta_lambda", SRC / "P8_Y5_R2FR_4006_VARIATION_CHAIN.csv", "VAR4006_0_delta_Lambda", "delta lambda R=0"),
        ("SRC4009_27_delta_R", SRC / "P8_Y5_R2FR_4006_VARIATION_CHAIN.csv", "VAR4006_1_delta_R_or_cell_density", "delta R source equation"),
        ("SRC4009_28_source_label_packet", SRC / "P8_Y5_R2FR_4008_SOURCE_LABEL_FORGETTING_CONSTRUCTOR_PACKET.csv", "SLF4008_0_signature", "4008 matter constructor"),
        ("SRC4009_29_hcore_linear", SRC / "P8_Y5_R10_1273_HCORE_OWNER_CLASSIFICATION.csv", "HCO1273_4_linear_multiplier", "linear multiplier mechanism"),
        ("SRC4009_30_hcore_unimodular", SRC / "P8_Y5_R10_1273_HCORE_OWNER_CLASSIFICATION.csv", "HCO1273_5_unimodular_radial_cell", "unimodular radial cell"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def q_attempt_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "QK4009_0_direct_verticality",
            "claim_piece": "R_AB in ker(Dq) before readout",
            "calculation": "For q_full=(A=T^2,B=S,...), delta R_AB=delta ln A + delta ln B changes A, B, clocks/rulers and matter coframe unless both delta A and delta B vanish.",
            "result": "FAILS_FOR_FULL_OBSERVED_METRIC",
            "non_smuggling_status": "REJECT_DIRECT_VERTICALITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "attempt_id": "QK4009_1_split_tuning",
            "claim_piece": "choose split a so one observable hides R_AB",
            "calculation": "A split can protect one composite such as T/sqrt(S), but A and B are separately observed by clocks, radial rulers, light bending and matter coframe.",
            "result": "PARTIAL_CANCELLATION_NOT_KERNEL",
            "non_smuggling_status": "REJECT_TUNED_SPLIT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "attempt_id": "QK4009_2_class_quotient",
            "claim_piece": "declare q=[A,B]/R_AB so Dq[v_R]=0",
            "calculation": "This makes the target true by definition after identifying the problem; it needs a primitive parent proof before observed metric variables are declared.",
            "result": "CIRCULAR_UNLESS_PARENT_PRIMITIVE_PROVES_EQUIVALENCE",
            "non_smuggling_status": "REJECT_AS_CLOSURE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "attempt_id": "QK4009_3_constraint_first",
            "claim_piece": "R_AB eliminated by parent cell-lock before public q/readout",
            "calculation": "E_Lambda gives R_AB=0; after reducing to the constraint surface, there is no independent v_R tangent to public readout, so DObs_e[v_R] is not a physical variation term.",
            "result": "PASS_CONDITIONAL_IF_CELL_LOCK_ADOPTED_BEFORE_Q",
            "non_smuggling_status": "BEST_ROUTE_NOT_A_KERNEL_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "attempt_id": "QK4009_4_verdict",
            "claim_piece": "actual R_AB vertical route",
            "calculation": "Direct q-kernel route fails; constraint-first auxiliary elimination is the only non-smuggling path currently supported by the corpus.",
            "result": "DIRECT_VERTICALITY_REJECTED_CONSTRAINT_FIRST_ROUTE_RETAINED",
            "non_smuggling_status": "NO_LOCAL_GR_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def coframe_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "certificate_id": "OC4009_0_public_coframe",
            "statement": "e_obs is the public coframe used by EH, Hilbert stress, clocks, rods and local readout.",
            "condition": "one observed coframe branch exists and no second hidden coframe enters S_ord or source normalization",
            "current_status": "CANDIDATE_VISIBLE_NOT_PARENT_DERIVED",
            "effect_on_JR_geom": "if unsigned, Hilbert stress can see hidden coframe leakage",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "certificate_id": "OC4009_1_direct_preconstraint",
            "statement": "Before cell-lock elimination, D_R e_obs is generically nonzero because e_obs contains T and sqrt(S).",
            "condition": "full metric/coframe readout",
            "current_status": "GEOMETRY_LEAK_EXPLICIT",
            "effect_on_JR_geom": "J_R_geom = int tau_a^mu D_R e_mu^a can survive",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "certificate_id": "OC4009_2_constraint_reduced",
            "statement": "After parent-signed E_Lambda imposes T sqrt(S)=1, the reduced coframe e_red is evaluated on C_R=0 and no independent R_AB variation is available to matter readout.",
            "condition": "cell-lock action adopted before q/readout; no derivative R_AB; variation-before-readout",
            "current_status": "EXACT_IF_SINGLE_BRANCH_ADOPTED",
            "effect_on_JR_geom": "bulk geometric matter term is removed by reduction, not hidden as gauge",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "certificate_id": "OC4009_3_connection",
            "statement": "omega_obs=omega[e_red] descends with the same reduced coframe, not an independent hidden connection.",
            "condition": "Levi-Civita/compatible connection selected after reduction",
            "current_status": "CONDITIONAL_UNSIGNED",
            "effect_on_JR_geom": "independent connection/torsion source charge remains if not signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "certificate_id": "OC4009_4_same_branch",
            "statement": "4006 cell-lock packet, 4008 matter constructor and this reduced coframe certificate must be adopted in one parent branch.",
            "condition": "no stitched certificate from separate checkpoints",
            "current_status": "MISSING_SINGLE_BRANCH_ADOPTION",
            "effect_on_JR_geom": "conditional zeros cannot be promoted yet",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def geom_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "GJR4009_0_master",
            "coefficient": "J_R_geom",
            "formula": "J_R_geom := int_M tau_a^mu D_R e_mu^a dmu_obs = 1/2 int_M sqrt(-g_obs) T^{mu nu} D_R g_obs_{mu nu} d^4x",
            "value": "ZERO_IF_CONSTRAINT_FIRST_REDUCTION_ADOPTED_ELSE_MISSING_GEOMETRY_RESPONSE",
            "units": "action_density_per_RAB_or_normalized_dimensionless_after_source_projection",
            "observable_link": "local_GR;Newton_G;PPN_gamma;clock_redshift;radial_rulers;R10",
            "source_status": "DERIVED_ZERO_CONDITIONAL_OR_FINITE_ROW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GJR4009_1_lapse",
            "coefficient": "c_lapse_R",
            "formula": "D_R ln A with A=T^2=-g_tt/c^2",
            "value": "MISSING_IF_FULL_METRIC_READOUT_USED",
            "units": "per_RAB",
            "observable_link": "clocks;redshift;Newtonian_potential",
            "source_status": "FINITE_COMPONENT_IF_NOT_ELIMINATED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GJR4009_2_radial",
            "coefficient": "c_radial_R",
            "formula": "D_R ln B with B=S=g_rr",
            "value": "MISSING_IF_FULL_METRIC_READOUT_USED",
            "units": "per_RAB",
            "observable_link": "radial_rulers;light_bending;PPN_gamma",
            "source_status": "FINITE_COMPONENT_IF_NOT_ELIMINATED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GJR4009_3_hidden_coframe",
            "coefficient": "c_hidden_coframe_R",
            "formula": "D_R(e_hidden/e_obs) or hidden coframe leakage into S_ord/source normalization",
            "value": "MISSING_NO_SECOND_COFRAME_THEOREM_OR_NUMERIC_BOUND",
            "units": "per_RAB",
            "observable_link": "WEP;clock;PPN;source_normalization",
            "source_status": "MISSING_PARENT_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GJR4009_4_projection",
            "coefficient": "arena_projection",
            "formula": "map any surviving J_R_geom to PPN/WEP/R10/clock/orbital kernels",
            "value": "MISSING_ARENA_PROJECTION_IF_ANY_GEOMETRY_COMPONENT_SURVIVES",
            "units": "arena_dependent",
            "observable_link": "all_local_tests",
            "source_status": "MISSING_IF_NOT_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def branch_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "SBG4009_0_cell_lock",
            "required_clause": "S_cell=int Lambda_J(Omega_tr-Omega_ref) is parent-adopted before public q/readout",
            "status": "PACKET_EXISTS_NOT_ADOPTED",
            "if_passed": "R_AB=0 by E_Lambda on the constraint surface",
            "if_failed": "direct R_AB verticality remains rejected",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "SBG4009_1_no_independent_vR",
            "required_clause": "q is defined on the reduced constraint surface, so no independent v_R is a readout tangent",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "if_passed": "DObs_e[v_R] term is absent rather than assumed zero",
            "if_failed": "J_R_geom finite row remains",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "SBG4009_2_single_coframe",
            "required_clause": "one observed coframe and compatible connection feed EH, S_ord, clocks, rods and source normalization",
            "status": "CANDIDATE_UNSIGNED",
            "if_passed": "hidden coframe leakage closed",
            "if_failed": "c_hidden_coframe_R retained",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "SBG4009_3_matter_constructor",
            "required_clause": "4008 source-label-forgetting constructor is adopted in the same branch",
            "status": "PACKET_EXISTS_NOT_ADOPTED",
            "if_passed": "source-label and constant-marker matter terms are typed out",
            "if_failed": "w_R_source/b_theta_R/readout_regen_R retained",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "SBG4009_4_boundary_worldtube",
            "required_clause": "matter/worldtube/boundary terms have no reciprocal flux or are bounded",
            "status": "OPEN_NEXT_TARGET",
            "if_passed": "bulk J_R route can proceed to current/source normalization gates",
            "if_failed": "J_R_boundary retained",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"case_id": "CASE4009_0_direct_full_metric", "constraint_first": False, "full_metric_readout": True, "single_coframe": True, "matter_packet": True, "boundary_closed": True, "timestamp_utc": timestamp},
        {"case_id": "CASE4009_1_class_quotient", "constraint_first": False, "full_metric_readout": False, "single_coframe": True, "matter_packet": True, "boundary_closed": True, "timestamp_utc": timestamp},
        {"case_id": "CASE4009_2_constraint_first_bulk", "constraint_first": True, "full_metric_readout": False, "single_coframe": True, "matter_packet": True, "boundary_closed": True, "timestamp_utc": timestamp},
        {"case_id": "CASE4009_3_constraint_hidden_coframe", "constraint_first": True, "full_metric_readout": False, "single_coframe": False, "matter_packet": True, "boundary_closed": True, "timestamp_utc": timestamp},
        {"case_id": "CASE4009_4_constraint_matter_packet_open", "constraint_first": True, "full_metric_readout": False, "single_coframe": True, "matter_packet": False, "boundary_closed": True, "timestamp_utc": timestamp},
        {"case_id": "CASE4009_5_constraint_boundary_open", "constraint_first": True, "full_metric_readout": False, "single_coframe": True, "matter_packet": True, "boundary_closed": False, "timestamp_utc": timestamp},
    ]


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        constraint_first = bool(case["constraint_first"])
        full_metric_readout = bool(case["full_metric_readout"])
        single_coframe = bool(case["single_coframe"])
        matter_packet = bool(case["matter_packet"])
        boundary_closed = bool(case["boundary_closed"])

        if full_metric_readout:
            q_status = "DIRECT_VERTICALITY_FAILS"
            geom_status = "J_R_GEOM_LIVE"
            next_action = "do not call R_AB vertical; use constraint-first route or finite geometry row"
        elif not constraint_first:
            q_status = "CLASS_QUOTIENT_CIRCULAR"
            geom_status = "J_R_GEOM_NOT_ZEROED"
            next_action = "derive primitive equivalence before readout or reject"
        elif not single_coframe:
            q_status = "CONSTRAINT_FIRST_HIDDEN_COFRAME_OPEN"
            geom_status = "C_HIDDEN_COFRAME_R_LIVE"
            next_action = "prove one observed coframe/no hidden metric leakage"
        elif not matter_packet:
            q_status = "CONSTRAINT_FIRST_MATTER_PACKET_OPEN"
            geom_status = "SOURCE_LABEL_OR_CONSTANT_TERMS_LIVE"
            next_action = "adopt 4008 constructor in same branch or keep coefficient pack"
        elif not boundary_closed:
            q_status = "BULK_GEOMETRY_ZERO_BOUNDARY_OPEN"
            geom_status = "J_R_BOUNDARY_WORLD_TUBE_OPEN"
            next_action = "derive boundary/worldtube nohair or finite boundary row"
        else:
            q_status = "CONDITIONAL_CONSTRAINT_FIRST_BULK_PASS"
            geom_status = "J_R_GEOM_BULK_ZERO_CONDITIONAL"
            next_action = "assemble single-branch adoption and attack boundary/source-normalization gates"

        rows.append(
            {
                "case_id": case["case_id"],
                "q_status": q_status,
                "J_R_geom_status": geom_status,
                "claim_allowed": False,
                "valid_for_claim": False,
                "next_action": next_action,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4009_0_reject_direct_verticality",
            "decision": "do not claim R_AB is in ker(Dq) under full metric/coframe readout",
            "reason": "A, B, clocks, radial rulers and matter coframe see the reciprocal cell mode",
            "effect": "prevents closure smuggling and keeps PPN-relevant geometry honest",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4009_1_constraint_first_route",
            "decision": "retain constraint-first cell-lock elimination as the non-smuggling route",
            "reason": "E_Lambda removes R_AB before public readout rather than calling an observed metric component gauge",
            "effect": "bulk J_R_geom can be conditionally zero if the cell-lock/matter/coframe packets are adopted in one branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4009_2_geom_row",
            "decision": "if constraint-first adoption fails, J_R_geom is a finite row",
            "reason": "the geometric coupling is explicitly tau_a^mu D_R e_mu^a or 1/2 T^{mu nu}D_R g_mu_nu",
            "effect": "no vague geometry leak remains; it is either eliminated or parameterized",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4009_3_next",
            "decision": "next target is boundary/worldtube nohair or J_R_boundary row",
            "reason": "after source-label and bulk geometry leaks are conditionally narrowed, boundary/local projection is the next live J_R term",
            "effect": "4010 should attack the boundary flux, not repeat quotient sorting",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CLAIM4009_0_RAB_vertical",
            "claim": "R_AB is in ker(Dq)",
            "allowed": False,
            "blocker": "rejected under full observed metric/coframe readout; only constraint-first elimination survives",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4009_1_JR_geom_zero",
            "claim": "J_R_geom=0",
            "allowed": False,
            "blocker": "conditional on adopted cell-lock before q, single observed coframe, adopted 4008 matter constructor and boundary closure",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4009_2_local_GR",
            "claim": "local GR/Newton recovered",
            "allowed": False,
            "blocker": "boundary/worldtube, source normalization, current-chain and PPN second-order gates remain",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4009_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive boundary/worldtube nohair for reciprocal cell-lock branch, or create a finite J_R_boundary row with units, source path and local-test projections",
            "success_condition": "Pi_R^n, B_R, worldtube support variation and local projection boundary flux are zero/exact/proper in the same branch; otherwise J_R_boundary is explicitly bounded and valid_for_claim=false",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "direct R_AB q-kernel verticality rejected; constraint-first cell-lock elimination retained as the clean route; finite J_R_geom rows written for nonadoption",
            "current_best_next": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    lines = [
        "# 4009 - q-Kernel Observed-Coframe Single-Branch Certificate Or Geometric J_R Row",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "The direct quotient route is rejected for the current observer map.",
        "",
        "If the public readout sees `A=T^2` and `B=S`, then `R_AB=ln(AB)` is not vertical: clocks, radial rulers, light bending and the matter coframe can all see it.",
        "",
        "The clean route is different: parent-signed constraint-first elimination.",
        "",
        "`E_Lambda: Omega_tr=Omega_ref -> T sqrt(S)=1 -> R_AB=0`.",
        "",
        "After that reduction, there is no independent `v_R` tangent to public readout. This is not a gauge claim; it is auxiliary elimination before readout.",
        "",
        "## Geometric Source Term",
        "",
        "If the constraint-first route is not adopted, the honest residual is",
        "",
        "`J_R_geom = int tau_a^mu D_R e_mu^a dmu_obs = 1/2 int sqrt(-g) T^{mu nu} D_R g_{mu nu}`.",
        "",
        "So the geometry leak is now explicit: either eliminated by the cell-lock branch, or carried as a finite coefficient row.",
        "",
        "## Single-Branch Conditions",
        "",
        "- 4006 cell-lock action adopted before `q` and readout.",
        "- no independent derivative/kinetic `R_AB` grammar.",
        "- one observed coframe feeds EH, matter, clocks, rods and source normalization.",
        "- 4008 source-label-forgetting matter constructor adopted in the same branch.",
        "- boundary/worldtube reciprocal flux closed or bounded.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: q=`{row['q_status']}`, J_R_geom=`{row['J_R_geom_status']}`, next=`{row['next_action']}`"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "This is stricter and cleaner than claiming `R_AB` is gauge. Direct verticality fails; constraint-first elimination remains viable. The next live term is boundary/worldtube flux.",
            "",
            "## Next Target",
            "",
            f"- `{NEXT_DOC}`",
            f"- `{NEXT_SCRIPT}`",
            "",
            "## Source Count",
            "",
            f"- source needles found: `{found}/{len(sources)}`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def append_spine(timestamp: str) -> None:
    marker = "## 4009 - q-Kernel/Coframe Geometry Fork"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: direct `R_AB in ker(Dq)` is rejected under full observed metric/coframe readout; `A=T^2`, `B=S`, clocks/rulers and matter coframe see it.
- Clean route: constraint-first cell-lock elimination, `E_Lambda -> T sqrt(S)=1 -> R_AB=0`, before public `q` and readout.
- Geometric residual if not adopted: `J_R_geom=int tau_a^mu D_R e_mu^a = (1/2)int sqrt(-g)T^{{mu nu}}D_R g_{{mu nu}}`.
- No claim: cell-lock, single observed coframe, 4008 matter constructor and boundary/worldtube gates are not adopted in one final branch.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4009 - q-Kernel/Coframe Geometry Fork" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    q_attempt: list[dict[str, Any]],
    coframe: list[dict[str, Any]],
    geom: list[dict[str, Any]],
    branch: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4009_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4009_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL4009_02_direct_fail", any(row["attempt_id"] == "QK4009_0_direct_verticality" and row["result"] == "FAILS_FOR_FULL_OBSERVED_METRIC" for row in q_attempt), "direct verticality failure recorded")
    add("VAL4009_03_tuning_reject", any(row["attempt_id"] == "QK4009_1_split_tuning" for row in q_attempt), "split tuning rejection recorded")
    add("VAL4009_04_class_reject", any(row["attempt_id"] == "QK4009_2_class_quotient" and "CIRCULAR" in row["result"] for row in q_attempt), "class quotient circularity recorded")
    add("VAL4009_05_constraint_pass", any(row["attempt_id"] == "QK4009_3_constraint_first" and "PASS_CONDITIONAL" in row["result"] for row in q_attempt), "constraint-first conditional route recorded")
    add("VAL4009_06_public_coframe", any(row["certificate_id"] == "OC4009_0_public_coframe" for row in coframe), "public coframe certificate row present")
    add("VAL4009_07_preconstraint_leak", any(row["certificate_id"] == "OC4009_1_direct_preconstraint" for row in coframe), "preconstraint geometry leak row present")
    add("VAL4009_08_reduced_coframe", any(row["certificate_id"] == "OC4009_2_constraint_reduced" for row in coframe), "reduced coframe row present")
    add("VAL4009_09_same_branch", any(row["certificate_id"] == "OC4009_4_same_branch" for row in coframe), "same-branch coframe row present")
    master = next(row for row in geom if row["row_id"] == "GJR4009_0_master")
    add("VAL4009_10_geom_master", "tau_a^mu" in master["formula"] and "T^{mu nu}" in master["formula"], "J_R_geom master formula present")
    add("VAL4009_11_lapse_row", any(row["row_id"] == "GJR4009_1_lapse" for row in geom), "lapse component row present")
    add("VAL4009_12_radial_row", any(row["row_id"] == "GJR4009_2_radial" for row in geom), "radial component row present")
    add("VAL4009_13_hidden_row", any(row["row_id"] == "GJR4009_3_hidden_coframe" for row in geom), "hidden coframe row present")
    add("VAL4009_14_projection_row", any(row["row_id"] == "GJR4009_4_projection" for row in geom), "projection guard row present")
    add("VAL4009_15_cell_gate", any(row["gate_id"] == "SBG4009_0_cell_lock" for row in branch), "cell-lock branch gate present")
    add("VAL4009_16_no_vR_gate", any(row["gate_id"] == "SBG4009_1_no_independent_vR" for row in branch), "no independent v_R gate present")
    add("VAL4009_17_coframe_gate", any(row["gate_id"] == "SBG4009_2_single_coframe" for row in branch), "single coframe gate present")
    add("VAL4009_18_boundary_gate", any(row["gate_id"] == "SBG4009_4_boundary_worldtube" for row in branch), "boundary next gate present")
    direct = next(row for row in results if row["case_id"] == "CASE4009_0_direct_full_metric")
    klass = next(row for row in results if row["case_id"] == "CASE4009_1_class_quotient")
    bulk = next(row for row in results if row["case_id"] == "CASE4009_2_constraint_first_bulk")
    hidden = next(row for row in results if row["case_id"] == "CASE4009_3_constraint_hidden_coframe")
    matter = next(row for row in results if row["case_id"] == "CASE4009_4_constraint_matter_packet_open")
    boundary = next(row for row in results if row["case_id"] == "CASE4009_5_constraint_boundary_open")
    add("VAL4009_19_direct_case", direct["q_status"] == "DIRECT_VERTICALITY_FAILS", "direct full metric case fails")
    add("VAL4009_20_class_case", klass["q_status"] == "CLASS_QUOTIENT_CIRCULAR", "class quotient case circular")
    add("VAL4009_21_bulk_case", bulk["J_R_geom_status"] == "J_R_GEOM_BULK_ZERO_CONDITIONAL", "constraint-first bulk case conditionally closes")
    add("VAL4009_22_hidden_case", hidden["J_R_geom_status"] == "C_HIDDEN_COFRAME_R_LIVE", "hidden coframe case routed")
    add("VAL4009_23_matter_case", matter["J_R_geom_status"] == "SOURCE_LABEL_OR_CONSTANT_TERMS_LIVE", "matter packet open case routed")
    add("VAL4009_24_boundary_case", boundary["J_R_geom_status"] == "J_R_BOUNDARY_WORLD_TUBE_OPEN", "boundary open case routed")
    add("VAL4009_25_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4009_26_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4009_27_doc_exists", DOC_PATH.exists() and "Geometric Source Term" in read_text(DOC_PATH), "document written")
    add("VAL4009_28_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4009_29_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4009_30_compile", compile_ok, "script compiles")
    add("VAL4009_31_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    output_tables = [sources, q_attempt, coframe, geom, branch, results, read_csv(OUTPUTS["decision"]), read_csv(OUTPUTS["claim_gate"]), read_csv(OUTPUTS["next"]), read_csv(OUTPUTS["status"])]
    add("VAL4009_32_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4009_33_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4009_34_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4009_35_forward_target", "boundary" in read_text(OUTPUTS["next"]) and "worldtube" in read_text(OUTPUTS["next"]), "forward target is boundary/worldtube nohair")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    q_attempt = q_attempt_rows(timestamp)
    coframe = coframe_rows(timestamp)
    geom = geom_rows(timestamp)
    branch = branch_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["q_attempt"], q_attempt)
    write_csv(OUTPUTS["coframe"], coframe)
    write_csv(OUTPUTS["geom"], geom)
    write_csv(OUTPUTS["branch"], branch)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, q_attempt, coframe, geom, branch, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4009 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
