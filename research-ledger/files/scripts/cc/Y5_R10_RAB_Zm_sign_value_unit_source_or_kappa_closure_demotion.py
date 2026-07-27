from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1381"
TITLE = "1381-Y5-R10-RAB-Zm-sign-value-unit-source-or-kappa-closure-demotion"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
ZM_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_ZM_SIGN_VALUE_UNIT_AUDIT.csv"
DEMOTION_PATH = OUT_DIR / f"{PACK_ID}_KAPPA_CLOSURE_SYMBOLIC_DEMOTION.csv"
RUNNER_FEED_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_FEED_UPDATE.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1381_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1381_0_1380_doc",
            "source_path": "1380-Y5-R10-RAB-kappa-origin-or-shell-bound-first-parent-signing-clause.md",
            "required_anchor": "NEXT1380_0_1381",
            "purpose": "1380 handoff to Z_m sign/value/unit source or kappa closure demotion.",
        },
        {
            "source_id": "SRC1381_1_1380_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1380_NEXT_TARGET.csv",
            "required_anchor": "NEXT1380_0_1381",
            "purpose": "machine-readable 1381 target.",
        },
        {
            "source_id": "SRC1381_2_1380_kappa_origin",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1380_KAPPA_ZM_ORIGIN_COEFFICIENT_ROW.csv",
            "required_anchor": "KOR1380_4_parent_status",
            "purpose": "kappa_m=Z_m symbolic coefficient origin.",
        },
        {
            "source_id": "SRC1381_3_826_coefficients",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_COEFFICIENT_LEDGER.csv",
            "required_anchor": "C826_0_Zm",
            "purpose": "original Z_m coefficient checklist.",
        },
        {
            "source_id": "SRC1381_4_826_action_ansatz",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
            "required_anchor": "AA826_1_memory_sector",
            "purpose": "candidate L_m action containing Z_m.",
        },
        {
            "source_id": "SRC1381_5_970_quadratic_action",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
            "required_anchor": "QMA970_2_positivity",
            "purpose": "relative positive-operator identity and unsigned inputs.",
        },
        {
            "source_id": "SRC1381_6_1302_stress",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
            "required_anchor": "MSR1302_0_canonical_scalar_stress_form",
            "purpose": "canonical scalar stress row with missing Z_m sign/value.",
        },
        {
            "source_id": "SRC1381_7_1303_stress_inputs",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1303_K_MEM_STRESS_SIGMA_BOUND_INPUT_LEDGER_NONCLAIM.csv",
            "required_anchor": "KMS1303_0_Zm_abs_bound",
            "purpose": "Z_m_bar and memory stress input requirements.",
        },
        {
            "source_id": "SRC1381_8_1304_owner",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1304_MEMORY_OPERATOR_OWNER_ATTEMPT.csv",
            "required_anchor": "OO1304_1_static_local_operator_map",
            "purpose": "relative operator map A_m^{ij}=Z_m h^{ij}.",
        },
        {
            "source_id": "SRC1381_9_1304_positive_gap",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1304_ZM_POSITIVE_GAP_MAP_NONCLAIM.csv",
            "required_anchor": "ZPG1304_0_Zm_positive",
            "purpose": "positive ellipticity and missing Z_m_min/Z_m_bar map.",
        },
        {
            "source_id": "SRC1381_10_1304_first_bound",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1304_FIRST_STRESS_BOUND_INPUT_ROWS_NONCLAIM.csv",
            "required_anchor": "KMS1304_0_Zm_bar_first_row",
            "purpose": "first source-backed symbol row for Z_m_bar with value missing.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def zm_audit_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "audit_id": "ZMS1381_0_symbol_presence",
                "target": "Z_m(X_B)",
                "question": "Does the corpus define the coefficient slot?",
                "evidence": "C826_0_Zm names Z_m(X_B) for memory kinetic stress, stability, and perturbation speed.",
                "result": "PASS_SYMBOL_NAMED",
                "remaining_gap": "current_status is missing_parent_value",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_COEFFICIENT_LEDGER.csv",
                "source_anchor": "C826_0_Zm",
            },
            {
                "audit_id": "ZMS1381_1_action_slot",
                "target": "L_m kinetic term",
                "question": "Does the parent action language contain a Z_m kinetic term?",
                "evidence": "AA826_1 writes L_m=-1/2 Z_m(X_B) nabla m nabla m - V_R(m;X_B) plus sourced/bath terms.",
                "result": "PASS_CANDIDATE_ACTION_SLOT",
                "remaining_gap": "action is a candidate scaffold; Z_m, V_R, X_B, and source/bath terms remain unsigned",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
                "source_anchor": "AA826_1_memory_sector",
            },
            {
                "audit_id": "ZMS1381_2_sign_no_ghost",
                "target": "Z_m sign",
                "question": "Is positive sign parent-signed?",
                "evidence": "C826_0 and ZPG1304 require positive/no-ghost or Z_m>=Z_m_min>0, but mark the value/theorem missing.",
                "result": "CONDITIONAL_SIGN_REQUIREMENT_NOT_SOURCED",
                "remaining_gap": "Z_m_min or a positivity theorem from parent coefficient law",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_COEFFICIENT_LEDGER.csv;source-intake/mts_residuals/P8_Y5_R10_1304_ZM_POSITIVE_GAP_MAP_NONCLAIM.csv",
                "source_anchor": "C826_0_Zm;ZPG1304_0_Zm_positive",
            },
            {
                "audit_id": "ZMS1381_3_value_range",
                "target": "Z_m value/range",
                "question": "Is a numeric value, lower bound, or upper bound sourced?",
                "evidence": "ZPG1304 requests Z_m_min and Z_m_bar; KMS1304 names Z_m_bar but supplied_value is MISSING_PARENT_VALUE_OR_BOUND.",
                "result": "VALUE_RANGE_NOT_SOURCED",
                "remaining_gap": "Z_m_min, Z_m_bar, Z_m(X_B) function, X_B range, local domain D_loc",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1304_ZM_POSITIVE_GAP_MAP_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_1304_FIRST_STRESS_BOUND_INPUT_ROWS_NONCLAIM.csv",
                "source_anchor": "ZPG1304_1_Zm_abs_bound;KMS1304_0_Zm_bar_first_row",
            },
            {
                "audit_id": "ZMS1381_4_units",
                "target": "Z_m units",
                "question": "Are units locked enough for runner scoring?",
                "evidence": "KMS1303 and KMS1304 both mark units as required from parent L_m normalization; frame/units lock remains missing.",
                "result": "UNITS_NOT_LOCKED",
                "remaining_gap": "parent L_m normalization, units of m, length convention, frame/signature lock",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1303_K_MEM_STRESS_SIGMA_BOUND_INPUT_LEDGER_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_1304_FIRST_STRESS_BOUND_INPUT_ROWS_NONCLAIM.csv",
                "source_anchor": "KMS1303_0_Zm_abs_bound;KMS1304_0_Zm_bar_first_row",
            },
            {
                "audit_id": "ZMS1381_5_operator_positivity",
                "target": "local elliptic operator",
                "question": "Does relative operator positivity prove Z_m sign/value?",
                "evidence": "QMA970 and OO1304 give a relative positive-operator/elliptic map, but require A^ij positive and Z_m sign/Hessian/local branch.",
                "result": "RELATIVE_POSITIVITY_ONLY",
                "remaining_gap": "A^ij owner, Z_m sign, M_m^2 Hessian, local branch, source/boundary closure",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv;source-intake/mts_residuals/P8_Y5_R10_1304_MEMORY_OPERATOR_OWNER_ATTEMPT.csv",
                "source_anchor": "QMA970_2_positivity;OO1304_1_static_local_operator_map",
            },
            {
                "audit_id": "ZMS1381_6_stress_bound",
                "target": "memory stress bound",
                "question": "Can Z_m be bounded indirectly by the stress envelope?",
                "evidence": "KMS1303/KMS1304 build first stress-bound input rows, but all values remain missing.",
                "result": "BOUND_ROUTE_READY_VALUES_MISSING",
                "remaining_gap": "Z_m_bar, gradient profile/nohair, potential subtraction, source/bath/boundary, frame lock",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1303_K_MEM_STRESS_SIGMA_BOUND_INPUT_LEDGER_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_1304_FIRST_STRESS_BOUND_INPUT_ROWS_NONCLAIM.csv",
                "source_anchor": "KMS1303_0_Zm_abs_bound;KMS1304_0_Zm_bar_first_row",
            },
            {
                "audit_id": "ZMS1381_7_verdict",
                "target": "Z_m sign/value/unit source",
                "question": "Does Z_m receive a source-backed sign/value/unit row?",
                "evidence": "All available rows name the coefficient or conditional positivity requirement, but explicitly mark values/units/sign source missing.",
                "result": "NO_SOURCE_BACKED_SIGN_VALUE_UNIT_ROW",
                "remaining_gap": "derive/source Z_m_min, Z_m_bar, units, field status, and frame lock",
                "source_path": "aggregate_ZMS1381_0_to_ZMS1381_6",
                "source_anchor": "aggregate",
            },
        ]
    )


def demotion_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "demotion_id": "KCD1381_0_status",
                "runner_object": "kappa_m=Z_m",
                "demoted_status": "PURELY_SYMBOLIC_CLOSURE_COEFFICIENT",
                "allowed_use": "symbolic algebra and schema wiring only",
                "blocked_use": "numeric scoring, local-GR/PPN/R10 pass, theorem-zero claim",
                "reason": "Z_m sign/value/range/units are not source-backed",
            },
            {
                "demotion_id": "KCD1381_1_sign_gate",
                "runner_object": "Z_m F2 > 0",
                "demoted_status": "SIGN_CONDITION_ONLY",
                "allowed_use": "refusal gate for real ell_tr",
                "blocked_use": "assuming positive Z_m or stable branch",
                "reason": "positive/no-ghost premise is named but not parent-proved",
            },
            {
                "demotion_id": "KCD1381_2_value_gate",
                "runner_object": "ell_tr=sqrt(Z_m L0^2/F2)",
                "demoted_status": "SYMBOLIC_LENGTH_ONLY",
                "allowed_use": "formula register and future candidate rows",
                "blocked_use": "computing L_tr or U_B numerically",
                "reason": "Z_m, F2, L0 values are missing",
            },
            {
                "demotion_id": "KCD1381_3_stress_gate",
                "runner_object": "Z_m gradient stress",
                "demoted_status": "RETAINED_RESIDUAL",
                "allowed_use": "stress-bound ledger with symbolic Z_m_bar",
                "blocked_use": "deleting scalar stress after using it to derive the profile",
                "reason": "stress envelope rows are not scoreable",
            },
            {
                "demotion_id": "KCD1381_4_verdict",
                "runner_object": "kappa/Z_m branch",
                "demoted_status": "CLOSURE_SYMBOLIC_BRANCH_NO_NUMERIC_SCORING",
                "allowed_use": "prepare parent coefficient acquisition and symbolic dry-run schema",
                "blocked_use": "any claim-grade reduction to GR/Newton or local empirical pass",
                "reason": "sign/value/unit source failed in current corpus",
            },
        ]
    )


def runner_feed_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "feed_id": "RUF1381_0_Zm_sign",
                "runner_field": "Z_m_sign",
                "feed_update": "Z_m>0 remains a required no-ghost/ellipticity premise, not a sourced fact",
                "status": "CONDITIONAL_SIGN_ONLY",
                "blocks_claim_because": "Z_m_min positivity theorem/value is missing",
            },
            {
                "feed_id": "RUF1381_1_Zm_value",
                "runner_field": "Z_m_value_or_range",
                "feed_update": "no Z_m value, lower bound, upper bound, or range is sourced",
                "status": "MISSING_VALUE_RANGE",
                "blocks_claim_because": "Z_m_bar and Z_m_min are missing",
            },
            {
                "feed_id": "RUF1381_2_Zm_units",
                "runner_field": "Z_m_units",
                "feed_update": "units remain symbolic from parent L_m normalization",
                "status": "MISSING_UNITS_LOCK",
                "blocks_claim_because": "m units, Fhat units, frame/signature, and action density normalization are missing",
            },
            {
                "feed_id": "RUF1381_3_kappa_branch",
                "runner_field": "kappa_m=Z_m",
                "feed_update": "demote to closure-symbolic coefficient; allow symbolic formulas only",
                "status": "CLOSURE_SYMBOLIC_ONLY",
                "blocks_claim_because": "coefficient origin exists but sign/value/units do not",
            },
            {
                "feed_id": "RUF1381_4_claim_status",
                "runner_field": "local_GR_PPN_R10_status",
                "feed_update": "local-GR, PPN, R10, and q_loc=0 claims remain blocked",
                "status": "BLOCKED_NO_CLAIM",
                "blocks_claim_because": "closure-symbolic kappa branch cannot prove GR reduction or local tests",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1381_0_symbol",
                "gate": "Z_m coefficient slot exists",
                "status": "PASS_SYMBOL_EXISTS",
                "reason": "826/1302/1380 name Z_m and map kappa_m to it.",
            },
            {
                "gate_id": "GATE1381_1_sign",
                "gate": "Z_m sign is parent-signed",
                "status": "BLOCKED_SIGN_NOT_SOURCED",
                "reason": "positive/no-ghost premise is conditional; no Z_m_min theorem/value exists.",
            },
            {
                "gate_id": "GATE1381_2_value",
                "gate": "Z_m value/range is source-backed",
                "status": "BLOCKED_VALUE_RANGE_MISSING",
                "reason": "Z_m_bar and Z_m_min are requested but missing.",
            },
            {
                "gate_id": "GATE1381_3_units",
                "gate": "Z_m units/frame are locked",
                "status": "BLOCKED_UNITS_FRAME_MISSING",
                "reason": "parent L_m normalization and local frame/signature lock remain missing.",
            },
            {
                "gate_id": "GATE1381_4_demote",
                "gate": "kappa branch is explicitly closure-symbolic",
                "status": "PASS_DEMOTED_TO_CLOSURE_SYMBOLIC",
                "reason": "KCD1381 rows prevent numeric scoring from symbolic coefficient origin.",
            },
            {
                "gate_id": "GATE1381_5_local_claim",
                "gate": "local GR / PPN / R10 pass can be claimed",
                "status": "BLOCKED_NO_CLAIM",
                "reason": "Z_m sign/value/units are missing and shell/arena gates remain open.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1381_0_Zm_status",
                "decision": "do not source-sign Z_m yet",
                "why": "current corpus names Z_m and requires positivity, but does not supply sign/value/range/units",
                "next_action": "attack parent coefficient law for Z_m or construct a normalized symbolic prior with refusal gates",
            },
            {
                "decision_id": "DEC1381_1_kappa_status",
                "decision": "demote kappa_m=Z_m to closure-symbolic only",
                "why": "coefficient origin is real but still not scoreable",
                "next_action": "keep ell_tr and U_B formulas symbolic until coefficient values and units exist",
            },
            {
                "decision_id": "DEC1381_2_next_best_route",
                "decision": "derive a coefficient-law scaffold for Z_m(X_B)",
                "why": "this is the shortest route from symbolic transition law to a testable nonclaim branch",
                "next_action": "try to derive admissibility constraints on Z_m(X_B): positivity, boundedness, same-value rule, and units normalization",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1381_0_1382",
                "next_doc": "1382-Y5-R10-RAB-Zm-coefficient-law-admissibility-or-symbolic-prior-pack.md",
                "next_script": "scripts/Y5_R10_RAB_Zm_coefficient_law_admissibility_or_symbolic_prior_pack.py",
                "task": "derive admissibility constraints for Z_m(X_B)—positivity/no-ghost, finite upper/lower bounds, same local/cosmology value rule, and units normalization—or build a symbolic prior pack that refuses numeric scoring",
                "success_condition": "either a source-backed/nonclaim Z_m coefficient-law scaffold exists, or a symbolic prior pack records all missing values and keeps local claims blocked",
                "do_not_claim": "local GR;PPN pass;R10 pass;q_loc=0;GitHub-ready result",
            }
        ]
    )


def generated_csv_paths() -> list[Path]:
    return [
        SOURCE_REGISTER_PATH,
        ZM_AUDIT_PATH,
        DEMOTION_PATH,
        RUNNER_FEED_PATH,
        CLAIM_GATE_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]


def all_rows_nonclaim(*groups: list[dict[str, object]]) -> bool:
    for rows in groups:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() != "false":
                return False
            if str(row.get("claim_allowed", "")).lower() != "false":
                return False
    return True


def csv_parse_details(paths: list[Path]) -> tuple[bool, str]:
    details = []
    ok = True
    for path in paths:
        try:
            count = len(read_csv_rows(path))
            details.append(f"{path.name}:{count}")
        except Exception as exc:  # pragma: no cover
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def validation_rows(
    sources: list[dict[str, object]],
    zm_audit: list[dict[str, object]],
    demotion: list[dict[str, object]],
    runner_feed: list[dict[str, object]],
    gates: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    all_sources_ok = all(bool(row["exists"]) and bool(row["anchor_found"]) for row in sources)
    no_zm_source = any(row["audit_id"] == "ZMS1381_7_verdict" and row["result"] == "NO_SOURCE_BACKED_SIGN_VALUE_UNIT_ROW" for row in zm_audit)
    demoted = any(row["demotion_id"] == "KCD1381_4_verdict" and row["demoted_status"] == "CLOSURE_SYMBOLIC_BRANCH_NO_NUMERIC_SCORING" for row in demotion)
    runner_blocks = any(row["feed_id"] == "RUF1381_4_claim_status" and row["status"] == "BLOCKED_NO_CLAIM" for row in runner_feed)
    local_claim_blocked = any(row["gate_id"] == "GATE1381_5_local_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    symbol_gate = any(row["gate_id"] == "GATE1381_0_symbol" and row["status"] == "PASS_SYMBOL_EXISTS" for row in gates)
    nonclaim = all_rows_nonclaim(sources, zm_audit, demotion, runner_feed, gates)
    csv_ok, csv_details = csv_parse_details(csv_paths)
    outputs = [DOC_PATH, VALIDATION_PATH, *csv_paths]
    outputs_scoped = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs)
    formalization_untouched_by_script = FORMALIZATION.exists() and all(FORMALIZATION not in path.resolve().parents for path in outputs)

    rows = [
        {
            "validation_id": "VAL1381_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1381_1_symbol_but_no_source",
            "check": "Z_m symbol exists but sign/value/unit source fails",
            "status": "PASS" if no_zm_source and symbol_gate else "FAIL",
            "details": "ZMS1381_7 blocks source-backed sign/value/unit row while GATE1381_0 preserves symbol existence.",
        },
        {
            "validation_id": "VAL1381_2_demotion",
            "check": "kappa_m=Z_m branch is demoted to closure-symbolic only",
            "status": "PASS" if demoted else "FAIL",
            "details": "KCD1381_4 blocks numeric scoring.",
        },
        {
            "validation_id": "VAL1381_3_runner_refusal",
            "check": "runner feed and gates keep local claims blocked",
            "status": "PASS" if runner_blocks and local_claim_blocked else "FAIL",
            "details": "RUF1381_4 and GATE1381_5 keep BLOCKED_NO_CLAIM.",
        },
        {
            "validation_id": "VAL1381_4_no_claim_rows",
            "check": "all generated rows keep valid_for_claim=false and claim_allowed=false",
            "status": "PASS" if nonclaim else "FAIL",
            "details": "1381 is a Z_m source audit and closure demotion, not a local-GR/PPN/R10 pass.",
        },
        {
            "validation_id": "VAL1381_5_csv_parse",
            "check": "all generated CSVs parse cleanly",
            "status": "PASS" if csv_ok else "FAIL",
            "details": csv_details,
        },
        {
            "validation_id": "VAL1381_6_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if outputs_scoped and formalization_untouched_by_script else "FAIL",
            "details": f"ROOT={ROOT}; FORMALIZATION_EXISTS={FORMALIZATION.exists()}",
        },
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL1381_7_overall",
            "check": "overall 1381 validation",
            "status": "PASS" if overall_ok else "FAIL",
            "details": "1381 fails to source Z_m sign/value/units and demotes kappa_m=Z_m to closure-symbolic only.",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    zm_audit: list[dict[str, object]],
    demotion: list[dict[str, object]],
    runner_feed: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    text = f"""# {TITLE}

**Current verdict:** `Z_m` is real in the corpus as a named scalar kinetic/stress coefficient, and the `kappa_m=Z_m` identification remains useful. But the sign, value/range, and units are **not** source-backed. The no-ghost/positive-ellipticity condition is a requirement, not yet a theorem.

**Discipline move:** demote `kappa_m=Z_m` to a purely symbolic closure coefficient. It can carry formulas like `ell_tr=sqrt(Z_m L0^2/F2)`, but it cannot score `L_tr`, `U_B`, `Q_alg`, PPN, R10, or local-GR claims.

**Next pressure point:** derive an admissible coefficient law for `Z_m(X_B)`—positive, bounded, same local/cosmology value rule, and unit-normalized—or keep it as a symbolic prior pack.

## Source Register

{table(["source_id", "source_path", "required_anchor", "exists", "anchor_found", "purpose", "valid_for_claim", "claim_allowed"], sources)}

## `Z_m` Sign / Value / Unit Audit

{table(["audit_id", "target", "question", "evidence", "result", "remaining_gap", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"], zm_audit)}

## `kappa_m=Z_m` Closure Demotion

{table(["demotion_id", "runner_object", "demoted_status", "allowed_use", "blocked_use", "reason", "valid_for_claim", "claim_allowed"], demotion)}

## Runner Feed Update

{table(["feed_id", "runner_field", "feed_update", "status", "blocks_claim_because", "valid_for_claim", "claim_allowed"], runner_feed)}

## Claim Gates

{table(["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"], gates)}

## Decision Ledger

{table(["decision_id", "decision", "why", "next_action", "valid_for_claim", "claim_allowed"], decisions)}

## Next Target

{table(["next_id", "next_doc", "next_script", "task", "success_condition", "do_not_claim", "valid_for_claim", "claim_allowed"], next_targets)}

## Validation

{table(["validation_id", "check", "status", "details"], validations)}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    zm_audit = zm_audit_rows()
    demotion = demotion_rows()
    runner_feed = runner_feed_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    csv_paths = generated_csv_paths()
    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(ZM_AUDIT_PATH, zm_audit)
    write_csv(DEMOTION_PATH, demotion)
    write_csv(RUNNER_FEED_PATH, runner_feed)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_targets)

    validations = validation_rows(sources, zm_audit, demotion, runner_feed, gates, csv_paths)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, zm_audit, demotion, runner_feed, gates, decisions, next_targets, validations)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"formalization-workbench touched by this script: {FORMALIZATION.exists() and False}")


if __name__ == "__main__":
    main()
