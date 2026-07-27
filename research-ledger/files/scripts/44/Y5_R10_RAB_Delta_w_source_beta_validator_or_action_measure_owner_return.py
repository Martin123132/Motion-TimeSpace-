from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1388-Y5-R10-RAB-Delta-w-source-beta-validator-or-action-measure-owner-return.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1388_SOURCE_REGISTER.csv"
VALIDATOR_PATH = SRC_DIR / "P8_Y5_R10_1388_DELTA_W_SOURCE_BETA_VALIDATOR.csv"
OWNER_RETURN_GATE_PATH = SRC_DIR / "P8_Y5_R10_1388_ACTION_MEASURE_OWNER_RETURN_GATE.csv"
SCORING_REFUSAL_PATH = SRC_DIR / "P8_Y5_R10_1388_SCORING_REFUSAL_MATRIX.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1388_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1388_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1388_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1388_VALIDATION.csv"

STATUS = (
    "delta_w_source_beta_validator_ready_scoring_refused_"
    "action_measure_owner_return_unsigned_local_claims_blocked"
)
CLAIM_CEILING = (
    "strict_validator_and_owner_return_gate_only_no_Delta_w_value_no_beta_score_"
    "no_R10_no_PPN_no_WEP_no_Newton_no_clock_no_orbital_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1388_0_1387_doc",
        "source_path": "1387-Y5-R10-RAB-action-weight-exclusion-or-source-beta-first-fill.md",
        "required_anchor": "NEXT1387_0_1388",
        "purpose": "handoff to strict Delta_w/source-beta validator",
    },
    {
        "source_id": "SRC1388_1_1387_next",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1387_NEXT_TARGET.csv",
        "required_anchor": "NEXT1387_0_1388",
        "purpose": "machine-readable 1388 target",
    },
    {
        "source_id": "SRC1388_2_1387_first_fill",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1387_DELTA_W_SOURCE_BETA_FIRST_FILL.csv",
        "required_anchor": "DWB1387_6_first_fill_verdict",
        "purpose": "Delta_w/source-beta first-fill rows to validate",
    },
    {
        "source_id": "SRC1388_3_1387_exclusion",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1387_ACTION_WEIGHT_EXCLUSION_AUDIT.csv",
        "required_anchor": "AWE1387_7_verdict",
        "purpose": "action-weight counterexample remains active",
    },
    {
        "source_id": "SRC1388_4_1387_arena",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1387_ARENA_IMPACT_MAP.csv",
        "required_anchor": "AIM1387_5_local_GR",
        "purpose": "local GR arena remains blocked by action-weight residual",
    },
    {
        "source_id": "SRC1388_5_1387_gate",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1387_CLAIM_GATE.csv",
        "required_anchor": "GATE1387_5_local_claim",
        "purpose": "1387 claim refusal gate",
    },
    {
        "source_id": "SRC1388_6_1386_beta_runner",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1386_BETA_ACQUISITION_RUNNER_ROWS.csv",
        "required_anchor": "BAR1386_7_runner_verdict",
        "purpose": "finite beta acquisition runner remains schema-only",
    },
    {
        "source_id": "SRC1388_7_1078_action_measure",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv",
        "required_anchor": "AM1078_4_verdict",
        "purpose": "action-measure owner route is unsigned",
    },
    {
        "source_id": "SRC1388_8_1078_object_language",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv",
        "required_anchor": "OL1078_4_verdict",
        "purpose": "object-language route is unsigned",
    },
    {
        "source_id": "SRC1388_9_1079_current_owner",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
        "required_anchor": "NCO1079_5_species_action_weight",
        "purpose": "current owner cannot kill pre-variation weights",
    },
    {
        "source_id": "SRC1388_10_1229_single_GN",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv",
        "required_anchor": "CLC1229_7_single_GN_normalization",
        "purpose": "single-GN calibration clause and limits",
    },
    {
        "source_id": "SRC1388_11_1036_beta_product",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv",
        "required_anchor": "BETA1036_2_R10_alpha_match",
        "purpose": "finite source-test beta product law",
    },
    {
        "source_id": "SRC1388_12_this_script",
        "source_path": "scripts/Y5_R10_RAB_Delta_w_source_beta_validator_or_action_measure_owner_return.py",
        "required_anchor": "STATUS",
        "purpose": "1388 generator",
    },
]


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        columns = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: clean(row.get(column, "")) for column in columns})


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(clean(row.get(column, "")).replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def anchor_found(path: Path, anchor: str) -> bool:
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCE_ROWS:
        source_path = ROOT / source["source_path"]
        exists = source_path.exists()
        found = anchor_found(source_path, source["required_anchor"])
        rows.append(
            {
                **source,
                "exists": str(exists),
                "anchor_found": str(found),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def validator_rows() -> list[dict[str, str]]:
    return [
        {
            "validator_id": "DWV1388_0_input_integrity",
            "requirement": "DWB1387 rows are present and remain explicitly nonclaim",
            "required_inputs": "DWB1387_0_w_common;DWB1387_1_Delta_w_A;DWB1387_2_beta_w_source;DWB1387_3_beta_w_test;DWB1387_4_beta_product_guard;DWB1387_5_no_absorption_guard;DWB1387_6_first_fill_verdict",
            "pass_for_schema": "True",
            "pass_for_numeric": "False",
            "pass_for_claim": "False",
            "current_status": "SCHEMA_READY_NONCLAIM",
            "failure_mode": "first-fill rows exist, but no value/bound/source package is present",
            "next_action": "validate candidate fills only if every row remains sourced and nonplaceholder",
            "valid_for_claim": "False",
        },
        {
            "validator_id": "DWV1388_1_common_calibration",
            "requirement": "common w_* may be absorbed only if universal and derivative/source/range/frame silent",
            "required_inputs": "w_A=w_* theorem; partial_t,r,A,lambda,frame ln w_A=0; single G_N calibration convention",
            "pass_for_schema": "True",
            "pass_for_numeric": "False",
            "pass_for_claim": "False",
            "current_status": "MISSING_COMMON_CALIBRATION_THEOREM_AND_DERIVATIVE_SILENCE",
            "failure_mode": "measured-G absorption would be a cheat unless common factor and silence are proved",
            "next_action": "derive common-calibration silence or keep Delta_w_A active",
            "valid_for_claim": "False",
        },
        {
            "validator_id": "DWV1388_2_relative_weight",
            "requirement": "Delta_w_A must be theorem-zero, value-filled, or upper-bounded by material/source class",
            "required_inputs": "Delta_w_A value or bound; material/source class A; provenance; units dimensionless",
            "pass_for_schema": "True",
            "pass_for_numeric": "False",
            "pass_for_claim": "False",
            "current_status": "MISSING_DELTA_W_A_VALUE_OR_BOUND",
            "failure_mode": "source normalization and WEP material dependence cannot be scored",
            "next_action": "build a material/source map or return to parent action-measure owner proof",
            "valid_for_claim": "False",
        },
        {
            "validator_id": "DWV1388_3_source_beta",
            "requirement": "beta_w_source requires canonical field convention and source weight function",
            "required_inputs": "canonical phi; w_S(phi); beta_w,S=partial_phi ln w_S; source worldtube/readout map",
            "pass_for_schema": "True",
            "pass_for_numeric": "False",
            "pass_for_claim": "False",
            "current_status": "MISSING_SOURCE_BETA_WEIGHT_FUNCTION",
            "failure_mode": "R10 and local finite-force source leg cannot be evaluated",
            "next_action": "source or derive w_S(phi), otherwise keep source beta blocked",
            "valid_for_claim": "False",
        },
        {
            "validator_id": "DWV1388_4_test_beta",
            "requirement": "beta_w_test requires test-material response in the same beta convention",
            "required_inputs": "canonical phi; w_T(phi); beta_w,T=partial_phi ln w_T; test material/composition map",
            "pass_for_schema": "True",
            "pass_for_numeric": "False",
            "pass_for_claim": "False",
            "current_status": "MISSING_TEST_BETA_WEIGHT_FUNCTION",
            "failure_mode": "WEP, R10 test leg, and clock material response cannot be evaluated",
            "next_action": "source or derive w_T(phi) and material classes",
            "valid_for_claim": "False",
        },
        {
            "validator_id": "DWV1388_5_beta_product",
            "requirement": "finite exchange scoring must use source-test product, not a naked coupling shortcut",
            "required_inputs": "beta_w,S; beta_w,T; K_w(lambda); epsilon_tail(lambda); mu_m^2; convention lock",
            "pass_for_schema": "True",
            "pass_for_numeric": "False",
            "pass_for_claim": "False",
            "current_status": "PRODUCT_FORMULA_READY_VALUES_MISSING",
            "failure_mode": "alpha_w(lambda)=K_w beta_w,S beta_w,T + epsilon_tail cannot be computed",
            "next_action": "refuse any numeric alpha(lambda) until both beta legs and kernel are sourced",
            "valid_for_claim": "False",
        },
        {
            "validator_id": "DWV1388_6_arena_kernels",
            "requirement": "each local arena needs its own projection kernel and source/material map",
            "required_inputs": "WEP kernel; R10 kernel; PPN residual vector; clock kernel; orbital/source kernel; local-GR residual map",
            "pass_for_schema": "True",
            "pass_for_numeric": "False",
            "pass_for_claim": "False",
            "current_status": "MISSING_ARENA_PROJECTIONS",
            "failure_mode": "a coefficient pack cannot be promoted into Newton/WEP/R10/PPN/local-GR evidence",
            "next_action": "fill arena-specific kernels after Delta_w/beta rows are sourced",
            "valid_for_claim": "False",
        },
        {
            "validator_id": "DWV1388_7_verdict",
            "requirement": "strict validator must refuse scoring unless every coupling input is sourced",
            "required_inputs": "DWV1388_1 through DWV1388_6 all numeric/claim pass",
            "pass_for_schema": "True",
            "pass_for_numeric": "False",
            "pass_for_claim": "False",
            "current_status": "VALIDATOR_READY_SCORING_BLOCKED",
            "failure_mode": "common calibration, Delta_w_A, source beta, test beta, product kernel, and arena projections remain missing",
            "next_action": "choose between parent owner proof and material/source map acquisition",
            "valid_for_claim": "False",
        },
    ]


def owner_return_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "return_id": "AMR1388_0_object_language_owner",
            "theorem_route": "forbid inert species/source-only scalar slots in parent object language",
            "required_parent_signature": "parent grammar admits no independent positive w_A label except real fields/currents/constants with transformation law",
            "current_status": "UNSIGNED_RETURN_ROUTE_OL1078_4",
            "if_signed": "kills pre-variation label weights before finite Delta_w rows are needed",
            "if_unsigned": "Delta_w_A remains an allowed counterexample input",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "return_id": "AMR1388_1_action_measure_owner",
            "theorem_route": "single hbar/action-measure owner across ordinary matter",
            "required_parent_signature": "one action scale and measure owner fixes all ordinary matter sector weights up to common calibration",
            "current_status": "UNSIGNED_RETURN_ROUTE_AM1078_4",
            "if_signed": "relative action weights are inadmissible or gauge-equivalent to common calibration",
            "if_unsigned": "species/source pre-variation weights survive",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "return_id": "AMR1388_2_current_owner",
            "theorem_route": "variation-before-readout Hilbert/current owner",
            "required_parent_signature": "source tensor is read only after the single common action is varied",
            "current_status": "PARTIAL_NCO1079_5_NOT_ENOUGH",
            "if_signed": "kills post-variation rescaling, but still needs pre-action weight exclusion",
            "if_unsigned": "cannot support local-GR source universality",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "return_id": "AMR1388_3_single_GN_calibration",
            "theorem_route": "single measured-G_N normalization",
            "required_parent_signature": "only a universal derivative-silent w_* may be absorbed into G_N",
            "current_status": "CALIBRATION_POLICY_ONLY_CLC1229_7",
            "if_signed": "common factor is harmless calibration",
            "if_unsigned": "measured-G absorption cannot hide Delta_w_A or beta_w,A",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "return_id": "AMR1388_4_return_verdict",
            "theorem_route": "owner-return supersedes finite Delta_w rows only if all owner clauses close together",
            "required_parent_signature": "object-language owner + action-measure owner + current owner + derivative silence",
            "current_status": "RETURN_BLOCKED_PARENT_UNSIGNED",
            "if_signed": "return to zero-theorem branch and demote finite rows to guards",
            "if_unsigned": "continue material/source map acquisition with all rows nonclaim",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def scoring_refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "SFM1388_0_Newton",
            "arena": "Newton/source normalization",
            "score_equation": "G_N,obs M_A -> G_N w_A M_A; only w_A=w_* with derivative silence is calibration",
            "missing_inputs": "Delta_w_A theorem-zero or sourced bound; common calibration; source class map",
            "status": "BLOCKED_NO_SCORE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "refusal_id": "SFM1388_1_WEP",
            "arena": "WEP/source charge",
            "score_equation": "eta_AB requires Delta_w_AB and/or Delta beta_AB with material/source kernel",
            "missing_inputs": "composition/material classes; Delta_w_AB; beta_w,A matrix; WEP projection kernel",
            "status": "BLOCKED_NO_SCORE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "refusal_id": "SFM1388_2_R10",
            "arena": "R10 alpha(lambda)",
            "score_equation": "alpha_w(lambda)=K_w(lambda) beta_w,S beta_w,T + epsilon_tail(lambda)",
            "missing_inputs": "beta_w,S; beta_w,T; K_w(lambda); epsilon_tail; mu_m^2; real bound curve",
            "status": "BLOCKED_NO_SCORE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "refusal_id": "SFM1388_3_PPN",
            "arena": "PPN/local residual vector",
            "score_equation": "delta gamma, delta beta, delta U_source require calibrated weak-field source residuals",
            "missing_inputs": "source normalization after measured-G calibration; second-order beta residue; local projection kernel",
            "status": "BLOCKED_NO_SCORE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "refusal_id": "SFM1388_4_clocks_orbital",
            "arena": "clocks/constants/orbital systems",
            "score_equation": "clock/orbital response needs material standard, source class, and time/range silence",
            "missing_inputs": "clock material beta; orbital source map; derivative silence; arena-specific bounds",
            "status": "BLOCKED_NO_SCORE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "refusal_id": "SFM1388_5_local_GR",
            "arena": "local GR reduction",
            "score_equation": "local GR requires universal matter source plus residual vector below all local bounds",
            "missing_inputs": "action-weight theorem-zero or complete finite residual vector; PPN/R10/WEP/clock/orbital gates",
            "status": "BLOCKED_NO_SCORE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE1388_0_sources",
            "gate": "all cited local sources exist and anchors are present",
            "status": "PASS",
            "reason": "source register validates against the local corpus",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1388_1_validator",
            "gate": "Delta_w/source-beta validator exists",
            "status": "PASS_SCHEMA_ONLY",
            "reason": "validator rows define exact inputs required before scoring",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1388_2_numeric",
            "gate": "finite coupling rows can score numeric alpha or residuals",
            "status": "BLOCKED_VALUES_MISSING",
            "reason": "Delta_w_A, beta_w,S, beta_w,T, K_w, tails, and arena kernels remain unsourced",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1388_3_owner_return",
            "gate": "parent action-measure/object-language owner theorem closes",
            "status": "BLOCKED_PARENT_UNSIGNED",
            "reason": "object-language, action-measure, current-owner, and derivative-silence clauses do not close together",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1388_4_scoring",
            "gate": "Newton/WEP/R10/PPN/clock/orbital scores may be reported",
            "status": "BLOCKED_NO_SCORE",
            "reason": "strict validator refuses all arena scores until source-backed rows exist",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1388_5_local_claim",
            "gate": "local GR reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1388 is a coupling validator and owner-return gate, not a derived GR limit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1388_0_no_scoring",
            "decision": "do not score Delta_w/beta_w rows yet",
            "because": "the first-fill rows are schema-ready but have no sourced values, bounds, or parent-zero theorem",
            "next_action": "refuse numeric alpha(lambda), PPN, WEP, Newton, clock, orbital, and local-GR promotion",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1388_1_owner_return",
            "decision": "preserve a clean theorem route back to parent action-measure ownership",
            "because": "a signed owner theorem would be cleaner than finite nuisance coefficients",
            "next_action": "if new evidence appears, close object-language + action-measure + current-owner + derivative-silence clauses together",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1388_2_best_next_move",
            "decision": "build material/source map or make a targeted owner proof attempt",
            "because": "the current bottleneck is not algebraic prettiness but missing coupling provenance",
            "next_action": "try to source/derive Delta_w_A, beta_w_source, beta_w_test by material/source class while keeping claims blocked",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1388_0_1389",
            "next_doc": "1389-Y5-R10-RAB-Delta-w-material-source-map-or-action-measure-owner-proof.md",
            "next_script": "scripts/Y5_R10_RAB_Delta_w_material_source_map_or_action_measure_owner_proof.py",
            "task": "either source/derive material and source classes for Delta_w_A, beta_w_source, and beta_w_test, or make a targeted parent action-measure owner proof attempt",
            "success_condition": "no local scoring unless Delta_w/beta rows are theorem-zero or source-backed with units, material/source map, beta convention, arena kernels, and nonplaceholder provenance",
            "do_not_claim": "local GR;Newton limit;PPN pass;R10 pass;WEP pass;q_loc=0;numeric alpha(lambda);GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def csv_rows(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validation_rows(
    sources: list[dict[str, str]],
    validator: list[dict[str, str]],
    owner_gate: list[dict[str, str]],
    refusals: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_pass = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    first_fill_ids = {
        row["fill_id"]
        for row in csv_rows(Path("source-intake/mts_residuals/P8_Y5_R10_1387_DELTA_W_SOURCE_BETA_FIRST_FILL.csv"))
    }
    required_fill_ids = {
        "DWB1387_0_w_common",
        "DWB1387_1_Delta_w_A",
        "DWB1387_2_beta_w_source",
        "DWB1387_3_beta_w_test",
        "DWB1387_4_beta_product_guard",
        "DWB1387_5_no_absorption_guard",
        "DWB1387_6_first_fill_verdict",
    }
    input_integrity = required_fill_ids.issubset(first_fill_ids)
    validator_verdict = any(
        row["validator_id"] == "DWV1388_7_verdict"
        and row["pass_for_schema"] == "True"
        and row["pass_for_numeric"] == "False"
        and row["pass_for_claim"] == "False"
        and row["valid_for_claim"] == "False"
        for row in validator
    )
    all_validator_nonclaim = all(
        row["valid_for_claim"] == "False"
        and row["pass_for_numeric"] == "False"
        and row["pass_for_claim"] == "False"
        for row in validator
    )
    owner_blocked = any(
        row["return_id"] == "AMR1388_4_return_verdict"
        and row["current_status"] == "RETURN_BLOCKED_PARENT_UNSIGNED"
        and row["claim_allowed"] == "False"
        for row in owner_gate
    )
    refusals_blocked = all(
        row["status"] == "BLOCKED_NO_SCORE"
        and row["claim_allowed"] == "False"
        and row["valid_for_claim"] == "False"
        for row in refusals
    )
    local_claim_blocked = any(
        row["gate_id"] == "GATE1388_5_local_claim"
        and row["status"] == "BLOCKED_NO_CLAIM"
        and row["claim_allowed"] == "False"
        for row in gates
    )
    outputs = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        VALIDATOR_PATH,
        OWNER_RETURN_GATE_PATH,
        SCORING_REFUSAL_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
        Path("scripts/Y5_R10_RAB_Delta_w_source_beta_validator_or_action_measure_owner_return.py"),
    ]
    formalization_touched = any("formalization-workbench" in str((ROOT / output).resolve()) for output in outputs)
    scope_ok = all((ROOT / output).resolve().is_relative_to(ROOT.resolve()) for output in outputs) and not formalization_touched
    overall = (
        source_pass
        and input_integrity
        and validator_verdict
        and all_validator_nonclaim
        and owner_blocked
        and refusals_blocked
        and local_claim_blocked
        and scope_ok
    )
    return [
        {
            "validation_id": "VAL1388_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if source_pass else "FAIL",
            "details": "; ".join(
                f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources
            ),
        },
        {
            "validation_id": "VAL1388_1_first_fill_input_integrity",
            "check": "all 1387 Delta_w/source-beta first-fill rows are present",
            "status": "PASS" if input_integrity else "FAIL",
            "details": f"required={len(required_fill_ids)} found={len(required_fill_ids.intersection(first_fill_ids))}",
        },
        {
            "validation_id": "VAL1388_2_validator_refuses_numeric_scoring",
            "check": "strict validator exists and refuses numeric/claim scoring",
            "status": "PASS" if validator_verdict and all_validator_nonclaim else "FAIL",
            "details": "DWV1388_7 records schema readiness while pass_for_numeric=False and pass_for_claim=False.",
        },
        {
            "validation_id": "VAL1388_3_owner_return_unsigned",
            "check": "action-measure/object-language owner return remains unsigned",
            "status": "PASS" if owner_blocked else "FAIL",
            "details": "AMR1388_4 keeps the owner-return theorem blocked until parent clauses close together.",
        },
        {
            "validation_id": "VAL1388_4_arena_refusal",
            "check": "Newton/WEP/R10/PPN/clock/orbital/local-GR scoring remains blocked",
            "status": "PASS" if refusals_blocked and local_claim_blocked else "FAIL",
            "details": "All SFM1388 rows are BLOCKED_NO_SCORE and GATE1388_5 blocks local-GR promotion.",
        },
        {
            "validation_id": "VAL1388_5_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if scope_ok else "FAIL",
            "details": f"ROOT={ROOT}; output_count={len(outputs)}; formalization_touched={formalization_touched}",
        },
        {
            "validation_id": "VAL1388_6_overall",
            "check": "overall 1388 validation",
            "status": "PASS" if overall else "FAIL",
            "details": "1388 builds the Delta_w/source-beta validator, blocks scoring, and preserves the owner-return route without claiming local GR.",
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    validator: list[dict[str, str]],
    owner_gate: list[dict[str, str]],
    refusals: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    generated = datetime.now(timezone.utc).isoformat()
    body = f"""# 1388 - Y5 R10 RAB Delta-w Source-Beta Validator Or Action-Measure Owner Return

**Generated:** {generated}

**Current verdict:** the `Delta_w`/source-beta route is now executable as a validator, not as evidence. The 1387 action-weight counterexample still survives, and the parent object-language/action-measure owner theorem is still unsigned.

**Discipline move:** do not score `Delta_w_A`, `beta_w,S`, `beta_w,T`, `alpha_w(lambda)`, PPN, WEP, Newton, clocks, orbital systems, or local GR until the coupling inputs are theorem-zero or source-backed. Common `w_*` is calibration only when it is universal and derivative/source/range/frame silent.

**Claim ceiling:** {CLAIM_CEILING}

## Source Register

{md_table(sources)}

## `Delta_w` / Source-Beta Validator

{md_table(validator)}

## Action-Measure Owner Return Gate

{md_table(owner_gate)}

## Scoring Refusal Matrix

{md_table(refusals)}

## Claim Gates

{md_table(gates)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    validator = validator_rows()
    owner_gate = owner_return_gate_rows()
    refusals = scoring_refusal_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, validator, owner_gate, refusals, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(VALIDATOR_PATH, validator)
    write_csv(OWNER_RETURN_GATE_PATH, owner_gate)
    write_csv(SCORING_REFUSAL_PATH, refusals)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, validator, owner_gate, refusals, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1388 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
