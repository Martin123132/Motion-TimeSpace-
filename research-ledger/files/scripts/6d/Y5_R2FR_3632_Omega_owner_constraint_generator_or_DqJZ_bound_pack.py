from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3632"
BRANCH_ID = "MTS_R2FR_Y5_OMEGA_OWNER_CONSTRAINT_GENERATOR_OR_DQJZ_BOUND_PACK_3632"
DOC = ROOT / "3632-Y5-R2FR-Omega-owner-constraint-generator-or-DqJZ-bound-pack.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8", errors="replace")


def out_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3632_SOURCE_REGISTER.csv",
        "owner_routes": RESIDUALS / "P8_Y5_R2FR_3632_SAME_PARENT_OWNER_ROUTES.csv",
        "omega_chain_gate": RESIDUALS / "P8_Y5_R2FR_3632_OMEGA_THETA_PJQ_CHAIN_GATE.csv",
        "constraint_generator": RESIDUALS / "P8_Y5_R2FR_3632_CONSTRAINT_GENERATOR_AUDIT.csv",
        "bound_pack": RESIDUALS / "P8_Y5_R2FR_3632_DQJZ_BOUND_PACK.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3632_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3632_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3632_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_Omega_owner_constraint_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3632_VALIDATION.csv",
    }


def source_map() -> list[dict[str, str]]:
    return [
        {
            "source_id": "handoff_3631",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3631_NEXT_TARGET.csv"),
            "needle": "Omega/theta/P/J/q owner",
            "role": "3631 handoff: same-parent owner or Dq/J_Z coefficient pack.",
        },
        {
            "source_id": "dcdagger_vertical_3631",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3631_DCDAGGER_VERTICAL_GENERATOR_MAP.csv"),
            "needle": "Omega_flat(e_X)",
            "role": "exact generator reconstruction equation.",
        },
        {
            "source_id": "leaks_3631",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3631_DQ_Z_LEAK_AND_JZ_COEFFICIENTS.csv"),
            "needle": "JZC3631_8_R11_operator",
            "role": "Dq and J_Z rows to convert to bound pack if owner route fails.",
        },
        {
            "source_id": "dcdagger_591",
            "path": str(RESIDUALS / "P8_Y5_R10_591_DCDAGGER_FORMULA.csv"),
            "needle": "DCA591_4_compare_to_Omega_flat",
            "role": "formal DCdagger-to-Omega comparison.",
        },
        {
            "source_id": "omega_compare_591",
            "path": str(RESIDUALS / "P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv"),
            "needle": "CMP591_5_verdict",
            "role": "prior comparison says formula progress but no certificate.",
        },
        {
            "source_id": "noether_583",
            "path": str(RESIDUALS / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv"),
            "needle": "NMC583_3_momentum_map",
            "role": "momentum-map/constraint generator contract.",
        },
        {
            "source_id": "owner_attempt_583",
            "path": str(RESIDUALS / "P8_Y5_R10_583_PARENT_MOMENTUM_MAP_OWNER_ATTEMPT.csv"),
            "needle": "OMA583_5_verdict",
            "role": "same-parent owner routes and failure modes.",
        },
        {
            "source_id": "variation_667",
            "path": str(RESIDUALS / "P8_Y5_R10_667_VARIATION_LEDGER.csv"),
            "needle": "VL667_4_integrability_curl",
            "role": "covariant phase-space variation and integrability obstruction.",
        },
        {
            "source_id": "action_ansatz_667",
            "path": str(RESIDUALS / "P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv"),
            "needle": "PBA667_1_bulk_action",
            "role": "candidate parent action ansatz.",
        },
        {
            "source_id": "fallback_667",
            "path": str(RESIDUALS / "P8_Y5_R10_667_RESIDUAL_FALLBACK_ROWS.csv"),
            "needle": "RF667_0_LX_theta_Qtau_owner",
            "role": "fallback rows for missing sector Lagrangian/theta/charge owner.",
        },
        {
            "source_id": "lx_candidates_669",
            "path": str(RESIDUALS / "P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv"),
            "needle": "LX669_1_vertical_constraint",
            "role": "ranked L_X routes with vertical constraint as best active theorem route.",
        },
        {
            "source_id": "theta_669",
            "path": str(RESIDUALS / "P8_Y5_R10_669_THETA_QX_VARIATION_LEDGER.csv"),
            "needle": "V669_3_symplectic",
            "role": "theta/Q_X/omega variation ledger.",
        },
        {
            "source_id": "r10r11_vector_669",
            "path": str(RESIDUALS / "P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv"),
            "needle": "RV669_9_R11_operator_coefficients",
            "role": "finite-range/operator coefficients for residual branch.",
        },
    ]


def source_rows(t: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for src in source_map():
        path = Path(src["path"])
        exists = path.exists()
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": src["source_id"],
                "path": src["path"],
                "exists": exists,
                "needle": src["needle"],
                "needle_found": exists and contains(path, src["needle"]),
                "role": src["role"],
            }
        )
    return rows


def owner_route_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "route_id": "OR3632_0_strict_quotient_absence",
            "route": "strict quotient action / no independent X or Z pole",
            "parent_action_shape": "S_parent=S_red[q(Phi)]+S_matter[g_obs(q),Psi]+S_top[q]",
            "omega_chain_effect": "i_e Omega=0 and DCdagger has no physical generator because the direction is absent from phase space",
            "what_it_would_buy": "K_X=0, Q_edge=0, no local fifth-force/PPN pole from this sector",
            "current_evidence": "583 marks this best if parent projection is derived; 669 says absent quotient variable is rank 1 but not derived",
            "current_status": "BEST_GR_REDUCTION_ROUTE_NOT_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "route_id": "OR3632_1_first_class_vertical_constraint",
            "route": "first-class vertical constraint",
            "parent_action_shape": "S_parent=S_obs[q]+int Lambda^A C_A(Phi)+S_matter[g_obs(q),Psi]",
            "omega_chain_effect": "e_epsilon generated by G[epsilon]; i_e Omega=delta G; Dq[e_epsilon]=0; boundary charge proper/zero",
            "what_it_would_buy": "Z becomes genuine gauge/constraint direction; J_Z and Dq leaks can vanish without fitted compensation",
            "current_evidence": "669 ranks vertical constraint as best active theorem route but needs actual generator, algebra, and boundary silence",
            "current_status": "BEST_ACTIVE_ROUTE_NOT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "route_id": "OR3632_2_defect_potential_owner",
            "route": "defect potential / canonical P owner",
            "parent_action_shape": "S_X=int V_def(Z_{mu nu},Y)+matter/source terms with P^{mu nu}=partial V_def/partial Z_{mu nu}",
            "omega_chain_effect": "P and J_eff come from the same variation, so DCdagger can match Omega_flat(e_X)",
            "what_it_would_buy": "turns P,J from inserted tensors into a true variational object",
            "current_evidence": "583 calls this promising but V_def, Z_{mu nu}, and J_eff are not supplied",
            "current_status": "PROMISING_CONTRACT_NOT_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "route_id": "OR3632_3_relative_cohomology_owner",
            "route": "relative cohomology / memory-current momentum map",
            "parent_action_shape": "J_eff=S_L+d_rel(P_mem J_rel), with parent-owned P_mem and exact/proper boundary primitive",
            "omega_chain_effect": "boundary/memory charge becomes exact or topological-zero if P_mem stress and primitive are parent-owned",
            "what_it_would_buy": "could remove edge leakage without a propagating scalar pole",
            "current_evidence": "583 keeps relative cohomology route open but not closed; boundary/projector stress remains conditional",
            "current_status": "OPEN_NOT_PARENT_OWNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "route_id": "OR3632_4_positive_sourcefree_mode",
            "route": "positive source-free physical mode",
            "parent_action_shape": "L_X=1/2 Z_X|grad X|^2+1/2 M_X^2X^2 with J_X=0 and boundary_flux=0",
            "omega_chain_effect": "does not make X vertical; it makes X a silent physical mode only if source and boundary are zero",
            "what_it_would_buy": "source-free no-hair, not a quotient-descent theorem",
            "current_evidence": "669 ranks it below vertical routes; Z_X,M_X^2,J_X,boundary flux are unsigned",
            "current_status": "SEPARATE_NOHAIR_ROUTE_NOT_VERTICAL_OWNER",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "route_id": "OR3632_5_residual_branch",
            "route": "massive/source residual branch",
            "parent_action_shape": "L_X=1/2 Z_X|grad X|^2+1/2 M_X^2X^2-XJ_X plus retained Dq/J_Z couplings",
            "omega_chain_effect": "no zero theorem; coefficients must be sourced and scored",
            "what_it_would_buy": "honest empirical survival path through R10/R11/PPN/WEP/clock/orbital bounds",
            "current_evidence": "669 residual vector and 3631 Dq/J_Z rows already stage nonclaim inputs",
            "current_status": "FALLBACK_SELECTED_IF_OWNER_FAILS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def omega_chain_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "OCG3632_0_parent_L",
            "needed_object": "single parent Lagrangian L_parent",
            "required_identity": "delta L_parent=E_i delta Phi^i+d theta(delta Phi)",
            "current_evidence": "667 has a covariant phase-space ansatz but L_X/L_residual are not unique enough to compute Theta_X/Q_X",
            "result_if_pass": "theta and Omega are owned, not chosen after the fact",
            "current_status": "FORMAL_ANSATZ_NOT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "OCG3632_1_theta_Omega",
            "needed_object": "theta and Omega",
            "required_identity": "Omega=delta theta from the same L_parent and is invertible modulo proper gauge on the chosen branch",
            "current_evidence": "591/583 require parent Omega; 669 says theta/Q_X are formal not owned",
            "result_if_pass": "e_X=Omega^{-1}DCdagger[X] can be computed",
            "current_status": "OMEGA_OWNER_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "OCG3632_2_PJ_owner",
            "needed_object": "P^{mu nu} and J_eff^nu",
            "required_identity": "C_X^nu=-nabla_mu P^{mu nu}+J_eff^nu with P,J from theta/Noether/source variation of the same L_parent",
            "current_evidence": "591 says P and J owners are not derived; 583 rejects independent P",
            "result_if_pass": "DCdagger is not an inserted operator; it is the adjoint of a parent current constraint",
            "current_status": "P_J_OWNER_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "OCG3632_3_q_owner",
            "needed_object": "quotient map q",
            "required_identity": "q(Phi) is defined before matter/source readout and Dq[e_X]=0 for the generated e_X",
            "current_evidence": "1667 says q is a partial prior contract and not computable",
            "result_if_pass": "quotient descent can kill matter/source coupling",
            "current_status": "Q_OWNER_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "OCG3632_4_boundary",
            "needed_object": "boundary differentiability and charge",
            "required_identity": "delta Q_X cancels B_DC and Q_X is zero/exact/proper on compact local collar",
            "current_evidence": "591 boundary adjoint not cancelled; 583 boundary zero not derived; 667 boundary flux open",
            "result_if_pass": "vertical generator does not leak through alpha3/source-normalization boundary channels",
            "current_status": "BOUNDARY_CHARGE_OWNER_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "OCG3632_5_observable_map",
            "needed_object": "Z-to-R_local map",
            "required_identity": "R_local^i=M^i_A Z^A+N^i_aDq^a+B^i with full coverage of R0-R11 or explicit bounds",
            "current_evidence": "3631 writes the map but all projections remain missing",
            "result_if_pass": "local-GR residual scoring becomes component-complete",
            "current_status": "OBSERVABLE_MAP_OWNER_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "OCG3632_6_verdict",
            "needed_object": "same-parent owner chain",
            "required_identity": "L_parent -> theta/Omega/P/J/q/Q_boundary -> e_X -> Dq[e_X]=0 -> R_local map",
            "current_evidence": "each piece exists as a contract, but not one same-parent signed chain",
            "result_if_pass": "3630 conditional theorem can promote from target to derivation",
            "current_status": "OWNER_CHAIN_NOT_SIGNED_BOUND_PACK_REQUIRED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def constraint_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "constraint_id": "CGA3632_0_generator_definition",
            "test": "define Hamiltonian generator",
            "formula": "G[epsilon]=int_Sigma epsilon^A C_A + int_boundary Q_epsilon",
            "pass_condition": "i_{e_epsilon}Omega=delta G[epsilon] with differentiable G",
            "current_status": "CONTRACT_ONLY",
            "if_fail": "no parent vertical generator; retain Dq leak",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "constraint_id": "CGA3632_1_constraint_surface",
            "test": "constraint removes physical pole",
            "formula": "C_A(Phi)=0 before matter coupling and before source readout",
            "pass_condition": "X/Z is absent from physical quotient or pure first-class gauge",
            "current_status": "NOT_PARENT_SIGNED",
            "if_fail": "X/Z remains physical or sourced residual",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "constraint_id": "CGA3632_2_algebra",
            "test": "first-class closure",
            "formula": "{G[epsilon],G[eta]}=G[[epsilon,eta]]+K_boundary[epsilon,eta]",
            "pass_condition": "K_boundary=0 or proper/forbidden local branch charge",
            "current_status": "NOT_COMPUTED",
            "if_fail": "constraint is second-class/anomalous or boundary-physical",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "constraint_id": "CGA3632_3_quotient_action",
            "test": "generator is vertical to q",
            "formula": "Dq[{Phi,G[epsilon]}]=0",
            "pass_condition": "q includes matter/coframe/source/boundary readout and all components vanish",
            "current_status": "NOT_RUNNABLE_Q_MISSING",
            "if_fail": "quotient descent does not kill J_Z",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "constraint_id": "CGA3632_4_boundary_silence",
            "test": "proper/zero boundary charge",
            "formula": "Q_epsilon|local collar=0, exact, or Pi_M-orthogonal theorem-zero",
            "pass_condition": "no alpha3/source-normalization/edge flux from the would-be gauge direction",
            "current_status": "NOT_DERIVED",
            "if_fail": "boundary flux rows remain physical residuals",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "constraint_id": "CGA3632_5_verdict",
            "test": "constraint-first route",
            "formula": "CGA3632_0..CGA3632_4 all pass",
            "pass_condition": "Z/X is a parent-owned proper vertical direction",
            "current_status": "CONSTRAINT_GENERATOR_NOT_CLAIMED",
            "if_fail": "Dq/J_Z/R10/R11 bound pack is required",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bound_pack_rows(t: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    leaks = read_csv(RESIDUALS / "P8_Y5_R2FR_3631_DQ_Z_LEAK_AND_JZ_COEFFICIENTS.csv")
    for row in leaks:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "pack_id": row["row_id"].replace("3631", "3632"),
                "source_type": row["type"],
                "quantity": row["quantity"],
                "formula_or_template": row["formula_or_template"],
                "affected_channel": row["affected_channel"],
                "minimum_for_executable": row["minimum_inputs"] + "; source_path; units; comparator_bound; no_cancellation_guard",
                "score_status": "not_scoreable",
                "source_path": row["source_path"],
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    residual_vector = read_csv(RESIDUALS / "P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv")
    for row in residual_vector:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "pack_id": row["residual_id"].replace("RV669", "RV3632"),
                "source_type": "X_sector_R10_R11_residual",
                "quantity": row["coefficient"],
                "formula_or_template": row["meaning"],
                "affected_channel": row["feeds"],
                "minimum_for_executable": row["required_parent_input"] + "; " + row["units_status"] + "; source-backed numeric/theorem-zero value",
                "score_status": "not_scoreable",
                "source_path": row["source_paths"],
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def decision_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3632_0_owner_attempt",
            "decision": "The same-parent owner chain is now explicit: L_parent must generate theta/Omega/P/J/q and boundary charge together.",
            "status": "OWNER_CHAIN_SPECIFIED",
            "next_action": "do not treat separate ledgers as a derivation until OCG3632 gates pass together",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3632_1_best_route",
            "decision": "The best route remains strict quotient absence or first-class vertical constraint; positive source-free mode is a separate no-hair route, not verticality.",
            "status": "ROUTE_RANK_LOCKED",
            "next_action": "attempt explicit constraint algebra only if q/Omega owners can be sourced",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3632_2_current_claim",
            "decision": "Current corpus still lacks the same-parent owner, so no vertical generator, J_Z zero, local GR, Newton, PPN, or R10/R11 claim is promoted.",
            "status": "NO_CLAIM_BOUND_PACK_ACTIVE",
            "next_action": "use bound pack rows if owner construction remains unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3632_3_next_target",
            "decision": "Next target should attempt the strict quotient/absent-pole theorem first because it removes the most local-test pressure.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3633-Y5-R2FR-strict-quotient-absent-pole-theorem-or-bound-pack-fill.md",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def status_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS3632_0",
            "result": "SAME_PARENT_OWNER_CHAIN_EXPLICIT_NOT_SIGNED_DQJZ_BOUND_PACK_STAGED",
            "summary": "3632 makes the Omega/theta/P/J/q owner chain explicit and ranks the viable routes. Strict quotient absence and first-class vertical constraint are the only clean local-GR routes; defect-potential and relative-cohomology owners remain promising but unsigned; positive source-free mode is a separate no-hair branch, not a vertical proof. The current corpus does not sign one parent action that supplies L, theta, Omega, P, J, q, and boundary charge together, so Dq/J_Z/R10/R11 bound-pack rows remain active and no claim is promoted.",
            "owner_chain_written": True,
            "constraint_generator_claimed": False,
            "bound_pack_staged": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3632_0",
            "target_doc": "3633-Y5-R2FR-strict-quotient-absent-pole-theorem-or-bound-pack-fill.md",
            "target_script": "scripts/Y5_R2FR_3633_strict_quotient_absent_pole_theorem_or_bound_pack_fill.py",
            "objective": "try the strict quotient/no-independent-pole theorem first: prove X/Z is absent from the physical tangent space before variation; if not, start filling the Dq/J_Z/X-sector bound pack with executable source rows",
            "success_gate": "q is explicit, X/Z is absent or pure quotient fibre before matter coupling, no boundary charge survives, and R0-R11 residual map is covered; otherwise at least one bound-pack row becomes source-ready",
            "reason": "3632 shows this is the least-scrutiny route; if it fails, the project should move from theorem-zero attempts to concrete scoring rows.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_object": "Omega_theta_PJq_owner",
            "canonical_status": "OWNER_CHAIN_EXPLICIT_NOT_SIGNED",
            "usable_result": "Local vertical proof requires one parent L that generates theta/Omega/P/J/q and a proper boundary charge; otherwise Dq/J_Z/R10/R11 coefficients must be scored.",
            "hard_block": "explicit q and same-parent L/theta/Omega/P/J/Q_boundary owner",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(rows: list[dict[str, object]], cols: list[str]) -> str:
    output = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(col, "")) for col in cols) + " |")
    return "\n".join(output)


def write_doc(src: list[dict[str, object]], routes: list[dict[str, object]], chain: list[dict[str, object]], constraints: list[dict[str, object]], bounds: list[dict[str, object]], decisions: list[dict[str, object]], status: list[dict[str, object]], nxt: list[dict[str, object]]) -> None:
    text = "\n\n".join(
        [
            "# 3632 Y5 R2FR Omega owner constraint generator or Dq/J_Z bound pack",
            f"**Status:** {status[0]['summary']}",
            "**Claim ceiling:** no same-parent owner, vertical generator, `J_Z=0`, local-GR, Newton, PPN, R10/R11, WEP, clock, Gdot, or EM-source claim is allowed from 3632.",
            "## Core result",
            (
                "The exact owner chain is now the object to prove:\n\n"
                "```text\n"
                "L_parent -> theta -> Omega=delta theta\n"
                "L_parent -> P,J through the same Noether/source variation\n"
                "L_parent -> q and matter/source descent\n"
                "Omega_flat(e_X)=DCdagger[X]\n"
                "Dq[e_X]=0\n"
                "Q_boundary[e_X]=0/exact/proper\n"
                "```\n\n"
                "If one parent action supplies all of that, the `3630` theorem can become a derivation. If not, the branch must stop trying to theorem-zero local GR and start scoring `Dq`, `J_Z`, and X-sector residual coefficients."
            ),
            "## Source register",
            table(src, ["source_id", "path", "exists", "needle_found", "role"]),
            "## Same-parent owner routes",
            table(routes, ["route_id", "route", "parent_action_shape", "omega_chain_effect", "what_it_would_buy", "current_status"]),
            "## Omega/theta/P/J/q chain gate",
            table(chain, ["gate_id", "needed_object", "required_identity", "current_evidence", "result_if_pass", "current_status"]),
            "## Constraint generator audit",
            table(constraints, ["constraint_id", "test", "formula", "pass_condition", "current_status", "if_fail"]),
            "## Dq/J_Z/X-sector bound pack",
            table(bounds, ["pack_id", "source_type", "quantity", "formula_or_template", "affected_channel", "minimum_for_executable", "score_status"]),
            "## Decisions",
            table(decisions, ["decision_id", "decision", "status", "next_action"]),
            "## Next target",
            table(nxt, ["target_doc", "target_script", "objective", "success_gate"]),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def validate(outputs: dict[str, Path], src: list[dict[str, object]]) -> list[dict[str, object]]:
    t = now()
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3632_0_sources_exist", all(row["exists"] for row in src), "all sources exist")
    add("VAL3632_1_needles_found", all(row["needle_found"] for row in src), "all source anchors found")
    pre = {name: path for name, path in outputs.items() if name != "validation"}
    add("VAL3632_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all pre-validation outputs written")
    details = []
    parse_ok = True
    for name, path in pre.items():
        try:
            count = len(read_csv(path))
            details.append(f"{name}:{count}")
            parse_ok = parse_ok and count > 0
        except Exception as exc:
            details.append(f"{name}:ERR:{exc}")
            parse_ok = False
    add("VAL3632_3_csv_parse", parse_ok, "; ".join(details))

    routes = read_csv(outputs["owner_routes"])
    chain = read_csv(outputs["omega_chain_gate"])
    constraints = read_csv(outputs["constraint_generator"])
    bounds = read_csv(outputs["bound_pack"])
    decisions = read_csv(outputs["decision_gates"])
    status = read_csv(outputs["status"])
    nxt = read_csv(outputs["next_target"])

    add("VAL3632_4_owner_routes_ranked", any(row["route_id"] == "OR3632_0_strict_quotient_absence" for row in routes) and any(row["route_id"] == "OR3632_1_first_class_vertical_constraint" for row in routes), "strict quotient and first-class routes present")
    add("VAL3632_5_chain_gate_complete", len(chain) >= 7 and any("L_parent -> theta/Omega/P/J/q" in row["required_identity"] for row in chain), "same-parent chain gate complete")
    add("VAL3632_6_constraint_generator_audit_written", any("G[epsilon]" in row["formula"] for row in constraints), "constraint generator audit written")
    add("VAL3632_7_bound_pack_carries_rows", len(bounds) >= 27 and any(row["source_type"] == "Dq_leak" for row in bounds) and any(row["source_type"] == "J_Z_coefficient" for row in bounds) and any(row["source_type"] == "X_sector_R10_R11_residual" for row in bounds), "Dq/JZ/X-sector bound rows carried forward")
    add("VAL3632_8_owner_not_claimed", all(row["valid_for_claim"].lower() == "false" for row in routes + chain + constraints), "owner and constraint rows remain nonclaim")
    add("VAL3632_9_bound_pack_nonclaim", all(row["valid_for_claim"].lower() == "false" and row["score_status"] == "not_scoreable" for row in bounds), "bound pack remains nonclaim/not scoreable")
    add("VAL3632_10_status_decision_nonclaim", all(row["valid_for_claim"].lower() == "false" for row in status + decisions + nxt), "status, decision, and next rows remain nonclaim")
    leaks = list(FORMALIZATION.rglob("*3632*")) if FORMALIZATION.exists() else []
    add("VAL3632_11_no_formalization_leak", not leaks, "no 3632 files in formalization-workbench")
    add("VAL3632_12_next_target_written", bool(nxt) and "3633" in nxt[0]["target_doc"], "3633 strict quotient target written")
    add("VAL3632_13_canonical_status_written", outputs["canonical_status"].exists() and "OWNER_CHAIN_EXPLICIT_NOT_SIGNED" in outputs["canonical_status"].read_text(encoding="utf-8", errors="replace"), "canonical Omega owner status written")
    return rows


def main() -> None:
    t = now()
    outputs = out_paths()
    src = source_rows(t)
    routes = owner_route_rows(t)
    chain = omega_chain_rows(t)
    constraints = constraint_rows(t)
    bounds = bound_pack_rows(t)
    decisions = decision_rows(t)
    status = status_rows(t)
    nxt = next_rows(t)
    canonical = canonical_rows(t)

    write_csv(outputs["source_register"], src)
    write_csv(outputs["owner_routes"], routes)
    write_csv(outputs["omega_chain_gate"], chain)
    write_csv(outputs["constraint_generator"], constraints)
    write_csv(outputs["bound_pack"], bounds)
    write_csv(outputs["decision_gates"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], nxt)
    write_csv(outputs["canonical_status"], canonical)
    write_doc(src, routes, chain, constraints, bounds, decisions, status, nxt)

    validation = validate(outputs, src)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3632 validation failed: {failures}")
    print(f"wrote 3632 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
