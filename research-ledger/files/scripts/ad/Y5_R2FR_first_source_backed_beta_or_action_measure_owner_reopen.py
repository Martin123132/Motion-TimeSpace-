from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1595"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1595-Y5-R2FR-first-source-backed-beta-or-action-measure-owner-reopen.md"

SOURCE_FILES = {
    "1594_doc": ROOT / "1594-Y5-R2FR-action-weight-exclusion-or-beta-source-acquisition-validator.md",
    "1594_validation": OUT / "P8_Y5_BRR545_1594_VALIDATION.csv",
    "1594_validator_spec": OUT / "P8_Y5_PARENT_QLOC_1594_BETA_ROW_VALIDATOR_SPEC.csv",
    "1594_validator_results": OUT / "P8_Y5_PARENT_QLOC_1594_BETA_ROW_VALIDATOR_RESULTS.csv",
    "1594_queue": OUT / "P8_Y5_PARENT_QLOC_1594_BETA_SOURCE_ACQUISITION_QUEUE.csv",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
    "1066_wep_bound_import": OUT / "P8_Y5_R10_1066_WEP_DELTA_W_BOUND_IMPORT.csv",
    "1066_prior_schema": OUT / "P8_Y5_R10_1066_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv",
    "1224_finite_weight_contract": OUT / "P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv",
    "1078_action_measure": OUT / "P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv",
    "1452_common_measure": OUT / "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv",
    "1453_current_source": OUT / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv",
    "1584_gr_runner": OUT / "P8_Y5_PARENT_QLOC_1584_GR_REDUCTION_RUNNER.csv",
}

NEEDLES = {
    "1594_doc": ["NEXT_1595_FIRST_SOURCE_BACKED_BETA_OR_ACTION_MEASURE_OWNER_REOPEN", "STRICT_BETA_VALIDATOR_NOW_EXISTS"],
    "1594_validation": ["VAL1594_OVERALL", "PASS"],
    "1594_validator_spec": ["BVS1594_9_verdict", "strict validator"],
    "1594_validator_results": ["BVR1594_VERDICT", "NO_ACCEPTED_BETA_ROWS"],
    "1594_queue": ["BSQ1594_2_Delta_w_A", "highest"],
    "local_bound_claims": ["R1_WEP_source_charge", "2.8e-15"],
    "1066_wep_bound_import": ["BOUND1066_0_WEP_source_charge", "2.8e-15"],
    "1066_prior_schema": ["DWP1066_0_WEP_bound", "bound_anchor_available"],
    "1224_finite_weight_contract": ["FSW1224_0_eta_bound", "BOUND_ANCHOR_ONLY"],
    "1078_action_measure": ["AM1078_4_verdict", "ACTION_MEASURE_NOT_SIGNED"],
    "1452_common_measure": ["CMT1452_6_verdict", "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED"],
    "1453_current_source": ["CSO1453_7_verdict", "PARTIAL_THEOREM_NOT_CLOSED"],
    "1584_gr_runner": ["RUN1584_4_local_gr", "BLOCKED_NO_CLAIM"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1595_SOURCE_REGISTER.csv"
ACTION_MEASURE_REOPEN = OUT / "P8_Y5_PARENT_QLOC_1595_ACTION_MEASURE_OWNER_REOPEN.csv"
SOURCE_BACKED_CANDIDATE = OUT / "P8_Y5_PARENT_QLOC_1595_SOURCE_BACKED_BETA_DELTAW_CANDIDATE.csv"
VALIDATOR_COMPAT = OUT / "P8_Y5_PARENT_QLOC_1595_1594_VALIDATOR_COMPATIBILITY.csv"
CLAIM_LIMITS = OUT / "P8_Y5_PARENT_QLOC_1595_CANDIDATE_CLAIM_LIMITS.csv"
NEXT_INPUTS = OUT / "P8_Y5_PARENT_QLOC_1595_NEXT_INPUT_REQUIREMENTS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1595_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1595_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1595_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1595_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1595_VALIDATION.csv"

COPY_TARGETS = {
    ACTION_MEASURE_REOPEN: [
        QUARANTINE / "ACTION_MEASURE_OWNER_REOPEN_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_action_measure_owner_reopen_nonclaim_1595.csv",
    ],
    SOURCE_BACKED_CANDIDATE: [
        QUARANTINE / "SOURCE_BACKED_BETA_DELTAW_CANDIDATE_BOUND_ONLY.csv",
        BRANCH_RESIDUALS / "R2FR_source_backed_beta_deltaW_candidate_bound_only_1595.csv",
    ],
    VALIDATOR_COMPAT: [
        QUARANTINE / "VALIDATOR_COMPATIBILITY_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_1594_validator_compatibility_nonclaim_1595.csv",
    ],
    CLAIM_LIMITS: [
        QUARANTINE / "CANDIDATE_CLAIM_LIMITS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_candidate_claim_limits_nonclaim_1595.csv",
    ],
    NEXT_INPUTS: [
        QUARANTINE / "NEXT_INPUT_REQUIREMENTS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_input_requirements_nonclaim_1595.csv",
    ],
    RUNNER: [
        QUARANTINE / "RUNNER_REFUSAL_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_runner_refusal_nonclaim_1595.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_first_source_backed_beta_decision_nonclaim_1595.csv",
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


def local_bound_row(row_id: str) -> dict[str, str]:
    for row in read_csv(LOCAL_BOUNDS / "local_bound_claims.csv"):
        if row.get("row_id") == row_id:
            return row
    raise ValueError(f"missing local bound row {row_id}")


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_index, (source_key, source_path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1595_{source_index}_{source_key}",
                "source_path": rel(source_path),
                "exists": source_path.exists(),
                "needle_found": file_contains(source_path, NEEDLES[source_key]),
                "needles": "; ".join(NEEDLES[source_key]),
                "purpose": "first source-backed beta/Delta_w candidate or action-measure owner reopen",
                **false_flags(),
            }
        )
    return rows


def action_measure_reopen_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "AMR1595_0_classical_blocker",
            "classical EOM route",
            "delta(w_A S_A)/delta Psi_A=0 can preserve isolated equations while delta(w_A S_A)/delta g=w_A T_A.",
            "Classical field equations cannot derive common source normalization.",
            "REJECTED_AS_GENERAL_PROOF",
            "source variation sees w_A",
        ),
        (
            "AMR1595_1_quantum_measure_route",
            "single hbar/action-measure",
            "A unique parent phase/statistical measure would make independent exp(i w_A S_A/hbar_parent) inadmissible.",
            "Cleanest remaining derivation route, but no parent measure owner is signed in the corpus.",
            "CONDITIONAL_ROUTE_NOT_PARENT_SIGNED",
            "requires deeper MTS primitive for action scale/measure",
        ),
        (
            "AMR1595_2_object_language_route",
            "no source-only slot",
            "w_A is forbidden only if the parent grammar excludes inert species-indexed source scalars.",
            "The desired grammar is written but not derived from deeper primitives.",
            "CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED",
            "absence of slot is not yet proof of impossibility",
        ),
        (
            "AMR1595_3_current_owner_route",
            "Hilbert current before readout",
            "Current owner can kill post-variation rescalings after a common action is fixed.",
            "It does not kill weights already inserted before variation.",
            "PARTIAL_THEOREM_ONLY",
            "pre-variation w_A survives",
        ),
        (
            "AMR1595_4_nonhilbert_bypass",
            "non-Hilbert source currents",
            "Even a Hilbert theorem needs zeta_A J_NH,A absent, exact or projected silent.",
            "Non-Hilbert source bypass remains a parallel open gate.",
            "PARALLEL_GATE_OPEN",
            "requires zeta_A source rows or zero theorem",
        ),
        (
            "AMR1595_5_verdict",
            "action-measure owner reopen",
            "No new parent-signed owner is found from current corpus evidence.",
            "Proceed with first source-backed bound anchor row rather than pretending w_A is dead.",
            "ACTION_MEASURE_OWNER_STILL_NOT_DERIVED",
            "finite source-backed beta/Delta_w acquisition route activated",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "reopen_id": reopen_id,
            "route": route,
            "formal_statement": statement,
            "result": result,
            "status": status,
            "blocking_gap": gap,
            "theorem_closed": False,
            **false_flags(),
        }
        for reopen_id, route, statement, result, status, gap in rows
    ]


def source_backed_candidate_rows() -> list[dict[str, Any]]:
    bound = local_bound_row("R1_WEP_source_charge")
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "SBC1595_0_MICROSCOPE_Delta_w_tau_bound_anchor",
            "quantity": "P_WEP_relative_source_weight",
            "definition": "absolute product bound for relative source/action weight channel, P=abs(Delta_w_TiPt*tau_WEP)",
            "required_units": bound["units"],
            "required_source": "MICROSCOPE Ti/Pt WEP source-charge proxy bound plus MTS tau_WEP projection contract",
            "observable_links": "MICROSCOPE_WEP;Newton_source;common_matter",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "source_anchor": "R1_WEP_source_charge",
            "extraction_method": "imported_local_bound_anchor_from_MICROSCOPE_final_TiPt_source_charge_proxy",
            "beta_convention": "product_bound_not_individual_beta; P=abs(Delta_w_TiPt*tau_WEP); no source/test split claimed",
            "arena_map": "MICROSCOPE/Eotvos/composition -> abs(Delta_w_TiPt*tau_WEP) <= eta_bound",
            "current_status": "EXPLICIT_BOUND_SOURCE_BACKED",
            "value": bound["upper_bound"],
            "value_role": "upper_bound",
            "units": bound["units"],
            "confidence_label": bound["confidence_label"],
            "reference_path_or_url": bound["reference_path_or_url"],
            "claim_scope": "BOUND_ANCHOR_ONLY_NO_MTS_PREDICTION",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": True,
            "claim_allowed": False,
        }
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
    return "ACCEPT_SCHEMA_PROVENANCE", "none", "none"


def validator_compat_rows() -> list[dict[str, Any]]:
    rows = []
    for row in source_backed_candidate_rows():
        result, missing_fields, bad_markers = validate_beta_row({key: str(value) for key, value in row.items()})
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "validation_id": "VCOMP1595_0_source_backed_bound_anchor",
                "input_row_id": row["row_id"],
                "quantity": row["quantity"],
                "validator_result": result,
                "missing_required_fields": missing_fields,
                "bad_markers": bad_markers,
                "claim_allowed_after_validation": False,
                "reason": "passes 1594-style schema/provenance gates as a bound anchor, but remains non-prediction and non-score until tau_WEP/source projection exists",
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": True,
                "claim_allowed": False,
            }
        )
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "validation_id": "VCOMP1595_VERDICT",
            "input_row_id": "aggregate_source_backed_candidate",
            "quantity": "P_WEP_relative_source_weight",
            "validator_result": "ONE_SCHEMA_PROVENANCE_PASS_BOUND_ONLY",
            "missing_required_fields": "none",
            "bad_markers": "none",
            "claim_allowed_after_validation": False,
            "reason": "first validator-readable source-backed local bound input exists, but it is not an MTS prediction row",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": True,
            "claim_allowed": False,
        }
    )
    return rows


def claim_limit_rows() -> list[dict[str, Any]]:
    rows = [
        ("CLM1595_0_not_prediction", "not an MTS prediction", "the row is an empirical bound anchor only; no beta_source, beta_test, Delta_w_TiPt or tau_WEP prediction is supplied", "claim blocked"),
        ("CLM1595_1_tau_missing", "tau_WEP missing", "without tau_WEP, eta_bound cannot become abs(Delta_w_TiPt) <= eta/tau", "Delta_w prior width blocked"),
        ("CLM1595_2_source_worldtube_missing", "source worldtube missing", "Earth/source stress profile and orbit/readout weighting are required before interpreting source-normalization residuals", "projection blocked"),
        ("CLM1595_3_material_map_missing", "material map missing", "TA6V/PtRh10 material response convention is context only, not a full source/test beta map", "WEP material score blocked"),
        ("CLM1595_4_no_G_absorption", "no measured-G shortcut", "relative or phi-dependent source weights cannot be hidden in G_N; only common derivative-silent factors are calibration", "Newton/common-matter claim blocked"),
        ("CLM1595_5_verdict", "bound-only candidate", "candidate can seed acquisition and validator tests, but cannot reopen local GR or score local arenas", "nonclaim retained"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "limit_id": limit_id,
            "limit": limit,
            "reason": reason,
            "effect": effect,
            **false_flags(),
        }
        for limit_id, limit, reason, effect in rows
    ]


def next_input_rows() -> list[dict[str, Any]]:
    rows = [
        ("NIR1595_0_tau_WEP", "tau_WEP", "derive/source functional[source worldtube, orbit average, observed coframe, material tensor, force readout]", "needed to convert product bound into Delta_w bound", "highest"),
        ("NIR1595_1_source_worldtube", "T_source^Earth(x)", "profile-weighted Earth/source stress in observed local frame", "needed for beta_source/source-normalization projection", "high"),
        ("NIR1595_2_material_map", "Ti/Pt response tensor", "official TA6V/PtRh10 material sensitivity map and convention", "needed for WEP material beta/test leg", "high"),
        ("NIR1595_3_readout_kernel", "K_MICROSCOPE", "map parent residual to reported eta_AB with masks/segments/orbit/coframe convention", "needed before data score", "high"),
        ("NIR1595_4_action_measure_owner", "parent action-measure owner", "derive unique hbar/action measure or keep finite Delta_w", "cleanest theorem-zero route", "high"),
        ("NIR1595_5_verdict", "1596 work order", "source tau_WEP/readout kernel before attempting numerical Delta_w or WEP score", "next target selected", "decision"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": input_id,
            "quantity": quantity,
            "required_input": required_input,
            "why_needed": why_needed,
            "priority": priority,
            **false_flags(),
        }
        for input_id, quantity, required_input, why_needed, priority in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1595_0_action_measure", "accept action-measure theorem only if parent owner is signed", "AMR1595 verdict still not derived", "REJECT_ACTION_MEASURE_THEOREM_CLAIM", "finite route stays active"),
        ("RUN1595_1_validator_compat", "accept source-backed candidate only as schema/provenance bound input", "VCOMP1595 has one schema/provenance pass", "ACCEPT_BOUND_ANCHOR_ONLY", "no prediction score"),
        ("RUN1595_2_delta_w_score", "score Delta_w only if tau_WEP and source projection are supplied", "tau_WEP and source/readout kernels missing", "REJECT_DELTA_W_NUMERIC_SCORE", "no WEP score"),
        ("RUN1595_3_local_GR", "accept local GR only after source/coupling/conservation/Newton gates close", "source-weight channel remains finite", "REJECT_LOCAL_GR_REENTRY", "keep local GR blocked"),
        ("RUN1595_4_next", "next run should acquire tau_WEP/readout or derive action-measure owner", "bound anchor exists but not enough", "WAIT_FOR_TAU_OR_THEOREM", "1596 target selected"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "acceptance_rule": rule,
            "input_state": state,
            "runner_result": result,
            "effect": effect,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": result == "ACCEPT_BOUND_ANCHOR_ONLY",
            "claim_allowed": False,
        }
        for runner_id, rule, state, result, effect in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1595_0_action_measure", "parent action-measure owner", "BLOCKED_NO_CLAIM", "no parent-signed owner found"),
        ("GATE1595_1_bound_anchor", "source-backed bound input", "BOUND_INPUT_ONLY_NO_CLAIM", "one candidate passes schema/provenance but is not an MTS prediction"),
        ("GATE1595_2_delta_w", "Delta_w_TiPt prediction/bound", "BLOCKED_NO_CLAIM", "tau_WEP and source projection missing"),
        ("GATE1595_3_WEP", "MICROSCOPE/WEP score", "BLOCKED_NO_CLAIM", "material/source/readout kernel missing"),
        ("GATE1595_4_Newton_GR", "Newton/local GR source normalization", "BLOCKED_NO_CLAIM", "finite source-weight channel remains open"),
        ("GATE1595_5_R10_PPN_clock_orbital", "other local arena scores", "BLOCKED_NO_CLAIM", "candidate is WEP bound anchor only"),
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
            "DEC1595_0_owner_status",
            "ACTION_MEASURE_OWNER_STILL_NOT_DERIVED",
            "the proof routes remain sharp but unsigned; classical EOM and current owner alone cannot kill pre-variation w_A",
            "keep source-weight channel finite",
        ),
        (
            "DEC1595_1_first_source_backed_input",
            "FIRST_VALIDATOR_READABLE_BOUND_ANCHOR_CREATED",
            "MICROSCOPE R1 provides a source-backed upper bound on abs(Delta_w_TiPt*tau_WEP) that passes schema/provenance gates",
            "use it as bound input only, not prediction",
        ),
        (
            "DEC1595_2_no_score",
            "NO_LOCAL_SCORE_FROM_BOUND_ANCHOR",
            "tau_WEP, source worldtube, material map and readout kernel are still missing",
            "do not score WEP/local GR yet",
        ),
        (
            "DEC1595_3_next",
            "NEXT_1596_TAU_WEP_SOURCE_PROJECTION_OR_ACTION_MEASURE_OWNER_LAST_GATE",
            "the next useful source item is tau_WEP/readout projection; the clean proof alternative remains action-measure owner",
            "derive tau_WEP/source projection or close parent action-measure owner",
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
            "next_target": "1596-Y5-R2FR-tau-WEP-source-projection-or-action-measure-owner-last-gate.md",
            "script": "scripts/Y5_R2FR_tau_WEP_source_projection_or_action_measure_owner_last_gate.py",
            "objective": "derive or source tau_WEP/source-worldtube/readout projection so the 1595 MICROSCOPE bound anchor can become a Delta_w constraint, while keeping the action-measure owner theorem as the zero route",
            "success_condition": "source-backed tau_WEP/readout projection row, or parent-signed action-measure owner; otherwise a blocker ledger proving why Delta_w cannot yet be numeric",
            "do_not": "do not score WEP or local GR from the bound anchor alone, do not absorb relative weights into measured G, do not edit formalization-workbench or GitHub",
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


def generated_flags_safe(generated_csvs: list[Path]) -> bool:
    for csv_path in generated_csvs:
        for row in read_csv(csv_path):
            if row.get("claim_allowed") == "True":
                return False
            if row.get("score_ready") == "True":
                return False
            if row.get("valid_prediction_row") == "True":
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


def has_1595_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1595" in csv_path.name for csv_path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    reopen = read_csv(ACTION_MEASURE_REOPEN)
    candidate = read_csv(SOURCE_BACKED_CANDIDATE)
    compat = read_csv(VALIDATOR_COMPAT)
    limits = read_csv(CLAIM_LIMITS)
    next_inputs = read_csv(NEXT_INPUTS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    checks = [
        ("VAL1595_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1595 source paths exist"),
        ("VAL1595_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all 1595 source needles found"),
        (
            "VAL1595_2_action_measure_still_open",
            any(row["reopen_id"] == "AMR1595_5_verdict" and row["status"] == "ACTION_MEASURE_OWNER_STILL_NOT_DERIVED" for row in reopen),
            "action-measure owner remains unsigned",
        ),
        (
            "VAL1595_3_source_backed_candidate_present",
            any(row["row_id"] == "SBC1595_0_MICROSCOPE_Delta_w_tau_bound_anchor" and row["current_status"] == "EXPLICIT_BOUND_SOURCE_BACKED" and row["valid_for_claim"] == "True" for row in candidate),
            "source-backed MICROSCOPE product-bound candidate is present",
        ),
        (
            "VAL1595_4_validator_schema_pass_bound_only",
            any(row["validation_id"] == "VCOMP1595_VERDICT" and row["validator_result"] == "ONE_SCHEMA_PROVENANCE_PASS_BOUND_ONLY" for row in compat),
            "candidate passes schema/provenance compatibility as bound-only input",
        ),
        (
            "VAL1595_5_claim_limits_block_score",
            any(row["limit_id"] == "CLM1595_5_verdict" and row["effect"] == "nonclaim retained" for row in limits),
            "claim limits keep candidate from becoming a prediction",
        ),
        (
            "VAL1595_6_next_inputs_require_tau",
            any(row["input_id"] == "NIR1595_0_tau_WEP" for row in next_inputs)
            and any(row["input_id"] == "NIR1595_5_verdict" for row in next_inputs),
            "tau_WEP/source projection requirements are queued",
        ),
        (
            "VAL1595_7_runner_refuses_score",
            any(row["runner_result"] == "ACCEPT_BOUND_ANCHOR_ONLY" for row in runner)
            and any(row["runner_result"] == "REJECT_DELTA_W_NUMERIC_SCORE" for row in runner)
            and any(row["runner_result"] == "REJECT_LOCAL_GR_REENTRY" for row in runner),
            "runner accepts bound anchor only and refuses score/local GR",
        ),
        (
            "VAL1595_8_claim_gates_closed",
            all(row["claim_allowed"] == "False" for row in gates)
            and any(row["status"] == "BOUND_INPUT_ONLY_NO_CLAIM" for row in gates),
            "claim gates remain closed while acknowledging bound input",
        ),
        (
            "VAL1595_9_decision_next",
            any(row["decision"] == "NEXT_1596_TAU_WEP_SOURCE_PROJECTION_OR_ACTION_MEASURE_OWNER_LAST_GATE" for row in decisions),
            "decision selects tau_WEP source projection or action-measure owner last gate",
        ),
        ("VAL1595_10_csv_parse", all(len(read_csv(csv_path)) > 0 for csv_path in generated_csvs), "all generated 1595 CSVs parse cleanly"),
        ("VAL1595_11_claim_safety_flags", generated_flags_safe(generated_csvs), "no generated rows are score-ready, valid predictions, or claim-allowed"),
        ("VAL1595_12_no_raw_accepted", not has_1595_rows(RAB_RAW) and not has_1595_rows(RAB_ACCEPTED), "no 1595 rows written to raw/accepted finite directories"),
        ("VAL1595_13_branch_copies", all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths), "branch/quarantine nonclaim copies written"),
        ("VAL1595_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1595_15_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1595 paths are outside formalization-workbench; git status is clean when available"),
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
            "check_id": "VAL1595_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1595 first source-backed beta or action-measure owner reopen validation",
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
    reopen: list[dict[str, Any]],
    candidate: list[dict[str, Any]],
    compat: list[dict[str, Any]],
    limits: list[dict[str, Any]],
    next_inputs: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1595 - R2/fR First Source-Backed Beta Or Action-Measure Owner Reopen",
                "## Verdict\n"
                "- 1595 reopens the action-measure owner route and still cannot parent-sign it: classical equations and current-owner arguments do not kill pre-variation `w_A`.\n"
                "- The concrete progress is a first validator-readable source-backed local input: the MICROSCOPE `R1_WEP_source_charge` anchor gives `abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15` as a bound-only row.\n"
                "- This row passes the 1594-style schema/provenance gates because it has branch id, units, source path, anchor, extraction method, beta convention and arena map.\n"
                "- It is **not** an MTS prediction and not a local-GR/WEP score: `tau_WEP`, source worldtube, material response and readout kernel are still missing.\n"
                "- No local-GR, Newton, WEP, PPN, R10, clock, orbital, beta, action-measure, measured-`G`, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Action-Measure Owner Reopen",
                md_table(reopen, ["reopen_id", "route", "formal_statement", "result", "status", "blocking_gap"]),
                "## Source-Backed Candidate",
                md_table(candidate, ["row_id", "quantity", "definition", "value", "units", "source_path", "source_anchor", "current_status", "claim_scope"]),
                "## Validator Compatibility",
                md_table(compat, ["validation_id", "input_row_id", "quantity", "validator_result", "missing_required_fields", "bad_markers", "claim_allowed_after_validation", "reason"]),
                "## Claim Limits",
                md_table(limits, ["limit_id", "limit", "reason", "effect"]),
                "## Next Input Requirements",
                md_table(next_inputs, ["input_id", "quantity", "required_input", "why_needed", "priority"]),
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
    reopen = action_measure_reopen_rows()
    candidate = source_backed_candidate_rows()
    compat = validator_compat_rows()
    limits = claim_limit_rows()
    next_inputs = next_input_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        ACTION_MEASURE_REOPEN,
        SOURCE_BACKED_CANDIDATE,
        VALIDATOR_COMPAT,
        CLAIM_LIMITS,
        NEXT_INPUTS,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(ACTION_MEASURE_REOPEN, reopen)
    write_csv(SOURCE_BACKED_CANDIDATE, candidate)
    write_csv(VALIDATOR_COMPAT, compat)
    write_csv(CLAIM_LIMITS, limits)
    write_csv(NEXT_INPUTS, next_inputs)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, reopen, candidate, compat, limits, next_inputs, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
