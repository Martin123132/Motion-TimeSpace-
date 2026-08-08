from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "772-Y5-R10-hybrid-EH-quotient-current-owner-or-deltaH-curl-source-fill.md"
NEXT_TARGET = "773-Y5-R10-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md"
STATUS = "Y5_R10_772_hybrid_EH_quotient_current_owner_audited_narrow_zeros_imported_observed_flux_still_open_nonclaim"
CLAIM_CEILING = "hybrid_EH_quotient_current_owner_audit_only_no_deltaH_zero_no_HPiM_integrability_no_Newton_no_PPN_no_R10_R11_or_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_772_SOURCE_REGISTER.csv"
HYBRID_OWNER_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_772_HYBRID_CURRENT_OWNER_AUDIT.csv"
NARROW_ZERO_IMPORT_PATH = RESIDUALS / "P8_Y5_R10_772_NARROW_ZERO_IMPORT_LEDGER.csv"
DELTAH_CURL_DECOMPOSITION_PATH = RESIDUALS / "P8_Y5_R10_772_DELTAH_CURL_DECOMPOSITION.csv"
SOURCE_FILL_FALLBACK_PATH = RESIDUALS / "P8_Y5_R10_772_DELTAH_CURL_SOURCE_FILL_FALLBACK.csv"
DECISION_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_772_DECISION_MATRIX.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_772_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_772_VALIDATION.csv"

CANDIDATE_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_772_HYBRID_CURRENT_OWNER_CERTIFICATE_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_772_DELTAH_CURL_NUMERIC_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_772_OBSERVED_BOUNDARY_FLUX_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_772_Y5_PIM_SOURCE_FLUX_INPUT_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    HYBRID_OWNER_AUDIT_PATH,
    NARROW_ZERO_IMPORT_PATH,
    DELTAH_CURL_DECOMPOSITION_PATH,
    SOURCE_FILL_FALLBACK_PATH,
    DECISION_MATRIX_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCES: dict[str, dict[str, Any]] = {
    "771_doc": {
        "path": POST_CHECKPOINT / "771-Y5-R10-theta-Qtau-current-owner-or-deltaH-component-source-row.md",
        "needles": [
            "hybrid EH plus quotient-silent extra route is the best next derivation attempt",
            "772-Y5-R10-hybrid-EH-quotient-current-owner-or-deltaH-curl-source-fill.md",
        ],
        "role": "immediate hybrid-current handoff",
    },
    "771_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_771_VALIDATION.csv",
        "needles": ["V771_4_hybrid_route_selected", "pass"],
        "role": "prior 771 validation guard",
    },
    "771_route": {
        "path": RESIDUALS / "P8_Y5_R10_771_CURRENT_OWNER_ROUTE_COMPARISON.csv",
        "needles": ["COR771_C_hybrid_EH_quotient_extra", "best_next_derivation_route"],
        "role": "hybrid route selection row",
    },
    "731_doc": {
        "path": POST_CHECKPOINT / "731-Y5-R10-choose-quotient-zero-or-diffeo-current-identity-and-close-boundary.md",
        "needles": ["Current route choice: **hybrid EH-plus-quotient-extra first**", "S_parent = S_EH[O_GR]"],
        "role": "initial hybrid route selection",
    },
    "731_contract": {
        "path": RESIDUALS / "P8_Y5_R10_731_HYBRID_QUOTIENT_CONTRACT.csv",
        "needles": ["HQC731_0_parent_space_split", "HQC731_3_action_factorisation"],
        "role": "hybrid quotient contract",
    },
    "732_doc": {
        "path": POST_CHECKPOINT / "732-Y5-R10-construct-hybrid-pi-observed-quotient-map-or-demote.md",
        "needles": ["hybrid map constructed, exact local silence not derived", "representative-vertical-blind"],
        "role": "hybrid observed quotient map",
    },
    "732_pullback": {
        "path": RESIDUALS / "P8_Y5_R10_732_HYBRID_PULLBACK_LEMMA.csv",
        "needles": ["HPL732_0_pullback_setup", "representative motion cannot directly create"],
        "role": "hybrid pullback lemma",
    },
    "733_doc": {
        "path": POST_CHECKPOINT / "733-Y5-R10-reduced-GK-action-owner-or-hybrid-q_loc-residual-runner.md",
        "needles": ["owner contract written, current symbol match failed", "hybrid `q_loc` is queued"],
        "role": "reduced GK owner failure",
    },
    "733_owner": {
        "path": RESIDUALS / "P8_Y5_R10_733_REDUCED_GK_OWNER_ATTEMPT.csv",
        "needles": ["RGA733_A_hybrid_reduced_scalar_density_owner", "contract_written_not_matched"],
        "role": "reduced GK owner attempt rows",
    },
    "734_doc": {
        "path": POST_CHECKPOINT / "734-Y5-R10-fill-hybrid-q_loc-residual-runner-or-derive-first-zero-row.md",
        "needles": ["one narrow zero row is derivable", "L_{v_X^rep} q_loc^nu = 0"],
        "role": "first hybrid narrow zero",
    },
    "734_zero": {
        "path": RESIDUALS / "P8_Y5_R10_734_FIRST_ZERO_ATTEMPT.csv",
        "needles": ["FZA734_0_representative_vertical_q_loc_variation", "derived_narrow_zero_row_conditional"],
        "role": "first narrow zero attempt rows",
    },
    "735_doc": {
        "path": POST_CHECKPOINT / "735-Y5-R10-source-backed-hybrid-q_loc-residual-inputs-or-second-zero-row.md",
        "needles": ["a second narrow zero row is derivable", "proper representative vertical transformations"],
        "role": "second hybrid narrow zero",
    },
    "735_zero": {
        "path": RESIDUALS / "P8_Y5_R10_735_SECOND_ZERO_ATTEMPT.csv",
        "needles": ["SZA735_0_proper_representative_boundary_charge", "derived_second_narrow_zero_row_conditional"],
        "role": "second narrow zero attempt rows",
    },
    "736_doc": {
        "path": POST_CHECKPOINT / "736-Y5-R10-matter-no-marker-source-normalization-or-third-zero-row.md",
        "needles": ["a third narrow zero row is derivable conditionally", "does **not** prove full `Y5_source_normalization=0`"],
        "role": "third hybrid narrow zero",
    },
    "736_zero": {
        "path": RESIDUALS / "P8_Y5_R10_736_THIRD_ZERO_ATTEMPT.csv",
        "needles": ["TZA736_0_direct_representative_matter_marker", "derived_third_narrow_zero_row_conditional"],
        "role": "third narrow zero attempt rows",
    },
    "737_doc": {
        "path": POST_CHECKPOINT / "737-Y5-R10-source-current-Ward-flux-closure-or-source-backed-Y5-inputs.md",
        "needles": ["Ward bridge is real, but projected source flux is not closed", "d(Pi_M J_H) != proved zero"],
        "role": "source-current Ward flux blocker",
    },
    "738_doc": {
        "path": POST_CHECKPOINT / "738-Y5-R10-PiM-projector-owner-or-radial-bound-runner.md",
        "needles": ["PiM owner fork is sharp, but no current-chain PiM owner is claimed", "readout/fit masks are forbidden"],
        "role": "PiM owner fork blocker",
    },
    "770_curl": {
        "path": RESIDUALS / "P8_Y5_R10_770_INTEGRABILITY_CURL_TEST.csv",
        "needles": ["ICT770_1_curl_identity", "ICT770_5_curl_verdict"],
        "role": "deltaH curl identity from 770",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post_checkpoint(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed_count = 0
    for scanned_path in FORMALIZATION.rglob("*"):
        if scanned_path.is_file() and datetime.fromtimestamp(scanned_path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            changed_count += 1
    return changed_count


def validation_clean(number: int) -> bool:
    path = RESIDUALS / f"P8_Y5_BRR545_{number}_VALIDATION.csv"
    rows = read_csv_rows(path)
    return path.exists() and bool(rows) and all(row.get("result") == "pass" for row in rows)


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(source_spec["path"]),
            "exists": bool_string(Path(source_spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(source_spec["path"]), source_spec["needles"])),
            "role": source_spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, source_spec in SOURCES.items()
    ]


def hybrid_owner_audit_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "HCO772_0_observed_EH_current",
            "hybrid_clause": "observed GR sector uses the EH current",
            "test": "Q_tau^MTS has an EH part Q_EH[g_obs,tau] with fixed boundary/reference",
            "current_result": "conditional_reference_allowed",
            "what_it_prunes": "prevents rebuilding GR charge from scratch where observed EH assumptions hold",
            "what_remains": "EH-only does not own MTS extra, boundary, q_loc/Y5/Y6, or coupling terms",
            "claim_status": "baseline_only_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "HCO772_1_hybrid_split",
            "hybrid_clause": "parent configuration splits into observed quotient plus representative fibre",
            "test": "Y=(O_GR,Phi_red,R_rep,B_ref) and pi_h(Y)=(O_GR,Phi_red,B_ref)",
            "current_result": "formal_map_constructed_not_full_parent_signature",
            "what_it_prunes": "representative variables are not automatically observed local fields",
            "what_remains": "Gamma/Khat/P_loc symbol match, matter descent, boundary/reference and ADM separation remain unsigned",
            "claim_status": "candidate_split_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "HCO772_2_representative_vertical_zero",
            "hybrid_clause": "representative-fibre motion cannot directly source q_loc when all q_loc objects are pullbacks",
            "test": "L_{v_X^rep} q_loc^nu=0 under Gamma/Khat/P_loc pullback premises",
            "current_result": "narrow_zero_imported",
            "what_it_prunes": "direct hidden representative fifth-force source",
            "what_remains": "observed reduced q_loc itself can be nonzero through Phi_red/Euler/boundary/source terms",
            "claim_status": "partial_zero_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "HCO772_3_proper_boundary_zero",
            "hybrid_clause": "proper representative transformations have zero representative boundary charge",
            "test": "Q_X^rep[partial U]=0 for compact-support or boundary-collar-vanishing v_X^rep",
            "current_result": "narrow_zero_imported",
            "what_it_prunes": "pure representative improper edge charge",
            "what_remains": "observed reduced boundary/source-measure flux and non-proper edge modes remain live",
            "claim_status": "partial_zero_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "HCO772_4_matter_marker_zero",
            "hybrid_clause": "ordinary matter/readout has no direct representative marker",
            "test": "delta_{v_X^rep}S_matter=0 if matter functors factor through Q_obs^hybrid",
            "current_result": "narrow_zero_imported_conditional",
            "what_it_prunes": "direct representative matter-marker/source-frame charge",
            "what_remains": "full source normalization, mu_extra, PiM flux closure, Gauss/orbital calibration and PPN stability remain open",
            "claim_status": "partial_zero_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "HCO772_5_reduced_q_loc_owner",
            "hybrid_clause": "Gamma/Khat/P_loc are owned by a reduced GK action on Q_obs^hybrid",
            "test": "S_GK^hyb gives Gamma_eff=gamma, K_hat=metric response, q_loc=P_loc div(T_GK)",
            "current_result": "failed_current_symbol_match",
            "what_it_prunes": "nothing beyond conditional pullback zero",
            "what_remains": "observed q_loc residual, Y5/Y6, PPN tail, boundary flux, and source projection",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "HCO772_6_source_projector_owner",
            "hybrid_clause": "same-frame source current and PiM projector close projected mass flux",
            "test": "d(Pi_M J_H)=0 on compact local exterior",
            "current_result": "blocked_by_737_738",
            "what_it_prunes": "standard matter Ward identity only",
            "what_remains": "projector commutator, exchange flux, boundary/anomaly flux, Hilbert/topological equality",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "HCO772_7_owner_verdict",
            "hybrid_clause": "accept hybrid EH+quotient current owner for FB5540",
            "test": "HCO772_0..HCO772_6 jointly close",
            "current_result": "fail_current_corpus",
            "what_it_prunes": "representative-only ghost channels are pruned",
            "what_remains": "observed reduced boundary/source flux and deltaH curl must be derived or source-filled",
            "claim_status": "nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def narrow_zero_import_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "zero_id": "NZI772_0_representative_q_loc_variation",
            "source_row": "FZA734_0_representative_vertical_q_loc_variation",
            "zero_statement": "L_{v_X^rep} q_loc^nu=0 under hybrid pullback premises",
            "status_after_772": "imported_conditional_zero",
            "legitimate_use": "remove direct representative-fibre source dependence",
            "forbidden_use": "claim observed q_loc^nu=0 or local-GR pass",
            "residual_left": "observed reduced q_loc from Phi_red/Euler/boundary/source terms",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "NZI772_1_proper_representative_boundary",
            "source_row": "SZA735_0_proper_representative_boundary_charge",
            "zero_statement": "Q_X^rep[partial U]=0 for proper representative transformations",
            "status_after_772": "imported_conditional_zero",
            "legitimate_use": "remove pure representative improper boundary charge from the proper gauge domain",
            "forbidden_use": "claim observed boundary/source-measure flux vanishes",
            "residual_left": "observed reduced boundary flux, edge modes, corner flux, ADM/reference split",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "NZI772_2_proper_corner_symplectic",
            "source_row": "SZA735_1_proper_corner_symplectic_flux",
            "zero_statement": "Omega_boundary(delta Y,v_X^rep)=0 for representative support vanishing in boundary collar",
            "status_after_772": "imported_conditional_zero",
            "legitimate_use": "remove proper representative corner symplectic leakage",
            "forbidden_use": "erase non-representative corner/source flux",
            "residual_left": "boundary flux carried by Q_obs^hybrid/Phi_red/matter readout",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "NZI772_3_matter_no_marker",
            "source_row": "TZA736_0_direct_representative_matter_marker",
            "zero_statement": "delta_{v_X^rep}S_matter=0 under strict no-marker one-coframe contract",
            "status_after_772": "imported_conditional_zero",
            "legitimate_use": "remove direct representative matter-marker coupling",
            "forbidden_use": "claim full Y5 source normalization or WEP derivation",
            "residual_left": "dressed source mass, mu_extra, C_qmu q_loc, Gauss calibration, PPN stability",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "NZI772_4_ADM_double_count_guard",
            "source_row": "SZA735_2_ADM_double_count_guard",
            "zero_statement": "ordinary ADM/time/rotation/boost charges remain in Q_obs^hybrid, not in representative vertical domain",
            "status_after_772": "guard_imported_not_full_proof",
            "legitimate_use": "avoid quotienting away physical EH Hamiltonian generators",
            "forbidden_use": "claim PiM/Hilbert/source equality or M_H_ref calibration",
            "residual_left": "Pi_M/Pi_EH projection, M_H_ref, source equality and PG calibration",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def deltaH_curl_decomposition_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "curl_id": "CDC772_0_EH_observed_flux",
            "curl_term": "int_S i_tau omega_EH",
            "hybrid_status": "conditional_GR_baseline",
            "zero_or_bound_condition": "observed local exterior is EH with fixed stationary boundary/reference",
            "current_result": "not_full_MTS_owner_but_allowed_reference_piece",
            "source_fill_if_fails": "deltaH_EH_boundary_flux_over_MH",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "curl_id": "CDC772_1_representative_vertical_flux",
            "curl_term": "Omega_boundary(delta Y,v_X^rep)+Q_X^rep",
            "hybrid_status": "proper_representative_piece_pruned_conditionally",
            "zero_or_bound_condition": "v_X^rep is proper/compact-supported and acts only in representative fibre",
            "current_result": "narrow_zero_only",
            "source_fill_if_fails": "QX_rep_improper_edge_flux_over_MH",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "curl_id": "CDC772_2_observed_reduced_boundary_flux",
            "curl_term": "P_loc B_boundary^nu and reduced observed source flux",
            "hybrid_status": "not_pruned",
            "zero_or_bound_condition": "reduced GK action owner plus on-shell fields plus boundary/source-measure no-flux",
            "current_result": "open_primary_next_target",
            "source_fill_if_fails": "B_observed_reduced_flux_over_MH",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "curl_id": "CDC772_3_Y5_source_projector_flux",
            "curl_term": "d(Pi_M J_H) and source-normalization projection",
            "hybrid_status": "not_pruned",
            "zero_or_bound_condition": "PiM parent owner, zero commutator/exchange/boundary flux, Hilbert/topological equality",
            "current_result": "blocked_by_737_738",
            "source_fill_if_fails": "Y5_projected_source_flux_over_MH",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "curl_id": "CDC772_4_tau_reference_surface",
            "curl_term": "Delta_tau+Delta_S+Delta_ref",
            "hybrid_status": "not_pruned",
            "zero_or_bound_condition": "same observed tau, fixed surface/domain, fixed B_ref before readout",
            "current_result": "still_open_from_770",
            "source_fill_if_fails": "tau_ref_surface_mismatch_over_MH",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "curl_id": "CDC772_5_total_deltaH",
            "curl_term": "delta_H_tau_nonintegrable_over_MH",
            "hybrid_status": "not_zero",
            "zero_or_bound_condition": "CDC772_0..CDC772_4 all theorem-zero or source-backed bounds",
            "current_result": "source_fill_required_if_next_zero_fails",
            "source_fill_if_fails": "DHS771_0_deltaH_curl",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def source_fill_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "fill_id": "HSF772_0_observed_reduced_boundary_flux",
            "quantity": "B_observed_reduced_flux_over_MH",
            "definition": "abs(P_loc B_boundary^nu contribution to curl(deltaH))/M_H_ref",
            "required_columns": "system_id;boundary_shell;P_loc;B_boundary_component;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_OBSERVED_REDUCED_BOUNDARY_FLUX_ZERO_OR_NUMERIC",
            "claim_gate": "theorem-zero or source-backed bound before deltaH pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "HSF772_1_Y5_projected_source_flux",
            "quantity": "Y5_projected_source_flux_over_MH",
            "definition": "abs(integral_A d(Pi_M J_H))/M_H_ref or equivalent projected source-mass flux",
            "required_columns": "system_id;annulus;Pi_M_owner;flux_value;M_H_ref;units;source_path;valid_for_claim",
            "current_status": "MISSING_PIM_PROJECTED_FLUX_ZERO_OR_NUMERIC",
            "claim_gate": "closed projected mass current or source-backed radial/source flux bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "HSF772_2_tau_ref_surface_mismatch",
            "quantity": "tau_ref_surface_mismatch_over_MH",
            "definition": "abs(Delta_tau+Delta_S+Delta_ref)/M_H_ref",
            "required_columns": "tau_id;surface_id;reference_branch;Delta_tau;Delta_S;Delta_ref;M_H_ref;source_path;valid_for_claim",
            "current_status": "MISSING_TAU_REF_SURFACE_ZERO_OR_NUMERIC",
            "claim_gate": "same tau/reference/surface theorem or source-backed mismatch bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "HSF772_3_deltaH_total",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "definition": "sum of nonnegative curl components with no cancellation credit",
            "required_columns": "component_id;value;units;source_path;zero_theorem_or_bound;no_cancellation_flag;valid_for_claim",
            "current_status": "MISSING_COMPONENTS",
            "claim_gate": "every component zero/bounded and no placeholder markers",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D772_0_hybrid_not_promoted",
            "decision": "do not accept the hybrid EH+quotient route as full current owner yet",
            "reason": "it prunes representative-only channels but observed reduced q_loc/source/boundary/tau flux remains open",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D772_1_keep_narrow_zeros",
            "decision": "retain the three narrow zeros as discipline gates",
            "reason": "they remove fake representative channels and stop us from double-counting EH/ADM as representative charge",
            "claim_status": "partial_theorem_support_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D772_2_next_target",
            "decision": "attack observed reduced boundary/source flux next",
            "reason": "that is the first live deltaH curl term not killed by representative quotient silence",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "hybrid EH+quotient route prunes representative-only q_loc, proper boundary charge, and direct matter-marker channels, but it does not kill observed reduced boundary/source flux or deltaH curl",
            "hard_blocker": "observed reduced boundary/source flux and PiM/Y5 projected source flux remain live after all representative narrow zeros are imported",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_claim_rows_false(row_groups: list[list[dict[str, Any]]]) -> bool:
    rows_with_claim_field = [
        row
        for row_group in row_groups
        for row in row_group
        if "valid_for_claim" in row
    ]
    return bool(rows_with_claim_field) and all(str(row["valid_for_claim"]).lower() == "false" for row in rows_with_claim_field)


def validation_rows(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    zeros: list[dict[str, Any]],
    curl: list[dict[str, Any]],
    fills: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_771_clean = all(validation_clean(number) for number in range(665, 772))
    hybrid_audited = any(row["audit_id"] == "HCO772_7_owner_verdict" and row["current_result"] == "fail_current_corpus" for row in audit)
    expected_zero_ids = {
        "NZI772_0_representative_q_loc_variation",
        "NZI772_1_proper_representative_boundary",
        "NZI772_2_proper_corner_symplectic",
        "NZI772_3_matter_no_marker",
        "NZI772_4_ADM_double_count_guard",
    }
    narrow_zeros_imported = expected_zero_ids.issubset({row["zero_id"] for row in zeros})
    curl_decomposed = any(row["curl_id"] == "CDC772_5_total_deltaH" and row["current_result"] == "source_fill_required_if_next_zero_fails" for row in curl)
    fallback_staged = len(fills) >= 4 and all("MISSING_" in row["current_status"] for row in fills)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D772_2_next_target" for row in decisions)
    candidate_artifacts_not_faked = all(not path.exists() for path in CANDIDATE_ARTIFACTS)
    all_nonclaim = all_claim_rows_false([sources, audit, zeros, curl, fills, decisions, summary])
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V772_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V772_1_source_needles_present", source_needles_present, "all local source needles present"),
        ("V772_2_prior_665_771_clean", prior_665_771_clean, "665-771 validation rows have no failures"),
        ("V772_3_hybrid_owner_audited", hybrid_audited, "hybrid owner audit recorded fail_current_corpus"),
        ("V772_4_narrow_zeros_imported", narrow_zeros_imported, "representative narrow zeros and ADM guard imported"),
        ("V772_5_deltaH_curl_decomposed", curl_decomposed, "deltaH curl live terms decomposed"),
        ("V772_6_fallback_source_rows_staged", fallback_staged, "source-fill fallback rows staged with missing markers"),
        ("V772_7_candidate_artifacts_not_faked", candidate_artifacts_not_faked, "no claim-input artifacts fabricated"),
        ("V772_8_no_claim_rows_promoted", all_nonclaim, "all generated rows valid_for_claim=false"),
        ("V772_9_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V772_10_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V772_11_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V772_12_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    zeros: list[dict[str, Any]],
    curl: list[dict[str, Any]],
    fills: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 772 - Y5 R10 Hybrid EH Quotient Current Owner Or deltaH Curl Source Fill

Start point: 771 selected the hybrid EH-plus-quotient-extra route as the least-cheaty current-owner attempt: keep the real EH current for observed GR, and force MTS extra local directions to be quotient-silent, exact/proper, or residualized.

Current result: **the hybrid route is useful but not yet a full current owner**. It imports three real narrow zeros: representative-fibre motion does not directly source `q_loc`, proper representative boundary charge vanishes, and direct representative matter-marker charge vanishes under the no-marker one-coframe contract. Those prune ghost channels. They do **not** kill observed reduced `q_loc`, observed boundary/source flux, Y5/PiM projected source flux, tau/reference/surface terms, or the total `delta_H_tau` curl.

## Status

| field | value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | {summary[0]["main_result"]} |
| Hard blocker | `{summary[0]["hard_blocker"]}` |
| Next target | `{NEXT_TARGET}` |

## Hybrid Current Owner Audit

{markdown_table(audit, ["audit_id", "hybrid_clause", "test", "current_result", "what_it_prunes", "what_remains", "claim_status", "valid_for_claim"])}

## Narrow Zero Import Ledger

{markdown_table(zeros, ["zero_id", "source_row", "zero_statement", "status_after_772", "legitimate_use", "forbidden_use", "residual_left", "valid_for_claim"])}

## deltaH Curl Decomposition

{markdown_table(curl, ["curl_id", "curl_term", "hybrid_status", "zero_or_bound_condition", "current_result", "source_fill_if_fails", "valid_for_claim"])}

## deltaH Curl Source Fill Fallback

{markdown_table(fills, ["fill_id", "quantity", "definition", "required_columns", "current_status", "claim_gate", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

The hybrid branch earns a small but real win: representative ghost motion is not the local-GR killer. The surviving problem is physical/observed, not notational. The next derivation target is the observed reduced boundary/source flux term in the `delta_H_tau` curl. If that cannot be killed by a reduced Ward/boundary theorem, it must be filled as a source-backed component row.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    audit = hybrid_owner_audit_rows(generated_utc)
    zeros = narrow_zero_import_rows(generated_utc)
    curl = deltaH_curl_decomposition_rows(generated_utc)
    fills = source_fill_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, audit, zeros, curl, fills, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(HYBRID_OWNER_AUDIT_PATH, audit, ["audit_id", "hybrid_clause", "test", "current_result", "what_it_prunes", "what_remains", "claim_status", "valid_for_claim", "generated_utc"])
    write_csv(NARROW_ZERO_IMPORT_PATH, zeros, ["zero_id", "source_row", "zero_statement", "status_after_772", "legitimate_use", "forbidden_use", "residual_left", "valid_for_claim", "generated_utc"])
    write_csv(DELTAH_CURL_DECOMPOSITION_PATH, curl, ["curl_id", "curl_term", "hybrid_status", "zero_or_bound_condition", "current_result", "source_fill_if_fails", "valid_for_claim", "generated_utc"])
    write_csv(SOURCE_FILL_FALLBACK_PATH, fills, ["fill_id", "quantity", "definition", "required_columns", "current_status", "claim_gate", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_MATRIX_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, audit, zeros, curl, fills, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"772 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
