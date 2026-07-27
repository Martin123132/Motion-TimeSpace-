from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_parent_P_constitutive_owner_partial_candidate_Qbar_denominator_unfilled_nonclaim"
CLAIM_CEILING = "P_owner_contract_only_no_BX_claim_row_no_Qbar_denominator_no_alpha_edge_no_R10_no_PPN_no_local_GR_claim"
NEXT_TARGET = "681-Y5-R10-defect-potential-Z-map-or-explicit-BX-closure-demotion.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "680-Y5-R10-parent-P-constitutive-owner-or-Qbar-numeric-denominator-source.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "210_doc": ROOT / "210-GK-alphaK-parent-invariant-or-fixed-closure.md",
    "211_doc": ROOT / "211-GK-parent-metric-Ward-identity-attempt.md",
    "222_doc": ROOT / "222-parent-X-sector-degree-count-and-boundary-action.md",
    "223_doc": ROOT / "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md",
    "235_doc": ROOT / "235-projector-stress-variation-or-nohair-constraint-algebra.md",
    "667_validation": RESIDUALS / "P8_Y5_BRR545_667_VALIDATION.csv",
    "667_variation": RESIDUALS / "P8_Y5_R10_667_VARIATION_LEDGER.csv",
    "668_validation": RESIDUALS / "P8_Y5_BRR545_668_VALIDATION.csv",
    "668_boundary_lock": RESIDUALS / "P8_Y5_R10_668_BOUNDARY_CONDITION_LOCK.csv",
    "671_validation": RESIDUALS / "P8_Y5_BRR545_671_VALIDATION.csv",
    "671_edge": RESIDUALS / "P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv",
    "673_validation": RESIDUALS / "P8_Y5_BRR545_673_VALIDATION.csv",
    "673_acquisition": RESIDUALS / "P8_Y5_R10_673_EDGE_COEFFICIENT_ACQUISITION_LEDGER.csv",
    "673_pim_audit": RESIDUALS / "P8_Y5_R10_673_HAMILTONIAN_PIM_ORTHOGONALITY_PROOF_AUDIT.csv",
    "674_validation": RESIDUALS / "P8_Y5_BRR545_674_VALIDATION.csv",
    "674_requirements": RESIDUALS / "P8_Y5_R10_674_COEFFICIENT_REQUIREMENTS.csv",
    "675_validation": RESIDUALS / "P8_Y5_BRR545_675_VALIDATION.csv",
    "675_blockers": RESIDUALS / "P8_Y5_R10_675_EDGE_ROW_BLOCKER_MATRIX.csv",
    "676_validation": RESIDUALS / "P8_Y5_BRR545_676_VALIDATION.csv",
    "677_validation": RESIDUALS / "P8_Y5_BRR545_677_VALIDATION.csv",
    "677_bx": RESIDUALS / "P8_Y5_R10_677_BX_EXACTNESS_OR_SOURCE_ROW.csv",
    "678_validation": RESIDUALS / "P8_Y5_BRR545_678_VALIDATION.csv",
    "678_bx_gate": RESIDUALS / "P8_Y5_R10_678_BX_SOURCE_ROW_GATE.csv",
    "678_silence": RESIDUALS / "P8_Y5_R10_678_SILENCE_STACK_AUDIT.csv",
    "679_validation": RESIDUALS / "P8_Y5_BRR545_679_VALIDATION.csv",
    "679_scout": RESIDUALS / "P8_Y5_R10_679_CANDIDATE_SOURCE_SCOUT.csv",
    "679_eval": RESIDUALS / "P8_Y5_R10_679_CLAIM_READY_EVALUATION.csv",
    "679_acquisition": RESIDUALS / "P8_Y5_R10_679_ACQUISITION_LEDGER.csv",
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
        "210_doc": "G_K candidate invariant and parent metric missing source",
        "211_doc": "partial flow-block parent metric and Ward identity failure source",
        "222_doc": "X boundary momentum action source",
        "223_doc": "P constitutive owner contract source",
        "235_doc": "projector stress/nohair source",
        "667_validation": "667 validation gate",
        "667_variation": "boundary flux and Hamiltonian variation ledger",
        "668_validation": "668 validation gate",
        "668_boundary_lock": "boundary/projector lock rows",
        "671_validation": "671 validation gate",
        "671_edge": "edge residual vector",
        "673_validation": "673 validation gate",
        "673_acquisition": "Qbar and M_H acquisition ledger",
        "673_pim_audit": "Hamiltonian Pi_M orthogonality audit",
        "674_validation": "674 validation gate",
        "674_requirements": "coefficient requirements",
        "675_validation": "675 validation gate",
        "675_blockers": "edge blocker matrix",
        "676_validation": "676 validation gate",
        "677_validation": "677 validation gate",
        "677_bx": "BX exactness/source rows",
        "678_validation": "678 validation gate",
        "678_bx_gate": "BX source row gate",
        "678_silence": "silence stack audit",
        "679_validation": "679 validation gate",
        "679_scout": "candidate source scout",
        "679_eval": "claim-ready evaluation",
        "679_acquisition": "acquisition ledger",
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


def p_constitutive_owner_attempt_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "clause_id": "PCO680_0_reject_free_P",
            "object": "independent P^{mu nu}",
            "candidate_form": "S_X=int sqrt(-g)(P^{mu nu} nabla_mu X_nu+J_eff^nu X_nu)",
            "test": "P must not be a free tensor inserted to enforce the desired source identity",
            "current_result": "pass_rejected",
            "obstruction": "free P moves the hand insertion rather than deriving it",
            "if_passes": "only composite P[Y] route remains",
            "valid_for_claim": "false",
            "source_paths": source_list("223_doc"),
            "generated_utc": now,
        },
        {
            "clause_id": "PCO680_1_composite_P_contract",
            "object": "P^{mu nu}[Y]",
            "candidate_form": "P^{mu nu}=partial V_def(Y,Z)/partial Z_{mu nu}",
            "test": "P is owned by parent fields Y and a parent deformation Z, not by readout",
            "current_result": "contract_identified",
            "obstruction": "V_def and Z_{mu nu} are not derived from the corpus yet",
            "if_passes": "B_X becomes a derived boundary momentum candidate",
            "valid_for_claim": "false",
            "source_paths": source_list("223_doc", "210_doc", "211_doc"),
            "generated_utc": now,
        },
        {
            "clause_id": "PCO680_2_defect_potential_candidate",
            "object": "V_def",
            "candidate_form": "V_def=1/2 <Z,Z>_M + higher coherent-defect terms",
            "test": "M_AB and Z map must be derived before taking partial V_def/partial Z",
            "current_result": "partial_candidate_only",
            "obstruction": "211 derives only flow-block ownership; Weyl/J_rel/Q/cross terms remain closure",
            "if_passes": "P normalization and units can be inherited from the parent defect metric",
            "valid_for_claim": "false",
            "source_paths": source_list("210_doc", "211_doc", "223_doc"),
            "generated_utc": now,
        },
        {
            "clause_id": "PCO680_3_trace_traceless_split",
            "object": "Gamma_eff and Khat",
            "candidate_form": "Gamma_eff=-1/4 tr(P); Khat^{mu nu}=P^{mu nu}+Gamma_eff g^{mu nu}",
            "test": "four-dimensional trace split makes Khat trace-free and Gamma_eff the scalar trace response",
            "current_result": "conditional_pass_if_P_owned",
            "obstruction": "split is algebraic but inherits every missing P-owner input",
            "if_passes": "Gamma/Khat stop being separate knobs once P is parent-owned",
            "valid_for_claim": "false",
            "source_paths": source_list("223_doc", "222_doc"),
            "generated_utc": now,
        },
        {
            "clause_id": "PCO680_4_constraint_algebra",
            "object": "X multiplier constraints",
            "candidate_form": "pi_X^nu approx 0; C_X^nu=-nabla_mu P[Y]^{mu nu}+J_eff[Y]^nu approx 0",
            "test": "{C_X^nu(x),C_X^rho(y)} closes on parent constraints",
            "current_result": "not_derived",
            "obstruction": "parent Y symplectic structure and full M_AB are not specified",
            "if_passes": "X contributes zero local propagating degrees",
            "valid_for_claim": "false",
            "source_paths": source_list("223_doc", "211_doc"),
            "generated_utc": now,
        },
        {
            "clause_id": "PCO680_5_boundary_momentum_row",
            "object": "B_X^nu",
            "candidate_form": "B_X^nu=n_mu P[Y]^{mu nu}+B_ct^nu",
            "test": "normalization, units, counterterm, compact shell, and boundary class are fixed before R10 scoring",
            "current_result": "not_claim_ready",
            "obstruction": "P owner partial only; B_ct and C_top remain unsigned",
            "if_passes": "first B_X source row can be promoted",
            "valid_for_claim": "false",
            "source_paths": source_list("222_doc", "235_doc", "671_edge", "678_bx_gate", "679_scout"),
            "generated_utc": now,
        },
        {
            "clause_id": "PCO680_6_verdict",
            "object": "parent P constitutive owner",
            "candidate_form": "P=dV_def/dZ with closed constraint algebra and boundary current",
            "test": "all PCO680 clauses pass together",
            "current_result": "partial_candidate_not_claim",
            "obstruction": "V_def, Z map, full M_AB, cross terms, constraint algebra, and B_ct remain missing",
            "if_passes": "B_X can become a real source/theorem-zero row",
            "valid_for_claim": "false",
            "source_paths": source_list("210_doc", "211_doc", "222_doc", "223_doc", "235_doc", "679_acquisition"),
            "generated_utc": now,
        },
    ]


def bx_claim_row_candidate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "row_id": "BXC680_0_candidate_not_promoted",
            "factor": "B_X_boundary_momentum",
            "value_or_theorem_zero": "B_X^nu=n_mu partial V_def(Y,Z)/partial Z_{mu nu}+B_ct^nu",
            "units": "MISSING_PARENT_DEFECT_METRIC_UNITS",
            "lambda_or_shell": "MISSING_COMPACT_LOCAL_SHELL",
            "boundary_class": "MISSING_PARENT_FIXED_C_TOP",
            "counterterm_convention": "MISSING_B_ct",
            "source_path": source_list("222_doc", "223_doc", "235_doc"),
            "equation_ref": "222 lines 152-169; 223 lines 163-172; 235 line 137",
            "derivation_status": "partial_candidate_not_claim_ready",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "BXC680_1_theorem_zero_not_promoted",
            "factor": "B_edge_exact_zero",
            "value_or_theorem_zero": "false",
            "units": "theorem_zero_condition",
            "lambda_or_shell": "inactive_only_if_silence_stack_signed",
            "boundary_class": "conditional_trivial_H_rel_not_signed",
            "counterterm_convention": "proper_charge_guard_missing",
            "source_path": source_list("677_bx", "678_silence"),
            "equation_ref": "677/678 conditional Stokes-cohomology stack",
            "derivation_status": "theorem_zero_unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def qbar_denominator_source_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "QDG680_0_Qedge_numerator",
            "target": "Q_edge^H(lambda)",
            "needed_input": "boundary current integral from B_X on a fixed shell/domain",
            "current_status": "missing_until_BX_owned_or_sourced",
            "claim_promotable_if": "B_X row passes or exact boundary zero theorem passes",
            "fallback": "source Q_edge numerator directly from Hamiltonian boundary current",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "673_acquisition", "678_bx_gate"),
            "generated_utc": now,
        },
        {
            "gate_id": "QDG680_1_MH_denominator",
            "target": "M_H_ref",
            "needed_input": "positive same-frame Hamiltonian/source mass tied to observed GM",
            "current_status": "missing_for_current_branch",
            "claim_promotable_if": "fixed reference and GM_orbit=G*M_H_ref certificate exists",
            "fallback": "source measured denominator row with explicit frame/reference",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "hamiltonian_source_contract", "673_acquisition", "674_requirements"),
            "generated_utc": now,
        },
        {
            "gate_id": "QDG680_2_same_frame_lambda",
            "target": "lambda/support convention",
            "needed_input": "same local shell/range used by Q_edge, M_H_ref, and R10 bound lookup",
            "current_status": "missing_edge_range_or_envelope",
            "claim_promotable_if": "positive length envelope with source path or theorem-zero inactive branch",
            "fallback": "source lambda_edge after B_X/Qbar numerator exists",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "675_blockers", "679_eval"),
            "generated_utc": now,
        },
        {
            "gate_id": "QDG680_3_Qbar_verdict",
            "target": "Qbar_edge_XH(lambda)",
            "needed_input": "Pi_M^H[Q_edge^H(lambda)]/M_H_ref",
            "current_status": "not_claim_ready",
            "claim_promotable_if": "Qedge numerator, M_H_ref, lambda, units, fixed reference, and same frame all pass",
            "fallback": "source numerator/denominator only after P-owner route fails",
            "valid_for_claim": "false",
            "source_paths": source_list("673_acquisition", "673_pim_audit", "674_requirements", "679_eval"),
            "generated_utc": now,
        },
    ]


def evaluator_rows(
    p_rows: list[dict[str, str]],
    bx_rows: list[dict[str, str]],
    qbar_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    p_claim = any(row["valid_for_claim"] == "true" for row in p_rows)
    bx_claim = any(row["valid_for_claim"] == "true" for row in bx_rows)
    qbar_claim = any(row["valid_for_claim"] == "true" for row in qbar_rows)
    return [
        {
            "evaluator_id": "EV680_0_P_owner_attempt",
            "target": "derive P=dV_def/dZ",
            "status": "partial_nonclaim",
            "reason": f"p_claim={bool_text(p_claim)}; contract exists but V_def/Z/full M_AB/cross terms/constraint algebra missing",
            "claim_effect": "B_X still nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV680_1_BX_row",
            "target": "promote B_X row",
            "status": "fail_nonclaim",
            "reason": f"bx_claim={bool_text(bx_claim)}; B_X candidate has MISSING units/shell/class/counterterm",
            "claim_effect": "Q_edge numerator unavailable",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV680_2_Qbar_denominator",
            "target": "source Qbar numerator/denominator",
            "status": "fail_nonclaim",
            "reason": f"qbar_claim={bool_text(qbar_claim)}; Q_edge numerator and M_H_ref denominator remain missing",
            "claim_effect": "alpha_edge remains blocked",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV680_3_claim_guardrail",
            "target": "prevent R10/local promotion",
            "status": "pass",
            "reason": "all 680 generated rows remain valid_for_claim=false",
            "claim_effect": "no R10/R11/PPN/local-GR claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D680_0_P_owner",
            "target": "parent P constitutive owner",
            "result": "partial_candidate_not_derived",
            "reason": "P=dV_def/dZ is the right contract, but V_def, Z, full M_AB, cross terms, constraint algebra, and B_ct are not parent-signed",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D680_1_Qbar_source",
            "target": "Qbar numeric denominator/source route",
            "result": "unfilled",
            "reason": "Q_edge numerator depends on B_X and M_H_ref is still missing for the current branch",
            "next_action": "keep Qbar sourcing as fallback after P-owner attempt",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D680_2_route",
            "target": "next hinge",
            "result": "construct_Z_map_or_demote_BX_to_closure",
            "reason": "the cleanest decisive move is to try one concrete Z_{mu nu}/V_def construction; if it is only named to fit B_X, demote B_X to explicit closure",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "NCS680_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "P-owner route is sharpened but not derived; Qbar denominator route remains unfilled",
            "blocked_claims": "B_X_claim_row;Qbar_edge_XH;alpha_edge;R10;R11;PPN;clock;orbital;local_GR",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    source_register: list[dict[str, str]],
    p_rows: list[dict[str, str]],
    bx_rows: list[dict[str, str]],
    qbar_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    missing_sources = [row["source_id"] for row in source_register if row["exists"] != "true"]
    rows.append({"check_id": "V680_0_source_paths_exist", "result": "pass" if not missing_sources else "fail", "detail": "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources), "generated_utc": now})

    validation_ids = ["667_validation", "668_validation", "671_validation", "673_validation", "674_validation", "675_validation", "676_validation", "677_validation", "678_validation", "679_validation"]
    prior_failures = {source_id: len(validation_failures_for(source_id)) for source_id in validation_ids}
    rows.append({"check_id": "V680_1_prior_validations_clean", "result": "pass" if all(count == 0 for count in prior_failures.values()) else "fail", "detail": ";".join(f"{source_id}={count}" for source_id, count in prior_failures.items()), "generated_utc": now})

    rows.append({"check_id": "V680_2_P_owner_attempt_coverage", "result": "pass" if len(p_rows) >= 7 else "fail", "detail": f"p_rows={len(p_rows)}", "generated_utc": now})

    verdict_rows = [row for row in p_rows if row["clause_id"] == "PCO680_6_verdict"]
    rows.append({"check_id": "V680_3_P_owner_not_promoted", "result": "pass" if verdict_rows and verdict_rows[0]["current_result"] == "partial_candidate_not_claim" and all(row["valid_for_claim"] == "false" for row in p_rows) else "fail", "detail": "P owner remains nonclaim", "generated_utc": now})

    bx_claim_rows = [row for row in bx_rows if row["valid_for_claim"] == "true"]
    rows.append({"check_id": "V680_4_BX_candidate_not_promoted", "result": "pass" if len(bx_rows) >= 2 and not bx_claim_rows else "fail", "detail": f"bx_rows={len(bx_rows)};claim_rows={len(bx_claim_rows)}", "generated_utc": now})

    qbar_claim_rows = [row for row in qbar_rows if row["valid_for_claim"] == "true"]
    rows.append({"check_id": "V680_5_Qbar_gate_unfilled", "result": "pass" if len(qbar_rows) >= 4 and not qbar_claim_rows else "fail", "detail": f"qbar_rows={len(qbar_rows)};claim_rows={len(qbar_claim_rows)}", "generated_utc": now})

    generated = p_rows + bx_rows + qbar_rows + evaluator + decision
    claim_rows = [row for row in generated if row.get("valid_for_claim") == "true"]
    rows.append({"check_id": "V680_6_no_claim_rows_promoted", "result": "pass" if not claim_rows else "fail", "detail": "all generated 680 rows remain valid_for_claim=false" if not claim_rows else f"claim_rows={len(claim_rows)}", "generated_utc": now})

    rows.append({"check_id": "V680_7_next_target_selected", "result": "pass" if any(row["next_action"] == NEXT_TARGET for row in decision) else "fail", "detail": NEXT_TARGET, "generated_utc": now})

    output_paths = [
        RESIDUALS / "P8_Y5_R10_680_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_680_P_CONSTITUTIVE_OWNER_ATTEMPT.csv",
        RESIDUALS / "P8_Y5_R10_680_BX_CLAIM_ROW_CANDIDATE.csv",
        RESIDUALS / "P8_Y5_R10_680_QBAR_DENOMINATOR_SOURCE_GATE.csv",
        RESIDUALS / "P8_Y5_R10_680_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_680_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_680_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_680_VALIDATION.csv",
        DOC_PATH,
    ]
    rows.append({"check_id": "V680_8_generated_outputs_scoped", "result": "pass" if all(str(path).startswith(str(ROOT)) for path in output_paths) else "fail", "detail": "all 680 outputs target post-checkpoint-work", "generated_utc": now})

    changed_count = formalization_changed_count()
    rows.append({"check_id": "V680_9_formalization_workbench_untouched", "result": "pass" if changed_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed_count}", "generated_utc": now})

    rows.append({"check_id": "V680_10_status_nonclaim", "result": "pass" if "no_BX_claim_row" in CLAIM_CEILING and "no_Qbar_denominator" in CLAIM_CEILING and "no_local_GR" in CLAIM_CEILING else "fail", "detail": CLAIM_CEILING, "generated_utc": now})

    missing_language_rows = [row for row in bx_rows + qbar_rows if "missing" in ";".join(str(value).lower() for value in row.values())]
    rows.append({"check_id": "V680_11_missing_inputs_block_claims", "result": "pass" if missing_language_rows and not claim_rows else "fail", "detail": f"missing_language_rows={len(missing_language_rows)};claim_rows={len(claim_rows)}", "generated_utc": now})

    return rows


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_register: list[dict[str, str]],
    p_rows: list[dict[str, str]],
    bx_rows: list[dict[str, str]],
    qbar_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 680 - Y5 R10 Parent P Constitutive Owner Or Qbar Numeric Denominator Source

## Verdict

680 gets us a sharper mathematical contract, but not a promotion.

The best route is still:

```text
P^{{mu nu}} = partial V_def(Y,Z) / partial Z_mu_nu
B_X^nu = n_mu P^{{mu nu}} + B_ct^nu
Gamma_eff = -1/4 tr(P)
Khat^{{mu nu}} = P^{{mu nu}} + Gamma_eff g^{{mu nu}}
```

That is a serious route because it would make `Gamma_eff` and `Khat` algebraic projections of one parent-owned response tensor instead of separate knobs. But it is **not yet derived**: `V_def`, `Z_mu_nu`, the full parent metric `M_AB`, cross-term policy, constraint algebra, and `B_ct` are still missing.

The fallback `Qbar_edge_XH(lambda)` route also remains unfilled because it needs both the `Q_edge` numerator and a positive same-frame `M_H_ref` denominator.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_register, ["source_id", "source_path", "exists", "role"])}

## P Constitutive Owner Attempt

{markdown_table(p_rows, ["clause_id", "object", "candidate_form", "test", "current_result", "obstruction", "if_passes", "valid_for_claim"])}

## BX Claim Row Candidate

{markdown_table(bx_rows, ["row_id", "factor", "value_or_theorem_zero", "units", "lambda_or_shell", "boundary_class", "counterterm_convention", "equation_ref", "derivation_status", "valid_for_claim"])}

## Qbar Denominator Source Gate

{markdown_table(qbar_rows, ["gate_id", "target", "needed_input", "current_status", "claim_promotable_if", "fallback", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Next Target

`{NEXT_TARGET}`

Default next route: try one concrete `Z_mu_nu` / `V_def` construction from existing coherence-defect variables. If it is merely chosen to make `B_X` work, demote `B_X` to explicit closure and use the sourced `Qbar_edge_XH` route instead.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_register = source_register_rows()
    p_rows = p_constitutive_owner_attempt_rows()
    bx_rows = bx_claim_row_candidate_rows()
    qbar_rows = qbar_denominator_source_gate_rows()
    evaluator = evaluator_rows(p_rows, bx_rows, qbar_rows)
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_register, p_rows, bx_rows, qbar_rows, evaluator, decision)

    write_csv(RESIDUALS / "P8_Y5_R10_680_SOURCE_REGISTER.csv", source_register, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_680_P_CONSTITUTIVE_OWNER_ATTEMPT.csv", p_rows, ["clause_id", "object", "candidate_form", "test", "current_result", "obstruction", "if_passes", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_680_BX_CLAIM_ROW_CANDIDATE.csv", bx_rows, ["row_id", "factor", "value_or_theorem_zero", "units", "lambda_or_shell", "boundary_class", "counterterm_convention", "source_path", "equation_ref", "derivation_status", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_680_QBAR_DENOMINATOR_SOURCE_GATE.csv", qbar_rows, ["gate_id", "target", "needed_input", "current_status", "claim_promotable_if", "fallback", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_680_EVALUATOR.csv", evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_680_DECISION.csv", decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_680_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "blocked_claims", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_680_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_register, p_rows, bx_rows, qbar_rows, evaluator, decision, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"p_rows={len(p_rows)}")
    print(f"bx_rows={len(bx_rows)}")
    print(f"qbar_rows={len(qbar_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
