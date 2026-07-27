from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_EH_prefactor_constant_theorem_conditional_kappa_gradient_bound_staged_nonclaim"
CLAIM_CEILING = "EH_prefactor_constant_or_kappa_gradient_bound_contract_only_no_AEH_value_no_epsilon_G_zero_no_Rsrc_zero_no_Delta_Poisson_fill_no_local_GR_claim"
NEXT_TARGET = "705-Y5-R10-AEH-prefactor-source-row-or-no-FchiR-theorem.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "704-Y5-R10-EH-prefactor-constant-theorem-or-kappa-gradient-bound.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

OUTPUT_PATHS = [
    DOC_PATH,
    RESIDUALS / "P8_Y5_R10_704_SOURCE_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_704_EH_PREFACTOR_FORMALIZATION.csv",
    RESIDUALS / "P8_Y5_R10_704_CONSTANT_THEOREM_AUDIT.csv",
    RESIDUALS / "P8_Y5_R10_704_KAPPA_GRADIENT_BOUND_PACK.csv",
    RESIDUALS / "P8_Y5_R10_704_DELTA_POISSON_UPDATE.csv",
    RESIDUALS / "P8_Y5_R10_704_EVALUATOR.csv",
    RESIDUALS / "P8_Y5_R10_704_CLAIM_GATE_EVALUATION.csv",
    RESIDUALS / "P8_Y5_R10_704_DECISION.csv",
    RESIDUALS / "P8_Y5_R10_704_NONCLAIM_SUMMARY.csv",
    RESIDUALS / "P8_Y5_BRR545_704_VALIDATION.csv",
]

SOURCE_PATHS = {
    "402_doc": ROOT / "402-EH-source-normalization-parent-pair.md",
    "424_doc": ROOT / "424-same-frame-EH-source-Poisson-reduction-gate.md",
    "429_doc": ROOT / "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
    "440_doc": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
    "523_doc": ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "657_doc": ROOT / "657-Y5-R10-source-normalization-family-first-real-R11-fill.md",
    "696_doc": ROOT / "696-Y5-R10-MHref-same-frame-denominator-or-BTF-product-bound-guard.md",
    "703_doc": ROOT / "703-Y5-R10-parent-action-coupling-lock-or-Rsrc-channel-zero-theorem.md",
    "703_validation": RESIDUALS / "P8_Y5_BRR545_703_VALIDATION.csv",
    "703_parent_lock": RESIDUALS / "P8_Y5_R10_703_PARENT_ACTION_COUPLING_LOCK_AUDIT.csv",
    "703_variation": RESIDUALS / "P8_Y5_R10_703_ACTION_VARIATION_CONTRACT.csv",
    "703_rsrc_zero": RESIDUALS / "P8_Y5_R10_703_RSRC_ZERO_THEOREM_AUDIT.csv",
    "703_delta": RESIDUALS / "P8_Y5_R10_703_DELTA_POISSON_UPDATE_ROW.csv",
    "702_kappa_lock": RESIDUALS / "P8_Y5_R10_702_KAPPA_GREF_LOCK_AUDIT.csv",
    "702_rsrc": RESIDUALS / "P8_Y5_R10_702_RSRC_CHANNEL_DECOMPOSITION.csv",
    "702_delta": RESIDUALS / "P8_Y5_R10_702_DELTA_POISSON_CANDIDATE_FILL.csv",
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
        "429_doc": "Ward/Bianchi kappa/source residual owner",
        "440_doc": "metric-only second-order sector reduction attempt",
        "523_doc": "Gauss/orbital source-normalization scorecard",
        "655_doc": "EH operator selection and R11 fallback",
        "657_doc": "source-normalization family first fill",
        "696_doc": "M_H_ref/G_ref circularity guard",
        "703_doc": "parent-action coupling lock predecessor",
        "703_validation": "703 validation gate",
        "703_parent_lock": "703 parent-action coupling lock audit",
        "703_variation": "703 action variation contract",
        "703_rsrc_zero": "703 R_src zero theorem audit",
        "703_delta": "703 Delta_Poisson update row",
        "702_kappa_lock": "702 kappa/Gref lock audit",
        "702_rsrc": "702 R_src channel decomposition",
        "702_delta": "702 Delta_Poisson candidate fill",
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


def prefactor_formalization_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "EHPF704_0_parent_action",
            "A_EH",
            "S_EH=(c^4/(16*pi*G_ref)) int sqrt(-g_obs) A_EH(chi,theta,X,domain) R[g_obs]",
            "A_EH is the dimensionless local EH prefactor multiplying R in the observed frame",
            "definition_for_audit",
        ),
        (
            "EHPF704_1_kappa_eff",
            "kappa_eff",
            "kappa_eff = kappa_ref/A_EH, with kappa_ref=8*pi*G_ref/c^4",
            "coefficient readout if A_EH multiplies R and matter source is in same frame",
            "conditional_formula",
        ),
        (
            "EHPF704_2_epsilon_G",
            "epsilon_G",
            "epsilon_G = abs(kappa_eff/kappa_ref - 1) = abs(1/A_EH - 1)",
            "coupling mismatch generated by a non-unit EH prefactor",
            "formula_written_value_missing",
        ),
        (
            "EHPF704_3_gradient",
            "grad_ln_kappa_eff",
            "grad ln(kappa_eff) = - grad ln(A_EH)",
            "kappa-gradient source channel is killed if A_EH is constant",
            "formula_written_bound_missing",
        ),
        (
            "EHPF704_4_source_channel",
            "T_obs_grad_kappa",
            "T_obs grad(kappa_eff) = -kappa_eff T_obs grad ln(A_EH)",
            "Ward/Bianchi source channel controlled by prefactor gradient",
            "formula_written_bound_missing",
        ),
    ]
    return [
        {
            "formalization_id": formalization_id,
            "target": target,
            "mathematical_form": form,
            "meaning": meaning,
            "current_status": status,
            "valid_for_claim": "false",
            "source_paths": source_list("402_doc", "424_doc", "429_doc", "703_parent_lock", "703_variation"),
            "generated_utc": generated,
        }
        for formalization_id, target, form, meaning, status in rows
    ]


def constant_theorem_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "CTH704_0_AEH_extraction",
            "extract A_EH from parent action",
            "read the coefficient multiplying R[g_obs] after all parent maps and field redefinitions",
            "MISSING_PARENT_AEH_EXTRACTION",
            "cannot know whether coupling is constant",
        ),
        (
            "CTH704_1_unit_prefactor",
            "A_EH=1",
            "A_EH is exactly one in the observed local branch",
            "not_parent_signed",
            "epsilon_G remains open",
        ),
        (
            "CTH704_2_no_variable_prefactor",
            "no F(chi)R/F(theta)R",
            "scalar, memory, selector, class, or domain variables do not multiply R",
            "not_parent_signed",
            "kappa gradient remains open",
        ),
        (
            "CTH704_3_no_disformal_rename",
            "no Weyl/disformal frame transfer",
            "field redefinitions do not move variable coupling from gravity into matter/source sector",
            "not_parent_signed",
            "frame/source coupling remains open",
        ),
        (
            "CTH704_4_no_boundary_shift",
            "no boundary/counterterm renormalization",
            "boundary/counterterm choices do not shift the local EH coefficient or measured source mass",
            "not_parent_signed",
            "G_ref/M_H_ref circularity remains open",
        ),
        (
            "CTH704_5_constant_offset_guard",
            "A_EH=C constant",
            "a constant C can be absorbed into G_ref only if G_ref is independently fixed and same-frame source normalization is signed",
            "conditional_not_claim_ready",
            "constant offset alone is not a Newton proof",
        ),
        (
            "CTH704_6_conditional_theorem",
            "EH prefactor constant theorem",
            "A_EH=1 constant plus no frame transfer implies epsilon_G=0 and grad(kappa_eff)=0",
            "proved_as_conditional_template",
            "theorem shape only",
        ),
        (
            "CTH704_7_verdict",
            "claim-ready constant prefactor",
            "A_EH=1 and grad A_EH=0 from parent action",
            "fail_current_corpus",
            "no epsilon_G zero claim",
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
            "source_paths": source_list("440_doc", "655_doc", "657_doc", "696_doc", "703_parent_lock"),
            "generated_utc": generated,
        }
        for theorem_id, clause, requirement, status, effect in rows
    ]


def kappa_gradient_bound_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "KGB704_0_dimensionless_gradient",
            "epsilon_kappa_grad",
            "epsilon_kappa_grad <= L_loc sup_local |grad ln kappa_eff| = L_loc sup_local |grad ln A_EH|",
            "MISSING_L_LOC_AND_GRAD_AEH_BOUND",
            "dimensionless",
            "fallback bound if constant theorem fails",
        ),
        (
            "KGB704_1_time_drift",
            "dlnG_dt",
            "abs(partial_t ln kappa_eff)=abs(partial_t ln A_EH)",
            "MISSING_TIME_DRIFT_BOUND",
            "per_time",
            "feeds Gdot/G and source-normalization rows",
        ),
        (
            "KGB704_2_radial_gradient",
            "partial_r_lnG",
            "abs(partial_r ln kappa_eff)=abs(partial_r ln A_EH)",
            "MISSING_RADIAL_GRADIENT_BOUND",
            "per_length",
            "feeds radial source hair and local Poisson residual",
        ),
        (
            "KGB704_3_range_dependence",
            "partial_lambda_lnG",
            "abs(partial_lambda ln kappa_eff)=abs(partial_lambda ln A_EH)",
            "MISSING_RANGE_DEPENDENCE_BOUND",
            "per_length_or_per_range_parameter",
            "feeds R10 alpha(lambda)",
        ),
        (
            "KGB704_4_species_dependence",
            "partial_A_lnG",
            "composition/source-label dependence of A_EH",
            "MISSING_SPECIES_DEPENDENCE_BOUND",
            "dimensionless_per_species_contrast",
            "feeds WEP/source-charge rows",
        ),
        (
            "KGB704_5_source_channel_bound",
            "T_obs_grad_kappa_channel",
            "epsilon_src_kappa <= abs(T_obs grad(kappa_eff))/(4*pi*G_ref*rho_H)",
            "MISSING_TOBS_AND_RHOH_NORMALIZATION",
            "dimensionless",
            "cannot score R_src without source normalization",
        ),
        (
            "KGB704_6_verdict",
            "claim-ready kappa-gradient bound",
            "numeric/theorem-zero bound for every derivative and normalization input",
            "fail_current_corpus",
            "dimensionless_or_channel_specific",
            "not a substitute for parent prefactor theorem yet",
        ),
    ]
    return [
        {
            "bound_id": bound_id,
            "target": target,
            "formula": formula,
            "current_status": status,
            "units": units,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("429_doc", "523_doc", "657_channels", "702_rsrc", "source_norm_scorecard"),
            "generated_utc": generated,
        }
        for bound_id, target, formula, status, units, effect in rows
    ]


def delta_update_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "DPU704_0_AEH",
            "A_EH",
            "dimensionless parent EH prefactor",
            "MISSING_AEH_PARENT_VALUE_OR_THEOREM_ONE",
            "MISSING_AEH_SOURCE_PATH",
        ),
        (
            "DPU704_1_epsilon_G",
            "epsilon_G",
            "abs(1/A_EH - 1)",
            "MISSING_EPSILON_G_VALUE_OR_ZERO_THEOREM",
            "MISSING_EPSILON_G_SOURCE_PATH",
        ),
        (
            "DPU704_2_kappa_gradient",
            "epsilon_src_kappa",
            "abs(T_obs grad(kappa_eff))/(4*pi*G_ref*rho_H)",
            "MISSING_KAPPA_GRADIENT_SOURCE_BOUND",
            "MISSING_KAPPA_GRADIENT_SOURCE_PATH",
        ),
        (
            "DPU704_3_Delta_Poisson",
            "Delta_Poisson",
            "Delta_Poisson <= epsilon_G + epsilon_src_kappa + remaining_Rsrc_channels",
            "MISSING_NUMERIC_EPSILON_VECTOR",
            "MISSING_CLAIM_READY_DELTA_POISSON_SOURCE_PATH",
        ),
    ]
    return [
        {
            "update_id": update_id,
            "target": target,
            "formula": formula,
            "value_or_bound": value,
            "source_path": source_path,
            "valid_for_claim": "false",
            "source_paths": source_list("703_delta", "703_parent_lock", "703_rsrc_zero", "702_delta"),
            "generated_utc": generated,
        }
        for update_id, target, formula, value, source_path in rows
    ]


def evaluator_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("EVAL704_0_constant", "Can A_EH=1 constant be claimed now?", "No. The formula is exact, but no parent-source row extracts A_EH or proves no F(chi)R/no frame transfer.", "fail_blocked", NEXT_TARGET),
        ("EVAL704_1_gradient", "Can the kappa-gradient channel be bounded instead?", "No. The bound shape is clear, but L_loc, grad A_EH, T_obs, and rho_H normalization are still missing.", "fail_blocked", NEXT_TARGET),
        ("EVAL704_2_best_next", "Best next strike?", "Create the A_EH source row: either parent theorem A_EH=1/no F(chi)R, or a derivative/value bound with units.", "route_selected", NEXT_TARGET),
    ]
    return [
        {
            "eval_id": eval_id,
            "question": question,
            "answer": answer,
            "result": result,
            "next_action": next_action,
            "valid_for_claim": "false",
            "source_paths": source_list("703_doc", "703_parent_lock", "703_rsrc_zero"),
            "generated_utc": generated,
        }
        for eval_id, question, answer, result, next_action in rows
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("CG704_0_sources", "all source files load", "source register exists check", "pass_structure", "allows checkpoint only"),
        ("CG704_1_prior_703", "703 validation clean", "703 validation has no failures", "pass_structure", "inherits clean predecessor"),
        ("CG704_2_AEH_value", "A_EH parent value/theorem", "MISSING_AEH_PARENT_VALUE_OR_THEOREM_ONE", "fail_blocked", "no epsilon_G claim"),
        ("CG704_3_gradient_bound", "kappa-gradient bound", "MISSING_L_LOC_AND_GRAD_AEH_BOUND", "fail_blocked", "no kappa-source bound"),
        ("CG704_4_Rsrc", "R_src zero/bound", "remaining channels unfilled", "fail_blocked", "no epsilon_src claim"),
        ("CG704_5_Delta_Poisson", "Delta_Poisson fill", "MISSING_NUMERIC_EPSILON_VECTOR", "fail_blocked", "no local Poisson claim"),
        ("CG704_6_local_GR", "PPN/R10/local-GR promotion", "not reached", "fail_blocked", "no local-GR claim"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": observed,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("703_validation", "703_parent_lock", "703_delta", "702_rsrc"),
            "generated_utc": generated,
        }
        for gate_id, gate, observed, result, effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("D704_0_prefactor_form", "A_EH formalization", "written", "variable EH prefactor now has exact coefficient, mismatch, and gradient formulas", NEXT_TARGET),
        ("D704_1_constant_theorem", "A_EH=1 constant theorem", "conditional_only", "would kill epsilon_G and T_obs grad(kappa_eff), but parent extraction is missing", NEXT_TARGET),
        ("D704_2_gradient_bound", "kappa-gradient fallback", "bound_shape_written_unfilled", "fallback needs L_loc, grad A_EH, T_obs, and rho_H source rows", NEXT_TARGET),
        ("D704_3_next", "next target", "selected", "fill the A_EH source row or prove no F(chi)R/no variable prefactor from parent action", NEXT_TARGET),
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
            "summary_id": "S704_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "A_EH is now the exact parent-action bottleneck: epsilon_G=abs(1/A_EH-1) and grad ln kappa_eff=-grad ln A_EH",
            "hardest_blocker": "no sourced parent row proves A_EH=1 constant/no F(chi)R, and no numeric derivative bound is loaded",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def has_missing_marker(row: dict[str, str]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values())


def validation_rows(source_rows, prefactor, constant, gradient, delta_update, evaluator, gates, decisions, summary):
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = len(validation_failures("703_validation"))
    parent_rows = read_csv(SOURCE_PATHS["703_parent_lock"])
    parent_still_blocked = any(row.get("lock_id") == "PAL703_8_verdict" and row.get("current_status") == "fail_current_corpus" for row in parent_rows)
    prefactor_formulas = len(prefactor) == 5 and any(row["target"] == "epsilon_G" for row in prefactor)
    conditional_theorem = any(row["theorem_id"] == "CTH704_6_conditional_theorem" and row["current_status"] == "proved_as_conditional_template" for row in constant)
    constant_blocks = any(row["theorem_id"] == "CTH704_7_verdict" and row["current_status"] == "fail_current_corpus" for row in constant)
    gradient_blocks = any(row["bound_id"] == "KGB704_6_verdict" and row["current_status"] == "fail_current_corpus" for row in gradient)
    delta_unfilled = any(row["update_id"] == "DPU704_3_Delta_Poisson" and has_missing_marker(row) for row in delta_update)
    no_claim = all(
        row.get("valid_for_claim") != "true"
        for group in [prefactor, constant, gradient, delta_update, evaluator, gates, decisions, summary]
        for row in group
    )
    gates_block = all(row["valid_for_claim"] == "false" for row in gates) and any(row["result"] == "fail_blocked" for row in gates)
    scoped = all(str(path).startswith(str(ROOT)) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_count()
    checks = [
        ("V704_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V704_1_prior_703_clean", prior_failures == 0, f"703_validation_failures={prior_failures}"),
        ("V704_2_703_parent_lock_still_blocked", parent_still_blocked, "PAL703 verdict remains fail_current_corpus"),
        ("V704_3_prefactor_formulas_written", prefactor_formulas, f"prefactor_rows={len(prefactor)}"),
        ("V704_4_constant_theorem_conditional", conditional_theorem, "CTH704 conditional theorem present"),
        ("V704_5_constant_theorem_not_promoted", constant_blocks, "CTH704 verdict blocks claim"),
        ("V704_6_gradient_bound_not_promoted", gradient_blocks, "KGB704 verdict blocks claim"),
        ("V704_7_Delta_Poisson_update_unfilled", delta_unfilled, "Delta update keeps MISSING markers"),
        ("V704_8_gates_block_claim", gates_block, f"gate_rows={len(gates)}"),
        ("V704_9_no_claim_rows_promoted", no_claim, "all generated rows valid_for_claim=false"),
        ("V704_10_next_target_selected", summary[0]["next_target"] == NEXT_TARGET and decisions[-1]["next_action"] == NEXT_TARGET, NEXT_TARGET),
        ("V704_11_outputs_scoped", scoped, "all outputs under post-checkpoint-work"),
        ("V704_12_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V704_13_status_nonclaim", "no_AEH_value" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
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


def write_doc(source_rows, prefactor, constant, gradient, delta_update, evaluator, gates, decisions, summary, validation) -> None:
    doc = f"""# 704 - Y5 R10 EH Prefactor Constant Theorem Or Kappa Gradient Bound

## Verdict

704 turns the coupling problem into one sharp variable:

```text
S_EH = (c^4/(16*pi*G_ref)) int sqrt(-g_obs) A_EH(chi,theta,X,domain) R[g_obs]
kappa_eff = kappa_ref / A_EH
epsilon_G = abs(1/A_EH - 1)
grad ln(kappa_eff) = - grad ln(A_EH)
```

So if the parent action proves `A_EH=1` constant, then both `epsilon_G=0` and the `T_obs grad(kappa_eff)` source channel vanish. If it cannot prove that, the fallback is a real kappa-gradient bound:

```text
epsilon_kappa_grad <= L_loc sup_local |grad ln A_EH|.
```

The current corpus does not yet supply the `A_EH` parent source row, no-`F(chi)R` theorem, or derivative bound. No claim is promoted.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## EH Prefactor Formalization

{markdown_table(prefactor, ["formalization_id", "target", "current_status", "valid_for_claim"])}

## Constant Theorem Audit

{markdown_table(constant, ["theorem_id", "clause", "current_status", "claim_effect", "valid_for_claim"])}

## Kappa Gradient Bound Pack

{markdown_table(gradient, ["bound_id", "target", "current_status", "units", "claim_effect", "valid_for_claim"])}

## Delta Poisson Update

{markdown_table(delta_update, ["update_id", "target", "value_or_bound", "source_path", "valid_for_claim"])}

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
    prefactor = prefactor_formalization_rows()
    constant = constant_theorem_rows()
    gradient = kappa_gradient_bound_rows()
    delta_update = delta_update_rows()
    evaluator = evaluator_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    summary = summary_rows()
    validation = validation_rows(source_rows, prefactor, constant, gradient, delta_update, evaluator, gates, decisions, summary)

    write_csv(RESIDUALS / "P8_Y5_R10_704_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_704_EH_PREFACTOR_FORMALIZATION.csv", prefactor, ["formalization_id", "target", "mathematical_form", "meaning", "current_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_704_CONSTANT_THEOREM_AUDIT.csv", constant, ["theorem_id", "clause", "mathematical_requirement", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_704_KAPPA_GRADIENT_BOUND_PACK.csv", gradient, ["bound_id", "target", "formula", "current_status", "units", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_704_DELTA_POISSON_UPDATE.csv", delta_update, ["update_id", "target", "formula", "value_or_bound", "source_path", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_704_EVALUATOR.csv", evaluator, ["eval_id", "question", "answer", "result", "next_action", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_704_CLAIM_GATE_EVALUATION.csv", gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_704_DECISION.csv", decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_704_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_704_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_rows, prefactor, constant, gradient, delta_update, evaluator, gates, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"prefactor_rows={len(prefactor)}")
    print(f"constant_rows={len(constant)}")
    print(f"gradient_rows={len(gradient)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
