from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "775-Y5-R10-observed-boundary-flux-source-acquisition-or-response-displacement-owner.md"
NEXT_TARGET = "776-Y5-R10-response-displacement-action-variation-ledger-or-Bobs-first-source-pack.md"
STATUS = "Y5_R10_775_response_displacement_owner_attempted_not_parent_signed_Bobs_source_acquisition_ledger_opened_nonclaim"
CLAIM_CEILING = "response_displacement_owner_attempt_and_Bobs_source_acquisition_only_no_Bobs_zero_no_deltaH_zero_no_Newton_PPN_R10_R11_or_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_775_SOURCE_REGISTER.csv"
OWNER_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_775_RESPONSE_DISPLACEMENT_OWNER_ATTEMPT.csv"
BOBS_SOURCE_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_775_BOBS_SOURCE_ACQUISITION_LEDGER.csv"
CLAIM_READINESS_PATH = RESIDUALS / "P8_Y5_R10_775_BOBS_CLAIM_READINESS_GATE.csv"
EXIT_CRITERIA_PATH = RESIDUALS / "P8_Y5_R10_775_EXIT_CRITERIA.csv"
DECISION_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_775_DECISION_MATRIX.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_775_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_775_VALIDATION.csv"

CANDIDATE_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_775_RESPONSE_DISPLACEMENT_OWNER_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_775_BOBS_BULK_EULER_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_775_BOBS_BOUNDARY_IMPROVEMENT_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_775_BOBS_SOURCE_MEASURE_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_775_BOBS_CORNER_EDGE_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_775_BOBS_PROJECTOR_COMMUTATOR_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_775_OBSERVED_FLUX_ZERO_CLAIM.csv",
    RESIDUALS / "P8_Y5_R10_775_LOCAL_GR_REENTRY_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    OWNER_ATTEMPT_PATH,
    BOBS_SOURCE_LEDGER_PATH,
    CLAIM_READINESS_PATH,
    EXIT_CRITERIA_PATH,
    DECISION_MATRIX_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCES: dict[str, dict[str, Any]] = {
    "774_doc": {
        "path": POST_CHECKPOINT / "774-Y5-R10-reduced-GK-symbol-match-or-observed-boundary-flux-input-runner.md",
        "needles": ["RDR774_0_parent_response_field", "BIR774_5_total_Bobs"],
        "role": "immediate 775 handoff: response-displacement or B_obs source acquisition",
    },
    "774_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_774_VALIDATION.csv",
        "needles": ["V774_6_Bobs_runner_schema_complete", "pass"],
        "role": "prior validation guard",
    },
    "774_runner": {
        "path": RESIDUALS / "P8_Y5_R10_774_BOBS_INPUT_RUNNER_SCHEMA.csv",
        "needles": ["BIR774_0_bulk_Euler_flux", "BIR774_5_total_Bobs"],
        "role": "B_obs component runner schema",
    },
    "774_repair": {
        "path": RESIDUALS / "P8_Y5_R10_774_RESPONSE_DISPLACEMENT_REPAIR_CONTRACT.csv",
        "needles": ["RDR774_0_parent_response_field", "RDR774_3_projector_descent"],
        "role": "response-displacement repair contract",
    },
    "758_doc": {
        "path": POST_CHECKPOINT / "758-Y5-R10-full-residual-vector-parent-action-contract-or-component-input-acquisition.md",
        "needles": ["the stronger parent-action contract can be written, but it is not yet parent-signed", "PAC758_3_universal_coupling_owner"],
        "role": "full residual-vector parent action contract",
    },
    "758_contract": {
        "path": RESIDUALS / "P8_Y5_R10_758_PARENT_ACTION_CONTRACT_ATTEMPT.csv",
        "needles": ["PAC758_0_action_skeleton", "PAC758_3_universal_coupling_owner"],
        "role": "parent action and universal coupling clauses",
    },
    "758_lock_gate": {
        "path": RESIDUALS / "P8_Y5_R10_758_FULL_RESIDUAL_VECTOR_LOCK_GATE.csv",
        "needles": ["FLG758_4_boundary", "FLG758_5_coupling"],
        "role": "boundary/coupling residual-vector lock gates",
    },
    "758_acquisition": {
        "path": RESIDUALS / "P8_Y5_R10_758_COMPONENT_INPUT_ACQUISITION_LEDGER.csv",
        "needles": ["AIL758_0_q_loc_components", "AIL758_5_coupling_descent"],
        "role": "component/residual acquisition precedent",
    },
    "759_coupling_audit": {
        "path": RESIDUALS / "P8_Y5_R10_759_COUPLING_OWNER_ACTION_AUDIT.csv",
        "needles": ["COA759_0_single_observed_geometry", "COA759_6_verdict"],
        "role": "coupling owner action audit",
    },
    "759_coupling_runner": {
        "path": RESIDUALS / "P8_Y5_R10_759_COUPLING_RESIDUAL_ACQUISITION_RUNNER.csv",
        "needles": ["CAR759_0_coupling_descent_input", "CAR759_5_PPN_coupling_response"],
        "role": "coupling residual acquisition runner",
    },
    "759_impact": {
        "path": RESIDUALS / "P8_Y5_R10_759_RESIDUAL_VECTOR_IMPACT_MATRIX.csv",
        "needles": ["IM759_2_alpha3_q_loc", "IM759_4_local_GR"],
        "role": "coupling impact on local residual vector",
    },
    "517_doc": {
        "path": POST_CHECKPOINT / "517-response-doublet-action-variation-ledger-or-run-q_loc-bound.md",
        "needles": ["AV517_2_first_variation_Z", "MR517_3_boundary_terms"],
        "role": "response-doublet variation and boundary-source work blocker",
    },
    "757_doc": {
        "path": POST_CHECKPOINT / "757-Y5-R10-response-doublet-physical-lock-or-real-q_loc-component-input.md",
        "needles": ["physical_lock_not_proved", "real q_loc^nu field/profile or theorem-zero certificate"],
        "role": "formal auxiliary doublet not enough for observed residuals",
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


def owner_attempt_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "owner_id": "RDO775_0_response_displacement_ansatz",
            "owner_clause": "Introduce parent response/displacement fields R^A on Q_obs^hybrid before local readout.",
            "mathematical_form": "S_R = 1/2 int sqrt(-g_obs) R^A G_AB(g_obs,U) R^B + boundary/reference terms",
            "would_close": "Gamma_eff can be gamma=1/2 R G R and K_hat can be its metric response if all fields/units/domain data are parent-owned.",
            "current_result": "ansatz_written_not_parent_signed",
            "missing_for_claim": "explicit R^A definitions, units, source paths, relation to current Gamma_eff/K_hat/P_loc",
            "fallback": "B_obs component source acquisition",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "RDO775_1_metric_response_conjugacy",
            "owner_clause": "K_hat must equal the metric response K_gamma of the response action.",
            "mathematical_form": "K_hat^{mu nu}=2/sqrt(-g_obs) delta[sqrt(-g_obs) gamma]/delta g_obs_{mu nu}, including derivative/domain/boundary terms",
            "would_close": "T_GK becomes a true reduced Hilbert stress instead of a bookkeeping tensor.",
            "current_result": "not_derived_current_corpus",
            "missing_for_claim": "tensor slot comparison Khat-K_gamma and Helmholtz/integrability ledger",
            "fallback": "Khat_unmatched and boundary-improvement B_obs rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "RDO775_2_physical_residual_lock",
            "owner_clause": "R^A must be full-rank locked to the measured residual vector, not only auxiliary exchange shadows.",
            "mathematical_form": "c_- ||R_phys||^2 <= R^A G_AB R^B <= c_+ ||R_phys||^2 for q_loc,Y5,Y6,PPN,boundary,coupling channels",
            "would_close": "response fixed point would force observed residual silence rather than only an internal double-zero.",
            "current_result": "not_proved",
            "missing_for_claim": "full-rank response map to q_loc, source-normalization, extra stress, PPN, boundary, coupling",
            "fallback": "component/residual acquisition rows for every unlocked channel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "RDO775_3_no_source_or_boundary_work",
            "owner_clause": "Compact exterior response Euler equation has no source or boundary work.",
            "mathematical_form": "L_AB R^B = J_A + B_A with J_A=0 and B_A=0 by parent Ward/charge/boundary identities",
            "would_close": "positive response norm could imply R=0 and hence local silence.",
            "current_result": "blocked_by_Y5_Y6_boundary_coupling",
            "missing_for_claim": "source current closure, no extra stress work, observed boundary no-flux, coupling descent",
            "fallback": "B_obs_bulk_Euler, B_obs_source_measure, B_obs_boundary rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "RDO775_4_projector_and_readout_descent",
            "owner_clause": "P_loc/Pi_M/readout projections descend from parent data and commute on the allowed local domain.",
            "mathematical_form": "[d,P_loc]J_red=0 and [d,Pi_M]J_H=0 or each commutator is retained as source-backed residual",
            "would_close": "projected Ward zero would not hide unprojected force/flux components.",
            "current_result": "open_current_corpus",
            "missing_for_claim": "parent projector algebra, Hodge/domain operator, source-orbit readout descent",
            "fallback": "B_obs_projector_commutator_over_MH row",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "RDO775_5_verdict",
            "owner_clause": "Promote response-displacement owner to current MTS proof.",
            "mathematical_form": "RDO775_0..RDO775_4 all close with source paths and no placeholder/cancellation credit",
            "would_close": "Gamma/Khat owner, B_obs zero theorem candidate, and deltaH curl branch reentry",
            "current_result": "fail_current_corpus",
            "missing_for_claim": "owner clauses are not parent-signed; B_obs source rows are absent",
            "fallback": "open B_obs source acquisition and target variation ledger next",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def bobs_source_ledger_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": "BSA775_0_bulk_Euler_flux",
            "quantity": "B_obs_bulk_Euler_over_MH",
            "candidate_artifact": str(RESIDUALS / "P8_Y5_R10_775_BOBS_BULK_EULER_INPUT_CANDIDATE.csv"),
            "required_columns": "system_id;annulus;field_A;E_A;nabla_Phi_A;P_loc_component;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "acceptable_source": "explicit reduced Euler equations/profile, or theorem-zero certificate for E_A=0 in compact exterior",
            "status": "schema_ready_no_source_rows",
            "claim_gate": "no MISSING markers and units/source path verified",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "source_id": "BSA775_1_boundary_improvement_flux",
            "quantity": "B_obs_boundary_improvement_over_MH",
            "candidate_artifact": str(RESIDUALS / "P8_Y5_R10_775_BOBS_BOUNDARY_IMPROVEMENT_INPUT_CANDIDATE.csv"),
            "required_columns": "system_id;surface_id;boundary_class;B_GK_component;B_ref_component;P_loc_component;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "acceptable_source": "fixed-reference no-flux theorem, exact/topological boundary term proof, or finite-boundary flux source",
            "status": "schema_ready_no_source_rows",
            "claim_gate": "boundary convention and reference branch fixed before readout",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "source_id": "BSA775_2_source_measure_flux",
            "quantity": "B_obs_source_measure_over_MH",
            "candidate_artifact": str(RESIDUALS / "P8_Y5_R10_775_BOBS_SOURCE_MEASURE_INPUT_CANDIDATE.csv"),
            "required_columns": "system_id;source_channel;coupling_descent_status;C_qmu;flux_value;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "acceptable_source": "quotient-invariant matter/source action, same-frame Hilbert current, PiM/source closure, or sourced coefficient",
            "status": "schema_ready_no_source_rows",
            "claim_gate": "coupling/source descent signed or coefficient bounded",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "source_id": "BSA775_3_corner_edge_flux",
            "quantity": "B_obs_corner_edge_over_MH",
            "candidate_artifact": str(RESIDUALS / "P8_Y5_R10_775_BOBS_CORNER_EDGE_INPUT_CANDIDATE.csv"),
            "required_columns": "system_id;corner_id;edge_mode_class;flux_value;proper_or_improper;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "acceptable_source": "observed edge-mode theorem, corner symplectic flux calculation, or boundary-collar exclusion proof",
            "status": "schema_ready_no_source_rows",
            "claim_gate": "proper representative zeros not reused as observed edge zeros",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "source_id": "BSA775_4_projector_commutator_flux",
            "quantity": "B_obs_projector_commutator_over_MH",
            "candidate_artifact": str(RESIDUALS / "P8_Y5_R10_775_BOBS_PROJECTOR_COMMUTATOR_INPUT_CANDIDATE.csv"),
            "required_columns": "system_id;projector_id;commutator_value;domain_dependence;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "acceptable_source": "parent-owned topological/projector descent theorem, Hodge/domain operator proof, or finite commutator bound",
            "status": "schema_ready_no_source_rows",
            "claim_gate": "no post-readout projector masks",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "source_id": "BSA775_5_total_Bobs",
            "quantity": "B_observed_reduced_flux_over_MH",
            "candidate_artifact": str(RESIDUALS / "P8_Y5_R10_775_BOBS_TOTAL_INPUT_CANDIDATE.csv"),
            "required_columns": "component_id;value;units;source_path;zero_theorem_or_bound;no_cancellation_flag;valid_for_claim",
            "acceptable_source": "all component rows zero/bounded with no cancellation credit",
            "status": "schema_ready_no_source_rows",
            "claim_gate": "every component valid_for_claim=true before total can be true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_readiness_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "BCR775_0_owner_certificate",
            "gate": "response-displacement owner certificate exists and closes RDO775_0..RDO775_4",
            "current_evidence": "no certificate artifact exists",
            "result": "blocked",
            "required_exit": "parent-signed owner with explicit variables, action, variation, source paths, and no hidden multiplier",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "BCR775_1_component_sources",
            "gate": "all B_obs source component candidate files contain sourced rows",
            "current_evidence": "component candidate files intentionally absent",
            "result": "blocked",
            "required_exit": "positive numeric/theorem rows with units and no MISSING markers",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "BCR775_2_coupling_source_measure",
            "gate": "source-measure flux is covered by quotient-invariant matter/source/readout descent",
            "current_evidence": "759 coupling owner action not accepted; coupling residual acquisition runner remains open",
            "result": "blocked",
            "required_exit": "coupling descent input or source-measure coefficient bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "BCR775_3_no_cancellation",
            "gate": "total B_obs uses nonnegative component sum with no cancellation credit",
            "current_evidence": "guard retained from 774",
            "result": "guard_passed_nonclaim",
            "required_exit": "future total row must list every component and source path",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "BCR775_4_local_claim",
            "gate": "B_obs zero, deltaH zero, local GR/Newton/PPN/R10/R11 promotion",
            "current_evidence": "owner and source rows remain missing",
            "result": "blocked",
            "required_exit": "owner theorem or fully sourced component bounds plus downstream Y5/Y6/PPN gates",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def exit_criteria_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "exit_id": "EX775_0_derivation_route",
            "route": "response-displacement parent owner",
            "exit_condition": "RDO775_0..RDO775_4 close and validation finds a real owner certificate",
            "if_met": "return to reduced Ward/no-flux theorem and retest B_obs zero",
            "if_not_met": "continue B_obs source acquisition",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "exit_id": "EX775_1_component_route",
            "route": "B_obs source acquisition",
            "exit_condition": "BSA775_0..BSA775_5 have sourced theorem/numeric rows with units and no placeholders",
            "if_met": "run B_obs comparator and deltaH curl component gate",
            "if_not_met": "local claims remain blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "exit_id": "EX775_2_coupling_route",
            "route": "source-measure/coupling descent",
            "exit_condition": "COA759-style quotient matter/source/readout descent is parent-signed or coefficient-bounded",
            "if_met": "source-measure component can be zeroed or bounded",
            "if_not_met": "B_obs_source_measure_over_MH remains live",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D775_0_owner_attempt_not_promoted",
            "decision": "do not accept the response-displacement owner for current MTS",
            "reason": "the ansatz is coherent but lacks explicit parent variables, metric response, physical residual lock, source/boundary silence, and projector descent",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D775_1_Bobs_source_ledger_opened",
            "decision": "open source-acquisition rows for every B_obs component",
            "reason": "if the owner does not close, the live deltaH curl component must be bounded component-by-component",
            "claim_status": "source_acquisition_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D775_2_coupling_bite_retained",
            "decision": "keep source-measure/coupling descent inside B_obs rather than treating boundary flux as pure geometry",
            "reason": "759 shows source/readout coupling can leak into measured GM, EM/charge, clocks, or orbit readout even if geometry looks clean",
            "claim_status": "coupling_gate_active",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D775_3_next_target",
            "decision": "write the response-displacement variation ledger or start the first B_obs source pack",
            "reason": "this is the fastest way to find out whether the derivation route can be parent-signed before going numerical",
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
            "main_result": "response-displacement owner ansatz sharpened but not parent-signed; B_obs component source-acquisition ledger opened",
            "hard_blocker": "no explicit parent response field, no Khat metric response computation, no physical residual lock, no source/boundary work zero, no projector/readout descent",
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
    owner: list[dict[str, Any]],
    source_ledger: list[dict[str, Any]],
    readiness: list[dict[str, Any]],
    exits: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    expected_owner_ids = {
        "RDO775_0_response_displacement_ansatz",
        "RDO775_1_metric_response_conjugacy",
        "RDO775_2_physical_residual_lock",
        "RDO775_3_no_source_or_boundary_work",
        "RDO775_4_projector_and_readout_descent",
        "RDO775_5_verdict",
    }
    expected_source_ids = {
        "BSA775_0_bulk_Euler_flux",
        "BSA775_1_boundary_improvement_flux",
        "BSA775_2_source_measure_flux",
        "BSA775_3_corner_edge_flux",
        "BSA775_4_projector_commutator_flux",
        "BSA775_5_total_Bobs",
    }

    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_774_clean = all(validation_clean(number) for number in range(665, 775))
    owner_attempt_complete = expected_owner_ids.issubset({row["owner_id"] for row in owner})
    owner_not_promoted = any(row["owner_id"] == "RDO775_5_verdict" and row["current_result"] == "fail_current_corpus" for row in owner)
    source_ledger_complete = expected_source_ids.issubset({row["source_id"] for row in source_ledger})
    source_rows_nonclaim = all(row["status"] == "schema_ready_no_source_rows" for row in source_ledger)
    readiness_blocks_claim = any(row["gate_id"] == "BCR775_4_local_claim" and row["result"] == "blocked" for row in readiness)
    exit_routes_written = len(exits) >= 3
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, owner, source_ledger, readiness, exits, decisions, summary)
    )
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D775_3_next_target" for row in decisions)
    candidate_artifacts_not_faked = all(not path.exists() for path in CANDIDATE_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V775_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V775_1_source_needles_present", source_needles_present, "all local source needles present"),
        ("V775_2_prior_665_774_clean", prior_665_774_clean, "665-774 validation rows have no failures"),
        ("V775_3_owner_attempt_complete", owner_attempt_complete, "response-displacement owner clauses complete"),
        ("V775_4_owner_not_promoted", owner_not_promoted, "current corpus verdict remains fail_current_corpus"),
        ("V775_5_Bobs_source_ledger_complete", source_ledger_complete, "B_obs source acquisition rows complete"),
        ("V775_6_source_rows_nonclaim", source_rows_nonclaim, "source acquisition rows are schemas, not data"),
        ("V775_7_readiness_blocks_claim", readiness_blocks_claim, "local claim gate remains blocked"),
        ("V775_8_exit_routes_written", exit_routes_written, "derivation/component/coupling exits written"),
        ("V775_9_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V775_10_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V775_11_candidate_artifacts_not_faked", candidate_artifacts_not_faked, "no owner/Bobs/local-GR claim artifacts fabricated"),
        ("V775_12_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V775_13_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V775_14_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    source_ledger: list[dict[str, Any]],
    readiness: list[dict[str, Any]],
    exits: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 775 - Y5 R10 Observed Boundary Flux Source Acquisition Or Response Displacement Owner

Current result: **the response-displacement route is coherent but not parent-signed**. A parent response field could in principle make `Gamma_eff` and `K_hat` two faces of one variational object, but current MTS does not yet provide the explicit response variables, metric-response computation, full physical residual lock, zero source/boundary work theorem, or projector/readout descent. Therefore `B_obs` source acquisition is opened component-by-component without claim data.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Response-Displacement Owner Attempt

{markdown_table(owner, ["owner_id", "owner_clause", "mathematical_form", "would_close", "current_result", "missing_for_claim", "fallback", "valid_for_claim"])}

## B_obs Source Acquisition Ledger

{markdown_table(source_ledger, ["source_id", "quantity", "candidate_artifact", "required_columns", "acceptable_source", "status", "claim_gate", "valid_for_claim"])}

## B_obs Claim Readiness Gate

{markdown_table(readiness, ["gate_id", "gate", "current_evidence", "result", "required_exit", "valid_for_claim"])}

## Exit Criteria

{markdown_table(exits, ["exit_id", "route", "exit_condition", "if_met", "if_not_met", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is good engineering discipline: the owner route now has exact failure points, and the data route now has exact source columns. The coupling bite is explicitly retained inside `B_obs_source_measure_over_MH`; we are not treating boundary flux as pure geometry when matter/source/readout can leak into measured GM, clocks, photons, EM charge, or orbital calibration.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    owner = owner_attempt_rows(generated_utc)
    source_ledger = bobs_source_ledger_rows(generated_utc)
    readiness = claim_readiness_rows(generated_utc)
    exits = exit_criteria_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, owner, source_ledger, readiness, exits, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(OWNER_ATTEMPT_PATH, owner, ["owner_id", "owner_clause", "mathematical_form", "would_close", "current_result", "missing_for_claim", "fallback", "valid_for_claim", "generated_utc"])
    write_csv(BOBS_SOURCE_LEDGER_PATH, source_ledger, ["source_id", "quantity", "candidate_artifact", "required_columns", "acceptable_source", "status", "claim_gate", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_READINESS_PATH, readiness, ["gate_id", "gate", "current_evidence", "result", "required_exit", "valid_for_claim", "generated_utc"])
    write_csv(EXIT_CRITERIA_PATH, exits, ["exit_id", "route", "exit_condition", "if_met", "if_not_met", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_MATRIX_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, owner, source_ledger, readiness, exits, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"775 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
