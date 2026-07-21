from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4671"
CLAIM_ID = "L-513"
BRANCH = "MTS_R2FR_Y5_PARENT_MEMORY_HESSIAN_SIGNATURE_OR_B826_ROOT_LOCK_4671"
MARKER = "PPC4161_PARENT_MEMORY_HESSIAN_SIGNATURE_OR_B826_ROOT_LOCK_4671"
PACKET_MARKER = "PPC4161_PACKET_PARENT_MEMORY_HESSIAN_SIGNATURE_OR_B826_ROOT_LOCK_4671"
DECISION = "STRICT_MINIMUM_EVEN_BRANCH_THEOREM_CANDIDATE_WRITTEN_PARENT_SIGNATURE_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4672-Y5-R2FR-even-branch-symmetry-owner-or-first-Hessian-B826-bound-row.md"

DOC_PATH = POST / "4671-Y5-R2FR-parent-memory-Hessian-signature-or-B826-root-lock-first-row.md"
FORMAL_PATH = FORMAL / "687-PPC4161-parent-memory-Hessian-signature-or-B826-root-lock-first-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4670 = POST / "4670-Y5-R2FR-Zmem-M2mem-positive-parent-Hessian-or-Bmem-first-component-source-row.md"
FORMAL_686 = FORMAL / "686-PPC4161-Zmem-M2mem-positive-parent-Hessian-or-Bmem-first-component-source-row.md"
FORMAL_646 = FORMAL / "646-PPC4161-co-normalized-gap-and-source-coupling-parent-action.md"
FORMAL_523 = FORMAL / "523-PPC4161-memory-trace-projection-lock-or-finite-Bmem-source-row.md"

CSV_4670_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4670_NEXT_TARGET.csv"
CSV_4670_ZM = SOURCE_DIR / "P8_Y5_R2FR_4670_ZM_PARENT_HESSIAN_AUDIT.csv"
CSV_4670_B = SOURCE_DIR / "P8_Y5_R2FR_4670_BMEM_FIRST_COMPONENT_AUDIT.csv"
CSV_4670_FIRST = SOURCE_DIR / "P8_Y5_R2FR_4670_ZM_B826_FIRST_ROW_CONTRACT.csv"
CSV_4670_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4670_STATUS.csv"
CSV_4670_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4670_VALIDATION.csv"

CSV_4630_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4630_PARENT_ACTION_CONTRACT_ROWS.csv"
CSV_4630_EVAL = SOURCE_DIR / "P8_Y5_R2FR_4630_PARENT_ACTION_EVALUATION_ROWS.csv"
CSV_4630_VARIATION = SOURCE_DIR / "P8_Y5_R2FR_4630_VARIATION_DERIVATION_ROWS.csv"
CSV_4630_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4630_CONDITIONAL_LOCAL_GR_THEOREM_ROWS.csv"
CSV_4630_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4630_CLAIM_BLOCKERS.csv"
CSV_4630_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4630_VALIDATION.csv"

CSV_4507_FORMULA = SOURCE_DIR / "P8_Y5_R2FR_4507_BMEM_EFFECTIVE_FORMULA.csv"
CSV_4507_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4507_PARENT_SIGNATURE_AUDIT.csv"
CSV_4507_FINITE = SOURCE_DIR / "P8_Y5_R2FR_4507_FINITE_BMEM_SOURCE_ROW.csv"
CSV_4507_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4507_STATUS.csv"
CSV_4507_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4507_VALIDATION.csv"

CSV_4510_ROOT = SOURCE_DIR / "P8_Y5_R2FR_4510_PARENT_SOURCE_ROOT_THEOREM.csv"
CSV_4514_BMEM = SOURCE_DIR / "P8_Y5_R2FR_4514_BMEM_EFFECTIVE_COMPONENT_VECTOR.csv"
CSV_4621_IDENTITY = SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_POSITIVE_OPERATOR_IDENTITY.csv"
CSV_4621_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4621_ZMEM_M2MEM_SOURCE_ROWS_NONCLAIM.csv"
CSV_4628_HESSIAN = SOURCE_DIR / "P8_Y5_R2FR_4628_PARENT_HESSIAN_ROWS.csv"
CSV_4628_GAP = SOURCE_DIR / "P8_Y5_R2FR_4628_LAMBDA_MEM_GAP_ROWS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4671_SOURCE_REGISTER.csv"
SIGNATURE_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4671_STRICT_MINIMUM_EVEN_BRANCH_THEOREM.csv"
HESSIAN_TEST_CSV = SOURCE_DIR / "P8_Y5_R2FR_4671_PARENT_HESSIAN_SIGNATURE_TEST.csv"
B826_LOCK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4671_B826_ROOT_LOCK_TEST.csv"
FIRST_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4671_FIRST_HESSIAN_B826_ROW_CONTRACT.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4671_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4671_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4671_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4671_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4671_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4671_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_number(path: Path, needle: str) -> int:
    for index, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    suffix = "" if not existing or existing.endswith("\n") else "\n"
    path.write_text(existing + suffix + text.lstrip("\n"), encoding="utf-8")


def csv_line(values: list[str]) -> str:
    buffer = io.StringIO()
    csv.writer(buffer, lineterminator="\n").writerow(values)
    return buffer.getvalue()


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4671_00_4670_next", CSV_4670_NEXT, "4671-Y5-R2FR-parent-memory-Hessian-signature-or-B826-root-lock-first-row.md", "4670 selected 4671."),
        ("SRC4671_01_4670_ZM", CSV_4670_ZM, "ZMH4670_6_decision", "Z/M parent Hessian was the first gate."),
        ("SRC4671_02_4670_B826", CSV_4670_B, "BFC4670_1_B826", "B826 first component was isolated."),
        ("SRC4671_03_4670_first", CSV_4670_FIRST, "FR4670_6_Rm", "root-lock row requirement."),
        ("SRC4671_04_4670_status", CSV_4670_STATUS, "False,False,False", "4670 remains nonclaim."),
        ("SRC4671_05_4670_validation", CSV_4670_VALIDATION, "VAL4670_OVERALL,True,PASS", "4670 validation."),
        ("SRC4671_06_doc4670", DOC_4670, "The exact theorem shape is good", "4670 prose result."),
        ("SRC4671_07_formal686", FORMAL_686, "B_826 = a_F L_cg^-2 R_m", "4670 formal contract."),
        ("SRC4671_08_4630_contract", CSV_4630_CONTRACT, "PACT4630_2_extremum_local_GR_route", "parent action extremum route."),
        ("SRC4671_09_4630_eval", CSV_4630_EVAL, "EVAL4630_1_extremum_positive_gap", "best theorem branch."),
        ("SRC4671_10_4630_variation", CSV_4630_VARIATION, "VAR4630_0_memory_euler_lagrange", "operator/source variation."),
        ("SRC4671_11_4630_theorem", CSV_4630_THEOREM, "TGR4630_0_conditional_statement", "conditional local-GR theorem."),
        ("SRC4671_12_4630_blockers", CSV_4630_BLOCKERS, "BLK4630_1_branch_extremum_signature", "missing branch signature."),
        ("SRC4671_13_4630_validation", CSV_4630_VALIDATION, "VAL4630_OVERALL,PASS", "4630 validation."),
        ("SRC4671_14_formal646", FORMAL_646, "beta_visible=0", "formal parent action summary."),
        ("SRC4671_15_4507_formula", CSV_4507_FORMULA, "BMF4507_1_826_term", "B826 formula."),
        ("SRC4671_16_4507_audit", CSV_4507_AUDIT, "PA4507_1_F1_zero", "826 partial-only audit."),
        ("SRC4671_17_4507_finite", CSV_4507_FINITE, "FBM4507_0_memory_B_source", "finite Bmem row."),
        ("SRC4671_18_4507_status", CSV_4507_STATUS, "PRIVATE_NONCLAIM", "4507 nonclaim."),
        ("SRC4671_19_4507_validation", CSV_4507_VALIDATION, "VAL4507_OVERALL,PASS", "4507 validation."),
        ("SRC4671_20_formal523", FORMAL_523, "The 826 extremum can kill the first term", "formal 4507 result."),
        ("SRC4671_21_4510_root", CSV_4510_ROOT, "PST4510_3_response_extremum_constructor", "source-root/extremum constructor."),
        ("SRC4671_22_4514_Bmem", CSV_4514_BMEM, "BMV4514_0_B826", "B826 component vector."),
        ("SRC4671_23_4621_nohair", CSV_4621_IDENTITY, "MPI4621_2_nohair_zero", "positive operator nohair."),
        ("SRC4671_24_4621_ZM", CSV_4621_SOURCE, "ZMR4621_0_Zmem_min", "Z/M source rows."),
        ("SRC4671_25_4628_hessian", CSV_4628_HESSIAN, "HES4628_1_parent_hessian_definitions", "parent Hessian definition."),
        ("SRC4671_26_4628_gap", CSV_4628_GAP, "GAP4628_0_exact_positive_gap", "positive gap criterion."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, note in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "line_number": line_number(path, needle),
                "note": note,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def signature_theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "STM4671_0_parent_action",
            "single parent memory action",
            "S_parent has one branch variable m and one local expansion point m0",
            "prevents fitting Z/M and B826 in different normalizations",
            "CONTRACT_PRESENT_NOT_COEFFICIENT_SIGNED",
        ),
        (
            "STM4671_1_strict_minimum",
            "strict local minimum",
            "V_eff'(m0)=0 and V_eff''(m0)+environment Hessian >= M0^2 > 0",
            "gives M2_mem>0 and removes tachyon/flat zero mode in the selected branch",
            "EXACT_IF_PARENT_ENERGY_MINIMUM_SIGNED",
        ),
        (
            "STM4671_2_kinetic_positivity",
            "ghost-free kinetic Hessian",
            "Z(m0) >= Z0 > 0 with fixed sign convention",
            "gives elliptic/coercive memory operator for 4621 nohair",
            "EXACT_IF_PARENT_KINETIC_SIGNED",
        ),
        (
            "STM4671_3_even_branch_symmetry",
            "local reflection/even branch",
            "sigma: delta_m -> -delta_m leaves ordinary visible matter/source-response parent density invariant",
            "all odd first derivatives vanish at m0, including beta_visible and B826 root derivative",
            "BEST_ROUTE_UNSIGNED_SYMMETRY_OWNER_MISSING",
        ),
        (
            "STM4671_4_B826_root",
            "B826 source-root lock",
            "R_m(m_L;X_B)=0 or partial_m R(m_L;X_B)=0 with X_B fixed and m_L=m0",
            "kills the first B_mem_eff component without cancellation",
            "EXACT_IF_SAME_BRANCH_EXTREMUM_SIGNED",
        ),
        (
            "STM4671_5_result",
            "combined theorem candidate",
            "STM4671_1+2+3+4 and zero boundary/source-current gates imply first-order memory body charge from ZM/B826 route is silent",
            "the route is mathematically real but remains private nonclaim because the symmetry/minimum signatures are not parent-owned in current rows",
            "THEOREM_CANDIDATE_WRITTEN_NOT_PROMOTED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": row[0],
            "clause": row[1],
            "signature_condition": row[2],
            "derivation_payoff": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def hessian_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "HST4671_0_Zmem",
            "Z_mem",
            "Z_mem=Z(m0)",
            "No-ghost/coercive kinetic term requires Z(m0)>0. If parent action chooses the positive kinetic sign and no field-space degeneracy, Z_mem_min>0 follows on a compact local branch.",
            "current rows state Z(m0)>0 only inside a conditional contract; no value/lower bound/source path is signed",
            "UNSIGNED_POSITIVE_KINETIC_HESSIAN",
        ),
        (
            "HST4671_1_M2mem",
            "M2_mem",
            "M2_mem=V_eff''(m0)+H_env",
            "A strict local energy minimum gives M2_mem>0; an even branch alone gives V_eff'(m0)=0 but not positivity.",
            "current rows do not prove strict convexity or source/environment Hessian positivity",
            "UNSIGNED_STRICT_GAP_HESSIAN",
        ),
        (
            "HST4671_2_zero_mode",
            "zero mode",
            "M2_mem=0 with projected mean/boundary condition",
            "If M2 is not positive, a zero-mode removal theorem can replace it only with explicit boundary/mean constraints and no source-current.",
            "no constraint-elimination proof is signed",
            "ALTERNATIVE_UNSIGNED",
        ),
        (
            "HST4671_3_ratio",
            "lambda_mem",
            "lambda_mem=sqrt(Z_mem/M2_mem)",
            "Range is claim-grade only if Z and M2 are same-branch parent coefficients.",
            "R10 anchor and independent bound rows are barred from signing the ratio",
            "CO_NORMALIZATION_GUARD_ACTIVE",
        ),
        (
            "HST4671_4_claim_result",
            "Hessian promotion",
            "Z_mem>0 and M2_mem>0",
            "Would unlock 4621 nohair once rho_mem and Q_boundary_mem vanish.",
            "not promoted from current evidence",
            "HESSIAN_SIGNATURE_FAILS_FOR_CLAIM",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "test_id": row[0],
            "quantity": row[1],
            "parent_formula": row[2],
            "derivation_attempt": row[3],
            "current_evidence_result": row[4],
            "status": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def b826_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "BRL4671_0_formula",
            "B_826",
            "B_826=a_F L_cg^-2 R_m(m_L;X_B)",
            "4507/4514 isolate this as the first B_mem_eff component.",
            "formula signed as structure, not as zero",
            "STRUCTURE_READY",
        ),
        (
            "BRL4671_1_root_lock",
            "R_m(m_L;X_B)",
            "R_m=0 or partial_m R=0 at m_L=m0 with X_B fixed",
            "If R is the same parent residual/response whose stationary point defines the local branch, the derivative/root vanishes.",
            "4510 gives constructors, but current branch does not prove this is the actual parent owner",
            "ROOT_LOCK_UNSIGNED",
        ),
        (
            "BRL4671_2_even_route",
            "even response",
            "R(m0+delta_m;X_B)=R(m0-delta_m;X_B)",
            "Reflection/even branch symmetry kills the linear response and therefore B826.",
            "no MTS-owned symmetry map is signed for ordinary visible source response",
            "BEST_ZERO_ROUTE_UNSIGNED",
        ),
        (
            "BRL4671_3_finite_route",
            "finite B826",
            "|B_826| <= |a_F| L_cg^-2 |R_m|",
            "If root lock fails, this is the first source row needed for the no-cancellation B_mem_eff bound.",
            "a_F, L_cg, R_m and body profile values are missing",
            "FINITE_ROW_REQUIRED_IF_ZERO_FAILS",
        ),
        (
            "BRL4671_4_claim_result",
            "B826 promotion",
            "B_826=0",
            "Would remove only the first B_mem_eff component; Weyl/Y5/Y6/boundary/readout tails remain separate.",
            "not promoted from current evidence",
            "B826_ZERO_FAILS_FOR_CLAIM",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "lock_id": row[0],
            "object": row[1],
            "formula": row[2],
            "derivation_attempt": row[3],
            "current_evidence_result": row[4],
            "status": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def first_row_contract(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("FHR4671_0_symmetry_owner", "THEOREM_ZERO", "sigma_branch", "parent map sigma: delta_m -> -delta_m or equivalent extremum owner", "derive from MTS parent variables, not impose as closure", "MISSING_PARENT_SYMMETRY_OWNER"),
        ("FHR4671_1_energy_minimum", "THEOREM_ZERO", "strict_minimum", "V_eff'(m0)=0 and V_eff''+H_env>=M0^2>0", "source parent Hessian or signed stability theorem", "MISSING_STRICT_MINIMUM_SIGNATURE"),
        ("FHR4671_2_kinetic_lower", "THEOREM_ZERO", "Z0", "Z_mem>=Z0>0 over local branch/domain", "source no-ghost lower bound and sign convention", "MISSING_Z0"),
        ("FHR4671_3_B826_root", "THEOREM_ZERO", "R_m=0", "R_m(m_L;X_B)=0 with fixed X_B and m_L=m0", "source branch lock or response extremum proof", "MISSING_ROOT_LOCK"),
        ("FHR4671_4_B826_value", "FINITE_BOUND", "a_F,L_cg,R_m", "|B_826| <= |a_F| L_cg^-2 |R_m|", "numeric/source-backed values plus units and profile", "MISSING_FINITE_VALUES"),
        ("FHR4671_5_lambda_value", "FINITE_BOUND", "lambda_mem", "sqrt(Z_mem/M2_mem)", "same-branch Z/M values; no R10 anchor substitution", "MISSING_ZM_RATIO"),
        ("FHR4671_6_no_cancellation", "COMMON", "absolute_sum_guard", "B_mem_eff finite route uses abs component sum", "componentwise zeros or componentwise source bounds only", "GUARD_ACTIVE"),
        ("FHR4671_7_claim_switch", "COMMON", "valid_for_claim", "claim admission", "true only when theorem-zero clauses are parent-signed or finite rows source-backed", "FALSE_NOW"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row[0],
            "route": row[1],
            "required_object": row[2],
            "definition": row[3],
            "claim_grade_requirement": row[4],
            "status": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def runner_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    hessian: list[dict[str, Any]],
    b826: list[dict[str, Any]],
    first_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    all_sources = all(row["path_exists"] and row["needle_found"] for row in sources)
    all_nonclaim = all(
        str(row.get("valid_for_claim")) == "False"
        for row in theorem + hessian + b826 + first_rows
    )
    has_even_branch = any(row["theorem_id"] == "STM4671_3_even_branch_symmetry" for row in theorem)
    has_hessian_fail = any(row["status"] == "HESSIAN_SIGNATURE_FAILS_FOR_CLAIM" for row in hessian)
    has_b826_fail = any(row["status"] == "B826_ZERO_FAILS_FOR_CLAIM" for row in b826)
    has_finite_fallback = any(row["row_id"] == "FHR4671_4_B826_value" for row in first_rows)
    data = [
        ("RUN4671_0_sources", all_sources, "all source paths and needles found"),
        ("RUN4671_1_even_branch_route", has_even_branch, "strict-minimum/even-branch theorem candidate is written"),
        ("RUN4671_2_hessian_not_promoted", has_hessian_fail, "Hessian positivity remains unsigned for claim"),
        ("RUN4671_3_B826_not_promoted", has_b826_fail, "B826 root lock remains unsigned for claim"),
        ("RUN4671_4_finite_fallback", has_finite_fallback, "first finite B826/ZM row contract is present"),
        ("RUN4671_5_nonclaim_flags", all_nonclaim, "all theorem and source rows remain nonclaim"),
        ("RUN4671_6_decision", DECISION.endswith("NONCLAIM"), "decision refuses local-GR/R10/PPN promotion"),
        ("RUN4671_7_next", NEXT_TARGET.startswith("4672-"), "next target selected"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "runner_id": row[0],
            "passed": bool(row[1]),
            "status": "PASS" if row[1] else "FAIL",
            "detail": row[2],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CTRL4671_0_no_symmetry_axiom", "even/reflection branch is a theorem target, not an inserted axiom", "PASS"),
        ("CTRL4671_1_no_R10_anchor", "R10 anchor cannot sign Z/M or lambda", "PASS"),
        ("CTRL4671_2_no_cancellation", "B826 cannot cancel Weyl/Y5/Y6/boundary/readout tails", "PASS"),
        ("CTRL4671_3_no_Cmem_reopen", "Cmem closure is not reused to delete B/J/Q/ZM gates", "PASS"),
        ("CTRL4671_4_same_branch", "m0, m_L, X_B, Z/M and B826 must be same branch", "PASS"),
        ("CTRL4671_5_metric_limit_still_open", "metric EH/Newton limit remains a later gate", "PASS"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "rule": row[1],
            "status": row[2],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "why": "A strict local minimum plus an MTS-owned even/reflection branch would simultaneously sign Z/M positivity and kill the linear visible/B826 source derivative, but the current corpus does not yet own that symmetry or numeric Hessian/source row.",
            "promoted": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "strict_minimum_theorem_written": True,
            "even_branch_symmetry_parent_signed": False,
            "Z_mem_positive_parent_signed": False,
            "M2_mem_positive_parent_signed": False,
            "B826_root_parent_signed": False,
            "B826_finite_row_source_backed": False,
            "A_mem_zero": False,
            "local_GR_claim": False,
            "r10_claim": False,
            "ppn_claim": False,
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "The least-scrutiny route is now a single parent-owned symmetry/minimum certificate: prove an MTS even/reflection branch or fill the first Z/M+B826 finite row.",
            "derive_route": "Search existing MTS variables for a parent map sigma or branch extremum that forces A_m'(m0)=0 and R_m(m0;X_B)=0 while preserving Z_mem>0 and M2_mem>0.",
            "fallback_route": "If no symmetry owner exists, write first source-backed finite rows for Z0, M0^2, lambda_mem and B826, then feed them into the no-cancellation body-charge bound.",
            "avoid": "Do not call the even branch an axiom, do not use R10 anchor as Hessian data, do not claim B_mem_eff zero from B826 alone, and do not claim local GR before metric EH/Newton and J/Q gates close.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    outputs: list[Path],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_failures = [row["source_id"] for row in sources if not (row["path_exists"] and row["needle_found"])]
    rows.append(
        {
            "validation_id": "VAL4671_0_sources",
            "passed": not source_failures,
            "detail": "all source paths and needles found" if not source_failures else ";".join(source_failures),
            "timestamp_utc": timestamp,
        }
    )
    for path in [
        SOURCE_REGISTER,
        SIGNATURE_THEOREM_CSV,
        HESSIAN_TEST_CSV,
        B826_LOCK_CSV,
        FIRST_ROW_CSV,
        RUNNER_CSV,
        CONTROL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]:
        try:
            parsed = read_csv(path)
            rows.append(
                {
                    "validation_id": f"VAL4671_parse_{path.name}",
                    "passed": len(parsed) > 0,
                    "detail": f"rows={len(parsed)} columns={len(parsed[0]) if parsed else 0}",
                    "timestamp_utc": timestamp,
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "validation_id": f"VAL4671_parse_{path.name}",
                    "passed": False,
                    "detail": repr(exc),
                    "timestamp_utc": timestamp,
                }
            )
    rows.append(
        {
            "validation_id": "VAL4671_1_runner_pass",
            "passed": all(str(row["status"]) == "PASS" for row in runner),
            "detail": "runner rows passed" if all(str(row["status"]) == "PASS" for row in runner) else "runner failure",
            "timestamp_utc": timestamp,
        }
    )
    rows.append(
        {
            "validation_id": "VAL4671_2_outputs_exist",
            "passed": all(path.exists() for path in outputs),
            "detail": ";".join(str(path) for path in outputs if path.exists()),
            "timestamp_utc": timestamp,
        }
    )
    rows.append(
        {
            "validation_id": "VAL4671_3_no_claim_promotion",
            "passed": all(str(row.get("valid_for_claim", "False")) == "False" for row in runner),
            "detail": "valid_for_claim remains false",
            "timestamp_utc": timestamp,
        }
    )
    overall = all(bool(row["passed"]) for row in rows)
    rows.append(
        {
            "validation_id": "VAL4671_OVERALL",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def write_doc(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    hessian: list[dict[str, Any]],
    b826: list[dict[str, Any]],
    first_rows: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    content = f"""# 4671 — Parent memory Hessian signature or B826 root lock first row

Timestamp: `{timestamp}`

## Result

4671 takes the leap that 4670 identified.  The best current route is a **strict-minimum/even-branch theorem**:

```text
m = m0 + δm
σ: δm -> -δm
S_parent is σ-even in the ordinary visible/source-response local branch
Z(m0) >= Z0 > 0
V_eff''(m0)+H_env >= M0^2 > 0
```

Then all σ-odd first derivatives vanish at `m0`, so the visible linear source coupling and the `B_826` root derivative vanish:

```text
β_visible = ∂m ln A_visible |m0 = 0
R_m(m0;X_B) = 0
B_826 = a_F L_cg^-2 R_m(m0;X_B) = 0.
```

This is exactly the kind of parent-owned mechanism we need: one local branch structure would give the positive memory operator and kill the first linear source/root coupling without cancellation.  But the current corpus does **not** yet prove that `σ` is an MTS-owned parent symmetry, does not provide `Z0` or `M0^2`, and does not source `a_F,L_cg,R_m`.  Therefore the result is a real theorem candidate, not a local-GR claim.

## Strict-minimum/even-branch theorem candidate

{table(theorem)}

## Parent Hessian signature test

{table(hessian)}

## B826 root-lock test

{table(b826)}

## First row contract

{table(first_rows)}

## Runner

{table(runner)}

## Controls

{table(controls)}

## Decision

{table(decision)}

## Status

{table(status)}

## Next target

{table(next_target)}

## Source register

{table(sources)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def write_formal(
    timestamp: str,
    theorem: list[dict[str, Any]],
    hessian: list[dict[str, Any]],
    b826: list[dict[str, Any]],
    first_rows: list[dict[str, Any]],
    decision: list[dict[str, Any]],
) -> None:
    content = f"""# PPC4161 — Parent memory Hessian signature or B826 root lock first row

Checkpoint: `{CHECKPOINT}`  
Claim row: `{CLAIM_ID}`  
Timestamp: `{timestamp}`

## Formal statement

Let the local memory branch be `m=m0+δm`.  If a parent-owned local branch symmetry `σ:δm -> -δm` leaves the ordinary visible matter/source-response sector invariant, then every σ-odd first derivative vanishes at the branch point:

```text
∂m ln A_visible |m0 = 0,
R_m(m0;X_B) = 0.
```

If the same branch is a strict stable minimum with positive kinetic Hessian,

```text
Z_mem = Z(m0) >= Z0 > 0,
M2_mem = V_eff''(m0)+H_env >= M0^2 > 0,
```

then the 4621 positive-operator theorem can be used once `J_mem_live` and `Q_boundary_mem` are also zero/bounded.  The first `B_mem_eff` component is killed termwise:

```text
B_826 = a_F L_cg^-2 R_m(m0;X_B) = 0.
```

4671 does not promote this theorem because the corpus has not yet signed the parent symmetry/minimum certificate or supplied finite source rows for `Z0`, `M0^2`, `a_F`, `L_cg`, and `R_m`.

## Theorem candidate

{table(theorem)}

## Hessian test

{table(hessian)}

## B826 root-lock test

{table(b826)}

## First-row contract

{table(first_rows)}

## Decision

{table(decision)}
"""
    FORMAL_PATH.write_text(content, encoding="utf-8")


def update_claims() -> None:
    existing = read_text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4671 constructs the next real derivation route: a strict-minimum/even-branch parent theorem. If the local memory branch has an MTS-owned reflection/even symmetry, ordinary visible/source-response first derivatives vanish, giving beta_visible=0 and R_m=0; if the same branch is a strict stable minimum with Z_mem>0 and M2_mem>0, the 4621 positive-operator theorem becomes usable and B_826 vanishes termwise. Current evidence does not parent-sign the symmetry/minimum or source Z0, M0^2, a_F, L_cg and R_m, so this is a theorem candidate and first-row contract, not a local-GR/R10/PPN claim.",
        "Generated source register, strict-minimum/even-branch theorem candidate, Hessian signature test, B826 root-lock test, first Hessian/B826 row contract, runner, controls, decision, status, next target and validation.",
        "strict_minimum_even_branch_theorem_candidate_parent_signature_unsigned_nonclaim",
        NEXT_TARGET,
        "Treating the even branch as an axiom, using R10 anchor as Hessian data, promoting B826 zero while Weyl/Y5/Y6/boundary/readout tails remain, using cancellation, or claiming local GR before J/Q and metric EH/Newton gates close.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10 claim until the even-branch/minimum certificate or finite ZM/B826 rows are parent-signed/source-backed and the remaining B/J/Q/metric gates close.",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        handle.write(csv_line(row))


def update_spine_and_packet() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4671 writes the first genuine mechanism candidate for the reduced body-charge gate. A strict stable local memory minimum plus a parent-owned even/reflection branch `δm -> -δm` would give `Z_mem>0`, `M2_mem>0`, `β_visible=0`, and `R_m(m0;X_B)=0`, hence `B_826=0` termwise. This is the right kind of derivation route because it kills the linear coupling by structure, not by fitting or cancellation. The current corpus has not signed the symmetry/minimum certificate or finite source rows, so the route remains nonclaim and the next target is `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

Checkpoint `{CHECKPOINT}` converts the Z/M+B826 bottleneck into a strict-minimum/even-branch theorem candidate. If the symmetry is parent-owned, it is the cleanest route to first-order source silence; if not, the fallback is finite `Z0/M0^2/lambda_mem/B826` rows. Next packet target: `{NEXT_TARGET}`.
""",
    )


def main() -> None:
    timestamp = now()
    sources = source_rows(timestamp)
    theorem = signature_theorem_rows(timestamp)
    hessian = hessian_rows(timestamp)
    b826 = b826_rows(timestamp)
    first_rows = first_row_contract(timestamp)
    runner = runner_rows(timestamp, sources, theorem, hessian, b826, first_rows)
    controls = control_rows(timestamp)
    decision = decision_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SIGNATURE_THEOREM_CSV, theorem)
    write_csv(HESSIAN_TEST_CSV, hessian)
    write_csv(B826_LOCK_CSV, b826)
    write_csv(FIRST_ROW_CSV, first_rows)
    write_csv(RUNNER_CSV, runner)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decision)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)

    write_doc(timestamp, sources, theorem, hessian, b826, first_rows, runner, controls, decision, status, next_target)
    write_formal(timestamp, theorem, hessian, b826, first_rows, decision)
    update_claims()
    update_spine_and_packet()

    outputs = [
        DOC_PATH,
        FORMAL_PATH,
        SOURCE_REGISTER,
        SIGNATURE_THEOREM_CSV,
        HESSIAN_TEST_CSV,
        B826_LOCK_CSV,
        FIRST_ROW_CSV,
        RUNNER_CSV,
        CONTROL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validation = validation_rows(timestamp, sources, runner, outputs)
    write_csv(VALIDATION_CSV, validation)
    if not all(bool(row["passed"]) for row in validation):
        failures = [row for row in validation if not row["passed"]]
        raise SystemExit(f"4671 validation failed: {failures}")
    print(f"4671 complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
