from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from second_curvature_channel_gate import (  # noqa: E402
    bound_pressure_rows,
    channel_classification_rows,
    claim_gate_rows,
    decision_rows as gate_decision_rows,
    finite_coefficient_pack_rows,
    read_csv,
    second_order_theorem_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4469"
CLAIM_ID = "L-311"
MARKER = "PPC4161_SECOND_CURVATURE_CHANNEL_FORBIDDEN_OR_FINITE_CR2_PACK_4469"
PACKET_MARKER = "PPC4161_PACKET_SECOND_CURVATURE_CHANNEL_FORBIDDEN_OR_FINITE_CR2_PACK_4469"
DECISION = "STRICT_SECOND_ORDER_NO_EXTRA_MODE_THEOREM_WRITTEN_PARENT_SELECTOR_UNSIGNED_FINITE_CR2_CTOTAL_PACK_RETAINED_NONCLAIM"
NEXT_TARGET = "4470-Y5-R2FR-parent-two-derivative-no-extra-mode-selector-signature-or-cR2-coefficient-intake.md"

FORMAL_PATH = FORMAL / "485-PPC4161-second-curvature-channel-forbidden-or-finite-cR2-parent-coefficient-pack.md"
DOC_PATH = POST / "4469-Y5-R2FR-second-curvature-channel-forbidden-or-finite-cR2-parent-coefficient-pack.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4469_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4469_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4469_SECOND_ORDER_THEOREM_AUDIT.csv"
CHANNEL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4469_CHANNEL_CLASSIFICATION.csv"
COEFFICIENT_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4469_FINITE_COEFFICIENT_PACK.csv"
PRESSURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4469_BOUND_PRESSURE_PACK.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4469_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4469_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4469_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4469_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4469_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "second_curvature_channel_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4469_second_curvature_channel_forbidden_or_finite_cR2_parent_coefficient_pack.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4468 = SOURCE_DIR / "P8_Y5_R2FR_4468_NEXT_TARGET.csv"
FORMAL_484 = FORMAL / "484-PPC4161-parent-action-normal-form-no-Achi-no-second-channel.md"
FORMAL_200 = FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md"
FORMAL_201 = FORMAL / "201-PPC4161-extra-invariant-residual-coefficient-map.md"
POST_4459 = POST / "4459-Y5-R2FR-primitive-deficit-action-law-or-first-cR2-coefficient-owner-value.md"
FORMAL_477 = FORMAL / "477-PPC4161-connection-hinge-refinement-owner-or-c2-scalaron-map.md"
SCALARON_4461 = SOURCE_DIR / "P8_Y5_R2FR_4461_C2_SCALARON_OBSERVABLE_MAP.csv"
OWNER_4461 = SOURCE_DIR / "P8_Y5_R2FR_4461_OWNER_COMPATIBILITY_THEOREM.csv"
REFINEMENT_4460 = SOURCE_DIR / "P8_Y5_R2FR_4460_PARENT_REFINEMENT_SIGNATURE_CONTRACT.csv"
R10_PRESSURE_4466 = SOURCE_DIR / "P8_Y5_R2FR_4466_R10_PRESSURE_EVALUATION.csv"
METRIC_SECOND_ORDER_SCRIPT = SCRIPT_DIR / "metric_only_second_order_sector_reduction_attempt.py"


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
            "source_id": "SRC4469_00_next4468",
            "ref": NEXT_4468,
            "needle": "4469-Y5-R2FR-second-curvature-channel-forbidden",
            "role": "4468 selected the second-curvature-channel/finite-coefficient target.",
        },
        {
            "source_id": "SRC4469_01_formal484",
            "ref": FORMAL_484,
            "needle": "That does **not** kill a metric scalaron",
            "role": "4468 split explicit Achi from metric scalaron coupling.",
        },
        {
            "source_id": "SRC4469_02_palatini_two_derivative",
            "ref": FORMAL_200,
            "needle": "leading low-energy/two-derivative order",
            "role": "strict local selector premise.",
        },
        {
            "source_id": "SRC4469_03_palatini_no_extra_modes",
            "ref": FORMAL_200,
            "needle": "no extra unscreened light modes",
            "role": "strict local selector premise.",
        },
        {
            "source_id": "SRC4469_04_palatini_residual",
            "ref": FORMAL_200,
            "needle": "curvature squares -> coefficient",
            "role": "current selector retains curvature-square residuals.",
        },
        {
            "source_id": "SRC4469_05_palatini_unsigned",
            "ref": FORMAL_200,
            "needle": "selector_assumptions_parent_derived = false",
            "role": "selector not globally parent-derived.",
        },
        {
            "source_id": "SRC4469_06_residual201",
            "ref": FORMAL_201,
            "needle": "c_R2 or M_R curvature-square finite-range tail",
            "role": "residual map keeps c_R2/M_R live.",
        },
        {
            "source_id": "SRC4469_07_refinement4459",
            "ref": POST_4459,
            "needle": "separate second channel",
            "role": "same-channel refinement linearity does not exclude separate channels.",
        },
        {
            "source_id": "SRC4469_08_scalaron477_basis",
            "ref": FORMAL_477,
            "needle": "SM4461_0_basis_guard",
            "role": "D0/D2 finite scalaron basis guard.",
        },
        {
            "source_id": "SRC4469_09_scalaron477_coupling",
            "ref": FORMAL_477,
            "needle": "SM4461_3_scalar_coupling",
            "role": "alpha_eff=C_matter^2/3 finite coupling formula.",
        },
        {
            "source_id": "SRC4469_10_scalaron_csv",
            "ref": SCALARON_4461,
            "needle": "SM4461_0_basis_guard",
            "role": "machine-readable scalaron basis guard.",
        },
        {
            "source_id": "SRC4469_11_refinement_contract",
            "ref": REFINEMENT_4460,
            "needle": "RGC4460_1_cylindrical_action",
            "role": "refinement/cylindrical parent action not signed.",
        },
        {
            "source_id": "SRC4469_12_owner4461",
            "ref": OWNER_4461,
            "needle": "OCT4461_4_refinement_linearity",
            "role": "owner compatibility refinement-linearity row.",
        },
        {
            "source_id": "SRC4469_13_r10_pressure",
            "ref": R10_PRESSURE_4466,
            "needle": "R10P4466_0_current_lambda_pressure",
            "role": "current finite universal scalar pressure.",
        },
        {
            "source_id": "SRC4469_14_metric_second_order_script",
            "ref": METRIC_SECOND_ORDER_SCRIPT,
            "needle": "no parent theorem forbids R2/fR/Ricci/Weyl/nonlocal operators",
            "role": "previous metric-only second-order sector attempt.",
        },
        {
            "source_id": "SRC4469_15_gate",
            "ref": GATE_PATH,
            "needle": "def second_order_theorem_rows",
            "role": "4469 second curvature channel gate.",
        },
        {
            "source_id": "SRC4469_16_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4469"',
            "role": "4469 generator script.",
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
            "conditional_theorem_result": "strict second-order/no-extra-mode local selector forbids non-topological curvature-square bulk channels",
            "parent_status": "selector exists but is not parent-derived in current MTS",
            "finite_pack_result": "D0/D2, c_R2_eff, C_total, live alpha(lambda), and PPN projection remain missing",
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
            "second_order_theorem_status": "exact_conditional_selector_theorem_written",
            "parent_selector_status": "not_parent_derived",
            "second_channel_status": "not_forbidden_by_current_parent",
            "finite_pack_status": "retained_missing_coefficients",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4469_0",
            "target": NEXT_TARGET,
            "objective": "Try to parent-sign the strict two-derivative/no-extra-mode selector from MTS primitives; if that fails, intake finite c_R2_eff/D0/D2/C_total coefficient rows.",
            "derive_first": "prove MTS object language admits only EH/Lambda/GB-topological local geometry through tested scales",
            "fallback": "source finite D0/D2 or c_R2_eff plus C_total, live alpha(lambda), and PPN/lightcone projection",
            "risk": "treating a low-energy truncation or selector assumption as an exact parent zero theorem",
            "valid_for_claim": False,
        }
    ]


def update_claims_register() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else [
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
    ]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r10_scalar_source_coupling",
        "claim": "4469 writes the strict second-order/no-extra-mode theorem that would forbid non-topological curvature-square channels, but current MTS has not parent-derived that selector, so c_R2_eff/C_total finite rows remain live and nonclaim.",
        "current_evidence": "4469 source register, second-order theorem audit, channel classification, finite coefficient pack, pressure pack, claim gates, decision/status/next CSVs and validation.",
        "status": "private_nonclaim_checkpoint",
        "next_test": NEXT_TARGET,
        "key_risk": "using a low-energy/two-derivative selector as if it were an exact parent action theorem.",
        "sector": "local_gr_newton_r10_scalar_source_coupling",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "finite scalar/tensor curvature channels survive without parent selector signature or source-backed coefficients",
    }
    rows.append({fieldname: claim_row.get(fieldname, "") for fieldname in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def append_section_once(path: Path, marker: str, title: str, body: str) -> None:
    current_text = text(path)
    if marker in current_text:
        return
    section = f"\n\n<!-- {marker} -->\n## {title}\n\n{body.strip()}\n"
    write_text(path, current_text.rstrip() + section)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    theorem_rows: Sequence[Mapping[str, object]],
    channel_rows: Sequence[Mapping[str, object]],
    coefficient_rows: Sequence[Mapping[str, object]],
    pressure_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 485 PPC4161 — Second Curvature Channel Forbidden Or Finite `c_R2` Parent Coefficient Pack

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4469 makes the second-channel route precise.

There is a clean exact theorem shape: if the MTS parent signs a strict 4D local metric/coframe selector with second-order local equations, no extra unscreened local modes, and only fixed/topological/routed boundary terms, then the local bulk geometry reduces to EH plus `Lambda` plus topological/boundary harmless terms. Non-topological `R^2`, `Ricci^2`, `Weyl^2`, `f(R)` and nonlocal channels are then forbidden through tested local scales.

But current MTS has not parent-derived that selector. The existing corpus records it as a selector with active residual coefficients, so the second curvature/scalar channel is not yet killed. Therefore the finite branch remains live and must be represented by `D0`, `D2`, `c_R2_eff`, `C_total`, `alpha_bound(lambda)` and PPN/lightcone projections before any empirical local claim.

## Second-Order Theorem Audit

{table(theorem_rows)}

## Channel Classification

{table(channel_rows)}

## Finite Coefficient Pack

{table(coefficient_rows)}

## Bound Pressure Pack

{table(pressure_rows)}

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
    channel_rows: Sequence[Mapping[str, object]],
    coefficient_rows: Sequence[Mapping[str, object]],
    pressure_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4469 Y5/R2FR — Second Curvature Channel Forbidden Or Finite `c_R2` Parent Coefficient Pack

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

The best derivation route is now explicit: a strict second-order/no-extra-mode parent selector would kill the non-topological second curvature channel. The current MTS corpus does not yet derive that selector, so this checkpoint also stages the finite coefficient pack instead of pretending the channel vanished.

## Theorem Audit

{table(theorem_rows)}

## Channel Classification

{table(channel_rows)}

## Finite Coefficient Pack

{table(coefficient_rows)}

## Pressure Pack

{table(pressure_rows)}

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
    channel_rows: Sequence[Mapping[str, object]],
    coefficient_rows: Sequence[Mapping[str, object]],
    pressure_rows: Sequence[Mapping[str, object]],
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
        "VAL4469_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4469_1_conditional_theorem_written",
        any(row.get("theorem_id") == "SOT4469_0_strict_metric_second_order" for row in theorem_rows),
        "strict second-order/no-extra-mode theorem route is written",
    )
    add(
        "VAL4469_2_parent_selector_unsigned",
        any(row.get("theorem_id") == "SOT4469_1_current_MTS_selector_status" and row.get("parent_signed") is False for row in theorem_rows),
        "current MTS selector is not parent-signed",
    )
    add(
        "VAL4469_3_no_second_channel_not_signed",
        any(row.get("theorem_id") == "SOT4469_4_no_second_channel_verdict" and row.get("current_status") == "NOT_SIGNED_FINITE_BRANCH_RETAINED" for row in theorem_rows),
        "full no-second-channel certificate remains unsigned",
    )
    add(
        "VAL4469_4_channel_verdict_retained",
        any(row.get("channel_id") == "CH4469_5_verdict" and row.get("current_status") == "NOT_FORBIDDEN_BY_CURRENT_PARENT" for row in channel_rows),
        "channel classification retains finite branch",
    )
    add(
        "VAL4469_5_coefficient_pack_blocked",
        all(row.get("claim_status") == "BLOCKED" for row in coefficient_rows),
        "finite coefficient pack is staged but blocked by missing parent/source inputs",
    )
    add(
        "VAL4469_6_pressure_guard_present",
        any(row.get("pressure_id") == "BP4469_0_current_R10_pressure" and float(row.get("ratio_alpha_to_bound", 0)) > 1 for row in pressure_rows),
        "universal scalar pressure guard is present and failing",
    )
    add(
        "VAL4469_7_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4469_2_no_second_channel_parent_signed" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR scalar closure",
    )
    add(
        "VAL4469_8_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, theorem_rows, channel_rows, coefficient_rows, pressure_rows, gates, decisions, statuses, next_targets]
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
    add("VAL4469_9_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4469_10_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4469_11_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-311",
    )
    add(
        "VAL4469_12_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4469_13_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    theorem_rows = second_order_theorem_rows()
    channel_rows = channel_classification_rows()
    coefficient_rows = finite_coefficient_pack_rows()
    pressure_rows = bound_pressure_rows()
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, theorem_rows, channel_rows, coefficient_rows, pressure_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem_rows)
    write_csv(CHANNEL_CSV, channel_rows)
    write_csv(COEFFICIENT_PACK_CSV, coefficient_rows)
    write_csv(PRESSURE_CSV, pressure_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, theorem_rows, channel_rows, coefficient_rows, pressure_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, theorem_rows, channel_rows, coefficient_rows, pressure_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4469 Strict Second-Order Selector Or Finite Curvature Pack",
        "4469 writes the exact conditional theorem shape for forbidding the second curvature/scalar channel: a parent-signed strict second-order/no-extra-unscreened-mode local metric/coframe selector would leave only EH, Lambda and topological/boundary harmless terms. Current MTS has not parent-derived that selector, so `D0`, `D2`, `c_R2_eff`, `C_total`, live `alpha(lambda)` and PPN projection rows remain mandatory finite inputs.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4469 Packet Integration",
        "The private packet now knows the difference between a true theorem and a low-energy selector. The exact route is to derive the strict two-derivative/no-extra-mode parent signature; otherwise the finite curvature/scalar coefficient pack must be filled before R10/PPN/local-GR claims.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        CHANNEL_CSV,
        COEFFICIENT_PACK_CSV,
        PRESSURE_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, theorem_rows, channel_rows, coefficient_rows, pressure_rows, gates, decisions, statuses, next_targets, csv_paths)
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
