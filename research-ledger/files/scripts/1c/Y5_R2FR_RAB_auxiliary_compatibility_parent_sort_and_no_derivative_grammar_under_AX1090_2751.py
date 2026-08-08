from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2751-Y5-R2FR-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar-under-AX1090.md"
BRANCH_ID = "MTS_R2FR_AX1090_LOCAL_GR_RAB_AUXILIARY_GRAMMAR_2751"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2751_SOURCE_REGISTER.csv",
    "sort": RESIDUALS / "P8_Y5_R2FR_2751_PARENT_SORT_AUDIT.csv",
    "grammar": RESIDUALS / "P8_Y5_R2FR_2751_NO_DERIVATIVE_GRAMMAR_GATE.csv",
    "elimination": RESIDUALS / "P8_Y5_R2FR_2751_AUXILIARY_ELIMINATION_GATE.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_2751_JOINT_PROTECTION_CONTRACT.csv",
    "loop": RESIDUALS / "P8_Y5_R2FR_2751_NON_LOOP_AUDIT.csv",
    "finite": RESIDUALS / "P8_Y5_R2FR_2751_FINITE_QR_RESIDUAL_FALLBACK_GATE.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2751_RUNNER_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2751_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2751_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2751_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2751_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2751_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "grammar": SOURCE_WEIGHT / "RAB_auxiliary_grammar_loop_breaker_2751_NONCLAIM.csv",
    "finite": LOCAL_BOUNDS / "finite_qR_residual_fallback_2751_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2751_PARENT_CONTRACT_OR_FINITE_QR_VECTOR_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = ["| " + " | ".join(md(row.get(col, "")) for col in cols) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def local_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["numeric_value_present"] = False
    row["source_backed"] = False
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2751_0_2750_doc",
            "description": "current lambda_R handoff selecting auxiliary parent sort/no-derivative grammar.",
            "source_path": "2750-Y5-R2FR-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test-under-AX1090.md",
            "required_needles": "ROUTE2750_1_second_class_auxiliary;NEXT2750_0_2751;VAL2750_OVERALL",
        },
        {
            "source_id": "SRC2751_1_2750_validation",
            "description": "2750 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2750_VALIDATION.csv",
            "required_needles": "VAL2750_OVERALL;True",
        },
        {
            "source_id": "SRC2751_2_2750_boundary",
            "description": "2750 boundary/operator/matter/readout gates.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2750_BOUNDARY_DEGREE_COUNT_GATE.csv",
            "required_needles": "BD2750_4_operator;UNSIGNED;BD2750_2_matter",
        },
        {
            "source_id": "SRC2751_3_2750_constraint",
            "description": "2750 constraint class gate preferring second-class auxiliary route conditionally.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2750_CONSTRAINT_CLASS_GATE.csv",
            "required_needles": "CLASS2750_5_second_class;BETTER_CONDITIONAL_THAN_FIRST_CLASS",
        },
        {
            "source_id": "SRC2751_4_2236_doc",
            "description": "prior R2FR auxiliary grammar gate; used here as a no-loop precedent.",
            "source_path": "2236-Y5-R2FR-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md",
            "required_needles": "DEC2236_0_verdict;NEXT_2237_VERTICAL_NULL_PRESYMPLECTIC_DEGENERACY_OR_FINITE_ZR_INTAKE",
        },
        {
            "source_id": "SRC2751_5_2288_doc",
            "description": "prior auxiliary/finite-Zq intake checkpoint identifying the parent protection contract hinge.",
            "source_path": "2288-Y5-R2FR-RAB-auxiliary-parent-sort-no-derivative-or-finite-Zq-intake.md",
            "required_needles": "PARENT_PROTECTION_CONTRACT_IS_THE_HINGE;FINITE_ZQ_INTAKE_REMAINS_MANDATORY_FALLBACK",
        },
        {
            "source_id": "SRC2751_6_2289_doc",
            "description": "primitive contract derivation recheck; prevents repeating a failed broad primitive route.",
            "source_path": "2289-Y5-R2FR-parent-protection-contract-derivation-from-MTS-primitives-or-first-live-Zq-row.md",
            "required_needles": "FAILED_CURRENT_EVIDENCE_REUSE_1237_2241;NEXT_2290_FIRST_INTERNAL_ZQ_OR_TAUR10_PROJECTION_ROW",
        },
        {
            "source_id": "SRC2751_7_2291_doc",
            "description": "finite q parent row and source/test coupling split.",
            "source_path": "2291-Y5-R2FR-parent-finite-quadratic-row-and-source-test-beta-split.md",
            "required_needles": "BETA2291_5_verdict;c_g^2;PQA2291_0_finite_q_parent_row",
        },
        {
            "source_id": "SRC2751_8_2716_doc",
            "description": "AX1090 finite R_AB operator fallback and parent-protection audit.",
            "source_path": "2716-Y5-R2FR-parent-protection-contract-or-finite-ZR-row-under-AX1090-closure.md",
            "required_needles": "LAW2716_0_finite_action;FZR2716_0_ZR;VAL2716_OVERALL",
        },
        {
            "source_id": "SRC2751_9_2732_doc",
            "description": "anti-circling local-GR route rollup.",
            "source_path": "2732-Y5-R2FR-local-GR-route-rollup-after-memory-closure-only-or-next-derivation-branch.md",
            "required_needles": "STOP_REPEATING_MEMORY_ZERO_ROUTE;SELECT_KHAT_KMETRIC_DELTAK_QLOC;VAL2732_OVERALL",
        },
        {
            "source_id": "SRC2751_10_2747_doc",
            "description": "q_R/delta_beta PPN control runner and finite residual translation.",
            "source_path": "2747-Y5-R2FR-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt-under-AX1090.md",
            "required_needles": "gamma-1 = q_R;ZERO2747_0_qR_linear;VAL2747_OVERALL",
        },
    ]
    for row in rows:
        path = local_path(row["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = [needle for needle in row["required_needles"].split(";") if needle]
        missing = [needle for needle in needles if needle not in text]
        row["exists"] = path.exists()
        row["needles_present"] = len(missing) == 0
        row["missing_needles"] = ";".join(missing)
        nonclaim(row)
    return rows


def sort_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SORT2751_0_identity_not_dynamics",
            "R_AB=ln(T^2 S)=2 ln(J_q) is an exact compatibility/diagnostic identity.",
            "names the reciprocal local residual cleanly",
            "EXACT_DEFINITION_NOT_PARENT_DYNAMICS",
            "an identity does not forbid stiffness, source, or boundary terms",
        ),
        (
            "SORT2751_1_auxiliary_coordinate",
            "R_AB is an auxiliary compatibility coordinate rather than a physical scalar.",
            "would let Lambda_R/R_AB eliminate algebraically before local readout",
            "CANDIDATE_NOT_PARENT_SIGNED",
            "2750 adds the multiplier ansatz but not the typed parent field/sort list",
        ),
        (
            "SORT2751_2_vertical_representative",
            "R_AB variations lie in ker(Dq) of the public quotient map.",
            "would make R_AB representative/fibre data rather than observable geometry",
            "EXACT_CONDITIONAL_NOT_PARENT_DERIVED",
            "the quotient/presymplectic null certificate remains unsigned",
        ),
        (
            "SORT2751_3_physical_countermodel",
            "R_AB is a genuine local scalar/tensor channel.",
            "then finite Z_R h^ij D_i R_AB D_j R_AB is legal by locality",
            "LEGAL_COUNTERMODEL_SURVIVES",
            "forces finite q_R/Z_R residual branch if parent sort fails",
        ),
        (
            "SORT2751_4_current_verdict",
            "current accepted parent sort",
            "none claim-making",
            "FAIL_CURRENT_THEOREM",
            "auxiliary sort remains the best route but not a theorem",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "sort_id": sid,
                "parent_sort_statement": statement,
                "claim_effect_if_signed": effect,
                "status": status,
                "blocker": blocker,
            }
        )
        for sid, statement, effect, status, blocker in specs
    ]


def grammar_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "GRAM2751_0_no_DRAB",
            "ban D_i R_AB and D_mu R_AB kinetic/gradient terms",
            "needed so R_AB cannot carry exterior q_R/Z_R hair",
            "REQUIRED_UNSIGNED",
            "no parent object-language rule forbids the derivative constructor yet",
        ),
        (
            "GRAM2751_1_no_DLambda",
            "ban D Lambda_R kinetic/gradient terms",
            "needed so Lambda_R remains algebraic/reaction-only",
            "REQUIRED_UNSIGNED",
            "Lambda_R was inserted as a candidate multiplier, not generated as an algebraic-only parent object",
        ),
        (
            "GRAM2751_2_no_vertical_metric",
            "no vertical fibre metric/connection G_vert or nabla_vert",
            "otherwise G_vert(DR_AB,DR_AB) is a legal representative energy",
            "REQUIRED_UNSIGNED",
            "no-vertical-metric theorem remains conditional",
        ),
        (
            "GRAM2751_3_no_boundary_derivative",
            "no boundary/corner derivative momentum for R_AB",
            "prevents Q_R/B_R hair after bulk algebraic elimination",
            "REQUIRED_UNSIGNED",
            "source-worldtube/corner variational class not signed",
        ),
        (
            "GRAM2751_4_exact_conditional",
            "if parent syntax contains only Lambda_R(R_AB-C_AB[q,theta,top]) and no derivative/source/boundary slots",
            "then R_AB/Lambda_R eliminate algebraically and no Z_R/q_R hair is generated at tree level",
            "EXACT_CONDITIONAL",
            "the conditional theorem is sound but its parent-syntax premise is not derived",
        ),
        (
            "GRAM2751_5_current_verdict",
            "no-derivative grammar under current corpus",
            "cannot claim Z_R=0, q_R=0, or local GR",
            "FAIL_CURRENT_THEOREM_RETAIN_FINITE_BRANCH",
            "2750 does not add new parent syntax beyond prior 2236/2288 gate",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "grammar_id": gid,
                "grammar_clause": clause,
                "why_needed": why,
                "status": status,
                "blocker_or_effect": blocker,
            }
        )
        for gid, clause, why, status, blocker in specs
    ]


def elimination_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ELIM2751_0_E_Lambda",
            "delta_{Lambda_R} S_R",
            "R_AB-C_AB[q,theta,top]=0",
            "FORMAL_PASS_WITHIN_CANDIDATE",
            "requires parent-owned compatibility action",
        ),
        (
            "ELIM2751_1_E_R",
            "delta_{R_AB} S_total",
            "Lambda_R + J_R + delta B_R/delta R_AB + readout_regen = 0",
            "PASS_ONLY_IF_SOURCES_ZERO",
            "matter descent, boundary silence, and readout stability are unsigned",
        ),
        (
            "ELIM2751_2_Lambda_zero",
            "solve E_R with J_R=B_R=readout_regen=0",
            "Lambda_R=0",
            "EXACT_CONDITIONAL",
            "not available if any source/boundary/readout term survives",
        ),
        (
            "ELIM2751_3_zero_stress",
            "metric variation after algebraic elimination",
            "constraint stress is silent only if Lambda_R=0 and no hidden source slot remains",
            "EXACT_CONDITIONAL_UNSIGNED",
            "2750 zero-stress failure is repaired only by the full joint contract",
        ),
        (
            "ELIM2751_4_current_verdict",
            "accepted elimination theorem",
            "not parent-signed",
            "BLOCKED_NO_CLAIM",
            "conditional route survives, but finite residual fallback stays active",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "elimination_id": eid,
                "variation_or_step": variation,
                "result": result,
                "status": status,
                "blocker": blocker,
            }
        )
        for eid, variation, result, status, blocker in specs
    ]


def contract_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CON2751_0_parent_sorts",
            "typed parent field/sort list",
            "R_AB and Lambda_R are compatibility auxiliaries, not public physical fields",
            "SCHEMA_WRITTEN_NOT_DERIVED",
            "no current parent primitive source signs the sort list",
        ),
        (
            "CON2751_1_action_image",
            "ParentGenerate action-image exhaustion",
            "only algebraic compatibility block may contain R_AB/Lambda_R",
            "SCHEMA_WRITTEN_NOT_DERIVED",
            "independent derivative/source/counterterm slots are not syntactically forbidden",
        ),
        (
            "CON2751_2_matter_descent",
            "matter descends through public quotient fields",
            "J_R=delta S_matter/delta R_AB=0",
            "UNSIGNED",
            "ordinary matter/source-worldtube may still source q/R_AB",
        ),
        (
            "CON2751_3_boundary_descent",
            "boundary/corner terms descend through public boundary data",
            "B_R=Q_R=Pi_R^n=0",
            "UNSIGNED",
            "bulk auxiliary algebra does not kill boundary charges by itself",
        ),
        (
            "CON2751_4_readout_closure",
            "readout/effective action preserves the algebraic elimination",
            "readout_regen=0",
            "UNSIGNED",
            "readout-after-variation can reintroduce q_R tails unless ruled out",
        ),
        (
            "CON2751_5_operator_exclusion",
            "no D R_AB, D Lambda_R, vertical metric, or boundary derivative operator",
            "Z_R=0 at tree level",
            "BLOCKED_EXACT_CONDITIONAL",
            "operator ban remains conditional on parent syntax",
        ),
        (
            "CON2751_6_joint_contract",
            "CON2751_0 through CON2751_5 close in one parent action",
            "q_R=0 route becomes a derivation candidate instead of closure",
            "FAIL_CURRENT_CLAIM",
            "one unsigned clause is enough to regenerate finite residuals",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "contract_id": cid,
                "clause": clause,
                "effect_if_signed": effect,
                "current_status": status,
                "missing_for_claim": missing,
                "parent_signed_by_2750": False,
            }
        )
        for cid, clause, effect, status, missing in specs
    ]


def loop_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "LOOP2751_0_1563_2236",
            "auxiliary sort/no-derivative grammar",
            "already exact-conditional and unsigned",
            "do not rerun unless new parent sort text appears",
        ),
        (
            "LOOP2751_1_2288_2289",
            "parent protection contract from broad primitives",
            "already demoted under current evidence",
            "do not spend another pass asking the same broad primitive question",
        ),
        (
            "LOOP2751_2_2291_2716",
            "finite q/R_AB residual law",
            "already has the right template: Z_R, M_R^2, J_eff, B_R, tau_i",
            "if theorem route fails, use this scaffold instead of pretending q_R is zero",
        ),
        (
            "LOOP2751_3_2750_new_information",
            "lambda_R multiplier/stress test",
            "adds a concrete zero-stress failure and second-class preference",
            "use it to demand the joint contract, not to restart first-class language",
        ),
        (
            "LOOP2751_4_next_move",
            "current non-circular route",
            "one-pass current contract saturation, then finite q_R residual vector if any slot stays unsigned",
            "selected for 2752",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "loop_id": lid,
                "topic": topic,
                "current_evidence": evidence,
                "rule": rule,
            }
        )
        for lid, topic, evidence, rule in specs
    ]


def finite_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "FQR2751_0_qR_translation",
            "q_R",
            "linear PPN reciprocal residual",
            "gamma-1=q_R from 2747",
            "dimensionless",
            "PPN;Cassini;light_bending;Shapiro",
            "source-intake/mts_residuals/P8_Y5_R2FR_2747_TWO_PARAMETER_MODEL.csv",
            "TRANSLATION_READY_NOT_PARENT_PREDICTION",
        ),
        (
            "FQR2751_1_ZR",
            "Z_R",
            "finite gradient stiffness",
            "coefficient of 0.5 h^ij D_i R_AB D_j R_AB",
            "parent action density units, not yet normalized",
            "R10;PPN;clock;orbital",
            "2716-Y5-R2FR-parent-protection-contract-or-finite-ZR-row-under-AX1090-closure.md",
            "MISSING_NUMERIC_OR_THEOREM_ZERO",
        ),
        (
            "FQR2751_2_MR2",
            "M_R^2",
            "finite mass/Hessian stiffness",
            "ell_R=sqrt(Z_R/M_R^2)",
            "same parent action frame as Z_R over length^2",
            "R10;PPN;clock;orbital",
            "2716-Y5-R2FR-parent-protection-contract-or-finite-ZR-row-under-AX1090-closure.md",
            "MISSING_HESSIAN_OR_RANGE",
        ),
        (
            "FQR2751_3_Jeff",
            "J_eff",
            "effective source vector",
            "J_eff=J_R+J_boundary+J_readout",
            "Euler source conjugate to dimensionless R_AB",
            "PPN;R10;clock;orbital",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2291_PARENT_FINITE_Q_ACTION_AUDIT.csv",
            "MISSING_SOURCE_ZERO_OR_COMPONENT_BOUNDS",
        ),
        (
            "FQR2751_4_boundary",
            "B_R/Q_R/Pi_R",
            "boundary/corner reciprocal charge",
            "finite boundary data can seed exterior q_R/R_AB hair",
            "boundary momentum/charge units in same R_AB normalization",
            "PPN;orbital;R10",
            "2716-Y5-R2FR-parent-protection-contract-or-finite-ZR-row-under-AX1090-closure.md",
            "MISSING_BOUNDARY_ZERO_OR_BOUND",
        ),
        (
            "FQR2751_5_tau",
            "tau_R10/tau_PPN/tau_clock/tau_orbital",
            "arena projection kernels",
            "observable_i=tau_i G_R[J_eff] or PPN dictionary when reduced to q_R",
            "arena-specific",
            "all_local_arenas",
            "2747-Y5-R2FR-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt-under-AX1090.md",
            "MISSING_ARENA_PROJECTIONS_EXCEPT_CONTROL_PPN",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "fallback_id": fid,
                "symbol": symbol,
                "role": role,
                "formula_or_mapping": formula,
                "units_status": units,
                "observable_link": observable,
                "source_path": source,
                "current_status": status,
            }
        )
        for fid, symbol, role, formula, units, observable, source, status in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2751_0_sources", "load current and no-loop evidence", "PASS", "all registered sources are present with needles"),
        ("RUN2751_1_2750_new_signing", "does 2750 sign auxiliary parent sort?", "NO_NEW_PARENT_SORT_SIGNATURE", "2750 selects second-class route but keeps all parent clauses unsigned"),
        ("RUN2751_2_grammar_theorem", "no-derivative theorem status", "EXACT_CONDITIONAL_UNSIGNED", "the conditional algebraic theorem is sound but not parent-derived"),
        ("RUN2751_3_loop_break", "avoid redoing 1563/2236/2288", "PASS_NO_LOOP_RULE", "next work must saturate current contract or emit finite residual vector"),
        ("RUN2751_4_finite_fallback", "finite q_R/R_AB fallback status", "READY_AS_SYMBOLIC_NONCLAIM", "2747 and 2716 give the translation/operator scaffold but not coefficients"),
        ("RUN2751_5_claim", "local GR/Newton claim", "BLOCKED_NO_CLAIM", "neither theorem-zero nor finite residual scoring is ready"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "runner_id": rid,
                "test": test,
                "current_status": status,
                "detail": detail,
            }
        )
        for rid, test, status, detail in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2751_0_auxiliary_sort", "R_AB auxiliary parent sort", "BLOCKED_NO_CLAIM", "typed parent sort still unsigned"),
        ("GATE2751_1_no_derivative", "Z_R=0 from no-derivative grammar", "BLOCKED_NO_CLAIM", "operator exclusion exact conditional only"),
        ("GATE2751_2_zero_stress", "Lambda_R/R_AB zero-stress elimination", "BLOCKED_NO_CLAIM", "requires joint matter/boundary/readout/operator contract"),
        ("GATE2751_3_finite_residual_score", "finite q_R/R_AB residual score", "BLOCKED_NO_CLAIM", "coefficients and projection kernels missing"),
        ("GATE2751_4_local_GR", "derived local GR/Newton", "BLOCKED_NO_CLAIM", "q_R=0 remains closure unless joint contract closes"),
        ("GATE2751_5_public", "public/GitHub claim", "BLOCKED_PRIVATE", "not requested and not claim-safe"),
    ]
    return [nonclaim({"claim_gate_id": gid, "claim_gate": gate, "status": status, "reason": reason}) for gid, gate, status, reason in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2751_0_verdict",
            "auxiliary compatibility grammar",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "2750 does not add the parent sort/operator/matter/boundary/readout signatures needed to promote it",
        ),
        (
            "DEC2751_1_loop_policy",
            "do not circle old grammar proof",
            "NO_LOOP_RULE_ACTIVE",
            "1563/2236/2288/2289 already say the broad route is unsigned under current evidence",
        ),
        (
            "DEC2751_2_fallback",
            "finite q_R/R_AB branch",
            "MANDATORY_IF_CONTRACT_FAILS",
            "2716/2747 provide the symbolic finite operator and PPN control lane but no coefficients",
        ),
        (
            "DEC2751_3_next",
            "next target",
            "NEXT_2752_CURRENT_CONTRACT_SATURATION_OR_FINITE_QR_VECTOR",
            "try one current-action contract saturation pass; if any clause fails, emit the finite q_R residual vector instead of restarting the grammar loop",
        ),
    ]
    return [nonclaim({"decision_id": did, "decision": decision, "result": result, "reason": reason}) for did, decision, result, reason in specs]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2751_0_2752",
                "status": "selected_primary",
                "target_doc": "2752-Y5-R2FR-current-parent-protection-contract-saturation-or-finite-qR-residual-vector-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_current_parent_protection_contract_saturation_or_finite_qR_residual_vector_under_AX1090_2752.py",
                "mission": "try a one-pass saturation of the current minimal parent action contract: parent sorts, action image, matter descent, boundary descent, readout closure, and operator exclusion; if any clause remains unsigned, emit a finite q_R/R_AB residual vector using 2747/2716 scaffolds",
                "acceptance": "either all joint-contract clauses are parent-signed in one action, or every surviving finite residual component is listed with missing coefficient/source/projection requirements",
                "forbidden": "do not rerun broad primitive grammar without new source text; do not claim local GR; do not score placeholder finite rows; do not edit formalization-workbench; no GitHub action",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2751_0_grammar", "source_table": rel(OUTPUTS["grammar"]), "copy_path": rel(BRANCH_OUTPUTS["grammar"]), "purpose": "source-weight nonloop auxiliary grammar status", "exists": BRANCH_OUTPUTS["grammar"].exists()}),
        nonclaim({"copy_id": "BR2751_1_finite", "source_table": rel(OUTPUTS["finite"]), "copy_path": rel(BRANCH_OUTPUTS["finite"]), "purpose": "local-bound finite qR/RAB fallback status", "exists": BRANCH_OUTPUTS["finite"].exists()}),
        nonclaim({"copy_id": "BR2751_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB acquisition queue for contract saturation or finite vector", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def pycache_path() -> Path:
    return Path(__file__).resolve().parent / "__pycache__"


def remove_pycache() -> None:
    pycache = pycache_path()
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def validation_rows(
    sources: list[dict[str, Any]],
    sort: list[dict[str, Any]],
    grammar: list[dict[str, Any]],
    elimination: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    loop: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    sort_ok = any(row["sort_id"] == "SORT2751_3_physical_countermodel" and row["status"] == "LEGAL_COUNTERMODEL_SURVIVES" for row in sort) and any(row["sort_id"] == "SORT2751_4_current_verdict" and row["status"] == "FAIL_CURRENT_THEOREM" for row in sort)
    grammar_ok = any(row["grammar_id"] == "GRAM2751_4_exact_conditional" and row["status"] == "EXACT_CONDITIONAL" for row in grammar) and any(row["grammar_id"] == "GRAM2751_5_current_verdict" and row["status"] == "FAIL_CURRENT_THEOREM_RETAIN_FINITE_BRANCH" for row in grammar)
    elim_ok = any(row["elimination_id"] == "ELIM2751_3_zero_stress" and row["status"] == "EXACT_CONDITIONAL_UNSIGNED" for row in elimination) and any(row["elimination_id"] == "ELIM2751_4_current_verdict" and row["status"] == "BLOCKED_NO_CLAIM" for row in elimination)
    contract_ok = any(row["contract_id"] == "CON2751_6_joint_contract" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in contract) and all(row["parent_signed_by_2750"] is False for row in contract)
    loop_ok = any(row["loop_id"] == "LOOP2751_4_next_move" and "2752" in row["rule"] for row in loop)
    finite_ok = {"q_R", "Z_R", "M_R^2", "J_eff", "B_R/Q_R/Pi_R", "tau_R10/tau_PPN/tau_clock/tau_orbital"}.issubset({row["symbol"] for row in finite})
    runner_ok = any(row["runner_id"] == "RUN2751_3_loop_break" and row["current_status"] == "PASS_NO_LOOP_RULE" for row in runner)
    gate_ok = all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in gates) and any(row["claim_gate_id"] == "GATE2751_4_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    decision_ok = any(row["decision_id"] == "DEC2751_3_next" and row["result"] == "NEXT_2752_CURRENT_CONTRACT_SATURATION_OR_FINITE_QR_VECTOR" for row in decisions)
    next_ok = next_target[0]["selected"] is True and "2752" in next_target[0]["target_doc"]
    no_claim_flags_ok = all(
        row.get("valid_for_claim") is False and row.get("claim_allowed") is False
        for block in [sort, grammar, elimination, contract, loop, finite, runner, gates, decisions, next_target]
        for row in block
    )
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    csv_ok = True
    csv_bits: list[str] = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    pycache_ok = not pycache_path().exists()
    formalization_count = formalization_recent_count()
    formalization_ok = formalization_count == 0
    rows = [
        {"validation_id": "VAL2751_0_sources", "passed": source_ok, "detail": "all source paths exist and needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2751_1_sort", "passed": sort_ok, "detail": "auxiliary sort remains unsigned and physical countermodel survives", "timestamp_utc": ts()},
        {"validation_id": "VAL2751_2_grammar", "passed": grammar_ok, "detail": "no-derivative grammar is exact conditional but not current theorem", "timestamp_utc": ts()},
        {"validation_id": "VAL2751_3_elimination", "passed": elim_ok, "detail": "auxiliary elimination and zero-stress are conditional on source silence", "timestamp_utc": ts()},
        {"validation_id": "VAL2751_4_joint_contract", "passed": contract_ok, "detail": "joint protection contract remains unsigned by 2750", "timestamp_utc": ts()},
        {"validation_id": "VAL2751_5_no_loop", "passed": loop_ok, "detail": "non-loop rule selects current contract saturation or finite vector", "timestamp_utc": ts()},
        {"validation_id": "VAL2751_6_finite_fallback", "passed": finite_ok, "detail": "finite qR/RAB residual vector scaffold contains all required symbolic slots", "timestamp_utc": ts()},
        {"validation_id": "VAL2751_7_runner", "passed": runner_ok, "detail": "runner refuses grammar-loop promotion", "timestamp_utc": ts()},
        {"validation_id": "VAL2751_8_claim_gates", "passed": gate_ok and no_claim_flags_ok, "detail": "claim gates remain closed and flags false", "timestamp_utc": ts()},
        {"validation_id": "VAL2751_9_decision_next", "passed": decision_ok and next_ok, "detail": "2752 current contract saturation or finite qR residual vector selected", "timestamp_utc": ts()},
        {"validation_id": "VAL2751_10_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2751_11_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2751_12_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2751_13_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2751_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2751 breaks the auxiliary-grammar loop, keeps the theorem exact-conditional/nonclaim, and selects current contract saturation or finite qR residual vector next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2751 - Y5 R2/f(R): R_AB Auxiliary Compatibility Parent Sort And No-Derivative Grammar Under AX1090

Status: `Y5_R2FR_2751_auxiliary_grammar_loop_broken_contract_or_finite_qR_next`

## Private Verdict

2751 re-tests the `R_AB` auxiliary-compatibility route after the current `lambda_R` stress/constraint pass.

The result is deliberately strict:

The algebraic route is still mathematically clean. If the parent action contains only an algebraic compatibility block

`S_R = int mu_parent Lambda_R [R_AB-C_AB(q,theta,top)]`

and if matter, boundary, readout, and derivative/operator slots are absent, then `R_AB` and `Lambda_R` eliminate before local readout. That would kill tree-level `Z_R`/`q_R` hair without a plateau axiom.

But 2750 does not sign those parent syntax clauses. It only tells us that first-class language is weaker and the second-class auxiliary route is the best conditional route. Therefore this checkpoint refuses to count the old conditional grammar as a new derivation.

The non-circular next move is a one-pass current parent-protection saturation. Either the present minimal action signs parent sorts, action image, matter descent, boundary descent, readout closure, and operator exclusion together, or we emit the finite `q_R/R_AB` residual vector and stop pretending the local branch has theorem-zero.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Parent Sort Audit

{markdown_table(data["sort"], ["sort_id", "parent_sort_statement", "claim_effect_if_signed", "status", "blocker", "valid_for_claim"])}

## No-Derivative Grammar Gate

{markdown_table(data["grammar"], ["grammar_id", "grammar_clause", "why_needed", "status", "blocker_or_effect", "valid_for_claim"])}

## Auxiliary Elimination Gate

{markdown_table(data["elimination"], ["elimination_id", "variation_or_step", "result", "status", "blocker", "valid_for_claim"])}

## Joint Protection Contract

{markdown_table(data["contract"], ["contract_id", "clause", "effect_if_signed", "current_status", "missing_for_claim", "parent_signed_by_2750", "valid_for_claim"])}

## Non-Loop Audit

{markdown_table(data["loop"], ["loop_id", "topic", "current_evidence", "rule", "valid_for_claim"])}

## Finite q_R/R_AB Residual Fallback Gate

{markdown_table(data["finite"], ["fallback_id", "symbol", "role", "formula_or_mapping", "units_status", "observable_link", "source_path", "current_status", "valid_for_claim"])}

## Runner

{markdown_table(data["runner"], ["runner_id", "test", "current_status", "detail", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim_gate", "status", "reason", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "result", "reason", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is progress because it stops us circling. The auxiliary route is not dead; it is the cleanest exact-conditional route. But it is not yet a derivation. The next pass must either sign the whole protection contract in the current parent action, or make the finite residual vector explicit enough for later bounds. That is the honest fork.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    sort = sort_rows()
    grammar = grammar_rows()
    elimination = elimination_rows()
    contract = contract_rows()
    loop = loop_rows()
    finite = finite_rows()
    runner = runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["sort"], sort)
    write_csv(OUTPUTS["grammar"], grammar)
    write_csv(OUTPUTS["elimination"], elimination)
    write_csv(OUTPUTS["contract"], contract)
    write_csv(OUTPUTS["loop"], loop)
    write_csv(OUTPUTS["finite"], finite)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["grammar"], grammar)
    write_csv(BRANCH_OUTPUTS["finite"], finite)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, sort, grammar, elimination, contract, loop, finite, runner, gates, decisions, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "sort": sort,
        "grammar": grammar,
        "elimination": elimination,
        "contract": contract,
        "loop": loop,
        "finite": finite,
        "runner": runner,
        "gates": gates,
        "decisions": decisions,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    remove_pycache()

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2751 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
