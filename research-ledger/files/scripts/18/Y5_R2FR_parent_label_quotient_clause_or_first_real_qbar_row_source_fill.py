from __future__ import annotations

import csv
import importlib.util
import shutil
import sys
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1686"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1686-Y5-R2FR-parent-label-quotient-clause-or-first-real-qbar-row-source-fill.md"
VALIDATOR_MODULE = ROOT / "scripts" / "qbar_source_weight_intake_validator_1685.py"

SOURCE_FILES = {
    "1685_doc": ROOT / "1685-Y5-R2FR-qbar-source-weight-intake-runner-or-matter-category-connectedness-proof.md",
    "1685_validation": OUT / "P8_Y5_BRR545_1685_VALIDATION.csv",
    "1685_connectedness": OUT / "P8_Y5_PARENT_QLOC_1685_MATTER_CATEGORY_CONNECTEDNESS_PROOF_ATTEMPT.csv",
    "1685_candidate": OUT / "P8_Y5_PARENT_QLOC_1685_QBAR_CANDIDATE_TEMPLATE_NONCLAIM.csv",
    "1685_dry_run": OUT / "P8_Y5_PARENT_QLOC_1685_QBAR_INTAKE_DRY_RUN.csv",
    "1685_gate": OUT / "P8_Y5_PARENT_QLOC_1685_GATE_STATUS.csv",
    "1685_next": OUT / "P8_Y5_PARENT_QLOC_1685_NEXT_TARGET.csv",
    "1685_validator": VALIDATOR_MODULE,
    "1066_doc": ROOT / "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md",
    "1066_source_scalar": OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
    "1066_object_language": OUT / "P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv",
    "1066_operator_domain": OUT / "P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv",
    "1078_doc": ROOT / "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md",
    "1078_object_language": OUT / "P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv",
    "1078_action_measure": OUT / "P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv",
    "1078_current_owner": OUT / "P8_Y5_R10_1078_CURRENT_OWNER_PROOF_ATTEMPT.csv",
    "1078_counterexamples": OUT / "P8_Y5_R10_1078_COUNTEREXAMPLE_KILL_MATRIX.csv",
    "1088_doc": ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
    "1088_signature": OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
    "1088_zero_theorem": OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
    "1088_countermodels": OUT / "P8_Y5_R10_1088_COUNTERMODEL_RETENTION.csv",
    "1090_doc": ROOT / "1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md",
    "1090_synthesis": OUT / "P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv",
    "1090_missing_axioms": OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv",
    "1090_closure": OUT / "P8_Y5_R10_1090_CLOSURE_DEMOTION_REGISTER.csv",
    "1311_audit": OUT / "P8_Y5_R10_1311_COEFFICIENT_SOURCE_AUDIT.csv",
    "1417_acquisition": OUT / "P8_Y5_R10_1417_QBAR_SOURCE_WEIGHT_ACQUISITION_ROWS.csv",
}

NEEDLES = {
    "1685_doc": ["parent-signed quotient", "finite route is now executable", "1686-Y5-R2FR-parent-label-quotient-clause-or-first-real-qbar-row-source-fill.md"],
    "1685_validation": ["VAL1685_OVERALL", "PASS"],
    "1685_connectedness": ["MCC1685_3_parent_quotient", "UNSIGNED"],
    "1685_candidate": ["CAND1685_0_qbar_source_weight_missing_template", "MISSING_SOURCE_WEIGHT_VALUE_OR_BOUND"],
    "1685_dry_run": ["DRY1685_0", "PLACEHOLDER_OR_BLOCKED_FIELDS"],
    "1685_gate": ["GATE_ACTIVE_REJECTS_SOURCE_BRANCH", "qbar_source_weight"],
    "1685_next": ["1686-Y5-R2FR-parent-label-quotient-clause-or-first-real-qbar-row-source-fill.md", "source-label forgetting"],
    "1685_validator": ["def evaluate_qbar_source_weight_row", "REQUIRED_FIELDS"],
    "1066_doc": ["SSE1066_5_verdict", "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED"],
    "1066_source_scalar": ["SSE1066_5_verdict", "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED"],
    "1066_object_language": ["OLT1066_6_verdict", "conditional_not_parent_derived"],
    "1066_operator_domain": ["ODR1066_2_species_component_obstruction", "OBSTRUCTION_SURVIVES"],
    "1078_doc": ["OL1078_4_verdict", "OBJECT_LANGUAGE_NOT_SIGNED"],
    "1078_object_language": ["OL1078_4_verdict", "OBJECT_LANGUAGE_NOT_SIGNED"],
    "1078_action_measure": ["AM1078_4_verdict", "ACTION_MEASURE_NOT_SIGNED"],
    "1078_current_owner": ["CO1078_4_verdict", "CURRENT_OWNER_NOT_SIGNED"],
    "1078_counterexamples": ["CEK1078_0_species_action_weight", "SURVIVES"],
    "1088_doc": ["MOMS1088_7_verdict", "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED"],
    "1088_signature": ["MOMS1088_7_verdict", "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED"],
    "1088_zero_theorem": ["THM1088_6_current_corpus_verdict", "CONDITIONAL_ZERO_THEOREM_NOT_PROMOTED"],
    "1088_countermodels": ["CM1088_0_species_weight", "NOT_KILLED_BY_CURRENT_CORPUS"],
    "1090_doc": ["SYN1090_8_verdict", "SYNTHESIS_FAILS_MISSING_AXIOMS"],
    "1090_synthesis": ["SYN1090_8_verdict", "SYNTHESIS_FAILS_MISSING_AXIOMS"],
    "1090_missing_axioms": ["AX1090_2_common_quantum_measure", "MISSING_AXIOM_NOT_ADOPTED"],
    "1090_closure": ["CLOS1090_0_MOMS", "closure_candidate_not_adopted"],
    "1311_audit": ["QCSA1311_5_qbar_source_weight", "NONE"],
    "1417_acquisition": ["QSA1417_0_qbar_source_weight", "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1686_SOURCE_REGISTER.csv"
PARENT_QUOTIENT_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1686_PARENT_LABEL_QUOTIENT_CLAUSE_AUDIT.csv"
QUOTIENT_FAILURE_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1686_QUOTIENT_FAILURE_LEDGER.csv"
QBAR_FILL_SEARCH = OUT / "P8_Y5_PARENT_QLOC_1686_FIRST_REAL_QBAR_ROW_SOURCE_FILL_SEARCH.csv"
QBAR_CANDIDATE = OUT / "P8_Y5_PARENT_QLOC_1686_QBAR_CANDIDATE_ROW_ATTEMPT_NONCLAIM.csv"
QBAR_VALIDATOR_RESULT = OUT / "P8_Y5_PARENT_QLOC_1686_QBAR_VALIDATOR_RESULT.csv"
GATE_STATUS = OUT / "P8_Y5_PARENT_QLOC_1686_GATE_STATUS.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1686_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1686_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1686_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1686_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    PARENT_QUOTIENT_AUDIT,
    QUOTIENT_FAILURE_LEDGER,
    QBAR_FILL_SEARCH,
    QBAR_CANDIDATE,
    QBAR_VALIDATOR_RESULT,
    GATE_STATUS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    PARENT_QUOTIENT_AUDIT,
    QUOTIENT_FAILURE_LEDGER,
    QBAR_FILL_SEARCH,
    QBAR_CANDIDATE,
    QBAR_VALIDATOR_RESULT,
    GATE_STATUS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    PARENT_QUOTIENT_AUDIT: [
        QUARANTINE / "PARENT_LABEL_QUOTIENT_CLAUSE_AUDIT.csv",
        BRANCH_RESIDUALS / "R2FR_parent_label_quotient_clause_audit_1686.csv",
        QUEUE / "JR1686_PARENT_LABEL_QUOTIENT_CLAUSE_AUDIT.csv",
    ],
    QBAR_FILL_SEARCH: [
        QUARANTINE / "FIRST_REAL_QBAR_ROW_SOURCE_FILL_SEARCH.csv",
        BRANCH_RESIDUALS / "R2FR_first_real_qbar_row_source_fill_search_1686.csv",
        QUEUE / "JR1686_FIRST_REAL_QBAR_ROW_SOURCE_FILL_SEARCH.csv",
    ],
    QBAR_CANDIDATE: [
        QUARANTINE / "QBAR_CANDIDATE_ROW_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_qbar_candidate_row_attempt_nonclaim_1686.csv",
        QUEUE / "JR1686_QBAR_CANDIDATE_ROW_ATTEMPT_NONCLAIM.csv",
    ],
    QBAR_VALIDATOR_RESULT: [
        QUARANTINE / "QBAR_VALIDATOR_RESULT.csv",
        BRANCH_RESIDUALS / "R2FR_qbar_validator_result_1686.csv",
        QUEUE / "JR1686_QBAR_VALIDATOR_RESULT.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1686.csv",
        QUEUE / "JR1686_NEXT_TARGET_NONCLAIM.csv",
    ],
}

SCORE_FLAGS = [
    "proof_signed",
    "source_fill_found",
    "row_pass",
    "gate_pass",
    "accepted_for_scoring",
    "score_ready",
    "valid_prediction_row",
    "valid_for_claim",
    "claim_allowed",
]


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_cell(value: object) -> bool:
    return str(value).strip().lower() == "true"


def blocked_marker(value: object) -> bool:
    text = str(value)
    markers = [
        "MISSING_",
        "NOT_",
        "BLOCKED",
        "REJECT",
        "FAIL",
        "DRY_RUN",
        "UNSIGNED",
        "NONE",
        "NO_VALUE",
        "NO_BOUND",
        "NONCLAIM",
        "SURVIVES",
    ]
    return any(marker in text for marker in markers)


def list_cell(value: object) -> str:
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if isinstance(value, dict):
        return ";".join(f"{key}={item}" for key, item in sorted(value.items()))
    return str(value)


def load_validator() -> ModuleType:
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("qbar_source_weight_intake_validator_1685", VALIDATOR_MODULE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator module: {VALIDATOR_MODULE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_key, source_path in SOURCE_FILES.items():
        exists = source_path.exists()
        body = read_text(source_path) if exists else ""
        needles_present = all(needle in body for needle in NEEDLES[source_key])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": source_key,
                "source_path": str(source_path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": "; ".join(NEEDLES[source_key]),
                "use_in_1686": "parent label quotient proof audit or first real qbar row source fill",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def parent_quotient_audit_rows() -> list[dict[str, object]]:
    rows = [
        (
            "PLQ1686_0_exact_clause",
            "parent label quotient before source coupling",
            "U: C_matter^labelled -> C_matter^source with q_src((T_A,A)) = T_A and F_grav o U = kappa_univ sum_A T_A",
            "EXACT_CLAUSE",
            "would remove the A argument before any kappa_A selector can be formed",
            "1685 names this as the missing parent-signed quotient rather than a derived fact",
            "MCC1685_3_parent_quotient",
        ),
        (
            "PLQ1686_1_object_language",
            "no inert source-only parent argument",
            "Arg(S_parent) excludes w_A, kappa_A, source-only material multipliers, and hidden label markers",
            "CONDITIONAL_ONLY",
            "would make source-only weights syntactically unavailable",
            "1066/1078 show the object language is a contract, not a parent-derived grammar",
            "SSE1066_5_verdict;OL1078_4_verdict",
        ),
        (
            "PLQ1686_2_action_measure",
            "one common action/measure/current normalization owner",
            "S_matter = sum_A S_A with one hbar/measure/current owner; no w_A S_A sectors",
            "UNSIGNED",
            "would kill the main w_A S_A counterexample at the action level",
            "1078/1090 keep action measure and common quantum measure as missing parent signatures",
            "AM1078_4_verdict;AX1090_2_common_quantum_measure",
        ),
        (
            "PLQ1686_3_connectedness",
            "ordinary matter source category has no disconnected source-weight characters",
            "Nat(pi_0(C_ord), R_+) = constant singleton for source-normalization characters",
            "NOT_DERIVED",
            "would prevent independent constants on species/simple-object components",
            "1066/1078 explicitly retain disconnected component counterexamples",
            "ODR1066_2_species_component_obstruction;CEK1078_2_disconnected_material_components",
        ),
        (
            "PLQ1686_4_variation_order",
            "source extraction is before readout/projector fitting",
            "T_total = delta S_parent/delta e_obs before material/source/readout maps; no post-variation F(T_A,A)",
            "CONDITIONAL_ONLY",
            "would stop source labels re-entering after variation",
            "1088 lists this as a conditional subtheorem, not a parent-owned rule",
            "MOMS1088_5_variation_order;CM1088_3_post_variation_selector",
        ),
        (
            "PLQ1686_5_no_shadow_domain",
            "no shadow frame/domain/boundary/source support marker reintroduces labels",
            "ordinary matter uses only observed quotient geometry/gauge data plus fixed representation constants",
            "UNSIGNED",
            "would keep the quotient silent through WEP/R10/Newton/R11/PPN projection",
            "1088/1090 keep no-shadow/readout guards in the missing-signature stack",
            "MOMS1088_6_no_shadow_domain;SYN1090_6_no_shadow_readout",
        ),
        (
            "PLQ1686_6_verdict",
            "parent label quotient signs qbar_source_weight theorem-zero",
            "PLQ1686_0 through PLQ1686_5 all parent-derived in one action",
            "PROOF_NOT_CLOSED",
            "qbar_source_weight = 0 as a derived theorem rather than a closure axiom",
            "the exact contract is known, but current evidence still leaves legal kappa_A T_A and w_A S_A countermodels",
            "SYN1090_8_verdict;MCC1685_5_verdict",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "clause": clause,
            "mathematical_form": mathematical_form,
            "current_result": current_result,
            "if_signed": if_signed,
            "current_gap": current_gap,
            "source_anchor": source_anchor,
            "proof_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, clause, mathematical_form, current_result, if_signed, current_gap, source_anchor in rows
    ]


def quotient_failure_rows() -> list[dict[str, object]]:
    rows = [
        ("QFL1686_0_species_action_weight", "S_matter -> sum_A w_A S_A", "classical EOM can be unchanged while Hilbert source/path-integral weight changes", "requires one common action-measure owner", "CEK1078_0_species_action_weight;AX1090_2_common_quantum_measure"),
        ("QFL1686_1_source_current_rescale", "T_source -> sum_A kappa_A T_A", "local covariance/additivity do not forbid species constants", "requires parent source functor to total Hilbert source before label access", "THM1063_1_additivity;MCC1685_2_naturality"),
        ("QFL1686_2_disconnected_components", "independent constants on disconnected species/source components", "naturality can be componentwise constant, not globally constant", "requires connected/rich ordinary matter category or no external source-label argument", "ODR1066_2_species_component_obstruction;CEK1078_2_disconnected_material_components"),
        ("QFL1686_3_post_variation_selector", "F(T_A,A) after variation/readout", "even a common action can be spoiled by source/readout projection re-entry", "requires variation-before-readout and readout silence signed by parent action", "CM1088_3_post_variation_selector;MCC1685_4_measure_readout"),
        ("QFL1686_4_shadow_domain_marker", "A_A(X)^2 g_obs, B_A(X), source support or boundary/domain marker", "label dependence can hide outside the direct source functor", "requires no-shadow/domain/boundary clause derived, not assumed", "CM1088_2_shadow_frame;CM1088_4_boundary_domain_marker"),
        ("QFL1686_5_verdict", "quotient route obstruction set", "all above countermodels remain legal unless the missing parent owner clauses are signed", "requires common action-measure-current owner plus parent object language", "SYN1090_8_verdict;CLOS1090_0_MOMS"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "failure_id": failure_id,
            "countermodel": countermodel,
            "why_it_survives": why_it_survives,
            "what_would_kill_it": what_would_kill_it,
            "source_anchor": source_anchor,
            "countermodel_survives": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for failure_id, countermodel, why_it_survives, what_would_kill_it, source_anchor in rows
    ]


def qbar_fill_search_rows() -> list[dict[str, object]]:
    rows = [
        ("QFS1686_0_1685_template", "1685 qbar candidate", "P8_Y5_PARENT_QLOC_1685_QBAR_CANDIDATE_TEMPLATE_NONCLAIM.csv", "CAND1685_0_qbar_source_weight_missing_template", "MISSING_SOURCE_WEIGHT_VALUE_OR_BOUND", "no value/bound"),
        ("QFS1686_1_1311_audit", "coefficient audit qbar row", "P8_Y5_R10_1311_COEFFICIENT_SOURCE_AUDIT.csv", "QCSA1311_5_qbar_source_weight", "NONE", "no value/bound/source path"),
        ("QFS1686_2_1417_acquisition", "qbar acquisition row", "P8_Y5_R10_1417_QBAR_SOURCE_WEIGHT_ACQUISITION_ROWS.csv", "QSA1417_0_qbar_source_weight", "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT", "row is a placeholder acquisition target"),
        ("QFS1686_3_1066_delta_w", "source scalar exclusion route", "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_5_verdict", "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED", "theorem route not signed"),
        ("QFS1686_4_1090_moms", "MOMS synthesis route", "P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv", "SYN1090_8_verdict", "SYNTHESIS_FAILS_MISSING_AXIOMS", "closure candidate not derived"),
        ("QFS1686_5_verdict", "first real qbar_source_weight finite row", "local corpus search", "this checkpoint", "NO_VALUE_FOUND", "no sourced numeric value or bound found"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "search_id": search_id,
            "object": obj,
            "source_file": source_file,
            "source_anchor": source_anchor,
            "found_status": found_status,
            "why_not_validator_ready": why_not_validator_ready,
            "source_fill_found": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for search_id, obj, source_file, source_anchor, found_status, why_not_validator_ready in rows
    ]


def qbar_candidate_rows(validator: ModuleType) -> list[dict[str, object]]:
    row = {
        "branch_id": BRANCH_ID,
        "candidate_id": "CAND1686_0_first_real_qbar_row_attempt",
        "basis_component": "qbar_source_weight",
        "coefficient_symbol": "zeta_source_weight_I",
        "accepted_form": "finite envelope sup_{A,B}|partial_{X_I} ln(kappa_A/kappa_B)| or theorem-zero parent label quotient",
        "theorem_route_status": "NOT_PARENT_SIGNED",
        "finite_route_status": "NOT_FILLED",
        "source_label_forgetting_status": "NOT_DERIVED",
        "ordinary_matter_connectedness_status": "NOT_DERIVED",
        "value_or_bound": "MISSING_SOURCE_WEIGHT_VALUE_OR_BOUND",
        "uncertainty": "MISSING_UNCERTAINTY",
        "sign_convention": "MISSING_SIGN_CONVENTION",
        "material_or_source_tags": "MISSING_MATERIAL_OR_SOURCE_TAGS",
        "lambda_or_domain_if_range_dependent": "MISSING_DOMAIN_OR_LAMBDA_DEPENDENCE",
        "parent_basis_X_I": "MISSING_PARENT_BASIS_X_I",
        "normalization": "MISSING_NORMALIZATION",
        "units": "MISSING_UNITS",
        "coordinate_dimension": "MISSING_COORDINATE_DIMENSION",
        "common_mode_measured_G_convention": "MISSING_COMMON_MODE_MEASURED_G_CONVENTION",
        "local_source_path": str(QBAR_FILL_SEARCH),
        "source_anchor": "QFS1686_5_verdict",
        "derivation_or_data_method": "local corpus search found no source-backed value",
        "confidence": "high confidence in absence of current local row; no confidence in coefficient value",
        "extraction_status": "NO_VALUE_FOUND_NONCLAIM",
        "WEP_tau_material_worldtube": "MISSING_WEP_TAU_MATERIAL_WORLDTUBE",
        "R10_lambda_alpha_projection": "MISSING_R10_LAMBDA_ALPHA_PROJECTION",
        "Newton_GM_calibration": "MISSING_NEWTON_GM_CALIBRATION",
        "R11_operator_projection": "MISSING_R11_OPERATOR_PROJECTION",
        "PPN_local_GR_projection": "MISSING_PPN_LOCAL_GR_PROJECTION",
        "accepted_for_scoring": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    return [{field: row.get(field, "") for field in validator.REQUIRED_FIELDS}]


def validator_result_rows(validator: ModuleType, candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for candidate in candidates:
        result = validator.evaluate_qbar_source_weight_row(candidate, root=ROOT)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "result_id": f"QVR1686_{len(rows)}",
                "candidate_id": candidate["candidate_id"],
                "row_pass": result["row_pass"],
                "reason": result["reason"],
                "route": result["route"],
                "route_ok": result["route_ok"],
                "placeholder_fields": list_cell(result["placeholder_fields"]),
                "numeric_failures": list_cell(result["numeric_failures"]),
                "source_path_exists": result["source_path_exists"],
                "resolved_source_path": result["resolved_source_path"],
                "claim_safety_violation": result["claim_safety_violation"],
                "accepted_for_scoring": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": result["valid_for_claim"],
                "claim_allowed": result["claim_allowed"],
            }
        )
    return rows


def gate_status_rows(
    audit_rows: list[dict[str, object]],
    fill_rows: list[dict[str, object]],
    validator_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    quotient_closed = any(row["current_result"] == "PROOF_CLOSED" and bool_cell(row["proof_signed"]) for row in audit_rows)
    source_fill_found = any(bool_cell(row["source_fill_found"]) for row in fill_rows)
    validator_pass = any(bool_cell(row["row_pass"]) for row in validator_rows)
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1686_0_parent_label_quotient",
            "gate": "parent label quotient theorem-zero route",
            "current_status": "PROOF_NOT_CLOSED" if not quotient_closed else "UNEXPECTED_PROOF_CLOSED",
            "gate_pass": False,
            "reason": "object-language, action-measure/current owner, connectedness, variation/readout, and no-shadow clauses are unsigned",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1686_1_first_real_qbar_row",
            "gate": "first real finite qbar_source_weight row",
            "current_status": "NO_SOURCE_FILL_FOUND" if not source_fill_found else "UNEXPECTED_SOURCE_FILL",
            "gate_pass": False,
            "reason": "no sourced numeric value/bound, basis, normalization, units, sign, or arena projections",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1686_2_qbar_validator",
            "gate": "1685 qbar intake validator",
            "current_status": "ACTIVE_REJECTS_1686_CANDIDATE" if not validator_pass else "UNEXPECTED_VALIDATOR_PASS",
            "gate_pass": False,
            "reason": "candidate has missing value/bound, uncertainty, basis, units, and arena projections",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1686_3_source_branch",
            "gate": "local source branch claim gate",
            "current_status": "GATE_ACTIVE_REJECTS_SOURCE_BRANCH",
            "gate_pass": False,
            "reason": "neither theorem-zero nor finite coefficient route is available",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("D1686_0_quotient", "PARENT_LABEL_QUOTIENT_NOT_DERIVED", "the exact quotient clause is known but still needs parent object-language/action-measure/current ownership", "do not set qbar_source_weight=0"),
        ("D1686_1_countermodels", "SOURCE_WEIGHT_COUNTERMODELS_SURVIVE", "w_A S_A, kappa_A T_A, disconnected source characters, and readout selectors remain legal", "attack the owner clauses or keep finite residual"),
        ("D1686_2_fill", "FIRST_REAL_QBAR_ROW_NOT_FOUND", "local sources still contain placeholder rows rather than numeric/bounded qbar values", "no empirical source-side scoring"),
        ("D1686_3_validator", "1685_VALIDATOR_REJECTS_1686_ATTEMPT", "candidate source path exists but value/basis/projection fields are missing", "retain validator as mandatory gate"),
        ("D1686_4_next", "TARGET_COMMON_ACTION_MEASURE_CURRENT_OWNER", "the shortest route to theorem-zero now appears to be one common action-measure/current owner", "move to 1687"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1686_0_parent_label_quotient", "parent label quotient/source-label forgetting theorem", "BLOCKED", "quotient clause remains unsigned"),
        ("CG1686_1_common_measure_owner", "one action-measure/current owner", "BLOCKED", "w_A S_A and current rescaling counterexamples survive"),
        ("CG1686_2_qbar_theorem_zero", "qbar_source_weight theorem-zero", "BLOCKED", "source-label forgetting and connectedness not parent-signed"),
        ("CG1686_3_qbar_finite", "qbar_source_weight finite row", "BLOCKED", "no sourced numeric value/bound row"),
        ("CG1686_4_validator", "qbar validator pass", "BLOCKED", "1686 candidate rejected"),
        ("CG1686_5_local_claim", "local GR/Newton/WEP/R10/PPN source-side claim", "BLOCKED", "neither theorem-zero nor finite coefficient gate passes"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_pass": False,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1687-Y5-R2FR-common-action-measure-current-owner-or-source-weight-bound-acquisition.md",
            "script": "scripts/Y5_R2FR_common_action_measure_current_owner_or_source_weight_bound_acquisition.py",
            "objective": "try to derive the single common action-measure/current owner that kills w_A S_A and kappa_A T_A; if it remains unsigned, acquire a real finite qbar_source_weight bound/value row with the 1685 validator",
            "success_condition": "either one parent owner forbids all relative source weights before variation, or a numeric sourced qbar row passes the validator without placeholder fields",
            "why_next": "1686 shows the label quotient itself reduces to owner clauses, especially action-measure/current ownership",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def validate(
    source_rows: list[dict[str, object]],
    audit_rows: list[dict[str, object]],
    failure_rows: list[dict[str, object]],
    fill_rows: list[dict[str, object]],
    candidate_rows_: list[dict[str, object]],
    validator_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    quotient_not_closed = any(row["audit_id"] == "PLQ1686_6_verdict" and row["current_result"] == "PROOF_NOT_CLOSED" for row in audit_rows) and all(not bool_cell(row["proof_signed"]) for row in audit_rows)
    failures_survive = len(failure_rows) >= 5 and all(bool_cell(row["countermodel_survives"]) for row in failure_rows)
    no_source_fill = any(row["search_id"] == "QFS1686_5_verdict" and row["found_status"] == "NO_VALUE_FOUND" for row in fill_rows) and all(not bool_cell(row["source_fill_found"]) for row in fill_rows)
    candidate_nonclaim = len(candidate_rows_) == 1 and candidate_rows_[0]["candidate_id"] == "CAND1686_0_first_real_qbar_row_attempt" and not bool_cell(candidate_rows_[0]["valid_for_claim"])
    validator_rejects = len(validator_rows) == 1 and not bool_cell(validator_rows[0]["row_pass"]) and "PLACEHOLDER_OR_BLOCKED_FIELDS" in validator_rows[0]["reason"]
    source_path_used = len(validator_rows) == 1 and bool_cell(validator_rows[0]["source_path_exists"])
    gate_locked = all(not bool_cell(row["gate_pass"]) for row in gate_rows) and any(row["current_status"] == "GATE_ACTIVE_REJECTS_SOURCE_BRANCH" for row in gate_rows)
    decision_safe = any(row["decision"] == "TARGET_COMMON_ACTION_MEASURE_CURRENT_OWNER" for row in decisions)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claims)
    next_target_selected = next_rows[0]["next_target"] == "1687-Y5-R2FR-common-action-measure-current-owner-or-source-weight-bound-acquisition.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED)
    branch_copies = all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1686*")) if FORMALIZATION.exists() else True

    no_claim_flags = True
    blocked_not_ready = True
    for generated_path in CLAIM_CHECKED:
        for generated_row in read_csv(generated_path):
            if generated_row.get("valid_for_claim", "False").lower() == "true" or generated_row.get("claim_allowed", "False").lower() == "true":
                no_claim_flags = False
            if any(blocked_marker(value) for value in generated_row.values()):
                for claim_key in SCORE_FLAGS:
                    if claim_key in generated_row and bool_cell(generated_row[claim_key]):
                        blocked_not_ready = False

    checks = [
        ("VAL1686_0_sources_exist", sources_ok, "all cited 1686 source paths exist and required needles are present"),
        ("VAL1686_1_quotient_not_closed", quotient_not_closed, "parent label quotient remains unsigned"),
        ("VAL1686_2_countermodels_survive", failures_survive, "source-weight countermodels remain live"),
        ("VAL1686_3_no_source_fill", no_source_fill, "no real qbar source-weight value/bound row found"),
        ("VAL1686_4_candidate_nonclaim", candidate_nonclaim, "candidate row stays nonclaim"),
        ("VAL1686_5_validator_rejects", validator_rejects, "1685 validator rejects the 1686 candidate"),
        ("VAL1686_6_source_path_used", source_path_used, "candidate points to an existing local search ledger"),
        ("VAL1686_7_gate_locked", gate_locked, "source branch remains locked"),
        ("VAL1686_8_decision_safe", decision_safe, "decision selects common action-measure/current owner as next route"),
        ("VAL1686_9_claim_gate_safe", claim_gate_safe, "all claim gates remain false"),
        ("VAL1686_10_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1686_11_blocked_not_ready", blocked_not_ready, "no blocked/missing row is marked claim/scoring ready"),
        ("VAL1686_12_next_target_selected", next_target_selected, "next target selects owner theorem or source-weight bound acquisition"),
        ("VAL1686_13_csv_parse", csv_parse, "all generated 1686 CSVs parse"),
        ("VAL1686_14_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1686_15_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1686_16_formalization_untouched", formalization_clean, "no 1686 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "check_id": "VAL1686_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1686 parent label quotient clause or first real qbar row source fill validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    table_rows = []
    for row in rows:
        table_rows.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *table_rows])


def write_doc(
    source_rows: list[dict[str, object]],
    audit_rows: list[dict[str, object]],
    failure_rows: list[dict[str, object]],
    fill_rows: list[dict[str, object]],
    candidate_rows_: list[dict[str, object]],
    validator_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1686 - Parent Label Quotient Clause Or First Real Qbar Row Source Fill

**Private status:** qbar/source-weight checkpoint. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, WEP pass, R10 pass, R11 pass, clock pass, orbital pass, or public claim is made.

## Verdict

The parent label-quotient route is now sharply formulated but still not derived. The exact theorem would be: ordinary source labels are forgotten before gravitational coupling, one common action-measure/current owner fixes the Hilbert source normalization, and readout/projection maps cannot recreate source labels. Current files still leave `w_A S_A`, `kappa_A T_A`, disconnected source-character constants, and post-variation selectors alive.

The first real finite `qbar_source_weight` fill also fails honestly. The 1686 candidate points to a real local search ledger, but it still has no numeric value/bound, uncertainty, sign convention, parent basis, units, or WEP/R10/Newton/R11/PPN projections. The 1685 validator correctly rejects it.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1686"])}

## Parent Label Quotient Clause Audit

{markdown_table(audit_rows, ["audit_id", "clause", "mathematical_form", "current_result", "current_gap"])}

## Quotient Failure Ledger

{markdown_table(failure_rows, ["failure_id", "countermodel", "why_it_survives", "what_would_kill_it", "countermodel_survives"])}

## First Real Qbar Row Source Fill Search

{markdown_table(fill_rows, ["search_id", "object", "source_file", "source_anchor", "found_status", "why_not_validator_ready"])}

## Qbar Candidate Attempt

{markdown_table(candidate_rows_, ["candidate_id", "basis_component", "coefficient_symbol", "theorem_route_status", "finite_route_status", "value_or_bound", "local_source_path", "valid_for_claim"])}

## Validator Result

{markdown_table(validator_rows, ["result_id", "candidate_id", "row_pass", "reason", "route", "source_path_exists", "claim_safety_violation"])}

## Gate Status

{markdown_table(gate_rows, ["gate_id", "gate", "current_status", "gate_pass", "reason"])}

## Decisions

{markdown_table(decision_rows_, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "gate", "gate_pass", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

1686 says the next best derivation target is not more broad source-label language. It is the owner theorem underneath it: one common parent action-measure/current normalization. If that can be derived, source weights die by construction. If it cannot, `qbar_source_weight` must become an explicit finite coefficient with a real sourced value or bound before source-side tests can score.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    validator = load_validator()
    source_rows = source_register_rows()
    audit_rows = parent_quotient_audit_rows()
    failure_rows = quotient_failure_rows()
    fill_rows = qbar_fill_search_rows()

    write_csv(SOURCE_REGISTER, source_rows, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1686", "valid_for_claim", "claim_allowed"])
    write_csv(PARENT_QUOTIENT_AUDIT, audit_rows, ["branch_id", "audit_id", "clause", "mathematical_form", "current_result", "if_signed", "current_gap", "source_anchor", "proof_signed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(QUOTIENT_FAILURE_LEDGER, failure_rows, ["branch_id", "failure_id", "countermodel", "why_it_survives", "what_would_kill_it", "source_anchor", "countermodel_survives", "valid_for_claim", "claim_allowed"])
    write_csv(QBAR_FILL_SEARCH, fill_rows, ["branch_id", "search_id", "object", "source_file", "source_anchor", "found_status", "why_not_validator_ready", "source_fill_found", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])

    candidates = qbar_candidate_rows(validator)
    validator_rows = validator_result_rows(validator, candidates)
    gate_rows = gate_status_rows(audit_rows, fill_rows, validator_rows)
    decisions = decision_rows()
    claims = claim_gate_rows()
    next_rows = next_target_rows()

    write_csv(QBAR_CANDIDATE, candidates, list(validator.REQUIRED_FIELDS))
    write_csv(QBAR_VALIDATOR_RESULT, validator_rows, ["branch_id", "result_id", "candidate_id", "row_pass", "reason", "route", "route_ok", "placeholder_fields", "numeric_failures", "source_path_exists", "resolved_source_path", "claim_safety_violation", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(GATE_STATUS, gate_rows, ["branch_id", "gate_id", "gate", "current_status", "gate_pass", "reason", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(DECISION, decisions, ["branch_id", "decision_id", "decision", "reason", "next_action", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claims, ["branch_id", "gate_id", "gate", "gate_pass", "status", "reason", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "next_target", "script", "objective", "success_condition", "why_next", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    validation_rows = validate(source_rows, audit_rows, failure_rows, fill_rows, candidates, validator_rows, gate_rows, decisions, claims, next_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, audit_rows, failure_rows, fill_rows, candidates, validator_rows, gate_rows, decisions, claims, next_rows, validation_rows)

    failed_rows = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAIL {failed_row['check_id']}: {failed_row['detail']}")
        raise SystemExit(1)
    print("1686 validation PASS")


if __name__ == "__main__":
    main()
