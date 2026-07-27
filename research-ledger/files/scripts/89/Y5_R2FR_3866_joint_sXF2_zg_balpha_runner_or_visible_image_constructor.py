from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3866"
BRANCH = "MTS_R2FR_Y5_JOINT_SXF2_ZG_BALPHA_RUNNER_OR_VISIBLE_IMAGE_CONSTRUCTOR_3866"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3866-Y5-R2FR-joint-sXF2-zg-balpha-runner-or-visible-image-constructor.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3865_THEOREM = OUT / "P8_Y5_R2FR_3865_VISIBLE_OPERATOR_IMAGE_THEOREM.csv"
CSV_3865_JOINT = OUT / "P8_Y5_R2FR_3865_SXF2_ZG_BALPHA_JOINT_BOUND.csv"
CSV_3865_GATES = OUT / "P8_Y5_R2FR_3865_CLAIM_GATES.csv"
CSV_3865_VALIDATION = OUT / "P8_Y5_BRR545_3865_VALIDATION.csv"
CSV_3864_BOUND = OUT / "P8_Y5_R2FR_3864_LAMBDAF2_BOUND.csv"
CSV_3679_MAP = OUT / "P8_Y5_R2FR_3679_SXF2_CANONICAL_MAP_ROWS.csv"
CSV_3679_BOUND = OUT / "P8_Y5_R2FR_3679_SXF2_BOUND_INPUT_ROWS.csv"
CSV_3680_ZG = OUT / "P8_Y5_R2FR_3680_ZG_COMPONENT_DECOMPOSITION_ROWS.csv"
CSV_3680_ZERO = OUT / "P8_Y5_R2FR_3680_ZG_ZERO_THEOREM_AUDIT.csv"
CSV_3508_ZG = OUT / "P8_Y5_R2FR_3508_ZG_BETA_SOURCE_REDUCTION.csv"
CSV_3118_BALPHA = OUT / "P8_Y5_R2FR_3118_BALPHA_PRODUCT_INPUTS_TEMPLATE.csv"
CSV_1052_CLOCK = OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"
CSV_1052_WEP = OUT / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv"
CSV_1052_R10 = OUT / "P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv"
CSV_2766_IMAGE = OUT / "P8_Y5_R2FR_2766_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv"
CSV_2659_HOM = OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv"
CSV_3118_HOM = OUT / "P8_Y5_R2FR_3118_NO_HIDDEN_VISIBLE_COEFFICIENT_HOM_GATE.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3866_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3866_JOINT_RUNNER_THEOREM.csv",
    "schema": OUT / "P8_Y5_R2FR_3866_JOINT_INPUT_SCHEMA.csv",
    "cases": OUT / "P8_Y5_R2FR_3866_DRYRUN_CASES.csv",
    "results": OUT / "P8_Y5_R2FR_3866_DRYRUN_RESULTS.csv",
    "gates": OUT / "P8_Y5_R2FR_3866_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3866_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3866_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3866_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3866_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3866_00_3865_theorem", CSV_3865_THEOREM, "NEXT_GATE_IS_IMAGE_CONSTRUCTOR_OR_JOINT_RUNNER", "3865 runner handoff"),
    ("SRC3866_01_3865_joint", CSV_3865_JOINT, "JHB3865_5_runner_acceptance", "3865 runner acceptance"),
    ("SRC3866_02_3865_gates", CSV_3865_GATES, "PASS_3866_JOINT_RUNNER_OR_IMAGE_CONSTRUCTOR_TARGET", "3865 next target gate"),
    ("SRC3866_03_3865_validation", CSV_3865_VALIDATION, "PASS", "previous validation"),
    ("SRC3866_04_3864_bound", CSV_3864_BOUND, "LFB3864_0_canonical_identity", "3864 lambdaF2 bound"),
    ("SRC3866_05_3679_identity", CSV_3679_MAP, "MAP3679_3_alpha_identity", "canonical alpha/current/F2 identity"),
    ("SRC3866_06_3679_live", CSV_3679_MAP, "MAP3679_5_zg_live_branch", "two-knob branch"),
    ("SRC3866_07_3679_bound", CSV_3679_BOUND, "SXF23679_2_alpha_clock_route", "s_XF2 alpha clock route"),
    ("SRC3866_08_3680_zg_components", CSV_3680_ZG, "ZGD3680_7_two_knob_identity", "z_g component decomposition"),
    ("SRC3866_09_3680_zg_verdict", CSV_3680_ZERO, "ZG3680_7_verdict", "z_g zero verdict"),
    ("SRC3866_10_3508_zg", CSV_3508_ZG, "CSR3508_0_z_g", "z_g source reduction"),
    ("SRC3866_11_3118_balpha", CSV_3118_BALPHA, "BAP3118_1", "b_alpha product template"),
    ("SRC3866_12_1052_clock", CSV_1052_CLOCK, "ACB1052_2", "alpha clock bound"),
    ("SRC3866_13_1052_wep", CSV_1052_WEP, "AWP1052_0_alpha_Coulomb", "alpha WEP projection"),
    ("SRC3866_14_1052_r10", CSV_1052_R10, "RAP1052_0_product_law", "alpha R10 product"),
    ("SRC3866_15_2766_image", CSV_2766_IMAGE, "VOE2766_6_verdict", "visible image verdict"),
    ("SRC3866_16_2659_hom", CSV_2659_HOM, "ODT2659_1_exact_typed_theorem", "typed no-Hom theorem"),
    ("SRC3866_17_3118_hom", CSV_3118_HOM, "NHV3118_1", "hidden F2 countermodel"),
]

IDENTITY = "b_alpha_X = 2 z_g - s_XF2"
RUNNER_LAW = "|s_XF2 tau_A| <= |b_alpha_X tau_A| + 2|z_g tau_A|"
IMAGE_CONSTRUCTOR = (
    "The derivation route closes only if the parent constructs the visible coefficient image category "
    "A_vis=Image(ParentGenerate) with no independent Coeff(F_Q^2), no hidden-visible Hom, and radiative/readout stability."
)
ACCEPTANCE_RULE = (
    "A claim row is allowed only if the image theorem is parent-signed, or every arena row has numeric same-domain "
    "b_alpha, z_g and s_XF2/projection inputs, source paths, units, and a valid external bound."
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def parse_float_or_none(value: str) -> float | None:
    try:
        if value.startswith("MISSING") or value in {"", "NA", "not_applicable"}:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_joint_runner_or_image_constructor",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "JRI3866_0_identity",
            "claim_piece": "joint alpha/current/F2 identity",
            "statement": IDENTITY,
            "derivation": "canonical EM/current block alpha_eff proportional to g_J^2/lambda_A",
            "result": "EXACT_LINEAR_IDENTITY",
            "status": "DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "JRI3866_1_runner_law",
            "claim_piece": "same-arena no-cancellation bound",
            "statement": RUNNER_LAW,
            "derivation": "multiply the exact identity by tau_A and apply triangle inequality",
            "result": "EXECUTABLE_BOUND_LAW",
            "status": "NONCLAIM_RUNNER_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "JRI3866_2_image_constructor",
            "claim_piece": "visible image constructor route",
            "statement": IMAGE_CONSTRUCTOR,
            "derivation": "imports the 3865 typed image theorem as a construction target rather than an adopted closure",
            "result": "CONSTRUCTOR_ROUTE_DEFINED_NOT_CLOSED",
            "status": "CURRENTLY_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "JRI3866_3_acceptance_rule",
            "claim_piece": "runner acceptance rule",
            "statement": ACCEPTANCE_RULE,
            "derivation": "prevents alpha-only, unity-projection, cross-domain and toy-number shortcuts",
            "result": "STRICT_ACCEPTANCE_RULE",
            "status": "IMPLEMENTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "JRI3866_4_current_verdict",
            "claim_piece": "strict current verdict",
            "statement": "Current inputs are not claim-ready: z_g is neither zeroed nor bounded, MTS-side b_alpha/tau/beta projections are missing, and R10/WEP source maps remain nonclaim.",
            "derivation": "3680 keeps z_g live; 3118/1052 provide templates/source bounds but missing MTS prediction rows",
            "result": "JOINT_RUNNER_BLOCKED_CORRECTLY",
            "status": "CURRENT_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "JRI3866_5_next_handoff",
            "claim_piece": "next target",
            "statement": "Next fill source-backed joint input rows or parent-construct A_vis=Image(ParentGenerate); do not keep re-auditing the same algebra.",
            "derivation": "3866 makes the finite runner contract executable; progress now requires inputs or construction",
            "result": "NEXT_GATE_IS_INPUT_ACQUISITION_OR_IMAGE_CONSTRUCTION",
            "status": "COUPLING_ROUTE_EXECUTABLE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def schema_rows(timestamp: str) -> list[dict[str, object]]:
    base = [
        ("SCHEMA3866_0", "all", "arena", "arena identifier: clock/WEP/R10/source/PPN", "text", "required", "provided by row", "present"),
        ("SCHEMA3866_1", "all", "tau_A", "same-domain projection scale multiplying all three coefficients", "arena_units", "required", "source path or theorem", "missing"),
        ("SCHEMA3866_2", "all", "b_alpha_tau", "arena product b_alpha_X*tau_A or theorem-zero", "arena_units", "required", "source-backed MTS row", "missing_or_source_only"),
        ("SCHEMA3866_3", "all", "z_g_tau", "arena product z_g*tau_A or parent-signed z_g=0", "arena_units", "required", "source-backed MTS row", "missing"),
        ("SCHEMA3866_4", "all", "s_XF2_tau", "optional direct s_XF2*tau_A prediction", "arena_units", "optional", "source-backed MTS row", "missing"),
        ("SCHEMA3866_5", "all", "external_bound", "valid external/source bound for same arena and units", "arena_units", "required for scoring", "source-backed bound row", "partial"),
        ("SCHEMA3866_6", "all", "projection_consistency", "same Xhat normalization/material/profile/readout convention", "boolean", "required", "provenance rows", "missing"),
    ]
    return [
        {
            "input_id": input_id,
            "arena": arena,
            "symbol": symbol,
            "meaning": meaning,
            "units": units,
            "requirement": requirement,
            "source_requirement": source_requirement,
            "current_status": current_status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for input_id, arena, symbol, meaning, units, requirement, source_requirement, current_status in base
    ]


def dryrun_case_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE3866_0_all_missing",
            "arena": "clock",
            "b_alpha_tau": "MISSING_BALPHA_TIMES_TAU_CLOCK",
            "z_g_tau": "MISSING_ZG_TIMES_TAU_CLOCK",
            "external_bound": "2.1e-18",
            "external_bound_units": "yr^-1",
            "input_status": "MISSING_MTS_PRODUCTS",
            "source_path": rel(CSV_3118_BALPHA),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3866_1_alpha_only_clock",
            "arena": "clock",
            "b_alpha_tau": "2.1e-18",
            "z_g_tau": "MISSING_ZG_TIMES_TAU_CLOCK",
            "external_bound": "2.1e-18",
            "external_bound_units": "yr^-1",
            "input_status": "ALPHA_SOURCE_BOUND_ONLY",
            "source_path": rel(CSV_1052_CLOCK),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3866_2_zg_zero_unsigned",
            "arena": "clock",
            "b_alpha_tau": "2.1e-18",
            "z_g_tau": "0",
            "external_bound": "2.1e-18",
            "external_bound_units": "yr^-1",
            "input_status": "ZG_ZERO_ASSUMED_NOT_PARENT_SIGNED",
            "source_path": rel(CSV_3680_ZERO),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3866_3_toy_numeric_nonclaim",
            "arena": "clock",
            "b_alpha_tau": "2.0e-18",
            "z_g_tau": "1.0e-18",
            "external_bound": "5.0e-18",
            "external_bound_units": "yr^-1",
            "input_status": "TOY_NUMERIC_NO_SOURCE",
            "source_path": "toy_nonclaim_internal_arithmetic",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3866_4_R10_template",
            "arena": "R10",
            "b_alpha_tau": "MISSING_KX_BETA_SOURCE_BETA_TEST_TAIL",
            "z_g_tau": "MISSING_ZG_R10_PROJECTION",
            "external_bound": "MISSING_VALID_ALPHA_BOUND_CURVE",
            "external_bound_units": "dimensionless",
            "input_status": "R10_PROJECTION_INPUTS_MISSING",
            "source_path": rel(CSV_1052_R10),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def evaluate_case(case: dict[str, object], timestamp: str) -> dict[str, object]:
    b_alpha = parse_float_or_none(str(case["b_alpha_tau"]))
    z_g = parse_float_or_none(str(case["z_g_tau"]))
    external_bound = parse_float_or_none(str(case["external_bound"]))
    if b_alpha is None or z_g is None:
        s_bound = "MISSING"
        passes_bound = False
        verdict = "BLOCKED_MISSING_JOINT_INPUTS"
    else:
        s_bound_value = abs(b_alpha) + 2 * abs(z_g)
        s_bound = f"{s_bound_value:.12e}"
        passes_bound = external_bound is not None and s_bound_value <= external_bound
        verdict = "TOY_PASS_NONCLAIM" if passes_bound else "TOY_FAIL_OR_NO_BOUND_NONCLAIM"
    if "ALPHA_SOURCE_BOUND_ONLY" in str(case["input_status"]):
        verdict = "BLOCKED_ALPHA_ONLY_NO_ZG"
    if "ZG_ZERO_ASSUMED_NOT_PARENT_SIGNED" in str(case["input_status"]):
        verdict = "BLOCKED_ZG_ZERO_UNSIGNED"
    if "R10_PROJECTION_INPUTS_MISSING" in str(case["input_status"]):
        verdict = "BLOCKED_R10_PROJECTION_INPUTS_MISSING"
    return {
        "result_id": f"RES_{case['case_id']}",
        "case_id": case["case_id"],
        "arena": case["arena"],
        "computed_abs_s_XF2_tau_bound": s_bound,
        "external_bound": case["external_bound"],
        "passes_bound": passes_bound,
        "runner_verdict": verdict,
        "claim_allowed": False,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }


def dryrun_result_rows(cases: list[dict[str, object]], timestamp: str) -> list[dict[str, object]]:
    return [evaluate_case(case, timestamp) for case in cases]


def gate_rows(results: list[dict[str, object]], timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G3866_0_identity",
            "gate": "joint identity and runner law are explicit",
            "status": "PASS_EXACT_IDENTITY_AND_RUNNER_LAW",
            "claim_allowed": False,
            "reason": "b_alpha_X=2z_g-s_XF2 and |s tau| bound are implemented",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3866_1_alpha_only",
            "gate": "alpha-only shortcuts are refused",
            "status": "PASS_ALPHA_ONLY_BLOCKED",
            "claim_allowed": False,
            "reason": "alpha clock source bound without z_g projection is blocked",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3866_2_zg_unsigned",
            "gate": "unsigned z_g=0 is refused",
            "status": "PASS_ZG_ZERO_UNSIGNED_BLOCKED",
            "claim_allowed": False,
            "reason": "z_g=0 must be parent-signed before direct s_XF2 bound is claimable",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3866_3_results_nonclaim",
            "gate": "all dryrun results remain nonclaim",
            "status": "PASS_DRYRUN_NONCLAIM",
            "claim_allowed": False,
            "reason": f"{len(results)} dryrun rows generated with claim_allowed=false",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3866_4_next",
            "gate": "next target selected",
            "status": "PASS_3867_SOURCE_INPUT_ACQUISITION_OR_IMAGE_CONSTRUCTOR_TARGET",
            "claim_allowed": False,
            "reason": "the runner exists; progress now needs source-backed inputs or parent image construction",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D3866_0",
            "decision": "Build the runner before claiming any finite bound.",
            "consequence": "The branch now has executable nonclaim failure modes instead of prose-only warnings.",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3866_1",
            "decision": "Reject alpha-only and unsigned z_g=0 routes.",
            "consequence": "The coupling throat cannot be bypassed by clock alpha data alone.",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3866_2",
            "decision": "Next step must supply inputs or construct the parent image category.",
            "consequence": "Further progress should be either source acquisition/projection or actual parent-category construction.",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3866_0",
            "target_checkpoint": "3867-Y5-R2FR-source-backed-joint-alpha-current-F2-input-acquisition-or-image-constructor.md",
            "script": "scripts/Y5_R2FR_3867_source_backed_joint_alpha_current_F2_input_acquisition_or_image_constructor.py",
            "objective": "fill same-domain source-backed b_alpha, z_g and s_XF2 projection inputs for clock/WEP/R10/source arenas, or parent-construct the visible coefficient image category",
            "why_next": "3866 makes the runner executable but blocked by missing inputs; this is now an input/construction problem rather than algebra fog",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_JOINT_RUNNER_EXECUTABLE_BLOCKED_CORRECTLY",
            "summary": "3866 implements the joint s_XF2/z_g/b_alpha runner law, dry-runs strict nonclaim cases, blocks alpha-only and unsigned z_g routes, and selects source-backed input acquisition or image construction next.",
            "doc": rel(DOC_PATH),
            "validation": rel(OUTPUTS["validation"]),
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    schema: list[dict[str, object]],
    cases: list[dict[str, object]],
    results: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3866 — Joint sXF2 / z_g / b_alpha Runner Or Visible Image Constructor

Generated: `{timestamp}`

## Purpose

3865 gave the exact finite identity and warned that alpha-only bounds cannot isolate `s_XF2`. This checkpoint makes that warning executable.

## Runner Law

`{IDENTITY}`

`{RUNNER_LAW}`

## Parent Constructor Route

`{IMAGE_CONSTRUCTOR}`

## Acceptance Rule

`{ACCEPTANCE_RULE}`

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Runner Theorem

{markdown_table(theorem, ["theorem_id", "claim_piece", "status", "result"])}

## Input Schema

{markdown_table(schema, ["input_id", "arena", "symbol", "requirement", "current_status"])}

## Dryrun Cases

{markdown_table(cases, ["case_id", "arena", "input_status", "b_alpha_tau", "z_g_tau", "external_bound"])}

## Dryrun Results

{markdown_table(results, ["result_id", "arena", "computed_abs_s_XF2_tau_bound", "passes_bound", "runner_verdict", "claim_allowed"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3866 turns the coupling fork into a usable tool: if the parent image theorem closes, the no-extra-F2 route can promote; if it does not, the finite branch must be scored jointly with `s_XF2`, `z_g`, and `b_alpha` in the same arena. Current clock/WEP/R10 rows are correctly blocked because `z_g` and MTS-side projection inputs are missing.

Next target: `3867-Y5-R2FR-source-backed-joint-alpha-current-F2-input-acquisition-or-image-constructor.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3865", "Current State After 3866", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3866 at ")
    )
    paragraph = (
        "`3866` makes the finite no-extra-F2 branch executable. "
        "The runner law is `b_alpha_X=2 z_g-s_XF2` and `|s_XF2 tau_A| <= |b_alpha_X tau_A|+2|z_g tau_A|` in each arena. "
        "It also preserves the parent-constructor route: the derivation closes only if `A_vis=Image(ParentGenerate)` is parent-constructed with no independent `Coeff(F_Q^2)`, no hidden-visible Hom, and radiative/readout stability. "
        "Dry-run cases now explicitly block all-missing inputs, alpha-only clock input, unsigned `z_g=0`, and R10 projection shortcuts; a toy numeric case is computed but still nonclaim. "
        "The branch has therefore moved from algebra warning to executable gate: current rows are blocked because `z_g`, same-domain `tau`, MTS-side `b_alpha/s_XF2` projections, and valid arena inputs are missing.\n\n"
    )
    if paragraph not in text and "## Next Best Gate" in text:
        text = text.replace("## Next Best Gate", paragraph + "## Next Best Gate", 1)
    old_gate = """`3866-Y5-R2FR-joint-sXF2-zg-balpha-runner-or-visible-image-constructor.md`

Target: either parent-construct the visible coefficient image category, or create a runnable nonclaim joint `s_XF2` / `z_g` / `b_alpha` product runner for clock/WEP/R10/source arenas.

This is the best next move because 3865 has the exact theorem and finite algebra; now the branch needs either a parent construction or executable bound validation."""
    new_gate = """`3867-Y5-R2FR-source-backed-joint-alpha-current-F2-input-acquisition-or-image-constructor.md`

Target: fill same-domain source-backed `b_alpha`, `z_g`, and `s_XF2` projection inputs for clock/WEP/R10/source arenas, or parent-construct the visible coefficient image category.

This is the best next move because 3866 makes the runner executable but correctly blocked by missing inputs; the problem is now input acquisition or parent construction, not algebra fog."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3866_JOINT_RUNNER_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3866_JOINT_INPUT_SCHEMA.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3866_DRYRUN_RESULTS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3866_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3866_JOINT_RUNNER_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3866 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    schema: list[dict[str, object]],
    cases: list[dict[str, object]],
    results: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    all_text = " ".join(str(row) for row in theorem + schema + cases + results + gates)
    add(
        "VAL3866_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3866_1_identity",
        "joint identity and runner law are explicit",
        "b_alpha_X = 2 z_g - s_XF2" in all_text and "|s_XF2 tau_A| <= |b_alpha_X tau_A| + 2|z_g tau_A|" in all_text,
        "identity and runner law present",
    )
    add(
        "VAL3866_2_alpha_only_blocked",
        "alpha-only dryrun is blocked",
        any(row["runner_verdict"] == "BLOCKED_ALPHA_ONLY_NO_ZG" for row in results),
        "alpha-only shortcut refused",
    )
    add(
        "VAL3866_3_zg_unsigned_blocked",
        "unsigned z_g zero dryrun is blocked",
        any(row["runner_verdict"] == "BLOCKED_ZG_ZERO_UNSIGNED" for row in results),
        "unsigned z_g=0 refused",
    )
    add(
        "VAL3866_4_r10_blocked",
        "R10 projection dryrun is blocked",
        any(row["runner_verdict"] == "BLOCKED_R10_PROJECTION_INPUTS_MISSING" for row in results),
        "R10 missing projection refused",
    )
    add(
        "VAL3866_5_nonclaim",
        "all rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in theorem + schema + cases + results + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3866_6_next",
        "next target is source-backed input acquisition or image constructor",
        DOC_PATH.exists() and "3867-Y5-R2FR-source-backed-joint-alpha-current-F2-input-acquisition-or-image-constructor" in read_text(DOC_PATH),
        "3867 target visible",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3866_7_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3866_8_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "3865 gave the exact finite identity" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    formalization_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3866*", "P8_Y5_BRR545_3866*", "*Y5_R2FR_3866*", "3866-Y5-R2FR*"):
            formalization_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3866_9_formalization_clean",
        "formalization-workbench has no generated 3866 project files",
        len(formalization_hits) == 0,
        "; ".join(str(path) for path in formalization_hits) if formalization_hits else "no generated 3866 project file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3866_10_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    schema = schema_rows(timestamp)
    cases = dryrun_case_rows(timestamp)
    results = dryrun_result_rows(cases, timestamp)
    gates = gate_rows(results, timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["schema"], schema)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, schema, cases, results, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, schema, cases, results, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_JOINT_RUNNER_EXECUTABLE_BLOCKED_CORRECTLY")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
