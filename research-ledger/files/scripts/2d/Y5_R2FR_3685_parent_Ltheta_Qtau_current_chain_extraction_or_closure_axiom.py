from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3685"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_LTHETA_QTAU_CURRENT_CHAIN_EXTRACTION_OR_CLOSURE_AXIOM_3685"
DOC = ROOT / "3685-Y5-R2FR-parent-Ltheta-Qtau-current-chain-extraction-or-closure-axiom.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        return True, len(load_csv(path))
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3684", RESIDUALS / "P8_Y5_R2FR_3684_NEXT_TARGET.csv", "theta_MTS", "3684 selected parent L/theta/Q extraction"),
        ("rq_parent_3684", RESIDUALS / "P8_Y5_R2FR_3684_RQTAU_COMPONENT_ROWS.csv", "R_parent_LthetaQ", "3684 isolated parent action extraction residual"),
        ("noether_2939", RESIDUALS / "P8_Y5_R2FR_2939_PARENT_NOETHER_EXTRACTION_ATTEMPT.csv", "PNE2939_0_master_formula", "exact conditional Noether formula"),
        ("ctau_2939", RESIDUALS / "P8_Y5_R2FR_2939_CTAU_RESIDUAL_DECOMPOSITION.csv", "CTA2939_0_master", "C_tau total residual decomposition"),
        ("axiom_2939", RESIDUALS / "P8_Y5_R2FR_2939_SOURCE_MEASURE_CLOSURE_AXIOM.csv", "AX2939_0_parent_Noether", "older closure-only parent Noether axiom"),
        ("synthesis_2940", RESIDUALS / "P8_Y5_R2FR_2940_MINIMAL_PARENT_ACTION_SYNTHESIS_ATTEMPT.csv", "SYN2940_0_total_spine", "finite minimal parent current-chain spine"),
        ("matrix_2940", RESIDUALS / "P8_Y5_R2FR_2940_SECTOR_CERTIFICATE_MATRIX.csv", "SEC2940_9_total", "sector certificate matrix refuses total adoption"),
        ("audit_3006", RESIDUALS / "P8_Y5_R2FR_3006_PARENT_CURRENT_CHAIN_AUDIT.csv", "CCA3006_9_verdict", "current-chain audit keeps theta/Q/H_tau owner unpromoted"),
        ("grammar_3007", RESIDUALS / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv", "G3007_10_verdict", "selected minimal parent-action grammar"),
        ("lc_branch_3566", RESIDUALS / "P8_Y5_R2FR_3566_PARENT_LOCAL_LC_ACTION_SIGNATURE.csv", "SIG3566_10_total_signature", "local LC branch signature is private nonclaim"),
        ("action_clause_3630", RESIDUALS / "P8_Y5_R2FR_3630_PARENT_ACTION_CLAUSE.csv", "PAC3630_1_total_action", "single admissible parent action clause written but unsigned"),
        ("response_3540", RESIDUALS / "P8_Y5_R2FR_3540_PARENT_RESPONSE_ACTION.csv", "PAC3540_3_Euler_operator", "Gamma/Khat/q_loc response action route"),
        ("gk_contract", RESIDUALS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv", "GK513_0_action_existence", "GK/q_loc first-variation contract"),
        ("current_chain_2948", RESIDUALS / "P8_Y5_R2FR_2948_PARENT_CURRENT_CHAIN_CERTIFICATE_ATTEMPT.csv", "PCC2948_6_verdict", "non-EH current-chain sector action certificate not derived"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "relevance": relevance,
            }
        )
    return rows


def extraction_audit_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "LQ3685_0_target",
            "extract parent theta_MTS, Q_tau^MTS and C_tau",
            "delta L_parent = E_I delta Phi^I + d theta_MTS; J_tau = theta_MTS(L_tau Phi)-i_tau L_parent = dQ_tau^MTS + C_tau",
            "TARGET_NOT_PROVED",
            "this is the exact current-chain extraction target",
            False,
        ),
        (
            "LQ3685_1_exact_noether_formula",
            "conditional Noether formula is exact",
            "For any finite-order diffeomorphism-invariant L_parent with fixed tau action and boundary class, theta_MTS, Q_tau^MTS and C_tau are extracted by the covariant phase-space identity.",
            "EXACT_CONDITIONAL_FORMULA",
            "the algebra is not the gap; parent sector ownership is the gap",
            True,
        ),
        (
            "LQ3685_2_trial_spine_written",
            "finite trial parent action spine is available",
            "S_parent^trial = S_EH + S_matter+EM + S_kappa_top + S_GK + S_selector/PiM/worldtube + S_boundary_ref + S_silent_aux.",
            "TRIAL_SPINE_WRITTEN_NOT_ADOPTED",
            "a concrete object exists for derivation attempts, but it is not yet a derived MTS parent action",
            False,
        ),
        (
            "LQ3685_3_partial_LC_branch",
            "local LC branch signature gives a private action route",
            "S_loc^LC = S_EH + S_m + S_EM + S_extra + S_boundary + S_source_norm with readouts post-variation and no independent Gamma_ind in the ordinary/source sectors.",
            "PRIVATE_BRANCH_SIGNATURE_NONCLAIM",
            "useful for local-GR derivation, not a public parent derivation",
            False,
        ),
        (
            "LQ3685_4_sector_failure",
            "current MTS owns every sector variation",
            "All retained sectors must supply field list, first variation, theta_i, Q_tau_i/C_tau_i, stress/source term, boundary rule and source path.",
            "SECTOR_CERTIFICATES_FAIL",
            "GK/q_loc action existence, PiM/worldtube glue, fixed reference, tau lock and extra-sector silence remain live",
            False,
        ),
        (
            "LQ3685_5_closure_axiom",
            "closure-only axiom can be stated exactly",
            "AX_LQ: There exists a finite-order diffeomorphism-invariant S_parent^trial whose sector variations are complete and whose observed-time Noether current yields theta_MTS, Q_tau^MTS and C_tau.",
            "CLOSURE_AXIOM_WRITTEN_NOT_ADOPTED",
            "allowed only for private algebraic exploration; no Newton/local-GR claim can use it",
            False,
        ),
        (
            "LQ3685_6_verdict",
            "current corpus derives R_parent_LthetaQ=0",
            "R_parent_LthetaQ is zero only if LQ3685_2 is adopted and all sector certificates pass; they do not.",
            "R_PARENT_LTHETAQ_ZERO_NOT_DERIVED_ACTION_SPINE_AND_AXIOM_STAGED",
            "move next to the first failed hard sector: GK/q_loc action existence and first variation",
            False,
        ),
    ]
    return [
        {
            **base(ts),
            "audit_id": audit_id,
            "claim": claim,
            "mathematical_statement": mathematical_statement,
            "status": status,
            "consequence": consequence,
            "formal_identity_passed": formal_identity_passed,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for audit_id, claim, mathematical_statement, status, consequence, formal_identity_passed in specs
    ]


def action_spine_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "SPN3685_0_EH_core",
            "S_EH[g_obs;kappa0,Lambda0]",
            "g_obs,e_obs,tau",
            "delta S_EH = E_EH delta g + d theta_EH; Q_tau^EH exists as GR reference",
            "REFERENCE_ANCHOR_ONLY",
            "Q_tau^EH cannot be the total MTS charge until MTS-to-EH reduction and silent sectors are signed",
        ),
        (
            "SPN3685_1_matter_EM",
            "S_matter[psi,e_obs(q)] + S_EM[A_Q,e_obs(q)]",
            "psi,A_Q,e_obs,q,theta_A,tau",
            "Hilbert stress and ordinary/EM source current come from the same observed action before readout",
            "CONDITIONAL_STANDARD_FORM_UNSIGNED",
            "matter descent, no source-only prefactor and EM normalization owner remain unsigned",
        ),
        (
            "SPN3685_2_kappa_top",
            "S_kappa_top[kappa_eff,A3]",
            "kappa_eff,A3",
            "delta_A3 S -> d kappa_eff=0 if the topological sector is adopted",
            "CANDIDATE_NOT_ADOPTED",
            "constant G/kappa cannot be claimed yet",
        ),
        (
            "SPN3685_3_GK_q_loc",
            "S_GK[A_mu,Gamma_eff,K_hat,Phi,J_M]",
            "Phi,A_mu,Gamma_eff,K_hat,P_loc,J_M",
            "desired first variation gives P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu} - J_M^nu)=0 plus theta_GK,Q_tau^GK,C_tau^GK",
            "PRIMARY_HARDEST_BLOCKER",
            "action existence, Helmholtz integrability, Euler closure, double-zero and boundary no-flux are not proved",
        ),
        (
            "SPN3685_4_selector_PiM_worldtube",
            "S_selector/PiM/worldtube",
            "P_loc,Pi_M,J_H,W,Q_M,H_tau,H_ref",
            "source support, mass projector and worldtube source measure are parent-owned before readout",
            "PARALLEL_CORE_BLOCKER",
            "Pi_M/worldtube/H_tau source glue remains unsigned",
        ),
        (
            "SPN3685_5_boundary_reference",
            "S_boundary_ref = GHY + B_ref + exact/corner terms",
            "B_ref,H_ref,tau,S_inner,S_outer,corner class",
            "boundary variation and reference are fixed before readout; Q_tau improvement policy is fixed",
            "REQUIRED_OPEN",
            "fixed H_ref, no-flux and improvement ambiguity remain unsigned",
        ),
        (
            "SPN3685_6_silent_aux",
            "S_silent_aux[Z^A]",
            "Z^A,q,Dq,domain/memory variables",
            "extra variables are first-class, topological, or positive double-zero with no linear source/stress hair",
            "SILENCE_NOT_PROVED",
            "Dq map, vertical basis and double-zero theorem remain unsigned",
        ),
        (
            "SPN3685_7_total",
            "S_parent^trial=sum owned/staged blocks",
            "all retained fields",
            "theta_MTS=sum theta_i and Q_tau^MTS=sum Q_tau_i plus fixed improvements only after every sector certificate passes",
            "TOTAL_NOT_ADOPTED",
            "use as derivation spine only, not claim input",
        ),
    ]
    return [
        {
            **base(ts),
            "spine_id": spine_id,
            "action_block": action_block,
            "fields": fields,
            "variation_output": variation_output,
            "status": status,
            "blocking_gap": blocking_gap,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for spine_id, action_block, fields, variation_output, status, blocking_gap in specs
    ]


def sector_certificate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("SEC3685_0_EH", "EH/local spin-2", "theta_EH,Q_tau^EH", "REFERENCE_ONLY", "MTS-to-EH reduction and silent sectors", "R_EH_reference_guard"),
        ("SEC3685_1_matter_EM", "ordinary matter/EM", "theta_matter,theta_EM,Hilbert source stress", "CONDITIONAL_UNSIGNED", "matter descent, no source-only prefactor, EM normalization", "R_matter_EM_source"),
        ("SEC3685_2_kappa", "constant coupling", "no local Q_tau drift from kappa", "CANDIDATE_NOT_ADOPTED", "topological kappa owner", "R_kappa_owner"),
        ("SEC3685_3_GK", "Gamma/Khat/q_loc", "theta_GK,Q_tau^GK,C_tau^GK", "PRIMARY_HARDEST_BLOCKER", "action existence and first variation", "R_GK_action"),
        ("SEC3685_4_selector_projector", "domain selector/PiM", "selector/projector current contribution", "PARTIAL_NOT_PARENT_CLOSED", "metric stress, projector origin, source support", "R_selector_PiM"),
        ("SEC3685_5_worldtube", "worldtube source glue", "Q_M[tau] and M_source[W] bridge", "CORE_MASS_BLOCKER", "H_tau-H_ref and noncircular denominator", "R_worldtube_glue"),
        ("SEC3685_6_boundary", "boundary/reference", "Q_tau^boundary and fixed improvement", "REFERENCE_BLOCKER", "fixed reference, no-flux, counterterm policy", "R_boundary_ref"),
        ("SEC3685_7_tau_frame", "tau/surface/frame", "same observed tau action", "SAME_FRAME_LOCK_MISSING", "tau_source=tau_charge=tau_clock=tau_readout", "R_tau_surface"),
        ("SEC3685_8_total", "total parent action", "theta_MTS,Q_tau^MTS,C_tau", "PARENT_CERTIFICATE_FAILED", "all sector certificates above", "R_parent_LthetaQ"),
    ]
    return [
        {
            **base(ts),
            "sector_id": sector_id,
            "sector": sector,
            "required_theta_Qtau_piece": required_theta_qtau_piece,
            "status": status,
            "promotion_requirement": promotion_requirement,
            "feeds_residual": feeds_residual,
            "sector_certificate_passed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for sector_id, sector, required_theta_qtau_piece, status, promotion_requirement, feeds_residual in specs
    ]


def residual_bound_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("RPB3685_0_total", "abs(R_parent_LthetaQ)/N_H", "(|R_GK_action|+|R_selector_PiM|+|R_worldtube_glue|+|R_boundary_ref|+|R_tau_surface|+|R_matter_EM_source|+|R_kappa_owner|+|R_silent_aux|)/N_H", "dimensionless no-cancellation envelope", "source-ready parent extraction envelope; nonclaim until every component and N_H are sourced", "SPN3685_7_total"),
        ("RPB3685_1_GK_action", "abs(R_GK_action)/N_H", "MISSING_GK_ACTION_FIRST_VARIATION_BOUND_VALUE", "dimensionless", "needs S_GK action existence, Helmholtz check, Euler closure, double-zero and boundary no-flux", "GK513_0_action_existence"),
        ("RPB3685_2_selector_PiM", "abs(R_selector_PiM)/N_H", "MISSING_SELECTOR_PIM_BOUND_VALUE", "dimensionless", "needs parent projector/domain selector first variation and source support map", "SEC3685_4_selector_projector"),
        ("RPB3685_3_worldtube", "abs(R_worldtube_glue)/N_H", "MISSING_WORLDTUBE_GLUE_BOUND_VALUE", "dimensionless", "needs M_source[W]=H_tau-H_ref and noncircular denominator proof", "SEC3685_5_worldtube"),
        ("RPB3685_4_boundary", "abs(R_boundary_ref)/N_H", "MISSING_BOUNDARY_REFERENCE_BOUND_VALUE", "dimensionless", "needs fixed H_ref/B_ref/no-flux/improvement policy", "SEC3685_6_boundary"),
        ("RPB3685_5_tau", "abs(R_tau_surface)/N_H", "MISSING_TAU_SURFACE_BOUND_VALUE", "dimensionless", "needs single tau/surface/frame branch", "SEC3685_7_tau_frame"),
        ("RPB3685_6_matter_EM", "abs(R_matter_EM_source)/N_H", "MISSING_MATTER_EM_DESCENT_BOUND_VALUE", "dimensionless", "needs matter/EM q-descent and no source-only prefactor", "SEC3685_1_matter_EM"),
        ("RPB3685_7_closure_axiom_flag", "AX_LQ_adopted", "False", "boolean", "closure axiom is staged but not adopted", "AX3685_0_parent_Noether"),
    ]
    return [
        {
            **base(ts),
            "bound_id": bound_id,
            "quantity": quantity,
            "bound_or_formula": bound_or_formula,
            "units": units,
            "status": "FORMULA_READY_INPUTS_MISSING" if bound_or_formula != "False" else "CLOSURE_AXIOM_NOT_ADOPTED",
            "interpretation": interpretation,
            "source_anchor": source_anchor,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for bound_id, quantity, bound_or_formula, units, interpretation, source_anchor in specs
    ]


def closure_axiom_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "AX3685_0_parent_Noether",
            "There exists a finite-order diffeomorphism-invariant S_parent^trial whose complete variation gives theta_MTS and whose observed-time Noether current satisfies J_tau=dQ_tau^MTS+C_tau.",
            "would close R_parent_LthetaQ by assumption, not derivation",
            "private algebraic continuation only; no local-GR/Newton/R10/PPN/WEP claim",
            "NOT_ADOPTED",
        ),
        (
            "AX3685_1_sector_completeness",
            "Every retained sector supplies field list, first variation, theta_i, Q_tau_i/C_tau_i, stress/source term and boundary rule.",
            "prevents EH-only or partial-sector smuggling",
            "checklist for future derivation attempts",
            "NOT_ADOPTED",
        ),
        (
            "AX3685_2_local_LC_branch",
            "A local LC branch may be used as a private derivation branch if Gamma_ind/omega_ind are absent from ordinary/source/readout sectors and all residual rows remain explicit.",
            "gives the least-scrutiny local-GR route without claiming public parent derivation",
            "guide for local branch algebra only",
            "PRIVATE_BRANCH_ONLY",
        ),
        (
            "AX3685_3_no_claim_use",
            "No empirical score or public statement may use AX_LQ as if it were derived.",
            "keeps closure from becoming a hidden axiom-smuggle",
            "claim gates remain blocked",
            "ACTIVE_GUARD",
        ),
    ]
    return [
        {
            **base(ts),
            "axiom_id": axiom_id,
            "axiom_if_adopted": axiom_if_adopted,
            "cost": cost,
            "allowed_use": allowed_use,
            "status": status,
            "adopted_now": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for axiom_id, axiom_if_adopted, cost, allowed_use, status in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3685_0_result", "R_parent_LthetaQ=0 is not derived", "ACTION_SPINE_STAGED_NOT_ADOPTED", "the trial parent spine exists but sector certificates fail", "do not promote theta_MTS/Q_tau^MTS"),
        ("DEC3685_1_progress", "the parent action problem is now sector-factorized", "REAL_PROGRESS", "the exact Noether target, trial action spine, failed sectors and closure axiom are separated", "attack the first failed sector instead of recircling coupling"),
        ("DEC3685_2_best_next", "GK/q_loc action existence is the first hard sector", "NEXT_BEST_TARGET", "it blocks theta_GK,Q_tau_GK,C_tau_GK and the local vacuum q_loc route", "run Helmholtz/action-existence test next"),
        ("DEC3685_3_closure_policy", "closure axiom remains not adopted", "NO_AXIOM_SMUGGLING", "adopting it would make the framework less derivable", "use only as private algebraic fallback"),
        ("DEC3685_4_private", "no local-GR/Newton/source claim", "PRIVATE_NONCLAIM", "action spine is not proof", "continue privately"),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "status": status,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for decision_id, decision, status, reason, next_action in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3685_0_parent_action", "adopt S_parent^trial as current MTS parent action", "BLOCKED_SECTOR_CERTIFICATES", "GK/q_loc, PiM/worldtube, boundary/reference, tau/frame, matter descent and silent sectors are not all signed"),
        ("CG3685_1_theta_Qtau", "claim theta_MTS/Q_tau^MTS extracted", "BLOCKED_NO_SIGNED_TOTAL_ACTION", "exact Noether formula needs a signed total parent action"),
        ("CG3685_2_closure_axiom_claim", "use AX_LQ as claim evidence", "BLOCKED_AXIOM_NOT_DERIVATION", "closure axiom is not adopted and cannot support empirical/local-GR claims"),
        ("CG3685_3_Newton_GR", "claim Newton/local-GR source bridge", "BLOCKED_RPARENT_AND_RQTAU", "parent L/theta/Q and downstream source bridge remain residualized"),
        ("CG3685_4_public_or_github", "public/GitHub promotion", "BLOCKED_PRIVATE", "private derivation checkpoint only"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": claim_gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for claim_gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "PARENT_ACTION_SPINE_STAGED_LTHETA_QTAU_EXTRACTION_NOT_DERIVED_CLOSURE_AXIOM_NOT_ADOPTED_NONCLAIM",
            "summary": "3685 writes the trial parent current-chain action spine and exact Noether extraction formula, but refuses adoption because sector certificates fail. R_parent_LthetaQ remains live as a sector-factorized residual; AX_LQ is staged only as a nonclaim closure axiom.",
            "claim_ceiling": "no S_parent adoption, theta_MTS/Q_tau extraction, R_parent_LthetaQ zero, R_Qtau_owner zero, Newton/local-GR source bridge, empirical pass, or public claim is made",
            "useful_result": "the next derivation is no longer generic coupling: it is the GK/q_loc sector action-existence and first-variation test",
            "next_missing_piece": "derive S_GK with Helmholtz-compatible first variation generating Gamma_eff/K_hat/q_loc, or retain R_GK_action as a bound row",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3685_0",
            "target_doc": "3686-Y5-R2FR-GK-q_loc-action-existence-Helmholtz-or-RGK-action-bound-row.md",
            "target_script": "scripts/Y5_R2FR_3686_GK_q_loc_action_existence_Helmholtz_or_RGK_action_bound_row.py",
            "objective": "test whether a parent S_GK exists whose first variation supplies theta_GK, Q_tau^GK, C_tau^GK and the q_loc Euler/Ward identity; if not, promote R_GK_action as a nonclaim bound row with Helmholtz, boundary and double-zero inputs",
            "success_gate": "S_GK is theorem-owned by an explicit first variation and Helmholtz check, or R_GK_action is staged as a finite residual without local-GR/Newton claims",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    spine: list[dict[str, object]],
    sectors: list[dict[str, object]],
    bounds: list[dict[str, object]],
    axioms: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3685 - Parent L/theta/Qtau current-chain extraction or closure axiom",
        "",
        f"**Status:** {status[0]['status']}",
        "",
        "This checkpoint attempts the parent Noether extraction directly. It writes the trial parent action spine and exact current-chain formula, but it does **not** adopt the action as current MTS because the sector certificates still fail.",
        "",
        "## Main result",
        "",
        "`delta L_parent = E_I delta Phi^I + d theta_MTS`.",
        "",
        "`J_tau = theta_MTS(L_tau Phi) - i_tau L_parent = dQ_tau^MTS + C_tau`.",
        "",
        "Trial spine:",
        "",
        "`S_parent^trial = S_EH + S_matter+EM + S_kappa_top + S_GK + S_selector/PiM/worldtube + S_boundary_ref + S_silent_aux`.",
        "",
        "Extraction verdict:",
        "",
        "`R_parent_LthetaQ != 0` is retained because the action spine is staged but not adopted.",
        "",
        "Closure axiom:",
        "",
        "`AX_LQ` is written for private algebraic continuation only and is **not adopted** as evidence.",
        "",
        "## Extraction audit rows",
    ]
    for row in audit:
        lines.append(f"- `{row['audit_id']}`: {row['status']} - {row['claim']} -> {row['consequence']}")
    lines.extend(["", "## Trial action spine"])
    for row in spine:
        lines.append(f"- `{row['spine_id']}`: {row['status']} - `{row['action_block']}` -> {row['blocking_gap']}")
    lines.extend(["", "## Sector certificate rows"])
    for row in sectors:
        lines.append(f"- `{row['sector_id']}`: {row['status']} - {row['sector']} needs {row['promotion_requirement']}")
    lines.extend(["", "## Residual bound rows"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}`: {row['status']} - `{row['quantity']}` -> `{row['bound_or_formula']}`; {row['interpretation']}")
    lines.extend(["", "## Closure axiom rows"])
    for row in axioms:
        lines.append(f"- `{row['axiom_id']}`: {row['status']} adopted_now={row['adopted_now']} - {row['allowed_use']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['decision']} -> {row['next_action']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']} because {row['reason']}")
    lines.extend(["", "## Next target", f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.", "", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    spine: list[dict[str, object]],
    sectors: list[dict[str, object]],
    bounds: list[dict[str, object]],
    axioms: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + audit + spine + sectors + bounds + axioms + decisions + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3685*", "3685-Y5-R2FR-*", "P8_Y5*3685*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    audit_by_id = {str(row["audit_id"]): row for row in audit}
    spine_by_id = {str(row["spine_id"]): row for row in spine}
    sector_by_id = {str(row["sector_id"]): row for row in sectors}
    axiom_by_id = {str(row["axiom_id"]): row for row in axioms}
    bound_by_id = {str(row["bound_id"]): row for row in bounds}

    add("VAL3685_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3685_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3685_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3685 outputs written")
    add("VAL3685_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3685_4_noether_formula", audit_by_id["LQ3685_1_exact_noether_formula"]["status"] == "EXACT_CONDITIONAL_FORMULA", "exact Noether formula recorded")
    add("VAL3685_5_trial_spine", "S_GK" in spine_by_id["SPN3685_7_total"]["variation_output"] or "sum" in spine_by_id["SPN3685_7_total"]["action_block"], "trial spine total row present")
    add("VAL3685_6_not_adopted", audit_by_id["LQ3685_6_verdict"]["status"] == "R_PARENT_LTHETAQ_ZERO_NOT_DERIVED_ACTION_SPINE_AND_AXIOM_STAGED", "R_parent_LthetaQ zero is not claimed")
    add("VAL3685_7_primary_blocker", sector_by_id["SEC3685_3_GK"]["status"] == "PRIMARY_HARDEST_BLOCKER" and "S_GK" in spine_by_id["SPN3685_3_GK_q_loc"]["action_block"], "GK/q_loc action sector is identified as primary blocker")
    add("VAL3685_8_closure_axiom_not_adopted", axiom_by_id["AX3685_0_parent_Noether"]["adopted_now"] is False and bound_by_id["RPB3685_7_closure_axiom_flag"]["bound_or_formula"] == "False", "closure axiom is written but not adopted")
    add("VAL3685_9_claim_gates_blocked", all(row["claim_allowed"] is False and row["score_ready"] is False for row in gates), "claim gates remain blocked")
    add("VAL3685_10_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3685_11_doc_written", "S_parent^trial" in doc_text and "not adopted" in doc_text.lower() and "J_tau" in doc_text, "doc records trial spine, Noether formula and non-adoption")
    add("VAL3685_12_next_target", next_target[0]["target_doc"].startswith("3686-") and "S_GK" in next_target[0]["objective"], "3686 targets GK/q_loc action existence")
    add("VAL3685_13_no_formalization_leak", not leaks, "no 3685 checkpoint files in formalization-workbench")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    audit = extraction_audit_rows(ts)
    spine = action_spine_rows(ts)
    sectors = sector_certificate_rows(ts)
    bounds = residual_bound_rows(ts)
    axioms = closure_axiom_rows(ts)
    decisions = decision_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3685_SOURCE_REGISTER.csv",
        "audit": RESIDUALS / "P8_Y5_R2FR_3685_LTHETA_QTAU_EXTRACTION_AUDIT.csv",
        "spine": RESIDUALS / "P8_Y5_R2FR_3685_TRIAL_PARENT_ACTION_SPINE_ROWS.csv",
        "sectors": RESIDUALS / "P8_Y5_R2FR_3685_SECTOR_CERTIFICATE_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3685_RPARENT_LTHETAQ_BOUND_ROWS.csv",
        "axioms": RESIDUALS / "P8_Y5_R2FR_3685_CLOSURE_AXIOM_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3685_DECISION_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3685_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3685_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3685_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3685_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["audit"], audit)
    write_csv(outputs["spine"], spine)
    write_csv(outputs["sectors"], sectors)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["axioms"], axioms)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, audit, spine, sectors, bounds, axioms, decisions, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, audit, spine, sectors, bounds, axioms, decisions, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3685 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3685 checkpoint: parent action spine staged; L/theta/Q extraction not adopted; GK action next")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
