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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1788"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1788_0_1787_handoff",
        "source_key": "1787_handoff_doc",
        "source_path": ROOT / "1787-Y5-R2FR-hybrid-EH-plus-quotient-extra-local-action-split-and-extra-sector-silence.md",
        "needles": ["DEC1787_1_first_target", "NEXT1787_0_primary", "VAL1787_OVERALL"],
    },
    {
        "source_id": "SRC1788_1_1787_validation",
        "source_key": "1787_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1787_VALIDATION.csv",
        "needles": ["VAL1787_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1788_2_1787_conditional",
        "source_key": "1787_conditional_reduction",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1787_CONDITIONAL_REDUCTION_THEOREM.csv",
        "needles": ["HCT1787_3_R2FR_relative_result", "HCT1787_4_verdict"],
    },
    {
        "source_id": "SRC1788_3_959_no_extra",
        "source_key": "959_no_extra_field",
        "source_path": RESIDUALS / "P8_Y5_R10_959_NO_EXTRA_FIELD_CLAUSE_ATTEMPT.csv",
        "needles": ["NEF959_0_target", "NEF959_5_verdict"],
    },
    {
        "source_id": "SRC1788_4_959_silence",
        "source_key": "959_silence_requirements",
        "source_path": RESIDUALS / "P8_Y5_R10_959_SILENCE_MECHANISM_REQUIREMENTS.csv",
        "needles": ["SMR959_0_operator", "SMR959_4_retained_vector"],
    },
    {
        "source_id": "SRC1788_5_960_r2fr",
        "source_key": "960_r2fr",
        "source_path": RESIDUALS / "P8_Y5_R10_960_R2_FR_ZERO_OR_BOUND_ATTEMPT.csv",
        "needles": ["R2FR960_0_target", "R2FR960_4_verdict"],
    },
    {
        "source_id": "SRC1788_6_962_r2fr_proof",
        "source_key": "962_r2fr_zero_proof",
        "source_path": RESIDUALS / "P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv",
        "needles": ["R2Z962_0_target", "R2Z962_5_relative_zero_theorem"],
    },
    {
        "source_id": "SRC1788_7_962_scalar_fallback",
        "source_key": "962_scalar_bound_fallback",
        "source_path": RESIDUALS / "P8_Y5_R10_962_SCALAR_BOUND_FALLBACK_ROWS.csv",
        "needles": ["R2B962_0_parent_zero_route", "R2B962_4_Cassini_gamma_anchor"],
    },
    {
        "source_id": "SRC1788_8_963_derivative",
        "source_key": "963_derivative_order",
        "source_path": RESIDUALS / "P8_Y5_R10_963_DERIVATIVE_ORDER_AUDIT.csv",
        "needles": ["DO963_0_962_relative_theorem", "DO963_6_verdict"],
    },
    {
        "source_id": "SRC1788_9_963_runner_spec",
        "source_key": "963_r2fr_runner_spec",
        "source_path": RESIDUALS / "P8_Y5_R10_963_R2FR_BOUND_RUNNER_SPEC.csv",
        "needles": ["R2RUN963_0_model_input", "R2RUN963_4_decision_logic"],
    },
    {
        "source_id": "SRC1788_10_964_minimality",
        "source_key": "964_minimality",
        "source_path": RESIDUALS / "P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
        "needles": ["MIN964_0_target", "MIN964_5_verdict"],
    },
    {
        "source_id": "SRC1788_11_964_template",
        "source_key": "964_r2fr_input_template",
        "source_path": RESIDUALS / "P8_Y5_R10_964_R2FR_NONCLAIM_INPUT_TEMPLATE.csv",
        "needles": ["R2IN964_0_mts_prediction_required", "R2IN964_3_full_curve_required"],
    },
    {
        "source_id": "SRC1788_12_964_runner",
        "source_key": "964_r2fr_runner_result",
        "source_path": RESIDUALS / "P8_Y5_R10_964_R2FR_NONCLAIM_RUNNER_RESULT.csv",
        "needles": ["R2RUN964_0_mts_prediction_required", "R2RUN964_VERDICT"],
    },
    {
        "source_id": "SRC1788_13_965_primitive",
        "source_key": "965_primitive_quotient",
        "source_path": RESIDUALS / "P8_Y5_R10_965_PRIMITIVE_QUOTIENT_THEOREM_ATTEMPT.csv",
        "needles": ["PQ965_0_theorem_target", "PQ965_5_verdict"],
    },
    {
        "source_id": "SRC1788_14_965_curve_manifest",
        "source_key": "965_full_curve_manifest",
        "source_path": RESIDUALS / "P8_Y5_R10_965_R2FR_FULL_CURVE_INTAKE_MANIFEST.csv",
        "needles": ["R2FC965_0_Lee2020_full_curve_required", "R2FC965_5_runner_acceptance_rule"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1788_SOURCE_REGISTER.csv",
    "relative_theorem_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1788_R2FR_RELATIVE_THEOREM_REGISTER.csv",
    "parent_premise_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1788_PARENT_PREMISE_ACTIVATION_GATE.csv",
    "premise_counterexample_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1788_PREMISE_COUNTEREXAMPLE_AUDIT.csv",
    "finite_bound_fallback": RESIDUALS / "P8_Y5_PARENT_QLOC_1788_R2FR_FINITE_BOUND_FALLBACK.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1788_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1788_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1788_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1788_VALIDATION.csv",
}

DOC_PATH = ROOT / "1788-Y5-R2FR-parent-second-order-no-extra-scalar-premise-or-R2FR-bound-row.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
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
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and all(needle in text for needle in needles),
                "role": "1788 R2/fR parent-premise activation and finite scalar fallback evidence",
            }
        )
    return rows


def relative_theorem_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "RZT1788_0_setup",
            "piece": "local f(R) expansion",
            "mathematical_form": "L = sqrt(-g) f(R), f(R)=a0+a1 R+a2 R^2+O(R^3)",
            "result": "SETUP_IMPORTED",
            "source_basis": "R2Z962_0_target",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "RZT1788_1_scalar_pole",
            "piece": "nonlinear f(R) carries scalar trace mode",
            "mathematical_form": "for R+aR^2 around flat space: (Box - 1/(6a)) delta R = -kappa T/(6a)",
            "result": "RELATIVE_THEOREM_STEP_PASS",
            "source_basis": "R2Z962_2_trace_scalar_pole",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "RZT1788_2_topological_escape",
            "piece": "isolated R2/fR is not generically topological",
            "mathematical_form": "4D Gauss-Bonnet may be topological, but isolated R^2 or generic f(R) is not the GB density",
            "result": "ESCAPE_FAILS_CURRENT_ROW",
            "source_basis": "R2Z962_3_topological_escape",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "RZT1788_3_field_redefinition_escape",
            "piece": "field redefinition redundancy is not certified",
            "mathematical_form": "a redefinition cannot move leakage into matter couplings, source normalization, clocks, or PPN readout",
            "result": "ESCAPE_NOT_CERTIFIED",
            "source_basis": "R2Z962_4_field_redefinition_escape",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "RZT1788_4_relative_zero",
            "piece": "relative zero theorem",
            "mathematical_form": "4D local diffeo metric-only second-order equations plus no retained scalar => f_RR=0 and c_R2=c_fR=0",
            "result": "RELATIVE_THEOREM_PROVEN_PARENT_PREMISE_UNSIGNED",
            "source_basis": "R2Z962_5_relative_zero_theorem;HCT1787_3_R2FR_relative_result",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "RZT1788_5_verdict",
            "piece": "absolute MTS R2/fR zero theorem",
            "mathematical_form": "RZT1788_0 through RZT1788_4 plus parent premise gate closes",
            "result": "RELATIVE_READY_ABSOLUTE_NOT_CLAIMED",
            "source_basis": "962/963/964/965 chain",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def parent_premise_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PPG1788_0_local_4D_domain",
            "required_premise": "ordinary compact exterior branch is local and 4D",
            "mathematical_form": "S_ext[g_obs] is a local 4D diffeomorphism-invariant exterior action through the local test order",
            "current_status": "CONDITIONAL_BRANCH_LANGUAGE_ONLY",
            "blocker": "domain/boundary/projector selection remains parent-open",
            "would_activate": "Lovelock/EH operator route if other premises pass",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PPG1788_1_metric_only",
            "required_premise": "only observed metric/coframe is locally dynamical",
            "mathematical_form": "Fields_ext={g_obs/e_obs}; connection, scalar/class, memory, projector, and domain variables are absent/gauge/topological/silent",
            "current_status": "NOT_PARENT_SIGNED",
            "blocker": "connection, projector, scalar/class, memory/domain, and matter-frame sectors remain legal or retained",
            "would_activate": "metric-only half of R2/fR and EH theorem",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PPG1788_2_second_order",
            "required_premise": "local metric equations are exactly second order",
            "mathematical_form": "delta S_ext/delta g_obs contains no fourth-order metric equation and no finite scalar pole",
            "current_status": "NOT_PARENT_SIGNED",
            "blocker": "no parent rule forbids higher-curvature or integrated-out effective curvature tower",
            "would_activate": "f_RR=0 in the relative theorem",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PPG1788_3_no_extra_scalar",
            "required_premise": "no retained scalar/class/readout marker couples to R or matter locally",
            "mathematical_form": "no scalar R-prefactor, no local kinetic scalar, no quotient-invariant material marker, no finite scalar pole",
            "current_status": "NOT_PARENT_SIGNED",
            "blocker": "primitive quotient/no-natural-marker theorem and local invariant algebra triviality are not derived",
            "would_activate": "no scalar-tensor/f(R)-like leakage",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PPG1788_4_no_integrated_out_tower",
            "required_premise": "solving hidden sectors cannot regenerate R2/fR/nonlocal curvature terms",
            "mathematical_form": "integrating out auxiliary/projector/memory/scalar sectors contributes no Delta S_eff[g] with R^2, f(R), Yukawa, or nonlocal kernel",
            "current_status": "KEY_BLOCKER_NOT_DERIVED",
            "blocker": "E_A=0 or large mass is not enough unless metric variation and matter/readout source are silent",
            "would_activate": "prevents R2/fR from returning after reduction",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PPG1788_5_boundary_readout_invariance",
            "required_premise": "boundary and readout terms cannot carry the scalar curvature mode",
            "mathematical_form": "boundary/reference/readout equivalence is invariant under any attempted removal of R2/fR",
            "current_status": "NOT_CERTIFIED",
            "blocker": "field-redefinition and boundary zero-flux certificates are not present",
            "would_activate": "keeps zero theorem from hiding leakage in observables",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PPG1788_6_verdict",
            "required_premise": "parent premise activates the relative R2/fR zero theorem",
            "mathematical_form": "PPG1788_0 through PPG1788_5 all parent-signed",
            "current_status": "PARENT_PREMISE_NOT_ACTIVATED",
            "blocker": "metric-only, second-order, no-extra-scalar, no-integrated-out-tower, and boundary/readout invariance are unsigned",
            "would_activate": "absolute c_R2=c_fR=0",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def premise_counterexample_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "PCA1788_0_integrated_out_scalar",
            "countermodel": "hidden scalar or memory sector is eliminated but leaves an effective R2/fR/Yukawa term",
            "survives_current_constraints": True,
            "why_survives": "MIN964_2 says no-integrated-out tower is not derived",
            "what_kills_it": "parent no-integrated-out-curvature-tower theorem or finite scalar bound row",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "PCA1788_1_marker_scalar",
            "countermodel": "primitive quotient is extended by a covariant scalar/material marker that couples to R or matter",
            "survives_current_constraints": True,
            "why_survives": "PQ965_5 keeps primitive/no-marker theorem unproven",
            "what_kills_it": "primitive minimal quotient theorem and local invariant algebra triviality",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "PCA1788_2_boundary_redefinition_leak",
            "countermodel": "R2/fR is field-redefined away in bulk but reappears in boundary/readout/source normalization",
            "survives_current_constraints": True,
            "why_survives": "R2Z962_4 says field-redefinition redundancy is not certified",
            "what_kills_it": "readout and boundary invariance certificate",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "PCA1788_3_connection_disguise",
            "countermodel": "independent connection or nonmetricity makes equations look metric-only after projection but keeps scalar/vector residues",
            "survives_current_constraints": True,
            "why_survives": "connection gate remains open in 960 and 1787",
            "what_kills_it": "Levi-Civita/no-hypermomentum theorem or P4 residual bounds",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "PCA1788_4_anchor_only_false_pass",
            "countermodel": "R10 alpha(lambda) anchor is mistaken for a full bound curve score",
            "survives_current_constraints": True,
            "why_survives": "965 curve manifest says full curve is not acquired",
            "what_kills_it": "digitized/machine-readable alpha(lambda) curve plus numeric MTS alpha/lambda prediction",
        },
    ]


def finite_bound_fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "R2F1788_0_zero_route",
            "row_type": "zero_theorem",
            "model_id": "MTS_R2FR_zero_route",
            "required_parent_inputs": "parent exact local second-order metric-only no-extra-scalar action signature",
            "alpha_predicted": "0_if_parent_signed_else_MISSING",
            "lambda_predicted_um": "not_applicable_if_zero",
            "status": "ZERO_THEOREM_UNSIGNED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "R2F1788_1_finite_scalar_prediction",
            "row_type": "mts_prediction",
            "model_id": "MTS_R2FR_retained_scalar_branch",
            "required_parent_inputs": "c_R2_or_fRR; normalization; screening flag; source coupling; scalar mass",
            "alpha_predicted": "MISSING_ALPHA_OR_PARENT_COEFFICIENT",
            "lambda_predicted_um": "MISSING_LAMBDA_OR_MASS",
            "status": "MISSING_PARENT_INPUT",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "R2F1788_2_full_curve_required",
            "row_type": "bound_curve",
            "model_id": "external_R10_alpha_lambda_curve",
            "required_parent_inputs": "positive numeric lambda/alpha bound rows with source path and extraction method",
            "alpha_predicted": "not_applicable",
            "lambda_predicted_um": "MISSING_DIGITIZED_CURVE",
            "status": "FULL_CURVE_REQUIRED_NOT_ACQUIRED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "R2F1788_3_anchor_smoke_only",
            "row_type": "anchor_only_non_curve",
            "model_id": "Lee2020_and_Kapner2007_anchor_smoke",
            "required_parent_inputs": "not for claim; regression sanity only",
            "alpha_predicted": "anchor_only",
            "lambda_predicted_um": "38.6_or_56_anchor_only",
            "status": "ANCHOR_RECORDED_NONCLAIM",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "R2F1788_4_runner_policy",
            "row_type": "acceptance_gate",
            "model_id": "strict_R2FR_nonclaim_runner",
            "required_parent_inputs": "zero theorem signed OR numeric prediction plus full valid bound curve",
            "alpha_predicted": "MISSING",
            "lambda_predicted_um": "MISSING",
            "status": "R2FR_BRANCH_BLOCKED_NONCLAIM",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1788_0_zero_theorem_claim",
            "claim": "c_R2=c_fR=0 is derived for MTS",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "parent premise not activated",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1788_1_second_order_claim",
            "claim": "MTS local exterior is metric-only and second-order",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "no-integrated-out tower and no-extra-scalar clauses are not derived",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1788_2_finite_scalar_score_claim",
            "claim": "retained R2/fR scalar branch is score-ready against R10/PPN",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "missing parent coefficient/mass/coupling and full alpha(lambda) curve",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1788_3_local_GR_claim",
            "claim": "local GR/Newton branch follows from this checkpoint",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "R2/fR remains one open component of the larger 1787 silence matrix",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1788_0_relative_status",
            "decision": "R2FR_RELATIVE_ZERO_THEOREM_RETAINED",
            "reason": "the conditional scalar-pole theorem is useful and mathematically sharp",
            "next_action": "do not demote it; keep trying to activate its parent premise",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1788_1_parent_status",
            "decision": "PARENT_SECOND_ORDER_NO_EXTRA_SCALAR_PREMISE_NOT_ACTIVATED",
            "reason": "no-integrated-out tower, primitive quotient/no-marker, metric-only, and boundary/readout invariance are unsigned",
            "next_action": "attack no-integrated-out curvature tower as the narrowest missing premise",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1788_2_fallback_status",
            "decision": "FINITE_SCALAR_BOUND_ROUTE_STAGED_NONCLAIM",
            "reason": "if the zero theorem fails, the R2/fR scalar must be bounded with real parent coefficients and full curve data",
            "next_action": "do not score anchor-only data or placeholder MTS rows",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1788_0_primary",
            "next_target": "1789-Y5-R2FR-no-integrated-out-curvature-tower-or-finite-scalar-bound-pack.md",
            "script": "scripts/Y5_R2FR_no_integrated_out_curvature_tower_or_finite_scalar_bound_pack.py",
            "objective": "try to prove eliminated MTS sectors cannot generate R2/fR, Yukawa, nonlocal, or scalar-tensor effective curvature terms; if not, prepare finite scalar bound inputs",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1788_1_parallel",
            "next_target": "1789b-Y5-R2FR-primitive-quotient-no-natural-marker-local-invariant-algebra.md",
            "script": "scripts/Y5_R2FR_primitive_quotient_no_natural_marker_local_invariant_algebra.py",
            "objective": "prove no quotient-invariant scalar/material marker can couple to local curvature or matter, or retain marker residual rows",
            "selection_status": "queued_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1788_2_fallback",
            "next_target": "1789c-Y5-R2FR-full-alpha-lambda-curve-and-MTS-scalar-prediction-pack.md",
            "script": "scripts/Y5_R2FR_full_alpha_lambda_curve_and_MTS_scalar_prediction_pack.py",
            "objective": "acquire full source-backed alpha(lambda) curve and require numeric MTS scalar mass/coupling before any R2/fR score",
            "selection_status": "deferred_until_zero_route_fails",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "relative_theorem_register": relative_theorem_register_rows(),
        "parent_premise_gate": parent_premise_gate_rows(),
        "premise_counterexample_audit": premise_counterexample_audit_rows(),
        "finite_bound_fallback": finite_bound_fallback_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def fieldnames_for(rows: list[dict[str, Any]]) -> list[str]:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    return fieldnames


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames_for(rows))
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
        shutil.copy2(path, RAB_QUEUE / f"JR1788_{key.upper()}.csv")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "pass", "passed"}


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return (
        all(boolish(row["exists"]) for row in rows),
        all(boolish(row["needles_present"]) for row in rows),
    )


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for flag in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "accepted_for_scoring",
                "theorem_closed_for_claim",
                "parent_signed",
                "valid_prediction_row",
                "gate_pass",
            ):
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                for flag in (
                    "valid_for_claim",
                    "claim_allowed",
                    "score_ready",
                    "accepted_for_scoring",
                    "theorem_closed_for_claim",
                    "valid_prediction_row",
                    "gate_pass",
                ):
                    if boolish(row.get(flag, False)):
                        return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not (MICROSCOPE_RESIDUALS / path.name).exists():
            return False
        if not (QUARANTINE / path.name).exists():
            return False
        if not (RAB_QUEUE / f"JR1788_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add(DOC_PATH.name)
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1788_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1788_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1788_2_relative_theorem_retained",
            any(
                row["theorem_id"] == "RZT1788_4_relative_zero"
                and row["result"] == "RELATIVE_THEOREM_PROVEN_PARENT_PREMISE_UNSIGNED"
                for row in rows_map["relative_theorem_register"]
            ),
            "relative R2/fR zero theorem is retained without promotion",
        ),
        (
            "VAL1788_3_parent_premise_not_activated",
            any(
                row["premise_id"] == "PPG1788_6_verdict"
                and row["current_status"] == "PARENT_PREMISE_NOT_ACTIVATED"
                for row in rows_map["parent_premise_gate"]
            )
            and all(not boolish(row["parent_signed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["parent_premise_gate"]),
            "parent premise gate is explicit and unsigned",
        ),
        (
            "VAL1788_4_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["premise_counterexample_audit"]),
            "premise countermodels remain live",
        ),
        (
            "VAL1788_5_fallback_nonclaim",
            all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["finite_bound_fallback"]),
            "finite scalar fallback rows remain nonclaim and not score-ready",
        ),
        (
            "VAL1788_6_claim_gates_blocked",
            all(
                not boolish(row["valid_for_claim"])
                and not boolish(row["gate_pass"])
                and row["status"] == "BLOCKED"
                for row in rows_map["claim_gate"]
            ),
            "claim gates are blocked",
        ),
        ("VAL1788_7_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1788_8_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1788_9_decision_next",
            any(
                row["decision_id"] == "DEC1788_1_parent_status"
                and row["decision"] == "PARENT_SECOND_ORDER_NO_EXTRA_SCALAR_PREMISE_NOT_ACTIVATED"
                for row in rows_map["decision_ledger"]
            ),
            "decision records parent premise not activated",
        ),
        (
            "VAL1788_10_next_selected",
            any(row["route_id"] == "NEXT1788_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1788_11_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1788 CSVs parse"),
        ("VAL1788_12_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1788_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1788_14_formalization_untouched", formalization_untouched(), "no 1788 outputs found under formalization-workbench"),
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
            "check_id": "VAL1788_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1788 R2/fR parent-premise activation or finite scalar bound checkpoint",
        }
    )
    return rows


def clean_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(clean_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1788 - Y5/R2FR Parent Second-Order No-Extra-Scalar Premise or R2FR Bound Row",
            "",
            "## Verdict",
            "",
            "1788 keeps the good part: the R2/fR relative zero theorem is real as a conditional statement. If the parent local exterior is truly 4D, local, diffeomorphism-invariant, metric-only, second-order, and has no retained scalar/class mode, then the R2/fR scalar branch is killed.",
            "",
            "But MTS does not yet earn that premise. The live blockers are now precise: no-integrated-out curvature tower, primitive quotient/no-natural-marker theorem, metric-only connection/scalar silence, and boundary/readout invariance. So `c_R2=c_fR=0` is not claimable. The finite scalar branch is staged as nonclaim only and cannot be scored without real parent coefficients and a full `alpha(lambda)` curve.",
            "",
            "**Claim ceiling:** no R2/fR zero claim, no second-order parent claim, no scalar-mode score, no local-GR/Newton claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1788.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Relative Theorem Register",
            markdown_table(rows_map["relative_theorem_register"], ["theorem_id", "piece", "mathematical_form", "result", "source_basis", "valid_for_claim"]),
            "",
            "## Parent Premise Activation Gate",
            markdown_table(rows_map["parent_premise_gate"], ["premise_id", "required_premise", "mathematical_form", "current_status", "blocker", "would_activate", "valid_for_claim"]),
            "",
            "## Premise Counterexample Audit",
            markdown_table(rows_map["premise_counterexample_audit"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "",
            "## Finite Bound Fallback",
            markdown_table(rows_map["finite_bound_fallback"], ["row_id", "row_type", "model_id", "required_parent_inputs", "alpha_predicted", "lambda_predicted_um", "status", "score_ready", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a useful failure. We are not saying 'R2/fR is bad' by taste; we are saying exactly what parent theorem would kill it and exactly why MTS has not earned that theorem yet. The next clean derivation target is the no-integrated-out curvature tower clause, because that is where hidden sectors could sneak the scalar mode back in after we thought it was gone.",
            "",
        ]
    )


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1788 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
