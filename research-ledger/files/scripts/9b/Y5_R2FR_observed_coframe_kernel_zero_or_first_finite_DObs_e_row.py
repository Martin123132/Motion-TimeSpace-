from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1738"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1738 - Observed Coframe Kernel Zero Or First Finite DObs e Row"
UTC = datetime.now(timezone.utc).isoformat()


def yesno(value: bool) -> str:
    return "True" if value else "False"


def no() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1738_0_1737_doc",
        "source_key": "1737_handoff_doc",
        "source_path": ROOT / "1737-Y5-R2FR-q-map-Dq-vertical-basis-source-row-or-coframe-functor-zero.md",
        "needles": ["NEXT1737_0_primary", "VAL1737_OVERALL"],
    },
    {
        "source_id": "SRC1738_1_1737_coframe_zero",
        "source_key": "1737_coframe_zero_attempt",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_COFRAME_FUNCTOR_ZERO_ATTEMPT.csv",
        "needles": ["CFZ1737_0_exact_conditional", "COFRAME_FUNCTOR_ZERO_NOT_SIGNED"],
    },
    {
        "source_id": "SRC1738_2_1737_finite_Dq",
        "source_key": "1737_finite_Dq_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_FINITE_DQ_SOURCE_ROWS.csv",
        "needles": ["FDQ1737_vZ_e", "RETAINED_NONCLAIM_DQ_LEAK_INPUT"],
    },
    {
        "source_id": "SRC1738_3_1675_coframe_descent",
        "source_key": "1675_coframe_descent_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1675_COFRAME_DESCENT_GATE.csv",
        "needles": ["CDG1675_3_verdict", "COFRAME_DESCENT_NOT_PARENT_SIGNED"],
    },
    {
        "source_id": "SRC1738_4_1504_independence",
        "source_key": "1504_observed_coframe_independence",
        "source_path": RESIDUALS / "P8_Y5_R10_1504_OBSERVED_COFRAME_INDEPENDENCE_AUDIT.csv",
        "needles": ["OC1504_7_verdict", "NOT_PARENT_DERIVED"],
    },
    {
        "source_id": "SRC1738_5_623_functor",
        "source_key": "623_coframe_functor_theorem",
        "source_path": RESIDUALS / "P8_Y5_R10_623_COFRAME_FUNCTOR_THEOREM_ATTEMPT.csv",
        "needles": ["OCF623_4_bg_verdict", "not_closed"],
    },
    {
        "source_id": "SRC1738_6_863_zero",
        "source_key": "863_coframe_zero_theorem",
        "source_path": RESIDUALS / "P8_Y5_R10_863_COFRAME_ZERO_THEOREM.csv",
        "needles": ["CZT863_5_zero_verdict", "not_proven"],
    },
    {
        "source_id": "SRC1738_7_785_metric_contract",
        "source_key": "785_psi_metric_coframe_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_785_PSI_METRIC_COFRAME_CONTRACT.csv",
        "needles": ["PMC785_7_GR_Newton_reduction", "not_closed"],
    },
    {
        "source_id": "SRC1738_8_862_pullback",
        "source_key": "862_coframe_pullback_closure",
        "source_path": RESIDUALS / "P8_Y5_R10_862_COFRAME_PULLBACK_CLOSURE_AUDIT.csv",
        "needles": ["CC862_1_strict_identity_coframe", "cleanest_route_but_not_parent_derived"],
    },
    {
        "source_id": "SRC1738_9_same_coframe_variation",
        "source_key": "same_coframe_variation",
        "source_path": RESIDUALS / "P8_Y5_SAME_COFRAME_VARIATION_DERIVATION.csv",
        "needles": ["VD519_2_same_frame_identity", "conditional_zero_not_current_MTS_claim"],
    },
    {
        "source_id": "SRC1738_10_943_coupling_contract",
        "source_key": "943_coframe_coupling_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
        "needles": ["CFC943_7_contract_verdict", "contract_exact_but_unsigned"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1738_SOURCE_REGISTER.csv",
    "kernel_clause_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1738_COFRAME_KERNEL_CLAUSE_AUDIT.csv",
    "direction_classification": RESIDUALS / "P8_Y5_PARENT_QLOC_1738_DIRECTION_CLASSIFICATION.csv",
    "kernel_theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1738_KERNEL_THEOREM_ATTEMPT.csv",
    "common_frame_countermodels": RESIDUALS / "P8_Y5_PARENT_QLOC_1738_COMMON_FRAME_COUNTERMODELS.csv",
    "finite_DObs_e_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1738_FINITE_DOBS_E_SOURCE_ROWS.csv",
    "local_gr_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1738_LOCAL_GR_IMPACT_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1738_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1738_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1738_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1738_VALIDATION.csv",
}


COPY_MAP = {
    "kernel_clause_audit": "R2FR_1738_COFRAME_KERNEL_CLAUSE_AUDIT.csv",
    "direction_classification": "R2FR_1738_DIRECTION_CLASSIFICATION.csv",
    "kernel_theorem_attempt": "R2FR_1738_KERNEL_THEOREM_ATTEMPT.csv",
    "common_frame_countermodels": "R2FR_1738_COMMON_FRAME_COUNTERMODELS.csv",
    "finite_DObs_e_rows": "R2FR_1738_FINITE_DOBS_E_SOURCE_ROWS.csv",
    "local_gr_impact": "R2FR_1738_LOCAL_GR_IMPACT_LEDGER.csv",
    "decision": "R2FR_1738_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1738_CLAIM_GATE.csv",
    "next_target": "R2FR_1738_NEXT_TARGET.csv",
}


KERNEL_CLAUSES = [
    {
        "clause_id": "OCK1738_0_parent_q",
        "clause": "parent quotient map",
        "required_statement": "q_obs is supplied by the parent kinematics before local matter/readout calibration.",
        "mathematical_test": "q_obs: Phi_parent -> Q_obs exists and Dq_obs is computable.",
        "current_status": "Q_VIS_CONTRACT_ONLY",
        "blocker": "1737 and 1667 keep q as a candidate, not a signed parent chart.",
    },
    {
        "clause_id": "OCK1738_1_coframe_factorization",
        "clause": "observed coframe factorizes through q",
        "required_statement": "e_obs(Phi)=E(q_obs(Phi)) with no direct Z, phi, R_AB, boundary or marker argument.",
        "mathematical_test": "DObs_e[v]=DE(Dq_obs[v]); if Dq_obs[v]=0 then DObs_e[v]=0.",
        "current_status": "CONDITIONAL_SUPPORT_NOT_PARENT_SIGNED",
        "blocker": "1675 says e_obs=Obs_e(Q_vis) has support but is not parent-signed.",
    },
    {
        "clause_id": "OCK1738_2_kernel_membership",
        "clause": "candidate direction is in ker(Dq_obs)",
        "required_statement": "the specific v_Z, v_phi, v_RAB/Jq and boundary directions have Dq_obs[v]=0.",
        "mathematical_test": "Dq_obs[v_a]=0 componentwise for coframe, readout, marker, boundary and tau channels.",
        "current_status": "Dq_KERNEL_UNSIGNED",
        "blocker": "1737 finite Dq rows retain every component as missing numeric/theorem-zero.",
    },
    {
        "clause_id": "OCK1738_3_no_common_frame_derivative",
        "clause": "no residual-dependent common frame",
        "required_statement": "a universal coframe cannot still depend on X by e_obs=exp(B_X X)e0 or a disformal analogue.",
        "mathematical_test": "b_g,X := partial_X ln e_obs = 0 for every retained local residual direction.",
        "current_status": "COMMON_FRAME_COUNTERMODEL_SURVIVES",
        "blocker": "1504/623 explicitly keep universal conformal/common-frame countermodels alive.",
    },
    {
        "clause_id": "OCK1738_4_connection_lock",
        "clause": "connection follows the observed coframe",
        "required_statement": "omega_matter=omega[e_obs] or any torsion/nonmetricity/source connection is separately zeroed/bounded.",
        "mathematical_test": "Domega_m[v]=Domega[e_obs](DObs_e[v]) and no independent connection leak.",
        "current_status": "MISSING_CONNECTION_DESCENT",
        "blocker": "785/943 keep connection and hidden-frame coupling clauses unsigned.",
    },
    {
        "clause_id": "OCK1738_5_boundary_endpoint_silence",
        "clause": "boundary and endpoint data have zero local coframe projection",
        "required_statement": "boundary/exact endpoint terms do not alter the local observed coframe.",
        "mathematical_test": "P_loc(partial e_obs/partial Q_endpoint)=0 and no clock/WEP/PPN boundary component survives.",
        "current_status": "BOUNDARY_ENDPOINT_SILENCE_NOT_PARENT_SIGNED",
        "blocker": "862/863 keep endpoint and boundary silence open.",
    },
    {
        "clause_id": "OCK1738_6_verdict",
        "clause": "observed coframe kernel verdict",
        "required_statement": "OCK1738_0 through OCK1738_5 all pass in the same parent branch.",
        "mathematical_test": "DObs_e[v_a]=0 for all coframe-relevant retained directions.",
        "current_status": "DOBS_E_KERNEL_ZERO_NOT_SIGNED",
        "blocker": "the chain-rule theorem is exact, but parent q/coframe/kernel/common-frame/connection/boundary clauses are unsigned.",
    },
]


DIRECTIONS = [
    {
        "direction_id": "DCL1738_0_vZ",
        "direction": "v_Z=partial_Z",
        "coframe_relevance": "direct_candidate",
        "kernel_test": "DObs_e[v_Z]=0",
        "current_status": "MISSING_PARENT_SELECTOR_AND_Z_BASIS",
        "finite_row": "DOE1738_0_vZ",
    },
    {
        "direction_id": "DCL1738_1_vphi",
        "direction": "v_phi=partial_phi",
        "coframe_relevance": "direct_candidate",
        "kernel_test": "DObs_e[v_phi]=0",
        "current_status": "PHI_IMPROVEMENT_OWNER_UNSIGNED",
        "finite_row": "DOE1738_1_vphi",
    },
    {
        "direction_id": "DCL1738_2_vRAB_Jq",
        "direction": "v_RAB/Jq",
        "coframe_relevance": "direct_or_cell_readout_candidate",
        "kernel_test": "DObs_e[v_RAB/Jq]=0",
        "current_status": "OBSERVER_CELL_DATA_MAY_BE_VISIBLE",
        "finite_row": "DOE1738_2_vRAB_Jq",
    },
    {
        "direction_id": "DCL1738_3_vboundary",
        "direction": "v_boundary/projector",
        "coframe_relevance": "boundary_endpoint_candidate",
        "kernel_test": "P_loc DObs_e[v_boundary]=0",
        "current_status": "BOUNDARY_PROJECTOR_NOT_BASIC",
        "finite_row": "DOE1738_3_vboundary",
    },
    {
        "direction_id": "DCL1738_4_vtheta_marker",
        "direction": "v_theta_marker",
        "coframe_relevance": "not_primary_coframe_kernel",
        "kernel_test": "route to Dtheta_marker, not DObs_e",
        "current_status": "ROUTE_TO_SOURCE_READOUT_MARKER_BRANCH",
        "finite_row": "NOT_A_DOBS_E_ROW",
    },
    {
        "direction_id": "DCL1738_5_vtau_readout",
        "direction": "v_tau_readout",
        "coframe_relevance": "not_primary_coframe_kernel",
        "kernel_test": "route to tau pushforward, not DObs_e",
        "current_status": "ROUTE_TO_TAU_PUSHFORWARD_BRANCH",
        "finite_row": "NOT_A_DOBS_E_ROW",
    },
]


COUNTERMODELS = [
    {
        "countermodel_id": "CM1738_0_common_Weyl",
        "form": "e_obs = exp(b_g X) e0",
        "why_it_survives": "one universal coframe can still depend on a residual direction and produce local metric/PPN/fifth-force effects",
        "repair": "derive b_g=0 from parent coframe ownership or retain b_g as a finite row",
    },
    {
        "countermodel_id": "CM1738_1_common_disformal",
        "form": "g_obs = C(X)g0 + D(X)u_mu u_nu",
        "why_it_survives": "same-frame matter does not exclude universal disformal dependence",
        "repair": "prove disformal/current residual coefficients vanish or bound them in PPN/clock rows",
    },
    {
        "countermodel_id": "CM1738_2_representative_invariant_scalar",
        "form": "e_obs = exp(F(C_D)) e0 with F'(C_D) nonzero",
        "why_it_survives": "being representative-invariant is not the same as being locally vertical-blind",
        "repair": "derive local extremum/selector theorem forcing F'=0",
    },
    {
        "countermodel_id": "CM1738_3_boundary_endpoint",
        "form": "e_obs = E(q_loc,Q_endpoint) with P_loc partial_Q_endpoint E nonzero",
        "why_it_survives": "cosmological or boundary memory can leak into local coframe unless no-hair/projection silence is proved",
        "repair": "prove endpoint boundary silence or retain local projection row",
    },
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def source_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles": ";".join(needles),
                "needles_present": yesno(exists and all(needle in text for needle in needles)),
                "checked_utc": UTC,
            }
        )
    return rows


def kernel_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            **clause,
            "parent_signed": no(),
            "kernel_zero_proved": no(),
            "finite_row_required": "True",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for clause in KERNEL_CLAUSES
    ]


def direction_classification_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            **direction,
            "coframe_kernel_zero_proved": no(),
            "accepted_for_scoring": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for direction in DIRECTIONS
    ]


def kernel_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "DOK1738_0_chain_rule_kernel",
            "statement": "If e_obs=E(q_obs(Phi)) and v is in ker(Dq_obs), then DObs_e[v]=0.",
            "mathematical_form": "DObs_e[v]=DE|_q(Dq_obs[v])=DE|_q(0)=0",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "MISSING_PARENT_Q;MISSING_E_OBS_FACTORISATION;MISSING_DQ_KERNEL;MISSING_NO_COMMON_FRAME_DERIVATIVE",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "DOK1738_1_same_coframe_not_enough",
            "statement": "A universal coframe does not prove local invisibility if that same coframe depends on residual variables.",
            "mathematical_form": "e_obs=exp(b_g X)e0 gives one frame but DObs_e[partial_X]=b_g e_obs",
            "proof_status": "COUNTERMODEL_SURVIVES",
            "missing_for_current_claim": "MISSING_B_G_ZERO_THEOREM_OR_BOUND",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "DOK1738_2_current_verdict",
            "statement": "Current MTS proves DObs_e[v_a]=0 for all coframe-relevant vertical directions.",
            "mathematical_form": "OCK1738_0..OCK1738_5 all parent-signed and direction rows DCL1738_0..DCL1738_3 pass",
            "proof_status": "DOBS_E_KERNEL_ZERO_NOT_SIGNED",
            "missing_for_current_claim": "Q_AND_COFRAME_OWNERSHIP_UNSIGNED;COMMON_FRAME_COUNTERMODEL_OPEN;BOUNDARY_ENDPOINT_SILENCE_OPEN",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            **countermodel,
            "excluded_by_current_parent": no(),
            "finite_row_required": "True",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for countermodel in COUNTERMODELS
    ]


def finite_DObs_e_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DBG1738_0_common_frame_log_derivative",
            "symbol": "b_g,X",
            "direction": "generic coframe-relevant residual X",
            "definition": "norm of partial_X ln e_obs or equivalent common-frame derivative",
            "formula": "b_g,X := ||e_obs^{-1} DObs_e[partial_X]||",
            "units": "dimensionless_per_declared_X_unit_or_component_norm_MISSING",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "source_path": "MISSING_SOURCE_PATH",
            "status": "RETAINED_NONCLAIM_COMMON_FRAME_ROW",
            "accepted_for_scoring": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
    ]
    for direction in DIRECTIONS[:4]:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": direction["finite_row"],
                "symbol": "DObs_e[v]",
                "direction": direction["direction"],
                "definition": "observed coframe derivative along candidate local vertical direction",
                "formula": direction["kernel_test"],
                "units": "coframe_norm_or_metric_norm_MISSING",
                "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "RETAINED_NONCLAIM_DOBS_E_ROW",
                "accepted_for_scoring": no(),
                "score_ready": no(),
                "valid_prediction_row": no(),
                "valid_for_claim": no(),
                "claim_allowed": no(),
            }
        )
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "DOE1738_4_total_coframe_kernel_envelope",
            "symbol": "epsilon_DObs_e_abs",
            "direction": "all coframe-relevant directions",
            "definition": "absolute no-cancellation envelope for observed-coframe leakage",
            "formula": "sum_a ||DObs_e[v_a]|| over v_Z,v_phi,v_RAB/Jq,v_boundary plus common-frame derivative row",
            "units": "common_coframe_norm_MISSING",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "source_path": "MISSING_SOURCE_PATH",
            "status": "RETAINED_NONCLAIM_ENVELOPE",
            "accepted_for_scoring": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
    )
    return rows


def local_gr_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "LGI1738_0_metric_limit",
            "local_limit": "GR metric carrier",
            "needed_condition": "epsilon_DObs_e_abs=0 or bounded below local metric/PPN thresholds",
            "current_status": "BLOCKED",
            "reason": "DObs_e kernel zero is not signed",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "LGI1738_1_Newton_limit",
            "local_limit": "Newtonian weak-field potential",
            "needed_condition": "metric carrier fixed plus source normalization and Gauss/Poisson operator closure",
            "current_status": "BLOCKED",
            "reason": "coframe ownership is upstream of the Newton reduction chain",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "LGI1738_2_WEP_PPN",
            "local_limit": "WEP/PPN smoke gates",
            "needed_condition": "DObs_e, source/readout, marker, boundary and tau rows are zero or source-backed bounded",
            "current_status": "BLOCKED",
            "reason": "coframe row alone is necessary but not sufficient",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1738_0_chain_rule",
            "decision": "CHAIN_RULE_KERNEL_THEOREM_VALID",
            "reason": "DObs_e[v]=0 follows immediately if e_obs factorizes through q and v is in ker(Dq)",
            "next_action": "do not abandon the derivation route; source the missing parent coframe ownership",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1738_1_same_coframe_warning",
            "decision": "SAME_COFRAME_IS_NOT_ENOUGH",
            "reason": "a universal coframe can still depend on residual variables through a common-frame derivative b_g",
            "next_action": "derive b_g=0 or keep b_g as the first finite coframe row",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1738_2_current_status",
            "decision": "DOBS_E_KERNEL_NOT_CLOSED",
            "reason": "q/coframe ownership, Dq kernel, common-frame countermodels and boundary endpoint silence remain unsigned",
            "next_action": "retain finite DObs_e rows and keep local-GR claim blocked",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1738_3_best_next_domino",
            "decision": "TARGET_PARENT_COFRAME_OWNERSHIP_OR_BG_ROW",
            "reason": "this is the smallest upstream theorem that can turn same-frame structure into real local metric invisibility",
            "next_action": "attempt parent coframe ownership or stage common-frame log-derivative row for bounds",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1738_0_DObs_e_zero",
            "claim": "observed coframe kernel vanishes",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "DOBS_E_KERNEL_ZERO_NOT_SIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1738_1_bg_zero",
            "claim": "common-frame derivative b_g is zero",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "COMMON_FRAME_COUNTERMODEL_SURVIVES",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1738_2_metric_GR_limit",
            "claim": "local metric branch reduces to GR",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "NO_PARENT_COFRAME_OWNERSHIP_NO_EINSTEIN_REDUCTION",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1738_3_Newton_limit",
            "claim": "Newtonian limit follows",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "NO_METRIC_GR_SOURCE_NORMALIZATION_CHAIN",
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1738_0_primary",
            "next_target": "1739-Y5-R2FR-parent-coframe-ownership-or-common-frame-log-derivative-row.md",
            "script": "scripts/Y5_R2FR_parent_coframe_ownership_or_common_frame_log_derivative_row.py",
            "objective": "derive e_obs=E(Q_vis) with no residual argument, or stage b_g/common-frame log-derivative rows for finite local bounds",
            "success_condition": "parent-signed coframe ownership theorem or source-backed nonclaim b_g row ready for WEP/PPN/R10 smoke gates",
            "selection_status": "selected",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1738_1_parallel_readout",
            "next_target": "1738b-Y5-R2FR-source-readout-marker-Dq-zero-or-finite-row.md",
            "script": "scripts/Y5_R2FR_source_readout_marker_Dq_zero_or_finite_row.py",
            "objective": "prove source/readout and marker functors descend through q, or keep finite leak rows",
            "success_condition": "source/readout and marker rows source-backed with units and nonclaim comparisons",
            "selection_status": "held_parallel",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1738_2_later_tau",
            "next_target": "1740-Y5-R2FR-tau-pushforward-on-qvis-or-finite-Dtau-row.md",
            "script": "scripts/Y5_R2FR_tau_pushforward_on_qvis_or_finite_Dtau_row.py",
            "objective": "prove the observed-time generator is the pushforward of one parent tau on Q_vis",
            "success_condition": "tau pushforward theorem or finite Dtau row for commutator and PPN gates",
            "selection_status": "later",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "kernel_clause_audit": kernel_clause_rows(),
        "direction_classification": direction_classification_rows(),
        "kernel_theorem_attempt": kernel_theorem_rows(),
        "common_frame_countermodels": countermodel_rows(),
        "finite_DObs_e_rows": finite_DObs_e_rows(),
        "local_gr_impact": local_gr_impact_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1738_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1738_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {
        "accepted_for_scoring",
        "claim_allowed",
        "coframe_kernel_zero_proved",
        "excluded_by_current_parent",
        "gate_pass",
        "kernel_zero_proved",
        "parent_signed",
        "score_allowed",
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    readiness = {
        "accepted_for_scoring",
        "claim_allowed",
        "coframe_kernel_zero_proved",
        "excluded_by_current_parent",
        "gate_pass",
        "kernel_zero_proved",
        "parent_signed",
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for rows in rows_map.values():
        for row in rows:
            contains_missing = any("MISSING_" in str(value) for value in row.values())
            if contains_missing and any(str(row.get(flag, "")).lower() == "true" for flag in readiness):
                return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1738_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1738_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1738*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    source_register = rows_map["source_register"]
    clauses = rows_map["kernel_clause_audit"]
    directions = rows_map["direction_classification"]
    theorem_rows = rows_map["kernel_theorem_attempt"]
    countermodels = rows_map["common_frame_countermodels"]
    finite_rows = rows_map["finite_DObs_e_rows"]
    local_impact = rows_map["local_gr_impact"]
    decision = rows_map["decision"]
    claim_rows = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1738_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1738_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check("VAL1738_2_kernel_clauses_complete", {row["clause_id"] for row in clauses} == {row["clause_id"] for row in KERNEL_CLAUSES}, "coframe kernel clause audit covers all required blockers", "kernel clause audit missing row"),
        check("VAL1738_3_kernel_zero_not_signed", all(row["kernel_zero_proved"] == "False" and row["claim_allowed"] == "False" for row in clauses), "no coframe kernel clause signs a zero theorem", "a coframe kernel clause opened a claim"),
        check("VAL1738_4_direction_classification_complete", {row["direction_id"] for row in directions} == {row["direction_id"] for row in DIRECTIONS}, "candidate directions are classified for coframe relevance", "direction classification missing row"),
        check("VAL1738_5_chain_rule_recorded", any(row["theorem_id"] == "DOK1738_0_chain_rule_kernel" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem_rows), "exact chain-rule kernel theorem is recorded", "chain-rule kernel theorem row missing"),
        check("VAL1738_6_same_coframe_warning", any(row["theorem_id"] == "DOK1738_1_same_coframe_not_enough" and row["proof_status"] == "COUNTERMODEL_SURVIVES" for row in theorem_rows), "same-coframe-not-enough countermodel is recorded", "same-coframe countermodel row missing"),
        check("VAL1738_7_countermodels_retained", all(row["excluded_by_current_parent"] == "False" for row in countermodels), "all common-frame countermodels remain active until parent proof", "a countermodel was incorrectly excluded"),
        check("VAL1738_8_finite_rows_nonclaim", all(row["valid_for_claim"] == "False" and row["score_ready"] == "False" for row in finite_rows), "finite DObs_e/common-frame rows are nonclaim and not score-ready", "finite coframe row became claim-ready or score-ready"),
        check("VAL1738_9_local_impact_blocked", all(row["current_status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in local_impact), "local GR/Newton impact rows remain blocked", "a local impact row opened a claim"),
        check("VAL1738_10_decision_next_domino", any(row["decision_id"] == "DEC1738_3_best_next_domino" and row["decision"] == "TARGET_PARENT_COFRAME_OWNERSHIP_OR_BG_ROW" for row in decision), "decision selects parent coframe ownership or b_g row as next domino", "decision ledger did not select parent coframe ownership"),
        check("VAL1738_11_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claim_rows), "all claim gates keep local claims false", "one or more claim gates opened"),
        check("VAL1738_12_no_claim_flags", no_claim_flags(rows_map), "all generated rows keep claim/no-score flags false", "one or more generated flags enabled a claim"),
        check("VAL1738_13_missing_not_ready", missing_rows_not_ready(rows_map), "no row containing MISSING_* is marked source-backed, claim-ready, or score-ready", "a missing row is marked ready"),
        check("VAL1738_14_next_selected", any(row["route_id"] == "NEXT1738_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selects parent coframe ownership or common-frame log-derivative row", "next target missing selected primary route"),
        check("VAL1738_15_csv_parse", parsed_ok, "all generated 1738 CSVs parse", "one or more generated 1738 CSVs failed to parse"),
        check("VAL1738_16_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1738_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1738_18_formalization_untouched", formalization_untouched(), "no 1738 outputs found under formalization-workbench", "1738 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1738_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1738 observed coframe kernel zero or first finite DObs_e row validation" if overall else "one or more 1738 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- The chain-rule coframe-kernel theorem is exact: `e_obs=E(q(Phi))` and `Dq[v]=0` imply `DObs_e[v]=0`.",
        "- The current corpus does not yet sign the theorem because parent coframe ownership and kernel membership remain open.",
        "- The important red-team catch is that a single universal coframe is not enough: `e_obs=exp(b_g X)e0` is still one frame, but it is locally physical unless `b_g=0` is derived or bounded.",
        "- Therefore 1738 stages finite nonclaim `DObs_e` and common-frame derivative rows.",
        "- No local-GR, Newton, WEP, PPN, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Why This Is A Real GR Gate",
        "GR locally begins with the metric/coframe carrier being the thing ordinary matter sees. If MTS residual directions move that carrier, they are not invisible. If they do not move it, the theory still has to close source/readout, marker, boundary, and tau leaks — but the metric branch becomes much cleaner.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Coframe Kernel Clause Audit",
        markdown_table(rows_map["kernel_clause_audit"], ["clause_id", "clause", "mathematical_test", "current_status", "blocker"]),
        "",
        "## Direction Classification",
        markdown_table(rows_map["direction_classification"], ["direction_id", "direction", "coframe_relevance", "kernel_test", "current_status", "finite_row"]),
        "",
        "## Kernel Theorem Attempt",
        markdown_table(rows_map["kernel_theorem_attempt"], ["theorem_id", "statement", "mathematical_form", "proof_status", "missing_for_current_claim"]),
        "",
        "## Common Frame Countermodels",
        markdown_table(rows_map["common_frame_countermodels"], ["countermodel_id", "form", "why_it_survives", "repair"]),
        "",
        "## Finite DObs e Rows",
        markdown_table(rows_map["finite_DObs_e_rows"], ["row_id", "symbol", "direction", "formula", "value_or_formula", "status"]),
        "",
        "## Local GR Impact",
        markdown_table(rows_map["local_gr_impact"], ["impact_id", "local_limit", "needed_condition", "current_status", "reason"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "This is probably the cleanest current local branch: parent coframe ownership must either kill `b_g` or hand us a finite `b_g` row to compare against local tests. That is not a dead end; it is the correct Grossmann-style geometry problem hiding under the physics language.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1738-Y5-R2FR-observed-coframe-kernel-zero-or-first-finite-DObs-e-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1738_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1738 validation FAIL")
    print("1738 validation PASS")


if __name__ == "__main__":
    main()
