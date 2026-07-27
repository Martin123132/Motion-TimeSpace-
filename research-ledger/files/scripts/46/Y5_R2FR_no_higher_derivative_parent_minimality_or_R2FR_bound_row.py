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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1821"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1821-Y5-R2FR-no-higher-derivative-parent-minimality-or-R2FR-bound-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1821_0_1820_next",
        "source_key": "1820_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1820_NEXT_TARGET.csv",
        "needles": ["NEXT1820_0_primary", "selected"],
        "role": "1820 selects no-higher-derivative parent minimality as the primary target.",
    },
    {
        "source_id": "SRC1821_1_1820_validation",
        "source_key": "1820_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1820_VALIDATION.csv",
        "needles": ["VAL1820_OVERALL", "PASS"],
        "role": "confirms 1820 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1821_2_1820_decision",
        "source_key": "1820_decision",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1820_DECISION_LEDGER.csv",
        "needles": ["DEC1820_3_best_next", "NO_HIGHER_DERIVATIVE_PARENT_MINIMALITY_NEXT"],
        "role": "1820 decision ledger identifies the next derivation-first route.",
    },
    {
        "source_id": "SRC1821_3_1820_R2FR_audit",
        "source_key": "1820_R2FR_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1820_R2FR_SCALAR_MODE_AUDIT.csv",
        "needles": ["R2A1820_8_verdict", "FAIL_ZERO_PROOF_KEEP_FIRST_ROW_NONCLAIM"],
        "role": "R2/fR closure failed in 1820 and must remain explicit.",
    },
    {
        "source_id": "SRC1821_4_1820_CEH_row",
        "source_key": "1820_CEH_first_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1820_C_EH_FIRST_ROW_SCHEMA.csv",
        "needles": ["CEH1820_4_total", "MISSING_PARENT_INPUTS_ROW_NONCLAIM"],
        "role": "first C_EH/R11 scalar-mode row exists only as a schema.",
    },
    {
        "source_id": "SRC1821_5_964_minimality",
        "source_key": "964_minimality",
        "source_path": RESIDUALS / "P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
        "needles": ["MIN964_5_verdict", "THEOREM_NOT_PROVEN_CURRENT_CORPUS"],
        "role": "prior no-higher-derivative/minimality theorem attempt failed.",
    },
    {
        "source_id": "SRC1821_6_964_template",
        "source_key": "964_R2FR_template",
        "source_path": RESIDUALS / "P8_Y5_R10_964_R2FR_NONCLAIM_INPUT_TEMPLATE.csv",
        "needles": ["R2IN964_0_mts_prediction_required", "MISSING_PARENT_INPUT"],
        "role": "finite R2/fR scalar-mode input template rejects placeholders.",
    },
    {
        "source_id": "SRC1821_7_965_primitive",
        "source_key": "965_primitive_quotient",
        "source_path": RESIDUALS / "P8_Y5_R10_965_PRIMITIVE_QUOTIENT_THEOREM_ATTEMPT.csv",
        "needles": ["PQ965_5_verdict", "THEOREM_NOT_PROVEN_CURRENT_CORPUS"],
        "role": "primitive quotient/no-natural-marker theorem is not proven.",
    },
    {
        "source_id": "SRC1821_8_965_algebra",
        "source_key": "965_invariant_algebra",
        "source_path": RESIDUALS / "P8_Y5_R10_965_LOCAL_INVARIANT_ALGEBRA_AUDIT.csv",
        "needles": ["ALG965_5_memory_class_scalar", "not_eliminated"],
        "role": "local invariant generators still exist that can act as markers or scalar channels.",
    },
    {
        "source_id": "SRC1821_9_962_zero",
        "source_key": "962_relative_zero",
        "source_path": RESIDUALS / "P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv",
        "needles": ["R2Z962_5_relative_zero_theorem", "RELATIVE_THEOREM_PROVEN_PARENT_PREMISE_UNSIGNED"],
        "role": "R2/fR zero theorem exists only as a relative implication.",
    },
    {
        "source_id": "SRC1821_10_963_order",
        "source_key": "963_derivative_order",
        "source_path": RESIDUALS / "P8_Y5_R10_963_DERIVATIVE_ORDER_AUDIT.csv",
        "needles": ["DO963_6_verdict", "NOT_PARENT_SIGNED_CURRENT_CORPUS"],
        "role": "parent second-order/no-extra-scalar signature is not signed.",
    },
    {
        "source_id": "SRC1821_11_963_owner",
        "source_key": "963_coefficient_owner",
        "source_path": RESIDUALS / "P8_Y5_R10_963_R2FR_COEFFICIENT_OWNER_AUDIT.csv",
        "needles": ["CO963_4_verdict", "NO_EXECUTABLE_OWNER_FOUND"],
        "role": "no executable owner exists for c_R2/f_RR.",
    },
    {
        "source_id": "SRC1821_12_963_scalar",
        "source_key": "963_no_extra_scalar",
        "source_path": RESIDUALS / "P8_Y5_R10_963_NO_EXTRA_SCALAR_SIGNATURE.csv",
        "needles": ["NES963_5_verdict", "BLOCKED_NOT_PARENT_SIGNED"],
        "role": "no-extra-scalar parent signature is blocked.",
    },
    {
        "source_id": "SRC1821_13_440_reduction",
        "source_key": "440_sector_reduction",
        "source_path": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
        "needles": ["R2_fR_scalar_mode", "retained_R11_plus_R10_if_finite_range"],
        "role": "sector-reduction ledger retains R2/fR as R11 plus finite-range R10 if not zeroed.",
    },
]


OUTPUTS: dict[str, Path] = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1821_SOURCE_REGISTER.csv",
    "minimality_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1821_NO_HIGHER_DERIVATIVE_PARENT_MINIMALITY_THEOREM.csv",
    "linear_holonomy_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1821_LINEAR_HOLONOMY_DERIVATION_CONTRACT.csv",
    "integrated_tower_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1821_NO_INTEGRATED_TOWER_AUDIT.csv",
    "bound_row_schema": RESIDUALS / "P8_Y5_PARENT_QLOC_1821_R2FR_BOUND_ROW_SCHEMA.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1821_COUNTERMODEL_LEDGER.csv",
    "gr_newton_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1821_GR_NEWTON_IMPACT_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1821_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1821_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1821_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1821_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1821_VALIDATION.csv",
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


def minimality_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHD1821_0_target",
            "claim_piece": "parent no-higher-derivative minimality theorem",
            "mathematical_statement": "The ordinary compact local exterior parent action admits no R2, nonlinear f(R), Ricci2, Weyl2, nonlocal curvature kernel, or integrated-out scalar tower after reduction.",
            "attempt_result": "TARGET_RESTATED_WITH_STRONGER_LINEARITY_ROUTE",
            "current_status": "NOT_PARENT_SIGNED",
            "would_close": "activates R2Z962_5 and sets c_R2=f_RR=0",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHD1821_1_relative_filter",
            "claim_piece": "derivative-order filter",
            "mathematical_statement": "Nonlinear f(R) yields f_R-dependent metric variation and therefore higher-derivative trace/scalaron terms unless f_RR=0 on the local branch.",
            "attempt_result": "RELATIVE_THEOREM_ALREADY_AVAILABLE",
            "current_status": "PARENT_ACTIVATOR_UNSIGNED",
            "would_close": "kills R2/fR if second-order/no-extra-scalar/minimality is signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHD1821_2_linear_holonomy_route",
            "claim_piece": "new best derivation route",
            "mathematical_statement": "If the primitive MTS gravitational response is additive over infinitesimal cells and depends on a single curvature-holonomy flux channel, C(F1+F2)=C(F1)+C(F2) forces a linear curvature density; R2/fR requires an independent quadratic response coefficient.",
            "attempt_result": "EXACT_CONDITIONAL_LEMMA_SHAPE",
            "current_status": "LINEARITY_AXIOM_NOT_PARENT_DERIVED",
            "would_close": "forbids visible curvature-squared terms without appealing to empirical smallness",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHD1821_3_single_channel_requirement",
            "claim_piece": "single response channel",
            "mathematical_statement": "The parent must own exactly one local metric/coframe curvature response channel; no second response coefficient, local marker, hidden scalar, or post-readout EFT term may be varied as part of the parent action.",
            "attempt_result": "REQUIRED_CLOSURE_CONTRACT",
            "current_status": "NOT_DERIVED_FROM_CURRENT_CORPUS",
            "would_close": "prevents c_R2/f_RR from entering through a second channel",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHD1821_4_integrated_tower",
            "claim_piece": "no integrated-out curvature tower",
            "mathematical_statement": "Solving auxiliary/projector/memory/scalar equations must not generate Delta S_eff[g] containing R2, f(R), Ricci2, Weyl2, Yukawa poles or nonlocal kernels.",
            "attempt_result": "CENTRAL_OPEN_HAZARD",
            "current_status": "NOT_DERIVED",
            "would_close": "blocks hidden origin of c_R2/f_RR",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHD1821_5_no_marker_prefactor",
            "claim_piece": "no marker-prefactor curvature term",
            "mathematical_statement": "No quotient-invariant scalar, domain selector, memory class, finite-cell spectrum, species constant, or class label may form F(sigma)R or F(sigma)R2 in the local parent action.",
            "attempt_result": "NOT_PROVEN",
            "current_status": "LIVE_LOCAL_INVARIANT_GENERATORS",
            "would_close": "removes source/domain-dependent curvature coefficients",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHD1821_6_stability_guard",
            "claim_piece": "regularity/stability is not enough",
            "mathematical_statement": "Ostrogradsky or regularity intuition alone cannot zero R2/fR because R2/f(R) can be rewritten as scalar-tensor with a finite scalar mode.",
            "attempt_result": "NO_ZERO_CREDIT",
            "current_status": "STABILITY_IS_GUIDE_NOT_PROOF",
            "would_close": "nothing unless converted into a parent constraint algebra",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHD1821_7_verdict",
            "claim_piece": "1821 proves no-higher-derivative parent minimality",
            "mathematical_statement": "1821 sharpens the route to a linear-holonomy/additive-cell parent axiom plus no-hidden-tower/no-marker conditions, but it does not prove those clauses from the current corpus.",
            "attempt_result": "CONDITIONAL_ROUTE_NOT_CURRENT_PROOF",
            "current_status": "DEMOTE_TO_R2FR_BOUND_ROW_SCHEMA",
            "would_close": "not closed; R2/fR remains retained nonclaim",
            "valid_for_claim": False,
        },
    ]


def linear_holonomy_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "LHC1821_0_parent_axiom",
            "needed_clause": "primitive local gravitational action is generated by infinitesimal motion-time-space holonomy/area response",
            "formal_condition": "S_cell[F]=C(F)dV with F the local curvature/holonomy flux of the observed connection/coframe",
            "reason_it_helps": "moves EH selection from arbitrary metric EFT to a primitive response law",
            "current_status": "AXIOM_NOT_PARENT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "LHC1821_1_additivity",
            "needed_clause": "cell response is additive under independent infinitesimal patches",
            "formal_condition": "C(F1+F2)=C(F1)+C(F2), C(0)=0, locality and smoothness",
            "reason_it_helps": "smooth additive response is linear, so quadratic curvature terms require a second channel",
            "current_status": "BEST_NEW_PROOF_TARGET",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "LHC1821_2_single_tensor_channel",
            "needed_clause": "only the metric/coframe curvature scalar channel couples to the local action",
            "formal_condition": "no independent scalar/vector/projector/domain/memory response coefficient is varied in S_parent",
            "reason_it_helps": "prevents a hidden c_R2/f_RR owner",
            "current_status": "NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "LHC1821_3_EH_reconstruction",
            "needed_clause": "linear curvature scalar plus volume term reconstructs EH plus Lambda/topological boundary",
            "formal_condition": "S_ext = int sqrt(-g)(a R - 2 Lambda) + S_boundary/topological",
            "reason_it_helps": "connects the linear response law directly to the EH operator selector",
            "current_status": "CONDITIONAL_IF_0_TO_2_CLOSE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "LHC1821_4_failure_mode",
            "needed_clause": "no quadratic response coefficient",
            "formal_condition": "delta^2 C/dF^2 = 0 as parent theorem, not a chosen truncation",
            "reason_it_helps": "without this, EH+epsilon R2 is a legal covariant local theory",
            "current_status": "UNSIGNED_THEREFORE_R2FR_RETAINED",
            "valid_for_claim": False,
        },
    ]


def integrated_tower_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ITA1821_0_hidden_scalar",
            "sector": "auxiliary or hidden scalar",
            "escape_formula": "-1/2 M2 phi2 + beta phi R -> beta2 R2/(2 M2) after solving phi",
            "current_status": "COUNTERMODEL_LIVE",
            "needed_zero_or_bound": "prove scalar absent/gauge/topological/stressless or source c_R2_eff",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ITA1821_1_memory_kernel",
            "sector": "memory or nonlocal kernel",
            "escape_formula": "integral K(x,x') R(x)R(x') or R Box^-1 R",
            "current_status": "NOT_FORBIDDEN",
            "needed_zero_or_bound": "local compact memory silence theorem or nonlocal kernel norm row",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ITA1821_2_projector_readout",
            "sector": "projector/readout variable",
            "escape_formula": "metric variation after early readout can regenerate source-dependent curvature terms",
            "current_status": "READOUT_AFTER_VARIATION_THEOREM_MISSING",
            "needed_zero_or_bound": "parent-owned readout-after-variation theorem or projector commutator bound",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ITA1821_3_marker_prefactor",
            "sector": "domain/class/species marker",
            "escape_formula": "F(sigma)R or F(sigma)R2",
            "current_status": "NO_NATURAL_MARKER_THEOREM_MISSING",
            "needed_zero_or_bound": "primitive quotient/no-marker theorem or finite marker-coupling row",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ITA1821_4_total",
            "sector": "all hidden tower channels",
            "escape_formula": "sum of visible and generated higher-curvature/nonlocal scalar-mode residuals",
            "current_status": "FAIL_NO_INTEGRATED_TOWER_PROOF",
            "needed_zero_or_bound": "componentwise theorem-zero or source-backed no-cancellation envelope",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def bound_row_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "R2B1821_0_zero_switch",
            "row_type": "theorem_zero_switch",
            "quantity": "c_R2_eff_or_f_RR",
            "formula_or_value": "0 only if NHD1821 parent clauses are signed",
            "required_inputs": "linear holonomy/additivity; single channel; no integrated tower; no marker prefactor",
            "source_path": str(RESIDUALS / "P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv"),
            "units": "not_applicable_if_zero",
            "current_status": "ZERO_THEOREM_UNSIGNED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "R2B1821_1_c_R2_eff",
            "row_type": "finite_scalar_mode_input",
            "quantity": "c_R2_eff_or_f_RR",
            "formula_or_value": "MISSING_PARENT_INPUT",
            "required_inputs": "numeric or symbolic parent coefficient; sign; normalization relative to EH term; source path",
            "source_path": "",
            "units": "length_squared_after_EH_normalization",
            "current_status": "MISSING_PARENT_COEFFICIENT",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "R2B1821_2_lambda_alpha",
            "row_type": "finite_scalar_mode_map",
            "quantity": "lambda_s_and_alpha_s",
            "formula_or_value": "lambda_s=sqrt(6 c_R2_eff); alpha_s=1/3 only for simple unscreened metric f(R)",
            "required_inputs": "positive c_R2_eff; matter coupling theorem; screening/environment flag; unit conversion",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1820_C_EH_FIRST_ROW_SCHEMA.csv"),
            "units": "meters_and_dimensionless",
            "current_status": "MISSING_COEFFICIENT_AND_COUPLING_REGIME",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "R2B1821_3_C_EH",
            "row_type": "charge_residual_component",
            "quantity": "epsilon_C_EH_R2FR_abs",
            "formula_or_value": "abs(int_A C_EH[R2FR])/M_H_ref",
            "required_inputs": "source curvature scale; annulus normalizer; operator coefficient; no-cancellation guard",
            "source_path": "",
            "units": "dimensionless_charge_fraction",
            "current_status": "MISSING_NORMALIZER_AND_SOURCE_SCALE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "R2B1821_4_bound_source",
            "row_type": "external_bound_source",
            "quantity": "alpha_bound(lambda)",
            "formula_or_value": "Lee2020/Eot-Wash anchor exists in prior template, but full digitized curve and arena response are still required for claim",
            "required_inputs": "digitized bound curve; provenance; lambda units; alpha convention; valid_for_claim source flag",
            "source_path": str(RESIDUALS / "P8_Y5_R10_964_R2FR_NONCLAIM_INPUT_TEMPLATE.csv"),
            "units": "dimensionless_alpha_vs_length",
            "current_status": "ANCHOR_ONLY_NONCLAIM_FULL_CURVE_REQUIRED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "R2B1821_5_total",
            "row_type": "R2FR_bound_row_contract",
            "quantity": "finite_R2FR_scalar_mode_score_row",
            "formula_or_value": "valid only if coefficient, lambda, alpha, screening, C_EH normalizer, weak-field map and full bound source are all real",
            "required_inputs": "R2B1821_1 through R2B1821_4 plus PPN/clock/orbital response maps",
            "source_path": "",
            "units": "row_contract",
            "current_status": "MISSING_PARENT_AND_ARENA_INPUTS_ROW_NONCLAIM",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1821_0_EH_plus_R2",
            "countermodel": "S = S_EH + epsilon int sqrt(-g) R2 with epsilon small",
            "why_it_survives": "covariant and local unless parent proves linear curvature response or zero coefficient",
            "blocked_by": "linear-holonomy/additive-cell theorem or finite bound row",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1821_1_aux_scalar",
            "countermodel": "hidden scalar integrates out to R2",
            "why_it_survives": "a visible metric-only ansatz can be misleading after reduction",
            "blocked_by": "no-integrated-out-tower theorem or source c_R2_eff",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1821_2_marker_curvature",
            "countermodel": "F(sigma)R or F(sigma)R2 from a local quotient-invariant marker",
            "why_it_survives": "covariant markers are not excluded by fixed-spurion logic",
            "blocked_by": "primitive quotient/no-natural-marker theorem",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1821_3_nonlocal_memory",
            "countermodel": "R Box^-1 R or compact memory kernel",
            "why_it_survives": "sector reduction has not proven memory/kernel silence",
            "blocked_by": "memory no-hair theorem or kernel norm row",
            "retained": True,
            "valid_for_claim": False,
        },
    ]


def gr_newton_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1821_0_if_linear_holonomy_closes",
            "if_closed": "LHC1821_0 through LHC1821_4 parent-sign",
            "would_buy": "a real derivation route to EH operator linearity without merely assuming second order",
            "still_missing": "connection/Levi-Civita, source equality, boundary/projector and C_extra gates",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1821_1_if_R2FR_zero_closes",
            "if_closed": "R2/fR scalar branch is theorem-zero",
            "would_buy": "one major non-EH scalar-mode obstruction to local GR/Newton is removed",
            "still_missing": "other R11 families and source/PPN calibration remain",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1821_2_if_finite_row_filled",
            "if_closed": "finite R2/fR row becomes source-backed",
            "would_buy": "MTS can honestly test or bound the scalar-mode leakage instead of hiding it",
            "still_missing": "full alpha(lambda) curve, PPN response, clocks/orbits and parent coefficient",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1821_3_verdict",
            "if_closed": "1821 alone proves GR/Newton",
            "would_buy": "nothing claimable alone; this is one left-hand-operator subgate",
            "still_missing": "current 1821 leaves no-higher-derivative proof unsigned and bound row nonclaim",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1821_0_contract_written",
            "gate": "no-higher-derivative theorem route sharpened",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "1821 reduces the vague minimality demand to linear holonomy/additivity plus no hidden tower/no marker",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1821_1_linear_holonomy_signed",
            "gate": "linear holonomy/additive-cell axiom parent-derived",
            "current_status": "BLOCKED",
            "reason": "the current corpus has not derived C(F1+F2)=C(F1)+C(F2) from MTS primitives",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1821_2_no_hidden_tower",
            "gate": "integrated-out curvature tower forbidden",
            "current_status": "BLOCKED",
            "reason": "hidden scalar, memory, projector and marker countermodels remain live",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1821_3_R2FR_bound_row",
            "gate": "finite R2/fR row source-backed",
            "current_status": "BLOCKED",
            "reason": "parent coefficient, coupling, normalizer and full bound curve are missing",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1821_4_local_GR_Newton",
            "gate": "local GR/Newton promotion allowed",
            "current_status": "REFUSED",
            "reason": "one operator subgate remains unresolved and broader C-term/source gates remain open",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1821_0_no_higher_derivative",
            "claim": "MTS parent action forbids all higher-curvature local operators",
            "status": "BLOCKED",
            "reason": "linear holonomy/additivity and no-hidden-tower clauses are not parent-signed",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1821_1_R2FR_zero",
            "claim": "R2/fR scalar-mode coefficient is zero",
            "status": "BLOCKED",
            "reason": "R2Z962 relative theorem still lacks the parent activator",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1821_2_R2FR_score",
            "claim": "finite R2/fR row can be scored against R10/PPN",
            "status": "REFUSED",
            "reason": "bound row remains missing parent and arena inputs",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1821_3_local_GR",
            "claim": "local GR/Newton is derived",
            "status": "REFUSED",
            "reason": "1821 is not the whole GR/Newton bridge and does not close its own R2/fR gate",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1821_0_theorem_result",
            "decision": "NO_HIGHER_DERIVATIVE_THEOREM_NOT_PROVEN",
            "reason": "the route is now sharper, but the additive linear-holonomy and no-hidden-tower clauses are not derived from current MTS primitives",
            "next_action": "do not claim EH/local GR; keep R2/fR residual explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1821_1_real_gain",
            "decision": "BEST_PROOF_TARGET_IDENTIFIED",
            "reason": "R2/fR can be excluded cleanly if MTS proves primitive cell additivity/linearity rather than merely preferring second-order equations",
            "next_action": "attack linear holonomy/additive-cell axiom directly",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1821_2_fallback",
            "decision": "R2FR_BOUND_ROW_SCHEMA_READY_NONCLAIM",
            "reason": "if the linearity theorem fails, the scalar mode has a strict coefficient/range/coupling/bound row contract",
            "next_action": "source no finite row until coefficient, units, coupling, normalizer and bounds are real",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1821_3_best_next",
            "decision": "LINEAR_HOLONOMY_PARENT_AXIOM_NEXT",
            "reason": "this is the least ad hoc route: derive why the local action is linear in curvature from primitive motion-time-space composition/additivity",
            "next_action": "1822-Y5-R2FR-linear-holonomy-parent-axiom-or-R2FR-coefficient-owner-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1821_0_primary",
            "next_target": "1822-Y5-R2FR-linear-holonomy-parent-axiom-or-R2FR-coefficient-owner-row.md",
            "script": "scripts/Y5_R2FR_linear_holonomy_parent_axiom_or_R2FR_coefficient_owner_row.py",
            "objective": "derive the primitive additivity/linear-holonomy axiom that would forbid quadratic curvature response; if not, convert c_R2/f_RR into an explicit coefficient-owner row",
            "selection_status": "selected",
            "success_condition": "parent-signed linearity theorem, or a nonclaim coefficient-owner row with all missing inputs explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1821_1_parallel",
            "next_target": "1822b-Y5-R2FR-full-bound-source-and-response-map-intake.md",
            "script": "scripts/Y5_R2FR_full_bound_source_and_response_map_intake.py",
            "objective": "acquire full alpha(lambda) bound and weak-field response map only if finite R2/fR branch survives",
            "selection_status": "held_parallel",
            "success_condition": "full curve, units, provenance, alpha convention and response map parse with valid_for_claim=false until parent coefficient exists",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "minimality_theorem": minimality_theorem_rows(),
        "linear_holonomy_contract": linear_holonomy_rows(),
        "integrated_tower_audit": integrated_tower_rows(),
        "bound_row_schema": bound_row_rows(),
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
    allowed_gate_pass = {"AC1821_0_contract_written"}
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
                or (boolish(row.get("gate_pass", False)) and row.get("gate_id") != "AC1821_0_contract_written")
            ):
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    exists_ok = all(boolish(row["exists"]) for row in source_rows)
    needles_ok = all(boolish(row["needles_present"]) for row in source_rows)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1821_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1821_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1821_2_minimality_route_written",
            any(row["theorem_id"] == "NHD1821_0_target" and row["attempt_result"] == "TARGET_RESTATED_WITH_STRONGER_LINEARITY_ROUTE" for row in rows_map["minimality_theorem"]),
            "no-higher-derivative parent minimality route is written",
        ),
        (
            "VAL1821_3_linear_holonomy_selected",
            any(row["theorem_id"] == "NHD1821_2_linear_holonomy_route" and row["current_status"] == "LINEARITY_AXIOM_NOT_PARENT_DERIVED" for row in rows_map["minimality_theorem"]),
            "linear holonomy/additive-cell route is identified but unsigned",
        ),
        (
            "VAL1821_4_theorem_not_promoted",
            any(row["theorem_id"] == "NHD1821_7_verdict" and row["attempt_result"] == "CONDITIONAL_ROUTE_NOT_CURRENT_PROOF" for row in rows_map["minimality_theorem"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["minimality_theorem"]),
            "1821 theorem is not promoted as current proof",
        ),
        (
            "VAL1821_5_linear_contract_nonclaim",
            any(row["contract_id"] == "LHC1821_4_failure_mode" and row["current_status"] == "UNSIGNED_THEREFORE_R2FR_RETAINED" for row in rows_map["linear_holonomy_contract"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["linear_holonomy_contract"]),
            "linear holonomy contract remains nonclaim",
        ),
        (
            "VAL1821_6_tower_audit_blocked",
            any(row["audit_id"] == "ITA1821_4_total" and row["current_status"] == "FAIL_NO_INTEGRATED_TOWER_PROOF" for row in rows_map["integrated_tower_audit"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["integrated_tower_audit"]),
            "integrated tower audit remains blocked and nonclaim",
        ),
        (
            "VAL1821_7_bound_rows_nonclaim",
            any(row["row_id"] == "R2B1821_5_total" and row["current_status"] == "MISSING_PARENT_AND_ARENA_INPUTS_ROW_NONCLAIM" for row in rows_map["bound_row_schema"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["bound_row_schema"]),
            "R2/fR bound rows are schema-only and nonclaim",
        ),
        (
            "VAL1821_8_countermodels_retained",
            all(boolish(row["retained"]) and not boolish(row["valid_for_claim"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain retained",
        ),
        (
            "VAL1821_9_gr_newton_nonclaim",
            all(not boolish(row["claim_allowed_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["gr_newton_impact"]),
            "GR/Newton impact rows remain nonclaim",
        ),
        (
            "VAL1821_10_acceptance_blocks",
            any(row["gate_id"] == "AC1821_0_contract_written" and boolish(row["gate_pass"]) and not boolish(row["claim_allowed"]) for row in rows_map["acceptance_gate"])
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["acceptance_gate"]),
            "acceptance gate permits contract-only progress and blocks claims",
        ),
        (
            "VAL1821_11_claim_gates_blocked",
            all(row["status"] in {"BLOCKED", "REFUSED"} and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all no-higher-derivative/R2FR/local-GR claim gates remain blocked or refused",
        ),
        ("VAL1821_12_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1821_13_missing_not_ready", missing_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1821_14_decision_next",
            any(row["decision_id"] == "DEC1821_3_best_next" and row["decision"] == "LINEAR_HOLONOMY_PARENT_AXIOM_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects linear holonomy parent axiom next",
        ),
        (
            "VAL1821_15_next_selected",
            any(row["route_id"] == "NEXT1821_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1821_16_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1821 CSVs parse"),
        ("VAL1821_17_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1821_18_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1821_19_formalization_untouched", formalization_untouched(), "no 1821 outputs found under formalization-workbench"),
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
            "check_id": "VAL1821_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1821 no-higher-derivative parent minimality or R2FR bound row checkpoint",
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
            "# 1821 Y5 R2FR no higher derivative parent minimality or R2FR bound row",
            "",
            "**Progress:** 1821 takes the derivation-first route seriously. It does not just repeat that higher derivatives are bad; it isolates the cleaner thing MTS would need to prove: primitive local action additivity/linear holonomy, plus no hidden tower and no marker-prefactor route.",
            "",
            "**Current verdict:** not a proof yet, but a sharper target. The R2/fR scalar branch would be killed if MTS can prove the primitive local response is additive and linear in curvature flux. The current corpus has not derived that axiom, so R2/fR remains retained as a nonclaim `C_EH/R11` scalar-mode row.",
            "",
            "**Claim ceiling:** no no-higher-derivative theorem claim, no R2/fR zero claim, no finite scalaron score, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1821.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## No Higher Derivative Parent Minimality Theorem",
            markdown_table(rows_map["minimality_theorem"], ["theorem_id", "claim_piece", "mathematical_statement", "attempt_result", "current_status", "would_close", "valid_for_claim"]),
            "",
            "## Linear Holonomy Derivation Contract",
            markdown_table(rows_map["linear_holonomy_contract"], ["contract_id", "needed_clause", "formal_condition", "reason_it_helps", "current_status", "valid_for_claim"]),
            "",
            "## No Integrated Tower Audit",
            markdown_table(rows_map["integrated_tower_audit"], ["audit_id", "sector", "escape_formula", "current_status", "needed_zero_or_bound", "score_ready", "valid_for_claim"]),
            "",
            "## R2FR Bound Row Schema",
            markdown_table(rows_map["bound_row_schema"], ["row_id", "row_type", "quantity", "formula_or_value", "required_inputs", "source_path", "units", "current_status", "score_ready", "valid_for_claim"]),
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
            "This is probably the best route of attack for the GR/Newton bridge. If MTS can derive primitive cell additivity and linear curvature response, then EH stops looking imported and starts looking forced. If it cannot, the theory is still not dead, but it must carry R2/fR as a quantified modified-gravity residual and beat/bound it honestly.",
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
    print(f"1821 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
