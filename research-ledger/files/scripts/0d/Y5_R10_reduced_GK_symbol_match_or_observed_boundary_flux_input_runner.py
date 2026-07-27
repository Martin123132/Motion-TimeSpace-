from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "774-Y5-R10-reduced-GK-symbol-match-or-observed-boundary-flux-input-runner.md"
NEXT_TARGET = "775-Y5-R10-observed-boundary-flux-source-acquisition-or-response-displacement-owner.md"
STATUS = "Y5_R10_774_reduced_GK_symbol_match_reaudited_current_match_fails_Bobs_input_runner_staged_nonclaim"
CLAIM_CEILING = "reduced_GK_symbol_match_reentry_and_Bobs_input_runner_only_no_observed_flux_zero_no_deltaH_zero_no_Newton_PPN_R10_R11_or_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_774_SOURCE_REGISTER.csv"
SYMBOL_MATCH_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_774_REDUCED_GK_SYMBOL_MATCH_REENTRY_AUDIT.csv"
REPAIR_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_774_RESPONSE_DISPLACEMENT_REPAIR_CONTRACT.csv"
BOBS_INPUT_RUNNER_PATH = RESIDUALS / "P8_Y5_R10_774_BOBS_INPUT_RUNNER_SCHEMA.csv"
RUNNER_DRYRUN_PATH = RESIDUALS / "P8_Y5_R10_774_BOBS_INPUT_RUNNER_DRYRUN.csv"
DECISION_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_774_DECISION_MATRIX.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_774_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_774_VALIDATION.csv"

CANDIDATE_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_774_REDUCED_GK_SYMBOL_MATCH_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_774_BOBS_NUMERIC_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_774_OBSERVED_FLUX_ZERO_CLAIM.csv",
    RESIDUALS / "P8_Y5_R10_774_LOCAL_GR_REENTRY_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    SYMBOL_MATCH_AUDIT_PATH,
    REPAIR_CONTRACT_PATH,
    BOBS_INPUT_RUNNER_PATH,
    RUNNER_DRYRUN_PATH,
    DECISION_MATRIX_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCES: dict[str, dict[str, Any]] = {
    "773_doc": {
        "path": POST_CHECKPOINT / "773-Y5-R10-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md",
        "needles": ["D773_3_next_target", "B_observed_reduced_flux_over_MH"],
        "role": "immediate 774 handoff: reduced symbol match before B_obs inputs",
    },
    "773_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_773_VALIDATION.csv",
        "needles": ["V773_3_conditional_theorem_contract_written", "pass"],
        "role": "prior validation guard",
    },
    "773_clause_gate": {
        "path": RESIDUALS / "P8_Y5_R10_773_OBSERVED_FLUX_ZERO_CLAUSE_GATE.csv",
        "needles": ["OFC773_1_Gamma_Khat_metric_response", "OFC773_5_projector_descent"],
        "role": "observed no-flux theorem clauses",
    },
    "773_component_split": {
        "path": RESIDUALS / "P8_Y5_R10_773_OBSERVED_FLUX_COMPONENT_SPLIT.csv",
        "needles": ["OFS773_5_total_observed_reduced_flux", "source_fill_required_if_774_fails"],
        "role": "observed flux component split",
    },
    "513_doc": {
        "path": POST_CHECKPOINT / "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
        "needles": ["T_GK^{mu nu} := Gamma_eff g^{mu nu} - K_hat^{mu nu}", "GK513_4_projector_ownership"],
        "role": "original stress-divergence identity and projector gate",
    },
    "514_doc": {
        "path": POST_CHECKPOINT / "514-construct-GK-stress-action-or-residual-bound.md",
        "needles": ["GK514_A_metric_response_scalar_density", "MR514_1_Khat_metric_response"],
        "role": "candidate GK action and metric-response contract",
    },
    "515_doc": {
        "path": POST_CHECKPOINT / "515-match-Gamma-eff-Khat-to-metric-response-action.md",
        "needles": ["No current corpus source proves that Gamma_eff is a covariant scalar action density.", "MA515_1_Khat_metric_response"],
        "role": "first strict symbol-match failure",
    },
    "516_doc": {
        "path": POST_CHECKPOINT / "516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md",
        "needles": ["GO516_A_response_doublet_quadratic_density", "not_checked_current_MTS"],
        "role": "response-doublet owner candidate and unresolved metric response",
    },
    "733_ward_gate": {
        "path": RESIDUALS / "P8_Y5_R10_733_WARD_ZERO_GATE.csv",
        "needles": ["WZG733_0_current_symbol_match", "fail_for_current_claim"],
        "role": "hybrid reduced Ward zero gate",
    },
    "755_obstruction": {
        "path": RESIDUALS / "P8_Y5_R10_755_GK_SYMBOL_MATCH_OBSTRUCTION_LEDGER.csv",
        "needles": ["GKO755_0_Gamma_scalar_density", "GKO755_1_Khat_metric_response"],
        "role": "recent q_loc Ward-owner symbol obstruction",
    },
    "756_match_audit": {
        "path": RESIDUALS / "P8_Y5_R10_756_METRIC_RESPONSE_SYMBOL_MATCH_AUDIT.csv",
        "needles": ["MRM756_5_verdict", "accept current Gamma/Khat metric-response symbol match"],
        "role": "recent metric-response symbol match audit",
    },
    "756_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_756_VALIDATION.csv",
        "needles": ["V756_3_symbol_match_failed_cleanly", "pass"],
        "role": "recent symbol-match validation",
    },
    "757_doc": {
        "path": POST_CHECKPOINT / "757-Y5-R10-response-doublet-physical-lock-or-real-q_loc-component-input.md",
        "needles": ["physical_lock_not_proved", "real q_loc^nu field/profile or theorem-zero certificate"],
        "role": "formal response doublet not enough for observed residuals",
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


def symbol_match_audit_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "match_id": "RGM774_0_variational_contract",
            "target": "reduced GK Hilbert-stress owner",
            "required_identity": "S_GK^hyb=-int sqrt(-g_obs) gamma[Q_obs^hybrid]+int_boundary B_GK; T_GK^{mu nu}=Gamma_eff g_obs^{mu nu}-K_hat^{mu nu}",
            "current_evidence": "513/514/733/755 give a coherent conditional Ward route",
            "result": "pass_conditional_contract_only",
            "repair_or_fallback": "use only as theorem contract until symbol rows below close",
            "blocks": "none by itself; it is the allowed route shape",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "match_id": "RGM774_1_Gamma_scalar_density",
            "target": "Gamma_eff == gamma[g_obs,Phi_red,nablaPhi,D,...]",
            "required_identity": "Gamma_eff is a covariant scalar action density with units and no post-readout selector",
            "current_evidence": "515/756 find Gamma_eff remains symbolic/readout/route-level, not a parent scalar density",
            "result": "fail_current_corpus",
            "repair_or_fallback": "response-displacement parent owner or B_obs/q_loc source-backed component rows",
            "blocks": "T_GK Hilbert-stress owner and observed Ward no-flux theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "match_id": "RGM774_2_Khat_metric_response",
            "target": "K_hat == K_gamma",
            "required_identity": "K_gamma^{mu nu}=2/sqrt(-g_obs) delta[sqrt(-g_obs)gamma]/delta g_obs_{mu nu} including derivative, boundary, projector, and domain terms",
            "current_evidence": "515/755/756 keep Khat in q_loc identities and owner-current targets but not as a computed metric response",
            "result": "fail_current_corpus",
            "repair_or_fallback": "compute K_gamma from a proposed gamma and compare tensor slots, otherwise carry Khat as independent residual source",
            "blocks": "Ward divergence identity for current T_GK",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "match_id": "RGM774_3_Helmholtz_integrability",
            "target": "stress tensor is variational",
            "required_identity": "delta(sqrt(-g)T_GK^{mu nu})/delta g_alpha_beta has symmetric second-variation/Helmholtz structure up to allowed boundary terms",
            "current_evidence": "513 marked this not checked; 756 found no newer closure",
            "result": "not_closed_current_corpus",
            "repair_or_fallback": "run Helmholtz/integrability test only after gamma and Khat definitions are explicit",
            "blocks": "existence of a true S_GK owner",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "match_id": "RGM774_4_Ploc_projector_descent",
            "target": "P_loc parent owner and commutator silence",
            "required_identity": "P_loc descends from parent data and commutes with local/readout/Hodge split on the allowed exterior domain",
            "current_evidence": "513/733/755/773 keep P_loc ownership and projector descent open",
            "result": "open_current_corpus",
            "repair_or_fallback": "derive parent projector algebra or carry unprojected/component residuals",
            "blocks": "projected q_loc and observed B_obs zero claims",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "match_id": "RGM774_5_boundary_source_metric_terms",
            "target": "boundary/source/domain metric variations",
            "required_identity": "boundary, source-measure, domain, and reference variations are included in K_gamma or theorem-zero/fixed-reference",
            "current_evidence": "755 and 773 keep observed reduced boundary/source flux alive after representative zeros",
            "result": "open_current_corpus",
            "repair_or_fallback": "B_obs input runner rows BIR774_0..BIR774_5",
            "blocks": "observed reduced no-flux theorem and deltaH curl closure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "match_id": "RGM774_6_response_doublet_repair",
            "target": "response-displacement/doublet repair route",
            "required_identity": "formal auxiliary double-zero must be full-rank locked to observed q_loc/Y5/Y6/PPN/boundary/coupling residual vector",
            "current_evidence": "516 gives a formal quadratic candidate; 757 says the physical residual lock is not proved",
            "result": "promising_but_not_symbol_match",
            "repair_or_fallback": "parent-sign response-displacement owner or switch to real component inputs",
            "blocks": "using formal Z=0 as observed local-GR proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "match_id": "RGM774_7_verdict",
            "target": "accept reduced GK symbol match for current MTS",
            "required_identity": "RGM774_1 through RGM774_5 close without placeholders",
            "current_evidence": "multiple prior audits agree the match is not present",
            "result": "fail_current_corpus",
            "repair_or_fallback": "stage B_obs input runner and target response-displacement owner/source acquisition next",
            "blocks": "observed flux zero, deltaH zero, local GR, Newton, PPN, R10/R11 claims",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def repair_contract_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "repair_id": "RDR774_0_parent_response_field",
            "repair_route": "construct a parent response/displacement field R_A whose scalar projection is gamma and whose tensor response is K_gamma",
            "required_deliverable": "explicit field variables; action density; units; variation with respect to g_obs; source path",
            "pass_condition": "Gamma_eff=gamma and K_hat=K_gamma are both derived from one parent object",
            "current_status": "not_filled",
            "fallback_if_missing": "BIR774 component rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "repair_id": "RDR774_1_metric_response_computation",
            "repair_route": "compute K_gamma including derivative/boundary/domain terms",
            "required_deliverable": "tensor slot comparison table Khat-K_gamma with sign convention and boundary terms",
            "pass_condition": "all tensor components match or unmatched pieces are separately residualized",
            "current_status": "not_filled",
            "fallback_if_missing": "B_obs_boundary_improvement_over_MH and Khat_unmatched_over_MH rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "repair_id": "RDR774_2_Helmholtz_integrability_test",
            "repair_route": "test whether proposed T_GK is variational",
            "required_deliverable": "second-variation symmetry/Helmholtz ledger for sqrt(-g)T_GK",
            "pass_condition": "stress derives from a scalar action up to declared exact boundary improvements",
            "current_status": "waiting_on_explicit_gamma_Kgamma",
            "fallback_if_missing": "treat q_loc/B_obs as nonvariational residual",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "repair_id": "RDR774_3_projector_descent",
            "repair_route": "derive P_loc from parent projector algebra before readout",
            "required_deliverable": "P_loc owner, commutator [d,P_loc] proof, and no hidden component tuning",
            "pass_condition": "P_loc may be applied after the Ward identity without creating leakage",
            "current_status": "open",
            "fallback_if_missing": "B_obs_projector_commutator_over_MH row",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "repair_id": "RDR774_4_no_public_claim_guard",
            "repair_route": "do not promote local GR from the contract alone",
            "required_deliverable": "all rows above parent-signed or source-backed",
            "pass_condition": "no MISSING markers and validation confirms no candidate artifacts were fabricated",
            "current_status": "guard_active",
            "fallback_if_missing": "nonclaim status retained",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def bobs_input_runner_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "input_id": "BIR774_0_bulk_Euler_flux",
            "quantity": "B_obs_bulk_Euler_over_MH",
            "formula": "abs(P_loc sum_A E_A nabla^nu Phi_A contribution to curl(deltaH))/M_H_ref",
            "required_columns": "system_id;annulus;field_A;E_A;nabla_Phi_A;P_loc_component;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "source_requirement": "reduced Euler equations/profile or theorem-zero certificate",
            "current_status": "MISSING_REDUCED_EULER_ZERO_OR_NUMERIC",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "BIR774_1_boundary_improvement_flux",
            "quantity": "B_obs_boundary_improvement_over_MH",
            "formula": "abs(P_loc B_GK^nu plus reference/improvement contribution to curl(deltaH))/M_H_ref",
            "required_columns": "system_id;surface_id;boundary_class;B_GK_component;B_ref_component;P_loc_component;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "source_requirement": "fixed-reference no-flux theorem or finite-boundary flux source",
            "current_status": "MISSING_BOUNDARY_REFERENCE_NO_FLUX_OR_NUMERIC",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "BIR774_2_source_measure_flux",
            "quantity": "B_obs_source_measure_over_MH",
            "formula": "abs(P_loc B_source_measure^nu or C_qmu q_loc projected source-strength term)/M_H_ref",
            "required_columns": "system_id;source_channel;coupling_descent_status;C_qmu;flux_value;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "source_requirement": "same-frame source measure/no-marker theorem plus PiM closure or sourced coefficient",
            "current_status": "MISSING_SOURCE_MEASURE_SILENCE_OR_NUMERIC",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "BIR774_3_corner_edge_flux",
            "quantity": "B_obs_corner_edge_over_MH",
            "formula": "abs(non-proper observed edge/corner symplectic flux contribution)/M_H_ref",
            "required_columns": "system_id;corner_id;edge_mode_class;flux_value;proper_or_improper;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "source_requirement": "observed edge-mode zero theorem or corner flux source",
            "current_status": "MISSING_OBSERVED_EDGE_MODE_ZERO_OR_NUMERIC",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "BIR774_4_projector_commutator_flux",
            "quantity": "B_obs_projector_commutator_over_MH",
            "formula": "abs(integral_A [d,P_loc]J_red or [d,Pi_M]J_H contribution)/M_H_ref",
            "required_columns": "system_id;projector_id;commutator_value;domain_dependence;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "source_requirement": "parent-owned topological/projector descent theorem or finite commutator bound",
            "current_status": "MISSING_PROJECTOR_DESCENT_ZERO_OR_NUMERIC",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "BIR774_5_total_Bobs",
            "quantity": "B_observed_reduced_flux_over_MH",
            "formula": "sum of nonnegative BIR774 components with no cancellation credit",
            "required_columns": "component_id;value;units;source_path;zero_theorem_or_bound;no_cancellation_flag;valid_for_claim",
            "source_requirement": "all component rows zero/bounded and no MISSING markers",
            "current_status": "MISSING_COMPONENTS",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def runner_dryrun_rows(generated_utc: str) -> list[dict[str, Any]]:
    candidate_path = RESIDUALS / "P8_Y5_R10_774_BOBS_NUMERIC_INPUT_CANDIDATE.csv"
    symbol_certificate = RESIDUALS / "P8_Y5_R10_774_REDUCED_GK_SYMBOL_MATCH_CERTIFICATE.csv"
    return [
        {
            "dryrun_id": "BDR774_0_symbol_match_certificate_absent",
            "check": "reduced GK symbol match claim data",
            "input_state": f"exists={symbol_certificate.exists()} path={symbol_certificate}",
            "runner_effect": "symbol theorem cannot promote observed no-flux",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "BDR774_1_Bobs_candidate_absent",
            "check": "observed boundary flux numeric/theorem input",
            "input_state": f"exists={candidate_path.exists()} path={candidate_path}",
            "runner_effect": "no B_obs score is run; schema only",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "BDR774_2_missing_markers_guard",
            "check": "component rows contain MISSING status",
            "input_state": "BIR774 rows intentionally MISSING_* until theorem/source rows exist",
            "runner_effect": "valid_for_claim remains false",
            "claim_status": "guard_passed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "BDR774_3_no_cancellation_guard",
            "check": "total B_obs is nonnegative component sum",
            "input_state": "no cancellation credit allowed between bulk, boundary, source, edge, and projector pieces",
            "runner_effect": "future bounds must close every component or carry total residual",
            "claim_status": "guard_passed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D774_0_contract_retained",
            "decision": "retain reduced GK Ward route as a conditional theorem contract",
            "reason": "the algebra/action shape is coherent and remains the cleanest derivation path if ownership is supplied",
            "claim_status": "contract_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D774_1_symbol_match_fails",
            "decision": "do not accept current Gamma_eff/K_hat/P_loc as reduced GK variational objects",
            "reason": "515, 733, 755, 756, and 773 all preserve the same missing owner/metric-response/projector clauses",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D774_2_Bobs_runner_staged",
            "decision": "stage the observed-boundary-flux input runner without candidate data",
            "reason": "773 made B_observed_reduced_flux_over_MH the live deltaH curl component if symbol ownership is not repaired",
            "claim_status": "schema_only_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D774_3_next_target",
            "decision": "hunt response-displacement owner while preparing source acquisition for B_obs rows",
            "reason": "this keeps derivation-first alive but gives us the bounded fallback if the owner cannot be parent-signed",
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
            "main_result": "reduced GK symbol match remains failed for current MTS; the observed B_obs flux runner is staged as the honest fallback",
            "hard_blocker": "no parent-signed Gamma_eff scalar density, K_hat metric response, Helmholtz integrability, P_loc descent, or observed boundary/source metric-variation no-flux certificate",
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
    symbol_audit: list[dict[str, Any]],
    repairs: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    expected_match_ids = {
        "RGM774_0_variational_contract",
        "RGM774_1_Gamma_scalar_density",
        "RGM774_2_Khat_metric_response",
        "RGM774_3_Helmholtz_integrability",
        "RGM774_4_Ploc_projector_descent",
        "RGM774_5_boundary_source_metric_terms",
        "RGM774_6_response_doublet_repair",
        "RGM774_7_verdict",
    }
    expected_runner_ids = {
        "BIR774_0_bulk_Euler_flux",
        "BIR774_1_boundary_improvement_flux",
        "BIR774_2_source_measure_flux",
        "BIR774_3_corner_edge_flux",
        "BIR774_4_projector_commutator_flux",
        "BIR774_5_total_Bobs",
    }

    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_773_clean = all(validation_clean(number) for number in range(665, 774))
    symbol_audit_complete = expected_match_ids.issubset({row["match_id"] for row in symbol_audit})
    symbol_match_failed = any(row["match_id"] == "RGM774_7_verdict" and row["result"] == "fail_current_corpus" for row in symbol_audit)
    repair_contract_written = len(repairs) >= 5 and any(row["repair_id"] == "RDR774_0_parent_response_field" for row in repairs)
    runner_schema_complete = expected_runner_ids.issubset({row["input_id"] for row in runner})
    runner_all_missing = all("MISSING" in row["current_status"] for row in runner)
    dryrun_blocks_without_data = any(row["dryrun_id"] == "BDR774_1_Bobs_candidate_absent" and "exists=False" in row["input_state"] for row in dryrun)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, symbol_audit, repairs, runner, dryrun, decisions, summary)
    )
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D774_3_next_target" for row in decisions)
    candidate_artifacts_not_faked = all(not path.exists() for path in CANDIDATE_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V774_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V774_1_source_needles_present", source_needles_present, "all local source needles present"),
        ("V774_2_prior_665_773_clean", prior_665_773_clean, "665-773 validation rows have no failures"),
        ("V774_3_symbol_audit_complete", symbol_audit_complete, "reduced GK symbol match rows complete"),
        ("V774_4_symbol_match_failed_cleanly", symbol_match_failed, "current corpus verdict remains fail_current_corpus"),
        ("V774_5_repair_contract_written", repair_contract_written, "response-displacement repair contract written"),
        ("V774_6_Bobs_runner_schema_complete", runner_schema_complete, "B_obs component input runner rows complete"),
        ("V774_7_Bobs_runner_missing_markers", runner_all_missing, "runner rows stay MISSING_* until theorem/source rows exist"),
        ("V774_8_dryrun_blocks_without_data", dryrun_blocks_without_data, "dry-run does not score absent B_obs candidate"),
        ("V774_9_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V774_10_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V774_11_candidate_artifacts_not_faked", candidate_artifacts_not_faked, "no symbol-match/B_obs/local-GR claim artifacts fabricated"),
        ("V774_12_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V774_13_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V774_14_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    symbol_audit: list[dict[str, Any]],
    repairs: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 774 - Y5 R10 Reduced GK Symbol Match Or Observed Boundary Flux Input Runner

Current result: **the reduced GK symbol match still fails for current MTS**. The contract is good — `S_GK^hyb` would make `q_loc` an on-shell Ward/boundary residual if `Gamma_eff`, `K_hat`, and `P_loc` were parent-owned reduced variational objects. But the current corpus still does not provide the scalar-density owner, the metric-response tensor, Helmholtz integrability, projector descent, or observed boundary/source no-flux certificate. Therefore the observed `B_obs` component runner is staged as the honest fallback.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Reduced GK Symbol Match Reentry Audit

{markdown_table(symbol_audit, ["match_id", "target", "required_identity", "current_evidence", "result", "repair_or_fallback", "blocks", "valid_for_claim"])}

## Response-Displacement Repair Contract

{markdown_table(repairs, ["repair_id", "repair_route", "required_deliverable", "pass_condition", "current_status", "fallback_if_missing", "valid_for_claim"])}

## B_obs Input Runner Schema

{markdown_table(runner, ["input_id", "quantity", "formula", "required_columns", "source_requirement", "current_status", "valid_for_claim"])}

## Runner Dry Run

{markdown_table(dryrun, ["dryrun_id", "check", "input_state", "runner_effect", "claim_status", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is the cleanest version of the bad news: the route itself is not dead, but the current symbols have still not paid the entry fee. To get local GR from this branch we now need one of two things: either a real parent response-displacement owner that makes `Gamma_eff` and `K_hat` two faces of one variational object, or real source-backed `B_obs` component rows. No plateau axiom, no fake zeros, no hidden cancellation.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    symbol_audit = symbol_match_audit_rows(generated_utc)
    repairs = repair_contract_rows(generated_utc)
    runner = bobs_input_runner_rows(generated_utc)
    dryrun = runner_dryrun_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, symbol_audit, repairs, runner, dryrun, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(SYMBOL_MATCH_AUDIT_PATH, symbol_audit, ["match_id", "target", "required_identity", "current_evidence", "result", "repair_or_fallback", "blocks", "valid_for_claim", "generated_utc"])
    write_csv(REPAIR_CONTRACT_PATH, repairs, ["repair_id", "repair_route", "required_deliverable", "pass_condition", "current_status", "fallback_if_missing", "valid_for_claim", "generated_utc"])
    write_csv(BOBS_INPUT_RUNNER_PATH, runner, ["input_id", "quantity", "formula", "required_columns", "source_requirement", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(RUNNER_DRYRUN_PATH, dryrun, ["dryrun_id", "check", "input_state", "runner_effect", "claim_status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_MATRIX_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, symbol_audit, repairs, runner, dryrun, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"774 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
