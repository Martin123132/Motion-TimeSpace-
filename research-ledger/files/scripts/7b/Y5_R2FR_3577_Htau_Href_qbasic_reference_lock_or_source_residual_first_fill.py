from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3577-Y5-R2FR-Htau-Href-qbasic-reference-lock-or-source-residual-first-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_HTAU_HREF_REFERENCE_LOCK_3577"
CHECKPOINT_ID = "3577"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty CSV requested: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def sources() -> dict[str, Path]:
    return {
        "handoff_3576": RESIDUALS / "P8_Y5_R2FR_3576_NEXT_TARGET.csv",
        "adoption_3576": RESIDUALS / "P8_Y5_R2FR_3576_CANDIDATE_PARENT_BRANCH_ADOPTION_PACKET.csv",
        "residual_rows_3576": RESIDUALS / "P8_Y5_R2FR_3576_FIRST_RETAINED_RESIDUAL_ROWS.csv",
        "status_3576": RESIDUALS / "P8_Y5_R2FR_3576_STATUS.csv",
        "pc3400_update_3576": RESIDUALS / "P8_Y5_R2FR_3576_PC3400_3_4_UPDATE.csv",
        "htau_exact_3446": RESIDUALS / "P8_Y5_R2FR_3446_HTAU_EXACT_ONE_FORM_THEOREM.csv",
        "reference_split_3446": RESIDUALS / "P8_Y5_R2FR_3446_REFERENCE_LOCK_SPLIT.csv",
        "denominator_rows_3446": RESIDUALS / "P8_Y5_R2FR_3446_MHREF_DENOMINATOR_BOUND_ROWS.csv",
        "htau_update_3446": RESIDUALS / "P8_Y5_R2FR_3446_PC3400_3_HTAU_UPDATE.csv",
        "descent_audit_3551": RESIDUALS / "P8_Y5_R2FR_3551_HTAU_HREF_DESCENT_CLAUSE_AUDIT.csv",
        "mhref_descent_3551": RESIDUALS / "P8_Y5_R2FR_3551_MHREF_DESCENT_THEOREM.csv",
        "mhref_leakage_3551": RESIDUALS / "P8_Y5_R2FR_3551_MHREF_LEAKAGE_BOUND_PACK.csv",
        "htau_qbasic_3552": RESIDUALS / "P8_Y5_R2FR_3552_HTAU_QBASIC_THEOREM.csv",
        "dxhtau_bounds_3552": RESIDUALS / "P8_Y5_R2FR_3552_DXHTAU_LEAKAGE_BOUND_PACK.csv",
        "partialm_dxhtau_3552": RESIDUALS / "P8_Y5_R2FR_3552_PARTIALM_DXHTAU_BOUND_ROWS.csv",
        "lower_bound_3207": RESIDUALS / "P8_Y5_R2FR_3207_MHREF_DENOMINATOR_LOWER_BOUND_LAW.csv",
        "first_row_3207": RESIDUALS / "P8_Y5_R2FR_3207_MHREF_FIRST_ROW_CANDIDATE.csv",
        "curl_law_3208": RESIDUALS / "P8_Y5_R2FR_3208_HTAU_ONE_FORM_CURL_LAW.csv",
        "reference_curl_3209": RESIDUALS / "P8_Y5_R2FR_3209_REFERENCE_CURL_BOUND_ROW.csv",
        "reference_lock_3427": RESIDUALS / "P8_Y5_R2FR_3427_REFERENCE_LOCK_THEOREM.csv",
        "source_descent": RESIDUALS / "P8_EM_quotient_source_coordinate_descent_certificate.csv",
        "mass_flat_zero": RESIDUALS / "P8_Y5_R2FR_3550_MASS_FLAT_ZERO_PROOF_ATTEMPT.csv",
        "pc3400_lock": RESIDUALS / "P8_Y5_R2FR_3425_PC3400_3_LOCK_AUDIT.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": "3577 H_tau/H_ref q-basic reference-lock input",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def reference_lock_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "REF3577_0_fixed_reference_rule",
            "fixed reference selector",
            "H_ref := H_tau[g_ref,e_ref,tau_ref,S_ref] where g_ref/e_ref/tau_ref/S_ref are selected by the parent branch before source/orbit/PPN scoring.",
            "D_source H_ref=D_readout H_ref=D_orbit H_ref=0 by construction if the selector has no source/readout arguments.",
            "INTERNAL_CANDIDATE_SIGNED_REFERENCE_DERIVATIVE_SILENCE",
            "reference_lock_3427",
        ),
        (
            "REF3577_1_no_GM_laundering",
            "no measured-GM reference import",
            "partial_{GM_obs,M_fit,M_H_ref,kappa_A,composition_A} H_ref=0",
            "The reference is allowed as a background/counterterm choice, not as a post-fit source-normalization knob.",
            "FORBIDDEN_INPUT_RULE_ADOPTED",
            "reference_split_3446",
        ),
        (
            "REF3577_2_surface_class",
            "closed linked surface/reference class",
            "S_outer, S_inner and S_ref remain in one fixed linked boundary class with no source/radius/orbit retuning.",
            "Closed-surface exact improvements integrate to zero, so the Hilbert-identity branch has no B_zero flux debt.",
            "INTERNAL_CANDIDATE_SIGNED_IF_SURFACE_CLASS_FIXED",
            "reference_lock_3427",
        ),
        (
            "REF3577_3_reference_component",
            "reference residual component",
            "epsilon_ref_source := |D_X H_ref|/M_H_ref_lower",
            "In the candidate branch this component is zero; if reference selector is not parent-fixed it remains a residual row.",
            "CANDIDATE_ZERO_OR_RETAINED_ROW",
            "reference_curl_3209",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "lock_id": lock_id,
            "claim_piece": claim_piece,
            "mathematical_form": mathematical_form,
            "derivation": derivation,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for lock_id, claim_piece, mathematical_form, derivation, status, source_key in specs
    ]


def htau_qbasic_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "HTQ3577_0_alpha_definition",
            "Hamiltonian variation one-form",
            "alpha_tau(delta Phi)=int_S(delta Q_tau^MTS-i_tau Theta_MTS(delta Phi))-delta H_ref",
            "Exact conditional definition on a fixed tau/surface/reference branch.",
            "EXACT_CONDITIONAL_DEFINITION",
            "htau_exact_3446",
        ),
        (
            "HTQ3577_1_curl_law",
            "field-space curl law",
            "d_F alpha_tau=-int_S i_tau omega_MTS + C_tau + C_S + C_ref",
            "Candidate fixed reference sets C_ref=0; remaining curl/surface/tau/symplectic terms are not zero-derived.",
            "DERIVED_ACCOUNTING_IDENTITY_REFERENCE_TERM_NARROWED",
            "curl_law_3208",
        ),
        (
            "HTQ3577_2_qbasic_theorem",
            "H_tau q-basic theorem",
            "If alpha_tau is closed and all ingredients factor through q/e_obs/tau, then H_tau=Hbar_tau(q(Phi)).",
            "Then for vertical v_X, D_X H_tau=dHbar_tau(Dq(v_X))=0.",
            "EXACT_CONDITIONAL_THEOREM_NOT_LIVE",
            "htau_qbasic_3552",
        ),
        (
            "HTQ3577_3_MHref_qbasic",
            "M_H_ref q-basic theorem",
            "If H_tau=Hbar_tau(q(Phi)) and H_ref=Hbar_ref(q(Phi)), then M_H_ref=H_tau-H_ref descends through q.",
            "This would kill A_X^M and C_M for certified vertical directions.",
            "EXACT_CONDITIONAL_THEOREM_NOT_LIVE",
            "mhref_descent_3551",
        ),
        (
            "HTQ3577_4_live_blocker",
            "current H_tau/H_ref status",
            "H_ref derivative silence is internally signed; H_tau exactness/q-basicness and positive M_H_ref are not.",
            "So epsilon_Href_lock is narrowed, not closed.",
            "REFERENCE_LOCK_NARROWED_HTAU_DENOMINATOR_RETAINED",
            "htau_update_3446",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "mathematical_form": mathematical_form,
            "derivation": derivation,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for theorem_id, claim_piece, mathematical_form, derivation, status, source_key in specs
    ]


def denominator_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "DEN3577_0_exact_MHref",
            "M_H_ref",
            "M_H_ref := G_ref^-1*(H_tau[S_outer]-H_ref)",
            "mass or energy/G_ref convention",
            "Exact candidate needs finite H_tau, fixed H_ref, constant G_ref, same frame and positive value.",
            "DEFINITION_READY_VALUE_MISSING",
            "lower_bound_3207",
        ),
        (
            "DEN3577_1_lower_bound",
            "M_H_ref_lower",
            "M_H_ref >= M_EH*(1-epsilon_abs), epsilon_abs=sum_i |Delta_i|/(G_ref*M_EH)",
            "same as M_EH",
            "If M_EH>0 and epsilon_abs<1, the denominator is positive without importing orbital GM.",
            "DERIVED_LOWER_BOUND_LAW_COMPONENTS_MISSING",
            "lower_bound_3207",
        ),
        (
            "DEN3577_2_EH_comparator",
            "M_EH",
            "EH/Komar/ADM/Gauss reference mass in the same tau/coframe/source branch",
            "mass",
            "Needed as the positive comparator for the lower-bound route.",
            "SOURCE_BACKED_VALUE_MISSING",
            "first_row_3207",
        ),
        (
            "DEN3577_3_epsilon_abs",
            "epsilon_abs",
            "epsilon_abs := (|Delta_H_curl|+|Delta_ref|+|Delta_tau_surface_frame|+|Delta_symp_boundary|+|Delta_extra|)/(G_ref*M_EH)",
            "dimensionless",
            "Candidate fixed reference makes Delta_ref=0, but other components still need zeroes or bounds.",
            "COMPONENT_ENVELOPE_NARROWED_NOT_FILLED",
            "denominator_rows_3446",
        ),
        (
            "DEN3577_4_acceptance",
            "denominator_acceptance",
            "Accept exact positive M_H_ref or source-backed M_H_ref_lower>0; reject orbital-GM denominator import.",
            "policy",
            "This is the anti-laundering rule for future local tests.",
            "ACCEPTANCE_RULE_ACTIVE",
            "lower_bound_3207",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "denominator_id": denominator_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "condition_or_status": condition,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for denominator_id, symbol, formula, units, condition, status, source_key in specs
    ]


def epsilon_href_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "EHL3577_0_reference_zero",
            "epsilon_ref_source",
            "epsilon_ref_source := |D_X H_ref|/M_H_ref_lower = 0 in fixed-reference candidate branch",
            "dimensionless",
            "CANDIDATE_ZERO_INTERNAL_NONCLAIM",
            "reference_lock_3427",
            "reference/source laundering",
        ),
        (
            "EHL3577_1_Htau_curl",
            "epsilon_Htau_curl",
            "Delta_H_curl_bound/M_H_ref_lower, with Delta_H_curl_bound <= A_F sup_BF|-int_S i_tau omega_MTS + C_tau + C_S|",
            "dimensionless",
            "FORMULA_READY_COMPONENT_INPUTS_MISSING",
            "htau_exact_3446",
            "H_tau path dependence",
        ),
        (
            "EHL3577_2_tau_surface_frame",
            "epsilon_tau_surface_frame",
            "(|C_tau|+|C_S|+|C_frame|)/M_H_ref_lower",
            "dimensionless",
            "MISSING_TAU_SURFACE_FRAME_LOCK_OR_BOUND",
            "denominator_rows_3446",
            "same generator/surface/frame lock",
        ),
        (
            "EHL3577_3_symplectic_boundary",
            "epsilon_symplectic_boundary",
            "|int_S i_tau omega_extra + Delta_symp|/M_H_ref_lower",
            "dimensionless",
            "MISSING_SYMPLECTIC_BOUNDARY_ZERO_OR_BOUND",
            "denominator_rows_3446",
            "non-EH/projector/boundary symplectic flux",
        ),
        (
            "EHL3577_4_qbasic_mass_leak",
            "epsilon_MHref_qbasic",
            "|D_X M_H_ref|/M_H_ref_lower <= (|D_X H_tau|+|D_X H_ref|)/M_H_ref_lower",
            "dimensionless",
            "NARROWED_TO_DX_HTAU_AFTER_REFERENCE_ZERO",
            "mhref_leakage_3551",
            "source-coordinate/q-basic leakage",
        ),
        (
            "EHL3577_5_total",
            "epsilon_Href_lock",
            "epsilon_Href_lock <= epsilon_Htau_curl + epsilon_tau_surface_frame + epsilon_symplectic_boundary + epsilon_MHref_qbasic",
            "dimensionless no-cancellation envelope",
            "FIRST_RETAINED_ROW_FORMULA_READY_VALUES_MISSING",
            "residual_rows_3576",
            "Hamiltonian reference/source denominator lock",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "observable_link": observable,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, symbol, formula, units, status, source_key, observable in specs
    ]


def gates_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        ("GATE3577_0_sources", "source audit", "PASS", "all required 3577 source paths exist"),
        ("GATE3577_1_Href", "fixed H_ref derivative silence", "PASS_INTERNAL_CANDIDATE", "source/readout derivative of H_ref is zero if the parent-fixed reference selector is adopted"),
        ("GATE3577_2_Htau", "H_tau q-basic/exactness", "FAIL_CURRENT_CLAIM", "theta/Q_tau/curl/symplectic/tau/surface terms are not all zero-derived"),
        ("GATE3577_3_MHref_positive", "positive same-frame M_H denominator", "FAIL_CURRENT_CLAIM", "lower-bound law exists but M_EH and Delta_i rows are unfilled"),
        ("GATE3577_4_epsilon_Href", "epsilon_Href_lock first row", "PASS_NONCLAIM", "epsilon_Href_lock now has narrowed formula, units and components"),
        ("GATE3577_5_Newton", "first-order Newton", "PARTIAL_NOT_PROMOTED", "source denominator blocker narrowed but not closed"),
        ("GATE3577_6_local_GR", "local GR/PPN", "FAIL_CURRENT_CLAIM", "PPN/R10/clock/orbital residual vector remains downstream"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths["status_3576"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, detail in specs
    ]


def decisions_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3577_0_reference_signed",
            "sign fixed-reference derivative silence internally",
            "The candidate parent branch may fix H_ref before source/readout, which makes D_source H_ref=0 without laundering GM.",
            "Reference leakage is removed from epsilon_Href_lock in this private branch.",
            "ADOPTED_INTERNAL_NONCLAIM",
            "reference_lock_3427",
        ),
        (
            "DEC3577_1_Htau_not_signed",
            "do not sign H_tau exactness yet",
            "The one-form theorem is real but theta/Q_tau/curl/symplectic/tau/surface inputs are not all parent-owned.",
            "H_tau terms stay in the residual envelope.",
            "ADOPTED_GUARDRAIL",
            "htau_exact_3446",
        ),
        (
            "DEC3577_2_denominator_route",
            "use lower-bound route instead of orbital-GM import",
            "M_H_ref positivity can be proved by M_EH*(1-epsilon_abs)>0 if components are bounded, but no current row satisfies it.",
            "Next work should derive/fill M_EH and Delta_i rows rather than using fitted GM.",
            "ADOPTED",
            "lower_bound_3207",
        ),
        (
            "DEC3577_3_next_target",
            "attack H_tau curl/component vector next",
            "With reference derivative silence signed, the leading source-denominator terms are H_tau curl, tau/surface/frame lock and symplectic boundary flux.",
            "3578 should derive or fill the H_tau curl component vector.",
            "NEXT_TARGET_SELECTED",
            "dxhtau_bounds_3552",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "valid_for_claim": False,
        }
        for decision_id, decision, reason, consequence, status, source_key in specs
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "HREF_REFERENCE_DERIVATIVE_SILENCE_SIGNED_INTERNAL_HTAU_DENOMINATOR_RETAINED",
            "strongest_result": "Fixed H_ref derivative silence is internally signed in the single-charge branch, so epsilon_Href_lock is narrowed to H_tau curl, tau/surface/frame, symplectic boundary and q-basic denominator leakage terms.",
            "still_missing": "H_tau exact one-form/curl zero, theta/Q_tau parent extraction, same tau/surface/frame lock, positive M_H_ref lower bound, M_EH and Delta_i component rows, q map/vertical basis, and downstream PPN/local-GR closure",
            "public_claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3577_0",
            "target_doc": "3578-Y5-R2FR-Htau-curl-component-zero-or-first-bound-vector.md",
            "target_script": "scripts/Y5_R2FR_3578_Htau_curl_component_zero_or_first_bound_vector.py",
            "objective": "derive H_tau field-space curl zero for the single-charge branch by extracting theta/Q_tau/symplectic/tau/surface components, or fill the first Delta_H_curl_bound component vector",
            "success_gate": "d_F alpha_tau=0 with parent-owned theta/Q_tau and fixed tau/surface, or source-backed curl component rows with common units",
            "reason": "3577 signed fixed-reference silence; H_tau curl is now the leading denominator blocker",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "Htau_Href_reference_lock",
            "status": "HREF_ZERO_INTERNAL_HTAU_CURL_DENOMINATOR_ROWS_ACTIVE",
            "signed_zero": "D_source H_ref=D_readout H_ref=0 in fixed-reference candidate branch",
            "retained_formula": "epsilon_Href_lock <= epsilon_Htau_curl + epsilon_tau_surface_frame + epsilon_symplectic_boundary + epsilon_MHref_qbasic",
            "positive_denominator_route": "M_H_ref >= M_EH*(1-epsilon_abs)>0 if M_EH>0 and epsilon_abs<1",
            "next_action": "derive/fill H_tau curl component vector",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    reference: list[dict[str, object]],
    htau: list[dict[str, object]],
    denominator: list[dict[str, object]],
    epsilon_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in outputs.items() if key != "validation"}
    validations.append(("VAL3577_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3577 source paths exist"))
    needles = {
        "handoff_3576": "NEXT3576_0",
        "adoption_3576": "ADOPT3576_5_Htau_Href",
        "residual_rows_3576": "FR3576_2_epsilon_Href_lock",
        "status_3576": "SINGLE_CHARGE_BRANCH_INTERNALLY_ADOPTED",
        "pc3400_update_3576": "PCU3576_4_PC3400_3_Htau",
        "htau_exact_3446": "HOT3446_2_exact_denominator_route",
        "reference_split_3446": "RLS3446_1_no_GM_laundering",
        "denominator_rows_3446": "DBR3446_5_epsilon_den_total",
        "htau_update_3446": "PCU3446_0_PC3400_3",
        "descent_audit_3551": "HHD3551_3_Href_qbasic",
        "mhref_descent_3551": "MHD3551_2_vertical_zero",
        "mhref_leakage_3551": "LB3551_3_normalized_mass_leak",
        "htau_qbasic_3552": "HTD3552_1_qbasic_charge_theorem",
        "dxhtau_bounds_3552": "DXH3552_0_total",
        "partialm_dxhtau_3552": "PMDX3552_0_total",
        "lower_bound_3207": "LAW3207_3_positive_lower_bound",
        "first_row_3207": "MH3207_1_lower_bound_candidate",
        "curl_law_3208": "HCL3208_4_bound_route",
        "reference_curl_3209": "RCB3209_0_fixed_reference_zero",
        "reference_lock_3427": "RLT3427_2_reference_derivative_silence",
        "source_descent": "QSC3516_1_MHref_descent",
        "mass_flat_zero": "ZP3550_1_MHref_qbasic",
        "pc3400_lock": "P3L3425_2_reference_lock",
    }
    validations.append(("VAL3577_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected Htau/Href needles found"))
    validations.append(("VAL3577_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3577 output files written"))
    csvs_parse = True
    parse_details: list[str] = []
    for output_id, path in pre_validation_outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            row_count = len(read_csv(path))
            csvs_parse = csvs_parse and row_count > 0
            parse_details.append(f"{output_id}:{row_count}")
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3577_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3577_4_reference_zero_present", any(row["lock_id"] == "REF3577_0_fixed_reference_rule" and "D_source H_ref" in str(row["derivation"]) for row in reference), "fixed-reference derivative silence row present"))
    validations.append(("VAL3577_5_Htau_not_claimed", any(row["theorem_id"] == "HTQ3577_4_live_blocker" and "RETAINED" in str(row["status"]) for row in htau), "H_tau denominator remains retained"))
    validations.append(("VAL3577_6_lower_bound_route_present", any(row["denominator_id"] == "DEN3577_1_lower_bound" and "epsilon_abs" in str(row["formula"]) for row in denominator), "positive denominator lower-bound route present"))
    validations.append(("VAL3577_7_epsilon_Href_formula_present", any(row["row_id"] == "EHL3577_5_total" and "epsilon_Htau_curl" in str(row["formula"]) for row in epsilon_rows), "epsilon_Href_lock narrowed formula present"))
    validations.append(("VAL3577_8_reference_gate_passes_only_internal", any(row["gate_id"] == "GATE3577_1_Href" and row["status"] == "PASS_INTERNAL_CANDIDATE" for row in gates), "H_ref pass is internal candidate only"))
    validations.append(("VAL3577_9_denominator_not_promoted", any(row["gate_id"] == "GATE3577_3_MHref_positive" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "positive denominator remains unclaimed"))
    validations.append(("VAL3577_10_next_target_selected", any(row["decision_id"] == "DEC3577_3_next_target" for row in decisions), "Htau curl next target selected"))
    validations.append(("VAL3577_11_no_claim_flags", all(str(row["valid_for_claim"]).lower() == "false" for row in reference + htau + denominator + epsilon_rows + gates + decisions), "all generated physics rows remain nonclaim"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in reference + htau + denominator + epsilon_rows + gates + decisions)
    validations.append(("VAL3577_12_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = any(FORMALIZATION.rglob("*3577*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3577_13_formalization_workbench_untouched", not formalization_touched, "no 3577 checkpoint output appears in formalization-workbench"))
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passed,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passed, detail in validations
    ]


def write_doc(
    outputs: dict[str, Path],
    reference: list[dict[str, object]],
    htau: list[dict[str, object]],
    denominator: list[dict[str, object]],
    epsilon_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3577 - Htau/Href q-basic reference lock or source residual first fill",
        "",
        "## Verdict",
        "3577 narrows the source-denominator blocker.  In the private single-charge branch, `H_ref` is now treated as a parent-fixed reference selected before source/orbit/PPN readout, so `D_source H_ref=0` and the reference-laundering part of `epsilon_Href_lock` is internally zero.",
        "",
        "But `H_tau` itself is not promoted.  The one-form route is exact only if `alpha_tau` is closed and `Theta_MTS/Q_tau^MTS/tau/surface/symplectic` data are parent-owned.  Those pieces are still retained.",
        "",
        "The resulting first residual row is now sharper: `epsilon_Href_lock <= epsilon_Htau_curl + epsilon_tau_surface_frame + epsilon_symplectic_boundary + epsilon_MHref_qbasic`.  The positive denominator route is also explicit: `M_H_ref >= M_EH(1-epsilon_abs)>0`, but `M_EH` and `Delta_i` rows are still missing.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Reference lock"])
    for row in reference:
        lines.append(f"- `{row['lock_id']}`: {row['mathematical_form']} ({row['status']})")
    lines.extend(["", "## Htau q-basic theorem"])
    for row in htau:
        lines.append(f"- `{row['theorem_id']}`: {row['mathematical_form']} ({row['status']})")
    lines.extend(["", "## Denominator route"])
    for row in denominator:
        lines.append(f"- `{row['denominator_id']}` `{row['symbol']}`: {row['formula']} ({row['status']})")
    lines.extend(["", "## Epsilon Href rows"])
    for row in epsilon_rows:
        lines.append(f"- `{row['row_id']}` `{row['symbol']}`: {row['formula']} ({row['status']})")
    lines.extend(["", "## Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} -> {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target", f"- `{next_target[0]['target_doc']}`", f"- Objective: {next_target[0]['objective']}"])
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    register = source_register(source_paths)
    reference = reference_lock_rows(source_paths)
    htau = htau_qbasic_rows(source_paths)
    denominator = denominator_rows(source_paths)
    epsilon_rows = epsilon_href_rows(source_paths)
    gates = gates_rows(source_paths)
    decisions = decisions_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3577_SOURCE_REGISTER.csv",
        "reference_lock": RESIDUALS / "P8_Y5_R2FR_3577_HREF_REFERENCE_LOCK.csv",
        "htau_qbasic": RESIDUALS / "P8_Y5_R2FR_3577_HTAU_QBASIC_REFERENCE_THEOREM.csv",
        "denominator_route": RESIDUALS / "P8_Y5_R2FR_3577_MHREF_POSITIVE_DENOMINATOR_ROUTE.csv",
        "epsilon_Href_rows": RESIDUALS / "P8_Y5_R2FR_3577_EPSILON_HREF_LOCK_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3577_ACTIVATION_GATES.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3577_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3577_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3577_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_Htau_Href_reference_lock_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3577_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["reference_lock"], reference)
    write_csv(outputs["htau_qbasic"], htau)
    write_csv(outputs["denominator_route"], denominator)
    write_csv(outputs["epsilon_Href_rows"], epsilon_rows)
    write_csv(outputs["activation_gates"], gates)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, reference, htau, denominator, epsilon_rows, gates, decisions)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, reference, htau, denominator, epsilon_rows, gates, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3577 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
