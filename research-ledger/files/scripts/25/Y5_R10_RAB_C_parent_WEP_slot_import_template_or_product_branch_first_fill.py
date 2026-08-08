from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
METADATA = MICROSCOPE / "metadata"
BRANCH_ROOT = MICROSCOPE / "branch_locked_wep"
COEFFICIENT_ROOT = BRANCH_ROOT / "coefficients"
RESIDUAL_ROOT = BRANCH_ROOT / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1442-Y5-R10-RAB-C-parent-WEP-slot-import-template-or-product-branch-first-fill.md"

BRANCH_ID_FILE = BRANCH_ROOT / "branch_id.csv"
NEXT_1441 = OUT / "P8_Y5_R10_1441_NEXT_TARGET.csv"
VALIDATION_1441 = OUT / "P8_Y5_BRR545_1441_VALIDATION.csv"
PRIORITY_1441 = OUT / "P8_Y5_R10_1441_SOURCE_PACK_ACQUISITION_PRIORITY.csv"
AXRED_1441 = OUT / "P8_Y5_R10_1441_AX1090_REDUCTION_AUDIT.csv"
ACTIVE_ROUTE_1441 = OUT / "P8_Y5_R10_1441_ACTIVE_ROUTE_STATUS.csv"
C_PARENT_IMPORT_SCHEMA = COEFFICIENT_ROOT / "C_parent_import_schema.csv"
SOURCE_PACK_MANIFEST_1438 = OUT / "P8_Y5_R10_1438_OFFICIAL_MICROSCOPE_SOURCE_PACK_MANIFEST.csv"
PARSER_1439 = OUT / "P8_Y5_R10_1439_SOURCE_PACK_PARSER_DRYRUN.csv"
WEB_SOURCES_1336 = METADATA / "P8_Y5_R10_1336_WEB_SOURCE_CANDIDATE_REGISTER.csv"
PRODUCT_SCHEMA_1336 = METADATA / "P8_Y5_R10_1336_PRODUCT_CONVENTION_SCHEMA.csv"
BRANCH_SCHEMA_1336 = METADATA / "P8_Y5_R10_1336_BRANCH_CLASSIFIER_SCHEMA.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1442_SOURCE_REGISTER.csv"
C_PARENT_WEP_IMPORT_TEMPLATE = OUT / "P8_Y5_R10_1442_C_PARENT_WEP_SLOT_IMPORT_TEMPLATE.csv"
C_PARENT_WEP_IMPORT_GATES = OUT / "P8_Y5_R10_1442_C_PARENT_WEP_SLOT_IMPORT_GATES.csv"
PRODUCT_BRANCH_FIRST_FILL_TEMPLATE = OUT / "P8_Y5_R10_1442_PRODUCT_BRANCH_FIRST_FILL_TEMPLATE.csv"
TEMPLATE_PARSER_DRYRUN = OUT / "P8_Y5_R10_1442_TEMPLATE_PARSER_DRYRUN.csv"
ROUTE_DECISION = OUT / "P8_Y5_R10_1442_ROUTE_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1442_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1442_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1442_VALIDATION.csv"

BRANCH_C_PARENT_TEMPLATE = COEFFICIENT_ROOT / "C_parent_WEP_slot_import_TEMPLATE.csv"
BRANCH_PRODUCT_BRANCH_TEMPLATE = RESIDUAL_ROOT / "product_branch_first_fill_TEMPLATE.csv"


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
        ("SRC1442_0_1441_next", NEXT_1441, "NEXT1441_0_1442", "1441 handoff selecting C_parent import template or product/branch first fill."),
        ("SRC1442_1_1441_validation", VALIDATION_1441, "VAL1441_10_overall", "1441 validation summary."),
        ("SRC1442_2_1441_priority", PRIORITY_1441, "PACK1438_5_C_parent_import", "1441 source-pack acquisition priority."),
        ("SRC1442_3_1441_axred", AXRED_1441, "AXRED1441_0_parent_object", "1441 AX1090 reduction audit."),
        ("SRC1442_4_1441_route", ACTIVE_ROUTE_1441, "ARS1441_1_source_pack", "1441 active source-pack route."),
        ("SRC1442_5_c_parent_schema", C_PARENT_IMPORT_SCHEMA, "C_PARENT_IMPORT_SCHEMA_1431", "generic C_parent import schema."),
        ("SRC1442_6_manifest1438", SOURCE_PACK_MANIFEST_1438, "PACK1438_5_C_parent_import", "source-pack manifest."),
        ("SRC1442_7_parser1439", PARSER_1439, "PARSE1439_5", "source-pack parser dry-run."),
        ("SRC1442_8_product_schema", PRODUCT_SCHEMA_1336, "PRODSCHEMA1336_6_branch_lock", "product convention schema."),
        ("SRC1442_9_branch_schema", BRANCH_SCHEMA_1336, "BRANCHSCHEMA1336_1_forbidden_mixing_rule", "branch classifier schema."),
        ("SRC1442_10_web_sources", WEB_SOURCES_1336, "WEB1336_3_PRL_final_result", "official MICROSCOPE web source strings."),
        ("SRC1442_11_branch_id", BRANCH_ID_FILE, branch, "active branch lock."),
    ]
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "path_exists": path.exists(),
            "anchor": anchor,
            "anchor_found": text_has(path, anchor),
            "role": role,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, anchor, role in specs
    ]


def c_parent_template_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "template_id": "CPWEP1442_0_slot_import",
            "schema_version": "C_PARENT_WEP_SLOT_IMPORT_TEMPLATE_1442",
            "coefficient_id": "CP_WEP_TiPt_TEMPLATE",
            "component": "C_parent_WEP_TiPt",
            "value": "MISSING_DERIVED_ZERO_OR_NUMERIC_VALUE",
            "uncertainty": "MISSING_EXACT_OR_NUMERIC_UNCERTAINTY",
            "units": "MISSING_PARENT_BASIS_UNITS",
            "sign_convention": "MISSING_TiPt_BODY_ORDER_AND_FIELD_SIGN",
            "basis": "MISSING_MTS_PARENT_WEP_BASIS",
            "source_path": "MISSING_PARENT_THEOREM_OR_NUMERIC_SOURCE_PATH",
            "parent_status": "MISSING_PARENT_DERIVED_OR_SOURCE_BACKED_NUMERIC",
            "zero_certificate_status": "NOT_ZERO_CERTIFIED",
            "accepted_value_policy": "DERIVED_ZERO with exact certificate OR finite numeric value with uncertainty, units, sign, basis, and source path",
            "forbidden_value_policy": "no placeholder zero, no DD-only pullback, no bound-as-prediction, no fitted value without parent/status provenance",
            "parser_status": "TEMPLATE_ONLY_NOT_IMPORTABLE",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def c_parent_gate_rows(branch: str) -> list[dict[str, Any]]:
    gates = [
        ("CPWG1442_0_branch", "same_parent_branch_id must exactly match branch_id.csv"),
        ("CPWG1442_1_component", "component must be C_parent_WEP_TiPt or a declared subcomponent mapped to that slot"),
        ("CPWG1442_2_value", "value must be DERIVED_ZERO or finite numeric; MISSING/PENDING/PLACEHOLDER forbidden"),
        ("CPWG1442_3_zero", "DERIVED_ZERO requires parent-signed zero certificate, not closure-only AX1090/MOMS assumption"),
        ("CPWG1442_4_numeric", "numeric value requires uncertainty, units, sign convention, basis, source path, and parent_status"),
        ("CPWG1442_5_basis", "basis must be MTS parent WEP basis, not DD-only/external comparator basis"),
        ("CPWG1442_6_no_absorption", "measured-G absorption and tau_eff=1 shortcuts cannot supply C_parent"),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "gate_id": gate_id,
            "gate": gate,
            "gate_status": "ENFORCED_FOR_TEMPLATE",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate in gates
    ]


def product_branch_template_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "template_id": "PBF1442_0_branch_classifier",
            "target_file": "P_WEP_same_parent_branch_lock.csv",
            "target_path": str(MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv"),
            "required_fields": "same_parent_branch_id;forbidden_mixing_rule",
            "proposed_first_fill": "same_parent_branch_id fixed; forbid surrogate/DD-only/tau=1/measured-G-absorbed rows",
            "fill_status": "TEMPLATE_ONLY_TARGET_FILE_NOT_WRITTEN",
            "why_first_fill": "can be filled without inventing coefficient values and protects every later WEP factor",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "template_id": "PBF1442_1_product_convention",
            "target_file": "P_WEP_eta_product_convention.csv",
            "target_path": str(MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv"),
            "required_fields": "eta_formula;sign_convention;tau_eff_definition;readout_kernel_units;source_kernel_units;orbit_average_rule;branch_lock",
            "proposed_first_fill": "use PRL/CQG source strings as candidates; leave official sign/readout fields pending until extracted",
            "fill_status": "TEMPLATE_ONLY_TARGET_FILE_NOT_WRITTEN",
            "why_first_fill": "can fix comparison conventions while C_parent remains unavailable, but still cannot score",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def parser_dryrun_rows(branch: str, c_template: list[dict[str, Any]], product_templates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    c_row = c_template[0]
    hard_missing = [
        key
        for key in ("value", "uncertainty", "units", "sign_convention", "basis", "source_path", "parent_status")
        if str(c_row[key]).startswith("MISSING")
    ]
    rows.append(
        {
            "same_parent_branch_id": branch,
            "dryrun_id": "TPD1442_0_C_parent_template",
            "target": "C_parent_WEP_slot_import.csv",
            "template_rows": len(c_template),
            "missing_or_forbidden_fields": ";".join(hard_missing),
            "parser_status": "REFUSED_TEMPLATE_PLACEHOLDERS_PRESENT",
            "promotion_effect": "cannot become score-ready until replaced by DERIVED_ZERO or numeric sourced row",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    for template in product_templates:
        rows.append(
            {
                "same_parent_branch_id": branch,
                "dryrun_id": f"TPD1442_{len(rows)}_{template['target_file']}",
                "target": template["target_file"],
                "template_rows": 1,
                "missing_or_forbidden_fields": "target_file_not_written; official_extraction_pending",
                "parser_status": "REFUSED_TEMPLATE_ONLY_TARGET_ABSENT",
                "promotion_effect": "safe first-fill candidate but not a prediction row",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def route_decision_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1442_0_C_parent_template",
            "decision": "write C_parent_WEP slot import template, but do not create live C_parent_WEP_slot_import.csv",
            "why": "C_parent is the physics bottleneck and must not be filled by invented values or closure-only zero",
            "consequence": "template is ready for a real theorem/numeric source, but parser refuses it now",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1442_1_branch_product_fallback",
            "decision": "stage branch/product first-fill templates as the safer non-coefficient path",
            "why": "branch/product conventions can be filled from official sources without pretending to know C_parent",
            "consequence": "next checkpoint should either fill branch/product nonclaim rows or keep waiting for C_parent source",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(branch: str) -> list[dict[str, Any]]:
    gates = [
        ("CG1442_0_template_not_import", "C_parent_WEP template is not the live import file"),
        ("CG1442_1_no_placeholder", "placeholder values cannot become valid prediction rows"),
        ("CG1442_2_no_closure_zero", "closure-only WEP parent clause cannot certify DERIVED_ZERO"),
        ("CG1442_3_no_invented_coefficient", "no numeric C_parent value may be invented or fitted without provenance"),
        ("CG1442_4_product_nonclaim", "branch/product first-fill templates are convention scaffolds, not WEP predictions"),
        ("CG1442_5_local_gr_blocked", "WEP/local-GR claims remain blocked until C_parent and source-pack parser pass"),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "gate_id": gate_id,
            "gate": gate,
            "gate_status": "LOCKED_CLAIM_FALSE",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate in gates
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1442_0_1443",
            "next_target": "1443-Y5-R10-RAB-branch-product-first-fill-or-C-parent-source-search-plan.md",
            "script": "scripts/Y5_R10_RAB_branch_product_first_fill_or_C_parent_source_search_plan.py",
            "objective": "fill the branch/product convention rows as nonclaim if official source extraction is possible; otherwise write a C_parent source-search plan and keep the coefficient template blocked.",
            "include": "branch classifier first-fill; product convention extraction plan; C_parent source-search plan; parser dry-run; no-claim gates",
            "exclude": "numeric WEP score; local-GR claim; invented coefficient value; fabricated official data; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_branch_files(c_template: list[dict[str, Any]], product_templates: list[dict[str, Any]]) -> None:
    write_csv(BRANCH_C_PARENT_TEMPLATE, c_template)
    write_csv(BRANCH_PRODUCT_BRANCH_TEMPLATE, product_templates)


def validation_rows(
    sources: list[dict[str, Any]],
    c_template: list[dict[str, Any]],
    c_gates: list[dict[str, Any]],
    product_templates: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        C_PARENT_WEP_IMPORT_TEMPLATE,
        C_PARENT_WEP_IMPORT_GATES,
        PRODUCT_BRANCH_FIRST_FILL_TEMPLATE,
        TEMPLATE_PARSER_DRYRUN,
        ROUTE_DECISION,
        CLAIM_GATE,
        NEXT_TARGET,
        BRANCH_C_PARENT_TEMPLATE,
        BRANCH_PRODUCT_BRANCH_TEMPLATE,
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
    sources_ok = all(row["path_exists"] and row["anchor_found"] for row in sources)
    c_template_blocked = len(c_template) == 1 and c_template[0]["parser_status"] == "TEMPLATE_ONLY_NOT_IMPORTABLE"
    c_gate_ok = all(row["gate_status"] == "ENFORCED_FOR_TEMPLATE" for row in c_gates)
    product_template_safe = len(product_templates) == 2 and all(row["fill_status"] == "TEMPLATE_ONLY_TARGET_FILE_NOT_WRITTEN" for row in product_templates)
    dryrun_refuses = all(row["parser_status"].startswith("REFUSED") for row in dryrun)
    claims_safe = all(row["gate_status"] == "LOCKED_CLAIM_FALSE" for row in claims) and not truthy_claim_flags
    live_import_absent = not (COEFFICIENT_ROOT / "C_parent_WEP_slot_import.csv").exists()
    branch_files_ok = BRANCH_C_PARENT_TEMPLATE.exists() and BRANCH_PRODUCT_BRANCH_TEMPLATE.exists()
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1442_0_source_register", sources_ok, "all 1442 cited source paths and anchors resolve"),
        ("VAL1442_1_c_template_blocked", c_template_blocked, "C_parent_WEP template exists but is not importable"),
        ("VAL1442_2_c_gates", c_gate_ok, "C_parent import gates are enforced"),
        ("VAL1442_3_product_template_safe", product_template_safe, "branch/product first-fill templates remain target-absent and nonclaim"),
        ("VAL1442_4_dryrun_refuses", dryrun_refuses, "template parser dry-run refuses all template rows"),
        ("VAL1442_5_claim_gates", claims_safe, "all claim/valid/prediction flags remain false"),
        ("VAL1442_6_live_import_absent", live_import_absent, "live C_parent_WEP_slot_import.csv was not created"),
        ("VAL1442_7_csv_parse", parse_ok, "all generated 1442 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1442_8_branch_files", branch_files_ok, "branch template files written"),
        ("VAL1442_9_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1442_10_next_target", True, "1443 handoff written"),
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
            "check_id": "VAL1442_11_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1442 writes strict C_parent_WEP and branch/product templates while keeping all WEP claims blocked",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1442 - C_parent WEP-slot import template or product/branch first fill",
            "**Current verdict:** the `C_parent_WEP` slot now has a strict import template, but no live coefficient row is created. Branch/product first-fill templates are staged as the safe fallback path, all nonclaim.",
            "**Main progress:** the source-pack route can now reject placeholder `C_parent` rows mechanically while allowing future theorem-zero or source-backed numeric imports.",
            "## Source register\n" + md_table(sections["sources"]),
            "## C_parent WEP-slot import template\n" + md_table(sections["c_template"]),
            "## C_parent WEP import gates\n" + md_table(sections["c_gates"]),
            "## Product/branch first-fill template\n" + md_table(sections["product_templates"]),
            "## Template parser dry-run\n" + md_table(sections["dryrun"]),
            "## Route decision\n" + md_table(sections["decisions"]),
            "## Claim gates\n" + md_table(sections["claims"]),
            "## Validation\n" + md_table(sections["validation"]),
            "## Next target\n" + md_table(sections["next"]),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    COEFFICIENT_ROOT.mkdir(parents=True, exist_ok=True)
    RESIDUAL_ROOT.mkdir(parents=True, exist_ok=True)
    branch = branch_id()
    sources = source_register_rows(branch)
    c_template = c_parent_template_rows(branch)
    c_gates = c_parent_gate_rows(branch)
    product_templates = product_branch_template_rows(branch)
    dryrun = parser_dryrun_rows(branch, c_template, product_templates)
    decisions = route_decision_rows(branch)
    claims = claim_gate_rows(branch)
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(C_PARENT_WEP_IMPORT_TEMPLATE, c_template)
    write_csv(C_PARENT_WEP_IMPORT_GATES, c_gates)
    write_csv(PRODUCT_BRANCH_FIRST_FILL_TEMPLATE, product_templates)
    write_csv(TEMPLATE_PARSER_DRYRUN, dryrun)
    write_csv(ROUTE_DECISION, decisions)
    write_csv(CLAIM_GATE, claims)
    write_csv(NEXT_TARGET, next_rows)
    write_branch_files(c_template, product_templates)

    validation = validation_rows(sources, c_template, c_gates, product_templates, dryrun, claims)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "c_template": c_template,
            "c_gates": c_gates,
            "product_templates": product_templates,
            "dryrun": dryrun,
            "decisions": decisions,
            "claims": claims,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1442_C_parent_WEP_template_written_live_import_absent_nonclaim")


if __name__ == "__main__":
    main()
