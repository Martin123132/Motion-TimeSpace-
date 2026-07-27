from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2647-Y5-R2FR-ordinary-matter-action-signature-or-Delta-w-projection-kernels.md"

CHECKPOINT = "2647"
BRANCH_ID = "Y5_R2FR_ORDINARY_MATTER_SIGNATURE_OR_DELTAW_KERNELS_2647"
PREFIX = "P8_Y5_ORDINARY_MATTER_SIGNATURE_2647"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "signature_attempt": RESIDUALS / f"{PREFIX}_SIGNATURE_ATTEMPT.csv",
    "clause_matrix": RESIDUALS / f"{PREFIX}_CLAUSE_MATRIX.csv",
    "projection_kernels": RESIDUALS / f"{PREFIX}_DELTAW_PROJECTION_KERNELS_NONCLAIM.csv",
    "validator_cases": RESIDUALS / f"{PREFIX}_VALIDATOR_CASES.csv",
    "validator_results": RESIDUALS / f"{PREFIX}_VALIDATOR_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2647_ORDINARY_MATTER_SIGNATURE_DELTAW_KERNELS_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "Delta_w_projection_kernels_2647_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "DELTAW_PROJECTION_KERNELS2647_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2647_DELTAW_WEP_KERNELS_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2647_00_2646",
        "role": "immediate matter-normalization owner handoff",
        "path": ROOT / "2646-Y5-R2FR-matter-normalization-owner-or-Delta-w-species-coefficient-source-row.md",
        "needles": ["MNO2646_6_verdict", "DWS2646_0_delta_w_species", "VAL2646_OVERALL"],
    },
    {
        "source_id": "SRC2647_01_1892",
        "role": "older ordinary matter action signature and kernel stubs",
        "path": ROOT / "1892-Y5-R2FR-ordinary-matter-action-signature-or-deltaw-species-projection-kernels.md",
        "needles": ["OMAS1892_2_signature_not_signed", "DK1892_1_WEP", "VAL1892_OVERALL"],
    },
    {
        "source_id": "SRC2647_02_1088",
        "role": "minimal ordinary-matter signature clause",
        "path": ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
        "needles": ["MOMS1088_0_action_form", "MOMS1088_4_no_species_weights", "MOMS1088_7_verdict"],
    },
    {
        "source_id": "SRC2647_03_1045",
        "role": "matter bundle/functor signature",
        "path": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
        "needles": ["MFS1045_2_matter_bundle_functor", "REF1045_0_parent_functor"],
    },
    {
        "source_id": "SRC2647_04_1098",
        "role": "source-weight exclusion as ordinary constant owner clause",
        "path": ROOT / "1098-Y5-R10-ordinary-constant-owner-action-signature-or-source-backed-coefficient-prior.md",
        "needles": ["OCS1098_4_source_weight_exclusion", "UNSIGNED"],
    },
    {
        "source_id": "SRC2647_05_1897",
        "role": "Delta_w arena projection matrix lineage",
        "path": ROOT / "1897-Y5-R2FR-action-scale-readout-stability-or-deltaw-projection-matrix.md",
        "needles": ["DPM1897_1_WEP_MICROSCOPE", "DPM1897_2_R10", "VAL1897_OVERALL"],
    },
    {
        "source_id": "SRC2647_06_1914",
        "role": "finite residual branch no-cancellation interface",
        "path": ROOT / "1914-Y5-R2FR-finite-residual-branch-v0-no-cancellation-interface.md",
        "needles": ["ARI1914_WEP_MICROSCOPE_TiPt", "ARI1914_R10_short_range", "ARI1914_PPN_beta_gamma_source"],
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "valid_for_claim": "False",
        "claim_allowed": "False",
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        return bool(read_csv(path))
    except Exception:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    if columns is None:
        columns = []
        for row in rows:
            for key in row:
                if key not in columns:
                    columns.append(key)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2647_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2647-Y5-R2FR*",
        "*P8_Y5_ORDINARY_MATTER_SIGNATURE_2647*",
        "*P8_Y5_BRR545_2647*",
        "*Y5_R2FR_ordinary_matter_action_signature_or_Delta_w_projection_kernels_2647*",
        "*JR2647*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        text = read_text(source["path"])
        found = [needle for needle in source["needles"] if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                role=source["role"],
                source_path=str(source["path"]),
                path_exists=str(source["path"].exists()),
                required_needles=";".join(source["needles"]),
                found_needles=";".join(found),
                needles_present=str(source["path"].exists() and len(found) == len(source["needles"])),
            )
        )
    return rows


def signature_attempt_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            attempt_id="OMAS2647_0_target_signature",
            claim_piece="ordinary-matter action signature",
            formal_statement="S_matter=sum_A S_A[Psi_A; e_obs(q(Phi)), omega[e_obs], A_obs(q(Phi)), theta_A] with J_H=delta S_matter/delta e_obs before readout and no w_A/kappa_A source slot.",
            status="TARGET_SIGNATURE_SHARP",
            derivation_or_obstruction="exact signature needed for local GR/Newton source recovery and for killing Delta_w_species in Xi_JH_DqZ_A",
            source_anchor="1088:MOMS1088_0_action_form;2646:DWS2646_0_delta_w_species",
        ),
        base_row(
            attempt_id="OMAS2647_1_chain_rule_if_signed",
            claim_piece="local source silence theorem",
            formal_statement="For v in ker(Dq), if Lie_v e_obs=Lie_v A_obs=Lie_v theta_A=0 and the matter lift is fixed/gauge/boundary-only, then Lie_v S_matter is gauge/boundary-only and source weights have no legal slot.",
            status="EXACT_CONDITIONAL_THEOREM",
            derivation_or_obstruction="chain-rule route is mathematically clean but depends on all signature clauses simultaneously.",
            source_anchor="1045:MFS1045_2_matter_bundle_functor;1892:OMAS1892_1_chain_rule_if_signed",
        ),
        base_row(
            attempt_id="OMAS2647_2_parent_adoption_attempt",
            claim_piece="promote signature as current MTS parent action",
            formal_statement="The current parent action derives quotient geometry, matter bundle, vertical lift, fixed constants, no species weights, hbar/measure owner and readout/boundary silence in one package.",
            status="ORDINARY_MATTER_ACTION_SIGNATURE_NOT_PARENT_SIGNED",
            derivation_or_obstruction="clauses exist as contracts but not as a single derived parent action from MTS primitives.",
            source_anchor="1088:MOMS1088_7_verdict;2646:SOA2646_5_verdict",
        ),
        base_row(
            attempt_id="OMAS2647_3_kernel_fallback",
            claim_piece="Delta_w projection-kernel fallback",
            formal_statement="If the parent signature is unsigned, Delta_w_species must be projected into WEP, R10, PPN, clock and orbital arenas with explicit tau/K/Qbar/material kernels.",
            status="FALLBACK_KERNEL_CONTRACTS_REQUIRED_NONCLAIM",
            derivation_or_obstruction="projection kernels prepare testability but do not create a prediction until parent epsilon_A or theorem-zero exists.",
            source_anchor="2646:PRJ2646_1_WEP..PRJ2646_5_orbital;1897:DPM1897_1_WEP_MICROSCOPE..DPM1897_5_orbital",
        ),
    ]


def clause_matrix_rows() -> list[dict[str, Any]]:
    return [
        base_row(clause_id="OMC2647_0_quotient_object", signature_clause="parent quotient object and observed geometry", required_identity="q exists; v in ker(Dq); e_obs=E(q(Phi)); omega_obs=omega[e_obs] or owned connection", current_status="CONDITIONAL_SUPPORT_NOT_PARENT_COMPLETE", if_signed="visible geometry carries no representative motion", if_unsigned="frame/disformal/connection residuals remain live", source_anchor="1088:MOMS1088_1_quotient_observables"),
        base_row(clause_id="OMC2647_1_matter_bundle", signature_clause="ordinary matter bundle over observed geometry", required_identity="Psi_A in Gamma(E_A[e_obs,A_obs]) and S_A uses only observed geometry/gauge data plus theta_A", current_status="MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED", if_signed="matter frame/source split cannot be fitted later", if_unsigned="a hidden matter frame can mimic GR recovery", source_anchor="1045:MFS1045_2_matter_bundle_functor"),
        base_row(clause_id="OMC2647_2_vertical_lift", signature_clause="fixed/gauge ordinary-matter vertical lift", required_identity="delta_v Psi_A=0 or owned gauge/local-Lorentz/diffeomorphism lift with boundary-only variation", current_status="VERTICAL_LIFT_NOT_PARENT_SIGNED", if_signed="ordinary matter gets no physical representative source charge", if_unsigned="vertical motion can act as fifth-force/source label", source_anchor="1045:MFS1045_3_vertical_lift"),
        base_row(clause_id="OMC2647_3_constant_superselection", signature_clause="constants and representation standards", required_identity="Lie_v theta_A=0 for masses, charges, clocks, binding and labels, or the channel is retained as a finite residual", current_status="CONSTANT_SUPERSELECTION_UNSIGNED", if_signed="constant/material marker channels collapse", if_unsigned="WEP/clock/alpha/mass residuals remain active", source_anchor="1088:MOMS1088_3_constant_superselection"),
        base_row(clause_id="OMC2647_4_source_functor_label_forgetting", signature_clause="total Hilbert source before readout", required_identity="J_H=delta S_matter/delta e_obs with no pre-variation w_A, kappa_A, material selector or per-species source label", current_status="CONDITIONAL_LEMMA_NOT_PARENT_DERIVED", if_signed="Delta_w_species=0 follows from source grammar", if_unsigned="relative source weights remain the main coupling debt", source_anchor="1098:OCS1098_4_source_weight_exclusion;2646:MNO2646_6_verdict"),
        base_row(clause_id="OMC2647_5_hbar_measure_action_scale", signature_clause="single action-scale/measure owner", required_identity="one hbar_parent and measure/action-density line for all ordinary sectors; no species-only Jacobian", current_status="OWNER_NOT_DERIVED", if_signed="action-scale prefactor cannot reappear as w_A S_A", if_unsigned="effective hbar_A/measure factors mimic Delta_w_species", source_anchor="2646:MNO2646_4_measure_action_density_line"),
        base_row(clause_id="OMC2647_6_no_shadow_boundary_readout", signature_clause="no shadow frame, marker, boundary, readout or EFT re-entry", required_identity="no hidden conformal/disformal frame, marker/domain selector, boundary local projection or post-readout source coefficient", current_status="BOUNDARY_AND_EFT_SILENCE_NOT_SIGNED", if_signed="bare parent signature survives local tests", if_unsigned="readout/boundary source terms can restore fifth-force pressure", source_anchor="2646:SOA2646_4_readout_radiative"),
        base_row(clause_id="OMC2647_7_verdict", signature_clause="ordinary matter action signature as current theorem", required_identity="OMC2647_0 through OMC2647_6 are derived from one parent action", current_status="ORDINARY_MATTER_SIGNATURE_NOT_DERIVED", if_signed="Delta_w_species and the source part of Xi_JH_DqZ_A theorem-zero", if_unsigned="finite Delta_w projection kernels remain mandatory", source_anchor="OMC2647_0 through OMC2647_6"),
    ]


def projection_kernel_rows() -> list[dict[str, Any]]:
    return [
        base_row(kernel_id="DK2647_0_core_vector", arena="core Delta_w vector", kernel_formula="epsilon_perp=P_perp epsilon, P_perp removes common calibration mode using sourced p_A", required_inputs="parent epsilon_A vector or theorem-zero; p_A basis; norm/no-cancellation policy", current_status="SYMBOLIC_KERNEL_ONLY_PARENT_COEFFICIENT_MISSING", units="dimensionless", score_ready="False", valid_prediction_row="False"),
        base_row(kernel_id="DK2647_1_WEP", arena="WEP_MICROSCOPE_TiPt", kernel_formula="eta_AB=tau_WEP*K_WEP[A,B,source,readout] dot epsilon_perp", required_inputs="test/source material tensor; tau_WEP; force/readout convention; parent epsilon_A vector", current_status="KERNEL_STUB_NONCLAIM_MATERIAL_TENSOR_AND_PARENT_VALUES_MISSING", units="dimensionless eta", score_ready="False", valid_prediction_row="False"),
        base_row(kernel_id="DK2647_2_R10", arena="R10_short_range", kernel_formula="alpha_Delta_w(lambda)=tau_R10(lambda)*K_R10(lambda)*Qbar_source_test(lambda) dot epsilon_perp", required_inputs="range kernel; source/test composition; tau_R10; K_R10; Qbar; real alpha_bound(lambda); parent epsilon_A vector", current_status="KERNEL_STUB_NONCLAIM_RANGE_KERNEL_AND_PARENT_VALUES_MISSING", units="dimensionless alpha(lambda)", score_ready="False", valid_prediction_row="False"),
        base_row(kernel_id="DK2647_3_PPN", arena="PPN_beta_gamma_source", kernel_formula="[Delta gamma, Delta beta, alpha_i, xi]_source=M_PPN dot epsilon_perp plus retained source/test legs", required_inputs="weak-field solution; PPN operator matrix; GR limit matching; source/test split; parent epsilon_A vector", current_status="KERNEL_STUB_NONCLAIM_OPERATOR_MATRIX_AND_GR_LIMIT_MISSING", units="dimensionless PPN deviations", score_ready="False", valid_prediction_row="False"),
        base_row(kernel_id="DK2647_4_clock", arena="clock_and_constant_drift", kernel_formula="Delta ln nu_i=K_clock_i dot epsilon_perp plus retained alpha/mass/readout coefficients", required_inputs="clock sensitivity vector; alpha/mass split; source body composition; tau_clock; parent epsilon_A vector", current_status="KERNEL_STUB_NONCLAIM_CLOCK_SENSITIVITY_AND_PARENT_VALUES_MISSING", units="dimensionless frequency shift/drift", score_ready="False", valid_prediction_row="False"),
        base_row(kernel_id="DK2647_5_orbital", arena="orbital_GM_inverse_square", kernel_formula="Delta ln(GM)_obs=K_orbital dot epsilon_perp plus retained finite-range/source-test/projector terms", required_inputs="source body composition; orbital GM convention; inverse-square kernel; tau_orbital; parent epsilon_A vector", current_status="KERNEL_STUB_NONCLAIM_ORBITAL_SOURCE_MAP_AND_PARENT_VALUES_MISSING", units="dimensionless GM/source deviation", score_ready="False", valid_prediction_row="False"),
        base_row(kernel_id="DK2647_6_no_cancellation", arena="all", kernel_formula="observable envelope=sum_i ||K_i residual_i|| unless a parent identity proves signed cancellation", required_inputs="component values or theorem-zero; covariance/correlation matrix if cancellations are claimed", current_status="NO_CANCELLATION_POLICY_ENFORCED_NONCLAIM", units="arena-dependent residual norm", score_ready="False", valid_prediction_row="False"),
    ]


def validator_case_rows() -> list[dict[str, Any]]:
    return [
        base_row(case_id="CASE2647_0_signature_unsigned", signature_signed="False", closure_as_theorem="False", epsilon_value="symbolic", kernel_ready="False", bound_as_prediction="False", expected_status="REFUSED_SIGNATURE_UNSIGNED"),
        base_row(case_id="CASE2647_1_closure_as_theorem", signature_signed="False", closure_as_theorem="True", epsilon_value="symbolic", kernel_ready="False", bound_as_prediction="False", expected_status="REFUSED_CLOSURE_NOT_PARENT_THEOREM"),
        base_row(case_id="CASE2647_2_missing_epsilon", signature_signed="True", closure_as_theorem="False", epsilon_value="missing", kernel_ready="True", bound_as_prediction="False", expected_status="REFUSED_MISSING_PARENT_EPSILON_VECTOR"),
        base_row(case_id="CASE2647_3_missing_kernel", signature_signed="True", closure_as_theorem="False", epsilon_value="parent_numeric", kernel_ready="False", bound_as_prediction="False", expected_status="REFUSED_PROJECTION_KERNEL_MISSING"),
        base_row(case_id="CASE2647_4_bound_shortcut", signature_signed="True", closure_as_theorem="False", epsilon_value="parent_numeric", kernel_ready="True", bound_as_prediction="True", expected_status="REFUSED_BOUND_NOT_PREDICTION"),
        base_row(case_id="CASE2647_5_schema_only", signature_signed="False", closure_as_theorem="False", epsilon_value="symbolic", kernel_ready="schema_only", bound_as_prediction="False", expected_status="SCHEMA_KERNEL_ONLY_NOT_EVIDENCE"),
    ]


def classify_case(row: dict[str, Any]) -> str:
    if row.get("closure_as_theorem") == "True":
        return "REFUSED_CLOSURE_NOT_PARENT_THEOREM"
    if row.get("signature_signed") != "True":
        if row.get("kernel_ready") == "schema_only":
            return "SCHEMA_KERNEL_ONLY_NOT_EVIDENCE"
        return "REFUSED_SIGNATURE_UNSIGNED"
    if row.get("epsilon_value") == "missing":
        return "REFUSED_MISSING_PARENT_EPSILON_VECTOR"
    if row.get("bound_as_prediction") == "True":
        return "REFUSED_BOUND_NOT_PREDICTION"
    if row.get("kernel_ready") != "True":
        return "REFUSED_PROJECTION_KERNEL_MISSING"
    return "FINITE_KERNEL_READY_NONCLAIM"


def validator_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        observed = classify_case(case)
        row = dict(case)
        row.update(
            {
                "observed_status": observed,
                "status_matches_expected": str(observed == case["expected_status"]),
                "valid_prediction_row": "False",
                "score_ready": "False",
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2647_0_signature", claim="ordinary matter action signature is parent-signed", allowed="False", blocker="clause matrix remains conditional/unsigned"),
        base_row(gate_id="CG2647_1_source_label_forgetting", claim="source functor returns total Hilbert stress and forgets species labels", allowed="False", blocker="no-source-weight clause remains unsigned"),
        base_row(gate_id="CG2647_2_delta_w_zero", claim="Delta_w_species theorem-zero", allowed="False", blocker="signature and source-label forgetting not parent-derived"),
        base_row(gate_id="CG2647_3_projection_kernels", claim="Delta_w kernels are prediction-ready", allowed="False", blocker="parent epsilon_A vector and arena kernels/material maps missing"),
        base_row(gate_id="CG2647_4_local_GR_Newton", claim="local GR/Newton source coupling is derived", allowed="False", blocker="finite coupling residual branch remains live"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2647_0_signature", decision="ORDINARY_MATTER_SIGNATURE_NOT_DERIVED", rationale="the required clauses are finite and sharp, but not derived from one parent action", consequence="no Delta_w_species theorem-zero or local-GR source claim"),
        base_row(decision_id="DEC2647_1_kernel_fallback", decision="DELTA_W_PROJECTION_KERNELS_STAGED_NONCLAIM", rationale="WEP/R10/PPN/clock/orbital formulas are explicit enough to guide future data plumbing without pretending to predict", consequence="arena work can proceed only after parent epsilon_A or theorem-zero exists"),
        base_row(decision_id="DEC2647_2_next", decision="SELECT_2648_SOURCE_FUNCTOR_LABEL_FORGETTING_OR_WEP_KERNEL_V0", rationale="source-label forgetting is narrower than the full signature and directly targets the coupling; WEP v0 is the most concrete fallback kernel", consequence="attack the smallest coupling clause next"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            next_id="NEXT2647_0_selected",
            next_doc="2648-Y5-R2FR-source-functor-label-forgetting-or-Delta-w-WEP-kernel-v0.md",
            next_script="scripts/Y5_R2FR_source_functor_label_forgetting_or_Delta_w_WEP_kernel_v0_2648.py",
            objective="Try to derive the source functor that forgets species labels and returns total Hilbert stress-energy before coupling; if it fails, build a nonclaim WEP Delta_w kernel v0 with material/source/tau requirements explicit.",
            include="source-label forgetting; total Hilbert stress; no w_A/kappa_A slot; variation-before-readout; WEP material tensor placeholders; tau_WEP; parent epsilon requirement",
            exclude="Ward-only proof; closure as theorem; symbolic kernel scoring; bound-as-prediction; local-GR/WEP claim; GitHub action; formalization-workbench edits",
        )
    ]


def branch_copy_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_rows: list[dict[str, Any]] = []
    for copy_id, path in BRANCH_COPIES.items():
        write_csv(path, rows)
        copy_rows.append(base_row(copy_id=copy_id, copy_path=str(path), path_exists=str(path.exists()), csv_parses=str(csv_parses(path)), contents="2647 Delta_w projection kernels, nonclaim"))
    return copy_rows


def validation_rows(generated_paths: list[Path], rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    signature_rows = rows_by_name["signature_attempt"]
    clause_rows = rows_by_name["clause_matrix"]
    kernel_rows = rows_by_name["projection_kernels"]
    result_rows = rows_by_name["validator_results"]
    gate_rows = rows_by_name["claim_gates"]
    decision_rows_ = rows_by_name["decision"]
    next_rows = rows_by_name["next_target"]
    branch_rows = rows_by_name["branch_copies"]
    checks = [
        ("VAL2647_00_sources", all(row["path_exists"] == "True" and row["needles_present"] == "True" for row in source_rows), "all cited source paths exist and required needles are present"),
        ("VAL2647_01_signature_not_promoted", any(row["attempt_id"] == "OMAS2647_2_parent_adoption_attempt" and row["status"] == "ORDINARY_MATTER_ACTION_SIGNATURE_NOT_PARENT_SIGNED" for row in signature_rows), "ordinary matter signature is not promoted"),
        ("VAL2647_02_clause_matrix", any(row["clause_id"] == "OMC2647_7_verdict" and row["current_status"] == "ORDINARY_MATTER_SIGNATURE_NOT_DERIVED" for row in clause_rows), "clause matrix records nonclaim verdict"),
        ("VAL2647_03_projection_kernels", {"DK2647_1_WEP", "DK2647_2_R10", "DK2647_3_PPN", "DK2647_4_clock", "DK2647_5_orbital"}.issubset({row["kernel_id"] for row in kernel_rows}) and all(row["score_ready"] == "False" for row in kernel_rows), "WEP/R10/PPN/clock/orbital kernels are nonclaim"),
        ("VAL2647_04_validator_refusals", all(row["status_matches_expected"] == "True" and row["valid_for_claim"] == "False" for row in result_rows), "validator rejects unsigned signature, closure shortcuts, missing epsilon, missing kernels and bound shortcuts"),
        ("VAL2647_05_claim_gates_false", all(row["allowed"] == "False" and row["valid_for_claim"] == "False" for row in gate_rows), "all claim gates remain blocked"),
        ("VAL2647_06_decision_next", any(row["decision"] == "SELECT_2648_SOURCE_FUNCTOR_LABEL_FORGETTING_OR_WEP_KERNEL_V0" for row in decision_rows_), "decision selects source-label forgetting/WEP kernel v0"),
        ("VAL2647_07_next_target", any(row["next_doc"].startswith("2648-Y5-R2FR-source-functor-label-forgetting") for row in next_rows), "2648 next target is recorded"),
        ("VAL2647_08_branch_copies", all(row["path_exists"] == "True" and row["csv_parses"] == "True" for row in branch_rows), "branch copies exist and parse"),
        ("VAL2647_09_csv_parse", all(csv_parses(path) for path in generated_paths if path.suffix.lower() == ".csv"), "all generated CSVs parse cleanly"),
        ("VAL2647_10_formalization_untouched", not formalization_has_2647_artifacts(), "no 2647 outputs are written under formalization-workbench"),
        ("VAL2647_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    rows = [base_row(validation_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]
    rows.append(base_row(validation_id="VAL2647_OVERALL", status="PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL", detail="2647 keeps ordinary matter action signature unsigned, stages Delta_w projection kernels, and selects source-label forgetting/WEP kernel v0 next"))
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        "\n\n".join(
            [
                "# 2647 - Y5/R2FR Ordinary-Matter Action Signature Or Delta-w Projection Kernels",
                "**Status:** the exact ordinary-matter action signature needed for local GR/Newton source coupling is written, but not parent-signed.",
                "**Main result:** `Delta_w_species` remains live. WEP/R10/PPN/clock/orbital projection kernels are staged as nonclaim contracts, not predictions.",
                "## Source register",
                md_table(rows_by_name["source_register"], ["source_id", "role", "source_path", "path_exists", "needles_present", "valid_for_claim"]),
                "## Signature attempt",
                md_table(rows_by_name["signature_attempt"], ["attempt_id", "claim_piece", "status", "formal_statement", "derivation_or_obstruction", "source_anchor", "valid_for_claim"]),
                "## Signature clause matrix",
                md_table(rows_by_name["clause_matrix"], ["clause_id", "signature_clause", "required_identity", "current_status", "if_signed", "if_unsigned", "source_anchor", "valid_for_claim"]),
                "## Delta_w projection kernels",
                md_table(rows_by_name["projection_kernels"], ["kernel_id", "arena", "kernel_formula", "required_inputs", "current_status", "units", "score_ready", "valid_prediction_row", "valid_for_claim"]),
                "## Validator cases",
                md_table(rows_by_name["validator_cases"], ["case_id", "expected_status", "valid_for_claim"]),
                "## Validator results",
                md_table(rows_by_name["validator_results"], ["case_id", "observed_status", "status_matches_expected", "valid_prediction_row", "score_ready", "valid_for_claim"]),
                "## Claim gates",
                md_table(rows_by_name["claim_gates"], ["gate_id", "claim", "allowed", "blocker", "valid_for_claim"]),
                "## Decision ledger",
                md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "consequence", "valid_for_claim"]),
                "## Next target",
                md_table(rows_by_name["next_target"], ["next_id", "next_doc", "next_script", "objective", "include", "exclude", "valid_for_claim"]),
                "## Branch copies",
                md_table(rows_by_name["branch_copies"], ["copy_id", "copy_path", "path_exists", "csv_parses", "contents", "valid_for_claim"]),
                "## Validation",
                md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    for directory in (RESIDUALS, QUEUE, LOCAL_BOUNDS, SOURCE_WEIGHT, MICROSCOPE):
        directory.mkdir(parents=True, exist_ok=True)
    remove_pycache()

    cases = validator_case_rows()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "signature_attempt": signature_attempt_rows(),
        "clause_matrix": clause_matrix_rows(),
        "projection_kernels": projection_kernel_rows(),
        "validator_cases": cases,
        "validator_results": validator_result_rows(cases),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    rows_by_name["branch_copies"] = branch_copy_rows(rows_by_name["projection_kernels"])

    for name, rows in rows_by_name.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], rows)

    generated = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())
    rows_by_name["validation"] = validation_rows(generated, rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()
