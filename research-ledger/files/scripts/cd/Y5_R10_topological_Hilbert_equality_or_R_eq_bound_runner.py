from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def missing(value: object) -> bool:
    text = str(value or "").strip()
    return text == "" or text.upper().startswith("MISSING") or text.startswith("FILL_")


def source_path(path_text: str) -> Path:
    candidate = Path(path_text)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for data_row in rows:
            for key in data_row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for data_row in rows:
            writer.writerow({key: data_row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(data_row.get(column, "")) for column in columns) + " |" for data_row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1015_0_1014_next", "source-intake/mts_residuals/P8_Y5_R10_1014_NEXT_TARGET.csv", "derive Pi_M J_H = J_M_top + dB_zero", "1014 handoff target."),
        ("SRC1015_1_1014_decision", "source-intake/mts_residuals/P8_Y5_R10_1014_DECISION_LEDGER.csv", "DEC1014_2_next_R_eq", "1014 decision selecting R_eq/Hilbert equality."),
        ("SRC1015_2_1014_coefficients", "source-intake/mts_residuals/P8_Y5_R10_1014_COEFFICIENT_BOUND_ROWS.csv", "PCC1014_0_R_eq_integral", "1014 retained R_eq and commutator rows."),
        ("SRC1015_3_501_attempt", "source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv", "EH501_1_worldtube_charge_route", "prior topological-Hilbert equality attempt."),
        ("SRC1015_4_501_obstructions", "source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv", "OB501_0_independent_topological_label", "prior conserved-wrong-object obstruction map."),
        ("SRC1015_5_501_routes", "source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_ROUTE_TESTS.csv", "R501_0_define_top_charge_from_Hilbert_source", "prior route split."),
        ("SRC1015_6_topological_conditions", "source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv", "TC500_3_Hilbert_equality", "topological PiM closure conditions."),
        ("SRC1015_7_topological_certificate", "source-intake/mts_residuals/P8_Y5_PIM_TOPO_EQUALITY_CERTIFICATE.csv", "PTEC534_4_topological_Hilbert_equality", "PiM topological-equality certificate."),
        ("SRC1015_8_hwt_attempt", "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv", "HWT536_3_Hilbert_to_PiM_charge_map", "Hilbert worldtube glue theorem attempt."),
        ("SRC1015_9_hwt_certificate", "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv", "HWG535_2_topological_representative_matches_worldtube_boundary", "Hilbert worldtube certificate gaps."),
        ("SRC1015_10_parent_contract", "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv", "PAC537_5_Hilbert_topological_charge_equality", "parent action contract for equality."),
        ("SRC1015_11_worldtube_measure", "source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_1_worldtube_source_measure", "GR-style source-measure theorem."),
        ("SRC1015_12_hamiltonian_measure", "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv", "HSM541_2_observed_worldtube_source", "Hamiltonian source-measure contract."),
        ("SRC1015_13_pim_fill", "source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv", "PIF537_0_R_eq_integral", "PiM residual input fill template."),
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


def same_object_lemma_rows() -> list[dict[str, str]]:
    rows = [
        (
            "SOL1015_0_domain",
            "same compact Hilbert source worldtube",
            "W_source is fixed by the parent Hilbert source support before readout; linking spheres S1,S2 enclose the same W_source",
            "conditional_reference_lemma",
            "without this, Q_M can be chosen after seeing mu_obs",
        ),
        (
            "SOL1015_1_source_measure",
            "same Hilbert/Noether source measure",
            "Q_M := H_tau[S_outer]-H_ref := integral_W rho_H dV_H in the observed source frame",
            "conditional_reference_lemma",
            "without this, the topological charge is a bare or independent label",
        ),
        (
            "SOL1015_2_poincare_dual",
            "topological representative is the Poincare dual of that same worldtube",
            "J_M_top := Q_M omega_M_top, d omega_M_top=0, integral_link omega_M_top=1",
            "conditional_reference_lemma",
            "without this, closed J_M_top may be the wrong conserved object",
        ),
        (
            "SOL1015_3_de_rham_equality",
            "closed currents with the same compact-support class differ by an exact form",
            "Pi_M J_H - J_M_top = dB_zero + R_eq; if same class and no residual source, R_eq=0",
            "mathematical_lemma_pass_conditional",
            "exactness only follows after the same-class hypothesis is parent-signed",
        ),
        (
            "SOL1015_4_boundary_zero",
            "exact improvement has zero compact linked-boundary flux",
            "integral_boundary dB_zero=0 with reference fixed once",
            "not_signed_for_current_MTS",
            "otherwise measured GM shifts by a boundary/reference convention",
        ),
        (
            "SOL1015_5_commutator_stress_silence",
            "Pi_M is a fixed chain map on the Hilbert current domain",
            "[d,Pi_M]J_H=0 and delta_g Pi_M stress is absent or below locks",
            "not_signed_for_current_MTS",
            "otherwise equality still leaves projector hair",
        ),
        (
            "SOL1015_6_verdict",
            "topological-Hilbert equality theorem",
            "Pi_M J_H = J_M_top + dB_zero requires SOL1015_0 through SOL1015_5",
            "conditional_lemma_written_current_claim_fails",
            "current MTS lacks parent worldtube/source-measure/class and boundary-zero signatures",
        ),
    ]
    return [
        {
            "lemma_id": lemma_id,
            "required_clause": required_clause,
            "mathematical_form": mathematical_form,
            "current_status": current_status,
            "failure_if_missing": failure_if_missing,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for lemma_id, required_clause, mathematical_form, current_status, failure_if_missing in rows
    ]


def equality_audit_rows() -> list[dict[str, str]]:
    rows = [
        ("HEA1015_0_worldtube_fixed", "HWT536_0;HWG535_0;PAC537_2;HSM541_2", "W_source fixed by parent source/support/topology before readout", "not_derived_for_current_MTS", "readout/domain mask risk remains"),
        ("HEA1015_1_source_measure_owned", "HWT536_1;HWG535_1;PAC537_1;HSM541_2", "same observed Hilbert/Noether measure defines Q_M", "same_frame_source_measure_not_yet_locked", "source and orbital mass may live in different frames"),
        ("HEA1015_2_dressed_charge_not_bare_mass", "HWT536_2;T510_1;SMT540_6", "M_source is dressed Hamiltonian/Noether charge", "definition_guardrail_pass_but_not_full_MTS_theorem", "bare mass shortcut remains forbidden"),
        ("HEA1015_3_Hilbert_to_PiM_charge_map", "HWT536_3;PAC537_4;HSM541_0", "Pi_M J_H is the same Hamiltonian/source charge form", "not_derived", "Pi_M may still select a non-observed mass channel"),
        ("HEA1015_4_topological_boundary_match", "HWT536_4;HWG535_2;PTEC534_4", "omega_M_top is the Poincare dual of the same Hilbert worldtube", "certificate_missing", "closed topology can conserve the wrong object"),
        ("HEA1015_5_boundary_reference_zero", "HWT536_5;PAC537_6;OB501_2", "dB_zero has zero compact boundary flux with one fixed reference", "missing_certificate_or_bound", "boundary bookkeeping can move measured GM"),
        ("HEA1015_6_extra_exchange_silence", "HWT536_7;FC3;SMR509_3", "Pi_M dJ_extra and nonEH/domain/memory/frame/range charge channels vanish or are bounded", "field_specific_silence_queue_open", "mu_extra/radial hair remains active"),
        ("HEA1015_7_calibration_and_PPN", "HWT536_8;FC7;HSM541_5;HSM541_7", "same charge controls inverse-square coefficient and PPN residual vector", "not_reached", "local GR cannot be claimed from first-order equality alone"),
        ("HEA1015_8_verdict", "SOL1015_0-SOL1015_5", "current MTS satisfies the equality theorem hypotheses", "fail_current_claim", "use R_eq/I_commutator bound path until parent signatures exist"),
    ]
    return [
        {
            "audit_id": audit_id,
            "source_clauses": source_clauses,
            "required_identity": required_identity,
            "current_status": current_status,
            "failure_if_missing": failure_if_missing,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for audit_id, source_clauses, required_identity, current_status, failure_if_missing in rows
    ]


def bound_input_rows() -> list[dict[str, str]]:
    rows = [
        ("REB1015_0_R_eq_integral", "R_eq_integral", "finite shell integral of R_eq := Pi_M J_H - J_M_top - dB_zero", "MISSING_R_EQ_INTEGRAL", "dimensionless_after_MHref_normalization", "R4;R9;R10;R11", "source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv"),
        ("REB1015_1_B_zero_flux", "B_zero_flux", "compact linked-boundary flux of exact/reference term dB_zero", "MISSING_B_ZERO_FLUX", "GM_flux_or_dimensionless", "R3;R4;R7;R8;R9;R11", "source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv"),
        ("REB1015_2_I_commutator", "I_commutator", "finite annulus integral of [d,Pi_M]J_H inherited if Pi_M is not a fixed chain map", "MISSING_I_COMMUTATOR", "GM_flux_or_dimensionless_after_Meff_normalization", "R4;R7;R9;R10;R11", "source-intake/mts_residuals/P8_Y5_R10_1014_COEFFICIENT_BOUND_ROWS.csv"),
        ("REB1015_3_Delta_worldtube_domain", "Delta_worldtube_domain", "charge shift under allowed compact-source worldtube/domain choices", "MISSING_DOMAIN_SELECTOR_BOUND", "dimensionless_or_GM_flux", "R5;R6;R8;R9;R11", "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv"),
        ("REB1015_4_Delta_extra_vector", "Delta_extra_vector", "nonEH/domain/memory/motion/time/range/frame/source-channel mass residual vector", "MISSING_DELTA_EXTRA_VECTOR", "dimensionless_or_GM_flux", "R1;R3;R4;R7;R8;R9;R10;R11", "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv"),
        ("REB1015_5_M_H_ref", "M_H_ref", "same-frame Hilbert/Hamiltonian source charge used to normalize equality residuals", "MISSING_M_H_REF", "mass_or_charge_normalization", "R4;R9;R10;R11", "source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv"),
        ("REB1015_6_projector_stress_beta_equiv", "projector_stress_beta_equiv", "PPN equivalent of any retained Pi_M metric/projector stress", "MISSING_PROJECTOR_STRESS_MAP", "PPN_or_operator_units_required", "R3;R4;R5;R6;R7;R8;R10;R11", "source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv"),
        ("REB1015_7_epsilon_eq_Meff", "epsilon_eq_Meff", "M_H_ref^-1 absolute envelope of R_eq, B_zero, commutator, domain, and extra-channel residuals", "MISSING_COMPONENT_INPUTS", "dimensionless", "R4;R10;R11", "source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_SPEC.csv"),
    ]
    return [
        {
            "bound_id": bound_id,
            "quantity": quantity,
            "definition": definition,
            "value_or_theorem": value_or_theorem,
            "units": units,
            "affected_rows": affected_rows,
            "source_path": path_text,
            "current_status": "retained_unfilled",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for bound_id, quantity, definition, value_or_theorem, units, affected_rows, path_text in rows
    ]


def runner_rows(bounds: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for bound_row in bounds:
        reasons = []
        if missing(bound_row["value_or_theorem"]):
            reasons.append("MISSING_VALUE_OR_THEOREM")
        if bound_row["current_status"] != "filled_source_backed":
            reasons.append("RETAINED_UNFILLED_BLOCKS_CLAIM")
        if not flag(bound_row["valid_for_claim"]):
            reasons.append("VALID_FOR_CLAIM_FALSE")
        rows.append(
            {
                "runner_id": bound_row["bound_id"].replace("REB1015", "RER1015"),
                "bound_id": bound_row["bound_id"],
                "quantity": bound_row["quantity"],
                "verdict": "RETAINED_NONCLAIM_R_EQ_BOUND_ROW",
                "score_ready": "false",
                "claim_allowed": "false",
                "failure_reasons": ";".join(reasons),
                "generated_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, str]]:
    gates = [
        ("CG1015_0_same_object_lemma", "same-object lemma is valid as mathematics", "true", "conditional de Rham/Poincare-dual lemma is recorded", "false"),
        ("CG1015_1_parent_worldtube_signed", "parent fixes the compact Hilbert worldtube before readout", "false", "HWT536_0/HWG535_0/PAC537_2 remain unsigned", "false"),
        ("CG1015_2_source_measure_signed", "same-frame Hilbert/Noether source measure defines Q_M", "false", "HWT536_1/HSM541_2 remain unsigned", "false"),
        ("CG1015_3_topological_Hilbert_equality", "Pi_M J_H = J_M_top + dB_zero is derived for current MTS", "false", "same-class and boundary-zero hypotheses are not parent-signed", "false"),
        ("CG1015_4_R_eq_bound_ready", "R_eq/I_commutator/equality residual rows are source-backed numeric rows", "false", "all bound rows are retained placeholders", "false"),
        ("CG1015_5_Newton_local_GR", "Newton/local-GR gates can reopen", "false", "measured-GM source normalization, calibration, and PPN stability remain blocked", "false"),
        ("CG1015_6_guardrail", "topological-Hilbert equality guardrail is installed", "true", "conditional lemma is not promoted; residual rows stay nonclaim", "false"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "claim_allowed": claim_allowed,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for gate_id, claim, gate_pass, reason, claim_allowed in gates
    ]


def decision_rows() -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC1015_0_conditional_lemma",
            "decision": "The de Rham/Poincare-dual same-object route is mathematically clean.",
            "because": "if Pi_M J_H and J_M_top are representatives of the same compact Hilbert source worldtube class, their difference is exact plus a residual R_eq.",
            "next_action": "prove the parent worldtube/source-measure/class hypotheses, not merely write the equality",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1015_1_current_MTS_not_signed",
            "decision": "Current MTS does not yet satisfy the same-object hypotheses.",
            "because": "worldtube selection, source measure, topological boundary match, boundary zero flux, extra-channel silence, and PPN stability remain unsigned.",
            "next_action": "target parent worldtube-source-measure selector or fill source-backed R_eq/B_zero/I_commutator rows",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1015_2_bound_runner",
            "decision": "R_eq/I_commutator rows are now the explicit fallback path.",
            "because": "failed proof components have named quantities, units, affected arenas, and source paths, but no claim-valid numeric inputs.",
            "next_action": "build first source-backed equality residual row only after M_H_ref and source path are real",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1015_3_next_target",
            "decision": "The next root theorem is parent worldtube-source-measure selection.",
            "because": "without HWT536_0-HWT536_3/HSM541_2, topology conserves an object but not necessarily the observed mass source.",
            "next_action": "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
            "valid_for_claim": "false",
        },
    ]
    for data_row in rows:
        data_row["generated_utc"] = stamp()
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
            "objective": "derive the parent-owned compact Hilbert source worldtube and same-frame source measure that make Q_M the observed Hilbert/Noether charge, or fill the first source-backed R_eq/B_zero/I_commutator row",
            "include": "HWT536_0-HWT536_3, HSM541_2, W_source, rho_H dV_H, M_H_ref, fixed linking surfaces, source path, units, no readout mask",
            "exclude": "bare mass shortcut, late equality multiplier, independent topological label, reference-only zero, Newton/local-GR claim, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file() and datetime.fromtimestamp(candidate.stat().st_mtime, timezone.utc) >= STARTED:
            changed.append(candidate)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    lemma: list[dict[str, str]],
    audit: list[dict[str, str]],
    bounds: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    required_bounds = {
        "R_eq_integral",
        "B_zero_flux",
        "I_commutator",
        "Delta_worldtube_domain",
        "Delta_extra_vector",
        "M_H_ref",
        "projector_stress_beta_equiv",
        "epsilon_eq_Meff",
    }
    validations = [
        ("V1015_0_sources_exist", all(flag(data_row["exists"]) and flag(data_row["needle_found"]) for data_row in sources), "all source paths exist and needles are present"),
        ("V1015_1_same_object_lemma_written", any(data_row["lemma_id"] == "SOL1015_6_verdict" and data_row["current_status"] == "conditional_lemma_written_current_claim_fails" for data_row in lemma), "same-object lemma is explicit and not promoted"),
        ("V1015_2_lemma_nonclaim", all(not flag(data_row["valid_for_claim"]) for data_row in lemma), "all lemma rows remain nonclaim"),
        ("V1015_3_audit_covers_parent_debts", {"HEA1015_0_worldtube_fixed", "HEA1015_1_source_measure_owned", "HEA1015_3_Hilbert_to_PiM_charge_map", "HEA1015_4_topological_boundary_match", "HEA1015_7_calibration_and_PPN"}.issubset({data_row["audit_id"] for data_row in audit}), "parent worldtube/source/calibration debts are audited"),
        ("V1015_4_current_claim_fails", any(data_row["audit_id"] == "HEA1015_8_verdict" and data_row["current_status"] == "fail_current_claim" for data_row in audit), "current MTS equality proof is blocked"),
        ("V1015_5_bound_rows_complete", required_bounds.issubset({data_row["quantity"] for data_row in bounds}), "R_eq, commutator, boundary, source, and stress bound rows are present"),
        ("V1015_6_bound_rows_nonclaim", all(data_row["current_status"] == "retained_unfilled" and not flag(data_row["valid_for_claim"]) for data_row in bounds), "all bound rows remain retained/unfilled and nonclaim"),
        ("V1015_7_runner_refuses", len(runner) == len(bounds) and all(data_row["verdict"] == "RETAINED_NONCLAIM_R_EQ_BOUND_ROW" and not flag(data_row["claim_allowed"]) for data_row in runner), "runner refuses unfilled equality residual rows"),
        ("V1015_8_claim_gates_blocked", all(not flag(data_row["claim_allowed"]) and not flag(data_row["valid_for_claim"]) for data_row in gates), "Newton/local-GR and equality claims remain blocked"),
        ("V1015_9_guardrail_written", any(data_row["gate_id"] == "CG1015_6_guardrail" and flag(data_row["gate_pass"]) for data_row in gates), "topological-Hilbert equality guardrail is installed"),
        ("V1015_10_decision_written", any(data_row["decision_id"] == "DEC1015_3_next_target" for data_row in decisions), "1016 root target decision is written"),
        ("V1015_11_next_target_written", len(next_target) == 1 and "1016-Y5-R10-parent-worldtube-source-measure" in next_target[0]["next_target"], "1016 target row is present and nonclaim"),
        ("V1015_12_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in validations]
    rows.insert(0, {"check_id": "V1015_SUMMARY", "result": "pass" if all(data_row["result"] == "pass" for data_row in rows) else "fail", "detail": "1015 topological-Hilbert equality/R_eq validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    lemma: list[dict[str, str]],
    audit: list[dict[str, str]],
    bounds: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1015 Y5 R10 topological-Hilbert equality or R_eq bound runner",
            "",
            "**Status:** The exact same-object lemma is now written: a fixed compact Hilbert source worldtube plus a Poincare-dual topological representative would give `Pi_M J_H = J_M_top + dB_zero` when the residual class `R_eq` and boundary flux vanish. Current MTS does not yet parent-sign those hypotheses.",
            "",
            "**Claim ceiling:** no topological-Hilbert equality, closed Hilbert flux, measured-GM closure, Newton/GR reduction, R10/R11 pass, PPN pass, or local-GR claim is allowed from 1015.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Same-object lemma",
            md_table(lemma, ["lemma_id", "required_clause", "mathematical_form", "current_status", "failure_if_missing", "valid_for_claim"]),
            "## Equality audit",
            md_table(audit, ["audit_id", "source_clauses", "required_identity", "current_status", "failure_if_missing", "valid_for_claim"]),
            "## R_eq bound input rows",
            md_table(bounds, ["bound_id", "quantity", "definition", "value_or_theorem", "units", "affected_rows", "current_status", "valid_for_claim"]),
            "## Runner",
            md_table(runner, ["runner_id", "bound_id", "quantity", "verdict", "score_ready", "claim_allowed", "failure_reasons"]),
            "## Claim gate",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
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
    lemma = same_object_lemma_rows()
    audit = equality_audit_rows()
    bounds = bound_input_rows()
    runner = runner_rows(bounds)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, lemma, audit, bounds, runner, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1015_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1015_DE_RHAM_SAME_OBJECT_LEMMA.csv", lemma)
    write_csv(OUT / "P8_Y5_R10_1015_HILBERT_TO_TOPOLOGICAL_EQUALITY_AUDIT.csv", audit)
    write_csv(OUT / "P8_Y5_R10_1015_R_EQ_BOUND_INPUT_ROWS.csv", bounds)
    write_csv(OUT / "P8_Y5_R10_1015_BOUND_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1015_CLAIM_GATE.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1015_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1015_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1015_VALIDATION.csv", validations)
    write_doc(sources, lemma, audit, bounds, runner, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()
