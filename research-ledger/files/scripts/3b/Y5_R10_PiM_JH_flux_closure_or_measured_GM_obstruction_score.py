from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"
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
    if text in {"REFERENCE_ONLY", "THEOREM_ONLY", "NUMERIC_REQUIRED", "FORBIDDEN"}:
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
        ("SRC1013_0_1012_next", "source-intake/mts_residuals/P8_Y5_R10_1012_NEXT_TARGET.csv", "derive compact-exterior closure", "1012 handoff target."),
        ("SRC1013_1_1012_owner", "source-intake/mts_residuals/P8_Y5_R10_1012_Y5_OWNER_THEOREM_ATTEMPT.csv", "Y5O1012_3_flux_closure", "prior Y5 owner theorem blocker."),
        ("SRC1013_2_1012_decision", "source-intake/mts_residuals/P8_Y5_R10_1012_DECISION_LEDGER.csv", "DEC1012_2_next_root", "Pi_M J_H selected as next root."),
        ("SRC1013_3_parent_identity", "source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_ATTEMPT.csv", "I499_3_parent_source_identity", "exact flux obstruction identity."),
        ("SRC1013_4_mass_flux", "source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv", "MF2_Euler_flux_closure", "mass flux closure contract."),
        ("SRC1013_5_PiM_algebra", "source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv", "PM6_flux_closure_requires_Ward_or_Euler", "Pi_M algebra does not imply closure."),
        ("SRC1013_6_PiM_stress", "source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv", "PV0_product_variation_included", "projector variation/stress contract."),
        ("SRC1013_7_worldtube", "source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv", "W504_4_worldtube_source_measure_glue", "worldtube source-measure glue."),
        ("SRC1013_8_flux_theorem", "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv", "T509_1_flux_closure", "source-measure/M_eff flux theorem attempt."),
        ("SRC1013_9_flux_residual", "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv", "SMR509_0_Delta_flux", "source-measure residual map."),
        ("SRC1013_10_flux_gates", "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_GATE_TESTS.csv", "G509_2_flux_closure", "source-measure flux gate tests."),
        ("SRC1013_11_pim_commutator", "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_GATE.csv", "PC521_0_product_rule", "Pi_M commutator gate."),
        ("SRC1013_12_pim_radial_input", "source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv", "PI521_1_commutator_profile", "Pi_M radial bound input."),
        ("SRC1013_13_pim_input_template", "source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv", "PIF537_1_I_commutator", "Pi_M input fill template."),
        ("SRC1013_14_pim_numeric_audit", "source-intake/mts_residuals/P8_Y5_PIM_NUMERIC_INPUT_AUDIT.csv", "AUD536_5", "numeric input audit says commutator unfilled."),
        ("SRC1013_15_meff_runner", "source-intake/mts_residuals/P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv", "MR510_0_flux_leak", "worldtube M_eff residual runner."),
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


def flux_theorem_rows() -> list[dict[str, str]]:
    rows = [
        ("PFC1013_0_same_frame_JH", "same-frame Hilbert mass current", "J_H[e_obs] is defined by the matter action in the same observed coframe used for clocks/orbits", "conditional_from_source_current_contract", "source current remains fitted/calibration-only"),
        ("PFC1013_1_PiM_parent_origin", "parent-owned Pi_M", "Pi_M is fixed before readout as topological/symplectic/source charge data", "candidate_origin_not_completed", "Pi_M can be a readout mask"),
        ("PFC1013_2_product_rule", "full product rule", "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H", "exact_obstruction_active", "commutator term remains source-normalization residual"),
        ("PFC1013_3_extra_projection_zero", "zero projected extra current", "Pi_M dJ_extra=0 for boundary/domain/bulk/nonEH/kappa/frame/species channels", "not_parent_derived", "mu_extra enters measured mass"),
        ("PFC1013_4_commutator_zero", "zero Pi_M commutator", "[d,Pi_M]J_H=0 by fixed absolute charge map or explicit coefficient bound", "not_parent_derived", "radial/time/source residual remains"),
        ("PFC1013_5_parent_anomaly_zero", "zero parent anomaly", "A_parent=0 or source-backed finite bound", "not_derived", "source identity is decomposition, not closure"),
        ("PFC1013_6_worldtube_glue", "worldtube source equals exterior charge", "M_source[W]=integral_S Q_M[tau]=M_eff before orbital fitting", "not_yet_derived_core_missing_piece", "closed wrong charge can mimic success"),
        ("PFC1013_7_absolute_calibration", "closed charge calibrates to measured Newtonian GM", "M_eff=(4*pi*G_ref)^-1 int_S Pi_M J_H and mu_obs=G_eff M_eff", "not_parent_derived", "conserved but misnormalized mass remains possible"),
        ("PFC1013_8_verdict", "d(Pi_M J_H)=0 compact-exterior flux closure", "PFC1013_0 through PFC1013_7 all pass with no missing obstruction rows", "fail_current_claim", "measured-GM/Newton/local-GR cannot reopen"),
    ]
    output = []
    for row in rows:
        output.append(
            {
                "clause_id": row[0],
                "claim_piece": row[1],
                "mathematical_form": row[2],
                "current_status": row[3],
                "failure_if_missing": row[4],
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return output


def obstruction_rows() -> list[dict[str, str]]:
    rows = [
        ("OBS1013_0_projected_extra_current", "-Pi_M dJ_extra", "projected boundary/domain/bulk/nonEH/kappa/frame/species exchange current", "MISSING_DELTA_EXTRA_VECTOR", "dimensionless_or_GM_flux_units", "R1;R3;R4;R7;R8;R9;R10;R11", "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv"),
        ("OBS1013_1_PiM_commutator", "[d,Pi_M]J_H", "projector commutator finite-annulus integral", "MISSING_I_COMMUTATOR", "GM_flux_or_dimensionless_after_Meff_normalization", "R4;R7;R9;R10;R11", "source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv"),
        ("OBS1013_2_parent_anomaly", "A_parent", "parent anomaly/source-identity defect in Hilbert mass closure", "MISSING_A_PARENT_BOUND", "GM_flux_or_dimensionless", "R4;R9;R11", "source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_ATTEMPT.csv"),
        ("OBS1013_3_topological_equality_residual", "R_eq", "Pi_M J_H - J_M_top - dB_zero", "MISSING_R_EQ_INTEGRAL", "dimensionless_after_MHref_normalization", "R4;R9;R11", "source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv"),
        ("OBS1013_4_boundary_zero_flux", "B_zero_flux", "exact/reference/boundary improvement flux through compact linked boundary", "MISSING_B_ZERO_FLUX", "GM_flux_or_dimensionless", "R4;R7;R8;R9;R11", "source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv"),
        ("OBS1013_5_projector_stress", "T_PiM", "weak-field/PPN equivalent of metric stress from projector variation", "MISSING_PROJECTOR_STRESS_MAP", "PPN_or_operator_units_required", "R3;R4;R5;R6;R7;R8;R10;R11", "source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv"),
        ("OBS1013_6_flux_leak", "dln_Meff_dt or epsilon_radial_Meff", "finite-annulus flux leakage M_eff^-1 int_A d(Pi_M J_H)", "MISSING_TIME_RADIAL_PROFILE_OR_THEOREM", "yr^-1_or_dimensionless_radial_envelope", "R4;R9;R10;R11", "source-intake/mts_residuals/P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv"),
        ("OBS1013_7_calibration_PPN_tail", "Delta_cal + Delta_PPN", "closed charge fails inverse-square/second-order PPN readout", "MISSING_GAUSS_ORBITAL_PPN_RESIDUAL", "dimensionless_vector", "R3;R4;R5;R6;R7;R8;R11", "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv"),
    ]
    output = []
    for row in rows:
        output.append(
            {
                "obstruction_id": row[0],
                "symbol": row[1],
                "definition": row[2],
                "value_or_theorem": row[3],
                "units": row[4],
                "affected_rows": row[5],
                "source_path": row[6],
                "current_status": "retained_unfilled",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return output


def evaluate_obstruction(row: dict[str, str]) -> dict[str, str]:
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
        "runner_id": row["obstruction_id"].replace("OBS", "OBR"),
        "obstruction_id": row["obstruction_id"],
        "symbol": row["symbol"],
        "verdict": "PASS_FLUX_OBSTRUCTION_ROW" if claim_allowed else "RETAINED_NONCLAIM_FLUX_OBSTRUCTION_ROW",
        "score_ready": "false",
        "claim_allowed": str(claim_allowed).lower(),
        "valid_for_claim": str(claim_allowed).lower(),
        "failure_reasons": ";".join(reasons),
        "generated_utc": stamp(),
    }


def runner_rows(obstructions: list[dict[str, str]]) -> list[dict[str, str]]:
    return [evaluate_obstruction(row) for row in obstructions]


def claim_gate_rows(theorem: list[dict[str, str]], runner: list[dict[str, str]]) -> list[dict[str, str]]:
    theorem_failed = any(row["clause_id"] == "PFC1013_8_verdict" and row["current_status"] == "fail_current_claim" for row in theorem)
    runner_nonclaim = all(not flag(row["claim_allowed"]) for row in runner)
    gates = [
        ("CG1013_0_flux_closure", "d(Pi_M J_H)=0 compact-exterior closure passes", "false", "Pi_M origin, extra projection, commutator, anomaly, worldtube glue, and calibration remain unsigned"),
        ("CG1013_1_commutator", "[d,Pi_M]J_H is zero or bounded", "false", "I_commutator is unfilled and projector variation remains active"),
        ("CG1013_2_extra_projection", "Pi_M dJ_extra=0", "false", "boundary/domain/bulk/nonEH/frame/species extra channels remain active"),
        ("CG1013_3_obstruction_score", "exact measured-GM obstruction vector is score-ready", "false", "all obstruction terms are retained/unfilled"),
        ("CG1013_4_Newton_local_GR", "Newton/local-GR gates can reopen", "false", "measured-GM flux closure and obstruction scores are not claim-ready"),
        ("CG1013_5_guardrail", "Pi_M J_H flux proof-or-score guardrail is installed", str(theorem_failed and runner_nonclaim).lower(), "closure theorem is not promoted and obstruction rows stay nonclaim"),
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
            "decision_id": "DEC1013_0_exact_obstruction_is_best_object",
            "decision": "The exact flux obstruction is now the measured-GM object to derive or score.",
            "because": "d(Pi_M J_H)=0 reduces to separately controlling -Pi_M dJ_extra, [d,Pi_M]J_H, and A_parent plus glue/calibration tails.",
            "next_action": "attack the Pi_M commutator/projector variation first because it is a direct product-rule obstruction",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1013_1_topological_route_not_enough",
            "decision": "A closed topological mass current is insufficient unless it equals Pi_M J_H.",
            "because": "the conserved object can be the wrong object without Hilbert/worldtube equality and calibration.",
            "next_action": "do not use topological closure as Newton evidence until R_eq is zero or bounded",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1013_2_next_commutator",
            "decision": "The next root target is the Pi_M commutator/projector variation row.",
            "because": "[d,Pi_M]J_H directly contaminates radial M_eff, source-normalization, PPN, and R11 rows.",
            "next_action": "derive [d,Pi_M]J_H=0 from fixed topological charge map or fill I_commutator/projector-stress coefficients",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
            "objective": "derive [d,Pi_M]J_H=0 and delta Pi_M stress silence from a fixed topological charge map, or fill I_commutator and projector-stress coefficient bounds",
            "include": "Pi_M product rule, I_commutator, delta Pi_M, topology/Hodge route split, R_eq, boundary zero flux, projector stress beta equivalent, affected PPN/R11 rows, source paths",
            "exclude": "projector algebra counted as closure, post-readout mask, reference-only topological zero, fitted cancellation, Newton/local-GR claim, GitHub action",
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
    obstructions: list[dict[str, str]],
    runner: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    required_symbols = {"-Pi_M dJ_extra", "[d,Pi_M]J_H", "A_parent", "R_eq", "B_zero_flux", "T_PiM", "dln_Meff_dt or epsilon_radial_Meff", "Delta_cal + Delta_PPN"}
    validations = [
        ("V1013_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and needles are present"),
        ("V1013_1_theorem_blocks_claim", any(row["clause_id"] == "PFC1013_8_verdict" and row["current_status"] == "fail_current_claim" for row in theorem) and all(not flag(row["valid_for_claim"]) for row in theorem), "Pi_M J_H flux theorem remains nonclaim"),
        ("V1013_2_obstruction_vector_complete", required_symbols.issubset({row["symbol"] for row in obstructions}), "exact obstruction and glue/calibration tails are represented"),
        ("V1013_3_obstructions_nonclaim", len(obstructions) >= 8 and all(row["current_status"] == "retained_unfilled" and not flag(row["valid_for_claim"]) for row in obstructions), "obstruction rows remain retained/unfilled and nonclaim"),
        ("V1013_4_runner_refuses", len(runner) == len(obstructions) and all(row["verdict"] == "RETAINED_NONCLAIM_FLUX_OBSTRUCTION_ROW" and not flag(row["claim_allowed"]) for row in runner), "obstruction runner refuses all unfilled rows"),
        ("V1013_5_commutator_present", any(row["symbol"] == "[d,Pi_M]J_H" for row in obstructions) and any(row["gate_id"] == "CG1013_1_commutator" for row in claims), "Pi_M commutator is explicitly gated"),
        ("V1013_6_claim_gates_blocked", all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in claims), "flux closure, obstruction score, Newton, and local-GR claims stay blocked"),
        ("V1013_7_guardrail_written", any(row["gate_id"] == "CG1013_5_guardrail" and flag(row["gate_pass"]) for row in claims), "Pi_M J_H flux guardrail is installed"),
        ("V1013_8_decision_written", any(row["decision_id"] == "DEC1013_2_next_commutator" for row in decisions), "Pi_M commutator next-root decision is written"),
        ("V1013_9_next_target_written", len(next_target) == 1 and "1014-Y5-R10-PiM-commutator" in next_target[0]["next_target"], "1014 target row is present and nonclaim"),
        ("V1013_10_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": cid, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for cid, passed, detail in validations]
    rows.insert(0, {"check_id": "V1013_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1013 Pi_M J_H flux closure or obstruction-score validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    obstructions: list[dict[str, str]],
    runner: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1013 Y5 R10 PiM JH flux closure or measured-GM obstruction score",
            "",
            "**Status:** compact-exterior closure of `d(Pi_M J_H)=0` is not derived. The exact measured-GM obstruction vector is written as retained nonclaim rows.",
            "",
            "**Claim ceiling:** no measured-GM closure, Newton reduction, source-normalization pass, H_tau, M_H_ref, or local-GR claim is allowed from 1013.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Flux closure theorem attempt",
            md_table(theorem, ["clause_id", "claim_piece", "mathematical_form", "current_status", "failure_if_missing", "valid_for_claim"]),
            "## Obstruction score rows",
            md_table(obstructions, ["obstruction_id", "symbol", "definition", "value_or_theorem", "units", "affected_rows", "current_status", "valid_for_claim"]),
            "## Obstruction runner",
            md_table(runner, ["runner_id", "obstruction_id", "symbol", "verdict", "score_ready", "claim_allowed", "failure_reasons"]),
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
    theorem = flux_theorem_rows()
    obstructions = obstruction_rows()
    runner = runner_rows(obstructions)
    claims = claim_gate_rows(theorem, runner)
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, theorem, obstructions, runner, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1013_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1013_PIM_JH_FLUX_THEOREM_ATTEMPT.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv", obstructions)
    write_csv(OUT / "P8_Y5_R10_1013_OBSTRUCTION_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1013_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_1013_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1013_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1013_VALIDATION.csv", validations)
    write_doc(sources, theorem, obstructions, runner, claims, decisions, next_target, validations)


if __name__ == "__main__":
    main()
