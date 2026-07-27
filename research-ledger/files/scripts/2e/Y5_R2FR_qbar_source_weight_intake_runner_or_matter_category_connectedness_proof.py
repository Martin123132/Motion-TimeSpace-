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
QUARANTINE = MICROSCOPE / "quarantine" / "1685"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1685-Y5-R2FR-qbar-source-weight-intake-runner-or-matter-category-connectedness-proof.md"
VALIDATOR_MODULE = ROOT / "scripts" / "qbar_source_weight_intake_validator_1685.py"

SOURCE_FILES = {
    "1684_doc": ROOT / "1684-Y5-R2FR-qbar-source-weight-value-hunt-or-source-label-forgetting-proof.md",
    "1684_validation": OUT / "P8_Y5_BRR545_1684_VALIDATION.csv",
    "1684_forgetting": OUT / "P8_Y5_PARENT_QLOC_1684_SOURCE_LABEL_FORGETTING_PROOF_ATTEMPT.csv",
    "1684_intake": OUT / "P8_Y5_PARENT_QLOC_1684_QBAR_SOURCE_WEIGHT_FINITE_INTAKE_SCHEMA_NONCLAIM.csv",
    "1684_arena": OUT / "P8_Y5_PARENT_QLOC_1684_QBAR_SOURCE_WEIGHT_ARENA_HOOKS_NONCLAIM.csv",
    "1684_gate": OUT / "P8_Y5_PARENT_QLOC_1684_GATE_STATUS.csv",
    "1684_next": OUT / "P8_Y5_PARENT_QLOC_1684_NEXT_TARGET.csv",
    "1682_gate_module": ROOT / "scripts" / "Rsource_runner_gate_1682.py",
    "1063_forgetting": OUT / "P8_Y5_R10_1063_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv",
    "1231_stack": OUT / "P8_Y5_R10_1231_SOURCE_LABEL_FORGETTING_PROOF_STACK.csv",
    "950_source_norm": OUT / "P8_Y5_R10_950_SOURCE_NORMALIZATION_LEMMA_ATTEMPT.csv",
    "1098_owner": OUT / "P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
    "1309_counter": OUT / "P8_Y5_R10_1309_QC_COUNTEREXAMPLE_LEDGER.csv",
    "1417_acquisition": OUT / "P8_Y5_R10_1417_QBAR_SOURCE_WEIGHT_ACQUISITION_ROWS.csv",
    "1418_arena": OUT / "P8_Y5_R10_1418_QBAR_SOURCE_WEIGHT_ARENA_ACQUISITION_LEDGER.csv",
}

NEEDLES = {
    "1684_doc": ["qbar_source_weight", "strict finite intake schema", "1685-Y5-R2FR-qbar-source-weight-intake-runner-or-matter-category-connectedness-proof.md"],
    "1684_validation": ["VAL1684_OVERALL", "PASS"],
    "1684_forgetting": ["SLF1684_3_connected_category", "NOT_DERIVED"],
    "1684_intake": ["INT1684_0_qbar_source_weight", "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT"],
    "1684_arena": ["HOOK1684_0_WEP", "BLOCKED_BY_QBAR_AND_WEP_PROJECTION"],
    "1684_gate": ["GATE_ACTIVE_REJECTS_CURRENT_BRANCH", "qbar_source_weight"],
    "1684_next": ["1685-Y5-R2FR-qbar-source-weight-intake-runner-or-matter-category-connectedness-proof.md", "executable row validator"],
    "1682_gate_module": ["def require_source_branch_gate", "SOURCE_BRANCH_GATE_REJECTED"],
    "1063_forgetting": ["THM1063_5_verdict", "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED"],
    "1231_stack": ["SFL1231_2_connected_components", "NOT_DERIVED"],
    "950_source_norm": ["SNL950_4_countermodel", "species-weighted source current"],
    "1098_owner": ["OCS1098_4_source_weight_exclusion", "UNSIGNED"],
    "1309_counter": ["QCE1309_3_source_weight", "qbar_source_weight"],
    "1417_acquisition": ["QSA1417_0_qbar_source_weight", "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT"],
    "1418_arena": ["QAA1418_6_verdict", "QBAR_ARENA_LEDGER_SOURCE_READY_BUT_UNSCORED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1685_SOURCE_REGISTER.csv"
CONNECTEDNESS_PROOF = OUT / "P8_Y5_PARENT_QLOC_1685_MATTER_CATEGORY_CONNECTEDNESS_PROOF_ATTEMPT.csv"
VALIDATOR_RULES = OUT / "P8_Y5_PARENT_QLOC_1685_QBAR_INTAKE_VALIDATOR_RULES.csv"
CANDIDATE_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1685_QBAR_CANDIDATE_TEMPLATE_NONCLAIM.csv"
DRY_RUN = OUT / "P8_Y5_PARENT_QLOC_1685_QBAR_INTAKE_DRY_RUN.csv"
GATE_STATUS = OUT / "P8_Y5_PARENT_QLOC_1685_GATE_STATUS.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1685_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1685_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1685_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1685_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    CONNECTEDNESS_PROOF,
    VALIDATOR_RULES,
    CANDIDATE_TEMPLATE,
    DRY_RUN,
    GATE_STATUS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    CONNECTEDNESS_PROOF,
    VALIDATOR_RULES,
    CANDIDATE_TEMPLATE,
    DRY_RUN,
    GATE_STATUS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    CONNECTEDNESS_PROOF: [
        QUARANTINE / "MATTER_CATEGORY_CONNECTEDNESS_PROOF_ATTEMPT.csv",
        BRANCH_RESIDUALS / "R2FR_matter_category_connectedness_proof_attempt_1685.csv",
        QUEUE / "JR1685_MATTER_CATEGORY_CONNECTEDNESS_PROOF_ATTEMPT.csv",
    ],
    VALIDATOR_RULES: [
        QUARANTINE / "QBAR_INTAKE_VALIDATOR_RULES.csv",
        BRANCH_RESIDUALS / "R2FR_qbar_intake_validator_rules_1685.csv",
        QUEUE / "JR1685_QBAR_INTAKE_VALIDATOR_RULES.csv",
    ],
    CANDIDATE_TEMPLATE: [
        QUARANTINE / "QBAR_CANDIDATE_TEMPLATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_qbar_candidate_template_nonclaim_1685.csv",
        QUEUE / "JR1685_QBAR_CANDIDATE_TEMPLATE_NONCLAIM.csv",
    ],
    DRY_RUN: [
        QUARANTINE / "QBAR_INTAKE_DRY_RUN.csv",
        BRANCH_RESIDUALS / "R2FR_qbar_intake_dry_run_1685.csv",
        QUEUE / "JR1685_QBAR_INTAKE_DRY_RUN.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1685.csv",
        QUEUE / "JR1685_NEXT_TARGET_NONCLAIM.csv",
    ],
}

SCORE_FLAGS = [
    "proof_signed",
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
    markers = ["MISSING_", "NOT_", "BLOCKED", "REJECT", "FAIL", "DRY_RUN", "UNSIGNED", "NONE", "NO_VALUE", "NO_BOUND", "NONCLAIM"]
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
                "use_in_1685": "qbar intake validator and matter-category connectedness proof attempt",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def connectedness_proof_rows() -> list[dict[str, object]]:
    rows = [
        (
            "MCC1685_0_target",
            "ordinary-matter source category connectedness",
            "pi_0(C_ord/source-label-forgetting) = * and q_src((T_A,A)) = T_A before gravitational coupling",
            "TARGET_EXACT",
            "would make species/source-only weights impossible rather than merely bounded",
            "the parent action has not signed the quotient map that removes A before variation/readout",
            "SFL1231_2_connected_components;SLF1684_3_connected_category",
        ),
        (
            "MCC1685_1_morphisms",
            "interactions and field redefinitions connect all ordinary source sectors",
            "for every A,B there is a source-preserving morphism path A -> B with no extra weight character",
            "NOT_DERIVED",
            "would collapse independent kappa_A/kappa_B constants",
            "disconnected charge/species sectors can still carry a legal character chi_c",
            "SNL950_4_countermodel;OBS1054_3_source_labels",
        ),
        (
            "MCC1685_2_naturality",
            "local covariance/additivity/naturality are enough to force a single source weight",
            "F((T_A,A)) is natural and additive",
            "INSUFFICIENT",
            "would give source universality without new data",
            "F((T_A,A)) = sum_A kappa_A T_A is still local, additive, and covariant",
            "THM1063_1_additivity;SFL1231_1_additive_natural_source",
        ),
        (
            "MCC1685_3_parent_quotient",
            "parent quotient forgets source labels before gravity reads the source",
            "S_parent = S_grav[g, q_src(T_total)] + sum_A S_A with no qbar slot",
            "UNSIGNED",
            "would parent-sign source-label forgetting",
            "the corpus still permits source-only prefactors inside S_A or the readout map",
            "OCS1098_4_source_weight_exclusion;QCE1309_3_source_weight",
        ),
        (
            "MCC1685_4_measure_readout",
            "measure/coframe/readout kernels cannot reintroduce source labels",
            "K_readout o q_src has no material/source tag argument",
            "UNSIGNED",
            "would preserve the quotient through WEP/R10/Newton/R11/PPN projections",
            "projection kernels can still hold source tags unless explicitly signed silent",
            "QAA1418_6_verdict;HOOK1684_0_WEP",
        ),
        (
            "MCC1685_5_verdict",
            "qbar_source_weight theorem-zero from connectedness/source-label forgetting",
            "MCC1685_0 through MCC1685_4 all parent-signed",
            "PROOF_NOT_CLOSED",
            "qbar_source_weight = 0 as a derivation",
            "connectedness and quotient clauses remain exact targets, not proven facts",
            "this checkpoint",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "proof_id": proof_id,
            "claim": claim,
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
        for proof_id, claim, mathematical_form, current_result, if_signed, current_gap, source_anchor in rows
    ]


def validator_rule_rows(validator: ModuleType) -> list[dict[str, object]]:
    field_groups = [
        ("VR1685_0_identity", "identity", ", ".join(validator.IDENTITY_FIELDS), "branch/basis/coefficient must match qbar_source_weight/zeta_source_weight_I"),
        ("VR1685_1_route", "route", ", ".join(validator.ROUTE_FIELDS), "either theorem zero is parent-signed or finite value/bound is sourced"),
        ("VR1685_2_value", "value", ", ".join(validator.VALUE_FIELDS), "numeric value_or_bound and uncertainty with sign/domain/source tags"),
        ("VR1685_3_basis", "basis", ", ".join(validator.BASIS_FIELDS), "parent basis, normalization, units, dimension, and measured-G convention are explicit"),
        ("VR1685_4_source", "source", ", ".join(validator.SOURCE_FIELDS), "local source path exists and source anchor/method/confidence/status are non-placeholder"),
        ("VR1685_5_projection", "projection", ", ".join(validator.PROJECTION_FIELDS), "WEP/R10/Newton/R11/PPN projections are explicit"),
        ("VR1685_6_claim_flags", "claim_flags", ", ".join(validator.CLAIM_FIELDS), "all claim flags true only after every core field passes"),
        ("VR1685_7_placeholders", "placeholder_filter", ", ".join(validator.PLACEHOLDER_MARKERS), "any missing/blocked/unsigned/nonclaim placeholder rejects the row"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "rule_id": rule_id,
            "field_group": field_group,
            "fields_or_markers": fields_or_markers,
            "pass_condition": pass_condition,
            "implemented_in": str(VALIDATOR_MODULE),
            "current_result": "RULE_ACTIVE",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rule_id, field_group, fields_or_markers, pass_condition in field_groups
    ]


def candidate_template_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "candidate_id": "CAND1685_0_qbar_source_weight_missing_template",
            "basis_component": "qbar_source_weight",
            "coefficient_symbol": "zeta_source_weight_I",
            "accepted_form": "theorem_zero_source_label_forgetting OR finite envelope sup_{A,B}|partial_{X_I} ln(kappa_A/kappa_B)|",
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
            "local_source_path": "MISSING_LOCAL_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "derivation_or_data_method": "MISSING_DERIVATION_OR_DATA_METHOD",
            "confidence": "MISSING_CONFIDENCE",
            "extraction_status": "MISSING_EXTRACTION_STATUS",
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
    ]


def dry_run_rows(validator: ModuleType, candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for candidate in candidates:
        result = validator.evaluate_qbar_source_weight_row(candidate, root=ROOT)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "dry_run_id": f"DRY1685_{len(rows)}",
                "candidate_id": candidate["candidate_id"],
                "row_pass": result["row_pass"],
                "reason": result["reason"],
                "route": result["route"],
                "route_ok": result["route_ok"],
                "missing_fields": list_cell(result["missing_fields"]),
                "placeholder_fields": list_cell(result["placeholder_fields"]),
                "identity_failures": list_cell(result["identity_failures"]),
                "numeric_failures": list_cell(result["numeric_failures"]),
                "source_path_exists": result["source_path_exists"],
                "resolved_source_path": result["resolved_source_path"],
                "claim_flags": list_cell(result["claim_flags"]),
                "claim_safety_violation": result["claim_safety_violation"],
                "accepted_for_scoring": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": result["valid_for_claim"],
                "claim_allowed": result["claim_allowed"],
            }
        )
    return rows


def gate_status_rows(dry_rows: list[dict[str, object]], proof_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    qbar_rejected = all(not bool_cell(row["row_pass"]) for row in dry_rows)
    proof_closed = any(row["current_result"] == "PROOF_CLOSED" and bool_cell(row["proof_signed"]) for row in proof_rows)
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1685_0_qbar_validator",
            "gate": "qbar source-weight finite/theorem-zero intake row",
            "current_status": "ACTIVE_REJECTS_TEMPLATE" if qbar_rejected else "UNEXPECTED_PASS",
            "gate_pass": False,
            "reason": "template has missing value, basis, source path, projection fields, and no parent-signed theorem route",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1685_1_connectedness_route",
            "gate": "ordinary matter category connectedness/source-label forgetting theorem",
            "current_status": "PROOF_NOT_CLOSED" if not proof_closed else "UNEXPECTED_PROOF_CLOSED",
            "gate_pass": False,
            "reason": "connectedness and label quotient clauses remain unsigned",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1685_2_1682_source_branch",
            "gate": "1682 imported source branch gate",
            "current_status": "GATE_ACTIVE_REJECTS_SOURCE_BRANCH",
            "gate_pass": False,
            "reason": "qbar_source_weight still has no theorem-zero proof or finite sourced row",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("D1685_0_proof", "CONNECTEDNESS_PROOF_NOT_CLOSED", "ordinary-matter connectedness is the right theorem route but not parent-signed", "do not set qbar_source_weight=0"),
        ("D1685_1_validator", "QBAR_INTAKE_VALIDATOR_BUILT", "1684 finite intake schema is now executable and importable", "use validator before any WEP/R10/Newton/R11/PPN source-side scoring"),
        ("D1685_2_template", "CURRENT_QBAR_TEMPLATE_REJECTED", "candidate has missing value, basis, source path, projection fields, and blocked theorem route", "keep all claim flags false"),
        ("D1685_3_gate", "SOURCE_BRANCH_GATE_REMAINS_LOCKED", "neither theorem-zero nor finite row exists", "no local-GR/Newton/R10/WEP claim"),
        ("D1685_4_next", "HUNT_PARENT_LABEL_QUOTIENT_OR_FIRST_REAL_QBAR_ROW", "next route must either sign the parent quotient or fill the first real finite row", "move to 1686"),
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
        ("CG1685_0_connectedness", "ordinary matter connectedness/source-label forgetting theorem", "BLOCKED", "parent quotient and connectedness clauses unsigned"),
        ("CG1685_1_qbar_zero", "qbar_source_weight theorem-zero", "BLOCKED", "no parent-signed NoSourceOnlySpeciesSlot theorem"),
        ("CG1685_2_qbar_finite", "qbar_source_weight finite coefficient row", "BLOCKED", "no sourced value/bound/source path/basis/projections"),
        ("CG1685_3_validator_pass", "qbar intake validator pass", "BLOCKED", "dry-run template rejected"),
        ("CG1685_4_source_gate", "1682 source branch gate pass", "BLOCKED", "qbar obstruction remains open"),
        ("CG1685_5_local_GR", "local GR/Newton/PPN source-side reduction", "BLOCKED", "source side still not derived or bounded"),
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
            "next_target": "1686-Y5-R2FR-parent-label-quotient-clause-or-first-real-qbar-row-source-fill.md",
            "script": "scripts/Y5_R2FR_parent_label_quotient_clause_or_first_real_qbar_row_source_fill.py",
            "objective": "try one more parent-derivation route for the label quotient/source connectedness clause; if it remains unsigned, use the 1685 validator to acquire or reject the first real qbar_source_weight finite row",
            "success_condition": "either source-label forgetting is parent-signed and qbar_source_weight becomes theorem-zero, or a numeric sourced finite row passes the 1685 validator without placeholder fields",
            "why_next": "1685 turns the finite path into executable discipline and identifies the remaining proof route precisely",
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
    validator: ModuleType,
    source_rows: list[dict[str, object]],
    proof_rows: list[dict[str, object]],
    rule_rows: list[dict[str, object]],
    candidate_rows_: list[dict[str, object]],
    dry_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    connectedness_not_closed = any(row["proof_id"] == "MCC1685_5_verdict" and row["current_result"] == "PROOF_NOT_CLOSED" for row in proof_rows) and all(not bool_cell(row["proof_signed"]) for row in proof_rows)
    validator_module_ok = VALIDATOR_MODULE.exists() and hasattr(validator, "evaluate_qbar_source_weight_row") and hasattr(validator, "require_qbar_source_weight_row")
    required_fields_covered = set(validator.REQUIRED_FIELDS).issubset(set().union(*[set(row["fields_or_markers"].split(", ")) for row in rule_rows if row["field_group"] != "placeholder_filter"]))
    candidate_exact = len(candidate_rows_) == 1 and candidate_rows_[0]["basis_component"] == "qbar_source_weight" and "MISSING_" in ";".join(str(value) for value in candidate_rows_[0].values())
    dry_run_rejects = len(dry_rows) == 1 and not bool_cell(dry_rows[0]["row_pass"]) and "PLACEHOLDER_OR_BLOCKED_FIELDS" in dry_rows[0]["reason"]
    claim_safety = len(dry_rows) == 1 and not bool_cell(dry_rows[0]["claim_safety_violation"])
    gate_locked = all(not bool_cell(row["gate_pass"]) for row in gate_rows) and any(row["current_status"] == "GATE_ACTIVE_REJECTS_SOURCE_BRANCH" for row in gate_rows)
    decision_safe = any(row["decision"] == "QBAR_INTAKE_VALIDATOR_BUILT" for row in decisions)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claims)
    next_target_selected = next_rows[0]["next_target"] == "1686-Y5-R2FR-parent-label-quotient-clause-or-first-real-qbar-row-source-fill.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED)
    branch_copies = all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1685*")) if FORMALIZATION.exists() else True

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
        ("VAL1685_0_sources_exist", sources_ok, "all cited 1685 source paths exist and required needles are present"),
        ("VAL1685_1_connectedness_not_closed", connectedness_not_closed, "matter-category connectedness/source-label forgetting remains unsigned"),
        ("VAL1685_2_validator_module_ok", validator_module_ok, "qbar intake validator module exposes evaluate and require functions"),
        ("VAL1685_3_required_fields_covered", required_fields_covered, "validator rules cover every required intake field"),
        ("VAL1685_4_candidate_template_missing", candidate_exact, "candidate template is exactly qbar_source_weight and remains missing-field nonclaim"),
        ("VAL1685_5_dry_run_rejects", dry_run_rejects, "validator rejects the current qbar template"),
        ("VAL1685_6_claim_safety", claim_safety, "rejected dry-run row has no unsafe true claim flags"),
        ("VAL1685_7_gate_locked", gate_locked, "source gates remain locked"),
        ("VAL1685_8_decision_safe", decision_safe, "decision records validator built but nonclaim"),
        ("VAL1685_9_claim_gate_safe", claim_gate_safe, "all claim gates remain false"),
        ("VAL1685_10_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1685_11_blocked_not_ready", blocked_not_ready, "no blocked/missing row is marked claim/scoring ready"),
        ("VAL1685_12_next_target_selected", next_target_selected, "next target selects parent label quotient or first real qbar row"),
        ("VAL1685_13_csv_parse", csv_parse, "all generated 1685 CSVs parse"),
        ("VAL1685_14_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1685_15_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1685_16_formalization_untouched", formalization_clean, "no 1685 outputs found under formalization-workbench"),
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
            "check_id": "VAL1685_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1685 qbar intake runner or matter-category connectedness proof validation",
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
    proof_rows: list[dict[str, object]],
    rule_rows: list[dict[str, object]],
    candidate_rows_: list[dict[str, object]],
    dry_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1685 - Qbar Source-Weight Intake Runner Or Matter-Category Connectedness Proof

**Private status:** qbar/source-weight checkpoint. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, WEP pass, R10 pass, R11 pass, clock pass, orbital pass, or public claim is made.

## Verdict

The connectedness route remains the clean derivation target, but it still does not close. Additivity, locality, Hilbert-source language, and covariance do not by themselves forbid `sum_A kappa_A T_A`; the missing move is a parent-signed quotient that forgets source labels before gravitational coupling and prevents readout/projection re-entry.

The finite route is now executable. `scripts/qbar_source_weight_intake_validator_1685.py` rejects the current `qbar_source_weight` template because the value/bound, uncertainty, sign convention, parent basis, units, local source path, and WEP/R10/Newton/R11/PPN projections are still missing. This is good discipline rather than bad news: the gap is now a locked intake gate, not a vague hand-wave.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1685"])}

## Matter-Category Connectedness Proof Attempt

{markdown_table(proof_rows, ["proof_id", "claim", "mathematical_form", "current_result", "current_gap"])}

## Qbar Intake Validator Rules

{markdown_table(rule_rows, ["rule_id", "field_group", "fields_or_markers", "pass_condition", "current_result"])}

## Candidate Template

{markdown_table(candidate_rows_, ["candidate_id", "basis_component", "coefficient_symbol", "theorem_route_status", "finite_route_status", "value_or_bound", "parent_basis_X_I", "local_source_path", "valid_for_claim"])}

## Dry Run

{markdown_table(dry_rows, ["dry_run_id", "candidate_id", "row_pass", "reason", "route", "source_path_exists", "claim_safety_violation"])}

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

1685 does not make the source branch pass, but it gives us a proper lock. The next derivation attempt should attack the parent label-quotient clause directly; if that still fails, the finite route must produce a real `zeta_source_weight_I` row that passes the validator before any empirical source-side scoring is allowed.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    validator = load_validator()
    source_rows = source_register_rows()
    proof_rows = connectedness_proof_rows()
    rule_rows = validator_rule_rows(validator)
    candidates = candidate_template_rows()
    dry_rows = dry_run_rows(validator, candidates)
    gate_rows = gate_status_rows(dry_rows, proof_rows)
    decisions = decision_rows()
    claims = claim_gate_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, source_rows, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1685", "valid_for_claim", "claim_allowed"])
    write_csv(CONNECTEDNESS_PROOF, proof_rows, ["branch_id", "proof_id", "claim", "mathematical_form", "current_result", "if_signed", "current_gap", "source_anchor", "proof_signed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(VALIDATOR_RULES, rule_rows, ["branch_id", "rule_id", "field_group", "fields_or_markers", "pass_condition", "implemented_in", "current_result", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    candidate_fieldnames = list(validator.REQUIRED_FIELDS)
    write_csv(CANDIDATE_TEMPLATE, candidates, candidate_fieldnames)
    write_csv(DRY_RUN, dry_rows, ["branch_id", "dry_run_id", "candidate_id", "row_pass", "reason", "route", "route_ok", "missing_fields", "placeholder_fields", "identity_failures", "numeric_failures", "source_path_exists", "resolved_source_path", "claim_flags", "claim_safety_violation", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(GATE_STATUS, gate_rows, ["branch_id", "gate_id", "gate", "current_status", "gate_pass", "reason", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(DECISION, decisions, ["branch_id", "decision_id", "decision", "reason", "next_action", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claims, ["branch_id", "gate_id", "gate", "gate_pass", "status", "reason", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "next_target", "script", "objective", "success_condition", "why_next", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    validation_rows = validate(validator, source_rows, proof_rows, rule_rows, candidates, dry_rows, gate_rows, decisions, claims, next_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, proof_rows, rule_rows, candidates, dry_rows, gate_rows, decisions, claims, next_rows, validation_rows)

    failed_rows = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAIL {failed_row['check_id']}: {failed_row['detail']}")
        raise SystemExit(1)
    print("1685 validation PASS")


if __name__ == "__main__":
    main()
