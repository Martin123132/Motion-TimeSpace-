from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1709"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1709-Y5-R2FR-primitive-minimality-no-higher-derivative-or-first-R11-component-fill.md"

SOURCE_FILES = {
    "1708_doc": ROOT / "1708-Y5-R2FR-EH-core-operator-refresh-after-WEP-demotion-or-R11-priority-fill.md",
    "1708_validation": OUT / "P8_Y5_BRR545_1708_VALIDATION.csv",
    "1708_next": OUT / "P8_Y5_PARENT_QLOC_1708_NEXT_TARGET.csv",
    "1708_r11_contract": OUT / "P8_Y5_PARENT_QLOC_1708_R11_PRIORITY_FILL_CONTRACT.csv",
    "1513_doc": ROOT / "1513-Y5-parent-primitive-minimality-no-higher-derivative-theorem-or-R11-vector-lock.md",
    "1513_validation": OUT / "P8_Y5_BRR545_1513_VALIDATION.csv",
    "1513_primitive": OUT / "P8_Y5_PARENT_MINIMALITY_1513_PRIMITIVE_THEOREM_AUDIT.csv",
    "1513_generators": OUT / "P8_Y5_PARENT_MINIMALITY_1513_LOCAL_INVARIANT_GENERATOR_LOCK.csv",
    "1513_countermodels": OUT / "P8_Y5_PARENT_MINIMALITY_1513_COUNTERMODEL_LEDGER.csv",
    "1513_r11_lock": OUT / "P8_Y5_PARENT_MINIMALITY_1513_R11_VECTOR_LOCK.csv",
    "1586_minimality": OUT / "P8_Y5_PARENT_QLOC_1586_MINIMALITY_SIGNATURE_ATTEMPT.csv",
    "1587_doc": ROOT / "1587-Y5-R11-beta-vector-first-component-fill-R2FR-RicciWeyl-or-nohair.md",
    "1587_nohair": OUT / "P8_Y5_PARENT_QLOC_1587_R2FR_RICCIWEYL_NOHAIR_ATTEMPT.csv",
    "1587_fill": OUT / "P8_Y5_PARENT_QLOC_1587_FIRST_COMPONENT_FILL_ROWS.csv",
    "1587_bounds": OUT / "P8_Y5_PARENT_QLOC_1587_BOUND_INTERFACE_REQUIREMENTS.csv",
    "1588_doc": ROOT / "1588-Y5-R2FR-scalaron-coefficient-map-or-full-curve-bound-intake.md",
    "1588_scalaron": OUT / "P8_Y5_PARENT_QLOC_1588_R2FR_SCALARON_MAP.csv",
    "1588_curve": OUT / "P8_Y5_PARENT_QLOC_1588_FULL_CURVE_INTAKE_STATUS.csv",
    "1588_smoke": OUT / "P8_Y5_PARENT_QLOC_1588_R2FR_NONCLAIM_SMOKE_ROWS.csv",
}

NEEDLES = {
    "1708_doc": ["NO_EH_CLAIM", "NEXT1708_0_primary"],
    "1708_validation": ["VAL1708_OVERALL", "PASS"],
    "1708_next": ["1709-Y5-R2FR-primitive-minimality-no-higher-derivative-or-first-R11-component-fill.md", "selected"],
    "1708_r11_contract": ["R11F1708_0_R2_fR", "R11F1708_1_torsion_nonmetricity"],
    "1513_doc": ["THEOREM_NOT_PROVEN_CURRENT_CORPUS", "NEXT_1514_GENERATOR_ELIMINATION"],
    "1513_validation": ["VAL1513_12_overall", "PASS"],
    "1513_primitive": ["PM1513_6_verdict", "THEOREM_NOT_PROVEN_CURRENT_CORPUS"],
    "1513_generators": ["GEN1513_3_domain_selector", "NOT_ELIMINATED"],
    "1513_countermodels": ["CM1513_0_EH_plus_R2", "LIVE"],
    "1513_r11_lock": ["R11LOCK1513_01", "R2_fR_scalar_mode"],
    "1586_minimality": ["MIN1586_5_verdict", "FAIL_CURRENT_CLAIM_MINIMALITY_NOT_DERIVED"],
    "1587_doc": ["R2/f(R) zero route is mathematically clean only as a relative theorem", "FC1587_0_R2FR"],
    "1587_nohair": ["NH1587_6_verdict", "FAIL_CURRENT_CLAIM_FIRST_COMPONENTS_NOT_DERIVED"],
    "1587_fill": ["FC1587_0_R2FR", "MISSING_PARENT_COEFFICIENT_AND_FULL_CURVE"],
    "1587_bounds": ["BI1587_0_R2FR_R10_curve", "MISSING_FULL_CURVE_AND_PREDICTION"],
    "1588_doc": ["MTS_COEFFICIENT_SIDE_IS_NOW_THE_BOTTLENECK", "do not backsolve"],
    "1588_scalaron": ["SC1588_1_formula", "FORMULA_AVAILABLE_PARENT_COEFFICIENT_MISSING"],
    "1588_curve": ["CURVE1588_1_review_candidate", "390"],
    "1588_smoke": ["SMOKE1588_1_anchor_backsolve", "FORBIDDEN_BOUND_TO_PREDICTION_INVERSION"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1709_SOURCE_REGISTER.csv"
MINIMALITY_RETEST = OUT / "P8_Y5_PARENT_QLOC_1709_PRIMITIVE_MINIMALITY_RETEST.csv"
GENERATOR_SURVIVAL = OUT / "P8_Y5_PARENT_QLOC_1709_LOCAL_GENERATOR_SURVIVAL.csv"
COUNTERMODEL_SURVIVAL = OUT / "P8_Y5_PARENT_QLOC_1709_COUNTERMODEL_SURVIVAL.csv"
R11_LOCK_UPDATE = OUT / "P8_Y5_PARENT_QLOC_1709_R11_VECTOR_LOCK_UPDATE.csv"
FIRST_COMPONENT_INTERFACE = OUT / "P8_Y5_PARENT_QLOC_1709_FIRST_R11_COMPONENT_INTERFACE.csv"
SCALARON_HANDOFF = OUT / "P8_Y5_PARENT_QLOC_1709_R2FR_SCALARON_HANDOFF.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_PARENT_QLOC_1709_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1709_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1709_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1709_VALIDATION.csv"

GENERATED_CSVS = [
    SOURCE_REGISTER,
    MINIMALITY_RETEST,
    GENERATOR_SURVIVAL,
    COUNTERMODEL_SURVIVAL,
    R11_LOCK_UPDATE,
    FIRST_COMPONENT_INTERFACE,
    SCALARON_HANDOFF,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED_CSVS = [
    MINIMALITY_RETEST,
    GENERATOR_SURVIVAL,
    COUNTERMODEL_SURVIVAL,
    R11_LOCK_UPDATE,
    FIRST_COMPONENT_INTERFACE,
    SCALARON_HANDOFF,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    MINIMALITY_RETEST: [
        QUARANTINE / "PRIMITIVE_MINIMALITY_RETEST.csv",
        BRANCH_RESIDUALS / "R2FR_primitive_minimality_retest_1709.csv",
        QUEUE / "JR1709_PRIMITIVE_MINIMALITY_RETEST.csv",
    ],
    GENERATOR_SURVIVAL: [
        QUARANTINE / "LOCAL_GENERATOR_SURVIVAL.csv",
        BRANCH_RESIDUALS / "R2FR_local_generator_survival_1709.csv",
        QUEUE / "JR1709_LOCAL_GENERATOR_SURVIVAL.csv",
    ],
    R11_LOCK_UPDATE: [
        QUARANTINE / "R11_VECTOR_LOCK_UPDATE.csv",
        BRANCH_RESIDUALS / "R2FR_R11_vector_lock_update_1709.csv",
        QUEUE / "JR1709_R11_VECTOR_LOCK_UPDATE.csv",
    ],
    FIRST_COMPONENT_INTERFACE: [
        QUARANTINE / "FIRST_R11_COMPONENT_INTERFACE.csv",
        BRANCH_RESIDUALS / "R2FR_first_R11_component_interface_1709.csv",
        QUEUE / "JR1709_FIRST_R11_COMPONENT_INTERFACE.csv",
    ],
    SCALARON_HANDOFF: [
        QUARANTINE / "R2FR_SCALARON_HANDOFF.csv",
        BRANCH_RESIDUALS / "R2FR_scalaron_handoff_1709.csv",
        QUEUE / "JR1709_R2FR_SCALARON_HANDOFF.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1709.csv",
        QUEUE / "JR1709_NEXT_TARGET.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_1709.csv",
        QUEUE / "JR1709_CLAIM_GATE.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _field in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_key, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC1709_{index}_{source_key}",
                "source_key": source_key,
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "required_needles": ";".join(needles),
                "use_in_1709": "primitive minimality retest and first R11 component interface",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def minimality_retest_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PMR1709_0_object_language",
            "primitive parent object language generated only by motion/time/space, observed geometry, matter reps and constants",
            "TARGET_RESTATED_NOT_DERIVED",
            "would exclude extra local scalar/vector/domain/marker targets before variation",
            "universal-property/no-extension theorem still absent",
        ),
        (
            "PMR1709_1_no_marker",
            "no natural marker, class scalar, material label or hidden-visible coefficient morphism",
            "NOT_DERIVED",
            "would kill F(sigma)R and source/source-only marker prefactors",
            "covariant material markers and local invariant scalars remain legal",
        ),
        (
            "PMR1709_2_no_integrated_tower",
            "no integrated-out auxiliary/projector/memory tower generating f(R), R^2, Ricci^2, Weyl^2 or nonlocal kernels",
            "NOT_DERIVED",
            "would protect the EH second-order selector after eliminating hidden sectors",
            "auxiliary scalar and nonlocal memory countermodels survive",
        ),
        (
            "PMR1709_3_no_extra_stress",
            "no extra local propagating stress/source carriers",
            "ACTIVE_PRIMARY_OBSTRUCTION",
            "would make R11 vector mostly theorem-zero",
            "scalar, vector, torsion/nonmetricity, projector/domain and memory rows remain live",
        ),
        (
            "PMR1709_4_second_order_filter",
            "local tested exterior equations are second order in observed metric/coframe",
            "CENTRAL_BLOCKER_NOT_DERIVED",
            "would activate the Lovelock/EH selector route",
            "R2/fR, Ricci/Weyl and nonlocal rows are still legal",
        ),
        (
            "PMR1709_5_verdict",
            "primitive minimality/no-higher-derivative theorem",
            "THEOREM_NOT_PROVEN_CURRENT_CORPUS",
            "would promote EH operator route if signed with no-extra-field clauses",
            "lock first R11 components as nonclaim fill rows",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "theorem_piece": theorem_piece,
            "current_status": status,
            "effect_if_signed": effect,
            "blocking_gap": gap,
            "parent_signed": False,
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for attempt_id, theorem_piece, status, effect, gap in rows
    ]


def generator_survival_rows() -> list[dict[str, Any]]:
    rows = [
        ("GEN1709_0_finite_cell_spectrum", "finite-cell/fibre spectrum", "NOT_ELIMINATED", "can feed marker-prefactors or local residual coefficients"),
        ("GEN1709_1_domain_selector", "domain selector chi_D", "NOT_ELIMINATED", "can source projector/domain stress and preferred-location effects"),
        ("GEN1709_2_memory_class_scalar", "memory/class scalar", "NOT_ELIMINATED", "can regenerate f(R)-like or nonlocal kernels"),
        ("GEN1709_3_species_constants", "species constants theta_A(I_Q)", "NOT_ELIMINATED", "can re-enter source normalization and WEP channels"),
        ("GEN1709_4_orientation_time_arrow", "orientation/time-arrow marker", "NOT_CLASSIFIED", "could affect readout, dissipation or parity/time branches"),
        ("GEN1709_5_readout_projector", "post-readout projector/reduced-action marker", "POLICY_BLOCKED_NOT_THEOREM_BLOCKED", "cannot be used as absence theorem"),
        ("GEN1709_6_boundary_topological_marker", "boundary/topological marker", "CONDITIONALLY_SAFE_NOT_DERIVED", "safe only after exact topological/no-flux proof"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "generator_id": generator_id,
            "generator": generator,
            "local_status": status,
            "why_it_matters": why,
            "blocks_no_marker": True,
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for generator_id, generator, status, why in rows
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        ("CM1709_0_EH_plus_R2", "S_EH + epsilon int sqrt(-g) R^2", "LIVE", "kills pure EH unless no-higher-derivative or c_R2=0 is parent-signed"),
        ("CM1709_1_auxiliary_scalar", "hidden scalar integrated out into beta^2 R^2/(2M^2)", "LIVE", "regenerates f(R) after apparently harmless elimination"),
        ("CM1709_2_marker_prefactor", "F(sigma_marker) R", "LIVE", "covariant marker/class scalar can alter EH prefactor"),
        ("CM1709_3_RicciWeyl", "Ricci^2/Weyl^2 generic curvature-squared operator", "LIVE", "not killed by broad Gauss-Bonnet language"),
        ("CM1709_4_connection", "independent torsion/nonmetricity sector", "LIVE", "blocks Levi-Civita and universal readout/source connection"),
        ("CM1709_5_domain_projector", "domain selector/projector stress", "LIVE", "feeds preferred-frame/location and q_loc/Qnorm channels"),
        ("CM1709_6_nonlocal_memory", "R Box^-1 R or compact history kernel", "LIVE", "adds range/time-drift/source normalization tails"),
        ("CM1709_7_source_normalization", "domain-dependent G_eff/M_eff operator", "LIVE", "blocks Newton measured-GM and beta/source denominator"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": countermodel_id,
            "countermodel": countermodel,
            "current_status": status,
            "damage": damage,
            "currently_killed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for countermodel_id, countermodel, status, damage in rows
    ]


def r11_lock_rows() -> list[dict[str, Any]]:
    families = [
        ("R11LOCK1709_00", "boundary_topological_terms"),
        ("R11LOCK1709_01", "R2_fR_scalar_mode"),
        ("R11LOCK1709_02", "Ricci_Weyl_squared"),
        ("R11LOCK1709_03", "scalar_tensor_class_metric"),
        ("R11LOCK1709_04", "vector_preferred_frame"),
        ("R11LOCK1709_05", "torsion_nonmetricity"),
        ("R11LOCK1709_06", "bulk_X_force_law"),
        ("R11LOCK1709_07", "nonlocal_memory_kernel"),
        ("R11LOCK1709_08", "source_normalization_operator"),
        ("R11LOCK1709_09", "projector_domain_stress"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "lock_id": lock_id,
            "operator_family": family,
            "lock_status": "ACTIVE_LOCAL_OPERATOR_BRANCH_UNTIL_ZERO_OR_BOUND",
            "reason": "primitive minimality/no-higher-derivative retest did not close",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for lock_id, family in families
    ]


def first_component_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FC1709_0_R2FR",
            "R2_fR_scalar_mode",
            "delta_beta_R2_fR / finite scalaron alpha(lambda)",
            "c_R2_or_c_fR",
            "length^2_or_inverse_mass_squared_after_EH_normalization",
            "HIGHEST_FIRST",
            "coefficient value/sign/units, f_RR normalization, scalaron mass/range, alpha_s coupling, screening flag, source path",
            "PPN_gamma_beta;R10_alpha_lambda;clock_orbital_range",
        ),
        (
            "FC1709_1_torsion_nonmetricity",
            "torsion_nonmetricity",
            "connection/readout/source beta and WEP leakage",
            "c_T_or_c_Q",
            "declared_connection_response_units",
            "HIGHEST_FIRST_PARALLEL",
            "Levi-Civita theorem or finite torsion/nonmetricity coefficient, spin/light/source response map, source path",
            "WEP;clocks;light_cone;PPN_alpha_i;source_charge",
        ),
        (
            "FC1709_2_RicciWeyl",
            "Ricci_Weyl_squared",
            "delta_beta_Ricci_Weyl / tensor slip",
            "c_Ricci_or_c_Weyl",
            "length^2_or_cutoff_power_after_EH_normalization",
            "SECOND_AFTER_R2FR",
            "coefficient, topological decomposition, weak-field slip/tensor response, boundary policy, source path",
            "PPN_beta_gamma;xi;preferred_location;wave_sector",
        ),
        (
            "FC1709_3_boundary_topology",
            "boundary_topological_combination",
            "boundary/corner/readout flux residual",
            "c_GB_or_boundary_charge",
            "topological_or_boundary_normalized",
            "GUARD_ROW",
            "exact 4D topological combination, boundary no-flux certificate, corner/readout silence, source path",
            "alpha3;xi;Gdot;mass_charge",
        ),
        (
            "FC1709_4_field_redefinition",
            "field_redefinition_escape",
            "observable-equivalence error after curvature operator removal",
            "Delta_redef",
            "dimensionless_equivalence_error",
            "GUARD_ROW",
            "matter/source/readout/boundary equivalence proof or finite residual after redefinition",
            "WEP;clock;gamma;beta;source_normalization",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "fill_id": fill_id,
            "operator_family": family,
            "component": component,
            "coefficient_symbol": coefficient,
            "required_units": units,
            "priority": priority,
            "required_real_input": required,
            "observable_interfaces": interfaces,
            "current_status": "SOURCE_BACKED_VALUE_OR_THEOREM_ZERO_REQUIRED",
            "parent_signed": False,
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for fill_id, family, component, coefficient, units, priority, required, interfaces in rows
    ]


def scalaron_handoff_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SH1709_0_formula",
            "finite R2/fR scalaron formula",
            "m_s^2=1/(6 c_R2), lambda_s=sqrt(6 c_R2), alpha_s=1/3 only for simple unscreened metric f(R)",
            "FORMULA_AVAILABLE_PARENT_COEFFICIENT_MISSING",
            "cannot become MTS prediction without parent c_R2/fRR row",
        ),
        (
            "SH1709_1_curve",
            "R10 bound curve side",
            "390-row 2020 review candidate exists but remains nonclaim; live digitized file is placeholder",
            "CURVE_SIDE_SECONDARY",
            "coefficient side is bottleneck before curve scoring matters",
        ),
        (
            "SH1709_2_anchor_guard",
            "alpha=1 threshold anchors",
            "anchors cannot be inverted to set lambda_s or c_R2",
            "ANCHOR_BACKSOLVE_REFUSED",
            "no prediction-from-bound cheating",
        ),
        (
            "SH1709_3_next_input_pack",
            "first R2/fR input pack",
            "c_R2/fRR, units, sign, normalization, branch context, screening flag, scalar range, alpha_s, source path",
            "NEXT_INPUT_PACK",
            "prepare a strict nonclaim row; score only after values and curve are valid",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "handoff_id": handoff_id,
            "object": obj,
            "formula_or_status": formula,
            "current_status": status,
            "reason": reason,
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for handoff_id, obj, formula, status, reason in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1709_0_minimality_zero", "set R11 vector to zero by primitive minimality", "REFUSE_UNSIGNED_MINIMALITY", "minimality/no-marker/no-integrated-tower theorem is not derived"),
        ("RUN1709_1_R2FR_zero", "set c_R2=c_fR=0", "REFUSE_UNSIGNED_ZERO_THEOREM", "relative theorem exists but parent activator is unsigned"),
        ("RUN1709_2_first_component_score", "score first R11 components", "NOT_RUN_COMPONENTS_MISSING", "coefficient values, units, response maps and source paths are absent"),
        ("RUN1709_3_scalaron_R10", "score scalaron branch against R10", "NOT_RUN_PREDICTION_MISSING", "no MTS c_R2/fRR-derived alpha/lambda prediction exists"),
        ("RUN1709_4_local_gr", "claim local GR/Newton", "BLOCKED_NO_CLAIM", "EH/source/GM/PPN/R11 gates remain open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "score_emitted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, case, status, reason in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NEXT1709_0_primary",
            "1710-Y5-R2FR-R2FR-parent-coefficient-source-hunt-or-scalar-branch-input-pack.md",
            "scripts/Y5_R2FR_R2FR_parent_coefficient_source_hunt_or_scalar_branch_input_pack.py",
            "hunt the parent-owned c_R2/fRR coefficient, units, sign, normalization, screening flag and scalaron map; if unavailable, create the strict first nonclaim input-pack blocker ledger",
            "selected",
        ),
        (
            "NEXT1709_1_parallel_theorem",
            "1710b-Y5-R2FR-local-invariant-generator-domain-selector-elimination.md",
            "scripts/Y5_R2FR_local_invariant_generator_domain_selector_elimination.py",
            "attack the domain selector/projector local invariant generator directly as the theorem-side path",
            "held_parallel",
        ),
        (
            "NEXT1709_2_curve_qa",
            "1710c-Y5-R2FR-R10-review-curve-QA-after-prediction-inputs.md",
            "scripts/Y5_R2FR_R10_review_curve_QA_after_prediction_inputs.py",
            "promote or reject the 390-row R10 review candidate only after an MTS scalaron prediction row exists",
            "held_until_prediction_exists",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "next_target": target,
            "script": script,
            "objective": objective,
            "selection_status": status,
            "success_condition": "source-backed coefficient/theorem-zero input or explicit blocker ledger; no score unless all prediction fields are real",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, target, script, objective, status in rows
    ]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG1709_0_minimality", "primitive minimality/no-higher-derivative theorem", "BLOCKED_NO_CLAIM", "covariant markers, integrated-out towers and local invariant generators survive"),
        ("CG1709_1_EH", "EH operator selected by parent MTS", "BLOCKED_NO_CLAIM", "R11 vector remains active"),
        ("CG1709_2_R2FR_zero", "R2/fR component theorem-zero", "BLOCKED_NO_CLAIM", "relative theorem not activated by parent clauses"),
        ("CG1709_3_R2FR_score", "finite scalaron/R10/PPN score", "BLOCKED_NO_CLAIM", "parent c_R2/fRR prediction missing"),
        ("CG1709_4_torsion_LC", "Levi-Civita/torsion silence", "BLOCKED_NO_CLAIM", "connection theorem or residual map missing"),
        ("CG1709_5_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "operator/source/GM/PPN/R11 gates not closed together"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in rows
    ]


def parse_all(paths: list[Path]) -> bool:
    for path in paths:
        read_csv(path)
    return True


def claim_flags_false(paths: list[Path]) -> bool:
    checked_keys = {
        "accepted_for_scoring",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "theorem_proven",
        "gate_pass",
        "score_emitted",
        "parent_signed",
        "numeric_value_present",
        "source_backed",
        "currently_killed",
    }
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in checked_keys and truthy(value):
                    return False
    return True


def formalization_1709_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [
        path
        for path in FORMALIZATION.rglob("*1709*")
        if path.is_file() and ".venv" not in path.parts and "__pycache__" not in path.parts
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    source_rows: list[dict[str, Any]],
    minimality_rows: list[dict[str, Any]],
    generator_rows: list[dict[str, Any]],
    countermodel_rows_: list[dict[str, Any]],
    r11_rows: list[dict[str, Any]],
    component_rows: list[dict[str, Any]],
    scalaron_rows: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    remove_pycache()
    checks = [
        ("VAL1709_0_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL1709_1_needles_present", all(row["needles_present"] for row in source_rows), "required source needles are present"),
        (
            "VAL1709_2_minimality_retested_open",
            any(row["attempt_id"] == "PMR1709_5_verdict" and row["current_status"] == "THEOREM_NOT_PROVEN_CURRENT_CORPUS" for row in minimality_rows),
            "primitive minimality retest remains open",
        ),
        (
            "VAL1709_3_generators_survive",
            len(generator_rows) >= 7 and any(row["generator_id"] == "GEN1709_1_domain_selector" for row in generator_rows),
            "local invariant generators remain explicit blockers",
        ),
        (
            "VAL1709_4_countermodels_live",
            len(countermodel_rows_) >= 8 and all(row["current_status"] == "LIVE" for row in countermodel_rows_),
            "countermodel survival ledger keeps non-EH alternatives live",
        ),
        (
            "VAL1709_5_R11_vector_locked",
            len(r11_rows) >= 10 and any(row["operator_family"] == "R2_fR_scalar_mode" for row in r11_rows),
            "R11 vector locked as active local operator branch",
        ),
        (
            "VAL1709_6_first_components_ready_nonclaim",
            component_rows[0]["operator_family"] == "R2_fR_scalar_mode"
            and component_rows[1]["operator_family"] == "torsion_nonmetricity",
            "first component interface prioritizes R2/fR and torsion/nonmetricity",
        ),
        (
            "VAL1709_7_scalaron_handoff_blocks",
            any(row["handoff_id"] == "SH1709_0_formula" and row["current_status"] == "FORMULA_AVAILABLE_PARENT_COEFFICIENT_MISSING" for row in scalaron_rows),
            "scalaron formula available but no MTS coefficient prediction promoted",
        ),
        (
            "VAL1709_8_runner_blocks",
            all("CLAIM" in row["status"] or "REFUSE" in row["status"] or "NOT_RUN" in row["status"] for row in runner_rows_),
            "runner blocks all theorem-zero, score and local-GR shortcuts",
        ),
        (
            "VAL1709_9_next_selected",
            any(row["route_id"] == "NEXT1709_0_primary" and row["selection_status"] == "selected" for row in next_rows_),
            "next target selects R2/fR coefficient/source hunt or scalar input pack",
        ),
        (
            "VAL1709_10_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows_),
            "all claim gates remain blocked",
        ),
        ("VAL1709_11_csv_parse", parse_all(GENERATED_CSVS), "all generated 1709 CSVs parse"),
        (
            "VAL1709_12_no_claim_flags",
            claim_flags_false(CLAIM_CHECKED_CSVS),
            "all generated scoring and claim flags remain false",
        ),
        (
            "VAL1709_13_branch_copies",
            all(target.exists() for targets in COPY_TARGETS.values() for target in targets),
            "branch/quarantine/queue copies exist",
        ),
        (
            "VAL1709_14_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1709_15_formalization_untouched",
            not formalization_1709_hits(),
            "no 1709 outputs found under formalization-workbench",
        ),
    ]
    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1709_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1709 primitive minimality retest and first R11 component interface validation",
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    minimality_rows: list[dict[str, Any]],
    generator_rows: list[dict[str, Any]],
    countermodel_rows_: list[dict[str, Any]],
    r11_rows: list[dict[str, Any]],
    component_rows: list[dict[str, Any]],
    scalaron_rows: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    content = "\n\n".join(
        [
            "# 1709 - Primitive Minimality / No-Higher-Derivative Or First R11 Component Fill",
            "## Verdict\n"
            "- The derivation-first path was tested again after the WEP cleanup.\n"
            "- Primitive minimality/no-natural-marker/no-higher-derivative still does not close from the current corpus.\n"
            "- That does not kill the project; it means the honest local-GR route is now an active R11 residual branch until components are theorem-zeroed or source-bounded.\n"
            "- First fill priority is `R2_fR_scalar_mode`, with `torsion_nonmetricity` in parallel because Levi-Civita ownership is equally upstream.\n"
            "- No EH, Newton, PPN, R10, WEP, clock, orbital or local-GR claim is made.",
            "## Source Register\n" + table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present"]),
            "## Primitive Minimality Retest\n"
            + table(minimality_rows, ["attempt_id", "theorem_piece", "current_status", "effect_if_signed", "blocking_gap"]),
            "## Local Generator Survival\n"
            + table(generator_rows, ["generator_id", "generator", "local_status", "why_it_matters"]),
            "## Countermodel Survival\n"
            + table(countermodel_rows_, ["countermodel_id", "countermodel", "current_status", "damage"]),
            "## R11 Vector Lock Update\n"
            + table(r11_rows, ["lock_id", "operator_family", "lock_status", "reason"]),
            "## First R11 Component Interface\n"
            + table(
                component_rows,
                [
                    "fill_id",
                    "operator_family",
                    "component",
                    "coefficient_symbol",
                    "priority",
                    "required_real_input",
                    "current_status",
                ],
            ),
            "## R2/fR Scalaron Handoff\n"
            + table(scalaron_rows, ["handoff_id", "object", "formula_or_status", "current_status", "reason"]),
            "## Runner Refusal\n" + table(runner_rows_, ["runner_id", "case", "status", "reason"]),
            "## Next Target\n"
            + table(next_rows_, ["route_id", "next_target", "script", "objective", "selection_status"]),
            "## Claim Gates\n" + table(claim_rows_, ["claim_id", "claim", "status", "reason"]),
            "## Validation\n" + table(validation_rows_, ["check_id", "result", "detail"]),
            "## Working Interpretation\n"
            "This is the route getting narrower in a useful way. We did not derive GR yet, but we have stopped asking a vague question. The next real object is a parent-owned `c_R2/fRR` scalaron input pack or a proof it is zero. If that row can be sourced, MTS has a concrete local residual to test; if it cannot, the blocker is clean and named.",
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    minimality_rows = minimality_retest_rows()
    generator_rows = generator_survival_rows()
    countermodel_rows_ = countermodel_rows()
    r11_rows = r11_lock_rows()
    component_rows = first_component_rows()
    scalaron_rows = scalaron_handoff_rows()
    runner_rows_ = runner_rows()
    next_rows_ = next_rows()
    claim_rows_ = claim_rows()

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(MINIMALITY_RETEST, minimality_rows)
    write_csv(GENERATOR_SURVIVAL, generator_rows)
    write_csv(COUNTERMODEL_SURVIVAL, countermodel_rows_)
    write_csv(R11_LOCK_UPDATE, r11_rows)
    write_csv(FIRST_COMPONENT_INTERFACE, component_rows)
    write_csv(SCALARON_HANDOFF, scalaron_rows)
    write_csv(RUNNER_REFUSAL, runner_rows_)
    write_csv(NEXT_TARGET, next_rows_)
    write_csv(CLAIM_GATE, claim_rows_)
    copy_outputs()

    validation_rows_ = validation_rows(
        source_rows,
        minimality_rows,
        generator_rows,
        countermodel_rows_,
        r11_rows,
        component_rows,
        scalaron_rows,
        runner_rows_,
        next_rows_,
        claim_rows_,
    )
    write_csv(VALIDATION, validation_rows_)
    write_doc(
        source_rows,
        minimality_rows,
        generator_rows,
        countermodel_rows_,
        r11_rows,
        component_rows,
        scalaron_rows,
        runner_rows_,
        next_rows_,
        claim_rows_,
        validation_rows_,
    )

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print(f"1709 validation {validation_rows_[-1]['result']}")


if __name__ == "__main__":
    main()
