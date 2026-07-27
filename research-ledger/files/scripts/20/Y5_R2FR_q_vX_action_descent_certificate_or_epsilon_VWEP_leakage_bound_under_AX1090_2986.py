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

CHECKPOINT = "2986"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2986-Y5-R2FR-q-vX-action-descent-certificate-or-epsilon-VWEP-leakage-bound-under-AX1090.md"

SRC_2985_DOC = ROOT / "2985-Y5-R2FR-AX1090-parent-action-object-or-VWEP-vertical-generator-zero-certificate-under-AX1090.md"
SRC_AX1090 = MICRO_COEFF / "AX1090_parent_object_proof_attempt.csv"
SRC_VWEP_MAP = MICRO_COEFF / "V_WEP_field_by_field_action_map.csv"
SRC_VWEP_CANDIDATE = MICRO_COEFF / "V_WEP_generator_candidate.csv"
SRC_QVX_1023 = RESIDUALS / "P8_Y5_R10_1023_QVX_CERTIFICATE.csv"
SRC_VWEP_DOMAIN = RESIDUALS / "P8_Y5_R10_1448_VWEP_DOMAIN_PROOF_ATTEMPT.csv"
SRC_QVX_2154 = RESIDUALS / "P8_Y5_PARENT_QLOC_2154_QVX_ACTION_DESCENT_CERTIFICATE.csv"
SRC_PARENT_CLAUSES_2356 = RESIDUALS / "P8_Y5_PARENT_QLOC_2356_PARENT_DESCENT_CLAUSES.csv"
SRC_COMMON_DQZ_2643 = RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_PARENT_SIGNATURE_THEOREM_GATE.csv"
SRC_Q_ADMISS_2686 = RESIDUALS / "P8_Y5_R2FR_2686_Q_DESCENT_ADMISSIBILITY_AUDIT.csv"
SRC_PROJECTOR_2812 = RESIDUALS / "P8_Y5_R2FR_2812_ORTHOGONAL_PROJECTOR_SIGNATURE_AUDIT.csv"
SRC_RANK_2884 = RESIDUALS / "P8_Y5_R2FR_2884_FULL_RANK_COERCIVITY_GATE.csv"
SRC_SOURCE_CURRENT_2909 = RESIDUALS / "P8_Y5_R2FR_2909_SOURCE_CURRENT_DESCENT_PROOF_ATTEMPT.csv"
SRC_MATTER_2956 = RESIDUALS / "P8_Y5_R2FR_2956_MATTER_PULLBACK_DESCENT_AUDIT.csv"
SRC_TERM_STATUS_2968 = RESIDUALS / "P8_Y5_R2FR_2968_RANK_ZERO_TERM_STATUS.csv"
SRC_COMBINED_2969 = RESIDUALS / "P8_Y5_R2FR_2969_COMBINED_DESCENT_THEOREM_LEDGER.csv"
SRC_SIGNATURE_2970 = RESIDUALS / "P8_Y5_R2FR_2970_PARENT_SIGNATURE_GATE.csv"
SRC_QMAP_2970 = RESIDUALS / "P8_Y5_R2FR_2970_QMAP_KERNEL_AUDIT.csv"
SRC_MATTER_2970 = RESIDUALS / "P8_Y5_R2FR_2970_BASIC_MATTER_ACTION_AUDIT.csv"
SRC_COEFFS_2970 = RESIDUALS / "P8_Y5_R2FR_2970_FIRST_LEAKAGE_COEFFICIENT_ROWS_NONCLAIM.csv"
SRC_ZERO_2971 = RESIDUALS / "P8_Y5_R2FR_2971_THEOREM_ZERO_ATTEMPT.csv"
SRC_ENVELOPE_2971 = RESIDUALS / "P8_Y5_R2FR_2971_NO_CANCELLATION_ENVELOPE.csv"
SRC_FACTOR_2972 = RESIDUALS / "P8_Y5_R2FR_2972_DQZ_FACTOR_AUDIT.csv"
SRC_EPSQ_2972 = RESIDUALS / "P8_Y5_R2FR_2972_FIRST_EPSQ_SUBROWS_NONCLAIM.csv"
SRC_PO_1019 = RESIDUALS / "P8_Y5_R10_1019_PROJECTOR_ORTHOGONALITY_CLAUSES.csv"
SRC_STOKES_1020 = RESIDUALS / "P8_Y5_R10_1020_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv"
SRC_BX_1021 = RESIDUALS / "P8_Y5_R10_1021_BX_PRIMITIVE_GATES.csv"

LIVE_C_PARENT = MICRO_COEFF / "C_parent_WEP_slot_import.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2986_SOURCE_REGISTER.csv",
    "conditional": RESIDUALS / "P8_Y5_R2FR_2986_CONDITIONAL_DESCENT_THEOREM_LEDGER.csv",
    "certificate": RESIDUALS / "P8_Y5_R2FR_2986_QVX_ACTION_DESCENT_CERTIFICATE_AUDIT.csv",
    "epsilon": RESIDUALS / "P8_Y5_R2FR_2986_EPSILON_VWEP_BOUND_ROWS_NONCLAIM.csv",
    "requirements": RESIDUALS / "P8_Y5_R2FR_2986_BOUND_INPUT_REQUIREMENTS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2986_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2986_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2986_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2986_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2986_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "certificate_copy": PARENT_ACTION / "q_vX_action_descent_certificate_2986_NOT_SIGNED.csv",
    "epsilon_copy": LOCAL_BOUNDS / "epsilon_VWEP_bound_rows_2986_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2986_epsilon_VWEP_or_parent_generator_next_NONCLAIM.csv",
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
        ("SRC2986_00_2985_doc", SRC_2985_DOC, ["NEXT2985_0_2986", "q/v_X/action descent"], "2985 selected handoff"),
        ("SRC2986_01_AX1090", SRC_AX1090, ["AXP1447_3_verdict", "PARENT_OBJECT_NOT_PROVEN"], "AX1090 parent object status"),
        ("SRC2986_02_VWEP_map", SRC_VWEP_MAP, ["parent_configuration", "MISSING_ACTUAL_PARENT_TRANSFORMATION_LAW"], "field-by-field V_WEP action map"),
        ("SRC2986_03_VWEP_candidate", SRC_VWEP_CANDIDATE, ["VWEP1448_0_candidate", "CANDIDATE_ONLY_NOT_PARENT_SIGNED"], "V_WEP generator candidate"),
        ("SRC2986_04_QVX_1023", SRC_QVX_1023, ["QVC1023_8_verdict", "fail_current_claim_demote_current_branch"], "R10 q/v_X certificate"),
        ("SRC2986_05_VWEP_domain", SRC_VWEP_DOMAIN, ["VDP1448_0_chain_rule", "FAIL_CURRENT_CLAIM_DOMAIN_NOT_SIGNED"], "V_WEP domain proof attempt"),
        ("SRC2986_06_QVX_2154", SRC_QVX_2154, ["QVC2154_8_verdict", "FAIL_CURRENT_CLAIM_DEMOTE_CURRENT_BRANCH"], "parent qloc q/v_X action certificate"),
        ("SRC2986_07_parent_clauses_2356", SRC_PARENT_CLAUSES_2356, ["PDC2356_9_verdict", "DESCENT_CHAIN_NOT_CLOSED"], "parent descent clause matrix"),
        ("SRC2986_08_common_dqz_2643", SRC_COMMON_DQZ_2643, ["QVIS2643_6_verdict", "NOT_CLOSED_FINITE_LEAK_ROWS_REQUIRED"], "common descent theorem gate"),
        ("SRC2986_09_q_admiss_2686", SRC_Q_ADMISS_2686, ["QDA2686_5_verdict", "Q_DESCENT_INSUFFICIENT_NEEDS_SORT_DISJOINTNESS_NOHOM"], "q-descent admissibility audit"),
        ("SRC2986_10_projector_2812", SRC_PROJECTOR_2812, ["OPS2812_4_verdict", "FAIL_CURRENT_CLAIM"], "orthogonal projector signature audit"),
        ("SRC2986_11_rank_2884", SRC_RANK_2884, ["RG2884_5_verdict", "FULL_RANK_COERCIVITY_NOT_PROVED"], "full-rank coercivity gate"),
        ("SRC2986_12_source_current_2909", SRC_SOURCE_CURRENT_2909, ["PROOF2909_7_verdict", "CONDITIONAL_THEOREM_CLOSED_APPLICATION_BLOCKED"], "source-current descent proof attempt"),
        ("SRC2986_13_matter_2956", SRC_MATTER_2956, ["DESC2956_7_verdict", "QBARXT_ZERO_NOT_DERIVED"], "matter pullback descent audit"),
        ("SRC2986_14_term_status_2968", SRC_TERM_STATUS_2968, ["TERM2968_7_total", "ALL_FORCING_TERMS_NOT_CLOSED"], "rank-zero term status"),
        ("SRC2986_15_combined_2969", SRC_COMBINED_2969, ["THM2969_0_combined_descent", "NOT_DERIVED_CURRENT_MTS"], "combined Dq_Z/J_A theorem ledger"),
        ("SRC2986_16_signature_2970", SRC_SIGNATURE_2970, ["SIG2970_8_verdict", "NOT_DERIVED_COEFFICIENT_ROWS_REQUIRED"], "parent signature gate"),
        ("SRC2986_17_qmap_2970", SRC_QMAP_2970, ["QMAP2970_6_verdict", "NOT_PARENT_SIGNED_FINITE_DQZ_REQUIRED"], "q-map kernel audit"),
        ("SRC2986_18_matter_2970", SRC_MATTER_2970, ["MAT2970_7_verdict", "NOT_DERIVED_J_DIRECT_J_SPURION_ROWS_REQUIRED"], "basic matter action audit"),
        ("SRC2986_19_coeffs_2970", SRC_COEFFS_2970, ["COEF2970_9_total", "DqZ_JA_first_leakage_total"], "first leakage coefficient rows"),
        ("SRC2986_20_zero_2971", SRC_ZERO_2971, ["TZ2971_5_verdict", "NOT_DERIVED_SPLIT_REQUIRED"], "theorem-zero attempt"),
        ("SRC2986_21_envelope_2971", SRC_ENVELOPE_2971, ["ENV2971_3_total", "first_leakage_total_abs"], "no-cancellation leakage envelope"),
        ("SRC2986_22_factor_2972", SRC_FACTOR_2972, ["FAC2972_5_verdict", "NOT_SOURCE_BACKED_SPLIT_REQUIRED"], "DqZ factor audit"),
        ("SRC2986_23_epsq_2972", SRC_EPSQ_2972, ["EPSQ2972_00_eps_q_declaration", "MISSING_SOURCE_BACKED_UPPER_BOUND"], "epsq subrows"),
        ("SRC2986_24_po_1019", SRC_PO_1019, ["PO1019_5_verdict", "fail_current_claim"], "projector orthogonality clauses"),
        ("SRC2986_25_stokes_1020", SRC_STOKES_1020, ["ETB1020_5_verdict", "fail_current_claim_but_derivation_progress"], "weighted Stokes edge theorem"),
        ("SRC2986_26_bx_1021", SRC_BX_1021, ["BXG1021_5_verdict", "fail_current_claim"], "B_X primitive gates"),
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


def conditional_rows() -> list[dict[str, Any]]:
    data = [
        (
            "CDT2986_0_chain_rule_spine",
            "single descent chain-rule theorem",
            "If q is parent-owned, v_X is a parent vector field with Dq[v_X]=0, S_parent=Sbar[q(Phi),Psi,theta]+B, theta is q-basic, no direct source slot exists, and B/readout are silent, then dS_parent[v_X]=0.",
            "EXACT_CONDITIONAL_THEOREM",
            "parent premises are not signed together",
        ),
        (
            "CDT2986_1_geometry",
            "observed geometry term",
            "D Obs(q)[Dq[v_X]]=0 when Dq[v_X]=0 and Obs is q-basic.",
            "CHAIN_RULE_EXACT_CONDITIONAL",
            "observed coframe/frame/readout functor is not parent-unique",
        ),
        (
            "CDT2986_2_matter",
            "ordinary matter pullback",
            "delta_v S_matter=D Sbar[Dq(v)]+J_theta L_v theta+J_direct[v]+delta_v B.",
            "CHAIN_RULE_EXACT_CONDITIONAL",
            "J_theta, J_direct and boundary terms remain live",
        ),
        (
            "CDT2986_3_boundary",
            "edge/projector term",
            "boundary silence follows only if B_X is primitive/exact, weighted Stokes has zero or bounded derivative term, and Pi_M^H is parent-owned.",
            "CONDITIONAL_OR_BOUND_ONLY",
            "B_X primitive, projector orthogonality and source support are not closed",
        ),
        (
            "CDT2986_4_verdict",
            "current MTS application",
            "The theorem is useful and should be kept, but it cannot be imported as a local-GR/Newton/WEP zero in the current corpus.",
            "EXACT_CONDITIONAL_CURRENT_APPLICATION_BLOCKED",
            "stage epsilon_VWEP instead of claiming C_parent_WEP=0",
        ),
    ]
    return [
        add(
            {
                "theorem_id": theorem_id,
                "target": target,
                "statement": statement,
                "current_status": status,
                "blocking_gap": gap,
                "theorem_zero_adopted": False,
                "parent_signed": False,
            }
        )
        for theorem_id, target, statement, status, gap in data
    ]


def certificate_rows() -> list[dict[str, Any]]:
    data = [
        (
            "QVX2986_0_parent_action_owner",
            "AX1090 parent action object",
            "one parent action owns q, fields, matter/source, boundary, measure/current and variation domain before readout",
            "AXP1447_3;SIG2970_0_parent_object",
            "NOT_PARENT_SIGNED",
            "AX1090_0 remains missing, not adopted as an axiom",
            "epsilon_parent_object",
        ),
        (
            "QVX2986_1_q_canonical",
            "canonical quotient map q",
            "q: Conf_parent -> Q_obs/Q_vis is declared before empirical readout and not fitted after the fact",
            "QVC2154_0_parent_q;SIG2970_1_q_object;QMAP2970_0_projection",
            "FORMAL_PROJECTION_NOT_PARENT_SIGNATURE",
            "projection declaration does not prove parent-owned chart/domain",
            "eps_q_parent",
        ),
        (
            "QVX2986_2_vX_vertical_generator",
            "field-by-field v_X/V_WEP",
            "v_X is an actual vector field on every retained parent field, coefficient, source, boundary and readout block",
            "QVC2154_1_vertical_generator;VWEP1448_0_candidate;V_WEP_field_by_field_action_map",
            "MISSING_FIELD_BY_FIELD_PARENT_ACTION",
            "physical WEP/local direction is a candidate, not a signed field-space transformation law",
            "eps_v_generator",
        ),
        (
            "QVX2986_3_Dq_kernel",
            "Dq[v_X]=0",
            "selected local generator lies in ker(Dq) on an open local branch with declared q/v norms",
            "VDP1448_0_chain_rule;QMAP2970_6_verdict;FAC2972_3_Dq_Z_zero",
            "EXACT_CONDITIONAL_NOT_SIGNED",
            "Dq derivative, Z/v_X basis, norm and source/readout/boundary columns are missing",
            "Dq_Z_norm_total",
        ),
        (
            "QVX2986_4_action_descent",
            "parent action descent",
            "S_parent[Phi]=Sbar[q(Phi)]+fixed/proper boundary terms before variation",
            "QVC2154_2_action_descent;THM2969_0_combined_descent;SIG2970_6_basic_matter_action",
            "CONDITIONAL_THEOREM_ONLY",
            "same parent L, Theta, Q, boundary counterterm and readout order are not signed",
            "eps_action_descent",
        ),
        (
            "QVX2986_5_matter_descent",
            "ordinary matter/source descent",
            "S_matter is q-basic with owned matter lift, fixed constants, Hilbert current and no direct source slot",
            "DESC2956_7_verdict;MAT2970_7_verdict;PROOF2909_7_verdict",
            "QBARXT_AND_JA_ZERO_NOT_DERIVED",
            "matter action descent, no-source slot, current owner and species-blind grammar do not close",
            "J_A_bulk_envelope",
        ),
        (
            "QVX2986_6_no_marker_shadow_source",
            "no hidden visible/source channels",
            "hidden representative variables cannot enter visible constants, frames, weights, clocks, EM labels or source couplings",
            "QDA2686_5_verdict;QVIS2643_3_no_marker_theta;QVIS2643_4_no_source_only_slot",
            "SORT_DISJOINTNESS_NOHOM_NOT_DERIVED",
            "q-descent alone is insufficient; source-prefactor counterexample survives",
            "C_shadow_abs_plus_J_spurion",
        ),
        (
            "QVX2986_7_boundary_projector",
            "boundary/projector silence",
            "Q_edge and support/readout terms are exact/proper or source-bounded and Pi_M^H is parent-owned",
            "PO1019_5_verdict;ETB1020_5_verdict;BXG1021_5_verdict;OPS2812_4_verdict",
            "BOUNDARY_PROJECTOR_NOT_SIGNED",
            "B_X primitive, weighted-Stokes zero, projector orthogonality and support collar are open",
            "epsilon_boundary_projector",
        ),
        (
            "QVX2986_8_rank_non_degeneracy",
            "rank/nondegeneracy and physical lock",
            "quotient removes only representative redundancy, while reduced physical residuals are controlled by a full-rank coercive response map",
            "RG2884_5_verdict;TERM2968_7_total",
            "FULL_RANK_COERCIVITY_NOT_PROVED",
            "rank map, coercive physical lock and no-linear-work theorem remain missing",
            "epsilon_rank_lock",
        ),
        (
            "QVX2986_9_arena_projection",
            "R10/WEP/PPN/clock/orbital projection",
            "local residual vector is mapped into test arenas by sourced operator rows after upstream zero/bound rows exist",
            "TERM2968_6_arena_projection;ENV2971_3_total",
            "MISSING_ARENA_PROJECTION",
            "runner specs block scoring without arena operators and numeric/theorem-zero upstream heads",
            "epsilon_arena_projection",
        ),
        (
            "QVX2986_10_verdict",
            "single q/v_X/action descent certificate",
            "all certificate rows close in one parent-signed branch",
            "QVC1023_8;QVC2154_8;SIG2970_8;TZ2971_5",
            "NOT_PARENT_SIGNED_STAGE_EPSILON_VWEP",
            "conditional theorem survives, but current branch must be carried as explicit finite leakage rows",
            "epsilon_VWEP_total",
        ),
    ]
    return [
        add(
            {
                "certificate_id": cert_id,
                "clause": clause,
                "required_statement": required,
                "source_anchor": anchor,
                "current_status": status,
                "blocking_gap": gap,
                "fallback_symbol": fallback,
                "certificate_clause_signed": False,
                "theorem_zero_adopted": False,
            }
        )
        for cert_id, clause, required, anchor, status, gap, fallback in data
    ]


def epsilon_rows() -> list[dict[str, Any]]:
    data = [
        (
            "EPSV2986_00_definition",
            "epsilon_VWEP",
            "total normalized leakage of the would-be vertical WEP/local generator",
            "||dS_parent[V_WEP]||/N_WEP <= sum absolute component heads",
            "mixed_declared_by_projection",
            "no single parent action/vertical generator certificate",
            "QVX2986_10_verdict",
        ),
        ("EPSV2986_01_parent_object", "epsilon_parent_object", "parent action owner leakage", "epsilon_parent_object >= failure of one-owner AX1090 action", "dimensionless", "AX1090_0 not reduced", "SIG2970_0_parent_object"),
        ("EPSV2986_02_q", "eps_q_parent", "q declaration/chart/domain leakage", "Dq_Z_norm <= eps_q_parent + eps_constraint + eps_factorization + ...", "dimensionless", "q is formal projection, not parent-owned chart", "QMAP2970_0_projection"),
        ("EPSV2986_03_generator", "eps_v_generator", "field-by-field generator leakage", "||V_physical - V_parent_kernel|| <= eps_v_generator", "field_norm", "V_WEP field action missing on several blocks", "V_WEP_field_by_field_action_map"),
        ("EPSV2986_04_Dq", "Dq_Z_norm_total", "quotient-kernel leakage", "Dq_Z_norm <= sum EPSQ2972 subrows", "declared_q_norm", "Dq derivative/basis/norm/source-current columns missing", "FAC2972_5_verdict"),
        ("EPSV2986_05_action", "eps_action_descent", "parent action descent residual", "||S_parent - Sbar[q] - B||_var <= eps_action_descent", "action_variation_norm", "same L/Theta/Q/B/readout owner missing", "QVC2154_2_action_descent"),
        ("EPSV2986_06_matter", "J_A_bulk_envelope", "ordinary matter/source-current leakage", "|J_A| <= C_matter Dq_Z_norm + |J_direct| + |J_spurion| + |J_nonH| + boundary", "source_norm", "q-basic matter action and no-source-slot not derived", "ENV2971_1_JA"),
        ("EPSV2986_07_marker", "eps_theta_basic", "constant/material/clock/EM marker leakage", "|J_theta L_v theta| <= C_theta eps_theta_basic", "dimensionless_or_geometry_norm", "theta/dmu/basicness and constants owner unsigned", "COEF2970_3_eps_theta_basic"),
        ("EPSV2986_08_shadow", "C_shadow_abs", "hidden Weyl/disformal/source/readout shadow envelope", "DqZ_readout <= C_Obs_e Dq_Z_norm N_Z + C_shadow_abs", "dimensionless", "no-shadow/no-Hom theorem not derived", "COEF2970_8_C_shadow_abs"),
        ("EPSV2986_09_boundary", "epsilon_boundary_projector", "edge/support/projector leakage", "|Q_edge| bound plus Pi_M^H norm and support collar terms", "boundary_norm", "B_X primitive, weighted Stokes and projector orthogonality open", "ETB1020_3_residual_bound"),
        ("EPSV2986_10_rank", "epsilon_rank_lock", "rank/coercivity residual leakage", "physical residual <= ||M^-1|| * absolute forcing vector", "residual_norm", "full-rank coercive physical lock not proved", "RG2884_5_verdict"),
        ("EPSV2986_11_arena", "epsilon_arena_projection", "test-arena projection leakage", "arena_residual <= ||Pi_arena|| * upstream residual vector", "arena_norm", "R10/WEP/PPN/clock/orbital operators missing", "TERM2968_6_arena_projection"),
        ("EPSV2986_12_total", "epsilon_VWEP_total_abs", "absolute no-cancellation total", "epsilon_VWEP_total_abs <= sum EPSV2986_01..11 after each head is sourced or theorem-zero", "mixed_declared_by_projection", "no numeric/theorem-zero head is promotable now", "ENV2971_3_total"),
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
                "why_nonclaim": gap,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "no_cancellation_policy": True,
            }
        )
        for eps_id, symbol, definition, formula, units, gap, anchor in data
    ]


def requirement_rows() -> list[dict[str, Any]]:
    data = [
        ("REQ2986_0_parent_action", "AX1090 parent action object", "S_parent with field chart, variation domain, measure/current and matter/source/readout owner", "MISSING_PARENT_ACTION_OBJECT", "epsilon_parent_object"),
        ("REQ2986_1_q_map", "canonical q map", "explicit q(Phi), derivative Dq, domain/collar and quotient norm before readout", "MISSING_PARENT_Q_AND_DQ", "eps_q_parent;Dq_Z_norm_total"),
        ("REQ2986_2_generator", "actual v_X/V_WEP generator", "field-by-field transformation law on geometry, hidden fields, matter, constants, source and boundary", "MISSING_ACTUAL_PARENT_TRANSFORMATION_LAW", "eps_v_generator"),
        ("REQ2986_3_action_descent", "action descent residual", "derive or bound S_parent-Sbar[q]-B and its first variation", "MISSING_ACTION_DESCENT_RESIDUAL", "eps_action_descent"),
        ("REQ2986_4_matter", "q-basic ordinary matter action", "matter functor, matter lift, Hilbert current owner and species-blind measure", "MISSING_MATTER_SOURCE_OWNER", "J_A_bulk_envelope"),
        ("REQ2986_5_no_slots", "no source/shadow/marker slots", "typed no-Hom/sort-disjointness theorem forbidding hidden visible/source coefficient maps", "MISSING_NOHOM_SORT_THEOREM", "J_spurion;C_shadow_abs;eps_theta_basic"),
        ("REQ2986_6_boundary", "boundary/support/projector silence", "B_X primitive/edge theorem, support collar, Pi_M^H and readout-before-projection", "MISSING_BOUNDARY_PROJECTOR_OWNER", "epsilon_boundary_projector"),
        ("REQ2986_7_rank", "rank/coercive physical lock", "rank map and positive response operator controlling all physical residual channels", "MISSING_FULL_RANK_COERCIVITY", "epsilon_rank_lock"),
        ("REQ2986_8_arena", "arena projection operators", "R10/WEP/PPN/clock/orbital projection norms and units after upstream vector exists", "MISSING_ARENA_OPERATOR", "epsilon_arena_projection"),
    ]
    return [
        add(
            {
                "requirement_id": req_id,
                "required_object": obj,
                "acceptance_evidence": evidence,
                "current_status": status,
                "fallback_if_open": fallback,
                "promotion_allowed_now": False,
            }
        )
        for req_id, obj, evidence, status, fallback in data
    ]


def claim_rows() -> list[dict[str, Any]]:
    data = [
        ("CG2986_0_descent_certificate", "q/v_X/action descent certificate parent-signed", False, "verdict is NOT_PARENT_SIGNED_STAGE_EPSILON_VWEP"),
        ("CG2986_1_Cparent_zero", "C_parent_WEP DERIVED_ZERO import", False, "live C_parent import remains forbidden"),
        ("CG2986_2_local_GR", "local GR/Newton reduction", False, "epsilon_VWEP and rank/boundary/source residuals remain open"),
        ("CG2986_3_WEP_R10_PPN_clock_orbital", "local empirical pass", False, "arena operators and source-backed heads missing"),
        ("CG2986_4_public_claim", "public claim-grade local branch", False, "private nonclaim checkpoint only"),
    ]
    return [
        add(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "claim_allowed": False,
            }
        )
        for gate_id, claim, passed, status in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "decision_id": "DEC2986_0_keep_theorem",
                "decision": "Keep the descent theorem as the clean mathematical spine.",
                "because": "geometry and source-current silence are the same chain-rule theorem once q, v_X and matter action descent are parent-signed.",
                "next_action": "do not re-prove the conditional theorem; sign its premises or bound their leakage.",
            }
        ),
        add(
            {
                "decision_id": "DEC2986_1_refuse_zero_claim",
                "decision": "Do not claim C_parent_WEP=0, local GR, Newton, WEP, R10, PPN, clock or orbital pass.",
                "because": "the parent action object, actual generator, Dq matrix, matter/source owner, boundary/projector and rank map remain unsigned.",
                "next_action": "carry epsilon_VWEP rows as explicit nonclaim residuals.",
            }
        ),
        add(
            {
                "decision_id": "DEC2986_2_next_route",
                "decision": "Next route is a first sourced epsilon_VWEP component or the actual parent generator transformation law.",
                "because": "either path attacks the same bottleneck without smuggling in a plateau/local-GR axiom.",
                "next_action": "attempt parent generator law first; if it fails, fill the first finite leakage coefficient row.",
            }
        ),
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "next_id": "NEXT2986_0_2987",
                "priority": "selected_primary",
                "next_doc": "2987-Y5-R2FR-parent-generator-transformation-law-or-first-epsilon-VWEP-component-bound-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_parent_generator_transformation_law_or_first_epsilon_VWEP_component_bound_under_AX1090_2987.py",
                "objective": "Try to construct the actual field-by-field parent transformation law for v_X/V_WEP; if it cannot be signed, produce the first source-ready epsilon_VWEP component bound row with norm, units, source path and nonclaim status.",
                "include": "field-space chart;v_X action on geometry/matter/constants/source/boundary;Dq matrix hooks;epsilon component split;no-cancellation envelope",
                "exclude": "C_parent import;local-GR claim;theorem-zero promotion;GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [add({"copy_id": key, "path": str(path), "exists": path.exists()}) for key, path in BRANCH_OUTPUTS.items()]


def validation(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    csv_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
    generated = [*csv_paths, DOC]
    formal_count = sum(1 for path in FORMALIZATION.rglob("*2986*") if path.is_file()) if FORMALIZATION.exists() else 0
    verdict_staged = any(
        row["certificate_id"] == "QVX2986_10_verdict"
        and row["current_status"] == "NOT_PARENT_SIGNED_STAGE_EPSILON_VWEP"
        and not row["certificate_clause_signed"]
        for row in all_rows["certificate"]
    )
    epsilon_nonclaim = all(
        not row["valid_for_claim"]
        and row["current_value"] == "MISSING_SOURCE_BACKED_UPPER_BOUND"
        and not row["finite_value_present"]
        for row in all_rows["epsilon"]
    )
    checks = [
        ("VAL2986_0_sources_exist", all(row["exists"] for row in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2986_1_anchors_found", all(row["anchors_found"] for row in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2986_2_conditional_theorem_retained", any(row["theorem_id"] == "CDT2986_4_verdict" and row["current_status"] == "EXACT_CONDITIONAL_CURRENT_APPLICATION_BLOCKED" for row in all_rows["conditional"]), "conditional theorem retained but application blocked", True),
        ("VAL2986_3_certificate_not_signed", verdict_staged, "single q/v_X/action descent certificate not parent-signed", True),
        ("VAL2986_4_epsilon_nonclaim", epsilon_nonclaim, "epsilon_VWEP rows remain missing-source nonclaim rows", True),
        ("VAL2986_5_requirements_blocked", all(row["current_status"].startswith("MISSING_") for row in all_rows["requirements"]), "all bound input requirements remain explicit blockers", True),
        ("VAL2986_6_claims_blocked", all(not row["claim_allowed"] for row in all_rows["claims"]), "all claim gates blocked", True),
        ("VAL2986_7_no_live_cparent", not LIVE_C_PARENT.exists(), "C_parent_WEP_slot_import.csv not created or promoted", True),
        ("VAL2986_8_next_written", any(row["next_id"] == "NEXT2986_0_2987" for row in all_rows["next"]), "2987 next target written", True),
        ("VAL2986_9_branches_exist", all(row["exists"] for row in all_rows["branches"]), "branch copies exist", True),
        ("VAL2986_10_csvs_parse", all(csv_ok(path) for path in csv_paths), "all generated CSVs parse", True),
        ("VAL2986_11_outputs_under_post", all(under(path, ROOT) for path in generated), "all generated outputs under post-checkpoint-work", True),
        ("VAL2986_12_formalization_clean", formal_count == 0, f"no 2986 outputs in formalization-workbench (count={formal_count})", True),
        ("VAL2986_13_doc_written", DOC.exists(), "2986 markdown checkpoint exists", True),
    ]
    out_rows = [add({"validation_id": check_id, "passed": bool(passed), "check": check, "required": required}) for check_id, passed, check, required in checks]
    out_rows.append(add({"validation_id": "VAL2986_OVERALL", "passed": all(row["passed"] for row in out_rows), "check": "2986 validation overall", "required": True}))
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
        f"""# 2986 - q/v_X Action Descent Certificate or epsilon_VWEP Leakage Bound

Status: `Y5_R2FR_2986_q_vX_action_descent_exact_conditional_not_parent_signed_epsilon_VWEP_nonclaim_bound_rows_staged`

Claim ceiling: `no_qvX_action_descent_certificate_no_Cparent_DERIVED_ZERO_no_Cparent_import_no_local_GR_no_Newton_no_WEP_no_R10_no_PPN_no_clock_no_orbital_no_public_claim`

## Summary

- The clean theorem is now explicit: if `q`, `v_X`, action descent, matter descent, no-slot/no-shadow clauses, boundary/projector silence and rank lock are all parent-signed, then the local/WEP vertical source vanishes by chain rule.
- The current corpus does **not** sign those premises together; `q` is still partly formal, `V_WEP` is a candidate generator, and `Dq[v_X]=0` is exact only conditionally.
- Therefore this checkpoint refuses `C_parent_WEP = DERIVED_ZERO` and stages `epsilon_VWEP` as an explicit no-cancellation leakage envelope.
- The best next move is not more rhetoric: either derive the actual field-by-field parent transformation law, or source the first finite `epsilon_VWEP` component bound.

## Generated Outputs

{table(outputs, ["output", "path", "exists"])}

## Branch Copies

{table(branches, ["copy", "path", "exists"])}

## Conditional Descent Theorem

{table(all_rows["conditional"], ["theorem_id", "target", "current_status", "blocking_gap", "theorem_zero_adopted"])}

## q/v_X Action Descent Certificate Audit

{table(all_rows["certificate"], ["certificate_id", "clause", "current_status", "blocking_gap", "fallback_symbol", "certificate_clause_signed"])}

## epsilon_VWEP Nonclaim Bound Rows

{table(all_rows["epsilon"], ["epsilon_id", "symbol", "definition", "bound_interface", "current_value", "why_nonclaim"])}

## Bound Input Requirements

{table(all_rows["requirements"], ["requirement_id", "required_object", "current_status", "fallback_if_open", "promotion_allowed_now"])}

## Claim Gates

{table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

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
        "conditional": conditional_rows(),
        "certificate": certificate_rows(),
        "epsilon": epsilon_rows(),
        "requirements": requirement_rows(),
        "claims": claim_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])
    shutil.copyfile(OUTPUTS["certificate"], BRANCH_OUTPUTS["certificate_copy"])
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
    print(f"2986 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
