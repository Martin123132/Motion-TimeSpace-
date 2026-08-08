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

CHECKPOINT = "3007"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3007-Y5-R2FR-minimal-parent-action-sector-grammar-or-sector-variation-ledger-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3007_SOURCE_REGISTER.csv",
    "grammar": RESIDUALS / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv",
    "fields": RESIDUALS / "P8_Y5_R2FR_3007_RETAINED_FIELD_LIST.csv",
    "variation": RESIDUALS / "P8_Y5_R2FR_3007_SECTOR_VARIATION_LEDGER.csv",
    "omissions": RESIDUALS / "P8_Y5_R2FR_3007_OMITTED_SECTOR_DEMOTION_LEDGER.csv",
    "feed": RESIDUALS / "P8_Y5_R2FR_3007_THETA_QTAU_FEED_ROWS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3007_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3007_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3007_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3007_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3007_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "grammar_copy": PARENT_ACTION / "minimal_parent_action_sector_grammar_3007_NOT_SIGNED.csv",
    "variation_copy": PARENT_ACTION / "sector_variation_ledger_3007_NOT_SIGNED.csv",
    "theta_qtau_feed_copy": LOCAL_BOUNDS / "theta_Qtau_feed_rows_3007_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3007_HARD_SECTOR_ACTION_EXISTENCE_NEXT_NONCLAIM.csv",
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
    (
        "SRC3007_00_3006_next",
        RESIDUALS / "P8_Y5_R2FR_3006_NEXT_TARGET.csv",
        ["NEXT3006_0_3007", "minimal parent action sector grammar"],
        "3006 selects minimal parent action sector grammar as the next upstream target.",
    ),
    (
        "SRC3007_01_3006_doc",
        ROOT / "3006-Y5-R2FR-parent-theta-Qtau-Htau-extraction-or-Hamiltonian-current-owner-under-AX1090.md",
        ["parent action -> symplectic potential -> Noether charge", "minimal parent action sector grammar"],
        "3006 says the GR-like route is correct but the parent action remains distributed across contracts.",
    ),
    (
        "SRC3007_02_3006_current_chain",
        RESIDUALS / "P8_Y5_R2FR_3006_PARENT_CURRENT_CHAIN_AUDIT.csv",
        ["CCA3006_0_single_action", "CCA3006_9_verdict"],
        "3006 current-chain audit identifies missing single action, field list, variations and constraints.",
    ),
    (
        "SRC3007_03_3006_sectors",
        RESIDUALS / "P8_Y5_R2FR_3006_SECTOR_CHARGE_OWNER_ROWS.csv",
        ["SEC3006_0_EH_core", "SEC3006_9_total"],
        "3006 sector charge-owner rows give the sector inventory to grammarize.",
    ),
    (
        "SRC3007_04_3006_htau",
        RESIDUALS / "P8_Y5_R2FR_3006_HTAU_EXTRACTION_ROWS.csv",
        ["HTE3006_0_theta", "HTE3006_8_verdict"],
        "3006 H_tau extraction rows define what the sector grammar must feed.",
    ),
    (
        "SRC3007_05_1009_parent_sector",
        RESIDUALS / "P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv",
        ["PCS1009_0_EH_core", "PCS1009_9_total_parent_contract"],
        "1009 parent sector contract names action blocks and required first-variation targets.",
    ),
    (
        "SRC3007_06_1009_variation_candidates",
        RESIDUALS / "P8_Y5_R10_1009_SECTOR_VARIATION_CANDIDATES.csv",
        ["SVC1009_0_EH_anchor_only", "SVC1009_6_total_parent_switch_unsigned"],
        "1009 variation candidates show why current sector variations are not enough for a claim.",
    ),
    (
        "SRC3007_07_2939_sector_certificate",
        RESIDUALS / "P8_Y5_R2FR_2939_THETA_QTAU_SECTOR_CERTIFICATE_LEDGER.csv",
        ["SEC2939_0_EH_core", "SEC2939_10_total"],
        "2939 theta/Q_tau sector certificate ledger keeps every sector unsigned.",
    ),
    (
        "SRC3007_08_2989_theta_sector",
        RESIDUALS / "P8_Y5_R2FR_2989_PARENT_LAGRANGIAN_THETA_SECTOR_AUDIT.csv",
        ["TLS2989_0_master_identity", "TLS2989_8_total"],
        "2989 parent Lagrangian theta-sector audit gives the sector-complete identity shape.",
    ),
    (
        "SRC3007_09_2990_normal_form",
        RESIDUALS / "P8_Y5_R2FR_2990_SELECTED_PARENT_NORMAL_FORM_CONTRACT.csv",
        ["NF2990_0_formula", "NF2990_8_verdict"],
        "2990 selected working normal form is the best nonclaim scaffold for 3007.",
    ),
    (
        "SRC3007_10_2990_sector_normal",
        RESIDUALS / "P8_Y5_R2FR_2990_SECTOR_BY_SECTOR_THETA_NORMAL_FORM_CONTRACT.csv",
        ["SNF2990_0_EH", "SNF2990_7_total"],
        "2990 sector-by-sector theta normal form supplies fallback residual symbols.",
    ),
    (
        "SRC3007_11_2552_current_chain",
        RESIDUALS / "P8_Y5_NO_SHADOW_2552_CURRENT_CHAIN_PROMOTION_CONTRACT.csv",
        ["PCC2552_0_single_action_source", "PCC2552_7_source_bridge"],
        "2552 promotion contract defines what is needed to reopen theta/Q_tau/H_tau.",
    ),
    (
        "SRC3007_12_2552_material",
        RESIDUALS / "P8_Y5_NO_SHADOW_2552_REOPEN_MATERIAL_SPEC.csv",
        ["MAT2552_0_action_source", "MAT2552_5_reference_pack"],
        "2552 material spec supplies reopening requirements for action, fields, theta, Q_tau and reference.",
    ),
    (
        "SRC3007_13_2551_requirements",
        RESIDUALS / "P8_Y5_NO_SHADOW_2551_CHARGE_POSITIVITY_PACK_REQUIREMENTS.csv",
        ["REQ2551_0_parent_action", "REQ2551_6_no_shortcuts"],
        "2551 charge positivity pack forbids shortcut denominators and EH-only imports.",
    ),
    (
        "SRC3007_14_2504_noether",
        RESIDUALS / "P8_Y5_NO_SHADOW_2504_NOETHER_HAMILTONIAN_CHARGE_CHAIN.csv",
        ["NHC2504_0_variation", "NHC2504_4_PiM_identification"],
        "2504 Noether/Hamiltonian chain is the exact target the grammar must support.",
    ),
    (
        "SRC3007_15_BZTC552",
        RESIDUALS / "P8_Y5_BRR545_PARENT_ACTION_ZERO_THEOREM_CONTRACT.csv",
        ["BZTC552_0_covariant_phase_space_parent", "BZTC552_7_no_cancellation_envelope_identity"],
        "552 parent-action zero theorem contract defines no-cancellation and current-chain requirements.",
    ),
    (
        "SRC3007_16_symbol_map",
        RESIDUALS / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        ["Gamma_eff", "memory / B_mem / U_mem / I_M"],
        "Symbol-to-action map places local GR variables in candidate parent sectors.",
    ),
    (
        "SRC3007_17_first_variation_gates",
        RESIDUALS / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
        ["FV512_0_metric", "FV512_6_transition_scale"],
        "First-variation gates define the variables that still block local GR/Newton.",
    ),
    (
        "SRC3007_18_1841_variation",
        RESIDUALS / "P8_Y5_PARENT_QLOC_1841_SECTOR_ACTION_VARIATION_LEDGER.csv",
        ["SAV1841_0_higher_derivative", "SAV1841_6_verdict"],
        "1841 variation ledger identifies retained local residual/bound-input sectors.",
    ),
    (
        "SRC3007_19_2464_fields",
        RESIDUALS / "P8_Y5_PARENT_ACTION_2464_FIELD_INVENTORY.csv",
        ["FLD2464_0_metric", "FLD2464_7_reference"],
        "2464 field inventory supplies an earlier skeleton for q_loc/source bridge fields.",
    ),
]

source_rows = []
for source_id, path, required, role in SOURCE_SPECS:
    source_rows.append(
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
    )


grammar_rows = [
    base(
        {
            "grammar_id": "G3007_0_total_normal_form",
            "sector": "local parent action total",
            "retention_class": "WORKING_CONTRACT_NONCLAIM",
            "action_block": "S_parent^loc = S_EH + S_matter[q^*e_obs,psi] + S_boundary_fixed + S_extra[Z] + S_selector/PiM + S_worldtube + S_constraint + S_residual_explicit",
            "fields": "g_obs,e_obs,tau,psi,q/Phi,Z,Gamma_eff,K_hat,P_loc,Pi_M,Q_M,B_ref,H_ref,W",
            "coupling_rule": "all readout/source/matter couplings must descend from one parent action before any Newton/GR claim",
            "local_limit_rule": "local branch reduces to EH plus universal matter only after every non-EH sector is silent, exact, topological, bounded, or explicitly demoted",
            "variation_contract": "delta S_parent = sum_s(E_s delta Phi_s + d theta_s)",
            "theta_Qtau_contract": "theta_MTS=sum_s theta_s and Q_tau^MTS=sum_s Q_tau^s, with C_tau_total accounted",
            "current_status": "SELECTED_GRAMMAR_NOT_PARENT_SIGNED",
            "residual_symbol": "epsilon_theta_piece_total_abs",
            "promotion_blocker": "single varied parent action and sector first-variation certificates are missing",
            "source_anchors": "NF2990_0_formula;TLS2989_0_master_identity;CCA3006_9_verdict",
        }
    ),
    base(
        {
            "grammar_id": "G3007_1_EH_metric",
            "sector": "EH/local metric comparator",
            "retention_class": "RETAIN_BASELINE_REFERENCE_NOT_TOTAL",
            "action_block": "S_EH[g_obs;kappa0,Lambda0] plus fixed local subtraction convention",
            "fields": "g_obs,e_obs,tau",
            "coupling_rule": "same observed metric/coframe must couple to matter, clocks and readout",
            "local_limit_rule": "Theta_EH/Q_tau^EH may seed the GR comparator but cannot absorb MTS extra sectors",
            "variation_contract": "delta S_EH = E_g delta g + d theta_EH",
            "theta_Qtau_contract": "theta_EH and Q_tau^EH only",
            "current_status": "REFERENCE_TEMPLATE_ONLY",
            "residual_symbol": "epsilon_EH_reference_guard",
            "promotion_blocker": "non-EH sectors and source bridge are unsigned",
            "source_anchors": "PCS1009_0_EH_core;SNF2990_0_EH;FV512_0_metric",
        }
    ),
    base(
        {
            "grammar_id": "G3007_2_universal_matter_worldtube",
            "sector": "universal matter/source/worldtube",
            "retention_class": "RETAIN_REQUIRED_CORE_UNSIGNED",
            "action_block": "S_matter[psi,e_obs(q(Phi))] + S_worldtube[W,Q_M,tau] if source support is parent-owned",
            "fields": "psi,e_obs,q/Phi,W,J_H,Q_M,M_source",
            "coupling_rule": "matter sees q-only observed data; no source-only prefactor or species/domain label",
            "local_limit_rule": "Hilbert current and Hamiltonian/worldtube source charge must be the same object before orbital fitting",
            "variation_contract": "delta S_matter = E_psi delta psi + 1/2 T_m^{mu nu} delta g_mu_nu + d theta_matter plus source-support variation",
            "theta_Qtau_contract": "theta_matter, Q_tau^matter/source or proof of no separate matter surface charge",
            "current_status": "CONDITIONAL_MATTER_DESCENT_NOT_PARENT_SIGNED",
            "residual_symbol": "epsilon_Qv_matter_source_piece",
            "promotion_blocker": "hidden source prefactors/support/worldtube slots remain legal",
            "source_anchors": "PCS1009_2_universal_matter;PCS1009_8_worldtube_source_glue;NF2990_5_matter_qpullback",
        }
    ),
    base(
        {
            "grammar_id": "G3007_3_boundary_reference",
            "sector": "boundary/reference/improvement",
            "retention_class": "RETAIN_FIXED_EXACT_OR_TOPOLOGICAL_UNSIGNED",
            "action_block": "S_GHY + B_ref + exact/topological/corner convention fixed before readout",
            "fields": "boundary metric,normal,B_ref,H_ref,counterterm class,corner class",
            "coupling_rule": "reference data are selected before source/readout fitting and cannot set the denominator",
            "local_limit_rule": "delta B_ref is zero/exact/topological on linked local surfaces or carried as explicit residual",
            "variation_contract": "delta S_boundary = E_boundary delta beta + d theta_boundary + delta B_ref",
            "theta_Qtau_contract": "Q_tau^boundary and reference shift H_ref with fixed-before-readout certificate",
            "current_status": "FIXED_REFERENCE_MISSING",
            "residual_symbol": "epsilon_Bv_ambiguity",
            "promotion_blocker": "fixed-reference/no-flux convention is not parent-signed",
            "source_anchors": "PCS1009_3_boundary_reference;SNF2990_1_boundary;NF2990_2_boundary",
        }
    ),
    base(
        {
            "grammar_id": "G3007_4_Gamma_Khat_q_loc",
            "sector": "Gamma/Khat/q_loc extra local sector",
            "retention_class": "DEMOTE_TO_EXPLICIT_RESIDUAL_UNLESS_ACTION_EXISTS",
            "action_block": "S_GK[g,Phi,Z] with Gamma_eff(Phi,g) and K_hat^{mu nu}=partial L_GK/partial(nabla_mu A_nu), or no-action residual",
            "fields": "Phi,Z,A_nu,Gamma_eff,K_hat,q_loc,P_loc",
            "coupling_rule": "q_loc is a Ward/Euler residual, not a fitted force field",
            "local_limit_rule": "P_loc(nabla Gamma_eff - div K_hat) vanishes only if Helmholtz action, Euler closure and double-zero hold",
            "variation_contract": "delta S_GK = E_Z delta Z + E_A delta A + d theta_GK",
            "theta_Qtau_contract": "theta_GK, Q_tau^GK and C_tau^GK, or an explicit epsilon_q_loc residual row",
            "current_status": "MISSING_ACTION_EXISTENCE_AND_DOUBLE_ZERO",
            "residual_symbol": "epsilon_q_loc_action_owner_abs",
            "promotion_blocker": "FV512_2 fails for current claim",
            "source_anchors": "PCS1009_4_Gamma_Khat_extra;FV512_2_Gamma_Khat_q;GK513_3_double_zero",
        }
    ),
    base(
        {
            "grammar_id": "G3007_5_memory_response",
            "sector": "memory/response doublet",
            "retention_class": "AUXILIARY_DOUBLE_ZERO_CANDIDATE_UNSIGNED",
            "action_block": "S_response[R_+^A,R_-^A,memory] or quadratic silent sector L_silent[Z]",
            "fields": "R_+^A,R_-^A,B_mem,U_mem,I_M,Z",
            "coupling_rule": "cosmological activation allowed only if local odd/source vertex is zero",
            "local_limit_rule": "Z=0, dL_silent|0=0, Hessian positive, no linear stress/readout/source vertex",
            "variation_contract": "delta S_response = E_+ delta R_+ + E_- delta R_- + d theta_memory",
            "theta_Qtau_contract": "theta_memory/Q_tau^memory zero, double-zero, or residualized",
            "current_status": "ZERO_ODD_SOURCE_NOT_PARENT_DERIVED",
            "residual_symbol": "epsilon_Qv_extra_piece",
            "promotion_blocker": "positive operator and no odd source are conditional only",
            "source_anchors": "PCS1009_7_memory_response_doublet;NF2990_3_extra_double_zero;FV512_4_memory",
        }
    ),
    base(
        {
            "grammar_id": "G3007_6_domain_selector_projector",
            "sector": "domain/local selector and projector",
            "retention_class": "AUXILIARY_CONSTRAINT_OR_RESIDUAL",
            "action_block": "S_selector[u,h,X,Qcoh,chi_D,lambda_D] + parent-owned P_loc/Pi_M algebra",
            "fields": "u,h,X,Qcoh,chi_D,lambda_D,P_loc",
            "coupling_rule": "selectors must be parent-given, not data-chosen after readout",
            "local_limit_rule": "auxiliary variations force local zero without kinetic/vector/domain-wall stress",
            "variation_contract": "delta S_selector gives selector constraints plus possible metric/projector stress",
            "theta_Qtau_contract": "theta_selector and Q_tau^selector vanish/topological, or retained as epsilon_Qv_projector_piece",
            "current_status": "PARTIAL_CLAUSE_NOT_PARENT_CLOSED",
            "residual_symbol": "epsilon_Qv_projector_piece",
            "promotion_blocker": "metric-stress, tau action and local/FLRW branch rule are unsigned",
            "source_anchors": "PCS1009_5_domain_projector_selector;FV512_3_domain_selector;SNF2990_3_projector",
        }
    ),
    base(
        {
            "grammar_id": "G3007_7_PiM_mass_projector",
            "sector": "Pi_M/source-measure Hamiltonian bridge",
            "retention_class": "RETAIN_REQUIRED_BRIDGE_UNSIGNED",
            "action_block": "Pi_M J_H, Q_M[tau], Hamiltonian/worldtube source charge and exterior homology",
            "fields": "Pi_M,J_H,Q_M,H_tau,M_H_ref,worldtube W,exterior annulus A",
            "coupling_rule": "same charge must feed Hilbert current, Hamiltonian surface charge and metric 1/r readout",
            "local_limit_rule": "Pi_M equals the EH/Hamiltonian mass projector at the fixed point and first variation vanishes",
            "variation_contract": "delta(Pi_M J_H)=Pi_M delta J_H+(delta Pi_M)J_H with Ward/Euler flux closure",
            "theta_Qtau_contract": "Q_M[tau] and H_tau source bridge before measured-GM/orbital readout",
            "current_status": "NOT_PARENT_DERIVED",
            "residual_symbol": "epsilon_Mref_normalization",
            "promotion_blocker": "source charge calibration and delta Pi_M stress remain open",
            "source_anchors": "PCS1009_6_mass_projector_PiM;FV512_5_mass_projector;NHC2504_4_PiM_identification",
        }
    ),
    base(
        {
            "grammar_id": "G3007_8_kappa_topological",
            "sector": "kappa/G topological coupling",
            "retention_class": "OPTIONAL_TOPOLOGICAL_CANDIDATE_UNSIGNED",
            "action_block": "S_kappa_top[kappa_eff,A_3]",
            "fields": "kappa_eff,G_eff,A_3",
            "coupling_rule": "coupling is universal, constant on local branch and has no matter/species/domain labels",
            "local_limit_rule": "d kappa_eff=0 by topological variation or G_eff drift stays explicit",
            "variation_contract": "delta_{A_3} S -> d kappa_eff=0; delta_kappa gives companion constraint",
            "theta_Qtau_contract": "topological sector contributes no local charge except fixed constant-superselection term",
            "current_status": "CANDIDATE_NOT_ADOPTED",
            "residual_symbol": "epsilon_Geff_drift",
            "promotion_blocker": "A_3/kappa parent adoption is not signed",
            "source_anchors": "PCS1009_1_kappa_topological;FV512_1_kappa",
        }
    ),
    base(
        {
            "grammar_id": "G3007_9_tau_surface_lock",
            "sector": "tau/surface/readout lock",
            "retention_class": "READOUT_LOCK_REQUIRED_NOT_ACTION_SUBSTITUTE",
            "action_block": "choice of tau, linked surfaces and local frame as parent-owned structure/gauge data",
            "fields": "tau_source,tau_charge,tau_clock,tau_readout,S_inner,S_outer,frame",
            "coupling_rule": "the same observed time generator must act on every retained sector",
            "local_limit_rule": "tau/source/surface mismatch is residualized, not ignored",
            "variation_contract": "L_tau acts on metric, matter, representative, boundary and source fields consistently",
            "theta_Qtau_contract": "J_tau and H_tau use this single tau/surface class",
            "current_status": "MISSING_TAU_SURFACE_LOCK",
            "residual_symbol": "epsilon_tau_surface_mismatch",
            "promotion_blocker": "tau/source/clock/readout equality remains unsigned",
            "source_anchors": "SEC2939_8_tau_surface;CCA3006_4_Noether_current",
        }
    ),
    base(
        {
            "grammar_id": "G3007_10_verdict",
            "sector": "sector grammar verdict",
            "retention_class": "GRAMMAR_READY_CURRENT_CLAIM_BLOCKED",
            "action_block": "use rows G3007_1..9 as the minimal parent-action grammar and keep residual channels explicit",
            "fields": "all rows above",
            "coupling_rule": "no sector can be silently imported from EH or removed after seeing data",
            "local_limit_rule": "local GR/Newton opens only after retained sector variations are signed or residuals are bounded",
            "variation_contract": "all sector rows must supply E_i, theta_i, Q_tau^i, C_tau^i/stress, boundary and source terms",
            "theta_Qtau_contract": "theta_MTS/Q_tau/H_tau remain feed-ready but unpromoted",
            "current_status": "PARENT_ACTION_GRAMMAR_STAGED_NOT_SIGNED",
            "residual_symbol": "epsilon_parent_action_grammar_unsigned",
            "promotion_blocker": "hard sectors still require action existence, descent and source bridge proofs",
            "source_anchors": "CCA3006_9_verdict;TQV2552_1_current_promotion;REQ2551_6_no_shortcuts",
        }
    ),
]


field_rows = [
    base(
        {
            "field_id": "FLD3007_0_metric",
            "symbol": "g_obs / g_readout",
            "sector_owner": "G3007_1_EH_metric",
            "status": "reference metric anchor, not total MTS proof",
            "variation_role": "delta_g S_EH plus all sector stress/source variations",
            "can_be_fundamental_now": True,
            "must_be_derived_or_locked_by": "same observed coframe/source/readout theorem",
            "missing_certificate": "same metric/coframe couples to matter, clocks, source and readout",
            "source_anchors": "FLD2464_0_metric;FV512_0_metric",
        }
    ),
    base(
        {
            "field_id": "FLD3007_1_tau_coframe",
            "symbol": "tau_mu / e_obs / coframe",
            "sector_owner": "G3007_9_tau_surface_lock",
            "status": "candidate parent/gauge structure",
            "variation_role": "defines L_tau, local frame, clock and surface charge generator",
            "can_be_fundamental_now": False,
            "must_be_derived_or_locked_by": "tau_source=tau_charge=tau_clock=tau_readout",
            "missing_certificate": "tau/surface lock",
            "source_anchors": "FLD2464_1_clock;SEC2939_8_tau_surface",
        }
    ),
    base(
        {
            "field_id": "FLD3007_2_matter",
            "symbol": "psi / J_H",
            "sector_owner": "G3007_2_universal_matter_worldtube",
            "status": "required physical sector",
            "variation_role": "Hilbert stress/current and matter equations",
            "can_be_fundamental_now": True,
            "must_be_derived_or_locked_by": "q-only matter descent and source Ward identity",
            "missing_certificate": "no hidden species/source/domain coupling",
            "source_anchors": "PCS1009_2_universal_matter;NF2990_5_matter_qpullback",
        }
    ),
    base(
        {
            "field_id": "FLD3007_3_parent_quotient",
            "symbol": "Phi / q(Phi)",
            "sector_owner": "G3007_2_universal_matter_worldtube",
            "status": "parent quotient variable remains conditional",
            "variation_role": "chain rule must route matter/source dependence through q only",
            "can_be_fundamental_now": False,
            "must_be_derived_or_locked_by": "parent quotient map and matter descent proof",
            "missing_certificate": "direct source/support slots excluded",
            "source_anchors": "NF2990_5_matter_qpullback;TLS2989_5_matter_source",
        }
    ),
    base(
        {
            "field_id": "FLD3007_4_Gamma_eff",
            "symbol": "Gamma_eff",
            "sector_owner": "G3007_4_Gamma_Khat_q_loc",
            "status": "dangerous residual/action-owner target",
            "variation_role": "must be action-owned or a derived coupling/readout scalar",
            "can_be_fundamental_now": False,
            "must_be_derived_or_locked_by": "Helmholtz-compatible S_GK or explicit residual bound",
            "missing_certificate": "partial_A Gamma_eff(Phi0)=0 or finite local bound",
            "source_anchors": "FLD2464_3_connection_scalar;FV512_2_Gamma_Khat_q",
        }
    ),
    base(
        {
            "field_id": "FLD3007_5_Khat",
            "symbol": "K_hat^{mu nu}",
            "sector_owner": "G3007_4_Gamma_Khat_q_loc",
            "status": "derived/boundary/auxiliary candidate",
            "variation_role": "must arise from theta/Q/boundary or momentum derivative of S_GK",
            "can_be_fundamental_now": False,
            "must_be_derived_or_locked_by": "K_hat definition from parent action",
            "missing_certificate": "div K_hat exact/silent or bounded",
            "source_anchors": "FLD2464_4_displacement_tensor;FV512_2_Gamma_Khat_q",
        }
    ),
    base(
        {
            "field_id": "FLD3007_6_q_loc",
            "symbol": "q_loc^nu",
            "sector_owner": "G3007_4_Gamma_Khat_q_loc",
            "status": "derived residual only, not fundamental",
            "variation_role": "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}) as Ward/Euler residual",
            "can_be_fundamental_now": False,
            "must_be_derived_or_locked_by": "Euler closure/double-zero proof",
            "missing_certificate": "local q_loc -> 0 theorem or sourced residual bound",
            "source_anchors": "FV512_2_Gamma_Khat_q;Gamma_eff",
        }
    ),
    base(
        {
            "field_id": "FLD3007_7_selector",
            "symbol": "P_loc / chi_D / Qcoh / u / h / X",
            "sector_owner": "G3007_6_domain_selector_projector",
            "status": "auxiliary selector candidate",
            "variation_role": "selector constraints and possible preferred-frame/projector stress",
            "can_be_fundamental_now": False,
            "must_be_derived_or_locked_by": "parent-owned selector algebra and metric-stress zero",
            "missing_certificate": "no vector/domain-wall/preferred-frame stress",
            "source_anchors": "FV512_3_domain_selector;PCS1009_5_domain_projector_selector",
        }
    ),
    base(
        {
            "field_id": "FLD3007_8_PiM_QM",
            "symbol": "Pi_M / Q_M / M_source",
            "sector_owner": "G3007_7_PiM_mass_projector",
            "status": "required source-charge bridge",
            "variation_role": "mass-projector variation and Hamiltonian/worldtube source equality",
            "can_be_fundamental_now": False,
            "must_be_derived_or_locked_by": "Pi_M chain map and worldtube source charge theorem",
            "missing_certificate": "delta Pi_M stress and measured-GM calibration",
            "source_anchors": "FV512_5_mass_projector;NHC2504_4_PiM_identification",
        }
    ),
    base(
        {
            "field_id": "FLD3007_9_reference",
            "symbol": "B_ref / H_ref",
            "sector_owner": "G3007_3_boundary_reference",
            "status": "late boundary/reference data only",
            "variation_role": "fixed improvement/reference term; must not tune source mass",
            "can_be_fundamental_now": False,
            "must_be_derived_or_locked_by": "fixed-before-readout reference theorem",
            "missing_certificate": "reference lock and no fitted subtraction",
            "source_anchors": "FLD2464_7_reference;MAT2552_5_reference_pack",
        }
    ),
    base(
        {
            "field_id": "FLD3007_10_memory",
            "symbol": "Z / memory / B_mem / U_mem / I_M",
            "sector_owner": "G3007_5_memory_response",
            "status": "empirical/EFT candidate until parent-signed",
            "variation_role": "double-zero auxiliary stress/current sector",
            "can_be_fundamental_now": False,
            "must_be_derived_or_locked_by": "positive operator and zero odd source",
            "missing_certificate": "local silence with cosmological activation",
            "source_anchors": "FV512_4_memory;NF2990_3_extra_double_zero",
        }
    ),
    base(
        {
            "field_id": "FLD3007_11_kappa",
            "symbol": "kappa_eff / G_eff / A_3",
            "sector_owner": "G3007_8_kappa_topological",
            "status": "optional topological candidate",
            "variation_role": "constant universal coupling superselection",
            "can_be_fundamental_now": False,
            "must_be_derived_or_locked_by": "topological A_3/kappa adoption",
            "missing_certificate": "no source/species/domain dependence",
            "source_anchors": "FV512_1_kappa;PCS1009_1_kappa_topological",
        }
    ),
    base(
        {
            "field_id": "FLD3007_12_transition_scale",
            "symbol": "L_cg / ell_tr",
            "sector_owner": "not an independent action sector",
            "status": "derived scale or residual only",
            "variation_role": "must follow from spectrum/mass gap/topology/source compactness",
            "can_be_fundamental_now": False,
            "must_be_derived_or_locked_by": "operator spectrum or explicit residual-bound branch",
            "missing_certificate": "no arena switch by hand",
            "source_anchors": "FV512_6_transition_scale;L_cg / ell_tr",
        }
    ),
]


variation_rows = [
    base(
        {
            "variation_id": "VAR3007_0_master",
            "sector": "total parent action",
            "delta_action_contract": "delta S_parent = sum_i delta S_i",
            "eom_piece": "E_total = sum_i E_i",
            "theta_piece": "theta_MTS = sum_i theta_i",
            "qtau_piece": "Q_tau^MTS = sum_i Q_tau^i",
            "constraint_piece": "C_tau_total = sum_i C_tau^i",
            "stress_source_piece": "T_total and J_source from same varied action",
            "local_silence_condition": "every non-EH sector zero/exact/topological/bounded/demoted before GR limit",
            "status": "CONDITIONAL_IDENTITY_NOT_CURRENT_PROOF",
            "effect_on_3006": "feeds HTE3006 only as schema, not promotion",
        }
    ),
    base(
        {
            "variation_id": "VAR3007_1_EH",
            "sector": "EH/local metric",
            "delta_action_contract": "delta S_EH = E_EH^{mu nu} delta g_mu nu + d theta_EH",
            "eom_piece": "Einstein operator plus Lambda/reference convention",
            "theta_piece": "theta_EH",
            "qtau_piece": "Q_tau^EH",
            "constraint_piece": "C_tau^EH",
            "stress_source_piece": "couples to T_matter only after same metric/source lock",
            "local_silence_condition": "non-EH sectors silent or residualized",
            "status": "BASELINE_ONLY",
            "effect_on_3006": "cannot replace theta_MTS/Q_tau^MTS",
        }
    ),
    base(
        {
            "variation_id": "VAR3007_2_matter",
            "sector": "matter/source/worldtube",
            "delta_action_contract": "delta S_m = E_psi delta psi + 1/2 T^{mu nu} delta g_mu nu + d theta_m plus support terms",
            "eom_piece": "matter EOM and source Ward identity",
            "theta_piece": "theta_matter/source or proof none contributes on local surface",
            "qtau_piece": "Q_tau^matter/source or explicit zero theorem",
            "constraint_piece": "source exchange terms",
            "stress_source_piece": "J_H, T_matter, worldtube charge Q_M",
            "local_silence_condition": "q-only descent and compact support before readout",
            "status": "MISSING_MATTER_DESCENT_AND_SOURCE_WARD",
            "effect_on_3006": "keeps source bridge blocked",
        }
    ),
    base(
        {
            "variation_id": "VAR3007_3_boundary",
            "sector": "boundary/reference",
            "delta_action_contract": "delta S_boundary = E_boundary delta beta + d theta_boundary + delta B_ref",
            "eom_piece": "boundary stationarity/reference condition",
            "theta_piece": "theta_boundary + delta B_ref",
            "qtau_piece": "Q_tau^boundary + H_ref shift",
            "constraint_piece": "corner/exact/topological flux terms",
            "stress_source_piece": "reference can shift mass normalization unless fixed",
            "local_silence_condition": "fixed before readout and exact/topological on linked surfaces",
            "status": "MISSING_FIXED_REFERENCE_BEFORE_READOUT",
            "effect_on_3006": "keeps H_ref/M_H_ref blocked",
        }
    ),
    base(
        {
            "variation_id": "VAR3007_4_GK",
            "sector": "Gamma/Khat/q_loc",
            "delta_action_contract": "delta S_GK = E_Z delta Z + E_A delta A + d theta_GK",
            "eom_piece": "E_A should own P_loc(nabla Gamma_eff - div K_hat)",
            "theta_piece": "theta_GK or explicit epsilon_q_loc row",
            "qtau_piece": "Q_tau^GK or zero/bound theorem",
            "constraint_piece": "C_tau^GK local residual",
            "stress_source_piece": "T_GK and any source vertex",
            "local_silence_condition": "Helmholtz-compatible action, Euler closure, double-zero, boundary no-flux",
            "status": "MISSING_ACTION_EXISTENCE",
            "effect_on_3006": "hard local-GR blocker remains explicit",
        }
    ),
    base(
        {
            "variation_id": "VAR3007_5_memory",
            "sector": "memory/response",
            "delta_action_contract": "delta S_response = E_+ delta R_+ + E_- delta R_- + d theta_memory",
            "eom_piece": "positive/even response operator",
            "theta_piece": "theta_memory",
            "qtau_piece": "Q_tau^memory",
            "constraint_piece": "odd/even exchange residual",
            "stress_source_piece": "memory stress and source-normalization leakage",
            "local_silence_condition": "zero odd source and quadratic activation on local branch",
            "status": "PARTIAL_CANDIDATE_NOT_MATCHED",
            "effect_on_3006": "cannot be silently cancelled against GK/projector rows",
        }
    ),
    base(
        {
            "variation_id": "VAR3007_6_selector",
            "sector": "domain/projector selector",
            "delta_action_contract": "delta S_selector = constraints + metric/projector stress + d theta_selector",
            "eom_piece": "selector/local-zero constraints",
            "theta_piece": "theta_selector",
            "qtau_piece": "Q_tau^selector or topological/exact silence",
            "constraint_piece": "domain wall/vector/preferred-frame terms",
            "stress_source_piece": "projector stress and PPN alpha_i/xi channels",
            "local_silence_condition": "auxiliary algebraic constraint with zero kinetic/domain-wall stress",
            "status": "PARTIAL_CLAUSE_NOT_PARENT_CLOSED",
            "effect_on_3006": "requires source-ready residual if not proved",
        }
    ),
    base(
        {
            "variation_id": "VAR3007_7_PiM",
            "sector": "Pi_M/source charge",
            "delta_action_contract": "delta(Pi_M J_H)=Pi_M delta J_H+(delta Pi_M)J_H",
            "eom_piece": "Ward/Euler flux closure and exterior homology",
            "theta_piece": "projector/source theta contribution or exact zero",
            "qtau_piece": "Q_M[tau] equals Hamiltonian charge piece",
            "constraint_piece": "commutator/flux residual",
            "stress_source_piece": "delta Pi_M stress and source mass denominator",
            "local_silence_condition": "Pi_M fixed chain map or bounded commutator/stress row",
            "status": "MISSING_PIM_SOURCE_BRIDGE",
            "effect_on_3006": "M_H_ref denominator remains unavailable",
        }
    ),
    base(
        {
            "variation_id": "VAR3007_8_kappa",
            "sector": "kappa topological",
            "delta_action_contract": "delta_{A_3} S_kappa -> d kappa_eff=0; delta_kappa gives topological constraint",
            "eom_piece": "constant universal coupling",
            "theta_piece": "topological/exact only",
            "qtau_piece": "no local source charge if superselected",
            "constraint_piece": "global/topological constraint",
            "stress_source_piece": "no local matter/species/domain drift",
            "local_silence_condition": "A_3/kappa sector adopted and labels forbidden",
            "status": "CANDIDATE_NOT_ADOPTED",
            "effect_on_3006": "G_eff drift remains residual if not adopted",
        }
    ),
    base(
        {
            "variation_id": "VAR3007_9_tau_surface",
            "sector": "tau/surface/readout",
            "delta_action_contract": "L_tau acts on every retained field and surface/reference data consistently",
            "eom_piece": "gauge/readout lock rather than new dynamics",
            "theta_piece": "i_tau theta_MTS uses same tau",
            "qtau_piece": "Q_tau on linked surfaces only",
            "constraint_piece": "surface/tau mismatch residual",
            "stress_source_piece": "clock/readout/source mismatch channels",
            "local_silence_condition": "tau_source=tau_charge=tau_clock=tau_readout",
            "status": "MISSING_TAU_SURFACE_LOCK",
            "effect_on_3006": "H_tau cannot be promoted without this lock",
        }
    ),
]


omission_rows = [
    base(
        {
            "omission_id": "OMIT3007_0_higher_derivative",
            "sector": "higher-curvature / higher-derivative",
            "omit_allowed_if": "normal form explicitly sets coefficients zero, topological, or below sourced local bounds",
            "if_not_omitted": "retain E_HD, theta_HD and PPN/R10 residual coefficients",
            "current_status": "RETAIN_BOUND_INPUT",
            "why_it_matters": "otherwise local GR can be spoiled while EH comparator still looks present",
            "source_anchors": "SAV1841_0_higher_derivative",
        }
    ),
    base(
        {
            "omission_id": "OMIT3007_1_nonminimal",
            "sector": "nonminimal matter-geometry/MTS coupling",
            "omit_allowed_if": "matter functor descends q-only through e_obs and forbids source/species/domain labels",
            "if_not_omitted": "retain WEP/clock/PPN/R10 coefficient rows",
            "current_status": "NOT_FORBIDDEN_BY_COMPLETE_PARENT_ACTION",
            "why_it_matters": "this is the coupling loophole that can fake or break source universality",
            "source_anchors": "SAV1841_3_nonminimal;NF2990_5_matter_qpullback",
        }
    ),
    base(
        {
            "omission_id": "OMIT3007_2_preferred_frame",
            "sector": "vector/coframe/preferred-frame leakage",
            "omit_allowed_if": "tau/coframe is gauge/constraint locked with no independent kinetic stress",
            "if_not_omitted": "retain PPN alpha_i, clock drift and xi residual rows",
            "current_status": "LOCAL_FRAME_AND_TAU_LOCK_UNSIGNED",
            "why_it_matters": "preferred-frame leakage would kill local PPN even with a good metric sector",
            "source_anchors": "SAV1841_4_memory_coframe;FV512_3_domain_selector",
        }
    ),
    base(
        {
            "omission_id": "OMIT3007_3_fitted_boundary",
            "sector": "fitted boundary/reference subtraction",
            "omit_allowed_if": "B_ref/H_ref selected before source/readout fitting",
            "if_not_omitted": "boundary ambiguity stays explicit and denominator remains blocked",
            "current_status": "REFERENCE_LOCK_UNSIGNED",
            "why_it_matters": "a fitted reference can hide the mass/source normalization proof",
            "source_anchors": "SNF2990_1_boundary;MAT2552_5_reference_pack",
        }
    ),
    base(
        {
            "omission_id": "OMIT3007_4_EH_only_import",
            "sector": "EH-only current import",
            "omit_allowed_if": "never allowed as total MTS proof; only reference comparator",
            "if_not_omitted": "would smuggle GR charge while ignoring MTS sectors",
            "current_status": "REJECTED_SHORTCUT",
            "why_it_matters": "avoids proving Newton by secretly inserting Newton/GR normalization",
            "source_anchors": "SEC3006_0_EH_core;REQ2551_6_no_shortcuts",
        }
    ),
    base(
        {
            "omission_id": "OMIT3007_5_arena_switch",
            "sector": "local/cosmology arena transition scale",
            "omit_allowed_if": "L_cg/ell_tr derived from operator spectrum, topology, mass gap or source compactness",
            "if_not_omitted": "retain transition-scale residual and no unified-field claim",
            "current_status": "OPEN",
            "why_it_matters": "prevents local GR and cosmological memory from being stitched by hand",
            "source_anchors": "FV512_6_transition_scale",
        }
    ),
]


feed_rows = [
    base(
        {
            "feed_id": "FEED3007_0_theta",
            "feeds_3006_row": "HTE3006_0_theta",
            "object": "theta_MTS",
            "grammar_feed": "theta_MTS=sum(theta_EH,theta_matter,theta_boundary,theta_GK,theta_memory,theta_selector,theta_PiM,theta_kappa)",
            "current_status": "SCHEMA_READY_NOT_SIGNED",
            "blocking_gap": "theta_i missing or unsigned for every non-EH retained sector",
            "promotion_effect": "no promotion; use as extraction contract",
        }
    ),
    base(
        {
            "feed_id": "FEED3007_1_Jtau",
            "feeds_3006_row": "HTE3006_1_Jtau",
            "object": "J_tau",
            "grammar_feed": "J_tau=theta_MTS(Phi,L_tau Phi)-i_tau L_parent with tau acting on all retained fields",
            "current_status": "FORMAL_SHAPE_READY_NOT_OWNER",
            "blocking_gap": "tau action and total L_parent not signed",
            "promotion_effect": "no promotion; tau/surface lock remains required",
        }
    ),
    base(
        {
            "feed_id": "FEED3007_2_Qtau",
            "feeds_3006_row": "HTE3006_2_Qtau",
            "object": "Q_tau^MTS",
            "grammar_feed": "Q_tau^MTS=sum_i Q_tau^i plus explicit exact/topological conventions",
            "current_status": "SCHEMA_READY_NOT_SIGNED",
            "blocking_gap": "non-EH Q_tau pieces and boundary/projector pieces are missing",
            "promotion_effect": "no total MTS charge claim",
        }
    ),
    base(
        {
            "feed_id": "FEED3007_3_constraints",
            "feeds_3006_row": "HTE3006_3_constraints",
            "object": "C_tau_total",
            "grammar_feed": "C_tau_total=C_EH+C_matter+C_boundary+C_GK+C_memory+C_selector+C_PiM+C_kappa",
            "current_status": "COMPONENT_LEDGER_READY_NOT_CLOSED",
            "blocking_gap": "common EOM/Ward split missing",
            "promotion_effect": "local current residual remains explicit",
        }
    ),
    base(
        {
            "feed_id": "FEED3007_4_Htau",
            "feeds_3006_row": "HTE3006_4_Htau_variation",
            "object": "delta H_tau",
            "grammar_feed": "int_S(delta Q_tau^MTS-i_tau theta_MTS)",
            "current_status": "CONTRACT_ONLY",
            "blocking_gap": "theta/Q_tau pieces not signed and H_tau curl not controlled",
            "promotion_effect": "no integrable H_tau claim",
        }
    ),
    base(
        {
            "feed_id": "FEED3007_5_Href_MHref",
            "feeds_3006_row": "HTE3006_6_Href;HTE3006_7_MHref_feed",
            "object": "H_ref and M_H_ref",
            "grammar_feed": "H_tau[S_outer]-H_ref with fixed reference and positive same-frame source bridge",
            "current_status": "BLOCKED_NONCLAIM",
            "blocking_gap": "fixed reference, source bridge and positivity missing",
            "promotion_effect": "denominator remains closed",
        }
    ),
    base(
        {
            "feed_id": "FEED3007_6_verdict",
            "feeds_3006_row": "HTE3006_8_verdict",
            "object": "H_tau_current_owner",
            "grammar_feed": "3007 gives a grammar and variation ledger only",
            "current_status": "CURRENT_OWNER_NOT_PROMOTED",
            "blocking_gap": "hard sectors still require derivation/source bounds",
            "promotion_effect": "move to 3008 hard sector action existence",
        }
    ),
]


gate_rows = [
    base(
        {
            "gate_id": "GATE3007_0_sources",
            "gate": "all 3007 source anchors exist",
            "gate_status": "PASS" if all(boolish(row["path_exists"]) and boolish(row["anchors_found"]) for row in source_rows) else "FAIL",
            "condition_passed": all(boolish(row["path_exists"]) and boolish(row["anchors_found"]) for row in source_rows),
            "promotion_allowed_now": False,
            "reason": "source register is evidence for grammar construction only",
        }
    ),
    base(
        {
            "gate_id": "GATE3007_1_minimal_grammar",
            "gate": "minimal parent-action grammar exists",
            "gate_status": "PASS_AS_NONCLAIM_SCAFFOLD",
            "condition_passed": True,
            "promotion_allowed_now": False,
            "reason": "grammar rows exist, but signatures/variations are not parent-signed",
        }
    ),
    base(
        {
            "gate_id": "GATE3007_2_non_EH_channels_explicit",
            "gate": "non-EH sectors are explicit",
            "gate_status": "PASS",
            "condition_passed": all(
                any(token in row["sector"] for token in ["EH", "matter", "boundary", "Gamma", "memory", "domain", "Pi_M", "kappa", "tau", "verdict", "total"])
                for row in grammar_rows
            ),
            "promotion_allowed_now": False,
            "reason": "no hidden EH-only total-current shortcut is allowed",
        }
    ),
    base(
        {
            "gate_id": "GATE3007_3_variation_owner",
            "gate": "every retained sector has parent-signed variation",
            "gate_status": "FAIL_CLOSED",
            "condition_passed": False,
            "promotion_allowed_now": False,
            "reason": "matter/source, boundary, GK, memory, selector, Pi_M, kappa and tau locks remain unsigned",
        }
    ),
    base(
        {
            "gate_id": "GATE3007_4_theta_Qtau_feed",
            "gate": "theta/Q_tau/H_tau can be promoted from feed rows",
            "gate_status": "BLOCKED_NONCLAIM",
            "condition_passed": False,
            "promotion_allowed_now": False,
            "reason": "feed rows are extraction contracts, not source-backed values",
        }
    ),
    base(
        {
            "gate_id": "GATE3007_5_local_claims",
            "gate": "local GR/Newton/PPN/WEP/R10 claim allowed",
            "gate_status": "FAIL_CLOSED",
            "condition_passed": False,
            "promotion_allowed_now": False,
            "reason": "parent action grammar is staged but hard sector derivations remain missing",
        }
    ),
]


decision_rows = [
    base(
        {
            "decision_id": "DEC3007_0_select_grammar",
            "decision": "Keep the selected normal-form grammar as the private parent-action scaffold.",
            "rationale": "It is the narrowest route that can still become a real GR-like reduction: every sector is either varied, made exact/topological/silent, bounded, or explicitly demoted.",
            "next_effect": "theta_MTS/Q_tau/H_tau now have a concrete sector checklist instead of a vague missing-parent-action label.",
        }
    ),
    base(
        {
            "decision_id": "DEC3007_1_no_promotion",
            "decision": "Do not promote the grammar to a field theory claim.",
            "rationale": "A grammar is not a varied action; hard sectors still lack action existence, source descent, current pieces and no-cancellation proofs.",
            "next_effect": "all rows remain nonclaim and local GR/Newton stays blocked.",
        }
    ),
    base(
        {
            "decision_id": "DEC3007_2_coupling_key",
            "decision": "Treat nonminimal/source coupling as the dangerous central loophole.",
            "rationale": "If matter/source coupling has hidden direct slots, even a good EH comparator and q_loc zero proof will not deliver universal Newton/GR.",
            "next_effect": "the next derivation must not only silence q_loc; it must prevent hidden coupling/source prefactors.",
        }
    ),
    base(
        {
            "decision_id": "DEC3007_3_next",
            "decision": "Move to hard sector action existence or explicit residual split.",
            "rationale": "The grammar reduces the problem to concrete hard sectors; the highest-risk local one is Gamma/Khat/q_loc, with matter/source coupling as the paired guard.",
            "next_effect": "3008 should try to derive S_GK/response Ward residual or demote it to explicit local-bound rows while preserving matter descent guard.",
        }
    ),
]


next_rows = [
    base(
        {
            "next_id": "NEXT3007_0_3008",
            "priority": "selected_primary",
            "target_doc": "3008-Y5-R2FR-Gamma-Khat-q_loc-action-existence-or-explicit-residual-split-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_Gamma_Khat_q_loc_action_existence_or_explicit_residual_split_under_AX1090_3008.py",
            "mission": "Try to construct the hard Gamma/Khat/q_loc parent action block that makes q_loc a Ward/Euler residual with double-zero local silence; if that fails, split it into source-ready finite residual rows guarded by matter/source coupling descent.",
            "success_condition": "either S_GK supplies E_A, theta_GK, Q_tau^GK and local double-zero clauses, or q_loc/GK leakage is demoted into explicit nonclaim residual rows without hiding inside EH.",
            "fallback_if_fail": "keep Hamiltonian-current route closure-only and move to sourcing local residual bounds for q_loc, projector stress, nonminimal coupling and source-prefactor channels.",
            "guardrails": "no EH-only current import; no orbital-GM denominator; no full q_loc zero claim without S_GK or sourced bounds; no hidden matter/source prefactor; no local-GR/Newton/PPN/WEP/R10 claim; no GitHub; no formalization-workbench edits",
        }
    )
]


write_csv(OUTPUTS["sources"], source_rows)
write_csv(OUTPUTS["grammar"], grammar_rows)
write_csv(OUTPUTS["fields"], field_rows)
write_csv(OUTPUTS["variation"], variation_rows)
write_csv(OUTPUTS["omissions"], omission_rows)
write_csv(OUTPUTS["feed"], feed_rows)
write_csv(OUTPUTS["gates"], gate_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

shutil.copyfile(OUTPUTS["grammar"], BRANCH_OUTPUTS["grammar_copy"])
shutil.copyfile(OUTPUTS["variation"], BRANCH_OUTPUTS["variation_copy"])
shutil.copyfile(OUTPUTS["feed"], BRANCH_OUTPUTS["theta_qtau_feed_copy"])
shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = []
for copy_id, path in BRANCH_OUTPUTS.items():
    copy_rows = rows(path)
    claim_flags_present = any(
        boolish(row.get("valid_for_claim")) or boolish(row.get("claim_allowed")) or boolish(row.get("score_ready")) or boolish(row.get("valid_prediction_row"))
        for row in copy_rows
    )
    branch_rows.append(
        base(
            {
                "copy_id": copy_id,
                "path": str(path),
                "path_exists": path.exists(),
                "row_count": len(copy_rows),
                "csv_parse_ok": csv_ok(path),
                "claim_flags_present": claim_flags_present,
            }
        )
    )
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
    base(
        {
            "validation_id": "VAL3007_00_sources_exist",
            "passed": all(boolish(row["path_exists"]) for row in source_rows),
            "detail": "every cited source path exists",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3007_01_source_anchors",
            "passed": all(boolish(row["anchors_found"]) for row in source_rows),
            "detail": "every source contains required anchors",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3007_02_grammar_written",
            "passed": len(grammar_rows) >= 10 and any(row["grammar_id"] == "G3007_10_verdict" for row in grammar_rows),
            "detail": "minimal parent action grammar contains total, sector and verdict rows",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3007_03_non_EH_sectors_explicit",
            "passed": all(token in " ".join(row["sector"] for row in grammar_rows) for token in ["matter", "boundary", "Gamma", "memory", "Pi_M"]),
            "detail": "non-EH local/source sectors are explicit and cannot hide inside EH",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3007_04_field_list_written",
            "passed": len(field_rows) >= 12 and all(not boolish(row.get("can_be_fundamental_now")) or row["field_id"] in {"FLD3007_0_metric", "FLD3007_2_matter"} for row in field_rows),
            "detail": "retained field list separates fundamental anchors from derived/conditional variables",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3007_05_variation_ledger_nonclaim",
            "passed": len(variation_rows) >= 10 and all(not boolish(row["valid_for_claim"]) for row in variation_rows),
            "detail": "sector variation ledger exists and remains nonclaim",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3007_06_omitted_sectors_demoted",
            "passed": len(omission_rows) >= 6 and all(row["if_not_omitted"] for row in omission_rows),
            "detail": "omitted sectors carry explicit if-not-omitted residual policy",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3007_07_feed_rows_blocked",
            "passed": all(
                any(token in row["current_status"] for token in ["NOT_SIGNED", "BLOCKED", "NOT_OWNER", "NOT_CLOSED", "CONTRACT_ONLY", "NOT_PROMOTED"])
                for row in feed_rows
            ),
            "detail": "theta/Q_tau/H_tau feed rows do not promote current owner",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3007_08_local_claims_blocked",
            "passed": any(row["gate_id"] == "GATE3007_5_local_claims" and not boolish(row["promotion_allowed_now"]) for row in gate_rows),
            "detail": "no local GR/Newton/PPN/WEP/R10 claim is allowed",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3007_09_next_target_hard_sector",
            "passed": next_rows[0]["target_doc"].startswith("3008-Y5-R2FR-Gamma-Khat-q_loc-action-existence"),
            "detail": "3008 selects hard Gamma/Khat/q_loc action-existence or residual split",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3007_10_branch_copies",
            "passed": all(boolish(row["path_exists"]) and boolish(row["csv_parse_ok"]) and not boolish(row["claim_flags_present"]) for row in branch_rows),
            "detail": "branch copies exist, parse, and carry no claim flags",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3007_11_csv_parse",
            "passed": all(csv_ok(path) for path in list(OUTPUTS.values())[:-1] + list(BRANCH_OUTPUTS.values())),
            "detail": "all 3007 CSV outputs parse cleanly",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3007_12_paths_under_post_checkpoint",
            "passed": all(under(path, ROOT) for path in generated_paths),
            "detail": "all generated outputs are under post-checkpoint-work",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3007_13_formalization_untouched",
            "passed": not any(FORMALIZATION.rglob("*3007*")) if FORMALIZATION.exists() else True,
            "detail": "no targeted 3007 files exist under formalization-workbench",
            "required": True,
        }
    ),
    base(
        {
            "validation_id": "VAL3007_14_no_claim_flags",
            "passed": no_claim_flags(list(OUTPUTS.values())[:-1] + list(BRANCH_OUTPUTS.values())),
            "detail": "all generated rows remain valid_for_claim=false and claim_allowed=false",
            "required": True,
        }
    ),
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    base(
        {
            "validation_id": "VAL3007_OVERALL",
            "passed": overall_pass,
            "detail": "3007 stages a minimal parent-action sector grammar, variation ledger and theta/Q_tau feed rows without promoting local GR/Newton",
            "required": True,
        }
    )
)
write_csv(OUTPUTS["validation"], validation_rows)


doc = f"""# 3007 - Y5/R2FR Minimal Parent Action Sector Grammar Or Sector Variation Ledger Under AX1090

Status: `Y5_R2FR_3007_minimal_parent_action_grammar_staged_not_signed_hard_sector_3008_next`

Generated: `{RUN_UTC}`

## Current Verdict

3007 turns the 3006 missing-parent-action label into an actual sector grammar. The best private scaffold is:

`S_parent^loc = S_EH + S_matter[q^*e_obs,psi] + S_boundary_fixed + S_extra[Z] + S_selector/PiM + S_worldtube + S_constraint + S_residual_explicit`.

That is a useful leap forward, because it tells us exactly what has to be varied before the local GR/Newton route can be claimed. It also prevents the bad shortcut: EH is a comparator/reference block, not the total MTS charge.

Current MTS is still not promoted. The grammar is a contract, not a signed parent action. Matter/source descent, Gamma/Khat/q_loc action existence, boundary/reference lock, memory double-zero, selector/projector stress, Pi_M source bridge, kappa topological adoption and tau/surface lock all remain unsigned or residualized.

The coupling issue is now front and centre: hidden nonminimal/source prefactors are the thing that can quietly break universal Newton/GR even if the metric side looks good. So 3008 should attack the hard Gamma/Khat/q_loc action block while guarding against hidden matter/source coupling.

## Source Register

{md_table(source_rows, ["source_id", "path_exists", "anchors_found", "missing_anchors", "role"])}

## Minimal Parent Action Grammar

{md_table(grammar_rows, ["grammar_id", "sector", "retention_class", "action_block", "current_status", "residual_symbol", "promotion_blocker"])}

## Retained Field List

{md_table(field_rows, ["field_id", "symbol", "sector_owner", "status", "variation_role", "can_be_fundamental_now", "missing_certificate"])}

## Sector Variation Ledger

{md_table(variation_rows, ["variation_id", "sector", "delta_action_contract", "theta_piece", "qtau_piece", "constraint_piece", "status", "effect_on_3006"])}

## Omitted Sector Demotion Ledger

{md_table(omission_rows, ["omission_id", "sector", "omit_allowed_if", "if_not_omitted", "current_status", "why_it_matters"])}

## Theta/Q_tau Feed Rows

{md_table(feed_rows, ["feed_id", "feeds_3006_row", "object", "grammar_feed", "current_status", "blocking_gap", "promotion_effect"])}

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

This is a good movement toward the goal, but it is not the finish line. We now have the skeleton of the field theory written in the right language: a parent action grammar with sector variation obligations. The grim bit is that the biggest obligations are still real: no hidden coupling, no EH-only import, no q_loc zero by declaration, no source mass from orbital GM. The hopeful bit is that the problem has become finite and named. We are no longer waving at 'derive local GR'; we are asking whether specific parent action blocks can own specific currents and residuals.

## Forbidden Claims From 3007

- `S_parent^loc` is a signed complete MTS parent action.
- `theta_MTS` or `Q_tau^MTS` has been extracted from a complete parent action.
- EH current is the total MTS current.
- `q_loc^nu` is locally zero.
- Matter/source coupling is universally descended through `q(Phi)`.
- `H_tau`, `H_ref` or `M_H_ref` is promoted as a denominator.
- Local GR/Newton/PPN/WEP/R10 pass.
"""

DOC.write_text(doc, encoding="utf-8")

if not overall_pass:
    failed = [row["validation_id"] for row in validation_rows if not boolish(row["passed"])]
    raise SystemExit(f"3007 validation failed: {failed}")

print(f"wrote {DOC}")
for key, path in OUTPUTS.items():
    print(f"{key}: {path}")
for key, path in BRANCH_OUTPUTS.items():
    print(f"{key}: {path}")
