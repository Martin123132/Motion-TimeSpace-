from __future__ import annotations

import csv
import re
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_scalar_class_parent_coefficient_hunt_failed_zero_premise_contract_written_nonclaim"
CLAIM_CEILING = "scalar_class_parent_coefficient_hunt_and_zero_premise_contract_only_no_AEH_zero_no_scalar_charge_zero_no_R10_PPN_WEP_Gdot_pass_no_local_GR_claim"
NEXT_TARGET = "710-Y5-R10-scalar-class-zero-premise-parent-action-clause-or-frame-transfer-guard.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "709-Y5-R10-scalar-class-parent-coefficient-hunt-or-zero-premise.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

OUTPUT_PATHS = [
    DOC_PATH,
    RESIDUALS / "P8_Y5_R10_709_SOURCE_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_709_PARENT_COEFFICIENT_HUNT_LEDGER.csv",
    RESIDUALS / "P8_Y5_R10_709_SOURCE_HIT_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_709_ZERO_PREMISE_AUDIT.csv",
    RESIDUALS / "P8_Y5_R10_709_COEFFICIENT_DECISION_MATRIX.csv",
    RESIDUALS / "P8_Y5_R10_709_CLOSURE_BRANCH_CONTRACT.csv",
    RESIDUALS / "P8_Y5_R10_709_AEH_SCALAR_UPDATE.csv",
    RESIDUALS / "P8_Y5_R10_709_CLAIM_GATE_EVALUATION.csv",
    RESIDUALS / "P8_Y5_R10_709_DECISION.csv",
    RESIDUALS / "P8_Y5_R10_709_NONCLAIM_SUMMARY.csv",
    RESIDUALS / "P8_Y5_BRR545_709_VALIDATION.csv",
]

SOURCE_PATHS = {
    "402_doc": ROOT / "402-EH-source-normalization-parent-pair.md",
    "424_doc": ROOT / "424-same-frame-EH-source-Poisson-reduction-gate.md",
    "440_doc": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "704_doc": ROOT / "704-Y5-R10-EH-prefactor-constant-theorem-or-kappa-gradient-bound.md",
    "705_doc": ROOT / "705-Y5-R10-AEH-prefactor-source-row-or-no-FchiR-theorem.md",
    "706_doc": ROOT / "706-Y5-R10-parent-action-term-inventory-for-AEH-source-row.md",
    "707_doc": ROOT / "707-Y5-R10-scalar-class-FR-prefactor-zero-or-AEH-bound.md",
    "708_doc": ROOT / "708-Y5-R10-scalar-class-source-row-or-R11-R10-bound-map.md",
    "708_validation": RESIDUALS / "P8_Y5_BRR545_708_VALIDATION.csv",
    "705_channels": RESIDUALS / "P8_Y5_R10_705_VARIABLE_PREFACTOR_CHANNELS.csv",
    "705_no_fchir": RESIDUALS / "P8_Y5_R10_705_NO_FCHIR_THEOREM_AUDIT.csv",
    "706_inventory": RESIDUALS / "P8_Y5_R10_706_AEH_TERM_INVENTORY.csv",
    "707_zero": RESIDUALS / "P8_Y5_R10_707_SCALAR_CLASS_ZERO_THEOREM_AUDIT.csv",
    "708_contract": RESIDUALS / "P8_Y5_R10_708_SCALAR_CLASS_SOURCE_ROW_CONTRACT.csv",
    "708_expansion": RESIDUALS / "P8_Y5_R10_708_LOCAL_EXPANSION_MAP.csv",
    "708_r10": RESIDUALS / "P8_Y5_R10_708_R10_ALPHA_LAMBDA_SCALAR_TEMPLATE.csv",
    "708_r11": RESIDUALS / "P8_Y5_R10_708_R11_SCALAR_OPERATOR_ROW.csv",
    "708_ppn": RESIDUALS / "P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv",
}

SEARCH_TERMS = {
    "scalar_prefactor": re.compile(r"F\(phi,C\)R|F\(φ,C\)R|scalar_tensor_class_metric|scalar_class", re.IGNORECASE),
    "aeh": re.compile(r"A_EH|delta_AEH|grad(?:_mu)? ln A_EH", re.IGNORECASE),
    "coefficient": re.compile(r"Z_IJ|M_IJ|mass matrix|B_A|source charge|matter charge|kinetic metric|prefactor gradient", re.IGNORECASE),
    "missing": re.compile(r"MISSING|not_parent_signed|retained_not_reduced|fail_current_corpus|retained_unfilled", re.IGNORECASE),
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
        "402_doc": "EH/source normalization warning source",
        "424_doc": "same-frame Poisson reduction gate",
        "440_doc": "scalar/class retained sector source",
        "655_doc": "R11 scalar/class fallback source",
        "704_doc": "A_EH bottleneck source",
        "705_doc": "A_EH source-row/no-FchiR source",
        "706_doc": "A_EH inventory source",
        "707_doc": "scalar zero theorem predecessor",
        "708_doc": "scalar coefficient contract predecessor",
        "708_validation": "708 validation gate",
        "705_channels": "variable prefactor channel ledger",
        "705_no_fchir": "no-FchiR theorem audit",
        "706_inventory": "A_EH term inventory",
        "707_zero": "scalar zero theorem audit",
        "708_contract": "scalar source-row contract",
        "708_expansion": "scalar local expansion map",
        "708_r10": "scalar R10 template",
        "708_r11": "scalar R11 row",
        "708_ppn": "PPN/Gdot/WEP scalar map",
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


def source_hit_rows() -> list[dict[str, str]]:
    generated = now()
    rows: list[dict[str, str]] = []
    text_sources = [
        "402_doc",
        "424_doc",
        "440_doc",
        "655_doc",
        "704_doc",
        "705_doc",
        "706_doc",
        "707_doc",
        "708_doc",
    ]
    for source_id in text_sources:
        path = SOURCE_PATHS[source_id]
        if not path.exists():
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            matched_terms = [term for term, pattern in SEARCH_TERMS.items() if pattern.search(line)]
            if not matched_terms:
                continue
            rows.append(
                {
                    "hit_id": f"HIT709_{len(rows):03d}",
                    "source_id": source_id,
                    "path": str(path),
                    "line_number": str(line_number),
                    "matched_terms": ";".join(matched_terms),
                    "snippet": line.strip()[:420],
                    "claim_usable": "false",
                    "reason": "hit names scalar/A_EH/coefficient debt but does not supply all claim-ready coefficient values",
                    "generated_utc": generated,
                }
            )
    return rows


def coefficient_hunt_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "PCH709_0_parent_action_form",
            "A_EH(u), Z_IJ(u), V(u), B_A(u) in one observed-frame parent action",
            "MISSING_PARENT_ACTION_COEFFICIENT_SOURCE",
            "708 names required form; 440/705/706/707 identify the scalar/class danger but do not provide the action coefficients",
            "blocks executable scalar branch",
        ),
        (
            "PCH709_1_field_multiplet",
            "u^I=(phi,C,...) concrete list",
            "MISSING_FIELD_MULTIPLET_SOURCE",
            "phi/C/class labels are named only schematically",
            "cannot diagonalize or prove absence",
        ),
        (
            "PCH709_2_background",
            "u0^I and A_EH(u0)",
            "MISSING_BACKGROUND_VALUE",
            "no local vacuum background value found",
            "cannot compute delta_AEH_scalar",
        ),
        (
            "PCH709_3_prefactor_gradient",
            "a_I=partial_I ln A_EH|u0",
            "MISSING_PREFACTOR_GRADIENT_VECTOR",
            "no derivative vector or theorem a_I=0 found",
            "cannot compute grad ln A_EH or scalar force amplitude",
        ),
        (
            "PCH709_4_kinetic_metric",
            "Z_IJ(u0)",
            "MISSING_KINETIC_METRIC",
            "no kinetic metric, degeneracy proof, or gauge classification found",
            "cannot canonicalize scalar modes",
        ),
        (
            "PCH709_5_mass_matrix",
            "M_IJ^2 or equivalent scalar range",
            "MISSING_MASS_MATRIX",
            "no mass/range or infinite-mass theorem found",
            "cannot place R10 lambda",
        ),
        (
            "PCH709_6_matter_charges",
            "b_A,I=partial_I ln m_A(u) or b_A,I=0 theorem",
            "MISSING_SOURCE_TEST_CHARGE_VECTOR",
            "source charge is repeatedly flagged as debt, not sourced",
            "cannot compute WEP/R10 alpha",
        ),
        (
            "PCH709_7_frame_guard",
            "same observed frame and no Weyl/disformal matter debt",
            "MISSING_FRAME_TRANSFER_GUARD",
            "frame-transfer channel remains not_parent_signed",
            "cannot set A_EH=1 by field redefinition without moving debt",
        ),
        (
            "PCH709_8_bound_sources",
            "real R10/PPN/WEP/Gdot bound inputs tied to scalar branch",
            "MISSING_BRANCH_BOUND_SOURCE_ROWS",
            "708 writes branch templates only",
            "no score-ready comparison",
        ),
        (
            "PCH709_9_verdict",
            "claim-ready parent coefficient row",
            "fail_current_corpus",
            "hunt found named debts and templates, not a sourced coefficient row",
            "scalar/class remains retained/nonclaim",
        ),
    ]
    return [
        {
            "hunt_id": hunt_id,
            "target_object": target,
            "current_status": status,
            "evidence_summary": evidence,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("440_doc", "705_doc", "706_doc", "707_doc", "708_doc", "708_contract", "708_expansion"),
            "generated_utc": generated,
        }
        for hunt_id, target, status, evidence, effect in rows
    ]


def zero_premise_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "ZP709_0_target",
            "scalar/class zero premise",
            "If scalar/class labels are non-dynamical quotient/topological labels with no local R prefactor and no matter charge, then delta_AEH_scalar=0 and q_Aa=0.",
            "conditional_target_written",
            "states the clean route",
        ),
        (
            "ZP709_1_no_local_field",
            "no local scalar/class degree of freedom",
            "u^I is absent from the local variational field set or is pure gauge/topological with delta_g u^I=0.",
            "not_parent_signed",
            "blocks absence proof",
        ),
        (
            "ZP709_2_no_prefactor",
            "no A_EH(u)R term",
            "parent local action separates as R[g_obs] plus scalar/class terms that do not multiply R after projection.",
            "not_parent_signed",
            "blocks delta_AEH_scalar=0",
        ),
        (
            "ZP709_3_constant_universal",
            "constant universal quotient value",
            "if u^I survives, u^I=u0^I is constant across time, range, source species, frame, and local environment.",
            "not_parent_signed",
            "constant offset still needs independent G_ref/source normalization guard",
        ),
        (
            "ZP709_4_no_kinetic_or_massive_decoupled",
            "no propagating sourced scalar",
            "Z_IJ is gauge-degenerate/topological or modes have infinite mass and zero matter charge through tested ranges.",
            "not_parent_signed",
            "blocks R10 silence",
        ),
        (
            "ZP709_5_matter_blind",
            "matter functor blind to scalar/class labels",
            "B_A(u)=constant universal and b_A,I=0 for all source/test species.",
            "not_parent_signed",
            "blocks WEP/source-charge zero",
        ),
        (
            "ZP709_6_no_frame_transfer",
            "frame-transfer guard",
            "no Weyl/disformal redefinition moves A_EH variation into matter, clocks, or source masses.",
            "not_parent_signed",
            "blocks fake Einstein-frame pass",
        ),
        (
            "ZP709_7_boundary_projection_silence",
            "no boundary/projection leakage",
            "projecting quotient/class labels to the observed branch creates no boundary stress, counterterm shift, or source-mass subtraction.",
            "not_parent_signed",
            "blocks hidden A_EH shift",
        ),
        (
            "ZP709_8_conditional_theorem",
            "zero-premise theorem",
            "ZP709_1+ZP709_2+ZP709_5+ZP709_6+ZP709_7 imply delta_AEH_scalar=0, grad ln A_EH=0, q_Aa=0, and no scalar R10/PPN/WEP/Gdot residual.",
            "proved_as_conditional_template",
            "the theorem shape is useful but not parent-owned",
        ),
        (
            "ZP709_9_verdict",
            "claim-ready zero premise",
            "parent action proves all zero-premise clauses without adding a closure axiom.",
            "fail_current_corpus",
            "zero route not promoted",
        ),
    ]
    return [
        {
            "premise_id": premise_id,
            "clause": clause,
            "mathematical_requirement": requirement,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("440_doc", "705_no_fchir", "706_inventory", "707_zero", "708_contract"),
            "generated_utc": generated,
        }
        for premise_id, clause, requirement, status, effect in rows
    ]


def decision_matrix_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "CDM709_0_numeric_branch",
            "source parent coefficients and compute residuals",
            "blocked",
            "A_EH(u0), a_I, Z_IJ, M_IJ, b_A,I, frame convention, and bounds are missing",
            "do not score R10/PPN/WEP/Gdot",
        ),
        (
            "CDM709_1_zero_branch",
            "prove scalar/class zero premise",
            "blocked_but_best_derivation_route",
            "zero theorem shape is clean and subject to less empirical normalization ambiguity, but parent ownership is missing",
            "try parent-action clause next",
        ),
        (
            "CDM709_2_closure_branch",
            "declare scalar/class locally silent closure",
            "allowed_only_if_labelled_closure",
            "can define a private branch, but it is not derived local GR",
            "keep valid_for_claim=false",
        ),
        (
            "CDM709_3_retained_branch",
            "retain scalar/class as modified-gravity R11/R10 branch",
            "available_but_unfilled",
            "requires coefficients and bounds before testing",
            "not a local-GR proof",
        ),
        (
            "CDM709_4_next",
            "best next action",
            "selected",
            "write or reject the exact parent-action clause that would own ZP709_1 through ZP709_7, with frame-transfer guard",
            NEXT_TARGET,
        ),
    ]
    return [
        {
            "decision_matrix_id": matrix_id,
            "route": route,
            "status": status,
            "reason": reason,
            "next_action": action,
            "valid_for_claim": "false",
            "source_paths": source_list("707_doc", "708_doc", "708_contract", "708_expansion"),
            "generated_utc": generated,
        }
        for matrix_id, route, status, reason, action in rows
    ]


def closure_contract_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "CLC709_0_branch_label",
            "MTS_scalar_class_silent_closure",
            "must be explicitly labelled closure-only unless ZP709 clauses are parent-derived",
            "closure_only_nonclaim",
        ),
        (
            "CLC709_1_allowed_assumption",
            "u^I is locally quotient/topological/readout-only and cannot source local stress or matter charge",
            "may be used for private algebra exploration only",
            "closure_only_nonclaim",
        ),
        (
            "CLC709_2_forbidden_upgrade",
            "closure branch cannot count as A_EH=1 proof, local GR proof, or R10/PPN pass",
            "prevents axiom smuggling",
            "guard_active",
        ),
        (
            "CLC709_3_exit_condition",
            "closure becomes derived only if parent action proves ZP709_1 through ZP709_7",
            "requires source paths and no MISSING markers",
            "blocked_current_corpus",
        ),
    ]
    return [
        {
            "closure_id": closure_id,
            "item": item,
            "rule": rule,
            "current_status": status,
            "valid_for_claim": "false",
            "source_paths": source_list("707_doc", "708_doc"),
            "generated_utc": generated,
        }
        for closure_id, item, rule, status in rows
    ]


def aeh_update_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("AEHS709_0_delta_AEH_scalar", "delta_AEH_scalar", "MISSING_PARENT_COEFFICIENT_OR_ZERO_PREMISE", "retained_not_reduced_after_709"),
        ("AEHS709_1_grad_ln_AEH_scalar", "grad_ln_AEH_scalar", "MISSING_PREFACTOR_GRADIENT_OR_ZERO_PREMISE", "retained_not_reduced_after_709"),
        ("AEHS709_2_source_charge", "q_Aa", "MISSING_SOURCE_TEST_CHARGE_OR_MATTER_BLIND_THEOREM", "retained_not_reduced_after_709"),
        ("AEHS709_3_R10_alpha", "alpha_AB(lambda_a)", "MISSING_LAMBDA_AND_ALPHA_OR_ZERO_PREMISE", "retained_not_reduced_after_709"),
        ("AEHS709_4_AEH_sum", "A_EH", "MISSING_CHANNEL_VALUES_OR_ZERO_THEOREMS", "still_unfilled_after_709"),
    ]
    return [
        {
            "update_id": update_id,
            "target": target,
            "value_or_bound": value,
            "current_status": status,
            "valid_for_claim": "false",
            "source_paths": source_list("706_inventory", "707_zero", "708_contract", "708_expansion"),
            "generated_utc": generated,
        }
        for update_id, target, value, status in rows
    ]


def gate_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("CG709_0_sources", "all source files load", "source register exists check", "pass_structure", "allows checkpoint only"),
        ("CG709_1_prior_708", "708 validation clean", "708 validation has no failures", "pass_structure", "inherits clean predecessor"),
        ("CG709_2_hunt", "parent coefficient hunt", "no claim-ready coefficient row found", "fail_blocked", "no scalar coefficient claim"),
        ("CG709_3_zero_premise", "zero-premise theorem", "conditional template only", "fail_blocked", "no delta_AEH_scalar zero claim"),
        ("CG709_4_matter_blind", "source/test charge zero", "not_parent_signed", "fail_blocked", "no WEP/R10 source silence"),
        ("CG709_5_frame_guard", "frame transfer guard", "not_parent_signed", "fail_blocked", "no Einstein-frame shortcut"),
        ("CG709_6_R10_R11", "retained branch score", "coefficients and bounds missing", "fail_blocked", "no R10/R11 score"),
        ("CG709_7_local_GR", "local-GR promotion", "not reached", "fail_blocked", "no local-GR claim"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": observed,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("708_validation", "708_contract", "708_expansion", "707_zero", "705_no_fchir"),
            "generated_utc": generated,
        }
        for gate_id, gate, observed, result, effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "D709_0_hunt",
            "parent coefficient hunt",
            "failed_current_corpus",
            "existing sources name the scalar/class coupling but do not provide A_EH(u), Z_IJ, V, B_A, u0, diagonalization, or charges",
            NEXT_TARGET,
        ),
        (
            "D709_1_zero",
            "zero premise",
            "conditional_template_written",
            "the clean derivation route is to prove scalar/class labels are locally non-dynamical, matter-blind, no-prefactor, and frame-safe",
            NEXT_TARGET,
        ),
        (
            "D709_2_policy",
            "claim policy",
            "blocked_nonclaim",
            "closure is allowed only as labelled private branch; no public/local-GR claim",
            NEXT_TARGET,
        ),
        (
            "D709_3_next",
            "next target",
            "selected",
            "attempt exact parent-action clause or frame-transfer guard for scalar/class zero premise",
            NEXT_TARGET,
        ),
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
            "summary_id": "S709_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "no parent coefficient source was found; scalar/class zero premise is now written as exact parent-action obligations",
            "hardest_blocker": "prove no local scalar/class degree, no A_EH(u)R prefactor, matter-blindness, frame safety, and no boundary/projection leakage",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def has_missing_marker(row: dict[str, str]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values())


def all_generated_rows(*groups: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for group in groups for row in group]


def validation_rows(source_rows, hunt, hits, zero, matrix, closure, aeh, gates, decisions, summary) -> list[dict[str, str]]:
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = len(validation_failures("708_validation"))
    hunt_targets = {
        "PCH709_0_parent_action_form",
        "PCH709_1_field_multiplet",
        "PCH709_2_background",
        "PCH709_3_prefactor_gradient",
        "PCH709_4_kinetic_metric",
        "PCH709_5_mass_matrix",
        "PCH709_6_matter_charges",
        "PCH709_7_frame_guard",
        "PCH709_8_bound_sources",
        "PCH709_9_verdict",
    }
    zero_targets = {
        "ZP709_1_no_local_field",
        "ZP709_2_no_prefactor",
        "ZP709_5_matter_blind",
        "ZP709_6_no_frame_transfer",
        "ZP709_7_boundary_projection_silence",
        "ZP709_8_conditional_theorem",
        "ZP709_9_verdict",
    }
    hunt_complete = hunt_targets.issubset({row["hunt_id"] for row in hunt})
    hunt_failed = any(row["hunt_id"] == "PCH709_9_verdict" and row["current_status"] == "fail_current_corpus" for row in hunt)
    hits_recorded = len(hits) > 0 and all(row["claim_usable"] == "false" for row in hits)
    zero_complete = zero_targets.issubset({row["premise_id"] for row in zero})
    zero_not_promoted = any(row["premise_id"] == "ZP709_9_verdict" and row["current_status"] == "fail_current_corpus" for row in zero)
    closure_nonclaim = all(row["valid_for_claim"] == "false" for row in closure) and any(row["current_status"] == "closure_only_nonclaim" for row in closure)
    aeh_unfilled = all(row["valid_for_claim"] == "false" for row in aeh) and any(has_missing_marker(row) for row in aeh)
    gates_block = all(row["valid_for_claim"] == "false" for row in gates) and any(row["result"] == "fail_blocked" for row in gates)
    no_claim = all(row.get("valid_for_claim") != "true" for row in all_generated_rows(hunt, hits, zero, matrix, closure, aeh, gates, decisions, summary))
    next_selected = decisions[-1]["next_action"] == NEXT_TARGET and summary[0]["next_target"] == NEXT_TARGET
    scoped = all(str(path).startswith(str(ROOT)) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_count()
    checks = [
        ("V709_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V709_1_prior_708_clean", prior_failures == 0, f"708_validation_failures={prior_failures}"),
        ("V709_2_coefficient_hunt_complete", hunt_complete, f"hunt_rows={len(hunt)}"),
        ("V709_3_no_parent_coefficient_found", hunt_failed, "PCH709_9_verdict=fail_current_corpus"),
        ("V709_4_source_hits_recorded_nonclaim", hits_recorded, f"hit_rows={len(hits)}"),
        ("V709_5_zero_premise_complete", zero_complete, f"zero_rows={len(zero)}"),
        ("V709_6_zero_not_promoted", zero_not_promoted, "ZP709_9_verdict blocks claim"),
        ("V709_7_closure_branch_nonclaim", closure_nonclaim, "closure branch labelled closure_only_nonclaim"),
        ("V709_8_AEH_update_unfilled", aeh_unfilled, "AEH scalar rows remain MISSING/nonclaim"),
        ("V709_9_gates_block_claim", gates_block, f"gate_rows={len(gates)}"),
        ("V709_10_no_claim_rows_promoted", no_claim, "all generated rows valid_for_claim=false"),
        ("V709_11_next_target_selected", next_selected, NEXT_TARGET),
        ("V709_12_outputs_scoped", scoped, "all outputs under post-checkpoint-work"),
        ("V709_13_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V709_14_status_nonclaim", "no_AEH_zero" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
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


def write_doc(source_rows, hunt, hits, zero, matrix, closure, aeh, gates, decisions, summary, validation) -> None:
    doc = f"""# 709 - Y5 R10 Scalar Class Parent Coefficient Hunt Or Zero Premise

## Verdict

709 performs the parent-coefficient hunt requested by 708.

The result is sharp but non-claim:

```text
No sourced parent row was found for:
A_EH(u), u0^I, partial_I ln A_EH, Z_IJ, M_IJ^2, b_A,I, canonical modes, or frame/source normalization.
```

So the scalar/class branch still cannot be scored as R10, PPN, WEP, Gdot, R11, or local GR.

The useful progress is that the alternate route is now exact: a future parent action must prove the scalar/class zero premise, not merely say the scalar/class sector is "intuitive", "quotient", "readout", or "background". The required clauses are no local field, no `A_EH(u)R` prefactor, matter blindness, no frame transfer, and no boundary/projection leakage.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Parent Coefficient Hunt Ledger

{markdown_table(hunt, ["hunt_id", "target_object", "current_status", "evidence_summary", "claim_effect", "valid_for_claim"])}

## Source Hit Register

{markdown_table(hits[:30], ["hit_id", "source_id", "line_number", "matched_terms", "claim_usable", "reason"])}

## Zero Premise Audit

{markdown_table(zero, ["premise_id", "clause", "current_status", "claim_effect", "valid_for_claim"])}

## Coefficient Decision Matrix

{markdown_table(matrix, ["decision_matrix_id", "route", "status", "reason", "next_action", "valid_for_claim"])}

## Closure Branch Contract

{markdown_table(closure, ["closure_id", "item", "rule", "current_status", "valid_for_claim"])}

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
    hunt = coefficient_hunt_rows()
    hits = source_hit_rows()
    zero = zero_premise_rows()
    matrix = decision_matrix_rows()
    closure = closure_contract_rows()
    aeh = aeh_update_rows()
    gates = gate_rows()
    decisions = decision_rows()
    summary = summary_rows()
    validation = validation_rows(source_rows, hunt, hits, zero, matrix, closure, aeh, gates, decisions, summary)

    write_csv(OUTPUT_PATHS[1], source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(
        OUTPUT_PATHS[2],
        hunt,
        ["hunt_id", "target_object", "current_status", "evidence_summary", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[3],
        hits,
        ["hit_id", "source_id", "path", "line_number", "matched_terms", "snippet", "claim_usable", "reason", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[4],
        zero,
        ["premise_id", "clause", "mathematical_requirement", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[5],
        matrix,
        ["decision_matrix_id", "route", "status", "reason", "next_action", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[6],
        closure,
        ["closure_id", "item", "rule", "current_status", "valid_for_claim", "source_paths", "generated_utc"],
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
    write_doc(source_rows, hunt, hits, zero, matrix, closure, aeh, gates, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"hunt_rows={len(hunt)}")
    print(f"hit_rows={len(hits)}")
    print(f"zero_rows={len(zero)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
