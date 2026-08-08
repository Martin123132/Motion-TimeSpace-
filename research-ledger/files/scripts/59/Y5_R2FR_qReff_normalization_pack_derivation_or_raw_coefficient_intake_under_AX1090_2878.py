from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2878-Y5-R2FR-qReff-normalization-pack-derivation-or-raw-coefficient-intake-under-AX1090.md"

SRC_2877_DOC = ROOT / "2877-Y5-R2FR-first-finite-row-fill-under-two-sign-interface-under-AX1090.md"
SRC_2877_NEXT = RESIDUALS / "P8_Y5_R2FR_2877_NEXT_TARGET.csv"
SRC_2877_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2877_VALIDATION.csv"
SRC_2877_FILL = RESIDUALS / "P8_Y5_R2FR_2877_QREFF_ELLR_FILL_ATTEMPT.csv"
SRC_2877_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2877_NORMALIZATION_PACK_SOURCE_REQUESTS.csv"
SRC_2877_GATES = RESIDUALS / "P8_Y5_R2FR_2877_ACCEPTANCE_GATES.csv"

SRC_2839_KERNEL = RESIDUALS / "P8_Y5_R2FR_2839_GREEN_KERNEL_NORMALIZATION.csv"
SRC_2839_SELECTOR = RESIDUALS / "P8_Y5_R2FR_2839_FIRST_SOURCE_ROW_SELECTOR.csv"
SRC_2840_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2840_NORMALIZATION_PACK_CONTRACT.csv"
SRC_2840_ZERO = RESIDUALS / "P8_Y5_R2FR_2840_PARENT_ZERO_CERTIFICATE_AUDIT.csv"
SRC_2872_LAW = RESIDUALS / "P8_Y5_R2FR_2872_QREFF_SOURCE_EQUATION_AUDIT.csv"
SRC_2872_TEMPLATE = RESIDUALS / "P8_Y5_R2FR_2872_QREFF_FINITE_ROW_TEMPLATE_NONCLAIM.csv"
SRC_1625_BUILDER = RESIDUALS / "P8_Y5_PARENT_QLOC_1625_FINITE_ZR_PRIOR_ROW_BUILDER.csv"
SRC_1869_SCHEMA = RESIDUALS / "P8_Y5_PARENT_QLOC_1869_COMPONENT_INPUT_SCHEMA.csv"
SRC_2169_SCHEMA = RESIDUALS / "P8_Y5_PARENT_QLOC_2169_FINITE_LOCAL_COMPONENT_SCHEMA.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2878_SOURCE_REGISTER.csv",
    "derivation": RESIDUALS / "P8_Y5_R2FR_2878_QREFF_NORMALIZATION_DERIVATION.csv",
    "pack_schema": RESIDUALS / "P8_Y5_R2FR_2878_NORMALIZATION_PACK_SCHEMA.csv",
    "raw_queue": RESIDUALS / "P8_Y5_R2FR_2878_RAW_COEFFICIENT_INTAKE_QUEUE.csv",
    "promotion": RESIDUALS / "P8_Y5_R2FR_2878_PROMOTION_CRITERIA.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2878_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2878_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2878_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2878_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2878_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2878_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "schema_copy": LOCAL_BOUNDS / "RAB_QREFF_NORMALIZATION_PACK_SCHEMA_2878_NONCLAIM.csv",
    "queue_copy": SOURCE_WEIGHT / "RAB_QREFF_RAW_COEFFICIENT_INTAKE_QUEUE_2878_NONCLAIM.csv",
    "derivation_copy": BETA_DOCS / "RAB_QREFF_NORMALIZATION_DERIVATION_2878_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2878_SR_over_ZR_source_map_or_zero_theorem_NEXT.csv",
}


for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


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
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2878_0_2877_doc", SRC_2877_DOC, "Status: `Y5_R2FR_2877_first_finite_row_fill_attempted_qReff_ellR_not_live_qcab_not_live_2878_next`;same-normalization `q_R_eff` pack", "2877 selected q_R_eff normalization-pack target"),
        ("SRC2878_1_2877_next", SRC_2877_NEXT, "NEXT2877_0_2878", "handoff to 2878"),
        ("SRC2878_2_2877_validation", SRC_2877_VALIDATION, "VAL2877_OVERALL", "2877 validation"),
        ("SRC2878_3_2877_fill", SRC_2877_FILL, "FILL2877_0_qReff_ellR_live_row_attempt", "q_R_eff+ell_R fill refused"),
        ("SRC2878_4_2877_requests", SRC_2877_REQUESTS, "REQ2877_0_qReff_normalization_pack", "normalization pack request"),
        ("SRC2878_5_2877_gates", SRC_2877_GATES, "GATE2877_0_qReff_value;GATE2877_1_ellR_range", "2877 fail-closed gates"),
        ("SRC2878_6_2839_kernel", SRC_2839_KERNEL, "KER2839_0_static_operator;KER2839_1_normalized_operator;KER2839_4_compact_body", "kernel algebra"),
        ("SRC2878_7_2839_selector", SRC_2839_SELECTOR, "SEL2839_0_minimal_pair;SEL2839_3_JR_PiR_readout", "first row selector"),
        ("SRC2878_8_2840_contract", SRC_2840_CONTRACT, "PACK2840_0_range;PACK2840_1_amplitude;PACK2840_5_source;PACK2840_6_convention", "normalization pack contract"),
        ("SRC2878_9_2840_zero", SRC_2840_ZERO, "PZ2840_2_source_zero;PZ2840_5_joint_certificate", "zero certificate blockers"),
        ("SRC2878_10_2872_law", SRC_2872_LAW, "LAW2872_1_compact_source_charge;LAW2872_6_verdict", "q_R_eff law"),
        ("SRC2878_11_2872_template", SRC_2872_TEMPLATE, "TPL2872_0_qReff_parent_source_row;TPL2872_2_SRZR_source_density", "q_R_eff template"),
        ("SRC2878_12_1625_builder", SRC_1625_BUILDER, "PB1625_0_ZR;PB1625_1_MR2;PB1625_2_JR;PB1625_3_BR", "older coefficient builder"),
        ("SRC2878_13_1869_schema", SRC_1869_SCHEMA, "FLC1869_1_ZR;FLC1869_2_MR2;FLC1869_6_JR;FLC1869_8_tau_R10", "finite component schema"),
        ("SRC2878_14_2169_schema", SRC_2169_SCHEMA, "FLC2169_1_ZR;FLC2169_3_lambdaR;FLC2169_6_JR;FLC2169_8_tau_R10", "finite local component schema"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def derivation_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "derivation_id": "DER2878_0_static_equation",
            "statement": "E_R^finite=-Div(Z_R Grad delta_R)+M_R^2 delta_R+S_R=0",
            "consequence": "static residual branch has a candidate elliptic operator before normalization",
            "source_path": str(SRC_2839_KERNEL),
            "source_anchor": "KER2839_0_static_operator",
            "status": "SYMBOLIC_PARENT_NORMAL_FORM_ONLY",
            "missing_for_claim": "source-backed Z_R, M_R^2, S_R and sign/domain convention",
            "parent_signed": False,
        },
        {
            "derivation_id": "DER2878_1_normalize_by_ZR",
            "statement": "if Z_R is nonzero and same-normalized, divide by Z_R: (-Laplace+M_R^2/Z_R)delta_R=-S_R/Z_R",
            "consequence": "ell_R^-2=M_R^2/Z_R",
            "source_path": str(SRC_2839_KERNEL),
            "source_anchor": "KER2839_1_normalized_operator",
            "status": "CONDITIONAL_ALGEBRA_VALID",
            "missing_for_claim": "Z_R and M_R^2 source-backed in same normalization with positive range branch or explicit complex/tachyon rejection",
            "parent_signed": False,
        },
        {
            "derivation_id": "DER2878_2_range",
            "statement": "ell_R=sqrt(Z_R/M_R^2) when Z_R/M_R^2>0, or direct sourced ell_R can replace the ratio",
            "consequence": "range is not a standalone fitted number unless the parent/operator normalization is declared",
            "source_path": str(SRC_2840_CONTRACT),
            "source_anchor": "PACK2840_0_range",
            "status": "RANGE_RULE_READY_INPUTS_MISSING",
            "missing_for_claim": "Z_R, M_R^2, units, branch and source anchor",
            "parent_signed": False,
        },
        {
            "derivation_id": "DER2878_3_compact_charge",
            "statement": "outside compact W: delta_R=q_R_eff exp(-r/ell_R)/(4*pi*r)+H_R with q_R_eff=-int_W S_R/Z_R d^3x",
            "consequence": "amplitude depends on the normalized source integral and cannot be inferred from Z_R alone",
            "source_path": str(SRC_2839_KERNEL),
            "source_anchor": "KER2839_4_compact_body",
            "status": "CHARGE_RULE_READY_SOURCE_INTEGRAL_MISSING",
            "missing_for_claim": "S_R/Z_R source map, compact support/worldtube, units, boundary H_R class",
            "parent_signed": False,
        },
        {
            "derivation_id": "DER2878_4_arena_projection",
            "statement": "tau_R10/tau_PPN/tau_clock/tau_orbital map delta_R into observables after q_R_eff and ell_R exist",
            "consequence": "empirical scoring is a later projection layer, not a source-row substitute",
            "source_path": str(SRC_2839_SELECTOR),
            "source_anchor": "SEL2839_4_projection",
            "status": "PROJECTION_REQUIRED_NOT_FILLED",
            "missing_for_claim": "arena kernels, source/test charges, local denominator and bound/readout conventions",
            "parent_signed": False,
        },
        {
            "derivation_id": "DER2878_5_verdict",
            "statement": "the q_R_eff pack algebra is exact enough to define intake rows, but not sourced enough to fill them",
            "consequence": "create raw coefficient intake queue and route next to S_R/Z_R source map or source-zero theorem",
            "source_path": str(SRC_2877_FILL),
            "source_anchor": "FILL2877_0_qReff_ellR_live_row_attempt",
            "status": "DERIVED_SCHEMA_NOT_LIVE_ROW",
            "missing_for_claim": "all live source/value/projection inputs",
            "parent_signed": False,
        },
    ]
    return [add_common(row) for row in rows]


def pack_schema_rows() -> list[dict[str, Any]]:
    rows = [
        ("PACK2878_0_ZR", "Z_R", "kinetic residue / gradient coefficient", "same-normalized operator coefficient", "numeric value, theorem-zero, or bounded interval with source", "MISSING_Z_R"),
        ("PACK2878_1_MR2", "M_R^2", "mass gap / range owner", "same normalization as Z_R", "numeric value, theorem-zero, or direct range replacement", "MISSING_M_R2"),
        ("PACK2878_2_ellR", "ell_R", "interaction range", "length", "sqrt(Z_R/M_R^2) or direct sourced range", "MISSING_ELL_R"),
        ("PACK2878_3_SRZR", "S_R/Z_R", "normalized compact source density", "declared source-density units", "parent source map or source-zero theorem", "MISSING_S_R_OVER_Z_R"),
        ("PACK2878_4_qReff", "q_R_eff", "compact-source Green charge", "length if delta_R dimensionless else declared", "-int_W S_R/Z_R d^3x plus included boundary term", "MISSING_q_R_eff"),
        ("PACK2878_5_HR", "H_R", "boundary homogeneous/no-hair class", "same as delta_R profile", "zero/exact/included/finite bounded homogeneous mode", "MISSING_H_R_BOUNDARY_CLASS"),
        ("PACK2878_6_tau", "tau_arena", "arena projection kernels", "arena dependent", "tau_R10/tau_PPN/tau_clock/tau_orbital", "MISSING_TAU_ARENA"),
        ("PACK2878_7_provenance", "source_path+equation_anchor", "local provenance", "n/a", "existing source path and anchor for every nonzero/theorem entry", "MISSING_PARENT_SOURCE_PATH"),
    ]
    return [
        add_common(
            {
                "schema_id": schema_id,
                "symbol": symbol,
                "role": role,
                "units": units,
                "acceptance_content": content,
                "current_marker": marker,
                "field_ready": False,
            }
        )
        for schema_id, symbol, role, units, content, marker in rows
    ]


def raw_queue_rows() -> list[dict[str, Any]]:
    rows = [
        ("RAW2878_0_ZR", "Z_R", "operator_coefficient", "derive from parent quadratic action block or source as coefficient row", "PB1625_0_ZR;FLC1869_1_ZR", "MISSING_NUMERIC_VALUE", 1),
        ("RAW2878_1_MR2", "M_R^2", "operator_coefficient", "derive parent Hessian/mass-gap eigenvalue or source direct range replacement", "PB1625_1_MR2;FLC1869_2_MR2", "MISSING_NUMERIC_VALUE", 2),
        ("RAW2878_2_SRZR", "S_R/Z_R", "source_density", "derive source map from parent matter/readout variation or prove source-zero theorem", "KER2839_4_compact_body;PZ2840_2_source_zero", "MISSING_SOURCE_MAP", 3),
        ("RAW2878_3_HR", "H_R", "boundary_homogeneous", "prove no-hair/zero boundary class or source finite included homogeneous row", "PACK2840_3_boundary;PZ2840_3_boundary_zero", "MISSING_BOUNDARY_CLASS", 4),
        ("RAW2878_4_tau_R10", "tau_R10", "arena_projection", "project delta_R profile to alpha(lambda) with source/test support and accepted bound curve", "SEL2839_4_projection;FLC1869_8_tau_R10", "MISSING_TAU_R10", 5),
        ("RAW2878_5_tau_PPN", "tau_PPN", "arena_projection", "project q_R_eff/ell_R to PPN residual vector in same source frame", "SEL2839_4_projection;FLC1869_9_tau_PPN", "MISSING_TAU_PPN", 6),
    ]
    return [
        add_common(
            {
                "queue_id": queue_id,
                "symbol": symbol,
                "row_type": row_type,
                "needed_action": action,
                "source_basis": basis,
                "current_marker": marker,
                "priority": priority,
                "accepted_live_input": False,
                "selected_for_next": queue_id == "RAW2878_2_SRZR",
            }
        )
        for queue_id, symbol, row_type, action, basis, marker, priority in rows
    ]


def promotion_rows() -> list[dict[str, Any]]:
    rows = [
        ("PROM2878_0_same_norm", "Z_R and M_R^2 share one normalization and units", "MISSING_SAME_NORMALIZATION"),
        ("PROM2878_1_source_map", "S_R/Z_R source density is parent-derived or theorem-zero", "MISSING_SOURCE_MAP"),
        ("PROM2878_2_integral", "q_R_eff integral is finite with compact support/worldtube", "MISSING_q_R_eff"),
        ("PROM2878_3_boundary", "H_R boundary homogeneous mode is zero, included, or bounded", "MISSING_BOUNDARY_CLASS"),
        ("PROM2878_4_projection", "tau projections exist before empirical scoring", "MISSING_TAU_ARENA"),
        ("PROM2878_5_provenance", "all nonzero/theorem entries have source_path and equation_anchor", "MISSING_PARENT_SOURCE_PATH"),
    ]
    return [
        add_common(
            {
                "promotion_id": promotion_id,
                "requirement": requirement,
                "current_blocker": blocker,
                "promotion_ready": False,
            }
        )
        for promotion_id, requirement, blocker in rows
    ]


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2878_0_algebra", "normalization algebra is recorded", "PASS_CONTROL_ONLY", "derivation rows define ell_R and q_R_eff shape"),
        ("GATE2878_1_ZR_MR2", "Z_R and M_R^2 live same-normalization rows exist", "FAIL", "builder/schema rows only"),
        ("GATE2878_2_SRZR", "S_R/Z_R source map or source-zero theorem exists", "FAIL", "source map is the selected next blocker"),
        ("GATE2878_3_qReff", "q_R_eff finite integral or zero theorem exists", "FAIL", "depends on missing S_R/Z_R and boundary class"),
        ("GATE2878_4_boundary", "H_R boundary class exists", "FAIL", "boundary/no-hair certificate not signed"),
        ("GATE2878_5_tau", "arena projections exist", "FAIL", "projection rows are schema only"),
        ("GATE2878_6_runner", "first finite row can be imported", "FAIL", "raw queue contains no accepted live inputs"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
                "control_gate_recorded": result == "PASS_CONTROL_ONLY",
                "claim_unlocked": False,
            }
        )
        for gate_id, criterion, result, reason in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2878_0_qReff_pack_import",
                "status": "REFUSED_RAW_QUEUE_ONLY",
                "accepted_pack_fields": 0,
                "required_pack_fields": 8,
                "reason": "normalization pack schema and raw queue are written, but no live coefficient/source/projection row is accepted",
                "runner_ready": False,
                "score_allowed": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2878_0_derivation",
            "decision": "Derive exact q_R_eff normalization pack algebra.",
            "result": "COMPLETE_CONDITIONAL",
            "because": "static operator, range rule and compact-source charge are now one schema",
        },
        {
            "decision_id": "DEC2878_1_fill",
            "decision": "Promote q_R_eff pack to live row.",
            "result": "REFUSED",
            "because": "all coefficient/source/boundary/projection fields remain missing",
        },
        {
            "decision_id": "DEC2878_2_queue",
            "decision": "Create raw coefficient intake queue.",
            "result": "COMPLETE_NONCLAIM",
            "because": "future fills now have explicit rows for Z_R, M_R^2, S_R/Z_R, H_R and tau",
        },
        {
            "decision_id": "DEC2878_3_next",
            "decision": "Attack S_R/Z_R source map or source-zero theorem next.",
            "result": "SELECTED_2879",
            "because": "without the source map, q_R_eff cannot be finite even if range is later sourced",
        },
    ]
    return [add_common(row) for row in rows]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2878_0_2879",
                "status": "selected_primary",
                "target_doc": "2879-Y5-R2FR-SR-over-ZR-source-map-or-source-zero-theorem-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_SR_over_ZR_source_map_or_source_zero_theorem_under_AX1090_2879.py",
                "mission": "derive the parent source map S_R/Z_R from matter/readout variation or prove a parent source-zero theorem; if neither closes, keep q_R_eff raw queue open and route to Z_R/M_R^2 operator normalization",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    pairs = [
        ("COPY2878_0_schema", OUTPUTS["pack_schema"], BRANCH_OUTPUTS["schema_copy"], "q_R_eff normalization pack schema nonclaim copy"),
        ("COPY2878_1_queue", OUTPUTS["raw_queue"], BRANCH_OUTPUTS["queue_copy"], "raw coefficient intake queue nonclaim copy"),
        ("COPY2878_2_derivation", OUTPUTS["derivation"], BRANCH_OUTPUTS["derivation_copy"], "q_R_eff normalization derivation nonclaim copy"),
        ("COPY2878_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to S_R/Z_R source map target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in pairs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def generated_under_root(paths: list[Path]) -> bool:
    root_resolved = ROOT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "parent_signed",
        "field_ready",
        "accepted_live_input",
        "promotion_ready",
        "gate_passed",
        "claim_unlocked",
        "runner_ready",
        "score_allowed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    derivation = rows_by_name["derivation"]
    schema = rows_by_name["pack_schema"]
    raw_queue = rows_by_name["raw_queue"]
    promotion = rows_by_name["promotion"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2878_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2878_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2878_2_derivation_complete", len(derivation) == 6 and any(row["derivation_id"] == "DER2878_3_compact_charge" for row in derivation), "normalization derivation rows complete"),
        ("VAL2878_3_schema_complete", {row["symbol"] for row in schema} >= {"Z_R", "M_R^2", "ell_R", "S_R/Z_R", "q_R_eff", "H_R", "tau_arena"}, "pack schema covers all required symbols"),
        ("VAL2878_4_raw_queue_open", len(raw_queue) >= 6 and not any(row["accepted_live_input"] for row in raw_queue), "raw coefficient queue written with no accepted inputs"),
        ("VAL2878_5_SRZR_selected_next", any(row["queue_id"] == "RAW2878_2_SRZR" and row["selected_for_next"] is True for row in raw_queue), "S_R/Z_R source map selected next"),
        ("VAL2878_6_promotion_blocked", len(promotion) == 6 and all(row["promotion_ready"] is False for row in promotion), "promotion criteria all blocked"),
        ("VAL2878_7_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "all claim gates fail closed"),
        ("VAL2878_8_runner_refused", runner[0]["status"] == "REFUSED_RAW_QUEUE_ONLY" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2878_9_next_target_2879", next_target[0]["next_id"] == "NEXT2878_0_2879" and next_target[0]["selected"] is True, "2879 source-map target selected"),
        ("VAL2878_10_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2878_11_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2878_12_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2878_13_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2878_14_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2878_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2878_16_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": now(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2878_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2878 derived the q_R_eff normalization pack algebra, wrote a raw coefficient intake queue, kept all rows nonclaim, refused runner import, and selected S_R/Z_R source-map or source-zero theorem for 2879.",
            "timestamp_utc": now(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    text = f"""# 2878 - Y5 R2FR q_R_eff Normalization Pack Derivation Or Raw Coefficient Intake Under AX1090

Status: `Y5_R2FR_2878_qReff_normalization_pack_algebra_derived_raw_queue_written_SRZR_2879_next`

## Private Verdict

2878 gets a real little gear in place: the `q_R_eff` row is no longer a vague missing value. It is a same-normalization pack.

The conditional algebra is:

`E_R^finite=-Div(Z_R Grad delta_R)+M_R^2 delta_R+S_R=0`,

so, if `Z_R` and `M_R^2` are sourced in the same normalization,

`(-Laplace+M_R^2/Z_R)delta_R=-S_R/Z_R`, `ell_R=sqrt(Z_R/M_R^2)`, and `q_R_eff=-int_W S_R/Z_R d^3x`.

This does not fill the row yet. It defines exactly what has to be filled: `Z_R`, `M_R^2` or direct `ell_R`, `S_R/Z_R`, `H_R`, `tau` projections, units, and source anchors. The next best attack is the source map `S_R/Z_R`, because without it there is no finite amplitude even if the range is later sourced.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## q_R_eff Normalization Derivation

{md_table(rows_by_name["derivation"], ["derivation_id", "statement", "consequence", "status", "missing_for_claim", "parent_signed", "valid_for_claim"])}

## Normalization Pack Schema

{md_table(rows_by_name["pack_schema"], ["schema_id", "symbol", "role", "units", "acceptance_content", "current_marker", "field_ready", "valid_for_claim"])}

## Raw Coefficient Intake Queue

{md_table(rows_by_name["raw_queue"], ["queue_id", "symbol", "row_type", "needed_action", "current_marker", "priority", "accepted_live_input", "selected_for_next", "valid_for_claim"])}

## Promotion Criteria

{md_table(rows_by_name["promotion"], ["promotion_id", "requirement", "current_blocker", "promotion_ready", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_pack_fields", "required_pack_fields", "reason", "runner_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    remove_pycache()

    rows_by_name = {
        "sources": source_register_rows(),
        "derivation": derivation_rows(),
        "pack_schema": pack_schema_rows(),
        "raw_queue": raw_queue_rows(),
        "promotion": promotion_rows(),
        "gates": gate_rows(),
        "runner": runner_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branch_rows)
    rows_by_name["branches"] = branch_rows

    remove_pycache()
    validation = validation_rows(rows_by_name, branch_rows)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name, branch_rows, validation)
    remove_pycache()

    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation if row["validation_id"] == "VAL2878_OVERALL")
    print(f"VAL2878_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
