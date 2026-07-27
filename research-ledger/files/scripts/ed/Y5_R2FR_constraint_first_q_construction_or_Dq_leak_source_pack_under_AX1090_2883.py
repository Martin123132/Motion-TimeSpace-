from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2883-Y5-R2FR-constraint-first-q-construction-or-Dq-leak-source-pack-under-AX1090.md"

SRC_2882_DOC = ROOT / "2882-Y5-R2FR-q-object-vertical-generator-certificate-or-Dq-leak-row-under-AX1090.md"
SRC_2882_NEXT = RESIDUALS / "P8_Y5_R2FR_2882_NEXT_TARGET.csv"
SRC_2882_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2882_VALIDATION.csv"
SRC_2882_FILL = RESIDUALS / "P8_Y5_R2FR_2882_DQ_LEAK_FILL_ATTEMPT.csv"

SRC_1668_DOC = ROOT / "1668-Y5-R2FR-constraint-first-Zphi-RAB-action-or-Dq-leak-source-pack.md"
SRC_1668_ACTION = RESIDUALS / "P8_Y5_PARENT_QLOC_1668_CONSTRAINT_FIRST_ACTION_ATTEMPT.csv"
SRC_1668_NOPOLE = RESIDUALS / "P8_Y5_PARENT_QLOC_1668_NO_POLE_GATE_AUDIT.csv"
SRC_1668_PACK = RESIDUALS / "P8_Y5_PARENT_QLOC_1668_DQ_LEAK_SOURCE_PACK_SCHEMA.csv"
SRC_1668_VALIDATION = RESIDUALS / "P8_Y5_BRR545_1668_VALIDATION.csv"

SRC_1669_DOC = ROOT / "1669-Y5-R2FR-Dq-leak-bound-source-pack-units-and-arena-projections.md"
SRC_1669_UNITS = RESIDUALS / "P8_Y5_PARENT_QLOC_1669_DQ_LEAK_UNIT_CONVENTIONS.csv"
SRC_1669_ARENA = RESIDUALS / "P8_Y5_PARENT_QLOC_1669_ARENA_PROJECTION_MATRIX.csv"
SRC_1669_R10 = RESIDUALS / "P8_Y5_PARENT_QLOC_1669_R10_SOURCE_PACK_TEMPLATE.csv"
SRC_1669_VALIDATION = RESIDUALS / "P8_Y5_BRR545_1669_VALIDATION.csv"

SRC_1670_DOC = ROOT / "1670-Y5-R2FR-Cqm-DqZ-observed-coframe-zero-or-first-finite-bound-row.md"
SRC_1670_CHAIN = RESIDUALS / "P8_Y5_PARENT_QLOC_1670_CQM_DQZ_CHAIN_RULE_THEOREM.csv"
SRC_1670_PRODUCT = RESIDUALS / "P8_Y5_PARENT_QLOC_1670_PRODUCT_BOUND_CONTRACT.csv"
SRC_1670_ARENA = RESIDUALS / "P8_Y5_PARENT_QLOC_1670_ARENA_PROJECTION_UPDATE.csv"
SRC_1670_VALIDATION = RESIDUALS / "P8_Y5_BRR545_1670_VALIDATION.csv"

SRC_1671_DOC = ROOT / "1671-Y5-R2FR-DqZ-basis-kernel-or-Cobs-operator-norm-input.md"
SRC_1671_ZLOCK = RESIDUALS / "P8_Y5_PARENT_QLOC_1671_Z_BASIS_COMPONENT_LOCK_AUDIT.csv"
SRC_1671_DQZ = RESIDUALS / "P8_Y5_PARENT_QLOC_1671_DQZ_KERNEL_THEOREM_ATTEMPT.csv"
SRC_1671_FACTORS = RESIDUALS / "P8_Y5_PARENT_QLOC_1671_PRODUCT_FACTOR_QUEUE.csv"
SRC_1671_VALIDATION = RESIDUALS / "P8_Y5_BRR545_1671_VALIDATION.csv"

SRC_1576_CNP = RESIDUALS / "P8_Y5_PARENT_QLOC_1576_RAB_CONSTRAINT_NO_POLE_TEST.csv"
SRC_1576_NPT = RESIDUALS / "P8_Y5_PARENT_QLOC_1576_RAB_NO_POLE_THEOREM_ATTEMPT.csv"
SRC_1621_NOPOLE = RESIDUALS / "P8_Y5_PARENT_QLOC_1621_NO_POLE_THEOREM_AUDIT.csv"
SRC_2708_THEOREM = RESIDUALS / "P8_Y5_R2FR_2708_CONDITIONAL_NO_POLE_SOURCE_ZERO_THEOREM.csv"
SRC_2708_MATRIX = RESIDUALS / "P8_Y5_R2FR_2708_NO_POLE_CERTIFICATE_MATRIX.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2883_SOURCE_REGISTER.csv",
    "synthesis": RESIDUALS / "P8_Y5_R2FR_2883_CONSTRAINT_FIRST_SYNTHESIS.csv",
    "no_pole": RESIDUALS / "P8_Y5_R2FR_2883_NO_POLE_CURRENT_GATE.csv",
    "source_pack": RESIDUALS / "P8_Y5_R2FR_2883_DQ_LEAK_ARENA_SOURCE_PACK.csv",
    "product_queue": RESIDUALS / "P8_Y5_R2FR_2883_CQM_DQZ_PRODUCT_BOUND_QUEUE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2883_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2883_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2883_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2883_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2883_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2883_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "synthesis_copy": LOCAL_BOUNDS / "RAB_CONSTRAINT_FIRST_SYNTHESIS_2883_NONCLAIM.csv",
    "pack_copy": SOURCE_WEIGHT / "RAB_DQ_LEAK_ARENA_SOURCE_PACK_2883_NONCLAIM.csv",
    "queue_copy": BETA_DOCS / "RAB_CQM_DQZ_PRODUCT_BOUND_QUEUE_2883_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2883_Z_physical_lock_or_first_product_factor_NEXT.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2883_0_2882_doc", SRC_2882_DOC, "Status: `Y5_R2FR_2882_qv_certificate_rejected_Dq_leaks_retained_2883_next`;best next route", "2882 handoff"),
        ("SRC2883_1_2882_next", SRC_2882_NEXT, "NEXT2882_0_2883", "explicit 2883 target"),
        ("SRC2883_2_2882_validation", SRC_2882_VALIDATION, "VAL2882_OVERALL", "2882 validation"),
        ("SRC2883_3_2882_fill", SRC_2882_FILL, "FILL2882_0_Dq_vertical_leak;FILL2882_5_constraint_zero_attempt", "2882 retained leak and constraint-zero attempt"),
        ("SRC2883_4_1668_doc", SRC_1668_DOC, "CONSTRAINT_FIRST_NOT_DERIVED_CURRENT_CORPUS;Dq Leak Source Pack Schema", "prior constraint-first source-pack checkpoint"),
        ("SRC2883_5_1668_action", SRC_1668_ACTION, "CFA1668_1_RAB_algebraic_auxiliary;CFA1668_8_verdict", "constraint-first action attempts"),
        ("SRC2883_6_1668_nopole", SRC_1668_NOPOLE, "NPG1668_7_verdict", "no-pole gate audit"),
        ("SRC2883_7_1668_pack", SRC_1668_PACK, "DSP1668_0_Dq_Z;DSP1668_7_Scg_envelope", "Dq leak source-pack schema"),
        ("SRC2883_8_1668_validation", SRC_1668_VALIDATION, "VAL1668_OVERALL", "1668 validation"),
        ("SRC2883_9_1669_doc", SRC_1669_DOC, "arena-ready acquisition pack;R10 Source Pack Template", "arena-ready leak source-pack checkpoint"),
        ("SRC2883_10_1669_units", SRC_1669_UNITS, "Dq_Z;C_qm;S_cg_envelope", "unit conventions"),
        ("SRC2883_11_1669_arena", SRC_1669_ARENA, "R0_identity_coframe_direct;R10_fifth_force", "arena projection matrix"),
        ("SRC2883_12_1669_r10", SRC_1669_R10, "alpha_predicted;tau_R10_a;MISSING_DIGITIZED_ALPHA_LAMBDA_CURVE", "R10 source-pack template"),
        ("SRC2883_13_1669_validation", SRC_1669_VALIDATION, "VAL1669_OVERALL", "1669 validation"),
        ("SRC2883_14_1670_doc", SRC_1670_DOC, "C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z", "C_qm/Dq_Z product-bound checkpoint"),
        ("SRC2883_15_1670_chain", SRC_1670_CHAIN, "CR1670_3_product_bound;CR1670_4_zero_routes", "chain-rule product theorem"),
        ("SRC2883_16_1670_product", SRC_1670_PRODUCT, "PB1670_0_DqZ;PB1670_3_CqmZ", "product-bound contract"),
        ("SRC2883_17_1670_arena", SRC_1670_ARENA, "R0_identity_coframe_direct;R10_fifth_force", "primary arena update"),
        ("SRC2883_18_1670_validation", SRC_1670_VALIDATION, "VAL1670_OVERALL", "1670 validation"),
        ("SRC2883_19_1671_doc", SRC_1671_DOC, "`Dq_Z=0` is not parent-signed;C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z", "Dq_Z basis/kernel checkpoint"),
        ("SRC2883_20_1671_zlock", SRC_1671_ZLOCK, "ZB1671_2_component_lock;ZB1671_6_verdict", "Z physical lock audit"),
        ("SRC2883_21_1671_dqz", SRC_1671_DQZ, "KT1671_0_kernel_theorem_statement;KT1671_5_verdict", "Dq_Z kernel theorem attempt"),
        ("SRC2883_22_1671_factors", SRC_1671_FACTORS, "PFQ1671_0_clean_kill;PFQ1671_3_physical_lock", "product-factor queue"),
        ("SRC2883_23_1671_validation", SRC_1671_VALIDATION, "VAL1671_OVERALL", "1671 validation"),
        ("SRC2883_24_1576_constraint", SRC_1576_CNP, "CNP1576_0_multiplier_origin;CNP1576_5_verdict", "R_AB constraint/no-pole test"),
        ("SRC2883_25_1576_nopole", SRC_1576_NPT, "NPT1576_0_first_class;NPT1576_3_verdict", "R_AB no-pole theorem attempt"),
        ("SRC2883_26_1621_nopole", SRC_1621_NOPOLE, "NPA1621_0_conditional_theorem;NPA1621_5_verdict", "conditional no-pole audit"),
        ("SRC2883_27_2708_theorem", SRC_2708_THEOREM, "THM2708_1_no_pole;THM2708_6_current_corpus_verdict", "conditional no-pole/source-zero theorem"),
        ("SRC2883_28_2708_matrix", SRC_2708_MATRIX, "NPC2708_3_degree_count;NPC2708_8_verdict", "no-pole certificate matrix"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def synthesis_rows() -> list[dict[str, Any]]:
    specs = [
        ("SYN2883_0_exact_constraint_law", "If a parent constraint/no-pole action removes R_AB/Z/phi before q and ordinary matter/readout are formed, then Dq leak for that variable is zero by absence rather than by post-hoc gauge naming.", "EXACT_CONDITIONAL_ROUTE", SRC_2708_THEOREM, "THM2708_1_no_pole", False),
        ("SYN2883_1_magic_multiplier_guard", "Adding lambda_R R_AB or lambda_Z Z only proves an inserted multiplier can impose a zero; it is not a derivation unless the multiplier/current originates in the parent action.", "REJECT_MAGIC_MULTIPLIER_AS_DERIVATION", SRC_1621_NOPOLE, "NPA1621_1_multiplier_insertion_refusal", False),
        ("SYN2883_2_second_class_preference", "The second-class/algebraic auxiliary route is the least-scrutiny constraint path because it removes a visible residual before q, rather than calling a visible metric component gauge.", "BEST_CONDITIONAL_ROUTE_UNSIGNED", SRC_1668_ACTION, "CFA1668_1_RAB_algebraic_auxiliary", False),
        ("SYN2883_3_first_class_nopole", "A first-class/no-pole proof would need Omega, generator, bracket closure, degree count and boundary charge silence.", "FIRST_CLASS_ROUTE_NOT_CONSTRUCTED", SRC_1668_NOPOLE, "NPG1668_2_momentum_map", False),
        ("SYN2883_4_positive_nohair", "If residuals are physical, a positive source-free operator could force zero only with Z_R/M_R^2 positivity, source zero and boundary flux zero.", "VALUES_AND_SOURCE_ZERO_MISSING", SRC_1576_NPT, "NPT1576_1_positive_sourcefree", False),
        ("SYN2883_5_current_verdict", "Current corpus still lacks parent constraint origin, no-pole certificate, Z physical lock, matter/readout descent and boundary/source silence in one branch.", "CONSTRAINT_FIRST_NOT_DERIVED_CURRENT_CHAIN", SRC_1668_ACTION, "CFA1668_8_verdict", False),
    ]
    return [
        add_common(
            {
                "synthesis_id": synthesis_id,
                "statement": statement,
                "status": status,
                "source_path": str(path),
                "source_anchor": anchor,
                "theorem_closed": closed,
                "parent_signed": False,
            }
        )
        for synthesis_id, statement, status, path, anchor, closed in specs
    ]


def no_pole_rows() -> list[dict[str, Any]]:
    specs = [
        ("NP2883_0_parent_qmap", "parent q map and observed bundle owned before matter/readout", "CONDITIONAL_ONLY_NOT_PARENT_SIGNED", SRC_2708_MATRIX, "NPC2708_0_parent_qmap"),
        ("NP2883_1_vertical_kernel", "same v_X used in source rows satisfies Dq[v_X]=0 or is pre-q eliminated", "CONDITIONAL_ONLY", SRC_2708_MATRIX, "NPC2708_1_vertical_kernel"),
        ("NP2883_2_action_descent", "S_parent descends through q or is gauge-degenerate/topological along v_X", "NOT_SIGNED", SRC_2708_MATRIX, "NPC2708_2_action_descent_or_gauge_degeneracy"),
        ("NP2883_3_degree_count", "constraint/Hilbert degree count removes the local residual from propagating spectrum", "MISSING_DEGREE_COUNT", SRC_2708_MATRIX, "NPC2708_3_degree_count"),
        ("NP2883_4_matter_signature", "ordinary matter obeys quotient geometry/gauge data with fixed constants and no shadow frame", "CONDITIONAL_THEOREM_NOT_PROMOTED", SRC_2708_MATRIX, "NPC2708_4_matter_MOMS"),
        ("NP2883_5_boundary_domain", "boundary, support, projector and non-Hilbert tails are zero or explicitly bounded", "MISSING_BOUNDARY_DOMAIN_SILENCE", SRC_2708_MATRIX, "NPC2708_5_boundary_domain_silence"),
        ("NP2883_6_GR_readout", "weak-field observed equations reduce to GR/Newton/PPN after source charge and readout are fixed", "NOT_REACHED", SRC_2708_MATRIX, "NPC2708_7_GR_readout"),
        ("NP2883_7_verdict", "all no-pole/source-zero clauses close in one parent branch", "CERTIFICATE_NOT_CLOSED", SRC_2708_MATRIX, "NPC2708_8_verdict"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "required_clause": clause,
                "current_status": status,
                "source_path": str(path),
                "source_anchor": anchor,
                "gate_pass": False,
                "theorem_closed": False,
                "parent_signed": False,
            }
        )
        for gate_id, clause, status, path, anchor in specs
    ]


def source_pack_rows() -> list[dict[str, Any]]:
    specs = [
        ("DSP2883_0_Dq_Z", "Dq_Z_norm", "Z normal-form quotient leak", "dimensionless only after q/Z basis and arena norm are declared", "R0;R3;R4;R10;R11", "MISSING_NUMERIC_OR_THEOREM_ZERO"),
        ("DSP2883_1_Dq_phi", "Dq_phi_norm", "phi improvement quotient leak", "arena-dependent until phi normalization and boundary/domain convention are fixed", "R2;R3;R4;R10;R11", "MISSING_NUMERIC_OR_THEOREM_ZERO"),
        ("DSP2883_2_Dq_RAB_Jq", "Dq_RAB_or_Jq_norm", "R_AB/J_q cell-visible leak", "dimensionless after cell-map normalization", "R3;R4;R5;R6;R8;R10", "MISSING_NUMERIC_OR_THEOREM_ZERO"),
        ("DSP2883_3_Cqm", "C_qm=||DObs_e[Dq[v]]||", "geometry pullback/source stress", "coframe norm after observed coframe functor and local norm are fixed", "R0;R3;R4;R10", "MISSING_QMAP_DERIVATIVE"),
        ("DSP2883_4_S_direct", "S_direct", "direct matter/source dependence", "E* forcing/action-gradient units until converted by Green/readout operator", "R1;R7;R9;R10", "MISSING_NUMERIC_OR_THEOREM_ZERO"),
        ("DSP2883_5_S_boundary", "S_boundary", "compact boundary/source-memory coupling", "E* or boundary-charge units until projection is fixed", "R5;R6;R7;R8;R10", "MISSING_NUMERIC_OR_THEOREM_ZERO"),
        ("DSP2883_6_Dtheta_marker", "Dtheta_marker_Dq_leak", "constants/material marker channel", "dimensionless derivative of constants/material markers", "R1;R2;R7;R8;R9", "MISSING_NUMERIC_OR_THEOREM_ZERO"),
        ("DSP2883_7_Scg_envelope", "S_cg_norm", "absolute no-cancellation envelope", "E* forcing units", "R0-R11", "FORMULA_ONLY_INPUTS_MISSING"),
    ]
    return [
        add_common(
            {
                "source_pack_id": row_id,
                "symbol": symbol,
                "channel": channel,
                "unit_convention": units,
                "priority_arenas": arenas,
                "candidate_value": value,
                "source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, symbol, channel, units, arenas, value in specs
    ]


def product_queue_rows() -> list[dict[str, Any]]:
    specs = [
        ("PQ2883_0_Z_physical_lock", "Z -> R_phys full-rank/coercive physical residual lock", "derive", "MISSING_COMPONENT_LOCK_AND_NORM_EQUIVALENCE", "highest", True),
        ("PQ2883_1_DqZ_zero", "Dq_Z_norm=0 by q-independence or pre-q constraint elimination", "derive", "MISSING_PARENT_KERNEL_OR_CONSTRAINT_PROOF", "high", False),
        ("PQ2883_2_Cobs", "C_Obs_e or annihilator on im(Dq_Z)", "derive_or_bound", "MISSING_OBSERVED_COFRAME_FUNCTOR_AND_OPERATOR_NORM", "medium", False),
        ("PQ2883_3_product_bound", "C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z", "finite_nonclaim_row", "MISSING_COBS_DQZ_NZ_FACTORS", "fallback", False),
        ("PQ2883_4_arena_projection", "Pi_R0/Pi_gamma/Pi_beta/Pi_R10 projections", "finite_nonclaim_row", "MISSING_ARENA_PROJECTION_FACTORS", "fallback", False),
    ]
    return [
        add_common(
            {
                "queue_id": row_id,
                "target": target,
                "route_type": route_type,
                "current_marker": marker,
                "priority": priority,
                "selected_for_next": selected,
                "accepted_live_input": False,
            }
        )
        for row_id, target, route_type, marker, priority, selected in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2883_0_constraint_law", "conditional constraint/no-pole law recorded", "PASS_CONTROL_ONLY", "law is exact only under parent-signed assumptions", False),
        ("GATE2883_1_constraint_origin", "parent constraint/no-pole action removes R_AB/Z/phi before matter", "FAIL", "origin/class/stress/boundary gates are unsigned", False),
        ("GATE2883_2_no_pole", "no physical residual pole/source remains", "FAIL", "degree count, action descent and boundary silence are missing", False),
        ("GATE2883_3_source_pack", "Dq leak source pack can be scored", "FAIL", "all values are missing/theorem-zero placeholders", False),
        ("GATE2883_4_Cqm_DqZ", "C_qm/Dq_Z product bound has sourced factors", "FAIL", "C_Obs_e, Dq_Z_norm, N_Z and arena Pi factors are missing", False),
        ("GATE2883_5_Z_physical_lock", "formal Z controls measured residual vector", "FAIL", "full-rank/coercive Z-to-R_phys lock is not proved", False),
        ("GATE2883_6_local_GR_Newton", "local GR/Newton reduction follows", "FAIL_CLOSED", "constraint/no-pole proof and physical lock remain incomplete", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": passed,
            }
        )
        for gate_id, criterion, result, reason, passed in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2883_0_constraint_or_leak_import",
                "status": "REFUSED_CONSTRAINT_FIRST_AND_LEAK_PACK_NOT_LIVE",
                "accepted_constraint_theorems": 0,
                "accepted_leak_rows": 0,
                "accepted_product_factors": 0,
                "reason": "constraint/no-pole route is conditional only; Dq leak/source-pack rows and C_qm/Dq_Z product factors contain missing numeric/theorem-zero inputs",
                "runner_ready": False,
                "claim_unlocked": False,
                "score_allowed": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2883_0_constraint", "CONSTRAINT_FIRST_REMAINS_BEST_DERIVATION_IDEA", "it removes visible residuals before q instead of calling them gauge", "keep as theorem target, not a claim"),
        ("DEC2883_1_current_result", "CONSTRAINT_FIRST_NOT_DERIVED_CURRENT_CHAIN", "parent origin, degree count, boundary/source silence and matter/readout descent fail together", "do not promote local GR/Newton"),
        ("DEC2883_2_source_pack", "DQ_LEAK_ARENA_PACK_RETAINED_NONCLAIM", "1669/1670 make leaks arena-ready in schema, but no values are source-backed", "no scoring until rows are numeric or theorem-zero"),
        ("DEC2883_3_next", "TARGET_Z_PHYSICAL_LOCK_OR_FIRST_FACTOR", "local GR needs Z-to-R_phys lock; empirical fallback needs C_Obs_e/Dq_Z/N_Z factors", "attempt physical lock before product-factor sourcing"),
    ]
    return [
        add_common({"decision_id": row_id, "decision": decision, "because": because, "next_action": next_action})
        for row_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2883_0_2884",
                "status": "selected_primary",
                "target_doc": "2884-Y5-R2FR-Z-physical-lock-map-or-first-DqZ-factor-source-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_Z_physical_lock_map_or_first_DqZ_factor_source_row_under_AX1090_2884.py",
                "mission": "attempt the full-rank/coercive Z-to-R_phys lock needed for local GR/Newton; if it fails, fill the first source-ready nonclaim Dq_Z/C_Obs_e/N_Z product-factor row with units, source path and arena projections",
                "forbidden_shortcuts": "no formal-Z-only victory; no coframe-only local-GR claim; no arena scoring while product factors contain MISSING_* placeholders",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    pairs = [
        ("COPY2883_0_synthesis", OUTPUTS["synthesis"], BRANCH_OUTPUTS["synthesis_copy"], "constraint-first synthesis nonclaim copy"),
        ("COPY2883_1_pack", OUTPUTS["source_pack"], BRANCH_OUTPUTS["pack_copy"], "Dq leak arena pack nonclaim copy"),
        ("COPY2883_2_queue", OUTPUTS["product_queue"], BRANCH_OUTPUTS["queue_copy"], "C_qm/Dq_Z product queue nonclaim copy"),
        ("COPY2883_3_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to Z physical-lock target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in pairs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def generated_under_root(paths: list[Path]) -> bool:
    root_resolved = ROOT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "theorem_closed",
        "parent_signed",
        "source_backed",
        "accepted_for_scoring",
        "accepted_live_input",
        "gate_passed",
        "runner_ready",
        "claim_unlocked",
        "score_allowed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    synthesis = rows_by_name["synthesis"]
    no_pole = rows_by_name["no_pole"]
    source_pack = rows_by_name["source_pack"]
    product_queue = rows_by_name["product_queue"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2883_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2883_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2883_2_constraint_law_recorded", any(row["synthesis_id"] == "SYN2883_0_exact_constraint_law" for row in synthesis), "conditional constraint/no-pole law recorded"),
        ("VAL2883_3_constraint_not_promoted", not any(row["theorem_closed"] for row in synthesis), "constraint-first route not promoted"),
        ("VAL2883_4_no_pole_blocked", any(row["gate_id"] == "NP2883_7_verdict" and row["current_status"] == "CERTIFICATE_NOT_CLOSED" for row in no_pole), "no-pole certificate remains blocked"),
        ("VAL2883_5_source_pack_nonclaim", len(source_pack) >= 8 and not any(row["source_backed"] for row in source_pack), "Dq leak source pack remains nonclaim"),
        ("VAL2883_6_product_queue_next", any(row["queue_id"] == "PQ2883_0_Z_physical_lock" and row["selected_for_next"] is True for row in product_queue), "Z physical lock selected as next pressure point"),
        ("VAL2883_7_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "all claim gates fail closed"),
        ("VAL2883_8_runner_refused", runner[0]["status"] == "REFUSED_CONSTRAINT_FIRST_AND_LEAK_PACK_NOT_LIVE" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2883_9_next_target_2884", next_target[0]["next_id"] == "NEXT2883_0_2884" and next_target[0]["selected"] is True, "2884 target selected"),
        ("VAL2883_10_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2883_11_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2883_12_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2883_13_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2883_14_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2883_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2883_16_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2883_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2883 synthesized the constraint-first/no-pole route, kept it nonclaim, retained the Dq arena source pack, and selected Z physical lock or first product-factor sourcing for 2884.",
            "timestamp_utc": now(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    text = f"""# 2883 - Y5 R2FR Constraint-First q Construction Or Dq Leak Source Pack Under AX1090

Status: `Y5_R2FR_2883_constraint_first_not_derived_Dq_pack_retained_Zlock_2884_next`

## Private Verdict

2883 turns the previous constraint-first material into the current R2FR chain.

The clean route is still conceptually right: remove `R_AB/Z/phi` before ordinary matter and the observed quotient `q` see them. If a parent action genuinely supplies that constraint/no-pole mechanism, the local leak dies by derivation, not by vibes.

But the current corpus still does not sign the parent origin, constraint class, no-pole degree count, matter/readout descent, boundary/source silence, or `Z -> R_phys` physical lock. So no local-GR/Newton/PPN/R10/WEP/clock/orbit claim is unlocked.

The useful progress is that the fallback is now concrete: retained `Dq` leaks map into arena-ready nonclaim rows, and the sharp next theorem target is the full-rank/coercive `Z` physical lock. If that lock fails, we source the first product factor in `C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z`.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Constraint-First Synthesis

{md_table(rows_by_name["synthesis"], ["synthesis_id", "statement", "status", "theorem_closed", "parent_signed", "valid_for_claim"])}

## No-Pole Current Gate

{md_table(rows_by_name["no_pole"], ["gate_id", "required_clause", "current_status", "gate_pass", "theorem_closed", "valid_for_claim"])}

## Dq Leak Arena Source Pack

{md_table(rows_by_name["source_pack"], ["source_pack_id", "symbol", "channel", "unit_convention", "priority_arenas", "candidate_value", "source_backed", "valid_for_claim"])}

## C_qm/Dq_Z Product-Bound Queue

{md_table(rows_by_name["product_queue"], ["queue_id", "target", "route_type", "current_marker", "priority", "selected_for_next", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_constraint_theorems", "accepted_leak_rows", "accepted_product_factors", "reason", "runner_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    remove_pycache()
    rows_by_name = {
        "sources": source_register_rows(),
        "synthesis": synthesis_rows(),
        "no_pole": no_pole_rows(),
        "source_pack": source_pack_rows(),
        "product_queue": product_queue_rows(),
        "gates": gate_rows(),
        "runner": runner_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branch_rows)
    rows_by_name["branches"] = branch_rows
    remove_pycache()
    validation = validation_rows(rows_by_name, branch_rows)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name, branch_rows, validation)
    remove_pycache()
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation if row["validation_id"] == "VAL2883_OVERALL")
    print(f"VAL2883_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
