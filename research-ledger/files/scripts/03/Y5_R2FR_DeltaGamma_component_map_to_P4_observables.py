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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1835"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
P4_RUN = ROOT / "runs" / "20260602-141500-metric-compatibility-Levi-Civita-or-R11-connection-row" / "results"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1835-Y5-R2FR-DeltaGamma-component-map-to-P4-observables.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1835_0_1834_next",
        "source_key": "1834_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1834_NEXT_TARGET.csv",
        "needles": ["NEXT1834_0_primary", "selected"],
        "role": "1834 selects DeltaGamma component map to P4 observables.",
    },
    {
        "source_id": "SRC1835_1_1834_validation",
        "source_key": "1834_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1834_VALIDATION.csv",
        "needles": ["VAL1834_OVERALL", "PASS"],
        "role": "confirms 1834 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1835_2_1834_components",
        "source_key": "1834_component_basis",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1834_DELTAGAMMA_COMPONENT_BASIS.csv",
        "needles": ["DGC1834_0_spin", "DGC1834_6_projective"],
        "role": "component basis to map into observables.",
    },
    {
        "source_id": "SRC1835_3_1834_bound",
        "source_key": "1834_DeltaGamma_bound",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1834_DELTAGAMMA_BOUND_ROW.csv",
        "needles": ["DGB1834_0_total", "MISSING_DELTAGAMMA_TO_P4_WEP_PPN_CLOCK_MAP"],
        "role": "prior bound row requiring observable map.",
    },
    {
        "source_id": "SRC1835_4_1833_hypermomentum",
        "source_key": "1833_hypermomentum_source",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_HYPERMOMENTUM_SOURCE_ROW.csv",
        "needles": ["HYP1833_0_Delta_Gamma_total", "SOURCE_ROW_STAGED_NONCLAIM"],
        "role": "hypermomentum source row staged before component split.",
    },
    {
        "source_id": "SRC1835_5_P4_template",
        "source_key": "P4_R11_template",
        "source_path": P4_RUN / "P4_R11_template_rows.csv",
        "needles": ["independent_connection_hypermomentum", "fill_WEP_source_clock_spin_map"],
        "role": "P4 connection template names observable channels.",
    },
    {
        "source_id": "SRC1835_6_P4_demotions",
        "source_key": "P4_demotions",
        "source_path": P4_RUN / "connection_operator_demotions.csv",
        "needles": ["independent_connection_hypermomentum", "fill hypermomentum/source-charge row"],
        "role": "connection demotion ledger keeps hypermomentum live.",
    },
    {
        "source_id": "SRC1835_7_R11_lock",
        "source_key": "1513_R11_vector_lock",
        "source_path": RESIDUALS / "P8_Y5_PARENT_MINIMALITY_1513_R11_VECTOR_LOCK.csv",
        "needles": ["torsion_nonmetricity", "eta_WEP;source_charge_residual;clock_residual;lightcone_residual"],
        "role": "existing R11 lock gives observable vocabulary for connection residuals.",
    },
    {
        "source_id": "SRC1835_8_source_norm",
        "source_key": "R11_source_norm_minimum",
        "source_path": RESIDUALS / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv",
        "needles": ["species_source_charge", "eta_source_AB;clock_redshift;operator_ledger"],
        "role": "source-normalization residual map for species/source current channels.",
    },
    {
        "source_id": "SRC1835_9_trace_schema",
        "source_key": "1434_projection_schema",
        "source_path": ROOT / "1434-Y5-R10-RAB-local-trace-residual-source-pack-schema-and-bound-map.md",
        "needles": ["REQ1434_1_projection_matrices", "MISSING_PROJECTION_MATRICES"],
        "role": "local residual schema policy: map projections before scoring.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_SOURCE_REGISTER.csv",
    "component_observable_map": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_DELTAGAMMA_COMPONENT_OBSERVABLE_MAP.csv",
    "arena_projection_requirements": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_ARENA_PROJECTION_REQUIREMENTS.csv",
    "score_blocker_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_SCORE_BLOCKER_LEDGER.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1835_VALIDATION.csv",
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


def component_observable_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "map_id": "DGOM1835_0_spin",
            "DeltaGamma_component": "spin_hypermomentum",
            "connection_channel": "axial_torsion_spin_coupling",
            "primary_observables": "spin_torsion_residual;clock_residual;lightcone_residual;eta_WEP;operator_ledger",
            "projection_required": "P_spin_to_axial_torsion;P_spin_to_clock;P_spin_to_lightcone;P_spin_to_WEP",
            "needed_inputs": "spin current norm;spin connection normalization;matter species basis;source path",
            "current_status": "MAP_SKELETON_ONLY_MISSING_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "DGOM1835_1_material",
            "DeltaGamma_component": "material_marker_connection_current",
            "connection_channel": "species_source_charge",
            "primary_observables": "eta_source_AB;eta_WEP;clock_redshift;operator_ledger",
            "projection_required": "P_material_to_composition;P_material_to_clock;P_material_to_source_charge",
            "needed_inputs": "material tensor;marker derivative;same-frame source basis;no hidden species theorem or bound",
            "current_status": "MAP_SKELETON_ONLY_MISSING_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "DGOM1835_2_source_support",
            "DeltaGamma_component": "source_support_connection_current",
            "connection_channel": "source_normalization_operator",
            "primary_observables": "source_charge_residual;alpha(lambda);gamma_minus_1;beta_minus_1;orbital_GM;operator_ledger",
            "projection_required": "P_source_support_to_GM;P_source_support_to_R10;P_source_support_to_PPN",
            "needed_inputs": "worldtube support;source current norm;radial profile;range scale;GM transfer convention",
            "current_status": "MAP_SKELETON_ONLY_MISSING_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "DGOM1835_3_clock_rods",
            "DeltaGamma_component": "clock_rod_nonmetric_connection_current",
            "connection_channel": "nonmetricity_weyl_trace",
            "primary_observables": "clock_residual;rod_residual;redshift_fractional_deviation;eta_WEP;operator_ledger",
            "projection_required": "P_nonmetricity_to_clock;P_nonmetricity_to_rods;P_clock_to_WEP",
            "needed_inputs": "clock functional;rod calibration functional;Q_trace normalization;redshift bound source",
            "current_status": "MAP_SKELETON_ONLY_MISSING_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "DGOM1835_4_photon_lightcone",
            "DeltaGamma_component": "photon_lightcone_connection_current",
            "connection_channel": "nonmetricity_shear_lightcone",
            "primary_observables": "lightcone_residual;gamma_minus_1;clock_residual;eta_WEP;operator_ledger",
            "projection_required": "P_shearQ_to_lightcone;P_lightcone_to_gamma;P_lightcone_to_clock",
            "needed_inputs": "lightcone response operator;trace-free Q normalization;gauge choice;photon/readout branch",
            "current_status": "MAP_SKELETON_ONLY_MISSING_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "DGOM1835_5_orbital_readout",
            "DeltaGamma_component": "orbital_readout_connection_current",
            "connection_channel": "source_readout_connection_current",
            "primary_observables": "orbital_GM;Gdot_over_G;alpha(lambda);beta_minus_1;gamma_minus_1;operator_ledger",
            "projection_required": "P_orbital_readout_to_GM;P_orbital_readout_to_Gdot;P_orbital_readout_to_fifth_force",
            "needed_inputs": "test-body readout action;inverse-square split;time/range law;no fitted GM absorption guard",
            "current_status": "MAP_SKELETON_ONLY_MISSING_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "DGOM1835_6_projective",
            "DeltaGamma_component": "projective_trace_current",
            "connection_channel": "torsion_trace_projective_mode",
            "primary_observables": "eta_WEP;source_charge_residual;clock_residual;projective_invariance_certificate;operator_ledger",
            "projection_required": "P_projective_to_source;P_projective_to_clock;P_projective_invariance_all_sectors",
            "needed_inputs": "projective gauge rule;all-sector invariance proof;source/readout trace coupling bound",
            "current_status": "MAP_SKELETON_ONLY_MISSING_PROJECTION",
            "valid_for_claim": False,
        },
    ]


def arena_projection_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "arena_id": "ARENA1835_0_R10",
            "arena": "R10_short_range_inverse_square",
            "observable": "alpha(lambda)",
            "DeltaGamma_components": "source_support_connection_current;orbital_readout_connection_current",
            "required_projection": "P_DeltaGamma_to_alpha_lambda with source geometry and lambda scale",
            "current_status": "MISSING_R10_PROJECTION_AND_FULL_BOUND_CURVE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "arena_id": "ARENA1835_1_WEP",
            "arena": "WEP_MICROSCOPE",
            "observable": "eta_AB",
            "DeltaGamma_components": "spin_hypermomentum;material_marker_connection_current;clock_rod_nonmetric_connection_current;projective_trace_current",
            "required_projection": "P_DeltaGamma_to_eta_AB with material tensor and no measured-G absorption",
            "current_status": "MISSING_WEP_PROJECTION_MATRIX",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "arena_id": "ARENA1835_2_PPN",
            "arena": "PPN",
            "observable": "gamma_minus_1;beta_minus_1;alpha1;alpha2;alpha3;xi",
            "DeltaGamma_components": "source_support_connection_current;photon_lightcone_connection_current;orbital_readout_connection_current",
            "required_projection": "P_DeltaGamma_to_metric_PPN with gauge, trace-reversal and source-normalization split",
            "current_status": "MISSING_PPN_RESPONSE_OPERATOR",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "arena_id": "ARENA1835_3_CLOCK",
            "arena": "clock_redshift",
            "observable": "redshift_fractional_deviation;clock_residual",
            "DeltaGamma_components": "clock_rod_nonmetric_connection_current;spin_hypermomentum;material_marker_connection_current;projective_trace_current",
            "required_projection": "P_DeltaGamma_to_clock_functional with clock species and coframe lock",
            "current_status": "MISSING_CLOCK_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "arena_id": "ARENA1835_4_LIGHTCONE",
            "arena": "lightcone_photon",
            "observable": "lightcone_residual;gamma_minus_1",
            "DeltaGamma_components": "photon_lightcone_connection_current;clock_rod_nonmetric_connection_current;spin_hypermomentum",
            "required_projection": "P_DeltaGamma_to_null_cone with photon/readout branch and gauge control",
            "current_status": "MISSING_LIGHTCONE_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "arena_id": "ARENA1835_5_ORBITAL",
            "arena": "orbital_Newton_source_normalization",
            "observable": "orbital_GM;Gdot_over_G;anomalous_radial_acceleration",
            "DeltaGamma_components": "orbital_readout_connection_current;source_support_connection_current;projective_trace_current",
            "required_projection": "P_DeltaGamma_to_orbital_readout with inverse-square split and no fitted-G shortcut",
            "current_status": "MISSING_ORBITAL_SOURCE_PROJECTION",
            "valid_for_claim": False,
        },
    ]


def score_blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "SBL1835_0_component_values",
            "blocks": "all arenas",
            "missing": "component numeric values or parent zero certificates",
            "status": "BLOCKS_SCORE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "SBL1835_1_common_units",
            "blocks": "DeltaGamma total norm",
            "missing": "common dual-connection units and normalization across components",
            "status": "BLOCKS_SCORE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "SBL1835_2_projection_matrices",
            "blocks": "observable maps",
            "missing": "P_R10, P_WEP, P_PPN, P_clock, P_lightcone, P_orbital",
            "status": "BLOCKS_SCORE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "SBL1835_3_no_cancellation",
            "blocks": "combined residual pass",
            "missing": "individual component pass or parent cancellation identity",
            "status": "GUARD_ACTIVE",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1835_0_map_result",
            "decision": "DELTAGAMMA_OBSERVABLE_MAP_SKELETON_WRITTEN_NONCLAIM",
            "reason": "each retained DeltaGamma component now has observable channels and required projection operators, but no projections or values are sourced",
            "next_action": "do not score any arena yet",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1835_1_primary_gap",
            "decision": "PROJECTION_MATRICES_MISSING",
            "reason": "component-to-observable rows cannot become predictions without P_R10/P_WEP/P_PPN/P_clock/P_lightcone/P_orbital",
            "next_action": "build first projection skeleton for the highest pressure channel",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1835_2_best_next",
            "decision": "FIRST_DELTAGAMMA_PROJECTION_MATRIX_NEXT",
            "reason": "the WEP/clock/lightcone channels are most directly connected to hypermomentum and can expose whether this branch is locally dangerous",
            "next_action": "1836-Y5-R2FR-DeltaGamma-WEP-clock-lightcone-projection-skeleton.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1835_0_primary",
            "next_target": "1836-Y5-R2FR-DeltaGamma-WEP-clock-lightcone-projection-skeleton.md",
            "script": "scripts/Y5_R2FR_DeltaGamma_WEP_clock_lightcone_projection_skeleton.py",
            "objective": "build the first nonclaim projection skeleton from DeltaGamma spin/material/clock/lightcone components into WEP, clock and lightcone residuals",
            "selection_status": "selected",
            "success_condition": "projection skeleton declares domains, units, response operators and blockers without inserting coefficients",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1835_1_secondary",
            "next_target": "1836b-Y5-R2FR-DeltaGamma-R10-PPN-orbital-projection-skeleton.md",
            "script": "scripts/Y5_R2FR_DeltaGamma_R10_PPN_orbital_projection_skeleton.py",
            "objective": "parallel source/orbital/PPN projection skeleton after WEP-clock-lightcone is staged",
            "selection_status": "held_secondary",
            "success_condition": "R10/PPN/orbital projection skeleton remains nonclaim with no fitted-G shortcut",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "component_observable_map": component_observable_map_rows(),
        "arena_projection_requirements": arena_projection_requirement_rows(),
        "score_blocker_ledger": score_blocker_rows(),
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
        if "1835-Y5-R2FR" in name or name.startswith("P8_Y5_PARENT_QLOC_1835") or name.startswith("P8_Y5_BRR545_1835"):
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
    checks: list[tuple[str, bool, str]] = [
        ("VAL1835_0_sources_exist", all(str(row["exists"]).lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL1835_1_needles_present", all(str(row["needles_present"]).lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL1835_2_component_map_complete",
            len(rows_map["component_observable_map"]) == 7 and all(row["valid_for_claim"] is False for row in rows_map["component_observable_map"]),
            "all seven DeltaGamma components have nonclaim observable map rows",
        ),
        (
            "VAL1835_3_arena_requirements_complete",
            len(rows_map["arena_projection_requirements"]) == 6 and all(row["valid_for_claim"] is False for row in rows_map["arena_projection_requirements"]),
            "six arena projection requirement rows are written and nonclaim",
        ),
        (
            "VAL1835_4_score_blockers_active",
            all(row["valid_for_claim"] is False for row in rows_map["score_blocker_ledger"]) and any(row["status"] == "BLOCKS_SCORE" for row in rows_map["score_blocker_ledger"]),
            "score blockers are active",
        ),
        (
            "VAL1835_5_decision_next",
            any(row["decision_id"] == "DEC1835_2_best_next" and row["decision"] == "FIRST_DELTAGAMMA_PROJECTION_MATRIX_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects first DeltaGamma projection matrix next",
        ),
        (
            "VAL1835_6_next_selected",
            any(row["route_id"] == "NEXT1835_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1835_7_no_claim_flags", no_claim_flags(rows_map), "no generated claim flags are true"),
        ("VAL1835_8_csv_parse", csv_parse_ok(output_paths), "all generated 1835 CSVs parse"),
        ("VAL1835_9_branch_copies", branch_copies_exist(copied_paths), "branch/quarantine/queue copies exist"),
        ("VAL1835_10_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1835_11_formalization_untouched", no_formalization_outputs(), "no 1835 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1835_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1835 DeltaGamma component map to P4 observables checkpoint",
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
            "# 1835 Y5 R2FR DeltaGamma component map to P4 observables",
            "",
            "**Progress:** 1835 maps the retained `Delta_Gamma` source-current components into concrete observable channels. This does not score the theory; it turns the coupling problem into a projection-matrix problem with named WEP, PPN, clock, lightcone, R10 and orbital rows.",
            "",
            "**Current verdict:** observable map skeleton complete, but no arena is score-ready. Component values, common units, and projection matrices are still missing, so every row remains `valid_for_claim=false`.",
            "",
            "**Claim ceiling:** no `Delta_Gamma` bound pass, no P4 pass, no WEP/PPN/clock/R10/orbital pass, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1835.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## DeltaGamma Component Observable Map",
            markdown_table(rows_map["component_observable_map"], ["map_id", "DeltaGamma_component", "connection_channel", "primary_observables", "projection_required", "needed_inputs", "current_status", "valid_for_claim"]),
            "",
            "## Arena Projection Requirements",
            markdown_table(rows_map["arena_projection_requirements"], ["arena_id", "arena", "observable", "DeltaGamma_components", "required_projection", "current_status", "valid_for_claim"]),
            "",
            "## Score Blocker Ledger",
            markdown_table(rows_map["score_blocker_ledger"], ["blocker_id", "blocks", "missing", "status", "valid_for_claim"]),
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
            "This is now much more testable. `Delta_Gamma` is no longer just a symbol for danger; it is a seven-component vector with arena projections. The next useful step is to build the first actual projection skeleton for WEP/clock/lightcone, because those channels are closest to spin, nonmetricity and matter-frame leakage.",
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
    print(f"1835 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
