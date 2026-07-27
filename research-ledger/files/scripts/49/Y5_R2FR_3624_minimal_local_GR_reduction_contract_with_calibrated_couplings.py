from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3624"
BRANCH_ID = "MTS_R2FR_Y5_MINIMAL_LOCAL_GR_REDUCTION_CONTRACT_WITH_CALIBRATED_COUPLINGS_3624"
DOC = ROOT / "3624-Y5-R2FR-minimal-local-GR-reduction-contract-with-calibrated-couplings.md"


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
        "source_register": RESIDUALS / "P8_Y5_R2FR_3624_SOURCE_REGISTER.csv",
        "local_gr_contract": RESIDUALS / "P8_Y5_R2FR_3624_MINIMAL_LOCAL_GR_CONTRACT.csv",
        "calibrated_constants": RESIDUALS / "P8_Y5_R2FR_3624_CALIBRATED_CONSTANTS_LEDGER.csv",
        "residual_vector": RESIDUALS / "P8_Y5_R2FR_3624_EXPLICIT_MTS_RESIDUAL_VECTOR.csv",
        "newton_ppn_gates": RESIDUALS / "P8_Y5_R2FR_3624_NEWTON_PPN_COMPLETION_GATES.csv",
        "maxwell_hilbert_gates": RESIDUALS / "P8_Y5_R2FR_3624_MAXWELL_HILBERT_STRESS_GATES.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3624_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3624_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3624_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_minimal_local_GR_contract_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3624_VALIDATION.csv",
    }


def source_map() -> list[dict[str, str]]:
    return [
        {
            "source_id": "handoff_3623",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3623_NEXT_TARGET.csv"),
            "needle": "minimal-local-GR-reduction-contract",
            "role": "3623 selected calibrated-coupling local-GR contract.",
        },
        {
            "source_id": "gr_constant_3623",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3623_GR_G_CONSTANT_ANALOGY.csv"),
            "needle": "S_EH=(16*pi*G)^-1",
            "role": "GR/Newton constant analogy: measured constants are acceptable at reduction stage.",
        },
        {
            "source_id": "coupling_no_go_3623",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3623_COUPLING_SCALING_NO_GO.csv"),
            "needle": "alpha_Q=Q_*^2/(4*pi*Z_Q)",
            "role": "EM coupling ratio/no-go source.",
        },
        {
            "source_id": "wem_phi_3623",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3623_WEM_PHI_SOURCE_THEOREM.csv"),
            "needle": "T_EM^{0i}=S_Poynting^i/c^2",
            "role": "Poynting and EM Hilbert stress split.",
        },
        {
            "source_id": "motion_load_02",
            "path": str(ROOT / "02-motion-load-local-GR-reduction.md"),
            "needle": "motion_load_local_GR_reduction_conditional_not_promoted",
            "role": "early motion-load local-GR conditional status.",
        },
        {
            "source_id": "observer_contract_10",
            "path": str(ROOT / "10-observer-map-symplectic-contract.md"),
            "needle": "Bianchi-like consistency identity",
            "role": "older no-smuggling PPN/conservation completion requirements.",
        },
        {
            "source_id": "min_parent_action_511",
            "path": str(RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"),
            "needle": "S_EH",
            "role": "minimum parent local-GR action blocks.",
        },
        {
            "source_id": "min_parent_residual_511",
            "path": str(RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_RESIDUAL_VECTOR.csv"),
            "needle": "AR511_7_metric_PPN_tail",
            "role": "prior local-GR residual vector.",
        },
        {
            "source_id": "einstein_lhs_2619",
            "path": str(RESIDUALS / "P8_Y5_GR_LEFT_HAND_GATE_2619_EINSTEIN_LEFT_HAND_LIMIT_ATTEMPT.csv"),
            "needle": "ELH2619_3_residual_decomposition",
            "role": "Einstein left-hand residual decomposition.",
        },
        {
            "source_id": "newton_2619",
            "path": str(RESIDUALS / "P8_Y5_GR_LEFT_HAND_GATE_2619_NEWTON_POISSON_WEAK_FIELD_ATTEMPT.csv"),
            "needle": "NWF2619_1_poisson_conditional",
            "role": "Newton/Poisson weak-field conditional bridge.",
        },
        {
            "source_id": "operator_pack_2619",
            "path": str(RESIDUALS / "P8_Y5_GR_LEFT_HAND_GATE_2619_OPERATOR_RESIDUAL_PACK.csv"),
            "needle": "ORP2619_8_nonclaim_lock",
            "role": "operator residual pack and nonclaim lock.",
        },
        {
            "source_id": "eh_envelope_2579",
            "path": str(RESIDUALS / "P8_Y5_EH_DESCENT_COUPLING_PIM_2579_LOCAL_GR_RESIDUAL_ENVELOPE.csv"),
            "needle": "ENV2579_9_total",
            "role": "absolute local-GR residual envelope.",
        },
        {
            "source_id": "ppn_interface_2636",
            "path": str(RESIDUALS / "P8_Y5_GENERATOR_EFFECTIVE_PACK_2636_PPN_INTERFACE_MAP.csv"),
            "needle": "PPNI2636_6_total_abs",
            "role": "PPN component interface map.",
        },
        {
            "source_id": "gk_stress_2469",
            "path": str(RESIDUALS / "P8_Y5_GK_STRESS_2469_LOCAL_METRIC_EQUATION_GATE.csv"),
            "needle": "MET2469_2_stealth_reduction",
            "role": "GK stress and local metric equation gate.",
        },
        {
            "source_id": "maxwell_poynting_3463",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv"),
            "needle": "EM3463_2_poynting",
            "role": "Maxwell action, Hilbert stress, Poynting ledger.",
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


def local_gr_contract_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "contract_id": "LGC3624_0_domain",
            "contract_piece": "observed local fields",
            "statement": "The local reduction uses one observed metric/coframe, one observed EM Hodge structure, and one Hilbert source frame.",
            "formula": "Domain_local={g_obs,e_obs,A_Q,psi_matter,Phi_MTS}; readout fixed before tests",
            "required_proof_or_bound": "parent observer/coframe map and no shadow-frame/readout morphism",
            "current_status": "CONTRACT_ONLY",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "contract_id": "LGC3624_1_action_normal_form",
            "contract_piece": "EH plus calibrated constants",
            "statement": "Local MTS may reduce to an Einstein-Hilbert normal form with calibrated low-energy constants rather than deriving their numerical values.",
            "formula": "S_local=(2*kappa_eff)^-1 int sqrt(-g)(R-2Lambda_eff)+S_matter+S_EM+S_extra+S_boundary",
            "required_proof_or_bound": "derive EH dominance and show S_extra/S_boundary contribute only explicit zero-or-bound residuals",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "contract_id": "LGC3624_2_metric_equation",
            "contract_piece": "local field equation",
            "statement": "The field equation must be GR plus an explicit MTS residual tensor, never GR plus hidden assumptions.",
            "formula": "G_mn+Lambda_eff g_mn = kappa_eff(T_matter_mn+T_EM_mn)+DeltaE_MTS_mn",
            "required_proof_or_bound": "DeltaE_MTS_mn=0 by theorem or |projection(DeltaE)| below local tests with no-cancellation guard",
            "current_status": "EXPLICIT_RESIDUAL_CONTRACT_WRITTEN",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "contract_id": "LGC3624_3_newton_limit",
            "contract_piece": "Newton/Poisson limit",
            "statement": "Newtonian mechanics is recovered by the weak-field 00 equation with calibrated G_eff and a fixed Hilbert source mass.",
            "formula": "nabla^2 Phi = 4*pi*G_eff*rho_H + delta_Newton_MTS; a=-grad Phi",
            "required_proof_or_bound": "delta_Newton_MTS=0/bounded; rho_H equals measured source charge before orbital fitting",
            "current_status": "CONDITIONAL_TEMPLATE_NOT_CLAIMED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "contract_id": "LGC3624_4_ppn_completion",
            "contract_piece": "PPN/local GR completion",
            "statement": "gamma=1 is insufficient; beta, preferred-frame, conservation, WEP/source, and readout residuals must all close.",
            "formula": "Delta_PPN_abs=|gamma-1|+|beta-1|+|alpha_i|+|zeta_i|+|xi|+readout/source terms",
            "required_proof_or_bound": "each PPN component theorem-zeroed or source-bounded independently; no cancellation-only pass",
            "current_status": "PPN_VECTOR_CONTRACT_WRITTEN",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "contract_id": "LGC3624_5_bianchi_conservation",
            "contract_piece": "Bianchi/conservation compatibility",
            "statement": "Diffeomorphism consistency must hold for the whole retained equation, including MTS residuals and source exchange.",
            "formula": "nabla_m[DeltaE_MTS^{mn}-kappa_eff DeltaT_MTS^{mn}]=0 with nabla_m(T_matter+T_EM+DeltaT_MTS)^{mn}=0",
            "required_proof_or_bound": "parent Noether identity or explicit residual-conservation closure",
            "current_status": "NEXT_DERIVATION_TARGET",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "contract_id": "LGC3624_6_maxwell_stress",
            "contract_piece": "Maxwell/EM stress coupling",
            "statement": "The EM sector may use calibrated alpha_eff, but its Hilbert stress and Poynting flow must couple through the same source slot.",
            "formula": "T_EM^{mn}=-(2/sqrt(-g))delta S_EM/delta g_mn; T_EM^{0i}=S_Poynting^i/c^2",
            "required_proof_or_bound": "observed Hodge/coframe descent, same current owner, w_EM=0/bound, Phi_EM boundary branch",
            "current_status": "CONDITIONAL_STRUCTURE_WRITTEN",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def calibrated_constants_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "constant_id": "CC3624_0_G_eff",
            "constant": "G_eff or kappa_eff",
            "role": "low-energy gravitational coupling in EH/Newton limit",
            "allowed_status": "CALIBRATED_CONSTANT_ALLOWED",
            "formula": "kappa_eff=8*pi*G_eff/c^4; c=1 convention gives kappa_eff=8*pi*G_eff",
            "not_required_at_this_stage": "numerically derive G from pure MTS geometry",
            "still_required": "prove constancy/local drift bound and same source mass rho_H/M_H_ref",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "constant_id": "CC3624_1_alpha_eff",
            "constant": "alpha_eff",
            "role": "low-energy EM coupling/fine-structure input",
            "allowed_status": "CALIBRATED_CONSTANT_ALLOWED",
            "formula": "alpha_eff=Q_*^2/(4*pi*Z_Q)",
            "not_required_at_this_stage": "derive observed alpha without parent Q_* and Z_Q certificate",
            "still_required": "prove no drift/source residual or provide clock/WEP/EM bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "constant_id": "CC3624_2_Lambda_eff",
            "constant": "Lambda_eff",
            "role": "locally negligible/background-subtracted cosmological term",
            "allowed_status": "LOCAL_BACKGROUND_PARAMETER",
            "formula": "G_mn+Lambda_eff g_mn; local compact tests take Lambda_eff*r^2 << tolerance",
            "not_required_at_this_stage": "solve cosmological constant problem inside local-GR reduction",
            "still_required": "do not let Lambda/memory branch fake local source residuals",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "constant_id": "CC3624_3_c_units",
            "constant": "c",
            "role": "conversion between time/space units and null cone structure",
            "allowed_status": "UNIT_AND_CAUSAL_CONVERSION_CONSTANT",
            "formula": "ds^2=-c^2 dt^2+dx^2 locally; often set c=1",
            "not_required_at_this_stage": "rederive the unit conversion before local-GR contract",
            "still_required": "if MTS modifies time-flow interpretation, preserve tested null cone and clock observables",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def residual_vector_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "residual_id": "RV3624_0_DeltaE",
            "symbol": "DeltaE_MTS_mn",
            "definition": "left-hand metric operator deviation from Einstein form",
            "contract": "must vanish by EH dominance/Lovelock/locality theorem or project below PPN/R10/orbital bounds",
            "observable_links": "PPN;R10;orbital;clocks;growth",
            "source_anchor": str(RESIDUALS / "P8_Y5_GR_LEFT_HAND_GATE_2619_OPERATOR_RESIDUAL_PACK.csv"),
            "current_status": "LIVE_ZERO_OR_BOUND_REQUIRED",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "residual_id": "RV3624_1_source_weight",
            "symbol": "DeltaT_source; w_EM; kappa_J; delta_ellJ",
            "definition": "source/test current or EM Hilbert source weighting mismatch",
            "contract": "same Noether/Hilbert source owner or source-backed WEP/Newton/clock bound",
            "observable_links": "WEP;Newton_GM;R10;PPN;clocks",
            "source_anchor": str(RESIDUALS / "P8_Y5_R2FR_3623_WEM_PHI_SOURCE_THEOREM.csv"),
            "current_status": "LIVE_ZERO_OR_BOUND_REQUIRED",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "residual_id": "RV3624_2_coupling_drift",
            "symbol": "delta_kappa; b_alpha; lambda_F2",
            "definition": "drift or unowned normalization in calibrated G_eff/alpha_eff sectors",
            "contract": "calibration allowed, but local drift and independent F2/source coefficients must be zeroed or bounded",
            "observable_links": "Gdot;alpha_dot;clock spectroscopy;WEP",
            "source_anchor": str(RESIDUALS / "P8_Y5_R2FR_3623_COUPLING_SCALING_NO_GO.csv"),
            "current_status": "LIVE_ZERO_OR_BOUND_REQUIRED",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "residual_id": "RV3624_3_q_loc",
            "symbol": "q_loc^nu",
            "definition": "local projected non-GR force/current vector from Gamma/Khat mismatch",
            "contract": "derive Ward/local vacuum zero or map to PPN/R10/clock/orbital components",
            "observable_links": "PPN preferred-frame;R10;clocks;orbital",
            "source_anchor": str(RESIDUALS / "P8_Y5_GAMMAKHAT_QLOC_2581_LOCAL_TEST_MAP.csv"),
            "current_status": "LIVE_ZERO_OR_BOUND_REQUIRED",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "residual_id": "RV3624_4_GK_stress",
            "symbol": "T_GK_mn; T_tau/P_mn",
            "definition": "homogeneous extra-sector stress that can survive even if q_loc=0",
            "contract": "positive/no-hair/stealth theorem or metric Green-function bound",
            "observable_links": "PPN gamma,beta;orbital;R10",
            "source_anchor": str(RESIDUALS / "P8_Y5_GK_STRESS_2469_LOCAL_METRIC_EQUATION_GATE.csv"),
            "current_status": "LIVE_ZERO_OR_BOUND_REQUIRED",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "residual_id": "RV3624_5_PiM_boundary",
            "symbol": "delta_PiM; Phi_EM_boundary; Q_boundary",
            "definition": "readout/source projection or boundary flux mass shift",
            "contract": "fixed-before-readout Pi_M and no-flux/reference theorem or source-backed boundary flux row",
            "observable_links": "Newton_GM;R10;R11;orbital energy",
            "source_anchor": str(RESIDUALS / "P8_Y5_EH_DESCENT_COUPLING_PIM_2579_LOCAL_GR_RESIDUAL_ENVELOPE.csv"),
            "current_status": "LIVE_ZERO_OR_BOUND_REQUIRED",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "residual_id": "RV3624_6_PPN_total",
            "symbol": "Delta_PPN_abs",
            "definition": "absolute no-cancellation envelope over gamma,beta,preferred-frame,conservation,source/readout tails",
            "contract": "no cancellation-only pass; every component independently theorem-zeroed or bounded",
            "observable_links": "all local GR/PPN tests",
            "source_anchor": str(RESIDUALS / "P8_Y5_GENERATOR_EFFECTIVE_PACK_2636_PPN_INTERFACE_MAP.csv"),
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def newton_ppn_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "NPG3624_0_EH_dominance",
            "gate": "Einstein left-hand form",
            "required_result": "E_LHS -> G_mn + Lambda g_mn + explicit DeltaE_MTS_mn",
            "current_status": "CONDITIONAL_NOT_PARENT_PROOF",
            "blocks_claim_if_missing": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "NPG3624_1_Poisson",
            "gate": "Newton/Poisson equation",
            "required_result": "nabla^2 Phi=4*pi*G_eff*rho_H with delta_Newton_MTS=0/bounded",
            "current_status": "CONDITIONAL_TEMPLATE_NOT_PARENT_DERIVED",
            "blocks_claim_if_missing": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "NPG3624_2_Gauss_worldtube",
            "gate": "inverse-square/source mass",
            "required_result": "closed source worldtube gives Phi=-G_eff*M_H/r with M_H fixed before orbital fitting",
            "current_status": "SOURCE_WORLDTUBE_GLUE_OPEN",
            "blocks_claim_if_missing": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "NPG3624_3_gamma",
            "gate": "PPN gamma",
            "required_result": "gamma-1=0 or bounded after reciprocal/readout residuals",
            "current_status": "CONDITIONAL_GAMMA_NOT_ENOUGH",
            "blocks_claim_if_missing": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "NPG3624_4_beta",
            "gate": "PPN beta/nonlinear completion",
            "required_result": "beta-1=0 or bounded from second-order field/readout map",
            "current_status": "OPEN",
            "blocks_claim_if_missing": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "NPG3624_5_bianchi",
            "gate": "Bianchi/conservation",
            "required_result": "residual tensor and source exchange satisfy parent Noether identity",
            "current_status": "NEXT_TARGET",
            "blocks_claim_if_missing": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def maxwell_hilbert_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "MHG3624_0_action",
            "gate": "observed Maxwell action",
            "required_result": "S_EM uses same g_obs/e_obs/Hodge as the local gravitational variation",
            "current_status": "STANDARD_CONDITIONAL_ACTION_FORM",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "MHG3624_1_hilbert_stress",
            "gate": "EM Hilbert stress",
            "required_result": "T_EM_mn is the variational stress entering the same source slot as matter",
            "current_status": "EXACT_FROM_ACTION_CONDITIONAL",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "MHG3624_2_poynting",
            "gate": "Poynting/source-flow identity",
            "required_result": "T_EM^{0i}=S_Poynting^i/c^2 in the local inertial frame",
            "current_status": "EXACT_CONDITIONAL_LOCAL_FRAME_IDENTITY",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3623_WEM_PHI_SOURCE_THEOREM.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "MHG3624_3_exchange",
            "gate": "matter/EM stress exchange",
            "required_result": "nabla_m T_EM^{mn}=-F^{nl}J_l and total matter+EM+MTS stress is conserved",
            "current_status": "CONDITIONAL_ON_CURRENT_OWNER",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "MHG3624_4_w_phi",
            "gate": "EM source-weight/boundary residual",
            "required_result": "w_EM=0/bounded and Phi_EM_boundary stationary-zero or radiative-flux-accounted",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3623_WEM_PHI_SOURCE_THEOREM.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "claim_gate_id": "CG3624_0_calibrated_constants",
            "claim": "using calibrated G_eff and alpha_eff is allowed",
            "gate_status": "PASS_AS_STRATEGY_NOT_PUBLIC_CLAIM",
            "reason": "GR itself measures G; the real test is equation form plus residual suppression.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "claim_gate_id": "CG3624_1_local_GR",
            "claim": "MTS derives local GR",
            "gate_status": "FAIL_CURRENT_CLAIM",
            "reason": "DeltaE_MTS, source/readout, beta, Bianchi, boundary and PPN residuals are not all zeroed or bounded.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "claim_gate_id": "CG3624_2_Newton",
            "claim": "MTS derives Newtonian mechanics",
            "gate_status": "FAIL_CURRENT_CLAIM",
            "reason": "Poisson/Gauss/source-mass closure remains conditional.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "claim_gate_id": "CG3624_3_Maxwell_source",
            "claim": "MTS fully derives Maxwell/EM stress coupling",
            "gate_status": "FAIL_CURRENT_CLAIM_BUT_CONTRACT_SHARP",
            "reason": "Poynting/Hilbert identities are exact once the observed Maxwell action is admitted, but parent Hodge/current/source ownership is not signed.",
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
            "status_id": "STATUS3624_0",
            "result": "MINIMAL_LOCAL_GR_CONTRACT_WRITTEN_NO_CLAIM",
            "summary": "3624 consolidates the local-GR/Newton/Maxwell reduction route: calibrated G_eff and alpha_eff are allowed, but every extra MTS residual is now explicit and must be theorem-zeroed or bounded before any local-GR claim.",
            "calibrated_constants_allowed": True,
            "residual_vector_explicit": True,
            "local_GR_claim_allowed": False,
            "newton_claim_allowed": False,
            "maxwell_source_claim_allowed": False,
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
            "next_id": "NEXT3624_0",
            "target_doc": "3625-Y5-R2FR-Bianchi-residual-closure-or-first-PPN-envelope-runner.md",
            "target_script": "scripts/Y5_R2FR_3625_Bianchi_residual_closure_or_first_PPN_envelope_runner.py",
            "objective": "derive the parent Noether/Bianchi closure for the explicit residual vector, or build the first executable PPN/Newton residual envelope with nonclaim source rows",
            "success_gate": "either nabla_m[DeltaE_MTS-kappa DeltaT_MTS] closes from parent symmetry, or each residual component is mapped to a no-cancellation PPN/Newton bound interface",
            "reason": "Bianchi/conservation is the least optional local-GR gate; without it, residual zeroing can become inconsistent bookkeeping.",
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
            "local_GR_contract": "CALIBRATED_CONSTANTS_PLUS_EXPLICIT_RESIDUAL_VECTOR",
            "G_eff": "CALIBRATED_ALLOWED_CONSTANT_DRIFT_BOUND_REQUIRED",
            "alpha_eff": "CALIBRATED_ALLOWED_CONSTANT_DRIFT_BOUND_REQUIRED",
            "Newton_status": "POISSON_GAUSS_SOURCE_CLOSURE_CONDITIONAL",
            "Maxwell_status": "HILBERT_POYNTING_STRUCTURE_CONDITIONAL_PARENT_OWNERSHIP_OPEN",
            "next_pressure_point": "Bianchi_residual_closure_or_PPN_envelope",
            "claim_status": "NO_CLAIM",
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
    contract = local_gr_contract_rows()
    constants = calibrated_constants_rows()
    residuals = residual_vector_rows()
    newton_ppn = newton_ppn_gate_rows()
    maxwell = maxwell_hilbert_gate_rows()
    claims = claim_gate_rows()
    status = status_rows()
    next_target = next_target_rows()
    content = f"""# 3624 Y5 R2FR minimal local-GR reduction contract with calibrated couplings

**Status:** {status[0]["summary"]}

**Claim ceiling:** this checkpoint does not claim local GR, Newtonian mechanics, Maxwell source ownership, PPN pass, WEP pass, R10/R11 pass, or numerical prediction of `G`/`alpha`.

## Core move

3624 makes the least-smuggled local route explicit:

1. Use calibrated low-energy constants `G_eff`, `alpha_eff`, `Lambda_eff`, and `c` where standard theory also uses measured constants.
2. Derive the **form** of the local equations: Einstein-Hilbert metric equation, Newton/Poisson weak field, Maxwell Hilbert stress, and Poynting source-flow identity.
3. Put every non-GR/MTS contribution into an explicit residual vector.
4. Demand theorem-zero or source-backed bound rows for every residual before any claim.

This is not retreat; it is the cleaner boxing stance. We stop throwing haymakers at constants and make the judges score the actual residuals.

## Source register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Minimal local-GR contract

{markdown_table(contract, ["contract_id", "contract_piece", "formula", "required_proof_or_bound", "current_status"])}

## Calibrated constants ledger

{markdown_table(constants, ["constant_id", "constant", "allowed_status", "formula", "still_required"])}

## Explicit MTS residual vector

{markdown_table(residuals, ["residual_id", "symbol", "contract", "observable_links", "current_status"])}

## Newton / PPN completion gates

{markdown_table(newton_ppn, ["gate_id", "gate", "required_result", "current_status", "blocks_claim_if_missing"])}

## Maxwell / Hilbert stress gates

{markdown_table(maxwell, ["gate_id", "gate", "required_result", "current_status"])}

## Claim gates

{markdown_table(claims, ["claim_gate_id", "claim", "gate_status", "reason"])}

## Next target

{markdown_table(next_target, ["target_doc", "target_script", "objective", "success_gate"])}
"""
    DOC.write_text(content, encoding="utf-8")


def validate() -> list[dict[str, object]]:
    timestamp = utc_now()
    paths = output_paths()
    pre_validation = {key: path for key, path in paths.items() if key != "validation"}
    sources = source_register_rows()
    contract = local_gr_contract_rows()
    constants = calibrated_constants_rows()
    residuals = residual_vector_rows()
    newton_ppn = newton_ppn_gate_rows()
    maxwell = maxwell_hilbert_gate_rows()
    claims = claim_gate_rows()
    status = status_rows()
    next_target = next_target_rows()

    results: list[tuple[str, bool, str]] = []
    missing_sources = [row["path"] for row in sources if not row["exists"]]
    results.append(("VAL3624_0_sources_exist", not missing_sources, "all sources exist" if not missing_sources else "; ".join(missing_sources)))
    missing_needles = [row["source_id"] for row in sources if not row["needle_found"]]
    results.append(("VAL3624_1_needles_found", not missing_needles, "all source anchors found" if not missing_needles else "; ".join(missing_needles)))
    missing_outputs = [key for key, path in pre_validation.items() if not path.exists()]
    results.append(("VAL3624_2_outputs_exist", not missing_outputs, "all pre-validation outputs written" if not missing_outputs else "; ".join(missing_outputs)))

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
    results.append(("VAL3624_3_csv_parse", parse_ok, "; ".join(parse_details)))

    calibrated_ok = any(row["constant"] == "G_eff or kappa_eff" for row in constants) and any(row["constant"] == "alpha_eff" for row in constants)
    results.append(("VAL3624_4_calibrated_constants_written", calibrated_ok, "G_eff and alpha_eff calibrated constant rows written"))
    residual_ok = len(residuals) >= 7 and any(row["symbol"] == "Delta_PPN_abs" for row in residuals)
    results.append(("VAL3624_5_residual_vector_explicit", residual_ok, "explicit residual vector includes PPN no-cancellation envelope"))
    bianchi_ok = any(row["contract_id"] == "LGC3624_5_bianchi_conservation" for row in contract) and any(row["gate_id"] == "NPG3624_5_bianchi" for row in newton_ppn)
    results.append(("VAL3624_6_bianchi_gate_written", bianchi_ok, "Bianchi/conservation gate written"))
    poynting_ok = any("T_EM^{0i}=S_Poynting^i/c^2" in row["required_result"] for row in maxwell)
    results.append(("VAL3624_7_poynting_gate_written", poynting_ok, "Poynting source-flow gate written"))
    claim_lock_ok = all(row["claim_allowed"] is False and row["valid_for_claim"] is False for collection in [contract, constants, residuals, newton_ppn, maxwell, claims, status, next_target] for row in collection)
    results.append(("VAL3624_8_all_outputs_nonclaim", claim_lock_ok, "all generated outputs remain nonclaim"))
    local_claim_false = any(row["claim_gate_id"] == "CG3624_1_local_GR" and row["gate_status"] == "FAIL_CURRENT_CLAIM" for row in claims)
    results.append(("VAL3624_9_local_GR_claim_blocked", local_claim_false, "local-GR claim remains blocked"))

    if FORMALIZATION.exists():
        leaked_paths = list(FORMALIZATION.rglob("*3624*"))
        formalization_clean = len(leaked_paths) == 0
        formalization_detail = "no 3624 files in formalization-workbench" if formalization_clean else "; ".join(str(path) for path in leaked_paths[:5])
    else:
        formalization_clean = True
        formalization_detail = "formalization-workbench not present"
    results.append(("VAL3624_10_no_formalization_leak", formalization_clean, formalization_detail))

    next_ok = next_target[0]["target_doc"] == "3625-Y5-R2FR-Bianchi-residual-closure-or-first-PPN-envelope-runner.md"
    results.append(("VAL3624_11_next_target_written", next_ok, "3625 Bianchi/residual envelope target written"))

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
    write_csv(paths["local_gr_contract"], local_gr_contract_rows())
    write_csv(paths["calibrated_constants"], calibrated_constants_rows())
    write_csv(paths["residual_vector"], residual_vector_rows())
    write_csv(paths["newton_ppn_gates"], newton_ppn_gate_rows())
    write_csv(paths["maxwell_hilbert_gates"], maxwell_hilbert_gate_rows())
    write_csv(paths["claim_gates"], claim_gate_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_csv(paths["canonical_status"], canonical_status_rows())
    write_markdown()
    write_csv(paths["validation"], validate())

    failed = [row for row in read_csv(paths["validation"]) if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3624 validation failed: {failed}")
    print(f"wrote 3624 checkpoint with {len(read_csv(paths['validation']))} validation checks")


if __name__ == "__main__":
    main()
