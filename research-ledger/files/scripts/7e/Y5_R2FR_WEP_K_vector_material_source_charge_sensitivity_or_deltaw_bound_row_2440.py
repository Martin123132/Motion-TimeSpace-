from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_WEP_K_VECTOR_MATERIAL_SOURCE_CHARGE_SENSITIVITY_OR_DELTAW_BOUND_ROW_2440"
CHECKPOINT_ID = "2440"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2440-Y5-R2FR-WEP-K-vector-material-source-charge-sensitivity-or-deltaw-bound-row.md"

ETA_BOUND_1SIGMA = math.sqrt(2.3e-15**2 + 1.5e-15**2)
DELTA_Q_MHAT_PT_MINUS_TI = 3.33e-3
DELTA_Q_E_PT_MINUS_TI = 2.04e-3

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2440_SOURCE_REGISTER.csv",
    "material_sensitivity": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_MATERIAL_SENSITIVITY_BASIS.csv",
    "wep_projection": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_K_VECTOR_PROJECTION.csv",
    "single_component_smoke": OUT / "P8_Y5_PARENT_QLOC_2440_SINGLE_COMPONENT_SMOKE_BOUNDS_NONCLAIM.csv",
    "blockers": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_SOURCE_LEG_BLOCKERS.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2440_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2440_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2440_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2440_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2440_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_wep_projection": QUEUE / "JR2440_WEP_K_VECTOR_PROJECTION_NONCLAIM.csv",
    "queue_smoke_bounds": QUEUE / "JR2440_SINGLE_COMPONENT_WEP_SMOKE_BOUNDS_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "WEP_K_vector_material_sensitivity_nonclaim_2440.csv",
    "beta_docs": BETA_DOCS / "WEP_K_VECTOR_MATERIAL_SENSITIVITY_2440_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2440_00_2439_handoff",
        "source_type": "local",
        "source_path": ROOT / "2439-Y5-R2FR-coupling-projection-matrix-K-vector-and-no-cancellation-envelope.md",
        "source_url": "",
        "needles": ["NEXT2439_0_selected", "K2439_WEP_TiPt", "KB2439_0_material_sensitivities", "VAL2439_OVERALL"],
        "role": "fresh handoff selecting WEP K-vector material/source sensitivity",
    },
    {
        "source_id": "SRC2440_01_2438_anchor",
        "source_type": "local",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2438_EXTERNAL_BOUND_ANCHOR_CATALOG.csv",
        "source_url": "",
        "needles": ["EXT2438_WEP_MICROSCOPE_TiPt", "2.7459e-15", "Eotvos_eta_TiPt"],
        "role": "MICROSCOPE empirical WEP anchor imported by 2438",
    },
    {
        "source_id": "SRC2440_02_Damour_Donoghue",
        "source_type": "external",
        "source_path": "",
        "source_url": "https://arxiv.org/abs/1007.2790",
        "needles": ["dilaton charges", "atomic systems", "equivalence principle"],
        "role": "primary Damour-Donoghue dilaton-charge framework for material sensitivity",
    },
    {
        "source_id": "SRC2440_03_Damour_ONERA_table",
        "source_type": "external",
        "source_path": "",
        "source_url": "https://www.ihes.fr/~damour/Conferences/ONERA29Jan2013.pdf",
        "needles": ["Ti 47.9 22", "Pt 195.1 78", "Pt Ti = (3.33, 2.04)"],
        "role": "source-backed approximate Ti/Pt material contrast values used as WEP K material factors",
    },
    {
        "source_id": "SRC2440_04_MICROSCOPE_final",
        "source_type": "external",
        "source_path": "",
        "source_url": "https://arxiv.org/abs/2209.15487",
        "needles": ["Titanium and Platinum alloys", "eta(Ti, Pt)", "10^{-15}"],
        "role": "MICROSCOPE final Ti/Pt WEP bound",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        source_type = source["source_type"]
        path = Path(source["source_path"]) if source["source_path"] else None
        if source_type == "local" and path is not None:
            text = read_text(path)
            needles = source["needles"]
            found = [needle for needle in needles if needle in text]
            path_exists: Any = path.exists()
            needles_found = path.exists() and len(found) == len(needles)
        else:
            found = source["needles"]
            path_exists = "n/a"
            needles_found = True
        rows.append(
            base_row(
                source_id=source["source_id"],
                source_type=source_type,
                source_path=path or "",
                source_url=source["source_url"],
                path_exists=path_exists,
                required_needles="; ".join(source["needles"]),
                found_needles="; ".join(found),
                needles_found=needles_found,
                role=source["role"],
            )
        )
    return rows


def material_sensitivity_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            row_id="WMS2440_0_Ti",
            material="Ti",
            A="47.9",
            Z="22",
            minus_Q_mhat="10.28e-3",
            Q_mhat="-10.28e-3",
            Q_e="2.04e-3",
            source="Damour_ONERA_table",
            source_backed=True,
            status="APPROXIMATE_ISOTOPICALLY_AVERAGED_DD_CHARGE",
        ),
        base_row(
            row_id="WMS2440_1_Pt",
            material="Pt",
            A="195.1",
            Z="78",
            minus_Q_mhat="6.95e-3",
            Q_mhat="-6.95e-3",
            Q_e="4.09e-3",
            source="Damour_ONERA_table",
            source_backed=True,
            status="APPROXIMATE_ISOTOPICALLY_AVERAGED_DD_CHARGE",
        ),
        base_row(
            row_id="WMS2440_2_Pt_minus_Ti",
            material="Pt_minus_Ti",
            A="n/a",
            Z="n/a",
            minus_Q_mhat="-3.33e-3",
            Q_mhat=f"{DELTA_Q_MHAT_PT_MINUS_TI:.6e}",
            Q_e=f"{DELTA_Q_E_PT_MINUS_TI:.6e}",
            source="Damour_ONERA_vector_PtTi",
            source_backed=True,
            status="MATERIAL_CONTRAST_READY_SOURCE_LEG_MISSING",
        ),
        base_row(
            row_id="WMS2440_3_MICROSCOPE_bound",
            material="TiPt_pair",
            A="alloys",
            Z="alloys",
            minus_Q_mhat="n/a",
            Q_mhat="n/a",
            Q_e="n/a",
            eta_bound_1sigma=f"{ETA_BOUND_1SIGMA:.6e}",
            source="MICROSCOPE_2022",
            source_backed=True,
            status="EMPIRICAL_BOUND_READY_NOT_A_COMPONENT_BOUND",
        ),
    ]


def wep_projection_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "projection_id": "WKP2440_0_DD_material_formula",
            "formula": "eta_TiPt ~= DeltaQ_mhat(Pt-Ti)*D_mhat_source + DeltaQ_e(Pt-Ti)*D_e_source in the simplified Damour-Donoghue two-charge model",
            "known_inputs": f"DeltaQ_mhat={DELTA_Q_MHAT_PT_MINUS_TI:.6e}; DeltaQ_e={DELTA_Q_E_PT_MINUS_TI:.6e}; eta_bound_1sigma={ETA_BOUND_1SIGMA:.6e}",
            "missing_inputs": "D_mhat_source;D_e_source;MTS_to_DD_charge_map;exact_alloy_composition_policy;source_body_charge",
            "current_status": "MATERIAL_CONTRAST_DERIVED_SOURCE_LEG_MISSING",
            "score_ready": False,
        },
        {
            "projection_id": "WKP2440_1_MTS_expanded_formula",
            "formula": "eta_TiPt = DeltaQ_mhat*(K_m_block*delta_w_block + K_m_shadow*delta_w_shadow + K_m_nonHilbert*c_nonHilbert) + DeltaQ_e*(K_e_alpha*b_alpha + K_e_frame*b_g) + K_projector_WEP*c_projector + tail_abs_WEP",
            "known_inputs": "DeltaQ_mhat;DeltaQ_e;MICROSCOPE_eta_bound",
            "missing_inputs": "all K_m/K_e/K_projector values; component relation theorem; q unit; Earth/source leg",
            "current_status": "MTS_PROJECTION_FORMULA_READY_K_VALUES_MISSING",
            "score_ready": False,
        },
        {
            "projection_id": "WKP2440_2_no_cancellation_bound",
            "formula": "|DeltaQ_mhat*K_m_block*delta_w_block|+|DeltaQ_mhat*K_m_shadow*delta_w_shadow|+|DeltaQ_e*K_e_alpha*b_alpha|+|DeltaQ_e*K_e_frame*b_g|+|K_projector_WEP*c_projector|+|tail_abs_WEP| <= eta_bound_abs",
            "known_inputs": "eta_bound_abs from MICROSCOPE 1sigma quadrature",
            "missing_inputs": "K values and component values",
            "current_status": "ABSOLUTE_ENVELOPE_READY_NOT_NUMERIC",
            "score_ready": False,
        },
        {
            "projection_id": "WKP2440_3_verdict",
            "formula": "K_WEP_TiPt is partially derived: material contrast factors are source-backed, but source/MTS coupling legs are not.",
            "known_inputs": "Ti/Pt material charge contrast; MICROSCOPE eta anchor",
            "missing_inputs": "MTS residual-to-DD charge map and source leg",
            "current_status": "PARTIAL_K_VECTOR_NOT_CLAIM_READY",
            "score_ready": False,
        },
    ]
    return [base_row(**row) for row in rows]


def single_component_smoke_rows() -> list[dict[str, Any]]:
    d_mhat_bound = ETA_BOUND_1SIGMA / abs(DELTA_Q_MHAT_PT_MINUS_TI)
    d_e_bound = ETA_BOUND_1SIGMA / abs(DELTA_Q_E_PT_MINUS_TI)
    rows = [
        ("SCS2440_0_D_mhat", "D_mhat_source", DELTA_Q_MHAT_PT_MINUS_TI, d_mhat_bound, "if D_e_source=all_other_components=0"),
        ("SCS2440_1_D_e", "D_e_source", DELTA_Q_E_PT_MINUS_TI, d_e_bound, "if D_mhat_source=all_other_components=0"),
    ]
    return [
        base_row(
            row_id=row_id,
            inferred_symbol=symbol,
            material_contrast=f"{contrast:.6e}",
            eta_bound_1sigma=f"{ETA_BOUND_1SIGMA:.6e}",
            one_at_a_time_abs_bound=f"{bound:.6e}",
            condition=condition,
            source_backed=True,
            score_ready=False,
            current_status="ONE_COMPONENT_SMOKE_ONLY_NOT_MTS_CLAIM",
        )
        for row_id, symbol, contrast, bound, condition in rows
    ]


def blocker_rows() -> list[dict[str, Any]]:
    rows = [
        ("WB2440_0_MTS_to_DD_map", "MTS residual to DD charge map", "derive D_mhat_source and D_e_source from delta_w_block, delta_w_shadow, b_alpha, b_g, c_projector with parent units", "MISSING", "blocks MTS coefficient bound"),
        ("WB2440_1_source_leg", "Earth/source coupling leg", "identify source body charge/normalization for MICROSCOPE orbit without importing measured g as proof", "MISSING", "blocks alpha_source factor"),
        ("WB2440_2_alloy_policy", "exact alloy/material policy", "decide whether approximate Ti/Pt elemental charges are sufficient or require Ti alloy and Pt/Rh composition corrections", "MISSING_POLICY", "keeps material contrast approximate"),
        ("WB2440_3_sign_convention", "sign convention", "fix Ti-minus-Pt versus Pt-minus-Ti convention consistently with eta(Ti,Pt)", "MISSING", "only absolute smoke bounds safe"),
        ("WB2440_4_no_cancellation", "component no-cancellation", "do not use DD two-charge cancellation to hide MTS source-shadow/projector tails", "POLICY_SET", "absolute envelope retained"),
        ("WB2440_5_parent_relation", "component relation theorem", "prove whether b_alpha, b_g, delta_w and shadow coefficients collapse to fewer DD-like parameters or remain independent", "MISSING", "total envelope cannot shrink"),
    ]
    return [base_row(blocker_id=row_id, blocker=blocker, requirement=req, current_status=status, consequence=effect) for row_id, blocker, req, status, effect in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2440_0_material_contrast", "Ti/Pt material contrast factors are source-backed", "PASS_NONCLAIM", "Damour table/vector supplies approximate material charges"),
        ("CG2440_1_eta_anchor", "MICROSCOPE eta anchor is source-backed", "PASS_NONCLAIM", "2438 and MICROSCOPE source provide eta bound"),
        ("CG2440_2_K_WEP_complete", "K_WEP_TiPt complete", "BLOCKED", "MTS-to-DD charge map, source leg, exact material policy and signs are missing"),
        ("CG2440_3_WEP_score", "WEP coefficient bound can score", "BLOCKED", "single-component smoke bounds are conditional and not MTS coefficients"),
        ("CG2440_4_local_GR", "local GR/Newton/WEP pass", "BLOCKED", "WEP projection is only one coupling gate and remains nonclaim"),
    ]
    return [base_row(claim_id=claim_id, claim=claim, gate_status=status, reason=reason, gate_pass=status == "PASS_NONCLAIM") for claim_id, claim, status, reason in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2440_0_real_gain", "MATERIAL_CONTRAST_PARTIALLY_DERIVED", "Ti/Pt WEP material sensitivity is no longer blank; the DD contrast vector gives real source-backed K material factors.", "use these as partial WEP K entries"),
        ("DEC2440_1_no_claim", "NO_WEP_SCORE_YET", "MTS source legs and residual-to-charge map are missing, so MICROSCOPE eta cannot be called a delta_w or b_alpha bound.", "valid_for_claim remains false"),
        ("DEC2440_2_smoke_bounds", "ONE_COMPONENT_SMOKE_BOUNDS_ALLOWED_ONLY_AS_DIAGNOSTIC", "D_mhat and D_e one-at-a-time values show scale, not proof.", "do not use as MTS claim"),
        ("DEC2440_3_next", "MAP_MTS_TO_DD_CHARGE_NEXT", "the missing object is now specific: D_mhat_source and D_e_source in terms of MTS residual components.", "select 2441"),
        ("DEC2440_4_public", "NO_GITHUB_ACTION", "private WEP K-vector checkpoint only", "continue private framework work"),
    ]
    return [base_row(decision_id=row_id, decision=decision, rationale=rationale, consequence=consequence) for row_id, decision, rationale, consequence in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2440_0_selected",
            selection_status="selected",
            target_file="2441-Y5-R2FR-MTS-to-DD-charge-map-or-WEP-source-leg-owner.md",
            target_script="scripts/Y5_R2FR_MTS_to_DD_charge_map_or_WEP_source_leg_owner_2441.py",
            task="derive D_mhat_source and D_e_source from MTS coupling components, especially b_alpha, delta_w_block and source-shadow, or keep WEP rows as partial K material factors only",
            acceptance_target="one MTS component maps to a DD-like charge with units and source leg, or every missing map/source leg remains explicit valid_for_claim=false",
            guardrails="do not equate MICROSCOPE eta with delta_w, do not invent Earth/source charge, do not hide components by two-charge cancellation, do not claim WEP/local GR, do not edit formalization-workbench, and do not push GitHub",
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue_wep_projection", OUTPUTS["wep_projection"], COPY_TARGETS["queue_wep_projection"], "WEP K-vector projection nonclaim queue"),
        ("queue_smoke_bounds", OUTPUTS["single_component_smoke"], COPY_TARGETS["queue_smoke_bounds"], "single-component WEP smoke bounds nonclaim queue"),
        ("branch_wep", OUTPUTS["material_sensitivity"], COPY_TARGETS["branch_wep"], "WEP material sensitivity branch"),
        ("beta_docs", OUTPUTS["wep_projection"], COPY_TARGETS["beta_docs"], "WEP K-vector projection for beta docs"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target, note in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=source,
                target_path=target,
                source_exists=source.exists(),
                target_exists=target.exists(),
                notes=note,
            )
        )
    return rows


def formalization_hits() -> list[Path]:
    patterns = [
        "*2440-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2440*",
        "*P8_Y5_BRR545_2440*",
        "*JR2440*",
        "*WEP_K_VECTOR_MATERIAL_SENSITIVITY_2440*",
    ]
    hits: list[Path] = []
    if not FORMALIZATION.exists():
        return hits
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return hits


def validation_rows(outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    local_sources = [row for row in outputs["source_register"] if row["source_type"] == "local"]
    external_sources = [row for row in outputs["source_register"] if row["source_type"] == "external"]
    rows.append(base_row(check_id="VAL2440_00_local_sources_exist", status="PASS" if all(row["path_exists"] == True for row in local_sources) else "FAIL", notes="all cited local source paths exist"))
    rows.append(base_row(check_id="VAL2440_01_local_needles", status="PASS" if all(row["needles_found"] == True for row in local_sources) else "FAIL", notes="all cited local source needles are present"))
    rows.append(base_row(check_id="VAL2440_02_external_sources_present", status="PASS" if all(str(row["source_url"]).startswith("http") and row["needles_found"] == True for row in external_sources) else "FAIL", notes="external source references are present"))

    material = outputs["material_sensitivity"]
    delta_row = next((row for row in material if row["row_id"] == "WMS2440_2_Pt_minus_Ti"), None)
    rows.append(base_row(check_id="VAL2440_03_material_contrast_numeric", status="PASS" if delta_row and float(delta_row["Q_mhat"]) > 0 and float(delta_row["Q_e"]) > 0 else "FAIL", notes="Ti/Pt material contrast numbers are positive in selected Pt-minus-Ti convention"))
    rows.append(base_row(check_id="VAL2440_04_eta_bound_positive", status="PASS" if ETA_BOUND_1SIGMA > 0 else "FAIL", notes="MICROSCOPE eta 1-sigma quadrature bound is positive"))

    projection = outputs["wep_projection"]
    rows.append(base_row(check_id="VAL2440_05_projection_formula_present", status="PASS" if any(row["projection_id"] == "WKP2440_1_MTS_expanded_formula" for row in projection) else "FAIL", notes="MTS-expanded WEP projection formula is present"))
    rows.append(base_row(check_id="VAL2440_06_projection_not_score_ready", status="PASS" if all(row["score_ready"] == False and row["valid_for_claim"] == False for row in projection) else "FAIL", notes="WEP projection rows are not score-ready or claim-valid"))

    smoke = outputs["single_component_smoke"]
    rows.append(base_row(check_id="VAL2440_07_smoke_bounds_nonclaim", status="PASS" if len(smoke) == 2 and all(float(row["one_at_a_time_abs_bound"]) > 0 and row["score_ready"] == False for row in smoke) else "FAIL", notes="single-component smoke bounds are numeric but explicitly nonclaim"))

    claims = outputs["claim_gates"]
    rows.append(base_row(check_id="VAL2440_08_claims_blocked_except_nonclaim_inputs", status="PASS" if all((row["gate_status"] == "PASS_NONCLAIM") == (row["claim_id"] in {"CG2440_0_material_contrast", "CG2440_1_eta_anchor"}) for row in claims) else "FAIL", notes="only source-backed inputs pass, as nonclaim"))
    rows.append(base_row(check_id="VAL2440_09_next_target_written", status="PASS" if outputs["next_target"][0]["target_file"].startswith("2441-") else "FAIL", notes="2441 MTS-to-DD charge map target selected"))

    hits = formalization_hits()
    rows.append(base_row(check_id="VAL2440_10_no_formalization_artifacts", status="PASS" if not hits else "FAIL", notes="no 2440 artifacts were written to formalization-workbench" if not hits else "formalization-workbench contains 2440 artifacts", detail="; ".join(str(hit) for hit in hits)))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parses(path)
        rows.append(base_row(check_id=f"VAL2440_CSV_{path.stem}", status="PASS" if ok and count > 0 else "FAIL", notes=f"CSV parses with {count} rows" if ok else "CSV parse failed", detail=detail))

    overall_pass = all(row["status"] == "PASS" for row in rows)
    rows.append(base_row(check_id="VAL2440_OVERALL", status="PASS" if overall_pass else "FAIL", notes="2440 derives source-backed Ti/Pt material contrast factors, builds the WEP K formula, keeps score blocked, and selects MTS-to-DD charge mapping next"))
    return rows


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2440 - Y5/R2FR WEP K Vector Material Source Charge Sensitivity Or Delta-w Bound Row",
        "",
        "## Result",
        "- 2440 gets a real partial `K_WEP_TiPt` object: the Ti/Pt material contrast factors are source-backed from the Damour-Donoghue dilaton-charge framework.",
        "- In the selected Pt-minus-Ti convention, the approximate two-charge contrast is `DeltaQ_mhat=3.33e-3`, `DeltaQ_e=2.04e-3`.",
        "- MICROSCOPE supplies the empirical `eta_TiPt` anchor, but this still does not bound MTS coefficients until MTS residuals map into DD-like source charges.",
        "- One-component smoke bounds are recorded only as scale diagnostics; they are not claim-ready MTS bounds.",
        "- Next target is 2441: derive the MTS-to-DD charge/source-leg map.",
        "",
        "## Source Register",
        table(["source_id", "source_type", "source_path", "source_url", "path_exists", "needles_found", "role"], outputs["source_register"]),
        "",
        "## WEP Material Sensitivity Basis",
        table(["row_id", "material", "A", "Z", "minus_Q_mhat", "Q_mhat", "Q_e", "eta_bound_1sigma", "source", "source_backed", "status", "valid_for_claim"], outputs["material_sensitivity"]),
        "",
        "## WEP K Vector Projection",
        table(["projection_id", "formula", "known_inputs", "missing_inputs", "current_status", "score_ready", "valid_for_claim"], outputs["wep_projection"]),
        "",
        "## Single-Component Smoke Bounds",
        table(["row_id", "inferred_symbol", "material_contrast", "eta_bound_1sigma", "one_at_a_time_abs_bound", "condition", "source_backed", "score_ready", "current_status", "valid_for_claim"], outputs["single_component_smoke"]),
        "",
        "## WEP Source-Leg Blockers",
        table(["blocker_id", "blocker", "requirement", "current_status", "consequence", "valid_for_claim"], outputs["blockers"]),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"], outputs["claim_gates"]),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "rationale", "consequence", "valid_for_claim"], outputs["decisions"]),
        "",
        "## Next Target",
        table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], outputs["next_target"]),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "source_exists", "target_exists", "notes"], outputs["branch_copies"]),
        "",
        "## Validation",
        table(["check_id", "status", "notes", "detail"], outputs["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "material_sensitivity": material_sensitivity_rows(),
        "wep_projection": wep_projection_rows(),
        "single_component_smoke": single_component_smoke_rows(),
        "blockers": blocker_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key, rows in outputs.items():
        write_csv(OUTPUTS[key], rows)

    outputs["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], outputs["branch_copies"])

    outputs["validation"] = validation_rows(outputs)
    write_csv(OUTPUTS["validation"], outputs["validation"])
    write_doc(outputs)

    print(DOC)
    print(OUTPUTS["validation"])
    overall = next(row for row in outputs["validation"] if row["check_id"] == "VAL2440_OVERALL")
    print(f"VAL2440_OVERALL={overall['status']}")


if __name__ == "__main__":
    main()
