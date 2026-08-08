from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "991-Y5-R10-Hamiltonian-PiM-FB5540-integrability-reference-lock-or-source-closure.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "990_doc",
            "path": "990-Y5-R10-minimal-parent-action-coupling-contract-EM-matter-GR-reentry.md",
            "role": "immediate parent-action handoff selecting Hamiltonian PiM/FB554_0",
            "needle": "Hamiltonian `Pi_M`/`FB554_0` source-mass obstruction",
        },
        {
            "source_id": "990_contract",
            "path": "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
            "role": "minimal parent-action contract with source-charge clause",
            "needle": "PAC990_4_source_charge",
        },
        {
            "source_id": "990_ladder",
            "path": "source-intake/mts_residuals/P8_Y5_R10_990_GR_NEWTON_REENTRY_LADDER.csv",
            "role": "GR/Newton reentry ladder selecting source mass",
            "needle": "LAD990_2_source_mass",
        },
        {
            "source_id": "768_doc",
            "path": "768-Y5-R10-local-GR-EH-or-R11-reentry-after-alpha-WEP-quarantine.md",
            "role": "local GR reentry and Hamiltonian PiM live edge",
            "needle": "FB554_0_HPiM_integrability_reference_bound",
        },
        {
            "source_id": "768_HPiM",
            "path": "source-intake/mts_residuals/P8_Y5_R10_768_HAMILTONIAN_PIM_LIVE_EDGE.csv",
            "role": "Hamiltonian PiM component target rows",
            "needle": "HPI768_0_integrability_target",
        },
        {
            "source_id": "769_doc",
            "path": "769-Y5-R10-FB554-0-Hamiltonian-integrability-reference-row-reentry.md",
            "role": "FB554_0 theorem contract and obstruction split",
            "needle": "FBR769_0_definition",
        },
        {
            "source_id": "769_contract",
            "path": "source-intake/mts_residuals/P8_Y5_R10_769_FB5540_REENTRY_THEOREM_CONTRACT.csv",
            "role": "FB554_0 theorem contract",
            "needle": "FBR769_0_definition",
        },
        {
            "source_id": "770_doc",
            "path": "770-Y5-R10-Hamiltonian-integrability-parent-action-clause-or-FB5540-component-fill.md",
            "role": "parent action certificate and fallback component fill",
            "needle": "theta_total/Q_tau",
        },
        {
            "source_id": "770_parent_action",
            "path": "source-intake/mts_residuals/P8_Y5_R10_770_PARENT_ACTION_CERTIFICATE_AUDIT.csv",
            "role": "Hamiltonian current certificate audit",
            "needle": "HIC770_0_parent_action_domain",
        },
        {
            "source_id": "771_doc",
            "path": "771-Y5-R10-theta-Qtau-current-owner-or-deltaH-component-source-row.md",
            "role": "theta/Q_tau current owner attempt",
            "needle": "D771_1_select_hybrid_route",
        },
        {
            "source_id": "772_doc",
            "path": "772-Y5-R10-hybrid-EH-quotient-current-owner-or-deltaH-curl-source-fill.md",
            "role": "hybrid current owner and narrow representative-zero imports",
            "needle": "HCO772_7_owner_verdict",
        },
        {
            "source_id": "773_doc",
            "path": "773-Y5-R10-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md",
            "role": "observed reduced boundary/source flux zero attempt",
            "needle": "B_observed_reduced_flux_over_MH",
        },
        {
            "source_id": "774_symbol_match",
            "path": "source-intake/mts_residuals/P8_Y5_R10_774_REDUCED_GK_SYMBOL_MATCH_REENTRY_AUDIT.csv",
            "role": "reduced GK symbol match reentry audit",
            "needle": "RGM774_7_verdict",
        },
        {
            "source_id": "776_variation",
            "path": "source-intake/mts_residuals/P8_Y5_R10_776_RESPONSE_DISPLACEMENT_VARIATION_LEDGER.csv",
            "role": "formal response-displacement double-zero ledger",
            "needle": "RAV776_2_formal_double_zero",
        },
        {
            "source_id": "777_lock_map",
            "path": "source-intake/mts_residuals/P8_Y5_R10_777_PHYSICAL_RESIDUAL_LOCK_MAP.csv",
            "role": "physical residual lock map failure",
            "needle": "PRL777_6_verdict",
        },
        {
            "source_id": "778_coupling",
            "path": "source-intake/mts_residuals/P8_Y5_R10_778_COUPLING_DESCENT_THEOREM_GATE.csv",
            "role": "conditional coupling descent theorem",
            "needle": "CDT778_7_theorem_result",
        },
        {
            "source_id": "779_runner",
            "path": "source-intake/mts_residuals/P8_Y5_R10_779_SOURCE_MEASURE_BOUND_RUNNER.csv",
            "role": "source-measure bound runner proving current inputs are blocked",
            "needle": "SMR779_2_local_branch_rule",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                "source_id": spec["source_id"],
                "role": spec["role"],
                "path": spec["path"],
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "needle": spec["needle"],
                "valid_for_claim": "false",
            }
        )
    return rows


def component_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "component_id": "FB991_0_deltaH_integrability",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "formula_or_gate": "curl(delta H_tau)=delta int_S(delta Q_tau - i_tau theta); require delta^2 H_tau=0",
            "current_evidence": "768/769/770/771 keep theta_total, Q_tau, constraint split, and curl test unsigned",
            "status": "blocked_missing_parent_current_owner",
            "blocks": "observed Hamiltonian source mass and Newtonian GM normalization",
            "next_action": "extract theta_total and Q_tau from explicit parent L, or source-fill nonintegrable curl row",
            "valid_for_claim": "false",
        },
        {
            "component_id": "FB991_1_reference_lock",
            "quantity": "Delta_ref_over_MH",
            "formula_or_gate": "H_tau=surface_charge - B_ref with B_ref fixed before source/orbit readout",
            "current_evidence": "769/770 preserve reference silence as a first-order obstruction",
            "status": "blocked_missing_fixed_B_ref_owner",
            "blocks": "source mass can be hidden in the subtraction convention",
            "next_action": "parent-sign B_ref or retain Delta_ref component with units and source path",
            "valid_for_claim": "false",
        },
        {
            "component_id": "FB991_2_symplectic_boundary_flux",
            "quantity": "symplectic_boundary_flux_over_MH",
            "formula_or_gate": "no extra theta, corner, edge, projector, or observed boundary/source metric-variation flux",
            "current_evidence": "772 prunes representative-only flux, but 773-779 keep observed B_obs and source-measure flux alive",
            "status": "blocked_observed_flux_not_zero",
            "blocks": "deltaH curl zero and local-GR source closure",
            "next_action": "derive observed no-flux theorem or use B_obs component bound rows",
            "valid_for_claim": "false",
        },
        {
            "component_id": "FB991_3_tau_MHref_lock",
            "quantity": "tau_mismatch_and_MHref_denominator",
            "formula_or_gate": "same tau generator and same M_H_ref denominator in charge, orbit, clock, PPN, and R10 branches",
            "current_evidence": "768-771 require tau lock and M_H_ref normalization before source equality",
            "status": "blocked_same_frame_denominator_unsigned",
            "blocks": "comparing orbital GM to Hamiltonian charge without a hidden frame map",
            "next_action": "write same-frame tau/M_H_ref certificate or retain mismatch residual",
            "valid_for_claim": "false",
        },
        {
            "component_id": "FB991_4_coupling_source_measure",
            "quantity": "B_obs_source_measure_over_MH",
            "formula_or_gate": "matter/source/readout descent makes source-measure work zero, or finite no-cancellation bound is sourced",
            "current_evidence": "779 runner finds 0 valid rows and all coupling/source/readout/PPN response routes missing or nonclaim",
            "status": "blocked_missing_coupling_signature_or_numeric_bound",
            "blocks": "using measured source mass as if it were already parent-owned",
            "next_action": "prove parent coupling owner or carry finite coupling residual into tests",
            "valid_for_claim": "false",
        },
        {
            "component_id": "FB991_5_same_frame_source_equality",
            "quantity": "M_H_tau_minus_M_observed_source",
            "formula_or_gate": "M_H_tau from Pi_M/Hamiltonian charge equals observed source current before orbital calibration",
            "current_evidence": "source equality is explicitly downstream of FB554_0; orbital GM substitution is disallowed",
            "status": "blocked_downstream_of_FB5540",
            "blocks": "Newtonian limit, PPN, R10, Gdot, and orbit claims",
            "next_action": "after FB554_0 components close, derive Hilbert-current/Pi_M/source equality",
            "valid_for_claim": "false",
        },
    ]


def theorem_route_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "HPT991_0_parent_L_owner",
            "theorem_clause": "explicit parent Lagrangian and variation owner",
            "required_object": "L_parent[Phi,Psi] with theta_total and Q_tau obtained by variation",
            "current_status": "not_signed",
            "why": "770/771 do not extract theta_total and Q_tau from a complete current MTS parent L",
            "claim_effect": "no Hamiltonian integrability theorem",
            "valid_for_claim": "false",
        },
        {
            "route_id": "HPT991_1_integrability_curl",
            "theorem_clause": "deltaH one-form is closed on allowed solution space",
            "required_object": "delta(int_S(delta Q_tau - i_tau theta))=0 after constraints and allowed boundary variations",
            "current_status": "not_evaluated_current_corpus",
            "why": "curl identity exists, but the required current and boundary objects are not explicit",
            "claim_effect": "FB554_0 cannot be set to zero",
            "valid_for_claim": "false",
        },
        {
            "route_id": "HPT991_2_reference_lock",
            "theorem_clause": "fixed reference subtraction",
            "required_object": "B_ref chosen by parent boundary condition, not fit to source mass",
            "current_status": "not_signed",
            "why": "reference silence remains a named obstruction in 769 and 770",
            "claim_effect": "mass normalization can hide in reference choice",
            "valid_for_claim": "false",
        },
        {
            "route_id": "HPT991_3_tau_lock",
            "theorem_clause": "same observed time generator",
            "required_object": "one tau_obs used for Hamiltonian charge, local clocks, orbits, PPN, R10, and Gdot",
            "current_status": "not_signed",
            "why": "same-frame denominator/tau lock remains blocked",
            "claim_effect": "no cross-arena source equality",
            "valid_for_claim": "false",
        },
        {
            "route_id": "HPT991_4_boundary_flux_silence",
            "theorem_clause": "no observed symplectic/boundary/source flux",
            "required_object": "B_obs_bulk, boundary, source, corner, and projector components theorem-zero or bounded",
            "current_status": "fails_current_inputs",
            "why": "773-779 stage B_obs components and show coupling/source-measure route is blocked",
            "claim_effect": "deltaH zero and local-GR reentry remain blocked",
            "valid_for_claim": "false",
        },
        {
            "route_id": "HPT991_5_representative_zero_not_enough",
            "theorem_clause": "representative/vertical zeros cannot be reused as observed zeros",
            "required_object": "observed reduced source/boundary/readout descent",
            "current_status": "guard_passed_nonclaim",
            "why": "772 gives narrow credit only for representative ghost channels; 777 warns auxiliary R=0 is not physical residual zero",
            "claim_effect": "prevents fake local-GR proof",
            "valid_for_claim": "false",
        },
        {
            "route_id": "HPT991_6_coupling_descent",
            "theorem_clause": "matter/source/readout descent through one observed geometry",
            "required_object": "quotient-invariant matter/source/readout/EM/PPN signatures or numeric residual bounds",
            "current_status": "blocked_by_779",
            "why": "signature runner has 0 valid rows across descent, C_qmu, flux, readout, and PPN response inputs",
            "claim_effect": "source-measure flux remains live",
            "valid_for_claim": "false",
        },
        {
            "route_id": "HPT991_7_verdict",
            "theorem_clause": "FB554_0=0 promotion",
            "required_object": "all clauses above close without placeholders, cancellations, or orbital-GM substitution",
            "current_status": "not_promoted",
            "why": "at least five first-order clauses are unsigned",
            "claim_effect": "no Newton, PPN, R10, Gdot, R11, or local-GR claim",
            "valid_for_claim": "false",
        },
    ]


def fallback_schema_rows() -> list[dict[str, str]]:
    base = "source-intake/mts_residuals"
    return [
        {
            "schema_id": "FBS991_0_deltaH_curl_input",
            "target_quantity": "delta_H_tau_nonintegrable_over_MH",
            "candidate_artifact": f"{base}/P8_Y5_R10_991_DELTAH_CURL_INPUT_CANDIDATE.csv",
            "required_columns": "system_id;surface_id;tau_id;theta_owner;Qtau_owner;curl_value;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_THETA_QTAU_CURL_SOURCE",
            "promotion_gate": "numeric/theorem row with theta_total and Q_tau source paths, positive M_H_ref, and no MISSING markers",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "FBS991_1_reference_input",
            "target_quantity": "Delta_ref_over_MH",
            "candidate_artifact": f"{base}/P8_Y5_R10_991_REFERENCE_LOCK_INPUT_CANDIDATE.csv",
            "required_columns": "system_id;B_ref_owner;reference_class;Delta_ref;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_FIXED_REFERENCE_OWNER",
            "promotion_gate": "fixed parent boundary/reference rule or sourced finite reference residual",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "FBS991_2_boundary_flux_input",
            "target_quantity": "symplectic_boundary_flux_over_MH",
            "candidate_artifact": f"{base}/P8_Y5_R10_991_SYMPLECTIC_BOUNDARY_FLUX_INPUT_CANDIDATE.csv",
            "required_columns": "system_id;component;flux_value;M_H_ref;units;source_path;no_cancellation_flag;valid_for_claim",
            "current_status": "MISSING_OBSERVED_BOUNDARY_FLUX_ZERO_OR_BOUND",
            "promotion_gate": "observed no-flux theorem or component-wise positive bound with no cancellation credit",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "FBS991_3_tau_MHref_input",
            "target_quantity": "tau_mismatch_and_MHref_denominator",
            "candidate_artifact": f"{base}/P8_Y5_R10_991_TAU_MHREF_LOCK_INPUT_CANDIDATE.csv",
            "required_columns": "system_id;tau_charge;tau_clock;tau_orbit;tau_PPN;M_H_ref;frame_map;source_path;valid_for_claim",
            "current_status": "MISSING_SAME_FRAME_TAU_MHREF_CERTIFICATE",
            "promotion_gate": "all arenas use same tau and denominator or mismatch is retained as finite residual",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "FBS991_4_coupling_source_measure_input",
            "target_quantity": "B_obs_source_measure_over_MH",
            "candidate_artifact": f"{base}/P8_Y5_R10_991_SOURCE_MEASURE_COUPLING_INPUT_CANDIDATE.csv",
            "required_columns": "system_id;coupling_channel;descent_status;C_qmu;flux_value;readout_response;PPN_response;M_H_ref;units;source_path;valid_for_claim",
            "current_status": "MISSING_COUPLING_SIGNATURE_OR_NUMERIC_BOUND",
            "promotion_gate": "779 blockers replaced by sourced zero theorem or finite no-cancellation numeric bound",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "FBS991_5_source_equality_input",
            "target_quantity": "M_H_tau_minus_M_observed_source",
            "candidate_artifact": f"{base}/P8_Y5_R10_991_SOURCE_EQUALITY_INPUT_CANDIDATE.csv",
            "required_columns": "system_id;Hamiltonian_charge;Hilbert_source_current;Pi_M_Gauss_rule;orbital_calibration_rule;difference_value;units;source_path;valid_for_claim",
            "current_status": "MISSING_SOURCE_EQUALITY_AFTER_FB5540",
            "promotion_gate": "source equality derived before orbital GM substitution",
            "valid_for_claim": "false",
        },
    ]


def representative_zero_credit_rows() -> list[dict[str, str]]:
    return [
        {
            "credit_id": "RZC991_0_representative_vertical_zero",
            "input": "772 narrow representative vertical zero",
            "credit_allowed": "prunes representative-only ghost channels",
            "credit_forbidden": "cannot kill observed boundary/source/readout flux",
            "surviving_obstruction": "B_obs observed reduced flux and source-measure coupling",
            "valid_for_claim": "false",
        },
        {
            "credit_id": "RZC991_1_response_double_zero",
            "input": "776 formal gamma_R quadratic double-zero",
            "credit_allowed": "gives a plausible auxiliary mechanism for F_1=0",
            "credit_forbidden": "cannot prove physical residual vector zero without full-rank lock",
            "surviving_obstruction": "q_loc/Y5/Y6/PPN/boundary/coupling residual lock",
            "valid_for_claim": "false",
        },
        {
            "credit_id": "RZC991_2_coupling_descent_conditional",
            "input": "778 conditional coupling descent theorem",
            "credit_allowed": "would set source-measure coupling work to zero if parent signatures close",
            "credit_forbidden": "cannot set B_obs_source_measure=0 under current 779 runner",
            "surviving_obstruction": "all coupling/source/readout/PPN candidate routes are missing or nonclaim",
            "valid_for_claim": "false",
        },
        {
            "credit_id": "RZC991_3_EH_only_reference",
            "input": "EH or GR baseline identities",
            "credit_allowed": "useful reference for theta/Q_tau shape and ADM-style charge discipline",
            "credit_forbidden": "does not prove MTS source mass, B_ref, tau lock, or retained operator silence",
            "surviving_obstruction": "MTS parent current owner and source equality",
            "valid_for_claim": "false",
        },
    ]


def live_priority_rows() -> list[dict[str, str]]:
    return [
        {
            "priority_id": "PRI991_0_HPiM_current_owner",
            "rank": "1",
            "live_target": "theta_total/Q_tau plus integrability curl",
            "why_first": "without this, source mass is not a Hamiltonian charge",
            "best_route": "derive from explicit parent L or write deltaH curl input row",
            "valid_for_claim": "false",
        },
        {
            "priority_id": "PRI991_1_reference_tau_lock",
            "rank": "2",
            "live_target": "B_ref, tau_obs, M_H_ref same-frame certificate",
            "why_first": "prevents hidden source-mass normalization through convention",
            "best_route": "fixed boundary/reference rule before readout",
            "valid_for_claim": "false",
        },
        {
            "priority_id": "PRI991_2_observed_flux",
            "rank": "3",
            "live_target": "observed B_obs boundary/source/projector flux",
            "why_first": "representative zeros do not cover observed reduced flux",
            "best_route": "observed no-flux theorem or component-wise source pack",
            "valid_for_claim": "false",
        },
        {
            "priority_id": "PRI991_3_coupling_source_measure",
            "rank": "4",
            "live_target": "parent coupling descent or finite source-measure bound",
            "why_first": "coupling leakage can fake measured-GM, clock, orbit, EM, and PPN readouts",
            "best_route": "replace 779 missing rows with parent signatures or numeric bounds",
            "valid_for_claim": "false",
        },
        {
            "priority_id": "PRI991_4_PPN_response",
            "rank": "5",
            "live_target": "weak-field/PPN response after source charge is owned",
            "why_first": "PPN scoring is downstream, not a substitute for source charge",
            "best_route": "linearized operator and source-charge readout matrix",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG991_0_FB5540_zero",
            "claim": "FB554_0=0",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "integrability, reference, tau, observed flux, coupling, and source equality clauses remain unsigned",
        },
        {
            "gate_id": "CG991_1_Newton_source",
            "claim": "Hamiltonian source mass equals Newtonian/observed GM",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "source equality is downstream and orbital GM substitution is forbidden",
        },
        {
            "gate_id": "CG991_2_local_GR_PPN_R10",
            "claim": "local GR, PPN, R10, R11, Gdot, or orbit pass",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "source charge and boundary/coupling residuals are not closed",
        },
        {
            "gate_id": "CG991_3_parent_action_derivation",
            "claim": "parent action has been derived",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "991 is a contract/gate consolidation, not a full parent Lagrangian derivation",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC991_0_zero_proof_attempt",
            "decision": "do not promote FB554_0 zero proof",
            "reason": "the exact theorem route still lacks parent current, reference, tau, flux, and coupling signatures",
            "effect": "local branch remains alive but blocked",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC991_1_source_closure_pack",
            "decision": "stage source-closure fallback rows without candidate data",
            "reason": "if the zero theorem does not close, every live component needs a source-backed bound",
            "effect": "future work has a no-handwaving input contract",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC991_2_next_target",
            "decision": "target Hamiltonian PiM source-current descent next",
            "reason": "theta/Q_tau integrability and M_H source equality are closest to the GR/Newton reduction spine",
            "effect": "attack source charge directly before PPN/R10 scoring",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "992-Y5-R10-Hamiltonian-PiM-source-current-descent-or-FB5540-component-bound-pack.md",
            "objective": "derive the Hamiltonian source-current/Pi_M descent that makes observed source mass a parent-owned charge, or create explicit nonclaim component-bound inputs",
            "include": "theta_total/Q_tau extraction, Hilbert source current, Pi_M/Gauss normalization, B_ref/tau lock, source equality before orbital calibration",
            "exclude": "PPN/R10/local-GR pass, orbital GM substitution, invented source-charge coefficients, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_timestamp:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    components: list[dict[str, str]],
    theorem: list[dict[str, str]],
    fallback: list[dict[str, str]],
    credit: list[dict[str, str]],
    priorities: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    component_ok = all(row["valid_for_claim"] == "false" for row in components) and any(row["component_id"] == "FB991_0_deltaH_integrability" for row in components)
    theorem_ok = all(row["valid_for_claim"] == "false" for row in theorem) and theorem[-1]["current_status"] == "not_promoted"
    fallback_ok = all(row["valid_for_claim"] == "false" and "MISSING" in row["current_status"] for row in fallback)
    credit_ok = all(row["valid_for_claim"] == "false" and row["credit_forbidden"] for row in credit)
    priority_ok = priorities and priorities[0]["priority_id"] == "PRI991_0_HPiM_current_owner"
    claims_ok = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims)
    decision_ok = any(row["decision_id"] == "DEC991_2_next_target" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V991_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all cited local source files exist and expected needles are found"},
        {"check_id": "V991_1_component_gate_nonclaim", "result": "pass" if component_ok else "fail", "detail": "FB554_0 component gate is complete and nonclaim"},
        {"check_id": "V991_2_theorem_not_promoted", "result": "pass" if theorem_ok else "fail", "detail": "Hamiltonian PiM zero theorem is explicitly not promoted"},
        {"check_id": "V991_3_fallback_schema_fail_closed", "result": "pass" if fallback_ok else "fail", "detail": "fallback source rows stay MISSING and valid_for_claim=false"},
        {"check_id": "V991_4_representative_credit_limited", "result": "pass" if credit_ok else "fail", "detail": "representative/formal zeros cannot be reused as observed local-GR proof"},
        {"check_id": "V991_5_priority_order", "result": "pass" if priority_ok else "fail", "detail": "theta_total/Q_tau Hamiltonian current owner remains first priority"},
        {"check_id": "V991_6_claim_gates_safe", "result": "pass" if claims_ok else "fail", "detail": "FB554_0, Newton, PPN/R10/local-GR, and parent-action claims are blocked"},
        {"check_id": "V991_7_decision_written", "result": "pass" if decision_ok else "fail", "detail": "next derivation target is selected"},
        {"check_id": "V991_8_next_target_written", "result": "pass" if next_ok else "fail", "detail": "992 source-current descent target is present and nonclaim"},
        {"check_id": "V991_9_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {
            "check_id": "V991_READY",
            "result": "pass" if ready else "fail",
            "detail": "991 checkpoint pack validation summary",
            "generated_utc": stamp(),
        }
    ]


def write_doc(
    sources: list[dict[str, str]],
    components: list[dict[str, str]],
    theorem: list[dict[str, str]],
    fallback: list[dict[str, str]],
    credit: list[dict[str, str]],
    priorities: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 991 Y5 R10: Hamiltonian PiM FB554_0 Integrability, Reference Lock, Or Source Closure",
        "",
        "Status: `Y5_R10_991_Hamiltonian_PiM_FB5540_zero_not_promoted_source_closure_pack_staged_nonclaim`",
        "",
        "Claim ceiling: no `FB554_0=0`, no Newton/source-mass equality, no PPN/R10/R11/Gdot/orbit/local-GR pass, no parent-action derivation claim.",
        "",
        "## Readout",
        "",
        "991 takes the 990 parent-action contract into the actual GR/Newton bottleneck: the observed source mass has to be an integrable Hamiltonian/Pi_M charge before the theory can honestly reduce to Newton in the GR sense.",
        "",
        "The result is useful but strict. The theorem route is now exact enough to be tested, but current MTS does not yet sign the needed parent current, fixed reference, tau lock, observed boundary/source flux silence, coupling descent, or source equality. So `FB554_0=0` is not claimed. The win is that the missing teeth are now named and fail-closed instead of living as fog.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## FB554_0 Consolidated Component Gate",
        "",
        md_table(components, ["component_id", "quantity", "formula_or_gate", "current_evidence", "status", "blocks", "next_action", "valid_for_claim"]),
        "",
        "## Theorem Route Audit",
        "",
        md_table(theorem, ["route_id", "theorem_clause", "required_object", "current_status", "why", "claim_effect", "valid_for_claim"]),
        "",
        "## Source Closure Fallback Schema",
        "",
        md_table(fallback, ["schema_id", "target_quantity", "candidate_artifact", "required_columns", "current_status", "promotion_gate", "valid_for_claim"]),
        "",
        "## Representative Zero Credit Ledger",
        "",
        md_table(credit, ["credit_id", "input", "credit_allowed", "credit_forbidden", "surviving_obstruction", "valid_for_claim"]),
        "",
        "## Live Obstruction Priority",
        "",
        md_table(priorities, ["priority_id", "rank", "live_target", "why_first", "best_route", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "claim_allowed", "why_not"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register()
    components = component_gate_rows()
    theorem = theorem_route_rows()
    fallback = fallback_schema_rows()
    credit = representative_zero_credit_rows()
    priorities = live_priority_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, components, theorem, fallback, credit, priorities, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_991_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_991_FB5540_CONSOLIDATED_COMPONENT_GATE.csv", components)
    write_csv(OUT / "P8_Y5_R10_991_THEOREM_ROUTE_AUDIT.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_991_SOURCE_CLOSURE_FALLBACK_SCHEMA.csv", fallback)
    write_csv(OUT / "P8_Y5_R10_991_REPRESENTATIVE_ZERO_CREDIT_LEDGER.csv", credit)
    write_csv(OUT / "P8_Y5_R10_991_LIVE_OBSTRUCTION_PRIORITY.csv", priorities)
    write_csv(OUT / "P8_Y5_R10_991_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_991_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_991_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_991_VALIDATION.csv", validation)
    write_doc(sources, components, theorem, fallback, credit, priorities, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
