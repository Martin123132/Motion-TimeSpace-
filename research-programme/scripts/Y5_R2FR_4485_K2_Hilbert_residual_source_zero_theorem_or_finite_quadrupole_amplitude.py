from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from k2_source_silence_quadrupole_gate import (  # noqa: E402
    claim_gate_rows,
    current_source_audit_rows,
    finite_quadrupole_rows,
    next_input_rows,
    read_csv,
    source_silence_theorem_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4485"
CLAIM_ID = "L-327"
MARKER = "PPC4161_K2_HILBERT_RESIDUAL_SOURCE_ZERO_THEOREM_OR_FINITE_QUADRUPOLE_AMPLITUDE_4485"
PACKET_MARKER = "PPC4161_PACKET_K2_HILBERT_RESIDUAL_SOURCE_ZERO_THEOREM_OR_FINITE_QUADRUPOLE_AMPLITUDE_4485"
DECISION = "CURRENT_OWNED_K2_SOURCE_RESPONSE_ZERO_FINITE_QUADRUPOLE_BRANCH_RETAINED_NONCLAIM"
NEXT_TARGET = "4486-Y5-R2FR-K2-source-derivative-inventory-sweep-or-first-M2K2-input-row.md"

FORMAL_PATH = FORMAL / "501-PPC4161-K2-Hilbert-residual-source-zero-theorem-or-finite-quadrupole-amplitude.md"
DOC_PATH = POST / "4485-Y5-R2FR-K2-Hilbert-residual-source-zero-theorem-or-finite-quadrupole-amplitude.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4485_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4485_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4485_K2_SOURCE_SILENCE_THEOREM.csv"
AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4485_CURRENT_K2_SOURCE_AUDIT.csv"
AMPLITUDE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4485_FINITE_QUADRUPOLE_AMPLITUDE_ROWS.csv"
INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4485_NEXT_INPUT_ROWS.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4485_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4485_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4485_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4485_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4485_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "k2_source_silence_quadrupole_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4485_K2_Hilbert_residual_source_zero_theorem_or_finite_quadrupole_amplitude.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_4484 = FORMAL / "500-PPC4161-parent-EH-weak-field-operator-signature-or-PiJ2metric-transfer-row.md"
NEXT_4484 = SOURCE_DIR / "P8_Y5_R2FR_4484_NEXT_TARGET.csv"
PI_4484 = SOURCE_DIR / "P8_Y5_R2FR_4484_PIJ2METRIC_TRANSFER_ROWS.csv"
OWNER_4484 = SOURCE_DIR / "P8_Y5_R2FR_4484_K2_SOURCE_OWNER_ROWS.csv"
RESIDUAL_4484 = SOURCE_DIR / "P8_Y5_R2FR_4484_RESIDUAL_INTERFACE_ROWS.csv"
K2_3165 = SOURCE_DIR / "P8_Y5_R2FR_3165_K2_LOCAL_RESIDUAL_VECTOR.csv"
CK2_3165 = SOURCE_DIR / "P8_Y5_R2FR_3165_K2_UNIT_RESIDUAL_COEFFICIENT.csv"
DOC_3175 = POST / "3175-Y5-R2FR-K2-STF-source-tensor-in-Khat-or-source-backed-bound-row-under-AX1090.md"
AUDIT_3175 = SOURCE_DIR / "P8_Y5_R2FR_3175_K2_SCALAR_TO_TENSOR_AUDIT.csv"
DOC_3176 = POST / "3176-Y5-R2FR-signed-K2-STF-basis-owner-or-source-moment-bound-under-AX1090.md"
DOC_3177 = POST / "3177-Y5-R2FR-K2-source-moment-normalization-or-direct-STF-comparator-bound-under-AX1090.md"
DOC_3178 = POST / "3178-Y5-R2FR-Khat-source-kernel-normalization-or-STF-product-bound-gate-under-AX1090.md"
DOC_3179 = POST / "3179-Y5-R2FR-tracefree-Hessian-K2-kernel-projection-or-DeltaKTF-product-bound-under-AX1090.md"
DOC_3180 = POST / "3180-Y5-R2FR-quadratic-core-boundary-layer-or-DeltaKTF-leakage-bound-under-AX1090.md"
FORMAL_489 = FORMAL / "489-PPC4161-no-marker-source-extension-proof-or-cell-marker-residual-row.md"
FORMAL_490 = FORMAL / "490-PPC4161-external-readout-no-backreaction-proof-or-marker-coupling-fill.md"
FORMAL_492 = FORMAL / "492-PPC4161-parent-action-inventory-signature-or-lambdaM-projection-map.md"
BOUNDS_3170 = SOURCE_DIR / "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv"


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
        "c_k2_unit": float(csv_lookup(CK2_3165, "unit_id", "KU3165_0_definition", "value")),
        "half_bound": float(
            csv_lookup(
                BOUNDS_3170,
                "bound_id",
                "CJ3170_2_Rozelot_half_range_proxy",
                "K2_corrected_surface_bound",
            )
        ),
    }


def source_specs() -> List[Dict[str, object]]:
    return [
        {
            "source_id": "SRC4485_00_next4484",
            "ref": NEXT_4484,
            "needle": "4485-Y5-R2FR-K2-Hilbert-residual-source-zero-theorem-or-finite-quadrupole-amplitude.md",
            "role": "4484 selected K2 source-silence or finite quadrupole amplitude.",
        },
        {
            "source_id": "SRC4485_01_formal4484",
            "ref": FORMAL_4484,
            "needle": "source-silent branch: Pi_J2_metric*K2 = 0;",
            "role": "4484 K2 zero-or-source fork.",
        },
        {
            "source_id": "SRC4485_02_pi4484",
            "ref": PI_4484,
            "needle": "PI4484_2_finite_source_functional",
            "role": "4484 finite source functional.",
        },
        {
            "source_id": "SRC4485_03_owner4484",
            "ref": OWNER_4484,
            "needle": "KSO4484_5_verdict",
            "role": "4484 K2 owner derivative verdict.",
        },
        {
            "source_id": "SRC4485_04_residual4484",
            "ref": RESIDUAL_4484,
            "needle": "RIF4484_0_master_equation",
            "role": "4484 residual interface.",
        },
        {
            "source_id": "SRC4485_05_k2_3165",
            "ref": K2_3165,
            "needle": "RV3165_2",
            "role": "3165 K2 local residual vector tracefree channel.",
        },
        {
            "source_id": "SRC4485_06_ck2_3165",
            "ref": CK2_3165,
            "needle": "KU3165_0_definition",
            "role": "3165 C_K2_unit.",
        },
        {
            "source_id": "SRC4485_07_doc3175",
            "ref": DOC_3175,
            "needle": "S_K2_STF",
            "role": "3175 exact K2 STF target tensor.",
        },
        {
            "source_id": "SRC4485_08_audit3175",
            "ref": AUDIT_3175,
            "needle": "AUD3175_3_Khat_action",
            "role": "3175 Khat action/source-owner audit.",
        },
        {
            "source_id": "SRC4485_09_doc3176",
            "ref": DOC_3176,
            "needle": "P2(a.n) = (3/2) Y_a",
            "role": "3176 STF angular lift.",
        },
        {
            "source_id": "SRC4485_10_doc3177",
            "ref": DOC_3177,
            "needle": "M2_K2",
            "role": "3177 compact source moment.",
        },
        {
            "source_id": "SRC4485_11_doc3178",
            "ref": DOC_3178,
            "needle": "No live source-owned K_hat source kernel is found.",
            "role": "3178 no live Khat source kernel.",
        },
        {
            "source_id": "SRC4485_12_doc3179",
            "ref": DOC_3179,
            "needle": "D2[F]",
            "role": "3179 tracefree Hessian projection.",
        },
        {
            "source_id": "SRC4485_13_doc3180",
            "ref": DOC_3180,
            "needle": "projected source moment closes conditionally",
            "role": "3180 conditional projected moment and leakage warning.",
        },
        {
            "source_id": "SRC4485_14_formal489",
            "ref": FORMAL_489,
            "needle": "delta S_bulk/delta R_obs = 0",
            "role": "4473 no marker/source extension contract.",
        },
        {
            "source_id": "SRC4485_15_formal490",
            "ref": FORMAL_490,
            "needle": "no bulk equation, no Hilbert stress",
            "role": "4474 external readout no-backreaction theorem.",
        },
        {
            "source_id": "SRC4485_16_formal492",
            "ref": FORMAL_492,
            "needle": "PAI4476_0_parent_action_alphabet",
            "role": "4476 parent action inventory signature.",
        },
        {
            "source_id": "SRC4485_17_bounds3170",
            "ref": BOUNDS_3170,
            "needle": "CJ3170_2_Rozelot_half_range_proxy",
            "role": "3170 pressure row carried into product bound.",
        },
        {
            "source_id": "SRC4485_18_gate",
            "ref": GATE_PATH,
            "needle": "def source_silence_theorem_rows",
            "role": "4485 helper gate.",
        },
        {
            "source_id": "SRC4485_19_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4485"',
            "role": "4485 generator script.",
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


def decision_ledger_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4485_0_zero_branch",
            "finding": "current source-owned K2 derivative is absent",
            "reason": "K2 is a residual/projection lane, and no parent-owned Hilbert/residual/boundary/readout derivative is present",
            "effect": "the current owned K2 lane cannot be used as a public J2 metric source",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4485_1_parent_zero_not_global",
            "finding": "the global parent source-silence claim is still unsigned",
            "reason": "the parent action inventory, readout role, boundary routing and source-domain transfer are not globally signed",
            "effect": "source-silent branch remains private/conditional rather than a public local-GR pass",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4485_2_finite_branch",
            "finding": "finite quadrupole amplitude branch is retained with exact functional form",
            "reason": "3176-3180 define the signed STF/moment/Hessian product route but leave source owner and leakage inputs missing",
            "effect": "next work can sweep for K2 derivatives or fill first M2_K2/DeltaK_TF input rows",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "proof_result": "K2 source-silence theorem written; current owned K2 source response is zero/absent",
            "fallback_result": "finite A_surface_K2 branch retained as EH Green functional and signed STF source-moment product",
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
            "current_owned_K2_source_response": "zero_or_absent",
            "parent_global_source_silence": "unsigned",
            "finite_quadrupole_amplitude": "functional_written_inputs_missing",
            "local_GR_claim": False,
            "sharpest_open_clause": "K2_source_derivative_inventory_or_first_M2K2_input",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4485_0",
            "target": NEXT_TARGET,
            "objective": "Run a targeted K2 source-derivative inventory and either sign the source-silent branch or fill the first finite M2_K2/DeltaK_TF input row.",
            "derive_first": "prove sigma_K2 is absent from S_src, S_extra, boundary and readout at the parent action level",
            "fallback": "extract a source-backed finite derivative: deltaT_H_K2, deltaE_res_K2, deltaB_l2, deltaReadout_l2, M2_K2 or DeltaK_TF",
            "risk": "treating absence of current source rows as a universal parent theorem",
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
            "claim": "4485 proves the conditional K2 source-silence theorem for the same-frame EH equation, audits that the current owned K2 artifact has no source derivative, and retains a finite quadrupole amplitude branch without claiming local GR or J2 safety.",
            "current_evidence": "4485 source register, K2 source-silence theorem rows, current source audit, finite quadrupole amplitude rows, input rows, claim gates, decision/status/next CSVs and validation.",
            "status": "private_K2_source_silence_theorem_and_finite_quadrupole_branch_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "turning absence of current source rows into a global parent theorem, or using the finite branch before M2_K2/DeltaK_TF is sourced.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "parent global source silence, source-domain transfer and finite K2 quadrupole inputs remain unsigned",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    theorem_rows: Sequence[Mapping[str, object]],
    audit_rows: Sequence[Mapping[str, object]],
    amplitude_rows: Sequence[Mapping[str, object]],
    input_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 501 PPC4161 - K2 Hilbert Residual Source Zero Theorem Or Finite Quadrupole Amplitude

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4485 attacks the source question directly.

Let:

```text
sigma_K2 = K2*C_K2_unit.
```

In the same-frame EH branch, the only way `K2` can source a public quadrupole is:

```text
partial_sigma E_metric
= kappa_eff partial_sigma T_H
 + partial_sigma E_res
 + partial_sigma B_l2
 + partial_sigma R_readout.
```

Therefore the exact zero theorem is:

```text
partial_sigma T_H
= partial_sigma E_res
= partial_sigma B_l2
= partial_sigma R_readout
= 0
=> A_surface_K2 = 0.
```

The current corpus does not contain a source-owned `deltaT_H_K2`, `deltaE_res_K2`, boundary derivative, or readout derivative. So the current owned K2 artifact is not allowed to masquerade as a public J2 metric source.

That is a real cleanup, but not a public local-GR claim. The global parent theorem is still unsigned because the parent action inventory/readout/boundary/source-domain signatures are not globally closed.

The finite branch is retained and made explicit:

```text
A_surface_K2
= P_surf,l2 G_EH[
    kappa_eff deltaT_H_K2
  + deltaE_res_K2
  + deltaB_l2
  + deltaReadout_l2
  ].
```

For the signed STF source-moment branch:

```text
A_surface_K2 = s_K2*C_K2_unit*M2_K2.
```

No local-GR, J2, PPN, R10, clock, orbital or EM claim is promoted.

## K2 Source-Silence Theorem

{table(theorem_rows)}

## Current Source Audit

{table(audit_rows)}

## Finite Quadrupole Amplitude Rows

{table(amplitude_rows)}

## Next Input Rows

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
    theorem_rows: Sequence[Mapping[str, object]],
    audit_rows: Sequence[Mapping[str, object]],
    amplitude_rows: Sequence[Mapping[str, object]],
    input_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4485 Y5/R2FR - K2 Hilbert Residual Source Zero Theorem Or Finite Quadrupole Amplitude

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

4485 stops `K2` being treated as a mystery source. If it is absent from Hilbert stress, residual equations, boundary data and readout, the metric response is zero. If it is present, its public quadrupole amplitude must be the EH Green functional of the sourced derivatives, or the signed STF source-moment product `s_K2*C_K2_unit*M2_K2`.

## Source-Silence Theorem

{table(theorem_rows)}

## Current Audit

{table(audit_rows)}

## Finite Branch

{table(amplitude_rows)}

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
    theorem_rows: Sequence[Mapping[str, object]],
    audit_rows: Sequence[Mapping[str, object]],
    amplitude_rows: Sequence[Mapping[str, object]],
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
        "VAL4485_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4485_1_source_silence_theorem_written",
        any(row.get("theorem_id") == "KZS4485_1_clean_zero_theorem" for row in theorem_rows),
        "source-silence theorem exists",
    )
    add(
        "VAL4485_2_current_owned_source_audit_written",
        any(row.get("theorem_id") == "KZS4485_2_current_artifact_audit" for row in theorem_rows)
        and any(row.get("audit_id") == "CSA4485_2_residual_equation" for row in audit_rows),
        "current owned source audit exists",
    )
    add(
        "VAL4485_3_finite_branch_functional_written",
        any(row.get("amp_id") == "FQA4485_0_general_functional" for row in amplitude_rows)
        and any(row.get("amp_id") == "FQA4485_1_signed_source_moment" for row in amplitude_rows),
        "finite quadrupole functional and signed source-moment branch exist",
    )
    add(
        "VAL4485_4_parent_global_zero_not_overclaimed",
        any(
            row.get("theorem_id") == "KZS4485_5_verdict"
            and "GLOBAL_PARENT_ZERO_UNSIGNED" in str(row.get("current_status"))
            for row in theorem_rows
        ),
        "global parent source-silence is not overclaimed",
    )
    add(
        "VAL4485_5_missing_inputs_explicit",
        any(row.get("input_id") == "NI4485_2_deltaE_res_K2" and "MISSING" in str(row.get("current_value")) for row in input_rows)
        and any(row.get("input_id") == "NI4485_4_DeltaK_TF" and "MISSING" in str(row.get("current_value")) for row in input_rows),
        "finite branch missing inputs are explicit",
    )
    add(
        "VAL4485_6_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4485_3_parent_global_zero_signed" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR/J2 promotion",
    )
    add(
        "VAL4485_7_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, theorem_rows, audit_rows, amplitude_rows, input_rows, gates, decisions, statuses, next_targets]
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
    add("VAL4485_8_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4485_9_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4485_10_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-327",
    )
    add(
        "VAL4485_11_spine_and_packet_updated",
        MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH),
        "unification spine and private packet integration contain 4485 markers",
    )
    add(
        "VAL4485_12_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4485_13_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    inputs = numeric_inputs()
    sources = source_rows()
    theorem_rows = source_silence_theorem_rows()
    audit_rows = current_source_audit_rows()
    amplitude_rows = finite_quadrupole_rows(inputs["c_k2_unit"], inputs["half_bound"])
    input_rows = next_input_rows()
    ledger = decision_ledger_rows()
    gates = claim_gate_rows(sources, theorem_rows, audit_rows, amplitude_rows, input_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem_rows)
    write_csv(AUDIT_CSV, audit_rows)
    write_csv(AMPLITUDE_CSV, amplitude_rows)
    write_csv(INPUT_CSV, input_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, theorem_rows, audit_rows, amplitude_rows, input_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, theorem_rows, audit_rows, amplitude_rows, input_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4485 K2 Source Silence Or Finite Quadrupole",
        "4485 proves the conditional K2 source-silence theorem: if `sigma_K2` is absent from Hilbert stress, residual equations, boundary data and readout, then `A_surface_K2=0`. The current owned K2 artifact has no source derivative, so it cannot be used as a public J2 metric source. The global parent-zero claim remains unsigned; the finite fallback is `A_surface_K2=P_surf,l2 G_EH[kappa_eff deltaT_H_K2+deltaE_res_K2+deltaB_l2+deltaReadout_l2]` or `s_K2*C_K2_unit*M2_K2`.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4485 Packet Integration",
        "The private packet now distinguishes current-owned K2 source response from a global parent theorem. Current K2 is source-silent as an owned artifact, but finite source branches stay live until `deltaT_H_K2`, `deltaE_res_K2`, `M2_K2`, `DeltaK_TF` and source-domain transfer are zeroed or sourced.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        AUDIT_CSV,
        AMPLITUDE_CSV,
        INPUT_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, theorem_rows, audit_rows, amplitude_rows, input_rows, gates, decisions, statuses, next_targets, csv_paths)
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
