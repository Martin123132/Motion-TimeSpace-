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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1824"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1824-Y5-R2FR-Phi-second-derivative-zero-or-visible-c2-source-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1824_0_1823_next",
        "source_key": "1823_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1823_NEXT_TARGET.csv",
        "needles": ["NEXT1823_0_primary", "selected"],
        "role": "1823 selects Phi second derivative zero or visible c2 source as the next target.",
    },
    {
        "source_id": "SRC1824_1_1823_validation",
        "source_key": "1823_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1823_VALIDATION.csv",
        "needles": ["VAL1823_OVERALL", "PASS"],
        "role": "confirms 1823 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1824_2_1823_deficit",
        "source_key": "1823_deficit_attempt",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1823_PRIMITIVE_DEFICIT_ACTION_LAW_ATTEMPT.csv",
        "needles": ["DAL1823_2_generic_deficit_cost", "C2_NOT_ZEROED"],
        "role": "generic deficit cost exposes c2 unless Phi''(0)=0 is derived.",
    },
    {
        "source_id": "SRC1824_3_1823_visible_c2",
        "source_key": "1823_visible_c2",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1823_VISIBLE_C2_OWNER_ROW.csv",
        "needles": ["VC21823_1_visible_c2", "MISSING_PARENT_INPUT"],
        "role": "visible c2 coefficient is missing and nonclaim.",
    },
    {
        "source_id": "SRC1824_4_1823_scaling",
        "source_key": "1823_scaling",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1823_DEFICIT_CONTINUUM_SCALING_AUDIT.csv",
        "needles": ["DCS1823_1_quadratic", "VISIBLE_C2_ROUTE"],
        "role": "quadratic deficit maps to an R2-like continuum route.",
    },
    {
        "source_id": "SRC1824_5_1822_linearity",
        "source_key": "1822_linearity",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1822_LINEAR_HOLONOMY_PARENT_AXIOM_ATTEMPT.csv",
        "needles": ["LHA1822_2_same_cell_additivity", "PREMISE_NOT_DERIVED_FROM_MTS"],
        "role": "same-cell response linearity remains a conditional lemma only.",
    },
    {
        "source_id": "SRC1824_6_962_zero",
        "source_key": "962_relative_zero",
        "source_path": RESIDUALS / "P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv",
        "needles": ["R2Z962_5_relative_zero_theorem", "RELATIVE_THEOREM_PROVEN_PARENT_PREMISE_UNSIGNED"],
        "role": "R2/fR zero theorem remains relative to unsigned parent premises.",
    },
    {
        "source_id": "SRC1824_7_111_endpoint",
        "source_key": "111_endpoint_owner",
        "source_path": ROOT / "111-endpoint-quadratic-variational-owner-attempt.md",
        "needles": ["variational_owner_written_but_not_parent_derived", "constraint_trick_rejected"],
        "role": "endpoint variational owner remains suggestive but not parent-derived.",
    },
]


OUTPUTS: dict[str, Path] = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1824_SOURCE_REGISTER.csv",
    "phi_zero_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1824_PHI_SECOND_DERIVATIVE_ZERO_THEOREM_ATTEMPT.csv",
    "symmetry_route_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1824_SIGNED_DEFICIT_SYMMETRY_ROUTE_AUDIT.csv",
    "visible_c2_source_row": RESIDUALS / "P8_Y5_PARENT_QLOC_1824_VISIBLE_C2_SOURCE_ROW.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1824_COUNTERMODEL_LEDGER.csv",
    "gr_newton_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1824_GR_NEWTON_IMPACT_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1824_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1824_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1824_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1824_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1824_VALIDATION.csv",
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


def phi_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PZ1824_0_target",
            "claim_piece": "derive Phi''(0)=0",
            "mathematical_statement": "For primitive deficit response Phi(delta)=k1 delta + c2 delta^2 + ..., prove Phi''(0)=0 so c2_visible=0.",
            "derivation_result": "TARGET_ATTEMPTED",
            "current_status": "NOT_PARENT_PROVEN",
            "consequence": "visible c2 remains live unless a symmetry or source row closes it",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PZ1824_1_signed_oddness",
            "claim_piece": "signed-deficit oddness",
            "mathematical_statement": "If delta is an oriented signed deficit and the primitive action is a signed holonomy charge with Phi(-delta)=-Phi(delta), then every even Taylor coefficient vanishes and Phi''(0)=0.",
            "derivation_result": "EXACT_CONDITIONAL_LEMMA",
            "current_status": "ODDNESS_NOT_PARENT_DERIVED",
            "consequence": "would kill the visible delta^2/R2 coefficient if parent-signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PZ1824_2_odd_not_full_EH",
            "claim_piece": "oddness is not full linearity",
            "mathematical_statement": "Phi odd still permits delta^3, delta^5, and other nonlinear odd terms; this can remove c2 around zero but does not by itself prove the full EH-only operator for arbitrary curvature.",
            "derivation_result": "LIMITATION_IDENTIFIED",
            "current_status": "NEEDS_HIGHER_ODD_TERM_GATE",
            "consequence": "R2/fR quadratic wound can close before all higher-curvature wounds close",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PZ1824_3_trace_norm_warning",
            "claim_piece": "trace/norm costs are dangerous",
            "mathematical_statement": "If the primitive action uses a holonomy trace, norm, entropy, mismatch energy, or 1-cos(delta)-type cost, the first nonzero term can be quadratic and Phi''(0) is generically nonzero.",
            "derivation_result": "COUNTERMODEL_LIVE",
            "current_status": "NO_SIGNED_CHARGE_OWNER",
            "consequence": "visible c2 source row remains required",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PZ1824_4_log_angle_route",
            "claim_piece": "log-holonomy/angle route",
            "mathematical_statement": "Using the signed logarithm/angle of small holonomy can define an oriented first-moment deficit response, but MTS must derive why this is the action variable rather than trace or norm.",
            "derivation_result": "BEST_ZERO_ROUTE",
            "current_status": "ACTION_VARIABLE_NOT_PARENT_SIGNED",
            "consequence": "selects the next theorem target",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PZ1824_5_verdict",
            "claim_piece": "1824 proves Phi''(0)=0",
            "mathematical_statement": "The oddness lemma is exact, but current MTS sources do not prove signed-deficit oddness or log-angle action ownership.",
            "derivation_result": "CONDITIONAL_ZERO_LEMMA_NOT_CURRENT_PROOF",
            "current_status": "DEMOTE_TO_VISIBLE_C2_SOURCE_ROW",
            "consequence": "visible c2 remains explicit nonclaim debt",
            "valid_for_claim": False,
        },
    ]


def symmetry_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "SDA1824_0_orientation",
            "needed_clause": "delta is a signed oriented deficit, not an unsigned magnitude",
            "formal_condition": "orientation reversal maps delta -> -delta",
            "why_it_matters": "only signed variables can support an odd action response",
            "current_status": "CANDIDATE_NOT_PARENT_CERTIFIED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "SDA1824_1_odd_action",
            "needed_clause": "primitive action is odd under signed deficit reversal",
            "formal_condition": "Phi(-delta)=-Phi(delta)",
            "why_it_matters": "forces Phi''(0)=0 and kills the visible c2 coefficient",
            "current_status": "NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "SDA1824_2_not_norm",
            "needed_clause": "parent action is not a norm/energy/entropy of holonomy mismatch",
            "formal_condition": "Phi(delta) is not |delta|^2, 1-cos(delta), Tr(I-U), or other even cost",
            "why_it_matters": "these routes generate c2 immediately",
            "current_status": "NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "SDA1824_3_log_angle_owner",
            "needed_clause": "parent action owns signed log-holonomy/angle as the primitive variable",
            "formal_condition": "Phi depends on log(U) or signed deficit first moment, not only on class trace",
            "why_it_matters": "this is the cleanest route to an odd first-response law",
            "current_status": "BEST_NEXT_TARGET",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "SDA1824_4_higher_odd_guard",
            "needed_clause": "higher odd nonlinearities are absent, suppressed, topological, or bounded",
            "formal_condition": "Phi'''(0), Phi^(5)(0), ... controlled if local EH beyond quadratic is claimed",
            "why_it_matters": "c2 zero is not full EH selection",
            "current_status": "FUTURE_OPERATOR_GATE",
            "valid_for_claim": False,
        },
    ]


def visible_c2_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "C2S1824_0_zero_if_odd",
            "row_type": "conditional_zero_switch",
            "quantity": "c2_visible",
            "formula_or_value": "0 if signed-deficit oddness and log-angle action owner are parent-signed",
            "required_inputs": "orientation certificate; Phi(-delta)=-Phi(delta); not norm/trace cost; source path",
            "units": "dimensionless_deficit_response",
            "source_path": "",
            "current_status": "ZERO_THEOREM_UNSIGNED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "C2S1824_1_visible_value",
            "row_type": "finite_visible_c2",
            "quantity": "c2_visible",
            "formula_or_value": "c2_visible=1/2 Phi''(0)",
            "required_inputs": "Phi(delta) parent expansion; sign; normalization; uncertainty/prior; source path",
            "units": "dimensionless_deficit_response",
            "source_path": "",
            "current_status": "MISSING_PARENT_INPUT",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "C2S1824_2_R2_map",
            "row_type": "continuum_map",
            "quantity": "c_R2_eff",
            "formula_or_value": "c_R2_eff ~ shape_factor * c2_visible * ell_cell^2 after EH normalization",
            "required_inputs": "ell_cell; shape_factor; EH normalization; continuum limit; source path",
            "units": "length_squared_after_EH_normalization",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1823_DEFICIT_CONTINUUM_SCALING_AUDIT.csv"),
            "current_status": "MISSING_CELL_SCALE_AND_SHAPE_FACTOR",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "C2S1824_3_total",
            "row_type": "visible_c2_source_contract",
            "quantity": "visible_c2_to_R2FR_scalar_mode",
            "formula_or_value": "valid only if zero theorem or c2 value plus c_R2_eff/lambda/alpha/normalizer maps exist",
            "required_inputs": "C2S1824_0 or C2S1824_1 plus C2S1824_2 and weak-field response maps",
            "units": "row_contract",
            "source_path": "",
            "current_status": "MISSING_ZERO_OR_FINITE_SOURCE_ROW_NONCLAIM",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1824_0_squared_norm",
            "countermodel": "primitive action is a squared holonomy mismatch or strain energy",
            "why_it_survives": "no parent theorem says the action is a signed first-moment charge",
            "blocked_by": "signed-deficit oddness/log-angle action theorem or finite c2 row",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1824_1_trace_cost",
            "countermodel": "action uses trace/class function such as 1-cos(delta)",
            "why_it_survives": "trace holonomy is gauge-natural and even in small angle",
            "blocked_by": "parent selects signed log-holonomy rather than trace/norm",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1824_2_odd_but_cubic",
            "countermodel": "Phi is odd but contains delta^3",
            "why_it_survives": "oddness kills c2 but not all higher-curvature nonlinearities",
            "blocked_by": "higher-odd-term theorem or finite higher-operator rows",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1824_3_endpoint_import",
            "countermodel": "endpoint variational potential is treated as parent proof of Phi oddness",
            "why_it_survives": "111 marks variational owner written but not parent-derived",
            "blocked_by": "actual parent action derivation",
            "retained": True,
            "valid_for_claim": False,
        },
    ]


def gr_newton_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1824_0_if_oddness_closes",
            "if_closed": "signed-deficit oddness and log-angle action owner are parent-derived",
            "would_buy": "visible c2/R2 coefficient is zero by theorem, one major scalar-mode wound closes",
            "still_missing": "higher odd nonlinearities, hidden tower, connection/source/C-term gates",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1824_1_if_c2_sourced",
            "if_closed": "finite c2_visible and c_R2_eff map are source-backed",
            "would_buy": "R2/fR scalar branch becomes quantitatively bounded/testable",
            "still_missing": "cell scale, full R10/PPN response, matter coupling and normalizer",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1824_2_verdict",
            "if_closed": "1824 alone proves local GR/Newton",
            "would_buy": "nothing claimable alone; 1824 only targets the visible quadratic deficit response",
            "still_missing": "broader EH/GR/Newton bridge remains open",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1824_0_phi_attempt_written",
            "gate": "Phi''(0) zero attempt written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "1824 identifies signed-deficit oddness as an exact conditional zero route",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1824_1_oddness_signed",
            "gate": "signed-deficit oddness parent-derived",
            "current_status": "BLOCKED",
            "reason": "no parent source proves Phi(-delta)=-Phi(delta)",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1824_2_not_norm_trace",
            "gate": "norm/trace cost excluded",
            "current_status": "BLOCKED",
            "reason": "squared/norm/trace holonomy actions remain live countermodels",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1824_3_c2_source",
            "gate": "finite c2 source row filled",
            "current_status": "BLOCKED",
            "reason": "Phi expansion, c2 value, cell scale and response maps are missing",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1824_0_Phi_second_zero",
            "claim": "Phi''(0)=0 is derived",
            "status": "BLOCKED",
            "reason": "oddness/log-angle owner is unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1824_1_R2FR_zero",
            "claim": "R2/fR scalar branch is theorem-zero",
            "status": "BLOCKED",
            "reason": "visible c2 is not zeroed and hidden/higher terms remain",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1824_2_finite_score",
            "claim": "finite R2/fR branch can be scored",
            "status": "REFUSED",
            "reason": "c2 value, c_R2 map and response data are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1824_3_local_GR",
            "claim": "local GR/Newton follows",
            "status": "REFUSED",
            "reason": "1824 is one operator subgate and remains open",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1824_0_phi_result",
            "decision": "PHI_SECOND_DERIVATIVE_ZERO_NOT_PROVEN",
            "reason": "signed-deficit oddness would zero c2, but current corpus does not derive oddness or log-angle action ownership",
            "next_action": "do not set c2_visible to zero yet",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1824_1_best_route",
            "decision": "SIGNED_DEFICIT_ODDNESS_NEXT",
            "reason": "this is the cleanest theorem route for the visible c2 coefficient: prove the action is an oriented signed charge, not a norm",
            "next_action": "attempt signed-deficit oddness parent theorem",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1824_2_fallback",
            "decision": "VISIBLE_C2_SOURCE_ROW_READY_NONCLAIM",
            "reason": "if oddness fails, c2_visible must be sourced with Phi expansion, cell scale and continuum map",
            "next_action": "keep finite c2 invalid for claim until sourced",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1824_3_best_next",
            "decision": "SIGNED_DEFICIT_ODDNESS_THEOREM_OR_C2_PRIOR_NEXT",
            "reason": "1824 reduces the issue to one exact symmetry question: is the primitive deficit action odd under delta reversal?",
            "next_action": "1825-Y5-R2FR-signed-deficit-oddness-theorem-or-c2-prior-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1824_0_primary",
            "next_target": "1825-Y5-R2FR-signed-deficit-oddness-theorem-or-c2-prior-row.md",
            "script": "scripts/Y5_R2FR_signed_deficit_oddness_theorem_or_c2_prior_row.py",
            "objective": "derive whether primitive deficit action is odd under signed deficit reversal; if not, create a c2 prior/source row without claiming a pass",
            "selection_status": "selected",
            "success_condition": "oddness theorem signed, or c2 prior/source row remains valid_for_claim=false with all missing inputs explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1824_1_parallel",
            "next_target": "1825b-Y5-R2FR-higher-odd-curvature-term-gate.md",
            "script": "scripts/Y5_R2FR_higher_odd_curvature_term_gate.py",
            "objective": "if c2 is zeroed by oddness, audit cubic and higher odd terms before any full EH claim",
            "selection_status": "held_parallel",
            "success_condition": "higher odd terms are theorem-zero, bounded, or retained as nonclaim operator rows",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "phi_zero_theorem": phi_zero_rows(),
        "symmetry_route_audit": symmetry_route_rows(),
        "visible_c2_source_row": visible_c2_rows(),
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
    allowed_gate_pass = {"AC1824_0_phi_attempt_written"}
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
                or (boolish(row.get("gate_pass", False)) and row.get("gate_id") != "AC1824_0_phi_attempt_written")
            ):
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    exists_ok = all(boolish(row["exists"]) for row in source_rows)
    needles_ok = all(boolish(row["needles_present"]) for row in source_rows)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1824_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1824_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1824_2_phi_attempt_written",
            any(row["attempt_id"] == "PZ1824_0_target" and row["derivation_result"] == "TARGET_ATTEMPTED" for row in rows_map["phi_zero_theorem"]),
            "Phi second derivative zero attempt is written",
        ),
        (
            "VAL1824_3_oddness_conditional",
            any(row["attempt_id"] == "PZ1824_1_signed_oddness" and row["derivation_result"] == "EXACT_CONDITIONAL_LEMMA" for row in rows_map["phi_zero_theorem"]),
            "signed-deficit oddness lemma is exact but conditional",
        ),
        (
            "VAL1824_4_theorem_not_promoted",
            any(row["attempt_id"] == "PZ1824_5_verdict" and row["derivation_result"] == "CONDITIONAL_ZERO_LEMMA_NOT_CURRENT_PROOF" for row in rows_map["phi_zero_theorem"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["phi_zero_theorem"]),
            "1824 theorem is not promoted as current proof",
        ),
        (
            "VAL1824_5_symmetry_route_nonclaim",
            any(row["route_id"] == "SDA1824_3_log_angle_owner" and row["current_status"] == "BEST_NEXT_TARGET" for row in rows_map["symmetry_route_audit"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["symmetry_route_audit"]),
            "signed-deficit symmetry route remains nonclaim",
        ),
        (
            "VAL1824_6_c2_rows_nonclaim",
            any(row["row_id"] == "C2S1824_3_total" and row["current_status"] == "MISSING_ZERO_OR_FINITE_SOURCE_ROW_NONCLAIM" for row in rows_map["visible_c2_source_row"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["visible_c2_source_row"]),
            "visible c2 source rows are nonclaim",
        ),
        (
            "VAL1824_7_countermodels_retained",
            all(boolish(row["retained"]) and not boolish(row["valid_for_claim"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain retained",
        ),
        (
            "VAL1824_8_gr_newton_nonclaim",
            all(not boolish(row["claim_allowed_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["gr_newton_impact"]),
            "GR/Newton impact rows remain nonclaim",
        ),
        (
            "VAL1824_9_acceptance_blocks",
            any(row["gate_id"] == "AC1824_0_phi_attempt_written" and boolish(row["gate_pass"]) and not boolish(row["claim_allowed"]) for row in rows_map["acceptance_gate"])
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["acceptance_gate"]),
            "acceptance gate permits contract-only progress and blocks claims",
        ),
        (
            "VAL1824_10_claim_gates_blocked",
            all(row["status"] in {"BLOCKED", "REFUSED"} and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all Phi/R2FR/local-GR claim gates remain blocked or refused",
        ),
        ("VAL1824_11_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1824_12_missing_not_ready", missing_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1824_13_decision_next",
            any(row["decision_id"] == "DEC1824_3_best_next" and row["decision"] == "SIGNED_DEFICIT_ODDNESS_THEOREM_OR_C2_PRIOR_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects signed-deficit oddness theorem next",
        ),
        (
            "VAL1824_14_next_selected",
            any(row["route_id"] == "NEXT1824_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1824_15_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1824 CSVs parse"),
        ("VAL1824_16_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1824_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1824_18_formalization_untouched", formalization_untouched(), "no 1824 outputs found under formalization-workbench"),
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
            "check_id": "VAL1824_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1824 Phi second derivative zero or visible c2 source row checkpoint",
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
            "# 1824 Y5 R2FR Phi second derivative zero or visible c2 source row",
            "",
            "**Progress:** 1824 finds the cleanest possible zero route for the visible quadratic deficit coefficient. If the primitive action is an oriented signed holonomy charge, `Phi(-delta)=-Phi(delta)` and `Phi''(0)=0`. If the action is a norm, trace, energy, entropy, or mismatch cost, `Phi''(0)` is generically live.",
            "",
            "**Current verdict:** conditional win only. Signed-deficit oddness would kill `c2_visible`, but the corpus does not yet derive that the parent action uses signed log-holonomy/angle rather than a trace or squared norm. So `c2_visible` remains a nonclaim source row.",
            "",
            "**Claim ceiling:** no `Phi''(0)=0` claim, no R2/fR zero claim, no finite scalaron score, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1824.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Phi Second Derivative Zero Theorem Attempt",
            markdown_table(rows_map["phi_zero_theorem"], ["attempt_id", "claim_piece", "mathematical_statement", "derivation_result", "current_status", "consequence", "valid_for_claim"]),
            "",
            "## Signed Deficit Symmetry Route Audit",
            markdown_table(rows_map["symmetry_route_audit"], ["route_id", "needed_clause", "formal_condition", "why_it_matters", "current_status", "valid_for_claim"]),
            "",
            "## Visible C2 Source Row",
            markdown_table(rows_map["visible_c2_source_row"], ["row_id", "row_type", "quantity", "formula_or_value", "required_inputs", "units", "source_path", "current_status", "score_ready", "valid_for_claim"]),
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
            "This is a small but real mathematical gain. The visible R2 wound now has a specific zero mechanism: odd signed-deficit response. The next fight is not vague at all: prove MTS action is signed log-holonomy/angle, not a norm/trace cost. If that fails, the c2 prior/source row becomes unavoidable.",
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
    print(f"1824 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
