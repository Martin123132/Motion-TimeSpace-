from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3625"
BRANCH_ID = "MTS_R2FR_Y5_BIANCHI_RESIDUAL_CLOSURE_OR_FIRST_PPN_ENVELOPE_3625"
DOC = ROOT / "3625-Y5-R2FR-Bianchi-residual-closure-or-first-PPN-envelope-runner.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8", errors="replace")


def output_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3625_SOURCE_REGISTER.csv",
        "bianchi_derivation": RESIDUALS / "P8_Y5_R2FR_3625_BIANCHI_NOETHER_DERIVATION.csv",
        "closure_audit": RESIDUALS / "P8_Y5_R2FR_3625_RESIDUAL_CLOSURE_AUDIT.csv",
        "ppn_newton_schema": RESIDUALS / "P8_Y5_R2FR_3625_PPN_NEWTON_ENVELOPE_SCHEMA.csv",
        "smoke_rows": RESIDUALS / "P8_Y5_R2FR_3625_NONCLAIM_SMOKE_ROWS.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3625_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3625_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3625_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_Bianchi_residual_closure_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3625_VALIDATION.csv",
    }


def source_map() -> list[dict[str, str]]:
    return [
        {
            "source_id": "handoff_3624",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3624_NEXT_TARGET.csv"),
            "needle": "Bianchi-residual-closure",
            "role": "3624 handoff selecting Bianchi/residual envelope.",
        },
        {
            "source_id": "contract_3624",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3624_MINIMAL_LOCAL_GR_CONTRACT.csv"),
            "needle": "nabla_m[DeltaE_MTS^{mn}-kappa_eff DeltaT_MTS^{mn}]=0",
            "role": "minimal local-GR contract containing conservation gate.",
        },
        {
            "source_id": "residual_vector_3624",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3624_EXPLICIT_MTS_RESIDUAL_VECTOR.csv"),
            "needle": "RV3624_6_PPN_total",
            "role": "explicit residual vector to close or bound.",
        },
        {
            "source_id": "newton_ppn_3624",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3624_NEWTON_PPN_COMPLETION_GATES.csv"),
            "needle": "NPG3624_5_bianchi",
            "role": "Newton/PPN completion gates.",
        },
        {
            "source_id": "claim_gates_3624",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3624_CLAIM_GATES.csv"),
            "needle": "FAIL_CURRENT_CLAIM",
            "role": "nonclaim guard from 3624.",
        },
        {
            "source_id": "ppn_interface_2636",
            "path": str(RESIDUALS / "P8_Y5_GENERATOR_EFFECTIVE_PACK_2636_PPN_INTERFACE_MAP.csv"),
            "needle": "PPNI2636_6_total_abs",
            "role": "PPN interface map for fallback envelope.",
        },
        {
            "source_id": "operator_pack_2619",
            "path": str(RESIDUALS / "P8_Y5_GR_LEFT_HAND_GATE_2619_OPERATOR_RESIDUAL_PACK.csv"),
            "needle": "ORP2619_8_nonclaim_lock",
            "role": "operator residual pack and nonclaim lock.",
        },
        {
            "source_id": "einstein_lhs_2619",
            "path": str(RESIDUALS / "P8_Y5_GR_LEFT_HAND_GATE_2619_EINSTEIN_LEFT_HAND_LIMIT_ATTEMPT.csv"),
            "needle": "ELH2619_4_bianchi_gate",
            "role": "prior Bianchi/Noether compatibility gate.",
        },
        {
            "source_id": "newton_2619",
            "path": str(RESIDUALS / "P8_Y5_GR_LEFT_HAND_GATE_2619_NEWTON_POISSON_WEAK_FIELD_ATTEMPT.csv"),
            "needle": "NWF2619_1_poisson_conditional",
            "role": "Newton/Poisson conditional bridge.",
        },
        {
            "source_id": "eh_envelope_2579",
            "path": str(RESIDUALS / "P8_Y5_EH_DESCENT_COUPLING_PIM_2579_LOCAL_GR_RESIDUAL_ENVELOPE.csv"),
            "needle": "ENV2579_9_total",
            "role": "absolute local-GR residual envelope precedent.",
        },
        {
            "source_id": "q_loc_2581",
            "path": str(RESIDUALS / "P8_Y5_GAMMAKHAT_QLOC_2581_LOCAL_TEST_MAP.csv"),
            "needle": "TEST2581_0_PPN_alpha",
            "role": "q_loc local test projection map.",
        },
        {
            "source_id": "gk_stress_2469",
            "path": str(RESIDUALS / "P8_Y5_GK_STRESS_2469_LOCAL_METRIC_EQUATION_GATE.csv"),
            "needle": "MET2469_2_stealth_reduction",
            "role": "GK stress/local metric equation gate.",
        },
        {
            "source_id": "maxwell_3463",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv"),
            "needle": "nabla_mu T_EM",
            "role": "Maxwell stress exchange and Poynting source ledger.",
        },
        {
            "source_id": "wem_phi_3623",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3623_WEM_PHI_SOURCE_THEOREM.csv"),
            "needle": "Phi_EM_boundary",
            "role": "EM source-weight/boundary theorem split.",
        },
    ]


def source_register_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    rows = []
    for item in source_map():
        path = Path(item["path"])
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                **item,
                "exists": path.exists(),
                "needle_found": path.exists() and contains(path, item["needle"]),
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def bianchi_derivation_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "BND3625_0_parent_action",
            "step": "parent diffeomorphism-invariant action",
            "statement": "If the retained local MTS fields all descend from one diffeomorphism-invariant parent action, the residual tensors cannot be chosen independently.",
            "formula": "S_parent[g,psi,A,Phi]=S_EH+S_matter+S_EM+S_MTS_extra+S_boundary",
            "derived_effect": "sets the stage for a Noether identity over the whole retained system",
            "current_status": "CONDITIONAL_PARENT_ACTION_NOT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "BND3625_1_noether_identity",
            "step": "diffeomorphism variation",
            "statement": "For delta_xi fields = Lie_xi fields, integration by parts gives the generalized Bianchi/Noether identity.",
            "formula": "0=delta_xi S=int sqrt(-g)[E_g^{mn} L_xi g_mn+E_A L_xi Phi^A+E_psi L_xi psi]+boundary",
            "derived_effect": "nabla_m(2E_g^{mn}) + E_A nabla^n Phi^A + E_psi D^n psi + B_boundary^n = 0",
            "current_status": "EXACT_CONDITIONAL_IDENTITY",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "BND3625_2_on_shell_reduction",
            "step": "on-shell retained fields",
            "statement": "If matter, EM, and extra MTS Euler equations are satisfied and boundary flux is fixed/zero, the metric equation is divergence-compatible.",
            "formula": "E_A=0; E_psi=0; B_boundary^n=0 => nabla_m E_g^{mn}=0",
            "derived_effect": "Bianchi closure follows from the parent action rather than a separate plateau axiom",
            "current_status": "CONDITIONAL_REQUIRES_PARENT_EULER_AND_BOUNDARY",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "BND3625_3_residual_closure_law",
            "step": "residual field equation",
            "statement": "Writing local MTS as GR plus residuals imposes a conservation law on the residual difference, not on each piece separately.",
            "formula": "G^{mn}+Lambda g^{mn}=kappa_eff(T_matter^{mn}+T_EM^{mn})+DeltaE_MTS^{mn}; nabla_m[DeltaE_MTS^{mn}-kappa_eff DeltaT_MTS^{mn}]=C_B^n",
            "derived_effect": "C_B^n must be zero by parent Noether identity or carried as an observable conservation/preferred-frame residual",
            "current_status": "EXACT_CONDITIONAL_CLOSURE_LAW",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "BND3625_4_variable_coupling_warning",
            "step": "calibrated constants consistency",
            "statement": "Calibrated constants are allowed only if locally constant or if their gradients are included as residual source terms.",
            "formula": "nabla_m[kappa_eff T^{mn}] = (nabla_m kappa_eff)T^{mn}+kappa_eff nabla_m T^{mn}",
            "derived_effect": "G_eff/alpha_eff calibration is safe; Gdot/alpha_dot drift is not silently ignorable",
            "current_status": "CONSERVATION_WARNING_WRITTEN",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "BND3625_5_necessary_not_sufficient",
            "step": "closure limit",
            "statement": "Bianchi closure is necessary for consistency but does not prove local GR; a conserved nonzero residual can still fail PPN/Newton tests.",
            "formula": "nabla_m DeltaR^{mn}=0 does not imply DeltaR^{mn}=0",
            "derived_effect": "if closure is conditional, fallback must be a no-cancellation PPN/Newton envelope",
            "current_status": "NO_SMUGGLING_GUARD",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def closure_audit_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": "RCA3625_0_DeltaE",
            "residual_symbol": "DeltaE_MTS_mn",
            "closure_condition": "DeltaE_MTS must be the metric variation of a retained parent sector or a fixed boundary term.",
            "failure_mode": "arbitrary dropped/kept DeltaE breaks Bianchi identity or hides a force term",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "next_needed": "actual local parent L_extra/L_boundary inventory and variation map",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": "RCA3625_1_source_weight",
            "residual_symbol": "DeltaT_source; w_EM; kappa_J; delta_ellJ",
            "closure_condition": "source weights must come from the same Hilbert/Noether current used in the field equation.",
            "failure_mode": "test/source current rescaling creates nonconservation or WEP/GM drift",
            "current_status": "CONDITIONAL_CURRENT_OWNER_NOT_SIGNED",
            "next_needed": "same-current theorem or source-backed WEP/Newton rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": "RCA3625_2_coupling_drift",
            "residual_symbol": "delta_kappa; b_alpha; lambda_F2",
            "closure_condition": "calibrated constants must be locally constant or their gradients must be represented as residual fields.",
            "failure_mode": "Gdot/alpha_dot terms sneak into conservation and clock/GM observables",
            "current_status": "DRIFT_BOUND_REQUIRED",
            "next_needed": "d kappa_eff=0 theorem or clock/Gdot/alpha_dot envelope rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": "RCA3625_3_q_loc",
            "residual_symbol": "q_loc^nu",
            "closure_condition": "q_loc must appear as a Ward-balanced force/current term or be zero in the local vacuum branch.",
            "failure_mode": "q_loc=0 alone may not kill homogeneous stress; q_loc nonzero maps to PPN/R10/clock/orbit residuals",
            "current_status": "WARD_ZERO_OR_PROJECTION_REQUIRED",
            "next_needed": "derive q_loc Ward zero or fill projection coefficients",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": "RCA3625_4_GK_stress",
            "residual_symbol": "T_GK_mn; T_tau/P_mn",
            "closure_condition": "extra-sector stress must be zero, pure gauge, exponentially suppressed, or explicitly bounded.",
            "failure_mode": "conserved but nonzero stress can still change gamma/beta/orbits",
            "current_status": "BIANCHI_CLOSURE_NOT_ENOUGH",
            "next_needed": "positive/no-hair/stealth theorem or stress-norm bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": "RCA3625_5_boundary_PiM",
            "residual_symbol": "delta_PiM; Phi_EM_boundary; Q_boundary",
            "closure_condition": "boundary and readout terms must be fixed before readout and included in the Noether charge balance.",
            "failure_mode": "mass/GM can be laundered through the boundary/reference subtraction",
            "current_status": "BOUNDARY_FLUX_OR_ZERO_REQUIRED",
            "next_needed": "no-flux worldtube theorem or radiative/source-bound flux row",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": "RCA3625_6_Delta_PPN_abs",
            "residual_symbol": "Delta_PPN_abs",
            "closure_condition": "each PPN/Newton residual component must be independently zeroed or bounded; no cancellation-only pass.",
            "failure_mode": "a conserved residual vector can pass divergence but fail a component bound",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "next_needed": "PPN/Newton component coefficients, bounds, units, and source paths",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def ppn_newton_schema_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "envelope_id": "ENV3625_0_gamma",
            "observable_component": "gamma_minus_1",
            "source_residuals": "DeltaE_MTS; readout/coframe; q_loc; GK_stress",
            "prediction_formula_template": "gamma_minus_1 = K_gamma_DeltaE*Pi_gamma(DeltaE_MTS)+K_gamma_readout*epsilon_readout+K_gamma_q*q_loc_projection",
            "required_bound_source": "PPN gamma comparator row with value, units, citation/source path",
            "current_status": "MISSING_COMPONENT_VALUES_AND_BOUND",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "envelope_id": "ENV3625_1_beta",
            "observable_component": "beta_minus_1",
            "source_residuals": "second-order DeltaE_MTS; source weights; operator tower; readout",
            "prediction_formula_template": "beta_minus_1 = sum_abs(beta_source + beta_operator + beta_readout + beta_boundary)",
            "required_bound_source": "PPN beta/perihelion/LLR comparator row with value, units, citation/source path",
            "current_status": "MISSING_SECOND_ORDER_COMPONENT_VALUES_AND_BOUND",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "envelope_id": "ENV3625_2_preferred_frame",
            "observable_component": "alpha_i; xi",
            "source_residuals": "q_loc; coframe/memory; domain/projector preferred-frame terms",
            "prediction_formula_template": "Delta_PF_abs = |alpha1|+|alpha2|+|alpha3|+|xi| from projected residual basis",
            "required_bound_source": "PPN preferred-frame bounds with component-level rows",
            "current_status": "MISSING_PROJECTION_MATRIX_AND_BOUNDS",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "envelope_id": "ENV3625_3_conservation",
            "observable_component": "zeta_i; Bianchi leakage",
            "source_residuals": "C_B^nu = nabla_m[DeltaE_MTS^{mn}-kappa DeltaT_MTS^{mn}]",
            "prediction_formula_template": "Delta_cons_abs = |Pi_zeta(C_B)| + |Pi_orbit(C_B)|",
            "required_bound_source": "PPN conservation/nonconservation or orbital energy-balance comparator rows",
            "current_status": "MISSING_C_B_VALUE_AND_PROJECTION",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "envelope_id": "ENV3625_4_Newton_Poisson",
            "observable_component": "delta_Newton_MTS",
            "source_residuals": "DeltaE_00; delta_kappa; delta_source; PiM_boundary",
            "prediction_formula_template": "nabla^2 Phi - 4*pi*G_eff*rho_H = Pi_00(DeltaE_MTS)-4*pi*G_eff*delta_rho_source+boundary",
            "required_bound_source": "Newton/GM/Cavendish/ephemeris residual bound rows",
            "current_status": "MISSING_SOURCE_MASS_CLOSURE_AND_BOUND",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "envelope_id": "ENV3625_5_EM_source",
            "observable_component": "w_EM; Phi_EM_boundary",
            "source_residuals": "EM Hilbert source weight; Poynting/boundary flux",
            "prediction_formula_template": "Delta_EM_source_abs = |w_EM|*f_EM + |Phi_EM_boundary|/M_H_ref",
            "required_bound_source": "WEP/clock/orbital-radiative flux rows with EM fraction or H_tau normalization",
            "current_status": "MISSING_EM_FRACTION_OR_FLUX_NORMALIZATION",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "envelope_id": "ENV3625_6_total",
            "observable_component": "Delta_local_GR_total_abs",
            "source_residuals": "all 3625 envelope rows",
            "prediction_formula_template": "Delta_total_abs = sum_abs(ENV3625_0..ENV3625_5); pass only if each component has theorem-zero or numeric bound pass",
            "required_bound_source": "component-complete local-GR envelope",
            "current_status": "RUNNER_SCHEMA_READY_INPUTS_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def smoke_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "smoke_id": f"SMOKE3625_{index}",
            "envelope_id": row["envelope_id"],
            "observable_component": row["observable_component"],
            "predicted_value": "MISSING_COMPONENT_VALUE",
            "bound_value": "MISSING_BOUND_VALUE",
            "units": "MISSING_UNITS",
            "source_path": "MISSING_SOURCE_PATH",
            "runner_verdict": "BLOCKED_NOT_SCORED",
            "reason": row["current_status"],
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for index, row in enumerate(ppn_newton_schema_rows())
    ]


def decision_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3625_0_bianchi_result",
            "decision": "Bianchi closure has an exact conditional derivation from a single diffeomorphism-invariant parent action, but current MTS has not signed the parent action/Euler/boundary package.",
            "status": "CONDITIONAL_DERIVATION_NOT_CLAIM",
            "next_action": "derive actual local parent residual Lagrangian inventory or keep C_B^nu as a bounded residual",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3625_1_closure_not_silence",
            "decision": "A divergence-closed residual is not necessarily zero; local-GR still requires PPN/Newton component silence or bounds.",
            "status": "NO_SMUGGLING_GUARD",
            "next_action": "do not treat Bianchi closure as a local-GR pass",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3625_2_envelope_result",
            "decision": "The first PPN/Newton envelope schema and smoke rows now exist, but all numeric/source inputs remain missing and nonclaim.",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "next_action": "fill component rows in the least-scrutiny order: Bianchi C_B, beta, gamma/readout, Newton source mass, EM source/boundary",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3625_3_next_target",
            "decision": "Next checkpoint should attempt the parent local residual Lagrangian inventory, because it can close Bianchi and populate residual components from one source.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3626-Y5-R2FR-local-residual-Lagrangian-inventory-or-PPN-component-fill.md",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS3625_0",
            "result": "BIANCHI_CONDITIONAL_DERIVATION_AND_PPN_ENVELOPE_SCHEMA_WRITTEN_NO_CLAIM",
            "summary": "3625 derives the conditional Noether/Bianchi residual closure law and builds a first nonclaim PPN/Newton envelope schema; local-GR remains unclaimed because parent action/Euler/boundary signatures and numeric component rows are missing.",
            "bianchi_conditional_derivation": True,
            "ppn_newton_envelope_schema": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3625_0",
            "target_doc": "3626-Y5-R2FR-local-residual-Lagrangian-inventory-or-PPN-component-fill.md",
            "target_script": "scripts/Y5_R2FR_3626_local_residual_Lagrangian_inventory_or_PPN_component_fill.py",
            "objective": "construct the actual retained local residual Lagrangian/source inventory that would make the Bianchi identity concrete, or fill the first PPN/Newton component rows with source-backed values/bounds",
            "success_gate": "each residual in RV3624 has a parent Lagrangian/Euler/boundary owner or a component-level nonclaim PPN/Newton row with value, units, bound, source path, and no-cancellation guard",
            "reason": "Bianchi closure now says exactly what must be owned; the next leap is to attach each residual to an actual Lagrangian piece or empirical component row.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    status = status_rows()[0]
    return [
        {
            "timestamp_utc": status["timestamp_utc"],
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "Bianchi_route": "EXACT_CONDITIONAL_PARENT_NOETHER_IDENTITY_NOT_SIGNED",
            "closure_law": "nabla_m[DeltaE_MTS-kappa_eff_DeltaT_MTS]=C_B",
            "PPN_envelope": "SCHEMA_READY_VALUES_MISSING",
            "local_GR_claim": "NO_CLAIM",
            "next_pressure_point": "local_residual_Lagrangian_inventory_or_component_fill",
            "valid_for_claim": False,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def write_markdown() -> None:
    sources = source_register_rows()
    derivation = bianchi_derivation_rows()
    closure = closure_audit_rows()
    schema = ppn_newton_schema_rows()
    smoke = smoke_rows()
    decisions = decision_gate_rows()
    status = status_rows()
    next_target = next_target_rows()
    content = f"""# 3625 Y5 R2FR Bianchi residual closure or first PPN envelope runner

**Status:** {status[0]["summary"]}

**Claim ceiling:** no local-GR, Newton, PPN, WEP, R10/R11, Maxwell-source, or conservation pass is claimed from 3625.

## Core result

The Bianchi route is real but conditional:

```text
single diffeomorphism-invariant parent action
  -> parent Noether identity
  -> residual closure law
  -> nabla_m[DeltaE_MTS^{{mn}} - kappa_eff DeltaT_MTS^{{mn}}] = C_B^n
```

`C_B^n=0` only follows when the actual parent Euler equations, source current, and boundary/no-flux terms are signed. Even then, closure is necessary but not sufficient: a conserved nonzero residual can still fail `gamma`, `beta`, preferred-frame, Newton/source, clock, or orbital tests.

## Source register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Bianchi / Noether derivation

{markdown_table(derivation, ["derivation_id", "step", "formula", "derived_effect", "current_status"])}

## Residual closure audit

{markdown_table(closure, ["audit_id", "residual_symbol", "closure_condition", "failure_mode", "current_status"])}

## PPN / Newton envelope schema

{markdown_table(schema, ["envelope_id", "observable_component", "prediction_formula_template", "current_status"])}

## Nonclaim smoke rows

{markdown_table(smoke, ["smoke_id", "envelope_id", "predicted_value", "bound_value", "runner_verdict", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "status", "next_action"])}

## Next target

{markdown_table(next_target, ["target_doc", "target_script", "objective", "success_gate"])}
"""
    DOC.write_text(content, encoding="utf-8")


def validate() -> list[dict[str, object]]:
    timestamp = utc_now()
    paths = output_paths()
    pre_validation = {key: path for key, path in paths.items() if key != "validation"}
    sources = source_register_rows()
    derivation = bianchi_derivation_rows()
    closure = closure_audit_rows()
    schema = ppn_newton_schema_rows()
    smoke = smoke_rows()
    decisions = decision_gate_rows()
    status = status_rows()
    next_target = next_target_rows()

    results: list[tuple[str, bool, str]] = []
    missing_sources = [row["path"] for row in sources if not row["exists"]]
    results.append(("VAL3625_0_sources_exist", not missing_sources, "all sources exist" if not missing_sources else "; ".join(missing_sources)))
    missing_needles = [row["source_id"] for row in sources if not row["needle_found"]]
    results.append(("VAL3625_1_needles_found", not missing_needles, "all source anchors found" if not missing_needles else "; ".join(missing_needles)))
    missing_outputs = [key for key, path in pre_validation.items() if not path.exists()]
    results.append(("VAL3625_2_outputs_exist", not missing_outputs, "all pre-validation outputs written" if not missing_outputs else "; ".join(missing_outputs)))

    parse_ok = True
    parse_details: list[str] = []
    for key, path in pre_validation.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            rows = read_csv(path)
            parse_details.append(f"{key}:{len(rows)}")
            if not rows:
                parse_ok = False
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{key}:{exc}")
    results.append(("VAL3625_3_csv_parse", parse_ok, "; ".join(parse_details)))

    identity_ok = any("nabla_m(2E_g" in row["derived_effect"] for row in derivation)
    results.append(("VAL3625_4_noether_identity_written", identity_ok, "Noether/Bianchi identity row written"))
    closure_law_ok = any("nabla_m[DeltaE_MTS" in row["formula"] for row in derivation)
    results.append(("VAL3625_5_residual_closure_law_written", closure_law_ok, "residual closure law written"))
    necessary_guard_ok = any(row["derivation_id"] == "BND3625_5_necessary_not_sufficient" for row in derivation)
    results.append(("VAL3625_6_closure_not_silence_guard", necessary_guard_ok, "Bianchi closure not treated as silence"))
    schema_components = {row["observable_component"] for row in schema}
    expected_components = {"gamma_minus_1", "beta_minus_1", "alpha_i; xi", "zeta_i; Bianchi leakage", "delta_Newton_MTS", "w_EM; Phi_EM_boundary", "Delta_local_GR_total_abs"}
    results.append(("VAL3625_7_envelope_components", expected_components.issubset(schema_components), "PPN/Newton/EM envelope components written"))
    smoke_blocked = all(row["runner_verdict"] == "BLOCKED_NOT_SCORED" and row["score_ready"] is False and row["valid_for_claim"] is False for row in smoke)
    results.append(("VAL3625_8_smoke_rows_blocked", smoke_blocked, "all smoke rows remain blocked/nonclaim"))
    all_nonclaim = all(row.get("claim_allowed") is False and row.get("valid_for_claim") is False for collection in [derivation, closure, schema, smoke, decisions, status, next_target] for row in collection)
    results.append(("VAL3625_9_all_outputs_nonclaim", all_nonclaim, "all outputs remain nonclaim"))

    if FORMALIZATION.exists():
        leaked_paths = list(FORMALIZATION.rglob("*3625*"))
        formalization_clean = len(leaked_paths) == 0
        detail = "no 3625 files in formalization-workbench" if formalization_clean else "; ".join(str(path) for path in leaked_paths[:5])
    else:
        formalization_clean = True
        detail = "formalization-workbench not present"
    results.append(("VAL3625_10_no_formalization_leak", formalization_clean, detail))

    next_ok = next_target[0]["target_doc"] == "3626-Y5-R2FR-local-residual-Lagrangian-inventory-or-PPN-component-fill.md"
    results.append(("VAL3625_11_next_target_written", next_ok, "3626 Lagrangian inventory/component fill selected"))

    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in results
    ]


def main() -> None:
    paths = output_paths()
    write_csv(paths["source_register"], source_register_rows())
    write_csv(paths["bianchi_derivation"], bianchi_derivation_rows())
    write_csv(paths["closure_audit"], closure_audit_rows())
    write_csv(paths["ppn_newton_schema"], ppn_newton_schema_rows())
    write_csv(paths["smoke_rows"], smoke_rows())
    write_csv(paths["decision_gates"], decision_gate_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_csv(paths["canonical_status"], canonical_status_rows())
    write_markdown()
    write_csv(paths["validation"], validate())

    failed = [row for row in read_csv(paths["validation"]) if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3625 validation failed: {failed}")
    print(f"wrote 3625 checkpoint with {len(read_csv(paths['validation']))} validation checks")


if __name__ == "__main__":
    main()
