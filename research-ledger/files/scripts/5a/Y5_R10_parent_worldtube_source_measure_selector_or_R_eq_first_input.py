from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"
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
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1016_0_1015_next", "source-intake/mts_residuals/P8_Y5_R10_1015_NEXT_TARGET.csv", "parent-owned compact Hilbert source worldtube", "1015 handoff target."),
        ("SRC1016_1_1015_audit", "source-intake/mts_residuals/P8_Y5_R10_1015_HILBERT_TO_TOPOLOGICAL_EQUALITY_AUDIT.csv", "HEA1015_0_worldtube_fixed", "1015 equality audit."),
        ("SRC1016_2_1015_bounds", "source-intake/mts_residuals/P8_Y5_R10_1015_R_EQ_BOUND_INPUT_ROWS.csv", "REB1015_5_M_H_ref", "1015 retained bound rows."),
        ("SRC1016_3_662_proof_chain", "source-intake/mts_residuals/P8_Y5_R10_662_PROOF_CHAIN.csv", "P662_2_worldtube_support", "662 proof chain."),
        ("SRC1016_4_662_residuals", "source-intake/mts_residuals/P8_Y5_R10_662_RESIDUAL_DECOMPOSITION.csv", "RG662_0_R_worldtube", "662 residual decomposition."),
        ("SRC1016_5_662_template", "source-intake/mts_residuals/P8_Y5_R10_662_BOUND_INPUT_TEMPLATE.csv", "BI662_0_R_glue_integral", "662 bound input template."),
        ("SRC1016_6_663_chain", "source-intake/mts_residuals/P8_Y5_R10_663_EULER_WARD_CHAIN_RESULT.csv", "EW663_2_source_current_ownership", "663 Euler/Ward chain."),
        ("SRC1016_7_663_priority", "source-intake/mts_residuals/P8_Y5_R10_663_RESIDUAL_INPUT_PRIORITY.csv", "FI663_1_second_target_source_measure_frame", "663 residual input priority."),
        ("SRC1016_8_HSM541_contract", "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv", "HSM541_2_observed_worldtube_source", "Hamiltonian source-measure contract."),
        ("SRC1016_9_source_measure_attempt", "source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_THEOREM_ATTEMPT.csv", "SMT542_2_observed_worldtube_source", "source-measure theorem attempt."),
        ("SRC1016_10_first_residual", "source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_FIRST_RESIDUAL_INPUT.csv", "MISSING_B_ZERO_FLUX", "first residual input template."),
        ("SRC1016_11_BOBS_pack", "source-intake/mts_residuals/P8_Y5_R10_777_BOBS_SOURCE_MEASURE_FIRST_PACK.csv", "BSM777_0_coupling_descent_input", "coupling/source/readout descent pack."),
        ("SRC1016_12_bound_schema", "source-intake/mts_residuals/P8_Y5_R10_778_SOURCE_MEASURE_BOUND_SCHEMA.csv", "SMB778_0_theorem_zero_route", "source-measure bound schema."),
        ("SRC1016_13_bound_runner", "source-intake/mts_residuals/P8_Y5_R10_779_SOURCE_MEASURE_BOUND_RUNNER.csv", "SMR779_0_zero_route", "source-measure bound runner."),
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


def selector_contract_rows() -> list[dict[str, str]]:
    rows = [
        (
            "PSC1016_0_parent_action",
            "explicit diffeomorphism-covariant parent action and symplectic potential",
            "delta L = E_A delta Phi^A + dTheta(Phi,delta Phi)",
            "contract_only_no_full_current_Lagrangian",
            "without a real parent Lagrangian, J_H and Q_tau are placeholders",
        ),
        (
            "PSC1016_1_single_observed_coframe",
            "one observed coframe/metric is used by matter, clocks, rods, and orbital readout",
            "S_matter = S_matter[e_obs,psi_m]; J_H[tau] := delta S_matter/delta e_obs contracted with tau",
            "same_frame_measure_not_parent_signed",
            "frame leakage becomes Delta_frame_source and WEP/PPN preferred-frame debt",
        ),
        (
            "PSC1016_2_fixed_time_generator",
            "time/Hamiltonian generator tau is fixed before source or orbital fitting",
            "L_tau e_obs = O(local stationary branch); tau chosen by parent boundary/asymptotic structure",
            "tau_source_readout_lock_open",
            "mass charge can be readout dependent",
        ),
        (
            "PSC1016_3_support_selector",
            "compact source worldtube is selected by Hilbert source support, not by fitted mass radius",
            "W_source := closure(supp J_H[tau]); S1,S2 link W_source in the source-free exterior",
            "formal_selector_definition_available_conditional",
            "requires compactness/regularity and same-frame source measure",
        ),
        (
            "PSC1016_4_linking_surface_class",
            "linking surfaces are homologous around the same W_source and fixed before readout",
            "partial A = S2 - S1; A cap W_source = empty; [S1]=[S2] in exterior homology",
            "conditional_topological_step",
            "domain sensitivity becomes Delta_worldtube_domain",
        ),
        (
            "PSC1016_5_dressed_source_charge",
            "source normalization is the dressed Hamiltonian/Noether charge, not bare mass",
            "M_H_ref := H_tau[S_outer] - H_ref = integral_S Q_tau after integrability/reference lock",
            "definition_guardrail_pass_but_integrability_missing",
            "R_eq rows cannot be normalized without a real M_H_ref",
        ),
        (
            "PSC1016_6_PiM_Hamiltonian_map",
            "Pi_M is adopted or derived as the Hamiltonian mass-charge map on this branch",
            "Pi_M^H J_H := ell_H[J_H;tau,S] omega_M^H, with ell_H proportional to integral_S Q_tau",
            "candidate_only_not_parent_adopted",
            "old Pi_M/topological labels remain residual branches",
        ),
        (
            "PSC1016_7_coupling_descent_silence",
            "matter/source/readout couplings descend through the same observed variables with no hidden source channel",
            "delta_vertical S_matter = delta_vertical S_readout = 0 or source-backed B_obs_source_measure/M_H bound",
            "not_signed_coupling_bound_schema_only",
            "coupling residual can mimic source-measure failure",
        ),
        (
            "PSC1016_8_boundary_reference_lock",
            "reference, exact improvement, and symplectic boundary terms are fixed once",
            "B_zero_flux=0 and Delta_symp=0, or finite source-backed coefficients with units",
            "missing_theorem_or_source_input",
            "boundary bookkeeping can move the measured source charge",
        ),
        (
            "PSC1016_9_verdict",
            "parent-owned source selector for current MTS",
            "PSC1016_0 through PSC1016_8 must be signed before W_source and M_H_ref can support R_eq claims",
            "fail_current_claim",
            "selector contract is exact, but current MTS has not proved the clauses",
        ),
    ]
    return [
        {
            "contract_id": contract_id,
            "required_clause": required_clause,
            "mathematical_form": mathematical_form,
            "current_status": current_status,
            "failure_if_missing": failure_if_missing,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for contract_id, required_clause, mathematical_form, current_status, failure_if_missing in rows
    ]


def theorem_attempt_rows() -> list[dict[str, str]]:
    rows = [
        (
            "PST1016_0_selector_lemma",
            "If PSC1016_0-PSC1016_4 hold, W_source := closure(supp J_H[tau]) is a covariant pre-readout compact source selector.",
            "conditional_lemma_pass",
            "turns worldtube selection from fitted mask into parent structure",
            "current parent action and same-frame source current are unsigned",
        ),
        (
            "PST1016_1_source_measure_lemma",
            "If PSC1016_1, PSC1016_2, PSC1016_5, and PSC1016_8 hold, M_H_ref is a dressed source charge with fixed reference.",
            "conditional_lemma_pass",
            "gives the normalization needed by R_eq/B_zero/I_commutator rows",
            "integrability/reference lock is not derived",
        ),
        (
            "PST1016_2_Hamiltonian_PiM_repair",
            "If PSC1016_6 is adopted and signed, Pi_M is no longer an empirical mass selector but the Hamiltonian charge map.",
            "best_repair_candidate_not_promotion",
            "kills the old conserved-wrong-object loophole if old Pi_M is demoted or mapped to Pi_M^H",
            "old topological equivalence and commutator silence remain unproved",
        ),
        (
            "PST1016_3_coupling_descent_gate",
            "If PSC1016_7 is signed, source/readout coupling leakage cannot masquerade as a mass-measure residual.",
            "schema_only_not_signed",
            "protects local-GR recovery from hidden source-measure coupling",
            "777/778/779 rows are templates with missing parent signatures",
        ),
        (
            "PST1016_4_R_eq_first_input_rule",
            "R_eq, B_zero, and I_commutator may be scored only after M_H_ref, source path, units, and no-cancellation components are real.",
            "runner_rule_written",
            "prevents reference-zero or unnormalized rows from becoming evidence",
            "no first claim-valid input exists",
        ),
        (
            "PST1016_5_verdict",
            "derive parent worldtube-source-measure selector for current MTS",
            "fail_current_claim",
            "the route is precise and viable as a contract, not yet a current-MTS theorem",
            "move next to Hamiltonian PiM reference/integrability lock or source-backed first row",
        ),
    ]
    return [
        {
            "attempt_id": attempt_id,
            "statement": statement,
            "current_status": current_status,
            "would_close": would_close,
            "current_blocker": current_blocker,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for attempt_id, statement, current_status, would_close, current_blocker in rows
    ]


def first_input_schema_rows() -> list[dict[str, str]]:
    rows = [
        (
            "FIS1016_0_M_H_ref",
            "M_H_ref",
            "dressed Hamiltonian/Hilbert source charge used to normalize equality residuals",
            "system_id;tau_id;surface_outer;H_tau;H_ref;M_H_ref;units;reference_rule;source_path;assumptions;valid_for_claim",
            "MISSING_M_H_REF",
            "source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_FIRST_RESIDUAL_INPUT.csv",
        ),
        (
            "FIS1016_1_B_zero_Delta_symp_Href",
            "B_zero_flux;Delta_symp;H_ref_shift",
            "boundary/exact/reference/symplectic shift in the compact linked source charge",
            "system_id;surface_pair;B_zero_flux;Delta_symp;H_ref_shift;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "MISSING_BOUNDARY_REFERENCE_INPUT",
            "source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_FIRST_RESIDUAL_INPUT.csv",
        ),
        (
            "FIS1016_2_worldtube_domain_shift",
            "Delta_worldtube_domain",
            "fractional charge shift under allowed W_source/linking-surface selector choices",
            "system_id;domain_rule;surface_pair;Delta_worldtube_domain;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "MISSING_PARENT_WORLDTUBE_SELECTOR",
            "source-intake/mts_residuals/P8_Y5_R10_662_BOUND_INPUT_TEMPLATE.csv",
        ),
        (
            "FIS1016_3_Delta_frame_source",
            "Delta_frame_source",
            "same-frame source/readout mismatch between matter source, clocks, rods, and orbital frame",
            "system_id;source_frame;readout_frame;Delta_frame_source;local_lock;source_path;assumptions;valid_for_claim",
            "MISSING_FRAME_BOUND_OR_THEOREM",
            "source-intake/mts_residuals/P8_Y5_R10_662_BOUND_INPUT_TEMPLATE.csv",
        ),
        (
            "FIS1016_4_R_eq_integral",
            "R_eq_integral",
            "finite shell integral of Pi_M J_H - J_M_top - dB_zero after M_H_ref normalization",
            "system_id;r1;r2;R_eq_integral;M_H_ref;units;normalization;source_path;assumptions;valid_for_claim",
            "MISSING_R_EQ_INTEGRAL",
            "source-intake/mts_residuals/P8_Y5_R10_1015_R_EQ_BOUND_INPUT_ROWS.csv",
        ),
        (
            "FIS1016_5_I_commutator",
            "I_commutator",
            "finite annulus integral of [d,Pi_M]J_H if the Hamiltonian PiM chain map is unsigned",
            "system_id;r1;r2;I_commutator;M_H_ref;units;normalization;source_path;assumptions;valid_for_claim",
            "MISSING_I_COMMUTATOR",
            "source-intake/mts_residuals/P8_Y5_R10_1015_R_EQ_BOUND_INPUT_ROWS.csv",
        ),
        (
            "FIS1016_6_coupling_descent_certificate",
            "B_obs_source_measure_over_MH",
            "source-measure leakage from coupling/readout descent failure",
            "system_id;source_channel;matter_action_owner;uses_e_obs;uses_q_parent;hidden_frame_map;coupling_descent_status;source_path;valid_for_claim",
            "MISSING_PARENT_SIGNATURE",
            "source-intake/mts_residuals/P8_Y5_R10_777_BOBS_SOURCE_MEASURE_FIRST_PACK.csv",
        ),
        (
            "FIS1016_7_epsilon_selector",
            "epsilon_selector_Meff",
            "no-cancellation envelope of M_H_ref, boundary, frame, domain, R_eq, commutator, and coupling residuals",
            "system_id;epsilon_selector;component_sum_abs;M_H_ref;normalization;source_path;assumptions;valid_for_claim",
            "MISSING_COMPONENT_INPUTS",
            "source-intake/mts_residuals/P8_Y5_R10_779_SOURCE_MEASURE_BOUND_RUNNER.csv",
        ),
    ]
    return [
        {
            "input_id": input_id,
            "quantity": quantity,
            "definition": definition,
            "required_columns": required_columns,
            "current_status": current_status,
            "source_path": path_text,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for input_id, quantity, definition, required_columns, current_status, path_text in rows
    ]


def runner_rows(inputs: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for input_row in inputs:
        reasons = []
        if missing(input_row["current_status"]):
            reasons.append("MISSING_THEOREM_OR_SOURCE_INPUT")
        if not flag(input_row["valid_for_claim"]):
            reasons.append("VALID_FOR_CLAIM_FALSE")
        rows.append(
            {
                "runner_id": input_row["input_id"].replace("FIS1016", "SIR1016"),
                "input_id": input_row["input_id"],
                "quantity": input_row["quantity"],
                "computed_status": "blocked_missing_inputs",
                "claim_allowed": "false",
                "failure_reasons": ";".join(reasons),
                "generated_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, str]]:
    gates = [
        ("CG1016_0_selector_contract_written", "parent worldtube/source-measure selector contract is explicit", "true", "PSC1016 rows define the required parent clauses", "false"),
        ("CG1016_1_selector_lemma_claim", "W_source=supp(J_H) is parent-owned for current MTS", "false", "parent action, same-frame source current, tau, and compactness are unsigned", "false"),
        ("CG1016_2_M_H_ref_claim", "M_H_ref is a fixed dressed Hamiltonian source charge", "false", "integrability/reference/boundary lock is missing", "false"),
        ("CG1016_3_PiM_H_claim", "Pi_M is derived/adopted as Hamiltonian mass-charge map", "false", "Pi_M_H remains candidate only and old topological PiM is demoted unless bounded", "false"),
        ("CG1016_4_first_input_claim_ready", "first R_eq/B_zero/I_commutator row is source-backed and normalized", "false", "all first-input rows carry MISSING status", "false"),
        ("CG1016_5_coupling_descent_zero", "source-measure coupling/readout leakage is theorem-zero", "false", "777/778/779 source-measure rows are schema/blocked only", "false"),
        ("CG1016_6_Newton_local_GR", "Newton/local-GR gates can reopen", "false", "source selector, M_H_ref, PiM_H, calibration, and PPN stability remain blocked", "false"),
        ("CG1016_7_guardrail", "selector/R_eq first-input guardrail is installed", "true", "contract is not promoted and first-input rows stay nonclaim", "false"),
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
            "decision_id": "DEC1016_0_selector_contract",
            "decision": "The legal parent selector is now exact.",
            "because": "W_source may be closure(supp J_H[tau]) only when J_H, e_obs, tau, compactness, linking surfaces, and M_H_ref are parent-owned before readout.",
            "next_action": "try the Hamiltonian PiM reference/integrability lock, not a new topological shortcut",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1016_1_current_MTS_status",
            "decision": "Current MTS does not yet derive the selector.",
            "because": "the support selector is a coherent conditional construction, but the parent action, same-frame source measure, and coupling descent remain unsigned.",
            "next_action": "keep R_worldtube, Delta_frame_source, M_H_ref, B_zero_flux, I_commutator, and coupling residual rows active",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1016_2_first_input_order",
            "decision": "M_H_ref and boundary/reference lock must precede a claim-ready R_eq number.",
            "because": "R_eq, B_zero, and I_commutator are not meaningful evidence until the normalization and reference convention are real.",
            "next_action": "attempt M_H_ref/Delta_symp/B_zero theorem-zero or source-backed first row",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1016_3_next_target",
            "decision": "The next root target is Hamiltonian PiM reference lock or first normalized source row.",
            "because": "without fixed H_tau-H_ref and M_H_ref, no residual row can become scoreable without smuggling the answer.",
            "next_action": "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
            "objective": "derive fixed Hamiltonian reference/integrability and M_H_ref for the local source charge, or fill a source-backed first row for M_H_ref plus B_zero_flux/Delta_symp with units and source path",
            "include": "delta H_tau integrability, fixed H_ref, B_zero_flux, Delta_symp, M_H_ref, tau, surface pair, source path, no readout mask, no cancellation",
            "exclude": "bare mass normalization, reference-only zero, late equality multiplier, unnormalized R_eq row, Newton/local-GR claim, GitHub action",
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
    contract: list[dict[str, str]],
    attempts: list[dict[str, str]],
    inputs: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    required_contracts = {
        "PSC1016_1_single_observed_coframe",
        "PSC1016_2_fixed_time_generator",
        "PSC1016_3_support_selector",
        "PSC1016_5_dressed_source_charge",
        "PSC1016_6_PiM_Hamiltonian_map",
        "PSC1016_7_coupling_descent_silence",
        "PSC1016_9_verdict",
    }
    required_inputs = {
        "M_H_ref",
        "B_zero_flux;Delta_symp;H_ref_shift",
        "Delta_worldtube_domain",
        "Delta_frame_source",
        "R_eq_integral",
        "I_commutator",
        "B_obs_source_measure_over_MH",
        "epsilon_selector_Meff",
    }
    checks = [
        ("V1016_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and needles are present"),
        ("V1016_1_selector_contract_complete", required_contracts.issubset({row["contract_id"] for row in contract}), "selector contract covers coframe, tau, support, charge, PiM, coupling, and verdict"),
        ("V1016_2_contract_blocks_claim", any(row["contract_id"] == "PSC1016_9_verdict" and row["current_status"] == "fail_current_claim" for row in contract) and all(not flag(row["valid_for_claim"]) for row in contract), "selector contract is nonclaim and blocks current MTS promotion"),
        ("V1016_3_theorem_attempt_written", any(row["attempt_id"] == "PST1016_0_selector_lemma" and row["current_status"] == "conditional_lemma_pass" for row in attempts), "conditional selector lemma is written"),
        ("V1016_4_theorem_current_claim_fails", any(row["attempt_id"] == "PST1016_5_verdict" and row["current_status"] == "fail_current_claim" for row in attempts), "current theorem route fails without parent signatures"),
        ("V1016_5_input_schema_complete", required_inputs.issubset({row["quantity"] for row in inputs}), "first-input schema covers normalization, boundary, frame, domain, R_eq, commutator, coupling, and envelope"),
        ("V1016_6_input_schema_nonclaim", all(not flag(row["valid_for_claim"]) and missing(row["current_status"]) for row in inputs), "all first-input rows remain missing and nonclaim"),
        ("V1016_7_runner_refuses", len(runner) == len(inputs) and all(row["computed_status"] == "blocked_missing_inputs" and not flag(row["claim_allowed"]) for row in runner), "runner refuses all missing first-input rows"),
        ("V1016_8_claim_gates_blocked", all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in gates), "selector, source-measure, Newton, and local-GR claims remain blocked"),
        ("V1016_9_guardrail_written", any(row["gate_id"] == "CG1016_7_guardrail" and flag(row["gate_pass"]) for row in gates), "selector/R_eq guardrail is installed"),
        ("V1016_10_decision_written", any(row["decision_id"] == "DEC1016_3_next_target" for row in decisions), "1017 root target decision is written"),
        ("V1016_11_next_target_written", len(next_target) == 1 and "1017-Y5-R10-Hamiltonian-PiM-reference-lock" in next_target[0]["next_target"], "1017 target row is present and nonclaim"),
        ("V1016_12_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1016_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1016 parent worldtube/source-measure selector validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    contract: list[dict[str, str]],
    attempts: list[dict[str, str]],
    inputs: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1016 Y5 R10 parent worldtube source-measure selector or R_eq first input",
            "",
            "**Status:** The legal selector contract is now explicit: `W_source = closure(supp J_H[tau])` is a valid pre-readout source worldtube only if the parent action owns `J_H`, `e_obs`, `tau`, compact support, linking surfaces, `M_H_ref`, `Pi_M^H`, boundary/reference locks, and coupling descent. Current MTS has not yet signed those clauses.",
            "",
            "**Claim ceiling:** no parent selector, source-measure equality, `R_eq` score, measured-GM closure, Newton/GR reduction, R10/R11 pass, PPN pass, or local-GR claim is allowed from 1016.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Parent selector contract",
            md_table(contract, ["contract_id", "required_clause", "mathematical_form", "current_status", "failure_if_missing", "valid_for_claim"]),
            "## Theorem attempt",
            md_table(attempts, ["attempt_id", "statement", "current_status", "would_close", "current_blocker", "valid_for_claim"]),
            "## First input schema",
            md_table(inputs, ["input_id", "quantity", "definition", "required_columns", "current_status", "valid_for_claim"]),
            "## First input runner",
            md_table(runner, ["runner_id", "input_id", "quantity", "computed_status", "claim_allowed", "failure_reasons"]),
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
    contract = selector_contract_rows()
    attempts = theorem_attempt_rows()
    inputs = first_input_schema_rows()
    runner = runner_rows(inputs)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, contract, attempts, inputs, runner, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1016_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv", contract)
    write_csv(OUT / "P8_Y5_R10_1016_SELECTOR_THEOREM_ATTEMPT.csv", attempts)
    write_csv(OUT / "P8_Y5_R10_1016_FIRST_INPUT_SCHEMA.csv", inputs)
    write_csv(OUT / "P8_Y5_R10_1016_FIRST_INPUT_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1016_CLAIM_GATE.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1016_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1016_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1016_VALIDATION.csv", validations)
    write_doc(sources, contract, attempts, inputs, runner, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()
