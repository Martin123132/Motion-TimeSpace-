from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_PSI_TO_PHIQ_QUOTIENT_OR_QR_STIFFNESS_2270"
DOC = ROOT / "2270-Y5-R2FR-psi-to-Phiq-quotient-map-or-qR-stiffness-source.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2270_00_2269_doc",
        "source_key": "2269_doc",
        "source_path": ROOT / "2269-Y5-R2FR-radial-cell-conservation-theorem-or-qR-stiffness-coefficient.md",
        "needles": ["RCT2269_4_psi_quotient_route", "SCI2269_2_qR", "NEXT2269_0_primary"],
        "role": "handoff: psi quotient or stiffness source selected",
    },
    {
        "source_id": "SRC2270_01_2269_validation",
        "source_key": "2269_validation",
        "source_path": OUT / "P8_Y5_BRR545_2269_VALIDATION.csv",
        "needles": ["VAL2269_OVERALL", "PASS"],
        "role": "confirms 2269 passed before 2270 starts",
    },
    {
        "source_id": "SRC2270_02_2268_split",
        "source_key": "2268_split",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2268_PHI_Q_VARIABLE_SPLIT.csv",
        "needles": ["PQS2268_0_definitions", "PQS2268_2_reduced_branch"],
        "role": "machine-readable Phi/q split",
    },
    {
        "source_id": "SRC2270_03_2269_stiffness",
        "source_key": "2269_stiffness",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2269_QR_STIFFNESS_COEFFICIENT_INTAKE.csv",
        "needles": ["SCI2269_0_MR2", "SCI2269_1_jR", "SCI2269_2_qR"],
        "role": "q_R stiffness coefficient intake",
    },
    {
        "source_id": "SRC2270_04_micro_action",
        "source_key": "micro_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "needles": ["g_{μν} = η_{μν}", "A_MTS[ψ]", "∂²_t ψ"],
        "role": "primitive psi action and emergent covariance metric",
    },
    {
        "source_id": "SRC2270_05_macro_action",
        "source_key": "macro_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md",
        "needles": ["g_{μν}(x)", "⟨ ∂_μ ψ(x) ∂_ν ψ(x) ⟩_{smooth}", "correct Lorentzian signature"],
        "role": "macro statement of psi-gradient smoothing into geometry",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2270_SOURCE_REGISTER.csv",
    "covariance_map": OUT / "P8_Y5_PARENT_QLOC_2270_PSI_COVARIANCE_TO_PHIQ_MAP.csv",
    "quotient_tests": OUT / "P8_Y5_PARENT_QLOC_2270_PSI_QUOTIENT_TESTS.csv",
    "stiffness_source": OUT / "P8_Y5_PARENT_QLOC_2270_STIFFNESS_SOURCE_ATTEMPT.csv",
    "claim_requirements": OUT / "P8_Y5_PARENT_QLOC_2270_CLAIM_REQUIREMENTS.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2270_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2270_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2270_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2270_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2270_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2270_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_map": QUEUE / "JR2270_PSI_TO_PHIQ_MAP_NONCLAIM.csv",
    "queue_stiffness": QUEUE / "JR2270_STIFFNESS_SOURCE_ATTEMPT_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_psi_to_Phiq_or_stiffness_refusal_2270.csv",
    "beta_docs": BETA_DOCS / "RAB_PSI_TO_PHIQ_OR_STIFFNESS_2270_NONCLAIM.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        try:
            return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
        except ValueError:
            return str(path)


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = next((key for key in ("check_id", "validation_id", "id") if key in rows[0]), "")
    result_key = next((key for key in ("result", "status") if key in rows[0]), "")
    if not result_key:
        return False
    overall = [row for row in rows if id_key and "overall" in row.get(id_key, "").lower()]
    return all(row.get(result_key, "").lower() == "pass" for row in (overall or rows))


def source_path(key: str) -> Path:
    return next(source["source_path"] for source in SOURCES if source["source_key"] == key)


def source_refs(*keys: str) -> str:
    return ";".join(rel(source_path(key)) for key in keys)


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": rel(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and all(needle in text for needle in source["needles"]),
                "validation_overall_pass": validation_pass(path) if "validation" in source["source_key"] else "",
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def covariance_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "map_id": "PCM2270_0_covariance_definition",
            "object": "psi covariance metric",
            "formula": "g_munu=eta_munu+C_munu, C_munu=<partial_mu psi partial_nu psi>_smooth",
            "phi_q_projection": "in static radial sector use A=-g_tt, B=g_rr, q=ln(AB), Phi=1/4 ln(A/B)",
            "result": "defines a possible pullback q[psi] once sign/frame/areal conventions are fixed",
            "status": "FORMAL_MAP_SHAPE_AVAILABLE",
            "valid_for_claim": False,
        },
        {
            "map_id": "PCM2270_1_component_projection",
            "object": "linear weak-field q channel",
            "formula": "if g_tt=-1+C_tt and g_rr=1+C_rr, then A=1-C_tt, B=1+C_rr",
            "phi_q_projection": "q=ln[(1-C_tt)(1+C_rr)] = (C_rr-C_tt)+O(C^2)",
            "result": "q is the temporal/radial covariance mismatch at first order",
            "status": "DERIVED_LINEAR_CHANNEL_TEST",
            "valid_for_claim": False,
        },
        {
            "map_id": "PCM2270_2_q_zero_condition",
            "object": "q=0 covariance condition",
            "formula": "(1-C_tt)(1+C_rr)=1, hence C_rr=C_tt/(1-C_tt); linearized condition C_rr=C_tt",
            "phi_q_projection": "reduced local branch demands a parent relation between temporal and radial covariance channels",
            "result": "psi map could derive local reciprocity only if this channel relation is parent-forced",
            "status": "EXACT_CONDITIONAL_RELATION",
            "valid_for_claim": False,
        },
        {
            "map_id": "PCM2270_3_current_corpus",
            "object": "current psi action evidence",
            "formula": "A_MTS[psi] supplies scalar dynamics and a covariance metric ansatz",
            "phi_q_projection": "no source line fixes C_rr=C_tt, q in ker(Dq), or a stiffness Hessian in q",
            "result": "q is not shown absent, vertical, or minimized by the current psi map",
            "status": "PSI_TO_PHIQ_QUOTIENT_NOT_DERIVED_CURRENT_CORPUS",
            "valid_for_claim": False,
        },
    ]


def quotient_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "PQT2270_0_absent_q",
            "test": "Does the psi covariance map land only in Phi, with q absent?",
            "required_evidence": "explicit map C_munu[psi] satisfying (1-C_tt)(1+C_rr)=1 identically",
            "current_evidence": "metric covariance ansatz has independent temporal and radial channels",
            "result": "FAIL_CURRENT_CLAIM",
            "valid_for_claim": False,
        },
        {
            "test_id": "PQT2270_1_vertical_q",
            "test": "Is q quotient-vertical/gauge under a parent map?",
            "required_evidence": "a quotient q_parent with Dq killing q variations and matter/readout descent",
            "current_evidence": "no quotient map or matter descent for q exists in current action files",
            "result": "MISSING_QUOTIENT_MAP",
            "valid_for_claim": False,
        },
        {
            "test_id": "PQT2270_2_stiff_q",
            "test": "Does the psi action generate a positive algebraic stiffness in q?",
            "required_evidence": "second variation along q gives M_R^2>0 and first source leg gives j_R",
            "current_evidence": "psi action has kinetic/potential terms but no pullback Hessian to q",
            "result": "MISSING_STIFFNESS_PULLBACK",
            "valid_for_claim": False,
        },
        {
            "test_id": "PQT2270_3_source_q",
            "test": "Does matter/readout source q with known j_R?",
            "required_evidence": "delta S_matter/delta q or readout functor source coefficient in same normalization",
            "current_evidence": "no q-specific source coefficient in current corpus",
            "result": "MISSING_SOURCE_COEFFICIENT",
            "valid_for_claim": False,
        },
        {
            "test_id": "PQT2270_4_verdict",
            "test": "Can psi-to-(Phi,q) map promote reduced local GR?",
            "required_evidence": "PQT2270_0 or PQT2270_1 closes; otherwise PQT2270_2 and PQT2270_3 source finite q_R",
            "current_evidence": "none closed",
            "result": "PSI_QUOTIENT_NOT_CLOSED_STIFFNESS_NOT_SOURCED",
            "valid_for_claim": False,
        },
    ]


def stiffness_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": "SSA2270_0_MR2_pullback",
            "target": "M_R^2",
            "candidate_formula": "M_R^2 := second variation of parent action along q at local vacuum, normalized to L_q=-1/2 M_R^2 q^2",
            "source_attempt": "pull back A_MTS[psi] through psi -> C_munu -> q",
            "current_status": "MISSING_PSI_TO_Q_PULLBACK",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "source_id": "SSA2270_1_jR_source",
            "target": "j_R",
            "candidate_formula": "J_R=j_R L+O(L^2), J_R := source/readout variation in q direction",
            "source_attempt": "extract from matter/readout coupling after Phi/q split",
            "current_status": "MISSING_MATTER_Q_SOURCE_MAP",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "source_id": "SSA2270_2_qR_ratio",
            "target": "q_R",
            "candidate_formula": "q_R=j_R/M_R^2",
            "source_attempt": "requires SSA2270_0 and SSA2270_1 with compatible units",
            "current_status": "MISSING_RATIO_INPUTS",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "source_id": "SSA2270_3_no_gradient_guard",
            "target": "Q_R",
            "candidate_formula": "Q_R=0 for algebraic q only if no nabla q term or boundary q momentum is generated",
            "source_attempt": "operator inventory of psi pullback and boundary variation",
            "current_status": "MISSING_OPERATOR_BOUNDARY_INVENTORY",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def claim_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "REQ2270_0_sign_frame",
            "claim_path": "psi-to-Phiq map",
            "must_have": "declare sign/frame/areal conventions turning g_tt,g_rr into A,B",
            "current_status": "PARTIAL_FORMAL_ONLY",
            "valid_for_claim": False,
        },
        {
            "requirement_id": "REQ2270_1_channel_relation",
            "claim_path": "reduced local branch",
            "must_have": "parent proof of C_rr=C_tt/(1-C_tt) or q absent/vertical",
            "current_status": "MISSING",
            "valid_for_claim": False,
        },
        {
            "requirement_id": "REQ2270_2_matter_descent",
            "claim_path": "quotient branch",
            "must_have": "matter/readout cannot observe or source q",
            "current_status": "MISSING",
            "valid_for_claim": False,
        },
        {
            "requirement_id": "REQ2270_3_stiffness",
            "claim_path": "finite q_R branch",
            "must_have": "M_R^2, j_R, no-gradient guard, units, source paths",
            "current_status": "MISSING",
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2270_0_q_absent",
            "attempted_claim": "psi covariance map makes q absent",
            "runner_result": "BLOCKED",
            "blocked_by": "PQT2270_0_absent_q=FAIL_CURRENT_CLAIM",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2270_1_q_vertical",
            "attempted_claim": "q is quotient-vertical/gauge",
            "runner_result": "BLOCKED",
            "blocked_by": "PQT2270_1_vertical_q=MISSING_QUOTIENT_MAP",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2270_2_qR_score",
            "attempted_claim": "finite q_R can be scored",
            "runner_result": "BLOCKED",
            "blocked_by": "M_R^2, j_R, and no-gradient guard missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2270_3_local_GR",
            "attempted_claim": "derived local GR/Newton/PPN from psi map",
            "runner_result": "BLOCKED",
            "blocked_by": "psi quotient not closed and stiffness not sourced",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2270_0_linear_channel_test",
            "claim": "q linear channel identified",
            "gate_pass": False,
            "reason": "math test is identified but not a physics claim",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2270_1_psi_quotient",
            "claim": "psi map removes q",
            "gate_pass": False,
            "reason": "C_rr/C_tt relation or quotient map missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2270_2_stiffness",
            "claim": "q stiffness/source coefficients sourced",
            "gate_pass": False,
            "reason": "M_R^2 and j_R missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2270_3_local_GR",
            "claim": "derived local GR/Newton branch",
            "gate_pass": False,
            "reason": "not achieved",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2270_0_map_gain",
            "decision": "Q_CHANNEL_IDENTIFIED_AS_COVARIANCE_MISMATCH",
            "reason": "linearized q is C_rr-C_tt in the psi covariance radial sector",
            "next_action": "future proof must derive the temporal/radial covariance relation, not merely assert AB=1",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2270_1_quotient",
            "decision": "PSI_QUOTIENT_NOT_CLOSED",
            "reason": "current psi action states emergent covariance but lacks the determinant/radial-cell quotient map",
            "next_action": "do not claim q absent or vertical",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2270_2_fallback",
            "decision": "FINITE_STIFFNESS_NOT_SOURCED",
            "reason": "no pullback Hessian M_R^2 or q-source coefficient j_R exists yet",
            "next_action": "write the parent pullback contract or source q_R numerically later",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2270_3_next",
            "decision": "PARENT_PULLBACK_CONTRACT_NEXT",
            "reason": "the next honest step is a contract for pulling A_MTS[psi] into the Phi/q variables and identifying the q Hessian/source leg",
            "next_action": "2271-Y5-R2FR-parent-psi-action-Phiq-pullback-contract-or-qR-numeric-backstop.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2270_0_primary",
            "next_target": "2271-Y5-R2FR-parent-psi-action-Phiq-pullback-contract-or-qR-numeric-backstop.md",
            "script": "scripts/Y5_R2FR_parent_psi_action_Phiq_pullback_contract_or_qR_numeric_backstop_2271.py",
            "objective": "write the explicit contract for pulling A_MTS[psi] through psi -> C_munu -> (Phi,q), extracting either q absence/verticality or finite M_R^2 and j_R inputs",
            "selection_status": "selected",
            "success_condition": "the pullback makes q absent/vertical, or supplies source-backed M_R^2 and j_R rows for nonclaim q_R scoring",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2270_map",
            "source_path": rel(OUTPUTS["covariance_map"]),
            "target_path": rel(COPY_TARGETS["queue_map"]),
            "target_exists": COPY_TARGETS["queue_map"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_map"]),
            "reason": "psi-to-Phi/q map attempt copied as nonclaim queue",
        },
        {
            "copy_id": "BC2270_stiffness",
            "source_path": rel(OUTPUTS["stiffness_source"]),
            "target_path": rel(COPY_TARGETS["queue_stiffness"]),
            "target_exists": COPY_TARGETS["queue_stiffness"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_stiffness"]),
            "reason": "stiffness source attempt copied as nonclaim queue",
        },
        {
            "copy_id": "BC2270_branch_wep",
            "source_path": rel(OUTPUTS["claim_gates"]),
            "target_path": rel(COPY_TARGETS["branch_wep"]),
            "target_exists": COPY_TARGETS["branch_wep"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["branch_wep"]),
            "reason": "branch-locked WEP/local refusal gates",
        },
        {
            "copy_id": "BC2270_beta_docs",
            "source_path": rel(OUTPUTS["decision"]),
            "target_path": rel(COPY_TARGETS["beta_docs"]),
            "target_exists": COPY_TARGETS["beta_docs"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["beta_docs"]),
            "reason": "portable psi-map decision ledger",
        },
    ]


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def validation_rows() -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    mapping = read_csv(OUTPUTS["covariance_map"])
    tests = read_csv(OUTPUTS["quotient_tests"])
    stiffness = read_csv(OUTPUTS["stiffness_source"])
    requirements = read_csv(OUTPUTS["claim_requirements"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    next_rows = read_csv(OUTPUTS["next_target"])
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("VAL2270_0_sources_exist", all(row["exists"].lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL2270_1_needles_present", all(row["needles_present"].lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL2270_2_prior_validation",
            any(row["source_key"] == "2269_validation" and row["validation_overall_pass"].lower() == "true" for row in source_rows),
            "2269 validation passes",
        ),
        (
            "VAL2270_3_linear_channel_test",
            any(row["map_id"] == "PCM2270_1_component_projection" and row["status"] == "DERIVED_LINEAR_CHANNEL_TEST" for row in mapping),
            "linear q covariance channel test written",
        ),
        (
            "VAL2270_4_quotient_not_claimed",
            any(row["test_id"] == "PQT2270_4_verdict" and row["result"] == "PSI_QUOTIENT_NOT_CLOSED_STIFFNESS_NOT_SOURCED" for row in tests)
            and all(row["valid_for_claim"].lower() == "false" for row in tests),
            "psi quotient is not falsely claimed",
        ),
        (
            "VAL2270_5_stiffness_nonclaim",
            all(row["score_ready"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in stiffness),
            "stiffness source rows remain nonclaim",
        ),
        (
            "VAL2270_6_requirements_written",
            len(requirements) >= 4 and all(row["valid_for_claim"].lower() == "false" for row in requirements),
            "claim requirements written and blocked",
        ),
        (
            "VAL2270_7_refusal_blocks",
            all(row["score_eligible"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in refusal),
            "refusal runner blocks local claims",
        ),
        (
            "VAL2270_8_claim_gates_blocked",
            all(row["gate_pass"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in claims),
            "claim gates are all blocked",
        ),
        (
            "VAL2270_9_next_selected",
            any(row["route_id"] == "NEXT2270_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "2271 target selected",
        ),
        ("VAL2270_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 2270 CSVs parse"),
        (
            "VAL2270_11_no_claim_flags",
            not any(
                row.get(key, "").lower() == "true"
                for path in generated_csvs
                for row in read_csv(path)
                for key in ("score_ready", "accepted_ready", "valid_for_claim", "claim_allowed", "gate_pass")
            ),
            "no generated score/claim/gate flags are true",
        ),
        (
            "VAL2270_12_branch_copies",
            all(row["target_exists"].lower() == "true" and row["target_parses"].lower() == "true" for row in read_csv(OUTPUTS["branch_copies"])),
            "branch/queue copies exist and parse",
        ),
        ("VAL2270_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        (
            "VAL2270_14_formalization_no_2270",
            not any(
                path.is_file()
                and (path.name.startswith("2270-") or (path.name.startswith("P8_Y5") and "2270" in path.name))
                for path in FORMALIZATION.rglob("*")
            ),
            "formalization-workbench has no 2270 output files",
        ),
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2270_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2270 identifies q as temporal/radial covariance mismatch, blocks psi quotient claim, keeps stiffness nonclaim, and selects 2271",
        }
    )
    return rows


def write_doc() -> None:
    source_rows = read_csv(OUTPUTS["source_register"])
    mapping = read_csv(OUTPUTS["covariance_map"])
    tests = read_csv(OUTPUTS["quotient_tests"])
    stiffness = read_csv(OUTPUTS["stiffness_source"])
    requirements = read_csv(OUTPUTS["claim_requirements"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    decisions = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])
    copies = read_csv(OUTPUTS["branch_copies"])
    validation = read_csv(OUTPUTS["validation"])
    sections = [
        "# 2270 - Y5/R2FR psi-to-Phi/q Quotient Map Or q_R Stiffness Source",
        "",
        "## Verdict",
        "",
        "2270 makes the primitive-map obstruction concrete. With `g_munu=eta_munu+C_munu`, `C_munu=<partial_mu psi partial_nu psi>_smooth`, and the static radial convention `A=-g_tt`, `B=g_rr`, the reciprocal strain is `q=ln[(1-C_tt)(1+C_rr)]`. Linearized, `q=C_rr-C_tt+O(C^2)`. So `q` is the mismatch between radial and temporal covariance channels.",
        "",
        "That gives a clear proof target: MTS must derive the covariance-channel relation `(1-C_tt)(1+C_rr)=1`, or show `q` is quotient-vertical/absent, or source a finite stiffness/source pair. The current corpus does not yet do that. The psi action gives a covariance metric ansatz and scalar dynamics, but no determinant/radial-cell quotient theorem, no `M_R^2` Hessian in `q`, and no `j_R` source leg.",
        "",
        "So local GR is not derived here, but the target is sharper than before: prove the channel relation, or treat `q_R=j_R/M_R^2` as a finite residual. No local-GR/Newton, PPN, R10, WEP, clock, orbital, `R_AB=0`, `Q_R=0`, or finite residual pass claim is made.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"], source_rows),
        "",
        "## psi Covariance to Phi/q Map",
        table(["map_id", "object", "formula", "phi_q_projection", "result", "status", "valid_for_claim"], mapping),
        "",
        "## psi Quotient Tests",
        table(["test_id", "test", "required_evidence", "current_evidence", "result", "valid_for_claim"], tests),
        "",
        "## Stiffness Source Attempt",
        table(["source_id", "target", "candidate_formula", "source_attempt", "current_status", "score_ready", "valid_for_claim"], stiffness),
        "",
        "## Claim Requirements",
        table(["requirement_id", "claim_path", "must_have", "current_status", "valid_for_claim"], requirements),
        "",
        "## Refusal Runner",
        table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusal),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], claims),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions),
        "",
        "## Next Target",
        table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition"], next_rows),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], copies),
        "",
        "## Validation",
        table(["check_id", "result", "detail"], validation),
        "",
        "## Working Interpretation",
        "",
        "The local problem now has a very useful diagnostic: `q` is not mystical. At first order it is `C_rr-C_tt`. If the theory wants derived local GR, it must explain why those covariance channels are tied together in local vacuum. If it cannot, then `q` is a physical residual and must be carried into tests with sourced `M_R^2` and `j_R` rather than hidden by closure language.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["covariance_map"], covariance_map_rows())
    write_csv(OUTPUTS["quotient_tests"], quotient_test_rows())
    write_csv(OUTPUTS["stiffness_source"], stiffness_source_rows())
    write_csv(OUTPUTS["claim_requirements"], claim_requirement_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["covariance_map"], COPY_TARGETS["queue_map"])
    shutil.copyfile(OUTPUTS["stiffness_source"], COPY_TARGETS["queue_stiffness"])
    shutil.copyfile(OUTPUTS["claim_gates"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["decision"], COPY_TARGETS["beta_docs"])
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows())

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
