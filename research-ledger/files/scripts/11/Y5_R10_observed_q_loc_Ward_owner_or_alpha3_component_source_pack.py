from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "755-Y5-R10-observed-q_loc-Ward-owner-or-alpha3-component-source-pack.md"
NEXT_TARGET = "756-Y5-R10-Gamma-Khat-metric-response-symbol-match-or-q_loc-component-candidate-builder.md"
STATUS = "Y5_R10_755_observed_q_loc_Ward_owner_not_accepted_alpha3_component_source_pack_schema_written_nonclaim"
CLAIM_CEILING = "observed_q_loc_Ward_owner_attempt_and_alpha3_component_source_pack_schema_only_no_fqV_no_Wqalpha3_no_alpha3_PPN_R10_Newton_or_local_GR_pass"
Q_PROXY = 7.432631961576971e-06
ALPHA3_BOUND = 4.0e-20
WF_LIMIT = ALPHA3_BOUND / Q_PROXY
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_755_SOURCE_REGISTER.csv"
WARD_OWNER_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_755_OBSERVED_QLOC_WARD_OWNER_ATTEMPT.csv"
OBSTRUCTION_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_755_GK_SYMBOL_MATCH_OBSTRUCTION_LEDGER.csv"
SOURCE_PACK_SCHEMA_PATH = RESIDUALS / "P8_Y5_R10_755_ALPHA3_COMPONENT_SOURCE_PACK_SCHEMA.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_755_DECISION_MATRIX.csv"
PRODUCT_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_755_ALPHA3_PRODUCT_UPDATE.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_755_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_755_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_755_VALIDATION.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "754_doc": {
        "path": POST_CHECKPOINT / "754-Y5-R10-q_loc-parent-kernel-signature-or-preferred-frame-source-fill.md",
        "needles": ["parent-kernel lift fails", "observed q_loc Ward owner next", "755-Y5-R10-observed-q_loc-Ward-owner-or-alpha3-component-source-pack.md"],
        "role": "immediate 755 handoff",
    },
    "754_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_754_VALIDATION.csv",
        "needles": ["V754_16_validation_rows_ready", "V754_13_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "754_kernel_certificate": {
        "path": RESIDUALS / "P8_Y5_R10_754_PARENT_KERNEL_SIGNATURE_CERTIFICATE.csv",
        "needles": ["PKC754_1_q_loc_observed_Ward_owner", "not_derived"],
        "role": "observed q_loc Ward-owner blocker",
    },
    "754_source_queue": {
        "path": RESIDUALS / "P8_Y5_R10_754_PREFERRED_FRAME_SOURCE_FILL_QUEUE.csv",
        "needles": ["PFS754_0_q_loc_component_candidate", "PFS754_2_alpha3_response_operator"],
        "role": "preferred-frame source fill handoff",
    },
    "754_product": {
        "path": RESIDUALS / "P8_Y5_R10_754_ALPHA3_PRODUCT_STATUS.csv",
        "needles": ["A3S754_3_gate", "retained_not_scoreable"],
        "role": "alpha3 product blocker",
    },
    "733_doc": {
        "path": POST_CHECKPOINT / "733-Y5-R10-reduced-GK-action-owner-or-hybrid-q_loc-residual-runner.md",
        "needles": ["owner contract written, current symbol match failed", "q_loc^nu = P_loc nabla_mu T_GK"],
        "role": "reduced GK owner contract",
    },
    "733_owner_attempt": {
        "path": RESIDUALS / "P8_Y5_R10_733_REDUCED_GK_OWNER_ATTEMPT.csv",
        "needles": ["RGA733_A_hybrid_reduced_scalar_density_owner", "contract_written_not_matched"],
        "role": "reduced owner attempt",
    },
    "733_metric_response": {
        "path": RESIDUALS / "P8_Y5_R10_733_METRIC_RESPONSE_DERIVATION.csv",
        "needles": ["MRD733_1_metric_response", "definition_possible_existing_match_failed"],
        "role": "Gamma/Khat metric-response obstruction",
    },
    "733_ward_gate": {
        "path": RESIDUALS / "P8_Y5_R10_733_WARD_ZERO_GATE.csv",
        "needles": ["WZG733_0_current_symbol_match", "fail_for_current_claim"],
        "role": "Ward zero gate",
    },
    "734_residual_formula": {
        "path": RESIDUALS / "P8_Y5_R10_734_RESIDUAL_FORMULA_LEDGER.csv",
        "needles": ["RFL734_0_reduced_Ward_shape", "contract_shape_retained_not_current_claim"],
        "role": "observed q_loc residual formula",
    },
    "750_component_schema": {
        "path": RESIDUALS / "P8_Y5_R10_750_QLOC_COMPONENT_INPUT_SCHEMA.csv",
        "needles": ["QIN750_3_q_loc_components", "component-resolved q_loc field/profile"],
        "role": "component input schema",
    },
    "750_hodge_schema": {
        "path": RESIDUALS / "P8_Y5_R10_750_HODGE_COMPONENT_RUNNER_SCHEMA.csv",
        "needles": ["HRS750_3_fqV", "blocked_no_Palpha3_or_q_field"],
        "role": "Hodge/f_qV runner schema",
    },
    "752_requirements": {
        "path": RESIDUALS / "P8_Y5_R10_752_SOURCE_REQUIREMENTS_QUEUE.csv",
        "needles": ["REQ752_0_component_input", "REQ752_1_flux_projector", "REQ752_2_green_operator"],
        "role": "source requirements queue",
    },
    "746_projection": {
        "path": RESIDUALS / "P8_Y5_R10_746_QLOC_PROJECTION_CONTRACT.csv",
        "needles": ["QPC746_2_alpha3_momentum_flux", "highest_pressure_if_nonzero"],
        "role": "q_loc alpha3 projection contract",
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
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
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


def under_post(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            count += 1
    return count


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCES.items()
    ]


def ward_owner_attempt_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "WOA755_0_Ward_identity_shape",
            "target": "observed q_loc Ward owner",
            "mathematical_form": "If T_GK^{mu nu}=(-2/sqrt(-g_obs)) delta S_GK^hyb/delta g_obs_mu_nu and S_GK^hyb is reduced-diffeomorphism invariant, then nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi_A + B_boundary^nu.",
            "current_status": "standard_conditional_identity",
            "blocker": "identity only helps after current Gamma_eff/K_hat/P_loc are matched to the reduced action",
            "claim_effect_if_closed": "q_loc^nu=P_loc(sum_A E_A nabla^nu Phi_A+B_boundary^nu)",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "WOA755_1_symbol_match",
            "target": "Gamma_eff and K_hat current-symbol match",
            "mathematical_form": "Gamma_eff=gamma[Q_obs^hybrid] and K_hat=K_gamma metric response including derivative and boundary terms",
            "current_status": "failed_current_chain",
            "blocker": "733/515 record no actual Gamma scalar-density owner and no K_hat metric-response match",
            "claim_effect_if_closed": "T_GK becomes a parent-owned reduced Hilbert stress",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "WOA755_2_on_shell_source_free",
            "target": "E_A=0 compact local vacuum",
            "mathematical_form": "reduced fields entering gamma are on shell and source-free in the compact local exterior",
            "current_status": "not_derived",
            "blocker": "Y5 source-normalization and Y6/extra-stress ledgers remain active",
            "claim_effect_if_closed": "bulk Ward source term vanishes",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "WOA755_3_projector_owner",
            "target": "P_loc ownership and commutation",
            "mathematical_form": "P_loc is parent-owned and can be applied after the Ward identity without hiding unprojected vector/flux components",
            "current_status": "open",
            "blocker": "P_loc/projector algebra and local/readout commutation remain unresolved",
            "claim_effect_if_closed": "projected q_loc zero can inherit the unprojected Ward zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "WOA755_4_boundary_no_flux",
            "target": "B_boundary^nu=0 in compact local branch",
            "mathematical_form": "metric-response integrations by parts and source-measure terms carry no observed compact-local boundary or harmonic flux",
            "current_status": "open",
            "blocker": "proper representative boundary zero does not kill observed reduced boundary/source-measure flux",
            "claim_effect_if_closed": "P_flux P_Hodge q_loc may become theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "WOA755_5_verdict",
            "target": "claim observed q_loc Ward zero",
            "mathematical_form": "WOA755_1..WOA755_4 all close => q_loc=0 or at least P_flux P_Hodge q_loc=0",
            "current_status": "Ward_owner_not_accepted_current_corpus",
            "blocker": "symbol match, source-free Euler terms, P_loc owner, and boundary no-flux are not signed",
            "claim_effect_if_closed": "alpha3 q_loc theorem-zero branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def obstruction_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "obstruction_id": "GKO755_0_Gamma_scalar_density",
            "missing_object": "Gamma_eff scalar-density owner gamma[Q_obs^hybrid]",
            "current_evidence": "contract exists but current symbol match failed",
            "minimum_fix": "define gamma with units, covariance, no representative marker, and source path to current Gamma_eff",
            "blocks": "T_GK Hilbert stress owner",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "GKO755_1_Khat_metric_response",
            "missing_object": "K_hat equals metric response K_gamma",
            "current_evidence": "definition possible, existing match failed",
            "minimum_fix": "derive K_hat from delta(sqrt(-g) gamma)/delta g including derivative and boundary terms",
            "blocks": "Ward divergence identity for current T_GK",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "GKO755_2_Ploc_owner",
            "missing_object": "P_loc parent owner / projector algebra",
            "current_evidence": "projector ownership open in 733 and 754",
            "minimum_fix": "prove P_loc is parent-owned and commutes with local/readout/Hodge split or carry unprojected residual",
            "blocks": "projected q_loc and f_qV theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "GKO755_3_boundary_flux",
            "missing_object": "observed reduced boundary/source-measure flux silence",
            "current_evidence": "only proper representative boundary charge is zero",
            "minimum_fix": "derive B_boundary^nu=0 for observed reduced fields or source alpha3-equivalent boundary coefficient",
            "blocks": "q_H / boundary contribution to P_flux",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "GKO755_4_Y5_Y6_source_terms",
            "missing_object": "source-normalization and extra-stress closure",
            "current_evidence": "Y5/Y6 retained as hard blockers",
            "minimum_fix": "derive zero for source-normalization/extra stress or provide channelwise bounded coefficients",
            "blocks": "source-free Euler premise and PPN/local-GR promotion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def source_pack_schema_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "pack_id": "ACS755_0_q_loc_component_candidate",
            "artifact": "P8_Y5_R10_750_QLOC_COMPONENT_INPUT_CANDIDATE.csv",
            "required_columns": "sample_id;domain_id;weight_dV;frame_convention;q0;q1;q2;q3;boundary_tag;boundary_condition;source_file",
            "claim_gate": "all q components source-backed; no MISSING_*; valid_for_claim can only be true after theorem/source audit",
            "current_status": "missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "ACS755_1_Hodge_flux_projector",
            "artifact": "P8_Y5_R10_755_PFLUX_PROJECTOR_INPUT.csv",
            "required_columns": "projector_id;domain_id;boundary_operator;P_flux_formula;normalization;q_proxy_denominator;units;source_path",
            "claim_gate": "P_flux P_Hodge q_loc is either theorem-zero or computable from sourced component data",
            "current_status": "schema_only_not_written_as_claim_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "ACS755_2_alpha3_response_operator",
            "artifact": "P8_Y5_R10_755_ALPHA3_RESPONSE_OPERATOR_INPUT.csv",
            "required_columns": "operator_id;G_PPN_source_to_g0i;Pi_alpha3_extraction;gauge;frame;units;source_path",
            "claim_gate": "W_q_alpha3 is derived/bounded in same convention as f_qV",
            "current_status": "schema_only_not_written_as_claim_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "ACS755_3_product_row",
            "artifact": "P8_Y5_R10_755_ALPHA3_PRODUCT_INPUT.csv",
            "required_columns": "W_q_alpha3;f_qV;q_proxy;alpha3_q;target_bound;source_paths;no_cancellation_flag;valid_for_claim",
            "claim_gate": f"abs(W_q_alpha3*f_qV) <= {WF_LIMIT:.15g} and abs(alpha3_q)<=4e-20",
            "current_status": "blocked_until_zero_theorem_or_ACS755_0_to_2_filled",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D755_0_Ward_owner",
            "decision": "do not accept observed q_loc Ward owner for current corpus",
            "meaning": "the Ward identity is valid as a conditional route, but current Gamma/Khat/P_loc/boundary/source premises are unsigned",
            "claim_status": "owner_not_accepted",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D755_1_source_pack",
            "decision": "write alpha3 component source-pack schema",
            "meaning": "if 756 cannot close symbol match, the fallback is real component/operator inputs, not scalar proxy smoke",
            "claim_status": "schema_only_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D755_2_next",
            "decision": "attack Gamma/Khat metric-response symbol match next",
            "meaning": "this is the first hinge in the Ward-owner proof; without it q_loc remains an observed residual",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def product_update_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "product_id": "A3U755_0_Ward_zero_route",
            "quantity": "P_flux P_Hodge q_loc",
            "value": "MISSING_OBSERVED_WARD_OWNER",
            "status_after_755": "not_theorem_zero",
            "acceptance": "requires accepted WOA755 owner chain",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "product_id": "A3U755_1_numeric_route",
            "quantity": "W_q_alpha3*f_qV",
            "value": f"must_be <= {WF_LIMIT:.15g}",
            "status_after_755": "source_pack_schema_only",
            "acceptance": "requires ACS755_0..ACS755_3 real rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU755_0_allowed",
            "allowed_after_755": "say observed q_loc Ward-owner theorem has a precise conditional form",
            "forbidden_after_755": "say current MTS has derived q_loc=0 or alpha3_q_loc=0",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU755_1_allowed",
            "allowed_after_755": "use the alpha3 component source-pack schema as a no-fake-data fallback",
            "forbidden_after_755": "treat schema rows as component data or score the product",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU755_2_allowed",
            "allowed_after_755": "target Gamma/Khat metric-response symbol match next",
            "forbidden_after_755": "hide missing symbol match behind the Ward identity",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "observed q_loc Ward owner not accepted; alpha3 component source-pack schema written",
            "hard_blocker": "Gamma_eff/K_hat metric-response symbol match fails before Ward-owner theorem can be promoted",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    ward: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    pack: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    product: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V755_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V755_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all local source needles present"})
    prior_754 = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_754_VALIDATION.csv")
    validation.append({"check_id": "V755_2_prior_754_clean", "result": "pass" if prior_754 and all(row.get("result") == "pass" for row in prior_754) else "fail", "detail": "754 validation has no failures"})
    validation.append({"check_id": "V755_3_Ward_owner_not_accepted", "result": "pass" if any(row["attempt_id"] == "WOA755_5_verdict" and row["current_status"] == "Ward_owner_not_accepted_current_corpus" for row in ward) else "fail", "detail": "observed q_loc Ward owner remains nonclaim"})
    validation.append({"check_id": "V755_4_symbol_match_blocker_explicit", "result": "pass" if any(row["obstruction_id"] == "GKO755_1_Khat_metric_response" for row in obstructions) else "fail", "detail": "Gamma/Khat metric-response blocker retained"})
    validation.append({"check_id": "V755_5_source_pack_schema_written", "result": "pass" if len(pack) == 4 and all(row["valid_for_claim"] == "false" for row in pack) else "fail", "detail": "alpha3 component source-pack schema is nonclaim"})
    validation.append({"check_id": "V755_6_product_gate_retained", "result": "pass" if any(row["product_id"] == "A3U755_1_numeric_route" and row["status_after_755"] == "source_pack_schema_only" for row in product) else "fail", "detail": f"WF_limit={WF_LIMIT:.15g}"})
    all_generated = ward + obstructions + pack + decisions + product + routes + summary
    validation.append({"check_id": "V755_7_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_generated) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V755_8_no_local_arena_claim", "result": "pass" if "no_alpha3_PPN_R10_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "alpha3/PPN/R10/Newton/local-GR claims remain blocked"})
    validation.append({"check_id": "V755_9_next_target_selected", "result": "pass" if all(row.get("next_action") == NEXT_TARGET for row in routes) and all(row.get("next_target") == NEXT_TARGET for row in decisions) else "fail", "detail": NEXT_TARGET})
    output_paths = [OUTPUT_DOC, SOURCE_REGISTER_PATH, WARD_OWNER_ATTEMPT_PATH, OBSTRUCTION_LEDGER_PATH, SOURCE_PACK_SCHEMA_PATH, DECISION_PATH, PRODUCT_UPDATE_PATH, ROUTE_PATH, SUMMARY_PATH, VALIDATION_PATH]
    validation.append({"check_id": "V755_10_outputs_scoped", "result": "pass" if all(under_post(path) for path in output_paths) else "fail", "detail": "all outputs under post-checkpoint-work"})
    fw_count = formalization_changed_after_cutoff()
    validation.append({"check_id": "V755_11_formalization_workbench_untouched", "result": "pass" if fw_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={fw_count}"})
    validation.append({"check_id": "V755_12_schema_not_data", "result": "pass" if all("schema" in row["current_status"] or row["current_status"] == "missing" or row["current_status"].startswith("blocked") for row in pack) else "fail", "detail": "source pack rows are schema/missing only"})
    validation.append({"check_id": "V755_13_route_forbids_Ward_overclaim", "result": "pass" if any("hide missing symbol match" in row["forbidden_after_755"] for row in routes) else "fail", "detail": "Ward identity cannot hide symbol-match failure"})
    validation.append({"check_id": "V755_14_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    ward: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    pack: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    product: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 755 - Y5 R10 Observed q_loc Ward Owner Or Alpha3 Component Source Pack

Start point: 754 showed that representative/no-marker zeros do not by themselves put the observed reduced `q_loc` residual in the alpha3 kernel.

Current result: **the observed `q_loc` Ward-owner route is precise, but not accepted for the current corpus**. The Ward identity is not the weak point; the weak point is the symbol ownership needed before it can be used:

```text
T_GK^{{mu nu}} = Gamma_eff g_obs^{{mu nu}} - K_hat^{{mu nu}}
               ?= (-2/sqrt(-g_obs)) delta S_GK^hyb / delta g_obs_mu_nu
```

Until `Gamma_eff`, `K_hat`, `P_loc`, on-shell reduced fields, and observed boundary flux are signed, `q_loc` remains an observed residual. Therefore 755 writes the no-fake-data alpha3 component source-pack schema as the fallback.

## Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target"])}

## Observed q_loc Ward Owner Attempt

{markdown_table(ward, ["attempt_id", "target", "mathematical_form", "current_status", "blocker", "claim_effect_if_closed", "valid_for_claim"])}

## GK Symbol-Match Obstruction Ledger

{markdown_table(obstructions, ["obstruction_id", "missing_object", "current_evidence", "minimum_fix", "blocks", "valid_for_claim"])}

## Alpha3 Component Source-Pack Schema

{markdown_table(pack, ["pack_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Alpha3 Product Update

{markdown_table(product, ["product_id", "quantity", "value", "status_after_755", "acceptance", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_755", "forbidden_after_755", "next_action", "valid_for_claim"])}

## Local Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is the hinge: the Ward road is mathematically respectable, but it cannot carry the theory until `Gamma_eff` and `K_hat` are proven to be the current reduced Hilbert-stress pair. Next best shot is not another broad sweep; it is the surgical symbol-match gate. If that fails, we stop trying to magic alpha3 away and build the real component/operator input pack.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    ward = ward_owner_attempt_rows(generated_utc)
    obstructions = obstruction_rows(generated_utc)
    pack = source_pack_schema_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    product = product_update_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validate(sources, ward, obstructions, pack, decisions, product, routes, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(WARD_OWNER_ATTEMPT_PATH, ward, ["attempt_id", "target", "mathematical_form", "current_status", "blocker", "claim_effect_if_closed", "valid_for_claim", "generated_utc"])
    write_csv(OBSTRUCTION_LEDGER_PATH, obstructions, ["obstruction_id", "missing_object", "current_evidence", "minimum_fix", "blocks", "valid_for_claim", "generated_utc"])
    write_csv(SOURCE_PACK_SCHEMA_PATH, pack, ["pack_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(PRODUCT_UPDATE_PATH, product, ["product_id", "quantity", "value", "status_after_755", "acceptance", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_755", "forbidden_after_755", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, ward, obstructions, pack, decisions, product, routes, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        print(f"wrote {OUTPUT_DOC}")
        print(f"wrote {VALIDATION_PATH}")
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()
