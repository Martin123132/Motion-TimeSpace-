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
QUARANTINE = MICROSCOPE / "quarantine" / "1681"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1681-Y5-R2FR-finite-Rsource-contract-validator-or-parent-action-owner-clause.md"

SOURCE_FILES = {
    "1680_doc": ROOT / "1680-Y5-R2FR-source-current-owner-zero-theorem-or-finite-coefficient-contract.md",
    "1680_validation": OUT / "P8_Y5_BRR545_1680_VALIDATION.csv",
    "1680_clauses": OUT / "P8_Y5_PARENT_QLOC_1680_SOURCE_CURRENT_OWNER_ZERO_THEOREM_CLAUSES.csv",
    "1680_contract": OUT / "P8_Y5_PARENT_QLOC_1680_FINITE_RSOURCE_COEFFICIENT_CONTRACT_NONCLAIM.csv",
    "1680_countermodels": OUT / "P8_Y5_PARENT_QLOC_1680_COUNTERMODEL_MERGE_LEDGER.csv",
    "1680_claim_gate": OUT / "P8_Y5_PARENT_QLOC_1680_CLAIM_GATE.csv",
    "1679_wep_probe": OUT / "P8_Y5_PARENT_QLOC_1679_WEP_DATA_PROBE_DRY_RUN_LEDGER.csv",
    "1679_r10_probe": OUT / "P8_Y5_PARENT_QLOC_1679_R10_SOURCE_PROBE_DRY_RUN_LEDGER.csv",
    "1678_newton_probe": OUT / "P8_Y5_PARENT_QLOC_1678_NEWTON_GM_PROJECTION_ACQUISITION_TABLE_NONCLAIM.csv",
    "1678_r11_probe": OUT / "P8_Y5_PARENT_QLOC_1678_R11_SOURCE_OPERATOR_ACQUISITION_TABLE_NONCLAIM.csv",
    "1338_closure": OUT / "P8_Y5_R10_1338_NO_SOURCE_SLOT_CLOSURE_CONDITION.csv",
    "1416_acceptance": OUT / "P8_Y5_R10_1416_RSOURCE_ROW_ACCEPTANCE_GATE.csv",
}

NEEDLES = {
    "1680_doc": ["refuses `R_source=0`", "locks the six finite coefficient contracts"],
    "1680_validation": ["VAL1680_OVERALL", "PASS"],
    "1680_clauses": ["CL1680_3", "NoSourceOnlySpeciesSlot", "CL1680_4", "single_source_current_owner"],
    "1680_contract": ["RFC1680_0", "qbar_source_weight", "RFC1680_5", "beta_source_alpha_projection"],
    "1680_countermodels": ["CM1680_0", "LIVE_COUNTERMODEL_UNTIL_PARENT_CLAUSE_SIGNED_OR_FINITE_BOUND_SUPPLIED"],
    "1680_claim_gate": ["CG1680_2_finite_contract", "BLOCKED"],
    "1679_wep_probe": ["WDP1679_2_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_ACQUIRED"],
    "1679_r10_probe": ["R10P1679_6_bound_curve", "MISSING_FULL_CURVE_OR_CLAIM_GRADE_ANCHORS"],
    "1678_newton_probe": ["NEW1678_3_verdict", "NOT_SCOREABLE"],
    "1678_r11_probe": ["R11S1678_3_verdict", "NOT_SCOREABLE"],
    "1338_closure": ["CLOS1338_2_no_source_only_species_slot", "SHARPEST_EXPLICIT_CLOSURE"],
    "1416_acceptance": ["ACC1416_5_verdict", "ROW_SCHEMA_READY_VALUES_MISSING_NO_PASS"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1681_SOURCE_REGISTER.csv"
OWNER_CLAUSE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1681_PARENT_ACTION_OWNER_CLAUSE_AUDIT.csv"
VALIDATOR_RULES = OUT / "P8_Y5_PARENT_QLOC_1681_FINITE_CONTRACT_VALIDATOR_RULES.csv"
VALIDATOR_RESULT = OUT / "P8_Y5_PARENT_QLOC_1681_VALIDATOR_RESULT_MATRIX.csv"
ARENA_REFUSAL = OUT / "P8_Y5_PARENT_QLOC_1681_ARENA_USE_REFUSAL_MATRIX.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1681_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1681_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1681_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1681_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    OWNER_CLAUSE_AUDIT,
    VALIDATOR_RULES,
    VALIDATOR_RESULT,
    ARENA_REFUSAL,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    OWNER_CLAUSE_AUDIT,
    VALIDATOR_RULES,
    VALIDATOR_RESULT,
    ARENA_REFUSAL,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    OWNER_CLAUSE_AUDIT: [
        QUARANTINE / "PARENT_ACTION_OWNER_CLAUSE_AUDIT.csv",
        BRANCH_RESIDUALS / "R2FR_parent_action_owner_clause_audit_1681.csv",
        QUEUE / "JR1681_PARENT_ACTION_OWNER_CLAUSE_AUDIT.csv",
    ],
    VALIDATOR_RULES: [
        QUARANTINE / "FINITE_CONTRACT_VALIDATOR_RULES.csv",
        BRANCH_RESIDUALS / "R2FR_finite_contract_validator_rules_1681.csv",
        QUEUE / "JR1681_FINITE_CONTRACT_VALIDATOR_RULES.csv",
    ],
    VALIDATOR_RESULT: [
        QUARANTINE / "VALIDATOR_RESULT_MATRIX.csv",
        BRANCH_RESIDUALS / "R2FR_validator_result_matrix_1681.csv",
        QUEUE / "JR1681_VALIDATOR_RESULT_MATRIX.csv",
    ],
    ARENA_REFUSAL: [
        QUARANTINE / "ARENA_USE_REFUSAL_MATRIX.csv",
        BRANCH_RESIDUALS / "R2FR_arena_use_refusal_matrix_1681.csv",
        QUEUE / "JR1681_ARENA_USE_REFUSAL_MATRIX.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1681.csv",
        QUEUE / "JR1681_NEXT_TARGET_NONCLAIM.csv",
    ],
}

EXPECTED_COMPONENTS = {
    "qbar_source_weight",
    "current_rescaling_residual",
    "marker_readout_residual",
    "source_worldtube_projection",
    "direct_source_product",
    "beta_source_alpha_projection",
}

EXPECTED_ARENAS = {"WEP", "R10", "NEWTON_GM", "R11"}

SCORE_FLAGS = [
    "accepted_for_scoring",
    "score_ready",
    "valid_prediction_row",
    "valid_for_claim",
    "claim_allowed",
    "parent_signed",
    "validator_pass",
    "owner_clause_signed",
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
    value_text = str(value)
    markers = [
        "MISSING_",
        "NOT_SCORE",
        "NOT_DERIVED",
        "NOT_PARENT",
        "NOT_SIGNED",
        "BLOCKED",
        "REJECT",
        "FAIL",
        "DRY_RUN",
        "CONDITIONAL",
        "LIVE_COUNTER",
        "NO_PASS",
        "ABSENT",
    ]
    return any(marker in value_text for marker in markers)


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
                "use_in_1681": "finite R_source validator and parent-action owner clause audit",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def owner_clause_audit_rows() -> list[dict[str, object]]:
    raw_rows = [
        (
            "OCA1681_0_parent_domain",
            "parent_domain_fixed",
            "use CLOS1338_0 as parent action owner clause",
            "explicit closure row exists but is not a parent-derived action clause",
            "NOT_SIGNED_CLOSURE_ONLY",
            "CLOS1338_0_parent_domain;CL1680_0",
        ),
        (
            "OCA1681_1_observed_descent",
            "observed_descent_only",
            "use observed-frame descent as source-current owner",
            "descent protects representative leakage only conditionally; it does not ban all source-current coefficients",
            "NOT_SIGNED_CONDITIONAL_ONLY",
            "CLOS1338_1_observed_descent;CL1680_1",
        ),
        (
            "OCA1681_2_action_measure",
            "single_action_measure_owner",
            "promote one action/measure scale to owner of all ordinary matter source weights",
            "repeatedly marked missing parent proof; adopting it would be an axiom at this stage",
            "MISSING_PARENT_PROOF",
            "CL1680_2;OLT1338_4_action_scale_owner",
        ),
        (
            "OCA1681_3_no_source_slot",
            "NoSourceOnlySpeciesSlot",
            "promote Hom(SpeciesLabel,Coeff_active_source)=empty",
            "sharpest closure exists but 1338/1416 say it is not derived",
            "NOT_DERIVED_CURRENT_CORPUS",
            "CLOS1338_2_no_source_only_species_slot;BAN1416_2_object_language;CL1680_3",
        ),
        (
            "OCA1681_4_current_owner",
            "single_source_current_owner",
            "promote one Hilbert/Noether current functor before readout",
            "current owner is explicitly missing; CE1077_1 counterexample remains live",
            "MISSING_CURRENT_OWNER",
            "OWN1076_2_current_owner;CE1077_1_current_rescaling;CL1680_4",
        ),
        (
            "OCA1681_5_readout_order",
            "variation_before_readout",
            "promote readout-after-Hilbert-current ordering",
            "conditional closure only; non-Hilbert readout current remains live",
            "MISSING_PARENT_PROOF",
            "CLOS1338_4_variation_before_readout;CM1338_3_nonHilbert_readout_current;CL1680_5",
        ),
        (
            "OCA1681_6_no_marker",
            "no_marker_readout_extension",
            "ban marker/domain/boundary/readout masks as coefficient arguments",
            "no-marker extension theorem is not parent-signed; marker countermodels remain live",
            "MISSING_PARENT_PROOF",
            "CM1416_3_hidden_marker;CM1513_3_comoving_marker;CL1680_6",
        ),
        (
            "OCA1681_7_radiative",
            "radiative_readout_stability",
            "promote bare zero theorem through loops/readouts",
            "unsigned parallel gate; no observed-row transfer is allowed",
            "UNSIGNED_PARALLEL_GATE",
            "OLT1338_5_readout_stability;BAN1416_5_readout_radiative;CL1680_7",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "candidate_clause": candidate_clause,
            "promotion_attempt": promotion_attempt,
            "audit_result": audit_result,
            "current_status": current_status,
            "source_anchor": source_anchor,
            "owner_clause_signed": False,
            "parent_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, candidate_clause, promotion_attempt, audit_result, current_status, source_anchor in raw_rows
    ]


def validator_rule_rows() -> list[dict[str, object]]:
    raw_rows = [
        ("VR1681_0_components", "six_component_coverage", "all six 1680 R_source basis components must be present exactly once", "PASS_CURRENT_SCHEMA_ONLY", "schema integrity, not score readiness"),
        ("VR1681_1_zero_or_value", "theorem_zero_or_finite_value", "each component needs parent-signed theorem-zero or numeric/symbolic finite coefficient value", "FAIL_CURRENT_CONTRACT", "missing current_status markers remain"),
        ("VR1681_2_units", "declared_units", "each component needs declared units in the parent source-current basis", "PASS_REQUIREMENT_PRESENT_NOT_SUFFICIENT", "unit requirement text exists but no parent basis/normalization is signed"),
        ("VR1681_3_source_path", "source_path_and_anchor", "each coefficient or zero proof needs local source path and anchor support", "FAIL_CURRENT_CONTRACT", "1680 finite contract has requirements but no value source path"),
        ("VR1681_4_parent_basis", "parent_basis_and_normalization", "the parent R_source coordinate basis and source-current normalization must be declared", "FAIL_CURRENT_CONTRACT", "parent basis remains not signed"),
        ("VR1681_5_arena_projection", "arena_projection", "WEP/R10/Newton/R11 must each have compatible projection kernels before use", "FAIL_CURRENT_CONTRACT", "arena probes remain dry-run/nonclaim"),
        ("VR1681_6_no_missing_markers", "missing_marker_refusal", "any MISSING/NOT_SCOREABLE/DRY_RUN/CONDITIONAL/LIVE_COUNTER marker rejects the row", "ACTIVE_REFUSAL_RULE", "strict guard for future runners"),
        ("VR1681_7_claim_flags", "claim_flags_false_until_pass", "valid_for_claim and claim_allowed stay false unless all rules pass", "ACTIVE_REFUSAL_RULE", "prevents accidental public/local-GR claim"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "rule_id": rule_id,
            "rule": rule,
            "acceptance_condition": acceptance_condition,
            "current_status": current_status,
            "effect": effect,
            "validator_pass": False if "FAIL" in current_status or "REFUSAL" in current_status else False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rule_id, rule, acceptance_condition, current_status, effect in raw_rows
    ]


def validator_result_rows(contract_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_row in contract_rows:
        current_status = source_row["current_status"]
        has_missing = blocked_marker(current_status)
        unit_present = bool(source_row.get("unit_requirement", "").strip())
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "contract_id": source_row["contract_id"],
                "basis_component": source_row["basis_component"],
                "coefficient_symbol": source_row["coefficient_symbol"],
                "component_exists": True,
                "unit_requirement_present": unit_present,
                "theorem_zero_signed": bool_cell(source_row.get("theorem_proved", "False")) and bool_cell(source_row.get("parent_signed", "False")),
                "finite_value_present": False,
                "source_path_present": False,
                "source_anchor_present": False,
                "parent_basis_signed": False,
                "arena_projection_ready": False,
                "missing_marker_present": has_missing,
                "validation_result": "REJECT_MISSING_ZERO_OR_VALUE_SOURCE_PATH_PARENT_BASIS_OR_ARENA_PROJECTION",
                "failure_reason": f"{current_status}; no theorem-zero; no finite value; no value source path; no arena projection",
                "validator_pass": False,
                "accepted_for_scoring": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def arena_refusal_rows() -> list[dict[str, object]]:
    raw_rows = [
        (
            "AR1681_0_WEP",
            "WEP",
            "all six finite R_source coefficients plus MICROSCOPE arrays/product convention/worldtube/material tensor/tau",
            "P8_Y5_PARENT_QLOC_1679_WEP_DATA_PROBE_DRY_RUN_LEDGER.csv",
            "OFFICIAL_ARRAYS_NOT_ACQUIRED;MISSING_SOURCE_PROFILE_WEIGHTING;MISSING_FULL_MATERIAL_TENSOR;finite coefficients missing",
        ),
        (
            "AR1681_1_R10",
            "R10",
            "all six finite R_source coefficients plus lambda owner, source/test charge, projection, alpha row, bound curve",
            "P8_Y5_PARENT_QLOC_1679_R10_SOURCE_PROBE_DRY_RUN_LEDGER.csv",
            "MISSING_COMPONENT_VALUES;MISSING_M_c_OR_MASS_GAP;MISSING_FULL_CURVE_OR_CLAIM_GRADE_ANCHORS",
        ),
        (
            "AR1681_2_NEWTON",
            "NEWTON_GM",
            "all six finite R_source coefficients plus current owner, single G_N normalization, Gauss/orbital calibration",
            "P8_Y5_PARENT_QLOC_1678_NEWTON_GM_PROJECTION_ACQUISITION_TABLE_NONCLAIM.csv",
            "MISSING_CURRENT_OWNER;MISSING_SINGLE_GN_NORMALIZATION;MISSING_GAUSS_OR_ORBITAL_CALIBRATION",
        ),
        (
            "AR1681_3_R11",
            "R11",
            "all six finite R_source coefficients plus operator basis, projection coefficients, current owner",
            "P8_Y5_PARENT_QLOC_1678_R11_SOURCE_OPERATOR_ACQUISITION_TABLE_NONCLAIM.csv",
            "MISSING_R11_OPERATOR_SOURCE_BASIS;MISSING_R11_PROJECTION_COEFFICIENTS;MISSING_CURRENT_OWNER",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "arena_gate_id": arena_gate_id,
            "arena": arena,
            "required_inputs": required_inputs,
            "source_file": source_file,
            "current_blockers": current_blockers,
            "validator_result": "REJECT_ARENA_USE",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for arena_gate_id, arena, required_inputs, source_file, current_blockers in raw_rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        (
            "D1681_0_owner_clause",
            "NO_PARENT_ACTION_OWNER_CLAUSE_SIGNED",
            "all candidate zero-theorem clauses remain closure-only, missing parent proof, or unsigned",
            "do not promote any R_source component to theorem-zero",
        ),
        (
            "D1681_1_validator",
            "VALIDATOR_REJECTS_CURRENT_CONTRACT",
            "each finite coefficient row lacks theorem-zero/value source path, signed parent basis, and arena projection",
            "block WEP/R10/Newton/R11 use until rows are filled or proved zero",
        ),
        (
            "D1681_2_arena",
            "ALL_SOURCE_ARENAS_REJECTED",
            "WEP, R10, Newton-GM, and R11 all still depend on missing source coefficients and projection/readout inputs",
            "future runners must import this gate before scoring",
        ),
        (
            "D1681_3_next",
            "BUILD_RUNNER_IMPORT_GATE",
            "the contract is now enforceable as a matrix; next step is a reusable runner gate that downstream tests must call",
            "move to 1682",
        ),
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
        ("CG1681_0_owner", "parent action owner clause signed", "BLOCKED", "owner clause audit signs zero clauses=0"),
        ("CG1681_1_validator", "finite R_source contract validator pass", "BLOCKED", "all six finite coefficient rows are rejected"),
        ("CG1681_2_WEP", "WEP source-side use", "BLOCKED", "arena matrix rejects WEP use"),
        ("CG1681_3_R10", "R10 source-side use", "BLOCKED", "arena matrix rejects R10 use"),
        ("CG1681_4_Newton", "Newton-GM source-side use", "BLOCKED", "arena matrix rejects Newton-GM use"),
        ("CG1681_5_R11", "R11 source/operator use", "BLOCKED", "arena matrix rejects R11 use"),
        ("CG1681_6_local_GR", "local GR/Newton/PPN pass", "BLOCKED", "source-side branch remains nonclaim and geometric reduction remains separate"),
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
            "next_target": "1682-Y5-R2FR-source-branch-runner-import-gate-and-parent-clause-search.md",
            "script": "scripts/Y5_R2FR_source_branch_runner_import_gate_and_parent_clause_search.py",
            "objective": "make downstream WEP/R10/Newton/R11 runners import the 1681 validator gate before scoring, while running a narrow parent-clause search for any non-ad-hoc action statement that can sign a zero-theorem clause",
            "success_condition": "source-side runner use is programmatically refused unless 1681 passes, and any candidate parent clause is either source-backed and clause-specific or rejected as closure/ad hoc",
            "why_next": "1681 creates the enforcement matrix; 1682 should wire it into future tests so the framework cannot accidentally overclaim while we keep hunting derivations",
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
    owner_rows: list[dict[str, object]],
    rule_rows: list[dict[str, object]],
    result_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    no_owner_clause_signed = all(not bool_cell(row["owner_clause_signed"]) and not bool_cell(row["parent_signed"]) for row in owner_rows)
    validator_rules_complete = {row["rule"] for row in rule_rows} == {
        "six_component_coverage",
        "theorem_zero_or_finite_value",
        "declared_units",
        "source_path_and_anchor",
        "parent_basis_and_normalization",
        "arena_projection",
        "missing_marker_refusal",
        "claim_flags_false_until_pass",
    }
    result_components_exact = {row["basis_component"] for row in result_rows} == EXPECTED_COMPONENTS
    all_rows_rejected = all(row["validation_result"].startswith("REJECT_") and not bool_cell(row["validator_pass"]) for row in result_rows)
    all_missing_guarded = all(bool_cell(row["missing_marker_present"]) for row in result_rows)
    arena_exact = {row["arena"] for row in arena_rows} == EXPECTED_ARENAS
    all_arenas_rejected = all(row["validator_result"] == "REJECT_ARENA_USE" and not bool_cell(row["score_ready"]) for row in arena_rows)
    decision_safe = any(row["decision"] == "VALIDATOR_REJECTS_CURRENT_CONTRACT" for row in decisions)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claims)
    next_target_selected = next_rows[0]["next_target"] == "1682-Y5-R2FR-source-branch-runner-import-gate-and-parent-clause-search.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED)
    branch_copies = all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1681*")) if FORMALIZATION.exists() else True

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
        ("VAL1681_0_sources_exist", sources_ok, "all cited 1681 source paths exist and required needles are present"),
        ("VAL1681_1_no_owner_clause_signed", no_owner_clause_signed, "parent-action owner clause audit signs no zero-theorem clause"),
        ("VAL1681_2_validator_rules_complete", validator_rules_complete, "validator rules cover components, values, units, sources, parent basis, arenas, missing markers, and claim flags"),
        ("VAL1681_3_result_components_exact", result_components_exact, "validator matrix covers exactly six R_source components"),
        ("VAL1681_4_all_rows_rejected", all_rows_rejected, "current finite contract rows are rejected"),
        ("VAL1681_5_all_missing_guarded", all_missing_guarded, "each rejected row has missing/blocked markers guarded"),
        ("VAL1681_6_arena_exact", arena_exact, "arena refusal matrix covers WEP, R10, Newton-GM, and R11"),
        ("VAL1681_7_all_arenas_rejected", all_arenas_rejected, "all source-side arenas are rejected for current use"),
        ("VAL1681_8_decision_safe", decision_safe, "decision records validator rejection"),
        ("VAL1681_9_claim_gate_safe", claim_gate_safe, "all claim gates remain false"),
        ("VAL1681_10_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1681_11_blocked_not_ready", blocked_not_ready, "no blocked/missing/rejected row is marked claim/scoring ready"),
        ("VAL1681_12_next_target_selected", next_target_selected, "next target selects source-branch runner import gate and parent clause search"),
        ("VAL1681_13_csv_parse", csv_parse, "all generated 1681 CSVs parse"),
        ("VAL1681_14_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1681_15_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1681_16_formalization_untouched", formalization_clean, "no 1681 outputs found under formalization-workbench"),
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
            "check_id": "VAL1681_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1681 finite R_source contract validator or parent action owner clause validation",
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
    owner_rows: list[dict[str, object]],
    rule_rows: list[dict[str, object]],
    result_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1681 - Finite Rsource Contract Validator Or Parent Action Owner Clause

**Private status:** enforcement checkpoint. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, WEP pass, R10 pass, R11 pass, clock pass, orbital pass, or public claim is made.

## Verdict

1681 finds **no parent-action owner clause** that can sign a source-current/no-marker zero theorem without becoming an added closure axiom.

The finite `R_source` validator therefore rejects the current source-side branch for WEP, R10, Newton-GM, and R11 use. This is the right kind of ugly: future tests now need real theorem-zero clauses or real finite coefficients with units, source paths, parent basis, and arena projections.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1681"])}

## Parent-Action Owner Clause Audit

{markdown_table(owner_rows, ["audit_id", "candidate_clause", "promotion_attempt", "audit_result", "current_status"])}

## Validator Rules

{markdown_table(rule_rows, ["rule_id", "rule", "acceptance_condition", "current_status", "effect"])}

## Validator Result Matrix

{markdown_table(result_rows, ["contract_id", "basis_component", "coefficient_symbol", "unit_requirement_present", "missing_marker_present", "validation_result"])}

## Arena Use Refusal Matrix

{markdown_table(arena_rows, ["arena_gate_id", "arena", "required_inputs", "current_blockers", "validator_result"])}

## Decisions

{markdown_table(decision_rows_, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "gate", "gate_pass", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This checkpoint is a seatbelt. The project can still go two ways: derive the owner clause properly, or fill finite coefficients honestly. But after 1681, a downstream local-GR/WEP/R10/Newton/R11 test has to pass the gate before it can call the source side clean.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    owner_rows = owner_clause_audit_rows()
    rule_rows = validator_rule_rows()
    contract_rows = read_csv(SOURCE_FILES["1680_contract"])
    result_rows = validator_result_rows(contract_rows)
    arena_rows = arena_refusal_rows()
    decisions = decision_rows()
    claims = claim_gate_rows()
    next_rows = next_target_rows()

    write_csv(
        SOURCE_REGISTER,
        source_rows,
        ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1681", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        OWNER_CLAUSE_AUDIT,
        owner_rows,
        ["branch_id", "audit_id", "candidate_clause", "promotion_attempt", "audit_result", "current_status", "source_anchor", "owner_clause_signed", "parent_signed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        VALIDATOR_RULES,
        rule_rows,
        ["branch_id", "rule_id", "rule", "acceptance_condition", "current_status", "effect", "validator_pass", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        VALIDATOR_RESULT,
        result_rows,
        ["branch_id", "contract_id", "basis_component", "coefficient_symbol", "component_exists", "unit_requirement_present", "theorem_zero_signed", "finite_value_present", "source_path_present", "source_anchor_present", "parent_basis_signed", "arena_projection_ready", "missing_marker_present", "validation_result", "failure_reason", "validator_pass", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        ARENA_REFUSAL,
        arena_rows,
        ["branch_id", "arena_gate_id", "arena", "required_inputs", "source_file", "current_blockers", "validator_result", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(DECISION, decisions, ["branch_id", "decision_id", "decision", "reason", "next_action", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claims, ["branch_id", "gate_id", "gate", "gate_pass", "status", "reason", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "next_target", "script", "objective", "success_condition", "why_next", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    validation_rows = validate(source_rows, owner_rows, rule_rows, result_rows, arena_rows, decisions, claims, next_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, owner_rows, rule_rows, result_rows, arena_rows, decisions, claims, next_rows, validation_rows)

    failed_rows = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAIL {failed_row['check_id']}: {failed_row['detail']}")
        raise SystemExit(1)
    print("1681 validation PASS")


if __name__ == "__main__":
    main()
