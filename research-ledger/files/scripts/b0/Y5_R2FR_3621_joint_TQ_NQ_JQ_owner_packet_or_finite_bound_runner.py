from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3621"
BRANCH_ID = "MTS_R2FR_Y5_JOINT_TQ_NQ_JQ_OWNER_PACKET_OR_FINITE_BOUND_RUNNER_3621"
DOC = ROOT / "3621-Y5-R2FR-joint-TQ-NQ-JQ-owner-packet-or-finite-bound-runner.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def output_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3621_SOURCE_REGISTER.csv",
        "joint_owner_packet": RESIDUALS / "P8_Y5_R2FR_3621_JOINT_OWNER_PACKET.csv",
        "closure_audit": RESIDUALS / "P8_Y5_R2FR_3621_JOINT_OWNER_CLOSURE_AUDIT.csv",
        "finite_runner_template": RESIDUALS / "P8_Y5_R2FR_3621_FINITE_BOUND_RUNNER_TEMPLATE.csv",
        "finite_runner_smoke": RESIDUALS / "P8_Y5_R2FR_3621_FINITE_BOUND_RUNNER_SMOKE.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3621_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3621_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3621_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_joint_TQ_NQ_JQ_owner_packet_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3621_VALIDATION.csv",
    }


def source_map() -> dict[str, tuple[Path, str]]:
    return {
        "handoff_3620": (
            RESIDUALS / "P8_Y5_R2FR_3620_NEXT_TARGET.csv",
            "3621-Y5-R2FR-joint-TQ-NQ-JQ-owner-packet-or-finite-bound-runner.md",
        ),
        "owner_theorem_3620": (
            RESIDUALS / "P8_Y5_R2FR_3620_EM_SOURCE_OWNER_THEOREM_ATTEMPT.csv",
            "lambda_F2=b_alpha=kappa_J=w_EM=0",
        ),
        "calibration_3620": (
            RESIDUALS / "P8_Y5_R2FR_3620_MAXWELL_SOURCE_CALIBRATION_GATE.csv",
            "MCG3620_3_same_current",
        ),
        "finite_coefficients_3620": (
            RESIDUALS / "P8_Y5_R2FR_3620_FINITE_F2_SOURCE_COEFFICIENT_ROWS.csv",
            "Phi_EM_boundary",
        ),
        "kinetic_765": (
            RESIDUALS / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv",
            "MKI765_5_total",
        ),
        "current_1814": (
            RESIDUALS / "P8_Y5_PARENT_QLOC_1814_VISIBLE_CONNECTION_CURRENT_OWNER_THEOREM.csv",
            "VCC1814_4_verdict",
        ),
        "alpha_1812": (
            RESIDUALS / "P8_Y5_PARENT_QLOC_1812_ALPHA_LEVEL_OWNER_AUDIT.csv",
            "ALO1812_5_verdict",
        ),
        "unique_f2_1235": (
            RESIDUALS / "P8_Y5_R10_1235_UNIQUE_F2_TYPED_COEFFICIENT_DOMAIN_PROOF_ATTEMPT.csv",
            "UF21235_7_verdict",
        ),
        "f2_gates_3212": (
            RESIDUALS / "P8_Y5_R2FR_3212_NO_EXTRA_F2_THEOREM_GATES.csv",
            "F2G3212_5_total_EM_zero",
        ),
        "no_hidden_visible_2659": (
            RESIDUALS / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
            "ODT2659_6_verdict",
        ),
        "poynting_3463": (
            RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv",
            "EM3463_4_multiplier_obstruction",
        ),
        "alpha_bound_3118": (
            RESIDUALS / "P8_Y5_R2FR_3118_BALPHA_PRODUCT_BOUND_RUNNER_OUTPUT.csv",
            "BAP3118_1",
        ),
        "alpha_smoke_3272": (
            RESIDUALS / "P8_Y5_R2FR_3272_ALPHA_EM_BOUND_RUNNER_RESULTS_NONCLAIM.csv",
            "ARUN3272_0_missing_prediction_refusal",
        ),
        "wep_components_2100": (
            RESIDUALS / "P8_Y5_PARENT_QLOC_2100_WEP_COMPONENT_BOUND_ROWS.csv",
            "WCB2100_5_total_guard",
        ),
        "wep_product_1094": (
            RESIDUALS / "P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_BOUND_IMPORT.csv",
            "BOUND1094_0_direct_WEP_alpha_threshold",
        ),
        "common_scale_runner": (
            RESIDUALS / "P8_EM_common_scale_bound_runner_results.csv",
            "UCRUN3510_1_Newton_GM",
        ),
    }


def source_register_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    rows = []
    for source_id, source_data in source_map().items():
        source_path, needle = source_data
        exists = source_path.exists()
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(source_path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(source_path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def joint_owner_packet_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "packet_id": "JOP3621_0_parent_connection",
            "owner_object": "A_Q from parent connection",
            "required_statement": "A_parent=A_Q T_Q + A_perp is defined before readout and T_Q is part of the parent field/representation data.",
            "mathematical_role": "prevents appended Maxwell-sector normalization",
            "zero_if_joint_signed": "no appended A_Q normalization",
            "source_path": str(sources["kinetic_765"][0]),
            "current_status": "TEMPLATE_ONLY",
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "packet_id": "JOP3621_1_fixed_norm",
            "owner_object": "N_Q=<T_Q,T_Q>_P",
            "required_statement": "N_Q is fixed by parent fibre metric/lattice/symplectic data and D_v N_Q=0 on q-fibres.",
            "mathematical_role": "fixes Maxwell kinetic normalization inherited from the parent curvature norm",
            "zero_if_joint_signed": "lambda_F2=0 contribution from norm drift; b_alpha norm part=0",
            "source_path": str(sources["alpha_1812"][0]),
            "current_status": "NORM_ROUTE_CONDITIONAL_NOT_SIGNED",
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "packet_id": "JOP3621_2_unique_curvature_norm",
            "owner_object": "unique F_Q^2 subblock",
            "required_statement": "The visible EM subblock descends from one parent curvature norm and no independent lambda_A F_Q^2 or f_X F_Q^2 slot exists.",
            "mathematical_role": "kills hidden or visible Maxwell kinetic counterterms",
            "zero_if_joint_signed": "lambda_F2=0 and F2-induced b_alpha=0",
            "source_path": str(sources["unique_f2_1235"][0]),
            "current_status": "UNIQUE_F2_NOT_CLOSED",
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "packet_id": "JOP3621_3_noether_current",
            "owner_object": "J_Q Noether/Ward current",
            "required_statement": "J_Q := delta S_matter/delta A_Q with charge labels as fixed T_Q representation weights.",
            "mathematical_role": "ties Lorentz force, charge/current normalization and matter-EM exchange to one source current",
            "zero_if_joint_signed": "kappa_J=0 for current-owner drift",
            "source_path": str(sources["current_1814"][0]),
            "current_status": "NOETHER_CURRENT_OWNER_MISSING",
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "packet_id": "JOP3621_4_no_current_morphism",
            "owner_object": "source/test current readout",
            "required_statement": "No map J_Q -> c_J J_Q, source label kappa_A, or species/source-only current morphism is an allowed parent operator.",
            "mathematical_role": "prevents WEP/source/test rescaling after Noether current is defined",
            "zero_if_joint_signed": "kappa_J=0 and source-label current terms vanish",
            "source_path": str(sources["no_hidden_visible_2659"][0]),
            "current_status": "CURRENT_RESCALING_COUNTERMODEL_SURVIVES",
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "packet_id": "JOP3621_5_readout_radiative",
            "owner_object": "measured alpha/readout closure",
            "required_statement": "Clock, spectroscopy, EFT/radiative and material readouts preserve the same parent EM owner and factor only through q or fixed representation data.",
            "mathematical_role": "prevents alpha/source markers from regenerating after tree-level closure",
            "zero_if_joint_signed": "b_alpha=0 in clock/spectroscopy/WEP readout channels",
            "source_path": str(sources["alpha_1812"][0]),
            "current_status": "READOUT_RADIATIVE_CLOSURE_UNSIGNED",
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "packet_id": "JOP3621_6_Hilbert_source_weight",
            "owner_object": "EM Hilbert source weight",
            "required_statement": "The EM stress source is the Hilbert stress of the same observed-Hodge Maxwell action with no extra w_EM multiplier.",
            "mathematical_role": "makes Poynting/EM energy gravitate through the same local GR source slot",
            "zero_if_joint_signed": "w_EM=0",
            "source_path": str(sources["poynting_3463"][0]),
            "current_status": "OBSTRUCTION_RETAINED",
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "packet_id": "JOP3621_7_boundary_flux",
            "owner_object": "EM boundary/radiative flux accounting",
            "required_statement": "Stationary source charge uses a closed worldtube/no-radiation branch or explicit Poynting boundary flux row.",
            "mathematical_role": "separates source mass from radiative leakage without cancellation",
            "zero_if_joint_signed": "Phi_EM_boundary=0 only for closed stationary/no-flux branch",
            "source_path": str(sources["f2_gates_3212"][0]),
            "current_status": "NEW_GATE_VALUES_MISSING",
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "packet_id": "JOP3621_8_joint_zero",
            "owner_object": "joint EM source-coupling owner packet",
            "required_statement": "JOP3621_0 through JOP3621_7 close on the same parent branch without post-fit cancellation.",
            "mathematical_role": "the only safe theorem-zero route for calibrated EM source coupling",
            "zero_if_joint_signed": "lambda_F2=b_alpha=kappa_J=w_EM=0 and Phi_EM_boundary=0 only on no-flux branch",
            "source_path": str(sources["owner_theorem_3620"][0]),
            "current_status": "JOINT_PACKET_NOT_PARENT_SIGNED",
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def closure_audit_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": "JCA3621_0_all_or_nothing",
            "audit_target": "joint owner packet",
            "condition": "all packet rows must be parent_signed=True on the same branch",
            "current_result": "FAIL_NONCLAIM",
            "reason": "every packet row remains conditional or countermodel-retained",
            "effect": "finite bound runner path remains mandatory",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": "JCA3621_1_no_piecemeal_credit",
            "audit_target": "anti-knob-moving guard",
            "condition": "closing unique F2 alone is insufficient if J_Q or readout/current owner remains free",
            "current_result": "GUARD_ACTIVE",
            "reason": "source coupling can move into kappa_J, b_alpha or w_EM",
            "effect": "zero claims require packet-level closure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": "JCA3621_2_bound_runner_ready",
            "audit_target": "finite coefficient fallback",
            "condition": "each live coefficient has units, arena, prediction field, bound field, and source path",
            "current_result": "TEMPLATE_READY_VALUES_MISSING",
            "reason": "runner rows are schema-ready but MTS predictions and some direct bound rows are missing",
            "effect": "runner refuses to score until numeric/source-backed inputs exist",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def finite_runner_template_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "runner_row_id": "FBR3621_0_lambda_F2_alpha",
            "coefficient": "lambda_F2",
            "prediction_symbol": "lambda_F2_pred",
            "prediction_value": "MISSING_PARENT_ZERO_OR_NUMERIC_VALUE",
            "prediction_units": "dimensionless",
            "arena": "alpha_EM_clock_spectroscopy_WEP",
            "bound_symbol": "alpha_clock_or_WEP_product_bound",
            "bound_value": "1.389797711495e-12",
            "bound_units": "dimensionless",
            "bound_source_path": str(sources["alpha_smoke_3272"][0]),
            "local_owner_source_path": str(sources["unique_f2_1235"][0]),
            "comparison": "abs(lambda_F2_pred) <= bound_value after projection map is declared",
            "source_backed": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "runner_row_id": "FBR3621_1_b_alpha_clock",
            "coefficient": "b_alpha",
            "prediction_symbol": "b_alpha_pred",
            "prediction_value": "MISSING_PARENT_ZERO_OR_NUMERIC_VALUE",
            "prediction_units": "yr^-1_or_dimensionless_after_tau",
            "arena": "clock_alpha_drift",
            "bound_symbol": "clock_product_bound",
            "bound_value": "2.1e-18",
            "bound_units": "yr^-1",
            "bound_source_path": str(sources["alpha_bound_3118"][0]),
            "local_owner_source_path": str(sources["alpha_1812"][0]),
            "comparison": "abs(b_alpha_pred*tau_clock_time) <= bound_value with tau_clock_time declared",
            "source_backed": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "runner_row_id": "FBR3621_2_kappa_J_WEP",
            "coefficient": "kappa_J",
            "prediction_symbol": "kappa_J_pred",
            "prediction_value": "MISSING_PARENT_ZERO_OR_NUMERIC_VALUE",
            "prediction_units": "dimensionless",
            "arena": "MICROSCOPE_WEP_current_source_rescaling",
            "bound_symbol": "P_WEP_alpha_direct_or_eta_component_bound",
            "bound_value": "4.7977805227322346e-05",
            "bound_units": "dimensionless",
            "bound_source_path": str(sources["wep_product_1094"][0]),
            "local_owner_source_path": str(sources["current_1814"][0]),
            "comparison": "abs(kappa_J_pred * material_projection) <= bound_value",
            "source_backed": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "runner_row_id": "FBR3621_3_w_EM_source",
            "coefficient": "w_EM",
            "prediction_symbol": "w_EM_pred",
            "prediction_value": "MISSING_PARENT_ZERO_OR_NUMERIC_VALUE",
            "prediction_units": "dimensionless",
            "arena": "Newton_GM_WEP_PPN_EM_binding_source_weight",
            "bound_symbol": "source_weight_or_common_scale_bound",
            "bound_value": "MISSING_DIRECT_NUMERIC_BOUND",
            "bound_units": "dimensionless_or_declared_projection",
            "bound_source_path": str(sources["common_scale_runner"][0]),
            "local_owner_source_path": str(sources["poynting_3463"][0]),
            "comparison": "abs(w_EM_pred * EM_binding_fraction_or_source_projection) <= bound_value",
            "source_backed": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "runner_row_id": "FBR3621_4_Phi_EM_boundary",
            "coefficient": "Phi_EM_boundary",
            "prediction_symbol": "Phi_EM_boundary_pred",
            "prediction_value": "MISSING_BOUNDARY_ZERO_OR_NUMERIC_FLUX",
            "prediction_units": "power_or_dimensionless_after_Htau_normalization",
            "arena": "stationary_source_charge_orbital_energy_loss_Htau_flux",
            "bound_symbol": "no_flux_theorem_or_radiative_flux_bound",
            "bound_value": "MISSING_DIRECT_NUMERIC_BOUND",
            "bound_units": "power_or_dimensionless_after_Htau_normalization",
            "bound_source_path": str(sources["f2_gates_3212"][0]),
            "local_owner_source_path": str(sources["poynting_3463"][0]),
            "comparison": "abs(Phi_EM_boundary_pred/H_tau_scale) <= bound_value",
            "source_backed": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def finite_runner_smoke_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    rows = []
    for template in finite_runner_template_rows():
        has_numeric_bound = not str(template["bound_value"]).startswith("MISSING")
        has_numeric_prediction = not str(template["prediction_value"]).startswith("MISSING")
        can_score = has_numeric_bound and has_numeric_prediction and template["source_backed"] is True
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "smoke_id": f"FSM3621_{len(rows)}",
                "runner_row_id": template["runner_row_id"],
                "coefficient": template["coefficient"],
                "arena": template["arena"],
                "prediction_value": template["prediction_value"],
                "bound_value": template["bound_value"],
                "can_score": can_score,
                "result": "BLOCKED_NOT_SCORED",
                "reason": "missing numeric MTS prediction and/or direct bound projection",
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def decision_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3621_0_packet_attempt",
            "decision": "The joint owner packet is now explicit, but every row remains parent-unsigned; no theorem-zero promotion is allowed.",
            "status": "PASS_PACKET_BUILT_NOT_SIGNED",
            "next_action": "try to derive the parent representation/fibre metric owner for T_Q and N_Q",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3621_1_finite_runner",
            "decision": "Finite runner templates are now wired with units, arenas and source paths; smoke rows refuse to score missing predictions/bounds.",
            "status": "PASS_RUNNER_TEMPLATE_BLOCKED_CORRECTLY",
            "next_action": "source direct bounds for w_EM and Phi_EM_boundary or derive theorem zeros",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3621_2_best_next_route",
            "decision": "Best next route is parent geometry: derive T_Q and N_Q from a compact/fixed fibre metric or lattice, because that removes multiple coefficients at once.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3622-Y5-R2FR-TQ-NQ-parent-fibre-metric-or-source-bound-acquisition.md",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS3621_0",
            "result": "JOINT_OWNER_PACKET_BUILT_FINITE_RUNNER_TEMPLATES_BLOCKED",
            "summary": "3621 builds the all-or-nothing T_Q/N_Q/J_Q/unique-F2/Hilbert-source owner packet and source-linked finite runner templates; no claim is promoted because the parent packet is unsigned and predictions remain missing.",
            "joint_packet_parent_signed": False,
            "finite_runner_template_ready": True,
            "finite_runner_score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3621_0",
            "target_doc": "3622-Y5-R2FR-TQ-NQ-parent-fibre-metric-or-source-bound-acquisition.md",
            "target_script": "scripts/Y5_R2FR_3622_TQ_NQ_parent_fibre_metric_or_source_bound_acquisition.py",
            "objective": "derive whether T_Q and N_Q are fixed by parent representation/fibre metric/lattice data; if not, acquire or stage direct source bounds for w_EM and Phi_EM_boundary while keeping lambda_F2, b_alpha and kappa_J nonclaim",
            "success_gate": "either T_Q/N_Q owner signs the shared EM normalization spine, or w_EM/Phi_EM_boundary receive source-backed bound rows and the finite runner remains blocked without MTS predictions",
            "reason": "3621 shows the highest-leverage derivation is fixed parent gauge-generator norm; the empirical fallback now has templates.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "joint_owner_packet": "BUILT_NOT_PARENT_SIGNED",
            "finite_runner": "TEMPLATE_READY_BLOCKED_CORRECTLY",
            "live_missing_predictions": "lambda_F2;b_alpha;kappa_J;w_EM;Phi_EM_boundary",
            "next_pressure_point": "T_Q_N_Q_parent_fibre_metric_or_wEM_Phi_bound_acquisition",
            "claim_status": "NO_CLAIM",
            "valid_for_claim": False,
        }
    ]


def write_markdown() -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3621 Y5 R2FR: joint T_Q/N_Q/J_Q owner packet or finite bound runner",
                "",
                "## Verdict",
                "- The all-or-nothing EM owner packet is now explicit.",
                "- No theorem-zero promotion is allowed yet: `T_Q`, `N_Q`, unique `F2`, `J_Q`, readout/radiative closure, Hilbert source weight and boundary flux are not jointly parent-signed.",
                "- Finite runner templates now exist with units, arenas and source paths, but correctly refuse to score missing MTS predictions.",
                "",
                "## Joint owner packet",
                "- `A_Q` must be a parent connection projection along fixed `T_Q`.",
                "- `N_Q=<T_Q,T_Q>_P` must be fixed representation/fibre metric/lattice data.",
                "- Unique `F_Q^2` must exclude `lambda_A F_Q^2` and hidden `f_X F_Q^2`.",
                "- `J_Q` must be the same `T_Q` Noether/Ward current used by source/test readout.",
                "- Readout/radiative closure must preserve the same owner.",
                "- EM Hilbert stress must have no extra `w_EM` source weight.",
                "- Boundary Poynting flux must be zero by stationary/no-flux theorem or carried explicitly.",
                "",
                "## Finite runner rows",
                "- `lambda_F2`: dimensionless alpha/clock/spectroscopy/WEP row.",
                "- `b_alpha`: clock alpha-drift row.",
                "- `kappa_J`: MICROSCOPE/WEP source-current rescaling row.",
                "- `w_EM`: Newton/PPN/orbital/source-weight row, direct bound still missing.",
                "- `Phi_EM_boundary`: stationary source/H_tau flux row, direct bound still missing.",
                "",
                "## Practical read",
                "- Piecemeal closure is not enough; this packet must close as one unit.",
                "- Best derivation target is now `T_Q/N_Q`: if the parent fixes the gauge generator and norm, several knobs collapse at once.",
                "",
                "## Next target",
                "- `3622-Y5-R2FR-TQ-NQ-parent-fibre-metric-or-source-bound-acquisition.md`.",
                "- First try the derivation: fixed parent representation/fibre metric/lattice for `T_Q` and `N_Q`.",
                "- Backup: acquire/stage direct bounds for `w_EM` and `Phi_EM_boundary`.",
                "",
                "## Claim status",
                "- `NO_CLAIM`: packet built, runner templates blocked correctly.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def validate() -> list[dict[str, object]]:
    timestamp = utc_now()
    paths = output_paths()
    results: list[tuple[str, bool, str]] = []

    sources = source_map()
    sources_exist = all(source_path.exists() for source_path, _needle in sources.values())
    needles_found = all(source_path.exists() and contains(source_path, needle) for source_path, needle in sources.values())
    results.append(("VAL3621_0_sources_exist", sources_exist, "all required 3621 source paths exist"))
    results.append(("VAL3621_1_needles_found", needles_found, "all selected 3621 source anchors found"))

    pre_validation_paths = [path for name, path in paths.items() if name != "validation"]
    outputs_exist = DOC.exists() and all(path.exists() for path in pre_validation_paths)
    results.append(("VAL3621_2_outputs_exist", outputs_exist, "all pre-validation 3621 outputs written"))

    parse_details: list[str] = []
    csv_parse_pass = True
    for name, path in paths.items():
        if name == "validation":
            continue
        try:
            parse_details.append(f"{name}:{len(read_csv(path))}")
        except Exception as exception:
            csv_parse_pass = False
            parse_details.append(f"{name}:ERROR:{exception}")
    results.append(("VAL3621_3_csv_parse", csv_parse_pass, "; ".join(parse_details)))

    packet_rows = read_csv(paths["joint_owner_packet"]) if paths["joint_owner_packet"].exists() else []
    packet_has_joint_zero = any("lambda_F2=b_alpha=kappa_J=w_EM=0" in row["zero_if_joint_signed"] for row in packet_rows)
    packet_not_signed = bool(packet_rows) and all(row["parent_signed"] == "False" for row in packet_rows)
    results.append(("VAL3621_4_packet_joint_zero_written", packet_has_joint_zero, "joint zero row written"))
    results.append(("VAL3621_5_packet_not_parent_signed", packet_not_signed, "packet remains nonclaim/not parent-signed"))

    template_rows = read_csv(paths["finite_runner_template"]) if paths["finite_runner_template"].exists() else []
    expected = {"lambda_F2", "b_alpha", "kappa_J", "w_EM", "Phi_EM_boundary"}
    found = {row["coefficient"] for row in template_rows}
    template_fields = {"prediction_value", "prediction_units", "arena", "bound_value", "bound_units", "bound_source_path", "local_owner_source_path"}
    template_complete = bool(template_rows) and all(template_fields.issubset(row.keys()) for row in template_rows)
    results.append(("VAL3621_6_finite_templates_present", expected.issubset(found), "finite runner rows present"))
    results.append(("VAL3621_7_finite_template_fields", template_complete, "finite runner templates include units/arenas/source paths"))

    smoke_rows = read_csv(paths["finite_runner_smoke"]) if paths["finite_runner_smoke"].exists() else []
    smoke_blocks = bool(smoke_rows) and all(row["result"] == "BLOCKED_NOT_SCORED" and row["can_score"] == "False" for row in smoke_rows)
    results.append(("VAL3621_8_smoke_blocks_missing_inputs", smoke_blocks, "finite runner smoke refuses to score missing predictions"))

    all_outputs_nonclaim = True
    for name, path in paths.items():
        if name == "validation" or not path.exists():
            continue
        for row in read_csv(path):
            if row.get("valid_for_claim") == "True" or row.get("claim_allowed") == "True":
                all_outputs_nonclaim = False
    results.append(("VAL3621_9_all_outputs_nonclaim", all_outputs_nonclaim, "all generated rows remain nonclaim"))

    formalization_clean = True
    formalization_detail = "formalization-workbench not found"
    if FORMALIZATION.exists():
        leaked_paths = list(FORMALIZATION.rglob("*3621*"))
        formalization_clean = len(leaked_paths) == 0
        formalization_detail = "no 3621 files in formalization-workbench" if formalization_clean else "; ".join(str(path) for path in leaked_paths[:5])
    results.append(("VAL3621_10_no_formalization_leak", formalization_clean, formalization_detail))

    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in results
    ]


def main() -> None:
    paths = output_paths()
    write_csv(paths["source_register"], source_register_rows())
    write_csv(paths["joint_owner_packet"], joint_owner_packet_rows())
    write_csv(paths["closure_audit"], closure_audit_rows())
    write_csv(paths["finite_runner_template"], finite_runner_template_rows())
    write_csv(paths["finite_runner_smoke"], finite_runner_smoke_rows())
    write_csv(paths["decision_gates"], decision_gate_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_csv(paths["canonical_status"], canonical_status_rows())
    write_markdown()
    write_csv(paths["validation"], validate())

    failed = [row for row in read_csv(paths["validation"]) if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3621 validation failed: {failed}")
    print(f"wrote 3621 checkpoint with {len(read_csv(paths['validation']))} validation checks")


if __name__ == "__main__":
    main()
