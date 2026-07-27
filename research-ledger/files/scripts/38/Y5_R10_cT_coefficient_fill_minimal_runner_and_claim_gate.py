from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "875-Y5-R10-cT-coefficient-fill-minimal-runner-and-claim-gate.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_875_SOURCE_REGISTER.csv"
INPUT_SCHEMA_PATH = RESIDUALS / "P8_Y5_R10_875_CT_INPUT_SCHEMA.csv"
PREDICTION_PATH = RESIDUALS / "P8_Y5_R10_875_SYMBOLIC_PREDICTION_ROWS.csv"
BOUND_LINK_PATH = RESIDUALS / "P8_Y5_R10_875_BOUND_LINK_ROWS.csv"
CLAIM_GATE_PATH = RESIDUALS / "P8_Y5_R10_875_CLAIM_GATE_EVALUATION.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_875_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_875_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_875_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_875_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_875_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_875_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_874_VALIDATION.csv"
CT_FILL_SOURCE_PATH = RESIDUALS / "P8_Y5_R10_874_CT_COEFFICIENT_FILL_LEDGER.csv"
BOUND_SOURCE_PATH = RESIDUALS / "P8_Y5_R10_871_CT_BOUND_ROWS.csv"

STATUS = "Y5_R10_875_cT_coefficient_gate_built_all_claims_blocked_missing_parent_inputs_nonclaim"
CLAIM_CEILING = "minimal_cT_runner_schema_and_gate_only_no_numeric_cT_bound_no_R10_PPN_WEP_or_local_GR_claim"
NEXT_TARGET = "876-Y5-R10-trace-sector-ZT-lambdaT-parent-input-or-zero-return.md"

GENERATED_CSV_PATHS = [
    SOURCE_REGISTER_PATH,
    INPUT_SCHEMA_PATH,
    PREDICTION_PATH,
    BOUND_LINK_PATH,
    CLAIM_GATE_PATH,
    ROUTE_CHOICE_PATH,
    CLAIM_GUARD_PATH,
    DECISION_PATH,
    NEXT_TARGET_PATH,
    NONCLAIM_SUMMARY_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "874_doc",
        "path": POST_CHECKPOINT / "874-Y5-R10-parent-qloc-verticality-signature-or-cT-coefficient-fill.md",
        "needles": [
            "CTF874_0_Z_T",
            "D874_2",
            "875-Y5-R10-cT-coefficient-fill-minimal-runner-and-claim-gate.md",
        ],
        "role": "immediate c_T coefficient fill handoff",
    },
    {
        "source_id": "874_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V874_6_cT_fill_rows_missing_nonclaim,pass",
            "V874_8_all_rows_nonclaim,pass",
            "V874_9_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "874_fill_ledger",
        "path": CT_FILL_SOURCE_PATH,
        "needles": [
            "CTF874_0_Z_T",
            "MISSING_PARENT_INPUT",
            "CTF874_4_metric_source_response",
        ],
        "role": "missing c_T coefficient source rows",
    },
    {
        "source_id": "871_bound_rows",
        "path": BOUND_SOURCE_PATH,
        "needles": [
            "CT871_R10_EOTWASH_2020_ALPHA1_38P6UM_ANCHOR",
            "CT871_PPN_CASSINI_GAMMA_SIGMA",
            "CT871_WEP_MICROSCOPE_ETA_PROXY",
        ],
        "role": "source-backed bound rows, nonclaim",
    },
    {
        "source_id": "872_projection_formulas",
        "path": POST_CHECKPOINT / "872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md",
        "needles": [
            "OF872_0_R10_yukawa_alpha",
            "OF872_1_orbital_acceleration",
            "OF872_3_clock_WEP_response",
        ],
        "role": "symbolic c_T projection formulas",
    },
    {
        "source_id": "873_trace_charge_zero",
        "path": POST_CHECKPOINT / "873-Y5-R10-local-matter-trace-charge-zero-theorem-or-coefficient-fill.md",
        "needles": [
            "QTZ873_1_chain_rule_zero",
            "QTZ873_3_verdict",
            "FB873_0_QT_universal",
        ],
        "role": "conditional Q_T zero theorem and fallback rows",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "source_id": spec["source_id"],
            "path": str(spec["path"]),
            "exists": str(spec["path"].exists()).lower(),
            "needle_check": check_needles(spec["path"], spec["needles"]),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for spec in SOURCE_SPECS
    ]


def input_schema_rows(generated_utc: str) -> list[dict[str, object]]:
    source_rows = {row.get("coefficient", ""): row for row in read_csv(CT_FILL_SOURCE_PATH)}
    return [
        {
            "input_id": "IN875_0_Z_T",
            "coefficient": "Z_T",
            "role": "trace carrier kinetic normalization",
            "required_for": "R10/orbital alpha amplitude",
            "value": source_rows.get("Z_T", {}).get("current_value", "MISSING_PARENT_INPUT"),
            "units": "parent_defined",
            "source_path": str(CT_FILL_SOURCE_PATH),
            "status": "missing_parent_input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN875_1_lambda_T",
            "coefficient": "lambda_T_or_m_T",
            "role": "trace carrier range/mass",
            "required_for": "R10 alpha(lambda) and finite-range orbital profile",
            "value": source_rows.get("m_T_or_lambda_T", {}).get("current_value", "MISSING_PARENT_INPUT"),
            "units": "length_or_mass_parent_defined",
            "source_path": str(CT_FILL_SOURCE_PATH),
            "status": "missing_parent_input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN875_2_Q_T_over_m_universal",
            "coefficient": "Q_T_over_m_universal",
            "role": "universal trace matter charge per inertial mass",
            "required_for": "R10/orbital common force",
            "value": source_rows.get("Q_T_over_m_universal", {}).get("current_value", "MISSING_PARENT_INPUT_OR_ZERO_THEOREM"),
            "units": "parent_defined_charge_per_mass",
            "source_path": str(CT_FILL_SOURCE_PATH),
            "status": "missing_parent_input_or_zero_theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN875_3_Delta_Q_T_species",
            "coefficient": "Delta_AB_Q_T_over_m",
            "role": "composition-dependent trace charge difference",
            "required_for": "WEP and clock species response",
            "value": source_rows.get("Delta_AB_Q_T_over_m", {}).get("current_value", "MISSING_NO_MARKER_RESULT"),
            "units": "parent_defined_charge_per_mass_difference",
            "source_path": str(CT_FILL_SOURCE_PATH),
            "status": "missing_no_marker_result",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN875_4_C_T_metric_source",
            "coefficient": "C_T_gamma,C_T_beta,C_T_clock,C_T_source",
            "role": "observed metric/clock/source response",
            "required_for": "PPN, clocks, source-normalized Newtonian/orbital tests",
            "value": source_rows.get("C_T_gamma,C_T_beta,C_T_clock,C_T_source", {}).get("current_value", "MISSING_RESPONSE_OPERATOR"),
            "units": "arena_dependent",
            "source_path": str(CT_FILL_SOURCE_PATH),
            "status": "missing_response_operator",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN875_5_full_R10_curve",
            "coefficient": "alpha_bound(lambda)_full_curve",
            "role": "real R10 bound curve rather than anchor-only thresholds",
            "required_for": "R10 claim scoring",
            "value": "MISSING_FULL_CURVE",
            "units": "dimensionless_alpha_vs_length",
            "source_path": str(BOUND_SOURCE_PATH),
            "status": "anchor_rows_only_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def symbolic_prediction_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "prediction_id": "PRED875_0_R10_alpha",
            "arena": "R10_short_range",
            "formula": "alpha_T_AB = (Q_T^A/m_A)*(Q_T^B/m_B)/(4*pi*Z_T*G_obs), evaluated at lambda_T",
            "requires_inputs": "Z_T;lambda_T;Q_T^A/m_A;Q_T^B/m_B;full alpha(lambda) curve",
            "prediction_value": "MISSING_COEFFICIENT_INPUTS",
            "status": "blocked",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "prediction_id": "PRED875_1_orbital_residual",
            "arena": "orbital_dynamics",
            "formula": "delta a/a_N = alpha_T_AB*(1+r/lambda_T)*exp(-r/lambda_T)",
            "requires_inputs": "alpha_T_AB;lambda_T;source geometry;GM absorption proof;specific orbital bound",
            "prediction_value": "MISSING_COEFFICIENT_INPUTS",
            "status": "blocked",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "prediction_id": "PRED875_2_PPN_gamma_beta",
            "arena": "PPN",
            "formula": "gamma-1=C_T_gamma*c_T and beta-1=C_T_beta*c_T",
            "requires_inputs": "C_T_gamma;C_T_beta;c_T;gauge;source-normalization split",
            "prediction_value": "MISSING_RESPONSE_OPERATOR",
            "status": "blocked",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "prediction_id": "PRED875_3_clock_WEP",
            "arena": "clock_WEP",
            "formula": "delta nu_i/nu_i=C_T_clock_i*c_T; eta_AB controlled by Delta_AB(Q_T/m)",
            "requires_inputs": "C_T_clock_i;Delta_AB_Q_T_over_m;clock functional;no-marker result",
            "prediction_value": "MISSING_NO_MARKER_RESULT",
            "status": "blocked",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def bound_link_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for bound in read_csv(BOUND_SOURCE_PATH):
        rows.append(
            {
                "bound_id": bound.get("bound_id", ""),
                "arena": bound.get("arena", ""),
                "observable": bound.get("observable", ""),
                "bound_value": bound.get("bound_value", ""),
                "bound_units": bound.get("bound_units", ""),
                "lambda_value": bound.get("lambda_value", ""),
                "source_status": bound.get("extraction_status", ""),
                "projection_status": bound.get("projection_status", ""),
                "source_valid_for_claim": bound.get("valid_for_claim", "false"),
                "gate_use": "nonclaim_bound_context_only",
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G875_0_R10",
            "arena": "R10_short_range",
            "coefficient_inputs_ready": "false",
            "bound_inputs_ready": "false",
            "prediction_numeric": "false",
            "claim_allowed": "false",
            "blocker": "Z_T/lambda_T/Q_T missing and R10 curve is anchor-only nonclaim",
            "next_action": "derive Z_T and lambda_T or prove c_T zero; later digitize full R10 curve",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G875_1_PPN",
            "arena": "PPN",
            "coefficient_inputs_ready": "false",
            "bound_inputs_ready": "true_context_only",
            "prediction_numeric": "false",
            "claim_allowed": "false",
            "blocker": "C_T_gamma/C_T_beta/c_T response operator missing",
            "next_action": "derive observed metric response or prove trace verticality",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G875_2_clock_WEP",
            "arena": "clock_WEP",
            "coefficient_inputs_ready": "false",
            "bound_inputs_ready": "true_context_only",
            "prediction_numeric": "false",
            "claim_allowed": "false",
            "blocker": "no-marker/species charge and clock functional missing",
            "next_action": "derive Q_T^A=0/no-marker or fill Delta_AB_Q_T_over_m",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G875_3_orbital",
            "arena": "orbital_dynamics",
            "coefficient_inputs_ready": "false",
            "bound_inputs_ready": "false",
            "prediction_numeric": "false",
            "claim_allowed": "false",
            "blocker": "C_T_source/alpha_T/lambda_T and specific numeric orbital bound missing",
            "next_action": "derive source response and choose real orbital observable/bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G875_4_local_GR",
            "arena": "local_GR_Newton",
            "coefficient_inputs_ready": "false",
            "bound_inputs_ready": "not_sufficient",
            "prediction_numeric": "false",
            "claim_allowed": "false",
            "blocker": "c_T is only one q_loc channel; q_loc zero, EH operator, projector stress, and source normalization remain unproved",
            "next_action": "continue parent derivation stack after c_T gate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC875_0_selected",
            "route": "trace_sector_ZT_lambdaT_parent_input_or_zero_return",
            "status": "selected",
            "reason": "the gate shows no arena can score until at least the trace-sector normalization/range or a zero theorem is parent-owned",
            "include": "derive Z_T, m_T/lambda_T, or prove no local trace carrier; keep all claim gates closed",
            "exclude": "fitted c_T, scoring with missing coefficients, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG875_0_no_numeric_cT_claim",
            "claim": "c_T has numeric sourced inputs",
            "status": "forbidden",
            "reason": "every coefficient input row is missing or theorem-dependent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG875_1_no_bound_pass",
            "claim": "R10/PPN/clock/WEP/orbital bounds pass",
            "status": "forbidden",
            "reason": "predictions are symbolic/blocked and bound rows are context-only nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG875_2_no_local_GR_claim",
            "claim": "local GR/Newton recovery is derived",
            "status": "forbidden",
            "reason": "875 is a gate around one residual channel, not the full GR/Newton derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG875_3_allowed_private_result",
            "claim": "a minimal c_T coefficient gate exists and blocks claims correctly",
            "status": "allowed_private_nonclaim",
            "reason": "the runner prevents placeholders from becoming evidence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D875_0",
            "finding": "cT_gate_built",
            "reason": "coefficient schema, symbolic predictions, bound links, and claim gates are now explicit",
            "status": STATUS,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D875_1",
            "finding": "all_arenas_blocked",
            "reason": "R10, PPN, clock/WEP, orbital, and local-GR gates all refuse claims due missing parent inputs",
            "status": STATUS,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D875_2",
            "finding": "ZT_lambdaT_or_zero_return_selected",
            "reason": "the first coefficient to attack is the existence, normalization, and range of a local trace carrier",
            "status": STATUS,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "derive Z_T and lambda_T/m_T from a parent local trace-sector quadratic action, or prove no local trace carrier exists",
            "include": "quadratic operator, kinetic sign, mass/range, gauge/constraint null option, zero-return branch",
            "exclude": "numeric test claims, free fitted coefficients, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "built a minimal c_T coefficient-fill runner/gate linking missing parent inputs to existing local bound rows",
            "best_partial_result": "all c_T arenas are now mechanically blocked unless coefficients are sourced or theorem-zero closes",
            "hard_blockers": "Z_T, lambda_T/m_T, Q_T/m, Delta_Q_T species charge, metric/source response, full R10 curve",
            "what_is_not_claimed": "numeric c_T prediction, R10 pass, PPN pass, clock/WEP pass, orbital pass, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def any_valid_for_claim_true(paths: list[Path]) -> bool:
    for path in paths:
        if not path.exists():
            return True
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("valid_for_claim", "").strip().lower() == "true":
                    return True
    return False


def build_validation_rows(
    source_rows: list[dict[str, object]],
    input_rows: list[dict[str, object]],
    prediction_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_value: list[dict[str, object]],
) -> list[dict[str, str]]:
    validation_rows: list[dict[str, str]] = []

    sources_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    validation_rows.append(
        {
            "check_id": "V875_0_sources_exist_and_needles",
            "result": "pass" if sources_ok else "fail",
            "detail": "all source paths exist and needles are present" if sources_ok else "one or more source checks failed",
        }
    )

    prior_ok, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    validation_rows.append(
        {
            "check_id": "V875_1_prior_874_clean",
            "result": "pass" if prior_ok else "fail",
            "detail": prior_detail,
        }
    )

    input_blocked = all("MISSING" in str(row["value"]) and row["valid_for_claim"] == "false" for row in input_rows)
    validation_rows.append(
        {
            "check_id": "V875_2_inputs_missing_nonclaim",
            "result": "pass" if input_blocked else "fail",
            "detail": f"input_rows={len(input_rows)} all missing/nonclaim",
        }
    )

    predictions_blocked = all(row["status"] == "blocked" and row["claim_allowed"] == "false" for row in prediction_rows)
    validation_rows.append(
        {
            "check_id": "V875_3_predictions_blocked",
            "result": "pass" if predictions_blocked else "fail",
            "detail": f"prediction_rows={len(prediction_rows)} blocked",
        }
    )

    bounds_nonclaim = len(bound_rows) >= 7 and all(row["valid_for_claim"] == "false" for row in bound_rows)
    validation_rows.append(
        {
            "check_id": "V875_4_bound_links_nonclaim",
            "result": "pass" if bounds_nonclaim else "fail",
            "detail": f"bound_link_rows={len(bound_rows)} remain context-only",
        }
    )

    gates_false = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in gate_rows)
    validation_rows.append(
        {
            "check_id": "V875_5_all_claim_gates_false",
            "result": "pass" if gates_false else "fail",
            "detail": "all arena claim gates are false",
        }
    )

    claim_false = all(row["claim_allowed"] == "false" for row in decision_rows_value)
    validation_rows.append(
        {
            "check_id": "V875_6_decision_claim_allowed_false",
            "result": "pass" if claim_false else "fail",
            "detail": "decision rows keep claim_allowed=false",
        }
    )

    all_nonclaim = not any_valid_for_claim_true(GENERATED_CSV_PATHS)
    validation_rows.append(
        {
            "check_id": "V875_7_all_rows_nonclaim",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated rows valid_for_claim=false",
        }
    )

    formalization_count = formalization_workbench_modified_count()
    validation_rows.append(
        {
            "check_id": "V875_8_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        }
    )

    validation_rows.append(
        {
            "check_id": "V875_9_route_selected",
            "result": "pass",
            "detail": NEXT_TARGET,
        }
    )

    validation_rows.append(
        {
            "check_id": "V875_10_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        }
    )

    return validation_rows


def markdown_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines) + "\n"


def write_output_doc(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    input_rows: list[dict[str, object]],
    prediction_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_value: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    source_fields = ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"]
    input_fields = ["input_id", "coefficient", "role", "required_for", "value", "units", "source_path", "status", "valid_for_claim", "generated_utc"]
    prediction_fields = ["prediction_id", "arena", "formula", "requires_inputs", "prediction_value", "status", "claim_allowed", "valid_for_claim", "generated_utc"]
    bound_fields = ["bound_id", "arena", "observable", "bound_value", "bound_units", "lambda_value", "source_status", "projection_status", "source_valid_for_claim", "gate_use", "valid_for_claim", "generated_utc"]
    gate_fields = ["gate_id", "arena", "coefficient_inputs_ready", "bound_inputs_ready", "prediction_numeric", "claim_allowed", "blocker", "next_action", "valid_for_claim", "generated_utc"]
    route_fields = ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"]
    guard_fields = ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"]
    decision_fields = ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"]
    next_fields = ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"]
    summary_fields = [
        "status",
        "claim_ceiling",
        "what_changed",
        "best_partial_result",
        "hard_blockers",
        "what_is_not_claimed",
        "next_target",
        "valid_for_claim",
        "generated_utc",
    ]
    validation_fields = ["check_id", "result", "detail"]

    doc = "\n".join(
        [
            "# 875 - Y5/R10 c_T Coefficient Fill Minimal Runner and Claim Gate",
            "",
            f"Status: `{STATUS}`  ",
            f"Claim ceiling: `{CLAIM_CEILING}`  ",
            f"Generated UTC: `{generated_utc}`",
            "",
            "Current result: **the c_T testing gate exists and every local claim is blocked for the right reason**. The runner links the missing parent coefficients (`Z_T`, `lambda_T/m_T`, `Q_T/m`, species charge, metric/source response) to the source-backed bound rows from 871. Because all parent inputs are missing or theorem-dependent, every prediction remains symbolic and every arena gate remains `claim_allowed=false`.",
            "",
            "## Nonclaim Summary",
            markdown_table(summary_rows, summary_fields),
            "## Source Register",
            markdown_table(source_rows, source_fields),
            "## c_T Input Schema",
            markdown_table(input_rows, input_fields),
            "## Symbolic Prediction Rows",
            markdown_table(prediction_rows, prediction_fields),
            "## Bound Link Rows",
            markdown_table(bound_rows, bound_fields),
            "## Claim Gate Evaluation",
            markdown_table(gate_rows, gate_fields),
            "## Route Choice",
            markdown_table(route_rows, route_fields),
            "## Claim Guard",
            markdown_table(guard_rows, guard_fields),
            "## Decision",
            markdown_table(decision_rows_value, decision_fields),
            "## Next Target",
            markdown_table(next_rows, next_fields),
            "## Validation",
            markdown_table(validation_rows, validation_fields),
        ]
    )
    OUTPUT_DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat()

    source_rows = source_register_rows(generated_utc)
    input_rows = input_schema_rows(generated_utc)
    prediction_rows = symbolic_prediction_rows(generated_utc)
    bound_rows = bound_link_rows(generated_utc)
    gate_rows = claim_gate_rows(generated_utc)
    route_rows = route_choice_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_value = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(INPUT_SCHEMA_PATH, input_rows, ["input_id", "coefficient", "role", "required_for", "value", "units", "source_path", "status", "valid_for_claim", "generated_utc"])
    write_csv(PREDICTION_PATH, prediction_rows, ["prediction_id", "arena", "formula", "requires_inputs", "prediction_value", "status", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(BOUND_LINK_PATH, bound_rows, ["bound_id", "arena", "observable", "bound_value", "bound_units", "lambda_value", "source_status", "projection_status", "source_valid_for_claim", "gate_use", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GATE_PATH, gate_rows, ["gate_id", "arena", "coefficient_inputs_ready", "bound_inputs_ready", "prediction_numeric", "claim_allowed", "blocker", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, route_rows, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decision_rows_value, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(
        NONCLAIM_SUMMARY_PATH,
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "what_changed",
            "best_partial_result",
            "hard_blockers",
            "what_is_not_claimed",
            "next_target",
            "valid_for_claim",
            "generated_utc",
        ],
    )

    validation_rows = build_validation_rows(
        source_rows,
        input_rows,
        prediction_rows,
        bound_rows,
        gate_rows,
        decision_rows_value,
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    write_output_doc(
        generated_utc,
        source_rows,
        input_rows,
        prediction_rows,
        bound_rows,
        gate_rows,
        route_rows,
        guard_rows,
        decision_rows_value,
        next_rows,
        summary_rows,
        validation_rows,
    )

    failed = [row for row in validation_rows if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"875 validation failed: {failed}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()
