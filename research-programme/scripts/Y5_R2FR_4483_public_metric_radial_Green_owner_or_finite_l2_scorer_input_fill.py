from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from public_metric_radial_green_owner_gate import (  # noqa: E402
    claim_gate_rows,
    decision_ledger_rows,
    finite_scorer_input_rows,
    metric_owner_clause_rows,
    radial_green_theorem_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4483"
CLAIM_ID = "L-325"
MARKER = "PPC4161_PUBLIC_METRIC_RADIAL_GREEN_OWNER_OR_FINITE_L2_SCORER_INPUT_FILL_4483"
PACKET_MARKER = "PPC4161_PACKET_PUBLIC_METRIC_RADIAL_GREEN_OWNER_OR_FINITE_L2_SCORER_INPUT_FILL_4483"
DECISION = "PUBLIC_R_MINUS_3_GREEN_THEOREM_DERIVED_PARENT_METRIC_SOURCE_OWNER_UNSIGNED"
NEXT_TARGET = "4484-Y5-R2FR-parent-EH-weak-field-operator-signature-or-PiJ2metric-transfer-row.md"

FORMAL_PATH = FORMAL / "499-PPC4161-public-metric-radial-Green-owner-or-finite-l2-scorer-input-fill.md"
DOC_PATH = POST / "4483-Y5-R2FR-public-metric-radial-Green-owner-or-finite-l2-scorer-input-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4483_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4483_SOURCE_REGISTER.csv"
RADIAL_GREEN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4483_RADIAL_GREEN_THEOREM.csv"
OWNER_CLAUSES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4483_PI_J2_METRIC_OWNER_CLAUSES.csv"
SCORER_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4483_FINITE_SCORER_INPUT_FILL.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4483_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4483_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4483_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4483_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4483_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "public_metric_radial_green_owner_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4483_public_metric_radial_Green_owner_or_finite_l2_scorer_input_fill.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_4482 = FORMAL / "498-PPC4161-parent-STF-carrier-alphabet-closure-or-J2eff-transfer-scorer.md"
NEXT_4482 = SOURCE_DIR / "P8_Y5_R2FR_4482_NEXT_TARGET.csv"
OWNER_4482 = SOURCE_DIR / "P8_Y5_R2FR_4482_OWNER_INPUT_ROWS.csv"
TRANSFER_4482 = SOURCE_DIR / "P8_Y5_R2FR_4482_UPSILON_J2_TRANSFER_SCORER.csv"
SCORER_4482 = SOURCE_DIR / "P8_Y5_R2FR_4482_FINITE_L2_SCORER_BRIDGE.csv"
DOC_3172 = POST / "3172-Y5-R2FR-public-metric-radial-Green-owner-or-J2-channel-closure-under-AX1090.md"
GREEN_3172 = SOURCE_DIR / "P8_Y5_R2FR_3172_GREEN_OWNER_ATTEMPT.csv"
CHANNEL_3172 = SOURCE_DIR / "P8_Y5_R2FR_3172_CHANNEL_STATUS.csv"
CONTRACT_3172 = SOURCE_DIR / "P8_Y5_R2FR_3172_CLOSURE_CONTRACT.csv"
DECISION_3172 = SOURCE_DIR / "P8_Y5_R2FR_3172_DECISION.csv"
AUDIT_3171 = SOURCE_DIR / "P8_Y5_R2FR_3171_PROFILE_OWNER_AUDIT.csv"
UPSILON_3171 = SOURCE_DIR / "P8_Y5_R2FR_3171_UPSILON_J2_TRANSFER_CONTRACT.csv"
NORM_3170 = SOURCE_DIR / "P8_Y5_R2FR_3170_SOLAR_J2_NORMALIZATION_DERIVATION.csv"
BOUNDS_3170 = SOURCE_DIR / "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv"
CK2_3165 = SOURCE_DIR / "P8_Y5_R2FR_3165_K2_UNIT_RESIDUAL_COEFFICIENT.csv"
RESIDUAL_1955 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1955_RESIDUAL_L2_BOUND_LEDGER.csv"
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


def csv_lookup(path: Path, key: str, key_value: str, column: str) -> str:
    for row in read_csv(path):
        if row.get(key) == key_value:
            return row[column]
    raise KeyError(f"missing {key}={key_value} in {path}")


def numeric_inputs() -> Dict[str, float]:
    return {
        "corrected_half": float(
            csv_lookup(
                BOUNDS_3170,
                "bound_id",
                "CJ3170_2_Rozelot_half_range_proxy",
                "K2_corrected_surface_bound",
            )
        ),
        "c_k2_unit": float(csv_lookup(CK2_3165, "unit_id", "KU3165_0_definition", "value")),
        "two_epsilon": float(
            csv_lookup(
                NORM_3170,
                "derivation_id",
                "JN3170_1_corrected_J2eff_map",
                "two_epsilon_sun_surface",
            )
        ),
    }


def source_specs() -> List[Dict[str, object]]:
    return [
        {
            "source_id": "SRC4483_00_next4482",
            "ref": NEXT_4482,
            "needle": "4483-Y5-R2FR-public-metric-radial-Green-owner-or-finite-l2-scorer-input-fill.md",
            "role": "4482 selected the public Green/profile owner or finite l2 scorer input fill.",
        },
        {
            "source_id": "SRC4483_01_formal4482",
            "ref": FORMAL_4482,
            "needle": "exterior `r^-3` Green/profile owner",
            "role": "4482 formal handoff naming the open Green/profile owner.",
        },
        {
            "source_id": "SRC4483_02_owner4482",
            "ref": OWNER_4482,
            "needle": "OI4482_2_Green_profile",
            "role": "4482 owner input rows for Green, Pi_J2_metric and source transfer.",
        },
        {
            "source_id": "SRC4483_03_transfer4482",
            "ref": TRANSFER_4482,
            "needle": "J2T4482_2_corrected_J2eff",
            "role": "4482 corrected symbolic Upsilon_J2 transfer.",
        },
        {
            "source_id": "SRC4483_04_scorer4482",
            "ref": SCORER_4482,
            "needle": "FLS4482_3_residual_l2_after_GR_baseline",
            "role": "4482 residual-l2 scorer bridge.",
        },
        {
            "source_id": "SRC4483_05_doc3172",
            "ref": DOC_3172,
            "needle": "f_2(r) = a r^2 + b r^-3",
            "role": "3172 earlier public radial Green derivation.",
        },
        {
            "source_id": "SRC4483_06_green3172",
            "ref": GREEN_3172,
            "needle": "GO3172_2_l2_solution",
            "role": "3172 machine-readable r^-3 profile row.",
        },
        {
            "source_id": "SRC4483_07_channel3172",
            "ref": CHANNEL_3172,
            "needle": "CS3172_0_public_radial_profile",
            "role": "3172 channel status: public radial profile conditional math pass.",
        },
        {
            "source_id": "SRC4483_08_contract3172",
            "ref": CONTRACT_3172,
            "needle": "CL3172_0_Upsilon_decomposition",
            "role": "3172 Upsilon decomposition contract.",
        },
        {
            "source_id": "SRC4483_09_decision3172",
            "ref": DECISION_3172,
            "needle": "D3172_0_public_Green_profile_result",
            "role": "3172 decision: Green profile derived conditionally.",
        },
        {
            "source_id": "SRC4483_10_audit3171",
            "ref": AUDIT_3171,
            "needle": "PO3171_4_public_metric_injection",
            "role": "3171 missing Pi_J2_metric owner audit.",
        },
        {
            "source_id": "SRC4483_11_upsilon3171",
            "ref": UPSILON_3171,
            "needle": "UJ3171_0_definition",
            "role": "3171 Upsilon_J2 contract.",
        },
        {
            "source_id": "SRC4483_12_norm3170",
            "ref": NORM_3170,
            "needle": "JN3170_1_corrected_J2eff_map",
            "role": "3170 corrected public metric/J2 normalization.",
        },
        {
            "source_id": "SRC4483_13_bounds3170",
            "ref": BOUNDS_3170,
            "needle": "CJ3170_2_Rozelot_half_range_proxy",
            "role": "3170 half-range pressure row.",
        },
        {
            "source_id": "SRC4483_14_ck2_3165",
            "ref": CK2_3165,
            "needle": "KU3165_0_definition",
            "role": "3165 C_K2_unit value.",
        },
        {
            "source_id": "SRC4483_15_residual1955",
            "ref": RESIDUAL_1955,
            "needle": "RB1955_0_residual_bound_formula",
            "role": "1955 fair residual-l2 scorer after GR baseline.",
        },
        {
            "source_id": "SRC4483_16_transfer3169",
            "ref": TRANSFER_3169,
            "needle": "TR3169_2_transfer_blocker",
            "role": "3169 source-domain transfer blocker.",
        },
        {
            "source_id": "SRC4483_17_gate",
            "ref": GATE_PATH,
            "needle": "def radial_green_theorem_rows",
            "role": "4483 helper gate.",
        },
        {
            "source_id": "SRC4483_18_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4483"',
            "role": "4483 generator script.",
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
            "proof_result": "public exterior l=2 radial Green theorem derived: r^2/r^-3 branches and asymptotic-flat r^-3 selection",
            "fallback_result": "finite l2 scorer inputs rewritten with G_ext_l2_surface separated from Pi_J2_metric and T_source",
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
            "public_radial_Green": "derived_conditionally",
            "parent_operator_match": "unsigned",
            "Pi_J2_metric": "missing",
            "T_source": "missing",
            "finite_l2_scorer": "input_pack_sharpened_nonclaim",
            "sharpest_open_clause": "parent_EH_weak_field_operator_or_PiJ2metric_transfer_row",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4483_0",
            "target": NEXT_TARGET,
            "objective": "Derive the parent weak-field exterior operator and public metric projection, or produce explicit nonclaim Pi_J2_metric/T_source transfer rows.",
            "derive_first": "show the parent local equations reduce to the visible EH/Laplace l=2 equation with the same metric readout",
            "fallback": "create source-ready bounded rows for Pi_J2_metric, T_source, boundary l2 and residual-l2 envelopes",
            "risk": "treating the public r^-3 Green theorem as a proof that MTS sources the public metric channel",
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
            "claim": "4483 derives the public exterior l=2 radial Green theorem and separates it from the parent MTS metric/source coupling problem, without claiming local GR or J2 safety.",
            "current_evidence": "4483 source register, radial Green theorem rows, Pi_J2 metric owner clauses, finite scorer input fill, claim gates, decision/status/next CSVs and validation.",
            "status": "private_radial_green_theorem_and_owner_gate_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "promoting the public r^-3 Green theorem into an MTS coupling proof before Pi_J2_metric and T_source are owned.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "parent operator match, public metric projection, source transfer and residual-l2 envelopes remain unsigned",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    green_rows: Sequence[Mapping[str, object]],
    owner_rows: Sequence[Mapping[str, object]],
    scorer_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 499 PPC4161 - Public Metric Radial Green Owner Or Finite L2 Scorer Input Fill

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4483 takes the actual derivation route first.

The exterior public quadrupole profile is now derived cleanly:

```text
Delta[R_l(r)Y_lm] = 0
=> r^2 R_l'' + 2 r R_l' - l(l+1)R_l = 0
=> R_l = a_l r^l + b_l r^(-l-1)
=> R_2 = a r^2 + b r^-3
```

For an isolated asymptotically flat exterior, the growing `r^2` branch is removed, so the public exterior l=2 metric amplitude transports as:

```text
A_metric(r) = A_surface (R_s/r)^3.
```

That moves one thing forward: `G_ext_l2_surface` is not an unknown physics invention. It is `1` at the surface, and `rho^-3` away from it, provided `A_surface` is already a public metric amplitude.

The hard MTS question is now sharper, not hand-waved:

```text
Upsilon_J2 = Pi_J2_metric * T_source * G_ext_l2_surface.
```

So at the solar surface the Green factor is conditionally closed, but `Pi_J2_metric` and `T_source` are still parent-owner clauses. No local-GR, J2, PPN, clock, orbital, R10 or EM claim is promoted here.

## Radial Green Theorem

{table(green_rows)}

## Parent Metric Owner Clauses

{table(owner_rows)}

## Finite Scorer Input Fill

{table(scorer_rows)}

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
    green_rows: Sequence[Mapping[str, object]],
    owner_rows: Sequence[Mapping[str, object]],
    scorer_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4483 Y5/R2FR - Public Metric Radial Green Owner Or Finite L2 Scorer Input Fill

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

4483 derives the exterior public `r^-3` quadrupole Green theorem instead of treating it as a vague missing item. The profile part is conditionally closed in the public weak-field channel; the remaining problem is the parent coupling/projection: `Pi_J2_metric` and `T_source`.

## Green Derivation

{table(green_rows)}

## Owner Clauses

{table(owner_rows)}

## Scorer Inputs

{table(scorer_rows)}

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
    green_rows: Sequence[Mapping[str, object]],
    owner_rows: Sequence[Mapping[str, object]],
    scorer_rows: Sequence[Mapping[str, object]],
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
        "VAL4483_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4483_1_radial_green_derivation_written",
        any(row.get("theorem_id") == "RGT4483_1_power_law_solution" for row in green_rows)
        and any(row.get("theorem_id") == "RGT4483_2_l2_profile_selection" for row in green_rows),
        "power-law and l=2 r^-3 derivation rows exist",
    )
    add(
        "VAL4483_2_green_factor_conditional_not_overclaimed",
        any(
            row.get("input_id") == "FSI4483_0_G_ext_l2_surface"
            and "CONDITIONAL" in str(row.get("status"))
            for row in scorer_rows
        ),
        "Green factor is marked conditional on owning A_surface",
    )
    add(
        "VAL4483_3_parent_owner_blocks_claim",
        any(row.get("clause_id") == "MOC4483_5_verdict" and row.get("status") == "GREEN_DERIVED_PARENT_CHANNEL_NOT_CLOSED" for row in owner_rows),
        "parent metric/source owner verdict blocks claim",
    )
    add(
        "VAL4483_4_projection_source_inputs_explicit",
        any(row.get("input_id") == "FSI4483_1_Pi_J2_metric" and "MISSING" in str(row.get("status")) for row in scorer_rows)
        and any(row.get("input_id") == "FSI4483_2_T_source" and "MISSING" in str(row.get("status")) for row in scorer_rows),
        "Pi_J2_metric and T_source remain explicit missing inputs",
    )
    add(
        "VAL4483_5_composite_transfer_written",
        any(row.get("input_id") == "FSI4483_3_Upsilon_J2" and "Pi_J2_metric*T_source*G_ext_l2_surface" in str(row.get("formula_or_value")) for row in scorer_rows),
        "Upsilon_J2 composite transfer is written",
    )
    add(
        "VAL4483_6_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4483_3_projection_and_source_signed" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR/J2/PPN promotion",
    )
    add(
        "VAL4483_7_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, green_rows, owner_rows, scorer_rows, gates, decisions, statuses, next_targets]
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
    add("VAL4483_8_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4483_9_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4483_10_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-325",
    )
    add(
        "VAL4483_11_spine_and_packet_updated",
        MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH),
        "unification spine and private packet integration contain 4483 markers",
    )
    add(
        "VAL4483_12_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4483_13_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    inputs = numeric_inputs()
    sources = source_rows()
    green_rows = radial_green_theorem_rows(inputs["two_epsilon"])
    owner_rows = metric_owner_clause_rows()
    scorer_rows = finite_scorer_input_rows(inputs["corrected_half"], inputs["c_k2_unit"], inputs["two_epsilon"])
    ledger = decision_ledger_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, green_rows, owner_rows, scorer_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(RADIAL_GREEN_CSV, green_rows)
    write_csv(OWNER_CLAUSES_CSV, owner_rows)
    write_csv(SCORER_INPUT_CSV, scorer_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, green_rows, owner_rows, scorer_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, green_rows, owner_rows, scorer_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4483 Public Metric Radial Green Owner",
        "4483 derives the public exterior l=2 radial Green theorem: the source-free weak-field radial equation gives `R_2=a r^2+b r^-3`, and asymptotic flatness selects the `r^-3` profile. This closes `G_ext_l2_surface=1` only after a public surface amplitude is already owned; it does not supply `Pi_J2_metric` or `T_source`, so the MTS-to-GR local claim remains nonclaim.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4483 Packet Integration",
        "The private packet now splits the old Green/profile gap into a solved public radial theorem and two genuine parent-owner clauses: `Pi_J2_metric` and `T_source`. The next derivation should attack the parent EH/Laplace weak-field operator and metric projection, not collect more J2 bound rows.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        RADIAL_GREEN_CSV,
        OWNER_CLAUSES_CSV,
        SCORER_INPUT_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, green_rows, owner_rows, scorer_rows, gates, decisions, statuses, next_targets, csv_paths)
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
