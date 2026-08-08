from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from source_charge_universality_gate import (  # noqa: E402
    claim_gate_rows,
    decision_rows as gate_decision_rows,
    material_vector_fallback_rows,
    read_csv,
    source_charge_derivation_rows,
    theorem_clause_rows,
    wep_response_bound_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = POST / "source-intake" / "local_bounds"

CHECKPOINT = "4465"
CLAIM_ID = "L-307"
MARKER = "PPC4161_SOURCE_CHARGE_UNIVERSALITY_ZERO_PROOF_OR_WEP_MATERIAL_VECTOR_RUNNER_4465"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_CHARGE_UNIVERSALITY_ZERO_PROOF_OR_WEP_MATERIAL_VECTOR_RUNNER_4465"
DECISION = "SOURCE_CHARGE_DIFFERENTIAL_ZERO_THEOREM_DERIVED_COMMON_MODE_R10_THROAT_SURVIVES_NONCLAIM"
NEXT_TARGET = "4466-Y5-R2FR-common-mode-scalar-decoupling-or-cR2-zero-against-R10-pressure.md"

FORMAL_PATH = FORMAL / "481-PPC4161-source-charge-universality-zero-proof-or-WEP-material-vector-runner.md"
DOC_PATH = POST / "4465-Y5-R2FR-source-charge-universality-zero-proof-or-WEP-material-vector-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4465_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4465_SOURCE_REGISTER.csv"
THEOREM_CLAUSES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4465_THEOREM_CLAUSE_AUDIT.csv"
DERIVATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4465_SOURCE_CHARGE_DERIVATION.csv"
WEP_RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4465_WEP_RESPONSE_BOUND_RUNNER.csv"
MATERIAL_FALLBACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4465_MATERIAL_VECTOR_FALLBACK.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4465_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4465_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4465_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4465_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4465_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "source_charge_universality_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4465_source_charge_universality_zero_proof_or_WEP_material_vector_runner.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_478 = FORMAL / "478-PPC4161-universal-source-coupling-and-Newton-G-normalization-or-residual-bound-row.md"
FORMAL_480 = FORMAL / "480-PPC4161-first-calibrated-G-residual-score-pack-WEP-R10-PPN-or-source-zero.md"
CLAIMS_REGISTER = FORMAL / "02-claims-register.csv"
NEXT_4464 = SOURCE_DIR / "P8_Y5_R2FR_4464_NEXT_TARGET.csv"
SCORE_4464 = SOURCE_DIR / "P8_Y5_R2FR_4464_FIRST_SCORE_PACK.csv"
ZERO_4464 = SOURCE_DIR / "P8_Y5_R2FR_4464_RESIDUAL_ZERO_THEOREM_ATTEMPT.csv"
LOCAL_BOUND_CLAIMS = LOCAL_BOUNDS / "local_bound_claims.csv"
MICROSCOPE_READOUT = LOCAL_BOUNDS / "MICROSCOPE_readout_and_profile_gate_2995_NONCLAIM.csv"
MICROSCOPE_RANGE = LOCAL_BOUNDS / "MICROSCOPE_range_readout_gate_2996_NONCLAIM.csv"
A_SOURCE_RATIO = LOCAL_BOUNDS / "A_source_coefficient_ratio_law_3031_NONCLAIM.csv"
A_SOURCE_EQUALITY = LOCAL_BOUNDS / "A_source_equality_condition_3033_NONCLAIM.csv"


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
            "source_id": "SRC4465_00_next4464",
            "ref": NEXT_4464,
            "needle": "source-charge-universality-zero-proof-or-WEP-material-vector-runner",
            "role": "4464 selected source-charge zero proof or WEP material vector.",
        },
        {
            "source_id": "SRC4465_01_formal480",
            "ref": FORMAL_480,
            "needle": "Attack the coupling throat directly",
            "role": "4464 handoff and score-pack decision.",
        },
        {
            "source_id": "SRC4465_02_score4464",
            "ref": SCORE_4464,
            "needle": "BOUND_OPERATOR_READY_BUT_THEORY_VECTOR_MISSING",
            "role": "WEP source branch is bound-ready but theory-vector missing.",
        },
        {
            "source_id": "SRC4465_03_zero4464",
            "ref": ZERO_4464,
            "needle": "one adopted standard matter action",
            "role": "4464 Delta_C_AB zero-theorem clause.",
        },
        {
            "source_id": "SRC4465_04_source4462",
            "ref": FORMAL_478,
            "needle": "universal same-Hilbert coupling gives C_A=C_B",
            "role": "4462 WEP response operator.",
        },
        {
            "source_id": "SRC4465_05_claims_private_import",
            "ref": CLAIMS_REGISTER,
            "needle": "GR_parity_standard_matter_import_private_branch_adopted",
            "role": "prior private standard-matter import/source-universality branch.",
        },
        {
            "source_id": "SRC4465_06_local_bounds",
            "ref": LOCAL_BOUND_CLAIMS,
            "needle": "eta_WEP_source_charge",
            "role": "MICROSCOPE source-charge bound anchor.",
        },
        {
            "source_id": "SRC4465_07_microscope_readout",
            "ref": MICROSCOPE_READOUT,
            "needle": "OFFICIAL_READOUT_NOT_IMPORTED",
            "role": "finite data route remains blocked without official arrays.",
        },
        {
            "source_id": "SRC4465_08_microscope_range",
            "ref": MICROSCOPE_RANGE,
            "needle": "lambda_WEP=sqrt",
            "role": "finite WEP range/profile route requirements.",
        },
        {
            "source_id": "SRC4465_09_Asource_ratio",
            "ref": A_SOURCE_RATIO,
            "needle": "A_source = C_psiH / C_WH",
            "role": "source coefficient equality/fallback ratio context.",
        },
        {
            "source_id": "SRC4465_10_Asource_equality",
            "ref": A_SOURCE_EQUALITY,
            "needle": "A_source=1 requires",
            "role": "source normalization equality condition.",
        },
        {
            "source_id": "SRC4465_11_gate",
            "ref": GATE_PATH,
            "needle": "def source_charge_derivation_rows",
            "role": "4465 source-charge theorem gate.",
        },
        {
            "source_id": "SRC4465_12_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4465"',
            "role": "4465 generator script.",
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
            "WEP_result": "Delta_C_AB=0 follows exactly if no source-Hom, source-label-forgetting and constant-sector silence are signed",
            "common_mode_result": "C_A=C_B=C_common can pass WEP while leaving R10/PPN/orbital common fifth-force pressure",
            "fallback_result": "finite Ti/Pt WEP material-vector runner is formula-ready but missing source-backed sensitivity vector, parent coefficients and range/profile",
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
            "Delta_C_AB_status": "exact_conditional_zero_theorem_written",
            "WEP_finite_status": "operator_ready_material_vector_missing",
            "common_mode_status": "survives_WEP_selected_for_R10_decoupling",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4465_0",
            "target": NEXT_TARGET,
            "objective": "Attack the common-mode scalar/source coupling left after WEP differential closure: derive C_common=0/C_matter=0, c_R2_eff=0, or a source-backed finite branch that survives R10 pressure.",
            "derive_first": "prove scalar/source decoupling from the matter action or refinement/hinge zero for c_R2_eff before relying on numeric bounds",
            "fallback": "use the review-candidate R10 pressure only as smoke, then promote a live alpha(lambda) curve or fill a finite parent coefficient row",
            "risk": "thinking WEP differential zero is the same as local-GR/R10 safety",
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
        "domain": "local_gr_wep_source_charge",
        "claim": "The WEP differential source-charge throat now has an exact conditional zero theorem: Delta_C_AB vanishes under no-source-Hom, source-label-forgetting and constant-sector silence, while common-mode coupling survives for R10/PPN/orbital tests.",
        "current_evidence": "4465 source register, theorem clause audit, source-charge derivation, WEP response bound runner, material-vector fallback, claim gates, decision, status, next target and validation CSV.",
        "status": "private_nonclaim_checkpoint",
        "next_test": NEXT_TARGET,
        "key_risk": "WEP zero may be overread as local-GR/R10 safety; finite material vector remains unsourced.",
        "sector": "local_gr_newton_wep_source_coupling",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "common-mode scalar leakage or unsourced finite WEP vector",
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
    clauses: List[Dict[str, object]],
    derivations: List[Dict[str, object]],
    wep_rows: List[Dict[str, object]],
    material_rows: List[Dict[str, object]],
    ledger: List[Dict[str, object]],
    gates: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    statuses: List[Dict[str, object]],
    next_targets: List[Dict[str, object]],
) -> str:
    return f"""# 481 - PPC4161 Source Charge Universality Zero Proof Or WEP Material Vector Runner

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4465 makes the coupling throat sharper. For a finite source coordinate `chi`, define the charge per Hilbert/inertial mass by `C_A=d ln M_A/dchi`. A composite body has

`C_A = C_common + sum_j s_Aj b_j`, so `Delta_C_AB = sum_j (s_Aj-s_Bj)b_j`.

That is the actual proof lever. If the parent branch has no source-only Hom, forgets material labels after constructing the Hilbert source, and keeps all dimensionless internal constants silent (`b_j=0`), then `C_A=C_B=C_common` and the MICROSCOPE differential WEP signal is exactly zero. This is a real conditional derivation, not a fitted cancellation.

But it also exposes the next danger. `C_A=C_B` only kills differential WEP. A universal common mode `C_common != 0` can still produce a composition-blind fifth force, which belongs to R10/PPN/orbital pressure rather than MICROSCOPE. So the next derivation target is not another WEP circle; it is common-mode scalar/source decoupling or `c_R2_eff=0`.

## Theorem Clause Audit

{table(clauses)}

## Source-Charge Derivation

{table(derivations)}

## WEP Response Bound Runner

{table(wep_rows)}

## Material Vector Fallback

{table(material_rows)}

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
    return body.replace("# 481 - PPC4161", "# 4465 - Y5/R2FR", 1)


def validate(
    sources: List[Dict[str, object]],
    clauses: List[Dict[str, object]],
    derivations: List[Dict[str, object]],
    wep_rows: List[Dict[str, object]],
    material_rows: List[Dict[str, object]],
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
    zero_derivation = any(row.get("status") == "EXACT_CONDITIONAL_ZERO_THEOREM" for row in derivations)
    differential_law = any(
        "Delta_C_AB" in (str(row.get("equation")) + str(row.get("result")))
        and "sum_j" in (str(row.get("equation")) + str(row.get("result")))
        and "s_Aj-s_Bj" in (str(row.get("equation")) + str(row.get("result")))
        for row in derivations
    )
    common_guard = any(row.get("status") == "COMMON_MODE_SURVIVES_WEP" for row in derivations)
    wep_bound = any(row.get("bound") == "2.8e-15" or str(row.get("bound")).startswith("2.8e-15") for row in wep_rows)
    fallback_blocks = any("MISSING_SOURCE_BACKED_MATERIAL_SENSITIVITY_VECTOR" in str(row.get("current_value")) for row in material_rows)
    no_claims = all(str(row.get("valid_for_claim")).lower() != "true" for row in clauses + derivations + wep_rows + material_rows + gates)
    return [
        {"check_id": "VAL4465_0_sources_exist_and_needles_found", "passed": source_ok, "detail": "all cited source paths and needles validate" if source_ok else "missing source path or needle"},
        {"check_id": "VAL4465_1_differential_law_written", "passed": differential_law, "detail": "Delta_C_AB=sum_j(s_Aj-s_Bj)b_j law present"},
        {"check_id": "VAL4465_2_zero_theorem_written", "passed": zero_derivation, "detail": "source-label-forgetting zero theorem present"},
        {"check_id": "VAL4465_3_common_mode_guard_present", "passed": common_guard, "detail": "WEP-zero/R10-common-mode split present"},
        {"check_id": "VAL4465_4_wep_bound_registered", "passed": wep_bound, "detail": "MICROSCOPE eta source-charge bound registered"},
        {"check_id": "VAL4465_5_fallback_blocks_missing_vector", "passed": fallback_blocks, "detail": "finite material-vector route remains blocked until vector exists"},
        {"check_id": "VAL4465_6_claims_blocked", "passed": no_claims, "detail": "no generated row allows public/local-GR claim"},
        {"check_id": "VAL4465_7_csv_parse", "passed": parsed_all, "detail": "all generated CSVs parse" if parsed_all else "; ".join(parse_errors)},
        {"check_id": "VAL4465_8_formal_doc_written", "passed": FORMAL_PATH.exists(), "detail": str(FORMAL_PATH)},
        {"check_id": "VAL4465_9_post_doc_written", "passed": DOC_PATH.exists(), "detail": str(DOC_PATH)},
        {"check_id": "VAL4465_10_claim_register_updated", "passed": any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "detail": CLAIM_ID},
        {"check_id": "VAL4465_11_next_target_selected", "passed": NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "detail": NEXT_TARGET},
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    local_bounds = read_csv(LOCAL_BOUND_CLAIMS)

    sources = source_rows()
    clauses = theorem_clause_rows()
    derivations = source_charge_derivation_rows()
    wep_rows = wep_response_bound_rows(local_bounds)
    material_rows = material_vector_fallback_rows(local_bounds)
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, clauses, derivations, wep_rows, material_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CLAUSES_CSV, clauses)
    write_csv(DERIVATION_CSV, derivations)
    write_csv(WEP_RUNNER_CSV, wep_rows)
    write_csv(MATERIAL_FALLBACK_CSV, material_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, clauses, derivations, wep_rows, material_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, clauses, derivations, wep_rows, material_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4465 Source-Charge Universality",
        "4465 derives the WEP differential throat in a clean form: `C_A=C_common+sum_j s_Aj b_j`, so `Delta_C_AB=sum_j(s_Aj-s_Bj)b_j`. Under no-source-Hom, source-label-forgetting and constant-sector silence, `Delta_C_AB=0` exactly. This closes the WEP differential branch only conditionally; common-mode scalar/source coupling survives and is pushed to R10/PPN/orbital pressure.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4465 Packet Integration",
        "The local packet now distinguishes differential WEP safety from common-mode fifth-force safety. The private same-Hilbert branch can zero `Delta_C_AB`, but `C_common` must still be decoupled or bounded. Next target: common-mode scalar/source decoupling or `c_R2_eff=0` against the R10 pressure.",
    )

    csv_paths = [
        SOURCE_REGISTER,
        THEOREM_CLAUSES_CSV,
        DERIVATION_CSV,
        WEP_RUNNER_CSV,
        MATERIAL_FALLBACK_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, clauses, derivations, wep_rows, material_rows, gates, csv_paths)
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
