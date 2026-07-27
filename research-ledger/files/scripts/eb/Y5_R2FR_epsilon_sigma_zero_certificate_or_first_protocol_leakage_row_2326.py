from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_EPSILON_SIGMA_ZERO_OR_PROTOCOL_LEAKAGE_2326"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2326-Y5-R2FR-epsilon-sigma-zero-certificate-or-first-protocol-leakage-row.md"

PATHS = {
    "2325_doc": ROOT / "2325-Y5-R2FR-source-feedback-epsilon-sigma-or-PPN-gauge-bound-row.md",
    "2325_validation": OUT / "P8_Y5_BRR545_2325_VALIDATION.csv",
    "2325_epsilon": OUT / "P8_Y5_PARENT_QLOC_2325_EPSILON_SIGMA_FEEDBACK_CONTRACT.csv",
    "2325_score": OUT / "P8_Y5_PARENT_QLOC_2325_ALPHA_READOUT_SCORE_READINESS.csv",
    "2124_protocol": OUT / "P8_Y5_PARENT_QLOC_2124_PROTOCOL_VARIABLE_NORMAL_FORM.csv",
    "2124_schema": OUT / "P8_Y5_PARENT_QLOC_2124_FIRST_BOUNDED_ROW_SCHEMA.csv",
    "2124_chain": OUT / "P8_Y5_PARENT_QLOC_2124_SOURCE_FEEDBACK_CHAIN_RULE.csv",
    "2124_gm": OUT / "P8_Y5_PARENT_QLOC_2124_GM_GUARD_DESCENT_AUDIT.csv",
    "2123_finite": OUT / "P8_Y5_PARENT_QLOC_2123_FINITE_KERNEL_BOUND_ROWS.csv",
    "2123_zero": OUT / "P8_Y5_PARENT_QLOC_2123_COMMUTATOR_ZERO_CONDITIONS.csv",
    "2123_pi": OUT / "P8_Y5_PARENT_QLOC_2123_PI_SPLIT_THEOREM.csv",
    "1701_comm": OUT / "P8_Y5_PARENT_QLOC_1701_READOUT_COMMUTATOR_AUDIT.csv",
    "1701_queue": OUT / "P8_Y5_PARENT_QLOC_1701_READOUT_RESIDUAL_QUEUE.csv",
    "1898_attempt": OUT / "P8_Y5_PARENT_QLOC_1898_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv",
    "1900_point": OUT / "P8_Y5_PARENT_QLOC_1900_WEP_SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_ATTEMPT.csv",
    "1900_residual": OUT / "P8_Y5_PARENT_QLOC_1900_WEP_POINT_SOURCE_RESIDUAL_LEDGER_NONCLAIM.csv",
    "2200_source": OUT / "P8_Y5_PARENT_QLOC_2200_PPN_VECTOR_SOURCE_ROW.csv",
}

SOURCES = [
    ("SRC2326_00_2325_doc", "2325_doc", PATHS["2325_doc"], ["NEXT2325_0", "epsilon-sigma-zero-certificate"], "2325 handoff"),
    ("SRC2326_01_2325_validation", "2325_validation", PATHS["2325_validation"], ["VAL2325_OVERALL", "PASS"], "2325 validation"),
    ("SRC2326_02_2325_epsilon", "2325_epsilon", PATHS["2325_epsilon"], ["ESC2325_2_feedback_bound", "L_feedback_A * epsilon_sigma_A"], "epsilon sigma contract"),
    ("SRC2326_03_2325_score", "2325_score", PATHS["2325_score"], ["SRS2325_0_alpha_readout_envelope", "CONTRACT_READY_VALUES_MISSING"], "alpha_readout score readiness"),
    ("SRC2326_04_2124_protocol", "2124_protocol", PATHS["2124_protocol"], ["SIG2124_0_source_profile", "SIG2124_1_GM_calibration"], "protocol variable split"),
    ("SRC2326_05_2124_schema", "2124_schema", PATHS["2124_schema"], ["FK2124_0_source_GM", "epsilon_sigma_source_GM"], "first bounded row schema"),
    ("SRC2326_06_2124_chain", "2124_chain", PATHS["2124_chain"], ["CR2124_3_bound_case", "FINITE_BOUND_NORMAL_FORM_DERIVED"], "feedback chain rule"),
    ("SRC2326_07_2124_gm", "2124_gm", PATHS["2124_gm"], ["GM2124_3_verdict", "GUARD_NORMAL_FORM_CLOSED_DATA_OPEN"], "GM guard"),
    ("SRC2326_08_2123_finite", "2123_finite", PATHS["2123_finite"], ["FK2123_0_source_support", "FINITE_KERNEL_SHAPE_ONLY"], "finite source support kernel"),
    ("SRC2326_09_2123_zero", "2123_zero", PATHS["2123_zero"], ["ZC2123_2_fixed_protocol", "CLOSURE_ONLY"], "protocol zero condition"),
    ("SRC2326_10_2123_pi", "2123_pi", PATHS["2123_pi"], ["PIS2123_2_q_descended_projector", "CONDITIONAL_ZERO_VALID"], "projector descent"),
    ("SRC2326_11_1701_comm", "1701_comm", PATHS["1701_comm"], ["RC1701_2_projection_operator", "retained_residual"], "readout commutator audit"),
    ("SRC2326_12_1701_queue", "1701_queue", PATHS["1701_queue"], ["RQ1701_1_I_commutator", "retained_nonclaim"], "readout residual queue"),
    ("SRC2326_13_1898_attempt", "1898_attempt", PATHS["1898_attempt"], ["RVC1898_2_projection_commutator_survives", "COUNTERMODEL_ACTIVE"], "readout commutator attempt"),
    ("SRC2326_14_1900_point", "1900_point", PATHS["1900_point"], ["PSR1900_6_verdict", "SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_NOT_PARENT_DERIVED"], "source worldtube point-source attempt"),
    ("SRC2326_15_1900_residual", "1900_residual", PATHS["1900_residual"], ["PSE1900_6_verdict", "POINT_SOURCE_RESIDUAL_PACK_NOT_EXECUTABLE_NONCLAIM"], "point-source residual ledger"),
    ("SRC2326_16_2200_source", "2200_source", PATHS["2200_source"], ["PVS2200_2_vector_contract", "0.005788015401465051"], "PPN source target"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2326_SOURCE_REGISTER.csv",
    "zero": OUT / "P8_Y5_PARENT_QLOC_2326_EPSILON_SIGMA_ZERO_CERTIFICATE_ATTEMPT.csv",
    "leakage": OUT / "P8_Y5_PARENT_QLOC_2326_FIRST_PROTOCOL_LEAKAGE_ROW.csv",
    "inputs": OUT / "P8_Y5_PARENT_QLOC_2326_PROTOCOL_INPUT_REQUIREMENTS.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2326_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2326_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2326_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2326_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2326_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2326_0_zero", OUTPUTS["zero"], BETA_DOCS / "EPSILON_SIGMA_ZERO_CERTIFICATE_ATTEMPT_2326_NONCLAIM.csv"),
    ("COPY2326_1_leakage", OUTPUTS["leakage"], MICRO_RESIDUALS / "first_protocol_leakage_row_nonclaim_2326.csv"),
    ("COPY2326_2_inputs", OUTPUTS["inputs"], RAB_QUEUE / "JR2326_PROTOCOL_INPUT_REQUIREMENTS_NONCLAIM.csv"),
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


def build_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ESZ2326_0_exact_zero_condition",
            "sigma_channel": "generic protocol/support variables",
            "zero_statement": "epsilon_sigma_A=||D_v sigma_A||=0 if sigma_A=sigma_bar_A(q,e_obs,theta) or sigma_A is fixed external protocol before variation.",
            "proof_status": "EXACT_CONDITIONAL_ZERO",
            "active_branch_status": "UNSIGNED_FOR_SOURCE_FEEDBACK",
            "missing_certificate": "q/e_obs descent certificate or fixed-protocol parent declaration for each sigma_A",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ESZ2326_1_source_profile",
            "sigma_channel": "sigma_source_profile",
            "zero_statement": "Earth/source density, composition, support profile, and source worldtube are fixed q/e_obs data before readout.",
            "proof_status": "NOT_PARENT_SIGNED",
            "active_branch_status": "SOURCE_PROFILE_AND_COMPOSITION_OBSTRUCTION_ACTIVE",
            "missing_certificate": "profile weighting, source composition basis, support map, and same-frame source pullback",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ESZ2326_2_GM_common_mode",
            "sigma_channel": "sigma_GM_common_mode",
            "zero_statement": "GM/G calibration contains only one universal common-mode source factor; no relative source vector is absorbed.",
            "proof_status": "GUARD_WRITTEN_NOT_NUMERIC",
            "active_branch_status": "CALIBRATION_EQUATION_MISSING",
            "missing_certificate": "calibration equation and no-relative-source-hiding proof",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ESZ2326_3_mask_orbit_boundary",
            "sigma_channel": "sigma_mask_orbit_attitude + sigma_boundary_domain",
            "zero_statement": "masks, orbit windows, attitude, support tube, boundary transport, and projector domain are fixed protocol or q/e_obs descendants.",
            "proof_status": "CLOSURE_OR_SOURCE_REQUIRED",
            "active_branch_status": "OFFICIAL_ARRAYS_AND_BOUNDARY_CERTIFICATES_MISSING",
            "missing_certificate": "official arrays/protocol source plus boundary/domain descent or finite bound",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ESZ2326_4_verdict",
            "sigma_channel": "epsilon_sigma active zero",
            "zero_statement": "all sigma channels required by alpha_readout have epsilon_sigma_A=0",
            "proof_status": "NOT_DERIVED_RETAIN_LEAKAGE_ROW",
            "active_branch_status": "first leakage row required",
            "missing_certificate": "at least source_GM channel remains unsigned",
            "valid_for_claim": "false",
        },
    ]


def build_leakage_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PLR2326_0_source_GM",
            "leakage_row": "first protocol leakage row",
            "epsilon_symbol": "epsilon_sigma_source_GM",
            "protocol_variables": "sigma_source_profile; sigma_GM_common_mode",
            "bound_contract": "|C_source_GM| <= L_source_GM * epsilon_sigma_source_GM",
            "lipschitz_factor": "L_source_GM = ||D_sigma Pi_source||||J_source|| + ||Pi_source||||D_sigma J_source||",
            "target": "feeds alpha_readout and source-normalization part of PPN/local-GR vector",
            "source_basis": "FK2124_0_source_GM;FK2123_0_source_support",
            "current_status": "CONTRACT_READY_VALUES_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PLR2326_1_target_budget",
            "leakage_row": "nonclaim target budget",
            "epsilon_symbol": "epsilon_sigma_source_GM",
            "protocol_variables": "same-frame source profile and common-mode GM calibration",
            "bound_contract": "abs(Pi_gamma C_source_GM) must fit inside alpha_readout_abs_target <= 0.005788015401465051",
            "lipschitz_factor": "requires Pi_gamma and L_source_GM in common dimensionless PPN units",
            "target": "PVS2200_2_vector_contract",
            "source_basis": "P8_Y5_PARENT_QLOC_2200_PPN_VECTOR_SOURCE_ROW.csv",
            "current_status": "SOURCE_TARGET_ONLY_NOT_PREDICTION",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PLR2326_2_no_point_source_shortcut",
            "leakage_row": "point-source shortcut guard",
            "epsilon_symbol": "epsilon_sigma_source_GM",
            "protocol_variables": "source worldtube/profile/composition",
            "bound_contract": "common monopole can be used only for universal source factor; relative/source-profile residuals stay explicit",
            "lipschitz_factor": "not applicable",
            "target": "prevents measured-GM hiding",
            "source_basis": "PSR1900_2_no_relative_hiding;PSE1900_6_verdict",
            "current_status": "GUARD_ACTIVE_RESIDUAL_PACK_NOT_EXECUTABLE",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PIR2326_0_profile",
            "needed_input": "source profile/composition",
            "meaning": "orbit/worldtube-weighted source density, composition, and support variables entering sigma_source_profile",
            "current_status": "MISSING_SOURCE_VECTOR_OR_PROFILE_WEIGHTING",
            "source_basis": "SIG2124_0_source_profile;PSR1900_3_source_composition_obstruction",
            "next_evidence": "parent universality theorem or source-backed profile/composition vector",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PIR2326_1_GM_calibration",
            "needed_input": "GM calibration equation",
            "meaning": "equation showing fitted GM absorbs only common-mode source factor",
            "current_status": "GUARD_WRITTEN_NOT_NUMERIC",
            "source_basis": "SIG2124_1_GM_calibration;GM2124_0_common_mode_rule",
            "next_evidence": "calibration equation plus no-relative-source-hiding proof",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PIR2326_2_L_source_GM",
            "needed_input": "L_source_GM",
            "meaning": "operator/source-current Lipschitz factor multiplying protocol leakage",
            "current_status": "MISSING_OPERATOR_NORM_AND_SOURCE_CURRENT_NORM",
            "source_basis": "FK2124_0_source_GM;CR2124_3_bound_case",
            "next_evidence": "norm convention, units, source path, and projection to Pi_gamma",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PIR2326_3_same_frame",
            "needed_input": "same-frame source pullback",
            "meaning": "one observed coframe/time generator for force law, source variation, clocks, orbit, and eta/PPN readout",
            "current_status": "SAME_FRAME_SOURCE_PULLBACK_NOT_DERIVED",
            "source_basis": "PSR1900_5_same_frame_obstruction",
            "next_evidence": "same-frame parent certificate or explicit frame residual",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2326_0_sources",
            "gate": "source paths and needles valid",
            "passed": "true",
            "claim_effect": "audit reproducible",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2326_1_epsilon_zero_contract",
            "gate": "epsilon_sigma zero condition exact conditionally",
            "passed": "true",
            "claim_effect": "zero theorem shape exists",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2326_2_active_epsilon_zero",
            "gate": "epsilon_sigma_source_GM=0 in active branch",
            "passed": "false",
            "claim_effect": "profile/GM/source certificates missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2326_3_leakage_score",
            "gate": "first source_GM leakage row score-ready",
            "passed": "false",
            "claim_effect": "L_source_GM and epsilon_sigma_source_GM missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2326_4_local_GR_Newton",
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
            "row_id": "REF2326_0_zero_promotion",
            "claim": "epsilon_sigma_source_GM=0 now",
            "allowed": "false",
            "reason": "source profile/composition, GM calibration, and same-frame source pullback certificates are missing",
            "blocking_rows": "ESZ2326_1_source_profile;ESZ2326_2_GM_common_mode;PIR2326_3_same_frame",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2326_1_leakage_bound_claim",
            "claim": "source_GM protocol leakage is bounded below PPN target",
            "allowed": "false",
            "reason": "contract exists but L_source_GM and epsilon_sigma_source_GM values are missing",
            "blocking_rows": "PLR2326_0_source_GM;PIR2326_2_L_source_GM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2326_2_point_source_shortcut",
            "claim": "point-source/common monopole removes the source_GM protocol tail",
            "allowed": "false",
            "reason": "common monopole is conditional only and cannot hide relative source/profile residuals",
            "blocking_rows": "PLR2326_2_no_point_source_shortcut;PIR2326_0_profile",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2326_3_local_GR",
            "claim": "2326 derives local GR/Newton",
            "allowed": "false",
            "reason": "2326 names the first leakage channel but does not close or score the full PPN vector",
            "blocking_rows": "CG2326_4_local_GR_Newton;PLR2326_0_source_GM",
            "valid_for_claim": "false",
        },
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2326_0",
            "next_target": "2327-Y5-R2FR-source-GM-profile-universality-or-LsourceGM-bound.md",
            "why": "2326 selects source_GM as the first protocol leakage row; next either prove source profile/GM universality or fill L_source_GM and epsilon_sigma_source_GM as finite inputs.",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2326_1",
            "next_target": "2327b-Y5-R2FR-same-frame-source-pullback-certificate.md",
            "why": "parallel theorem route: same-frame pullback would zero a large class of protocol leakage without numeric fitting.",
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

    add("VAL2326_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists")
    add("VAL2326_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found")
    zero_rows = read_csv_rows(OUTPUTS["zero"])
    add("VAL2326_02_zero_condition", any(row.get("row_id") == "ESZ2326_0_exact_zero_condition" and row.get("proof_status") == "EXACT_CONDITIONAL_ZERO" for row in zero_rows), "epsilon_sigma conditional zero row exists")
    add("VAL2326_03_active_zero_blocked", any(row.get("row_id") == "ESZ2326_4_verdict" and row.get("proof_status") == "NOT_DERIVED_RETAIN_LEAKAGE_ROW" for row in zero_rows), "active epsilon zero not promoted")
    leakage_rows = read_csv_rows(OUTPUTS["leakage"])
    add("VAL2326_04_leakage_row", any(row.get("row_id") == "PLR2326_0_source_GM" and "L_source_GM * epsilon_sigma_source_GM" in row.get("bound_contract", "") for row in leakage_rows), "first source_GM leakage row exists")
    add("VAL2326_05_leakage_nonready", all(row.get("score_ready") == "false" for row in leakage_rows), "leakage rows remain non-score-ready")
    input_rows = read_csv_rows(OUTPUTS["inputs"])
    add("VAL2326_06_input_requirements", len(input_rows) >= 4, "protocol input requirements listed")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2326_07_claim_gates_block", any(row.get("row_id") == "CG2326_4_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim remains blocked")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2326_08_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks premature epsilon/leakage/local-GR claims")
    add("VAL2326_09_next_target", len(read_csv_rows(OUTPUTS["next"])) >= 1, "next target selected")
    add("VAL2326_10_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")
    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2326_11_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        checkpoint_patterns = ("*P8_Y5*2326*.csv", "*2326-Y5*.md", "*EPSILON_SIGMA*2326*", "*MTS_R2FR_EPSILON_SIGMA_ZERO_OR_PROTOCOL_LEAKAGE_2326*")
        for pattern in checkpoint_patterns:
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2326_12_formalization_untouched_by_2326", not formalization_hits, "no 2326 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2326_OVERALL", all(row["status"] == "PASS" for row in rows), "2326 keeps epsilon_sigma zero conditional, creates the first source_GM protocol leakage row, leaves values missing/nonclaim, and blocks local-GR/Newton claims.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    leakage_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2326 - epsilon_sigma Zero Certificate Or First Protocol Leakage Row

## Summary

2326 attacks the first live `epsilon_sigma` channel directly. The exact zero theorem remains simple:
`epsilon_sigma_A=0` if the protocol/support variables `sigma_A` descend through `(q,e_obs,theta)` or are fixed external
protocol before variation.

The active branch cannot claim that yet. The source profile, source composition, same-frame pullback, and GM calibration
equation are still unsigned. So 2326 promotes the first finite leakage row:
`|C_source_GM| <= L_source_GM * epsilon_sigma_source_GM`.

This is the right kind of progress. The readout tail is no longer a fog bank; it now has a first concrete leakage channel
with named inputs.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## epsilon_sigma Zero Certificate Attempt

{markdown_table(zero_rows, ["row_id", "sigma_channel", "zero_statement", "proof_status", "active_branch_status", "missing_certificate", "valid_for_claim"])}

## First Protocol Leakage Row

{markdown_table(leakage_rows, ["row_id", "leakage_row", "epsilon_symbol", "protocol_variables", "bound_contract", "current_status", "score_ready", "valid_for_claim"])}

## Protocol Input Requirements

{markdown_table(input_rows, ["row_id", "needed_input", "meaning", "current_status", "source_basis", "next_evidence", "valid_for_claim"])}

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
        "zero": build_zero_rows(),
        "leakage": build_leakage_rows(),
        "inputs": build_input_rows(),
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
        rows_by_output["zero"],
        rows_by_output["leakage"],
        rows_by_output["inputs"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2326 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
