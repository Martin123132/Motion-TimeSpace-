from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3440-Y5-R2FR-no-linear-X-parent-grammar-or-explicit-closure-demotion-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3439": ROOT / "3439-Y5-R2FR-block-diagonal-parent-Hessian-or-first-BHX-source-row-under-AX1090.md",
    "next_3439": OUT / "P8_Y5_R2FR_3439_NEXT_TARGET.csv",
    "hessian_3439": OUT / "P8_Y5_R2FR_3439_BLOCK_DIAGONAL_HESSIAN_THEOREM.csv",
    "obstructions_3439": OUT / "P8_Y5_R2FR_3439_BHX_OBSTRUCTION_AUDIT.csv",
    "bhx_row_3439": OUT / "P8_Y5_R2FR_3439_BHX_INPUT_ROW.csv",
    "local_gr_3439": OUT / "P8_Y5_R2FR_3439_LOCAL_GR_IMPACT.csv",
    "object_language_1078": ROOT / "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md",
    "matter_descent_1087": ROOT / "1087-Y5-R10-parent-matter-descent-zero-current-or-DD-coefficient-source-pack.md",
    "minimal_matter_1088": ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
    "moms_axiom_1090": ROOT / "1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md",
    "ordinary_sector_1104": ROOT / "1104-Y5-R10-parent-ordinary-sector-action-signature-or-explicit-closure-ledger.md",
    "single_public_metric_1030": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
    "matter_pullback_1044": ROOT / "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md",
    "source_owner_contract": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "field_silence_queue": OUT / "P8_FIELD_SPECIFIC_SILENCE_QUEUE.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3440_SOURCE_REGISTER.csv",
    "no_linear_x_grammar_theorem": OUT / "P8_Y5_R2FR_3440_NO_LINEAR_X_GRAMMAR_THEOREM.csv",
    "grammar_signature_audit": OUT / "P8_Y5_R2FR_3440_GRAMMAR_SIGNATURE_AUDIT.csv",
    "forbidden_vertex_ledger": OUT / "P8_Y5_R2FR_3440_FORBIDDEN_VERTEX_LEDGER.csv",
    "closure_demotion_ledger": OUT / "P8_Y5_R2FR_3440_CLOSURE_DEMOTION_LEDGER.csv",
    "bhx_route_update": OUT / "P8_Y5_R2FR_3440_BHX_ROUTE_UPDATE.csv",
    "local_gr_impact": OUT / "P8_Y5_R2FR_3440_LOCAL_GR_IMPACT.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3440_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3440_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3440_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3440_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3440_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3439": "B_i block-diagonal theorem handoff",
        "next_3439": "3440 target declaration",
        "hessian_3439": "conditional B_i=0 theorem",
        "obstructions_3439": "linear-X obstruction audit",
        "bhx_row_3439": "clean/fallback B_HX rows",
        "local_gr_3439": "local-GR impact from B_i route",
        "object_language_1078": "object-language/action-measure/current-owner proof attempt",
        "matter_descent_1087": "matter descent zero-current theorem and object-language gap",
        "minimal_matter_1088": "minimal parent ordinary-matter signature attempt",
        "moms_axiom_1090": "MOMS parent action missing-axiom ledger",
        "ordinary_sector_1104": "ordinary-sector action signature/closure ledger",
        "single_public_metric_1030": "single public metric/shadow-frame gate",
        "matter_pullback_1044": "matter pullback J_X zero theorem and unsigned gates",
        "source_owner_contract": "parent source-owner action terms",
        "field_silence_queue": "field-specific silence queue including no-linear-source need",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def no_linear_x_grammar_theorem() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "NLX3440_0_target",
            "statement": "The parent grammar needed by 3439 is a no-linear-X object-language rule for compact local finite modes.",
            "formula": "Allowed local X_i appearances: X_i^2, (nabla X_i)^2, X_i^4, topological/even functions; forbidden: X_i R, X_i T, X_i U_source, X_i boundary/readout.",
            "status": "TARGET_SHARPENED",
            "condition_or_missing": "grammar must come from parent MTS primitives, not taste",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NLX3440_1_conditional_grammar_to_Bzero",
            "statement": "If the no-linear-X grammar is parent-signed, then the 3439 block-diagonal theorem is promoted inside that branch.",
            "formula": "G_no-linear-X + X0=0 + nabla X0=0 => B_i=delta_h delta_X S_parent|0=0",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "condition_or_missing": "requires signed grammar clauses NLX3440_2..6",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NLX3440_2_even_or_vertical_symmetry",
            "statement": "A genuine symmetry or quotient-vertical rule can forbid odd X_i terms.",
            "formula": "X_i -> -X_i, or S_parent[Phi]=S_red[q(Phi)] with v_X in ker(Dq), forbids linear X_i slots.",
            "status": "CONDITIONAL_ROUTE_NOT_SIGNED",
            "condition_or_missing": "no current source proves this for every finite local X_i channel",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NLX3440_3_stationary_local_vacuum",
            "statement": "The local compact exterior must expand around X_i=0 with no background gradient.",
            "formula": "X_i|A=0, nabla X_i|A=0, delta_X S_parent|0=0",
            "status": "PREMISE_NOT_PARENT_SIGNED",
            "condition_or_missing": "without this, metric dependence of X kinetic/mass terms can create h-X mixing",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NLX3440_4_matter_readout_descent",
            "statement": "Ordinary matter, constants, EM/clock readout and measured-source maps must not take X_i as a direct argument.",
            "formula": "S_matter=Sbar[Psi,e_obs(q),theta_rep], alpha_EM=alpha_EM(theta_rep), mu_obs=mu_obs[q] plus retained residuals",
            "status": "CONDITIONAL_ROUTE_NOT_SIGNED",
            "condition_or_missing": "1078/1087/1044 keep object-language and matter descent unsigned",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NLX3440_5_boundary_readout_silence",
            "statement": "Boundary, projector and domain terms must not contain local source-visible linear X_i charge.",
            "formula": "delta_X S_boundary|0=0 and Pi_source[delta_X B]=0",
            "status": "OPEN",
            "condition_or_missing": "3439 boundary-X obstruction remains live",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NLX3440_6_verdict",
            "statement": "The no-linear-X grammar is an exact sufficient theorem shape, but not a current MTS derivation.",
            "formula": "B_i=0 stays closure-only until NLX3440_2..5 are parent-signed",
            "status": "GRAMMAR_NOT_PARENT_SIGNED_DEMOTE_BZERO_TO_CLOSURE",
            "condition_or_missing": "object-language, symmetry/quotient, vacuum, readout and boundary signatures",
            "valid_for_claim": False,
        },
    ]


def grammar_signature_audit() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "GSA3440_0_object_language",
            "needed_signature": "parent object-language forbids local scalar slots linear in finite X_i",
            "current_evidence": "1078 says object-language typing is sharpened but not parent-signed.",
            "current_status": "UNSIGNED",
            "effect": "cannot forbid X_i R or source-only X_i by grammar alone",
            "valid_for_claim": False,
        },
        {
            "audit_id": "GSA3440_1_matter_functor",
            "needed_signature": "ordinary matter functor descends through observed quotient data and excludes X_i markers",
            "current_evidence": "1087 and 1044 give exact conditional chain rules but keep matter functor/descent unsigned.",
            "current_status": "UNSIGNED",
            "effect": "class-metric/readout X_i can survive",
            "valid_for_claim": False,
        },
        {
            "audit_id": "GSA3440_2_minimal_ordinary_sector",
            "needed_signature": "one minimal ordinary-sector action excludes hidden/source/material slots before variation",
            "current_evidence": "1088/1104 treat this as a signature/closure problem, not a completed derivation.",
            "current_status": "UNSIGNED",
            "effect": "source-only or hidden-visible coefficient morphisms remain legal countermodels",
            "valid_for_claim": False,
        },
        {
            "audit_id": "GSA3440_3_single_public_metric",
            "needed_signature": "single public metric/no-shadow-frame branch is parent-selected",
            "current_evidence": "1030 rejects covariance/Ward shortcuts and leaves single-public-metric theorem nonclaim.",
            "current_status": "UNSIGNED",
            "effect": "universal class metric X_i pullback remains a possible B_i/source route",
            "valid_for_claim": False,
        },
        {
            "audit_id": "GSA3440_4_axiom_ledger",
            "needed_signature": "MOMS/no-hidden-slot/readout-order axioms are derived rather than adopted",
            "current_evidence": "1090 marks missing axioms and variation/readout-order issues.",
            "current_status": "MISSING_AXIOM_NOT_ADOPTED",
            "effect": "no-linear-X is closure if used now",
            "valid_for_claim": False,
        },
    ]


def forbidden_vertex_ledger() -> list[dict[str, Any]]:
    return [
        {
            "vertex_id": "FV3440_0_XR",
            "forbidden_vertex": "X_i R[g]",
            "why_it_matters": "creates h-X Hessian B_i in the scalar metric channel",
            "current_status": "NOT_FORBIDDEN",
            "fallback_if_allowed": "source B_HX and include alpha_i^{gX}/gamma/beta residuals",
            "valid_for_claim": False,
        },
        {
            "vertex_id": "FV3440_1_XT",
            "forbidden_vertex": "X_i T_matter or X_i U_source",
            "why_it_matters": "direct source-normalization and trace force",
            "current_status": "NOT_FORBIDDEN",
            "fallback_if_allowed": "qbar/Qbar source rows and WEP/R10/PPN bounds",
            "valid_for_claim": False,
        },
        {
            "vertex_id": "FV3440_2_Xboundary",
            "forbidden_vertex": "linear X_i boundary/projector/domain charge",
            "why_it_matters": "bulk B_i=0 would not remove source-visible tail",
            "current_status": "OPEN",
            "fallback_if_allowed": "absolute alpha_i_tail and boundary/source rows",
            "valid_for_claim": False,
        },
        {
            "vertex_id": "FV3440_3_class_metric",
            "forbidden_vertex": "g_hat=exp(F(X_i))g or disformal X_i frame",
            "why_it_matters": "reintroduces matter coupling even if S_X is even",
            "current_status": "RETAINED_COUNTERMODEL",
            "fallback_if_allowed": "class-metric trace current and local bounds",
            "valid_for_claim": False,
        },
        {
            "vertex_id": "FV3440_4_background_X",
            "forbidden_vertex": "nonzero X0 or nabla X0 in compact local exterior",
            "why_it_matters": "turns even kinetic/mass terms into linearized h-X mixing",
            "current_status": "NOT_PARENT_ZEROED",
            "fallback_if_allowed": "background-profile residual and PPN/R10 projection",
            "valid_for_claim": False,
        },
        {
            "vertex_id": "FV3440_5_effective_readout",
            "forbidden_vertex": "radiative/effective/readout coefficient f_X(X_i) multiplying visible sectors",
            "why_it_matters": "tree-level grammar can be bypassed after effective reduction",
            "current_status": "READOUT_CLOSURE_UNSIGNED",
            "fallback_if_allowed": "finite coefficient prior/source pack",
            "valid_for_claim": False,
        },
    ]


def closure_demotion_ledger() -> list[dict[str, Any]]:
    return [
        {
            "demotion_id": "CLD3440_0_conditional_theorem_retained",
            "object": "B_i=0 from no-linear-X grammar",
            "status": "CONDITIONAL_THEOREM_RETAINED",
            "reason": "the theorem is mathematically sound if the grammar is signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "demotion_id": "CLD3440_1_current_signature_missing",
            "object": "parent no-linear-X grammar",
            "status": "NOT_PARENT_SIGNED",
            "reason": "object-language, matter functor, no-shadow-frame, boundary and readout closure are unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "demotion_id": "CLD3440_2_demote_Bzero",
            "object": "use B_i=0 as local-GR/R10 evidence",
            "status": "CLOSURE_ONLY_UNTIL_PARENT_GRAMMAR_SIGNED",
            "reason": "surviving countervertices can create nonzero B_i",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "demotion_id": "CLD3440_3_finite_route_retained",
            "object": "nonzero B_HX",
            "status": "SOURCED_INPUT_ROUTE_RETAINED",
            "reason": "fallback B_HX row from 3439 remains the honest empirical/PPN/R10 route",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bhx_route_update() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "BRU3440_0_clean_branch",
            "prior_row": "BHX3439_0_clean_branch_zero_candidate",
            "before": "EXACT_CONDITIONAL_ZERO_IF_EVEN_X_GRAMMAR_SIGNED",
            "after": "CLOSURE_ONLY_GRAMMAR_UNSIGNED",
            "impact": "B_i=0 remains a clean assumption/theorem target, not a claim row",
            "valid_for_claim": False,
        },
        {
            "update_id": "BRU3440_1_fallback",
            "prior_row": "BHX3439_1_fallback_source_row",
            "before": "SOURCE_READY_TEMPLATE_NONCLAIM",
            "after": "ACTIVE_IF_ANY_FORBIDDEN_VERTEX_SURVIVES",
            "impact": "nonzero B_i must be treated as an operator coefficient with source paths/units",
            "valid_for_claim": False,
        },
        {
            "update_id": "BRU3440_2_alpha",
            "prior_row": "ATU3439_0_if_clean_branch_signed",
            "before": "alpha_i^{gX}=0 if clean branch signed",
            "after": "alpha_i^{gX}=0 only as closure until grammar theorem exists",
            "impact": "R10 metric-mixing alpha leg remains blocked unless closure is explicitly declared",
            "valid_for_claim": False,
        },
    ]


def local_gr_impact() -> list[dict[str, Any]]:
    return [
        {
            "impact_id": "LGI3440_0_good_news",
            "gate": "metric/X mixing",
            "status": "THEOREM_SHAPE_EXACT",
            "impact": "we know exactly what grammar would kill B_i without a fit",
            "remaining": "derive grammar from MTS primitives or mark closure explicitly",
            "valid_for_claim": False,
        },
        {
            "impact_id": "LGI3440_1_bad_news",
            "gate": "current MTS local-GR branch",
            "status": "NOT_PROMOTED",
            "impact": "current corpus does not sign no-linear-X, so B_i=0 is not evidence yet",
            "remaining": "nonzero B_HX route plus source-normalization/EH/PPN/boundary gates",
            "valid_for_claim": False,
        },
        {
            "impact_id": "LGI3440_2_next_best_move",
            "gate": "avoid broad grammar loop",
            "status": "ONE_CHANNEL_SIGNATURE_OR_BHX_PACK",
            "impact": "choose a specific finite channel and either sign its no-linear grammar or stage its B_HX coefficient pack",
            "remaining": "motion/time/flow or bulk-X channel selection",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3440_0_conditional_grammar",
            "gate": "no-linear-X grammar implies B_i=0",
            "result": "PASS_CONDITIONAL_THEOREM",
            "evidence": "NLX3440_1",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3440_1_parent_signed_grammar",
            "gate": "MTS parent signs the grammar",
            "result": "BLOCKED_UNSIGNED",
            "evidence": "GSA3440 rows and forbidden vertex ledger",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3440_2_Bzero_claim",
            "gate": "B_i=0 may be used as derived evidence",
            "result": "DEMOTED_TO_CLOSURE_ONLY",
            "evidence": "CLD3440_2",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3440_3_BHX_fallback",
            "gate": "nonzero B_HX source route remains executable",
            "result": "PASS_TEMPLATE_NONCLAIM",
            "evidence": "BRU3440_1",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3440_4_local_GR",
            "gate": "local GR/Newton branch is derived",
            "result": "BLOCKED",
            "evidence": "grammar unsigned plus source-normalization/EH/PPN gates remain open",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3440_0_truth",
            "decision": "Do not pretend no-linear-X is derived.",
            "reason": "current object-language evidence supports a disciplined closure theorem, not a signed parent grammar.",
            "next_action": "use B_i=0 only if explicitly labeled closure until one channel is signed",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3440_1_keep_theorem",
            "decision": "Keep the conditional theorem as valuable.",
            "reason": "it gives the exact grammar needed to kill metric mixing without empirical tuning.",
            "next_action": "attempt one-channel signature rather than another whole-corpus grammar loop",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3440_2_best_next",
            "decision": "Move to one finite channel: sign no-linear-X or build B_HX pack.",
            "reason": "a channel-specific proof can actually close a row; a broad grammar proof has already hit unsigned object-language walls.",
            "next_action": "3441 one-channel no-linear-X signature or B_HX coefficient pack",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3441-Y5-R2FR-one-channel-no-linear-X-signature-or-BHX-coefficient-pack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3441_one_channel_no_linear_X_signature_or_BHX_coefficient_pack.py",
            "objective": "select one finite local channel and try to sign its no-linear-X/no-XR/no-boundary-X grammar; if that fails, stage the channel-specific B_HX coefficient pack for R10/PPN scoring",
            "success_condition": "one channel obtains a signed or explicitly closure-labeled no-linear-X status, plus a channel-specific nonclaim B_HX fallback row with units/source-path requirements",
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3440_0",
            "status": "NO_LINEAR_X_GRAMMAR_CONDITIONAL_BZERO_DEMOTED_TO_CLOSURE",
            "claim_allowed": False,
            "reason": "parent grammar not signed; B_HX fallback retained",
            "next_safe_action": "choose one channel and either sign its grammar or source its B_HX coefficient",
            "valid_for_claim": False,
        }
    ]


def all_generated_nonclaim(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for output_name, rows in rows_by_name.items():
        if output_name == "validation":
            continue
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    theorem_rows = rows_by_name["no_linear_x_grammar_theorem"]
    audit_rows = rows_by_name["grammar_signature_audit"]
    forbidden_rows = rows_by_name["forbidden_vertex_ledger"]
    demotion_rows = rows_by_name["closure_demotion_ledger"]
    route_rows = rows_by_name["bhx_route_update"]
    promotion_rows = rows_by_name["promotion_gates"]
    next_rows = rows_by_name["next_target"]
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1 for checked_path in FORMALIZATION.rglob("*") if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )
    validations = [
        {
            "check_id": "VAL3440_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3440_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": all(str(path).startswith(str(ROOT)) for path in OUTPUTS.values()),
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3440_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": all_generated_nonclaim(rows_by_name),
            "detail": "valid_for_claim=false and claim_allowed=false throughout generated rows",
        },
        {
            "check_id": "VAL3440_3_conditional_theorem",
            "condition": "no-linear-X grammar theorem is present",
            "passed": any(row["theorem_id"] == "NLX3440_1_conditional_grammar_to_Bzero" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem_rows),
            "detail": "grammar implies B_i=0 only if parent-signed",
        },
        {
            "check_id": "VAL3440_4_signature_unsigned",
            "condition": "grammar is not falsely treated as signed",
            "passed": len(audit_rows) >= 5 and all(row["current_status"] in {"UNSIGNED", "MISSING_AXIOM_NOT_ADOPTED"} for row in audit_rows),
            "detail": f"{len(audit_rows)} signature blockers retained",
        },
        {
            "check_id": "VAL3440_5_forbidden_vertices",
            "condition": "linear-X countervertices remain visible",
            "passed": len(forbidden_rows) >= 6 and all(row["current_status"] != "FORBIDDEN_SIGNED" for row in forbidden_rows),
            "detail": f"{len(forbidden_rows)} forbidden-vertex candidates retained",
        },
        {
            "check_id": "VAL3440_6_closure_demotion",
            "condition": "B_i=0 demoted to closure-only while grammar unsigned",
            "passed": any(row["demotion_id"] == "CLD3440_2_demote_Bzero" and row["status"] == "CLOSURE_ONLY_UNTIL_PARENT_GRAMMAR_SIGNED" for row in demotion_rows)
            and any(row["gate_id"] == "PG3440_2_Bzero_claim" and row["result"] == "DEMOTED_TO_CLOSURE_ONLY" for row in promotion_rows),
            "detail": "B_i=0 not claim evidence",
        },
        {
            "check_id": "VAL3440_7_BHX_route_retained",
            "condition": "finite B_HX route remains active",
            "passed": any(row["update_id"] == "BRU3440_1_fallback" and row["after"] == "ACTIVE_IF_ANY_FORBIDDEN_VERTEX_SURVIVES" for row in route_rows),
            "detail": "nonzero B_HX source route retained",
        },
        {
            "check_id": "VAL3440_8_next_target",
            "condition": "next target narrows to one channel",
            "passed": "one-channel" in next_rows[0]["target_doc"],
            "detail": next_rows[0]["target_doc"],
        },
        {
            "check_id": "VAL3440_9_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3440_10_overall",
            "condition": "3440 no-linear-X grammar checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3440 - No-Linear-X Parent Grammar or Explicit Closure Demotion

## Summary
- This checkpoint tests whether the 3439 `B_i=0` route is currently derivable from the parent object-language.
- The conditional theorem is exact: if finite local `X_i` modes are even/nonmetric, expanded about `X_i=0`, and barred from linear curvature, matter, source, boundary and readout slots, then `B_i=0`.
- The current corpus does not sign that grammar. Existing object-language, matter-descent, no-shadow-frame, readout-order and ordinary-sector sources keep the needed clauses unsigned.
- Therefore `B_i=0` is retained as a clean closure theorem, but demoted from derived evidence until a channel-specific parent signature exists.
- The finite `B_HX` route remains active and source-ready if any linear-X vertex survives.

## Source Register
{md_table(rows_by_name["source_register"])}

## No-Linear-X Grammar Theorem
{md_table(rows_by_name["no_linear_x_grammar_theorem"])}

## Grammar Signature Audit
{md_table(rows_by_name["grammar_signature_audit"])}

## Forbidden Vertex Ledger
{md_table(rows_by_name["forbidden_vertex_ledger"])}

## Closure Demotion Ledger
{md_table(rows_by_name["closure_demotion_ledger"])}

## BHX Route Update
{md_table(rows_by_name["bhx_route_update"])}

## Local GR Impact
{md_table(rows_by_name["local_gr_impact"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
This is a disciplined loss with a useful win inside it. The no-linear-`X` grammar is exactly the right theorem shape for killing metric mixing, but the present corpus does not derive that grammar globally. So we do not throw away the ladder: we keep the theorem as closure, keep `B_HX` executable, and next narrow to one finite channel where a real signature might actually close.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "no_linear_x_grammar_theorem": no_linear_x_grammar_theorem(),
        "grammar_signature_audit": grammar_signature_audit(),
        "forbidden_vertex_ledger": forbidden_vertex_ledger(),
        "closure_demotion_ledger": closure_demotion_ledger(),
        "bhx_route_update": bhx_route_update(),
        "local_gr_impact": local_gr_impact(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3440 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
