from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from external_readout_no_backreaction_gate import (  # noqa: E402
    claim_gate_rows,
    decision_rows as gate_decision_rows,
    external_readout_theorem_rows,
    marker_coupling_fill_rows,
    read_csv,
    variational_source_audit_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4474"
CLAIM_ID = "L-316"
MARKER = "PPC4161_EXTERNAL_READOUT_NO_BACKREACTION_PROOF_OR_MARKER_COUPLING_FILL_4474"
PACKET_MARKER = "PPC4161_PACKET_EXTERNAL_READOUT_NO_BACKREACTION_PROOF_OR_MARKER_COUPLING_FILL_4474"
DECISION = "EXTERNAL_READOUT_NO_BACKREACTION_CONDITIONAL_PROOF_DERIVED_PARENT_UNSIGNED_MARKER_COUPLING_ROWS_STAGED_NONCLAIM"
NEXT_TARGET = "4475-Y5-R2FR-marker-bulk-coupling-zero-theorem-or-first-lambdaM-source-row.md"

FORMAL_PATH = FORMAL / "490-PPC4161-external-readout-no-backreaction-proof-or-marker-coupling-fill.md"
DOC_PATH = POST / "4474-Y5-R2FR-external-readout-no-backreaction-proof-or-marker-coupling-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4474_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4474_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4474_EXTERNAL_READOUT_NO_BACKREACTION_THEOREM.csv"
AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4474_VARIATIONAL_SOURCE_AUDIT.csv"
COUPLING_CSV = SOURCE_DIR / "P8_Y5_R2FR_4474_MARKER_COUPLING_FILL_ROWS.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4474_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4474_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4474_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4474_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4474_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "external_readout_no_backreaction_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4474_external_readout_no_backreaction_proof_or_marker_coupling_fill.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_489 = FORMAL / "489-PPC4161-no-marker-source-extension-proof-or-cell-marker-residual-row.md"
NEXT_4473 = SOURCE_DIR / "P8_Y5_R2FR_4473_NEXT_TARGET.csv"
THEOREM_4473 = SOURCE_DIR / "P8_Y5_R2FR_4473_NO_MARKER_THEOREM.csv"
RESIDUAL_4473 = SOURCE_DIR / "P8_Y5_R2FR_4473_CELL_MARKER_RESIDUAL_ROW.csv"
READOUT_4473 = SOURCE_DIR / "P8_Y5_R2FR_4473_READOUT_CLASSIFICATION.csv"
STATUS_4473 = SOURCE_DIR / "P8_Y5_R2FR_4473_STATUS.csv"
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
            "source_id": "SRC4474_00_next4473",
            "ref": NEXT_4473,
            "needle": "4474-Y5-R2FR-external-readout-no-backreaction-proof-or-marker-coupling-fill.md",
            "role": "4473 selected external-readout no-backreaction as next target.",
        },
        {
            "source_id": "SRC4474_01_formal489_Robs",
            "ref": FORMAL_489,
            "needle": "delta S_bulk/delta R_obs = 0",
            "role": "4473 formal statement of readout silence condition.",
        },
        {
            "source_id": "SRC4474_02_theorem4473_variational_silence",
            "ref": THEOREM_4473,
            "needle": "NME4473_2_bulk_variational_silence",
            "role": "machine-readable open no-backreaction clause.",
        },
        {
            "source_id": "SRC4474_03_residual4473_lambdaM",
            "ref": RESIDUAL_4473,
            "needle": "MR4473_1_marker_bulk_coupling",
            "role": "previous marker coupling fallback row.",
        },
        {
            "source_id": "SRC4474_04_readout4473_external",
            "ref": READOUT_4473,
            "needle": "RC4473_0_external_observer_readout",
            "role": "previous readout classification route.",
        },
        {
            "source_id": "SRC4474_05_status4473_open_clause",
            "ref": STATUS_4473,
            "needle": "external_readout_no_variational_backreaction",
            "role": "4473 status identifies the sharpest open clause.",
        },
        {
            "source_id": "SRC4474_06_cell340_source_at_zero",
            "ref": POST_340,
            "needle": "source-at-zero",
            "role": "earlier source-at-zero readout route.",
        },
        {
            "source_id": "SRC4474_07_cell340_external_readout",
            "ref": POST_340,
            "needle": "if the reference mask is only observer/source dressing",
            "role": "340 safe external readout fork.",
        },
        {
            "source_id": "SRC4474_08_cell340_physical_marker",
            "ref": POST_340,
            "needle": "physical marker fields or boundary defects whose background is P_active",
            "role": "340 physical marker counterroute.",
        },
        {
            "source_id": "SRC4474_09_cell340_boundary_reference",
            "ref": POST_340,
            "needle": "relational boundary reference",
            "role": "340 boundary readout caveat.",
        },
        {
            "source_id": "SRC4474_10_cell341_external_readout",
            "ref": POST_341,
            "needle": "if the reference is observer/source dressing",
            "role": "341 quotient readout safe fork.",
        },
        {
            "source_id": "SRC4474_11_cell341_readout_backreaction_open",
            "ref": POST_341,
            "needle": "relational readout has no backreaction",
            "role": "341 leaves no-backreaction as an open quotient clause.",
        },
        {
            "source_id": "SRC4474_12_cell341_covariant_marker",
            "ref": POST_341,
            "needle": "covariant material marker",
            "role": "341 shows covariance is not enough to erase a physical marker.",
        },
        {
            "source_id": "SRC4474_13_cell341_no_marker_contract",
            "ref": POST_341,
            "needle": "no marker/background extension exists",
            "role": "341 parent-action no-marker requirement.",
        },
        {
            "source_id": "SRC4474_14_gate",
            "ref": GATE_PATH,
            "needle": "def external_readout_theorem_rows",
            "role": "4474 external-readout no-backreaction gate.",
        },
        {
            "source_id": "SRC4474_15_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4474"',
            "role": "4474 generator script.",
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
            "proof_result": "exact conditional no-backreaction lemma derived for external readout and source-at-zero insertions",
            "parent_status": "not signed; parent field-inventory/readout-action split must prove R_obs is not material",
            "fallback_result": "marker coupling intake rows staged for M_cell, lambda_M, ell_marker, zeta_M, c_R2_marker, C_marker, T_marker/J_marker and boundary_marker",
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
            "conditional_theorem": "derived",
            "parent_signature_status": "not_signed",
            "sharpest_open_clause": "marker_bulk_coupling_lambda_M_zero_or_source",
            "marker_coupling_status": "staged_missing_source_values",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4474_0",
            "target": NEXT_TARGET,
            "objective": "Attack the first physical marker coupling directly: prove lambda_M=0 by parent grammar/source-at-zero role, or source it as a finite branch.",
            "derive_first": "show no parent term can contain F_M(M_cell) O_marker once R_obs is classified as external readout/J=0 source",
            "fallback": "declare O_marker, lambda_M, support, operator dimension, sign and source path for R10/PPN scoring",
            "risk": "leaving lambda_M as a verbal missing input instead of proving zero or making it a bounded coefficient",
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
            "claim": "4474 derives the exact conditional no-backreaction lemma for external readout/source-at-zero variables: if R_obs is absent from the bulk action and any diagnostic source J is set to zero before variation, the bulk, Hilbert, coframe, connection, scalar and curvature-vertex source terms vanish.",
            "current_evidence": "4474 source register, external-readout theorem rows, variational source audit, marker coupling fill rows, claim gates, decision/status/next CSVs and validation.",
            "status": "private_conditional_theorem_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "treating the conditional readout theorem as parent-signed before the MTS field inventory proves R_obs is not a material marker.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "finite lambda_M/c_R2_marker/C_marker/T_marker branch survives unless the parent grammar signs external readout/source-at-zero role",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    theorem_rows: Sequence[Mapping[str, object]],
    audit_rows: Sequence[Mapping[str, object]],
    coupling_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 490 PPC4161 - External Readout No-Backreaction Proof Or Marker Coupling Fill

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4474 actually proves the clean route, but only as a conditional theorem.

If the reference/readout variable `R_obs` is only a post-solution observable or a diagnostic source set to zero, write

```text
S_total[Phi;R_obs,J] = S_bulk[Phi] + S_boundary[Phi] + int J O_read[Phi;R_obs].
```

The physical local equations are taken at `J=0`, so

```text
delta S_total/delta Phi | J=0 = delta S_bulk/delta Phi + delta S_boundary/delta Phi.
```

Therefore the readout contributes no bulk equation, no Hilbert stress, no coframe/connection current, no scalar source, and no curvature-square vertex. This proves the external-readout/source-at-zero no-backreaction lemma.

The theorem does **not** yet prove that MTS uses this safe route. If `R_obs` is actually a material marker, boundary defect, active-cell spurion, finite diagnostic source, or source-measure multiplier, it becomes a physical coupling branch. The first branch to attack is `lambda_M`.

## External Readout No-Backreaction Theorem

{table(theorem_rows)}

## Variational Source Audit

{table(audit_rows)}

## Marker Coupling Fill Rows

{table(coupling_rows)}

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
    coupling_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4474 Y5/R2FR - External Readout No-Backreaction Proof Or Marker Coupling Fill

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

The readout route is no longer just an open phrase. It has a derivation: if `R_obs` appears only in `O_read` or in `int J O_read` with `J=0` before variation, all local source variations vanish. If that parent role is not signed, the branch becomes a finite marker-coupling problem, beginning with `lambda_M`.

## Conditional Theorem

{table(theorem_rows)}

## Variational Source Audit

{table(audit_rows)}

## Coupling Rows

{table(coupling_rows)}

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
    coupling_rows: Sequence[Mapping[str, object]],
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
        "VAL4474_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4474_1_conditional_theorem_written",
        any(row.get("theorem_id") == "ERN4474_7_verdict" for row in theorem_rows),
        "external-readout no-backreaction theorem verdict is written",
    )
    add(
        "VAL4474_2_all_variational_zeros_derived_conditionally",
        all(
            any(row.get("theorem_id") == theorem_id for row in theorem_rows)
            for theorem_id in [
                "ERN4474_1_bulk_Robs_variation",
                "ERN4474_2_hilbert_stress_zero",
                "ERN4474_3_coframe_connection_scalar_zero",
                "ERN4474_4_source_at_zero_lemma",
                "ERN4474_5_curvature_vertex_zero",
            ]
        ),
        "bulk, Hilbert, coframe/connection/scalar, source-at-zero and curvature-vertex zero clauses exist",
    )
    add(
        "VAL4474_3_parent_signature_not_overclaimed",
        any(row.get("theorem_id") == "ERN4474_7_verdict" and row.get("parent_signed") is False for row in theorem_rows),
        "the theorem remains parent-unsigned and nonclaim",
    )
    add(
        "VAL4474_4_audit_covers_source_slots",
        all(
            any(row.get("audit_id") == audit_id for row in audit_rows)
            for audit_id in [
                "VSA4474_0_bulk_absence",
                "VSA4474_1_metric_stress",
                "VSA4474_2_coframe_connection",
                "VSA4474_3_scalar_source",
                "VSA4474_4_curvature_vertex",
                "VSA4474_5_boundary_flux",
                "VSA4474_6_source_at_zero",
            ]
        ),
        "variational audit covers bulk, metric, coframe/connection, scalar, curvature, boundary and source-at-zero slots",
    )
    add(
        "VAL4474_5_marker_coupling_rows_staged",
        all(
            any(row.get("row_id") == row_id for row in coupling_rows)
            for row_id in [
                "MCF4474_1_lambda_M",
                "MCF4474_2_ell_marker",
                "MCF4474_5_c_R2_marker",
                "MCF4474_6_C_marker",
                "MCF4474_7_T_marker_J_marker",
                "MCF4474_8_boundary_marker",
            ]
        ),
        "marker coupling rows include first finite components and local arenas",
    )
    add(
        "VAL4474_6_marker_rows_remain_nonclaim",
        any("MISSING" in str(row.get("current_value")) for row in coupling_rows)
        and all(row.get("valid_for_claim") is False for row in coupling_rows),
        "marker coupling rows keep missing source values and valid_for_claim=false",
    )
    add(
        "VAL4474_7_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4474_2_parent_readout_role_signed" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR/R10 promotion until parent readout role is signed",
    )
    add(
        "VAL4474_8_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, theorem_rows, audit_rows, coupling_rows, gates, decisions, statuses, next_targets]
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
    add("VAL4474_9_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4474_10_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4474_11_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-316",
    )
    add(
        "VAL4474_12_spine_and_packet_updated",
        MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH),
        "unification spine and private packet integration contain 4474 markers",
    )
    add(
        "VAL4474_13_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4474_14_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    theorem_rows = external_readout_theorem_rows()
    audit_rows = variational_source_audit_rows()
    coupling_rows = marker_coupling_fill_rows()
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, theorem_rows, audit_rows, coupling_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem_rows)
    write_csv(AUDIT_CSV, audit_rows)
    write_csv(COUPLING_CSV, coupling_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, theorem_rows, audit_rows, coupling_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, theorem_rows, audit_rows, coupling_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4474 External Readout No-Backreaction Lemma",
        "4474 proves the conditional no-backreaction theorem for external readout/source-at-zero variables: if `R_obs` appears only in post-solution `O_read` or `int J O_read` with `J=0` before variation, bulk equations, Hilbert stress, coframe/connection currents, scalar sources and curvature-square vertices are unchanged. The parent has not yet signed that MTS readout is only this safe kind, so marker coupling rows remain live, starting with `lambda_M`.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4474 Packet Integration",
        "The private packet now has a genuine external-readout no-backreaction lemma rather than a verbal assumption. It also has finite fallback rows for `M_cell`, `lambda_M`, `ell_marker`, `zeta_M`, `c_R2_marker`, `C_marker`, `T_marker/J_marker` and boundary residues if the readout is material.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        AUDIT_CSV,
        COUPLING_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, theorem_rows, audit_rows, coupling_rows, gates, decisions, statuses, next_targets, csv_paths)
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
