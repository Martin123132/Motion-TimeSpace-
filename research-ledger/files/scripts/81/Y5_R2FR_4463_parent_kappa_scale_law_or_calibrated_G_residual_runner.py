from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from kappa_scale_residual_gate import (  # noqa: E402
    claim_gate_rows,
    decision_rows as gate_decision_rows,
    dimensional_audit_rows,
    read_csv,
    residual_runner_rows,
    scale_law_attempt_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4463"
CLAIM_ID = "L-305"
MARKER = "PPC4161_PARENT_KAPPA_SCALE_LAW_OR_CALIBRATED_G_RESIDUAL_RUNNER_4463"
PACKET_MARKER = "PPC4161_PACKET_PARENT_KAPPA_SCALE_LAW_OR_CALIBRATED_G_RESIDUAL_RUNNER_4463"
DECISION = "NUMERIC_G_SCALE_LAW_NOT_DERIVED_CALIBRATED_G_ALLOWED_RESIDUAL_RUNNER_STAGED_NONCLAIM"
NEXT_TARGET = "4464-Y5-R2FR-first-calibrated-G-residual-score-pack-WEP-R10-PPN-or-source-zero.md"

FORMAL_PATH = FORMAL / "479-PPC4161-parent-kappa-scale-law-or-calibrated-G-residual-runner.md"
DOC_PATH = POST / "4463-Y5-R2FR-parent-kappa-scale-law-or-calibrated-G-residual-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4463_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4463_SOURCE_REGISTER.csv"
SCALE_LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4463_KAPPA_SCALE_LAW_ATTEMPT.csv"
DIMENSIONAL_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4463_DIMENSIONAL_SCALE_AUDIT.csv"
RESIDUAL_RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4463_CALIBRATED_G_RESIDUAL_RUNNER.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4463_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4463_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4463_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4463_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4463_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "kappa_scale_residual_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4463_parent_kappa_scale_law_or_calibrated_G_residual_runner.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4462 = SOURCE_DIR / "P8_Y5_R2FR_4462_NEXT_TARGET.csv"
FORMAL_478 = FORMAL / "478-PPC4161-universal-source-coupling-and-Newton-G-normalization-or-residual-bound-row.md"
FORMAL_181 = FORMAL / "181-PPC4161-kappa-G-normalization-gate.md"
FORMAL_184 = FORMAL / "184-PPC4161-parent-adopted-topological-kappa-sector.md"
FORMAL_194 = FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md"
FORMAL_222 = FORMAL / "222-PPC4161-calibrated-GN-bridge-and-source-charge-caveat.md"
VAR_AUDIT = FORMAL / "04-variable-audit.csv"
DOC_3269 = POST / "3269-Y5-R2FR-fixed-local-constants-superselection-for-DD-zero-or-coefficient-runner-under-AX1090.md"
DOC_3294 = POST / "3294-Y5-R2FR-local-GR-reduction-contract-Hilbert-source-common-G-and-Newton-limit-under-AX1090.md"


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
        {"source_id": "SRC4463_00_next4462", "ref": NEXT_4462, "needle": "4463-Y5-R2FR-parent-kappa-scale-law-or-calibrated-G-residual-runner.md", "role": "4462 selected parent kappa scale law or calibrated-G residual runner."},
        {"source_id": "SRC4463_01_formal478", "ref": FORMAL_478, "needle": "MTS predicts numerical Newton G", "role": "4462 numeric-G gate."},
        {"source_id": "SRC4463_02_kappa181", "ref": FORMAL_181, "needle": "The numerical value of `G_N` is not predicted here", "role": "kappa/G normalization gate."},
        {"source_id": "SRC4463_03_top184", "ref": FORMAL_184, "needle": "d u_kappa = 0", "role": "topological kappa sector derives constancy."},
        {"source_id": "SRC4463_04_g194", "ref": FORMAL_194, "needle": "numeric(G_cal) = empirical calibration unless parent scale law fixes kappa_*", "role": "calibrated G law and numeric caveat."},
        {"source_id": "SRC4463_05_bridge222", "ref": FORMAL_222, "needle": "MTS does not need to numerically predict G_N to reduce to GR/Newton", "role": "fair calibrated-G standard."},
        {"source_id": "SRC4463_06_phiG_audit", "ref": VAR_AUDIT, "needle": "gamma=Phi_G sqrt(c^5/(G hbar))", "role": "Phi_G/gamma route and circularity risk."},
        {"source_id": "SRC4463_07_super3269", "ref": DOC_3269, "needle": "If kappa_eff belongs to a parent global/superselection sector", "role": "constant/superselection analogue."},
        {"source_id": "SRC4463_08_contract3294", "ref": DOC_3294, "needle": "A common constant G_cal is acceptable", "role": "local GR contract allows common calibrated G."},
        {"source_id": "SRC4463_09_gate", "ref": GATE_PATH, "needle": "def scale_law_attempt_rows", "role": "4463 kappa scale/residual gate."},
        {"source_id": "SRC4463_10_generator", "ref": GENERATOR_PATH, "needle": 'CHECKPOINT = "4463"', "role": "4463 generator script."},
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
            "scale_law_result": "topological/flux/induced/cell/PhiG routes do not currently fix numeric kappa_eff without a non-circular dimensionful parent scale",
            "calibrated_G_result": "G_cal remains a universal calibrated constant like GR, allowed for local reduction if drift/source residuals vanish or bound",
            "runner_result": "calibrated-G residual runner staged for delta_kappa, species/source charge, R2 scalar, frame/connection and EM leaks",
            "numeric_G_prediction": False,
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
            "kappa_scale_status": "numeric_scale_owner_missing",
            "G_policy_status": "calibrated_universal_G_allowed_not_prediction",
            "residual_status": "runner_staged_not_score_ready",
            "numeric_G_prediction": False,
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4463_0",
            "target": NEXT_TARGET,
            "objective": "Build the first source-backed calibrated-G residual score pack: WEP/species charge, R10 alpha(lambda), PPN gamma/beta/Gdot, orbital GM and source-zero theorem branches.",
            "derive_first": "try to theorem-zero delta_kappa, Delta_C_AB, C_S, c_D/qbar_geom, DeltaGamma_WEP, alpha_eff and EM side-channel from the same-source parent branch",
            "fallback": "fill only source-backed bounds and keep every placeholder valid_for_claim=false",
            "risk": "turning calibrated G into a hiding place for range/species/time/frame residuals",
            "valid_for_claim": False,
        }
    ]


def update_claims_register() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_kappa_scale",
        "claim": "MTS currently has a calibrated universal-G route but no non-circular parent scale law predicting numerical G.",
        "current_evidence": "4463 tests topological, flux, induced metric, cell/refinement, and Phi_G/gamma routes; all require an unsourced dimensionful parent scale or are circular.",
        "status": "private_nonclaim_checkpoint",
        "next_test": NEXT_TARGET,
        "key_risk": "numeric G may be overclaimed or residual coupling leaks may be hidden in fitted GM.",
        "sector": "local_gr_newton_source_coupling",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "calibration mistaken for prediction",
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
    scale_rows: List[Dict[str, object]],
    dim_rows: List[Dict[str, object]],
    runner_rows: List[Dict[str, object]],
    decision_ledger: List[Dict[str, object]],
    claim_rows: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    statuses: List[Dict[str, object]],
    next_targets: List[Dict[str, object]],
) -> str:
    return f"""# 479 - PPC4161 Parent Kappa Scale Law Or Calibrated-G Residual Runner

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4463 takes the risky question head-on: can MTS predict the numerical value of Newton's constant right now?

Current answer: no, not honestly. The topological `kappa_*` sector is useful because it can lock constancy, but it does not fix the value. A flux-quantized sector could fix a discrete value only if the flux normalization and reference coupling are parent-owned. An induced-metric or physical-cell route could fix the value only if MTS derives a microscopic cutoff, cell scale, or action-density normalization without defining it from `G`. The existing `Phi_G/gamma` formula is not a prediction of `G` unless `Phi_G` and `gamma` are independently derived from non-gravitational parent data.

That is not a disaster. It puts MTS on the same fair footing as GR for the local limit: one universal calibrated `G_cal` is acceptable. The competitive burden is not "magically predict G today"; it is "do not hide residual range, species, time, frame, scalar, connection, or EM leakage inside fitted G/GM." 4463 therefore stages the calibrated-G residual runner as the next empirical pressure point.

## Kappa Scale Law Attempt

{table(scale_rows)}

## Dimensional Scale Audit

{table(dim_rows)}

## Calibrated-G Residual Runner

{table(runner_rows)}

## Decision Ledger

{table(decision_ledger)}

## Claim Gates

{table(claim_rows)}

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
    return formal_body(*args).replace("# 479 - PPC4161", "# 4463 - Y5/R2FR")


def validation_rows(
    sources: List[Dict[str, object]],
    scale_rows: List[Dict[str, object]],
    dim_rows: List[Dict[str, object]],
    runner_rows: List[Dict[str, object]],
    decision_ledger: List[Dict[str, object]],
    claim_rows: List[Dict[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    parsed_ok = True
    malformed = []
    for path in csv_paths:
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover - validation report
            parsed_ok = False
            malformed.append(f"{path.name}:{exc}")
    no_claim_true = all(str(row.get("valid_for_claim")).lower() != "true" for rows in [sources, scale_rows, dim_rows, runner_rows, decision_ledger, claim_rows] for row in rows)
    no_claim_allowed = all(str(row.get("claim_allowed")).lower() != "true" for row in scale_rows + runner_rows + claim_rows)
    scale_text = "\n".join(str(row) for row in scale_rows)
    runner_text = "\n".join(str(row) for row in runner_rows)
    rows = [
        {"check_id": "VAL4463_0_local_sources_exist", "passed": all(bool(row["local_path_exists"]) for row in sources), "detail": "all source paths exist"},
        {"check_id": "VAL4463_1_local_needles_found", "passed": all(bool(row["needle_found"]) for row in sources), "detail": "all source needles found"},
        {"check_id": "VAL4463_2_scale_routes_tested", "passed": len(scale_rows) >= 6 and "PhiG" in scale_text and "dimensionful" in scale_text, "detail": "topological, flux, induced, cell, PhiG and no-go routes present"},
        {"check_id": "VAL4463_3_dimensional_audit_present", "passed": len(dim_rows) >= 5 and any(row.get("current_owner") == "MISSING_NONCIRCULAR_PARENT_SCALE" for row in dim_rows), "detail": "dimensionful scale audit blocks numeric G"},
        {"check_id": "VAL4463_4_numeric_G_refused", "passed": any(row.get("gate_id") == "CG4463_2_numeric_G_prediction" and not bool(row.get("gate_pass")) for row in claim_rows), "detail": "numeric G prediction gate is false"},
        {"check_id": "VAL4463_5_calibrated_G_allowed", "passed": any(row.get("gate_id") == "CG4463_3_calibrated_G_policy" and bool(row.get("gate_pass")) for row in claim_rows), "detail": "calibrated universal G policy is allowed as nonclaim"},
        {"check_id": "VAL4463_6_residual_runner_present", "passed": len(runner_rows) >= 6 and "REFUSE_NUMERIC_G_CLAIM" in runner_text and "eta_AB" in runner_text, "detail": "residual runner rows include numeric-G refusal and WEP branch"},
        {"check_id": "VAL4463_7_claims_blocked", "passed": no_claim_true and no_claim_allowed, "detail": "no generated row allows a public/local-GR claim"},
        {"check_id": "VAL4463_8_csv_parse", "passed": parsed_ok, "detail": "all generated CSVs parse" if parsed_ok else ";".join(malformed)},
        {"check_id": "VAL4463_9_formal_doc_written", "passed": FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "detail": str(FORMAL_PATH)},
        {"check_id": "VAL4463_10_post_doc_written", "passed": DOC_PATH.exists() and MARKER in text(DOC_PATH), "detail": str(DOC_PATH)},
        {"check_id": "VAL4463_11_claims_register_updated", "passed": CLAIM_ID in text(CLAIMS_PATH), "detail": CLAIM_ID},
        {"check_id": "VAL4463_12_next_selected", "passed": NEXT_TARGET in text(NEXT_CSV), "detail": NEXT_TARGET},
        {"check_id": "VAL4463_13_pycache_absent", "passed": not (SCRIPT_DIR / "__pycache__").exists(), "detail": "scripts __pycache__ absent"},
    ]
    rows.append({"check_id": "VAL4463_OVERALL", "passed": all(bool(row["passed"]) for row in rows), "detail": "4463 parent kappa scale-law or calibrated-G residual runner checkpoint"})
    return rows


def main() -> None:
    sources = source_rows()
    scale_rows = scale_law_attempt_rows()
    dim_rows = dimensional_audit_rows()
    runner_rows = residual_runner_rows()
    decision_ledger = gate_decision_rows()
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SCALE_LAW_CSV, scale_rows)
    write_csv(DIMENSIONAL_AUDIT_CSV, dim_rows)
    write_csv(RESIDUAL_RUNNER_CSV, runner_rows)
    write_csv(DECISION_LEDGER_CSV, decision_ledger)
    write_csv(CLAIM_GATES_CSV, claim_rows)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, scale_rows, dim_rows, runner_rows, decision_ledger, claim_rows, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, scale_rows, dim_rows, runner_rows, decision_ledger, claim_rows, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4463 Parent Kappa Scale Law",
        "4463 tests whether MTS currently predicts numerical G. It does not: topological kappa locks constancy, while flux, induced, cell/refinement and Phi_G/gamma routes all need a non-circular dimensionful parent scale. The fair local-GR route is calibrated universal G plus strict residual tests for drift, species, range, frame, scalar, connection and EM leakage.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4463 Packet Integration",
        "The packet now treats numeric G as empirical calibration unless a future parent scale owner is derived. This is not a retreat: the residual runner forbids hiding nonuniversal coupling in G/GM and makes calibrated-G leakage the next test target.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        SCALE_LAW_CSV,
        DIMENSIONAL_AUDIT_CSV,
        RESIDUAL_RUNNER_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validation_rows(sources, scale_rows, dim_rows, runner_rows, decision_ledger, claim_rows, csv_paths)
    write_csv(VALIDATION_PATH, validations)

    failed = [row for row in validations if not bool(row["passed"])]
    if failed:
        raise SystemExit(f"4463 validation failed: {failed}")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
