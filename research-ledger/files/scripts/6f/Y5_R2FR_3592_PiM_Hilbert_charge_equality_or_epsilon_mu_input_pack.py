from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R2FR_Y5_PIM_HILBERT_CHARGE_EQUALITY_3592"
CHECKPOINT_ID = "3592"
DOC = ROOT / "3592-Y5-R2FR-PiM-Hilbert-charge-equality-or-epsilon-mu-input-pack.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sources() -> dict[str, Path]:
    return {
        "next_3591": RESIDUALS / "P8_Y5_R2FR_3591_NEXT_TARGET.csv",
        "status_3591": RESIDUALS / "P8_Y5_R2FR_3591_STATUS.csv",
        "gm_contract_3591": RESIDUALS / "P8_Y5_R2FR_3591_GM_TRANSFER_CONTRACT.csv",
        "epsilon_mu_3591": RESIDUALS / "P8_Y5_R2FR_3591_EPSILON_MU_RESIDUAL_CONTRACT.csv",
        "validation_3591": RESIDUALS / "P8_Y5_BRR545_3591_VALIDATION.csv",
        "charge_direct": RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        "charge_residuals": RESIDUALS / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
        "charge_status": RESIDUALS / "P8_charge_current_equality_STATUS.csv",
        "top_hilbert_attempt": RESIDUALS / "P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv",
        "top_hilbert_obstructions": RESIDUALS / "P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv",
        "top_hilbert_decision": RESIDUALS / "P8_TOPOLOGICAL_HILBERT_EQUALITY_DECISION.csv",
        "parent_source_identity": RESIDUALS / "P8_PARENT_SOURCE_IDENTITY_ATTEMPT.csv",
        "parent_source_residuals": RESIDUALS / "P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv",
        "parent_source_decision": RESIDUALS / "P8_PARENT_SOURCE_IDENTITY_DECISION.csv",
        "noether_theorem": RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_THEOREM.csv",
        "noether_chain": RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
        "noether_terms": RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_C_TERM_LEDGER.csv",
        "source_measure_theorem": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
        "source_measure_residuals": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "source_measure_decision": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_DECISION.csv",
        "worldtube_theorem": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "worldtube_proof": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_PROOF_SKETCH.csv",
        "worldtube_decision": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_DECISION.csv",
        "mass_flux": RESIDUALS / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "hamiltonian_charge": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "mu_extra_vector": RESIDUALS / "P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
        "constant_gm_2583": RESIDUALS / "P8_Y5_SOURCE_NORM_2583_CONSTANT_GM_RESIDUAL_ROWS.csv",
        "branch_3590": RESIDUALS / "P8_Y5_R2FR_3590_BRANCH_VERDICT.csv",
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3592_SOURCE_REGISTER.csv",
        "equality_attempt": RESIDUALS / "P8_Y5_R2FR_3592_PIM_HILBERT_EQUALITY_ATTEMPT.csv",
        "residual_identity": RESIDUALS / "P8_Y5_R2FR_3592_CHARGE_EQUALITY_RESIDUAL_IDENTITY.csv",
        "epsilon_mu_input_pack": RESIDUALS / "P8_Y5_R2FR_3592_EPSILON_MU_INPUT_PACK.csv",
        "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3592_PROMOTION_GATES.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3592_ACTIVATION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3592_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3592_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_PiM_Hilbert_charge_equality_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3592_VALIDATION.csv",
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": "3592 Pi_M/Hilbert charge equality or epsilon_mu input source",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def equality_attempt_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "PHE3592_0_target",
            "B_xi/G_ref = M_H[Pi_M J_H]",
            "the Hamiltonian/asymptotic mass charge equals the parent projected Hilbert source charge",
            "TARGET_EXACT",
            "gm_contract_3591",
        ),
        (
            "PHE3592_1_phase_space_start",
            "delta H_xi = integral_boundary(delta Q_xi - xi dot theta) + retained terms",
            "covariant phase-space route exists if parent Lagrangian, symplectic current, boundary class, and observed xi are owned",
            "CONDITIONAL_NOT_PARENT_DERIVED",
            "charge_direct",
        ),
        (
            "PHE3592_2_PiM_parent_origin",
            "Pi_M: J_H -> mass-flux class before readout",
            "projector must be parent/topological/source-measure owned, not an orbital-GM mask",
            "MISSING_PARENT_PROJECTOR_ORIGIN",
            "mass_flux",
        ),
        (
            "PHE3592_3_variation_equality",
            "delta(B_xi/G_ref) = delta M_H[Pi_M J_H]",
            "would integrate to equality only if symplectic/reference/projector/source leakage vanishes or is universal",
            "NOT_PARENT_DERIVED",
            "charge_direct",
        ),
        (
            "PHE3592_4_topological_Hilbert_route",
            "Pi_M J_H = J_M_top + dB_zero + R_eq",
            "best clean route is to define topological charge from the same Hilbert compact-source charge before readout",
            "BEST_ROUTE_CONDITIONAL_R_EQ_NOT_ZERO",
            "top_hilbert_attempt",
        ),
        (
            "PHE3592_5_source_identity",
            "d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent",
            "closed flux requires zero projected extra-current, zero projector commutator, and no parent anomaly",
            "DECOMPOSITION_DERIVED_NOT_ZERO",
            "parent_source_identity",
        ),
        (
            "PHE3592_6_worldtube_glue",
            "M_source[W] := H_tau[S_outer]-H_tau[reference]",
            "source mass should be dressed Hamiltonian/Noether charge, not bare rest mass",
            "NECESSARY_DEFINITION_CORRECTION_NOT_LOCKED",
            "worldtube_theorem",
        ),
        (
            "PHE3592_7_verdict",
            "Pi_M/Hilbert equality not parent-signed in current corpus",
            "exact residual identity is available, so move to epsilon_mu input pack without Newton/PPN claim",
            "EQUALITY_NOT_DERIVED_RESIDUAL_PACK_ACTIVE",
            "charge_status",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "attempt_id": attempt_id,
            "mathematical_form": form,
            "meaning": meaning,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for attempt_id, form, meaning, status, source_key in rows
    ]


def residual_identity_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("CEI3592_0_Delta_frame", "Delta_frame", "B_xi[e_charge]/G_ref - B_xi[e_obs]/G_ref", "epsilon_frame", "charge_residuals"),
        ("CEI3592_1_Delta_nonEH", "Delta_nonEH", "sum_i c_i Q_i^nonEH/G_ref", "epsilon_operator", "charge_residuals"),
        ("CEI3592_2_Delta_symp", "Delta_symp", "integral_boundary(xi dot theta_extra - delta Q_extra)", "epsilon_extra", "charge_residuals"),
        ("CEI3592_3_Delta_PiM", "Delta_PiM", "M_eff[delta Pi_M J_H] + M_eff[Pi_M J_H - J_M^parent]", "epsilon_PiM", "charge_residuals"),
        ("CEI3592_4_Delta_extra", "Delta_extra", "Pi_M(Q_boundary + Q_bulk + Q_domain + Q_memory + Q_range + Q_connection)", "epsilon_extra", "charge_residuals"),
        ("CEI3592_5_Delta_flux", "Delta_flux", "integral_annulus d(Pi_M J_H)", "epsilon_flux", "charge_residuals"),
        ("CEI3592_6_Delta_G", "Delta_G", "B_xi(1/G_eff - 1/G0) or d ln G_eff", "epsilon_calibration", "charge_residuals"),
        ("CEI3592_7_Delta_cal", "Delta_cal", "M_eff[Pi_M J_H] - M_Gauss_orbital", "epsilon_calibration", "charge_residuals"),
        ("CEI3592_8_Delta_PPN", "Delta_PPN", "leading source equality fails to remain stable at beta/gamma/PPN order", "epsilon_PPN_source", "source_measure_residuals"),
        ("CEI3592_9_Delta_GK", "Delta_GK_source", "K_GK_mu * X_GK_residual from retained GK finite-hair branch", "epsilon_GK_source", "branch_3590"),
        (
            "CEI3592_10_total_identity",
            "Delta_charge_total",
            "B_xi/G_ref - M_H[Pi_M J_H] = Delta_frame+Delta_nonEH+Delta_symp+Delta_PiM+Delta_extra+Delta_flux+Delta_G+Delta_cal+Delta_PPN+Delta_GK_source",
            "epsilon_mu",
            "charge_status",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "identity_id": identity_id,
            "residual_symbol": symbol,
            "residual_expression": expression,
            "epsilon_mu_component": component,
            "status": "RETAINED_UNFILLED_NO_CANCELLATION_CREDIT" if identity_id != "CEI3592_10_total_identity" else "TOTAL_IDENTITY_READY_VALUES_MISSING",
            "source_path": str(source_paths[source_key]),
            "numeric_value_present": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for identity_id, symbol, expression, component, source_key in rows
    ]


def epsilon_mu_input_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("EMI3592_0_epsilon_frame", "epsilon_frame", "Delta_frame/(G_ref M_H)", "dimensionless", "same-frame observed source/orbit/charge split", "MISSING_ZERO_OR_NUMERIC_INPUT", "charge_residuals"),
        ("EMI3592_1_epsilon_operator", "epsilon_operator", "Delta_nonEH/(G_ref M_H)", "dimensionless", "non-EH operator charge/source contribution", "MISSING_EH_ONLY_OR_R11_INPUT", "charge_residuals"),
        ("EMI3592_2_epsilon_symp", "epsilon_symp", "Delta_symp/(G_ref M_H)", "dimensionless", "boundary symplectic/reference leakage", "MISSING_BOUNDARY_REFERENCE_INPUT", "charge_residuals"),
        ("EMI3592_3_epsilon_PiM", "epsilon_PiM", "Delta_PiM/(G_ref M_H)", "dimensionless", "projector variation or wrong mass-current object", "MISSING_PROJECTOR_VARIATION_INPUT", "charge_residuals"),
        ("EMI3592_4_epsilon_extra", "epsilon_extra", "Delta_extra/(G_ref M_H)", "dimensionless", "boundary/bulk/domain/memory/range/connection extra mass charge", "MISSING_EXTRA_MONOPOLE_INPUT", "mu_extra_vector"),
        ("EMI3592_5_epsilon_flux", "epsilon_flux", "Delta_flux/(G_ref M_H)", "dimensionless_or_rate_profile", "radial/time source-flux drift", "MISSING_FLUX_PROFILE_OR_ZERO", "constant_gm_2583"),
        ("EMI3592_6_epsilon_G", "epsilon_G", "Delta_G/(G_ref M_H)", "dimensionless_or_rate", "G_ref/kappa drift or species/range dependence", "MISSING_CONSTANT_G_INPUT", "constant_gm_2583"),
        ("EMI3592_7_epsilon_cal", "epsilon_calibration", "Delta_cal/(G_ref M_H)", "dimensionless", "closed charge not calibrated to Gauss/orbital mass", "MISSING_GAUSS_ORBITAL_INPUT", "charge_residuals"),
        ("EMI3592_8_epsilon_PPN_source", "epsilon_PPN_source", "Delta_PPN/(G_ref M_H)", "dimensionless", "second-order source stability failure", "MISSING_PPN_SOURCE_INPUT", "source_measure_residuals"),
        ("EMI3592_9_epsilon_GK_source", "epsilon_GK_source", "K_GK_mu*X_GK_residual/(G_ref M_H)", "dimensionless", "retained GK branch projected into source coupling", "MISSING_K_GK_MU_INPUT", "branch_3590"),
        (
            "EMI3592_10_epsilon_mu",
            "epsilon_mu",
            "sum_abs(epsilon_frame,epsilon_operator,epsilon_symp,epsilon_PiM,epsilon_extra,epsilon_flux,epsilon_G,epsilon_calibration,epsilon_PPN_source,epsilon_GK_source)",
            "dimensionless envelope",
            "measured-GM source-coupling residual, no cancellation credit",
            "INPUT_PACK_READY_VALUES_MISSING",
            "epsilon_mu_3591",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "input_id": input_id,
            "symbol": symbol,
            "formula_or_definition": formula,
            "units": units,
            "meaning": meaning,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "numeric_value_present": False,
            "source_backed_owner": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for input_id, symbol, formula, units, meaning, status, source_key in rows
    ]


def promotion_gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("PROM3592_0_equality_zero", "B_xi/G_ref - M_H[Pi_M J_H]=0", "FAIL_CURRENT_CLAIM", "all Delta rows must be theorem-zero; current status says equality parent-derived fail", "charge_status"),
        ("PROM3592_1_flux_closure", "d(Pi_M J_H)=0", "FAIL_CURRENT_CLAIM", "projector commutator and extra-current terms remain open", "parent_source_identity"),
        ("PROM3592_2_topological_glue", "Pi_M J_H=J_M_top+dB_zero", "FAIL_CURRENT_CLAIM", "R_eq and boundary improvement zero are not parent-derived", "top_hilbert_decision"),
        ("PROM3592_3_worldtube_measure", "M_source[W]=exterior charge", "FAIL_CURRENT_CLAIM", "worldtube source-measure glue is conditional and not inherited by current MTS", "worldtube_decision"),
        ("PROM3592_4_epsilon_pack", "epsilon_mu input rows exist", "PASS_NONCLAIM", "input pack is source-owner complete but values remain missing", "epsilon_mu_3591"),
        ("PROM3592_5_no_Newton_claim", "Newton/PPN/local-GR promotion", "PASS_GUARD", "no measured-GM/Newton/PPN claim allowed until equality or epsilon rows score", "charge_status"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "criterion": criterion,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, criterion, status, detail, source_key in rows
    ]


def activation_gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("GATE3592_0_sources", "PASS", "all source paths and selected anchors exist", "next_3591"),
        ("GATE3592_1_equality_attempt", "PASS_DERIVED_AS_CONTRACT", "exact equality route and closure conditions are written", "charge_direct"),
        ("GATE3592_2_equality_claim", "FAIL_CURRENT_CLAIM", "Pi_M/Hilbert/Hamiltonian equality is not parent-signed", "charge_status"),
        ("GATE3592_3_residual_identity", "PASS", "charge-current equality residual identity is adopted and extended to epsilon_mu", "charge_residuals"),
        ("GATE3592_4_input_pack", "PASS_NONCLAIM", "epsilon_mu input pack has source/unit owners", "epsilon_mu_3591"),
        ("GATE3592_5_score_ready", "FAIL_CURRENT_SCORE", "numeric/theorem-zero values remain missing for epsilon_mu components", "constant_gm_2583"),
        ("GATE3592_6_local_GR", "FAIL_CURRENT_CLAIM", "Newton/PPN/local-GR remain blocked until equality or residual scores close", "source_measure_decision"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, status, detail, source_key in rows
    ]


def status_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "PIM_HILBERT_EQUALITY_NOT_DERIVED_EPSILON_MU_INPUT_PACK_READY",
            "strongest_result": "3592 adopts the exact residual identity for the central source-coupling clause: B_xi/G_ref - M_H[Pi_M J_H] is decomposed into Delta_frame, Delta_nonEH, Delta_symp, Delta_PiM, Delta_extra, Delta_flux, Delta_G, Delta_cal, Delta_PPN, and Delta_GK_source. Equality is not parent-signed, but epsilon_mu now has a source-owner input pack with units and no cancellation credit.",
            "decision": "do not claim Pi_M/Hilbert equality, measured GM, Newton, PPN, or local GR; next work should fill or zero the epsilon_mu components, starting with Pi_M/projector variation and flux closure",
            "still_missing": "parent Pi_M origin, projector variation silence, topological-Hilbert glue, Hamiltonian boundary integrability/reference zero, source-current Ward closure, zero extra mass channel, Gauss/orbital calibration, numeric/source-backed epsilon_mu inputs",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_paths["status_3591"]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3592_0",
            "target_doc": "3593-Y5-R2FR-PiM-projector-variation-zero-or-DeltaPiM-bound.md",
            "target_script": "scripts/Y5_R2FR_3593_PiM_projector_variation_zero_or_DeltaPiM_bound.py",
            "objective": "attack the biggest equality obstruction: prove Pi_M is parent-owned/variation-silent so Delta_PiM=0, or build a first source-backed Delta_PiM/epsilon_PiM bound input row",
            "success_gate": "either delta(Pi_M)J_H and [d,Pi_M]J_H vanish by parent/topological theorem, or epsilon_PiM gets explicit source/unit/bound rows without GM/Newton claims",
            "reason": "3592 shows Delta_PiM is the central obstruction between closed Hilbert current and measured Hamiltonian mass",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_paths: dict[str, Path],
    out_paths: dict[str, Path],
    equality: list[dict[str, object]],
    residuals: list[dict[str, object]],
    inputs: list[dict[str, object]],
    promotion: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in out_paths.items() if key != "validation"}
    needles = {
        "next_3591": "NEXT3591_0",
        "status_3591": "GM_TRANSFER_CONTRACT_DERIVED_RESIDUAL_PROPAGATION_ACTIVE",
        "gm_contract_3591": "GMT3591_3_Hamiltonian_equals_Hilbert_mass",
        "epsilon_mu_3591": "EMU3591_8_epsilon_mu_total",
        "validation_3591": "VAL3591_13_formalization_workbench_untouched",
        "charge_direct": "CC4_boundary_variation_equals_projected_source_variation",
        "charge_residuals": "Delta_PiM",
        "charge_status": "charge-current equality parent-derived",
        "top_hilbert_attempt": "EH501_0_equality_statement",
        "top_hilbert_obstructions": "OB501_0_independent_topological_label",
        "top_hilbert_decision": "D501_3_promotion",
        "parent_source_identity": "I499_3_parent_source_identity",
        "parent_source_residuals": "S499_0_projector_commutator",
        "parent_source_decision": "D499_4_promotion",
        "noether_theorem": "T505_conditional_Noether_mass_charge_closure",
        "noether_chain": "D505_6_worldtube_readout",
        "noether_terms": "C505_projector",
        "source_measure_theorem": "T509_2_no_extra_mass_channel",
        "source_measure_residuals": "SMR509_1_Delta_PiM",
        "source_measure_decision": "D509_2",
        "worldtube_theorem": "T510_2_MTS_transfer_condition",
        "worldtube_proof": "P510_6",
        "worldtube_decision": "D510_1",
        "mass_flux": "MF0_parent_projector_origin",
        "hamiltonian_charge": "HC4_charge_equals_PiM_Hilbert_mass",
        "mu_extra_vector": "epsilon_domain_projector",
        "constant_gm_2583": "GM2583_3_radial_source_hair",
        "branch_3590": "BV3590_3_demoted_residual_parameter",
    }
    validations.append(("VAL3592_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3592 source paths exist"))
    validations.append(("VAL3592_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected 3592 anchors found"))
    validations.append(("VAL3592_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3592 output files written"))
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
    validations.append(("VAL3592_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3592_4_equality_verdict_present", any(row["attempt_id"] == "PHE3592_7_verdict" and row["status"] == "EQUALITY_NOT_DERIVED_RESIDUAL_PACK_ACTIVE" for row in equality), "PiM/Hilbert equality verdict is explicit"))
    required_deltas = {"Delta_frame", "Delta_nonEH", "Delta_symp", "Delta_PiM", "Delta_extra", "Delta_flux", "Delta_G", "Delta_cal", "Delta_PPN", "Delta_GK_source", "Delta_charge_total"}
    validations.append(("VAL3592_5_delta_identity_complete", required_deltas.issubset({str(row["residual_symbol"]) for row in residuals}), "charge residual identity includes all required Delta terms"))
    required_inputs = {"epsilon_frame", "epsilon_operator", "epsilon_symp", "epsilon_PiM", "epsilon_extra", "epsilon_flux", "epsilon_G", "epsilon_calibration", "epsilon_PPN_source", "epsilon_GK_source", "epsilon_mu"}
    validations.append(("VAL3592_6_epsilon_input_pack_complete", required_inputs.issubset({str(row["symbol"]) for row in inputs}), "epsilon_mu input pack includes all required components"))
    validations.append(("VAL3592_7_no_claim_flags", all(str(row.get("valid_for_claim", False)).lower() == "false" and str(row.get("claim_allowed", False)).lower() == "false" for row in equality + residuals + inputs + promotion + gates + status + next_target), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3592_8_score_blocked", any(row["gate_id"] == "GATE3592_5_score_ready" and row["status"] == "FAIL_CURRENT_SCORE" for row in gates), "score remains blocked until epsilon inputs have values or zero theorems"))
    validations.append(("VAL3592_9_no_Newton_claim", any(row["gate_id"] == "PROM3592_5_no_Newton_claim" and row["status"] == "PASS_GUARD" for row in promotion), "Newton/PPN/local-GR claim guard is active"))
    validations.append(("VAL3592_10_next_target_selected", any(row["next_id"] == "NEXT3592_0" for row in next_target), "3593 PiM projector variation target selected"))
    validations.append(("VAL3592_11_generated_source_paths_exist", all(Path(str(row["source_path"])).exists() for row in equality + residuals + inputs + promotion + gates + status), "every generated row source_path exists"))
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_3592*")) or any(FORMALIZATION.rglob("3592-Y5-R2FR*"))
    validations.append(("VAL3592_12_formalization_workbench_untouched", not formalization_touched, "no 3592 checkpoint output appears in formalization-workbench"))
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passes, detail in validations
    ]


def write_doc(
    equality: list[dict[str, object]],
    residuals: list[dict[str, object]],
    inputs: list[dict[str, object]],
    promotion: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 3592 - PiM/Hilbert charge equality or epsilon_mu input pack",
        "",
        "## Verdict",
        "`B_xi/G_ref = M_H[Pi_M J_H]` is still not parent-derived.  The useful result is that the equality failure is now an explicit measured-GM residual identity, not a vague missing step.",
        "",
        "`B_xi/G_ref - M_H[Pi_M J_H] = Delta_frame + Delta_nonEH + Delta_symp + Delta_PiM + Delta_extra + Delta_flux + Delta_G + Delta_cal + Delta_PPN + Delta_GK_source`.",
        "",
        "So `epsilon_mu` is now an input pack with source/unit owners and no cancellation credit.",
        "",
        "## Equality Attempt",
    ]
    for row in equality:
        lines.append(f"- `{row['attempt_id']}`: {row['status']} - {row['mathematical_form']}")
    lines.extend(["", "## Residual Identity"])
    for row in residuals:
        lines.append(f"- `{row['identity_id']}` `{row['residual_symbol']}`: {row['status']} - {row['residual_expression']}")
    lines.extend(["", "## Epsilon Mu Input Pack"])
    for row in inputs:
        lines.append(f"- `{row['input_id']}` `{row['symbol']}`: {row['status']} - {row['formula_or_definition']}")
    lines.extend(["", "## Promotion Gates"])
    for row in promotion:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['criterion']}")
    lines.extend(["", "## Activation Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
        lines.append(f"- Decision: {row['decision']}")
        lines.append(f"- Still missing: {row['still_missing']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target"])
    for row in next_target:
        lines.append(f"- `{row['next_id']}` -> `{row['target_doc']}`")
        lines.append(f"- Objective: {row['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    out_paths = outputs()
    register = source_register(source_paths)
    equality = equality_attempt_rows(source_paths)
    residuals = residual_identity_rows(source_paths)
    inputs = epsilon_mu_input_rows(source_paths)
    promotion = promotion_gate_rows(source_paths)
    gates = activation_gate_rows(source_paths)
    status = status_rows(source_paths)
    next_target = next_target_rows()
    for key, rows in {
        "source_register": register,
        "equality_attempt": equality,
        "residual_identity": residuals,
        "epsilon_mu_input_pack": inputs,
        "promotion_gates": promotion,
        "activation_gates": gates,
        "status": status,
        "next_target": next_target,
        "canonical_status": status,
    }.items():
        write_csv(out_paths[key], rows)
    validation = validation_rows(source_paths, out_paths, equality, residuals, inputs, promotion, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(equality, residuals, inputs, promotion, gates, status, next_target, validation)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise SystemExit(f"3592 validation failed: {failures}")
    print(f"wrote {DOC}")
    for key, path in out_paths.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
