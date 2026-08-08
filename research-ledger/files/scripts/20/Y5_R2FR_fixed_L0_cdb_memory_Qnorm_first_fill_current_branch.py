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
QUARANTINE = MICROSCOPE / "quarantine" / "1693"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "1693-Y5-R2FR-fixed-L0-cdb-memory-Qnorm-first-fill-current-branch.md"

SOURCE_FILES = {
    "1692_doc": ROOT / "1692-Y5-R2FR-EH-source-owner-or-R11-beta-vector-current-branch.md",
    "1692_validation": OUT / "P8_Y5_BRR545_1692_VALIDATION.csv",
    "1692_next": OUT / "P8_Y5_PARENT_QLOC_1692_NEXT_TARGET.csv",
    "1591_doc": ROOT / "1591-Y5-R2FR-fixed-L0-cdb-memory-Qnorm-first-fill-or-cR2-bound-row.md",
    "1591_qnorm": OUT / "P8_Y5_PARENT_QLOC_1591_QNORM_FIRST_FILL_SYNTHESIS.csv",
    "1591_theorem": OUT / "P8_Y5_PARENT_QLOC_1591_CDB_MEMORY_THEOREM_ATTEMPT.csv",
    "1591_transition": OUT / "P8_Y5_PARENT_QLOC_1591_TRANSITION_CLOSURE_PACK.csv",
    "1592_doc": ROOT / "1592-Y5-R2FR-transition-gradient-parent-signature-or-Qnorm-source-acquisition.md",
    "1592_parent": OUT / "P8_Y5_PARENT_QLOC_1592_PARENT_SIGNATURE_AUDIT.csv",
    "1592_theorem": OUT / "P8_Y5_PARENT_QLOC_1592_CANONICAL_TRANSITION_THEOREM.csv",
    "1592_source": OUT / "P8_Y5_PARENT_QLOC_1592_QNORM_CANONICAL_SOURCE_ACQUISITION.csv",
    "1592_arena": OUT / "P8_Y5_PARENT_QLOC_1592_ARENA_PROJECTION_CONTRACT.csv",
    "1593_doc": ROOT / "1593-Y5-R2FR-canonical-coupling-zero-theorem-or-finite-beta-source-rows.md",
    "1593_zero": OUT / "P8_Y5_PARENT_QLOC_1593_CANONICAL_COUPLING_ZERO_THEOREM_ATTEMPT.csv",
    "1593_package": OUT / "P8_Y5_PARENT_QLOC_1593_MATTER_PACKAGE_CLAUSE_GATE.csv",
    "1593_beta_rows": OUT / "P8_Y5_PARENT_QLOC_1593_FINITE_BETA_SOURCE_ROWS.csv",
    "1593_source_residual": OUT / "P8_Y5_PARENT_QLOC_1593_ACTION_WEIGHT_SOURCE_RESIDUAL.csv",
    "1594_doc": ROOT / "1594-Y5-R2FR-action-weight-exclusion-or-beta-source-acquisition-validator.md",
    "1594_validation": OUT / "P8_Y5_BRR545_1594_VALIDATION.csv",
    "1594_action_weight": OUT / "P8_Y5_PARENT_QLOC_1594_ACTION_WEIGHT_EXCLUSION_THEOREM_ATTEMPT.csv",
    "1594_validator_spec": OUT / "P8_Y5_PARENT_QLOC_1594_BETA_ROW_VALIDATOR_SPEC.csv",
    "1594_validator_results": OUT / "P8_Y5_PARENT_QLOC_1594_BETA_ROW_VALIDATOR_RESULTS.csv",
    "1594_queue": OUT / "P8_Y5_PARENT_QLOC_1594_BETA_SOURCE_ACQUISITION_QUEUE.csv",
}

NEEDLES = {
    "1692_doc": ["fixed-L0 residuals", "Q_norm"],
    "1692_validation": ["VAL1692_OVERALL", "PASS"],
    "1692_next": ["NEXT1692_0_primary", "fixed-L0-cdb-memory-Qnorm"],
    "1591_doc": ["Q_norm <= Q_alg + Q_cdb + Q_mem + Q_bdy + Q_trans + Q_proj", "CDB_MEMORY_ZERO_THEOREM_NOT_DERIVED"],
    "1591_qnorm": ["QNF1591_0_Q_alg", "QNF1591_6_Q_norm_total"],
    "1591_theorem": ["CMA1591_8_verdict", "CDB_MEMORY_ZERO_THEOREM_NOT_DERIVED"],
    "1591_transition": ["TCP1591_13_verdict", "TRANSITION_CLOSURE_PACK_READY_NONCLAIM"],
    "1592_doc": ["mu_m^2", "beta_source"],
    "1592_parent": ["PSA1592_7_verdict", "PARENT_SIGNATURE_NOT_CLOSED_CANONICAL_SOURCE_ACQUISITION_REQUIRED"],
    "1592_theorem": ["CTT1592_8_verdict", "CONDITIONAL_CANONICAL_THEOREM_DERIVED_NONCLAIM"],
    "1592_source": ["CSA1592_0_mu_m2", "CSA1592_12_verdict"],
    "1592_arena": ["APR1592_6_verdict", "ARENA_CONTRACT_READY_NONCLAIM"],
    "1593_doc": ["range suppression without beta_source beta_test", "ACTION_WEIGHT_AND_SOURCE_CURRENT_OWNER_ARE_HIGHEST_PRESSURE"],
    "1593_zero": ["ZTH1593_8_verdict", "ZERO_THEOREM_NOT_CLOSED_FINITE_BETA_ROWS_REQUIRED"],
    "1593_package": ["PKG1593_8_verdict", "PACKAGE_FAILS_CURRENT_CLAIM"],
    "1593_beta_rows": ["FBR1593_11_verdict", "FINITE_BETA_SOURCE_ROWS_READY_NONCLAIM"],
    "1593_source_residual": ["SWR1593_6_verdict", "SOURCE_RESIDUAL_VECTOR_READY_NONCLAIM"],
    "1594_doc": ["strict beta-row validator", "ACTION_WEIGHT_EXCLUSION_NOT_DERIVED"],
    "1594_validation": ["VAL1594_OVERALL", "PASS"],
    "1594_action_weight": ["AWT1594_7_verdict", "ACTION_WEIGHT_EXCLUSION_NOT_DERIVED_VALIDATOR_REQUIRED"],
    "1594_validator_spec": ["BVS1594_9_verdict", "current 1593 beta rows are expected to fail"],
    "1594_validator_results": ["BVR1594_VERDICT", "NO_ACCEPTED_BETA_ROWS"],
    "1594_queue": ["BSQ1594_2_Delta_w_A", "BSQ1594_7_verdict"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1693_SOURCE_REGISTER.csv"
FIXED_L0_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1693_FIXED_L0_RESIDUAL_LEDGER.csv"
CANONICAL_INPUTS = OUT / "P8_Y5_PARENT_QLOC_1693_CANONICAL_INPUT_REQUIREMENTS.csv"
COUPLING_GATE = OUT / "P8_Y5_PARENT_QLOC_1693_COUPLING_AND_ACTION_WEIGHT_GATE.csv"
BETA_VALIDATOR_IMPORT = OUT / "P8_Y5_PARENT_QLOC_1693_BETA_VALIDATOR_IMPORT_STATUS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1693_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1693_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1693_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1693_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    FIXED_L0_LEDGER,
    CANONICAL_INPUTS,
    COUPLING_GATE,
    BETA_VALIDATOR_IMPORT,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED = [
    FIXED_L0_LEDGER,
    CANONICAL_INPUTS,
    COUPLING_GATE,
    BETA_VALIDATOR_IMPORT,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    FIXED_L0_LEDGER: [
        QUARANTINE / "FIXED_L0_RESIDUAL_LEDGER.csv",
        BRANCH_RESIDUALS / "R2FR_fixed_L0_residual_ledger_1693.csv",
        QUEUE / "JR1693_FIXED_L0_RESIDUAL_LEDGER.csv",
    ],
    CANONICAL_INPUTS: [
        QUARANTINE / "CANONICAL_INPUT_REQUIREMENTS.csv",
        BRANCH_RESIDUALS / "R2FR_canonical_input_requirements_1693.csv",
        QUEUE / "JR1693_CANONICAL_INPUT_REQUIREMENTS.csv",
    ],
    COUPLING_GATE: [
        QUARANTINE / "COUPLING_AND_ACTION_WEIGHT_GATE.csv",
        BRANCH_RESIDUALS / "R2FR_coupling_action_weight_gate_1693.csv",
        QUEUE / "JR1693_COUPLING_AND_ACTION_WEIGHT_GATE.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1693.csv",
        QUEUE / "JR1693_NEXT_TARGET.csv",
    ],
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bool_cell(value: object) -> bool:
    return str(value).strip().lower() == "true"


def list_cell(values: list[object] | tuple[object, ...]) -> str:
    return ";".join(str(value) for value in values)


def markdown_table(rows: list[dict[str, object]], headers: list[str]) -> str:
    if not rows:
        return "_No rows._"
    table = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        table.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(table)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, path in SOURCE_FILES.items():
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = NEEDLES[key]
        needles_present = exists and all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": list_cell(needles),
                "use_in_1693": "fixed-L0 Qnorm residual and canonical coupling/action-weight bridge",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def fixed_l0_rows() -> list[dict[str, object]]:
    rows = [
        ("FL1693_0_Q_alg", "Q_alg", "fixed-L0 algebraic m/L branch", "SYMBOLIC_FIRST_FILL_READY_VALUES_MISSING", "F2;Phi_S or A_S;mu_m2;L0;ell_tr;A_ref;source_path"),
        ("FL1693_1_Q_cdb", "Q_cdb", "K_conn+K_domain+K_boundary+K_comm response", "SUBCHANNEL_DECOMPOSITION_READY_NUMERIC_VALUES_MISSING", "K_conn;K_domain;K_boundary;K_comm;N_div;trace/index convention"),
        ("FL1693_2_Q_mem", "Q_mem", "memory kinetic/source/bath/boundary stress", "MEMORY_STRESS_CONTRACT_READY_VALUES_MISSING", "K_mem_kin;K_mem_drift;J_mem;B_mem;source silence/no-hair theorem"),
        ("FL1693_3_Q_bdy", "Q_bdy", "boundary primitive, reference subtraction, corner/edge terms", "BOUNDARY_FIRST_FILL_READY_NO_FLUX_OR_VALUES_MISSING", "boundary primitive;domain;normal;corner terms;reference subtraction"),
        ("FL1693_4_Q_trans", "Q_trans", "transition shell and gradient-support residual", "CLOSURE_SCHEMA_READY_PARENT_SIGNATURE_AND_VALUES_MISSING", "mu_m2;Phi_S;tail terms;shell bound;parent signature"),
        ("FL1693_5_Q_proj", "Q_proj", "P_loc/readout/divergence/trace commutator leakage", "PROJECTOR_FIRST_FILL_READY_VALUES_MISSING", "P_loc;readout frame;commutator norm;trace convention"),
        ("FL1693_6_Q_norm", "Q_norm", "Q_norm <= Q_alg+Q_cdb+Q_mem+Q_bdy+Q_trans+Q_proj", "TOTAL_BOUND_FORM_READY_ALL_COMPONENT_VALUES_MISSING", "all Q_i;units;source paths;no-cancellation;arena projection"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "ledger_id": ledger_id,
            "quantity": quantity,
            "role": role,
            "current_status": status,
            "missing_inputs": missing,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for ledger_id, quantity, role, status, missing in rows
    ]


def canonical_input_rows() -> list[dict[str, object]]:
    rows = [
        ("CAN1693_0_mu_m2", "mu_m^2(X_B)", "canonical mass gap, ell_tr=1/sqrt(mu_m^2)", "MISSING_SOURCE_BACKED_CANONICAL_GAP", "range;Q_alg;R10 lambda;transition length"),
        ("CAN1693_1_beta_source", "beta_source", "source leg partial_phi ln m_source_eff or source-current variation", "MISSING_SOURCE_BETA", "R10;Newton source;WEP"),
        ("CAN1693_2_beta_test", "beta_test", "test leg partial_phi ln m_test_eff or test-body variation", "MISSING_TEST_BETA", "R10;WEP;clock;orbital"),
        ("CAN1693_3_beta_product", "beta_source*beta_test", "finite exchange product; no linear shortcut", "PRODUCT_LAW_READY_VALUES_MISSING", "all alpha(lambda) and local finite-force scoring"),
        ("CAN1693_4_Phi_S", "Phi_S", "canonical source/boundary amplitude for exterior profile", "MISSING_CANONICAL_AMPLITUDE", "Delta_phi;gradient envelope;Q_alg;stress envelope"),
        ("CAN1693_5_epsilon_tail", "epsilon_tail", "boundary/readout/projector/non-Hilbert/CDB/source-normalization tails", "MISSING_TAIL_ENVELOPE", "all local arenas"),
        ("CAN1693_6_Aref_projection", "A_ref;N_div;N_G;N_D;U_min", "normalizations converting residuals into observable bounds", "MISSING_OPERATOR_PROJECTION_NORMS", "PPN gamma and arena contracts"),
        ("CAN1693_7_Delta_w", "Delta_w_A;beta_w_source;beta_w_test", "action-weight counterexample variables", "FIRST_FILL_READY_VALUE_MISSING", "Newton;common matter;R10;WEP"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": input_id,
            "quantity": quantity,
            "definition": definition,
            "current_status": status,
            "observable_links": links,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for input_id, quantity, definition, status, links in rows
    ]


def coupling_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("COUP1693_0_chain_rule", "delta_vphi S_matter chain rule", "exact conditional route to J_c=0 and beta_source=beta_test=0", "STANDARD_CHAIN_RULE_CONDITIONAL", "zero clauses must close together"),
        ("COUP1693_1_q_kernel", "Dq_loc[v_phi]=0", "canonical generator quotient-vertical", "UNSIGNED_KERNEL", "q_loc and v_phi not jointly parent-signed"),
        ("COUP1693_2_coframe", "e_obs=Obs_e(q) with no shadow frame", "observed geometry blind to canonical mode", "SUFFICIENT_SIGNATURE_NOT_PARENT_SIGNED", "coframe/no-shadow route unsigned"),
        ("COUP1693_3_constants", "Lie_vphi theta_A=0", "constants and material labels phi-blind", "CONSTANT_SUPERSELECTION_UNSIGNED", "finite clock/material rows retained"),
        ("COUP1693_4_action_weights", "no independent w_A S_A", "kills source-normalization gremlin", "ACTIVE_COUNTEREXAMPLE", "pre-variation action weights remain legal"),
        ("COUP1693_5_current_owner", "single Hilbert/source current owner", "links beta silence to conservation/local GR", "CURRENT_OWNER_NOT_DERIVED", "source-current and Bianchi descent remain contracts"),
        ("COUP1693_6_boundary_readout", "boundary/projection/readout silence", "prevents arena kernels from reintroducing couplings", "BOUNDARY_READOUT_UNSIGNED", "tail rows mandatory"),
        ("COUP1693_7_verdict", "whole coupling package", "g_c=0 only if every package gate closes under one parent action", "ZERO_THEOREM_NOT_CLOSED_FINITE_BETA_ROWS_REQUIRED", "use strict beta/source rows until theorem closes"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "clause": clause,
            "would_close": would_close,
            "current_status": status,
            "blocking_gap": gap,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, clause, would_close, status, gap in rows
    ]


def validator_import_rows() -> list[dict[str, object]]:
    rows = [
        ("BVI1693_0_policy", "strict beta validator", "IMPORTED_FROM_1594", "reject rows without source path, source anchor, extraction method, units, beta convention and arena map"),
        ("BVI1693_1_current_rows", "1593 beta templates", "NO_ACCEPTED_BETA_ROWS", "all current rows are nonclaim templates"),
        ("BVI1693_2_action_weight", "Delta_w_A/beta_w rows", "HIGHEST_PRIORITY", "w_A can preserve classical equations while changing Hilbert source variation"),
        ("BVI1693_3_measured_G_guard", "common derivative-silent absorption only", "GUARD_ACTIVE", "relative or phi-dependent weights are physics, not calibration"),
        ("BVI1693_4_next_order", "source beta rows before arena kernels", "SELECTED_ORDER", "arena kernels cannot score until beta_source/beta_test/Delta_w/tails exist"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "import_id": import_id,
            "object": obj,
            "status": status,
            "effect": effect,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for import_id, obj, status, effect in rows
    ]


def runner_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1693_0_fixed_L0", "claim local GR from fixed-L0 double-zero", "REJECT_CLOSURE_AS_DERIVATION", "fixed-L0 closes algebraic branch only"),
        ("RUN1693_1_Qnorm", "score Qnorm/Cassini from symbolic Q_i rows", "REJECT_QNORM_NUMERIC_PASS", "all Q_i and projection norms are missing"),
        ("RUN1693_2_range_only", "use mu_m2/range suppression as coupling suppression", "REJECT_RANGE_ONLY_CLAIM", "beta_source beta_test are separate required inputs"),
        ("RUN1693_3_coupling_zero", "claim g_c=0 from conditional chain rule", "REJECT_ZERO_COUPLING_CLAIM", "matter package and action weights are unsigned"),
        ("RUN1693_4_beta_score", "score local arenas from beta templates", "REJECT_FINITE_BETA_SCORE", "1594 validator accepts no current beta rows"),
        ("RUN1693_5_local_GR", "claim derived local GR/Newton", "BLOCKED_NO_CLAIM", "coupling, conservation, common matter and source-normalized Newton remain open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, case, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT1693_0_primary",
            "1694-Y5-R2FR-action-weight-exclusion-or-first-source-backed-beta-current-branch.md",
            "scripts/Y5_R2FR_action_weight_exclusion_or_first_source_backed_beta_current_branch.py",
            "try to derive the parent action-measure/source-current owner that excludes independent w_A; if not, create the first validator-readable beta_source/beta_test/Delta_w acquisition row without scoring",
            "action weights are the highest-pressure seam for Newton/common-matter recovery",
            "selected",
        ),
        (
            "NEXT1693_1_parallel",
            "1694b-Y5-R2FR-Qnorm-component-source-acquisition-first-row.md",
            "scripts/Y5_R2FR_Qnorm_component_source_acquisition_first_row.py",
            "begin source acquisition for Q_alg/Q_cdb/Q_mem/Q_bdy/Q_trans/Q_proj components only after coupling rows are not completely blank",
            "Qnorm scoring still needs beta/tail/source normalization to avoid fake local-GR pressure",
            "held_fallback",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "next_target": target,
            "script": script,
            "objective": objective,
            "reason": reason,
            "selection_status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, target, script, objective, reason, status in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1693_0_fixed_L0", "fixed-L0 local GR branch", "BLOCKED_NO_CLAIM", "algebraic double-zero is not full residual closure"),
        ("CG1693_1_Qnorm", "Qnorm finite bound pass", "BLOCKED_NO_CLAIM", "all Q_i values and projection norms are missing"),
        ("CG1693_2_coupling_zero", "g_c=0 / beta_source=beta_test=0", "BLOCKED_NO_CLAIM", "matter package and action weights are unsigned"),
        ("CG1693_3_beta_rows", "finite beta/source row score", "BLOCKED_NO_CLAIM", "strict validator accepts no beta rows"),
        ("CG1693_4_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "coupling, source normalization, conservation and common matter do not close together"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in rows
    ]


def all_claim_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if field in row and bool_cell(row[field]):
                    return False
    return True


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validate(
    source_rows: list[dict[str, object]],
    fixed_rows: list[dict[str, object]],
    canonical_rows: list[dict[str, object]],
    coupling_rows: list[dict[str, object]],
    validator_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    qnorm_complete = {"Q_alg", "Q_cdb", "Q_mem", "Q_bdy", "Q_trans", "Q_proj", "Q_norm"}.issubset({str(row["quantity"]) for row in fixed_rows})
    canonical_has_beta = {"beta_source", "beta_test", "beta_source*beta_test", "Delta_w_A;beta_w_source;beta_w_test"}.issubset({str(row["quantity"]) for row in canonical_rows})
    coupling_blocked = any(row["gate_id"] == "COUP1693_7_verdict" and row["current_status"] == "ZERO_THEOREM_NOT_CLOSED_FINITE_BETA_ROWS_REQUIRED" for row in coupling_rows)
    validator_imported = any(row["import_id"] == "BVI1693_1_current_rows" and row["status"] == "NO_ACCEPTED_BETA_ROWS" for row in validator_rows)
    runner_blocks = all(not bool_cell(row["can_score"]) for row in runner_rows_)
    next_selected = any(row["route_id"] == "NEXT1693_0_primary" and row["selection_status"] == "selected" and "action-weight-exclusion" in row["next_target"] for row in next_rows)
    local_gr_blocked = any(row["claim"] == "derived local GR/Newton reduction" and row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows)
    no_claim_flags = all_claim_flags_false(CLAIM_CHECKED)
    csv_parse = True
    for path in GENERATED:
        try:
            read_csv(path)
        except Exception:
            csv_parse = False
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = len(list(FORMALIZATION.rglob("*1693*"))) == 0 if FORMALIZATION.exists() else True

    checks = [
        ("VAL1693_0_sources_exist", sources_ok, "all cited source paths exist and required needles are present"),
        ("VAL1693_1_qnorm_complete", qnorm_complete, "Qnorm ledger includes all six components and total"),
        ("VAL1693_2_canonical_beta_inputs", canonical_has_beta, "canonical input rows include beta source/test/product and action weights"),
        ("VAL1693_3_coupling_blocked", coupling_blocked, "coupling zero theorem remains blocked"),
        ("VAL1693_4_validator_imported", validator_imported, "1594 validator status is imported and rejects current beta rows"),
        ("VAL1693_5_runner_blocks", runner_blocks, "runner blocks all current scoring cases"),
        ("VAL1693_6_next_selected", next_selected, "next target selects action-weight exclusion or first source-backed beta row"),
        ("VAL1693_7_local_gr_blocked", local_gr_blocked, "local GR/Newton claim remains blocked"),
        ("VAL1693_8_no_claim_flags", no_claim_flags, "all generated scoring and claim flags remain false"),
        ("VAL1693_9_csv_parse", csv_parse, "all generated 1693 CSVs parse"),
        ("VAL1693_10_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1693_11_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1693_12_formalization_untouched", formalization_untouched, "no 1693 outputs found under formalization-workbench"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1693_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1693 fixed-L0 Qnorm and canonical coupling current-branch validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    fixed_rows: list[dict[str, object]],
    canonical_rows: list[dict[str, object]],
    coupling_rows: list[dict[str, object]],
    validator_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1693 - Fixed-L0 CDB Memory Qnorm First Fill Current Branch

## Verdict

1693 stitches the fixed-`L0` residual lane into the canonical coupling lane. The fixed-`L0` double-zero branch remains the best local algebraic route, but it only closes the algebraic `m/L0` sector. The live residual ledger is still `Q_norm <= Q_alg+Q_cdb+Q_mem+Q_bdy+Q_trans+Q_proj`.

The current branch has a better language now: use canonical inputs `mu_m^2`, `beta_source`, `beta_test`, `Phi_S`, tail envelopes and projection norms. But range suppression is not coupling suppression. Without `beta_source beta_test` or a parent-signed `g_c=0` theorem, no R10/PPN/WEP/clock/orbital/local-GR score is allowed.

The hardest seam remains the pre-variation action/source weight `w_A`. It can leave classical-looking equations while changing Hilbert source variation, so it blocks the Newton/common-matter side unless excluded by parent action-measure/current-owner theorem or filled as finite `Delta_w/beta_w` rows.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1693"])}

## Fixed-L0 Residual Ledger

{markdown_table(fixed_rows, ["ledger_id", "quantity", "role", "current_status", "missing_inputs"])}

## Canonical Input Requirements

{markdown_table(canonical_rows, ["input_id", "quantity", "definition", "current_status", "observable_links"])}

## Coupling And Action-Weight Gate

{markdown_table(coupling_rows, ["gate_id", "clause", "current_status", "blocking_gap"])}

## Beta Validator Import Status

{markdown_table(validator_rows, ["import_id", "object", "status", "effect"])}

## Runner Refusal

{markdown_table(runner_rows_, ["runner_id", "case", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["route_id", "next_target", "objective", "selection_status"])}

## Claim Gates

{markdown_table(claim_rows, ["claim_id", "claim", "status", "reason"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This is where the theory stops being vague and starts behaving like engineering: every path to local GR now has a named load-bearing part. Fixed-`L0` gives the clean branch, `Q_norm` gives the no-cancellation empirical lane, and the coupling/action-weight gate decides whether the branch can reduce to GR or must stay a finite residual theory.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    fixed_rows = fixed_l0_rows()
    canonical_rows = canonical_input_rows()
    coupling_rows = coupling_gate_rows()
    validator_rows = validator_import_rows()
    runner_rows_ = runner_rows()
    next_rows = next_target_rows()
    claim_rows = claim_gate_rows()

    write_csv(SOURCE_REGISTER, source_rows, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1693", "valid_for_claim", "claim_allowed"])
    write_csv(FIXED_L0_LEDGER, fixed_rows, ["branch_id", "ledger_id", "quantity", "role", "current_status", "missing_inputs", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(CANONICAL_INPUTS, canonical_rows, ["branch_id", "input_id", "quantity", "definition", "current_status", "observable_links", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(COUPLING_GATE, coupling_rows, ["branch_id", "gate_id", "clause", "would_close", "current_status", "blocking_gap", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(BETA_VALIDATOR_IMPORT, validator_rows, ["branch_id", "import_id", "object", "status", "effect", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(RUNNER, runner_rows_, ["branch_id", "runner_id", "case", "status", "reason", "can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "route_id", "next_target", "script", "objective", "reason", "selection_status", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claim_rows, ["branch_id", "claim_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    cleanup_pycache()
    validation_rows = validate(source_rows, fixed_rows, canonical_rows, coupling_rows, validator_rows, runner_rows_, next_rows, claim_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, fixed_rows, canonical_rows, coupling_rows, validator_rows, runner_rows_, next_rows, claim_rows, validation_rows)

    failed = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1693 validation PASS")


if __name__ == "__main__":
    main()
