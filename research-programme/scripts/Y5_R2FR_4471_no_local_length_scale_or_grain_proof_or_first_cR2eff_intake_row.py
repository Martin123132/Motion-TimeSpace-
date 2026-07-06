from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from no_local_grain_cr2_gate import (  # noqa: E402
    claim_gate_rows,
    continuum_scaling_rows,
    decision_rows as gate_decision_rows,
    first_cr2eff_intake_rows,
    no_grain_theorem_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4471"
CLAIM_ID = "L-313"
MARKER = "PPC4161_NO_LOCAL_LENGTH_SCALE_OR_GRAIN_PROOF_OR_FIRST_CR2EFF_INTAKE_4471"
PACKET_MARKER = "PPC4161_PACKET_NO_LOCAL_LENGTH_SCALE_OR_GRAIN_PROOF_OR_FIRST_CR2EFF_INTAKE_4471"
DECISION = "VISIBLE_CELL_CR2_NO_GRAIN_THEOREM_DERIVED_CONDITIONALLY_PARENT_GRAIN_SIGNATURE_UNSIGNED_FIRST_CR2EFF_INTAKE_STAGED_NONCLAIM"
NEXT_TARGET = "4472-Y5-R2FR-refinement-parameter-gauge-proof-or-ellcell-source-normalization.md"

FORMAL_PATH = FORMAL / "487-PPC4161-no-local-length-scale-or-grain-proof-or-first-cR2eff-intake-row.md"
DOC_PATH = POST / "4471-Y5-R2FR-no-local-length-scale-or-grain-proof-or-first-cR2eff-intake-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4471_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4471_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4471_NO_GRAIN_THEOREM.csv"
SCALING_CSV = SOURCE_DIR / "P8_Y5_R2FR_4471_CONTINUUM_SCALING_DERIVATION.csv"
INTAKE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4471_FIRST_CR2EFF_INTAKE_ROW.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4471_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4471_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4471_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4471_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4471_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "no_local_grain_cr2_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4471_no_local_length_scale_or_grain_proof_or_first_cR2eff_intake_row.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4470 = SOURCE_DIR / "P8_Y5_R2FR_4470_NEXT_TARGET.csv"
FORMAL_486 = FORMAL / "486-PPC4161-parent-two-derivative-no-extra-mode-selector-signature-or-cR2-coefficient-intake.md"
SIGNATURE_4470 = SOURCE_DIR / "P8_Y5_R2FR_4470_PARENT_SELECTOR_SIGNATURE_AUDIT.csv"
INTAKE_4470 = SOURCE_DIR / "P8_Y5_R2FR_4470_FINITE_COEFFICIENT_INTAKE_REQUEST.csv"
FORMAL_476 = FORMAL / "476-PPC4161-parent-refinement-gauge-signature-or-visible-c2-finite-row.md"
FORMAL_477 = FORMAL / "477-PPC4161-connection-hinge-refinement-owner-or-c2-scalaron-map.md"
FORMAL_479 = FORMAL / "479-PPC4161-parent-kappa-scale-law-or-calibrated-G-residual-runner.md"
SCALING_1823 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1823_DEFICIT_CONTINUUM_SCALING_AUDIT.csv"
POST_1343 = POST / "1343-Y5-R10-RAB-R2FR-parent-coefficient-zero-signature-or-finite-scalar-map-fill.md"


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
            "source_id": "SRC4471_00_next4470",
            "ref": NEXT_4470,
            "needle": "4471-Y5-R2FR-no-local-length-scale-or-grain-proof-or-first-cR2eff-intake-row.md",
            "role": "4470 selected the no-local-grain/cR2 intake target.",
        },
        {
            "source_id": "SRC4471_01_formal486_result",
            "ref": FORMAL_486,
            "needle": "The decisive open clause is the no-local-length/no-grain theorem",
            "role": "4470 identifies no-grain as the decisive open clause.",
        },
        {
            "source_id": "SRC4471_02_signature4470",
            "ref": SIGNATURE_4470,
            "needle": "SIG4470_2_no_local_length_scale_or_grain",
            "role": "machine-readable no-grain selector clause.",
        },
        {
            "source_id": "SRC4471_03_intake4470",
            "ref": INTAKE_4470,
            "needle": "REQ4470_2_cR2_eff_from_grain",
            "role": "machine-readable cR2_eff grain intake row.",
        },
        {
            "source_id": "SRC4471_04_refinement_physical_grain",
            "ref": FORMAL_476,
            "needle": "DICH4460_2_physical_grain_cutoff",
            "role": "physical-grain finite fallback branch.",
        },
        {
            "source_id": "SRC4471_05_refinement_cell_scale",
            "ref": FORMAL_476,
            "needle": "FC24460_1_cell_scale",
            "role": "ell_cell/shape/EH normalization finite row.",
        },
        {
            "source_id": "SRC4471_06_scalaron_map",
            "ref": FORMAL_477,
            "needle": "SM4461_1_c2_to_cR2",
            "role": "c2 to c_R2_eff map.",
        },
        {
            "source_id": "SRC4471_07_kappa_cell_scale",
            "ref": FORMAL_479,
            "needle": "KSL4463_3_cell_or_refinement_scale",
            "role": "cell/refinement scale route for kappa and circularity guard.",
        },
        {
            "source_id": "SRC4471_08_dimensionful_nogo",
            "ref": FORMAL_479,
            "needle": "KSL4463_5_dimensionful_no_go",
            "role": "dimensionful scale no-go guard.",
        },
        {
            "source_id": "SRC4471_09_scaling_linear",
            "ref": SCALING_1823,
            "needle": "DCS1823_0_linear",
            "role": "older continuum scaling row for linear EH term.",
        },
        {
            "source_id": "SRC4471_10_scaling_quadratic",
            "ref": SCALING_1823,
            "needle": "DCS1823_1_quadratic",
            "role": "older continuum scaling row for quadratic visible c2 term.",
        },
        {
            "source_id": "SRC4471_11_scaling_zero_limit",
            "ref": SCALING_1823,
            "needle": "DCS1823_2_zero_limit",
            "role": "older row distinguishing suppression from theorem-zero.",
        },
        {
            "source_id": "SRC4471_12_scaling_renormalized",
            "ref": SCALING_1823,
            "needle": "DCS1823_3_renormalized",
            "role": "older row retaining renormalized/hidden residue.",
        },
        {
            "source_id": "SRC4471_13_hidden_residue1343",
            "ref": POST_1343,
            "needle": "LAW1343_0_quadratic_parent_block",
            "role": "hidden-mode c_R2_eff coefficient law.",
        },
        {
            "source_id": "SRC4471_14_gate",
            "ref": GATE_PATH,
            "needle": "def no_grain_theorem_rows",
            "role": "4471 no-local-grain gate.",
        },
        {
            "source_id": "SRC4471_15_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4471"',
            "role": "4471 generator script.",
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
            "derivation_result": "visible cell R2 term scales as ell_cell^2 and vanishes only when ell is a gauge refinement with smooth c2 and no singular residue",
            "parent_status": "no physical primitive grain/refinement gauge/no singular running/no hidden residue are not signed together",
            "finite_row_result": "first c_R2_eff intake row now has visible cell, total residue and observable projection slots",
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
            "visible_cell_scaling": "derived",
            "no_grain_zero_status": "conditional_parent_unsigned",
            "total_cR2_status": "retained_due_to_hidden_bare_measure_boundary_residue",
            "finite_intake_status": "first_row_staged_missing_values",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4471_0",
            "target": NEXT_TARGET,
            "objective": "Prove the refinement parameter is gauge rather than a physical primitive grain, or source ell_cell/action-normalization as a finite residual input.",
            "derive_first": "construct parent quotient/refinement evidence that cell labels, subdivisions and ell are readout/gauge data with cylindrical observables",
            "fallback": "fill ell_cell, c2_visible, xi_shape and N_EH as explicit nonclaim coefficient-source rows",
            "risk": "using absence of a sourced scale as proof that no physical scale exists",
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
            "claim": "4471 derives the visible-cell no-grain scaling theorem: a quadratic cell deficit term contributes c_R2_cell proportional to ell_cell^2 and vanishes if ell is only gauge refinement with smooth c2 and no singular residue.",
            "current_evidence": "4471 source register, no-grain theorem rows, continuum scaling derivation, first c_R2_eff intake row, claim gates, decision/status/next CSVs and validation.",
            "status": "private_nonclaim_checkpoint",
            "next_test": NEXT_TARGET,
            "key_risk": "mistaking ell_cell missingness for a parent proof that no physical primitive grain exists.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "hidden bare/auxiliary/measure/boundary c_R2_eff terms survive even if visible cell-grain contribution vanishes",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    theorem_rows: Sequence[Mapping[str, object]],
    scaling_rows: Sequence[Mapping[str, object]],
    intake_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 487 PPC4161 - No Local Length Scale Or Grain Proof Or First `c_R2_eff` Intake Row

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4471 gets an actual theorem out of the no-grain route.

For a regular local hinge/cell description with cell size `ell`, the linear term scales as `sum A_h delta_h -> integral sqrt(-g) R`, while the quadratic visible term scales as `sum A_h delta_h^2 -> ell^2 integral sqrt(-g) R^2`. Therefore a visible cell/grain contribution has the form:

```text
c_R2_cell = xi_shape * c2_visible * ell_cell^2 / N_EH.
```

If `ell` is only a gauge/refinement parameter, `c2_visible` is smooth, and no singular counterterm or hidden residue is allowed, then the only refinement-cylindrical value is `c_R2_cell=0`. That is the real derivation gain.

But current MTS does not yet parent-sign the required no-physical-grain/refinement-gauge/no-singular-running/no-hidden-residue package. So 4471 does not claim local GR. It stages the exact first finite row instead: `c_R2_eff_total = c_R2_cell + c_bare + 0.5 B^T L^-1 B + c_measure + c_boundary`.

## No-Grain Theorem Rows

{table(theorem_rows)}

## Continuum Scaling Derivation

{table(scaling_rows)}

## First `c_R2_eff` Intake Row

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
    theorem_rows: Sequence[Mapping[str, object]],
    scaling_rows: Sequence[Mapping[str, object]],
    intake_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4471 Y5/R2FR - No Local Length Scale Or Grain Proof Or First `c_R2_eff` Intake Row

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

The no-grain route now has teeth: visible cell curvature-square response dies like `ell^2` if `ell` is gauge refinement. The remaining problem is not "maybe there is a missing number"; it is whether MTS parent-signs refinement-gauge/no-physical-grain and no hidden renormalized residue.

## No-Grain Theorem

{table(theorem_rows)}

## Scaling

{table(scaling_rows)}

## Finite Intake

{table(intake_rows)}

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
    scaling_rows: Sequence[Mapping[str, object]],
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
        "VAL4471_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4471_1_scaling_lemma_derived",
        any(row.get("theorem_id") == "NG4471_0_cell_scaling_lemma" and row.get("parent_signed") is True for row in theorem_rows),
        "cell scaling identity is derived as math",
    )
    add(
        "VAL4471_2_no_grain_not_overclaimed",
        any(row.get("theorem_id") == "NG4471_5_verdict" and row.get("parent_signed") is False for row in theorem_rows),
        "no-grain theorem remains parent-unsigned",
    )
    add(
        "VAL4471_3_visible_quadratic_scaling_present",
        any(row.get("scaling_id") == "SCL4471_1_quadratic_visible" for row in scaling_rows),
        "visible quadratic scaling row exists",
    )
    add(
        "VAL4471_4_total_residue_guard_present",
        any(row.get("theorem_id") == "NG4471_4_hidden_residue_guard" for row in theorem_rows)
        and any(row.get("intake_id") == "CR2I4471_2_total_effective_component" for row in intake_rows),
        "hidden/bare/measure/boundary residue guard is present",
    )
    add(
        "VAL4471_5_intake_has_missing_markers",
        any("MISSING" in str(row.get("current_value")) for row in intake_rows) and all(row.get("valid_for_claim") is False for row in intake_rows),
        "finite intake remains source-request/nonclaim with missing markers",
    )
    add(
        "VAL4471_6_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4471_2_no_grain_parent_signed" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR scalar closure",
    )
    add(
        "VAL4471_7_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, theorem_rows, scaling_rows, intake_rows, gates, decisions, statuses, next_targets]
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
    add("VAL4471_8_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4471_9_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4471_10_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-313",
    )
    add(
        "VAL4471_11_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4471_12_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    theorem_rows = no_grain_theorem_rows()
    scaling_rows = continuum_scaling_rows()
    intake_rows = first_cr2eff_intake_rows()
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, theorem_rows, scaling_rows, intake_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem_rows)
    write_csv(SCALING_CSV, scaling_rows)
    write_csv(INTAKE_CSV, intake_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, theorem_rows, scaling_rows, intake_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, theorem_rows, scaling_rows, intake_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4471 No-Grain Scaling Theorem",
        "4471 derives the visible-cell scaling result: `sum A_h delta_h^2` contributes `ell_cell^2 integral R^2`, so the visible `c_R2_cell` vanishes if `ell` is only gauge refinement with smooth `c2_visible` and no singular counterterm. This is not yet a local-GR claim because the parent no-physical-grain/no-hidden-residue package is unsigned. The first finite fallback row is now `c_R2_eff_total = xi_shape*c2_visible*ell_cell^2/N_EH + c_bare + 0.5 B^T L^-1 B + c_measure + c_boundary`.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4471 Packet Integration",
        "The private packet now treats `ell_cell` as the decisive fork: if it is gauge refinement, the visible cell `R^2` term dies; if it is physical or renormalized, `c_R2_eff` must be filled with explicit coefficient/source rows before R10/PPN/local-GR scoring.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        SCALING_CSV,
        INTAKE_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, theorem_rows, scaling_rows, intake_rows, gates, decisions, statuses, next_targets, csv_paths)
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
