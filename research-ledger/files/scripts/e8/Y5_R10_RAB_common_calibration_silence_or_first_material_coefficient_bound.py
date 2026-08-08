from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1390-Y5-R10-RAB-common-calibration-silence-or-first-material-coefficient-bound.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1390_SOURCE_REGISTER.csv"
COMMON_SILENCE_PATH = SRC_DIR / "P8_Y5_R10_1390_COMMON_CALIBRATION_SILENCE_PROOF.csv"
BULK_BOUND_PATH = SRC_DIR / "P8_Y5_R10_1390_BULK_MATERIAL_COEFFICIENT_BOUND_ROWS.csv"
FAILURE_MODE_PATH = SRC_DIR / "P8_Y5_R10_1390_DERIVATIVE_SILENCE_FAILURE_MODES.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1390_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1390_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1390_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1390_VALIDATION.csv"

STATUS = (
    "common_calibration_silence_conditional_theorem_written_"
    "bulk_material_coefficient_bound_rows_ready_nonclaim"
)
CLAIM_CEILING = (
    "conditional_common_wstar_constant_calibration_only_no_parent_signed_silence_"
    "no_bulk_coefficient_value_no_numeric_beta_no_R10_no_WEP_no_PPN_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1390_0_1389_doc",
        "source_path": "1389-Y5-R10-RAB-Delta-w-material-source-map-or-action-measure-owner-proof.md",
        "required_anchor": "NEXT1389_0_1390",
        "purpose": "handoff to common calibration silence or first material coefficient bound",
    },
    {
        "source_id": "SRC1390_1_1389_next",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1389_NEXT_TARGET.csv",
        "required_anchor": "NEXT1389_0_1390",
        "purpose": "machine-readable 1390 target",
    },
    {
        "source_id": "SRC1390_2_1389_owner_proof",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1389_ACTION_MEASURE_OWNER_PROOF_ATTEMPT.csv",
        "required_anchor": "AMP1389_6_theorem_if_signed",
        "purpose": "conditional Delta_w/beta zero theorem",
    },
    {
        "source_id": "SRC1390_3_1389_owner_verdict",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1389_ACTION_MEASURE_OWNER_PROOF_ATTEMPT.csv",
        "required_anchor": "AMP1389_7_current_verdict",
        "purpose": "owner theorem remains unsigned",
    },
    {
        "source_id": "SRC1390_4_1389_material_map",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1389_MATERIAL_SOURCE_CLASS_MAP.csv",
        "required_anchor": "MSC1389_0_bulk_neutral_baryonic",
        "purpose": "bulk neutral baryonic class row to refine",
    },
    {
        "source_id": "SRC1390_5_1389_map_verdict",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1389_MATERIAL_SOURCE_CLASS_MAP.csv",
        "required_anchor": "MSC1389_6_map_verdict",
        "purpose": "material map remains nonclaim",
    },
    {
        "source_id": "SRC1390_6_1389_convention",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1389_COUPLING_EXPANSION_CONVENTION.csv",
        "required_anchor": "CEC1389_5_verdict",
        "purpose": "coupling expansion convention scaffold",
    },
    {
        "source_id": "SRC1390_7_1389_arena",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1389_ARENA_REQUIREMENT_MATRIX.csv",
        "required_anchor": "ARM1389_6_local_GR",
        "purpose": "local GR gate remains blocked",
    },
    {
        "source_id": "SRC1390_8_1229_single_GN",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv",
        "required_anchor": "CLC1229_7_single_GN_normalization",
        "purpose": "measured-G absorption cannot hide residual source weights",
    },
    {
        "source_id": "SRC1390_9_1036_beta_product",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv",
        "required_anchor": "BETA1036_2_R10_alpha_match",
        "purpose": "source-test product law for finite exchange",
    },
    {
        "source_id": "SRC1390_10_this_script",
        "source_path": "scripts/Y5_R10_RAB_common_calibration_silence_or_first_material_coefficient_bound.py",
        "required_anchor": "STATUS",
        "purpose": "1390 generator",
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


def common_silence_rows() -> list[dict[str, str]]:
    return [
        {
            "silence_id": "CCS1390_0_definition",
            "target": "common action factor w_*",
            "attempted_derivation": "write S_matter = w_* S_matter,0 with the same w_* for all ordinary matter classes",
            "result": "TARGET_DEFINED",
            "required_for_silence": "w_* must be a parent global constant, not a field, source label, range kernel, frame selector, or readout variable",
            "if_missing": "w_* cannot be absorbed into a single measured G_N",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "silence_id": "CCS1390_1_metric_variation",
            "target": "metric/source normalization",
            "attempted_derivation": "if w_* is a true constant, Hilbert stress scales as T_eff=w_* T_0 and can be absorbed by kappa_eff or measured G_N",
            "result": "EXACT_IF_TRUE_CONSTANT",
            "required_for_silence": "partial_mu w_*=0 and no source/material dependence",
            "if_missing": "source normalization becomes environment/composition dependent",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "silence_id": "CCS1390_2_diffeomorphism_conservation",
            "target": "Bianchi/conservation compatibility",
            "attempted_derivation": "explicit x or frame dependence in w_* is not a pure normalization and produces a non-silent source in the matter conservation identity",
            "result": "DERIVATIVE_SILENCE_REQUIRED",
            "required_for_silence": "nabla_mu w_*=0 in the local branch or a parent identity that moves the term into a closed sector",
            "if_missing": "Bianchi/current conservation gate remains open",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "silence_id": "CCS1390_3_scalar_variation",
            "target": "scalar/fifth-force source",
            "attempted_derivation": "if w_*=w_*(phi_c), then beta_* := partial_phi_c ln w_* sources a universal finite exchange even when Delta_w_A=0",
            "result": "BETA_STAR_MUST_BE_ZERO_OR_BOUNDED",
            "required_for_silence": "partial_phi_c ln w_*=0 or a sourced beta_* bound",
            "if_missing": "R10/PPN/Newton finite-force scoring is blocked",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "silence_id": "CCS1390_4_range_frame_readout",
            "target": "range/frame/readout dependence",
            "attempted_derivation": "if w_* depends on lambda, frame choice, source radius, or readout convention, it is not one calibration constant",
            "result": "RANGE_FRAME_SILENCE_REQUIRED",
            "required_for_silence": "partial_lambda w_*=0 and frame/readout invariance of the calibration map",
            "if_missing": "inverse-square, local frame, and clock/orbital gates remain blocked",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "silence_id": "CCS1390_5_constant_theorem",
            "target": "common calibration theorem",
            "attempted_derivation": "if parent object language signs w_* as a single global positive constant multiplying all ordinary matter, then all derivative/source/range/frame silence clauses follow",
            "result": "EXACT_CONDITIONAL_CALIBRATION_THEOREM",
            "required_for_silence": "parent global-constant signature for w_* plus single measured-G_N normalization",
            "if_missing": "common calibration remains a conditional lemma, not a claim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "silence_id": "CCS1390_6_current_evidence",
            "target": "current corpus evidence",
            "attempted_derivation": "compare 1389 owner proof, 1389 material map, and 1229 measured-G guard",
            "result": "GLOBAL_CONSTANT_SIGNATURE_NOT_PARENT_SIGNED",
            "required_for_silence": "new parent evidence that w_* is not a field/function/source label",
            "if_missing": "create beta_* and bulk coefficient bound rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "silence_id": "CCS1390_7_verdict",
            "target": "common calibration silence verdict",
            "attempted_derivation": "keep the exact theorem but refuse to use it as local evidence",
            "result": "COMMON_SILENCE_NOT_PARENT_SIGNED",
            "required_for_silence": "close CCS1390_5 as a parent-signed theorem or source beta_*/bulk bounds",
            "if_missing": "no Newton/GR/PPN/R10 promotion from w_* absorption",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def bulk_bound_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BMB1390_0_wstar_common",
            "coefficient": "w_*",
            "definition": "common ordinary-matter action multiplier",
            "units": "dimensionless",
            "maps_to": "measured G_N calibration only if global constant and derivative silent",
            "required_source_or_bound": "parent global-constant signature or external bound on nonconstant pieces",
            "current_value": "MISSING",
            "current_status": "CONDITIONAL_CALIBRATION_ONLY",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "bound_id": "BMB1390_1_beta_star_common",
            "coefficient": "beta_* := partial_phi_c ln w_*",
            "definition": "universal derivative of the common action factor",
            "units": "canonical inverse-field or locked dimensionless beta convention",
            "maps_to": "universal finite scalar exchange even with Delta_w_A=0",
            "required_source_or_bound": "parent theorem beta_*=0 or sourced R10/PPN/Newton bound",
            "current_value": "MISSING",
            "current_status": "MISSING_BETA_STAR_ZERO_OR_BOUND",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "bound_id": "BMB1390_2_Delta_w_bulk",
            "coefficient": "Delta_w_bulk",
            "definition": "relative bulk neutral baryonic source/action multiplier after common calibration",
            "units": "dimensionless",
            "maps_to": "Newton source normalization and WEP/source-charge residuals",
            "required_source_or_bound": "parent theorem Delta_w_bulk=0 or material/source bound for neutral bulk matter",
            "current_value": "MISSING",
            "current_status": "MISSING_BULK_DELTA_VALUE_OR_BOUND",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "bound_id": "BMB1390_3_beta_w_bulk",
            "coefficient": "beta_w,bulk",
            "definition": "canonical phi derivative of the bulk neutral baryonic action weight",
            "units": "canonical inverse-field or locked dimensionless beta convention",
            "maps_to": "R10/PPN/orbital finite source leg",
            "required_source_or_bound": "parent theorem beta_w,bulk=0 or sourced bound by bulk material class",
            "current_value": "MISSING",
            "current_status": "MISSING_BULK_BETA_VALUE_OR_BOUND",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "bound_id": "BMB1390_4_bulk_R10_product",
            "coefficient": "alpha_bulk,ST(lambda)",
            "definition": "short-range bulk source-test exchange strength",
            "units": "dimensionless alpha(lambda)",
            "maps_to": "R10 comparator row once beta source/test, K_ST(lambda), tail, and real bound curve exist",
            "required_source_or_bound": "beta_w,bulk,S; beta_w,bulk,T; K_ST(lambda); epsilon_tail; R10 material pair; bound curve",
            "current_value": "MISSING",
            "current_status": "MISSING_R10_PRODUCT_INPUTS",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "bound_id": "BMB1390_5_bulk_local_residual_vector",
            "coefficient": "R_bulk_local",
            "definition": "bulk neutral contribution to Newton/WEP/PPN/clock/orbital residual vector",
            "units": "arena-specific residual units",
            "maps_to": "local-GR branch only after every local arena gate closes",
            "required_source_or_bound": "Newton kernel; WEP kernel; PPN vector; clock/orbital kernels; all coefficient bounds",
            "current_value": "MISSING",
            "current_status": "MISSING_LOCAL_RESIDUAL_VECTOR",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "bound_id": "BMB1390_6_bound_verdict",
            "coefficient": "bulk material coefficient pack",
            "definition": "first nonclaim bulk coefficient/bound routing pack",
            "units": "per-row units above",
            "maps_to": "future local tests only after values, bounds, kernels, and provenance are real",
            "required_source_or_bound": "BMB1390_0 through BMB1390_5 all theorem-zero or source-backed",
            "current_value": "MISSING",
            "current_status": "BULK_BOUND_ROWS_READY_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def failure_mode_rows() -> list[dict[str, str]]:
    return [
        {
            "failure_id": "DSF1390_0_time_space_dependence",
            "failure_mode": "w_* varies over spacetime",
            "why_not_calibration": "a single measured G_N cannot absorb time/spatial dependence",
            "blocked_arenas": "Newton;PPN;clocks;orbital;local GR",
            "required_fix": "prove nabla_mu w_*=0 or bound the variation",
            "status": "BLOCKED_IF_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "failure_id": "DSF1390_1_scalar_dependence",
            "failure_mode": "w_* depends on phi_c",
            "why_not_calibration": "beta_* sources universal finite exchange",
            "blocked_arenas": "R10;PPN;Newton;local GR",
            "required_fix": "prove beta_*=0 or source beta_* bound",
            "status": "BLOCKED_IF_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "failure_id": "DSF1390_2_source_environment_dependence",
            "failure_mode": "w_* changes by source, material, environment, or branch",
            "why_not_calibration": "relative source normalization reappears as Delta_w_A",
            "blocked_arenas": "WEP;Newton;PPN;local GR",
            "required_fix": "prove universality or fill material/source coefficient rows",
            "status": "BLOCKED_IF_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "failure_id": "DSF1390_3_range_dependence",
            "failure_mode": "w_* depends on lambda or source/test separation",
            "why_not_calibration": "range dependence is an inverse-square/fifth-force signal, not G_N calibration",
            "blocked_arenas": "R10;Newton;orbital;local GR",
            "required_fix": "prove partial_lambda w_*=0 or bind it to the finite exchange kernel",
            "status": "BLOCKED_IF_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "failure_id": "DSF1390_4_frame_readout_dependence",
            "failure_mode": "w_* depends on frame, gauge, or readout convention",
            "why_not_calibration": "a physical prediction cannot depend on a representative selector",
            "blocked_arenas": "PPN;clocks;orbital;local GR",
            "required_fix": "prove frame/readout invariance or keep a residual vector",
            "status": "BLOCKED_IF_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "failure_id": "DSF1390_5_failure_verdict",
            "failure_mode": "any derivative silence clause remains open",
            "why_not_calibration": "common factor absorption is valid only for a true global constant",
            "blocked_arenas": "Newton;WEP;R10;PPN;clocks;orbital;local GR",
            "required_fix": "close all silence clauses or treat coefficients as finite nonclaim inputs",
            "status": "SILENCE_FAILURES_ROUTED_NONCLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE1390_0_sources",
            "gate": "all cited local sources exist and anchors are present",
            "status": "PASS",
            "reason": "source register validates against local corpus",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1390_1_common_constant",
            "gate": "w_* is parent-signed as a global constant",
            "status": "BLOCKED_PARENT_UNSIGNED",
            "reason": "1390 proves the conditional theorem but current corpus does not sign the global-constant premise",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1390_2_derivative_silence",
            "gate": "time/source/range/frame/scalar derivatives of w_* vanish",
            "status": "BLOCKED_NOT_SIGNED",
            "reason": "derivative silence is required but not parent-proven",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1390_3_bulk_bound_rows",
            "gate": "bulk material coefficient rows exist",
            "status": "PASS_NONCLAIM_ROWS",
            "reason": "w_*, beta_*, Delta_w_bulk, beta_w,bulk, alpha_bulk, and local residual rows are staged without values",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1390_4_numeric_score",
            "gate": "bulk coefficients can score Newton/WEP/R10/PPN/local residuals",
            "status": "BLOCKED_VALUES_AND_KERNELS_MISSING",
            "reason": "no coefficient values, real bounds, material kernels, or local residual vector exist yet",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1390_5_local_claim",
            "gate": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1390 is a common-calibration theorem attempt plus nonclaim coefficient routing pack",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1390_0_exact_if_constant",
            "decision": "true global common w_* is harmless calibration",
            "because": "if w_* is parent-signed as one constant, it only rescales the matter source and can be absorbed into measured G_N",
            "next_action": "seek the parent global-constant signature or keep beta_* row active",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1390_1_not_if_derivative",
            "decision": "nonconstant w_* is physics, not normalization",
            "because": "scalar, spacetime, range, frame, or source dependence creates conservation, fifth-force, or residual-vector obligations",
            "next_action": "route every non-silent piece into explicit coefficient rows",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1390_2_bulk_first",
            "decision": "use bulk neutral matter as the first finite coefficient channel",
            "because": "bulk neutral matter is shared by Newton, WEP, R10, PPN, orbital, and local-GR gates",
            "next_action": "1391 should build the first source-backed bulk coefficient/kernel pack or prove bulk theorem-zero",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1390_0_1391",
            "next_doc": "1391-Y5-R10-RAB-bulk-neutral-coefficient-source-pack-and-R10-kernel-gate.md",
            "next_script": "scripts/Y5_R10_RAB_bulk_neutral_coefficient_source_pack_and_R10_kernel_gate.py",
            "task": "build the first source-backed/nonclaim bulk neutral coefficient pack and R10 material-kernel gate, or prove beta_w,bulk and Delta_w_bulk theorem-zero from ordinary-matter universality",
            "success_condition": "bulk neutral rows have explicit source/test roles, units, required bounds, material kernels, and refusal gates; no scoring unless all numeric/provenance fields are real",
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
    silence: list[dict[str, str]],
    bulk_bounds: list[dict[str, str]],
    failures: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_pass = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    conditional_theorem = any(
        row["silence_id"] == "CCS1390_5_constant_theorem"
        and row["result"] == "EXACT_CONDITIONAL_CALIBRATION_THEOREM"
        and row["valid_for_claim"] == "False"
        for row in silence
    )
    silence_blocked = any(
        row["silence_id"] == "CCS1390_7_verdict"
        and row["result"] == "COMMON_SILENCE_NOT_PARENT_SIGNED"
        and row["claim_allowed"] == "False"
        for row in silence
    )
    bulk_ready = any(
        row["bound_id"] == "BMB1390_6_bound_verdict"
        and row["current_status"] == "BULK_BOUND_ROWS_READY_NONCLAIM"
        and row["valid_for_claim"] == "False"
        for row in bulk_bounds
    )
    no_values = all(row["current_value"] == "MISSING" for row in bulk_bounds)
    failure_routing = any(
        row["failure_id"] == "DSF1390_5_failure_verdict"
        and row["status"] == "SILENCE_FAILURES_ROUTED_NONCLAIM"
        and row["claim_allowed"] == "False"
        for row in failures
    )
    local_claim_blocked = any(
        row["gate_id"] == "GATE1390_5_local_claim"
        and row["status"] == "BLOCKED_NO_CLAIM"
        and row["claim_allowed"] == "False"
        for row in gates
    )
    prior_gate = csv_rows(Path("source-intake/mts_residuals/P8_Y5_R10_1389_CLAIM_GATE.csv"))
    prior_local_blocked = any(
        row["gate_id"] == "GATE1389_5_local_claim" and row["status"] == "BLOCKED_NO_CLAIM"
        for row in prior_gate
    )
    outputs = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        COMMON_SILENCE_PATH,
        BULK_BOUND_PATH,
        FAILURE_MODE_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
        Path("scripts/Y5_R10_RAB_common_calibration_silence_or_first_material_coefficient_bound.py"),
    ]
    formalization_touched = any("formalization-workbench" in str((ROOT / output).resolve()) for output in outputs)
    scope_ok = all((ROOT / output).resolve().is_relative_to(ROOT.resolve()) for output in outputs) and not formalization_touched
    overall = (
        source_pass
        and conditional_theorem
        and silence_blocked
        and bulk_ready
        and no_values
        and failure_routing
        and local_claim_blocked
        and prior_local_blocked
        and scope_ok
    )
    return [
        {
            "validation_id": "VAL1390_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if source_pass else "FAIL",
            "details": "; ".join(
                f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources
            ),
        },
        {
            "validation_id": "VAL1390_1_common_silence_theorem",
            "check": "common calibration theorem is exact only if w_* is a parent global constant",
            "status": "PASS" if conditional_theorem and silence_blocked else "FAIL",
            "details": "CCS1390_5 gives the exact conditional theorem; CCS1390_7 keeps it unsigned.",
        },
        {
            "validation_id": "VAL1390_2_bulk_bound_rows",
            "check": "bulk material coefficient rows are staged without values or claims",
            "status": "PASS" if bulk_ready and no_values else "FAIL",
            "details": f"bulk_rows={len(bulk_bounds)}; all_current_value_missing={no_values}",
        },
        {
            "validation_id": "VAL1390_3_failure_modes",
            "check": "non-silent w_* failure modes are routed to explicit rows",
            "status": "PASS" if failure_routing else "FAIL",
            "details": "DSF1390_5 records that any open derivative-silence clause blocks calibration claims.",
        },
        {
            "validation_id": "VAL1390_4_claim_refusal",
            "check": "local and arena claims remain blocked",
            "status": "PASS" if local_claim_blocked and prior_local_blocked else "FAIL",
            "details": "GATE1390_5 and prior GATE1389_5 both block local GR/Newton promotion.",
        },
        {
            "validation_id": "VAL1390_5_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if scope_ok else "FAIL",
            "details": f"ROOT={ROOT}; output_count={len(outputs)}; formalization_touched={formalization_touched}",
        },
        {
            "validation_id": "VAL1390_6_overall",
            "check": "overall 1390 validation",
            "status": "PASS" if overall else "FAIL",
            "details": "1390 proves common w_* calibration only conditionally and stages first bulk coefficient rows without scoring.",
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    silence: list[dict[str, str]],
    bulk_bounds: list[dict[str, str]],
    failures: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    generated = datetime.now(timezone.utc).isoformat()
    body = f"""# 1390 - Y5 R10 RAB Common Calibration Silence Or First Material Coefficient Bound

**Generated:** {generated}

**Current verdict:** a common `w_*` is harmless calibration only under the exact conditional theorem that it is a parent global constant. If `w_*` has scalar, spacetime, range, frame, source, or readout dependence, it is not calibration; it is a physical residual that must be bounded or derived zero.

**Discipline move:** split the common-factor problem into `w_*`, `beta_*`, `Delta_w_bulk`, `beta_w,bulk`, `alpha_bulk,ST(lambda)`, and a bulk local residual vector. The rows are ready for future sourcing, but every value is still missing and no arena score is allowed.

**Claim ceiling:** {CLAIM_CEILING}

## Source Register

{md_table(sources)}

## Common Calibration Silence Proof

{md_table(silence)}

## Bulk Material Coefficient Bound Rows

{md_table(bulk_bounds)}

## Derivative Silence Failure Modes

{md_table(failures)}

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
    silence = common_silence_rows()
    bulk_bounds = bulk_bound_rows()
    failures = failure_mode_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, silence, bulk_bounds, failures, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(COMMON_SILENCE_PATH, silence)
    write_csv(BULK_BOUND_PATH, bulk_bounds)
    write_csv(FAILURE_MODE_PATH, failures)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, silence, bulk_bounds, failures, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1390 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
