from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def missing(value: object) -> bool:
    text = str(value or "").strip()
    return text == "" or text.upper().startswith("MISSING") or text.startswith("FILL_")


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def path_exists(path_text: str) -> bool:
    text = str(path_text or "").strip()
    if missing(text):
        return False
    if text in {"REFERENCE_ONLY", "POST_READOUT", "ALGEBRA_ONLY", "FORBIDDEN"}:
        return False
    return source_path(text).exists()


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(col, "")) for col in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1014_0_1013_next", "source-intake/mts_residuals/P8_Y5_R10_1013_NEXT_TARGET.csv", "derive [d,Pi_M]J_H=0", "1013 handoff target."),
        ("SRC1014_1_1013_vector", "source-intake/mts_residuals/P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv", "OBS1013_1_PiM_commutator", "prior measured-GM obstruction vector."),
        ("SRC1014_2_1013_decision", "source-intake/mts_residuals/P8_Y5_R10_1013_DECISION_LEDGER.csv", "DEC1013_2_next_commutator", "prior commutator decision."),
        ("SRC1014_3_commutator_gate", "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_GATE.csv", "PC521_0_product_rule", "PiM commutator/product-rule gate."),
        ("SRC1014_4_pim_radial_input", "source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv", "PI521_1_commutator_profile", "PiM radial bound input schema."),
        ("SRC1014_5_pim_fill", "source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv", "PIF537_1_I_commutator", "PiM coefficient fill template."),
        ("SRC1014_6_numeric_audit", "source-intake/mts_residuals/P8_Y5_PIM_NUMERIC_INPUT_AUDIT.csv", "AUD536_5", "numeric input audit."),
        ("SRC1014_7_top_conditions", "source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv", "TC500_3_Hilbert_equality", "topological route conditions."),
        ("SRC1014_8_top_clause", "source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_PARENT_CLAUSE_ATTEMPT.csv", "TP500_3_Hilbert_equality_gate", "topological parent clause."),
        ("SRC1014_9_top_failure", "source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_FAILURE_ANALYSIS.csv", "F500_0_conserved_wrong_object", "topological route failure analysis."),
        ("SRC1014_10_top_certificate", "source-intake/mts_residuals/P8_Y5_PIM_TOPO_EQUALITY_CERTIFICATE.csv", "PTEC534_5_commutator_zero", "topological equality certificate."),
        ("SRC1014_11_top_gates", "source-intake/mts_residuals/P8_Y5_PIM_TOPO_EQUALITY_ACCEPTANCE_GATES.csv", "AG534_2_commutator_or_bound", "topological equality acceptance gates."),
        ("SRC1014_12_PiM_stress", "source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv", "PV2_Hodge_DeWitt_metric_dependence_retained", "projector variation stress contract."),
        ("SRC1014_13_PiM_algebra", "source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv", "PM6_flux_closure_requires_Ward_or_Euler", "PiM algebra contract."),
        ("SRC1014_14_commutator_template", "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_NUMERIC_INPUT_TEMPLATE.csv", "MISSING_I_COMMUTATOR", "current commutator input template."),
        ("SRC1014_15_commutator_eval", "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_EVALUATOR.csv", "not_computed_missing_numeric_inputs", "current commutator evaluator status."),
    ]
    rows = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": path_text,
                "exists": str(path.exists()).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "generated_utc": stamp(),
            }
        )
    return rows


def commutator_theorem_rows() -> list[dict[str, str]]:
    rows = [
        ("PCT1014_0_product_rule", "full projected-current product rule", "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H", "active_obstruction", "commutator term must be zero/bounded"),
        ("PCT1014_1_fixed_topology", "fixed topological charge map", "Pi_M J=ell_M(J) omega_M_top with d omega_M_top=0 and delta_g Pi_M=0", "conditional_not_parent_derived", "topological route not parent-certified"),
        ("PCT1014_2_commutator_zero", "commutator zero", "[d,Pi_M]J_H=0 if Pi_M is fixed/covariantly constant on source-current space", "not_derived_bound_template_required", "I_commutator remains unfilled"),
        ("PCT1014_3_Hilbert_equality", "topological current equals observed Hilbert projected current", "Pi_M J_H = J_M_top + dB_zero with integral_boundary dB_zero=0", "not_derived_key_blocker", "closed topological current can be the wrong object"),
        ("PCT1014_4_Hodge_route_retained", "Hodge/DeWitt metric projector variation retained", "delta_g Pi_H(g), delta chi_D, delta n_mu, delta G_B all varied or bounded", "retained_if_used", "projector stress maps to PPN/R11 rows"),
        ("PCT1014_5_no_readout_mask", "post-readout masks forbidden", "Pi_read only acts after theorem or residual scoring, not inside parent variation", "policy_pass_theorem_open", "policy is active but theorem still open"),
        ("PCT1014_6_no_closure_from_algebra", "projector algebra is not flux closure", "Pi_M^2=Pi_M does not imply d(Pi_M J_H)=0", "no_closure_promotion", "separate Ward/Hamiltonian/topological/Euler equation required"),
        ("PCT1014_7_verdict", "derive [d,Pi_M]J_H=0 and delta Pi_M stress silence", "PCT1014_0 through PCT1014_6 all parent-signed or numerically bounded", "fail_current_claim", "Newton/source-normalization/local-GR cannot reopen"),
    ]
    return [
        {
            "clause_id": row[0],
            "claim_piece": row[1],
            "mathematical_form": row[2],
            "current_status": row[3],
            "failure_if_missing": row[4],
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for row in rows
    ]


def route_split_rows() -> list[dict[str, str]]:
    rows = [
        ("PRS1014_0_topological_metric_independent", "topological", "delta_g Pi_M=0 and d omega_M_top=0", "conditional_pass_if_topological_not_Hodge", "still needs Hilbert equality and calibration", "false"),
        ("PRS1014_1_topological_Hilbert_equality", "topological", "Pi_M J_H = J_M_top + dB_zero", "fail_open", "main conserved-wrong-object blocker", "false"),
        ("PRS1014_2_topological_extra_projection", "topological", "Pi_M dJ_extra=0", "fail_open", "extra channels still feed mu_extra/radial source hair", "false"),
        ("PRS1014_3_Hodge_metric_projector", "Hodge/DeWitt", "delta_g Pi_H(g) retained", "retained_if_used", "requires projector-stress coefficient/PPN map", "false"),
        ("PRS1014_4_post_readout_mask", "forbidden", "Pi_M chosen after orbit/readout", "forbidden_as_derivation", "no derivation credit; closure-only if used", "false"),
        ("PRS1014_5_reference_zero", "forbidden", "reference row sets R_eq=I_commutator=B_zero=T_PiM=0", "reference_not_MTS_evidence", "cannot score current branch", "false"),
    ]
    return [
        {
            "route_id": row[0],
            "route_type": row[1],
            "condition": row[2],
            "current_status": row[3],
            "meaning": row[4],
            "valid_for_claim": row[5],
            "generated_utc": stamp(),
        }
        for row in rows
    ]


def coefficient_rows() -> list[dict[str, str]]:
    rows = [
        ("PCC1014_0_R_eq_integral", "R_eq_integral", "finite-shell integral of Pi_M J_H - J_M_top - dB_zero", "MISSING_R_EQ_INTEGRAL", "dimensionless_after_MHref_normalization", "R4;R9;R11", "source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv"),
        ("PCC1014_1_I_commutator", "I_commutator", "finite-annulus integral of [d,Pi_M]J_H", "MISSING_I_COMMUTATOR", "GM_flux_or_dimensionless_after_Meff_normalization", "R4;R7;R9;R10;R11", "source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv"),
        ("PCC1014_2_B_zero_flux", "B_zero_flux", "exact/reference/boundary improvement flux through compact linked boundary", "MISSING_B_ZERO_FLUX", "GM_flux_or_dimensionless", "R4;R7;R8;R9;R11", "source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv"),
        ("PCC1014_3_projector_stress_beta_equiv", "projector_stress_beta_equiv", "weak-field/PPN equivalent of metric stress from projector variation", "MISSING_PROJECTOR_STRESS_MAP", "PPN_or_operator_units_required", "R3;R4;R5;R6;R7;R8;R10;R11", "source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv"),
        ("PCC1014_4_Delta_PiM", "Delta_PiM", "projector-ownership/variation residual in measured source flux", "MISSING_DELTA_PIM", "GM_flux_or_dimensionless", "R4;R7;R9;R10;R11", "source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv"),
        ("PCC1014_5_epsilon_radial_Meff", "epsilon_radial_Meff", "M_eff_ref^-1 int_A[-Pi_M dJ_extra+[d,Pi_M]J_H+A_parent]", "MISSING_EPSILON_RADIAL_MEFF", "dimensionless", "R4;R10;R11", "source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv"),
    ]
    return [
        {
            "coefficient_id": row[0],
            "quantity": row[1],
            "definition": row[2],
            "value_or_theorem": row[3],
            "units": row[4],
            "affected_rows": row[5],
            "source_path": row[6],
            "current_status": "retained_unfilled",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for row in rows
    ]


def evaluate_coefficient(row: dict[str, str]) -> dict[str, str]:
    reasons: list[str] = []
    if not path_exists(row["source_path"]):
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if missing(row["value_or_theorem"]):
        reasons.append("MISSING_VALUE_OR_THEOREM")
    if missing(row["units"]):
        reasons.append("MISSING_UNITS")
    if row["current_status"] != "derived_zero" and row["current_status"] != "numeric_bound":
        reasons.append("RETAINED_UNFILLED_BLOCKS_CLAIM")
    if not flag(row["valid_for_claim"]):
        reasons.append("VALID_FOR_CLAIM_FALSE")
    claim_allowed = not reasons and flag(row["valid_for_claim"])
    return {
        "runner_id": row["coefficient_id"].replace("PCC", "PCR"),
        "coefficient_id": row["coefficient_id"],
        "quantity": row["quantity"],
        "verdict": "PASS_PIM_COMMUTATOR_BOUND_ROW" if claim_allowed else "RETAINED_NONCLAIM_PIM_COMMUTATOR_BOUND_ROW",
        "score_ready": "false",
        "claim_allowed": str(claim_allowed).lower(),
        "valid_for_claim": str(claim_allowed).lower(),
        "failure_reasons": ";".join(reasons),
        "generated_utc": stamp(),
    }


def runner_rows(coefficients: list[dict[str, str]]) -> list[dict[str, str]]:
    return [evaluate_coefficient(row) for row in coefficients]


def claim_gate_rows(theorem: list[dict[str, str]], routes: list[dict[str, str]], runner: list[dict[str, str]]) -> list[dict[str, str]]:
    theorem_failed = any(row["clause_id"] == "PCT1014_7_verdict" and row["current_status"] == "fail_current_claim" for row in theorem)
    runner_nonclaim = all(not flag(row["claim_allowed"]) for row in runner)
    route_nonclaim = all(not flag(row["valid_for_claim"]) for row in routes)
    gates = [
        ("CG1014_0_commutator_zero", "[d,Pi_M]J_H=0 is derived", "false", "fixed topological charge map/Hilbert equality is not parent-signed"),
        ("CG1014_1_projector_stress", "delta Pi_M stress is absent or below bounds", "false", "Hodge/domain/projector variation stress is retained/unfilled"),
        ("CG1014_2_topological_route", "topological Pi_M route closes measured source flux", "false", "closed topological current is not proved equal to Pi_M J_H"),
        ("CG1014_3_Hodge_route", "Hodge/DeWitt route is safe for local-GR", "false", "projector stress coefficient and weak-field map are missing"),
        ("CG1014_4_no_readout_mask", "post-readout Pi_M masks are allowed as derivation", "false", "post-readout masks are forbidden as derivation"),
        ("CG1014_5_coefficient_bound", "I_commutator/projector-stress bound rows are claim-ready", "false", "coefficient rows are retained/unfilled"),
        ("CG1014_6_Newton_local_GR", "Newton/local-GR gates can reopen", "false", "commutator/projector variation remains retained residual"),
        ("CG1014_7_guardrail", "PiM commutator/projector variation guardrail is installed", str(theorem_failed and runner_nonclaim and route_nonclaim).lower(), "zero theorem is not promoted and bound rows stay nonclaim"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for gate_id, claim, gate_pass, reason in gates
    ]


def decision_rows() -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC1014_0_topological_route_conditional",
            "decision": "A fixed topological Pi_M can kill the commutator only conditionally.",
            "because": "metric independence and closed representative are not enough; Hilbert equality and no extra projection are still missing.",
            "next_action": "try the topological-Hilbert equality theorem or fill R_eq/I_commutator rows",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1014_1_Hodge_route_retained",
            "decision": "Any Hodge/DeWitt/domain-dependent Pi_M route must carry projector stress.",
            "because": "delta_g Pi_M, domain selector, normal, Green operator, and boundary metric dependence can feed PPN/R11 rows.",
            "next_action": "keep projector_stress_beta_equiv and T_PiM rows active unless zero theorem is sourced",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1014_2_next_R_eq",
            "decision": "The next root target is topological-Hilbert equality or R_eq bound.",
            "because": "even a closed topological current can be the wrong conserved object unless Pi_M J_H = J_M_top + dB_zero.",
            "next_action": "derive Hilbert/worldtube equality or fill R_eq_integral with source-backed units and normalization",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
            "objective": "derive Pi_M J_H = J_M_top + dB_zero from the same Hilbert compact-source worldtube, or fill R_eq_integral/I_commutator source-backed bound rows",
            "include": "J_M_top, Pi_M J_H, dB_zero, R_eq_integral, compact source worldtube, fixed S2 class, boundary zero flux, M_H_ref normalization, source paths",
            "exclude": "closed wrong topological charge, reference-only zero, post-readout equality multiplier, fitted GM calibration, Newton/local-GR claim, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED:
            changed.append(path)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    routes: list[dict[str, str]],
    coefficients: list[dict[str, str]],
    runner: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    required_quantities = {"R_eq_integral", "I_commutator", "B_zero_flux", "projector_stress_beta_equiv", "Delta_PiM", "epsilon_radial_Meff"}
    validations = [
        ("V1014_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and needles are present"),
        ("V1014_1_theorem_blocks_claim", any(row["clause_id"] == "PCT1014_7_verdict" and row["current_status"] == "fail_current_claim" for row in theorem) and all(not flag(row["valid_for_claim"]) for row in theorem), "PiM commutator zero theorem remains nonclaim"),
        ("V1014_2_route_split_written", {"topological", "Hodge/DeWitt", "forbidden"}.issubset({row["route_type"] for row in routes}), "topological/Hodge/forbidden route split is represented"),
        ("V1014_3_coefficients_complete", required_quantities.issubset({row["quantity"] for row in coefficients}), "commutator/projector-stress bound quantities are represented"),
        ("V1014_4_coefficients_nonclaim", all(row["current_status"] == "retained_unfilled" and not flag(row["valid_for_claim"]) for row in coefficients), "coefficient rows remain retained/unfilled and nonclaim"),
        ("V1014_5_runner_refuses", len(runner) == len(coefficients) and all(row["verdict"] == "RETAINED_NONCLAIM_PIM_COMMUTATOR_BOUND_ROW" and not flag(row["claim_allowed"]) for row in runner), "runner refuses all unfilled bound rows"),
        ("V1014_6_reference_zero_guarded", any(row["route_id"] == "PRS1014_5_reference_zero" and not flag(row["valid_for_claim"]) for row in routes), "reference-only zero is nonclaim"),
        ("V1014_7_claim_gates_blocked", all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in claims), "commutator, projector stress, Newton, and local-GR claims stay blocked"),
        ("V1014_8_guardrail_written", any(row["gate_id"] == "CG1014_7_guardrail" and flag(row["gate_pass"]) for row in claims), "PiM commutator/projector variation guardrail is installed"),
        ("V1014_9_decision_written", any(row["decision_id"] == "DEC1014_2_next_R_eq" for row in decisions), "topological-Hilbert equality next-root decision is written"),
        ("V1014_10_next_target_written", len(next_target) == 1 and "1015-Y5-R10-topological-Hilbert-equality" in next_target[0]["next_target"], "1015 target row is present and nonclaim"),
        ("V1014_11_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": cid, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for cid, passed, detail in validations]
    rows.insert(0, {"check_id": "V1014_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1014 PiM commutator/projector variation validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    routes: list[dict[str, str]],
    coefficients: list[dict[str, str]],
    runner: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1014 Y5 R10 PiM commutator/projector variation zero or coefficient bound",
            "",
            "**Status:** `[d,Pi_M]J_H=0` and `delta Pi_M` stress silence are not derived. The topological route remains conditional on Hilbert equality, and Hodge/domain projector routes remain retained residuals.",
            "",
            "**Claim ceiling:** no PiM commutator zero, projector-stress silence, measured-GM closure, Newton/GR reduction, or local-GR claim is allowed from 1014.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Commutator theorem attempt",
            md_table(theorem, ["clause_id", "claim_piece", "mathematical_form", "current_status", "failure_if_missing", "valid_for_claim"]),
            "## Route split",
            md_table(routes, ["route_id", "route_type", "condition", "current_status", "meaning", "valid_for_claim"]),
            "## Coefficient bound rows",
            md_table(coefficients, ["coefficient_id", "quantity", "definition", "value_or_theorem", "units", "affected_rows", "current_status", "valid_for_claim"]),
            "## Runner",
            md_table(runner, ["runner_id", "coefficient_id", "quantity", "verdict", "score_ready", "claim_allowed", "failure_reasons"]),
            "## Claim gate",
            md_table(claims, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Validation",
            md_table(validations, ["check_id", "result", "detail", "generated_utc"]),
            "## Next target",
            md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    theorem = commutator_theorem_rows()
    routes = route_split_rows()
    coefficients = coefficient_rows()
    runner = runner_rows(coefficients)
    claims = claim_gate_rows(theorem, routes, runner)
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, theorem, routes, coefficients, runner, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1014_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1014_PIM_COMMUTATOR_THEOREM_ATTEMPT.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_1014_ROUTE_SPLIT.csv", routes)
    write_csv(OUT / "P8_Y5_R10_1014_COEFFICIENT_BOUND_ROWS.csv", coefficients)
    write_csv(OUT / "P8_Y5_R10_1014_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1014_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_1014_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1014_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1014_VALIDATION.csv", validations)
    write_doc(sources, theorem, routes, coefficients, runner, claims, decisions, next_target, validations)


if __name__ == "__main__":
    main()
