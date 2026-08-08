from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2900-Y5-R2FR-source-worldtube-current-complex-owner-or-Jdomain-bound-fill-under-AX1090.md"

SRC_2899_DOC = ROOT / "2899-Y5-R2FR-PiM-parent-owned-projector-equality-or-commutator-envelope-under-AX1090.md"
SRC_2899_NEXT = RESIDUALS / "P8_Y5_R2FR_2899_NEXT_TARGET.csv"
SRC_2899_THEOREM = RESIDUALS / "P8_Y5_R2FR_2899_PIM_THEOREM_AUDIT.csv"
SRC_2586_DOC = ROOT / "2586-Y5-R2FR-source-worldtube-current-complex-owner-or-Jdomain-bound-fill.md"
SRC_2586_OWNER = RESIDUALS / "P8_Y5_SOURCE_COMPLEX_2586_OWNER_AUDIT.csv"
SRC_2586_CONTRACT = RESIDUALS / "P8_Y5_SOURCE_COMPLEX_2586_HILBERT_CURRENT_CONTRACT.csv"
SRC_2586_JDOMAIN = RESIDUALS / "P8_Y5_SOURCE_COMPLEX_2586_JDOMAIN_BOUND_ROWS.csv"
SRC_2587_DOC = ROOT / "2587-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md"
SRC_2587_ACTION = RESIDUALS / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv"
SRC_2587_DOMAIN = RESIDUALS / "P8_Y5_MIN_PARENT_MATTER_2587_DOMAIN_MOTION_ROWS.csv"
SRC_2588_DOC = ROOT / "2588-Y5-R2FR-observed-stack-q-eobs-tau-parent-owner-or-source-leak-fill.md"
SRC_2588_OWNER = RESIDUALS / "P8_Y5_OBS_STACK_2588_OWNER_CERTIFICATE.csv"
SRC_2588_LEAKS = RESIDUALS / "P8_Y5_OBS_STACK_2588_SOURCE_LEAK_ROWS.csv"
SRC_2585_AUDIT = RESIDUALS / "P8_Y5_PIM_CHAINMAP_2585_THEOREM_AUDIT.csv"
SRC_TAU_CONTRACT = RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2900_SOURCE_REGISTER.csv",
    "owner": RESIDUALS / "P8_Y5_R2FR_2900_SOURCE_COMPLEX_OWNER_AUDIT.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_2900_HILBERT_CURRENT_COMPLEX_CONTRACT.csv",
    "escape": RESIDUALS / "P8_Y5_R2FR_2900_JDOMAIN_CURRENT_ESCAPE_ROWS.csv",
    "evaluator": RESIDUALS / "P8_Y5_R2FR_2900_CURRENT_COMPLEX_EVALUATOR.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2900_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2900_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2900_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2900_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2900_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2900_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "owner_copy": RAB_QUEUE / "JR2900_SOURCE_COMPLEX_OWNER_AUDIT_NONCLAIM.csv",
    "contract_copy": RAB_QUEUE / "JR2900_HILBERT_CURRENT_COMPLEX_CONTRACT_NONCLAIM.csv",
    "escape_copy": LOCAL_BOUNDS / "Source_worldtube_current_escape_rows_2900_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2900_Q_OBSERVED_STACK_KERNEL_NEXT.csv",
}

for output_directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    output_directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    source_text = read_text(path)
    missing_anchors = [anchor for anchor in anchors.split(";") if anchor and anchor not in source_text]
    return not missing_anchors, ";".join(missing_anchors)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    source_specs = [
        ("SRC2900_0_2899_doc", SRC_2899_DOC, "The next target is not to re-derive the product rule again;`W_source`", "2899 selects source-worldtube/current-complex owner as the next antecedent"),
        ("SRC2900_1_2899_next", SRC_2899_NEXT, "NEXT2899_0_2900;prove W_source", "machine-readable 2900 handoff"),
        ("SRC2900_2_2899_theorem", SRC_2899_THEOREM, "PIM2899_2_physical_current_complex;FAIL_CURRENT_MTS_PIM_LOCK_NOT_DERIVED", "latest PiM antecedent audit"),
        ("SRC2900_3_2586_doc", SRC_2586_DOC, "`J_domain` remains a retained nonclaim obstruction;J_M^mu = ell_J T_H", "prior source-worldtube/current-complex checkpoint"),
        ("SRC2900_4_2586_owner", SRC_2586_OWNER, "SCO2586_7_verdict;SOURCE_WORLDTUBE_CURRENT_COMPLEX_NOT_DERIVED_CURRENT_CORPUS", "prior owner audit"),
        ("SRC2900_5_2586_contract", SRC_2586_CONTRACT, "HCC2586_0_primary_current;J_M^mu = ell_J", "Hilbert-current contract"),
        ("SRC2900_6_2586_jdomain", SRC_2586_JDOMAIN, "JD2586_TOTAL;J_domain", "J_domain residual rows"),
        ("SRC2900_7_2587_doc", SRC_2587_DOC, "ordinary matter sees only the quotient-owned observed stack;not yet derived or adopted", "minimal matter-coupling contract status"),
        ("SRC2900_8_2587_action", SRC_2587_ACTION, "MCA2587_6_descent_output;EXACT_CONDITIONAL_OUTPUT", "conditional action-to-current descent clause"),
        ("SRC2900_9_2587_domain", SRC_2587_DOMAIN, "DM2587_TOTAL;E_matter_action", "matter-action/domain residual rows"),
        ("SRC2900_10_2588_doc", SRC_2588_DOC, "regular quotient `q:Phi_parent -> Q_vis`;OBSERVED_STACK_OWNER_NOT_DERIVED_CURRENT_CORPUS", "observed-stack quotient/basic-coframe status"),
        ("SRC2900_11_2588_owner", SRC_2588_OWNER, "OSC2588_0_q_map;MISSING_PARENT_Q_MAP", "observed-stack owner certificates"),
        ("SRC2900_12_2588_leaks", SRC_2588_LEAKS, "OSL2588_TOTAL;Delta_observed_stack_total_over_MH", "q/frame/tau/ellJ leak rows"),
        ("SRC2900_13_2585_audit", SRC_2585_AUDIT, "CMA2585_4_physical_current_complex;PIM_CHAINMAP_COMMUTATOR_ZERO_NOT_DERIVED_CURRENT_CORPUS", "chainmap current-complex antecedent source"),
        ("SRC2900_14_tau_contract", SRC_TAU_CONTRACT, "TGC685_6_verdict;blocked_nonclaim", "tau generator lock source"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in source_specs:
        found_anchors, missing_anchors = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found_anchors,
                    "missing_anchors": missing_anchors,
                }
            )
        )
    return rows


def owner_audit_rows() -> list[dict[str, Any]]:
    owner_specs = [
        ("SC2900_0_parent_matter_action", "parent matter action before readout", "S_parent[Phi,psi]=S_geom[Phi]+sum_A S_A[psi_A;q(Phi),theta_A]+S_boundary[q(Phi)] is adopted by MTS core before readout", "CANDIDATE_FORM_EXISTS_NOT_PARENT_DERIVED", "2587 writes the least-circular candidate, but current MTS has not derived/adopted it", "J_H can still be a disciplined ansatz rather than a theorem"),
        ("SC2900_1_single_observed_stack", "single quotient-owned observed stack", "q(Phi)->e_obs,D_obs,A_obs,tau,ell_J controls matter, clocks, rods, photons, source charge and orbit readout", "OBSERVED_STACK_OWNER_NOT_DERIVED", "parent q map, basic coframe, tau and ell_J owner certificates remain unsigned", "source/current descent cannot be promoted"),
        ("SC2900_2_tau_lock", "same time generator", "tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit=tau_obs with fixed parent normalization", "MISSING_PARENT_TAU_IDENTITY", "tau generator contract remains blocked_nonclaim", "current divergence can leak through T^{mu nu} nabla_mu tau_nu"),
        ("SC2900_3_ellJ_scale_lock", "source-current scale fixed before GM", "ell_J is parent-normalized and constant/universal on the compact branch or has an exact exchange identity", "MISSING_PARENT_ELLJ_SCALE", "ell_J is not derived from parent action or spectrum/normalization", "source mass can hide an empirical scale"),
        ("SC2900_4_worldtube_support", "source worldtube fixed before fitting", "W_source := supp(J_H[e_obs,tau]) is determined by parent current support before orbital/PPN scoring", "MISSING_SUPPORT_AND_JUMP_LEDGER", "support regularity, jumps and source-free annulus are not theorem-zero or bounded", "moving support creates domain/source-hair terms"),
        ("SC2900_5_exterior_link_complex", "A_ext and S_link fixed", "compact exterior annulus A_ext, linking surfaces S_link, orientation and boundary conditions are fixed before Pi_M acts", "MISSING_FIXED_DOMAIN_COMPLEX", "domain owner theorem and no moving mask proof remain missing", "Stokes/chainmap use can drop domain-motion terms"),
        ("SC2900_6_current_complex_membership", "J_H lives in the same complex used by Pi_M", "J_H[e_obs,tau] in C_H(A_ext;W_source,S_link) with extra channels zeroed or explicitly included", "MISSING_PHYSICAL_CURRENT_COMPLEX", "same-frame current descent plus extra-current silence are incomplete", "Pi_M may act on a surrogate current"),
        ("SC2900_7_same_object_Mref", "same object and denominator", "Pi_M J_H = J_M_top + dB_zero with zero boundary flux and common M_ref", "MISSING_R_EQ_B_ZERO_MREF_LOCK", "R_eq, B_zero_flux and positive same-frame M_ref remain unfilled", "closed wrong charge could be conserved"),
        ("SC2900_8_no_source_slot_shadow", "no hidden source-only matter slot", "no w_A(X), c_A(X), source mask, shadow frame, non-Hilbert current or support retune survives outside q/e_obs", "CONTRACT_ONLY_NOT_UNIQUENESS_PROOF", "2587/2588 forbid the route conditionally but not from a parent grammar theorem", "source normalization can be absorbed by hidden couplings"),
        ("SC2900_9_verdict", "source-worldtube/current-complex owner theorem", "W_source, A_ext, S_link, J_H[e_obs,tau], tau, ell_J and M_ref are all parent-owned before readout in one Pi_M-compatible Hilbert-current complex", "FAIL_CURRENT_MTS_SOURCE_COMPLEX_OWNER_NOT_DERIVED", "SC2900_0 through SC2900_8 remain unsigned", "2899 fixed-chainmap theorem cannot be promoted"),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "owner_clause": owner_clause,
                "formal_statement": formal_statement,
                "current_status": current_status,
                "blocking_gap": blocking_gap,
                "effect_if_missing": effect_if_missing,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for audit_id, owner_clause, formal_statement, current_status, blocking_gap, effect_if_missing in owner_specs
    ]


def contract_rows() -> list[dict[str, Any]]:
    contract_specs = [
        ("HCC2900_0_primary_current", "Hilbert/energy source current", "J_M^mu = ell_J T_H^{mu nu} tau_nu", "SELECTED_LEAST_CIRCULAR_CONTRACT_NONCLAIM", "same stress-energy object that sources the metric also sources the Newton/GR bridge", "parent action adoption; q/e_obs/tau/ell_J ownership; support/domain ledger"),
        ("HCC2900_1_exact_divergence_identity", "source-current divergence", "nabla_mu J_M^mu=(nabla_mu ell_J)T_H^{mu nu}tau_nu + ell_J(nabla_mu T_H^{mu nu})tau_nu + ell_J T_H^{mu nu}nabla_mu tau_nu", "EXACT_IDENTITY_RETAINED", "localizes leakage into scale, matter-shell/exchange and clock-generator terms", "zero/exchange theorem for each term or finite source rows"),
        ("HCC2900_2_matter_descent_condition", "matter descent", "S_matter=Sbar_matter[q(Phi),psi,theta] and v in ker(Dq) imply delta_v S_matter=0 modulo Euler/gauge/boundary, hence J_H=q^*Jbar_H conditionally", "EXACT_CONDITIONAL_OUTPUT_NOT_PARENT_SIGNED", "2587 gives the right contract shape but current MTS has not adopted it", "parent q/kernel/basic stack and no-source-slot uniqueness"),
        ("HCC2900_3_fixed_complex", "Hilbert current complex", "C_H(A_ext;W_source,S_link,e_obs,tau) is fixed before readout and Pi_M:C_H->C_M is a parent chain map", "CONDITIONAL_COMPLEX_DEFINITION", "this is the minimum object needed by the 2899 fixed-chainmap theorem", "fixed domain/worldtube/support and Pi_M selector"),
        ("HCC2900_4_worldtube_charge", "source mass readout", "Q_M[Sigma]=int_{Sigma cap W_source}J_M^mu dSigma_mu and M_ref=Q_M/ell_J in the same tau/e_obs branch", "CONDITIONAL_CONTRACT", "defines mass before orbital GM fitting if support and scale are parent-owned", "surface independence; positive M_ref; no fitted GM"),
        ("HCC2900_5_rejected_orbital_GM", "fitted orbital-GM current", "J_M chosen so int J_M reproduces observed GM", "REJECTED_AS_DERIVATION", "this puts Newton into the source definition", "forbidden shortcut"),
    ]
    return [
        add_common(
            {
                "contract_id": contract_id,
                "object": contract_object,
                "formula": formula,
                "status": status,
                "reason": reason,
                "missing_for_claim": missing_for_claim,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for contract_id, contract_object, formula, status, reason, missing_for_claim in contract_specs
    ]


def escape_rows() -> list[dict[str, Any]]:
    escape_specs = [
        ("ESC2900_0_action_adoption", "E_action_adoption", "failure of current MTS core to derive/adopt the minimal parent matter action", "source-backed parent action clause or adoption certificate", "MISSING_ACTION_ADOPTION_CERTIFICATE", "dimensionless_gate_or_action_norm", "source_current_descent;Newton;local_GR", "MISSING_NUMERIC_VALUE", SRC_2587_ACTION),
        ("ESC2900_1_q_owner", "epsilon_q_owner", "abs(int_S(J_H[q_candidate]-J_H[q_parent]))/M_ref", "parent q map, J_H density and positive same-frame M_ref", "MISSING_PARENT_Q_MAP", "dimensionless", "source_normalization;PPN;R11;local_GR", "MISSING_NUMERIC_VALUE", SRC_2588_OWNER),
        ("ESC2900_2_frame_source", "Delta_frame_source_over_MH", "abs(int_S(T_a[e_source]-T_a[e_obs]) tau^a)/M_ref", "same-frame readout theorem and source density", "MISSING_SAME_FRAME_LOCK_OR_BOUND", "dimensionless", "WEP;source_normalization;PPN;orbital", "MISSING_NUMERIC_VALUE", SRC_2588_LEAKS),
        ("ESC2900_3_tau_selector", "epsilon_tau_selector", "abs(int_S T_a(tau_role^a-tau_obs^a))/M_ref", "single parent tau identity and same-frame source density", "MISSING_PARENT_TAU_IDENTITY", "dimensionless", "clock;Hamiltonian_charge;orbit;source_mass", "MISSING_NUMERIC_VALUE", SRC_TAU_CONTRACT),
        ("ESC2900_4_ellJ_scale", "epsilon_ellJ_scale", "source-current scale drift or mismatch from non-parent ell_J", "parent ell_J theorem or finite scale-drift bound", "MISSING_PARENT_ELLJ_SCALE", "dimensionless_or_scale_drift", "Gdot;source_normalization;orbital;PPN", "MISSING_NUMERIC_VALUE", SRC_2588_LEAKS),
        ("ESC2900_5_domain_motion", "E_domain_motion", "domain/worldtube/linking-surface motion contribution to the current complex", "fixed W_source/A_ext/S_link theorem or domain-motion coefficient", "MISSING_FIXED_DOMAIN_OR_OPERATOR_BOUND", "dimensionless_or_operator_norm_times_domain_variation", "I_commutator;radial_Meff_hair;R10;orbital", "MISSING_NUMERIC_VALUE", SRC_2586_JDOMAIN),
        ("ESC2900_6_support_jump", "E_support_jump", "surface-layer or boundary-crossing current at the edge of W_source", "regular support/jump ledger with zero compact-boundary leak or finite source row", "MISSING_JUMP_LEDGER_ZERO_OR_BOUND", "GM_flux_or_dimensionless_after_Mref", "Newton;R10;R11;orbital", "MISSING_NUMERIC_VALUE", SRC_2586_JDOMAIN),
        ("ESC2900_7_current_descent", "E_current_descent", "norm of failure of J_H[e_obs,tau] to descend from parent matter action into C_H(A_ext)", "J_H=q^*Jbar_H theorem or finite current-escape row", "MISSING_CURRENT_DESCENT_ZERO_OR_VALUE", "dimensionless_or_current_norm", "I_commutator;source_normalization;PPN;R11", "MISSING_NUMERIC_VALUE", SRC_2586_JDOMAIN),
        ("ESC2900_8_extra_current_escape", "E_extra_current_escape", "non-Hilbert/memory/domain/species/boundary current not included in J_H but seen by Pi_M or q_loc", "extra-source annihilator theorem or component vector", "MISSING_EXTRA_CURRENT_ZERO_OR_BOUND", "dimensionless_or_GM_flux", "WEP;PPN;clock;R11;local_GR", "MISSING_NUMERIC_VALUE", SRC_2586_JDOMAIN),
        ("ESC2900_TOTAL", "J_domain_current_escape_envelope", "sum_abs(ESC2900_0..ESC2900_8)", "absolute no-cancellation source-worldtube/current-complex obstruction", "MISSING_COMPONENT_VALUES", "dimensionless_after_common_source_normalization", "PiM_chainmap;epsilon_charge;Newton;PPN;R10;R11;local_GR", "THIS_CHECKPOINT_SYMBOLIC_LEDGER_ONLY", SRC_2586_DOC),
    ]
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "needed_for_claim": needed_for_claim,
                "current_status": current_status,
                "units": units,
                "observable_link": observable_link,
                "numeric_value": numeric_value,
                "source_path": str(source_path),
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, symbol, definition, needed_for_claim, current_status, units, observable_link, numeric_value, source_path in escape_specs
    ]


def evaluator_rows() -> list[dict[str, Any]]:
    evaluator_specs = [
        ("EVAL2900_0_strict_owner_theorem", "strict_claim", "source_complex_owner = all(SC2900_0..SC2900_8 parent-signed)", "NOT_EVALUATED", "REFUSED_UNSIGNED_OWNER_CLAUSES", "parent matter action, q stack, tau, ell_J, fixed support/domain and same-object denominator are unsigned"),
        ("EVAL2900_1_conditional_route", "conditional_theorem_control", "MCA2587 + q/basic stack + fixed complex would give J_H=q^*Jbar_H in C_H(A_ext)", "CONDITIONAL_ONLY", "USEFUL_NOT_CLAIM", "route is mathematically clean but lacks parent adoption and owner certificates"),
        ("EVAL2900_2_escape_envelope", "nonclaim_residual_envelope", "J_domain_current_escape_envelope=sum_abs(action,q,frame,tau,ellJ,domain,support,current,extra)", "NOT_EVALUATED", "STAGED_MISSING_COMPONENT_VALUES", "all rows have units/source paths but no theorem-zero or numeric values"),
    ]
    return [
        add_common(
            {
                "eval_id": eval_id,
                "mode": mode,
                "formula": formula,
                "computed_value": computed_value,
                "result": result,
                "reason": reason,
                "runner_ready": False,
            }
        )
        for eval_id, mode, formula, computed_value, result, reason in evaluator_specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    gate_specs = [
        ("GATE2900_0_sources", "all source paths and anchors exist", "PASS", "source register validation covers cited inputs", True),
        ("GATE2900_1_hilbert_current", "Hilbert/energy current is selected as least-circular source contract", "PASS_NONCLAIM", "contract uses stress-energy instead of fitted orbital GM", True),
        ("GATE2900_2_minimal_action_candidate", "minimal parent matter action contract is available", "PASS_NONCLAIM", "2587 supplies a disciplined single observed-stack candidate", True),
        ("GATE2900_3_action_adoption", "candidate action is derived/adopted by MTS core", "FAIL", "no parent action adoption or uniqueness certificate exists", False),
        ("GATE2900_4_observed_stack", "q/e_obs/tau/ell_J observed stack is parent-owned", "FAIL", "2588 leaves q map, basic coframe, tau and ell_J unsigned", False),
        ("GATE2900_5_fixed_worldtube", "W_source/A_ext/S_link are fixed before readout", "FAIL", "support/jump/domain-owner theorem is missing", False),
        ("GATE2900_6_same_object", "Pi_M current and Hilbert source mass are the same object with common M_ref", "FAIL", "R_eq, B_zero_flux and M_ref locks remain unfilled", False),
        ("GATE2900_7_escape_rows", "J_domain/current-escape rows have units and source paths", "PASS_NONCLAIM", "rows are source-ready but not score-ready", True),
        ("GATE2900_8_no_shortcuts", "fitted GM, source-only slots and Noether-only closure are rejected", "PASS_GUARD", "forbidden routes stay explicit", True),
        ("GATE2900_9_local_GR", "Newton/local-GR source bridge is derived", "FAIL_CLOSED", "source-worldtube/current-complex owner theorem is not proved", False),
        ("GATE2900_10_next", "next target attacks the upstream q/observed-stack kernel owner", "PASS_NONCLAIM", "do not circle product-rule algebra; attack the quotient/kernel certificate", True),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": gate_passed,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for gate_id, criterion, result, reason, gate_passed in gate_specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    runner_specs = [
        ("RUN2900_0_owner_proof", "REFUSED_UNSIGNED_OWNER_CLAUSES", "parent action; observed stack; tau; ell_J; fixed W_source/A_ext/S_link; same M_ref", 0, "current MTS has conditional contracts but not parent-signed antecedents"),
        ("RUN2900_1_escape_rows", "STAGED_NONCLAIM_ROWS", "E_action_adoption;epsilon_q_owner;Delta_frame_source;epsilon_tau_selector;epsilon_ellJ_scale;E_domain_motion;E_support_jump;E_current_descent;E_extra_current_escape", 0, "units and source paths exist, values/theorem-zero proofs do not"),
        ("RUN2900_2_next_kernel", "NEXT_TARGET_SELECTED", "q map, vertical kernel nullness, basic coframe, tau/ellJ owner", 0, "the source-complex proof now reduces upstream to the q/observed-stack kernel certificate"),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "status": status,
                "required_components": required_components,
                "components_evaluable": components_evaluable,
                "reason": reason,
                "runner_ready": False,
            }
        )
        for runner_id, status, required_components, components_evaluable, reason in runner_specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    decision_specs = [
        ("DEC2900_0_keep_hilbert_route", "KEEP_HILBERT_ENERGY_CURRENT_AS_PRIMARY", "it is the only route in this stack that can honestly reduce toward GR/Newton without fitting GM into the definition", "retain J_M^mu=ell_J T_H^{mu nu} tau_nu as a contract"),
        ("DEC2900_1_no_promotion", "DO_NOT_PROMOTE_SOURCE_COMPLEX_OWNER", "the current corpus has conditional action/quotient/current-complex theorems but not parent-signed adoption and owner certificates", "keep J_domain_current_escape_envelope nonclaim"),
        ("DEC2900_2_reduce_upstream", "SOURCE_COMPLEX_LOCK_REDUCES_TO_Q_OBSERVED_STACK_KERNEL_LOCK", "2587/2588 show matter descent needs q/e_obs/tau/ell_J ownership and a null/matter-invisible kernel", "attack the q/observed-stack kernel certificate next"),
        ("DEC2900_3_no_magic", "FORBID_FITTED_GM_NOETHER_ONLY_AND_SOURCE_SLOT_CLOSURES", "those routes assume the source equality instead of deriving it", "allow only explicit closure labels, no derivation credit"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in decision_specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2900_0_2901",
                "status": "selected_primary",
                "target_doc": "2901-Y5-R2FR-parent-q-observed-stack-kernel-nullness-or-current-escape-bound-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_parent_q_observed_stack_kernel_nullness_or_current_escape_bound_under_AX1090_2901.py",
                "mission": "prove a parent q map with regular quotient, ker(Dq) presymplectic-null and matter-invisible, and basic e_obs/tau/ell_J stack; if proof fails, fill q/frame/tau/ellJ current-escape rows with units and source paths",
                "forbidden": "q=(e_obs,...) projection by declaration; standard-GR minimal coupling import as MTS proof; fitted GM; post-readout tau/frame; source-only slot; Newton/local-GR/beta/R10 claim; GitHub action; formalization-workbench edit",
                "selected": True,
            }
        ),
        add_common(
            {
                "next_id": "NEXT2900_1_held_extra_projection",
                "status": "held_after_current_complex_owner",
                "target_doc": "2901b-Y5-R2FR-extra-current-projection-channelwise-zero-or-source-envelope-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_extra_current_projection_channelwise_zero_or_source_envelope_under_AX1090_2901b.py",
                "mission": "attack Pi_M dJ_extra channelwise only after q/current-complex ownership is claim-grade or explicitly bounded",
                "forbidden": "channel cancellation; measured-GM absorption; local-GR claim",
                "selected": False,
            }
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("BR2900_0_owner_copy", OUTPUTS["owner"], BRANCH_OUTPUTS["owner_copy"], "RAB queue copy of source-complex owner audit"),
        ("BR2900_1_contract_copy", OUTPUTS["contract"], BRANCH_OUTPUTS["contract_copy"], "RAB queue copy of Hilbert-current complex contract"),
        ("BR2900_2_escape_copy", OUTPUTS["escape"], BRANCH_OUTPUTS["escape_copy"], "local-bounds copy of source-worldtube/current-escape rows"),
        ("BR2900_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue copy of next q/observed-stack kernel target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in copy_specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def formalization_touched() -> bool:
    if not FORMALIZATION.exists():
        return False
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for candidate_path in FORMALIZATION.rglob("*"):
        try:
            if candidate_path.is_file() and candidate_path.stat().st_mtime >= start_timestamp:
                return True
        except OSError:
            return True
    return False


def local_source_path_exists(source_path: str) -> bool:
    return Path(source_path).exists()


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    owner_rows_data = all_rows["owner"]
    escape_rows_data = all_rows["escape"]
    evaluator_rows_data = all_rows["evaluator"]
    gate_rows_data = all_rows["gates"]
    next_rows_data = all_rows["next"]
    branch_rows_data = all_rows["branches"]
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]

    required_symbols = {
        "E_action_adoption",
        "epsilon_q_owner",
        "Delta_frame_source_over_MH",
        "epsilon_tau_selector",
        "epsilon_ellJ_scale",
        "E_domain_motion",
        "E_support_jump",
        "E_current_descent",
        "E_extra_current_escape",
        "J_domain_current_escape_envelope",
    }
    found_symbols = {row["symbol"] for row in escape_rows_data}
    value_rows = [row for row in escape_rows_data if row["row_id"] != "ESC2900_TOTAL"]

    checks = [
        ("VAL2900_0_sources_exist", all(row["path_exists"] for row in source_rows), "all registered source paths exist"),
        ("VAL2900_1_source_anchors", all(row["anchors_found"] for row in source_rows), "all registered source anchors were found"),
        ("VAL2900_2_owner_refused", any(row["audit_id"] == "SC2900_9_verdict" and "FAIL" in row["current_status"] for row in owner_rows_data), "source-worldtube/current-complex owner theorem remains refused"),
        ("VAL2900_3_hilbert_route_retained", any(row["gate_id"] == "GATE2900_1_hilbert_current" and row["result"] == "PASS_NONCLAIM" for row in gate_rows_data), "Hilbert-current route retained as least-circular contract"),
        ("VAL2900_4_required_escape_rows", required_symbols <= found_symbols, "all required current-escape symbols are present"),
        ("VAL2900_5_escape_rows_nonclaim", all(not row["valid_for_claim"] and not row["accepted_for_scoring"] for row in escape_rows_data), "all escape rows remain nonclaim"),
        ("VAL2900_6_escape_units_sources", all(row["units"] and local_source_path_exists(row["source_path"]) for row in value_rows), "non-total escape rows have units and existing source paths"),
        ("VAL2900_7_evaluator_refuses", any(row["eval_id"] == "EVAL2900_0_strict_owner_theorem" and row["result"] == "REFUSED_UNSIGNED_OWNER_CLAUSES" for row in evaluator_rows_data), "strict source-complex evaluator refuses unsigned owner clauses"),
        ("VAL2900_8_no_shortcut_guard", any(row["gate_id"] == "GATE2900_8_no_shortcuts" and row["result"] == "PASS_GUARD" for row in gate_rows_data), "fitted GM, source-only slots and Noether-only closure remain forbidden"),
        ("VAL2900_9_local_gr_fail_closed", any(row["gate_id"] == "GATE2900_9_local_GR" and row["result"] == "FAIL_CLOSED" for row in gate_rows_data), "local GR/Newton remains fail-closed"),
        ("VAL2900_10_next_target_2901", any(row["next_id"] == "NEXT2900_0_2901" and row["selected"] for row in next_rows_data), "2901 q/observed-stack kernel target selected"),
        ("VAL2900_11_branch_copies_exist", all(row["exists"] for row in branch_rows_data), "branch copies were written"),
        ("VAL2900_12_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs), "all generated CSV outputs parse cleanly"),
        ("VAL2900_13_formalization_untouched_during_run", not formalization_touched(), "formalization-workbench was not touched during this run"),
    ]
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL2900_OVERALL", overall, "2900 validation overall"))
    return [
        {
            "check_id": check_id,
            "passed": passed,
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2900 - Y5 R2FR Source-Worldtube Current-Complex Owner or Jdomain Bound Fill Under AX1090",
        "",
        f"Run: `runs/{SCRIPT_START_UTC.strftime('%Y%m%d-%H%M%S')}-Y5-R2FR-source-worldtube-current-complex-owner-or-Jdomain-bound-fill-under-AX1090`",
        "Status: `Y5_R2FR_2900_source_complex_owner_not_derived_Jdomain_escape_rows_source_ready_q_stack_kernel_2901_next`",
        "Claim ceiling: `source_complex_owner_and_Jdomain_current_escape_nonclaim_only_no_PiM_lock_epsilon_charge_Newton_beta_PPN_local_GR_R10_or_GitHub_claim`",
        "",
        "## Summary",
        "",
        "2900 tries the direct source-worldtube/current-complex proof selected by 2899. It does not close for current MTS.",
        "",
        "The clean route remains: define ordinary matter through one parent-owned observed stack, derive the Hilbert source current before readout, fix `W_source/A_ext/S_link`, then let a parent-selected `Pi_M` act as a fixed chain map on that same current complex. If all of that were parent-signed, the 2899 commutator route would become claim-grade.",
        "",
        "Current MTS has the shape of this route but not the parent signatures. The 2587 minimal matter action is a disciplined candidate, not a derived action. The 2588 observed stack is an exact quotient/basic-coframe route, not an owned `q/e_obs/tau/ell_J` theorem. Therefore `J_domain_current_escape_envelope` is now the active nonclaim residual pack.",
        "",
        "The important progress is reduction: this blocker now points upstream to one sharper certificate, not a fog bank. The next target is a parent `q` map with a presymplectic-null, matter-invisible kernel and a basic observed stack.",
        "",
        "## Source Register",
        "",
        md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## Source-Complex Owner Audit",
        "",
        md_table(all_rows["owner"], ["audit_id", "owner_clause", "formal_statement", "current_status", "blocking_gap", "effect_if_missing", "valid_for_claim"]),
        "",
        "## Hilbert Current Complex Contract",
        "",
        md_table(all_rows["contract"], ["contract_id", "object", "formula", "status", "reason", "missing_for_claim", "valid_for_claim"]),
        "",
        "## Jdomain Current-Escape Rows",
        "",
        md_table(all_rows["escape"], ["row_id", "symbol", "definition", "current_status", "units", "observable_link", "numeric_value", "source_path", "valid_for_claim"]),
        "",
        "## Evaluator",
        "",
        md_table(all_rows["evaluator"], ["eval_id", "mode", "computed_value", "result", "reason", "runner_ready", "valid_for_claim"]),
        "",
        "## Acceptance Gates",
        "",
        md_table(all_rows["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"]),
        "",
        "## Runner Status",
        "",
        md_table(all_rows["runner"], ["runner_id", "status", "required_components", "components_evaluable", "reason", "runner_ready", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(all_rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(all_rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(all_rows["validation"], ["check_id", "passed", "detail", "generated_utc"]),
        "",
        "## Working Read",
        "",
        "This is not a dead end; it is the coupling problem sharpening into an actual theorem contract. The source current is no longer allowed to be an orbital-GM disguise. It must come from a parent matter action over a parent-owned observed stack. That is exactly the kind of bridge a serious GR-reduction proof needs.",
        "",
        "## Forbidden Claims From 2900",
        "",
        "- MTS has proved the source-worldtube/current-complex owner theorem.",
        "- MTS has proved `J_H=q^*Jbar_H` for the current corpus.",
        "- MTS has fixed `W_source/A_ext/S_link`, `tau`, `ell_J`, and `M_ref` as one parent-owned complex.",
        "- MTS has proved `[d,Pi_M]J_H=0`, `epsilon_charge=0`, measured `GM`, source-normalized Newton, beta, PPN, R10, or local GR.",
        "- Fitted orbital `GM`, Noether conservation alone, source-only slots, or a readout-defined worldtube count as derivations.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {}
    all_rows["sources"] = source_register_rows()
    all_rows["owner"] = owner_audit_rows()
    all_rows["contract"] = contract_rows()
    all_rows["escape"] = escape_rows()
    all_rows["evaluator"] = evaluator_rows()
    all_rows["gates"] = gate_rows()
    all_rows["runner"] = runner_rows()
    all_rows["decision"] = decision_rows()
    all_rows["next"] = next_rows()

    for output_key in ["sources", "owner", "contract", "escape", "evaluator", "gates", "runner", "decision", "next"]:
        write_csv(OUTPUTS[output_key], all_rows[output_key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_doc(all_rows)

    overall = next(row["passed"] for row in all_rows["validation"] if row["check_id"] == "VAL2900_OVERALL")
    print(f"2900 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()
