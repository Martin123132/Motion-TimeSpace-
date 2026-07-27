from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_OBSERVED_COFRAME_FUNCTOR_2487"
CHECKPOINT_ID = "2487"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2487-Y5-R2FR-observed-coframe-functor-and-vertical-generator-certificate-or-DObs-leak-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_OBS_COFRAME_2487_SOURCE_REGISTER.csv",
    "functor_attempt": OUT / "P8_Y5_OBS_COFRAME_2487_FUNCTOR_ATTEMPT.csv",
    "vertical_generators": OUT / "P8_Y5_OBS_COFRAME_2487_VERTICAL_GENERATOR_TABLE.csv",
    "dobs_kernel": OUT / "P8_Y5_OBS_COFRAME_2487_DOBS_KERNEL_GATE.csv",
    "no_shadow": OUT / "P8_Y5_OBS_COFRAME_2487_NO_SHADOW_FRAME_GATE.csv",
    "finite_leaks": OUT / "P8_Y5_OBS_COFRAME_2487_FINITE_DOBS_LEAK_ROWS.csv",
    "projection_interface": OUT / "P8_Y5_OBS_COFRAME_2487_PROJECTION_INTERFACE.csv",
    "claim_gates": OUT / "P8_Y5_OBS_COFRAME_2487_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_OBS_COFRAME_2487_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_OBS_COFRAME_2487_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_OBS_COFRAME_2487_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2487_VALIDATION.csv",
}

COPY_TARGETS = {
    "functor_attempt": LOCAL_BOUNDS / "Observed_coframe_functor_attempt_2487_NONCLAIM.csv",
    "vertical_generators": LOCAL_BOUNDS / "Observed_coframe_vertical_generator_table_2487_NONCLAIM.csv",
    "finite_leaks": LOCAL_BOUNDS / "Finite_DObs_leak_rows_2487_NONCLAIM.csv",
    "projection_interface": LOCAL_BOUNDS / "Common_frame_projection_interface_2487_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2487_TERMINAL_PUBLIC_COFRAME_OR_COMMON_FRAME_KERNEL.csv",
}

SOURCES = [
    {
        "source_id": "SRC2487_00_2486_doc",
        "source_path": ROOT / "2486-Y5-R2FR-parent-field-sort-and-quotient-map-signature-or-residual-owner-split.md",
        "needles": ["NEXT2486_0_selected", "DQ2486_3_RAB", "VAL2486_OVERALL"],
        "role": "handoff selecting observed coframe/readout functor",
    },
    {
        "source_id": "SRC2487_01_1737_qmap",
        "source_path": ROOT / "1737-Y5-R2FR-q-map-Dq-vertical-basis-source-row-or-coframe-functor-zero.md",
        "needles": ["CFZ1737_0_exact_conditional", "DQM1737_0_DObs_e", "VAL1737_OVERALL"],
        "role": "q-map/Dq vertical basis and DObs_e finite row precedent",
    },
    {
        "source_id": "SRC2487_02_1738_kernel",
        "source_path": ROOT / "1738-Y5-R2FR-observed-coframe-kernel-zero-or-first-finite-DObs-e-row.md",
        "needles": ["DOBS_E_KERNEL_ZERO_NOT_SIGNED", "SAME_COFRAME_IS_NOT_ENOUGH", "VAL1738_OVERALL"],
        "role": "observed coframe kernel no-claim and same-frame countermodel",
    },
    {
        "source_id": "SRC2487_03_1878_qshape",
        "source_path": ROOT / "1878-Y5-R2FR-qshape-readout-functor-kernel-or-parent-category-principle.md",
        "needles": ["CKT1878_0_chain_rule", "CKT1878_5_verdict", "VAL1878_OVERALL"],
        "role": "q_shape coframe kernel failure and finite DObs_e rows",
    },
    {
        "source_id": "SRC2487_04_1879_coframe_owner",
        "source_path": ROOT / "1879-Y5-R2FR-parent-coframe-ownership-or-common-frame-leak-bound.md",
        "needles": ["PCO1879_1_coframe_owner", "CFL1879_0_bR", "VAL1879_OVERALL"],
        "role": "parent coframe ownership and common-frame leak rows",
    },
    {
        "source_id": "SRC2487_05_1880_terminal",
        "source_path": ROOT / "1880-Y5-R2FR-terminal-public-coframe-no-shadow-frame-or-bg-bound-projection.md",
        "needles": ["TPC1880_0_terminal_object", "ZTH1880_0_exact_conditional", "VAL1880_OVERALL"],
        "role": "terminal public coframe/no-shadow theorem and projection contracts",
    },
    {
        "source_id": "SRC2487_06_565_vertical_observation",
        "source_path": ROOT / "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md",
        "needles": ["VT565_0_vertical_observation_theorem", "E565_0_conditional_theorem"],
        "role": "early vertical-observation theorem shape",
    },
    {
        "source_id": "SRC2487_07_566_no_marker",
        "source_path": ROOT / "566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md",
        "needles": ["NM566_3_verdict", "RU566_0_allowed"],
        "role": "primitive quotient/no-marker clause is sufficient but not derived",
    },
    {
        "source_id": "SRC2487_08_2486_validation",
        "source_path": OUT / "P8_Y5_BRR545_2486_VALIDATION.csv",
        "needles": ["VAL2486_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:  # pragma: no cover
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
            "functor_id": "FUN2487_0_chain_rule",
            "target": "observed coframe/metric",
            "required_functor": "e_obs = E(q_parent(Phi))",
            "theorem_status": "EXACT_CONDITIONAL",
            "proof_or_failure": "if v in ker(Dq_parent), then DObs_e[v]=DE(Dq_parent[v])=0",
            "missing_parent_input": "q_parent, E, vertical generators and q-basic readout domain are not parent-signed",
            "valid_for_claim": False,
        },
        {
            "functor_id": "FUN2487_1_terminal_public_coframe",
            "target": "terminal public coframe",
            "required_functor": "ordinary matter, clocks, rods, photons, source current and orbit readout all factor through one e_pub",
            "theorem_status": "CANDIDATE_NOT_DERIVED",
            "proof_or_failure": "1880 gives exact no-shadow theorem if terminal public coframe/no-extra-frame domain is signed",
            "missing_parent_input": "terminal-object derivation and no C_R/J_q frame/source-prefactor slots",
            "valid_for_claim": False,
        },
        {
            "functor_id": "FUN2487_2_RAB_qshape",
            "target": "R_AB/J_q direction",
            "required_functor": "q_shape forgets J_q/R_AB and e_obs is q_shape-basic",
            "theorem_status": "FAIL_CURRENT_CORPUS",
            "proof_or_failure": "Dq_shape[v_R]=0 is easy by construction, but DObs_e[v_R]=0 is not proved; current observed coframe sees radial-cell variation",
            "missing_parent_input": "q_shape readout functor or constraint-first elimination before readout",
            "valid_for_claim": False,
        },
        {
            "functor_id": "FUN2487_3_same_frame_warning",
            "target": "same observed coframe",
            "required_functor": "same frame must be independent of hidden/residual variables, not merely universal",
            "theorem_status": "COUNTERMODEL_SURVIVES",
            "proof_or_failure": "e_obs=exp(b_R C_R)e0 is one universal coframe but DObs_e[partial_C_R]=b_R e_obs",
            "missing_parent_input": "b_R=0/no-shadow theorem or numeric/source-backed bound",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def vertical_generator_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "generator_id": "VG2487_0_vZ",
            "direction": "v_Z=partial_Z",
            "candidate_role": "formal response-doublet residual direction",
            "required_kernel": "DObs_e[v_Z]=0 plus source/readout/boundary/tau q-basicity",
            "current_status": "MISSING_UNIFIED_Z_BASIS_AND_COMPONENT_LOCK",
            "finite_leak_row": "DLEAK2487_0_vZ",
            "valid_for_claim": False,
        },
        {
            "generator_id": "VG2487_1_vphi",
            "direction": "v_phi=partial_phi",
            "candidate_role": "trace-free improvement auxiliary direction",
            "required_kernel": "DObs_e[v_phi]=0 and connection/coframe ownership",
            "current_status": "PHI_IMPROVEMENT_OWNER_UNSIGNED",
            "finite_leak_row": "DLEAK2487_1_vphi",
            "valid_for_claim": False,
        },
        {
            "generator_id": "VG2487_2_vRAB",
            "direction": "v_RAB/Jq",
            "candidate_role": "cell/radial response or observer phase-cell direction",
            "required_kernel": "DObs_e[v_RAB]=0 via q-basic coframe or constraint-first removal",
            "current_status": "REJECTED_ZERO_CURRENT_EVIDENCE",
            "finite_leak_row": "DLEAK2487_2_RAB_cell",
            "valid_for_claim": False,
        },
        {
            "generator_id": "VG2487_3_vboundary",
            "direction": "v_boundary/projector",
            "candidate_role": "compact boundary/projector representative variation",
            "required_kernel": "P_loc DObs_e[v_boundary]=0 and boundary charge silence",
            "current_status": "BOUNDARY_PROJECTOR_NOT_BASIC",
            "finite_leak_row": "DLEAK2487_3_boundary_endpoint",
            "valid_for_claim": False,
        },
        {
            "generator_id": "VG2487_4_common_frame",
            "direction": "partial_C_R or hidden common-frame direction",
            "candidate_role": "common Weyl/disformal/source-frame leak",
            "required_kernel": "b_R=d_R=w_R=epsilon_endpoint_R=0 by no-shadow terminal public coframe",
            "current_status": "NO_SHADOW_ZERO_NOT_DERIVED",
            "finite_leak_row": "DLEAK2487_4_common_frame_abs",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def dobs_kernel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "kernel_id": "DOK2487_0_exact_kernel",
            "statement": "If e_obs=E(q_parent(Phi)) and v in ker(Dq_parent), then DObs_e[v]=0.",
            "status": "PROVED_CONDITIONALLY",
            "blocker": "q_parent, E(q), and v_X are not parent-signed simultaneously",
            "effect_if_closed": "private/residual directions stop moving the metric carrier of local GR",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DOK2487_1_connection_lock",
            "statement": "spin/metric connection follows the same observed coframe with no independent hidden-frame leak.",
            "status": "MISSING_CONNECTION_DESCENT",
            "blocker": "connection/coframe ownership and hidden-frame coupling clauses unsigned",
            "effect_if_closed": "metric/coframe zero also suppresses connection-level PPN/light-cone leakage",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DOK2487_2_boundary_endpoint",
            "statement": "boundary and endpoint data have zero local coframe projection.",
            "status": "BOUNDARY_ENDPOINT_SILENCE_NOT_PARENT_SIGNED",
            "blocker": "P_loc partial_Q_endpoint E and compact boundary flux are not zeroed",
            "effect_if_closed": "cosmology/boundary memory can stay global without local clock/PPN hair",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DOK2487_3_current_verdict",
            "statement": "Current MTS proves DObs_e[v_X]=0 for all coframe-relevant retained directions.",
            "status": "DOBS_E_KERNEL_ZERO_NOT_SIGNED",
            "blocker": "coframe ownership, common-frame countermodels, boundary endpoint, and q/Dq generators remain unsigned",
            "effect_if_closed": "would reopen the strongest local-GR reduction path",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def no_shadow_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "shadow_id": "NS2487_0_terminal_public_object",
            "clause": "ordinary observables have a terminal public coframe object e_pub=E(Q_vis)",
            "status": "TERMINAL_PUBLIC_COFRAME_NOT_PARENT_DERIVED",
            "countermodel_or_debt": "same universal coframe may still depend on hidden residual variable",
            "zero_if_signed": "common metric carrier no longer has hidden C_R/J_q argument",
            "valid_for_claim": False,
        },
        {
            "shadow_id": "NS2487_1_no_extra_frame_slot",
            "clause": "action/readout domain excludes A_R(C_R), B_R(C_R), w_A(C_R), E(Q_vis,C_R)",
            "status": "NO_EXTRA_FRAME_SLOT_CLOSURE_ONLY",
            "countermodel_or_debt": "covariance/WEP/Ward do not independently forbid common-frame slots",
            "zero_if_signed": "b_R=d_R=w_R=0 by action-domain exclusion",
            "valid_for_claim": False,
        },
        {
            "shadow_id": "NS2487_2_inheritance_stack",
            "clause": "connection, source, tau and boundary readouts inherit from the same public coframe domain",
            "status": "INHERITANCE_STACK_UNSIGNED",
            "countermodel_or_debt": "metric readout can be zeroed while source/clock/boundary readout reopens the leak",
            "zero_if_signed": "coframe zero survives into source normalization and PPN readouts",
            "valid_for_claim": False,
        },
        {
            "shadow_id": "NS2487_3_current_verdict",
            "clause": "terminal public coframe/no-shadow zero is derived",
            "status": "NO_SHADOW_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "countermodel_or_debt": "b_R,d_R,w_R,epsilon_endpoint_R remain finite nonclaim rows",
            "zero_if_signed": "DObs/common-frame leak rows can be promoted to theorem-zero candidates",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def finite_leak_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "leak_id": "DLEAK2487_0_vZ",
            "symbol": "epsilon_DObs_Z",
            "definition": "dimensionless observed-coframe derivative under v_Z",
            "status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless coframe-log derivative",
            "source_path": "MISSING_SOURCE_PATH",
            "arena": "local_GR;PPN;clock",
            "valid_for_claim": False,
        },
        {
            "leak_id": "DLEAK2487_1_vphi",
            "symbol": "epsilon_DObs_phi",
            "definition": "dimensionless observed-coframe derivative under v_phi",
            "status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless coframe-log derivative",
            "source_path": "MISSING_SOURCE_PATH",
            "arena": "local_GR;PPN;clock",
            "valid_for_claim": False,
        },
        {
            "leak_id": "DLEAK2487_2_RAB_cell",
            "symbol": "epsilon_R_cell",
            "definition": "radial-cell/coframe leak under v_RAB/J_q, e.g. norm of delta ln T and delta ln sqrt(S)",
            "status": "MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND",
            "units": "dimensionless",
            "source_path": "MISSING_SOURCE_PATH",
            "arena": "local_GR;PPN;WEP;clock;orbital",
            "valid_for_claim": False,
        },
        {
            "leak_id": "DLEAK2487_3_boundary_endpoint",
            "symbol": "epsilon_endpoint_R",
            "definition": "local projection of boundary/endpoint coframe leak",
            "status": "MISSING_BOUNDARY_ENDPOINT_SILENCE_OR_BOUND",
            "units": "dimensionless projection norm",
            "source_path": "MISSING_SOURCE_PATH",
            "arena": "PPN;clock;orbital;local_GR",
            "valid_for_claim": False,
        },
        {
            "leak_id": "DLEAK2487_4_common_frame_abs",
            "symbol": "epsilon_common_frame_abs",
            "definition": "absolute no-cancellation envelope |b_R|+|d_R|+|w_R|+|epsilon_endpoint_R| plus any sourced coframe/tau/readout leaks",
            "status": "MISSING_ABSOLUTE_ENVELOPE",
            "units": "dimensionless",
            "source_path": "MISSING_SOURCE_PATH",
            "arena": "all_local_arenas",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def projection_interface_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "projection_id": "PROJ2487_0_local_metric",
            "arena": "local_GR/Newton",
            "required_input": "epsilon_common_frame_abs=0 or source-backed bound plus EH/source/beta gates",
            "current_status": "BLOCKED_NONCLAIM",
            "wrong_route_guard": "coframe zero alone cannot prove Newton without source normalization and field-equation closure",
            "valid_for_claim": False,
        },
        {
            "projection_id": "PROJ2487_1_PPN",
            "arena": "PPN gamma/beta/preferred frame",
            "required_input": "b_R,d_R,endpoint,tau and massless-tail response kernels",
            "current_status": "MISSING_RESPONSE_KERNEL_AND_COEFFICIENTS",
            "wrong_route_guard": "same-frame WEP cleanliness does not imply PPN silence",
            "valid_for_claim": False,
        },
        {
            "projection_id": "PROJ2487_2_clock_WEP",
            "arena": "clock/WEP/material",
            "required_input": "b_R,w_R,material sensitivity, constants-marker and tau_clock/tau_WEP rows",
            "current_status": "MISSING_RESPONSE_KERNEL_AND_COEFFICIENTS",
            "wrong_route_guard": "common-mode metric/source shifts can evade differential WEP but affect clocks/source normalization",
            "valid_for_claim": False,
        },
        {
            "projection_id": "PROJ2487_3_orbital",
            "arena": "orbital/light-time",
            "required_input": "b_R,d_R,endpoint leak, orbital projection and no-cancellation envelope",
            "current_status": "MISSING_RESPONSE_KERNEL_AND_COEFFICIENTS",
            "wrong_route_guard": "do not absorb coframe/source leak into fitted orbital GM",
            "valid_for_claim": False,
        },
        {
            "projection_id": "PROJ2487_4_R10",
            "arena": "R10 finite range",
            "required_input": "finite Z_R/M_R^2/lambda_R plus source/test charges and accepted bound curve",
            "current_status": "WRONG_ROUTE_GUARD_ACTIVE",
            "wrong_route_guard": "common-frame source leg is not a finite-range alpha(lambda) substitute",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2487_0_chain_rule",
            "claim": "Observed coframe kernel theorem is available conditionally.",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "DObs_e[v]=DE(Dq[v]) gives zero once e_obs=E(q) and v in ker(Dq) are parent-signed.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2487_1_DObs_zero",
            "claim": "DObs_e[v_X]=0 is derived for all retained private/residual directions.",
            "gate_status": "BLOCKED",
            "reason": "q/Dq generators, coframe ownership, no-shadow and boundary endpoint clauses remain unsigned.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2487_2_terminal_public_coframe",
            "claim": "Terminal public coframe/no-shadow frame is parent-derived.",
            "gate_status": "BLOCKED",
            "reason": "current corpus does not derive no C_R/J_q frame/source-prefactor slots.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2487_3_common_frame_bounds",
            "claim": "Finite DObs/common-frame leak rows are source-backed and below local thresholds.",
            "gate_status": "BLOCKED",
            "reason": "numeric values, source paths, units, response kernels and arena bounds are missing.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2487_4_local_GR_Newton",
            "claim": "Newton/local-GR reduction is derived.",
            "gate_status": "BLOCKED",
            "reason": "DObs/no-shadow is necessary but not sufficient; EH origin, kappa, source normalization and PPN gates remain open.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2487_5_no_shortcuts",
            "claim": "No same-frame, WEP, Ward, q_shape or fitted-GM shortcut is used as a proof.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "same-coframe and q_shape shortcuts are explicitly retained as blockers/fallback rows.",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2487_0_result",
            "decision": "Retain the observed-coframe functor theorem as exact conditional, not a current claim.",
            "reason": "The chain-rule proof is real, but q/Dq/E(q) and no-shadow parent clauses are unsigned.",
            "effect": "local-GR route stays alive but now hinges on terminal public coframe ownership.",
        },
        {
            "decision_id": "DEC2487_1_RAB",
            "decision": "Keep R_AB/J_q coframe leak as explicit finite residual unless DObs_e[v_R]=0 is proved.",
            "reason": "q_shape forgetting J_q does not prove clocks/rulers/source readout forget it.",
            "effect": "epsilon_R_cell and epsilon_common_frame_abs remain nonclaim rows.",
        },
        {
            "decision_id": "DEC2487_2_next",
            "decision": "Next target is terminal public coframe/no-shadow action-domain clause or first response kernel.",
            "reason": "Either we prove b_R=d_R=w_R=0 structurally, or we need one real projection kernel to start bounding the leak.",
            "effect": "2488 should try no-shadow parent action clause first, then source first common-frame response-kernel row if it fails.",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2487_0_selected",
            "selection_status": "selected",
            "target_file": "2488-Y5-R2FR-terminal-public-coframe-no-shadow-action-domain-or-first-response-kernel.md",
            "target_script": "scripts/Y5_R2FR_terminal_public_coframe_no_shadow_action_domain_or_first_response_kernel_2488.py",
            "task": "try to derive the parent action-domain clause that excludes C_R/J_q Weyl, disformal, source-prefactor and endpoint slots from ordinary readout; if it fails, stage the first source-ready response kernel for b_R/d_R/w_R into PPN, clock/WEP or orbital tests",
            "acceptance_target": "no-shadow theorem attempt, b_R/d_R/w_R residual rows, first response-kernel acquisition ledger, all local-GR claims blocked",
            "guardrails": "no same-frame shortcut; no q_shape shortcut; no WEP/Ward shortcut; no fitted GM; no EH import; no GitHub",
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
                    "copy_id": f"COPY2487_{key}",
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
        rows.append(
            stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": notes,
                    "detail": detail,
                }
            )
        )

    add("VAL2487_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2487_01_chain_rule_conditional",
        any(row["functor_id"] == "FUN2487_0_chain_rule" and row["theorem_status"] == "EXACT_CONDITIONAL" for row in data["functors"]),
        "observed coframe chain-rule theorem is recorded as exact conditional",
    )
    add(
        "VAL2487_02_RAB_current_failure",
        any(row["functor_id"] == "FUN2487_2_RAB_qshape" and row["theorem_status"] == "FAIL_CURRENT_CORPUS" for row in data["functors"]),
        "q_shape/R_AB route fails current DObs_e proof",
    )
    add(
        "VAL2487_03_same_frame_warning",
        any(row["functor_id"] == "FUN2487_3_same_frame_warning" and row["theorem_status"] == "COUNTERMODEL_SURVIVES" for row in data["functors"]),
        "same-frame-not-enough countermodel retained",
    )
    add(
        "VAL2487_04_no_shadow_blocked",
        any(row["shadow_id"] == "NS2487_3_current_verdict" and row["status"] == "NO_SHADOW_ZERO_NOT_DERIVED_CURRENT_CORPUS" for row in data["shadow"]),
        "terminal public coframe/no-shadow theorem remains blocked",
    )
    add(
        "VAL2487_05_finite_leaks_nonclaim",
        len(data["leaks"]) >= 5 and all(row["valid_for_claim"] is False for row in data["leaks"]),
        "finite DObs/common-frame leak rows remain nonclaim",
    )
    add(
        "VAL2487_06_projection_guards",
        all(row["valid_for_claim"] is False for row in data["projections"]),
        "projection interfaces remain blocked/nonclaim",
    )
    add("VAL2487_07_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no gate allows Newton/local-GR/R10 claim")
    add(
        "VAL2487_08_next_target_written",
        any(row["route_id"] == "NEXT2487_0_selected" for row in data["next"]),
        "2488 no-shadow or response-kernel target selected",
    )
    add("VAL2487_09_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2487*", "*P8_Y5_OBS_COFRAME_2487*", "*JR2487*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2487_10_no_formalization_artifacts", not formalization_artifacts, "no 2487 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2487_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2487_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2487_OVERALL",
        overall,
        "2487 consolidates the observed coframe functor theorem, blocks no-shadow promotion, retains finite DObs leaks, and selects 2488",
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
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2487 Y5 R2FR Observed Coframe Functor And Vertical Generator Certificate Or DObs Leak Row",
        "",
        "**Status:** the observed-coframe chain-rule theorem is exact but still conditional. Current MTS does not yet derive the terminal public coframe/no-shadow action-domain clause needed to promote `DObs_e[v_X]=0`.",
        "",
        "**Main result:** the right local-GR hinge is now specific: ordinary observables need a terminal public coframe `e_pub=E(Q_vis)` with no `C_R/J_q` Weyl, disformal, source-prefactor, endpoint, or post-readout frame slot. A single universal coframe is not enough, because `e_obs=exp(b_R C_R)e0` is universal but still locally physical. Therefore `b_R`, `d_R`, `w_R`, endpoint leakage, and the absolute common-frame envelope remain nonclaim residual rows.",
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
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
