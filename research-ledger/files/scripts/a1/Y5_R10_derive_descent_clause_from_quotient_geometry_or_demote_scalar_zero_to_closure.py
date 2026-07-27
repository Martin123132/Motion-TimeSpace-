from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_quotient_descent_derivation_fails_scalar_zero_demoted_to_labelled_closure_nonclaim"
CLAIM_CEILING = "scalar_zero_closure_lock_only_no_parent_descent_no_delta_AEH_zero_no_R10_PPN_WEP_Gdot_pass_no_local_GR_claim"
NEXT_TARGET = "712-Y5-R10-scalar-class-closure-lock-and-residual-test-vector.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "711-Y5-R10-derive-descent-clause-from-quotient-geometry-or-demote-scalar-zero-to-closure.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

OUTPUT_PATHS = [
    DOC_PATH,
    RESIDUALS / "P8_Y5_R10_711_SOURCE_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_711_QUOTIENT_DESCENT_DERIVATION_AUDIT.csv",
    RESIDUALS / "P8_Y5_R10_711_DPC710_OWNERSHIP_MAP.csv",
    RESIDUALS / "P8_Y5_R10_711_PRIOR_QUOTIENT_EVIDENCE_LEDGER.csv",
    RESIDUALS / "P8_Y5_R10_711_SCALAR_ZERO_DEMOTION_LEDGER.csv",
    RESIDUALS / "P8_Y5_R10_711_RETAINED_BRANCH_REQUIREMENTS.csv",
    RESIDUALS / "P8_Y5_R10_711_AEH_SCALAR_UPDATE.csv",
    RESIDUALS / "P8_Y5_R10_711_CLAIM_GATE_EVALUATION.csv",
    RESIDUALS / "P8_Y5_R10_711_DECISION.csv",
    RESIDUALS / "P8_Y5_R10_711_NONCLAIM_SUMMARY.csv",
    RESIDUALS / "P8_Y5_BRR545_711_VALIDATION.csv",
]

SOURCE_PATHS = {
    "231_doc": ROOT / "231-Jrel-cohomology-projector-or-local-EH-limit.md",
    "251_doc": ROOT / "251-N5-boundary-projector-parent-owner-or-modified-exterior-branch.md",
    "252_doc": ROOT / "252-topological-projector-parent-action-skeleton.md",
    "253_doc": ROOT / "253-FLRW-reduction-of-topological-projector-or-Bmem-stays-closure.md",
    "255_doc": ROOT / "255-memory-stress-exchange-normalization-or-kappa-mem-free.md",
    "272_doc": ROOT / "272-quotient-configuration-principle-from-topological-projector.md",
    "341_doc": ROOT / "341-indistinguishable-cell-quotient-parent-action-gate.md",
    "367_doc": ROOT / "367-topological-class-selection-or-local-GR-closure-ledger.md",
    "372_doc": ROOT / "372-local-phiC-zero-theorem-or-gradient-bound.md",
    "407_doc": ROOT / "407-primitive-relational-quotient-action-sketch.md",
    "410_doc": ROOT / "410-quotient-matter-functor-theorem-attempt.md",
    "414_doc": ROOT / "414-local-quotient-invariant-algebra-triviality-gate.md",
    "415_doc": ROOT / "415-local-trivial-class-selector-theorem-attempt.md",
    "710_doc": ROOT / "710-Y5-R10-scalar-class-zero-premise-parent-action-clause-or-frame-transfer-guard.md",
    "710_validation": RESIDUALS / "P8_Y5_BRR545_710_VALIDATION.csv",
    "710_descent": RESIDUALS / "P8_Y5_R10_710_DESCENT_PARENT_ACTION_CLAUSE.csv",
    "710_frame": RESIDUALS / "P8_Y5_R10_710_FRAME_TRANSFER_GUARD.csv",
    "710_aeh": RESIDUALS / "P8_Y5_R10_710_AEH_SCALAR_UPDATE.csv",
    "709_zero": RESIDUALS / "P8_Y5_R10_709_ZERO_PREMISE_AUDIT.csv",
    "708_r11": RESIDUALS / "P8_Y5_R10_708_R11_SCALAR_OPERATOR_ROW.csv",
    "708_r10": RESIDUALS / "P8_Y5_R10_708_R10_ALPHA_LAMBDA_SCALAR_TEMPLATE.csv",
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
        "231_doc": "relative cohomology/projector conditional gate",
        "251_doc": "topological projector parent-owner fork",
        "252_doc": "topological projector parent-action skeleton",
        "253_doc": "FLRW topological projector closure warning",
        "255_doc": "stress normalization closure warning",
        "272_doc": "quotient configuration principle conditional route",
        "341_doc": "indistinguishable-cell quotient parent-action gate",
        "367_doc": "class selection closure ledger",
        "372_doc": "local phi_C zero conditional branch",
        "407_doc": "primitive relational quotient action sketch",
        "410_doc": "quotient matter functor theorem attempt",
        "414_doc": "local quotient-invariant algebra triviality gate",
        "415_doc": "local trivial class selector attempt",
        "710_doc": "descent clause predecessor",
        "710_validation": "710 validation gate",
        "710_descent": "DPC710 descent clause rows",
        "710_frame": "DPC710 frame guard rows",
        "710_aeh": "710 scalar AEH update rows",
        "709_zero": "709 zero premise audit",
        "708_r11": "708 retained scalar R11 row",
        "708_r10": "708 scalar R10 template",
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


def quotient_descent_audit_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "QDA711_0_quotient_object",
            "parent quotient object Q exists",
            "physical local configurations are quotient classes, not labelled representatives",
            "conditional_support_not_parent_complete",
            "272/341/407 provide theorem targets, not final parent derivation",
        ),
        (
            "QDA711_1_presymplectic_null",
            "forbidden scalar/class directions are null",
            "vertical variations along scalar/class representative directions lie in ker(Omega) with vanishing boundary primitive",
            "open_burden",
            "272 leaves Cperp exactness and boundary primitive as open",
        ),
        (
            "QDA711_2_invariant_algebra_triviality",
            "local quotient-invariant algebra is only geometry plus universal constants",
            "I_loc(Q)=I_geom[g_obs,connection] plus constants; no independent scalar/class generator remains",
            "fail_current_corpus",
            "414 explicitly fails local invariant algebra triviality",
        ),
        (
            "QDA711_3_local_class_selection",
            "local selected class is trivial/silent",
            "local Q_rel=[J_rel]=0 or exact, with no boundary exchange or defect class",
            "fail_current_corpus",
            "415 and 367 demote this to fixed-class closure",
        ),
        (
            "QDA711_4_matter_functor_factorization",
            "matter factors through observed geometry only",
            "S_matter = S_matter[psi, Obs(Q)] with no marker/class/species charge dependence",
            "fail_current_corpus",
            "410 writes conditional theorem but fails parent derivation",
        ),
        (
            "QDA711_5_action_basicness",
            "local action is basic under vertical scalar/class directions",
            "i_v delta S = 0 and L_v S is boundary/topological for scalar/class vertical v",
            "not_derived",
            "topological projector analogy is insufficient for scalar/class action",
        ),
        (
            "QDA711_6_no_prefactor",
            "no A_EH(sigma)R generated by quotient reduction",
            "descent to quotient does not create scalar/class EH prefactor or counterterm",
            "not_derived",
            "710 DPC710_2 remains candidate_not_parent_signed",
        ),
        (
            "QDA711_7_frame_readout",
            "same-frame readout and matter blindness descend from quotient",
            "g_matter=g_obs and clock/EM/mass readouts are quotient-invariant without scalar/class charge",
            "not_derived",
            "410 counterexamples and 710 frame guard remain open",
        ),
        (
            "QDA711_8_topological_projector_analogy",
            "topological/projector route supports stress silence shape",
            "metric-independent relative/topological projector can have zero bulk metric variation",
            "analogy_conditional_support",
            "251/252 support a route but do not prove scalar/class descent",
        ),
        (
            "QDA711_9_verdict",
            "claim-ready quotient descent proof",
            "QDA711_0 through QDA711_7 are parent-derived with source paths",
            "fail_current_corpus",
            "scalar-zero route must be demoted to labelled closure",
        ),
    ]
    return [
        {
            "audit_id": audit_id,
            "required_step": step,
            "mathematical_requirement": requirement,
            "current_status": status,
            "evidence_summary": evidence,
            "valid_for_claim": "false",
            "source_paths": source_list("272_doc", "341_doc", "407_doc", "410_doc", "414_doc", "415_doc", "710_doc"),
            "generated_utc": generated,
        }
        for audit_id, step, requirement, status, evidence in rows
    ]


def dpc710_ownership_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("OWN711_0_DPC710_0", "DPC710_0_field_split", "QDA711_0_quotient_object;QDA711_1_presymplectic_null", "open_burden", "field split not parent-owned"),
        ("OWN711_1_DPC710_1", "DPC710_1_action_descent", "QDA711_5_action_basicness", "not_derived", "action descent not parent-owned"),
        ("OWN711_2_DPC710_2", "DPC710_2_no_R_prefactor", "QDA711_6_no_prefactor", "not_derived", "delta_AEH zero not parent-owned"),
        ("OWN711_3_DPC710_3", "DPC710_3_matter_functor_blind", "QDA711_4_matter_functor_factorization", "fail_current_corpus", "matter blindness not parent-owned"),
        ("OWN711_4_DPC710_4", "DPC710_4_no_local_kinetic_mode", "QDA711_2_invariant_algebra_triviality;QDA711_3_local_class_selection", "fail_current_corpus", "scalar mode absence not parent-owned"),
        ("OWN711_5_DPC710_5", "DPC710_5_projection_silence", "QDA711_5_action_basicness;QDA711_6_no_prefactor", "not_derived", "projection silence not parent-owned"),
        ("OWN711_6_DPC710_6", "DPC710_6_same_frame", "QDA711_7_frame_readout", "not_derived", "same-frame identity not parent-owned"),
        ("OWN711_7_DPC710_7", "DPC710_7_Ward_owner", "QDA711_5_action_basicness;QDA711_8_topological_projector_analogy", "partial_analogy_only", "Ward owner not proved for scalar/class"),
        ("OWN711_8_DPC710_8", "DPC710_8_conditional_theorem", "DPC710_0..DPC710_7", "conditional_template_only", "theorem shape survives"),
        ("OWN711_9_DPC710_9", "DPC710_9_verdict", "all owners signed", "fail_current_corpus", "descent clause remains unowned"),
    ]
    return [
        {
            "owner_id": owner_id,
            "dpc710_clause": clause,
            "required_owner": owner,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("710_descent", "710_frame", "710_aeh"),
            "generated_utc": generated,
        }
        for owner_id, clause, owner, status, effect in rows
    ]


def prior_evidence_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("PE711_0_231", "relative cohomology route", "conditional_support", "cohomology/projector gate supports topological silence shape but parent projector remains open"),
        ("PE711_1_251_252", "metric-independent topological projector", "conditional_support", "good analogue for zero bulk metric variation; not scalar/class descent"),
        ("PE711_2_253_255", "FLRW/projector and stress normalization", "closure_warning", "topology can give shape while stress normalization remains closure"),
        ("PE711_3_272", "quotient configuration principle", "conditional_support_with_open_burden", "quotient follows if Cperp exactness/null direction is proved; open"),
        ("PE711_4_341", "indistinguishable-cell quotient", "template_not_promotion", "class action descends conditionally; effective action class function still open"),
        ("PE711_5_367", "class selection closure ledger", "demotion_support", "local-GR route explicitly demoted to labelled closure and residual testing"),
        ("PE711_6_372", "local phi_C silence", "conditional_closure_support", "grad phi_C zero only inside labelled local-trivial-class/boundary-state branch"),
        ("PE711_7_407", "primitive relational quotient action", "candidate_sketch", "best action sketch but matter functor/EH proofs remain open"),
        ("PE711_8_410", "quotient matter functor", "conditional_theorem_failed_parent_derivation", "factorization/no-marker/no-class-charge premises not parent-derived"),
        ("PE711_9_414_415", "invariant algebra and local class selector", "hard_fail_for_derivation", "local invariant algebra triviality and local class selector are not derived"),
    ]
    return [
        {
            "evidence_id": evidence_id,
            "source_topic": topic,
            "status": status,
            "readout_for_711": readout,
            "valid_for_claim": "false",
            "source_paths": source_list("231_doc", "251_doc", "252_doc", "253_doc", "255_doc", "272_doc", "341_doc", "367_doc", "372_doc", "407_doc", "410_doc", "414_doc", "415_doc"),
            "generated_utc": generated,
        }
        for evidence_id, topic, status, readout in rows
    ]


def demotion_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("DEM711_0_branch_label", "scalar_class_zero_route", "demoted_to_labelled_closure", "use only as MTS_scalar_class_silent_closure, not derived local GR"),
        ("DEM711_1_allowed_use", "private derivation/testing", "allowed", "may test the silent scalar/class branch as a disciplined closure hypothesis"),
        ("DEM711_2_forbidden_use", "claim delta_AEH_scalar=0", "forbidden", "not allowed until quotient descent clauses are parent-derived"),
        ("DEM711_3_forbidden_R10", "claim alpha(lambda)=0/pass", "forbidden", "R10 silence is closure-only unless matter functor and no-mode clauses are derived"),
        ("DEM711_4_forbidden_PPN", "claim PPN/WEP/Gdot pass", "forbidden", "same-frame/matter-blind/readout guard remains unowned"),
        ("DEM711_5_exit_condition", "closure can become theorem", "requires_QDA711_0_to_QDA711_7_parent_signed", "source paths, no MISSING markers, and retained stress accounting required"),
        ("DEM711_6_next", "next practical target", "build_closure_lock_and_residual_test_vector", NEXT_TARGET),
    ]
    return [
        {
            "demotion_id": demotion_id,
            "target": target,
            "status": status,
            "rule": rule,
            "valid_for_claim": "false",
            "source_paths": source_list("367_doc", "372_doc", "709_zero", "710_doc"),
            "generated_utc": generated,
        }
        for demotion_id, target, status, rule in rows
    ]


def retained_requirements_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("RR711_0_R11", "scalar_tensor_class_metric", "retain 708 R11 scalar row unless closure is explicitly selected or descent is parent-derived", "R11 residual ledger"),
        ("RR711_1_R10", "alpha_AB(lambda)", "closure branch sets alpha=0 only as closure; retained branch still needs lambda and source charges", "R10 alpha(lambda) template"),
        ("RR711_2_PPN", "gamma_minus_1;beta_minus_1", "closure branch sets scalar contribution zero only as closure; retained branch needs scalar-tensor map", "PPN residual vector"),
        ("RR711_3_WEP", "eta_AB", "closure branch assumes matter blindness; retained branch needs b_A,I source charges", "WEP/source-charge row"),
        ("RR711_4_Gdot", "Gdot/G", "closure branch assumes no time/readout drift; retained branch needs grad/time A_EH and clock map", "Gdot/clock row"),
        ("RR711_5_AEH", "A_EH scalar contribution", "closure branch may set delta_AEH_scalar=0 only with closure label; parent A_EH still unfilled", "A_EH inventory"),
    ]
    return [
        {
            "requirement_id": requirement_id,
            "observable_or_channel": channel,
            "rule": rule,
            "artifact_needed_next": artifact,
            "valid_for_claim": "false",
            "source_paths": source_list("708_r11", "708_r10", "710_aeh"),
            "generated_utc": generated,
        }
        for requirement_id, channel, rule, artifact in rows
    ]


def aeh_update_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("AEHU711_0_delta_AEH_scalar", "delta_AEH_scalar", "CLOSURE_ZERO_ONLY_OR_MISSING_PARENT_DESCENT", "closure_demoted_after_711"),
        ("AEHU711_1_grad_ln_AEH_scalar", "grad_ln_AEH_scalar", "CLOSURE_ZERO_ONLY_OR_MISSING_PARENT_DESCENT", "closure_demoted_after_711"),
        ("AEHU711_2_q_Aa", "q_Aa", "CLOSURE_ZERO_ONLY_OR_MISSING_MATTER_FUNCTOR_PROOF", "closure_demoted_after_711"),
        ("AEHU711_3_alpha_AB", "alpha_AB(lambda)", "CLOSURE_ZERO_ONLY_OR_RETAINED_R10_TEMPLATE", "closure_demoted_after_711"),
        ("AEHU711_4_scalar_R11", "scalar_tensor_class_metric", "CLOSURE_ZERO_ONLY_OR_RETAINED_R11_ROW", "closure_demoted_after_711"),
        ("AEHU711_5_AEH_sum", "A_EH", "MISSING_ALL_CHANNEL_VALUES_OR_ZERO_THEOREMS", "still_unfilled_after_711"),
    ]
    return [
        {
            "update_id": update_id,
            "target": target,
            "value_or_bound": value,
            "current_status": status,
            "valid_for_claim": "false",
            "source_paths": source_list("710_aeh", "708_r11", "708_r10"),
            "generated_utc": generated,
        }
        for update_id, target, value, status in rows
    ]


def gate_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("CG711_0_sources", "all source files load", "source register exists check", "pass_structure", "allows checkpoint only"),
        ("CG711_1_prior_710", "710 validation clean", "710 validation has no failures", "pass_structure", "inherits clean predecessor"),
        ("CG711_2_quotient_descent", "derive DPC710 from quotient geometry", "fail_current_corpus", "fail_blocked", "no parent descent claim"),
        ("CG711_3_invariant_algebra", "local invariant algebra triviality", "414 fail", "fail_blocked", "no scalar/class generator removal"),
        ("CG711_4_class_selector", "local trivial class selection", "415/367 closure", "fail_blocked", "no local class theorem"),
        ("CG711_5_matter_functor", "matter quotient functor", "410 conditional only", "fail_blocked", "no matter-blind theorem"),
        ("CG711_6_scalar_zero", "scalar zero route", "demoted_to_labelled_closure", "fail_blocked", "no claim-valid zero"),
        ("CG711_7_local_GR", "local-GR promotion", "not reached", "fail_blocked", "no local-GR claim"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": observed,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("710_validation", "410_doc", "414_doc", "415_doc", "367_doc"),
            "generated_utc": generated,
        }
        for gate_id, gate, observed, result, effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("D711_0_derivation", "quotient descent proof", "failed_current_corpus", "quotient/topological machinery is conditional and key scalar/class descent owners fail", NEXT_TARGET),
        ("D711_1_demote", "scalar zero route", "demoted_to_labelled_closure", "scalar silence may be used only as explicit closure branch", NEXT_TARGET),
        ("D711_2_retained", "retained modified branch", "still_available_unfilled", "if closure is not selected, scalar/class remains R11/R10/PPN/WEP/Gdot debt", NEXT_TARGET),
        ("D711_3_next", "next target", "selected", "lock the scalar/class closure branch and build the residual test vector without claiming GR", NEXT_TARGET),
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
            "summary_id": "S711_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "quotient geometry does not yet derive the DPC710 descent clause; scalar/class zero is demoted to an explicitly labelled closure branch",
            "hardest_blocker": "local quotient-invariant algebra triviality, local class selection, and matter functor factorization remain not parent-derived",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def all_generated_rows(*groups: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for group in groups for row in group]


def validation_rows(source_rows, audit, ownership, evidence, demotion, retained, aeh, gates, decisions, summary) -> list[dict[str, str]]:
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = len(validation_failures("710_validation"))
    audit_complete = {f"QDA711_{index}_{suffix}" for index, suffix in [
        (0, "quotient_object"),
        (1, "presymplectic_null"),
        (2, "invariant_algebra_triviality"),
        (3, "local_class_selection"),
        (4, "matter_functor_factorization"),
        (5, "action_basicness"),
        (6, "no_prefactor"),
        (7, "frame_readout"),
        (8, "topological_projector_analogy"),
        (9, "verdict"),
    ]}.issubset({row["audit_id"] for row in audit})
    audit_failed = any(row["audit_id"] == "QDA711_9_verdict" and row["current_status"] == "fail_current_corpus" for row in audit)
    dpc_mapped = len(ownership) >= 10 and any(row["dpc710_clause"] == "DPC710_9_verdict" and row["current_status"] == "fail_current_corpus" for row in ownership)
    evidence_covers_prior = len(evidence) >= 10 and any(row["evidence_id"] == "PE711_9_414_415" and row["status"] == "hard_fail_for_derivation" for row in evidence)
    demoted = any(row["demotion_id"] == "DEM711_0_branch_label" and row["status"] == "demoted_to_labelled_closure" for row in demotion)
    retained_ready_for_next = len(retained) >= 6 and all(row["valid_for_claim"] == "false" for row in retained)
    aeh_closure_only = all(row["valid_for_claim"] == "false" for row in aeh) and any("CLOSURE_ZERO_ONLY" in row["value_or_bound"] for row in aeh)
    gates_block = all(row["valid_for_claim"] == "false" for row in gates) and any(row["result"] == "fail_blocked" for row in gates)
    no_claim = all(row.get("valid_for_claim") != "true" for row in all_generated_rows(audit, ownership, evidence, demotion, retained, aeh, gates, decisions, summary))
    next_selected = decisions[-1]["next_action"] == NEXT_TARGET and summary[0]["next_target"] == NEXT_TARGET
    scoped = all(str(path).startswith(str(ROOT)) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_count()
    checks = [
        ("V711_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V711_1_prior_710_clean", prior_failures == 0, f"710_validation_failures={prior_failures}"),
        ("V711_2_quotient_audit_complete", audit_complete, f"audit_rows={len(audit)}"),
        ("V711_3_descent_derivation_failed", audit_failed, "QDA711_9_verdict=fail_current_corpus"),
        ("V711_4_DPC710_ownership_mapped", dpc_mapped, f"ownership_rows={len(ownership)}"),
        ("V711_5_prior_evidence_ledger_covers_failures", evidence_covers_prior, f"evidence_rows={len(evidence)}"),
        ("V711_6_scalar_zero_demoted", demoted, "scalar zero route demoted_to_labelled_closure"),
        ("V711_7_retained_requirements_written", retained_ready_for_next, f"retained_rows={len(retained)}"),
        ("V711_8_AEH_update_closure_only", aeh_closure_only, "AEH scalar rows are CLOSURE_ZERO_ONLY/nonclaim"),
        ("V711_9_gates_block_claim", gates_block, f"gate_rows={len(gates)}"),
        ("V711_10_no_claim_rows_promoted", no_claim, "all generated rows valid_for_claim=false"),
        ("V711_11_next_target_selected", next_selected, NEXT_TARGET),
        ("V711_12_outputs_scoped", scoped, "all outputs under post-checkpoint-work"),
        ("V711_13_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V711_14_status_nonclaim", "closure_lock_only" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
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


def write_doc(source_rows, audit, ownership, evidence, demotion, retained, aeh, gates, decisions, summary, validation) -> None:
    doc = f"""# 711 - Y5 R10 Derive Descent Clause From Quotient Geometry Or Demote Scalar Zero To Closure

## Verdict

711 tries to promote the 710 descent clause from a candidate into a derived quotient-geometry theorem.

It does **not** close. The existing quotient/topological machinery gives conditional support, but the needed parent derivation still fails at three hard points:

```text
local quotient-invariant algebra triviality
local trivial class selection
matter functor factorization / no class charge
```

Therefore the scalar/class zero route is now explicitly demoted to a labelled closure branch. That is not a defeat; it is the clean version of honesty. We can still test the closure branch, but we cannot call it derived local GR.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Quotient Descent Derivation Audit

{markdown_table(audit, ["audit_id", "required_step", "current_status", "evidence_summary", "valid_for_claim"])}

## DPC710 Ownership Map

{markdown_table(ownership, ["owner_id", "dpc710_clause", "required_owner", "current_status", "claim_effect", "valid_for_claim"])}

## Prior Quotient Evidence Ledger

{markdown_table(evidence, ["evidence_id", "source_topic", "status", "readout_for_711", "valid_for_claim"])}

## Scalar Zero Demotion Ledger

{markdown_table(demotion, ["demotion_id", "target", "status", "rule", "valid_for_claim"])}

## Retained Branch Requirements

{markdown_table(retained, ["requirement_id", "observable_or_channel", "rule", "artifact_needed_next", "valid_for_claim"])}

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
    audit = quotient_descent_audit_rows()
    ownership = dpc710_ownership_rows()
    evidence = prior_evidence_rows()
    demotion = demotion_rows()
    retained = retained_requirements_rows()
    aeh = aeh_update_rows()
    gates = gate_rows()
    decisions = decision_rows()
    summary = summary_rows()
    validation = validation_rows(source_rows, audit, ownership, evidence, demotion, retained, aeh, gates, decisions, summary)

    write_csv(OUTPUT_PATHS[1], source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(
        OUTPUT_PATHS[2],
        audit,
        ["audit_id", "required_step", "mathematical_requirement", "current_status", "evidence_summary", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[3],
        ownership,
        ["owner_id", "dpc710_clause", "required_owner", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[4],
        evidence,
        ["evidence_id", "source_topic", "status", "readout_for_711", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[5],
        demotion,
        ["demotion_id", "target", "status", "rule", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[6],
        retained,
        ["requirement_id", "observable_or_channel", "rule", "artifact_needed_next", "valid_for_claim", "source_paths", "generated_utc"],
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
    write_doc(source_rows, audit, ownership, evidence, demotion, retained, aeh, gates, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"audit_rows={len(audit)}")
    print(f"ownership_rows={len(ownership)}")
    print(f"demotion_rows={len(demotion)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
