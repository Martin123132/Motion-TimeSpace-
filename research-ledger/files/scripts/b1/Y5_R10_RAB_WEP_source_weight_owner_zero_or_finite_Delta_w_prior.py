from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1326"
TITLE = "1326-Y5-R10-RAB-WEP-source-weight-owner-zero-or-finite-Delta-w-prior"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
ZERO_PROOF_PATH = OUT_DIR / f"{PACK_ID}_DELTA_W_ZERO_PROOF_AUDIT.csv"
PREMISE_STATUS_PATH = OUT_DIR / f"{PACK_ID}_PARENT_PREMISE_STATUS.csv"
FINITE_PRIOR_PATH = OUT_DIR / f"{PACK_ID}_FINITE_DELTA_W_PRIOR_CONTRACT.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_WEIGHT_RUNNER_UPDATE.csv"
OBSTRUCTION_PATH = OUT_DIR / f"{PACK_ID}_OBSTRUCTION_LEDGER.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1326_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
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
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        ZERO_PROOF_PATH,
        PREMISE_STATUS_PATH,
        FINITE_PRIOR_PATH,
        RUNNER_PATH,
        OBSTRUCTION_PATH,
        ANTI_SHORTCUT_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1326_0_1325_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1325_NEXT_TARGET.csv",
            "needle": "NEXT1325_0_1326",
            "role": "handoff into source-weight owner zero or finite Delta_w prior",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1326_1_1325_blocker",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1325_BLOCKER_LEDGER.csv",
            "needle": "BLK1325_3_delta_w",
            "role": "current Delta_w blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1326_2_1224_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1224_OWNER_PROOF_CLAUSES.csv",
            "needle": "OWN1224_6_verdict",
            "role": "source-weight owner proof clauses",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1326_3_1224_obstructions",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1224_SOURCE_WEIGHT_OBSTRUCTION_LEDGER.csv",
            "needle": "OBS1224_0_wA_action_multiplier",
            "role": "active source-weight obstructions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1326_4_1224_product",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1224_SOURCE_WEIGHT_PRODUCT_LAW.csv",
            "needle": "PROD1224_0_source_weight",
            "role": "source-weight product law",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1326_5_1230_action",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv",
            "needle": "UAS1230_1_connected_naturality_lemma",
            "role": "exact conditional connected-naturality theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1326_6_1230_measure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1230_MEASURE_DESCENT_PROOF_STACK.csv",
            "needle": "MDS1230_4_verdict",
            "role": "measure/current descent proof stack",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1326_7_1230_failures",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1230_OWNER_FAILURE_MODE_LEDGER.csv",
            "needle": "FAIL1230_0_disconnected_category",
            "role": "active theorem failure modes",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1326_8_1230_finite",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1230_FINITE_DELTA_W_PRIOR_CONTRACT.csv",
            "needle": "FDW1230_0_Delta_w_TiPt",
            "role": "finite Delta_w prior contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1326_9_1231_component_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1231_DELTA_W_COMPONENT_MAP.csv",
            "needle": "DWM1231_1_TiPt_difference",
            "role": "Delta_w component residual map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1326_10_1229_clauses",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv",
            "needle": "CLC1229_8_verdict",
            "role": "universal source-coupling clause audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1326_11_1067_action_scale",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv",
            "needle": "ASO1067_5_verdict",
            "role": "prior action-scale owner attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1326_12_1067_hbar_measure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv",
            "needle": "HMO1067_4_verdict",
            "role": "hbar/measure owner audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    zero_proof = [
        {
            "zero_id": "ZERO1326_0_connected_naturality",
            "claim_piece": "connected parent matter category collapses natural source weights",
            "formal_result": "If C_matter is connected and the action-density/source functor is parent-owned, every natural positive w_A is one common w_*.",
            "evidence": "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv:UAS1230_1_connected_naturality_lemma",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_promotion": "parent-signed connected C_matter and action-density functor",
            "effect_on_delta_w": "would remove relative Delta_w only after premise is signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "ZERO1326_1_common_factor",
            "claim_piece": "common source scale can be absorbed into G_N",
            "formal_result": "If w_A=w_* for all ordinary matter, T_eff=w_* sum_A T_A; only the common normalization changes.",
            "evidence": "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv:UAS1230_2_common_factor_absorption",
            "status": "EXACT_IF_CONNECTEDNESS_SIGNED",
            "missing_for_promotion": "relative weights must already be collapsed to one common factor",
            "effect_on_delta_w": "common mode does not create Ti/Pt residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "ZERO1326_2_measure_current_extension",
            "claim_piece": "measure/current/readout descent cannot regenerate w_A",
            "formal_result": "The parent measure, hbar, Hilbert current extraction, and readout projection must be species-blind.",
            "evidence": "P8_Y5_R10_1230_MEASURE_DESCENT_PROOF_STACK.csv:MDS1230_4_verdict",
            "status": "NOT_CLOSED",
            "missing_for_promotion": "parent measure line, quotient Jacobian, hbar_parent, current extraction, readout descent",
            "effect_on_delta_w": "finite Delta_w branch remains mandatory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "ZERO1326_3_current_corpus_signature",
            "claim_piece": "current corpus already signs Delta_w_TiPt=0",
            "formal_result": "All owner clauses would need to be signed together before zero promotion.",
            "evidence": "P8_Y5_R10_1224_OWNER_PROOF_CLAUSES.csv:OWN1224_6_verdict;P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv:UAS1230_5_verdict",
            "status": "NOT_PARENT_SIGNED",
            "missing_for_promotion": "source-weight owner proof, connectedness, action-scale/measure owner, and readout descent",
            "effect_on_delta_w": "Delta_w_TiPt is retained as an explicit finite residual slot",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    premise_status = [
        {
            "premise_id": "PREM1326_0_single_action_scale",
            "needed_premise": "single parent action scale/hbar/action-density line",
            "source": "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv:UAS1230_0_target",
            "current_status": "TARGET_SHARPENED_NOT_PARENT_DERIVED",
            "zero_effect": "cannot remove species action multipliers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "PREM1326_1_connected_category",
            "needed_premise": "connected ordinary matter category for source normalization",
            "source": "P8_Y5_R10_1231_DELTA_W_COMPONENT_MAP.csv:DWM1231_1_TiPt_difference",
            "current_status": "MISSING_COMPONENT_FRACTIONS_AND_PRIORS",
            "zero_effect": "disconnected component residuals remain live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "PREM1326_2_measure_descent",
            "needed_premise": "species-blind measure/coframe/quotient descent",
            "source": "P8_Y5_R10_1230_MEASURE_DESCENT_PROOF_STACK.csv:MDS1230_4_verdict",
            "current_status": "NOT_CLOSED",
            "zero_effect": "measure Jacobian can mimic source multiplier",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "PREM1326_3_current_owner",
            "needed_premise": "Hilbert source/current extracted before source-label/readout selection",
            "source": "P8_Y5_R10_1224_OWNER_PROOF_CLAUSES.csv:OWN1224_1_universal_current_owner",
            "current_status": "CONDITIONAL_NOT_READOUT_SIGNED",
            "zero_effect": "w_A T_A counterexample remains available",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "PREM1326_4_readout_descent",
            "needed_premise": "MICROSCOPE/source-worldtube/readout does not reintroduce weights",
            "source": "P8_Y5_R10_1224_OWNER_PROOF_CLAUSES.csv:OWN1224_5_tau_readout_projection",
            "current_status": "PROJECTION_CONTRACT_WRITTEN_NOT_DERIVED",
            "zero_effect": "Delta_w_TiPt*tau_WEP product remains unscoreable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_prior = [
        {
            "prior_id": "FDW1326_0_zero_option",
            "quantity": "Delta_w_TiPt",
            "value_or_status": "ZERO_ONLY_IF_ALL_PREM1326_CLAUSES_SIGNED",
            "units": "dimensionless",
            "source_requirement": "connected C_matter + action-density owner + measure/current/readout descent",
            "runner_role": "theorem route retained but blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "FDW1326_1_finite_prior_width",
            "quantity": "abs(Delta_w_TiPt)",
            "value_or_status": "MISSING_NUMERIC_PRIOR_WIDTH",
            "units": "dimensionless",
            "source_requirement": "parent-derived prior, material model, or explicit phenomenological prior marked nonclaim",
            "runner_role": "finite source-weight residual input",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "FDW1326_2_component_formula",
            "quantity": "Delta_w_TiPt",
            "value_or_status": "sum_c (F_Ti,c-F_Pt,c) delta_w_c + (delta_w_K,Ti-delta_w_K,Pt)",
            "units": "dimensionless",
            "source_requirement": "component fractions, component priors, and readout residual in one convention",
            "runner_role": "strict finite fallback formula",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "FDW1326_3_tau_WEP_dependency",
            "quantity": "tau_WEP",
            "value_or_status": "MISSING_LAB_SOURCE_ORBIT_PROJECTION",
            "units": "dimensionless",
            "source_requirement": "source worldtube/orbit/readout/product convention",
            "runner_role": "finite product cannot score even if Delta_w prior is later sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "FDW1326_4_no_claim_guard",
            "quantity": "P_WEP_source_weight",
            "value_or_status": "NOT_SCOREABLE",
            "units": "dimensionless_eta",
            "source_requirement": "no MISSING markers, no placeholders, no threshold-as-prior, no unity/cancellation shortcuts",
            "runner_role": "guard against premature WEP/local-GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner = [
        {
            "runner_id": "RUN1326_0_zero_theorem",
            "target": "Delta_w_TiPt=0",
            "input_status": "CONDITIONAL_THEOREM_ONLY_NOT_PARENT_SIGNED",
            "missing_inputs": "connected_C_matter;action_density_owner;hbar_measure_owner;source_label_forgetting;readout_descent",
            "runner_status": "REFUSED_NO_ZERO_PROMOTION",
            "claim_effect": "no Delta_w=0, no WEP pass, no local-GR source-coupling pass",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1326_1_finite_prior",
            "target": "abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15",
            "input_status": "FINITE_PRIOR_CONTRACT_STAGED",
            "missing_inputs": "numeric_Delta_w_TiPt;tau_WEP;source_profile;official_readout_arrays",
            "runner_status": "REFUSED_NOT_SCOREABLE",
            "claim_effect": "finite branch retained as nonclaim input contract",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    obstruction = [
        {
            "obstruction_id": "OBS1326_0_disconnected_category",
            "failure_mode": "C_matter splits into disconnected source components",
            "source": "P8_Y5_R10_1230_OWNER_FAILURE_MODE_LEDGER.csv:FAIL1230_0_disconnected_category",
            "status": "ACTIVE_UNTIL_PARENT_CATEGORY_SIGNED",
            "blocks": "connected naturality collapse",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS1326_1_action_multiplier",
            "failure_mode": "S_matter=sum_A w_A S_A changes Hilbert source normalization",
            "source": "P8_Y5_R10_1224_SOURCE_WEIGHT_OBSTRUCTION_LEDGER.csv:OBS1224_0_wA_action_multiplier",
            "status": "ACTIVE_OBSTRUCTION",
            "blocks": "Delta_w theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS1326_2_hbar_measure",
            "failure_mode": "sector-specific hbar_A or measure Jacobian recreates source weights",
            "source": "P8_Y5_R10_1230_OWNER_FAILURE_MODE_LEDGER.csv:FAIL1230_2_measure_jacobian;FAIL1230_3_hbar_A",
            "status": "ACTIVE_UNTIL_MEASURE_DESCENT_SIGNED",
            "blocks": "measure/current owner extension",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS1326_3_readout_reentry",
            "failure_mode": "post-variation readout/projection introduces effective source-weight kernel",
            "source": "P8_Y5_R10_1230_OWNER_FAILURE_MODE_LEDGER.csv:FAIL1230_4_readout_reentry",
            "status": "ACTIVE_UNTIL_READOUT_DESCENT_SIGNED",
            "blocks": "observable WEP/source-weight theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1326_0_no_naturality_only_zero",
            "shortcut": "set Delta_w_TiPt=0 using naturality without connected parent category",
            "enforcement": "REFUSED; disconnected components remain active",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1326_1_no_action_scale_eom_shortcut",
            "shortcut": "treat sector action multipliers as harmless because classical EOM are unchanged",
            "enforcement": "REFUSED; Hilbert source and quantum measure can see them",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1326_2_no_threshold_as_prior",
            "shortcut": "use the WEP bound to define a theory prior for Delta_w",
            "enforcement": "REFUSED; bound is comparison data, not a parent/source value",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1326_3_no_tau_unity",
            "shortcut": "set tau_WEP=1 to convert eta bound into Delta_w width",
            "enforcement": "REFUSED; tau_WEP requires source-worldtube/orbit/readout derivation or source",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1326_4_no_local_GR_from_conditional",
            "shortcut": "claim local GR/Newton source-coupling reduction from the conditional theorem",
            "enforcement": "REFUSED until all parent premises and Bianchi/readout gates close",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1326_0_conditional_theorem_kept",
            "decision": "keep connected-naturality as the strongest derivation route",
            "because": "it is an exact conditional theorem and would collapse relative source weights if parent premises are signed",
            "effect": "derivation path remains alive but not claimable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1326_1_zero_not_promoted",
            "decision": "do not promote Delta_w_TiPt=0",
            "because": "connectedness, action-scale/measure ownership, current extraction, and readout descent remain unsigned",
            "effect": "WEP/local-GR source-coupling branch remains blocked but disciplined",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1326_2_finite_prior_retained",
            "decision": "stage finite Delta_w prior contract as the honest fallback",
            "because": "the source-weight theorem-zero route is not closed and the product law needs explicit Delta_w and tau_WEP",
            "effect": "next work should fill component fractions/priors or prove parent graph connectedness",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1326_0_1327",
            "target_file": "1327-Y5-R10-RAB-parent-interaction-graph-or-Delta-w-component-fraction-intake.md",
            "target_script": "scripts/Y5_R10_RAB_parent_interaction_graph_or_Delta_w_component_fraction_intake.py",
            "task": "reuse the 1231 component map: try one parent interaction-graph certificate; if not signed, turn Delta_w_TiPt component fractions and priors into strict nonclaim intake rows",
            "success_condition": "either connectedness/source-label forgetting gains a parent-signed certificate, or the Delta_w component formula gets a source-ready input matrix without WEP/local-GR claims",
            "do_not": "do not claim Delta_w=0; do not treat component proxies as full energy fractions; do not use WEP threshold as theory prior",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(ZERO_PROOF_PATH, zero_proof)
    write_csv(PREMISE_STATUS_PATH, premise_status)
    write_csv(FINITE_PRIOR_PATH, finite_prior)
    write_csv(RUNNER_PATH, runner)
    write_csv(OBSTRUCTION_PATH, obstruction)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations: list[dict[str, object]] = []
    sources_ok = all(row["exists"] and row["needle_found"] for row in source_register)
    validations.append(
        validation_row(
            "VAL1326_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(1 for row in source_register if row['exists'] and row['needle_found'])}/{len(source_register)} source anchors found",
        )
    )
    zero_not_promoted = all(not row["claim_allowed"] for row in zero_proof) and any(
        row["status"] == "NOT_PARENT_SIGNED" for row in zero_proof
    )
    validations.append(
        validation_row(
            "VAL1326_1_zero_not_promoted",
            "Delta_w zero proof is attempted but not promoted",
            zero_not_promoted,
            ";".join(f"{row['zero_id']}={row['status']}" for row in zero_proof),
        )
    )
    premise_blocked = all(row["current_status"] != "PARENT_SIGNED" for row in premise_status)
    validations.append(
        validation_row(
            "VAL1326_2_parent_premises_blocked",
            "all parent premises remain unsigned or conditional",
            premise_blocked,
            ";".join(f"{row['premise_id']}={row['current_status']}" for row in premise_status),
        )
    )
    finite_prior_ok = any(row["prior_id"] == "FDW1326_1_finite_prior_width" for row in finite_prior) and all(
        not row["claim_allowed"] for row in finite_prior
    )
    validations.append(
        validation_row(
            "VAL1326_3_finite_prior_contract_retained",
            "finite Delta_w prior contract exists and remains nonclaim",
            finite_prior_ok,
            ";".join(row["prior_id"] for row in finite_prior),
        )
    )
    runner_refuses = all(row["runner_status"].startswith("REFUSED") and not row["score_ready"] for row in runner)
    validations.append(
        validation_row(
            "VAL1326_4_runner_refuses",
            "source-weight zero and finite branches remain refused",
            runner_refuses,
            ";".join(f"{row['runner_id']}={row['runner_status']}" for row in runner),
        )
    )
    obstructions_active = all("ACTIVE" in row["status"] for row in obstruction)
    validations.append(
        validation_row(
            "VAL1326_5_obstructions_active",
            "source-weight theorem counterexamples remain explicit",
            obstructions_active,
            ";".join(row["obstruction_id"] for row in obstruction),
        )
    )
    shortcut_ok = all(row["status"] == "ENFORCED" for row in anti_shortcut)
    validations.append(
        validation_row(
            "VAL1326_6_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            shortcut_ok,
            ";".join(row["gate_id"] for row in anti_shortcut),
        )
    )
    nonclaim_ok = all_nonclaim(
        [
            source_register,
            zero_proof,
            premise_status,
            finite_prior,
            runner,
            obstruction,
            anti_shortcut,
            decision,
            next_target,
        ]
    )
    validations.append(
        validation_row(
            "VAL1326_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_ok,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    formal_outputs = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1326_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formal_outputs,
            f"formalization_generated_output_count={len(formal_outputs)}",
        )
    )
    next_ok = next_target[0]["target_file"].startswith("1327-Y5-R10-RAB-parent-interaction-graph")
    validations.append(
        validation_row(
            "VAL1326_9_next_target_1327",
            "next target routes to parent interaction graph or Delta_w component intake",
            next_ok,
            str(next_target[0]["target_file"]),
        )
    )
    validations.append(
        validation_row(
            "VAL1326_10_overall",
            "overall 1326 validation",
            all(row["status"] == "PASS" for row in validations),
            "1326 keeps exact conditional source-weight theorem, refuses zero promotion, and stages finite Delta_w prior contract",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1326: RAB WEP Source-Weight Owner Zero Or Finite Delta-w Prior

**Current verdict:** 1326 does not prove `Delta_w_TiPt=0`. It keeps the strongest result we have: connected naturality would collapse source weights to one common factor, but the parent connectedness/action-scale/measure/readout premises are not signed.

**Main progress:** the coupling lock is now in theorem form rather than fog form. Either prove the parent ordinary-matter interaction graph and measure/current owner, or keep a finite `Delta_w_TiPt` residual with explicit priors and projections.

**Decision:** retain `Delta_w_TiPt` as a nonclaim finite residual and route next to parent interaction graph / component-fraction intake. No WEP, local-GR, or source-coupling pass is claimed.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Delta-w Zero Proof Audit
{markdown_table(zero_proof, ["zero_id", "claim_piece", "formal_result", "evidence", "status", "missing_for_promotion", "effect_on_delta_w", "valid_for_claim", "claim_allowed"])}

## Parent Premise Status
{markdown_table(premise_status, ["premise_id", "needed_premise", "source", "current_status", "zero_effect", "valid_for_claim", "claim_allowed"])}

## Finite Delta-w Prior Contract
{markdown_table(finite_prior, ["prior_id", "quantity", "value_or_status", "units", "source_requirement", "runner_role", "valid_for_claim", "claim_allowed"])}

## Source-Weight Runner Update
{markdown_table(runner, ["runner_id", "target", "input_status", "missing_inputs", "runner_status", "claim_effect", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Obstruction Ledger
{markdown_table(obstruction, ["obstruction_id", "failure_mode", "source", "status", "blocks", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates
{markdown_table(anti_shortcut, ["gate_id", "shortcut", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
