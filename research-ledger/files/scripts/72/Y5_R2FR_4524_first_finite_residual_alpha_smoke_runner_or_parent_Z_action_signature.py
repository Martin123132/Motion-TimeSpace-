from __future__ import annotations

import csv
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = POST / "source-intake" / "local_bounds"
RUN_DIR = POST / "runs" / "4524-first-finite-residual-alpha-smoke-runner"
RUN_INPUTS = RUN_DIR / "inputs"

CHECKPOINT = "4524"
CLAIM_ID = "L-366"
MARKER = "PPC4161_FIRST_FINITE_RESIDUAL_ALPHA_SMOKE_RUNNER_OR_PARENT_Z_ACTION_SIGNATURE_4524"
PACKET_MARKER = "PPC4161_PACKET_FIRST_FINITE_RESIDUAL_ALPHA_SMOKE_RUNNER_OR_PARENT_Z_ACTION_SIGNATURE_4524"
DECISION = "FINITE_RESIDUAL_ALPHA_BRIDGE_EXECUTABLE_LIVE_BRANCH_BLOCKED_TOY_INTERPOLATION_FAILS_PARENT_Z_ACTION_STILL_PREFERRED"
NEXT_TARGET = "4525-Y5-R2FR-parent-Z-algebraic-action-derivation-or-source-normalized-first-coefficient-fill.md"

FORMAL_PATH = FORMAL / "540-PPC4161-first-finite-residual-alpha-smoke-runner-or-parent-Z-action-signature.md"
DOC_PATH = POST / "4524-Y5-R2FR-first-finite-residual-alpha-smoke-runner-or-parent-Z-action-signature.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4524_SOURCE_REGISTER.csv"
LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4524_FINITE_RESIDUAL_ALPHA_LAW.csv"
INPUTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4524_RESIDUAL_ALPHA_INPUT_CONTRACT.csv"
PARENT_Z_CSV = SOURCE_DIR / "P8_Y5_R2FR_4524_PARENT_Z_ACTION_SIGNATURE_HUNT.csv"
LIVE_STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4524_R10_LIVE_PLACEHOLDER_RUNNER_STATUS.csv"
TOY_STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4524_R10_TOY_INTERPOLATION_SMOKE_STATUS.csv"
TOY_INPUT_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4524_TOY_INPUT_REGISTER.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4524_DECISION.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4524_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4524_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4524_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4524_VALIDATION.csv"

R10_RUNNER = SCRIPT_DIR / "R10_alpha_lambda_bound_prediction_runner.py"
LIVE_MTS_CURVE = SOURCE_DIR / "R10_alpha_lambda_curve_MTS_source_normalization.csv"
LIVE_BOUND_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
TOY_MTS_CURVE = RUN_INPUTS / "toy_MTS_alpha_curve_interpolation_fail_NONCLAIM.csv"
TOY_BOUND_CURVE = RUN_INPUTS / "toy_R10_alpha_bound_curve_interpolation_fail_NONCLAIM.csv"

DOC_4523 = POST / "4523-Y5-R2FR-same-branch-parent-signature-audit-or-first-alpha-runner.md"
FORMAL_4523 = FORMAL / "539-PPC4161-same-branch-parent-signature-audit-or-first-alpha-runner.md"
VALIDATION_4523 = SOURCE_DIR / "P8_Y5_BRR545_4523_VALIDATION.csv"
ALPHA_INPUTS_4523 = SOURCE_DIR / "P8_Y5_R2FR_4523_FIRST_ALPHA_RUNNER_INPUTS.csv"
RUNNER_TRIGGER_4523 = SOURCE_DIR / "P8_Y5_R2FR_4523_FIRST_ALPHA_RESIDUAL_RUNNER_TRIGGER.csv"
PARENT_ACTION_4523 = SOURCE_DIR / "P8_Y5_R2FR_4523_RANK_ZERO_PARENT_ACTION_CONTRACT.csv"
DECISION_4523 = SOURCE_DIR / "P8_Y5_R2FR_4523_DECISION.csv"
FORMAL_4520 = FORMAL / "536-PPC4161-rank-zero-source-current-silence-or-alpha-input-acquisition.md"
FORMAL_4521 = FORMAL / "537-PPC4161-boundary-CDB-readout-silence-or-alpha-input-fill.md"
FORMAL_4522 = FORMAL / "538-PPC4161-rank-M-lock-and-retained-current-firewall-or-alpha-runner.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def line_of(path: Path, needle: str) -> int:
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        try:
            return str(path.relative_to(POST)).replace("\\", "/")
        except ValueError:
            return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, body: str) -> None:
    current = text(path)
    if marker in current:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as handle:
        if current and not current.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + body.strip() + "\n")


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4524_00_formal4523", "4523 formal handoff", FORMAL_4523, "PPC4161_SAME_BRANCH_PARENT_SIGNATURE_AUDIT_OR_FIRST_ALPHA_RUNNER_4523", "same-branch failure and runner trigger"),
        ("SRC4524_01_post4523", "4523 post handoff", DOC_4523, "4524-Y5-R2FR-first-finite-residual-alpha-smoke-runner-or-parent-Z-action-signature.md", "declared 4524 target"),
        ("SRC4524_02_val4523", "4523 validation", VALIDATION_4523, "VAL4523_OVERALL", "previous validation pass"),
        ("SRC4524_03_alpha_inputs4523", "4523 alpha inputs", ALPHA_INPUTS_4523, "AIR4523_0_mmin", "rank-zero and finite-alpha input pack"),
        ("SRC4524_04_trigger4523", "4523 runner trigger", RUNNER_TRIGGER_4523, "RTR4523_2_finite_alpha", "finite-alpha dryrun blocked"),
        ("SRC4524_05_action4523", "4523 parent action contract", PARENT_ACTION_4523, "RZPA4523_2_M_lock", "M lock source signature"),
        ("SRC4524_06_decision4523", "4523 decision", DECISION_4523, "DEC4523_0", "same-branch claim failed"),
        ("SRC4524_07_formal4520", "4520 source-current theorem", FORMAL_4520, "PPC4161_RANK_ZERO_SOURCE_CURRENT_SILENCE_OR_ALPHA_INPUT_ACQUISITION_4520", "Hilbert/Poynting retained-current split"),
        ("SRC4524_08_formal4521", "4521 boundary/CDB/readout theorem", FORMAL_4521, "PPC4161_BOUNDARY_CDB_READOUT_SILENCE_OR_ALPHA_INPUT_FILL_4521", "B/CDB/R termwise silence or bounds"),
        ("SRC4524_09_formal4522", "4522 M-lock theorem", FORMAL_4522, "PPC4161_RANK_M_LOCK_AND_RETAINED_CURRENT_FIREWALL_OR_ALPHA_RUNNER_4522", "coercive finite residual bound"),
        ("SRC4524_10_r10_runner", "existing R10 runner", R10_RUNNER, "def run_runner", "schema/unit/interpolation comparator"),
        ("SRC4524_11_live_mts", "live MTS alpha placeholder", LIVE_MTS_CURVE, "MISSING_SOURCE_NORMALIZED_ALPHA_PREDICTION", "live branch remains blocked"),
        ("SRC4524_12_live_bound", "live R10 bound placeholder", LIVE_BOUND_CURVE, "MISSING_DIGITIZED_ALPHA_BOUND", "live bound curve remains blocked"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, role, path, needle, note in specs:
        body = text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in body,
                "line": line_of(path, needle),
                "note": note,
                "valid_for_claim": False,
            }
        )
    return rows


def law_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "FRA4524_0_rank_zero_residual",
            "object": "rank-zero algebraic residual",
            "derivation": "4520-4522 reduce the active local obstruction to M_AB Z^B = J_A^retained + B_A + C_A^CDB + R_A when rank(Z_AB)=0.",
            "formula": "M_AB Z^B = R_A^tot, R_A^tot := J_A^retained + B_A + C_A^CDB + R_A",
            "status": "DERIVED_CONDITIONAL_FROM_4520_4522",
            "valid_for_claim": False,
        },
        {
            "law_id": "FRA4524_1_coercive_bound",
            "object": "finite residual amplitude bound",
            "derivation": "If M_AB is coercive with smallest physical eigenvalue m_min>0, the algebraic branch has a no-cancellation bound.",
            "formula": "||Z|| <= m_min^-1 (||J_retained|| + ||B|| + ||CDB|| + ||R||)",
            "status": "DERIVED_CONDITIONAL_NEEDS_MMIN_AND_NORMS",
            "valid_for_claim": False,
        },
        {
            "law_id": "FRA4524_2_arena_projection",
            "object": "observable residual vector",
            "derivation": "An arena transfer operator K_a maps the local residual amplitude into PPN, R10, clock, orbital or EM observables.",
            "formula": "|delta O_a| <= ||K_a|| ||Z|| + |direct_tail_a|",
            "status": "DERIVED_OPERATOR_BOUND_NEEDS_K_A",
            "valid_for_claim": False,
        },
        {
            "law_id": "FRA4524_3_R10_alpha_projection",
            "object": "fifth-force alpha bound",
            "derivation": "For a static Yukawa-like residual kernel delta V_ST(r) = -C_X^ST exp(-r/lambda_X)/r, comparison with V_N = -G_N M_S m_T/r gives alpha_X = C_X^ST/(G_N M_S m_T).",
            "formula": "|alpha_X| <= K_R10_X/(G_N M_S m_T) * m_min^-1 (||J_retained|| + ||B|| + ||CDB|| + ||R||)",
            "status": "DERIVED_CONDITIONAL_ALPHA_BRIDGE_NEEDS_SOURCE_NORMALIZATION",
            "valid_for_claim": False,
        },
        {
            "law_id": "FRA4524_4_finite_range_mode",
            "object": "finite principal branch alpha law",
            "derivation": "If a retained finite-range mode X exists with mass M_X and source/test charges Q_X^S and q_X^T, the Yukawa coefficient is an explicit product rather than a free fit.",
            "formula": "alpha_X(lambda_X) = K_X Qbar_XS qbar_XT / (G_N M_S m_T M_X^2), lambda_X = 1/M_X, up to the declared Green-kernel convention",
            "status": "DERIVED_TEMPLATE_NEEDS_K_Q_Q_M_SOURCES",
            "valid_for_claim": False,
        },
        {
            "law_id": "FRA4524_5_Poynting_wave_channel",
            "object": "EM/Poynting and wave residual routing",
            "derivation": "A Hilbert-owned stationary no-flux Poynting sector is silent only through the boundary flux theorem; radiative or non-Hilbert wave flux is not erased and enters B_A or J_A^retained before alpha scoring.",
            "formula": "B_A^EM = int_boundary v_A^nu T^EM_{mu nu} n^mu dSigma; B_A^EM=0 only under owned no-flux, otherwise retained in R_A^tot",
            "status": "DERIVED_ROUTING_RULE_NOT_ZERO_AXIOM",
            "valid_for_claim": False,
        },
        {
            "law_id": "FRA4524_6_no_claim_firewall",
            "object": "claim rule",
            "derivation": "No alpha/local-GR claim is allowed unless m_min, residual norms, K_R10, source/test charges, calibration and a full source-backed bound curve are numeric and sourced.",
            "formula": "claim_allowed iff every source input is numeric/sourced and |alpha_predicted(lambda)| <= alpha_bound(lambda) over the declared domain",
            "status": "HARD_GATE",
            "valid_for_claim": False,
        },
    ]


def input_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "RAI4524_0_mmin",
            "symbol": "m_min(M_AB)",
            "role": "coercive algebraic lock",
            "required_source": "parent Z-action Hessian or constraint Schur complement on the physical quotient",
            "current_value": "MISSING",
            "claim_gate": "BLOCKED",
            "valid_for_claim": False,
        },
        {
            "input_id": "RAI4524_1_residual_norms",
            "symbol": "||J_retained||, ||B||, ||CDB||, ||R||",
            "role": "rank-zero RHS amplitude",
            "required_source": "same-branch zero theorem or finite source-backed residual profiles",
            "current_value": "MISSING",
            "claim_gate": "BLOCKED",
            "valid_for_claim": False,
        },
        {
            "input_id": "RAI4524_2_K_R10",
            "symbol": "K_R10_X",
            "role": "projection from local residual to fifth-force alpha",
            "required_source": "arena transfer operator with units and Green-kernel convention",
            "current_value": "MISSING",
            "claim_gate": "BLOCKED",
            "valid_for_claim": False,
        },
        {
            "input_id": "RAI4524_3_source_test_charges",
            "symbol": "Qbar_XS, qbar_XT",
            "role": "source/test response product",
            "required_source": "same-frame source-normalized charge integral, not inferred from exclusion bounds",
            "current_value": "MISSING",
            "claim_gate": "BLOCKED",
            "valid_for_claim": False,
        },
        {
            "input_id": "RAI4524_4_mass_range",
            "symbol": "M_X^2, lambda_X",
            "role": "finite-range Yukawa kernel",
            "required_source": "parent principal operator/eigenvalue with unit convention",
            "current_value": "MISSING",
            "claim_gate": "BLOCKED",
            "valid_for_claim": False,
        },
        {
            "input_id": "RAI4524_5_bound_curve",
            "symbol": "alpha_bound(lambda)",
            "role": "external R10 comparison curve",
            "required_source": "full digitized/source-backed curve or official machine-readable table",
            "current_value": "PLACEHOLDER_LIVE_FILE",
            "claim_gate": "BLOCKED",
            "valid_for_claim": False,
        },
        {
            "input_id": "RAI4524_6_EM_wave_flux",
            "symbol": "B_A^EM or J_A^wave",
            "role": "Poynting/wave residual route",
            "required_source": "stationary no-flux theorem or radiative flux profile before variation",
            "current_value": "ROUTED_NOT_NUMERIC",
            "claim_gate": "BLOCKED",
            "valid_for_claim": False,
        },
    ]


def parent_z_rows() -> list[dict[str, Any]]:
    return [
        {
            "hunt_id": "PZA4524_0_action_form",
            "required_signature": "S_Z = 1/2 int sqrt(-g) Z^A M_AB(q) Z^B + int sqrt(-g) Z^A R_A^tot with no Z kinetic term",
            "why_it_matters": "This is the parent-owned route to rank-zero closure instead of an empirical alpha branch.",
            "current_status": "CONTRACT_KNOWN_SOURCE_NOT_FOUND",
            "next_derivation_move": "search parent action/coupling notes for an auxiliary algebraic field or constraint multiplier that exactly matches Z_A",
            "valid_for_claim": False,
        },
        {
            "hunt_id": "PZA4524_1_no_linear_sources",
            "required_signature": "R_A^tot vanishes termwise by q-basic Hilbert ownership, no-flux boundary, pure readout and no retained source vertices",
            "why_it_matters": "Without this, local GR is bounded rather than derived.",
            "current_status": "UNSIGNED_COUNTERCHANNELS_LIVE",
            "next_derivation_move": "attempt source-neutrality proof for calibration/source/worldtube/marker/memory/Poynting channels one by one",
            "valid_for_claim": False,
        },
        {
            "hunt_id": "PZA4524_2_constraint_nulls",
            "required_signature": "ker(M_AB) is exactly gauge/constraint-owned with differentiable charge and no boundary leakage",
            "why_it_matters": "Null algebraic directions cannot be left as hidden free physics.",
            "current_status": "UNSIGNED_CONSTRAINT_ALGEBRA_NOT_CLOSED",
            "next_derivation_move": "derive bracket-preserving constraint reduction or demote null directions to finite residual scoring",
            "valid_for_claim": False,
        },
        {
            "hunt_id": "PZA4524_3_numeric_fallback",
            "required_signature": "if any parent signature fails, fill RAI4524 rows and run alpha/PPN/clock/orbital residual scoring",
            "why_it_matters": "Keeps the branch testable instead of rhetorical.",
            "current_status": "RUNNER_EXECUTABLE_INPUTS_BLOCKED",
            "next_derivation_move": NEXT_TARGET,
            "valid_for_claim": False,
        },
    ]


def toy_mts_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_id": "TOY_NOT_MTS_4524",
            "branch_id": "toy_interpolation_fail",
            "curve_id": "toy_alpha_curve_interpolation_fail",
            "lambda_value": "0.0031622776601683794",
            "lambda_units": "m",
            "alpha_predicted": "20.0",
            "alpha_bound": "",
            "alpha_bound_source": "toy local 4524 smoke bound file",
            "force_law_form": "toy_yukawa_schema_only",
            "derivation_status": "toy_mechanical_validation_not_physics",
            "formula_reference": rel(DOC_PATH),
            "source_file": rel(Path("scripts") / Path(__file__).name),
            "assumptions": "tests schema units log interpolation and failure mode only",
            "valid_for_claim": "true",
            "notes": "not an MTS row; deliberately fails bound so claim_allowed remains false",
        }
    ]


def toy_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "TOY_BOUND_4524_A",
            "dataset_id": "toy_interpolation_fail_nonclaim",
            "lambda_value": "0.001",
            "lambda_units": "m",
            "alpha_bound": "1.0",
            "alpha_bound_source": "toy local 4524 smoke bound file",
            "digitization_method": "toy_exact_point",
            "source_file": rel(Path("scripts") / Path(__file__).name),
            "valid_for_claim": "true",
            "notes": "toy row; not a physics bound",
        },
        {
            "bound_id": "TOY_BOUND_4524_B",
            "dataset_id": "toy_interpolation_fail_nonclaim",
            "lambda_value": "0.01",
            "lambda_units": "m",
            "alpha_bound": "10.0",
            "alpha_bound_source": "toy local 4524 smoke bound file",
            "digitization_method": "toy_exact_point",
            "source_file": rel(Path("scripts") / Path(__file__).name),
            "valid_for_claim": "true",
            "notes": "toy row; not a physics bound",
        },
    ]


def run_alpha_runner(mts_curve: Path, bound_curve: Path, output_dir: Path) -> dict[str, Any]:
    sys.path.insert(0, str(SCRIPT_DIR))
    from R10_alpha_lambda_bound_prediction_runner import run_runner

    return run_runner(mts_curve=mts_curve, bound_curve=bound_curve, output_dir=output_dir)


def status_rows_from_result(prefix: str, result: dict[str, Any]) -> list[dict[str, Any]]:
    status = result["status"]
    comparisons = result["comparisons"]
    rows: list[dict[str, Any]] = [
        {
            "status_id": f"{prefix}_STATUS",
            "mts_rows": status["mts_rows"],
            "bound_rows": status["bound_rows"],
            "valid_mts_rows": status["valid_mts_rows"],
            "valid_bound_rows": status["valid_bound_rows"],
            "comparison_rows": status["comparison_rows"],
            "passed_rows": status["passed_rows"],
            "blocked_or_failed_rows": status["blocked_or_failed_rows"],
            "claim_allowed": status["claim_allowed"],
            "output_dir": status["output_dir"],
        }
    ]
    for row in comparisons:
        rows.append({"status_id": f"{prefix}_{row.get('comparison_id', 'comparison')}", **row})
    return rows


def decision_rows(live_status: dict[str, Any], toy_status: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4524_0",
            "decision": DECISION,
            "live_claim_allowed": live_status["status"]["claim_allowed"],
            "toy_claim_allowed": toy_status["status"]["claim_allowed"],
            "meaning": "The finite-residual to alpha bridge is now executable. The live branch remains blocked by missing source-normalized MTS rows and missing full R10 bound curve. The toy branch proves the runner detects a bound failure.",
            "preferred_next_route": "derive parent Z algebraic action signature first; if that fails, fill source-normalized residual coefficients for the runner",
            "valid_for_claim": False,
        }
    ]


def claim_gate_rows(live_status: dict[str, Any], toy_status: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG4524_0_live_branch",
            "gate": "live R10 branch cannot claim",
            "status": "PASS_BLOCKED",
            "evidence": json.dumps(live_status["status"], sort_keys=True),
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4524_1_toy_branch",
            "gate": "toy smoke branch cannot claim",
            "status": "PASS_TOY_FAILS_BOUND",
            "evidence": json.dumps(toy_status["status"], sort_keys=True),
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4524_2_parent_Z",
            "gate": "parent Z action still unsigned",
            "status": "BLOCKED_FOR_LOCAL_GR_CLAIM",
            "evidence": "PZA4524 requires algebraic Z action, no retained source vertices, and constraint-owned nulls",
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "claim_id": CLAIM_ID,
            "marker": MARKER,
            "decision": DECISION,
            "claim_status": "private_conditional_nonclaim_runner_executable",
            "created_at_utc": now(),
            "next_target": NEXT_TARGET,
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "derive parent Z algebraic action first, otherwise fill source-normalized coefficient rows",
            "why": "This is the least-cheaty route: local GR comes from parent action if possible; if not, the residual becomes a measured alpha/PPN/clock/orbital vector.",
            "valid_for_claim": False,
        }
    ]


def toy_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "toy_id": "TOY4524_MTS",
            "path": str(TOY_MTS_CURVE),
            "purpose": "mechanical runner validation only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "toy_id": "TOY4524_BOUND",
            "path": str(TOY_BOUND_CURVE),
            "purpose": "mechanical runner validation only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def validate(
    sources: list[dict[str, Any]],
    live_status: dict[str, Any],
    toy_status: dict[str, Any],
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER,
        LAW_CSV,
        INPUTS_CSV,
        PARENT_Z_CSV,
        LIVE_STATUS_CSV,
        TOY_STATUS_CSV,
        TOY_INPUT_REGISTER,
        DECISION_CSV,
        CLAIM_GATES_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    parse_issues: list[str] = []
    for path in csv_paths:
        try:
            rows = read_csv(path)
            if not rows:
                parse_issues.append(f"{path.name}:empty")
        except Exception as error:
            parse_issues.append(f"{path.name}:{error}")
    rows = [
        {
            "validation_id": "VAL4524_00_sources",
            "status": "PASS" if all(row["exists"] and row["needle_found"] for row in sources) else "FAIL",
            "detail": "all source paths exist and source needles are found",
        },
        {
            "validation_id": "VAL4524_01_live_runner",
            "status": "PASS" if live_status["status"]["claim_allowed"] is False and live_status["status"]["valid_mts_rows"] == 0 else "FAIL",
            "detail": json.dumps(live_status["status"], sort_keys=True),
        },
        {
            "validation_id": "VAL4524_02_toy_runner",
            "status": "PASS" if toy_status["status"]["claim_allowed"] is False and toy_status["status"]["valid_mts_rows"] == 1 and toy_status["status"]["valid_bound_rows"] == 2 else "FAIL",
            "detail": json.dumps(toy_status["status"], sort_keys=True),
        },
        {
            "validation_id": "VAL4524_03_law",
            "status": "PASS" if any(row.get("law_id") == "FRA4524_3_R10_alpha_projection" for row in read_csv(LAW_CSV)) else "FAIL",
            "detail": "finite residual alpha bridge row present",
        },
        {
            "validation_id": "VAL4524_04_parent_Z",
            "status": "PASS" if any(row.get("hunt_id") == "PZA4524_0_action_form" for row in read_csv(PARENT_Z_CSV)) else "FAIL",
            "detail": "parent Z action signature hunt row present",
        },
        {
            "validation_id": "VAL4524_05_claims_blocked",
            "status": "PASS" if all(str(row.get("valid_for_claim", "")).lower() == "false" for row in claims) else "FAIL",
            "detail": "all claim gates remain blocked",
        },
        {
            "validation_id": "VAL4524_06_csv_parse",
            "status": "PASS" if not parse_issues else "FAIL",
            "detail": ";".join(parse_issues) if parse_issues else "all generated CSV files parse and have rows",
        },
        {
            "validation_id": "VAL4524_07_next_target",
            "status": "PASS" if NEXT_TARGET.startswith("4525-") else "FAIL",
            "detail": NEXT_TARGET,
        },
        {
            "validation_id": "VAL4524_08_pycache_absent",
            "status": "PASS" if not (SCRIPT_DIR / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append({"validation_id": "VAL4524_OVERALL", "status": overall, "detail": "4524 finite residual alpha smoke runner"})
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    laws: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    parent_z: list[dict[str, Any]],
    live_rows: list[dict[str, Any]],
    toy_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4524 — First Finite Residual Alpha Smoke Runner Or Parent Z Action Signature

Marker: `{MARKER}`  
Packet marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}`  
Status: private conditional non-claim; runner executable, live claim blocked.

## What moved forward

4523 wrote the exact parent `Z`-action contract and showed the same-branch parent signature is not claim-grade. 4524 does not circle that result. It builds the executable fallback:

```text
M_AB Z^B = R_A^tot
R_A^tot = J_A^retained + B_A + C_A^CDB + R_A
||Z|| <= m_min^-1 ||R_A^tot||
|alpha_X| <= K_R10_X ||Z|| / (G_N M_S m_T)
```

This means an unsigned local-GR route now has two honest exits:

1. derive the parent algebraic `Z` action and close the branch;
2. fill source-normalized residual coefficients and let the R10/PPN/clock/orbital runner score the finite residual.

The Poynting/wave channel is explicitly routed rather than hand-waved: Hilbert-owned stationary no-flux is silent; radiative or non-Hilbert EM flux becomes `B_A^EM` or `J_A^wave` and must be scored.

## Finite Residual Alpha Law

{table(laws)}

## Required Inputs

{table(inputs)}

## Parent Z Action Hunt

{table(parent_z)}

## Live R10 Runner Status

{table(live_rows)}

## Toy Interpolation Smoke Status

{table(toy_rows)}

## Decision

{table(decisions)}

## Claim Gates

{table(gates)}

## Sources

{table(sources)}

## Validation

{table(validation)}

## Next

`{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    current = text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in current:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r2fr_finite_residual_alpha",
        "claim": "4524 derives the finite-residual to R10 alpha bridge, runs the live placeholder branch as blocked, and runs a toy interpolation-failure smoke test to prove the comparator is executable without allowing a claim.",
        "current_evidence": "Generated finite residual alpha law, residual input contract, parent Z action hunt, live/toy R10 runner outputs, and validation P8_Y5_BRR545_4524_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim_runner_executable",
        "next_test": NEXT_TARGET,
        "key_risk": "Toy runner rows are mechanical only; live MTS alpha and real R10 bound curve remain missing, and parent Z action remains unsigned.",
        "sector": "local_gr_newton",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Confusing an executable fallback runner with a local-GR or R10 pass; no claim is allowed until real source-normalized coefficients and bound curves are supplied.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def main() -> None:
    RUN_INPUTS.mkdir(parents=True, exist_ok=True)
    write_csv(TOY_MTS_CURVE, toy_mts_rows())
    write_csv(TOY_BOUND_CURVE, toy_bound_rows())

    live_result = run_alpha_runner(LIVE_MTS_CURVE, LIVE_BOUND_CURVE, RUN_DIR / "live_placeholder_results")
    toy_result = run_alpha_runner(TOY_MTS_CURVE, TOY_BOUND_CURVE, RUN_DIR / "toy_interpolation_fail_results")

    sources = source_rows()
    laws = law_rows()
    inputs = input_contract_rows()
    parent_z = parent_z_rows()
    live_status_rows = status_rows_from_result("LIVE4524", live_result)
    toy_status_rows = status_rows_from_result("TOY4524", toy_result)
    toy_register = toy_register_rows()
    decisions = decision_rows(live_result, toy_result)
    gates = claim_gate_rows(live_result, toy_result)
    status = status_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(LAW_CSV, laws)
    write_csv(INPUTS_CSV, inputs)
    write_csv(PARENT_Z_CSV, parent_z)
    write_csv(LIVE_STATUS_CSV, live_status_rows)
    write_csv(TOY_STATUS_CSV, toy_status_rows)
    write_csv(TOY_INPUT_REGISTER, toy_register)
    write_csv(DECISION_CSV, decisions)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, live_result, toy_result, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, laws, inputs, parent_z, live_status_rows, toy_status_rows, decisions, gates, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4524 First Finite Residual Alpha Smoke Runner Or Parent Z Action Signature

Marker: `{MARKER}`  
The local branch now has an executable finite-residual to alpha bridge. If the parent algebraic `Z` action is not derived, residual pieces are no longer rhetorical: `||Z|| <= m_min^-1(||J_retained||+||B||+||CDB||+||R||)` and `|alpha_X| <= K_R10_X ||Z||/(G_N M_S m_T)` define the source-normalized scoring route. Live data remain blocked; a toy run verifies interpolation and failure behavior.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4524 Packet Integration

Marker: `{PACKET_MARKER}`  
The PPC4161 packet now separates derivation from scoring: parent `Z` action closure is the preferred route, while finite residuals feed an executable alpha runner if closure fails. Poynting/wave flux is explicitly routed into boundary or retained-current terms unless an owned no-flux theorem applies. Next target: `{NEXT_TARGET}`.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"live claim_allowed {live_result['status']['claim_allowed']}")
    print(f"toy claim_allowed {toy_result['status']['claim_allowed']}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
