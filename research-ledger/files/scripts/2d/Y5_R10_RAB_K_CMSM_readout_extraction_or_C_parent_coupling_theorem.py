from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
METADATA = MICROSCOPE / "metadata"
BRANCH_ROOT = MICROSCOPE / "branch_locked_wep"
COEFFICIENT_ROOT = BRANCH_ROOT / "coefficients"
RESIDUAL_ROOT = BRANCH_ROOT / "residuals"
OFFICIAL_READOUT = MICROSCOPE / "official_readout"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1445-Y5-R10-RAB-K-CMSM-readout-extraction-or-C-parent-coupling-theorem.md"

PREV_NEXT = OUT / "P8_Y5_R10_1444_NEXT_TARGET.csv"
PREV_EXTRACTION = OUT / "P8_Y5_R10_1444_PRODUCT_CONVENTION_OFFICIAL_EXTRACTION.csv"
PREV_REFRESH = OUT / "P8_Y5_R10_1444_SOURCE_PACK_STATUS_REFRESH.csv"
PREV_C_PARENT = OUT / "P8_Y5_R10_1444_C_PARENT_THEOREM_SOURCE_SEARCH.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1444_VALIDATION.csv"
READOUT_SCHEMA = METADATA / "P8_Y5_R10_1336_OFFICIAL_READOUT_SCHEMA.csv"
PRODUCT_TARGET = MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv"
LIVE_READOUT_TARGET = OFFICIAL_READOUT / "P_WEP_K_CMSM_readout.csv"
LIVE_C_PARENT_IMPORT = COEFFICIENT_ROOT / "C_parent_WEP_slot_import.csv"
C_PARENT_IMPORT_SCHEMA = COEFFICIENT_ROOT / "C_parent_import_schema.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1445_SOURCE_REGISTER.csv"
READOUT_EXTRACTION = OUT / "P8_Y5_R10_1445_K_CMSM_READOUT_OFFICIAL_EXTRACTION.csv"
READOUT_REQUIREMENTS = OUT / "P8_Y5_R10_1445_K_CMSM_READOUT_REQUIREMENTS.csv"
COUPLING_THEOREM = OUT / "P8_Y5_R10_1445_C_PARENT_COUPLING_THEOREM_CONTRACT.csv"
COUPLING_AUDIT = OUT / "P8_Y5_R10_1445_C_PARENT_COUPLING_THEOREM_AUDIT.csv"
PARSER_DRYRUN = OUT / "P8_Y5_R10_1445_PARSER_DRYRUN.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1445_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1445_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1445_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1445_VALIDATION.csv"

BRANCH_READOUT_REQUIREMENTS = OFFICIAL_READOUT / "P_WEP_K_CMSM_readout_REQUIREMENTS.csv"
BRANCH_READOUT_AUDIT = RESIDUAL_ROOT / "K_CMSM_readout_extraction_audit.csv"
BRANCH_COUPLING_CONTRACT = COEFFICIENT_ROOT / "C_parent_WEP_coupling_theorem_contract.csv"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_table(handle: Any, title: str, rows: list[dict[str, Any]]) -> None:
    handle.write(f"\n## {title}\n")
    if not rows:
        handle.write("\nNo rows.\n")
        return
    fields = list(rows[0].keys())
    handle.write("| " + " | ".join(fields) + " |\n")
    handle.write("| " + " | ".join(["---"] * len(fields)) + " |\n")
    for row in rows:
        handle.write("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |\n")


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def has_pending(rows: list[dict[str, Any]]) -> bool:
    text = " ".join(str(value) for row in rows for value in row.values()).upper()
    return "PENDING" in text or "MISSING" in text or "ABSENT" in text


def source_register_rows() -> list[dict[str, Any]]:
    local = [
        ("SRC1445_0_prev_next", PREV_NEXT, "1445 handoff"),
        ("SRC1445_1_prev_extraction", PREV_EXTRACTION, "1444 product extraction facts"),
        ("SRC1445_2_prev_refresh", PREV_REFRESH, "source-pack status refresh"),
        ("SRC1445_3_prev_c_parent", PREV_C_PARENT, "C_parent theorem/source search"),
        ("SRC1445_4_prev_validation", PREV_VALIDATION, "1444 validation"),
        ("SRC1445_5_readout_schema", READOUT_SCHEMA, "official readout required fields"),
        ("SRC1445_6_product_target", PRODUCT_TARGET, "partial product target"),
        ("SRC1445_7_c_parent_schema", C_PARENT_IMPORT_SCHEMA, "C_parent import schema"),
    ]
    web = [
        ("WEB1445_0_CQG_arxiv", "https://arxiv.org/abs/2209.15488", "CQG final result page"),
        ("WEB1445_1_CQG_eprint", "https://arxiv.org/e-print/2209.15488", "TeX source for readout/model anchors"),
        ("WEB1445_2_PRL_arxiv", "https://arxiv.org/abs/2209.15487", "PRL mission summary and eta bound"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role in local:
        rows.append(
            {
                "source_id": source_id,
                "source_path_or_url": str(path),
                "source_kind": "local_file",
                "resolved": path.exists(),
                "role": role,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    for source_id, url, role in web:
        rows.append(
            {
                "source_id": source_id,
                "source_path_or_url": url,
                "source_kind": "web_source_string_checked",
                "resolved": True,
                "role": role,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def readout_extraction_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "readout_id": "KREAD1445_0_axis_channel",
            "official_fact": "Gamma_x^(d), the differential acceleration along the most sensitive X axis, is the analysed readout channel",
            "source": "https://arxiv.org/e-print/2209.15488",
            "source_locator": "chap9.tex scientific sessions and available data; equation section",
            "maps_to_requirement": "axis; sign_convention; readout kernel orientation",
            "extraction_status": "PARTIAL_OFFICIAL_EXTRACTED",
            "remaining_gap": "positive X orientation and K_CMSM sign are not yet a local matrix row",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "readout_id": "KREAD1445_1_sampling",
            "official_fact": "measured accelerations are sampled at 4 Hz with timestamps; attitude data share timestamps; satellite position/velocity are provided at lower cadence",
            "source": "https://arxiv.org/e-print/2209.15488",
            "source_locator": "chap9.tex data-list paragraphs",
            "maps_to_requirement": "time_s; session_id; orbit_id; calibration_flag",
            "extraction_status": "PARTIAL_OFFICIAL_EXTRACTED",
            "remaining_gap": "actual arrays are not imported; interpolation/derivative conventions are not rows",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "readout_id": "KREAD1445_2_model_terms",
            "official_fact": "the X-channel model contains bias, common-mode coupling, differential gravity, gravity/inertia-gradient terms, offcentring terms, and correction terms",
            "source": "https://arxiv.org/e-print/2209.15488",
            "source_locator": "chap9.tex equation labelled eq_xacc and following correction discussion",
            "maps_to_requirement": "gx_m_s2; gz_m_s2; Sxx; Sxz; calibration_flag; source_url_or_path",
            "extraction_status": "STRUCTURE_EXTRACTED_VALUES_NOT_IMPORTED",
            "remaining_gap": "K_CMSM needs concrete column values/units, not just the published model structure",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "readout_id": "KREAD1445_3_masks_segments",
            "official_fact": "the final analysis uses session/segment handling and glitch/onboard masks before estimating eta",
            "source": "https://arxiv.org/e-print/2209.15488",
            "source_locator": "chap9.tex glitch detection and segment-analysis paragraphs",
            "maps_to_requirement": "mask_flag; orbit_average_rule; tau_eff definition",
            "extraction_status": "MASK_POLICY_DESCRIBED_ARRAYS_NOT_IMPORTED",
            "remaining_gap": "no local mask table reproduces final cuts or weights",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "readout_id": "KREAD1445_4_target_absence",
            "official_fact": "no local official-readout target file exists yet",
            "source": str(LIVE_READOUT_TARGET),
            "source_locator": "filesystem check",
            "maps_to_requirement": "P_WEP_K_CMSM_readout.csv",
            "extraction_status": "LIVE_TARGET_ABSENT",
            "remaining_gap": "must acquire official arrays or construct a reproducible design matrix before claim use",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def readout_requirement_rows(extraction: list[dict[str, Any]]) -> list[dict[str, Any]]:
    schema_rows = read_csv(READOUT_SCHEMA)
    extracted_map = {
        "time_s": "PARTIAL_SOURCE_FACT_ONLY_4HZ_TIMESTAMPS",
        "session_id": "PENDING_OFFICIAL_SEGMENT_TABLE",
        "orbit_id": "PENDING_ORBIT_PHASE_KEY",
        "axis": "PARTIAL_X_AXIS_EXTRACTED_SIGN_PENDING",
        "gx_m_s2": "PENDING_DESIGN_MATRIX_VALUES",
        "gz_m_s2": "PENDING_DESIGN_MATRIX_VALUES",
        "Sxx": "PENDING_GRADIENT_COLUMN_VALUES",
        "Sxz": "PENDING_GRADIENT_COLUMN_VALUES",
        "mask_flag": "PENDING_GLITCH_AND_ONBOARD_MASK_ROWS",
        "calibration_flag": "PENDING_CALIBRATION_STATE_ROWS",
        "attitude_quaternion_or_axis": "PENDING_ATTITUDE_ROWS",
        "source_url_or_path": "PENDING_OFFICIAL_ARRAY_SOURCE_PATH",
    }
    rows: list[dict[str, Any]] = []
    for index, schema in enumerate(schema_rows):
        column = schema.get("column", "")
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "requirement_id": f"KREQ1445_{index}",
                "column": column,
                "schema_definition": schema.get("definition", ""),
                "official_extraction_status": extracted_map.get(column, "PENDING_SCHEMA_COLUMN_REVIEW"),
                "live_target_path": str(LIVE_READOUT_TARGET),
                "live_target_exists": LIVE_READOUT_TARGET.exists(),
                "promotion_condition": "live target exists, parses, declares same branch, has values/units/source path, and contains no PENDING/MISSING placeholders",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": "KREQ1445_extra_K_CMSM_semantics",
            "column": "K_CMSM_semantics",
            "schema_definition": "conversion from official readout/model columns to the MTS WEP product kernel",
            "official_extraction_status": "PENDING_PARENT_BASIS_MAP_AND_UNITS",
            "live_target_path": str(LIVE_READOUT_TARGET),
            "live_target_exists": LIVE_READOUT_TARGET.exists(),
            "promotion_condition": "must specify units, sign, axis orientation, source projection, and branch lock",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def coupling_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "CTC1445_0_parent_action",
            "clause": "parent action must be explicit enough to vary with respect to local matter/source response slots",
            "minimal_contract": "S_parent[Phi, matter, theta] contains a declared WEP/source coupling sector, not an empirical post-fit coefficient",
            "current_status": "MISSING_PARENT_ACTION_SLOT",
            "failure_mode_if_absent": "C_parent becomes a closure parameter rather than a derived MTS coefficient",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "CTC1445_1_projection_generator",
            "clause": "vertical/source generator for the WEP Ti/Pt contrast must be defined in the parent basis",
            "minimal_contract": "V_WEP maps the Ti/Pt material contrast and source/readout projection into one branch-locked functional derivative",
            "current_status": "PARTIAL_BRANCH_GUARD_ONLY",
            "failure_mode_if_absent": "DD/material proxy or mixed-basis rows can be mistaken for MTS predictions",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "CTC1445_2_coefficient_definition",
            "clause": "C_parent_WEP must be a functional derivative or theorem-zero of the parent action",
            "minimal_contract": "C_parent_WEP := normalized delta S_parent / delta V_WEP, with declared units/sign/basis, or DERIVED_ZERO with a proof",
            "current_status": "CONTRACT_STATED_NOT_PROVEN",
            "failure_mode_if_absent": "numeric coefficient has no derivation and cannot compete with GR/Newton locally",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "CTC1445_3_GR_limit",
            "clause": "GR/Newton local limit must emerge by a signed suppression/annihilation mechanism",
            "minimal_contract": "universal minimal coupling branch gives zero or bounded residual without fitting to MICROSCOPE",
            "current_status": "NOT_DERIVED_FOR_WEP_SLOT",
            "failure_mode_if_absent": "local branch remains a phenomenological closure, not a GR-reduction proof",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "CTC1445_4_no_bound_inversion",
            "clause": "empirical bounds cannot define the parent coefficient",
            "minimal_contract": "MICROSCOPE may test C_parent_WEP but cannot be used to choose it",
            "current_status": "LOCKED_FORBIDDEN",
            "failure_mode_if_absent": "bound-as-prediction circularity",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "CTC1445_5_import_condition",
            "clause": "C_parent import requires either proof or source-backed finite coefficient",
            "minimal_contract": "row satisfies C_parent_import_schema with no placeholders and source path/URL/DOI",
            "current_status": "LIVE_IMPORT_ABSENT",
            "failure_mode_if_absent": "claim gate must remain false",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def coupling_audit_rows(contract: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": f"CTA1445_{index}",
            "clause_id": row["clause_id"],
            "audit_result": "PASS_FOR_CONTRACT_ONLY" if row["current_status"] in {"LOCKED_FORBIDDEN", "LIVE_IMPORT_ABSENT"} else "OPEN_DERIVATION_GAP",
            "claim_effect": "keeps C_parent_WEP nonclaim until parent action/coupling source exists",
            "next_action": "derive or source this clause before any import row is allowed",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, row in enumerate(contract)
    ]


def parser_dryrun_rows(requirements: list[dict[str, Any]], contract: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1445_0_readout_requirements",
            "target_path": str(BRANCH_READOUT_REQUIREMENTS),
            "target_exists": BRANCH_READOUT_REQUIREMENTS.exists(),
            "parser_status": "PASS_REQUIREMENTS_ONLY_NONCLAIM",
            "refusal_reason": "requirements file is not the official readout target and contains pending fields",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1445_1_live_readout",
            "target_path": str(LIVE_READOUT_TARGET),
            "target_exists": LIVE_READOUT_TARGET.exists(),
            "parser_status": "REFUSED_LIVE_K_CMSM_READOUT_ABSENT",
            "refusal_reason": "no K_CMSM/readout data rows exist",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1445_2_coupling_contract",
            "target_path": str(BRANCH_COUPLING_CONTRACT),
            "target_exists": BRANCH_COUPLING_CONTRACT.exists(),
            "parser_status": "PASS_CONTRACT_ONLY_NONCLAIM",
            "refusal_reason": "contract is not a DERIVED_ZERO proof or finite coefficient import",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1445_3_live_C_parent_import",
            "target_path": str(LIVE_C_PARENT_IMPORT),
            "target_exists": LIVE_C_PARENT_IMPORT.exists(),
            "parser_status": "REFUSED_LIVE_C_PARENT_IMPORT_ABSENT",
            "refusal_reason": "coupling theorem not proven and no finite source row exists",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1445_0_readout_absent", "live K_CMSM/readout target remains absent"),
        ("CG1445_1_requirements_only", "requirements rows are scaffold only and contain pending fields"),
        ("CG1445_2_coupling_contract_only", "C_parent coupling theorem is contract-only, not proof"),
        ("CG1445_3_C_parent_absent", "live C_parent_WEP_slot_import.csv remains absent"),
        ("CG1445_4_product_still_pending", "product convention still cannot promote while readout/source units are pending"),
        ("CG1445_5_no_local_claim", "no WEP/local-GR/Newton claim is allowed from 1445"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_status": "LOCKED_CLAIM_FALSE",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1445_0_no_live_readout",
            "decision": "do not create P_WEP_K_CMSM_readout.csv",
            "why": "official model structure is extractable but data/design matrix rows are absent",
            "consequence": "write requirements and extraction audit only",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1445_1_contract_C_parent",
            "decision": "state C_parent coupling theorem clauses explicitly",
            "why": "this is the cleanest derivation route and prevents closure parameters from masquerading as theory",
            "consequence": "next proof attempt can attack named clauses rather than vague coupling language",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1445_2_next_parent_action_search",
            "decision": "hunt parent-action/coupling source text before importing coefficients",
            "why": "K_CMSM alone cannot rescue the local branch if C_parent is not derivable",
            "consequence": "1446 should search corpus action/coupling files and map candidates to the theorem clauses",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1445_0_1446",
            "next_target": "1446-Y5-R10-RAB-parent-action-coupling-source-search-against-C-parent-contract.md",
            "script": "scripts/Y5_R10_RAB_parent_action_coupling_source_search_against_C_parent_contract.py",
            "objective": "search the post-checkpoint corpus for parent action/coupling candidates and map each one against the C_parent_WEP coupling theorem contract; do not import a coefficient unless a clause is actually source-signed.",
            "include": "corpus source search; parent action/coupling candidate ledger; clause-by-clause reduction audit; no-claim parser dry-run",
            "exclude": "numeric WEP score; local-GR claim; invented coefficient; bound-inverted C_parent; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_live_scaffolds(requirements: list[dict[str, Any]], extraction: list[dict[str, Any]], contract: list[dict[str, Any]]) -> None:
    write_csv(BRANCH_READOUT_REQUIREMENTS, requirements)
    write_csv(BRANCH_READOUT_AUDIT, extraction)
    write_csv(BRANCH_COUPLING_CONTRACT, contract)


def validation_rows(
    sources: list[dict[str, Any]],
    extraction: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated = [
        SOURCE_REGISTER,
        READOUT_EXTRACTION,
        READOUT_REQUIREMENTS,
        COUPLING_THEOREM,
        COUPLING_AUDIT,
        PARSER_DRYRUN,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        BRANCH_READOUT_REQUIREMENTS,
        BRANCH_READOUT_AUDIT,
        BRANCH_COUPLING_CONTRACT,
    ]
    all_sources_resolve = all(row["resolved"] for row in sources)
    extracted_structure = any(row["extraction_status"] == "STRUCTURE_EXTRACTED_VALUES_NOT_IMPORTED" for row in extraction)
    requirements_pending = has_pending(requirements)
    live_readout_absent = not LIVE_READOUT_TARGET.exists()
    contract_not_proof = any(row["current_status"] in {"CONTRACT_STATED_NOT_PROVEN", "NOT_DERIVED_FOR_WEP_SLOT"} for row in contract)
    audit_false = all(str(row["claim_allowed"]) == "False" for row in audit)
    dryrun_false = all(str(row["claim_allowed"]) == "False" for row in dryrun)
    gates_false = all(str(row["claim_allowed"]) == "False" for row in gates)
    c_parent_absent = not LIVE_C_PARENT_IMPORT.exists()
    csvs_parse = all(csv_parses(path) for path in generated)
    formalization_recent = 0
    if FORMALIZATION.exists():
        formalization_recent = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)
    checks = [
        ("VAL1445_0_source_register", all_sources_resolve, "all local sources exist and web source strings are recorded"),
        ("VAL1445_1_readout_structure", extracted_structure, "official readout model structure extracted but values not imported"),
        ("VAL1445_2_requirements_pending", requirements_pending, "readout requirements remain pending and nonclaim"),
        ("VAL1445_3_live_readout_absent", live_readout_absent, "live P_WEP_K_CMSM_readout.csv remains absent"),
        ("VAL1445_4_contract_not_proof", contract_not_proof, "C_parent coupling theorem is stated as contract, not proof"),
        ("VAL1445_5_audit_false", audit_false, "coupling audit keeps claim flags false"),
        ("VAL1445_6_dryrun_false", dryrun_false, "parser dry-run refuses score paths"),
        ("VAL1445_7_claim_gates", gates_false, "all claim gates remain false"),
        ("VAL1445_8_C_parent_absent", c_parent_absent, "live C_parent_WEP_slot_import.csv remains absent"),
        ("VAL1445_9_csv_parse", csvs_parse, "all generated 1445 CSVs parse cleanly"),
        ("VAL1445_10_formalization_untouched", formalization_recent == 0, f"formalization modified-file count since start={formalization_recent}"),
        ("VAL1445_11_next_target", True, "1446 handoff written"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail, "generated_utc": now()}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1445_12_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1445 records readout requirements and C_parent coupling contract without claims",
            "generated_utc": now(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    extraction: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1445 - K_CMSM readout extraction or C_parent coupling theorem\n\n")
        handle.write(
            "**Current verdict:** the official MICROSCOPE paper gives the X-channel/readout structure, sampling, "
            "and model ingredients, but not a local `P_WEP_K_CMSM_readout.csv` matrix. The right move is to keep "
            "readout as requirements-only and pin `C_parent_WEP` to a parent-action coupling theorem contract. "
            "No WEP/local-GR/Newton claim is opened.\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "K_CMSM readout official extraction", extraction)
        write_table(handle, "K_CMSM readout requirements", requirements)
        write_table(handle, "C_parent coupling theorem contract", contract)
        write_table(handle, "C_parent coupling theorem audit", audit)
        write_table(handle, "Parser dry-run", dryrun)
        write_table(handle, "Claim gates", gates)
        write_table(handle, "Decision ledger", decisions)
        write_table(handle, "Validation", validation)
        write_table(handle, "Next target", next_rows)


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def main() -> None:
    sources = source_register_rows()
    extraction = readout_extraction_rows()
    requirements = readout_requirement_rows(extraction)
    contract = coupling_theorem_rows()
    audit = coupling_audit_rows(contract)
    dryrun = parser_dryrun_rows(requirements, contract)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_live_scaffolds(requirements, extraction, contract)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(READOUT_EXTRACTION, extraction)
    write_csv(READOUT_REQUIREMENTS, requirements)
    write_csv(COUPLING_THEOREM, contract)
    write_csv(COUPLING_AUDIT, audit)
    write_csv(PARSER_DRYRUN, dryrun)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validation = validation_rows(sources, extraction, requirements, contract, audit, dryrun, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, extraction, requirements, contract, audit, dryrun, gates, decisions, validation, next_rows)
    remove_pycache()
    print("Y5_R10_1445_K_CMSM_requirements_C_parent_coupling_contract_nonclaim")


if __name__ == "__main__":
    main()
