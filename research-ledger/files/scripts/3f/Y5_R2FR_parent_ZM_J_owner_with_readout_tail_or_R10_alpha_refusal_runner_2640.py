from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2640-Y5-R2FR-parent-ZM-J-owner-with-readout-tail-or-R10-alpha-refusal-runner.md"

PREFIX = "P8_Y5_PARENT_ZMJ_READOUT_TAIL_2640"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "zmj_audit": RESIDUALS / f"{PREFIX}_ZMJ_READOUT_OWNER_AUDIT.csv",
    "join_gate": RESIDUALS / f"{PREFIX}_SINGLE_BRANCH_JOIN_GATE.csv",
    "readout_tail": RESIDUALS / f"{PREFIX}_READOUT_TAIL_OWNER_MATRIX.csv",
    "alpha_refusal": RESIDUALS / f"{PREFIX}_R10_ALPHA_REFUSAL_RUNNER.csv",
    "branch_decision": RESIDUALS / f"{PREFIX}_BRANCH_DECISION.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2640_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2640_00_2639",
        "role": "immediate readout-to-R10 alpha row handoff",
        "path": ROOT / "2639-Y5-R2FR-readout-residual-to-q-loc-response-map-or-R10-Yukawa-source-row.md",
        "needles": ["READOUT_TO_QLOC_R10_BRIDGE_WRITTEN_NOT_CLOSED", "R10R2639_0_readout_alpha_source_row", "VAL2639_OVERALL"],
    },
    {
        "source_id": "SRC2640_01_2639_alpha_csv",
        "role": "machine-readable readout R10 alpha row contract",
        "path": RESIDUALS / "P8_Y5_READOUT_QLOC_R10_BRIDGE_2639_R10_YUKAWA_SOURCE_ROW.csv",
        "needles": ["R10R2639_0_readout_alpha_source_row", "MISSING_LAMBDA_I", "MISSING_J_i_FROM_QLOC_OR_READOUT_RESIDUAL"],
    },
    {
        "source_id": "SRC2640_02_2411",
        "role": "parent Z/M/J owner fork",
        "path": ROOT / "2411-Y5-R2FR-parent-ZM-and-J-current-owner-or-constraint-branch.md",
        "needles": ["NO_FULL_ZMJ_OWNER_SIGNED", "RANK_ZERO_CONSTRAINT_ROUTE_PROMOTED", "VAL2411_OVERALL"],
    },
    {
        "source_id": "SRC2640_03_2410",
        "role": "q_loc source-map contract and alpha refusal",
        "path": ROOT / "2410-Y5-R2FR-R10-q-loc-Yukawa-source-map-or-bound-curve-blocker.md",
        "needles": ["SOURCE_MAP_GATE_TIGHTENED_NO_CLAIM", "SMG2410_1_parent_quadratic_source_action", "VAL2410_OVERALL"],
    },
    {
        "source_id": "SRC2640_04_1036",
        "role": "parent finite-X row and beta source/test split",
        "path": ROOT / "1036-Y5-R10-parent-X-quadratic-action-and-beta-source-test-split.md",
        "needles": ["parent finite-`X` action row is **not owned**", "CGATE1036_0_parent_action_row", "DEC1036_0_parent_row_status"],
    },
    {
        "source_id": "SRC2640_05_1036_template_csv",
        "role": "machine parent finite-X template",
        "path": RESIDUALS / "P8_Y5_R10_1036_PARENT_ACTION_ROW_TEMPLATE.csv",
        "needles": ["PXA1036_0_finite_X_parent_row", "TEMPLATE_ONLY_PARENT_ROW_NOT_OWNED", "MISSING_ABSOLUTE_TAIL_ENVELOPE"],
    },
    {
        "source_id": "SRC2640_06_1037",
        "role": "no physical X pole and bounded beta fallback",
        "path": ROOT / "1037-Y5-R10-no-physical-X-pole-theorem-or-bounded-beta-runner.md",
        "needles": ["FAIL_CURRENT_CLAIM_NO_POLE_NOT_PROVED", "BB1037_7_beta_product_guard", "V1037_3_beta_rows_complete"],
    },
    {
        "source_id": "SRC2640_07_1035",
        "role": "Yukawa kernel/source-test product law",
        "path": ROOT / "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
        "needles": ["KXD1035_1_static_green_function", "BETA1035_0_product_law", "V1035_1_green_kernel_contract"],
    },
    {
        "source_id": "SRC2640_08_2638",
        "role": "readout tail no-cancellation envelope",
        "path": ROOT / "2638-Y5-R2FR-readout-residual-component-zero-or-source-bound-pack.md",
        "needles": ["READOUT_COMPONENT_ZERO_ATTEMPTS_DO_NOT_CLOSE", "RB2638_6_Delta_readout_abs", "VAL2638_OVERALL"],
    },
    {
        "source_id": "SRC2640_09_563",
        "role": "R10 anchor-only external curve blocker",
        "path": ROOT / "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
        "needles": ["B563_0_no_full_bound_curve", "B563_1_no_numeric_MTS_alpha", "V563_10_no_overclaim"],
    },
    {
        "source_id": "SRC2640_10_1034",
        "role": "review candidate alpha_bound curve not promoted",
        "path": ROOT / "1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md",
        "needles": ["REVIEW_CANDIDATE_CURVE_PRESENT_NONCLAIM", "R10P1034_0_alpha_bound_curve", "V1034_2_candidate_file_written"],
    },
]


def ensure_dirs() -> None:
    for directory in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
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


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *[
                "| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |"
                for row in rows
            ],
        ]
    )


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        text = read_text(source["path"])
        exists = source["path"].exists()
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "timestamp_utc": now(),
                "source_id": source["source_id"],
                "role": source["role"],
                "source_path": str(source["path"]),
                "exists": bool_text(exists),
                "needles_present": bool_text(needles_present),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": "False",
            }
        )
    return rows


def zmj_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "ZMJ2640_0_single_parent_branch",
            "object": "single parent finite-range branch",
            "owner_question": "Does one parent branch own Z_i, M_i^2/lambda_i, J_i, beta_s, beta_t and Delta_readout_abs_R10 together?",
            "current_result": "NO_SINGLE_BRANCH_OWNER",
            "evidence": "2411 and 1036 both keep the finite-X/ZMJ row template-only; 2638 keeps readout tail values missing",
            "missing_inputs": "Z_i;M_i_squared;lambda_i;J_i;beta_source_readout;beta_test_readout;Delta_readout_abs_R10;source_paths",
            "passes_now": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "ZMJ2640_1_Z_principal_symbol",
            "object": "Z_i or Z_AB",
            "owner_question": "Is the physical quotient principal symbol source-signed?",
            "current_result": "MISSING_SOURCE_SIGNED_OWNER",
            "evidence": "2411: M_AB candidate exists but Z_AB/principal symbol is not signed",
            "missing_inputs": "principal-symbol extraction from Gamma_eff/Khat/CDB branch; domain; units; rank",
            "passes_now": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "ZMJ2640_2_M_range",
            "object": "M_i^2 and lambda_i",
            "owner_question": "Can the range be predicted from the same branch as Z_i?",
            "current_result": "RELATION_KNOWN_VALUES_MISSING",
            "evidence": "range law lambda_i=sqrt(Z_i/M_i^2) or generalized eigenvalue law is known, but values/eigenvectors are absent",
            "missing_inputs": "M_i_squared; generalized spectrum; same-branch normalization; length units",
            "passes_now": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "ZMJ2640_3_J_current",
            "object": "J_i",
            "owner_question": "Is the Yukawa source current parent-owned and readout-stable?",
            "current_result": "PARTIAL_HILBERT_THEOREM_PLUS_LIVE_RESIDUALS",
            "evidence": "2411 records Hilbert/coframe source ownership as conditional, but non-Hilbert/readout/source-weight tails remain live",
            "missing_inputs": "common matter action; source-blind syntax; non-Hilbert current zeros or bounds; readout stability",
            "passes_now": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "ZMJ2640_4_beta_source_test",
            "object": "beta_source_readout and beta_test_readout",
            "owner_question": "Are source and test legs separately owned?",
            "current_result": "MISSING_BETA_SOURCE_TEST_SPLIT",
            "evidence": "1035/1036/1037 require a source-test product law and reject naked linear coupling",
            "missing_inputs": "beta_source_readout;beta_test_readout;profile/material convention; c_g/c_g^2 declaration",
            "passes_now": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "ZMJ2640_5_readout_tail",
            "object": "Delta_readout_abs_R10",
            "owner_question": "Can readout tail be set to zero or bounded for the R10 lane?",
            "current_result": "SCHEMA_READY_COMPONENT_VALUES_MISSING",
            "evidence": "2638 writes readout tail envelope but all component values/source paths are missing",
            "missing_inputs": "E_readout_total_R10;projector_norm_R10;marker_readout_R10 theorem-zero or numeric source rows",
            "passes_now": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "ZMJ2640_6_external_curve",
            "object": "alpha_bound(lambda)",
            "owner_question": "Is the external R10 bound claim-valid?",
            "current_result": "ANCHOR_OR_REVIEW_CANDIDATE_NONCLAIM",
            "evidence": "563 anchors and 1034 review curve are nonclaim; live DIGITIZED file remains placeholder",
            "missing_inputs": "official table or promoted digitized dense curve with QA and interpolation policy",
            "passes_now": "False",
            "valid_for_claim": "False",
        },
    ]


def join_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "join_id": "JOIN2640_0_parent_row",
            "required_join": "E_X=0;Z_i;M_i^2;lambda_i;J_i;beta_source;beta_test;sign;normalization;Delta_readout_abs_R10",
            "current_status": "MISSING_PARENT_ROW",
            "failure_reason": "no single source path signs all finite-range and readout-tail inputs together",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "join_id": "JOIN2640_1_range_source_pair",
            "required_join": "Z_i/M_i^2 range owner plus J_i source map from same quotient branch",
            "current_status": "Z_OWNER_AND_J_OWNER_NOT_JOINED",
            "failure_reason": "M candidate is not a range; partial Hilbert source theorem is not full source silence",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "join_id": "JOIN2640_2_beta_product",
            "required_join": "beta_source_readout and beta_test_readout separately sourced or theorem-zero",
            "current_status": "MISSING_BETA_SOURCE_TEST_SPLIT",
            "failure_reason": "two-body exchange cannot be scored with one naked coupling",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "join_id": "JOIN2640_3_readout_tail",
            "required_join": "Delta_readout_abs_R10 zero or numeric bounded envelope",
            "current_status": "MISSING_READOUT_COMPONENT_VALUES",
            "failure_reason": "readout residual components were not theorem-zero in 2638",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "join_id": "JOIN2640_4_external_bound",
            "required_join": "promoted alpha_bound(lambda) curve",
            "current_status": "REVIEW_CANDIDATE_NONCLAIM",
            "failure_reason": "anchors/review candidate cannot support claim scoring",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "join_id": "JOIN2640_5_verdict",
            "required_join": "all R10 alpha scoring inputs",
            "current_status": "R10_ALPHA_SCORING_REFUSED",
            "failure_reason": "Z/M/J, beta source/test, readout tail and external curve are not jointly claim-ready",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
    ]


def readout_tail_rows() -> list[dict[str, Any]]:
    return [
        {
            "tail_id": "RT2640_0_E_readout_total_R10",
            "component": "E_readout_total",
            "required_for_zero_or_bound": "S_red/P_read source path or parent proof no S_red branch exists",
            "current_status": "MISSING_SOURCE_PATH_AND_NUMERIC_VALUE",
            "alpha_row_effect": "additive tail in Delta_readout_abs_R10",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "RT2640_1_projector_norm_R10",
            "component": "projector_norm",
            "required_for_zero_or_bound": "physical current complex, projector definition, M_H_ref/tau denominator",
            "current_status": "MISSING_PROJECTOR_NORM_AND_DOMAIN",
            "alpha_row_effect": "projector/source mismatch tail; may overlap with R_eq/I_commutator",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "RT2640_2_marker_readout_R10",
            "component": "marker_readout",
            "required_for_zero_or_bound": "no-marker/no-extension theorem or finite marker coefficients",
            "current_status": "BLOCKED_BY_NO_MARKER_THEOREM_MISSING",
            "alpha_row_effect": "source/test composition tail",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "RT2640_3_readout_abs_R10",
            "component": "Delta_readout_abs_R10",
            "required_for_zero_or_bound": "absolute sum over RT2640_0..2 plus any R10-specific readout/gauge terms",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "alpha_row_effect": "must remain in alpha_predicted until zeroed or bounded",
            "valid_for_claim": "False",
        },
    ]


def alpha_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2640_0_missing_parent_row",
            "attempted_score": "score R10R2639_0 without parent Z/M/J row",
            "verdict": "REFUSED",
            "reason": "lambda, source current and charge normalization are not parent-owned",
            "required_exit": "one parent branch source-signs Z_i, M_i^2/lambda_i, J_i, beta_source and beta_test",
            "runner_must_return": "False",
            "valid_for_claim": "False",
        },
        {
            "refusal_id": "REF2640_1_missing_readout_tail",
            "attempted_score": "drop Delta_readout_abs_R10",
            "verdict": "REFUSED",
            "reason": "readout component zeros failed; the tail is additive in the R10 alpha row",
            "required_exit": "RB2638/RT2640 readout components theorem-zero or numeric sourced",
            "runner_must_return": "False",
            "valid_for_claim": "False",
        },
        {
            "refusal_id": "REF2640_2_missing_bound_curve",
            "attempted_score": "use anchor or review candidate alpha_bound curve",
            "verdict": "REFUSED",
            "reason": "external bound evidence remains nonclaim",
            "required_exit": "promoted dense alpha_bound(lambda) curve with QA/interpolation policy",
            "runner_must_return": "False",
            "valid_for_claim": "False",
        },
        {
            "refusal_id": "REF2640_3_linear_coupling",
            "attempted_score": "linear c_g or unity coupling shortcut",
            "verdict": "REFUSED",
            "reason": "R10 exchange uses source-test product; universal Weyl leg is generally c_g squared",
            "required_exit": "explicit beta_source/beta_test split or sourced packed convention",
            "runner_must_return": "False",
            "valid_for_claim": "False",
        },
        {
            "refusal_id": "REF2640_4_local_GR_claim",
            "attempted_score": "claim local GR/Newton because finite R10 branch is demoted",
            "verdict": "REFUSED",
            "reason": "demotion is not a rank-zero/source-current proof",
            "required_exit": "principal-symbol rank-zero plus J_H/J_NH/boundary source identity",
            "runner_must_return": "False",
            "valid_for_claim": "False",
        },
    ]


def branch_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "BD2640_0_finite_range_readout_R10",
            "status": "DEMOTED_TO_EXPLICIT_NONCLAIM_ACQUISITION",
            "why": "one-branch Z/M/J plus readout-tail owner is absent",
            "next_condition": "source-sign Z/M/J/beta/tail row before any R10 score",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BD2640_1_rank_zero_constraint_GR_route",
            "status": "PROMOTED_AS_BEST_DERIVATION_FORK",
            "why": "if Z_AB is rank-zero/absent on the physical quotient, the cleaner GR route is constraint/source-current silence rather than Yukawa suppression",
            "next_condition": "principal-symbol rank proof plus J_H/J_NH/boundary/readout source identity",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BD2640_2_data_parallel_R10_curve",
            "status": "HELD_PARALLEL_NONCLAIM",
            "why": "external curve work is useful but cannot rescue missing theory coefficients",
            "next_condition": "official/promoted alpha_bound(lambda) curve; still nonclaim until alpha prediction exists",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2640_0_internal",
            "claim": "2640 may guide private Z/M/J/readout-tail routing",
            "status": "ALLOW_INTERNAL_NONCLAIM",
            "passed": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2640_1_parent_ZMJ_readout_owner",
            "claim": "one parent branch owns Z/M/J plus readout tail",
            "status": "BLOCKED",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2640_2_R10_alpha_score",
            "claim": "R10 alpha_readout(lambda) can be scored",
            "status": "BLOCKED_REFUSAL_RUNNER_ACTIVE",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2640_3_rank_zero_GR",
            "claim": "rank-zero/constraint route derives local GR/Newton",
            "status": "BLOCKED_NOT_PROVED",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2640_4_public",
            "claim": "public/GitHub claim is appropriate",
            "status": "BLOCKED_PRIVATE_NONCLAIM",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2640_0_result",
            "decision": "NO_PARENT_ZMJ_READOUT_TAIL_OWNER_FOUND",
            "reason": "current corpus has conditional pieces but no single branch signs Z, M, J, source/test beta and readout tail together",
            "consequence": "R10 alpha scoring remains refused",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2640_1_gain",
            "decision": "READOUT_TAIL_INCLUDED_IN_ZMJ_GATE",
            "reason": "the finite-range branch can no longer ignore readout residuals while chasing Z/M/J coefficients",
            "consequence": "future alpha rows must join theory coefficients and Delta_readout_abs_R10",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2640_2_best_route",
            "decision": "PRINCIPAL_SYMBOL_OR_RANK_ZERO_SOURCE_CURRENT_IDENTITY_NEXT",
            "reason": "2411 already showed M alone is not range; 2640 confirms finite R10 is blocked unless Z/J/tails close",
            "consequence": "next proof target should derive Z_AB rank/principal symbol or reject finite-range branch for rank-zero/source-current closure",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2641-Y5-R2FR-readout-tail-aware-principal-symbol-ZAB-or-rank-zero-source-current-identity.md",
            "script": "scripts/Y5_R2FR_readout_tail_aware_principal_symbol_ZAB_or_rank_zero_source_current_identity_2641.py",
            "objective": "extract the principal symbol of the Gamma_eff/Khat/CDB branch with readout tails included; either source-sign physical Z_AB or prove rank-zero and write the J_H/J_NH/boundary/readout source-current identity contract",
            "include": "2640 Z/M/J/readout join gate; 2411 principal-symbol fork; 1037 no-pole certificate; 2638 readout tail envelope; 2409 Khat/Gamma response defect",
            "exclude": "infer Z from M, ignore readout tails, score R10 alpha, use anchor curves as evidence, claim local GR/Newton, GitHub action",
            "selected": "True",
            "valid_for_claim": "False",
        }
    ]


def branch_copy_pairs() -> list[tuple[str, Path, Path]]:
    return [
        ("COPY2640_zmj", OUTPUTS["zmj_audit"], LOCAL_BOUNDS / "Parent_ZMJ_readout_owner_audit_2640_NONCLAIM.csv"),
        ("COPY2640_join", OUTPUTS["join_gate"], LOCAL_BOUNDS / "Single_branch_ZMJ_readout_join_gate_2640_NONCLAIM.csv"),
        ("COPY2640_tail", OUTPUTS["readout_tail"], LOCAL_BOUNDS / "Readout_tail_owner_matrix_2640_NONCLAIM.csv"),
        ("COPY2640_refusal", OUTPUTS["alpha_refusal"], LOCAL_BOUNDS / "R10_alpha_refusal_runner_2640_NONCLAIM.csv"),
        ("COPY2640_branch", OUTPUTS["branch_decision"], LOCAL_BOUNDS / "ZMJ_readout_branch_decision_2640_NONCLAIM.csv"),
        ("COPY2640_next", OUTPUTS["next_target"], RAB_QUEUE / "JR2640_PRINCIPAL_SYMBOL_RANK_ZERO_READOUT_NEXT.csv"),
    ]


def copy_branch_artifacts() -> None:
    for _, source, target in branch_copy_pairs():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": copy_id,
            "source_path": str(source),
            "copy_path": str(target),
            "source_exists": bool_text(source.exists()),
            "copy_exists": bool_text(target.exists()),
            "valid_for_claim": "False",
        }
        for copy_id, source, target in branch_copy_pairs()
    ]


def formalization_has_2640_outputs() -> bool:
    if not FORMALIZATION.exists():
        return False
    for path in FORMALIZATION.rglob("*2640*"):
        if path.is_file():
            return True
    for path in FORMALIZATION.rglob("*PARENT_ZMJ_READOUT_TAIL_2640*"):
        if path.is_file():
            return True
    return False


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    copy_paths = [target for _, _, target in branch_copy_pairs()]
    checks = [
        (
            "VAL2640_00_sources",
            all(row["exists"] == "True" and row["needles_present"] == "True" for row in generated["source_register"]),
            "all cited source paths exist and required needles are present",
        ),
        (
            "VAL2640_01_zmj_not_owned",
            any(row["current_result"] == "NO_SINGLE_BRANCH_OWNER" for row in generated["zmj_audit"])
            and all(row["passes_now"] == "False" and row["valid_for_claim"] == "False" for row in generated["zmj_audit"]),
            "Z/M/J/readout owner audit stays nonclaim",
        ),
        (
            "VAL2640_02_join_gate_refuses",
            any(row["current_status"] == "R10_ALPHA_SCORING_REFUSED" for row in generated["join_gate"])
            and all(row["score_ready"] == "False" for row in generated["join_gate"]),
            "single-branch join gate refuses scoring",
        ),
        (
            "VAL2640_03_readout_tail_visible",
            any(row["component"] == "Delta_readout_abs_R10" and row["current_status"] == "SCHEMA_READY_VALUES_MISSING" for row in generated["readout_tail"]),
            "readout tail remains visible in the R10 gate",
        ),
        (
            "VAL2640_04_refusal_runner",
            all(row["runner_must_return"] == "False" and row["valid_for_claim"] == "False" for row in generated["alpha_refusal"])
            and any(row["refusal_id"] == "REF2640_1_missing_readout_tail" for row in generated["alpha_refusal"]),
            "alpha refusal runner blocks missing readout tail and shortcuts",
        ),
        (
            "VAL2640_05_branch_decision",
            any(row["branch_id"] == "BD2640_0_finite_range_readout_R10" and row["status"] == "DEMOTED_TO_EXPLICIT_NONCLAIM_ACQUISITION" for row in generated["branch_decision"])
            and any(row["branch_id"] == "BD2640_1_rank_zero_constraint_GR_route" for row in generated["branch_decision"]),
            "finite R10 is demoted and rank-zero route promoted as proof fork",
        ),
        (
            "VAL2640_06_claim_gates",
            all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in generated["claim_gates"]),
            "no claim gate allows R10/local GR/public claim",
        ),
        (
            "VAL2640_07_next_target",
            any(row["selected"] == "True" and row["next_target"].startswith("2641-Y5-R2FR-readout-tail-aware") for row in generated["next_target"]),
            "2641 readout-tail-aware principal-symbol target selected",
        ),
        (
            "VAL2640_08_branch_copies",
            all(path.exists() and csv_parses(path) for path in copy_paths),
            "nonclaim local_bounds copies and acquisition queue exist and parse",
        ),
        (
            "VAL2640_09_csv_parse",
            all(path.exists() and csv_parses(path) for path in output_csvs),
            "all generated 2640 CSVs parse",
        ),
        (
            "VAL2640_10_formalization_untouched",
            not formalization_has_2640_outputs(),
            "no 2640 outputs are written under formalization-workbench",
        ),
        (
            "VAL2640_11_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
    ]
    overall = all(status for _, status, _ in checks)
    rows = [
        {"check_id": check_id, "status": "PASS" if status else "FAIL", "detail": detail, "valid_for_claim": "False"}
        for check_id, status, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2640_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2640 parent Z/M/J owner with readout tail and R10 alpha refusal runner",
            "valid_for_claim": "False",
        }
    )
    return rows


def write_markdown(generated: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]]) -> None:
    lines = [
        "# 2640 - Y5 R2/f(R) Parent Z/M/J Owner With Readout Tail Or R10 Alpha Refusal Runner",
        "",
        "Status: `Y5_R2FR_2640_no_parent_ZMJ_readout_tail_owner_R10_alpha_scoring_refused_rank_zero_route_promoted_nonclaim`",
        "",
        "Claim ceiling: no parent finite-range row, no numeric R10 alpha, no readout-tail zero, no R10/PPN/WEP/clock/orbital pass, no local-GR/Newton proof, no anchor/review-curve scoring, no public/GitHub action, and no `formalization-workbench` edit is made.",
        "",
        "## Summary",
        "",
        "2640 asks the hard join question: does one parent branch own `Z_i`, `M_i^2/lambda_i`, `J_i`, source/test readout charges, and `Delta_readout_abs_R10` together?",
        "",
        "The answer in the current corpus is no. That does not kill the programme, but it kills the temptation to score R10 from a partial alpha row. The finite-range R10 lane remains explicit nonclaim acquisition. The better derivation fork is now principal-symbol/rank-zero source-current identity with readout tails included.",
        "",
        "## Source Register",
        md_table(generated["source_register"]),
        "",
        "## Z/M/J Readout Owner Audit",
        md_table(generated["zmj_audit"]),
        "",
        "## Single-Branch Join Gate",
        md_table(generated["join_gate"]),
        "",
        "## Readout Tail Owner Matrix",
        md_table(generated["readout_tail"]),
        "",
        "## R10 Alpha Refusal Runner",
        md_table(generated["alpha_refusal"]),
        "",
        "## Branch Decision",
        md_table(generated["branch_decision"]),
        "",
        "## Claim Gates",
        md_table(generated["claim_gates"]),
        "",
        "## Decision Ledger",
        md_table(generated["decision"]),
        "",
        "## Next Target",
        md_table(generated["next_target"]),
        "",
        "## Branch Copies",
        md_table(generated["branch_copies"]),
        "",
        "## Validation",
        md_table(validation),
        "",
        "## Plain-English Verdict",
        "",
        "This is the useful kind of grim: the finite-range R10 branch cannot be scored honestly yet, but now we know exactly why. It needs one parent-owned stack, not scattered almost-pieces.",
        "",
        "The stronger path toward GR is the rank/principal-symbol fork. If the physical quotient has no propagating `Z_AB` branch, then the local-GR route may come from constraint/source-current silence rather than fifth-force suppression. That is the next shot worth taking.",
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    generated = {
        "source_register": source_register_rows(),
        "zmj_audit": zmj_audit_rows(),
        "join_gate": join_gate_rows(),
        "readout_tail": readout_tail_rows(),
        "alpha_refusal": alpha_refusal_rows(),
        "branch_decision": branch_decision_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for key, rows in generated.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    generated["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], generated["branch_copies"])
    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(generated, validation)
    print(f"wrote {DOC_PATH}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
