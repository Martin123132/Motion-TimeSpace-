from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common_mode_scalar_gate import (  # noqa: E402
    claim_gate_rows,
    common_mode_normal_form_rows,
    decision_rows as gate_decision_rows,
    finite_branch_contract_rows,
    r10_pressure_rows,
    read_csv,
    write_csv,
    zero_route_rows,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = POST / "source-intake" / "local_bounds"

CHECKPOINT = "4466"
CLAIM_ID = "L-308"
MARKER = "PPC4161_COMMON_MODE_SCALAR_DECOUPLING_OR_CR2_ZERO_AGAINST_R10_PRESSURE_4466"
PACKET_MARKER = "PPC4161_PACKET_COMMON_MODE_SCALAR_DECOUPLING_OR_CR2_ZERO_AGAINST_R10_PRESSURE_4466"
DECISION = "COMMON_MODE_SCALAR_NORMAL_FORM_WRITTEN_UNIVERSAL_R2_FAILS_R10_PRESSURE_ZERO_OR_DECOUPLING_REQUIRED_NONCLAIM"
NEXT_TARGET = "4467-Y5-R2FR-parent-action-source-silence-or-refinement-cR2-zero-certificate.md"

FORMAL_PATH = FORMAL / "482-PPC4161-common-mode-scalar-decoupling-or-cR2-zero-against-R10-pressure.md"
DOC_PATH = POST / "4466-Y5-R2FR-common-mode-scalar-decoupling-or-cR2-zero-against-R10-pressure.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4466_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4466_SOURCE_REGISTER.csv"
NORMAL_FORM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4466_COMMON_MODE_NORMAL_FORM.csv"
ZERO_ROUTES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4466_ZERO_ROUTE_AUDIT.csv"
R10_PRESSURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4466_R10_PRESSURE_EVALUATION.csv"
FINITE_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4466_FINITE_BRANCH_CONTRACT.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4466_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4466_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4466_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4466_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4466_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "common_mode_scalar_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4466_common_mode_scalar_decoupling_or_cR2_zero_against_R10_pressure.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_477 = FORMAL / "477-PPC4161-connection-hinge-refinement-owner-or-c2-scalaron-map.md"
FORMAL_480 = FORMAL / "480-PPC4161-first-calibrated-G-residual-score-pack-WEP-R10-PPN-or-source-zero.md"
FORMAL_481 = FORMAL / "481-PPC4161-source-charge-universality-zero-proof-or-WEP-material-vector-runner.md"
NEXT_4465 = SOURCE_DIR / "P8_Y5_R2FR_4465_NEXT_TARGET.csv"
DERIVATION_4465 = SOURCE_DIR / "P8_Y5_R2FR_4465_SOURCE_CHARGE_DERIVATION.csv"
PRESSURE_4464 = SOURCE_DIR / "P8_Y5_R2FR_4464_FIRST_SCORE_PACK.csv"
REFINEMENT_4459 = SOURCE_DIR / "P8_Y5_R2FR_4459_REFINEMENT_LINEARITY_THEOREM.csv"
REFINEMENT_DECISION_4459 = SOURCE_DIR / "P8_Y5_R2FR_4459_DECISION.csv"
REFINEMENT_CONTRACT_4460 = SOURCE_DIR / "P8_Y5_R2FR_4460_PARENT_REFINEMENT_SIGNATURE_CONTRACT.csv"
REFINEMENT_DICHOTOMY_4460 = SOURCE_DIR / "P8_Y5_R2FR_4460_REFINEMENT_DICHOTOMY.csv"
SCALARON_4461 = SOURCE_DIR / "P8_Y5_R2FR_4461_C2_SCALARON_OBSERVABLE_MAP.csv"
R10_REVIEW = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"
R10_LIVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"


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
            "source_id": "SRC4466_00_next4465",
            "ref": NEXT_4465,
            "needle": "common-mode-scalar-decoupling-or-cR2-zero",
            "role": "4465 selected common-mode scalar/source decoupling or cR2 zero.",
        },
        {
            "source_id": "SRC4466_01_formal481",
            "ref": FORMAL_481,
            "needle": "universal common mode",
            "role": "4465 WEP differential/common-mode split.",
        },
        {
            "source_id": "SRC4466_02_deriv4465",
            "ref": DERIVATION_4465,
            "needle": "COMMON_MODE_SURVIVES_WEP",
            "role": "common mode survives WEP and moves to R10/PPN/orbits.",
        },
        {
            "source_id": "SRC4466_03_pressure4464",
            "ref": PRESSURE_4464,
            "needle": "UNIVERSAL_ALPHA_FAILS_REVIEW_CANDIDATE_PRESSURE",
            "role": "R10 smoke pressure on universal R2 scalar.",
        },
        {
            "source_id": "SRC4466_04_formal480",
            "ref": FORMAL_480,
            "needle": "alpha_eff=C_matter^2/3",
            "role": "4464 scalar pressure formula.",
        },
        {
            "source_id": "SRC4466_05_formal477",
            "ref": FORMAL_477,
            "needle": "lambda_bound_um=76.39299809562831",
            "role": "4461 lambda pressure and c2 scalaron map.",
        },
        {
            "source_id": "SRC4466_06_refinement4459",
            "ref": REFINEMENT_DECISION_4459,
            "needle": "S_n(delta)=n Phi(delta/n)",
            "role": "4459 refinement-linearity zero theorem summary.",
        },
        {
            "source_id": "SRC4466_07_contract4460",
            "ref": REFINEMENT_CONTRACT_4460,
            "needle": "RGC4460_4_geometry_owner",
            "role": "4460 parent refinement signature contract.",
        },
        {
            "source_id": "SRC4466_08_dichotomy4460",
            "ref": REFINEMENT_DICHOTOMY_4460,
            "needle": "DICH4460_0_exact_refinement_gauge",
            "role": "4460 exact-refinement vs finite-c2 dichotomy.",
        },
        {
            "source_id": "SRC4466_09_scalaron4461",
            "ref": SCALARON_4461,
            "needle": "lambda_R2",
            "role": "4461 finite c2 scalaron observable map.",
        },
        {
            "source_id": "SRC4466_10_r10_review",
            "ref": R10_REVIEW,
            "needle": "Lee_Adelberger_Cook_Fleischer_Heckel_2020_EotWash_vector_curve",
            "role": "R10 review-candidate curve for nonclaim pressure.",
        },
        {
            "source_id": "SRC4466_11_r10_live",
            "ref": R10_LIVE,
            "needle": "MISSING_DIGITIZED_ALPHA_BOUND",
            "role": "live R10 claim curve remains placeholder.",
        },
        {
            "source_id": "SRC4466_12_gate",
            "ref": GATE_PATH,
            "needle": "def common_mode_normal_form_rows",
            "role": "4466 common-mode scalar gate.",
        },
        {
            "source_id": "SRC4466_13_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4466"',
            "role": "4466 generator script.",
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
            "normal_form_result": "common-mode scalar reduced to S_matter[A(chi)^2 g_obs, theta_j(chi)] plus finite c_R2_eff scalar pole",
            "R10_result": "universal C_matter=1 at current lambda pressure fails review-candidate R10 by alpha/bound ratio about 2.44",
            "zero_result": "local-GR route now needs C_matter=0 source silence or c_R2_eff=0 refinement/hinge zero before public claim",
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
            "common_mode_status": "normal_form_written",
            "universal_R2_status": "fails_review_candidate_R10_pressure",
            "zero_routes_status": "source_silence_or_cR2_zero_required_parent_unsigned",
            "finite_route_status": "blocked_until_live_curve_and_parent_coefficients",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4466_0",
            "target": NEXT_TARGET,
            "objective": "Try to sign the parent action certificate that makes the common scalar source-silent or activates the refinement c_R2 zero selector.",
            "derive_first": "inspect parent action normal form for an explicit absence of A(chi) matter coupling and for quotient/cylindrical refinement ownership",
            "fallback": "if neither zero route signs, keep finite scalar as a bound-only branch requiring live R10 curve plus parent C_matter and c_R2_eff values",
            "risk": "using WEP closure or calibrated G to hide a composition-blind fifth force",
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
        "domain": "local_gr_r10_common_mode_scalar",
        "claim": "The common-mode scalar/local fifth-force branch is now reduced to three honest exits: C_matter=0 source silence, c_R2_eff=0 refinement zero, or a finite alpha(lambda) branch that must pass R10/PPN/orbital bounds.",
        "current_evidence": "4466 source register, common-mode normal form, zero-route audit, R10 pressure evaluation, finite-branch contract, claim gates, decision, status, next target and validation CSV.",
        "status": "private_nonclaim_checkpoint",
        "next_test": NEXT_TARGET,
        "key_risk": "universal R2 scalar may be hidden behind WEP closure despite failing R10 pressure.",
        "sector": "local_gr_newton_r10_scalar_source_coupling",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "composition-blind fifth-force leakage or unsigned c_R2 zero selector",
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
    normal_rows: List[Dict[str, object]],
    zero_rows: List[Dict[str, object]],
    r10_rows: List[Dict[str, object]],
    finite_rows: List[Dict[str, object]],
    ledger: List[Dict[str, object]],
    gates: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    statuses: List[Dict[str, object]],
    next_targets: List[Dict[str, object]],
) -> str:
    return f"""# 482 - PPC4161 Common Mode Scalar Decoupling Or cR2 Zero Against R10 Pressure

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4466 turns the surviving universal scalar/common-mode problem into a closed normal-form fork. After WEP differential closure, the remaining scalar sector can be written as

`S = S_GR[g_obs] + S_chi[g_obs,chi;c_R2_eff] + S_matter[Psi, A(chi)^2 g_obs, theta_j(chi)]`.

That leaves three honest exits. First, source silence: `dS_matter/dchi=0`, equivalently `C_matter=d ln A/dchi=0` and `d ln theta_j/dchi=0`. Second, scalar absence: `c_R2_eff=0` from the refinement/hinge zero selector, so no finite scalar pole exists. Third, finite survival: `alpha_eff=C_matter^2/3` at `lambda_R2=sqrt(6*c_R2_eff)` must pass R10/PPN/orbital bounds with source-backed coefficients.

The pressure is real. Using the existing review-candidate R10 curve only as smoke, universal `C_matter=1` at the current `lambda_R2≈76.39 um` pressure gives `alpha_eff=1/3`, while the nearest review bound is about `0.1365`; the ratio is about `2.44`. So the clean route is not "WEP passed"; it is source decoupling or `c_R2_eff=0`.

## Common-Mode Normal Form

{table(normal_rows)}

## Zero Route Audit

{table(zero_rows)}

## R10 Pressure Evaluation

{table(r10_rows)}

## Finite Branch Contract

{table(finite_rows)}

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
    return body.replace("# 482 - PPC4161", "# 4466 - Y5/R2FR", 1)


def live_numeric_count(rows: List[Dict[str, str]]) -> int:
    count = 0
    for row in rows:
        try:
            float(row.get("lambda_value", ""))
            float(row.get("alpha_bound", ""))
        except (TypeError, ValueError):
            continue
        count += 1
    return count


def validate(
    sources: List[Dict[str, object]],
    normal_rows: List[Dict[str, object]],
    zero_rows: List[Dict[str, object]],
    r10_rows: List[Dict[str, object]],
    finite_rows: List[Dict[str, object]],
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
    normal_ok = any("S_matter[Psi, A(chi)^2 g_obs" in str(row.get("formula")) for row in normal_rows)
    zero_source = any(row.get("route_id") == "ZR4466_0_source_silence" for row in zero_rows)
    zero_cr2 = any(row.get("route_id") == "ZR4466_1_refinement_cR2_zero" for row in zero_rows)
    r10_fail = any(row.get("status") == "UNIVERSAL_CMATTER_FAILS_REVIEW_PRESSURE" for row in r10_rows)
    cmatter_limit = next((row.get("C_matter_abs_limit") for row in r10_rows if row.get("pressure_id") == "R10P4466_0_current_lambda_pressure"), "")
    finite_blocked = any(row.get("current_status") == "MISSING_PARENT_COEFFICIENT_VALUE" for row in finite_rows) and any(row.get("current_status") == "MISSING_PARENT_SOURCE_SILENCE_OR_COUPLING_VALUE" for row in finite_rows)
    no_claims = all(str(row.get("valid_for_claim")).lower() != "true" for row in normal_rows + zero_rows + r10_rows + finite_rows + gates)
    return [
        {"check_id": "VAL4466_0_sources_exist_and_needles_found", "passed": source_ok, "detail": "all cited source paths and needles validate" if source_ok else "missing source path or needle"},
        {"check_id": "VAL4466_1_normal_form_written", "passed": normal_ok, "detail": "S_matter[A(chi)^2 g_obs] normal form present"},
        {"check_id": "VAL4466_2_zero_routes_present", "passed": zero_source and zero_cr2, "detail": "source-silence and c_R2 zero routes present"},
        {"check_id": "VAL4466_3_R10_universal_pressure_fails", "passed": r10_fail, "detail": f"C_matter limit at current pressure = {cmatter_limit}"},
        {"check_id": "VAL4466_4_finite_contract_blocks_claim", "passed": finite_blocked, "detail": "finite branch missing parent c_R2 and C_matter values"},
        {"check_id": "VAL4466_5_claims_blocked", "passed": no_claims, "detail": "no generated row allows public/local-GR claim"},
        {"check_id": "VAL4466_6_csv_parse", "passed": parsed_all, "detail": "all generated CSVs parse" if parsed_all else "; ".join(parse_errors)},
        {"check_id": "VAL4466_7_formal_doc_written", "passed": FORMAL_PATH.exists(), "detail": str(FORMAL_PATH)},
        {"check_id": "VAL4466_8_post_doc_written", "passed": DOC_PATH.exists(), "detail": str(DOC_PATH)},
        {"check_id": "VAL4466_9_claim_register_updated", "passed": any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "detail": CLAIM_ID},
        {"check_id": "VAL4466_10_next_target_selected", "passed": NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "detail": NEXT_TARGET},
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    r10_review = read_csv(R10_REVIEW)
    r10_live = read_csv(R10_LIVE)

    sources = source_rows()
    normal_rows = common_mode_normal_form_rows()
    zero_rows = zero_route_rows()
    r10_rows = r10_pressure_rows(r10_review, live_numeric_rows=live_numeric_count(r10_live))
    finite_rows = finite_branch_contract_rows()
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, normal_rows, zero_rows, r10_rows, finite_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(NORMAL_FORM_CSV, normal_rows)
    write_csv(ZERO_ROUTES_CSV, zero_rows)
    write_csv(R10_PRESSURE_CSV, r10_rows)
    write_csv(FINITE_CONTRACT_CSV, finite_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, normal_rows, zero_rows, r10_rows, finite_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, normal_rows, zero_rows, r10_rows, finite_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4466 Common-Mode Scalar Gate",
        "4466 reduces the post-WEP common-mode scalar to a three-exit normal form: `C_matter=0`, `c_R2_eff=0`, or finite `alpha_eff=C_matter^2/3` that must pass R10/PPN/orbital bounds. The universal metric scalar at the current `lambda_R2` pressure fails the review-candidate R10 smoke check, so the clean local-GR route now needs parent source silence or the refinement/hinge `c_R2` zero selector.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4466 Packet Integration",
        "The private packet now blocks a common-mode fifth force from hiding behind WEP. Differential source charge can be zero while a universal scalar remains; therefore local GR requires either matter-source silence, no scalar pole, or a finite source-backed bound pass.",
    )

    csv_paths = [
        SOURCE_REGISTER,
        NORMAL_FORM_CSV,
        ZERO_ROUTES_CSV,
        R10_PRESSURE_CSV,
        FINITE_CONTRACT_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, normal_rows, zero_rows, r10_rows, finite_rows, gates, csv_paths)
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
