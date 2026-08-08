from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "773-Y5-R10-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md"
NEXT_TARGET = "774-Y5-R10-reduced-GK-symbol-match-or-observed-boundary-flux-input-runner.md"
STATUS = "Y5_R10_773_observed_reduced_boundary_flux_zero_contract_written_current_MTS_fails_component_fill_staged_nonclaim"
CLAIM_CEILING = "observed_reduced_flux_Ward_zero_contract_only_no_deltaH_zero_no_HPiM_integrability_no_Newton_no_PPN_no_R10_R11_or_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_773_SOURCE_REGISTER.csv"
ZERO_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_773_OBSERVED_FLUX_ZERO_ATTEMPT.csv"
CLAUSE_GATE_PATH = RESIDUALS / "P8_Y5_R10_773_OBSERVED_FLUX_ZERO_CLAUSE_GATE.csv"
COMPONENT_SPLIT_PATH = RESIDUALS / "P8_Y5_R10_773_OBSERVED_FLUX_COMPONENT_SPLIT.csv"
CURL_COMPONENT_FILL_PATH = RESIDUALS / "P8_Y5_R10_773_DELTAH_CURL_COMPONENT_FILL.csv"
DECISION_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_773_DECISION_MATRIX.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_773_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_773_VALIDATION.csv"

CANDIDATE_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_773_OBSERVED_REDUCED_BOUNDARY_FLUX_ZERO_CLAIM.csv",
    RESIDUALS / "P8_Y5_R10_773_DELTAH_CURL_PASS_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_773_LOCAL_GR_REENTRY_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    ZERO_ATTEMPT_PATH,
    CLAUSE_GATE_PATH,
    COMPONENT_SPLIT_PATH,
    CURL_COMPONENT_FILL_PATH,
    DECISION_MATRIX_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCES: dict[str, dict[str, Any]] = {
    "772_doc": {
        "path": POST_CHECKPOINT / "772-Y5-R10-hybrid-EH-quotient-current-owner-or-deltaH-curl-source-fill.md",
        "needles": ["CDC772_2_observed_reduced_boundary_flux", "observed reduced boundary/source flux"],
        "role": "immediate handoff: observed reduced flux is primary next target",
    },
    "772_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_772_VALIDATION.csv",
        "needles": ["V772_5_deltaH_curl_decomposed", "pass"],
        "role": "prior validation guard",
    },
    "772_curl": {
        "path": RESIDUALS / "P8_Y5_R10_772_DELTAH_CURL_DECOMPOSITION.csv",
        "needles": ["CDC772_2_observed_reduced_boundary_flux", "open_primary_next_target"],
        "role": "deltaH curl component source",
    },
    "772_fill": {
        "path": RESIDUALS / "P8_Y5_R10_772_DELTAH_CURL_SOURCE_FILL_FALLBACK.csv",
        "needles": ["HSF772_0_observed_reduced_boundary_flux", "MISSING_OBSERVED_REDUCED_BOUNDARY_FLUX_ZERO_OR_NUMERIC"],
        "role": "fallback row requiring observed flux zero or numeric source",
    },
    "733_doc": {
        "path": POST_CHECKPOINT / "733-Y5-R10-reduced-GK-action-owner-or-hybrid-q_loc-residual-runner.md",
        "needles": [
            "Current verdict: **owner contract written, current symbol match failed**",
            "Diffeomorphism invariance of the reduced action controls divergence of T_GK.",
        ],
        "role": "reduced Ward/no-flux theorem source",
    },
    "733_metric_response": {
        "path": RESIDUALS / "P8_Y5_R10_733_METRIC_RESPONSE_DERIVATION.csv",
        "needles": ["MRD733_3_reduced_Ward_identity", "nabla_mu T_GK"],
        "role": "formal reduced Ward identity ledger",
    },
    "733_ward_gate": {
        "path": RESIDUALS / "P8_Y5_R10_733_WARD_ZERO_GATE.csv",
        "needles": ["WZG733_0_current_symbol_match", "WZG733_4_boundary_no_flux"],
        "role": "failed current-corpus zero clauses",
    },
    "734_residual_formula": {
        "path": RESIDUALS / "P8_Y5_R10_734_RESIDUAL_FORMULA_LEDGER.csv",
        "needles": ["RFL734_0_reduced_Ward_shape", "q_loc^nu = P_loc"],
        "role": "observed reduced residual formula",
    },
    "735_second_zero": {
        "path": RESIDUALS / "P8_Y5_R10_735_SECOND_ZERO_ATTEMPT.csv",
        "needles": ["SZA735_3_observed_boundary_flux", "not_derived_for_current_claim"],
        "role": "proper representative boundary zero does not kill observed boundary flux",
    },
    "737_doc": {
        "path": POST_CHECKPOINT / "737-Y5-R10-source-current-Ward-flux-closure-or-source-backed-Y5-inputs.md",
        "needles": ["Current verdict: **the Ward bridge is real, but projected source flux is not closed**", "d(Pi_M J_H) != proved zero"],
        "role": "source-measure/projected flux obstruction source",
    },
    "737_ward_flux": {
        "path": RESIDUALS / "P8_Y5_R10_737_SOURCE_CURRENT_WARD_FLUX_ATTEMPT.csv",
        "needles": ["WFA737_2_projected_mass_flux_target", "not_derived_for_current_claim"],
        "role": "projected mass flux product-rule obstruction",
    },
    "737_obstruction": {
        "path": RESIDUALS / "P8_Y5_R10_737_PROJECTED_MASS_FLUX_OBSTRUCTION.csv",
        "needles": ["PMF737_4_boundary_improvement_flux", "open"],
        "role": "boundary/source-measure projected-flux obstruction",
    },
    "738_doc": {
        "path": POST_CHECKPOINT / "738-Y5-R10-PiM-projector-owner-or-radial-bound-runner.md",
        "needles": ["The topological absolute-mass route is the cleanest conditional option", "Hodge/DeWitt routes keep projector stress"],
        "role": "PiM/projector route status",
    },
    "738_commutator": {
        "path": RESIDUALS / "P8_Y5_R10_738_PIM_COMMUTATOR_GATE.csv",
        "needles": ["PCG738_0_product_rule_retained", "active_obstruction"],
        "role": "projector commutator gate",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


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


def zero_attempt_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "OFZ773_0_reduced_Ward_identity",
            "target": "observed reduced boundary/source flux",
            "identity": "q_loc^nu = P_loc nabla_mu T_GK^{mu nu} = P_loc(sum_A E_A nabla^nu Phi_A + B_obs^nu)",
            "required_clauses": "reduced action ownership; metric response K_hat; parent-owned P_loc; on-shell reduced fields; fixed boundary/reference; no source-measure leakage",
            "derivation_status": "conditional_identity_available",
            "current_mts_verdict": "not_a_zero_by_itself",
            "residual_left": "E_A, B_obs, source-measure, corner/edge, and projector terms can survive",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "OFZ773_1_compact_exterior_no_flux_theorem_contract",
            "target": "B_observed_reduced_flux_over_MH",
            "identity": "If S_red is parent-owned/diffeomorphism invariant, E_A=0, P_loc descends, and all observed boundary/source-measure flux is exact/proper/fixed-reference, then P_loc B_obs^nu=0 on the compact local exterior.",
            "required_clauses": "OFC773_0 through OFC773_6 all pass together",
            "derivation_status": "conditional_theorem_contract_written",
            "current_mts_verdict": "premises_unsigned_for_current_claim",
            "residual_left": "this is a theorem route, not a current local-GR result",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "OFZ773_2_boundary_source_flux_zero_attempt",
            "target": "P_loc B_boundary^nu plus reduced observed source flux",
            "identity": "B_obs^nu := B_GK^nu + B_corner^nu + B_source_measure^nu + B_projector^nu",
            "required_clauses": "boundary collar silence; no improper observed edge modes; same-frame source measure; no post-readout projector; no hidden ADM subtraction",
            "derivation_status": "failed_current_corpus",
            "current_mts_verdict": "observed boundary/source flux remains live",
            "residual_left": "component fill rows required unless 774 closes reduced owner/symbol match",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "OFZ773_3_current_MTS_verdict",
            "target": "promote observed reduced flux zero",
            "identity": "CDC772_2_observed_reduced_boundary_flux -> theorem zero",
            "required_clauses": "all observed reduced flux clauses close plus Y5/PiM source flux stays separate",
            "derivation_status": "fail_current_corpus",
            "current_mts_verdict": "do_not_promote",
            "residual_left": "B_observed_reduced_flux_over_MH remains a live deltaH curl component",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "OFZ773_4_no_smuggling_gate",
            "target": "boundary condition discipline",
            "identity": "A proper representative boundary zero cannot be reused as an observed reduced no-flux condition.",
            "required_clauses": "boundary condition must be parent/domain/theorem signed, not imposed after readout to erase physical flux",
            "derivation_status": "discipline_gate_passed",
            "current_mts_verdict": "no_cheat_guard_retained",
            "residual_left": "observed reduced flux still needs owner theorem or source-backed bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def clause_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "OFC773_0_reduced_action_owner",
            "clause": "S_red or S_GK^hyb is a parent-owned functional on Q_obs^hybrid before readout.",
            "needed_for": "make T_GK and B_obs variational objects rather than fitted residual names",
            "source_status": "contract_written_symbol_match_failed_in_733",
            "failure_mode_if_missing": "Ward identity cannot be applied to current Gamma_eff/K_hat/P_loc as a theorem",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "OFC773_1_Gamma_Khat_metric_response",
            "clause": "Gamma_eff=gamma and K_hat=K_gamma from the same reduced action variation.",
            "needed_for": "turn q_loc into the divergence of a parent-owned stress response",
            "source_status": "WZG733_0_fail_for_current_claim",
            "failure_mode_if_missing": "B_obs may be an independent stress/current leak",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "OFC773_2_on_shell_reduced_fields",
            "clause": "All reduced local-vacuum fields satisfy E_A=0 in the compact exterior annulus.",
            "needed_for": "remove bulk Euler flux P_loc sum_A E_A nabla Phi_A",
            "source_status": "WZG733_1_not_derived",
            "failure_mode_if_missing": "local residual can be real source-free hair rather than boundary-only leakage",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "OFC773_3_boundary_reference_no_flux",
            "clause": "Observed boundary/corner/reference terms are fixed, exact, proper, or cancel by a parent theorem.",
            "needed_for": "kill B_GK^nu, corner symplectic flux, and finite improvement flux",
            "source_status": "WZG733_4_open_and_SZA735_only_representative",
            "failure_mode_if_missing": "a total divergence can still carry finite compact-boundary mass/Hamiltonian flux",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "OFC773_4_source_measure_silence",
            "clause": "Matter/source measure and coupling descend through the same observed geometry with no hidden source marker.",
            "needed_for": "prevent B_source_measure^nu and C_qmu q_loc from entering measured GM/source strength",
            "source_status": "direct_marker_pruned_but_dressed_source_flux_open_in_737",
            "failure_mode_if_missing": "same-frame stress Ward conservation is not projected source-mass closure",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "OFC773_5_projector_descent",
            "clause": "P_loc and any Pi_M/source projection are parent-owned and commute with the exterior derivative on the allowed domain.",
            "needed_for": "avoid [d,P] and [d,Pi_M] leakage after an otherwise good Ward identity",
            "source_status": "PCG738_0_active_obstruction",
            "failure_mode_if_missing": "projector product-rule terms mimic radial/time source hair",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "OFC773_6_tau_surface_reference_lock",
            "clause": "The same tau, surface class, and reference branch are fixed before variation and readout.",
            "needed_for": "separate observed flux from tau/reference/surface mismatch in delta_H_tau",
            "source_status": "still_open_from_770_772",
            "failure_mode_if_missing": "flux zero can be counterterm or surface-choice artefact",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def component_split_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "component_id": "OFS773_0_bulk_Euler_flux",
            "component": "P_loc sum_A E_A nabla^nu Phi_A",
            "zero_condition": "OFC773_2_on_shell_reduced_fields",
            "current_result": "not_zero_current_corpus",
            "maps_to": "B_obs_bulk_Euler_over_MH",
            "why_not_killed_by_772": "representative pullback silence does not solve observed reduced Euler equations",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "OFS773_1_boundary_improvement_flux",
            "component": "P_loc B_GK^nu from integrations by parts, improvements, and reference subtraction",
            "zero_condition": "OFC773_3_boundary_reference_no_flux",
            "current_result": "not_zero_current_corpus",
            "maps_to": "B_obs_boundary_improvement_over_MH",
            "why_not_killed_by_772": "proper representative boundary zero does not erase observed boundary/reference terms",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "OFS773_2_source_measure_flux",
            "component": "P_loc B_source_measure^nu and C_qmu q_loc source-strength projection",
            "zero_condition": "OFC773_4_source_measure_silence",
            "current_result": "not_zero_current_corpus",
            "maps_to": "B_obs_source_measure_over_MH",
            "why_not_killed_by_772": "direct representative marker zero does not close dressed Hilbert/source flux",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "OFS773_3_corner_edge_mode_flux",
            "component": "non-proper observed corner/edge mode flux",
            "zero_condition": "OFC773_3_boundary_reference_no_flux plus no improper observed edge modes",
            "current_result": "not_zero_current_corpus",
            "maps_to": "B_obs_corner_edge_over_MH",
            "why_not_killed_by_772": "772 imports only proper representative edge silence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "OFS773_4_projector_commutator_flux",
            "component": "[d,P_loc]J_red or [d,Pi_M]J_H leakage in projected source channel",
            "zero_condition": "OFC773_5_projector_descent",
            "current_result": "not_zero_current_corpus",
            "maps_to": "B_obs_projector_commutator_over_MH",
            "why_not_killed_by_772": "hybrid quotient silence does not prove projector commutators vanish",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "OFS773_5_total_observed_reduced_flux",
            "component": "B_observed_reduced_flux_over_MH",
            "zero_condition": "OFS773_0 through OFS773_4 all theorem-zero or source-backed below gate",
            "current_result": "source_fill_required_if_774_fails",
            "maps_to": "HSF772_0_observed_reduced_boundary_flux",
            "why_not_killed_by_772": "772 only pruned representative channels, not observed/reduced flux",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def curl_component_fill_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "fill_id": "BCF773_0_bulk_Euler_flux",
            "quantity": "B_obs_bulk_Euler_over_MH",
            "definition": "abs(P_loc sum_A E_A nabla^nu Phi_A contribution to curl(deltaH))/M_H_ref",
            "required_columns": "system_id;annulus;field_A;E_A;nabla_Phi_A;P_loc_component;M_H_ref;units;source_path;valid_for_claim",
            "current_status": "MISSING_REDUCED_EULER_ZERO_OR_NUMERIC",
            "claim_gate": "on-shell reduced-field theorem or source-backed compact-exterior bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "BCF773_1_boundary_improvement_flux",
            "quantity": "B_obs_boundary_improvement_over_MH",
            "definition": "abs(P_loc B_GK^nu plus reference/improvement contribution to curl(deltaH))/M_H_ref",
            "required_columns": "system_id;surface_id;boundary_class;B_GK_component;B_ref_component;P_loc_component;M_H_ref;units;source_path;valid_for_claim",
            "current_status": "MISSING_BOUNDARY_REFERENCE_NO_FLUX_OR_NUMERIC",
            "claim_gate": "fixed-reference no-flux theorem or explicit finite-boundary flux bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "BCF773_2_source_measure_flux",
            "quantity": "B_obs_source_measure_over_MH",
            "definition": "abs(P_loc B_source_measure^nu or C_qmu q_loc projected source-strength term)/M_H_ref",
            "required_columns": "system_id;source_channel;coupling_descent_status;C_qmu;flux_value;M_H_ref;units;source_path;valid_for_claim",
            "current_status": "MISSING_SOURCE_MEASURE_SILENCE_OR_NUMERIC",
            "claim_gate": "same-frame source measure/no-marker theorem plus PiM closure or source-backed coefficient",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "BCF773_3_corner_edge_flux",
            "quantity": "B_obs_corner_edge_over_MH",
            "definition": "abs(non-proper observed edge/corner symplectic flux contribution)/M_H_ref",
            "required_columns": "system_id;corner_id;edge_mode_class;flux_value;proper_or_improper;M_H_ref;units;source_path;valid_for_claim",
            "current_status": "MISSING_OBSERVED_EDGE_MODE_ZERO_OR_NUMERIC",
            "claim_gate": "observed edge mode theorem or source-backed corner flux bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "BCF773_4_projector_commutator_flux",
            "quantity": "B_obs_projector_commutator_over_MH",
            "definition": "abs(integral_A [d,P_loc]J_red or [d,Pi_M]J_H contribution)/M_H_ref",
            "required_columns": "system_id;projector_id;commutator_value;domain_dependence;M_H_ref;units;source_path;valid_for_claim",
            "current_status": "MISSING_PROJECTOR_DESCENT_ZERO_OR_NUMERIC",
            "claim_gate": "parent-owned topological/projector descent theorem or finite commutator bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "BCF773_5_total_B_observed",
            "quantity": "B_observed_reduced_flux_over_MH",
            "definition": "sum of nonnegative observed reduced flux components with no cancellation credit",
            "required_columns": "component_id;value;units;source_path;zero_theorem_or_bound;no_cancellation_flag;valid_for_claim",
            "current_status": "MISSING_COMPONENTS",
            "claim_gate": "all BCF773 component rows zero/bounded with no placeholders",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D773_0_conditional_theorem_retained",
            "decision": "retain the compact-exterior reduced Ward no-flux theorem as a contract",
            "reason": "it is the cleanest derivation route if reduced action ownership and boundary/source clauses are later signed",
            "claim_status": "contract_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D773_1_zero_not_promoted",
            "decision": "do not promote observed reduced boundary/source flux to zero for current MTS",
            "reason": "Gamma/Khat/P_loc ownership, on-shell reduced fields, boundary/reference no-flux, source-measure silence, and projector descent are not jointly proved",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D773_2_component_fill_staged",
            "decision": "stage B_observed_reduced_flux_over_MH as decomposed deltaH curl component rows",
            "reason": "if the next reduced-symbol attempt fails, the component must be bounded rather than hidden",
            "claim_status": "source_fill_ready_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D773_3_next_target",
            "decision": "attack reduced GK symbol match before running numeric B_obs inputs",
            "reason": "derivation-first remains best: if Gamma_eff/K_hat/P_loc become owned, the no-flux theorem has a real spine",
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
            "main_result": "the observed reduced no-flux theorem is written as a precise conditional contract, but current MTS does not satisfy the clauses needed to set B_observed_reduced_flux_over_MH to zero",
            "hard_blocker": "Gamma_eff/K_hat/P_loc reduced-action ownership, reduced Euler equations, boundary/reference no-flux, source-measure silence, projector descent, and tau/surface/reference lock are not jointly signed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_rows(*row_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in row_groups:
        rows.extend(group)
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    zero_attempt: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    components: list[dict[str, Any]],
    fills: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    expected_clause_ids = {
        "OFC773_0_reduced_action_owner",
        "OFC773_1_Gamma_Khat_metric_response",
        "OFC773_2_on_shell_reduced_fields",
        "OFC773_3_boundary_reference_no_flux",
        "OFC773_4_source_measure_silence",
        "OFC773_5_projector_descent",
        "OFC773_6_tau_surface_reference_lock",
    }
    expected_component_ids = {
        "OFS773_0_bulk_Euler_flux",
        "OFS773_1_boundary_improvement_flux",
        "OFS773_2_source_measure_flux",
        "OFS773_3_corner_edge_mode_flux",
        "OFS773_4_projector_commutator_flux",
        "OFS773_5_total_observed_reduced_flux",
    }

    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_772_clean = all(validation_clean(number) for number in range(665, 773))
    theorem_contract_written = any(
        row["attempt_id"] == "OFZ773_1_compact_exterior_no_flux_theorem_contract"
        and row["derivation_status"] == "conditional_theorem_contract_written"
        for row in zero_attempt
    )
    current_verdict_fail = any(
        row["attempt_id"] == "OFZ773_3_current_MTS_verdict"
        and row["derivation_status"] == "fail_current_corpus"
        for row in zero_attempt
    )
    clauses_complete = expected_clause_ids.issubset({row["clause_id"] for row in clauses})
    components_complete = expected_component_ids.issubset({row["component_id"] for row in components})
    fallback_staged = len(fills) >= 6 and all("MISSING" in row["current_status"] for row in fills)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, zero_attempt, clauses, components, fills, decisions, summary)
    )
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D773_3_next_target" for row in decisions)
    candidate_artifacts_not_faked = all(not path.exists() for path in CANDIDATE_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V773_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V773_1_source_needles_present", source_needles_present, "all local source needles present"),
        ("V773_2_prior_665_772_clean", prior_665_772_clean, "665-772 validation rows have no failures"),
        ("V773_3_conditional_theorem_contract_written", theorem_contract_written, "observed reduced Ward/no-flux contract written"),
        ("V773_4_current_zero_not_promoted", current_verdict_fail, "current MTS verdict is fail_current_corpus"),
        ("V773_5_clause_gate_complete", clauses_complete, "all observed flux zero clauses enumerated"),
        ("V773_6_component_split_complete", components_complete, "all observed flux components split"),
        ("V773_7_fallback_source_rows_staged", fallback_staged, "deltaH curl component fill rows staged with missing markers"),
        ("V773_8_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V773_9_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V773_10_candidate_artifacts_not_faked", candidate_artifacts_not_faked, "no local-GR/deltaH pass artifacts fabricated"),
        ("V773_11_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V773_12_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V773_13_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    zero_attempt: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    components: list[dict[str, Any]],
    fills: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 773 - Y5 R10 Observed Reduced Boundary Source Flux Zero Or deltaH Curl Component Fill

Current result: **the reduced Ward/no-flux path is mathematically clean but not yet owned by current MTS**. If `S_red` is parent-owned on `Q_obs^hybrid`, `Gamma_eff/K_hat/P_loc` are the reduced variational objects, the compact exterior is on shell, and all observed boundary/source/projector terms are fixed/exact/silent, then the observed reduced flux component can vanish. The current corpus does **not** satisfy those clauses, so `B_observed_reduced_flux_over_MH` remains a live `delta_H_tau` curl component.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Observed Flux Zero Attempt

{markdown_table(zero_attempt, ["attempt_id", "target", "identity", "required_clauses", "derivation_status", "current_mts_verdict", "residual_left", "valid_for_claim"])}

## Clause Gate

{markdown_table(clauses, ["clause_id", "clause", "needed_for", "source_status", "failure_mode_if_missing", "claim_status", "valid_for_claim"])}

## Observed Flux Component Split

{markdown_table(components, ["component_id", "component", "zero_condition", "current_result", "maps_to", "why_not_killed_by_772", "valid_for_claim"])}

## deltaH Curl Component Fill

{markdown_table(fills, ["fill_id", "quantity", "definition", "required_columns", "current_status", "claim_gate", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is a useful narrowing, not a grim one. The observed flux is not some vague monster now: it has five named teeth — bulk Euler, boundary/reference improvement, source-measure coupling, corner/edge mode, and projector commutator. The best derivation-first move is therefore to attack the reduced `Gamma_eff/K_hat/P_loc` ownership/symbol match. If that closes, the Ward no-flux route becomes a real theorem candidate. If it does not, the `B_obs` component rows are already staged for source-backed bounds.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    zero_attempt = zero_attempt_rows(generated_utc)
    clauses = clause_gate_rows(generated_utc)
    components = component_split_rows(generated_utc)
    fills = curl_component_fill_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, zero_attempt, clauses, components, fills, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(ZERO_ATTEMPT_PATH, zero_attempt, ["attempt_id", "target", "identity", "required_clauses", "derivation_status", "current_mts_verdict", "residual_left", "valid_for_claim", "generated_utc"])
    write_csv(CLAUSE_GATE_PATH, clauses, ["clause_id", "clause", "needed_for", "source_status", "failure_mode_if_missing", "claim_status", "valid_for_claim", "generated_utc"])
    write_csv(COMPONENT_SPLIT_PATH, components, ["component_id", "component", "zero_condition", "current_result", "maps_to", "why_not_killed_by_772", "valid_for_claim", "generated_utc"])
    write_csv(CURL_COMPONENT_FILL_PATH, fills, ["fill_id", "quantity", "definition", "required_columns", "current_status", "claim_gate", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_MATRIX_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, zero_attempt, clauses, components, fills, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"773 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
