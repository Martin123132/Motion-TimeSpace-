from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_FIRST_REAL_COUPLING_COEFFICIENT_BOUND_SOURCE_ACQUISITION_OR_NO_SHADOW_CONSTRUCTOR_SIGNATURE_2438"
CHECKPOINT_ID = "2438"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2438-Y5-R2FR-first-real-coupling-coefficient-bound-source-acquisition-or-no-shadow-constructor-signature.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2438_SOURCE_REGISTER.csv",
    "constructor_signature": OUT / "P8_Y5_PARENT_QLOC_2438_NO_SHADOW_CONSTRUCTOR_SIGNATURE_ATTEMPT.csv",
    "external_anchor_catalog": OUT / "P8_Y5_PARENT_QLOC_2438_EXTERNAL_BOUND_ANCHOR_CATALOG.csv",
    "coefficient_bound_rows": OUT / "P8_Y5_PARENT_QLOC_2438_FIRST_REAL_COEFFICIENT_BOUND_ROWS_NONCLAIM.csv",
    "projection_blockers": OUT / "P8_Y5_PARENT_QLOC_2438_PROJECTION_BLOCKER_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2438_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2438_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2438_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2438_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2438_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_constructor": QUEUE / "JR2438_NO_SHADOW_CONSTRUCTOR_SIGNATURE_ATTEMPT_NONCLAIM.csv",
    "queue_bounds": QUEUE / "JR2438_FIRST_REAL_COEFFICIENT_BOUND_ROWS_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "first_real_coupling_bound_rows_nonclaim_2438.csv",
    "beta_docs": BETA_DOCS / "FIRST_REAL_COUPLING_BOUND_ROWS_2438_NONCLAIM.csv",
}

LOCAL_SOURCES = [
    {
        "source_id": "SRC2438_00_2437_handoff",
        "source_path": ROOT / "2437-Y5-R2FR-coupling-sector-Qv-shadow-slot-zero-or-first-real-coefficient-bound-pack.md",
        "needles": ["NEXT2437_0_selected", "CZT2437_5_verdict", "CBP2437_0_delta_w_block", "VAL2437_OVERALL"],
        "role": "fresh handoff selecting constructor signature or first real coefficient acquisition",
    },
    {
        "source_id": "SRC2438_01_2401_shadow_theorem",
        "source_path": ROOT / "2401-Y5-R2FR-source-shadow-functional-exclusion-parent-action-grammar-or-shadow-bound-pack.md",
        "needles": ["SSE2401_3_zero_if_contract_signed", "SBP2401_0_delta_w_shadow", "VAL2401_OVERALL"],
        "role": "conditional no-shadow theorem and shadow bound pack",
    },
    {
        "source_id": "SRC2438_02_2402_finite_basis",
        "source_path": ROOT / "2402-Y5-R2FR-parent-action-normal-form-ownership-signer-or-shadow-coefficient-acquisition.md",
        "needles": ["NFT2402_1_shadow_expansion", "NFT2402_2_zero_condition", "VAL2402_OVERALL"],
        "role": "finite shadow coefficient basis",
    },
    {
        "source_id": "SRC2438_03_2436_live_ledger",
        "source_path": ROOT / "2436-Y5-R2FR-Qv-sector-piece-ledger-or-real-balpha-bg-source-acquisition.md",
        "needles": ["QVSL2436_2_coupling_source_shadow", "BBR2436_4_verdict", "VAL2436_OVERALL"],
        "role": "live Q_v sector map and b_alpha/b_g acquisition readiness",
    },
]

EXTERNAL_SOURCES = [
    {
        "anchor_id": "EXT2438_WEP_MICROSCOPE_TiPt",
        "source_title": "MICROSCOPE mission: final results of the test of the Equivalence Principle",
        "source_url": "https://arxiv.org/abs/2209.15487",
        "doi": "10.1103/PhysRevLett.129.121102",
        "year": "2022",
        "observable": "Eotvos_eta_TiPt",
        "bound_expression": "eta(Ti,Pt)=[-1.5 +/- 2.3(stat) +/- 1.5(syst)]e-15 at 1 sigma",
        "bound_value": "2.7459e-15",
        "bound_value_meaning": "quadrature 1-sigma uncertainty from stat/syst terms; central value retained separately",
        "central_value": "-1.5e-15",
        "units": "dimensionless",
        "confidence": "1_sigma_reported",
        "arena": "WEP",
        "maps_to_symbols": "delta_w_block;delta_w_shadow;b_alpha",
        "extraction_method": "manual_from_arxiv_abstract",
        "source_confidence": "high",
    },
    {
        "anchor_id": "EXT2438_R10_KAPNER_2007",
        "source_title": "Tests of the gravitational inverse-square law below the dark-energy length scale",
        "source_url": "https://pubmed.ncbi.nlm.nih.gov/17358595/",
        "doi": "10.1103/PhysRevLett.98.021101",
        "year": "2007",
        "observable": "Yukawa_alpha_lambda_anchor",
        "bound_expression": "|alpha|<=1 down to lambda=56 microm at 95 percent confidence",
        "bound_value": "1.0",
        "bound_value_meaning": "Yukawa alpha anchor at lambda=56e-6 m",
        "central_value": "0",
        "units": "dimensionless",
        "confidence": "95_percent",
        "arena": "R10",
        "maps_to_symbols": "b_g;delta_w_shadow;c_projector;B_coupling_abs",
        "extraction_method": "manual_from_pubmed_abstract",
        "source_confidence": "high",
    },
    {
        "anchor_id": "EXT2438_R10_TAN_2020",
        "source_title": "Improvement for Testing the Gravitational Inverse-Square Law at the Submillimeter Range",
        "source_url": "https://doi.org/10.1103/PhysRevLett.124.051301",
        "doi": "10.1103/PhysRevLett.124.051301",
        "year": "2020",
        "observable": "Yukawa_alpha_lambda_anchor",
        "bound_expression": "|alpha|<=1 down to lambda=48 microm at 95 percent confidence",
        "bound_value": "1.0",
        "bound_value_meaning": "Yukawa alpha anchor at lambda=48e-6 m",
        "central_value": "0",
        "units": "dimensionless",
        "confidence": "95_percent",
        "arena": "R10",
        "maps_to_symbols": "b_g;delta_w_shadow;c_projector;B_coupling_abs",
        "extraction_method": "manual_from_PRL_DOI_record_and_abstract_snippet",
        "source_confidence": "medium_until_full_curve_digitized",
    },
    {
        "anchor_id": "EXT2438_PPN_CASSINI_GAMMA",
        "source_title": "A test of general relativity using radio links with the Cassini spacecraft",
        "source_url": "https://www.oca.eu/Mignard/Grex/Presentations_pdf/Grex04_B_Bertotti.pdf",
        "doi": "10.1038/nature01997",
        "year": "2003",
        "observable": "PPN_gamma_minus_one",
        "bound_expression": "gamma-1=(2.1 +/- 2.3)e-5 reported in Nature/Cassini summary",
        "bound_value": "2.3e-5",
        "bound_value_meaning": "1-sigma uncertainty on gamma-1; central value retained separately",
        "central_value": "2.1e-5",
        "units": "dimensionless",
        "confidence": "1_sigma_reported",
        "arena": "PPN",
        "maps_to_symbols": "b_g;c_nonHilbert;B_coupling_abs",
        "extraction_method": "manual_from_Cassini_summary_pdf",
        "source_confidence": "medium_high",
    },
    {
        "anchor_id": "EXT2438_CLOCK_ROSENBAND_ALPHA_DOT",
        "source_title": "Frequency ratio of Al+ and Hg+ single-ion optical clocks; metrology at the 17th decimal place",
        "source_url": "https://pubmed.ncbi.nlm.nih.gov/18323415/",
        "doi": "10.1126/science.1154622",
        "year": "2008",
        "observable": "alpha_dot_over_alpha",
        "bound_expression": "alpha_dot/alpha=(-1.6 +/- 2.3)e-17 per year",
        "bound_value": "2.3e-17",
        "bound_value_meaning": "1-sigma uncertainty on local temporal alpha drift",
        "central_value": "-1.6e-17",
        "units": "per_year",
        "confidence": "1_sigma_reported",
        "arena": "clock;EM",
        "maps_to_symbols": "b_alpha",
        "extraction_method": "manual_from_pubmed_abstract",
        "source_confidence": "high",
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
    for source in LOCAL_SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                source_type="local",
                source_path=path,
                source_url="",
                path_exists=path.exists(),
                required_needles="; ".join(needles),
                found_needles="; ".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=source["role"],
            )
        )
    for source in EXTERNAL_SOURCES:
        rows.append(
            base_row(
                source_id=source["anchor_id"],
                source_type="external",
                source_path="",
                source_url=source["source_url"],
                path_exists="n/a",
                required_needles=source["observable"],
                found_needles=source["bound_expression"],
                needles_found=True,
                role=f"{source['arena']} empirical anchor for {source['maps_to_symbols']}",
            )
        )
    return rows


def constructor_signature_rows() -> list[dict[str, Any]]:
    rows = [
        ("NCS2438_0_parent_constructor", "parent constructor inventory", "Conf_parent and S_parent must list only admitted sectors before variation: observed geometry, ordinary Hilbert matter, q/residual sector, allowed boundary/reference, and explicitly named gauge data.", "CONTRACT_READY_NOT_PARENT_SIGNED", "blocks no-shadow promotion"),
        ("NCS2438_1_no_shadow_slot", "no source-shadow constructor", "There is no constructor that forms J_shadow, source-only prefactors, labelled active-source weights, or post-Hilbert source maps after variation.", "NOT_SIGNED", "delta_w_shadow remains live"),
        ("NCS2438_2_no_hidden_visible_targets", "typed coefficient target exclusion", "No Hom from hidden/source/readout labels to alpha, mass, clock, frame, source-weight or finite-range targets except fixed representation labels and one common calibration.", "NOT_SIGNED", "b_alpha, b_g and delta_w_block remain live"),
        ("NCS2438_3_readout_after_variation", "readout no-reentry constructor", "Projectors/worldtubes/readouts are fixed chain maps after variation and cannot feed back into T_active or coefficient definitions.", "NOT_SIGNED", "c_projector remains live"),
        ("NCS2438_4_constructor_verdict", "constructor signature status", "A clean no-shadow constructor would close the coupling sector, but the current corpus does not parent-sign all clauses.", "ZERO_CONSTRUCTOR_NOT_CLOSED", "empirical source anchors are required as nonclaim fallback"),
    ]
    return [
        base_row(
            clause_id=clause_id,
            clause=clause,
            required_signature=signature,
            current_status=status,
            consequence=consequence,
            parent_signed=False,
        )
        for clause_id, clause, signature, status, consequence in rows
    ]


def external_anchor_catalog_rows() -> list[dict[str, Any]]:
    return [base_row(**source, source_backed=True, claim_effect="empirical_anchor_only_not_MTS_projection") for source in EXTERNAL_SOURCES]


def coefficient_bound_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "bound_row_id": "FRCB2438_0_delta_w_block_WEP",
            "symbol": "delta_w_block",
            "anchor_id": "EXT2438_WEP_MICROSCOPE_TiPt",
            "empirical_bound_value": "2.7459e-15",
            "empirical_bound_units": "dimensionless_eta",
            "projection_map": "eta_TiPt = K_WEP_TiPt_block * delta_w_block + K_shadow_TiPt * delta_w_shadow + K_alpha_TiPt * b_alpha + tails_abs",
            "projection_coefficient_status": "MISSING_PARENT_K_VECTOR",
            "no_cancellation_group": "COUPLING_ABS_2438_WEP",
            "source_backed": True,
            "score_ready": False,
            "current_status": "REAL_SOURCE_ANCHOR_READY_MTS_PROJECTION_MISSING",
        },
        {
            "bound_row_id": "FRCB2438_1_b_alpha_clock",
            "symbol": "b_alpha",
            "anchor_id": "EXT2438_CLOCK_ROSENBAND_ALPHA_DOT",
            "empirical_bound_value": "2.3e-17",
            "empirical_bound_units": "per_year",
            "projection_map": "alpha_dot/alpha = K_alpha_clock * b_alpha * qdot_or_local_clock_drive + tails_abs",
            "projection_coefficient_status": "MISSING_PARENT_K_ALPHA_AND_QDOT",
            "no_cancellation_group": "COUPLING_ABS_2438_CLOCK",
            "source_backed": True,
            "score_ready": False,
            "current_status": "REAL_SOURCE_ANCHOR_READY_TIME_DRIVE_PROJECTION_MISSING",
        },
        {
            "bound_row_id": "FRCB2438_2_b_g_PPN",
            "symbol": "b_g",
            "anchor_id": "EXT2438_PPN_CASSINI_GAMMA",
            "empirical_bound_value": "2.3e-5",
            "empirical_bound_units": "dimensionless_gamma_minus_one",
            "projection_map": "gamma_minus_one = K_gamma_bg * b_g + K_gamma_nonHilbert * c_nonHilbert + tails_abs",
            "projection_coefficient_status": "MISSING_PARENT_K_GAMMA_BG",
            "no_cancellation_group": "COUPLING_ABS_2438_PPN",
            "source_backed": True,
            "score_ready": False,
            "current_status": "REAL_SOURCE_ANCHOR_READY_PPN_PROJECTION_MISSING",
        },
        {
            "bound_row_id": "FRCB2438_3_R10_yukawa",
            "symbol": "B_coupling_abs_R10",
            "anchor_id": "EXT2438_R10_TAN_2020;EXT2438_R10_KAPNER_2007",
            "empirical_bound_value": "1.0",
            "empirical_bound_units": "dimensionless_Yukawa_alpha_anchor",
            "projection_map": "alpha_Yukawa(lambda)=K_R10_bg(lambda)*b_g + K_R10_shadow(lambda)*delta_w_shadow + K_R10_projector(lambda)*c_projector + tails_abs",
            "projection_coefficient_status": "MISSING_LAMBDA_DEPENDENT_PARENT_K_VECTOR_AND_FULL_BOUND_CURVE",
            "no_cancellation_group": "COUPLING_ABS_2438_R10",
            "source_backed": True,
            "score_ready": False,
            "current_status": "ANCHOR_ONLY_NON_CURVE_REAL_SOURCE_READY_FULL_R10_PROJECTION_MISSING",
        },
        {
            "bound_row_id": "FRCB2438_4_total_abs",
            "symbol": "B_coupling_abs",
            "anchor_id": "all_EXT2438",
            "empirical_bound_value": "",
            "empirical_bound_units": "mixed",
            "projection_map": "B_coupling_abs=sum_i |K_i component_i| with arena-specific positive terms; no cross-arena cancellation",
            "projection_coefficient_status": "MISSING_ALL_PARENT_K_COMPONENTS",
            "no_cancellation_group": "COUPLING_ABS_2438_TOTAL",
            "source_backed": False,
            "score_ready": False,
            "current_status": "TOTAL_SCHEMA_ONLY",
        },
    ]
    return [base_row(**row) for row in rows]


def projection_blocker_rows() -> list[dict[str, Any]]:
    rows = [
        ("PB2438_0_q_normalization", "q or vertical residual normalization", "same q unit must feed b_alpha, b_g, delta_w and R10/source maps", "MISSING_PARENT_Q_UNIT", "blocks cross-arena scoring"),
        ("PB2438_1_K_vectors", "arena projection coefficients", "K_WEP, K_clock, K_gamma, K_R10(lambda), K_projector must be derived or source-backed", "MISSING_PARENT_K_VECTORS", "real empirical anchors cannot become MTS coefficient bounds"),
        ("PB2438_2_component_basis", "component basis", "delta_w_block, delta_w_shadow, b_alpha, b_g, c_projector and c_nonHilbert must be independent or related by theorem", "MISSING_COMPONENT_INDEPENDENCE_OR_RELATION", "no total envelope score"),
        ("PB2438_3_no_cancellation", "absolute envelope policy", "score sum of nonnegative component projections unless a parent theorem enforces a sign relation", "POLICY_SET_NOT_NUMERIC", "prevents hiding with fitted cancellation"),
        ("PB2438_4_R10_curve", "full R10 bound curve", "anchor-only lambda points are not a full alpha(lambda) curve", "MISSING_DIGITIZED_CURVE_OR_TABLE", "R10 remains smoke/anchor only"),
        ("PB2438_5_constructor", "no-shadow constructor signature", "if parent signs no-shadow/no-target/no-reentry, coefficient rows become theorem-zero instead of bounded", "NOT_SIGNED", "derivation route remains open but not closed"),
    ]
    return [base_row(blocker_id=row_id, blocker=blocker, requirement=req, current_status=status, consequence=effect) for row_id, blocker, req, status, effect in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2438_0_constructor_zero", "no-shadow constructor closes coupling sector", "BLOCKED", "constructor clauses are not parent-signed"),
        ("CG2438_1_source_anchors", "real empirical source anchors exist", "PASS_NONCLAIM", "WEP, R10, PPN and clock anchors are recorded with source URLs"),
        ("CG2438_2_score_ready", "MTS coefficient rows can score", "BLOCKED", "q normalization, projection K vectors, component basis and R10 curve are missing"),
        ("CG2438_3_local_tests", "WEP/R10/PPN/clock pass", "BLOCKED", "anchors are not MTS projections and valid_for_claim remains false"),
        ("CG2438_4_local_GR", "local GR/Newton reduction", "BLOCKED", "coupling/source, Q_v, J_q, boundary, projector and no-hair gates remain upstream"),
    ]
    return [base_row(claim_id=claim_id, claim=claim, gate_status=status, reason=reason, gate_pass=status == "PASS_NONCLAIM") for claim_id, claim, status, reason in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2438_0_constructor", "NO_SHADOW_CONSTRUCTOR_NOT_SIGNED", "the clean zero route remains exact but the corpus does not yet prove the constructor clauses", "do not claim coupling zero"),
        ("DEC2438_1_real_sources", "FIRST_REAL_ANCHORS_ACQUIRED", "MICROSCOPE/WEP, R10/Yukawa, Cassini/PPN and Rosenband/clock anchors are now source-backed in the private ledger", "future runs can stop pretending the bound side is empty"),
        ("DEC2438_2_nonclaim", "ANCHORS_ARE_NOT_MTS_COEFFICIENTS", "empirical bounds constrain only after parent projection maps are derived", "valid_for_claim stays false"),
        ("DEC2438_3_best_next", "BUILD_PROJECTION_MATRIX_NEXT", "the next missing object is K: a map from MTS residual components to WEP/clock/PPN/R10 observables with absolute no-cancellation rules", "select 2439"),
        ("DEC2438_4_public", "NO_GITHUB_ACTION", "private source-acquisition checkpoint only", "continue private framework work"),
    ]
    return [base_row(decision_id=row_id, decision=decision, rationale=rationale, consequence=consequence) for row_id, decision, rationale, consequence in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2438_0_selected",
            selection_status="selected",
            target_file="2439-Y5-R2FR-coupling-projection-matrix-K-vector-and-no-cancellation-envelope.md",
            target_script="scripts/Y5_R2FR_coupling_projection_matrix_K_vector_and_no_cancellation_envelope_2439.py",
            task="derive the projection matrix from delta_w_block, delta_w_shadow, b_alpha, b_g, c_projector and c_nonHilbert into WEP, clock, PPN and R10 anchors, or mark each K coefficient missing with source-ready nonclaim rows",
            acceptance_target="at least one K-vector row has a parent formula or every missing K is explicit; no empirical anchor is treated as an MTS coefficient",
            guardrails="do not fabricate K values, do not cancel residual components, do not promote anchor-only R10 curves, do not claim local GR/R10/PPN/WEP/clock/orbital pass, do not edit formalization-workbench, and do not push GitHub",
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue_constructor", OUTPUTS["constructor_signature"], COPY_TARGETS["queue_constructor"], "no-shadow constructor signature attempt nonclaim queue"),
        ("queue_bounds", OUTPUTS["coefficient_bound_rows"], COPY_TARGETS["queue_bounds"], "first real coefficient bound rows nonclaim queue"),
        ("branch_wep", OUTPUTS["coefficient_bound_rows"], COPY_TARGETS["branch_wep"], "MICROSCOPE/WEP and coupled local bound rows"),
        ("beta_docs", OUTPUTS["external_anchor_catalog"], COPY_TARGETS["beta_docs"], "external anchor catalog for beta docs"),
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
        "*2438-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2438*",
        "*P8_Y5_BRR545_2438*",
        "*JR2438*",
        "*FIRST_REAL_COUPLING_BOUND_ROWS_2438*",
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
    rows.append(base_row(check_id="VAL2438_00_local_sources_exist", status="PASS" if all(row["path_exists"] == True for row in local_sources) else "FAIL", notes="all cited local source paths exist"))
    rows.append(base_row(check_id="VAL2438_01_local_needles", status="PASS" if all(row["needles_found"] == True for row in local_sources) else "FAIL", notes="all cited local source needles are present"))
    rows.append(base_row(check_id="VAL2438_02_external_urls_present", status="PASS" if all(str(row["source_url"]).startswith("http") for row in external_sources) and len(external_sources) >= 4 else "FAIL", notes="external source URLs are present for empirical anchors"))

    anchors = outputs["external_anchor_catalog"]
    rows.append(base_row(check_id="VAL2438_03_real_anchor_values", status="PASS" if all(float(row["bound_value"]) > 0 for row in anchors) else "FAIL", notes="all external anchors have positive numeric bound values"))
    rows.append(base_row(check_id="VAL2438_04_required_arenas_present", status="PASS" if {"WEP", "R10", "PPN"}.issubset({row["arena"] for row in anchors}) and any("clock" in row["arena"] for row in anchors) else "FAIL", notes="WEP, R10, PPN and clock/EM anchors are present"))

    constructor = outputs["constructor_signature"]
    rows.append(base_row(check_id="VAL2438_05_constructor_not_overclaimed", status="PASS" if all(row["parent_signed"] == False for row in constructor) else "FAIL", notes="no no-shadow constructor clause is falsely parent-signed"))

    bounds = outputs["coefficient_bound_rows"]
    source_backed_nonclaim = [row for row in bounds if row["source_backed"] == True and row["valid_for_claim"] == False]
    rows.append(base_row(check_id="VAL2438_06_first_rows_source_backed_nonclaim", status="PASS" if len(source_backed_nonclaim) >= 4 else "FAIL", notes="real source-backed nonclaim bound rows exist for several coupling channels"))
    rows.append(base_row(check_id="VAL2438_07_no_score_ready_rows", status="PASS" if all(row["score_ready"] == False and row["valid_for_claim"] == False for row in bounds) else "FAIL", notes="no coefficient row is score-ready or valid for claim"))
    rows.append(base_row(check_id="VAL2438_08_projection_blockers_present", status="PASS" if len(outputs["projection_blockers"]) >= 5 and any(row["blocker_id"] == "PB2438_1_K_vectors" for row in outputs["projection_blockers"]) else "FAIL", notes="projection blockers include missing K vectors"))

    claims = outputs["claim_gates"]
    rows.append(base_row(check_id="VAL2438_09_claims_blocked_except_source_anchor", status="PASS" if all((row["gate_status"] == "PASS_NONCLAIM") == (row["claim_id"] == "CG2438_1_source_anchors") for row in claims) else "FAIL", notes="only empirical-anchor existence passes, and it is explicitly nonclaim"))
    rows.append(base_row(check_id="VAL2438_10_next_target_written", status="PASS" if outputs["next_target"][0]["target_file"].startswith("2439-") else "FAIL", notes="2439 projection-matrix target selected"))

    hits = formalization_hits()
    rows.append(base_row(check_id="VAL2438_11_no_formalization_artifacts", status="PASS" if not hits else "FAIL", notes="no 2438 artifacts were written to formalization-workbench" if not hits else "formalization-workbench contains 2438 artifacts", detail="; ".join(str(hit) for hit in hits)))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parses(path)
        rows.append(base_row(check_id=f"VAL2438_CSV_{path.stem}", status="PASS" if ok and count > 0 else "FAIL", notes=f"CSV parses with {count} rows" if ok else "CSV parse failed", detail=detail))

    overall_pass = all(row["status"] == "PASS" for row in rows)
    rows.append(base_row(check_id="VAL2438_OVERALL", status="PASS" if overall_pass else "FAIL", notes="2438 refuses no-shadow constructor promotion, acquires real empirical anchors as nonclaim rows, and selects K-vector projection matrix next"))
    return rows


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2438 - Y5/R2FR First Real Coupling Coefficient Bound Source Acquisition Or No-Shadow Constructor Signature",
        "",
        "## Result",
        "- 2438 tries the clean no-shadow constructor route and refuses to sign it without a parent constructor proof.",
        "- It then acquires the first real empirical anchors for the coupling coefficient pack: MICROSCOPE/WEP, short-range Yukawa/R10, Cassini/PPN, and Rosenband clock/alpha.",
        "- These are source-backed empirical bounds, not MTS coefficients.  The missing object is the projection matrix `K` from MTS residual components into observables.",
        "- Therefore the rows are useful but nonclaim: `valid_for_claim=false`, `score_ready=false`, and no local-GR/R10/PPN/WEP/clock pass is made.",
        "- Next target is 2439: derive or explicitly mark missing `K` vectors with no-cancellation envelopes.",
        "",
        "## Source Register",
        table(["source_id", "source_type", "source_path", "source_url", "path_exists", "needles_found", "role"], outputs["source_register"]),
        "",
        "## No-Shadow Constructor Signature Attempt",
        table(["clause_id", "clause", "required_signature", "current_status", "consequence", "parent_signed", "valid_for_claim"], outputs["constructor_signature"]),
        "",
        "## External Bound Anchor Catalog",
        table(["anchor_id", "source_title", "source_url", "doi", "year", "observable", "bound_expression", "bound_value", "units", "confidence", "arena", "maps_to_symbols", "source_backed", "valid_for_claim"], outputs["external_anchor_catalog"]),
        "",
        "## First Real Coefficient Bound Rows",
        table(["bound_row_id", "symbol", "anchor_id", "empirical_bound_value", "empirical_bound_units", "projection_map", "projection_coefficient_status", "no_cancellation_group", "source_backed", "score_ready", "current_status", "valid_for_claim"], outputs["coefficient_bound_rows"]),
        "",
        "## Projection Blocker Ledger",
        table(["blocker_id", "blocker", "requirement", "current_status", "consequence", "valid_for_claim"], outputs["projection_blockers"]),
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
        "constructor_signature": constructor_signature_rows(),
        "external_anchor_catalog": external_anchor_catalog_rows(),
        "coefficient_bound_rows": coefficient_bound_rows(),
        "projection_blockers": projection_blocker_rows(),
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
    overall = next(row for row in outputs["validation"] if row["check_id"] == "VAL2438_OVERALL")
    print(f"VAL2438_OVERALL={overall['status']}")


if __name__ == "__main__":
    main()
