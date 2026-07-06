from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from k2_source_derivative_inventory_gate import (  # noqa: E402
    claim_gate_rows,
    decision_ledger_rows,
    deltak_tf_rows,
    derivative_inventory_rows,
    first_m2k2_input_rows,
    read_csv,
    source_silence_scorecard_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4486"
CLAIM_ID = "L-328"
MARKER = "PPC4161_K2_SOURCE_DERIVATIVE_INVENTORY_SWEEP_OR_FIRST_M2K2_INPUT_ROW_4486"
PACKET_MARKER = "PPC4161_PACKET_K2_SOURCE_DERIVATIVE_INVENTORY_SWEEP_OR_FIRST_M2K2_INPUT_ROW_4486"
DECISION = "K2_DERIVATIVE_INVENTORY_WRITTEN_FIRST_PROJECTED_M2K2_INPUT_ROW_FILLED_NONCLAIM"
NEXT_TARGET = "4487-Y5-R2FR-Hessian-carrier-adoption-or-DeltaKTF-metric-response-bound.md"

FORMAL_PATH = FORMAL / "502-PPC4161-K2-source-derivative-inventory-sweep-or-first-M2K2-input-row.md"
DOC_PATH = POST / "4486-Y5-R2FR-K2-source-derivative-inventory-sweep-or-first-M2K2-input-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4486_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4486_SOURCE_REGISTER.csv"
INVENTORY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4486_K2_DERIVATIVE_INVENTORY.csv"
SCORECARD_CSV = SOURCE_DIR / "P8_Y5_R2FR_4486_SOURCE_SILENCE_SCORECARD.csv"
M2_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4486_FIRST_M2K2_INPUT_ROW.csv"
DELTAKTF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4486_DELTAKTF_LEAKAGE_INPUT_ROW.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4486_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4486_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4486_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4486_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4486_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "k2_source_derivative_inventory_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4486_K2_source_derivative_inventory_sweep_or_first_M2K2_input_row.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_501 = FORMAL / "501-PPC4161-K2-Hilbert-residual-source-zero-theorem-or-finite-quadrupole-amplitude.md"
NEXT_4485 = SOURCE_DIR / "P8_Y5_R2FR_4485_NEXT_TARGET.csv"
AUDIT_4485 = SOURCE_DIR / "P8_Y5_R2FR_4485_CURRENT_K2_SOURCE_AUDIT.csv"
AMP_4485 = SOURCE_DIR / "P8_Y5_R2FR_4485_FINITE_QUADRUPOLE_AMPLITUDE_ROWS.csv"
INPUT_4485 = SOURCE_DIR / "P8_Y5_R2FR_4485_NEXT_INPUT_ROWS.csv"
THEOREM_4485 = SOURCE_DIR / "P8_Y5_R2FR_4485_K2_SOURCE_SILENCE_THEOREM.csv"
FORMAL_500 = FORMAL / "500-PPC4161-parent-EH-weak-field-operator-signature-or-PiJ2metric-transfer-row.md"
FORMAL_499 = FORMAL / "499-PPC4161-public-metric-radial-Green-owner-or-finite-l2-scorer-input-fill.md"
DOC_3175 = POST / "3175-Y5-R2FR-K2-STF-source-tensor-in-Khat-or-source-backed-bound-row-under-AX1090.md"
AUDIT_3175 = SOURCE_DIR / "P8_Y5_R2FR_3175_K2_SCALAR_TO_TENSOR_AUDIT.csv"
DOC_3177 = POST / "3177-Y5-R2FR-K2-source-moment-normalization-or-direct-STF-comparator-bound-under-AX1090.md"
DOC_3179 = POST / "3179-Y5-R2FR-tracefree-Hessian-K2-kernel-projection-or-DeltaKTF-product-bound-under-AX1090.md"
PROJ_3179 = SOURCE_DIR / "P8_Y5_R2FR_3179_HESSIAN_PROJECTION_DERIVATION.csv"
DOC_3180 = POST / "3180-Y5-R2FR-quadratic-core-boundary-layer-or-DeltaKTF-leakage-bound-under-AX1090.md"
MOMENT_3180 = SOURCE_DIR / "P8_Y5_R2FR_3180_PROJECTED_MOMENT_IDENTITY.csv"
RECAST_3180 = SOURCE_DIR / "P8_Y5_R2FR_3180_PRODUCT_BOUND_RECAST.csv"
LEAK_3180 = SOURCE_DIR / "P8_Y5_R2FR_3180_DELTAKTF_LEAKAGE_REQUIREMENTS.csv"
FORMAL_489 = FORMAL / "489-PPC4161-no-marker-source-extension-proof-or-cell-marker-residual-row.md"
FORMAL_490 = FORMAL / "490-PPC4161-external-readout-no-backreaction-proof-or-marker-coupling-fill.md"
FORMAL_492 = FORMAL / "492-PPC4161-parent-action-inventory-signature-or-lambdaM-projection-map.md"


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
        "product_bound": float(
            csv_lookup(
                RECAST_3180,
                "recast_id",
                "PR3180_CJ3170_2_Rozelot_half_range_proxy",
                "source_bound",
            )
        ),
        "recast_bound": float(
            csv_lookup(
                RECAST_3180,
                "recast_id",
                "PR3180_CJ3170_2_Rozelot_half_range_proxy",
                "recast_bound",
            )
        ),
    }


def source_specs() -> List[Dict[str, object]]:
    return [
        {
            "source_id": "SRC4486_00_next4485",
            "ref": NEXT_4485,
            "needle": "4486-Y5-R2FR-K2-source-derivative-inventory-sweep-or-first-M2K2-input-row.md",
            "role": "4485 selected derivative inventory or first M2K2 input row.",
        },
        {
            "source_id": "SRC4486_01_formal501",
            "ref": FORMAL_501,
            "needle": "partial_sigma E_metric",
            "role": "4485 exact K2 source-derivative identity.",
        },
        {
            "source_id": "SRC4486_02_theorem4485",
            "ref": THEOREM_4485,
            "needle": "KZS4485_1_clean_zero_theorem",
            "role": "4485 clean zero theorem.",
        },
        {
            "source_id": "SRC4486_03_audit4485",
            "ref": AUDIT_4485,
            "needle": "CSA4485_2_residual_equation",
            "role": "4485 current K2 residual source audit.",
        },
        {
            "source_id": "SRC4486_04_amp4485",
            "ref": AMP_4485,
            "needle": "FQA4485_2_hessian_projected_moment",
            "role": "4485 finite Hessian candidate branch.",
        },
        {
            "source_id": "SRC4486_05_input4485",
            "ref": INPUT_4485,
            "needle": "NI4485_4_DeltaK_TF",
            "role": "4485 next input row for DeltaK_TF.",
        },
        {
            "source_id": "SRC4486_06_formal500",
            "ref": FORMAL_500,
            "needle": "Box hbar_munu = -2 kappa_eff T_H_munu - 2 E_res_munu",
            "role": "4484 EH weak-field source operator.",
        },
        {
            "source_id": "SRC4486_07_formal499",
            "ref": FORMAL_499,
            "needle": "R_2 = a r^2 + b r^-3",
            "role": "4483 public exterior l=2 Green profile.",
        },
        {
            "source_id": "SRC4486_08_doc3175",
            "ref": DOC_3175,
            "needle": "S_K2_STF",
            "role": "3175 K2 STF source tensor target.",
        },
        {
            "source_id": "SRC4486_09_audit3175",
            "ref": AUDIT_3175,
            "needle": "AUD3175_3_Khat_action",
            "role": "3175 Khat action/source owner gap.",
        },
        {
            "source_id": "SRC4486_10_doc3177",
            "ref": DOC_3177,
            "needle": "M2_K2",
            "role": "3177 source moment normalization.",
        },
        {
            "source_id": "SRC4486_11_doc3179",
            "ref": DOC_3179,
            "needle": "D2[F]",
            "role": "3179 tracefree-Hessian projection derivation.",
        },
        {
            "source_id": "SRC4486_12_proj3179",
            "ref": PROJ_3179,
            "needle": "HP3179_2_angular_average_projection",
            "role": "3179 machine-readable projection row.",
        },
        {
            "source_id": "SRC4486_13_doc3180",
            "ref": DOC_3180,
            "needle": "M2_K2^proj",
            "role": "3180 projected moment and product-bound recast.",
        },
        {
            "source_id": "SRC4486_14_moment3180",
            "ref": MOMENT_3180,
            "needle": "MID3180_3_candidate_M2",
            "role": "3180 candidate M2 formula.",
        },
        {
            "source_id": "SRC4486_15_recast3180",
            "ref": RECAST_3180,
            "needle": "PR3180_CJ3170_2_Rozelot_half_range_proxy",
            "role": "3180 tight product-bound recast.",
        },
        {
            "source_id": "SRC4486_16_leak3180",
            "ref": LEAK_3180,
            "needle": "DL3180_2_parent_adoption",
            "role": "3180 DeltaK_TF leakage requirements.",
        },
        {
            "source_id": "SRC4486_17_formal489",
            "ref": FORMAL_489,
            "needle": "delta S_bulk/delta R_obs = 0",
            "role": "4473 no marker/source extension contract.",
        },
        {
            "source_id": "SRC4486_18_formal490",
            "ref": FORMAL_490,
            "needle": "no bulk equation, no Hilbert stress",
            "role": "4474 external readout no-backreaction lemma.",
        },
        {
            "source_id": "SRC4486_19_formal492",
            "ref": FORMAL_492,
            "needle": "PAI4476_0_parent_action_alphabet",
            "role": "4476 parent action inventory signature.",
        },
        {
            "source_id": "SRC4486_20_gate",
            "ref": GATE_PATH,
            "needle": "def derivative_inventory_rows",
            "role": "4486 helper gate.",
        },
        {
            "source_id": "SRC4486_21_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4486"',
            "role": "4486 generator script.",
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
            "proof_result": "K2 metric-response inventory written as four explicit derivative channels; current artifact source silence retained without parent overclaim.",
            "fallback_result": "first symbolic finite M2_K2 projected Hessian input row and DeltaK_TF leakage row are filled for the next coupling/adoption hunt.",
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
            "current_artifact_source_silence": "retained",
            "parent_global_source_silence": "unsigned",
            "first_finite_M2K2_input": "M2_K2^proj=(4/25)kappa_STF*c_ext",
            "DeltaK_TF_status": "zero_or_bound_missing",
            "local_GR_claim": False,
            "sharpest_open_clause": "K_L_to_live_Khat_adoption_or_DeltaK_TF_metric_response_bound",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4486_0",
            "target": NEXT_TARGET,
            "objective": "Decide whether the Hessian carrier K_L is a live parent K_hat source, metric-null, or a finite DeltaK_TF leakage residual.",
            "derive_first": "prove K_L descends as live K_hat with zero non-Y tensor leakage or prove the carrier is metric-null",
            "fallback": "fill DeltaK_TF metric-response bound rows for J2/PPN/clock/orbital comparison",
            "risk": "using the projected M2_K2 row while ignoring full tensor-harmonic leakage",
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
            "claim": "4486 converts the K2 coupling problem into an explicit source-derivative inventory and fills the first symbolic projected M2_K2 Hessian input row, while keeping local-GR/J2/PPN/R10 claims blocked by parent adoption and DeltaK_TF leakage.",
            "current_evidence": "4486 source register, K2 derivative inventory, source-silence scorecard, first M2K2 input rows, DeltaKTF leakage rows, gates, decision/status/next CSVs and validation.",
            "status": "private_K2_source_inventory_first_projected_M2K2_input_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "treating the projected M2_K2 candidate as a live source before K_L is parent-adopted and DeltaK_TF leakage is zeroed or bounded.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "parent global source silence, live Khat adoption, source-domain transfer and DeltaK_TF leakage remain unsigned",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    inventory: Sequence[Mapping[str, object]],
    scorecard: Sequence[Mapping[str, object]],
    m2_rows: Sequence[Mapping[str, object]],
    leakage_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 502 PPC4161 - K2 Source Derivative Inventory Sweep Or First M2K2 Input Row

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4486 takes the coupling fork seriously.

The derivative inventory is now exact:

```text
delta_sigma A_surface
  = P_surf,l2 G_EH[
      kappa_eff partial_sigma T_H
    + partial_sigma E_res
    + partial_sigma B_l2
    + partial_sigma R_readout
    ].
```

So `K2` cannot enter the public metric by mood, analogy, or hidden cancellation. It must enter through Hilbert stress, residual equations, boundary/matching data, or readout deformation.

The current owned artifact remains source-silent: no owned `deltaT_H_K2`, `deltaE_res_K2`, `deltaB_l2`, or `deltaReadout_l2` is present. That blocks fake public `J2` amplitude use, but it still does not prove global parent source silence.

The finite branch also moved forward. The first source-ready symbolic input row is:

```text
M2_K2^proj = (4/25) kappa_STF c_ext.
```

Inserted into the signed source-moment branch:

```text
A_surface_K2^proj
  = s_K2 C_K2_unit (4/25) kappa_STF c_ext.
```

With the tight carried bound:

```text
|s_K2 kappa_STF c_ext| <= {m2_rows[3]["formula"].split(" <= ", 1)[1]}.
```

This is not a claim. It is a usable finite scorer row. The live obstruction is now precise:

```text
DeltaK_TF^{{ij}} := K_L^{{<ij>}} - P_Y[K_L]^{{ij}}.
```

Either the parent makes `K_L` a live metric source and zeroes/bounds `DeltaK_TF`, or the Hessian route cannot be used for local-GR/J2 safety.

## K2 Derivative Inventory

{table(inventory)}

## Source-Silence Scorecard

{table(scorecard)}

## First M2K2 Input Rows

{table(m2_rows)}

## DeltaKTF Leakage Rows

{table(leakage_rows)}

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
    inventory: Sequence[Mapping[str, object]],
    scorecard: Sequence[Mapping[str, object]],
    m2_rows: Sequence[Mapping[str, object]],
    leakage_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4486 Y5/R2FR - K2 Source Derivative Inventory Sweep Or First M2K2 Input Row

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

4486 stops the K2 coupling issue being vague. It writes the exact source-derivative inventory and fills the first finite symbolic scorer row: `M2_K2^proj=(4/25)kappa_STF*c_ext`. The current K2 artifact remains source-silent, but the finite Hessian route is not dead; it is now gated by live `K_L -> K_hat` adoption and `DeltaK_TF`.

## Inventory

{table(inventory)}

## Scorecard

{table(scorecard)}

## M2K2 Rows

{table(m2_rows)}

## Leakage Rows

{table(leakage_rows)}

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
    inventory: Sequence[Mapping[str, object]],
    scorecard: Sequence[Mapping[str, object]],
    m2_rows: Sequence[Mapping[str, object]],
    leakage_rows: Sequence[Mapping[str, object]],
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
        "VAL4486_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4486_1_inventory_identity_written",
        any(row.get("inventory_id") == "KDI4486_0_master_variation" for row in inventory),
        "master K2 source-derivative inventory exists",
    )
    add(
        "VAL4486_2_four_channels_present",
        all(
            channel in {str(row.get("source_channel")) for row in inventory}
            for channel in ["partial_sigma T_H", "partial_sigma E_res", "partial_sigma B_l2", "partial_sigma R_readout"]
        ),
        "Hilbert, residual, boundary and readout channels are all present",
    )
    add(
        "VAL4486_3_parent_zero_not_overclaimed",
        any("PARENT_GLOBAL_ZERO_UNSIGNED" in str(row.get("proof_level")) for row in scorecard),
        "parent global source silence remains unsigned",
    )
    add(
        "VAL4486_4_first_m2k2_input_filled",
        any(row.get("input_id") == "M2I4486_0_projected_hessian_moment" and "(4/25)" in str(row.get("formula")) for row in m2_rows),
        "projected Hessian M2_K2 symbolic input row exists",
    )
    add(
        "VAL4486_5_recast_product_bound_filled",
        any(row.get("input_id") == "M2I4486_3_recast_hessian_product_bound" and "2.436252730681616e+11" in str(row.get("formula")) for row in m2_rows),
        "tight recast product bound is carried",
    )
    add(
        "VAL4486_6_deltak_tf_row_filled",
        any(row.get("leak_id") == "DTF4486_0_definition" and "DeltaK_TF" in str(row.get("quantity")) for row in leakage_rows),
        "DeltaK_TF leakage row exists",
    )
    add(
        "VAL4486_7_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4486_4_deltak_tf_not_silenced" and str(row.get("gate_pass")).lower() == "true" for row in gates),
        "claim gates block local-GR/J2 promotion while leakage remains open",
    )
    add(
        "VAL4486_8_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, inventory, scorecard, m2_rows, leakage_rows, gates, decisions, statuses, next_targets]
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
    add("VAL4486_9_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4486_10_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4486_11_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-328",
    )
    add(
        "VAL4486_12_spine_and_packet_updated",
        MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH),
        "unification spine and private packet integration contain 4486 markers",
    )
    add(
        "VAL4486_13_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4486_14_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    inputs = numeric_inputs()
    sources = source_rows()
    inventory = derivative_inventory_rows()
    scorecard = source_silence_scorecard_rows()
    m2_rows = first_m2k2_input_rows(inputs["product_bound"], inputs["recast_bound"])
    leakage_rows = deltak_tf_rows()
    ledger = decision_ledger_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, inventory, scorecard, m2_rows, leakage_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(INVENTORY_CSV, inventory)
    write_csv(SCORECARD_CSV, scorecard)
    write_csv(M2_INPUT_CSV, m2_rows)
    write_csv(DELTAKTF_CSV, leakage_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, inventory, scorecard, m2_rows, leakage_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, inventory, scorecard, m2_rows, leakage_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4486 K2 Source Derivative Inventory And First M2K2 Input",
        "4486 writes the exact K2 metric-response inventory `delta_sigma A_surface=P_surf,l2 G_EH[kappa_eff partial_sigma T_H+partial_sigma E_res+partial_sigma B_l2+partial_sigma R_readout]`. The current K2 artifact remains source-silent but the global parent-zero theorem is unsigned. The finite branch now has the first symbolic scorer row `M2_K2^proj=(4/25)kappa_STF c_ext`, with `DeltaK_TF` identified as the live leakage/adoption obstruction.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4486 Packet Integration",
        "The private packet now treats the coupling problem as a four-channel derivative inventory rather than a vague missing input. The first projected finite `M2_K2` row is filled, but no public local-GR/J2/PPN/R10 claim is allowed until `K_L` is adopted as live `K_hat` or proved metric-null and `DeltaK_TF` is zeroed or bounded.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        INVENTORY_CSV,
        SCORECARD_CSV,
        M2_INPUT_CSV,
        DELTAKTF_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, inventory, scorecard, m2_rows, leakage_rows, gates, decisions, statuses, next_targets, csv_paths)
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
