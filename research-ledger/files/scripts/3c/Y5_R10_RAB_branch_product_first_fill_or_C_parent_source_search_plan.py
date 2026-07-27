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
PRODUCT_ROOT = BRANCH_ROOT / "product"
GUARD_ROOT = BRANCH_ROOT / "guards"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1443-Y5-R10-RAB-branch-product-first-fill-or-C-parent-source-search-plan.md"

BRANCH_ID_FILE = BRANCH_ROOT / "branch_id.csv"
NEXT_1442 = OUT / "P8_Y5_R10_1442_NEXT_TARGET.csv"
VALIDATION_1442 = OUT / "P8_Y5_BRR545_1442_VALIDATION.csv"
C_TEMPLATE_1442 = OUT / "P8_Y5_R10_1442_C_PARENT_WEP_SLOT_IMPORT_TEMPLATE.csv"
PRODUCT_BRANCH_TEMPLATE_1442 = OUT / "P8_Y5_R10_1442_PRODUCT_BRANCH_FIRST_FILL_TEMPLATE.csv"
C_GATES_1442 = OUT / "P8_Y5_R10_1442_C_PARENT_WEP_SLOT_IMPORT_GATES.csv"
BRANCH_SCHEMA_1336 = METADATA / "P8_Y5_R10_1336_BRANCH_CLASSIFIER_SCHEMA.csv"
PRODUCT_SCHEMA_1336 = METADATA / "P8_Y5_R10_1336_PRODUCT_CONVENTION_SCHEMA.csv"
WEB_SOURCES_1336 = METADATA / "P8_Y5_R10_1336_WEB_SOURCE_CANDIDATE_REGISTER.csv"
ETA_GUARD_1429 = PRODUCT_ROOT / "eta_product_convention.csv"
MEASURED_G_GUARD = GUARD_ROOT / "measured_G_guard.csv"
BRANCH_C_TEMPLATE_1442 = COEFFICIENT_ROOT / "C_parent_WEP_slot_import_TEMPLATE.csv"

BRANCH_CLASSIFIER_TARGET = MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv"
PRODUCT_CONVENTION_TARGET = MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv"
LIVE_C_PARENT_IMPORT = COEFFICIENT_ROOT / "C_parent_WEP_slot_import.csv"
C_PARENT_SOURCE_SEARCH_PLAN_BRANCH = COEFFICIENT_ROOT / "C_parent_WEP_source_search_plan.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1443_SOURCE_REGISTER.csv"
BRANCH_CLASSIFIER_FIRST_FILL = OUT / "P8_Y5_R10_1443_BRANCH_CLASSIFIER_FIRST_FILL.csv"
PRODUCT_CONVENTION_FIRST_FILL = OUT / "P8_Y5_R10_1443_PRODUCT_CONVENTION_FIRST_FILL.csv"
C_PARENT_SOURCE_SEARCH_PLAN = OUT / "P8_Y5_R10_1443_C_PARENT_SOURCE_SEARCH_PLAN.csv"
FIRST_FILL_PARSER_DRYRUN = OUT / "P8_Y5_R10_1443_FIRST_FILL_PARSER_DRYRUN.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1443_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1443_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1443_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1443_VALIDATION.csv"


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
        ("SRC1443_0_1442_next", NEXT_1442, "NEXT1442_0_1443", "1442 handoff selecting branch/product fill or C_parent search plan."),
        ("SRC1443_1_1442_validation", VALIDATION_1442, "VAL1442_11_overall", "1442 validation summary."),
        ("SRC1443_2_1442_c_template", C_TEMPLATE_1442, "CPWEP1442_0_slot_import", "1442 C_parent WEP template."),
        ("SRC1443_3_1442_branch_product_template", PRODUCT_BRANCH_TEMPLATE_1442, "PBF1442_1_product_convention", "1442 product/branch template."),
        ("SRC1443_4_1442_c_gates", C_GATES_1442, "CPWG1442_5_basis", "1442 C_parent import gates."),
        ("SRC1443_5_branch_schema", BRANCH_SCHEMA_1336, "BRANCHSCHEMA1336_1_forbidden_mixing_rule", "branch classifier schema."),
        ("SRC1443_6_product_schema", PRODUCT_SCHEMA_1336, "PRODSCHEMA1336_6_branch_lock", "product convention schema."),
        ("SRC1443_7_web_sources", WEB_SOURCES_1336, "WEB1336_3_PRL_final_result", "official source strings."),
        ("SRC1443_8_eta_guard", ETA_GUARD_1429, "tau_eff = branch_locked_orbit_average", "existing eta product guard."),
        ("SRC1443_9_measured_G_guard", MEASURED_G_GUARD, "MGG1429_0_no_relative_absorption", "measured-G guard."),
        ("SRC1443_10_branch_id", BRANCH_ID_FILE, branch, "active branch id."),
        ("SRC1443_11_branch_c_template", BRANCH_C_TEMPLATE_1442, "CPWEP1442_0_slot_import", "branch C_parent template copy."),
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


def branch_classifier_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "forbidden_mixing_rule": "refuse any WEP product unless C_parent_WEP, R_material, R_source, K_CMSM, product convention, measured_G_guard, and eta bound all declare this same_parent_branch_id; refuse surrogate, DD-only, tau_eff=1, measured-G-absorbed, bound-as-prediction, or mixed-basis rows",
            "source_path": str(DOC),
            "row_status": "BRANCH_CLASSIFIER_FIRST_FILL_NONCLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def product_convention_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "eta_formula": "eta_AB = 2(a_A - a_B)/(a_A + a_B); candidate convention from existing guard, official Ti/Pt body order still pending",
            "sign_convention": "PENDING_OFFICIAL_TiPt_BODY_ORDER_AND_SENSITIVE_AXIS_SIGN",
            "tau_eff_definition": "tau_eff = branch_locked_orbit_average(K_CMSM * R_source * readout_mask); tau_eff=1 forbidden",
            "readout_kernel_units": "PENDING_OFFICIAL_K_CMSM_UNITS",
            "source_kernel_units": "PENDING_PARENT_SOURCE_BASIS_UNITS",
            "orbit_average_rule": "PENDING_OFFICIAL_SESSION_MASK_OR_REPRODUCIBLE_CQG_ORBIT_WEIGHTING",
            "branch_lock": branch,
            "source_path": str(DOC),
            "row_status": "PRODUCT_CONVENTION_PARTIAL_FIRST_FILL_NONCLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def c_parent_search_rows(branch: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CPS1443_0_parent_zero",
            "derive DERIVED_ZERO",
            "single parent action proves C_parent_WEP_TiPt=0",
            "AX1090/MOMS proof obligations currently closure-only",
            "BLOCKED_THEOREM_ROUTE",
            "do not use closure-only zero as import",
        ),
        (
            "CPS1443_1_parent_numeric",
            "derive/source numeric coefficient",
            "parent action or source-backed coefficient row gives finite C_parent_WEP_TiPt with units/sign/basis",
            "no current source-backed numeric row",
            "OPEN_SOURCE_SEARCH",
            "search parent action/coupling ledgers before any empirical fit",
        ),
        (
            "CPS1443_2_bound_inversion_forbidden",
            "forbidden shortcut",
            "choose C_parent from MICROSCOPE bound or set it to zero by fit",
            "would be bound-as-prediction and circular",
            "FORBIDDEN",
            "never import as C_parent source",
        ),
        (
            "CPS1443_3_DD_proxy_forbidden",
            "forbidden shortcut",
            "use Damour-Donoghue or material-smoke coefficient as MTS C_parent",
            "external comparator basis only",
            "FORBIDDEN",
            "may inform material tensor but not parent coefficient",
        ),
        (
            "CPS1443_4_finite_route",
            "finite nonclaim route",
            "if no theorem/numeric C_parent exists, keep source-pack acquisition and later bounded-coefficient rows nonclaim",
            "requires branch/product/readout/material/source rows first",
            "OPEN_NONCLAIM_ROUTE",
            "build parser-ready inputs before any comparison",
        ),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "search_id": search_id,
            "route": route,
            "required_evidence": required_evidence,
            "current_obstruction": obstruction,
            "route_status": status,
            "next_action": next_action,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for search_id, route, required_evidence, obstruction, status, next_action in specs
    ]


def parser_dryrun_rows(branch: str, branch_rows: list[dict[str, Any]], product_rows: list[dict[str, Any]], search_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    product_row = product_rows[0]
    pending_fields = [key for key, value in product_row.items() if str(value).startswith("PENDING")]
    return [
        {
            "same_parent_branch_id": branch,
            "dryrun_id": "PDR1443_0_branch_classifier",
            "target_path": str(BRANCH_CLASSIFIER_TARGET),
            "target_exists": BRANCH_CLASSIFIER_TARGET.exists(),
            "row_count": len(branch_rows),
            "parser_status": "PASS_GUARD_ROW_NONCLAIM",
            "refusal_reason": "not a prediction row; only forbids mixed inputs",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "dryrun_id": "PDR1443_1_product_convention",
            "target_path": str(PRODUCT_CONVENTION_TARGET),
            "target_exists": PRODUCT_CONVENTION_TARGET.exists(),
            "row_count": len(product_rows),
            "parser_status": "REFUSED_PENDING_OFFICIAL_FIELDS",
            "refusal_reason": ";".join(pending_fields),
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "dryrun_id": "PDR1443_2_C_parent_search",
            "target_path": str(LIVE_C_PARENT_IMPORT),
            "target_exists": LIVE_C_PARENT_IMPORT.exists(),
            "row_count": len(search_rows),
            "parser_status": "REFUSED_LIVE_C_PARENT_IMPORT_ABSENT",
            "refusal_reason": "C_parent_WEP source-search plan exists, but no live coefficient import row exists",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(branch: str) -> list[dict[str, Any]]:
    gates = [
        ("CG1443_0_branch_guard_not_prediction", "branch classifier is a guard, not a WEP prediction"),
        ("CG1443_1_product_pending", "product convention has pending official sign/readout/source fields"),
        ("CG1443_2_C_parent_absent", "live C_parent_WEP_slot_import.csv remains absent"),
        ("CG1443_3_no_bound_inversion", "MICROSCOPE bound cannot be inverted into C_parent"),
        ("CG1443_4_no_DD_proxy", "DD/material-smoke rows cannot stand in for MTS parent coefficient"),
        ("CG1443_5_no_score", "no WEP/local-GR/Newton claim is allowed from first-fill convention rows"),
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


def decision_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1443_0_fill_branch",
            "decision": "write live branch classifier guard row",
            "why": "it protects all later WEP factors from mixed-basis/surrogate shortcuts without inventing physics",
            "consequence": "branch guard can pass as nonclaim scaffold",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1443_1_partial_product",
            "decision": "write live product convention partial row with pending official fields",
            "why": "eta formula and tau guard can be staged, but official sign/readout/source units must remain pending",
            "consequence": "product row exists but parser refuses score",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1443_2_C_parent_plan",
            "decision": "write C_parent source-search plan and keep live import absent",
            "why": "the coefficient remains the physics bottleneck and cannot be inferred from a bound or proxy",
            "consequence": "next work should extract official product fields or begin C_parent theorem/source search",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1443_0_1444",
            "next_target": "1444-Y5-R10-RAB-product-convention-official-extraction-or-C-parent-theorem-source-search.md",
            "script": "scripts/Y5_R10_RAB_product_convention_official_extraction_or_C_parent_theorem_source_search.py",
            "objective": "attempt official product-convention extraction for sign/readout/source-unit fields; if unavailable, start the C_parent theorem/source search ledger without creating a coefficient.",
            "include": "official product field extraction; C_parent theorem/source search; parser dry-run; no-claim gates",
            "exclude": "numeric WEP score; local-GR claim; invented coefficient; fabricated official data; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_live_files(branch_rows: list[dict[str, Any]], product_rows: list[dict[str, Any]], search_rows: list[dict[str, Any]]) -> None:
    write_csv(BRANCH_CLASSIFIER_TARGET, branch_rows)
    write_csv(PRODUCT_CONVENTION_TARGET, product_rows)
    write_csv(C_PARENT_SOURCE_SEARCH_PLAN_BRANCH, search_rows)


def validation_rows(
    sources: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    product_rows: list[dict[str, Any]],
    search_rows: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        BRANCH_CLASSIFIER_FIRST_FILL,
        PRODUCT_CONVENTION_FIRST_FILL,
        C_PARENT_SOURCE_SEARCH_PLAN,
        FIRST_FILL_PARSER_DRYRUN,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        BRANCH_CLASSIFIER_TARGET,
        PRODUCT_CONVENTION_TARGET,
        C_PARENT_SOURCE_SEARCH_PLAN_BRANCH,
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
    branch_written = BRANCH_CLASSIFIER_TARGET.exists() and len(branch_rows) == 1
    product_written_pending = PRODUCT_CONVENTION_TARGET.exists() and len(product_rows) == 1 and any(
        str(value).startswith("PENDING") for value in product_rows[0].values()
    )
    search_written = C_PARENT_SOURCE_SEARCH_PLAN_BRANCH.exists() and len(search_rows) >= 5
    dryrun_safe = any(row["parser_status"] == "PASS_GUARD_ROW_NONCLAIM" for row in dryrun) and all(
        row["valid_prediction_row"] is False for row in dryrun
    )
    claims_safe = all(row["gate_status"] == "LOCKED_CLAIM_FALSE" for row in gates) and not truthy_claim_flags
    live_import_absent = not LIVE_C_PARENT_IMPORT.exists()
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1443_0_source_register", sources_ok, "all 1443 cited source paths and anchors resolve"),
        ("VAL1443_1_branch_written", branch_written, "live branch classifier guard row written"),
        ("VAL1443_2_product_pending", product_written_pending, "product convention row written but official fields remain pending"),
        ("VAL1443_3_search_written", search_written, "C_parent source-search plan written"),
        ("VAL1443_4_dryrun_safe", dryrun_safe, "parser passes branch guard only as nonclaim and refuses score elsewhere"),
        ("VAL1443_5_claim_gates", claims_safe, "all claim/valid/prediction flags remain false"),
        ("VAL1443_6_live_import_absent", live_import_absent, "live C_parent_WEP_slot_import.csv remains absent"),
        ("VAL1443_7_csv_parse", parse_ok, "all generated 1443 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1443_8_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1443_9_next_target", True, "1444 handoff written"),
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
            "check_id": "VAL1443_10_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1443 fills branch/product guard rows as nonclaim and keeps C_parent import blocked",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1443 - Branch/product first fill or C_parent source-search plan",
            "**Current verdict:** the branch classifier guard is now filled as a live nonclaim row. The product convention row is partially filled but still pending official sign/readout/source-unit extraction. `C_parent_WEP` remains absent.",
            "**Main progress:** the WEP source-pack route now has live branch/product guard files plus a C_parent source-search plan, while the coefficient and WEP score remain blocked.",
            "## Source register\n" + md_table(sections["sources"]),
            "## Branch classifier first fill\n" + md_table(sections["branch_rows"]),
            "## Product convention first fill\n" + md_table(sections["product_rows"]),
            "## C_parent source-search plan\n" + md_table(sections["search_rows"]),
            "## First-fill parser dry-run\n" + md_table(sections["dryrun"]),
            "## Claim gates\n" + md_table(sections["gates"]),
            "## Decision ledger\n" + md_table(sections["decisions"]),
            "## Validation\n" + md_table(sections["validation"]),
            "## Next target\n" + md_table(sections["next"]),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    branch = branch_id()
    sources = source_register_rows(branch)
    branch_rows = branch_classifier_rows(branch)
    product_rows = product_convention_rows(branch)
    search_rows = c_parent_search_rows(branch)
    write_live_files(branch_rows, product_rows, search_rows)
    dryrun = parser_dryrun_rows(branch, branch_rows, product_rows, search_rows)
    gates = claim_gate_rows(branch)
    decisions = decision_rows(branch)
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(BRANCH_CLASSIFIER_FIRST_FILL, branch_rows)
    write_csv(PRODUCT_CONVENTION_FIRST_FILL, product_rows)
    write_csv(C_PARENT_SOURCE_SEARCH_PLAN, search_rows)
    write_csv(FIRST_FILL_PARSER_DRYRUN, dryrun)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validation = validation_rows(sources, branch_rows, product_rows, search_rows, dryrun, gates)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "branch_rows": branch_rows,
            "product_rows": product_rows,
            "search_rows": search_rows,
            "dryrun": dryrun,
            "gates": gates,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1443_branch_product_first_fill_nonclaim_C_parent_blocked")


if __name__ == "__main__":
    main()
