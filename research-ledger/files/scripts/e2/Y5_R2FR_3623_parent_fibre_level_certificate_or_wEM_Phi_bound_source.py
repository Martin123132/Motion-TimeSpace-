from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3623"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_FIBRE_LEVEL_CERTIFICATE_OR_WEM_PHI_BOUND_SOURCE_3623"
DOC = ROOT / "3623-Y5-R2FR-parent-fibre-level-certificate-or-wEM-Phi-bound-source.md"


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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def output_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3623_SOURCE_REGISTER.csv",
        "parent_level_certificate": RESIDUALS / "P8_Y5_R2FR_3623_PARENT_FIBRE_LEVEL_CERTIFICATE.csv",
        "scaling_no_go": RESIDUALS / "P8_Y5_R2FR_3623_COUPLING_SCALING_NO_GO.csv",
        "wem_phi_theorem": RESIDUALS / "P8_Y5_R2FR_3623_WEM_PHI_SOURCE_THEOREM.csv",
        "gr_g_analogy": RESIDUALS / "P8_Y5_R2FR_3623_GR_G_CONSTANT_ANALOGY.csv",
        "bound_source_rows": RESIDUALS / "P8_Y5_R2FR_3623_WEM_PHI_BOUND_SOURCE_ROWS.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3623_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3623_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3623_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_parent_level_coupling_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3623_VALIDATION.csv",
    }


def source_map() -> list[dict[str, str]]:
    items = [
        (
            "handoff_3622",
            RESIDUALS / "P8_Y5_R2FR_3622_NEXT_TARGET.csv",
            "parent fibre metric, level, lattice index",
            "3622 selected the parent-fibre-level certificate as next pressure point.",
        ),
        (
            "theorem_3622",
            RESIDUALS / "P8_Y5_R2FR_3622_TQ_NQ_FIBRE_METRIC_THEOREM.csv",
            "N_Q=G_P(T_Q,T_Q)",
            "3622 exact conditional T_Q/N_Q route.",
        ),
        (
            "countermodel_3622",
            RESIDUALS / "P8_Y5_R2FR_3622_TQ_RESCALE_COUNTERMODEL_AUDIT.csv",
            "Z_Q=C_P N_Q + lambda_F2",
            "3622 retained the rescaling and independent F2 countermodels.",
        ),
        (
            "acquisition_3622",
            RESIDUALS / "P8_Y5_R2FR_3622_WEM_PHI_BOUND_ACQUISITION_LEDGER.csv",
            "MISSING_DIRECT_NUMERIC_BOUND",
            "3622 staged w_EM and Phi_EM_boundary acquisition without scoring.",
        ),
        (
            "fibre_metric_609",
            RESIDUALS / "P8_Y5_R10_609_FIBRE_METRIC_OWNERSHIP.csv",
            "FM609_3_metric_verdict",
            "Prior fibre-metric ownership gate.",
        ),
        (
            "tq_signature_1100",
            RESIDUALS / "P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv",
            "TQS1100_2_fixed_generator_norm",
            "Prior T_Q gauge norm signature audit.",
        ),
        (
            "tq_theorem_1100",
            RESIDUALS / "P8_Y5_R10_1100_TQ_THEOREM_ATTEMPT.csv",
            "TQT1100_2_rescaling_countermodel",
            "Prior T_Q theorem/countermodel attempt.",
        ),
        (
            "noether_3291",
            RESIDUALS / "P8_Y5_R2FR_3291_TQ_NOETHER_OWNER_LEMMA.csv",
            "TQN3291_1_minimal_coupling_variation",
            "Noether current owner route.",
        ),
        (
            "poynting_3463",
            RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv",
            "EM3463_2_poynting",
            "Poynting/stress-energy source ledger.",
        ),
        (
            "common_scale_runner",
            RESIDUALS / "P8_EM_common_scale_bound_runner_results.csv",
            "UCRUN3510_1_Newton_GM",
            "Existing common-scale bound runner remains input-blocked.",
        ),
        (
            "charge_lattice_885",
            RESIDUALS / "P8_Y5_R10_885_CHARGE_LATTICE_ATTEMPT.csv",
            "CL885_5_lattice_verdict",
            "Charge lattice attempt: relative labels not absolute coupling.",
        ),
        (
            "bf_lattice_926",
            RESIDUALS / "P8_Y5_R10_926_BF_LATTICE_THEOREM_ATTEMPT.csv",
            "BF926_4_ratio_lattice",
            "BF/lattice theorem attempt.",
        ),
    ]
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "needle": needle,
            "needle_found": path.exists() and contains(path, needle),
            "role": role,
            "valid_for_claim": False,
        }
        for source_id, path, needle, role in items
    ]


def source_register_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
            "claim_allowed": False,
        }
        for row in source_map()
    ]


def parent_level_certificate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    source_3622 = RESIDUALS / "P8_Y5_R2FR_3622_TQ_NQ_FIBRE_METRIC_THEOREM.csv"
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "certificate_id": "PLC3623_0_parent_bundle",
            "piece": "visible U(1) direction",
            "certificate_clause": "A parent principal/gauge bundle contains a compact visible generator T_Q selected before readout.",
            "formula": "A_parent = A_Q T_Q + A_perp; exp(2*pi*T_Q)=1",
            "what_it_fixes": "relative charge labels and the visible direction in field space",
            "current_status": "RELATIVE_LABELS_ONLY",
            "source_path": str(source_3622),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "certificate_id": "PLC3623_1_parent_level_metric",
            "piece": "kinetic norm / level",
            "certificate_clause": "A nonrescalable parent fibre metric, trace, symplectic level, or lattice index fixes the Q norm.",
            "formula": "N_Q=G_P(T_Q,T_Q); Z_Q=C_P N_Q",
            "what_it_fixes": "Maxwell kinetic normalization inherited from the parent action",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "source_path": str(source_3622),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "certificate_id": "PLC3623_2_charge_unit",
            "piece": "absolute charge/current unit",
            "certificate_clause": "The observed base charge unit Q_* must be tied to the same parent representation normalization, not fitted after readout.",
            "formula": "q_A=n_A Q_*; alpha_Q=Q_*^2/(4*pi*Z_Q)",
            "what_it_fixes": "fine-structure/current calibration if Q_* and Z_Q are jointly owned",
            "current_status": "MISSING_PARENT_QSTAR_CERTIFICATE",
            "source_path": str(RESIDUALS / "P8_Y5_R10_885_CHARGE_LATTICE_ATTEMPT.csv"),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "certificate_id": "PLC3623_3_unique_F2_domain",
            "piece": "no independent visible F_Q^2",
            "certificate_clause": "The local visible EM action domain must forbid a separate lambda_F2 counterterm.",
            "formula": "S_EM^local = -Z_Q/4 int F_Q wedge *F_Q; no +lambda_F2 F_Q^2",
            "what_it_fixes": "prevents b_alpha/lambda_F2 reopening after a parent norm is found",
            "current_status": "DOMAIN_EXHAUSTION_UNSIGNED",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3622_TQ_RESCALE_COUNTERMODEL_AUDIT.csv"),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "certificate_id": "PLC3623_4_same_Noether_source",
            "piece": "source/current owner",
            "certificate_clause": "The current that sources A_Q and the current used in tests must be the same Noether current.",
            "formula": "J_Q=delta S_matter/delta A_Q; no J_Q^readout=(1+kappa_J)J_Q",
            "what_it_fixes": "source/test current calibration and WEP/R10 current residual",
            "current_status": "EXACT_CONDITIONAL_CURRENT_OWNER",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3291_TQ_NOETHER_OWNER_LEMMA.csv"),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "certificate_id": "PLC3623_5_coupling_certificate",
            "piece": "minimal coupling closure",
            "certificate_clause": "Only the joint certificate fixes alpha/current/source calibration; compact charge labels alone do not.",
            "formula": "compact_TQ && fixed_G_P_level && fixed_Q_* && unique_F2 && same_J_Q => D_v alpha_Q=D_v J_Q=0",
            "what_it_fixes": "lambda_F2, b_alpha norm branch, kappa_J, and source-scale drift",
            "current_status": "JOINT_CERTIFICATE_NOT_PARENT_SIGNED",
            "source_path": str(source_3622),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def scaling_no_go_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "no_go_id": "SNG3623_0_canonical_rescale",
            "statement": "A Maxwell sector with unfixed Z_Q has a canonical-field rescaling that moves the coupling without changing the formal field equations.",
            "formula": "S=-Z_Q/4 int F^2 + int A J; A_c=sqrt(Z_Q)A; g_eff=Q_*/sqrt(Z_Q)",
            "consequence": "alpha_Q=Q_*^2/(4*pi*Z_Q) is not predicted until Q_* and Z_Q are jointly parent-owned.",
            "status": "NO_GO_PROVED_FOR_CURRENT_UNSIGNED_CERTIFICATE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "no_go_id": "SNG3623_1_compactness_not_alpha",
            "statement": "Compact U(1) fixes integer charge ratios, not the numerical value of the fine-structure constant.",
            "formula": "n_A in Z does not determine Q_*^2/Z_Q",
            "consequence": "charge quantization is useful structure but cannot by itself close EM calibration.",
            "status": "COUNTERMODEL_RETAINED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "no_go_id": "SNG3623_2_independent_F2_escape",
            "statement": "Even a fixed parent norm fails to predict the observed coupling if an independent local F_Q^2 coefficient is allowed.",
            "formula": "Z_obs=C_P N_Q + lambda_F2",
            "consequence": "the no-extra-F2 domain theorem is mandatory, not cosmetic.",
            "status": "NO_GO_UNLESS_DOMAIN_EXHAUSTION_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "no_go_id": "SNG3623_3_current_readout_escape",
            "statement": "A post-Noether current morphism reopens source coupling even if the kinetic coefficient is fixed.",
            "formula": "J_readout=(1+kappa_J)J_Noether",
            "consequence": "same-current ownership must be signed beside the kinetic certificate.",
            "status": "NO_GO_UNLESS_CURRENT_OWNER_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def wem_phi_theorem_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    source = RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv"
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "WPT3623_0_Hilbert_weight_zero",
            "object": "w_EM",
            "conditional_theorem": "If the observed EM action is the same action varied in the gravitational/Hilbert equation, no separate EM source weight exists.",
            "formula": "T_EM^{mu nu}=-(2/sqrt(-g)) delta S_EM/delta g_mu_nu; G_mu_nu=8*pi*G(T_matter+T_EM)",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "missing_piece": "parent proof that observed Hodge/coframe and gravitational variation use the same local action object",
            "source_path": str(source),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "WPT3623_1_Poynting_source_identity",
            "object": "Poynting / EM momentum source",
            "conditional_theorem": "Poynting transport is already a component of EM stress-current, so it is the right place to look for coupling leakage.",
            "formula": "T_EM^{0i}=S_Poynting^i/c^2; S_Poynting=E x H",
            "current_status": "EXACT_CONDITIONAL_LOCAL_FRAME_IDENTITY",
            "missing_piece": "derive the observed EM Hodge/flow rule from the MTS parent rather than importing Maxwell form",
            "source_path": str(source),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "WPT3623_2_boundary_flux_zero",
            "object": "Phi_EM_boundary",
            "conditional_theorem": "For stationary compact local sources with no radiative flux through the chosen worldtube boundary, EM boundary leakage is zero rather than fitted.",
            "formula": "Phi_EM[partial W]=int_{partial W} T_EM^{mu nu} tau_nu dSigma_mu = 0 if L_tau fields=0 and S_Poynting.n=0",
            "current_status": "EXACT_CONDITIONAL_STATIONARY_BRANCH",
            "missing_piece": "parent-owned stationary worldtube/readout surface and H_tau normalization",
            "source_path": str(source),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "WPT3623_3_radiative_branch",
            "object": "Phi_EM_boundary",
            "conditional_theorem": "For radiative systems Phi_EM_boundary is not zero; it must equal the observed EM flux contribution and be included in energy balance.",
            "formula": "Delta H_tau = -int dt int_{S_R} S_Poynting.n dA + work/source terms",
            "current_status": "RADIATIVE_BRANCH_REQUIRES_NUMERIC_FLUX_SOURCE",
            "missing_piece": "source-backed radiative flux/H_tau conversion row",
            "source_path": str(source),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def gr_g_analogy_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": "GGA3623_0_GR_constant",
            "point": "GR does not derive Newton's constant from pure geometry; it places G in the Einstein-Hilbert coefficient and measures it.",
            "formula": "S_EH=(16*pi*G)^-1 int sqrt(-g) R",
            "impact_for_MTS": "MTS can still be a serious local-GR reduction if it derives the Einstein-Hilbert form and treats G_eff as a calibrated low-energy constant.",
            "status": "FRAMEWORK_CLARIFICATION",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": "GGA3623_1_Newton_limit",
            "point": "The Newtonian limit derives the Poisson/source structure, not a numerical value of G from nothing.",
            "formula": "G_00 linearized => nabla^2 Phi = 4*pi*G rho",
            "impact_for_MTS": "The immediate target should be deriving the source structure and showing extra residuals vanish/bound, not pretending every constant must be numerically predicted at this stage.",
            "status": "LOCAL_GR_STRATEGY",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": "GGA3623_2_alpha_parallel",
            "point": "The EM analogue is alpha: deriving Maxwell/U(1) structure is different from deriving the observed fine-structure constant.",
            "formula": "alpha=Q_*^2/(4*pi*Z_Q)",
            "impact_for_MTS": "A measured alpha is acceptable if no extra MTS drift/source residual remains; a predicted alpha requires the stronger parent level certificate.",
            "status": "COUPLING_STRATEGY",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bound_source_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "BS3623_0_w_EM_WEP",
            "coefficient": "w_EM",
            "candidate_arena": "WEP composition / EM binding energy",
            "source_status": "LOCAL_RUNNER_HAS_PLACEHOLDER_ONLY",
            "candidate_source_path": str(RESIDUALS / "P8_EM_common_scale_bound_runner_results.csv"),
            "needed_numeric_row": "eta_bound, EM_binding_fraction_difference, map eta ~= w_EM Delta f_EM",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "BS3623_1_w_EM_Newton_GM",
            "coefficient": "w_EM",
            "candidate_arena": "Newton/source calibration",
            "source_status": "LOCAL_RUNNER_HAS_PLACEHOLDER_ONLY",
            "candidate_source_path": str(RESIDUALS / "P8_EM_common_scale_bound_runner_results.csv"),
            "needed_numeric_row": "GM calibration residual plus composition/source model linking EM fraction to effective gravitational mass",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "BS3623_2_Phi_stationary",
            "coefficient": "Phi_EM_boundary",
            "candidate_arena": "stationary local source",
            "source_status": "THEOREM_ROUTE_PREFERRED_OVER_NUMERIC_BOUND",
            "candidate_source_path": str(RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv"),
            "needed_numeric_row": "not numeric if stationary/no-flux worldtube is parent-signed; otherwise H_tau flux normalization",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "BS3623_3_Phi_radiative",
            "coefficient": "Phi_EM_boundary",
            "candidate_arena": "radiative/orbital flux",
            "source_status": "NEEDS_EXTERNAL_OR_LOCAL_FLUX_TABLE",
            "candidate_source_path": str(RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv"),
            "needed_numeric_row": "observed EM luminosity/flux, surface radius, H_tau conversion, and no-double-counting with matter stress",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3623_0_real_progress",
            "decision": "The coupling gap has been reduced to a precise invariant-ratio problem: alpha/current calibration needs Q_* and Z_Q, not just compact U(1).",
            "status": "PROOF_SHARPENED",
            "next_action": "do not keep searching for alpha from charge quantization alone; search for parent level/metric/Q_* certificate",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3623_1_GR_strategy",
            "decision": "Measured constants are acceptable at the local-GR reduction stage; what must be derived is the form of the equations and absence/bounds of extra residuals.",
            "status": "STRATEGY_SET",
            "next_action": "build the minimal local-GR reduction contract with calibrated constants and explicit residual vector",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3623_2_Poynting_route",
            "decision": "Poynting is not a side idea; it is the EM stress-current component and should be used to test source leakage/no-flux closure.",
            "status": "ROUTE_RETAINED",
            "next_action": "derive stationary Phi_EM=0 branch and separate radiative flux branch",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3623_3_next_target",
            "decision": "Next checkpoint should build a minimal local-GR reduction contract: Einstein-Hilbert form with calibrated G, Maxwell/Hilbert stress with calibrated alpha, and an explicit MTS residual vector.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3624-Y5-R2FR-minimal-local-GR-reduction-contract-with-calibrated-couplings.md",
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
            "status_id": "STATUS3623_0",
            "result": "COUPLING_GAP_REDUCED_TO_PARENT_LEVEL_OR_CALIBRATED_CONSTANT_CONTRACT",
            "summary": "3623 proves compact charge quantization alone cannot derive alpha/source calibration, identifies the exact parent certificate that would, and reframes local-GR reduction around calibrated constants plus residual suppression.",
            "parent_level_signed": False,
            "w_EM_zero_signed": False,
            "Phi_EM_zero_signed": False,
            "local_GR_strategy_ready": True,
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
            "next_id": "NEXT3623_0",
            "target_doc": "3624-Y5-R2FR-minimal-local-GR-reduction-contract-with-calibrated-couplings.md",
            "target_script": "scripts/Y5_R2FR_3624_minimal_local_GR_reduction_contract_with_calibrated_couplings.py",
            "objective": "write the minimal local-GR reduction contract using calibrated low-energy constants G_eff and alpha_eff while deriving or bounding every extra MTS residual coefficient",
            "success_gate": "Einstein-Hilbert/Newton/Maxwell stress forms are separated from extra MTS residuals; no residual is silently set to zero without theorem or bound",
            "reason": "GR itself measures G; MTS should first derive the form and kill/bound extra residuals before trying to predict constants numerically.",
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
            "coupling_result": status["result"],
            "alpha_route": "PARENT_LEVEL_QSTAR_CERTIFICATE_OR_CALIBRATED_ALPHA",
            "G_route": "CALIBRATED_G_EFF_ALLOWED_IN_LOCAL_GR_LIMIT",
            "Poynting_route": "EM_STRESS_CURRENT_DIAGNOSTIC_RETAINED",
            "next_pressure_point": "minimal_local_GR_reduction_contract_residual_vector",
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
    certificate = parent_level_certificate_rows()
    no_go = scaling_no_go_rows()
    wem_phi = wem_phi_theorem_rows()
    gr_g = gr_g_analogy_rows()
    bounds = bound_source_rows()
    decisions = decision_gate_rows()
    status = status_rows()
    next_target = next_target_rows()
    content = f"""# 3623 Y5 R2FR parent fibre-level certificate or w_EM/Phi bound source

**Status:** {status[0]["summary"]}

**Claim ceiling:** no derived alpha, no derived Newton constant, no local-GR pass, no WEP/R10/PPN pass, and no GitHub action is allowed from 3623. This checkpoint is a coupling-structure gate.

## Core outcome

The useful advance is not a new public claim. It is a sharper mathematical split:

- Compact `U(1)` can fix relative integer charge labels.
- It cannot by itself fix the observed coupling because `alpha_Q = Q_*^2/(4*pi*Z_Q)`.
- A parent level/fibre-metric/base-charge certificate could fix `Q_*` and `Z_Q` together.
- If that certificate is absent, `G_eff` and `alpha_eff` may be treated like calibrated low-energy constants, exactly as GR treats `G`, while the extra MTS residual vector must still be derived zero or bounded.
- Poynting flux remains central because it is the EM stress-current component `T_EM^{{0i}}`, not an optional side story.

## Source register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Parent fibre-level certificate

{markdown_table(certificate, ["certificate_id", "piece", "formula", "current_status", "parent_signed"])}

## Scaling/no-go audit

{markdown_table(no_go, ["no_go_id", "statement", "formula", "status"])}

## w_EM / Phi_EM theorem split

{markdown_table(wem_phi, ["theorem_id", "object", "formula", "current_status", "missing_piece"])}

## GR/Newton constant analogy

{markdown_table(gr_g, ["row_id", "point", "formula", "impact_for_MTS"])}

## Bound-source rows

{markdown_table(bounds, ["bound_id", "coefficient", "candidate_arena", "source_status", "needed_numeric_row"])}

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
    certificate = parent_level_certificate_rows()
    no_go = scaling_no_go_rows()
    wem_phi = wem_phi_theorem_rows()
    gr_g = gr_g_analogy_rows()
    bounds = bound_source_rows()
    decisions = decision_gate_rows()
    status = status_rows()
    next_target = next_target_rows()

    results: list[tuple[str, bool, str]] = []
    missing_sources = [row["path"] for row in sources if not row["exists"]]
    results.append(("VAL3623_0_sources_exist", not missing_sources, "all sources exist" if not missing_sources else "; ".join(missing_sources)))
    missing_needles = [row["source_id"] for row in sources if not row["needle_found"]]
    results.append(("VAL3623_1_needles_found", not missing_needles, "all selected anchors found" if not missing_needles else "; ".join(missing_needles)))
    missing_outputs = [key for key, path in pre_validation.items() if not path.exists()]
    results.append(("VAL3623_2_outputs_exist", not missing_outputs, "all pre-validation outputs written" if not missing_outputs else "; ".join(missing_outputs)))

    parse_details: list[str] = []
    csv_parse_ok = True
    for key, path in pre_validation.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            rows = read_csv(path)
            parse_details.append(f"{key}:{len(rows)}")
            if not rows:
                csv_parse_ok = False
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{key}:{exc}")
    results.append(("VAL3623_3_csv_parse", csv_parse_ok, "; ".join(parse_details)))

    has_alpha_formula = any("alpha_Q=Q_*^2/(4*pi*Z_Q)" in str(row.get("formula", "")) for row in certificate + no_go + gr_g)
    results.append(("VAL3623_4_alpha_ratio_written", has_alpha_formula, "alpha invariant-ratio formula written"))
    no_go_status = any(row["status"] == "NO_GO_PROVED_FOR_CURRENT_UNSIGNED_CERTIFICATE" for row in no_go)
    results.append(("VAL3623_5_scaling_no_go_written", no_go_status, "coupling scaling no-go written"))
    gr_g_ok = any("GR does not derive Newton" in row["point"] for row in gr_g)
    results.append(("VAL3623_6_GR_G_analogy_written", gr_g_ok, "GR/Newton constant analogy written"))
    poynting_ok = any("T_EM^{0i}=S_Poynting^i/c^2" in row["formula"] for row in wem_phi)
    results.append(("VAL3623_7_poynting_identity_written", poynting_ok, "Poynting stress-current identity written"))
    stationary_ok = any(row["theorem_id"] == "WPT3623_2_boundary_flux_zero" and row["claim_allowed"] is False for row in wem_phi)
    results.append(("VAL3623_8_stationary_phi_nonclaim", stationary_ok, "stationary Phi zero branch remains conditional/nonclaim"))
    all_nonclaim = all(row.get("claim_allowed") is False and row.get("valid_for_claim") is False for collection in [certificate, no_go, wem_phi, gr_g, bounds, decisions, status, next_target] for row in collection)
    results.append(("VAL3623_9_all_outputs_nonclaim", all_nonclaim, "all generated rows remain nonclaim"))

    if FORMALIZATION.exists():
        leaked_paths = list(FORMALIZATION.rglob("*3623*"))
        formalization_clean = len(leaked_paths) == 0
        formalization_detail = "no 3623 files in formalization-workbench" if formalization_clean else "; ".join(str(path) for path in leaked_paths[:5])
    else:
        formalization_clean = True
        formalization_detail = "formalization-workbench not present"
    results.append(("VAL3623_10_no_formalization_leak", formalization_clean, formalization_detail))

    next_ok = next_target[0]["target_doc"] == "3624-Y5-R2FR-minimal-local-GR-reduction-contract-with-calibrated-couplings.md"
    results.append(("VAL3623_11_next_target_written", next_ok, "3624 local-GR contract selected"))

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
    write_csv(paths["parent_level_certificate"], parent_level_certificate_rows())
    write_csv(paths["scaling_no_go"], scaling_no_go_rows())
    write_csv(paths["wem_phi_theorem"], wem_phi_theorem_rows())
    write_csv(paths["gr_g_analogy"], gr_g_analogy_rows())
    write_csv(paths["bound_source_rows"], bound_source_rows())
    write_csv(paths["decision_gates"], decision_gate_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_csv(paths["canonical_status"], canonical_status_rows())
    write_markdown()
    write_csv(paths["validation"], validate())

    failed = [row for row in read_csv(paths["validation"]) if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3623 validation failed: {failed}")
    print(f"wrote 3623 checkpoint with {len(read_csv(paths['validation']))} validation checks")


if __name__ == "__main__":
    main()
