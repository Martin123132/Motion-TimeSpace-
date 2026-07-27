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

CHECKPOINT = "2911"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2911-Y5-R2FR-parent-field-chart-q-map-kernel-basis-or-finite-DqZ-norm-under-AX1090.md"

SRC_2910_DOC = ROOT / "2910-Y5-R2FR-Qvis-object-language-no-source-slot-or-finite-JH-DqZ-Y5Y6-vector-under-AX1090.md"
SRC_2910_NEXT = RESIDUALS / "P8_Y5_R2FR_2910_NEXT_TARGET.csv"
SRC_2910_QVIS = RESIDUALS / "P8_Y5_R2FR_2910_QVIS_OBJECT_LANGUAGE_GATE.csv"
SRC_2910_VECTOR = RESIDUALS / "P8_Y5_R2FR_2910_FINITE_JH_DQZ_Y5Y6_VECTOR.csv"
SRC_2901_DOC = ROOT / "2901-Y5-R2FR-parent-q-observed-stack-kernel-nullness-or-current-escape-bound-under-AX1090.md"
SRC_2901_CERT = RESIDUALS / "P8_Y5_R2FR_2901_Q_KERNEL_CERTIFICATE_GATE.csv"
SRC_2901_AUDIT = RESIDUALS / "P8_Y5_R2FR_2901_Q_KERNEL_NULLNESS_AUDIT.csv"
SRC_2901_LEAKS = RESIDUALS / "P8_Y5_R2FR_2901_Q_KERNEL_CURRENT_ESCAPE_ROWS.csv"
SRC_2885_DOC = ROOT / "2885-Y5-R2FR-DqZ-zero-theorem-or-first-factor-value-fill-under-AX1090.md"
SRC_2885_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2885_DQZ_ZERO_THEOREM_CONTRACT.csv"
SRC_2885_FACTOR = RESIDUALS / "P8_Y5_R2FR_2885_DQZ_FACTOR_VALUE_OR_BLOCKER_LEDGER.csv"
SRC_2886_COMPONENT = RESIDUALS / "P8_Y5_R2FR_2886_FIRST_FINITE_DQZ_COMPONENT_ROW_NONCLAIM.csv"
SRC_2887_DOBS = RESIDUALS / "P8_Y5_R2FR_2887_DOBS_KERNEL_THEOREM_ATTEMPT.csv"
SRC_1674_ANSATZ = RESIDUALS / "P8_Y5_PARENT_QLOC_1674_PARENT_Q_Z_MINIMAL_ANSATZ.csv"
SRC_1674_DERIV = RESIDUALS / "P8_Y5_PARENT_QLOC_1674_DQZ_COMPONENT_DERIVATIVE_MATRIX.csv"
SRC_1674_ZBASIS = RESIDUALS / "P8_Y5_PARENT_QLOC_1674_Z_BASIS_CANDIDATE.csv"
SRC_1674_CONSTRAINT = RESIDUALS / "P8_Y5_PARENT_QLOC_1674_CONSTRAINT_FIRST_ZERO_LEDGER.csv"
SRC_1673_COND = RESIDUALS / "P8_Y5_PARENT_QLOC_1673_DQZ_ZERO_THEOREM_CONDITIONS.csv"
SRC_1673_BLOCK = RESIDUALS / "P8_Y5_PARENT_QLOC_1673_DQZ_FACTOR_BLOCKER_LEDGER.csv"
SRC_1671_ZLOCK = RESIDUALS / "P8_Y5_PARENT_QLOC_1671_Z_BASIS_COMPONENT_LOCK_AUDIT.csv"
SRC_2670_ERASURE = RESIDUALS / "P8_Y5_R2FR_QUOTIENT_ERASURE_2670_ERASURE_CERTIFICATE_AUDIT.csv"
SRC_2867_DQ = RESIDUALS / "P8_Y5_R2FR_2867_QUOTIENT_DQ_GATE.csv"
SRC_2611_PREMISE = RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv"
SRC_2588_LEAKS = RESIDUALS / "P8_Y5_OBS_STACK_2588_SOURCE_LEAK_ROWS.csv"
SRC_2589_LEAKS = RESIDUALS / "P8_Y5_VERTICAL_KERNEL_2589_KERNEL_LEAK_ROWS.csv"
SRC_2590_CHARGE = RESIDUALS / "P8_Y5_VERTICAL_QV_2590_KERNEL_CHARGE_ROWS.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2911_SOURCE_REGISTER.csv",
    "field_chart": RESIDUALS / "P8_Y5_R2FR_2911_PARENT_FIELD_CHART_ATTEMPT.csv",
    "qmap": RESIDUALS / "P8_Y5_R2FR_2911_Q_MAP_DERIVATIVE_AUDIT.csv",
    "kernel_basis": RESIDUALS / "P8_Y5_R2FR_2911_KERNEL_BASIS_ATTEMPT.csv",
    "finite_dqz": RESIDUALS / "P8_Y5_R2FR_2911_FINITE_DQZ_NORM_VECTOR.csv",
    "arenas": RESIDUALS / "P8_Y5_R2FR_2911_ARENA_DQZ_PROJECTION_MAP.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2911_RUNNER_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2911_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2911_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2911_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2911_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2911_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "qmap_copy": PARENT_ACTION / "Parent_qmap_kernel_attempt_2911_NONCLAIM.csv",
    "dqz_copy": LOCAL_BOUNDS / "DqZ_norm_vector_2911_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2911_CONSTRAINT_FIRST_Z_ELIMINATION_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


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
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
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


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2911_00_2910_doc", SRC_2910_DOC, "NEXT2910_0_2911;QVIS2910_1_parent_q_map", "2910 handoff to parent q-map/kernel target"),
        ("SRC2911_01_2910_next", SRC_2910_NEXT, "NEXT2910_0_2911;q:Phi_parent->Q_vis", "machine-readable 2911 target"),
        ("SRC2911_02_2910_qvis", SRC_2910_QVIS, "QVIS2910_1_parent_q_map;QVIS2910_2_vertical_kernel_basis", "Qvis gate showing q and kernel blockers"),
        ("SRC2911_03_2910_vector", SRC_2910_VECTOR, "FV2910_0_DqZ;FV2910_TOTAL", "finite vector requiring Dq_Z_norm"),
        ("SRC2911_04_2901_doc", SRC_2901_DOC, "QK2901_0_q_map;QK2901_9_verdict", "parent q observed-stack kernel theorem audit"),
        ("SRC2911_05_2901_cert", SRC_2901_CERT, "CERT2901_0_q_map;CERT2901_10_no_tautology", "q/kernel certificate gate"),
        ("SRC2911_06_2901_audit", SRC_2901_AUDIT, "QK2901_0_q_map;QK2901_9_verdict", "q/kernel nullness audit"),
        ("SRC2911_07_2901_leaks", SRC_2901_LEAKS, "LEAK2901_1_rank_integrability;LEAK2901_TOTAL", "q-kernel current escape rows"),
        ("SRC2911_08_2885_doc", SRC_2885_DOC, "Dq_Z_norm=0;current MTS parent branch", "DqZ zero theorem verdict"),
        ("SRC2911_09_2885_contract", SRC_2885_CONTRACT, "DZC2885_1_parent_chart;DZC2885_9_verdict", "DqZ zero theorem clauses"),
        ("SRC2911_10_2885_factor", SRC_2885_FACTOR, "DQZF2885_0_Dq_Z_norm;DQZF2885_3_direct_tail_sum", "DqZ factor blocker ledger"),
        ("SRC2911_11_2886_component", SRC_2886_COMPONENT, "DQC2886_0_E_DqZ_coframe;MISSING_COMPONENT_VALUES", "first finite DqZ component row"),
        ("SRC2911_12_2887_dobs", SRC_2887_DOBS, "DOK2887_0_exact;DOK2887_4_verdict", "DObs kernel theorem attempt"),
        ("SRC2911_13_1674_ansatz", SRC_1674_ANSATZ, "QANS1674_0_parent_chart;QANS1674_4_constraint_first_route", "minimal parent q/Z ansatz"),
        ("SRC2911_14_1674_deriv", SRC_1674_DERIV, "DQM1674_0_coframe_metric;DQM1674_5_operator_norm", "component derivative matrix"),
        ("SRC2911_15_1674_zbasis", SRC_1674_ZBASIS, "ZB1674_0_q;ZB1674_5_coupling", "Z basis candidate"),
        ("SRC2911_16_1674_constraint", SRC_1674_CONSTRAINT, "CFZ1674_0_parent_constraint;CFZ1674_5_verdict", "constraint-first zero ledger"),
        ("SRC2911_17_1673_conditions", SRC_1673_COND, "ZC1673_0_parent_chart;ZC1673_6_norms", "DqZ zero theorem conditions"),
        ("SRC2911_18_1673_blockers", SRC_1673_BLOCK, "BLK1673_0_parent_q;BLK1673_6_boundary", "DqZ blocker ledger"),
        ("SRC2911_19_1671_zlock", SRC_1671_ZLOCK, "ZB1671_0_formal_Z;ZB1671_6_verdict", "Z basis component lock audit"),
        ("SRC2911_20_2670_erasure", SRC_2670_ERASURE, "QER2670_1_parent_quotient_map;QER2670_10_verdict", "absent quotient erasure failure"),
        ("SRC2911_21_2867_dq", SRC_2867_DQ, "DQ2867_0_chain_rule;DQ2867_4_verdict", "parent sigma/vertical generator Dq gate"),
        ("SRC2911_22_2611_premise", SRC_2611_PREMISE, "PRE2611_0_q_map;PRE2611_8_verdict", "matter descent q-map premise"),
        ("SRC2911_23_2588_leaks", SRC_2588_LEAKS, "OSL2588_0_q_owner;OSL2588_TOTAL", "observed-stack source leak rows"),
        ("SRC2911_24_2589_leaks", SRC_2589_LEAKS, "VKL2589_0_rank_integrability;VKL2589_TOTAL", "vertical kernel leak rows"),
        ("SRC2911_25_2590_charge", SRC_2590_CHARGE, "VQL2590_0_kernel_charge;VQL2590_TOTAL", "vertical Noether charge rows"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def field_chart_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PFC2911_0_domain",
            "Phi_parent",
            "Phi_parent=(Q_vis,Z^A,C_Z,lambda_Z,gauge,Psi_A,theta_A,A_owned,B_edge,P_loc)",
            "CANDIDATE_CHART_WRITTEN_NOT_PARENT_ACTION_OWNED",
            "1674 already has a minimal ansatz, but no parent action declares these as primitive/live/eliminated fields",
            "gives one place to test q and Dq rather than scattering labels",
        ),
        (
            "PFC2911_1_visible_target",
            "Q_vis",
            "Q_vis=(e_obs,g_obs,mu_m,D_m,J_H/source/readout data,theta_owned,A_owned)",
            "TARGET_OBJECT_SHARP_NOT_DERIVED",
            "ordinary matter/readout functor and no-marker/no-source-slot clauses remain unsigned",
            "if parent-owned, matter and readouts become q-basic candidates",
        ),
        (
            "PFC2911_2_residual_basis",
            "Z^A",
            "Z^A=(Z_q,Z_mu,Z_T,Z_PPN,Z_H,Z_c) spanning q_loc, Y5 GM/source, Y6 stress, PPN, boundary, coupling residuals",
            "CANDIDATE_BASIS_NOT_LIVE_PARENT_BASIS",
            "component lock/full-rank/coercive norm over physical residuals is missing",
            "names the exact residual directions that Dq must kill or bound",
        ),
        (
            "PFC2911_3_constraint_block",
            "C_Z(Phi)=0 with multiplier lambda_Z",
            "constraint-first branch eliminates Z before q/matter/readout if parent Euler equations and tangent space prove it",
            "BEST_ROUTE_CONDITIONAL_ONLY",
            "constraint origin, tangent proof, q factorization, source descent and boundary no-flux are unsigned",
            "least-scrutiny path because it removes Z before coupling rather than hiding it after",
        ),
        (
            "PFC2911_4_boundary_projector",
            "B_edge,P_loc",
            "boundary, corner, source-worldtube and local projector data are explicit chart objects, not silent omissions",
            "OPEN_CHART_COMPONENT",
            "no compact-local no-flux or projector descent theorem exists",
            "prevents boundary/projector leaks from being accidentally erased",
        ),
        (
            "PFC2911_5_theta_matter",
            "Psi_A,theta_A,A_owned",
            "ordinary matter fields, representation constants, clock/EM standards and owned gauge data live outside Z unless explicitly derived otherwise",
            "OWNERSHIP_UNSIGNED",
            "no-marker theorem and ordinary matter functor remain open",
            "keeps WEP/clock/EM channels visible in the finite bill",
        ),
        (
            "PFC2911_6_verdict",
            "parent field chart for current MTS",
            "the candidate chart is promoted as the parent field chart for theorem-grade DqZ zero",
            "NOT_PARENT_SIGNED_CANDIDATE_ONLY",
            "no parent action/constraint list makes the chart authoritative",
            "use as a workbench contract; do not use as proof",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for chart_id, object_name, candidate_definition, status, blocker, use in specs:
        rows.append(
            add_common(
                {
                    "chart_id": chart_id,
                    "object": object_name,
                    "candidate_definition": candidate_definition,
                    "current_status": status,
                    "blocking_gap": blocker,
                    "use_if_retained": use,
                    "parent_signed": False,
                    "promoted_to_theorem": False,
                }
            )
        )
    return rows


def qmap_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "QMAP2911_0_projection_form",
            "q:Phi_parent->Q_vis",
            "q(Phi) = Q_vis after the parent has declared the chart and after any constraint-first eliminations",
            "FORMAL_PROJECTION_AVAILABLE_NOT_PROOF",
            "projection onto a named Q_vis is tautological unless parent chart, constraints and readout order are independent",
            "epsilon_projection_declaration",
        ),
        (
            "QMAP2911_1_Dq_geometry",
            "Dq[Z_A] on e_obs,g_obs,connection,measure",
            "partial_Z(e_obs,g_obs,omega,mu_m)=0 if observed geometry is q-basic and Z is absent/eliminated before q",
            "CONDITIONAL_ZERO_NOT_ADOPTED",
            "observed coframe functor, no shadow frame and q/Z norms are unsigned",
            "DqZ_geometry",
        ),
        (
            "QMAP2911_2_Dq_source",
            "Dq[Z_A] on J_H/source normalization",
            "partial_Z(J_H,source strength,Pi_M,worldtube)=0 if source current descends through Q_vis and no source slot exists",
            "NOT_ZERO_ON_CURRENT_EVIDENCE",
            "J_M/J_H owner, source worldtube, no-source-slot and Pi_M equality are unsigned",
            "DqZ_source",
        ),
        (
            "QMAP2911_3_Dq_readout",
            "Dq[Z_A] on clocks, EM, photons, PPN, orbit readouts",
            "partial_Z(readout_i)=0 if readout-after-variation maps are Q_vis functors and markers are silent",
            "CONDITIONAL_ZERO_NOT_ADOPTED",
            "theta/marker and radiative/readout re-entry remain open",
            "DqZ_readout",
        ),
        (
            "QMAP2911_4_Dq_boundary",
            "Dq[Z_A] on boundary/projector/source support",
            "partial_Z(B_edge,P_loc,W_source)=0 only after compact-local no-flux/projector descent or inclusion in Q_vis",
            "NOT_ZERO_OR_UNPROVED",
            "boundary/corner/projector and source support terms remain independent",
            "DqZ_boundary_projector",
        ),
        (
            "QMAP2911_5_Dq_residual_lock",
            "Dq[Z_A] on physical residual vector",
            "Dq must control q_loc/Y5/Y6/PPN/boundary/coupling residuals through a full-rank component lock",
            "NOT_COMPUTED",
            "Z basis is not proven full-rank/coercive over physical residual channels",
            "DqZ_residual_lock",
        ),
        (
            "QMAP2911_6_operator_norm",
            "Dq_Z_norm",
            "Dq_Z_norm := sup_A ||Dq[v_A]||_q/||v_A||_Z with declared q norm, Z norm and tangent normalization",
            "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "q/Z norms, Dq matrix and source-backed interval are missing",
            "Dq_Z_norm",
        ),
        (
            "QMAP2911_7_verdict",
            "Dq matrix for current MTS",
            "Dq[v_Z]=0 for every selected residual generator in the current branch",
            "NOT_PARENT_SIGNED_FINITE_DQZ_REQUIRED",
            "field chart, q map, Z basis, constraint-first branch, source/readout descent, boundary and norms do not close together",
            "Delta_DqZ_operator_total",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for qmap_id, object_name, derivative_statement, status, blocker, residual in specs:
        rows.append(
            add_common(
                {
                    "qmap_id": qmap_id,
                    "object": object_name,
                    "derivative_statement": derivative_statement,
                    "current_status": status,
                    "blocking_gap": blocker,
                    "residual_if_missing": residual,
                    "source_paths": ";".join(str(p) for p in [SRC_1674_DERIV, SRC_2885_CONTRACT, SRC_2901_CERT]),
                    "theorem_zero_adopted": False,
                }
            )
        )
    return rows


def kernel_basis_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "KB2911_0_Zq",
            "Z_q",
            "q_loc source residual direction",
            "v_q acts on Gamma_eff/Khat/P_loc/q_loc sector while preserving Q_vis",
            "MISSING_GAMMA_EFF_KHAT_PLOC_OWNER_AND_DQ_ACTION",
            "CANDIDATE_NOT_LIVE_PARENT_BASIS",
        ),
        (
            "KB2911_1_Zmu",
            "Z_mu",
            "Y5 measured-GM/source normalization residual",
            "v_mu changes source-normalization residual but not Q_vis or Hilbert source if source-current owner closes",
            "SOURCE_CURRENT_ZERO_AND_GM_OUTPUT_GUARD_UNSIGNED",
            "CANDIDATE_NOT_LIVE_PARENT_BASIS",
        ),
        (
            "KB2911_2_ZT",
            "Z_T",
            "Y6 extra local stress/exterior metric residual",
            "v_T is vertical only if extra stress is constraint-owned or q-basic invisible",
            "Y6_STRESS_PARENT_SIGNATURE_MISSING",
            "CANDIDATE_NOT_LIVE_PARENT_BASIS",
        ),
        (
            "KB2911_3_ZPPN",
            "Z_PPN",
            "PPN residual vector",
            "v_PPN is vertical only after response operator maps residuals to zero/bounded PPN perturbations",
            "NO_RESPONSE_OPERATOR_OR_PPN_KERNEL",
            "CANDIDATE_NOT_LIVE_PARENT_BASIS",
        ),
        (
            "KB2911_4_ZH",
            "Z_H",
            "boundary/harmonic/source-measure residual",
            "v_H is vertical only if boundary/projector/source-measure flux is exact, proper or bounded",
            "BOUNDARY_PROJECTOR_OPEN",
            "CANDIDATE_NOT_LIVE_PARENT_BASIS",
        ),
        (
            "KB2911_5_Zc",
            "Z_c",
            "matter/source/readout coupling residual",
            "v_c is vertical only if no-source-slot, no-marker and source/readout descent close",
            "MATTER_SOURCE_DESCENT_AND_NO_SOURCE_SLOT_MISSING",
            "CANDIDATE_NOT_LIVE_PARENT_BASIS",
        ),
        (
            "KB2911_6_rank_bracket",
            "V=span{v_A}",
            "regular kernel distribution",
            "rank(Dq) is constant and [v_A,v_B] lies in V with source-backed structure functions",
            "MISSING_RANK_BRACKET_AND_FIELDSPACE_CURL_AUDIT",
            "NOT_A_REGULAR_QUOTIENT_YET",
        ),
        (
            "KB2911_7_presymplectic_null",
            "V subset ker Omega_red or Q_v flux zero",
            "vertical directions carry no compact local charge",
            "int_S(delta Q_v-i_v Theta_parent+delta B_v+C_v)=0 or source-backed bounded",
            "MISSING_THETA_PARENT_QV_ZERO_FLUX_CERTIFICATE",
            "NOT_PRESYMPLECTIC_NULL_YET",
        ),
        (
            "KB2911_8_verdict",
            "ker(Dq) basis for current MTS",
            "selected v_A are actual parent field variations spanning ker(Dq)",
            "MISSING_PARENT_KERNEL_BASIS",
            "basis labels are useful but not live variations",
            "FINITE_DQZ_AND_KERNEL_ESCAPE_ROWS_REQUIRED",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for basis_id, symbol, physical_channel, candidate_action, blocker, status in specs:
        rows.append(
            add_common(
                {
                    "basis_id": basis_id,
                    "basis_symbol": symbol,
                    "physical_channel": physical_channel,
                    "candidate_action": candidate_action,
                    "current_status": status,
                    "blocking_gap": blocker,
                    "source_paths": ";".join(str(p) for p in [SRC_1674_ZBASIS, SRC_1671_ZLOCK, SRC_2901_AUDIT]),
                    "parent_signed": False,
                    "Dq_kernel_claimed": False,
                }
            )
        )
    return rows


def finite_dqz_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DQZ2911_0_Dq_Z_norm",
            "Dq_Z_norm",
            "operator norm of selected residual directions through the visible quotient map",
            "dimensionless_after_q_and_Z_norms",
            "sup_A ||Dq[v_A]||_q/||v_A||_Z",
            "MISSING_PARENT_Q_MAP_DQ_MATRIX_Z_NORMS",
            "all_local_arenas",
        ),
        (
            "DQZ2911_1_DqZ_geometry",
            "DqZ_geometry",
            "geometry/coframe/metric/measure derivative leakage",
            "dimensionless_frame_or_metric_response",
            "||partial_Z(e_obs,g_obs,omega,mu_m)||",
            "MISSING_OBSERVED_GEOMETRY_FUNCTOR_AND_NO_SHADOW_CERTIFICATE",
            "PPN;clock;orbital;local_GR",
        ),
        (
            "DQZ2911_2_DqZ_source",
            "DqZ_source",
            "Hilbert/source normalization/source-worldtube derivative leakage",
            "source-current-normalized",
            "||partial_Z(J_H,Pi_M,W_source,source calibration)||/||J_ref||",
            "MISSING_SOURCE_CURRENT_OWNER_WORLDTUBE_AND_NO_SOURCE_SLOT",
            "Newton;WEP;R10;orbital",
        ),
        (
            "DQZ2911_3_DqZ_readout",
            "DqZ_readout",
            "clock/EM/photon/orbit/PPN readout derivative leakage",
            "arena_specific_readout_units",
            "||partial_Z R_readout|| plus marker/radiative tail",
            "MISSING_READOUT_DESCENT_AND_NO_MARKER_THEOREM",
            "clock;EM;PPN;WEP;orbital",
        ),
        (
            "DQZ2911_4_DqZ_boundary_projector",
            "DqZ_boundary_projector",
            "boundary/projector/source-support derivative leakage",
            "boundary_or_projector_units",
            "||partial_Z(B_edge,P_loc,W_source)||",
            "MISSING_BOUNDARY_NOFLUX_PROJECTOR_DESCENT",
            "R10;orbital;PPN;local_GR",
        ),
        (
            "DQZ2911_5_DqZ_residual_lock",
            "DqZ_residual_lock",
            "failure of Z basis to control physical residual vector full-rank/coercively",
            "operator_norm_or_condition_number",
            "||R_phys - L_Z Z|| + cond(L_Z) guard",
            "MISSING_Z_COMPONENT_LOCK_AND_NORM_EQUIVALENCE",
            "q_loc;Y5;Y6;PPN;boundary;coupling",
        ),
        (
            "DQZ2911_6_rank_integrability",
            "epsilon_q_rank_or_integrability",
            "regular quotient rank/bracket defect",
            "field-space_quotient_defect",
            "||[v_A,v_B] mod V|| + ||rank(Dq)-rank_expected||",
            "MISSING_VERTICAL_BASIS_BRACKET_TABLE_RANK_AUDIT",
            "q_owner;Obs_e;PPN;local_GR",
        ),
        (
            "DQZ2911_7_kernel_charge",
            "epsilon_kernel_charge",
            "compact local charge carried by would-be vertical directions",
            "dimensionless_Hamiltonian_charge_leakage",
            "|int_S(delta Q_v - i_v Theta_parent + delta B_v + C_v)|/M_ref",
            "MISSING_THETA_PARENT_QV_ZERO_FLUX_MREF",
            "Newton;PPN;R10;clock;orbital;local_GR",
        ),
        (
            "DQZ2911_8_projection_guard",
            "epsilon_projection_declaration",
            "boolean guard against defining q from observed success variables before kernel proof",
            "boolean_guard",
            "1 if q/Obs stack is used as proof object before independent kernel certificates pass else 0",
            "ANTI_TAUTOLOGY_GUARD_ACTIVE",
            "q_owner;same_frame;local_GR",
        ),
        (
            "DQZ2911_TOTAL",
            "Delta_DqZ_kernel_total",
            "absolute no-cancellation DqZ/q-kernel residual envelope",
            "dimensionless_after_declared_normalization",
            "sum_abs(DQZ2911_0..DQZ2911_8) with no cancellation and no GM/G_N absorption",
            "COMPONENTS_MISSING_NONCLAIM",
            "all_local_arenas",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, symbol, definition, units, formula, missing, arenas in specs:
        rows.append(
            add_common(
                {
                    "row_id": row_id,
                    "symbol": symbol,
                    "definition": definition,
                    "units": units,
                    "formula_or_bound": formula,
                    "current_value": missing,
                    "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                    "source_paths": ";".join(str(p) for p in [SRC_2885_FACTOR, SRC_1674_DERIV, SRC_2901_LEAKS, SRC_2589_LEAKS]),
                    "observable_link": arenas,
                    "promotion_rule": "theorem-zero from parent q/kernel proof or source-backed finite interval with units and no MISSING markers",
                    "current_status": "STAGED_NONCLAIM_ROW",
                    "theorem_zero_adopted": False,
                    "finite_value_present": False,
                    "prediction_source_backed": False,
                    "accepted_for_scoring": False,
                }
            )
        )
    return rows


def arena_rows() -> list[dict[str, Any]]:
    specs = [
        ("A2911_0_Newton", "Newton/local GM", "Delta_GM <= Pi_GM(DqZ_source + kernel_charge + boundary + projection_guard)", "MISSING_SOURCE_CURRENT_AND_Q_KERNEL_OWNER", "no orbital/fitted GM absorption"),
        ("A2911_1_PPN", "PPN gamma/beta/preferred-frame", "Delta_PPN <= Pi_PPN(DqZ_geometry + DqZ_readout + DqZ_boundary_projector + Y6 stress tail)", "MISSING_GEOMETRY_READOUT_KERNEL", "metric-looking success cannot hide source/readout leaks"),
        ("A2911_2_WEP", "WEP/composition", "eta_AB <= Pi_WEP(DqZ_source + DqZ_readout + no-source-slot/marker tails)", "NO_SOURCE_SLOT_AND_MARKER_STILL_OPEN", "coupling/source throat remains explicit"),
        ("A2911_3_R10", "R10/contact/source-test", "R10 rows require DqZ_source, boundary/projector and source/test charge split before alpha(lambda) scoring", "R10_HELD_NONCLAIM", "no bound-anchor shortcut"),
        ("A2911_4_clock_EM", "clock/time/EM", "Delta_clock/alpha_EM <= Pi_clock(DqZ_readout + theta marker + geometry coframe leak)", "READOUT_THETA_DESCENT_UNSIGNED", "charge/clock route remains citation/source backed later"),
        ("A2911_5_orbital", "orbital/light-time", "Delta_orbit <= Pi_orbit(DqZ_geometry + DqZ_source + boundary support)", "SOURCE_SUPPORT_BOUNDARY_OWNER_UNSIGNED", "local tests need same source/worldtube branch"),
        ("A2911_6_local_GR", "local GR/Newton reduction", "local GR requires Dq_Z_norm=0 or finite vector below arena tolerances plus source-current/Y5/Y6 closure", "BLOCKED_NONCLAIM", "2911 is an upstream map attempt, not a GR proof"),
    ]
    return [
        add_common(
            {
                "arena_id": arena_id,
                "arena": arena,
                "projection_or_gate": projection,
                "current_status": status,
                "guardrail": guardrail,
                "missing_inputs": "parent q map; Dq matrix; live Z basis; q/Z norms; source/readout descent; boundary/projector silence",
            }
        )
        for arena_id, arena, projection, status, guardrail in specs
    ]


def runner_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_sources_ready = all(bool(row["path_exists"]) and bool(row["anchors_found"]) for row in source_rows)
    specs = [
        ("RUN2911_0_sources", "SOURCE_AUDIT_COMPLETE" if all_sources_ready else "SOURCE_AUDIT_HAS_BLOCKERS", "all cited source paths and anchors", all_sources_ready, "source evidence checked before promotion"),
        ("RUN2911_1_parent_chart", "PARENT_FIELD_CHART_CANDIDATE_WRITTEN_NOT_SIGNED", "Phi_parent and Q_vis candidate", False, "candidate is not backed by a parent action/constraint declaration"),
        ("RUN2911_2_qmap_Dq", "QMAP_DQ_ATTEMPTED_NOT_COMPUTABLE", "q map, Dq component derivatives, q/Z norms", False, "Dq matrix rows remain missing numeric/theorem-zero values"),
        ("RUN2911_3_kernel_basis", "KERNEL_BASIS_ATTEMPTED_NOT_LIVE", "Z_q,Z_mu,Z_T,Z_PPN,Z_H,Z_c plus rank/bracket", False, "basis labels are not parent field variations"),
        ("RUN2911_4_finite_vector", "FINITE_DQZ_VECTOR_STAGED_NONCLAIM", "DqZ geometry/source/readout/boundary/residual/norm rows", False, "component values and source-backed upper bounds missing"),
        ("RUN2911_5_next", "CONSTRAINT_FIRST_Z_ELIMINATION_SELECTED", "2912 target", False, "best derivation-first path is proving Z is eliminated before q/matter/readout"),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "status": status,
                "required_components": required,
                "components_evaluable": evaluable,
                "reason": reason,
            }
        )
        for runner_id, status, required, evaluable, reason in specs
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2911_0_conditional_chain_rule", "if q is parent-defined and v_Z in ker(Dq), q-basic observables have zero vertical derivative", "PASS_CONDITIONAL_ONLY", "standard chain rule/control theorem is valid but premises are unsigned", True),
        ("CG2911_1_parent_chart", "current MTS has an authoritative parent field chart for Q_vis/Z", "BLOCKED_NONCLAIM", "candidate chart is not parent-action signed", False),
        ("CG2911_2_qmap_Dq", "q and Dq matrix are computable for selected residual generators", "BLOCKED_NONCLAIM", "Dq component derivative matrix and norm convention are missing", False),
        ("CG2911_3_kernel_basis", "selected Z directions are live parent variations in ker(Dq)", "BLOCKED_NONCLAIM", "Z basis component lock, full-rank/coercive norm and field actions are missing", False),
        ("CG2911_4_constraint_first", "Z is eliminated before q/matter/readout", "BLOCKED_NONCLAIM", "constraint origin, tangent proof and q factorization are unsigned", False),
        ("CG2911_5_DqZ_zero", "Dq_Z_norm=0 for current MTS", "BLOCKED_NONCLAIM", "q map, kernel basis, source/readout descent, boundary and norms do not close together", False),
        ("CG2911_6_finite_DqZ_score", "finite DqZ vector is score-ready", "BLOCKED_NONCLAIM", "no source-backed upper bounds or arena coefficients", False),
        ("CG2911_7_local_GR_Newton", "local GR/Newton follows after 2911", "BLOCKED_NONCLAIM", "2911 supplies a map contract and residual rows only", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": status,
                "reason": reason,
                "gate_pass": gate_pass,
            }
        )
        for gate_id, claim, status, reason, gate_pass in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2911_0_result",
            "PARENT_QMAP_NOT_SIGNED",
            "The best candidate chart/q map can be written, but promoting it would be projection by declaration without a parent action, constraint, Dq matrix and kernel basis.",
            "keep candidate as contract only",
        ),
        (
            "DEC2911_1_real_gain",
            "DqZ_BILL_LOCALISED",
            "Dq_Z_norm is no longer an abstract missing symbol: it splits into geometry, source, readout, boundary/projector, residual-lock, rank and kernel-charge components.",
            "use finite vector for future score gates",
        ),
        (
            "DEC2911_2_derivation_route",
            "CONSTRAINT_FIRST_ROUTE_BEST",
            "The least-scrutiny route is to prove C_Z eliminates Z before q/matter/readout, because a raw q projection would look like a closure axiom.",
            "attack parent constraint origin and tangent-space proof next",
        ),
        (
            "DEC2911_3_guard",
            "NO_PROJECTION_BY_DECLARATION",
            "q=(Q_vis) is not proof unless Q_vis and ker(Dq) are independently parent-owned and regular.",
            "do not claim Dq_Z_norm=0 from notation",
        ),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2911_0_2912",
                "selection_status": "selected_primary",
                "target_file": "2912-Y5-R2FR-constraint-first-Z-elimination-or-first-DqZ-component-bound-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_constraint_first_Z_elimination_or_first_DqZ_component_bound_under_AX1090_2912.py",
                "task": "try to derive parent constraint C_Z(Phi)=0 and tangent-space elimination before q/matter/readout; if it fails, fill the first DqZ component bound row with explicit source requirements",
                "success_condition": "parent action supplies C_Z, multiplier/signature, tangent condition delta C_Z=0, q factorization on C_Z=0, and source/readout/boundary silence in one branch",
                "fallback_condition": "DqZ_geometry or DqZ_source receives a nonclaim bound-input row with units, coefficient origin and source path requirements",
                "guardrails": "no post-readout deletion; no closure axiom; no plateau axiom; no empirical scoring; no GM/G_N absorption; no GitHub; no formalization-workbench edits",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("qmap_copy", OUTPUTS["qmap"], BRANCH_OUTPUTS["qmap_copy"]),
        ("dqz_copy", OUTPUTS["finite_dqz"], BRANCH_OUTPUTS["dqz_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination in specs:
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "destination_path": str(destination),
                    "source_exists": source.exists(),
                    "destination_exists": destination.exists(),
                    "destination_parses": csv_parses(destination),
                }
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    field_rows: list[dict[str, Any]],
    qmap_rows_: list[dict[str, Any]],
    kernel_rows: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    include_doc_check: bool,
) -> list[dict[str, Any]]:
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_outputs_with_validation = [*csv_outputs, OUTPUTS["validation"]]
    required_symbols = {
        "Dq_Z_norm",
        "DqZ_geometry",
        "DqZ_source",
        "DqZ_readout",
        "DqZ_boundary_projector",
        "DqZ_residual_lock",
        "epsilon_q_rank_or_integrability",
        "epsilon_kernel_charge",
        "epsilon_projection_declaration",
        "Delta_DqZ_kernel_total",
    }
    finite_symbols = {str(row["symbol"]) for row in finite_rows}
    chart_verdict = next(row for row in field_rows if row["chart_id"] == "PFC2911_6_verdict")
    qmap_verdict = next(row for row in qmap_rows_ if row["qmap_id"] == "QMAP2911_7_verdict")
    kernel_verdict = next(row for row in kernel_rows if row["basis_id"] == "KB2911_8_verdict")
    local_claim = next(row for row in claim_rows_ if row["gate_id"] == "CG2911_7_local_GR_Newton")
    checks = [
        ("VAL2911_0_source_paths_exist", all(bool(row["path_exists"]) for row in source_rows), "all cited source paths exist"),
        ("VAL2911_1_source_anchors_found", all(bool(row["anchors_found"]) for row in source_rows), "all source anchors found"),
        ("VAL2911_2_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs_with_validation if path.exists()), "generated CSV outputs parse cleanly"),
        ("VAL2911_3_chart_not_promoted", chart_verdict["current_status"] == "NOT_PARENT_SIGNED_CANDIDATE_ONLY" and not bool(chart_verdict["parent_signed"]), "parent field chart remains candidate-only"),
        ("VAL2911_4_qmap_not_promoted", qmap_verdict["current_status"] == "NOT_PARENT_SIGNED_FINITE_DQZ_REQUIRED" and not bool(qmap_verdict["theorem_zero_adopted"]), "q map/Dq zero remains unpromoted"),
        ("VAL2911_5_kernel_not_promoted", kernel_verdict["current_status"] == "FINITE_DQZ_AND_KERNEL_ESCAPE_ROWS_REQUIRED" and not bool(kernel_verdict["Dq_kernel_claimed"]), "kernel basis remains unclaimed"),
        ("VAL2911_6_finite_DqZ_complete", required_symbols.issubset(finite_symbols), "finite DqZ vector has required components"),
        (
            "VAL2911_7_claim_gates_safe",
            local_claim["gate_status"] == "BLOCKED_NONCLAIM"
            and all(not bool(row["claim_allowed"]) and not bool(row["valid_for_claim"]) for row in claim_rows_),
            "local GR/Newton and empirical claims remain blocked",
        ),
        ("VAL2911_8_next_target_selected", next_rows_[0]["route_id"] == "NEXT2911_0_2912" and bool(next_rows_[0]["selected"]), "2912 constraint-first target selected"),
        ("VAL2911_9_branch_copies_parse", all(bool(row["destination_exists"]) and bool(row["destination_parses"]) for row in branch_rows_), "branch copies exist and parse"),
        ("VAL2911_10_no_formalization_outputs", not any(is_under(path, FORMALIZATION) for path in [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC]), "no generated output path is inside formalization-workbench"),
        ("VAL2911_11_doc_written", DOC.exists() if include_doc_check else True, "markdown checkpoint exists"),
    ]
    rows: list[dict[str, Any]] = [
        {
            "validation_id": validation_id,
            "status": bool(status),
            "detail": detail,
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
        for validation_id, status, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2911_OVERALL",
            "status": all(bool(row["status"]) for row in rows),
            "detail": "2911 validation overall",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    field_rows: list[dict[str, Any]],
    qmap_rows_: list[dict[str, Any]],
    kernel_rows: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    arena_rows_: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2911_OVERALL")
    text = f"""# 2911 - Y5/R2FR Parent Field Chart q-Map Kernel Basis Or Finite DqZ Norm Under AX1090

Status: `Y5_R2FR_2911_parent_qmap_candidate_not_signed_finite_DqZ_kernel_vector_staged_2912_next`

Claim ceiling: `parent_qmap_kernel_nonclaim_only_no_DqZ_zero_no_kernel_basis_no_constraint_first_elimination_no_Newton_no_PPN_no_R10_no_local_GR_no_GitHub_claim`

Generated UTC: `{RUN_UTC}`

## Summary

2911 tries the upstream route selected by 2910: write the parent field chart, the map `q:Phi_parent -> Q_vis`, the derivative `Dq`, and the selected residual kernel basis. The clean theorem is still simple:

`v_Z in ker(Dq)` and `Obs=Obs(Q_vis)` imply `DObs[v_Z]=DObs[Dq(v_Z)]=0`.

The problem is not the mathematics. The problem is ownership. Current MTS can write a sensible candidate chart, but it still cannot promote that chart to a parent-action theorem without an explicit parent action/constraint list, a computable `Dq` matrix, a live `Z` basis, a rank/bracket audit, q/Z norm conventions, source/readout descent and boundary/projector silence.

So 2911 refuses the cheap move `q=(the variables we want visible)`. That would be projection by declaration. Instead it stages `Dq_Z_norm` as a finite operator vector and selects the cleaner derivation path: prove a constraint-first `C_Z(Phi)=0` branch that removes `Z` before q/matter/readout are formed.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "anchors_found", "role", "missing_anchors"])}

## Parent Field Chart Attempt

{md_table(field_rows, ["chart_id", "object", "candidate_definition", "current_status", "blocking_gap", "use_if_retained", "parent_signed", "valid_for_claim"])}

## q-Map Derivative Audit

{md_table(qmap_rows_, ["qmap_id", "object", "derivative_statement", "current_status", "blocking_gap", "residual_if_missing", "theorem_zero_adopted", "valid_for_claim"])}

## Kernel Basis Attempt

{md_table(kernel_rows, ["basis_id", "basis_symbol", "physical_channel", "candidate_action", "current_status", "blocking_gap", "Dq_kernel_claimed", "valid_for_claim"])}

## Finite DqZ Norm Vector

{md_table(finite_rows, ["row_id", "symbol", "definition", "units", "formula_or_bound", "current_value", "upper_bound", "observable_link", "current_status", "valid_for_claim"])}

## Arena Map

{md_table(arena_rows_, ["arena_id", "arena", "projection_or_gate", "current_status", "guardrail", "valid_for_claim"])}

## Runner Status

{md_table(runner_rows_, ["runner_id", "status", "required_components", "components_evaluable", "reason", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows_, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"])}

## Decision Ledger

{md_table(decision_rows_, ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(next_rows_, ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows_, ["copy_id", "source_path", "destination_path", "destination_exists", "destination_parses", "valid_for_claim"])}

## Validation

{md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim"])}

Validation overall: `{overall["status"]}`.

## Interpretation

This is a good failure, not a dead-end failure. We now know the exact missing object: not "some coupling magic", but a parent-owned quotient package. A claim-grade local branch needs `Phi_parent`, `q`, `Dq`, `ker(Dq)`, rank/bracket regularity, matter/source/readout descent, boundary silence and norm conventions in one branch.

The best leap forward is constraint-first elimination. If `C_Z(Phi)=0` is derived from the parent action and its tangent space preserves `q`, then `Dq_Z_norm=0` can become a theorem without pretending the observed stack is fundamental by definition.

## Not Claimed

- The candidate `Phi_parent` chart is not promoted to a parent action.
- `q`, `Dq`, `ker(Dq)` and `Dq_Z_norm=0` are not proved for current MTS.
- The selected `Z` basis is not a live parent field-variation basis.
- Newton, PPN, R10, WEP, clock/EM, orbital or local-GR reduction is not claimed.
- No public/GitHub action is implied.
- No file in `formalization-workbench` is modified by this checkpoint.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    field_rows = field_chart_rows()
    qmap_rows_ = qmap_rows()
    kernel_rows = kernel_basis_rows()
    finite_rows = finite_dqz_rows()
    arena_rows_ = arena_rows()
    runner_rows_ = runner_rows(source_rows)
    claim_rows_ = claim_rows()
    decision_rows_ = decision_rows()
    next_rows_ = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["field_chart"], field_rows)
    write_csv(OUTPUTS["qmap"], qmap_rows_)
    write_csv(OUTPUTS["kernel_basis"], kernel_rows)
    write_csv(OUTPUTS["finite_dqz"], finite_rows)
    write_csv(OUTPUTS["arenas"], arena_rows_)
    write_csv(OUTPUTS["runner"], runner_rows_)
    write_csv(OUTPUTS["claims"], claim_rows_)
    write_csv(OUTPUTS["decision"], decision_rows_)
    write_csv(OUTPUTS["next"], next_rows_)

    branch_rows_ = branch_rows()
    write_csv(OUTPUTS["branches"], branch_rows_)

    validation_rows_ = validation_rows(
        source_rows,
        field_rows,
        qmap_rows_,
        kernel_rows,
        finite_rows,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=False,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        field_rows,
        qmap_rows_,
        kernel_rows,
        finite_rows,
        arena_rows_,
        runner_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    validation_rows_ = validation_rows(
        source_rows,
        field_rows,
        qmap_rows_,
        kernel_rows,
        finite_rows,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=True,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        field_rows,
        qmap_rows_,
        kernel_rows,
        finite_rows,
        arena_rows_,
        runner_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2911_OVERALL")
    if not bool(overall["status"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
