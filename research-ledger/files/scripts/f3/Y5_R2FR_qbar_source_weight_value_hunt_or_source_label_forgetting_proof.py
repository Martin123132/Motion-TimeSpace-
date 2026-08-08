from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1684"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1684-Y5-R2FR-qbar-source-weight-value-hunt-or-source-label-forgetting-proof.md"

SOURCE_FILES = {
    "1683_doc": ROOT / "1683-Y5-R2FR-first-Rsource-coefficient-fill-or-source-current-owner-derivation.md",
    "1683_validation": OUT / "P8_Y5_BRR545_1683_VALIDATION.csv",
    "1683_fill": OUT / "P8_Y5_PARENT_QLOC_1683_QBAR_SOURCE_WEIGHT_FILL_ATTEMPT_NONCLAIM.csv",
    "1683_acquisition": OUT / "P8_Y5_PARENT_QLOC_1683_QBAR_SOURCE_WEIGHT_ACQUISITION_LEDGER.csv",
    "1682_gate_module": ROOT / "scripts" / "Rsource_runner_gate_1682.py",
    "1063_forgetting": OUT / "P8_Y5_R10_1063_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv",
    "1063_owner": OUT / "P8_Y5_R10_1063_NOETHER_SOURCE_OWNER_AUDIT.csv",
    "1054_clause": OUT / "P8_Y5_R10_1054_ZERO_THEOREM_CLAUSE_AUDIT.csv",
    "1054_counter": OUT / "P8_Y5_R10_1054_COUNTEREXAMPLE_OBSTRUCTION_LEDGER.csv",
    "1055_counter": OUT / "P8_Y5_R10_1055_COUNTEREXAMPLE_LEDGER.csv",
    "1231_stack": OUT / "P8_Y5_R10_1231_SOURCE_LABEL_FORGETTING_PROOF_STACK.csv",
    "950_source_norm": OUT / "P8_Y5_R10_950_SOURCE_NORMALIZATION_LEMMA_ATTEMPT.csv",
    "1046_split": OUT / "P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv",
    "1098_owner": OUT / "P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
    "1309_counter": OUT / "P8_Y5_R10_1309_QC_COUNTEREXAMPLE_LEDGER.csv",
    "1311_audit": OUT / "P8_Y5_R10_1311_COEFFICIENT_SOURCE_AUDIT.csv",
    "1417_acquisition": OUT / "P8_Y5_R10_1417_QBAR_SOURCE_WEIGHT_ACQUISITION_ROWS.csv",
    "1418_arena": OUT / "P8_Y5_R10_1418_QBAR_SOURCE_WEIGHT_ARENA_ACQUISITION_LEDGER.csv",
}

NEEDLES = {
    "1683_doc": ["first finite `R_source` coefficient target", "qbar_source_weight"],
    "1683_validation": ["VAL1683_OVERALL", "PASS"],
    "1683_fill": ["FILL1683_0_qbar_source_weight", "FILL_FAILED_VALUE_AND_ZERO_THEOREM_MISSING"],
    "1683_acquisition": ["ACQ1683_1_value", "MISSING_COEFFICIENT_VALUE"],
    "1682_gate_module": ["def require_source_branch_gate", "SOURCE_BRANCH_GATE_REJECTED"],
    "1063_forgetting": ["THM1063_5_verdict", "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED"],
    "1063_owner": ["NO1063_0_source_functor_domain", "label_forgetting_not_parent_signed"],
    "1054_clause": ["ZC1054_5_source_label_forgetting", "CONDITIONAL_PROOF_NOT_PARENT_DERIVATION"],
    "1054_counter": ["OBS1054_3_source_labels", "kappa_A T_A"],
    "1055_counter": ["CE1055_3_relative_source_weight", "kappa_A T_A"],
    "1231_stack": ["SFL1231_4_verdict", "NOT_CLOSED"],
    "950_source_norm": ["SNL950_4_countermodel", "species-weighted source current"],
    "1046_split": ["CMA1046_4_source_only_weights", "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED"],
    "1098_owner": ["OCS1098_4_source_weight_exclusion", "UNSIGNED"],
    "1309_counter": ["QCE1309_3_source_weight", "qbar_source_weight"],
    "1311_audit": ["QCSA1311_5_qbar_source_weight", "NONE"],
    "1417_acquisition": ["QSA1417_0_qbar_source_weight", "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT"],
    "1418_arena": ["QAA1418_6_verdict", "QBAR_ARENA_LEDGER_SOURCE_READY_BUT_UNSCORED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1684_SOURCE_REGISTER.csv"
FORGETTING_PROOF = OUT / "P8_Y5_PARENT_QLOC_1684_SOURCE_LABEL_FORGETTING_PROOF_ATTEMPT.csv"
VALUE_HUNT = OUT / "P8_Y5_PARENT_QLOC_1684_QBAR_SOURCE_WEIGHT_VALUE_HUNT.csv"
FINITE_INTAKE = OUT / "P8_Y5_PARENT_QLOC_1684_QBAR_SOURCE_WEIGHT_FINITE_INTAKE_SCHEMA_NONCLAIM.csv"
ARENA_HOOKS = OUT / "P8_Y5_PARENT_QLOC_1684_QBAR_SOURCE_WEIGHT_ARENA_HOOKS_NONCLAIM.csv"
GATE_STATUS = OUT / "P8_Y5_PARENT_QLOC_1684_GATE_STATUS.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1684_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1684_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1684_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1684_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    FORGETTING_PROOF,
    VALUE_HUNT,
    FINITE_INTAKE,
    ARENA_HOOKS,
    GATE_STATUS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    FORGETTING_PROOF,
    VALUE_HUNT,
    FINITE_INTAKE,
    ARENA_HOOKS,
    GATE_STATUS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    FORGETTING_PROOF: [
        QUARANTINE / "SOURCE_LABEL_FORGETTING_PROOF_ATTEMPT.csv",
        BRANCH_RESIDUALS / "R2FR_source_label_forgetting_proof_attempt_1684.csv",
        QUEUE / "JR1684_SOURCE_LABEL_FORGETTING_PROOF_ATTEMPT.csv",
    ],
    FINITE_INTAKE: [
        QUARANTINE / "QBAR_SOURCE_WEIGHT_FINITE_INTAKE_SCHEMA_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_qbar_source_weight_finite_intake_schema_nonclaim_1684.csv",
        QUEUE / "JR1684_QBAR_SOURCE_WEIGHT_FINITE_INTAKE_SCHEMA_NONCLAIM.csv",
    ],
    ARENA_HOOKS: [
        QUARANTINE / "QBAR_SOURCE_WEIGHT_ARENA_HOOKS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_qbar_source_weight_arena_hooks_nonclaim_1684.csv",
        QUEUE / "JR1684_QBAR_SOURCE_WEIGHT_ARENA_HOOKS_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1684.csv",
        QUEUE / "JR1684_NEXT_TARGET_NONCLAIM.csv",
    ],
}

EXPECTED_ARENAS = {"WEP", "R10", "NEWTON_GM", "R11", "PPN_LOCAL_GR"}
SCORE_FLAGS = [
    "proof_signed",
    "coefficient_filled",
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
    markers = ["MISSING_", "NOT_", "BLOCKED", "REJECT", "FAIL", "DRY_RUN", "CONDITIONAL", "UNSIGNED", "NONE", "NOT_CLOSED", "NO_PASS"]
    return any(marker in text for marker in markers)


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
                "use_in_1684": "qbar source-weight value hunt or source-label forgetting proof",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def forgetting_proof_rows() -> list[dict[str, object]]:
    rows = [
        (
            "SLF1684_0_target",
            "source functor forgets species labels before gravitational coupling selection",
            "q_src({(T_A,A)}) = sum_A T_A, not {(T_A,A)} -> sum_A kappa_A T_A",
            "TARGET_EXACT",
            "would make qbar_source_weight syntactically impossible",
            "parent category still exposes labels unless a deeper quotient forgets them",
            "THM1063_0_target;SFL1231_0_label_quotient",
        ),
        (
            "SLF1684_1_additivity",
            "local covariance and additivity",
            "F_src(T+U)=F_src(T)+F_src(U)",
            "INSUFFICIENT_ALONE",
            "removes nonlinear source mixing",
            "F((T_A,A))=kappa_A T_A remains additive and covariant",
            "THM1063_1_additivity;SFL1231_1_additive_natural_source",
        ),
        (
            "SLF1684_2_same_action",
            "same action supplies equations and Hilbert source",
            "T_A=2/sqrt(-g) delta S_A/delta g_obs",
            "STRONG_CONDITIONAL_LEMMA",
            "rules out a separate arbitrary source functional",
            "constant relative prefactors w_A inside S_A survive unless action-density owner is signed",
            "THM1063_2_same_action_Hilbert_source;CON1604_0_action_density_owner",
        ),
        (
            "SLF1684_3_connected_category",
            "ordinary matter category is connected for source normalization",
            "pi_0(C_ord)=* for the source-density functor",
            "NOT_DERIVED",
            "would forbid independent source constants per disconnected species component",
            "each connected component can carry a finite delta w_c",
            "SFL1231_2_connected_components",
        ),
        (
            "SLF1684_4_measure_readout",
            "measure, boundary, and readout maps preserve label forgetting",
            "K_readout o q_src has no A argument except through T_A",
            "UNSIGNED",
            "would transfer bare source-label forgetting to observed WEP/R10/Newton/R11 rows",
            "tau/readout kernels can recreate effective source labels",
            "SFL1231_3_measure_readout_no_reentry;ZC1054_6_radiative_readout_closure",
        ),
        (
            "SLF1684_5_verdict",
            "source-label forgetting / NoSourceOnlySpeciesSlot theorem",
            "SLF1684_0 through SLF1684_4 parent-signed",
            "PROOF_NOT_CLOSED",
            "qbar_source_weight would be theorem-zero",
            "relative source-weight counterexamples remain legal",
            "THM1063_5_verdict;SFL1231_4_verdict;OBS1054_3_source_labels",
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


def value_hunt_rows() -> list[dict[str, object]]:
    rows = [
        (
            "VH1684_0_local_source_audit",
            "qbar_source_weight",
            "P8_Y5_R10_1311_COEFFICIENT_SOURCE_AUDIT.csv",
            "QCSA1311_5_qbar_source_weight",
            "NONE",
            "NONE",
            "source-weight exclusion is unsigned and no kappa_A/w_A coefficient is sourced",
        ),
        (
            "VH1684_1_countermodel",
            "species/source-weight counterexample",
            "P8_Y5_R10_950_SOURCE_NORMALIZATION_LEMMA_ATTEMPT.csv",
            "SNL950_4_countermodel",
            "species-weighted source current",
            "not a value",
            "countermodel proves the coefficient class is legal if the parent proof is missing",
        ),
        (
            "VH1684_2_owner_signature",
            "source weight exclusion clause",
            "P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
            "OCS1098_4_source_weight_exclusion",
            "UNSIGNED",
            "not a value",
            "owner clause would help but is not parent-signed",
        ),
        (
            "VH1684_3_acquisition_rows",
            "qbar source acquisition row",
            "P8_Y5_R10_1417_QBAR_SOURCE_WEIGHT_ACQUISITION_ROWS.csv",
            "QSA1417_0_qbar_source_weight",
            "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT",
            "not a value",
            "template row is precise but not source-backed",
        ),
        (
            "VH1684_4_verdict",
            "source-backed finite kappa_A/w_A coefficient",
            "local corpus search",
            "this checkpoint",
            "NO_VALUE_FOUND",
            "NO_BOUND_FOUND",
            "finite coefficient must be acquired from a new parent derivation or explicit finite residual source",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "hunt_id": hunt_id,
            "object": obj,
            "source_file": source_file,
            "source_anchor": source_anchor,
            "found_value": found_value,
            "found_bound_or_threshold": found_bound,
            "why_not_scoreable": why_not_scoreable,
            "coefficient_filled": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for hunt_id, obj, source_file, source_anchor, found_value, found_bound, why_not_scoreable in rows
    ]


def finite_intake_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "intake_id": "INT1684_0_qbar_source_weight",
            "basis_component": "qbar_source_weight",
            "coefficient_symbol": "zeta_source_weight_I",
            "accepted_forms": "theorem_zero_source_label_forgetting OR finite envelope sup_{A,B}|partial_{X_I} ln(kappa_A/kappa_B)|",
            "required_value_fields": "value_or_bound; uncertainty; sign_convention; material_or_source_tags; lambda_or_domain_if_range_dependent",
            "required_basis_fields": "parent_basis_X_I; normalization; units; coordinate dimension; common-mode measured-G convention",
            "required_source_fields": "local_source_path; source_anchor; derivation_or_data_method; confidence; extraction_status",
            "required_projection_fields": "WEP_tau_material_worldtube; R10_lambda_alpha_projection; Newton_GM_calibration; R11_operator_projection",
            "current_value": "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT",
            "current_basis": "MISSING_PARENT_COUPLING_BASIS",
            "current_source_path": "MISSING_VALUE_SOURCE_PATH",
            "current_projection": "MISSING_WEP_R10_NEWTON_R11_PROJECTION",
            "intake_status": "SCHEMA_READY_VALUES_MISSING_NONCLAIM",
            "coefficient_filled": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def arena_hook_rows() -> list[dict[str, object]]:
    rows = [
        ("HOOK1684_0_WEP", "WEP", "eta_source_AB envelope from zeta_source_weight_I times tau_WEP/material/source contrast", "needs MICROSCOPE arrays, material tensor, source worldtube, product convention", "BLOCKED_BY_QBAR_AND_WEP_PROJECTION"),
        ("HOOK1684_1_R10", "R10", "alpha_source_weight(lambda) from zeta_source_weight_I, source/test map, mediator range, and alpha bound curve", "needs lambda owner, source/test charges, Pi_M projection, full bound curve", "BLOCKED_BY_QBAR_AND_R10_PROJECTION"),
        ("HOOK1684_2_Newton", "NEWTON_GM", "Delta(GM)/GM source-normalization residual", "needs measured-G convention, Gauss/orbital calibration, common-mode split", "BLOCKED_BY_QBAR_AND_GM_CALIBRATION"),
        ("HOOK1684_3_R11", "R11", "source-normalization operator coefficient projection", "needs R11 operator/source basis and projection coefficients", "BLOCKED_BY_QBAR_AND_R11_OPERATOR_BASIS"),
        ("HOOK1684_4_PPN", "PPN_LOCAL_GR", "weak-field metric/source residual contribution to gamma,beta,alpha_i,xi and local GR reduction", "needs parent weak-field equations and source-current owner or finite residual vector", "BLOCKED_BY_QBAR_AND_GEOMETRIC_LEFT_HAND"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "hook_id": hook_id,
            "arena": arena,
            "projection_hook": projection_hook,
            "additional_requirements": additional_requirements,
            "current_status": current_status,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for hook_id, arena, projection_hook, additional_requirements, current_status in rows
    ]


def gate_status_rows() -> list[dict[str, object]]:
    rows = read_csv(SOURCE_FILES["1683_acquisition"])
    gate_row = next(row for row in rows if row["acquisition_id"] == "ACQ1683_5_gate")
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1684_0_1682_import_gate",
            "gate_module": str(SOURCE_FILES["1682_gate_module"]),
            "prior_status": gate_row["current_status"],
            "current_status": "GATE_ACTIVE_REJECTS_CURRENT_BRANCH",
            "gate_pass": False,
            "reason": "qbar_source_weight has no theorem-zero or finite value row",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("D1684_0_proof", "SOURCE_LABEL_FORGETTING_NOT_PROVED", "additivity/Hilbert/Ward ingredients are insufficient while labels remain available", "do not set qbar_source_weight=0"),
        ("D1684_1_value", "NO_QBAR_SOURCE_WEIGHT_VALUE_FOUND", "local corpus has no coefficient value, bound, basis, sign, or source path", "use finite intake schema"),
        ("D1684_2_schema", "QBAR_SOURCE_WEIGHT_INTAKE_SCHEMA_READY", "exact required fields for theorem-zero or finite coefficient are now stated", "next work can fill or reject row explicitly"),
        ("D1684_3_gate", "SOURCE_GATE_REMAINS_LOCKED", "1682 gate still rejects source-side arenas", "no WEP/R10/Newton/R11 scoring"),
        ("D1684_4_next", "BUILD_QBAR_INTAKE_RUNNER_OR_PROVE_CONNECTEDNESS", "deep proof blocker is source-label connectedness; finite path needs an intake runner", "move to 1685"),
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
        ("CG1684_0_source_label_forgetting", "source-label forgetting theorem", "BLOCKED", "ordinary matter labels/connectedness not parent-forgotten"),
        ("CG1684_1_qbar_zero", "qbar_source_weight theorem-zero", "BLOCKED", "NoSourceOnlySpeciesSlot not parent-derived"),
        ("CG1684_2_qbar_value", "qbar_source_weight finite coefficient", "BLOCKED", "no value/bound/source path/basis/projection"),
        ("CG1684_3_gate", "1682 source branch gate pass", "BLOCKED", "gate remains active and rejects current branch"),
        ("CG1684_4_local_GR", "local GR/Newton source-side pass", "BLOCKED", "qbar source-weight obstruction remains open"),
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
            "next_target": "1685-Y5-R2FR-qbar-source-weight-intake-runner-or-matter-category-connectedness-proof.md",
            "script": "scripts/Y5_R2FR_qbar_source_weight_intake_runner_or_matter_category_connectedness_proof.py",
            "objective": "turn the 1684 qbar_source_weight intake schema into an executable row validator, while separately testing whether ordinary matter category connectedness/source-label forgetting can be parent-derived rather than imposed",
            "success_condition": "either connectedness/source-label forgetting is signed as a parent theorem, or the qbar finite row validator rejects/passes candidate kappa_A/w_A rows strictly by value, units, source path, basis, and projection fields",
            "why_next": "1684 shows no value and no proof; the next step is an executable intake gate or the deepest remaining proof clause",
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
    proof_rows: list[dict[str, object]],
    hunt_rows: list[dict[str, object]],
    intake_rows: list[dict[str, object]],
    hook_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    proof_not_closed = any(row["current_result"] == "PROOF_NOT_CLOSED" for row in proof_rows) and all(not bool_cell(row["proof_signed"]) for row in proof_rows)
    value_none = any(row["hunt_id"] == "VH1684_4_verdict" and row["found_value"] == "NO_VALUE_FOUND" for row in hunt_rows)
    intake_exact = len(intake_rows) == 1 and intake_rows[0]["basis_component"] == "qbar_source_weight" and intake_rows[0]["intake_status"] == "SCHEMA_READY_VALUES_MISSING_NONCLAIM"
    hooks_exact = {row["arena"] for row in hook_rows} == EXPECTED_ARENAS
    gate_locked = len(gate_rows) == 1 and gate_rows[0]["current_status"] == "GATE_ACTIVE_REJECTS_CURRENT_BRANCH" and not bool_cell(gate_rows[0]["gate_pass"])
    decision_safe = any(row["decision"] == "NO_QBAR_SOURCE_WEIGHT_VALUE_FOUND" for row in decisions)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claims)
    next_target_selected = next_rows[0]["next_target"] == "1685-Y5-R2FR-qbar-source-weight-intake-runner-or-matter-category-connectedness-proof.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED)
    branch_copies = all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1684*")) if FORMALIZATION.exists() else True

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
        ("VAL1684_0_sources_exist", sources_ok, "all cited 1684 source paths exist and required needles are present"),
        ("VAL1684_1_proof_not_closed", proof_not_closed, "source-label forgetting proof remains unsigned"),
        ("VAL1684_2_value_none", value_none, "qbar source-weight value hunt finds no value/bound"),
        ("VAL1684_3_intake_exact", intake_exact, "finite intake schema targets qbar_source_weight and remains nonclaim"),
        ("VAL1684_4_hooks_exact", hooks_exact, "arena hooks cover WEP, R10, Newton-GM, R11, and PPN/local-GR"),
        ("VAL1684_5_gate_locked", gate_locked, "1682 source branch gate remains locked"),
        ("VAL1684_6_decision_safe", decision_safe, "decision records no qbar source-weight value found"),
        ("VAL1684_7_claim_gate_safe", claim_gate_safe, "all claim gates remain false"),
        ("VAL1684_8_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1684_9_blocked_not_ready", blocked_not_ready, "no blocked/missing row is marked claim/scoring ready"),
        ("VAL1684_10_next_target_selected", next_target_selected, "next target selects qbar intake runner or matter-category connectedness proof"),
        ("VAL1684_11_csv_parse", csv_parse, "all generated 1684 CSVs parse"),
        ("VAL1684_12_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1684_13_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1684_14_formalization_untouched", formalization_clean, "no 1684 outputs found under formalization-workbench"),
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
            "check_id": "VAL1684_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1684 qbar source-weight value hunt or source-label forgetting proof validation",
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
    hunt_rows: list[dict[str, object]],
    intake_rows: list[dict[str, object]],
    hook_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1684 - Qbar Source-Weight Value Hunt Or Source-Label Forgetting Proof

**Private status:** narrow qbar/source-weight checkpoint. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, WEP pass, R10 pass, R11 pass, clock pass, orbital pass, or public claim is made.

## Verdict

`qbar_source_weight` is still not theorem-zero. Source-label forgetting is an exact route, but the current corpus does not parent-sign the label quotient, connected ordinary-matter source category, measure/readout no-reentry, or radiative stability clauses.

The finite value hunt also finds no local value or bound for `zeta_source_weight_I`. 1684 therefore writes the strict finite intake schema and arena hooks, but keeps the 1682 source-branch gate locked.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1684"])}

## Source-Label Forgetting Proof Attempt

{markdown_table(proof_rows, ["proof_id", "claim", "mathematical_form", "current_result", "current_gap"])}

## Value Hunt

{markdown_table(hunt_rows, ["hunt_id", "object", "source_file", "source_anchor", "found_value", "found_bound_or_threshold", "why_not_scoreable"])}

## Finite Intake Schema

{markdown_table(intake_rows, ["intake_id", "basis_component", "coefficient_symbol", "accepted_forms", "current_value", "current_basis", "current_projection", "intake_status"])}

## Arena Hooks

{markdown_table(hook_rows, ["hook_id", "arena", "projection_hook", "additional_requirements", "current_status"])}

## Gate Status

{markdown_table(gate_rows, ["gate_id", "gate_module", "current_status", "gate_pass", "reason"])}

## Decisions

{markdown_table(decision_rows_, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "gate", "gate_pass", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This checkpoint does not close the source side, but it cuts the problem down to a concrete fork. Either prove the ordinary matter source category forgets labels before gravity couples, or fill the `zeta_source_weight_I` row as a real finite coefficient. Until then, the source-side gate stays closed.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    proof_rows = forgetting_proof_rows()
    hunt_rows = value_hunt_rows()
    intake_rows = finite_intake_rows()
    hook_rows = arena_hook_rows()
    gate_rows = gate_status_rows()
    decisions = decision_rows()
    claims = claim_gate_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, source_rows, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1684", "valid_for_claim", "claim_allowed"])
    write_csv(FORGETTING_PROOF, proof_rows, ["branch_id", "proof_id", "claim", "mathematical_form", "current_result", "if_signed", "current_gap", "source_anchor", "proof_signed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(VALUE_HUNT, hunt_rows, ["branch_id", "hunt_id", "object", "source_file", "source_anchor", "found_value", "found_bound_or_threshold", "why_not_scoreable", "coefficient_filled", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(FINITE_INTAKE, intake_rows, ["branch_id", "intake_id", "basis_component", "coefficient_symbol", "accepted_forms", "required_value_fields", "required_basis_fields", "required_source_fields", "required_projection_fields", "current_value", "current_basis", "current_source_path", "current_projection", "intake_status", "coefficient_filled", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(ARENA_HOOKS, hook_rows, ["branch_id", "hook_id", "arena", "projection_hook", "additional_requirements", "current_status", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(GATE_STATUS, gate_rows, ["branch_id", "gate_id", "gate_module", "prior_status", "current_status", "gate_pass", "reason", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(DECISION, decisions, ["branch_id", "decision_id", "decision", "reason", "next_action", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claims, ["branch_id", "gate_id", "gate", "gate_pass", "status", "reason", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "next_target", "script", "objective", "success_condition", "why_next", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    validation_rows = validate(source_rows, proof_rows, hunt_rows, intake_rows, hook_rows, gate_rows, decisions, claims, next_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, proof_rows, hunt_rows, intake_rows, hook_rows, gate_rows, decisions, claims, next_rows, validation_rows)

    failed_rows = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAIL {failed_row['check_id']}: {failed_row['detail']}")
        raise SystemExit(1)
    print("1684 validation PASS")


if __name__ == "__main__":
    main()
