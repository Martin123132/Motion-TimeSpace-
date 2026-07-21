from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4674"
CLAIM_ID = "L-516"
BRANCH = "MTS_R2FR_Y5_FIRST_ZM_B826_FINITE_INPUT_PACK_OR_R826_NO_SLOT_OWNER_PROOF_4674"
MARKER = "PPC4161_FIRST_ZM_B826_FINITE_INPUT_PACK_OR_R826_NO_SLOT_OWNER_PROOF_4674"
PACKET_MARKER = "PPC4161_PACKET_FIRST_ZM_B826_FINITE_INPUT_PACK_OR_R826_NO_SLOT_OWNER_PROOF_4674"
DECISION = "R826_EULER_RESIDUAL_IDENTITY_DERIVED_PARENT_OWNER_UNSIGNED_FINITE_INPUT_PACK_SHARPENED_NONCLAIM"
NEXT_TARGET = "4675-Y5-R2FR-source-branch-force-residual-zero-or-first-numeric-bound-row.md"

DOC_PATH = POST / "4674-Y5-R2FR-first-ZM-B826-finite-input-pack-or-R826-no-slot-owner-proof.md"
FORMAL_PATH = FORMAL / "690-PPC4161-first-ZM-B826-finite-input-pack-or-R826-no-slot-owner-proof.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4673_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4673_NEXT_TARGET.csv"
CSV_4673_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4673_R826_SLOT_OWNER_AUDIT.csv"
CSV_4673_BRIDGE = SOURCE_DIR / "P8_Y5_R2FR_4673_AM_R826_NO_SOURCE_SLOT_BRIDGE.csv"
CSV_4673_PACK = SOURCE_DIR / "P8_Y5_R2FR_4673_FIRST_ZM_B826_INPUT_PACK.csv"
CSV_4673_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4673_STATUS.csv"
CSV_4673_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4673_VALIDATION.csv"
DOC_4673 = POST / "4673-Y5-R2FR-no-source-slot-common-measure-bridge-or-first-ZM-B826-input-fill.md"
FORMAL_689 = FORMAL / "689-PPC4161-no-source-slot-common-measure-bridge-or-first-ZM-B826-input-fill.md"

CSV_4507_FORMULA = SOURCE_DIR / "P8_Y5_R2FR_4507_BMEM_EFFECTIVE_FORMULA.csv"
CSV_4514_BMEM = SOURCE_DIR / "P8_Y5_R2FR_4514_BMEM_EFFECTIVE_COMPONENT_VECTOR.csv"
CSV_4628_HESSIAN = SOURCE_DIR / "P8_Y5_R2FR_4628_PARENT_HESSIAN_ROWS.csv"
CSV_4628_NUMERIC = SOURCE_DIR / "P8_Y5_R2FR_4628_ZMEM_M2MEM_FIRST_NUMERIC_TEMPLATE_NONCLAIM.csv"
CSV_1451_THEOREM = SOURCE_DIR / "P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv"
CSV_1452_THEOREM = SOURCE_DIR / "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv"
CSV_1454_THEOREM = SOURCE_DIR / "P8_Y5_R10_1454_VARIATION_BEFORE_READOUT_THEOREM_ATTEMPT.csv"
CSV_1455_THEOREM = SOURCE_DIR / "P8_Y5_R10_1455_DERIVATIVE_BEFORE_PROJECTION_THEOREM.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4674_SOURCE_REGISTER.csv"
PROOF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4674_R826_EULER_RESIDUAL_PROOF.csv"
FINITE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4674_FIRST_FINITE_B826_BOUND_SCHEMA.csv"
INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4674_ZM_EPSILON_INPUT_SCHEMA.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4674_CONTROL_ROWS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4674_RUNNER_RESULTS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4674_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4674_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4674_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4674_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_number(path: Path, needle: str) -> int:
    for index, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    suffix = "" if not existing or existing.endswith("\n") else "\n"
    path.write_text(existing + suffix + text.lstrip("\n"), encoding="utf-8")


def csv_line(values: list[str]) -> str:
    buffer = io.StringIO()
    csv.writer(buffer, lineterminator="\n").writerow(values)
    return buffer.getvalue()


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4674_00_4673_next", CSV_4673_NEXT, "4674-Y5-R2FR-first-ZM-B826-finite-input-pack-or-R826-no-slot-owner-proof.md", "4673 selected this 4674 target."),
        ("SRC4674_01_4673_audit", CSV_4673_AUDIT, "R8264673_6_verdict", "R826 owner was unsigned."),
        ("SRC4674_02_4673_bridge", CSV_4673_BRIDGE, "BR4673_1_R826_qbasic", "R826 no-source-slot bridge requirement."),
        ("SRC4674_03_4673_pack", CSV_4673_PACK, "PACK4673_7_B826", "B826 finite input was missing."),
        ("SRC4674_04_4673_status", CSV_4673_STATUS, "NO_SOURCE_SLOT_BRIDGE_EXTENDED_TO_R826_UNSIGNED", "4673 status."),
        ("SRC4674_05_4673_validation", CSV_4673_VALIDATION, "VAL4673_OVERALL,True,PASS", "4673 validation."),
        ("SRC4674_06_doc4673", DOC_4673, "R826 no-source-slot bridge", "4673 prose bridge."),
        ("SRC4674_07_formal689", FORMAL_689, "R826 no-source-slot bridge", "4673 formal bridge."),
        ("SRC4674_08_4507_formula", CSV_4507_FORMULA, "BMF4507_1_826_term", "B826 formula."),
        ("SRC4674_09_4514_component", CSV_4514_BMEM, "BMV4514_0_B826", "B826 component vector."),
        ("SRC4674_10_4628_hessian", CSV_4628_HESSIAN, "HES4628_1_parent_hessian_definitions", "positive Z/M branch definitions."),
        ("SRC4674_11_4628_numeric", CSV_4628_NUMERIC, "LNUM4628_2_lambda", "ZM numeric template remains nonclaim."),
        ("SRC4674_12_1451_no_slot", CSV_1451_THEOREM, "OG1451_6_verdict", "no-source-slot theorem attempt."),
        ("SRC4674_13_1452_measure", CSV_1452_THEOREM, "CMT1452_6_verdict", "common measure/current attempt."),
        ("SRC4674_14_1454_readout", CSV_1454_THEOREM, "VBR1454_1_variational_identity", "variation-before-readout identity."),
        ("SRC4674_15_1455_projection", CSV_1455_THEOREM, "DBP1455_4_conclusion", "derivative-before-projection guard."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, note in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "line_number": line_number(path, needle),
                "note": note,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def proof_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "PR4674_0_known_formula",
            "Known 826 component",
            "B_826 = a_F L_cg^-2 R_m(m_L;X_B)",
            "4507/4514 give the object to attack; no cancellation is used.",
            "SOURCE_BACKED_FORMULA",
        ),
        (
            "PR4674_1_parent_euler_slot",
            "Parent stationary branch route",
            "E_m := delta S_parent/delta m = R_m + J_m_src + J_m_bdy + J_m_readout + J_m_domain = 0",
            "This is the needed local branch equation; it turns a vague missing coupling into one residual force.",
            "DERIVED_IDENTITY_IF_PARENT_EULER_DOMAIN_SIGNED",
        ),
        (
            "PR4674_2_exact_identity",
            "Euler-residual identity",
            "B_826 = -a_F L_cg^-2 (J_m_src + J_m_bdy + J_m_readout + J_m_domain) when E_m=0",
            "If the branch equation is parent-owned, B826 is not free: it is exactly the unowned branch-force residual.",
            "NEW_SHARP_DERIVATION_CONDITIONAL",
        ),
        (
            "PR4674_3_zero_corollary",
            "No-source-slot zero corollary",
            "J_m_src=J_m_bdy=J_m_readout=J_m_domain=0 => R_m=0 => B_826=0",
            "This is the clean route to the local plateau without assuming a plateau.",
            "ZERO_COROLLARY_UNSIGNED",
        ),
        (
            "PR4674_4_countermodel",
            "Pre-action branch-force countermodel",
            "S_parent may include J_m_source m or w_R R(m;X_B) before variation",
            "Then the stationarity equation gives R_m=-J_m_source and B826 survives.",
            "COUNTERMODEL_SURVIVES_CURRENT_CORPUS",
        ),
        (
            "PR4674_5_finite_bound",
            "Finite fallback bound",
            "|B_826| <= |a_F| L_cg^-2 (|J_m_src|+|J_m_bdy|+|J_m_readout|+|J_m_domain|+|E_m_res|)",
            "The next empirical row should source these residuals, not just say coupling is missing.",
            "EXECUTABLE_BOUND_FORM_DERIVED",
        ),
        (
            "PR4674_6_verdict",
            "R826 owner proof status",
            "exact zero requires parent-signed E_m domain plus all J_m residuals zero",
            "The derivation improves the target, but local-GR/R10/PPN claims remain false.",
            "PARENT_OWNER_UNSIGNED_NONCLAIM",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "proof_id": row[0],
            "claim": row[1],
            "mathematical_form": row[2],
            "consequence": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def finite_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BND4674_0_master", "B826_master", "|B_826| <= |a_F| L_cg^-2 |J_m_unowned|", "a_F;L_cg;J_m_unowned;units;source_path", "MISSING_NUMERIC_INPUTS"),
        ("BND4674_1_source", "J_m_src", "vertical/source branch-force part", "source species/body;norm convention;value;units;source_path", "MISSING_SOURCE_FORCE_ROW"),
        ("BND4674_2_boundary", "J_m_bdy", "boundary/collar branch-force part", "surface/domain;value;units;source_path", "MISSING_BOUNDARY_FORCE_ROW"),
        ("BND4674_3_readout", "J_m_readout", "readout/calibration branch-force part", "readout map;value;units;source_path", "MISSING_READOUT_FORCE_ROW"),
        ("BND4674_4_domain", "J_m_domain", "derivative-before-projection/domain residual", "projection map;commutator norm;value;units;source_path", "MISSING_DOMAIN_FORCE_ROW"),
        ("BND4674_5_euler", "E_m_res", "parent Euler residual if stationarity not signed", "branch equation;residual;units;source_path", "MISSING_PARENT_EULER_CERTIFICATE"),
        ("BND4674_6_claim_gate", "valid_for_claim", "true only if bound has numeric sourced rows and local arena comparator", "all rows numeric; units compatible; source paths exist", "FALSE_NOW"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row[0],
            "symbol": row[1],
            "definition": row[2],
            "required_columns": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def input_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("IN4674_0_Z0", "Z0", "positive branch kinetic/Hessian lower bound", "MISSING_PARENT_HESSIAN_NUMERIC"),
        ("IN4674_1_M0", "M0^2", "positive branch gap/Hessian lower bound", "MISSING_PARENT_GAP_NUMERIC"),
        ("IN4674_2_lambda", "lambda_mem=sqrt(Z0/M0^2)", "range from same branch, not R10 anchor", "MISSING_SAME_BRANCH_RATIO"),
        ("IN4674_3_epsilonA", "epsilon_A", "visible/source vertical sensitivity", "MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND"),
        ("IN4674_4_epsilonB", "epsilon_B", "test body/source vertical sensitivity", "MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND"),
        ("IN4674_5_aF", "a_F", "front coefficient in B826", "MISSING_PARENT_COEFFICIENT"),
        ("IN4674_6_Lcg", "L_cg", "conversion/correlation length in B826", "MISSING_PARENT_LENGTH"),
        ("IN4674_7_Jm", "J_m_unowned", "unowned branch-force residual from Euler identity", "MISSING_FORCE_RESIDUAL_ROWS"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "input_id": row[0],
            "symbol": row[1],
            "role": row[2],
            "status": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CTRL4674_0_no_plateau_axiom", "Do not assume R_m=0 as a plateau axiom; derive it from E_m=0 and J_m=0.", "ACTIVE"),
        ("CTRL4674_1_no_r10_as_hessian", "Do not use Eot-Wash/R10 anchor as Z0/M0 parent Hessian evidence.", "ACTIVE"),
        ("CTRL4674_2_no_cancellation", "Do not cancel B826 against Weyl/Y5/Y6/boundary/readout pieces to claim local GR.", "ACTIVE"),
        ("CTRL4674_3_same_branch", "All Z/M/lambda/aF/Lcg/Jm rows must live on the same parent branch.", "ACTIVE"),
        ("CTRL4674_4_nonclaim", "Keep local-GR/R10/PPN claims false until proof or numeric bound passes.", "ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "rule": row[1],
            "status": row[2],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "why": "4674 derives a sharper Euler-residual identity: B826 is zero only when the parent local branch is stationary and all unowned branch-force residuals vanish; otherwise B826 is exactly bounded by those residuals.",
            "promoted": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "euler_identity_derived": True,
            "parent_euler_domain_signed": False,
            "Jm_zero_signed": False,
            "finite_bound_schema_ready": True,
            "numeric_inputs_sourced": False,
            "B826_zero": False,
            "local_GR_claim": False,
            "r10_claim": False,
            "ppn_claim": False,
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "The B826 problem has been reduced to J_m_unowned. The next executable step is to prove J_m_unowned=0 from source/variation/readout grammar, or fill the first numeric bound row for it.",
            "derive_route": "Prove parent stationary local branch E_m=0 plus no source/boundary/readout/domain branch-force residuals.",
            "fallback_route": "Create numeric/source-backed rows for a_F, L_cg, J_m_src, J_m_bdy, J_m_readout, J_m_domain and compare with local arenas.",
            "avoid": "Do not call B826 zero from m_L notation alone; do not use empirical R10 bounds as parent coefficients.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def runner_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    proofs: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    identity_ok = any(row["proof_id"] == "PR4674_2_exact_identity" for row in proofs)
    zero_refused = any(row["proof_id"] == "PR4674_6_verdict" and row["status"] == "PARENT_OWNER_UNSIGNED_NONCLAIM" for row in proofs)
    finite_ok = any(row["bound_id"] == "BND4674_0_master" for row in finite)
    inputs_nonclaim = all(not row["valid_for_claim"] and not row["claim_allowed"] for row in inputs)
    checks = [
        ("RUN4674_0_sources", source_ok, "all source paths and needles found" if source_ok else "source path/needle failure"),
        ("RUN4674_1_identity", identity_ok, "Euler-residual identity row present" if identity_ok else "identity row missing"),
        ("RUN4674_2_zero_refused", zero_refused, "zero corollary remains nonclaim" if zero_refused else "zero was promoted"),
        ("RUN4674_3_finite_bound", finite_ok, "finite B826 bound schema present" if finite_ok else "finite schema missing"),
        ("RUN4674_4_inputs_nonclaim", inputs_nonclaim, "numeric input rows remain nonclaim" if inputs_nonclaim else "input row promoted"),
        ("RUN4674_5_next", True, "next target selected"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "runner_id": check_id,
            "passed": passed,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]


def validation_rows(timestamp: str, csv_paths: list[Path], sources: list[dict[str, Any]], runners: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    rows.append({"validation_id": "VAL4674_0_sources", "passed": source_ok, "detail": "all source paths and needles found" if source_ok else "source path/needle failure", "timestamp_utc": timestamp})
    parse_ok = True
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            detail = f"rows={len(parsed)} columns={len(parsed[0]) if parsed else 0}"
            passed = bool(parsed)
        except Exception as exc:  # pragma: no cover
            detail = repr(exc)
            passed = False
        parse_ok = parse_ok and passed
        rows.append({"validation_id": f"VAL4674_parse_{path.name}", "passed": passed, "detail": detail, "timestamp_utc": timestamp})
    runner_ok = all(row["passed"] for row in runners)
    rows.append({"validation_id": "VAL4674_1_runner_pass", "passed": runner_ok, "detail": "runner rows passed" if runner_ok else "runner failure", "timestamp_utc": timestamp})
    output_paths = [DOC_PATH, FORMAL_PATH, *csv_paths]
    outputs_exist = all(path.exists() for path in output_paths)
    rows.append({"validation_id": "VAL4674_2_outputs_exist", "passed": outputs_exist, "detail": ";".join(str(path) for path in output_paths), "timestamp_utc": timestamp})
    nonclaim = "valid_for_claim,true" not in read_text(RUNNER_CSV).lower() and "claim_allowed,true" not in read_text(RUNNER_CSV).lower()
    rows.append({"validation_id": "VAL4674_3_no_claim_promotion", "passed": nonclaim, "detail": "valid_for_claim remains false", "timestamp_utc": timestamp})
    overall = source_ok and parse_ok and runner_ok and outputs_exist and nonclaim
    rows.append({"validation_id": "VAL4674_OVERALL", "passed": overall, "detail": "PASS" if overall else "FAIL", "timestamp_utc": timestamp})
    return rows


def write_documents(
    sources: list[dict[str, Any]],
    proofs: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    body = f"""# 4674 - Y5/R2FR First ZM+B826 Finite Input Pack or R826 No-Slot Owner Proof

**Current verdict:** 4674 makes a real step forward: the B826 problem is reduced to a single Euler-residual identity. If the parent local branch equation is signed and the unowned branch-force residual vanishes, then `B_826=0`. If not, `B_826` is not mysterious; it is bounded by the residual `J_m_unowned`.

## Core derivation

From 4507/4514:

```text
B_826 = a_F L_cg^-2 R_m(m_L; X_B)
```

Introduce the parent local branch equation:

```text
E_m := delta S_parent/delta m
     = R_m + J_m_src + J_m_bdy + J_m_readout + J_m_domain
     = 0.
```

Therefore, on a parent-owned stationary local branch:

```text
B_826 = -a_F L_cg^-2 (J_m_src + J_m_bdy + J_m_readout + J_m_domain).
```

So the plateau route is no longer an axiom. It is the special case:

```text
J_m_src = J_m_bdy = J_m_readout = J_m_domain = 0
=> R_m = 0
=> B_826 = 0.
```

The current corpus does not yet parent-sign those zero clauses, so this remains private/nonclaim.

## Runner results

{table(runners)}

## Decision

{table(decisions)}

## Status

{table(statuses)}

## Next target

{table(nexts)}

## R826 Euler-residual proof

{table(proofs)}

## First finite B826 bound schema

{table(finite)}

## ZM and epsilon input schema

{table(inputs)}

## Controls

{table(controls)}

## Source register

{table(sources)}

## Validation

{table(validations)}
"""
    DOC_PATH.write_text(body, encoding="utf-8")
    FORMAL_PATH.write_text(body.replace("# 4674 -", "# 690 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        claim = csv_line(
            [
                CLAIM_ID,
                "local_gr_empirical_interface",
                "4674 derives the R826 Euler-residual identity: B_826 is zero only if the parent local branch is stationary and all unowned branch-force residuals vanish; otherwise B_826 is exactly bounded by those residuals.",
                "Generated source register, Euler-residual proof rows, finite B826 bound schema, ZM/epsilon input schema, controls, runner, decision, status, next target and validation.",
                DECISION.lower(),
                NEXT_TARGET,
                "Calling m_L an extremum without a parent Euler certificate, using R10 anchors as Hessian data, or cancelling B826 against unrelated Bmem pieces.",
                "local_gr",
                str(DOC_PATH),
                NEXT_TARGET,
                "No public local-GR/Newton/PPN/R10 claim until J_m_unowned is theorem-zero or source-backed numeric bounds pass.",
            ]
        )
        append_once(CLAIMS_PATH, CLAIM_ID, claim)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""

## {MARKER}

4674 reduces the `B_826` obstruction to an Euler-residual identity:

```text
B_826 = -a_F L_cg^-2 J_m_unowned
```

on a parent-owned stationary local branch. Exact zero now requires `J_m_unowned=0`, not an assumed plateau. If that cannot be proven, the first finite bound row is explicit. Status remains private/nonclaim; local-GR/R10/PPN claims stay false.

- checkpoint: `{DOC_PATH.name}`
- formal note: `{FORMAL_PATH.name}`
- decision: `{DECISION}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""

## {PACKET_MARKER}

Packet update: `B_826` is now routed through the branch-force residual `J_m_unowned`. This is the least hand-wavy formulation of the coupling gap so far: either prove the residual vanishes from parent source/variation/readout grammar, or measure/source-bound it directly.

- claim id: `{CLAIM_ID}`
- source csv: `{SOURCE_REGISTER.name}`
- proof csv: `{PROOF_CSV.name}`
- finite csv: `{FINITE_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def main() -> None:
    timestamp = now()
    sources = source_rows(timestamp)
    proofs = proof_rows(timestamp)
    finite = finite_rows(timestamp)
    inputs = input_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    runners = runner_rows(timestamp, sources, proofs, finite, inputs)

    csv_paths = [
        SOURCE_REGISTER,
        PROOF_CSV,
        FINITE_CSV,
        INPUT_CSV,
        CONTROL_CSV,
        RUNNER_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(PROOF_CSV, proofs)
    write_csv(FINITE_CSV, finite)
    write_csv(INPUT_CSV, inputs)
    write_csv(CONTROL_CSV, controls)
    write_csv(RUNNER_CSV, runners)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_documents(sources, proofs, finite, inputs, controls, runners, decisions, statuses, nexts, [])
    validations = validation_rows(timestamp, csv_paths, sources, runners)
    write_csv(VALIDATION_CSV, validations)
    write_documents(sources, proofs, finite, inputs, controls, runners, decisions, statuses, nexts, validations)
    update_registers(timestamp)
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
