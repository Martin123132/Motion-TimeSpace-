from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1579"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1579-Y5-RAB-finite-component-source-acquisition-ledger-and-comparator-dry-run.md"

SOURCE_FILES = {
    "1578_doc": ROOT / "1578-Y5-RAB-finite-component-bound-pack-and-runner.md",
    "1578_validation": OUT / "P8_Y5_BRR545_1578_VALIDATION.csv",
    "1578_inputs": OUT / "P8_Y5_PARENT_QLOC_1578_COMPONENT_INPUT_STATUS.csv",
    "1578_arena": OUT / "P8_Y5_PARENT_QLOC_1578_ARENA_BLOCK_MATRIX.csv",
    "1578_runner": OUT / "P8_Y5_PARENT_QLOC_1578_PLACEHOLDER_REFUSAL_RUNNER.csv",
    "1578_next": OUT / "P8_Y5_PARENT_QLOC_1578_NEXT_TARGET.csv",
    "1574_finite": OUT / "P8_Y5_PARENT_QLOC_1574_RAB_FINITE_INPUT_ROWS_NONCLAIM.csv",
    "1573_required": OUT / "P8_Y5_PARENT_QLOC_1573_TAU_R10_REQUIRED_INPUTS.csv",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
    "r10_review_candidate": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
}

NEEDLES = {
    "1578_doc": ["NEXT_1579_RAB_FINITE_COMPONENT_SOURCE_ACQUISITION_LEDGER_AND_COMPARATOR_DRY_RUN", "q_R_hat/Q_R"],
    "1578_validation": ["VAL1578_OVERALL", "PASS"],
    "1578_inputs": ["INPUT1578_10_tau_orbital", "MISSING_ORBITAL_PROJECTION"],
    "1578_arena": ["ARENA1578_1_PPN", "BLOCKED_NO_CLAIM"],
    "1578_runner": ["RUN1578_5_reviewed_curve", "REFUSE_PLACEHOLDER"],
    "1578_next": ["1579-Y5-RAB-finite-component-source-acquisition-ledger-and-comparator-dry-run.md", "do not fabricate internal coefficients"],
    "1574_finite": ["FIN1574_2_ZR", "MISSING_ZR_OR_NO_POLE_THEOREM"],
    "1573_required": ["REQ1573_6_bound_curve", "REVIEWED_CANDIDATE_NOT_ACCEPTED"],
    "local_bound_claims": ["MICROSCOPE_final_TiPt", "Cassini_Shapiro_gamma_2003", "LLR_Biskupek_Muller_Torre_2021", "R10_fifth_force"],
    "r10_review_candidate": ["review_candidate_only_requires_official_supplement", "false"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1579_SOURCE_REGISTER.csv"
ACQUISITION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1579_COMPONENT_SOURCE_ACQUISITION_LEDGER.csv"
EXTERNAL_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1579_EXTERNAL_BOUND_AUDIT.csv"
COMPARATOR_DRY_RUN = OUT / "P8_Y5_PARENT_QLOC_1579_COMPARATOR_DRY_RUN.csv"
RUNNER_SUMMARY = OUT / "P8_Y5_PARENT_QLOC_1579_RUNNER_SUMMARY.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1579_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1579_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1579_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1579_VALIDATION.csv"

COPY_TARGETS = {
    ACQUISITION_LEDGER: [
        QUARANTINE / "COMPONENT_SOURCE_ACQUISITION_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_component_source_acquisition_ledger_nonclaim_1579.csv",
    ],
    EXTERNAL_AUDIT: [
        QUARANTINE / "EXTERNAL_BOUND_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_external_bound_audit_nonclaim_1579.csv",
    ],
    COMPARATOR_DRY_RUN: [
        QUARANTINE / "COMPARATOR_DRY_RUN_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_comparator_dry_run_nonclaim_1579.csv",
    ],
    RUNNER_SUMMARY: [
        QUARANTINE / "RUNNER_SUMMARY_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_runner_summary_nonclaim_1579.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_claim_gate_nonclaim_1579.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_finite_component_source_decision_nonclaim_1579.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "parent_signed": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def local_bound_by_dataset(dataset_id: str) -> dict[str, str]:
    for row in read_csv(SOURCE_FILES["local_bound_claims"]):
        if row.get("dataset_id") == dataset_id:
            return row
    return {}


def r10_review_rows() -> list[dict[str, str]]:
    return read_csv(SOURCE_FILES["r10_review_candidate"])


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1579_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, NEEDLES[key]),
                "needles": "; ".join(NEEDLES[key]),
                "purpose": "finite R_AB source acquisition and comparator dry-run",
                **flags(),
            }
        )
    return rows


def acquisition_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ACQ1579_0_qRhat",
            "q_R_hat or Q_R",
            "P0",
            "PPN/local-GR source denominator",
            "theorem-zero from parent no-charge/current route OR numeric Q_R/q_R_hat with source body, radius, frame and GM convention",
            "1577 current route failed; 1578 row remains blank",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1578_COMPONENT_INPUT_STATUS.csv::INPUT1578_0_qRhat",
            "MISSING_INTERNAL_SOURCE",
            "derive PPN residual vector first, then decide whether q_R_hat is theorem-zero or bounded",
        ),
        (
            "ACQ1579_1_ZR",
            "Z_R",
            "P0",
            "finite propagator denominator and R10 range",
            "parent Hessian/kinetic residue in same normalization as beta legs OR no-pole theorem",
            "1573/1574/1578 all mark Z_R missing",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1574_RAB_FINITE_INPUT_ROWS_NONCLAIM.csv::FIN1574_2_ZR",
            "MISSING_PARENT_OPERATOR",
            "extract quadratic R_AB block from parent action or keep finite branch unscoreable",
        ),
        (
            "ACQ1579_2_MR2",
            "M_R^2",
            "P0",
            "lambda_R=sqrt(Z_R/M_R^2)",
            "positive parent mass-gap/Hessian coefficient in same normalization as Z_R",
            "1573/1574/1578 all mark M_R^2 missing",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1574_RAB_FINITE_INPUT_ROWS_NONCLAIM.csv::FIN1574_3_MR2",
            "MISSING_PARENT_MASS_GAP",
            "extract mass-gap with Z_R or refuse lambda_R",
        ),
        (
            "ACQ1579_3_beta_source",
            "beta_S^R",
            "P1",
            "source leg for R10/WEP/clock exchange",
            "matter descent theorem-zero OR numeric partial ln m_source / partial R_AB with material/source path",
            "chain-rule theorem is conditional, not parent-signed",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1574_RAB_FINITE_INPUT_ROWS_NONCLAIM.csv::FIN1574_0_beta_source",
            "MISSING_SOURCE_CHARGE",
            "do not use single coupling; split source/test and material markers",
        ),
        (
            "ACQ1579_4_beta_test",
            "beta_T^R",
            "P1",
            "test leg for R10/WEP/clock exchange",
            "matter descent theorem-zero OR numeric partial ln m_test / partial R_AB with material/readout path",
            "chain-rule theorem is conditional, not parent-signed",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1574_RAB_FINITE_INPUT_ROWS_NONCLAIM.csv::FIN1574_1_beta_test",
            "MISSING_TEST_CHARGE",
            "pair with beta_S^R; no source/test collapse",
        ),
        (
            "ACQ1579_5_JR",
            "J_R",
            "P1",
            "bulk source current and local source denominator",
            "parent source-current density or theorem-zero from matter/source action",
            "1577 current route leaves Q_R hair; J_R not source-normalized",
            "1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md::RCC1577_0_current_equation",
            "MISSING_SOURCE_CURRENT",
            "derive source denominator in PPN-compatible variables before orbital scoring",
        ),
        (
            "ACQ1579_6_boundary_tail",
            "B_R, Pi_R^n, alpha_boundary_tail",
            "P0",
            "no-cancellation tail envelope for every arena",
            "zero/proper/exact boundary theorem OR absolute finite bound",
            "source-neutral boundary route is sufficient only conditionally",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1577_QR_NO_CHARGE_THEOREM_AUDIT.csv::NCA1577_1_boundary_momentum",
            "MISSING_BOUNDARY_TAIL_OR_ZERO_THEOREM",
            "treat as mandatory additive envelope, never as cancellation",
        ),
        (
            "ACQ1579_7_tau_R10",
            "tau_R10 or Xi_R10",
            "P2",
            "R10 Yukawa alpha(lambda) projection",
            "R10-specific source-normalized kernel plus accepted curve/table",
            "formal kernel exists, but Xi/readout and accepted curve are missing",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1573_TAU_R10_REQUIRED_INPUTS.csv::REQ1573_4_Xi",
            "MISSING_R10_PROJECTION_OR_ACCEPTED_CURVE",
            "wait until Z/M/betas/tail have at least theorem-zero or numeric rows",
        ),
        (
            "ACQ1579_8_tau_PPN",
            "tau_PPN or C_QR",
            "P0",
            "PPN gamma/local-GR residual vector",
            "PPN-specific projection from R_AB/q_R_hat to gamma-1 in source-frame variables",
            "external Cassini row exists, internal projection absent",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1578_ARENA_BLOCK_MATRIX.csv::ARENA1578_1_PPN",
            "MISSING_PPN_PROJECTION",
            "best next derivation target because it directly tests GR reduction",
        ),
        (
            "ACQ1579_9_tau_clock",
            "tau_clock",
            "P2",
            "clock/redshift/fine-structure residual",
            "clock-specific projection plus constant/material sensitivity coefficients or superselection theorem",
            "external Galileo row exists, internal projection and constants absent",
            "source-intake/local_bounds/local_bound_claims.csv::Galileo_redshift_Delva_2018",
            "MISSING_CLOCK_PROJECTION",
            "keep as follow-on after PPN and material constants are controlled",
        ),
        (
            "ACQ1579_10_tau_orbital",
            "tau_orbital",
            "P1",
            "orbital/perihelion/timing residual",
            "orbital potential/acceleration kernel in same source frame as PPN denominator",
            "external LLR/Gdot row exists, internal projection absent",
            "source-intake/local_bounds/local_bound_claims.csv::LLR_Biskupek_Muller_Torre_2021",
            "MISSING_ORBITAL_PROJECTION",
            "derive after or alongside PPN source denominator",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "acquisition_id": acquisition_id,
            "symbol": symbol,
            "priority": priority,
            "why_needed": why_needed,
            "acceptable_source_form": acceptable_source_form,
            "current_evidence": current_evidence,
            "candidate_source_anchor": candidate_source_anchor,
            "current_status": current_status,
            "next_action": next_action,
            **flags(),
        }
        for acquisition_id, symbol, priority, why_needed, acceptable_source_form, current_evidence, candidate_source_anchor, current_status, next_action in rows
    ]


def external_bound_audit_rows() -> list[dict[str, Any]]:
    r10_rows = r10_review_rows()
    r10_all_nonclaim = all(row.get("valid_for_claim", "").strip().lower() == "false" for row in r10_rows)
    datasets = [
        ("EXT1579_1_PPN", "PPN", "Cassini_Shapiro_gamma_2003", "gamma_minus_1", "numeric_bound_available_but_internal_projection_missing"),
        ("EXT1579_2_clock", "clock", "Galileo_redshift_Delva_2018", "alpha_clock_redshift", "numeric_bound_available_but_internal_projection_missing"),
        ("EXT1579_3_orbital", "orbital", "LLR_Biskupek_Muller_Torre_2021", "Gdot_over_G", "numeric_bound_available_but_internal_projection_missing"),
        ("EXT1579_4_WEP", "WEP", "MICROSCOPE_final_TiPt", "eta_WEP_direct_geometry", "numeric_bound_available_but_internal_projection_missing"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "external_id": "EXT1579_0_R10",
            "arena": "R10",
            "source_path": rel(SOURCE_FILES["r10_review_candidate"]),
            "row_selector": "all review-candidate curve rows",
            "observable": "alpha_bound(lambda)",
            "row_count": len(r10_rows),
            "bound_summary": "digitized reviewed candidate curve, not accepted",
            "external_status": "REVIEW_CANDIDATE_NONCLAIM_ROWS_PRESENT" if r10_rows else "MISSING_R10_ROWS",
            "accepted_for_scoring": False,
            "dry_run_allowed": False,
            "reason_not_scoreable": "all valid_for_claim flags are false" if r10_all_nonclaim else "curve claim flags require manual audit",
            **flags(),
        }
    ]
    for external_id, arena, dataset_id, observable, status in datasets:
        row = local_bound_by_dataset(dataset_id)
        upper = row.get("upper_bound", "")
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "external_id": external_id,
                "arena": arena,
                "source_path": rel(SOURCE_FILES["local_bound_claims"]),
                "row_selector": dataset_id,
                "observable": observable,
                "row_count": 1 if row else 0,
                "bound_summary": f"upper_bound={upper} {row.get('units', '')}".strip() if row else "missing",
                "external_status": status if row else "MISSING_EXTERNAL_BOUND_ROW",
                "accepted_for_scoring": False,
                "dry_run_allowed": bool(row),
                "reason_not_scoreable": "external comparator exists but MTS internal component/projection rows are missing",
                **flags(),
            }
        )
    return rows


def comparator_dry_run_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DRY1579_0_R10",
            "R10",
            "alpha_MTS(lambda_R)",
            "R10 reviewed candidate curve",
            "Z_R;M_R^2;beta_S^R;beta_T^R;tau_R10/Xi_R10;alpha_boundary_tail;accepted alpha_bound(lambda)",
            "NOT_RUN_BLOCKED",
            "EXTERNAL_CURVE_NOT_ACCEPTED;INTERNAL_COMPONENTS_MISSING",
            "no alpha_MTS numeric row; no accepted alpha_bound(lambda)",
        ),
        (
            "DRY1579_1_PPN",
            "PPN",
            "gamma_minus_1=C_QR q_R_hat+tails",
            "Cassini gamma bound",
            "q_R_hat/Q_R;tau_PPN/C_QR;source denominator;boundary/source tail",
            "NOT_RUN_BLOCKED",
            "INTERNAL_PROJECTION_MISSING",
            "external bound exists, but no MTS PPN residual vector exists",
        ),
        (
            "DRY1579_2_clock",
            "clock",
            "delta_clock=tau_clock*(constant/material sensitivity)+tail",
            "Galileo redshift/LPI bound",
            "tau_clock;constant superselection or dtheta/dR_AB;material coefficients;tail",
            "NOT_RUN_BLOCKED",
            "INTERNAL_PROJECTION_MISSING",
            "external bound exists, but no constant/material projection exists",
        ),
        (
            "DRY1579_3_orbital",
            "orbital",
            "delta_orbital=tau_orbital*(J_R,Z_R,M_R^2,q_R_hat)+tail",
            "LLR/Gdot bound row",
            "tau_orbital;J_R;source denominator;Z_R/M_R^2 or q_R_hat;tail",
            "NOT_RUN_BLOCKED",
            "INTERNAL_PROJECTION_MISSING",
            "external bound exists, but no same-frame source denominator exists",
        ),
        (
            "DRY1579_4_WEP",
            "WEP",
            "eta_MTS=tau_WEP*(beta_S^R beta_T^R composition split)+tail",
            "MICROSCOPE Ti/Pt bound",
            "beta source/test material split;tau_WEP;no-marker theorem;tail",
            "NOT_RUN_BLOCKED",
            "BETA_AND_PROJECTION_MISSING",
            "external bound exists, but beta-zero theorem is conditional and finite beta rows are blank",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "dry_run_id": dry_run_id,
            "arena": arena,
            "mts_observable": mts_observable,
            "external_comparator": external_comparator,
            "required_missing_inputs": required_missing_inputs,
            "dry_run_status": dry_run_status,
            "blocker": blocker,
            "runner_detail": runner_detail,
            "mts_prediction_value": "",
            "comparator_bound_value": "",
            "can_score": False,
            "passes_for_claim": False,
            **flags(),
        }
        for dry_run_id, arena, mts_observable, external_comparator, required_missing_inputs, dry_run_status, blocker, runner_detail in rows
    ]


def runner_summary_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "summary_id": "RUN1579_0_external_ready",
            "status": "PARTIAL_EXTERNAL_COMPARATORS_EXIST",
            "detail": "PPN, WEP, clock and orbital bound rows exist locally; R10 curve is reviewed-only and not accepted",
            "claim_effect": "external readiness alone does not permit MTS scoring",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "summary_id": "RUN1579_1_internal_missing",
            "status": "INTERNAL_COMPONENTS_MISSING",
            "detail": "q_R_hat/Q_R, Z_R/M_R^2, beta legs, J_R, boundary tail and arena projections are blank or theorem-unsigned",
            "claim_effect": "all comparator rows remain blocked",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "summary_id": "RUN1579_2_best_next",
            "status": "PPN_RESIDUAL_VECTOR_FIRST",
            "detail": "tau_PPN/C_QR plus q_R_hat is the cleanest route because it directly tests local GR reduction rather than an isolated fifth-force score",
            "claim_effect": "next step is derivation-first, not public claim",
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1579_0_source_acquisition", "real finite component source row exists", "BLOCKED_NO_CLAIM", "ledger is source-ready but contains no accepted internal coefficients"),
        ("GATE1579_1_dry_comparator", "dry comparator may score MTS", "BLOCKED_NO_CLAIM", "all dry-run rows have can_score=false"),
        ("GATE1579_2_R10", "R10 comparison can be run", "BLOCKED_NO_CLAIM", "R10 curve remains reviewed-only and internal alpha_MTS inputs are missing"),
        ("GATE1579_3_PPN_local_GR", "PPN/local-GR residual vector can be tested", "BLOCKED_NO_CLAIM", "q_R_hat/Q_R and tau_PPN/C_QR are not derived or sourced"),
        ("GATE1579_4_public_claim", "any local-GR/R10/WEP/clock/orbital claim", "BLOCKED_NO_CLAIM", "no arena has both external comparator and complete internal MTS prediction"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1579_0_acquisition_state",
            "SOURCE_LEDGER_READY_NO_INTERNAL_VALUES",
            "the finite branch now has exact acquisition rows but no real internal coefficient has appeared",
            "no MTS finite residual can be scored yet",
        ),
        (
            "DEC1579_1_comparator_state",
            "EXTERNAL_COMPARATORS_EXIST_BUT_DRY_RUNS_BLOCK",
            "PPN/WEP/clock/orbital bounds exist locally and R10 has reviewed curve data, but internal MTS predictions are missing",
            "testing can start only after a first internal PPN/q_R or operator row is derived/sourced",
        ),
        (
            "DEC1579_2_next",
            "NEXT_1580_RAB_PPN_RESIDUAL_VECTOR_OR_QRHAT_SOURCE_ROW",
            "PPN is the least-dodgy next arena because it attacks the GR reduction directly rather than asking a fifth-force comparison to carry the theory",
            "derive gamma_minus_1=C_QR q_R_hat+tails or explicitly keep q_R_hat as a missing closure/source row",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            **flags(),
        }
        for decision_id, decision, reason, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1580-Y5-RAB-PPN-residual-vector-or-qRhat-source-row.md",
            "script": "scripts/Y5_RAB_PPN_residual_vector_or_qRhat_source_row.py",
            "objective": "derive the local PPN residual vector from finite R_AB/q_R_hat to gamma_minus_1, or prove that q_R_hat must remain a missing source/closure row",
            "do_not": "do not score Cassini or claim GR reduction until q_R_hat/Q_R, C_QR/tau_PPN, source denominator and boundary tails are derived or source-backed",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "parent_signed",
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "can_score",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def formalization_scope_clean(generated_csvs: list[Path]) -> bool:
    generated_paths = [Path(__file__).resolve(), DOC, *generated_csvs]
    generated_paths.extend(target for targets in COPY_TARGETS.values() for target in targets)
    if any(is_within(path, FORMALIZATION) for path in generated_paths):
        return False
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return True
    if result.returncode != 0:
        return True
    return len([line for line in result.stdout.splitlines() if line.strip()]) == 0


def has_1579_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1579" in path.name for path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    ledger = read_csv(ACQUISITION_LEDGER)
    external = read_csv(EXTERNAL_AUDIT)
    dry = read_csv(COMPARATOR_DRY_RUN)
    summary = read_csv(RUNNER_SUMMARY)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    required_symbols = {
        "q_R_hat or Q_R",
        "Z_R",
        "M_R^2",
        "beta_S^R",
        "beta_T^R",
        "J_R",
        "B_R, Pi_R^n, alpha_boundary_tail",
        "tau_R10 or Xi_R10",
        "tau_PPN or C_QR",
        "tau_clock",
        "tau_orbital",
    }
    checks = [
        ("VAL1579_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist"),
        ("VAL1579_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL1579_2_acquisition_symbols_complete",
            {row["symbol"] for row in ledger} == required_symbols,
            "acquisition ledger covers every 1578 finite component symbol",
        ),
        (
            "VAL1579_3_internal_rows_nonclaim",
            all(row["valid_for_claim"] == "False" and row["numeric_value_present"] == "False" for row in ledger),
            "component ledger is source-ready but contains no accepted internal coefficients",
        ),
        (
            "VAL1579_4_external_audit_present",
            {"R10", "PPN", "clock", "orbital", "WEP"} == {row["arena"] for row in external},
            "external audit covers R10, PPN, clock, orbital and WEP comparators",
        ),
        (
            "VAL1579_5_r10_not_accepted",
            any(row["arena"] == "R10" and row["accepted_for_scoring"] == "False" for row in external),
            "R10 reviewed curve remains not accepted for scoring",
        ),
        (
            "VAL1579_6_dry_runs_blocked",
            all(row["dry_run_status"] == "NOT_RUN_BLOCKED" and row["can_score"] == "False" for row in dry),
            "all dry comparator rows block scoring",
        ),
        (
            "VAL1579_7_runner_summary_next",
            any(row["status"] == "PPN_RESIDUAL_VECTOR_FIRST" for row in summary),
            "runner selects PPN residual vector as best next derivation target",
        ),
        (
            "VAL1579_8_claim_gates_closed",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in gates),
            "claim gates remain closed",
        ),
        (
            "VAL1579_9_decision_next",
            any(row["decision"] == "NEXT_1580_RAB_PPN_RESIDUAL_VECTOR_OR_QRHAT_SOURCE_ROW" for row in decisions),
            "decision selects PPN residual vector/q_Rhat source target",
        ),
        ("VAL1579_10_csv_parse", all(len(read_csv(path)) > 0 for path in generated_csvs), "all generated 1579 CSVs parse cleanly"),
        ("VAL1579_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1579_12_no_raw_accepted", not has_1579_rows(RAB_RAW) and not has_1579_rows(RAB_ACCEPTED), "no 1579 rows written to raw/accepted finite directories"),
        ("VAL1579_13_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets), "branch/quarantine nonclaim copies written"),
        ("VAL1579_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1579_15_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1579 paths are outside formalization-workbench; git status is clean when available"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1579_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1579 finite component source acquisition ledger and comparator dry-run validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")) for col in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    ledger: list[dict[str, Any]],
    external: list[dict[str, Any]],
    dry: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1579 - R_AB Finite Component Source Acquisition Ledger And Comparator Dry-Run",
                "## Verdict\n"
                "- The finite `R_AB` branch now has a source-acquisition ledger for every missing internal object from 1578.\n"
                "- External comparators exist locally for PPN, WEP, clock and orbital checks, while R10 has reviewed candidate curve rows only.\n"
                "- Every comparator dry-run is deliberately blocked because no arena has a complete internal MTS prediction row.\n"
                "- The strongest next move is not to score R10 first; it is to derive the PPN residual vector `gamma_minus_1=C_QR q_R_hat+tails`, because that attacks the local GR reduction directly.\n"
                "- No R10, PPN, WEP, clock, orbital, local GR/Newton, beta-zero, no-pole, `q_R=0`, or finite-component claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Component Source Acquisition Ledger",
                md_table(ledger, ["acquisition_id", "symbol", "priority", "why_needed", "current_status", "next_action"]),
                "## External Bound Audit",
                md_table(external, ["external_id", "arena", "row_selector", "row_count", "bound_summary", "external_status", "accepted_for_scoring"]),
                "## Comparator Dry-Run",
                md_table(dry, ["dry_run_id", "arena", "mts_observable", "required_missing_inputs", "dry_run_status", "blocker"]),
                "## Runner Summary",
                md_table(summary, ["summary_id", "status", "detail", "claim_effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "consequence"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    ledger = acquisition_ledger_rows()
    external = external_bound_audit_rows()
    dry = comparator_dry_run_rows()
    summary = runner_summary_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        ACQUISITION_LEDGER,
        EXTERNAL_AUDIT,
        COMPARATOR_DRY_RUN,
        RUNNER_SUMMARY,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(ACQUISITION_LEDGER, ledger)
    write_csv(EXTERNAL_AUDIT, external)
    write_csv(COMPARATOR_DRY_RUN, dry)
    write_csv(RUNNER_SUMMARY, summary)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, ledger, external, dry, summary, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
