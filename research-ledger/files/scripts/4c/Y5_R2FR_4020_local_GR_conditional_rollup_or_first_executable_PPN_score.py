from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4020"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4020-Y5-R2FR-local-GR-conditional-rollup-or-first-executable-PPN-score.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4020_SOURCE_REGISTER.csv",
    "rollup": SRC / "P8_Y5_R2FR_4020_LOCAL_GR_ROLLUP_CHAIN.csv",
    "audit": SRC / "P8_Y5_R2FR_4020_ADOPTION_EVIDENCE_AUDIT.csv",
    "score": SRC / "P8_Y5_R2FR_4020_FIRST_EXECUTABLE_PPN_SCORE_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4020_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4020_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4020_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4020_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4020_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4020_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4020_VALIDATION.csv",
}

NEXT_DOC = "4021-Y5-R2FR-parent-adoption-witness-or-first-PPN-score-input-fill.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4021_parent_adoption_witness_or_first_PPN_score_input_fill.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4020_00_handoff", SRC / "P8_Y5_R2FR_4019_NEXT_TARGET.csv", "NEXT4019_0", "4019 handoff to 4020"),
        ("SRC4020_01_4012_charge", SRC / "P8_Y5_R2FR_4012_PIM_HTAU_CHARGE_LOCK_THEOREM.csv", "CHG4012_0_parent_constraint_map", "Pi_M/H_tau charge map"),
        ("SRC4020_02_4013_em_once", SRC / "P8_Y5_R2FR_4013_MAXWELL_POYNTING_ONCE_ONLY_THEOREM.csv", "MPE4013_1_Maxwell_Hilbert_stress", "EM stress once-only source"),
        ("SRC4020_03_4014_hodge", SRC / "P8_Y5_R2FR_4014_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv", "OHN4014_0_observed_Hodge_lock", "observed Hodge owner"),
        ("SRC4020_04_4015_newton", SRC / "P8_Y5_R2FR_4015_GAUSS_POISSON_GREF_NEWTON_THEOREM.csv", "GPN4015_1_EH00_to_Poisson", "EH00 to Poisson bridge"),
        ("SRC4020_05_4015_finite", SRC / "P8_Y5_R2FR_4015_NEWTON_BRIDGE_FINITE_ROWS.csv", "NBR4015_0_master", "Newton bridge finite residuals"),
        ("SRC4020_06_4016_superselection", SRC / "P8_Y5_R2FR_4016_GREF_SUPERSELECTION_THEOREM.csv", "GSS4016_0_global_sector_factorization", "G_ref superselection"),
        ("SRC4020_07_4016_drift", SRC / "P8_Y5_R2FR_4016_GREF_DRIFT_RANGE_FINITE_ROWS.csv", "GREF4016_0_master", "G_ref drift/range residuals"),
        ("SRC4020_08_4017_packet", SRC / "P8_Y5_R2FR_4017_KAPPA_SECTOR_INSERTION_PACKET.csv", "KSP4017_1_action", "kappa sector action packet"),
        ("SRC4020_09_4017_nohom", SRC / "P8_Y5_R2FR_4017_KAPPA_VARIATION_AND_NOHOM_THEOREM.csv", "KVT4017_0_local_variation_zero", "no local kappa variation"),
        ("SRC4020_10_4018_gamma", SRC / "P8_Y5_R2FR_4018_SECOND_ORDER_PPN_STABILITY_THEOREM.csv", "PPN4018_1_gamma_EH_zero", "gamma theorem"),
        ("SRC4020_11_4018_beta", SRC / "P8_Y5_R2FR_4018_SECOND_ORDER_PPN_STABILITY_THEOREM.csv", "PPN4018_3_beta_EH_zero", "beta theorem"),
        ("SRC4020_12_4018_residual", SRC / "P8_Y5_R2FR_4018_GAMMA_BETA_SOURCE_RESIDUAL_ROWS.csv", "PPR4018_0_master", "second-order PPN residual vector"),
        ("SRC4020_13_4019_adoption", SRC / "P8_Y5_R2FR_4019_EH_ONLY_R11_ADOPTION_CLAUSES.csv", "EHA4019_1_R11_absent", "EH-only/R11 adoption clause"),
        ("SRC4020_14_4019_theorem", SRC / "P8_Y5_R2FR_4019_NO_EXTRA_OPERATOR_THEOREM.csv", "NOX4019_2_EH_PPN_solution", "EH-only PPN theorem"),
        ("SRC4020_15_4019_scorer", SRC / "P8_Y5_R2FR_4019_PPN_RESIDUAL_SCORER_ROWS.csv", "PPS4019_0_master", "PPN residual scorer"),
        ("SRC4020_16_4019_results", SRC / "P8_Y5_R2FR_4019_EVALUATOR_RESULTS.csv", "CASE4019_0_full_EH_only_adopted", "4019 evaluator result"),
        ("SRC4020_17_3886_vector", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_00_delta_gamma_R11", "older coefficient skeleton"),
        ("SRC4020_18_3915_vector", SRC / "P8_Y5_R2FR_3915_EXECUTABLE_PPN_RESIDUAL_VECTOR.csv", "PPNR3915_8_total", "older executable residual vector"),
        ("SRC4020_19_3933_rollup", SRC / "P8_Y5_R2FR_3933_PPN_ZERO_ROLLUP.csv", "PPN3933_8_total", "private zero rollup guard"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "role": role,
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def rollup_chain_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "rollup_id": "ROLL4020_0_source_charge",
            "component": "source charge/readout",
            "inherits_from": "4012, 4015",
            "mathematical_form": "Pi_M^C J_H -> M_H_ref; G_00^(1)=kappa_ref T_00^H with kappa_ref=8*pi*G_ref/c^4",
            "closes_if": "parent owns Pi_M/H_tau charge map and same observed source frame",
            "current_status": "conditional_coherent_unsigned",
            "residual_if_unsigned": "C_PiM_H + C_frame + delta_readout_frame",
            "next_action": "write parent-owned source-charge witness, or score readout/source residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "rollup_id": "ROLL4020_1_global_coupling",
            "component": "G_ref/kappa global sector",
            "inherits_from": "4016, 4017",
            "mathematical_form": "Q_parent ~= Q_dyn x K_G; kappa_* in K_G; delta_local kappa_*=0; G_ref=c^4*kappa_*/(8*pi)",
            "closes_if": "final parent action adopts K_G as a global branch parameter, not a local scalar field",
            "current_status": "candidate_parent_packet_unsigned",
            "residual_if_unsigned": "C_sector + C_noHom + Gdot/G + range/material coupling leakage",
            "next_action": "turn 4017 packet into a parent-action witness clause and reject scalar-kappa leakage",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "rollup_id": "ROLL4020_2_EM_once_only",
            "component": "EM/Hilbert current once-only slot",
            "inherits_from": "4013, 4014",
            "mathematical_form": "T_EM from observed Hodge *_obs contributes once to J_H_total; no separate fitted EM mass channel",
            "closes_if": "typed action domain owns *_obs, mu0 constants, current J, and binding terms in the same source variation",
            "current_status": "conditional_coherent_unsigned",
            "residual_if_unsigned": "epsilon_EM_once + Delta_Hodge_EM + source double-count risk",
            "next_action": "insert the observed-Hodge/source-current owner into the parent local action",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "rollup_id": "ROLL4020_3_second_order_PPN",
            "component": "gamma/beta second-order law",
            "inherits_from": "4018",
            "mathematical_form": "gamma-1=0 under EH spatial stress; beta_eff=B_source/A_source^2 and beta-1=0 only if B_source=A_source^2",
            "closes_if": "EH-only nonlinear completion fixes B_source after A_source is fixed by Newton bridge",
            "current_status": "exact_conditional_theorem_unsigned",
            "residual_if_unsigned": "delta_gamma_R11 + delta_beta_source + delta_beta_R11 + delta_beta_q_loc",
            "next_action": "derive square-law source stability or score beta source prefactor explicitly",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "rollup_id": "ROLL4020_4_EH_only_R11",
            "component": "R11/q_loc no-extra operator gate",
            "inherits_from": "4019",
            "mathematical_form": "S_loc^{<=2PN}=S_EH+S_matter+S_EM+dB_proper+S_topological; Allowed(O_R11)={topological, exact, auxiliary-double-zero, Sigma_loc-selected-zero}",
            "closes_if": "final parent branch explicitly excludes non-EH R11/q_loc/projector stress through O(U^2)",
            "current_status": "conditional_exact_gate_not_adopted",
            "residual_if_unsigned": "delta_gamma_R11 + delta_beta_R11 + delta_beta_q_loc + alpha_lambda",
            "next_action": "prove no-extra operator theorem from parent domain, or fill first executable PPN coefficients",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "rollup_id": "ROLL4020_5_conditional_local_GR_vector",
            "component": "conditional local-GR vector",
            "inherits_from": "4015-4019",
            "mathematical_form": "If ROLL4020_0..4 are parent-signed, then gamma=beta=1 and alpha_i=xi=zeta_i=Gdot=0 in the local branch",
            "closes_if": "all adoption evidence clauses are signed or every corresponding scorer row is numeric and passes",
            "current_status": "route_exists_but_no_public_claim",
            "residual_if_unsigned": "Delta_PPN_abs_4019",
            "next_action": "4021 must either write the adoption witness or fill the first scoreable coefficient block",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def adoption_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "AUD4020_0_parent_action_KG",
            "evidence_needed": "parent action explicitly includes K_G and kappa_* as a global branch parameter",
            "current_evidence": "4017 candidate packet exists, not final parent adoption",
            "decision": "unsigned",
            "next_action": "write an adoption witness line in the parent local action, or route to Gdot/range scorer",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4020_1_parent_action_EH_only",
            "evidence_needed": "parent local branch is EH-only plus matter/EM/exact/topological pieces through 2PN",
            "current_evidence": "4019 conditional gate exists, but final corpus action has not adopted it",
            "decision": "unsigned",
            "next_action": "derive the no-extra operator result from the parent domain restrictions",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4020_2_source_charge",
            "evidence_needed": "Pi_M/H_tau/Hilbert source equality is parent-owned before orbital readout",
            "current_evidence": "4012 and 4015 give a conditional charge map and Newton bridge",
            "decision": "unsigned",
            "next_action": "prove chain-map/source equality in the adopted local branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4020_3_source_square_law",
            "evidence_needed": "second-order source coefficient obeys B_source=A_source^2 after A_source is fixed",
            "current_evidence": "4018 identifies beta law; no parent-owned coefficient witness yet",
            "decision": "unsigned",
            "next_action": "derive beta square law from EH nonlinear completion or score delta_beta_source",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4020_4_EM_owner",
            "evidence_needed": "observed Hodge, Poynting/current, and binding energy are in the same Hilbert source variation once",
            "current_evidence": "4013/4014 conditional owner theorems exist",
            "decision": "unsigned",
            "next_action": "bind EM owner theorem into the parent source/current clause",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4020_5_q_loc_projector_kernel",
            "evidence_needed": "q_loc and Khat tails lie in the PPN projector kernel through O(U^2)",
            "current_evidence": "4019 states the kernel condition, not a parent proof",
            "decision": "unsigned",
            "next_action": "derive projector-kernel zero or score delta_beta_q_loc/alpha_lambda",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4020_6_preferred_frame_conservation",
            "evidence_needed": "domain/coframe/memory selectors do not generate alpha_i, xi, or zeta_i terms",
            "current_evidence": "scorer rows exist but no numeric/source-backed fill",
            "decision": "unsigned",
            "next_action": "derive diffeo-covariant conservation identity in the adopted branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "AUD4020_7_public_claim_guard",
            "evidence_needed": "all adoption clauses signed or all scorer rows numeric and passing",
            "current_evidence": "not satisfied",
            "decision": "claim_blocked",
            "next_action": "keep checkpoint private/nonclaim until 4021+ closes at least one primary block",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def score_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "score_id": "FES4020_0_delta_gamma_R11",
            "quantity": "delta_gamma_R11",
            "formula": "Pi_gamma[DeltaE_R11^{(1)}] + readout/frame spatial-stress terms",
            "needed_input": "R11 first-order operator coefficient or theorem-zero adoption",
            "current_input": "MISSING_PARENT_ADOPTION_OR_NUMERIC_COEFFICIENT",
            "score_ready": False,
            "priority": 1,
            "next_derivation": "prove non-EH R11 stress is topological/exact/auxiliary-double-zero, otherwise compute Pi_gamma coefficient",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "score_id": "FES4020_1_delta_beta_source",
            "quantity": "delta_beta_source",
            "formula": "B_source/A_source^2 - 1 + epsilon_SN",
            "needed_input": "A_source and B_source from the same parent source current",
            "current_input": "MISSING_B_SOURCE_PARENT_WITNESS",
            "score_ready": False,
            "priority": 2,
            "next_derivation": "derive B_source=A_source^2 from EH nonlinear completion after Newton source normalization",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "score_id": "FES4020_2_delta_beta_R11",
            "quantity": "delta_beta_R11",
            "formula": "Pi_beta[DeltaE_R11^{(2)}]",
            "needed_input": "R11 second-order metric operator coefficient or theorem-zero adoption",
            "current_input": "MISSING_R11_2PN_COEFFICIENT",
            "score_ready": False,
            "priority": 3,
            "next_derivation": "extend no-extra R11 proof to O(U^2), or compute beta projection of residual operator",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "score_id": "FES4020_3_delta_beta_q_loc",
            "quantity": "delta_beta_q_loc",
            "formula": "Pi_beta[q_loc_Khat^{(2)}] + finite-range alpha_lambda tail",
            "needed_input": "PPN projector-kernel proof or q_loc amplitude/profile coefficient",
            "current_input": "MISSING_QLOC_PROJECTOR_KERNEL_OR_BOUND",
            "score_ready": False,
            "priority": 4,
            "next_derivation": "map q_loc/Khat to PPN projectors and prove kernel zero; otherwise source a bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "score_id": "FES4020_4_preferred_frame",
            "quantity": "alpha1, alpha2, alpha3, xi",
            "formula": "PPN vector/domain/coframe/memory selector projections",
            "needed_input": "diffeomorphism/conservation identity in observed branch or numeric component bounds",
            "current_input": "MISSING_SELECTOR_PROJECTION",
            "score_ready": False,
            "priority": 5,
            "next_derivation": "prove no preferred-frame selector survives once e_obs and K_G are fixed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "score_id": "FES4020_5_conservation_zeta",
            "quantity": "zeta_i",
            "formula": "nonconservative stress/source residual projections",
            "needed_input": "same-action Hilbert conservation identity including EM/binding",
            "current_input": "MISSING_TOTAL_SOURCE_CONSERVATION_WITNESS",
            "score_ready": False,
            "priority": 6,
            "next_derivation": "derive nabla_mu T_total^{mu nu}=0 from the adopted source action",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "score_id": "FES4020_6_Gdot",
            "quantity": "Gdot/G",
            "formula": "D_t ln G_ref under K_G branch sector",
            "needed_input": "K_G no-Hom/superselection final adoption or external bound",
            "current_input": "MISSING_FINAL_KG_ADOPTION",
            "score_ready": False,
            "priority": 7,
            "next_derivation": "adopt K_G packet as branch constant and prove no morphism from time/range/source into K_G",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "score_id": "FES4020_7_master_abs_sum",
            "quantity": "Delta_PPN_abs_4020",
            "formula": "sum(abs(FES4020_0..6 components)) with no cancellation credit",
            "needed_input": "every component theorem-zero or numeric/source-backed",
            "current_input": "NOT_SCOREABLE_CURRENTLY",
            "score_ready": False,
            "priority": 8,
            "next_derivation": "do not run a claim score until at least one primary coefficient block is filled",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4020_0_all_parent_signed",
            "branch_signature": "K_G adopted; EH-only/R11 no-extra adopted; Pi_M/H_tau source adopted; EM once-only adopted; q_loc projector zero",
            "adoption_signed": True,
            "score_inputs_numeric": False,
            "expected_result": "CONDITIONAL_LOCAL_GR_ZERO_VECTOR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4020_1_current_state",
            "branch_signature": "conditional packets exist, no final adoption witness, no numeric PPN score inputs",
            "adoption_signed": False,
            "score_inputs_numeric": False,
            "expected_result": "LOCAL_GR_ROUTE_EXISTS_BUT_NOT_SCOREABLE_OR_CLAIMABLE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4020_2_R11_open",
            "branch_signature": "source/K_G accepted provisionally, R11/q_loc no-extra theorem unsigned",
            "adoption_signed": False,
            "score_inputs_numeric": False,
            "expected_result": "ROUTE_TO_DELTA_GAMMA_R11_DELTA_BETA_R11_QLOC",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4020_3_source_square_open",
            "branch_signature": "Newton bridge works but beta source square law unsigned",
            "adoption_signed": False,
            "score_inputs_numeric": False,
            "expected_result": "ROUTE_TO_DELTA_BETA_SOURCE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4020_4_score_inputs_supplied",
            "branch_signature": "adoption not final but every scorer coefficient is numeric/source-backed",
            "adoption_signed": False,
            "score_inputs_numeric": True,
            "expected_result": "EXECUTABLE_ABS_SUM_SCORE_AVAILABLE_BUT_NOT_CURRENTLY_POPULATED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        case_id = str(case["case_id"])
        if case["adoption_signed"]:
            owner_status = "CONDITIONAL_ZERO_VECTOR_IF_PARENT_WITNESS_REAL"
            ppn_result = "gamma=1, beta=1, alpha_i=xi=zeta_i=Gdot=0 conditionally"
            next_action = "turn hypothetical witness into actual parent-action text before any claim"
        elif case["score_inputs_numeric"]:
            owner_status = "EXECUTABLE_SCORE_ROUTE_AVAILABLE_IN_PRINCIPLE"
            ppn_result = "Delta_PPN_abs can be evaluated only after numeric rows replace placeholders"
            next_action = "fill score rows with sourced coefficients and bounds"
        elif case_id == "CASE4020_2_R11_open":
            owner_status = "R11_QLOC_PRIMARY_BLOCK"
            ppn_result = "delta_gamma_R11, delta_beta_R11, and delta_beta_q_loc remain live"
            next_action = "derive no-extra R11/projector kernel or fill those coefficients first"
        elif case_id == "CASE4020_3_source_square_open":
            owner_status = "BETA_SOURCE_PRIMARY_BLOCK"
            ppn_result = "delta_beta_source remains live even if Newtonian normalization works"
            next_action = "derive B_source=A_source^2 from EH/source completion"
        else:
            owner_status = "CURRENT_STATE_NOT_SCOREABLE_NONCLAIM"
            ppn_result = "local-GR branch is coherent as a conditional route, but no public PPN pass exists"
            next_action = "4021 should attempt adoption witness first, then first coefficient fill if witness fails"
        rows.append(
            {
                "case_id": case_id,
                "owner_status": owner_status,
                "ppn_result": ppn_result,
                "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4020",
                "next_action": next_action,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4020_0_rollup_status",
            "decision": "local-GR route is coherent but conditional",
            "rationale": "4015-4019 form a finite chain from source/G_ref/Newton to gamma/beta/no-extra-operator gates",
            "effect": "project has moved from vague local closure to a precise adoption-or-score fork",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4020_1_best_next_move",
            "decision": "try parent adoption witness before broad source sweeps",
            "rationale": "one signed parent local action could zero many PPN terms at once; source sweeps only bound leftovers",
            "effect": "4021 is a derivation-forward move, not another inventory loop",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4020_2_score_if_witness_fails",
            "decision": "fallback to first executable PPN coefficient fill",
            "rationale": "if EH-only/R11/q_loc/source square law cannot be adopted, the scorer gives a falsifiable residual route",
            "effect": "failure becomes measurable instead of hand-waved",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4020_3_no_G_claim",
            "decision": "do not claim numerical G derivation",
            "rationale": "current chain calibrates a universal coupling; it does not predict the measured value of G",
            "effect": "avoids a weak overclaim while preserving the GR/Newton reduction route",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4020_4_next",
            "decision": f"move to {NEXT_DOC}",
            "rationale": "4021 should either write the parent adoption witness or fill the first PPN score inputs",
            "effect": "next checkpoint has a concrete target with a pass/fail fork",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CLAIM4020_0_local_GR",
            "claim": "MTS locally reduces to GR/PPN",
            "allowed": False,
            "reason": "adoption witness and/or executable numeric PPN score is not complete",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4020_1_Newton",
            "claim": "MTS derives numerical Newton constant G",
            "allowed": False,
            "reason": "G_ref is a calibrated universal coupling in the current branch, not a predicted number",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4020_2_PPN_score",
            "claim": "PPN residual vector passes bounds",
            "allowed": False,
            "reason": "score rows are structured but not numeric/source-backed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4020_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "objective": "attempt the parent adoption witness for K_G, EH-only/R11, source charge, EM owner, and q_loc projector kernel; if any clause fails, fill the first executable PPN score input rows",
            "success_condition": "at least one primary local-GR blocker becomes either parent-signed theorem-zero or numeric/source-backed scorer input",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "private_nonclaim_checkpoint",
            "summary": "local-GR route rolled up into an adoption-or-score fork; no public claim",
            "current_best_route": "derive parent adoption witness first, score residual coefficients second",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    source_hits = sum(1 for row in sources if row["exists"] and row["needle_found"])
    source_total = len(sources)
    current_result = next(row for row in results if row["case_id"] == "CASE4020_1_current_state")
    DOC_PATH.write_text(
        f"""# 4020 - Local GR Conditional Rollup Or First Executable PPN Score

- Timestamp: `{timestamp}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

The local-GR branch has now moved from scattered gates into one clean adoption-or-score fork:

1. **Adoption route:** if the parent action explicitly adopts the 4017 `K_G` packet, the 4019 EH-only/R11 no-extra local action, the 4012/4015 source-charge map, the 4013/4014 EM once-only owner, and the q_loc PPN-projector kernel, then the local branch conditionally gives the GR PPN vector:

`gamma=1`, `beta=1`, `alpha_i=xi=zeta_i=0`, and `Gdot/G=0`.

2. **Score route:** if any adoption clause fails, the branch falls into the absolute PPN residual score:

`Delta_PPN_abs_4020 = |delta_gamma_R11|+|delta_beta_source|+|delta_beta_R11|+|delta_beta_q_loc|+|alpha_i|+|xi|+|zeta_i|+|Gdot/G|`.

No cancellation credit is allowed.

## Current State

- Current evaluator result: `{current_result["owner_status"]}`.
- PPN result: `{current_result["ppn_result"]}`.
- Claim result: `{current_result["claim_result"]}`.
- Source needles found: `{source_hits}/{source_total}`.

## What This Actually Means

This is progress, not victory. The chain is no longer "maybe local closure saves us"; it is now:

`parent adoption witness OR executable PPN residual score`.

The best next move is the derivation-first route: try to write the parent-owned local action witness that makes the EH-only/R11/no-extra and source-current clauses real. If that witness cannot be written without cheating, fill the first PPN coefficient rows instead.

## Missing Before Any Public Claim

- Final parent action must adopt `K_G` as a global branch sector.
- Final parent action must adopt EH-only plus matter/EM/exact/topological local operators through 2PN.
- `Pi_M/H_tau` source equality must be parent-owned before orbital readout.
- `B_source=A_source^2` must be derived or scored.
- `q_loc/Khat` must be killed by PPN projectors or bounded numerically.
- Preferred-frame/conservation terms must be theorem-zero or score-backed.

## Next Target

- `{NEXT_DOC}`
- `{NEXT_SCRIPT}`
""",
        encoding="utf-8",
    )


def append_spine(timestamp: str) -> None:
    marker = "## 4020 - Local GR Conditional Rollup And PPN Score Fork"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: local GR is now a precise adoption-or-score fork, not a closure slogan.
- Conditional route: 4015 source/Newton bridge + 4016/4017 `K_G` coupling packet + 4013/4014 EM owner + 4018 gamma/beta theorem + 4019 EH-only/R11 no-extra gate.
- If all parent-owned clauses are signed, the branch conditionally gives `gamma=beta=1`, `alpha_i=xi=zeta_i=0`, and `Gdot/G=0`.
- If any clause fails, use `Delta_PPN_abs_4020` with no cancellation credit.
- No claim: the current branch is coherent but unsigned and not yet scoreable.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4020 - Local GR Conditional Rollup And PPN Score Fork" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    rollup: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    score: list[dict[str, Any]],
    results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4020_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4020_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    for idx, rollup_id in enumerate(
        [
            "ROLL4020_0_source_charge",
            "ROLL4020_1_global_coupling",
            "ROLL4020_2_EM_once_only",
            "ROLL4020_3_second_order_PPN",
            "ROLL4020_4_EH_only_R11",
            "ROLL4020_5_conditional_local_GR_vector",
        ],
        start=2,
    ):
        add(f"VAL4020_{idx:02d}_rollup", any(row["rollup_id"] == rollup_id for row in rollup), f"{rollup_id} present")
    for idx, audit_id in enumerate(
        [
            "AUD4020_0_parent_action_KG",
            "AUD4020_1_parent_action_EH_only",
            "AUD4020_2_source_charge",
            "AUD4020_3_source_square_law",
            "AUD4020_4_EM_owner",
            "AUD4020_5_q_loc_projector_kernel",
            "AUD4020_6_preferred_frame_conservation",
            "AUD4020_7_public_claim_guard",
        ],
        start=8,
    ):
        add(f"VAL4020_{idx:02d}_audit", any(row["audit_id"] == audit_id for row in audit), f"{audit_id} present")
    for idx, score_id in enumerate(
        [
            "FES4020_0_delta_gamma_R11",
            "FES4020_1_delta_beta_source",
            "FES4020_2_delta_beta_R11",
            "FES4020_3_delta_beta_q_loc",
            "FES4020_4_preferred_frame",
            "FES4020_5_conservation_zeta",
            "FES4020_6_Gdot",
            "FES4020_7_master_abs_sum",
        ],
        start=16,
    ):
        add(f"VAL4020_{idx:02d}_score", any(row["score_id"] == score_id for row in score), f"{score_id} present")
    result_lookup = {row["case_id"]: row for row in results}
    add("VAL4020_24_current_nonclaim", result_lookup["CASE4020_1_current_state"]["owner_status"] == "CURRENT_STATE_NOT_SCOREABLE_NONCLAIM", "current case remains nonclaim")
    add("VAL4020_25_adoption_case", result_lookup["CASE4020_0_all_parent_signed"]["owner_status"] == "CONDITIONAL_ZERO_VECTOR_IF_PARENT_WITNESS_REAL", "adoption case routes to conditional zero vector")
    add("VAL4020_26_R11_case", "delta_gamma_R11" in result_lookup["CASE4020_2_R11_open"]["ppn_result"], "R11 open case routes to gamma/beta/q_loc")
    add("VAL4020_27_source_case", "delta_beta_source" in result_lookup["CASE4020_3_source_square_open"]["ppn_result"], "source square case routes to beta source")
    add("VAL4020_28_score_case", result_lookup["CASE4020_4_score_inputs_supplied"]["owner_status"] == "EXECUTABLE_SCORE_ROUTE_AVAILABLE_IN_PRINCIPLE", "score-input case defined")
    add("VAL4020_29_decision_next", any(row["decision_id"] == "DEC4020_4_next" and NEXT_DOC in row["decision"] for row in decisions), "next decision recorded")
    add("VAL4020_30_claims_false", all(str(row.get("allowed", "")).lower() == "false" for row in claims), "all claim gates disallowed")
    add("VAL4020_31_score_not_ready", all(str(row.get("score_ready", "")).lower() == "false" for row in score), "score rows remain not ready")
    output_tables = [
        sources,
        rollup,
        audit,
        score,
        results,
        decisions,
        claims,
        read_csv(OUTPUTS["next"]),
        read_csv(OUTPUTS["status"]),
    ]
    add("VAL4020_32_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4020_33_doc_exists", DOC_PATH.exists() and "adoption-or-score fork" in read_text(DOC_PATH), "document written with fork verdict")
    add("VAL4020_34_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4020_35_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4020_36_compile", compile_ok, "script compiles")
    add("VAL4020_37_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL4020_38_next_target", OUTPUTS["next"].exists() and NEXT_SCRIPT in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4020_39_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4020_40_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4020_41_derivation_first", any(row["decision_id"] == "DEC4020_1_best_next_move" and "parent adoption witness" in row["decision"] for row in decisions), "derivation-first next move recorded")
    add("VAL4020_42_no_numerical_G_claim", any(row["claim_id"] == "CLAIM4020_1_Newton" and not row["allowed"] for row in claims), "numerical G overclaim blocked")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    rollup = rollup_chain_rows(timestamp)
    audit = adoption_audit_rows(timestamp)
    score = score_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["rollup"], rollup)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["score"], score)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, rollup, audit, score, results, decisions, claims, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4020 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
