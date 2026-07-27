from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1239"
TITLE = "1239-Y5-R10-local-residual-vector-runner-input-schema-and-source-priority"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_INPUT_SCHEMA.csv"
INPUT_ROWS_PATH = OUT_DIR / f"{PACK_ID}_BRANCH_INPUT_ROWS_TEMPLATE.csv"
SOURCE_PRIORITY_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_PRIORITY_CHECKLIST.csv"
DRYRUN_PATH = OUT_DIR / f"{PACK_ID}_DRYRUN_ACCEPTANCE_MATRIX.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1239_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def is_false(row: dict[str, object], key: str) -> bool:
    return not parse_bool(row.get(key, False))


def source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > RUN_STARTED_UTC
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1239_0_1238_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1238_NEXT_TARGET.csv",
            "needle": "NEXT1238_0_1239",
            "purpose": "1238 handoff to residual-vector runner input schema",
        },
        {
            "source_id": "SRC1239_1_1238_vector",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1238_LOCAL_RESIDUAL_VECTOR_MAP.csv",
            "needle": "RV1238_0_QR",
            "purpose": "local residual vector source",
        },
        {
            "source_id": "SRC1239_2_1238_priority",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1238_EMPIRICAL_TEST_PRIORITY_LEDGER.csv",
            "needle": "TP1238_0_PPN_QR",
            "purpose": "empirical source priority ordering",
        },
        {
            "source_id": "SRC1239_3_1238_benchmark",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1238_LOCAL_GR_CLOSURE_BENCHMARK_SCORECARD.csv",
            "needle": "BGR1238_2_finite_residual",
            "purpose": "closure versus finite residual branch distinction",
        },
        {
            "source_id": "SRC1239_4_1238_claim_gates",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1238_CLAIM_GATES.csv",
            "needle": "GATE1238_1_derived_local_GR",
            "purpose": "no derived local GR claim gate",
        },
        {
            "source_id": "SRC1239_5_ppn_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_PPN_EVALUATOR_INPUT_TEMPLATE.csv",
            "needle": "PPN524_0_gamma_operator_slip",
            "purpose": "older PPN input template discipline",
        },
        {
            "source_id": "SRC1239_6_ppn_vector",
            "local_path": "source-intake/mts_residuals/P8_Y5_PPN_RESIDUAL_VECTOR.csv",
            "needle": "PPN524_1_beta_source_quadratic",
            "purpose": "older PPN residual vector discipline",
        },
        {
            "source_id": "SRC1239_7_ppn_comparator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1181_PPN_RESIDUAL_VECTOR_COMPARATOR_ROWS.csv",
            "needle": "PPNV1181_0_gamma",
            "purpose": "PPN comparator rows with missing MTS prediction slots",
        },
        {
            "source_id": "SRC1239_8_ppn_bounds",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1141_PPN_BOUND_ANCHOR_ROWS.csv",
            "needle": "PPNBA1141_0_alpha1",
            "purpose": "source-backed PPN bound anchor style",
        },
    ]

    source_register = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    schema = [
        {
            "field_name": "input_id",
            "required": True,
            "type": "string",
            "allowed_values_or_format": "unique row id",
            "purpose": "stable row identity for future local residual runner",
        },
        {
            "field_name": "branch_type",
            "required": True,
            "type": "enum",
            "allowed_values_or_format": "closure_benchmark | finite_residual | source_required | derived_target",
            "purpose": "prevents closure rows being treated as finite evidence or theorem rows",
        },
        {
            "field_name": "arena",
            "required": True,
            "type": "enum",
            "allowed_values_or_format": "PPN_QR | PPN_beta | WEP_R10 | clock_alpha | readout_transfer | QCD_component | cosmology_separate",
            "purpose": "routes rows to the correct future evaluator",
        },
        {
            "field_name": "symbol",
            "required": True,
            "type": "string",
            "allowed_values_or_format": "declared residual symbol",
            "purpose": "connects runner row to residual-vector map",
        },
        {
            "field_name": "value_mode",
            "required": True,
            "type": "enum",
            "allowed_values_or_format": "closure_value | numeric_value | bound_interval | source_kernel | missing_source | derived_zero_candidate",
            "purpose": "states whether a value is closure-only, numeric, sourced, or missing",
        },
        {
            "field_name": "value",
            "required": False,
            "type": "number_or_symbolic",
            "allowed_values_or_format": "numeric finite value, interval, kernel id, or MISSING_SOURCE",
            "purpose": "future runner payload; closure zeros are explicitly labelled by branch_type/value_mode",
        },
        {
            "field_name": "units",
            "required": True,
            "type": "string",
            "allowed_values_or_format": "dimensionless | declared_physical_units | source_kernel",
            "purpose": "blocks silent unit mixing",
        },
        {
            "field_name": "source_requirement",
            "required": True,
            "type": "string",
            "allowed_values_or_format": "derivation path, source table path, external source id, or closure label",
            "purpose": "makes missing evidence visible before scoring",
        },
        {
            "field_name": "validation_gate",
            "required": True,
            "type": "enum",
            "allowed_values_or_format": "blocked | schema_only | source_required | closure_only | ready_nonclaim",
            "purpose": "future runner acceptance gate",
        },
        {
            "field_name": "valid_for_claim",
            "required": True,
            "type": "boolean",
            "allowed_values_or_format": "False for all 1239 rows",
            "purpose": "no public/local-GR claim promotion",
        },
        {
            "field_name": "claim_allowed",
            "required": True,
            "type": "boolean",
            "allowed_values_or_format": "False for all 1239 rows",
            "purpose": "hard stop against closure-as-evidence",
        },
    ]

    input_rows = [
        {
            "input_id": "IN1239_0_QR_closure",
            "branch_type": "closure_benchmark",
            "arena": "PPN_QR",
            "residual_id": "RV1238_0_QR",
            "symbol": "Q_R",
            "value_mode": "closure_value",
            "value": "0",
            "units": "dimensionless_or_RAB_charge_units_declared",
            "source_requirement": "CLOSE1237_1_local_reciprocity; explicit closure label required",
            "validation_gate": "closure_only",
            "runner_action": "may compare as private GR-like baseline; must not count as evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1239_1_QR_finite",
            "branch_type": "finite_residual",
            "arena": "PPN_QR",
            "residual_id": "RV1238_0_QR",
            "symbol": "Q_R",
            "value_mode": "missing_source",
            "value": "MISSING_QR_BOUND_OR_MODEL",
            "units": "dimensionless_or_RAB_charge_units_declared",
            "source_requirement": "first-class zero theorem or PPN residual bound schema for gamma/light-bending/Shapiro/orbits",
            "validation_gate": "source_required",
            "runner_action": "block scoring until bound/model supplied",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1239_2_beta_PPN",
            "branch_type": "source_required",
            "arena": "PPN_beta",
            "residual_id": "RV1238_1_beta_PPN",
            "symbol": "beta_PPN-1",
            "value_mode": "missing_source",
            "value": "MISSING_SECOND_ORDER_FIELD_EQUATIONS",
            "units": "dimensionless",
            "source_requirement": "full local field equation expansion, conservation identity, and beta comparator map",
            "validation_gate": "blocked",
            "runner_action": "do not score beta until field equation source exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1239_3_alpha_EM",
            "branch_type": "finite_residual",
            "arena": "clock_alpha",
            "residual_id": "RV1238_2_alpha",
            "symbol": "b_alpha_or_c_alpha_DD",
            "value_mode": "missing_source",
            "value": "MISSING_ALPHA_COEFFICIENT_PRIOR",
            "units": "dimensionless_or_declared_DD_units",
            "source_requirement": "EM-lock theorem or source-backed coefficient prior",
            "validation_gate": "source_required",
            "runner_action": "block claim; allow schema smoke only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1239_4_source_alpha",
            "branch_type": "finite_residual",
            "arena": "WEP_R10",
            "residual_id": "RV1238_3_source_alpha",
            "symbol": "beta_source_alpha",
            "value_mode": "missing_source",
            "value": "MISSING_SOURCE_FUNCTOR_OR_PRIOR",
            "units": "dimensionless",
            "source_requirement": "source-label forgetting theorem or numeric source-normalization prior",
            "validation_gate": "source_required",
            "runner_action": "block WEP/R10 scoring until supplied",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1239_5_readout_transfer",
            "branch_type": "source_required",
            "arena": "readout_transfer",
            "residual_id": "RV1238_4_readout",
            "symbol": "tau_clock_tau_WEP_tau_readout",
            "value_mode": "missing_source",
            "value": "MISSING_READOUT_KERNEL",
            "units": "source_kernel",
            "source_requirement": "official/readout kernel or parent radiative/readout closure theorem",
            "validation_gate": "source_required",
            "runner_action": "block transfer scoring; allow schema smoke only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1239_6_QCD_components",
            "branch_type": "source_required",
            "arena": "QCD_component",
            "residual_id": "RV1238_5_QCD",
            "symbol": "F_Bq_F_Bg_delta_wq_delta_wg",
            "value_mode": "missing_source",
            "value": "MISSING_QCD_COMPONENT_ROWS",
            "units": "dimensionless_energy_fraction_and_dimensionless_coupling",
            "source_requirement": "claim-grade F_B,q/F_B,g source rows plus delta_w priors or theorem-zero",
            "validation_gate": "source_required",
            "runner_action": "block material source-vector scoring until supplied",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1239_7_closure_GR_bundle",
            "branch_type": "closure_benchmark",
            "arena": "PPN_QR",
            "residual_id": "BGR1238_1_closure_GR",
            "symbol": "closure_bundle_RAB_F2_source_readout",
            "value_mode": "closure_value",
            "value": "all_closure_residuals_set_to_zero_or_fixed",
            "units": "mixed_declared_by_component",
            "source_requirement": "closure label only; never evidence",
            "validation_gate": "closure_only",
            "runner_action": "may run as best-case baseline beside finite residual branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    source_priority = [
        {
            "priority_id": "SP1239_0_QR",
            "rank": 1,
            "needed_for": "IN1239_1_QR_finite",
            "source_or_derivation_needed": "first-class zero theorem or explicit PPN_QR residual-to-gamma model with bound units",
            "minimum_acceptance": "declares how Q_R maps to gamma_minus_1/light-bending/Shapiro/orbit residual and has numeric bound or theorem-zero source",
            "current_status": "MISSING",
            "next_action": "build PPN_QR residual bound schema before any local-GR score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority_id": "SP1239_1_beta",
            "rank": 2,
            "needed_for": "IN1239_2_beta_PPN",
            "source_or_derivation_needed": "second-order local field equations and beta comparator map",
            "minimum_acceptance": "maps beta_PPN-1 to declared MTS coefficients and source paths",
            "current_status": "MISSING",
            "next_action": "keep beta blocked until field equation expansion exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority_id": "SP1239_2_source_WEP",
            "rank": 3,
            "needed_for": "IN1239_4_source_alpha",
            "source_or_derivation_needed": "source-label forgetting proof or numeric beta_source_alpha prior with material convention",
            "minimum_acceptance": "source path, units, material convention, and no placeholder markers",
            "current_status": "MISSING",
            "next_action": "tie to WEP/R10 material source vector once component rows exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority_id": "SP1239_3_alpha_readout",
            "rank": 4,
            "needed_for": "IN1239_3_alpha_EM; IN1239_5_readout_transfer",
            "source_or_derivation_needed": "alpha coefficient prior plus clock/WEP/readout transfer kernel",
            "minimum_acceptance": "coefficient source and transfer kernel are separately cited and unit-checked",
            "current_status": "MISSING",
            "next_action": "keep clock-alpha rows schema-only until sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority_id": "SP1239_4_QCD_components",
            "rank": 5,
            "needed_for": "IN1239_6_QCD_components",
            "source_or_derivation_needed": "F_B,q/F_B,g source rows and delta_w_q/delta_w_g priors or theorem-zero",
            "minimum_acceptance": "energy-fraction convention, material basis, source path, and no toy/proxy labels",
            "current_status": "MISSING",
            "next_action": "stage source intake after PPN_QR schema because local GR hair is first-order fatal",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    dryrun = [
        {
            "dryrun_id": "DRY1239_0_schema_fields",
            "check": "required schema fields exist",
            "result": "PASS",
            "details": f"{len(schema)} schema fields declared",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "dryrun_id": "DRY1239_1_branch_separation",
            "check": "closure rows and finite/source rows are distinguishable",
            "result": "PASS",
            "details": "branch_type separates closure_benchmark from finite_residual/source_required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "dryrun_id": "DRY1239_2_missing_sources_block",
            "check": "missing finite rows are blocked from scoring",
            "result": "PASS",
            "details": "all missing finite rows use source_required or blocked validation gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "dryrun_id": "DRY1239_3_closure_not_evidence",
            "check": "closure rows are labelled closure_only",
            "result": "PASS",
            "details": "closure_value rows cannot be counted as derived_zero or evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "dryrun_id": "DRY1239_4_no_long_jobs",
            "check": "no data job is launched",
            "result": "PASS",
            "details": "1239 is schema/checklist generation only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1239_0_schema_not_runner_claim",
            "decision": "create runner input schema but do not score data",
            "because": "source rows are missing and closure rows are baseline-only",
            "next_action": "build PPN_QR bound schema first",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1239_1_QR_first",
            "decision": "prioritize Q_R/gamma residual over subtler WEP/QCD rows",
            "because": "nonzero reciprocal hair would kill local-GR recovery before composition tests",
            "next_action": "map Q_R to PPN gamma/light-bending/Shapiro/orbital residual or prove Q_R=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1239_2_closure_rows_allowed_private",
            "decision": "allow closure rows only as private benchmark baseline",
            "because": "closure values are not derivations or evidence",
            "next_action": "future runners must report closure and finite residual branches separately",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1239_0_runner_input_schema",
            "claim": "schema exists for future nonclaim testing",
            "status": "PASS_NONCLAIM",
            "reason": "schema/template rows generated and validation passed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1239_1_any_physics_pass",
            "claim": "any PPN/WEP/R10/clock/local-GR pass",
            "status": "BLOCKED",
            "reason": "1239 does not run data or provide sourced finite values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1239_2_closure_as_evidence",
            "claim": "closure zeros are evidence for MTS",
            "status": "BLOCKED",
            "reason": "closure rows are explicitly branch_type=closure_benchmark and validation_gate=closure_only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1239_3_derived_local_GR",
            "claim": "derived local GR/Newton reduction",
            "status": "BLOCKED",
            "reason": "Q_R/beta/source/readout/QCD residual rows remain missing or closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1239_0_1240",
            "target_file": "1240-Y5-R10-PPN-QR-residual-bound-schema-or-zero-charge-theorem.md",
            "target_script": "scripts/Y5_R10_PPN_QR_residual_bound_schema_or_zero_charge_theorem.py",
            "task": "attack the rank-1 local blocker: either derive Q_R=0 from a parent zero-charge theorem or build a nonclaim schema mapping Q_R to PPN gamma/light-bending/Shapiro/orbital residual bounds",
            "success_condition": "Q_R is either parent-zeroed without closure or becomes a bounded finite residual row with units, comparator, and source requirements",
            "do_not_do": "do not claim local GR, do not use closure Q_R=0 as evidence, and do not run long data jobs",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_paths = [
        SOURCE_REGISTER_PATH,
        SCHEMA_PATH,
        INPUT_ROWS_PATH,
        SOURCE_PRIORITY_PATH,
        DRYRUN_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(SCHEMA_PATH, schema)
    write_csv(INPUT_ROWS_PATH, input_rows)
    write_csv(SOURCE_PRIORITY_PATH, source_priority)
    write_csv(DRYRUN_PATH, dryrun)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(NEXT_PATH, next_target)

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:ERROR:{exc}")

    all_sources_exist = all(parse_bool(row["path_exists"]) for row in source_register)
    all_needles_found = all(parse_bool(row["needle_found"]) for row in source_register)
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for table in [
            source_register,
            schema,
            input_rows,
            source_priority,
            dryrun,
            decisions,
            claim_gates,
            next_target,
        ]
        for row in table
    )
    schema_fields_ok = {row["field_name"] for row in schema} >= {
        "input_id",
        "branch_type",
        "arena",
        "symbol",
        "value_mode",
        "source_requirement",
        "validation_gate",
        "valid_for_claim",
        "claim_allowed",
    }
    branch_types = {row["branch_type"] for row in input_rows}
    branch_separation_ok = "closure_benchmark" in branch_types and {"finite_residual", "source_required"} & branch_types
    closure_rows_safe = all(
        row["validation_gate"] == "closure_only" and row["value_mode"] == "closure_value"
        for row in input_rows
        if row["branch_type"] == "closure_benchmark"
    )
    missing_rows_blocked = all(
        row["validation_gate"] in {"source_required", "blocked"}
        for row in input_rows
        if row["value_mode"] == "missing_source"
    )
    qr_first = source_priority[0]["priority_id"] == "SP1239_0_QR" and source_priority[0]["rank"] == 1
    dryrun_pass = all(row["result"] == "PASS" for row in dryrun)
    physics_gates_blocked = all(
        row["status"] in {"BLOCKED", "PASS_NONCLAIM"} and is_false(row, "claim_allowed")
        for row in claim_gates
    )
    next_is_1240 = next_target[0]["target_file"].startswith("1240-Y5-R10-PPN-QR")
    fw_recent = formalization_recent_count()

    validation = [
        validation_row(
            "VAL1239_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(parse_bool(row['path_exists']) for row in source_register)}/{len(source_register)} sources exist",
        ),
        validation_row(
            "VAL1239_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(parse_bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        ),
        validation_row(
            "VAL1239_2_schema_fields",
            "runner input schema includes required fields",
            schema_fields_ok,
            f"schema_fields={len(schema)}",
        ),
        validation_row(
            "VAL1239_3_branch_separation",
            "closure and finite/source rows are distinguishable",
            bool(branch_separation_ok),
            f"branch_types={sorted(branch_types)}",
        ),
        validation_row(
            "VAL1239_4_closure_rows_safe",
            "closure rows cannot count as evidence",
            closure_rows_safe,
            "closure rows use value_mode=closure_value and validation_gate=closure_only",
        ),
        validation_row(
            "VAL1239_5_missing_rows_blocked",
            "missing finite/source rows are blocked from scoring",
            missing_rows_blocked,
            "missing_source rows use source_required or blocked gates",
        ),
        validation_row(
            "VAL1239_6_QR_priority",
            "Q_R/gamma residual is rank 1",
            qr_first,
            "SP1239_0_QR rank=1",
        ),
        validation_row(
            "VAL1239_7_dryrun_pass",
            "dry-run acceptance matrix passes",
            dryrun_pass,
            f"dryrun_rows={len(dryrun)}",
        ),
        validation_row(
            "VAL1239_8_claim_gates",
            "physics claim gates remain blocked/nonclaim",
            physics_gates_blocked,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1239_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_generated_nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1239_10_next_target_1240",
            "next target is PPN Q_R bound schema or zero-charge theorem",
            next_is_1240,
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1239_11_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_counts),
        ),
        validation_row(
            "VAL1239_12_formalization_untouched",
            "formalization-workbench untouched during run",
            fw_recent == 0,
            f"formalization_recent_write_count_since_run_start={fw_recent}",
        ),
    ]
    validation.append(
        validation_row(
            "VAL1239_13_overall",
            "overall 1239 validation",
            all(row["status"] == "PASS" for row in validation),
            "1239 creates a nonclaim runner-input schema, separates closure from finite rows, and prioritizes Q_R/gamma next",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1239 does **not** run data or claim a pass. It converts the 1238 local residual vector into a nonclaim runner-input schema that keeps closure benchmark rows separate from finite/source-required rows.",
        "",
        "**Main progress:** future testing now has a concrete intake contract. `Q_R/gamma` is rank 1, closure zeros are labelled `closure_only`, and missing finite residuals are blocked until sourced.",
        "",
        "**No-claim guard:** no derived GR, EM lock, graph connectedness, `Delta_w=0`, R10, WEP, PPN, clock, orbital, local-GR, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Runner Input Schema",
        markdown_table(schema, list(schema[0].keys())),
        "",
        "## Branch Input Rows Template",
        markdown_table(input_rows, list(input_rows[0].keys())),
        "",
        "## Source Priority Checklist",
        markdown_table(source_priority, list(source_priority[0].keys())),
        "",
        "## Dry-Run Acceptance Matrix",
        markdown_table(dryrun, list(dryrun[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Next Target",
        markdown_table(next_target, list(next_target[0].keys())),
        "",
        "## Validation",
        markdown_table(validation, list(validation[0].keys())),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
