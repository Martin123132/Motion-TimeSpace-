from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2621-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md"

PREFIX = "P8_Y5_SECTOR_VARIATION_GATE_2621"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "lineage_ledger": RESIDUALS / f"{PREFIX}_LINEAGE_LEDGER.csv",
    "variation_derivation": RESIDUALS / f"{PREFIX}_SECTOR_VARIATION_DERIVATION_ATTEMPT.csv",
    "scaling_estimate": RESIDUALS / f"{PREFIX}_LOCAL_SCALING_ESTIMATE_PACK.csv",
    "sector_verdict": RESIDUALS / f"{PREFIX}_SECTOR_VERDICT_MATRIX.csv",
    "deltae_norm": RESIDUALS / f"{PREFIX}_DELTAE_RESIDUAL_NORM_PACK.csv",
    "lovelock_audit": RESIDUALS / f"{PREFIX}_LOVEL0CK_HYPOTHESIS_AUDIT.csv",
    "empirical_bound_queue": RESIDUALS / f"{PREFIX}_EMPIRICAL_BOUND_QUEUE.csv",
    "countermodel": RESIDUALS / f"{PREFIX}_COUNTERMODEL_LEDGER.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2621_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2621_00_2620_handoff_doc",
        "description": "2620 selects sector variation/local scaling as the next target",
        "path": ROOT / "2620-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md",
        "needles": ["NEXT2620_0_primary", "SECTOR_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT", "SVA2620_6_nonlocal_history"],
    },
    {
        "source_id": "SRC2621_01_2620_validation",
        "description": "2620 validation passed",
        "path": RESIDUALS / "P8_Y5_BRR545_2620_VALIDATION.csv",
        "needles": ["VAL2620_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC2621_02_2620_sector_variation",
        "description": "2620 sector variation audit",
        "path": RESIDUALS / "P8_Y5_EH_DOMINANCE_GATE_2620_SECTOR_VARIATION_AUDIT.csv",
        "needles": ["SVA2620_0_EH_core", "SVA2620_6_nonlocal_history"],
    },
    {
        "source_id": "SRC2621_03_2620_scaling",
        "description": "2620 local scaling silence audit",
        "path": RESIDUALS / "P8_Y5_EH_DOMINANCE_GATE_2620_LOCAL_SCALING_SILENCE_AUDIT.csv",
        "needles": ["LSS2620_0_exact_zero_path", "LSS2620_4_verdict"],
    },
    {
        "source_id": "SRC2621_04_2620_coefficients",
        "description": "2620 operator coefficient pack",
        "path": RESIDUALS / "P8_Y5_EH_DOMINANCE_GATE_2620_OPERATOR_COEFFICIENT_PACK.csv",
        "needles": ["OPC2620_0_EH_normalization", "OPC2620_7_total_DeltaE"],
    },
    {
        "source_id": "SRC2621_05_2619_operator_pack",
        "description": "2619 original DeltaE operator pack",
        "path": RESIDUALS / "P8_Y5_GR_LEFT_HAND_GATE_2619_OPERATOR_RESIDUAL_PACK.csv",
        "needles": ["ORP2619_0_E_LHS_GR_residual", "ORP2619_8_nonclaim_lock"],
    },
]


def ensure_dirs() -> None:
    for path in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        text = read_text(source["path"])
        exists = source["path"].exists()
        rows.append(
            {
                "source_id": source["source_id"],
                "description": source["description"],
                "source_path": str(source["path"]),
                "exists": exists,
                "needles_present": exists and all(needle in text for needle in source["needles"]),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": False,
            }
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    return [
        {
            "lineage_id": "LIN2621_0_current_handoff",
            "input_checkpoint": "2620",
            "what_it_gave": "EH dominance contract plus sector list",
            "current_use": "give every sector a variation formula, scaling form, and verdict class",
            "claim_status": "nonclaim_handoff",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2621_1_deltae_object",
            "input_checkpoint": "2619",
            "what_it_gave": "DeltaE_munu as the exact local-GR obstruction",
            "current_use": "rewrite DeltaE_munu as a sum of sector residual norms",
            "claim_status": "residual_object_retained",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2621_2_derivation_philosophy",
            "input_checkpoint": "GR reduction programme",
            "what_it_gave": "GR recovery needs derivation, not fitted similarity",
            "current_use": "prefer Lovelock-hypothesis closure over empirical patching",
            "claim_status": "derivation_first",
            "valid_for_claim": False,
        },
    ]


def variation_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "variation_id": "VAR2621_0_EH_core",
            "sector": "Einstein-Hilbert core",
            "action_block": "S_EH=(a_EH/2) int sqrt(-g)(R-2 Lambda)",
            "euler_variation": "E_EH_munu=a_EH(G_munu+Lambda g_munu)",
            "local_silence_condition": "not silent; this is the desired dominant operator",
            "verdict_class": "DOMINANT_TEMPLATE_NOT_PARENT_NORMALIZED",
            "why_not_closed": "a_EH and G calibration remain parent-normalization tasks",
            "valid_for_claim": False,
        },
        {
            "variation_id": "VAR2621_1_boundary_topological",
            "sector": "topological / boundary / reference",
            "action_block": "S_top+S_bdy+S_ref",
            "euler_variation": "E_top_munu+E_bdy_munu; topological pieces can be locally silent, boundary pieces depend on allowed variations",
            "local_silence_condition": "fixed topology, fixed boundary data, compact-support variations, and reference chosen before readout",
            "verdict_class": "CONDITIONAL_ZERO_WITH_UNSIGNED_BOUNDARY_CLAUSE",
            "why_not_closed": "current branch lacks fixed-before-readout boundary/reference certificate",
            "valid_for_claim": False,
        },
        {
            "variation_id": "VAR2621_2_higher_derivative",
            "sector": "higher-curvature / higher-derivative",
            "action_block": "c_R2 R^2 + c_Ricci2 R_munu R^munu + c_boxR R box R",
            "euler_variation": "E_higher_munu carries fourth or higher derivatives and curvature-squared terms",
            "local_silence_condition": "operator absent/topological, or |c_i|/L_local^2 below tolerance for dimension-four examples",
            "verdict_class": "NONCLAIM_BOUND_REQUIRED",
            "why_not_closed": "operator basis, coefficients, and local scale hierarchy are not parent-sourced",
            "valid_for_claim": False,
        },
        {
            "variation_id": "VAR2621_3_projector",
            "sector": "projector/domain/readout",
            "action_block": "S_projector[Pi_M,q,e,Phi]",
            "euler_variation": "E_projector_munu plus commutator/readout obstruction [nabla,Pi_M]J_H",
            "local_silence_condition": "Pi_M is identity/commuting in local branch or the commutator norm is bounded",
            "verdict_class": "NONCLAIM_BOUND_REQUIRED",
            "why_not_closed": "no parent projector variation or commutator-zero proof",
            "valid_for_claim": False,
        },
        {
            "variation_id": "VAR2621_4_nonminimal",
            "sector": "nonminimal matter-geometry/MTS coupling",
            "action_block": "f(X,Phi)L_m or A(X)J_m",
            "euler_variation": "E_nonminimal_munu plus composition-dependent matter equation terms",
            "local_silence_condition": "term forbidden by parent grammar, universal and reclassified, or bounded by WEP/clock/PPN/R10 maps",
            "verdict_class": "NONCLAIM_BOUND_REQUIRED",
            "why_not_closed": "direct coupling would be heavily scrutinized and no forbid theorem is signed",
            "valid_for_claim": False,
        },
        {
            "variation_id": "VAR2621_5_memory_coframe",
            "sector": "memory/coframe/preferred-frame",
            "action_block": "S_memory+S_coframe+frame-lock terms",
            "euler_variation": "E_memory_munu+E_frame_munu and possible PPN alpha_i residuals",
            "local_silence_condition": "auxiliary elimination, local vacuum frame lock, or preferred-frame residual bounds",
            "verdict_class": "NONCLAIM_BOUND_REQUIRED",
            "why_not_closed": "local frame-lock theorem is not yet derived",
            "valid_for_claim": False,
        },
        {
            "variation_id": "VAR2621_6_nonlocal_history",
            "sector": "nonlocal/history kernel",
            "action_block": "S_nonlocal[g,Phi;history]",
            "euler_variation": "E_nonlocal_munu = integral K(t,t') O_munu(t') dt'",
            "local_silence_condition": "kernel collapses to local auxiliary term, adiabatic tail is negligible, or kernel bound is sourced",
            "verdict_class": "NONCLAIM_BOUND_REQUIRED",
            "why_not_closed": "no locality-reduction theorem or kernel bound",
            "valid_for_claim": False,
        },
    ]


def scaling_estimate_rows() -> list[dict[str, Any]]:
    return [
        {
            "scale_id": "SCL2621_0_EH_reference",
            "sector": "Einstein reference",
            "relative_scale": "||E_EH|| ~ a_EH/L_local^2",
            "needed_inputs": "local curvature length L_local and parent a_EH normalization",
            "current_status": "REFERENCE_SCALE_READY_SYMBOLIC",
            "observable_lane": "Newton G and PPN normalization",
            "valid_for_claim": False,
        },
        {
            "scale_id": "SCL2621_1_boundary",
            "sector": "boundary/topological",
            "relative_scale": "eta_bdy = ||E_bdy||/||E_EH||; eta_bdy=0 only under fixed-boundary compact-support conditions",
            "needed_inputs": "boundary variational class and reference-before-readout rule",
            "current_status": "MISSING_BOUNDARY_CLASS",
            "observable_lane": "mass charge, clocks, orbits",
            "valid_for_claim": False,
        },
        {
            "scale_id": "SCL2621_2_higher",
            "sector": "higher derivative",
            "relative_scale": "eta_R2 ~ |c_R2|/L_local^2; eta_boxR ~ |c_boxR|/L_local^4 for representative terms",
            "needed_inputs": "operator dimension, coefficient units, and L_local hierarchy",
            "current_status": "MISSING_COEFFICIENT_UNITS",
            "observable_lane": "R10, PPN, waves, cosmology",
            "valid_for_claim": False,
        },
        {
            "scale_id": "SCL2621_3_projector",
            "sector": "projector",
            "relative_scale": "eta_Pi <= L_local ||[nabla,Pi_M]|| + ||delta Pi_M/delta g||_local",
            "needed_inputs": "projector definition, commutator norm, and local domain theorem",
            "current_status": "MISSING_PROJECTOR_NORM",
            "observable_lane": "WEP, R10, measured GM, orbits",
            "valid_for_claim": False,
        },
        {
            "scale_id": "SCL2621_4_nonminimal",
            "sector": "nonminimal coupling",
            "relative_scale": "eta_nonmin ~ |partial ln A/partial X| |delta X| + |c_nonminimal f|",
            "needed_inputs": "coupling function, composition dependence, and matter-sector universality proof",
            "current_status": "MISSING_COUPLING_FUNCTION_OR_FORBID_THEOREM",
            "observable_lane": "WEP, clocks, PPN, R10",
            "valid_for_claim": False,
        },
        {
            "scale_id": "SCL2621_5_memory_frame",
            "sector": "memory/coframe",
            "relative_scale": "eta_frame maps to PPN alpha_i and clock-frame residuals",
            "needed_inputs": "frame-lock theorem or preferred-frame projection",
            "current_status": "MISSING_FRAME_LOCK_MAP",
            "observable_lane": "PPN preferred-frame, clocks, orbits",
            "valid_for_claim": False,
        },
        {
            "scale_id": "SCL2621_6_nonlocal",
            "sector": "nonlocal history",
            "relative_scale": "eta_K <= integral |K(t,t')| ||O(t')|| dt' / ||G||",
            "needed_inputs": "kernel support, decay, and local reduction theorem",
            "current_status": "MISSING_KERNEL_BOUND",
            "observable_lane": "clock drift, orbital hysteresis, cosmology growth",
            "valid_for_claim": False,
        },
    ]


def sector_verdict_rows() -> list[dict[str, Any]]:
    return [
        {
            "verdict_id": "VER2621_0_EH_core",
            "sector": "EH core",
            "allowed_statuses": "DOMINANT",
            "current_verdict": "DOMINANT_TEMPLATE_NOT_PARENT_NORMALIZED",
            "gr_risk": "normalization/G calibration open",
            "next_needed": "parent a_EH and source normalization",
            "valid_for_claim": False,
        },
        {
            "verdict_id": "VER2621_1_boundary",
            "sector": "boundary/topological",
            "allowed_statuses": "ZERO or NONCLAIM_BOUND_REQUIRED",
            "current_verdict": "CONDITIONAL_ZERO_UNSIGNED",
            "gr_risk": "boundary/reference can fake mass or potential readout",
            "next_needed": "fixed-before-readout boundary certificate",
            "valid_for_claim": False,
        },
        {
            "verdict_id": "VER2621_2_higher_derivative",
            "sector": "higher derivative",
            "allowed_statuses": "ZERO, SUPPRESSED_WITH_UNITS, or NONCLAIM_BOUND_REQUIRED",
            "current_verdict": "NONCLAIM_BOUND_REQUIRED",
            "gr_risk": "Yukawa/PPN/wave residual tails",
            "next_needed": "operator basis plus units and coefficient bounds",
            "valid_for_claim": False,
        },
        {
            "verdict_id": "VER2621_3_projector",
            "sector": "projector",
            "allowed_statuses": "ZERO_COMMUTATOR, RECLASSIFIED, or NONCLAIM_BOUND_REQUIRED",
            "current_verdict": "NONCLAIM_BOUND_REQUIRED",
            "gr_risk": "mass/source readout and WEP contamination",
            "next_needed": "commutator-zero or projector norm",
            "valid_for_claim": False,
        },
        {
            "verdict_id": "VER2621_4_nonminimal",
            "sector": "nonminimal coupling",
            "allowed_statuses": "FORBIDDEN, UNIVERSAL_RECLASSIFIED, or NONCLAIM_BOUND_REQUIRED",
            "current_verdict": "NONCLAIM_BOUND_REQUIRED",
            "gr_risk": "WEP/clock/PPN failures",
            "next_needed": "forbid theorem or explicit coupling bounds",
            "valid_for_claim": False,
        },
        {
            "verdict_id": "VER2621_5_memory_coframe",
            "sector": "memory/coframe",
            "allowed_statuses": "FRAME_LOCKED, AUXILIARY, or NONCLAIM_BOUND_REQUIRED",
            "current_verdict": "NONCLAIM_BOUND_REQUIRED",
            "gr_risk": "preferred-frame and local clock residuals",
            "next_needed": "local frame-lock proof",
            "valid_for_claim": False,
        },
        {
            "verdict_id": "VER2621_6_nonlocal_history",
            "sector": "nonlocal/history",
            "allowed_statuses": "LOCAL_REDUCED, SUPPRESSED_WITH_KERNEL_BOUND, or NONCLAIM_BOUND_REQUIRED",
            "current_verdict": "NONCLAIM_BOUND_REQUIRED",
            "gr_risk": "history-dependent local gravity",
            "next_needed": "kernel decay/locality reduction",
            "valid_for_claim": False,
        },
        {
            "verdict_id": "VER2621_7_overall",
            "sector": "DeltaE_munu total",
            "allowed_statuses": "ALL_SECTORS_CLOSED",
            "current_verdict": "LOCAL_GR_NOT_CLOSED",
            "gr_risk": "at least five sectors still require bounds or zero theorems",
            "next_needed": "Lovelock-hypothesis audit or sector coefficient sourcing",
            "valid_for_claim": False,
        },
    ]


def deltae_norm_rows() -> list[dict[str, Any]]:
    return [
        {
            "norm_id": "NORM2621_0_total",
            "residual": "DeltaE_munu",
            "bound_form": "||DeltaE||/||G|| <= eta_bdy + eta_R2 + eta_Pi + eta_nonmin + eta_frame + eta_K",
            "closed_terms": "none fully closed",
            "open_terms": "eta_bdy, eta_R2, eta_Pi, eta_nonmin, eta_frame, eta_K",
            "current_status": "SYMBOLIC_BOUND_ONLY_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "norm_id": "NORM2621_1_no_cancellation_guard",
            "residual": "sector sum",
            "bound_form": "use absolute-sum sector bounds, not cancellation in one observable",
            "closed_terms": "guard written",
            "open_terms": "numeric sector bounds missing",
            "current_status": "NO_CANCELLATION_POLICY_READY",
            "valid_for_claim": False,
        },
        {
            "norm_id": "NORM2621_2_claim_threshold",
            "residual": "local tolerance",
            "bound_form": "claim allowed only if ||DeltaE||/||G|| <= min(tau_R10,tau_PPN,tau_clock,tau_orbital)",
            "closed_terms": "threshold structure written",
            "open_terms": "arena tolerances and projections missing",
            "current_status": "THRESHOLD_SYMBOLIC_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def lovelock_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "LOV2621_0_dimension",
            "hypothesis": "four-dimensional local branch",
            "needed_evidence": "local effective theory is 4D for the tested arena",
            "current_status": "LIKELY_BUT_NOT_CERTIFIED_HERE",
            "blocker": "write explicit local branch dimensional assumption/certificate",
            "valid_for_claim": False,
        },
        {
            "audit_id": "LOV2621_1_metric_only",
            "hypothesis": "metric-only or extra fields auxiliary/gauge/frozen",
            "needed_evidence": "motion/time/memory/coframe variables do not produce independent local Euler equations",
            "current_status": "NOT_PROVED",
            "blocker": "memory/coframe/nonlocal sectors remain live",
            "valid_for_claim": False,
        },
        {
            "audit_id": "LOV2621_2_second_order",
            "hypothesis": "second-order field equations",
            "needed_evidence": "higher-derivative operators absent or suppressed",
            "current_status": "NOT_PROVED",
            "blocker": "higher-derivative basis and scale not closed",
            "valid_for_claim": False,
        },
        {
            "audit_id": "LOV2621_3_divergence_free",
            "hypothesis": "Noether/Bianchi-compatible LHS",
            "needed_evidence": "complete diffeomorphism-invariant parent action with no illegal dropped terms",
            "current_status": "PARTLY_STRUCTURED_NOT_SIGNED",
            "blocker": "complete parent action inventory still unsigned",
            "valid_for_claim": False,
        },
        {
            "audit_id": "LOV2621_4_next",
            "hypothesis": "lowest-scrutiny route to GR",
            "needed_evidence": "prove metric-only/second-order/local/no-extra-field hypotheses or retain residual coefficients",
            "current_status": "LOVEL0CK_HYPOTHESIS_AUDIT_IS_NEXT",
            "blocker": "sector rows identify exact hypotheses to close",
            "valid_for_claim": False,
        },
    ]


def empirical_bound_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "EBQ2621_0_R10",
            "arena": "short-range gravity",
            "required_inputs": "eta_R2, eta_Pi, eta_nonmin projected to alpha(lambda)",
            "status": "SOURCE_BACKED_MAP_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "queue_id": "EBQ2621_1_PPN",
            "arena": "solar-system PPN",
            "required_inputs": "eta_frame, eta_R2, eta_Pi mapped to gamma,beta,alpha_i",
            "status": "SOURCE_BACKED_MAP_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "queue_id": "EBQ2621_2_clocks",
            "arena": "clock tests",
            "required_inputs": "eta_nonmin and eta_frame redshift projection",
            "status": "SOURCE_BACKED_MAP_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "queue_id": "EBQ2621_3_orbits",
            "arena": "orbital dynamics",
            "required_inputs": "eta_bdy, eta_Pi, eta_total plus worldtube/Gauss chain",
            "status": "SOURCE_BACKED_MAP_REQUIRED",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM2621_0_sector_left_unvaried",
            "failure_mode": "one non-EH sector remains unvaried but is assumed silent",
            "mathematical_form": "exists i: delta S_i/delta g != 0 but omitted from DeltaE",
            "retained": True,
            "why_survives": "several sectors still lack variation certificates",
            "what_kills_it": "sector-by-sector ZERO/SUPPRESSED/RECLASSIFIED verdicts",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2621_1_scale_without_dimension",
            "failure_mode": "operator residual is called tiny without dimensional scale",
            "mathematical_form": "eta_i << 1 without c_i units or L_local",
            "retained": True,
            "why_survives": "coefficient units and local scale hierarchy are incomplete",
            "what_kills_it": "dimensioned coefficient rows and arena tolerances",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2621_2_lovelock_gap",
            "failure_mode": "Lovelock theorem is invoked while its hypotheses are not met",
            "mathematical_form": "extra fields or higher derivatives survive in local branch",
            "retained": True,
            "why_survives": "metric-only and second-order hypotheses are not proven",
            "what_kills_it": "2622 Lovelock-hypothesis audit closes every hypothesis",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2621_3_verdict",
            "failure_mode": "local GR remains unclosed after sector audit",
            "mathematical_form": "DeltaE/G <= symbolic eta_total with open terms",
            "retained": True,
            "why_survives": "2621 gives formulas but not sufficient evidence to zero/bound all sectors",
            "what_kills_it": "close Lovelock hypotheses or source numeric operator bounds",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2621_0_all_sectors_closed",
            "claim": "all non-EH sectors are zero/suppressed/reclassified",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SECTOR_VERDICTS_OPEN",
        },
        {
            "gate_id": "GATE2621_1_deltae_bound",
            "claim": "DeltaE_munu is below all local tolerances",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_NUMERIC_TOLERANCE_MAPS_MISSING",
        },
        {
            "gate_id": "GATE2621_2_lovelock_route",
            "claim": "Lovelock-style GR uniqueness hypotheses hold",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_METRIC_ONLY_SECOND_ORDER_LOCAL_HYPOTHESES_UNSIGNED",
        },
        {
            "gate_id": "GATE2621_3_local_GR",
            "claim": "local GR/Newton branch is derived",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_DELTAE_AND_SOURCE_NORMALIZATION_OPEN",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2621_0_real_gain",
            "decision": "DELTAE_IS_NOW_SECTOR_RESOLVED",
            "reason": "DeltaE_munu is no longer one blob; it has explicit sector formulas and scaling placeholders",
            "next_action": "close the hypotheses that kill several sectors at once",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2621_1_no_local_gr_claim",
            "decision": "LOCAL_GR_STILL_BLOCKED",
            "reason": "sector variation formulas exist but silence/bounds are not proven",
            "next_action": "keep local GR/Newton/R10/PPN gates blocked",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2621_2_best_next",
            "decision": "LOVEL0CK_HYPOTHESIS_AUDIT_IS_NEXT",
            "reason": "the least-scrutiny route is proving metric-only/second-order/local/no-extra-field conditions rather than bounding every residual separately",
            "next_action": "build 2622 Lovelock-hypothesis audit or residual-bounds fallback",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2621_0_primary",
            "selection_status": "selected",
            "target_doc": "2622-Y5-R2FR-Lovelock-hypothesis-audit-metric-only-second-order-or-residual-bounds.md",
            "target_script": "scripts/Y5_R2FR_Lovelock_hypothesis_audit_metric_only_second_order_or_residual_bounds_2622.py",
            "objective": "prove or reject the low-scrutiny GR route: local 4D, metric-only, second-order, divergence-free parent LHS; otherwise retain explicit residual coefficients",
            "acceptance_gate": "each Lovelock hypothesis is PASS, FAIL_TO_BOUND, or NONCLAIM_BOUND_REQUIRED with source rows",
            "claim_policy": "no local-GR claim unless all hypotheses pass and source normalization later closes",
            "valid_for_claim": False,
        },
        {
            "route_id": "NEXT2621_1_fallback",
            "selection_status": "held_fallback",
            "target_doc": "2622b-Y5-R2FR-operator-coefficient-source-bound-pack.md",
            "target_script": "scripts/Y5_R2FR_operator_coefficient_source_bound_pack_2622b.py",
            "objective": "source numeric coefficient bounds for sectors that fail the Lovelock route",
            "acceptance_gate": "every coefficient has units, source path, observable map, and valid_for_claim=false until fully sourced",
            "claim_policy": "fallback only after derivation-first route fails",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "variation": variation_derivation_rows(),
        "scaling": scaling_estimate_rows(),
        "verdict": sector_verdict_rows(),
        "norm": deltae_norm_rows(),
        "lovelock": lovelock_audit_rows(),
        "bound_queue": empirical_bound_queue_rows(),
        "countermodel": countermodel_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
        "branch_copies": [],
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_parse(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return True, sum(1 for _ in csv.DictReader(handle))
    except Exception:
        return False, 0


def copy_outputs() -> list[dict[str, Any]]:
    specs = [
        ("COPY2621_variation", "variation_derivation", OUTPUTS["variation_derivation"], LOCAL_BOUNDS / "Sector_variation_derivation_2621_NONCLAIM.csv"),
        ("COPY2621_scaling", "scaling_estimate", OUTPUTS["scaling_estimate"], LOCAL_BOUNDS / "Local_scaling_estimate_2621_NONCLAIM.csv"),
        ("COPY2621_verdict", "sector_verdict", OUTPUTS["sector_verdict"], LOCAL_BOUNDS / "Sector_verdict_matrix_2621_NONCLAIM.csv"),
        ("COPY2621_deltae_norm", "deltae_norm", OUTPUTS["deltae_norm"], LOCAL_BOUNDS / "DeltaE_residual_norm_pack_2621_NONCLAIM.csv"),
        ("COPY2621_next_target", "next_target", OUTPUTS["next_target"], RAB_QUEUE / "JR2621_LOVEL0CK_HYPOTHESIS_AUDIT_NEXT.csv"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_key, source, target in specs:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        parsed, row_count = csv_parse(target)
        rows.append(
            {
                "copy_id": copy_id,
                "source_key": source_key,
                "copy_path": str(target),
                "copy_exists": target.exists(),
                "csv_parse": parsed,
                "row_count": row_count,
                "valid_for_claim": False,
            }
        )
    return rows


def sources_pass(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(row["exists"] and row["needles_present"] for row in rows_map["sources"])


def variation_rows_complete(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    required = {f"VAR2621_{index}_{suffix}" for index, suffix in [
        (0, "EH_core"),
        (1, "boundary_topological"),
        (2, "higher_derivative"),
        (3, "projector"),
        (4, "nonminimal"),
        (5, "memory_coframe"),
        (6, "nonlocal_history"),
    ]}
    return required.issubset({row["variation_id"] for row in rows_map["variation"]})


def scaling_rows_complete(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["scale_id"] == "SCL2621_6_nonlocal" for row in rows_map["scaling"]) and all(
        not bool(row["valid_for_claim"]) for row in rows_map["scaling"]
    )


def verdict_overall_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["verdict_id"] == "VER2621_7_overall"
        and row["current_verdict"] == "LOCAL_GR_NOT_CLOSED"
        and not bool(row["valid_for_claim"])
        for row in rows_map["verdict"]
    )


def deltae_norm_symbolic(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["norm_id"] == "NORM2621_0_total"
        and row["current_status"] == "SYMBOLIC_BOUND_ONLY_NONCLAIM"
        and "eta_bdy" in row["bound_form"]
        for row in rows_map["norm"]
    )


def lovelock_next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["audit_id"] == "LOV2621_4_next"
        and row["current_status"] == "LOVEL0CK_HYPOTHESIS_AUDIT_IS_NEXT"
        for row in rows_map["lovelock"]
    )


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["countermodel_id"] == "CM2621_3_verdict" and bool(row["retained"]) for row in rows_map["countermodel"])


def claim_gates_safe(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(not bool(row["claim_allowed"]) and row["status"] == "BLOCKED" for row in rows_map["claim_gates"])


def generated_rows_have_no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    claim_like_keys = {"valid_for_claim", "claim_allowed", "score_ready", "claim_ready", "public_claim_allowed"}
    for rows in rows_map.values():
        for row in rows:
            for field, value in row.items():
                if field in claim_like_keys and bool(value):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            joined = " ".join(str(value) for value in row.values())
            if "MISSING_" in joined and bool(row.get("valid_for_claim", False)):
                return False
            if "MISSING_" in joined and str(row.get("current_status", "")).upper() == "READY":
                return False
    return True


def decision_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["decision_id"] == "DEC2621_2_best_next"
        and row["decision"] == "LOVEL0CK_HYPOTHESIS_AUDIT_IS_NEXT"
        for row in rows_map["decisions"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["route_id"] == "NEXT2621_0_primary" and row["selection_status"] == "selected" for row in rows_map["next"])


def no_formalization_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*2621*"))


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def csv_parse_all() -> bool:
    return all(csv_parse(path)[0] for key, path in OUTPUTS.items() if key != "validation" and path.exists())


def branch_copies_pass(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return bool(rows_map["branch_copies"]) and all(row["copy_exists"] and row["csv_parse"] for row in rows_map["branch_copies"])


def check_row(check_id: str, passed: bool, detail: str, blocker: str = "") -> dict[str, Any]:
    return {
        "check_id": check_id,
        "result": "PASS" if passed else "FAIL",
        "detail": detail if passed else blocker,
        "valid_for_claim": False,
    }


def validation_rows(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = [
        check_row("VAL2621_00_sources_exist", sources_pass(rows_map), "all cited source paths exist and needles are present", "one or more cited source paths or needles missing"),
        check_row("VAL2621_01_variation_rows_complete", variation_rows_complete(rows_map), "all sector variation rows are present", "one or more sector variation rows missing"),
        check_row("VAL2621_02_scaling_rows_complete", scaling_rows_complete(rows_map), "all scaling rows remain nonclaim and include nonlocal sector", "scaling rows incomplete or promoted"),
        check_row("VAL2621_03_verdict_overall_blocked", verdict_overall_blocked(rows_map), "overall local-GR verdict remains blocked", "overall verdict missing or promoted"),
        check_row("VAL2621_04_deltae_norm_symbolic", deltae_norm_symbolic(rows_map), "DeltaE norm pack is symbolic/nonclaim", "DeltaE norm pack missing or promoted"),
        check_row("VAL2621_05_lovelock_next", lovelock_next_selected(rows_map), "Lovelock-hypothesis audit selected next", "Lovelock next audit missing"),
        check_row("VAL2621_06_countermodel_retained", countermodel_retained(rows_map), "sector-audit countermodel remains retained", "countermodel missing or promoted"),
        check_row("VAL2621_07_claim_gates_safe", claim_gates_safe(rows_map), "all claim gates remain blocked/nonclaim", "one or more claim gates opened"),
        check_row("VAL2621_08_no_claim_flags", generated_rows_have_no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL2621_09_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row("VAL2621_10_formalization_untouched", no_formalization_artifacts(), "no 2621 outputs found under formalization-workbench", "2621 outputs found under formalization-workbench"),
        check_row("VAL2621_11_decision_next", decision_next(rows_map), "decision selects Lovelock-hypothesis audit", "decision route missing"),
        check_row("VAL2621_12_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL2621_13_branch_copies", branch_copies_pass(rows_map), "branch/local/queue copies exist and parse", "branch copies missing or malformed"),
        check_row("VAL2621_14_csv_parse", csv_parse_all(), "all generated 2621 CSVs parse", "one or more generated 2621 CSVs fail to parse"),
        check_row("VAL2621_15_pycache_absent", pycache_absent(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
    ]
    overall = all(row["result"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL2621_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2621 sector action variation and local scaling silence or operator bounds",
            "valid_for_claim": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, divider, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validations: list[dict[str, Any]]) -> str:
    sections = [
        "# 2621 - Sector Action Variation And Local Scaling Silence Or Operator Bounds",
        "## Summary\n"
        "- 2621 splits `DeltaE_munu` into sector-level variation and scaling rows.\n"
        "- The result is not a local-GR proof; it is a sharper map of what must be killed or bounded.\n"
        "- The strongest next route is the Lovelock-style hypothesis audit: prove local 4D metric-only second-order divergence-free dynamics, or keep residual coefficients.\n"
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "## Source Register\n" + markdown_table(rows_map["sources"], ["source_id", "description", "source_path", "exists", "needles_present"]),
        "## Lineage Ledger\n" + markdown_table(rows_map["lineage"], ["lineage_id", "input_checkpoint", "what_it_gave", "current_use", "claim_status"]),
        "## Sector Variation Derivation Attempt\n" + markdown_table(rows_map["variation"], ["variation_id", "sector", "action_block", "euler_variation", "local_silence_condition", "verdict_class", "why_not_closed"]),
        "## Local Scaling Estimate Pack\n" + markdown_table(rows_map["scaling"], ["scale_id", "sector", "relative_scale", "needed_inputs", "current_status", "observable_lane"]),
        "## Sector Verdict Matrix\n" + markdown_table(rows_map["verdict"], ["verdict_id", "sector", "allowed_statuses", "current_verdict", "gr_risk", "next_needed"]),
        "## DeltaE Residual Norm Pack\n" + markdown_table(rows_map["norm"], ["norm_id", "residual", "bound_form", "closed_terms", "open_terms", "current_status"]),
        "## Lovelock Hypothesis Audit\n" + markdown_table(rows_map["lovelock"], ["audit_id", "hypothesis", "needed_evidence", "current_status", "blocker"]),
        "## Empirical Bound Queue\n" + markdown_table(rows_map["bound_queue"], ["queue_id", "arena", "required_inputs", "status"]),
        "## Countermodel Ledger\n" + markdown_table(rows_map["countermodel"], ["countermodel_id", "failure_mode", "mathematical_form", "retained", "why_survives", "what_kills_it"]),
        "## Claim Gates\n" + markdown_table(rows_map["claim_gates"], ["gate_id", "claim", "claim_allowed", "status", "blocker"]),
        "## Decision Ledger\n" + markdown_table(rows_map["decisions"], ["decision_id", "decision", "reason", "next_action"]),
        "## Next Target\n" + markdown_table(rows_map["next"], ["route_id", "selection_status", "target_doc", "target_script", "objective", "acceptance_gate", "claim_policy"]),
        "## Branch Copies\n" + markdown_table(rows_map["branch_copies"], ["copy_id", "source_key", "copy_path", "copy_exists", "csv_parse", "row_count"]),
        "## Validation\n" + markdown_table(validations, ["check_id", "result", "detail", "valid_for_claim"]),
        "## Verdict\n"
        "This is real progress but not a green flag for GR yet. The project has moved from a vague left-hand obstruction to a sector-resolved residual norm. The best next shot is not to fit the residuals; it is to prove the Lovelock-style hypotheses locally. If that fails, the same sector rows become the coefficient-bound programme.",
    ]
    return "\n\n".join(sections) + "\n"


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    write_csv(OUTPUTS["source_register"], rows_map["sources"])
    write_csv(OUTPUTS["lineage_ledger"], rows_map["lineage"])
    write_csv(OUTPUTS["variation_derivation"], rows_map["variation"])
    write_csv(OUTPUTS["scaling_estimate"], rows_map["scaling"])
    write_csv(OUTPUTS["sector_verdict"], rows_map["verdict"])
    write_csv(OUTPUTS["deltae_norm"], rows_map["norm"])
    write_csv(OUTPUTS["lovelock_audit"], rows_map["lovelock"])
    write_csv(OUTPUTS["empirical_bound_queue"], rows_map["bound_queue"])
    write_csv(OUTPUTS["countermodel"], rows_map["countermodel"])
    write_csv(OUTPUTS["claim_gates"], rows_map["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], rows_map["decisions"])
    write_csv(OUTPUTS["next_target"], rows_map["next"])
    rows_map["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], rows_map["branch_copies"])
    validations = validation_rows(rows_map)
    write_csv(OUTPUTS["validation"], validations)
    DOC_PATH.write_text(build_markdown(rows_map, validations), encoding="utf-8")
    print(f"2621 validation {validations[-1]['result']}")
    print(f"doc={DOC_PATH}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
