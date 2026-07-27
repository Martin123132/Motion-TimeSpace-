from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from gluing_origin_transfer_gate import (  # noqa: E402
    claim_gate_rows,
    constrained_variation_rows,
    finite_action_theorem_rows,
    observable_transfer_matrix_rows,
    parent_decision_rows,
    read_csv,
    slip_amplitude_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4490"
CLAIM_ID = "L-332"
MARKER = "PPC4161_GLUING_MULTIPLIER_PARENT_ORIGIN_OR_PPN_TRANSFER_MATRIX_4490"
PACKET_MARKER = "PPC4161_PACKET_GLUING_MULTIPLIER_PARENT_ORIGIN_OR_PPN_TRANSFER_MATRIX_4490"
DECISION = "FINITE_ACTION_C1_DOMAIN_REACTION_DERIVED_TRANSFER_MATRIX_STAGED_NONCLAIM"
NEXT_TARGET = "4491-Y5-R2FR-transfer-bound-input-pack-or-coupling-zero-theorem.md"

FORMAL_PATH = FORMAL / "506-PPC4161-gluing-multiplier-parent-origin-or-PPN-transfer-matrix.md"
DOC_PATH = POST / "4490-Y5-R2FR-gluing-multiplier-parent-origin-or-PPN-transfer-matrix.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4490_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4490_SOURCE_REGISTER.csv"
FINITE_ACTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4490_FINITE_ACTION_C1_THEOREM.csv"
CONSTRAINED_VARIATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4490_CONSTRAINED_VARIATION_GLUE_ORIGIN.csv"
SLIP_AMPLITUDE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4490_SLIP_AMPLITUDE_ENVELOPES.csv"
TRANSFER_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4490_OBSERVABLE_TRANSFER_MATRIX.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4490_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4490_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4490_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4490_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4490_DECISION.csv"

FORMAL_505 = FORMAL / "505-PPC4161-parent-profile-selection-or-PPN-transfer-upgrade.md"
STATUS_4489 = SOURCE_DIR / "P8_Y5_R2FR_4489_STATUS.csv"
PROFILE_4489 = SOURCE_DIR / "P8_Y5_R2FR_4489_PROFILE_SELECTION_ROWS.csv"
GLUE_3194 = SOURCE_DIR / "P8_Y5_R2FR_3194_C1_GLUING_MULTIPLIER_DERIVATION.csv"
SOL_3194 = SOURCE_DIR / "P8_Y5_R2FR_3194_MULTIPLIER_SOLUTIONS.csv"
NORM_4487 = SOURCE_DIR / "P8_Y5_R2FR_4487_CHIH_PH_NORMALIZATION.csv"
PHG_4488 = SOURCE_DIR / "P8_Y5_R2FR_4488_PH_PROFILE_GATE.csv"
J2_4482 = SOURCE_DIR / "P8_Y5_R2FR_4482_UPSILON_J2_TRANSFER_SCORER.csv"
GREEN_4483 = SOURCE_DIR / "P8_Y5_R2FR_4483_RADIAL_GREEN_THEOREM.csv"
PI_4484 = SOURCE_DIR / "P8_Y5_R2FR_4484_PIJ2METRIC_TRANSFER_ROWS.csv"
PT_3190 = SOURCE_DIR / "P8_Y5_R2FR_3190_PPN_TRANSFER_UPGRADE_CONTRACT.csv"
GATE_PATH = SCRIPT_DIR / "gluing_origin_transfer_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4490_gluing_multiplier_parent_origin_or_PPN_transfer_matrix.py"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4490_00_formal505", FORMAL_505, "lambda_i=-[Pi_i]", "4489 gluing mechanism handoff."),
        ("SRC4490_01_status4489", STATUS_4489, "PPC4161_PARENT_PROFILE_SELECTION_OR_PPN_TRANSFER_UPGRADE_4489", "4489 status and next target."),
        ("SRC4490_02_profile4489", PROFILE_4489, "PSEL4489_1_min_N4_exact_EL_scan", "4489 exact profile selection rows."),
        ("SRC4490_03_glue3194", GLUE_3194, "GLUE3194_5_multiplier_solution", "3194 multiplier derivation."),
        ("SRC4490_04_solution3194", SOL_3194, "GLUE3194_1_balanced_Fpp_jump", "3194 multiplier solution rows."),
        ("SRC4490_05_chi4487", NORM_4487, "NORM4487_2_chiH_natural", "4487 chiH normalization."),
        ("SRC4490_06_ph4488", PHG_4488, "PG4488_1_absolute_envelope", "4488 PH envelope law."),
        ("SRC4490_07_j24482", J2_4482, "J2T4482_2_corrected_J2eff", "4482 J2 transfer scorer."),
        ("SRC4490_08_green4483", GREEN_4483, "RGT4483_2_l2_profile_selection", "4483 exterior r^-3 Green theorem."),
        ("SRC4490_09_pi4484", PI_4484, "PI4484_2_finite_source_functional", "4484 public metric transfer functional."),
        ("SRC4490_10_pt3190", PT_3190, "PT3190_0_observable_transfer", "3190 transfer-upgrade contract."),
        ("SRC4490_11_gate", GATE_PATH, "def finite_action_theorem_rows", "4490 helper gate."),
        ("SRC4490_12_generator", GENERATOR_PATH, 'CHECKPOINT = "4490"', "4490 generator script."),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        line_number = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_kind": "local",
                "source_ref": str(path),
                "local_path_exists": exists,
                "needle": needle,
                "needle_found": bool(line_number),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def status_rows(amplitude_rows: Sequence[Mapping[str, object]], transfer_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    one_e9_rows = [row for row in amplitude_rows if row.get("abs_sK2_kappaSTF") == "1.000000000000000e+09" and row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate"]
    fraction_1e9 = one_e9_rows[0]["tight_pressure_fraction"] if one_e9_rows else ""
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "finite_action_C1_origin": "conditional_derived",
            "lambda_origin": "lambda_i=-[Pi_i]_from_domain_reaction",
            "smoothstep_1e9_tight_pressure_fraction": fraction_1e9,
            "transfer_matrix_rows": len(transfer_rows),
            "local_GR_claim": False,
            "sharpest_open_clause": "parent_selects_D2_sector_plus_coupling_product_and_numeric_transfer_bounds",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4490_0",
            "target": NEXT_TARGET,
            "objective": "Fill the first numeric no-cancellation transfer-bound pack for J2/orbital/light-time/clock/PPN rows, or prove the source coupling product s_K2*kappa_STF or the DeltaKTF lane is zero.",
            "derive_first": "parent selection of the D2 curvature sector or exact s_K2*kappa_STF=0 / DeltaKTF=0 theorem",
            "fallback": "source-backed beta_g00, beta_space, beta_clock, beta_light, A_DeltaKTF and arena-bound rows",
            "risk": "promoting symbolic transfer rows as empirical pass before coefficients and bound rows are sourced",
            "valid_for_claim": False,
        }
    ]


def decision_row() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "proof_result": "finite-action H2/D2 domain conditionally derives [F]=[F']=0 and recovers lambda_i=-[Pi_i] as constrained-domain reaction forces",
            "fallback_result": "symbolic no-cancellation transfer matrix staged for J2, clocks, light-time, PPN-STF and orbital acceleration",
            "claim_status": "private_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def append_section_once(path: Path, marker: str, title: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    addition = f"\n\n## {title}\n\nMarker: `{marker}`  \n{body.strip()}\n"
    write_text(path, existing.rstrip() + addition + "\n")


def update_claims_register() -> None:
    rows = read_csv(CLAIMS_PATH)
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r10_scalar_source_coupling",
        "claim": "4490 conditionally derives the C1 gluing multiplier origin from finite-action D2/H2 regularity and stages a no-cancellation observable transfer matrix, while keeping local-GR/J2/PPN claims blocked.",
        "current_evidence": "4490 source register, finite-action C1 theorem rows, constrained-variation gluing-origin rows, slip-amplitude envelopes, observable transfer matrix, claim gates, decision/status/next CSVs and validation.",
        "status": "private_conditional_gluing_origin_and_transfer_matrix_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "treating conditional finite-action domain reaction or symbolic transfer coefficients as parent-signed empirical local-GR pass.",
        "sector": "local_gr_newton_r10_scalar_source_coupling",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "parent D2-sector selection, coupling product, DeltaKTF leakage and numeric transfer-bound rows remain unsigned",
    }
    replaced = False
    for index, row in enumerate(rows):
        if row.get("claim_id") == CLAIM_ID:
            rows[index] = new_row
            replaced = True
            break
    if not replaced:
        rows.append(new_row)
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    theorem_rows: Sequence[Mapping[str, object]],
    variation_rows: Sequence[Mapping[str, object]],
    amplitude_rows: Sequence[Mapping[str, object]],
    transfer_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 506 PPC4161 - Gluing Multiplier Parent Origin Or PPN Transfer Matrix

Private checkpoint: `{CHECKPOINT}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Generated UTC: `{STAMP}`

## Result

4490 takes the leap at the interface problem instead of circling it. The clean result is conditional but real:

```text
J[F]=integral x^4(D2[F])^2 dx
D2[F]=(2/5)F''+2F'/x+6F/(5x^2)
finite J on an internal interface => [F]=0 and [F']=0
J_c=J+sum_interfaces(lambda_0[F]+lambda_1[F'])
delta J_c => lambda_i=-[Pi_i]
```

So the `C1` gluing multipliers are not merely hand-added closure knobs if the parent local profile sector is a finite-action `D2` curvature sector: they are the reaction forces of the finite-action domain constraints. That is the strongest current derivation of the gluing mechanism.

The limit is equally explicit: this does not prove that the global MTS parent action selects this `D2` sector, nor does it source `s_K2*kappa_STF`, `DeltaK_TF`, or the metric/readout split coefficients. Therefore no local-GR, J2, PPN, clock, orbital, or R10 claim is promoted.

The fallback is now a usable transfer matrix rather than a pressure-proxy fog bank. Future tests can fill the missing numeric coefficients row by row without cancellation games.

## Finite-Action C1 Theorem

{table(theorem_rows)}

## Constrained Variation And Gluing Origin

{table(variation_rows)}

## Slip Amplitude Envelopes

{table(amplitude_rows)}

## Observable Transfer Matrix

{table(transfer_rows)}

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
    variation_rows: Sequence[Mapping[str, object]],
    amplitude_rows: Sequence[Mapping[str, object]],
    transfer_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4490 Y5/R2FR - Gluing Multiplier Parent Origin Or PPN Transfer Matrix

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

4490 derives a conditional origin for the interface multipliers: finite action in the `D2` curvature profile sector forces `C1` gluing, and constrained variation recovers `lambda_i=-[Pi_i]`. It also stages the no-cancellation transfer matrix needed to turn the slip branch into J2/orbital/light-time/clock/PPN rows later.

## Proof Rows

{table(theorem_rows)}

{table(variation_rows)}

## Transfer Rows

{table(amplitude_rows)}

{table(transfer_rows)}

## Gates And Decisions

{table(gates)}

{table(ledger)}

{table(statuses)}

{table(next_targets)}

{table(decisions)}

## Sources

{table(sources)}
"""


def validate(
    sources: Sequence[Mapping[str, object]],
    theorem_rows: Sequence[Mapping[str, object]],
    variation_rows: Sequence[Mapping[str, object]],
    amplitude_rows: Sequence[Mapping[str, object]],
    transfer_rows: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    validations: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False})

    add("VAL4490_0_sources_exist_and_needles_found", all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources), "every cited source path exists and its needle is found")
    add("VAL4490_1_finite_action_C1_theorem_written", any(row.get("theorem_id") == "FA4490_1_C1_constraints" for row in theorem_rows), "finite-action route to [F]=[F']=0 exists")
    add("VAL4490_2_lambda_origin_written", any(row.get("variation_id") == "CV4490_2_multiplier_solution" for row in variation_rows), "lambda_i=-[Pi_i] recovered")
    add("VAL4490_3_3194_solution_rows_imported", len([row for row in variation_rows if str(row.get("variation_id", "")).startswith("CV4490_lambda_")]) >= 3, "3194 multiplier solution rows carried")
    add("VAL4490_4_slip_amplitudes_written", len(amplitude_rows) >= 10 and any(row.get("abs_sK2_kappaSTF") == "1.000000000000000e+09" for row in amplitude_rows), "profile/coupling amplitude envelopes exist")
    add("VAL4490_5_transfer_matrix_written", len(transfer_rows) >= 6 and any(row.get("transfer_id") == "TM4490_3_light_time" for row in transfer_rows), "arena transfer matrix exists")
    add("VAL4490_6_claim_gates_block_promotion", all(str(row.get("claim_allowed")).lower() == "false" for row in gates), "claim gates block promotion")
    add("VAL4490_7_decision_and_next_target", bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET and bool(ledger), NEXT_TARGET)
    add("VAL4490_8_status_local_GR_false", bool(statuses) and str(statuses[0].get("local_GR_claim")).lower() == "false", "local_GR_claim remains false")
    add(
        "VAL4490_9_all_generated_rows_nonclaim",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, theorem_rows, variation_rows, amplitude_rows, transfer_rows, gates, ledger, statuses, next_targets]
            for row in group
        ),
        "all generated rows are private/nonclaim",
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
    add("VAL4490_10_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4490_11_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add("VAL4490_12_claim_register_updated", any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "claims register contains L-332")
    add("VAL4490_13_spine_and_packet_updated", MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH), "spine and packet contain 4490 markers")
    add("VAL4490_14_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    theorem_rows = finite_action_theorem_rows()
    variation_rows = constrained_variation_rows(read_csv(SOL_3194))
    amplitude_rows = slip_amplitude_rows(read_csv(PROFILE_4489))
    transfer_rows = observable_transfer_matrix_rows()
    ledger = parent_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, theorem_rows, variation_rows, amplitude_rows, transfer_rows)
    statuses = status_rows(amplitude_rows, transfer_rows)
    next_targets = next_rows()
    decisions = decision_row()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(FINITE_ACTION_CSV, theorem_rows)
    write_csv(CONSTRAINED_VARIATION_CSV, variation_rows)
    write_csv(SLIP_AMPLITUDE_CSV, amplitude_rows)
    write_csv(TRANSFER_MATRIX_CSV, transfer_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)
    write_csv(DECISION_CSV, decisions)

    write_text(FORMAL_PATH, formal_body(sources, theorem_rows, variation_rows, amplitude_rows, transfer_rows, ledger, gates, statuses, next_targets, decisions))
    write_text(DOC_PATH, post_body(sources, theorem_rows, variation_rows, amplitude_rows, transfer_rows, ledger, gates, statuses, next_targets, decisions))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4490 Gluing Multiplier Parent Origin Or Transfer Matrix",
        "4490 conditionally derives the gluing multiplier origin: finite action in the `D2` curvature profile sector forces `[F]=[F']=0`, and constrained variation gives `lambda_i=-[Pi_i]`. It also stages a no-cancellation transfer matrix for J2, clocks, light-time, PPN-STF and orbital acceleration. Local-GR remains nonclaim until parent D2-sector selection, coupling product, `DeltaK_TF`, split coefficients and numeric arena bounds close.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4490 Packet Integration",
        "The packet now has a conditional finite-action origin for the C1 interface multipliers and a symbolic transfer matrix. This narrows the next job to source/coupling proof or numeric no-cancellation transfer-bound inputs.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        FINITE_ACTION_CSV,
        CONSTRAINED_VARIATION_CSV,
        SLIP_AMPLITUDE_CSV,
        TRANSFER_MATRIX_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    validations = validate(sources, theorem_rows, variation_rows, amplitude_rows, transfer_rows, gates, ledger, statuses, next_targets, csv_paths)
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
