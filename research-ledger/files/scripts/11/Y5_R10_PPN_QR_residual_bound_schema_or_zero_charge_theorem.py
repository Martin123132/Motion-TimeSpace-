from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1240"
TITLE = "1240-Y5-R10-PPN-QR-residual-bound-schema-or-zero-charge-theorem"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
ZERO_THEOREM_PATH = OUT_DIR / f"{PACK_ID}_QR_ZERO_CHARGE_THEOREM_ATTEMPT.csv"
PPN_MAP_PATH = OUT_DIR / f"{PACK_ID}_QR_TO_PPN_MAPPING_SCHEMA.csv"
BOUND_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_QR_BOUND_INPUT_SCHEMA.csv"
COMPARATOR_PATH = OUT_DIR / f"{PACK_ID}_PPN_COMPARATOR_LEDGER.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1240_VALIDATION.csv"


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
            "source_id": "SRC1240_0_1239_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1239_NEXT_TARGET.csv",
            "needle": "NEXT1239_0_1240",
            "purpose": "1239 handoff to Q_R zero theorem or PPN bound schema",
        },
        {
            "source_id": "SRC1240_1_1239_inputs",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1239_BRANCH_INPUT_ROWS_TEMPLATE.csv",
            "needle": "IN1239_1_QR_finite",
            "purpose": "Q_R finite residual runner row",
        },
        {
            "source_id": "SRC1240_2_1239_priority",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1239_SOURCE_PRIORITY_CHECKLIST.csv",
            "needle": "SP1239_0_QR",
            "purpose": "Q_R rank-1 source priority",
        },
        {
            "source_id": "SRC1240_3_cell_current",
            "local_path": "11-cell-current-origin-attempt.md",
            "needle": "W partial_r R_AB = Q_R",
            "purpose": "cell-current equation and Q_R hair",
        },
        {
            "source_id": "SRC1240_4_cell_fail",
            "local_path": "11-cell-current-origin-attempt.md",
            "needle": "It does not give:",
            "purpose": "current conservation does not imply Q_R=0",
        },
        {
            "source_id": "SRC1240_5_gauge_noether",
            "local_path": "12-gauge-noether-origin-audit.md",
            "needle": "first-class parent constraint",
            "purpose": "first-class route possible in principle but absent",
        },
        {
            "source_id": "SRC1240_6_ppn_gamma",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1181_PPN_RESIDUAL_VECTOR_COMPARATOR_ROWS.csv",
            "needle": "PPNV1181_0_gamma",
            "purpose": "sourced gamma comparator row",
        },
        {
            "source_id": "SRC1240_7_ppn_source_register",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv",
            "needle": "SRC1181W_0_Cassini_gamma",
            "purpose": "Cassini gamma source provenance",
        },
        {
            "source_id": "SRC1240_8_ppn_framework",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_753_EXTERNAL_PPN_SOURCE_PACK.csv",
            "needle": "EXT753_0_Will_2014_LRR",
            "purpose": "PPN framework source pack",
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

    zero_theorem = [
        {
            "attempt_id": "ZQR1240_0_target",
            "claim_piece": "Q_R zero-charge theorem",
            "formal_statement": "Prove Q_R=0 from parent MTS rather than closure R_AB=0.",
            "attempt_result": "TARGET_SHARP",
            "blocker": "requires topological/source representation zero or first-class parent constraint",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1239_SOURCE_PRIORITY_CHECKLIST.csv", "SP1239_0_QR"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "ZQR1240_1_current_conservation",
            "claim_piece": "ordinary cell current conservation",
            "formal_statement": "partial_r(W partial_r R_AB)=0 implies W partial_r R_AB=Q_R.",
            "attempt_result": "FAILS_ZERO_THEOREM",
            "blocker": "conservation makes Q_R constant, not zero",
            "source": source_ref("11-cell-current-origin-attempt.md", "W partial_r R_AB = Q_R"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "ZQR1240_2_asymptotic_flatness",
            "claim_piece": "asymptotic reciprocity",
            "formal_statement": "R_infinity=0 still permits R_AB=-Q_R/r.",
            "attempt_result": "FAILS_ZERO_THEOREM",
            "blocker": "asymptotic condition kills constant offset but not reciprocal charge hair",
            "source": source_ref("11-cell-current-origin-attempt.md", "R_AB = -Q_R/r"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "ZQR1240_3_topological_zero_charge",
            "claim_piece": "topological/source representation Q_R=0",
            "formal_statement": "Q_R = integral rho_R = 0 by source representation or topological selection.",
            "attempt_result": "EXACT_CONDITIONAL_NOT_DERIVED",
            "blocker": "11 names this as the best possible route but says it is not currently derived",
            "source": source_ref("11-cell-current-origin-attempt.md", "topological_zero_charge"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "ZQR1240_4_gauge_noether",
            "claim_piece": "gauge/Noether origin",
            "formal_statement": "A genuine first-class parent constraint could eliminate R_AB and forbid Q_R.",
            "attempt_result": "POSSIBLE_IN_PRINCIPLE_NOT_PRESENT",
            "blocker": "12 says current scaffold lacks the constrained parent action",
            "source": source_ref("12-gauge-noether-origin-audit.md", "first-class parent constraint"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "ZQR1240_5_verdict",
            "claim_piece": "Q_R=0 as theorem",
            "formal_statement": "No inspected current-state route derives Q_R=0; Q_R remains a finite local residual unless closure is explicitly assumed.",
            "attempt_result": "ZERO_CHARGE_THEOREM_NOT_DERIVED",
            "blocker": "ordinary conservation, asymptotic flatness, and Noether identity are insufficient",
            "source": "ZQR1240_1 through ZQR1240_4",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    ppn_map = [
        {
            "map_id": "QMAP1240_0_weak_field_identity",
            "quantity": "R_AB",
            "schema_relation": "R_AB = ln(T^2 S) approximately 2(gamma-1) U/c^2 in weak-field areal-radial PPN matching",
            "normalization": "U=GM/r and |R_AB|<<1",
            "status": "SCHEMA_RELATION_NONCLAIM",
            "blocker": "requires exact metric/coordinate convention before scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "QMAP1240_1_cell_hair_solution",
            "quantity": "Q_R",
            "schema_relation": "cell-current exterior gives R_AB = -Q_R/r after R_infinity=0",
            "normalization": "Q_R has length-like units unless normalized by GM/c^2",
            "status": "SOURCE_BACKED_INTERNAL_RELATION",
            "blocker": "Q_R normalization must be declared in any runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "QMAP1240_2_dimensionless_qR",
            "quantity": "q_R_hat",
            "schema_relation": "q_R_hat = Q_R c^2/(GM)",
            "normalization": "dimensionless; source mass convention must be specified",
            "status": "RUNNER_NORMALIZATION_PROPOSED",
            "blocker": "GM must be same measured source used in PPN comparator",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "QMAP1240_3_gamma_projection",
            "quantity": "gamma_minus_1_QR",
            "schema_relation": "gamma_minus_1_QR approximately -q_R_hat/2 under QMAP1240_0 and QMAP1240_1",
            "normalization": "linear weak field only",
            "status": "NONCLAIM_PROJECTION_SCHEMA",
            "blocker": "not a derived MTS prediction; only a scoring map for finite Q_R residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "QMAP1240_4_other_PPN_channels",
            "quantity": "light_bending_Shapiro_orbital",
            "schema_relation": "light-bending and Shapiro rows can inherit gamma projection; orbital rows need beta/source field equations too",
            "normalization": "channel-specific comparator required",
            "status": "PARTIAL_SCHEMA_ONLY",
            "blocker": "primary numeric rows for light-bending/orbital not filled here",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    bound_schema = [
        {
            "bound_id": "QB1240_0_qR_input",
            "runner_field": "q_R_hat",
            "definition": "Q_R c^2/(GM)",
            "units": "dimensionless",
            "required_value": "numeric finite residual or derived zero theorem",
            "current_value": "MISSING_QR_VALUE",
            "validation_gate": "source_required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "QB1240_1_gamma_projection",
            "runner_field": "gamma_minus_1_QR",
            "definition": "-q_R_hat/2",
            "units": "dimensionless",
            "required_value": "computed from q_R_hat after normalization",
            "current_value": "MISSING_QR_VALUE",
            "validation_gate": "blocked_until_qR_supplied",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "QB1240_2_gamma_comparator",
            "runner_field": "gamma_comparator",
            "definition": "Cassini gamma_minus_1 comparator from 1181 source row",
            "units": "dimensionless",
            "required_value": "(2.1 +/- 2.3)e-5 comparator available as nonclaim source-backed anchor",
            "current_value": "SOURCED_COMPARATOR_PREDICTION_MISSING",
            "validation_gate": "comparator_available_nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "QB1240_3_pass_rule",
            "runner_field": "pass_rule",
            "definition": "abs(gamma_minus_1_QR) <= N_sigma * sigma_gamma or a separately justified absolute target",
            "units": "dimensionless",
            "required_value": "N_sigma policy and uncertainty convention",
            "current_value": "MISSING_STATISTICAL_POLICY",
            "validation_gate": "source_required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "QB1240_4_closure_row",
            "runner_field": "closure_q_R_hat",
            "definition": "q_R_hat=0 only for closure benchmark",
            "units": "dimensionless",
            "required_value": "explicit branch_type=closure_benchmark",
            "current_value": "0_CLOSURE_ONLY",
            "validation_gate": "closure_only_not_evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    comparator = [
        {
            "comparator_id": "COMP1240_0_gamma_Cassini",
            "observable": "gamma_minus_1",
            "source_row": "PPNV1181_0_gamma",
            "comparator_value": "(2.1 +/- 2.3)e-5",
            "use_in_QR_schema": "primary bound anchor for gamma_minus_1_QR",
            "status": "COMPARATOR_AVAILABLE_PREDICTION_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "comparator_id": "COMP1240_1_Shapiro_radio",
            "observable": "Shapiro/radio time-delay gamma channel",
            "source_row": "SRC1181W_0_Cassini_gamma",
            "comparator_value": "same Cassini gamma source anchor",
            "use_in_QR_schema": "same gamma projection; do not duplicate as independent evidence",
            "status": "COMPARATOR_AVAILABLE_NOT_INDEPENDENT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "comparator_id": "COMP1240_2_light_bending",
            "observable": "light-bending gamma channel",
            "source_row": "EXT753_0_Will_2014_LRR framework only in current local evidence",
            "comparator_value": "MISSING_PRIMARY_NUMERIC_ROW_IN_1240",
            "use_in_QR_schema": "future independent check if primary row is sourced",
            "status": "SOURCE_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "comparator_id": "COMP1240_3_orbital",
            "observable": "orbital/perihelion/local dynamics",
            "source_row": "PPNV1181_1_beta and PPNV1181_2_eta require beta/source inputs",
            "comparator_value": "NOT_QR_ONLY",
            "use_in_QR_schema": "blocked until beta/source field equations exist",
            "status": "BLOCKED_BY_BETA_SOURCE_MAP",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1240_0_no_zero_theorem",
            "decision": "do not claim Q_R=0",
            "because": "ordinary conservation/asymptotic/gauge-Noether routes do not derive zero charge",
            "next_action": "treat Q_R as finite residual unless future first-class/topological theorem appears",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1240_1_schema_map",
            "decision": "use q_R_hat -> gamma_minus_1_QR as nonclaim projection schema",
            "because": "it makes the fatal local-GR residual testable without pretending a prediction exists",
            "next_action": "build a smoke runner that refuses missing q_R/statistical policy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1240_2_cassini_anchor_limited",
            "decision": "use Cassini gamma as primary sourced comparator anchor only",
            "because": "light-bending/orbital rows need separate primary numeric rows or beta/source maps",
            "next_action": "do not multiply evidence by reusing the same gamma anchor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1240_0_QR_zero",
            "claim": "Q_R=0 theorem",
            "status": "BLOCKED",
            "reason": "ZQR1240_5 result=ZERO_CHARGE_THEOREM_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1240_1_QR_bound_pass",
            "claim": "finite Q_R passes PPN bound",
            "status": "BLOCKED",
            "reason": "q_R_hat value and statistical pass rule are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1240_2_local_GR",
            "claim": "derived local GR/Newton reduction",
            "status": "BLOCKED",
            "reason": "Q_R remains finite residual; beta/source/conservation still open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1240_3_schema_ready",
            "claim": "nonclaim Q_R PPN schema exists",
            "status": "PASS_NONCLAIM",
            "reason": "mapping and comparator schema rows generated, but no score run",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1240_0_1241",
            "target_file": "1241-Y5-R10-PPN-QR-nonclaim-smoke-runner-and-refusal-gates.md",
            "target_script": "scripts/Y5_R10_PPN_QR_nonclaim_smoke_runner_and_refusal_gates.py",
            "task": "build a tiny nonclaim smoke runner that loads q_R_hat/gamma comparator rows, refuses missing q_R or missing statistical policy, and keeps closure Q_R=0 separate from finite residual scoring",
            "success_condition": "runner dry-run proves closure rows cannot pass as evidence and finite Q_R rows remain blocked until numeric q_R and pass-policy inputs exist",
            "do_not_do": "do not run long jobs, do not claim local GR, and do not treat Cassini comparator alone as an MTS prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_paths = [
        SOURCE_REGISTER_PATH,
        ZERO_THEOREM_PATH,
        PPN_MAP_PATH,
        BOUND_SCHEMA_PATH,
        COMPARATOR_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(ZERO_THEOREM_PATH, zero_theorem)
    write_csv(PPN_MAP_PATH, ppn_map)
    write_csv(BOUND_SCHEMA_PATH, bound_schema)
    write_csv(COMPARATOR_PATH, comparator)
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
            zero_theorem,
            ppn_map,
            bound_schema,
            comparator,
            decisions,
            claim_gates,
            next_target,
        ]
        for row in table
    )
    zero_not_derived = any(
        row["attempt_id"] == "ZQR1240_5_verdict"
        and row["attempt_result"] == "ZERO_CHARGE_THEOREM_NOT_DERIVED"
        for row in zero_theorem
    )
    gamma_map_exists = any(
        row["map_id"] == "QMAP1240_3_gamma_projection" for row in ppn_map
    )
    q_bound_schema_exists = any(row["bound_id"] == "QB1240_0_qR_input" for row in bound_schema)
    comparator_available = any(
        row["comparator_id"] == "COMP1240_0_gamma_Cassini"
        and row["status"] == "COMPARATOR_AVAILABLE_PREDICTION_MISSING"
        for row in comparator
    )
    closure_not_evidence = any(
        row["bound_id"] == "QB1240_4_closure_row"
        and row["validation_gate"] == "closure_only_not_evidence"
        for row in bound_schema
    )
    claim_gates_ok = all(
        row["status"] in {"BLOCKED", "PASS_NONCLAIM"} and is_false(row, "claim_allowed")
        for row in claim_gates
    )
    next_is_1241 = next_target[0]["target_file"].startswith("1241-Y5-R10-PPN-QR")
    fw_recent = formalization_recent_count()

    validation = [
        validation_row(
            "VAL1240_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(parse_bool(row['path_exists']) for row in source_register)}/{len(source_register)} sources exist",
        ),
        validation_row(
            "VAL1240_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(parse_bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        ),
        validation_row(
            "VAL1240_2_zero_not_derived",
            "Q_R zero-charge theorem is not promoted",
            zero_not_derived,
            "ZQR1240_5 result=ZERO_CHARGE_THEOREM_NOT_DERIVED",
        ),
        validation_row(
            "VAL1240_3_gamma_map",
            "Q_R to gamma projection schema exists",
            gamma_map_exists,
            "QMAP1240_3 gamma projection row exists",
        ),
        validation_row(
            "VAL1240_4_bound_schema",
            "q_R bound input schema exists",
            q_bound_schema_exists,
            "QB1240_0 q_R input row exists",
        ),
        validation_row(
            "VAL1240_5_comparator_available",
            "Cassini gamma comparator is available but prediction missing",
            comparator_available,
            "COMP1240_0 status=COMPARATOR_AVAILABLE_PREDICTION_MISSING",
        ),
        validation_row(
            "VAL1240_6_closure_not_evidence",
            "closure q_R=0 is not evidence",
            closure_not_evidence,
            "QB1240_4 validation_gate=closure_only_not_evidence",
        ),
        validation_row(
            "VAL1240_7_claim_gates",
            "claim gates remain blocked/nonclaim",
            claim_gates_ok,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1240_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_generated_nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1240_9_next_target_1241",
            "next target is Q_R nonclaim smoke runner",
            next_is_1241,
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1240_10_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_counts),
        ),
        validation_row(
            "VAL1240_11_formalization_untouched",
            "formalization-workbench untouched during run",
            fw_recent == 0,
            f"formalization_recent_write_count_since_run_start={fw_recent}",
        ),
    ]
    validation.append(
        validation_row(
            "VAL1240_12_overall",
            "overall 1240 validation",
            all(row["status"] == "PASS" for row in validation),
            "1240 refuses Q_R=0 theorem promotion and builds a nonclaim Q_R-to-PPN gamma bound schema",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1240 does **not** derive `Q_R=0`. It converts `Q_R` into a nonclaim PPN residual schema by introducing `q_R_hat = Q_R c^2/(GM)` and the weak-field projection `gamma_minus_1_QR ~ -q_R_hat/2`.",
        "",
        "**Main progress:** the rank-1 local blocker is now runner-shaped: closure `Q_R=0` is labelled benchmark-only, finite `Q_R` needs a value plus statistical pass policy, and the Cassini gamma row is a comparator, not an MTS prediction.",
        "",
        "**No-claim guard:** no derived GR, local-GR pass, PPN pass, WEP/R10 pass, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Q_R Zero-Charge Theorem Attempt",
        markdown_table(zero_theorem, list(zero_theorem[0].keys())),
        "",
        "## Q_R To PPN Mapping Schema",
        markdown_table(ppn_map, list(ppn_map[0].keys())),
        "",
        "## Q_R Bound Input Schema",
        markdown_table(bound_schema, list(bound_schema[0].keys())),
        "",
        "## PPN Comparator Ledger",
        markdown_table(comparator, list(comparator[0].keys())),
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
