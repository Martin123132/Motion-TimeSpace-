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
QUARANTINE = MICROSCOPE / "quarantine" / "1634"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1634-Y5-R2FR-massless-tail-PPN-envelope-or-zero-mode-proof.md"

SOURCE_FILES = {
    "1633_doc": ROOT / "1633-Y5-R2FR-RAB-quadratic-range-and-charge-row-or-massless-tail-demotion.md",
    "1633_validation": OUT / "P8_Y5_BRR545_1633_VALIDATION.csv",
    "1633_next": OUT / "P8_Y5_PARENT_QLOC_1633_NEXT_TARGET.csv",
    "04_vacuum_contract": ROOT / "04-vacuum-reciprocity-action-contract.md",
    "05_reciprocity_attempt": ROOT / "05-reciprocity-theorem-attempt.md",
    "06_source_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "07_nonpropagating_constraint": ROOT / "07-nonpropagating-reciprocity-constraint.md",
}

NEEDLES = {
    "1633_doc": [
        "MASSLESS_TAIL_DEMOTED_FROM_R10_TO_PPN_LOCAL",
        "J_R=0 -> W(r) R_AB'(r)=Q_R",
    ],
    "1633_validation": ["VAL1633_OVERALL", "PASS"],
    "1633_next": [
        "1634-Y5-R2FR-massless-tail-PPN-envelope-or-zero-mode-proof.md",
        "do not use R10 for the massless tail",
    ],
    "04_vacuum_contract": ["R_AB(infinity) = 0", "dR_AB/dr = 0"],
    "05_reciprocity_attempt": ["Asymptotic flatness alone does not kill `Q_R`", "R_AB ~ Q_R/r"],
    "06_source_neutrality": ["Q_R = -Pi_R", "gamma - 1 ~= q_R", "|q_R| <= 1e-5"],
    "07_nonpropagating_constraint": ["no conserved Q_R", "This is not yet a full parent derivation"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1634_SOURCE_REGISTER.csv"
ZERO_PROOF = OUT / "P8_Y5_PARENT_QLOC_1634_ZERO_PROOF_CLAUSE_AUDIT.csv"
PPN_ENVELOPE = OUT / "P8_Y5_PARENT_QLOC_1634_PPN_ENVELOPE_TEMPLATE.csv"
LOCAL_RESIDUAL = OUT / "P8_Y5_PARENT_QLOC_1634_LOCAL_RESIDUAL_VECTOR.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1634_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1634_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1634_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1634_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    ZERO_PROOF,
    PPN_ENVELOPE,
    LOCAL_RESIDUAL,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    ZERO_PROOF,
    PPN_ENVELOPE,
    LOCAL_RESIDUAL,
    DECISION,
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
    shutil.copy2(ZERO_PROOF, QUEUE / "JR1634_ZERO_PROOF_CLAUSE_AUDIT_NONCLAIM.csv")
    shutil.copy2(PPN_ENVELOPE, QUEUE / "JR1634_PPN_ENVELOPE_TEMPLATE_NONCLAIM.csv")
    shutil.copy2(NEXT_TARGET, QUEUE / "JR1634_NEXT_TARGET_NONCLAIM.csv")


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
                "role": "1634 zero-proof/PPN-envelope input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def zero_proof_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ZERO1634_0_exterior_equation",
            "proof_clause": "source-free exterior equation",
            "required_statement": "J_R=0 -> W R_AB'=Q_R",
            "status": "DERIVED_BUT_LEAVES_INTEGRATION_CHARGE",
            "why_not_closed": "the equation identifies the hair; it does not set Q_R=0",
            "next_action": "use source/boundary/constraint input to kill or bound Q_R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ZERO1634_1_asymptotic_boundary",
            "proof_clause": "asymptotic flatness",
            "required_statement": "R_AB(infinity)=0",
            "status": "KILLS_CONSTANT_NOT_CHARGE",
            "why_not_closed": "R_AB~Q_R/r still satisfies the infinity condition",
            "next_action": "do not treat asymptotic flatness as a Q_R zero theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ZERO1634_2_boundary_momentum",
            "proof_clause": "surface momentum neutrality",
            "required_statement": "Q_R=-Pi_R and Pi_R=0",
            "status": "RELATION_EXISTS_ZERO_UNSIGNED",
            "why_not_closed": "Q_R=-Pi_R is staged, but Pi_R=0 is not parent-signed for real matter",
            "next_action": "derive Pi_R=0 from matter action descent or source neutrality",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ZERO1634_3_matter_descent",
            "proof_clause": "matter does not see representative R_AB",
            "required_statement": "S_matter descends through quotient variables, giving no independent R_AB source leg",
            "status": "MOST_PROMISING_BUT_UNSIGNED",
            "why_not_closed": "current notes do not yet give a parent-level matter-coupling theorem",
            "next_action": "audit parent matter action/coupling map for vertical R_AB invariance",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ZERO1634_4_nonpropagating_constraint",
            "proof_clause": "R_AB is constrained, not propagated",
            "required_statement": "no kinetic exterior R_AB mode -> no conserved Q_R",
            "status": "CLEAN_ESCAPE_PARENT_ORIGIN_OPEN",
            "why_not_closed": "constraint route is algebraically clean, but its parent origin is not derived",
            "next_action": "derive the constraint from parent symmetry or demote to closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def ppn_envelope_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PPNENV1634_0_parameterization",
            "quantity": "q_R",
            "symbolic_definition": "R_AB(r)=q_R L_N(r)+O(L_N^2), with L_N the local Newtonian load/potential variable",
            "units": "dimensionless",
            "status": "SYMBOLIC_ENVELOPE_ONLY",
            "source_basis": "06 reciprocal charge source neutrality",
            "missing_input": "parent amplitude law for q_R in terms of matter/source variables",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PPNENV1634_1_gamma",
            "quantity": "Delta gamma",
            "symbolic_definition": "gamma-1 ~= q_R",
            "units": "dimensionless",
            "status": "PPN_TARGET_STAGED",
            "source_basis": "06 notes",
            "missing_input": "q_R value or zero theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PPNENV1634_2_safety_target",
            "quantity": "local PPN safety target",
            "symbolic_definition": "|q_R| <= 1e-5 as current internal rough gate",
            "units": "dimensionless",
            "status": "INTERNAL_TARGET_NOT_PUBLIC_CLAIM",
            "source_basis": "06 notes",
            "missing_input": "formal external PPN-source table and parent q_R amplitude",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PPNENV1634_3_zero_limit",
            "quantity": "GR recovery in R_AB sector",
            "symbolic_definition": "Q_R=0 -> q_R=0 -> R_AB=0 under R_AB(infinity)=0",
            "units": "dimensionless",
            "status": "CONDITIONAL_GR_LIMIT",
            "source_basis": "04/05/06",
            "missing_input": "parent proof of Q_R=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def local_residual_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RES1634_0_gamma",
            "observable_sector": "PPN light/time-delay geometry",
            "residual_form": "Delta gamma ~= q_R",
            "status": "SYMBOLIC_BOUND_REQUIRED",
            "missing_input": "q_R amplitude or zero theorem",
            "decision_effect": "local GR cannot be claimed until this closes",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RES1634_1_AB_product",
            "observable_sector": "weak-field metric reciprocity",
            "residual_form": "R_AB=ln(A B)=q_R L_N+O(L_N^2)",
            "status": "SYMBOLIC_PROFILE_REQUIRED",
            "missing_input": "mapping of A/B split and higher-order terms",
            "decision_effect": "only AB product is controlled here; full metric residual still needs split rules",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RES1634_2_source_boundary",
            "observable_sector": "compact/local source matching",
            "residual_form": "Q_R=-Pi_R",
            "status": "SOURCE_MATCH_REQUIRED",
            "missing_input": "Pi_R for matter source and boundary variation class",
            "decision_effect": "source theorem, not R10, is the next decisive local-GR task",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1634_0_zero_proof",
            "decision": "ZERO_PROOF_NOT_CLOSED",
            "reason": "asymptotic flatness and exterior equation leave Q_R; Pi_R=0/matter descent/constraint origin remains unsigned",
            "next_action": "target parent matter descent or explicit closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1634_1_ppn_envelope",
            "decision": "PPN_ENVELOPE_STAGED_NONCLAIM",
            "reason": "q_R maps to gamma-1 in the existing notes, but no parent amplitude law exists",
            "next_action": "derive q_R=0, or build explicit local residual bounds with no GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1634_2_next",
            "decision": "NEXT_1635_PARENT_MATTER_DESCENT_SIGNATURE_FOR_PIR_ZERO",
            "reason": "Pi_R=0 is the shortest route from reciprocal hair to local GR recovery",
            "next_action": "audit matter action/coupling map for vertical R_AB invariance and source momentum silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1634_0_QR_zero",
            "claim": "Q_R=0 theorem",
            "status": "BLOCKED",
            "blocker": "Pi_R=0 / matter descent / constraint origin not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1634_1_local_GR",
            "claim": "local GR/Newton recovery",
            "status": "BLOCKED",
            "blocker": "q_R amplitude not derived or bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1634_2_PPN",
            "claim": "PPN pass",
            "status": "BLOCKED",
            "blocker": "only symbolic Delta gamma ~= q_R envelope exists",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1634_3_R10",
            "claim": "R10 branch",
            "status": "BLOCKED",
            "blocker": "massless Q_R/r tail remains routed away from R10",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1635-Y5-R2FR-parent-matter-descent-signature-for-PiR-zero.md",
            "script": "scripts/Y5_R2FR_parent_matter_descent_signature_for_PiR_zero.py",
            "objective": "audit whether the parent matter/coupling action is invariant along the vertical R_AB representative direction, forcing Pi_R=0 and hence Q_R=0",
            "success_condition": "either Pi_R=0 is parent-signed by descent/vertical invariance, or the local branch is explicitly marked closure-only with q_R residual envelope",
            "guardrails": "do not infer Pi_R=0 from desire for GR, do not use asymptotic flatness as a zero theorem, do not claim local GR until q_R closes",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


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
            "VAL1634_0_sources_exist",
            all(row["path_exists"] for row in source_rows),
            "all cited 1634 source paths exist",
        ),
        (
            "VAL1634_1_needles_found",
            all(row["needles_found"] for row in source_rows),
            "all required 1634 source needles found",
        ),
        (
            "VAL1634_2_zero_clause_coverage",
            {row["clause_id"] for row in zero_proof_rows()}
            == {
                "ZERO1634_0_exterior_equation",
                "ZERO1634_1_asymptotic_boundary",
                "ZERO1634_2_boundary_momentum",
                "ZERO1634_3_matter_descent",
                "ZERO1634_4_nonpropagating_constraint",
            },
            "zero proof audits exterior, boundary, matter descent, and constraint routes",
        ),
        (
            "VAL1634_3_zero_not_closed",
            any(row["decision"] == "ZERO_PROOF_NOT_CLOSED" for row in decision_rows()),
            "zero proof remains explicitly unclosed",
        ),
        (
            "VAL1634_4_ppn_envelope",
            any("gamma-1 ~= q_R" in row["symbolic_definition"] for row in ppn_envelope_rows()),
            "PPN q_R envelope is staged",
        ),
        (
            "VAL1634_5_local_residual_vector",
            any(row["residual_id"] == "RES1634_0_gamma" for row in local_residual_rows()),
            "local residual vector includes Delta gamma",
        ),
        (
            "VAL1634_6_claim_gates_closed",
            all(row["status"] == "BLOCKED" for row in claim_gate_rows()),
            "all 1634 claim gates remain blocked",
        ),
        (
            "VAL1634_7_next_target_selected",
            next_target_rows()[0]["next_target"] == "1635-Y5-R2FR-parent-matter-descent-signature-for-PiR-zero.md",
            "next target selects parent matter descent signature",
        ),
        (
            "VAL1634_8_csv_parse",
            all(len(csv_rows(path)) > 0 for path in GENERATED),
            "all generated 1634 CSVs parse",
        ),
        (
            "VAL1634_9_nonclaim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1634 generated decision rows remain nonclaim",
        ),
        (
            "VAL1634_10_branch_copies",
            all((QUARANTINE / path.name).exists() and (BRANCH_RESIDUALS / path.name).exists() for path in GENERATED),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1634_11_queue_copies",
            all(
                path.exists()
                for path in [
                    QUEUE / "JR1634_ZERO_PROOF_CLAUSE_AUDIT_NONCLAIM.csv",
                    QUEUE / "JR1634_PPN_ENVELOPE_TEMPLATE_NONCLAIM.csv",
                    QUEUE / "JR1634_NEXT_TARGET_NONCLAIM.csv",
                ]
            ),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1634_12_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1634_13_formalization_untouched",
            not any(FORMALIZATION.rglob("*1634*")) if FORMALIZATION.exists() else True,
            "no 1634 outputs found under formalization-workbench",
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
            "check_id": "VAL1634_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1634 massless tail PPN envelope or zero-mode proof validation",
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
    zero_rows = csv_rows(ZERO_PROOF)
    ppn_rows = csv_rows(PPN_ENVELOPE)
    residual_rows = csv_rows(LOCAL_RESIDUAL)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_rows = csv_rows(NEXT_TARGET)
    validation = csv_rows(VALIDATION)

    content = f"""# 1634 — Massless Tail PPN Envelope Or Zero-Mode Proof

**Private status:** nonclaim checkpoint. This does not claim local GR, Newton, PPN, R10, WEP, clock, or orbital success.

## Verdict

The proof-first route did not close yet. The current corpus gives the exterior massless equation and the boundary relation, but it does not yet parent-sign `Pi_R=0`, matter descent, or the nonpropagating constraint origin. The honest local branch is therefore:

```text
Q_R=0 -> GR-safe R_AB sector
Q_R!=0 -> R_AB~Q_R/r -> q_R PPN residual envelope
```

So the next target is narrow and important: prove the matter action is silent along the vertical `R_AB` representative direction, or mark this as closure-only.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Zero-Proof Clause Audit

{markdown_table(zero_rows, ["clause_id", "proof_clause", "required_statement", "status", "why_not_closed", "next_action"])}

## PPN Envelope Template

{markdown_table(ppn_rows, ["row_id", "quantity", "symbolic_definition", "status", "missing_input"])}

## Local Residual Vector

{markdown_table(residual_rows, ["residual_id", "observable_sector", "residual_form", "status", "missing_input", "decision_effect"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "claim", "status", "blocker"])}

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
        ZERO_PROOF: zero_proof_rows(),
        PPN_ENVELOPE: ppn_envelope_rows(),
        LOCAL_RESIDUAL: local_residual_rows(),
        DECISION: decision_rows(),
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
