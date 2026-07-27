from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from calibrated_G_residual_score_gate import (  # noqa: E402
    arena_score_status_rows,
    bound_anchor_rows,
    claim_gate_rows,
    decision_rows as gate_decision_rows,
    first_score_pack_rows,
    read_csv,
    residual_zero_theorem_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = POST / "source-intake" / "local_bounds"

CHECKPOINT = "4464"
CLAIM_ID = "L-306"
MARKER = "PPC4161_FIRST_CALIBRATED_G_RESIDUAL_SCORE_PACK_WEP_R10_PPN_OR_SOURCE_ZERO_4464"
PACKET_MARKER = "PPC4161_PACKET_FIRST_CALIBRATED_G_RESIDUAL_SCORE_PACK_WEP_R10_PPN_OR_SOURCE_ZERO_4464"
DECISION = "FIRST_CALIBRATED_G_RESIDUAL_SCORE_PACK_WRITTEN_R2_SCALAR_PRESSURED_SOURCE_ZERO_SELECTED_NONCLAIM"
NEXT_TARGET = "4465-Y5-R2FR-source-charge-universality-zero-proof-or-WEP-material-vector-runner.md"

FORMAL_PATH = FORMAL / "480-PPC4161-first-calibrated-G-residual-score-pack-WEP-R10-PPN-or-source-zero.md"
DOC_PATH = POST / "4464-Y5-R2FR-first-calibrated-G-residual-score-pack-WEP-R10-PPN-or-source-zero.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4464_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4464_SOURCE_REGISTER.csv"
BOUND_ANCHORS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4464_BOUND_ANCHOR_REGISTER.csv"
ZERO_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4464_RESIDUAL_ZERO_THEOREM_ATTEMPT.csv"
SCORE_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4464_FIRST_SCORE_PACK.csv"
ARENA_STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4464_ARENA_SCORE_STATUS.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4464_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4464_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4464_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4464_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4464_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "calibrated_G_residual_score_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4464_first_calibrated_G_residual_score_pack_WEP_R10_PPN_or_source_zero.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_477 = FORMAL / "477-PPC4161-connection-hinge-refinement-owner-or-c2-scalaron-map.md"
FORMAL_478 = FORMAL / "478-PPC4161-universal-source-coupling-and-Newton-G-normalization-or-residual-bound-row.md"
FORMAL_479 = FORMAL / "479-PPC4161-parent-kappa-scale-law-or-calibrated-G-residual-runner.md"
NEXT_4463 = SOURCE_DIR / "P8_Y5_R2FR_4463_NEXT_TARGET.csv"
RUNNER_4463 = SOURCE_DIR / "P8_Y5_R2FR_4463_CALIBRATED_G_RESIDUAL_RUNNER.csv"
LOCAL_BOUND_CLAIMS = LOCAL_BOUNDS / "local_bound_claims.csv"
R10_LIVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
R10_REVIEW = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_specs() -> List[Dict[str, object]]:
    return [
        {
            "source_id": "SRC4464_00_next4463",
            "ref": NEXT_4463,
            "needle": "4464-Y5-R2FR-first-calibrated-G-residual-score-pack-WEP-R10-PPN-or-source-zero.md",
            "role": "4463 selected the calibrated-G residual score pack.",
        },
        {
            "source_id": "SRC4464_01_formal479",
            "ref": FORMAL_479,
            "needle": "local competitiveness does not require numeric G prediction",
            "role": "calibrated-G policy and residual runner handoff.",
        },
        {
            "source_id": "SRC4464_02_runner4463",
            "ref": RUNNER_4463,
            "needle": "CGR4463_3_species_charge_WEP",
            "role": "residual branches staged by 4463.",
        },
        {
            "source_id": "SRC4464_03_source4462",
            "ref": FORMAL_478,
            "needle": "eta_AB ~= (C_A-C_B)",
            "role": "source-coupling WEP response operator.",
        },
        {
            "source_id": "SRC4464_04_scalaron4461",
            "ref": FORMAL_477,
            "needle": "lambda_bound_um=76.39299809562831",
            "role": "current pure-R2 pressure lambda used for R10 smoke pressure.",
        },
        {
            "source_id": "SRC4464_05_local_bounds",
            "ref": LOCAL_BOUND_CLAIMS,
            "needle": "MICROSCOPE_final_TiPt",
            "role": "WEP, clock, PPN, Gdot and symbolic R10 local bound anchors.",
        },
        {
            "source_id": "SRC4464_06_r10_live_placeholder",
            "ref": R10_LIVE,
            "needle": "MISSING_DIGITIZED_ALPHA_BOUND",
            "role": "live claim curve remains blocked/placeholder.",
        },
        {
            "source_id": "SRC4464_07_r10_review_candidate",
            "ref": R10_REVIEW,
            "needle": "Lee_Adelberger_Cook_Fleischer_Heckel_2020_EotWash_vector_curve",
            "role": "review-candidate numeric curve for nonclaim smoke pressure only.",
        },
        {
            "source_id": "SRC4464_08_gate",
            "ref": GATE_PATH,
            "needle": "def first_score_pack_rows",
            "role": "4464 residual score gate.",
        },
        {
            "source_id": "SRC4464_09_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4464"',
            "role": "4464 generator script.",
        },
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        path = Path(spec["ref"])
        needle = str(spec["needle"])
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_kind": "local",
                "source_ref": str(path),
                "local_path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "line_number": line,
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "score_result": "first residual score pack separates clean theorem branch from finite WEP/R10/PPN/Gdot/clock/orbital branches",
            "strongest_pressure": "universal R2 scalar alpha=1/3 is pressured by the review-candidate R10 curve near lambda_R2 pressure",
            "best_next_route": "prove source-charge universality/Delta_C_AB=0 or run a WEP material vector rather than hiding residuals in calibrated G",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "calibrated_G_policy": "allowed_as_GR_parity_calibration",
            "residual_score_pack": "written_nonclaim",
            "R10_scalar_status": "review_candidate_pressure_not_live_claim",
            "selected_next_target": NEXT_TARGET,
            "public_local_GR_claim": False,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4464_0",
            "target": NEXT_TARGET,
            "objective": "Attack the coupling throat directly: prove same-Hilbert/source-label-forgetting gives Delta_C_AB=0, or build the first WEP material vector runner.",
            "derive_first": "derive C_A=C_B from one matter action, one Hilbert source, no source-Hom, source-label-forgetting and worldtube source normalization",
            "fallback": "fill a source-backed material vector for Ti/Pt or nearest MICROSCOPE composition proxy and score the finite product against eta<=2.8e-15",
            "risk": "treating calibrated G as if it hides species/source coupling; relying on R10 candidate curve before live promotion",
            "valid_for_claim": False,
        }
    ]


def update_claims_register() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else [
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
    ]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_residual_scoring",
        "claim": "MTS now has a first calibrated-G residual score pack: WEP/source charge, R10 scalar, PPN, Gdot/clock and orbital source channels are separated from the clean theorem branch.",
        "current_evidence": "4464 source register, bound-anchor register, residual zero-theorem attempt, first score pack, arena status, claim gates, decision, status, next target and validation CSV.",
        "status": "private_nonclaim_checkpoint",
        "next_test": NEXT_TARGET,
        "key_risk": "conditional clean branch may be mistaken for a public local-GR pass; R10 review candidate may be overused before live curve promotion.",
        "sector": "local_gr_newton_wep_r10_ppn_source_coupling",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "fitted-G residual absorption or overclaiming review-candidate R10 pressure",
    }
    rows.append({key: claim_row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def append_section_once(path: Path, marker: str, title: str, body: str) -> None:
    current = text(path)
    if marker in current:
        return
    addition = f"\n\n## {title}\n\nMarker: `{marker}`\n\n{body.strip()}\n"
    write_text(path, current.rstrip() + addition + "\n")


def formal_body(
    sources: List[Dict[str, object]],
    bounds: List[Dict[str, object]],
    zero_rows: List[Dict[str, object]],
    score_rows: List[Dict[str, object]],
    arena_rows: List[Dict[str, object]],
    ledger: List[Dict[str, object]],
    gates: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    statuses: List[Dict[str, object]],
    next_targets: List[Dict[str, object]],
) -> str:
    return f"""# 480 - PPC4161 First Calibrated-G Residual Score Pack WEP R10 PPN Or Source Zero

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4464 converts the calibrated-G local branch into an explicit residual score pack. This is the fair route: MTS does not need to predict the numerical value of Newton's constant today, but it is not allowed to hide species, range, time, frame, connection, scalar, orbital-source or EM leakage inside the calibrated `G` or fitted `GM`.

The useful new pressure is concrete. The clean branch survives as a conditional theorem branch, but the finite pure-R2 scalar branch is no longer vague: using the existing nonclaim review-candidate R10 curve near the current `lambda_R2` pressure, universal `alpha_eff=1/3` is pressured rather than silently safe. That pushes the next derivation toward a real zero/decoupling theorem for `c_R2_eff` or `C_matter`, while the coupling throat points to `Delta_C_AB=0` from source-charge universality.

## Bound Anchor Register

{table(bounds)}

## Residual Zero-Theorem Attempt

{table(zero_rows)}

## First Score Pack

{table(score_rows)}

## Arena Score Status

{table(arena_rows)}

## Decision Ledger

{table(ledger)}

## Claim Gates

{table(gates)}

## Decision

{table(decisions)}

## Status

{table(statuses)}

## Next Target

{table(next_targets)}

## Source Register

{table(sources)}
"""


def post_body(*args: object) -> str:
    body = formal_body(*args)  # type: ignore[arg-type]
    return body.replace("# 480 - PPC4161", "# 4464 - Y5/R2FR", 1)


def validate(
    sources: List[Dict[str, object]],
    bounds: List[Dict[str, object]],
    zero_rows: List[Dict[str, object]],
    score_rows: List[Dict[str, object]],
    gates: List[Dict[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    parsed_all = True
    parse_errors: List[str] = []
    for path in csv_paths:
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover - validation report path
            parsed_all = False
            parse_errors.append(f"{path.name}: {exc}")

    source_ok = all(bool(row["local_path_exists"]) and bool(row["needle_found"]) for row in sources)
    local_anchor_ok = all(
        row.get("source_status") == "SOURCE_BACKED_EMPIRICAL_BOUND"
        and str(row.get("bound_value", "")).strip() not in {"", "MISSING_BOUND", "alpha(lambda)"}
        for row in bounds[:10]
    )
    r10_row = next((row for row in bounds if row.get("anchor_id") == "BA4464_10_R10_review_candidate_at_lambda_R2"), {})
    r10_pressure = next((row for row in score_rows if row.get("score_id") == "SP4464_2_R10_R2_scalar"), {})
    arenas = {row.get("arena") for row in score_rows}
    return [
        {"check_id": "VAL4464_0_sources_exist_and_needles_found", "passed": source_ok, "detail": "all source paths and needles validate" if source_ok else "missing source path or needle"},
        {"check_id": "VAL4464_1_bound_anchors_numeric", "passed": local_anchor_ok, "detail": "WEP, clock, PPN and Gdot anchor rows have numeric bounds and units"},
        {"check_id": "VAL4464_2_R10_review_nonclaim", "passed": r10_row.get("source_status") == "REVIEW_CANDIDATE_NONCLAIM_NOT_LIVE_CURVE" and str(r10_row.get("valid_for_claim")).lower() == "false", "detail": str(r10_row.get("theory_mapping", "missing"))},
        {"check_id": "VAL4464_3_R2_universal_pressure_recorded", "passed": "FAILS" in str(r10_pressure.get("branch_score_status", "")), "detail": str(r10_pressure.get("prediction_formula", "missing"))},
        {"check_id": "VAL4464_4_zero_theorem_attempt_present", "passed": len(zero_rows) >= 8, "detail": "residual zero theorem rows written"},
        {"check_id": "VAL4464_5_score_pack_arenas_present", "passed": {"MICROSCOPE_WEP", "R10_YUKAWA_SHORT_RANGE", "Cassini/planetary_PPN", "LLR_GDOT_and_CLOCKS", "orbital_GM_Newton_limit"}.issubset(arenas), "detail": ",".join(sorted(str(a) for a in arenas))},
        {"check_id": "VAL4464_6_claims_blocked", "passed": all(str(row.get("claim_allowed", "False")).lower() != "true" for row in score_rows + gates), "detail": "no public/local-GR claim allowed"},
        {"check_id": "VAL4464_7_csv_parse", "passed": parsed_all, "detail": "all generated CSVs parse" if parsed_all else "; ".join(parse_errors)},
        {"check_id": "VAL4464_8_formal_doc_written", "passed": FORMAL_PATH.exists(), "detail": str(FORMAL_PATH)},
        {"check_id": "VAL4464_9_post_doc_written", "passed": DOC_PATH.exists(), "detail": str(DOC_PATH)},
        {"check_id": "VAL4464_10_claim_register_updated", "passed": any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "detail": CLAIM_ID},
        {"check_id": "VAL4464_11_next_target_selected", "passed": NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "detail": NEXT_TARGET},
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    local_bounds = read_csv(LOCAL_BOUND_CLAIMS)
    r10_live = read_csv(R10_LIVE)
    r10_review = read_csv(R10_REVIEW)

    sources = source_rows()
    bounds = bound_anchor_rows(local_bounds, r10_review, r10_live)
    zero_rows = residual_zero_theorem_rows()
    score_rows = first_score_pack_rows(bounds)
    arena_rows = arena_score_status_rows(score_rows)
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, bounds, zero_rows, score_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(BOUND_ANCHORS_CSV, bounds)
    write_csv(ZERO_THEOREM_CSV, zero_rows)
    write_csv(SCORE_PACK_CSV, score_rows)
    write_csv(ARENA_STATUS_CSV, arena_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, bounds, zero_rows, score_rows, arena_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, bounds, zero_rows, score_rows, arena_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4464 First Calibrated-G Residual Score Pack",
        "4464 turns calibrated `G` into a residual score pack rather than a hiding place. WEP/source charge, R10 scalar range, PPN gamma/beta/preferred-frame, Gdot/clock and orbital source channels are now separated. The clean branch is conditional; the finite universal R2 scalar is pressured by the review-candidate R10 curve near `lambda_R2 ~ 76 um`, so the best next move is source-charge universality or scalar decoupling/zero.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4464 Packet Integration",
        "The private local packet now has its first score pack: calibrated `G_cal` is allowed only with separate residual controls. The next exact throat is the coupling/source theorem: either `Delta_C_AB=0` follows from same-Hilbert source-label-forgetting, or MICROSCOPE-style WEP rows become the first finite material-vector score.",
    )

    csv_paths = [
        SOURCE_REGISTER,
        BOUND_ANCHORS_CSV,
        ZERO_THEOREM_CSV,
        SCORE_PACK_CSV,
        ARENA_STATUS_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, bounds, zero_rows, score_rows, gates, csv_paths)
    write_csv(VALIDATION_PATH, validations)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validations if str(row.get("passed")).lower() != "true"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Generated {CHECKPOINT}: {FORMAL_PATH}")
    print(f"Validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
