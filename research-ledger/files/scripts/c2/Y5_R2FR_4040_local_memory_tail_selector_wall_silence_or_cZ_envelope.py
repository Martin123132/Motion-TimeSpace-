from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
MICRO_DIR = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4040-Y5-R2FR-local-memory-tail-selector-wall-silence-or-cZ-envelope.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4040_SOURCE_REGISTER.csv",
    "tail_wall_theorem": SOURCE_DIR / "P8_Y5_R2FR_4040_TAIL_WALL_THEOREM_ATTEMPT.csv",
    "cz_envelope": SOURCE_DIR / "P8_Y5_R2FR_4040_CZ_ENVELOPE.csv",
    "input_contract": SOURCE_DIR / "P8_Y5_R2FR_4040_CZ_INPUT_CONTRACT.csv",
    "remaining_residuals": SOURCE_DIR / "P8_Y5_R2FR_4040_REMAINING_LOCAL_RESIDUAL_VECTOR.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4040_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4040_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4040_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4040_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4040_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4040_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(ts: str) -> List[Dict[str, object]]:
    specs = [
        ("SRC4040_0", ROOT / "4039-Y5-R2FR-hidden-current-fixed-point-silence-or-cZ-bound.md", "C_Z_NARROWED_NOT_FULLY_ZEROED", "immediate predecessor verdict"),
        ("SRC4040_1", SOURCE_DIR / "P8_Y5_R2FR_4039_CZ_BOUND_TEMPLATE.csv", "J_Z^tail = P_loc integral K_mem", "tail/wall bound template"),
        ("SRC4040_2", SOURCE_DIR / "P8_Y5_R2FR_4039_REMAINING_LOCAL_RESIDUAL_VECTOR.csv", "derive local kernel support/gap/tail silence", "next route from 4039"),
        ("SRC4040_3", SOURCE_DIR / "P8_Y5_R2FR_3894_MEMORY_JX_COMPONENT_CLOSURE_GATE.csv", "history_tail_norm remains needed", "memory tail obstruction"),
        ("SRC4040_4", MICRO_DIR / "domain_selector_audit_nonclaim_1514.csv", "domain selector remains a live generator", "selector wall obstruction"),
        ("SRC4040_5", SOURCE_DIR / "P8_Y5_R2FR_4031_EXTERIOR_COLLAR_DELTAPHI_THEOREM.csv", "int_Omega(|grad u|^2+mu_phi^2 u^2)dV", "collar positive energy identity"),
        ("SRC4040_6", SOURCE_DIR / "P8_Y5_R2FR_3645_JX_VARIATION_DERIVATION.csv", "numeric_profile_run_allowed=false", "profile run refusal contract"),
        ("SRC4040_7", ROOT / "1127-Y5-R10-local-vs-FLRW-branch-selector-no-flux-certificate.md", "global all-domain zero is forbidden", "do not erase cosmology/memory guard"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": ts,
            }
        )
    return rows


def theorem_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "TW4040_0_tail_zero_sufficient",
            "piece": "local memory-tail silence sufficient condition",
            "statement": "If P_loc K_mem vanishes on the compact stationary collar, or its support is disjoint from the collar, then J_Z^history_tail=0 locally.",
            "formula": "J_Z^tail(x)=P_loc int K_mem(x,y) H(y) dy; P_loc K_mem|Omega_ext=0 => J_Z^tail=0",
            "current_evidence": "not proven by current corpus",
            "status": "SUFFICIENT_THEOREM_WRITTEN_NOT_CLOSED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "TW4040_1_tail_gap_bound",
            "piece": "exponential/local gap bound",
            "statement": "If the local memory kernel is massive/stable with range ell_mem, the collar tail is exponentially bounded.",
            "formula": "||J_Z^tail||_1 <= C_mem exp(-L_collar/ell_mem) ||H||_1",
            "current_evidence": "kernel range/support constants missing",
            "status": "BOUND_THEOREM_DERIVED_SYMBOLICALLY",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "TW4040_2_selector_wall_zero",
            "piece": "selector-wall silence sufficient condition",
            "statement": "If the branch selector is fixed, exact/topological, or geometry-derived with no transition surface motion, then J_Z^selector_wall=0.",
            "formula": "jump(D_Z n.grad Z)|Sigma=0 and delta S_wall/delta Z=0 => J_Z^wall=0",
            "current_evidence": "domain selector audit keeps this unsigned",
            "status": "SUFFICIENT_THEOREM_WRITTEN_NOT_CLOSED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "TW4040_3_no_global_memory_zero",
            "piece": "cosmology guard",
            "statement": "Local tail silence cannot be promoted to global all-domain memory silence.",
            "formula": "P_loc K_mem=0 does not imply P_FLRW K_mem=0",
            "current_evidence": "1127 guard preserved",
            "status": "GLOBAL_OVERKILL_GUARD",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "TW4040_4_current_verdict",
            "piece": "4040 verdict",
            "statement": "The exact zero route is clear but not closed; carry an absolute c_Z envelope forward.",
            "formula": "A_Z <= A_tail + A_wall, both nonnegative envelopes",
            "current_evidence": "tail support/gap and selector no-wall inputs are missing",
            "status": "LOCAL_MEMORY_SELECTOR_SILENCE_NOT_PROVED_CZ_ENVELOPE_ACTIVE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def envelope_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "envelope_id": "ENV4040_0_tail",
            "component": "memory_tail",
            "formula": "A_tail <= C_G(D_Z,M_Z,L_collar)*|c_Z|*C_mem*exp(-L_collar/ell_mem)*||H||_1",
            "zero_condition": "P_loc K_mem=0 or C_mem=0 on compact stationary collar",
            "claim_status": "symbolic_bound_not_numeric",
            "needed_inputs": "D_Z,M_Z_or_lambda_Z,L_collar,C_mem,ell_mem,history_norm,projection_norm,c_Z",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "envelope_id": "ENV4040_1_wall",
            "component": "selector_wall",
            "formula": "A_wall <= C_G(D_Z,M_Z,L_collar)*|c_Z|*(||jump(D_Z n.grad Z)||_Sigma + ||delta S_wall/delta Z||_Sigma)",
            "zero_condition": "fixed/exact/topological selector with no wall motion and no shell mismatch",
            "claim_status": "symbolic_bound_not_numeric",
            "needed_inputs": "transition_support,Sigma_norm,jump_norm,wall_variation_norm,D_Z,M_Z,c_Z",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "envelope_id": "ENV4040_2_absolute",
            "component": "total_cZ_remaining",
            "formula": "A_Z_remaining <= A_tail + A_wall; Delta_local_GR_abs includes |A_Z_remaining| with no cancellation credit",
            "zero_condition": "A_tail=0 and A_wall=0",
            "claim_status": "absolute_envelope_ready_not_scoreable",
            "needed_inputs": "all tail and wall inputs plus arena projection constants for R10/PPN/clock/orbital",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def input_contract_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "input_id": "IN4040_0_kernel",
            "quantity": "K_mem local tail norm",
            "required_for": "prove/bound J_Z^history_tail",
            "acceptable_evidence": "parent kernel support theorem, gap/range derivation, or source-backed numeric norm",
            "current_status": "MISSING",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "input_id": "IN4040_1_selector",
            "quantity": "selector wall motion/shell mismatch",
            "required_for": "prove/bound J_Z^selector_wall",
            "acceptable_evidence": "geometry-derived fixed selector theorem, topological/exact proof, or finite wall norm",
            "current_status": "MISSING",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "input_id": "IN4040_2_operator",
            "quantity": "D_Z,M_Z,lambda_Z,Green constant",
            "required_for": "convert current norm to amplitude/local force envelope",
            "acceptable_evidence": "parent Hessian/gap coefficients or conservative sourced priors",
            "current_status": "MISSING_NUMERIC_VALUES",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "input_id": "IN4040_3_projection",
            "quantity": "arena projection constants",
            "required_for": "R10/PPN/clock/orbital score",
            "acceptable_evidence": "derived projection map or conservative bound rows",
            "current_status": "MISSING",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def remaining_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "REM4040_0_cZ_envelope",
            "symbol": "Delta_cZ_envelope",
            "residual": "absolute c_Z tail/wall envelope carried forward as nonclaim residual",
            "current_route": "fill kernel/selector/operator inputs or prove both zero before any local-GR pass",
            "priority": "carried",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4040_1_norm",
            "symbol": "c_norm",
            "residual": "universal source/action normalization drift",
            "current_route": "route common mode into calibrated kappa_obs/Newton G or bound time/source variation",
            "priority": "next",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4040_2_nonEH",
            "symbol": "c_nonEH",
            "residual": "non-EH or higher-curvature metric operator leakage",
            "current_route": "show decoupling at local scale or compare to PPN/Cassini-style bounds",
            "priority": "after_cnorm",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def evaluator_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "case_id": "CASE4040_0_current",
            "verdict": "TAIL_WALL_SILENCE_NOT_PROVED_CZ_ENVELOPE_ACTIVE",
            "result": "c_Z is converted from open hidden current into absolute tail/wall envelope",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4040",
            "next_action": "carry Delta_cZ_envelope and attack c_norm/Newton-G calibration route",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4040_1_future_zero",
            "verdict": "FULL_CZ_ZERO_IF_KERNEL_AND_SELECTOR_INPUTS_CLOSE",
            "result": "A_tail=A_wall=0 would remove c_Z from local residual vector",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4040",
            "next_action": "requires parent kernel support/gap and selector no-wall proof",
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4040_0_not_zero",
            "decision": "Do not claim local memory-tail or selector-wall silence from current evidence.",
            "status": "ZERO_THEOREM_NOT_CLOSED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4040_1_envelope",
            "decision": "Carry an absolute c_Z envelope with no cancellation credit.",
            "status": "CZ_ENVELOPE_SELECTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4040_2_progress",
            "decision": "Since c_Z is now envelope-bound rather than structurally vague, move the derivation pressure to c_norm/Newton-G routing while retaining the c_Z envelope.",
            "status": "MOVE_TO_CNORM_WITH_CZ_CARRIED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4040_3_next",
            "decision": "Move to 4041-Y5-R2FR-cnorm-common-mode-into-kappa-obs-or-Gdot-bound.md.",
            "status": "NEXT_TARGET_SELECTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def claim_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4040_0_full_cZ_zero",
            "claim": "full c_Z zero",
            "allowed": False,
            "scope": "hidden/domain/memory current",
            "reason": "kernel tail and selector wall are not zero-proven",
            "public_claim_allowed": False,
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4040_1_cZ_envelope",
            "claim": "absolute c_Z envelope exists",
            "allowed": True,
            "scope": "internal nonclaim residual accounting",
            "reason": "tail/wall amplitude bounds are explicit and no-cancellation",
            "public_claim_allowed": False,
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4040_2_local_GR",
            "claim": "local GR/PPN/R10 pass",
            "allowed": False,
            "scope": "full local-gravity phenomenology",
            "reason": "c_Z envelope, c_norm, c_nonEH, and PPN closure remain open",
            "public_claim_allowed": False,
            "timestamp_utc": ts,
        },
    ]


def next_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NEXT4040_0",
            "next_doc": "4041-Y5-R2FR-cnorm-common-mode-into-kappa-obs-or-Gdot-bound.md",
            "next_script": "scripts/Y5_R2FR_4041_cnorm_common_mode_into_kappa_obs_or_Gdot_bound.py",
            "why": "c_Z is now carried as an absolute envelope; the next live structural blocker is whether c_norm is a harmless common-mode kappa/G calibration or a real Gdot/source-normalization residual.",
            "fallback": "if common-mode routing fails, build Gdot/R10/source-normalization bound rows",
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STATUS4040_0",
            "checkpoint": "4040",
            "canonical_status": "CZ_ENVELOPE_ACTIVE_MOVE_TO_CNORM",
            "strongest_result": "c_Z no longer blocks as an undefined hole; it is an explicit absolute tail/wall envelope with named missing inputs.",
            "still_missing": "kernel support/gap, selector no-wall, operator/range values, arena projections; plus c_norm and c_nonEH branches",
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: List[Dict[str, object]]) -> str:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    total = len(sources)
    return f"""# 4040 - Local Memory Tail Selector Wall Silence Or cZ Envelope

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.
- Source needles found: `{found}/{total}`.

## What Actually Moved

4040 tries the exact zero route for the last `c_Z` pieces and refuses to smuggle it.

The zero theorem would need:

- `P_loc K_mem=0` or disjoint support on the compact stationary collar;
- or a real gap/range bound `||J_Z^tail||_1 <= C_mem exp(-L_collar/ell_mem)||H||_1`;
- a fixed/exact/topological selector with no wall motion or shell mismatch.

The current corpus does not prove those inputs.

## Result

So the full `c_Z=0` claim is not made. Instead the remaining hidden-current effect is an absolute envelope:

`A_Z_remaining <= A_tail + A_wall`.

with

- `A_tail <= C_G(D_Z,M_Z,L_collar)*|c_Z|*C_mem*exp(-L_collar/ell_mem)*||H||_1`;
- `A_wall <= C_G(D_Z,M_Z,L_collar)*|c_Z|*(||jump(D_Z n.grad Z)||_Sigma + ||delta S_wall/delta Z||_Sigma)`.

No cancellation credit is allowed.

## Guardrail

Local memory silence is not global memory silence. The FLRW/cosmology memory branch remains alive.

## Current Verdict

- Current evaluator result: `TAIL_WALL_SILENCE_NOT_PROVED_CZ_ENVELOPE_ACTIVE`.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4040`.
- Remaining live local residuals: `Delta_cZ_envelope`, `c_norm`, `c_nonEH`.

## Next Target

- `4041-Y5-R2FR-cnorm-common-mode-into-kappa-obs-or-Gdot-bound.md`
- `scripts/Y5_R2FR_4041_cnorm_common_mode_into_kappa_obs_or_Gdot_bound.py`
"""


def validation_rows(
    ts: str,
    sources: List[Dict[str, object]],
    theorem: List[Dict[str, object]],
    envelope: List[Dict[str, object]],
    inputs: List[Dict[str, object]],
    remaining: List[Dict[str, object]],
    evaluator: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    claims: List[Dict[str, object]],
    next_target: List[Dict[str, object]],
    compile_ok: bool,
) -> List[Dict[str, object]]:
    def row(check_id: str, passed: bool, detail: str) -> Dict[str, object]:
        return {"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": ts}

    output_paths = [str(path) for path in OUTPUTS.values()] + [str(DOC_PATH), str(SCRIPT_PATH)]
    return [
        row("VAL4040_00_sources_exist", all(item["exists"] for item in sources), "all cited source paths exist"),
        row("VAL4040_01_needles_found", all(item["needle_found"] for item in sources), "all source needles found"),
        row("VAL4040_02_tail_zero_condition", any(item["theorem_id"] == "TW4040_0_tail_zero_sufficient" for item in theorem), "tail zero sufficient theorem present"),
        row("VAL4040_03_tail_bound", any(item["theorem_id"] == "TW4040_1_tail_gap_bound" for item in theorem), "tail gap bound theorem present"),
        row("VAL4040_04_wall_zero", any(item["theorem_id"] == "TW4040_2_selector_wall_zero" for item in theorem), "selector wall theorem present"),
        row("VAL4040_05_global_guard", any(item["theorem_id"] == "TW4040_3_no_global_memory_zero" for item in theorem), "global memory guard present"),
        row("VAL4040_06_not_closed_verdict", any(item["theorem_id"] == "TW4040_4_current_verdict" and "NOT_PROVED" in item["status"] for item in theorem), "not-closed verdict present"),
        row("VAL4040_07_tail_envelope", any(item["envelope_id"] == "ENV4040_0_tail" for item in envelope), "tail envelope present"),
        row("VAL4040_08_wall_envelope", any(item["envelope_id"] == "ENV4040_1_wall" for item in envelope), "wall envelope present"),
        row("VAL4040_09_absolute_envelope", any(item["envelope_id"] == "ENV4040_2_absolute" for item in envelope), "absolute envelope present"),
        row("VAL4040_10_input_kernel", any(item["input_id"] == "IN4040_0_kernel" for item in inputs), "kernel input contract present"),
        row("VAL4040_11_input_selector", any(item["input_id"] == "IN4040_1_selector" for item in inputs), "selector input contract present"),
        row("VAL4040_12_input_operator", any(item["input_id"] == "IN4040_2_operator" for item in inputs), "operator input contract present"),
        row("VAL4040_13_remaining_cZ", any(item["symbol"] == "Delta_cZ_envelope" for item in remaining), "c_Z envelope carried"),
        row("VAL4040_14_remaining_cnorm", any(item["symbol"] == "c_norm" for item in remaining), "c_norm next residual"),
        row("VAL4040_15_remaining_cnonEH", any(item["symbol"] == "c_nonEH" for item in remaining), "c_nonEH remains"),
        row("VAL4040_16_current_verdict", any(item["case_id"] == "CASE4040_0_current" for item in evaluator), "current evaluator present"),
        row("VAL4040_17_no_full_cZ_claim", any(item["claim_id"] == "CLAIM4040_0_full_cZ_zero" and item["allowed"] is False for item in claims), "full c_Z zero not claimed"),
        row("VAL4040_18_envelope_claim_scoped", any(item["claim_id"] == "CLAIM4040_1_cZ_envelope" and item["allowed"] is True and item["public_claim_allowed"] is False for item in claims), "envelope claim scoped internal"),
        row("VAL4040_19_no_public_local_claim", all(item["public_claim_allowed"] is False for item in claims), "no public claims allowed"),
        row("VAL4040_20_move_cnorm", any(item["decision_id"] == "DEC4040_2_progress" for item in decisions), "move to c_norm decision present"),
        row("VAL4040_21_next_decision", any(item["decision_id"] == "DEC4040_3_next" for item in decisions), "4041 next decision present"),
        row("VAL4040_22_next_target", bool(next_target and "4041" in str(next_target[0]["next_doc"])), "next target row present"),
        row("VAL4040_23_doc_written", DOC_PATH.exists(), "checkpoint doc written"),
        row("VAL4040_24_no_formalization_output", all(str(FORMALIZATION) not in path for path in output_paths), "no output targets formalization-workbench"),
        row("VAL4040_25_script_compiles", compile_ok, "script compiles"),
        row("VAL4040_26_private_guard", all(item["valid_for_public_claim"] is False for table in [theorem, envelope, inputs, remaining, decisions] for item in table), "public-claim guard retained"),
    ]


def main() -> None:
    ts = timestamp()
    sources = source_rows(ts)
    theorem = theorem_rows(ts)
    envelope = envelope_rows(ts)
    inputs = input_contract_rows(ts)
    remaining = remaining_rows(ts)
    evaluator = evaluator_rows(ts)
    decisions = decision_rows(ts)
    claims = claim_rows(ts)
    next_target = next_rows(ts)
    status = status_rows(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["tail_wall_theorem"], theorem)
    write_csv(OUTPUTS["cz_envelope"], envelope)
    write_csv(OUTPUTS["input_contract"], inputs)
    write_csv(OUTPUTS["remaining_residuals"], remaining)
    write_csv(OUTPUTS["evaluator"], evaluator)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["status"], status)

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
    except py_compile.PyCompileError:
        compile_ok = False

    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    checks = validation_rows(ts, sources, theorem, envelope, inputs, remaining, evaluator, decisions, claims, next_target, compile_ok)
    write_csv(OUTPUTS["validation"], checks)
    passed = sum(1 for item in checks if item["passed"])
    total = len(checks)
    print(f"4040 validation: {passed}/{total} passed")
    if passed != total:
        for item in checks:
            if not item["passed"]:
                print(f"FAIL {item['check_id']}: {item['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
