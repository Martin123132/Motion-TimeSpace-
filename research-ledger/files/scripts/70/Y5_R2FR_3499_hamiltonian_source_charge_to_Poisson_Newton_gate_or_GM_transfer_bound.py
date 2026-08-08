from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3499-Y5-R2FR-Hamiltonian-source-charge-to-Poisson-Newton-gate-or-GM-transfer-bound.md"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3499": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3498": {
        "path": ROOT / "3498-Y5-R2FR-projector-naturality-stress-test-or-Kprojector-bound.md",
        "role": "3498 handoff",
    },
    "next_3498": {
        "path": OUT / "P8_Y5_R2FR_3498_NEXT_TARGET.csv",
        "role": "3498 selected next target",
    },
    "hsrc_3498": {
        "path": OUT / "P8_Y5_R2FR_3498_HSRC_STATUS_UPDATE.csv",
        "role": "source-hypermomentum status update",
    },
    "hilbert_3423": {
        "path": OUT / "P8_Y5_R2FR_3423_HILBERT_WORLDTUBE_CLOSURE_THEOREM.csv",
        "role": "Hilbert worldtube closure theorem",
    },
    "pg_contract": {
        "path": OUT / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "role": "Hamiltonian charge -> Poisson/Gauss contract",
    },
    "hc_contract": {
        "path": OUT / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "role": "Hamiltonian boundary charge contract",
    },
    "mf_contract": {
        "path": OUT / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "role": "mass flux/projector calibration contract",
    },
    "charge_equality": {
        "path": OUT / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        "role": "charge-current equality direct attempt",
    },
    "charge_residuals": {
        "path": OUT / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
        "role": "charge-current residual decomposition",
    },
    "gauss_chain": {
        "path": OUT / "P8_Y5_GAUSS_ORBITAL_CALIBRATION_CHAIN.csv",
        "role": "Gauss/orbital calibration chain",
    },
    "gauss_gates": {
        "path": OUT / "P8_Y5_GAUSS_ORBITAL_ACCEPTANCE_GATES.csv",
        "role": "Gauss/orbital acceptance gates",
    },
    "newton_stack": {
        "path": OUT / "P8_source_normalized_Newton_branch_STACK.csv",
        "role": "source-normalized Newton branch stack",
    },
    "weak_field": {
        "path": OUT / "P8_Y5_GR_LEFT_HAND_GATE_2619_NEWTON_POISSON_WEAK_FIELD_ATTEMPT.csv",
        "role": "Newton/Poisson weak-field template",
    },
    "constant_g": {
        "path": OUT / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv",
        "role": "constant measured-GM zero theorem attempt",
    },
    "constant_g_gate": {
        "path": OUT / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
        "role": "constant-GM derivative hair gate",
    },
    "delta_newton_law": {
        "path": OUT / "P8_Y5_HCORE_QR_COUPLING_2576_NEWTON_PPN_COEFFICIENT_LAW.csv",
        "role": "Newton coefficient residual law",
    },
    "gm_transfer": {
        "path": OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv",
        "role": "GM transfer component rows",
    },
}


def generated_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(metadata["path"]),
            "exists": str(Path(metadata["path"]).exists()),
            "role": metadata["role"],
            "valid_for_claim": "False",
        }
        for source_id, metadata in SOURCES.items()
    ]


def poisson_newton_theorem_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "chain_id": "PNC3499_0_do_not_derive_number_G",
            "claim_piece": "Newton constant policy",
            "statement": "The target is not to derive the numerical value of Newton's constant from GR; GR itself uses a measured coupling. The MTS target is one parent-fixed G_ref with no post-readout GM absorption.",
            "derivation": "A constant coupling can be a branch parameter of the parent action. What must be derived is that the same constant multiplies the same Hilbert/Hamiltonian source in the weak-field equation and the orbital readout.",
            "status": "POLICY_AND_DIMENSIONAL_GUARD",
            "remaining_gap": "parent-fixed constant/superselection proof for G_ref/kappa_eff",
            "source_path": str(SOURCES["constant_g"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "chain_id": "PNC3499_1_same_frame_source",
            "claim_piece": "observed source frame",
            "statement": "Matter, clocks, rods, the Hamiltonian source current and slow orbits must all use the same observed coframe e_obs.",
            "derivation": "Without a same-frame pullback, the potential that moves matter need not be the potential sourced by the Hilbert current. With e_source=e_matter=e_obs, the same T_00 enters both variation and readout.",
            "status": "CANDIDATE_FROM_MPA3497_NOT_LIVE_CLAIM",
            "remaining_gap": "source variation same-frame theorem and frame residual row",
            "source_path": str(SOURCES["newton_stack"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "chain_id": "PNC3499_2_EH_00_to_Poisson",
            "claim_piece": "weak-field Poisson equation",
            "statement": "If the local exterior left-hand operator is EH-only and T_00 ~= rho_H c^2, then g_00=-1+2U/c^2 gives nabla^2 U = 4 pi G_ref rho_H.",
            "derivation": "The linearized EH 00 equation gives G_00 ~= 2 nabla^2 U/c^2. With kappa_eff=8 pi G_ref/c^4 and T_00 ~= rho_H c^2, the equation reduces to the standard Poisson coefficient.",
            "status": "DERIVED_CONDITIONAL_TEMPLATE",
            "remaining_gap": "EH-only/R11 operator silence and clean nonrelativistic Hilbert source",
            "source_path": str(SOURCES["weak_field"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "chain_id": "PNC3499_3_Hamiltonian_charge_equals_source_mass",
            "claim_piece": "source charge identity",
            "statement": "The mass in the Poisson equation must be M_H := H_tau[S]-H_ref = M_eff[Pi_M J_H], fixed before orbital readout.",
            "derivation": "If the Hamiltonian variation integrates to the same projected Hilbert source current, the surface charge is the enclosed source mass rather than an external fitted GM label.",
            "status": "EXACT_IF_INTEGRABILITY_REFERENCE_AND_PIM_IDENTITY_SIGNED",
            "remaining_gap": "H_ref, M_H_ref positivity, Pi_M/current equality and boundary reference lock",
            "source_path": str(SOURCES["hilbert_3423"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "chain_id": "PNC3499_4_Gauss_to_inverse_square",
            "claim_piece": "Newton inverse-square exterior",
            "statement": "If nabla^2 U = 4 pi G_ref rho_H and the exterior has no residual volume/boundary flux, then U(r)=G_ref M_H/r+O(r^-2 multipoles) and a=-nabla U.",
            "derivation": "Gauss' theorem gives surface_int grad U dot dS = -4 pi G_ref M_H up to sign convention for U. Spherical or monopole exterior yields the 1/r coefficient without using measured orbital GM as an input.",
            "status": "DERIVED_CONDITIONAL_GAUSS_TEMPLATE",
            "remaining_gap": "closed source-free exterior annulus, zero mu_extra, no radial/range hair, slow-particle readout",
            "source_path": str(SOURCES["gauss_chain"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "chain_id": "PNC3499_5_no_extra_mass_or_derivative_hair",
            "claim_piece": "no hidden measured-GM correction",
            "statement": "mu_obs = G_ref M_H only if mu_extra=0 and D_X ln mu_obs=0 for X in time, radius, species, range, frame and domain channels.",
            "derivation": "The exact identity D_X ln mu_obs = D_X ln G_ref + D_X ln M_H + D_X ln(1+epsilon_mu) converts vague GM absorption into row-by-row derivative tests.",
            "status": "EXACT_IDENTITY_ZERO_NOT_DERIVED",
            "remaining_gap": "constant G_ref, M_eff flux closure, mu_extra vector, source universality, R10 range curve",
            "source_path": str(SOURCES["constant_g_gate"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "chain_id": "PNC3499_6_first_order_Newton_verdict",
            "claim_piece": "first-order source-normalized Newton",
            "statement": "The first-order Newton route is mathematically clean inside the candidate branch, but current MTS has not closed the required calibration gates in one parent proof.",
            "derivation": "EH 00 -> Poisson -> Gauss -> inverse-square works if the same Hamiltonian/Hilbert source charge is calibrated by a constant parent G_ref and all extra/radial/range/source channels are zero or bounded.",
            "status": "CONDITIONAL_THEOREM_CHAIN_SHARPENED_NOT_CLAIMED",
            "remaining_gap": "fill or derive the Delta_Newton residual vector",
            "source_path": str(SOURCES["pg_contract"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "chain_id": "PNC3499_7_local_GR_caveat",
            "claim_piece": "do not promote Newton to full GR",
            "statement": "Even a first-order Newton pass would not prove local GR; beta, gamma, preferred-frame, xi and R11 operator rows still require a second-order source/operator calculation.",
            "derivation": "Poisson fixes the leading 1/r source coefficient. PPN requires the nonlinear g_00 term, spatial curvature response, vector sectors, and operator residuals to satisfy their locks.",
            "status": "GUARDRAIL_RETAINED",
            "remaining_gap": "second-order PPN source stability after first-order source calibration",
            "source_path": str(SOURCES["newton_stack"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def calibration_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PNG3499_0_same_frame",
            "gate": "one observed coframe/source frame",
            "required_identity": "e_source=e_matter=e_obs and tau is shared by Hamiltonian charge and readout",
            "candidate_result": "SUPPORTED_BY_MPA3497_BUT_NOT_PARENT_ADOPTED",
            "blocks_newton_claim": "True",
            "residual_if_failed": "delta_frame_source",
            "source_path": str(SOURCES["newton_stack"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PNG3499_1_EH_operator",
            "gate": "EH-only 00 operator or scored R11 vector",
            "required_identity": "G_00 linearizes to Poisson with no non-EH/source residual operator",
            "candidate_result": "CONDITIONAL_TEMPLATE_ONLY",
            "blocks_newton_claim": "True",
            "residual_if_failed": "c_nonEH_operator_vector;alpha(lambda);gamma_minus_1",
            "source_path": str(SOURCES["weak_field"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PNG3499_2_charge_current_identity",
            "gate": "Hamiltonian charge equals projected Hilbert source",
            "required_identity": "B_xi/G_ref = M_eff[Pi_M J_H] = M_H before readout",
            "candidate_result": "NOT_PARENT_DERIVED",
            "blocks_newton_claim": "True",
            "residual_if_failed": "Delta_cal;Delta_PiM;epsilon_M",
            "source_path": str(SOURCES["charge_equality"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PNG3499_3_flux_closure",
            "gate": "closed exterior source flux",
            "required_identity": "d(Pi_M J_H)=0 in compact source-free exterior",
            "candidate_result": "OPEN",
            "blocks_newton_claim": "True",
            "residual_if_failed": "dln_Meff_dt;partial_r_ln_mu_obs",
            "source_path": str(SOURCES["mf_contract"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PNG3499_4_constant_G",
            "gate": "constant universal G_ref/kappa_eff",
            "required_identity": "partial_{t,r,A,lambda,frame,domain} G_ref = 0",
            "candidate_result": "CONDITIONAL_NOT_PARENT_DERIVED",
            "blocks_newton_claim": "True",
            "residual_if_failed": "dln_Geff_dt;eta_source_AB;alpha(lambda)",
            "source_path": str(SOURCES["constant_g"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PNG3499_5_mu_extra_zero",
            "gate": "no extra measured-mass monopole",
            "required_identity": "mu_extra = mu_boundary+mu_domain+mu_memory+mu_range+mu_connection+mu_nonEH = 0 or universal derivative-silent constant",
            "candidate_result": "NOT_DERIVED",
            "blocks_newton_claim": "True",
            "residual_if_failed": "mu_extra_boundary_bulk_domain/(G_ref M_H)",
            "source_path": str(SOURCES["charge_residuals"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PNG3499_6_orbital_readout",
            "gate": "slow-particle inverse-square readout",
            "required_identity": "a_r=-partial_r U=-G_ref M_H/r^2 with no finite-range, direct-force, frame or species correction",
            "candidate_result": "NOT_DERIVED_NOT_SCORED",
            "blocks_newton_claim": "True",
            "residual_if_failed": "alpha(lambda);eta_source_AB;delta_frame_source",
            "source_path": str(SOURCES["gauss_gates"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PNG3499_7_second_order_guard",
            "gate": "PPN source stability",
            "required_identity": "gamma-1=0 and delta_beta_source=0 after first-order measured-GM normalization",
            "candidate_result": "DEFERRED_NOT_REQUIRED_FOR_FIRST_ORDER_NEWTON",
            "blocks_newton_claim": "False",
            "residual_if_failed": "gamma_minus_1;delta_beta_source;c_nonEH_operator_vector",
            "source_path": str(SOURCES["newton_stack"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def delta_newton_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "DN3499_0_master",
            "symbol": "Delta_Newton_source",
            "definition": "fractional failure of source-normalized Newtonian monopole",
            "formula": "(1+delta_KC)(1+epsilon_M)(1+delta_kappa)(1+delta_ellJ)(1+Delta_flux)(1+epsilon_mu)(1+Delta_cal)-1",
            "zero_or_bound_condition": "each factor zero/owned or individually source-backed below mapped locks; no cancellation credit",
            "mapped_observables": "Newton; beta source; Gdot; WEP source charge; R10 alpha(lambda)",
            "source_path": str(SOURCES["delta_newton_law"]["path"]),
            "current_status": "EXECUTABLE_SYMBOLIC_VECTOR_NONCLAIM",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "DN3499_1_delta_KC",
            "symbol": "delta_KC",
            "definition": "EH/Poisson operator coefficient mismatch",
            "formula": "C_v c^4/(16*pi*G_ref*K_v)-1",
            "zero_or_bound_condition": "EH-only 00 operator or scored non-EH/R11 coefficient vector",
            "mapped_observables": "gamma_minus_1;beta_minus_1;R10;R11",
            "source_path": str(SOURCES["delta_newton_law"]["path"]),
            "current_status": "CONDITIONAL_NOT_SCORED",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "DN3499_2_epsilon_M",
            "symbol": "epsilon_M",
            "definition": "source measure glue mismatch",
            "formula": "M_source[W]/M_eff[Pi_M J_H]-1",
            "zero_or_bound_condition": "Hamiltonian charge equals projected Hilbert current before readout",
            "mapped_observables": "Newton;eta_source;radial_Meff",
            "source_path": str(SOURCES["gm_transfer"]["path"]),
            "current_status": "MISSING_CHARGE_CURRENT_IDENTITY",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "DN3499_3_delta_kappa",
            "symbol": "delta_kappa",
            "definition": "parent coupling/G_ref drift",
            "formula": "D ln kappa_MTS relative to fixed local comparator normalization",
            "zero_or_bound_condition": "constant universal parent coupling superselection",
            "mapped_observables": "Gdot;eta_source;R10 range dependence",
            "source_path": str(SOURCES["constant_g_gate"]["path"]),
            "current_status": "OPEN_NOT_PARENT_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "DN3499_4_delta_ellJ",
            "symbol": "delta_ellJ",
            "definition": "source-current scale residual",
            "formula": "D ln ell_J relative to compact-source Hilbert current",
            "zero_or_bound_condition": "source current scale parent-owned and selector-blind",
            "mapped_observables": "WEP source charge;Newton source normalization",
            "source_path": str(SOURCES["delta_newton_law"]["path"]),
            "current_status": "OPEN",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "DN3499_5_Delta_flux",
            "symbol": "Delta_flux",
            "definition": "radial/time drift of projected source mass",
            "formula": "int_A d(Pi_M J_H)/M_H_ref",
            "zero_or_bound_condition": "closed exterior flux or explicit dln_Meff_dt/partial_r profile below locks",
            "mapped_observables": "Gdot;radial hair;R10",
            "source_path": str(SOURCES["charge_residuals"]["path"]),
            "current_status": "RETAINED_UNFILLED",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "DN3499_6_epsilon_mu",
            "symbol": "epsilon_mu",
            "definition": "extra measured-mass monopole relative to G_ref M_H",
            "formula": "mu_extra/(G_ref M_H)",
            "zero_or_bound_condition": "mu_extra zero/universal constant with all derivatives zero, or channel coefficient vector",
            "mapped_observables": "alpha3;xi;beta;Gdot;R11",
            "source_path": str(SOURCES["constant_g_gate"]["path"]),
            "current_status": "RETAINED_UNFILLED",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "DN3499_7_Delta_cal",
            "symbol": "Delta_cal",
            "definition": "closed source charge not calibrated to Gauss/orbital mass",
            "formula": "M_eff[Pi_M J_H]/M_Gauss_orbital - 1",
            "zero_or_bound_condition": "Gauss surface theorem and slow-particle readout without using measured GM as input",
            "mapped_observables": "Newton;orbital;R10",
            "source_path": str(SOURCES["charge_residuals"]["path"]),
            "current_status": "RETAINED_UNFILLED",
            "valid_for_claim": "False",
        },
    ]


def gm_transfer_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "GMTB3499_0_first_order_Newton_envelope",
            "trigger": "any PNG3499 Newton calibration gate fails",
            "residual_symbol": "Delta_Newton_source",
            "bound_formula": "abs(Delta_Newton_source) <= product_abs_envelope(DN3499_i) - 1",
            "required_inputs": "numeric/theorem-zero rows for delta_KC, epsilon_M, delta_kappa, delta_ellJ, Delta_flux, epsilon_mu, Delta_cal",
            "observable_lock": "no source-normalized Newton claim until every active factor is zero or below a mapped lock",
            "current_value": "NOT_COMPUTED_COMPONENTS_UNFILLED",
            "source_path": str(SOURCES["gm_transfer"]["path"]),
            "score_status": "BOUND_ROW_READY_NONCLAIM",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "GMTB3499_1_no_orbital_GM_shortcut",
            "trigger": "attempt to set M_H := GM_orb/G_ref by readout",
            "residual_symbol": "epsilon_GM_absorption_shortcut",
            "bound_formula": "invalid_for_claim unless GM_orb is derived from Poisson/Gauss after variation",
            "required_inputs": "none; this is a hard guardrail",
            "observable_lock": "using the target measured GM as proof blocks Newton/local-GR promotion",
            "current_value": "FORBIDDEN_SHORTCUT",
            "source_path": str(SOURCES["gauss_chain"]["path"]),
            "score_status": "REJECTED_FOR_CLAIM",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3499_0_Newton_route_real",
            "decision": "The first-order Newton route is a real conditional theorem chain.",
            "rationale": "EH weak field plus the same Hamiltonian/Hilbert source charge gives Poisson, Gauss and inverse-square without needing orbital GM as a premise.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3499_1_not_claimed",
            "decision": "Do not claim source-normalized Newton yet.",
            "rationale": "Charge-current identity, constant G_ref, no mu_extra/derivative hair, EH/R11 silence and orbital readout are still not closed in one parent proof.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3499_2_next_best_gate",
            "decision": "Attack constant G_ref and derivative-hair rows next.",
            "rationale": "Once the theorem chain is written, the cleanest make-or-break test is whether mu_obs has time/radial/species/range/frame/domain derivative hair.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3500-Y5-R2FR-constant-Gref-and-muobs-derivative-hair-zero-or-residual-fill.md",
            "next_script": "scripts/Y5_R2FR_3500_constant_Gref_and_muobs_derivative_hair_zero_or_residual_fill.py",
            "objective": "Try to prove G_ref and mu_obs are derivative-silent in time, radius, species, range, frame and domain channels; if not, fill the first derivative-hair residual rows with units and nonclaim status.",
            "success_gate": "D_X ln G_ref = D_X ln M_H = D_X epsilon_mu = 0 by parent identity for all active X, or source-ready residual rows for Gdot/radial/source/R10/frame channels",
            "forbidden_shortcuts": "tuned cancellation between G_ref, M_H and mu_extra; single-radius orbital calibration; importing cosmological G behavior into local tests; claiming Newton before derivative rows close",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_files = [
        OUT / "P8_Y5_R2FR_3499_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R2FR_3499_POISSON_NEWTON_THEOREM_CHAIN.csv",
        OUT / "P8_Y5_R2FR_3499_SOURCE_CHARGE_CALIBRATION_GATES.csv",
        OUT / "P8_Y5_R2FR_3499_DELTA_NEWTON_RESIDUAL_VECTOR.csv",
        OUT / "P8_Y5_R2FR_3499_GM_TRANSFER_BOUND_ROW.csv",
        OUT / "P8_Y5_R2FR_3499_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R2FR_3499_NEXT_TARGET.csv",
    ]
    parsed_counts = [f"{output_file.name}:{len(read_csv(output_file))}" for output_file in output_files]
    all_rows = [*sources, *theorem, *gates, *residuals, *bounds, *decisions, *next_rows]
    blocking_gates = sum(1 for row in gates if row.get("blocks_newton_claim") == "True")
    checks = [
        {
            "check_id": "VAL3499_0_sources_exist",
            "passed": all(source_row["exists"] == "True" for source_row in sources),
            "detail": "all cited local sources exist",
        },
        {
            "check_id": "VAL3499_1_csv_parse",
            "passed": True,
            "detail": "; ".join(parsed_counts),
        },
        {
            "check_id": "VAL3499_2_theorem_chain",
            "passed": len(theorem) >= 8 and any(row["status"] == "DERIVED_CONDITIONAL_TEMPLATE" for row in theorem),
            "detail": f"theorem_rows={len(theorem)}; EH-to-Poisson template present",
        },
        {
            "check_id": "VAL3499_3_gates_block_claim",
            "passed": blocking_gates >= 6,
            "detail": f"blocking_Newton_gates={blocking_gates}",
        },
        {
            "check_id": "VAL3499_4_residual_vector_complete",
            "passed": len(residuals) >= 8 and residuals[0]["symbol"] == "Delta_Newton_source",
            "detail": f"residual_rows={len(residuals)}; master={residuals[0]['symbol']}",
        },
        {
            "check_id": "VAL3499_5_bound_guardrails",
            "passed": len(bounds) == 2 and bounds[1]["current_value"] == "FORBIDDEN_SHORTCUT",
            "detail": "GM-transfer bound row and no-orbital-GM shortcut guard present",
        },
        {
            "check_id": "VAL3499_6_no_claim",
            "passed": all(str(row.get("valid_for_claim", "False")) == "False" for row in all_rows),
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "VAL3499_7_no_formalization_outputs",
            "passed": all(not str(output_file).startswith(str(FORMALIZATION)) for output_file in output_files),
            "detail": "outputs are under post-checkpoint-work/source-intake only",
        },
        {
            "check_id": "VAL3499_8_next_target",
            "passed": len(next_rows) == 1 and "3500" in next_rows[0]["next_doc"],
            "detail": next_rows[0]["next_doc"],
        },
    ]
    checks.append(
        {
            "check_id": "VAL3499_SUMMARY",
            "passed": all(bool(check["passed"]) for check in checks),
            "detail": "PASS" if all(bool(check["passed"]) for check in checks) else "FAIL",
        }
    )
    return [
        {
            "check_id": check["check_id"],
            "passed": str(bool(check["passed"])),
            "detail": check["detail"],
            "valid_for_claim": "False",
        }
        for check in checks
    ]


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    theorem: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3499 - Hamiltonian Source Charge to Poisson/Newton Gate or GM-Transfer Bound",
                "",
                "## Current Verdict",
                "- **Real theorem chain:** EH weak field plus the same Hamiltonian/Hilbert source charge gives Poisson, Gauss and inverse-square Newton as a conditional derivation.",
                "- **No magic G claim:** the numerical value of `G_ref` is not derived; the target is a parent-fixed, universal, derivative-silent coupling that cannot be fitted after readout.",
                "- **No Newton claim yet:** charge-current identity, constant `G_ref`, `mu_extra=0`, derivative-hair silence, EH/R11 silence and orbital readout still have to close together.",
                "- **Next best move:** attack `D_X ln mu_obs` derivative hair directly, because that decides whether measured `GM` is a true constant or a hidden fit.",
                "",
                "## Poisson/Newton Theorem Chain",
                markdown_table(
                    theorem,
                    ["chain_id", "claim_piece", "statement", "status", "remaining_gap", "valid_for_claim"],
                ),
                "",
                "## Source-Charge Calibration Gates",
                markdown_table(
                    gates,
                    [
                        "gate_id",
                        "gate",
                        "required_identity",
                        "candidate_result",
                        "blocks_newton_claim",
                        "residual_if_failed",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Delta Newton Residual Vector",
                markdown_table(
                    residuals,
                    [
                        "residual_id",
                        "symbol",
                        "definition",
                        "formula",
                        "zero_or_bound_condition",
                        "mapped_observables",
                        "current_status",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## GM-Transfer Bound Rows",
                markdown_table(
                    bounds,
                    [
                        "bound_id",
                        "trigger",
                        "residual_symbol",
                        "bound_formula",
                        "current_value",
                        "score_status",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Decisions",
                markdown_table(decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"]),
                "",
                "## Next Target",
                markdown_table(
                    next_rows,
                    ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
                ),
                "",
                "## Validation",
                markdown_table(validation, ["check_id", "passed", "detail", "valid_for_claim"]),
                "",
                f"Generated: {generated_timestamp()}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    source_rows = source_register_rows()
    theorem_rows = poisson_newton_theorem_chain_rows()
    gate_rows = calibration_gate_rows()
    residual_rows = delta_newton_residual_rows()
    bound_rows = gm_transfer_bound_rows()
    decision_ledger_rows = decision_rows()
    next_rows = next_target_rows()

    write_csv(
        OUT / "P8_Y5_R2FR_3499_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "path", "exists", "role", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3499_POISSON_NEWTON_THEOREM_CHAIN.csv",
        theorem_rows,
        ["chain_id", "claim_piece", "statement", "derivation", "status", "remaining_gap", "source_path", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3499_SOURCE_CHARGE_CALIBRATION_GATES.csv",
        gate_rows,
        ["gate_id", "gate", "required_identity", "candidate_result", "blocks_newton_claim", "residual_if_failed", "source_path", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3499_DELTA_NEWTON_RESIDUAL_VECTOR.csv",
        residual_rows,
        [
            "residual_id",
            "symbol",
            "definition",
            "formula",
            "zero_or_bound_condition",
            "mapped_observables",
            "source_path",
            "current_status",
            "valid_for_claim",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3499_GM_TRANSFER_BOUND_ROW.csv",
        bound_rows,
        [
            "bound_id",
            "trigger",
            "residual_symbol",
            "bound_formula",
            "required_inputs",
            "observable_lock",
            "current_value",
            "source_path",
            "score_status",
            "valid_for_claim",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3499_DECISION_LEDGER.csv",
        decision_ledger_rows,
        ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3499_NEXT_TARGET.csv",
        next_rows,
        ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
    )

    validation = validation_rows(
        source_rows,
        theorem_rows,
        gate_rows,
        residual_rows,
        bound_rows,
        decision_ledger_rows,
        next_rows,
    )
    write_csv(
        OUT / "P8_Y5_BRR545_3499_VALIDATION.csv",
        validation,
        ["check_id", "passed", "detail", "valid_for_claim"],
    )
    write_doc(theorem_rows, gate_rows, residual_rows, bound_rows, decision_ledger_rows, next_rows, validation)


if __name__ == "__main__":
    main()
