from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3543-Y5-R2FR-constructor-exhaustion-or-first-species-source-coefficient-fill.md"
CANONICAL_STATUS = OUT / "P8_Y5_constructor_or_species_source_fill_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3543": {"path": Path(__file__).resolve(), "role": "3543 generator"},
    "doc_3542": {
        "path": ROOT / "3542-Y5-R2FR-no-source-only-slot-and-Hilbert-monopole-lock-or-coefficient-intake.md",
        "role": "no-source-slot/Hilbert-monopole handoff",
    },
    "next_3542": {
        "path": OUT / "P8_Y5_R2FR_3542_NEXT_TARGET.csv",
        "role": "selected constructor/species coefficient target",
    },
    "intake_3542": {
        "path": OUT / "P8_Y5_R2FR_3542_COEFFICIENT_INTAKE_ROWS.csv",
        "role": "3542 coefficient intake rows",
    },
    "no_source_3542": {
        "path": OUT / "P8_Y5_R2FR_3542_NO_SOURCE_ONLY_SLOT_PROOF_ATTEMPT.csv",
        "role": "3542 no-source-only proof attempt",
    },
    "material_basis_2440": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_MATERIAL_SENSITIVITY_BASIS.csv",
        "role": "Ti/Pt Damour-style material charge basis",
    },
    "k_projection_2440": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_K_VECTOR_PROJECTION.csv",
        "role": "Ti/Pt WEP projection formulas",
    },
    "source_leg_blockers_2440": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_SOURCE_LEG_BLOCKERS.csv",
        "role": "remaining blockers for MTS-to-WEP source leg",
    },
    "source_charge_rows_2396": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2396_SOURCE_CHARGE_ROWS.csv",
        "role": "matter/source residual charge rows",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "MICROSCOPE Ti/Pt source-charge bound",
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


def constructor_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CE3543_0_parent_generate_domain",
            "gate": "ParentGenerate coefficient domain",
            "statement": "Coeff_active_source may be generated only from q(Phi), theta_rep, and universal constants.",
            "pass_effect": "species/source coefficients w_A cannot be formed",
            "current_status": "NOT_DERIVED",
            "fallback": "use first species-source coefficient inequality",
            "claim_allowed": "False",
        },
        {
            "gate_id": "CE3543_1_noHom_species",
            "gate": "no-Hom from SpeciesLabel to active-source coefficient",
            "statement": "Hom_parent(SpeciesLabel,Coeff_active_source)=empty.",
            "pass_effect": "source-only Ti/Pt relative weights are untypeable",
            "current_status": "EXACT_CONDITIONAL_UNSIGNED",
            "fallback": "bound epsilon_species_Ti-epsilon_species_Pt",
            "claim_allowed": "False",
        },
        {
            "gate_id": "CE3543_2_noHiddenMarker",
            "gate": "no-Hom from hidden marker to active-source coefficient",
            "statement": "Hom_parent(HiddenMarker,Coeff_active_source)=empty.",
            "pass_effect": "marker/readout source charge cannot re-enter after variation",
            "current_status": "EXACT_CONDITIONAL_UNSIGNED",
            "fallback": "include hidden marker in absolute WEP envelope",
            "claim_allowed": "False",
        },
        {
            "gate_id": "CE3543_3_action_scale_owner",
            "gate": "single action-density line",
            "statement": "One parent action scale/measure/Jacobian covers ordinary matter before Hilbert variation.",
            "pass_effect": "relative source weights cannot hide as action-normalization choices",
            "current_status": "UNSIGNED",
            "fallback": "retain delta_w_species row",
            "claim_allowed": "False",
        },
        {
            "gate_id": "CE3543_4_countermodel",
            "gate": "surviving weighted-action countermodel",
            "statement": "S_matter=sum_A w_A S_A remains legal unless CE3543_0 through CE3543_3 pass.",
            "pass_effect": "none; this is the obstruction",
            "current_status": "COUNTERMODEL_RETAINED",
            "fallback": "score species/source coefficient",
            "claim_allowed": "False",
        },
    ]


def material_rows() -> list[dict[str, Any]]:
    return [
        {
            "material_id": "MAT3543_0_Ti",
            "material": "Ti",
            "A": "47.9",
            "Z": "22",
            "minus_Q_mhat": "10.28e-3",
            "Q_mhat": "-10.28e-3",
            "Q_e": "2.04e-3",
            "source": "Damour_ONERA_table via P8_Y5_PARENT_QLOC_2440_WEP_MATERIAL_SENSITIVITY_BASIS.csv",
            "status": "SOURCE_BACKED_APPROXIMATE_ISOTOPICALLY_AVERAGED",
            "valid_for_claim": "False",
        },
        {
            "material_id": "MAT3543_1_Pt",
            "material": "Pt",
            "A": "195.1",
            "Z": "78",
            "minus_Q_mhat": "6.95e-3",
            "Q_mhat": "-6.95e-3",
            "Q_e": "4.09e-3",
            "source": "Damour_ONERA_table via P8_Y5_PARENT_QLOC_2440_WEP_MATERIAL_SENSITIVITY_BASIS.csv",
            "status": "SOURCE_BACKED_APPROXIMATE_ISOTOPICALLY_AVERAGED",
            "valid_for_claim": "False",
        },
        {
            "material_id": "MAT3543_2_Pt_minus_Ti",
            "material": "Pt_minus_Ti",
            "A": "n/a",
            "Z": "n/a",
            "minus_Q_mhat": "-3.33e-3",
            "Q_mhat": "3.330000e-03",
            "Q_e": "2.040000e-03",
            "source": "Damour_ONERA_vector_PtTi via P8_Y5_PARENT_QLOC_2440_WEP_MATERIAL_SENSITIVITY_BASIS.csv",
            "status": "MATERIAL_CONTRAST_READY_SOURCE_LEG_MISSING",
            "valid_for_claim": "False",
        },
        {
            "material_id": "MAT3543_3_MICROSCOPE_bound",
            "material": "TiPt_pair",
            "A": "alloys",
            "Z": "alloys",
            "minus_Q_mhat": "n/a",
            "Q_mhat": "n/a",
            "Q_e": "n/a",
            "source": "local_bound_claims.csv:MICROSCOPE_final_TiPt_source_charge_proxy",
            "status": "EMPIRICAL_BOUND_READY_NOT_A_COMPONENT_BOUND",
            "valid_for_claim": "False",
        },
    ]


def first_species_fill_rows() -> list[dict[str, Any]]:
    return [
        {
            "fill_id": "SSF3543_0_DD_two_charge_constraint",
            "coefficient_target": "D_mhat_source,D_e_source",
            "projection_formula": "eta_TiPt ~= 3.330000e-03*D_mhat_source + 2.040000e-03*D_e_source",
            "bound_inequality": "|3.330000e-03*D_mhat_source + 2.040000e-03*D_e_source| <= 2.8e-15",
            "known_inputs": "DeltaQ_mhat=3.330000e-03; DeltaQ_e=2.040000e-03; eta_bound=2.8e-15",
            "missing_inputs": "MTS_to_DD_charge_map; Earth/source leg; alloy policy; sign convention for non-absolute scoring",
            "score_ready": "True",
            "mts_prediction_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "fill_id": "SSF3543_1_absolute_envelope",
            "coefficient_target": "MTS source-shadow/projector components",
            "projection_formula": "|DeltaQ_mhat*K_m_block*delta_w_block|+|DeltaQ_mhat*K_m_shadow*delta_w_shadow|+|DeltaQ_e*K_e_alpha*b_alpha|+|DeltaQ_e*K_e_frame*b_g|+|K_projector_WEP*c_projector|+|tail_abs_WEP|",
            "bound_inequality": "absolute_envelope <= 2.8e-15",
            "known_inputs": "DeltaQ_mhat; DeltaQ_e; MICROSCOPE eta bound",
            "missing_inputs": "all K_m/K_e/K_projector values; component relation theorem; q unit; Earth/source leg",
            "score_ready": "False",
            "mts_prediction_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "fill_id": "SSF3543_2_single_difference_ceiling",
            "coefficient_target": "epsilon_species_Pt_minus_Ti",
            "projection_formula": "eta_source_TiPt = |epsilon_species_Pt - epsilon_species_Ti| after common-mode removal",
            "bound_inequality": "|epsilon_species_Pt_minus_Ti| <= 2.8e-15 under unit projection",
            "known_inputs": "MICROSCOPE Ti/Pt source-charge proxy row",
            "missing_inputs": "proof unit projection applies to MTS epsilon_species_A; material/source split",
            "score_ready": "True",
            "mts_prediction_ready": "False",
            "valid_for_claim": "False",
        },
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK3543_0_MTS_to_DD_map",
            "blocker": "MTS residual to Damour-Donoghue charge map",
            "requirement": "derive D_mhat_source and D_e_source from delta_w_block, delta_w_shadow, b_alpha, b_g, c_projector with parent units",
            "current_status": "MISSING",
            "consequence": "DD inequality is a source-backed constraint, not an MTS prediction",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK3543_1_source_leg",
            "blocker": "Earth/source coupling leg",
            "requirement": "identify source body charge/normalization for MICROSCOPE orbit without importing measured g as proof",
            "current_status": "MISSING",
            "consequence": "alpha/source factor cannot be scored for MTS",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK3543_2_alloy_policy",
            "blocker": "exact material policy",
            "requirement": "decide whether elemental Ti/Pt charges are enough or require Ti alloy and Pt/Rh corrections",
            "current_status": "MISSING_POLICY",
            "consequence": "only approximate absolute smoke inequality is safe",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK3543_3_no_cancellation",
            "blocker": "component no-cancellation",
            "requirement": "do not use two-charge cancellation to hide MTS source-shadow/projector tails",
            "current_status": "POLICY_SET",
            "consequence": "absolute envelope row retained",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3543_0_constructor_not_closed",
            "decision": "Constructor exhaustion/no-Hom remains the clean derivation target but is not closed.",
            "rationale": "The weighted-action countermodel survives without parent grammar.",
            "effect": "Use species/source coefficient branch, not a source-coupling claim.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3543_1_first_real_inequality",
            "decision": "First species/source coefficient inequality is now source-backed.",
            "rationale": "Ti/Pt material contrast plus MICROSCOPE bound gives a concrete DD two-charge constraint.",
            "effect": "The fallback branch has a real numerical target: |3.33e-3 D_mhat + 2.04e-3 D_e| <= 2.8e-15.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3543_2_not_MTS_prediction",
            "decision": "Do not treat the inequality as an MTS prediction yet.",
            "rationale": "MTS-to-DD map, Earth/source leg, alloy policy and K values are still missing.",
            "effect": "The row is score-ready for DD-like coefficients but MTS-prediction-ready is false.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3543_3_next",
            "decision": "Attack MTS-to-DD source map or source leg next.",
            "rationale": "That is the shortest path from nonclaim inequality to a real source-coupling test.",
            "effect": "3544 should either derive D_mhat/D_e from MTS coefficients or build the source-leg intake.",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3543_0_constructor",
            "quantity": "constructor_exhaustion",
            "value": "not_derived_countermodel_retained",
            "meaning": "source-only species coefficients are not yet structurally impossible",
            "claim_effect": "Y5 source coupling not theorem-zero",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3543_1_species_bound",
            "quantity": "first_species_source_inequality",
            "value": "|3.33e-3 D_mhat + 2.04e-3 D_e| <= 2.8e-15",
            "meaning": "Ti/Pt material contrast and MICROSCOPE source bound are wired into a concrete nonclaim constraint",
            "claim_effect": "fallback branch becomes numerically targetable",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3543_2_prediction",
            "quantity": "MTS_species_prediction",
            "value": "not_ready",
            "meaning": "MTS-to-DD map and source leg are missing",
            "claim_effect": "no WEP/source coupling pass",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3543_3_next",
            "quantity": "next_best_target",
            "value": "MTS_to_DD_source_map_or_source_leg",
            "meaning": "turn the DD inequality into an MTS coefficient score, or prove the source slot impossible",
            "claim_effect": "direct empirical source-coupling route",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3544-Y5-R2FR-MTS-to-DD-source-map-or-MICROSCOPE-source-leg-intake.md",
            "next_script": "scripts/Y5_R2FR_3544_MTS_to_DD_source_map_or_MICROSCOPE_source_leg_intake.py",
            "objective": "Derive the map from MTS source-coupling coefficients into the Damour-Donoghue D_mhat/D_e basis, or build the MICROSCOPE Earth/source-leg intake needed to score the first species/source row.",
            "success_gate": "Either D_mhat_source and D_e_source are expressed in MTS coefficients with units, or the missing source-leg/alloy/sign inputs are converted into explicit acquisition rows.",
            "why_next": "3543 produced a real Ti/Pt inequality; the missing step is the MTS-to-material/source map.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    constructors: list[dict[str, Any]],
    materials: list[dict[str, Any]],
    fills: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    fill_ids = {row["fill_id"] for row in fills}
    checks.append({"check_id": "VAL3543_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3543_1_constructor_countermodel_kept", "passed": bool_text(any(row["gate_id"] == "CE3543_4_countermodel" and row["current_status"] == "COUNTERMODEL_RETAINED" for row in constructors)), "detail": "constructor countermodel retained", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3543_2_material_contrast_ready", "passed": bool_text(any(row["material_id"] == "MAT3543_2_Pt_minus_Ti" and "3.330000e-03" in row["Q_mhat"] and "2.040000e-03" in row["Q_e"] for row in materials)), "detail": "Pt-Ti material contrast present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3543_3_DD_inequality_written", "passed": bool_text("SSF3543_0_DD_two_charge_constraint" in fill_ids and any("2.8e-15" in row["bound_inequality"] and "3.330000e-03" in row["bound_inequality"] for row in fills)), "detail": "DD two-charge inequality written", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3543_4_MTS_prediction_blockers_present", "passed": bool_text({"BLK3543_0_MTS_to_DD_map", "BLK3543_1_source_leg", "BLK3543_2_alloy_policy"} <= {row["blocker_id"] for row in blockers}), "detail": "MTS map, source leg and alloy blockers present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3543_5_no_claims_promoted", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + materials + fills + blockers + status) and all(row.get("claim_allowed", "False") == "False" for row in constructors + decisions + next_rows)), "detail": "no WEP/source/local-GR claim promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3543_6_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3544-Y5-R2FR-MTS-to-DD")), "detail": "3544 MTS-to-DD/source-leg target selected", "valid_for_claim": "False"})
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
    checks.append({"check_id": "VAL3543_7_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3543_8_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3543_9_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3543_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    constructors: list[dict[str, Any]],
    materials: list[dict[str, Any]],
    fills: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3543 - Constructor Exhaustion Or First Species Source Coefficient Fill

## Summary
- **Constructor route:** no-Hom/constructor exhaustion remains the clean derivation path, but the weighted-action countermodel still survives.
- **First real bound row:** Ti/Pt material contrast and MICROSCOPE source-charge bound now give a concrete two-charge inequality.
- **Inequality:** `|3.330000e-03*D_mhat_source + 2.040000e-03*D_e_source| <= 2.8e-15`.
- **No claim:** this is not yet an MTS prediction because the MTS-to-DD map, Earth/source leg, alloy policy, and component K values are missing.
- **Next hinge:** derive `D_mhat_source,D_e_source` from MTS coefficients, or build the source-leg/alloy intake.

## Source-Backed Constraint
Using the existing Ti/Pt material contrast row,

`DeltaQ_mhat(Pt-Ti)=3.330000e-03`,

`DeltaQ_e(Pt-Ti)=2.040000e-03`,

and the MICROSCOPE source-charge proxy bound,

`eta_source_TiPt <= 2.8e-15`,

the simplified two-charge source-coupling row becomes

`|3.330000e-03*D_mhat_source + 2.040000e-03*D_e_source| <= 2.8e-15`.

That is a real numerical target for the source-coupling branch. The MTS-specific prediction still needs the map from MTS coefficients into `D_mhat_source,D_e_source`.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Constructor Exhaustion Gate
{markdown_table(constructors, ["gate_id", "gate", "statement", "pass_effect", "current_status", "fallback", "claim_allowed"])}

## Material Inputs
{markdown_table(materials, ["material_id", "material", "A", "Z", "minus_Q_mhat", "Q_mhat", "Q_e", "source", "status", "valid_for_claim"])}

## First Species Fill
{markdown_table(fills, ["fill_id", "coefficient_target", "projection_formula", "bound_inequality", "known_inputs", "missing_inputs", "score_ready", "mts_prediction_ready", "valid_for_claim"])}

## Blockers
{markdown_table(blockers, ["blocker_id", "blocker", "requirement", "current_status", "consequence", "valid_for_claim"])}

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
    constructors = constructor_rows()
    materials = material_rows()
    fills = first_species_fill_rows()
    blockers = blocker_rows()
    decisions = decision_rows()
    status = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3543_SOURCE_REGISTER.csv",
        "constructor_gate": OUT / "P8_Y5_R2FR_3543_CONSTRUCTOR_EXHAUSTION_GATE.csv",
        "material_inputs": OUT / "P8_Y5_R2FR_3543_TIPT_MATERIAL_INPUTS.csv",
        "first_species_fill": OUT / "P8_Y5_R2FR_3543_FIRST_SPECIES_SOURCE_FILL.csv",
        "blockers": OUT / "P8_Y5_R2FR_3543_MTS_TO_DD_BLOCKERS.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3543_DECISION_LEDGER.csv",
        "status": OUT / "P8_Y5_R2FR_3543_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "next_target": OUT / "P8_Y5_R2FR_3543_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3543_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["constructor_gate"], constructors, ["gate_id", "gate", "statement", "pass_effect", "current_status", "fallback", "claim_allowed"])
    write_csv(outputs["material_inputs"], materials, ["material_id", "material", "A", "Z", "minus_Q_mhat", "Q_mhat", "Q_e", "source", "status", "valid_for_claim"])
    write_csv(outputs["first_species_fill"], fills, ["fill_id", "coefficient_target", "projection_formula", "bound_inequality", "known_inputs", "missing_inputs", "score_ready", "mts_prediction_ready", "valid_for_claim"])
    write_csv(outputs["blockers"], blockers, ["blocker_id", "blocker", "requirement", "current_status", "consequence", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, constructors, materials, fills, blockers, decisions, status, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, constructors, materials, fills, blockers, decisions, status, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
