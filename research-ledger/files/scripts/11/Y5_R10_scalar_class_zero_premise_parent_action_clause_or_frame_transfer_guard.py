from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_scalar_class_descent_clause_and_frame_guard_written_conditional_nonclaim"
CLAIM_CEILING = "descent_clause_template_only_not_parent_signed_no_delta_AEH_scalar_zero_no_scalar_charge_zero_no_R10_PPN_WEP_Gdot_pass_no_local_GR_claim"
NEXT_TARGET = "711-Y5-R10-derive-descent-clause-from-quotient-geometry-or-demote-scalar-zero-to-closure.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "710-Y5-R10-scalar-class-zero-premise-parent-action-clause-or-frame-transfer-guard.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

OUTPUT_PATHS = [
    DOC_PATH,
    RESIDUALS / "P8_Y5_R10_710_SOURCE_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_710_DESCENT_PARENT_ACTION_CLAUSE.csv",
    RESIDUALS / "P8_Y5_R10_710_ZERO_PREMISE_CLAUSE_MAP.csv",
    RESIDUALS / "P8_Y5_R10_710_FRAME_TRANSFER_GUARD.csv",
    RESIDUALS / "P8_Y5_R10_710_CONDITIONAL_DERIVATION.csv",
    RESIDUALS / "P8_Y5_R10_710_COUNTEREXAMPLE_LEDGER.csv",
    RESIDUALS / "P8_Y5_R10_710_AEH_SCALAR_UPDATE.csv",
    RESIDUALS / "P8_Y5_R10_710_CLAIM_GATE_EVALUATION.csv",
    RESIDUALS / "P8_Y5_R10_710_DECISION.csv",
    RESIDUALS / "P8_Y5_R10_710_NONCLAIM_SUMMARY.csv",
    RESIDUALS / "P8_Y5_BRR545_710_VALIDATION.csv",
]

SOURCE_PATHS = {
    "440_doc": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "704_doc": ROOT / "704-Y5-R10-EH-prefactor-constant-theorem-or-kappa-gradient-bound.md",
    "705_doc": ROOT / "705-Y5-R10-AEH-prefactor-source-row-or-no-FchiR-theorem.md",
    "706_doc": ROOT / "706-Y5-R10-parent-action-term-inventory-for-AEH-source-row.md",
    "707_doc": ROOT / "707-Y5-R10-scalar-class-FR-prefactor-zero-or-AEH-bound.md",
    "708_doc": ROOT / "708-Y5-R10-scalar-class-source-row-or-R11-R10-bound-map.md",
    "709_doc": ROOT / "709-Y5-R10-scalar-class-parent-coefficient-hunt-or-zero-premise.md",
    "709_validation": RESIDUALS / "P8_Y5_BRR545_709_VALIDATION.csv",
    "709_hunt": RESIDUALS / "P8_Y5_R10_709_PARENT_COEFFICIENT_HUNT_LEDGER.csv",
    "709_zero": RESIDUALS / "P8_Y5_R10_709_ZERO_PREMISE_AUDIT.csv",
    "709_closure": RESIDUALS / "P8_Y5_R10_709_CLOSURE_BRANCH_CONTRACT.csv",
    "708_contract": RESIDUALS / "P8_Y5_R10_708_SCALAR_CLASS_SOURCE_ROW_CONTRACT.csv",
    "708_expansion": RESIDUALS / "P8_Y5_R10_708_LOCAL_EXPANSION_MAP.csv",
    "707_zero": RESIDUALS / "P8_Y5_R10_707_SCALAR_CLASS_ZERO_THEOREM_AUDIT.csv",
    "706_inventory": RESIDUALS / "P8_Y5_R10_706_AEH_TERM_INVENTORY.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


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


def validation_failures(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "missing", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate.is_file() and datetime.fromtimestamp(candidate.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    generated = now()
    roles = {
        "440_doc": "metric-only/scalar retained sector warning",
        "655_doc": "R11 scalar fallback warning",
        "704_doc": "A_EH prefactor bottleneck",
        "705_doc": "no-FchiR theorem audit source",
        "706_doc": "A_EH term inventory source",
        "707_doc": "scalar/class zero theorem predecessor",
        "708_doc": "scalar/class coefficient map predecessor",
        "709_doc": "parent coefficient hunt predecessor",
        "709_validation": "709 validation gate",
        "709_hunt": "709 missing coefficient ledger",
        "709_zero": "709 zero-premise clauses",
        "709_closure": "709 closure-only guard",
        "708_contract": "required scalar coefficient source row",
        "708_expansion": "local scalar expansion map",
        "707_zero": "scalar zero theorem audit",
        "706_inventory": "A_EH scalar/class inventory row",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": "true" if path.exists() else "false",
            "role": roles[source_id],
            "generated_utc": generated,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def descent_clause_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "DPC710_0_field_split",
            "parent field split",
            "Phi_parent = (g_obs, psi_matter, auxiliary); scalar/class labels sigma are quotient/readout labels, not local spacetime fields in the exterior variational algebra",
            "candidate_clause_not_parent_signed",
            "owns ZP709_1 if derived",
        ),
        (
            "DPC710_1_action_descent",
            "local action descends",
            "S_parent|local = S_EH[g_obs;G_ref] + S_matter[g_obs,psi] + S_top[sigma] with delta_g S_top = delta_psi S_top = 0",
            "candidate_clause_not_parent_signed",
            "kills local scalar/class stress if derived",
        ),
        (
            "DPC710_2_no_R_prefactor",
            "no scalar/class EH prefactor",
            "coefficient of R[g_obs] is exactly one and independent of sigma: partial_sigma A_EH = 0 and A_EH=1 in the observed frame",
            "candidate_clause_not_parent_signed",
            "would imply delta_AEH_scalar=0 and grad ln A_EH=0",
        ),
        (
            "DPC710_3_matter_functor_blind",
            "matter is scalar/class blind",
            "S_matter uses g_obs only; B_A(sigma)=constant universal and partial_sigma ln m_A = 0 for all source/test species",
            "candidate_clause_not_parent_signed",
            "would imply q_Aa=0 and WEP/R10 silence",
        ),
        (
            "DPC710_4_no_local_kinetic_mode",
            "no propagating scalar/class mode",
            "there is no Z_IJ grad sigma grad sigma term in the exterior local action, or it is pure gauge/topological and cannot source a canonical mode",
            "candidate_clause_not_parent_signed",
            "would remove the need for scalar mass/range rows",
        ),
        (
            "DPC710_5_projection_silence",
            "projection and quotient do not create stress",
            "quotient projection has no Jacobian/counterterm/boundary correction that shifts A_EH, source mass, or local stress",
            "candidate_clause_not_parent_signed",
            "blocks hidden boundary/projection leakage",
        ),
        (
            "DPC710_6_same_frame",
            "observed-frame identity",
            "g_obs is the metric used by both EH and matter terms; no Weyl/disformal transform is used to hide a variable prefactor",
            "candidate_clause_not_parent_signed",
            "core frame-transfer guard",
        ),
        (
            "DPC710_7_Ward_owner",
            "Ward/Bianchi owner",
            "any discarded scalar/class term is either topological with zero metric variation or retained in R11; nothing is dropped without a divergence owner",
            "candidate_clause_not_parent_signed",
            "prevents conservation smuggling",
        ),
        (
            "DPC710_8_conditional_theorem",
            "descent-zero theorem",
            "DPC710_0 through DPC710_7 imply delta_AEH_scalar=0, grad ln A_EH=0, q_Aa=0, alpha(lambda)=0, and no scalar PPN/Gdot/WEP residual",
            "proved_as_conditional_template",
            "useful theorem shape but not a current claim",
        ),
        (
            "DPC710_9_verdict",
            "claim-ready descent clause",
            "parent corpus derives DPC710_0 through DPC710_7 from deeper quotient geometry rather than asserting them",
            "fail_current_corpus",
            "descent clause is not yet parent-owned",
        ),
    ]
    return [
        {
            "clause_id": clause_id,
            "clause": clause,
            "mathematical_statement": statement,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("709_doc", "709_zero", "709_hunt", "708_contract", "708_expansion"),
            "generated_utc": generated,
        }
        for clause_id, clause, statement, status, effect in rows
    ]


def zero_premise_clause_map_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("ZCM710_0_ZP709_1", "ZP709_1_no_local_field", "DPC710_0_field_split;DPC710_4_no_local_kinetic_mode", "candidate_not_parent_signed", "absence not yet claimable"),
        ("ZCM710_1_ZP709_2", "ZP709_2_no_prefactor", "DPC710_1_action_descent;DPC710_2_no_R_prefactor", "candidate_not_parent_signed", "delta_AEH_scalar zero not yet claimable"),
        ("ZCM710_2_ZP709_3", "ZP709_3_constant_universal", "DPC710_0_field_split;DPC710_2_no_R_prefactor;DPC710_3_matter_functor_blind", "candidate_not_parent_signed", "constant offset guard not yet earned"),
        ("ZCM710_3_ZP709_4", "ZP709_4_no_kinetic_or_massive_decoupled", "DPC710_4_no_local_kinetic_mode", "candidate_not_parent_signed", "R10 silence not yet earned"),
        ("ZCM710_4_ZP709_5", "ZP709_5_matter_blind", "DPC710_3_matter_functor_blind", "candidate_not_parent_signed", "source charge zero not yet earned"),
        ("ZCM710_5_ZP709_6", "ZP709_6_no_frame_transfer", "DPC710_6_same_frame;DPC710_7_Ward_owner", "candidate_not_parent_signed", "frame guard not yet earned"),
        ("ZCM710_6_ZP709_7", "ZP709_7_boundary_projection_silence", "DPC710_5_projection_silence;DPC710_7_Ward_owner", "candidate_not_parent_signed", "boundary/projection silence not yet earned"),
        ("ZCM710_7_ZP709_8", "ZP709_8_conditional_theorem", "DPC710_8_conditional_theorem", "conditional_template_only", "theorem shape only"),
        ("ZCM710_8_verdict", "all ZP709 clauses", "DPC710_0..DPC710_7", "fail_current_corpus", "no zero-premise promotion"),
    ]
    return [
        {
            "map_id": map_id,
            "zp709_clause": zp_clause,
            "dpc710_owner_clause": owner,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("709_zero", "709_closure"),
            "generated_utc": generated,
        }
        for map_id, zp_clause, owner, status, effect in rows
    ]


def frame_transfer_guard_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "FTG710_0_same_metric",
            "same metric in EH and matter",
            "g_matter = g_obs, not Omega^2(sigma) g_obs and not g_obs + D(sigma) partial sigma partial sigma",
            "candidate_not_parent_signed",
            "prevents hiding A_EH variation in matter",
        ),
        (
            "FTG710_1_no_species_BA",
            "no species-dependent conformal factor",
            "B_A(sigma)=B0 constant for all A, with B0 absorbed only by an independent unit convention",
            "candidate_not_parent_signed",
            "prevents WEP/source-charge leak",
        ),
        (
            "FTG710_2_clock_guard",
            "clock/readout independence",
            "atomic, clock, EM, and mass readouts do not depend on sigma after local projection",
            "candidate_not_parent_signed",
            "prevents apparent PPN/Gdot pass with hidden clock drift",
        ),
        (
            "FTG710_3_Gref_guard",
            "independent G_ref",
            "G_ref is not fitted by absorbing A_EH(sigma); measured GM and source normalization are separately audited",
            "candidate_not_parent_signed",
            "prevents circular calibration",
        ),
        (
            "FTG710_4_Ward_guard",
            "stress exchange accounted",
            "if a frame redefinition is used, all induced stress/current terms are retained in R11 rather than dropped",
            "candidate_not_parent_signed",
            "prevents Bianchi/conservation leak",
        ),
        (
            "FTG710_5_verdict",
            "claim-ready frame guard",
            "FTG710_0 through FTG710_4 are parent-derived and source-cited",
            "fail_current_corpus",
            "no Einstein-frame shortcut allowed",
        ),
    ]
    return [
        {
            "guard_id": guard_id,
            "guard": guard,
            "mathematical_requirement": requirement,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("705_doc", "706_doc", "707_doc", "708_doc", "709_doc"),
            "generated_utc": generated,
        }
        for guard_id, guard, requirement, status, effect in rows
    ]


def conditional_derivation_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("CDR710_0_delta", "delta_AEH_scalar", "DPC710_2 gives A_EH=1, so delta_AEH_scalar=A_EH-1=0", "conditional_on_DPC710_parent_signature", "not_current_claim"),
        ("CDR710_1_gradient", "grad_ln_AEH_scalar", "partial_sigma A_EH=0 and no local sigma field imply grad_mu ln A_EH=0", "conditional_on_DPC710_parent_signature", "not_current_claim"),
        ("CDR710_2_source_charge", "q_Aa", "DPC710_3 gives partial_sigma ln m_A=0 and no canonical sigma modes, so q_Aa=0", "conditional_on_DPC710_parent_signature", "not_current_claim"),
        ("CDR710_3_R10", "alpha_AB(lambda)", "with q_Aa=0 or no lambda_a mode, alpha_AB(lambda)=0 for scalar/class branch", "conditional_on_DPC710_parent_signature", "not_current_claim"),
        ("CDR710_4_PPN", "gamma_minus_1;beta_minus_1", "no scalar coupling and same-frame matter leaves no scalar/class PPN residual", "conditional_on_DPC710_parent_signature", "not_current_claim"),
        ("CDR710_5_WEP_Gdot", "eta_AB;Gdot/G", "matter blindness and grad/time silence remove scalar/class WEP and Gdot channels", "conditional_on_DPC710_parent_signature", "not_current_claim"),
        ("CDR710_6_R11", "scalar_tensor_class_metric", "scalar/class R11 row can be marked derived_zero only after DPC710 clauses are source-signed", "blocked_current_corpus", "retain_R11_row"),
        ("CDR710_7_verdict", "conditional descent result", "mathematics is sufficient; parent ownership is missing", "fail_current_corpus", "no scalar zero claim"),
    ]
    return [
        {
            "derivation_id": derivation_id,
            "target": target,
            "derivation_statement": statement,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("708_expansion", "709_zero", "709_hunt"),
            "generated_utc": generated,
        }
        for derivation_id, target, statement, status, effect in rows
    ]


def counterexample_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("CE710_0_variable_prefactor", "quotient label enters F(sigma)R", "produces delta_AEH_scalar and kappa-gradient even if sigma sounds like a label", "DPC710_2_no_R_prefactor"),
        ("CE710_1_matter_frame", "Einstein-frame rewrite sets A_EH=1 but matter gets B_A(sigma)", "produces WEP/source-charge/R10 residuals", "DPC710_3_matter_functor_blind;DPC710_6_same_frame"),
        ("CE710_2_boundary_jacobian", "projection/integration creates sigma-dependent local counterterm", "shifts A_EH or measured source mass", "DPC710_5_projection_silence"),
        ("CE710_3_kinetic_mode", "sigma has kinetic term and finite mass", "creates scalar mode with lambda_a and possible alpha(lambda)", "DPC710_4_no_local_kinetic_mode"),
        ("CE710_4_clock_readout", "clock/EM/mass readout depends on sigma while gravity looks clean", "hides PPN/Gdot/local calibration drift", "FTG710_2_clock_guard"),
        ("CE710_5_Ward_drop", "scalar stress is omitted without topological proof or R11 retention", "violates conservation/Bianchi accounting", "DPC710_7_Ward_owner"),
    ]
    return [
        {
            "counterexample_id": counterexample_id,
            "failure_mode": failure_mode,
            "why_it_matters": why,
            "required_guard": guard,
            "valid_for_claim": "false",
            "source_paths": source_list("440_doc", "705_doc", "706_doc", "707_doc", "709_doc"),
            "generated_utc": generated,
        }
        for counterexample_id, failure_mode, why, guard in rows
    ]


def aeh_update_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("AEHU710_0_delta_AEH_scalar", "delta_AEH_scalar", "CONDITIONAL_ZERO_IF_DPC710_PARENT_SIGNED_ELSE_MISSING", "retained_not_reduced_after_710"),
        ("AEHU710_1_grad_ln_AEH_scalar", "grad_ln_AEH_scalar", "CONDITIONAL_ZERO_IF_DPC710_PARENT_SIGNED_ELSE_MISSING", "retained_not_reduced_after_710"),
        ("AEHU710_2_source_charge", "q_Aa", "CONDITIONAL_ZERO_IF_DPC710_PARENT_SIGNED_ELSE_MISSING", "retained_not_reduced_after_710"),
        ("AEHU710_3_R10_alpha", "alpha_AB(lambda)", "CONDITIONAL_ZERO_IF_DPC710_PARENT_SIGNED_ELSE_MISSING", "retained_not_reduced_after_710"),
        ("AEHU710_4_scalar_R11", "scalar_tensor_class_metric", "CONDITIONAL_DERIVED_ZERO_ELSE_RETAINED_UNFILLED", "retained_not_reduced_after_710"),
        ("AEHU710_5_AEH_sum", "A_EH", "MISSING_ALL_CHANNEL_VALUES_OR_ZERO_THEOREMS", "still_unfilled_after_710"),
    ]
    return [
        {
            "update_id": update_id,
            "target": target,
            "value_or_bound": value,
            "current_status": status,
            "valid_for_claim": "false",
            "source_paths": source_list("706_inventory", "708_expansion", "709_zero"),
            "generated_utc": generated,
        }
        for update_id, target, value, status in rows
    ]


def gate_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("CG710_0_sources", "all source files load", "source register exists check", "pass_structure", "allows checkpoint only"),
        ("CG710_1_prior_709", "709 validation clean", "709 validation has no failures", "pass_structure", "inherits clean predecessor"),
        ("CG710_2_clause_written", "descent parent-action clause", "candidate clause written", "pass_structure", "useful theorem target"),
        ("CG710_3_parent_signature", "parent derives DPC710 clauses", "not_parent_signed", "fail_blocked", "no scalar zero claim"),
        ("CG710_4_frame_guard", "frame-transfer guard", "candidate not parent-signed", "fail_blocked", "no Einstein-frame shortcut"),
        ("CG710_5_conditional_derivation", "delta/q/alpha zero", "conditional only", "fail_blocked", "no R10/PPN/WEP/Gdot pass"),
        ("CG710_6_R11_retention", "scalar R11 branch", "retained unless DPC710 signed", "fail_blocked", "no R11 pass"),
        ("CG710_7_local_GR", "local-GR promotion", "not reached", "fail_blocked", "no local-GR claim"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": observed,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("709_validation", "709_zero", "709_hunt", "709_closure"),
            "generated_utc": generated,
        }
        for gate_id, gate, observed, result, effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("D710_0_clause", "descent clause", "candidate_written", "sufficient parent-action clause now exists as exact theorem target", NEXT_TARGET),
        ("D710_1_signature", "parent ownership", "failed_current_corpus", "current work has not derived the descent clause from quotient geometry", NEXT_TARGET),
        ("D710_2_frame_guard", "frame transfer", "guard_written_unowned", "same-frame/matter-blind/readout guard is explicit but not parent-signed", NEXT_TARGET),
        ("D710_3_policy", "claim status", "blocked_nonclaim", "conditional zero is not a local-GR pass until DPC710 clauses are derived", NEXT_TARGET),
        ("D710_4_next", "next target", "selected", "derive descent clause from quotient geometry or demote scalar zero route to closure-only", NEXT_TARGET),
    ]
    return [
        {
            "decision_id": decision_id,
            "target": target,
            "result": result,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
        for decision_id, target, result, reason, next_action in rows
    ]


def summary_rows() -> list[dict[str, str]]:
    generated = now()
    return [
        {
            "summary_id": "S710_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "a sufficient descent parent-action clause and frame-transfer guard are written, but remain candidate clauses not derived from the parent corpus",
            "hardest_blocker": "derive that scalar/class labels are quotient/readout-only and matter-blind from deeper geometry rather than asserting a closure axiom",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def all_generated_rows(*groups: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for group in groups for row in group]


def validation_rows(source_rows, descent, zero_map, frame, derivation, counterexamples, aeh, gates, decisions, summary) -> list[dict[str, str]]:
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = len(validation_failures("709_validation"))
    descent_ids = {row["clause_id"] for row in descent}
    required_descent = {f"DPC710_{index}_{suffix}" for index, suffix in [
        (0, "field_split"),
        (1, "action_descent"),
        (2, "no_R_prefactor"),
        (3, "matter_functor_blind"),
        (4, "no_local_kinetic_mode"),
        (5, "projection_silence"),
        (6, "same_frame"),
        (7, "Ward_owner"),
        (8, "conditional_theorem"),
        (9, "verdict"),
    ]}
    descent_complete = required_descent.issubset(descent_ids)
    descent_not_promoted = any(row["clause_id"] == "DPC710_9_verdict" and row["current_status"] == "fail_current_corpus" for row in descent)
    zero_map_complete = {"ZP709_1_no_local_field", "ZP709_2_no_prefactor", "ZP709_5_matter_blind", "ZP709_6_no_frame_transfer", "ZP709_7_boundary_projection_silence"}.issubset({row["zp709_clause"] for row in zero_map})
    frame_complete = len(frame) >= 6 and any(row["guard_id"] == "FTG710_5_verdict" and row["current_status"] == "fail_current_corpus" for row in frame)
    conditional_outputs = {"delta_AEH_scalar", "grad_ln_AEH_scalar", "q_Aa", "alpha_AB(lambda)", "gamma_minus_1;beta_minus_1", "eta_AB;Gdot/G"}.issubset({row["target"] for row in derivation})
    counterexample_guard = len(counterexamples) >= 6 and all(row["valid_for_claim"] == "false" for row in counterexamples)
    aeh_conditional = all(row["valid_for_claim"] == "false" for row in aeh) and any("CONDITIONAL" in row["value_or_bound"] for row in aeh)
    gates_block = all(row["valid_for_claim"] == "false" for row in gates) and any(row["result"] == "fail_blocked" for row in gates)
    no_claim = all(row.get("valid_for_claim") != "true" for row in all_generated_rows(descent, zero_map, frame, derivation, counterexamples, aeh, gates, decisions, summary))
    next_selected = decisions[-1]["next_action"] == NEXT_TARGET and summary[0]["next_target"] == NEXT_TARGET
    scoped = all(str(path).startswith(str(ROOT)) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_count()
    checks = [
        ("V710_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V710_1_prior_709_clean", prior_failures == 0, f"709_validation_failures={prior_failures}"),
        ("V710_2_descent_clause_complete", descent_complete, f"descent_rows={len(descent)}"),
        ("V710_3_descent_not_promoted", descent_not_promoted, "DPC710_9_verdict=fail_current_corpus"),
        ("V710_4_zero_premise_map_complete", zero_map_complete, "ZP709 key clauses mapped to DPC710 owners"),
        ("V710_5_frame_guard_complete", frame_complete, f"frame_rows={len(frame)}"),
        ("V710_6_conditional_outputs_written", conditional_outputs, "delta;grad;q;alpha;PPN;WEP/Gdot conditional rows present"),
        ("V710_7_counterexamples_guarded", counterexample_guard, f"counterexamples={len(counterexamples)}"),
        ("V710_8_AEH_update_conditional_nonclaim", aeh_conditional, "AEH rows conditional/nonclaim"),
        ("V710_9_gates_block_claim", gates_block, f"gate_rows={len(gates)}"),
        ("V710_10_no_claim_rows_promoted", no_claim, "all generated rows valid_for_claim=false"),
        ("V710_11_next_target_selected", next_selected, NEXT_TARGET),
        ("V710_12_outputs_scoped", scoped, "all outputs under post-checkpoint-work"),
        ("V710_13_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V710_14_status_nonclaim", "not_parent_signed" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
    ]
    return [{"check_id": cid, "result": "pass" if ok else "fail", "detail": detail, "generated_utc": generated} for cid, ok, detail in checks]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body]) + "\n"


def write_doc(source_rows, descent, zero_map, frame, derivation, counterexamples, aeh, gates, decisions, summary, validation) -> None:
    doc = f"""# 710 - Y5 R10 Scalar Class Zero Premise Parent Action Clause Or Frame Transfer Guard

## Verdict

710 writes the exact sufficient clause that would close the scalar/class route:

```text
S_parent|local = S_EH[g_obs;G_ref] + S_matter[g_obs,psi] + S_top[sigma]
delta_g S_top = delta_psi S_top = 0
A_EH = 1
partial_sigma A_EH = 0
B_A(sigma) = constant universal
g_matter = g_obs
```

If the parent theory derives those statements from quotient geometry, the scalar/class branch goes silent: `delta_AEH_scalar=0`, `grad ln A_EH=0`, `q_Aa=0`, and the scalar/class R10/PPN/WEP/Gdot rows vanish.

But 710 does **not** claim that derivation has been achieved. The clause is a candidate theorem target, not a parent-signed result. The frame-transfer guard is also explicit: we cannot set `A_EH=1` by changing frame and then forget the induced matter/clock/source couplings.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Descent Parent Action Clause

{markdown_table(descent, ["clause_id", "clause", "current_status", "claim_effect", "valid_for_claim"])}

## Zero Premise Clause Map

{markdown_table(zero_map, ["map_id", "zp709_clause", "dpc710_owner_clause", "current_status", "claim_effect", "valid_for_claim"])}

## Frame Transfer Guard

{markdown_table(frame, ["guard_id", "guard", "current_status", "claim_effect", "valid_for_claim"])}

## Conditional Derivation

{markdown_table(derivation, ["derivation_id", "target", "current_status", "claim_effect", "valid_for_claim"])}

## Counterexample Ledger

{markdown_table(counterexamples, ["counterexample_id", "failure_mode", "why_it_matters", "required_guard", "valid_for_claim"])}

## AEH Scalar Update

{markdown_table(aeh, ["update_id", "target", "value_or_bound", "current_status", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    descent = descent_clause_rows()
    zero_map = zero_premise_clause_map_rows()
    frame = frame_transfer_guard_rows()
    derivation = conditional_derivation_rows()
    counterexamples = counterexample_rows()
    aeh = aeh_update_rows()
    gates = gate_rows()
    decisions = decision_rows()
    summary = summary_rows()
    validation = validation_rows(source_rows, descent, zero_map, frame, derivation, counterexamples, aeh, gates, decisions, summary)

    write_csv(OUTPUT_PATHS[1], source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(
        OUTPUT_PATHS[2],
        descent,
        ["clause_id", "clause", "mathematical_statement", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[3],
        zero_map,
        ["map_id", "zp709_clause", "dpc710_owner_clause", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[4],
        frame,
        ["guard_id", "guard", "mathematical_requirement", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[5],
        derivation,
        ["derivation_id", "target", "derivation_statement", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[6],
        counterexamples,
        ["counterexample_id", "failure_mode", "why_it_matters", "required_guard", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[7],
        aeh,
        ["update_id", "target", "value_or_bound", "current_status", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[8],
        gates,
        ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[9],
        decisions,
        ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[10],
        summary,
        ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(OUTPUT_PATHS[11], validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_rows, descent, zero_map, frame, derivation, counterexamples, aeh, gates, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"descent_rows={len(descent)}")
    print(f"frame_rows={len(frame)}")
    print(f"derivation_rows={len(derivation)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
