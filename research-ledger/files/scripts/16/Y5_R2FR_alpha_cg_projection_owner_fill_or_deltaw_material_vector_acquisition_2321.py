from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_ALPHA_CG_PROJECTION_OWNER_FILL_2321"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2321-Y5-R2FR-alpha-cg-projection-owner-fill-or-deltaw-material-vector-acquisition.md"

PATHS = {
    "2320_doc": ROOT / "2320-Y5-R2FR-delta-w-material-source-vector-or-PPN-component-owner-row.md",
    "2320_validation": OUT / "P8_Y5_BRR545_2320_VALIDATION.csv",
    "2320_alpha_status": OUT / "P8_Y5_PARENT_QLOC_2320_ALPHA_CG_COMPONENT_STATUS.csv",
    "2320_ppn_import": OUT / "P8_Y5_PARENT_QLOC_2320_PPN_COMPONENT_OWNER_IMPORT.csv",
    "2320_delta_status": OUT / "P8_Y5_PARENT_QLOC_2320_DELTAW_MATERIAL_SOURCE_VECTOR_STATUS.csv",
    "2201_projection": OUT / "P8_Y5_PARENT_QLOC_2201_ALPHA_CG_PROJECTION_GATE.csv",
    "2201_alpha_source": OUT / "P8_Y5_PARENT_QLOC_2201_ALPHA_CG_SOURCE_ROW.csv",
    "2201_matrix": OUT / "P8_Y5_PARENT_QLOC_2201_PPN_COMPONENT_OWNER_MATRIX.csv",
    "2202_projection": OUT / "P8_Y5_PARENT_QLOC_2202_ALPHA_CG_PROJECTION_ATTEMPT.csv",
    "2202_effective": OUT / "P8_Y5_PARENT_QLOC_2202_ALPHA_CG_EFFECTIVE_ROW.csv",
    "1853_norm": OUT / "P8_Y5_PARENT_QLOC_1853_CANONICAL_X_NORMALIZATION_DERIVATION.csv",
    "1853_range": OUT / "P8_Y5_PARENT_QLOC_1853_RANGE_TRANSFER_DERIVATION.csv",
    "1853_gate": OUT / "P8_Y5_PARENT_QLOC_1853_ZX_MX2_INPUT_GATE.csv",
    "1854_extract": OUT / "P8_Y5_PARENT_QLOC_1854_ZX_MX2_EXTRACTION_RESULT.csv",
    "2161_lambda": OUT / "P8_Y5_PARENT_QLOC_2161_NX_LAMBDA_EXTRACTION_ATTEMPT.csv",
    "2161_hessian": OUT / "P8_Y5_PARENT_QLOC_2161_PARENT_HESSIAN_INPUT_AUDIT.csv",
    "2161_vector": OUT / "P8_Y5_PARENT_QLOC_2161_PPN_VECTOR_ENVELOPE.csv",
    "2162_clause": OUT / "P8_Y5_PARENT_QLOC_2162_PARENT_X_ACTION_CLAUSE_ATTEMPT.csv",
    "2162_vector": OUT / "P8_Y5_PARENT_QLOC_2162_PPN_VECTOR_FILL.csv",
    "2319_delta": OUT / "P8_Y5_PARENT_QLOC_2319_DELTA_W_ACQUISITION_STATUS.csv",
    "2319_runner": OUT / "P8_Y5_PARENT_QLOC_2319_SOURCE_BACKED_FINITE_COUPLING_ROWS_NONCLAIM.csv",
}

SOURCES = [
    ("SRC2321_00_2320_doc", "2320_doc", PATHS["2320_doc"], ["NEXT2320_0", "alpha-cg-projection-owner-fill"], "2320 handoff"),
    ("SRC2321_01_2320_validation", "2320_validation", PATHS["2320_validation"], ["VAL2320_OVERALL", "PASS"], "2320 validation"),
    ("SRC2321_02_2320_alpha_status", "2320_alpha_status", PATHS["2320_alpha_status"], ["ACG2320_6_verdict", "ALPHA_CG_COMPONENT_OWNER_IMPORTED_NOT_SCORE_READY"], "current alpha_cg blockers"),
    ("SRC2321_03_2320_ppn_import", "2320_ppn_import", PATHS["2320_ppn_import"], ["PPNI2320_1_alpha_cg_source", "gamma_minus_1"], "alpha_cg source import"),
    ("SRC2321_04_2320_delta_status", "2320_delta_status", PATHS["2320_delta_status"], ["DWV2320_4_verdict", "DEFERRED_TO_ACQUISITION"], "delta_w acquisition status"),
    ("SRC2321_05_2201_projection", "2201_projection", PATHS["2201_projection"], ["ACG2201_6_verdict", "BLOCKED_NONCLAIM_SOURCE_ROW_ONLY"], "original alpha_cg gate"),
    ("SRC2321_06_2201_alpha_source", "2201_alpha_source", PATHS["2201_alpha_source"], ["ACS2201_0_alpha_cg_target", "6.7e-05"], "Cassini source target"),
    ("SRC2321_07_2201_matrix", "2201_matrix", PATHS["2201_matrix"], ["PCM2201_0_alpha_cg", "alpha_cg"], "PPN component matrix"),
    ("SRC2321_08_2202_projection", "2202_projection", PATHS["2202_projection"], ["APA2202_6_verdict", "ALPHA_CG_PROJECTION_NOT_DERIVED"], "projection attempt"),
    ("SRC2321_09_2202_effective", "2202_effective", PATHS["2202_effective"], ["tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X)", "alpha_cg_eff"], "effective alpha formula"),
    ("SRC2321_10_1853_norm", "1853_norm", PATHS["1853_norm"], ["N_X := dXhat/d(varphi/M_Pl)=1/sqrt(Z_X)", "FORMULA_DERIVED_INPUTS_MISSING"], "conditional canonical normalization"),
    ("SRC2321_11_1853_range", "1853_range", PATHS["1853_range"], ["lambda_X = 1/mu_X = sqrt(Z_X/M_X^2)", "TRANSFER_FORMULA_READY"], "conditional range transfer"),
    ("SRC2321_12_1853_gate", "1853_gate", PATHS["1853_gate"], ["MISSING_RANGE_TRANSFER", "FAIL_CURRENT_CLAIM"], "Z_X/M_X2 input gate"),
    ("SRC2321_13_1854_extract", "1854_extract", PATHS["1854_extract"], ["NO_CLAIM_GRADE_ZX_OR_MX2_FOUND", "RELATION_ONLY"], "Z_X/M_X2 extraction result"),
    ("SRC2321_14_2161_lambda", "2161_lambda", PATHS["2161_lambda"], ["NLE2161_6_verdict", "FAIL_CURRENT_CLAIM_NX_LAMBDA_NOT_EXTRACTED"], "N_X/lambda extraction"),
    ("SRC2321_15_2161_hessian", "2161_hessian", PATHS["2161_hessian"], ["PHA2161_5_verdict", "FAIL_PARENT_HESSIAN_INPUTS_STILL_MISSING"], "parent Hessian audit"),
    ("SRC2321_16_2161_vector", "2161_vector", PATHS["2161_vector"], ["PVE2161_0_cg", "MISSING_ZX_TAU_RANGE"], "PPN vector envelope"),
    ("SRC2321_17_2162_clause", "2162_clause", PATHS["2162_clause"], ["PXA2162_6_verdict", "CLOSURE_ONLY"], "parent X action clause attempt"),
    ("SRC2321_18_2162_vector", "2162_vector", PATHS["2162_vector"], ["PVF2162_0_cg", "ACQUISITION_REQUIRED_NONCLAIM"], "PPN vector fill"),
    ("SRC2321_19_2319_delta", "2319_delta", PATHS["2319_delta"], ["DW2319_1_MICROSCOPE", "COMPARATOR_BOUND_EXISTS_PREDICTION_MISSING"], "delta_w anchor"),
    ("SRC2321_20_2319_runner", "2319_runner", PATHS["2319_runner"], ["FCR2319_3_delta_w_missing_prediction", "MISSING_SOURCE_BACKED_VALUE"], "finite-coupling runner"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2321_SOURCE_REGISTER.csv",
    "blockers": OUT / "P8_Y5_PARENT_QLOC_2321_ALPHA_CG_PROJECTION_BLOCKER_AUDIT.csv",
    "conditional": OUT / "P8_Y5_PARENT_QLOC_2321_CONDITIONAL_FILL_ROWS.csv",
    "delta": OUT / "P8_Y5_PARENT_QLOC_2321_DELTAW_MATERIAL_VECTOR_ACQUISITION_LEDGER.csv",
    "readiness": OUT / "P8_Y5_PARENT_QLOC_2321_SCORE_READINESS.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2321_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2321_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2321_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2321_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2321_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2321_0_alpha_blockers", OUTPUTS["blockers"], BETA_DOCS / "ALPHA_CG_PROJECTION_BLOCKER_AUDIT_2321_NONCLAIM.csv"),
    ("COPY2321_1_conditional", OUTPUTS["conditional"], RAB_QUEUE / "JR2321_ALPHA_CG_CONDITIONAL_FILL_NONCLAIM.csv"),
    ("COPY2321_2_delta_acquisition", OUTPUTS["delta"], RAB_QUEUE / "JR2321_DELTAW_MATERIAL_VECTOR_ACQUISITION_NONCLAIM.csv"),
    ("COPY2321_3_score_readiness", OUTPUTS["readiness"], MICRO_RESIDUALS / "alpha_cg_score_readiness_nonclaim_2321.csv"),
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


def build_blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACG2321_0_common_frame",
            "projection_clause": "universal common matter frame",
            "current_status": "NOT_PARENT_SIGNED",
            "fill_attempt": "searched 2201/2202/2162; no parent matter-frame theorem",
            "strongest_result": "none",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACG2321_1_same_branch",
            "projection_clause": "same-branch Xhat owner",
            "current_status": "MISSING_PARENT_OWNER",
            "fill_attempt": "2161/2162 supply closure/action-clause scaffold only",
            "strongest_result": "one-branch owner remains a required parent-action signature",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACG2321_2_ZX",
            "projection_clause": "canonical normalization",
            "current_status": "RELATION_FILLED_VALUE_MISSING",
            "fill_attempt": "imported 1853 exact conditional N_X=1/sqrt(Z_X)",
            "strongest_result": "normalization law fixed; parent-owned positive numeric Z_X still absent",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACG2321_3_lambda_SPPN",
            "projection_clause": "range/screening transfer",
            "current_status": "LAMBDA_RELATION_FILLED_SPPN_MISSING",
            "fill_attempt": "imported 1853 exact conditional lambda_X=sqrt(Z_X/M_X^2)",
            "strongest_result": "range law fixed if Z_X and M_X^2 are owned; Cassini S_PPN geometry map still missing",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACG2321_4_tau_PPN",
            "projection_clause": "PPN projection coefficient",
            "current_status": "MISSING_TAU_PPN",
            "fill_attempt": "searched 1852/1853/2161/2201/2202/2320 current rows",
            "strongest_result": "tau_PPN appears only as a required symbol in the effective alpha object",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACG2321_5_vector_tails",
            "projection_clause": "other PPN vector tails",
            "current_status": "VECTOR_TAILS_UNCONTROLLED",
            "fill_attempt": "2161/2162 vector envelope retained",
            "strongest_result": "disformal, non-Hilbert, support/domain, boundary, and readout tails all remain acquisition rows",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACG2321_6_verdict",
            "projection_clause": "alpha_cg score-ready component",
            "current_status": "NOT_SCORE_READY_BUT_NORMAL_FORM_LOCKED",
            "fill_attempt": "filled exact conditional normal form only",
            "strongest_result": "alpha_cg^PPN normal form is now the only allowed score object; raw c_g remains forbidden",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
    ]


def build_conditional_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CF2321_0_NX",
            "object": "canonical projection factor",
            "conditional_formula": "N_X=dXhat/d(varphi/M_Pl)=1/sqrt(Z_X)",
            "source_path": str(PATHS["1853_norm"]),
            "mathematical_status": "EXACT_IF_PARENT_QUADRATIC_BLOCK_OWNED",
            "missing_for_score": "parent-owned positive Z_X with units and same-branch owner",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CF2321_1_lambda",
            "object": "range",
            "conditional_formula": "lambda_X=sqrt(Z_X/M_X^2)",
            "source_path": str(PATHS["1853_range"]),
            "mathematical_status": "EXACT_IF_PARENT_HESSIAN_ZX_MX2_OWNED",
            "missing_for_score": "parent-owned Z_X, M_X^2, units, sign, and range conversion",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CF2321_2_alpha_cg_normal_form",
            "object": "PPN common conformal component",
            "conditional_formula": "alpha_cg^PPN=tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X)",
            "source_path": str(PATHS["2202_effective"]),
            "mathematical_status": "NORMAL_FORM_LOCKED_NONCLAIM",
            "missing_for_score": "same-branch c_g, Z_X, M_X^2, lambda_X, S_PPN, tau_PPN, common frame, and tail bounds",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CF2321_3_raw_cg_refusal",
            "object": "raw c_g",
            "conditional_formula": "raw c_g is not invariant under Xhat rescaling",
            "source_path": str(PATHS["1853_norm"]),
            "mathematical_status": "FORBIDDEN_SCORE_OBJECT",
            "missing_for_score": "not applicable; use alpha_cg normal form instead",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_delta_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWA2321_0_bound_anchor",
            "needed_object": "delta_w comparator/product anchor",
            "current_evidence": "MICROSCOPE/source product ceiling exists from 1694/2319",
            "missing_input": "MTS material/source prediction vector",
            "next_evidence_needed": "material composition basis and source-current response tensor",
            "status": "ANCHOR_EXISTS_PREDICTION_MISSING",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWA2321_1_material_vector",
            "needed_object": "Ti/Pt or source-test material vector",
            "current_evidence": "2320 marks material tensor missing",
            "missing_input": "species/material basis, charge weights, nuclear/electronic/mass response decomposition",
            "next_evidence_needed": "parent-signed map from coefficient shifts to MICROSCOPE test-mass response",
            "status": "ACQUISITION_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWA2321_2_tau_readout",
            "needed_object": "tau_WEP/readout transfer",
            "current_evidence": "no score-ready tau/readout row",
            "missing_input": "experiment geometry/readout projection and no-cancellation rule",
            "next_evidence_needed": "tau_WEP operator or theorem-zero readout tail",
            "status": "ACQUISITION_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWA2321_3_verdict",
            "needed_object": "delta_w score object",
            "current_evidence": "held as fallback lane",
            "missing_input": "complete material/source vector plus tau/readout transfer",
            "next_evidence_needed": "build after alpha_cg projection normal form has been locked",
            "status": "DEFERRED_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def build_readiness_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "READY2321_0_alpha_normal_form",
            "test_object": "alpha_cg^PPN normal form",
            "progress": "conditional formula locked",
            "remaining_blocker": "same-branch owner, Z_X, M_X^2, S_PPN, tau_PPN, common frame, vector tails",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "READY2321_1_delta_w",
            "test_object": "delta_w material/source vector",
            "progress": "acquisition ledger refreshed",
            "remaining_blocker": "material vector and tau/readout missing",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "READY2321_2_local_GR",
            "test_object": "local GR/Newton recovery",
            "progress": "raw c_g loophole closed by normal-form rule",
            "remaining_blocker": "full no-cancellation PPN residual vector not theorem-zero or numerically bounded",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2321_0_sources",
            "gate": "source paths and needles valid",
            "passed": "true",
            "claim_effect": "audit reproducible",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2321_1_normal_form",
            "gate": "alpha_cg normal form locked",
            "passed": "true",
            "claim_effect": "only conditional score object is allowed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2321_2_alpha_score",
            "gate": "alpha_cg score-ready",
            "passed": "false",
            "claim_effect": "score blocked by missing parent inputs and tail controls",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2321_3_delta_w_score",
            "gate": "delta_w material/source vector score-ready",
            "passed": "false",
            "claim_effect": "delta_w remains acquisition-only",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2321_4_local_GR_Newton",
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
            "row_id": "REF2321_0_raw_cg",
            "claim": "Cassini bounds raw c_g",
            "allowed": "false",
            "reason": "raw c_g changes under Xhat rescaling; the invariant object is tau_PPN*S_PPN*c_g/sqrt(Z_X)",
            "blocking_rows": "CF2321_3_raw_cg_refusal;ACG2321_2_ZX;ACG2321_4_tau_PPN",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2321_1_relation_promotion",
            "claim": "N_X or lambda_X is now numeric",
            "allowed": "false",
            "reason": "2321 imports exact relations only; Z_X and M_X^2 remain missing",
            "blocking_rows": "CF2321_0_NX;CF2321_1_lambda;ACG2321_2_ZX;ACG2321_3_lambda_SPPN",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2321_2_alpha_score",
            "claim": "alpha_cg is score-ready",
            "allowed": "false",
            "reason": "normal form is locked but projection coefficients and vector-tail closure are missing",
            "blocking_rows": "ACG2321_0_common_frame through ACG2321_6_verdict",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2321_3_local_GR",
            "claim": "2321 derives local GR/Newton",
            "allowed": "false",
            "reason": "2321 closes a score-object loophole; it does not complete the full local residual vector",
            "blocking_rows": "READY2321_2_local_GR;CG2321_4_local_GR_Newton",
            "valid_for_claim": "false",
        },
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2321_0",
            "next_target": "2322-Y5-R2FR-tau-PPN-or-common-frame-parent-signature.md",
            "why": "2321 locks the invariant alpha_cg normal form; the least-circular next proof target is either tau_PPN/readout projection from the parent matter frame or the common-frame theorem that makes alpha_cg the actual Cassini leg.",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2321_1",
            "next_target": "2322b-Y5-R2FR-delta-w-material-vector-source-pack.md",
            "why": "fallback/acquisition lane if alpha_cg tau/common-frame proof stalls; build material vector without pretending it is local-GR recovery.",
            "claim_status": "fallback_nonclaim",
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

    add("VAL2321_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists")
    add("VAL2321_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found")
    add("VAL2321_02_normal_form_locked", any(row["row_id"] == "CF2321_2_alpha_cg_normal_form" for row in read_csv_rows(OUTPUTS["conditional"])), "alpha_cg PPN normal form row exists")
    blocker_rows = read_csv_rows(OUTPUTS["blockers"])
    add("VAL2321_03_blockers_preserved", all(row.get("blocks_score") == "true" for row in blocker_rows), "all alpha_cg blockers still block scoring")
    add("VAL2321_04_delta_acquisition", any(row.get("row_id") == "DWA2321_3_verdict" and row.get("status") == "DEFERRED_NONCLAIM" for row in read_csv_rows(OUTPUTS["delta"])), "delta_w remains acquisition-only")
    readiness_rows = read_csv_rows(OUTPUTS["readiness"])
    add("VAL2321_05_readiness_blocks_score", all(row.get("score_ready") == "false" for row in readiness_rows), "all readiness rows remain non-score-ready")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2321_06_claim_gates_block", any(row.get("row_id") == "CG2321_4_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim remains blocked")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2321_07_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks premature claims")
    add("VAL2321_08_next_target", len(read_csv_rows(OUTPUTS["next"])) >= 1, "next target selected")
    add("VAL2321_09_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")
    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2321_10_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))
    formalization_hits = list(FORMALIZATION.rglob("*2321*")) if FORMALIZATION.exists() else []
    add("VAL2321_11_formalization_untouched_by_2321", not formalization_hits, "no 2321 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2321_OVERALL", all(row["status"] == "PASS" for row in rows), "2321 fills only the exact conditional alpha_cg normal form, keeps all projection coefficients nonclaim, preserves delta_w acquisition status, and blocks local-GR/Newton claims.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    blocker_rows: list[dict[str, Any]],
    conditional_rows: list[dict[str, Any]],
    delta_rows: list[dict[str, Any]],
    readiness_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2321 - alpha_cg Projection Owner Fill Or delta_w Material Vector Acquisition

## Summary

2321 makes one real forward move: it locks the only honest PPN score object for the common conformal coupling,
`alpha_cg^PPN = tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X)`, with `N_X=1/sqrt(Z_X)` and
`lambda_X=sqrt(Z_X/M_X^2)` imported as exact conditional relations.

That is not a local-GR win. It is a loophole closure. Raw `c_g` is forbidden, the relation-only quantities are not
numeric inputs, and `alpha_cg` still cannot be scored until the parent branch supplies the common matter frame,
same-branch owner, positive `Z_X`, `M_X^2`, `S_PPN`, `tau_PPN`, and vector-tail control.

`delta_w` remains the fallback acquisition lane: useful comparator anchors exist, but the material/source vector and
tau/readout transfer are still absent.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## alpha_cg Projection Blocker Audit

{markdown_table(blocker_rows, ["row_id", "projection_clause", "current_status", "fill_attempt", "strongest_result", "blocks_score", "valid_for_claim"])}

## Conditional Fill Rows

{markdown_table(conditional_rows, ["row_id", "object", "conditional_formula", "mathematical_status", "missing_for_score", "score_ready", "valid_for_claim"])}

## delta_w Material Vector Acquisition Ledger

{markdown_table(delta_rows, ["row_id", "needed_object", "current_evidence", "missing_input", "next_evidence_needed", "status", "valid_for_claim"])}

## Score Readiness

{markdown_table(readiness_rows, ["row_id", "test_object", "progress", "remaining_blocker", "score_ready", "valid_for_claim"])}

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
        "blockers": build_blocker_rows(),
        "conditional": build_conditional_rows(),
        "delta": build_delta_rows(),
        "readiness": build_readiness_rows(),
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
        rows_by_output["blockers"],
        rows_by_output["conditional"],
        rows_by_output["delta"],
        rows_by_output["readiness"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2321 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
