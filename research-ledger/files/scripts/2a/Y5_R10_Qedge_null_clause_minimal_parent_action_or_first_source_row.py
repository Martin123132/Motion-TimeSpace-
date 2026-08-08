from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_Qedge_null_minimal_parent_action_contract_written_not_signed_first_source_row_spec_staged_nonclaim"
CLAIM_CEILING = "Qedge_null_minimal_parent_action_contract_and_first_source_row_spec_only_no_Qedge_zero_no_R10_no_R11_no_PPN_no_local_GR_claim"
NEXT_TARGET = "677-Y5-R10-parent-owned-Bedge-boundary-class-or-source-first-edge-factor.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC_PATH = ROOT / "676-Y5-R10-Qedge-null-clause-minimal-parent-action-or-first-source-row.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "222_doc": ROOT / "222-parent-X-sector-degree-count-and-boundary-action.md",
    "235_doc": ROOT / "235-projector-stress-variation-or-nohair-constraint-algebra.md",
    "539_doc": ROOT / "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
    "544_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
    "589_validation": RESIDUALS / "P8_Y5_BRR545_589_VALIDATION.csv",
    "589_template": RESIDUALS / "P8_Y5_R10_589_SOURCE_BACKED_EDGE_PRODUCT_ROW_TEMPLATE.csv",
    "590_validation": RESIDUALS / "P8_Y5_BRR545_590_VALIDATION.csv",
    "590_status": RESIDUALS / "P8_Y5_R10_590_EDGE_ROW_SOURCE_STATUS.csv",
    "591_validation": RESIDUALS / "P8_Y5_BRR545_591_VALIDATION.csv",
    "591_status": RESIDUALS / "P8_Y5_R10_591_EDGE_SOURCE_INPUT_STATUS.csv",
    "592_validation": RESIDUALS / "P8_Y5_BRR545_592_VALIDATION.csv",
    "592_plan": RESIDUALS / "P8_Y5_R10_592_EDGE_COEFFICIENT_SOURCE_PLAN.csv",
    "593_validation": RESIDUALS / "P8_Y5_BRR545_593_VALIDATION.csv",
    "593_inputs": RESIDUALS / "P8_Y5_R10_593_EDGE_COEFFICIENT_INPUT_ROWS.csv",
    "621_doc": ROOT / "621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md",
    "622_doc": ROOT / "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md",
    "629_validation": RESIDUALS / "P8_Y5_BRR545_629_VALIDATION.csv",
    "629_source_search": RESIDUALS / "P8_Y5_R10_629_SOURCE_SEARCH_STATUS.csv",
    "629_curve_audit": RESIDUALS / "P8_Y5_R10_629_R10_CURVE_PROMOTION_AUDIT.csv",
    "bound_live": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
    "bound_review": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv",
    "667_validation": RESIDUALS / "P8_Y5_BRR545_667_VALIDATION.csv",
    "667_ansatz": RESIDUALS / "P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv",
    "667_variation": RESIDUALS / "P8_Y5_R10_667_VARIATION_LEDGER.csv",
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
    "673_acquisition": RESIDUALS / "P8_Y5_R10_673_EDGE_COEFFICIENT_ACQUISITION_LEDGER.csv",
    "674_validation": RESIDUALS / "P8_Y5_BRR545_674_VALIDATION.csv",
    "674_parent_clause": RESIDUALS / "P8_Y5_R10_674_PARENT_PIM_CLAUSE_TEST.csv",
    "674_requirements": RESIDUALS / "P8_Y5_R10_674_COEFFICIENT_REQUIREMENTS.csv",
    "674_row_pack": RESIDUALS / "P8_Y5_R10_674_EDGE_ROW_FILL_PACK.csv",
    "675_doc": ROOT / "675-Y5-R10-source-backed-edge-row-scout-or-Qedge-null-action-clause.md",
    "675_validation": RESIDUALS / "P8_Y5_BRR545_675_VALIDATION.csv",
    "675_qedge_audit": RESIDUALS / "P8_Y5_R10_675_QEDGE_NULL_ACTION_CLAUSE_AUDIT.csv",
    "675_scout": RESIDUALS / "P8_Y5_R10_675_SOURCE_BACKED_EDGE_ROW_SCOUT.csv",
    "675_blockers": RESIDUALS / "P8_Y5_R10_675_EDGE_ROW_BLOCKER_MATRIX.csv",
    "675_pressure": RESIDUALS / "P8_Y5_R10_675_PRESSURE_ONLY_STATUS.csv",
    "675_decision": RESIDUALS / "P8_Y5_R10_675_DECISION.csv",
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
    return [row for row in read_csv(SOURCE_PATHS[source_id]) if row.get("result") != "pass"]


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
        "222_doc": "early parent X-sector boundary action source",
        "235_doc": "projector stress and B_X boundary formula source",
        "539_doc": "Hamiltonian Pi_M candidate definition",
        "544_status": "boundary/reference first-row missing status",
        "589_validation": "589 validation gate",
        "589_template": "source-backed edge product template",
        "590_validation": "590 validation gate",
        "590_status": "edge row source status",
        "591_validation": "591 validation gate",
        "591_status": "edge source input status",
        "592_validation": "592 validation gate",
        "592_plan": "edge coefficient source plan",
        "593_validation": "593 validation gate",
        "593_inputs": "edge coefficient input rows",
        "621_doc": "matter coupling normal form context",
        "622_doc": "parent matter sector contract context",
        "629_validation": "629 validation gate",
        "629_source_search": "R10 source search status",
        "629_curve_audit": "R10 curve promotion audit",
        "bound_live": "live digitized R10 bound curve file",
        "bound_review": "private review candidate curve",
        "667_validation": "667 validation gate",
        "667_ansatz": "parent boundary action ansatz",
        "667_variation": "parent variation ledger",
        "668_validation": "668 validation gate",
        "668_boundary_lock": "boundary condition lock",
        "670_validation": "670 validation gate",
        "670_no_pole": "no-pole quotient proof chain",
        "671_validation": "671 validation gate",
        "671_edge": "edge residual vector",
        "672_validation": "672 validation gate",
        "672_source_plan": "edge coefficient source plan",
        "673_validation": "673 validation gate",
        "673_pim_audit": "Pi_M orthogonality audit",
        "673_acquisition": "edge coefficient acquisition ledger",
        "674_validation": "674 validation gate",
        "674_parent_clause": "parent PiM clause test",
        "674_requirements": "coefficient requirements",
        "674_row_pack": "edge row fill pack",
        "675_doc": "immediate predecessor checkpoint",
        "675_validation": "675 validation gate",
        "675_qedge_audit": "Qedge null action audit",
        "675_scout": "source-backed edge row scout",
        "675_blockers": "edge row blocker matrix",
        "675_pressure": "pressure-only status",
        "675_decision": "675 decision rows",
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


def minimal_action_contract_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "contract_id": "MAC676_0_field_bundle",
            "object": "edge parent fields",
            "minimal_form": "Phi=(g,psi,X_edge,b_edge,C_boundary,q,tau)",
            "must_prove": "X_edge/b_edge are parent variables or quotient-null representatives, not post-readout knobs",
            "current_result": "candidate_contract_only",
            "blocker": "field bundle exists in 667/668 as scaffold, not as unique MTS parent action",
            "claim_effect_if_pass": "edge branch becomes a theorem target rather than coefficient-fitting target",
            "valid_for_claim": "false",
            "source_paths": source_list("667_ansatz", "668_boundary_lock", "675_qedge_audit"),
            "generated_utc": now,
        },
        {
            "contract_id": "MAC676_1_boundary_exact_action",
            "object": "B_edge exact boundary action",
            "minimal_form": "S_edge=int_boundary d_boundary b_edge with fixed compact boundary class",
            "must_prove": "B_edge=d_boundary b_edge on the allowed local shell, with no improper physical charge removed",
            "current_result": "not_signed",
            "blocker": "222/235 give B_X=n_mu P^{mu nu} style candidate, but not exact parent class ownership",
            "claim_effect_if_pass": "Q_edge local compact charge can vanish",
            "valid_for_claim": "false",
            "source_paths": source_list("222_doc", "235_doc", "667_variation", "675_qedge_audit"),
            "generated_utc": now,
        },
        {
            "contract_id": "MAC676_2_variational_silence",
            "object": "edge variation",
            "minimal_form": "delta_edge S_parent=0 or integral_boundary delta d b_edge=0 under fixed boundary class",
            "must_prove": "allowed variations fix the edge class before readout and do not depend on source/range/frame",
            "current_result": "not_closed",
            "blocker": "668 boundary lock still fails for relative class, nohair, projector/domain silence, and tau",
            "claim_effect_if_pass": "no edge Euler/source term enters local exterior equations",
            "valid_for_claim": "false",
            "source_paths": source_list("668_boundary_lock", "667_variation", "674_parent_clause"),
            "generated_utc": now,
        },
        {
            "contract_id": "MAC676_3_Noether_edge_charge",
            "object": "Q_edge",
            "minimal_form": "J_edge=dQ_edge+C_edge, Q_edge=int_boundary epsilon B_edge",
            "must_prove": "Q_edge=0 for the allowed local boundary or is pure exact/proper gauge",
            "current_result": "not_signed",
            "blocker": "670-672 preserve conditional quotient/exact-sector zeros but not the measured edge charge",
            "claim_effect_if_pass": "K_edge and B_X source slots become inactive",
            "valid_for_claim": "false",
            "source_paths": source_list("670_no_pole", "671_edge", "672_source_plan", "675_qedge_audit"),
            "generated_utc": now,
        },
        {
            "contract_id": "MAC676_4_Hamiltonian_mass_annihilator",
            "object": "Pi_M^H[Q_edge]",
            "minimal_form": "Pi_M^H[Q_edge^H(lambda)]/M_H_ref=0",
            "must_prove": "Hamiltonian mass representative, edge representative, fixed reference, and source frame are parent-owned",
            "current_result": "not_derived",
            "blocker": "673/674 show Pi_M orthogonality and M_H_ref remain unsigned",
            "claim_effect_if_pass": "Qbar_edge_XH(lambda)=0",
            "valid_for_claim": "false",
            "source_paths": source_list("539_doc", "544_status", "673_pim_audit", "674_parent_clause"),
            "generated_utc": now,
        },
        {
            "contract_id": "MAC676_5_matter_quotient_blindness",
            "object": "qbar_XT",
            "minimal_form": "S_matter=Sbar[q(Phi),psi,theta_obs], partial_edge S_matter=0",
            "must_prove": "test bodies see only quotient/observed variables in the same frame before fitting",
            "current_result": "not_closed",
            "blocker": "matter coupling normal form remains a route, not a signed theorem-zero",
            "claim_effect_if_pass": "qbar_XT=0",
            "valid_for_claim": "false",
            "source_paths": source_list("621_doc", "622_doc", "674_requirements", "675_blockers"),
            "generated_utc": now,
        },
        {
            "contract_id": "MAC676_6_verdict",
            "object": "minimal parent Qedge null clause",
            "minimal_form": "MAC676_0 through MAC676_5 jointly imply alpha_edge(lambda)=0",
            "must_prove": "all clauses are parent-signed without missing markers or diagnostic/source placeholders",
            "current_result": "contract_written_not_signed",
            "blocker": "B_edge boundary class and Pi_M annihilator remain the two hardest hinges",
            "claim_effect_if_pass": "R10 edge branch can be demoted to theorem-zero candidate",
            "valid_for_claim": "false",
            "source_paths": source_list("675_decision", "675_validation"),
            "generated_utc": now,
        },
    ]


def first_source_row_spec_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "row_id": "FSR676_0_first_acceptable_edge_factor_row",
            "target_factor": "choose one of B_X_boundary_momentum, Qbar_edge_XH, K_edge, qbar_XT, lambda_edge, M_H_ref",
            "minimum_columns": "factor;value;units;theorem_zero;source_path;derivation_status;assumptions;valid_for_claim",
            "acceptance_rule": "numeric positive/finite value or theorem_zero=true, no MISSING/diagnostic/placeholder markers, source path exists",
            "current_fill": "none_found",
            "why_first": "one real factor row would turn the branch from pure blockage into a measurable residual chain",
            "valid_for_claim": "false",
            "source_paths": source_list("675_scout", "675_blockers", "674_row_pack"),
            "generated_utc": now,
        },
        {
            "row_id": "FSR676_1_best_derivation_first_factor",
            "target_factor": "B_X_boundary_momentum",
            "minimum_columns": "B_X_formula;boundary_class;exactness_status;counterterm;source_path;valid_for_claim",
            "acceptance_rule": "prove B_X=d_boundary b_edge with fixed class, or give source-backed boundary momentum expression",
            "current_fill": "missing_boundary_owner",
            "why_first": "B_X is upstream of Q_edge and can kill or define the edge charge directly",
            "valid_for_claim": "false",
            "source_paths": source_list("222_doc", "235_doc", "667_variation", "675_qedge_audit"),
            "generated_utc": now,
        },
        {
            "row_id": "FSR676_2_best_empirical_pressure_factor",
            "target_factor": "Qbar_edge_XH",
            "minimum_columns": "Q_edge_numerator;M_H_ref;projection_convention;lambda;units;source_path;valid_for_claim",
            "acceptance_rule": "derive or source Pi_M^H[Q_edge]/M_H_ref in the same frame with fixed reference",
            "current_fill": "missing_Hamiltonian_projection_and_denominator",
            "why_first": "this is the central factor in alpha_edge and directly tests whether the edge carries measured mass",
            "valid_for_claim": "false",
            "source_paths": source_list("673_pim_audit", "544_status", "675_blockers"),
            "generated_utc": now,
        },
        {
            "row_id": "FSR676_3_bound_curve_guardrail",
            "target_factor": "alpha_bound(lambda)",
            "minimum_columns": "lambda_value;lambda_units;alpha_bound;source;digitization_method;valid_for_claim",
            "acceptance_rule": "live bound file promoted from source-backed QA; review candidate remains private pressure only",
            "current_fill": "live_file_not_promoted_review_curve_available",
            "why_first": "needed only after at least one real MTS edge factor exists",
            "valid_for_claim": "false",
            "source_paths": source_list("629_source_search", "629_curve_audit", "bound_live", "bound_review", "675_pressure"),
            "generated_utc": now,
        },
    ]


def route_selection_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "route_id": "RS676_0_best_next",
            "route": "derive B_edge boundary class first",
            "reason": "B_edge/B_X is upstream of Q_edge, K_edge, and Qbar_edge_XH; source rows are impossible to claim while the boundary representative is unowned",
            "risk": "may still fail if boundary nohair/projector silence cannot be parent-owned",
            "fallback": "source first edge factor row as retained residual",
            "selected": "true",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "route_id": "RS676_1_second_best",
            "route": "source Qbar_edge_XH first",
            "reason": "directly measures the unresolved Hamiltonian projection if theorem-zero fails",
            "risk": "needs M_H_ref and fixed source frame, which are also unresolved",
            "fallback": "source B_X or M_H_ref first",
            "selected": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "route_id": "RS676_2_defer",
            "route": "use private pressure rows",
            "reason": "private review curve and prior grids are useful intuition but cannot source the theory coefficients",
            "risk": "would overfit or smuggle if treated as evidence",
            "fallback": "keep pressure rows nonclaim only",
            "selected": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def handoff_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "area": "overall_status",
            "where_we_are": "private formal framework with strict ledgers, not a public claim",
            "what_is_good": "the missing local-GR/R10 objects are now explicit rather than foggy",
            "what_is_missing": "parent-owned boundary representative, Pi_M mass annihilator, matter quotient blindness, source-backed edge coefficients",
            "next_best_action": "derive B_edge boundary class or source first edge factor row",
            "generated_utc": now,
        },
        {
            "area": "local_GR_reduction",
            "where_we_are": "conditional GR-style Hamiltonian/source-measure route exists",
            "what_is_good": "we know the right standard structure: covariant phase-space charge, fixed reference, same-frame source, Poisson/Gauss readout",
            "what_is_missing": "current MTS has not signed fixed reference, boundary flux zero, M_H_ref measured source mass, or PPN followthrough",
            "next_best_action": "continue parent action ownership, not plateau axioms",
            "generated_utc": now,
        },
        {
            "area": "R10_edge_branch",
            "where_we_are": "blocked but sharply diagnosed",
            "what_is_good": "templates, pressure curves, and blocker matrix exist; no accidental claim-valid row",
            "what_is_missing": "lambda_edge, K_edge, Qbar_edge_XH, qbar_XT, B_X, M_H_ref, live bound curve promotion",
            "next_best_action": "start with B_X/B_edge because it can kill or define Q_edge",
            "generated_utc": now,
        },
        {
            "area": "empirical_testing",
            "where_we_are": "private pressure data exists, claim-grade local R10 input does not",
            "what_is_good": "review candidate has numeric pressure rows and comparator discipline",
            "what_is_missing": "promoted source-backed bound curve and theory coefficients",
            "next_best_action": "do data after at least one real theory coefficient/theorem-zero exists",
            "generated_utc": now,
        },
        {
            "area": "honest_assessment",
            "where_we_are": "not dead, not proven; now a disciplined research programme",
            "what_is_good": "the work is becoming referee-readable because every claim has gates and no smuggled zeros",
            "what_is_missing": "one decisive parent mechanism that makes extra/local edge sectors silent while preserving GR",
            "next_best_action": "attack the boundary representative hinge before broadening scope",
            "generated_utc": now,
        },
    ]


def evaluator_rows(
    contract_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    contract_claim_rows = sum(1 for row in contract_rows if row["valid_for_claim"] == "true")
    source_claim_rows = sum(1 for row in source_rows if row["valid_for_claim"] == "true")
    selected_route = next(row["route"] for row in route_rows if row["selected"] == "true")
    return [
        {
            "evaluator_id": "EV676_0_minimal_action_contract",
            "target": "derive Qedge null parent action clause",
            "status": "fail_nonclaim",
            "reason": f"contract_claim_rows={contract_claim_rows}; contract written but not signed",
            "claim_effect": "Qedge_zero remains false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV676_1_first_source_row",
            "target": "stage first acceptable source row",
            "status": "pass_nonclaim",
            "reason": f"source_claim_rows={source_claim_rows}; spec written for first future row",
            "claim_effect": "no R10 evidence promoted",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV676_2_route",
            "target": "choose next best hinge",
            "status": "selected_nonclaim",
            "reason": selected_route,
            "claim_effect": "next private checkpoint only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D676_0_Qedge_null_contract",
            "target": "minimal parent Qedge null action",
            "result": "contract_written_not_signed",
            "reason": "B_edge boundary class and Pi_M annihilator are not parent-owned yet",
            "next_action": "derive parent-owned B_edge boundary class",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D676_1_first_source_row",
            "target": "first source-backed edge factor row",
            "result": "spec_staged_no_value",
            "reason": "no claim-valid local source row exists; acceptable row columns and acceptance rule are now explicit",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D676_2_handoff",
            "target": "week-limit summary",
            "result": "handoff_rows_written",
            "reason": "project state captured for restart without losing the thread",
            "next_action": "resume at 677 after limit reset",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "NCS676_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "minimal parent Qedge null contract written but not signed; first source row spec staged",
            "blocked_claims": "Qedge_zero;Qbar_edge_zero;R10;R11;PPN;local_GR",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    source_register: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    source_row_specs: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    handoff_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    missing_sources = [row["source_id"] for row in source_register if row["exists"] != "true"]
    rows.append({"check_id": "V676_0_source_paths_exist", "result": "pass" if not missing_sources else "fail", "detail": "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources), "generated_utc": now})

    validation_ids = ["589_validation", "590_validation", "591_validation", "592_validation", "593_validation", "629_validation", "667_validation", "668_validation", "670_validation", "671_validation", "672_validation", "673_validation", "674_validation", "675_validation"]
    prior_failures = {source_id: len(validation_failures_for(source_id)) for source_id in validation_ids}
    rows.append({"check_id": "V676_1_prior_validations_clean", "result": "pass" if all(count == 0 for count in prior_failures.values()) else "fail", "detail": ";".join(f"{source_id}={count}" for source_id, count in prior_failures.items()), "generated_utc": now})

    rows.append({"check_id": "V676_2_minimal_contract_coverage", "result": "pass" if len(contract_rows) >= 7 else "fail", "detail": f"contract_rows={len(contract_rows)}", "generated_utc": now})

    rows.append({"check_id": "V676_3_contract_not_promoted", "result": "pass" if all(row["valid_for_claim"] == "false" for row in contract_rows) and any(row["current_result"] == "contract_written_not_signed" for row in contract_rows) else "fail", "detail": "minimal action contract remains nonclaim", "generated_utc": now})

    rows.append({"check_id": "V676_4_first_source_row_spec_coverage", "result": "pass" if len(source_row_specs) >= 4 else "fail", "detail": f"source_row_specs={len(source_row_specs)}", "generated_utc": now})

    rows.append({"check_id": "V676_5_route_selected", "result": "pass" if sum(1 for row in route_rows if row["selected"] == "true") == 1 else "fail", "detail": ";".join(row["route"] for row in route_rows if row["selected"] == "true"), "generated_utc": now})

    rows.append({"check_id": "V676_6_handoff_summary_written", "result": "pass" if len(handoff_rows) >= 5 else "fail", "detail": f"handoff_rows={len(handoff_rows)}", "generated_utc": now})

    generated = contract_rows + source_row_specs + route_rows + handoff_rows + evaluator + decision
    claim_rows = [row for row in generated if row.get("valid_for_claim") == "true"]
    rows.append({"check_id": "V676_7_no_claim_rows_promoted", "result": "pass" if not claim_rows else "fail", "detail": "all generated rows remain valid_for_claim=false" if not claim_rows else f"claim_rows={len(claim_rows)}", "generated_utc": now})

    rows.append({"check_id": "V676_8_next_target_selected", "result": "pass" if any(row["next_action"] == NEXT_TARGET for row in decision) else "fail", "detail": NEXT_TARGET, "generated_utc": now})

    output_paths = [
        RESIDUALS / "P8_Y5_R10_676_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_676_MINIMAL_PARENT_QEDGE_NULL_CONTRACT.csv",
        RESIDUALS / "P8_Y5_R10_676_FIRST_SOURCE_ROW_SPEC.csv",
        RESIDUALS / "P8_Y5_R10_676_ROUTE_SELECTION.csv",
        RESIDUALS / "P8_Y5_R10_676_HANDOFF_SUMMARY.csv",
        RESIDUALS / "P8_Y5_R10_676_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_676_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_676_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_676_VALIDATION.csv",
        DOC_PATH,
    ]
    rows.append({"check_id": "V676_9_generated_outputs_scoped", "result": "pass" if all(str(path).startswith(str(ROOT)) for path in output_paths) else "fail", "detail": "all 676 outputs target post-checkpoint-work", "generated_utc": now})

    changed_count = formalization_changed_count()
    rows.append({"check_id": "V676_10_formalization_workbench_untouched", "result": "pass" if changed_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed_count}", "generated_utc": now})

    rows.append({"check_id": "V676_11_status_nonclaim", "result": "pass" if "no_Qedge_zero" in CLAIM_CEILING and "no_R10" in CLAIM_CEILING else "fail", "detail": CLAIM_CEILING, "generated_utc": now})

    return rows


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_register: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    source_row_specs: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    handoff_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 676 - Y5 R10 Qedge Null Clause Minimal Parent Action Or First Source Row

## Verdict

676 writes the smallest honest parent-action contract that could kill the edge branch:

```text
Phi=(g,psi,X_edge,b_edge,C_boundary,q,tau)
S_edge = int_boundary d_boundary b_edge
Dq[v_edge] = 0
Pi_M^H[Q_edge^H(lambda)]/M_H_ref = 0
S_matter = Sbar[q(Phi),psi,theta_obs]
```

It does **not** sign it. The core hinge is still the parent-owned `B_edge` boundary class plus the Hamiltonian mass annihilator. Without those, `Q_edge=0`, `Qbar_edge_XH=0`, and R10 remain nonclaim.

676 also stages the first acceptable source-row spec, so the fallback is clear: source one real edge factor row with units and a real source path, or keep the branch blocked.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_register, ["source_id", "source_path", "exists", "role"])}

## Minimal Parent Qedge Null Contract

{markdown_table(contract_rows, ["contract_id", "object", "minimal_form", "must_prove", "current_result", "blocker", "claim_effect_if_pass", "valid_for_claim"])}

## First Source Row Spec

{markdown_table(source_row_specs, ["row_id", "target_factor", "minimum_columns", "acceptance_rule", "current_fill", "why_first", "valid_for_claim"])}

## Route Selection

{markdown_table(route_rows, ["route_id", "route", "reason", "risk", "fallback", "selected", "valid_for_claim"])}

## Handoff Summary

{markdown_table(handoff_rows, ["area", "where_we_are", "what_is_good", "what_is_missing", "next_best_action"])}

## Evaluator

{markdown_table(evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Next Target

`{NEXT_TARGET}`

Default next route: attack `B_edge`/`B_X` boundary class ownership first. It is the most upstream hinge: it can either kill `Q_edge` or define the first source-backed edge factor.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_register = source_register_rows()
    contract_rows = minimal_action_contract_rows()
    source_row_specs = first_source_row_spec_rows()
    route_rows = route_selection_rows()
    handoff_rows = handoff_summary_rows()
    evaluator = evaluator_rows(contract_rows, source_row_specs, route_rows)
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_register, contract_rows, source_row_specs, route_rows, handoff_rows, evaluator, decision)

    write_csv(RESIDUALS / "P8_Y5_R10_676_SOURCE_REGISTER.csv", source_register, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_676_MINIMAL_PARENT_QEDGE_NULL_CONTRACT.csv", contract_rows, ["contract_id", "object", "minimal_form", "must_prove", "current_result", "blocker", "claim_effect_if_pass", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_676_FIRST_SOURCE_ROW_SPEC.csv", source_row_specs, ["row_id", "target_factor", "minimum_columns", "acceptance_rule", "current_fill", "why_first", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_676_ROUTE_SELECTION.csv", route_rows, ["route_id", "route", "reason", "risk", "fallback", "selected", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_676_HANDOFF_SUMMARY.csv", handoff_rows, ["area", "where_we_are", "what_is_good", "what_is_missing", "next_best_action", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_676_EVALUATOR.csv", evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_676_DECISION.csv", decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_676_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "blocked_claims", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_676_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_register, contract_rows, source_row_specs, route_rows, handoff_rows, evaluator, decision, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"contract_rows={len(contract_rows)}")
    print(f"source_row_specs={len(source_row_specs)}")
    print(f"handoff_rows={len(handoff_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
