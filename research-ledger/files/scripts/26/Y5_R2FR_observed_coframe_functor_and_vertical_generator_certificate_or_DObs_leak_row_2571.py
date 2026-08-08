from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_OBSERVED_COFRAME_FUNCTOR_2571"
CHECKPOINT_ID = "2571"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2571-Y5-R2FR-observed-coframe-functor-and-vertical-generator-certificate-or-DObs-leak-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_OBS_COFRAME_2571_SOURCE_REGISTER.csv",
    "functor_attempt": OUT / "P8_Y5_OBS_COFRAME_2571_FUNCTOR_ATTEMPT.csv",
    "vertical_generators": OUT / "P8_Y5_OBS_COFRAME_2571_VERTICAL_GENERATOR_TABLE.csv",
    "dobs_kernel": OUT / "P8_Y5_OBS_COFRAME_2571_DOBS_KERNEL_GATE.csv",
    "no_shadow": OUT / "P8_Y5_OBS_COFRAME_2571_NO_SHADOW_FRAME_GATE.csv",
    "finite_leaks": OUT / "P8_Y5_OBS_COFRAME_2571_FINITE_DOBS_LEAK_ROWS.csv",
    "projection_interface": OUT / "P8_Y5_OBS_COFRAME_2571_PROJECTION_INTERFACE.csv",
    "claim_gates": OUT / "P8_Y5_OBS_COFRAME_2571_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_OBS_COFRAME_2571_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_OBS_COFRAME_2571_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_OBS_COFRAME_2571_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2571_VALIDATION.csv",
}

COPY_TARGETS = {
    "functor_attempt": LOCAL_BOUNDS / "Observed_coframe_functor_attempt_2571_NONCLAIM.csv",
    "vertical_generators": LOCAL_BOUNDS / "Observed_coframe_vertical_generator_table_2571_NONCLAIM.csv",
    "finite_leaks": LOCAL_BOUNDS / "Finite_DObs_leak_rows_2571_NONCLAIM.csv",
    "projection_interface": LOCAL_BOUNDS / "Common_frame_projection_interface_2571_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2571_TERMINAL_PUBLIC_COFRAME_OR_COMMON_FRAME_KERNEL.csv",
}

SOURCES = [
    {
        "source_id": "SRC2571_00_2570_doc",
        "source_path": ROOT / "2570-Y5-R2FR-parent-field-sort-and-quotient-map-signature-or-residual-owner-split.md",
        "needles": ["NEXT2570_0_selected", "DQ2570_3_RAB", "RS2570_9_coupling_owner", "VAL2570_OVERALL"],
        "role": "active handoff selecting observed coframe/readout functor with coupling directions",
    },
    {
        "source_id": "SRC2571_01_2487_precedent",
        "source_path": ROOT / "2487-Y5-R2FR-observed-coframe-functor-and-vertical-generator-certificate-or-DObs-leak-row.md",
        "needles": ["FUN2487_0_chain_rule", "DLEAK2487_4_common_frame_abs", "VAL2487_OVERALL"],
        "role": "earlier observed-coframe theorem and finite DObs leak precedent",
    },
    {
        "source_id": "SRC2571_02_1738_kernel",
        "source_path": ROOT / "1738-Y5-R2FR-observed-coframe-kernel-zero-or-first-finite-DObs-e-row.md",
        "needles": ["DOBS_E_KERNEL_ZERO_NOT_SIGNED", "SAME_COFRAME_IS_NOT_ENOUGH", "VAL1738_OVERALL"],
        "role": "same-frame countermodel and kernel-zero blocker",
    },
    {
        "source_id": "SRC2571_03_1878_qshape",
        "source_path": ROOT / "1878-Y5-R2FR-qshape-readout-functor-kernel-or-parent-category-principle.md",
        "needles": ["CKT1878_0_chain_rule", "CKT1878_5_verdict", "VAL1878_OVERALL"],
        "role": "R_AB/q_shape readout kernel failure",
    },
    {
        "source_id": "SRC2571_04_1879_coframe_owner",
        "source_path": ROOT / "1879-Y5-R2FR-parent-coframe-ownership-or-common-frame-leak-bound.md",
        "needles": ["PCO1879_1_coframe_owner", "CFL1879_0_bR", "VAL1879_OVERALL"],
        "role": "parent coframe ownership and common-frame leakage rows",
    },
    {
        "source_id": "SRC2571_05_1880_terminal",
        "source_path": ROOT / "1880-Y5-R2FR-terminal-public-coframe-no-shadow-frame-or-bg-bound-projection.md",
        "needles": ["TPC1880_0_terminal_object", "ZTH1880_0_exact_conditional", "VAL1880_OVERALL"],
        "role": "terminal public coframe/no-shadow theorem template",
    },
    {
        "source_id": "SRC2571_06_1933_coefficient_descent",
        "source_path": ROOT / "1933-Y5-R2FR-coefficient-descent-typing-proof-or-finite-source-row-selection.md",
        "needles": ["QDT1933_1_vertical_zero", "TYPE1933_4_verdict", "VAL1933_OVERALL"],
        "role": "visible coefficient/coupling descent criterion",
    },
    {
        "source_id": "SRC2571_07_2568_source_norm",
        "source_path": ROOT / "2568-Y5-R2FR-Hilbert-worldtube-source-normalization-zero-certificate-or-Enorm-row.md",
        "needles": ["ENORM2568_1_e_kappaG", "ENORM2568_2_e_ellJ_owner", "VAL2568_OVERALL"],
        "role": "current kappa and ellJ source-normalization blockers",
    },
    {
        "source_id": "SRC2571_08_2570_validation",
        "source_path": OUT / "P8_Y5_BRR545_2570_VALIDATION.csv",
        "needles": ["VAL2570_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, **row}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:
        return False, 0, str(error)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def functor_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "functor_id": "FUN2571_0_chain_rule",
            "target": "all ordinary local observables",
            "required_functor": "Obs=Obs_bar(q_parent(Phi)); in particular e_obs=E(q_parent(Phi))",
            "theorem_status": "EXACT_CONDITIONAL",
            "proof_or_failure": "for v in ker(Dq_parent), DObs[v]=DObs_bar(Dq_parent[v])=DObs_bar(0)=0",
            "missing_parent_input": "q_parent, E, Obs_bar and field-by-field vertical generators are not parent-signed",
            "valid_for_claim": False,
        },
        {
            "functor_id": "FUN2571_1_terminal_public_coframe",
            "target": "visible metric/coframe carrier",
            "required_functor": "ordinary matter, rods, clocks, photons, source currents and orbits factor through one terminal e_pub=E(Q_vis)",
            "theorem_status": "CANDIDATE_NOT_DERIVED",
            "proof_or_failure": "terminal public coframe would remove hidden frame arguments, but current parent action does not yet exclude them",
            "missing_parent_input": "no C_R/J_q Weyl, disformal, source-prefactor, endpoint, post-readout or coupling slot in ordinary readout",
            "valid_for_claim": False,
        },
        {
            "functor_id": "FUN2571_2_RAB_qshape",
            "target": "R_AB/J_q direction",
            "required_functor": "q_shape forgets R_AB/J_q and e_obs is q_shape-basic",
            "theorem_status": "FAIL_CURRENT_CORPUS",
            "proof_or_failure": "Dq_shape[v_R]=0 does not prove DObs_e[v_R]=0; 2570 keeps R_AB visible under the current observer-cell map",
            "missing_parent_input": "q-basic coframe functor or constraint-first elimination before readout",
            "valid_for_claim": False,
        },
        {
            "functor_id": "FUN2571_3_same_frame_warning",
            "target": "single common frame",
            "required_functor": "same observed frame must be independent of hidden/residual variables",
            "theorem_status": "COUNTERMODEL_SURVIVES",
            "proof_or_failure": "e_obs=exp(b_R C_R)e0 can be universal and still have DObs_e[partial_C_R]=b_R e_obs",
            "missing_parent_input": "b_R=d_R=w_R=0 theorem or source-backed local response bounds",
            "valid_for_claim": False,
        },
        {
            "functor_id": "FUN2571_4_coupling_readout",
            "target": "visible couplings/source-current scales",
            "required_functor": "kappa_MTS, ell_J and c_vis are q-basic parent coefficients before G_ref, GM, H0 or local tests are read",
            "theorem_status": "COUPLING_DESCENT_UNSIGNED",
            "proof_or_failure": "dc_vis[v]=0 follows from coefficient descent only if the visible coefficient map factors through q_parent",
            "missing_parent_input": "a1/kappa owner, ell_J parent scale/gap/tau-normalization, and no fitted-GM absorption theorem",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def vertical_generator_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "generator_id": "VG2571_0_vq",
            "direction": "v_q in private q/source-vector direction",
            "candidate_role": "hidden reciprocal/source representative",
            "required_kernel": "DObs_e[v_q]=0 plus matter, boundary, tau and source-current readouts q-basic",
            "current_status": "Q_VERTICALITY_UNSIGNED_SOURCE_CHANNELS_ACTIVE",
            "finite_leak_row": "DLEAK2571_0_q_source_readout",
            "valid_for_claim": False,
        },
        {
            "generator_id": "VG2571_1_vRAB",
            "direction": "v_RAB/J_q",
            "candidate_role": "radial-cell/observer-cell response direction",
            "required_kernel": "DObs_e[v_RAB]=0 via q-basic coframe or constraint-first elimination",
            "current_status": "REJECTED_ZERO_CURRENT_OBSERVER_MAP",
            "finite_leak_row": "DLEAK2571_1_RAB_cell",
            "valid_for_claim": False,
        },
        {
            "generator_id": "VG2571_2_vmemory",
            "direction": "v_memory, v_tau_private, partial_C_R",
            "candidate_role": "private memory/time/common-frame direction",
            "required_kernel": "DObs_e[v_memory]=0 and tau_source=tau_charge=tau_clock=tau_readout",
            "current_status": "MEMORY_TAU_FRAME_LOCK_UNSIGNED",
            "finite_leak_row": "DLEAK2571_2_memory_frame_abs",
            "valid_for_claim": False,
        },
        {
            "generator_id": "VG2571_3_vprojector",
            "direction": "delta Pi_M or post-readout projector direction",
            "candidate_role": "source/readout operator variation",
            "required_kernel": "delta_g Pi_M=0, [d,Pi_M]J_H=0 and P_loc DObs_e[v_projector]=0",
            "current_status": "PROJECTOR_READOUT_ORDER_UNSIGNED",
            "finite_leak_row": "DLEAK2571_3_projector_endpoint",
            "valid_for_claim": False,
        },
        {
            "generator_id": "VG2571_4_vboundary",
            "direction": "boundary/corner/reference variation",
            "candidate_role": "compact boundary and endpoint representative direction",
            "required_kernel": "P_loc partial_Q_endpoint E=0 plus zero compact linked-boundary flux",
            "current_status": "BOUNDARY_ENDPOINT_SILENCE_UNSIGNED",
            "finite_leak_row": "DLEAK2571_4_boundary_endpoint",
            "valid_for_claim": False,
        },
        {
            "generator_id": "VG2571_5_vcoupling",
            "direction": "v_coupling acts on a1/kappa_MTS/ell_J/c_vis",
            "candidate_role": "visible coefficient/source-current scale direction",
            "required_kernel": "DObs_e[v_coupling]=0 and dc_vis[v_coupling]=0 before local readout",
            "current_status": "COUPLING_DESCENT_UNSIGNED",
            "finite_leak_row": "DLEAK2571_5_coupling_readout",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def dobs_kernel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "kernel_id": "DOK2571_0_exact_kernel",
            "statement": "If e_obs=E(q_parent(Phi)) and v in ker(Dq_parent), then DObs_e[v]=DE(Dq_parent[v])=0.",
            "status": "PROVED_CONDITIONALLY",
            "blocker": "q_parent, E(q), ordinary readout domain and v_X are not parent-signed simultaneously",
            "effect_if_closed": "private directions stop moving the metric carrier of local GR",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DOK2571_1_connection_lock",
            "statement": "spin/metric connection inherits from the same terminal observed coframe with no independent hidden-frame leak.",
            "status": "MISSING_CONNECTION_DESCENT",
            "blocker": "coframe ownership, connection ownership and hidden-frame coupling clauses remain unsigned",
            "effect_if_closed": "coframe zero would suppress connection-level PPN/light-cone leakage",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DOK2571_2_source_and_coupling_lock",
            "statement": "Hilbert source mass, kappa_MTS, ell_J and visible coefficients are read from q-basic parent slots.",
            "status": "MISSING_SOURCE_COUPLING_DESCENT",
            "blocker": "e_kappaG, e_ellJ_owner, a1_vs_ellJ and E_norm remain live",
            "effect_if_closed": "local source normalization could no longer be hidden in fitted GM or source scale",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DOK2571_3_boundary_endpoint",
            "statement": "boundary/reference/endpoint data have zero local coframe and source projection.",
            "status": "BOUNDARY_ENDPOINT_SILENCE_NOT_PARENT_SIGNED",
            "blocker": "P_loc partial_Q_endpoint E and compact boundary flux are not zeroed",
            "effect_if_closed": "global/cosmology memory can remain global without local clock/PPN hair",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DOK2571_4_current_verdict",
            "statement": "Current MTS proves DObs_e[v_X]=0 and dc_vis[v_X]=0 for all retained local directions.",
            "status": "DOBS_AND_COUPLING_KERNEL_ZERO_NOT_SIGNED",
            "blocker": "q/Dq generators, no-shadow coframe, boundary endpoint, projector order, coupling descent and source normalization remain unsigned",
            "effect_if_closed": "would reopen the strongest local-GR/Newton derivation path",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def no_shadow_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "shadow_id": "NS2571_0_terminal_public_object",
            "clause": "ordinary observables have a terminal public coframe object e_pub=E(Q_vis)",
            "status": "TERMINAL_PUBLIC_COFRAME_NOT_PARENT_DERIVED",
            "countermodel_or_debt": "same universal coframe may still depend on hidden residual variables",
            "zero_if_signed": "ordinary metric carrier no longer has hidden C_R/J_q argument",
            "valid_for_claim": False,
        },
        {
            "shadow_id": "NS2571_1_no_extra_frame_slot",
            "clause": "action/readout domain excludes A_R(C_R), B_R(C_R), w_A(C_R), E(Q_vis,C_R), endpoint and source-prefactor slots",
            "status": "NO_EXTRA_FRAME_SLOT_CLOSURE_ONLY",
            "countermodel_or_debt": "covariance, WEP and Ward identities do not alone forbid common-frame slots",
            "zero_if_signed": "b_R=d_R=w_R=epsilon_endpoint_R=0 by action-domain exclusion",
            "valid_for_claim": False,
        },
        {
            "shadow_id": "NS2571_2_coupling_no_shadow",
            "clause": "visible coupling/source-scale slots are parent coefficients, not post-readout frame/source shadows",
            "status": "COUPLING_NO_SHADOW_UNSIGNED",
            "countermodel_or_debt": "a common coframe can still hide a source-scale or coupling rescaling if kappa_MTS/ell_J are not owned",
            "zero_if_signed": "e_kappaG=e_ellJ_owner=a1_vs_ellJ=0 structurally or become explicit bounded response rows",
            "valid_for_claim": False,
        },
        {
            "shadow_id": "NS2571_3_inheritance_stack",
            "clause": "connection, source, tau, constants and boundary readouts inherit from the same public domain",
            "status": "INHERITANCE_STACK_UNSIGNED",
            "countermodel_or_debt": "metric readout can be zeroed while source/clock/coupling/boundary readout reopens the leak",
            "zero_if_signed": "coframe zero survives into source normalization, constants, PPN and clock readouts",
            "valid_for_claim": False,
        },
        {
            "shadow_id": "NS2571_4_current_verdict",
            "clause": "terminal public coframe/no-shadow zero is derived",
            "status": "NO_SHADOW_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "countermodel_or_debt": "b_R,d_R,w_R,epsilon_endpoint_R and epsilon_coupling_readout remain finite nonclaim rows",
            "zero_if_signed": "DObs/common-frame/coupling leak rows can be promoted to theorem-zero candidates",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def finite_leak_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "leak_id": "DLEAK2571_0_q_source_readout",
            "symbol": "epsilon_q_source_readout",
            "definition": "absolute local coframe/source derivative under private q/source-vector direction",
            "status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless response envelope",
            "source_path": "MISSING_SOURCE_PATH",
            "arena": "local_GR;PPN;R10;clock",
            "valid_for_claim": False,
        },
        {
            "leak_id": "DLEAK2571_1_RAB_cell",
            "symbol": "epsilon_R_cell",
            "definition": "radial-cell/coframe leak under v_RAB/J_q, including local cell-size and clock/source readout response",
            "status": "MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND",
            "units": "dimensionless",
            "source_path": "MISSING_SOURCE_PATH",
            "arena": "local_GR;PPN;WEP;clock;orbital",
            "valid_for_claim": False,
        },
        {
            "leak_id": "DLEAK2571_2_memory_frame_abs",
            "symbol": "epsilon_memory_frame_abs",
            "definition": "absolute no-cancellation envelope for b_R,d_R,w_R,tau-lock and private memory frame readout",
            "status": "MISSING_ABSOLUTE_ENVELOPE_OR_ZERO_THEOREM",
            "units": "dimensionless",
            "source_path": "MISSING_SOURCE_PATH",
            "arena": "all_local_arenas",
            "valid_for_claim": False,
        },
        {
            "leak_id": "DLEAK2571_3_projector_endpoint",
            "symbol": "epsilon_projector_endpoint",
            "definition": "operator/readout-order leak from delta_g Pi_M, commutator [d,Pi_M]J_H and endpoint projection",
            "status": "MISSING_OPERATOR_ZERO_OR_BOUND",
            "units": "dimensionless projection norm",
            "source_path": "MISSING_SOURCE_PATH",
            "arena": "source_normalization;R10;orbital;local_GR",
            "valid_for_claim": False,
        },
        {
            "leak_id": "DLEAK2571_4_boundary_endpoint",
            "symbol": "epsilon_boundary_endpoint",
            "definition": "local projection of boundary/reference/corner coframe and source leak",
            "status": "MISSING_BOUNDARY_ENDPOINT_SILENCE_OR_BOUND",
            "units": "dimensionless projection norm",
            "source_path": "MISSING_SOURCE_PATH",
            "arena": "PPN;clock;orbital;local_GR",
            "valid_for_claim": False,
        },
        {
            "leak_id": "DLEAK2571_5_coupling_readout",
            "symbol": "epsilon_coupling_readout_abs",
            "definition": "|D ln kappa_MTS(v)| + |D ln ell_J(v)| + |D ln c_vis(v)| before local test readout",
            "status": "MISSING_COUPLING_DESCENT_OR_SOURCE_BACKED_BOUND",
            "units": "dimensionless logarithmic coefficient response",
            "source_path": "MISSING_SOURCE_PATH",
            "arena": "Newton;local_GR;PPN;cosmology;R10;orbital",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def projection_interface_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "projection_id": "PROJ2571_0_local_metric",
            "arena": "local_GR/Newton",
            "required_input": "epsilon_memory_frame_abs=0 and epsilon_coupling_readout_abs=0 or source-backed bounds plus EH/source/beta gates",
            "current_status": "BLOCKED_NONCLAIM",
            "wrong_route_guard": "coframe zero alone cannot prove Newton without EH origin, source normalization and coupling ownership",
            "valid_for_claim": False,
        },
        {
            "projection_id": "PROJ2571_1_PPN",
            "arena": "PPN gamma/beta/preferred frame",
            "required_input": "b_R,d_R,endpoint,tau,coupling and massless-tail response kernels",
            "current_status": "MISSING_RESPONSE_KERNEL_AND_COEFFICIENTS",
            "wrong_route_guard": "same-frame WEP cleanliness does not imply PPN or coupling silence",
            "valid_for_claim": False,
        },
        {
            "projection_id": "PROJ2571_2_clock_WEP",
            "arena": "clock/WEP/material",
            "required_input": "b_R,w_R,material sensitivity, constants-marker, coupling descent and tau_clock/tau_WEP rows",
            "current_status": "MISSING_RESPONSE_KERNEL_AND_COEFFICIENTS",
            "wrong_route_guard": "common-mode metric/source shifts can evade differential WEP but still affect clocks/constants/source normalization",
            "valid_for_claim": False,
        },
        {
            "projection_id": "PROJ2571_3_orbital",
            "arena": "orbital/light-time",
            "required_input": "b_R,d_R,endpoint leak, orbital projection, coupling/source-scale envelope and no fitted-GM absorption",
            "current_status": "MISSING_RESPONSE_KERNEL_AND_COEFFICIENTS",
            "wrong_route_guard": "do not absorb coframe/source/coupling leak into fitted orbital GM",
            "valid_for_claim": False,
        },
        {
            "projection_id": "PROJ2571_4_R10",
            "arena": "R10 finite range",
            "required_input": "finite Z_R/M_R^2/lambda_R plus source/test charges, coupling response and accepted bound curve",
            "current_status": "WRONG_ROUTE_GUARD_ACTIVE",
            "wrong_route_guard": "common-frame or coupling-source leg is not a finite-range alpha(lambda) substitute",
            "valid_for_claim": False,
        },
        {
            "projection_id": "PROJ2571_5_coupling_source",
            "arena": "source_normalization/coupling",
            "required_input": "e_kappaG=e_ellJ_owner=a1_vs_ellJ=0 by parent coefficient ownership or source-backed finite response rows",
            "current_status": "BLOCKED_NONCLAIM",
            "wrong_route_guard": "do not infer parent coupling from measured G_ref, fitted orbital GM, H0 calibration or local-test normalization",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2571_0_chain_rule",
            "claim": "Observed coframe/readout chain-rule theorem is available conditionally.",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "DObs[v]=DObs_bar(Dq[v]) gives zero only after e_obs, clocks, source and coefficients are q-basic.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2571_1_DObs_zero",
            "claim": "DObs_e[v_X]=0 is derived for all retained private/residual directions.",
            "gate_status": "BLOCKED",
            "reason": "q/Dq generators, coframe ownership, no-shadow, boundary endpoint and projector clauses remain unsigned.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2571_2_terminal_public_coframe",
            "claim": "Terminal public coframe/no-shadow frame is parent-derived.",
            "gate_status": "BLOCKED",
            "reason": "current corpus does not derive no C_R/J_q frame, source-prefactor, endpoint or coupling shadow slots.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2571_3_common_frame_bounds",
            "claim": "Finite DObs/common-frame leak rows are source-backed and below local thresholds.",
            "gate_status": "BLOCKED",
            "reason": "numeric values, source paths, response kernels and arena thresholds are missing.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2571_4_coupling_readout_bounds",
            "claim": "kappa_MTS, ell_J and visible coefficients are q-basic or locally bounded.",
            "gate_status": "BLOCKED",
            "reason": "e_kappaG, e_ellJ_owner, a1_vs_ellJ and epsilon_coupling_readout_abs remain unsigned/nonclaim.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2571_5_local_GR_Newton",
            "claim": "Newton/local-GR reduction is derived.",
            "gate_status": "BLOCKED",
            "reason": "DObs/no-shadow is necessary but not sufficient; EH origin, kappa, ell_J, source normalization and PPN gates remain open.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2571_6_no_shortcuts",
            "claim": "No Dq-only, same-frame, q_shape, WEP, Ward, fitted-GM or EH-import shortcut is used as proof.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "R_AB/q_shape, common-frame, coupling and source-normalization shortcuts are explicitly refused as claims.",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2571_0_result",
            "decision": "Keep the observed-coframe/readout theorem as exact conditional, not a current local-GR claim.",
            "reason": "The chain-rule proof is real, but q_parent, E(q), vertical generators and no-shadow action-domain clauses are unsigned.",
            "effect": "the route stays alive as a precise proof checklist instead of a plateau axiom.",
        },
        {
            "decision_id": "DEC2571_1_RAB",
            "decision": "Keep R_AB/J_q as a finite readout leak unless DObs_e[v_R]=0 is parent-proved.",
            "reason": "q_shape forgetting J_q does not prove clocks, rulers, source mass or local cells forget it.",
            "effect": "epsilon_R_cell remains a nonclaim residual row.",
        },
        {
            "decision_id": "DEC2571_2_coupling",
            "decision": "Move coupling ownership into the same readout-functor gate as coframe ownership.",
            "reason": "a common metric can still hide a source-scale/coupling rescaling if kappa_MTS and ell_J are not parent-owned.",
            "effect": "epsilon_coupling_readout_abs becomes a required local residual/bound row.",
        },
        {
            "decision_id": "DEC2571_3_next",
            "decision": "Attack the terminal public coframe/no-shadow action-domain clause next, now including coupling shadows.",
            "reason": "Either the parent action forbids hidden Weyl/disformal/source/coupling slots, or a response kernel must be sourced and bounded.",
            "effect": "2572 should try no-shadow closure first, then stage source-ready response-kernel rows for b_R/d_R/w_R/e_kappaG/e_ellJ_owner.",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2571_0_selected",
            "selection_status": "selected",
            "target_file": "2572-Y5-R2FR-terminal-public-coframe-no-shadow-action-domain-or-first-response-kernel.md",
            "target_script": "scripts/Y5_R2FR_terminal_public_coframe_no_shadow_action_domain_or_first_response_kernel_2572.py",
            "task": "derive the parent action-domain clause excluding C_R/J_q Weyl, disformal, source-prefactor, endpoint and coupling slots from ordinary readout; if it fails, stage source-ready response kernels for b_R/d_R/w_R/e_kappaG/e_ellJ_owner into PPN, clocks/WEP, orbital or local-GR tests",
            "acceptance_target": "no-shadow theorem attempt, coupling-shadow clauses, first response-kernel acquisition ledger, all local-GR/Newton claims blocked unless parent-signed",
            "guardrails": "no same-frame shortcut; no q_shape shortcut; no WEP/Ward shortcut; no fitted GM/H0; no EH import; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "functor_attempt": OUTPUTS["functor_attempt"],
        "vertical_generators": OUTPUTS["vertical_generators"],
        "finite_leaks": OUTPUTS["finite_leaks"],
        "projection_interface": OUTPUTS["projection_interface"],
        "acquisition_queue": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2571_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(stamp({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail}))

    add("VAL2571_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add(
        "VAL2571_01_chain_rule_conditional",
        any(row["functor_id"] == "FUN2571_0_chain_rule" and row["theorem_status"] == "EXACT_CONDITIONAL" for row in data["functors"]),
        "observed coframe/readout chain-rule theorem is recorded as exact conditional",
    )
    add(
        "VAL2571_02_RAB_current_failure",
        any(row["functor_id"] == "FUN2571_2_RAB_qshape" and row["theorem_status"] == "FAIL_CURRENT_CORPUS" for row in data["functors"]),
        "q_shape/R_AB route fails current DObs_e proof",
    )
    add(
        "VAL2571_03_same_frame_warning",
        any(row["functor_id"] == "FUN2571_3_same_frame_warning" and row["theorem_status"] == "COUNTERMODEL_SURVIVES" for row in data["functors"]),
        "same-frame-not-enough countermodel retained",
    )
    add(
        "VAL2571_04_no_shadow_blocked",
        any(row["shadow_id"] == "NS2571_4_current_verdict" and row["status"] == "NO_SHADOW_ZERO_NOT_DERIVED_CURRENT_CORPUS" for row in data["shadow"]),
        "terminal public coframe/no-shadow theorem remains blocked",
    )
    add(
        "VAL2571_05_coupling_leak_present",
        any(row["leak_id"] == "DLEAK2571_5_coupling_readout" and row["valid_for_claim"] is False for row in data["leaks"]),
        "coupling readout leak row is present and nonclaim",
    )
    add(
        "VAL2571_06_finite_leaks_nonclaim",
        len(data["leaks"]) >= 6 and all(row["valid_for_claim"] is False for row in data["leaks"]),
        "finite DObs/common-frame/coupling leak rows remain nonclaim",
    )
    add(
        "VAL2571_07_projection_guards",
        all(row["valid_for_claim"] is False for row in data["projections"]) and any(row["projection_id"] == "PROJ2571_5_coupling_source" for row in data["projections"]),
        "projection interfaces remain blocked/nonclaim and include coupling/source guard",
    )
    add("VAL2571_08_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no gate allows Newton/local-GR/R10 claim")
    add(
        "VAL2571_09_next_target_written",
        any(row["route_id"] == "NEXT2571_0_selected" for row in data["next"]),
        "2572 no-shadow/action-domain or response-kernel target selected",
    )
    add("VAL2571_10_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2571*", "*P8_Y5_OBS_COFRAME_2571*", "*JR2571*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2571_11_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2571 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2571_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2571_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2571_OVERALL",
        overall,
        "2571 keeps the DObs theorem conditional, rejects cheap R_AB/common-frame/coupling silence, stages finite leak rows, and selects 2572",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            values.append(value.replace("|", "\\|").replace("\n", " "))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2571 Y5 R2FR Observed Coframe Functor And Vertical Generator Certificate Or DObs Leak Row",
        "",
        "**Status:** the observed-coframe/readout chain-rule theorem is exact but still conditional. The current corpus does not yet parent-sign the terminal public coframe/no-shadow action-domain clause, the field-by-field vertical generators, or the coupling/source-scale descent needed to claim `DObs_e[v_X]=0` and `dc_vis[v_X]=0`.",
        "",
        "**Main result:** this checkpoint tightens the local-GR hinge. `Dq[v]=0` only becomes physics when every ordinary readout factors as `Obs=Obs_bar(q_parent(Phi))`. The clean route is a terminal public coframe `e_pub=E(Q_vis)` plus q-basic couplings/source scales. That route is alive but not closed: `R_AB`, common-frame response, projector/boundary terms, `kappa_MTS`, `ell_J`, and visible constants remain finite nonclaim leak rows rather than theorem zeros.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Observed Coframe Functor Attempt",
        markdown_table(data["functors"], ["functor_id", "target", "required_functor", "theorem_status", "proof_or_failure", "missing_parent_input", "valid_for_claim"]),
        "",
        "## Vertical Generator Table",
        markdown_table(data["generators"], ["generator_id", "direction", "candidate_role", "required_kernel", "current_status", "finite_leak_row", "valid_for_claim"]),
        "",
        "## DObs Kernel Gate",
        markdown_table(data["kernel"], ["kernel_id", "statement", "status", "blocker", "effect_if_closed", "valid_for_claim"]),
        "",
        "## No-Shadow Frame Gate",
        markdown_table(data["shadow"], ["shadow_id", "clause", "status", "countermodel_or_debt", "zero_if_signed", "valid_for_claim"]),
        "",
        "## Finite DObs Leak Rows",
        markdown_table(data["leaks"], ["leak_id", "symbol", "definition", "status", "units", "source_path", "arena", "valid_for_claim"]),
        "",
        "## Projection Interface",
        markdown_table(data["projections"], ["projection_id", "arena", "required_input", "current_status", "wrong_route_guard", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_register_rows(),
        "functors": functor_attempt_rows(),
        "generators": vertical_generator_rows(),
        "kernel": dobs_kernel_rows(),
        "shadow": no_shadow_rows(),
        "leaks": finite_leak_rows(),
        "projections": projection_interface_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["functor_attempt"], data["functors"])
    write_csv(OUTPUTS["vertical_generators"], data["generators"])
    write_csv(OUTPUTS["dobs_kernel"], data["kernel"])
    write_csv(OUTPUTS["no_shadow"], data["shadow"])
    write_csv(OUTPUTS["finite_leaks"], data["leaks"])
    write_csv(OUTPUTS["projection_interface"], data["projections"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2571_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
