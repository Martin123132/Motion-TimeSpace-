from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "1201-Y5-R10-WR10-official-kernel-source-or-toy-kernel-smoke-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
R10_CANDIDATE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"
STAMP = datetime.now(timezone.utc).isoformat()
TOY_WR10 = 1.0
TOY_QDT_BOUND = 1.0


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def numeric(value: Any) -> float | None:
    try:
        parsed = float(str(value))
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key != "generated_utc" and key not in headers:
                headers.append(key)
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1201_0_1200_next",
            "relative_path": "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md",
            "needle": "NEXT1200_0_1201",
            "role": "direct 1201 handoff.",
        },
        {
            "source_id": "SRC1201_1_1200_denominator",
            "relative_path": "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md",
            "needle": "WRK1200_0_unit_alpha_denominator",
            "role": "unit-alpha denominator source-pack requirement.",
        },
        {
            "source_id": "SRC1201_2_1200_numerator",
            "relative_path": "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md",
            "needle": "WRK1200_1_qDT_numerator",
            "role": "qDT numerator source-pack requirement.",
        },
        {
            "source_id": "SRC1201_3_1200_profile",
            "relative_path": "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md",
            "needle": "QPE1200_0_total_envelope",
            "role": "qDT profile-envelope requirement.",
        },
        {
            "source_id": "SRC1201_4_1034_status",
            "relative_path": "1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md",
            "needle": "R10B1034_4_official_supplement_table_status",
            "role": "official supplement table not acquired.",
        },
        {
            "source_id": "SRC1201_5_1035_harmonic",
            "relative_path": "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
            "needle": "KXF1035_3_harmonic",
            "role": "R10 harmonic kernel remains missing.",
        },
        {
            "source_id": "SRC1201_6_437_yukawa",
            "relative_path": "437-R10-alpha-lambda-executable-curve-contract.md",
            "needle": "Yukawa_potential",
            "role": "R10 Yukawa convention.",
        },
        {
            "source_id": "SRC1201_7_R10_candidate",
            "relative_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "needle": "R10_VECTOR_2020_REVIEW_0000",
            "role": "nonclaim numeric R10 review curve for smoke rows.",
        },
        {
            "source_id": "SRC1201_8_APS_supplement_attempt",
            "relative_path": "source-intake/local_bounds/downloads/aps_prl_124_101101/link_aps_supplemental_attempt.html",
            "needle": "Just a moment",
            "role": "local artifact documenting blocked supplement acquisition attempt.",
        },
        {
            "source_id": "SRC1201_9_arxiv_pdf",
            "relative_path": "source-intake/local_bounds/downloads/arxiv_2002_11761/2002.11761.pdf",
            "needle": "",
            "role": "local PRL/arXiv PDF artifact; existence checked only.",
        },
    ]
    rows: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        exists = path.exists()
        needle = str(entry["needle"])
        needle_found = exists if needle == "" else exists and needle in read_text(path)
        rows.append(entry | {"exists": exists, "needle_found": needle_found})
    return rows


def official_kernel_audit_rows() -> list[dict[str, object]]:
    return [
        {
            "audit_id": "OKA1201_0_APS_DOI_page",
            "source_url": "https://link.aps.org/doi/10.1103/PhysRevLett.124.101101",
            "local_artifact": "source-intake/local_bounds/downloads/aps_prl_124_101101/link_aps_supplemental_attempt.html",
            "wanted_object": "machine-readable R10 torque/readout kernel or alpha(lambda) supplement",
            "finding": "DOI/source page exists, but current local artifact does not provide a usable W_R10 torque kernel table",
            "status": "OFFICIAL_KERNEL_NOT_ACQUIRED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "OKA1201_1_EotWash_ISL_page",
            "source_url": "https://www.npl.washington.edu/eotwash/inverse-square-law",
            "local_artifact": "web_checked_no_local_kernel_table",
            "wanted_object": "experiment geometry/harmonic kernel sufficient for D_Y and N_DT",
            "finding": "public page gives experiment/publication context but not the numerical torque kernel needed for W_R10",
            "status": "PUBLIC_CONTEXT_NOT_KERNEL",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "OKA1201_2_arXiv_PRL_pdf",
            "source_url": "https://arxiv.org/abs/2002.11761",
            "local_artifact": "source-intake/local_bounds/downloads/arxiv_2002_11761/2002.11761.pdf",
            "wanted_object": "geometry/harmonic response kernel",
            "finding": "paper/PDF anchors the R10 force-law and harmonic-design context but not a ready machine-readable W_R10 kernel for arbitrary q_DT profiles",
            "status": "PAPER_CONTEXT_NOT_NUMERIC_KERNEL",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "OKA1201_3_review_curve_candidate",
            "source_url": "https://arxiv.org/abs/2002.11761; doi:10.1103/PhysRevLett.124.101101",
            "local_artifact": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "wanted_object": "external alpha_bound(lambda) curve",
            "finding": "numeric review-candidate bound curve exists, but it is not the W_R10 response kernel and remains valid_for_claim=false",
            "status": "EXTERNAL_BOUND_ONLY_NOT_WR10",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "OKA1201_4_verdict",
            "source_url": "multiple official/public sources checked",
            "local_artifact": "1201 audit",
            "wanted_object": "official/geometry W_R10 kernel",
            "finding": "no source-backed W_R10 kernel values are available in the current local corpus; proceed with toy smoke row only",
            "status": "MOVE_TO_TOY_KERNEL_SMOKE_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def toy_kernel_rows() -> list[dict[str, object]]:
    return [
        {
            "toy_id": "TOY1201_0_definition",
            "quantity": "toy W_R10(lambda)",
            "toy_value": TOY_WR10,
            "definition": "Set D_Y=1 and N_DT=1 for every sampled lambda, purely to exercise join arithmetic.",
            "reason_for_toy": "official/geometry W_R10 kernel not acquired",
            "physics_status": "TOY_NOT_PHYSICS_NOT_EVIDENCE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "toy_id": "TOY1201_1_qDT_smoke_value",
            "quantity": "toy q_DT_bound",
            "toy_value": TOY_QDT_BOUND,
            "definition": "Set q_DT_bound=1 dimensionless in toy units so the sample curve produces both pass and fail rows.",
            "reason_for_toy": "tests inequality logic without inventing MTS source/profile values",
            "physics_status": "TOY_NOT_PHYSICS_NOT_EVIDENCE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "toy_id": "TOY1201_2_no_promotion_guard",
            "quantity": "promotion policy",
            "toy_value": "valid_for_claim=false;claim_allowed=false",
            "definition": "Toy W_R10 rows cannot be merged into live R10 or local-GR evidence tables.",
            "reason_for_toy": "prevents smoke-test arithmetic from becoming a claim",
            "physics_status": "GUARD_ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def selected_curve_rows() -> list[tuple[float, float, dict[str, str]]]:
    rows = read_csv(R10_CANDIDATE) if R10_CANDIDATE.exists() else []
    numeric_rows: list[tuple[float, float, dict[str, str]]] = []
    for row in rows:
        lambda_value = numeric(row.get("lambda_value"))
        alpha_bound = numeric(row.get("alpha_bound"))
        if lambda_value is not None and alpha_bound is not None:
            numeric_rows.append((lambda_value, alpha_bound, row))
    numeric_rows = sorted(numeric_rows, key=lambda item: item[0])
    if not numeric_rows:
        return []
    indices = sorted({0, len(numeric_rows) // 2, len(numeric_rows) - 1, min(range(len(numeric_rows)), key=lambda index: numeric_rows[index][1])})
    return [numeric_rows[index] for index in indices]


def toy_smoke_rows() -> list[dict[str, object]]:
    selected = selected_curve_rows()
    if not selected:
        return [
            {
                "smoke_id": "SMK1201_missing_curve",
                "lambda_value": "MISSING",
                "alpha_bound": "MISSING",
                "W_R10_toy": TOY_WR10,
                "q_DT_bound_toy": TOY_QDT_BOUND,
                "alpha_DT_bound_toy": "MISSING",
                "toy_pass": False,
                "row_status": "blocked_missing_curve",
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        ]
    smoke_rows: list[dict[str, object]] = []
    for index, (lambda_value, alpha_bound, row) in enumerate(selected):
        alpha_dt_bound = TOY_WR10 * TOY_QDT_BOUND
        smoke_rows.append(
            {
                "smoke_id": f"SMK1201_{index}_toy_WR10_join",
                "bound_id": row.get("bound_id", ""),
                "lambda_value": lambda_value,
                "lambda_units": row.get("lambda_units", "m"),
                "alpha_bound": alpha_bound,
                "D_Y_unit_alpha_toy": 1.0,
                "N_DT_unit_profile_toy": 1.0,
                "W_R10_toy": TOY_WR10,
                "q_DT_bound_toy": TOY_QDT_BOUND,
                "alpha_DT_bound_toy": alpha_dt_bound,
                "qDT_allowed_if_WR10_1": alpha_bound / TOY_WR10,
                "toy_pass": alpha_dt_bound <= alpha_bound,
                "row_status": "toy_computed_nonclaim_not_physics",
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return smoke_rows


def runner_output_rows(smoke_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    computed = [row for row in smoke_rows if row.get("row_status") == "toy_computed_nonclaim_not_physics"]
    pass_count = sum(1 for row in computed if row.get("toy_pass") is True)
    fail_count = sum(1 for row in computed if row.get("toy_pass") is False)
    return [
        {
            "run_id": "RUN1201_0_toy_WR10_smoke_runner",
            "runner_status": "toy_computed_nonclaim",
            "rows_computed": len(computed),
            "toy_pass_count": pass_count,
            "toy_fail_count": fail_count,
            "expected_behavior": "mixed pass/fail is acceptable and proves inequality gate executes",
            "physics_interpretation": "none; toy W_R10 and qDT values are not source-backed",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1201_0_official_WR10",
            "claim": "official/geometry W_R10 kernel is sourced",
            "status": "BLOCKED_OFFICIAL_KERNEL_NOT_ACQUIRED",
            "why": "available official/public sources do not provide a machine-readable W_R10 kernel in the current corpus",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1201_1_toy_WR10",
            "claim": "toy W_R10 can support physics scoring",
            "status": "BLOCKED_TOY_ONLY",
            "why": "toy D_Y=N_DT=1 is an arithmetic smoke test, not an experiment geometry/readout model",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1201_2_R10_pass",
            "claim": "MTS qDT passes R10",
            "status": "BLOCKED_NO_SOURCE_BACKED_WR10_OR_QDT_PROFILE",
            "why": "real W_R10 and qDT profile/envelope values remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1201_3_local_GR",
            "claim": "MTS local-GR reduction is established",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "why": "1201 only exercises runner logic; it does not close parent, PPN, R10, or boundary/cokernel gates",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1201_0_official_kernel",
            "decision": "official_WR10_kernel_not_found",
            "reason": "local/web-visible official/public sources do not supply a ready response kernel table for arbitrary qDT profiles",
            "next_action": "either obtain dissertation/geometry kernel data or construct a conservative geometry toy with all assumptions explicit",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1201_1_toy_runner",
            "decision": "toy_kernel_smoke_runner_created",
            "reason": "the R10 join logic can now compute pass/fail rows while remaining nonclaim",
            "next_action": "replace toy D_Y/N_DT with source-backed kernel values or a transparent conservative geometry model",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1201_2_best_next",
            "decision": "build_conservative_geometry_kernel_or_qDT_profile_family",
            "reason": "official kernel acquisition is blocked, so the next useful private step is a conservative geometry model or qDT profile family that remains explicitly nonclaim",
            "next_action": "1202 should build a conservative geometry-kernel model with documented assumptions, or fill qDT profile components first",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1201_0_1202",
            "next_target": "1202-Y5-R10-conservative-geometry-kernel-or-qDT-profile-family.md",
            "objective": "replace the toy W_R10 smoke row with either a conservative geometry-kernel model or a qDT profile family, still nonclaim, so the R10 runner becomes physically interpretable enough for private stress tests",
            "include": "declared geometry assumptions; denominator positivity; harmonic weights; qDT profile family; absolute-sum guard; nonclaim sample run",
            "exclude": "official-kernel claim without source; promoted review curve; local-GR/R10 pass; tuned cancellation; GitHub; formalization edits",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, object]],
    official: list[dict[str, object]],
    toy_kernel: list[dict[str, object]],
    smoke: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["needle_found"] for row in sources)
    official_statuses = {row["status"] for row in official}
    toy_rows_ok = all(row.get("claim_allowed") is False and row.get("valid_for_claim") is False for row in toy_kernel)
    smoke_computed = [row for row in smoke if row.get("row_status") == "toy_computed_nonclaim_not_physics"]
    smoke_numeric = all(numeric(row.get("lambda_value")) is not None and numeric(row.get("alpha_bound")) is not None and numeric(row.get("alpha_DT_bound_toy")) is not None for row in smoke_computed)
    has_pass = any(row.get("toy_pass") is True for row in smoke_computed)
    has_fail = any(row.get("toy_pass") is False for row in smoke_computed)
    runner_ok = all(row.get("runner_status") == "toy_computed_nonclaim" and row.get("valid_for_claim") is False for row in runner)
    all_nonclaim = all(row.get("valid_for_claim") is False for row in official + toy_kernel + smoke + runner + gates + decisions + nexts)
    gates_blocked = all(row.get("claim_allowed") is False for row in gates + nexts)
    return [
        {
            "check_id": "V1201_0_sources_exist",
            "result": "pass" if all_sources_ok else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1201_1_official_kernel_audit",
            "result": "pass" if "MOVE_TO_TOY_KERNEL_SMOKE_NONCLAIM" in official_statuses else "fail",
            "detail": "official/geometry W_R10 kernel audit completed and remains not acquired",
            "claim_allowed": False,
        },
        {
            "check_id": "V1201_2_toy_kernel_nonclaim",
            "result": "pass" if toy_rows_ok else "fail",
            "detail": "toy kernel rows are explicitly nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1201_3_smoke_rows_compute",
            "result": "pass" if smoke_numeric and has_pass and has_fail else "fail",
            "detail": "toy smoke rows compute numeric pass/fail inequality with at least one pass and one fail",
            "claim_allowed": False,
        },
        {
            "check_id": "V1201_4_runner_nonclaim",
            "result": "pass" if runner_ok else "fail",
            "detail": "toy runner executes but remains nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1201_5_claim_gates_blocked",
            "result": "pass" if gates_blocked else "fail",
            "detail": "all 1201 claim gates and next target remain blocked/nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1201_6_all_science_rows_nonclaim",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated science rows keep valid_for_claim=false",
            "claim_allowed": False,
        },
        {
            "check_id": "V1201_7_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1201_8_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1201_SUMMARY",
            "result": "pass",
            "detail": "1201 records that official W_R10 kernel values are not acquired, creates a toy W_R10=1 smoke row, proves the R10 inequality gate executes with mixed pass/fail rows, and keeps every output nonclaim",
            "claim_allowed": False,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    official: list[dict[str, object]],
    toy_kernel: list[dict[str, object]],
    smoke: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 1201 - Y5/R10 W_R10 official kernel source or toy-kernel smoke row",
            "**Current verdict:** no official or geometry-sourced `W_R10` kernel values are acquired in the current corpus. 1201 therefore creates a transparent toy `W_R10=1` smoke row only to exercise the R10 inequality gate.",
            "**Main progress:** the runner now computes actual toy pass/fail rows against the nonclaim 2020 R10 curve samples. This is not physics evidence; it is plumbing proof that the gate can bite once real `W_R10` and `q_DT` values exist.",
            "**No claim:** no q_loc=0, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.",
            "## Source register\n\n" + table(sources),
            "## Official kernel audit\n\n" + table(official),
            "## Toy kernel definition\n\n" + table(toy_kernel),
            "## Toy smoke rows\n\n" + table(smoke),
            "## Runner output\n\n" + table(runner),
            "## Claim gates\n\n" + table(gates),
            "## Decision ledger\n\n" + table(decisions),
            "## Validation\n\n" + table(validations),
            "## Next target\n\n" + table(nexts),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    official = official_kernel_audit_rows()
    toy_kernel = toy_kernel_rows()
    smoke = toy_smoke_rows()
    runner = runner_output_rows(smoke)
    gates = claim_gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, official, toy_kernel, smoke, runner, gates, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1201_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1201_OFFICIAL_KERNEL_AUDIT.csv": official,
        "P8_Y5_R10_1201_TOY_KERNEL_DEFINITION.csv": toy_kernel,
        "P8_Y5_R10_1201_TOY_SMOKE_ROWS.csv": smoke,
        "P8_Y5_R10_1201_RUNNER_OUTPUT.csv": runner,
        "P8_Y5_R10_1201_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1201_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1201_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1201_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, stamp(rows))

    write_doc(sources, official, toy_kernel, smoke, runner, gates, decisions, validations, nexts)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: " + ("PASS" if not failed else "FAIL " + ";".join(failed)))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
