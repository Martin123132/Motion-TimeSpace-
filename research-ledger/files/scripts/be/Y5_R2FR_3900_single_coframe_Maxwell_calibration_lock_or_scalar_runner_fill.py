from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3900"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3900-Y5-R2FR-single-coframe-Maxwell-calibration-lock-or-scalar-runner-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3900_SOURCE_REGISTER.csv",
    "coframe": SRC / "P8_Y5_R2FR_3900_SINGLE_COFRAME_LOCK_ATTEMPT.csv",
    "maxwell": SRC / "P8_Y5_R2FR_3900_MAXWELL_EM_STRESS_CALIBRATION_GATE.csv",
    "runner": SRC / "P8_Y5_R2FR_3900_SCALAR_RUNNER_FILL_ROWS.csv",
    "gate": SRC / "P8_Y5_R2FR_3900_LOCAL_GR_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3900_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3900_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3900_VALIDATION.csv",
}

VISIBLE_ACTION = "S_vis=S_EH[g_obs]+S_Maxwell[A,e_obs,alpha_*]+sum_A S_A[psi_A,e_obs,omega[e_obs],theta_*]"
SINGLE_FRAME = "all visible rods, clocks, photons, EM stress, orbital motion, and source variation use the same e_obs(q(Phi))"
NO_DISFORMAL = "no independent tau-tau, spatial, hidden-frame, or disformal X-dependent coframe slot is allowed beyond e_obs"
MAXWELL_MINIMAL = "S_Maxwell=-1/4 int sqrt(-g_obs) alpha_*^{-1} F_{mu nu}F^{mu nu}; T_EM is included in the same Hilbert source variation"
RUNNER_GAMMA = "|gamma-1| <= |c_space-c_lapse| X_bound <= 2.3e-5, with c_space-c_lapse=0 only on the signed conformal/no-disformal branch"
RUNNER_GDOT = "|Gdot/G| <= |c_G||partial_t X| + |X partial_t c_G| + |calibration_source_drift| <= 9.6e-15 yr^-1"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    return str(path.relative_to(PCW)) if path.is_relative_to(PCW) else str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3900_00_next", SRC / "P8_Y5_R2FR_3899_NEXT_TARGET.csv", "NEXT3899_0", "3899 selected single-coframe/Maxwell target"),
        ("SRC3900_01_conformal", SRC / "P8_Y5_R2FR_3899_CONFORMAL_READOUT_PROOF_ATTEMPT.csv", "CONF3899_2_equal_response", "3899 conformal gamma branch"),
        ("SRC3900_02_bounds", SRC / "P8_Y5_R2FR_3899_SCALAR_GAMMA_GDOT_BOUND_ROWS.csv", "SGB3899_3_Gdot_bound_branch", "3899 scalar bound rows"),
        ("SRC3900_03_matter", SRC / "P8_Y5_R2FR_2674_MATTER_CHANNEL_DESCENT_AUDIT.csv", "CH2674_3_EM_fine_structure", "matter/EM/clock descent audit"),
        ("SRC3900_04_action", SRC / "P8_Y5_R2FR_3890_PARENT_ACTION_GRAMMAR_INSERTION.csv", "S_matter^q", "candidate parent action grammar"),
        ("SRC3900_05_object", SRC / "P8_Y5_R2FR_3889_PARENT_OBJECT_LANGUAGE_NO_DIRECT_SOURCE_THEOREM.csv", "Hom_parent", "object-language no hidden source arrow"),
        ("SRC3900_06_source_current", SRC / "P8_source_current_Ward_universality_CONTRACT.csv", "SC0_single_observed_coframe_input", "same observed coframe source current contract"),
        ("SRC3900_07_no_species", SRC / "P8_no_species_source_charge_CONTRACT.csv", "S0_one_observed_coframe_parent_selected", "one observed coframe/no species source charge contract"),
        ("SRC3900_08_em_qmap", SRC / "P8_EM_actual_q_map_vertical_basis_candidate.csv", "QMAP3517_0_public_geometry", "public geometry/coframe q-map candidate"),
        ("SRC3900_09_alpha_status", SRC / "P8_EM_alpha_level_current_owner_status.csv", "STAT3527_1_no_go", "alpha-level current owner no-go"),
        ("SRC3900_10_alpha_residual", SRC / "P8_EM_current_source_Ward_alpha_source_residual.csv", "CSR3508_1_b_alpha_X", "alpha/current residual coefficient"),
        ("SRC3900_11_poynting", SRC / "P8_mu_extra_over_Geff_Meff_vector.csv", "EMV3501_10_em_poynting_hilbert_dressing", "Poynting/Hilbert EM stress row"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": found,
                "role": role,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def coframe_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "COF3900_0_visible_action",
            "clause": "visible-sector action",
            "statement": VISIBLE_ACTION,
            "result": "candidate branch has one public observed geometry for EH, matter, and Maxwell sectors",
            "status": "PASS_CANDIDATE_BRANCH_FROM_3890",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "COF3900_1_single_frame",
            "clause": "same observed coframe",
            "statement": SINGLE_FRAME,
            "result": "kills matter/source frame split if parent adopts the same-frame contract",
            "status": "CANDIDATE_SAME_FRAME_LOCK_PARENT_UNSIGNED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "COF3900_2_no_hidden_frame",
            "clause": "no hidden matter frame",
            "statement": "Hom_parent(H_hidden,M_source)=0 forbids hidden e_A(X), w_A(X), m_A(X), alpha_A(X) source-only slots",
            "result": "direct hidden frame/source derivative vanishes in the candidate object language",
            "status": "PASS_IF_OBJECT_LANGUAGE_SIGNED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "COF3900_3_no_disformal",
            "clause": "no-disformal/lapse-space equality",
            "statement": NO_DISFORMAL,
            "result": "this is stronger than same-frame descent; it is what would force c_space=c_lapse",
            "status": "OPEN_STRONGER_THAN_CURRENT_GRAMMAR",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "COF3900_4_verdict",
            "clause": "coframe verdict",
            "statement": "same-frame is structurally supported; conformal/no-disformal response remains an explicit next proof obligation",
            "result": "gamma cannot be claimed zero yet, but the missing condition is now precise",
            "status": "PARTIAL_LOCK_NO_GAMMA_CLAIM",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def maxwell_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EM3900_0_minimal_Maxwell",
            "channel": "Maxwell action and stress",
            "statement": MAXWELL_MINIMAL,
            "result": "ordinary EM field energy belongs to the same Hilbert source, not an extra fitted mass channel",
            "status": "PASS_IF_MINIMAL_MAXWELL_SIGNED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EM3900_1_Poynting",
            "channel": "Poynting flux",
            "statement": "stationary closed-surface Poynting flux is included in T_total or zero; radiative/relic flux is retained as explicit leakage",
            "result": "user's Poynting-vector intuition is handled as Hilbert-source dressing or scored residual, not ignored",
            "status": "CONDITIONAL_ZERO_OR_RESIDUAL",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EM3900_2_alpha_vertex",
            "channel": "alpha_EM and F^2 vertex",
            "statement": "no alpha_EM(X)F^2 vertex is needed for minimal Maxwell, but existing alpha-level work says compact U(1) alone does not fix the gauge kinetic coefficient",
            "result": "alpha/clock calibration remains open unless quotient-owned constants are parent-signed",
            "status": "OPEN_ALPHA_CALIBRATION",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EM3900_3_clock",
            "channel": "clock/spectroscopy calibration",
            "statement": "clock ratios descend through e_obs and quotient-owned constants; if alpha/mass ratios run with X, fill c_clock and b_alpha rows",
            "result": "clock/EM stress can support the single-frame route but also supplies the sharp residual if constants run",
            "status": "CLOCK_CALIBRATION_UNSIGNED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EM3900_4_verdict",
            "channel": "EM/source coupling verdict",
            "statement": "minimal same-coframe Maxwell is enough to include ordinary EM stress in the Newton/Hilbert source; it does not by itself prove no-disformal gamma or no alpha drift",
            "result": "EM helps source coupling; gamma/Gdot/clock still need coefficient rows or stronger parent lock",
            "status": "PARTIAL_EM_LOCK_SCALAR_BOUNDS_RETAINED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "fill_id": "RUN3900_0_gamma_zero_candidate",
            "runner_target": "K_gamma",
            "branch": "single_coframe_plus_no_disformal",
            "fill_value_or_formula": "K_gamma=0",
            "required_parent_signature": "COF3900_1 same frame plus COF3900_3 no-disformal/lapse-space equality",
            "row_status": "CANDIDATE_ZERO_NOT_RUNNABLE_FOR_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "fill_id": "RUN3900_1_gamma_bound",
            "runner_target": "K_gamma",
            "branch": "nonconformal scalar",
            "fill_value_or_formula": RUNNER_GAMMA,
            "required_parent_signature": "numeric/source-backed c_space-c_lapse and X_bound",
            "row_status": "RUNNER_FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "fill_id": "RUN3900_2_Gdot_zero_candidate",
            "runner_target": "K_Gdot",
            "branch": "stationary memory plus fixed calibration",
            "fill_value_or_formula": "K_Gdot=0 and calibration_source_drift=0",
            "required_parent_signature": "stationary/Killing collar, no incoming memory, quotient-owned G/clock calibration",
            "row_status": "CANDIDATE_ZERO_NOT_RUNNABLE_FOR_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "fill_id": "RUN3900_3_Gdot_bound",
            "runner_target": "Gdot/G",
            "branch": "nonstationary or drifting calibration",
            "fill_value_or_formula": RUNNER_GDOT,
            "required_parent_signature": "c_G, partial_t X bound, partial_t c_G or zero, calibration drift bound",
            "row_status": "RUNNER_FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "fill_id": "RUN3900_4_alpha_clock_bound",
            "runner_target": "clock/alpha_EM",
            "branch": "nonminimal EM calibration",
            "fill_value_or_formula": "Delta ln alpha_EM or clock ratio <= |b_alpha_X| X_bound + clock gradient terms",
            "required_parent_signature": "b_alpha_X=0 by quotient-owned Maxwell coefficient or numeric spectroscopy/clock bound",
            "row_status": "RUNNER_FORMULA_READY_ALPHA_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"gate_id": "LGG3900_0_same_frame", "gate": "same observed coframe/source frame", "result": "structurally supported in candidate grammar but still parent-unsigned globally", "status": "CANDIDATE_PASS_PARENT_UNSIGNED", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3900_1_no_disformal", "gate": "no-disformal conformal response", "result": "not yet proved by same-frame descent alone", "status": "OPEN_REQUIRED_FOR_GAMMA_ZERO", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3900_2_Maxwell", "gate": "minimal Maxwell stress/source coupling", "result": "ordinary EM stress is Hilbert-source dressed if minimal Maxwell and same coframe are signed", "status": "CANDIDATE_PASS_EM_STRESS", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3900_3_alpha_clock", "gate": "alpha/clock calibration", "result": "gauge kinetic and clock constants remain quotient-ownership/coefficient rows", "status": "OPEN_ALPHA_CLOCK_CALIBRATION", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3900_4_local_GR", "gate": "local-GR/Newton/EM promotion", "result": "no claim until no-disformal, stationary/calibration, and EM constant ownership close or are scored", "status": "BLOCKED_NO_CLAIM_EM_COHERENCE_ADVANCED", "claim_allowed": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3900_0",
            "target_checkpoint": "3901-Y5-R2FR-no-disformal-coframe-response-equation-or-gamma-Gdot-runner-score.md",
            "script": "scripts/Y5_R2FR_3901_no_disformal_coframe_response_equation_or_gamma_Gdot_runner_score.py",
            "objective": "derive the coframe response equation that forbids independent lapse/spatial X coefficients; if not derivable, add gamma/Gdot/alpha-clock rows to the executable suppression runner as physical nonclaim inputs",
            "why_next": "3900 shows same-frame Maxwell/source coupling is structurally plausible, but gamma-zero still hinges on the stronger no-disformal coframe response",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_SINGLE_COFRAME_MAXWELL_PARTIAL_LOCK",
            "claim": "NO_LOCAL_GR_CLAIM",
            "summary": "same-coframe matter/EM/source route strengthened; ordinary EM stress can be Hilbert-source dressed; no-disformal gamma lock and alpha/clock calibration remain open",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    coframe: list[dict[str, Any]],
    maxwell: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    timestamp: str,
) -> None:
    doc = f"""# 3900 - Single-Coframe Maxwell Calibration Lock or Scalar Runner Fill

Generated: `{timestamp}`

## Result

3900 connects the local-GR route to the Maxwell/EM and calibrated-source side.

Candidate visible action:

`{VISIBLE_ACTION}`

Same-frame rule:

`{SINGLE_FRAME}`

Maxwell stress rule:

`{MAXWELL_MINIMAL}`

What improves: ordinary EM stress/Poynting energy can live inside the same Hilbert source, so it is not an extra arbitrary mass channel. What does not close yet: same-frame descent is weaker than the no-disformal condition needed for gamma zero, and compact U(1)/Maxwell alone does not prove the fine-structure coefficient cannot run.

## Single Coframe Lock Attempt

{markdown_table(coframe, ["row_id", "clause", "statement", "result", "status"])}

## Maxwell/EM Stress Calibration Gate

{markdown_table(maxwell, ["row_id", "channel", "statement", "result", "status"])}

## Scalar Runner Fill Rows

{markdown_table(runner, ["fill_id", "runner_target", "branch", "fill_value_or_formula", "required_parent_signature", "row_status"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "result", "status", "claim_allowed"])}

## Source Register

Resolved `{sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is genuine forward motion toward the full goal: EM stress and source coupling are now tied into the same-coframe Hilbert-source route. But gamma-zero still needs the stronger no-disformal coframe-response equation, and clock/alpha calibration still needs either quotient ownership or a bound.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3900 SINGLE COFRAME MAXWELL CALIBRATION -->
## 3900 Single-Coframe Maxwell Calibration Lock

Timestamp: `{timestamp}`

Result: `PASS_SINGLE_COFRAME_MAXWELL_PARTIAL_LOCK`.

Candidate visible action:
`{VISIBLE_ACTION}`

Same-frame rule:
`{SINGLE_FRAME}`

No-disformal requirement:
`{NO_DISFORMAL}`

Maxwell stress rule:
`{MAXWELL_MINIMAL}`

Decision: no local-GR claim. Same-frame Maxwell/source coupling is strengthened, but gamma-zero needs a stronger no-disformal coframe-response proof and EM/clock constants still need quotient ownership or bounds.

Next gate: `3901`, no-disformal coframe response equation or gamma/Gdot runner score.
<!-- END 3900 SINGLE COFRAME MAXWELL CALIBRATION -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3900 SINGLE COFRAME MAXWELL CALIBRATION -->"
    end = "<!-- END 3900 SINGLE COFRAME MAXWELL CALIBRATION -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    coframe: list[dict[str, Any]],
    maxwell: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = [row for row in sources if row["exists"] and row["needle_found"]]
    checks.append(("VAL3900_0_sources", "all source paths and needles resolve", len(resolved) == len(sources), f"{len(resolved)}/{len(sources)} sources resolved"))
    checks.append(("VAL3900_1_visible_action", "visible action row exists", any(row["row_id"] == "COF3900_0_visible_action" and "S_Maxwell" in str(row["statement"]) for row in coframe), "COF3900_0"))
    checks.append(("VAL3900_2_same_frame", "same-frame row exists", any(row["row_id"] == "COF3900_1_single_frame" and "CANDIDATE" in str(row["status"]) for row in coframe), "COF3900_1"))
    checks.append(("VAL3900_3_no_disformal_open", "no-disformal stronger condition is retained", any(row["row_id"] == "COF3900_3_no_disformal" and "OPEN" in str(row["status"]) for row in coframe), "COF3900_3"))
    checks.append(("VAL3900_4_Maxwell", "minimal Maxwell stress row exists", any(row["row_id"] == "EM3900_0_minimal_Maxwell" and "Hilbert source" in str(row["result"]) for row in maxwell), "EM3900_0"))
    checks.append(("VAL3900_5_alpha_open", "alpha/clock calibration remains open", any(row["row_id"] == "EM3900_2_alpha_vertex" and "OPEN" in str(row["status"]) for row in maxwell), "EM3900_2"))
    checks.append(("VAL3900_6_runner_rows", "gamma/Gdot/alpha runner rows exist", {"RUN3900_1_gamma_bound", "RUN3900_3_Gdot_bound", "RUN3900_4_alpha_clock_bound"}.issubset({str(row["fill_id"]) for row in runner}), f"{len(runner)} rows"))
    checks.append(("VAL3900_7_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3900_4_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3900_4"))
    checks.append(("VAL3900_8_all_nonclaim", "all generated rows are nonclaim", all(str(row.get("valid_for_claim", row.get("claim_allowed", False))) == "False" for collection in [coframe, maxwell, runner, gate] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3900_9_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "EM stress and source coupling" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3900_10_spine", "spine updated with 3900 block", SPINE_PATH.exists() and "BEGIN 3900 SINGLE COFRAME MAXWELL CALIBRATION" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3900_11_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3900*")
            if path.is_file() and ("3900-Y5" in path.name or "P8_Y5_R2FR_3900" in path.name or "P8_Y5_BRR545_3900" in path.name)
        ]
    checks.append(("VAL3900_12_formalization_untouched", "no generated 3900 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3900_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3900_14_next_target", "next target attacks no-disformal response", any("no-disformal-coframe-response" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3901 no-disformal"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    coframe = coframe_rows(timestamp)
    maxwell = maxwell_rows(timestamp)
    runner = runner_rows(timestamp)
    gate = gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["coframe"], coframe)
    write_csv(OUTPUTS["maxwell"], maxwell)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, coframe, maxwell, runner, gate, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, coframe, maxwell, runner, gate, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_SINGLE_COFRAME_MAXWELL_PARTIAL_LOCK")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
