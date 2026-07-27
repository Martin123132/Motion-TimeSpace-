from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1836"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
P4_RUN = ROOT / "runs" / "20260602-141500-metric-compatibility-Levi-Civita-or-R11-connection-row" / "results"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1836-Y5-R2FR-DeltaGamma-WEP-clock-lightcone-projection-skeleton.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1836_0_1835_next",
        "source_key": "1835_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_NEXT_TARGET.csv",
        "needles": ["NEXT1835_0_primary", "selected"],
        "role": "1835 selects the WEP/clock/lightcone projection skeleton as the primary next target.",
    },
    {
        "source_id": "SRC1836_1_1835_validation",
        "source_key": "1835_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1835_VALIDATION.csv",
        "needles": ["VAL1835_OVERALL", "PASS"],
        "role": "confirms the 1835 observable map passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1836_2_1835_component_map",
        "source_key": "1835_component_observable_map",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_DELTAGAMMA_COMPONENT_OBSERVABLE_MAP.csv",
        "needles": ["DGOM1835_0_spin", "DGOM1835_4_photon_lightcone"],
        "role": "DeltaGamma component rows supply the spin, material, clock, photon and projective channels used here.",
    },
    {
        "source_id": "SRC1836_3_1835_arena_requirements",
        "source_key": "1835_arena_projection_requirements",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_ARENA_PROJECTION_REQUIREMENTS.csv",
        "needles": ["ARENA1835_1_WEP", "ARENA1835_4_LIGHTCONE"],
        "role": "arena rows require P_WEP, P_clock and P_lightcone response operators before scoring.",
    },
    {
        "source_id": "SRC1836_4_1835_score_blockers",
        "source_key": "1835_score_blocker_ledger",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_SCORE_BLOCKER_LEDGER.csv",
        "needles": ["SBL1835_2_projection_matrices", "P_R10, P_WEP, P_PPN, P_clock, P_lightcone, P_orbital"],
        "role": "projection matrices, component values and common units remain explicit blockers.",
    },
    {
        "source_id": "SRC1836_5_P4_template",
        "source_key": "P4_R11_template",
        "source_path": P4_RUN / "P4_R11_template_rows.csv",
        "needles": ["axial_torsion_spin_coupling", "fill_spin_clock_lightcone_WEP_map"],
        "role": "P4 template anchors the spin, Weyl-nonmetricity and lightcone rows as required maps.",
    },
    {
        "source_id": "SRC1836_6_P4_demotions",
        "source_key": "P4_connection_demotions",
        "source_path": P4_RUN / "connection_operator_demotions.csv",
        "needles": ["independent_connection_hypermomentum", "fill hypermomentum/source-charge row"],
        "role": "connection demotion ledger prevents silently deleting matter/source hypermomentum.",
    },
    {
        "source_id": "SRC1836_7_projection_policy",
        "source_key": "1434_projection_policy",
        "source_path": ROOT / "1434-Y5-R10-RAB-local-trace-residual-source-pack-schema-and-bound-map.md",
        "needles": ["REQ1434_1_projection_matrices", "schema exists, but schema is not evidence"],
        "role": "projection rows must be mapped before any local residual score is allowed.",
    },
    {
        "source_id": "SRC1836_8_local_vector_policy",
        "source_key": "482_local_residual_vector",
        "source_path": ROOT / "482-local-residual-vector-from-domain-source-fill.md",
        "needles": ["local residual vector", "no tuned cancellation"],
        "role": "local GR promotion requires every retained component to be theorem-zero or numerically bounded.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1836_SOURCE_REGISTER.csv",
    "projection_skeleton": RESIDUALS / "P8_Y5_PARENT_QLOC_1836_WEP_CLOCK_LIGHTCONE_PROJECTION_SKELETON.csv",
    "response_operator_requirements": RESIDUALS / "P8_Y5_PARENT_QLOC_1836_RESPONSE_OPERATOR_REQUIREMENTS.csv",
    "units_domain_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1836_UNITS_AND_DOMAIN_LEDGER.csv",
    "score_refusal_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1836_SCORE_REFUSAL_LEDGER.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1836_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1836_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1836_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing_needles = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and not missing_needles,
                "missing_needles": ";".join(missing_needles),
                "role": source["role"],
            }
        )
    return rows


def projection_skeleton_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "projection_id": "P1836_WEP_0_eta_total",
            "arena": "WEP_MICROSCOPE",
            "target_residual": "eta_AB",
            "input_components": "spin_hypermomentum;material_marker_connection_current;clock_rod_nonmetric_connection_current;projective_trace_current",
            "symbolic_projection": "eta_AB = P_WEP_eta_AB · DeltaGamma_WEP",
            "response_operator_needed": "P_WEP_eta_AB(species_A,species_B,source,test_body,readout)",
            "domain": "local weak-field composition-dependent differential acceleration",
            "units_status": "eta_AB dimensionless; DeltaGamma component units unresolved",
            "missing_inputs": "MISSING_COMPONENT_VALUES;MISSING_COMMON_DELTAGAMMA_UNITS;MISSING_WEP_PROJECTION_MATRIX;MISSING_SOURCE_MATERIAL_BASIS",
            "no_cancellation_policy": "each active component must be theorem-zero or individually bounded unless a parent identity proves cancellation",
            "claim_ceiling": "NO_WEP_PASS",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "P1836_WEP_1_spin_material_split",
            "arena": "WEP_MICROSCOPE",
            "target_residual": "eta_spin_material_AB",
            "input_components": "spin_hypermomentum;material_marker_connection_current",
            "symbolic_projection": "eta_spin_material_AB = P_WEP_spin · DeltaGamma_spin + P_WEP_mat · DeltaGamma_material",
            "response_operator_needed": "spin/material differential response tensor in the observed source frame",
            "domain": "composition and spin-readout sector of local weak-field matter",
            "units_status": "dimensionless eta contribution after projection; input normalization missing",
            "missing_inputs": "MISSING_SPIN_CURRENT_NORM;MISSING_MATERIAL_TENSOR;MISSING_PARENT_MATTER_FUNCTOR",
            "no_cancellation_policy": "spin and material terms cannot be cancelled by hand",
            "claim_ceiling": "NO_WEP_COMPONENT_SCORE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "P1836_CLOCK_0_redshift_total",
            "arena": "clock_redshift",
            "target_residual": "redshift_fractional_deviation;clock_residual",
            "input_components": "clock_rod_nonmetric_connection_current;spin_hypermomentum;material_marker_connection_current;projective_trace_current",
            "symbolic_projection": "delta_nu_over_nu = P_clock · DeltaGamma_clock",
            "response_operator_needed": "P_clock(clock_species,rod_calibration,worldline,coframe_lock)",
            "domain": "local clock comparison and gravitational redshift branch",
            "units_status": "fractional frequency shift dimensionless; nonmetricity units unresolved",
            "missing_inputs": "MISSING_CLOCK_FUNCTIONAL;MISSING_ROD_CALIBRATION;MISSING_Q_TRACE_NORMALIZATION;MISSING_CLOCK_BOUND_SOURCE",
            "no_cancellation_policy": "clock silence requires theorem-zero clock coupling or sourced bound row",
            "claim_ceiling": "NO_CLOCK_PASS",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "P1836_CLOCK_1_weyl_trace",
            "arena": "clock_redshift",
            "target_residual": "rod_residual;clock_nonmetricity",
            "input_components": "clock_rod_nonmetric_connection_current",
            "symbolic_projection": "clock_nonmetricity = P_Qtrace_clock · Q_trace",
            "response_operator_needed": "Weyl-trace nonmetricity response of rods and clocks",
            "domain": "clock/rod calibration under a single observed coframe",
            "units_status": "inverse length or normalized Q units missing",
            "missing_inputs": "MISSING_Q_TRACE_VALUE;MISSING_Q_TRACE_UNITS;MISSING_SINGLE_CLOCK_ROD_FRAME_THEOREM",
            "no_cancellation_policy": "rod and clock effects must be absent by derivation or scored separately",
            "claim_ceiling": "NO_CLOCK_ROD_SILENCE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "P1836_LIGHT_0_null_cone_total",
            "arena": "lightcone_photon",
            "target_residual": "lightcone_residual;gamma_minus_1",
            "input_components": "photon_lightcone_connection_current;clock_rod_nonmetric_connection_current;spin_hypermomentum",
            "symbolic_projection": "delta_null = P_lightcone · DeltaGamma_light",
            "response_operator_needed": "P_lightcone(photon_branch,gauge,null_vector,readout_clock)",
            "domain": "local photon propagation and weak-field lensing/lightcone branch",
            "units_status": "gamma_minus_1 dimensionless; null-cone residual normalization missing",
            "missing_inputs": "MISSING_LIGHTCONE_RESPONSE_OPERATOR;MISSING_PHOTON_BRANCH;MISSING_GAUGE_RULE;MISSING_TRACE_FREE_Q_NORMALIZATION",
            "no_cancellation_policy": "metric lightcone cannot be assumed if shear nonmetricity survives",
            "claim_ceiling": "NO_LIGHTCONE_OR_PPN_GAMMA_PASS",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "P1836_LIGHT_1_shear_nonmetricity",
            "arena": "lightcone_photon",
            "target_residual": "trace_free_lightcone_shear",
            "input_components": "photon_lightcone_connection_current",
            "symbolic_projection": "trace_free_lightcone_shear = P_Qshear_light · Q_shear",
            "response_operator_needed": "trace-free nonmetricity-to-null-cone response tensor",
            "domain": "metric compatibility / photon eikonal branch",
            "units_status": "inverse length or normalized shear-Q units missing",
            "missing_inputs": "MISSING_Q_SHEAR_VALUE;MISSING_LIGHTCONE_BOUND;MISSING_METRIC_LIGHTCONE_THEOREM",
            "no_cancellation_policy": "Q_shear must vanish, be bounded, or remain in the local residual vector",
            "claim_ceiling": "NO_METRIC_LIGHTCONE_CLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "P1836_PROJECTIVE_0_common_trace",
            "arena": "WEP_CLOCK_LIGHTCONE_COMMON",
            "target_residual": "projective_trace_visibility",
            "input_components": "projective_trace_current",
            "symbolic_projection": "r_projective = P_projective_all · DeltaGamma_projective",
            "response_operator_needed": "all-sector projective invariance certificate or trace gauge-fixing map",
            "domain": "shared source/readout/clock/photon trace branch",
            "units_status": "projective trace normalization missing",
            "missing_inputs": "MISSING_PROJECTIVE_INVARIANCE_ALL_SECTORS;MISSING_TRACE_GAUGE_RULE;MISSING_SOURCE_TRACE_BOUND",
            "no_cancellation_policy": "projective trace cannot be hidden in a gauge unless all sectors descend through that gauge",
            "claim_ceiling": "NO_PROJECTIVE_SILENCE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "P1836_GUARD_0_cross_arena",
            "arena": "WEP_CLOCK_LIGHTCONE_COMMON",
            "target_residual": "combined_local_residual_vector",
            "input_components": "spin_hypermomentum;material_marker_connection_current;clock_rod_nonmetric_connection_current;photon_lightcone_connection_current;projective_trace_current",
            "symbolic_projection": "R_local = (P_WEP, P_clock, P_lightcone) · DeltaGamma_WCL",
            "response_operator_needed": "block response matrix with common units and source/readout frame",
            "domain": "local GR/Newton recovery guard",
            "units_status": "common residual norm not defined",
            "missing_inputs": "MISSING_BLOCK_MATRIX;MISSING_COMMON_UNITS;MISSING_NO_CANCELLATION_IDENTITY",
            "no_cancellation_policy": "combined pass is forbidden until individual rows pass or a parent identity exists",
            "claim_ceiling": "NO_LOCAL_GR_PROMOTION",
            "valid_for_claim": False,
        },
    ]


def response_operator_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "ROR1836_0_common_vector",
            "operator": "DeltaGamma_WCL",
            "required_form": "(DeltaGamma_spin, DeltaGamma_material, DeltaGamma_clock, DeltaGamma_lightcone, DeltaGamma_projective) with one dual-connection normalization",
            "why_needed": "all WEP/clock/lightcone projections must act on the same component basis",
            "current_status": "MISSING_COMMON_DELTAGAMMA_UNITS",
            "blocks": "all 1836 scores",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "ROR1836_1_P_WEP",
            "operator": "P_WEP_eta_AB",
            "required_form": "linearized response from spin/material/clock/projective connection currents to differential acceleration eta_AB",
            "why_needed": "without P_WEP, composition tests cannot be compared to DeltaGamma components",
            "current_status": "MISSING_WEP_PROJECTION_MATRIX",
            "blocks": "WEP_MICROSCOPE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "ROR1836_2_P_clock",
            "operator": "P_clock",
            "required_form": "clock/rod/redshift functional mapping Q_trace, spin and material currents to fractional frequency residuals",
            "why_needed": "local GR recovery requires clock and rod standards to descend to the observed metric branch",
            "current_status": "MISSING_CLOCK_PROJECTION_FUNCTIONAL",
            "blocks": "clock_redshift",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "ROR1836_3_P_lightcone",
            "operator": "P_lightcone",
            "required_form": "photon eikonal/null-cone response to trace-free nonmetricity and spin/lightcone currents with gauge fixed",
            "why_needed": "PPN gamma and photon propagation cannot assume metric lightcones while Q_shear is live",
            "current_status": "MISSING_LIGHTCONE_RESPONSE_OPERATOR",
            "blocks": "lightcone_photon;PPN_gamma",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "ROR1836_4_projective",
            "operator": "P_projective_all",
            "required_form": "projective trace invariance or gauge-fixing certificate for matter, clocks, photons, sources and boundaries",
            "why_needed": "a projective mode can otherwise leak into source charge, WEP, clocks or lightcone readout",
            "current_status": "MISSING_PROJECTIVE_ALL_SECTOR_CERTIFICATE",
            "blocks": "all 1836 arenas",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "ROR1836_5_no_cancellation",
            "operator": "local_residual_guard",
            "required_form": "each component theorem-zero or individually below sourced bound, unless parent action supplies exact cancellation identity",
            "why_needed": "prevents tuned cancellation between WEP, clock and lightcone residuals",
            "current_status": "GUARD_ACTIVE",
            "blocks": "combined local GR promotion",
            "valid_for_claim": False,
        },
    ]


def units_domain_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "ledger_id": "UD1836_0_DeltaGamma_units",
            "quantity": "DeltaGamma components",
            "expected_units": "dual-connection source density or normalized connection-response units",
            "domain": "local weak-field parent action variation",
            "status": "MISSING_COMMON_UNITS",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "ledger_id": "UD1836_1_WEP_eta",
            "quantity": "eta_AB",
            "expected_units": "dimensionless differential acceleration ratio",
            "domain": "composition-dependent free-fall response",
            "status": "OUTPUT_UNITS_KNOWN_INPUT_PROJECTION_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "ledger_id": "UD1836_2_clock",
            "quantity": "delta_nu_over_nu",
            "expected_units": "dimensionless fractional frequency/redshift residual",
            "domain": "clock/rod readout under observed coframe",
            "status": "OUTPUT_UNITS_KNOWN_CLOCK_FUNCTIONAL_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "ledger_id": "UD1836_3_lightcone",
            "quantity": "lightcone_residual;gamma_minus_1",
            "expected_units": "dimensionless after eikonal/PPN normalization",
            "domain": "photon null cone and weak-field metric response",
            "status": "OUTPUT_UNITS_KNOWN_LIGHTCONE_OPERATOR_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "ledger_id": "UD1836_4_domain",
            "quantity": "local domain split",
            "expected_units": "not a cosmological average; all rows must be local weak-field readouts",
            "domain": "local GR/Newton recovery branch",
            "status": "DOMAIN_DECLARED_NOT_SCORED",
            "valid_for_claim": False,
        },
    ]


def score_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "refusal_id": "SR1836_0_WEP",
            "arena": "WEP_MICROSCOPE",
            "reason": "P_WEP_eta_AB, component values, common units and material/source basis are missing",
            "required_to_unblock": "derive P_WEP from parent matter functor or fill sourced component bound rows",
            "status": "SCORE_REFUSED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "refusal_id": "SR1836_1_CLOCK",
            "arena": "clock_redshift",
            "reason": "clock functional, rod calibration, Q_trace value/units and redshift bound path are missing",
            "required_to_unblock": "derive clock/rod metric descent or fill clock residual bound row",
            "status": "SCORE_REFUSED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "refusal_id": "SR1836_2_LIGHTCONE",
            "arena": "lightcone_photon",
            "reason": "photon branch, gauge rule, Q_shear value/units and lightcone response operator are missing",
            "required_to_unblock": "derive metric lightcone theorem or fill lightcone residual bound row",
            "status": "SCORE_REFUSED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "refusal_id": "SR1836_3_PROJECTIVE",
            "arena": "WEP_CLOCK_LIGHTCONE_COMMON",
            "reason": "projective trace silence is not proven for all sectors",
            "required_to_unblock": "all-sector projective invariance certificate or sourced projective leakage bound",
            "status": "SCORE_REFUSED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "refusal_id": "SR1836_4_LOCAL_GR",
            "arena": "local_GR_Newton_recovery",
            "reason": "combined residual vector is not allowed to pass by cancellation or unfilled response matrices",
            "required_to_unblock": "every retained component theorem-zero or scored below source-locked bound",
            "status": "LOCAL_GR_PROMOTION_FORBIDDEN",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1836_0_skeleton_result",
            "decision": "WEP_CLOCK_LIGHTCONE_PROJECTION_SKELETON_WRITTEN_NONCLAIM",
            "reason": "the first DeltaGamma projection block now declares targets, operators, domains, units and blockers without inserting coefficients",
            "next_action": "do not score WEP/clock/lightcone yet",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1836_1_core_gap",
            "decision": "RESPONSE_OPERATORS_NOT_DERIVED",
            "reason": "P_WEP, P_clock, P_lightcone and projective all-sector silence remain unsigned by the parent action",
            "next_action": "derive the first response operator rather than fit it",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1836_2_best_next",
            "decision": "P_WEP_FROM_MATTER_FUNCTOR_NEXT",
            "reason": "WEP is the harshest local-coupling test and uses the same missing matter-functor machinery that controls clocks and source charge",
            "next_action": "1837-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1836_0_primary",
            "next_target": "1837-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-row.md",
            "script": "scripts/Y5_R2FR_PWEP_response_operator_from_matter_functor_or_component_bound_row.py",
            "objective": "try to derive P_WEP from the parent matter functor; if it fails, stage sourced nonclaim component-bound rows for eta_AB",
            "selection_status": "selected",
            "success_condition": "P_WEP is either parent-derived with signed assumptions, or WEP remains blocked with explicit component-bound inputs",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1836_1_secondary",
            "next_target": "1837b-Y5-R2FR-clock-lightcone-response-operators-or-zero-theorems.md",
            "script": "scripts/Y5_R2FR_clock_lightcone_response_operators_or_zero_theorems.py",
            "objective": "derive clock and lightcone response operators after the WEP branch exposes the matter coupling form",
            "selection_status": "held_secondary",
            "success_condition": "clock/lightcone channels remain nonclaim unless response operators or zero theorems are parent-signed",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "projection_skeleton": projection_skeleton_rows(),
        "response_operator_requirements": response_operator_requirement_rows(),
        "units_domain_ledger": units_domain_rows(),
        "score_refusal_ledger": score_refusal_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_csvs(paths: list[Path]) -> None:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            directory.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, directory / path.name)


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open("r", encoding="utf-8", newline="") as handle:
                list(csv.DictReader(handle))
    except Exception:
        return False
    return True


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    guarded_keys = {"valid_for_claim", "claim_allowed"}
    for rows in rows_map.values():
        for row in rows:
            for guarded_key in guarded_keys.intersection(row):
                if str(row[guarded_key]).lower() == "true":
                    return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        name = path.name
        if "1836-Y5-R2FR" in name or name.startswith("P8_Y5_PARENT_QLOC_1836") or name.startswith("P8_Y5_BRR545_1836"):
            return False
    return True


def branch_copies_exist(paths: list[Path]) -> bool:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            if not (directory / path.name).exists():
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]], copied_paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    output_paths = [OUTPUTS[key] for key in rows_map.keys()]
    skeleton_rows = rows_map["projection_skeleton"]
    requirement_rows = rows_map["response_operator_requirements"]
    refusal_rows = rows_map["score_refusal_ledger"]
    checks: list[tuple[str, bool, str]] = [
        ("VAL1836_0_sources_exist", all(str(row["exists"]).lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL1836_1_needles_present", all(str(row["needles_present"]).lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL1836_2_projection_rows_present",
            {"WEP_MICROSCOPE", "clock_redshift", "lightcone_photon"}.issubset({row["arena"] for row in skeleton_rows}),
            "WEP, clock and lightcone projection skeleton rows are present",
        ),
        (
            "VAL1836_3_all_projection_rows_nonclaim",
            all(row["valid_for_claim"] is False for row in skeleton_rows),
            "all projection rows remain valid_for_claim=false",
        ),
        (
            "VAL1836_4_response_operators_declared",
            {"P_WEP_eta_AB", "P_clock", "P_lightcone"}.issubset({row["operator"] for row in requirement_rows}),
            "P_WEP, P_clock and P_lightcone requirements are declared",
        ),
        (
            "VAL1836_5_score_refusals_active",
            all(row["status"] in {"SCORE_REFUSED", "LOCAL_GR_PROMOTION_FORBIDDEN"} for row in refusal_rows),
            "WEP, clock, lightcone and local-GR scoring remain refused",
        ),
        (
            "VAL1836_6_next_selected",
            any(row["route_id"] == "NEXT1836_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selects P_WEP response operator from matter functor",
        ),
        ("VAL1836_7_no_claim_flags", no_claim_flags(rows_map), "no generated claim flags are true"),
        ("VAL1836_8_csv_parse", csv_parse_ok(output_paths), "all generated 1836 CSVs parse"),
        ("VAL1836_9_branch_copies", branch_copies_exist(copied_paths), "branch/quarantine/queue copies exist"),
        ("VAL1836_10_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1836_11_formalization_untouched", no_formalization_outputs(), "no 1836 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1836_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1836 DeltaGamma WEP/clock/lightcone projection skeleton checkpoint",
        }
    )
    return rows


def markdown_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1836 Y5 R2FR DeltaGamma WEP clock lightcone projection skeleton",
            "",
            "**Progress:** 1836 turns the 1835 component map into the first local projection block. It does not test or score MTS yet; it names the response operators that must convert `Delta_Gamma` spin/material/clock/lightcone/projective currents into WEP, clock and photon residuals.",
            "",
            "**Current verdict:** the coupling problem is now sharply localized. `P_WEP`, `P_clock`, `P_lightcone`, common `Delta_Gamma` units and projective all-sector silence are still missing, so WEP/clock/lightcone/local-GR claims remain blocked.",
            "",
            "**Claim ceiling:** no WEP pass, no clock pass, no lightcone pass, no PPN gamma pass, no local GR/Newton promotion, no numerical score, no GitHub action, and no `formalization-workbench` edit is allowed from 1836.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## WEP Clock Lightcone Projection Skeleton",
            markdown_table(rows_map["projection_skeleton"], ["projection_id", "arena", "target_residual", "input_components", "symbolic_projection", "response_operator_needed", "domain", "units_status", "missing_inputs", "claim_ceiling", "valid_for_claim"]),
            "",
            "## Response Operator Requirements",
            markdown_table(rows_map["response_operator_requirements"], ["requirement_id", "operator", "required_form", "why_needed", "current_status", "blocks", "valid_for_claim"]),
            "",
            "## Units And Domain Ledger",
            markdown_table(rows_map["units_domain_ledger"], ["ledger_id", "quantity", "expected_units", "domain", "status", "valid_for_claim"]),
            "",
            "## Score Refusal Ledger",
            markdown_table(rows_map["score_refusal_ledger"], ["refusal_id", "arena", "reason", "required_to_unblock", "status", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a useful narrowing, not a defeat. The local branch is no longer failing vaguely at \"the coupling\"; it is asking for a specific first response operator. The best next shot is to derive `P_WEP` from the parent matter functor, because if WEP coupling descends cleanly then clocks and lightcones may inherit the same geometry discipline. If it does not descend, the branch has to remain a closure/bound-input route.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    nonvalidation_paths: list[Path] = []
    for key, rows in rows_map.items():
        path = OUTPUTS[key]
        write_csv(path, rows)
        nonvalidation_paths.append(path)
    copy_csvs(nonvalidation_paths)
    validation_rows = build_validation(rows_map, nonvalidation_paths)
    write_csv(OUTPUTS["validation"], validation_rows)
    copy_csvs([OUTPUTS["validation"]])
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1836 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
