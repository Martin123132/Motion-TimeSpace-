from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "771-Y5-R10-theta-Qtau-current-owner-or-deltaH-component-source-row.md"
NEXT_TARGET = "772-Y5-R10-hybrid-EH-quotient-current-owner-or-deltaH-curl-source-fill.md"
STATUS = "Y5_R10_771_theta_Qtau_current_owner_attempted_hybrid_route_selected_deltaH_source_row_staged_nonclaim"
CLAIM_CEILING = "theta_Qtau_current_owner_audit_and_deltaH_source_row_schema_only_no_HPiM_integrability_no_Newton_no_PPN_no_R10_R11_or_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_771_SOURCE_REGISTER.csv"
CURRENT_OWNER_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv"
ROUTE_COMPARISON_PATH = RESIDUALS / "P8_Y5_R10_771_CURRENT_OWNER_ROUTE_COMPARISON.csv"
NOETHER_EXTRACTION_TEST_PATH = RESIDUALS / "P8_Y5_R10_771_NOETHER_EXTRACTION_TEST.csv"
DELTAH_SOURCE_ROW_PATH = RESIDUALS / "P8_Y5_R10_771_DELTAH_COMPONENT_SOURCE_ROW_SCHEMA.csv"
DECISION_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_771_DECISION_MATRIX.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_771_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_771_VALIDATION.csv"

CANDIDATE_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_771_THETA_QTAU_OWNER_CERTIFICATE_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_771_DELTAH_CURL_SOURCE_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_771_HYBRID_CURRENT_OWNER_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_771_QX_BOUNDARY_SOURCE_INPUT_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    CURRENT_OWNER_AUDIT_PATH,
    ROUTE_COMPARISON_PATH,
    NOETHER_EXTRACTION_TEST_PATH,
    DELTAH_SOURCE_ROW_PATH,
    DECISION_MATRIX_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCES: dict[str, dict[str, Any]] = {
    "770_doc": {
        "path": POST_CHECKPOINT / "770-Y5-R10-Hamiltonian-integrability-parent-action-clause-or-FB5540-component-fill.md",
        "needles": [
            "theta_total and Q_tau^MTS are not yet extracted from one explicit parent Lagrangian/current",
            "771-Y5-R10-theta-Qtau-current-owner-or-deltaH-component-source-row.md",
        ],
        "role": "immediate handoff selecting theta/Q_tau owner",
    },
    "770_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_770_VALIDATION.csv",
        "needles": ["V770_9_next_target_selected", "pass"],
        "role": "prior 770 validation guard",
    },
    "770_certificate": {
        "path": RESIDUALS / "P8_Y5_R10_770_PARENT_ACTION_CERTIFICATE_AUDIT.csv",
        "needles": ["HIC770_1_variation_owner", "HIC770_8_certificate_verdict"],
        "role": "parent-action certificate audit",
    },
    "770_curl": {
        "path": RESIDUALS / "P8_Y5_R10_770_INTEGRABILITY_CURL_TEST.csv",
        "needles": ["ICT770_1_curl_identity", "ICT770_5_curl_verdict"],
        "role": "integrability curl test",
    },
    "663_doc": {
        "path": POST_CHECKPOINT / "663-Y5-R10-minimal-parent-action-source-current-Euler-Ward-test-or-residual-input-fill.md",
        "needles": ["Euler/Ward route survives as real mathematics", "Pi_M := Pi_M^H"],
        "role": "minimal parent action Euler/Ward route",
    },
    "664_doc": {
        "path": POST_CHECKPOINT / "664-Y5-R10-Hamiltonian-PiM-integrability-source-equality-or-first-residual-fill.md",
        "needles": ["delta H_tau = int_S(delta Q_tau - i_tau theta)", "missing explicit theta/Q_tau/B_ref/tau lock"],
        "role": "Hamiltonian PiM integrability blocker",
    },
    "667_doc": {
        "path": POST_CHECKPOINT / "667-Y5-R10-explicit-parent-boundary-action-ansatz-and-variation-ledger.md",
        "needles": ["delta H_tau[S] = int_S(delta Q_tau^MTS - i_tau Theta_total)", "Theta", "Q_tau"],
        "role": "explicit parent boundary action ansatz",
    },
    "667_term_map": {
        "path": RESIDUALS / "P8_Y5_R10_667_FB5540_TERM_MAP.csv",
        "needles": ["TM667_0_delta_H_tau", "retained_until_L_X_and_B_total_are_varied"],
        "role": "FB5540 term map",
    },
    "728_doc": {
        "path": POST_CHECKPOINT / "728-Y5-R10-parent-Omega-and-DC-operator-fill-or-edge-row-source-input.md",
        "needles": ["formula progress, not certificate", "theta/Omega"],
        "role": "Omega/DC operator fill",
    },
    "728_ownership": {
        "path": RESIDUALS / "P8_Y5_R10_728_PARENT_OWNERSHIP_BLOCKER.csv",
        "needles": ["theta", "Omega"],
        "role": "parent ownership blockers for Omega/DC chain",
    },
    "729_doc": {
        "path": POST_CHECKPOINT / "729-Y5-R10-fill-PJ-parent-origin-or-source-backed-edge-coefficients.md",
        "needles": ["j_X = theta_Y(v_X) - mu_X", "contract sharpened, not closed"],
        "role": "P/J parent-origin current contract",
    },
    "729_noether": {
        "path": RESIDUALS / "P8_Y5_R10_729_NOETHER_PJ_ORIGIN_FORMULA.csv",
        "needles": ["NPJ729_2_Noether_current", "NPJ729_6_current_verdict"],
        "role": "Noether P/J origin formula",
    },
    "730_doc": {
        "path": POST_CHECKPOINT / "730-Y5-R10-parent-Lagrangian-theta-vX-minimal-fill-or-edge-coefficients.md",
        "needles": ["Parent data needed: L_parent, theta_Y, mu_X, v_X", "templates written, proof not closed"],
        "role": "parent Lagrangian theta/vX route comparison",
    },
    "730_candidates": {
        "path": RESIDUALS / "P8_Y5_R10_730_MINIMAL_PARENT_FILL_CANDIDATES.csv",
        "needles": ["MPF730_C_hybrid_EH_plus_quotient_extra", "MPF730_E_affine_Vdef_block"],
        "role": "minimal parent fill route candidates",
    },
    "730_theta_forms": {
        "path": RESIDUALS / "P8_Y5_R10_730_THETA_MU_VX_FORMS.csv",
        "needles": ["TMV730_0_EH_theta", "TMV730_2_quotient_vertical_theta"],
        "role": "theta/mu/vX form templates",
    },
    "759_doc": {
        "path": POST_CHECKPOINT / "759-Y5-R10-coupling-owner-action-or-residual-vector-acquisition-runner.md",
        "needles": ["coupling owner action is not parent-signed yet", "quotient matter descent clause"],
        "role": "coupling owner action blocker",
    },
    "760_doc": {
        "path": POST_CHECKPOINT / "760-Y5-R10-quotient-matter-descent-or-coupling-residual-source-pack.md",
        "needles": ["quotient matter descent is not parent-signed", "`c_g=0` is not claimed"],
        "role": "quotient matter descent blocker",
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


def current_owner_audit_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "TQ771_0_parent_variation",
            "needed_object": "explicit L_parent and theta_total",
            "owner_test": "delta L_parent=E_A delta Phi^A+dTheta_total",
            "current_result": "template_available_not_filled",
            "blocker": "no single explicit current-chain L_parent with EH, matter, extra, boundary, and coupling sectors all varied",
            "claim_effect_if_closed": "delta_H_tau curl becomes evaluable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "TQ771_1_Noether_current",
            "needed_object": "J_tau and Q_tau^MTS",
            "owner_test": "J_tau=Theta_total(Phi,L_tau Phi)-i_tau L_parent=dQ_tau^MTS+C_tau",
            "current_result": "formal_shape_available_not_certificate",
            "blocker": "Q_X, C_tau, C_extra, C_boundary, C_ref not extracted for retained sectors",
            "claim_effect_if_closed": "Q_tau^MTS becomes a candidate physical Hamiltonian source charge",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "TQ771_2_PJ_not_independent",
            "needed_object": "P and J_eff from one current",
            "owner_test": "j_X=theta_Y(v_X)-mu_X = X_nu J_eff^nu + (nabla_mu X_nu)P^{mu nu}+dB",
            "current_result": "discipline_gate_installed",
            "blocker": "P and J_eff cannot be inserted independently; theta_Y, mu_X, v_X still missing for current MTS",
            "claim_effect_if_closed": "links DC_X/C_X operator rows to a real parent current",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "TQ771_3_tau_action",
            "needed_object": "tau action on every parent field",
            "owner_test": "L_tau Phi^A is defined for metric, matter, X/representative, boundary/reference fields before readout",
            "current_result": "blocked_by_tau_owner_chain",
            "blocker": "observed tau is not parent-owned; source/charge/clock/boundary/orbit roles remain split",
            "claim_effect_if_closed": "removes tau-choice ambiguity from delta H_tau curl",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "TQ771_4_boundary_reference",
            "needed_object": "B_ref and boundary representative inside the same current",
            "owner_test": "Theta_total includes delta B_ref and boundary improvements with fixed derivative-silent reference",
            "current_result": "not_parent_owned",
            "blocker": "boundary class, edge charge, and reference subtraction still have residual branches",
            "claim_effect_if_closed": "prevents Q_tau from shifting under counterterm/reference choices",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "TQ771_5_matter_coupling",
            "needed_object": "ordinary matter/coupling descent in the same L_parent",
            "owner_test": "matter, constants, charge normalization, measure/coframe/connection descend through q(Phi)",
            "current_result": "blocked_by_759_767",
            "blocker": "WEP/no-alpha/common geometry remains closure, not parent-signed descent",
            "claim_effect_if_closed": "prevents Hamiltonian current proof from hiding ordinary-coupling leaks",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "TQ771_6_owner_verdict",
            "needed_object": "theta_total/Q_tau current owner",
            "owner_test": "TQ771_0 through TQ771_5 pass together",
            "current_result": "not_accepted_current_corpus",
            "blocker": "current owner remains a scaffold; delta_H_tau source row must be staged",
            "claim_effect_if_closed": "would reactivate FB5540 theorem-zero path",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_comparison_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "COR771_A_EH_only",
            "route": "observed EH current only",
            "theta_Qtau_supply": "theta_EH and Q_EH are standard if local exterior is EH with fixed boundary",
            "why_not_enough": "does not own X/edge/coupling sectors; risks declaring the extra theory silent by omission",
            "current_rank": "useful_reference_not_full_owner",
            "next_action": "keep as EH baseline inside hybrid route",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "COR771_B_strict_quotient_zero",
            "route": "strict quotient-zero current",
            "theta_Qtau_supply": "theta(v_X)=0 or exact, Q_X=0 if all dangerous variables are quotient-vertical before variation",
            "why_not_enough": "pi, matter blindness, no-marker constants, boundary charge zero, and constraint algebra are not jointly built",
            "current_rank": "lowest_scrutiny_if_proved_but_not_proved",
            "next_action": "only promote if quotient map and coupling descent become parent-signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "COR771_C_hybrid_EH_quotient_extra",
            "route": "EH observed current plus quotient-silent extra local directions",
            "theta_Qtau_supply": "Q_tau^MTS=Q_EH+Q_boundary with Q_X=0/exact for representative-only verticals",
            "why_not_enough": "observed/representative split, no double-counting, coupling descent, and boundary silence remain unsigned",
            "current_rank": "best_next_derivation_route",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "COR771_D_fixed_point_double_zero",
            "route": "fixed-point/double-zero residual control",
            "theta_Qtau_supply": "theta_extra has no linear leakage at Phi0 if source-free positive operator and boundary no-hair hold",
            "why_not_enough": "F1=0/double-zero mechanism, source silence, and transition scale remain not parent-derived",
            "current_rank": "fallback_residual_control_not_GR_derivation",
            "next_action": "keep as bounded residual route if hybrid quotient route fails",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "COR771_E_affine_PJ_insert",
            "route": "affine P/J insertion",
            "theta_Qtau_supply": "P and J appear by construction",
            "why_not_enough": "rejected because it inserts the desired current rather than deriving it from theta_Y(v_X)-mu_X",
            "current_rank": "rejected_painted_door",
            "next_action": "do not use as derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def noether_extraction_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "test_id": "NET771_0_parent_variation",
            "extraction_test": "derive theta_Y from L_parent",
            "formula": "delta L_parent=E_A delta Y^A+dtheta_Y(delta Y)",
            "current_status": "missing_explicit_current_chain_L_parent",
            "if_passes": "enables j_tau and j_X extraction",
            "if_fails": "delta_H_tau row remains MISSING_PARENT_THETA_QTAU",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "NET771_1_tau_current",
            "extraction_test": "derive Q_tau from diffeomorphism current",
            "formula": "j_tau=theta_Y(L_tau Y)-i_tau L_parent=dQ_tau^MTS+C_tau",
            "current_status": "conditional_shape_no_current_owner",
            "if_passes": "Q_tau^MTS can enter M_H_ref and FB5540 curl",
            "if_fails": "M_H_ref and delta_H_tau remain source-row targets",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "NET771_2_X_current",
            "extraction_test": "derive P/J/Q_X from vertical or representative current",
            "formula": "j_X=theta_Y(v_X)-mu_X=X_nu J_eff^nu+(nabla_mu X_nu)P^{mu nu}+dB",
            "current_status": "formula_available_split_not_extracted",
            "if_passes": "C_X and boundary/edge flux become parent-owned",
            "if_fails": "boundary flux and q_loc/edge rows remain residuals",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "NET771_3_improvement_boundary",
            "extraction_test": "fix B/improvement ambiguity",
            "formula": "Q_tau^MTS and Q_X invariant under allowed dB improvements after B_ref/counterterm convention fixed",
            "current_status": "reference_boundary_not_fixed",
            "if_passes": "prevents arbitrary current improvement from shifting FB5540",
            "if_fails": "Delta_ref and symplectic_boundary_flux stay open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "NET771_4_verdict",
            "extraction_test": "accept theta_total/Q_tau owner",
            "formula": "NET771_0..NET771_3 all pass",
            "current_status": "fail_current_corpus",
            "if_passes": "FB5540 curl can be evaluated as theorem problem",
            "if_fails": "write delta_H_tau component source-row schema",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def deltaH_source_row_schema(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DHS771_0_deltaH_curl",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "definition": "abs((delta_1 delta_2-delta_2 delta_1)H_tau)/M_H_ref",
            "required_columns": "system_id;surface_id;variation_pair;curl_value;M_H_ref;units;frame;tau_id;source_path;assumptions;valid_for_claim",
            "current_status": "schema_only_missing_parent_current_or_numeric_source",
            "claim_gate": "theorem-zero or source-backed dimensionless curl bound; no cancellation with Delta_ref/boundary terms",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "row_id": "DHS771_1_theta_Qtau_certificate",
            "quantity": "theta_total_Qtau_owner_certificate",
            "definition": "explicit L_parent, theta_total, J_tau, Q_tau, C_tau, B_ref, tau action, and boundary convention",
            "required_columns": "sector;L_term;theta_term;Q_tau_term;C_tau_term;boundary_term;tau_action;owner_status;source_path;valid_for_claim",
            "current_status": "schema_only_missing_certificate",
            "claim_gate": "all sectors have owner_status=parent_signed or explicitly residualized",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "row_id": "DHS771_2_QX_boundary_piece",
            "quantity": "Q_X_boundary_or_exact_piece",
            "definition": "extra/representative sector contribution to Q_tau or proof it is exact/proper/zero",
            "required_columns": "sector;Q_X;exact_or_proper_status;boundary_class;edge_charge;source_path;valid_for_claim",
            "current_status": "schema_only_missing_QX_owner",
            "claim_gate": "Q_X zero/exact theorem or source-backed boundary contribution",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D771_0_current_owner_not_accepted",
            "decision": "do not accept theta_total/Q_tau current owner for current MTS",
            "reason": "all candidate routes still miss at least one parent-owned sector, boundary/reference, tau, or coupling clause",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D771_1_select_hybrid_route",
            "decision": "select hybrid EH plus quotient-silent extra route as next derivation attempt",
            "reason": "it preserves the known GR current while forcing MTS extra local directions to prove exact/proper/quotient silence instead of pretending they vanish",
            "claim_status": "next_target_selected_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D771_2_stage_deltaH_source_schema",
            "decision": "stage delta_H_tau source-row schema as fallback",
            "reason": "if hybrid current ownership fails, the curl must become a source-backed residual row",
            "claim_status": "schema_only",
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
            "main_result": "theta_total/Q_tau current ownership is not accepted for current MTS; the hybrid EH plus quotient-silent extra route is the best next derivation attempt",
            "hard_blocker": "no single parent current currently extracts theta_total, Q_tau^MTS, Q_X, boundary improvements, tau action, and coupling descent together",
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
    routes: list[dict[str, Any]],
    tests: list[dict[str, Any]],
    source_schema: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_770_clean = all(validation_clean(number) for number in range(665, 771))
    current_owner_rejected = any(row["audit_id"] == "TQ771_6_owner_verdict" and row["current_result"] == "not_accepted_current_corpus" for row in audit)
    hybrid_selected = any(row["route_id"] == "COR771_C_hybrid_EH_quotient_extra" and row["current_rank"] == "best_next_derivation_route" for row in routes)
    noether_tests_written = any(row["test_id"] == "NET771_4_verdict" and row["current_status"] == "fail_current_corpus" for row in tests)
    deltaH_schema_ready = len(source_schema) >= 3 and any(row["row_id"] == "DHS771_0_deltaH_curl" for row in source_schema)
    candidate_artifacts_not_faked = all(not path.exists() for path in CANDIDATE_ARTIFACTS)
    all_nonclaim = all_claim_rows_false([sources, audit, routes, tests, source_schema, decisions, summary])
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D771_1_select_hybrid_route" for row in decisions)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V771_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V771_1_source_needles_present", source_needles_present, "all local source needles present"),
        ("V771_2_prior_665_770_clean", prior_665_770_clean, "665-770 validation rows have no failures"),
        ("V771_3_current_owner_rejected", current_owner_rejected, "theta/Q_tau owner not promoted"),
        ("V771_4_hybrid_route_selected", hybrid_selected, "hybrid EH plus quotient-silent extra route selected"),
        ("V771_5_noether_tests_written", noether_tests_written, "Noether extraction tests written"),
        ("V771_6_deltaH_schema_ready", deltaH_schema_ready, "delta_H_tau source-row schema staged"),
        ("V771_7_candidate_artifacts_not_faked", candidate_artifacts_not_faked, "no claim-input artifacts fabricated"),
        ("V771_8_no_claim_rows_promoted", all_nonclaim, "all generated rows valid_for_claim=false"),
        ("V771_9_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V771_10_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V771_11_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V771_12_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    tests: list[dict[str, Any]],
    source_schema: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 771 - Y5 R10 Theta/Qtau Current Owner Or deltaH Component Source Row

Start point: 770 showed that the parent-action integrability certificate cannot be signed until `theta_total` and `Q_tau^MTS` are extracted from one explicit parent Lagrangian/current.

Current result: **the current owner is not accepted for current MTS**. The known GR/EH current is useful, and the P/J Noether discipline is sharp, but no route yet extracts `theta_total`, `Q_tau^MTS`, `Q_X`, boundary improvements, tau action, and coupling descent together. The best next derivation route is the hybrid one: keep the observed EH current for the GR sector, then prove every MTS extra local direction is quotient-silent/exact/proper or explicitly residualized.

## Status

| field | value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | {summary[0]["main_result"]} |
| Hard blocker | `{summary[0]["hard_blocker"]}` |
| Next target | `{NEXT_TARGET}` |

## Theta/Qtau Current Owner Audit

{markdown_table(audit, ["audit_id", "needed_object", "owner_test", "current_result", "blocker", "claim_effect_if_closed", "valid_for_claim"])}

## Current Owner Route Comparison

{markdown_table(routes, ["route_id", "route", "theta_Qtau_supply", "why_not_enough", "current_rank", "next_action", "valid_for_claim"])}

## Noether Extraction Test

{markdown_table(tests, ["test_id", "extraction_test", "formula", "current_status", "if_passes", "if_fails", "valid_for_claim"])}

## deltaH Component Source Row Schema

{markdown_table(source_schema, ["row_id", "quantity", "definition", "required_columns", "current_status", "claim_gate", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is not a collapse; it is a narrowing. The EH current exists as a known mathematical spine, but MTS only gets to use it for local GR if the extra local directions are shown not to add physical charge/current/edge/coupling terms. The hybrid route is therefore the fairest next shot: inherit the EH current where it is truly observed-GR, and make the MTS extra part prove quotient silence rather than hiding in symbols. If that fails, `delta_H_tau_nonintegrable_over_MH` becomes a sourced residual row.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    audit = current_owner_audit_rows(generated_utc)
    routes = route_comparison_rows(generated_utc)
    tests = noether_extraction_rows(generated_utc)
    source_schema = deltaH_source_row_schema(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, audit, routes, tests, source_schema, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(CURRENT_OWNER_AUDIT_PATH, audit, ["audit_id", "needed_object", "owner_test", "current_result", "blocker", "claim_effect_if_closed", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_COMPARISON_PATH, routes, ["route_id", "route", "theta_Qtau_supply", "why_not_enough", "current_rank", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(NOETHER_EXTRACTION_TEST_PATH, tests, ["test_id", "extraction_test", "formula", "current_status", "if_passes", "if_fails", "valid_for_claim", "generated_utc"])
    write_csv(DELTAH_SOURCE_ROW_PATH, source_schema, ["row_id", "quantity", "definition", "required_columns", "current_status", "claim_gate", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_MATRIX_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, audit, routes, tests, source_schema, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"771 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
