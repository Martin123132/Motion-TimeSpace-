from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "754-Y5-R10-q_loc-parent-kernel-signature-or-preferred-frame-source-fill.md"
NEXT_TARGET = "755-Y5-R10-observed-q_loc-Ward-owner-or-alpha3-component-source-pack.md"
STATUS = "Y5_R10_754_parent_kernel_lift_attempt_failed_narrow_zeros_retained_preferred_frame_source_fill_queue_written"
CLAIM_CEILING = "parent_kernel_lift_attempt_and_preferred_frame_source_fill_queue_only_no_fqV_no_Wqalpha3_no_alpha3_PPN_R10_Newton_or_local_GR_pass"
Q_PROXY = 7.432631961576971e-06
ALPHA3_BOUND = 4.0e-20
WF_LIMIT = ALPHA3_BOUND / Q_PROXY
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_754_SOURCE_REGISTER.csv"
NARROW_ZERO_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_754_NARROW_ZERO_LEDGER.csv"
KERNEL_LIFT_PATH = RESIDUALS / "P8_Y5_R10_754_KERNEL_LIFT_ATTEMPT.csv"
PARENT_KERNEL_SIGNATURE_PATH = RESIDUALS / "P8_Y5_R10_754_PARENT_KERNEL_SIGNATURE_CERTIFICATE.csv"
PREFERRED_FRAME_SOURCE_QUEUE_PATH = RESIDUALS / "P8_Y5_R10_754_PREFERRED_FRAME_SOURCE_FILL_QUEUE.csv"
ALPHA3_PRODUCT_STATUS_PATH = RESIDUALS / "P8_Y5_R10_754_ALPHA3_PRODUCT_STATUS.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_754_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_754_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_754_VALIDATION.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "753_doc": {
        "path": POST_CHECKPOINT / "753-Y5-R10-Palpha3-source-pack-or-parent-zero-theorem.md",
        "needles": ["best shot taken, but no claim promoted", "P_flux P_Hodge q_loc = 0", "754-Y5-R10-q_loc-parent-kernel-signature-or-preferred-frame-source-fill.md"],
        "role": "immediate 754 handoff",
    },
    "753_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_753_VALIDATION.csv",
        "needles": ["V753_16_validation_rows_ready", "V753_13_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "753_clause_matrix": {
        "path": RESIDUALS / "P8_Y5_R10_753_ZERO_CLAUSE_SIGNATURE_MATRIX.csv",
        "needles": ["ZCS753_2_q_loc_kernel_or_scalar_even", "missing_component_input_and_flux_projector"],
        "role": "kernel signature blocker",
    },
    "753_gap_ledger": {
        "path": RESIDUALS / "P8_Y5_R10_753_SOURCE_PACK_GAP_LEDGER.csv",
        "needles": ["GAP753_3_parent_kernel_signature", "parent variation showing q_loc vector branch is gauge"],
        "role": "parent-kernel gap handoff",
    },
    "732_pullback_lemma": {
        "path": RESIDUALS / "P8_Y5_R10_732_HYBRID_PULLBACK_LEMMA.csv",
        "needles": ["HPL732_1_q_loc_pullback", "HPL732_2_not_zero"],
        "role": "representative-vertical q_loc pullback lemma",
    },
    "734_first_zero": {
        "path": RESIDUALS / "P8_Y5_R10_734_FIRST_ZERO_ATTEMPT.csv",
        "needles": ["FZA734_0_representative_vertical_q_loc_variation", "derived_narrow_zero_row_conditional"],
        "role": "first narrow zero",
    },
    "735_second_zero": {
        "path": RESIDUALS / "P8_Y5_R10_735_SECOND_ZERO_ATTEMPT.csv",
        "needles": ["SZA735_0_proper_representative_boundary_charge", "derived_second_narrow_zero_row_conditional"],
        "role": "second narrow zero",
    },
    "736_third_zero": {
        "path": RESIDUALS / "P8_Y5_R10_736_THIRD_ZERO_ATTEMPT.csv",
        "needles": ["TZA736_0_direct_representative_matter_marker", "derived_third_narrow_zero_row_conditional"],
        "role": "third narrow zero",
    },
    "737_ward_flux": {
        "path": RESIDUALS / "P8_Y5_R10_737_SOURCE_CURRENT_WARD_FLUX_ATTEMPT.csv",
        "needles": ["WFA737_2_projected_mass_flux_target", "not_derived_for_current_claim"],
        "role": "projected source flux obstruction",
    },
    "738_pim_owner": {
        "path": RESIDUALS / "P8_Y5_R10_738_PIM_OWNER_FORK.csv",
        "needles": ["PIF738_0_topological_absolute_PiM", "best_route_conditional_not_current_MTS_derived"],
        "role": "PiM owner fork",
    },
    "739_extra_mass": {
        "path": RESIDUALS / "P8_Y5_R10_739_EXTRA_MASS_SILENCE_ATTEMPT.csv",
        "needles": ["ESA739_4_current_chain_verdict", "not_derived_for_current_chain"],
        "role": "extra-mass silence failure",
    },
    "746_projection": {
        "path": RESIDUALS / "P8_Y5_R10_746_QLOC_PROJECTION_CONTRACT.csv",
        "needles": ["QPC746_2_alpha3_momentum_flux", "highest_pressure_if_nonzero"],
        "role": "q_loc projection contract",
    },
    "750_component_schema": {
        "path": RESIDUALS / "P8_Y5_R10_750_QLOC_COMPONENT_INPUT_SCHEMA.csv",
        "needles": ["QIN750_3_q_loc_components", "component-resolved q_loc field/profile"],
        "role": "component input schema",
    },
    "750_hodge_schema": {
        "path": RESIDUALS / "P8_Y5_R10_750_HODGE_COMPONENT_RUNNER_SCHEMA.csv",
        "needles": ["HRS750_3_fqV", "blocked_no_Palpha3_or_q_field"],
        "role": "Hodge/f_qV schema",
    },
    "752_requirements": {
        "path": RESIDUALS / "P8_Y5_R10_752_SOURCE_REQUIREMENTS_QUEUE.csv",
        "needles": ["REQ752_0_component_input", "REQ752_1_flux_projector"],
        "role": "preferred-frame source-fill requirements",
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


def narrow_zero_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "zero_id": "NZ754_0_representative_vertical_q_loc",
            "source_zero": "FZA734_0 / HPL732_1",
            "mathematical_content": "L_{v_X^rep} q_loc^nu=0 when Gamma_eff, K_hat, P_loc, nabla factor through Q_obs^hybrid",
            "what_it_kills": "hidden representative-fibre source of q_loc",
            "what_survives": "nonzero observed reduced q_loc tensor on Q_obs^hybrid",
            "kernel_credit": "prunes_rep_source_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "NZ754_1_proper_representative_boundary",
            "source_zero": "SZA735_0 / SZA735_1",
            "mathematical_content": "Q_X^rep[partial U]=0 and Omega_boundary(deltaY,v_X^rep)=0 for proper representative vertical support",
            "what_it_kills": "pure representative edge charge and corner symplectic flux",
            "what_survives": "observed reduced boundary/source-measure flux",
            "kernel_credit": "prunes_rep_boundary_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "NZ754_2_direct_representative_matter_marker",
            "source_zero": "TZA736_0",
            "mathematical_content": "delta_{v_X^rep} S_matter=0 under strict one-coframe/no-marker matter functor",
            "what_it_kills": "direct representative matter/readout marker charge",
            "what_survives": "dressed source mass, C_qmu q_loc projection, PiM/exchange/boundary flux",
            "kernel_credit": "prunes_direct_marker_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "NZ754_3_same_frame_Ward_bridge",
            "source_zero": "WFA737_0 / WFA737_1",
            "mathematical_content": "nabla_mu T_m^{mu nu}=0 and nabla_mu(T_m^{mu nu} tau_nu)=0 if tau is observed Killing/stationary",
            "what_it_kills": "unprojected same-frame matter nonconservation",
            "what_survives": "projected mass flux d(Pi_M J_H), source-normalization, and preferred-frame q_loc projection",
            "kernel_credit": "Ward_bridge_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def kernel_lift_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "lift_id": "KLA754_0_narrow_zeros_to_kernel",
            "target": "P_flux P_Hodge q_loc",
            "attempted_implication": "narrow representative zeros + no-marker matter + Ward bridge => q_loc in alpha3 kernel",
            "result": "fails_current_chain",
            "reason": "all existing zeros act on representative directions or unprojected matter current; alpha3 needs the observed vector/flux component of q_loc",
            "next_action": "prove observed q_loc Ward owner or fill preferred-frame component rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lift_id": "KLA754_1_pullback_not_silence",
            "target": "q_loc^nu=0",
            "attempted_implication": "q_loc is a Q_obs^hybrid pullback => q_loc vanishes",
            "result": "invalid_implication",
            "reason": "a pullback tensor can be vertical-blind and still nonzero on the reduced observed space",
            "next_action": "derive reduced Ward identity for T_GK or keep residual runner active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lift_id": "KLA754_2_boundary_lift",
            "target": "q_H and boundary flux in alpha3 channel",
            "attempted_implication": "proper representative boundary zero => observed boundary/source-measure flux zero",
            "result": "invalid_implication",
            "reason": "proper representative charge zero does not silence Phi_red, matter, source-measure, non-proper edge, or calibration boundary flux",
            "next_action": "derive observed boundary Ward no-flux or source alpha3-equivalent boundary coefficient",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lift_id": "KLA754_3_no_marker_lift",
            "target": "C_qmu q_loc and source-normalization preferred-frame leakage",
            "attempted_implication": "direct representative matter marker zero => full Y5/source q_loc projection zero",
            "result": "invalid_implication",
            "reason": "dressed source charge, PiM projection, exchange terms, and q_loc-to-source units remain open",
            "next_action": "derive C_qmu=0 or fill source-normalization/preferred-frame component map",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lift_id": "KLA754_4_verdict",
            "target": "alpha3_q_loc=0",
            "attempted_implication": "claim theorem-zero from current parent-kernel state",
            "result": "not_claimed",
            "reason": "P_flux P_Hodge q_loc=0 is not parent-signed and no component-resolved q_loc field exists",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def parent_kernel_signature_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "certificate_id": "PKC754_0_parent_bundle_kernel",
            "needed_signature": "Conf_parent -> Q_obs^hybrid is a genuine parent bundle and v_X^rep lies in ker(d pi_h)",
            "pass_condition": "field-by-field map shows v_X^rep changes only R_rep and not O_GR, Phi_red, matter, clocks, or boundary reference class",
            "current_status": "formal_contract_only",
            "blocks": "parent-kernel theorem credit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "certificate_id": "PKC754_1_q_loc_observed_Ward_owner",
            "needed_signature": "T_GK=Gamma_eff g_obs-K_hat is the Hilbert stress of a reduced diffeo-invariant action",
            "pass_condition": "q_loc^nu=P_loc(sum_A E_A nabla^nu Phi_A+B_boundary^nu) with E_A=0 and no flux in compact local vacuum",
            "current_status": "not_derived",
            "blocks": "observed q_loc silence; P_flux kernel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "certificate_id": "PKC754_2_flux_projector_annihilation",
            "needed_signature": "P_flux P_Hodge q_loc=0 in the observed compact local branch",
            "pass_condition": "either q_loc is scalar/even only, or transverse/harmonic/flux components are exact/proper-boundary-silent",
            "current_status": "missing",
            "blocks": "f_qV and alpha3 theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "certificate_id": "PKC754_3_preferred_frame_absence",
            "needed_signature": "no fixed preferred vector/domain/projector stress survives in parent/readout action through PPN order",
            "pass_condition": "R11 vector family absent/gauge/aligned or all preferred-frame coefficients are source-backed below locks",
            "current_status": "R11_template_only",
            "blocks": "alpha1/alpha2/alpha3/xi local PPN silence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "certificate_id": "PKC754_4_component_source_fallback",
            "needed_signature": "if the theorem fails, q_loc component/source data are real and same-frame normalized",
            "pass_condition": "candidate input has sample/domain, weights, frame, q0..q3, boundary metadata, P_alpha3 or response_operator_id, and source path",
            "current_status": "candidate_input_absent",
            "blocks": "numeric f_qV; W_q_alpha3 product",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "certificate_id": "PKC754_5_verdict",
            "needed_signature": "claim parent-kernel alpha3 silence",
            "pass_condition": "PKC754_0..PKC754_3 signed or PKC754_4 numeric product passes",
            "current_status": "failed_current_corpus",
            "blocks": "alpha3/PPN/R10/Newton/local-GR promotion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def preferred_frame_source_queue_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "input_id": "PFS754_0_q_loc_component_candidate",
            "needed_input": "component-resolved q_loc candidate file",
            "minimum_columns": "sample_id;domain_id;weight_dV;frame_convention;q0;q1;q2;q3;boundary_condition;source_file",
            "theorem_alternative": "derive q_loc observed Ward zero or P_flux P_Hodge q_loc=0",
            "current_status": "missing",
            "blocks": "P_Hodge; f_qV",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "PFS754_1_flux_projector",
            "needed_input": "P_flux map from Hodge components to momentum/preferred-frame flux",
            "minimum_columns": "projector_id;domain;boundary_conditions;formula;normalization;units;source_path",
            "theorem_alternative": "prove transverse/harmonic components vanish in compact local branch",
            "current_status": "missing",
            "blocks": "epsilon_q_momentum; f_qV",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "PFS754_2_alpha3_response_operator",
            "needed_input": "G_PPN and Pi_alpha3^PPN in observed gauge",
            "minimum_columns": "operator_id;source_to_g0i_map;PPN_basis;alpha3_extraction;gauge;units;source_path",
            "theorem_alternative": "prove q_loc source is exactly zero before G_PPN",
            "current_status": "missing",
            "blocks": "W_q_alpha3",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "PFS754_3_no_preferred_frame_source_pack",
            "needed_input": "R11/vector-preferred-frame operator-family absence/gauge/alignment proof",
            "minimum_columns": "family;coefficient;zero_route_or_bound;alpha_i_xi_map;source_path;valid_for_claim",
            "theorem_alternative": "parent no-prior-frame theorem through PPN order",
            "current_status": "template_only",
            "blocks": "alpha1;alpha2;alpha3;xi;R11",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "PFS754_4_product_row",
            "needed_input": "no-cancellation alpha3 product row",
            "minimum_columns": "W_q_alpha3;f_qV;q_proxy;alpha3_q;target_bound;source_paths;no_cancellation_flag",
            "theorem_alternative": "derived_zero_certificate for W_q_alpha3*f_qV",
            "current_status": "blocked_until_PFS754_0_to_2_or_zero_theorem",
            "blocks": "alpha3_q_loc score",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def alpha3_product_status_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "product_id": "A3S754_0_q_proxy",
            "quantity": "q_proxy",
            "value": f"{Q_PROXY:.16g}",
            "status": "known_scalar_proxy_only",
            "gate": "not a vector fraction or alpha3 score",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "product_id": "A3S754_1_f_qV",
            "quantity": "f_qV",
            "value": "MISSING_PARENT_KERNEL_SIGNATURE_OR_COMPONENT_INPUT",
            "status": "missing",
            "gate": "must be theorem-zero or component/source-backed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "product_id": "A3S754_2_W_q_alpha3",
            "quantity": "W_q_alpha3",
            "value": "MISSING_PREFERRED_FRAME_RESPONSE_OPERATOR",
            "status": "missing",
            "gate": "must be sourced after PPN gauge/extraction is fixed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "product_id": "A3S754_3_gate",
            "quantity": "abs(W_q_alpha3*f_qV)",
            "value": f"must_be <= {WF_LIMIT:.15g}",
            "status": "retained_not_scoreable",
            "gate": "requires parent-kernel theorem-zero or both numeric factors",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU754_0_allowed",
            "allowed_after_754": "say three narrow representative/no-marker zeros are retained and useful",
            "forbidden_after_754": "say they imply observed q_loc alpha3-kernel silence",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU754_1_allowed",
            "allowed_after_754": "say the lift to P_flux P_Hodge q_loc=0 failed for current corpus",
            "forbidden_after_754": "run alpha3 product evaluator with missing W_q_alpha3 or f_qV",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU754_2_allowed",
            "allowed_after_754": "attack observed q_loc Ward owner next or fill preferred-frame source rows",
            "forbidden_after_754": "hide preferred-frame source inside q_proxy scalar smoke",
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
            "main_result": "kernel lift from narrow representative zeros to observed alpha3 silence fails; source-fill queue written",
            "hard_blocker": "no parent-signed observed q_loc Ward owner and no P_flux P_Hodge q_loc=0 certificate",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    narrow: list[dict[str, Any]],
    lift: list[dict[str, Any]],
    certificates: list[dict[str, Any]],
    queue: list[dict[str, Any]],
    product: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V754_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V754_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all local source needles present"})
    prior_753 = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_753_VALIDATION.csv")
    validation.append({"check_id": "V754_2_prior_753_clean", "result": "pass" if prior_753 and all(row.get("result") == "pass" for row in prior_753) else "fail", "detail": "753 validation has no failures"})
    validation.append({"check_id": "V754_3_narrow_zeros_retained", "result": "pass" if len(narrow) == 4 and all(row["kernel_credit"] != "observed_kernel_zero" for row in narrow) else "fail", "detail": "narrow zeros retained without overclaim"})
    validation.append({"check_id": "V754_4_kernel_lift_failed_cleanly", "result": "pass" if any(row["lift_id"] == "KLA754_4_verdict" and row["result"] == "not_claimed" for row in lift) else "fail", "detail": "alpha3 kernel silence not claimed"})
    validation.append({"check_id": "V754_5_certificate_requires_observed_owner", "result": "pass" if any(row["certificate_id"] == "PKC754_1_q_loc_observed_Ward_owner" and row["current_status"] == "not_derived" for row in certificates) else "fail", "detail": "observed q_loc Ward owner remains missing"})
    validation.append({"check_id": "V754_6_flux_kernel_missing", "result": "pass" if any(row["certificate_id"] == "PKC754_2_flux_projector_annihilation" and row["current_status"] == "missing" for row in certificates) else "fail", "detail": "P_flux P_Hodge q_loc certificate missing"})
    validation.append({"check_id": "V754_7_source_queue_written", "result": "pass" if len(queue) == 5 and all(row["valid_for_claim"] == "false" for row in queue) else "fail", "detail": "preferred-frame source fill queue written"})
    validation.append({"check_id": "V754_8_product_gate_retained", "result": "pass" if any(row["product_id"] == "A3S754_3_gate" and row["status"] == "retained_not_scoreable" for row in product) else "fail", "detail": f"WF_limit={WF_LIMIT:.15g}"})
    all_generated = narrow + lift + certificates + queue + product + routes + summary
    validation.append({"check_id": "V754_9_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_generated) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V754_10_no_local_arena_claim", "result": "pass" if "no_alpha3_PPN_R10_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "alpha3/PPN/R10/Newton/local-GR claims remain blocked"})
    validation.append({"check_id": "V754_11_next_target_selected", "result": "pass" if all(row.get("next_action") == NEXT_TARGET for row in routes) else "fail", "detail": NEXT_TARGET})
    output_paths = [OUTPUT_DOC, SOURCE_REGISTER_PATH, NARROW_ZERO_LEDGER_PATH, KERNEL_LIFT_PATH, PARENT_KERNEL_SIGNATURE_PATH, PREFERRED_FRAME_SOURCE_QUEUE_PATH, ALPHA3_PRODUCT_STATUS_PATH, ROUTE_PATH, SUMMARY_PATH, VALIDATION_PATH]
    validation.append({"check_id": "V754_12_outputs_scoped", "result": "pass" if all(under_post(path) for path in output_paths) else "fail", "detail": "all outputs under post-checkpoint-work"})
    fw_count = formalization_changed_after_cutoff()
    validation.append({"check_id": "V754_13_formalization_workbench_untouched", "result": "pass" if fw_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={fw_count}"})
    validation.append({"check_id": "V754_14_forbids_scalar_hiding", "result": "pass" if any("q_proxy scalar smoke" in row["forbidden_after_754"] for row in routes) else "fail", "detail": "preferred-frame leakage cannot hide in scalar proxy"})
    validation.append({"check_id": "V754_15_route_forbids_missing_product_eval", "result": "pass" if any("missing W_q_alpha3 or f_qV" in row["forbidden_after_754"] for row in routes) else "fail", "detail": "do not run evaluator with missing products"})
    validation.append({"check_id": "V754_16_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    narrow: list[dict[str, Any]],
    lift: list[dict[str, Any]],
    certificates: list[dict[str, Any]],
    queue: list[dict[str, Any]],
    product: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 754 - Y5 R10 q_loc Parent Kernel Signature Or Preferred Frame Source Fill

Start point: 753 made the desired alpha3 kill-switch explicit:

```text
P_flux P_Hodge q_loc = 0
=> f_qV = 0
=> alpha3_q_loc = 0
```

Current result: **the parent-kernel lift fails for the current corpus, but the useful narrow zeros are retained**. We have conditional zeros for representative-vertical variation, proper representative boundary charge, direct representative matter marker, and same-frame Ward stress. Those prune fake/representative channels. They do **not** prove the observed reduced `q_loc` vector/flux component vanishes.

So 754 writes the exact certificate needed to turn the narrow zeros into a real alpha3-kernel theorem, and the fallback source-fill queue if that theorem does not close.

## Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target"])}

## Narrow Zero Ledger

{markdown_table(narrow, ["zero_id", "source_zero", "mathematical_content", "what_it_kills", "what_survives", "kernel_credit", "valid_for_claim"])}

## Kernel Lift Attempt

{markdown_table(lift, ["lift_id", "target", "attempted_implication", "result", "reason", "next_action", "valid_for_claim"])}

## Parent Kernel Signature Certificate

{markdown_table(certificates, ["certificate_id", "needed_signature", "pass_condition", "current_status", "blocks", "valid_for_claim"])}

## Preferred-Frame Source Fill Queue

{markdown_table(queue, ["input_id", "needed_input", "minimum_columns", "theorem_alternative", "current_status", "blocks", "valid_for_claim"])}

## Alpha3 Product Status

{markdown_table(product, ["product_id", "quantity", "value", "status", "gate", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_754", "forbidden_after_754", "next_action", "valid_for_claim"])}

## Local Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is a clean bridge failure, not a collapse. The representative ghosts are mostly boxed in now; the live problem is the observed reduced `q_loc` residual. To get the alpha3 branch off our neck, the next useful target is the Ward-owner route: prove `T_GK` is a reduced Hilbert stress whose on-shell compact-local divergence has no vector/boundary flux. If that fails, we stop hunting the zero and fill the preferred-frame source rows numerically.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    narrow = narrow_zero_rows(generated_utc)
    lift = kernel_lift_rows(generated_utc)
    certificates = parent_kernel_signature_rows(generated_utc)
    queue = preferred_frame_source_queue_rows(generated_utc)
    product = alpha3_product_status_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validate(sources, narrow, lift, certificates, queue, product, routes, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(NARROW_ZERO_LEDGER_PATH, narrow, ["zero_id", "source_zero", "mathematical_content", "what_it_kills", "what_survives", "kernel_credit", "valid_for_claim", "generated_utc"])
    write_csv(KERNEL_LIFT_PATH, lift, ["lift_id", "target", "attempted_implication", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(PARENT_KERNEL_SIGNATURE_PATH, certificates, ["certificate_id", "needed_signature", "pass_condition", "current_status", "blocks", "valid_for_claim", "generated_utc"])
    write_csv(PREFERRED_FRAME_SOURCE_QUEUE_PATH, queue, ["input_id", "needed_input", "minimum_columns", "theorem_alternative", "current_status", "blocks", "valid_for_claim", "generated_utc"])
    write_csv(ALPHA3_PRODUCT_STATUS_PATH, product, ["product_id", "quantity", "value", "status", "gate", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_754", "forbidden_after_754", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, narrow, lift, certificates, queue, product, routes, summary, validation)

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
