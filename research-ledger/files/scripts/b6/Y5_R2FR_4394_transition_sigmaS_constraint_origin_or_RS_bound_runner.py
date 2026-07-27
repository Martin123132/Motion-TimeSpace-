from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from sigma_s_RS_bound_runner import evaluate_bound_rows, read_csv, write_csv  # noqa: E402
from sigma_s_constraint_origin_gate import evaluate_origin_rows  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4394"
CLAIM_ID = "L-235"
MARKER = "PPC4161_TRANSITION_SIGMAS_CONSTRAINT_ORIGIN_OR_RS_BOUND_RUNNER_4394"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_SIGMAS_CONSTRAINT_ORIGIN_OR_RS_BOUND_RUNNER_4394"
DECISION = "SIGMAS_ORIGIN_GATE_FAILS_PARENT_UNSIGNED_RS_BOUND_RUNNER_BUILT_NONCLAIM"
NEXT_TARGET = "4395-Y5-R2FR-transition-RS-first-source-row-or-sigma-constraint-parent-origin-proof.md"

FORMAL_PATH = FORMAL / "410-PPC4161-transition-sigmaS-constraint-origin-or-RS-bound-runner.md"
DOC_PATH = POST / "4394-Y5-R2FR-transition-sigmaS-constraint-origin-or-RS-bound-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4394_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
ORIGIN_RUNNER_PATH = SCRIPT_DIR / "sigma_s_constraint_origin_gate.py"
BOUND_RUNNER_PATH = SCRIPT_DIR / "sigma_s_RS_bound_runner.py"
ORIGIN_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4394_SIGMA_CONSTRAINT_ORIGIN_INPUT.csv"
ORIGIN_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4394_SIGMA_CONSTRAINT_ORIGIN_OUTPUT.csv"
BOUND_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4394_RS_BOUND_INPUT.csv"
BOUND_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4394_RS_BOUND_OUTPUT.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4394_0_4393_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4393_NEXT_TARGET.csv",
        "4394-Y5-R2FR-transition-sigmaS-constraint-origin-or-RS-bound-runner.md",
        "Explicit 4394 handoff.",
    ),
    "SRC4394_1_4393_action": (
        SOURCE_DIR / "P8_Y5_R2FR_4393_SIGMA_S_ACTION_THEOREMS.csv",
        "SACT4393_0_parent_constraint_signature",
        "Sigma/lambda constraint action template.",
    ),
    "SRC4394_2_4393_multiplier": (
        SOURCE_DIR / "P8_Y5_R2FR_4393_SIGMA_S_ACTION_THEOREMS.csv",
        "SACT4393_2_multiplier_null_lemma",
        "Multiplier-null lemma.",
    ),
    "SRC4394_3_4393_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4393_FIRST_BOUND_ROWS.csv",
        "RS4393_0_first_residual_bound",
        "First R_S residual bound schema.",
    ),
    "SRC4394_4_nonprop": (
        POST / "07-nonpropagating-reciprocity-constraint.md",
        "constraint parent origin",
        "Existing nonpropagating constraint route says parent origin is open.",
    ),
    "SRC4394_5_observer": (
        POST / "10-observer-map-symplectic-contract.md",
        "a genuine constraint whose multiplier has a parent origin",
        "Parent-origin constraint contract.",
    ),
    "SRC4394_6_origin_runner": (
        ORIGIN_RUNNER_PATH,
        "def evaluate_origin_rows",
        "Executable sigma constraint origin gate.",
    ),
    "SRC4394_7_bound_runner": (
        BOUND_RUNNER_PATH,
        "def evaluate_bound_rows",
        "Executable R_S/multiplier-stress bound runner.",
    ),
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    write_text(path, text + block)


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow(row)


def source_register_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(text and needle in text)),
                "valid_for_claim": "False",
            }
        )
    return rows


def origin_theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "ORG4394_0_constraint_family",
            "statement": "The sigma/lambda constraint belongs to the same mathematical family as the nonpropagating reciprocity constraint: a multiplier imposes a structural local relation while avoiding an exterior hair field.",
            "derivation": "Compare lambda_R R_AB with lambda_S(Delta_h sigma_S-delta rho_topH). Both are nonpropagating multipliers; both are useful only if the multiplier sector has parent origin rather than being inserted to force a wanted readout.",
            "effect": "Gives a real origin search target, not a proof.",
            "status": "CONSTRAINT_FAMILY_IDENTIFIED_PARENT_ORIGIN_OPEN",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "ORG4394_1_origin_triage",
            "statement": "There are three acceptable parent-origin routes: object-language axiom, first-class/gauge constraint with degree-count proof, or conserved cell/source current whose no-charge theorem forces the constraint.",
            "derivation": "This is the observer-map contract specialized to sigma_S. Generic phase-volume words, a late equality multiplier, or fitting local tests are excluded.",
            "effect": "The next derivation target is finite and testable.",
            "status": "ORIGIN_ROUTE_TRIAD_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "ORG4394_2_current_corpus_verdict",
            "statement": "Current local sources identify the nonpropagating-constraint pattern but do not parent-sign sigma/lambda as an allowed object-language sector.",
            "derivation": "07 records the same parent-origin gap for lambda_R; 10 says a genuine constraint must have parent origin. 4393 supplies a template but not that origin.",
            "effect": "Origin gate must fail closed for now.",
            "status": "PARENT_ORIGIN_UNSIGNED_NONCLAIM",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "ORG4394_3_RS_bound_transfer",
            "statement": "If the origin proof remains open, the first physical bound is |delta a_RS|/|a_N| <= K_N(s)||R_S||_weighted/M_H plus absolute multiplier and kernel stress scores.",
            "derivation": "R_S is the residual density mismatch left by the failed sigma owner identity. It enters the same compact-source Newton Green transfer as earlier profile/source residuals; stress terms must be added, not cancelled.",
            "effect": "Creates a strict fallback runner for real rows.",
            "status": "BOUND_RUNNER_LAW_DERIVED",
            "valid_for_claim": "False",
        },
    ]


def origin_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "candidate_id": "ORIG4394_0_nonpropagating_family",
            "origin_route": "analogy_to_lambda_R_nonpropagating_constraint",
            "nonpropagating_constraint_family_identified": "True",
            "parent_object_language_signed": "False",
            "origin_principle_derived": "False",
            "residual_density_parent_owned": "False",
            "sigma_lambda_added_before_readout": "False",
            "constraint_rank_or_gauge_count_checked": "False",
            "boundary_zero_mode_owner_signed": "False",
            "same_tau_coframe_signed": "False",
            "no_GR_import_or_fit": "True",
            "no_late_multiplier": "True",
            "source_path": str(POST / "07-nonpropagating-reciprocity-constraint.md"),
        },
        {
            "candidate_id": "ORIG4394_1_object_language_axiom_candidate",
            "origin_route": "parent_object_language_constraint_sector",
            "nonpropagating_constraint_family_identified": "True",
            "parent_object_language_signed": "False",
            "origin_principle_derived": "False",
            "residual_density_parent_owned": "False",
            "sigma_lambda_added_before_readout": "False",
            "constraint_rank_or_gauge_count_checked": "False",
            "boundary_zero_mode_owner_signed": "False",
            "same_tau_coframe_signed": "False",
            "no_GR_import_or_fit": "True",
            "no_late_multiplier": "True",
            "source_path": str(Path(__file__).resolve()),
        },
        {
            "candidate_id": "ORIG4394_2_first_class_constraint_route",
            "origin_route": "first_class_constraint_degree_count",
            "nonpropagating_constraint_family_identified": "True",
            "parent_object_language_signed": "False",
            "origin_principle_derived": "False",
            "residual_density_parent_owned": "False",
            "sigma_lambda_added_before_readout": "False",
            "constraint_rank_or_gauge_count_checked": "False",
            "boundary_zero_mode_owner_signed": "False",
            "same_tau_coframe_signed": "False",
            "no_GR_import_or_fit": "True",
            "no_late_multiplier": "True",
            "source_path": str(Path(__file__).resolve()),
        },
    ]


def bound_input_rows() -> List[Dict[str, str]]:
    script_path = str(Path(__file__).resolve())
    return [
        {
            "candidate_id": "RS4394_0_missing_first_real_row",
            "target": "R_S_residual_mismatch",
            "theorem_zero": "False",
            "theorem_zero_authority": "MISSING_PARENT_SIGNED_RS_ZERO",
            "R_S_weighted_norm": "MISSING_R_S_WEIGHTED_NORM",
            "M_H": "MISSING_M_H",
            "K_N": "MISSING_K_N",
            "lambda_stress_score": "MISSING_LAMBDA_STRESS_SCORE",
            "kernel_stress_score": "MISSING_KERNEL_STRESS_SCORE",
            "delta_threshold": "MISSING_DELTA_THRESHOLD",
            "source_path": "MISSING_FIRST_RS_SOURCE_PATH",
            "equation_ref": "MISSING_EQUATION_REF",
            "no_cancellation_guard": "False",
            "input_valid_for_claim": "False",
        },
        {
            "candidate_id": "RS4394_1_numeric_smoke_nonclaim",
            "target": "runner_arithmetic_smoke",
            "theorem_zero": "False",
            "theorem_zero_authority": "NONE",
            "R_S_weighted_norm": "1e-9",
            "M_H": "1.0",
            "K_N": "2e-2",
            "lambda_stress_score": "0.0",
            "kernel_stress_score": "0.0",
            "delta_threshold": "1e-6",
            "source_path": script_path,
            "equation_ref": "synthetic_arithmetic_smoke_not_evidence",
            "no_cancellation_guard": "True",
            "input_valid_for_claim": "False",
        },
        {
            "candidate_id": "RS4394_2_multiplier_stress_smoke_nonclaim",
            "target": "multiplier_payload_smoke",
            "theorem_zero": "False",
            "theorem_zero_authority": "NONE",
            "R_S_weighted_norm": "1e-9",
            "M_H": "1.0",
            "K_N": "2e-2",
            "lambda_stress_score": "2e-5",
            "kernel_stress_score": "1e-5",
            "delta_threshold": "1e-6",
            "source_path": script_path,
            "equation_ref": "synthetic_payload_smoke_not_evidence",
            "no_cancellation_guard": "True",
            "input_valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    reasons = {
        "origin": "constraint family is identified but parent object-language/origin principle is unsigned",
        "R_S_bound": "runner exists but first real R_S source row is missing",
        "multiplier_stress": "lambda/kernal stress rows are not sourced",
        "local_GR": "origin, R_S, static tau, boundary, Ward and curvature gates remain open",
        "Newton_PPN": "no claim-valid finite residual or theorem-zero row exists",
        "clock_R10_WEP": "same-frame projection and source coupling remain upstream gated",
    }
    return [
        {
            "gate_id": f"CG4394_{index}_{arena}",
            "arena": arena,
            "claim_allowed": "False",
            "reason": reason,
            "valid_for_claim": "False",
        }
        for index, (arena, reason) in enumerate(reasons.items())
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4394_0",
            "decision": DECISION,
            "summary": "4394 identifies sigma/lambda as a member of the nonpropagating constraint family but does not parent-sign its origin. To prevent another loop, it builds a strict R_S/multiplier-stress bound runner. Placeholder rows fail closed; numeric smoke proves the arithmetic only and remains nonclaim.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": DECISION,
            "timestamp_utc": STAMP,
            "summary": "origin proof remains open, but the first concrete R_S and multiplier-stress scoring runner now exists.",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4394_0",
            "target": NEXT_TARGET,
            "question": "Can we fill the first real R_S/profile or theorem-zero row, or prove sigma/lambda parent origin through object-language/constraint rank?",
            "preferred_route": "try one parent-origin proof pass using object-language and constraint-rank clauses; if unsigned, fill a real R_S source/profile row for the new runner.",
            "fallback_route": "source finite R_S, lambda stress, and kernel stress inputs with no-cancellation guard.",
            "avoid": "another origin discussion without either a signed clause or a runner-ready source row.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    origin_output: List[Dict[str, str]],
    bound_output: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# 410 PPC4161 transition: sigmaS constraint origin or RS bound runner

Marker: `{MARKER}`

## Result

4394 tests the parent-origin route and builds the fallback runner.

The origin result is honest:

`sigma/lambda` has the right mathematical species — a nonpropagating multiplier constraint — but the current corpus does not parent-sign the object-language/origin principle. The analogy to `lambda_R R_AB` helps, but it is not a proof.

So the fallback is now executable:

`|delta a_RS|/|a_N| <= K_N(s) ||R_S||_weighted/M_H + S_lambda + S_kernel`.

The new runner refuses missing source rows, refuses non-parent theorem-zero switches, and absolute-sums multiplier/kernel stress rather than allowing cancellations.

## Source Register

| source | exists | needle found | role |
|---|---:|---:|---|
"""
    for row in sources:
        text += f"| `{row['source_id']}` | {row['path_exists']} | {row['needle_found']} | {row['role']} |\n"
    text += "\n## Origin Theorems\n\n"
    for row in theorems:
        text += f"### {row['theorem_id']}\n\n- Statement: {row['statement']}\n- Derivation: {row['derivation']}\n- Status: `{row['status']}`\n\n"
    text += "## Origin Gate Output\n\n"
    for row in origin_output:
        text += f"- `{row['candidate_id']}`: pass=`{row['origin_pass']}`, origin_ready=`{row['origin_ready']}`, closed `{row['closed_clause_count']}/{row['total_clause_count']}`, failed `{row['failed_clauses']}`.\n"
    text += "\n## R_S Bound Output\n\n"
    for row in bound_output:
        text += f"- `{row['candidate_id']}`: pass_bound=`{row['pass_bound']}`, valid=`{row['valid_for_claim']}`, total=`{row['total_score']}`, reasons=`{row['refusal_reasons']}`.\n"
    text += "\n## Claim Gates\n\n"
    for row in gates:
        text += f"- `{row['arena']}`: claim_allowed=`{row['claim_allowed']}` because {row['reason']}.\n"
    text += "\n## Decision\n\n"
    text += f"{decisions[0]['summary']}\n\n"
    text += "## Next Target\n\n"
    text += f"- `{next_targets[0]['target']}`: {next_targets[0]['question']}\n"
    write_text(FORMAL_PATH, text)


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    write_text(
        DOC_PATH,
        f"""# 4394 Y5 R2FR: sigmaS constraint origin or RS bound runner

Marker: `{MARKER}`

## Private checkpoint

{decisions[0]['summary']}

## Next

{next_targets[0]['target']}

{next_targets[0]['question']}
""",
    )


def write_spine_update() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4394 local spine update: RS bound runner

Marker: `{MARKER}`

Spine update: the sigma/lambda constraint has the right nonpropagating species, but parent origin is not yet signed. The practical fallback is now executable: score `R_S=rho_top-rho_H-Delta_h sigma_S` plus absolute multiplier and kernel stress terms. This converts the open sigmaS route into a source-row problem rather than another circular proof attempt.
""",
    )


def write_packet_update() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4394 packet update: sigmaS origin gate and RS runner

Marker: `{PACKET_MARKER}`

Packet update: 4394 fails the parent-origin gate closed but builds the strict `R_S`/multiplier-stress bound runner. The next checkpoint must either sign the object-language/constraint-rank origin or feed the runner a real residual source row.
""",
    )


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4394 tests the sigma/lambda parent-origin route and builds the first strict fallback runner. The sigma/lambda sector is identified as the same nonpropagating-constraint species as the earlier lambda_R reciprocity route, but the current corpus does not parent-sign the object-language/origin principle, residual-density ownership, constraint rank, boundary zero-mode owner, or same tau/coframe clauses. A new runner now scores R_S=rho_top-rho_H-Delta_h sigma_S through |delta a_RS|/|a_N| <= K_N||R_S||/M_H plus absolute multiplier and kernel stress scores, refusing missing source paths, non-parent theorem-zero switches, cancellation, and placeholder rows. No local-GR/Newton/PPN/clock/orbital/R10 claim fires.",
            "4394 source register, origin theorem rows, origin gate input/output, R_S bound runner input/output, claim gates, decision, status, next target and validation CSV.",
            "sigmaS_origin_unsigned_RS_bound_runner_ready_nonclaim",
            "Parent-sign sigma/lambda origin or fill the first real R_S, lambda-stress and kernel-stress source rows for the runner.",
            "Late equality multiplier, post-readout Green solve, origin analogy as proof, Neumann zero-mode leakage, stress cancellation, or placeholder source rows.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4394_SOURCE_REGISTER.csv")
    theorems = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4394_ORIGIN_THEOREMS.csv")
    origin_output = read_csv(ORIGIN_OUTPUT_PATH)
    bound_output = read_csv(BOUND_OUTPUT_PATH)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4394_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4394_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4394_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add("VAL4394_2_constraint_family", any(row["theorem_id"] == "ORG4394_0_constraint_family" for row in theorems), "constraint family theorem staged")
    add("VAL4394_3_bound_law", any(row["theorem_id"] == "ORG4394_3_RS_bound_transfer" for row in theorems), "R_S bound law staged")
    add("VAL4394_4_origin_fails_closed", all(row["origin_pass"] == "False" and row["valid_for_claim"] == "False" for row in origin_output), "origin candidates fail closed")
    add("VAL4394_5_bound_rows_nonclaim", all(row["valid_for_claim"] == "False" for row in bound_output), "bound outputs remain nonclaim")
    add("VAL4394_6_bound_runner_computes", any(row["candidate_id"] == "RS4394_1_numeric_smoke_nonclaim" and row["total_score"] for row in bound_output), "bound runner computes numeric smoke")
    add("VAL4394_7_bound_runner_detects_payload", any(row["candidate_id"] == "RS4394_2_multiplier_stress_smoke_nonclaim" and row["pass_bound"] == "False" for row in bound_output), "bound runner detects multiplier payload")
    add("VAL4394_8_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4394_9_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4394_10_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4394_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4394_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4394_13_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4394_14_rows_nonclaim",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4394_15_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4394_16_origin_runner_exists", ORIGIN_RUNNER_PATH.exists() and "def evaluate_origin_rows" in read_text(ORIGIN_RUNNER_PATH), "origin runner exists")
    add("VAL4394_17_bound_runner_exists", BOUND_RUNNER_PATH.exists() and "def evaluate_bound_rows" in read_text(BOUND_RUNNER_PATH), "bound runner exists")
    return validations


def main() -> None:
    sources = source_register_rows()
    theorems = origin_theorem_rows()
    origin_inputs = origin_input_rows()
    bound_inputs = bound_input_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4394_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4394_ORIGIN_THEOREMS.csv": theorems,
        "P8_Y5_R2FR_4394_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4394_DECISION.csv": decisions,
        "P8_Y5_R2FR_4394_STATUS.csv": statuses,
        "P8_Y5_R2FR_4394_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [ORIGIN_INPUT_PATH, BOUND_INPUT_PATH]
    write_csv(ORIGIN_INPUT_PATH, origin_inputs)
    write_csv(BOUND_INPUT_PATH, bound_inputs)
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    origin_output = evaluate_origin_rows(ORIGIN_INPUT_PATH)
    bound_output = evaluate_bound_rows(BOUND_INPUT_PATH)
    write_csv(ORIGIN_OUTPUT_PATH, origin_output)
    write_csv(BOUND_OUTPUT_PATH, bound_output)
    csv_paths.extend([ORIGIN_OUTPUT_PATH, BOUND_OUTPUT_PATH])

    write_formal_doc(sources, theorems, origin_output, bound_output, gates, decisions, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
