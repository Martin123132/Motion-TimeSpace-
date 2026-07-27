from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3544-Y5-R2FR-MTS-to-DD-source-map-or-MICROSCOPE-source-leg-intake.md"
CANONICAL_STATUS = OUT / "P8_Y5_MTS_to_DD_source_map_status.csv"

DELTA_Q_MHAT = 3.330000e-03
DELTA_Q_E = 2.040000e-03
ETA_BOUND_ROUNDED = 2.8e-15
ETA_BOUND_SOURCE_LEGACY = 2.745906e-15


SOURCES: dict[str, dict[str, Any]] = {
    "script_3544": {"path": Path(__file__).resolve(), "role": "3544 generator"},
    "doc_3543": {
        "path": ROOT / "3543-Y5-R2FR-constructor-exhaustion-or-first-species-source-coefficient-fill.md",
        "role": "constructor/species coefficient handoff",
    },
    "next_3543": {
        "path": OUT / "P8_Y5_R2FR_3543_NEXT_TARGET.csv",
        "role": "selected MTS-to-DD/source-leg target",
    },
    "first_fill_3543": {
        "path": OUT / "P8_Y5_R2FR_3543_FIRST_SPECIES_SOURCE_FILL.csv",
        "role": "first Ti/Pt species-source inequality",
    },
    "material_inputs_3543": {
        "path": OUT / "P8_Y5_R2FR_3543_TIPT_MATERIAL_INPUTS.csv",
        "role": "3543 Ti/Pt material input copy",
    },
    "material_basis_2440": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_MATERIAL_SENSITIVITY_BASIS.csv",
        "role": "source-backed Ti/Pt DD-like material contrast",
    },
    "k_projection_2440": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_K_VECTOR_PROJECTION.csv",
        "role": "prior MTS expanded WEP projection formula",
    },
    "source_leg_blockers_2440": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_SOURCE_LEG_BLOCKERS.csv",
        "role": "remaining source-leg/alloy/map blockers",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "MICROSCOPE Ti/Pt bound row",
    },
    "mu_extra_vector": {
        "path": OUT / "P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
        "role": "source-normalization residual channels",
    },
    "em_ellj_residual": {
        "path": OUT / "P8_EM_ellJ_source_current_owner_residual_law.csv",
        "role": "source-current denominator residual decomposition",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def dd_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "map_id": "MAP3544_0_DD_material_formula",
            "target": "eta_TiPt",
            "formula": "eta_TiPt ~= DeltaQ_mhat(Pt-Ti)*D_mhat_source + DeltaQ_e(Pt-Ti)*D_e_source",
            "known_inputs": f"DeltaQ_mhat={DELTA_Q_MHAT:.6e}; DeltaQ_e={DELTA_Q_E:.6e}",
            "missing_inputs": "D_mhat_source; D_e_source; source leg; sign/alloy policy",
            "status": "SOURCE_BACKED_MATERIAL_MAP_READY",
            "valid_for_claim": "False",
        },
        {
            "map_id": "MAP3544_1_MTS_mhat_block",
            "target": "D_mhat_source",
            "formula": "D_mhat_source := K_m_block*delta_w_block + K_m_shadow*delta_w_shadow + K_m_nonHilbert*c_nonHilbert",
            "known_inputs": "symbolic component structure from WKP2440_1",
            "missing_inputs": "K_m_block; K_m_shadow; K_m_nonHilbert; component values; units; source leg",
            "status": "SYMBOLIC_MTS_TO_DD_MAP_WRITTEN",
            "valid_for_claim": "False",
        },
        {
            "map_id": "MAP3544_2_MTS_electromagnetic_block",
            "target": "D_e_source",
            "formula": "D_e_source := K_e_alpha*b_alpha + K_e_frame*b_g",
            "known_inputs": "symbolic component structure from WKP2440_1",
            "missing_inputs": "K_e_alpha; K_e_frame; b_alpha; b_g; units; source leg",
            "status": "SYMBOLIC_MTS_TO_DD_MAP_WRITTEN",
            "valid_for_claim": "False",
        },
        {
            "map_id": "MAP3544_3_orphan_projector_tail",
            "target": "non-DD residual tail",
            "formula": "eta_tail = K_projector_WEP*c_projector + tail_abs_WEP",
            "known_inputs": "tail structure from WKP2440_1",
            "missing_inputs": "K_projector_WEP; c_projector; tail_abs_WEP; relation theorem showing whether these collapse into DD basis",
            "status": "RETAINED_OUTSIDE_TWO_CHARGE_DD_BASIS",
            "valid_for_claim": "False",
        },
        {
            "map_id": "MAP3544_4_absolute_no_cancellation",
            "target": "absolute envelope",
            "formula": "|DeltaQ_mhat*K_m_block*delta_w_block|+|DeltaQ_mhat*K_m_shadow*delta_w_shadow|+|DeltaQ_mhat*K_m_nonHilbert*c_nonHilbert|+|DeltaQ_e*K_e_alpha*b_alpha|+|DeltaQ_e*K_e_frame*b_g|+|K_projector_WEP*c_projector|+|tail_abs_WEP| <= eta_bound",
            "known_inputs": "DeltaQ_mhat; DeltaQ_e; eta_bound",
            "missing_inputs": "all component values and K values",
            "status": "ABSOLUTE_ENVELOPE_FORM_READY",
            "valid_for_claim": "False",
        },
    ]


def ceiling_rows() -> list[dict[str, Any]]:
    rounded_mhat = ETA_BOUND_ROUNDED / DELTA_Q_MHAT
    rounded_e = ETA_BOUND_ROUNDED / DELTA_Q_E
    legacy_mhat = ETA_BOUND_SOURCE_LEGACY / DELTA_Q_MHAT
    legacy_e = ETA_BOUND_SOURCE_LEGACY / DELTA_Q_E
    return [
        {
            "ceiling_id": "CEIL3544_0_D_mhat_only",
            "assumption": "D_e_source=0 and all tail/projector terms zero",
            "inequality": f"|D_mhat_source| <= {rounded_mhat:.6e}",
            "rounded_bound_value": f"{rounded_mhat:.12e}",
            "legacy_1sigma_value": f"{legacy_mhat:.12e}",
            "units": "dimensionless effective source-coupling coefficient",
            "score_ready": "True",
            "mts_prediction_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "ceiling_id": "CEIL3544_1_D_e_only",
            "assumption": "D_mhat_source=0 and all tail/projector terms zero",
            "inequality": f"|D_e_source| <= {rounded_e:.6e}",
            "rounded_bound_value": f"{rounded_e:.12e}",
            "legacy_1sigma_value": f"{legacy_e:.12e}",
            "units": "dimensionless effective source-coupling coefficient",
            "score_ready": "True",
            "mts_prediction_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "ceiling_id": "CEIL3544_2_epsilon_species_unit",
            "assumption": "unit projection eta_source_TiPt=|epsilon_species_Pt-epsilon_species_Ti|",
            "inequality": f"|epsilon_species_Pt_minus_Ti| <= {ETA_BOUND_ROUNDED:.6e}",
            "rounded_bound_value": f"{ETA_BOUND_ROUNDED:.12e}",
            "legacy_1sigma_value": f"{ETA_BOUND_SOURCE_LEGACY:.12e}",
            "units": "dimensionless",
            "score_ready": "True",
            "mts_prediction_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "ceiling_id": "CEIL3544_3_absolute_two_charge_envelope",
            "assumption": "no cancellation credit between D_mhat_source and D_e_source",
            "inequality": f"{DELTA_Q_MHAT:.6e}*|D_mhat_source| + {DELTA_Q_E:.6e}*|D_e_source| <= {ETA_BOUND_ROUNDED:.6e}",
            "rounded_bound_value": f"{ETA_BOUND_ROUNDED:.12e}",
            "legacy_1sigma_value": f"{ETA_BOUND_SOURCE_LEGACY:.12e}",
            "units": "dimensionless eta envelope",
            "score_ready": "True",
            "mts_prediction_ready": "False",
            "valid_for_claim": "False",
        },
    ]


def source_leg_rows() -> list[dict[str, Any]]:
    return [
        {
            "intake_id": "SL3544_0_compressed_D_definition",
            "needed_object": "compressed effective D_i_source",
            "definition": "D_i_source already includes the Earth/source leg and orbit normalization used by the MICROSCOPE Ti/Pt comparison.",
            "required_inputs": "declare whether D_i_source is compressed; units; sign convention; no-cancellation policy",
            "current_status": "USABLE_FOR_DD_LIKE_NONCLAIM_CONSTRAINT",
            "why_needed": "allows the inequality to be used as a bound on effective coefficients without proving Earth composition",
            "valid_for_claim": "False",
        },
        {
            "intake_id": "SL3544_1_factorized_Earth_source",
            "needed_object": "Earth/source charge leg",
            "definition": "D_i_source = alpha_i^test * alpha_source or equivalent factorized source-charge product.",
            "required_inputs": "Earth composition/source-body charge; orbit normalization; active-vs-inertial mass split; parent Hilbert source lock",
            "current_status": "MISSING",
            "why_needed": "required to turn effective D_i_source into a fundamental MTS source coupling",
            "valid_for_claim": "False",
        },
        {
            "intake_id": "SL3544_2_alloy_policy",
            "needed_object": "Ti/Pt material policy",
            "definition": "decide whether elemental Ti and Pt charges are enough or whether exact Ti alloy and Pt/Rh test-mass corrections are required.",
            "required_inputs": "MICROSCOPE material composition; isotope/alloy correction policy; uncertainty handling",
            "current_status": "MISSING_POLICY",
            "why_needed": "keeps the material contrast approximate rather than overclaimed",
            "valid_for_claim": "False",
        },
        {
            "intake_id": "SL3544_3_sign_convention",
            "needed_object": "Ti-minus-Pt vs Pt-minus-Ti convention",
            "definition": "fix the sign convention for eta_TiPt and material contrast rows.",
            "required_inputs": "declared ordering; absolute-envelope policy; source-bound row convention",
            "current_status": "ABSOLUTE_ONLY_SAFE",
            "why_needed": "signed scoring is impossible until convention is fixed",
            "valid_for_claim": "False",
        },
        {
            "intake_id": "SL3544_4_MTS_units",
            "needed_object": "MTS component units and normalization",
            "definition": "K_m/K_e coefficients map MTS residual variables into dimensionless DD-like couplings.",
            "required_inputs": "q unit; source normalization denominator; component relation theorem; parent units",
            "current_status": "MISSING",
            "why_needed": "required for MTS prediction-ready status",
            "valid_for_claim": "False",
        },
    ]


def component_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "CMP3544_0_delta_w_block",
            "dd_channel": "D_mhat_source",
            "projection_weight": f"{DELTA_Q_MHAT:.6e}",
            "component_formula": "DeltaQ_mhat*K_m_block*delta_w_block",
            "coefficient_needed": "K_m_block",
            "value_needed": "delta_w_block",
            "units": "dimensionless after parent source normalization",
            "current_status": "MISSING_K_AND_VALUE",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CMP3544_1_delta_w_shadow",
            "dd_channel": "D_mhat_source",
            "projection_weight": f"{DELTA_Q_MHAT:.6e}",
            "component_formula": "DeltaQ_mhat*K_m_shadow*delta_w_shadow",
            "coefficient_needed": "K_m_shadow",
            "value_needed": "delta_w_shadow",
            "units": "dimensionless after parent source normalization",
            "current_status": "MISSING_K_AND_VALUE",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CMP3544_2_nonHilbert_current",
            "dd_channel": "D_mhat_source",
            "projection_weight": f"{DELTA_Q_MHAT:.6e}",
            "component_formula": "DeltaQ_mhat*K_m_nonHilbert*c_nonHilbert",
            "coefficient_needed": "K_m_nonHilbert",
            "value_needed": "c_nonHilbert",
            "units": "dimensionless after parent source normalization",
            "current_status": "MISSING_K_AND_VALUE",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CMP3544_3_b_alpha",
            "dd_channel": "D_e_source",
            "projection_weight": f"{DELTA_Q_E:.6e}",
            "component_formula": "DeltaQ_e*K_e_alpha*b_alpha",
            "coefficient_needed": "K_e_alpha",
            "value_needed": "b_alpha",
            "units": "dimensionless after EM/source normalization",
            "current_status": "MISSING_K_AND_VALUE",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CMP3544_4_b_g",
            "dd_channel": "D_e_source",
            "projection_weight": f"{DELTA_Q_E:.6e}",
            "component_formula": "DeltaQ_e*K_e_frame*b_g",
            "coefficient_needed": "K_e_frame",
            "value_needed": "b_g",
            "units": "dimensionless after frame/source normalization",
            "current_status": "MISSING_K_AND_VALUE",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CMP3544_5_projector",
            "dd_channel": "outside_two_charge_basis",
            "projection_weight": "1",
            "component_formula": "K_projector_WEP*c_projector",
            "coefficient_needed": "K_projector_WEP",
            "value_needed": "c_projector",
            "units": "dimensionless eta contribution",
            "current_status": "MISSING_K_AND_VALUE_RETAIN_ABSOLUTE",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CMP3544_6_tail",
            "dd_channel": "outside_two_charge_basis",
            "projection_weight": "1",
            "component_formula": "tail_abs_WEP",
            "coefficient_needed": "none if directly bounded",
            "value_needed": "tail_abs_WEP",
            "units": "dimensionless eta contribution",
            "current_status": "MISSING_VALUE_RETAIN_ABSOLUTE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3544_0_symbolic_map_written",
            "decision": "MTS-to-DD map is now explicit symbolically.",
            "rationale": "D_mhat_source and D_e_source are written as MTS component combinations from the existing 2440 formula.",
            "effect": "The next missing objects are K values, component values, units and source leg, not the map shape.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3544_1_single_channel_ceilings",
            "decision": "Single-channel ceilings are now calculable.",
            "rationale": "MICROSCOPE Ti/Pt bound divided by material contrast gives direct ceilings for effective D_mhat and D_e.",
            "effect": "D_mhat_source must be below about 8.41e-13 if alone; D_e_source below about 1.37e-12 if alone.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3544_2_source_leg_not_fundamental",
            "decision": "Compressed D_i coefficients are usable as nonclaim effective constraints, not fundamental MTS couplings.",
            "rationale": "Earth/source leg and parent Hilbert source lock remain missing.",
            "effect": "No source-coupling pass, but the empirical branch is now score-shaped.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3544_3_next",
            "decision": "Fill one K/component value or acquire source-leg/alloy inputs next.",
            "rationale": "That is the shortest path from symbolic map to an actual MTS score row.",
            "effect": "3545 should target K_e_alpha/b_alpha or Earth/source leg intake.",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3544_0_map",
            "quantity": "MTS_to_DD_map",
            "value": "symbolic_map_ready_values_missing",
            "meaning": "D_mhat_source and D_e_source are expressed as MTS component combinations but not numeric",
            "claim_effect": "not prediction-ready",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3544_1_ceilings",
            "quantity": "single_channel_ceilings",
            "value": "D_mhat<=8.408e-13; D_e<=1.373e-12",
            "meaning": "rounded MICROSCOPE Ti/Pt source bound gives effective one-channel constraints",
            "claim_effect": "nonclaim empirical target",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3544_2_source_leg",
            "quantity": "MICROSCOPE_source_leg",
            "value": "compressed_nonclaim_or_factorized_missing",
            "meaning": "effective D_i can be bounded, but fundamental MTS coupling needs Earth/source leg",
            "claim_effect": "source-coupling pass blocked",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3544_3_next",
            "quantity": "next_best_target",
            "value": "first_K_value_or_source_leg_intake",
            "meaning": "fill one MTS component projection or acquire the source/alloy/sign inputs",
            "claim_effect": "next empirical bridge",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3545-Y5-R2FR-first-DD-K-value-or-MICROSCOPE-source-leg-acquisition.md",
            "next_script": "scripts/Y5_R2FR_3545_first_DD_K_value_or_MICROSCOPE_source_leg_acquisition.py",
            "objective": "Try to fill the first MTS-to-DD projection coefficient/value pair, preferably K_e_alpha*b_alpha or K_m_block*delta_w_block; if not, build the Earth/source-leg and alloy/sign acquisition rows needed for MICROSCOPE scoring.",
            "success_gate": "Either one component contribution in the absolute envelope has a sourced value with units, or the source-leg/alloy/sign blockers are converted into concrete acquisition tasks.",
            "why_next": "3544 made the map and ceilings explicit; scoring now needs a real K/value or source-leg input.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    maps: list[dict[str, Any]],
    ceilings: list[dict[str, Any]],
    source_legs: list[dict[str, Any]],
    components: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    map_ids = {row["map_id"] for row in maps}
    ceiling_ids = {row["ceiling_id"] for row in ceilings}
    checks.append({"check_id": "VAL3544_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3544_1_symbolic_map_present", "passed": bool_text({"MAP3544_1_MTS_mhat_block", "MAP3544_2_MTS_electromagnetic_block", "MAP3544_4_absolute_no_cancellation"} <= map_ids), "detail": "D_mhat, D_e and absolute-envelope maps present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3544_2_single_channel_ceilings_present", "passed": bool_text({"CEIL3544_0_D_mhat_only", "CEIL3544_1_D_e_only", "CEIL3544_3_absolute_two_charge_envelope"} <= ceiling_ids and all(float(row["rounded_bound_value"]) > 0 for row in ceilings if row["ceiling_id"] in {"CEIL3544_0_D_mhat_only", "CEIL3544_1_D_e_only"})), "detail": "single-channel and absolute-envelope ceilings present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3544_3_source_leg_intake_present", "passed": bool_text({"SL3544_0_compressed_D_definition", "SL3544_1_factorized_Earth_source", "SL3544_2_alloy_policy", "SL3544_3_sign_convention"} <= {row["intake_id"] for row in source_legs}), "detail": "compressed/factorized source leg, alloy and sign rows present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3544_4_component_template_covers_terms", "passed": bool_text({"CMP3544_0_delta_w_block", "CMP3544_1_delta_w_shadow", "CMP3544_2_nonHilbert_current", "CMP3544_3_b_alpha", "CMP3544_4_b_g", "CMP3544_5_projector", "CMP3544_6_tail"} <= {row["component_id"] for row in components}), "detail": "all MTS component terms covered", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3544_5_no_claims_promoted", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + maps + ceilings + source_legs + components + status) and all(row.get("claim_allowed", "False") == "False" for row in decisions + next_rows)), "detail": "no source-coupling/WEP/local-GR claim promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3544_6_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3545-Y5-R2FR-first-DD-K-value")), "detail": "3545 K-value/source-leg target selected", "valid_for_claim": "False"})
    parse_ok = True
    parsed: list[str] = []
    for name, path in outputs.items():
        if name in {"doc", "validation"}:
            continue
        try:
            read_csv_rows(path)
            parsed.append(name)
        except Exception:
            parse_ok = False
            parsed.append(f"{name}:PARSE_FAIL")
    checks.append({"check_id": "VAL3544_7_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3544_8_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3544_9_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3544_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    maps: list[dict[str, Any]],
    ceilings: list[dict[str, Any]],
    source_legs: list[dict[str, Any]],
    components: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3544 - MTS-to-DD Source Map Or MICROSCOPE Source-Leg Intake

## Summary
- **Map shape derived:** `D_mhat_source` and `D_e_source` are now explicit symbolic combinations of MTS source-coupling components.
- **Main formula:** `eta_TiPt ~= 3.330000e-03*D_mhat_source + 2.040000e-03*D_e_source`.
- **Single-channel ceilings:** `|D_mhat_source| <= {ETA_BOUND_ROUNDED / DELTA_Q_MHAT:.6e}` and `|D_e_source| <= {ETA_BOUND_ROUNDED / DELTA_Q_E:.6e}` if each acts alone.
- **No-cancellation envelope:** `{DELTA_Q_MHAT:.6e}*|D_mhat_source| + {DELTA_Q_E:.6e}*|D_e_source| <= {ETA_BOUND_ROUNDED:.6e}`.
- **No claim:** source leg, units, K values, component values, alloy policy and sign convention are still missing.

## MTS-to-DD Map
From the existing 2440 projection structure:

`D_mhat_source := K_m_block*delta_w_block + K_m_shadow*delta_w_shadow + K_m_nonHilbert*c_nonHilbert`

and

`D_e_source := K_e_alpha*b_alpha + K_e_frame*b_g`.

The retained non-DD tail is

`eta_tail = K_projector_WEP*c_projector + tail_abs_WEP`.

The scoreable nonclaim envelope is therefore

`|3.330000e-03*D_mhat_source| + |2.040000e-03*D_e_source| + |eta_tail| <= 2.8e-15`,

unless a parent theorem justifies signed cancellation.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## MTS-to-DD Map Rows
{markdown_table(maps, ["map_id", "target", "formula", "known_inputs", "missing_inputs", "status", "valid_for_claim"])}

## Single-Channel Ceilings
{markdown_table(ceilings, ["ceiling_id", "assumption", "inequality", "rounded_bound_value", "legacy_1sigma_value", "units", "score_ready", "mts_prediction_ready", "valid_for_claim"])}

## Source-Leg Intake
{markdown_table(source_legs, ["intake_id", "needed_object", "definition", "required_inputs", "current_status", "why_needed", "valid_for_claim"])}

## Component Template
{markdown_table(components, ["component_id", "dd_channel", "projection_weight", "component_formula", "coefficient_needed", "value_needed", "units", "current_status", "valid_for_claim"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    maps = dd_map_rows()
    ceilings = ceiling_rows()
    source_legs = source_leg_rows()
    components = component_template_rows()
    decisions = decision_rows()
    status = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3544_SOURCE_REGISTER.csv",
        "dd_map": OUT / "P8_Y5_R2FR_3544_MTS_TO_DD_SOURCE_MAP.csv",
        "ceilings": OUT / "P8_Y5_R2FR_3544_SINGLE_CHANNEL_CEILINGS.csv",
        "source_leg": OUT / "P8_Y5_R2FR_3544_MICROSCOPE_SOURCE_LEG_INTAKE.csv",
        "components": OUT / "P8_Y5_R2FR_3544_COMPONENT_INPUT_TEMPLATE.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3544_DECISION_LEDGER.csv",
        "status": OUT / "P8_Y5_R2FR_3544_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "next_target": OUT / "P8_Y5_R2FR_3544_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3544_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["dd_map"], maps, ["map_id", "target", "formula", "known_inputs", "missing_inputs", "status", "valid_for_claim"])
    write_csv(outputs["ceilings"], ceilings, ["ceiling_id", "assumption", "inequality", "rounded_bound_value", "legacy_1sigma_value", "units", "score_ready", "mts_prediction_ready", "valid_for_claim"])
    write_csv(outputs["source_leg"], source_legs, ["intake_id", "needed_object", "definition", "required_inputs", "current_status", "why_needed", "valid_for_claim"])
    write_csv(outputs["components"], components, ["component_id", "dd_channel", "projection_weight", "component_formula", "coefficient_needed", "value_needed", "units", "current_status", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, maps, ceilings, source_legs, components, decisions, status, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, maps, ceilings, source_legs, components, decisions, status, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
