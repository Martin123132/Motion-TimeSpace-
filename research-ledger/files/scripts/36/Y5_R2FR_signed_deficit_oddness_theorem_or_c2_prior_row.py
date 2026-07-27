from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1825"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1825-Y5-R2FR-signed-deficit-oddness-theorem-or-c2-prior-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1825_0_1824_next",
        "source_key": "1824_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1824_NEXT_TARGET.csv",
        "needles": ["NEXT1824_0_primary", "selected"],
        "role": "1824 selects signed-deficit oddness as the next target.",
    },
    {
        "source_id": "SRC1825_1_1824_validation",
        "source_key": "1824_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1824_VALIDATION.csv",
        "needles": ["VAL1824_OVERALL", "PASS"],
        "role": "confirms 1824 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1825_2_1824_phi",
        "source_key": "1824_phi_attempt",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1824_PHI_SECOND_DERIVATIVE_ZERO_THEOREM_ATTEMPT.csv",
        "needles": ["PZ1824_1_signed_oddness", "ODDNESS_NOT_PARENT_DERIVED"],
        "role": "signed oddness is exact but not parent-derived.",
    },
    {
        "source_id": "SRC1825_3_1824_symmetry",
        "source_key": "1824_symmetry_route",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1824_SIGNED_DEFICIT_SYMMETRY_ROUTE_AUDIT.csv",
        "needles": ["SDA1824_3_log_angle_owner", "BEST_NEXT_TARGET"],
        "role": "signed log-holonomy/angle ownership is the cleanest zero route.",
    },
    {
        "source_id": "SRC1825_4_1824_c2",
        "source_key": "1824_visible_c2",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1824_VISIBLE_C2_SOURCE_ROW.csv",
        "needles": ["C2S1824_3_total", "MISSING_ZERO_OR_FINITE_SOURCE_ROW_NONCLAIM"],
        "role": "visible c2 remains a nonclaim source-row contract.",
    },
    {
        "source_id": "SRC1825_5_odd_theorem",
        "source_key": "odd_residual_theorem",
        "source_path": RESIDUALS / "P8_ODD_RESIDUAL_EXCHANGE_THEOREM.csv",
        "needles": ["E5_current_corpus", "conditional theorem only"],
        "role": "older odd-residual theorem route is conditional only.",
    },
    {
        "source_id": "SRC1825_6_odd_decision",
        "source_key": "odd_residual_decision",
        "source_path": RESIDUALS / "P8_ODD_RESIDUAL_DECISION.csv",
        "needles": ["D3_promotion", "forbidden"],
        "role": "older oddness route forbids promotion.",
    },
    {
        "source_id": "SRC1825_7_orientation_arrow",
        "source_key": "867_orientation_arrow",
        "source_path": RESIDUALS / "P8_Y5_R10_867_ORIENTATION_ARROW_AUDIT.csv",
        "needles": ["OA867_1_boundary_orientation_flip", "mathematically_viable_but_unsigned"],
        "role": "orientation flip is viable but unsigned.",
    },
    {
        "source_id": "SRC1825_8_orientation_signature",
        "source_key": "881_orientation_signature",
        "source_path": RESIDUALS / "P8_Y5_R10_881_ORIENTATION_SIGNATURE_AUDIT.csv",
        "needles": ["OS881_4_orientation_verdict", "partial_progress_nonclaim"],
        "role": "relative-chain orientation is partial progress but not a claim.",
    },
    {
        "source_id": "SRC1825_9_holonomy_zero",
        "source_key": "920_holonomy",
        "source_path": RESIDUALS / "P8_Y5_R10_920_HOLONOMY_ZERO_AUDIT.csv",
        "needles": ["HOL920_3_nontrivial_cycle_fallback", "retained_bound_row"],
        "role": "holonomy route keeps residual/bound fallbacks when topology is not fixed.",
    },
    {
        "source_id": "SRC1825_10_lifted_c",
        "source_key": "1165_lifted_C_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_1165_LIFTED_C_PARENT_ACTION_CONTRACT.csv",
        "needles": ["LPC1165_2_parent_action_term", "ACTION_CONTRACT_STUB_ONLY"],
        "role": "lifted form/holonomy action remains a contract stub.",
    },
    {
        "source_id": "SRC1825_11_endpoint",
        "source_key": "111_endpoint_owner",
        "source_path": ROOT / "111-endpoint-quadratic-variational-owner-attempt.md",
        "needles": ["variational_owner_written_but_not_parent_derived", "constraint_trick_rejected"],
        "role": "endpoint variational owner is not a parent derivation.",
    },
]


OUTPUTS: dict[str, Path] = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1825_SOURCE_REGISTER.csv",
    "oddness_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1825_SIGNED_DEFICIT_ODDNESS_THEOREM_ATTEMPT.csv",
    "orientation_owner_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1825_ORIENTATION_OWNER_AUDIT.csv",
    "c2_prior_row": RESIDUALS / "P8_Y5_PARENT_QLOC_1825_C2_PRIOR_SOURCE_ROW.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1825_COUNTERMODEL_LEDGER.csv",
    "gr_newton_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1825_GR_NEWTON_IMPACT_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1825_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1825_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1825_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1825_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1825_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for path in {RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "yes", "1", "pass", "passed"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    headers = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        text = read_text(path)
        exists = path.exists()
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
            }
        )
    return rows


def oddness_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SDO1825_0_target",
            "claim_piece": "signed-deficit oddness theorem",
            "mathematical_statement": "Show the primitive deficit response satisfies Phi(-delta)=-Phi(delta), so c2_visible=Phi''(0)/2=0.",
            "derivation_result": "TARGET_ATTEMPTED",
            "current_status": "NOT_PARENT_PROVEN",
            "consequence": "visible c2 remains live unless orientation/log-angle ownership closes",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SDO1825_1_exact_math",
            "claim_piece": "odd smooth response kills even coefficients",
            "mathematical_statement": "For smooth Phi(delta)=sum_n a_n delta^n, the identity Phi(-delta)=-Phi(delta) implies a_2=a_4=...=0; therefore Phi''(0)=0.",
            "derivation_result": "EXACT_LEMMA",
            "current_status": "MATH_OK_PARENT_PREMISE_UNSIGNED",
            "consequence": "the quadratic wound closes if oddness is parent-owned",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SDO1825_2_orientation_not_enough",
            "claim_piece": "orientation alone does not imply odd action",
            "mathematical_statement": "An oriented deficit variable can still enter an even scalar action such as delta^2, 1-cos(delta), Tr(I-U), or ||log U||^2.",
            "derivation_result": "LOOPHOLE_IDENTIFIED",
            "current_status": "EVEN_COST_COUNTERMODELS_LIVE",
            "consequence": "must prove action is a signed charge, not merely that delta has a sign",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SDO1825_3_gauge_vs_physical_orientation",
            "claim_piece": "orientation reversal status",
            "mathematical_statement": "If delta -> -delta is a gauge/relabeling reversal, the action should be invariant rather than odd; if it is a physical boundary-charge orientation, oddness can be meaningful.",
            "derivation_result": "CENTRAL_OWNER_TEST",
            "current_status": "PHYSICAL_ORIENTATION_NOT_PARENT_SIGNED",
            "consequence": "oddness cannot be promoted until orientation is owned as physical charge orientation",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SDO1825_4_log_angle_route",
            "claim_piece": "signed log-holonomy action owner",
            "mathematical_statement": "A parent action linear in the signed log-holonomy angle can be odd, while trace/norm holonomy actions are even at leading order.",
            "derivation_result": "BEST_ROUTE_NOT_PROOF",
            "current_status": "LOG_ANGLE_OWNER_MISSING",
            "consequence": "selects the next target",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SDO1825_5_odd_not_GR",
            "claim_piece": "oddness is not full EH",
            "mathematical_statement": "Even if c2 is killed, odd cubic and higher terms can remain; local EH/GR still needs higher-operator gates and source/C-term closure.",
            "derivation_result": "CLAIM_SCOPE_GUARD",
            "current_status": "HIGHER_ODD_TERMS_UNAUDITED",
            "consequence": "no local-GR promotion from c2 oddness alone",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SDO1825_6_verdict",
            "claim_piece": "1825 proves signed-deficit oddness",
            "mathematical_statement": "The theorem is exact if the action is a signed charge of oriented log-holonomy; current corpus only has conditional orientation/oddness support and nonclaim contracts.",
            "derivation_result": "CONDITIONAL_THEOREM_NOT_CURRENT_PROOF",
            "current_status": "DEMOTE_TO_C2_PRIOR_ROW",
            "consequence": "c2_visible remains explicit nonclaim coefficient debt",
            "valid_for_claim": False,
        },
    ]


def orientation_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OOA1825_0_signed_variable",
            "needed_owner": "oriented signed deficit variable",
            "formal_condition": "orientation reversal maps delta to -delta on the physical primitive cell",
            "current_status": "CANDIDATE_ONLY",
            "blocker": "orientation sign exists as a viable route but is not parent-owned",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OOA1825_1_physical_not_gauge",
            "needed_owner": "orientation is physical boundary/charge orientation, not a gauge convention",
            "formal_condition": "reversal changes the oriented charge/action contribution rather than relabeling the same state",
            "current_status": "NOT_DERIVED",
            "blocker": "relative-chain and endpoint-arrow owners remain unsigned",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OOA1825_2_signed_charge_action",
            "needed_owner": "primitive action is a signed first-moment charge",
            "formal_condition": "S_h proportional to signed log(U_h), signed deficit angle, or oriented boundary charge",
            "current_status": "LOG_ANGLE_OWNER_MISSING",
            "blocker": "lifted form/holonomy action is still a contract stub",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OOA1825_3_even_cost_exclusion",
            "needed_owner": "exclude trace/norm/energy/entropy costs",
            "formal_condition": "Phi is not Tr(I-U), 1-cos(delta), ||log U||^2, delta^2, or a positive mismatch energy",
            "current_status": "NOT_EXCLUDED",
            "blocker": "positive-energy and endpoint potential routes can naturally be even",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OOA1825_4_verdict",
            "needed_owner": "signed-deficit oddness owner stack",
            "formal_condition": "OOA1825_0 through OOA1825_3 all parent-signed",
            "current_status": "FAIL_CURRENT_OWNER_STACK",
            "blocker": "current corpus has no parent-signed log-angle/physical orientation action",
            "valid_for_claim": False,
        },
    ]


def c2_prior_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "C2P1825_0_zero_switch",
            "row_type": "conditional_zero_switch",
            "quantity": "c2_visible",
            "formula_or_value": "0 if signed log-angle action oddness is parent-signed",
            "required_inputs": "physical orientation; signed charge action; even-cost exclusion; source path",
            "units": "dimensionless_deficit_response",
            "source_path": "",
            "current_status": "ZERO_THEOREM_UNSIGNED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "C2P1825_1_norm_prior",
            "row_type": "finite_prior_example",
            "quantity": "c2_visible",
            "formula_or_value": "1 for Phi(delta)=delta^2 under the current expansion convention",
            "required_inputs": "actual parent selection of squared norm cost; normalization convention; source path",
            "units": "dimensionless_deficit_response",
            "source_path": "",
            "current_status": "EXAMPLE_ONLY_NOT_PARENT_SELECTED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "C2P1825_2_trace_prior",
            "row_type": "finite_prior_example",
            "quantity": "c2_visible",
            "formula_or_value": "1/2 for Phi(delta)=1-cos(delta) under the current expansion convention",
            "required_inputs": "actual parent selection of trace/class holonomy cost; normalization convention; source path",
            "units": "dimensionless_deficit_response",
            "source_path": "",
            "current_status": "EXAMPLE_ONLY_NOT_PARENT_SELECTED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "C2P1825_3_general_finite",
            "row_type": "finite_c2_prior_source_row",
            "quantity": "c2_visible",
            "formula_or_value": "c2_visible = 1/2 Phi''(0)",
            "required_inputs": "parent Phi expansion; sign; normalization; uncertainty/prior width; cell scale; shape factor; source path",
            "units": "dimensionless_deficit_response",
            "source_path": "",
            "current_status": "MISSING_PARENT_PHI_AND_PRIOR_WIDTH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "C2P1825_4_total",
            "row_type": "c2_prior_contract",
            "quantity": "visible_c2_prior_to_R2FR",
            "formula_or_value": "valid only if zero switch or finite c2 prior plus c_R2_eff/lambda/alpha maps exist",
            "required_inputs": "C2P1825_0 or C2P1825_3; ell_cell; shape_factor; EH normalization; weak-field response",
            "units": "row_contract",
            "source_path": "",
            "current_status": "MISSING_ZERO_OR_FINITE_PRIOR_ROW_NONCLAIM",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1825_0_trace_even",
            "countermodel": "primitive holonomy action is trace/class cost such as 1-cos(delta)",
            "why_it_survives": "trace holonomy is natural and even unless signed log-angle ownership is derived",
            "blocked_by": "parent-signed log-angle/signed-charge action theorem",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1825_1_norm_energy",
            "countermodel": "primitive action is a positive norm or mismatch energy",
            "why_it_survives": "orientation sign drops out of a norm, leaving c2 live",
            "blocked_by": "exclude norm/energy route from parent grammar or source finite c2",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1825_2_orientation_gauge",
            "countermodel": "delta reversal is a gauge/relabeling choice",
            "why_it_survives": "then action should be invariant/even, not odd",
            "blocked_by": "physical boundary-charge orientation theorem",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1825_3_odd_higher_terms",
            "countermodel": "Phi is odd but includes delta^3 and higher terms",
            "why_it_survives": "oddness only kills even coefficients; it is not a full EH theorem",
            "blocked_by": "higher odd term gate or explicit operator rows",
            "retained": True,
            "valid_for_claim": False,
        },
    ]


def gr_newton_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1825_0_if_oddness_closes",
            "if_closed": "signed log-angle/physical orientation action theorem is parent-signed",
            "would_buy": "visible c2/R2 quadratic deficit coefficient zero, tightening the EH operator route",
            "still_missing": "higher odd curvature terms, hidden tower, connection, source and C-term gates",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1825_1_if_c2_prior_filled",
            "if_closed": "finite c2 prior/source row is supplied",
            "would_buy": "R2/fR scalar branch becomes quantitative rather than vague",
            "still_missing": "cell-scale map, full bound curve, PPN response and matter coupling",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1825_2_verdict",
            "if_closed": "1825 alone proves local GR/Newton",
            "would_buy": "nothing claimable alone; this is one visible quadratic coefficient subgate",
            "still_missing": "broader GR/Newton derivation stack remains open",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1825_0_oddness_attempt_written",
            "gate": "signed-deficit oddness attempt written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "1825 separates exact oddness math from the missing parent owner",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1825_1_physical_orientation",
            "gate": "orientation reversal is physical charge orientation",
            "current_status": "BLOCKED",
            "reason": "relative-chain/endpoint orientation support is unsigned",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1825_2_log_angle_owner",
            "gate": "parent action owns signed log-holonomy/angle",
            "current_status": "BLOCKED",
            "reason": "lifted form/holonomy action is still a contract stub",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1825_3_c2_prior",
            "gate": "finite c2 prior/source row filled",
            "current_status": "BLOCKED",
            "reason": "parent Phi, prior width, cell scale and response maps are missing",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1825_0_oddness",
            "claim": "signed-deficit oddness is derived",
            "status": "BLOCKED",
            "reason": "physical orientation and log-angle owner are unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1825_1_c2_zero",
            "claim": "c2_visible is theorem-zero",
            "status": "BLOCKED",
            "reason": "oddness zero switch is unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1825_2_R2FR_score",
            "claim": "R2/fR finite scalar branch can be scored",
            "status": "REFUSED",
            "reason": "c2 prior/source, cell scale and response maps are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1825_3_local_GR",
            "claim": "local GR/Newton follows",
            "status": "REFUSED",
            "reason": "oddness is one subgate and remains unproven",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1825_0_oddness_result",
            "decision": "SIGNED_DEFICIT_ODDNESS_NOT_PROVEN",
            "reason": "oddness math is exact, but parent action ownership of physical signed log-holonomy is missing",
            "next_action": "do not set c2_visible to zero",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1825_1_best_route",
            "decision": "LOG_HOLONOMY_ACTION_OWNER_NEXT",
            "reason": "the precise next route is to derive the parent action variable as signed log-holonomy/angle rather than trace/norm",
            "next_action": "attempt log-holonomy action owner theorem",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1825_2_fallback",
            "decision": "C2_PRIOR_ROW_READY_NONCLAIM",
            "reason": "if log-angle ownership fails, c2_visible needs a finite prior/source path before R2/fR tests",
            "next_action": "keep finite c2 invalid for claim until sourced",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1825_3_best_next",
            "decision": "LOG_HOLONOMY_ACTION_OWNER_OR_TRACE_NORM_C2_PRIOR_NEXT",
            "reason": "the route is now a clean fork: signed log-angle action zeroes c2; trace/norm action sources c2",
            "next_action": "1826-Y5-R2FR-log-holonomy-action-owner-or-trace-norm-c2-prior.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1825_0_primary",
            "next_target": "1826-Y5-R2FR-log-holonomy-action-owner-or-trace-norm-c2-prior.md",
            "script": "scripts/Y5_R2FR_log_holonomy_action_owner_or_trace_norm_c2_prior.py",
            "objective": "derive whether the parent action owns signed log-holonomy/angle instead of trace/norm holonomy cost; if not, source trace/norm c2 prior rows",
            "selection_status": "selected",
            "success_condition": "log-angle action owner signed, or trace/norm c2 prior rows remain valid_for_claim=false with all inputs explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1825_1_parallel",
            "next_target": "1826b-Y5-R2FR-higher-odd-term-gate-if-c2-zero.md",
            "script": "scripts/Y5_R2FR_higher_odd_term_gate_if_c2_zero.py",
            "objective": "only if c2 is zeroed, audit cubic and higher odd curvature terms before any EH/local-GR claim",
            "selection_status": "held_parallel",
            "success_condition": "higher odd terms are theorem-zero, bounded, or retained nonclaim",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "oddness_theorem": oddness_theorem_rows(),
        "orientation_owner_audit": orientation_owner_rows(),
        "c2_prior_row": c2_prior_rows(),
        "countermodel_ledger": countermodel_rows(),
        "gr_newton_impact": gr_newton_impact_rows(),
        "acceptance_gate": acceptance_gate_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def copy_outputs() -> None:
    for output in generated_csvs():
        for target_dir in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(output, target_dir / output.name)


def branch_copies_exist() -> bool:
    for output in generated_csvs():
        for target_dir in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
            if not (target_dir / output.name).exists():
                return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    names = {DOC_PATH.name, OUTPUTS["validation"].name} | {path.name for path in generated_csvs()}
    return not any(path.name in names for path in FORMALIZATION.rglob("*") if path.is_file())


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    allowed_gate_pass = {"AC1825_0_oddness_attempt_written"}
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for field in ("valid_for_claim", "claim_allowed_now", "claim_allowed", "score_ready", "gate_pass"):
                if field in row and boolish(row[field]):
                    if field == "gate_pass" and row.get("gate_id") in allowed_gate_pass:
                        continue
                    return False
    return True


def missing_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            text = " ".join(str(value) for value in row.values())
            if "MISSING_" in text and (
                boolish(row.get("score_ready", False))
                or boolish(row.get("valid_for_claim", False))
                or boolish(row.get("claim_allowed", False))
                or boolish(row.get("claim_allowed_now", False))
                or (boolish(row.get("gate_pass", False)) and row.get("gate_id") != "AC1825_0_oddness_attempt_written")
            ):
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    exists_ok = all(boolish(row["exists"]) for row in source_rows)
    needles_ok = all(boolish(row["needles_present"]) for row in source_rows)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1825_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1825_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1825_2_oddness_attempt_written",
            any(row["attempt_id"] == "SDO1825_0_target" and row["derivation_result"] == "TARGET_ATTEMPTED" for row in rows_map["oddness_theorem"]),
            "signed-deficit oddness theorem attempt is written",
        ),
        (
            "VAL1825_3_exact_math_nonclaim",
            any(row["attempt_id"] == "SDO1825_1_exact_math" and row["current_status"] == "MATH_OK_PARENT_PREMISE_UNSIGNED" for row in rows_map["oddness_theorem"]),
            "oddness math is exact but parent premise remains unsigned",
        ),
        (
            "VAL1825_4_theorem_not_promoted",
            any(row["attempt_id"] == "SDO1825_6_verdict" and row["derivation_result"] == "CONDITIONAL_THEOREM_NOT_CURRENT_PROOF" for row in rows_map["oddness_theorem"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["oddness_theorem"]),
            "1825 theorem is not promoted as current proof",
        ),
        (
            "VAL1825_5_owner_stack_blocked",
            any(row["owner_id"] == "OOA1825_4_verdict" and row["current_status"] == "FAIL_CURRENT_OWNER_STACK" for row in rows_map["orientation_owner_audit"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["orientation_owner_audit"]),
            "orientation/log-angle owner stack remains blocked",
        ),
        (
            "VAL1825_6_c2_prior_nonclaim",
            any(row["row_id"] == "C2P1825_4_total" and row["current_status"] == "MISSING_ZERO_OR_FINITE_PRIOR_ROW_NONCLAIM" for row in rows_map["c2_prior_row"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["c2_prior_row"]),
            "c2 prior rows are nonclaim",
        ),
        (
            "VAL1825_7_countermodels_retained",
            all(boolish(row["retained"]) and not boolish(row["valid_for_claim"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain retained",
        ),
        (
            "VAL1825_8_gr_newton_nonclaim",
            all(not boolish(row["claim_allowed_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["gr_newton_impact"]),
            "GR/Newton impact rows remain nonclaim",
        ),
        (
            "VAL1825_9_acceptance_blocks",
            any(row["gate_id"] == "AC1825_0_oddness_attempt_written" and boolish(row["gate_pass"]) and not boolish(row["claim_allowed"]) for row in rows_map["acceptance_gate"])
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["acceptance_gate"]),
            "acceptance gate permits contract-only progress and blocks claims",
        ),
        (
            "VAL1825_10_claim_gates_blocked",
            all(row["status"] in {"BLOCKED", "REFUSED"} and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all oddness/c2/local-GR claim gates remain blocked or refused",
        ),
        ("VAL1825_11_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1825_12_missing_not_ready", missing_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1825_13_decision_next",
            any(row["decision_id"] == "DEC1825_3_best_next" and row["decision"] == "LOG_HOLONOMY_ACTION_OWNER_OR_TRACE_NORM_C2_PRIOR_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects log-holonomy action owner next",
        ),
        (
            "VAL1825_14_next_selected",
            any(row["route_id"] == "NEXT1825_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1825_15_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1825 CSVs parse"),
        ("VAL1825_16_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1825_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1825_18_formalization_untouched", formalization_untouched(), "no 1825 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1825_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1825 signed-deficit oddness theorem or c2 prior row checkpoint",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1825 Y5 R2FR signed deficit oddness theorem or c2 prior row",
            "",
            "**Progress:** 1825 separates the clean mathematics from the missing physics. If the primitive deficit response is genuinely odd, `Phi''(0)=0` follows. But orientation by itself does not force oddness; trace, norm, entropy, and mismatch-energy actions remain even-cost countermodels.",
            "",
            "**Current verdict:** no zero claim yet. The best route is now precise: derive that the parent action owns signed log-holonomy/angle as a physical boundary-charge variable, not a gauge relabeling and not a trace/norm cost. Until then, `c2_visible` remains a nonclaim prior/source row.",
            "",
            "**Claim ceiling:** no signed-oddness claim, no `c2_visible=0` claim, no R2/fR score, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1825.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Signed Deficit Oddness Theorem Attempt",
            markdown_table(rows_map["oddness_theorem"], ["attempt_id", "claim_piece", "mathematical_statement", "derivation_result", "current_status", "consequence", "valid_for_claim"]),
            "",
            "## Orientation Owner Audit",
            markdown_table(rows_map["orientation_owner_audit"], ["owner_id", "needed_owner", "formal_condition", "current_status", "blocker", "valid_for_claim"]),
            "",
            "## C2 Prior Source Row",
            markdown_table(rows_map["c2_prior_row"], ["row_id", "row_type", "quantity", "formula_or_value", "required_inputs", "units", "source_path", "current_status", "score_ready", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel_ledger"], ["countermodel_id", "countermodel", "why_it_survives", "blocked_by", "retained", "valid_for_claim"]),
            "",
            "## GR Newton Impact Ledger",
            markdown_table(rows_map["gr_newton_impact"], ["impact_id", "if_closed", "would_buy", "still_missing", "claim_allowed_now", "valid_for_claim"]),
            "",
            "## Acceptance Gate",
            markdown_table(rows_map["acceptance_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "claim_allowed", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is exactly the kind of narrowing the local-GR route needs. We are no longer asking vaguely why R2 is absent. We now know the theorem target: MTS must own signed log-holonomy as an action variable. If it owns only trace/norm holonomy, the quadratic coefficient is real and must be carried into tests.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1825 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
