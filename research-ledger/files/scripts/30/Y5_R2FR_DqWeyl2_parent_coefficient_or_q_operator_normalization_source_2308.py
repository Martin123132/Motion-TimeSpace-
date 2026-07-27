from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_DQWEYL2_COEFF_OR_Q_OPERATOR_SOURCE_2308"
DOC = ROOT / "2308-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md"

PATHS = {
    "2307_doc": ROOT / "2307-Y5-R2FR-DqWeyl2-projection-smoke-runner-input-contract-or-parent-coefficient-source.md",
    "2307_validation": OUT / "P8_Y5_BRR545_2307_VALIDATION.csv",
    "2307_hunt": OUT / "P8_Y5_PARENT_QLOC_2307_PARENT_COEFFICIENT_SOURCE_HUNT.csv",
    "2307_input": OUT / "P8_Y5_PARENT_QLOC_2307_SMOKE_RUNNER_INPUT_CONTRACT.csv",
    "2307_algebra": OUT / "P8_Y5_PARENT_QLOC_2307_PROJECTION_ALGEBRA.csv",
    "1025_doc": ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
    "1026_doc": ROOT / "1026-Y5-R10-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
    "1027_doc": ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
    "617_field_space": OUT / "P8_Y5_R10_617_FIELD_SPACE_NORMALIZATION_ATTEMPT.csv",
    "669_lx_candidates": OUT / "P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv",
    "669_residual": OUT / "P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv",
    "669_gates": OUT / "P8_Y5_R10_669_LX_OWNER_GATE_TESTS.csv",
    "2132_no_tower": OUT / "P8_Y5_PARENT_QLOC_2132_NO_TOWER_THEOREM_ATTEMPT.csv",
    "963_doc": ROOT / "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
    "1343_doc": ROOT / "1343-Y5-R10-RAB-R2FR-parent-coefficient-zero-signature-or-finite-scalar-map-fill.md",
}

SOURCES = [
    ("SRC2308_00_2307_doc", "2307_doc", PATHS["2307_doc"], ["DEC2307_3_next", "2308-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md"], "direct 2307 handoff"),
    ("SRC2308_01_2307_validation", "2307_validation", PATHS["2307_validation"], ["VAL2307_OVERALL", "PASS"], "2307 validation"),
    ("SRC2308_02_2307_hunt", "2307_hunt", PATHS["2307_hunt"], ["HUNT2307_0_DqWeyl2", "NOT_FOUND_CURRENT_CORPUS"], "D_qWeyl2 missing-source result"),
    ("SRC2308_03_2307_input", "2307_input", PATHS["2307_input"], ["IN2307_3_Zq", "MISSING_Q_OPERATOR"], "Z_q/q operator missing input"),
    ("SRC2308_04_2307_algebra", "2307_algebra", PATHS["2307_algebra"], ["ALG2307_3_massless_q_far", "16*D_qWeyl2"], "projection formula needing D/Z"),
    ("SRC2308_05_1025_doc", "1025_doc", PATHS["1025_doc"], ["SV1025_6_verdict", "FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED"], "scalar Hessian contract exists but is not owned"),
    ("SRC2308_06_1026_doc", "1026_doc", PATHS["1026_doc"], ["PM1026_6_verdict", "FAIL_CURRENT_CLAIM"], "parent metric lock failed"),
    ("SRC2308_07_1026_beta", "1026_doc", PATHS["1026_doc"], ["BE1026_4_verdict", "FAIL_CURRENT_CLAIM"], "beta/Hessian spectrum failed"),
    ("SRC2308_08_1027_doc", "1027_doc", PATHS["1027_doc"], ["QZ1027_6_verdict", "FAIL_CURRENT_CLAIM"], "source-zero theorem conditional only"),
    ("SRC2308_09_617_field_space", "617_field_space", PATHS["617_field_space"], ["FS617_5_finite_branch_ceiling", "promotion_blocked"], "field-space normalization blocked"),
    ("SRC2308_10_669_lx_candidates", "669_lx_candidates", PATHS["669_lx_candidates"], ["LX669_2_positive_sourcefree_massive", "conditional_sourcefree_operator_route"], "candidate L_X operator exists conditionally"),
    ("SRC2308_11_669_residual", "669_residual", PATHS["669_residual"], ["RV669_0_Z_X", "MISSING_PARENT_INPUT"], "Z_X missing residual vector"),
    ("SRC2308_12_669_gates", "669_gates", PATHS["669_gates"], ["G669_1_positive_kinetic", "blocked_as_expected"], "L_X owner gate blocked"),
    ("SRC2308_13_2132_no_tower", "2132_no_tower", PATHS["2132_no_tower"], ["NT2132_5_verdict", "NO_TOWER_THEOREM_NOT_DERIVED"], "no tower theorem not derived"),
    ("SRC2308_14_963_doc", "963_doc", PATHS["963_doc"], ["DO963_6_verdict", "NOT_PARENT_SIGNED_CURRENT_CORPUS"], "second-order parent signature not signed"),
    ("SRC2308_15_1343_doc", "1343_doc", PATHS["1343_doc"], ["ZERO1343_5_verdict", "ZERO_SIGNATURE_NOT_DERIVED_CURRENT_CORPUS"], "higher-curvature zero signature not derived"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2308_SOURCE_REGISTER.csv",
    "coefficient": OUT / "P8_Y5_PARENT_QLOC_2308_DQWEYL2_PARENT_COEFFICIENT_AUDIT.csv",
    "operator_bridge": OUT / "P8_Y5_PARENT_QLOC_2308_Q_OPERATOR_X_BRIDGE_AUDIT.csv",
    "normal_form": OUT / "P8_Y5_PARENT_QLOC_2308_Q_LOCAL_ACTION_NORMAL_FORM_CONTRACT.csv",
    "acceptance": OUT / "P8_Y5_PARENT_QLOC_2308_ACCEPTANCE_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2308_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2308_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2308_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2308_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2308_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2308_0_coeff_audit", OUTPUTS["coefficient"], QUEUE / "JR2308_DQWEYL2_PARENT_COEFFICIENT_AUDIT_NONCLAIM.csv"),
    ("COPY2308_1_operator_bridge", OUTPUTS["operator_bridge"], QUEUE / "JR2308_Q_OPERATOR_X_BRIDGE_AUDIT_NONCLAIM.csv"),
    ("COPY2308_2_normal_form", OUTPUTS["normal_form"], MICROSCOPE / "q_local_action_normal_form_contract_nonclaim_2308.csv"),
    ("COPY2308_3_acceptance", OUTPUTS["acceptance"], BETA_DOCS / "DQWEYL2_Q_OPERATOR_ACCEPTANCE_GATES_2308_NONCLAIM.csv"),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "missing_needles=" + ";".join(missing)
    return True, "all_needles_found"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def b(value: bool) -> str:
    return "true" if value else "false"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(clean(row.get(col, "")) for col in columns) + " |" for row in rows],
        ]
    )


def make_sources() -> list[dict[str, Any]]:
    rows = []
    for row_id, key, path, needles, role in SOURCES:
        ok, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needles": ";".join(needles),
                "needles_found": b(ok),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def make_coefficient_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DCO2308_0_definition",
            "target": "D_qWeyl2",
            "definition": "coefficient of q C_abcd C^abcd in the local parent/effective q equation or action after the q variable and normalization are fixed",
            "current_result": "DEFINED_AS_REQUIRED_INPUT_NOT_SOURCED",
            "source_status": "MISSING_PARENT_ACTION_TERM",
            "blocks": "cannot score 2307 projection kernel",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DCO2308_1_zero_route",
            "target": "D_qWeyl2=0",
            "definition": "follows if no bare Weyl2/qWeyl2 operator and no integrated higher-curvature tower are parent-signed",
            "current_result": "ZERO_ROUTE_NOT_DERIVED",
            "source_status": "2132/963/1343 all keep no-tower/higher-curvature signatures unsigned",
            "blocks": "must retain finite residual row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DCO2308_2_finite_route",
            "target": "finite D_qWeyl2",
            "definition": "requires source-backed sign, units, uncertainty, action normalization, and no-cancellation policy",
            "current_result": "NO_NUMERIC_SOURCE_FOUND",
            "source_status": "no file inspected supplies a coefficient value",
            "blocks": "projection smoke runner remains symbolic",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DCO2308_3_verdict",
            "target": "D_qWeyl2 coefficient source",
            "definition": "either theorem-zero or numeric coefficient",
            "current_result": "COEFFICIENT_UNSOURCED",
            "source_status": "nonclaim only",
            "blocks": "R10/PPN/orbital/clock/local-GR Weyl2 branch claim",
            "valid_for_claim": "false",
        },
    ]


def make_operator_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOP2308_0_bridge_target",
            "object": "q operator from existing X/L_X infrastructure",
            "statement": "Use L_X-style scalar operator for q only if q is proven identical to, or a signed projection of, the X/local residual variable.",
            "current_status": "BRIDGE_NOT_SIGNED",
            "evidence": "1025/1026/669 provide X operator scaffolding, not a q=X theorem for the D_qWeyl2 branch.",
            "missing_piece": "q-X identity/projection map with units and action normalization",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOP2308_1_positive_operator_contract",
            "object": "L_q=-div(Z_q grad)+M_q^2",
            "statement": "If q is a physical scalar mode with positive Hessian, the local operator has the same contract as X: Z_q>0, M_q^2>=0, boundary/domain signed.",
            "current_status": "EXACT_CONDITIONAL_CONTRACT",
            "evidence": "1025 derives the second-variation contract; 669 has positive-sourcefree/massive operator candidates.",
            "missing_piece": "parent Hessian signs, units, q field normalization, cross-block control",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOP2308_2_ZM_values",
            "object": "Z_q and M_q^2",
            "statement": "Z_q and M_q^2 cannot be copied from Z_X and M_X^2 until the bridge is signed; even Z_X/M_X^2 are currently missing.",
            "current_status": "MISSING_PARENT_INPUT",
            "evidence": "669 residual vector lists Z_X and M_X^2 as MISSING_PARENT_INPUT; 1026 metric/eigenvalue failed.",
            "missing_piece": "parent metric, Hessian spectrum, beta/range, or theorem-zero no-pole route",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOP2308_3_no_pole_route",
            "object": "q absent/first-class/no physical pole",
            "statement": "If q is quotient/constraint-only, no Green operator is needed; but first-class/vertical removal and boundary silence must be signed.",
            "current_status": "NOT_PARENT_SIGNED",
            "evidence": "669 ranks absent/constraint routes as best but not derived; 1027 source-zero remains conditional.",
            "missing_piece": "q map, vertical generator, first-class closure, boundary/source charge silence",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOP2308_4_verdict",
            "object": "q operator normalization",
            "statement": "Current corpus does not source Z_q, M_q^2, lambda_q, Green function, or a q=X bridge; operator route remains nonclaim.",
            "current_status": "Q_OPERATOR_UNSOURCED",
            "evidence": "2307, 1025, 1026, 617, and 669 agree the operator/range normalization is a contract, not a current theorem.",
            "missing_piece": "q-X bridge or independent q local action Hessian",
            "valid_for_claim": "false",
        },
    ]


def make_normal_form_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NF2308_0_minimal_action",
            "term": "minimal local q action contract",
            "formula": "S_q = int sqrt(g)[1/2 Z_q (nabla q)^2 + 1/2 M_q^2 q^2 + D_qWeyl2 q C_abcd C^abcd + D_qWeylDual q C_abcd *C^abcd] + boundary",
            "status": "CONTRACT_WRITTEN_NOT_DERIVED",
            "needed_to_promote": "parent action derivation, signs, units, boundary terms, q variable identity",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NF2308_1_variation",
            "term": "q Euler equation",
            "formula": "(-Z_q Box + M_q^2)q = -D_qWeyl2 C^2 - D_qWeylDual C*C - J_q - boundary_tail, up to sign convention",
            "status": "FORMAL_VARIATION_CONTRACT",
            "needed_to_promote": "signed parent convention and source/readout ownership",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NF2308_2_range",
            "term": "finite range",
            "formula": "lambda_q=sqrt(Z_q/M_q^2) if Z_q>0 and M_q^2>0",
            "status": "EXACT_CONDITIONAL_FORMULA",
            "needed_to_promote": "source-backed Z_q and M_q^2 in one normalization",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NF2308_3_no_pole",
            "term": "no-pole alternative",
            "formula": "if q is first-class/quotient absent, remove q and all D_qWeyl2 rows rather than fitting them",
            "status": "BETTER_GR_ROUTE_NOT_SIGNED",
            "needed_to_promote": "first-class closure and boundary/source silence",
            "valid_for_claim": "false",
        },
    ]


def make_acceptance_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "ACC2308_0_qX_bridge", "gate": "q-X identity/projection bridge signed", "passed": "false", "needed": "source path proving q variable in D_qWeyl2 branch is the same as X or has its own Hessian", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "ACC2308_1_D_coeff", "gate": "D_qWeyl2 theorem-zero or numeric coefficient sourced", "passed": "false", "needed": "parent action coefficient with units/sign or no-tower theorem", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "ACC2308_2_operator", "gate": "Z_q/M_q^2/lambda_q or no-pole route sourced", "passed": "false", "needed": "parent Hessian/operator normalization or first-class removal", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "ACC2308_3_source_zero", "gate": "J_q/source/readout tail zero or bounded", "passed": "false", "needed": "matter/coframe descent and hidden-source silence, or numeric bounds", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "ACC2308_4_projection_runner", "gate": "2307 smoke runner can become claim-grade", "passed": "false", "needed": "ACC2308_0 through ACC2308_3 plus P_arena", "valid_for_claim": "false"},
    ]


def make_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2308_0_copy_ZX", "claim": "use Z_X/M_X^2 as Z_q/M_q^2", "allowed": "false", "reason": "q-X bridge not signed and X values are themselves missing", "blocking_rows": "QOP2308_0_bridge_target;QOP2308_2_ZM_values", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2308_1_score_runner", "claim": "score 2307 projection as a physical bound", "allowed": "false", "reason": "D_qWeyl2, q operator, and observable coupling are unsourced", "blocking_rows": "DCO2308_3_verdict;QOP2308_4_verdict;ACC2308_4_projection_runner", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2308_2_local_GR", "claim": "local GR/Newton reduction derived", "allowed": "false", "reason": "operator/coefficient/source descent gates remain unsigned", "blocking_rows": "ACC2308_0_qX_bridge;ACC2308_1_D_coeff;ACC2308_2_operator;ACC2308_3_source_zero", "valid_for_claim": "false"},
    ]


def make_decision_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "DEC2308_0", "decision": "D_QWEYL2_COEFFICIENT_NOT_SOURCED", "reason": "no theorem-zero or numeric coefficient appears in current corpus", "next_action": "retain finite residual row", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2308_1", "decision": "Q_OPERATOR_CAN_NOT_BORROW_X_YET", "reason": "old X/L_X scaffolding is useful but q-X identity is not signed and X values are missing anyway", "next_action": "derive q-X bridge or independent q local action Hessian", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2308_2", "decision": "NORMAL_FORM_CONTRACT_WRITTEN", "reason": "minimum local q action and Euler equation now state the exact inputs needed for a real runner", "next_action": "use normal form as parent-action target, not as evidence", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2308_3_next", "decision": "NEXT_TARGET_SELECTED", "reason": "q-X bridge is the least wasteful next step; without it, coefficient/operator work duplicates old X audits", "next_action": "2309-Y5-R2FR-q-X-operator-identity-bridge-or-independent-q-Hessian.md", "valid_for_claim": "false"},
    ]


def make_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2308_0",
            "next_target": "2309-Y5-R2FR-q-X-operator-identity-bridge-or-independent-q-Hessian.md",
            "why": "before scoring D_qWeyl2 we must know whether q uses the existing X/L_X operator infrastructure or needs a separate Hessian",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        }
    ]


def copy_branch_files() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dst in BRANCH_COPY_SPECS:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": rel(src),
                "branch_copy_path": str(dst),
                "copy_exists": b(dst.exists()),
                "row_count": len(read_csv_rows(dst)),
                "valid_for_claim": "false",
            }
        )
    return rows


def validate(
    source_rows: list[dict[str, Any]],
    coefficient_rows: list[dict[str, Any]],
    operator_rows: list[dict[str, Any]],
    normal_form_rows: list[dict[str, Any]],
    acceptance_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tables = [source_rows, coefficient_rows, operator_rows, normal_form_rows, acceptance_rows, refusal_rows, decision_rows, copy_rows]
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2308_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited local source path exists"))
    checks.append(("VAL2308_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2308_02_coefficient_unsourced", any(row["row_id"] == "DCO2308_3_verdict" and row["current_result"] == "COEFFICIENT_UNSOURCED" for row in coefficient_rows), "D_qWeyl2 coefficient remains unsourced"))
    checks.append(("VAL2308_03_bridge_not_signed", any(row["row_id"] == "QOP2308_0_bridge_target" and row["current_status"] == "BRIDGE_NOT_SIGNED" for row in operator_rows), "q-X bridge is not signed"))
    checks.append(("VAL2308_04_operator_unsourced", any(row["row_id"] == "QOP2308_4_verdict" and row["current_status"] == "Q_OPERATOR_UNSOURCED" for row in operator_rows), "q operator remains unsourced"))
    checks.append(("VAL2308_05_normal_form", {"NF2308_0_minimal_action", "NF2308_1_variation", "NF2308_2_range"}.issubset({row["row_id"] for row in normal_form_rows}), "normal-form contract covers action, variation, and range"))
    checks.append(("VAL2308_06_acceptance_all_false", all(row["passed"] == "false" for row in acceptance_rows), "acceptance gates remain false"))
    checks.append(("VAL2308_07_refusal_runner", all(row["allowed"] == "false" for row in refusal_rows), "refusal runner blocks claims"))
    checks.append(("VAL2308_08_next_target", any(row["row_id"] == "DEC2308_3_next" and "2309-Y5-R2FR-q-X-operator-identity-bridge-or-independent-q-Hessian.md" in row["next_action"] for row in decision_rows), "next target selected"))
    checks.append(("VAL2308_09_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2308_10_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in tables for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2308_11_formalization_untouched_by_2308", len(list(FORMALIZATION.rglob("*2308*"))) == 0 if FORMALIZATION.exists() else True, "no 2308 output appears in formalization-workbench"))
    rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2308_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2308 confirms D_qWeyl2 and q-operator normalization are unsourced, refuses to copy X/L_X values without a q-X bridge, and writes the minimal q local action normal-form contract.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    coefficient_rows: list[dict[str, Any]],
    operator_rows: list[dict[str, Any]],
    normal_form_rows: list[dict[str, Any]],
    acceptance_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2308 — D_qWeyl2 Parent Coefficient Or q Operator Normalization Source",
        "",
        "## Summary",
        "",
        "2308 hunts the missing physics inputs behind the 2307 smoke contract. The result is strict: `D_qWeyl2` is still not sourced, and the `q` operator cannot safely borrow the old `X/L_X` infrastructure without a signed `q=X` or q-to-X projection bridge. Worse, even the old `X` operator values `Z_X`, `M_X^2`, `lambda_X`, and `K_X` are still nonclaim/missing.",
        "",
        "The useful progress is the exact local normal form. A future parent action must either remove `q` as a first-class/quotient variable, or own a local block with `Z_q`, `M_q^2`, `D_qWeyl2`, source terms, and boundary terms in one normalization. Until then, the 2307 runner stays symbolic.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## D_qWeyl2 Parent Coefficient Audit",
        "",
        md_table(coefficient_rows, ["row_id", "target", "definition", "current_result", "source_status", "blocks", "valid_for_claim"]),
        "",
        "## q Operator / X Bridge Audit",
        "",
        md_table(operator_rows, ["row_id", "object", "statement", "current_status", "evidence", "missing_piece", "valid_for_claim"]),
        "",
        "## q Local Action Normal Form Contract",
        "",
        md_table(normal_form_rows, ["row_id", "term", "formula", "status", "needed_to_promote", "valid_for_claim"]),
        "",
        "## Acceptance Gates",
        "",
        md_table(acceptance_rows, ["row_id", "gate", "passed", "needed", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        md_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decision_rows, ["row_id", "decision", "reason", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = make_sources()
    coefficient_rows = make_coefficient_rows()
    operator_rows = make_operator_bridge_rows()
    normal_form_rows = make_normal_form_rows()
    acceptance_rows = make_acceptance_rows()
    refusal_rows = make_refusal_rows()
    decision_rows = make_decision_rows()
    next_rows = make_next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["coefficient"], coefficient_rows)
    write_csv(OUTPUTS["operator_bridge"], operator_rows)
    write_csv(OUTPUTS["normal_form"], normal_form_rows)
    write_csv(OUTPUTS["acceptance"], acceptance_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["decision"], decision_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_files()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(source_rows, coefficient_rows, operator_rows, normal_form_rows, acceptance_rows, refusal_rows, decision_rows, copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_markdown(source_rows, coefficient_rows, operator_rows, normal_form_rows, acceptance_rows, refusal_rows, decision_rows, next_rows, copy_rows, validation_rows)

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2308_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
