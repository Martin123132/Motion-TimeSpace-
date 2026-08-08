from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "992-Y5-R10-Hamiltonian-PiM-source-current-descent-or-FB5540-component-bound-pack.md"
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
            "source_id": "991_doc",
            "path": "991-Y5-R10-Hamiltonian-PiM-FB5540-integrability-reference-lock-or-source-closure.md",
            "role": "immediate handoff selecting Hamiltonian PiM source-current descent",
            "needle": "DEC991_2_next_target",
        },
        {
            "source_id": "991_component_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_991_FB5540_CONSOLIDATED_COMPONENT_GATE.csv",
            "role": "FB554_0 component gate",
            "needle": "FB991_5_same_frame_source_equality",
        },
        {
            "source_id": "991_theorem",
            "path": "source-intake/mts_residuals/P8_Y5_R10_991_THEOREM_ROUTE_AUDIT.csv",
            "role": "theorem route audit blocking FB554_0 zero",
            "needle": "HPT991_7_verdict",
        },
        {
            "source_id": "768_HPiM",
            "path": "source-intake/mts_residuals/P8_Y5_R10_768_HAMILTONIAN_PIM_LIVE_EDGE.csv",
            "role": "Hamiltonian PiM live edge rows",
            "needle": "HPI768_4_source_equality_downstream",
        },
        {
            "source_id": "768_source_edge",
            "path": "source-intake/mts_residuals/P8_Y5_R10_768_R11_SOURCE_NORMALIZATION_LIVE_EDGE.csv",
            "role": "source normalization live edge and Pi_M repair candidate",
            "needle": "RSN768_4_HPiM_repair",
        },
        {
            "source_id": "p8_source_current",
            "path": "source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv",
            "role": "source-current Ward/universality contract",
            "needle": "SC6_closed_calibrated_mass_projector",
        },
        {
            "source_id": "p8_mass_charge",
            "path": "source-intake/mts_residuals/P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
            "role": "mass current to Hamiltonian boundary charge contract",
            "needle": "HC4_charge_equals_PiM_Hilbert_mass",
        },
        {
            "source_id": "p8_poisson_gauss",
            "path": "source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
            "role": "Hamiltonian charge to Poisson/Gauss calibration contract",
            "needle": "PG1_charge_equals_projected_Hilbert_source",
        },
        {
            "source_id": "p8_pim_flux",
            "path": "source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
            "role": "Pi_M flux closure and topological route contract",
            "needle": "FC2_closed_mass_current_equation",
        },
        {
            "source_id": "p8_parent_identity_decision",
            "path": "source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_DECISION.csv",
            "role": "parent source identity decision",
            "needle": "D499_4_promotion",
        },
        {
            "source_id": "p8_parent_identity_residuals",
            "path": "source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv",
            "role": "projected source identity residual decomposition",
            "needle": "S499_7_parent_anomaly_or_multiplier",
        },
        {
            "source_id": "p8_topological_pim_decision",
            "path": "source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_DECISION.csv",
            "role": "topological Pi_M current decision",
            "needle": "D500_1_Hilbert_equality",
        },
        {
            "source_id": "p8_charge_equality_status",
            "path": "source-intake/mts_residuals/P8_charge_current_equality_STATUS.csv",
            "role": "direct charge-current equality status",
            "needle": "Newtonian reduction promoted",
        },
        {
            "source_id": "p8_charge_equality_residuals",
            "path": "source-intake/mts_residuals/P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
            "role": "charge-current equality residual decomposition",
            "needle": "Delta_PPN",
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


def descent_theorem_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "SCD992_0_parent_action_current",
            "descent_clause": "derive theta_total and Q_tau from one parent action",
            "mathematical_form": "delta L_parent = E_i delta Phi^i + d theta_total; J_tau=theta_total(L_tau Phi)-i_tau L_parent; J_tau=dQ_tau+C_tau",
            "would_imply": "Hamiltonian charge is owned before any source-current equality is attempted",
            "current_status": "blocked_by_991_HPT991_0",
            "missing": "explicit L_parent, theta_total, Q_tau, constraints C_tau, boundary policy",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SCD992_1_integrable_charge",
            "descent_clause": "make H_tau finite, differentiable, and integrable",
            "mathematical_form": "delta H_tau = int_S(delta Q_tau - i_tau theta_total), with delta^2 H_tau=0 and fixed B_ref",
            "would_imply": "M_H_tau can be a physical source-mass candidate",
            "current_status": "blocked_by_991_FB991_0_FB991_1",
            "missing": "curl evaluation, B_ref owner, tau lock, zero observed symplectic flux",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SCD992_2_Hilbert_current_definition",
            "descent_clause": "define the observed Hilbert source current from the same matter action",
            "mathematical_form": "T_H^{mu nu}=2/sqrt(-g_obs) delta S_matter/delta g_obs_mu_nu; J_H[tau]=T_H^{mu nu} tau_nu dSigma_mu",
            "would_imply": "ordinary source current is not a separate fitted object",
            "current_status": "conditional_standard_identity_only",
            "missing": "parent-signed matter functor, one observed coframe, no hidden source/readout map",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SCD992_3_PiM_chain_map",
            "descent_clause": "prove Pi_M is a parent-owned chain map on the mass channel",
            "mathematical_form": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H; require [d,Pi_M]J_H=0 or source-bound it",
            "would_imply": "projected Hilbert mass flux is closed in the compact exterior",
            "current_status": "not_parent_derived",
            "missing": "Pi_M algebra, commutator silence, domain/homology policy, projector variation terms",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SCD992_4_charge_current_equality",
            "descent_clause": "identify Hamiltonian charge with projected Hilbert source current",
            "mathematical_form": "M_H_tau = G_ref^-1 int_S Q_tau = M_eff[Pi_M J_H] + residuals",
            "would_imply": "source equality can replace closure language",
            "current_status": "failed_current_corpus",
            "missing": "Delta_frame, Delta_nonEH, Delta_symp, Delta_PiM, Delta_extra, Delta_flux, Delta_G, Delta_cal, Delta_PPN zero or bounds",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SCD992_5_Poisson_Gauss_orbital_calibration",
            "descent_clause": "only after equality, calibrate to Poisson/Gauss/orbital mass",
            "mathematical_form": "nabla^2 Phi = 4*pi*G_ref rho_H and int grad Phi*dS = 4*pi*G_ref M_H_tau",
            "would_imply": "Newtonian inverse-square normalization is derived rather than borrowed",
            "current_status": "downstream_not_ready",
            "missing": "EH/R11 weak-field operator, same-frame potential, Gauss surface integral, no derivative/source hair",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SCD992_6_verdict",
            "descent_clause": "promote Hamiltonian Pi_M source-current descent",
            "mathematical_form": "SCD992_0 through SCD992_5 all pass with no placeholders",
            "would_imply": "Newton source normalization becomes derivable input to PPN/R10/orbit tests",
            "current_status": "not_promoted",
            "missing": "the first two clauses already fail under 991, and source equality is downstream",
            "valid_for_claim": "false",
        },
    ]


def residual_ledger_rows() -> list[dict[str, str]]:
    return [
        {
            "residual_id": "SCE992_Delta_frame",
            "symbolic_piece": "B_tau[e_charge]/G_eff - B_tau[e_obs]/G_eff",
            "meaning": "Hamiltonian charge generated in a different frame or normalization than matter/orbit readout",
            "source_basis": "P8_charge_current_equality_RESIDUAL_DECOMPOSITION Delta_frame",
            "status": "unbounded",
            "required_exit": "same observed coframe/time and no hidden frame map",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "SCE992_Delta_nonEH",
            "symbolic_piece": "sum_i c_i Q_i^nonEH/G_eff",
            "meaning": "retained non-EH operator terms carry mass/source charge",
            "source_basis": "P8_charge_current_equality_RESIDUAL_DECOMPOSITION Delta_nonEH",
            "status": "unbounded",
            "required_exit": "EH-only theorem or executable R11 weak-field/source-charge vector",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "SCE992_Delta_symp",
            "symbolic_piece": "int_partialSigma(tau dot theta_extra - delta Q_extra)",
            "meaning": "nonintegrable or reference-dependent boundary symplectic term",
            "source_basis": "991 FB991_0/1/2 and P8 Delta_symp",
            "status": "blocked_by_FB5540",
            "required_exit": "theta/Q_tau integrability, fixed B_ref, observed no-flux theorem or sourced bound",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "SCE992_Delta_PiM",
            "symbolic_piece": "M_eff[delta Pi_M J_H] + M_eff[Pi_M J_H - J_M^parent]",
            "meaning": "mass projector variation or missing parent mass current shifts source charge",
            "source_basis": "P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION S499_0 plus P8 Delta_PiM",
            "status": "unbounded",
            "required_exit": "Pi_M chain-map/topological current equality or component bound",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "SCE992_Delta_extra",
            "symbolic_piece": "Pi_M(Q_boundary + Q_bulk + Q_domain + Q_memory + Q_range + Q_connection)",
            "meaning": "non-Hilbert sectors carry unowned mass-channel charge",
            "source_basis": "P8 residuals S499_1..S499_4",
            "status": "unbounded",
            "required_exit": "extra sectors exact/proper/topological/source-free or retained in weak-field fits",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "SCE992_Delta_flux",
            "symbolic_piece": "int_annulus d(Pi_M J_H)",
            "meaning": "projected source mass drifts with radius/time in compact exterior",
            "source_basis": "P8_PARENT_SOURCE_IDENTITY_ATTEMPT I499_5 and RSN768_1",
            "status": "unbounded",
            "required_exit": "d(Pi_M J_H)=0 theorem or radial/source-backed bound",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "SCE992_Delta_G",
            "symbolic_piece": "B_tau(1/G_eff - 1/G0) or d ln G_eff",
            "meaning": "charge normalization drifts with time, range, species, frame, or domain",
            "source_basis": "P8 Delta_G and P8 source-current SC7",
            "status": "unbounded",
            "required_exit": "constant universal coupling theorem or sourced Gdot/range/species bound",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "SCE992_Delta_cal",
            "symbolic_piece": "M_eff[Pi_M J_H] - M_Gauss_orbital",
            "meaning": "closed source charge is not absolutely calibrated to Poisson/Gauss/orbital mass",
            "source_basis": "P8 Delta_cal and Poisson/Gauss contract",
            "status": "downstream_unbounded",
            "required_exit": "Gauss surface integral and orbital readout after Hamiltonian source equality",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "SCE992_Delta_PPN",
            "symbolic_piece": "delta_beta_source and gamma_minus_1 after first-order normalization",
            "meaning": "first-order source equality still might fail at second PPN order",
            "source_basis": "P8 Delta_PPN and PG9",
            "status": "downstream_not_ready",
            "required_exit": "PPN response matrix after source charge and weak-field operator are owned",
            "valid_for_claim": "false",
        },
    ]


def route_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RTA992_0_direct_substitution",
            "route": "set M_H_tau equal to orbital GM by definition",
            "result": "rejected",
            "why": "this is exactly the hidden calibration move 991 forbids",
            "next_action": "derive equality before orbital calibration",
            "valid_for_claim": "false",
        },
        {
            "route_id": "RTA992_1_total_Ward_conservation",
            "route": "use total conservation dJ_total=0",
            "result": "insufficient",
            "why": "P8 D499_1 says conserving the whole ledger does not prove the observed Hilbert mass channel is closed",
            "next_action": "prove zero Pi_M projection of extra channels or retain residuals",
            "valid_for_claim": "false",
        },
        {
            "route_id": "RTA992_2_topological_PiM",
            "route": "introduce metric-independent topological Pi_M current",
            "result": "promising_conditional_not_derived",
            "why": "P8 D500_1 says Hilbert equality to observed source current is not derived",
            "next_action": "only use if topological current equals Pi_M J_H on shell",
            "valid_for_claim": "false",
        },
        {
            "route_id": "RTA992_3_EH_baseline",
            "route": "borrow ADM/Gauss relation from GR",
            "result": "reference_only",
            "why": "EH baseline helps the shape of the charge but does not sign MTS extra-sector silence or source equality",
            "next_action": "use as comparison after parent current extraction",
            "valid_for_claim": "false",
        },
        {
            "route_id": "RTA992_4_component_bound",
            "route": "retain all equality failures as a no-cancellation residual vector",
            "result": "accepted_fallback",
            "why": "this is the honest route if parent equality theorem does not close",
            "next_action": "create source-backed bound input rows with units before empirical use",
            "valid_for_claim": "false",
        },
    ]


def bound_pack_rows() -> list[dict[str, str]]:
    base = "source-intake/mts_residuals"
    return [
        {
            "pack_id": "BPK992_0_current_extraction",
            "target_quantity": "theta_total_Qtau_current_owner",
            "candidate_artifact": f"{base}/P8_Y5_R10_992_THETA_QTAU_EXTRACTION_INPUT_CANDIDATE.csv",
            "required_columns": "sector;L_parent_term;theta_term;Qtau_term;constraint_term;boundary_term;source_path;valid_for_claim",
            "current_status": "MISSING_PARENT_CURRENT_EXTRACTION",
            "claim_gate": "all current pieces extracted from explicit parent L with source paths",
            "valid_for_claim": "false",
        },
        {
            "pack_id": "BPK992_1_PiM_chain_map",
            "target_quantity": "Pi_M_chain_map_commutator_bound",
            "candidate_artifact": f"{base}/P8_Y5_R10_992_PIM_CHAIN_MAP_INPUT_CANDIDATE.csv",
            "required_columns": "system_id;PiM_definition;commutator_value;domain_policy;units;source_path;valid_for_claim",
            "current_status": "MISSING_PIM_CHAIN_MAP_OR_BOUND",
            "claim_gate": "[d,Pi_M]J_H theorem-zero or sourced finite bound",
            "valid_for_claim": "false",
        },
        {
            "pack_id": "BPK992_2_charge_current_residuals",
            "target_quantity": "M_H_tau_minus_M_eff_PiM_JH_residual_vector",
            "candidate_artifact": f"{base}/P8_Y5_R10_992_CHARGE_CURRENT_RESIDUAL_INPUT_CANDIDATE.csv",
            "required_columns": "residual_id;value;units;source_path;zero_theorem_or_bound;no_cancellation_flag;valid_for_claim",
            "current_status": "MISSING_CHARGE_CURRENT_RESIDUAL_BOUNDS",
            "claim_gate": "all residual rows zero/bounded with no cancellation credit",
            "valid_for_claim": "false",
        },
        {
            "pack_id": "BPK992_3_Geff_lock",
            "target_quantity": "constant_universal_Geff_or_drift_bound",
            "candidate_artifact": f"{base}/P8_Y5_R10_992_GEFF_LOCK_INPUT_CANDIDATE.csv",
            "required_columns": "system_id;G_eff_definition;dlnG_dt;range_dependence;species_dependence;frame_dependence;source_path;valid_for_claim",
            "current_status": "MISSING_CONSTANT_GEFF_OR_DRIFT_BOUND",
            "claim_gate": "constant universal coupling theorem or source-backed drift bounds",
            "valid_for_claim": "false",
        },
        {
            "pack_id": "BPK992_4_Gauss_calibration",
            "target_quantity": "M_eff_PiM_JH_minus_M_Gauss_orbital",
            "candidate_artifact": f"{base}/P8_Y5_R10_992_GAUSS_ORBITAL_CALIBRATION_INPUT_CANDIDATE.csv",
            "required_columns": "system_id;Poisson_coefficient;Gauss_surface_mass;orbital_mass;difference_value;units;source_path;valid_for_claim",
            "current_status": "MISSING_GAUSS_ORBITAL_CALIBRATION",
            "claim_gate": "only evaluated after Hamiltonian source equality is parent-owned",
            "valid_for_claim": "false",
        },
        {
            "pack_id": "BPK992_5_PPN_source_stability",
            "target_quantity": "second_order_source_stability_vector",
            "candidate_artifact": f"{base}/P8_Y5_R10_992_PPN_SOURCE_STABILITY_INPUT_CANDIDATE.csv",
            "required_columns": "PPN_parameter;source_response;gauge;frame;value;units;source_path;valid_for_claim",
            "current_status": "MISSING_PPN_SOURCE_STABILITY_RESPONSE",
            "claim_gate": "gamma/beta/preferred-frame source responses scored after source charge closes",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG992_0_source_current_descent",
            "claim": "Hamiltonian Pi_M source-current descent is derived",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "parent current extraction and FB554_0 integrability are not signed",
        },
        {
            "gate_id": "CG992_1_charge_current_equality",
            "claim": "M_H_tau equals projected Hilbert source current",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "nine residual pieces remain unzeroed/unbounded",
        },
        {
            "gate_id": "CG992_2_Newton_Gauss_orbit",
            "claim": "Newtonian Poisson/Gauss/orbital source normalization is derived",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "Gauss/orbital calibration is downstream of source equality",
        },
        {
            "gate_id": "CG992_3_local_GR_PPN_R10",
            "claim": "local GR, PPN, R10, R11, Gdot, or orbit pass",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "source charge, weak-field operator, and PPN source stability remain open",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC992_0_derivation_attempt",
            "decision": "do not promote source-current descent",
            "reason": "the direct equality theorem is blocked before source equality by theta/Q_tau, integrability, B_ref, and tau lock",
            "effect": "Newton reduction remains live but unclaimed",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC992_1_residual_identity",
            "decision": "keep the exact residual decomposition as the source-current contract",
            "reason": "P8 already decomposes the failure into explicit residual pieces, which is stronger than vague closure",
            "effect": "future empirical tests can carry finite source residuals if theorem-zero fails",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC992_2_next_target",
            "decision": "target parent Lagrangian current extraction next",
            "reason": "source equality cannot be proved until theta_total, Q_tau, constraints, and boundary terms are owned",
            "effect": "move upstream to the actual covariant phase-space current owner",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "993-Y5-R10-parent-Lagrangian-current-extraction-theta-Qtau-or-deltaH-curl-input.md",
            "objective": "extract theta_total, Q_tau, constraints, and boundary/reference terms from the candidate parent action clauses, or stage deltaH curl input rows",
            "include": "sector-by-sector L_parent terms, theta terms, Q_tau terms, constraint split, B_ref policy, tau variation, source paths, nonclaim validation",
            "exclude": "Newton/PPN/R10/local-GR pass, orbital GM substitution, inferred source equality, GitHub action, formalization-workbench edits",
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
    theorem: list[dict[str, str]],
    residuals: list[dict[str, str]],
    routes: list[dict[str, str]],
    bounds: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    theorem_ok = all(row["valid_for_claim"] == "false" for row in theorem) and theorem[-1]["current_status"] == "not_promoted"
    residuals_ok = len(residuals) >= 9 and all(row["valid_for_claim"] == "false" for row in residuals)
    routes_ok = any(row["route_id"] == "RTA992_4_component_bound" and row["result"] == "accepted_fallback" for row in routes)
    bounds_ok = all(row["valid_for_claim"] == "false" and "MISSING" in row["current_status"] for row in bounds)
    claims_ok = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims)
    decision_ok = any(row["decision_id"] == "DEC992_2_next_target" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V992_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all cited local source files exist and expected needles are found"},
        {"check_id": "V992_1_descent_theorem_nonclaim", "result": "pass" if theorem_ok else "fail", "detail": "source-current descent theorem gate is written and not promoted"},
        {"check_id": "V992_2_residual_ledger_complete", "result": "pass" if residuals_ok else "fail", "detail": "charge-current residual ledger keeps every piece nonclaim"},
        {"check_id": "V992_3_route_audit_safe", "result": "pass" if routes_ok else "fail", "detail": "direct substitution is rejected and component-bound fallback is selected"},
        {"check_id": "V992_4_bound_pack_fail_closed", "result": "pass" if bounds_ok else "fail", "detail": "bound pack rows remain MISSING and valid_for_claim=false"},
        {"check_id": "V992_5_claim_gates_safe", "result": "pass" if claims_ok else "fail", "detail": "source-current, Newton/Gauss, PPN/R10/local-GR claims are blocked"},
        {"check_id": "V992_6_next_decision", "result": "pass" if decision_ok else "fail", "detail": "parent Lagrangian current extraction selected next"},
        {"check_id": "V992_7_next_target_written", "result": "pass" if next_ok else "fail", "detail": "993 theta/Qtau extraction target is present and nonclaim"},
        {"check_id": "V992_8_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {
            "check_id": "V992_READY",
            "result": "pass" if ready else "fail",
            "detail": "992 checkpoint pack validation summary",
            "generated_utc": stamp(),
        }
    ]


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    residuals: list[dict[str, str]],
    routes: list[dict[str, str]],
    bounds: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 992 Y5 R10: Hamiltonian PiM Source-Current Descent Or FB554_0 Component Bound Pack",
        "",
        "Status: `Y5_R10_992_source_current_descent_not_promoted_residual_identity_and_bound_pack_staged_nonclaim`",
        "",
        "Claim ceiling: no Hamiltonian source-current equality, no Newton/Poisson/Gauss/orbit calibration, no PPN/R10/R11/Gdot/local-GR pass, no parent-action derivation claim.",
        "",
        "## Readout",
        "",
        "992 tries the clean GR/Newton move: make the observed source mass descend from one Hamiltonian `Pi_M` charge and the same Hilbert matter current. The result is not a proof yet. The old P8 stack already got the right identity shape, but it also already found the trap: total conservation is not enough, and orbital `GM` cannot be substituted for a parent-owned source charge.",
        "",
        "The useful advance is the contract is now sharper. Source equality must wait for `L_parent -> theta_total/Q_tau -> integrable H_tau` plus a parent-owned `Pi_M` chain map. Until then the equality is a residual vector, not a Newtonian reduction.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## Source-Current Descent Theorem Gate",
        "",
        md_table(theorem, ["gate_id", "descent_clause", "mathematical_form", "would_imply", "current_status", "missing", "valid_for_claim"]),
        "",
        "## Charge-Current Residual Ledger",
        "",
        md_table(residuals, ["residual_id", "symbolic_piece", "meaning", "source_basis", "status", "required_exit", "valid_for_claim"]),
        "",
        "## Route Audit",
        "",
        md_table(routes, ["route_id", "route", "result", "why", "next_action", "valid_for_claim"]),
        "",
        "## Component Bound Pack",
        "",
        md_table(bounds, ["pack_id", "target_quantity", "candidate_artifact", "required_columns", "current_status", "claim_gate", "valid_for_claim"]),
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
    theorem = descent_theorem_gate_rows()
    residuals = residual_ledger_rows()
    routes = route_audit_rows()
    bounds = bound_pack_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, theorem, residuals, routes, bounds, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_992_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_992_SOURCE_CURRENT_DESCENT_THEOREM_GATE.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_992_CHARGE_CURRENT_RESIDUAL_LEDGER.csv", residuals)
    write_csv(OUT / "P8_Y5_R10_992_ROUTE_AUDIT.csv", routes)
    write_csv(OUT / "P8_Y5_R10_992_COMPONENT_BOUND_PACK.csv", bounds)
    write_csv(OUT / "P8_Y5_R10_992_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_992_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_992_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_992_VALIDATION.csv", validation)
    write_doc(sources, theorem, residuals, routes, bounds, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
