from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from refinement_parameter_gauge_gate import (  # noqa: E402
    claim_gate_rows,
    decision_rows as gate_decision_rows,
    ellcell_source_normalization_rows,
    gauge_vs_grain_decision_rows,
    read_csv,
    refinement_gauge_proof_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4472"
CLAIM_ID = "L-314"
MARKER = "PPC4161_REFINEMENT_PARAMETER_GAUGE_PROOF_OR_ELLCELL_SOURCE_NORMALIZATION_4472"
PACKET_MARKER = "PPC4161_PACKET_REFINEMENT_PARAMETER_GAUGE_PROOF_OR_ELLCELL_SOURCE_NORMALIZATION_4472"
DECISION = "REFINEMENT_PARAMETER_GAUGE_CONTRACT_WRITTEN_MARKER_HAZARD_RETAINED_ELLCELL_NORMALIZATION_ROWS_STAGED_NONCLAIM"
NEXT_TARGET = "4473-Y5-R2FR-no-marker-source-extension-proof-or-cell-marker-residual-row.md"

FORMAL_PATH = FORMAL / "488-PPC4161-refinement-parameter-gauge-proof-or-ellcell-source-normalization.md"
DOC_PATH = POST / "4472-Y5-R2FR-refinement-parameter-gauge-proof-or-ellcell-source-normalization.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4472_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4472_SOURCE_REGISTER.csv"
PROOF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4472_REFINEMENT_PARAMETER_GAUGE_PROOF.csv"
ELL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4472_ELLCELL_SOURCE_NORMALIZATION.csv"
MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4472_GAUGE_VS_GRAIN_DECISION_MATRIX.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4472_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4472_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4472_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4472_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4472_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "refinement_parameter_gauge_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4472_refinement_parameter_gauge_proof_or_ellcell_source_normalization.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4471 = SOURCE_DIR / "P8_Y5_R2FR_4471_NEXT_TARGET.csv"
FORMAL_487 = FORMAL / "487-PPC4161-no-local-length-scale-or-grain-proof-or-first-cR2eff-intake-row.md"
THEOREM_4471 = SOURCE_DIR / "P8_Y5_R2FR_4471_NO_GRAIN_THEOREM.csv"
INTAKE_4471 = SOURCE_DIR / "P8_Y5_R2FR_4471_FIRST_CR2EFF_INTAKE_ROW.csv"
FORMAL_476 = FORMAL / "476-PPC4161-parent-refinement-gauge-signature-or-visible-c2-finite-row.md"
FORMAL_479 = FORMAL / "479-PPC4161-parent-kappa-scale-law-or-calibrated-G-residual-runner.md"
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
            "source_id": "SRC4472_00_next4471",
            "ref": NEXT_4471,
            "needle": "4472-Y5-R2FR-refinement-parameter-gauge-proof-or-ellcell-source-normalization.md",
            "role": "4471 selected refinement-gauge/ellcell source normalization.",
        },
        {
            "source_id": "SRC4472_01_formal487",
            "ref": FORMAL_487,
            "needle": "c_R2_cell = xi_shape * c2_visible * ell_cell^2 / N_EH",
            "role": "4471 visible-cell cR2 scaling formula.",
        },
        {
            "source_id": "SRC4472_02_theorem4471",
            "ref": THEOREM_4471,
            "needle": "NG4471_1_refinement_gauge_zero",
            "role": "machine-readable no-grain conditional theorem row.",
        },
        {
            "source_id": "SRC4472_03_intake4471",
            "ref": INTAKE_4471,
            "needle": "CR2I4471_0_visible_cell_component",
            "role": "machine-readable visible cR2 intake row.",
        },
        {
            "source_id": "SRC4472_04_refinement_contract",
            "ref": FORMAL_476,
            "needle": "RGC4460_3_no_physical_marker_or_grain",
            "role": "no physical marker/grain refinement contract.",
        },
        {
            "source_id": "SRC4472_05_refinement_gauge_case",
            "ref": FORMAL_476,
            "needle": "DICH4460_0_exact_refinement_gauge",
            "role": "exact refinement gauge dichotomy case.",
        },
        {
            "source_id": "SRC4472_06_refinement_physical_grain",
            "ref": FORMAL_476,
            "needle": "DICH4460_2_physical_grain_cutoff",
            "role": "physical grain fallback case.",
        },
        {
            "source_id": "SRC4472_07_kappa_no_circular",
            "ref": FORMAL_479,
            "needle": "CIRCULAR_IF_ELL_CELL_EQUALS_L_PLANCK_BY_DECLARATION",
            "role": "no circular Planck/G scale guard.",
        },
        {
            "source_id": "SRC4472_08_cell340_label_symmetry",
            "ref": POST_340,
            "needle": "label symmetry alone is not enough",
            "role": "cell symmetry is not gauge proof.",
        },
        {
            "source_id": "SRC4472_09_cell340_marker",
            "ref": POST_340,
            "needle": "physical marker fields or boundary defects whose background is P_active",
            "role": "marker/boundary defect hazard.",
        },
        {
            "source_id": "SRC4472_10_cell340_contract",
            "ref": POST_340,
            "needle": "cell labels are arbitrary enumeration labels, not physical species",
            "role": "gauge-redundancy contract clause.",
        },
        {
            "source_id": "SRC4472_11_cell341_quotient",
            "ref": POST_341,
            "needle": "the quotient route is mathematically clean",
            "role": "quotient route exists.",
        },
        {
            "source_id": "SRC4472_12_cell341_formula_trap",
            "ref": POST_341,
            "needle": "the formula alone does not derive gauge redundancy",
            "role": "same formula trap.",
        },
        {
            "source_id": "SRC4472_13_cell341_marker",
            "ref": POST_341,
            "needle": "marker/background variables whose value is P_active",
            "role": "marker extension hazard.",
        },
        {
            "source_id": "SRC4472_14_gate",
            "ref": GATE_PATH,
            "needle": "def refinement_gauge_proof_rows",
            "role": "4472 refinement-parameter gauge gate.",
        },
        {
            "source_id": "SRC4472_15_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4472"',
            "role": "4472 generator script.",
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
            "proof_result": "ell gauge theorem contract written; quotient route is exact only if parent state/action/observable descent and no-marker clauses sign",
            "parent_status": "not signed; current corpus keeps marker and labelled-species counterroutes live",
            "fallback_result": "ell_cell, xi_shape, N_EH, c2_visible, visible c_R2_cell and total c_R2_eff normalization rows staged",
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
            "refinement_gauge_contract": "written",
            "parent_signature_status": "not_signed",
            "sharpest_open_clause": "no_marker_source_extension",
            "ellcell_fallback_status": "staged_missing_source_normalization",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4472_0",
            "target": NEXT_TARGET,
            "objective": "Prove no physical marker/source extension can carry primitive grain data, or create a cell-marker residual row with units and test arenas.",
            "derive_first": "show any relational/source readout is external dressing with no variational backreaction and no bulk action slot",
            "fallback": "source marker residual coupling, ell_cell dependence and projection into c_R2_eff/C_total/R10/PPN rows",
            "risk": "treating a covariant marker as gauge just because the pair descends to a quotient",
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
            "claim": "4472 writes the exact refinement-parameter gauge contract: ell is gauge only if projective state space, cylindrical observables, action descent, no-marker extension, no circular scale and no singular residue clauses all sign.",
            "current_evidence": "4472 source register, refinement gauge proof rows, ellcell normalization rows, gauge-vs-grain decision matrix, claim gates, decision/status/next CSVs and validation.",
            "status": "private_nonclaim_checkpoint",
            "next_test": NEXT_TARGET,
            "key_risk": "mistaking quotient covariance or a transforming marker pair for absence of physical primitive grain data.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "marker/source extension or labelled-species route can keep finite ell_cell/c_R2_cell alive",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    proof_rows: Sequence[Mapping[str, object]],
    ell_rows: Sequence[Mapping[str, object]],
    matrix_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 488 PPC4161 - Refinement Parameter Gauge Proof Or `ell_cell` Source Normalization

Private checkpoint: `{CHECKPOINT}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Generated UTC: `{STAMP}`

## Result

4472 sharpens the no-grain route into an exact parent-signature theorem:

```text
ell is gauge
iff
projective/quotient parent state space
+ cylindrical physical observables
+ descending bulk action
+ no physical marker/source extension
+ no circular scale normalization
+ no singular R2 residue.
```

If those clauses sign, `ell_cell` is not a local physical length and the visible `c_R2_cell` route closes. But the current corpus does not sign them together. In particular, 340/341 show the killer hazard: a covariant marker can descend to an extended quotient while still carrying physical active/grain data. Therefore quotient covariance alone is not enough.

So 4472 does not claim local GR. It stages the finite fallback cleanly: if `ell` is physical or marker-carried, source `ell_cell`, `xi_shape`, `N_EH`, `c2_visible`, visible `c_R2_cell`, and total `c_R2_eff`.

## Refinement Gauge Proof Rows

{table(proof_rows)}

## `ell_cell` Source Normalization Rows

{table(ell_rows)}

## Gauge Vs Grain Decision Matrix

{table(matrix_rows)}

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
    proof_rows: Sequence[Mapping[str, object]],
    ell_rows: Sequence[Mapping[str, object]],
    matrix_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4472 Y5/R2FR - Refinement Parameter Gauge Proof Or `ell_cell` Source Normalization

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

The `ell_cell` fight is now honest: `ell` is gauge only when the parent owns quotient/projective state space, cylindrical observables, descending action, and no marker extension. The marker extension is the thing to hunt next.

## Proof Contract

{table(proof_rows)}

## Source Normalization

{table(ell_rows)}

## Decision Matrix

{table(matrix_rows)}

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
    proof_rows: Sequence[Mapping[str, object]],
    ell_rows: Sequence[Mapping[str, object]],
    matrix_rows: Sequence[Mapping[str, object]],
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
        "VAL4472_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4472_1_contract_written",
        any(row.get("proof_id") == "RPG4472_6_verdict" for row in proof_rows),
        "refinement-parameter gauge theorem contract is written",
    )
    add(
        "VAL4472_2_parent_signature_not_overclaimed",
        any(row.get("proof_id") == "RPG4472_6_verdict" and row.get("parent_signed") is False for row in proof_rows),
        "refinement gauge remains parent-unsigned",
    )
    add(
        "VAL4472_3_marker_hazard_present",
        any(row.get("proof_id") == "RPG4472_3_no_marker_extension" for row in proof_rows)
        and any(row.get("case_id") == "GVG4472_2_marker_extended_quotient" for row in matrix_rows),
        "marker extension hazard is explicitly retained",
    )
    add(
        "VAL4472_4_ellcell_rows_have_missing_markers",
        any("MISSING" in str(row.get("current_value")) for row in ell_rows) and all(row.get("valid_for_claim") is False for row in ell_rows),
        "ellcell normalization rows remain source-request/nonclaim",
    )
    add(
        "VAL4472_5_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4472_2_parent_gauge_signed" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR scalar closure",
    )
    add(
        "VAL4472_6_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, proof_rows, ell_rows, matrix_rows, gates, decisions, statuses, next_targets]
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
    add("VAL4472_7_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4472_8_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4472_9_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-314",
    )
    add(
        "VAL4472_10_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4472_11_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    proof_rows = refinement_gauge_proof_rows()
    ell_rows = ellcell_source_normalization_rows()
    matrix_rows = gauge_vs_grain_decision_rows()
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, proof_rows, ell_rows, matrix_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PROOF_CSV, proof_rows)
    write_csv(ELL_CSV, ell_rows)
    write_csv(MATRIX_CSV, matrix_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, proof_rows, ell_rows, matrix_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, proof_rows, ell_rows, matrix_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4472 Refinement Parameter Gauge Contract",
        "4472 writes the exact contract for treating `ell_cell` as gauge rather than a physical primitive grain: projective parent state space, cylindrical observables, descending action, no physical marker/source extension, no circular scale normalization, and no singular residue. The contract is not parent-signed today; marker/source extension is the sharpest live obstruction. Finite `ell_cell`, `xi_shape`, `N_EH`, `c2_visible`, visible `c_R2_cell`, and total `c_R2_eff` rows are staged for fallback.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4472 Packet Integration",
        "The private packet now treats quotient covariance as insufficient by itself. A covariant marker can descend to a quotient and still carry physical grain data, so the next derivation target is no-marker/source extension; otherwise the marker/grain branch must be source-normalized and bounded.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        PROOF_CSV,
        ELL_CSV,
        MATRIX_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, proof_rows, ell_rows, matrix_rows, gates, decisions, statuses, next_targets, csv_paths)
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
