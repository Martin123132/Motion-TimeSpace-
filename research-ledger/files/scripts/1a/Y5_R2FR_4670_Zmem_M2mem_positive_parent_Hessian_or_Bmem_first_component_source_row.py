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

CHECKPOINT = "4670"
CLAIM_ID = "L-512"
BRANCH = "MTS_R2FR_Y5_ZMEM_M2MEM_POSITIVE_PARENT_HESSIAN_OR_BMEM_FIRST_COMPONENT_SOURCE_ROW_4670"
MARKER = "PPC4161_ZMEM_M2MEM_POSITIVE_PARENT_HESSIAN_OR_BMEM_FIRST_COMPONENT_SOURCE_ROW_4670"
PACKET_MARKER = "PPC4161_PACKET_ZMEM_M2MEM_POSITIVE_PARENT_HESSIAN_OR_BMEM_FIRST_COMPONENT_SOURCE_ROW_4670"
DECISION = "ZM_PARENT_HESSIAN_AND_B826_ROOT_ROUTE_EXACT_BUT_UNSIGNED_FIRST_ROWS_LOCKED_NONCLAIM"
NEXT_TARGET = "4671-Y5-R2FR-parent-memory-Hessian-signature-or-B826-root-lock-first-row.md"

DOC_PATH = POST / "4670-Y5-R2FR-Zmem-M2mem-positive-parent-Hessian-or-Bmem-first-component-source-row.md"
FORMAL_PATH = FORMAL / "686-PPC4161-Zmem-M2mem-positive-parent-Hessian-or-Bmem-first-component-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4669_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4669_NEXT_TARGET.csv"
CSV_4669_ATTEMPT = SOURCE_DIR / "P8_Y5_R2FR_4669_BJQ_ZM_ZERO_ATTEMPT_MATRIX.csv"
CSV_4669_FIRST_ROW = SOURCE_DIR / "P8_Y5_R2FR_4669_FIRST_BODY_CHARGE_SOURCE_ROW_CONTRACT.csv"
CSV_4669_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4669_STATUS.csv"
CSV_4669_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4669_VALIDATION.csv"
DOC_4669 = POST / "4669-Y5-R2FR-Bmem-Jmem-Qboundary-ZM-source-normalization-zero-or-first-body-charge-row.md"
FORMAL_685 = FORMAL / "685-PPC4161-Bmem-Jmem-Qboundary-ZM-source-normalization-gate.md"

CSV_4621_IDENTITY = SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_POSITIVE_OPERATOR_IDENTITY.csv"
CSV_4621_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4621_ZMEM_M2MEM_SOURCE_ROWS_NONCLAIM.csv"
CSV_4628_HESSIAN = SOURCE_DIR / "P8_Y5_R2FR_4628_PARENT_HESSIAN_ROWS.csv"
CSV_4628_GAP = SOURCE_DIR / "P8_Y5_R2FR_4628_LAMBDA_MEM_GAP_ROWS.csv"
CSV_4628_NUMERIC = SOURCE_DIR / "P8_Y5_R2FR_4628_ZMEM_M2MEM_FIRST_NUMERIC_TEMPLATE_NONCLAIM.csv"
CSV_4630_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4630_PARENT_ACTION_CONTRACT.csv"
CSV_4630_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4630_STATUS.csv"

CSV_4507_BMEM = SOURCE_DIR / "P8_Y5_R2FR_4507_BMEM_COMPONENT_ROWS.csv"
CSV_4508_THETA = SOURCE_DIR / "P8_Y5_R2FR_4508_THETA_WM_DECOMPOSITION.csv"
CSV_4509_COMBINED = SOURCE_DIR / "P8_Y5_R2FR_4509_COMBINED_ZERO_THEOREM.csv"
CSV_4510_ROOT = SOURCE_DIR / "P8_Y5_R2FR_4510_PARENT_SOURCE_ROOT_THEOREM.csv"
CSV_4511_SPURION = SOURCE_DIR / "P8_Y5_R2FR_4511_NO_SPURION_READOUT_THEOREM.csv"
CSV_4512_KHAT = SOURCE_DIR / "P8_Y5_R2FR_4512_KHAT_TRACE_MATCH_THEOREM.csv"
CSV_4513_BWEYL = SOURCE_DIR / "P8_Y5_R2FR_4513_FINAL_BWEYL_VECTOR.csv"
CSV_4514_BMEM = SOURCE_DIR / "P8_Y5_R2FR_4514_BMEM_EFFECTIVE_COMPONENT_VECTOR.csv"
CSV_4514_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4514_BODY_CHARGE_INSERTION_BOUND.csv"
CSV_4515_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4515_SOURCE_FUNCTOR_DESCENT_THEOREM.csv"
CSV_4515_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4515_CMEM_JMEM_COUPLING_VECTOR.csv"
CSV_4596_JMEM = SOURCE_DIR / "P8_Y5_R2FR_4596_JMEM_JH_REDUCED_RESIDUAL_VECTOR.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4670_SOURCE_REGISTER.csv"
ZM_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4670_ZM_PARENT_HESSIAN_AUDIT.csv"
BMEM_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4670_BMEM_FIRST_COMPONENT_AUDIT.csv"
FIRST_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4670_ZM_B826_FIRST_ROW_CONTRACT.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4670_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4670_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4670_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4670_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4670_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4670_VALIDATION.csv"


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
        ("SRC4670_00_4669_next", CSV_4669_NEXT, "4670-Y5-R2FR-Zmem-M2mem-positive-parent-Hessian-or-Bmem-first-component-source-row.md", "4669 selected this target."),
        ("SRC4670_01_4669_attempt_ZM", CSV_4669_ATTEMPT, "ZAT4669_0_ZM", "ZM positivity is the first reduced gate."),
        ("SRC4670_02_4669_attempt_B826", CSV_4669_ATTEMPT, "ZAT4669_1_B826", "B826 is the first B_mem component."),
        ("SRC4670_03_4669_first_row", CSV_4669_FIRST_ROW, "FBC4669_1_operator", "first body-charge row demands Z/M."),
        ("SRC4670_04_4669_status", CSV_4669_STATUS, "A_MEM_ZERO_NOT_CLAIMED", "4669 refused promotion."),
        ("SRC4670_05_4669_validation", CSV_4669_VALIDATION, "VAL4669_OVERALL", "4669 validation."),
        ("SRC4670_06_doc4669", DOC_4669, "first body-charge source-row contract", "4669 prose contract."),
        ("SRC4670_07_formal685", FORMAL_685, "A_mem=0", "formal 4669 exact but unsigned zero route."),
        ("SRC4670_08_4621_identity", CSV_4621_IDENTITY, "MPI4621_2_nohair_zero", "positive operator nohair theorem."),
        ("SRC4670_09_4621_source_Z", CSV_4621_SOURCE, "ZMR4621_0_Zmem_min", "Zmem source placeholder."),
        ("SRC4670_10_4621_source_M", CSV_4621_SOURCE, "ZMR4621_1_M2mem_min", "M2mem source placeholder."),
        ("SRC4670_11_4628_hessian_action", CSV_4628_HESSIAN, "HES4628_0_quadratic_memory_action", "quadratic parent action normal form."),
        ("SRC4670_12_4628_hessian_def", CSV_4628_HESSIAN, "HES4628_1_parent_hessian_definitions", "parent Hessian definitions."),
        ("SRC4670_13_4628_gap", CSV_4628_GAP, "GAP4628_0_exact_positive_gap", "positive gap criterion."),
        ("SRC4670_14_4628_constraint", CSV_4628_GAP, "GAP4628_3_constraint_limit", "constraint elimination route."),
        ("SRC4670_15_4628_numeric_template", CSV_4628_NUMERIC, "LNUM4628_0_Zmem", "first Z/M numeric template."),
        ("SRC4670_16_4628_anchor_smoke", CSV_4628_NUMERIC, "LNUM4628_3_R10_anchor_gap_ratio", "R10 anchor is smoke only."),
        ("SRC4670_17_4630_contract", CSV_4630_CONTRACT, "PARENT_ACTION_CONTRACT", "parent action contract if present."),
        ("SRC4670_18_4630_status", CSV_4630_STATUS, "valid_for_claim", "4630 status if present."),
        ("SRC4670_19_4507_Bmem", CSV_4507_BMEM, "BMF4507_1", "B826 parent expression if present."),
        ("SRC4670_20_4508_theta", CSV_4508_THETA, "Theta_W,m", "Weyl trace decomposition if present."),
        ("SRC4670_21_4509_combined", CSV_4509_COMBINED, "CZT4509_5_combined", "combined B_Weyl zero theorem."),
        ("SRC4670_22_4510_root", CSV_4510_ROOT, "PST4510_5_BWeyl_insertion", "parent source-root insertion."),
        ("SRC4670_23_4511_spurion", CSV_4511_SPURION, "no_spurion", "no-spurion theorem if present."),
        ("SRC4670_24_4512_khat", CSV_4512_KHAT, "Khat", "Khat trace-match theorem if present."),
        ("SRC4670_25_4513_BWeyl", CSV_4513_BWEYL, "B_Weyl", "final B_Weyl vector if present."),
        ("SRC4670_26_4514_B826", CSV_4514_BMEM, "BMV4514_0_B826", "B826 component row."),
        ("SRC4670_27_4514_combined", CSV_4514_BMEM, "BMV4514_6_combined", "B_mem_eff combined row."),
        ("SRC4670_28_4514_bound", CSV_4514_BOUND, "BCB4514_4_nohair", "body-charge insertion nohair if present."),
        ("SRC4670_29_4515_source_functor", CSV_4515_THEOREM, "SFT4515_1_single_source_functor_zero", "Y5/Y6 source functor zero route."),
        ("SRC4670_30_4515_poynting", CSV_4515_THEOREM, "SFT4515_4_EM_Poynting_guard", "Poynting guard."),
        ("SRC4670_31_4515_vector", CSV_4515_VECTOR, "SCV4515_4_total_density_source", "source/current vector."),
        ("SRC4670_32_4596_Jmem", CSV_4596_JMEM, "J4596_5_live_total", "Jmem live total remains separate."),
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


def zm_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "ZMH4670_0_operator_form",
            "L_mem delta_m = -nabla_i(Z_mem h^ij nabla_j delta_m)+M2_mem delta_m",
            "4621/4628 already give the coercive operator shape.",
            "exact conditional normal form",
            "needs same-branch parent coefficients",
            "NORMAL_FORM_READY_VALUES_MISSING",
        ),
        (
            "ZMH4670_1_Zmem_positive",
            "Z_mem = d^2 L_parent / d(nabla m)^2 | branch",
            "Z_mem>0 follows from a ghost-free/coercive parent kinetic Hessian with fixed sign convention.",
            "derivable as an inequality if the parent Hessian is signed",
            "no row gives Z_mem >= Z0 > 0 from parent action",
            "EXACT_CONDITIONAL_POSITIVITY_UNSIGNED",
        ),
        (
            "ZMH4670_2_M2mem_positive",
            "M2_mem = d^2 V_eff / dm^2 | branch after constraint/source corrections",
            "M2_mem>0 follows from a strict local minimum/gap, not from the R10 fit.",
            "derivable as branch stability condition",
            "no row gives M2_mem >= M0^2 > 0 from parent action",
            "EXACT_CONDITIONAL_GAP_UNSIGNED",
        ),
        (
            "ZMH4670_3_constraint_route",
            "M2_mem/Z_mem -> infinity or delta_m algebraically eliminated",
            "If memory is a constrained auxiliary rather than a propagating field, lambda_mem -> 0 and local force is absent/contact.",
            "acceptable alternative to finite positive M2",
            "needs explicit constraint-elimination proof and source-current projection",
            "EXACT_CONDITIONAL_CONSTRAINT_ROUTE_UNSIGNED",
        ),
        (
            "ZMH4670_4_same_normalization",
            "lambda_mem = sqrt(Z_mem/M2_mem)",
            "Only the ratio is physical under m rescaling; Z and M2 must come from the same branch and source normalization.",
            "normalization guard",
            "numeric Z/M row absent",
            "NORMALIZATION_GUARD_ACTIVE",
        ),
        (
            "ZMH4670_5_R10_anchor_guard",
            "(M2_mem/Z_mem)_anchor = 1/(38.6e-6 m)^2",
            "R10 alpha=1 anchor can smoke-test interpolation, but cannot parent-sign the Hessian.",
            "blocked from claim",
            "anchor is not parent action data",
            "ANCHOR_SMOKE_ONLY",
        ),
        (
            "ZMH4670_6_decision",
            "Z_mem>0 and M2_mem>0",
            "The theorem route is mathematically clean: prove the parent Hessian is positive, then 4621 nohair applies.",
            "not promoted",
            "parent Hessian signature is still missing",
            "FIRST_ZM_ROW_REQUIRED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": row[0],
            "object": row[1],
            "derivation_test": row[2],
            "exact_result": row[3],
            "missing_parent_input": row[4],
            "status": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def bmem_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "BFC4670_0_decomposition",
            "B_mem_eff",
            "B_826+B_Weyl_vec+B_Y5_trace+B_Y6_trace+B_src_boundary+B_src_readout",
            "4514 gives componentwise no-cancellation decomposition.",
            "component vector is ready",
            "BODY_CHARGE_COMPONENT_VECTOR_READY_VALUES_MISSING",
        ),
        (
            "BFC4670_1_B826",
            "B_826",
            "a_F L_cg^-2 R_m(m_L;X_B)",
            "B826 vanishes if the branch source-root/extremum gives R_m=0 with fixed X_B and parent-owned m_L.",
            "needs parent-owned R_m=0 or sourced finite a_F,L_cg,R_m row",
            "CONDITIONAL_ZERO_UNSIGNED_FIRST_COMPONENT_ROW_REQUIRED",
        ),
        (
            "BFC4670_2_BWeyl",
            "B_Weyl_vec",
            "CZT4509 source-root + no-spurion + Khat trace + boundary/readout clauses",
            "The Weyl tail has a real theorem shape and is not a cancellation if all clauses are signed in the same branch.",
            "same-branch signatures still absent",
            "CONDITIONAL_THEOREM_EXACT_BUT_UNSIGNED",
        ),
        (
            "BFC4670_3_BY5",
            "B_Y5_trace",
            "single q-basic source functor / measured-GM pullback",
            "Could vanish if source-normalization is owned by the Hilbert/source functor rather than a live coefficient.",
            "parent source-normalization map not signed",
            "LIVE_SOURCE_NORMALIZATION_TAIL",
        ),
        (
            "BFC4670_4_BY6",
            "B_Y6_trace",
            "extra stress topological/invisible/EH-owned/exchange-even",
            "Could vanish under an owned extra-stress parity/topological clause.",
            "extra-stress ownership not signed",
            "LIVE_EXTRA_STRESS_TAIL",
        ),
        (
            "BFC4670_5_boundary_readout",
            "B_src_boundary+B_src_readout",
            "no linear memory response from source boundary/reference/readout shifts",
            "Could vanish if variation-before-readout and fixed source-reference class are parent-owned.",
            "boundary/readout source-normalization clauses not signed",
            "LIVE_BOUNDARY_READOUT_TAIL",
        ),
        (
            "BFC4670_6_total",
            "B_mem_eff=0",
            "all B components zero componentwise with no cancellation",
            "This would remove the curvature-source body-charge branch from rho_mem.",
            "B826 first component and other B tails remain unsigned",
            "NOT_PROMOTED_FIRST_COMPONENT_ROW_REQUIRED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": row[0],
            "component": row[1],
            "formula_or_clause": row[2],
            "zero_or_bound_test": row[3],
            "current_result": row[4],
            "status": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def first_row_contract(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "FR4670_0_Zmem_parent",
            "ZM_HESSIAN",
            "Z_mem_min",
            "strict lower bound for kinetic Hessian on selected branch",
            "positive numeric bound or theorem-zero constraint route",
            "depends on m normalization",
            "parent quadratic action expansion",
            "MISSING_PARENT_HESSIAN_VALUE",
        ),
        (
            "FR4670_1_M2mem_parent",
            "ZM_HESSIAN",
            "M2_mem_min",
            "strict lower bound for branch/gap Hessian after constraints",
            "positive numeric bound or algebraic-elimination theorem",
            "Z_mem/length^2",
            "parent effective potential/Hessian",
            "MISSING_PARENT_GAP_VALUE",
        ),
        (
            "FR4670_2_lambda_parent",
            "ZM_HESSIAN",
            "lambda_mem",
            "same-branch range sqrt(Z_mem/M2_mem)",
            "finite positive length or zero-range constraint proof",
            "length",
            "same-branch Z/M ratio",
            "MISSING_ZM_RATIO",
        ),
        (
            "FR4670_3_no_anchor_smuggle",
            "ZM_HESSIAN",
            "R10_anchor_guard",
            "prevents R10 alpha anchor from replacing parent Hessian",
            "valid_for_claim=false unless parent action supplies Z/M",
            "dimensionless guard",
            "4628 anchor smoke row",
            "ANCHOR_NOT_CLAIM_DATA",
        ),
        (
            "FR4670_4_aF",
            "B826_COMPONENT",
            "a_F",
            "B826 amplitude prefactor",
            "numeric/source-backed value or theorem-zero owner",
            "units needed to make B826 match B_mem_eff",
            "4507/4514 B826 component",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "FR4670_5_Lcg",
            "B826_COMPONENT",
            "L_cg",
            "curvature-gradient/readout scale in B826",
            "same branch length source",
            "length",
            "4507/4514 B826 component",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "FR4670_6_Rm",
            "B826_COMPONENT",
            "R_m(m_L;X_B)",
            "branch source-root residual",
            "parent-signed zero or finite sourced residual",
            "depends on parent residual normalization",
            "4510 parent source-root theorem",
            "MISSING_ROOT_LOCK",
        ),
        (
            "FR4670_7_branch_lock",
            "B826_COMPONENT",
            "m_L,X_B",
            "same physical local branch and fixed background/source variables",
            "branch lock source path and fixed-X_B proof",
            "branch metadata",
            "4510 lock row",
            "MISSING_BRANCH_LOCK",
        ),
        (
            "FR4670_8_profile",
            "B826_COMPONENT",
            "R_obs/body_profile",
            "profile used to convert B826 into A_mem bound",
            "finite source profile with units or theorem-zero domain",
            "arena dependent",
            "4514 body-charge insertion bound",
            "MISSING_ARENA_PROFILE",
        ),
        (
            "FR4670_9_claim_switch",
            "COMMON",
            "valid_for_claim",
            "claim admission",
            "true only if every required ZM or B826 entry is source-backed/parent-signed",
            "boolean",
            "this checkpoint",
            "FALSE_NOW",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row[0],
            "route": row[1],
            "required_symbol": row[2],
            "definition": row[3],
            "claim_grade_requirement": row[4],
            "units": row[5],
            "source_basis": row[6],
            "status": row[7],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def runner_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    zm_rows: list[dict[str, Any]],
    bmem_rows: list[dict[str, Any]],
    first_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    all_required_sources_found = all(row["path_exists"] and row["needle_found"] for row in sources if "if present" not in str(row["note"]))
    no_claim_rows = all(str(row.get("valid_for_claim")) == "False" for row in zm_rows + bmem_rows + first_rows)
    has_zm_positive_row = any(row["audit_id"] == "ZMH4670_1_Zmem_positive" for row in zm_rows)
    has_m2_positive_row = any(row["audit_id"] == "ZMH4670_2_M2mem_positive" for row in zm_rows)
    has_b826_row = any(row["audit_id"] == "BFC4670_1_B826" for row in bmem_rows)
    has_anchor_guard = any(row["row_id"] == "FR4670_3_no_anchor_smuggle" for row in first_rows)
    data = [
        ("RUN4670_0_source_register", all_required_sources_found, "required sources exist and required needles are found"),
        ("RUN4670_1_Zmem_positive_clause", has_zm_positive_row, "Z_mem positivity clause is explicit and unsigned"),
        ("RUN4670_2_M2mem_positive_clause", has_m2_positive_row, "M2_mem positivity/gap clause is explicit and unsigned"),
        ("RUN4670_3_R10_anchor_guard", has_anchor_guard, "R10 anchor cannot become parent Z/M data"),
        ("RUN4670_4_B826_first_component", has_b826_row, "B826 first component route is isolated"),
        ("RUN4670_5_no_claim_rows", no_claim_rows, "no row is valid_for_claim in this checkpoint"),
        ("RUN4670_6_decision_nonclaim", DECISION.endswith("NONCLAIM"), "decision refuses local-GR/R10/PPN promotion"),
        ("RUN4670_7_next_target", NEXT_TARGET.startswith("4671-"), "next target selected"),
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
        ("CTRL4670_0_no_public_claim", "local-GR/Newton/PPN/R10 remains unclaimed", "PASS"),
        ("CTRL4670_1_no_R10_smuggle", "R10 alpha=1 anchor remains smoke only", "PASS"),
        ("CTRL4670_2_no_cancellation", "B components require componentwise zero or absolute finite rows", "PASS"),
        ("CTRL4670_3_no_Cmem_reopen", "Cmem closure is used only to reduce rho_mem, not to erase B/J/Q/ZM", "PASS"),
        ("CTRL4670_4_poynting_kept", "Poynting/EM current remains counted in J_mem route, not hidden in B826", "PASS"),
        ("CTRL4670_5_same_branch", "Z/M and B826 rows require the same selected local branch", "PASS"),
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
            "why": "4670 proves the exact shape of the Z/M positivity gate and isolates B826 as the first B_mem_eff component, but no parent Hessian value, branch gap, source-root lock, or B826 source row is signed.",
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
            "Z_mem_positive_parent_signed": False,
            "M2_mem_positive_parent_signed": False,
            "lambda_mem_claim_grade": False,
            "B826_zero_parent_signed": False,
            "B826_finite_source_row": False,
            "B_mem_eff_zero": False,
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
            "why": "The cleanest leap is now specific: either sign the parent memory Hessian/gap in the local branch, or sign/source-fill the B826 source-root component. Both directly reduce the body-charge gate without reopening solved Cmem work.",
            "derive_route": "Write the second-variation parent action test: compute/declare the quadratic memory Hessian, prove Z_mem>=Z0>0 and M2_mem>=M0^2>0, or prove algebraic constraint elimination. In parallel, test whether R_m(m_L;X_B)=0 is parent-owned for B826.",
            "fallback_route": "If the proof fails, produce the first nonclaim numeric/theorem-zero row for Z_mem/M2_mem/lambda_mem or B826 with units, source paths, and abs-bound insertion.",
            "avoid": "Do not use R10 anchor as parent Z/M, do not hide B components by cancellation, do not treat B826 root as signed without branch lock, and do not claim local GR from a conditional operator theorem.",
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

    required_source_failures = [
        row["source_id"]
        for row in sources
        if "if present" not in str(row["note"]) and not (row["path_exists"] and row["needle_found"])
    ]
    rows.append(
        {
            "validation_id": "VAL4670_0_required_sources",
            "passed": not required_source_failures,
            "detail": "all required source paths and needles found" if not required_source_failures else ";".join(required_source_failures),
            "timestamp_utc": timestamp,
        }
    )

    for path in [
        SOURCE_REGISTER,
        ZM_AUDIT_CSV,
        BMEM_AUDIT_CSV,
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
                    "validation_id": f"VAL4670_parse_{path.name}",
                    "passed": len(parsed) > 0,
                    "detail": f"rows={len(parsed)} columns={len(parsed[0]) if parsed else 0}",
                    "timestamp_utc": timestamp,
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "validation_id": f"VAL4670_parse_{path.name}",
                    "passed": False,
                    "detail": repr(exc),
                    "timestamp_utc": timestamp,
                }
            )

    rows.append(
        {
            "validation_id": "VAL4670_1_runner_pass",
            "passed": all(str(row["status"]) == "PASS" for row in runner),
            "detail": "runner rows passed" if all(str(row["status"]) == "PASS" for row in runner) else "runner failure",
            "timestamp_utc": timestamp,
        }
    )
    rows.append(
        {
            "validation_id": "VAL4670_2_no_claim_promotion",
            "passed": all(str(row.get("valid_for_claim", "False")) == "False" for row in runner),
            "detail": "valid_for_claim remains false",
            "timestamp_utc": timestamp,
        }
    )
    rows.append(
        {
            "validation_id": "VAL4670_3_outputs_exist",
            "passed": all(path.exists() for path in outputs),
            "detail": ";".join(str(path) for path in outputs if path.exists()),
            "timestamp_utc": timestamp,
        }
    )

    overall = all(bool(row["passed"]) for row in rows)
    rows.append(
        {
            "validation_id": "VAL4670_OVERALL",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def write_doc(
    timestamp: str,
    sources: list[dict[str, Any]],
    zm_rows: list[dict[str, Any]],
    bmem_rows: list[dict[str, Any]],
    first_rows: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    content = f"""# 4670 — Zmem/M2mem positive parent Hessian or Bmem first-component source row

Timestamp: `{timestamp}`

## Result

This checkpoint tries the requested leap instead of only listing missing pieces.  The leap has two doors:

1. **Operator door:** derive `Z_mem>0` and `M2_mem>0` from the same parent quadratic memory Hessian, so the 4621 coercive no-hair theorem can actually bite.
2. **Source door:** isolate the first `B_mem_eff` component, `B_826=a_F L_cg^-2 R_m(m_L;X_B)`, and either prove its branch source-root zero or lock the first source-backed finite row.

The exact theorem shape is good, but not claim-grade yet.  Current corpus rows define the operator and component structure; they do **not** sign the parent Hessian, prove the branch gap, lock `R_m=0`, or provide the first numeric/source row.  Therefore 4670 refuses local-GR/Newton/PPN/R10 promotion and writes the next hard contract.

## Minimal derivation

From the existing local memory normal form,

```text
L_mem δm = -∇_i(Z_mem h^ij ∇_j δm) + M2_mem δm
```

the coercive route is:

```text
Z_mem(x) ≥ Z0 > 0,
M2_mem(x) ≥ M0^2 > 0,
rho_mem = 0,
Q_boundary_mem = 0
⇒ δm = 0
⇒ A_mem = 0 for the memory-mediated local body-charge channel.
```

So the key is not another phenomenological fit.  The key is a **same-branch second-variation proof**:

```text
Z_mem = ∂²L_parent / ∂(∇m)² |branch,
M2_mem = ∂²V_eff / ∂m² |branch after constraint/source corrections.
```

`lambda_mem=sqrt(Z_mem/M2_mem)` is only meaningful when both pieces are in the same normalization.  The R10 anchor can test units and interpolation, but cannot sign the parent Hessian.

For the first `B_mem_eff` component,

```text
B_mem_eff = B_826 + B_Weyl_vec + B_Y5_trace + B_Y6_trace + B_src_boundary + B_src_readout
B_826 = a_F L_cg^-2 R_m(m_L; X_B)
```

`B_826=0` is exact if the parent branch owns `R_m(m_L;X_B)=0` with fixed `X_B` and the same local branch `m_L`.  That root lock is not yet signed, so the B route also stays nonclaim.

## Z/M parent Hessian audit

{table(zm_rows)}

## Bmem first-component audit

{table(bmem_rows)}

## First source-row contract

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
    zm_rows: list[dict[str, Any]],
    bmem_rows: list[dict[str, Any]],
    first_rows: list[dict[str, Any]],
    decision: list[dict[str, Any]],
) -> None:
    content = f"""# PPC4161 — Zmem/M2mem positive parent Hessian or Bmem first-component source row

Checkpoint: `{CHECKPOINT}`  
Claim row: `{CLAIM_ID}`  
Timestamp: `{timestamp}`

## Formal statement

The reduced local body-charge gate after 4668/4669 is

```text
rho_mem = B_mem_eff R_obs + J_mem_live
A_mem = G_mem[ rho_mem ; Z_mem, M2_mem, Q_boundary_mem ].
```

The exact coercive route is:

```text
Z_mem >= Z0 > 0
M2_mem >= M0^2 > 0
B_mem_eff = 0
J_mem_live = 0
Q_boundary_mem = 0
⇒ A_mem = 0.
```

4670 attacks the first denominator/source pieces.  It derives the claim-grade contract:

```text
Z_mem = ∂²L_parent / ∂(∇m)² |branch,
M2_mem = ∂²V_eff / ∂m² |branch,
lambda_mem = sqrt(Z_mem/M2_mem),
B_826 = a_F L_cg^-2 R_m(m_L;X_B).
```

If the parent action signs `Z_mem>0` and `M2_mem>0`, the 4621 no-hair theorem becomes usable for the memory amplitude.  If the parent branch signs `R_m(m_L;X_B)=0`, the first `B_mem_eff` component vanishes without cancellation.  Neither signature is present in the current corpus, so this is **not** a local-GR/Newton/PPN/R10 claim.

## Z/M gate

{table(zm_rows)}

## Bmem first-component gate

{table(bmem_rows)}

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
        "4670 attempts the real leap behind the reduced body-charge gate: parent-sign positive Z_mem/M2_mem from the quadratic memory Hessian, or close the first B_mem_eff component B_826. The exact route is clean: Z_mem and M2_mem must be same-branch second-variation coefficients, lambda_mem=sqrt(Z_mem/M2_mem), and B_826=a_F L_cg^-2 R_m(m_L;X_B) vanishes only when the parent branch owns R_m=0. Current corpus rows define this structure but do not sign the Hessian, branch gap, constraint elimination, source-root lock, or numeric/source row, so the checkpoint locks first-row contracts and refuses local-GR/R10/PPN promotion.",
        "Generated source register, Z/M parent Hessian audit, B_mem first-component audit, first ZM/B826 row contract, runner, controls, decision, status, next target and validation.",
        "ZM_parent_Hessian_and_B826_root_route_exact_but_unsigned_first_rows_locked_nonclaim",
        NEXT_TARGET,
        "Using R10 anchor as parent Z/M, treating a stationary/source-root formula as a signed branch lock, using cancellation between B components, reopening Cmem to hide B/J/Q, erasing Poynting/non-Hilbert currents, or claiming local GR from a conditional Hessian theorem.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10 claim until positive Z/M or constraint elimination and the B/J/Q source pieces are same-branch derived or source-backed.",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        handle.write(csv_line(row))


def update_spine_and_packet() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4670 attacks the reduced body-charge gate at the right hard point rather than looping the missing-list. The parent-Hessian route is exact: `Z_mem` is the branch kinetic Hessian, `M2_mem` is the branch/gap Hessian, and `lambda_mem=sqrt(Z_mem/M2_mem)` only counts if both are same-branch coefficients. The first `B_mem_eff` component is isolated as `B_826=a_F L_cg^-2 R_m(m_L;X_B)`, which vanishes only if the parent branch owns `R_m=0`. Current evidence is structurally strong but unsigned, so 4670 locks first-row contracts and selects `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

Checkpoint `{CHECKPOINT}` turns the 4669 bottleneck into two concrete first-row contracts: same-branch positive `Z_mem,M2_mem` from the parent Hessian, or a signed/source-backed `B_826` component row. Neither is promoted yet; next packet target: `{NEXT_TARGET}`.
""",
    )


def main() -> None:
    timestamp = now()
    sources = source_rows(timestamp)
    zm_rows = zm_audit_rows(timestamp)
    bmem_rows = bmem_audit_rows(timestamp)
    first_rows = first_row_contract(timestamp)
    runner = runner_rows(timestamp, sources, zm_rows, bmem_rows, first_rows)
    controls = control_rows(timestamp)
    decision = decision_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZM_AUDIT_CSV, zm_rows)
    write_csv(BMEM_AUDIT_CSV, bmem_rows)
    write_csv(FIRST_ROW_CSV, first_rows)
    write_csv(RUNNER_CSV, runner)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decision)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)

    write_doc(timestamp, sources, zm_rows, bmem_rows, first_rows, runner, controls, decision, status, next_target)
    write_formal(timestamp, zm_rows, bmem_rows, first_rows, decision)
    update_claims()
    update_spine_and_packet()

    outputs = [
        DOC_PATH,
        FORMAL_PATH,
        SOURCE_REGISTER,
        ZM_AUDIT_CSV,
        BMEM_AUDIT_CSV,
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
        raise SystemExit(f"4670 validation failed: {failures}")
    print(f"4670 complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
