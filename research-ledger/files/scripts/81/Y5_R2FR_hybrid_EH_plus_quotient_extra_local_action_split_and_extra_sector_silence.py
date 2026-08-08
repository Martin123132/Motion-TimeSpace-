from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1787"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1787_0_1786_handoff",
        "source_key": "1786_handoff_doc",
        "source_path": ROOT / "1786-Y5-R2FR-choose-quotient-zero-or-hybrid-and-close-boundary-or-DqZ-source-row.md",
        "needles": ["HQA1786_5_verdict", "DEC1786_1_hybrid_status", "NEXT1786_0_primary"],
    },
    {
        "source_id": "SRC1787_1_1786_validation",
        "source_key": "1786_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1786_VALIDATION.csv",
        "needles": ["VAL1786_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1787_2_1786_hybrid_audit",
        "source_key": "1786_hybrid_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1786_HYBRID_EH_QUOTIENT_AUDIT.csv",
        "needles": ["HQA1786_0_EH_core", "HQA1786_5_verdict"],
    },
    {
        "source_id": "SRC1787_3_912_eh_baseline",
        "source_key": "912_eh_core_baseline",
        "source_path": RESIDUALS / "P8_Y5_R10_912_EH_CORE_BASELINE.csv",
        "needles": ["EHB912_0_EH_variation", "EHB912_3_EH_does_not_silence_extras"],
    },
    {
        "source_id": "SRC1787_4_912_extra_omega",
        "source_key": "912_extra_sector_omega",
        "source_path": RESIDUALS / "P8_Y5_R10_912_EXTRA_SECTOR_OMEGA_LEDGER.csv",
        "needles": ["ESO912_0_projector", "ESO912_6_matter_frame"],
    },
    {
        "source_id": "SRC1787_5_912_delta_symp",
        "source_key": "912_delta_symp_extra_rows",
        "source_path": RESIDUALS / "P8_Y5_R10_912_DELTA_SYMP_EXTRA_ROWS.csv",
        "needles": ["DSE912_0_projector", "DSE912_5_connection"],
    },
    {
        "source_id": "SRC1787_6_913_projector_fate",
        "source_key": "913_projector_route_fate",
        "source_path": RESIDUALS / "P8_Y5_R10_913_ROUTE_FATE_AUDIT.csv",
        "needles": ["PR913_0_absolute_topological_PiM", "PR913_4_retained_source_row"],
    },
    {
        "source_id": "SRC1787_7_913_projector_zero",
        "source_key": "913_projector_zero_clauses",
        "source_path": RESIDUALS / "P8_Y5_R10_913_PROJECTOR_ZERO_ROUTE_CLAUSES.csv",
        "needles": ["ZP913_0_fixed_topology", "ZP913_7_no_readout_mask"],
    },
    {
        "source_id": "SRC1787_8_914_topological_parent",
        "source_key": "914_topological_parent_clause",
        "source_path": RESIDUALS / "P8_Y5_R10_914_TOPOLOGICAL_PARENT_CLAUSE_AUDIT.csv",
        "needles": ["TPC914_0_fixed_oriented_exterior", "TPC914_8_no_readout_mask_in_parent_variation"],
    },
    {
        "source_id": "SRC1787_9_915_equality",
        "source_key": "915_equality_derivation",
        "source_path": RESIDUALS / "P8_Y5_R10_915_EQUALITY_DERIVATION_ATTEMPT.csv",
        "needles": ["EDA915_1_equality_up_to_exact_term", "EDA915_6_measured_GM_after_equality"],
    },
    {
        "source_id": "SRC1787_10_915_residual_pack",
        "source_key": "915_current_mismatch_residual_pack",
        "source_path": RESIDUALS / "P8_Y5_R10_915_CURRENT_MISMATCH_RESIDUAL_PACK.csv",
        "needles": ["MRP915_0_Delta_HT_current", "MRP915_6_partial_r_ln_mu_obs"],
    },
    {
        "source_id": "SRC1787_11_956_source_side",
        "source_key": "956_source_side_spine",
        "source_path": RESIDUALS / "P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv",
        "needles": ["SSG956_0_observed_coframe", "SSG956_5_source_side_verdict"],
    },
    {
        "source_id": "SRC1787_12_956_left_hand",
        "source_key": "956_left_hand_eh_newton",
        "source_path": RESIDUALS / "P8_Y5_R10_956_LEFT_HAND_EH_NEWTON_GATE_MAP.csv",
        "needles": ["LHG956_0_EH_core_selection", "LHG956_5_PPN_completion"],
    },
    {
        "source_id": "SRC1787_13_957_spine",
        "source_key": "957_parent_local_gr_spine",
        "source_path": RESIDUALS / "P8_Y5_R10_957_PARENT_LOCAL_GR_SPINE_LEDGER.csv",
        "needles": ["PLG957_2_EH_operator", "PLG957_5_PPN_completion"],
    },
    {
        "source_id": "SRC1787_14_958_eh_core",
        "source_key": "958_eh_core_attempt",
        "source_path": RESIDUALS / "P8_Y5_R10_958_EH_CORE_SELECTION_ATTEMPT.csv",
        "needles": ["EH958_0_target", "EH958_5_verdict"],
    },
    {
        "source_id": "SRC1787_15_958_r11_review",
        "source_key": "958_r11_non_eh_review",
        "source_path": RESIDUALS / "P8_Y5_R10_958_R11_NON_EH_VECTOR_REVIEW.csv",
        "needles": ["R11REV958_1", "R11REV958_9"],
    },
    {
        "source_id": "SRC1787_16_958_r11_priority",
        "source_key": "958_r11_priority",
        "source_path": RESIDUALS / "P8_Y5_R10_958_R11_OPERATOR_FAMILY_PRIORITY.csv",
        "needles": ["R11PRI958_1", "R11PRI958_5", "R11PRI958_9"],
    },
    {
        "source_id": "SRC1787_17_959_no_extra",
        "source_key": "959_no_extra_field",
        "source_path": RESIDUALS / "P8_Y5_R10_959_NO_EXTRA_FIELD_CLAUSE_ATTEMPT.csv",
        "needles": ["NEF959_0_target", "NEF959_5_verdict"],
    },
    {
        "source_id": "SRC1787_18_959_silence_requirements",
        "source_key": "959_silence_requirements",
        "source_path": RESIDUALS / "P8_Y5_R10_959_SILENCE_MECHANISM_REQUIREMENTS.csv",
        "needles": ["SMR959_0_operator", "SMR959_4_retained_vector"],
    },
    {
        "source_id": "SRC1787_19_960_r2fr",
        "source_key": "960_r2fr",
        "source_path": RESIDUALS / "P8_Y5_R10_960_R2_FR_ZERO_OR_BOUND_ATTEMPT.csv",
        "needles": ["R2FR960_0_target", "R2FR960_4_verdict"],
    },
    {
        "source_id": "SRC1787_20_960_connection",
        "source_key": "960_torsion_levi_civita",
        "source_path": RESIDUALS / "P8_Y5_R10_960_TORSION_LEVI_CIVITA_GATE_ATTEMPT.csv",
        "needles": ["LC960_0_target", "LC960_4_verdict"],
    },
    {
        "source_id": "SRC1787_21_962_r2fr_relative",
        "source_key": "962_r2fr_zero_proof",
        "source_path": RESIDUALS / "P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv",
        "needles": ["R2Z962_0_target", "R2Z962_5_relative_zero_theorem"],
    },
    {
        "source_id": "SRC1787_22_963_derivative_order",
        "source_key": "963_derivative_order",
        "source_path": RESIDUALS / "P8_Y5_R10_963_DERIVATIVE_ORDER_AUDIT.csv",
        "needles": ["DO963_0_962_relative_theorem", "DO963_6_verdict"],
    },
    {
        "source_id": "SRC1787_23_964_minimality",
        "source_key": "964_minimality",
        "source_path": RESIDUALS / "P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
        "needles": ["MIN964_0_target", "MIN964_5_verdict"],
    },
    {
        "source_id": "SRC1787_24_965_primitive_quotient",
        "source_key": "965_primitive_quotient",
        "source_path": RESIDUALS / "P8_Y5_R10_965_PRIMITIVE_QUOTIENT_THEOREM_ATTEMPT.csv",
        "needles": ["PQ965_0_theorem_target", "PQ965_5_verdict"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1787_SOURCE_REGISTER.csv",
    "hybrid_action_split": RESIDUALS / "P8_Y5_PARENT_QLOC_1787_HYBRID_ACTION_SPLIT.csv",
    "conditional_reduction_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1787_CONDITIONAL_REDUCTION_THEOREM.csv",
    "extra_sector_silence_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1787_EXTRA_SECTOR_SILENCE_MATRIX.csv",
    "operator_priority": RESIDUALS / "P8_Y5_PARENT_QLOC_1787_OPERATOR_PRIORITY_GATE.csv",
    "residual_vector_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1787_RESIDUAL_VECTOR_PACK.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1787_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1787_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1787_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1787_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1787_VALIDATION.csv",
}

DOC_PATH = ROOT / "1787-Y5-R2FR-hybrid-EH-plus-quotient-extra-local-action-split-and-extra-sector-silence.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and all(needle in text for needle in needles),
                "role": "1787 hybrid action split and extra-sector silence evidence",
            }
        )
    return rows


def hybrid_action_split_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "split_id": "HAS1787_0_configuration",
            "clause": "hybrid local branch configuration",
            "mathematical_form": "Y_local=(e_obs/g_obs, Psi_matter, X_memory, Pi_M/projector, domain, boundary, connection, source-normalization)",
            "current_status": "CONFIGURATION_SPLIT_WRITTEN_NONCLAIM",
            "proof_value": "makes every non-EH local variable visible rather than hidden inside GR-like notation",
            "missing_for_claim": "parent action and field-specific Euler operators for all extra sectors",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "split_id": "HAS1787_1_action",
            "clause": "hybrid action split",
            "mathematical_form": "S_local = S_EH[e_obs] + S_matter[Psi,e_obs,theta] + S_extra[X,Pi_M,D,boundary,Gamma,kappa; e_obs]",
            "current_status": "ACTION_SPLIT_CONTRACT",
            "proof_value": "EH is allowed only as the core baseline; S_extra must be zero/silent/bounded",
            "missing_for_claim": "explicit parent-owned S_extra and no-shadow matter-frame theorem",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "split_id": "HAS1787_2_variation",
            "clause": "field equation split",
            "mathematical_form": "delta S_local/delta e_obs = E_EH + E_matter + sum_i DeltaE_i",
            "current_status": "EXACT_BOOKKEEPING_IDENTITY",
            "proof_value": "prevents claiming GR unless sum_i DeltaE_i is actually zero or bounded",
            "missing_for_claim": "sector-by-sector DeltaE_i expressions and source projections",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "split_id": "HAS1787_3_symplectic",
            "clause": "symplectic/charge split",
            "mathematical_form": "omega_total = omega_EH + omega_matter + omega_extra",
            "current_status": "EXACT_BOOKKEEPING_IDENTITY",
            "proof_value": "inherits the 912 warning that EH charge machinery does not silence omega_extra",
            "missing_for_claim": "omega_extra=0/gauge/topological/no-flux or residual rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "split_id": "HAS1787_4_residual_envelope",
            "clause": "no-cancellation residual discipline",
            "mathematical_form": "|Delta_local| <= sum_i |Delta_i|, with each i theorem-zero or source-backed below bounds",
            "current_status": "ABSOLUTE_ENVELOPE_RULE",
            "proof_value": "stops unknown extra sectors from being hidden by cancellations",
            "missing_for_claim": "numeric/source-backed rows or zero theorems for all retained components",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "split_id": "HAS1787_5_verdict",
            "clause": "hybrid split is enough to claim local GR",
            "mathematical_form": "HAS1787_0 through HAS1787_4 plus every silence matrix row closes",
            "current_status": "HYBRID_SPLIT_WRITTEN_EXTRA_SECTOR_SILENCE_NOT_CLOSED",
            "proof_value": "the route is now precise, not claim-ready",
            "missing_for_claim": "R2/fR, torsion/nonmetricity, projector/domain/boundary/source/matter-frame rows remain open",
            "valid_for_claim": False,
        },
    ]


def conditional_reduction_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HCT1787_0_conditional_GR_reduction",
            "claim": "hybrid local branch reduces to GR if all extra sectors are silent",
            "mathematical_form": "If S_extra has DeltaE_i=0 and omega_extra=0 modulo gauge/topological/no-flux terms, then E_EH = kappa_univ T_total plus harmless Lambda/background",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "why_exact": "variation and symplectic split are linear bookkeeping identities once the action split is accepted",
            "not_yet_proved": "the silence hypotheses are not parent-signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HCT1787_1_Newton_limit_condition",
            "claim": "Newtonian mechanics follows only after EH source calibration",
            "mathematical_form": "nabla^2 Phi = 4 pi G_eff rho_H and mu_EH=mu_obs=G_ref M_H[Pi_M J_H]",
            "proof_status": "EXACT_CONDITIONAL_REQUIREMENT",
            "why_exact": "EH weak-field algebra is clean conditionally, but measured-GM calibration is an extra gate",
            "not_yet_proved": "Hilbert-topological equality, boundary zero flux, and orbital GM calibration",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HCT1787_2_PPN_condition",
            "claim": "GR PPN values require all retained local residual vector components to vanish or pass bounds",
            "mathematical_form": "gamma=1, beta=1, alpha_i=0, xi=0 plus no Gdot/range/source-normalization leakage",
            "proof_status": "EXACT_CONDITIONAL_REQUIREMENT",
            "why_exact": "PPN promotion is blocked by any unsourced residual family",
            "not_yet_proved": "R2/fR, connection, projector/domain, boundary, source, matter-frame residuals",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HCT1787_3_R2FR_relative_result",
            "claim": "R2/fR scalar mode is killed if metric-only second-order no-extra-scalar premise is signed",
            "mathematical_form": "metric-only second-order local exterior + no retained scalar => f_RR=0 and c_R2=c_fR=0",
            "proof_status": "RELATIVE_THEOREM_AVAILABLE_PARENT_PREMISE_UNSIGNED",
            "why_exact": "962 proves the relative scalar-pole exclusion under the strong premise",
            "not_yet_proved": "parent theorem that MTS satisfies exact second-order/no-extra-scalar premise",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HCT1787_4_verdict",
            "claim": "hybrid branch currently proves local GR/Newton",
            "mathematical_form": "HCT1787_0 through HCT1787_3 plus silence matrix closes",
            "proof_status": "CONDITIONAL_ONLY_NOT_CLAIM",
            "why_exact": "the target theorem is now stated precisely",
            "not_yet_proved": "actual silence/bound rows",
            "valid_for_claim": False,
        },
    ]


def extra_sector_silence_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "sector_id": "ESM1787_0_R2_fR_scalar",
            "sector": "R2/fR scalar-mode curvature sector",
            "silence_route": "parent second-order metric-only/no-extra-scalar theorem OR scalar-mode bound row",
            "current_status": "RELATIVE_ZERO_THEOREM_AVAILABLE_PARENT_PREMISE_UNSIGNED",
            "source_basis": "R2FR960_4; R2Z962_5; DO963_6; MIN964_5",
            "local_risk": "Yukawa/fifth force, gamma/beta shift, finite-range R10 scalar channel",
            "next_action": "attempt parent second-order/minimality activation before numeric bounds",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "ESM1787_1_torsion_nonmetricity",
            "sector": "independent connection/torsion/nonmetricity sector",
            "silence_route": "metric-only parent or Palatini no-hypermomentum theorem OR P4 connection residual rows",
            "current_status": "LEVI_CIVITA_GATE_NOT_CLOSED",
            "source_basis": "LC960_0; LC960_4; R11PRI958_5",
            "local_risk": "WEP, clocks, light cones, spin, source charge, connection PPN leakage",
            "next_action": "attempt no-independent-connection/no-hypermomentum theorem after R2/fR priority or in parallel",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "ESM1787_2_projector_PiM",
            "sector": "projector/Pi_M/topological mass current sector",
            "silence_route": "metric-independent topological Pi_M plus Hilbert-topological equality plus boundary no-flux",
            "current_status": "BEST_ZERO_ROUTE_NOT_PARENT_SIGNED",
            "source_basis": "PR913_0; ZP913_5; TPC914_5; EDA915_1",
            "local_risk": "measured GM mismatch, PPN/source residuals, Bianchi-visible projector stress",
            "next_action": "keep as high-priority source/charge branch after operator-side R2/fR gate",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "ESM1787_3_boundary_reference",
            "sector": "boundary/corner/reference sector",
            "silence_route": "class-only boundary/reference theorem with no compact flux or radial/time/range hair",
            "current_status": "BOUNDARY_REFERENCE_RULE_MISSING",
            "source_basis": "DSE912_1_boundary; TPC914_6; MRP915_2_B_zero_flux",
            "local_risk": "beta/xi, radial source hair, Gdot, measured GM drift",
            "next_action": "derive boundary zero-flux or source boundary residual rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "ESM1787_4_domain_selector",
            "sector": "domain/selector/homology sector",
            "silence_route": "covariant fixed-domain/topological selector or finite preferred-frame/source rows",
            "current_status": "DOMAIN_SELECTOR_ZERO_MISSING",
            "source_basis": "DSE912_2_domain; R11PRI958_9; PSB914_6",
            "local_risk": "alpha1, alpha2, xi, domain drift, source normalization leakage",
            "next_action": "derive fixed-domain theorem or source c_domain row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "ESM1787_5_bulk_X_memory",
            "sector": "bulk X/memory/nonlocal sector",
            "silence_route": "source-free positive/no-hair theorem or source-normalized fifth-force/range row",
            "current_status": "X_MASS_GAP_OR_FORCE_LAW_MISSING",
            "source_basis": "ESO912_3_bulk_X_memory; DSE912_3_bulk_X; R11PRI958_7",
            "local_risk": "bulk fifth force, gamma/beta shifts, R10 alpha(lambda), Gdot/memory kernel",
            "next_action": "retain until operator-side and source-side highest priorities are attacked",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "ESM1787_6_source_normalization",
            "sector": "source normalization / G_eff / M_eff sector",
            "silence_route": "superselection/constraint theorem or derivative residual rows",
            "current_status": "SOURCE_NORMALIZATION_OMEGA_MISSING",
            "source_basis": "SSG956_5; LHG956_3_measured_GM_calibration; DSE912_4_source",
            "local_risk": "Gdot, measured GM mismatch, source charge drift, orbit residuals",
            "next_action": "requires projector/Hilbert equality and measured-GM calibration",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "ESM1787_7_matter_frame",
            "sector": "ordinary matter frame/spurion sector",
            "silence_route": "single public observed coframe and no direct MTS vertices/spurions",
            "current_status": "MATTER_NO_SPURION_CERTIFICATE_MISSING",
            "source_basis": "SPM/terminal route from 1030/1031 via 1786; ESO912_6_matter_frame",
            "local_risk": "WEP/source charge, clocks, frame transfer, c_g/b_A/b_alpha residuals",
            "next_action": "derive matter-interface functor or label SPM as closure and source finite rows",
            "valid_for_claim": False,
        },
    ]


def operator_priority_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "priority_id": "OPG1787_0_first",
            "target": "R2_fR_scalar_mode",
            "priority": "primary_next",
            "reason": "sharpest operator-side EH blocker; 962 gives a relative theorem, so the next attempt has a precise premise to activate",
            "current_status": "ZERO_NOT_PARENT_SIGNED_BOUND_NOT_EXECUTABLE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_id": "OPG1787_1_second",
            "target": "torsion_nonmetricity_Levi_Civita",
            "priority": "parallel_or_second",
            "reason": "connection compatibility is another highest-first EH premise affecting clocks, WEP, light, spin, and source charge",
            "current_status": "LC_GATE_NOT_CLOSED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_id": "OPG1787_2_source_charge",
            "target": "projector_PiM_Hilbert_topological_equality",
            "priority": "high_after_operator_gate",
            "reason": "source/charge side blocks measured Newton GM even if the EH operator is selected",
            "current_status": "BEST_ZERO_ROUTE_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_id": "OPG1787_3_fallback",
            "target": "nonclaim_residual_vector_pack",
            "priority": "fallback_if_zero_proofs_fail",
            "reason": "all retained sectors need executable coefficients, units, weak-field maps, source paths, and no-cancellation scoring",
            "current_status": "RESIDUAL_ROWS_NOT_EXECUTABLE",
            "valid_for_claim": False,
        },
    ]


def residual_vector_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "RVP1787_0_c_R2_fR",
            "symbol": "c_R2_or_c_fR",
            "sector": "R2/fR scalar mode",
            "observable_link": "R10 alpha(lambda), gamma, beta, finite-range scalar force",
            "needed_inputs": "coefficient value/units, scalar mass/coupling, weak-field map, source path",
            "current_status": "MISSING_NUMERIC_OR_DERIVED_ZERO_COEFFICIENT",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RVP1787_1_c_T_Q",
            "symbol": "c_T_or_c_Q",
            "sector": "torsion/nonmetricity",
            "observable_link": "WEP, clocks, light cones, spin, source charge",
            "needed_inputs": "LC theorem or torsion/nonmetricity coefficients and maps",
            "current_status": "MISSING_CONNECTION_ZERO_OR_BOUND_INPUTS",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RVP1787_2_Delta_symp_projector",
            "symbol": "Delta_symp_projector",
            "sector": "projector/Pi_M",
            "observable_link": "q_P^nu, c_PiM_g, gamma, beta, alpha3, xi, measured GM drift",
            "needed_inputs": "projector omega-zero theorem or coefficient/source row",
            "current_status": "MISSING_PROJECTOR_OMEGA_ZERO_OR_COEFFICIENT",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RVP1787_3_boundary_domain",
            "symbol": "B_P_flux;c_domain;Delta_ref",
            "sector": "boundary/domain/reference",
            "observable_link": "radial source hair, beta, xi, Gdot, preferred-frame rows",
            "needed_inputs": "boundary/domain no-flux theorem or finite coefficients",
            "current_status": "MISSING_BOUNDARY_DOMAIN_ZERO_OR_BOUND_INPUTS",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RVP1787_4_X_memory_source",
            "symbol": "alpha_X(lambda_X);c_nonlocal;kappa_source",
            "sector": "bulk X/memory/source normalization",
            "observable_link": "R10, PPN, clocks, Gdot, orbit/source-normalization rows",
            "needed_inputs": "mass-gap/no-hair theorem or force law and source-normalized coefficients",
            "current_status": "MISSING_X_MEMORY_SOURCE_INPUTS",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RVP1787_5_matter_frame",
            "symbol": "c_g;b_A;b_alpha;b_dis",
            "sector": "matter frame/spurion",
            "observable_link": "PPN, clocks, WEP, R10, source-charge residuals",
            "needed_inputs": "no-shadow/no-spurion theorem or finite coefficient rows",
            "current_status": "MISSING_MATTER_FRAME_THEOREM_OR_COEFFICIENTS",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1787_0_EH_core_plus_R2",
            "countermodel": "EH core is present but an R2/fR scalar mode remains in S_extra",
            "survives_current_constraints": True,
            "why_survives": "relative R2/fR zero theorem exists, but parent second-order/no-extra-scalar premise is unsigned",
            "what_kills_it": "parent minimality/second-order theorem or scalar-mode bound row below all local limits",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1787_1_EH_core_plus_connection",
            "countermodel": "observed metric has EH core but independent connection residues couple to matter/readout",
            "survives_current_constraints": True,
            "why_survives": "Levi-Civita gate is not closed and connection residual rows are unfilled",
            "what_kills_it": "metric-only parent, Palatini no-hypermomentum theorem, or executable P4 bounds",
        },
        {
            "branch_id": "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428",
            "countermodel_id": "CM1787_2_projector_wrong_current",
            "countermodel": "topological current closes but is not equal to observed Hilbert/Pi_M source current",
            "survives_current_constraints": True,
            "why_survives": "Hilbert-topological equality and measured-GM calibration are not parent-derived",
            "what_kills_it": "J_M^top = Pi_M J_H + dB_zero with zero boundary flux and orbital GM calibration",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1787_3_boundary_hair",
            "countermodel": "boundary or domain terms carry radial/time/range/source hair even when bulk extra sector is quiet",
            "survives_current_constraints": True,
            "why_survives": "boundary/domain no-flux rules are fail-open",
            "what_kills_it": "class-only no-hair theorem or finite boundary/domain residual bounds",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1787_4_spurion_frame",
            "countermodel": "ordinary matter sees a hidden frame/spurion while field equations are written in e_obs",
            "survives_current_constraints": True,
            "why_survives": "single-public-metric/no-shadow route is closure-only in current corpus",
            "what_kills_it": "parent matter-interface functor or finite c_g/b_A/b_alpha rows",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1787_0_hybrid_GR_claim",
            "claim": "hybrid action split proves local GR",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "extra-sector silence matrix is open",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1787_1_R2FR_zero_claim",
            "claim": "R2/fR scalar-mode coefficient is zero in MTS",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "relative theorem exists but parent second-order/no-extra-scalar premise is unsigned",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1787_2_Levi_Civita_claim",
            "claim": "observed connection is Levi-Civita with no torsion/nonmetricity residual",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "metric-only/Palatini no-hypermomentum theorem is not parent-signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1787_3_Newton_GM_claim",
            "claim": "Newtonian measured GM follows from the hybrid split",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "Hilbert-topological equality and boundary zero flux are not derived",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1787_4_residual_score_claim",
            "claim": "retained residual vector is executable/scorable",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "missing coefficients, units, weak-field maps, source paths, and arena projections",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1787_0_split_status",
            "decision": "HYBRID_ACTION_SPLIT_WRITTEN_NONCLAIM",
            "reason": "the route is now mathematically explicit: EH core plus all non-EH sectors in S_extra",
            "next_action": "attack the highest-priority operator-side silence gate",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1787_1_first_target",
            "decision": "R2FR_PARENT_PREMISE_ACTIVATION_IS_NEXT",
            "reason": "R2/fR has a useful relative zero theorem already; proving the parent premise would kill a central EH blocker",
            "next_action": "try to derive exact local second-order/no-extra-scalar/minimality premise; if it fails, stage scalar-mode bound rows",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1787_2_second_target",
            "decision": "LEVI_CIVITA_CONNECTION_GATE_IS_PARALLEL_SECOND",
            "reason": "torsion/nonmetricity is another highest-first obstruction, but R2/fR is sharper because the relative theorem is already available",
            "next_action": "queue no-independent-connection/no-hypermomentum theorem",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1787_3_source_charge_policy",
            "decision": "PROJECTOR_PIM_REMAINS_HIGH_PRIORITY_SOURCE_SIDE",
            "reason": "even a successful EH operator still needs measured-GM and Hilbert-topological current closure",
            "next_action": "return to Pi_M/Hilbert equality after operator-side gate or run in parallel",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1787_0_primary",
            "next_target": "1788-Y5-R2FR-parent-second-order-no-extra-scalar-premise-or-R2FR-bound-row.md",
            "script": "scripts/Y5_R2FR_parent_second_order_no_extra_scalar_premise_or_R2FR_bound_row.py",
            "objective": "try to activate the relative R2/fR zero theorem by deriving the parent local exterior is metric-only, second-order, and no-extra-scalar; if not, stage finite scalar-mode bound rows",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1787_1_parallel",
            "next_target": "1788b-Y5-R2FR-Levi-Civita-connection-theorem-or-P4-bound-row.md",
            "script": "scripts/Y5_R2FR_Levi_Civita_connection_theorem_or_P4_bound_row.py",
            "objective": "derive observed connection is Levi-Civita/no-hypermomentum or stage torsion/nonmetricity coefficient rows",
            "selection_status": "queued_parallel_second",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1787_2_source_side",
            "next_target": "1788c-Y5-R2FR-PiM-Hilbert-topological-equality-or-source-residual-row.md",
            "script": "scripts/Y5_R2FR_PiM_Hilbert_topological_equality_or_source_residual_row.py",
            "objective": "derive topological mass current equals observed Hilbert Pi_M current with zero boundary flux or retain measured-GM/source residual rows",
            "selection_status": "queued_after_operator_gate",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "hybrid_action_split": hybrid_action_split_rows(),
        "conditional_reduction_theorem": conditional_reduction_theorem_rows(),
        "extra_sector_silence_matrix": extra_sector_silence_matrix_rows(),
        "operator_priority": operator_priority_rows(),
        "residual_vector_pack": residual_vector_pack_rows(),
        "countermodel_ledger": countermodel_ledger_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def fieldnames_for(rows: list[dict[str, Any]]) -> list[str]:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    return fieldnames


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames_for(rows))
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
        shutil.copy2(path, RAB_QUEUE / f"JR1787_{key.upper()}.csv")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "pass", "passed"}


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return (
        all(boolish(row["exists"]) for row in rows),
        all(boolish(row["needles_present"]) for row in rows),
    )


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for flag in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "accepted_for_scoring",
                "theorem_closed_for_claim",
                "parent_signed",
                "valid_prediction_row",
                "gate_pass",
            ):
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                for flag in (
                    "valid_for_claim",
                    "claim_allowed",
                    "score_ready",
                    "accepted_for_scoring",
                    "theorem_closed_for_claim",
                    "valid_prediction_row",
                    "gate_pass",
                ):
                    if boolish(row.get(flag, False)):
                        return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not (MICROSCOPE_RESIDUALS / path.name).exists():
            return False
        if not (QUARANTINE / path.name).exists():
            return False
        if not (RAB_QUEUE / f"JR1787_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add(DOC_PATH.name)
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1787_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1787_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1787_2_action_split_written",
            any(
                row["split_id"] == "HAS1787_5_verdict"
                and row["current_status"] == "HYBRID_SPLIT_WRITTEN_EXTRA_SECTOR_SILENCE_NOT_CLOSED"
                for row in rows_map["hybrid_action_split"]
            )
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["hybrid_action_split"]),
            "hybrid action split is written and nonclaim",
        ),
        (
            "VAL1787_3_conditional_theorem_written",
            any(
                row["theorem_id"] == "HCT1787_0_conditional_GR_reduction"
                and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM"
                for row in rows_map["conditional_reduction_theorem"]
            )
            and any(
                row["theorem_id"] == "HCT1787_4_verdict"
                and row["proof_status"] == "CONDITIONAL_ONLY_NOT_CLAIM"
                for row in rows_map["conditional_reduction_theorem"]
            ),
            "conditional GR reduction theorem is explicit and not promoted",
        ),
        (
            "VAL1787_4_silence_matrix_complete",
            any(row["sector_id"] == "ESM1787_0_R2_fR_scalar" for row in rows_map["extra_sector_silence_matrix"])
            and any(row["sector_id"] == "ESM1787_1_torsion_nonmetricity" for row in rows_map["extra_sector_silence_matrix"])
            and any(row["sector_id"] == "ESM1787_2_projector_PiM" for row in rows_map["extra_sector_silence_matrix"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["extra_sector_silence_matrix"]),
            "extra-sector silence matrix includes R2/fR, connection, and projector gates",
        ),
        (
            "VAL1787_5_priority_selected",
            any(
                row["priority_id"] == "OPG1787_0_first"
                and row["target"] == "R2_fR_scalar_mode"
                for row in rows_map["operator_priority"]
            ),
            "R2/fR parent-premise activation is selected first",
        ),
        (
            "VAL1787_6_residual_pack_nonclaim",
            all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["residual_vector_pack"]),
            "residual vector pack remains nonclaim and not score-ready",
        ),
        (
            "VAL1787_7_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live",
        ),
        (
            "VAL1787_8_claim_gates_blocked",
            all(
                not boolish(row["valid_for_claim"])
                and not boolish(row["gate_pass"])
                and row["status"] == "BLOCKED"
                for row in rows_map["claim_gate"]
            ),
            "claim gates are blocked",
        ),
        ("VAL1787_9_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1787_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1787_11_decision_next",
            any(
                row["decision_id"] == "DEC1787_1_first_target"
                and row["decision"] == "R2FR_PARENT_PREMISE_ACTIVATION_IS_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects R2/fR premise activation next",
        ),
        (
            "VAL1787_12_next_selected",
            any(row["route_id"] == "NEXT1787_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1787_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1787 CSVs parse"),
        ("VAL1787_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1787_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1787_16_formalization_untouched", formalization_untouched(), "no 1787 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1787_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1787 hybrid EH-plus-quotient-extra action split and extra-sector silence checkpoint",
        }
    )
    return rows


def clean_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(clean_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1787 - Y5/R2FR Hybrid EH-Plus-Quotient-Extra Local Action Split and Extra-Sector Silence",
            "",
            "## Verdict",
            "",
            "1787 writes the hybrid branch in the form needed for a real GR reduction attempt: `S_local = S_EH[e_obs] + S_matter[Psi,e_obs,theta] + S_extra`. This is useful because it stops the EH core from being used as a shortcut. The conditional theorem is clean: if every extra-sector Euler/symplectic contribution is zero, gauge, topological/no-flux, positive source-free silent, or bounded below local limits, then the hybrid branch reduces to the EH local operator with the standard source side.",
            "",
            "That theorem is still conditional. The current corpus does not yet close R2/fR, torsion/nonmetricity, projector/Pi_M, boundary/domain, bulk X/memory, source normalization, or matter-frame/spurion silence. The first next target is R2/fR because the relative zero theorem already exists and only needs the parent second-order/no-extra-scalar premise activated.",
            "",
            "**Claim ceiling:** no local-GR/Newton/PPN/R10 claim, no R2/fR zero claim, no Levi-Civita claim, no residual score, no GitHub action, and no `formalization-workbench` edit is allowed from 1787.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Hybrid Action Split",
            markdown_table(rows_map["hybrid_action_split"], ["split_id", "clause", "mathematical_form", "current_status", "proof_value", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Conditional Reduction Theorem",
            markdown_table(rows_map["conditional_reduction_theorem"], ["theorem_id", "claim", "mathematical_form", "proof_status", "why_exact", "not_yet_proved", "valid_for_claim"]),
            "",
            "## Extra-Sector Silence Matrix",
            markdown_table(rows_map["extra_sector_silence_matrix"], ["sector_id", "sector", "silence_route", "current_status", "local_risk", "next_action", "valid_for_claim"]),
            "",
            "## Operator Priority Gate",
            markdown_table(rows_map["operator_priority"], ["priority_id", "target", "priority", "reason", "current_status", "valid_for_claim"]),
            "",
            "## Residual Vector Pack",
            markdown_table(rows_map["residual_vector_pack"], ["row_id", "symbol", "sector", "observable_link", "needed_inputs", "current_status", "score_ready", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel_ledger"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is the right shape for the GR reduction fight. We now have the ring: EH core in the observed frame. The work is to force every non-EH sector to either leave the ring, prove it is harmless, or stand there as a measured residual. First punch: activate the R2/fR zero theorem if the parent can genuinely earn second-order/no-extra-scalar dynamics.",
            "",
        ]
    )


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1787 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
