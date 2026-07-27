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
QUARANTINE = MICROSCOPE / "quarantine" / "1581"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1581-Y5-RAB-qRhat-profile-and-Cassini-bound-row-or-no-charge-return.md"

SOURCE_FILES = {
    "1580_doc": ROOT / "1580-Y5-RAB-PPN-residual-vector-or-qRhat-source-row.md",
    "1580_validation": OUT / "P8_Y5_BRR545_1580_VALIDATION.csv",
    "1580_qrhat": OUT / "P8_Y5_PARENT_QLOC_1580_QRHAT_SOURCE_ROW_NONCLAIM.csv",
    "1580_cassini": OUT / "P8_Y5_PARENT_QLOC_1580_CASSINI_BOUND_CONTRACT.csv",
    "05_reciprocity": ROOT / "05-reciprocity-theorem-attempt.md",
    "06_source_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "1577_nocharge": OUT / "P8_Y5_PARENT_QLOC_1577_QR_NO_CHARGE_THEOREM_AUDIT.csv",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}

NEEDLES = {
    "1580_doc": ["NEXT_1581_RAB_QRHAT_PROFILE_AND_CASSINI_BOUND_ROW_OR_NO_CHARGE_RETURN", "q_R_hat~sigma_Q Q_R/(2GM)"],
    "1580_validation": ["VAL1580_OVERALL", "PASS"],
    "1580_qrhat": ["QRHAT1580_1_current_hair_target", "CONDITIONAL_BOUND_TARGET_VALUE_MISSING"],
    "1580_cassini": ["CAS1580_0_gamma_bound", "2.3e-05"],
    "05_reciprocity": ["W ~ r^2", "R_AB ~ Q_R/r."],
    "06_source_neutrality": ["Pi_R = 0 -> Q_R = 0 -> R_AB = 0 -> AB = 1.", "gamma - 1 ~= q_R."],
    "1577_nocharge": ["NCA1577_4_verdict", "NOT_DERIVED_CURRENT_CORPUS"],
    "local_bound_claims": ["Cassini_Shapiro_gamma_2003", "gamma_minus_1", "2.3e-05"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1581_SOURCE_REGISTER.csv"
PROFILE_DERIVATION = OUT / "P8_Y5_PARENT_QLOC_1581_QRHAT_PROFILE_DERIVATION.csv"
CASSINI_BOUND_ROW = OUT / "P8_Y5_PARENT_QLOC_1581_CASSINI_QR_BOUND_ROW_NONCLAIM.csv"
NO_CHARGE_RETURN = OUT / "P8_Y5_PARENT_QLOC_1581_NO_CHARGE_RETURN_AUDIT.csv"
PPN_DRY_RUN = OUT / "P8_Y5_PARENT_QLOC_1581_PPN_DRY_RUN_UPDATE.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1581_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1581_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1581_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1581_VALIDATION.csv"

COPY_TARGETS = {
    PROFILE_DERIVATION: [
        QUARANTINE / "QRHAT_PROFILE_DERIVATION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "qRhat_profile_derivation_nonclaim_1581.csv",
    ],
    CASSINI_BOUND_ROW: [
        QUARANTINE / "CASSINI_QR_BOUND_ROW_NONCLAIM.csv",
        BRANCH_RESIDUALS / "Cassini_QR_bound_row_nonclaim_1581.csv",
    ],
    NO_CHARGE_RETURN: [
        QUARANTINE / "NO_CHARGE_RETURN_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "QR_no_charge_return_audit_nonclaim_1581.csv",
    ],
    PPN_DRY_RUN: [
        QUARANTINE / "PPN_DRY_RUN_UPDATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "PPN_dry_run_update_nonclaim_1581.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "qRhat_profile_decision_nonclaim_1581.csv",
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


def cassini_upper_bound() -> str:
    for row in read_csv(SOURCE_FILES["local_bound_claims"]):
        if row.get("dataset_id") == "Cassini_Shapiro_gamma_2003":
            return row.get("upper_bound", "")
    return ""


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1581_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, NEEDLES[key]),
                "needles": "; ".join(NEEDLES[key]),
                "purpose": "derive q_R_hat radial hair profile and Cassini bound target or return to no-charge theorem",
                **flags(),
            }
        )
    return rows


def profile_derivation_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PROF1581_0_current_equation",
            "exterior current equation",
            "W(r) dR_AB/dr = Q_R",
            "05 and 1577",
            "FORMAL_INPUT",
            "ordinary current preserves Q_R rather than setting it to zero",
        ),
        (
            "PROF1581_1_asymptotic_weight",
            "radial asymptotic weight",
            "W(r)=kappa_W r^2[1+O(GM/r)]",
            "05 records W~r^2; kappa_W tracks normalization",
            "CONDITIONAL_ASYMPTOTIC_GRAMMAR",
            "kappa_W must be fixed by parent radial-cell normalization",
        ),
        (
            "PROF1581_2_profile",
            "reciprocal hair profile",
            "R_AB(r)=R_AB(infinity)-Q_R/(kappa_W r)+O(r^-2)",
            "integrate dR_AB/dr=Q_R/(kappa_W r^2) with asymptotic flatness",
            "DERIVED_CONDITIONAL_PROFILE",
            "sign convention and kappa_W normalization remain open",
        ),
        (
            "PROF1581_3_ppn_ratio",
            "dimensionless q_R_hat",
            "q_R_hat=R_AB/(2U_N)=-Q_R/(2 kappa_W G M)+O(GM/r)",
            "use U_N=GM/r and 1580 PPN bridge",
            "DERIVED_CONDITIONAL_BOUND_TARGET",
            "source mass M, kappa_W, gauge and tails remain unsourced",
        ),
        (
            "PROF1581_4_zero_route",
            "derived GR route",
            "Q_R=0 and tails=0 imply q_R_hat=0 and gamma_minus_1=0 at leading PPN order",
            "06 source-neutrality route",
            "SUFFICIENT_CONDITIONAL_NOT_PARENT_SIGNED",
            "Pi_R=0/source-neutral boundary theorem is still not parent-derived",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "profile_id": profile_id,
            "object": obj,
            "equation": equation,
            "derivation_basis": derivation_basis,
            "status": status,
            "blocking_gap": blocking_gap,
            **flags(),
        }
        for profile_id, obj, equation, derivation_basis, status, blocking_gap in rows
    ]


def cassini_bound_rows() -> list[dict[str, Any]]:
    upper = cassini_upper_bound()
    try:
        q_bound = float(upper)
        qr_over_gm_bound = 2.0 * q_bound
    except ValueError:
        q_bound = ""
        qr_over_gm_bound = ""
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_id": "CB1581_0_qRhat",
            "observable": "q_R_hat + PPN tails",
            "external_dataset_id": "Cassini_Shapiro_gamma_2003",
            "cassini_gamma_upper_bound": upper,
            "conditional_bound_expression": "abs(-Q_R/(2 kappa_W G M)+delta_gauge+delta_source+delta_boundary) <= 2.3e-05",
            "q_R_hat_bound_if_tails_zero": f"{q_bound:.6g}" if isinstance(q_bound, float) else "",
            "QR_over_GM_bound_if_kappa1_tails_zero": f"{qr_over_gm_bound:.6g}" if isinstance(qr_over_gm_bound, float) else "",
            "units": "dimensionless",
            "current_status": "CONDITIONAL_BOUND_ROW_NONCLAIM",
            "why_not_claim": "Q_R, kappa_W, source mass convention, PPN gauge and tails are not parent-signed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_id": "CB1581_1_nocharge_limit",
            "observable": "q_R_hat",
            "external_dataset_id": "internal theorem target",
            "cassini_gamma_upper_bound": upper,
            "conditional_bound_expression": "Q_R=0 plus zero tails gives q_R_hat=0, automatically within Cassini gamma at leading order",
            "q_R_hat_bound_if_tails_zero": "0 if no-charge theorem closes",
            "QR_over_GM_bound_if_kappa1_tails_zero": "0 if no-charge theorem closes",
            "units": "dimensionless",
            "current_status": "SUFFICIENT_IF_PARENT_SIGNED_NOT_CLAIMED",
            "why_not_claim": "Q_R=0 is still not derived from the parent source/boundary action",
            **flags(),
        },
    ]


def no_charge_return_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NCR1581_0_source_boundary",
            "Pi_R=0 source-boundary neutrality",
            "Pi_R=0 -> Q_R=0 -> R_AB=0 -> AB=1",
            "SUFFICIENT_CONDITIONAL",
            "06 writes this route, but source boundary class is not parent-derived",
        ),
        (
            "NCR1581_1_free_variation",
            "free/proper R_AB boundary variation",
            "delta S_boundary=[W R_AB' + Pi_R] delta R_AB; if Pi_R=0 then Q_R=0",
            "OPEN_NOT_SIGNED",
            "needs matter/source action to forbid hidden reciprocal momentum",
        ),
        (
            "NCR1581_2_constraint",
            "constraint/no-pole return",
            "lambda_R R_AB or no physical R_AB pole removes Q_R before PPN",
            "OPEN_NOT_SIGNED",
            "1576 and 1577 keep multiplier/current-chain owner unsigned",
        ),
        (
            "NCR1581_3_finite_bound",
            "finite hair fallback",
            "if Q_R is not zero, Cassini bounds Q_R/(kappa_W GM) through q_R_hat",
            "BOUND_TARGET_ONLY",
            "bound target is not a prediction and cannot replace derived GR",
        ),
        (
            "NCR1581_4_verdict",
            "best next route",
            "return to Q_R no-charge/source denominator plus PPN tail envelope",
            "NEXT_ROUTE",
            "without Q_R=0 or a sourced Q_R value, Cassini cannot be scored",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "route": route,
            "condition": condition,
            "status": status,
            "why_not_claim": why_not_claim,
            **flags(),
        }
        for audit_id, route, condition, status, why_not_claim in rows
    ]


def ppn_dry_run_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "dry_run_id": "PPN1581_0_Cassini_QR_bound",
            "arena": "PPN/Cassini gamma",
            "bound_expression": "abs(-Q_R/(2 kappa_W G M)+tails) <= 2.3e-05",
            "derived_profile_status": "CONDITIONAL_PROFILE_READY",
            "missing_for_score": "Q_R value or Q_R=0 theorem; kappa_W normalization; source mass convention; gauge/source/boundary tails",
            "dry_run_status": "NOT_RUN_BLOCKED",
            "can_score": False,
            "passes_for_claim": False,
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "dry_run_id": "PPN1581_1_GR_zero_limit",
            "arena": "derived local GR gamma channel",
            "bound_expression": "Q_R=0 and tails=0 -> gamma_minus_1=0",
            "derived_profile_status": "SUFFICIENT_CONDITIONAL_NOT_PARENT_SIGNED",
            "missing_for_score": "parent no-charge theorem and tail silence",
            "dry_run_status": "NOT_RUN_BLOCKED",
            "can_score": False,
            "passes_for_claim": False,
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1581_0_profile", "q_R_hat radial profile is derived", "PASS_FORMAL_NONCLAIM", "profile follows conditionally from W R_AB'=Q_R and W~r^2"),
        ("GATE1581_1_Cassini_bound", "Cassini gives a conditional Q_R/(GM) bound target", "PASS_FORMAL_NONCLAIM", "bound expression is algebraic but not a prediction"),
        ("GATE1581_2_QR_value", "Q_R value or Q_R=0 theorem exists", "BLOCKED_NO_CLAIM", "Q_R remains unsourced and no-charge theorem is unsigned"),
        ("GATE1581_3_PPN_score", "PPN/Cassini can be scored", "BLOCKED_NO_CLAIM", "kappa_W, source mass, gauge and tails are missing"),
        ("GATE1581_4_local_GR", "derived local GR/Newton branch", "BLOCKED_NO_CLAIM", "gamma channel alone is conditional and beta/conservation/common matter coupling remain open"),
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
            "DEC1581_0_progress",
            "QRHAT_PROFILE_AND_CASSINI_BOUND_TARGET_DERIVED_CONDITIONALLY",
            "finite reciprocal hair maps to q_R_hat=-Q_R/(2 kappa_W G M), giving a concrete Cassini pressure row",
            "the local branch is now test-shaped, but not test-passed",
        ),
        (
            "DEC1581_1_claim_ceiling",
            "NO_PPN_OR_GR_CLAIM",
            "a bound target is not an MTS prediction while Q_R and tails are unknown",
            "do not promote Cassini, PPN, or local-GR claims",
        ),
        (
            "DEC1581_2_next",
            "NEXT_1582_QR_NO_CHARGE_SOURCE_DENOMINATOR_AND_TAIL_ENVELOPE",
            "the least-scrutiny path is to prove Q_R=0/tails=0; the fallback path is a sourced finite Q_R/(GM) row",
            "try the no-charge/source-boundary theorem with a PPN tail envelope",
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
            "next_target": "1582-Y5-QR-no-charge-source-denominator-and-tail-envelope.md",
            "script": "scripts/Y5_QR_no_charge_source_denominator_and_tail_envelope.py",
            "objective": "prove Q_R=0 from source-boundary/no-charge conditions or construct the absolute PPN tail/source-denominator envelope needed before any Cassini score",
            "do_not": "do not claim local GR from the conditional q_R_hat profile; do not cancel tails; do not score Cassini without Q_R and kappa_W/source normalization",
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


def has_1581_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1581" in path.name for path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    profile = read_csv(PROFILE_DERIVATION)
    bound = read_csv(CASSINI_BOUND_ROW)
    nocharge = read_csv(NO_CHARGE_RETURN)
    dry = read_csv(PPN_DRY_RUN)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    checks = [
        ("VAL1581_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist"),
        ("VAL1581_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL1581_2_profile_formula",
            any(row["profile_id"] == "PROF1581_3_ppn_ratio" and "Q_R/(2 kappa_W G M)" in row["equation"] for row in profile),
            "q_R_hat profile relation is recorded",
        ),
        (
            "VAL1581_3_cassini_bound_target",
            any(row["bound_id"] == "CB1581_0_qRhat" and row["QR_over_GM_bound_if_kappa1_tails_zero"] == "4.6e-05" for row in bound),
            "conditional Cassini target bound on Q_R/(GM) is recorded",
        ),
        (
            "VAL1581_4_nocharge_not_claimed",
            any(row["audit_id"] == "NCR1581_4_verdict" and row["status"] == "NEXT_ROUTE" for row in nocharge),
            "no-charge route is selected as next route but not claimed",
        ),
        (
            "VAL1581_5_ppn_dry_run_blocked",
            all(row["dry_run_status"] == "NOT_RUN_BLOCKED" and row["can_score"] == "False" for row in dry),
            "PPN dry-run rows remain blocked",
        ),
        (
            "VAL1581_6_claim_gates_closed",
            all(row["claim_allowed"] == "False" for row in gates),
            "claim gates remain nonclaim even when profile and bound target pass formally",
        ),
        (
            "VAL1581_7_decision_next",
            any(row["decision"] == "NEXT_1582_QR_NO_CHARGE_SOURCE_DENOMINATOR_AND_TAIL_ENVELOPE" for row in decisions),
            "decision selects Q_R no-charge/source denominator and tail envelope",
        ),
        ("VAL1581_8_csv_parse", all(len(read_csv(path)) > 0 for path in generated_csvs), "all generated 1581 CSVs parse cleanly"),
        ("VAL1581_9_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1581_10_no_raw_accepted", not has_1581_rows(RAB_RAW) and not has_1581_rows(RAB_ACCEPTED), "no 1581 rows written to raw/accepted finite directories"),
        ("VAL1581_11_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets), "branch/quarantine nonclaim copies written"),
        ("VAL1581_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1581_13_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1581 paths are outside formalization-workbench; git status is clean when available"),
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
            "check_id": "VAL1581_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1581 q_R_hat profile and Cassini bound-row validation",
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
    profile: list[dict[str, Any]],
    bound: list[dict[str, Any]],
    nocharge: list[dict[str, Any]],
    dry: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1581 - R_AB q_R_hat Profile And Cassini Bound Row Or No-Charge Return",
                "## Verdict\n"
                "- The exterior current-hair profile is now explicit: with `W(r)=kappa_W r^2`, `R_AB=-Q_R/(kappa_W r)+O(r^-2)` after asymptotic flatness.\n"
                "- Using the 1580 PPN bridge gives `q_R_hat=-Q_R/(2 kappa_W G M)+O(GM/r)`, so Cassini pressures the dimensionless reciprocal charge directly.\n"
                "- If `kappa_W=1` and all tails vanish, the Cassini row implies the conditional target `|Q_R/(G M)| <= 4.6e-05`; this is not an MTS prediction or pass.\n"
                "- The clean GR route is still `Q_R=0` plus tail silence from a parent source-boundary/no-charge theorem.\n"
                "- No Cassini, PPN, local GR/Newton, no-charge, finite-hair, R10, WEP, clock, orbital, beta, or conservation claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## q_R_hat Profile Derivation",
                md_table(profile, ["profile_id", "object", "equation", "status", "blocking_gap"]),
                "## Cassini Q_R Bound Row",
                md_table(bound, ["bound_id", "observable", "conditional_bound_expression", "q_R_hat_bound_if_tails_zero", "QR_over_GM_bound_if_kappa1_tails_zero", "current_status"]),
                "## No-Charge Return Audit",
                md_table(nocharge, ["audit_id", "route", "condition", "status", "why_not_claim"]),
                "## PPN Dry Run Update",
                md_table(dry, ["dry_run_id", "arena", "bound_expression", "missing_for_score", "dry_run_status"]),
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
    profile = profile_derivation_rows()
    bound = cassini_bound_rows()
    nocharge = no_charge_return_rows()
    dry = ppn_dry_run_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        PROFILE_DERIVATION,
        CASSINI_BOUND_ROW,
        NO_CHARGE_RETURN,
        PPN_DRY_RUN,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(PROFILE_DERIVATION, profile)
    write_csv(CASSINI_BOUND_ROW, bound)
    write_csv(NO_CHARGE_RETURN, nocharge)
    write_csv(PPN_DRY_RUN, dry)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, profile, bound, nocharge, dry, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
