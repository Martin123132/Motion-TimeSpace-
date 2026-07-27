from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3378-Y5-R2FR-parent-action-minimal-line-or-source-bound-inputs-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3378_SOURCE_REGISTER.csv",
    "minimal_action_line": OUT / "P8_Y5_R2FR_3378_MINIMAL_PARENT_ACTION_LINE.csv",
    "variation_chain": OUT / "P8_Y5_R2FR_3378_PARENT_VARIATION_CHAIN.csv",
    "ownership_map": OUT / "P8_Y5_R2FR_3378_OBJECT_OWNERSHIP_MAP.csv",
    "signature_audit": OUT / "P8_Y5_R2FR_3378_PARENT_SIGNATURE_AUDIT.csv",
    "bound_inputs": OUT / "P8_Y5_R2FR_3378_SOURCE_BOUND_INPUT_ROWS_NONCLAIM.csv",
    "smuggling_tests": OUT / "P8_Y5_R2FR_3378_NO_SMUGGLING_TESTS.csv",
    "transfer_update": OUT / "P8_Y5_R2FR_3378_LOCAL_GR_TRANSFER_UPDATE_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3378_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3378_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3378_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3378_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3378_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3378_0_3377_doc", ROOT / "3377-Y5-R2FR-weak-field-source-normalization-or-Gref-kappa-bound-under-AX1090.md", "3377 calibrated source-coupling handoff"),
    ("SRC3378_1_3377_next", OUT / "P8_Y5_R2FR_3377_NEXT_TARGET.csv", "3377 selected minimal parent action line"),
    ("SRC3378_2_3377_theorem", OUT / "P8_Y5_R2FR_3377_WEAK_FIELD_SOURCE_NORMALIZATION_THEOREM.csv", "3377 source-normalization theorem"),
    ("SRC3378_3_3377_contract", OUT / "P8_Y5_R2FR_3377_COEFFICIENT_IDENTITY_CONTRACT.csv", "3377 coefficient identity contract"),
    ("SRC3378_4_action_normal_form", OUT / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv", "parent action normal form signature"),
    ("SRC3378_5_min_parent_matter", OUT / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv", "minimal parent matter contract"),
    ("SRC3378_6_theta_qtau_ledger", OUT / "P8_Y5_R2FR_2939_THETA_QTAU_SECTOR_CERTIFICATE_LEDGER.csv", "Theta/Q_tau sector certificate ledger"),
    ("SRC3378_7_theta_qtau_attempt", OUT / "P8_Y5_R2FR_2947_THETA_QTAU_CERTIFICATE_ATTEMPT.csv", "Theta/Q_tau certificate attempt"),
    ("SRC3378_8_parent_action_2464", OUT / "P8_Y5_PARENT_ACTION_2464_CANDIDATE_ACTIONS.csv", "minimal parent action candidates"),
    ("SRC3378_9_variation_2465", OUT / "P8_Y5_PARENT_ACTION_2465_VARIATION_AUDIT.csv", "vertical generator variation audit"),
    ("SRC3378_10_generator_2634", OUT / "P8_Y5_PARENT_ACTION_GENERATOR_2634_GENERATING_PRINCIPLE_ATTEMPT.csv", "parent generating principle attempt"),
    ("SRC3378_11_local_GR_blocks", OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv", "minimum local GR parent action blocks"),
    ("SRC3378_12_hilbert_worldtube_contract", OUT / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv", "Hilbert worldtube parent action contract"),
    ("SRC3378_13_worldtube_3375", OUT / "P8_Y5_R2FR_3375_WORLDTUBE_SOURCE_MEASURE_SELECTOR_THEOREM.csv", "3375 worldtube source selector"),
    ("SRC3378_14_boundary_3376", OUT / "P8_Y5_R2FR_3376_BOUNDARY_ZERO_FLUX_THEOREM_ATTEMPT.csv", "3376 boundary zero theorem"),
]


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        parse_ok = False
        parse_error = ""
        if exists:
            parse_ok, parse_error = parse_csv(path) if path.suffix.lower() == ".csv" else parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def minimal_action_line_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "PAL3378_0_minimal_line",
            "object": "single parent action candidate",
            "mathematical_form": "S_parent=int_M sqrt(-g_obs)[c^4/(16*pi*G0)(R[g_obs]-2Lambda0)+L_MTS_silent(Q,dQ;g_obs)+L_kappa(kappa,A3)+L_PiM(Pi_M,Q,J_H)+L_matter(psi,e_obs(qPhi),D_obs,A_obs,theta(qPhi))]+int_dM(B_GHY+B_ref+B_top)",
            "what_it_owns": "e_obs, kappa_MTS/G_ref, ell_J, Theta, Q_tau, B_ref, Pi_M, ordinary Hilbert source and residual-sector bookkeeping",
            "status": "CONSTRUCTED_MINIMAL_CANDIDATE_NOT_PARENT_DERIVED",
            "failure_if_missing": "3375-3377 remain closure contracts rather than a field-theoretic reduction",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PAL3378_1_observed_stack",
            "object": "public observed stack",
            "mathematical_form": "e_obs=e_obs(q(Phi)); tau=tau(q(Phi)); D_obs=D[e_obs,A_obs]; A_obs=A_obs(q(Phi)); theta=theta(q(Phi))",
            "what_it_owns": "matter frame, clocks, rods, source support, orbital readout and PPN gauge seed",
            "status": "CONDITIONAL_STACK_NOT_UNIQUE_FROM_MTS_CORE",
            "failure_if_missing": "two-frame source/readout ambiguity returns",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PAL3378_2_kappa_owner",
            "object": "universal gravitational coupling",
            "mathematical_form": "either kappa_MTS=8*pi*G0/c^4 as a fixed parent constant, or S_kappa=int kappa dA3 with d kappa=0 on connected local domains",
            "what_it_owns": "G_ref and no local source/radius/frame drift",
            "status": "ALLOWED_PARAMETER_OR_TOPOLOGICAL_CANDIDATE_NOT_ADOPTED",
            "failure_if_missing": "delta_kappa and epsilon_Gref_match remain",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PAL3378_3_matter_source_scale",
            "object": "ordinary matter/source current",
            "mathematical_form": "S_matter=sum_A int mu_obs L_A(psi_A,D_obs psi_A,e_obs,A_obs,theta), with no source-only prefactor w_A(X) and ell_J fixed before variation",
            "what_it_owns": "J_H[tau], W_source and ell_J",
            "status": "MINIMAL_MATTER_CONTRACT_NOT_UNIQUE_PARENT_THEOREM",
            "failure_if_missing": "delta_ellJ, WEP/source prefactor and source-mask residuals remain",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PAL3378_4_theta_qtau",
            "object": "Noether current and Hamiltonian charge",
            "mathematical_form": "delta L_parent=sum_s E_s delta Phi_s+dTheta_total; J_tau=Theta_total(L_tau Phi)-i_tau L_parent=dQ_tau^MTS+C_tau",
            "what_it_owns": "Theta, Q_tau, H_tau and source-transfer charge",
            "status": "FORMAL_VARIATION_SCHEMA_SECTOR_CERTIFICATES_MISSING",
            "failure_if_missing": "H_tau/M_H_ref and source measure stay unowned",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PAL3378_5_PiM_owner",
            "object": "mass projector",
            "mathematical_form": "Pi_M^2=Pi_M, [d,Pi_M]J_H=0, delta Pi_M stress=0 or bounded, with Pi_M fixed by the parent algebra before readout",
            "what_it_owns": "topological-Hilbert same-object map and no post-fit mass selector",
            "status": "CHAINMAP_CONDITIONAL_PARENT_ORIGIN_MISSING",
            "failure_if_missing": "I_commutator, R_eq and wrong-object guards remain",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PAL3378_6_boundary_reference",
            "object": "finite charge and reference",
            "mathematical_form": "B_ref is fixed before readout; delta B_ref supplies only source-blind exact/topological terms, with B_zero_flux=Delta_symp=0 or bounded",
            "what_it_owns": "H_ref, M_H_ref and boundary/reference residuals",
            "status": "BOUNDARY_ZERO_CONDITIONAL_REFERENCE_UNSIGNED",
            "failure_if_missing": "boundary bookkeeping can absorb source coupling",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PAL3378_7_verdict",
            "object": "minimal parent action status",
            "mathematical_form": "PAL3378_0 through PAL3378_6 would parent-sign 3375, 3376 and 3377 only if adopted as the unique MTS parent action grammar with all sector certificates",
            "what_it_owns": "local-GR/Newton/Maxwell-source route as a field-theory branch",
            "status": "CANDIDATE_LINE_READY_NOT_CURRENT_MTS_CLAIM",
            "failure_if_missing": "calibrated source coupling remains closure-only/nonclaim",
            "valid_for_claim": "false",
        },
    ]


def variation_chain_rows() -> list[dict[str, str]]:
    return [
        {"step_id": "VAR3378_0_variation", "statement": "The parent action must vary before readout: delta S_parent=int(E_g delta g+E_Q delta Q+E_psi delta psi+...)+int_dM Theta_total.", "derived_if": "one explicit L_parent contains all retained sectors", "current_status": "SCHEMA_VALID_ACTION_MISSING", "valid_for_claim": "false"},
        {"step_id": "VAR3378_1_field_equations", "statement": "E_g=0 gives EH plus named residual operators; E_psi=0 gives ordinary matter equations; E_Q=0 gives extra-sector equations or silence conditions.", "derived_if": "sector Lagrangians and residual classifications are supplied", "current_status": "PARTIAL_CONTRACT", "valid_for_claim": "false"},
        {"step_id": "VAR3378_2_Noether", "statement": "Diffeomorphism covariance gives J_tau=Theta_total(L_tau Phi)-i_tau L_parent=dQ_tau^MTS+C_tau.", "derived_if": "Theta_s and Q_tau_s exist for EH, matter, extra, PiM and boundary sectors", "current_status": "FORMAL_NOETHER_SCHEMA_SECTOR_CERTS_FAIL", "valid_for_claim": "false"},
        {"step_id": "VAR3378_3_Hamiltonian", "statement": "delta H_tau=int_S(delta Q_tau^MTS-i_tau Theta_total)-delta H_ref must be integrable and source-blind in the reference.", "derived_if": "omega_total curl, H_ref lock and surface/tau lock vanish", "current_status": "INTEGRABILITY_REFERENCE_OPEN", "valid_for_claim": "false"},
        {"step_id": "VAR3378_4_source", "statement": "J_H[tau] is the Hilbert source current from the same S_matter and W_source=closure(supp J_H[tau]) before readout.", "derived_if": "matter descends only through e_obs(qPhi) and no source prefactor exists", "current_status": "CONDITIONAL_FROM_3375_NOT_PARENT_UNIQUE", "valid_for_claim": "false"},
        {"step_id": "VAR3378_5_weak_field", "statement": "The EH coefficient and Hilbert source produce nabla^2 Phi_N=4*pi*G_ref rho_H in the same frame.", "derived_if": "kappa/G_ref, e_obs, J_H and weak-field gauge are all parent-signed", "current_status": "CONDITIONAL_FROM_3377", "valid_for_claim": "false"},
        {"step_id": "VAR3378_6_total_verdict", "statement": "A single parent variation would close the ladder only if no extra hidden source, boundary, projector or coefficient slot remains outside it.", "derived_if": "no-extension/no-smuggling theorem passes", "current_status": "ADOPTION_AND_UNIQUENESS_NOT_DERIVED", "valid_for_claim": "false"},
    ]


def ownership_map_rows() -> list[dict[str, str]]:
    return [
        {"object_id": "OWN3378_0_e_obs", "object": "e_obs/q(Phi)", "owner_clause": "PAL3378_1", "required_for": "matter frame, clocks, rods, W_source, PPN gauge", "current_status": "CONDITIONAL_STACK_NOT_UNIQUE", "residual_if_unsigned": "R_frame_source_split", "valid_for_claim": "false"},
        {"object_id": "OWN3378_1_Theta", "object": "Theta_total", "owner_clause": "PAL3378_4", "required_for": "Noether current and H_tau", "current_status": "SECTOR_CERTIFICATES_MISSING", "residual_if_unsigned": "epsilon_theta", "valid_for_claim": "false"},
        {"object_id": "OWN3378_2_Qtau", "object": "Q_tau^MTS", "owner_clause": "PAL3378_4", "required_for": "Hamiltonian mass and source-transfer chain", "current_status": "SECTOR_CHARGE_CLOSURE_MISSING", "residual_if_unsigned": "epsilon_Qtau", "valid_for_claim": "false"},
        {"object_id": "OWN3378_3_Bref", "object": "B_ref/H_ref", "owner_clause": "PAL3378_6", "required_for": "finite mass and boundary zero", "current_status": "REFERENCE_LOCK_UNSIGNED", "residual_if_unsigned": "Delta_symp;B_zero_flux", "valid_for_claim": "false"},
        {"object_id": "OWN3378_4_PiM", "object": "Pi_M", "owner_clause": "PAL3378_5", "required_for": "mass projection and topological-Hilbert same-object theorem", "current_status": "PARENT_ORIGIN_MISSING", "residual_if_unsigned": "I_commutator;R_eq_integral", "valid_for_claim": "false"},
        {"object_id": "OWN3378_5_kappa", "object": "kappa_MTS/G_ref", "owner_clause": "PAL3378_2", "required_for": "Poisson/Newton/PPN normalization", "current_status": "PARAMETER_ALLOWED_NOT_ADOPTED", "residual_if_unsigned": "delta_kappa;epsilon_Gref_match", "valid_for_claim": "false"},
        {"object_id": "OWN3378_6_ellJ", "object": "ell_J/source-current scale", "owner_clause": "PAL3378_3", "required_for": "Hilbert source and WEP/Newton source normalization", "current_status": "SOURCE_SCALE_OPEN", "residual_if_unsigned": "delta_ellJ;epsilon_M", "valid_for_claim": "false"},
        {"object_id": "OWN3378_7_extra_sectors", "object": "motion/time/domain/memory/range extra sectors", "owner_clause": "PAL3378_0;PAL3378_5", "required_for": "local GR residual silence", "current_status": "STRESS_CHARGE_SILENCE_OPEN", "residual_if_unsigned": "epsilon_extra_stress;PPN_vector", "valid_for_claim": "false"},
    ]


def signature_audit_rows() -> list[dict[str, str]]:
    return [
        {"audit_id": "SIG3378_0_complete_field_inventory", "required_signature": "closed field list before variation", "evidence": "2634 keeps closed parent domain/universal property unsigned", "current_status": "MISSING", "blocks": "PAL3378_0", "valid_for_claim": "false"},
        {"audit_id": "SIG3378_1_unique_action_grammar", "required_signature": "no additional natural source-only or marker-prefactor functor", "evidence": "2634 and 2587 state no-prefactor/no-extra-slot contracts but not a uniqueness theorem", "current_status": "MISSING_NO_EXTENSION_THEOREM", "blocks": "PAL3378_3", "valid_for_claim": "false"},
        {"audit_id": "SIG3378_2_sector_lagrangians", "required_signature": "L_MTS_silent and every extra sector has Helmholtz-compatible action and variation", "evidence": "2939 flags GK, domain, PiM, memory and boundary sector certificates as failing", "current_status": "SECTOR_CERTS_FAIL", "blocks": "PAL3378_4", "valid_for_claim": "false"},
        {"audit_id": "SIG3378_3_theta_qtau", "required_signature": "Theta_total and Q_tau^MTS extracted for all retained sectors", "evidence": "2947 gives exact formula but certificate_not_derived", "current_status": "MISSING", "blocks": "VAR3378_2;VAR3378_3", "valid_for_claim": "false"},
        {"audit_id": "SIG3378_4_PiM_parent", "required_signature": "Pi_M is action-owned and not a post-fit mass selector", "evidence": "3373/3374 chainmap and same-object lemmas remain conditional", "current_status": "MISSING_PARENT_ORIGIN", "blocks": "PAL3378_5", "valid_for_claim": "false"},
        {"audit_id": "SIG3378_5_boundary_reference", "required_signature": "B_ref/H_ref fixed source-blind before readout", "evidence": "3376 boundary theorem is conditional and reference lock unsigned", "current_status": "UNSIGNED", "blocks": "PAL3378_6", "valid_for_claim": "false"},
        {"audit_id": "SIG3378_6_coefficient_owner", "required_signature": "kappa/G_ref and ell_J fixed by parent action before readout", "evidence": "3377 coefficient identity theorem is conditional, not signed", "current_status": "UNSIGNED", "blocks": "PAL3378_2;PAL3378_3", "valid_for_claim": "false"},
    ]


def bound_input_rows() -> list[dict[str, str]]:
    return [
        {"row_id": "PAB3378_0_R_parent_action_missing", "symbol": "R_parent_action_missing", "definition": "indicator/envelope for local-GR route relying on candidate action line rather than signed parent action", "bound_formula": "1 until all PAL3378 clauses are parent-signed; 0 if unique parent action theorem passes", "required_inputs": "complete field inventory, action grammar proof, sector variations", "current_status": "NONCLAIM_CLOSURE_GUARD", "valid_for_claim": "false"},
        {"row_id": "PAB3378_1_epsilon_theta_Qtau", "symbol": "epsilon_theta_Qtau", "definition": "missing or unmatched Theta/Q_tau sector contribution", "bound_formula": "sum_s ||Theta_s,Q_tau_s,C_tau_s missing or nonclosed||/|M_H_ref|", "required_inputs": "sector charge certificates, units, M_H_ref", "current_status": "SECTOR_CERTIFICATES_MISSING", "valid_for_claim": "false"},
        {"row_id": "PAB3378_2_epsilon_PiM_parent", "symbol": "epsilon_PiM_parent", "definition": "mass projector not derived from parent action/algebra", "bound_formula": "|I_commutator|/|M_H_ref| + |R_eq_integral|/|M_H_ref| + projector stress norm", "required_inputs": "I_commutator,R_eq_integral,projector stress,M_H_ref", "current_status": "FORMULA_READY_NUMERIC_MISSING", "valid_for_claim": "false"},
        {"row_id": "PAB3378_3_epsilon_extra_stress", "symbol": "epsilon_extra_stress", "definition": "extra MTS-sector stress/charge entering local weak-field or PPN equations", "bound_formula": "||T_extra+E_extra||/||T_H|| in declared local weak-field norm", "required_inputs": "extra-sector action, stress tensor, weak-field norm, source path", "current_status": "SOURCE_READY_SCHEMA_NONCLAIM", "valid_for_claim": "false"},
        {"row_id": "PAB3378_4_epsilon_Bref", "symbol": "epsilon_Bref", "definition": "source-dependent boundary/reference absorption left outside signed action", "bound_formula": "(|B_zero_flux|+|Delta_symp|+|D_source H_ref|)/|M_H_ref|", "required_inputs": "B_zero_flux,Delta_symp,H_ref derivative,M_H_ref", "current_status": "BOUNDARY_REFERENCE_NONCLAIM", "valid_for_claim": "false"},
        {"row_id": "PAB3378_5_delta_kappa_ellJ", "symbol": "delta_kappa_ellJ", "definition": "combined parent coefficient/source-scale ownership residual", "bound_formula": "|delta_kappa|+|delta_ellJ|+|epsilon_Gref_match|", "required_inputs": "kappa,G_ref,ell_J,N_G,H_tau,Poisson coefficient", "current_status": "COEFFICIENT_OWNER_NONCLAIM", "valid_for_claim": "false"},
        {"row_id": "PAB3378_6_epsilon_action_smuggling", "symbol": "epsilon_action_smuggling", "definition": "any source/readout/domain/projector coefficient introduced after variation", "bound_formula": "1 for any post-variation source slot; 0 only if no-smuggling tests all pass", "required_inputs": "action inventory and readout-order audit", "current_status": "GUARD_ACTIVE", "valid_for_claim": "false"},
    ]


def smuggling_test_rows() -> list[dict[str, str]]:
    return [
        {"test_id": "SMUG3378_0_no_source_prefactor", "forbidden_move": "w_A(X) or c_A(X) species/source prefactor in ordinary matter after variation", "why_forbidden": "turns ell_J/source mass into a hidden WEP/Newton fit knob", "current_result": "CONTRACT_EXISTS_UNIQUENESS_NOT_PROVED", "residual": "delta_ellJ;epsilon_action_smuggling", "valid_for_claim": "false"},
        {"test_id": "SMUG3378_1_no_second_metric", "forbidden_move": "source uses e_source while clocks/orbits use e_obs", "why_forbidden": "separates Hilbert mass from observed local acceleration", "current_result": "SINGLE_STACK_CANDIDATE_NOT_UNIQUE", "residual": "R_frame_source_split", "valid_for_claim": "false"},
        {"test_id": "SMUG3378_2_no_multiplier_closure", "forbidden_move": "lambda enforces q_loc=0 or GR source law directly without symmetry origin", "why_forbidden": "smuggles local GR as a constraint instead of deriving it", "current_result": "REJECT_AS_CLAIM_ALLOW_AS_DEMOTED_CLOSURE_ONLY", "residual": "R_parent_action_missing", "valid_for_claim": "false"},
        {"test_id": "SMUG3378_3_no_boundary_cancellation", "forbidden_move": "choose B_ref/H_ref after readout to cancel local residuals", "why_forbidden": "boundary bookkeeping can mimic measured GM", "current_result": "BLOCKED_BY_3376_GUARD", "residual": "epsilon_Bref", "valid_for_claim": "false"},
        {"test_id": "SMUG3378_4_no_PiM_tuning", "forbidden_move": "choose Pi_M after seeing source-transfer or PPN residuals", "why_forbidden": "projector becomes a fitted mass selector", "current_result": "CHAINMAP_CONDITIONAL_PARENT_ORIGIN_MISSING", "residual": "epsilon_PiM_parent", "valid_for_claim": "false"},
        {"test_id": "SMUG3378_5_no_G_backfill", "forbidden_move": "define G_ref/N_G/M_H_ref from measured orbital GM before proof", "why_forbidden": "circular Newton recovery", "current_result": "BLOCKED_BY_3377_GUARD", "residual": "delta_kappa_ellJ", "valid_for_claim": "false"},
    ]


def transfer_update_rows() -> list[dict[str, str]]:
    return [
        {"update_id": "UPD3378_0_if_parent_line_signed", "condition": "PAL3378_0..6 parent-signed as unique grammar", "local_GR_effect": "3375 source selector, 3376 boundary zero and 3377 source normalization can promote to one parent-action chain", "remaining_blockers": "full second-order PPN vector and empirical bound rows", "current_status": "CONDITIONAL_BRANCH_NOT_CURRENT_CLAIM", "valid_for_claim": "false"},
        {"update_id": "UPD3378_1_current_branch", "condition": "current MTS corpus", "local_GR_effect": "minimal action line is a disciplined ansatz/contract, not a proof of local GR", "remaining_blockers": "field inventory, uniqueness/no-extension, sector variations, Theta/Q_tau, PiM, boundary and coefficients", "current_status": "CLOSURE_GUARD_RETAINED", "valid_for_claim": "false"},
        {"update_id": "UPD3378_2_practical_gain", "condition": "3378 accepted as internal action contract", "local_GR_effect": "future derivations must point to a parent action clause or create a residual row; no loose target-writing allowed", "remaining_blockers": "parent adoption theorem", "current_status": "DISCIPLINE_INCREASED", "valid_for_claim": "false"},
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {"run_id": "RUN3378_0_action_line", "test": "construct one minimal parent action line covering 3375-3377 objects", "result": "PASS_CANDIDATE_CONTRACT", "detail": "single line owns e_obs, kappa, ell_J, Theta/Q_tau, B_ref, Pi_M and source current conditionally", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3378_1_variation_schema", "test": "derive Theta/Q_tau/H_tau form from candidate action", "result": "PASS_FORMAL_SCHEMA", "detail": "covariant variation gives formal Noether current if all sector Lagrangians exist", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3378_2_current_parent_signature", "test": "promote candidate line as current MTS parent action", "result": "BLOCKED_NOT_PARENT_SIGNED", "detail": "complete field inventory, uniqueness/no-extension, sector variations and charge certificates are missing", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3378_3_closure_smuggling", "test": "use multiplier/reference/readout choices to close local GR directly", "result": "REFUSED_AS_CLAIM", "detail": "allowed only as closure-only or bounded residual route, not as derivation", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3378_4_local_GR", "test": "claim local GR/Newton/PPN from 3378", "result": "REFUSED", "detail": "3378 supplies a parent-action contract; it does not sign the parent action or PPN vector", "claim_allowed": "false", "valid_for_claim": "false"},
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {"gate_id": "GATE3378_0_sources", "claim": "all required 3378 source paths exist and parse", "gate_pass": bool_text(source_ok), "reason": "source register validates local inputs", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3378_1_minimal_line", "claim": "minimal action line is written", "gate_pass": "true", "reason": "PAL3378_0 defines the candidate line and ownership clauses", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3378_2_parent_signed", "claim": "minimal action line is parent-derived from MTS core", "gate_pass": "false", "reason": "field inventory, uniqueness/no-extension and sector Lagrangians are missing", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3378_3_theta_qtau", "claim": "Theta/Q_tau/H_tau are claim-grade", "gate_pass": "false", "reason": "sector certificates and integrability remain unsigned", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3378_4_no_smuggling", "claim": "all no-smuggling tests are parent-proven", "gate_pass": "false", "reason": "tests are explicit but uniqueness/adoption proof is missing", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3378_5_local_GR", "claim": "local GR/Newton/PPN route is established", "gate_pass": "false", "reason": "3378 is a candidate action contract, not a signed parent theorem", "claim_allowed": "false", "valid_for_claim": "false"},
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {"decision_id": "DEC3378_0_progress", "decision": "The minimal parent action line is now explicit.", "because": "3375-3377 objects are placed in one candidate variation rather than separate closure clauses.", "next_action": "try to prove this action line is the unique/admissible MTS parent grammar", "valid_for_claim": "false"},
        {"decision_id": "DEC3378_1_current_status", "decision": "This is not yet a local-GR proof.", "because": "a candidate line without parent adoption, sector variations and charge certificates is still an ansatz.", "next_action": "retain R_parent_action_missing and source-bound rows", "valid_for_claim": "false"},
        {"decision_id": "DEC3378_2_best_next", "decision": "The next attack should be no-extension/adoption, not another residual rollup.", "because": "if no extra source-only or marker-prefactor action is allowed, the matter/source side becomes much more rigid.", "next_action": "prove or bound the no-source-prefactor/no-extension theorem for the parent action grammar", "valid_for_claim": "false"},
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {"target_id": "3379-Y5-R2FR-parent-action-adoption-no-extension-or-source-prefactor-bound-under-AX1090.md", "target_script": "scripts/Y5_R2FR_3379_parent_action_adoption_no_extension_or_source_prefactor_bound.py", "objective": "prove the minimal parent action grammar forbids source-only prefactors, second source metrics, post-variation projectors and hidden marker functors, or stage source-prefactor bound rows", "why_next": "3378 wrote the candidate action line; the missing claim step is adoption/uniqueness from MTS core rather than another conditional residual map", "valid_for_claim": "false"},
        {"target_id": "3380-Y5-R2FR-full-PPN-vector-after-parent-action-line-or-bound-pack-under-AX1090.md", "target_script": "scripts/Y5_R2FR_3380_full_PPN_vector_after_parent_action_line_or_bound_pack.py", "objective": "after adoption/no-extension, bind gamma, beta, alpha_i, zeta_i and xi from the same parent source convention", "why_next": "the PPN vector is the next empirical local-GR gate once the parent action grammar is no longer closure-only", "valid_for_claim": "false"},
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = list(FW.rglob("*3378*")) if FW.exists() else []
    clause_ids = {row["clause_id"] for row in rows_by_name["minimal_action_line"]}
    variation_ids = {row["step_id"] for row in rows_by_name["variation_chain"]}
    owner_ids = {row["object_id"] for row in rows_by_name["ownership_map"]}
    audit_ids = {row["audit_id"] for row in rows_by_name["signature_audit"]}
    bound_symbols = {row["symbol"] for row in rows_by_name["bound_inputs"]}
    smuggling_ids = {row["test_id"] for row in rows_by_name["smuggling_tests"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3378_0_sources_exist_parse", "all cited local source paths exist and parse", source_ok, ""),
        ("VAL3378_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3378_2_minimal_action_line", "minimal action line covers action, observed stack, kappa, matter, theta/qtau, PiM, boundary and verdict", {"PAL3378_0_minimal_line", "PAL3378_1_observed_stack", "PAL3378_2_kappa_owner", "PAL3378_3_matter_source_scale", "PAL3378_4_theta_qtau", "PAL3378_5_PiM_owner", "PAL3378_6_boundary_reference", "PAL3378_7_verdict"}.issubset(clause_ids), ""),
        ("VAL3378_3_variation_chain", "variation chain covers variation, equations, Noether, Hamiltonian, source, weak-field and verdict", {"VAR3378_0_variation", "VAR3378_1_field_equations", "VAR3378_2_Noether", "VAR3378_3_Hamiltonian", "VAR3378_4_source", "VAR3378_5_weak_field", "VAR3378_6_total_verdict"}.issubset(variation_ids), ""),
        ("VAL3378_4_ownership_map", "ownership map covers e_obs, Theta, Q_tau, B_ref, PiM, kappa, ellJ and extra sectors", {"OWN3378_0_e_obs", "OWN3378_1_Theta", "OWN3378_2_Qtau", "OWN3378_3_Bref", "OWN3378_4_PiM", "OWN3378_5_kappa", "OWN3378_6_ellJ", "OWN3378_7_extra_sectors"}.issubset(owner_ids), ""),
        ("VAL3378_5_signature_audit", "signature audit covers inventory, uniqueness, sectors, theta/qtau, PiM, boundary and coefficients", {"SIG3378_0_complete_field_inventory", "SIG3378_1_unique_action_grammar", "SIG3378_2_sector_lagrangians", "SIG3378_3_theta_qtau", "SIG3378_4_PiM_parent", "SIG3378_5_boundary_reference", "SIG3378_6_coefficient_owner"}.issubset(audit_ids), ""),
        ("VAL3378_6_bound_inputs", "bound rows cover parent action, theta/qtau, PiM, extra stress, boundary, coefficients and smuggling", {"R_parent_action_missing", "epsilon_theta_Qtau", "epsilon_PiM_parent", "epsilon_extra_stress", "epsilon_Bref", "delta_kappa_ellJ", "epsilon_action_smuggling"}.issubset(bound_symbols), ""),
        ("VAL3378_7_smuggling_tests", "smuggling tests cover source prefactor, second metric, multiplier closure, boundary cancellation, PiM tuning and G backfill", {"SMUG3378_0_no_source_prefactor", "SMUG3378_1_no_second_metric", "SMUG3378_2_no_multiplier_closure", "SMUG3378_3_no_boundary_cancellation", "SMUG3378_4_no_PiM_tuning", "SMUG3378_5_no_G_backfill"}.issubset(smuggling_ids), ""),
        ("VAL3378_8_runner_blocks_claim", "runner builds candidate but blocks current local-GR claim", "PASS_CANDIDATE_CONTRACT" in runner_results and "PASS_FORMAL_SCHEMA" in runner_results and "BLOCKED_NOT_PARENT_SIGNED" in runner_results and "REFUSED_AS_CLAIM" in runner_results and "REFUSED" in runner_results, ""),
        ("VAL3378_9_gates_block_local", "promotion gates write line but block parent signature and local GR", gate_map.get("GATE3378_1_minimal_line") == "true" and gate_map.get("GATE3378_2_parent_signed") == "false" and gate_map.get("GATE3378_5_local_GR") == "false", ""),
        ("VAL3378_10_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3378_11_next_target", "next target moves to parent-action adoption/no-extension", rows_by_name["next"][0]["target_id"].startswith("3379-Y5-R2FR-parent-action-adoption"), ""),
        ("VAL3378_12_write_scope_outside_formalization", "no 3378 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    checks.append(("VAL3378_13_overall", "3378 validation overall", all(passed for _, _, passed, _ in checks), "all required checks passed" if all(passed for _, _, passed, _ in checks) else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3378 - Y5/R2FR parent action minimal line or source-bound inputs under AX1090",
        "",
        "## Summary",
        "- 3378 writes the minimal parent action line demanded by 3375-3377: one action must own `e_obs`, `Theta`, `Q_tau`, `B_ref`, `Pi_M`, `kappa_MTS`, `ell_J`, and the ordinary Hilbert source before readout.",
        "- Constructive result: a coherent candidate line exists: EH core plus fixed/topological `kappa`, universal matter through `e_obs(qPhi)`, parent-owned `Pi_M`, silent/bounded extra MTS sectors, and fixed boundary/reference terms.",
        "- Derivation result: if that action is truly adopted, covariance gives `Theta_total`, `J_tau=dQ_tau+C_tau`, Hamiltonian charge, Hilbert source current, Poisson/Newton normalization, and the local-GR source chain from one object.",
        "- Current verdict: this is not yet a parent-signed MTS action. The missing step is adoption/uniqueness: complete field inventory, no source-prefactor/no-extension theorem, sector variations, `Theta/Q_tau` certificates, `Pi_M` origin, boundary lock, and coefficient ownership.",
        "- Fallback result: `R_parent_action_missing`, `epsilon_theta_Qtau`, `epsilon_PiM_parent`, `epsilon_extra_stress`, `epsilon_Bref`, `delta_kappa_ellJ`, and `epsilon_action_smuggling` are explicit nonclaim rows.",
        "- Best next strike is not another residual rollup: prove or bound the parent-action adoption/no-extension theorem so source-only prefactors, second metrics, post-variation projectors, and hidden marker functors are forbidden by the grammar.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Minimal Parent Action Line",
        md_table(rows_by_name["minimal_action_line"]),
        "## Parent Variation Chain",
        md_table(rows_by_name["variation_chain"]),
        "## Object Ownership Map",
        md_table(rows_by_name["ownership_map"]),
        "## Parent Signature Audit",
        md_table(rows_by_name["signature_audit"]),
        "## Source-bound Input Rows",
        md_table(rows_by_name["bound_inputs"]),
        "## No-smuggling Tests",
        md_table(rows_by_name["smuggling_tests"]),
        "## Local-GR Transfer Update",
        md_table(rows_by_name["transfer_update"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_register = source_rows()
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_register)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "minimal_action_line": minimal_action_line_rows(),
        "variation_chain": variation_chain_rows(),
        "ownership_map": ownership_map_rows(),
        "signature_audit": signature_audit_rows(),
        "bound_inputs": bound_input_rows(),
        "smuggling_tests": smuggling_test_rows(),
        "transfer_update": transfer_update_rows(),
        "runner": runner_rows(),
        "gates": gate_rows(source_ok),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()
