from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_boundary_class_nohair_projector_silence_not_derived_BX_source_gate_locked_nonclaim"
CLAIM_CEILING = "silence_stack_contract_and_BX_source_gate_only_no_Qedge_zero_no_alpha_edge_no_R10_no_PPN_no_local_GR_claim"
NEXT_TARGET = "679-Y5-R10-first-claim-ready-BX-or-Qbar-source-row-acquisition.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "678-Y5-R10-boundary-class-nohair-projector-silence-or-BX-source-row.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "222_doc": ROOT / "222-parent-X-sector-degree-count-and-boundary-action.md",
    "235_doc": ROOT / "235-projector-stress-variation-or-nohair-constraint-algebra.md",
    "539_doc": ROOT / "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
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
    "674_validation": RESIDUALS / "P8_Y5_BRR545_674_VALIDATION.csv",
    "674_parent_clause": RESIDUALS / "P8_Y5_R10_674_PARENT_PIM_CLAUSE_TEST.csv",
    "674_requirements": RESIDUALS / "P8_Y5_R10_674_COEFFICIENT_REQUIREMENTS.csv",
    "675_validation": RESIDUALS / "P8_Y5_BRR545_675_VALIDATION.csv",
    "675_qedge_audit": RESIDUALS / "P8_Y5_R10_675_QEDGE_NULL_ACTION_CLAUSE_AUDIT.csv",
    "675_scout": RESIDUALS / "P8_Y5_R10_675_SOURCE_BACKED_EDGE_ROW_SCOUT.csv",
    "675_blockers": RESIDUALS / "P8_Y5_R10_675_EDGE_ROW_BLOCKER_MATRIX.csv",
    "676_validation": RESIDUALS / "P8_Y5_BRR545_676_VALIDATION.csv",
    "676_contract": RESIDUALS / "P8_Y5_R10_676_MINIMAL_PARENT_QEDGE_NULL_CONTRACT.csv",
    "676_source_spec": RESIDUALS / "P8_Y5_R10_676_FIRST_SOURCE_ROW_SPEC.csv",
    "677_doc": ROOT / "677-Y5-R10-parent-owned-Bedge-boundary-class-or-source-first-edge-factor.md",
    "677_validation": RESIDUALS / "P8_Y5_BRR545_677_VALIDATION.csv",
    "677_bedge": RESIDUALS / "P8_Y5_R10_677_BEDGE_BOUNDARY_CLASS_OWNERSHIP_AUDIT.csv",
    "677_bx": RESIDUALS / "P8_Y5_R10_677_BX_EXACTNESS_OR_SOURCE_ROW.csv",
    "677_qedge": RESIDUALS / "P8_Y5_R10_677_QEDGE_EFFECT.csv",
    "677_decision": RESIDUALS / "P8_Y5_R10_677_DECISION.csv",
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
        "222_doc": "boundary momentum contract and primitive-selection failure",
        "235_doc": "projector stress/nohair condition source",
        "539_doc": "Hamiltonian mass projection context",
        "667_validation": "667 validation gate",
        "667_ansatz": "parent boundary action ansatz",
        "667_variation": "boundary flux and projector leakage ledger",
        "668_validation": "668 validation gate",
        "668_boundary_lock": "boundary/nohair/projector lock failure rows",
        "670_validation": "670 validation gate",
        "670_no_pole": "quotient no-pole conditional chain",
        "671_validation": "671 validation gate",
        "671_edge": "edge residual vector including B_X",
        "672_validation": "672 validation gate",
        "672_source_plan": "edge coefficient source plan",
        "673_validation": "673 validation gate",
        "673_pim_audit": "Hamiltonian Pi_M orthogonality blocker",
        "674_validation": "674 validation gate",
        "674_parent_clause": "parent Pi_M/null-edge clause test",
        "674_requirements": "coefficient requirements",
        "675_validation": "675 validation gate",
        "675_qedge_audit": "Qedge null action clause audit",
        "675_scout": "source-backed edge row scout",
        "675_blockers": "edge row blocker matrix",
        "676_validation": "676 validation gate",
        "676_contract": "minimal Qedge null parent action contract",
        "676_source_spec": "first acceptable source row spec",
        "677_doc": "immediate predecessor checkpoint",
        "677_validation": "677 validation gate",
        "677_bedge": "Bedge boundary class ownership audit",
        "677_bx": "BX exactness or source row gate",
        "677_qedge": "Qedge effect rows",
        "677_decision": "677 fork decision",
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


def silence_stack_audit_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "clause_id": "SSA678_0_boundary_primitive",
            "clause": "compact-shell boundary primitive exists",
            "mathematical_test": "B_X^nu=n_mu P^{mu nu} pulls back to B_edge=d_partial b_edge",
            "current_result": "candidate_formula_not_primitive",
            "obstruction": "222/235 give B_X but 222 explicitly leaves boundary primitive selection unproved",
            "if_passes": "B_X can be treated as exact boundary data rather than live edge hair",
            "fallback_source_row": "B_X_boundary_momentum",
            "valid_for_claim": "false",
            "source_paths": source_list("222_doc", "235_doc", "677_bedge", "677_bx"),
            "generated_utc": now,
        },
        {
            "clause_id": "SSA678_1_relative_class",
            "clause": "relative boundary class trivial or parent-selected",
            "mathematical_test": "[B_edge]_{H_rel}=0 before local readout",
            "current_result": "not_signed",
            "obstruction": "668 marks relative class C_top as fail_current_claim",
            "if_passes": "Stokes zero is not spoiled by a linked/topological charge",
            "fallback_source_row": "B_zero_flux_or_B_X_boundary_class",
            "valid_for_claim": "false",
            "source_paths": source_list("668_boundary_lock", "667_ansatz", "677_bedge"),
            "generated_utc": now,
        },
        {
            "clause_id": "SSA678_2_no_vector_tensor_hair",
            "clause": "boundary stress has no vector, trace-free tensor, shear, radial, or time hair",
            "mathematical_test": "Pi_vector=Pi_TF=Pi_shear=Pi_radial=Pi_time=0 on allowed shell",
            "current_result": "not_derived",
            "obstruction": "235 writes nohair route but records T_projector and X/J_rel/V_def nohair as fail",
            "if_passes": "edge boundary variations cannot create PPN preferred-frame or fifth-force residuals",
            "fallback_source_row": "boundary_stress_hair_envelope",
            "valid_for_claim": "false",
            "source_paths": source_list("235_doc", "668_boundary_lock", "667_variation"),
            "generated_utc": now,
        },
        {
            "clause_id": "SSA678_3_projector_stress_silence",
            "clause": "projector variations carry their own stress or vanish",
            "mathematical_test": "delta P_mem=-delta Pi_M-delta Pi_TF-delta Pi_matter has owned destinations",
            "current_result": "conditions_written_not_closed",
            "obstruction": "235 states no projector without projector stress and does not derive T_projector=0",
            "if_passes": "hidden projector stress cannot be smuggled into the local equations",
            "fallback_source_row": "T_projector_or_projector_flux_bound",
            "valid_for_claim": "false",
            "source_paths": source_list("235_doc", "668_boundary_lock", "670_no_pole"),
            "generated_utc": now,
        },
        {
            "clause_id": "SSA678_4_domain_projector_lock",
            "clause": "same boundary domain for quotient, projector, charge, and local arena",
            "mathematical_test": "Dq[v_edge]=0 and Pi_M^H[d_partial b_edge]=0 on one parent-owned domain",
            "current_result": "not_signed",
            "obstruction": "668 domain/projector fixed row fails; 670-674 remain conditional",
            "if_passes": "Qbar_edge_XH(lambda)=0 follows from same-domain projector silence",
            "fallback_source_row": "Qbar_edge_XH(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_list("668_boundary_lock", "670_no_pole", "673_pim_audit", "674_parent_clause", "677_bedge"),
            "generated_utc": now,
        },
        {
            "clause_id": "SSA678_5_proper_charge_guard",
            "clause": "exact boundary zero does not delete physical ADM/H_tau/source mass",
            "mathematical_test": "B_edge is exact only in proper gauge/topological sector; H_tau and M_H_ref remain fixed observables",
            "current_result": "not_signed",
            "obstruction": "fixed reference branch, source-measure equality, and Hamiltonian integrability remain unclosed",
            "if_passes": "Q_edge zero becomes physically legal rather than a reference subtraction trick",
            "fallback_source_row": "M_H_ref_or_Qbar_edge_XH_denominator",
            "valid_for_claim": "false",
            "source_paths": source_list("539_doc", "667_variation", "668_boundary_lock", "673_pim_audit", "674_parent_clause"),
            "generated_utc": now,
        },
        {
            "clause_id": "SSA678_6_matter_blindness",
            "clause": "test bodies and matter action are blind to edge representative",
            "mathematical_test": "S_matter=Sbar[q(Phi),psi,theta_obs], partial_edge S_matter=0, qbar_XT=0",
            "current_result": "not_closed",
            "obstruction": "674 keeps same-frame matter quotient as an unsigned route",
            "if_passes": "even a formal edge primitive has no direct test-body response",
            "fallback_source_row": "qbar_XT",
            "valid_for_claim": "false",
            "source_paths": source_list("674_parent_clause", "674_requirements", "671_edge"),
            "generated_utc": now,
        },
        {
            "clause_id": "SSA678_7_verdict",
            "clause": "boundary-class/nohair/projector silence stack",
            "mathematical_test": "SSA678_0 through SSA678_6 all pass",
            "current_result": "not_derived_nonclaim",
            "obstruction": "boundary primitive, relative class, nohair, projector stress, domain lock, proper-charge guard, and matter blindness are not jointly signed",
            "if_passes": "Q_edge=Qbar_edge_XH=qbar_XT=0 and the edge branch is theorem-silent",
            "fallback_source_row": "first claim-ready B_X or Qbar_edge_XH row",
            "valid_for_claim": "false",
            "source_paths": source_list("222_doc", "235_doc", "668_boundary_lock", "674_parent_clause", "677_bedge", "677_bx"),
            "generated_utc": now,
        },
    ]


def bx_source_row_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "BXG678_0_claim_ready_schema",
            "factor": "B_X_boundary_momentum",
            "required_columns": "factor;value_or_theorem_zero;units;lambda_or_shell;boundary_class;counterterm_convention;source_path;equation_ref;derivation_status;valid_for_claim",
            "acceptance_rule": "numeric finite value with units or parent theorem_zero=true; source path exists; no MISSING markers; same boundary convention as R10 arena",
            "current_fill": "schema_only",
            "why_needed": "without B_X exactness or a sourced B_X row, Q_edge cannot be computed or killed",
            "valid_for_claim": "false",
            "source_paths": source_list("676_source_spec", "677_bx", "675_blockers"),
            "generated_utc": now,
        },
        {
            "gate_id": "BXG678_1_corpus_candidate",
            "factor": "B_X_boundary_momentum",
            "required_columns": "formula;normalization;units;boundary_class;counterterm_convention;source_path",
            "acceptance_rule": "B_X^nu=n_mu P^{mu nu} plus explicit P^{mu nu}, B_ct, and shell/domain convention",
            "current_fill": "formula_present_missing_normalization_units_boundary_class_counterterm",
            "why_needed": "the formula is upstream of Q_edge but not yet a claim-ready factor",
            "valid_for_claim": "false",
            "source_paths": source_list("222_doc", "235_doc", "671_edge", "677_bx"),
            "generated_utc": now,
        },
        {
            "gate_id": "BXG678_2_theorem_zero_candidate",
            "factor": "B_edge_exact_zero",
            "required_columns": "exactness_clause;relative_class;proper_charge_guard;nohair_clause;projector_domain;source_paths",
            "acceptance_rule": "all silence-stack clauses pass and no physical charge is removed",
            "current_fill": "conditional_only_stack_fails",
            "why_needed": "the theorem-zero route is cleaner than sourcing a numerical residual if it can be honestly signed",
            "valid_for_claim": "false",
            "source_paths": source_list("677_bedge", "668_boundary_lock", "235_doc"),
            "generated_utc": now,
        },
        {
            "gate_id": "BXG678_3_best_empirical_fallback",
            "factor": "Qbar_edge_XH(lambda)",
            "required_columns": "Pi_M_projection;Q_edge_numerator;M_H_ref;lambda;units;source_path;frame_convention",
            "acceptance_rule": "same-frame Hamiltonian projection numerator and denominator are both sourced or derived",
            "current_fill": "missing_Q_edge_numerator_and_M_H_ref",
            "why_needed": "if B_X cannot be killed, Qbar_edge_XH is the direct measured edge factor",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "673_pim_audit", "674_parent_clause", "675_blockers"),
            "generated_utc": now,
        },
        {
            "gate_id": "BXG678_4_no_shortcut_guard",
            "factor": "edge_branch",
            "required_columns": "no_projector_stress;no_boundary_hair;no_matter_marker;no_missing_units;no_missing_sources",
            "acceptance_rule": "no local arena branch may pass while any required edge factor is MISSING or valid_for_claim=false",
            "current_fill": "guardrail_active",
            "why_needed": "prevents accidental R10/PPN/local-GR promotion from a symbolic boundary expression",
            "valid_for_claim": "false",
            "source_paths": source_list("675_scout", "676_contract", "677_qedge"),
            "generated_utc": now,
        },
    ]


def fork_decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "fork_id": "FD678_0_derive_route",
            "route": "continue theorem-zero proof",
            "result": "not_selected_as_next",
            "reason": "same missing clauses have now been isolated repeatedly; another abstract pass risks looping without a new parent action input",
            "minimum_new_input": "explicit parent boundary action/constraint algebra that signs primitive, relative class, nohair, and projector stress together",
            "next_action": "hold as conditional theorem route",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "fork_id": "FD678_1_source_route",
            "route": "source first B_X or Qbar_edge_XH row",
            "result": "selected",
            "reason": "if the zero theorem cannot be signed now, the most honest progress is to measure/bound the edge factor rather than keep assuming it away",
            "minimum_new_input": "claim-ready B_X_boundary_momentum or Qbar_edge_XH(lambda) row with units, source path, equation reference, and same-frame convention",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "fork_id": "FD678_2_data_route_guard",
            "route": "run local R10 comparator",
            "result": "blocked",
            "reason": "R10 comparator remains premature until at least one theory factor or theorem-zero is claim-ready",
            "minimum_new_input": "one valid theory row plus claim-grade bound curve",
            "next_action": "do not run as evidence yet",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def evaluator_rows(
    silence_rows: list[dict[str, str]],
    bx_gate_rows: list[dict[str, str]],
    fork_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    silence_closed = any(row["current_result"] == "closed_claim" and row["valid_for_claim"] == "true" for row in silence_rows)
    bx_promoted = any(row["valid_for_claim"] == "true" for row in bx_gate_rows)
    source_route_selected = any(row["route"] == "source first B_X or Qbar_edge_XH row" and row["result"] == "selected" for row in fork_rows)
    return [
        {
            "evaluator_id": "EV678_0_silence_stack_attempt",
            "target": "derive boundary-class/nohair/projector silence",
            "status": "fail_nonclaim",
            "reason": f"silence_closed={bool_text(silence_closed)}; 222/235/668 explicitly retain missing primitive, nohair, and projector stress clauses",
            "claim_effect": "Qedge_zero remains false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV678_1_BX_gate",
            "target": "lock first claim-ready B_X source row schema",
            "status": "pass_nonclaim",
            "reason": f"bx_promoted={bool_text(bx_promoted)}; schema and acceptance gates written but not filled",
            "claim_effect": "no alpha_edge promotion",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV678_2_fork",
            "target": "choose next route",
            "status": "selected_nonclaim",
            "reason": f"source_route_selected={bool_text(source_route_selected)}; next step is source acquisition unless new parent action input appears",
            "claim_effect": "next private checkpoint only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV678_3_claim_guardrail",
            "target": "prevent local claim from symbolic boundary expressions",
            "status": "pass",
            "reason": "all 678 rows remain valid_for_claim=false and missing markers block promotion",
            "claim_effect": "no R10/R11/PPN/local-GR claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D678_0_silence_stack",
            "target": "boundary-class/nohair/projector silence theorem",
            "result": "not_derived",
            "reason": "the corpus has conditions and a clean conditional theorem route, but not a signed parent boundary primitive/nohair/projector-stress proof",
            "next_action": "keep as conditional theorem route, not evidence",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D678_1_source_gate",
            "target": "first claim-ready B_X/Qbar edge source row",
            "result": "gate_locked_no_row_promoted",
            "reason": "required columns and acceptance rules are now explicit; current B_X remains formula-only and nonclaim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D678_2_project_status",
            "target": "local/R10 edge branch",
            "result": "blocked_but_testable_next",
            "reason": "the branch is no longer foggy: either provide a parent action that signs silence or source one edge factor",
            "next_action": "source acquisition before comparator rerun",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "NCS678_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "boundary-class/nohair/projector silence stack fails as a proof; B_X/Qbar source gate is locked",
            "blocked_claims": "Qedge_zero;Qbar_edge_zero;qbar_XT_zero;alpha_edge;R10;R11;PPN;clock;orbital;local_GR",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    source_register: list[dict[str, str]],
    silence_rows: list[dict[str, str]],
    bx_gate_rows: list[dict[str, str]],
    fork_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    missing_sources = [row["source_id"] for row in source_register if row["exists"] != "true"]
    rows.append({"check_id": "V678_0_source_paths_exist", "result": "pass" if not missing_sources else "fail", "detail": "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources), "generated_utc": now})

    validation_ids = ["667_validation", "668_validation", "670_validation", "671_validation", "672_validation", "673_validation", "674_validation", "675_validation", "676_validation", "677_validation"]
    prior_failures = {source_id: len(validation_failures_for(source_id)) for source_id in validation_ids}
    rows.append({"check_id": "V678_1_prior_validations_clean", "result": "pass" if all(count == 0 for count in prior_failures.values()) else "fail", "detail": ";".join(f"{source_id}={count}" for source_id, count in prior_failures.items()), "generated_utc": now})

    rows.append({"check_id": "V678_2_silence_stack_coverage", "result": "pass" if len(silence_rows) >= 8 else "fail", "detail": f"silence_rows={len(silence_rows)}", "generated_utc": now})

    verdict_rows = [row for row in silence_rows if row["clause_id"] == "SSA678_7_verdict"]
    rows.append({"check_id": "V678_3_silence_not_promoted", "result": "pass" if verdict_rows and verdict_rows[0]["current_result"] == "not_derived_nonclaim" and all(row["valid_for_claim"] == "false" for row in silence_rows) else "fail", "detail": "silence stack remains nonclaim", "generated_utc": now})

    rows.append({"check_id": "V678_4_bx_gate_locked", "result": "pass" if len(bx_gate_rows) >= 5 and all(row["valid_for_claim"] == "false" for row in bx_gate_rows) else "fail", "detail": f"bx_gate_rows={len(bx_gate_rows)};claim_rows={sum(1 for row in bx_gate_rows if row['valid_for_claim']=='true')}", "generated_utc": now})

    selected_forks = [row for row in fork_rows if row["result"] == "selected"]
    rows.append({"check_id": "V678_5_single_next_route_selected", "result": "pass" if len(selected_forks) == 1 and selected_forks[0]["next_action"] == NEXT_TARGET else "fail", "detail": ";".join(row["route"] for row in selected_forks), "generated_utc": now})

    generated = silence_rows + bx_gate_rows + fork_rows + evaluator + decision
    claim_rows = [row for row in generated if row.get("valid_for_claim") == "true"]
    rows.append({"check_id": "V678_6_no_claim_rows_promoted", "result": "pass" if not claim_rows else "fail", "detail": "all generated 678 rows remain valid_for_claim=false" if not claim_rows else f"claim_rows={len(claim_rows)}", "generated_utc": now})

    rows.append({"check_id": "V678_7_next_target_selected", "result": "pass" if any(row["next_action"] == NEXT_TARGET for row in decision) else "fail", "detail": NEXT_TARGET, "generated_utc": now})

    output_paths = [
        RESIDUALS / "P8_Y5_R10_678_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_678_SILENCE_STACK_AUDIT.csv",
        RESIDUALS / "P8_Y5_R10_678_BX_SOURCE_ROW_GATE.csv",
        RESIDUALS / "P8_Y5_R10_678_FORK_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_678_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_678_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_678_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_678_VALIDATION.csv",
        DOC_PATH,
    ]
    rows.append({"check_id": "V678_8_generated_outputs_scoped", "result": "pass" if all(str(path).startswith(str(ROOT)) for path in output_paths) else "fail", "detail": "all 678 outputs target post-checkpoint-work", "generated_utc": now})

    changed_count = formalization_changed_count()
    rows.append({"check_id": "V678_9_formalization_workbench_untouched", "result": "pass" if changed_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed_count}", "generated_utc": now})

    rows.append({"check_id": "V678_10_status_nonclaim", "result": "pass" if "no_Qedge_zero" in CLAIM_CEILING and "no_R10" in CLAIM_CEILING and "no_local_GR" in CLAIM_CEILING else "fail", "detail": CLAIM_CEILING, "generated_utc": now})

    missing_marker_rows = [row for row in bx_gate_rows if "MISSING" in ";".join(str(value) for value in row.values()) or "missing" in ";".join(str(value) for value in row.values())]
    rows.append({"check_id": "V678_11_missing_or_unfilled_rows_block_claims", "result": "pass" if missing_marker_rows and not claim_rows else "fail", "detail": f"unfilled_rows={len(missing_marker_rows)};claim_rows={len(claim_rows)}", "generated_utc": now})

    blocked_data_routes = [row for row in fork_rows if row["route"] == "run local R10 comparator" and row["result"] == "blocked"]
    rows.append({"check_id": "V678_12_data_route_blocked_until_theory_row", "result": "pass" if blocked_data_routes else "fail", "detail": "R10 comparator remains blocked until theory row exists", "generated_utc": now})

    return rows


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_register: list[dict[str, str]],
    silence_rows: list[dict[str, str]],
    bx_gate_rows: list[dict[str, str]],
    fork_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 678 - Y5 R10 Boundary Class Nohair Projector Silence Or BX Source Row

## Verdict

678 tried the clean theorem route and refused to pretend.

The nohair/projector stack is now exact enough to state:

```text
Q_edge = 0 only if the same parent action signs:
1. B_X -> d_partial b_edge on the compact local shell,
2. [B_edge]_(H_rel)=0 before readout,
3. no vector/tensor/shear/radial/time boundary hair,
4. projector stress is carried or vanishes,
5. quotient, projector, Hamiltonian charge, and arena domain are identical,
6. the exact boundary piece is proper-gauge/topological only,
7. matter/test bodies are blind to the edge representative.
```

The corpus does **not** sign that stack. The useful gain is that the failure is no longer fog: it is a locked fork. Either a future parent action signs the stack, or the next serious move is to source the first claim-ready `B_X_boundary_momentum` or `Qbar_edge_XH(lambda)` row.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_register, ["source_id", "source_path", "exists", "role"])}

## Silence Stack Audit

{markdown_table(silence_rows, ["clause_id", "clause", "mathematical_test", "current_result", "obstruction", "if_passes", "fallback_source_row", "valid_for_claim"])}

## BX Source Row Gate

{markdown_table(bx_gate_rows, ["gate_id", "factor", "required_columns", "acceptance_rule", "current_fill", "why_needed", "valid_for_claim"])}

## Fork Decision

{markdown_table(fork_rows, ["fork_id", "route", "result", "reason", "minimum_new_input", "next_action", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Next Target

`{NEXT_TARGET}`

Default next route: stop looping on abstract silence unless a new parent action input appears. Acquire or construct the first claim-ready `B_X_boundary_momentum` or `Qbar_edge_XH(lambda)` row, still nonclaim until it satisfies the gate.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_register = source_register_rows()
    silence_rows = silence_stack_audit_rows()
    bx_gate_rows = bx_source_row_gate_rows()
    fork_rows = fork_decision_rows()
    evaluator = evaluator_rows(silence_rows, bx_gate_rows, fork_rows)
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_register, silence_rows, bx_gate_rows, fork_rows, evaluator, decision)

    write_csv(RESIDUALS / "P8_Y5_R10_678_SOURCE_REGISTER.csv", source_register, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_678_SILENCE_STACK_AUDIT.csv", silence_rows, ["clause_id", "clause", "mathematical_test", "current_result", "obstruction", "if_passes", "fallback_source_row", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_678_BX_SOURCE_ROW_GATE.csv", bx_gate_rows, ["gate_id", "factor", "required_columns", "acceptance_rule", "current_fill", "why_needed", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_678_FORK_DECISION.csv", fork_rows, ["fork_id", "route", "result", "reason", "minimum_new_input", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_678_EVALUATOR.csv", evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_678_DECISION.csv", decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_678_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "blocked_claims", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_678_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_register, silence_rows, bx_gate_rows, fork_rows, evaluator, decision, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"silence_rows={len(silence_rows)}")
    print(f"bx_gate_rows={len(bx_gate_rows)}")
    print(f"fork_rows={len(fork_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
