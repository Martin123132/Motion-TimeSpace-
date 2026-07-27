from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1633"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1633-Y5-R2FR-RAB-quadratic-range-and-charge-row-or-massless-tail-demotion.md"

SOURCE_FILES = {
    "1632_doc": ROOT / "1632-Y5-R2FR-JR-QR-profile-to-R10-alpha-kernel-or-source-width-blocker.md",
    "1632_validation": OUT / "P8_Y5_BRR545_1632_VALIDATION.csv",
    "1632_next": OUT / "P8_Y5_PARENT_QLOC_1632_NEXT_TARGET.csv",
    "04_vacuum_contract": ROOT / "04-vacuum-reciprocity-action-contract.md",
    "05_reciprocity_attempt": ROOT / "05-reciprocity-theorem-attempt.md",
    "06_source_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "07_nonpropagating_constraint": ROOT / "07-nonpropagating-reciprocity-constraint.md",
    "1035_green_kernel": ROOT / "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
    "r10_reviewed_curve": QUEUE / "R10_alpha_lambda_bound_curve_DIGITIZED_1572_REVIEWED_CANDIDATE_NONCLAIM.csv",
}

NEEDLES = {
    "1632_doc": [
        "TAU_R10_KERNEL_CONTRACT_CONDITIONAL_VALUES_MISSING",
        "MASSLESS_QR_PROFILE_IS_PPN_NOT_R10",
    ],
    "1632_validation": ["VAL1632_OVERALL", "PASS"],
    "1632_next": [
        "1633-Y5-R2FR-RAB-quadratic-range-and-charge-row-or-massless-tail-demotion.md",
        "do not treat Q_R/r as finite-lambda R10",
    ],
    "04_vacuum_contract": [
        "d/dr [ W(r,L,fields) dR_AB/dr ] = J_R",
        "J_R = 0 in local vacuum",
    ],
    "05_reciprocity_attempt": [
        "S_R = integral dr [0.5 W(r) (R_AB')^2 + J_R R_AB]",
        "R_AB ~ Q_R/r",
    ],
    "06_source_neutrality": ["Q_R = -Pi_R", "gamma - 1 ~= q_R"],
    "07_nonpropagating_constraint": ["no R_AB kinetic term", "parent origin is still open"],
    "1035_green_kernel": [
        "KXD1035_0_parent_quadratic_operator",
        "alpha_X(lambda_X)=K_X^pt beta_s beta_t",
    ],
    "r10_reviewed_curve": ["REVIEWED_QA_CANDIDATE_NONCLAIM", "alpha_abs_bound"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1633_SOURCE_REGISTER.csv"
QUADRATIC_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1633_RAB_QUADRATIC_ROW_AUDIT.csv"
FINITE_RANGE_DECISION = OUT / "P8_Y5_PARENT_QLOC_1633_FINITE_RANGE_DECISION.csv"
R10_DEMOTION = OUT / "P8_Y5_PARENT_QLOC_1633_R10_DEMOTION_LEDGER.csv"
MASSLESS_ROUTE = OUT / "P8_Y5_PARENT_QLOC_1633_MASSLESS_TAIL_LOCAL_ROUTE.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1633_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1633_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1633_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    QUADRATIC_AUDIT,
    FINITE_RANGE_DECISION,
    R10_DEMOTION,
    MASSLESS_ROUTE,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    QUADRATIC_AUDIT,
    FINITE_RANGE_DECISION,
    R10_DEMOTION,
    MASSLESS_ROUTE,
    CLAIM_GATE,
    NEXT_TARGET,
]


def ensure_dirs() -> None:
    for path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def copy_outputs() -> None:
    paths = GENERATED + ([VALIDATION] if VALIDATION.exists() else [])
    for path in paths:
        for target_dir in [QUARANTINE, BRANCH_RESIDUALS]:
            shutil.copy2(path, target_dir / path.name)
    shutil.copy2(R10_DEMOTION, QUEUE / "JR1633_R10_DEMOTION_LEDGER_NONCLAIM.csv")
    shutil.copy2(MASSLESS_ROUTE, QUEUE / "JR1633_MASSLESS_TAIL_LOCAL_ROUTE_NONCLAIM.csv")
    shutil.copy2(NEXT_TARGET, QUEUE / "JR1633_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": key,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1633 parent-source audit input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def quadratic_audit_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "QUAD1633_0_variable",
            "object": "R_AB",
            "required_parent_form": "R_AB = ln(A B) = ln(T^2 S)",
            "status": "VARIABLE_IDENTIFIED",
            "source_basis": str(SOURCE_FILES["04_vacuum_contract"]),
            "implication": "reciprocity variable exists, but existence is not a finite-range R10 mode",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QUAD1633_1_derivative_mode",
            "object": "kinetic/source slot",
            "required_parent_form": "S_R = integral dr [0.5 W(r)(R_AB')^2 + J_R R_AB]",
            "status": "DERIVATIVE_ONLY_MODE_FOUND",
            "source_basis": str(SOURCE_FILES["05_reciprocity_attempt"]),
            "implication": "Euler equation gives d(W R_AB')/dr=J_R and source-free W R_AB'=Q_R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QUAD1633_2_finite_mass",
            "object": "M_R^2 or lambda_R",
            "required_parent_form": "S_R^(2) includes -0.5 Z_R lambda_R^-2 R_AB^2 or equivalent finite-range potential",
            "status": "MISSING_PARENT_FINITE_RANGE_OWNER",
            "source_basis": "not found in 04/05/06/07 R_AB parent notes; 1035 gives only generic conditional X-mode law",
            "implication": "no parent-signed Yukawa range for R_AB; finite-lambda R10 scoring remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QUAD1633_3_source_test_charges",
            "object": "beta_source_R and beta_test_R",
            "required_parent_form": "matter/readout action defines both source and test reciprocal charge legs",
            "status": "MISSING_SOURCE_TEST_CHARGE_NORMALIZATION",
            "source_basis": str(SOURCE_FILES["1035_green_kernel"]),
            "implication": "alpha_R(lambda) cannot be formed even if a range were later sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QUAD1633_4_boundary_charge",
            "object": "Q_R / Pi_R",
            "required_parent_form": "Q_R=-Pi_R plus parent-signed Pi_R=0 or bounded Pi_R",
            "status": "BOUNDARY_RELATION_EXISTS_ZERO_NOT_PROVED",
            "source_basis": str(SOURCE_FILES["06_source_neutrality"]),
            "implication": "nonzero massless reciprocal hair remains possible unless source neutrality is proved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QUAD1633_5_constraint_route",
            "object": "nonpropagating R_AB",
            "required_parent_form": "constraint route removes kinetic exterior R_AB mode",
            "status": "CLEAN_ZERO_ROUTE_PARENT_ORIGIN_OPEN",
            "source_basis": str(SOURCE_FILES["07_nonpropagating_constraint"]),
            "implication": "best GR-safe route is a parent-derived constraint/neutrality theorem, not an invented range",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def finite_range_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "FR1633_0_known_equation",
            "decision": "RAB_PARENT_NOTES_SUPPORT_MASSLESS_DERIVATIVE_EQUATION",
            "basis": "04 and 05 give d(W R_AB')/dr=J_R; 06 gives Q_R=-Pi_R",
            "effect": "massless reciprocal charge is the live local hazard",
            "next_action": "route Q_R/r to PPN/local residual analysis unless zero theorem closes it",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "FR1633_1_missing_range",
            "decision": "FINITE_RANGE_OWNER_NOT_FOUND_IN_CURRENT_PARENT_NOTES",
            "basis": "no R_AB-specific Z_R, M_R^2, lambda_R, or potential row is sourced in 04/05/06/07",
            "effect": "finite-lambda R10 branch cannot be scored",
            "next_action": "do not convert Q_R/r into alpha_R(lambda); keep R10 branch blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "FR1633_2_demote",
            "decision": "MASSLESS_TAIL_DEMOTED_FROM_R10_TO_PPN_LOCAL",
            "basis": "a 1/r reciprocal tail is not a Yukawa correction with a sourced lambda",
            "effect": "R10 remains a future finite-mode test only; local-GR recovery now hinges on Q_R=0 or tiny q_R",
            "next_action": "attempt zero-mode proof or explicit PPN envelope for Q_R/r",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def r10_demotion_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "R10DEM1633_0_bound_curve",
            "item": "external alpha_bound(lambda)",
            "status": "COMPARISON_BOUND_ASSET_PRESENT_NONCLAIM",
            "reason": "reviewed curve exists but has no parent-signed MTS alpha_R(lambda) row to compare",
            "effect": "asset retained for future finite-mode branch only",
            "next_action": "promote only after theory-side lambda_R/K_R/beta rows exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "R10DEM1633_1_massless_tail",
            "item": "Q_R/r reciprocal tail",
            "status": "NOT_R10_FINITE_LAMBDA_OBJECT",
            "reason": "R10 alpha(lambda) is a finite-range Yukawa-style comparison; Q_R/r has no sourced finite lambda_R",
            "effect": "tail cannot be scored against the R10 bound curve",
            "next_action": "test as PPN/local residual or prove Q_R=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "R10DEM1633_2_alpha_template",
            "item": "alpha_R(lambda)",
            "status": "BLOCKED_MISSING_ZR_LAMBDAR_BETAS_PROFILE_TAIL",
            "reason": "finite operator and source-test charge normalization are both absent",
            "effect": "no R10 pass/fail can be claimed",
            "next_action": "only reopen R10 if a parent finite reciprocal mode is actually derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def massless_route_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "TAIL1633_0_equation",
            "object": "massless reciprocal exterior",
            "derived_form": "J_R=0 -> W(r) R_AB'(r)=Q_R",
            "status": "DERIVED_FROM_CURRENT_RAB_ACTION",
            "risk": "Q_R is conserved hair unless a source/constraint theorem sets it to zero",
            "next_action": "derive Q_R=0 from parent matter descent or boundary neutrality",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TAIL1633_1_asymptotic",
            "object": "large-r profile",
            "derived_form": "for W~r^2, R_AB~Q_R/r plus constant fixed by R_AB(infinity)=0",
            "status": "LOCAL_PPN_PROFILE",
            "risk": "produces post-Newtonian residuals rather than R10 finite-range alpha(lambda)",
            "next_action": "map q_R to gamma-1 and local residual vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TAIL1633_2_ppn_gate",
            "object": "q_R amplitude",
            "derived_form": "06 notes gamma-1 ~= q_R and rough safety target |q_R| <= 1e-5",
            "status": "PPN_BOUND_TARGET_ONLY",
            "risk": "no parent amplitude law yet fixes q_R",
            "next_action": "derive amplitude law or demote local-GR recovery to explicit closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TAIL1633_3_constraint_escape",
            "object": "R_AB nonpropagating route",
            "derived_form": "constraint route can set R_AB=0 and remove Q_R, but parent origin remains open",
            "status": "PROMISING_ZERO_ROUTE_UNSIGNED",
            "risk": "cannot be used as proof until parent action supplies the constraint naturally",
            "next_action": "try parent matter-action descent / vertical generator signature for Q_R=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1633_0_R10_score",
            "claim": "R10 alpha(lambda) score",
            "status": "BLOCKED",
            "blocker": "no R_AB finite-range owner or alpha_R(lambda) prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1633_1_local_GR",
            "claim": "local GR/Newton recovery",
            "status": "BLOCKED",
            "blocker": "massless Q_R/r hair not proved zero or bounded below PPN residual targets",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1633_2_zero_theorem",
            "claim": "Q_R=0 source theorem",
            "status": "BLOCKED",
            "blocker": "Pi_R=0 / matter descent / nonpropagating parent origin not signed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1633_3_finite_mode",
            "claim": "finite reciprocal mode exists",
            "status": "BLOCKED",
            "blocker": "no parent R_AB quadratic mass/range row found",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1634-Y5-R2FR-massless-tail-PPN-envelope-or-zero-mode-proof.md",
            "script": "scripts/Y5_R2FR_massless_tail_PPN_envelope_or_zero_mode_proof.py",
            "objective": "derive Q_R=0 from parent matter descent, boundary neutrality, or nonpropagating constraint origin; if not, build the explicit PPN/local residual envelope for the Q_R/r tail",
            "success_condition": "either Q_R=0 is parent-signed, or the local branch carries an explicit q_R amplitude/bound ledger with no GR/Newton claim",
            "guardrails": "do not use R10 for the massless tail, do not invent q_R, do not claim local GR/Newton/PPN pass, keep all rows nonclaim until parent signed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def rab_parent_text() -> str:
    keys = [
        "04_vacuum_contract",
        "05_reciprocity_attempt",
        "06_source_neutrality",
        "07_nonpropagating_constraint",
    ]
    return "\n".join(read_text(SOURCE_FILES[key]) for key in keys)


def rab_finite_range_token_found() -> bool:
    text = rab_parent_text()
    forbidden_as_parent_range = [
        "Z_R lambda_R^-2 R_AB",
        "M_R^2 R_AB",
        "m_R^2 R_AB",
        "lambda_R^-2 R_AB^2",
        "finite-range R_AB",
    ]
    return any(token in text for token in forbidden_as_parent_range)


def all_claim_flags_false(paths: Iterable[Path]) -> bool:
    for path in paths:
        for row in csv_rows(path):
            for field in ["valid_for_claim", "claim_allowed", "score_allowed"]:
                if field in row and row[field] != "False":
                    return False
    return True


def validation_rows() -> list[dict[str, object]]:
    source_rows = source_register_rows()
    checks: list[tuple[str, bool, str]] = [
        (
            "VAL1633_0_sources_exist",
            all(row["path_exists"] for row in source_rows),
            "all cited 1633 source paths exist",
        ),
        (
            "VAL1633_1_needles_found",
            all(row["needles_found"] for row in source_rows),
            "all required 1633 source needles found",
        ),
        (
            "VAL1633_2_derivative_mode_found",
            any(row["status"] == "DERIVATIVE_ONLY_MODE_FOUND" for row in quadratic_audit_rows()),
            "R_AB derivative-only massless equation is staged",
        ),
        (
            "VAL1633_3_no_parent_range",
            not rab_finite_range_token_found(),
            "no R_AB-specific finite mass/range token found in 04/05/06/07 parent notes",
        ),
        (
            "VAL1633_4_demote_R10",
            any(row["decision"] == "MASSLESS_TAIL_DEMOTED_FROM_R10_TO_PPN_LOCAL" for row in finite_range_decision_rows()),
            "massless Q_R/r tail is demoted away from R10",
        ),
        (
            "VAL1633_5_R10_blocked",
            all(row["status"].startswith(("COMPARISON", "NOT_R10", "BLOCKED")) for row in r10_demotion_rows()),
            "R10 ledger remains nonclaim/blocked",
        ),
        (
            "VAL1633_6_massless_route",
            any(row["status"] == "LOCAL_PPN_PROFILE" for row in massless_route_rows()),
            "massless local/PPN route is explicitly staged",
        ),
        (
            "VAL1633_7_claim_gates_closed",
            all(row["status"] == "BLOCKED" for row in claim_gate_rows()),
            "all 1633 claim gates remain blocked",
        ),
        (
            "VAL1633_8_next_target_selected",
            next_target_rows()[0]["next_target"] == "1634-Y5-R2FR-massless-tail-PPN-envelope-or-zero-mode-proof.md",
            "next target selects Q_R zero proof or PPN envelope",
        ),
        (
            "VAL1633_9_csv_parse",
            all(len(csv_rows(path)) > 0 for path in GENERATED),
            "all generated 1633 CSVs parse",
        ),
        (
            "VAL1633_10_nonclaim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1633 generated decision rows remain nonclaim",
        ),
        (
            "VAL1633_11_branch_copies",
            all((QUARANTINE / path.name).exists() and (BRANCH_RESIDUALS / path.name).exists() for path in GENERATED),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1633_12_queue_copies",
            all(
                path.exists()
                for path in [
                    QUEUE / "JR1633_R10_DEMOTION_LEDGER_NONCLAIM.csv",
                    QUEUE / "JR1633_MASSLESS_TAIL_LOCAL_ROUTE_NONCLAIM.csv",
                    QUEUE / "JR1633_NEXT_TARGET_NONCLAIM.csv",
                ]
            ),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1633_13_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1633_14_formalization_untouched",
            not any(FORMALIZATION.rglob("*1633*")) if FORMALIZATION.exists() else True,
            "no 1633 outputs found under formalization-workbench",
        ),
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
            "check_id": "VAL1633_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1633 reciprocal quadratic/range row or massless-tail demotion validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    source_rows = csv_rows(SOURCE_REGISTER)
    quadratic_rows = csv_rows(QUADRATIC_AUDIT)
    finite_rows = csv_rows(FINITE_RANGE_DECISION)
    r10_rows = csv_rows(R10_DEMOTION)
    tail_rows = csv_rows(MASSLESS_ROUTE)
    gate_rows = csv_rows(CLAIM_GATE)
    next_rows = csv_rows(NEXT_TARGET)
    validation = csv_rows(VALIDATION)

    content = f"""# 1633 — R_AB Quadratic Range Row Or Massless Tail Demotion

**Private status:** nonclaim checkpoint. No R10, local-GR, Newton, PPN, WEP, clock, or orbital pass is claimed.

## Verdict

The current R_AB parent notes support a derivative-only reciprocal exterior, not a parent-signed finite-range R10 mode. The live equation is:

```text
J_R=0 -> W(r) R_AB'(r)=Q_R
```

With ordinary asymptotic weight this is a massless `Q_R/r` tail. That means it belongs in local/PPN recovery, not in a finite-lambda R10 alpha curve. The only clean way to recover local GR is therefore either to prove `Q_R=0` from the parent action, or to carry an explicit small-amplitude residual envelope.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Quadratic Row Audit

{markdown_table(quadratic_rows, ["row_id", "object", "required_parent_form", "status", "implication"])}

## Finite-Range Decision

{markdown_table(finite_rows, ["decision_id", "decision", "basis", "effect", "next_action"])}

## R10 Demotion Ledger

{markdown_table(r10_rows, ["row_id", "item", "status", "reason", "next_action"])}

## Massless Tail Local Route

{markdown_table(tail_rows, ["row_id", "object", "derived_form", "status", "risk", "next_action"])}

## Claim Gates

{markdown_table(gate_rows, ["gate_id", "claim", "status", "blocker"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        QUADRATIC_AUDIT: quadratic_audit_rows(),
        FINITE_RANGE_DECISION: finite_range_decision_rows(),
        R10_DEMOTION: r10_demotion_rows(),
        MASSLESS_ROUTE: massless_route_rows(),
        CLAIM_GATE: claim_gate_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    copy_outputs()
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
