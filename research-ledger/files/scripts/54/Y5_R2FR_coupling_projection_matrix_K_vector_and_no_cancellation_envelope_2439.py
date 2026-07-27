from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_COUPLING_PROJECTION_MATRIX_K_VECTOR_AND_NO_CANCELLATION_ENVELOPE_2439"
CHECKPOINT_ID = "2439"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2439-Y5-R2FR-coupling-projection-matrix-K-vector-and-no-cancellation-envelope.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2439_SOURCE_REGISTER.csv",
    "component_basis": OUT / "P8_Y5_PARENT_QLOC_2439_COUPLING_COMPONENT_BASIS.csv",
    "projection_matrix": OUT / "P8_Y5_PARENT_QLOC_2439_K_PROJECTION_MATRIX.csv",
    "no_cancellation": OUT / "P8_Y5_PARENT_QLOC_2439_NO_CANCELLATION_ENVELOPE.csv",
    "k_blockers": OUT / "P8_Y5_PARENT_QLOC_2439_K_VECTOR_BLOCKERS.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2439_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2439_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2439_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2439_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2439_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_projection": QUEUE / "JR2439_K_PROJECTION_MATRIX_NONCLAIM.csv",
    "queue_blockers": QUEUE / "JR2439_K_VECTOR_BLOCKERS_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "K_projection_matrix_WEP_first_nonclaim_2439.csv",
    "beta_docs": BETA_DOCS / "K_PROJECTION_MATRIX_2439_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2439_00_2438_handoff",
        "source_path": ROOT / "2438-Y5-R2FR-first-real-coupling-coefficient-bound-source-acquisition-or-no-shadow-constructor-signature.md",
        "needles": ["NEXT2438_0_selected", "FRCB2438_0_delta_w_block_WEP", "PB2438_1_K_vectors", "VAL2438_OVERALL"],
        "role": "fresh handoff selecting K-vector projection matrix",
    },
    {
        "source_id": "SRC2439_01_2438_bounds",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2438_FIRST_REAL_COEFFICIENT_BOUND_ROWS_NONCLAIM.csv",
        "needles": ["FRCB2438_0_delta_w_block_WEP", "FRCB2438_1_b_alpha_clock", "FRCB2438_2_b_g_PPN", "FRCB2438_3_R10_yukawa"],
        "role": "first real source-backed empirical anchor rows",
    },
    {
        "source_id": "SRC2439_02_2438_anchors",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2438_EXTERNAL_BOUND_ANCHOR_CATALOG.csv",
        "needles": ["EXT2438_WEP_MICROSCOPE_TiPt", "EXT2438_PPN_CASSINI_GAMMA", "EXT2438_CLOCK_ROSENBAND_ALPHA_DOT", "EXT2438_R10_TAN_2020"],
        "role": "external bound anchor catalog",
    },
    {
        "source_id": "SRC2439_03_2437_basis",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2437_SHADOW_COEFFICIENT_BASIS.csv",
        "needles": ["SCB2437_0_delta_w_block", "SCB2437_4_c_frame_bg", "SCB2437_5_b_alpha", "SCB2437_7_total_abs"],
        "role": "coupling/source-shadow component basis",
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
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                source_path=path,
                path_exists=path.exists(),
                required_needles="; ".join(needles),
                found_needles="; ".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=source["role"],
            )
        )
    return rows


def component_basis_rows() -> list[dict[str, Any]]:
    rows = [
        ("CBASE2439_0_delta_w_block", "delta_w_block", "relative active-source weight over disconnected ordinary exchange blocks", "dimensionless", "source_weight"),
        ("CBASE2439_1_delta_w_shadow", "delta_w_shadow", "non-Hilbert/post-Hilbert source-shadow weight", "dimensionless_if_normalized_to_T_H", "source_shadow"),
        ("CBASE2439_2_b_alpha", "b_alpha", "hidden-visible fine-structure/gauge kinetic coefficient slope", "dimensionless_or_per_q_unit", "visible_coefficient"),
        ("CBASE2439_3_b_g", "b_g", "shadow-frame/coframe Weyl/disformal coefficient slope", "dimensionless_or_per_q_unit", "frame_coefficient"),
        ("CBASE2439_4_c_projector", "c_projector", "projector/source-worldtube/readout reentry coefficient", "operator_or_projector_units", "readout_projector"),
        ("CBASE2439_5_c_nonHilbert", "c_nonHilbert", "spin/torsion/non-Hilbert current leakage coefficient", "connection_source_units", "nonHilbert_current"),
        ("CBASE2439_6_tail_abs", "tail_abs", "absolute residual for any not-yet-classified coupling tail", "arena_units", "no_cancellation_guard"),
    ]
    return [
        base_row(
            component_id=row_id,
            symbol=symbol,
            definition=definition,
            units=units,
            component_class=component_class,
            independent_status="ASSUME_INDEPENDENT_UNTIL_PARENT_RELATION_SIGNED",
            numeric_value="",
            source_backed=False,
            score_ready=False,
        )
        for row_id, symbol, definition, units, component_class in rows
    ]


def projection_matrix_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "k_row_id": "K2439_WEP_TiPt",
            "observable": "eta_TiPt",
            "anchor_id": "EXT2438_WEP_MICROSCOPE_TiPt",
            "bound_row_id": "FRCB2438_0_delta_w_block_WEP",
            "formula": "eta_TiPt = K_WEP_block_TiPt*delta_w_block + K_WEP_shadow_TiPt*delta_w_shadow + K_WEP_alpha_TiPt*b_alpha + K_WEP_bg_TiPt*b_g + K_WEP_proj_TiPt*c_projector + tail_abs_WEP",
            "component_columns": "delta_w_block;delta_w_shadow;b_alpha;b_g;c_projector;tail_abs",
            "required_inputs": "Ti/Pt material charge sensitivities; Earth/source composition charge; parent source normalization; q unit; body/worldtube projection",
            "formula_status": "FORMULA_DEFINED_K_VALUES_MISSING",
            "k_numeric_status": "MISSING",
            "score_ready": False,
        },
        {
            "k_row_id": "K2439_CLOCK_ALPHA",
            "observable": "alpha_dot_over_alpha",
            "anchor_id": "EXT2438_CLOCK_ROSENBAND_ALPHA_DOT",
            "bound_row_id": "FRCB2438_1_b_alpha_clock",
            "formula": "alpha_dot/alpha = K_clock_alpha*b_alpha*qdot_drive + K_clock_frame*b_g*qdot_drive + tail_abs_clock",
            "component_columns": "b_alpha;b_g;tail_abs",
            "required_inputs": "parent local time/drive qdot; clock sensitivity basis; coefficient target owner; units converting q to per-year drift",
            "formula_status": "FORMULA_DEFINED_DRIVE_AND_K_VALUES_MISSING",
            "k_numeric_status": "MISSING",
            "score_ready": False,
        },
        {
            "k_row_id": "K2439_PPN_GAMMA",
            "observable": "gamma_minus_one",
            "anchor_id": "EXT2438_PPN_CASSINI_GAMMA",
            "bound_row_id": "FRCB2438_2_b_g_PPN",
            "formula": "gamma-1 = K_gamma_bg*b_g + K_gamma_shadow*delta_w_shadow + K_gamma_nonHilbert*c_nonHilbert + tail_abs_PPN",
            "component_columns": "b_g;delta_w_shadow;c_nonHilbert;tail_abs",
            "required_inputs": "weak-field metric response; frame/coframe normalization; affine/nonHilbert response; solar-system source/test branch",
            "formula_status": "FORMULA_DEFINED_K_VALUES_MISSING",
            "k_numeric_status": "MISSING",
            "score_ready": False,
        },
        {
            "k_row_id": "K2439_R10_YUKAWA",
            "observable": "alpha_Yukawa(lambda)",
            "anchor_id": "EXT2438_R10_TAN_2020;EXT2438_R10_KAPNER_2007",
            "bound_row_id": "FRCB2438_3_R10_yukawa",
            "formula": "alpha_Y(lambda)=K_R10_bg(lambda)*b_g + K_R10_shadow(lambda)*delta_w_shadow + K_R10_proj(lambda)*c_projector + K_R10_block(lambda)*delta_w_block + tail_abs_R10(lambda)",
            "component_columns": "b_g;delta_w_shadow;c_projector;delta_w_block;tail_abs",
            "required_inputs": "lambda-dependent source/test product law; finite-range kernel normalization; source/test composition legs; full digitized alpha(lambda) curve",
            "formula_status": "FORMULA_DEFINED_LAMBDA_K_VALUES_AND_CURVE_MISSING",
            "k_numeric_status": "MISSING",
            "score_ready": False,
        },
        {
            "k_row_id": "K2439_TOTAL_ABS",
            "observable": "all_local_anchors",
            "anchor_id": "all_EXT2438",
            "bound_row_id": "FRCB2438_4_total_abs",
            "formula": "B_total_abs(arena)=sum_components |K_arena,component * component| + |tail_abs_arena| with no cross-arena cancellation",
            "component_columns": "delta_w_block;delta_w_shadow;b_alpha;b_g;c_projector;c_nonHilbert;tail_abs",
            "required_inputs": "all K rows above; component basis independence or parent-signed relations; arena-specific units",
            "formula_status": "ABSOLUTE_ENVELOPE_FORMULA_DEFINED_VALUES_MISSING",
            "k_numeric_status": "MISSING",
            "score_ready": False,
        },
    ]
    return [base_row(**row, source_backed_formula=True, valid_for_claim=False) for row in rows]


def no_cancellation_rows() -> list[dict[str, Any]]:
    rows = [
        ("NCE2439_0_WEP", "WEP", "B_WEP_abs=|K_WEP_block delta_w_block|+|K_WEP_shadow delta_w_shadow|+|K_WEP_alpha b_alpha|+|K_WEP_bg b_g|+|K_WEP_proj c_projector|+|tail_WEP|", "eta_TiPt_bound", "NO_SIGN_CANCELLATION_ALLOWED"),
        ("NCE2439_1_CLOCK", "clock", "B_clock_abs=|K_clock_alpha b_alpha qdot|+|K_clock_frame b_g qdot|+|tail_clock|", "alpha_dot_bound", "NO_TIME_DRIVE_CANCELLATION_ALLOWED"),
        ("NCE2439_2_PPN", "PPN", "B_PPN_abs=|K_gamma_bg b_g|+|K_gamma_shadow delta_w_shadow|+|K_gamma_nonHilbert c_nonHilbert|+|tail_PPN|", "gamma_minus_one_bound", "NO_METRIC_RESPONSE_CANCELLATION_ALLOWED"),
        ("NCE2439_3_R10", "R10", "B_R10_abs(lambda)=|K_R10_bg b_g|+|K_R10_shadow delta_w_shadow|+|K_R10_proj c_projector|+|K_R10_block delta_w_block|+|tail_R10(lambda)|", "alpha_Yukawa_bound_curve", "NO_SOURCE_TEST_LEG_CANCELLATION_ALLOWED"),
        ("NCE2439_4_TOTAL", "all", "B_total_abs=sum_arena B_arena_abs after converting only within declared arena units", "all_bounds", "NO_CROSS_ARENA_CANCELLATION_ALLOWED"),
    ]
    return [
        base_row(
            envelope_id=row_id,
            arena=arena,
            envelope_formula=formula,
            bound_target=target,
            policy=policy,
            numeric_ready=False,
        )
        for row_id, arena, formula, target, policy in rows
    ]


def k_blocker_rows() -> list[dict[str, Any]]:
    rows = [
        ("KB2439_0_material_sensitivities", "WEP material sensitivities", "Ti/Pt/Earth source charges for delta_w_block, b_alpha and shadow channels", "MISSING", "blocks K_WEP_TiPt"),
        ("KB2439_1_qdot_drive", "clock/time drive", "local qdot or clock-drive mapping for b_alpha/b_g temporal drift", "MISSING", "blocks K_clock_alpha"),
        ("KB2439_2_metric_response", "PPN weak-field response", "metric/coframe response of b_g and nonHilbert pieces in solar-system weak field", "MISSING", "blocks K_gamma_bg"),
        ("KB2439_3_R10_product_law", "R10 source/test product law", "lambda-dependent product of source and test legs with finite-range kernel normalization", "MISSING", "blocks K_R10(lambda)"),
        ("KB2439_4_full_R10_curve", "R10 bound curve", "digitized or tabulated alpha_bound(lambda), not anchor-only rows", "MISSING", "blocks R10 score"),
        ("KB2439_5_component_relations", "component relation theorem", "parent theorem relating b_alpha, b_g, delta_w, projector and nonHilbert channels, or independence assumption retained", "MISSING", "prevents reducing total envelope"),
        ("KB2439_6_units", "cross-arena units", "declared q unit and arena unit conversions", "MISSING", "prevents combined score"),
    ]
    return [base_row(blocker_id=row_id, blocker=blocker, required_input=req, current_status=status, consequence=effect) for row_id, blocker, req, status, effect in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2439_0_projection_formulas", "projection formulas exist", "PASS_NONCLAIM", "symbolic K projection rows are written"),
        ("CG2439_1_K_numeric", "K vector numeric/source-backed values exist", "BLOCKED", "all K values remain missing"),
        ("CG2439_2_score_bounds", "empirical anchors can bound MTS coefficients", "BLOCKED", "anchors cannot score until K vectors, q unit and component basis are owned"),
        ("CG2439_3_no_cancellation", "no-cancellation envelope policy exists", "PASS_NONCLAIM", "absolute envelope formulas are written but numeric-ready false"),
        ("CG2439_4_local_tests", "WEP/clock/PPN/R10 pass", "BLOCKED", "projection formulas are not scored"),
        ("CG2439_5_local_GR", "local GR/Newton reduction", "BLOCKED", "K matrix is only one gate among Q_v/J_q/boundary/projector/no-hair gates"),
    ]
    return [base_row(claim_id=claim_id, claim=claim, gate_status=status, reason=reason, gate_pass=status == "PASS_NONCLAIM") for claim_id, claim, status, reason in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2439_0_bridge_built", "K_MATRIX_SHAPE_BUILT", "empirical anchors now have a symbolic projection matrix into MTS coupling components", "we can see exactly what is missing"),
        ("DEC2439_1_no_numbers", "NO_K_VALUES_FILLED", "no parent formula supplies material/clock/metric/R10 K values yet", "no scoring or claims"),
        ("DEC2439_2_first_attack", "WEP_K_VECTOR_FIRST", "WEP has the cleanest real anchor and directly hits delta_w_block/source-shadow/material coefficients", "select WEP source-charge sensitivity target"),
        ("DEC2439_3_R10_later", "R10_REQUIRES_FULL_CURVE_AND_PRODUCT_LAW", "anchor-only Yukawa rows are not enough for a robust R10 score", "keep R10 as later source/test leg target"),
        ("DEC2439_4_public", "NO_GITHUB_ACTION", "private projection-matrix checkpoint only", "continue private framework work"),
    ]
    return [base_row(decision_id=row_id, decision=decision, rationale=rationale, consequence=consequence) for row_id, decision, rationale, consequence in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2439_0_selected",
            selection_status="selected",
            target_file="2440-Y5-R2FR-WEP-K-vector-material-source-charge-sensitivity-or-deltaw-bound-row.md",
            target_script="scripts/Y5_R2FR_WEP_K_vector_material_source_charge_sensitivity_or_deltaw_bound_row_2440.py",
            task="derive the WEP projection vector K_WEP_TiPt from material/source charge sensitivities and the parent source normalization, or keep delta_w_block/delta_w_shadow/b_alpha as explicit nonclaim rows with missing sensitivity inputs",
            acceptance_target="K_WEP formula becomes parent-owned enough to map MICROSCOPE eta_TiPt to component bounds, or every missing material/source sensitivity is listed with valid_for_claim=false",
            guardrails="do not invent composition charges, do not use MICROSCOPE eta directly as delta_w, do not cancel WEP components, do not claim WEP/local GR, do not edit formalization-workbench, and do not push GitHub",
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue_projection", OUTPUTS["projection_matrix"], COPY_TARGETS["queue_projection"], "symbolic K projection matrix nonclaim queue"),
        ("queue_blockers", OUTPUTS["k_blockers"], COPY_TARGETS["queue_blockers"], "K-vector blockers nonclaim queue"),
        ("branch_wep", OUTPUTS["projection_matrix"], COPY_TARGETS["branch_wep"], "WEP-first projection matrix branch"),
        ("beta_docs", OUTPUTS["no_cancellation"], COPY_TARGETS["beta_docs"], "no-cancellation envelopes for beta docs"),
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
        "*2439-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2439*",
        "*P8_Y5_BRR545_2439*",
        "*JR2439*",
        "*K_PROJECTION_MATRIX_2439*",
    ]
    hits: list[Path] = []
    if not FORMALIZATION.exists():
        return hits
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return hits


def validation_rows(outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources = outputs["source_register"]
    rows.append(base_row(check_id="VAL2439_00_sources_exist", status="PASS" if all(row["path_exists"] == True for row in sources) else "FAIL", notes="all cited source paths exist"))
    rows.append(base_row(check_id="VAL2439_01_source_needles", status="PASS" if all(row["needles_found"] == True for row in sources) else "FAIL", notes="all cited source needles are present"))

    matrix = outputs["projection_matrix"]
    observables = {row["observable"] for row in matrix}
    rows.append(base_row(check_id="VAL2439_02_required_projection_rows", status="PASS" if {"eta_TiPt", "alpha_dot_over_alpha", "gamma_minus_one", "alpha_Yukawa(lambda)", "all_local_anchors"}.issubset(observables) else "FAIL", notes="WEP, clock, PPN, R10 and total projection rows are present"))
    rows.append(base_row(check_id="VAL2439_03_no_numeric_K_values", status="PASS" if all(row["k_numeric_status"] == "MISSING" and row["score_ready"] == False for row in matrix) else "FAIL", notes="no K values are fabricated"))

    envelopes = outputs["no_cancellation"]
    rows.append(base_row(check_id="VAL2439_04_no_cancellation_envelopes", status="PASS" if all("NO_" in row["policy"] and row["numeric_ready"] == False for row in envelopes) else "FAIL", notes="absolute no-cancellation envelopes are present and nonnumeric"))

    blockers = outputs["k_blockers"]
    rows.append(base_row(check_id="VAL2439_05_blockers_present", status="PASS" if len(blockers) >= 6 and any(row["blocker_id"] == "KB2439_0_material_sensitivities" for row in blockers) else "FAIL", notes="K-vector blockers include WEP material sensitivities"))

    claims = outputs["claim_gates"]
    rows.append(base_row(check_id="VAL2439_06_claims_blocked_except_nonclaim_formulas", status="PASS" if all((row["gate_status"] == "PASS_NONCLAIM") == (row["claim_id"] in {"CG2439_0_projection_formulas", "CG2439_3_no_cancellation"}) for row in claims) else "FAIL", notes="only formula/envelope existence passes as nonclaim"))
    rows.append(base_row(check_id="VAL2439_07_next_target_written", status="PASS" if outputs["next_target"][0]["target_file"].startswith("2440-") else "FAIL", notes="2440 WEP K-vector target selected"))

    hits = formalization_hits()
    rows.append(base_row(check_id="VAL2439_08_no_formalization_artifacts", status="PASS" if not hits else "FAIL", notes="no 2439 artifacts were written to formalization-workbench" if not hits else "formalization-workbench contains 2439 artifacts", detail="; ".join(str(hit) for hit in hits)))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parses(path)
        rows.append(base_row(check_id=f"VAL2439_CSV_{path.stem}", status="PASS" if ok and count > 0 else "FAIL", notes=f"CSV parses with {count} rows" if ok else "CSV parse failed", detail=detail))

    overall_pass = all(row["status"] == "PASS" for row in rows)
    rows.append(base_row(check_id="VAL2439_OVERALL", status="PASS" if overall_pass else "FAIL", notes="2439 builds the symbolic K projection matrix and no-cancellation envelope, refuses numeric scoring, and selects WEP K-vector derivation next"))
    return rows


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2439 - Y5/R2FR Coupling Projection Matrix K Vector And No-Cancellation Envelope",
        "",
        "## Result",
        "- 2439 builds the missing bridge object: a symbolic projection matrix from MTS coupling components into WEP, clock, PPN and R10 observables.",
        "- No `K` values are filled.  That is deliberate: the matrix shape is derived, but material sensitivities, local drive, metric response and R10 source/test product laws are still missing.",
        "- The no-cancellation envelope is now explicit, so future fits cannot hide one residual by tuning another with an opposite sign.",
        "- The best next target is WEP first: derive `K_WEP_TiPt` or keep the MICROSCOPE row as source-backed/nonclaim.",
        "",
        "## Source Register",
        table(["source_id", "source_path", "path_exists", "needles_found", "role"], outputs["source_register"]),
        "",
        "## Coupling Component Basis",
        table(["component_id", "symbol", "definition", "units", "component_class", "independent_status", "score_ready", "valid_for_claim"], outputs["component_basis"]),
        "",
        "## K Projection Matrix",
        table(["k_row_id", "observable", "anchor_id", "bound_row_id", "formula", "component_columns", "required_inputs", "formula_status", "k_numeric_status", "score_ready", "valid_for_claim"], outputs["projection_matrix"]),
        "",
        "## No-Cancellation Envelope",
        table(["envelope_id", "arena", "envelope_formula", "bound_target", "policy", "numeric_ready", "valid_for_claim"], outputs["no_cancellation"]),
        "",
        "## K Vector Blockers",
        table(["blocker_id", "blocker", "required_input", "current_status", "consequence", "valid_for_claim"], outputs["k_blockers"]),
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
        "component_basis": component_basis_rows(),
        "projection_matrix": projection_matrix_rows(),
        "no_cancellation": no_cancellation_rows(),
        "k_blockers": k_blocker_rows(),
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
    overall = next(row for row in outputs["validation"] if row["check_id"] == "VAL2439_OVERALL")
    print(f"VAL2439_OVERALL={overall['status']}")


if __name__ == "__main__":
    main()
