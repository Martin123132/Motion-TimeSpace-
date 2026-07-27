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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1823"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1823-Y5-R2FR-primitive-deficit-action-law-or-visible-c2-owner-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1823_0_1822_next",
        "source_key": "1822_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1822_NEXT_TARGET.csv",
        "needles": ["NEXT1822_0_primary", "selected"],
        "role": "1822 selects the primitive deficit action law as the next target.",
    },
    {
        "source_id": "SRC1823_1_1822_validation",
        "source_key": "1822_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1822_VALIDATION.csv",
        "needles": ["VAL1822_OVERALL", "PASS"],
        "role": "confirms 1822 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1823_2_1822_linearity",
        "source_key": "1822_linearity_attempt",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1822_LINEAR_HOLONOMY_PARENT_AXIOM_ATTEMPT.csv",
        "needles": ["LHA1822_4_deficit_action_law", "DEFICIT_LINEAR_COST_NOT_DERIVED"],
        "role": "deficit-linearity is the best remaining parent proof route.",
    },
    {
        "source_id": "SRC1823_3_1822_owner",
        "source_key": "1822_coefficient_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1822_R2FR_COEFFICIENT_OWNER_ROW.csv",
        "needles": ["CO1822_1_visible_c2", "MISSING_PARENT_INPUT"],
        "role": "visible quadratic curvature response coefficient is missing and nonclaim.",
    },
    {
        "source_id": "SRC1823_4_1822_loopholes",
        "source_key": "1822_additivity_loopholes",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1822_ADDITIVITY_LOOPHOLE_AUDIT.csv",
        "needles": ["ALO1822_5_verdict", "FAIL_CURRENT_LINEARITY_PROOF"],
        "role": "additivity loopholes remain explicit.",
    },
    {
        "source_id": "SRC1823_5_962_zero",
        "source_key": "962_relative_zero",
        "source_path": RESIDUALS / "P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv",
        "needles": ["R2Z962_5_relative_zero_theorem", "RELATIVE_THEOREM_PROVEN_PARENT_PREMISE_UNSIGNED"],
        "role": "R2/fR zero theorem is relative and needs a parent activator.",
    },
    {
        "source_id": "SRC1823_6_963_owner",
        "source_key": "963_coefficient_owner",
        "source_path": RESIDUALS / "P8_Y5_R10_963_R2FR_COEFFICIENT_OWNER_AUDIT.csv",
        "needles": ["CO963_4_verdict", "NO_EXECUTABLE_OWNER_FOUND"],
        "role": "older coefficient-owner audit found no executable owner.",
    },
    {
        "source_id": "SRC1823_7_440_reduction",
        "source_key": "440_sector_reduction",
        "source_path": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
        "needles": ["R2_fR_scalar_mode", "retained_R11_plus_R10_if_finite_range"],
        "role": "R2/fR is retained unless zeroed or coefficient-mapped.",
    },
    {
        "source_id": "SRC1823_8_110_endpoint",
        "source_key": "110_endpoint_target",
        "source_path": ROOT / "110-endpoint-charge-equation-attempt.md",
        "needles": ["endpoint_quadratic_target_found_not_derived", "spatial-cell endpoint quadratic"],
        "role": "endpoint/cell intuition exists but was not parent-action derived.",
    },
    {
        "source_id": "SRC1823_9_111_variational",
        "source_key": "111_endpoint_owner",
        "source_path": ROOT / "111-endpoint-quadratic-variational-owner-attempt.md",
        "needles": ["variational_owner_written_but_not_parent_derived", "constraint_trick_rejected"],
        "role": "a writeable variational owner exists, but coefficient/arrow derivation failed.",
    },
]


OUTPUTS: dict[str, Path] = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1823_SOURCE_REGISTER.csv",
    "deficit_action_law": RESIDUALS / "P8_Y5_PARENT_QLOC_1823_PRIMITIVE_DEFICIT_ACTION_LAW_ATTEMPT.csv",
    "continuum_scaling": RESIDUALS / "P8_Y5_PARENT_QLOC_1823_DEFICIT_CONTINUUM_SCALING_AUDIT.csv",
    "visible_c2_owner": RESIDUALS / "P8_Y5_PARENT_QLOC_1823_VISIBLE_C2_OWNER_ROW.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1823_COUNTERMODEL_LEDGER.csv",
    "gr_newton_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1823_GR_NEWTON_IMPACT_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1823_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1823_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1823_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1823_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1823_VALIDATION.csv",
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


def deficit_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DAL1823_0_target",
            "claim_piece": "primitive deficit action law",
            "mathematical_statement": "For each primitive local cell/hinge, the gravitational action cost is proportional to area times holonomy deficit, S_h = k1 A_h delta_h + Lambda V_h + boundary, not a generic Phi(delta_h).",
            "derivation_result": "TARGET_ATTEMPTED",
            "current_status": "NOT_PARENT_PROVEN",
            "consequence": "without this law, visible c2 or hidden quadratic response remains legal",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DAL1823_1_Regge_EH_bridge",
            "claim_piece": "linear deficit gives EH-like continuum",
            "mathematical_statement": "A Regge-like sum over A_h delta_h converges to the integral of sqrt(-g) R up to conventional constants and boundary terms under the correct continuum/triangulation assumptions.",
            "derivation_result": "KNOWN_CONDITIONAL_BRIDGE_SHAPE",
            "current_status": "MTS_PRIMITIVE_ACTION_LAW_UNSIGNED",
            "consequence": "good bridge if MTS derives linear deficit cost, but not proof by itself",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DAL1823_2_generic_deficit_cost",
            "claim_piece": "generic primitive cost",
            "mathematical_statement": "If S_h = A_h Phi(delta_h) and Phi(delta)=k1 delta + c2 delta^2 + O(delta^3), then c2 is a visible quadratic response coefficient unless Phi''(0)=0 is parent-derived.",
            "derivation_result": "EXACT_LOCAL_EXPANSION",
            "current_status": "C2_NOT_ZEROED",
            "consequence": "visible c2 owner row is mandatory",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DAL1823_3_endpoint_cell_warning",
            "claim_piece": "endpoint/cell potentials do not prove deficit linearity",
            "mathematical_statement": "The endpoint quadratic/cubic potential work can suggest cell stationarity, but a written potential or endpoint equation is not a derivation of the gravitational deficit action law.",
            "derivation_result": "GUARDRAIL_FROM_110_111",
            "current_status": "DO_NOT_IMPORT_ENDPOINT_AS_PROOF",
            "consequence": "endpoint route remains suggestive only unless parent action derives coefficients",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DAL1823_4_no_square_principle",
            "claim_piece": "why not deficit squared",
            "mathematical_statement": "To kill R2/fR, MTS must prove the primitive action measures oriented holonomy/deficit first moment rather than strain energy, variance, entropy, or squared mismatch.",
            "derivation_result": "KEY_MISSING_PRINCIPLE",
            "current_status": "NOT_DERIVED",
            "consequence": "delta^2 response remains a live countermodel",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "DAL1823_5_verdict",
            "claim_piece": "1823 proves primitive deficit action law",
            "mathematical_statement": "1823 identifies the exact law that would make EH natural, but current sources do not derive why the primitive action is linear in deficit rather than a generic Phi(delta).",
            "derivation_result": "CONDITIONAL_BRIDGE_NOT_CURRENT_PROOF",
            "current_status": "DEMOTE_TO_VISIBLE_C2_OWNER_ROW",
            "consequence": "R2/fR remains explicit coefficient-owner debt",
            "valid_for_claim": False,
        },
    ]


def continuum_scaling_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "scaling_id": "DCS1823_0_linear",
            "term": "A_h delta_h",
            "cell_scaling": "A_h ~ ell^2, delta_h ~ R ell^2, so A_h delta_h ~ R ell^4",
            "continuum_effect": "sum over cells gives integral sqrt(-g) R",
            "status": "EH_BRIDGE_CONDITIONAL",
            "needed_input": "parent-derived k1 and continuum/measure convention",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "scaling_id": "DCS1823_1_quadratic",
            "term": "A_h delta_h^2",
            "cell_scaling": "A_h delta_h^2 ~ R^2 ell^6",
            "continuum_effect": "sum gives shape_factor * c2 * ell^2 integral sqrt(-g) R^2 unless coefficient scaling removes or enhances it",
            "status": "VISIBLE_C2_ROUTE",
            "needed_input": "cell scale ell_cell, shape factor, c2 normalization and continuum limit rule",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "scaling_id": "DCS1823_2_zero_limit",
            "term": "quadratic term in strict ell -> 0 limit",
            "cell_scaling": "if c2 fixed and ell_cell -> 0, R2 coefficient may vanish as ell_cell^2",
            "continuum_effect": "suppression, not theorem-zero, unless parent proves the limit and no renormalized residue",
            "status": "SUPPRESSION_ROUTE_NOT_ZERO_PROOF",
            "needed_input": "actual cell scale/continuum limit and radiative/effective closure",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "scaling_id": "DCS1823_3_renormalized",
            "term": "effective R2 residue after reduction",
            "cell_scaling": "hidden fields/readout/loops can leave finite c_R2_eff independent of bare ell^2 suppression",
            "continuum_effect": "R2/fR remains an R11/R10 scalar-mode branch",
            "status": "NOT_FORBIDDEN",
            "needed_input": "no-hidden-tower theorem or finite coefficient row",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def visible_c2_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "owner_id": "VC21823_0_zero_owner",
            "quantity": "Phi_double_prime_0_or_c2",
            "candidate_owner": "primitive linear deficit law",
            "formula_or_value": "0 only if Phi(delta)=k1 delta + constant is parent-derived",
            "required_inputs": "parent action law; orientation/first-moment principle; no deficit-squared cost",
            "units": "dimensionless_deficit_response",
            "current_status": "ZERO_OWNER_UNSIGNED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "VC21823_1_visible_c2",
            "quantity": "c2_visible",
            "candidate_owner": "visible primitive deficit-squared response",
            "formula_or_value": "c2_visible = 1/2 Phi''(0)",
            "required_inputs": "Phi(delta) expansion from parent action; sign; normalization; source path",
            "units": "dimensionless_deficit_response",
            "current_status": "MISSING_PARENT_INPUT",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "VC21823_2_map_to_R2",
            "quantity": "c_R2_eff",
            "candidate_owner": "continuum map of visible c2",
            "formula_or_value": "c_R2_eff ~ shape_factor * c2_visible * ell_cell^2 after EH normalization",
            "required_inputs": "ell_cell; shape factor; EH normalization; continuum limit; units",
            "units": "length_squared_after_EH_normalization",
            "current_status": "MISSING_CELL_SCALE_AND_SHAPE_FACTOR",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "VC21823_3_scalaron_map",
            "quantity": "lambda_s_alpha_s",
            "candidate_owner": "finite R2/fR scalar-mode map",
            "formula_or_value": "lambda_s=sqrt(6 c_R2_eff); alpha_s=1/3 only for simple unscreened metric f(R)",
            "required_inputs": "positive c_R2_eff; matter coupling; screening; source/readout map",
            "units": "meters_and_dimensionless",
            "current_status": "MISSING_COEFFICIENT_AND_COUPLING",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "VC21823_4_verdict",
            "quantity": "visible_c2_owner_row",
            "candidate_owner": "current corpus",
            "formula_or_value": "no executable visible c2 owner or zero theorem exists yet",
            "required_inputs": "prove primitive linear deficit law or source visible c2 and continuum map",
            "units": "row_contract",
            "current_status": "NO_EXECUTABLE_OWNER_FOUND_CURRENT_1823",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1823_0_deficit_squared",
            "countermodel": "primitive action includes A_h delta_h^2",
            "why_it_survives": "nothing in current corpus forbids squared deficit cost",
            "blocked_by": "parent-derived linear deficit law or finite c2 bound",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1823_1_endpoint_potential_import",
            "countermodel": "use endpoint quadratic/cubic potential as if it derived the local gravitational action",
            "why_it_survives": "110/111 explicitly mark endpoint coefficients/action owner as not derived",
            "blocked_by": "actual parent action coefficient derivation",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1823_2_cell_suppression_not_zero",
            "countermodel": "quadratic term is small because ell_cell is tiny but not zero",
            "why_it_survives": "suppression can help empirically but does not derive GR exactly",
            "blocked_by": "zero theorem or sourced bound below local tolerances",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1823_3_renormalized_R2",
            "countermodel": "effective reduction leaves a finite R2/fR coefficient",
            "why_it_survives": "hidden-tower and readout closure are not signed",
            "blocked_by": "no-integrated-tower theorem or explicit coefficient owner",
            "retained": True,
            "valid_for_claim": False,
        },
    ]


def gr_newton_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1823_0_if_linear_deficit_closes",
            "if_closed": "S_h = k1 A_h delta_h + Lambda V_h is parent-derived with no c2 channel",
            "would_buy": "a concrete path from primitive MTS cells to EH/linear curvature, reducing GR import risk",
            "still_missing": "Levi-Civita/connection, source charge, C_extra/projector/boundary and Newton calibration",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1823_1_if_visible_c2_filled",
            "if_closed": "visible c2 and c_R2_eff map are source-backed",
            "would_buy": "finite scalar-mode branch becomes quantitatively testable instead of vague",
            "still_missing": "full R10 curve, PPN map, matter coupling and normalizer",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1823_2_verdict",
            "if_closed": "1823 alone proves local GR/Newton",
            "would_buy": "nothing claimable alone; current 1823 does not close its own deficit law",
            "still_missing": "R2/fR zero or bound plus broader local-GR bridge",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1823_0_deficit_contract_written",
            "gate": "primitive deficit action law attempt written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "1823 identifies the exact linear-vs-squared deficit hinge and the visible c2 fallback",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1823_1_linear_deficit_signed",
            "gate": "parent action cost is linear in deficit",
            "current_status": "BLOCKED",
            "reason": "no current source derives why Phi''(0)=0",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1823_2_visible_c2_sourced",
            "gate": "visible c2 owner row source-backed",
            "current_status": "BLOCKED",
            "reason": "Phi(delta), ell_cell, shape factor and continuum map are missing",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1823_3_local_GR",
            "gate": "local GR/Newton promotion allowed",
            "current_status": "REFUSED",
            "reason": "deficit law is unsigned and broader GR/Newton gates remain open",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1823_0_linear_deficit",
            "claim": "primitive deficit action is linear",
            "status": "BLOCKED",
            "reason": "current MTS evidence does not derive Phi''(0)=0",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1823_1_R2FR_zero",
            "claim": "visible c2/R2/fR branch is theorem-zero",
            "status": "BLOCKED",
            "reason": "zero owner remains unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1823_2_scalar_score",
            "claim": "finite scalaron branch can be scored",
            "status": "REFUSED",
            "reason": "visible c2, cell scale, c_R2 map and response data are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1823_3_local_GR",
            "claim": "local GR/Newton follows",
            "status": "REFUSED",
            "reason": "one operator subgate remains unresolved and other local bridge gates are still open",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1823_0_deficit_result",
            "decision": "PRIMITIVE_DEFICIT_LINEARITY_NOT_PROVEN",
            "reason": "the Regge/EH bridge is strong if linear deficit cost is owned, but current MTS does not derive why the primitive cost lacks a squared deficit term",
            "next_action": "do not zero R2/fR from deficit intuition alone",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1823_1_real_gain",
            "decision": "VISIBLE_C2_MAP_EXPOSED",
            "reason": "the first visible coefficient debt is now c2_visible = 1/2 Phi''(0), mapping to c_R2_eff roughly through ell_cell^2",
            "next_action": "derive Phi''(0)=0 or source c2_visible and ell_cell/shape factor",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1823_2_endpoint_guard",
            "decision": "ENDPOINT_WORK_REMAINS_SUGGESTIVE_NOT_PROOF",
            "reason": "110/111 can guide the cell-action search but cannot be used as a parent action derivation",
            "next_action": "keep endpoint coefficients out of claim rows unless parent-owned",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1823_3_best_next",
            "decision": "PHI_SECOND_DERIVATIVE_ZERO_OR_VISIBLE_C2_SOURCE_NEXT",
            "reason": "the next exact hinge is whether the primitive response function Phi(delta) has Phi''(0)=0 by theorem or a finite sourced value",
            "next_action": "1824-Y5-R2FR-Phi-second-derivative-zero-or-visible-c2-source-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1823_0_primary",
            "next_target": "1824-Y5-R2FR-Phi-second-derivative-zero-or-visible-c2-source-row.md",
            "script": "scripts/Y5_R2FR_Phi_second_derivative_zero_or_visible_c2_source_row.py",
            "objective": "try to derive Phi''(0)=0 for the primitive deficit response; if not, source or quarantine visible c2 with units, cell scale, and continuum map",
            "selection_status": "selected",
            "success_condition": "Phi''(0) zero theorem signed, or visible c2 source row remains valid_for_claim=false with all missing inputs explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1823_1_parallel",
            "next_target": "1824b-Y5-R2FR-cell-scale-and-shape-factor-bound-row.md",
            "script": "scripts/Y5_R2FR_cell_scale_and_shape_factor_bound_row.py",
            "objective": "if visible c2 survives, derive or source ell_cell and shape_factor for c_R2_eff mapping",
            "selection_status": "held_parallel",
            "success_condition": "cell-scale map parses but remains nonclaim until c2 and response data exist",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "deficit_action_law": deficit_action_rows(),
        "continuum_scaling": continuum_scaling_rows(),
        "visible_c2_owner": visible_c2_rows(),
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
    allowed_gate_pass = {"AC1823_0_deficit_contract_written"}
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
                or (boolish(row.get("gate_pass", False)) and row.get("gate_id") != "AC1823_0_deficit_contract_written")
            ):
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    exists_ok = all(boolish(row["exists"]) for row in source_rows)
    needles_ok = all(boolish(row["needles_present"]) for row in source_rows)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1823_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1823_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1823_2_deficit_attempt_written",
            any(row["attempt_id"] == "DAL1823_0_target" and row["derivation_result"] == "TARGET_ATTEMPTED" for row in rows_map["deficit_action_law"]),
            "primitive deficit action law attempt is written",
        ),
        (
            "VAL1823_3_generic_cost_exposes_c2",
            any(row["attempt_id"] == "DAL1823_2_generic_deficit_cost" and row["current_status"] == "C2_NOT_ZEROED" for row in rows_map["deficit_action_law"]),
            "generic deficit cost exposes visible c2 coefficient",
        ),
        (
            "VAL1823_4_theorem_not_promoted",
            any(row["attempt_id"] == "DAL1823_5_verdict" and row["derivation_result"] == "CONDITIONAL_BRIDGE_NOT_CURRENT_PROOF" for row in rows_map["deficit_action_law"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["deficit_action_law"]),
            "1823 theorem is not promoted as current proof",
        ),
        (
            "VAL1823_5_scaling_nonclaim",
            any(row["scaling_id"] == "DCS1823_1_quadratic" and row["status"] == "VISIBLE_C2_ROUTE" for row in rows_map["continuum_scaling"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["continuum_scaling"]),
            "continuum scaling rows remain nonclaim",
        ),
        (
            "VAL1823_6_visible_c2_nonclaim",
            any(row["owner_id"] == "VC21823_4_verdict" and row["current_status"] == "NO_EXECUTABLE_OWNER_FOUND_CURRENT_1823" for row in rows_map["visible_c2_owner"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["visible_c2_owner"]),
            "visible c2 owner rows are schema-only and nonclaim",
        ),
        (
            "VAL1823_7_countermodels_retained",
            all(boolish(row["retained"]) and not boolish(row["valid_for_claim"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain retained",
        ),
        (
            "VAL1823_8_gr_newton_nonclaim",
            all(not boolish(row["claim_allowed_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["gr_newton_impact"]),
            "GR/Newton impact rows remain nonclaim",
        ),
        (
            "VAL1823_9_acceptance_blocks",
            any(row["gate_id"] == "AC1823_0_deficit_contract_written" and boolish(row["gate_pass"]) and not boolish(row["claim_allowed"]) for row in rows_map["acceptance_gate"])
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["acceptance_gate"]),
            "acceptance gate permits contract-only progress and blocks claims",
        ),
        (
            "VAL1823_10_claim_gates_blocked",
            all(row["status"] in {"BLOCKED", "REFUSED"} and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all deficit/R2FR/local-GR claim gates remain blocked or refused",
        ),
        ("VAL1823_11_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1823_12_missing_not_ready", missing_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1823_13_decision_next",
            any(row["decision_id"] == "DEC1823_3_best_next" and row["decision"] == "PHI_SECOND_DERIVATIVE_ZERO_OR_VISIBLE_C2_SOURCE_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects Phi second-derivative zero or c2 source next",
        ),
        (
            "VAL1823_14_next_selected",
            any(row["route_id"] == "NEXT1823_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1823_15_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1823 CSVs parse"),
        ("VAL1823_16_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1823_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1823_18_formalization_untouched", formalization_untouched(), "no 1823 outputs found under formalization-workbench"),
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
            "check_id": "VAL1823_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1823 primitive deficit action law or visible c2 owner row checkpoint",
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
            "# 1823 Y5 R2FR primitive deficit action law or visible c2 owner row",
            "",
            "**Progress:** 1823 makes the EH bridge more concrete. A linear `area * deficit` primitive cell action is the clean route toward EH/Regge-like curvature. But a generic primitive cost `area * Phi(deficit)` immediately exposes a visible quadratic coefficient `c2 = Phi''(0)/2`.",
            "",
            "**Current verdict:** the bridge is promising but not derived. Current MTS sources do not prove why the primitive action is linear in deficit rather than deficit-squared. Therefore `c2_visible` becomes the first explicit visible coefficient-owner debt for the R2/fR scalar-mode branch.",
            "",
            "**Claim ceiling:** no primitive deficit-law claim, no R2/fR zero claim, no finite scalaron score, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1823.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Primitive Deficit Action Law Attempt",
            markdown_table(rows_map["deficit_action_law"], ["attempt_id", "claim_piece", "mathematical_statement", "derivation_result", "current_status", "consequence", "valid_for_claim"]),
            "",
            "## Deficit Continuum Scaling Audit",
            markdown_table(rows_map["continuum_scaling"], ["scaling_id", "term", "cell_scaling", "continuum_effect", "status", "needed_input", "score_ready", "valid_for_claim"]),
            "",
            "## Visible C2 Owner Row",
            markdown_table(rows_map["visible_c2_owner"], ["owner_id", "quantity", "candidate_owner", "formula_or_value", "required_inputs", "units", "current_status", "score_ready", "valid_for_claim"]),
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
            "This is a genuinely useful tightening. The GR route is no longer just 'make it second order'; it is now 'derive why the primitive cell action is first-order in holonomy deficit'. If that derivation lands, EH becomes much less imported. If it does not, the theory can still proceed, but `c2_visible` must be sourced, bounded, and carried into the R2/fR scalar-mode tests.",
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
    print(f"1823 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
