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
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1444-Y5-R10-RAB-product-convention-official-extraction-or-C-parent-theorem-source-search.md"

PREV_NEXT = OUT / "P8_Y5_R10_1443_NEXT_TARGET.csv"
PREV_PRODUCT = OUT / "P8_Y5_R10_1443_PRODUCT_CONVENTION_FIRST_FILL.csv"
PREV_C_PARENT_SEARCH = OUT / "P8_Y5_R10_1443_C_PARENT_SOURCE_SEARCH_PLAN.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1443_VALIDATION.csv"

PRODUCT_SCHEMA = METADATA / "P8_Y5_R10_1336_PRODUCT_CONVENTION_SCHEMA.csv"
READOUT_SCHEMA = METADATA / "P8_Y5_R10_1336_OFFICIAL_READOUT_SCHEMA.csv"
SOURCE_WORLDTUBE_SCHEMA = METADATA / "P8_Y5_R10_1336_SOURCE_WORLDTUBE_SCHEMA.csv"
WEB_REGISTER = METADATA / "P8_Y5_R10_1336_WEB_SOURCE_CANDIDATE_REGISTER.csv"
OLD_PRODUCT_GUARD = BRANCH_ROOT / "product" / "eta_product_convention.csv"
PACK_MANIFEST = RESIDUAL_ROOT / "official_microscope_source_pack_manifest.csv"
LIVE_BRANCH_GUARD = MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv"
LIVE_PRODUCT_TARGET = MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv"
LIVE_C_PARENT_IMPORT = COEFFICIENT_ROOT / "C_parent_WEP_slot_import.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1444_SOURCE_REGISTER.csv"
OFFICIAL_EXTRACTION = OUT / "P8_Y5_R10_1444_PRODUCT_CONVENTION_OFFICIAL_EXTRACTION.csv"
PRODUCT_PROMOTION_AUDIT = OUT / "P8_Y5_R10_1444_PRODUCT_PROMOTION_AUDIT.csv"
SOURCE_PACK_REFRESH = OUT / "P8_Y5_R10_1444_SOURCE_PACK_STATUS_REFRESH.csv"
C_PARENT_THEOREM_SEARCH = OUT / "P8_Y5_R10_1444_C_PARENT_THEOREM_SOURCE_SEARCH.csv"
PARSER_DRYRUN = OUT / "P8_Y5_R10_1444_PARSER_DRYRUN.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1444_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1444_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1444_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1444_VALIDATION.csv"

BRANCH_PRODUCT_AUDIT = RESIDUAL_ROOT / "product_convention_official_extraction_audit.csv"
BRANCH_C_PARENT_SEARCH = COEFFICIENT_ROOT / "C_parent_WEP_theorem_source_search.csv"

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


def write_markdown_table(handle: Any, title: str, rows: list[dict[str, Any]]) -> None:
    handle.write(f"\n## {title}\n")
    if not rows:
        handle.write("\nNo rows.\n")
        return
    fields = list(rows[0].keys())
    handle.write("| " + " | ".join(fields) + " |\n")
    handle.write("| " + " | ".join(["---"] * len(fields)) + " |\n")
    for row in rows:
        handle.write("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |\n")


def is_source_resolved(value: str) -> bool:
    if value.startswith("https://") or value.startswith("http://"):
        return True
    return Path(value).exists()


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def contains_pending(row: dict[str, Any]) -> bool:
    text = " ".join(str(value) for value in row.values()).upper()
    return "PENDING" in text or "MISSING" in text


def source_register_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC1444_0_prev_next", PREV_NEXT, "1443 handoff into official product extraction"),
        ("SRC1444_1_prev_product", PREV_PRODUCT, "current nonclaim product first-fill row"),
        ("SRC1444_2_prev_c_parent", PREV_C_PARENT_SEARCH, "current C_parent source-search route"),
        ("SRC1444_3_prev_validation", PREV_VALIDATION, "1443 validation gate"),
        ("SRC1444_4_product_schema", PRODUCT_SCHEMA, "product convention required fields"),
        ("SRC1444_5_readout_schema", READOUT_SCHEMA, "official readout/readout-kernel required fields"),
        ("SRC1444_6_source_schema", SOURCE_WORLDTUBE_SCHEMA, "source-worldtube required fields"),
        ("SRC1444_7_web_register", WEB_REGISTER, "already recorded MICROSCOPE web sources"),
        ("SRC1444_8_old_product_guard", OLD_PRODUCT_GUARD, "older product guard row"),
        ("SRC1444_9_pack_manifest", PACK_MANIFEST, "source-pack manifest"),
        ("SRC1444_10_live_branch_guard", LIVE_BRANCH_GUARD, "same-parent branch guard"),
        ("SRC1444_11_live_product_target", LIVE_PRODUCT_TARGET, "live product target written in 1443"),
    ]
    web_sources = [
        (
            "WEB1444_0_CQG_arxiv",
            "https://arxiv.org/abs/2209.15488",
            "CQG final MICROSCOPE paper: eta formula, Ti/Pt channel, X-axis readout, sessions",
        ),
        (
            "WEB1444_1_PRL_arxiv",
            "https://arxiv.org/abs/2209.15487",
            "PRL final MICROSCOPE result: mission context and eta(Ti,Pt) bound",
        ),
        (
            "WEB1444_2_CQG_eprint",
            "https://arxiv.org/e-print/2209.15488",
            "TeX source checked for product-convention anchors",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role in local_sources:
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
    for source_id, url, role in web_sources:
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


def official_extraction_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "evidence_id": "OPE1444_0_eta_formula",
            "field": "eta_formula",
            "extracted_value": "eta(A,B)=2(a_A-a_B)/(a_A+a_B); reported channel eta(Ti,Pt), so A=Ti and B=Pt for the quoted final WEP channel",
            "source": "https://arxiv.org/abs/2209.15488",
            "source_locator": "abstract and arXiv TeX source chap9.tex",
            "extraction_status": "OFFICIAL_EXTRACTED",
            "remaining_gap": "does not by itself fix readout-kernel sign or MTS parent-basis coefficient",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "evidence_id": "OPE1444_1_test_mass_order",
            "field": "material_channel",
            "extracted_value": "SUEP compares PtRh10 inner mass with Ti alloy outer mass; final published channel is eta(Ti,Pt)",
            "source": "https://arxiv.org/e-print/2209.15488",
            "source_locator": "chap9.tex SUEP/test-mass composition paragraphs",
            "extraction_status": "OFFICIAL_EXTRACTED",
            "remaining_gap": "full material tensor remains separate and cannot be replaced by composition text alone",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "evidence_id": "OPE1444_2_readout_axis",
            "field": "sign_convention",
            "extracted_value": "difference acceleration Gamma_x^(d) along the most sensitive X axis is the analysed channel",
            "source": "https://arxiv.org/e-print/2209.15488",
            "source_locator": "chap9.tex scientific sessions and available data",
            "extraction_status": "PARTIAL_OFFICIAL_EXTRACTED",
            "remaining_gap": "positive X-axis orientation, body-order sign through the calibrated design matrix, and K_CMSM sign are not fully extracted",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "evidence_id": "OPE1444_3_sampling_and_segments",
            "field": "orbit_average_rule",
            "extracted_value": "accelerometer data are sampled at 4 Hz; SUEP uses 19 analysed segments totalling 1362 orbits",
            "source": "https://arxiv.org/e-print/2209.15488",
            "source_locator": "chap9.tex session/data-analysis paragraphs",
            "extraction_status": "PARTIAL_OFFICIAL_EXTRACTED",
            "remaining_gap": "actual segment mask, glitch mask, weighting, and reproducible orbit-average rows are not imported",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "evidence_id": "OPE1444_4_public_data_route",
            "field": "source_pack_route",
            "extracted_value": "official source strings identify ONERA/CMSM data route, but local calibrated arrays are not present",
            "source": str(WEB_REGISTER),
            "source_locator": "WEB1336_0 and WEB1336_1 rows",
            "extraction_status": "SOURCE_STRING_ONLY_ARRAYS_NOT_IMPORTED",
            "remaining_gap": "official readout rows, attitude/orbit arrays, and source-worldtube projection remain absent locally",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def product_row() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "eta_formula": "eta(A,B)=2(a_A-a_B)/(a_A+a_B); official channel eta(Ti,Pt), hence A=Ti and B=Pt for the published WEP channel",
            "sign_convention": "PARTIAL_OFFICIAL_BODY_ORDER_TiPt_AND_X_AXIS_EXTRACTED; PENDING_POSITIVE_X_AXIS_ORIENTATION_AND_K_CMSM_SIGN",
            "tau_eff_definition": "tau_eff = branch_locked_orbit_average(K_CMSM * R_source * readout_mask); official Gamma_x^(d), 4 Hz timestamps, and 19 SUEP segments are known but the full design matrix/mask is not imported",
            "readout_kernel_units": "PENDING_OFFICIAL_K_CMSM_UNITS_AND_COLUMN_MAP",
            "source_kernel_units": "PENDING_PARENT_SOURCE_BASIS_UNITS",
            "orbit_average_rule": "PENDING_OFFICIAL_SEGMENT_MASK_GLITCH_MASK_AND_REPRODUCIBLE_CQG_ORBIT_WEIGHTING",
            "branch_lock": BRANCH_ID,
            "source_path": str(DOC),
            "row_status": "PRODUCT_CONVENTION_OFFICIAL_PARTIAL_EXTRACTION_NONCLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def promotion_audit_rows(extraction: list[dict[str, Any]], product: list[dict[str, Any]]) -> list[dict[str, Any]]:
    row = product[0]
    fields = [
        ("eta_formula", "PROMOTABLE_FACT_ONLY", "official formula/body order is extracted, but this is not a prediction"),
        ("sign_convention", "BLOCKED_PENDING_SIGN", row["sign_convention"]),
        ("tau_eff_definition", "BLOCKED_PENDING_DESIGN_MATRIX", row["tau_eff_definition"]),
        ("readout_kernel_units", "BLOCKED_PENDING_READOUT_UNITS", row["readout_kernel_units"]),
        ("source_kernel_units", "BLOCKED_PENDING_SOURCE_BASIS", row["source_kernel_units"]),
        ("orbit_average_rule", "BLOCKED_PENDING_MASK_AND_WEIGHTING", row["orbit_average_rule"]),
        ("branch_lock", "NONCLAIM_GUARD_OK", "branch guard exists but cannot score WEP without all same-branch factors"),
        ("C_parent_WEP", "BLOCKED_IMPORT_ABSENT", "live C_parent_WEP_slot_import.csv remains absent"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": f"PPA1444_{index}",
            "field": field,
            "status": status,
            "detail": detail,
            "official_evidence_count": sum(1 for item in extraction if item["field"] == field),
            "promote_to_claim_allowed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, (field, status, detail) in enumerate(fields)
    ]


def source_pack_refresh_rows(product: list[dict[str, Any]]) -> list[dict[str, Any]]:
    targets = [
        ("PACK1444_0_official_readout", "official_readout", MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"),
        ("PACK1444_1_source_worldtube", "source_worldtube", MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"),
        ("PACK1444_2_product_convention", "product_convention", LIVE_PRODUCT_TARGET),
        ("PACK1444_3_branch_classifier", "branch_classifier", LIVE_BRANCH_GUARD),
        ("PACK1444_4_material_tensor", "material_tensor", MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"),
        ("PACK1444_5_C_parent_import", "C_parent_import", LIVE_C_PARENT_IMPORT),
    ]
    rows: list[dict[str, Any]] = []
    product_pending = contains_pending(product[0])
    for pack_id, item, target in targets:
        target_exists = target.exists()
        if item == "product_convention" and product_pending:
            status = "EXISTS_BUT_PENDING_NONCLAIM"
        elif item == "branch_classifier" and target_exists:
            status = "EXISTS_GUARD_NONCLAIM"
        elif target_exists:
            status = "EXISTS_REQUIRES_PROMOTION_AUDIT"
        else:
            status = "MISSING_REQUIRED_FILE"
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "pack_id": pack_id,
                "pack_item": item,
                "target_path": str(target),
                "target_exists": target_exists,
                "current_status": status,
                "promotion_allowed_now": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def c_parent_theorem_search_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "search_id": "CTS1444_0_parent_action_slot",
            "route": "derive C_parent_WEP from parent action",
            "input_sources": "AX1090 reduction audit; minimal WEP parent clause audits; C_parent closure demotion",
            "reduction_test": "single MTS parent action gives a signed WEP slot coefficient in the same branch as product/readout/source rows",
            "current_result": "NOT_FOUND_IN_CURRENT_LEDGER",
            "obstruction": "parent action/coupling map still closure-only for this slot",
            "next_action": "search coupling/action documents for a source-backed coefficient definition before importing any number",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "search_id": "CTS1444_1_zero_theorem",
            "route": "prove DERIVED_ZERO",
            "input_sources": str(COEFFICIENT_ROOT / "C_parent_WEP_clause_closure_demotion.csv"),
            "reduction_test": "all WEP vertical/source terms annihilate by parent geometry rather than by empirical tuning",
            "current_result": "FAILED_TO_CERTIFY_ZERO",
            "obstruction": "countermodels remain and quotient-invariant matter action is not signed enough",
            "next_action": "do not create zero import; only reopen if parent action proves signed annihilation",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "search_id": "CTS1444_2_numeric_source",
            "route": "source finite parent coefficient",
            "input_sources": "MTS coupling ledgers and future source pack",
            "reduction_test": "finite coefficient has units/sign/basis/source path and is not fitted to MICROSCOPE bound",
            "current_result": "OPEN_SOURCE_SEARCH",
            "obstruction": "no current row satisfies C_parent_import_schema without placeholders",
            "next_action": "build candidate intake only if a parent coefficient source is found",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "search_id": "CTS1444_3_forbidden_bound_inversion",
            "route": "invert MICROSCOPE bound into C_parent",
            "input_sources": "eta(Ti,Pt) bound",
            "reduction_test": "would turn an empirical limit into the model coefficient",
            "current_result": "FORBIDDEN",
            "obstruction": "circular bound-as-prediction shortcut",
            "next_action": "refuse as source for C_parent import",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "search_id": "CTS1444_4_nonclaim_pack_route",
            "route": "complete product/readout/source pack as nonclaim",
            "input_sources": "official MICROSCOPE source pack",
            "reduction_test": "parser can later compare a sourced coefficient against bounds without claiming local-GR pass",
            "current_result": "OPEN_NONCLAIM_ROUTE",
            "obstruction": "readout K_CMSM, source-worldtube, material tensor, and C_parent remain incomplete",
            "next_action": "prioritise K_CMSM/readout extraction and positive-axis convention",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def parser_dryrun_rows(product: list[dict[str, Any]], refresh: list[dict[str, Any]]) -> list[dict[str, Any]]:
    product_status = "REFUSED_PENDING_PRODUCT_FIELDS" if contains_pending(product[0]) else "UNEXPECTED_PROMOTABLE"
    missing = [row["pack_item"] for row in refresh if row["current_status"] == "MISSING_REQUIRED_FILE"]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1444_0_product_target",
            "target_path": str(LIVE_PRODUCT_TARGET),
            "target_exists": LIVE_PRODUCT_TARGET.exists(),
            "parser_status": product_status,
            "refusal_reason": "positive axis/K_CMSM/source units/orbit weighting remain pending",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1444_1_source_pack",
            "target_path": str(PACK_MANIFEST),
            "target_exists": PACK_MANIFEST.exists(),
            "parser_status": "REFUSED_INCOMPLETE_SOURCE_PACK",
            "refusal_reason": ";".join(missing),
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1444_2_C_parent_import",
            "target_path": str(LIVE_C_PARENT_IMPORT),
            "target_exists": LIVE_C_PARENT_IMPORT.exists(),
            "parser_status": "REFUSED_LIVE_C_PARENT_IMPORT_ABSENT",
            "refusal_reason": "theorem/source search ledger is not an import row",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1444_0_product_partial", "product convention remains partial and contains pending official fields"),
        ("CG1444_1_readout_missing", "official K_CMSM/readout matrix is absent locally"),
        ("CG1444_2_source_missing", "source-worldtube projection is absent locally"),
        ("CG1444_3_C_parent_absent", "live C_parent_WEP_slot_import.csv remains absent"),
        ("CG1444_4_no_zero", "C_parent_WEP=0 is not theorem-certified"),
        ("CG1444_5_no_score", "no WEP/local-GR/Newton score is allowed from 1444"),
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
            "decision_id": "DEC1444_0_extract_official_facts",
            "decision": "promote only eta formula/channel and X-axis facts into a partial nonclaim product row",
            "why": "these facts are source-backed, but not enough to define K_CMSM sign/units or source projection",
            "consequence": "product target improves but still refuses scoring",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1444_1_start_C_parent_theorem_search",
            "decision": "record C_parent theorem/source routes without creating an import",
            "why": "a closure-only zero or bound-inverted coefficient would be circular",
            "consequence": "C_parent remains the decisive missing coupling slot",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1444_2_next_readout_first",
            "decision": "make K_CMSM/readout extraction the next empirical target",
            "why": "it can close sign/units/orbit-mask parts of the product convention without inventing theory",
            "consequence": "1445 should hunt official readout/design matrix or explicitly leave it blocked",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1444_0_1445",
            "next_target": "1445-Y5-R10-RAB-K-CMSM-readout-extraction-or-C-parent-coupling-theorem.md",
            "script": "scripts/Y5_R10_RAB_K_CMSM_readout_extraction_or_C_parent_coupling_theorem.py",
            "objective": "try to extract official K_CMSM/readout sign, units, axis orientation, segment masks, and orbit weighting; in parallel state the parent coupling theorem requirements for C_parent_WEP without importing a coefficient.",
            "include": "official readout/design matrix source audit; K_CMSM schema gate; C_parent coupling theorem clauses; parser dry-run; no-claim gates",
            "exclude": "numeric WEP score; local-GR claim; invented coefficient; bound-inverted C_parent; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_live_files(product: list[dict[str, Any]], extraction: list[dict[str, Any]], c_parent: list[dict[str, Any]]) -> None:
    write_csv(LIVE_PRODUCT_TARGET, product)
    write_csv(BRANCH_PRODUCT_AUDIT, extraction)
    write_csv(BRANCH_C_PARENT_SEARCH, c_parent)


def validation_rows(
    sources: list[dict[str, Any]],
    product: list[dict[str, Any]],
    extraction: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    refresh: list[dict[str, Any]],
    c_parent: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated = [
        SOURCE_REGISTER,
        OFFICIAL_EXTRACTION,
        PRODUCT_PROMOTION_AUDIT,
        SOURCE_PACK_REFRESH,
        C_PARENT_THEOREM_SEARCH,
        PARSER_DRYRUN,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        LIVE_PRODUCT_TARGET,
        BRANCH_PRODUCT_AUDIT,
        BRANCH_C_PARENT_SEARCH,
    ]
    all_sources_resolve = all(row["resolved"] for row in sources)
    product_pending = contains_pending(product[0])
    extracted_some_official = any(row["extraction_status"] == "OFFICIAL_EXTRACTED" for row in extraction)
    all_promotions_false = all(str(row["promote_to_claim_allowed"]) == "False" for row in promotion)
    any_missing_pack = any(row["current_status"] == "MISSING_REQUIRED_FILE" for row in refresh)
    c_parent_no_import = not LIVE_C_PARENT_IMPORT.exists() and all(str(row["valid_for_claim"]) == "False" for row in c_parent)
    dryrun_refuses = all(str(row["claim_allowed"]) == "False" for row in dryrun)
    gates_false = all(str(row["claim_allowed"]) == "False" for row in gates)
    csvs_parse = all(csv_parses(path) for path in generated)
    formalization_recent = 0
    if FORMALIZATION.exists():
        formalization_recent = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)
    checks = [
        ("VAL1444_0_source_register", all_sources_resolve, "all local sources exist and web source strings are recorded"),
        ("VAL1444_1_official_extraction", extracted_some_official, "official eta/channel facts extracted from MICROSCOPE sources"),
        ("VAL1444_2_product_pending", product_pending, "product row still contains pending fields and remains nonclaim"),
        ("VAL1444_3_promotion_false", all_promotions_false, "promotion audit refuses claim promotion"),
        ("VAL1444_4_source_pack_incomplete", any_missing_pack, "source-pack refresh still exposes missing required files"),
        ("VAL1444_5_C_parent_no_import", c_parent_no_import, "C_parent theorem/source search did not create a live import"),
        ("VAL1444_6_dryrun_refuses", dryrun_refuses, "parser dry-run refuses score paths"),
        ("VAL1444_7_claim_gates", gates_false, "all claim gates remain false"),
        ("VAL1444_8_csv_parse", csvs_parse, "all generated 1444 CSVs parse cleanly"),
        ("VAL1444_9_formalization_untouched", formalization_recent == 0, f"formalization modified-file count since start={formalization_recent}"),
        ("VAL1444_10_next_target", True, "1445 handoff written"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1444_11_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1444 extracts official product facts but keeps WEP/local claims blocked",
            "generated_utc": now(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    extraction: list[dict[str, Any]],
    product: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    refresh: list[dict[str, Any]],
    c_parent: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1444 - Product convention official extraction or C_parent theorem/source search\n\n")
        handle.write(
            "**Current verdict:** official MICROSCOPE sources let us promote the eta formula, Ti/Pt channel, "
            "SUEP material order, and X-axis analysis facts into the product row. They do **not** yet supply "
            "the full K_CMSM sign/units, source-kernel units, or reproducible segment/orbit mask needed for a "
            "WEP score. `C_parent_WEP` remains absent and no zero theorem is certified.\n"
        )
        write_markdown_table(handle, "Source register", sources)
        write_markdown_table(handle, "Official product extraction", extraction)
        write_markdown_table(handle, "Live product row", product)
        write_markdown_table(handle, "Product promotion audit", promotion)
        write_markdown_table(handle, "Source-pack status refresh", refresh)
        write_markdown_table(handle, "C_parent theorem/source search", c_parent)
        write_markdown_table(handle, "Parser dry-run", dryrun)
        write_markdown_table(handle, "Claim gates", gates)
        write_markdown_table(handle, "Decision ledger", decisions)
        write_markdown_table(handle, "Validation", validation)
        write_markdown_table(handle, "Next target", next_rows)


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def main() -> None:
    sources = source_register_rows()
    extraction = official_extraction_rows()
    product = product_row()
    promotion = promotion_audit_rows(extraction, product)
    refresh = source_pack_refresh_rows(product)
    c_parent = c_parent_theorem_search_rows()
    dryrun = parser_dryrun_rows(product, refresh)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_live_files(product, extraction, c_parent)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(OFFICIAL_EXTRACTION, extraction)
    write_csv(PRODUCT_PROMOTION_AUDIT, promotion)
    write_csv(SOURCE_PACK_REFRESH, refresh)
    write_csv(C_PARENT_THEOREM_SEARCH, c_parent)
    write_csv(PARSER_DRYRUN, dryrun)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validation = validation_rows(sources, product, extraction, promotion, refresh, c_parent, dryrun, gates)
    write_csv(VALIDATION, validation)
    write_doc(
        sources,
        extraction,
        product,
        promotion,
        refresh,
        c_parent,
        dryrun,
        gates,
        decisions,
        validation,
        next_rows,
    )
    remove_pycache()
    print("Y5_R10_1444_product_official_partial_extraction_C_parent_search_blocked")


if __name__ == "__main__":
    main()
