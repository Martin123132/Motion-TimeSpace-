from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_parent_owned_Bedge_boundary_class_not_closed_first_edge_factor_source_row_staged_nonclaim"
CLAIM_CEILING = "conditional_Bedge_boundary_lemma_only_no_Qedge_zero_no_R10_no_R11_no_PPN_no_local_GR_claim"
NEXT_TARGET = "678-Y5-R10-boundary-class-nohair-projector-silence-or-BX-source-row.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "677-Y5-R10-parent-owned-Bedge-boundary-class-or-source-first-edge-factor.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "222_doc": ROOT / "222-parent-X-sector-degree-count-and-boundary-action.md",
    "235_doc": ROOT / "235-projector-stress-variation-or-nohair-constraint-algebra.md",
    "539_doc": ROOT / "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
    "667_doc": ROOT / "667-Y5-R10-explicit-parent-boundary-action-ansatz-and-variation-ledger.md",
    "667_validation": RESIDUALS / "P8_Y5_BRR545_667_VALIDATION.csv",
    "667_ansatz": RESIDUALS / "P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv",
    "667_variation": RESIDUALS / "P8_Y5_R10_667_VARIATION_LEDGER.csv",
    "668_doc": ROOT / "668-Y5-R10-sector-Lagrangian-owner-and-boundary-condition-lock.md",
    "668_validation": RESIDUALS / "P8_Y5_BRR545_668_VALIDATION.csv",
    "668_boundary_lock": RESIDUALS / "P8_Y5_R10_668_BOUNDARY_CONDITION_LOCK.csv",
    "670_validation": RESIDUALS / "P8_Y5_BRR545_670_VALIDATION.csv",
    "670_no_pole": RESIDUALS / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
    "671_validation": RESIDUALS / "P8_Y5_BRR545_671_VALIDATION.csv",
    "671_edge": RESIDUALS / "P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv",
    "672_validation": RESIDUALS / "P8_Y5_BRR545_672_VALIDATION.csv",
    "672_source_plan": RESIDUALS / "P8_Y5_R10_672_EDGE_COEFFICIENT_SOURCE_PLAN.csv",
    "673_validation": RESIDUALS / "P8_Y5_BRR545_673_VALIDATION.csv",
    "673_pim_audit": RESIDUALS / "P8_Y5_R10_673_HAMILTONIAN_PIM_ORTHOGONALITY_PROOF_AUDIT.csv",
    "674_validation": RESIDUALS / "P8_Y5_BRR545_674_VALIDATION.csv",
    "674_parent_clause": RESIDUALS / "P8_Y5_R10_674_PARENT_PIM_CLAUSE_TEST.csv",
    "674_requirements": RESIDUALS / "P8_Y5_R10_674_COEFFICIENT_REQUIREMENTS.csv",
    "675_doc": ROOT / "675-Y5-R10-source-backed-edge-row-scout-or-Qedge-null-action-clause.md",
    "675_validation": RESIDUALS / "P8_Y5_BRR545_675_VALIDATION.csv",
    "675_qedge_audit": RESIDUALS / "P8_Y5_R10_675_QEDGE_NULL_ACTION_CLAUSE_AUDIT.csv",
    "675_scout": RESIDUALS / "P8_Y5_R10_675_SOURCE_BACKED_EDGE_ROW_SCOUT.csv",
    "675_blockers": RESIDUALS / "P8_Y5_R10_675_EDGE_ROW_BLOCKER_MATRIX.csv",
    "676_doc": ROOT / "676-Y5-R10-Qedge-null-clause-minimal-parent-action-or-first-source-row.md",
    "676_validation": RESIDUALS / "P8_Y5_BRR545_676_VALIDATION.csv",
    "676_contract": RESIDUALS / "P8_Y5_R10_676_MINIMAL_PARENT_QEDGE_NULL_CONTRACT.csv",
    "676_source_spec": RESIDUALS / "P8_Y5_R10_676_FIRST_SOURCE_ROW_SPEC.csv",
    "676_route": RESIDUALS / "P8_Y5_R10_676_ROUTE_SELECTION.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "MISSING_VALIDATION_FILE", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for path in FORMALIZATION_WORKBENCH.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "222_doc": "candidate X-sector boundary momentum formula source",
        "235_doc": "projector stress and B_X boundary formula source",
        "539_doc": "Hamiltonian Pi_M context for measured edge charge",
        "667_doc": "parent boundary action ansatz checkpoint",
        "667_validation": "667 validation gate",
        "667_ansatz": "parent boundary action ansatz rows",
        "667_variation": "parent variation leakage ledger",
        "668_doc": "boundary condition lock checkpoint",
        "668_validation": "668 validation gate",
        "668_boundary_lock": "boundary class/nohair/projector missing-lock rows",
        "670_validation": "670 validation gate",
        "670_no_pole": "quotient no-pole proof chain",
        "671_validation": "671 validation gate",
        "671_edge": "edge residual vector",
        "672_validation": "672 validation gate",
        "672_source_plan": "edge coefficient source plan",
        "673_validation": "673 validation gate",
        "673_pim_audit": "Hamiltonian Pi_M orthogonality audit",
        "674_validation": "674 validation gate",
        "674_parent_clause": "parent Pi_M clause test",
        "674_requirements": "edge coefficient requirements",
        "675_doc": "Qedge null/source-backed scout checkpoint",
        "675_validation": "675 validation gate",
        "675_qedge_audit": "Qedge null action clause audit",
        "675_scout": "source-backed edge row scout",
        "675_blockers": "edge row blocker matrix",
        "676_doc": "minimal parent Qedge contract checkpoint",
        "676_validation": "676 validation gate",
        "676_contract": "minimal parent Qedge null contract",
        "676_source_spec": "first edge source-row spec",
        "676_route": "route selection into 677",
    }
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def bedge_boundary_class_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "audit_id": "BBC677_0_candidate_boundary_momentum",
            "object": "B_X^nu",
            "mathematical_form": "B_X^nu=n_mu P^{mu nu}",
            "needed_for_zero": "identify the boundary representative whose charge is Q_edge",
            "current_result": "candidate_formula_present",
            "blocker": "candidate boundary momentum is not yet parent-owned as an exact boundary class",
            "claim_effect_if_pass": "defines the edge source factor or starts the theorem-zero route",
            "valid_for_claim": "false",
            "source_paths": source_list("222_doc", "235_doc", "676_source_spec"),
            "generated_utc": now,
        },
        {
            "audit_id": "BBC677_1_exact_boundary_class",
            "object": "B_edge",
            "mathematical_form": "B_edge=d_partial b_edge on the allowed compact local shell",
            "needed_for_zero": "Stokes/exactness kills the compact local edge charge when the relative class is trivial",
            "current_result": "conditional_lemma_written_not_signed",
            "blocker": "no parent-owned proof that B_X pulls back to d_partial b_edge",
            "claim_effect_if_pass": "Q_edge can vanish as a local theorem-zero, not as a fitted zero",
            "valid_for_claim": "false",
            "source_paths": source_list("675_qedge_audit", "676_contract", "667_variation"),
            "generated_utc": now,
        },
        {
            "audit_id": "BBC677_2_relative_cohomology",
            "object": "[B_edge]_{H_rel}",
            "mathematical_form": "[B_edge]_{H^{d-1}(partial Omega,partial partial Omega)}=0",
            "needed_for_zero": "prevents an exact-looking local primitive from hiding a linked/topological charge",
            "current_result": "not_signed",
            "blocker": "668 still marks relative class C_top parent selection as failed",
            "claim_effect_if_pass": "removes topological edge leakage from Q_edge",
            "valid_for_claim": "false",
            "source_paths": source_list("668_boundary_lock", "667_ansatz"),
            "generated_utc": now,
        },
        {
            "audit_id": "BBC677_3_improper_charge_guard",
            "object": "proper versus improper boundary charge",
            "mathematical_form": "B_edge exact only in the proper-gauge sector, not in ADM/H_tau/source-mass sector",
            "needed_for_zero": "stops the proof from deleting the physical Hamiltonian/ADM mass by definition",
            "current_result": "not_signed",
            "blocker": "fixed reference branch and same-frame H_tau/source mass equality remain unsigned",
            "claim_effect_if_pass": "Q_edge zero would be physically legal rather than a subtraction trick",
            "valid_for_claim": "false",
            "source_paths": source_list("667_ansatz", "668_boundary_lock", "673_pim_audit", "674_parent_clause"),
            "generated_utc": now,
        },
        {
            "audit_id": "BBC677_4_variation_nohair",
            "object": "delta B_edge and boundary stress hair",
            "mathematical_form": "delta_edge S_parent=0, Pi_TF=Pi_vector=Pi_shear=Pi_time=0 on the local shell",
            "needed_for_zero": "prevents boundary variations from reintroducing a vector/tensor/local preferred-frame residual",
            "current_result": "not_closed",
            "blocker": "668 keeps no-vector/tensor-hair and sector boundary conditions failed",
            "claim_effect_if_pass": "edge branch becomes locally silent under allowed variations",
            "valid_for_claim": "false",
            "source_paths": source_list("235_doc", "668_boundary_lock", "667_variation"),
            "generated_utc": now,
        },
        {
            "audit_id": "BBC677_5_projector_domain_silence",
            "object": "quotient/projector action on B_edge",
            "mathematical_form": "Dq[v_edge]=0 and Pi_M^H[d_partial b_edge]=0 on the same boundary domain",
            "needed_for_zero": "keeps quotient exactness, Hamiltonian projection, and local readout in one frame",
            "current_result": "not_signed",
            "blocker": "670-674 give conditional verticality/Pi_M routes but not a single parent-owned domain",
            "claim_effect_if_pass": "Qbar_edge_XH(lambda)=0 follows from the boundary class rather than a coefficient prior",
            "valid_for_claim": "false",
            "source_paths": source_list("670_no_pole", "671_edge", "673_pim_audit", "674_parent_clause", "676_contract"),
            "generated_utc": now,
        },
        {
            "audit_id": "BBC677_6_verdict",
            "object": "parent-owned B_edge zero proof",
            "mathematical_form": "B_X -> B_edge=d_partial b_edge, [B_edge]=0, proper gauge, variation silence, projector silence",
            "needed_for_zero": "all clauses jointly imply Q_edge=0 and remove the R10 edge factor",
            "current_result": "not_closed_nonclaim",
            "blocker": "exact representative, relative class, nohair, and same-domain projector clauses are still unsigned",
            "claim_effect_if_pass": "R10 edge branch can be demoted to theorem-zero; currently it cannot",
            "valid_for_claim": "false",
            "source_paths": source_list("667_variation", "668_boundary_lock", "675_qedge_audit", "676_contract"),
            "generated_utc": now,
        },
    ]


def bx_exactness_or_source_row_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "row_id": "BX677_0_candidate_formula",
            "factor": "B_X_boundary_momentum",
            "formula_or_value": "B_X^nu=n_mu P^{mu nu}",
            "units": "boundary_momentum_density_unfixed_normalization",
            "boundary_class": "MISSING_PARENT_FIXED_C_TOP",
            "exactness_status": "candidate_not_exact",
            "counterterm_status": "MISSING_B_class_and_B_ct_selection",
            "source_status": "local_corpus_formula_only",
            "blocking_input": "need pullback proof B_X=d_partial b_edge or source-backed boundary momentum normalization",
            "valid_for_claim": "false",
            "source_paths": source_list("222_doc", "235_doc", "676_source_spec"),
            "generated_utc": now,
        },
        {
            "row_id": "BX677_1_conditional_theorem_zero",
            "factor": "B_edge_exact_zero",
            "formula_or_value": "if B_edge=d_partial b_edge and [B_edge]_{H_rel}=0 then integral_boundary B_edge=0",
            "units": "theorem_zero_condition",
            "boundary_class": "conditional_trivial_relative_class",
            "exactness_status": "lemma_valid_only_if_parent_clauses_signed",
            "counterterm_status": "must_not_remove_improper_charge",
            "source_status": "derived_condition_not_parent_signed",
            "blocking_input": "relative cohomology/nohair/projector silence",
            "valid_for_claim": "false",
            "source_paths": source_list("667_variation", "668_boundary_lock", "675_qedge_audit", "676_contract"),
            "generated_utc": now,
        },
        {
            "row_id": "BX677_2_first_claim_ready_row_template",
            "factor": "B_X_boundary_momentum",
            "formula_or_value": "MISSING_NUMERIC_VALUE_OR_PARENT_THEOREM_ZERO",
            "units": "MISSING_UNITS",
            "boundary_class": "MISSING_BOUNDARY_CLASS",
            "exactness_status": "MISSING_EXACTNESS_OR_SOURCE",
            "counterterm_status": "MISSING_COUNTERTERM_STATUS",
            "source_status": "MISSING_SOURCE_PATH",
            "blocking_input": "no claim-valid first edge factor row exists",
            "valid_for_claim": "false",
            "source_paths": source_list("675_scout", "675_blockers", "676_source_spec"),
            "generated_utc": now,
        },
        {
            "row_id": "BX677_3_source_first_search_target",
            "factor": "B_X_or_Qbar_edge_XH",
            "formula_or_value": "source a boundary momentum normalization or Hamiltonian projection numerator/denominator",
            "units": "must_match_alpha_edge_factorization",
            "boundary_class": "same local shell as R10/PPN/clock/orbital arena",
            "exactness_status": "fallback_if_Bedge_not_proved",
            "counterterm_status": "must state B_ref/B_class/B_ct convention",
            "source_status": "search_ready_nonclaim",
            "blocking_input": "source-backed row required before any R10 comparator promotion",
            "valid_for_claim": "false",
            "source_paths": source_list("672_source_plan", "674_requirements", "675_blockers", "676_source_spec"),
            "generated_utc": now,
        },
    ]


def qedge_effect_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "effect_id": "QE677_0_conditional_success_path",
            "condition": "B_edge exact, trivial relative class, proper gauge only, variation nohair, same-domain projector silence",
            "qedge_result": "Q_edge=0",
            "alpha_edge_result": "alpha_edge(lambda)=0",
            "arena_effect": "R10/PPN/clock/orbital edge residual removed by theorem-zero",
            "current_status": "not_available",
            "why": "required parent clauses are not all signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "effect_id": "QE677_1_current_status",
            "condition": "current corpus: B_X formula exists but exact class/nohair/projector silence unsigned",
            "qedge_result": "Q_edge_live_residual",
            "alpha_edge_result": "blocked_missing_factors",
            "arena_effect": "local arenas remain blocked, not failed or passed",
            "current_status": "active_blocker",
            "why": "source-backed B_X/Qbar/K/qbar/lambda rows are absent and theorem-zero is unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "effect_id": "QE677_2_safe_interpretation",
            "condition": "conditional lemma plus source-first row template only",
            "qedge_result": "no_Qedge_zero_claim",
            "alpha_edge_result": "no_alpha_claim",
            "arena_effect": "no R10, R11, PPN, clock, orbital, or local-GR claim",
            "current_status": "nonclaim_guardrail",
            "why": "677 sharpens the hinge but does not promote evidence",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D677_0_Bedge_boundary_class",
            "target": "parent-owned B_edge/B_X exact boundary class",
            "result": "conditional_lemma_only_not_closed",
            "reason": "Stokes/cohomology zero is mathematically available only after exactness, trivial relative class, proper-charge guard, nohair, and same-domain projector clauses are signed",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D677_1_first_edge_factor",
            "target": "first source-backed edge factor row",
            "result": "source_row_staged_not_filled",
            "reason": "B_X formula exists but lacks normalization, units, boundary class, counterterm convention, and source-backed/theorem-zero status",
            "next_action": "either sign boundary class/nohair/projector silence or source B_X/Qbar_edge_XH",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D677_2_project_state",
            "target": "R10/local branch honesty",
            "result": "blocked_but_sharper",
            "reason": "we now know the exact clause stack that would kill the edge branch; no claim rows were promoted",
            "next_action": "attack relative boundary class and nohair/projector silence before more data fitting",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def evaluator_rows(
    bedge_rows: list[dict[str, str]],
    bx_rows: list[dict[str, str]],
    qedge_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    bedge_closed = any(row["current_result"] == "closed_claim" and row["valid_for_claim"] == "true" for row in bedge_rows)
    bx_promoted = any(row["valid_for_claim"] == "true" for row in bx_rows)
    qedge_promoted = any(row["valid_for_claim"] == "true" for row in qedge_rows)
    next_selected = any(row["next_action"] == NEXT_TARGET for row in decision)
    return [
        {
            "evaluator_id": "EV677_0_conditional_boundary_lemma",
            "target": "write exact B_edge zero conditions",
            "status": "pass_nonclaim",
            "reason": "conditional Stokes/cohomology route written with proper-charge guard",
            "claim_effect": "none until parent clauses are signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV677_1_parent_ownership",
            "target": "prove parent-owned B_edge/B_X",
            "status": "fail_nonclaim",
            "reason": f"bedge_closed={bool_text(bedge_closed)}; exact representative/relative class/nohair/projector silence remain unsigned",
            "claim_effect": "Qedge_zero remains false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV677_2_first_source_row",
            "target": "promote first source-backed edge factor",
            "status": "fail_nonclaim",
            "reason": f"bx_promoted={bool_text(bx_promoted)}; no numeric/theorem-zero B_X row has units and source path",
            "claim_effect": "alpha_edge remains blocked",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV677_3_claim_guardrail",
            "target": "prevent accidental local claim",
            "status": "pass",
            "reason": f"qedge_promoted={bool_text(qedge_promoted)}; next_selected={bool_text(next_selected)}",
            "claim_effect": "no R10/R11/PPN/local-GR claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "NCS677_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "conditional B_edge exactness lemma written, but parent ownership not closed; first B_X source row staged only",
            "blocked_claims": "Qedge_zero;Qbar_edge_zero;alpha_edge;R10;R11;PPN;clock;orbital;local_GR",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    source_register: list[dict[str, str]],
    bedge_rows: list[dict[str, str]],
    bx_rows: list[dict[str, str]],
    qedge_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    missing_sources = [row["source_id"] for row in source_register if row["exists"] != "true"]
    rows.append({"check_id": "V677_0_source_paths_exist", "result": "pass" if not missing_sources else "fail", "detail": "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources), "generated_utc": now})

    validation_ids = ["667_validation", "668_validation", "670_validation", "671_validation", "672_validation", "673_validation", "674_validation", "675_validation", "676_validation"]
    prior_failures = {source_id: len(validation_failures_for(source_id)) for source_id in validation_ids}
    rows.append({"check_id": "V677_1_prior_validations_clean", "result": "pass" if all(count == 0 for count in prior_failures.values()) else "fail", "detail": ";".join(f"{source_id}={count}" for source_id, count in prior_failures.items()), "generated_utc": now})

    rows.append({"check_id": "V677_2_bedge_audit_coverage", "result": "pass" if len(bedge_rows) >= 7 else "fail", "detail": f"bedge_rows={len(bedge_rows)}", "generated_utc": now})

    verdict_rows = [row for row in bedge_rows if row["audit_id"] == "BBC677_6_verdict"]
    rows.append({"check_id": "V677_3_bedge_not_promoted", "result": "pass" if verdict_rows and verdict_rows[0]["current_result"] == "not_closed_nonclaim" and all(row["valid_for_claim"] == "false" for row in bedge_rows) else "fail", "detail": "parent-owned B_edge remains unsigned", "generated_utc": now})

    rows.append({"check_id": "V677_4_bx_source_row_staged", "result": "pass" if len(bx_rows) >= 4 and all(row["valid_for_claim"] == "false" for row in bx_rows) else "fail", "detail": f"bx_rows={len(bx_rows)};claim_rows={sum(1 for row in bx_rows if row['valid_for_claim']=='true')}", "generated_utc": now})

    rows.append({"check_id": "V677_5_qedge_effect_blocked", "result": "pass" if all(row["valid_for_claim"] == "false" for row in qedge_rows) and any(row["qedge_result"] == "no_Qedge_zero_claim" for row in qedge_rows) else "fail", "detail": "Q_edge effect rows remain nonclaim", "generated_utc": now})

    generated = bedge_rows + bx_rows + qedge_rows + evaluator + decision
    claim_rows = [row for row in generated if row.get("valid_for_claim") == "true"]
    rows.append({"check_id": "V677_6_no_claim_rows_promoted", "result": "pass" if not claim_rows else "fail", "detail": "all generated 677 rows remain valid_for_claim=false" if not claim_rows else f"claim_rows={len(claim_rows)}", "generated_utc": now})

    rows.append({"check_id": "V677_7_next_target_selected", "result": "pass" if any(row["next_action"] == NEXT_TARGET for row in decision) else "fail", "detail": NEXT_TARGET, "generated_utc": now})

    output_paths = [
        RESIDUALS / "P8_Y5_R10_677_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_677_BEDGE_BOUNDARY_CLASS_OWNERSHIP_AUDIT.csv",
        RESIDUALS / "P8_Y5_R10_677_BX_EXACTNESS_OR_SOURCE_ROW.csv",
        RESIDUALS / "P8_Y5_R10_677_QEDGE_EFFECT.csv",
        RESIDUALS / "P8_Y5_R10_677_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_677_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_677_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_677_VALIDATION.csv",
        DOC_PATH,
    ]
    rows.append({"check_id": "V677_8_generated_outputs_scoped", "result": "pass" if all(str(path).startswith(str(ROOT)) for path in output_paths) else "fail", "detail": "all 677 outputs target post-checkpoint-work", "generated_utc": now})

    changed_count = formalization_changed_count()
    rows.append({"check_id": "V677_9_formalization_workbench_untouched", "result": "pass" if changed_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed_count}", "generated_utc": now})

    rows.append({"check_id": "V677_10_status_nonclaim", "result": "pass" if "no_Qedge_zero" in CLAIM_CEILING and "no_R10" in CLAIM_CEILING and "no_local_GR" in CLAIM_CEILING else "fail", "detail": CLAIM_CEILING, "generated_utc": now})

    missing_marker_rows = [row for row in bx_rows if "MISSING_" in ";".join(str(value) for value in row.values())]
    rows.append({"check_id": "V677_11_missing_markers_block_claims", "result": "pass" if missing_marker_rows and not claim_rows else "fail", "detail": f"missing_marker_rows={len(missing_marker_rows)};claim_rows={len(claim_rows)}", "generated_utc": now})

    return rows


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_register: list[dict[str, str]],
    bedge_rows: list[dict[str, str]],
    bx_rows: list[dict[str, str]],
    qedge_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 677 - Y5 R10 Parent-Owned Bedge Boundary Class Or Source First Edge Factor

## Verdict

677 gets a real mathematical shape for the edge kill route, but it does **not** close it.

The conditional lemma is:

```text
If B_edge = d_partial b_edge on the allowed compact local boundary shell,
and [B_edge]_{{H_rel}}=0,
and B_edge lies only in the proper-gauge/topological sector,
and delta_edge S_parent has no boundary hair,
and the quotient/projector use the same boundary domain,
then Q_edge = integral_boundary B_edge = 0.
```

That is the clean route. It is not a hack; it is just Stokes plus a relative-cohomology/proper-charge guard. But the current corpus only gives the candidate formula `B_X^nu=n_mu P^{{mu nu}}`. It does not yet prove that this candidate is the parent-owned exact class `d_partial b_edge`, and it does not yet sign nohair/projector silence. So `Q_edge=0`, `Qbar_edge_XH=0`, and R10/local-GR claims remain blocked.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_register, ["source_id", "source_path", "exists", "role"])}

## Bedge Boundary Class Ownership Audit

{markdown_table(bedge_rows, ["audit_id", "object", "mathematical_form", "needed_for_zero", "current_result", "blocker", "claim_effect_if_pass", "valid_for_claim"])}

## BX Exactness Or Source Row

{markdown_table(bx_rows, ["row_id", "factor", "formula_or_value", "units", "boundary_class", "exactness_status", "counterterm_status", "source_status", "blocking_input", "valid_for_claim"])}

## Qedge Effect

{markdown_table(qedge_rows, ["effect_id", "condition", "qedge_result", "alpha_edge_result", "arena_effect", "current_status", "why", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Next Target

`{NEXT_TARGET}`

Default next route: either sign the relative boundary class/nohair/projector silence stack, or stop trying to kill the edge branch and source the first real `B_X`/`Qbar_edge_XH` factor row. This is the honest fork.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_register = source_register_rows()
    bedge_rows = bedge_boundary_class_rows()
    bx_rows = bx_exactness_or_source_row_rows()
    qedge_rows = qedge_effect_rows()
    decision = decision_rows()
    evaluator = evaluator_rows(bedge_rows, bx_rows, qedge_rows, decision)
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_register, bedge_rows, bx_rows, qedge_rows, evaluator, decision)

    write_csv(RESIDUALS / "P8_Y5_R10_677_SOURCE_REGISTER.csv", source_register, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_677_BEDGE_BOUNDARY_CLASS_OWNERSHIP_AUDIT.csv", bedge_rows, ["audit_id", "object", "mathematical_form", "needed_for_zero", "current_result", "blocker", "claim_effect_if_pass", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_677_BX_EXACTNESS_OR_SOURCE_ROW.csv", bx_rows, ["row_id", "factor", "formula_or_value", "units", "boundary_class", "exactness_status", "counterterm_status", "source_status", "blocking_input", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_677_QEDGE_EFFECT.csv", qedge_rows, ["effect_id", "condition", "qedge_result", "alpha_edge_result", "arena_effect", "current_status", "why", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_677_EVALUATOR.csv", evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_677_DECISION.csv", decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_677_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "blocked_claims", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_677_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_register, bedge_rows, bx_rows, qedge_rows, evaluator, decision, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"bedge_rows={len(bedge_rows)}")
    print(f"bx_rows={len(bx_rows)}")
    print(f"qedge_rows={len(qedge_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
