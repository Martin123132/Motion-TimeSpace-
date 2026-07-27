from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_R10_QLOC_YUKAWA_SOURCE_MAP_OR_BOUND_CURVE_BLOCKER_2410"
CHECKPOINT_ID = "2410"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2410-Y5-R2FR-R10-q-loc-Yukawa-source-map-or-bound-curve-blocker.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2410_SOURCE_REGISTER.csv",
    "source_map_gate": OUT / "P8_Y5_PARENT_QLOC_2410_R10_SOURCE_MAP_DERIVATION_GATE.csv",
    "quartet_status": OUT / "P8_Y5_PARENT_QLOC_2410_QUARTET_STATUS_AFTER_RANGE_IMPORT.csv",
    "bound_curve_gate": OUT / "P8_Y5_PARENT_QLOC_2410_BOUND_CURVE_ADMISSION_GATE.csv",
    "alpha_refusal": OUT / "P8_Y5_PARENT_QLOC_2410_ALPHA_SCORE_REFUSAL.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2410_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2410_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2410_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2410_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2410_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2410_R10_SOURCE_MAP_BLOCKER_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2410_R10_SOURCE_MAP_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_R10_BOUND_CURVE_STATUS_2410_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        body.append(
            "| "
            + " | ".join(
                str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
                for column in columns
            )
            + " |"
        )
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2410_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2410-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2410*",
        "*P8_Y5_BRR545_2410*",
        "*Y5_R2FR_R10_q_loc_Yukawa_source_map_or_bound_curve_blocker_2410*",
        "*JR2410*",
        "*PARENT_QLOC_R10_BOUND_CURVE_STATUS_2410*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2409_handoff",
            ROOT / "2409-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md",
            ["ROP2409_2_R10_yukawa_kernel_scaffold", "NEXT2409_0_selected", "VAL2409_OVERALL"],
            "current chain selects the R10 q_loc-to-Yukawa source-map blocker.",
        ),
        (
            "2409_response_operator_csv",
            OUT / "P8_Y5_PARENT_QLOC_2409_QLOC_RESPONSE_OPERATOR_STATUS.csv",
            ["ROP2409_2_R10_yukawa_kernel_scaffold", "MISSING_QLOC_TO_YUKAWA_SOURCE_MAP", "K_lambda(r)"],
            "machine-readable R10 scaffold and missing input list.",
        ),
        (
            "2209_quartet_checkpoint",
            ROOT / "2209-Y5-R2FR-R10-q-loc-Yukawa-source-map-or-bound-curve-blocker.md",
            ["R10_INPUT_QUARTET_DEFINED", "YSM2209_0_target_equation", "VAL2209_OVERALL"],
            "prior R10 quartet definition and bound-curve blocker.",
        ),
        (
            "2209_quartet_csv",
            OUT / "P8_Y5_PARENT_QLOC_2209_R10_INPUT_QUARTET_AUDIT.csv",
            ["R10Q2209_0_source_map", "R10Q2209_1_range", "R10Q2209_3_bound_curve"],
            "machine-readable four-lock R10 audit plus prediction-row lock.",
        ),
        (
            "2210_range_owner",
            ROOT / "2210-Y5-R2FR-lambda-X-range-owner-or-R10-source-map-first-row.md",
            ["M_AB v_i^B = mu_i^2 Z_AB v_i^B", "SOURCE_MAP_FIRST_ROW_STAGED_VALUES_BLOCKED", "VAL2210_OVERALL"],
            "operator-level lambda owner and eigenmode source-map first row.",
        ),
        (
            "2210_range_operator_csv",
            OUT / "P8_Y5_PARENT_QLOC_2210_RANGE_OPERATOR_DERIVATION.csv",
            ["ROD2210_1_generalized_range_spectrum", "lambda_i=1/sqrt(mu_i^2)", "MISSING_PARENT_COEFFICIENTS"],
            "machine-readable range owner: lambda comes from the parent spectrum.",
        ),
        (
            "2210_source_map_first_row_csv",
            OUT / "P8_Y5_PARENT_QLOC_2210_R10_SOURCE_MAP_FIRST_ROW.csv",
            ["SM2210_0_eigenmode_source_slot", "MISSING_J_A", "SM2210_2_no_scalar_proxy_guard"],
            "existing nonclaim q_loc-to-eigensource first row and scalar-proxy guard.",
        ),
        (
            "563_real_anchor_checkpoint",
            ROOT / "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
            ["E563_1_full_curve_missing", "E563_2_mts_parent_coefficients_missing", "B563_0_no_full_bound_curve"],
            "real R10 anchor provenance, with full-curve and parent-alpha blockers.",
        ),
        (
            "2209_bound_curve_csv",
            OUT / "P8_Y5_PARENT_QLOC_2209_BOUND_CURVE_STATUS.csv",
            ["ANCHOR_ONLY_NON_CURVE", "MISSING_ALPHA_BOUND_CURVE", "BOUND_CURVE_NOT_CLAIM_READY"],
            "machine-readable anchor-only and missing-full-curve status.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def source_map_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="SMG2410_0_no_direct_vector_scalarization",
            object="q_loc^nu versus Yukawa scalar source",
            statement="q_loc^nu is a local residual/vector-divergence object, not by itself the scalar rho_X that sources a Yukawa potential.",
            derived_condition="A direct assignment rho_X := q_loc or rho_X := |q_loc| is forbidden unless the parent supplies a covector projection, inverse-divergence convention, domain, and units before readout.",
            status="NO_DIRECT_SOURCE_MAP_THEOREM_CONDITION_WRITTEN",
            missing_inputs="MISSING_TAU_i_NU;MISSING_I_DIV_INVERSE;MISSING_PROJECTOR_DOMAIN;MISSING_UNITS",
            passes_now=False,
            score_ready=False,
        ),
        base_row(
            gate_id="SMG2410_1_parent_quadratic_source_action",
            object="finite-range residual mode action",
            statement="A score-ready R10 branch must descend to S2_i=1/2 integral[Z_i |grad X_i|^2 + M_i^2 X_i^2] - integral[J_i X_i] on the physical quotient domain.",
            derived_condition="Euler equation: (-Z_i Delta + M_i^2) X_i = J_i; lambda_i=sqrt(Z_i/M_i^2) in the one-mode case.",
            status="CONDITIONAL_YUKAWA_SOURCE_ACTION_FORM_DERIVED",
            missing_inputs="MISSING_Z_i;MISSING_M_i_SQUARED;MISSING_J_i;MISSING_DOMAIN",
            passes_now=False,
            score_ready=False,
        ),
        base_row(
            gate_id="SMG2410_2_range_owner_import",
            object="lambda_i",
            statement="2210 is imported: for a multi-mode parent operator, M_AB v_i^B=mu_i^2 Z_AB v_i^B and lambda_i=1/mu_i.",
            derived_condition="R10 range is not an empirical knob; it is a parent-spectrum output or the finite-range branch is not selected.",
            status="RANGE_OWNER_IMPORTED_VALUES_BLOCKED",
            missing_inputs="MISSING_PARENT_Z_AB;MISSING_PARENT_M_AB;MISSING_EIGENVECTORS;MISSING_UNITS_OWNER",
            passes_now=False,
            score_ready=False,
        ),
        base_row(
            gate_id="SMG2410_3_alpha_law_when_source_map_exists",
            object="alpha_i(lambda_i)",
            statement="If J_i and body charges are parent-owned, Phi_i(r)=-(Q_i^S/(4*pi*Z_i))*exp(-r/lambda_i)/r and alpha_i=s_i Q_i^S Q_i^T/(4*pi*G_obs*m_S*m_T*Z_i).",
            derived_condition="Q_i^B must be the source/test body integral of J_i in the same Newtonian frame and normalization used by the R10 apparatus.",
            status="CONDITIONAL_ALPHA_LAW_WRITTEN_VALUES_BLOCKED",
            missing_inputs="MISSING_Q_SOURCE;MISSING_Q_TEST;MISSING_Z_i;MISSING_SIGN_POLICY;MISSING_APPARATUS_NORMALIZATION",
            passes_now=False,
            score_ready=False,
        ),
        base_row(
            gate_id="SMG2410_4_q_loc_bridge_contract",
            object="q_loc-to-eigensource bridge",
            statement="A legitimate bridge has the form J_i = S_i[I_div^{-1}(q_loc)] or q_loc^nu = P_loc b_i^nu[(L_i X_i)-J_i] + boundary terms, with all maps parent-owned.",
            derived_condition="The same bridge must decide whether q_loc is an off-shell Euler residual, a stress-divergence readout, or a genuine source current.",
            status="BRIDGE_CONTRACT_EXACT_BUT_UNSIGNED",
            missing_inputs="MISSING_CURRENT_OWNER;MISSING_TGK_OR_I_DIV_INVERSE;MISSING_B_i_NU;MISSING_BOUNDARY_TERMS",
            passes_now=False,
            score_ready=False,
        ),
        base_row(
            gate_id="SMG2410_5_verdict",
            object="R10 q_loc source map",
            statement="2410 does not fill a numeric source map; it upgrades the source-map blocker into a precise theorem contract and blocks scalar shortcuts.",
            derived_condition="Next work must source-sign Z/M/J/current ownership or demote R10 to data-parallel/nonclaim only.",
            status="SOURCE_MAP_GATE_TIGHTENED_NO_CLAIM",
            missing_inputs="MISSING_PARENT_COEFFICIENTS;MISSING_QLOC_BRIDGE;MISSING_CHARGES;MISSING_FULL_BOUND_CURVE",
            passes_now=False,
            score_ready=False,
        ),
    ]


def quartet_status_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            quartet_id="R10Q2410_0_source_map",
            required_input="q_loc_to_Yukawa_source_map",
            current_status="CONDITIONAL_CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            progress_since_2409="direct q_loc scalarization is now explicitly forbidden; legal bridge forms are specified",
            still_missing="MISSING_TAU_i_NU;MISSING_I_DIV_INVERSE;MISSING_J_i;MISSING_BOUNDARY_TERMS",
            passes_now=False,
            score_ready=False,
        ),
        base_row(
            quartet_id="R10Q2410_1_range",
            required_input="lambda_i",
            current_status="OPERATOR_LAW_IMPORTED_VALUES_BLOCKED",
            progress_since_2409="range must come from M_AB v=mu^2 Z_AB v, not a fitted knob",
            still_missing="MISSING_Z_AB;MISSING_M_AB;MISSING_EIGENVECTORS;MISSING_UNITS",
            passes_now=False,
            score_ready=False,
        ),
        base_row(
            quartet_id="R10Q2410_2_charge_norm",
            required_input="source_test_charge_normalization",
            current_status="BLOCKED_NONCLAIM",
            progress_since_2409="alpha law now states Q_i^S and Q_i^T must be body integrals of the same J_i",
            still_missing="MISSING_Q_SOURCE;MISSING_Q_TEST;MISSING_TAU_R10;MISSING_SOURCE_TEST_PROFILES",
            passes_now=False,
            score_ready=False,
        ),
        base_row(
            quartet_id="R10Q2410_3_bound_curve",
            required_input="alpha_bound(lambda) full curve",
            current_status="ANCHOR_ONLY_NONCLAIM_FULL_CURVE_MISSING",
            progress_since_2409="anchor rows remain provenance only; no promotion to evidence curve",
            still_missing="MISSING_DENSE_DIGITIZED_OR_OFFICIAL_BOUND_CURVE;MISSING_INTERPOLATION_POLICY_FOR_CLAIM",
            passes_now=False,
            score_ready=False,
        ),
        base_row(
            quartet_id="R10Q2410_4_prediction_row",
            required_input="numeric alpha_i(lambda_i)",
            current_status="BLOCKED_NONCLAIM",
            progress_since_2409="formal alpha law now tied to J_i and Z_i rather than a placeholder scalar amplitude",
            still_missing="MISSING_NUMERIC_ALPHA;MISSING_UNCERTAINTY_ENVELOPE;MISSING_NO_CANCELLATION_COMPONENT_VECTOR",
            passes_now=False,
            score_ready=False,
        ),
        base_row(
            quartet_id="R10Q2410_5_verdict",
            required_input="R10 score readiness",
            current_status="R10_SCORE_BLOCKED_BUT_SOURCE_MAP_CONTRACT_TIGHTENED",
            progress_since_2409="the route is sharper: prove parent source-current ownership or stop treating R10 as score-ready",
            still_missing="MISSING_PARENT_ZMJ_STACK;MISSING_FULL_CURVE",
            passes_now=False,
            score_ready=False,
        ),
    ]


def bound_curve_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            curve_id="BCG2410_0_EotWash_2020_anchor",
            source="Eot-Wash 2020 PRL / PubMed 32216404 / arXiv:2002.11761",
            lambda_value="3.86e-5",
            lambda_units="m",
            alpha_bound="1.0",
            data_status="ANCHOR_ONLY_NON_CURVE",
            admission_status="PROVENANCE_OK_CLAIM_REJECTED",
            reason="single alpha=1 threshold anchor cannot bound an arbitrary predicted lambda_i or spectral envelope",
            valid_bound_curve_row=False,
        ),
        base_row(
            curve_id="BCG2410_1_EotWash_2007_anchor",
            source="Eot-Wash 2007 PRL / arXiv:hep-ph/0611184",
            lambda_value="5.6e-5",
            lambda_units="m",
            alpha_bound="1.0",
            data_status="ANCHOR_ONLY_NON_CURVE",
            admission_status="CONTINUITY_OK_CLAIM_REJECTED",
            reason="older threshold anchor remains continuity/provenance, not a dense modern curve",
            valid_bound_curve_row=False,
        ),
        base_row(
            curve_id="BCG2410_2_full_curve_requirement",
            source="future digitized PRL figure or official machine-readable table",
            lambda_value="positive dense lambda grid",
            lambda_units="m",
            alpha_bound="positive numeric alpha_bound(lambda)",
            data_status="MISSING_FULL_CURVE",
            admission_status="BLOCKED",
            reason="R10 scoring requires interpolation over the predicted lambda_i or envelope support",
            valid_bound_curve_row=False,
        ),
        base_row(
            curve_id="BCG2410_3_verdict",
            source="563+2209+2410",
            lambda_value="not_scoreable",
            lambda_units="not_scoreable",
            alpha_bound="not_scoreable",
            data_status="BOUND_CURVE_NOT_CLAIM_READY",
            admission_status="BLOCKED_NONCLAIM",
            reason="real anchors help plumbing but no alpha(lambda) claim can use them as the full curve",
            valid_bound_curve_row=False,
        ),
    ]


def alpha_refusal_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            refusal_id="AR2410_0_no_fake_q_scalar",
            attempted_shortcut="rho_X := q_loc or |q_loc|",
            verdict="REJECTED",
            reason="q_loc is a vector/residual object; R10 needs a scalar source current with parent-owned projection and units.",
            required_repair="derive tau_i_nu and I_div^{-1}/T_GK owner or write finite source-current rows",
            runner_must_return=False,
        ),
        base_row(
            refusal_id="AR2410_1_no_anchor_curve_claim",
            attempted_shortcut="use alpha=1 threshold anchor as full alpha_bound(lambda) curve",
            verdict="REJECTED",
            reason="anchor-only rows do not define a conservative bound at arbitrary lambda_i or spectral support.",
            required_repair="digitize the full 2020 curve or locate an official table, then validate interpolation",
            runner_must_return=False,
        ),
        base_row(
            refusal_id="AR2410_2_no_inserted_lambda",
            attempted_shortcut="choose lambda_X by convenience or fit pressure",
            verdict="REJECTED",
            reason="lambda_i must come from the parent spectrum M v=mu^2 Z v or the branch is not finite-range R10.",
            required_repair="source-sign Z_AB/M_AB/domain/eigenvectors or classify rank-zero/spectral branch",
            runner_must_return=False,
        ),
        base_row(
            refusal_id="AR2410_3_no_public_claim",
            attempted_shortcut="call this a local-GR/R10 pass",
            verdict="REJECTED",
            reason="the source map, numeric range, charges, full curve, and no-cancellation envelope remain missing.",
            required_repair="close every quartet row with numeric/sourced values and validation",
            runner_must_return=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2410_0_source_map_contract",
            gate="legal q_loc-to-Yukawa source-map form exists",
            status="PASS_NONCLAIM_CONTRACT_ONLY",
            implication="we know what a valid bridge must look like, but no parent-signed bridge exists yet",
        ),
        base_row(
            gate_id="CG2410_1_numeric_source_map",
            gate="numeric/source-signed J_i from q_loc exists",
            status="BLOCKED_NONCLAIM",
            implication="alpha_i(lambda_i) remains symbolic",
        ),
        base_row(
            gate_id="CG2410_2_range_values",
            gate="lambda_i values or branch-selection spectrum exists",
            status="BLOCKED_NONCLAIM",
            implication="R10 versus PPN/spectral/constraint arena cannot yet be selected quantitatively",
        ),
        base_row(
            gate_id="CG2410_3_bound_curve",
            gate="claim-valid alpha_bound(lambda) curve exists",
            status="BLOCKED_NONCLAIM",
            implication="anchor-only rows remain data plumbing, not evidence",
        ),
        base_row(
            gate_id="CG2410_4_local_GR_Newton",
            gate="local GR/Newton reduction follows",
            status="BLOCKED_NONCLAIM",
            implication="no theorem-zero or bounded residual proof has closed",
        ),
        base_row(
            gate_id="CG2410_5_GitHub",
            gate="public/GitHub update",
            status="BLOCKED_PRIVATE",
            implication="continue private derivation work before publishing",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2410_0_gain",
            decision="SOURCE_MAP_CONTRACT_TIGHTENED",
            rationale="R10 is no longer allowed to use a scalar proxy for q_loc; the bridge must be parent-owned through J_i, tau_i_nu, or I_div^{-1}/T_GK.",
            next_action="hunt parent Z/M/J/current ownership together rather than only bound-curve data",
        ),
        base_row(
            decision_id="DEC2410_1_limit",
            decision="NO_ALPHA_SCORE_OR_LOCAL_CLAIM",
            rationale="all score-critical values are still absent: source map, range values, source/test charges, full curve, and no-cancellation vector.",
            next_action="keep all generated rows valid_for_claim=false",
        ),
        base_row(
            decision_id="DEC2410_2_best_next",
            decision="PARENT_ZM_AND_J_OWNER_SELECTED",
            rationale="range and source cannot be separated: Z/M gives lambda_i, J_i gives the actual Yukawa charge; without both, R10 is only scaffolding.",
            next_action="2411 should try to source-sign Z_AB/M_AB/J_A from Gamma_eff/Khat/response-doublet or demote finite-range R10",
        ),
        base_row(
            decision_id="DEC2410_3_data_parallel",
            decision="BOUND_CURVE_DATA_HELD_PARALLEL",
            rationale="full curve acquisition is useful but cannot rescue missing theory coefficients.",
            next_action="run curve digitization only as a separate nonclaim data pass",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2410_0_selected",
            selection_status="selected",
            target_file="2411-Y5-R2FR-parent-ZM-and-J-current-owner-or-constraint-branch.md",
            target_script="scripts/Y5_R2FR_parent_ZM_and_J_current_owner_or_constraint_branch_2411.py",
            objective="try to identify the parent quadratic residues Z_AB/M_AB and the source current J_A feeding the q_loc bridge; if absent, classify finite-range R10 as constraint/spectral/coefficient-acquisition only",
            success_condition="one parent Z/M/J clause is source-signed or the finite-range R10 route is explicitly demoted with all claim gates false",
            do_not_do="do not insert q_loc as a scalar source, choose lambda by convenience, promote anchor-only curves, claim local GR/R10, or use GitHub",
        ),
        base_row(
            route_id="NEXT2410_1_data_parallel",
            selection_status="held_parallel",
            target_file="2411b-Y5-R2FR-EotWash-full-bound-curve-digitization-nonclaim.md",
            target_script="scripts/Y5_R2FR_EotWash_full_bound_curve_digitization_nonclaim_2411b.py",
            objective="acquire dense alpha_bound(lambda) rows with provenance and interpolation policy",
            success_condition="positive numeric full-curve rows parse and remain nonclaim until theory alpha exists",
            do_not_do="do not treat threshold anchors as a full bound curve",
        ),
    ]


def copy_branch_rows(quartet_rows: list[dict[str, Any]], source_map_rows: list[dict[str, Any]], bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["quartet_status"], BRANCH_COPIES["queue"], quartet_rows),
        ("branch_wep", OUTPUTS["source_map_gate"], BRANCH_COPIES["branch_wep"], source_map_rows),
        ("beta_docs", OUTPUTS["bound_curve_gate"], BRANCH_COPIES["beta_docs"], bound_rows),
    ]
    copy_rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, rows in copy_specs:
        write_csv(target_path, rows)
        parse_ok, row_count, parse_detail = csv_rows_parse(target_path)
        copy_rows.append(
            base_row(
                copy_id=copy_id,
                source_path=str(source_path),
                target_path=str(target_path),
                copied=target_path.exists(),
                parse_ok=parse_ok,
                row_count=row_count,
                parse_detail=parse_detail,
            )
        )
    return copy_rows


def all_generated_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, value in data.items():
        if key != "validation":
            rows.extend(value)
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    sources = data["source_register"]
    rows.append(
        base_row(
            validation_id="VAL2410_00_sources_exist",
            status="PASS" if all(row["path_exists"] for row in sources) else "FAIL",
            detail=f"{sum(1 for row in sources if row['path_exists'])}/{len(sources)} sources exist",
        )
    )
    rows.append(
        base_row(
            validation_id="VAL2410_01_needles_found",
            status="PASS" if all(row["needles_found"] for row in sources) else "FAIL",
            detail=f"{sum(1 for row in sources if row['needles_found'])}/{len(sources)} source needle sets found",
        )
    )

    source_map_text = " ".join(str(row) for row in data["source_map_gate"])
    rows.append(
        base_row(
            validation_id="VAL2410_02_no_direct_scalarization",
            status="PASS" if "rho_X := q_loc" in source_map_text and "forbidden" in source_map_text else "FAIL",
            detail="direct q_loc scalarization is explicitly rejected",
        )
    )
    rows.append(
        base_row(
            validation_id="VAL2410_03_range_imported",
            status="PASS" if "M_AB v_i^B=mu_i^2 Z_AB v_i^B" in source_map_text and "lambda_i=1/mu_i" in source_map_text else "FAIL",
            detail="2210 range owner imported into current R10 gate",
        )
    )
    rows.append(
        base_row(
            validation_id="VAL2410_04_bridge_contract",
            status="PASS" if "I_div^{-1}(q_loc)" in source_map_text and "BRIDGE_CONTRACT_EXACT_BUT_UNSIGNED" in source_map_text else "FAIL",
            detail="q_loc-to-eigensource bridge is exact but unsigned",
        )
    )

    quartet = data["quartet_status"]
    rows.append(
        base_row(
            validation_id="VAL2410_05_quartet_blocked",
            status="PASS" if len(quartet) >= 6 and not any(row["passes_now"] for row in quartet) else "FAIL",
            detail=f"quartet rows={len(quartet)}; no score-ready row promoted",
        )
    )

    bound_rows = data["bound_curve_gate"]
    rows.append(
        base_row(
            validation_id="VAL2410_06_bound_curve_nonclaim",
            status="PASS" if all(not row["valid_bound_curve_row"] for row in bound_rows) and any(row["data_status"] == "MISSING_FULL_CURVE" for row in bound_rows) else "FAIL",
            detail="anchor rows retained, full bound curve remains missing",
        )
    )

    refusal_text = " ".join(str(row) for row in data["alpha_refusal"])
    rows.append(
        base_row(
            validation_id="VAL2410_07_refusal_runner",
            status="PASS" if "REJECTED" in refusal_text and "runner_must_return': False" in refusal_text else "FAIL",
            detail="shortcut alpha scoring is refused",
        )
    )

    claim_rows = data["claim_gate"]
    rows.append(
        base_row(
            validation_id="VAL2410_08_claim_gates_false",
            status="PASS" if all(not row["valid_for_claim"] and not row["claim_allowed"] for row in claim_rows) else "FAIL",
            detail="claim gates remain false",
        )
    )

    next_text = " ".join(str(row) for row in data["next_target"])
    rows.append(
        base_row(
            validation_id="VAL2410_09_next_selected",
            status="PASS" if "2411-Y5-R2FR-parent-ZM-and-J-current-owner-or-constraint-branch.md" in next_text else "FAIL",
            detail="parent Z/M/J owner route selected next",
        )
    )

    csv_details: list[str] = []
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parse_ok, row_count, parse_detail = csv_rows_parse(path)
        csv_ok = csv_ok and parse_ok and row_count > 0
        csv_details.append(f"{path.name}:{row_count}:{parse_detail}")
    rows.append(
        base_row(
            validation_id="VAL2410_10_csv_parse",
            status="PASS" if csv_ok else "FAIL",
            detail="; ".join(csv_details),
        )
    )

    branch_copy_rows = data["branch_copies"]
    rows.append(
        base_row(
            validation_id="VAL2410_11_branch_copies",
            status="PASS" if all(row["copied"] and row["parse_ok"] for row in branch_copy_rows) else "FAIL",
            detail=";".join(str(row["target_path"]) for row in branch_copy_rows),
        )
    )

    generated = all_generated_rows(data)
    rows.append(
        base_row(
            validation_id="VAL2410_12_no_claim_flags",
            status="PASS" if all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in generated) else "FAIL",
            detail="all generated rows keep valid_for_claim=false and claim_allowed=false",
        )
    )
    rows.append(
        base_row(
            validation_id="VAL2410_13_formalization_untouched_by_outputs",
            status="PASS" if not formalization_has_2410_artifacts() else "FAIL",
            detail="script outputs stay inside post-checkpoint-work",
        )
    )

    overall_status = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(
        base_row(
            validation_id="VAL2410_OVERALL",
            status=overall_status,
            detail="2410 tightens the R10 q_loc-to-Yukawa source-map contract, imports the parent range law, refuses shortcut alpha scoring, and selects parent Z/M/J ownership next",
        )
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    validation = data["validation"]
    overall = next(row for row in validation if row["validation_id"] == "VAL2410_OVERALL")
    lines = [
        "# 2410 - Y5/R2FR R10 q_loc Yukawa Source Map Or Bound Curve Blocker",
        "",
        "## Result",
        "",
        "2410 is a useful tightening step, not a victory lap. The R10 lane is now forced through a legal source-map contract:",
        "",
        "`q_loc^nu` cannot be silently used as a scalar Yukawa charge. A scoreable branch must first produce a parent-owned finite-range mode with `(-Z_i Delta + M_i^2) X_i = J_i`, `lambda_i=sqrt(Z_i/M_i^2)` or the generalized `M_AB v_i^B=mu_i^2 Z_AB v_i^B`, and a source/test charge normalization built from the same `J_i`.",
        "",
        "That means the old shortcut is dead in a good way: either MTS derives `Z/M/J/current` ownership, or the R10 branch stays a nonclaim data/scaffolding branch. No local-GR/Newton claim follows yet.",
        "",
        "## Source Register",
        "",
        md_table(data["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## R10 Source Map Derivation Gate",
        "",
        md_table(
            data["source_map_gate"],
            [
                "gate_id",
                "object",
                "statement",
                "derived_condition",
                "status",
                "missing_inputs",
                "passes_now",
                "score_ready",
                "valid_for_claim",
            ],
        ),
        "",
        "## Quartet Status After Range Import",
        "",
        md_table(
            data["quartet_status"],
            [
                "quartet_id",
                "required_input",
                "current_status",
                "progress_since_2409",
                "still_missing",
                "passes_now",
                "score_ready",
                "valid_for_claim",
            ],
        ),
        "",
        "## Bound Curve Admission Gate",
        "",
        md_table(
            data["bound_curve_gate"],
            [
                "curve_id",
                "source",
                "lambda_value",
                "lambda_units",
                "alpha_bound",
                "data_status",
                "admission_status",
                "reason",
                "valid_bound_curve_row",
                "valid_for_claim",
            ],
        ),
        "",
        "## Alpha Score Refusal",
        "",
        md_table(
            data["alpha_refusal"],
            [
                "refusal_id",
                "attempted_shortcut",
                "verdict",
                "reason",
                "required_repair",
                "runner_must_return",
                "valid_for_claim",
            ],
        ),
        "",
        "## Claim Gates",
        "",
        md_table(data["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(data["decision"], ["decision_id", "decision", "rationale", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(
            data["next_target"],
            [
                "route_id",
                "selection_status",
                "target_file",
                "target_script",
                "objective",
                "success_condition",
                "do_not_do",
                "valid_for_claim",
            ],
        ),
        "",
        "## Branch Copies",
        "",
        md_table(data["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Practical Status",
        "",
        "This is the right kind of grind. We did not get a claimed fifth-force comparison, but we cut away a bad escape hatch: `q_loc` cannot be smuggled into R10 as a scalar charge. The next serious leap is to find the parent `Z/M/J` stack. If that stack exists, R10 becomes calculable; if it does not, the finite-range local branch should be demoted rather than endlessly circled.",
        "",
        f"Validation overall: `{overall['status']}`.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    BETA_DOCS.mkdir(parents=True, exist_ok=True)

    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "source_map_gate": source_map_gate_rows(),
        "quartet_status": quartet_status_rows(),
        "bound_curve_gate": bound_curve_gate_rows(),
        "alpha_refusal": alpha_refusal_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["source_register"])
    write_csv(OUTPUTS["source_map_gate"], data["source_map_gate"])
    write_csv(OUTPUTS["quartet_status"], data["quartet_status"])
    write_csv(OUTPUTS["bound_curve_gate"], data["bound_curve_gate"])
    write_csv(OUTPUTS["alpha_refusal"], data["alpha_refusal"])
    write_csv(OUTPUTS["claim_gate"], data["claim_gate"])
    write_csv(OUTPUTS["decision"], data["decision"])
    write_csv(OUTPUTS["next_target"], data["next_target"])

    data["branch_copies"] = copy_branch_rows(data["quartet_status"], data["source_map_gate"], data["bound_curve_gate"])
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
