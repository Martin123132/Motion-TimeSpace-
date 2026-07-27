from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3313-Y5-R2FR-upgraded-WEP-matrix-with-material-confidence-rows-under-AX1090.md"

SRC_3312_DOC = ROOT / "3312-Y5-R2FR-exact-WEP-material-confidence-ledger-or-parent-Ai-proof-under-AX1090.md"
SRC_3312_MATERIALS = OUT / "P8_Y5_R2FR_3312_EXACT_WEP_MATERIAL_LEDGER.csv"
SRC_3312_DELTAS = OUT / "P8_Y5_R2FR_3312_UPGRADED_PAIR_DELTAS.csv"
SRC_3312_CONFIDENCE = OUT / "P8_Y5_R2FR_3312_CONFIDENCE_LEDGER.csv"
SRC_3312_BOUND_UPDATE = OUT / "P8_Y5_R2FR_3312_BOUND_INPUT_UPDATE.csv"
SRC_3312_NEXT = OUT / "P8_Y5_R2FR_3312_NEXT_TARGET.csv"
SRC_3312_VALIDATION = OUT / "P8_Y5_BRR545_3312_VALIDATION.csv"
SRC_3310_ENVELOPE = OUT / "P8_Y5_R2FR_3310_WEP_KLAMBDA_ENVELOPE.csv"
SRC_3311_FACTOR = OUT / "P8_Y5_R2FR_3311_ALPHA_XI_FACTOR_LAW.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3313_SOURCE_REGISTER.csv",
    "matrix": OUT / "P8_Y5_R2FR_3313_UPGRADED_WEP_LINEAR_MATRIX.csv",
    "summary": OUT / "P8_Y5_R2FR_3313_UPGRADED_WEP_SUMMARY.csv",
    "blockers": OUT / "P8_Y5_R2FR_3313_FINAL_CLAIM_BLOCKERS.csv",
    "runner": OUT / "P8_Y5_R2FR_3313_UPGRADED_WEP_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3313_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3313_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3313_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3313_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
CHARGE_KEYS = ["Delta_q_B", "Delta_q_p", "Delta_q_n", "Delta_q_C", "Delta_q_D"]


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 820) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def evidence_hits(path: Path, needles: list[str], limit: int = 5) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    for line_number, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered_needles):
            hits.append(f"L{line_number}:{compact(line, 420)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    snapshot: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            stat = item.stat()
            snapshot[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3312_DOC, "3312 upgraded input handoff", ["PtRh10", "TA6V"]),
        (SRC_3312_MATERIALS, "3312 material ledger", ["MICROSCOPE_PtRh10", "MICROSCOPE_TA6V"]),
        (SRC_3312_DELTAS, "3312 upgraded pair deltas", ["PAIR3312_0_MICROSCOPE", "Delta_q_C"]),
        (SRC_3312_CONFIDENCE, "3312 confidence rows", ["two_sided_95_proxy"]),
        (SRC_3312_BOUND_UPDATE, "3312 bound input updates", ["UPGRADED_INPUT_NONCLAIM"]),
        (SRC_3312_NEXT, "3312 next target", ["upgraded-WEP-matrix"]),
        (SRC_3312_VALIDATION, "3312 validation", ["VAL3312_13_overall", "true"]),
        (SRC_3310_ENVELOPE, "3310 lambda envelope", ["F_lambda"]),
        (SRC_3311_FACTOR, "3311 A_i factor law", ["AXF3311_0_scalar", "AXF3311_1_spin2"]),
    ]
    rows: list[dict[str, Any]] = []
    for index, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3313_{index}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def confidence_lookup() -> dict[str, dict[str, str]]:
    return {row["anchor_id"]: row for row in read_csv(SRC_3312_CONFIDENCE)}


def delta_lookup() -> dict[str, dict[str, str]]:
    return {row["anchor_id"]: row for row in read_csv(SRC_3312_DELTAS)}


def mode_source_factor(mode: str) -> str:
    return "A_0" if mode == "scalar" else "A_2"


def mode_coeff_prefix(mode: str) -> str:
    return "s_0" if mode == "scalar" else "s_2"


def delta_norm(delta: dict[str, str]) -> float:
    return math.sqrt(sum(float(delta[key]) ** 2 for key in CHARGE_KEYS))


def upgraded_matrix_rows() -> list[dict[str, Any]]:
    confidence = confidence_lookup()
    deltas = delta_lookup()
    rows: list[dict[str, Any]] = []
    for env in read_csv(SRC_3310_ENVELOPE):
        anchor_id = env["anchor_id"]
        delta = deltas[anchor_id]
        conf = confidence[anchor_id]
        source_factor = mode_source_factor(env["mode"])
        coeff_prefix = mode_coeff_prefix(env["mode"])
        f_lambda = float(env["F_lambda"])
        eta95 = float(conf["two_sided_95_proxy"])
        bound = eta95 / f_lambda if f_lambda > 0 else math.inf
        bound_text = f"{bound:.12g}" if math.isfinite(bound) else "INF_SUPPRESSED"
        linear_form = (
            f"{coeff_prefix}B*{delta['Delta_q_B']} + "
            f"{coeff_prefix}p*{delta['Delta_q_p']} + "
            f"{coeff_prefix}n*{delta['Delta_q_n']} + "
            f"{coeff_prefix}C*{delta['Delta_q_C']} + "
            f"{coeff_prefix}D*{delta['Delta_q_D']}"
        )
        rows.append(
            {
                "matrix_id": f"UMAT3313_{env['envelope_id']}",
                "constraint_id": env["constraint_id"],
                "mode": env["mode"],
                "anchor_id": anchor_id,
                "lambda_m": env["lambda_m"],
                "F_lambda": env["F_lambda"],
                "source_factor": source_factor,
                "pair_id": delta["pair_id"],
                "Delta_q_B": delta["Delta_q_B"],
                "Delta_q_p": delta["Delta_q_p"],
                "Delta_q_n": delta["Delta_q_n"],
                "Delta_q_C": delta["Delta_q_C"],
                "Delta_q_D": delta["Delta_q_D"],
                "Delta_q_norm_upgraded": f"{delta_norm(delta):.12g}",
                "Delta_B_over_mu": delta["Delta_B_over_mu"],
                "eta95_proxy": conf["two_sided_95_proxy"],
                "linear_form_numeric_delta": linear_form,
                "bound_on_abs_A_times_sdotq_95_proxy": bound_text,
                "constraint_template": f"|{source_factor} * ({coeff_prefix} dot Delta_q_upgraded)| <= eta95_proxy/F_lambda",
                "why_nonclaim": "A_i, exact assay/covariance, source charge, and parent factor proof remain unresolved",
                "valid_for_claim": "false",
            }
        )
    return rows


def summary_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    matrix = upgraded_matrix_rows()
    constraints = sorted(set(row["constraint_id"] for row in matrix))
    for constraint_id in constraints:
        constraint_rows = [row for row in matrix if row["constraint_id"] == constraint_id]
        near_long = [row for row in constraint_rows if float(row["F_lambda"]) >= 0.9]
        best_row = min(
            (row for row in constraint_rows if row["bound_on_abs_A_times_sdotq_95_proxy"] != "INF_SUPPRESSED"),
            key=lambda row: float(row["bound_on_abs_A_times_sdotq_95_proxy"]),
        )
        rows.append(
            {
                "summary_id": f"USUM3313_{constraint_id}",
                "constraint_id": constraint_id,
                "mode": best_row["mode"],
                "anchor_id": best_row["anchor_id"],
                "pair_id": best_row["pair_id"],
                "best_lambda_in_grid_m": best_row["lambda_m"],
                "best_bound_on_abs_A_times_sdotq_95_proxy": best_row["bound_on_abs_A_times_sdotq_95_proxy"],
                "first_lambda_F_ge_0p9_m": near_long[0]["lambda_m"] if near_long else "OUTSIDE_GRID",
                "Delta_q_norm_upgraded": best_row["Delta_q_norm_upgraded"],
                "interpretation": "summary is still on A_i times source-coefficient projection, not on a final MTS parameter",
                "valid_for_claim": "false",
            }
        )
    return rows


def final_blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "FBLK3313_0_parent_Ai",
            "object": "A_0, A_2",
            "status": "NOT_PARENT_DERIVED",
            "why_blocks_claim": "matrix bounds A_i*s_i combinations, not s_i or local-GR safety alone",
            "valid_for_claim": "false",
        },
        {
            "blocker_id": "FBLK3313_1_exact_assay",
            "object": "alloy/isotope/purity and binding model",
            "status": "PARTIAL_SOURCE_BACKED_CATEGORY_ONLY",
            "why_blocks_claim": "material charge deltas are upgraded but not exact experimental charges",
            "valid_for_claim": "false",
        },
        {
            "blocker_id": "FBLK3313_2_covariance",
            "object": "full covariance/systematic confidence treatment",
            "status": "PROXY_95_ONLY",
            "why_blocks_claim": "eta95_proxy is not a final experiment likelihood",
            "valid_for_claim": "false",
        },
        {
            "blocker_id": "FBLK3313_3_cancellation",
            "object": "scalar/spin2 cancellation rule",
            "status": "NOT_DERIVED",
            "why_blocks_claim": "scalar and spin2 rows must stay separate unless parent derives shared/canceling structure",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    matrix = upgraded_matrix_rows()
    summaries = summary_rows()
    return [
        {
            "runner_id": "RUN3313_0_matrix_complete",
            "test": "upgraded matrix covers all lambda-envelope rows",
            "result": "PASS_NONCLAIM" if len(matrix) == len(read_csv(SRC_3310_ENVELOPE)) else "FAIL",
            "detail": f"rows={len(matrix)}",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3313_1_summary_complete",
            "test": "summary covers all four scalar/spin2 anchor constraints",
            "result": "PASS_NONCLAIM" if len(summaries) == 4 else "FAIL",
            "detail": ";".join(row["constraint_id"] for row in summaries),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3313_2_claim_permission",
            "test": "upgraded WEP matrix claim-ready",
            "result": "REFUSE_CLAIM_PARENT_Ai_ASSAY_COVARIANCE_CANCELLATION_MISSING",
            "detail": ";".join(row["object"] for row in final_blocker_rows()),
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3313_0_WEP_matrix_claim",
            "claim": "upgraded WEP matrix bounds MTS source coefficients for a local-GR claim",
            "requirements": "parent A_i, exact assays, covariance/confidence, lambda/range policy, and no cancellation loophole",
            "current_evidence": "upgraded nonclaim matrix only",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3313_1_parent_Ai_route",
            "claim": "source factor route closed by parent proof",
            "requirements": "derive A_0/A_2 from parent mode/source projectors",
            "current_evidence": "not derived",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3313_2_empirical_route",
            "claim": "source factor route closed empirically by WEP matrix",
            "requirements": "final claim-ready WEP likelihood and exact materials",
            "current_evidence": "proxy likelihood/material rows only",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3313_0",
            "question": "Did 3313 produce a better WEP runner?",
            "answer": "yes, nonclaim",
            "reason": "the matrix now uses upgraded material deltas and proxy 95 confidence rows over the lambda grid",
            "next_action": "decide whether to pursue parent A_i derivation or exact WEP likelihood/material assay acquisition",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3313_1",
            "question": "Can it close local-GR source coupling?",
            "answer": "not yet",
            "reason": "it bounds A_i*s_i projections only; parent A_i, exact assay, covariance, and cancellation policy remain open",
            "next_action": "rank blockers and attack parent A_i first if derivation is preferred",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3313_0_3314",
            "target_doc": "3314-Y5-R2FR-parent-Ai-derivation-or-final-WEP-likelihood-blocker-ranking-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3314_parent_Ai_derivation_or_final_WEP_likelihood_blocker_ranking.py",
            "objective": "rank the remaining source-coupling blockers and attempt parent A_i derivation before spending more effort on exact WEP likelihood/material assay extraction",
            "guardrails": "do not mistake an empirical A_i*s_i bound for a derivation of universal source coupling; keep scalar and spin2 separate",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_paths = [Path(row["path"]) for row in source_rows]
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    matrix = upgraded_matrix_rows()
    summaries = summary_rows()
    blockers = final_blocker_rows()
    runners = runner_rows()
    gates = promotion_gate_rows()
    next_rows = next_target_rows()

    checks = [
        (
            "VAL3313_0_sources_exist",
            "all cited source paths exist",
            all(path.exists() for path in source_paths),
            "",
        ),
        (
            "VAL3313_1_sources_parse",
            "all cited source paths parse",
            all(parse_ok(path) for path in source_paths),
            "",
        ),
        (
            "VAL3313_2_outputs_parse",
            "all 3313 non-validation output CSVs parse",
            all(csv_parse_ok(path) for path in output_paths),
            "",
        ),
        (
            "VAL3313_3_matrix_complete",
            "upgraded matrix covers every lambda envelope row",
            len(matrix) == len(read_csv(SRC_3310_ENVELOPE)),
            f"rows={len(matrix)}",
        ),
        (
            "VAL3313_4_matrix_uses_upgraded_inputs",
            "matrix rows include upgraded delta and eta95 fields",
            all("Delta_q_norm_upgraded" in row and "eta95_proxy" in row for row in matrix),
            "",
        ),
        (
            "VAL3313_5_summary_complete",
            "summary covers four scalar/spin2 anchor constraints",
            len(summaries) == 4,
            "",
        ),
        (
            "VAL3313_6_blockers_complete",
            "final blockers include parent A_i, exact assay, covariance, and cancellation",
            any("parent_Ai" in row["blocker_id"] and "A_0" in row["object"] and "A_2" in row["object"] for row in blockers)
            and all(any(token in row["object"] or token in row["blocker_id"] for row in blockers) for token in ["assay", "covariance", "cancellation"]),
            "",
        ),
        (
            "VAL3313_7_runner_refuses_claim",
            "runner refuses claim with blockers active",
            any(row["result"] == "REFUSE_CLAIM_PARENT_Ai_ASSAY_COVARIANCE_CANCELLATION_MISSING" for row in runners),
            "",
        ),
        (
            "VAL3313_8_claim_gates_false",
            "all promotion gates remain false",
            all(row["passed"] == "false" and row["valid_for_claim"] == "false" for row in gates),
            "",
        ),
        (
            "VAL3313_9_next_target_parent_Ai",
            "next target ranks blockers and attempts parent Ai derivation",
            "parent-Ai-derivation" in next_rows[0]["target_doc"],
            "",
        ),
    ]

    formalization_after = snapshot_tree(FW)
    formalization_changed = changed_count(formalization_before, formalization_after)
    checks.append(
        (
            "VAL3313_10_formalization_untouched",
            "formalization-workbench modified-file count remains zero by this script",
            formalization_changed == 0,
            f"formalization_changed_count={formalization_changed}",
        )
    )

    overall = all(passed for _, _, passed, _ in checks)
    checks.append(
        (
            "VAL3313_11_overall",
            "3313 validation overall",
            overall,
            "all required checks passed" if overall else "one or more checks failed",
        )
    )

    return [
        {
            "check_id": check_id,
            "check": check,
            "passed": bool_str(passed),
            "detail": detail,
        }
        for check_id, check, passed, detail in checks
    ]


def render_doc() -> str:
    source_table = "\n".join(
        f"- `{row['source_id']}`: `{row['path']}` — exists={row['exists']}; role={row['role']}"
        for row in source_register_rows()
    )
    summary_table = "\n".join(
        f"- `{row['constraint_id']}`: best proxy bound `{row['best_bound_on_abs_A_times_sdotq_95_proxy']}` at lambda={row['best_lambda_in_grid_m']} m; pair={row['pair_id']}."
        for row in summary_rows()
    )
    blocker_table = "\n".join(
        f"- `{row['blocker_id']}` `{row['object']}`: {row['why_blocks_claim']}."
        for row in final_blocker_rows()
    )
    runner_table = "\n".join(
        f"- `{row['runner_id']}`: `{row['result']}` — {row['detail']}"
        for row in runner_rows()
    )
    gate_table = "\n".join(
        f"- `{row['gate_id']}`: passed={row['passed']}; claim={row['claim']}"
        for row in promotion_gate_rows()
    )
    decision_table = "\n".join(
        f"- `{row['decision_id']}`: {row['answer']} — {row['reason']}"
        for row in decision_rows()
    )
    next_row = next_target_rows()[0]

    return f"""# 3313 - Upgraded WEP matrix with material-confidence rows under AX1090

Run UTC: `{RUN_UTC}`

## Verdict

The WEP matrix has been rebuilt using the upgraded material deltas and confidence rows from `3312`.

Every scalar/spin2, MICROSCOPE/Eot-Wash, lambda-grid row now has:

- upgraded `Delta_q` material contrasts;
- a proxy `eta95` row;
- explicit `A_i`;
- explicit `F(lambda)`.

The result is still nonclaim. It bounds `A_i * (s_i dot Delta_q)` only. It does not by itself prove universal source coupling or local GR.

## Source Register

{source_table}

## Summary

{summary_table}

## Final Claim Blockers

{blocker_table}

## Runner

{runner_table}

## Promotion Gates

{gate_table}

## Decision

{decision_table}

## Next Target

- `{next_row['target_doc']}`
- `{next_row['target_script']}`
- Objective: {next_row['objective']}
"""


def main() -> None:
    formalization_before = snapshot_tree(FW)

    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["matrix"], upgraded_matrix_rows())
    write_csv(OUTPUTS["summary"], summary_rows())
    write_csv(OUTPUTS["blockers"], final_blocker_rows())
    write_csv(OUTPUTS["runner"], runner_rows())
    write_csv(OUTPUTS["promotion"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())

    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))

    if PYCACHE.exists():
        for child in PYCACHE.rglob("*"):
            if child.is_file():
                child.unlink()
        for child in sorted(PYCACHE.rglob("*"), reverse=True):
            if child.is_dir():
                child.rmdir()
        PYCACHE.rmdir()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
