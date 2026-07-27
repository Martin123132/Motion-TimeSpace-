from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3578-Y5-R2FR-Htau-curl-component-zero-or-first-bound-vector.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_HTAU_CURL_COMPONENT_VECTOR_3578"
CHECKPOINT_ID = "3578"


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
        "handoff_3577": RESIDUALS / "P8_Y5_R2FR_3577_NEXT_TARGET.csv",
        "htau_qbasic_3577": RESIDUALS / "P8_Y5_R2FR_3577_HTAU_QBASIC_REFERENCE_THEOREM.csv",
        "epsilon_href_3577": RESIDUALS / "P8_Y5_R2FR_3577_EPSILON_HREF_LOCK_ROWS.csv",
        "status_3577": RESIDUALS / "P8_Y5_R2FR_3577_STATUS.csv",
        "denominator_3577": RESIDUALS / "P8_Y5_R2FR_3577_MHREF_POSITIVE_DENOMINATOR_ROUTE.csv",
        "curl_law_3208": RESIDUALS / "P8_Y5_R2FR_3208_HTAU_ONE_FORM_CURL_LAW.csv",
        "curl_envelope_3208": RESIDUALS / "P8_Y5_R2FR_3208_CURL_COMPONENT_ENVELOPE.csv",
        "omega_bound_3210": RESIDUALS / "P8_Y5_R2FR_3210_OMEGA_CURL_BOUND_FORMULA.csv",
        "omega_zero_3210": RESIDUALS / "P8_Y5_R2FR_3210_ZERO_TO_OMEGA_CURL_THEOREM.csv",
        "curl_first_3447": RESIDUALS / "P8_Y5_R2FR_3447_DELTAH_CURL_FIRST_COMPONENT_ROWS.csv",
        "curl_extra_3448": RESIDUALS / "P8_Y5_R2FR_3448_DELTAH_CURL_EXTRA_COMPONENT_ROW.csv",
        "curl_update_3449": RESIDUALS / "P8_Y5_R2FR_3449_DELTAH_CURL_UPDATE.csv",
        "theta_qtau_status_3447": RESIDUALS / "P8_Y5_R2FR_3447_THETA_QTAU_COMPONENT_STATUS.csv",
        "qtau_decomp_993": RESIDUALS / "P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
        "theta_qtau_rows_1733": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_COMPONENT_ROWS.csv",
        "theta_qtau_leaks_1734": RESIDUALS / "P8_Y5_PARENT_QLOC_1734_THETA_QTAU_LEAK_ROWS.csv",
        "theta_assembly_3553": RESIDUALS / "P8_Y5_R2FR_3553_THETA_ASSEMBLY_THEOREM.csv",
        "theta_leakage_3553": RESIDUALS / "P8_Y5_R2FR_3553_THETA_LEAKAGE_VECTOR.csv",
        "curl_gate_2667": RESIDUALS / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv",
        "curl_audit_2667": RESIDUALS / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_CURL_PROOF_AUDIT.csv",
        "curl_template_2667": RESIDUALS / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_COMPONENT_ROW_TEMPLATE_NONCLAIM.csv",
        "curl_results_2667": RESIDUALS / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_CURL_RUNNER_RESULTS.csv",
        "adoption_3576": RESIDUALS / "P8_Y5_R2FR_3576_CANDIDATE_PARENT_BRANCH_ADOPTION_PACKET.csv",
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
            "role": "3578 H_tau curl component extraction input",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def curl_identity_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "CID3578_0_alpha",
            "Hamiltonian one-form",
            "alpha_tau(delta Phi)=int_S(delta Q_tau^MTS-i_tau Theta_MTS(delta Phi))-delta H_ref",
            "Fixed H_ref from 3577 removes the reference-source derivative from this object, but not the theta/Q_tau curl.",
            "EXACT_INPUT_FROM_3577",
            "htau_qbasic_3577",
        ),
        (
            "CID3578_1_curl",
            "field-space curl",
            "d_F alpha_tau=-int_S i_tau omega_MTS + C_tau + C_S + C_ref",
            "In the 3577 fixed-reference branch, C_ref=0, so the remaining problem is omega_MTS+C_tau+C_S.",
            "DERIVED_IDENTITY_REFERENCE_TERM_ZEROED_INTERNAL",
            "curl_law_3208",
        ),
        (
            "CID3578_2_sector_split",
            "MTS curl sector split",
            "omega_MTS=omega_pub+omega_EM+omega_extra+omega_boundary+omega_projector+omega_selector+omega_memory",
            "The curl is now a sector vector; no cancellation across sectors is allowed.",
            "COMPONENT_SPLIT_DEFINED",
            "theta_qtau_status_3447",
        ),
        (
            "CID3578_3_branch_zeroes",
            "candidate branch zeroes",
            "C_ref=0 and omega_projector^PiMH=0 in the Hilbert-identity single-charge branch",
            "These are inherited from 3576/3577 and must not be double-counted as missing curl components.",
            "INTERNAL_ZEROES_ADOPTED_NONCLAIM",
            "adoption_3576",
        ),
        (
            "CID3578_4_bound_route",
            "no-cancellation curl bound",
            "Delta_H_curl_bound <= A_F sup_BF (I_pub+I_EM+I_extra+I_boundary+I_tau_surface+I_qdescent)",
            "If zero proof fails, every live term gets its own component row with units and source path.",
            "BOUND_VECTOR_ROUTE",
            "curl_envelope_3208",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "identity_id": identity_id,
            "claim_piece": claim_piece,
            "mathematical_form": mathematical_form,
            "derivation": derivation,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for identity_id, claim_piece, mathematical_form, derivation, status, source_key in specs
    ]


def curl_component_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "HCURL3578_0_reference",
            "I_ref",
            "0 in fixed-reference branch",
            "Hamiltonian curl numerator units",
            "SIGNED_INTERNAL_ZERO_FROM_3577",
            "epsilon_href_3577",
            "reference curl/source laundering",
        ),
        (
            "HCURL3578_1_PiM_projector",
            "I_projector_PiMH",
            "0 in Hilbert-identity Pi_M^H branch",
            "Hamiltonian curl numerator units",
            "SIGNED_INTERNAL_ZERO_FROM_3576",
            "adoption_3576",
            "projector/domain stress from Pi_M",
        ),
        (
            "HCURL3578_2_public_EH",
            "I_EH_stationary_boundary",
            "abs(int_S i_tau omega_EH) plus EH boundary flux",
            "Hamiltonian curl numerator units",
            "CONDITIONAL_ZERO_IF_STATIONARY_EH_BOUNDARY_ELSE_BOUND_REQUIRED",
            "curl_envelope_3208",
            "public EH stationary boundary term",
        ),
        (
            "HCURL3578_3_public_matter_EM",
            "I_matter_EM_flux",
            "int_BF | -int_S i_tau(omega_matter+omega_EM) + C_tau^matter + C_tau^EM |",
            "Hamiltonian curl numerator units",
            "PUBLIC_FLUX_BOUND_REQUIRED",
            "curl_first_3447",
            "ordinary matter/EM/radiation flux",
        ),
        (
            "HCURL3578_4_extra_sector",
            "I_extra",
            "abs(int_BF[-int_S i_tau omega_X + C_tau^X + B_X])",
            "Hamiltonian curl numerator units",
            "ZERO_IF_ABSENT_QUOTIENT_OR_VERTICAL_CONSTRAINT_SIGNED_ELSE_BOUND",
            "curl_extra_3448",
            "motion/time/domain/memory/range extra-sector curl",
        ),
        (
            "HCURL3578_5_boundary_corner",
            "I_boundary_corner",
            "abs(boundary/corner/edge contribution to d_F alpha_tau) excluding fixed H_ref derivative",
            "Hamiltonian curl numerator units",
            "BOUNDARY_EXACTNESS_OR_BOUND_REQUIRED",
            "curl_envelope_3208",
            "boundary/corner/edge symplectic flux",
        ),
        (
            "HCURL3578_6_tau_surface",
            "I_tau_surface",
            "abs(C_tau+C_S) from tau generator or linking surface variation",
            "Hamiltonian curl numerator units",
            "TAU_SURFACE_LOCK_OR_BOUND_REQUIRED",
            "curl_envelope_3208",
            "same generator/surface/frame lock",
        ),
        (
            "HCURL3578_7_qdescent_current",
            "I_qdescent_current",
            "epsilon_theta_Qtau_projectability_abs contribution from Dq/tau/current descent failure",
            "declared current-leak units or normalized by M_H_ref_lower",
            "Q_MAP_VERTICAL_BASIS_OR_BOUND_REQUIRED",
            "theta_qtau_leaks_1734",
            "q-basic current/projectability leakage",
        ),
        (
            "HCURL3578_8_total",
            "Delta_H_curl_bound",
            "A_F sup_BF sum_live |I_i| with no cancellation; signed-zero rows omitted from the live sum",
            "Hamiltonian curl numerator units",
            "FORMULA_READY_COMPONENT_VALUES_MISSING",
            "curl_template_2667",
            "H_tau path dependence denominator feed",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "component_id": component_id,
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
        for component_id, symbol, formula, units, status, source_key, observable in specs
    ]


def zero_attempt_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "ZERO3578_0_reference",
            "reference curl",
            "C_ref=0",
            "PASS_INTERNAL",
            "fixed H_ref selected before source/readout in 3577",
            "epsilon_href_3577",
        ),
        (
            "ZERO3578_1_PiM",
            "Pi_M projector curl",
            "omega_projector^PiMH=0 and [d,Pi_M^H]J_H=0",
            "PASS_INTERNAL",
            "Hilbert identity/inclusion branch from 3576",
            "adoption_3576",
        ),
        (
            "ZERO3578_2_EH",
            "EH public curl",
            "I_EH_stationary_boundary=0",
            "CONDITIONAL_ONLY",
            "requires stationary EH exterior and boundary conditions; not full MTS proof",
            "curl_envelope_3208",
        ),
        (
            "ZERO3578_3_public_EM",
            "public matter/EM curl",
            "I_matter_EM_flux=0",
            "NOT_SIGNED",
            "radiation/Poynting/public flux needs no-flux theorem or data",
            "curl_first_3447",
        ),
        (
            "ZERO3578_4_extra",
            "extra-sector curl",
            "I_extra=0",
            "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED",
            "absent-quotient or vertical-constraint theorem exists as route, but not parent activated for every retained sector",
            "curl_update_3449",
        ),
        (
            "ZERO3578_5_boundary_tau_surface",
            "boundary/tau/surface curl",
            "I_boundary_corner+I_tau_surface=0",
            "NOT_SIGNED",
            "requires boundary exactness, same tau, and fixed homology/surface branch",
            "curl_gate_2667",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "zero_id": zero_id,
            "target": target,
            "zero_statement": statement,
            "status": status,
            "reason": reason,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for zero_id, target, statement, status, reason, source_key in specs
    ]


def theta_qtau_update_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "TQU3578_0_EH",
            "Theta_EH;Q_tau^EH",
            "CONDITIONAL_PUBLIC_CONTROL_ANCHOR",
            "kept as public baseline, not total MTS charge",
            "theta_qtau_status_3447",
        ),
        (
            "TQU3578_1_matter_EM",
            "Theta_matter;Theta_EM;C_tau^matter;C_tau^EM",
            "RETAIN_PUBLIC_FLUX_BOUND",
            "feeds I_matter_EM_flux",
            "theta_qtau_status_3447",
        ),
        (
            "TQU3578_2_PiMH",
            "Theta_projector^H;Q_tau_projector^H",
            "ZERO_IN_IDENTITY_BRANCH",
            "do not retain old projector curl in the single-charge branch",
            "theta_qtau_status_3447",
        ),
        (
            "TQU3578_3_extra",
            "Theta_extra;Q_tau^extra;C_tau^extra",
            "RETAIN_COMPONENT_VECTOR",
            "feeds I_extra until absent-quotient/vertical-constraint route is signed or bounded",
            "theta_qtau_status_3447",
        ),
        (
            "TQU3578_4_boundary",
            "Theta_boundary;Q_tau^boundary;corner/exact improvements",
            "RETAIN_BOUNDARY_COMPONENT_EXCEPT_FIXED_HREF",
            "fixed reference derivative is zero, but boundary/corner symplectic flux still needs proof or bound",
            "theta_qtau_rows_1733",
        ),
        (
            "TQU3578_5_total",
            "Theta_MTS;Q_tau^MTS",
            "TOTAL_NOT_PROMOTED_COMPONENT_VECTOR_READY",
            "H_tau exactness remains a bounded component problem",
            "theta_assembly_3553",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "update_id": update_id,
            "component": component,
            "status": status,
            "effect": effect,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for update_id, component, status, effect, source_key in specs
    ]


def gates_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        ("GATE3578_0_sources", "source audit", "PASS", "all required 3578 source paths exist"),
        ("GATE3578_1_reference_projector_zero", "reference/PiM curl zeroes", "PASS_INTERNAL_CANDIDATE", "C_ref and Pi_M^H projector curl are zero in the candidate branch"),
        ("GATE3578_2_component_vector", "curl component vector", "PASS_NONCLAIM", "Delta_H_curl_bound now has live component rows and no-cancellation formula"),
        ("GATE3578_3_total_curl_zero", "d_F alpha_tau=0", "FAIL_CURRENT_CLAIM", "public EM, extra, boundary, tau/surface and qdescent components are not all zero-derived"),
        ("GATE3578_4_units_values", "component units/values", "FAIL_CURRENT_CLAIM", "common units and numeric/theorem component values are missing"),
        ("GATE3578_5_denominator", "M_H_ref denominator", "FAIL_CURRENT_CLAIM", "curl bound feeds denominator lower-bound route but does not close it"),
        ("GATE3578_6_local_GR", "local GR/PPN", "FAIL_CURRENT_CLAIM", "downstream PPN/R10/clock/orbital vector remains open"),
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
            "source_path": str(source_paths["status_3577"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, detail in specs
    ]


def decisions_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3578_0_zeroes_kept",
            "keep only earned curl zeroes",
            "C_ref and Pi_M^H projector curl are zero in the candidate branch; everything else needs proof or rows.",
            "prevents a fake H_tau integrability promotion",
            "ADOPTED",
            "epsilon_href_3577",
        ),
        (
            "DEC3578_1_component_vector",
            "replace generic curl blocker with component vector",
            "The live curl terms are now public EM/matter flux, extra-sector curl, boundary/corner flux, tau/surface mismatch and qdescent current leakage.",
            "next work can attack the largest-looking component instead of repeating 'H_tau curl missing'",
            "ADOPTED",
            "curl_envelope_3208",
        ),
        (
            "DEC3578_2_next_target",
            "attack public EM/Poynting flux first",
            "The user explicitly flagged Poynting/waves, and public EM flux is the least speculative retained curl component compared with hidden extra-sector actions.",
            "3579 should derive public matter/EM no-flux or fill the Poynting/radiation flux bound row.",
            "NEXT_TARGET_SELECTED",
            "curl_first_3447",
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
            "status": "HTAU_CURL_COMPONENT_VECTOR_READY_REFERENCE_AND_PIM_ZEROES_SIGNED_INTERNAL",
            "strongest_result": "The H_tau curl is no longer a generic blocker: C_ref and Pi_M^H projector curl are internally zero, and the live no-cancellation vector is public EM/matter flux, extra-sector curl, boundary/corner flux, tau/surface mismatch, and qdescent current leakage.",
            "still_missing": "public EM/Poynting no-flux or bound, extra-sector theta/omega/Q_tau owner, boundary/corner exactness or bound, same tau/surface lock, q-map/vertical current descent, common units and component values",
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
            "next_id": "NEXT3578_0",
            "target_doc": "3579-Y5-R2FR-public-EM-Poynting-Htau-curl-zero-or-flux-bound.md",
            "target_script": "scripts/Y5_R2FR_3579_public_EM_Poynting_Htau_curl_zero_or_flux_bound.py",
            "objective": "derive public matter/EM no-flux contribution to the H_tau curl in the compact local exterior, or fill the first Poynting/radiation flux bound row with units and source paths",
            "success_gate": "I_matter_EM_flux=0 under stationary/source-free exterior conditions, or source-backed Poynting/radiation flux bound rows",
            "reason": "3578 makes public EM/Poynting flux the least speculative live H_tau curl component",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "Htau_curl_component_vector",
            "status": "COMPONENT_VECTOR_READY_TOTAL_CURL_NOT_ZERO",
            "signed_zeroes": "C_ref=0; I_projector_PiMH=0",
            "live_components": "I_matter_EM_flux;I_extra;I_boundary_corner;I_tau_surface;I_qdescent_current",
            "bound_formula": "Delta_H_curl_bound <= A_F sup_BF sum_live |I_i|",
            "next_action": "derive/bound public EM/Poynting flux component",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    identities: list[dict[str, object]],
    components: list[dict[str, object]],
    zeroes: list[dict[str, object]],
    updates: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in outputs.items() if key != "validation"}
    validations.append(("VAL3578_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3578 source paths exist"))
    needles = {
        "handoff_3577": "NEXT3577_0",
        "htau_qbasic_3577": "HTQ3577_1_curl_law",
        "epsilon_href_3577": "EHL3577_1_Htau_curl",
        "status_3577": "HREF_REFERENCE_DERIVATIVE_SILENCE",
        "denominator_3577": "DEN3577_1_lower_bound",
        "curl_law_3208": "HCL3208_4_bound_route",
        "curl_envelope_3208": "HCURL3208_7_total",
        "omega_bound_3210": "OMG3210_2_omega_integral_bound",
        "omega_zero_3210": "ZOC3210_2_tangent_zero_to_omega_zero",
        "curl_first_3447": "DHC3447_0_public_sector_curl",
        "curl_extra_3448": "DHC3448_0_Delta_H_curl_extra",
        "curl_update_3449": "DHU3449_0_DHC3448_1",
        "theta_qtau_status_3447": "TQS3447_6_total",
        "qtau_decomp_993": "QDEC993_5_total",
        "theta_qtau_rows_1733": "TQC1733_6_total_Qtau",
        "theta_qtau_leaks_1734": "TLR1734_4_total_theta_qtau_leak",
        "theta_assembly_3553": "TSP3553_1_sum_theta_theorem",
        "theta_leakage_3553": "TL3553_0_total",
        "curl_gate_2667": "ICG2667_7_verdict",
        "curl_audit_2667": "HTC2667_7_verdict",
        "curl_template_2667": "HCUR2667_5_absolute_envelope",
        "curl_results_2667": "RUN2667_HTC2667_7_verdict",
        "adoption_3576": "ADOPT3576_3_PiM_identity",
    }
    validations.append(("VAL3578_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected Htau curl component needles found"))
    validations.append(("VAL3578_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3578 output files written"))
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
    validations.append(("VAL3578_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3578_4_reference_PiM_zeroes_present", {"HCURL3578_0_reference", "HCURL3578_1_PiM_projector"}.issubset({str(row["component_id"]) for row in components}), "reference and PiM zero component rows present"))
    validations.append(("VAL3578_5_live_components_present", {"I_matter_EM_flux", "I_extra", "I_boundary_corner", "I_tau_surface", "I_qdescent_current"}.issubset({str(row["symbol"]) for row in components}), "live curl components present"))
    validations.append(("VAL3578_6_total_bound_formula_present", any(row["component_id"] == "HCURL3578_8_total" and "sum_live" in str(row["formula"]) for row in components), "total curl no-cancellation formula present"))
    validations.append(("VAL3578_7_zero_audit_present", any(row["zero_id"] == "ZERO3578_3_public_EM" and row["status"] == "NOT_SIGNED" for row in zeroes), "public EM zero not overclaimed"))
    validations.append(("VAL3578_8_theta_qtau_update_present", any(row["update_id"] == "TQU3578_5_total" and "NOT_PROMOTED" in str(row["status"]) for row in updates), "theta/Qtau total not promoted"))
    validations.append(("VAL3578_9_total_curl_not_claimed", any(row["gate_id"] == "GATE3578_3_total_curl_zero" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "total Htau curl remains unclaimed"))
    validations.append(("VAL3578_10_next_target_selected", any(row["decision_id"] == "DEC3578_2_next_target" for row in decisions), "public EM/Poynting next target selected"))
    validations.append(("VAL3578_11_no_claim_flags", all(str(row["valid_for_claim"]).lower() == "false" for row in identities + components + zeroes + updates + gates + decisions), "all generated physics rows remain nonclaim"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in identities + components + zeroes + updates + gates + decisions)
    validations.append(("VAL3578_12_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = any(FORMALIZATION.rglob("*3578*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3578_13_formalization_workbench_untouched", not formalization_touched, "no 3578 checkpoint output appears in formalization-workbench"))
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
    identities: list[dict[str, object]],
    components: list[dict[str, object]],
    zeroes: list[dict[str, object]],
    updates: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3578 - Htau curl component zero or first bound vector",
        "",
        "## Verdict",
        "3578 turns the `H_tau` integrability problem into a live component vector.  The candidate branch earns two zeroes: `C_ref=0` from fixed `H_ref`, and `I_projector_PiMH=0` from the Hilbert-identity `Pi_M^H` branch.",
        "",
        "The total curl is not zero.  The live vector is `I_matter_EM_flux`, `I_extra`, `I_boundary_corner`, `I_tau_surface`, and `I_qdescent_current`, with no cancellation credit.  The denominator feed is `Delta_H_curl_bound <= A_F sup_BF sum_live |I_i|`.",
        "",
        "Best next target is public EM/Poynting flux because it is a concrete physical channel and less speculative than hidden extra-sector action reconstruction.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Curl identities"])
    for row in identities:
        lines.append(f"- `{row['identity_id']}`: {row['mathematical_form']} ({row['status']})")
    lines.extend(["", "## Component vector"])
    for row in components:
        lines.append(f"- `{row['component_id']}` `{row['symbol']}`: {row['formula']} ({row['status']})")
    lines.extend(["", "## Zero audit"])
    for row in zeroes:
        lines.append(f"- `{row['zero_id']}` `{row['target']}`: {row['status']} ({row['reason']})")
    lines.extend(["", "## Theta/Qtau update"])
    for row in updates:
        lines.append(f"- `{row['update_id']}` `{row['component']}`: {row['status']} -> {row['effect']}")
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
    identities = curl_identity_rows(source_paths)
    components = curl_component_rows(source_paths)
    zeroes = zero_attempt_rows(source_paths)
    updates = theta_qtau_update_rows(source_paths)
    gates = gates_rows(source_paths)
    decisions = decisions_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3578_SOURCE_REGISTER.csv",
        "curl_identities": RESIDUALS / "P8_Y5_R2FR_3578_HTAU_CURL_IDENTITIES.csv",
        "curl_components": RESIDUALS / "P8_Y5_R2FR_3578_HTAU_CURL_COMPONENT_VECTOR.csv",
        "zero_audit": RESIDUALS / "P8_Y5_R2FR_3578_CURL_ZERO_AUDIT.csv",
        "theta_qtau_update": RESIDUALS / "P8_Y5_R2FR_3578_THETA_QTAU_COMPONENT_UPDATE.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3578_ACTIVATION_GATES.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3578_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3578_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3578_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_Htau_curl_component_vector_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3578_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["curl_identities"], identities)
    write_csv(outputs["curl_components"], components)
    write_csv(outputs["zero_audit"], zeroes)
    write_csv(outputs["theta_qtau_update"], updates)
    write_csv(outputs["activation_gates"], gates)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, identities, components, zeroes, updates, gates, decisions)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, identities, components, zeroes, updates, gates, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3578 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
