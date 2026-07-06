from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from parent_stf_carrier_closure_j2_transfer_gate import (  # noqa: E402
    claim_gate_rows,
    closure_clause_rows,
    corrected_j2_transfer_rows,
    decision_rows as gate_decision_rows,
    finite_l2_scorer_rows,
    owner_input_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4482"
CLAIM_ID = "L-324"
MARKER = "PPC4161_PARENT_STF_CARRIER_ALPHABET_CLOSURE_OR_J2EFF_TRANSFER_SCORER_4482"
PACKET_MARKER = "PPC4161_PACKET_PARENT_STF_CARRIER_ALPHABET_CLOSURE_OR_J2EFF_TRANSFER_SCORER_4482"
DECISION = "PARENT_STF_ALPHABET_NOT_CLOSED_UPSILON_J2_TRANSFER_SCORER_DERIVED_NONCLAIM"
NEXT_TARGET = "4483-Y5-R2FR-public-metric-radial-Green-owner-or-finite-l2-scorer-input-fill.md"

FORMAL_PATH = FORMAL / "498-PPC4161-parent-STF-carrier-alphabet-closure-or-J2eff-transfer-scorer.md"
DOC_PATH = POST / "4482-Y5-R2FR-parent-STF-carrier-alphabet-closure-or-J2eff-transfer-scorer.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4482_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4482_SOURCE_REGISTER.csv"
CLOSURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4482_PARENT_STF_CARRIER_CLOSURE_CLAUSES.csv"
TRANSFER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4482_UPSILON_J2_TRANSFER_SCORER.csv"
SCORER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4482_FINITE_L2_SCORER_BRIDGE.csv"
OWNER_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4482_OWNER_INPUT_ROWS.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4482_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4482_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4482_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4482_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4482_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "parent_stf_carrier_closure_j2_transfer_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4482_parent_STF_carrier_alphabet_closure_or_J2eff_transfer_scorer.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_497 = FORMAL / "497-PPC4161-STF-carrier-inventory-source-sweep-or-l2-bound-input-pack.md"
NEXT_4481 = SOURCE_DIR / "P8_Y5_R2FR_4481_NEXT_TARGET.csv"
INVENTORY_4481 = SOURCE_DIR / "P8_Y5_R2FR_4481_STF_CARRIER_INVENTORY.csv"
INPUTS_4481 = SOURCE_DIR / "P8_Y5_R2FR_4481_L2_BOUND_INPUT_PACK.csv"
GATES_4481 = SOURCE_DIR / "P8_Y5_R2FR_4481_CLAIM_GATES.csv"
DOC_3170 = POST / "3170-Y5-R2FR-solar-domain-K2-J2eff-normalization-or-refusal-under-AX1090.md"
NORM_3170 = SOURCE_DIR / "P8_Y5_R2FR_3170_SOLAR_J2_NORMALIZATION_DERIVATION.csv"
BOUNDS_3170 = SOURCE_DIR / "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv"
DOC_3171 = POST / "3171-Y5-R2FR-K2-radial-profile-owner-or-J2-transfer-demotion-under-AX1090.md"
AUDIT_3171 = SOURCE_DIR / "P8_Y5_R2FR_3171_PROFILE_OWNER_AUDIT.csv"
NONID_3171 = SOURCE_DIR / "P8_Y5_R2FR_3171_PROFILE_NONIDENTIFIABILITY_PROOF.csv"
UPSILON_3171 = SOURCE_DIR / "P8_Y5_R2FR_3171_UPSILON_J2_TRANSFER_CONTRACT.csv"
DEMOTION_3171 = SOURCE_DIR / "P8_Y5_R2FR_3171_J2_SCORING_DEMOTION.csv"
L2_1955 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1955_RESIDUAL_L2_BOUND_LEDGER.csv"
TRANSFER_3169 = SOURCE_DIR / "P8_Y5_R2FR_3169_SOLAR_J2_EQUIVALENT_TRANSFER.csv"


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
            "source_id": "SRC4482_00_next4481",
            "ref": NEXT_4481,
            "needle": "4482-Y5-R2FR-parent-STF-carrier-alphabet-closure-or-J2eff-transfer-scorer.md",
            "role": "4481 selected carrier alphabet closure or J2eff transfer scorer.",
        },
        {
            "source_id": "SRC4482_01_formal497",
            "ref": FORMAL_497,
            "needle": "Z_orientation is not signed",
            "role": "4481 formal handoff: zero route not signed.",
        },
        {
            "source_id": "SRC4482_02_inventory4481",
            "ref": INVENTORY_4481,
            "needle": "CI4481_1_wave_flux_poynting",
            "role": "live wave/flux/Poynting carrier route.",
        },
        {
            "source_id": "SRC4482_03_inputs4481",
            "ref": INPUTS_4481,
            "needle": "L2BI4481_2_tau_Shapiro_Q_J2_scale",
            "role": "conditional J2/Shapiro hook staged in 4481.",
        },
        {
            "source_id": "SRC4482_04_gates4481",
            "ref": GATES_4481,
            "needle": "CG4481_2_Z_orientation_signed",
            "role": "4481 claim gate blocking Z_orientation.",
        },
        {
            "source_id": "SRC4482_05_doc3170",
            "ref": DOC_3170,
            "needle": "J2_eff = K_2 C_K2_unit rho^3",
            "role": "3170 corrected J2 metric normalization.",
        },
        {
            "source_id": "SRC4482_06_norm3170",
            "ref": NORM_3170,
            "needle": "JN3170_1_corrected_J2eff_map",
            "role": "machine corrected J2eff map.",
        },
        {
            "source_id": "SRC4482_07_bounds3170",
            "ref": BOUNDS_3170,
            "needle": "CJ3170_2_Rozelot_half_range_proxy",
            "role": "corrected conditional J2 pressure row.",
        },
        {
            "source_id": "SRC4482_08_doc3171",
            "ref": DOC_3171,
            "needle": "Upsilon_J2",
            "role": "3171 transfer-kernel non-identifiability.",
        },
        {
            "source_id": "SRC4482_09_audit3171",
            "ref": AUDIT_3171,
            "needle": "PO3171_4_public_metric_injection",
            "role": "missing Pi_J2_metric owner.",
        },
        {
            "source_id": "SRC4482_10_nonid3171",
            "ref": NONID_3171,
            "needle": "NI3171_0_counterfamily",
            "role": "non-identifiability proof.",
        },
        {
            "source_id": "SRC4482_11_upsilon3171",
            "ref": UPSILON_3171,
            "needle": "UJ3171_0_definition",
            "role": "Upsilon_J2 transfer contract.",
        },
        {
            "source_id": "SRC4482_12_demotion3171",
            "ref": DEMOTION_3171,
            "needle": "DM3171_1_3170_corrected_bounds",
            "role": "corrected J2 rows are transfer-only.",
        },
        {
            "source_id": "SRC4482_13_l2_1955",
            "ref": L2_1955,
            "needle": "RB1955_0_residual_bound_formula",
            "role": "fair residual l2 scorer after GR baseline.",
        },
        {
            "source_id": "SRC4482_14_transfer3169",
            "ref": TRANSFER_3169,
            "needle": "TR3169_2_transfer_blocker",
            "role": "source-domain transfer blocker.",
        },
        {
            "source_id": "SRC4482_15_gate",
            "ref": GATE_PATH,
            "needle": "def corrected_j2_transfer_rows",
            "role": "4482 helper gate.",
        },
        {
            "source_id": "SRC4482_16_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4482"',
            "role": "4482 generator script.",
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
            "proof_result": "parent STF alphabet closure remains unsigned; each live carrier now has an exact firewall condition",
            "fallback_result": "corrected J2eff transfer/scorer derived with Upsilon_J2 and residual-l2 scorer bridge staged",
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
            "parent_STF_alphabet": "not_closed",
            "Upsilon_J2_transfer": "derived_symbolic_not_sourced",
            "finite_l2_scorer": "bridge_written_inputs_missing",
            "sharpest_open_clause": "Pi_J2_metric_exterior_Green_profile_or_residual_l2_inputs",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4482_0",
            "target": NEXT_TARGET,
            "objective": "Derive Pi_J2_metric and the exterior r^-3 Green/profile owner, or fill the finite residual-l2 scorer inputs without claiming a pass.",
            "derive_first": "prove public metric injection and radial Green owner from the parent local equations",
            "fallback": "source/bound Upsilon_J2, W_STF, DeltaJ2, P2R_extra and Deltah2 as nonclaim finite scorer rows",
            "risk": "using corrected J2 pressure rows as empirical evidence before Upsilon_J2 is owned",
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
            "claim": "4482 writes the exact parent STF carrier closure clauses and derives the corrected Upsilon_J2 transfer/scorer bridge, without claiming local GR or J2 safety.",
            "current_evidence": "4482 source register, parent STF carrier closure clauses, Upsilon_J2 transfer scorer, finite l2 scorer bridge, owner input rows, claim gates, decision/status/next CSVs and validation.",
            "status": "private_closure_contract_and_Upsilon_J2_transfer_scorer_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "using J2 pressure rows before the parent public-metric/radial/source transfer is owned.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "Pi_J2_metric, exterior Green profile, Upsilon_J2 and residual-l2 inputs remain missing",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    closure_rows: Sequence[Mapping[str, object]],
    transfer_rows: Sequence[Mapping[str, object]],
    scorer_rows: Sequence[Mapping[str, object]],
    input_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 498 PPC4161 - Parent STF Carrier Alphabet Closure Or J2eff Transfer Scorer

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4482 tries the closure route first.

The honest result is:

```text
Z_orientation is still not signed.
```

But this is not a dead loop. The parent closure problem is now exact: every live carrier route has a firewall condition. Wave/EM/Poynting, tidal/Hessian, boundary, source-worldtube and phase-carrier channels must each be after-variation data, quotient-vertical, common-mode, isotropically averaged, same-source GR baseline, or source-bounded.

The fallback route also moved forward. The corrected transfer is:

```text
A_metric(r)=2 epsilon_sun_surface J2 rho^-3
A_metric_solar_surface = Upsilon_J2 K2 C_K2_unit
J2_eff = Upsilon_J2 K2 C_K2_unit rho^3/(2 epsilon_sun_surface)
K2 <= 2 epsilon_sun_surface J2_bound rho^-3/(|Upsilon_J2| C_K2_unit).
```

At the solar surface, the rough 3170 half-range pressure row is:

```text
K2 <= 3.898004369090586e10 / |Upsilon_J2|.
```

That is a real scorer shape. It is not a claim until `Upsilon_J2`, `Pi_J2_metric`, the exterior `r^-3` Green/profile owner, and the residual-l2 inputs are parent-sourced.

## Parent STF Carrier Closure Clauses

{table(closure_rows)}

## Corrected Upsilon J2 Transfer

{table(transfer_rows)}

## Finite L2 Scorer Bridge

{table(scorer_rows)}

## Owner Input Rows

{table(input_rows)}

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
    closure_rows: Sequence[Mapping[str, object]],
    transfer_rows: Sequence[Mapping[str, object]],
    scorer_rows: Sequence[Mapping[str, object]],
    input_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4482 Y5/R2FR - Parent STF Carrier Alphabet Closure Or J2eff Transfer Scorer

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

4482 does not close the parent STF alphabet, but it stops the loop by writing the exact firewall clauses and importing the corrected `Upsilon_J2` transfer. The finite l=2 branch now has a real scorer equation; the missing pieces are `Pi_J2_metric`, exterior `r^-3` Green/profile ownership, `Upsilon_J2`, and residual-l2 envelopes.

## Closure

{table(closure_rows)}

## Transfer

{table(transfer_rows)}

## Scorer

{table(scorer_rows)}

## Inputs

{table(input_rows)}

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
    closure_rows: Sequence[Mapping[str, object]],
    transfer_rows: Sequence[Mapping[str, object]],
    scorer_rows: Sequence[Mapping[str, object]],
    input_rows: Sequence[Mapping[str, object]],
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
        "VAL4482_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4482_1_closure_clauses_written",
        any(row.get("clause_id") == "PAC4482_6_verdict" for row in closure_rows),
        "parent STF closure verdict written",
    )
    add(
        "VAL4482_2_zero_not_overclaimed",
        any(row.get("clause_id") == "PAC4482_6_verdict" and row.get("Z_orientation_signed") is False for row in closure_rows),
        "Z_orientation remains unsigned",
    )
    add(
        "VAL4482_3_corrected_transfer_written",
        any(row.get("transfer_id") == "J2T4482_2_corrected_J2eff" for row in transfer_rows)
        and any(row.get("transfer_id") == "J2T4482_3_K2_bound_scaling" for row in transfer_rows),
        "corrected Upsilon_J2 transfer and bound scaling are written",
    )
    add(
        "VAL4482_4_scorer_bridge_written",
        any(row.get("scorer_id") == "FLS4482_3_residual_l2_after_GR_baseline" for row in scorer_rows),
        "finite residual-l2 after GR baseline scorer is written",
    )
    add(
        "VAL4482_5_owner_inputs_missing_explicit",
        all("MISSING" in str(row.get("current_value", "")) for row in input_rows),
        "owner inputs remain explicit missing rows",
    )
    add(
        "VAL4482_6_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4482_4_numeric_claim_ready" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR/J2 promotion",
    )
    add(
        "VAL4482_7_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, closure_rows, transfer_rows, scorer_rows, input_rows, gates, decisions, statuses, next_targets]
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
    add("VAL4482_8_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4482_9_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4482_10_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-324",
    )
    add(
        "VAL4482_11_spine_and_packet_updated",
        MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH),
        "unification spine and private packet integration contain 4482 markers",
    )
    add(
        "VAL4482_12_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4482_13_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    closure_rows = closure_clause_rows()
    transfer_rows = corrected_j2_transfer_rows()
    scorer_rows = finite_l2_scorer_rows()
    input_rows = owner_input_rows()
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, closure_rows, transfer_rows, scorer_rows, input_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(CLOSURE_CSV, closure_rows)
    write_csv(TRANSFER_CSV, transfer_rows)
    write_csv(SCORER_CSV, scorer_rows)
    write_csv(OWNER_INPUT_CSV, input_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, closure_rows, transfer_rows, scorer_rows, input_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, closure_rows, transfer_rows, scorer_rows, input_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4482 Parent STF Carrier Closure Or J2eff Transfer",
        "4482 writes the exact parent STF carrier firewall clauses and imports the corrected `Upsilon_J2` transfer. The corrected scorer is `J2_eff = Upsilon_J2 K2 C_K2_unit rho^3/(2 epsilon_sun_surface)`, so `K2 <= 2 epsilon_sun_surface J2_bound rho^-3/(|Upsilon_J2| C_K2_unit)`. This remains nonclaim until `Pi_J2_metric`, the exterior Green/profile owner, source-domain transfer and residual-l2 inputs are derived.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4482 Packet Integration",
        "The private packet now has the finite l=2 scorer bridge needed after 4481: either close all carrier firewalls and use the 4480 SO(3) zero theorem, or derive/source `Upsilon_J2`, `Pi_J2_metric`, `G_l2`, `T_source`, `W_STF`, `DeltaJ2`, `P2R_extra` and `Deltah2`.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        CLOSURE_CSV,
        TRANSFER_CSV,
        SCORER_CSV,
        OWNER_INPUT_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, closure_rows, transfer_rows, scorer_rows, input_rows, gates, decisions, statuses, next_targets, csv_paths)
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
