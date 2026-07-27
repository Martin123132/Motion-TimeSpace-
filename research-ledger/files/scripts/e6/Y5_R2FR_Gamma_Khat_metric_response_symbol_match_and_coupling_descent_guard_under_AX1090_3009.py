from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3009"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3009-Y5-R2FR-Gamma-Khat-metric-response-symbol-match-and-coupling-descent-guard-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3009_SOURCE_REGISTER.csv",
    "symbol_match": RESIDUALS / "P8_Y5_R2FR_3009_REAL_SYMBOL_MATCH_AUDIT.csv",
    "delta_k": RESIDUALS / "P8_Y5_R2FR_3009_DELTA_K_OBSTRUCTION_DECOMPOSITION.csv",
    "coupling": RESIDUALS / "P8_Y5_R2FR_3009_COUPLING_DESCENT_GUARD_AUDIT.csv",
    "residual_interface": RESIDUALS / "P8_Y5_R2FR_3009_SOURCE_READY_RESIDUAL_INTERFACE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3009_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3009_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3009_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3009_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3009_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "symbol_match_copy": PARENT_ACTION / "Gamma_Khat_metric_response_symbol_match_3009_NOT_SIGNED.csv",
    "delta_k_copy": LOCAL_BOUNDS / "Delta_K_q_loc_obstruction_rows_3009_NONCLAIM.csv",
    "coupling_copy": LOCAL_BOUNDS / "coupling_descent_guard_rows_3009_NONCLAIM.csv",
    "residual_interface_copy": LOCAL_BOUNDS / "q_loc_coupling_source_ready_residual_interface_3009_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3009_RESPONSE_OPERATOR_OR_RESIDUAL_BOUND_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def missing_anchors(path: Path, needles: list[str]) -> str:
    haystack = text(path)
    return "; ".join(needle for needle in needles if needle not in haystack)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [str(output_row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


SOURCE_SPECS = [
    ("SRC3009_00_3008_next", RESIDUALS / "P8_Y5_R2FR_3008_NEXT_TARGET.csv", ["NEXT3008_0_3009", "metric-response identity"], "3008 selects real symbol match and coupling descent guard."),
    ("SRC3009_01_3008_doc", ROOT / "3008-Y5-R2FR-Gamma-Khat-q_loc-action-existence-or-explicit-residual-split-under-AX1090.md", ["current MTS does not yet prove", "NEXT3008_0_3009"], "3008 refuses q_loc promotion and points to 3009."),
    ("SRC3009_02_3008_theorem", RESIDUALS / "P8_Y5_R2FR_3008_METRIC_RESPONSE_WARD_THEOREM.csv", ["MRW3008_2_q_loc_as_projected_Ward_residual", "MRW3008_6_current_status"], "3008 metric-response Ward theorem and current-status blocker."),
    ("SRC3009_03_3008_residual", RESIDUALS / "P8_Y5_R2FR_3008_EXPLICIT_QLOC_RESIDUAL_SPLIT.csv", ["QRES3008_0_metric_response_mismatch", "QRES3008_7_total_no_cancellation"], "3008 explicit q_loc residual split."),
    ("SRC3009_04_3008_coupling", RESIDUALS / "P8_Y5_R2FR_3008_COUPLING_GUARD_ROWS.csv", ["CG3008_0_q_only_geometry", "CG3008_6_guard_verdict"], "3008 coupling guard rows."),
    ("SRC3009_05_MA515_match", RESIDUALS / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv", ["MA515_0_Gamma_scalar_density_owner", "MA515_6_units_and_readout"], "515 match audit: Gamma density, Khat response and units fail current claim."),
    ("SRC3009_06_KMR2409", RESIDUALS / "P8_Y5_PARENT_QLOC_2409_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv", ["KMR2409_0_candidate_density", "KMR2409_5_overall"], "2409 Khat metric-response match: only formal variation passes."),
    ("SRC3009_07_MR2975", RESIDUALS / "P8_Y5_R2FR_2975_METRIC_RESPONSE_CERTIFICATE_AUDIT.csv", ["MR2975_0_Gamma_density", "MR2975_6_verdict"], "2975 certificate audit keeps K_hat=K_metric not derived."),
    ("SRC3009_08_GKM2807", RESIDUALS / "P8_Y5_R2FR_2807_GAMMA_KHAT_METRIC_RESPONSE_MATCH.csv", ["GKM2807_0_metric_response_identity", "GKM2807_3_verdict"], "2807 direct Gamma/Khat match says symbol match missing."),
    ("SRC3009_09_MRD2808", RESIDUALS / "P8_Y5_R2FR_2808_METRIC_RESPONSE_DERIVATION_ATTEMPT.csv", ["MRD2808_0_action", "MRD2808_6_verdict"], "2808 derives the obstruction identity q_loc = Ward residual plus Delta_K."),
    ("SRC3009_10_GMV2409", RESIDUALS / "P8_Y5_PARENT_QLOC_2409_GAMMA_EFF_METRIC_VARIATION_MERGE.csv", ["GMV2409_0_response_doublet", "GMV2409_3_current_verdict"], "2409 formal Gamma_eff metric variation merged as nonclaim."),
    ("SRC3009_11_KRS2111", RESIDUALS / "P8_Y5_PARENT_QLOC_2111_KMETRIC_RESPONSE_SPLIT.csv", ["KRS2111_0_total_split", "KRS2111_8_deltaK"], "2111 decomposes K_metric and Delta_K residual channels."),
    ("SRC3009_12_KLC2220", RESIDUALS / "P8_Y5_PARENT_QLOC_2220_KL_VARIATION_AND_COEFFICIENT_CONTRACT.csv", ["KLC2220_0_variation_identity", "KLC2220_6_verdict"], "2220 supplies a real conditional trace-free response contract but not live Khat adoption."),
    ("SRC3009_13_matter2611", RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv", ["PRE2611_0_q_map", "PRE2611_8_verdict"], "2611 matter descent premises fail current claim."),
    ("SRC3009_14_prefactor2612", RESIDUALS / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_PREFACTOR_CLASSIFICATION.csv", ["SP2612_0_absent_slot", "SP2612_6_readout_worldtube"], "2612 hidden source-prefactor countermodels."),
    ("SRC3009_15_coupling2660", RESIDUALS / "P8_Y5_COUPLING_VECTOR_2660_COUPLING_RESIDUAL_VECTOR_SCHEMA.csv", ["CV2660_0_c_g", "CV2660_7_total_policy"], "2660 coupling residual vector schema."),
]

source_rows = [
    base(
        {
            "source_id": source_id,
            "source_path": str(path),
            "path_exists": path.exists(),
            "required_anchors": "; ".join(required),
            "anchors_found": anchors(path, required),
            "missing_anchors": missing_anchors(path, required),
            "role": role,
        }
    )
    for source_id, path, required, role in SOURCE_SPECS
]


symbol_match_rows = [
    base(
        {
            "match_id": "SYM3009_0_Gamma_density",
            "required_identity": "Gamma_eff is a source-owned covariant scalar density Gamma_eff(g,Phi,nabla Phi,D,...) with units and boundary convention.",
            "current_evidence": "Formal candidate densities exist, but live Gamma_eff remains a route/readout/relaxation symbol rather than a sourced density.",
            "pass_now": False,
            "defect_symbol": "Delta_Gamma_density_owner",
            "effect": "without this, there is no specific S_GK to vary",
            "source_anchors": "MA515_0_Gamma_scalar_density_owner;KMR2409_0_candidate_density;MR2975_0_Gamma_density",
        }
    ),
    base(
        {
            "match_id": "SYM3009_1_formal_variation",
            "required_identity": "K_metric^{mu nu}=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_{mu nu} is computed with sign, volume, derivative and boundary conventions.",
            "current_evidence": "Formal metric variation is written for candidate response-doublet/auxiliary branches.",
            "pass_now": True,
            "defect_symbol": "none_for_formal_step",
            "effect": "the mathematical route is real as a contract",
            "source_anchors": "KMR2409_1_formal_variation;GMV2409_0_response_doublet;MRD2808_1_stress_split",
        }
    ),
    base(
        {
            "match_id": "SYM3009_2_Khat_identity",
            "required_identity": "live K_hat^{mu nu}=K_metric^{mu nu}[Gamma_eff] component-by-component under one convention.",
            "current_evidence": "No source proves live K_hat is the metric response; existing files explicitly mark this missing.",
            "pass_now": False,
            "defect_symbol": "Delta_K_metric_response_defect",
            "effect": "q_loc retains an extra P_loc div Delta_K term",
            "source_anchors": "MA515_1_Khat_metric_response;KMR2409_2_Khat_identity;MR2975_3_Khat_match",
        }
    ),
    base(
        {
            "match_id": "SYM3009_3_component_split",
            "required_identity": "K_metric split terms are either matched to live K_hat, theorem-zero, or retained with source-ready residual names.",
            "current_evidence": "KRS2111 splits volume/m-chain/L-chain/connection/domain/boundary/projector; only closure-style pieces are conditionally controlled.",
            "pass_now": False,
            "defect_symbol": "Delta_K_component_vector_abs",
            "effect": "connection, domain, boundary and projector tails remain live",
            "source_anchors": "KRS2111_0_total_split;KRS2111_8_deltaK",
        }
    ),
    base(
        {
            "match_id": "SYM3009_4_double_zero",
            "required_identity": "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0 for physical q_loc components.",
            "current_evidence": "response-doublet formal double-zero exists, but no physical q_loc component map or zero odd source theorem closes it.",
            "pass_now": False,
            "defect_symbol": "epsilon_C0_C1_GammaKhat_abs",
            "effect": "F_1 cannot be set to zero for current MTS",
            "source_anchors": "KMR2409_3_double_zero;GMV2409_0_response_doublet",
        }
    ),
    base(
        {
            "match_id": "SYM3009_5_units_readout",
            "required_identity": "Gamma/Khat/q_loc units and projections map to R10/PPN/clock/orbital arenas.",
            "current_evidence": "unit-normalized response map is missing; current rows are symbolic and non-score-ready.",
            "pass_now": False,
            "defect_symbol": "q_units_response_defect",
            "effect": "cannot score the local residual vector yet",
            "source_anchors": "MA515_6_units_and_readout;KMR2409_4_units_readout",
        }
    ),
    base(
        {
            "match_id": "SYM3009_6_symbol_match_verdict",
            "required_identity": "all rows SYM3009_0..5 pass in one branch.",
            "current_evidence": "only formal variation passes; live density owner, Khat identity, component split, double-zero and units fail or remain open.",
            "pass_now": False,
            "defect_symbol": "q_loc_symbol_match_total_abs",
            "effect": "q_loc zero/local GR remains nonclaim; move to Delta_K residual interface",
            "source_anchors": "KMR2409_5_overall;MR2975_6_verdict;MRD2808_6_verdict",
        }
    ),
]


delta_k_rows = [
    base(
        {
            "delta_id": "DK3009_0_identity",
            "component": "Delta_K_total",
            "definition": "Delta_K^{mu nu}:=K_hat_live^{mu nu}-K_metric^{mu nu}[Gamma_eff]",
            "status": "RETAIN_EXPLICIT",
            "residual_formula": "q_loc^nu=P_loc(nabla_mu T_GK^{mu nu})-P_loc(nabla_mu Delta_K^{mu nu}) plus projector/boundary convention terms",
            "source_needed": "live K_hat component map and K_metric component map",
            "source_anchors": "MRD2808_3_projected_q_loc;KRS2111_8_deltaK",
        }
    ),
    base(
        {
            "delta_id": "DK3009_1_volume",
            "component": "K_vol",
            "definition": "metric-proportional volume/subtraction response",
            "status": "CONDITIONAL_CLOSURE_NOT_CLAIM",
            "residual_formula": "epsilon_K_vol_abs if Gamma0/subtraction is not parent-fixed",
            "source_needed": "parent adoption of source-independent subtraction",
            "source_anchors": "KRS2111_1_volume",
        }
    ),
    base(
        {
            "delta_id": "DK3009_2_m_chain",
            "component": "K_m",
            "definition": "first response of mass/load chain around local branch",
            "status": "CONDITIONAL_DOUBLE_ZERO_NOT_CLAIM",
            "residual_formula": "epsilon_K_m_abs proportional to Fhat_prime(m_*) displacement if fixed branch fails",
            "source_needed": "locked m branch and amplitude law",
            "source_anchors": "KRS2111_2_m_chain",
        }
    ),
    base(
        {
            "delta_id": "DK3009_3_L_chain_tracefree",
            "component": "K_L / tracefree response",
            "definition": "variation/coefficient response, including possible trace-free improvement",
            "status": "REAL_CONDITIONAL_MATH_NOT_LIVE_CERTIFICATE",
            "residual_formula": "epsilon_K_L_abs if sigma_resp*c_I law or live adoption fails",
            "source_needed": "coefficient/sign source and parent adoption",
            "source_anchors": "KLC2220_1_tracefree_projection;KLC2220_2_coefficient_law;KLC2220_6_verdict",
        }
    ),
    base(
        {
            "delta_id": "DK3009_4_connection_kernel",
            "component": "K_conn",
            "definition": "connection/derivative/nonlocal kernel response hidden in Gamma_eff or K_hat",
            "status": "OPEN_RETAINED_RESIDUAL",
            "residual_formula": "epsilon_K_conn_abs from derivative/connection metric response",
            "source_needed": "explicit connection dependence theorem or component norm",
            "source_anchors": "KRS2111_4_connection",
        }
    ),
    base(
        {
            "delta_id": "DK3009_5_domain_window",
            "component": "K_domain",
            "definition": "domain/window/support/readout selection response",
            "status": "OPEN_RETAINED_RESIDUAL",
            "residual_formula": "epsilon_K_domain_abs from local domain selection variation",
            "source_needed": "domain descent/no-leak theorem or component norm",
            "source_anchors": "KRS2111_5_domain",
        }
    ),
    base(
        {
            "delta_id": "DK3009_6_boundary_corner",
            "component": "K_boundary",
            "definition": "boundary primitive, corner and no-flux response",
            "status": "OPEN_RETAINED_RESIDUAL",
            "residual_formula": "epsilon_K_boundary_abs from integration-by-parts/corner flux",
            "source_needed": "boundary no-flux theorem or edge/corner bound",
            "source_anchors": "KRS2111_6_boundary",
        }
    ),
    base(
        {
            "delta_id": "DK3009_7_projector_commutator",
            "component": "K_proj",
            "definition": "projector/readout commutator response",
            "status": "OPEN_RETAINED_RESIDUAL",
            "residual_formula": "epsilon_K_proj_abs from [P_loc,divergence/readout] leakage",
            "source_needed": "explicit P_loc definition and commutator norm/zero theorem",
            "source_anchors": "KRS2111_7_projector",
        }
    ),
    base(
        {
            "delta_id": "DK3009_8_no_cancellation",
            "component": "Delta_K_abs_envelope",
            "definition": "absolute no-cancellation envelope over DK3009_1..7",
            "status": "NOT_SCOREABLE_COMPONENTS_MISSING",
            "residual_formula": "epsilon_Delta_K_abs <= sum_i abs(epsilon_K_i)",
            "source_needed": "every component theorem-zero or source-backed numeric",
            "source_anchors": "QRES3008_7_total_no_cancellation",
        }
    ),
]


coupling_rows = [
    base(
        {
            "guard_id": "CDG3009_0_q_map",
            "required_clause": "q: Phi_parent -> Q_obs exists before readout and Dq[v_X]=0 for vertical directions.",
            "current_status": "NOT_PARENT_SIGNED",
            "residual_symbol": "epsilon_coupling_q_map_abs",
            "leak_if_missing": "matter/source descent cannot be trusted even if GK sector is action-owned",
            "source_anchors": "PRE2611_0_q_map",
        }
    ),
    base(
        {
            "guard_id": "CDG3009_1_observed_geometry",
            "required_clause": "e_obs and g_obs descend through q(Phi).",
            "current_status": "NOT_PARENT_SIGNED",
            "residual_symbol": "epsilon_coupling_geometry_descent_abs",
            "leak_if_missing": "T^{mu nu} Lie_v g_obs can become a physical local source",
            "source_anchors": "PRE2611_1_observed_geometry",
        }
    ),
    base(
        {
            "guard_id": "CDG3009_2_no_source_prefactor",
            "required_clause": "ordinary matter has no source-only weight, species-relative prefactor, hidden marker or post-readout mask.",
            "current_status": "LIVE_COUNTERMODELS",
            "residual_symbol": "epsilon_source_prefactor_abs",
            "leak_if_missing": "composition/source-normalization residual survives local GR attempt",
            "source_anchors": "SP2612_2_relative_species;SP2612_3_hidden_marker;SP2612_6_readout_worldtube",
        }
    ),
    base(
        {
            "guard_id": "CDG3009_3_no_hidden_frame",
            "required_clause": "no undeclared conformal/disformal matter frame.",
            "current_status": "LIVE_UNLESS_DECLARED_EXTENSION",
            "residual_symbol": "epsilon_hidden_frame_abs",
            "leak_if_missing": "PPN/clock/orbital residuals return through matter frame",
            "source_anchors": "SP2612_4_hidden_frame;CV2660_1_b_dis",
        }
    ),
    base(
        {
            "guard_id": "CDG3009_4_constants_blind",
            "required_clause": "masses, charges, alpha_EM, clocks and material standards are X-blind.",
            "current_status": "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED",
            "residual_symbol": "epsilon_alpha_mass_clock_abs",
            "leak_if_missing": "clock, EM and WEP material channels stay live",
            "source_anchors": "PRE2611_3_constants;SP2612_5_alpha_mass_vertex;CV2660_2_b_alpha;CV2660_3_b_mass",
        }
    ),
    base(
        {
            "guard_id": "CDG3009_5_Hilbert_worldtube",
            "required_clause": "source worldtube and active source are Hilbert/coframe current before readout.",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "residual_symbol": "epsilon_nonHilbert_worldtube_abs",
            "leak_if_missing": "active source can differ from Hamiltonian/metric source",
            "source_anchors": "PRE2611_5_worldtube_support;PRE2611_7_hilbert_source_owner;CV2660_5_q_nonH",
        }
    ),
    base(
        {
            "guard_id": "CDG3009_6_tau_projection_pack",
            "required_clause": "arena projections tau_R10, tau_PPN, tau_clock, tau_WEP and tau_orbital are sourced, not set to one by hand.",
            "current_status": "MISSING_ARENA_PROJECTION_SOURCES",
            "residual_symbol": "epsilon_tau_projection_pack_abs",
            "leak_if_missing": "finite coefficients cannot be scored in local arenas",
            "source_anchors": "CV2660_6_tau_pack",
        }
    ),
    base(
        {
            "guard_id": "CDG3009_7_guard_verdict",
            "required_clause": "all coupling descent guards close in the same parent branch.",
            "current_status": "COUPLING_DESCENT_NOT_CLOSED",
            "residual_symbol": "epsilon_coupling_guard_total_abs",
            "leak_if_missing": "GR/Newton reduction remains nonclaim even if Delta_K is later bounded",
            "source_anchors": "PRE2611_8_verdict;CV2660_7_total_policy",
        }
    ),
]


residual_interface_rows = [
    base(
        {
            "interface_id": "RI3009_0_Delta_K",
            "residual_family": "metric_response_symbol_match",
            "source_ready_row": "epsilon_Delta_K_abs",
            "components": "DK3009_1..DK3009_7",
            "needs_numeric_or_zero": "Gamma density, K_metric components, live K_hat components, parent convention",
            "claim_status": "NONCLAIM_SOURCE_READY",
            "next_use": "feeds q_loc total no-cancellation envelope",
        }
    ),
    base(
        {
            "interface_id": "RI3009_1_Ward_Euler",
            "residual_family": "Euler/source/boundary Ward residual",
            "source_ready_row": "epsilon_GK_Euler_boundary_abs",
            "components": "E_A field residual, boundary/improvement flux, source support",
            "needs_numeric_or_zero": "field list, E_A equations, boundary no-flux theorem or bound",
            "claim_status": "NONCLAIM_SOURCE_READY",
            "next_use": "tests whether q_loc is only Delta_K or has extra source work",
        }
    ),
    base(
        {
            "interface_id": "RI3009_2_coupling",
            "residual_family": "matter/source coupling guard",
            "source_ready_row": "epsilon_coupling_guard_total_abs",
            "components": "CDG3009_0..CDG3009_6",
            "needs_numeric_or_zero": "q-only matter descent theorem or coefficients c_g,b_dis,dalpha,dmass,P_WEP,q_nonH,tau pack",
            "claim_status": "NONCLAIM_SOURCE_READY",
            "next_use": "prevents hidden coupling from masquerading as local GR",
        }
    ),
    base(
        {
            "interface_id": "RI3009_3_total",
            "residual_family": "local q_loc/coupling total",
            "source_ready_row": "epsilon_q_loc_coupling_total_abs",
            "components": "epsilon_Delta_K_abs + epsilon_GK_Euler_boundary_abs + epsilon_coupling_guard_total_abs",
            "needs_numeric_or_zero": "all families theorem-zero or source-backed numeric with no cancellation",
            "claim_status": "NOT_SCOREABLE_COMPONENTS_MISSING",
            "next_use": "3009 handoff to response-operator derivation or bound acquisition",
        }
    ),
]


gate_rows = [
    base({"gate_id": "GATE3009_0_sources", "gate": "all 3009 source anchors exist", "gate_status": "PASS" if all(boolish(row["path_exists"]) and boolish(row["anchors_found"]) for row in source_rows) else "FAIL", "condition_passed": all(boolish(row["path_exists"]) and boolish(row["anchors_found"]) for row in source_rows), "promotion_allowed_now": False, "reason": "sources support a symbol-match audit only"}),
    base({"gate_id": "GATE3009_1_formal_variation", "gate": "formal metric variation exists", "gate_status": "PASS_AS_CONTRACT_ONLY", "condition_passed": True, "promotion_allowed_now": False, "reason": "formal variation is not live symbol match"}),
    base({"gate_id": "GATE3009_2_live_symbol_match", "gate": "live K_hat equals K_metric[Gamma_eff]", "gate_status": "FAIL_CLOSED", "condition_passed": False, "promotion_allowed_now": False, "reason": "Gamma density owner and Khat identity are missing"}),
    base({"gate_id": "GATE3009_3_DeltaK_residual", "gate": "Delta_K obstruction is explicit", "gate_status": "PASS_NONCLAIM", "condition_passed": True, "promotion_allowed_now": False, "reason": "Delta_K rows are source-ready but not scored"}),
    base({"gate_id": "GATE3009_4_coupling_descent", "gate": "q-only matter/source coupling descent closes", "gate_status": "FAIL_CLOSED", "condition_passed": False, "promotion_allowed_now": False, "reason": "source prefactors and hidden frames remain live countermodels"}),
    base({"gate_id": "GATE3009_5_local_claims", "gate": "local GR/Newton/PPN/WEP/R10 claim allowed", "gate_status": "FAIL_CLOSED", "condition_passed": False, "promotion_allowed_now": False, "reason": "symbol match and coupling descent fail current claim"}),
]


decision_rows = [
    base({"decision_id": "DEC3009_0_symbol_match_failed", "decision": "Do not match live K_hat to K_metric yet.", "rationale": "The corpus has formal candidate variations but lacks a component-by-component live Khat certificate.", "next_effect": "carry Delta_K as explicit residual rather than claiming q_loc zero."}),
    base({"decision_id": "DEC3009_1_formal_route_kept", "decision": "Keep the metric-response route as the preferred derivation path.", "rationale": "The Ward identity is the right way to derive local silence if the symbols can be matched later.", "next_effect": "future work should lower one response-operator component or source-bound Delta_K."}),
    base({"decision_id": "DEC3009_2_coupling_guard_failed", "decision": "Do not declare universal matter/source coupling closed.", "rationale": "q-only descent, source-prefactor absence, hidden-frame absence and worldtube ownership are unsigned.", "next_effect": "coupling residual vector remains coequal with q_loc residual."}),
    base({"decision_id": "DEC3009_3_next", "decision": "Move to response-operator component derivation or residual-bound acquisition.", "rationale": "The next productive step is either one real operator row for Gamma/Khat or numeric/source-backed bounds for the explicit residual families.", "next_effect": "3010 should attempt the first response-operator row before defaulting to bound acquisition."}),
]


next_rows = [
    base(
        {
            "next_id": "NEXT3009_0_3010",
            "priority": "selected_primary",
            "target_doc": "3010-Y5-R2FR-first-Gamma-Khat-response-operator-row-or-q_loc-coupling-bound-interface-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_first_Gamma_Khat_response_operator_row_or_q_loc_coupling_bound_interface_under_AX1090_3010.py",
            "mission": "Try to derive one actual response-operator row for Gamma_eff/K_metric/K_hat with units and component ownership; if that fails, convert Delta_K and coupling guard families into local-bound acquisition rows.",
            "success_condition": "one live response component is parent-owned and united, or every failed component is source-ready as nonclaim bound input.",
            "fallback_if_fail": "start numeric/source-backed local residual acquisition for R10, PPN, clocks, WEP, orbital and EM arenas.",
            "guardrails": "no q_loc zero claim from formal theorem alone; no cancellation between unknown residuals; no hidden coupling; no EH-only import; no orbital-GM denominator; no local-GR/Newton/PPN/WEP/R10 claim; no GitHub; no formalization-workbench edits",
        }
    )
]


write_csv(OUTPUTS["sources"], source_rows)
write_csv(OUTPUTS["symbol_match"], symbol_match_rows)
write_csv(OUTPUTS["delta_k"], delta_k_rows)
write_csv(OUTPUTS["coupling"], coupling_rows)
write_csv(OUTPUTS["residual_interface"], residual_interface_rows)
write_csv(OUTPUTS["gates"], gate_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

shutil.copyfile(OUTPUTS["symbol_match"], BRANCH_OUTPUTS["symbol_match_copy"])
shutil.copyfile(OUTPUTS["delta_k"], BRANCH_OUTPUTS["delta_k_copy"])
shutil.copyfile(OUTPUTS["coupling"], BRANCH_OUTPUTS["coupling_copy"])
shutil.copyfile(OUTPUTS["residual_interface"], BRANCH_OUTPUTS["residual_interface_copy"])
shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = []
for copy_id, path in BRANCH_OUTPUTS.items():
    copy_rows = rows(path)
    claim_flags_present = any(
        boolish(row.get("valid_for_claim")) or boolish(row.get("claim_allowed")) or boolish(row.get("score_ready")) or boolish(row.get("valid_prediction_row"))
        for row in copy_rows
    )
    branch_rows.append(base({"copy_id": copy_id, "path": str(path), "path_exists": path.exists(), "row_count": len(copy_rows), "csv_parse_ok": csv_ok(path), "claim_flags_present": claim_flags_present}))
write_csv(OUTPUTS["branches"], branch_rows)

generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv" or not path.exists():
            continue
        for row in rows(path):
            for key in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if boolish(row.get(key)):
                    return False
    return True


validation_rows = [
    base({"validation_id": "VAL3009_00_sources_exist", "passed": all(boolish(row["path_exists"]) for row in source_rows), "detail": "every cited source path exists", "required": True}),
    base({"validation_id": "VAL3009_01_source_anchors", "passed": all(boolish(row["anchors_found"]) for row in source_rows), "detail": "every source contains required anchors", "required": True}),
    base({"validation_id": "VAL3009_02_formal_variation_only_pass", "passed": sum(1 for row in symbol_match_rows if boolish(row["pass_now"])) == 1 and symbol_match_rows[1]["match_id"] == "SYM3009_1_formal_variation", "detail": "only the formal variation step passes; live symbol match remains failed", "required": True}),
    base({"validation_id": "VAL3009_03_DeltaK_explicit", "passed": any(row["delta_id"] == "DK3009_8_no_cancellation" for row in delta_k_rows), "detail": "Delta_K no-cancellation envelope is explicit", "required": True}),
    base({"validation_id": "VAL3009_04_coupling_guard_blocked", "passed": any(row["guard_id"] == "CDG3009_7_guard_verdict" and row["current_status"] == "COUPLING_DESCENT_NOT_CLOSED" for row in coupling_rows), "detail": "coupling descent remains blocked and explicit", "required": True}),
    base({"validation_id": "VAL3009_05_residual_interface_nonclaim", "passed": len(residual_interface_rows) >= 4 and all(not boolish(row["valid_for_claim"]) for row in residual_interface_rows), "detail": "source-ready residual interface remains nonclaim", "required": True}),
    base({"validation_id": "VAL3009_06_local_claims_blocked", "passed": any(row["gate_id"] == "GATE3009_5_local_claims" and not boolish(row["promotion_allowed_now"]) for row in gate_rows), "detail": "no local GR/Newton/PPN/WEP/R10 claim is allowed", "required": True}),
    base({"validation_id": "VAL3009_07_next_target_selected", "passed": next_rows[0]["target_doc"].startswith("3010-Y5-R2FR-first-Gamma-Khat-response-operator-row"), "detail": "3010 selects response-operator row or bound interface", "required": True}),
    base({"validation_id": "VAL3009_08_branch_copies", "passed": all(boolish(row["path_exists"]) and boolish(row["csv_parse_ok"]) and not boolish(row["claim_flags_present"]) for row in branch_rows), "detail": "branch copies exist, parse, and carry no claim flags", "required": True}),
    base({"validation_id": "VAL3009_09_csv_parse", "passed": all(csv_ok(path) for path in list(OUTPUTS.values())[:-1] + list(BRANCH_OUTPUTS.values())), "detail": "all 3009 CSV outputs parse cleanly", "required": True}),
    base({"validation_id": "VAL3009_10_paths_under_post_checkpoint", "passed": all(under(path, ROOT) for path in generated_paths), "detail": "all generated outputs are under post-checkpoint-work", "required": True}),
    base({"validation_id": "VAL3009_11_formalization_untouched", "passed": not any(FORMALIZATION.rglob("*3009*")) if FORMALIZATION.exists() else True, "detail": "no targeted 3009 files exist under formalization-workbench", "required": True}),
    base({"validation_id": "VAL3009_12_no_claim_flags", "passed": no_claim_flags(list(OUTPUTS.values())[:-1] + list(BRANCH_OUTPUTS.values())), "detail": "all generated rows remain valid_for_claim=false and claim_allowed=false", "required": True}),
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(base({"validation_id": "VAL3009_OVERALL", "passed": overall_pass, "detail": "3009 audits real Gamma/Khat symbol match, keeps only formal variation as passing, stages Delta_K/coupling residual interfaces, and blocks local GR/Newton promotion", "required": True}))
write_csv(OUTPUTS["validation"], validation_rows)


doc = f"""# 3009 - Y5/R2FR Gamma-Khat Metric-Response Symbol Match And Coupling Descent Guard Under AX1090

Status: `Y5_R2FR_3009_live_symbol_match_failed_DeltaK_and_coupling_residuals_staged_3010_next`

Generated: `{RUN_UTC}`

## Current Verdict

3009 tries the real match. The result is sharp: the formal metric-response variation exists, but the live MTS symbols do not yet satisfy the identity `K_hat = K_metric[Gamma_eff]`.

The useful equation is now:

`Delta_K^{{mu nu}} := K_hat_live^{{mu nu}} - K_metric^{{mu nu}}[Gamma_eff]`.

So the local residual is not just `q_loc = Ward residual`. Current MTS must carry the extra obstruction:

`q_loc^nu = P_loc(nabla_mu T_GK^{{mu nu}}) - P_loc(nabla_mu Delta_K^{{mu nu}}) + projector/boundary convention terms`.

That is progress because the failure is no longer foggy. It is `Delta_K`, plus the coupling guard. The coupling guard also fails current promotion: q-only matter descent, hidden source-prefactor absence, hidden frame absence, constant-sector blindness, Hilbert/worldtube source ownership and arena projection packs are not all parent-signed.

Therefore 3009 refuses `q_loc -> 0`, refuses local GR/Newton, and stages source-ready residual interfaces for `Delta_K` and hidden coupling.

## Source Register

{md_table(source_rows, ["source_id", "path_exists", "anchors_found", "missing_anchors", "role"])}

## Real Symbol Match Audit

{md_table(symbol_match_rows, ["match_id", "required_identity", "current_evidence", "pass_now", "defect_symbol", "effect"])}

## Delta_K Obstruction Decomposition

{md_table(delta_k_rows, ["delta_id", "component", "definition", "status", "residual_formula", "source_needed"])}

## Coupling Descent Guard Audit

{md_table(coupling_rows, ["guard_id", "required_clause", "current_status", "residual_symbol", "leak_if_missing"])}

## Source-Ready Residual Interface

{md_table(residual_interface_rows, ["interface_id", "residual_family", "source_ready_row", "components", "needs_numeric_or_zero", "claim_status"])}

## Promotion Gates

{md_table(gate_rows, ["gate_id", "gate", "gate_status", "condition_passed", "promotion_allowed_now", "reason"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "rationale", "next_effect"])}

## Next Target

{md_table(next_rows, ["next_id", "target_doc", "mission", "success_condition", "guardrails"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "path", "path_exists", "row_count", "csv_parse_ok", "claim_flags_present"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "detail", "required"])}

## Plain-English Takeaway

This is a clean failure, which is actually valuable. The live theory cannot yet say `K_hat` is the metric response of `Gamma_eff`, but we now know exactly what the mismatch is called and how it enters the local force residual. The road to derived GR is now: either derive one live response-operator row, or bound the `Delta_K` and coupling residual families honestly.

This keeps us out of the trap where we accidentally import GR through EH or hide a fifth-force in the coupling. It is not the win yet, but it is the right kind of battlefield map.

## Forbidden Claims From 3009

- Live `K_hat` equals `K_metric[Gamma_eff]`.
- `Delta_K=0`.
- `q_loc^nu=0`.
- Hidden matter/source couplings are excluded.
- Coupling residual vector is score-ready.
- Local GR/Newton/PPN/WEP/R10 pass.
"""

DOC.write_text(doc, encoding="utf-8")

if not overall_pass:
    failed = [row["validation_id"] for row in validation_rows if not boolish(row["passed"])]
    raise SystemExit(f"3009 validation failed: {failed}")

print(f"wrote {DOC}")
for key, path in OUTPUTS.items():
    print(f"{key}: {path}")
for key, path in BRANCH_OUTPUTS.items():
    print(f"{key}: {path}")
