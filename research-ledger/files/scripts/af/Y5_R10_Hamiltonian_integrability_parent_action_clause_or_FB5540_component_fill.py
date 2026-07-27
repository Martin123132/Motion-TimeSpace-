from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "770-Y5-R10-Hamiltonian-integrability-parent-action-clause-or-FB5540-component-fill.md"
NEXT_TARGET = "771-Y5-R10-theta-Qtau-current-owner-or-deltaH-component-source-row.md"
STATUS = "Y5_R10_770_Hamiltonian_integrability_parent_action_certificate_attempted_unsigned_FB5540_component_fill_staged_nonclaim"
CLAIM_CEILING = "parent_action_certificate_attempt_and_FB5540_component_fill_schema_only_no_HPiM_integrability_no_Newton_no_PPN_no_R10_R11_or_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_770_SOURCE_REGISTER.csv"
CERTIFICATE_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_770_PARENT_ACTION_CERTIFICATE_AUDIT.csv"
INTEGRABILITY_CURL_PATH = RESIDUALS / "P8_Y5_R10_770_INTEGRABILITY_CURL_TEST.csv"
COMPONENT_FILL_PATH = RESIDUALS / "P8_Y5_R10_770_FB5540_COMPONENT_FILL_FALLBACK.csv"
REPAIR_OPTIONS_PATH = RESIDUALS / "P8_Y5_R10_770_PARENT_ACTION_REPAIR_OPTIONS.csv"
DECISION_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_770_DECISION_MATRIX.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_770_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_770_VALIDATION.csv"

CANDIDATE_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_770_PARENT_ACTION_CERTIFICATE_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_770_DELTA_H_TAU_SOURCE_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_770_DELTA_REF_SOURCE_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_770_BOUNDARY_FLUX_SOURCE_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_770_TAU_MHREF_SOURCE_INPUT_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    CERTIFICATE_AUDIT_PATH,
    INTEGRABILITY_CURL_PATH,
    COMPONENT_FILL_PATH,
    REPAIR_OPTIONS_PATH,
    DECISION_MATRIX_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCES: dict[str, dict[str, Any]] = {
    "769_doc": {
        "path": POST_CHECKPOINT / "769-Y5-R10-FB554-0-Hamiltonian-integrability-reference-row-reentry.md",
        "needles": [
            "`FB554_0=0` is now an exact parent-action/coupling ownership target",
            "770-Y5-R10-Hamiltonian-integrability-parent-action-clause-or-FB5540-component-fill.md",
        ],
        "role": "immediate FB5540 reentry handoff",
    },
    "769_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_769_VALIDATION.csv",
        "needles": ["V769_6_parent_action_selected_first", "pass"],
        "role": "prior 769 validation guard",
    },
    "769_theorem_contract": {
        "path": RESIDUALS / "P8_Y5_R10_769_FB5540_REENTRY_THEOREM_CONTRACT.csv",
        "needles": ["FBR769_1_integrability_curl", "FBR769_5_total_verdict"],
        "role": "FB5540 theorem contract from reentry",
    },
    "769_components": {
        "path": RESIDUALS / "P8_Y5_R10_769_COMPONENT_STATUS_AFTER_REENTRY.csv",
        "needles": ["FBC769_0_delta_H_tau_nonintegrable", "FBC769_2_symplectic_boundary_flux"],
        "role": "FB5540 component state after reentry",
    },
    "667_doc": {
        "path": POST_CHECKPOINT / "667-Y5-R10-explicit-parent-boundary-action-ansatz-and-variation-ledger.md",
        "needles": ["delta H_tau[S] = int_S(delta Q_tau^MTS - i_tau Theta_total)", "does **not** yet prove `FB554_0=0`"],
        "role": "explicit parent boundary action ansatz",
    },
    "667_term_map": {
        "path": RESIDUALS / "P8_Y5_R10_667_FB5540_TERM_MAP.csv",
        "needles": ["TM667_0_delta_H_tau", "TM667_2_symplectic_boundary_flux"],
        "role": "FB5540 term map from parent action ansatz",
    },
    "668_doc": {
        "path": POST_CHECKPOINT / "668-Y5-R10-sector-Lagrangian-owner-and-boundary-condition-lock.md",
        "needles": ["L_X, Theta_X, Q_X", "`FB554_0=0` is still not proved"],
        "role": "sector Lagrangian owner lock",
    },
    "670_doc": {
        "path": POST_CHECKPOINT / "670-Y5-R10-no-pole-quotient-LX-route-or-positive-sourcefree-operator-proof.md",
        "needles": ["quotient/no-pole branch has a real conditional spine", "full no-pole proof is blocked"],
        "role": "no-pole/sourcefree L_X route",
    },
    "684_doc": {
        "path": POST_CHECKPOINT / "684-Y5-R10-observed-frame-tau-coframe-lock-for-MH-ref.md",
        "needles": ["tau_obs", "not yet constructed as the same stationary/clock/Hamiltonian generator"],
        "role": "observed frame tau/coframe lock",
    },
    "742_doc": {
        "path": POST_CHECKPOINT / "742-Y5-R10-observed-tau-owner-or-q_loc-free-coefficient-pack.md",
        "needles": ["observed `tau` is not parent-owned for the current chain", "NO_PARENT_SIGNED_TAU_LOCK"],
        "role": "later tau owner rejection",
    },
    "759_doc": {
        "path": POST_CHECKPOINT / "759-Y5-R10-coupling-owner-action-or-residual-vector-acquisition-runner.md",
        "needles": ["coupling owner action is not parent-signed yet", "quotient matter descent clause"],
        "role": "coupling owner action audit",
    },
    "760_doc": {
        "path": POST_CHECKPOINT / "760-Y5-R10-quotient-matter-descent-or-coupling-residual-source-pack.md",
        "needles": ["quotient matter descent is not parent-signed", "`c_g=0` is not claimed"],
        "role": "quotient matter descent proof attempt",
    },
    "767_doc": {
        "path": POST_CHECKPOINT / "767-Y5-R10-parent-matter-functor-no-alpha-vertex-or-WEP-closure.md",
        "needles": ["parent matter functor/no-alpha-vertex theorem is still not signed", "WEP safety remains an explicit quarantined closure"],
        "role": "WEP/no-alpha closure quarantine",
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


def certificate_audit_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "HIC770_0_parent_action_domain",
            "certificate_clause": "one local compact-region parent action and phase space",
            "mathematical_form": "S_parent[M,H]=int_M L_parent[g_obs,psi,X,lambda] + int_partialM B_ref + int_partialM B_top",
            "would_close": "gives one object from which theta_total, Q_tau, C_tau, and boundary terms must be varied",
            "current_status": "template_written_not_parent_signed",
            "failure_if_missing": "Hamiltonian current ownership remains notation rather than theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "HIC770_1_variation_owner",
            "certificate_clause": "explicit variation owner",
            "mathematical_form": "delta L_parent=E_A delta Phi^A+dTheta_total(Phi,delta Phi)",
            "would_close": "makes theta_total computable rather than imported from GR analogy",
            "current_status": "blocked_by_missing_explicit_LX_and_coupling_owner",
            "failure_if_missing": "delta_H_tau_nonintegrable cannot be evaluated",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "HIC770_2_charge_decomposition",
            "certificate_clause": "Noether/Hamiltonian charge decomposition",
            "mathematical_form": "J_tau=Theta_total(Phi,L_tau Phi)-i_tau L_parent=dQ_tau^MTS+C_tau",
            "would_close": "defines Q_tau^MTS and identifies constraint/source leakage C_tau",
            "current_status": "conditional_shape_only",
            "failure_if_missing": "Pi_M^H cannot be promoted to physical source-mass operator",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "HIC770_3_integrability_curl_zero",
            "certificate_clause": "field-space curl of delta H_tau vanishes",
            "mathematical_form": "curl(delta H_tau)=int_S i_tau omega_total + delta_tau terms + delta_surface terms + delta_ref terms = 0",
            "would_close": "kills delta_H_tau_nonintegrable_over_MH",
            "current_status": "not_signed",
            "failure_if_missing": "FB5540 first component remains live",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "HIC770_4_reference_lock",
            "certificate_clause": "B_ref/reference subtraction fixed before readout",
            "mathematical_form": "partial_{source,r,t,frame,lambda}Delta_ref=0 and delta H_ref=0",
            "would_close": "kills Delta_ref_over_MH and prevents source calibration hiding",
            "current_status": "not_parent_owned",
            "failure_if_missing": "reference freedom can mimic source normalization",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "HIC770_5_LX_boundary_policy",
            "certificate_clause": "retained L_X/boundary/edge sector is absent, proper-gauge, source-free no-pole, or explicitly residualized",
            "mathematical_form": "Theta_X=Q_X=0 or int_boundary(delta Q_X-i_tau Theta_X)=0; otherwise write residual component",
            "would_close": "kills or quarantines symplectic_boundary_flux_over_MH",
            "current_status": "not_closed_by_668_670_679_chain",
            "failure_if_missing": "edge/projector/non-EH flux remains a physical residual channel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "HIC770_6_tau_MHref_lock",
            "certificate_clause": "same observed tau and positive same-frame M_H_ref",
            "mathematical_form": "tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit; M_H_ref=G_ref^-1 int_S Q_tau^MTS>0",
            "would_close": "makes FB5540 normalization meaningful without importing orbital GM",
            "current_status": "blocked_by_684_742_and_MHref_chain",
            "failure_if_missing": "Hamiltonian source charge cannot be compared to Newton/PPN/R10 arenas",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "HIC770_7_coupling_descent_guard",
            "certificate_clause": "ordinary matter, constants, charge units, measure, coframe, and connection descend through the same observed quotient",
            "mathematical_form": "S_matter=Sbar_matter[q(Phi),psi,theta] and Lie_v S_matter=0 for v in ker(Dq), up to owned gauge/boundary terms",
            "would_close": "prevents a Hamiltonian charge proof from hiding WEP/clock/EM/source-coupling leakage",
            "current_status": "not_parent_signed_by_759_767_chain",
            "failure_if_missing": "local-GR proof would be a closure branch, not a field-theory derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "HIC770_8_certificate_verdict",
            "certificate_clause": "claim FB5540=0 from parent action",
            "mathematical_form": "HIC770_0..HIC770_7 all pass jointly => FB5540=0",
            "would_close": "would allow moving to FB5541/source equality",
            "current_status": "fail_current_corpus",
            "failure_if_missing": "stage FB5540 component-fill rows instead",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def integrability_curl_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "test_id": "ICT770_0_variation_formula",
            "object": "delta H_tau",
            "formula": "delta H_tau[S]=int_S(delta Q_tau^MTS-i_tau Theta_total)-delta H_ref",
            "passes_if": "Q_tau^MTS, Theta_total, tau, S, and H_ref are all parent-owned before readout",
            "current_result": "formula_shape_available_from_667_not_certificate",
            "activated_component": "delta_H_tau_nonintegrable_over_MH;Delta_ref_over_MH",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "ICT770_1_curl_identity",
            "object": "field-space curl",
            "formula": "(delta_1 delta_2-delta_2 delta_1)H_tau=int_S i_tau omega_total(delta_1,delta_2)+C_tau+Delta_tau+Delta_S+Delta_ref",
            "passes_if": "omega flux, constraints, tau variation, surface variation, and reference variation all vanish or are fixed constants",
            "current_result": "exact_test_written_not_evaluated",
            "activated_component": "delta_H_tau_nonintegrable_over_MH",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "ICT770_2_EH_sector",
            "object": "EH local exterior",
            "formula": "omega_EH flux vanishes under standard fixed boundary/Killing conditions",
            "passes_if": "local exterior is genuinely EH and boundary/reference conditions are fixed",
            "current_result": "conditional_reference_only",
            "activated_component": "delta_H_tau_nonintegrable_over_MH",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "ICT770_3_X_sector",
            "object": "retained MTS extra sector",
            "formula": "omega_X flux and C_X vanish only if X is quotient-absent/proper-gauge/source-free no-pole or bounded",
            "passes_if": "L_X owner, no-pole/sourcefree certificate, and boundary edge-zero all close",
            "current_result": "fail_current_corpus",
            "activated_component": "delta_H_tau_nonintegrable_over_MH;symplectic_boundary_flux_over_MH",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "ICT770_4_reference_and_tau",
            "object": "reference/tau/surface terms",
            "formula": "Delta_tau+Delta_S+Delta_ref=0",
            "passes_if": "tau_obs, surface/domain, and B_ref are fixed by one parent local branch",
            "current_result": "fail_current_corpus",
            "activated_component": "Delta_ref_over_MH;time_generator_lock;M_H_ref",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "ICT770_5_curl_verdict",
            "object": "delta_H_tau_nonintegrable_over_MH",
            "formula": "delta_H_tau_nonintegrable_over_MH=0",
            "passes_if": "ICT770_1 through ICT770_4 pass jointly",
            "current_result": "not_proved_zero",
            "activated_component": "FB5540_delta_H_tau_source_row_required_if_certificate_fails",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def component_fill_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "fill_id": "FB770_0_delta_H_tau",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "formula": "abs(curl(delta H_tau))/M_H_ref",
            "required_columns": "system_id;surface;field_variations;curl_value;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_PARENT_THETA_QTAU_OR_NUMERIC_CURL",
            "acceptance_gate": "theorem-zero or source-backed dimensionless bound with no cancellation credit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "FB770_1_Delta_ref",
            "quantity": "Delta_ref_over_MH",
            "formula": "abs(Delta_ref)/M_H_ref",
            "required_columns": "reference_branch;surface;Delta_ref;M_H_ref;derivative_silence_checks;units;source_path;valid_for_claim",
            "current_status": "MISSING_PARENT_REFERENCE_LOCK_OR_NUMERIC_PROFILE",
            "acceptance_gate": "source/range/frame/time derivatives zero or bounded with source-backed profile",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "FB770_2_boundary_flux",
            "quantity": "symplectic_boundary_flux_over_MH",
            "formula": "abs(int_boundary(delta Q_extra-i_tau Theta_extra)+delta B_class+projector_terms)/M_H_ref",
            "required_columns": "boundary_class;flux_integral;projector_terms;edge_terms;M_H_ref;units;source_path;valid_for_claim",
            "current_status": "MISSING_BOUNDARY_EDGE_PROJECTOR_ZERO_OR_NUMERIC_FLUX",
            "acceptance_gate": "boundary/edge theorem-zero or explicit source-backed flux bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "FB770_3_tau_mismatch",
            "quantity": "tau_role_mismatch",
            "formula": "norm(tau_source,tau_charge,tau_clock,tau_boundary,tau_orbit mismatch)",
            "required_columns": "tau_role;normalization;frame;domain;clock_link;charge_link;orbit_link;source_path;valid_for_claim",
            "current_status": "MISSING_PARENT_SELECTED_TAU_OBS_OR_MISMATCH_BOUND",
            "acceptance_gate": "one tau theorem or bounded mismatch small enough for every linked arena",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "FB770_4_MHref",
            "quantity": "M_H_ref",
            "formula": "G_ref^-1 int_S Q_tau^MTS",
            "required_columns": "system_id;surface;tau;Q_tau;G_ref;M_H_ref;positivity;source_frame;source_path;valid_for_claim",
            "current_status": "MISSING_POSITIVE_SAME_FRAME_MH_REF",
            "acceptance_gate": "positive same-frame Hamiltonian source denominator before orbital fitting",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def repair_option_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "repair_id": "RPO770_0_strict_quotient_absence",
            "route": "X is not a physical tangent direction before variation",
            "would_do": "Theta_X=Q_X=omega_X=0 and no X edge/source flux exists",
            "current_status": "not_signed",
            "risk": "setting X to zero after variation smuggles closure; must be absent in the parent tangent space",
            "next_action": "derive Dq kernel/tangent-space exclusion or abandon as theorem route",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "repair_id": "RPO770_1_sourcefree_positive_no_pole",
            "route": "X exists but is source-free, positive, no-pole, and boundary silent",
            "would_do": "omega_X and Q_X do not produce local source/PPN/R10 channels",
            "current_status": "blocked_by_670_and_edge_chain",
            "risk": "positive source-free bulk can still leave boundary/edge charge or coupling residue",
            "next_action": "prove boundary charge zero and matter descent jointly",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "repair_id": "RPO770_2_retained_residual_vector",
            "route": "accept retained X/boundary/coupling channels and score them",
            "would_do": "turn FB5540 into empirical residual rows rather than theorem-zero",
            "current_status": "fallback_selected_if_parent_certificate_fails",
            "risk": "the theory becomes testable but not yet derived local GR",
            "next_action": "fill FB770 component rows with source-backed values",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D770_0_certificate_attempt",
            "decision": "minimal Hamiltonian-integrability parent-action certificate attempted",
            "reason": "derivability is the preferred route and FB5540 is the first source-charge gate",
            "claim_status": "fail_current_corpus_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D770_1_no_theorem_zero",
            "decision": "do not claim FB5540=0",
            "reason": "theta_total/Q_tau, L_X/no-pole, B_ref, tau/MHref, boundary, and coupling descent are not jointly owned",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D770_2_next_best_target",
            "decision": "attack theta_total/Q_tau current ownership first",
            "reason": "without the parent current owner the curl cannot be evaluated and all component-fill rows remain symbolic",
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
            "main_result": "the minimal parent-action certificate is mathematically sharp but unsigned for current MTS; FB5540 theorem-zero is not promoted",
            "hard_blocker": "theta_total and Q_tau^MTS are not yet extracted from one explicit parent Lagrangian/current with fixed tau, B_ref, boundary policy, and coupling descent",
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
    certificate: list[dict[str, Any]],
    curl: list[dict[str, Any]],
    fill: list[dict[str, Any]],
    repairs: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_769_clean = all(validation_clean(number) for number in range(665, 770))
    certificate_attempted = any(row["clause_id"] == "HIC770_8_certificate_verdict" and row["current_status"] == "fail_current_corpus" for row in certificate)
    curl_test_written = any(row["test_id"] == "ICT770_1_curl_identity" and "curl" in row["object"] for row in curl)
    component_fallback_ready = len(fill) >= 5 and all("MISSING_" in row["current_status"] for row in fill)
    repair_options_written = len(repairs) == 3 and any(row["repair_id"] == "RPO770_2_retained_residual_vector" for row in repairs)
    candidate_artifacts_not_faked = all(not path.exists() for path in CANDIDATE_ARTIFACTS)
    all_nonclaim = all_claim_rows_false([sources, certificate, curl, fill, repairs, decisions, summary])
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D770_2_next_best_target" for row in decisions)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V770_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V770_1_source_needles_present", source_needles_present, "all local source needles present"),
        ("V770_2_prior_665_769_clean", prior_665_769_clean, "665-769 validation rows have no failures"),
        ("V770_3_certificate_attempted", certificate_attempted, "parent-action certificate attempted and verdict recorded"),
        ("V770_4_curl_test_written", curl_test_written, "integrability curl test written"),
        ("V770_5_component_fallback_ready", component_fallback_ready, "FB5540 component fallback rows staged with missing markers"),
        ("V770_6_repair_options_written", repair_options_written, "strict quotient, sourcefree/no-pole, and residual routes recorded"),
        ("V770_7_candidate_artifacts_not_faked", candidate_artifacts_not_faked, "no claim-input artifacts fabricated"),
        ("V770_8_no_claim_rows_promoted", all_nonclaim, "all generated rows valid_for_claim=false"),
        ("V770_9_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V770_10_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V770_11_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V770_12_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    certificate: list[dict[str, Any]],
    curl: list[dict[str, Any]],
    fill: list[dict[str, Any]],
    repairs: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 770 - Y5 R10 Hamiltonian Integrability Parent Action Clause Or FB5540 Component Fill

Start point: 769 collapsed the long FB5540 chain into one sharp question: can one parent action own `theta_total`, `Q_tau`, `B_ref`, `tau`, `L_X`, boundary policy, and ordinary coupling descent strongly enough to make the Hamiltonian charge integrable?

Current result: **the certificate can be stated cleanly, but it is not signed by the current corpus**. The key mathematical test is the field-space curl of `delta H_tau`; it can vanish only if the parent action fixes the symplectic flux, reference subtraction, time generator, surface/domain variation, and retained-sector boundary flux together. Current MTS does not yet supply those owned objects, so `FB5540=0` remains unproved and the component-fill fallback is staged.

## Status

| field | value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | {summary[0]["main_result"]} |
| Hard blocker | `{summary[0]["hard_blocker"]}` |
| Next target | `{NEXT_TARGET}` |

## Parent Action Certificate Audit

{markdown_table(certificate, ["clause_id", "certificate_clause", "mathematical_form", "would_close", "current_status", "failure_if_missing", "valid_for_claim"])}

## Integrability Curl Test

{markdown_table(curl, ["test_id", "object", "formula", "passes_if", "current_result", "activated_component", "valid_for_claim"])}

## FB5540 Component Fill Fallback

{markdown_table(fill, ["fill_id", "quantity", "formula", "required_columns", "current_status", "acceptance_gate", "valid_for_claim"])}

## Parent Action Repair Options

{markdown_table(repairs, ["repair_id", "route", "would_do", "current_status", "risk", "next_action", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is the clean engineering drawing of the missing bridge. If we can extract `theta_total` and `Q_tau^MTS` from one explicit parent Lagrangian/current, then the curl test becomes a real proof problem instead of fog. If that extraction fails, the honest route is not to “declare GR locally”; it is to fill `delta_H_tau`, `Delta_ref`, boundary flux, tau mismatch, and `M_H_ref` as source-backed residuals.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    certificate = certificate_audit_rows(generated_utc)
    curl = integrability_curl_rows(generated_utc)
    fill = component_fill_rows(generated_utc)
    repairs = repair_option_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, certificate, curl, fill, repairs, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(CERTIFICATE_AUDIT_PATH, certificate, ["clause_id", "certificate_clause", "mathematical_form", "would_close", "current_status", "failure_if_missing", "valid_for_claim", "generated_utc"])
    write_csv(INTEGRABILITY_CURL_PATH, curl, ["test_id", "object", "formula", "passes_if", "current_result", "activated_component", "valid_for_claim", "generated_utc"])
    write_csv(COMPONENT_FILL_PATH, fill, ["fill_id", "quantity", "formula", "required_columns", "current_status", "acceptance_gate", "valid_for_claim", "generated_utc"])
    write_csv(REPAIR_OPTIONS_PATH, repairs, ["repair_id", "route", "would_do", "current_status", "risk", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_MATRIX_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, certificate, curl, fill, repairs, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"770 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
