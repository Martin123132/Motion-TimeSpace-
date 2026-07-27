from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
INPUT_DIR = MICROSCOPE / "quarantine" / "1599" / "input"
QUARANTINE = MICROSCOPE / "quarantine" / "1600"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1600-Y5-R2FR-MICROSCOPE-HAR-intake-or-parent-K-vector-proof.md"

SOURCE_FILES = {
    "1599_doc": ROOT / "1599-Y5-R2FR-CMSM-capture-parser-or-symbolic-K-bridge.md",
    "1599_validation": OUT / "P8_Y5_BRR545_1599_VALIDATION.csv",
    "1599_input_inventory": OUT / "P8_Y5_PARENT_QLOC_1599_CMSM_INPUT_INVENTORY.csv",
    "1599_filelist": OUT / "P8_Y5_PARENT_QLOC_1599_CMSM_PARSED_FILELIST_CANDIDATE.csv",
    "1599_symbolic_k": OUT / "P8_Y5_PARENT_QLOC_1599_SYMBOLIC_K_BRIDGE.csv",
    "1599_contract": OUT / "P8_Y5_PARENT_QLOC_1599_CAPTURE_PARSER_CONTRACT.csv",
    "1599_next": OUT / "P8_Y5_PARENT_QLOC_1599_NEXT_TARGET.csv",
    "1598_kernel": OUT / "P8_Y5_PARENT_QLOC_1598_MEASUREMENT_KERNEL_STATUS.csv",
    "1597_countermodel": OUT / "P8_Y5_PARENT_QLOC_1597_NULL_SPACE_COUNTERMODEL.csv",
    "1084_readout": OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
}

NEEDLES = {
    "1599_doc": ["source-intake/microscope/quarantine/1599/input", "SKB1599_3_alignment_object"],
    "1599_validation": ["VAL1599_OVERALL", "PASS"],
    "1599_input_inventory": ["INV1599_0_no_input_files", "NO_CMSM_CAPTURE_OR_FILELIST_INPUT"],
    "1599_filelist": ["PFL1599_0_no_filelist_rows", "NO_PARSEABLE_OFFICIAL_FILELIST"],
    "1599_symbolic_k": ["SKB1599_3_alignment_object", "MISSING_CRITICAL_ALIGNMENT"],
    "1599_contract": ["CPC1599_2_K_extraction", "CONTRACT_WRITTEN"],
    "1599_next": ["1600-Y5-R2FR-MICROSCOPE-HAR-intake-or-parent-K-vector-proof", "ker(K_CMSM)"],
    "1598_kernel": ["MKS1598_1_official_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "1597_countermodel": ["NSC1597_0_linear_space_model", "ker(K)"],
    "1084_readout": ["RIG1084_0_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1600_SOURCE_REGISTER.csv"
HAR_INTAKE_STATUS = OUT / "P8_Y5_PARENT_QLOC_1600_HAR_INTAKE_STATUS.csv"
K_VECTOR_PROOF = OUT / "P8_Y5_PARENT_QLOC_1600_PARENT_K_VECTOR_PROOF_ATTEMPT.csv"
K_COMPONENT_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1600_K_COMPONENT_CONTRACT.csv"
ALIGNMENT_GATE = OUT / "P8_Y5_PARENT_QLOC_1600_ALIGNMENT_GATE.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1600_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1600_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1600_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1600_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1600_VALIDATION.csv"

COPY_TARGETS = {
    HAR_INTAKE_STATUS: [
        QUARANTINE / "HAR_INTAKE_STATUS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_HAR_intake_status_nonclaim_1600.csv",
    ],
    K_VECTOR_PROOF: [
        QUARANTINE / "PARENT_K_VECTOR_PROOF_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_parent_K_vector_proof_attempt_nonclaim_1600.csv",
    ],
    K_COMPONENT_CONTRACT: [
        QUARANTINE / "K_COMPONENT_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_K_component_contract_nonclaim_1600.csv",
    ],
    ALIGNMENT_GATE: [
        QUARANTINE / "ALIGNMENT_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_alignment_gate_nonclaim_1600.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1600.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1600_{index}_{source_id}",
                "source_path": path.relative_to(ROOT).as_posix() if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1600_HAR_intake_or_parent_K_vector_proof_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def har_intake_rows() -> list[dict[str, Any]]:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    files = [path for path in INPUT_DIR.iterdir() if path.is_file()]
    if not files:
        return [
            {
                "same_parent_branch_id": BRANCH_ID,
                "intake_id": "HAR1600_0_input_folder_empty",
                "input_path": INPUT_DIR.relative_to(ROOT).as_posix(),
                "input_type": "none",
                "status": "NO_HAR_JSON_CSV_EVIDENCE_PRESENT",
                "parser_action": "1599 parser is ready but has no file to ingest",
                "filelist_acquired": False,
                "checksums_acquired": False,
                "schema_acquired": False,
                "claim_allowed": False,
            }
        ]
    rows = []
    for index, path in enumerate(sorted(files)):
        supported = path.suffix.lower() in {".har", ".json", ".csv"}
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "intake_id": f"HAR1600_{index}_{path.stem}",
                "input_path": path.relative_to(ROOT).as_posix(),
                "input_type": path.suffix.lower().lstrip(".") or "unknown",
                "status": "SUPPORTED_QUARANTINE_INPUT_REQUIRES_1599_PARSE_REVIEW" if supported else "UNSUPPORTED_INPUT_TYPE",
                "parser_action": "rerun 1599 parser and review candidate rows before any promotion",
                "filelist_acquired": False,
                "checksums_acquired": False,
                "schema_acquired": False,
                "claim_allowed": False,
            }
        )
    return rows


def k_vector_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "KVP1600_0_target_statement",
            "target": "V_MTS not in ker(K_CMSM)",
            "formal_requirement": "prove |<K_CMSM,V_MTS>| >= c_min ||K_CMSM|| ||V_MTS|| with c_min>0",
            "current_status": "TARGET_SHARPENED",
            "result": "PROOF_CONDITION_DEFINED",
            "blocking_gap": "requires either official K_CMSM and V_MTS data or parent theorem fixing their alignment",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "KVP1600_1_EP_template_alignment",
            "target": "MTS source vector overlaps the MICROSCOPE EP-frequency gravity template",
            "formal_requirement": "parent source residual must contain a component proportional to the observed Earth-gravity EP template rather than only common-mode/source-renormalized pieces",
            "current_status": "NOT_PARENT_SIGNED",
            "result": "NO_EP_TEMPLATE_ALIGNMENT_PROOF",
            "blocking_gap": "symbolic EP template exists, but MTS does not yet force nonzero differential projection",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "KVP1600_2_window_nonannihilation",
            "target": "session masks/gaps/calibration do not annihilate the MTS EP component",
            "formal_requirement": "windowing operator W_session has positive response on the relevant branch component",
            "current_status": "MISSING_SESSION_MASKS",
            "result": "NO_WINDOW_NONNULL_PROOF",
            "blocking_gap": "official masks/gaps/calibration arrays absent",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "KVP1600_3_correction_non_cancellation",
            "target": "gravity-gradient/off-centering corrections do not cancel the branch projection",
            "formal_requirement": "signed correction terms are bounded below the EP-template projection or absorbed by reviewed calibration",
            "current_status": "MISSING_SIGNED_CORRECTION_BOUNDS",
            "result": "CANCELLATION_COUNTERMODEL_SURVIVES",
            "blocking_gap": "Sxx/Sxz/off-centering/calibration arrays absent",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "KVP1600_4_verdict",
            "target": "parent K-vector non-null theorem",
            "formal_requirement": "all clauses KVP1600_1 through KVP1600_3 plus material/source nonzero vector",
            "current_status": "PARENT_K_VECTOR_PROOF_NOT_DERIVED",
            "result": "THEOREM_ROUTE_BLOCKED",
            "blocking_gap": "readout-kernel null-space countermodel remains live",
            "claim_allowed": False,
        },
    ]


def k_component_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "KCC1600_0_K_EP",
            "component": "EP gravity template",
            "needed_for": "main nonzero projection",
            "required_inputs": "g_x,g_y,g_z time series or template; a_c11,a_c12,a_c13; attitude/instrument-frame convention",
            "source_anchor": "P8_Y5_PARENT_QLOC_1599_SYMBOLIC_K_BRIDGE.csv:SKB1599_0_EP_signal_template",
            "current_status": "SYMBOLIC_ONLY_NO_ARRAYS",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "KCC1600_1_K_grad",
            "component": "gravity-gradient/off-centering correction",
            "needed_for": "no-cancellation and correction bound",
            "required_inputs": "Sxx,Sxy,Sxz; off-centering vector; calibration/session masks",
            "source_anchor": "P8_Y5_PARENT_QLOC_1599_SYMBOLIC_K_BRIDGE.csv:SKB1599_1_gravity_gradient_terms",
            "current_status": "SYMBOLIC_ONLY_NO_ARRAYS",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "KCC1600_2_W_session",
            "component": "masks/gaps/calibration window",
            "needed_for": "window non-annihilation proof",
            "required_inputs": "session ids; masks; gaps; calibration flags; weighting rule",
            "source_anchor": "P8_Y5_PARENT_QLOC_1599_SYMBOLIC_K_BRIDGE.csv:SKB1599_2_masks_gaps_calibration",
            "current_status": "SYMBOLIC_ONLY_NO_ARRAYS",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "KCC1600_3_V_MTS",
            "component": "branch source-material vector",
            "needed_for": "source side of <K_CMSM,V_MTS>",
            "required_inputs": "Earth/source profile; Ti/Pt material response; parent source-weight convention; uncertainty",
            "source_anchor": "P8_Y5_PARENT_QLOC_1598_ALIGNMENT_IMPORT_REQUIREMENTS.csv:AIR1598_3_source_material_vector",
            "current_status": "MISSING_VECTOR",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "KCC1600_4_c_min",
            "component": "alignment lower bound",
            "needed_for": "tau_min and Delta_w amplitude law",
            "required_inputs": "projection value; K norm; V norm; uncertainty; sign/absolute convention",
            "source_anchor": "P8_Y5_PARENT_QLOC_1599_SYMBOLIC_K_BRIDGE.csv:SKB1599_3_alignment_object",
            "current_status": "MISSING_CRITICAL_ALIGNMENT",
            "claim_allowed": False,
        },
    ]


def alignment_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "ALG1600_0_data_route",
            "route": "official CMSM/HAR data",
            "pass_condition": "reviewed filelist/checksum/schema plus extracted K_CMSM and V_MTS projection",
            "current_status": "NO_HAR_OR_FILELIST_INPUT",
            "gate_result": "FAIL_NO_CLAIM",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "ALG1600_1_parent_route",
            "route": "parent K-vector theorem",
            "pass_condition": "parent action/source geometry forces V_MTS outside ker(K_CMSM) with c_min>0",
            "current_status": "THEOREM_NOT_DERIVED",
            "gate_result": "FAIL_NO_CLAIM",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "ALG1600_2_combined_verdict",
            "route": "alignment gate",
            "pass_condition": "data route or parent route passes",
            "current_status": "BOTH_ROUTES_BLOCKED",
            "gate_result": "ALIGNMENT_REMAINS_MISSING",
            "claim_allowed": False,
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1600_0_HAR",
            "acceptance_rule": "official HAR/JSON/CSV evidence must exist before parser intake can progress",
            "input_state": "1599 input folder empty",
            "runner_result": "NO_HAR_INTAKE",
            "effect": "parser remains ready but unused",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1600_1_K_vector",
            "acceptance_rule": "parent K-vector proof must exclude ker(K_CMSM) and cancellation",
            "input_state": "EP-template, window, correction and source-vector clauses unsigned",
            "runner_result": "REJECT_PARENT_K_VECTOR_PROOF",
            "effect": "null-space countermodel remains",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1600_2_tau_min",
            "acceptance_rule": "tau_min requires data projection or parent theorem",
            "input_state": "alignment missing",
            "runner_result": "REJECT_TAU_MIN_CLAIM",
            "effect": "no WEP/local-GR score",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("CG1600_0_HAR", "official CMSM HAR/filelist ingested", "no input evidence present"),
        ("CG1600_1_K_vector", "parent K-vector non-null theorem", "theorem clauses unsigned"),
        ("CG1600_2_tau", "tau_WEP lower bound exists", "alignment gate failed"),
        ("CG1600_3_WEP", "MTS passes MICROSCOPE/WEP", "product anchor only"),
        ("CG1600_4_local_GR", "derived local GR branch", "coupling/readout residual remains open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": "BLOCKED",
            "reason": reason,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, reason in claims
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1600_0_data_route",
            "decision": "NO_HAR_INTAKE_AVAILABLE",
            "reason": "1599 quarantine input folder contains no official HAR/JSON/CSV filelist evidence",
            "next_action": "capture/download official CMSM evidence or keep data route parked",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1600_1_theory_route",
            "decision": "PARENT_K_VECTOR_PROOF_NOT_DERIVED",
            "reason": "EP-template alignment, window nonannihilation, correction noncancellation and source-vector clauses are unsigned",
            "next_action": "try a narrower EP-template alignment lemma before full K-vector proof",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1600_2_next",
            "decision": "NEXT_1601_EP_TEMPLATE_ALIGNMENT_LEMMA_OR_CMSM_BROWSER_CAPTURE",
            "reason": "the full proof is too broad; next best derivation is the EP-template component only, with data capture as the parallel route",
            "next_action": "derive or reject EP-template alignment lemma; optionally run browser/HAR capture if accessible",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1601-Y5-R2FR-EP-template-alignment-lemma-or-CMSM-browser-capture.md",
            "script": "scripts/Y5_R2FR_EP_template_alignment_lemma_or_CMSM_browser_capture.py",
            "objective": "derive or reject the narrower lemma that the parent MTS source residual has a nonzero MICROSCOPE EP-template component, while keeping CMSM browser/HAR capture as data fallback",
            "success_condition": "parent-signed EP-template alignment clause, or reviewed CMSM/HAR filelist evidence; otherwise alignment remains missing",
            "do_not": "do not claim WEP/local GR, do not use tau_WEP=1, do not promote unreviewed parser rows",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    truthy = {"true", "1", "yes", "y"}
    for path in paths:
        for row in read_csv(path):
            for field in ("score_ready", "valid_prediction_row", "claim_allowed"):
                if row.get(field, "").strip().lower() in truthy:
                    return False
    return True


def no_formalization_1600() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1600*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    har = read_csv(HAR_INTAKE_STATUS)
    proof = read_csv(K_VECTOR_PROOF)
    components = read_csv(K_COMPONENT_CONTRACT)
    alignment = read_csv(ALIGNMENT_GATE)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1600_0_sources_exist", all(row["exists"] == "True" or row["exists"] is True for row in sources), "all cited 1600 local source paths exist"),
        ("VAL1600_1_needles_found", all(row["needle_found"] == "True" or row["needle_found"] is True for row in sources), "all required 1600 source needles found"),
        ("VAL1600_2_no_HAR_input", any(row["intake_id"] == "HAR1600_0_input_folder_empty" for row in har), "HAR/filelist input absence recorded"),
        ("VAL1600_3_K_vector_target", any(row["proof_id"] == "KVP1600_0_target_statement" and "c_min>0" in row["formal_requirement"] for row in proof), "K-vector target theorem sharpened"),
        ("VAL1600_4_K_vector_blocked", any(row["proof_id"] == "KVP1600_4_verdict" and row["result"] == "THEOREM_ROUTE_BLOCKED" for row in proof), "parent K-vector proof blocked"),
        ("VAL1600_5_components_named", len(components) >= 5 and any(row["component_id"] == "KCC1600_4_c_min" for row in components), "K components and c_min contract named"),
        ("VAL1600_6_alignment_gate_blocked", any(row["gate_id"] == "ALG1600_2_combined_verdict" and row["gate_result"] == "ALIGNMENT_REMAINS_MISSING" for row in alignment), "alignment gate remains missing"),
        ("VAL1600_7_runner_blocks_tau", any(row["runner_id"] == "RUN1600_2_tau_min" and row["runner_result"] == "REJECT_TAU_MIN_CLAIM" for row in runner), "runner rejects tau_min claim"),
        ("VAL1600_8_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" for row in gates), "all 1600 claim gates remain closed"),
        ("VAL1600_9_decision_next", any(row["decision"] == "NEXT_1601_EP_TEMPLATE_ALIGNMENT_LEMMA_OR_CMSM_BROWSER_CAPTURE" for row in decisions), "decision selects 1601 EP-template alignment or CMSM capture"),
        ("VAL1600_10_csv_parse", csv_parses(generated_csvs), "all generated 1600 CSVs parse"),
        ("VAL1600_11_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1600 rows are score-ready, prediction rows, or claim-allowed"),
        ("VAL1600_12_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1600_13_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1600_14_formalization_untouched", no_formalization_1600(), "no 1600 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1600_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1600 MICROSCOPE HAR intake or parent K-vector proof validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    har: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    components: list[dict[str, Any]],
    alignment: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1600 - R2/fR MICROSCOPE HAR Intake Or Parent K-Vector Proof",
                "## Verdict\n"
                "- 1600 finds no official CMSM HAR/JSON/CSV evidence in the `1599/input` quarantine folder, so no filelist or `K_CMSM` import occurs.\n"
                "- The parent `K`-vector proof target is now exact: prove `|<K_CMSM,V_MTS>| >= c_min ||K_CMSM|| ||V_MTS||` with `c_min>0`.\n"
                "- That proof does not close: EP-template alignment, session-window nonannihilation, correction noncancellation, and source/material vector clauses are still unsigned.\n"
                "- Best next derivation is narrower: attack the EP-template alignment lemma first, while keeping CMSM browser/HAR capture as the data fallback.\n"
                "- No WEP, local-GR, Newton, PPN, R10, clock, orbital, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## HAR Intake Status",
                md_table(har, ["intake_id", "input_path", "input_type", "status", "parser_action"]),
                "## Parent K-Vector Proof Attempt",
                md_table(proof, ["proof_id", "target", "formal_requirement", "current_status", "result", "blocking_gap"]),
                "## K Component Contract",
                md_table(components, ["component_id", "component", "needed_for", "required_inputs", "current_status"]),
                "## Alignment Gate",
                md_table(alignment, ["gate_id", "route", "pass_condition", "current_status", "gate_result"]),
                "## Runner Refusal",
                md_table(runner, ["runner_id", "acceptance_rule", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    har = har_intake_rows()
    proof = k_vector_proof_rows()
    components = k_component_rows()
    alignment = alignment_gate_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        HAR_INTAKE_STATUS,
        K_VECTOR_PROOF,
        K_COMPONENT_CONTRACT,
        ALIGNMENT_GATE,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(HAR_INTAKE_STATUS, har)
    write_csv(K_VECTOR_PROOF, proof)
    write_csv(K_COMPONENT_CONTRACT, components)
    write_csv(ALIGNMENT_GATE, alignment)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, har, proof, components, alignment, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
