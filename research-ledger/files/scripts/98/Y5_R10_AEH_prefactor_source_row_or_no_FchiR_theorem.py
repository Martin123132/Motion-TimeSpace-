from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_AEH_prefactor_source_row_schema_written_no_FchiR_theorem_conditional_unfilled_nonclaim"
CLAIM_CEILING = "AEH_source_row_or_no_FchiR_theorem_contract_only_no_AEH_value_no_epsilon_G_zero_no_kappa_gradient_bound_no_Delta_Poisson_fill_no_local_GR_claim"
NEXT_TARGET = "706-Y5-R10-parent-action-term-inventory-for-AEH-source-row.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "705-Y5-R10-AEH-prefactor-source-row-or-no-FchiR-theorem.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

OUTPUT_PATHS = [
    DOC_PATH,
    RESIDUALS / "P8_Y5_R10_705_SOURCE_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_705_AEH_SOURCE_ROW_SCHEMA.csv",
    RESIDUALS / "P8_Y5_R10_705_NO_FCHIR_THEOREM_AUDIT.csv",
    RESIDUALS / "P8_Y5_R10_705_VARIABLE_PREFACTOR_CHANNELS.csv",
    RESIDUALS / "P8_Y5_R10_705_AEH_CANDIDATE_FILL_ROW.csv",
    RESIDUALS / "P8_Y5_R10_705_EVALUATOR.csv",
    RESIDUALS / "P8_Y5_R10_705_CLAIM_GATE_EVALUATION.csv",
    RESIDUALS / "P8_Y5_R10_705_DECISION.csv",
    RESIDUALS / "P8_Y5_R10_705_NONCLAIM_SUMMARY.csv",
    RESIDUALS / "P8_Y5_BRR545_705_VALIDATION.csv",
]

SOURCE_PATHS = {
    "402_doc": ROOT / "402-EH-source-normalization-parent-pair.md",
    "424_doc": ROOT / "424-same-frame-EH-source-Poisson-reduction-gate.md",
    "429_doc": ROOT / "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
    "440_doc": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
    "523_doc": ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
    "652_doc": ROOT / "652-Y5-R10-WEP-source-normalization-or-common-geometry-zero-theorem.md",
    "653_doc": ROOT / "653-Y5-R10-parent-matter-functor-signature-or-WEP-closure-demotion.md",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "657_doc": ROOT / "657-Y5-R10-source-normalization-family-first-real-R11-fill.md",
    "696_doc": ROOT / "696-Y5-R10-MHref-same-frame-denominator-or-BTF-product-bound-guard.md",
    "703_doc": ROOT / "703-Y5-R10-parent-action-coupling-lock-or-Rsrc-channel-zero-theorem.md",
    "704_doc": ROOT / "704-Y5-R10-EH-prefactor-constant-theorem-or-kappa-gradient-bound.md",
    "704_validation": RESIDUALS / "P8_Y5_BRR545_704_VALIDATION.csv",
    "704_prefactor": RESIDUALS / "P8_Y5_R10_704_EH_PREFACTOR_FORMALIZATION.csv",
    "704_constant": RESIDUALS / "P8_Y5_R10_704_CONSTANT_THEOREM_AUDIT.csv",
    "704_gradient": RESIDUALS / "P8_Y5_R10_704_KAPPA_GRADIENT_BOUND_PACK.csv",
    "704_delta": RESIDUALS / "P8_Y5_R10_704_DELTA_POISSON_UPDATE.csv",
    "703_parent_lock": RESIDUALS / "P8_Y5_R10_703_PARENT_ACTION_COUPLING_LOCK_AUDIT.csv",
    "703_variation": RESIDUALS / "P8_Y5_R10_703_ACTION_VARIATION_CONTRACT.csv",
    "702_rsrc": RESIDUALS / "P8_Y5_R10_702_RSRC_CHANNEL_DECOMPOSITION.csv",
    "source_norm_scorecard": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
    "657_channels": RESIDUALS / "P8_Y5_R10_657_CMU_EIGHT_CHANNEL_VECTOR.csv",
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
        "402_doc": "EH/source-normalization parent pair",
        "424_doc": "same-frame EH-source Poisson gate",
        "429_doc": "Ward/Bianchi source residual owner",
        "440_doc": "metric-only second-order sector reduction attempt",
        "523_doc": "Gauss/orbital source-normalization scorecard",
        "652_doc": "common-geometry/WEP source normalization",
        "653_doc": "parent matter functor signature predecessor",
        "655_doc": "EH operator selection and R11 fallback",
        "657_doc": "source-normalization family and channel vector",
        "696_doc": "M_H_ref/G_ref circularity guard",
        "703_doc": "parent-action coupling lock predecessor",
        "704_doc": "EH prefactor predecessor",
        "704_validation": "704 validation gate",
        "704_prefactor": "704 A_EH formalization",
        "704_constant": "704 constant theorem audit",
        "704_gradient": "704 kappa-gradient bound pack",
        "704_delta": "704 Delta_Poisson update",
        "703_parent_lock": "703 parent-action coupling lock audit",
        "703_variation": "703 action variation contract",
        "702_rsrc": "702 R_src channel decomposition",
        "source_norm_scorecard": "source-normalization residual scorecard",
        "657_channels": "eight source-normalization residual channels",
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


def aeh_source_schema_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "AEH705_0_schema",
            "claim-ready A_EH source row",
            "A_EH; d_t ln A_EH; d_r ln A_EH; d_lambda ln A_EH; d_A ln A_EH; equation_ref; source_path; valid_for_claim",
            "all fields sourced, unit-checked, same-frame, and parent-action owned",
            "SCHEMA_WRITTEN",
            "not_applicable",
            "schema only",
        ),
        (
            "AEH705_1_AEH_value",
            "A_EH",
            "dimensionless coefficient multiplying R[g_obs] in the observed-frame parent action",
            "A_EH=1 theorem, A_EH=C independent constant with independent G_ref, or numeric bound abs(1/A_EH-1)",
            "MISSING_AEH_PARENT_VALUE_OR_THEOREM_ONE",
            "dimensionless",
            "blocks epsilon_G",
        ),
        (
            "AEH705_2_no_FchiR",
            "no variable prefactor",
            "no F(chi,theta,X,domain) R[g_obs] term survives the local branch",
            "parent action inventory plus reduction theorem",
            "MISSING_NO_FCHIR_THEOREM",
            "not_applicable",
            "blocks kappa-gradient zero",
        ),
        (
            "AEH705_3_no_frame_transfer",
            "no Weyl/disformal transfer",
            "field redefinitions do not move variable coupling into the matter/source sector",
            "same observed frame theorem",
            "MISSING_NO_FRAME_TRANSFER_THEOREM",
            "not_applicable",
            "blocks source-frame coupling lock",
        ),
        (
            "AEH705_4_derivative_vector",
            "grad ln A_EH",
            "d_t,d_r,d_lambda,d_A derivatives or theorem-zero",
            "derivative zero theorem or sourced bounds with units",
            "MISSING_GRAD_AEH_VECTOR",
            "per_time;per_length;per_range;dimensionless_per_species",
            "blocks kappa-gradient fallback",
        ),
        (
            "AEH705_5_boundary_guard",
            "boundary/counterterm shift",
            "boundary/counterterm convention does not renormalize A_EH or G_ref",
            "boundary no-hair/counterterm guard",
            "MISSING_BOUNDARY_PREFACTOR_GUARD",
            "not_applicable",
            "blocks constant-offset interpretation",
        ),
        (
            "AEH705_6_verdict",
            "claim-ready A_EH fill",
            "A_EH source row accepted for 704/Delta_Poisson",
            "AEH705_1 through AEH705_5 cleared",
            "fail_current_corpus",
            "mixed",
            "no A_EH claim",
        ),
    ]
    return [
        {
            "schema_id": schema_id,
            "target": target,
            "definition": definition,
            "required_evidence": evidence,
            "current_status": status,
            "units": units,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("704_prefactor", "704_constant", "704_gradient", "704_delta"),
            "generated_utc": generated,
        }
        for schema_id, target, definition, evidence, status, units, effect in rows
    ]


def no_fchir_theorem_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "NFC705_0_parent_inventory",
            "parent action term inventory",
            "list every local term that can become F(chi,theta,X,domain)R[g_obs] after projection/reduction",
            "MISSING_PARENT_TERM_INVENTORY",
            "cannot prove absence without inventory",
        ),
        (
            "NFC705_1_scalar_class",
            "scalar/class metric prefactors",
            "phi, C, class metric, or quotient scalar do not multiply R or are constant universal",
            "not_parent_signed",
            "scalar-tensor/f(R) channel remains retained",
        ),
        (
            "NFC705_2_memory_selector_domain",
            "memory/selector/domain prefactors",
            "theta, chi_D, P_D, L_cg, or domain variables do not multiply R locally",
            "not_parent_signed",
            "projector/domain stress remains retained",
        ),
        (
            "NFC705_3_bulk_auxiliary",
            "bulk-X/auxiliary integration",
            "integrating out auxiliary fields does not generate f(R), F(X)R, or finite-range scalar coupling",
            "not_parent_signed",
            "bulk/memory source channel remains retained",
        ),
        (
            "NFC705_4_higher_curvature",
            "higher-curvature disguise",
            "R^2, f(R), Ricci^2, Weyl^2, or nonlocal kernels do not masquerade as variable EH prefactor at weak field",
            "not_parent_signed",
            "R11/nonEH operator vector remains retained",
        ),
        (
            "NFC705_5_frame_redefinition",
            "Weyl/disformal frame guard",
            "a field redefinition cannot set A_EH=1 while making matter non-universally coupled",
            "not_parent_signed",
            "same-frame matter/source debt remains",
        ),
        (
            "NFC705_6_boundary_counterterm",
            "boundary/counterterm guard",
            "boundary terms do not shift the local R coefficient or subtract physical source mass",
            "not_parent_signed",
            "G_ref/M_H_ref circularity remains",
        ),
        (
            "NFC705_7_conditional_theorem",
            "no-FchiR theorem",
            "NFC705_0 through NFC705_6 imply A_EH=1 constant and grad A_EH=0",
            "proved_as_conditional_template",
            "useful theorem shape only",
        ),
        (
            "NFC705_8_verdict",
            "claim-ready no-FchiR theorem",
            "parent action has no local variable EH prefactor in observed branch",
            "fail_current_corpus",
            "no no-FchiR claim",
        ),
    ]
    return [
        {
            "theorem_id": theorem_id,
            "clause": clause,
            "mathematical_requirement": requirement,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("440_doc", "655_doc", "657_doc", "703_parent_lock", "704_constant"),
            "generated_utc": generated,
        }
        for theorem_id, clause, requirement, status, effect in rows
    ]


def variable_prefactor_channel_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("VPC705_0_scalar_class", "F(phi,C)R", "scalar/class/quotient metric sector", "retained_not_reduced", "R2/R3/R4/R9/R10/R11", "needs no-scalar-prefactor theorem or R11/R10 map"),
        ("VPC705_1_memory", "F(theta)R", "memory/nonlocal kernel sector", "retained_symbolic", "R7/R9/R10/R11", "needs compact-local kernel silence or derivative bound"),
        ("VPC705_2_selector_domain", "F(chi_D,P_D,L_cg)R", "selector/domain/projector sector", "retained_symbolic", "R5/R6/R7/R8/R9/R10/R11", "needs first-class/topological/no-stress theorem"),
        ("VPC705_3_bulk_X", "F(X_A)R", "bulk/load auxiliary fields", "operator_and_sources_not_parent_derived", "R1/R3/R4/R9/R10/R11", "needs source-free no-hair or finite-range map"),
        ("VPC705_4_higher_curvature", "f(R) or R^2 disguise", "higher-curvature metric operators", "central_open", "R3/R4/R8/R10/R11", "needs second-order restriction or coefficient map"),
        ("VPC705_5_torsion_nonmetric", "connection-induced prefactor/source transfer", "torsion/nonmetricity/connection sector", "not_parent_derived", "R0/R1/R2/R11", "needs Levi-Civita theorem or connection residual rows"),
        ("VPC705_6_boundary", "boundary/counterterm A_EH shift", "boundary/topological/counterterm sector", "not_parent_signed", "R3/R4/R7/R8/R11", "needs boundary no-hair/counterterm guard"),
        ("VPC705_7_frame_transfer", "Weyl/disformal matter coupling", "field-redefinition sector", "not_parent_signed", "R0/R1/R2/R4", "needs same-frame matter functor guard"),
        ("VPC705_8_constant_offset", "A_EH=C", "constant calibration offset", "conditional_not_claim_ready", "R1/R4/R9", "needs independent G_ref and same-frame source normalization"),
        ("VPC705_9_verdict", "all variable prefactor channels", "A_EH=1 constant", "fail_current_corpus", "all local locks", "no A_EH pass"),
    ]
    return [
        {
            "channel_id": channel_id,
            "prefactor_form": form,
            "sector": sector,
            "current_status": status,
            "affected_locks": locks,
            "minimum_to_clear": minimum,
            "valid_for_claim": "false",
            "source_paths": source_list("440_doc", "655_doc", "657_channels", "source_norm_scorecard"),
            "generated_utc": generated,
        }
        for channel_id, form, sector, status, locks, minimum in rows
    ]


def aeh_candidate_fill_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "AFR705_0_theorem_candidate",
            "A_EH",
            "A_EH=1; grad A_EH=0",
            "MISSING_NO_FCHIR_PARENT_THEOREM",
            "MISSING_PARENT_TERM_INVENTORY_OR_THEOREM_PATH",
            "false",
        ),
        (
            "AFR705_1_numeric_candidate",
            "A_EH",
            "abs(1/A_EH-1)<=epsilon_G_bound and |grad ln A_EH| bounds",
            "MISSING_AEH_NUMERIC_OR_BOUND_ROW",
            "MISSING_NUMERIC_AEH_SOURCE_PATH",
            "false",
        ),
        (
            "AFR705_2_constant_offset_candidate",
            "A_EH=C",
            "constant C absorbed into G_ref only with independent G_ref and same-frame source normalization",
            "MISSING_INDEPENDENT_GREF_AND_SOURCE_NORMALIZATION",
            "MISSING_CONSTANT_OFFSET_GUARD_PATH",
            "false",
        ),
        (
            "AFR705_3_claim_ready_fill",
            "704 DPU704_0_AEH",
            "fill A_EH row for epsilon_G and kappa-gradient gates",
            "MISSING_AEH_PARENT_VALUE_OR_THEOREM_ONE",
            "MISSING_CLAIM_READY_AEH_SOURCE_PATH",
            "false",
        ),
    ]
    return [
        {
            "fill_id": fill_id,
            "target": target,
            "formula": formula,
            "value_or_bound": value,
            "source_path": source_path,
            "valid_for_claim": valid,
            "source_paths": source_list("704_delta", "704_prefactor", "704_constant", "704_gradient"),
            "generated_utc": generated,
        }
        for fill_id, target, formula, value, source_path, valid in rows
    ]


def evaluator_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("EVAL705_0_AEH_row", "Can A_EH be filled now?", "No. 705 writes the claim-ready row schema, but the parent term inventory/source equation is still missing.", "fail_blocked", NEXT_TARGET),
        ("EVAL705_1_no_FchiR", "Can no-F(chi)R be proved now?", "Only conditionally. Every variable-prefactor channel is named, but none is parent-signed away.", "fail_blocked", NEXT_TARGET),
        ("EVAL705_2_best_next", "Best next strike?", "Inventory the parent action terms that can multiply R and classify each as absent, topological/gauge, harmless constant, or retained.", "route_selected", NEXT_TARGET),
    ]
    return [
        {
            "eval_id": eval_id,
            "question": question,
            "answer": answer,
            "result": result,
            "next_action": next_action,
            "valid_for_claim": "false",
            "source_paths": source_list("704_doc", "704_constant", "440_doc", "655_doc"),
            "generated_utc": generated,
        }
        for eval_id, question, answer, result, next_action in rows
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("CG705_0_sources", "all source files load", "source register exists check", "pass_structure", "allows checkpoint only"),
        ("CG705_1_prior_704", "704 validation clean", "704 validation has no failures", "pass_structure", "inherits clean predecessor"),
        ("CG705_2_AEH_source_row", "claim-ready A_EH source row", "MISSING_AEH_PARENT_VALUE_OR_THEOREM_ONE", "fail_blocked", "no A_EH claim"),
        ("CG705_3_no_FchiR", "no F(chi)R theorem", "MISSING_PARENT_TERM_INVENTORY", "fail_blocked", "no prefactor theorem claim"),
        ("CG705_4_gradient", "grad A_EH zero/bound", "MISSING_GRAD_AEH_VECTOR", "fail_blocked", "no kappa-gradient bound"),
        ("CG705_5_Delta_Poisson", "Delta_Poisson fill", "MISSING_NUMERIC_EPSILON_VECTOR", "fail_blocked", "no local Poisson claim"),
        ("CG705_6_local_GR", "local-GR promotion", "not reached", "fail_blocked", "no local-GR claim"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": observed,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("704_validation", "704_delta", "704_constant", "704_gradient"),
            "generated_utc": generated,
        }
        for gate_id, gate, observed, result, effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("D705_0_source_schema", "A_EH source row", "schema_written_unfilled", "claim-ready columns and acceptance conditions are explicit", NEXT_TARGET),
        ("D705_1_no_FchiR", "no-FchiR theorem", "conditional_theorem_written", "all variable-prefactor channels are named but not parent-signed", NEXT_TARGET),
        ("D705_2_candidate_fill", "A_EH fill", "not_filled", "no parent term inventory, no A_EH value, no derivative vector, no source path", NEXT_TARGET),
        ("D705_3_next", "next target", "selected", "inventory parent action terms for A_EH and classify them before another claim attempt", NEXT_TARGET),
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
            "summary_id": "S705_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "the A_EH claim-ready source row and no-FchiR theorem are now explicit, but the parent term inventory/source proof is still missing",
            "hardest_blocker": "no parent-action inventory showing every variable-prefactor channel is absent, harmless, or retained",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def has_missing_marker(row: dict[str, str]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values())


def validation_rows(source_rows, schema, no_fchir, channels, fill, evaluator, gates, decisions, summary):
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = len(validation_failures("704_validation"))
    delta_rows = read_csv(SOURCE_PATHS["704_delta"])
    aeh_still_missing = any(row.get("update_id") == "DPU704_0_AEH" and "MISSING_AEH" in row.get("value_or_bound", "") for row in delta_rows)
    schema_verdict_blocks = any(row["schema_id"] == "AEH705_6_verdict" and row["current_status"] == "fail_current_corpus" for row in schema)
    no_fchir_conditional = any(row["theorem_id"] == "NFC705_7_conditional_theorem" and row["current_status"] == "proved_as_conditional_template" for row in no_fchir)
    no_fchir_blocks = any(row["theorem_id"] == "NFC705_8_verdict" and row["current_status"] == "fail_current_corpus" for row in no_fchir)
    channel_coverage = len(channels) >= 10 and any(row["channel_id"] == "VPC705_9_verdict" for row in channels)
    fill_unfilled = any(row["fill_id"] == "AFR705_3_claim_ready_fill" and has_missing_marker(row) for row in fill)
    no_claim = all(
        row.get("valid_for_claim") != "true"
        for group in [schema, no_fchir, channels, fill, evaluator, gates, decisions, summary]
        for row in group
    )
    gates_block = all(row["valid_for_claim"] == "false" for row in gates) and any(row["result"] == "fail_blocked" for row in gates)
    scoped = all(str(path).startswith(str(ROOT)) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_count()
    checks = [
        ("V705_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V705_1_prior_704_clean", prior_failures == 0, f"704_validation_failures={prior_failures}"),
        ("V705_2_704_AEH_still_missing", aeh_still_missing, "DPU704_0_AEH remains missing"),
        ("V705_3_AEH_schema_blocks", schema_verdict_blocks, "AEH705 verdict blocks claim"),
        ("V705_4_no_FchiR_conditional_theorem_written", no_fchir_conditional, "NFC705 conditional theorem present"),
        ("V705_5_no_FchiR_not_promoted", no_fchir_blocks, "NFC705 verdict blocks claim"),
        ("V705_6_variable_prefactor_channel_coverage", channel_coverage, f"channels={len(channels)}"),
        ("V705_7_AEH_candidate_fill_unfilled", fill_unfilled, "candidate fill keeps MISSING markers"),
        ("V705_8_gates_block_claim", gates_block, f"gate_rows={len(gates)}"),
        ("V705_9_no_claim_rows_promoted", no_claim, "all generated rows valid_for_claim=false"),
        ("V705_10_next_target_selected", summary[0]["next_target"] == NEXT_TARGET and decisions[-1]["next_action"] == NEXT_TARGET, NEXT_TARGET),
        ("V705_11_outputs_scoped", scoped, "all outputs under post-checkpoint-work"),
        ("V705_12_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V705_13_status_nonclaim", "no_AEH_value" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
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


def write_doc(source_rows, schema, no_fchir, channels, fill, evaluator, gates, decisions, summary, validation) -> None:
    doc = f"""# 705 - Y5 R10 AEH Prefactor Source Row Or No FchiR Theorem

## Verdict

705 makes the next demand painfully explicit. To use the prefactor route, we need a claim-ready row for:

```text
A_EH = coefficient of R[g_obs] in the observed-frame parent action
epsilon_G = abs(1/A_EH - 1)
grad ln(kappa_eff) = - grad ln(A_EH)
```

The clean theorem route is:

```text
No F(chi,theta,X,domain) R[g_obs]
+ no Weyl/disformal frame transfer
+ no boundary/counterterm prefactor shift
=> A_EH = 1 constant
=> epsilon_G = 0 and grad(kappa_eff)=0.
```

That theorem is now written, but not parent-signed. The current corpus still lacks the parent action term inventory proving every variable-prefactor channel is absent, gauge/topological, harmless constant, or explicitly retained.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## AEH Source Row Schema

{markdown_table(schema, ["schema_id", "target", "current_status", "units", "claim_effect", "valid_for_claim"])}

## No FchiR Theorem Audit

{markdown_table(no_fchir, ["theorem_id", "clause", "current_status", "claim_effect", "valid_for_claim"])}

## Variable Prefactor Channels

{markdown_table(channels, ["channel_id", "prefactor_form", "sector", "current_status", "minimum_to_clear", "valid_for_claim"])}

## AEH Candidate Fill Row

{markdown_table(fill, ["fill_id", "target", "value_or_bound", "source_path", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator, ["eval_id", "question", "answer", "result", "next_action", "valid_for_claim"])}

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
    schema = aeh_source_schema_rows()
    no_fchir = no_fchir_theorem_rows()
    channels = variable_prefactor_channel_rows()
    fill = aeh_candidate_fill_rows()
    evaluator = evaluator_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    summary = summary_rows()
    validation = validation_rows(source_rows, schema, no_fchir, channels, fill, evaluator, gates, decisions, summary)

    write_csv(RESIDUALS / "P8_Y5_R10_705_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_705_AEH_SOURCE_ROW_SCHEMA.csv", schema, ["schema_id", "target", "definition", "required_evidence", "current_status", "units", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_705_NO_FCHIR_THEOREM_AUDIT.csv", no_fchir, ["theorem_id", "clause", "mathematical_requirement", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_705_VARIABLE_PREFACTOR_CHANNELS.csv", channels, ["channel_id", "prefactor_form", "sector", "current_status", "affected_locks", "minimum_to_clear", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_705_AEH_CANDIDATE_FILL_ROW.csv", fill, ["fill_id", "target", "formula", "value_or_bound", "source_path", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_705_EVALUATOR.csv", evaluator, ["eval_id", "question", "answer", "result", "next_action", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_705_CLAIM_GATE_EVALUATION.csv", gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_705_DECISION.csv", decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_705_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_705_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_rows, schema, no_fchir, channels, fill, evaluator, gates, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"schema_rows={len(schema)}")
    print(f"no_fchir_rows={len(no_fchir)}")
    print(f"channel_rows={len(channels)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
