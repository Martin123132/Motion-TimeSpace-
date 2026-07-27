from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1594"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1594-Y5-R2FR-action-weight-exclusion-or-beta-source-acquisition-validator.md"

SOURCE_FILES = {
    "1593_doc": ROOT / "1593-Y5-R2FR-canonical-coupling-zero-theorem-or-finite-beta-source-rows.md",
    "1593_validation": OUT / "P8_Y5_BRR545_1593_VALIDATION.csv",
    "1593_beta_rows": OUT / "P8_Y5_PARENT_QLOC_1593_FINITE_BETA_SOURCE_ROWS.csv",
    "1593_source_residual": OUT / "P8_Y5_PARENT_QLOC_1593_ACTION_WEIGHT_SOURCE_RESIDUAL.csv",
    "1066_source_scalar": OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
    "1066_field_measure": OUT / "P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv",
    "1078_object_language": OUT / "P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv",
    "1078_action_measure": OUT / "P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv",
    "1078_current_owner": OUT / "P8_Y5_R10_1078_CURRENT_OWNER_PROOF_ATTEMPT.csv",
    "1079_narrow_current": OUT / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
    "1224_owner_clauses": OUT / "P8_Y5_R10_1224_OWNER_PROOF_CLAUSES.csv",
    "1224_weight_obstruction": OUT / "P8_Y5_R10_1224_SOURCE_WEIGHT_OBSTRUCTION_LEDGER.csv",
    "1229_source_contract": OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv",
    "1229_counterexamples": OUT / "P8_Y5_R10_1229_SOURCE_COUPLING_COUNTEREXAMPLE_LEDGER.csv",
    "1229_clause_audit": OUT / "P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv",
    "1387_action_weight": OUT / "P8_Y5_R10_1387_ACTION_WEIGHT_EXCLUSION_AUDIT.csv",
    "1387_beta_fill": OUT / "P8_Y5_R10_1387_DELTA_W_SOURCE_BETA_FIRST_FILL.csv",
    "1450_hilbert_label": OUT / "P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv",
    "1451_operator_grammar": OUT / "P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv",
    "1452_common_measure": OUT / "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv",
    "1453_current_source": OUT / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv",
    "1584_gr_runner": OUT / "P8_Y5_PARENT_QLOC_1584_GR_REDUCTION_RUNNER.csv",
}

NEEDLES = {
    "1593_doc": ["NEXT_1594_ACTION_WEIGHT_EXCLUSION_OR_BETA_SOURCE_ACQUISITION_VALIDATOR", "w_A"],
    "1593_validation": ["VAL1593_OVERALL", "PASS"],
    "1593_beta_rows": ["FBR1593_11_verdict", "FINITE_BETA_SOURCE_ROWS_READY_NONCLAIM"],
    "1593_source_residual": ["SWR1593_6_verdict", "SOURCE_RESIDUAL_VECTOR_READY_NONCLAIM"],
    "1066_source_scalar": ["SSE1066_5_verdict", "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED"],
    "1066_field_measure": ["FMQ1066_4_verdict", "NOT_PARENT_SIGNED"],
    "1078_object_language": ["OL1078_4_verdict", "OBJECT_LANGUAGE_NOT_SIGNED"],
    "1078_action_measure": ["AM1078_4_verdict", "ACTION_MEASURE_NOT_SIGNED"],
    "1078_current_owner": ["CO1078_4_verdict", "CURRENT_OWNER_NOT_SIGNED"],
    "1079_narrow_current": ["NCO1079_6_verdict", "NARROW_CURRENT_OWNER_PARTIAL_NOT_WEP_CLOSED"],
    "1224_owner_clauses": ["OWN1224_6_verdict", "SOURCE_WEIGHT_OWNER_PROOF_NOT_DERIVED"],
    "1224_weight_obstruction": ["OBS1224_0_wA_action_multiplier", "valid_for_claim"],
    "1229_source_contract": ["THM1229_2_countermodel", "OBSTRUCTION_ACTIVE"],
    "1229_counterexamples": ["CEX1229_0_action_multiplier", "ACTIVE"],
    "1229_clause_audit": ["CLC1229_8_verdict", "NOT_CLOSED"],
    "1387_action_weight": ["AWE1387_7_verdict", "COUNTEREXAMPLE_SURVIVES_FIRST_FILL_REQUIRED"],
    "1387_beta_fill": ["DWB1387_6_first_fill_verdict", "NONCLAIM_FIRST_FILL_READY"],
    "1450_hilbert_label": ["HT1450_6_verdict", "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED"],
    "1451_operator_grammar": ["OG1451_6_verdict", "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED"],
    "1452_common_measure": ["CMT1452_6_verdict", "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED"],
    "1453_current_source": ["CSO1453_7_verdict", "PARTIAL_THEOREM_NOT_CLOSED"],
    "1584_gr_runner": ["RUN1584_4_local_gr", "BLOCKED_NO_CLAIM"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1594_SOURCE_REGISTER.csv"
ACTION_WEIGHT_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1594_ACTION_WEIGHT_EXCLUSION_THEOREM_ATTEMPT.csv"
MEASURE_CURRENT_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1594_COMMON_MEASURE_CURRENT_AUDIT.csv"
BETA_VALIDATOR_SPEC = OUT / "P8_Y5_PARENT_QLOC_1594_BETA_ROW_VALIDATOR_SPEC.csv"
BETA_VALIDATOR_RESULTS = OUT / "P8_Y5_PARENT_QLOC_1594_BETA_ROW_VALIDATOR_RESULTS.csv"
SOURCE_QUEUE = OUT / "P8_Y5_PARENT_QLOC_1594_BETA_SOURCE_ACQUISITION_QUEUE.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1594_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1594_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1594_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1594_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1594_VALIDATION.csv"

COPY_TARGETS = {
    ACTION_WEIGHT_THEOREM: [
        QUARANTINE / "ACTION_WEIGHT_EXCLUSION_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_action_weight_exclusion_theorem_attempt_nonclaim_1594.csv",
    ],
    MEASURE_CURRENT_AUDIT: [
        QUARANTINE / "COMMON_MEASURE_CURRENT_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_common_measure_current_audit_nonclaim_1594.csv",
    ],
    BETA_VALIDATOR_SPEC: [
        QUARANTINE / "BETA_ROW_VALIDATOR_SPEC_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_beta_row_validator_spec_nonclaim_1594.csv",
    ],
    BETA_VALIDATOR_RESULTS: [
        QUARANTINE / "BETA_ROW_VALIDATOR_RESULTS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_beta_row_validator_results_nonclaim_1594.csv",
    ],
    SOURCE_QUEUE: [
        QUARANTINE / "BETA_SOURCE_ACQUISITION_QUEUE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_beta_source_acquisition_queue_nonclaim_1594.csv",
    ],
    RUNNER: [
        QUARANTINE / "RUNNER_REFUSAL_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_runner_refusal_nonclaim_1594.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_action_weight_validator_decision_nonclaim_1594.csv",
    ],
}


REQUIRED_BETA_FIELDS = [
    "same_parent_branch_id",
    "quantity",
    "definition",
    "required_units",
    "required_source",
    "observable_links",
    "source_path",
    "source_anchor",
    "extraction_method",
    "beta_convention",
    "arena_map",
    "current_status",
]


def false_flags() -> dict[str, bool]:
    return {
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_index, (source_key, source_path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1594_{source_index}_{source_key}",
                "source_path": rel(source_path),
                "exists": source_path.exists(),
                "needle_found": file_contains(source_path, NEEDLES[source_key]),
                "needles": "; ".join(NEEDLES[source_key]),
                "purpose": "action-weight exclusion theorem or beta source acquisition validator",
                **false_flags(),
            }
        )
    return rows


def action_weight_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "AWT1594_0_target",
            "exclude independent pre-variation source weights",
            "Allowed[S_matter] = sum_A S_A[Psi_A,e_obs(q),A_Q,theta_A] with no independent w_A S_A source/action multiplier.",
            "Would kill Delta_w_A, beta_w_A and the cleanest source-normalization obstruction.",
            "TARGET_SHARPENED",
            "requires parent grammar, action-measure and current-owner premises together",
        ),
        (
            "AWT1594_1_classical_EOM_rejection",
            "isolated classical equations cannot kill w_A",
            "delta(w_A S_A)/delta Psi_A=0 can have the same form as delta S_A/delta Psi_A=0 while delta(w_A S_A)/delta g = w_A T_A.",
            "Prevents fake derivation by free-fall/classical dynamics alone.",
            "SHORTCUT_REJECTED",
            "source variation still sees w_A",
        ),
        (
            "AWT1594_2_object_language",
            "no source-only slot",
            "A species-indexed inert scalar with no field/current/representation/geometry type should not be an admissible parent argument.",
            "Would make partial S_matter/partial w_A undefined rather than merely small.",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "absence of a slot is still a parent grammar theorem, not derived from covariance alone",
        ),
        (
            "AWT1594_3_common_action_measure",
            "single hbar/action-measure owner",
            "One parent action scale and matter measure would make independent exp(i w_A S_A/hbar_parent) factors inadmissible.",
            "Would kill relative action weights and species Jacobian source weights.",
            "CONDITIONAL_ROUTE_CLEAN_NOT_SIGNED",
            "no parent statistical/path-integral measure owner is signed",
        ),
        (
            "AWT1594_4_current_owner_limit",
            "Hilbert current before readout",
            "T_H is unique once one common action is fixed and varied before readout.",
            "Kills post-variation source rescalings conditionally.",
            "PARTIAL_THEOREM_ONLY",
            "T_H inherits w_A if w_A is already inside S_matter before variation",
        ),
        (
            "AWT1594_5_naturality_limit",
            "connected ordinary matter category",
            "Naturality can force a common scalar only if ordinary matter components are connected by parent morphisms.",
            "Helpful if signed, but disconnected simple components can carry independent constants.",
            "HELPFUL_CONDITIONAL_ONLY",
            "connectedness of ordinary matter category not derived",
        ),
        (
            "AWT1594_6_nonHilbert_bypass",
            "no non-Hilbert source bypass",
            "J_src = kappa T_Hilbert plus possible non-Hilbert currents must have all zeta_A zero/exact/projected-silent.",
            "Prevents spin/torsion/boundary/current bypass of the Hilbert theorem.",
            "PARALLEL_GATE_OPEN",
            "non-Hilbert current absence/silence not proven",
        ),
        (
            "AWT1594_7_verdict",
            "action-weight exclusion theorem",
            "No-source-only-slot + common action-measure + current owner + label forgetting + non-Hilbert silence would imply w_A=w_star or null-projected.",
            "The route is exact as a contract, but current corpus does not parent-sign it.",
            "ACTION_WEIGHT_EXCLUSION_NOT_DERIVED_VALIDATOR_REQUIRED",
            "use strict beta/source validator until the parent theorem closes",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "clause": clause,
            "formal_statement": statement,
            "would_close": would_close,
            "status": status,
            "blocking_gap": gap,
            "theorem_closed": False,
            **false_flags(),
        }
        for theorem_id, clause, statement, would_close, status, gap in rows
    ]


def measure_current_rows() -> list[dict[str, Any]]:
    rows = [
        ("CMC1594_0_single_action_scale", "one universal action scale/hbar", "FMQ1066/AM1078/CMT1452", "NOT_PARENT_SIGNED", "Delta_w_A cannot be set to zero"),
        ("CMC1594_1_species_blind_measure", "species-blind measure and Jacobian", "CMT1452 species Jacobian countermodel", "COUNTERMODEL_SURVIVES", "measure-induced weights retained"),
        ("CMC1594_2_label_forgetting", "source functor forgets species labels before coupling", "HT1450 conditional uniqueness", "CONDITIONAL_NOT_PARENT_DERIVED", "relative kappa_A can be formed if labels survive"),
        ("CMC1594_3_hilbert_current_owner", "Hilbert source is varied before readout", "NCO1079/CSO1453 exact conditional subtheorem", "CONDITIONAL_PARTIAL_ONLY", "post-variation rescaling controlled, pre-variation w_A survives"),
        ("CMC1594_4_no_nonhilbert_current", "no spin/torsion/boundary/non-Hilbert source bypass", "HT1450/CSO1453 non-Hilbert guard", "PARALLEL_GATE_OPEN", "zeta_A finite rows retained"),
        ("CMC1594_5_readout_order", "readout cannot retroactively redefine source", "SSE1066/NCO1079 variation-before-readout", "CONTRACT_WRITTEN_NOT_DERIVED", "readout tails retained"),
        ("CMC1594_6_common_G_absorption", "only common derivative-silent w_star can be absorbed into G_N", "CLC1229/DWB1387 measured-G guard", "GUARD_ACTIVE_INPUTS_MISSING", "relative or phi-dependent weights are physics"),
        ("CMC1594_7_verdict", "common measure/current owner", "CMT1452/CSO1453 verdicts", "COMMON_MEASURE_CURRENT_NOT_DERIVED", "strict finite-row validation required"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "required_clause": clause,
            "source_basis": source_basis,
            "current_status": status,
            "effect_if_open": effect,
            "clause_signed": False,
            **false_flags(),
        }
        for audit_id, clause, source_basis, status, effect in rows
    ]


def beta_validator_spec_rows() -> list[dict[str, Any]]:
    rows = [
        ("BVS1594_0_branch", "same_parent_branch_id", "must equal MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428", "reject mismatched branch or blank branch"),
        ("BVS1594_1_identity", "quantity;definition", "must declare source/test leg, product, weight, kernel, or tail with explicit convention", "reject vague coupling symbols"),
        ("BVS1594_2_units", "required_units", "must be concrete beta, dimensionless, kernel, or arena residual units", "reject missing or placeholder units"),
        ("BVS1594_3_source", "source_path;source_anchor;extraction_method", "must cite a local source and how the value/theorem was obtained", "reject missing, toy, proxy, or unsourced rows"),
        ("BVS1594_4_beta_convention", "beta_convention", "must state canonical normalization and whether source/test legs are already packed", "reject linear-coupling shortcuts"),
        ("BVS1594_5_arena", "arena_map;observable_links", "must name R10/PPN/WEP/clock/orbital/Newton map and kernel role", "reject no-arena rows"),
        ("BVS1594_6_status", "current_status", "must be SOURCE_BACKED_NUMERIC, THEOREM_ZERO_PARENT_SIGNED, or EXPLICIT_BOUND_SOURCE_BACKED", "reject MISSING, TEMPLATE, NONCLAIM, TOY, PLACEHOLDER"),
        ("BVS1594_7_flags", "valid_for_claim;claim_allowed;score_ready", "may be true only if all previous gates pass", "default false"),
        ("BVS1594_8_no_absorption", "measured_G_guard", "must prove common derivative-silent factor before any G_N absorption", "reject relative or phi-dependent absorption"),
        ("BVS1594_9_verdict", "validator policy", "strict validator is ready and should be used before every local score", "current 1593 beta rows are expected to fail"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "spec_id": spec_id,
            "field_or_gate": field,
            "requirement": requirement,
            "failure_rule": failure_rule,
            **false_flags(),
        }
        for spec_id, field, requirement, failure_rule in rows
    ]


def validate_beta_row(row: dict[str, str]) -> tuple[str, str, str]:
    missing_fields = [field for field in REQUIRED_BETA_FIELDS if not row.get(field, "").strip()]
    bad_markers = []
    joined = " ".join(row.get(field, "") for field in row)
    for marker in ["MISSING", "TEMPLATE", "TOY", "PLACEHOLDER", "NONCLAIM"]:
        if marker in joined.upper():
            bad_markers.append(marker)
    if row.get("same_parent_branch_id") != BRANCH_ID:
        bad_markers.append("BRANCH_ID_MISMATCH")
    if row.get("valid_for_claim", "False") != "True":
        bad_markers.append("VALID_FOR_CLAIM_FALSE")
    if missing_fields or bad_markers:
        return "REJECT", ";".join(missing_fields) or "none", ";".join(sorted(set(bad_markers))) or "none"
    return "ACCEPT", "none", "none"


def beta_validator_result_rows() -> list[dict[str, Any]]:
    rows = []
    for index, row in enumerate(read_csv(OUT / "P8_Y5_PARENT_QLOC_1593_FINITE_BETA_SOURCE_ROWS.csv")):
        result, missing_fields, bad_markers = validate_beta_row(row)
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "validation_id": f"BVR1594_{index}_{row.get('row_id', 'unknown')}",
                "input_row_id": row.get("row_id", ""),
                "quantity": row.get("quantity", ""),
                "input_status": row.get("current_status", ""),
                "validator_result": result,
                "missing_required_fields": missing_fields,
                "bad_markers": bad_markers,
                "reason": "current row is a nonclaim first-fill/template row; not source-backed",
                **false_flags(),
            }
        )
    accepted = [row for row in rows if row["validator_result"] == "ACCEPT"]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "validation_id": "BVR1594_VERDICT",
            "input_row_id": "aggregate_1593_finite_beta_rows",
            "quantity": "all_beta_rows",
            "input_status": "aggregate",
            "validator_result": "NO_ACCEPTED_BETA_ROWS" if not accepted else "UNEXPECTED_ACCEPTED_ROWS",
            "missing_required_fields": "source_path;source_anchor;extraction_method;beta_convention;arena_map",
            "bad_markers": "MISSING;NONCLAIM;VALID_FOR_CLAIM_FALSE",
            "reason": "all current rows correctly fail strict validator until source-backed theorem/numeric inputs exist",
            **false_flags(),
        }
    )
    return rows


def source_queue_rows() -> list[dict[str, Any]]:
    rows = [
        ("BSQ1594_0_beta_source", "beta_source", "source worldtube plus matter descent map", "R10;Newton;WEP", "high", "source/test product cannot score without source leg"),
        ("BSQ1594_1_beta_test", "beta_test", "test-body matter action and material response map", "R10;WEP;clock;orbital", "high", "source/test product cannot score without test leg"),
        ("BSQ1594_2_Delta_w_A", "Delta_w_A", "action-weight exclusion theorem or finite source/material bound", "Newton;common matter;WEP", "highest", "kills or quantifies w_A gremlin"),
        ("BSQ1594_3_beta_w", "beta_w_source;beta_w_test", "phi-dependence of source/test action weights", "R10;PPN;WEP", "high", "finite scalar exchange if w_A(phi) survives"),
        ("BSQ1594_4_K_arena", "K_arena(lambda)", "arena kernel with mu_m2, source/test geometry and no double counting", "R10;PPN;clock;orbital", "medium", "data scoring waits until beta legs exist"),
        ("BSQ1594_5_epsilon_tail", "epsilon_tail", "boundary/readout/projector/non-Hilbert/CDB tail envelope", "all local arenas", "high", "prevents fake zero by ignoring tails"),
        ("BSQ1594_6_measured_G_guard", "measured_G_guard", "common derivative-silent proof for any absorbed factor", "Newton;PPN;WEP", "highest", "blocks calibration cheating"),
        ("BSQ1594_7_verdict", "acquisition_order", "prove action-weight exclusion first; otherwise acquire beta/Delta_w rows before arena kernels", "all", "decision", "least-scrutiny order selected"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "queue_id": queue_id,
            "quantity": quantity,
            "required_source": required_source,
            "arena_links": arena_links,
            "priority": priority,
            "why_next": why_next,
            **false_flags(),
        }
        for queue_id, quantity, required_source, arena_links, priority, why_next in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1594_0_action_weight_theorem", "accept w_A exclusion only if object-language, action-measure, current-owner, label-forgetting and non-Hilbert gates close", "AWT1594 verdict is not derived", "REJECT_ACTION_WEIGHT_ZERO_CLAIM", "finite Delta_w/beta_w rows remain mandatory"),
        ("RUN1594_1_beta_validator", "accept beta rows only if strict validator returns ACCEPT", "BVR1594 verdict has no accepted beta rows", "REJECT_ALL_CURRENT_BETA_ROWS", "no local empirical scoring"),
        ("RUN1594_2_measured_G", "accept G_N absorption only for common derivative-silent w_star", "relative/phi/source weights remain unsourced", "REJECT_MEASURED_G_ABSORPTION_SHORTCUT", "Newton/common matter blocked"),
        ("RUN1594_3_local_GR", "accept local GR only after action weights/beta/current/conservation/Newton gates close", "1584 and 1593 still block local GR", "REJECT_LOCAL_GR_REENTRY", "continue derivation/source acquisition"),
        ("RUN1594_4_next", "next run should either prove action-measure owner or source first beta rows", "validator exists but has no accepted inputs", "WAIT_FOR_THEOREM_OR_SOURCE_ROWS", "do not score yet"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "acceptance_rule": acceptance_rule,
            "input_state": input_state,
            "runner_result": result,
            "effect": effect,
            **false_flags(),
        }
        for runner_id, acceptance_rule, input_state, result, effect in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1594_0_action_weight", "action-weight exclusion theorem", "BLOCKED_NO_CLAIM", "parent grammar/action-measure/current-owner package not signed"),
        ("GATE1594_1_beta_validation", "finite beta/source row score", "BLOCKED_NO_CLAIM", "strict validator accepts no current beta rows"),
        ("GATE1594_2_measured_G", "absorb source weights into measured G_N", "BLOCKED_NO_CLAIM", "relative or phi-dependent weights are physics unless common derivative-silent proof exists"),
        ("GATE1594_3_Newton", "Newton source normalization", "BLOCKED_NO_CLAIM", "Delta_w/common current gates open"),
        ("GATE1594_4_R10_PPN_WEP", "R10/PPN/WEP score", "BLOCKED_NO_CLAIM", "beta legs, kernels and tails are missing"),
        ("GATE1594_5_local_GR", "local GR reduction", "BLOCKED_NO_CLAIM", "source/coupling/conservation gates do not close together"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **false_flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1594_0_theorem_status",
            "ACTION_WEIGHT_EXCLUSION_NOT_DERIVED",
            "all proof routes are sharp but remain unsigned; current owner kills post-variation tricks only, not pre-variation w_A",
            "keep w_A as live finite source residual",
        ),
        (
            "DEC1594_1_validator_status",
            "STRICT_BETA_VALIDATOR_NOW_EXISTS",
            "current beta rows fail because they are templates lacking source paths, anchors, extraction method, beta convention and arena maps",
            "run validator before any local R10/PPN/WEP/clock/orbital score",
        ),
        (
            "DEC1594_2_best_route",
            "SOURCE_FIRST_ROWS_BEFORE_ARENA_KERNELS",
            "arena kernels are useless until beta_source, beta_test, Delta_w and measured-G guard have source-backed rows or theorem-zero certificates",
            "source beta/Delta_w rows or prove action-measure owner next",
        ),
        (
            "DEC1594_3_next",
            "NEXT_1595_FIRST_SOURCE_BACKED_BETA_OR_ACTION_MEASURE_OWNER_REOPEN",
            "the next useful checkpoint should either close the parent action-measure owner or fill the first source-backed beta/Delta_w row that the validator can inspect",
            "attempt action-measure owner one more time from parent primitives, otherwise build first acquisition row",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            **false_flags(),
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1595-Y5-R2FR-first-source-backed-beta-or-action-measure-owner-reopen.md",
            "script": "scripts/Y5_R2FR_first_source_backed_beta_or_action_measure_owner_reopen.py",
            "objective": "try once more to derive the parent action-measure owner from MTS primitives; if it still fails, create the first source-backed finite beta/Delta_w acquisition row and run the 1594 validator against it",
            "success_condition": "parent-signed action-measure owner that kills w_A, or at least one beta/Delta_w row that passes schema/provenance but remains nonclaim until arena bounds exist",
            "do_not": "do not score local tests from templates, do not absorb relative weights into measured G, do not edit formalization-workbench or GitHub",
            **false_flags(),
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def generated_flags_false(generated_csvs: list[Path]) -> bool:
    flag_columns = {"score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "clause_signed", "theorem_closed"}
    for csv_path in generated_csvs:
        for row in read_csv(csv_path):
            for flag_column in flag_columns.intersection(row):
                if row[flag_column] != "False":
                    return False
    return True


def formalization_scope_clean(generated_csvs: list[Path]) -> bool:
    if any(FORMALIZATION in csv_path.parents for csv_path in generated_csvs):
        return False
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return True
    if result.returncode != 0:
        return True
    return len([line for line in result.stdout.splitlines() if line.strip()]) == 0


def has_1594_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1594" in csv_path.name for csv_path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    theorem = read_csv(ACTION_WEIGHT_THEOREM)
    measure = read_csv(MEASURE_CURRENT_AUDIT)
    spec = read_csv(BETA_VALIDATOR_SPEC)
    results = read_csv(BETA_VALIDATOR_RESULTS)
    queue = read_csv(SOURCE_QUEUE)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    checks = [
        ("VAL1594_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1594 source paths exist"),
        ("VAL1594_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all 1594 source needles found"),
        (
            "VAL1594_2_action_weight_not_derived",
            any(row["theorem_id"] == "AWT1594_7_verdict" and row["status"] == "ACTION_WEIGHT_EXCLUSION_NOT_DERIVED_VALIDATOR_REQUIRED" for row in theorem),
            "action-weight exclusion theorem remains unsigned",
        ),
        (
            "VAL1594_3_measure_current_not_derived",
            any(row["audit_id"] == "CMC1594_7_verdict" and row["current_status"] == "COMMON_MEASURE_CURRENT_NOT_DERIVED" for row in measure),
            "common measure/current owner remains unsigned",
        ),
        (
            "VAL1594_4_validator_spec_complete",
            len(spec) >= 10 and any(row["spec_id"] == "BVS1594_9_verdict" for row in spec),
            "strict beta validator policy is present",
        ),
        (
            "VAL1594_5_validator_rejects_current_rows",
            any(row["validation_id"] == "BVR1594_VERDICT" and row["validator_result"] == "NO_ACCEPTED_BETA_ROWS" for row in results)
            and all(row["validator_result"] != "ACCEPT" for row in results),
            "current 1593 beta rows are rejected as nonclaim templates",
        ),
        (
            "VAL1594_6_acquisition_queue_present",
            any(row["queue_id"] == "BSQ1594_7_verdict" for row in queue)
            and any(row["quantity"] == "Delta_w_A" for row in queue),
            "beta/Delta_w acquisition queue is present",
        ),
        (
            "VAL1594_7_runner_rejects_claims",
            any(row["runner_result"] == "REJECT_ACTION_WEIGHT_ZERO_CLAIM" for row in runner)
            and any(row["runner_result"] == "REJECT_ALL_CURRENT_BETA_ROWS" for row in runner)
            and any(row["runner_result"] == "REJECT_MEASURED_G_ABSORPTION_SHORTCUT" for row in runner),
            "runner refuses theorem, beta and measured-G shortcuts",
        ),
        (
            "VAL1594_8_claim_gates_closed",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in gates),
            "all 1594 claim gates remain closed",
        ),
        (
            "VAL1594_9_decision_next",
            any(row["decision"] == "NEXT_1595_FIRST_SOURCE_BACKED_BETA_OR_ACTION_MEASURE_OWNER_REOPEN" for row in decisions),
            "decision selects action-measure owner reopen or first source-backed beta row",
        ),
        ("VAL1594_10_csv_parse", all(len(read_csv(csv_path)) > 0 for csv_path in generated_csvs), "all generated 1594 CSVs parse cleanly"),
        ("VAL1594_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated claim/prediction/theorem flags remain false"),
        ("VAL1594_12_no_raw_accepted", not has_1594_rows(RAB_RAW) and not has_1594_rows(RAB_ACCEPTED), "no 1594 rows written to raw/accepted finite directories"),
        ("VAL1594_13_branch_copies", all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths), "branch/quarantine nonclaim copies written"),
        ("VAL1594_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1594_15_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1594 paths are outside formalization-workbench; git status is clean when available"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1594_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1594 action-weight exclusion or beta source acquisition validator validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    measure: list[dict[str, Any]],
    spec: list[dict[str, Any]],
    results: list[dict[str, Any]],
    queue: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1594 - R2/fR Action-Weight Exclusion Or Beta Source Acquisition Validator",
                "## Verdict\n"
                "- 1594 tries to kill the pre-variation `w_A` source/action-weight counterexample directly. The proof route is sharp, but still **not parent-signed**.\n"
                "- Classical matter equations do not remove `w_A`: the metric/Hilbert variation inherits it. Current-owner arguments kill post-variation rescalings only after a common action is fixed; they do not kill weights already inside `S_matter`.\n"
                "- The missing theorem package is now precise: no-source-only parent grammar, common action measure, source-label forgetting, Hilbert/current owner, non-Hilbert silence, readout order, and common-`G_N` absorption guard.\n"
                "- Since the theorem still does not close, 1594 adds a strict beta-row validator. It rejects every current 1593 beta row because they are nonclaim templates lacking source paths, anchors, extraction method, beta convention, and arena maps.\n"
                "- No local-GR, Newton, PPN, R10, WEP, clock, orbital, beta, action-weight, measured-`G`, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Action-Weight Exclusion Theorem Attempt",
                md_table(theorem, ["theorem_id", "clause", "formal_statement", "would_close", "status", "blocking_gap"]),
                "## Common Measure Current Audit",
                md_table(measure, ["audit_id", "required_clause", "source_basis", "current_status", "effect_if_open"]),
                "## Beta Validator Spec",
                md_table(spec, ["spec_id", "field_or_gate", "requirement", "failure_rule"]),
                "## Beta Validator Results",
                md_table(results, ["validation_id", "input_row_id", "quantity", "input_status", "validator_result", "missing_required_fields", "bad_markers"]),
                "## Beta Source Acquisition Queue",
                md_table(queue, ["queue_id", "quantity", "required_source", "arena_links", "priority", "why_next"]),
                "## Runner Refusal",
                md_table(runner, ["runner_id", "acceptance_rule", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    theorem = action_weight_theorem_rows()
    measure = measure_current_rows()
    spec = beta_validator_spec_rows()
    results = beta_validator_result_rows()
    queue = source_queue_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        ACTION_WEIGHT_THEOREM,
        MEASURE_CURRENT_AUDIT,
        BETA_VALIDATOR_SPEC,
        BETA_VALIDATOR_RESULTS,
        SOURCE_QUEUE,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(ACTION_WEIGHT_THEOREM, theorem)
    write_csv(MEASURE_CURRENT_AUDIT, measure)
    write_csv(BETA_VALIDATOR_SPEC, spec)
    write_csv(BETA_VALIDATOR_RESULTS, results)
    write_csv(SOURCE_QUEUE, queue)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, theorem, measure, spec, results, queue, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
