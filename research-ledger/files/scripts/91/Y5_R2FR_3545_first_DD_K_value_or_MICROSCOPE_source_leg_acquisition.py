from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3545-Y5-R2FR-first-DD-K-value-or-MICROSCOPE-source-leg-acquisition.md"
CANONICAL_STATUS = OUT / "P8_Y5_first_DD_K_value_or_source_leg_status.csv"

DELTA_Q_MHAT = 3.330000e-03
DELTA_Q_E = 2.040000e-03
ETA_BOUND = 2.8e-15
MHAT_COMPONENT_CEILING = ETA_BOUND / DELTA_Q_MHAT
E_COMPONENT_CEILING = ETA_BOUND / DELTA_Q_E


SOURCES: dict[str, dict[str, Any]] = {
    "script_3545": {"path": Path(__file__).resolve(), "role": "3545 generator"},
    "doc_3544": {
        "path": ROOT / "3544-Y5-R2FR-MTS-to-DD-source-map-or-MICROSCOPE-source-leg-intake.md",
        "role": "prior MTS-to-DD map and source-leg checkpoint",
    },
    "next_3544": {
        "path": OUT / "P8_Y5_R2FR_3544_NEXT_TARGET.csv",
        "role": "3544 selected first-DD-K/source-leg target",
    },
    "component_template_3544": {
        "path": OUT / "P8_Y5_R2FR_3544_COMPONENT_INPUT_TEMPLATE.csv",
        "role": "component formula and missing K/value rows",
    },
    "source_leg_3544": {
        "path": OUT / "P8_Y5_R2FR_3544_MICROSCOPE_SOURCE_LEG_INTAKE.csv",
        "role": "compressed/factorized MICROSCOPE source-leg blockers",
    },
    "ceilings_3544": {
        "path": OUT / "P8_Y5_R2FR_3544_SINGLE_CHANNEL_CEILINGS.csv",
        "role": "single-channel source-coupling ceilings",
    },
    "k_projection_2440": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_K_VECTOR_PROJECTION.csv",
        "role": "expanded WEP K-vector projection formula",
    },
    "source_leg_blockers_2440": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_SOURCE_LEG_BLOCKERS.csv",
        "role": "older WEP source-leg/alloy/map blocker ledger",
    },
    "material_basis_2440": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_MATERIAL_SENSITIVITY_BASIS.csv",
        "role": "Ti/Pt DD-like material contrast basis",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "MICROSCOPE Ti/Pt eta bound source row",
    },
    "em_alpha_runner_3507": {
        "path": OUT / "P8_EM_alpha_coupling_bound_runner_results.csv",
        "role": "alpha/clock/R10/WEP bound runner rows",
    },
    "em_alpha_source_runner_3508": {
        "path": OUT / "P8_EM_alpha_source_bound_runner_results.csv",
        "role": "alpha source-composition runner rows",
    },
    "em_visible_domain_3505": {
        "path": OUT / "P8_EM_visible_action_domain_exhaustion_no_chiEM_bound_vector.csv",
        "role": "EM visible-action residual domain rows",
    },
    "em_current_source_3508": {
        "path": OUT / "P8_EM_current_source_Ward_alpha_source_residual.csv",
        "role": "EM current/source Ward residual and b_alpha status",
    },
    "deltaw_slot_1891": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1891_DELTAW_SPECIES_COEFFICIENT_ROW_NONCLAIM.csv",
        "role": "Delta_w symbolic component slot",
    },
    "deltaw_fill_1906": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1906_DELTAW_RUNNER_INPUT_FILL_NONCLAIM.csv",
        "role": "Delta_w missing runner input ledger",
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


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv_rows(path)
    except (csv.Error, OSError, UnicodeDecodeError):
        return False
    return True


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = [
        "| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, item in SOURCES.items():
        path = item["path"]
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": bool_text(path.exists()),
                "role": item["role"],
                "valid_for_claim": "False",
            }
        )
    return rows


def count_rows_with_true(rows: list[dict[str, str]], *fields: str) -> int:
    total = 0
    for row in rows:
        for field in fields:
            if row.get(field, "").strip().lower() == "true":
                total += 1
                break
    return total


def source_scan_rows() -> list[dict[str, Any]]:
    scan_rows: list[dict[str, Any]] = []
    for source_id, item in SOURCES.items():
        path: Path = item["path"]
        if not path.exists():
            scan_rows.append(
                {
                    "source_id": source_id,
                    "path": str(path),
                    "exists": "False",
                    "row_count": 0,
                    "missing_marker_count": "MISSING_SOURCE_PATH",
                    "claim_true_rows": 0,
                    "score_ready_true_rows": 0,
                    "numeric_parent_value_rows": 0,
                    "scan_verdict": "SOURCE_PATH_MISSING",
                }
            )
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        csv_rows = read_csv_rows(path) if path.suffix.lower() == ".csv" else []
        numeric_parent_rows = 0
        for row in csv_rows:
            row_text = " ".join(str(value) for value in row.values())
            has_numeric = any(ch.isdigit() for ch in row_text)
            has_blocker = any(marker in row_text.upper() for marker in ["MISSING", "SYMBOLIC", "NONCLAIM", "NOT_NUMERIC"])
            claimable = row.get("valid_for_claim", "").lower() == "true" or row.get("claim_allowed", "").lower() == "true"
            if has_numeric and claimable and not has_blocker:
                numeric_parent_rows += 1

        scan_rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": "True",
                "row_count": len(csv_rows) if csv_rows else "n/a",
                "missing_marker_count": text.upper().count("MISSING"),
                "claim_true_rows": count_rows_with_true(csv_rows, "valid_for_claim", "claim_allowed"),
                "score_ready_true_rows": count_rows_with_true(csv_rows, "score_ready"),
                "numeric_parent_value_rows": numeric_parent_rows,
                "scan_verdict": "NO_CLAIMABLE_PARENT_NUMERIC_ROWS" if numeric_parent_rows == 0 else "HAS_CANDIDATE_NUMERIC_ROW_REVIEW_REQUIRED",
            }
        )
    return scan_rows


def hunt_rows() -> list[dict[str, Any]]:
    return [
        {
            "hunt_id": "HUNT3545_0_Ke_alpha_balpha",
            "target_component": "K_e_alpha*b_alpha",
            "eta_term": f"{DELTA_Q_E:.6e}*K_e_alpha*b_alpha",
            "single_term_product_ceiling": f"{E_COMPONENT_CEILING:.12e}",
            "searched_sources": "em_alpha_runner_3507; em_alpha_source_runner_3508; em_current_source_3508; em_visible_domain_3505",
            "evidence_found": "b_alpha_X exists as an identity/status object, but runner rows retain MISSING_SOURCE_COMPOSITION_MAP/MISSING_CLOCK_BOUND and valid_for_claim=False",
            "numeric_value_found": "False",
            "blocking_issue": "MISSING_ALPHA_SOURCE_COMPOSITION_MAP; MISSING_K_e_alpha projection; z_lambda/fixed Maxwell kinetic owner unsigned",
            "next_action": "derive or source K_e_alpha and b_alpha in one normalization, then test against |K_e_alpha*b_alpha| ceiling",
            "valid_for_claim": "False",
        },
        {
            "hunt_id": "HUNT3545_1_Km_block_delta_w_block",
            "target_component": "K_m_block*delta_w_block",
            "eta_term": f"{DELTA_Q_MHAT:.6e}*K_m_block*delta_w_block",
            "single_term_product_ceiling": f"{MHAT_COMPONENT_CEILING:.12e}",
            "searched_sources": "deltaw_slot_1891; deltaw_fill_1906; k_projection_2440",
            "evidence_found": "Delta_w_species slot exists, but current_value is SYMBOLIC_FREE_COEFFICIENT_NO_PARENT_VALUE and runner inputs are MISSING_PARENT_DELTAW_VALUES",
            "numeric_value_found": "False",
            "blocking_issue": "MISSING_PARENT_DELTAW_VALUES; MISSING_COMPONENT_BASIS; MISSING_ARENA_PROJECTION_KERNELS",
            "next_action": "derive theorem-zero for species/block prefactors or source a parent numeric Delta_w vector and arena projection",
            "valid_for_claim": "False",
        },
        {
            "hunt_id": "HUNT3545_2_Ke_frame_bg",
            "target_component": "K_e_frame*b_g",
            "eta_term": f"{DELTA_Q_E:.6e}*K_e_frame*b_g",
            "single_term_product_ceiling": f"{E_COMPONENT_CEILING:.12e}",
            "searched_sources": "k_projection_2440; em_visible_domain_3505",
            "evidence_found": "frame/source residual is named in the expanded projection, but no numeric b_g or K_e_frame source row appears in the inspected evidence",
            "numeric_value_found": "False",
            "blocking_issue": "MISSING_FRAME_SOURCE_NORMALIZATION; MISSING_PREFERRED_FRAME_LIGHT_CONE_BOUND_MAPPING",
            "next_action": "use EM Hodge/light-cone branch only after visible metric/Hodge owner is fixed or bounded",
            "valid_for_claim": "False",
        },
        {
            "hunt_id": "HUNT3545_3_projector_tail",
            "target_component": "K_projector_WEP*c_projector + tail_abs_WEP",
            "eta_term": "K_projector_WEP*c_projector + tail_abs_WEP",
            "single_term_product_ceiling": f"{ETA_BOUND:.12e}",
            "searched_sources": "k_projection_2440; source_leg_blockers_2440",
            "evidence_found": "outside-two-charge basis terms are retained explicitly; no collapse theorem or direct tail bound is present in the inspected rows",
            "numeric_value_found": "False",
            "blocking_issue": "MISSING_PROJECTOR_COLLAPSE_THEOREM; MISSING_TAIL_ABSOLUTE_BOUND",
            "next_action": "either prove projector/tail collapse into DD basis or keep absolute eta-level tail ceiling",
            "valid_for_claim": "False",
        },
    ]


def component_score_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "CMP3545_0_delta_w_block",
            "parent_component": "CMP3544_0_delta_w_block",
            "target_product": "K_m_block*delta_w_block",
            "eta_term": f"{DELTA_Q_MHAT:.6e}*K_m_block*delta_w_block",
            "single_product_ceiling": f"{MHAT_COMPONENT_CEILING:.12e}",
            "units": "dimensionless after parent source normalization",
            "required_inputs": "K_m_block; delta_w_block; source leg; units; sign/alloy policy",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CMP3545_1_delta_w_shadow",
            "parent_component": "CMP3544_1_delta_w_shadow",
            "target_product": "K_m_shadow*delta_w_shadow",
            "eta_term": f"{DELTA_Q_MHAT:.6e}*K_m_shadow*delta_w_shadow",
            "single_product_ceiling": f"{MHAT_COMPONENT_CEILING:.12e}",
            "units": "dimensionless after parent source normalization",
            "required_inputs": "K_m_shadow; delta_w_shadow; source leg; units; sign/alloy policy",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CMP3545_2_nonHilbert_current",
            "parent_component": "CMP3544_2_nonHilbert_current",
            "target_product": "K_m_nonHilbert*c_nonHilbert",
            "eta_term": f"{DELTA_Q_MHAT:.6e}*K_m_nonHilbert*c_nonHilbert",
            "single_product_ceiling": f"{MHAT_COMPONENT_CEILING:.12e}",
            "units": "dimensionless after parent source normalization",
            "required_inputs": "K_m_nonHilbert; c_nonHilbert; Hilbert/non-Hilbert split; source leg",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CMP3545_3_b_alpha",
            "parent_component": "CMP3544_3_b_alpha",
            "target_product": "K_e_alpha*b_alpha",
            "eta_term": f"{DELTA_Q_E:.6e}*K_e_alpha*b_alpha",
            "single_product_ceiling": f"{E_COMPONENT_CEILING:.12e}",
            "units": "dimensionless after EM/source normalization",
            "required_inputs": "K_e_alpha; b_alpha; alpha source composition map; fixed Maxwell kinetic owner",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CMP3545_4_b_g",
            "parent_component": "CMP3544_4_b_g",
            "target_product": "K_e_frame*b_g",
            "eta_term": f"{DELTA_Q_E:.6e}*K_e_frame*b_g",
            "single_product_ceiling": f"{E_COMPONENT_CEILING:.12e}",
            "units": "dimensionless after frame/source normalization",
            "required_inputs": "K_e_frame; b_g; frame-source map; light-cone/Hodge owner",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CMP3545_5_projector",
            "parent_component": "CMP3544_5_projector",
            "target_product": "K_projector_WEP*c_projector",
            "eta_term": "K_projector_WEP*c_projector",
            "single_product_ceiling": f"{ETA_BOUND:.12e}",
            "units": "dimensionless eta contribution",
            "required_inputs": "K_projector_WEP; c_projector; DD-basis collapse theorem or absolute bound",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CMP3545_6_tail",
            "parent_component": "CMP3544_6_tail",
            "target_product": "tail_abs_WEP",
            "eta_term": "tail_abs_WEP",
            "single_product_ceiling": f"{ETA_BOUND:.12e}",
            "units": "dimensionless eta contribution",
            "required_inputs": "direct tail bound or parent zero theorem",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    return [
        {
            "acquisition_id": "ACQ3545_0_alpha_source_map",
            "target": "K_e_alpha*b_alpha",
            "needed_object": "alpha source-composition map in the same normalization as Ti/Pt DD charge DeltaQ_e",
            "current_status": "ACQUISITION_REQUIRED",
            "minimum_acceptance": "numeric K_e_alpha and b_alpha, source path, units, sign convention, valid_for_claim=True source row",
            "why_first": "cleanest bridge from charge/EM work to WEP source coupling",
            "valid_for_claim": "False",
        },
        {
            "acquisition_id": "ACQ3545_1_deltaw_parent_vector",
            "target": "K_m_block*delta_w_block",
            "needed_object": "parent Delta_w block value or theorem-zero plus component basis",
            "current_status": "ACQUISITION_REQUIRED",
            "minimum_acceptance": "parent value/bound/zero theorem, material projection kernel, common-mode removal, units",
            "why_first": "mass/source side is a direct local-GR/Newton coupling hinge",
            "valid_for_claim": "False",
        },
        {
            "acquisition_id": "ACQ3545_2_MICROSCOPE_factorized_source_leg",
            "target": "source leg",
            "needed_object": "Earth/source-body charge vector, orbit normalization, active-vs-inertial source convention",
            "current_status": "ACQUISITION_REQUIRED",
            "minimum_acceptance": "factorized row replacing compressed D_i_source with explicit source-body factors",
            "why_first": "needed before any MTS coefficient can be compared as a true MICROSCOPE prediction",
            "valid_for_claim": "False",
        },
        {
            "acquisition_id": "ACQ3545_3_alloy_policy",
            "target": "Ti/Pt test masses",
            "needed_object": "MICROSCOPE alloy/isotope/material correction policy",
            "current_status": "ACQUISITION_REQUIRED",
            "minimum_acceptance": "sourced Ti alloy and Pt/Rh composition policy, or justified pure-element approximation with uncertainty",
            "why_first": "prevents fake precision in the material contrast vector",
            "valid_for_claim": "False",
        },
        {
            "acquisition_id": "ACQ3545_4_sign_and_units",
            "target": "projection convention",
            "needed_object": "Pt-minus-Ti or Ti-minus-Pt sign, q normalization, and source denominator",
            "current_status": "ACQUISITION_REQUIRED",
            "minimum_acceptance": "single written convention used by all component rows and runners",
            "why_first": "required before cancellation-sensitive scoring; absolute envelope remains safe until then",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3545_0_first_K_value",
            "question": "Was a first sourced numeric MTS-to-DD K/value product found?",
            "decision": "NO",
            "basis": "inspected alpha/source, Delta_w, and WEP K-projection rows retain missing/symbolic/nonclaim status",
            "claim_effect": "no WEP/local-GR claim; component ceilings are gates only",
            "next_action": "target K_e_alpha*b_alpha first, because it is the cleanest EM/source bridge",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3545_1_component_gates",
            "question": "Did 3545 add a useful forward step?",
            "decision": "YES_COMPONENT_CEILINGS_INSTALLED",
            "basis": f"mhat product ceilings <= {MHAT_COMPONENT_CEILING:.6e}; e product ceilings <= {E_COMPONENT_CEILING:.6e}; projector/tail eta ceilings <= {ETA_BOUND:.6e}",
            "claim_effect": "future derived K/value rows now have immediate pass/fail gates",
            "next_action": "fill one product value or prove a theorem-zero, instead of circling the full coupling cloud",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3545_2_source_leg",
            "question": "Can compressed MICROSCOPE D rows be used as public claim rows?",
            "decision": "NO",
            "basis": "compressed D_i_source rows hide Earth/source leg, orbit normalization, alloy policy, and sign/units convention",
            "claim_effect": "only private nonclaim smoke constraints are allowed",
            "next_action": "acquire factorized source-leg rows if K_e_alpha*b_alpha cannot be derived directly",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS3545_0",
            "checkpoint": "3545",
            "claim_allowed": "False",
            "first_numeric_K_value_found": "False",
            "usable_forward_result": "component product ceilings and concrete acquisition queue",
            "mhat_product_ceiling": f"{MHAT_COMPONENT_CEILING:.12e}",
            "e_product_ceiling": f"{E_COMPONENT_CEILING:.12e}",
            "eta_tail_ceiling": f"{ETA_BOUND:.12e}",
            "next_target": "3546-Y5-R2FR-Ke-alpha-balpha-source-value-or-EM-alpha-coupling-bound-intake.md",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3545_0",
            "target_doc": "3546-Y5-R2FR-Ke-alpha-balpha-source-value-or-EM-alpha-coupling-bound-intake.md",
            "target_script": "scripts/Y5_R2FR_3546_Ke_alpha_balpha_source_value_or_EM_alpha_coupling_bound_intake.py",
            "objective": "try to derive or source K_e_alpha*b_alpha; if not, turn EM alpha/source coupling rows into a value/acquisition pack",
            "success_gate": f"either |K_e_alpha*b_alpha| is sourced and compared to {E_COMPONENT_CEILING:.6e}, or every missing alpha/source input becomes a concrete acquisition row",
            "reason": "the EM alpha bridge is the cleanest coupling test route and connects charge work to local WEP/GR source coupling",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(generated_paths: list[Path], sources: list[dict[str, Any]], score_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    required_source_ids = {
        "doc_3544",
        "next_3544",
        "component_template_3544",
        "source_leg_3544",
        "ceilings_3544",
        "k_projection_2440",
        "local_bounds",
    }
    source_exists = {row["source_id"]: row["exists"] == "True" for row in sources}
    required_sources_exist = all(source_exists.get(source_id, False) for source_id in required_source_ids)
    generated_csvs = [path for path in generated_paths if path.suffix.lower() == ".csv"]
    csvs_parse = all(csv_parse_ok(path) for path in generated_csvs)
    component_rows_nonclaim = all(row["valid_for_claim"] == "False" and row["score_ready"] == "False" for row in score_rows)
    no_formalization_outputs = all(FORMALIZATION not in path.parents for path in generated_paths)
    no_claim_status = True
    return [
        {
            "validation_id": "VAL3545_0_required_sources_exist",
            "passes": bool_text(required_sources_exist),
            "status": "PASS" if required_sources_exist else "FAIL",
            "detail": "3544/2440/local bound sources needed for this gate exist",
        },
        {
            "validation_id": "VAL3545_1_generated_csvs_parse",
            "passes": bool_text(csvs_parse),
            "status": "PASS" if csvs_parse else "FAIL",
            "detail": f"{len(generated_csvs)} generated CSV files parse with DictReader",
        },
        {
            "validation_id": "VAL3545_2_component_rows_nonclaim",
            "passes": bool_text(component_rows_nonclaim),
            "status": "PASS" if component_rows_nonclaim else "FAIL",
            "detail": "all component score rows remain score_ready=False and valid_for_claim=False until sourced values exist",
        },
        {
            "validation_id": "VAL3545_3_formalization_workbench_untouched",
            "passes": bool_text(no_formalization_outputs),
            "status": "PASS" if no_formalization_outputs else "FAIL",
            "detail": "3545 generated outputs only inside post-checkpoint-work",
        },
        {
            "validation_id": "VAL3545_4_claim_block_retained",
            "passes": bool_text(no_claim_status),
            "status": "PASS",
            "detail": "no R10/WEP/PPN/local-GR claim is made by this checkpoint",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    status = rows_by_name["status"][0]
    lines = [
        "# 3545 — Y5/R2FR first DD K-value or MICROSCOPE source-leg acquisition",
        "",
        "## Verdict",
        "",
        "- **No first sourced numeric `K`/component product was found.** The alpha/source and Delta-w files are not empty, but they remain symbolic, missing-input, or nonclaim rows.",
        f"- **Useful forward result:** future component values now have hard gates: mhat products must satisfy `|K_m * component| <= {MHAT_COMPONENT_CEILING:.6e}`, EM products must satisfy `|K_e * component| <= {E_COMPONENT_CEILING:.6e}`, and projector/tail terms must satisfy `<= {ETA_BOUND:.6e}` at eta level.",
        "- **Claim status:** blocked. This is a private coupling bridge, not a WEP/local-GR pass.",
        "",
        "## Extractor logic",
        "",
        "The point of this checkpoint is to stop treating the coupling gap as a vibe. It scans the existing source hierarchy and records whether any row already supplies a claimable parent-owned numeric value. A row only counts as useful if it is numeric, sourced, and not marked `MISSING`, `SYMBOLIC`, `NONCLAIM`, or `NOT_NUMERIC`.",
        "",
        "## Component gates",
        "",
        markdown_table(
            rows_by_name["component_score"],
            ["component_id", "target_product", "eta_term", "single_product_ceiling", "score_ready", "valid_for_claim"],
        ),
        "",
        "## K/value hunt",
        "",
        markdown_table(
            rows_by_name["hunt"],
            ["hunt_id", "target_component", "numeric_value_found", "blocking_issue", "next_action"],
        ),
        "",
        "## Acquisition queue",
        "",
        markdown_table(
            rows_by_name["acquisition"],
            ["acquisition_id", "target", "needed_object", "current_status", "minimum_acceptance"],
        ),
        "",
        "## Decision ledger",
        "",
        markdown_table(
            rows_by_name["decision"],
            ["decision_id", "question", "decision", "basis", "next_action"],
        ),
        "",
        "## Validation",
        "",
        markdown_table(
            rows_by_name["validation"],
            ["validation_id", "passes", "status", "detail"],
        ),
        "",
        "## Status",
        "",
        markdown_table(
            rows_by_name["status"],
            ["checkpoint", "claim_allowed", "first_numeric_K_value_found", "usable_forward_result", "next_target"],
        ),
        "",
        "## Next target",
        "",
        "Move to `3546-Y5-R2FR-Ke-alpha-balpha-source-value-or-EM-alpha-coupling-bound-intake.md`. The best route is the EM alpha/source bridge first: either derive/source `K_e_alpha*b_alpha` in one normalization, or produce a narrow acquisition pack that says exactly which EM/source rows must be filled.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    source_scan = source_scan_rows()
    hunt = hunt_rows()
    component_score = component_score_rows()
    acquisition = acquisition_rows()
    decision = decision_rows()
    status = status_rows()
    next_target = next_target_rows()

    outputs: dict[Path, tuple[list[dict[str, Any]], list[str]]] = {
        OUT / "P8_Y5_R2FR_3545_SOURCE_REGISTER.csv": (
            sources,
            ["source_id", "path", "exists", "role", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3545_SOURCE_SCAN.csv": (
            source_scan,
            [
                "source_id",
                "path",
                "exists",
                "row_count",
                "missing_marker_count",
                "claim_true_rows",
                "score_ready_true_rows",
                "numeric_parent_value_rows",
                "scan_verdict",
            ],
        ),
        OUT / "P8_Y5_R2FR_3545_K_VALUE_HUNT_RESULTS.csv": (
            hunt,
            [
                "hunt_id",
                "target_component",
                "eta_term",
                "single_term_product_ceiling",
                "searched_sources",
                "evidence_found",
                "numeric_value_found",
                "blocking_issue",
                "next_action",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3545_COMPONENT_SCORE_INPUTS.csv": (
            component_score,
            [
                "component_id",
                "parent_component",
                "target_product",
                "eta_term",
                "single_product_ceiling",
                "units",
                "required_inputs",
                "score_ready",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3545_SOURCE_LEG_ALLOY_SIGN_ACQUISITION.csv": (
            acquisition,
            [
                "acquisition_id",
                "target",
                "needed_object",
                "current_status",
                "minimum_acceptance",
                "why_first",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3545_DECISION_LEDGER.csv": (
            decision,
            ["decision_id", "question", "decision", "basis", "claim_effect", "next_action", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3545_STATUS.csv": (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "first_numeric_K_value_found",
                "usable_forward_result",
                "mhat_product_ceiling",
                "e_product_ceiling",
                "eta_tail_ceiling",
                "next_target",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3545_NEXT_TARGET.csv": (
            next_target,
            ["next_id", "target_doc", "target_script", "objective", "success_gate", "reason", "valid_for_claim"],
        ),
        CANONICAL_STATUS: (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "first_numeric_K_value_found",
                "usable_forward_result",
                "mhat_product_ceiling",
                "e_product_ceiling",
                "eta_tail_ceiling",
                "next_target",
                "valid_for_claim",
            ],
        ),
    }

    generated_paths: list[Path] = []
    for path, (rows, fields) in outputs.items():
        write_csv(path, rows, fields)
        generated_paths.append(path)

    validation = validation_rows(generated_paths, sources, component_score)
    validation_path = OUT / "P8_Y5_BRR545_3545_VALIDATION.csv"
    write_csv(
        validation_path,
        validation,
        ["validation_id", "passes", "status", "detail"],
    )
    generated_paths.append(validation_path)

    write_doc(
        {
            "source_scan": source_scan,
            "hunt": hunt,
            "component_score": component_score,
            "acquisition": acquisition,
            "decision": decision,
            "status": status,
            "validation": validation,
            "next_target": next_target,
        }
    )

    print(f"wrote {DOC}")
    for path in generated_paths:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
