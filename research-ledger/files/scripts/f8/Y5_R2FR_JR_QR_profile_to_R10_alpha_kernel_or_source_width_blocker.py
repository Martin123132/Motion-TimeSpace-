from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1632"
INPUT_1632 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1632-Y5-R2FR-JR-QR-profile-to-R10-alpha-kernel-or-source-width-blocker.md"

SOURCE_FILES = {
    "1631_doc": ROOT / "1631-Y5-R2FR-JR-prior-width-source-acquisition-or-tau-kernel-first-row.md",
    "1631_validation": OUT / "P8_Y5_BRR545_1631_VALIDATION.csv",
    "1631_next": OUT / "P8_Y5_PARENT_QLOC_1631_NEXT_TARGET.csv",
    "1631_r10_asset": OUT / "P8_Y5_PARENT_QLOC_1631_R10_BOUND_ASSET_LEDGER.csv",
    "1631_blocker": OUT / "P8_Y5_PARENT_QLOC_1631_ACQUISITION_BLOCKER_LEDGER.csv",
    "1630_refusal": OUT / "P8_Y5_PARENT_QLOC_1630_PRIOR_WIDTH_REFUSAL_RUNNER.csv",
    "1629_prior_widths": OUT / "P8_Y5_PARENT_QLOC_1629_FINITE_JR_PIR_PRIOR_WIDTH_ROWS.csv",
    "04_vacuum_contract": ROOT / "04-vacuum-reciprocity-action-contract.md",
    "05_reciprocity_attempt": ROOT / "05-reciprocity-theorem-attempt.md",
    "06_source_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "1035_green_kernel": ROOT / "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
    "r10_reviewed_curve": QUEUE / "R10_alpha_lambda_bound_curve_DIGITIZED_1572_REVIEWED_CANDIDATE_NONCLAIM.csv",
}

NEEDLES = {
    "1631_doc": ["NEXT_1632_JR_QR_PROFILE_TO_R10_ALPHA_KERNEL_OR_SOURCE_WIDTH_BLOCKER", "VAL1631_OVERALL"],
    "1631_validation": ["VAL1631_OVERALL", "PASS"],
    "1631_next": ["1632-Y5-R2FR-JR-QR-profile-to-R10-alpha-kernel-or-source-width-blocker.md", "alpha_R(lambda)"],
    "1631_r10_asset": ["COMPARISON_BOUND_ASSET_PRESENT_NONCLAIM", "MTS tau_R10 kernel"],
    "1631_blocker": ["BLK1631_2_R10_asset", "derive tau_R10 kernel next"],
    "1630_refusal": ["RUN1630_4_tau_R10_width", "REFUSE_SCORING"],
    "1629_prior_widths": ["PW1629_4_tau_R10_width", "MISSING_R10_WIDTH_KERNEL"],
    "04_vacuum_contract": ["d/dr [ W(r,L,fields) dR_AB/dr ] = J_R", "J_R = 0 in local vacuum"],
    "05_reciprocity_attempt": ["R_AB ~ Q_R/r", "Q_R = integral J_R dr = 0"],
    "06_source_neutrality": ["Q_R = -Pi_R", "R_AB = q_R L"],
    "1035_green_kernel": ["KXD1035_1_static_green_function", "alpha_X(lambda_X)=K_X^pt beta_s beta_t"],
    "r10_reviewed_curve": ["REVIEWED_QA_CANDIDATE_NONCLAIM", "alpha_abs_bound"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1632_SOURCE_REGISTER.csv"
KERNEL_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1632_TAU_R10_KERNEL_CONTRACT.csv"
PROFILE_MODE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1632_RAB_PROFILE_MODE_AUDIT.csv"
ALPHA_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1632_ALPHA_TEMPLATE_NONCLAIM.csv"
JOIN_READINESS = OUT / "P8_Y5_PARENT_QLOC_1632_R10_JOIN_READINESS.csv"
BLOCKER_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1632_KERNEL_BLOCKER_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1632_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1632_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1632_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1632_VALIDATION.csv"

COPY_TARGETS = {
    KERNEL_CONTRACT: [
        QUARANTINE / "TAU_R10_KERNEL_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_tau_R10_kernel_contract_nonclaim_1632.csv",
    ],
    PROFILE_MODE_AUDIT: [
        QUARANTINE / "RAB_PROFILE_MODE_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_RAB_profile_mode_audit_nonclaim_1632.csv",
    ],
    ALPHA_TEMPLATE: [
        QUARANTINE / "ALPHA_TEMPLATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_alpha_template_nonclaim_1632.csv",
        QUEUE / "JR1632_ALPHA_TEMPLATE_NONCLAIM.csv",
    ],
    JOIN_READINESS: [
        QUARANTINE / "R10_JOIN_READINESS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_R10_join_readiness_nonclaim_1632.csv",
    ],
    BLOCKER_LEDGER: [
        QUARANTINE / "KERNEL_BLOCKER_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_kernel_blocker_ledger_nonclaim_1632.csv",
        QUEUE / "JR1632_KERNEL_BLOCKER_LEDGER_NONCLAIM.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1632.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1632.csv",
    ],
}


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def file_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def all_needles_found(source_id: str) -> bool:
    text = file_text(SOURCE_FILES[source_id])
    return all(needle in text for needle in NEEDLES[source_id])


def ensure_dirs() -> None:
    for directory in [OUT, INPUT_1632, BRANCH_RESIDUALS, QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
    except Exception:
        return False
    return True


def bool_str(value: Any) -> str:
    return str(value).strip().lower()


def row_has_true_claim_flag(row: dict[str, Any]) -> bool:
    for field in ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "accepted_for_scoring", "kernel_numeric"]:
        if field in row and bool_str(row[field]) == "true":
            return True
    return False


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": source_id,
            "source_path": rel(path),
            "exists": path.exists(),
            "required_needles": "; ".join(NEEDLES[source_id]),
            "needles_found": all_needles_found(source_id),
            "role": "1632 reciprocal-hair to R10 alpha-kernel provenance",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path in SOURCE_FILES.items()
    ]


def kernel_contract_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KERN1632_0_source_equation",
            "reciprocal source equation",
            "d/dr[W dR_AB/dr]=J_R and Q_R=W R_AB'",
            "SUPPORTED_BY_04_05_06",
            "gives source/charge language but not a finite R10 range",
        ),
        (
            "KERN1632_1_massless_profile",
            "massless reciprocal hair",
            "R_AB ~ Q_R/r or R_AB=q_R L",
            "LOCAL_PPN_PROFILE_NOT_R10_YUKAWA",
            "useful for PPN/local limit; not an alpha(lambda) R10 curve without range/profile conversion",
        ),
        (
            "KERN1632_2_finite_operator",
            "finite-range reciprocal operator",
            "Z_R (nabla^2-lambda_R^-2) R_AB = -J_R",
            "CONDITIONAL_OPERATOR_FORM",
            "specializes 1035 Green-kernel form to R_AB only if Z_R and lambda_R are parent-sourced",
        ),
        (
            "KERN1632_3_green_solution",
            "static Green solution",
            "R_AB(r)=Q_R exp(-r/lambda_R)/(4*pi*Z_R*r) under point-source normalization",
            "CONDITIONAL_GREEN_KERNEL",
            "requires Q_R, Z_R, lambda_R, and source convention",
        ),
        (
            "KERN1632_4_source_test_product",
            "two-body exchange product",
            "alpha_R(lambda)=K_R^R10(lambda) beta_source^R(lambda) beta_test^R(lambda)+epsilon_tail(lambda)",
            "CONDITIONAL_PRODUCT_LAW",
            "cannot score linear-in-one-coupling shortcut; both source and test/readout legs must be owned",
        ),
        (
            "KERN1632_5_R10_projection",
            "R10 torque/profile projection",
            "K_R^R10(lambda)=K_R^pt F_ST^R(lambda) Pi_R10^R(lambda)",
            "SYMBOLIC_PROFILE_CONTRACT",
            "needs R10 support integrals or official harmonic projection for the reciprocal source current",
        ),
        (
            "KERN1632_6_verdict",
            "tau_R10 kernel",
            "KERN1632_2 through KERN1632_5 numeric/source-backed",
            "TAU_R10_KERNEL_CONTRACT_CONDITIONAL_VALUES_MISSING",
            "write blocker ledger; no R10 score",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "kernel_id": kernel_id,
            "step": step,
            "mathematical_statement": statement,
            "status": status,
            "effect": effect,
            "kernel_numeric": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for kernel_id, step, statement, status, effect in rows
    ]


def profile_mode_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PROF1632_0_zero_mode",
            "J_R=Pi_R=Q_R=0",
            "R_AB=0, no reciprocal force",
            "BEST_THEOREM_ROUTE_BUT_UNSIGNED",
            "blocked by 1627-1630 source-slot/action-scale gates",
        ),
        (
            "PROF1632_1_massless_tail",
            "Q_R nonzero, no mass/range",
            "R_AB~Q_R/r",
            "PPN_LOCAL_TAIL_NOT_R10_FINITE_RANGE",
            "must be routed to PPN/local residual, not finite-lambda R10 score",
        ),
        (
            "PROF1632_2_massive_yukawa",
            "Q_R nonzero with M_R^2/Z_R range",
            "R_AB~Q_R exp(-r/lambda_R)/(4*pi Z_R r)",
            "R10_COMPATIBLE_IF_SOURCED",
            "requires parent Z_R/M_R^2/lambda_R and charge normalization",
        ),
        (
            "PROF1632_3_boundary_tail",
            "Pi_R boundary source",
            "Q_R=-Pi_R with boundary support profile",
            "BOUNDARY_PROFILE_MISSING",
            "requires surface convention and finite-size projection",
        ),
        (
            "PROF1632_4_hidden_tail",
            "epsilon_tail(lambda)",
            "non-Hilbert/domain/source-support residual envelope",
            "ABSOLUTE_ENVELOPE_MISSING",
            "no-cancellation guard requires absolute bound for retained tails",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "profile_id": profile_id,
            "mode": mode,
            "profile_law": law,
            "status": status,
            "missing_for_score": missing,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for profile_id, mode, law, status, missing in rows
    ]


def alpha_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "template_id": "ALPHA1632_0_reciprocal_R10_template",
            "lambda_value_m": "MISSING_PARENT_LAMBDA_R_GRID_OR_JOIN_TO_R10_BOUND_GRID",
            "alpha_predicted": "MISSING_KR_BETA_SOURCE_BETA_TEST_EPSILON_TAIL",
            "alpha_abs_bound_source": rel(SOURCE_FILES["r10_reviewed_curve"]),
            "formula": "alpha_R(lambda)=K_R^R10(lambda)*beta_source_R(lambda)*beta_test_R(lambda)+epsilon_tail_R(lambda)",
            "required_inputs": "Z_R;M_R^2_or_lambda_R;Q_R_or_J_R_profile;Pi_R_boundary_profile;beta_source_R;beta_test_R;F_ST^R;Pi_R10^R;epsilon_tail_R;G_N_normalization",
            "current_status": "TEMPLATE_INVALID_MISSING_KERNEL_AND_AMPLITUDES",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def join_readiness_rows() -> list[dict[str, Any]]:
    rows = [
        ("JOIN1632_0_bound_curve", "external alpha_bound(lambda)", "COMPARISON_BOUND_ASSET_PRESENT_NONCLAIM", "human/official promotion still needed before claim; usable as private comparison asset only"),
        ("JOIN1632_1_lambda_R", "MTS reciprocal range lambda_R", "MISSING_PARENT_RANGE_RELATION", "need M_R^2/Z_R or sourced range profile"),
        ("JOIN1632_2_K_R", "R10-normalized Green/profile factor", "MISSING_KR_PROFILE_HARMONIC", "need K_R^pt, source/test support, R10 torque projection"),
        ("JOIN1632_3_beta_source", "source reciprocal charge leg", "MISSING_BETA_SOURCE_R", "need J_R/Q_R/Pi_R source normalization"),
        ("JOIN1632_4_beta_test", "test/readout reciprocal charge leg", "MISSING_BETA_TEST_R", "need detector/test-body coupling to reciprocal profile"),
        ("JOIN1632_5_tail", "absolute retained tail envelope", "MISSING_EPSILON_TAIL", "need no-cancellation absolute envelope"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "join_id": join_id,
            "join_object": obj,
            "current_status": status,
            "needed_for_join": needed,
            "ready_for_join": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for join_id, obj, status, needed in rows
    ]


def blocker_rows() -> list[dict[str, Any]]:
    rows = [
        ("BLK1632_0_range", "lambda_R/M_R^2", "MISSING_PARENT_RANGE_RELATION", "massless Q_R/r profile is not a finite-lambda R10 prediction", "derive/source Z_R and M_R^2/lambda_R"),
        ("BLK1632_1_source_charge", "J_R/Q_R/Pi_R source leg", "MISSING_SOURCE_CHARGE_NORMALIZATION", "finite widths exist only as MISSING templates", "source Q_R/J_R/Pi_R or zero theorem"),
        ("BLK1632_2_test_charge", "test/readout reciprocal leg", "MISSING_TEST_CHARGE_NORMALIZATION", "R10 is a two-body product, not one source amplitude", "derive beta_test_R/tau_R10 readout leg"),
        ("BLK1632_3_profile", "R10 profile/harmonic projection", "MISSING_R10_PROFILE_HARMONIC_KERNEL", "need F_ST and Pi_R10 for reciprocal current distribution", "source official geometry kernel or derive symbolic nonclaim row"),
        ("BLK1632_4_newton_norm", "Newton/G_N normalization", "MISSING_PARENT_NEWTON_MATCH", "alpha is dimensionless only after dividing by same Newton convention", "connect to local Newton limit or keep nonclaim"),
        ("BLK1632_5_tail", "absolute tail envelope", "MISSING_ABSOLUTE_TAIL_ENVELOPE", "hidden/source/domain tails cannot cancel silently", "build no-cancellation envelope"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "target": target,
            "status": status,
            "why_blocks_R10": why,
            "next_action": next_action,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for blocker_id, target, status, why, next_action in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("CG1632_0_kernel_numeric", "tau_R10 kernel numeric/source-backed", "BLOCKED", "conditional kernel has missing range, charge, profile, and normalization"),
        ("CG1632_1_alpha_template", "alpha_R(lambda) prediction row scoreable", "BLOCKED", "alpha template contains MISSING inputs"),
        ("CG1632_2_R10_comparison", "R10 comparison/pass", "BLOCKED", "external bound cannot be joined to missing MTS prediction"),
        ("CG1632_3_PPN_local", "local GR/Newton/PPN recovery", "BLOCKED", "massless and finite reciprocal profiles remain unbounded/nonzero"),
        ("CG1632_4_theorem_zero", "J_R/Pi_R/Q_R zero theorem", "BLOCKED", "source-slot/action-scale gates remain unsigned"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in claims
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1632_0_kernel",
            "decision": "TAU_R10_KERNEL_CONTRACT_CONDITIONAL_VALUES_MISSING",
            "reason": "the Green-kernel/product law is known conditionally, but R_AB range/source/test/profile normalization is not sourced",
            "next_action": "do not score; derive/source the reciprocal quadratic/profile row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1632_1_massless",
            "decision": "MASSLESS_QR_PROFILE_IS_PPN_NOT_R10",
            "reason": "R_AB~Q_R/r maps to local/PPN residuals, not a finite-lambda Yukawa curve without a range owner",
            "next_action": "separate massless local tail from massive R10 branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1632_2_next",
            "decision": "NEXT_1633_RAB_QUADRATIC_RANGE_AND_CHARGE_ROW_OR_MASSLESS_TAIL_DEMOTION",
            "reason": "R10 scoring requires Z_R, M_R^2/lambda_R, beta_source, beta_test, and profile projection",
            "next_action": "build the reciprocal quadratic/profile row or demote R10 to blocked until finite-range source exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1633-Y5-R2FR-RAB-quadratic-range-and-charge-row-or-massless-tail-demotion.md",
            "script": "scripts/Y5_R2FR_RAB_quadratic_range_and_charge_row_or_massless_tail_demotion.py",
            "objective": "try to source or derive the reciprocal quadratic/profile row containing Z_R, M_R^2/lambda_R, J_R/Q_R/Pi_R source normalization, beta_source_R, beta_test_R, and tail envelope; if no finite range exists, demote R10 branch and route massless Q_R/r to PPN/local residuals",
            "success_condition": "either a nonclaim reciprocal quadratic/profile row is staged with all required fields, or the R10 branch is explicitly blocked as missing finite-range owner and massless tail is routed to PPN/local blockers",
            "do_not": "do not treat Q_R/r as finite-lambda R10, do not invent Z_R/M_R/lambda_R or charges, do not score the R10 bound curve, do not claim local GR/Newton/R10/PPN pass",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_paths() -> list[Path]:
    return [
        SOURCE_REGISTER,
        KERNEL_CONTRACT,
        PROFILE_MODE_AUDIT,
        ALPHA_TEMPLATE,
        JOIN_READINESS,
        BLOCKER_LEDGER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    for source_id, source in SOURCE_FILES.items():
        if source.exists():
            shutil.copyfile(source, INPUT_1632 / f"{source_id}{source.suffix}")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    paths = generated_paths()
    kernel_rows = read_csv(KERNEL_CONTRACT)
    profile_rows = read_csv(PROFILE_MODE_AUDIT)
    alpha_rows = read_csv(ALPHA_TEMPLATE)
    join_rows = read_csv(JOIN_READINESS)
    blocker_data = read_csv(BLOCKER_LEDGER)
    claim_rows = read_csv(CLAIM_GATE)
    decision_text = file_text(DECISION)
    next_text = file_text(NEXT_TARGET)
    all_rows: list[dict[str, Any]] = []
    for path in paths:
        all_rows.extend(read_csv(path))

    source_ok = all(path.exists() for path in SOURCE_FILES.values())
    needles_ok = all(all_needles_found(source_id) for source_id in SOURCE_FILES)
    conditional_kernel = any(row["kernel_id"] == "KERN1632_6_verdict" and row["status"] == "TAU_R10_KERNEL_CONTRACT_CONDITIONAL_VALUES_MISSING" for row in kernel_rows)
    massless_separated = any(row["profile_id"] == "PROF1632_1_massless_tail" and row["status"] == "PPN_LOCAL_TAIL_NOT_R10_FINITE_RANGE" for row in profile_rows)
    alpha_nonclaim = len(alpha_rows) == 1 and alpha_rows[0]["accepted_for_scoring"] == "False" and "MISSING" in " ".join(alpha_rows[0].values())
    join_blocked = all(row["ready_for_join"] == "False" for row in join_rows)
    blocker_cover = {row["target"] for row in blocker_data} == {
        "lambda_R/M_R^2",
        "J_R/Q_R/Pi_R source leg",
        "test/readout reciprocal leg",
        "R10 profile/harmonic projection",
        "Newton/G_N normalization",
        "absolute tail envelope",
    }
    claim_closed = all(row["status"] == "BLOCKED" and not row_has_true_claim_flag(row) for row in claim_rows)
    nonclaim_ok = all(not row_has_true_claim_flag(row) for row in all_rows)
    decision_next = "NEXT_1633_RAB_QUADRATIC_RANGE_AND_CHARGE_ROW_OR_MASSLESS_TAIL_DEMOTION" in decision_text
    next_selected = "1633-Y5-R2FR-RAB-quadratic-range-and-charge-row-or-massless-tail-demotion.md" in next_text
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    csv_ok = all(csv_parses(path) for path in paths)
    pycache_absent = not (Path(__file__).resolve().parent / "__pycache__").exists()
    formalization_clean = not any((FORMALIZATION / path.name).exists() for path in [DOC, *paths]) if FORMALIZATION.exists() else True

    checks = [
        ("VAL1632_0_sources_exist", source_ok, "all cited 1632 local source paths exist"),
        ("VAL1632_1_needles_found", needles_ok, "all required 1632 source needles found"),
        ("VAL1632_2_conditional_kernel", conditional_kernel, "tau_R10 kernel contract is conditional with values missing"),
        ("VAL1632_3_massless_separated", massless_separated, "massless Q_R/r profile is separated from finite-lambda R10"),
        ("VAL1632_4_alpha_nonclaim", alpha_nonclaim, "alpha template remains MISSING-marker nonclaim"),
        ("VAL1632_5_join_blocked", join_blocked, "R10 join readiness remains blocked"),
        ("VAL1632_6_blocker_coverage", blocker_cover, "blocker ledger covers range, source/test legs, profile, Newton norm, tail"),
        ("VAL1632_7_claim_gates_closed", claim_closed, "all claim gates remain blocked"),
        ("VAL1632_8_nonclaim_flags", nonclaim_ok, "all generated 1632 rows remain nonclaim/non-score-ready"),
        ("VAL1632_9_decision_next", decision_next, "decision selects reciprocal quadratic/profile row next"),
        ("VAL1632_10_next_target_selected", next_selected, "next target selected"),
        ("VAL1632_11_branch_copies", branch_copies, "branch/quarantine/acquisition queue nonclaim copies exist"),
        ("VAL1632_12_csv_parse", csv_ok, "all generated 1632 CSVs parse"),
        ("VAL1632_13_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1632_14_formalization_untouched", formalization_clean, "no 1632 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1632_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1632 J_R/Q_R profile to R10 alpha kernel validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, str]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    source_rows = read_csv(SOURCE_REGISTER)
    kernel_rows = read_csv(KERNEL_CONTRACT)
    profile_rows = read_csv(PROFILE_MODE_AUDIT)
    alpha_rows = read_csv(ALPHA_TEMPLATE)
    join_rows = read_csv(JOIN_READINESS)
    blockers = read_csv(BLOCKER_LEDGER)
    claims = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    validation = read_csv(VALIDATION)

    content = f"""# 1632 — `J_R/Q_R` Profile To R10 `alpha(lambda)` Kernel Or Source-Width Blocker

## Status

Private checkpoint. No R10 score, finite `J_R/Q_R/Pi_R` claim, local-GR/Newton, PPN, clock, or orbital claim is made.

## Outcome

The conditional kernel shape is now explicit: if the reciprocal branch supplies a finite-range quadratic operator, source/test reciprocal charges, R10 profile/harmonic projection, Newton normalization, and an absolute tail envelope, then `alpha_R(lambda)=K_R^R10(lambda) beta_source_R beta_test_R + epsilon_tail_R`. Current corpus does not supply those values. The massless `Q_R/r` profile is separated as a PPN/local-tail issue, not a finite-lambda R10 prediction.

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "needles_found"])}

## Tau R10 Kernel Contract

{markdown_table(kernel_rows, ["kernel_id", "step", "status", "effect"])}

## RAB Profile Mode Audit

{markdown_table(profile_rows, ["profile_id", "mode", "status", "missing_for_score"])}

## Alpha Template

{markdown_table(alpha_rows, ["template_id", "formula", "current_status", "accepted_for_scoring"])}

## Join Readiness

{markdown_table(join_rows, ["join_id", "join_object", "current_status", "needed_for_join"])}

## Blocker Ledger

{markdown_table(blockers, ["blocker_id", "target", "status", "next_action"])}

## Claim Gates

{markdown_table(claims, ["gate_id", "claim", "status", "reason"])}

## Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_target, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        KERNEL_CONTRACT: kernel_contract_rows(),
        PROFILE_MODE_AUDIT: profile_mode_rows(),
        ALPHA_TEMPLATE: alpha_template_rows(),
        JOIN_READINESS: join_readiness_rows(),
        BLOCKER_LEDGER: blocker_rows(),
        CLAIM_GATE: claim_gate_rows(),
        DECISION: decision_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
