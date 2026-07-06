from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from marker_bulk_coupling_gate import (  # noqa: E402
    claim_gate_rows,
    decision_rows as gate_decision_rows,
    lambda_operator_audit_rows,
    lambda_source_row_rows,
    marker_bulk_zero_theorem_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4475"
CLAIM_ID = "L-317"
MARKER = "PPC4161_MARKER_BULK_COUPLING_ZERO_THEOREM_OR_FIRST_LAMBDAM_SOURCE_ROW_4475"
PACKET_MARKER = "PPC4161_PACKET_MARKER_BULK_COUPLING_ZERO_THEOREM_OR_FIRST_LAMBDAM_SOURCE_ROW_4475"
DECISION = "LAMBDAM_ACTION_PROJECTION_ZERO_THEOREM_DERIVED_PARENT_UNSIGNED_FIRST_SOURCE_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4476-Y5-R2FR-parent-action-inventory-signature-or-lambdaM-projection-map.md"

FORMAL_PATH = FORMAL / "491-PPC4161-marker-bulk-coupling-zero-theorem-or-first-lambdaM-source-row.md"
DOC_PATH = POST / "4475-Y5-R2FR-marker-bulk-coupling-zero-theorem-or-first-lambdaM-source-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4475_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4475_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4475_MARKER_BULK_COUPLING_ZERO_THEOREM.csv"
AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4475_LAMBDAM_OPERATOR_AUDIT.csv"
SOURCE_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4475_LAMBDAM_SOURCE_ROW.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4475_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4475_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4475_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4475_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4475_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "marker_bulk_coupling_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4475_marker_bulk_coupling_zero_theorem_or_first_lambdaM_source_row.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_490 = FORMAL / "490-PPC4161-external-readout-no-backreaction-proof-or-marker-coupling-fill.md"
NEXT_4474 = SOURCE_DIR / "P8_Y5_R2FR_4474_NEXT_TARGET.csv"
THEOREM_4474 = SOURCE_DIR / "P8_Y5_R2FR_4474_EXTERNAL_READOUT_NO_BACKREACTION_THEOREM.csv"
AUDIT_4474 = SOURCE_DIR / "P8_Y5_R2FR_4474_VARIATIONAL_SOURCE_AUDIT.csv"
COUPLING_4474 = SOURCE_DIR / "P8_Y5_R2FR_4474_MARKER_COUPLING_FILL_ROWS.csv"
GATES_4474 = SOURCE_DIR / "P8_Y5_R2FR_4474_CLAIM_GATES.csv"
RESIDUAL_4473 = SOURCE_DIR / "P8_Y5_R2FR_4473_CELL_MARKER_RESIDUAL_ROW.csv"
READOUT_4473 = SOURCE_DIR / "P8_Y5_R2FR_4473_READOUT_CLASSIFICATION.csv"
POST_340 = POST / "340-full-cell-equivalence-gauge-redundancy-gate.md"
POST_341 = POST / "341-indistinguishable-cell-quotient-parent-action-gate.md"


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
            "source_id": "SRC4475_00_next4474",
            "ref": NEXT_4474,
            "needle": "4475-Y5-R2FR-marker-bulk-coupling-zero-theorem-or-first-lambdaM-source-row.md",
            "role": "4474 selected marker bulk coupling as next target.",
        },
        {
            "source_id": "SRC4475_01_formal490_lambda",
            "ref": FORMAL_490,
            "needle": "The first branch to attack is `lambda_M`.",
            "role": "formal 4474 identifies lambda_M as first finite branch.",
        },
        {
            "source_id": "SRC4475_02_theorem4474_verdict",
            "ref": THEOREM_4474,
            "needle": "ERN4474_7_verdict",
            "role": "4474 verdict: exact conditional readout theorem but parent unsigned.",
        },
        {
            "source_id": "SRC4475_03_audit4474_bulk_absence",
            "ref": AUDIT_4474,
            "needle": "VSA4474_0_bulk_absence",
            "role": "4474 bulk absence audit row.",
        },
        {
            "source_id": "SRC4475_04_audit4474_source_zero",
            "ref": AUDIT_4474,
            "needle": "VSA4474_6_source_at_zero",
            "role": "4474 source-at-zero firewall.",
        },
        {
            "source_id": "SRC4475_05_coupling4474_lambda",
            "ref": COUPLING_4474,
            "needle": "MCF4474_1_lambda_M",
            "role": "4474 marker bulk coupling fill row.",
        },
        {
            "source_id": "SRC4475_06_gates4474_parent_role",
            "ref": GATES_4474,
            "needle": "CG4474_2_parent_readout_role_signed",
            "role": "4474 claim gate blocks parent readout overclaim.",
        },
        {
            "source_id": "SRC4475_07_residual4473_lambda",
            "ref": RESIDUAL_4473,
            "needle": "MR4473_1_marker_bulk_coupling",
            "role": "4473 earlier lambda_M source row.",
        },
        {
            "source_id": "SRC4475_08_readout4473_material_marker",
            "ref": READOUT_4473,
            "needle": "RC4473_2_material_marker",
            "role": "4473 material-marker countermodel.",
        },
        {
            "source_id": "SRC4475_09_cell340_source_zero",
            "ref": POST_340,
            "needle": "source-at-zero",
            "role": "340 source-at-zero route.",
        },
        {
            "source_id": "SRC4475_10_cell340_physical_marker",
            "ref": POST_340,
            "needle": "physical marker fields or boundary defects whose background is P_active",
            "role": "340 marker/boundary defect counterroute.",
        },
        {
            "source_id": "SRC4475_11_cell341_backreaction_open",
            "ref": POST_341,
            "needle": "relational readout has no backreaction",
            "role": "341 no-backreaction as open quotient clause.",
        },
        {
            "source_id": "SRC4475_12_cell341_covariant_marker",
            "ref": POST_341,
            "needle": "covariant material marker",
            "role": "341 covariance is not enough to erase material marker.",
        },
        {
            "source_id": "SRC4475_13_gate",
            "ref": GATE_PATH,
            "needle": "def marker_bulk_zero_theorem_rows",
            "role": "4475 marker bulk coupling gate.",
        },
        {
            "source_id": "SRC4475_14_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4475"',
            "role": "4475 generator script.",
        },
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        source_path = Path(spec["ref"])
        needle = str(spec["needle"])
        line_number = line_of(source_path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_kind": "local",
                "source_ref": str(source_path),
                "local_path_exists": source_path.exists(),
                "needle": needle,
                "needle_found": line_number > 0,
                "line_number": line_number,
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
            "proof_result": "lambda_M defined as parent-action projection coefficient and proved zero on the external-readout/source-at-zero branch",
            "parent_status": "not signed; parent action inventory, readout role, finite-J, spurion, auxiliary and boundary firewalls remain open",
            "fallback_result": "first lambda_M source row staged with O_marker, F_M, N_M and projection target rows",
            "local_GR_claim": False,
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
            "zero_theorem": "derived_conditionally",
            "parent_signature_status": "not_signed",
            "sharpest_open_clause": "parent_action_inventory_or_lambdaM_projection_map",
            "lambdaM_source_status": "staged_missing_parent_zero_or_numeric_value",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4475_0",
            "target": NEXT_TARGET,
            "objective": "Either sign the parent action inventory that forbids marker monomials, or derive the projection from finite lambda_M into c_R2_marker/C_marker local residuals.",
            "derive_first": "audit parent action grammar for every admissible marker-containing monomial and prove the projection ideal is empty",
            "fallback": "derive Pi_local(lambda_M) to c_R2_marker, C_marker, T_marker/J_marker and boundary_marker without cancellation",
            "risk": "proving lambda_M=0 for explicit terms while leaving hidden auxiliary or boundary marker channels alive",
            "valid_for_claim": False,
        }
    ]


def append_section_once(path: Path, marker: str, title: str, body: str) -> None:
    current = text(path)
    if marker in current:
        return
    addition = f"\n\n## {title}\n\nMarker: `{marker}`  \n{body}\n"
    write_text(path, current.rstrip() + addition + "\n")


def update_claims_register() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr_newton_r10_scalar_source_coupling",
            "claim": "4475 defines lambda_M as the parent-action projection coefficient of a marker-containing bulk monomial and derives lambda_M=0 on the external-readout/source-at-zero branch.",
            "current_evidence": "4475 source register, marker bulk coupling zero theorem, lambda_M operator audit, lambda_M source row, claim gates, decision/status/next CSVs and validation.",
            "status": "private_conditional_theorem_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "treating explicit lambda_M absence as full closure while hidden finite-J, spurion, auxiliary or boundary marker routes remain unsigned.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "finite lambda_M branch survives unless the parent action inventory or projection map is completed",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    theorem_rows: Sequence[Mapping[str, object]],
    audit_rows: Sequence[Mapping[str, object]],
    source_row_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 491 PPC4161 - Marker Bulk Coupling Zero Theorem Or First LambdaM Source Row

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4475 pins down the coupling throat.

The marker bulk coupling is defined as an action projection:

```text
Delta S_M = int sqrt(-g) lambda_M F_M(M_cell) O_marker[Phi],
lambda_M = Pi_{{F_M O_marker}}(S_bulk).
```

So the zero theorem is simple and sharp:

```text
if S_bulk contains no marker monomial,
and R_obs is only external readout or J=0 source dressing,
and no finite-J, spurion, auxiliary, or boundary substitute exists,
then lambda_M = 0.
```

That is a real derivation. It says the coupling vanishes by action algebra, not by wishful closure. But current MTS has not yet signed the full parent action inventory, so the finite source row remains live.

## Marker Bulk Coupling Zero Theorem

{table(theorem_rows)}

## LambdaM Operator Audit

{table(audit_rows)}

## First LambdaM Source Row

{table(source_row_rows)}

## Decision Ledger

{table(ledger)}

## Claim Gates

{table(gates)}

## Status

{table(statuses)}

## Next Target

{table(next_targets)}

## Source Register

{table(sources)}

## Decision Row

{table(decisions)}
"""


def post_body(
    sources: Sequence[Mapping[str, object]],
    theorem_rows: Sequence[Mapping[str, object]],
    audit_rows: Sequence[Mapping[str, object]],
    source_row_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4475 Y5/R2FR - Marker Bulk Coupling Zero Theorem Or First LambdaM Source Row

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

`lambda_M` is now an action-projection coefficient. If the marker monomial is absent from `S_bulk`, it is zero. If it is present, the first finite branch has named rows for `lambda_M`, `O_marker`, `F_M`, `N_M` and `Pi_local(lambda_M)`.

## Zero Theorem

{table(theorem_rows)}

## Operator Audit

{table(audit_rows)}

## Source Rows

{table(source_row_rows)}

## Gates And Decisions

{table(gates)}

{table(ledger)}

{table(decisions)}

## Status And Next Target

{table(statuses)}

{table(next_targets)}

## Sources

{table(sources)}
"""


def validate(
    sources: Sequence[Mapping[str, object]],
    theorem_rows: Sequence[Mapping[str, object]],
    audit_rows: Sequence[Mapping[str, object]],
    source_row_rows: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    validations: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": passed,
                "detail": detail,
                "valid_for_claim": False,
            }
        )

    add(
        "VAL4475_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4475_1_lambda_projection_law_written",
        any(row.get("theorem_id") == "LMB4475_0_coefficient_definition" for row in theorem_rows),
        "lambda_M is defined as a parent-action projection coefficient",
    )
    add(
        "VAL4475_2_conditional_zero_theorem_written",
        any(row.get("theorem_id") == "LMB4475_7_verdict" for row in theorem_rows)
        and any(row.get("theorem_id") == "LMB4475_1_external_readout_zero" for row in theorem_rows),
        "conditional lambda_M=0 theorem is written",
    )
    add(
        "VAL4475_3_parent_signature_not_overclaimed",
        any(row.get("theorem_id") == "LMB4475_7_verdict" and row.get("parent_signed") is False for row in theorem_rows),
        "the lambda_M zero theorem remains parent-unsigned and nonclaim",
    )
    add(
        "VAL4475_4_operator_audit_covers_escape_routes",
        all(
            any(row.get("audit_id") == audit_id for row in audit_rows)
            for audit_id in [
                "LOA4475_0_bulk_marker_monomial",
                "LOA4475_1_diagnostic_source",
                "LOA4475_2_spurion_background",
                "LOA4475_3_auxiliary_marker_sector",
                "LOA4475_4_boundary_interface",
                "LOA4475_5_componentwise_guard",
            ]
        ),
        "operator audit covers bulk, source, spurion, auxiliary, boundary and cancellation routes",
    )
    add(
        "VAL4475_5_lambda_source_rows_staged",
        all(
            any(row.get("row_id") == row_id for row in source_row_rows)
            for row_id in [
                "LMR4475_0_zero_certificate",
                "LMR4475_1_lambda_M",
                "LMR4475_2_O_marker",
                "LMR4475_3_F_M",
                "LMR4475_4_N_M",
                "LMR4475_5_projection_targets",
            ]
        ),
        "first lambda_M source row and projection rows are staged",
    )
    add(
        "VAL4475_6_lambda_rows_remain_nonclaim",
        any("MISSING" in str(row.get("current_value")) for row in source_row_rows)
        and all(row.get("valid_for_claim") is False for row in source_row_rows),
        "lambda_M rows keep missing parent zero/numeric values and valid_for_claim=false",
    )
    add(
        "VAL4475_7_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4475_2_parent_zero_signed" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR/R10 promotion until parent zero is signed",
    )
    add(
        "VAL4475_8_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, theorem_rows, audit_rows, source_row_rows, gates, decisions, statuses, next_targets]
            for row in group
        ),
        "all generated rows remain private/nonclaim",
    )
    csv_ok = True
    csv_detail: List[str] = []
    for csv_path in csv_paths:
        try:
            parsed_rows = read_csv(csv_path)
            csv_detail.append(f"{csv_path.name}:{len(parsed_rows)}")
        except Exception as exc:  # pragma: no cover
            csv_ok = False
            csv_detail.append(f"{csv_path.name}:ERROR:{exc}")
    add("VAL4475_9_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4475_10_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4475_11_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-317",
    )
    add(
        "VAL4475_12_spine_and_packet_updated",
        MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH),
        "unification spine and private packet integration contain 4475 markers",
    )
    add(
        "VAL4475_13_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4475_14_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    theorem_rows = marker_bulk_zero_theorem_rows()
    audit_rows = lambda_operator_audit_rows()
    source_row_rows = lambda_source_row_rows()
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, theorem_rows, audit_rows, source_row_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem_rows)
    write_csv(AUDIT_CSV, audit_rows)
    write_csv(SOURCE_ROW_CSV, source_row_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, theorem_rows, audit_rows, source_row_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, theorem_rows, audit_rows, source_row_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4475 Marker Bulk Coupling LambdaM Throat",
        "4475 defines `lambda_M` as the parent-action projection coefficient of a marker-containing bulk monomial. On the external-readout/source-at-zero branch, if no finite-J, spurion, auxiliary or boundary substitute exists, the action projection is empty and `lambda_M=0`. The parent action inventory has not yet signed that absence, so a first finite `lambda_M` source row remains live.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4475 Packet Integration",
        "The private packet now treats the marker coupling as an action-algebra coefficient rather than a verbal gap. Either the parent action grammar forbids every marker monomial and `lambda_M=0`, or the finite branch must declare `O_marker`, `F_M`, `N_M`, `lambda_M` and `Pi_local(lambda_M)`.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        AUDIT_CSV,
        SOURCE_ROW_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, theorem_rows, audit_rows, source_row_rows, gates, decisions, statuses, next_targets, csv_paths)
    write_csv(VALIDATION_PATH, validations)

    failed = [row for row in validations if str(row.get("passed")).lower() != "true"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Generated {CHECKPOINT}: {FORMAL_PATH}")
    print(f"Validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
