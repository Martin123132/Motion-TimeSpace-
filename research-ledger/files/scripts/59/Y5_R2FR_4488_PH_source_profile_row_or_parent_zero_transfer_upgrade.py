from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from ph_source_profile_gate import (  # noqa: E402
    claim_gate_rows,
    decision_ledger_rows,
    margin_rows,
    profile_gate_rows,
    read_csv,
    smooth_profile_rows,
    transfer_status_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4488"
CLAIM_ID = "L-330"
MARKER = "PPC4161_PH_SOURCE_PROFILE_ROW_OR_PARENT_ZERO_TRANSFER_UPGRADE_4488"
PACKET_MARKER = "PPC4161_PACKET_PH_SOURCE_PROFILE_ROW_OR_PARENT_ZERO_TRANSFER_UPGRADE_4488"
DECISION = "PH_SMOOTH_SOURCE_PROFILE_GATE_AND_MARGIN_ROWS_FILLED_TRANSFER_PROXY_RETAINED_NONCLAIM"
NEXT_TARGET = "4489-Y5-R2FR-parent-profile-selection-or-PPN-transfer-upgrade.md"

FORMAL_PATH = FORMAL / "504-PPC4161-PH-source-profile-row-or-parent-zero-transfer-upgrade.md"
DOC_PATH = POST / "4488-Y5-R2FR-PH-source-profile-row-or-parent-zero-transfer-upgrade.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4488_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4488_SOURCE_REGISTER.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4488_PH_PROFILE_GATE.csv"
PROFILE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4488_SMOOTH_PROFILE_ROWS.csv"
MARGIN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4488_SMOOTH_PROFILE_MARGIN_ROWS.csv"
TRANSFER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4488_TRANSFER_STATUS.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4488_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4488_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4488_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4488_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4488_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "ph_source_profile_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4488_PH_source_profile_row_or_parent_zero_transfer_upgrade.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_503 = FORMAL / "503-PPC4161-Hessian-carrier-adoption-or-DeltaKTF-metric-response-bound.md"
NEXT_4487 = SOURCE_DIR / "P8_Y5_R2FR_4487_NEXT_TARGET.csv"
BOUND_4487 = SOURCE_DIR / "P8_Y5_R2FR_4487_PH_SLIP_BOUND_ROWS.csv"
NORM_4487 = SOURCE_DIR / "P8_Y5_R2FR_4487_CHIH_PH_NORMALIZATION.csv"
DOC_3187 = POST / "3187-Y5-R2FR-kappaSTF-cExt-source-profile-estimator-or-parent-zero-under-AX1090.md"
EST_3187 = SOURCE_DIR / "P8_Y5_R2FR_3187_PROFILE_ESTIMATOR_DERIVATION.csv"
ZERO_3187 = SOURCE_DIR / "P8_Y5_R2FR_3187_PARENT_ZERO_AUDIT.csv"
DOC_3188 = POST / "3188-Y5-R2FR-PH-source-profile-prior-grid-or-parent-coupling-zero-under-AX1090.md"
CRIT_3188 = SOURCE_DIR / "P8_Y5_R2FR_3188_CRITICAL_PROFILE_NORM_ROWS.csv"
GRID_3188 = SOURCE_DIR / "P8_Y5_R2FR_3188_ABSOLUTE_ENVELOPE_PRIOR_GRID.csv"
CZ_3188 = SOURCE_DIR / "P8_Y5_R2FR_3188_COUPLING_ZERO_AUDIT.csv"
DOC_3189 = POST / "3189-Y5-R2FR-live-source-profile-row-or-transfer-bound-upgrade-under-AX1090.md"
PROFILES_3189 = SOURCE_DIR / "P8_Y5_R2FR_3189_SMOOTH_PROFILE_FAMILY.csv"
MARGINS_3189 = SOURCE_DIR / "P8_Y5_R2FR_3189_SMOOTH_PROFILE_MARGIN_ROWS.csv"
TRANSFER_3189 = SOURCE_DIR / "P8_Y5_R2FR_3189_TRANSFER_BOUND_STATUS.csv"


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


def csv_lookup(path: Path, key: str, key_value: str, column: str) -> str:
    for row in read_csv(path):
        if row.get(key) == key_value:
            return row[column]
    raise KeyError(f"missing {key}={key_value} in {path}")


def tight_ph_bound() -> float:
    return float(csv_lookup(BOUND_4487, "bound_name", "solar_J2_half_range_proxy", "P_H_bound_from_slip"))


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4488_00_next4487", "ref": NEXT_4487, "needle": "4488-Y5-R2FR-PH-source-profile-row-or-parent-zero-transfer-upgrade.md", "role": "4487 selected PH source profile/transfer upgrade."},
        {"source_id": "SRC4488_01_formal503", "ref": FORMAL_503, "needle": "P_H = -(5/4) s_K2 kappa_STF I4_D2", "role": "4487 source-product frontier."},
        {"source_id": "SRC4488_02_bound4487", "ref": BOUND_4487, "needle": "solar_J2_half_range_proxy", "role": "4487 tight PH pressure row."},
        {"source_id": "SRC4488_03_norm4487", "ref": NORM_4487, "needle": "NORM4487_3_profile_estimator", "role": "4487 PH estimator normalization."},
        {"source_id": "SRC4488_04_doc3187", "ref": DOC_3187, "needle": "N4_D2", "role": "3187 absolute profile envelope."},
        {"source_id": "SRC4488_05_est3187", "ref": EST_3187, "needle": "EST3187_2_absolute_norm_envelope", "role": "3187 machine absolute envelope."},
        {"source_id": "SRC4488_06_zero3187", "ref": ZERO_3187, "needle": "ZERO3187_3_transition_cancellation", "role": "3187 zero route audit."},
        {"source_id": "SRC4488_07_doc3188", "ref": DOC_3188, "needle": "|s_K2 kappa_STF| N4_D2 <= (4/5) B_PH", "role": "3188 profile pressure gate."},
        {"source_id": "SRC4488_08_crit3188", "ref": CRIT_3188, "needle": "CRIT3188_solar_J2_half_range_proxy_c1e+00", "role": "3188 critical profile norm rows."},
        {"source_id": "SRC4488_09_grid3188", "ref": GRID_3188, "needle": "GRID3188_solar_J2_half_range_proxy_c1e+12_n1e+00", "role": "3188 prior grid."},
        {"source_id": "SRC4488_10_cz3188", "ref": CZ_3188, "needle": "CZ3188_3_no_zero_order_one_profile", "role": "3188 coupling zero audit."},
        {"source_id": "SRC4488_11_doc3189", "ref": DOC_3189, "needle": "N4_D2", "role": "3189 smooth profile result."},
        {"source_id": "SRC4488_12_profiles3189", "ref": PROFILES_3189, "needle": "SP3189_width_0.40", "role": "3189 smooth profile rows."},
        {"source_id": "SRC4488_13_margins3189", "ref": MARGINS_3189, "needle": "PM3189_SP3189_width_0.40_c1e+09", "role": "3189 smooth profile margin rows."},
        {"source_id": "SRC4488_14_transfer3189", "ref": TRANSFER_3189, "needle": "TR3189_0_current_proxy", "role": "3189 transfer status."},
        {"source_id": "SRC4488_15_gate", "ref": GATE_PATH, "needle": "def profile_gate_rows", "role": "4488 helper gate."},
        {"source_id": "SRC4488_16_generator", "ref": GENERATOR_PATH, "needle": 'CHECKPOINT = "4488"', "role": "4488 generator script."},
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
            "proof_result": "P_H profile gate is now executable through |s_K2*kappa_STF|N4_D2 <= (4/5)B_PH and live C2 smooth profiles",
            "fallback_result": "transfer proxy retained; parent profile selection, coupling ownership, DeltaKTF leakage and PPN/orbital transfer remain unsigned",
            "claim_status": "private_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def status_rows(ph_bound: float, profile_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    n4_values = [float(row["N4_D2"]) for row in profile_rows]
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "tight_PH_bound": f"{ph_bound:.15e}",
            "tight_source_norm_limit_4over5B": f"{(4.0 * ph_bound / 5.0):.15e}",
            "smooth_N4_min": f"{min(n4_values):.15e}",
            "smooth_N4_max": f"{max(n4_values):.15e}",
            "local_GR_claim": False,
            "sharpest_open_clause": "parent_profile_selection_coupling_owner_or_PPN_transfer_upgrade",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4488_0",
            "target": NEXT_TARGET,
            "objective": "Either parent-select the source profile/coupling product or upgrade the slip pressure proxy into PPN/orbital/light-time transfer rows.",
            "derive_first": "derive transition width/profile class and s_K2*kappa_STF from parent variation",
            "fallback": "build conservative PPN/orbital transfer matrix for induced slip and DeltaKTF leakage",
            "risk": "using smooth-profile pressure margins as a local-GR proof before profile/coupling/transfer are source-owned",
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
            "claim": "4488 turns the PH slip branch into an executable source-profile gate, imports finite C2 smooth profile rows with N4_D2 about 3.40-4.46, and shows current pressure is comfortable for order-one to 1e9 coupling products while retaining all rows as nonclaim.",
            "current_evidence": "4488 source register, PH profile gate, smooth profile rows, margin rows, transfer-status rows, claim gates, decision/status/next CSVs and validation.",
            "status": "private_PH_profile_gate_smooth_rows_and_transfer_proxy_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "treating profile pressure margins as local-GR proof before parent profile selection, coupling ownership and PPN/orbital transfer are signed.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "parent-selected profile, coupling owner, DeltaKTF leakage and arena transfer remain unsigned",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    gates_core: Sequence[Mapping[str, object]],
    profiles: Sequence[Mapping[str, object]],
    margins: Sequence[Mapping[str, object]],
    transfer_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 504 PPC4161 - PH Source Profile Row Or Parent Zero Transfer Upgrade

Private checkpoint: `{CHECKPOINT}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Generated UTC: `{STAMP}`

## Result

4488 makes the Hessian-slip source product executable.

The live product is:

```text
P_H = -(5/4) s_K2 kappa_STF I4_D2.
```

The conservative envelope is:

```text
|P_H| <= (5/4)|s_K2 kappa_STF| N4_D2.
```

Using the current tight pressure row:

```text
|s_K2 kappa_STF| N4_D2 <= {statuses[0]["tight_source_norm_limit_4over5B"]}.
```

The imported smooth `C2` transition profiles preserve:

```text
I4_D2=-4/5, c_ext=1,
```

and give:

```text
N4_D2 in [{statuses[0]["smooth_N4_min"]}, {statuses[0]["smooth_N4_max"]}].
```

So the tested profiles are not numerically fragile: order-one and `1e9` coupling products pass the current tight pressure proxy, while `1e12` fails. This is still not a local-GR claim because the parent has not selected the profile, source-owned `s_K2 kappa_STF`, bounded `DeltaK_TF`, or upgraded the transfer from public `P2` pressure to PPN/orbital/light-time covariance.

## PH Profile Gate

{table(gates_core)}

## Smooth Profile Rows

{table(profiles)}

## Smooth Profile Margin Rows

{table(margins)}

## Transfer Status

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
    gates_core: Sequence[Mapping[str, object]],
    profiles: Sequence[Mapping[str, object]],
    margins: Sequence[Mapping[str, object]],
    transfer_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4488 Y5/R2FR - PH Source Profile Row Or Parent Zero Transfer Upgrade

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

4488 takes `P_H` from symbolic product to executable profile gate. It imports smooth `C2` profile rows with finite `N4_D2`, computes tight-pressure coupling limits, and keeps transfer/profile/coupling ownership explicitly nonclaim.

## Gate

{table(gates_core)}

## Profiles And Margins

{table(profiles)}

{table(margins)}

## Transfer And Decisions

{table(transfer_rows)}

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
    gates_core: Sequence[Mapping[str, object]],
    profiles: Sequence[Mapping[str, object]],
    margins: Sequence[Mapping[str, object]],
    transfer_rows: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    validations: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False})

    add("VAL4488_0_sources_exist_and_needles_found", all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources), "every cited source path exists and its needle is found")
    add("VAL4488_1_profile_gate_written", any(row.get("gate_id") == "PG4488_2_tight_pressure_condition" for row in gates_core), "tight PH profile gate exists")
    add("VAL4488_2_smooth_profiles_written", len(profiles) == 6 and all(float(row["N4_D2"]) > 0 for row in profiles), "six smooth profile rows have positive N4_D2")
    add("VAL4488_3_margin_rows_written", len(margins) == 18, "selected 1, 1e9, 1e12 margin rows exist for six profiles")
    add("VAL4488_4_margin_has_pass_and_fail", any(str(row.get("pressure_pass_if_sourced")).lower() == "true" for row in margins) and any(str(row.get("pressure_pass_if_sourced")).lower() == "false" for row in margins), "margins include pass and fail scenarios")
    add("VAL4488_5_transfer_proxy_retained", any(row.get("transfer_id") == "TR4488_0_current_proxy" for row in transfer_rows), "transfer proxy remains explicit")
    add("VAL4488_6_claim_gates_block_local_GR", all(str(row.get("claim_allowed")).lower() == "false" for row in gates), "claim gates block promotion")
    add(
        "VAL4488_7_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, gates_core, profiles, margins, transfer_rows, gates, decisions, statuses, next_targets]
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
    add("VAL4488_8_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4488_9_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add("VAL4488_10_claim_register_updated", any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "claims register contains L-330")
    add("VAL4488_11_spine_and_packet_updated", MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH), "spine and packet contain 4488 markers")
    add("VAL4488_12_next_target_selected", bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET, NEXT_TARGET)
    add("VAL4488_13_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    ph_bound = tight_ph_bound()
    sources = source_rows()
    gates_core = profile_gate_rows(ph_bound)
    profiles = smooth_profile_rows(read_csv(PROFILES_3189), ph_bound)
    margins = margin_rows(read_csv(MARGINS_3189))
    transfer_rows = transfer_status_rows()
    ledger = decision_ledger_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, gates_core, profiles, margins, transfer_rows)
    decisions = decision_rows()
    statuses = status_rows(ph_bound, profiles)
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(GATE_CSV, gates_core)
    write_csv(PROFILE_CSV, profiles)
    write_csv(MARGIN_CSV, margins)
    write_csv(TRANSFER_CSV, transfer_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, gates_core, profiles, margins, transfer_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, gates_core, profiles, margins, transfer_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4488 PH Source Profile Gate",
        "4488 turns the Hessian-slip source product into the executable gate `|s_K2 kappa_STF| N4_D2 <= (4/5)B_PH`. Smooth `C2` core-to-exterior profile rows preserve `I4_D2=-4/5`, `c_ext=1`, and give `N4_D2≈3.40-4.46`; order-one through `1e9` coupling products pass current tight pressure, while `1e12` fails. This remains nonclaim until parent profile selection, coupling ownership, `DeltaK_TF`, and transfer upgrade close.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4488 Packet Integration",
        "The private packet now has live smooth source-profile rows for the Hessian-slip branch. The next concrete task is not another generic coupling hunt: it is parent-selecting the profile/coupling product or replacing the public `P2` pressure proxy with PPN/orbital/light-time transfer rows.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [SOURCE_REGISTER, GATE_CSV, PROFILE_CSV, MARGIN_CSV, TRANSFER_CSV, DECISION_LEDGER_CSV, CLAIM_GATES_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    validations = validate(sources, gates_core, profiles, margins, transfer_rows, gates, decisions, statuses, next_targets, csv_paths)
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
