from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from stf_carrier_inventory_l2_bound_gate import (  # noqa: E402
    carrier_inventory_rows,
    claim_gate_rows,
    l2_bound_input_rows,
    line_of,
    read_csv,
    scan_patterns,
    text,
    write_csv,
    zero_or_bound_decision_rows,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4481"
CLAIM_ID = "L-323"
MARKER = "PPC4161_STF_CARRIER_INVENTORY_SOURCE_SWEEP_OR_L2_BOUND_INPUT_PACK_4481"
PACKET_MARKER = "PPC4161_PACKET_STF_CARRIER_INVENTORY_SOURCE_SWEEP_OR_L2_BOUND_INPUT_PACK_4481"
DECISION = "STF_CARRIER_ZERO_NOT_SIGNED_L2_BOUND_INPUT_PACK_STAGED_NONCLAIM"
NEXT_TARGET = "4482-Y5-R2FR-parent-STF-carrier-alphabet-closure-or-J2eff-transfer-scorer.md"

FORMAL_PATH = FORMAL / "497-PPC4161-STF-carrier-inventory-source-sweep-or-l2-bound-input-pack.md"
DOC_PATH = POST / "4481-Y5-R2FR-STF-carrier-inventory-source-sweep-or-l2-bound-input-pack.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4481_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4481_SOURCE_REGISTER.csv"
SWEEP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4481_CORPUS_STF_CARRIER_SWEEP.csv"
INVENTORY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4481_STF_CARRIER_INVENTORY.csv"
INPUT_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4481_L2_BOUND_INPUT_PACK.csv"
ZERO_BOUND_DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4481_ZERO_OR_BOUND_DECISION.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4481_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4481_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4481_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4481_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "stf_carrier_inventory_l2_bound_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4481_STF_carrier_inventory_source_sweep_or_l2_bound_input_pack.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_496 = FORMAL / "496-PPC4161-orientation-carrier-zero-proof-or-quadrupole-residual-scorer.md"
NEXT_4480 = SOURCE_DIR / "P8_Y5_R2FR_4480_NEXT_TARGET.csv"
GATES_4480 = SOURCE_DIR / "P8_Y5_R2FR_4480_CLAIM_GATES.csv"
DOC_2275 = POST / "2275-Y5-R2FR-minimal-carrier-inventory-or-scale-separated-qR-bound.md"
INV_2275 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2275_MINIMAL_CARRIER_INVENTORY.csv"
DOC_1950 = POST / "1950-Y5-R2FR-dimensionless-STF-slip-source-or-zero-theorem.md"
SRC_1950 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1950_DIMENSIONLESS_STF_SOURCE_LEDGER.csv"
DOC_1951 = POST / "1951-Y5-R2FR-STF-response-functional-or-common-mode-router.md"
DOC_1954 = POST / "1954-Y5-R2FR-l2-source-boundary-zero-or-envelope.md"
DOC_1955 = POST / "1955-Y5-R2FR-local-EH-same-source-map-or-residual-l2-bound.md"
L2_1955 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1955_RESIDUAL_L2_BOUND_LEDGER.csv"
DOC_3169 = POST / "3169-Y5-R2FR-STF-Shapiro-source-bound-or-solar-domain-K2-transfer-under-AX1090.md"
BOUNDS_3169 = SOURCE_DIR / "P8_Y5_R2FR_3169_EQUIVALENT_J2_K2_BOUNDS.csv"
TRANSFER_3169 = SOURCE_DIR / "P8_Y5_R2FR_3169_SOLAR_J2_EQUIVALENT_TRANSFER.csv"
DOC_3182 = POST / "3182-Y5-R2FR-metric-readout-of-tracefree-Hessian-carrier-or-tidal-response-coefficient-under-AX1090.md"
CORE_ACTION = ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


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
            "source_id": "SRC4481_00_next4480",
            "ref": NEXT_4480,
            "needle": "4481-Y5-R2FR-STF-carrier-inventory-source-sweep-or-l2-bound-input-pack.md",
            "role": "4480 selected STF carrier inventory and l2 bound input pack.",
        },
        {
            "source_id": "SRC4481_01_formal496_poynting",
            "ref": FORMAL_496,
            "needle": "Poynting-vector instinct",
            "role": "4480 made Poynting/wave route an explicit live carrier fork.",
        },
        {
            "source_id": "SRC4481_02_gates4480",
            "ref": GATES_4480,
            "needle": "CG4480_2_orientation_zero_parent_signed",
            "role": "4480 gate blocking orientation-zero promotion.",
        },
        {
            "source_id": "SRC4481_03_2275_doc",
            "ref": DOC_2275,
            "needle": "Minimal Carrier Inventory",
            "role": "prior carrier/phase ensemble inventory.",
        },
        {
            "source_id": "SRC4481_04_2275_inventory",
            "ref": INV_2275,
            "needle": "MCI2275_0_covariance_ensemble",
            "role": "machine carrier inventory row.",
        },
        {
            "source_id": "SRC4481_05_1950_STF",
            "ref": DOC_1950,
            "needle": "STF1950_2_hessian_STF_channel",
            "role": "dimensionless STF danger channel.",
        },
        {
            "source_id": "SRC4481_06_1950_gamma_policy",
            "ref": SRC_1950,
            "needle": "gamma_bound_policy",
            "role": "private STF/gamma screening scale source.",
        },
        {
            "source_id": "SRC4481_07_1951_functional",
            "ref": DOC_1951,
            "needle": "FUNC1951_2_dimensionless_STF_response",
            "role": "STF response functional and readout norm gap.",
        },
        {
            "source_id": "SRC4481_08_1954_baseline",
            "ref": DOC_1954,
            "needle": "L2R1954_0_baseline_subtraction",
            "role": "GR baseline subtraction for fair l2 comparison.",
        },
        {
            "source_id": "SRC4481_09_1955_same_source",
            "ref": DOC_1955,
            "needle": "EH1955_0_target",
            "role": "EH same-source theorem contract for residual l2.",
        },
        {
            "source_id": "SRC4481_10_1955_bound_ledger",
            "ref": L2_1955,
            "needle": "RB1955_0_residual_bound_formula",
            "role": "residual l2 bound factor ledger.",
        },
        {
            "source_id": "SRC4481_11_3169_doc",
            "ref": DOC_3169,
            "needle": "J2_eff := K_2 C_K2_unit",
            "role": "conditional J2/Shapiro empirical hook.",
        },
        {
            "source_id": "SRC4481_12_3169_bounds",
            "ref": BOUNDS_3169,
            "needle": "JB3169_0_ZK_adopted_solar_J2_scale",
            "role": "machine J2-equivalent bound rows.",
        },
        {
            "source_id": "SRC4481_13_3169_transfer",
            "ref": TRANSFER_3169,
            "needle": "TR3169_2_transfer_blocker",
            "role": "source-domain transfer blocker.",
        },
        {
            "source_id": "SRC4481_14_3182_slip",
            "ref": DOC_3182,
            "needle": "Psi - Phi = 2 Sigma_H phi_ext",
            "role": "tracefree Hessian carrier enters metric readout if source amplitude survives.",
        },
        {
            "source_id": "SRC4481_15_core_action",
            "ref": CORE_ACTION,
            "needle": "scalar motion field",
            "role": "core scalar psi action source.",
        },
        {
            "source_id": "SRC4481_16_gate",
            "ref": GATE_PATH,
            "needle": "def scan_patterns",
            "role": "4481 sweep/input-pack helper.",
        },
        {
            "source_id": "SRC4481_17_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4481"',
            "role": "4481 generator script.",
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
            "proof_result": "Z_orientation is not signed by current corpus because non-scalar/wave/flux/STF/boundary/source routes are live or unsigned",
            "fallback_result": "l2 input pack stages epsilon_Q compact bound, conditional J2/Shapiro hook, private PPN policy, W_STF/residual/clock/orbital missing rows",
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
            "corpus_sweep": "executed",
            "Z_orientation": "not_signed",
            "finite_l2_scorer": "input_pack_staged_not_numeric_claim_ready",
            "best_source_hook": "conditional_J2eff_Shapiro_scale_from_3169",
            "sharpest_open_clause": "parent_STF_carrier_alphabet_closure_or_J2eff_transfer",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4481_0",
            "target": NEXT_TARGET,
            "objective": "Either close the parent STF carrier alphabet so the SO(3) zero theorem applies, or derive the J2eff/source-domain transfer needed to score the finite l2 branch.",
            "derive_first": "prove wave/EM/Poynting, tidal/Hessian, boundary, source-worldtube and phase-carrier routes are after-variation, quotient-vertical, common-mode, isotropically averaged, or absent",
            "fallback": "build a J2eff/residual-l2 scorer using the 3169 J2/Shapiro hook plus 1955 residual l2 bound factors",
            "risk": "claiming isotropy from scalar notation while the corpus contains live carrier routes",
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
            "claim": "4481 runs a corpus STF-carrier source sweep and stages the finite l2 bound input pack; it does not sign Z_orientation or local GR.",
            "current_evidence": "4481 source register, corpus sweep, carrier inventory, l2 bound input pack, zero/bound decision, claim gates, decision/status/next CSVs and validation.",
            "status": "private_carrier_inventory_and_l2_input_pack_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "mistaking corpus scalar action language for a complete parent alphabet while wave/flux/STF/boundary/source carrier routes remain live.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "finite l2 branch remains unscored until parent carrier closure or J2eff/residual transfer factors are derived",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    sweep_rows: Sequence[Mapping[str, object]],
    inventory_rows: Sequence[Mapping[str, object]],
    input_rows: Sequence[Mapping[str, object]],
    zero_bound_rows: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 497 PPC4161 - STF Carrier Inventory Source Sweep Or L2 Bound Input Pack

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4481 does the source sweep instead of guessing.

The result is not a local-GR pass. It is a useful fork:

```text
scalar/SO(3) branch exists
but wave/flux/Poynting, tidal/STF, boundary, source-worldtube and phase-carrier routes are live or unsigned
=> Z_orientation is not signed.
```

This is exactly the discipline we needed. The zero theorem from 4480 is mathematically real, but the current parent corpus has not yet proved that the scalar marker alphabet is exhaustive.

The finite route is now also less vague. The l=2 input pack has:

```text
epsilon_Q in [0,1] from compact support,
conditional J2/Shapiro scale from 3169,
private PPN/STF smoke policy from 1950,
and explicit missing rows for W_STF, residual l2 envelopes, clock and orbital bounds.
```

So the next honest move is not another broad missing-list. It is one of two real attacks:

```text
1. close the parent STF carrier alphabet, or
2. derive J2_eff/source-domain transfer and score the finite residual l=2 branch.
```

## Corpus STF Carrier Sweep

{table(sweep_rows)}

## STF Carrier Inventory

{table(inventory_rows)}

## L2 Bound Input Pack

{table(input_rows)}

## Zero Or Bound Decision

{table(zero_bound_rows)}

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
    sweep_rows: Sequence[Mapping[str, object]],
    inventory_rows: Sequence[Mapping[str, object]],
    input_rows: Sequence[Mapping[str, object]],
    zero_bound_rows: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4481 Y5/R2FR - STF Carrier Inventory Source Sweep Or L2 Bound Input Pack

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

4481 runs the carrier source sweep and refuses the shortcut: `Z_orientation` is not signed because the corpus still has live or unsigned wave/flux/Poynting, tidal/STF, boundary, source-worldtube and phase-carrier routes. The finite l=2 scorer now has a concrete input pack instead of a vague missing bucket.

## Sweep

{table(sweep_rows)}

## Inventory

{table(inventory_rows)}

## L2 Inputs

{table(input_rows)}

## Decisions And Gates

{table(zero_bound_rows)}

{table(gates)}

{table(decisions)}

## Status And Next Target

{table(statuses)}

{table(next_targets)}

## Sources

{table(sources)}
"""


def validate(
    sources: Sequence[Mapping[str, object]],
    sweep_rows: Sequence[Mapping[str, object]],
    inventory_rows: Sequence[Mapping[str, object]],
    input_rows: Sequence[Mapping[str, object]],
    zero_bound_rows: Sequence[Mapping[str, object]],
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
        "VAL4481_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4481_1_sweep_has_live_carriers",
        any(int(row.get("hit_count", 0)) > 0 and row.get("carrier_class") != "scalar_only_parent" for row in sweep_rows),
        "non-scalar carrier pattern hits exist and are recorded",
    )
    add(
        "VAL4481_2_inventory_blocks_Zorientation",
        any(row.get("inventory_id") == "CI4481_1_wave_flux_poynting" for row in inventory_rows)
        and any(row.get("inventory_id") == "CI4481_4_source_worldtube_l2" for row in inventory_rows),
        "inventory includes wave/flux and source-worldtube l2 routes",
    )
    add(
        "VAL4481_3_l2_bound_pack_written",
        all(
            any(row.get("input_id") == input_id for row in input_rows)
            for input_id in [
                "L2BI4481_0_epsilon_Q_compact_bound",
                "L2BI4481_2_tau_Shapiro_Q_J2_scale",
                "L2BI4481_3_tau_PPN_Q_private_gamma_policy",
                "L2BI4481_4_W_STF_norm",
                "L2BI4481_5_same_source_residuals",
                "L2BI4481_6_tau_clock_Q",
                "L2BI4481_7_tau_orbital_Q",
            ]
        ),
        "input pack includes compact bound, J2 hook, PPN policy and missing residual/readout/clock/orbital rows",
    )
    add(
        "VAL4481_4_zero_or_bound_decision_written",
        any(row.get("decision_id") == "ZBD4481_0_zero_certificate" and row.get("answer") == "NO_NOT_YET" for row in zero_bound_rows),
        "zero certificate refusal is explicit",
    )
    add(
        "VAL4481_5_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4481_2_Z_orientation_signed" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR/R10 promotion",
    )
    add(
        "VAL4481_6_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, sweep_rows, inventory_rows, input_rows, zero_bound_rows, gates, decisions, statuses, next_targets]
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
    add("VAL4481_7_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4481_8_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4481_9_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-323",
    )
    add(
        "VAL4481_10_spine_and_packet_updated",
        MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH),
        "unification spine and private packet integration contain 4481 markers",
    )
    add(
        "VAL4481_11_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4481_12_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    sweep_rows = scan_patterns(ROOT)
    inventory_rows = carrier_inventory_rows(sweep_rows)
    input_rows = l2_bound_input_rows()
    zero_bound_rows = zero_or_bound_decision_rows()
    gates = claim_gate_rows(sources, sweep_rows, inventory_rows, input_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SWEEP_CSV, sweep_rows)
    write_csv(INVENTORY_CSV, inventory_rows)
    write_csv(INPUT_PACK_CSV, input_rows)
    write_csv(ZERO_BOUND_DECISION_CSV, zero_bound_rows)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, sweep_rows, inventory_rows, input_rows, zero_bound_rows, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, sweep_rows, inventory_rows, input_rows, zero_bound_rows, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4481 STF Carrier Inventory And L2 Input Pack",
        "4481 runs a corpus sweep for STF/orientation carriers and refuses to sign `Z_orientation`: scalar action language exists, but wave/flux/Poynting, tidal/STF, boundary, source-worldtube and phase-carrier routes remain live or unsigned. The finite branch now has a concrete l=2 input pack with compact `epsilon_Q`, conditional J2/Shapiro rows, private PPN policy, and explicit missing residual/readout/clock/orbital inputs.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4481 Packet Integration",
        "The private packet now treats orientation closure as a parent-alphabet theorem, not a prose assumption. Next work should either prove carrier alphabet closure for the 4480 SO(3) zero theorem or derive the `J2_eff`/residual-l2 transfer needed to score finite quadrupole leakage.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        SWEEP_CSV,
        INVENTORY_CSV,
        INPUT_PACK_CSV,
        ZERO_BOUND_DECISION_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, sweep_rows, inventory_rows, input_rows, zero_bound_rows, gates, decisions, statuses, next_targets, csv_paths)
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
