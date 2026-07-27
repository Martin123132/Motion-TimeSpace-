from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
BRANCH_ROOT = ROOT / "source-intake" / "microscope" / "branch_locked_wep"
RESIDUAL_ROOT = BRANCH_ROOT / "residuals"
COEFFICIENT_ROOT = BRANCH_ROOT / "coefficients"
PRODUCT_ROOT = BRANCH_ROOT / "product"
GUARD_ROOT = BRANCH_ROOT / "guards"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1436-Y5-R10-RAB-first-projection-matrix-target-selection-and-row-contract.md"

BRANCH_ID_FILE = BRANCH_ROOT / "branch_id.csv"
C_PARENT_FILE = COEFFICIENT_ROOT / "C_parent.csv"
C_PARENT_IMPORT_SCHEMA = COEFFICIENT_ROOT / "C_parent_import_schema.csv"
ETA_PRODUCT_CONVENTION = PRODUCT_ROOT / "eta_product_convention.csv"
MEASURED_G_GUARD = GUARD_ROOT / "measured_G_guard.csv"

NEXT_1435 = OUT / "P8_Y5_R10_1435_NEXT_TARGET.csv"
DASHBOARD_1435 = OUT / "P8_Y5_R10_1435_ARENA_DRYRUN_DASHBOARD.csv"
MISSING_1435 = OUT / "P8_Y5_R10_1435_MISSING_INPUT_MATRIX.csv"
VALIDATION_1435 = OUT / "P8_Y5_BRR545_1435_VALIDATION.csv"
CT_PROJECTION_871 = OUT / "P8_Y5_R10_871_CT_PROJECTION_CONTRACT.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1436_SOURCE_REGISTER.csv"
PROJECTION_TARGET_RANKING = OUT / "P8_Y5_R10_1436_PROJECTION_TARGET_RANKING.csv"
FIRST_TARGET_CONTRACT = OUT / "P8_Y5_R10_1436_FIRST_TARGET_CONTRACT.csv"
PROJECTION_ROW_SCHEMA = OUT / "P8_Y5_R10_1436_PROJECTION_ROW_SCHEMA.csv"
REQUIRED_SOURCE_ROWS = OUT / "P8_Y5_R10_1436_REQUIRED_SOURCE_ROWS.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_R10_1436_RUNNER_REFUSAL_STATUS.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1436_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1436_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1436_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1436_VALIDATION.csv"

BRANCH_FIRST_TARGET = RESIDUAL_ROOT / "first_projection_matrix_target.csv"
BRANCH_ROW_SCHEMA = RESIDUAL_ROOT / "projection_row_contract_schema.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
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
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_has(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="ignore")


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def branch_id() -> str:
    rows = read_csv(BRANCH_ID_FILE)
    if len(rows) != 1:
        raise ValueError(f"expected one branch row, got {len(rows)}")
    value = rows[0].get("same_parent_branch_id", "").strip()
    if not value:
        raise ValueError("same_parent_branch_id missing")
    return value


def source_register_rows(branch: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC1436_0_1435_next", NEXT_1435, "NEXT1435_0_1436", "1435 handoff selecting projection target contract."),
        ("SRC1436_1_1435_validation", VALIDATION_1435, "VAL1435_9_overall", "1435 validation summary."),
        ("SRC1436_2_1435_dashboard", DASHBOARD_1435, "DRY1435_1", "1435 arena dry-run dashboard."),
        ("SRC1436_3_1435_missing_matrix", MISSING_1435, "MIM1435_5", "1435 missing-input matrix."),
        ("SRC1436_4_branch_id", BRANCH_ID_FILE, branch, "active same-parent branch lock."),
        ("SRC1436_5_c_parent", C_PARENT_FILE, "CP1430_6_verdict", "placeholder C_parent refusal rows."),
        ("SRC1436_6_c_parent_import_schema", C_PARENT_IMPORT_SCHEMA, "C_PARENT_IMPORT_SCHEMA_1431", "strict future import schema."),
        ("SRC1436_7_product_convention", ETA_PRODUCT_CONVENTION, "tau_eff = branch_locked_orbit_average", "eta product convention guard."),
        ("SRC1436_8_measured_g_guard", MEASURED_G_GUARD, "MGG1429_0_no_relative_absorption", "measured-G absorption guard."),
        ("SRC1436_9_ct_projection_871", CT_PROJECTION_871, "PC871_2_clock_WEP", "older trace projection contract family."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchor, role in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "anchor": anchor,
                "anchor_found": text_has(path, anchor),
                "role": role,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def dashboard_by_arena() -> dict[str, dict[str, str]]:
    return {row["arena_id"]: row for row in read_csv(DASHBOARD_1435)}


def ranking_rows(branch: str) -> list[dict[str, Any]]:
    dashboard = dashboard_by_arena()
    specs = [
        {
            "rank": 1,
            "arena_id": "ABM1434_1_WEP",
            "projection_matrix_id": "P_WEP_TRACE_TO_ETA_TIPT_1436",
            "candidate_target": "P_WEP",
            "selection_status": "SELECTED_FIRST_TARGET",
            "leverage_score": 5,
            "source_maturity_score": 4,
            "local_gr_relevance_score": 5,
            "reason": "sharpest composition/coupling pressure; directly tests whether trace leakage creates differential acceleration.",
        },
        {
            "rank": 2,
            "arena_id": "ABM1434_2_PPN",
            "projection_matrix_id": "P_PPN_TRACE_TO_METRIC_VECTOR_1436",
            "candidate_target": "P_PPN",
            "selection_status": "SECOND_TARGET",
            "leverage_score": 5,
            "source_maturity_score": 4,
            "local_gr_relevance_score": 5,
            "reason": "closest to local-GR reduction, but needs metric response operator and gauge fixing before a row is meaningful.",
        },
        {
            "rank": 3,
            "arena_id": "ABM1434_3_CLOCK",
            "projection_matrix_id": "P_CLOCK_TRACE_TO_REDSHIFT_1436",
            "candidate_target": "P_CLOCK",
            "selection_status": "THIRD_TARGET",
            "leverage_score": 4,
            "source_maturity_score": 4,
            "local_gr_relevance_score": 4,
            "reason": "fewest missing inputs, useful for clock pressure, but narrower than WEP/PPN for local-GR closure.",
        },
        {
            "rank": 4,
            "arena_id": "ABM1434_0_R10",
            "projection_matrix_id": "P_R10_TRACE_TO_ALPHA_LAMBDA_1436",
            "candidate_target": "P_R10",
            "selection_status": "DEFERRED_TARGET",
            "leverage_score": 4,
            "source_maturity_score": 2,
            "local_gr_relevance_score": 3,
            "reason": "strong short-range arena, but still anchor-only/non-curve and requires lambda/Z/source-normalized coupling.",
        },
        {
            "rank": 5,
            "arena_id": "ABM1434_4_ORBITAL_NEWTON",
            "projection_matrix_id": "P_GM_TRACE_TO_SOURCE_NORMALIZATION_1436",
            "candidate_target": "P_GM",
            "selection_status": "DEFERRED_TARGET",
            "leverage_score": 3,
            "source_maturity_score": 2,
            "local_gr_relevance_score": 4,
            "reason": "important Newtonian-limit guard, but first needs a selected observable and source-worldtube weighting.",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        dry = dashboard[spec["arena_id"]]
        missing_count = int(dry["missing_input_count"])
        priority_score = (
            100 * spec["leverage_score"]
            + 20 * spec["source_maturity_score"]
            + 20 * spec["local_gr_relevance_score"]
            - 15 * missing_count
        )
        rows.append(
            {
                "same_parent_branch_id": branch,
                "rank": spec["rank"],
                "arena_id": spec["arena_id"],
                "arena": dry["arena"],
                "observable": dry["observable"],
                "candidate_target": spec["candidate_target"],
                "projection_matrix_id": spec["projection_matrix_id"],
                "missing_input_count": missing_count,
                "source_status": dry["source_status"],
                "leverage_score": spec["leverage_score"],
                "source_maturity_score": spec["source_maturity_score"],
                "local_gr_relevance_score": spec["local_gr_relevance_score"],
                "priority_score": priority_score,
                "selection_status": spec["selection_status"],
                "reason": spec["reason"],
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def missing_inputs_for(arena_id: str) -> list[str]:
    return [row["missing_input"] for row in read_csv(MISSING_1435) if row.get("arena_id") == arena_id]


def first_target_contract_rows(branch: str) -> list[dict[str, Any]]:
    missing_inputs = "; ".join(missing_inputs_for("ABM1434_1_WEP"))
    return [
        {
            "same_parent_branch_id": branch,
            "contract_id": "FTC1436_0_P_WEP_FIRST_ROW",
            "selected_projection_matrix_id": "P_WEP_TRACE_TO_ETA_TIPT_1436",
            "selected_arena_id": "ABM1434_1_WEP",
            "selected_arena": "WEP_MICROSCOPE",
            "observable": "eta_Ti_Pt",
            "formula_shape": "eta_AB = P_WEP[C_parent, R_source, R_material, K_CMSM, eta_product_convention, measured_G_guard]",
            "required_inputs": "C_parent numeric/zero; full material tensor; source worldtube; official K_CMSM; official sign convention",
            "current_missing_inputs": missing_inputs,
            "row_status": "CONTRACT_ONLY_INPUTS_MISSING",
            "runner_effect": "BLOCK_NUMERIC_SCORE_UNTIL_ALL_REQUIRED_ROWS_ARE_SOURCED",
            "anti_shortcut_guard": "tau_eff=1 and measured-G relative absorption remain forbidden",
            "source_path": str(DOC),
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def projection_row_schema_rows(branch: str) -> list[dict[str, Any]]:
    schema = [
        ("same_parent_branch_id", "string", "must equal active branch id", "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"),
        ("projection_matrix_id", "string", "unique projection contract id", "P_WEP_TRACE_TO_ETA_TIPT_1436"),
        ("arena_id", "string", "dry-run arena id", "ABM1434_1_WEP"),
        ("observable", "string", "observable being predicted", "eta_Ti_Pt"),
        ("source_basis", "string", "source-worldtube and environmental basis", "MISSING_SOURCE_WORLDTUBE"),
        ("material_basis", "string", "test-mass material tensor basis", "MISSING_Ti_Pt_MATERIAL_TENSOR"),
        ("readout_basis", "string", "instrument/orbit/readout convention", "MISSING_OFFICIAL_K_CMSM"),
        ("formula_shape", "string", "symbolic row formula", "eta_AB=P_WEP[...]"),
        ("required_inputs", "semicolon_list", "all mandatory source/input rows", "C_parent;R_source;R_material;K_CMSM"),
        ("units", "string", "dimensionless eta after declared conversion factors", "dimensionless"),
        ("source_path", "path", "local source/provenance path for the row", str(DOC)),
        ("parent_status", "enum", "SOURCE_BACKED_NUMERIC | DERIVED_ZERO | CLOSURE_ONLY | MISSING_PARENT_INPUT", "MISSING_PARENT_INPUT"),
        ("valid_prediction_row", "bool", "true only after row is numeric/derived and sourced", "False"),
        ("valid_for_claim", "bool", "true only after all gates pass", "False"),
        ("claim_allowed", "bool", "must remain false in 1436", "False"),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "schema_id": f"PRS1436_{index}",
            "field": field,
            "type": field_type,
            "rule": rule,
            "example_or_current_value": example,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, (field, field_type, rule, example) in enumerate(schema)
    ]


def required_source_rows(branch: str) -> list[dict[str, Any]]:
    specs = [
        (
            "REQ1436_0_C_parent",
            "C_parent numeric/zero",
            C_PARENT_FILE,
            "CP1430_6_verdict",
            "PLACEHOLDER_ONLY_NOT_SCOREABLE",
            "import parent-signed zero theorem or numeric coefficient vector",
        ),
        (
            "REQ1436_1_material_tensor",
            "full Ti/Pt material tensor",
            "",
            "",
            "MISSING_SOURCE_PATH",
            "source or build official composition/material-response tensor for Ti and Pt/Rh test masses",
        ),
        (
            "REQ1436_2_source_worldtube",
            "Earth/source worldtube and orbit weighting",
            "",
            "",
            "MISSING_SOURCE_PATH",
            "source finite-size worldtube/orbit weighting compatible with MICROSCOPE readout",
        ),
        (
            "REQ1436_3_K_CMSM",
            "official K_CMSM or readout kernel",
            "",
            "",
            "MISSING_SOURCE_PATH",
            "source official/reproducible MICROSCOPE readout kernel and sign convention",
        ),
        (
            "REQ1436_4_eta_product_convention",
            "eta product convention",
            ETA_PRODUCT_CONVENTION,
            "tau_eff = branch_locked_orbit_average",
            "EXISTS_GUARD_NOT_OFFICIAL_COMPLETE",
            "keep product rule; fill official body order and orbit average",
        ),
        (
            "REQ1436_5_measured_G_guard",
            "measured-G absorption guard",
            MEASURED_G_GUARD,
            "MGG1429_0_no_relative_absorption",
            "EXISTS_GUARD_NOT_EXTERNAL_COMPLETE",
            "keep relative-absorption forbidden",
        ),
        (
            "REQ1436_6_official_sign_convention",
            "official sign/body-axis convention",
            "",
            "",
            "MISSING_SOURCE_PATH",
            "source official sign/body-order convention before any eta comparison",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for req_id, required_row, path, anchor, status, next_action in specs:
        path_obj = Path(path) if path else None
        rows.append(
            {
                "same_parent_branch_id": branch,
                "required_row_id": req_id,
                "projection_matrix_id": "P_WEP_TRACE_TO_ETA_TIPT_1436",
                "required_row": required_row,
                "source_path": str(path_obj) if path_obj else "MISSING_SOURCE_PATH",
                "path_exists": path_obj.exists() if path_obj else False,
                "anchor": anchor or "MISSING_ANCHOR",
                "anchor_found": text_has(path_obj, anchor) if path_obj and anchor else False,
                "row_status": status,
                "next_action": next_action,
                "blocks_numeric_score": True,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def runner_refusal_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "runner_id": "RRF1436_0_projection_contract_only",
            "selected_projection_matrix_id": "P_WEP_TRACE_TO_ETA_TIPT_1436",
            "score_status": "REFUSED_CONTRACT_ONLY_INPUTS_MISSING",
            "refusal_reason": "P_WEP has a formula contract but lacks C_parent, material tensor, source worldtube, official K_CMSM, and sign convention.",
            "claim_consequence": "no WEP/local-GR/local-residual claim may be made from 1436",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def claim_gate_rows(branch: str) -> list[dict[str, Any]]:
    gates = [
        ("CG1436_0_no_numeric_score", "P_WEP score remains forbidden until all source rows are real and sourced."),
        ("CG1436_1_no_tau_shortcut", "tau_eff=1 is forbidden; orbit/readout weighting must be sourced."),
        ("CG1436_2_no_measured_G_absorption", "relative Ti/Pt residual cannot be hidden in measured G."),
        ("CG1436_3_no_parent_placeholder", "MISSING_PARENT_INPUT rows cannot become evidence."),
        ("CG1436_4_no_local_GR_claim", "selection of WEP target is a workflow decision, not a local-GR pass."),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "gate_id": gate_id,
            "gate": gate,
            "gate_status": "LOCKED_FALSE_CLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate in gates
    ]


def decision_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1436_0_select_WEP",
            "decision": "select P_WEP_TRACE_TO_ETA_TIPT_1436 as the first projection-matrix target",
            "why": "WEP is the most surgical coupling test: if the trace residual creates species-dependent acceleration, this is where it should be forced into a sourced row.",
            "what_it_does_not_mean": "does not prove or disprove MTS; does not score eta; does not claim local GR",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1436_1_next_step",
            "decision": "attempt first P_WEP row or write the source-input acquisition ledger",
            "why": "the next bottleneck is no longer abstract coupling; it is the concrete map from C_parent and source/material/readout tensors to eta_Ti_Pt",
            "what_it_does_not_mean": "does not allow a placeholder source row to pass",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1436_0_1437",
            "next_target": "1437-Y5-R10-RAB-P-WEP-first-row-or-source-input-acquisition-ledger.md",
            "script": "scripts/Y5_R10_RAB_P_WEP_first_row_or_source_input_acquisition_ledger.py",
            "objective": "attempt the first branch-locked P_WEP projection row; if required inputs are unavailable, write the source acquisition ledger for C_parent, material tensor, source worldtube, K_CMSM, and sign convention.",
            "include": "P_WEP first row attempt; missing-source acquisition ledger; no-tau-shortcut guard; measured-G guard",
            "exclude": "numeric WEP claim; local-GR pass; placeholder coefficient promotion; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_branch_files(contract: list[dict[str, Any]], schema: list[dict[str, Any]]) -> None:
    write_csv(BRANCH_FIRST_TARGET, contract)
    write_csv(BRANCH_ROW_SCHEMA, schema)


def validation_rows(
    sources: list[dict[str, Any]],
    ranking: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    required: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        PROJECTION_TARGET_RANKING,
        FIRST_TARGET_CONTRACT,
        PROJECTION_ROW_SCHEMA,
        REQUIRED_SOURCE_ROWS,
        RUNNER_REFUSAL,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        BRANCH_FIRST_TARGET,
        BRANCH_ROW_SCHEMA,
    ]
    parse_ok = True
    parse_errors: list[str] = []
    truthy_claim_flags: list[str] = []
    for path in csvs:
        try:
            parsed_rows = read_csv(path)
        except Exception as exc:
            parse_ok = False
            parse_errors.append(f"{path.name}:{type(exc).__name__}")
            continue
        for index, row in enumerate(parsed_rows, start=2):
            for key in ("claim_allowed", "valid_for_claim", "valid_prediction_row"):
                if (row.get(key) or "").strip().lower() == "true":
                    truthy_claim_flags.append(f"{path.name}:{index}:{key}=true")
    source_register_ok = all(row["path_exists"] and row["anchor_found"] for row in sources)
    selected_rows = [row for row in ranking if row["selection_status"] == "SELECTED_FIRST_TARGET"]
    selected_ok = (
        len(selected_rows) == 1
        and selected_rows[0]["candidate_target"] == "P_WEP"
        and selected_rows[0]["arena_id"] == "ABM1434_1_WEP"
    )
    contract_ok = (
        len(contract) == 1
        and contract[0]["selected_projection_matrix_id"] == "P_WEP_TRACE_TO_ETA_TIPT_1436"
        and contract[0]["row_status"] == "CONTRACT_ONLY_INPUTS_MISSING"
    )
    schema_fields = {row["field"] for row in schema}
    schema_ok = {
        "same_parent_branch_id",
        "projection_matrix_id",
        "source_basis",
        "material_basis",
        "readout_basis",
        "parent_status",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
    }.issubset(schema_fields)
    required_missing_visible = any(row["source_path"] == "MISSING_SOURCE_PATH" for row in required)
    all_required_block = all(row["blocks_numeric_score"] for row in required)
    runner_refuses = all(row["score_status"].startswith("REFUSED") for row in runner)
    claim_safe = not truthy_claim_flags and all(str(row.get("claim_allowed")).lower() == "false" for row in claims)
    branch_files_ok = BRANCH_FIRST_TARGET.exists() and BRANCH_ROW_SCHEMA.exists()
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1436_0_source_register", source_register_ok, "all 1436 cited source-register paths and anchors resolve"),
        ("VAL1436_1_selected_target", selected_ok, "P_WEP is the single selected first target"),
        ("VAL1436_2_contract", contract_ok, "first target contract is WEP and contract-only"),
        ("VAL1436_3_schema", schema_ok, "projection row schema includes source/material/readout and claim gates"),
        ("VAL1436_4_required_inputs", required_missing_visible and all_required_block, "missing required inputs remain visible and block score"),
        ("VAL1436_5_runner_refusal", runner_refuses, "runner status refuses numeric scoring"),
        ("VAL1436_6_claim_gates", claim_safe, "all claim/valid/prediction flags remain false"),
        ("VAL1436_7_csv_parse", parse_ok, "all generated 1436 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1436_8_branch_files", branch_files_ok, "branch-locked first-target and row-schema files written"),
        ("VAL1436_9_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1436_10_next_target", True, "1437 handoff written"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1436_11_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1436 selects WEP as first projection target and locks it as nonclaim contract-only work",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1436 - First projection-matrix target selection and row contract",
            "**Current verdict:** WEP is selected as the first residual-to-observable projection target, but only as a contract. No WEP, R10, PPN, clock, orbital, or local-GR claim is allowed.",
            "**Main progress:** the coupling problem has been narrowed to a concrete `P_WEP` row: map `C_parent`, source worldtube, material tensor, readout kernel, product convention, and measured-G guard into `eta_Ti_Pt` without shortcuts.",
            "## Source register\n" + md_table(sections["sources"]),
            "## Projection target ranking\n" + md_table(sections["ranking"]),
            "## First target contract\n" + md_table(sections["contract"]),
            "## Projection row schema\n" + md_table(sections["schema"]),
            "## Required source rows\n" + md_table(sections["required"]),
            "## Runner refusal status\n" + md_table(sections["runner"]),
            "## Claim gates\n" + md_table(sections["claims"]),
            "## Decision ledger\n" + md_table(sections["decisions"]),
            "## Validation\n" + md_table(sections["validation"]),
            "## Next target\n" + md_table(sections["next"]),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RESIDUAL_ROOT.mkdir(parents=True, exist_ok=True)
    branch = branch_id()
    sources = source_register_rows(branch)
    ranking = ranking_rows(branch)
    contract = first_target_contract_rows(branch)
    schema = projection_row_schema_rows(branch)
    required = required_source_rows(branch)
    runner = runner_refusal_rows(branch)
    claims = claim_gate_rows(branch)
    decisions = decision_rows(branch)
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PROJECTION_TARGET_RANKING, ranking)
    write_csv(FIRST_TARGET_CONTRACT, contract)
    write_csv(PROJECTION_ROW_SCHEMA, schema)
    write_csv(REQUIRED_SOURCE_ROWS, required)
    write_csv(RUNNER_REFUSAL, runner)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    write_branch_files(contract, schema)

    validation = validation_rows(sources, ranking, contract, schema, required, runner, claims)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "ranking": ranking,
            "contract": contract,
            "schema": schema,
            "required": required,
            "runner": runner,
            "claims": claims,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1436_first_projection_target_selected_WEP_contract_only_nonclaim")


if __name__ == "__main__":
    main()
