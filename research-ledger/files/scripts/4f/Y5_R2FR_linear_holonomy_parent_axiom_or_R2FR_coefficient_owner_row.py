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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1822"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1822-Y5-R2FR-linear-holonomy-parent-axiom-or-R2FR-coefficient-owner-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1822_0_1821_next",
        "source_key": "1821_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1821_NEXT_TARGET.csv",
        "needles": ["NEXT1821_0_primary", "selected"],
        "role": "1821 selects the linear holonomy/additive-cell axiom as the next proof target.",
    },
    {
        "source_id": "SRC1822_1_1821_validation",
        "source_key": "1821_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1821_VALIDATION.csv",
        "needles": ["VAL1821_OVERALL", "PASS"],
        "role": "confirms 1821 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1822_2_1821_contract",
        "source_key": "1821_linear_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1821_LINEAR_HOLONOMY_DERIVATION_CONTRACT.csv",
        "needles": ["LHC1821_1_additivity", "BEST_NEW_PROOF_TARGET"],
        "role": "linear holonomy/additivity was the strongest remaining proof route.",
    },
    {
        "source_id": "SRC1822_3_1821_minimality",
        "source_key": "1821_minimality",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1821_NO_HIGHER_DERIVATIVE_PARENT_MINIMALITY_THEOREM.csv",
        "needles": ["NHD1821_2_linear_holonomy_route", "LINEARITY_AXIOM_NOT_PARENT_DERIVED"],
        "role": "1821 identified linearity as unsigned, not proven.",
    },
    {
        "source_id": "SRC1822_4_1821_bound",
        "source_key": "1821_bound_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1821_R2FR_BOUND_ROW_SCHEMA.csv",
        "needles": ["R2B1821_5_total", "MISSING_PARENT_AND_ARENA_INPUTS_ROW_NONCLAIM"],
        "role": "finite R2/fR fallback row remains schema-only.",
    },
    {
        "source_id": "SRC1822_5_962_zero",
        "source_key": "962_relative_zero",
        "source_path": RESIDUALS / "P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv",
        "needles": ["R2Z962_5_relative_zero_theorem", "RELATIVE_THEOREM_PROVEN_PARENT_PREMISE_UNSIGNED"],
        "role": "R2/fR zero theorem awaits a parent activator.",
    },
    {
        "source_id": "SRC1822_6_963_owner",
        "source_key": "963_coefficient_owner",
        "source_path": RESIDUALS / "P8_Y5_R10_963_R2FR_COEFFICIENT_OWNER_AUDIT.csv",
        "needles": ["CO963_4_verdict", "NO_EXECUTABLE_OWNER_FOUND"],
        "role": "no current executable owner for c_R2/f_RR exists.",
    },
    {
        "source_id": "SRC1822_7_963_order",
        "source_key": "963_derivative_order",
        "source_path": RESIDUALS / "P8_Y5_R10_963_DERIVATIVE_ORDER_AUDIT.csv",
        "needles": ["DO963_6_verdict", "NOT_PARENT_SIGNED_CURRENT_CORPUS"],
        "role": "second-order parent signature is still not signed.",
    },
    {
        "source_id": "SRC1822_8_964_minimality",
        "source_key": "964_minimality",
        "source_path": RESIDUALS / "P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
        "needles": ["MIN964_5_verdict", "THEOREM_NOT_PROVEN_CURRENT_CORPUS"],
        "role": "prior no-higher-derivative minimality attempt failed.",
    },
    {
        "source_id": "SRC1822_9_965_primitive",
        "source_key": "965_primitive",
        "source_path": RESIDUALS / "P8_Y5_R10_965_PRIMITIVE_QUOTIENT_THEOREM_ATTEMPT.csv",
        "needles": ["PQ965_5_verdict", "THEOREM_NOT_PROVEN_CURRENT_CORPUS"],
        "role": "primitive quotient/no-marker theorem is not proven.",
    },
    {
        "source_id": "SRC1822_10_440_reduction",
        "source_key": "440_sector_reduction",
        "source_path": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
        "needles": ["R2_fR_scalar_mode", "retained_R11_plus_R10_if_finite_range"],
        "role": "sector reduction retains R2/fR if no zero theorem closes.",
    },
]


OUTPUTS: dict[str, Path] = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1822_SOURCE_REGISTER.csv",
    "linearity_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1822_LINEAR_HOLONOMY_PARENT_AXIOM_ATTEMPT.csv",
    "additivity_loophole_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1822_ADDITIVITY_LOOPHOLE_AUDIT.csv",
    "coefficient_owner": RESIDUALS / "P8_Y5_PARENT_QLOC_1822_R2FR_COEFFICIENT_OWNER_ROW.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1822_COUNTERMODEL_LEDGER.csv",
    "gr_newton_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1822_GR_NEWTON_IMPACT_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1822_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1822_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1822_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1822_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1822_VALIDATION.csv",
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


def linearity_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LHA1822_0_target",
            "claim_piece": "primitive linear holonomy parent axiom",
            "mathematical_statement": "The local gravitational action density is generated by one primitive holonomy/deficit response C(F), and C is forced linear in the local curvature flux F.",
            "derivation_result": "TARGET_ATTEMPTED",
            "current_status": "NOT_PARENT_PROVEN",
            "consequence": "without this, c_R2/f_RR remains a legal coefficient owner",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LHA1822_1_disjoint_additivity",
            "claim_piece": "disjoint region additivity",
            "mathematical_statement": "S[A union B]=S[A]+S[B] for disjoint cells follows from locality and integration.",
            "derivation_result": "TRUE_BUT_TOO_WEAK",
            "current_status": "DOES_NOT_FORCE_L_DENSITY_LINEAR",
            "consequence": "a local density L=R+epsilon R2 is still additive over disjoint cells",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LHA1822_2_same_cell_additivity",
            "claim_piece": "same-cell flux additivity",
            "mathematical_statement": "If for independent infinitesimal curvature fluxes in the same primitive cell C(F1+F2)=C(F1)+C(F2), C(0)=0, and C is smooth/local, then C is linear and d2C/dF2=0.",
            "derivation_result": "EXACT_CONDITIONAL_LEMMA",
            "current_status": "PREMISE_NOT_DERIVED_FROM_MTS",
            "consequence": "would forbid quadratic curvature response if parent-signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LHA1822_3_holonomy_composition",
            "claim_piece": "loop composition",
            "mathematical_statement": "Small-loop holonomies compose with a leading additive curvature flux plus BCH/commutator corrections at higher order in loop area.",
            "derivation_result": "HELPFUL_BUT_NOT_ENOUGH",
            "current_status": "DOES_NOT_FORBID_ACTION_BUILT_FROM_QUADRATIC_INVARIANTS",
            "consequence": "holonomy composition alone does not kill R2/fR",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LHA1822_4_deficit_action_law",
            "claim_piece": "Regge-like linear deficit action",
            "mathematical_statement": "If the primitive cell action is proportional to area times deficit/holonomy angle rather than deficit squared, the continuum operator is EH-like and curvature-squared terms require a separate c2 response.",
            "derivation_result": "BEST_REMAINING_PARENT_PROOF_ROUTE",
            "current_status": "DEFICIT_LINEAR_COST_NOT_DERIVED",
            "consequence": "moves next target from vague additivity to a concrete primitive action law",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LHA1822_5_no_new_scale_guard",
            "claim_piece": "no-new-scale argument",
            "mathematical_statement": "In four dimensions, an R2 coefficient can be dimensionless after EH normalization, so absence of a new length scale alone does not zero c_R2.",
            "derivation_result": "REJECTED_AS_ZERO_PROOF",
            "current_status": "NO_ZERO_CREDIT",
            "consequence": "must prove coefficient absence, not merely scale absence",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LHA1822_6_verdict",
            "claim_piece": "1822 proves the linear holonomy axiom",
            "mathematical_statement": "The exact linearity lemma is available only if same-cell primitive response additivity or a linear deficit-action law is parent-derived; current corpus does not prove either.",
            "derivation_result": "CONDITIONAL_LEMMA_NOT_CURRENT_PROOF",
            "current_status": "DEMOTE_TO_COEFFICIENT_OWNER_ROW",
            "consequence": "R2/fR remains retained as explicit coefficient-owner debt",
            "valid_for_claim": False,
        },
    ]


def additivity_loophole_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "loophole_id": "ALO1822_0_local_density",
            "loophole": "ordinary locality already gives disjoint-cell additivity",
            "why_it_matters": "this does not distinguish R from R+epsilon R2",
            "needed_fix": "same-cell flux-response additivity, not merely region additivity",
            "current_status": "OPEN",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "loophole_id": "ALO1822_1_curvature_superposition",
            "loophole": "curvature amplitudes at the same point are not independent thermodynamic charges by default",
            "why_it_matters": "C(F1+F2)=C(F1)+C(F2) is an extra parent axiom unless MTS derives it",
            "needed_fix": "derive primitive response composition from motion-time-space path/cell rules",
            "current_status": "OPEN",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "loophole_id": "ALO1822_2_nonabelian_holonomy",
            "loophole": "holonomy composition has BCH commutators beyond leading flux",
            "why_it_matters": "nonlinear invariants are not automatically illegal just because leading holonomy is linear",
            "needed_fix": "show action uses only first deficit/trace response and treats higher BCH terms as boundary/topological/zero",
            "current_status": "OPEN",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "loophole_id": "ALO1822_3_dimensionless_c2",
            "loophole": "R2 in four dimensions can carry a dimensionless coefficient",
            "why_it_matters": "no-new-scale reasoning does not remove the R2 operator",
            "needed_fix": "coefficient-origin theorem or explicit coefficient-owner row",
            "current_status": "OPEN",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "loophole_id": "ALO1822_4_hidden_second_response",
            "loophole": "hidden scalar, marker, memory or projector can own the quadratic response",
            "why_it_matters": "even visible linearity is insufficient if reduction regenerates R2/fR",
            "needed_fix": "no-integrated-tower/no-marker theorem or finite bound row",
            "current_status": "OPEN",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "loophole_id": "ALO1822_5_verdict",
            "loophole": "linearity proof closure",
            "why_it_matters": "every loophole above must close before c_R2=f_RR=0 can be claimed",
            "needed_fix": "1823 primitive deficit-action law or coefficient owner",
            "current_status": "FAIL_CURRENT_LINEARITY_PROOF",
            "valid_for_claim": False,
        },
    ]


def coefficient_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "owner_id": "CO1822_0_zero_owner",
            "coefficient": "c_R2_eff_or_f_RR",
            "candidate_owner": "parent linear deficit/holonomy theorem",
            "owner_status": "UNSIGNED_ZERO_OWNER",
            "required_evidence": "primitive action law linear in deficit/holonomy plus no second channel/no hidden tower",
            "claim_effect": "would set c_R2_eff=f_RR=0",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "CO1822_1_visible_c2",
            "coefficient": "c_R2_eff_or_f_RR",
            "candidate_owner": "visible quadratic curvature response coefficient",
            "owner_status": "MISSING_PARENT_INPUT",
            "required_evidence": "symbolic or numeric c2 coefficient, sign, units, normalization and source path",
            "claim_effect": "would define a finite scalar-mode residual row, not a zero theorem",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "CO1822_2_hidden_scalar",
            "coefficient": "c_R2_eff_or_f_RR",
            "candidate_owner": "integrated-out scalar or auxiliary response",
            "owner_status": "COUNTERMODEL_LIVE_NOT_SOURCED",
            "required_evidence": "beta, M, coupling sign, source path, and readout/screening map",
            "claim_effect": "would produce c_R2_eff=beta2/(2M2) in the simple toy branch",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "CO1822_3_marker_prefactor",
            "coefficient": "c_R2_eff_or_f_RR",
            "candidate_owner": "domain/class/source marker response",
            "owner_status": "NO_MARKER_THEOREM_MISSING",
            "required_evidence": "prove absent/gauge/universal or source finite marker coefficient",
            "claim_effect": "would map source/domain dependence into a residual sector",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "CO1822_4_external_bound",
            "coefficient": "alpha_bound_lambda_interface",
            "candidate_owner": "R10/PPN empirical bound interface",
            "owner_status": "MISSING_FULL_CURVE_AND_RESPONSE_MAP",
            "required_evidence": "full bound curve, alpha convention, scalar range/coupling, PPN response and provenance",
            "claim_effect": "would test finite branch only after parent coefficient exists",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "CO1822_5_verdict",
            "coefficient": "c_R2_eff_or_f_RR",
            "candidate_owner": "current corpus",
            "owner_status": "NO_EXECUTABLE_OWNER_FOUND_CURRENT_1822",
            "required_evidence": "prove zero owner or fill one finite owner route above",
            "claim_effect": "R2/fR scalar branch remains explicit nonclaim residual",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1822_0_local_R_plus_R2",
            "countermodel": "a perfectly local additive density L=R+epsilon R2",
            "why_it_survives": "region additivity does not imply curvature-linearity",
            "blocked_by": "same-cell response linearity or deficit-action theorem",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1822_1_deficit_squared",
            "countermodel": "primitive action cost includes deficit angle squared",
            "why_it_survives": "requires no new spacetime region and can mimic R2 in the continuum",
            "blocked_by": "derive action cost linear in deficit/holonomy angle",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1822_2_hidden_quadratic_response",
            "countermodel": "hidden scalar or marker owns the second curvature response channel",
            "why_it_survives": "visible linearity alone does not prove the reduced action stays linear",
            "blocked_by": "no-hidden-tower/no-marker theorem",
            "retained": True,
            "valid_for_claim": False,
        },
    ]


def gr_newton_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1822_0_if_deficit_linear_closes",
            "if_closed": "primitive action is parent-derived linear in holonomy/deficit and has no second response channel",
            "would_buy": "strong operator-side route to EH linear curvature without importing Einstein equations",
            "still_missing": "connection, boundary, source equality and residual sectors",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1822_1_if_owner_row_filled",
            "if_closed": "c_R2/f_RR obtains a source-backed owner row",
            "would_buy": "finite scalar-mode branch becomes testable/boundable instead of vague",
            "still_missing": "bound curve, weak-field response, coupling and normalizer",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1822_2_verdict",
            "if_closed": "1822 proves local GR/Newton",
            "would_buy": "nothing claimable alone; 1822 leaves the linearity proof unsigned",
            "still_missing": "R2/fR zero, other R11 rows, C-term closure, source calibration",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1822_0_linearity_attempt_written",
            "gate": "linear holonomy proof attempt written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "1822 distinguishes weak disjoint additivity from the stronger same-cell/deficit-linearity axiom",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1822_1_same_cell_additivity",
            "gate": "same-cell flux response additivity parent-derived",
            "current_status": "BLOCKED",
            "reason": "MTS current corpus has not derived C(F1+F2)=C(F1)+C(F2)",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1822_2_deficit_linear_law",
            "gate": "primitive deficit action law parent-derived",
            "current_status": "BLOCKED",
            "reason": "linear deficit/holonomy cost is the next target, not current evidence",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1822_3_coefficient_owner",
            "gate": "finite c_R2/f_RR owner row source-backed",
            "current_status": "BLOCKED",
            "reason": "all coefficient-owner routes are missing parent inputs or response maps",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1822_0_linear_holonomy",
            "claim": "primitive linear holonomy axiom is derived",
            "status": "BLOCKED",
            "reason": "same-cell additivity/deficit-linearity is not parent-signed",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1822_1_R2FR_zero",
            "claim": "c_R2/f_RR is theorem-zero",
            "status": "BLOCKED",
            "reason": "the zero owner remains unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1822_2_finite_score",
            "claim": "finite R2/fR scalar branch can be scored",
            "status": "REFUSED",
            "reason": "no executable coefficient owner, bound curve or response map exists",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1822_3_local_GR",
            "claim": "local GR/Newton is derived",
            "status": "REFUSED",
            "reason": "operator-side linearity is still a subgate and remains open",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1822_0_linearity_result",
            "decision": "LINEAR_HOLONOMY_AXIOM_NOT_PROVEN",
            "reason": "same-cell response additivity is an exact sufficient condition but is not derived from current MTS primitives",
            "next_action": "do not zero R2/fR from additivity alone",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1822_1_best_subroute",
            "decision": "DEFICIT_ACTION_LAW_NEXT",
            "reason": "the sharper proof target is now whether MTS primitives force action cost linear in holonomy/deficit rather than deficit squared",
            "next_action": "attempt primitive deficit-angle action law",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1822_2_owner_status",
            "decision": "COEFFICIENT_OWNER_ROW_READY_NONCLAIM",
            "reason": "if the deficit law fails, c_R2/f_RR must be owned by zero theorem, visible c2, hidden scalar, marker, or empirical bound interface",
            "next_action": "keep all owner rows valid_for_claim=false until sourced",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1822_3_best_next",
            "decision": "PRIMITIVE_DEFICIT_ACTION_LAW_NEXT",
            "reason": "this is the concrete mathematical hinge behind linear holonomy; it may connect MTS path/cell intuition to EH/Regge-like linear curvature",
            "next_action": "1823-Y5-R2FR-primitive-deficit-action-law-or-visible-c2-owner-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1822_0_primary",
            "next_target": "1823-Y5-R2FR-primitive-deficit-action-law-or-visible-c2-owner-row.md",
            "script": "scripts/Y5_R2FR_primitive_deficit_action_law_or_visible_c2_owner_row.py",
            "objective": "derive whether the primitive MTS cell/path action is linear in holonomy deficit; if not, fill the visible c2 coefficient-owner row as nonclaim",
            "selection_status": "selected",
            "success_condition": "deficit-linearity theorem signed, or visible c2 owner row remains nonclaim with all inputs explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1822_1_parallel",
            "next_target": "1823b-Y5-R2FR-hidden-scalar-owner-row.md",
            "script": "scripts/Y5_R2FR_hidden_scalar_owner_row.py",
            "objective": "if visible deficit-linearity fails, quantify the integrated-out scalar route to c_R2_eff",
            "selection_status": "held_parallel",
            "success_condition": "beta, M, coupling, units and source path are present or row remains invalid for claim",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "linearity_theorem": linearity_theorem_rows(),
        "additivity_loophole_audit": additivity_loophole_rows(),
        "coefficient_owner": coefficient_owner_rows(),
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
    allowed_gate_pass = {"AC1822_0_linearity_attempt_written"}
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
                or (boolish(row.get("gate_pass", False)) and row.get("gate_id") != "AC1822_0_linearity_attempt_written")
            ):
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    exists_ok = all(boolish(row["exists"]) for row in source_rows)
    needles_ok = all(boolish(row["needles_present"]) for row in source_rows)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1822_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1822_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1822_2_linearity_attempt_written",
            any(row["attempt_id"] == "LHA1822_0_target" and row["derivation_result"] == "TARGET_ATTEMPTED" for row in rows_map["linearity_theorem"]),
            "linear holonomy parent axiom attempt is written",
        ),
        (
            "VAL1822_3_disjoint_additivity_rejected",
            any(row["attempt_id"] == "LHA1822_1_disjoint_additivity" and row["derivation_result"] == "TRUE_BUT_TOO_WEAK" for row in rows_map["linearity_theorem"]),
            "weak disjoint-cell additivity is rejected as a zero proof",
        ),
        (
            "VAL1822_4_conditional_lemma_only",
            any(row["attempt_id"] == "LHA1822_2_same_cell_additivity" and row["current_status"] == "PREMISE_NOT_DERIVED_FROM_MTS" for row in rows_map["linearity_theorem"]),
            "same-cell linearity lemma remains conditional",
        ),
        (
            "VAL1822_5_theorem_not_promoted",
            any(row["attempt_id"] == "LHA1822_6_verdict" and row["derivation_result"] == "CONDITIONAL_LEMMA_NOT_CURRENT_PROOF" for row in rows_map["linearity_theorem"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["linearity_theorem"]),
            "1822 theorem is not promoted as current proof",
        ),
        (
            "VAL1822_6_loopholes_retained",
            any(row["loophole_id"] == "ALO1822_5_verdict" and row["current_status"] == "FAIL_CURRENT_LINEARITY_PROOF" for row in rows_map["additivity_loophole_audit"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["additivity_loophole_audit"]),
            "additivity loopholes remain explicit",
        ),
        (
            "VAL1822_7_owner_rows_nonclaim",
            any(row["owner_id"] == "CO1822_5_verdict" and row["owner_status"] == "NO_EXECUTABLE_OWNER_FOUND_CURRENT_1822" for row in rows_map["coefficient_owner"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["coefficient_owner"]),
            "coefficient owner rows are schema-only and nonclaim",
        ),
        (
            "VAL1822_8_countermodels_retained",
            all(boolish(row["retained"]) and not boolish(row["valid_for_claim"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain retained",
        ),
        (
            "VAL1822_9_gr_newton_nonclaim",
            all(not boolish(row["claim_allowed_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["gr_newton_impact"]),
            "GR/Newton impact rows remain nonclaim",
        ),
        (
            "VAL1822_10_acceptance_blocks",
            any(row["gate_id"] == "AC1822_0_linearity_attempt_written" and boolish(row["gate_pass"]) and not boolish(row["claim_allowed"]) for row in rows_map["acceptance_gate"])
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["acceptance_gate"]),
            "acceptance gate permits contract-only progress and blocks claims",
        ),
        (
            "VAL1822_11_claim_gates_blocked",
            all(row["status"] in {"BLOCKED", "REFUSED"} and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all linearity/R2FR/local-GR claim gates remain blocked or refused",
        ),
        ("VAL1822_12_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1822_13_missing_not_ready", missing_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1822_14_decision_next",
            any(row["decision_id"] == "DEC1822_3_best_next" and row["decision"] == "PRIMITIVE_DEFICIT_ACTION_LAW_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects primitive deficit action law next",
        ),
        (
            "VAL1822_15_next_selected",
            any(row["route_id"] == "NEXT1822_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1822_16_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1822 CSVs parse"),
        ("VAL1822_17_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1822_18_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1822_19_formalization_untouched", formalization_untouched(), "no 1822 outputs found under formalization-workbench"),
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
            "check_id": "VAL1822_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1822 linear holonomy parent axiom or R2FR coefficient owner row checkpoint",
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
            "# 1822 Y5 R2FR linear holonomy parent axiom or R2FR coefficient owner row",
            "",
            "**Progress:** 1822 tests the additivity idea rather than just admiring it from a safe distance. The useful result is a separation: disjoint-region additivity is too weak, but same-cell curvature-flux additivity would force linear response if MTS can derive it.",
            "",
            "**Current verdict:** no proof yet. The exact conditional lemma is real: smooth same-cell additivity implies linear curvature response. But current MTS evidence does not derive that premise. The next sharper target is a primitive deficit/holonomy action law: why the action cost is linear in deficit rather than deficit-squared.",
            "",
            "**Claim ceiling:** no linear-holonomy theorem claim, no R2/fR zero claim, no finite scalaron score, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1822.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Linear Holonomy Parent Axiom Attempt",
            markdown_table(rows_map["linearity_theorem"], ["attempt_id", "claim_piece", "mathematical_statement", "derivation_result", "current_status", "consequence", "valid_for_claim"]),
            "",
            "## Additivity Loophole Audit",
            markdown_table(rows_map["additivity_loophole_audit"], ["loophole_id", "loophole", "why_it_matters", "needed_fix", "current_status", "valid_for_claim"]),
            "",
            "## R2FR Coefficient Owner Row",
            markdown_table(rows_map["coefficient_owner"], ["owner_id", "coefficient", "candidate_owner", "owner_status", "required_evidence", "claim_effect", "score_ready", "valid_for_claim"]),
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
            "This is a useful tightening. The theory cannot win by saying actions are additive over regions; every local field theory has that. The serious MTS route is stronger: prove the primitive cell/path cost is linear in holonomy deficit. If that works, EH begins to look forced. If it fails, c_R2/f_RR must be explicitly owned and tested.",
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
    print(f"1822 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
