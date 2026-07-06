from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from no_marker_source_extension_gate import (  # noqa: E402
    claim_gate_rows,
    decision_rows as gate_decision_rows,
    marker_residual_rows,
    no_marker_theorem_rows,
    read_csv,
    readout_classification_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4473"
CLAIM_ID = "L-315"
MARKER = "PPC4161_NO_MARKER_SOURCE_EXTENSION_PROOF_OR_CELL_MARKER_RESIDUAL_ROW_4473"
PACKET_MARKER = "PPC4161_PACKET_NO_MARKER_SOURCE_EXTENSION_PROOF_OR_CELL_MARKER_RESIDUAL_ROW_4473"
DECISION = "NO_MARKER_SOURCE_EXTENSION_CONTRACT_WRITTEN_PARENT_UNSIGNED_MARKER_RESIDUAL_ROWS_STAGED_NONCLAIM"
NEXT_TARGET = "4474-Y5-R2FR-external-readout-no-backreaction-proof-or-marker-coupling-fill.md"

FORMAL_PATH = FORMAL / "489-PPC4161-no-marker-source-extension-proof-or-cell-marker-residual-row.md"
DOC_PATH = POST / "4473-Y5-R2FR-no-marker-source-extension-proof-or-cell-marker-residual-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4473_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4473_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4473_NO_MARKER_THEOREM.csv"
RESIDUAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4473_CELL_MARKER_RESIDUAL_ROW.csv"
READOUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4473_READOUT_CLASSIFICATION.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4473_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4473_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4473_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4473_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4473_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "no_marker_source_extension_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4473_no_marker_source_extension_proof_or_cell_marker_residual_row.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4472 = SOURCE_DIR / "P8_Y5_R2FR_4472_NEXT_TARGET.csv"
FORMAL_488 = FORMAL / "488-PPC4161-refinement-parameter-gauge-proof-or-ellcell-source-normalization.md"
PROOF_4472 = SOURCE_DIR / "P8_Y5_R2FR_4472_REFINEMENT_PARAMETER_GAUGE_PROOF.csv"
MATRIX_4472 = SOURCE_DIR / "P8_Y5_R2FR_4472_GAUGE_VS_GRAIN_DECISION_MATRIX.csv"
ELL_4472 = SOURCE_DIR / "P8_Y5_R2FR_4472_ELLCELL_SOURCE_NORMALIZATION.csv"
FORMAL_476 = FORMAL / "476-PPC4161-parent-refinement-gauge-signature-or-visible-c2-finite-row.md"
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
            "source_id": "SRC4473_00_next4472",
            "ref": NEXT_4472,
            "needle": "4473-Y5-R2FR-no-marker-source-extension-proof-or-cell-marker-residual-row.md",
            "role": "4472 selected no-marker/source-extension proof or marker residual row.",
        },
        {
            "source_id": "SRC4473_01_formal488",
            "ref": FORMAL_488,
            "needle": "no physical marker/source extension",
            "role": "4472 identifies marker/source extension as the next obstruction.",
        },
        {
            "source_id": "SRC4473_02_proof4472_marker",
            "ref": PROOF_4472,
            "needle": "RPG4472_3_no_marker_extension",
            "role": "machine-readable no-marker proof clause.",
        },
        {
            "source_id": "SRC4473_03_matrix4472_marker",
            "ref": MATRIX_4472,
            "needle": "GVG4472_2_marker_extended_quotient",
            "role": "machine-readable marker-extended quotient countermodel.",
        },
        {
            "source_id": "SRC4473_04_ell4472_physical",
            "ref": ELL_4472,
            "needle": "ELL4472_1_physical_scale_source",
            "role": "ellcell finite source-normalization row.",
        },
        {
            "source_id": "SRC4473_05_refinement_marker_contract",
            "ref": FORMAL_476,
            "needle": "RGC4460_3_no_physical_marker_or_grain",
            "role": "refinement contract requiring no physical marker/grain.",
        },
        {
            "source_id": "SRC4473_06_cell340_external_readout",
            "ref": POST_340,
            "needle": "if the reference mask is only observer/source dressing",
            "role": "external readout safe route.",
        },
        {
            "source_id": "SRC4473_07_cell340_physical_marker",
            "ref": POST_340,
            "needle": "physical marker fields or boundary defects whose background is P_active",
            "role": "physical marker/boundary defect hazard.",
        },
        {
            "source_id": "SRC4473_08_cell340_relational_boundary",
            "ref": POST_340,
            "needle": "relational boundary reference",
            "role": "boundary reference conditional route.",
        },
        {
            "source_id": "SRC4473_09_cell340_material_marker",
            "ref": POST_340,
            "needle": "material marker/boundary defect",
            "role": "material marker counterroute.",
        },
        {
            "source_id": "SRC4473_10_cell341_external_readout",
            "ref": POST_341,
            "needle": "if the reference is observer/source dressing",
            "role": "quotient relational readout safe route.",
        },
        {
            "source_id": "SRC4473_11_cell341_covariant_marker",
            "ref": POST_341,
            "needle": "covariant material marker",
            "role": "covariant marker descends but remains physical.",
        },
        {
            "source_id": "SRC4473_12_cell341_marker_background",
            "ref": POST_341,
            "needle": "marker/background variables whose value is P_active",
            "role": "marker/background exclusion requirement.",
        },
        {
            "source_id": "SRC4473_13_cell341_no_marker_contract",
            "ref": POST_341,
            "needle": "no marker/background extension exists",
            "role": "quotient parent-action no-marker contract.",
        },
        {
            "source_id": "SRC4473_14_gate",
            "ref": GATE_PATH,
            "needle": "def no_marker_theorem_rows",
            "role": "4473 no-marker/source-extension gate.",
        },
        {
            "source_id": "SRC4473_15_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4473"',
            "role": "4473 generator script.",
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
            "proof_result": "no-marker/source-extension theorem contract written with external-readout exception and variational-silence clauses",
            "parent_status": "not signed; marker field absence and no-backreaction remain open",
            "fallback_result": "cell-marker residual row staged for M_cell, lambda_M, ell_marker, c_R2_marker, C_marker and marker stress/source",
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
            "no_marker_contract": "written",
            "parent_signature_status": "not_signed",
            "sharpest_open_clause": "external_readout_no_variational_backreaction",
            "marker_residual_status": "staged_missing_source_values",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4473_0",
            "target": NEXT_TARGET,
            "objective": "Prove external/source-at-zero readout has no variational backreaction, or fill marker coupling rows for local tests.",
            "derive_first": "show R_obs enters only observables, not S_bulk, with zero Hilbert/coframe/connection/scalar source",
            "fallback": "source lambda_M, ell_marker, c_R2_marker, C_marker and T_marker/J_marker rows with arena projections",
            "risk": "calling a relational material marker external readout without checking variation",
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
            "claim": "4473 writes the no-marker/source-extension contract: a relational marker is safe only if it is external readout with no bulk action slot, no variational backreaction, no boundary residue, and no labelled-species interpretation.",
            "current_evidence": "4473 source register, no-marker theorem rows, marker residual rows, readout classification, claim gates, decision/status/next CSVs and validation.",
            "status": "private_nonclaim_checkpoint",
            "next_test": NEXT_TARGET,
            "key_risk": "mistaking relational covariance for absence of marker stress, source coupling, or primitive grain data.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "finite marker c_R2/C_total/source-stress branch survives if no-backreaction is not parent-signed",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    theorem_rows: Sequence[Mapping[str, object]],
    residual_rows: Sequence[Mapping[str, object]],
    readout_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 489 PPC4161 - No Marker Source Extension Proof Or Cell Marker Residual Row

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4473 isolates the marker loophole.

A relational marker/source readout is safe only if it is genuinely external:

```text
R_obs appears in observables O_read[Phi;R_obs],
but not in S_bulk,
so delta S_bulk/delta R_obs = 0
and it has no Hilbert/coframe/connection/scalar source.
```

If the marker has a bulk action slot, stress tensor, boundary residue, source charge, curvature-linear vertex, or labelled-species meaning, it is not gauge. It becomes a finite residual branch:

```text
c_R2_marker = zeta_M*lambda_M*ell_marker^2/N_EH
              + c_marker_bare
              + 0.5*B_M^T*L_M^-1*B_M.
```

Current MTS has not parent-signed the no-marker/no-backreaction package. Therefore no local-GR claim fires. The win is that the marker branch is no longer fog: it has named coefficient rows feeding `c_R2_eff`, `C_total`, R10, PPN, clocks, orbital and source-coupling gates.

## No-Marker Theorem Rows

{table(theorem_rows)}

## Cell-Marker Residual Rows

{table(residual_rows)}

## Readout Classification

{table(readout_rows)}

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
    residual_rows: Sequence[Mapping[str, object]],
    readout_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4473 Y5/R2FR - No Marker Source Extension Proof Or Cell Marker Residual Row

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

The marker loophole is now a variational test. External readout is safe only if it never enters `S_bulk`; material/source markers become finite `c_R2_marker/C_marker/T_marker` rows.

## No-Marker Contract

{table(theorem_rows)}

## Marker Residuals

{table(residual_rows)}

## Readout Classes

{table(readout_rows)}

## Gates

{table(gates)}

## Decisions

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
    residual_rows: Sequence[Mapping[str, object]],
    readout_rows: Sequence[Mapping[str, object]],
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
        "VAL4473_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4473_1_no_marker_contract_written",
        any(row.get("theorem_id") == "NME4473_6_verdict" for row in theorem_rows),
        "no-marker/source-extension theorem contract is written",
    )
    add(
        "VAL4473_2_parent_signature_not_overclaimed",
        any(row.get("theorem_id") == "NME4473_6_verdict" and row.get("parent_signed") is False for row in theorem_rows),
        "no-marker theorem remains parent-unsigned",
    )
    add(
        "VAL4473_3_external_readout_exception_present",
        any(row.get("theorem_id") == "NME4473_1_external_readout_exception" for row in theorem_rows)
        and any(row.get("class_id") == "RC4473_0_external_observer_readout" for row in readout_rows),
        "external readout safe exception is explicit",
    )
    add(
        "VAL4473_4_marker_countermodel_present",
        any(row.get("class_id") == "RC4473_2_material_marker" for row in readout_rows)
        and any(row.get("row_id") == "MR4473_3_marker_cR2" for row in residual_rows),
        "material marker countermodel and c_R2 residual row are present",
    )
    add(
        "VAL4473_5_marker_residuals_have_missing_markers",
        any("MISSING" in str(row.get("current_value")) for row in residual_rows) and all(row.get("valid_for_claim") is False for row in residual_rows),
        "marker residual rows remain source-request/nonclaim",
    )
    add(
        "VAL4473_6_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4473_2_no_marker_parent_signed" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR scalar closure",
    )
    add(
        "VAL4473_7_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, theorem_rows, residual_rows, readout_rows, gates, decisions, statuses, next_targets]
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
    add("VAL4473_8_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4473_9_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4473_10_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-315",
    )
    add(
        "VAL4473_11_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4473_12_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    theorem_rows = no_marker_theorem_rows()
    residual_rows = marker_residual_rows()
    readout_rows = readout_classification_rows()
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, theorem_rows, residual_rows, readout_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem_rows)
    write_csv(RESIDUAL_CSV, residual_rows)
    write_csv(READOUT_CSV, readout_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, theorem_rows, residual_rows, readout_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, theorem_rows, residual_rows, readout_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4473 No-Marker Source Extension Contract",
        "4473 turns the marker loophole into a variational test. Relational/source readout is safe only if it is external to `S_bulk`, has no Hilbert/coframe/connection/scalar source, and has no boundary residue or labelled-species meaning. Current MTS has not parent-signed that no-backreaction package, so a finite marker branch is staged with `M_cell`, `lambda_M`, `ell_marker`, `c_R2_marker`, `C_marker` and `T_marker/J_marker` rows.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4473 Packet Integration",
        "The private packet now distinguishes external readout from material marker. Quotient covariance is not enough; a marker is safe only if it never enters the bulk variational problem. Otherwise it becomes a source-normalized residual branch for R10/PPN/local-GR scoring.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        RESIDUAL_CSV,
        READOUT_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, theorem_rows, residual_rows, readout_rows, gates, decisions, statuses, next_targets, csv_paths)
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
