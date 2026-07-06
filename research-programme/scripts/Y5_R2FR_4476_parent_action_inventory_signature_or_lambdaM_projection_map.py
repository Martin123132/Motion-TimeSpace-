from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from parent_action_inventory_projection_gate import (  # noqa: E402
    claim_gate_rows,
    decision_rows as gate_decision_rows,
    inventory_signature_rows,
    lambda_projection_map_rows,
    projection_intake_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4476"
CLAIM_ID = "L-318"
MARKER = "PPC4161_PARENT_ACTION_INVENTORY_SIGNATURE_OR_LAMBDAM_PROJECTION_MAP_4476"
PACKET_MARKER = "PPC4161_PACKET_PARENT_ACTION_INVENTORY_SIGNATURE_OR_LAMBDAM_PROJECTION_MAP_4476"
DECISION = "PARENT_INVENTORY_SIGNATURE_WRITTEN_UNSIGNED_LAMBDAM_PROJECTION_MAP_DERIVED_NONCLAIM"
NEXT_TARGET = "4477-Y5-R2FR-parent-inventory-zero-proof-or-marker-profile-moment-derivation.md"

FORMAL_PATH = FORMAL / "492-PPC4161-parent-action-inventory-signature-or-lambdaM-projection-map.md"
DOC_PATH = POST / "4476-Y5-R2FR-parent-action-inventory-signature-or-lambdaM-projection-map.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4476_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4476_SOURCE_REGISTER.csv"
INVENTORY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4476_PARENT_ACTION_INVENTORY_SIGNATURE.csv"
PROJECTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4476_LAMBDAM_PROJECTION_MAP.csv"
INTAKE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4476_PROJECTION_INTAKE_ROWS.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4476_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4476_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4476_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4476_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4476_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "parent_action_inventory_projection_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4476_parent_action_inventory_signature_or_lambdaM_projection_map.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_491 = FORMAL / "491-PPC4161-marker-bulk-coupling-zero-theorem-or-first-lambdaM-source-row.md"
NEXT_4475 = SOURCE_DIR / "P8_Y5_R2FR_4475_NEXT_TARGET.csv"
THEOREM_4475 = SOURCE_DIR / "P8_Y5_R2FR_4475_MARKER_BULK_COUPLING_ZERO_THEOREM.csv"
AUDIT_4475 = SOURCE_DIR / "P8_Y5_R2FR_4475_LAMBDAM_OPERATOR_AUDIT.csv"
SOURCE_4475 = SOURCE_DIR / "P8_Y5_R2FR_4475_LAMBDAM_SOURCE_ROW.csv"
GATES_4475 = SOURCE_DIR / "P8_Y5_R2FR_4475_CLAIM_GATES.csv"
COUPLING_4474 = SOURCE_DIR / "P8_Y5_R2FR_4474_MARKER_COUPLING_FILL_ROWS.csv"


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
            "source_id": "SRC4476_00_next4475",
            "ref": NEXT_4475,
            "needle": "4476-Y5-R2FR-parent-action-inventory-signature-or-lambdaM-projection-map.md",
            "role": "4475 selected parent inventory signature or lambda_M projection map.",
        },
        {
            "source_id": "SRC4476_01_formal491_projection",
            "ref": FORMAL_491,
            "needle": "lambda_M = Pi_{F_M O_marker}(S_bulk).",
            "role": "formal 4475 action-projection definition.",
        },
        {
            "source_id": "SRC4476_02_theorem4475_verdict",
            "ref": THEOREM_4475,
            "needle": "LMB4475_7_verdict",
            "role": "4475 lambda_M zero theorem verdict.",
        },
        {
            "source_id": "SRC4476_03_audit4475_bulk",
            "ref": AUDIT_4475,
            "needle": "LOA4475_0_bulk_marker_monomial",
            "role": "4475 bulk marker monomial audit.",
        },
        {
            "source_id": "SRC4476_04_audit4475_aux",
            "ref": AUDIT_4475,
            "needle": "LOA4475_3_auxiliary_marker_sector",
            "role": "4475 hidden auxiliary escape route.",
        },
        {
            "source_id": "SRC4476_05_source4475_projection",
            "ref": SOURCE_4475,
            "needle": "LMR4475_5_projection_targets",
            "role": "4475 projection-target source row.",
        },
        {
            "source_id": "SRC4476_06_gates4475_parent_zero",
            "ref": GATES_4475,
            "needle": "CG4475_2_parent_zero_signed",
            "role": "4475 claim gate blocks parent-zero overclaim.",
        },
        {
            "source_id": "SRC4476_07_coupling4474_cR2",
            "ref": COUPLING_4474,
            "needle": "MCF4474_5_c_R2_marker",
            "role": "4474 c_R2 marker target row.",
        },
        {
            "source_id": "SRC4476_08_coupling4474_Cmarker",
            "ref": COUPLING_4474,
            "needle": "MCF4474_6_C_marker",
            "role": "4474 source-coupling marker target row.",
        },
        {
            "source_id": "SRC4476_09_coupling4474_Tmarker",
            "ref": COUPLING_4474,
            "needle": "MCF4474_7_T_marker_J_marker",
            "role": "4474 stress/current marker target row.",
        },
        {
            "source_id": "SRC4476_10_coupling4474_boundary",
            "ref": COUPLING_4474,
            "needle": "MCF4474_8_boundary_marker",
            "role": "4474 boundary marker target row.",
        },
        {
            "source_id": "SRC4476_11_gate",
            "ref": GATE_PATH,
            "needle": "def inventory_signature_rows",
            "role": "4476 parent inventory/projection gate.",
        },
        {
            "source_id": "SRC4476_12_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4476"',
            "role": "4476 generator script.",
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
            "proof_result": "parent inventory signature written as Pi_{I_M}(S_bulk)=0 but not parent-signed",
            "fallback_result": "finite lambda_M projection map derived for c_R2_marker, C_marker, stress/current, scalar/current and boundary channels",
            "claim_status": "private_nonclaim",
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
            "inventory_signature": "written_parent_unsigned",
            "projection_map": "derived_template",
            "sharpest_open_clause": "Z_inventory_or_marker_profile_moments",
            "projection_intake_status": "staged_missing_values",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4476_0",
            "target": NEXT_TARGET,
            "objective": "Try to prove the parent inventory zero signature directly; if it cannot sign, derive marker profile moments mu0_M and mu2_M from parent geometry/support.",
            "derive_first": "show the parent action alphabet has no marker ideal I_M, so Pi_{I_M}(S_bulk)=0",
            "fallback": "derive or source mu0_M, mu2_M, zeta_a and N_a for the lambda_M projection vector",
            "risk": "using the projection map as evidence before its moments/projectors/normalizations are sourced",
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
            "claim": "4476 writes the parent action inventory signature Pi_{I_M}(S_bulk)=0 and derives the finite lambda_M projection map into c_R2_marker, C_marker, T_marker/J_marker, scalar/current and boundary residual channels.",
            "current_evidence": "4476 source register, parent action inventory signature, lambda_M projection map, projection intake rows, claim gates, decision/status/next CSVs and validation.",
            "status": "private_projection_map_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "using the projection map as evidence before the parent inventory is signed or the marker moments/projectors/normalizations are sourced.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "finite lambda_M branch remains unscored until Z_inventory or projection inputs close",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    inventory_rows: Sequence[Mapping[str, object]],
    projection_rows: Sequence[Mapping[str, object]],
    intake_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 492 PPC4161 - Parent Action Inventory Signature Or LambdaM Projection Map

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4476 turns the `lambda_M` fork into two precise roads.

The clean road is an action-inventory signature:

```text
I_M = <M_cell, R_obs_as_bulk, P_active, J_finite, labelled_species, M_aux>
Z_inventory = True iff Pi_I_M(S_bulk) = 0.
```

If that signature is parent-signed, every marker bulk coupling vanishes at once. Current MTS has not signed it yet.

The fallback road is now projectable:

```text
Delta S_M = int sqrt(-g) lambda_M F_M O_a
C_a^M = lambda_M*(zeta_a*mu0_M + zeta_grad_a*mu2_M/L_loc^2)/N_a.
```

So a finite marker branch can no longer float around as a mystery coupling. It has to land in `c_R2_marker`, `C_marker`, `T_marker/J_marker`, scalar/current leakage, or `boundary_marker`, with no cancellation credit.

## Parent Action Inventory Signature

{table(inventory_rows)}

## LambdaM Projection Map

{table(projection_rows)}

## Projection Intake Rows

{table(intake_rows)}

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
    inventory_rows: Sequence[Mapping[str, object]],
    projection_rows: Sequence[Mapping[str, object]],
    intake_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4476 Y5/R2FR - Parent Action Inventory Signature Or LambdaM Projection Map

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

`lambda_M` now has a full fork: prove the marker ideal in the parent action is empty, or project finite `lambda_M` through marker moments into local residual channels. This is not a claim pass; it is a sharper derivation/score map.

## Inventory Signature

{table(inventory_rows)}

## Projection Map

{table(projection_rows)}

## Intake Rows

{table(intake_rows)}

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
    inventory_rows: Sequence[Mapping[str, object]],
    projection_rows: Sequence[Mapping[str, object]],
    intake_rows: Sequence[Mapping[str, object]],
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
        "VAL4476_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4476_1_inventory_signature_written",
        any(row.get("signature_id") == "PAI4476_5_verdict" for row in inventory_rows),
        "parent inventory signature verdict is written",
    )
    add(
        "VAL4476_2_inventory_not_overclaimed",
        any(row.get("signature_id") == "PAI4476_5_verdict" and row.get("parent_signed") is False for row in inventory_rows),
        "inventory signature remains parent-unsigned",
    )
    add(
        "VAL4476_3_projection_map_covers_channels",
        all(
            any(row.get("map_id") == map_id for row in projection_rows)
            for map_id in [
                "PMAP4476_1_curvature_square",
                "PMAP4476_3_source_measure",
                "PMAP4476_4_em_or_stress",
                "PMAP4476_5_scalar_gamma_khat",
                "PMAP4476_6_boundary_interface",
                "PMAP4476_7_no_cancellation_envelope",
            ]
        ),
        "projection map covers curvature, source, stress/EM, scalar/current, boundary and envelope channels",
    )
    add(
        "VAL4476_4_projection_intake_rows_staged",
        all(
            any(row.get("row_id") == row_id for row in intake_rows)
            for row_id in [
                "PIR4476_0_parent_inventory_signature",
                "PIR4476_1_mu0_M",
                "PIR4476_2_mu2_M",
                "PIR4476_3_zeta_basis",
                "PIR4476_4_normalizations",
                "PIR4476_5_projection_values",
            ]
        ),
        "projection intake rows include inventory, moments, projectors, normalizations and values",
    )
    add(
        "VAL4476_5_projection_rows_remain_nonclaim",
        any("MISSING" in str(row.get("current_value")) for row in intake_rows)
        and all(row.get("valid_for_claim") is False for row in intake_rows),
        "projection intake rows keep missing source values and valid_for_claim=false",
    )
    add(
        "VAL4476_6_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4476_2_inventory_parent_signed" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR/R10 promotion until parent inventory is signed",
    )
    add(
        "VAL4476_7_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, inventory_rows, projection_rows, intake_rows, gates, decisions, statuses, next_targets]
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
    add("VAL4476_8_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4476_9_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4476_10_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-318",
    )
    add(
        "VAL4476_11_spine_and_packet_updated",
        MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH),
        "unification spine and private packet integration contain 4476 markers",
    )
    add(
        "VAL4476_12_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4476_13_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    inventory_rows = inventory_signature_rows()
    projection_rows = lambda_projection_map_rows()
    intake_rows = projection_intake_rows()
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, inventory_rows, projection_rows, intake_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(INVENTORY_CSV, inventory_rows)
    write_csv(PROJECTION_CSV, projection_rows)
    write_csv(INTAKE_CSV, intake_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, inventory_rows, projection_rows, intake_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, inventory_rows, projection_rows, intake_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4476 Parent Inventory Or LambdaM Projection Map",
        "4476 writes the clean parent-action inventory signature as `Pi_{I_M}(S_bulk)=0`, where the marker ideal contains material markers, bulk readout, finite diagnostic sources, active labels, labelled species and hidden marker auxiliaries. Because this is not yet parent-signed, 4476 derives the finite `lambda_M` projection map into `c_R2_marker`, `C_marker`, `T_marker/J_marker`, scalar/current and boundary channels with a no-cancellation envelope.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4476 Packet Integration",
        "The private packet now has a two-road `lambda_M` fork: sign the parent action inventory and close the branch, or use the projection map with marker moments `mu0_M`, `mu2_M`, projectors `zeta_a`, normalizations `N_a` and the componentwise residual vector.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        INVENTORY_CSV,
        PROJECTION_CSV,
        INTAKE_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, inventory_rows, projection_rows, intake_rows, gates, decisions, statuses, next_targets, csv_paths)
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
