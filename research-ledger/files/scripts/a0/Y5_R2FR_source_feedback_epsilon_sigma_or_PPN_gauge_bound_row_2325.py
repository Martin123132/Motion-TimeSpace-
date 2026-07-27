from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_SOURCE_FEEDBACK_EPSILON_SIGMA_OR_PPN_GAUGE_BOUND_2325"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2325-Y5-R2FR-source-feedback-epsilon-sigma-or-PPN-gauge-bound-row.md"

PATHS = {
    "2324_doc": ROOT / "2324-Y5-R2FR-readout-tail-zero-proof-or-first-alpha-readout-bound.md",
    "2324_validation": OUT / "P8_Y5_BRR545_2324_VALIDATION.csv",
    "2324_bound": OUT / "P8_Y5_PARENT_QLOC_2324_FIRST_ALPHA_READOUT_BOUND_ROW.csv",
    "2324_acquisition": OUT / "P8_Y5_PARENT_QLOC_2324_READOUT_INPUT_ACQUISITION_LEDGER.csv",
    "2324_zero": OUT / "P8_Y5_PARENT_QLOC_2324_ALPHA_READOUT_ZERO_PROOF_ATTEMPT.csv",
    "2124_chain": OUT / "P8_Y5_PARENT_QLOC_2124_SOURCE_FEEDBACK_CHAIN_RULE.csv",
    "2124_gm": OUT / "P8_Y5_PARENT_QLOC_2124_GM_GUARD_DESCENT_AUDIT.csv",
    "2123_zero": OUT / "P8_Y5_PARENT_QLOC_2123_COMMUTATOR_ZERO_CONDITIONS.csv",
    "2123_pi": OUT / "P8_Y5_PARENT_QLOC_2123_PI_SPLIT_THEOREM.csv",
    "2208_blockers": OUT / "P8_Y5_PARENT_QLOC_2208_PPN_BLOCKER_LEDGER.csv",
    "2208_green": OUT / "P8_Y5_PARENT_QLOC_2208_PPN_GREEN_OPERATOR_LOWERING.csv",
    "2200_source": OUT / "P8_Y5_PARENT_QLOC_2200_PPN_VECTOR_SOURCE_ROW.csv",
    "2200_contract": OUT / "P8_Y5_PARENT_QLOC_2200_PPN_COMPONENT_CONTRACT.csv",
    "2203_gm": OUT / "P8_Y5_PARENT_QLOC_2203_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
}

SOURCES = [
    ("SRC2325_00_2324_doc", "2324_doc", PATHS["2324_doc"], ["NEXT2324_0", "source-feedback-epsilon-sigma"], "2324 handoff"),
    ("SRC2325_01_2324_validation", "2324_validation", PATHS["2324_validation"], ["VAL2324_OVERALL", "PASS"], "2324 validation"),
    ("SRC2325_02_2324_bound", "2324_bound", PATHS["2324_bound"], ["ARB2324_0_source_ceiling", "0.005788015401465051"], "alpha_readout source target"),
    ("SRC2325_03_2324_acquisition", "2324_acquisition", PATHS["2324_acquisition"], ["RIA2324_2_C_feedback", "operator norm and epsilon_sigma_A"], "readout acquisition ledger"),
    ("SRC2325_04_2324_zero", "2324_zero", PATHS["2324_zero"], ["ARZ2324_4_verdict", "NOT_DERIVED_RETAIN_BOUND_ROW"], "readout zero status"),
    ("SRC2325_05_2124_chain", "2124_chain", PATHS["2124_chain"], ["CR2124_3_bound_case", "FINITE_BOUND_NORMAL_FORM_DERIVED"], "feedback chain rule"),
    ("SRC2325_06_2124_gm", "2124_gm", PATHS["2124_gm"], ["GM2124_2_bound_condition", "BOUND_ROUTE_DEFINED_VALUES_MISSING"], "GM guard bound route"),
    ("SRC2325_07_2123_zero", "2123_zero", PATHS["2123_zero"], ["ZC2123_2_fixed_protocol", "CLOSURE_ONLY"], "protocol zero condition"),
    ("SRC2325_08_2123_pi", "2123_pi", PATHS["2123_pi"], ["PIS2123_2_q_descended_projector", "CONDITIONAL_ZERO_VALID"], "projector descent"),
    ("SRC2325_09_2208_blockers", "2208_blockers", PATHS["2208_blockers"], ["PPNB2208_3_PPN_gauge", "MISSING_PPN_GAUGE_TRANSFORM"], "PPN gauge blocker"),
    ("SRC2325_10_2208_green", "2208_green", PATHS["2208_green"], ["PPNL2208_3_source_normalization", "SOURCE_NORMALIZATION_BLOCKER_CONNECTED"], "PPN source normalization"),
    ("SRC2325_11_2200_source", "2200_source", PATHS["2200_source"], ["PVS2200_2_vector_contract", "alpha_PPN_total_abs_vector"], "PPN vector source target"),
    ("SRC2325_12_2200_contract", "2200_contract", PATHS["2200_contract"], ["PCC2200_5_readout", "alpha_readout"], "PPN component contract"),
    ("SRC2325_13_2203_gm", "2203_gm", PATHS["2203_gm"], ["MGV2203_7_calibration_PPN_tail", "MISSING_GAUSS_ORBITAL_PPN_RESIDUAL"], "calibration obstruction"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2325_SOURCE_REGISTER.csv",
    "epsilon": OUT / "P8_Y5_PARENT_QLOC_2325_EPSILON_SIGMA_FEEDBACK_CONTRACT.csv",
    "gauge": OUT / "P8_Y5_PARENT_QLOC_2325_PPN_GAUGE_CALIBRATION_BOUND_ROW.csv",
    "score": OUT / "P8_Y5_PARENT_QLOC_2325_ALPHA_READOUT_SCORE_READINESS.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2325_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2325_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2325_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2325_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2325_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2325_0_epsilon", OUTPUTS["epsilon"], BETA_DOCS / "EPSILON_SIGMA_FEEDBACK_CONTRACT_2325_NONCLAIM.csv"),
    ("COPY2325_1_gauge", OUTPUTS["gauge"], MICRO_RESIDUALS / "ppn_gauge_calibration_bound_row_nonclaim_2325.csv"),
    ("COPY2325_2_score", OUTPUTS["score"], RAB_QUEUE / "JR2325_ALPHA_READOUT_SCORE_READINESS_NONCLAIM.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "missing_needles=" + ";".join(missing)
    return True, "all_needles_found"


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, key, path, needles, role in SOURCES:
        found, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needles": ";".join(needles),
                "needles_found": bool_text(found),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def build_epsilon_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ESC2325_0_definition",
            "object": "epsilon_sigma_A",
            "formula": "epsilon_sigma_A := ||D_v sigma_A|| for the source/readout protocol variables sigma_A",
            "status": "DEFINITION_LOCKED",
            "missing_for_score": "numeric value or theorem-zero descent certificate",
            "zero_condition": "sigma_A=sigma_bar_A(q,e_obs,theta) or fixed external protocol before variation",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ESC2325_1_operator_norm",
            "object": "L_feedback_A",
            "formula": "L_feedback_A := ||D_sigma Pi_A||||J_A|| + ||Pi_A||||D_sigma J_A||",
            "status": "NORMAL_FORM_DERIVED_VALUES_MISSING",
            "missing_for_score": "operator norm/source current norm with units and source path",
            "zero_condition": "L_feedback_A=0 if bracket operator vanishes by type or theorem",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ESC2325_2_feedback_bound",
            "object": "C_feedback_abs",
            "formula": "abs(C_feedback_A) <= L_feedback_A * epsilon_sigma_A",
            "status": "FINITE_BOUND_CONTRACT_READY_VALUES_MISSING",
            "missing_for_score": "L_feedback_A and epsilon_sigma_A values or theorem-zero rows",
            "zero_condition": "epsilon_sigma_A=0 or L_feedback_A=0",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ESC2325_3_verdict",
            "object": "source-feedback part of alpha_readout",
            "formula": "Pi_gamma C_feedback is scoreable only after ESC2325_0 and ESC2325_1 are numeric or zero",
            "status": "NOT_SCORE_READY",
            "missing_for_score": "first concrete protocol-leakage or operator-norm row",
            "zero_condition": "conditional zero not active",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_gauge_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PGB2325_0_source_target",
            "quantity": "PPN_gauge_calibration_readout_tail_target",
            "formula_or_bound": "abs(Pi_gamma[Delta_cal+Delta_PPN]) <= 0.005788015401465051 as a nonclaim target",
            "numeric_value": "0.005788015401465051",
            "units": "dimensionless",
            "source_path": str(PATHS["2200_source"]),
            "source_row_id": "PVS2200_2_vector_contract",
            "status": "SOURCE_BACKED_TARGET_NOT_MTS_PREDICTION",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PGB2325_1_delta_cal",
            "quantity": "Delta_cal",
            "formula_or_bound": "M_eff[Pi_M J_H] - M_Gauss_orbital projected into gamma/readout channel",
            "numeric_value": "MISSING_GAUSS_ORBITAL_PPN_RESIDUAL",
            "units": "dimensionless_or_declared_projection_units",
            "source_path": str(PATHS["2203_gm"]),
            "source_row_id": "MGV2203_7_calibration_PPN_tail",
            "status": "INPUT_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PGB2325_2_delta_ppn",
            "quantity": "Delta_PPN",
            "formula_or_bound": "PPN gauge/source-normalization residual after fixing G_ref and observed source mass",
            "numeric_value": "MISSING_PPN_GAUGE_TRANSFORM_AND_SOURCE_NORMALIZATION",
            "units": "dimensionless_or_declared_projection_units",
            "source_path": str(PATHS["2208_blockers"]),
            "source_row_id": "PPNB2208_2_source_normalization;PPNB2208_3_PPN_gauge",
            "status": "INPUT_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PGB2325_3_bound_contract",
            "quantity": "gauge_calibration_abs_envelope",
            "formula_or_bound": "abs(Pi_gamma Delta_cal)+abs(Pi_gamma Delta_PPN) <= target after same-frame source normalization",
            "numeric_value": "MISSING_TERM_BOUNDS",
            "units": "dimensionless",
            "source_path": str(PATHS["2208_green"]),
            "source_row_id": "PPNL2208_3_source_normalization",
            "status": "BOUND_CONTRACT_READY_VALUES_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_score_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRS2325_0_alpha_readout_envelope",
            "score_object": "alpha_readout_abs_envelope",
            "formula": "abs(alpha_readout) <= abs(Pi_gamma Delta_cal)+abs(Pi_gamma Delta_PPN)+L_feedback*epsilon_sigma+abs(Pi_gamma C_protocol)",
            "current_status": "CONTRACT_READY_VALUES_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRS2325_1_zero_route",
            "score_object": "alpha_readout=0",
            "formula": "Delta_cal=Delta_PPN=C_protocol=0 and epsilon_sigma=0 or L_feedback=0",
            "current_status": "THEOREM_CONDITIONS_NAMED_NOT_SIGNED",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRS2325_2_first_numeric_priority",
            "score_object": "first alpha_readout numeric input",
            "formula": "fill either epsilon_sigma/L_feedback product or Delta_cal/Delta_PPN gauge-calibration envelope",
            "current_status": "NEXT_INPUT_SELECTED",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2325_0_sources",
            "gate": "source paths and needles valid",
            "passed": "true",
            "claim_effect": "audit reproducible",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2325_1_feedback_contract",
            "gate": "source-feedback bound normal form complete",
            "passed": "true",
            "claim_effect": "contract only; no numeric prediction",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2325_2_feedback_score",
            "gate": "C_feedback numerically bounded or theorem-zero",
            "passed": "false",
            "claim_effect": "epsilon_sigma and L_feedback missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2325_3_gauge_score",
            "gate": "PPN gauge/calibration tail numerically bounded or theorem-zero",
            "passed": "false",
            "claim_effect": "Delta_cal and Delta_PPN missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2325_4_local_GR_Newton",
            "gate": "local GR/Newton recovery derived",
            "passed": "false",
            "claim_effect": "still a target, not a result",
            "valid_for_claim": "false",
        },
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2325_0_epsilon_zero",
            "claim": "epsilon_sigma=0 in active branch",
            "allowed": "false",
            "reason": "requires q/e_obs descent or fixed external protocol certificate for the relevant source/readout variables",
            "blocking_rows": "ESC2325_0_definition;ESC2325_3_verdict",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2325_1_feedback_bound_claim",
            "claim": "C_feedback passes the PPN target",
            "allowed": "false",
            "reason": "normal form exists but L_feedback and epsilon_sigma are missing",
            "blocking_rows": "ESC2325_1_operator_norm;ESC2325_2_feedback_bound",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2325_2_gauge_bound_claim",
            "claim": "PPN gauge/calibration tail passes the PPN target",
            "allowed": "false",
            "reason": "Delta_cal and Delta_PPN are missing; source target is not an MTS prediction",
            "blocking_rows": "PGB2325_1_delta_cal;PGB2325_2_delta_ppn;PGB2325_3_bound_contract",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2325_3_local_GR",
            "claim": "2325 derives local GR/Newton",
            "allowed": "false",
            "reason": "2325 makes alpha_readout scoreable in principle, but no live numeric/theorem-zero component closes",
            "blocking_rows": "SRS2325_0_alpha_readout_envelope;CG2325_4_local_GR_Newton",
            "valid_for_claim": "false",
        },
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2325_0",
            "next_target": "2326-Y5-R2FR-epsilon-sigma-zero-certificate-or-first-protocol-leakage-row.md",
            "why": "2325 shows the cleanest next datum is epsilon_sigma: either prove the protocol/support variables descend through q/e_obs, or fill the first finite leakage row.",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2325_1",
            "next_target": "2326b-Y5-R2FR-Delta-cal-PPN-gauge-source-normalization-row.md",
            "why": "parallel route if protocol descent stalls: source Delta_cal/Delta_PPN as a gauge-calibration bound row.",
            "claim_status": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dest in BRANCH_COPY_SPECS:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": relative_path(src),
                "branch_copy_path": str(dest),
                "copy_exists": bool_text(dest.exists()),
                "row_count": str(len(read_csv_rows(dest))),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation_rows(source_rows: list[dict[str, Any]], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths += [Path(row["branch_copy_path"]) for row in branch_copy_rows]
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": "false",
            }
        )

    add("VAL2325_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists")
    add("VAL2325_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found")
    epsilon_rows = read_csv_rows(OUTPUTS["epsilon"])
    add("VAL2325_02_feedback_contract", any(row.get("row_id") == "ESC2325_2_feedback_bound" and "L_feedback_A * epsilon_sigma_A" in row.get("formula", "") for row in epsilon_rows), "feedback finite-bound contract exists")
    gauge_rows = read_csv_rows(OUTPUTS["gauge"])
    add("VAL2325_03_gauge_target", any(row.get("row_id") == "PGB2325_0_source_target" and row.get("numeric_value") == "0.005788015401465051" for row in gauge_rows), "PPN gauge/calibration source target exists")
    add("VAL2325_04_inputs_missing_not_scored", all(row.get("score_ready") == "false" for row in epsilon_rows + gauge_rows), "feedback/gauge rows remain non-score-ready")
    score_rows = read_csv_rows(OUTPUTS["score"])
    add("VAL2325_05_score_rows_nonready", all(row.get("score_ready") == "false" for row in score_rows), "score readiness rows remain non-score-ready")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2325_06_claim_gates_block", any(row.get("row_id") == "CG2325_4_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim remains blocked")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2325_07_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks premature feedback/gauge/local-GR claims")
    add("VAL2325_08_next_target", len(read_csv_rows(OUTPUTS["next"])) >= 1, "next target selected")
    add("VAL2325_09_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")
    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2325_10_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        checkpoint_patterns = ("*P8_Y5*2325*.csv", "*2325-Y5*.md", "*EPSILON_SIGMA*2325*", "*MTS_R2FR_SOURCE_FEEDBACK_EPSILON_SIGMA_OR_PPN_GAUGE_BOUND_2325*")
        for pattern in checkpoint_patterns:
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2325_11_formalization_untouched_by_2325", not formalization_hits, "no 2325 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2325_OVERALL", all(row["status"] == "PASS" for row in rows), "2325 derives the source-feedback finite-bound contract, stages a PPN gauge/calibration source target, keeps all values missing/nonclaim, and blocks local-GR/Newton claims.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    epsilon_rows: list[dict[str, Any]],
    gauge_rows: list[dict[str, Any]],
    score_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2325 - Source Feedback epsilon_sigma Or PPN Gauge Bound Row

## Summary

2325 turns the live readout tail into a sharper quantitative contract. The source-feedback part is now
`abs(C_feedback_A) <= L_feedback_A * epsilon_sigma_A`, where `epsilon_sigma_A=||D_v sigma_A||` measures protocol/support
leakage and `L_feedback_A` is the bracket/operator norm multiplying that leakage.

This gives two clean routes: prove `epsilon_sigma_A=0` by q/e_obs descent or fixed external protocol, or provide a finite
source-backed product bound. In parallel, the PPN gauge/calibration part gets a nonclaim source target from the same
PPN vector ceiling, but `Delta_cal` and `Delta_PPN` remain missing.

No local-GR claim follows. The win is that `alpha_readout` is no longer a vague nuisance; it is now a finite list of
inputs that can be proven zero or bounded.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## epsilon_sigma Feedback Contract

{markdown_table(epsilon_rows, ["row_id", "object", "formula", "status", "missing_for_score", "zero_condition", "score_ready", "valid_for_claim"])}

## PPN Gauge Calibration Bound Row

{markdown_table(gauge_rows, ["row_id", "quantity", "formula_or_bound", "numeric_value", "units", "status", "score_ready", "valid_for_claim"])}

## alpha_readout Score Readiness

{markdown_table(score_rows, ["row_id", "score_object", "formula", "current_status", "score_ready", "valid_for_claim"])}

## Claim Gates

{markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"])}

## Branch Copies

{markdown_table(branch_copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_output = {
        "sources": build_sources(),
        "epsilon": build_epsilon_rows(),
        "gauge": build_gauge_rows(),
        "score": build_score_rows(),
        "claims": build_claim_rows(),
        "refusal": build_refusal_rows(),
        "next": build_next_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(OUTPUTS[key], rows)
    branch_copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], branch_copy_rows)
    validation_rows = build_validation_rows(rows_by_output["sources"], branch_copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_doc(
        rows_by_output["sources"],
        rows_by_output["epsilon"],
        rows_by_output["gauge"],
        rows_by_output["score"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2325 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
