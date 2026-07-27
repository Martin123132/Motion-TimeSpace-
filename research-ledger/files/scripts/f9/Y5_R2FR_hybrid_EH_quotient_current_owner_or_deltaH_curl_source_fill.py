from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1647"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1647-Y5-R2FR-hybrid-EH-quotient-current-owner-or-deltaH-curl-source-fill.md"

SOURCE_FILES = {
    "1646_doc": ROOT / "1646-Y5-R2FR-theta-Qtau-current-owner-or-deltaH-component-source-row.md",
    "1646_validation": OUT / "P8_Y5_BRR545_1646_VALIDATION.csv",
    "1646_next": OUT / "P8_Y5_PARENT_QLOC_1646_NEXT_TARGET.csv",
    "1646_current": OUT / "P8_Y5_PARENT_QLOC_1646_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
    "1646_qtau": OUT / "P8_Y5_PARENT_QLOC_1646_QTAU_DECOMPOSITION_STATUS.csv",
    "772_doc": ROOT / "772-Y5-R10-hybrid-EH-quotient-current-owner-or-deltaH-curl-source-fill.md",
    "772_validation": OUT / "P8_Y5_BRR545_772_VALIDATION.csv",
    "772_hybrid": OUT / "P8_Y5_R10_772_HYBRID_CURRENT_OWNER_AUDIT.csv",
    "772_narrow": OUT / "P8_Y5_R10_772_NARROW_ZERO_IMPORT_LEDGER.csv",
    "772_curl": OUT / "P8_Y5_R10_772_DELTAH_CURL_DECOMPOSITION.csv",
    "772_fallback": OUT / "P8_Y5_R10_772_DELTAH_CURL_SOURCE_FILL_FALLBACK.csv",
    "772_decision": OUT / "P8_Y5_R10_772_DECISION_MATRIX.csv",
    "734_zero": OUT / "P8_Y5_R10_734_FIRST_ZERO_ATTEMPT.csv",
    "735_zero": OUT / "P8_Y5_R10_735_SECOND_ZERO_ATTEMPT.csv",
    "736_zero": OUT / "P8_Y5_R10_736_THIRD_ZERO_ATTEMPT.csv",
    "737_doc": ROOT / "737-Y5-R10-source-current-Ward-flux-closure-or-source-backed-Y5-inputs.md",
    "738_doc": ROOT / "738-Y5-R10-PiM-projector-owner-or-radial-bound-runner.md",
    "773_doc": ROOT / "773-Y5-R10-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md",
    "773_validation": OUT / "P8_Y5_BRR545_773_VALIDATION.csv",
    "773_component": OUT / "P8_Y5_R10_773_DELTAH_CURL_COMPONENT_FILL.csv",
}

NEEDLES = {
    "1646_doc": ["1647-Y5-R2FR", "hybrid EH plus quotient-silent extra route"],
    "1646_validation": ["VAL1646_OVERALL", "PASS"],
    "1646_next": ["1647-Y5-R2FR-hybrid-EH-quotient-current-owner-or-deltaH-curl-source-fill.md"],
    "1646_current": ["TQ1646_5_owner_verdict", "FAIL_CURRENT_CLAIM"],
    "1646_qtau": ["QTS1646_5_total", "NOT_PROMOTED"],
    "772_doc": ["hybrid route is useful but not yet a full current owner", "observed reduced"],
    "772_validation": ["V772_9_next_target_selected", "pass"],
    "772_hybrid": ["HCO772_7_owner_verdict", "fail_current_corpus"],
    "772_narrow": ["NZI772_0_representative_q_loc_variation", "imported_conditional_zero"],
    "772_curl": ["CDC772_2_observed_reduced_boundary_flux", "open_primary_next_target"],
    "772_fallback": ["HSF772_0_observed_reduced_boundary_flux", "MISSING_OBSERVED_REDUCED_BOUNDARY_FLUX_ZERO_OR_NUMERIC"],
    "772_decision": ["D772_2_next_target", "observed reduced boundary/source flux"],
    "734_zero": ["FZA734_0_representative_vertical_q_loc_variation", "derived_narrow_zero_row_conditional"],
    "735_zero": ["SZA735_0_proper_representative_boundary_charge", "zero"],
    "736_zero": ["TZA736_0_direct_representative_matter_marker", "zero"],
    "737_doc": ["Source-Current Ward", "projected source flux"],
    "738_doc": ["PiM", "projector"],
    "773_doc": ["reduced Ward/no-flux path", "B_observed_reduced_flux_over_MH"],
    "773_validation": ["V773_9_next_target_selected", "pass"],
    "773_component": ["B_observed_reduced_flux_over_MH", "MISSING"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1647_SOURCE_REGISTER.csv"
HYBRID_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1647_HYBRID_CURRENT_OWNER_AUDIT.csv"
NARROW_ZERO = OUT / "P8_Y5_PARENT_QLOC_1647_NARROW_ZERO_IMPORT_LEDGER.csv"
CURL = OUT / "P8_Y5_PARENT_QLOC_1647_DELTAH_CURL_DECOMPOSITION.csv"
FALLBACK = OUT / "P8_Y5_PARENT_QLOC_1647_DELTAH_CURL_SOURCE_FILL_FALLBACK.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1647_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1647_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1647_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1647_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    HYBRID_AUDIT,
    NARROW_ZERO,
    CURL,
    FALLBACK,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    HYBRID_AUDIT,
    NARROW_ZERO,
    CURL,
    FALLBACK,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {"valid_for_claim", "valid_for_mts_claim", "claim_allowed", "score_allowed"}
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1647 hybrid EH-plus-quotient current-owner test",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def hybrid_audit_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HCO1647_0_observed_EH_current",
            "hybrid_clause": "observed GR sector uses the EH current",
            "test": "Q_tau^MTS has an EH part Q_EH[g_obs,tau] with fixed boundary/reference",
            "current_result": "CONDITIONAL_REFERENCE_ALLOWED",
            "what_it_prunes": "prevents rebuilding the GR Hamiltonian current from scratch where observed EH assumptions truly hold",
            "what_remains": "EH-only does not own MTS extra, boundary, q_loc/Y5/Y6, projector, tau/reference, or coupling terms",
            "claim_status": "BASELINE_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HCO1647_1_hybrid_split",
            "hybrid_clause": "parent configuration splits into observed quotient plus representative fibre",
            "test": "Y=(O_GR,Phi_red,R_rep,B_ref) and pi_h(Y)=(O_GR,Phi_red,B_ref)",
            "current_result": "FORMAL_MAP_CONSTRUCTED_NOT_FULL_PARENT_SIGNATURE",
            "what_it_prunes": "representative variables are not automatically observed local fields",
            "what_remains": "Gamma/Khat/P_loc symbol match, matter descent, boundary/reference and ADM separation remain unsigned",
            "claim_status": "CANDIDATE_SPLIT_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HCO1647_2_representative_vertical_zero",
            "hybrid_clause": "representative-fibre motion cannot directly source q_loc when q_loc objects are pullbacks",
            "test": "L_{v_X^rep} q_loc^nu=0 under Gamma/Khat/P_loc pullback premises",
            "current_result": "NARROW_ZERO_IMPORTED",
            "what_it_prunes": "direct hidden representative fifth-force source",
            "what_remains": "observed reduced q_loc itself can be nonzero through Phi_red/Euler/boundary/source terms",
            "claim_status": "PARTIAL_ZERO_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HCO1647_3_proper_boundary_zero",
            "hybrid_clause": "proper representative transformations have zero representative boundary charge",
            "test": "Q_X^rep[partial U]=0 for compact-support or boundary-collar-vanishing v_X^rep",
            "current_result": "NARROW_ZERO_IMPORTED",
            "what_it_prunes": "pure representative improper edge charge",
            "what_remains": "observed reduced boundary/source-measure flux and non-proper edge modes remain live",
            "claim_status": "PARTIAL_ZERO_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HCO1647_4_matter_marker_zero",
            "hybrid_clause": "ordinary matter/readout has no direct representative marker",
            "test": "delta_{v_X^rep}S_matter=0 if matter functors factor through Q_obs^hybrid",
            "current_result": "NARROW_ZERO_IMPORTED_CONDITIONAL",
            "what_it_prunes": "direct representative matter-marker/source-frame charge",
            "what_remains": "full source normalization, mu_extra, PiM flux closure, Gauss/orbital calibration and PPN stability remain open",
            "claim_status": "PARTIAL_ZERO_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HCO1647_5_reduced_q_loc_owner",
            "hybrid_clause": "Gamma/Khat/P_loc are owned by a reduced GK action on Q_obs^hybrid",
            "test": "S_GK^hyb gives Gamma_eff=gamma, K_hat=metric response, q_loc=P_loc div(T_GK)",
            "current_result": "FAILED_CURRENT_SYMBOL_MATCH",
            "what_it_prunes": "nothing beyond conditional pullback zero",
            "what_remains": "observed q_loc residual, Y5/Y6, PPN tail, boundary flux, and source projection",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HCO1647_6_source_projector_owner",
            "hybrid_clause": "same-frame source current and PiM projector close projected mass flux",
            "test": "d(Pi_M J_H)=0 on compact local exterior",
            "current_result": "BLOCKED_BY_SOURCE_PROJECTOR_CHAIN",
            "what_it_prunes": "standard matter Ward identity only",
            "what_remains": "projector commutator, exchange flux, boundary/anomaly flux, Hilbert/topological equality",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HCO1647_7_owner_verdict",
            "hybrid_clause": "accept hybrid EH+quotient current owner for FB5540/q_R local branch",
            "test": "HCO1647_0 through HCO1647_6 jointly close",
            "current_result": "FAIL_CURRENT_CLAIM",
            "what_it_prunes": "representative-only ghost channels are pruned",
            "what_remains": "observed reduced boundary/source flux and deltaH curl must be derived or source-filled",
            "claim_status": "NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def narrow_zero_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "zero_id": "NZI1647_0_representative_q_loc_variation",
            "source_row": "FZA734_0_representative_vertical_q_loc_variation",
            "zero_statement": "L_{v_X^rep} q_loc^nu=0 under hybrid pullback premises",
            "status_after_1647": "IMPORTED_CONDITIONAL_ZERO",
            "legitimate_use": "remove direct representative-fibre source dependence",
            "forbidden_use": "claim observed q_loc^nu=0 or local-GR pass",
            "residual_left": "observed reduced q_loc from Phi_red/Euler/boundary/source terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "zero_id": "NZI1647_1_proper_representative_boundary",
            "source_row": "SZA735_0_proper_representative_boundary_charge",
            "zero_statement": "Q_X^rep[partial U]=0 for proper representative transformations",
            "status_after_1647": "IMPORTED_CONDITIONAL_ZERO",
            "legitimate_use": "remove pure representative improper boundary charge from proper gauge domain",
            "forbidden_use": "claim observed boundary/source-measure flux vanishes",
            "residual_left": "observed reduced boundary flux, edge modes, corner flux, ADM/reference split",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "zero_id": "NZI1647_2_proper_corner_symplectic",
            "source_row": "SZA735_1_proper_corner_symplectic_flux",
            "zero_statement": "Omega_boundary(delta Y,v_X^rep)=0 for representative support vanishing in boundary collar",
            "status_after_1647": "IMPORTED_CONDITIONAL_ZERO",
            "legitimate_use": "remove proper representative corner symplectic leakage",
            "forbidden_use": "erase non-representative corner/source flux",
            "residual_left": "boundary flux carried by Q_obs^hybrid/Phi_red/matter readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "zero_id": "NZI1647_3_matter_no_marker",
            "source_row": "TZA736_0_direct_representative_matter_marker",
            "zero_statement": "delta_{v_X^rep}S_matter=0 under strict no-marker one-coframe contract",
            "status_after_1647": "IMPORTED_CONDITIONAL_ZERO",
            "legitimate_use": "remove direct representative matter-marker coupling",
            "forbidden_use": "claim full Y5 source normalization or WEP derivation",
            "residual_left": "dressed source mass, mu_extra, C_qmu q_loc, Gauss calibration, PPN stability",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "zero_id": "NZI1647_4_ADM_double_count_guard",
            "source_row": "SZA735_2_ADM_double_count_guard",
            "zero_statement": "ordinary ADM/time/rotation/boost charges remain in Q_obs^hybrid, not in representative vertical domain",
            "status_after_1647": "GUARD_IMPORTED_NOT_FULL_PROOF",
            "legitimate_use": "avoid quotienting away physical EH Hamiltonian generators",
            "forbidden_use": "claim PiM/Hilbert/source equality or M_H_ref calibration",
            "residual_left": "Pi_M/Pi_EH projection, M_H_ref, source equality and Poisson/Gauss calibration",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def curl_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "curl_id": "CDC1647_0_EH_observed_flux",
            "curl_term": "int_S i_tau omega_EH",
            "hybrid_status": "CONDITIONAL_GR_BASELINE",
            "zero_or_bound_condition": "observed local exterior is EH with fixed stationary boundary/reference",
            "current_result": "NOT_FULL_MTS_OWNER_BUT_ALLOWED_REFERENCE_PIECE",
            "source_fill_if_fails": "deltaH_EH_boundary_flux_over_MH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "curl_id": "CDC1647_1_representative_vertical_flux",
            "curl_term": "Omega_boundary(delta Y,v_X^rep)+Q_X^rep",
            "hybrid_status": "PROPER_REPRESENTATIVE_PIECE_PRUNED_CONDITIONALLY",
            "zero_or_bound_condition": "v_X^rep is proper/compact-supported and acts only in representative fibre",
            "current_result": "NARROW_ZERO_ONLY",
            "source_fill_if_fails": "QX_rep_improper_edge_flux_over_MH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "curl_id": "CDC1647_2_observed_reduced_boundary_flux",
            "curl_term": "P_loc B_boundary^nu and reduced observed source flux",
            "hybrid_status": "NOT_PRUNED",
            "zero_or_bound_condition": "reduced GK action owner plus on-shell fields plus boundary/source-measure no-flux",
            "current_result": "OPEN_PRIMARY_NEXT_TARGET",
            "source_fill_if_fails": "B_observed_reduced_flux_over_MH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "curl_id": "CDC1647_3_Y5_source_projector_flux",
            "curl_term": "d(Pi_M J_H) and source-normalization projection",
            "hybrid_status": "NOT_PRUNED",
            "zero_or_bound_condition": "PiM parent owner, zero commutator/exchange/boundary flux, Hilbert/topological equality",
            "current_result": "BLOCKED_BY_SOURCE_PROJECTOR_CHAIN",
            "source_fill_if_fails": "Y5_projected_source_flux_over_MH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "curl_id": "CDC1647_4_tau_reference_surface",
            "curl_term": "Delta_tau+Delta_S+Delta_ref",
            "hybrid_status": "NOT_PRUNED",
            "zero_or_bound_condition": "same observed tau, fixed surface/domain, fixed B_ref before readout",
            "current_result": "STILL_OPEN_FROM_1645_1646",
            "source_fill_if_fails": "tau_ref_surface_mismatch_over_MH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "curl_id": "CDC1647_5_total_deltaH",
            "curl_term": "delta_H_tau_nonintegrable_over_MH",
            "hybrid_status": "NOT_ZERO",
            "zero_or_bound_condition": "CDC1647_0 through CDC1647_4 all theorem-zero or source-backed bounds",
            "current_result": "SOURCE_FILL_REQUIRED_IF_NEXT_ZERO_FAILS",
            "source_fill_if_fails": "DHS1646_0_deltaH_curl",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def fallback_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "fill_id": "HSF1647_0_observed_reduced_boundary_flux",
            "quantity": "B_observed_reduced_flux_over_MH",
            "definition": "abs(P_loc B_boundary^nu contribution to curl(deltaH))/M_H_ref",
            "required_columns": "system_id;boundary_shell;P_loc;B_boundary_component;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_OBSERVED_REDUCED_BOUNDARY_FLUX_ZERO_OR_NUMERIC",
            "claim_gate": "theorem-zero or source-backed bound before deltaH pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "HSF1647_1_Y5_projected_source_flux",
            "quantity": "Y5_projected_source_flux_over_MH",
            "definition": "abs(integral_A d(Pi_M J_H))/M_H_ref or equivalent projected source-mass flux",
            "required_columns": "system_id;annulus;Pi_M_owner;flux_value;M_H_ref;units;source_path;valid_for_claim",
            "current_status": "MISSING_PIM_PROJECTED_FLUX_ZERO_OR_NUMERIC",
            "claim_gate": "closed projected mass current or source-backed radial/source flux bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "HSF1647_2_tau_ref_surface_mismatch",
            "quantity": "tau_ref_surface_mismatch_over_MH",
            "definition": "abs(Delta_tau+Delta_S+Delta_ref)/M_H_ref",
            "required_columns": "tau_id;surface_id;reference_branch;Delta_tau;Delta_S;Delta_ref;M_H_ref;source_path;valid_for_claim",
            "current_status": "MISSING_TAU_REF_SURFACE_ZERO_OR_NUMERIC",
            "claim_gate": "same tau/reference/surface theorem or source-backed mismatch bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "HSF1647_3_deltaH_total",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "definition": "sum of nonnegative curl components with no cancellation credit",
            "required_columns": "component_id;value;units;source_path;zero_theorem_or_bound;no_cancellation_flag;valid_for_claim",
            "current_status": "MISSING_COMPONENTS",
            "claim_gate": "every component zero/bounded and no placeholder markers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1647_0_hybrid_not_promoted",
            "decision": "do not accept the hybrid EH+quotient route as a full current owner yet",
            "reason": "it prunes representative-only channels but observed reduced q_loc/source/boundary/tau flux remains open",
            "effect": "H_tau/MHref/local-GR remain blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1647_1_keep_narrow_zeros",
            "decision": "retain the representative narrow zeros as discipline gates",
            "reason": "they remove fake representative channels and stop EH/ADM double counting",
            "effect": "representative ghosts are pruned but observed flux must still be derived or bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1647_2_next_observed_flux",
            "decision": "attack observed reduced boundary/source flux next",
            "reason": "it is the first live deltaH curl term not killed by representative quotient silence",
            "effect": "1648 should derive a reduced Ward/no-flux theorem or fill B_observed_reduced_flux_over_MH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1647_0_hybrid_current_owner",
            "claim": "hybrid EH+quotient route is a full current owner",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "OBSERVED_REDUCED_FLUX_AND_PROJECTOR_SOURCE_FLUX_OPEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1647_1_representative_narrow_zeros",
            "claim": "representative-only ghost channels are pruned",
            "gate_pass": True,
            "status": "PASS_AS_NARROW_INTERNAL_ZERO_ONLY",
            "blocker": "does not imply observed flux zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1647_2_deltaH_zero",
            "claim": "delta_H_tau_nonintegrable_over_MH is theorem-zero",
            "gate_pass": False,
            "status": "NO_CLAIM",
            "blocker": "B_observed_reduced_flux_over_MH and Y5_projected_source_flux_over_MH remain live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1647_3_local_GR_PPN_R10",
            "claim": "local GR, PPN, R10, or Newton pass follows from 1647",
            "gate_pass": False,
            "status": "NO_CLAIM",
            "blocker": "hybrid current owner remains nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1647_4_guardrail",
            "claim": "hybrid current-owner guardrail is installed",
            "gate_pass": True,
            "status": "PASS_AS_INTERNAL_GUARDRAIL_ONLY",
            "blocker": "guardrail is not evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1648-Y5-R2FR-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md",
            "script": "scripts/Y5_R2FR_observed_reduced_boundary_source_flux_zero_or_deltaH_curl_component_fill.py",
            "objective": "derive the observed reduced Ward/no-flux theorem for B_observed_reduced_flux_over_MH, or fill it as a source-ready deltaH curl component row",
            "success_condition": "S_red, Gamma_eff/K_hat/P_loc, reduced Euler equations, boundary/reference no-flux, source-measure silence, projector descent, and tau/surface lock jointly prove zero or yield explicit bounded rows",
            "guardrails": "do not reuse representative proper-zero as observed flux zero; no EH-only promotion; no fitted boundary condition; no PPN/local-GR/R10 claim",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for path in GENERATED + [VALIDATION]:
        if path.exists():
            shutil.copy2(path, QUARANTINE / path.name)
            shutil.copy2(path, BRANCH_RESIDUALS / path.name)
    shutil.copy2(HYBRID_AUDIT, QUEUE / "JR1647_HYBRID_CURRENT_OWNER_AUDIT_NONCLAIM.csv")
    shutil.copy2(FALLBACK, QUEUE / "JR1647_DELTAH_CURL_SOURCE_FILL_FALLBACK_NONCLAIM.csv")
    shutil.copy2(NEXT_TARGET, QUEUE / "JR1647_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, object]]:
    sources = csv_rows(SOURCE_REGISTER)
    hybrid = csv_rows(HYBRID_AUDIT)
    zeros = csv_rows(NARROW_ZERO)
    curl = csv_rows(CURL)
    fallback = csv_rows(FALLBACK)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)
    checks = [
        (
            "VAL1647_0_sources_exist",
            all(bool_string(row["path_exists"]) == "true" and bool_string(row["needles_found"]) == "true" for row in sources),
            "all cited 1647 source paths exist and needles are present",
        ),
        (
            "VAL1647_1_hybrid_owner_not_promoted",
            any(row["audit_id"] == "HCO1647_7_owner_verdict" and row["current_result"] == "FAIL_CURRENT_CLAIM" for row in hybrid),
            "hybrid owner audit refuses full promotion",
        ),
        (
            "VAL1647_2_narrow_zeros_imported",
            len(zeros) >= 5 and any(row["zero_id"] == "NZI1647_0_representative_q_loc_variation" for row in zeros),
            "representative narrow zeros and ADM guard imported",
        ),
        (
            "VAL1647_3_deltaH_live_terms_decomposed",
            any(row["curl_id"] == "CDC1647_2_observed_reduced_boundary_flux" and row["current_result"] == "OPEN_PRIMARY_NEXT_TARGET" for row in curl)
            and any(row["curl_id"] == "CDC1647_5_total_deltaH" and row["hybrid_status"] == "NOT_ZERO" for row in curl),
            "deltaH curl live terms are decomposed",
        ),
        (
            "VAL1647_4_fallback_rows_staged",
            any(row["fill_id"] == "HSF1647_0_observed_reduced_boundary_flux" for row in fallback)
            and all(bool_string(row["valid_for_claim"]) == "false" for row in fallback),
            "fallback source rows are staged as nonclaim",
        ),
        (
            "VAL1647_5_next_observed_flux_selected",
            any(row["decision_id"] == "DEC1647_2_next_observed_flux" for row in decisions),
            "observed reduced boundary/source flux selected next",
        ),
        (
            "VAL1647_6_claim_gates_safe",
            any(row["gate_id"] == "CG1647_4_guardrail" and row["status"] == "PASS_AS_INTERNAL_GUARDRAIL_ONLY" for row in gates)
            and all(bool_string(row["claim_allowed"]) == "false" for row in gates),
            "all claim gates keep MTS claims false",
        ),
        (
            "VAL1647_7_next_target_selected",
            next_targets[0]["next_target"] == "1648-Y5-R2FR-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md",
            "next target selects observed reduced boundary/source flux",
        ),
        (
            "VAL1647_8_csv_parse",
            all(len(csv_rows(path)) > 0 for path in GENERATED),
            "all generated 1647 CSVs parse",
        ),
        (
            "VAL1647_9_no_mts_claim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1647 generated rows keep MTS claim/no-score flags false",
        ),
        (
            "VAL1647_10_branch_copies",
            all((QUARANTINE / path.name).exists() and (BRANCH_RESIDUALS / path.name).exists() for path in GENERATED),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1647_11_queue_copies",
            all(
                path.exists()
                for path in [
                    QUEUE / "JR1647_HYBRID_CURRENT_OWNER_AUDIT_NONCLAIM.csv",
                    QUEUE / "JR1647_DELTAH_CURL_SOURCE_FILL_FALLBACK_NONCLAIM.csv",
                    QUEUE / "JR1647_NEXT_TARGET_NONCLAIM.csv",
                ]
            ),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1647_12_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1647_13_formalization_untouched",
            not any(FORMALIZATION.rglob("*1647*")) if FORMALIZATION.exists() else True,
            "no 1647 outputs found under formalization-workbench",
        ),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1647_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1647 hybrid EH quotient current-owner and deltaH curl source-fill validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    sources = csv_rows(SOURCE_REGISTER)
    hybrid = csv_rows(HYBRID_AUDIT)
    zeros = csv_rows(NARROW_ZERO)
    curl = csv_rows(CURL)
    fallback = csv_rows(FALLBACK)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)
    validation = csv_rows(VALIDATION)
    content = f"""# 1647 - Hybrid EH Quotient Current Owner Or deltaH Curl Source Fill

**Private status:** nonclaim checkpoint. No full hybrid current owner, `delta_H_tau` zero, stable Hamiltonian charge, `M_H_ref`, `M_*`, PPN pass, local-GR pass, Newton pass, R10 pass, WEP pass, clock pass, or orbital pass is claimed.

## Verdict

The hybrid route gets a real but narrow win:

```text
Q_tau^MTS = Q_EH + Q_extra + Q_boundary/ref + Q_projector + C_source
```

The EH piece remains a conditional GR baseline. Representative-only ghost channels can be pruned when they are proper, pullback-only, or matter-marker silent. But this does **not** prove the full current owner, because the surviving flux is observed/reduced, not merely representative:

```text
delta_H_tau curl still contains:
B_observed_reduced_flux_over_MH
Y5_projected_source_flux_over_MH
tau_ref_surface_mismatch_over_MH
```

So `delta_H_tau_nonintegrable_over_MH` is not theorem-zero. The next target is the observed reduced Ward/no-flux route: either derive `B_observed_reduced_flux_over_MH = 0`, or fill it as a source-backed component row.

## Source Register

{markdown_table(sources, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Hybrid Current Owner Audit

{markdown_table(hybrid, ["audit_id", "hybrid_clause", "test", "current_result", "what_it_prunes", "what_remains"])}

## Narrow Zero Import Ledger

{markdown_table(zeros, ["zero_id", "source_row", "zero_statement", "status_after_1647", "legitimate_use", "residual_left"])}

## deltaH Curl Decomposition

{markdown_table(curl, ["curl_id", "curl_term", "hybrid_status", "current_result", "source_fill_if_fails"])}

## deltaH Curl Source Fill Fallback

{markdown_table(fallback, ["fill_id", "quantity", "definition", "current_status", "claim_gate"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "effect"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        HYBRID_AUDIT: hybrid_audit_rows(),
        NARROW_ZERO: narrow_zero_rows(),
        CURL: curl_rows(),
        FALLBACK: fallback_rows(),
        DECISION: decision_rows(),
        CLAIM_GATE: claim_gate_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)
    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    copy_outputs()
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
