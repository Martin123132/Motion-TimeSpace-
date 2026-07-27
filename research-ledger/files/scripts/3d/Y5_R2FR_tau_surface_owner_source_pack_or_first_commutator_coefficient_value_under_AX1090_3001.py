from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3001"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3001-Y5-R2FR-tau-surface-owner-source-pack-or-first-commutator-coefficient-value-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3001_SOURCE_REGISTER.csv",
    "owner": RESIDUALS / "P8_Y5_R2FR_3001_TAU_SURFACE_OWNER_SOURCE_PACK_AUDIT.csv",
    "coefficients": RESIDUALS / "P8_Y5_R2FR_3001_COMMUTATOR_COEFFICIENT_ACQUISITION_ROWS.csv",
    "first_row": RESIDUALS / "P8_Y5_R2FR_3001_FIRST_COMMUTATOR_COEFFICIENT_ROW.csv",
    "demotion": RESIDUALS / "P8_Y5_R2FR_3001_TAU_SURFACE_ROUTE_DEMOTION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3001_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3001_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3001_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3001_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3001_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "owner_copy": PARENT_ACTION / "tau_surface_owner_source_pack_3001_NOT_SIGNED.csv",
    "coeff_copy": LOCAL_BOUNDS / "commutator_coefficient_acquisition_rows_3001_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3001_CORNER_TOPOLOGICAL_BV_CLASSIFICATION_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def missing_anchors(path: Path, needles: list[str]) -> str:
    haystack = text(path)
    return "; ".join(needle for needle in needles if needle not in haystack)


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [str(output_row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


SOURCE_SPECS = [
    (
        "SRC3001_00_3000_next",
        RESIDUALS / "P8_Y5_R2FR_3000_NEXT_TARGET.csv",
        ["NEXT3000_0_3001", "tau/surface owner pack"],
        "3000 selects tau/surface owner source pack or first commutator coefficient value.",
    ),
    (
        "SRC3001_01_3000_bound",
        RESIDUALS / "P8_Y5_R2FR_3000_EPSILON_BV_TAU_SURFACE_BOUND_ROWS.csv",
        ["BVT3000_1_tau_component", "C_tau ||delta_v tau|| / M_ref"],
        "3000 staged C_tau, C_S, C_A and cap coefficient interfaces.",
    ),
    (
        "SRC3001_02_3000_audit",
        RESIDUALS / "P8_Y5_R2FR_3000_TAU_SURFACE_COMMUTATOR_ZERO_AUDIT.csv",
        ["TSC3000_4_finite_bound", "BOUND_INTERFACE_DERIVED_VALUES_MISSING"],
        "3000 derives the finite bound law but leaves values missing.",
    ),
    (
        "SRC3001_03_2599_owner",
        RESIDUALS / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_OWNER_ATTEMPT.csv",
        ["BCT2599_8_verdict", "BOUNDARY_CLOCK_TAU_OWNER_NOT_DERIVED_CURRENT_CORPUS"],
        "2599 rejects boundary-clock tau ownership for current corpus.",
    ),
    (
        "SRC3001_04_2599_tau_pack",
        RESIDUALS / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_DELTA_TAU_SOURCE_PACK.csv",
        ["DTS2599_12_C_Tobs_tau", "MISSING_TOBS_OPERATOR_NORM"],
        "2599 has tau operator norm/source pack rows but no numeric/source-backed values.",
    ),
    (
        "SRC3001_05_2599_runner_contract",
        RESIDUALS / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_BOUND_RUNNER_CONTRACT.csv",
        ["BRC2599_0_identity", "C_Tobs_tau"],
        "2599 states the scoring rule requiring operator norms and source paths.",
    ),
    (
        "SRC3001_06_2547_delta_ref_bounds",
        RESIDUALS / "P8_Y5_NO_SHADOW_2547_DELTA_REF_BOUND_ROWS.csv",
        ["DRB2547_2_tau_leak", "C_tau"],
        "2547 has C_tau tau-leak bound row but no value.",
    ),
    (
        "SRC3001_07_2455_bound_template",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2455_DELTA_REF_BOUND_ROW_TEMPLATE.csv",
        ["DBR2455_0_partial_q_Bref_bound", "C_tau"],
        "2455 gives operator-norm fallback formulas for boundary reference leakage.",
    ),
    (
        "SRC3001_08_2547_signature",
        RESIDUALS / "P8_Y5_NO_SHADOW_2547_SIGNATURE_AUDIT.csv",
        ["SIG2547_1_boundary_surface", "SIG2547_3_tau_coframe"],
        "2547 shows tau/coframe and surface/domain signatures are missing.",
    ),
    (
        "SRC3001_09_2455_zero_cert",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2455_BOUNDARY_DATA_ZERO_CERTIFICATE.csv",
        ["ZC2455_0_surface_domain", "ZC2455_2_tau"],
        "2455 confirms both surface/domain and tau certificates are blocked.",
    ),
    (
        "SRC3001_10_2588_tau",
        RESIDUALS / "P8_Y5_OBS_STACK_2588_Q_OBSE_TAU_DESCENT_AUDIT.csv",
        ["OSA2588_5_tau_identity", "MISSING_PARENT_TAU_IDENTITY"],
        "2588 confirms parent tau identity remains absent.",
    ),
    (
        "SRC3001_11_2900_source_complex",
        RESIDUALS / "P8_Y5_R2FR_2900_SOURCE_COMPLEX_OWNER_AUDIT.csv",
        ["SC2900_2_tau_lock", "SC2900_5_exterior_link_complex"],
        "2900 confirms same tau and fixed exterior link complex are not owned.",
    ),
]


def source_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "required_anchors": "; ".join(needles),
                "anchors_found": anchors(path, needles),
                "missing_anchors": missing_anchors(path, needles),
                "role": role,
            }
        )
        for source_id, path, needles, role in SOURCE_SPECS
    ]


def owner_rows() -> list[dict[str, Any]]:
    data = [
        (
            "OWN3001_0_tau_identity",
            "tau_source=tau_charge=tau_clock=tau_boundary=tau_readout",
            "MISSING_PARENT_TAU_IDENTITY",
            "2588/2599/2900 all leave same-tau ownership unsigned.",
            "epsilon_Bv_tau_variation_abs",
        ),
        (
            "OWN3001_1_boundary_clock",
            "parent boundary-clock class and normalization",
            "MISSING_PARENT_BOUNDARY_CLOCK_CLASS",
            "clock product data constrain drift but do not define Hamiltonian/source tau.",
            "epsilon_delta_tau",
        ),
        (
            "OWN3001_2_q_eobs_basic",
            "tau is q/e_obs-basic",
            "MISSING_Q_OBS_E_CLOCK_BASICNESS",
            "tau cannot be used as a quotient-invariant generator without q/e_obs owner.",
            "epsilon_tau_frame",
        ),
        (
            "OWN3001_3_bulk_extension",
            "unique bulk/exterior extension of tau",
            "GENERATOR_EXTENSION_NOT_SOURCED",
            "boundary-normalized tau has no sourced stationary/Killing/quasilocal extension.",
            "epsilon_nonstationary_tau",
        ),
        (
            "OWN3001_4_surface_link",
            "delta_v S_link=0 and fixed linked surface pair",
            "MISSING_SOURCE_BLIND_SURFACE_DOMAIN_RULE",
            "surface/domain can still move with source/readout.",
            "epsilon_Bv_surface_motion_abs",
        ),
        (
            "OWN3001_5_Aext_caps",
            "delta_v A_ext=0 and fixed caps/collar",
            "MISSING_FIXED_AEXT_CAPS",
            "annulus/cap transport remains a legal boundary leakage channel.",
            "epsilon_Bv_annulus_cap_transport_abs",
        ),
        (
            "OWN3001_6_no_shortcuts",
            "no observed-GM/surface-fit import",
            "GUARDRAIL_ACTIVE",
            "surface or tau cannot be selected from target orbital/PPN success.",
            "shortcut_guard",
        ),
        (
            "OWN3001_7_coefficients",
            "C_tau, C_S, C_A, C_cap and derivative norms",
            "MISSING_OPERATOR_COEFFICIENTS_AND_NORMS",
            "bound law exists, but no finite coefficient values or derivative norms are sourced.",
            "epsilon_Bv_tau_surface_commutator_total_abs",
        ),
        (
            "OWN3001_8_Mref",
            "positive same-frame M_ref/M_H_ref",
            "MISSING_POSITIVE_SAME_FRAME_MREF",
            "even a finite numerator cannot be scored without noncircular normalization.",
            "all_tau_surface_rows",
        ),
        (
            "OWN3001_9_verdict",
            "tau/surface owner source pack",
            "OWNER_PACK_NOT_SIGNED_NO_FINITE_COEFFICIENT_VALUE",
            "no theorem-zero promotion and no finite score-ready coefficient row exists in current corpus.",
            "tau_surface_route_demoted_to_residual_closure",
        ),
    ]
    return [
        base(
            {
                "owner_id": owner_id,
                "required_object": obj,
                "current_status": status,
                "reason": reason,
                "residual_if_missing": residual,
                "owner_signed": False,
                "accepted_for_local_gr": False,
            }
        )
        for owner_id, obj, status, reason, residual in data
    ]


def coefficient_rows() -> list[dict[str, Any]]:
    source_path = RESIDUALS / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_DELTA_TAU_SOURCE_PACK.csv"
    data = [
        (
            "COEF3001_0_C_tau",
            "C_tau_commutator_operator_norm",
            "operator norm multiplying tau/coframe variation in epsilon_Bv_tau_surface_commutator",
            "operator_norm_boundary_charge_per_tau_norm_over_M_ref",
            "C_tau ||delta_v tau|| / M_ref",
            "MISSING_C_TAU_NUMERIC_OR_THEOREM_ZERO",
            source_path,
            "DTS2599_12_C_Tobs_tau;DRB2547_2_tau_leak;DBR2455_0_partial_q_Bref_bound",
        ),
        (
            "COEF3001_1_norm_delta_tau",
            "norm_delta_v_tau",
            "same-branch vertical tau/coframe variation norm",
            "tau_norm",
            "||delta_v tau||",
            "MISSING_DELTA_TAU_VALUE_OR_THEOREM_ZERO",
            source_path,
            "DTS2599_3_delta_tau_norm;ZC2455_2_tau",
        ),
        (
            "COEF3001_2_C_S",
            "C_S_surface_motion_operator_norm",
            "operator norm multiplying linked-surface embedding motion",
            "operator_norm_boundary_charge_per_surface_norm_over_M_ref",
            "C_S ||delta_v X_S|| / M_ref",
            "MISSING_C_S_OPERATOR_NORM",
            RESIDUALS / "P8_Y5_PARENT_QLOC_2455_BOUNDARY_DATA_ZERO_CERTIFICATE.csv",
            "ZC2455_0_surface_domain",
        ),
        (
            "COEF3001_3_norm_delta_XS",
            "norm_delta_v_X_S",
            "linked-surface/domain displacement under vertical/readout variation",
            "surface_embedding_norm",
            "||delta_v X_S||",
            "MISSING_SOURCE_BLIND_SURFACE_DOMAIN_RULE",
            RESIDUALS / "P8_Y5_NO_SHADOW_2547_SIGNATURE_AUDIT.csv",
            "SIG2547_1_boundary_surface",
        ),
        (
            "COEF3001_4_C_A_Ccap",
            "C_A_C_cap_annulus_transport_norms",
            "operator norms for exterior annulus and cap/collar transport",
            "operator_norm_boundary_charge_per_domain_norm_over_M_ref",
            "C_A ||delta_v A_ext||/M_ref + C_cap ||delta_v caps||/M_ref",
            "MISSING_C_A_C_CAP_AND_DOMAIN_NORMS",
            RESIDUALS / "P8_Y5_R2FR_2900_SOURCE_COMPLEX_OWNER_AUDIT.csv",
            "SC2900_5_exterior_link_complex",
        ),
        (
            "COEF3001_5_Mref",
            "M_ref_tau_surface_denominator",
            "positive same-frame denominator for tau/surface residual",
            "source_mass_or_Hamiltonian_charge",
            "M_ref > 0 in same q/e_obs/tau branch",
            "MISSING_POSITIVE_SAME_FRAME_MREF",
            RESIDUALS / "P8_Y5_OBS_STACK_2588_OWNER_CERTIFICATE.csv",
            "OSC2588_7_MHref",
        ),
        (
            "COEF3001_6_total",
            "epsilon_Bv_tau_surface_commutator_total_abs",
            "absolute no-cancellation sum of tau, surface and annulus/cap terms",
            "dimensionless_after_positive_same_frame_M_ref",
            "sum_abs(COEF3001_0..5) with no cancellation credit",
            "COMPONENTS_MISSING_NO_FINITE_VALUE",
            RESIDUALS / "P8_Y5_R2FR_3000_EPSILON_BV_TAU_SURFACE_BOUND_ROWS.csv",
            "BVT3000_5_total",
        ),
    ]
    return [
        base(
            {
                "coefficient_id": coefficient_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "formula_slot": formula,
                "current_value": current_value,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "source_anchor": anchor,
                "finite_value_present": False,
                "theorem_zero_claimed": False,
                "accepted_for_scoring": False,
                "accepted_for_local_gr": False,
                "no_cancellation_policy": True,
            }
        )
        for coefficient_id, symbol, definition, units, formula, current_value, path, anchor in data
    ]


def first_row() -> list[dict[str, Any]]:
    return [
        base(
            {
                "row_id": "FIRST3001_0_C_tau",
                "symbol": "C_tau_commutator_operator_norm",
                "target_residual": "epsilon_Bv_tau_surface_commutator",
                "required_to_score": "finite C_tau; finite norm_delta_v_tau or theorem-zero tau owner; positive same-frame M_ref; source path; units; no observed-GM import",
                "current_value": "MISSING_C_TAU_NUMERIC_OR_THEOREM_ZERO",
                "units": "operator_norm_boundary_charge_per_tau_norm_over_M_ref",
                "source_path": str(RESIDUALS / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_DELTA_TAU_SOURCE_PACK.csv"),
                "source_path_exists": (RESIDUALS / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_DELTA_TAU_SOURCE_PACK.csv").exists(),
                "source_anchor": "DTS2599_12_C_Tobs_tau",
                "finite_value_present": False,
                "valid_for_local_tests": False,
                "accepted_for_scoring": False,
            }
        )
    ]


def demotion_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DEM3001_0_tau_surface_zero",
            "epsilon_Bv_tau_surface_commutator=0 route",
            "DEMOTED_TO_PARENT_SIGNATURE_CONTRACT_ONLY",
            "tau/surface zero requires owner signatures not present in current corpus",
        ),
        (
            "DEM3001_1_tau_surface_numeric",
            "finite tau/surface coefficient route",
            "STAGED_NOT_SCORE_READY",
            "first coefficient row exists but no finite coefficient value or M_ref is sourced",
        ),
        (
            "DEM3001_2_Bv_program",
            "Bv component program",
            "MOVE_TO_CORNER_TOPOLOGICAL_CLASSIFICATION",
            "tau/surface route is now an explicit residual, so do not loop it again",
        ),
    ]
    return [
        base(
            {
                "demotion_id": demotion_id,
                "route": route,
                "status": status,
                "reason": reason,
            }
        )
        for demotion_id, route, status, reason in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE3001_0_owner_pack_audited", "tau/surface owner pack audited", "PASS", True, False, "owner clauses inspected against 2599/2455/2547/2588/2900"),
        ("GATE3001_1_owner_pack_signed", "tau/surface owner pack signed", "BLOCKED_NONCLAIM", False, False, "tau identity, boundary clock, surface/domain and M_ref remain missing"),
        ("GATE3001_2_first_coefficient_row", "first C_tau coefficient row exists", "PASS_SCHEMA_ONLY", True, False, "row is source-ready but value is missing"),
        ("GATE3001_3_finite_coefficient_value", "finite C_tau or tau/surface coefficient value exists", "BLOCKED_NONCLAIM", False, False, "no numeric/theorem-zero coefficient found"),
        ("GATE3001_4_tau_surface_zero", "epsilon_Bv_tau_surface_commutator=0 can be promoted", "FAIL_CLOSED", False, False, "owner signatures absent"),
        ("GATE3001_5_tau_surface_score", "epsilon_Bv_tau_surface_commutator can be scored", "FAIL_CLOSED", False, False, "finite coefficients, derivative norms and M_ref absent"),
        ("GATE3001_6_full_Bv_zero", "epsilon_Bv_ambiguity=0", "FAIL_CLOSED", False, False, "corner/topological/unfixed-reference/projector/Mref debts remain"),
        ("GATE3001_7_local_GR_Newton_PPN", "local GR/Newton/PPN claim allowed", "FAIL_CLOSED", False, False, "coefficient schema does not close local reduction"),
    ]
    return [
        base(
            {
                "gate_id": gate_id,
                "gate": gate,
                "gate_status": status,
                "condition_passed": passed,
                "promotion_allowed_now": promotion,
                "reason": reason,
                "accepted_for_local_gr": False,
            }
        )
        for gate_id, gate, status, passed, promotion, reason in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DEC3001_0_owner_rejected",
            "Do not promote the tau/surface owner pack.",
            "Every necessary source says tau identity, boundary-clock owner, surface/domain fix, and M_ref are unsigned.",
            "zero theorem remains a future parent-signature contract",
        ),
        (
            "DEC3001_1_coefficient_not_filled",
            "Do not fabricate C_tau or C_S/C_A coefficients.",
            "Existing tables provide formulas and source anchors, not finite values.",
            "first C_tau row is staged nonclaim",
        ),
        (
            "DEC3001_2_demote_route",
            "Demote tau/surface route to explicit residual closure for now.",
            "We have a clean zero condition and a clean bound schema; repeating it would circle.",
            "move to corner/topological Bv classification",
        ),
        (
            "DEC3001_3_next",
            "Select corner/topological Bv classification next.",
            "These are the next unexamined Bv remainder terms after exact and tau/surface components.",
            "3002 should classify corner and topological rows or stage bounds",
        ),
    ]
    return [
        base(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "effect": effect,
            }
        )
        for decision_id, decision, because, effect in data
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "next_id": "NEXT3001_0_3002",
                "priority": "selected_primary",
                "target_doc": "3002-Y5-R2FR-corner-topological-Bv-classification-or-third-boundary-component-bound-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_corner_topological_Bv_classification_or_third_boundary_component_bound_under_AX1090_3002.py",
                "mission": "Classify the remaining Bv corner and topological terms: corner/codimension-two anomaly, relative cohomology/topological class, and closed-but-not-exact flux. Prove a proper/exact/topological zero if parent-owned, otherwise stage source-backed epsilon_Bv_corner_abs and epsilon_Bv_topological_abs bound rows.",
                "success_condition": "corner/topological Bv component becomes theorem-zero or finite source-backed without treating exact/fixed Bv or tau/surface closure as full Bv zero",
                "fallback_condition": "if classification is unsigned and no value exists, keep the components as explicit residual rows and move to unfixed-reference/projector-boundary terms",
                "guardrails": "no full Bv zero claim; no epsilon_kernel_charge claim; no local-GR/Newton/PPN/WEP/R10 claim; no GitHub; no formalization-workbench edits",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "copy_id": copy_id,
                "destination": str(destination),
                "copy_exists": destination.exists(),
                "row_count": len(rows(destination)) if destination.exists() else 0,
                "parse_ok": csv_ok(destination) if destination.exists() else False,
            }
        )
        for copy_id, destination in BRANCH_OUTPUTS.items()
    ]


def validation_rows(
    source_output_rows: list[dict[str, Any]],
    owner_output_rows: list[dict[str, Any]],
    coefficient_output_rows: list[dict[str, Any]],
    first_output_rows: list[dict[str, Any]],
    demotion_output_rows: list[dict[str, Any]],
    gate_output_rows: list[dict[str, Any]],
    branch_output_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    sources_ok = all(boolish(row["path_exists"]) for row in source_output_rows)
    anchors_ok = all(boolish(row["anchors_found"]) for row in source_output_rows)
    owner_rejected = any(row["owner_id"] == "OWN3001_9_verdict" and row["current_status"] == "OWNER_PACK_NOT_SIGNED_NO_FINITE_COEFFICIENT_VALUE" for row in owner_output_rows)
    coefficients_staged = any(row["coefficient_id"] == "COEF3001_6_total" and row["current_value"] == "COMPONENTS_MISSING_NO_FINITE_VALUE" for row in coefficient_output_rows)
    first_row_staged = any(row["row_id"] == "FIRST3001_0_C_tau" and not boolish(row["finite_value_present"]) for row in first_output_rows)
    route_demoted = any(row["demotion_id"] == "DEM3001_2_Bv_program" and row["status"] == "MOVE_TO_CORNER_TOPOLOGICAL_CLASSIFICATION" for row in demotion_output_rows)
    local_claim_false = any(row["gate_id"] == "GATE3001_7_local_GR_Newton_PPN" and not boolish(row["condition_passed"]) for row in gate_output_rows)
    branch_ok = all(boolish(row["copy_exists"]) and boolish(row["parse_ok"]) for row in branch_output_rows)
    csv_parse_ok = all(csv_ok(path) for path in output_paths if path.exists() and path.suffix == ".csv")
    outputs_under_post = all(under(path, ROOT) for path in output_paths + [DOC])
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_patterns = [
            "*Y5_R2FR_3001*",
            "*3001-Y5-R2FR*",
            "*tau_surface_owner_source_pack_3001*",
            "*commutator_coefficient_acquisition_rows_3001*",
            "*JR3001_CORNER_TOPOLOGICAL*",
        ]
        formalization_count = sum(
            1
            for pattern in formalization_patterns
            for path in FORMALIZATION.rglob(pattern)
            if path.is_file()
        )
    no_claim_flags = True
    for output_path in output_paths:
        if output_path.exists() and output_path.suffix == ".csv":
            for output_row in rows(output_path):
                for key in ("valid_for_claim", "claim_allowed", "promotion_allowed_now", "accepted_for_local_gr", "accepted_for_scoring", "valid_for_local_tests"):
                    if str(output_row.get(key, "")).strip().lower() == "true":
                        no_claim_flags = False
    data = [
        ("VAL3001_0_sources_exist", sources_ok, "all cited local source paths exist"),
        ("VAL3001_1_anchors_found", anchors_ok, "all cited anchors are found"),
        ("VAL3001_2_owner_rejected", owner_rejected, "tau/surface owner source pack is rejected for current MTS"),
        ("VAL3001_3_coefficients_staged", coefficients_staged, "commutator coefficient acquisition rows are staged"),
        ("VAL3001_4_first_row_nonfinite", first_row_staged, "first C_tau coefficient row exists but has no finite value"),
        ("VAL3001_5_route_demoted", route_demoted, "tau/surface route is demoted to residual closure and next Bv component selected"),
        ("VAL3001_6_local_claim_false", local_claim_false, "local GR/Newton/PPN gate remains false"),
        ("VAL3001_7_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL3001_8_csvs_parse", csv_parse_ok, "all generated CSVs parse"),
        ("VAL3001_9_outputs_under_post", outputs_under_post, "all outputs are under post-checkpoint-work"),
        ("VAL3001_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL3001_11_formalization_clean", formalization_count == 0, f"no 3001 outputs in formalization-workbench (count={formalization_count})"),
        ("VAL3001_12_doc_written", DOC.exists(), "3001 markdown checkpoint exists"),
    ]
    overall = all(passed for _, passed, _ in data)
    data.append(("VAL3001_OVERALL", overall, "3001 rejects tau/surface owner and finite coefficient promotion, stages the first C_tau row as nonclaim, demotes the route to explicit residual closure, and selects corner/topological Bv classification next"))
    return [
        base(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": True,
            }
        )
        for validation_id, passed, check in data
    ]


def write_doc(
    source_output_rows: list[dict[str, Any]],
    owner_output_rows: list[dict[str, Any]],
    coefficient_output_rows: list[dict[str, Any]],
    first_output_rows: list[dict[str, Any]],
    demotion_output_rows: list[dict[str, Any]],
    gate_output_rows: list[dict[str, Any]],
    decision_output_rows: list[dict[str, Any]],
    next_output_rows: list[dict[str, Any]],
    branch_output_rows: list[dict[str, Any]],
    validation_output_rows: list[dict[str, Any]],
) -> None:
    document = f"""# 3001 - Y5/R2FR Tau-Surface Owner Source Pack Or First Commutator Coefficient Value Under AX1090

Status: `Y5_R2FR_3001_tau_surface_owner_not_signed_first_Ctau_row_staged_nonfinite_corner_topological_3002_next`

Claim ceiling: `no_tau_surface_zero_claim_no_commutator_score_claim_no_full_Bv_zero_claim_no_epsilon_kernel_charge_claim_no_local_GR_no_Newton_no_PPN_no_WEP_no_R10_no_GitHub_no_formalization_edit`

## Current Verdict

3001 checks whether the 3000 tau/surface commutator can be closed by existing source material.

It cannot. The corpus has useful schemas: boundary-clock tau rows, source-blind boundary-reference rows, and operator-norm bound formulas. But it does not contain a parent-signed tau identity, source-blind linked surface/domain rule, positive same-frame `M_ref`, or finite `C_tau/C_S/C_A/C_cap` coefficient values.

So the tau/surface route is now explicit residual closure only. The first coefficient row, `C_tau_commutator_operator_norm`, is staged with units and source anchors, but no finite value is fabricated. The next useful move is not another tau loop; it is corner/topological `B_v` classification.

## Source Register

{md_table(source_output_rows, ["source_id", "path_exists", "anchors_found", "missing_anchors", "role"])}

## Tau-Surface Owner Source Pack Audit

{md_table(owner_output_rows, ["owner_id", "required_object", "current_status", "reason", "residual_if_missing"])}

## Commutator Coefficient Acquisition Rows

{md_table(coefficient_output_rows, ["coefficient_id", "symbol", "formula_slot", "current_value", "units", "source_anchor"])}

## First Commutator Coefficient Row

{md_table(first_output_rows, ["row_id", "symbol", "current_value", "units", "required_to_score"])}

## Tau-Surface Route Demotion Ledger

{md_table(demotion_output_rows, ["demotion_id", "route", "status", "reason"])}

## Promotion Gates

{md_table(gate_output_rows, ["gate_id", "gate", "gate_status", "condition_passed", "promotion_allowed_now", "reason"])}

## Decision Ledger

{md_table(decision_output_rows, ["decision_id", "decision", "because", "effect"])}

## Next Target

{md_table(next_output_rows, ["next_id", "target_doc", "mission", "success_condition", "guardrails"])}

## Branch Copies

{md_table(branch_output_rows, ["copy_id", "destination", "copy_exists", "row_count", "parse_ok", "valid_for_claim"])}

## Validation

{md_table(validation_output_rows, ["validation_id", "passed", "check", "required"])}

## Plain-English Takeaway

This is a disciplined no. The tau/surface path has a clean theorem shape and a clean bound formula, but no live coefficient or owner signature. That is still progress: we have stopped it being a ghost objection, and we have stopped it being fake evidence. Next we work the remaining `B_v` pieces: corner and topological charge.

## Forbidden Claims From 3001

- `epsilon_Bv_tau_surface_commutator=0`.
- A finite score-ready `C_tau`, `C_S`, `C_A`, `C_cap`, or tau/surface residual.
- `epsilon_Bv_ambiguity=0`.
- `epsilon_kernel_charge_public_SRNG=0` or score-ready.
- Public `SRNG/OFC`, source-normalized Newton, PPN, WEP, R10, clock safety, orbital safety or local GR.
"""
    DOC.write_text(document, encoding="utf-8")


def main() -> None:
    source_output_rows = source_rows()
    owner_output_rows = owner_rows()
    coefficient_output_rows = coefficient_rows()
    first_output_rows = first_row()
    demotion_output_rows = demotion_rows()
    gate_output_rows = gate_rows()
    decision_output_rows = decision_rows()
    next_output_rows = next_rows()

    write_csv(OUTPUTS["sources"], source_output_rows)
    write_csv(OUTPUTS["owner"], owner_output_rows)
    write_csv(OUTPUTS["coefficients"], coefficient_output_rows)
    write_csv(OUTPUTS["first_row"], first_output_rows)
    write_csv(OUTPUTS["demotion"], demotion_output_rows)
    write_csv(OUTPUTS["gates"], gate_output_rows)
    write_csv(OUTPUTS["decision"], decision_output_rows)
    write_csv(OUTPUTS["next"], next_output_rows)

    shutil.copyfile(OUTPUTS["owner"], BRANCH_OUTPUTS["owner_copy"])
    shutil.copyfile(OUTPUTS["coefficients"], BRANCH_OUTPUTS["coeff_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

    branch_output_rows = branch_rows()
    write_csv(OUTPUTS["branches"], branch_output_rows)

    DOC.write_text("", encoding="utf-8")
    validation_output_rows = validation_rows(
        source_output_rows,
        owner_output_rows,
        coefficient_output_rows,
        first_output_rows,
        demotion_output_rows,
        gate_output_rows,
        branch_output_rows,
    )
    write_csv(OUTPUTS["validation"], validation_output_rows)

    write_doc(
        source_output_rows,
        owner_output_rows,
        coefficient_output_rows,
        first_output_rows,
        demotion_output_rows,
        gate_output_rows,
        decision_output_rows,
        next_output_rows,
        branch_output_rows,
        validation_output_rows,
    )


if __name__ == "__main__":
    main()
