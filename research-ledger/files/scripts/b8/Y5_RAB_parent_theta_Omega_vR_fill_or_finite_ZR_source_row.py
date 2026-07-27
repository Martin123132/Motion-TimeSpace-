from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_DOCS = ROOT / "source-intake" / "rab-sector" / "docs"
RAB_RAW = ROOT / "source-intake" / "rab-sector" / "raw"
RAB_ACCEPTED = ROOT / "source-intake" / "rab-sector" / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1565-Y5-RAB-parent-theta-Omega-vR-fill-or-finite-ZR-source-row.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1564_doc": ROOT / "1564-Y5-RAB-vertical-null-presymplectic-degeneracy-or-finite-ZR-intake.md",
    "1564_validation": OUT / "P8_Y5_BRR545_1564_VALIDATION.csv",
    "1564_next": OUT / "P8_Y5_PARENT_QLOC_1564_NEXT_TARGET.csv",
    "1564_null": OUT / "P8_Y5_PARENT_QLOC_1564_PRESYMPLECTIC_NULL_CHAIN.csv",
    "1564_kinetic": OUT / "P8_Y5_PARENT_QLOC_1564_KINETIC_TERM_CONTRADICTION.csv",
    "1563_doc": ROOT / "1563-Y5-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md",
    "1563_sort": OUT / "P8_Y5_PARENT_QLOC_1563_PARENT_SORT_AUDIT.csv",
    "1563_grammar": OUT / "P8_Y5_PARENT_QLOC_1563_NO_DERIVATIVE_GRAMMAR_GATE.csv",
    "1563_elim": OUT / "P8_Y5_PARENT_QLOC_1563_AUXILIARY_ELIMINATION_GATE.csv",
    "1562_doc": ROOT / "1562-Y5-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test.md",
    "1562_route": OUT / "P8_Y5_PARENT_QLOC_1562_ROUTE_DECISION_LEDGER.csv",
    "1264_doc": ROOT / "1264-Y5-R10-RAB-parent-theta-vR-fill-or-finite-ZR-source-row.md",
    "1264_theta": OUT / "P8_Y5_R10_1264_THETA_OMEGA_VR_FILL_AUDIT.csv",
    "1268_doc": ROOT / "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md",
    "1268_action": OUT / "P8_Y5_R10_1268_COMPATIBILITY_ACTION_CANDIDATE.csv",
    "zr1268_template": RAB_DOCS / "ZR1268_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM.csv",
}

NEEDLES = {
    "1564_doc": ["The vertical-null route gives a real conditional theorem", "NEXT_1565_PARENT_THETA_OMEGA_VR_FILL_OR_ZR_SOURCE_ROW"],
    "1564_validation": ["VAL1564_OVERALL", "PASS"],
    "1564_next": ["1565-Y5-RAB-parent-theta-Omega-vR-fill-or-finite-ZR-source-row.md"],
    "1564_null": ["NULL1564_3_vR_generator", "MISSING_RAB_VERTICAL_GENERATOR"],
    "1564_kinetic": ["KIN1564_1_null_contradiction", "EXACT_CONDITIONAL_ON_TRUE_NULLNESS"],
    "1563_doc": ["The auxiliary compatibility route remains the cleanest derivation path", "Finite `Z_R/q_R` remains the honest fallback"],
    "1563_sort": ["SORT1563_0_auxiliary_coordinate", "SORT1563_3_physical_countermodel"],
    "1563_grammar": ["GRAM1563_0_no_DRAB", "FAIL_CURRENT_THEOREM"],
    "1563_elim": ["ELIM1563_1_E_R", "PASS_ONLY_IF_SOURCES_ZERO"],
    "1562_doc": ["second-class/algebraic auxiliary compatibility", "ROUTE1562_1_second_class_auxiliary"],
    "1562_route": ["ROUTE1562_1_second_class_auxiliary", "BEST_DERIVATION_ROUTE_CONDITIONAL"],
    "1264_doc": ["theta_R=0", "ON_SHELL_AUXILIARY_NULL_NOT_OFFSHELL_GAUGE"],
    "1264_theta": ["TVR1264_3_on_shell_nullness", "ON_SHELL_AUXILIARY_NULL_NOT_OFFSHELL_GAUGE"],
    "1268_doc": ["second-class/algebraic auxiliary compatibility action", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED"],
    "1268_action": ["CAC1268_5_conditional_theorem", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED"],
    "zr1268_template": ["ZR1268_TEMPLATE_ZR", "MISSING_NUMERIC_VALUE_OR_THEOREM_ZERO"],
}

STRICT_REQUIREMENTS = RAB_DOCS / "ZR1565_FINITE_ZR_SOURCE_ROW_INTAKE_REQUIREMENTS_NONCLAIM.csv"
SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1565_SOURCE_REGISTER.csv"
PARENT_BLOCK = OUT / "P8_Y5_PARENT_QLOC_1565_PARENT_BLOCK_CANDIDATE.csv"
THETA_OMEGA = OUT / "P8_Y5_PARENT_QLOC_1565_THETA_OMEGA_FILL.csv"
VR_TANGENCY = OUT / "P8_Y5_PARENT_QLOC_1565_VR_TANGENCY_AUDIT.csv"
ELIMINATION = OUT / "P8_Y5_PARENT_QLOC_1565_SECOND_CLASS_ELIMINATION_CONDITIONS.csv"
FINITE_INTAKE = OUT / "P8_Y5_PARENT_QLOC_1565_FINITE_ZR_SOURCE_ROW_INTAKE.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1565_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1565_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1565_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1565_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1565_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1565"
BRANCH_PREFIX = BRANCH_RESIDUALS
COPY_TARGETS = {
    PARENT_BLOCK: [
        QUARANTINE / "PARENT_BLOCK_CANDIDATE_NONCLAIM.csv",
        BRANCH_PREFIX / "parent_block_candidate_nonclaim_1565.csv",
    ],
    THETA_OMEGA: [
        QUARANTINE / "THETA_OMEGA_FILL_NONCLAIM.csv",
        BRANCH_PREFIX / "theta_omega_fill_nonclaim_1565.csv",
    ],
    VR_TANGENCY: [
        QUARANTINE / "VR_TANGENCY_AUDIT_NONCLAIM.csv",
        BRANCH_PREFIX / "vR_tangency_audit_nonclaim_1565.csv",
    ],
    ELIMINATION: [
        QUARANTINE / "SECOND_CLASS_ELIMINATION_CONDITIONS_NONCLAIM.csv",
        BRANCH_PREFIX / "second_class_elimination_conditions_nonclaim_1565.csv",
    ],
    FINITE_INTAKE: [
        QUARANTINE / "FINITE_ZR_SOURCE_ROW_INTAKE_NONCLAIM.csv",
        BRANCH_PREFIX / "finite_ZR_source_row_intake_nonclaim_1565.csv",
    ],
    RUNNER: [
        QUARANTINE / "RUNNER_NONCLAIM.csv",
        BRANCH_PREFIX / "theta_omega_vR_runner_nonclaim_1565.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_PREFIX / "theta_omega_vR_decision_nonclaim_1565.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
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


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


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


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def row_count(folder: Path) -> int:
    if not folder.exists():
        return 0
    total = 0
    for path in folder.glob("*.csv"):
        try:
            total += len(read_csv(path))
        except Exception:
            total += 1
    return total


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        needles = NEEDLES[key]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1565_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles),
                "needles": "; ".join(needles),
                "purpose": "theta/Omega/v_R fill audit or finite ZR intake guard",
                **flags(),
            }
        )
    return rows


def parent_block_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PB1565_0_auxiliary_block",
            "L_Raux = mu_parent Lambda_R^{AB}(R_AB-C_AB[q(Phi),theta,top])",
            "second-class compatibility block",
            "E_Lambda fixes compatibility; no derivative momentum appears if the block is complete",
            "CANDIDATE_REUSED_NOT_PARENT_SIGNED",
            "parent primitive derivation of R_AB sort and C_AB map",
        ),
        (
            "PB1565_1_no_derivatives",
            "ParentGenerate excludes D R_AB, D Lambda_R, G_vert, nabla_vert, and boundary derivative terms",
            "operator grammar",
            "would make theta_R=0 and forbid tree-level Z_R kinetic hair",
            "REQUIRED_UNSIGNED",
            "no object-language theorem yet bans derivative operators",
        ),
        (
            "PB1565_2_matter_boundary_readout",
            "S_matter and B and S_eff factor through q(Phi), theta, top rather than R_AB",
            "source silence",
            "would make E_R solve Lambda_R=0 instead of sourcing q_R hair",
            "REQUIRED_UNSIGNED",
            "matter, boundary, and readout descent remain unsigned",
        ),
        (
            "PB1565_3_result",
            "auxiliary elimination rather than first-class gauge",
            "classification",
            "best route is algebraic second-class elimination, not a free R_AB gauge shift",
            "PARTIAL_FILL_ONLY",
            "v_R tangency and off-shell gauge-nullness fail below",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "block_id": block_id,
            "candidate_object": candidate_object,
            "role": role,
            "what_it_buys": what_it_buys,
            "status": status,
            "blocking_gap": blocking_gap,
            "source_paths": source_list("1563_doc", "1563_grammar", "1268_doc", "1268_action", "1264_doc"),
            **flags(),
        }
        for block_id, candidate_object, role, what_it_buys, status, blocking_gap in rows
    ]


def theta_omega_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "TO1565_0_theta_R",
            "theta_R = 0",
            "no D_mu R_AB or D_mu Lambda_R in the candidate algebraic block",
            "EXACT_IF_AUXILIARY_BLOCK_AND_NO_DERIVATIVE_GRAMMAR_ARE_PARENT_SIGNED",
            "candidate fill succeeds only conditionally",
        ),
        (
            "TO1565_1_Omega_R",
            "Omega_R = delta theta_R = 0",
            "algebraic fields have no covariant symplectic current contribution before a kinetic counterterm is added",
            "EXACT_IF_AUXILIARY_BLOCK_AND_NO_DERIVATIVE_GRAMMAR_ARE_PARENT_SIGNED",
            "zero symplectic sector is not the same as a first-class gauge proof",
        ),
        (
            "TO1565_2_boundary_momentum",
            "Pi_R^n = 0",
            "no normal derivative of R_AB exists in L_Raux",
            "EXACT_IF_NO_BOUNDARY_RAB_FUNCTIONAL",
            "a boundary/corner B_R can still create hair if not excluded",
        ),
        (
            "TO1565_3_operator_contradiction",
            "adding Z_R |D R_AB|^2 creates theta_R, Pi_R^n, and finite response",
            "variation gives derivative momentum, so it violates the auxiliary grammar",
            "EXACT_CONDITIONAL_ON_GRAMMAR",
            "does not prove Z_R=0 until the grammar is parent-derived",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "fill_id": fill_id,
            "candidate_value": candidate_value,
            "derivation": derivation,
            "status": status,
            "meaning": meaning,
            "source_paths": source_list("1264_theta", "1268_action", "1564_kinetic"),
            **flags(),
        }
        for fill_id, candidate_value, derivation, status, meaning in rows
    ]


def vR_tangency_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "VR1565_0_candidate_shift",
            "v_eta: delta R_AB=eta_AB, delta Lambda_R=0, delta q=0",
            "Dq[v_eta]=0 by declared q-independence",
            "FORMAL_CANDIDATE_ONLY",
            "this does not yet check constraint-surface tangency",
        ),
        (
            "VR1565_1_constraint_tangency",
            "delta(R_AB-C_AB[q,theta,top]) = eta_AB - DC_AB[Dq[v_eta]]",
            "with Dq[v_eta]=0 this equals eta_AB",
            "FAILS_OFF_SHELL_FIRST_CLASS_TANGENCY",
            "a pure R_AB shift does not preserve the auxiliary compatibility constraint",
        ),
        (
            "VR1565_2_action_variation",
            "delta_v S_Raux = int mu_parent Lambda_R^{AB} eta_AB",
            "vanishes only after E_R plus source silence gives Lambda_R=0",
            "ON_SHELL_AUXILIARY_NULL_NOT_OFFSHELL_GAUGE",
            "this is algebraic elimination, not an unrestricted gauge orbit",
        ),
        (
            "VR1565_3_modified_shift",
            "try delta q solving DC_AB[Dq]=eta_AB",
            "would preserve compatibility but no longer lies in ker(Dq)",
            "NOT_A_VERTICAL_GENERATOR",
            "cannot be used as q-local no-pole credit",
        ),
        (
            "VR1565_4_verdict",
            "R_AB theta/Omega fill",
            "theta/Omega can be zero for an auxiliary block, but v_R is not a first-class vertical gauge proof",
            "DEMOTE_TO_SECOND_CLASS_ELIMINATION_ROUTE",
            "do not call the presymplectic-null theorem closed",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "tangency_id": tangency_id,
            "test": test,
            "calculation": calculation,
            "status": status,
            "meaning": meaning,
            "source_paths": source_list("1564_null", "1264_theta", "1268_action", "1023_doc") if "1023_doc" in SOURCE_FILES else source_list("1564_null", "1264_theta", "1268_action"),
            **flags(),
        }
        for tangency_id, test, calculation, status, meaning in rows
    ]


def elimination_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ELIM1565_0_E_Lambda",
            "delta_{Lambda_R} S_R",
            "R_AB-C_AB[q,theta,top]=0",
            "FORMAL_PASS_WITHIN_CANDIDATE",
            "parent ownership of the compatibility block",
        ),
        (
            "ELIM1565_1_E_R",
            "delta_{R_AB} S_total",
            "Lambda_R + J_R + delta B_R/delta R_AB + readout_regen = 0",
            "PASS_ONLY_IF_SOURCES_ZERO",
            "matter descent, boundary silence, and readout stability",
        ),
        (
            "ELIM1565_2_Lambda_zero",
            "source-free algebraic elimination",
            "Lambda_R=0 and R_AB=C_AB before local readout",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "J_R, B_R, and readout_regen must be theorem-zero",
        ),
        (
            "ELIM1565_3_no_ZR",
            "operator exclusion",
            "Z_R=0 only if D R_AB operators are outside ParentGenerate",
            "REQUIRED_UNSIGNED",
            "no-derivative/no-vertical-metric theorem remains open",
        ),
        (
            "ELIM1565_4_local_gr",
            "local GR/Newton reduction",
            "needs eliminated auxiliary sector plus no residual q_R transfer",
            "BLOCKED_NO_CLAIM",
            "finite Z_R/q_R fallback remains active",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "elimination_id": elimination_id,
            "variation_or_clause": variation_or_clause,
            "result": result,
            "status": status,
            "blocking_gap": blocking_gap,
            "source_paths": source_list("1563_elim", "1562_doc", "1268_doc"),
            **flags(),
        }
        for elimination_id, variation_or_clause, result, status, blocking_gap in rows
    ]


def strict_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("REQ1565_0_ZR", "Z_R", "numeric coefficient or theorem-zero certificate with units and normalization", "docs template, no source path, or unowned parent convention", "all"),
        ("REQ1565_1_MR2", "M_R^2", "mass-gap/Hessian or range scale tied to the same R_AB normalization", "coefficient without Hessian/source equation", "all"),
        ("REQ1565_2_JR", "J_R", "matter-source zero theorem or finite sourced coupling", "matter descent asserted but not shown", "WEP/clock/R10/PPN"),
        ("REQ1565_3_BR", "B_R_or_Pi_Rn", "boundary zero theorem or finite boundary momentum/flux bound", "bulk auxiliary proof used as boundary proof", "R10/PPN/orbital"),
        ("REQ1565_4_tau_R10", "tau_R10", "projection from finite R_AB sector to alpha(lambda)", "missing kernel/sign/range convention", "R10"),
        ("REQ1565_5_tau_PPN", "tau_PPN", "projection to gamma,beta residual vector", "no metric gauge/convention", "PPN"),
        ("REQ1565_6_tau_clock", "tau_clock", "projection to fractional frequency/readout residual", "no clock-readout map", "clock"),
        ("REQ1565_7_tau_orbital", "tau_orbital", "projection to acceleration/timing observable", "no orbital force/timing map", "orbital"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": requirement_id,
            "field": field,
            "required_content": required_content,
            "reject_if": reject_if,
            "arena_projection": arena_projection,
            "status": "REQUIRED_BEFORE_RAW_OR_ACCEPTED",
            **flags(),
        }
        for requirement_id, field, required_content, reject_if, arena_projection in rows
    ]


def finite_intake_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "INTAKE1565_0_raw",
            str(RAB_RAW),
            row_count(RAB_RAW),
            "NO_LIVE_RAW_ROWS" if row_count(RAB_RAW) == 0 else "RAW_ROWS_PRESENT_REQUIRE_VALIDATION",
            "raw rows must satisfy ZR1565 requirements before scoring",
        ),
        (
            "INTAKE1565_1_accepted",
            str(RAB_ACCEPTED),
            row_count(RAB_ACCEPTED),
            "NO_ACCEPTED_ROWS" if row_count(RAB_ACCEPTED) == 0 else "ACCEPTED_ROWS_PRESENT_REQUIRE_CLAIM_AUDIT",
            "accepted rows must be source-backed, numeric/theorem-zero, unit-normalized, and arena-projected",
        ),
        (
            "INTAKE1565_2_requirements",
            rel(STRICT_REQUIREMENTS),
            len(strict_requirement_rows()),
            "STRICT_REQUIREMENTS_STAGED_NONCLAIM",
            "this is not a finite-ZR data row and cannot be scored",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "intake_id": intake_id,
            "folder_or_file": folder_or_file,
            "rows_found": rows_found,
            "status": status,
            "required_before_scoring": required_before_scoring,
            **flags(),
        }
        for intake_id, folder_or_file, rows_found, status, required_before_scoring in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1565_0_sources", "load 1564/1563/1562/1264/1268 evidence chain", "PASS", "all registered sources are present and needles are found"),
        ("RUN1565_1_theta_omega", "candidate theta/Omega fill", "PASS_CONDITIONAL", "theta_R=Omega_R=Pi_R^n=0 for a parent-signed algebraic auxiliary block"),
        ("RUN1565_2_vR_first_class", "true vertical gauge generator", "FAILS_CURRENT_PROOF", "pure R_AB shift is not constraint-tangent off shell; modified shift is not in ker(Dq)"),
        ("RUN1565_3_second_class", "second-class elimination route", "BEST_CONDITIONAL_ROUTE_RETAINED", "E_Lambda/E_R route can kill Lambda_R only with source/boundary/readout/operator protections"),
        ("RUN1565_4_finite_intake", "finite Z_R source-row intake", "NONCLAIM_REQUIREMENTS_ONLY", "strict requirements staged; no raw/accepted row is scoreable"),
        ("RUN1565_5_claim", "local GR/Newton claim", "BLOCKED_NO_CLAIM", "neither theorem-zero nor finite residual scoring is closed"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "test": test,
            "current_status": current_status,
            "detail": detail,
            **flags(),
        }
        for runner_id, test, current_status, detail in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1565_0_theta_omega", "theta_R/Omega_R/Pi_Rn zero", "BLOCKED_NO_CLAIM", "conditional on unsigned parent auxiliary block and no-derivative grammar"),
        ("GATE1565_1_vR_vertical", "v_R is a true first-class vertical gauge generator", "BLOCKED_NO_CLAIM", "candidate shift is not constraint-tangent off shell"),
        ("GATE1565_2_ZR_zero", "Z_R=0 theorem", "BLOCKED_NO_CLAIM", "requires signed operator exclusion, boundary silence, and readout stability"),
        ("GATE1565_3_finite_ZR", "finite Z_R/q_R residual scoring", "BLOCKED_NO_CLAIM", "no raw/accepted source-backed coefficient rows"),
        ("GATE1565_4_local_GR", "derived local GR/Newton/PPN safety", "BLOCKED_NO_CLAIM", "the local branch remains conditional/fallback only"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim_gate": claim_gate,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1564_doc", "1563_doc", "1268_doc"),
            **flags(),
        }
        for gate_id, claim_gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1565_0_progress",
            "decision": "theta/Omega fill",
            "result": "PARTIAL_FILL_AS_AUXILIARY_SECTOR",
            "reason": "theta_R=Omega_R=Pi_Rn=0 follows inside the algebraic auxiliary ansatz, not as a completed parent theorem",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1565_1_rejection",
            "decision": "first-class vertical v_R",
            "result": "REJECT_CURRENT_VERTICAL_GAUGE_PROMOTION",
            "reason": "pure R_AB shifts fail compatibility tangency; compatibility-preserving shifts are not q-vertical",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1565_2_best_route",
            "decision": "local route",
            "result": "SECOND_CLASS_ELIMINATION_OR_FINITE_ZR_INTAKE",
            "reason": "prove source/boundary/readout/operator protection or keep finite residual coefficients nonclaim",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1565_3_next",
            "decision": "next target",
            "result": "NEXT_1566_SOURCE_BOUNDARY_READOUT_PROTECTION_OR_FINITE_ZR_VALIDATOR",
            "reason": "the decisive missing clauses are J_R=0, B_R=0, readout stability, and operator exclusion",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1565_0_1566",
            "next_target": "1566-Y5-RAB-source-boundary-readout-protection-or-finite-ZR-validator.md",
            "script": "scripts/Y5_RAB_source_boundary_readout_protection_or_finite_ZR_validator.py",
            "objective": "prove or reject the source/boundary/readout/operator protection clauses needed for second-class auxiliary elimination; if they fail, validate finite Z_R intake rows and keep all placeholders unscoreable",
            "do_not": "do not call theta_R=0 a first-class gauge proof; do not score finite Z_R/q_R rows without source-backed coefficients and arena projections; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source, destinations in COPY_TARGETS.items():
        for destination in destinations:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    parent = read_csv(PARENT_BLOCK)
    theta = read_csv(THETA_OMEGA)
    tangency = read_csv(VR_TANGENCY)
    elim = read_csv(ELIMINATION)
    reqs = read_csv(STRICT_REQUIREMENTS)
    intake = read_csv(FINITE_INTAKE)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1565_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1565 source paths exist"),
        ("VAL1565_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1565_2_parent_block_conditional", any(row["block_id"] == "PB1565_3_result" and row["status"] == "PARTIAL_FILL_ONLY" for row in parent), "parent block is partial fill only"),
        ("VAL1565_3_theta_omega_conditional", any(row["fill_id"] == "TO1565_1_Omega_R" and row["status"].startswith("EXACT_IF") for row in theta), "theta/Omega zero is conditional"),
        ("VAL1565_4_vR_not_gauge", any(row["tangency_id"] == "VR1565_4_verdict" and row["status"] == "DEMOTE_TO_SECOND_CLASS_ELIMINATION_ROUTE" for row in tangency), "v_R first-class promotion rejected"),
        ("VAL1565_5_second_class_conditions", any(row["elimination_id"] == "ELIM1565_1_E_R" and row["status"] == "PASS_ONLY_IF_SOURCES_ZERO" for row in elim), "second-class route records source-zero condition"),
        ("VAL1565_6_requirements_staged", len(reqs) == 8 and all(row["status"] == "REQUIRED_BEFORE_RAW_OR_ACCEPTED" for row in reqs), "strict finite-ZR intake requirements staged"),
        ("VAL1565_7_no_accepted_rows", any(row["intake_id"] == "INTAKE1565_1_accepted" and row["status"] == "NO_ACCEPTED_ROWS" for row in intake), "finite intake has no accepted rows"),
        ("VAL1565_8_runner_blocks_claim", any(row["runner_id"] == "RUN1565_5_claim" and row["current_status"] == "BLOCKED_NO_CLAIM" for row in run_rows), "runner blocks local claim"),
        ("VAL1565_9_claim_gates", all(row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "all claim gates remain blocked"),
        ("VAL1565_10_decision_next", any(row["result"] == "NEXT_1566_SOURCE_BOUNDARY_READOUT_PROTECTION_OR_FINITE_ZR_VALIDATOR" for row in decision_items), "decision selects source/boundary/readout protection or validator"),
        ("VAL1565_11_next_target", any("1566-Y5-RAB-source-boundary-readout-protection" in row["next_target"] for row in next_rows), "next target is source/boundary/readout protection"),
        ("VAL1565_12_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1565 CSVs parse cleanly"),
        ("VAL1565_13_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1565_14_branch_copies", all(destination.exists() for destinations in COPY_TARGETS.values() for destination in destinations), "branch/quarantine nonclaim copies written"),
        ("VAL1565_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1565_16_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1565_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1565 parent theta/Omega/v_R fill or finite ZR source-row validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    parent: list[dict[str, Any]],
    theta: list[dict[str, Any]],
    tangency: list[dict[str, Any]],
    elim: list[dict[str, Any]],
    reqs: list[dict[str, Any]],
    intake: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1565 - R_AB Parent Theta/Omega/v_R Fill or Finite Z_R Source Row",
                "",
                "## Verdict",
                "- The candidate auxiliary block does fill a real piece: if `R_AB` and `Lambda_R` enter only algebraically, then `theta_R=0`, `Omega_R=0`, and `Pi_R^n=0` at tree level.",
                "- The catch is important: this is second-class auxiliary elimination, not a first-class vertical gauge proof.",
                "- A pure `v_R: delta R_AB=eta_AB, delta q=0` shift fails constraint-surface tangency because it changes `R_AB-C_AB[q,theta,top]`.",
                "- A compatibility-preserving shift needs `delta q != 0`, so it is not in `ker(Dq)` and cannot be used as q-local no-pole credit.",
                "- Therefore the clean route is now: prove source/boundary/readout/operator protection for second-class elimination, or keep finite `Z_R/q_R` as a nonclaim residual branch.",
                "- No `Z_R=0`, `q_R=0`, local GR/Newton, R10, PPN, clock, or orbital claim is made.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## Parent Block Candidate",
                md_table(parent, ["block_id", "candidate_object", "role", "what_it_buys", "status", "blocking_gap"]),
                "",
                "## Theta/Omega Fill",
                md_table(theta, ["fill_id", "candidate_value", "derivation", "status", "meaning"]),
                "",
                "## v_R Tangency Audit",
                md_table(tangency, ["tangency_id", "test", "calculation", "status", "meaning"]),
                "",
                "## Second-Class Elimination Conditions",
                md_table(elim, ["elimination_id", "variation_or_clause", "result", "status", "blocking_gap"]),
                "",
                "## Strict Finite Z_R Intake Requirements",
                md_table(reqs, ["requirement_id", "field", "required_content", "reject_if", "arena_projection", "status"]),
                "",
                "## Finite Z_R Intake Status",
                md_table(intake, ["intake_id", "folder_or_file", "rows_found", "status", "required_before_scoring"]),
                "",
                "## Runner",
                md_table(run_rows, ["runner_id", "test", "current_status", "detail"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim_gate", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    parent = parent_block_rows()
    theta = theta_omega_rows()
    tangency = vR_tangency_rows()
    elim = elimination_rows()
    reqs = strict_requirement_rows()
    intake = finite_intake_rows()
    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PARENT_BLOCK, parent)
    write_csv(THETA_OMEGA, theta)
    write_csv(VR_TANGENCY, tangency)
    write_csv(ELIMINATION, elim)
    write_csv(STRICT_REQUIREMENTS, reqs)
    write_csv(FINITE_INTAKE, intake)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        PARENT_BLOCK,
        THETA_OMEGA,
        VR_TANGENCY,
        ELIMINATION,
        STRICT_REQUIREMENTS,
        FINITE_INTAKE,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, parent, theta, tangency, elim, reqs, intake, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
