from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
OUT = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_kappa_alpha_pressure_envelope_and_charge_topology_next_proof.py"
DOC_PATH = ROOT / "641-Y5-R10-kappa-alpha-pressure-envelope-and-charge-topology-next-proof.md"

STATUS = "Y5_R10_kappa_alpha_pressure_envelope_staged_charge_unit_Maxwell_proofs_still_open_nonclaim"
CLAIM_CEILING = "charge_unit_Maxwell_attempt_and_kappa_alpha_pressure_envelope_only_no_numeric_score_no_EM_R10_WEP_clock_PPN_or_local_GR_pass"
NEXT_TARGET = "642-Y5-R10-charge-unit-Maxwell-proof-extension-or-kappa-alpha-pressure-runner.md"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_register_rows() -> list[dict[str, object]]:
    sources = [
        ("S641_0", "checkpoint_640_doc", ROOT / "640-Y5-R10-charge-topology-or-kappa-alpha-numeric-prior.md", "prior checkpoint verdict: topology route conditional, current corpus blocked"),
        ("S641_1", "validation_640", OUT / "P8_Y5_BRR545_640_VALIDATION.csv", "prior checkpoint validation input"),
        ("S641_2", "charge_topology_ladder_640", OUT / "P8_Y5_R10_640_CHARGE_TOPOLOGY_LADDER.csv", "rung-level blocker ledger for kappa_alpha zero theorem"),
        ("S641_3", "maxwell_gate_640", OUT / "P8_Y5_R10_640_MAXWELL_LIMIT_GATE.csv", "Maxwell-equation gate from prior checkpoint"),
        ("S641_4", "kappa_alpha_prior_template_640", OUT / "P8_Y5_R10_640_KAPPA_ALPHA_PRIOR_TEMPLATE.csv", "prior allowed/nonallowed kappa_alpha templates"),
        ("S641_5", "local_bound_matrix_639", OUT / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv", "cross-arena local bound matrix used for reaction-map slots"),
        ("S641_6", "andersen_charge_contract", ROOT / "source-intake" / "external_papers" / "Andersen_2026_phase_current_CHARGE_CONTRACT.csv", "external EM/gravitational-relic paper intake: phase/current charge-contract audit"),
        ("S641_7", "andersen_charge_relevance", ROOT / "source-intake" / "external_papers" / "Andersen_2026_HFGW_EM_charge_relevance_AUDIT.csv", "external EM/gravitational-relic relevance audit"),
        ("S641_8", "andersen_charge_phase_decision", ROOT / "source-intake" / "external_papers" / "Andersen_2026_charge_phase_DECISION.csv", "external EM/gravitational-relic decision ledger"),
        ("S641_9", "boundary_current_charge_attempt_287", ROOT / "287-boundary-current-charge-owner-attempt.md", "older MTS boundary-current charge-owner attempt"),
        ("S641_10", "generator_script_641", SCRIPT_PATH, "this checkpoint generator"),
    ]
    rows = []
    for source_id, label, path, role in sources:
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "path": rel(path),
                "exists": bool_text(path.exists()),
                "role": role,
                "confidence": "local_source_exists" if path.exists() else "missing_blocker",
                "valid_for_claim": "false",
            }
        )
    return rows


def charge_unit_next_proof_rows() -> list[dict[str, object]]:
    return [
        {
            "clause_id": "CUN641_0_compact_phase",
            "proof_obligation": "theta_Q is a compact parent phase theta_Q ~ theta_Q + 2pi with a real parent shift symmetry",
            "best_current_status": "necessary_but_not_sufficient",
            "attempted_derivation": "A compact phase can encode sign/orientation and makes an integer/winding route possible, but by itself it does not fix the observed charge unit.",
            "blocking_gap": "no parent theorem maps the MTS phase to the observed EM charge unit e",
            "effect_on_kappa_alpha": "supports possible topological route but does not prove kappa_alpha_zero",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CUN641_1_noether_current",
            "proof_obligation": "J_Q^mu is the Noether/Ward/topological current of theta_Q and obeys nabla_mu J_Q^mu = 0",
            "best_current_status": "conditional_support",
            "attempted_derivation": "The boundary-current programme can support conserved relative charge currents if the parent action has the right symmetry.",
            "blocking_gap": "current conservation is not yet identified with the EM current in a normalized observed coframe",
            "effect_on_kappa_alpha": "conservation alone does not make alpha_EM quotient-invariant",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CUN641_2_charge_unit",
            "proof_obligation": "Q/e = n or Q/Q_star = n/k follows from winding number, index, level, or boundary-current theorem",
            "best_current_status": "failed_current_corpus",
            "attempted_derivation": "The most scrutiny-safe route is to make charge a quantized topological readout rather than a smooth fitted scalar.",
            "blocking_gap": "no level/index/winding theorem fixes e, Q_star, or k against the measured charge unit",
            "effect_on_kappa_alpha": "this is the hard blocker: without it alpha_EM can still vary under Xhat",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CUN641_3_gauge_kinetic_normalization",
            "proof_obligation": "the gauge kinetic coefficient and fine-structure normalization are fixed by the same parent level/readout",
            "best_current_status": "not_derived",
            "attempted_derivation": "If the gauge kinetic coefficient is a topological level, then local smooth Xhat motion would not move alpha_EM.",
            "blocking_gap": "no parent-signed level or quotient-normalized Maxwell coefficient exists in the corpus",
            "effect_on_kappa_alpha": "blocks theorem zero and blocks numeric alpha pressure score",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CUN641_4_representative_silence",
            "proof_obligation": "smooth local changes in Xhat are vertical/gauge representatives and cannot change the topological charge sector",
            "best_current_status": "conditional_only",
            "attempted_derivation": "If charge and alpha_EM live only on the quotient/topological sector, D_v alpha_EM = 0 for vertical local representatives.",
            "blocking_gap": "the actual vertical generator and matter/gauge readout are not parent-signed for EM",
            "effect_on_kappa_alpha": "would prove kappa_alpha_zero only after CUN641_2 and CUN641_3 close",
            "valid_for_claim": "false",
        },
    ]


def maxwell_normalization_next_proof_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "MN641_0_Gauss",
            "required_result": "div E = rho/epsilon0 or a quotient-normalized equivalent",
            "proof_attempt_status": "proof_extension_target",
            "current_blocker": "charge density, observed coframe, and epsilon0 normalization are not derived from the parent variables",
            "why_it_matters": "Coulomb-like pressure is not enough to identify a full EM field",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "MN641_1_no_monopole",
            "required_result": "div B = 0 or a topological magnetic-sector constraint",
            "proof_attempt_status": "proof_extension_target",
            "current_blocker": "magnetic sector is not topologically tied to the same charge/readout branch",
            "why_it_matters": "without it the vector field could be an analogy rather than Maxwell EM",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "MN641_2_Faraday",
            "required_result": "curl E + partial_t B = 0",
            "proof_attempt_status": "proof_extension_target",
            "current_blocker": "no parent two-form/Bianchi identity has been mapped into observed EM units",
            "why_it_matters": "needed for gauge dynamics and spectroscopic consistency",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "MN641_3_Ampere_Maxwell",
            "required_result": "curl B - partial_t E = J",
            "proof_attempt_status": "proof_extension_target",
            "current_blocker": "Noether/boundary current is not yet the normalized Maxwell source current",
            "why_it_matters": "needed to connect conserved charge current to propagating EM field",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "MN641_4_Lorentz_force",
            "required_result": "matter readout gives q(E + v x B) in the observed coframe",
            "proof_attempt_status": "proof_extension_target",
            "current_blocker": "ordinary matter coupling and coframe readout are not derived without a hidden material marker",
            "why_it_matters": "needed before alpha_EM can enter the constants ledger as a derived structural constant",
            "valid_for_claim": "false",
        },
    ]


def kappa_alpha_pressure_envelope_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": "KAE641_0_theorem_zero",
            "branch_type": "topological_zero_target",
            "normalized_abs_kappa_alpha_factor": "0",
            "physical_kappa_alpha": "blocked_until_charge_unit_and_Maxwell_normalization_proofs_close",
            "Xhat_unit": "UNDEFINED_NORMALIZED_UNIT",
            "tau_map_status": "missing",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "use": "desired theorem branch only; not currently claimable",
        },
        {
            "branch_id": "KAE641_1_unit_response",
            "branch_type": "symbolic_pressure_probe",
            "normalized_abs_kappa_alpha_factor": "1",
            "physical_kappa_alpha": "one_normalized_unit_response_not_a_measured_value",
            "Xhat_unit": "UNDEFINED_NORMALIZED_UNIT",
            "tau_map_status": "missing",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "use": "sensitivity plumbing only if a later runner needs to see sign and arena response shape",
        },
        {
            "branch_id": "KAE641_2_decade_down",
            "branch_type": "symbolic_pressure_probe",
            "normalized_abs_kappa_alpha_factor": "0.1",
            "physical_kappa_alpha": "one_decade_below_normalized_unit_response_not_a_measured_value",
            "Xhat_unit": "UNDEFINED_NORMALIZED_UNIT",
            "tau_map_status": "missing",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "use": "checks whether future bounds are catastrophically sensitive to small nonzero alpha response",
        },
        {
            "branch_id": "KAE641_3_decade_up",
            "branch_type": "symbolic_pressure_probe",
            "normalized_abs_kappa_alpha_factor": "10",
            "physical_kappa_alpha": "one_decade_above_normalized_unit_response_not_a_measured_value",
            "Xhat_unit": "UNDEFINED_NORMALIZED_UNIT",
            "tau_map_status": "missing",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "use": "stress-tests future runner acceptance gates without pretending a physical value is known",
        },
        {
            "branch_id": "KAE641_4_bound_saturating",
            "branch_type": "future_diagnostic_slot",
            "normalized_abs_kappa_alpha_factor": "MISSING_BOUND_NORMALIZATION",
            "physical_kappa_alpha": "requires_arena_tau_sensitivities_and_Xhat_units",
            "Xhat_unit": "UNDEFINED_NORMALIZED_UNIT",
            "tau_map_status": "missing",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "use": "not available until at least one local bound can be projected into kappa_alpha units",
        },
    ]


def cross_arena_reaction_matrix_rows() -> list[dict[str, object]]:
    return [
        {
            "arena_id": "R0_R1_WEP",
            "observable": "composition-dependent acceleration eta_AB",
            "bound_input_status": "numeric_bound_available_from_639",
            "reaction_expression": "eta_AB ~ tau_WEP beta_source sum_i[(S_Ai - S_Bi) kappa_i]",
            "kappa_alpha_role": "enters only through composition alpha sensitivities and source/test-body EM binding response",
            "missing_for_score": "composition sensitivities S_A_alpha, source normalization beta_source, tau_WEP, Xhat unit",
            "prediction_numeric_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "R2_clocks",
            "observable": "clock redshift or clock-comparison drift",
            "bound_input_status": "numeric_bound_available_from_639",
            "reaction_expression": "delta nu_ab/nu_ab ~ tau_clock (K_a_alpha - K_b_alpha) kappa_alpha",
            "kappa_alpha_role": "direct if clock sensitivities to alpha_EM are supplied",
            "missing_for_score": "clock sensitivity pair K_a_alpha,K_b_alpha, tau_clock, Xhat unit, sign convention",
            "prediction_numeric_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "EM_spectra",
            "observable": "spectroscopic alpha_EM stability and atomic transition shifts",
            "bound_input_status": "source_slot_open",
            "reaction_expression": "delta alpha/alpha ~ tau_EM kappa_alpha Delta Xhat",
            "kappa_alpha_role": "primary alpha-pressure channel if theorem zero fails",
            "missing_for_score": "selected dataset, sensitivity coefficients, tau_EM, Delta Xhat mapping",
            "prediction_numeric_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "R10_short_range",
            "observable": "Yukawa alpha(lambda) or short-range inverse-square residual",
            "bound_input_status": "bound curve/anchor branch exists but local prediction still symbolic",
            "reaction_expression": "alpha_R10(lambda) ~ tau_R10 beta_source beta_test c_eff(lambda)",
            "kappa_alpha_role": "indirect through source normalization and EM binding content, not a standalone solution",
            "missing_for_score": "Z/lambda/tau_R10, body sensitivities, parent c_eff normalization",
            "prediction_numeric_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "PPN_Gdot_orbital",
            "observable": "gamma-1, beta-1, Gdot/G, orbital residual vectors",
            "bound_input_status": "arena ledgers exist but no alpha-only projection",
            "reaction_expression": "PPN residuals depend on metric/coframe/source-normalization operators, not only kappa_alpha",
            "kappa_alpha_role": "secondary consistency pressure; cannot repair local GR by itself",
            "missing_for_score": "metric-sector operator coefficients, observed-G normalization, local screening/descent map",
            "prediction_numeric_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def scoreability_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "SG641_0_charge_unit",
            "required_input": "charge unit/topological level theorem",
            "current_status": "missing_parent_theorem",
            "blocks": "kappa_alpha_zero_claim",
            "score_allowed": "false",
        },
        {
            "gate_id": "SG641_1_Maxwell_normalization",
            "required_input": "Maxwell equations and gauge kinetic normalization in observed coframe",
            "current_status": "not_derived",
            "blocks": "EM_claim_and_alpha_EM_constants_ledger",
            "score_allowed": "false",
        },
        {
            "gate_id": "SG641_2_Xhat_unit",
            "required_input": "physical unit for Xhat motion that defines kappa_alpha",
            "current_status": "undefined",
            "blocks": "numeric_kappa_alpha_prior",
            "score_allowed": "false",
        },
        {
            "gate_id": "SG641_3_tau_maps",
            "required_input": "arena projection maps tau_R10, tau_WEP, tau_clock, tau_EM",
            "current_status": "missing",
            "blocks": "cross_arena_score",
            "score_allowed": "false",
        },
        {
            "gate_id": "SG641_4_sensitivities",
            "required_input": "composition and clock alpha sensitivities",
            "current_status": "missing",
            "blocks": "WEP_clock_alpha_pressure_score",
            "score_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D641_0",
            "if_condition": "charge_unit and Maxwell normalization proofs close",
            "then_target": "promote kappa_alpha=0 theorem branch and check disformal/current residual cleanup",
            "current_truth": "false",
            "selected_next": "false",
            "claim_ceiling": CLAIM_CEILING,
        },
        {
            "decision_id": "D641_1",
            "if_condition": "proof route remains open or blocked",
            "then_target": NEXT_TARGET,
            "current_truth": "true",
            "selected_next": "true",
            "claim_ceiling": CLAIM_CEILING,
        },
    ]


def next_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "NC641_0",
            "next_target": NEXT_TARGET,
            "work_item": "Try one more parent-level charge-unit theorem: compact phase plus boundary current plus level/index map.",
            "acceptance_condition": "A sourced equation fixes Q/e or Q/Q_star without a fitted EM material marker.",
            "fallback_if_failed": "keep alpha branch finite and nonclaim; use pressure runner only for sensitivity.",
        },
        {
            "contract_id": "NC641_1",
            "next_target": NEXT_TARGET,
            "work_item": "Extend Maxwell normalization derivation from two-form/Bianchi/current descent rather than Coulomb analogy.",
            "acceptance_condition": "Gauss, no-monopole, Faraday, Ampere-Maxwell, and Lorentz readout are each parent-mapped.",
            "fallback_if_failed": "do not treat external gravitational-relic EM analogy as MTS EM derivation.",
        },
        {
            "contract_id": "NC641_2",
            "next_target": NEXT_TARGET,
            "work_item": "If proof route stays blocked, define Xhat unit and tau maps before any kappa_alpha numeric scan.",
            "acceptance_condition": "at least one arena has sourced tau, sensitivities, units, and a numeric prediction.",
            "fallback_if_failed": "no EM/R10/WEP/clock/PPN claim; keep only symbolic pressure ledger.",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "kappa_alpha_zero_claim": "false",
            "numeric_score_allowed": "false",
            "strongest_positive_result": "the pressure problem is now localized: the missing coupling is specifically charge-unit/topological-level plus Maxwell/gauge normalization, not a vague EM intuition gap",
            "hardest_blocker": "no parent-signed theorem fixes alpha_EM as quotient/topological rather than smooth Xhat-responsive",
            "next_target": NEXT_TARGET,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    charge_rows: list[dict[str, object]],
    maxwell_rows: list[dict[str, object]],
    envelope_rows: list[dict[str, object]],
    reaction_rows: list[dict[str, object]],
    score_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V641_0_source_paths_exist", all(row["exists"] == "true" for row in source_rows), "all cited local source paths must exist"))

    prior_validation = OUT / "P8_Y5_BRR545_640_VALIDATION.csv"
    prior_rows = read_csv(prior_validation)
    checks.append(("V641_1_prior_640_validation_clean", all(row.get("result") == "pass" for row in prior_rows), "640 validation remains clean"))

    checks.append(("V641_2_charge_unit_still_blocks_claim", any(row["best_current_status"] in {"failed_current_corpus", "not_derived"} for row in charge_rows), "charge-unit/gauge normalization blockers are explicit"))
    checks.append(("V641_3_charge_rows_nonclaim", all(row["valid_for_claim"] == "false" for row in charge_rows), "no charge proof row is claim-valid"))
    checks.append(("V641_4_maxwell_rows_nonclaim", all(row["valid_for_claim"] == "false" for row in maxwell_rows), "no Maxwell gate is claim-valid"))
    checks.append(("V641_5_pressure_envelope_nonclaim", all(row["valid_for_claim"] == "false" and row["numeric_ready"] == "false" for row in envelope_rows), "pressure envelope remains symbolic/nonclaim"))
    checks.append(("V641_6_reaction_matrix_nonclaim", all(row["prediction_numeric_ready"] == "false" and row["valid_for_claim"] == "false" for row in reaction_rows), "no cross-arena prediction is scored"))
    checks.append(("V641_7_score_gates_closed", all(row["score_allowed"] == "false" for row in score_rows), "all score gates stay closed"))
    checks.append(("V641_8_summary_nonclaim", summary_rows[0]["numeric_score_allowed"] == "false" and summary_rows[0]["kappa_alpha_zero_claim"] == "false", "summary does not overclaim"))

    fw = ROOT.parent / "formalization-workbench"
    cutoff = datetime(2026, 5, 31, 14, 42, 0).timestamp()
    changed_after_cutoff = 0
    if fw.exists():
        for path in fw.rglob("*"):
            if path.is_file() and path.stat().st_mtime > cutoff:
                changed_after_cutoff += 1
    checks.append(("V641_9_formalization_workbench_unchanged", changed_after_cutoff == 0, f"formalization files changed after cutoff: {changed_after_cutoff}"))
    checks.append(("V641_10_next_target_selected", summary_rows[0]["next_target"] == NEXT_TARGET, "next target is written into the nonclaim summary"))

    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now_iso(),
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("|", "\\|").replace("\n", " ")
            values.append(text)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    source_rows: list[dict[str, object]],
    charge_rows: list[dict[str, object]],
    maxwell_rows: list[dict[str, object]],
    envelope_rows: list[dict[str, object]],
    reaction_rows: list[dict[str, object]],
    score_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    contract: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 641 Y5/R10 Kappa-Alpha Pressure Envelope and Charge-Topology Next Proof",
        "",
        "## Verdict",
        "",
        f"- Status: `{STATUS}`",
        f"- Claim ceiling: `{CLAIM_CEILING}`",
        "- Result: the route is sharper but still non-claim. The missing coupling has been localized to a charge-unit/topological-level theorem plus Maxwell/gauge normalization.",
        "- `kappa_alpha = 0` is not proved. The finite branch is allowed only as symbolic pressure plumbing until `Xhat` units, arena `tau` maps, and sensitivity coefficients are sourced.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["source_id", "label", "path", "exists", "role"]),
        "",
        "## Charge Unit Next Proof",
        "",
        markdown_table(charge_rows, ["clause_id", "best_current_status", "proof_obligation", "blocking_gap", "effect_on_kappa_alpha"]),
        "",
        "## Maxwell Normalization Next Proof",
        "",
        markdown_table(maxwell_rows, ["gate_id", "required_result", "proof_attempt_status", "current_blocker", "why_it_matters"]),
        "",
        "## Kappa Alpha Pressure Envelope",
        "",
        "These rows are normalized pressure probes only. They are deliberately not physical `kappa_alpha` values because the `Xhat` unit and arena maps are still missing.",
        "",
        markdown_table(envelope_rows, ["branch_id", "branch_type", "normalized_abs_kappa_alpha_factor", "physical_kappa_alpha", "numeric_ready", "valid_for_claim", "use"]),
        "",
        "## Cross Arena Reaction Matrix",
        "",
        markdown_table(reaction_rows, ["arena_id", "observable", "bound_input_status", "reaction_expression", "kappa_alpha_role", "missing_for_score"]),
        "",
        "## Scoreability Gate",
        "",
        markdown_table(score_rows, ["gate_id", "required_input", "current_status", "blocks", "score_allowed"]),
        "",
        "## Decision",
        "",
        markdown_table(decision, ["decision_id", "if_condition", "then_target", "current_truth", "selected_next"]),
        "",
        "## Next Contract",
        "",
        markdown_table(contract, ["contract_id", "work_item", "acceptance_condition", "fallback_if_failed"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["check_id", "result", "detail"]),
        "",
        "## Interpretation",
        "",
        "- This is not grim in the vague sense; it is now specific. The theory does not merely need a better alpha fit, it needs a parent reason why EM charge/gauge normalization is quotient-fixed or else a finite coupling with sourced arena maps.",
        "- The cleanest win remains the theorem-zero route: charge as a topological/level readout makes smooth local `Xhat` motion invisible to `alpha_EM`.",
        "- If that theorem does not close, the honest next move is a finite-coupling pressure runner, but it must stay non-claim until `Xhat`, `tau`, composition, and clock sensitivities are real inputs.",
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(summary, ["status", "kappa_alpha_zero_claim", "numeric_score_allowed", "hardest_blocker", "next_target"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    charge_rows = charge_unit_next_proof_rows()
    maxwell_rows = maxwell_normalization_next_proof_rows()
    envelope_rows = kappa_alpha_pressure_envelope_rows()
    reaction_rows = cross_arena_reaction_matrix_rows()
    score_rows = scoreability_gate_rows()
    decision = decision_rows()
    contract = next_contract_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, charge_rows, maxwell_rows, envelope_rows, reaction_rows, score_rows, summary)

    write_csv(OUT / "P8_Y5_R10_641_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_641_CHARGE_UNIT_NEXT_PROOF.csv", charge_rows)
    write_csv(OUT / "P8_Y5_R10_641_MAXWELL_NORMALIZATION_NEXT_PROOF.csv", maxwell_rows)
    write_csv(OUT / "P8_Y5_R10_641_KAPPA_ALPHA_PRESSURE_ENVELOPE.csv", envelope_rows)
    write_csv(OUT / "P8_Y5_R10_641_CROSS_ARENA_REACTION_MATRIX.csv", reaction_rows)
    write_csv(OUT / "P8_Y5_R10_641_SCOREABILITY_GATE.csv", score_rows)
    write_csv(OUT / "P8_Y5_BRR545_641_DECISION.csv", decision)
    write_csv(OUT / "P8_Y5_R10_641_NEXT_CONTRACT.csv", contract)
    write_csv(OUT / "P8_Y5_R10_641_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_BRR545_641_VALIDATION.csv", validation)
    write_doc(source_rows, charge_rows, maxwell_rows, envelope_rows, reaction_rows, score_rows, decision, contract, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote_doc={DOC_PATH}")
    print(f"wrote_csv_dir={OUT}")
    print(f"validation_rows={len(validation)}")
    print(f"validation_failures={len(failures)}")
    print(f"status={STATUS}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for row in failures:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
