from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from transfer_bound_pack_gate import (  # noqa: E402
    bound_input_pack_rows,
    claim_gate_rows,
    coupling_zero_audit_rows,
    decision_ledger_rows,
    deltak_allowance_summary_rows,
    no_cancellation_scorer_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4491"
CLAIM_ID = "L-333"
MARKER = "PPC4161_TRANSFER_BOUND_INPUT_PACK_OR_COUPLING_ZERO_THEOREM_4491"
PACKET_MARKER = "PPC4161_PACKET_TRANSFER_BOUND_INPUT_PACK_OR_COUPLING_ZERO_THEOREM_4491"
DECISION = "FIRST_NO_CANCELLATION_TRANSFER_BOUND_PACK_BUILT_MODERATE_COUPLING_SURVIVES_HUGE_COUPLING_FAILS_NONCLAIM"
NEXT_TARGET = "4492-Y5-R2FR-DeltaKTF-bound-or-coupling-product-parent-signature.md"

FORMAL_PATH = FORMAL / "507-PPC4161-transfer-bound-input-pack-or-coupling-zero-theorem.md"
DOC_PATH = POST / "4491-Y5-R2FR-transfer-bound-input-pack-or-coupling-zero-theorem.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4491_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4491_SOURCE_REGISTER.csv"
BOUND_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4491_TRANSFER_BOUND_INPUT_PACK.csv"
SCORE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4491_NO_CANCELLATION_SCORER.csv"
ALLOWANCE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4491_DELTAKTF_ALLOWANCE.csv"
ZERO_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4491_COUPLING_ZERO_AUDIT.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4491_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4491_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4491_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4491_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4491_DECISION.csv"

FORMAL_506 = FORMAL / "506-PPC4161-gluing-multiplier-parent-origin-or-PPN-transfer-matrix.md"
STATUS_4490 = SOURCE_DIR / "P8_Y5_R2FR_4490_STATUS.csv"
AMPLITUDE_4490 = SOURCE_DIR / "P8_Y5_R2FR_4490_SLIP_AMPLITUDE_ENVELOPES.csv"
TRANSFER_4490 = SOURCE_DIR / "P8_Y5_R2FR_4490_OBSERVABLE_TRANSFER_MATRIX.csv"
BOUND_4173 = SOURCE_DIR / "P8_Y5_R2FR_4173_SOURCE_BACKED_BOUND_TABLE.csv"
SOURCE_4173 = SOURCE_DIR / "P8_Y5_R2FR_4173_SOURCE_REGISTER.csv"
PPN_4085 = SOURCE_DIR / "P8_Y5_R2FR_4085_PPN_BOUND_TABLE.csv"
BOUND_2230 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2230_LOCAL_BOUND_LINKS.csv"
PHB_4487 = SOURCE_DIR / "P8_Y5_R2FR_4487_PH_SLIP_BOUND_ROWS.csv"
J2_4482 = SOURCE_DIR / "P8_Y5_R2FR_4482_UPSILON_J2_TRANSFER_SCORER.csv"
GREEN_4483 = SOURCE_DIR / "P8_Y5_R2FR_4483_RADIAL_GREEN_THEOREM.csv"
GATE_PATH = SCRIPT_DIR / "transfer_bound_pack_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4491_transfer_bound_input_pack_or_coupling_zero_theorem.py"

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
        ("SRC4491_00_formal506", FORMAL_506, "A_total_l2 <=", "4490 transfer matrix handoff."),
        ("SRC4491_01_status4490", STATUS_4490, "PPC4161_GLUING_MULTIPLIER_PARENT_ORIGIN_OR_PPN_TRANSFER_MATRIX_4490", "4490 status and next target."),
        ("SRC4491_02_amp4490", AMPLITUDE_4490, "SA4490_PSEL4489_0_smoothstep_minN4_candidate_c1e+09", "4490 slip amplitude rows."),
        ("SRC4491_03_transfer4490", TRANSFER_4490, "TM4490_1_J2_equivalent", "4490 transfer matrix rows."),
        ("SRC4491_04_bound4173", BOUND_4173, "B4173_14_orbit_combo", "4173 source-backed local bound table."),
        ("SRC4491_05_source4173", SOURCE_4173, "SRC4173_WEB_01_Cassini_gamma", "4173 web source strings."),
        ("SRC4491_06_ppn4085", PPN_4085, "BND4085_0_gamma_cassini", "4085 PPN bound table."),
        ("SRC4491_07_bound2230", BOUND_2230, "BL2230_R3_gamma", "2230 local bound links."),
        ("SRC4491_08_phb4487", PHB_4487, "PHB4487_solar_J2_half_range_proxy", "4487 tight P2 pressure row."),
        ("SRC4491_09_j24482", J2_4482, "J2T4482_2_corrected_J2eff", "4482 J2 transfer formula."),
        ("SRC4491_10_green4483", GREEN_4483, "RGT4483_2_l2_profile_selection", "4483 public r^-3 Green theorem."),
        ("SRC4491_11_gate", GATE_PATH, "def no_cancellation_scorer_rows", "4491 scorer helper."),
        ("SRC4491_12_generator", GENERATOR_PATH, 'CHECKPOINT = "4491"', "4491 generator script."),
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


def status_rows(allowance_rows: Sequence[Mapping[str, object]], score_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    one_e9 = [row for row in allowance_rows if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate" and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+09"]
    one_e11 = [row for row in allowance_rows if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate" and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+11"]
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "bound_rows": 5,
            "score_rows": len(score_rows),
            "smoothstep_1e9_max_fraction": one_e9[0]["max_fraction_of_bound"] if one_e9 else "",
            "smoothstep_1e9_all_pass": one_e9[0]["all_slip_only_smoke_rows_pass"] if one_e9 else "",
            "smoothstep_1e11_max_fraction": one_e11[0]["max_fraction_of_bound"] if one_e11 else "",
            "smoothstep_1e11_all_pass": one_e11[0]["all_slip_only_smoke_rows_pass"] if one_e11 else "",
            "local_GR_claim": False,
            "sharpest_open_clause": "A_DeltaKTF_surface_or_coupling_product_parent_signature",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4491_0",
            "target": NEXT_TARGET,
            "objective": "Either prove/bound A_DeltaKTF_surface in the same public metric lane, or parent-sign the coupling product s_K2*kappa_STF so the no-cancellation scorer becomes source-owned.",
            "derive_first": "DeltaKTF zero theorem from quotient/same-source projection, or s_K2*kappa_STF parent-signature/scale law",
            "fallback": "fill numeric beta_g00, beta_clock, beta_light and arena path/integration coefficients",
            "risk": "using slip-only smoke rows as a local-GR pass while DeltaKTF or beta/path coefficients remain live",
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
            "proof_result": "no exact coupling or DeltaKTF zero theorem was found in this pass",
            "fallback_result": "first numeric no-cancellation transfer-bound pack computes A_DeltaKTF allowance for J2, PPN-gamma, light-time, clock and orbital proxy rows",
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
        "claim": "4491 builds the first numeric no-cancellation transfer-bound pack for the slip/DeltaKTF branch: moderate 1e9 coupling survives slip-only smoke rows, while 1e11 fails the tight J2 proxy; no local-GR claim is promoted.",
        "current_evidence": "4491 source register, transfer-bound input pack, no-cancellation scorer, DeltaKTF allowance rows, coupling-zero audit, claim gates, decision/status/next CSVs and validation.",
        "status": "private_numeric_transfer_bound_pack_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "treating slip-only smoke compatibility as a public local-GR/J2/PPN pass before DeltaKTF, beta/path coefficients and coupling ownership close.",
        "sector": "local_gr_newton_r10_scalar_source_coupling",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "A_DeltaKTF_surface, s_K2*kappa_STF, arena beta coefficients and path/integration factors remain unsigned",
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
    bound_rows: Sequence[Mapping[str, object]],
    score_rows: Sequence[Mapping[str, object]],
    allowance_rows: Sequence[Mapping[str, object]],
    zero_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    display_scores = list(score_rows)[:20]
    return f"""# 507 PPC4161 - Transfer Bound Input Pack Or Coupling Zero Theorem

Private checkpoint: `{CHECKPOINT}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Generated UTC: `{STAMP}`

## Result

4491 does not find a parent-owned exact zero for `s_K2*kappa_STF` or `A_DeltaKTF_surface`. So the route moves to the fallback properly: a numeric no-cancellation transfer-bound scorer.

The scoring rule is:

```text
A_total_l2 <= |A_slip_surface| + |A_DeltaKTF_surface|
pass only if |A_slip_surface| + |A_DeltaKTF_surface| <= arena_bound
```

This forbids hiding one lane behind another by cancellation. Under the first beta=1, surface-normalized smoke scorer, the smoothstep `|s_K2*kappa_STF|=1e9` row survives all proxy rows, but `1e11` fails the tight J2 surface proxy. That is useful: the scorer now rejects too-large coupling products instead of merely listing missing inputs.

This is still not a local-GR claim. It assumes `A_DeltaKTF=0` for the slip-only smoke pass, and it still needs parent-owned coupling, `DeltaKTF` projection, and arena beta/path coefficients.

## Transfer Bound Input Pack

{table(bound_rows)}

## No-Cancellation Scorer Rows

First 20 rows shown here; full table is in `{SCORE_CSV}`.

{table(display_scores)}

## DeltaKTF Allowance Summary

{table(allowance_rows)}

## Coupling / Zero Audit

{table(zero_rows)}

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
    bound_rows: Sequence[Mapping[str, object]],
    score_rows: Sequence[Mapping[str, object]],
    allowance_rows: Sequence[Mapping[str, object]],
    zero_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4491 Y5/R2FR - Transfer Bound Input Pack Or Coupling Zero Theorem

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

4491 turns the 4490 transfer matrix into numeric no-cancellation smoke rows. It records bounds, scores slip-only finite coupling cells, computes the remaining allowed `A_DeltaKTF_surface`, and keeps all rows private/nonclaim.

## Bounds And Allowances

{table(bound_rows)}

{table(allowance_rows)}

## Zero Audit

{table(zero_rows)}

## Gates And Decisions

{table(gates)}

{table(ledger)}

{table(statuses)}

{table(next_targets)}

{table(decisions)}

## Full Score Table

{table(score_rows)}

## Sources

{table(sources)}
"""


def validate(
    sources: Sequence[Mapping[str, object]],
    bound_rows: Sequence[Mapping[str, object]],
    score_rows: Sequence[Mapping[str, object]],
    allowance_rows: Sequence[Mapping[str, object]],
    zero_rows: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    validations: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False})

    one_e9 = [row for row in allowance_rows if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate" and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+09"]
    one_e11 = [row for row in allowance_rows if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate" and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+11"]
    add("VAL4491_0_sources_exist_and_needles_found", all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources), "every cited source path exists and its needle is found")
    add("VAL4491_1_bound_rows_numeric_positive", len(bound_rows) >= 5 and all(float(row["bound_on_A_total_l2"]) > 0 for row in bound_rows), "all transfer-bound rows are positive numeric thresholds")
    add("VAL4491_2_score_rows_written", len(score_rows) >= 40, f"{len(score_rows)} no-cancellation score rows")
    add("VAL4491_3_allowance_rows_written", len(allowance_rows) >= 9, f"{len(allowance_rows)} DeltaKTF allowance rows")
    add("VAL4491_4_1e9_survives_smoke", bool(one_e9) and str(one_e9[0].get("all_slip_only_smoke_rows_pass")).lower() == "true", "smoothstep 1e9 survives all proxy rows if DeltaKTF=0")
    add("VAL4491_5_1e11_fails_smoke", bool(one_e11) and str(one_e11[0].get("all_slip_only_smoke_rows_pass")).lower() == "false", "smoothstep 1e11 fails at least one proxy row")
    add("VAL4491_6_zero_audit_written", len(zero_rows) >= 5 and any(row.get("quantity") == "A_DeltaKTF_surface" for row in zero_rows), "coupling and DeltaKTF zero audit exists")
    add("VAL4491_7_claim_gates_block_promotion", all(str(row.get("claim_allowed")).lower() == "false" for row in gates), "claim gates block promotion")
    add("VAL4491_8_status_local_GR_false", bool(statuses) and str(statuses[0].get("local_GR_claim")).lower() == "false", "local_GR_claim remains false")
    add("VAL4491_9_next_target_selected", bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET and bool(ledger), NEXT_TARGET)
    add(
        "VAL4491_10_all_generated_rows_nonclaim",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, bound_rows, score_rows, allowance_rows, zero_rows, gates, ledger, statuses, next_targets]
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
    add("VAL4491_11_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4491_12_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add("VAL4491_13_claim_register_updated", any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "claims register contains L-333")
    add("VAL4491_14_spine_and_packet_updated", MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH), "spine and packet contain 4491 markers")
    add("VAL4491_15_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    bound_rows = bound_input_pack_rows()
    score_rows = no_cancellation_scorer_rows(read_csv(AMPLITUDE_4490), bound_rows)
    allowance_rows = deltak_allowance_summary_rows(score_rows)
    zero_rows = coupling_zero_audit_rows()
    ledger = decision_ledger_rows(NEXT_TARGET, allowance_rows)
    gates = claim_gate_rows(sources, bound_rows, score_rows, allowance_rows, zero_rows)
    statuses = status_rows(allowance_rows, score_rows)
    next_targets = next_rows()
    decisions = decision_row()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(BOUND_INPUT_CSV, bound_rows)
    write_csv(SCORE_CSV, score_rows)
    write_csv(ALLOWANCE_CSV, allowance_rows)
    write_csv(ZERO_AUDIT_CSV, zero_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)
    write_csv(DECISION_CSV, decisions)

    write_text(FORMAL_PATH, formal_body(sources, bound_rows, score_rows, allowance_rows, zero_rows, ledger, gates, statuses, next_targets, decisions))
    write_text(DOC_PATH, post_body(sources, bound_rows, score_rows, allowance_rows, zero_rows, ledger, gates, statuses, next_targets, decisions))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4491 Transfer Bound Input Pack Or Coupling Zero Theorem",
        "4491 builds the first numeric no-cancellation scorer for the slip/`DeltaKTF` branch. It maps source-backed/local bound rows to `A_total_l2` thresholds, computes remaining `A_DeltaKTF_surface` allowance, shows the smoothstep `1e9` coupling survives slip-only smoke rows, and shows `1e11` fails the tight J2 proxy. All rows remain nonclaim until coupling ownership, `DeltaKTF`, beta/path coefficients and parent selection close.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4491 Packet Integration",
        "The packet now has a numeric no-cancellation transfer-bound smoke scorer. The next hard fork is no longer vague: either bound/prove zero for `A_DeltaKTF_surface`, or parent-sign the coupling product `s_K2*kappa_STF` and the arena beta/path coefficients.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        BOUND_INPUT_CSV,
        SCORE_CSV,
        ALLOWANCE_CSV,
        ZERO_AUDIT_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    validations = validate(sources, bound_rows, score_rows, allowance_rows, zero_rows, gates, ledger, statuses, next_targets, csv_paths)
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
