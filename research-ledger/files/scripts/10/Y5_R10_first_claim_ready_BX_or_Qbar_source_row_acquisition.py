from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_first_claim_ready_BX_or_Qbar_source_row_not_found_acquisition_ledger_written_nonclaim"
CLAIM_CEILING = "candidate_source_rows_only_no_BX_promotion_no_Qbar_promotion_no_alpha_edge_no_R10_no_PPN_no_local_GR_claim"
NEXT_TARGET = "680-Y5-R10-parent-P-constitutive-owner-or-Qbar-numeric-denominator-source.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "679-Y5-R10-first-claim-ready-BX-or-Qbar-source-row-acquisition.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "222_doc": ROOT / "222-parent-X-sector-degree-count-and-boundary-action.md",
    "223_doc": ROOT / "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md",
    "235_doc": ROOT / "235-projector-stress-variation-or-nohair-constraint-algebra.md",
    "539_doc": ROOT / "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
    "667_validation": RESIDUALS / "P8_Y5_BRR545_667_VALIDATION.csv",
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
    "673_acquisition": RESIDUALS / "P8_Y5_R10_673_EDGE_COEFFICIENT_ACQUISITION_LEDGER.csv",
    "673_pim_audit": RESIDUALS / "P8_Y5_R10_673_HAMILTONIAN_PIM_ORTHOGONALITY_PROOF_AUDIT.csv",
    "674_validation": RESIDUALS / "P8_Y5_BRR545_674_VALIDATION.csv",
    "674_parent_clause": RESIDUALS / "P8_Y5_R10_674_PARENT_PIM_CLAUSE_TEST.csv",
    "674_requirements": RESIDUALS / "P8_Y5_R10_674_COEFFICIENT_REQUIREMENTS.csv",
    "674_fill_pack": RESIDUALS / "P8_Y5_R10_674_EDGE_ROW_FILL_PACK.csv",
    "675_validation": RESIDUALS / "P8_Y5_BRR545_675_VALIDATION.csv",
    "675_scout": RESIDUALS / "P8_Y5_R10_675_SOURCE_BACKED_EDGE_ROW_SCOUT.csv",
    "675_blockers": RESIDUALS / "P8_Y5_R10_675_EDGE_ROW_BLOCKER_MATRIX.csv",
    "676_validation": RESIDUALS / "P8_Y5_BRR545_676_VALIDATION.csv",
    "676_source_spec": RESIDUALS / "P8_Y5_R10_676_FIRST_SOURCE_ROW_SPEC.csv",
    "677_validation": RESIDUALS / "P8_Y5_BRR545_677_VALIDATION.csv",
    "677_bedge": RESIDUALS / "P8_Y5_R10_677_BEDGE_BOUNDARY_CLASS_OWNERSHIP_AUDIT.csv",
    "677_bx": RESIDUALS / "P8_Y5_R10_677_BX_EXACTNESS_OR_SOURCE_ROW.csv",
    "678_doc": ROOT / "678-Y5-R10-boundary-class-nohair-projector-silence-or-BX-source-row.md",
    "678_validation": RESIDUALS / "P8_Y5_BRR545_678_VALIDATION.csv",
    "678_silence": RESIDUALS / "P8_Y5_R10_678_SILENCE_STACK_AUDIT.csv",
    "678_bx_gate": RESIDUALS / "P8_Y5_R10_678_BX_SOURCE_ROW_GATE.csv",
    "678_fork": RESIDUALS / "P8_Y5_R10_678_FORK_DECISION.csv",
    "boundary_reference_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
    "hamiltonian_source_contract": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
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
        "222_doc": "B_X boundary momentum contract",
        "223_doc": "P[Y] constitutive owner and constraint-algebra route",
        "235_doc": "projector stress/nohair and B_X formula",
        "539_doc": "Hamiltonian Pi_M candidate definition",
        "667_validation": "667 validation gate",
        "667_variation": "boundary flux and charge decomposition ledger",
        "668_validation": "668 validation gate",
        "668_boundary_lock": "boundary class/nohair/projector lock rows",
        "670_validation": "670 validation gate",
        "670_no_pole": "quotient no-pole conditional chain",
        "671_validation": "671 validation gate",
        "671_edge": "edge residual vector",
        "672_validation": "672 validation gate",
        "672_source_plan": "edge coefficient source plan",
        "673_validation": "673 validation gate",
        "673_acquisition": "edge coefficient acquisition ledger",
        "673_pim_audit": "Hamiltonian Pi_M orthogonality audit",
        "674_validation": "674 validation gate",
        "674_parent_clause": "parent PiM/null-edge clause test",
        "674_requirements": "coefficient requirements",
        "674_fill_pack": "edge row fill pack",
        "675_validation": "675 validation gate",
        "675_scout": "source-backed edge row scout",
        "675_blockers": "edge blocker matrix",
        "676_validation": "676 validation gate",
        "676_source_spec": "first source row spec",
        "677_validation": "677 validation gate",
        "677_bedge": "Bedge boundary ownership audit",
        "677_bx": "BX exactness/source row gate",
        "678_doc": "immediate predecessor checkpoint",
        "678_validation": "678 validation gate",
        "678_silence": "silence stack audit",
        "678_bx_gate": "BX source row gate",
        "678_fork": "source acquisition fork decision",
        "boundary_reference_status": "boundary/reference first row status",
        "hamiltonian_source_contract": "Hamiltonian source measure contract",
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


def candidate_source_scout_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "candidate_id": "CSS679_0_BX_formula_222_235",
            "target_factor": "B_X_boundary_momentum",
            "candidate_value": "B_X^nu=n_mu P^{mu nu}",
            "what_is_real": "local source path exists and boundary equation is present",
            "missing_for_claim": "P^{mu nu} normalization; units; counterterm B_ct; parent fixed C_top; compact shell; exact/proper-charge status",
            "gate_status": "fails_BXG678_1",
            "claim_ready": "false",
            "source_paths": source_list("222_doc", "235_doc", "678_bx_gate"),
            "generated_utc": now,
        },
        {
            "candidate_id": "CSS679_1_P_constitutive_owner_223",
            "target_factor": "B_X_boundary_momentum",
            "candidate_value": "P^{mu nu}=partial V_def(Y,Z)/partial Z_{mu nu}",
            "what_is_real": "clean composite P[Y] ownership contract exists",
            "missing_for_claim": "V_def;Z_{mu nu};parent metric M_AB;cross-term policy;constraint algebra closure",
            "gate_status": "promising_but_not_claim_ready",
            "claim_ready": "false",
            "source_paths": source_list("223_doc", "222_doc", "235_doc"),
            "generated_utc": now,
        },
        {
            "candidate_id": "CSS679_2_BX_residual_vector_671",
            "target_factor": "B_X_boundary_momentum",
            "candidate_value": "B_X^nu=n_mu P^{mu nu}+B_ct^nu",
            "what_is_real": "edge residual vector names the exact missing factor and feeds Q_edge",
            "missing_for_claim": "MISSING_BOUNDARY_OWNER;MISSING_UNITS;source_status symbolic",
            "gate_status": "blocked_template",
            "claim_ready": "false",
            "source_paths": source_list("671_edge", "672_source_plan", "674_requirements"),
            "generated_utc": now,
        },
        {
            "candidate_id": "CSS679_3_Bedge_theorem_zero_677_678",
            "target_factor": "B_edge_exact_zero",
            "candidate_value": "Q_edge=0 if exact boundary class/nohair/projector stack passes",
            "what_is_real": "conditional Stokes/cohomology theorem route is mathematically clean",
            "missing_for_claim": "boundary primitive;relative class;proper-charge guard;nohair;projector stress/domain lock;matter blindness",
            "gate_status": "theorem_zero_unsigned",
            "claim_ready": "false",
            "source_paths": source_list("677_bedge", "678_silence", "678_bx_gate"),
            "generated_utc": now,
        },
        {
            "candidate_id": "CSS679_4_Qbar_requirement_673_674",
            "target_factor": "Qbar_edge_XH(lambda)",
            "candidate_value": "Pi_M^H[Q_edge^H(lambda)]/M_H_ref",
            "what_is_real": "definition and required source fields are explicit",
            "missing_for_claim": "Q_edge numerator;M_H_ref denominator;same-frame convention;fixed reference;lambda support",
            "gate_status": "fails_BXG678_3",
            "claim_ready": "false",
            "source_paths": source_list("673_acquisition", "673_pim_audit", "674_requirements", "678_bx_gate"),
            "generated_utc": now,
        },
        {
            "candidate_id": "CSS679_5_M_H_ref_denominator",
            "target_factor": "M_H_ref",
            "candidate_value": "positive Hamiltonian/source mass denominator",
            "what_is_real": "denominator role is isolated in prior Hamiltonian/source-measure contracts",
            "missing_for_claim": "same-frame GM_orbit=G*M_H_ref certificate;fixed reference branch;positive measured source mass row for current branch",
            "gate_status": "denominator_unfilled",
            "claim_ready": "false",
            "source_paths": source_list("boundary_reference_status", "hamiltonian_source_contract", "673_acquisition", "674_requirements"),
            "generated_utc": now,
        },
        {
            "candidate_id": "CSS679_6_fill_pack_current_row",
            "target_factor": "first_edge_factor_row",
            "candidate_value": "EFR674_0_current_edge_branch_template",
            "what_is_real": "single row already contains every edge factor slot and alpha formula",
            "missing_for_claim": "lambda,K_edge,Qbar_edge_XH,qbar_XT,B_X,M_H_ref all missing or unsigned",
            "gate_status": "template_only",
            "claim_ready": "false",
            "source_paths": source_list("674_fill_pack", "675_scout", "675_blockers"),
            "generated_utc": now,
        },
    ]


def claim_ready_evaluation_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "eval_id": "CRE679_0_BX_claim_ready_gate",
            "target_factor": "B_X_boundary_momentum",
            "required": "value_or_theorem_zero;units;lambda_or_shell;boundary_class;counterterm_convention;source_path;equation_ref;derivation_status",
            "best_candidate": "CSS679_0_BX_formula_222_235 plus CSS679_1_P_constitutive_owner_223",
            "passes": "false",
            "fail_reasons": "formula exists but parent P owner, units, counterterm, boundary class, and exact/proper status are not all signed",
            "repair": "derive P[Y] constitutive owner and boundary primitive, or source B_X normalization/current representative",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "eval_id": "CRE679_1_Qbar_claim_ready_gate",
            "target_factor": "Qbar_edge_XH(lambda)",
            "required": "Pi_M_projection;Q_edge_numerator;M_H_ref;lambda;units;source_path;frame_convention",
            "best_candidate": "CSS679_4_Qbar_requirement_673_674",
            "passes": "false",
            "fail_reasons": "Qbar definition exists but numerator, denominator, lambda support, and same-frame reference are missing",
            "repair": "derive Pi_M^H[Q_edge]=0 or source numerator/denominator in the same Hamiltonian frame",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "eval_id": "CRE679_2_theorem_zero_gate",
            "target_factor": "B_edge_exact_zero",
            "required": "exact boundary primitive;trivial relative class;proper-charge guard;nohair;projector silence;matter blindness",
            "best_candidate": "CSS679_3_Bedge_theorem_zero_677_678",
            "passes": "false",
            "fail_reasons": "conditional theorem stack is clean but unsigned",
            "repair": "new parent boundary action/constraint algebra input, not another ledger-only pass",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "eval_id": "CRE679_3_first_row_available",
            "target_factor": "first claim-ready edge factor row",
            "required": "at least one of B_X,Qbar_edge_XH,B_edge_zero passes its gate",
            "best_candidate": "none",
            "passes": "false",
            "fail_reasons": "claim_ready_candidates=0",
            "repair": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def acquisition_ledger_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "acquisition_id": "AL679_0_best_next_BX_parent_owner",
            "target": "B_X_boundary_momentum",
            "route": "derive parent P constitutive owner",
            "needed_artifact": "P^{mu nu}=partial V_def(Y,Z)/partial Z_{mu nu};B_X^nu=n_mu P^{mu nu}+B_ct^nu;B_ct convention;compact shell;units",
            "why_first": "this is upstream of Q_edge and may either define or kill the edge charge",
            "current_status": "promising_but_unfilled",
            "valid_for_claim": "false",
            "source_paths": source_list("223_doc", "222_doc", "235_doc", "678_bx_gate"),
            "generated_utc": now,
        },
        {
            "acquisition_id": "AL679_1_parallel_Qbar_denominator",
            "target": "Qbar_edge_XH(lambda)",
            "route": "source Hamiltonian projection numerator/denominator",
            "needed_artifact": "Q_edge numerator;M_H_ref;lambda;units;fixed reference;same-frame convention",
            "why_first": "if B_X remains live, Qbar is the measurable mass-projection factor",
            "current_status": "unfilled",
            "valid_for_claim": "false",
            "source_paths": source_list("673_acquisition", "673_pim_audit", "674_requirements", "boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "acquisition_id": "AL679_2_rejected_shortcut",
            "target": "use B_X formula as claim row",
            "route": "promote formula-only B_X",
            "needed_artifact": "not allowed",
            "why_first": "would smuggle normalization, boundary class, counterterm, and nohair conditions",
            "current_status": "rejected",
            "valid_for_claim": "false",
            "source_paths": source_list("222_doc", "235_doc", "678_bx_gate"),
            "generated_utc": now,
        },
        {
            "acquisition_id": "AL679_3_data_guard",
            "target": "R10 comparator",
            "route": "run after first theory row",
            "needed_artifact": "one claim-ready theory factor plus promoted bound curve",
            "why_first": "otherwise data run only tests placeholders",
            "current_status": "blocked",
            "valid_for_claim": "false",
            "source_paths": source_list("674_fill_pack", "675_blockers", "678_fork"),
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D679_0_first_claim_ready_row",
            "target": "B_X or Qbar claim-ready row",
            "result": "not_found",
            "reason": "local corpus contains formula/definition/contract rows but no row with complete units, boundary/frame convention, source path, and signed derivation status",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D679_1_best_route",
            "target": "choose next hinge",
            "result": "derive_P_owner_first",
            "reason": "223 is the only route that can turn B_X from symbolic boundary momentum into a parent-owned source row",
            "next_action": "derive P constitutive owner or fall back to Qbar numerator/denominator sourcing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D679_2_claim_guard",
            "target": "local/R10 evidence",
            "result": "blocked",
            "reason": "claim-ready edge factor count is zero",
            "next_action": "no R10 comparator evidence run until a theory row exists",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def evaluator_rows(
    scout_rows: list[dict[str, str]],
    claim_eval_rows: list[dict[str, str]],
    acquisition_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    claim_ready_count = sum(1 for row in scout_rows if row["claim_ready"] == "true")
    passing_evals = sum(1 for row in claim_eval_rows if row["passes"] == "true")
    selected_next = any(row["next_action"] == NEXT_TARGET for row in decision)
    return [
        {
            "evaluator_id": "EV679_0_local_source_scout",
            "target": "find local claim-ready B_X/Qbar row",
            "status": "fail_nonclaim",
            "reason": f"claim_ready_candidates={claim_ready_count}; candidates_scanned={len(scout_rows)}",
            "claim_effect": "no source row promoted",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV679_1_gate_evaluation",
            "target": "apply 678 gate to best candidates",
            "status": "fail_nonclaim",
            "reason": f"passing_evals={passing_evals}; B_X and Qbar both fail their gates",
            "claim_effect": "alpha_edge remains blocked",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV679_2_acquisition_ledger",
            "target": "write next actionable source/derivation plan",
            "status": "pass_nonclaim",
            "reason": f"acquisition_rows={len(acquisition_rows)}; best route is P-owner before comparator",
            "claim_effect": "next private checkpoint only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV679_3_next_target",
            "target": "select next hinge",
            "status": "selected_nonclaim",
            "reason": f"next_selected={bool_text(selected_next)}",
            "claim_effect": "no R10/R11/PPN/local-GR claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "NCS679_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "no first claim-ready B_X or Qbar row found; P constitutive owner is the best next derivation hinge",
            "blocked_claims": "B_X_claim_row;Qbar_edge_XH_claim_row;Bedge_theorem_zero;alpha_edge;R10;R11;PPN;clock;orbital;local_GR",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    source_register: list[dict[str, str]],
    scout_rows: list[dict[str, str]],
    claim_eval_rows: list[dict[str, str]],
    acquisition_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    missing_sources = [row["source_id"] for row in source_register if row["exists"] != "true"]
    rows.append({"check_id": "V679_0_source_paths_exist", "result": "pass" if not missing_sources else "fail", "detail": "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources), "generated_utc": now})

    validation_ids = ["667_validation", "668_validation", "670_validation", "671_validation", "672_validation", "673_validation", "674_validation", "675_validation", "676_validation", "677_validation", "678_validation"]
    prior_failures = {source_id: len(validation_failures_for(source_id)) for source_id in validation_ids}
    rows.append({"check_id": "V679_1_prior_validations_clean", "result": "pass" if all(count == 0 for count in prior_failures.values()) else "fail", "detail": ";".join(f"{source_id}={count}" for source_id, count in prior_failures.items()), "generated_utc": now})

    rows.append({"check_id": "V679_2_candidate_scout_coverage", "result": "pass" if len(scout_rows) >= 7 else "fail", "detail": f"candidate_rows={len(scout_rows)}", "generated_utc": now})

    claim_ready_count = sum(1 for row in scout_rows if row["claim_ready"] == "true")
    rows.append({"check_id": "V679_3_no_claim_ready_candidates", "result": "pass" if claim_ready_count == 0 else "fail", "detail": f"claim_ready_candidates={claim_ready_count}", "generated_utc": now})

    passing_evals = sum(1 for row in claim_eval_rows if row["passes"] == "true")
    rows.append({"check_id": "V679_4_gate_evaluations_fail_honestly", "result": "pass" if len(claim_eval_rows) >= 4 and passing_evals == 0 else "fail", "detail": f"claim_eval_rows={len(claim_eval_rows)};passing={passing_evals}", "generated_utc": now})

    rows.append({"check_id": "V679_5_acquisition_ledger_written", "result": "pass" if len(acquisition_rows) >= 4 else "fail", "detail": f"acquisition_rows={len(acquisition_rows)}", "generated_utc": now})

    generated = scout_rows + claim_eval_rows + acquisition_rows + evaluator + decision
    claim_rows = [row for row in generated if row.get("valid_for_claim") == "true"]
    rows.append({"check_id": "V679_6_no_claim_rows_promoted", "result": "pass" if not claim_rows else "fail", "detail": "all generated 679 rows remain valid_for_claim=false" if not claim_rows else f"claim_rows={len(claim_rows)}", "generated_utc": now})

    rows.append({"check_id": "V679_7_next_target_selected", "result": "pass" if any(row["next_action"] == NEXT_TARGET for row in decision) else "fail", "detail": NEXT_TARGET, "generated_utc": now})

    output_paths = [
        RESIDUALS / "P8_Y5_R10_679_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_679_CANDIDATE_SOURCE_SCOUT.csv",
        RESIDUALS / "P8_Y5_R10_679_CLAIM_READY_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_679_ACQUISITION_LEDGER.csv",
        RESIDUALS / "P8_Y5_R10_679_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_679_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_679_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_679_VALIDATION.csv",
        DOC_PATH,
    ]
    rows.append({"check_id": "V679_8_generated_outputs_scoped", "result": "pass" if all(str(path).startswith(str(ROOT)) for path in output_paths) else "fail", "detail": "all 679 outputs target post-checkpoint-work", "generated_utc": now})

    changed_count = formalization_changed_count()
    rows.append({"check_id": "V679_9_formalization_workbench_untouched", "result": "pass" if changed_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed_count}", "generated_utc": now})

    rows.append({"check_id": "V679_10_status_nonclaim", "result": "pass" if "no_BX_promotion" in CLAIM_CEILING and "no_Qbar_promotion" in CLAIM_CEILING and "no_local_GR" in CLAIM_CEILING else "fail", "detail": CLAIM_CEILING, "generated_utc": now})

    missing_language_rows = [row for row in scout_rows + claim_eval_rows if "missing" in ";".join(str(value).lower() for value in row.values())]
    rows.append({"check_id": "V679_11_missing_inputs_block_claims", "result": "pass" if missing_language_rows and not claim_rows else "fail", "detail": f"missing_language_rows={len(missing_language_rows)};claim_rows={len(claim_rows)}", "generated_utc": now})

    data_guard = [row for row in acquisition_rows if row["target"] == "R10 comparator" and row["current_status"] == "blocked"]
    rows.append({"check_id": "V679_12_data_guard_retained", "result": "pass" if data_guard else "fail", "detail": "R10 comparator remains blocked until theory factor row exists", "generated_utc": now})

    return rows


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_register: list[dict[str, str]],
    scout_rows: list[dict[str, str]],
    claim_eval_rows: list[dict[str, str]],
    acquisition_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 679 - Y5 R10 First Claim-Ready BX Or Qbar Source Row Acquisition

## Verdict

679 hunted for the first claim-ready `B_X_boundary_momentum` or `Qbar_edge_XH(lambda)` row and did **not** find one.

The important nuance: this is not empty failure. The corpus has a real candidate chain:

```text
B_X^nu = n_mu P^{{mu nu}}
P^{{mu nu}} = partial V_def(Y,Z) / partial Z_mu_nu
Qbar_edge_XH(lambda) = Pi_M^H[Q_edge^H(lambda)] / M_H_ref
```

But none of those are yet a claim row. `B_X` lacks a parent-owned `P[Y]` derivation, counterterm convention, compact-shell boundary class, and units. `Qbar_edge_XH` lacks the edge numerator, positive same-frame `M_H_ref`, fixed reference, and lambda/support convention. So the first source row remains nonclaim.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_register, ["source_id", "source_path", "exists", "role"])}

## Candidate Source Scout

{markdown_table(scout_rows, ["candidate_id", "target_factor", "candidate_value", "what_is_real", "missing_for_claim", "gate_status", "claim_ready"])}

## Claim Ready Evaluation

{markdown_table(claim_eval_rows, ["eval_id", "target_factor", "required", "best_candidate", "passes", "fail_reasons", "repair", "valid_for_claim"])}

## Acquisition Ledger

{markdown_table(acquisition_rows, ["acquisition_id", "target", "route", "needed_artifact", "why_first", "current_status", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Next Target

`{NEXT_TARGET}`

Default next route: derive the `P[Y]` constitutive owner first, because it is the shortest honest path from symbolic `B_X` to a source-ready boundary momentum. If that fails, source the `Qbar_edge_XH` numerator/denominator directly.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_register = source_register_rows()
    scout_rows = candidate_source_scout_rows()
    claim_eval_rows = claim_ready_evaluation_rows()
    acquisition_rows = acquisition_ledger_rows()
    decision = decision_rows()
    evaluator = evaluator_rows(scout_rows, claim_eval_rows, acquisition_rows, decision)
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_register, scout_rows, claim_eval_rows, acquisition_rows, evaluator, decision)

    write_csv(RESIDUALS / "P8_Y5_R10_679_SOURCE_REGISTER.csv", source_register, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_679_CANDIDATE_SOURCE_SCOUT.csv", scout_rows, ["candidate_id", "target_factor", "candidate_value", "what_is_real", "missing_for_claim", "gate_status", "claim_ready", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_679_CLAIM_READY_EVALUATION.csv", claim_eval_rows, ["eval_id", "target_factor", "required", "best_candidate", "passes", "fail_reasons", "repair", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_679_ACQUISITION_LEDGER.csv", acquisition_rows, ["acquisition_id", "target", "route", "needed_artifact", "why_first", "current_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_679_EVALUATOR.csv", evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_679_DECISION.csv", decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_679_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "blocked_claims", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_679_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_register, scout_rows, claim_eval_rows, acquisition_rows, evaluator, decision, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"candidate_rows={len(scout_rows)}")
    print(f"claim_ready_candidates={sum(1 for row in scout_rows if row['claim_ready'] == 'true')}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
