from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
EXT = ROOT / "source-intake" / "external-sources"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3363-Y5-R2FR-first-source-normalization-bound-row-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

MICROSCOPE_TEX = EXT / "microscope_2209.15488_source" / "chap9.tex"
ETA_CENTRAL = -1.5e-15
ETA_STAT = 2.3e-15
ETA_SYST = 1.5e-15
ETA_QUAD = math.sqrt(ETA_STAT**2 + ETA_SYST**2)
ETA_REPORTED = 2.7e-15
ETA_CONSERVATIVE = 2.8e-15
DOTG_BOUND = 4.0e-14
DOTG_INTERNAL_TARGET = 9.6e-15

LOCAL_SOURCES = [
    ("LSRC3363_0_3362_doc", ROOT / "3362-Y5-R2FR-source-current-gauge-lock-and-Gref-owner-under-AX1090.md", "3362 handoff"),
    ("LSRC3363_1_3362_next", OUT / "P8_Y5_R2FR_3362_NEXT_TARGET.csv", "3362 next target"),
    ("LSRC3363_2_3362_y5", OUT / "P8_Y5_R2FR_3362_Y5_RESULT_ROWS.csv", "3362 Y5 split"),
    ("LSRC3363_3_3362_gates", OUT / "P8_Y5_R2FR_3362_PROMOTION_GATES.csv", "3362 promotion gates"),
    ("LSRC3363_4_wep_bound_import", OUT / "P8_Y5_R2FR_2788_WEP_BOUND_IMPORT.csv", "MICROSCOPE WEP bound import"),
    ("LSRC3363_5_microscope_inputs", OUT / "P8_Y5_R2FR_3260_MICROSCOPE_DD_BOUND_INPUTS.csv", "MICROSCOPE numeric source inputs"),
    ("LSRC3363_6_microscope_evidence", OUT / "P8_Y5_R2FR_3260_MICROSCOPE_SOURCE_EVIDENCE_LINES.csv", "MICROSCOPE source evidence lines"),
    ("LSRC3363_7_microscope_tex", MICROSCOPE_TEX, "local MICROSCOPE TeX source"),
    ("LSRC3363_8_coupling_pack", OUT / "P8_Y5_R2FR_3271_COUPLING_BOUND_PACK_NONCLAIM.csv", "coupling bound pack"),
    ("LSRC3363_9_row_selection", OUT / "P8_Y5_R2FR_3272_FIRST_COUPLING_ROW_SELECTION.csv", "first coupling row selection"),
    ("LSRC3363_10_row_schema", OUT / "P8_Y5_R2FR_3272_FIRST_COUPLING_ROW_SCHEMA.csv", "first coupling row schema"),
    ("LSRC3363_11_source_current_rows", OUT / "P8_Y5_R2FR_3291_SOURCE_CURRENT_RESIDUAL_ROWS_NONCLAIM.csv", "source current residual rows"),
    ("LSRC3363_12_beta_reduction", OUT / "P8_Y5_R2FR_3291_BETA_SOURCE_ALPHA_REDUCTION.csv", "beta source alpha reduction"),
    ("LSRC3363_13_dotg_source", OUT / "P8_Y5_R2FR_2933_COUPLING_BOUND_SOURCE_ACQUISITION.csv", "dotG source-backed comparator"),
    ("LSRC3363_14_dotg_transfer", OUT / "P8_Y5_R2FR_2934_DOTG_BOUND_TRANSFER_SCORECARD.csv", "dotG transfer scorecard"),
    ("LSRC3363_15_r10_bound_rows", OUT / "P8_Y5_R2FR_3012_R10_BOUND_ROWS_NONCLAIM.csv", "R10 alpha bound rows"),
    ("LSRC3363_16_r10_anchor_rows", OUT / "P8_Y5_R2FR_2935_R10_SOURCE_BACKED_ANCHOR_ROWS.csv", "R10 source-backed anchors"),
    ("LSRC3363_17_r11_source_norm", OUT / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv", "R11 source-normalization rows"),
    ("LSRC3363_18_source_mass", OUT / "P8_Y5_R2FR_3109_SOURCE_MASS_LOCK_DELTA_GM_ROWS.csv", "source-mass DeltaGM rows"),
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3363_LOCAL_SOURCE_REGISTER.csv",
    "arena_scorecard": OUT / "P8_Y5_R2FR_3363_SOURCE_NORMALIZATION_ARENA_SCORECARD.csv",
    "first_bound": OUT / "P8_Y5_R2FR_3363_FIRST_SOURCE_NORMALIZATION_BOUND_ROW.csv",
    "projection_requirements": OUT / "P8_Y5_R2FR_3363_BOUND_TO_MTS_PROJECTION_REQUIREMENTS.csv",
    "runner": OUT / "P8_Y5_R2FR_3363_BOUND_ROW_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3363_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3363_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3363_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3363_VALIDATION.csv",
}


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parseable(path: Path) -> bool:
    try:
        if path.suffix.lower() == ".csv":
            read_csv(path)
        else:
            path.read_text(encoding="utf-8")
        return True
    except Exception:
        return False


def table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(compact(row.get(key, ""), 260).replace("|", "\\|") for key in headers) + " |")
    return "\n".join(lines) + "\n"


def local_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_str(path.exists()),
            "parseable": bool_str(path.exists() and parseable(path)),
            "usage": usage,
            "valid_for_claim": "false",
        }
        for source_id, path, usage in LOCAL_SOURCES
    ]


def arena_scorecard_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "SNB3363_0_MICROSCOPE_species_source_weight",
            "y5_channel": "species_source_charge",
            "arena": "MICROSCOPE_WEP",
            "observable": "eta_TiPt",
            "numeric_bound": f"{ETA_CONSERVATIVE:.12e}",
            "units": "dimensionless",
            "source_backed": "true",
            "why_selected": "tightest already source-backed Y5-relevant bound; directly attacks the species/source-weight survivor from 3362",
            "why_not_claim": "MTS-to-source-weight map, tau_WEP projection, and no-cancellation/source-readout assumptions remain unsigned",
            "selected_first_row": "true",
            "valid_external_bound": "true",
            "valid_mts_projection": "false",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "SNB3363_1_MESSENGER_time_drift",
            "y5_channel": "time_drift",
            "arena": "Mercury_MESSENGER_orbital",
            "observable": "|dotG/G|",
            "numeric_bound": f"{DOTG_BOUND:.12e}",
            "units": "yr^-1",
            "source_backed": "true",
            "why_selected": "not selected first: source-backed but weaker than the internal 9.6e-15 yr^-1 local lock and projection to kappa_MTS remains unsigned",
            "why_not_claim": "dotG/G includes source mass/readout/frame terms, not only parent kappa drift",
            "selected_first_row": "false",
            "valid_external_bound": "true",
            "valid_mts_projection": "false",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "SNB3363_2_R10_range_hair",
            "y5_channel": "radial_Meff_hair_or_bulk_X_tail",
            "arena": "short_range_R10",
            "observable": "alpha(lambda)",
            "numeric_bound": "alpha=1 at lambda=38.6 um anchor",
            "units": "dimensionless_at_length_anchor",
            "source_backed": "true_anchor_only",
            "why_selected": "not selected first: useful source-backed anchor, but not a full alpha(lambda) curve and not enough for interpolation/scoring",
            "why_not_claim": "anchor-only non-curve row and missing MTS alpha projection",
            "selected_first_row": "false",
            "valid_external_bound": "anchor_only",
            "valid_mts_projection": "false",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "SNB3363_3_EM_alpha_current_product",
            "y5_channel": "source_current_alpha_product",
            "arena": "MICROSCOPE_DD_EM_projection",
            "observable": "|b_alpha_or_Ce_product|",
            "numeric_bound": "1.389797711495e-12",
            "units": "dimensionless product",
            "source_backed": "derived_from_MICROSCOPE_DD_assumptions",
            "why_selected": "not selected first for Y5: strong EM-current row, but it is less directly source-normalization than Delta_w/source-weight",
            "why_not_claim": "requires parent alpha owner and tau/material projection rows",
            "selected_first_row": "false",
            "valid_external_bound": "conditional",
            "valid_mts_projection": "false",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "SNB3363_4_extra_mass_projection",
            "y5_channel": "DeltaGM_extra_mass_projection",
            "arena": "Newton_PPN_orbital",
            "observable": "DeltaGM_total / GM",
            "numeric_bound": "MISSING_NUMERIC_BOUND",
            "units": "dimensionless",
            "source_backed": "false",
            "why_selected": "not selected: this is central to source-normalized Newton, but no numeric source-backed row exists yet",
            "why_not_claim": "source mass lock and extra charge components remain unfilled",
            "selected_first_row": "false",
            "valid_external_bound": "false",
            "valid_mts_projection": "false",
            "valid_for_claim": "false",
        },
    ]


def first_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "Y5SN3363_0_MICROSCOPE_species_source_weight_bound",
            "target_y5_channel": "species_source_charge",
            "coefficient_symbol": "Delta_w_TiPt_or_epsilon_species_TiPt",
            "observable": "eta_WEP_source_charge_TiPt",
            "external_bound_abs": f"{ETA_CONSERVATIVE:.12e}",
            "external_bound_units": "dimensionless",
            "central_value": f"{ETA_CENTRAL:.12e}",
            "stat_uncertainty": f"{ETA_STAT:.12e}",
            "syst_uncertainty": f"{ETA_SYST:.12e}",
            "quadrature_uncertainty": f"{ETA_QUAD:.12e}",
            "reported_level": f"{ETA_REPORTED:.12e}",
            "source_path": str(MICROSCOPE_TEX),
            "source_url_or_doi": "https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102",
            "source_line_anchor": "chap9.tex:102; P8_Y5_R2FR_3260_MICROSCOPE_SOURCE_EVIDENCE_LINES.csv:MIC3260_abstract_result",
            "weak_field_map": "eta_source_AB = tau_WEP * Delta_w_AB + eta_other_channels; under tau_WEP=1 and no other channels, |Delta_w_TiPt| <= 2.8e-15",
            "no_cancellation_policy": "bound is componentwise only; no cancellation with EM, scalar, frame, clock, boundary, or readout channels is allowed for promotion",
            "projection_status": "BLOCKED_MISSING_TAU_WEP_SOURCE_READOUT_AND_NO_SOURCE_PREFACTOR_THEOREM",
            "valid_external_bound": "true",
            "valid_for_bound_packet": "true",
            "valid_mts_prediction_row": "false",
            "valid_for_claim": "false",
        }
    ]


def projection_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "PROJ3363_0_parent_coefficient_identity",
            "required_before_use": "Identify Delta_w_AB or epsilon_species_AB as an MTS parent coefficient/source-weight residual, not a post-fit label.",
            "math_form": "Delta_w_AB = partial_source ln(mu_obs_A/mu_obs_B) or parent source-only prefactor difference",
            "current_status": "NOT_PARENT_SIGNED",
            "blocks": "valid_mts_prediction_row",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "PROJ3363_1_tau_WEP_projection",
            "required_before_use": "Derive the WEP projection factor from the MTS source residual to the MICROSCOPE acceleration observable.",
            "math_form": "eta_TiPt = tau_WEP * Delta_w_TiPt + controlled_other_terms",
            "current_status": "MISSING",
            "blocks": "turning external eta bound into an MTS coefficient bound",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "PROJ3363_2_same_source_readout",
            "required_before_use": "Use the same observed coframe/time/source mass readout as the local GR/Newton branch.",
            "math_form": "g_source=g_orbit=g_clock=g_matter and tau_source=tau_orbit=tau_clock",
            "current_status": "NOT_SIGNED",
            "blocks": "hiding source normalization in readout/frame conversion",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "PROJ3363_3_no_cancellation_channels",
            "required_before_use": "Prove other composition-dependent channels vanish or score each channel componentwise.",
            "math_form": "eta_other_channels=0 or each |eta_i| <= bound_i with no sum cancellation",
            "current_status": "NOT_PROVED",
            "blocks": "componentwise claim",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "PROJ3363_4_no_source_prefactor_grammar",
            "required_before_use": "Either derive no source-only species prefactor grammar, or retain Delta_w_AB as a finite residual.",
            "math_form": "S_ord=sum_A S_A[Psi_A,g_obs,theta_A], no sum_A w_A S_A source selector",
            "current_status": "NEXT_THEOREM_TARGET",
            "blocks": "source universality/local GR source side",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "PROJ3363_5_source_mass_lock",
            "required_before_use": "Show the WEP source residual is the same source-normalization row entering Newtonian GM and PPN source mass.",
            "math_form": "Delta_w_AB -> DeltaGM_source and not merely a lab-specific acceleration proxy",
            "current_status": "OPEN",
            "blocks": "using MICROSCOPE bound as Newton/source-normalization closure",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    selected = first_bound_rows()[0]
    test_predictions = [
        ("RUN3363_0_zero_smoke", 0.0),
        ("RUN3363_1_half_bound_smoke", ETA_CONSERVATIVE / 2.0),
        ("RUN3363_2_twice_bound_smoke", ETA_CONSERVATIVE * 2.0),
    ]
    rows: list[dict[str, Any]] = []
    for run_id, prediction in test_predictions:
        rows.append(
            {
                "run_id": run_id,
                "row_id": selected["row_id"],
                "test_prediction_value": f"{prediction:.12e}",
                "bound_abs": selected["external_bound_abs"],
                "abs_le_bound": bool_str(abs(prediction) <= ETA_CONSERVATIVE),
                "runner_status": "PASS_NUMERIC_SMOKE_NONCLAIM" if abs(prediction) <= ETA_CONSERVATIVE else "FAIL_NUMERIC_SMOKE_NONCLAIM",
                "why_nonclaim": "smoke prediction is not a parent MTS coefficient; projection requirements remain unsigned",
                "valid_for_claim": "false",
            }
        )
    rows.append(
        {
            "run_id": "RUN3363_3_real_MTS_row_refusal",
            "row_id": selected["row_id"],
            "test_prediction_value": "MISSING_PARENT_DELTA_W_OR_EPSILON_SPECIES_VALUE",
            "bound_abs": selected["external_bound_abs"],
            "abs_le_bound": "false",
            "runner_status": "REFUSE_REAL_MTS_SCORE_MISSING_PARENT_PREDICTION",
            "why_nonclaim": "no parent coefficient value, tau_WEP projection, or source-readout theorem is supplied",
            "valid_for_claim": "false",
        }
    )
    return rows


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3363_0_external_bound_source_backed",
            "claim": "a real external bound row exists for Y5 species/source weight",
            "passed": "true",
            "reason": "MICROSCOPE Ti/Pt eta bound is locally sourced and numeric",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3363_1_positive_numeric_schema",
            "claim": "selected row has positive numeric bound, units, provenance, and no MISSING markers in external-bound fields",
            "passed": "true",
            "reason": "2.8e-15 dimensionless bound with MICROSCOPE path/URL/line anchor",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3363_2_parent_prediction_present",
            "claim": "MTS parent predicts Delta_w_TiPt or epsilon_species_TiPt",
            "passed": "false",
            "reason": "parent coefficient/source-weight residual is not supplied",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3363_3_tau_WEP_projection_present",
            "claim": "tau_WEP projection from MTS source-normalization residual to MICROSCOPE eta is derived",
            "passed": "false",
            "reason": "projection remains a requirement, not a derivation",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3363_4_no_cancellation_and_same_readout",
            "claim": "no-cancellation policy and same source/matter/orbit readout are parent-signed",
            "passed": "false",
            "reason": "other composition, frame, source-mass, and readout channels remain live",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3363_5_local_GR_Newton_claim",
            "claim": "source-normalized local GR/Newton is claim-ready",
            "passed": "false",
            "reason": "first external bound row is useful but does not derive or predict the source coupling",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3363_0",
            "question": "Did 3363 make the Y5 branch more testable?",
            "answer": "yes",
            "reason": "the species/source-weight survivor now has a concrete MICROSCOPE bound row with units, provenance, and a smoke runner",
            "next_action": "derive the no-source-prefactor/tau_WEP map or keep the row as an explicit finite residual",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3363_1",
            "question": "Did 3363 prove local GR/Newton source normalization?",
            "answer": "no",
            "reason": "external bound is not an MTS prediction; parent coefficient and projection map are missing",
            "next_action": "3364 should target no-source-prefactor grammar or WEP projection ownership",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3363_2",
            "question": "Why not use R10 or dotG first?",
            "answer": "WEP/source-weight is the clean first row",
            "reason": "R10 is anchor-only/non-curve; dotG is source-backed but mixes G drift, source mass, and readout/frame terms and is weaker than the internal local lock",
            "next_action": "keep R10/dotG as secondary rows after the WEP projection grammar is cleaned",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3364-Y5-R2FR-no-source-prefactor-grammar-or-WEP-projection-owner-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3364_no_source_prefactor_grammar_or_WEP_projection_owner.py",
            "objective": "try to prove the parent action has no source-only species prefactor and derive tau_WEP/source-readout projection for the 3363 MICROSCOPE row; if not, keep Delta_w_AB as an explicit finite residual",
            "why_next": "3363 supplies the bound; the missing piece is the MTS-to-observable projection/grammar, not another data row",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3365-Y5-R2FR-DeltaGM-extra-mass-projection-bound-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3365_DeltaGM_extra_mass_projection_bound_row.py",
            "objective": "attack the source-mass side of Y5: R_nonEH/R_symp/R_extra/R_boundary/R_time_frame as explicit DeltaGM rows with a numeric or theorem-zero route",
            "why_next": "MICROSCOPE bounds relative species/source weights; Newtonian source normalization also needs total source mass/charge closure",
            "valid_for_claim": "false",
        },
    ]


def validation_rows() -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = local_source_rows()
    arena_rows = arena_scorecard_rows()
    first_rows = first_bound_rows()
    projection_rows = projection_requirement_rows()
    runner = runner_rows()
    gate_rows = promotion_gate_rows()
    next_rows = next_target_rows()
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_str(passed),
                "detail": detail,
            }
        )

    selected = first_rows[0]
    bound_value = float(selected["external_bound_abs"])
    selected_text = " ".join(str(value) for value in selected.values())

    add("VAL3363_0_local_sources_exist", "all cited local source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3363_1_local_sources_parse", "all cited local source paths parse", all(row["parseable"] == "true" for row in sources))
    add("VAL3363_2_outputs_parse", "all 3363 non-validation outputs parse", all(path.exists() and parseable(path) for path in output_paths))
    add(
        "VAL3363_3_selected_external_bound_numeric",
        "selected first bound row has positive numeric external bound and units",
        bound_value > 0 and selected["external_bound_units"] == "dimensionless",
        f"bound={bound_value}",
    )
    add(
        "VAL3363_4_selected_external_bound_sourced",
        "selected first bound row has source path/URL/line anchor and no MISSING markers in external-bound fields",
        Path(selected["source_path"]).exists()
        and selected["source_url_or_doi"]
        and selected["source_line_anchor"]
        and "MISSING" not in selected["external_bound_abs"]
        and "MISSING" not in selected["source_path"],
    )
    add(
        "VAL3363_5_arena_scorecard_selects_WEP",
        "arena scorecard selects exactly one first row and it is the MICROSCOPE species/source-weight row",
        sum(1 for row in arena_rows if row["selected_first_row"] == "true") == 1
        and any(row["candidate_id"] == "SNB3363_0_MICROSCOPE_species_source_weight" and row["selected_first_row"] == "true" for row in arena_rows),
    )
    add(
        "VAL3363_6_projection_requirements_keep_claim_blocked",
        "projection requirements include parent coefficient, tau_WEP, same readout, no cancellation, no prefactor, and source mass lock",
        {row["requirement_id"] for row in projection_rows}
        == {
            "PROJ3363_0_parent_coefficient_identity",
            "PROJ3363_1_tau_WEP_projection",
            "PROJ3363_2_same_source_readout",
            "PROJ3363_3_no_cancellation_channels",
            "PROJ3363_4_no_source_prefactor_grammar",
            "PROJ3363_5_source_mass_lock",
        },
    )
    add(
        "VAL3363_7_runner_refuses_real_MTS_score",
        "smoke runner passes/fails toy values but refuses real MTS score without parent prediction",
        any(row["runner_status"] == "REFUSE_REAL_MTS_SCORE_MISSING_PARENT_PREDICTION" for row in runner)
        and any(row["runner_status"] == "FAIL_NUMERIC_SMOKE_NONCLAIM" for row in runner),
    )
    add(
        "VAL3363_8_no_overclaim",
        "parent prediction, tau projection, no-cancellation/readout, and local GR/Newton gates remain false",
        all(
            row["passed"] == "false"
            for row in gate_rows
            if row["gate_id"]
            in {
                "GATE3363_2_parent_prediction_present",
                "GATE3363_3_tau_WEP_projection_present",
                "GATE3363_4_no_cancellation_and_same_readout",
                "GATE3363_5_local_GR_Newton_claim",
            }
        )
        and all(row["valid_for_claim"] == "false" for row in first_rows + arena_rows + runner + gate_rows),
    )
    add(
        "VAL3363_9_next_target_projection_not_more_data",
        "next target attacks no-source-prefactor/WEP projection owner",
        any("WEP-projection-owner" in row["target_id"] or "WEP_projection_owner" in row["target_script"] for row in next_rows),
    )
    add(
        "VAL3363_10_write_scope_outside_formalization",
        "all 3363 write targets are outside formalization-workbench",
        all(FW not in path.parents and path != FW for path in [DOC, *output_paths, OUTPUTS["validation"]]),
        "write_targets=" + str(len([DOC, *output_paths, OUTPUTS["validation"]])),
    )
    add(
        "VAL3363_11_no_external_bound_missing_markers",
        "selected external-bound row does not use missing markers except in blocked projection status",
        "MISSING" not in selected["external_bound_abs"]
        and "MISSING" not in selected["central_value"]
        and "MISSING" not in selected["source_path"]
        and "MISSING" in selected["projection_status"],
    )
    overall = all(row["passed"] == "true" for row in checks)
    add(
        "VAL3363_12_overall",
        "3363 validation overall",
        overall,
        "all required checks passed" if overall else "one or more checks failed",
    )
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    first_rows: list[dict[str, Any]],
    projection_rows: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    sections = [
        "# 3363 - First Source-Normalization Bound Row Under AX1090",
        "",
        f"Generated: `{RUN_UTC}`",
        "",
        "## Summary",
        "- This checkpoint turns one Y5 source-normalization survivor into a real quantitative nonclaim row.",
        "- Selected row: MICROSCOPE Ti/Pt WEP bound as a species/source-weight ceiling, `|Delta_w_TiPt| <= 2.8e-15` only under the explicit `tau_WEP=1`, no-cancellation, same-readout assumptions.",
        "- This is progress because Y5 now has a source-backed finite external bound row, not just a symbolic `MISSING_SOURCE_NORMALIZATION` entry.",
        "- It is not an MTS prediction or local-GR proof: parent `Delta_w`, `tau_WEP`, source-readout, and no-source-prefactor grammar are still unsigned.",
        "- Next target is therefore projection/grammar ownership, not more broad data hunting.",
        "",
        "## Local Source Register",
        table(sources),
        "## Source-Normalization Arena Scorecard",
        table(arena_rows),
        "## First Source-Normalization Bound Row",
        table(first_rows),
        "## Bound-To-MTS Projection Requirements",
        table(projection_rows),
        "## Bound Row Runner Nonclaim",
        table(runner),
        "## Promotion Gates",
        table(gates),
        "## Decision Ledger",
        table(decisions),
        "## Next Target",
        table(next_rows),
        "## Validation",
        table(validations),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_output = {
        "local_sources": local_source_rows(),
        "arena_scorecard": arena_scorecard_rows(),
        "first_bound": first_bound_rows(),
        "projection_requirements": projection_requirement_rows(),
        "runner": runner_rows(),
        "gates": promotion_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(OUTPUTS[key], rows)
    validations = validation_rows()
    write_csv(OUTPUTS["validation"], validations)
    write_doc(
        rows_by_output["local_sources"],
        rows_by_output["arena_scorecard"],
        rows_by_output["first_bound"],
        rows_by_output["projection_requirements"],
        rows_by_output["runner"],
        rows_by_output["gates"],
        rows_by_output["decision"],
        rows_by_output["next"],
        validations,
    )
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
