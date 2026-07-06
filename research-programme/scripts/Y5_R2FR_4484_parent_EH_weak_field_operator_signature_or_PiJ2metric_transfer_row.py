from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from parent_eh_weak_field_operator_gate import (  # noqa: E402
    claim_gate_rows,
    eh_weak_field_rows,
    k2_source_owner_rows,
    pij2_transfer_rows,
    read_csv,
    residual_interface_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4484"
CLAIM_ID = "L-326"
MARKER = "PPC4161_PARENT_EH_WEAK_FIELD_OPERATOR_SIGNATURE_OR_PIJ2METRIC_TRANSFER_ROW_4484"
PACKET_MARKER = "PPC4161_PACKET_PARENT_EH_WEAK_FIELD_OPERATOR_SIGNATURE_OR_PIJ2METRIC_TRANSFER_ROW_4484"
DECISION = "EH_WEAK_FIELD_OPERATOR_CONDITIONAL_PIJ2_ZERO_OR_SOURCE_FUNCTIONAL_NONCLAIM"
NEXT_TARGET = "4485-Y5-R2FR-K2-Hilbert-residual-source-zero-theorem-or-finite-quadrupole-amplitude.md"

FORMAL_PATH = FORMAL / "500-PPC4161-parent-EH-weak-field-operator-signature-or-PiJ2metric-transfer-row.md"
DOC_PATH = POST / "4484-Y5-R2FR-parent-EH-weak-field-operator-signature-or-PiJ2metric-transfer-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4484_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4484_SOURCE_REGISTER.csv"
EH_WEAK_FIELD_CSV = SOURCE_DIR / "P8_Y5_R2FR_4484_EH_WEAK_FIELD_OPERATOR_SIGNATURE.csv"
PIJ2_CSV = SOURCE_DIR / "P8_Y5_R2FR_4484_PIJ2METRIC_TRANSFER_ROWS.csv"
K2_OWNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4484_K2_SOURCE_OWNER_ROWS.csv"
RESIDUAL_INTERFACE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4484_RESIDUAL_INTERFACE_ROWS.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4484_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4484_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4484_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4484_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4484_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "parent_eh_weak_field_operator_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4484_parent_EH_weak_field_operator_signature_or_PiJ2metric_transfer_row.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_4483 = FORMAL / "499-PPC4161-public-metric-radial-Green-owner-or-finite-l2-scorer-input-fill.md"
NEXT_4483 = SOURCE_DIR / "P8_Y5_R2FR_4483_NEXT_TARGET.csv"
GREEN_4483 = SOURCE_DIR / "P8_Y5_R2FR_4483_RADIAL_GREEN_THEOREM.csv"
OWNER_4483 = SOURCE_DIR / "P8_Y5_R2FR_4483_PI_J2_METRIC_OWNER_CLAUSES.csv"
SCORER_4483 = SOURCE_DIR / "P8_Y5_R2FR_4483_FINITE_SCORER_INPUT_FILL.csv"
DOC_3173 = POST / "3173-Y5-R2FR-parent-exterior-operator-match-or-PiJ2metric-source-row-under-AX1090.md"
OP_3173 = SOURCE_DIR / "P8_Y5_R2FR_3173_OPERATOR_MATCH_DERIVATION.csv"
EX_3173 = SOURCE_DIR / "P8_Y5_R2FR_3173_PIJ2_EXTRACTOR_CONTRACT.csv"
SRCROW_3173 = SOURCE_DIR / "P8_Y5_R2FR_3173_SOURCE_READY_NONCLAIM_ROWS.csv"
EH_4086 = SOURCE_DIR / "P8_Y5_R2FR_4086_EH_SIGNATURE_THEOREM.csv"
PROJ_4086 = SOURCE_DIR / "P8_Y5_R2FR_4086_NONEH_PPN_PROJECTION_FORMULAS.csv"
CHAIN_4070 = SOURCE_DIR / "P8_Y5_R2FR_4070_EH_REDUCTION_CHAIN.csv"
RED_4072 = SOURCE_DIR / "P8_Y5_R2FR_4072_EH_NEWTON_PPN_REDUCTION_CONTRACT.csv"
EHP_3818 = SOURCE_DIR / "P8_Y5_R2FR_3818_EH_METRIC_EQUATION_TEMPLATE.csv"
NEWTON_4151 = SOURCE_DIR / "P8_Y5_R2FR_4151_EH_ONLY_NEWTON_THEOREM.csv"
LHD_4278 = SOURCE_DIR / "P8_Y5_R2FR_4278_LEFT_HAND_EH_NEWTON_DERIVATION.csv"
FORMAL_294 = FORMAL / "294-PPC4161-left-hand-EH-Newton-limit-or-residual-EFT-bound-gate.md"
CK2_3165 = SOURCE_DIR / "P8_Y5_R2FR_3165_K2_UNIT_RESIDUAL_COEFFICIENT.csv"
NORM_3170 = SOURCE_DIR / "P8_Y5_R2FR_3170_SOLAR_J2_NORMALIZATION_DERIVATION.csv"
BOUNDS_3170 = SOURCE_DIR / "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv"
RESIDUAL_1955 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1955_RESIDUAL_L2_BOUND_LEDGER.csv"


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
        "two_epsilon": float(
            csv_lookup(
                NORM_3170,
                "derivation_id",
                "JN3170_1_corrected_J2eff_map",
                "two_epsilon_sun_surface",
            )
        ),
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
            "source_id": "SRC4484_00_next4483",
            "ref": NEXT_4483,
            "needle": "4484-Y5-R2FR-parent-EH-weak-field-operator-signature-or-PiJ2metric-transfer-row.md",
            "role": "4483 selected parent weak-field operator or PiJ2 transfer row.",
        },
        {
            "source_id": "SRC4484_01_formal4483",
            "ref": FORMAL_4483,
            "needle": "Upsilon_J2 = Pi_J2_metric * T_source * G_ext_l2_surface",
            "role": "4483 hard coupling split.",
        },
        {
            "source_id": "SRC4484_02_green4483",
            "ref": GREEN_4483,
            "needle": "RGT4483_5_verdict",
            "role": "4483 public Green theorem verdict.",
        },
        {
            "source_id": "SRC4484_03_owner4483",
            "ref": OWNER_4483,
            "needle": "MOC4483_0_parent_EH_operator",
            "role": "4483 parent operator owner clause.",
        },
        {
            "source_id": "SRC4484_04_scorer4483",
            "ref": SCORER_4483,
            "needle": "FSI4483_3_Upsilon_J2",
            "role": "4483 Upsilon factorization row.",
        },
        {
            "source_id": "SRC4484_05_doc3173",
            "ref": DOC_3173,
            "needle": "Upsilon_J2 = - P_surf,l2 E_metric L_parent^-1 S_K2",
            "role": "3173 exact extractor formula.",
        },
        {
            "source_id": "SRC4484_06_op3173",
            "ref": OP_3173,
            "needle": "OP3173_3_exact_Upsilon_formula",
            "role": "3173 machine-readable Upsilon operator extractor.",
        },
        {
            "source_id": "SRC4484_07_ex3173",
            "ref": EX_3173,
            "needle": "EX3173_4_compute_kernel",
            "role": "3173 PiJ2 extractor contract.",
        },
        {
            "source_id": "SRC4484_08_srcrow3173",
            "ref": SRCROW_3173,
            "needle": "SRCROW3173_0_Pi_J2_metric",
            "role": "3173 source-ready Pi row.",
        },
        {
            "source_id": "SRC4484_09_eh4086",
            "ref": EH_4086,
            "needle": "EH4086_0_lovelock_selector",
            "role": "4086 EH operator selector theorem.",
        },
        {
            "source_id": "SRC4484_10_proj4086",
            "ref": PROJ_4086,
            "needle": "PROJ4086_0_total",
            "role": "4086 non-EH residual projection interface.",
        },
        {
            "source_id": "SRC4484_11_chain4070",
            "ref": CHAIN_4070,
            "needle": "CHAIN4070_2",
            "role": "4070 EH reduction chain.",
        },
        {
            "source_id": "SRC4484_12_red4072",
            "ref": RED_4072,
            "needle": "RED4072_3_Newton",
            "role": "4072 Newton/PPN reduction contract.",
        },
        {
            "source_id": "SRC4484_13_ehp3818",
            "ref": EHP_3818,
            "needle": "EHP3818_0_public_metric_equation",
            "role": "3818 public metric equation template.",
        },
        {
            "source_id": "SRC4484_14_newton4151",
            "ref": NEWTON_4151,
            "needle": "EHN4151_1_poisson_reduction",
            "role": "4151 EH-only Poisson source normalization theorem.",
        },
        {
            "source_id": "SRC4484_15_lhd4278",
            "ref": LHD_4278,
            "needle": "LHD4278_2_metric_equation",
            "role": "4278 left-hand EH/Newton derivation.",
        },
        {
            "source_id": "SRC4484_16_formal294",
            "ref": FORMAL_294,
            "needle": "G_mu_nu[g_obs] + Lambda_eff g_mu_nu",
            "role": "formal 4278 left-hand EH/Newton gate.",
        },
        {
            "source_id": "SRC4484_17_ck2",
            "ref": CK2_3165,
            "needle": "KU3165_0_definition",
            "role": "C_K2_unit value.",
        },
        {
            "source_id": "SRC4484_18_norm3170",
            "ref": NORM_3170,
            "needle": "JN3170_1_corrected_J2eff_map",
            "role": "public J2 metric normalization.",
        },
        {
            "source_id": "SRC4484_19_bounds3170",
            "ref": BOUNDS_3170,
            "needle": "CJ3170_2_Rozelot_half_range_proxy",
            "role": "J2 half-range pressure row.",
        },
        {
            "source_id": "SRC4484_20_residual1955",
            "ref": RESIDUAL_1955,
            "needle": "RB1955_0_residual_bound_formula",
            "role": "fair residual-l2 scorer.",
        },
        {
            "source_id": "SRC4484_21_gate",
            "ref": GATE_PATH,
            "needle": "def eh_weak_field_rows",
            "role": "4484 helper gate.",
        },
        {
            "source_id": "SRC4484_22_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4484"',
            "role": "4484 generator script.",
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
            "decision_id": "DEC4484_0_operator",
            "finding": "the EH weak-field exterior operator is conditionally derived",
            "reason": "4086/4278 give EH plus residuals; linearization gives the public Laplace l=2 operator when residual/source support is silent",
            "effect": "4483 r^-3 theorem is inherited by the conditional EH branch",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4484_1_K2_fork",
            "finding": "K2 cannot be assumed to source the public metric",
            "reason": "differentiating the EH/residual equation with respect to sigma_K2 gives zero if K2 is absent from Hilbert stress, residual tensor, boundary and readout",
            "effect": "clean branch gives Pi response zero; finite branch needs sourced quadrupole derivatives",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4484_2_best_next",
            "finding": "the next target is K2 Hilbert/residual source ownership",
            "reason": "the operator is no longer the main fog; the source derivative decides whether Upsilon_J2 is zero, finite, or bounded",
            "effect": "derive source-silence theorem first; if it fails, fill finite A_surface_K2 rows",
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
            "proof_result": "conditional EH weak-field operator gives the public exterior l2 Laplace equation under selector/residual silence",
            "fallback_result": "Pi_J2_metric becomes a zero-or-source EH Green functional of K2 Hilbert/residual/boundary/readout derivatives",
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
            "EH_operator_match": "conditional_on_selector_and_residual_silence",
            "Pi_J2_metric": "zero_or_source_functional_not_numeric",
            "K2_source_status": "undecided",
            "T_source": "missing",
            "local_GR_claim": False,
            "sharpest_open_clause": "K2_Hilbert_residual_source_zero_or_finite_quadrupole_amplitude",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4484_0",
            "target": NEXT_TARGET,
            "objective": "Decide whether the K2 lane is source-silent in the same-frame EH equation or compute its finite public quadrupole amplitude.",
            "derive_first": "prove partial_sigma(T_H,E_res,B_l2,g_readout_extra)=0 from the parent action/source grammar",
            "fallback": "fill source-backed rows for deltaT_H_K2, deltaE_res_K2, boundary/readout l2 and T_source, then score A_surface_K2",
            "risk": "assuming K2*C_K2_unit is a public metric amplitude just because the EH operator is conditionally available",
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
            "claim": "4484 conditionally derives the EH weak-field exterior operator and turns Pi_J2_metric into a zero-or-source EH Green functional of K2 source/residual derivatives, without claiming local GR or J2 safety.",
            "current_evidence": "4484 source register, EH weak-field operator signature rows, PiJ2 transfer rows, K2 source owner rows, residual interface rows, claim gates, decision/status/next CSVs and validation.",
            "status": "private_conditional_EH_operator_and_PiJ2_zero_or_source_functional_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "treating K2*C_K2_unit as a public metric amplitude before its Hilbert/residual/boundary/readout source derivative is owned.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "K2 source status, T_source and finite residual quadrupole amplitudes remain unsigned",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    eh_rows: Sequence[Mapping[str, object]],
    pi_rows: Sequence[Mapping[str, object]],
    owner_rows: Sequence[Mapping[str, object]],
    residual_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 500 PPC4161 - Parent EH Weak-Field Operator Signature Or PiJ2metric Transfer Row

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4484 takes the leap that 4483 set up.

The operator part is no longer foggy. On the existing conditional EH branch:

```text
G_munu[g_obs] + Lambda_eff g_munu
= kappa_eff T_H_munu + E_res_munu.
```

Linearizing around the local exterior and using harmonic gauge gives:

```text
Box hbar_munu = -2 kappa_eff T_H_munu - 2 E_res_munu.
```

In the static exterior region, if Hilbert source, residual support and boundary/readout l=2 leaks are silent:

```text
nabla^2 hbar_munu^ext = 0,
```

so the 4483 public `r^-3` theorem is inherited exactly.

The coupling conclusion is the important bit:

```text
partial_sigma G_munu
= kappa_eff partial_sigma T_H_munu
 + partial_sigma E_res_munu
 + boundary/readout pieces.
```

where `sigma_K2 = K2*C_K2_unit`.

So `K2` has only two honest branches:

```text
source-silent branch: Pi_J2_metric*K2 = 0;
finite-source branch: A_surface_K2 = P_surf,l2 G_EH[kappa_eff deltaT_H_K2 + deltaE_res_K2 + deltaB_l2 + deltaReadout_l2].
```

That means the EH operator can be conditionally right while `Pi_J2_metric=1` is still wrong. The next target is therefore not another Green theorem; it is the K2 source derivative.

No local-GR, J2, PPN, R10, clock, orbital or EM claim is promoted.

## EH Weak-Field Operator Signature

{table(eh_rows)}

## PiJ2metric Transfer Rows

{table(pi_rows)}

## K2 Source Owner Rows

{table(owner_rows)}

## Residual Interface Rows

{table(residual_rows)}

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
    eh_rows: Sequence[Mapping[str, object]],
    pi_rows: Sequence[Mapping[str, object]],
    owner_rows: Sequence[Mapping[str, object]],
    residual_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4484 Y5/R2FR - Parent EH Weak-Field Operator Signature Or PiJ2metric Transfer Row

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

4484 separates two issues that were getting tangled. The conditional EH branch really does give the public weak-field exterior `l=2` operator. But `K2` only produces public J2 if it enters the Hilbert source, residual equation, boundary data or readout. Otherwise its metric response is zero, not one.

## EH Operator

{table(eh_rows)}

## PiJ2 Transfer

{table(pi_rows)}

## K2 Source Ownership

{table(owner_rows)}

## Residual Interface

{table(residual_rows)}

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
    eh_rows: Sequence[Mapping[str, object]],
    pi_rows: Sequence[Mapping[str, object]],
    owner_rows: Sequence[Mapping[str, object]],
    residual_rows: Sequence[Mapping[str, object]],
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
        "VAL4484_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4484_1_EH_operator_linearized",
        any(row.get("row_id") == "EHW4484_1_linearized_operator" for row in eh_rows)
        and any(row.get("row_id") == "EHW4484_2_static_exterior_l2" for row in eh_rows),
        "linearized and static exterior EH operator rows exist",
    )
    add(
        "VAL4484_2_K2_zero_or_source_fork_written",
        any(row.get("row_id") == "EHW4484_4_K2_source_fork" for row in eh_rows)
        and any(row.get("transfer_id") == "PI4484_1_clean_EH_silent_branch" for row in pi_rows)
        and any(row.get("transfer_id") == "PI4484_2_finite_source_functional" for row in pi_rows),
        "K2 zero-or-source fork is written",
    )
    add(
        "VAL4484_3_identity_shortcut_rejected",
        any(row.get("transfer_id") == "PI4484_5_no_identity_shortcut" for row in pi_rows),
        "Pi_J2_metric=1 shortcut is explicitly rejected",
    )
    add(
        "VAL4484_4_owner_derivatives_missing_explicit",
        any(row.get("owner_id") == "KSO4484_5_verdict" and row.get("status") == "ZERO_OR_FINITE_SOURCE_NOT_DECIDED" for row in owner_rows),
        "K2 source owner derivatives remain explicit open rows",
    )
    add(
        "VAL4484_5_residual_interface_written",
        any(row.get("interface_id") == "RIF4484_0_master_equation" for row in residual_rows),
        "residual interface for finite branch is written",
    )
    add(
        "VAL4484_6_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4484_4_K2_zero_or_source_decided" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR/J2 promotion",
    )
    add(
        "VAL4484_7_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, eh_rows, pi_rows, owner_rows, residual_rows, gates, decisions, statuses, next_targets]
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
    add("VAL4484_8_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4484_9_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4484_10_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-326",
    )
    add(
        "VAL4484_11_spine_and_packet_updated",
        MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH),
        "unification spine and private packet integration contain 4484 markers",
    )
    add(
        "VAL4484_12_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4484_13_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    inputs = numeric_inputs()
    sources = source_rows()
    eh_rows = eh_weak_field_rows()
    pi_rows = pij2_transfer_rows(inputs["c_k2_unit"], inputs["two_epsilon"], inputs["half_bound"])
    owner_rows = k2_source_owner_rows()
    residual_rows = residual_interface_rows()
    ledger = decision_ledger_rows()
    gates = claim_gate_rows(sources, eh_rows, pi_rows, owner_rows, residual_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(EH_WEAK_FIELD_CSV, eh_rows)
    write_csv(PIJ2_CSV, pi_rows)
    write_csv(K2_OWNER_CSV, owner_rows)
    write_csv(RESIDUAL_INTERFACE_CSV, residual_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, eh_rows, pi_rows, owner_rows, residual_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, eh_rows, pi_rows, owner_rows, residual_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4484 Parent EH Weak-Field Operator Signature",
        "4484 conditionally derives the parent EH weak-field exterior operator: the selected EH branch linearizes to `Box hbar_munu=-2 kappa_eff T_H_munu-2 E_res_munu`, and source-free exterior support gives the 4483 `r^-3` l=2 profile. The new fork is decisive: `K2` is either source-silent, giving zero public J2 response, or it must enter through a real Hilbert/residual/boundary/readout quadrupole functional. `Pi_J2_metric=1` remains rejected.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4484 Packet Integration",
        "The private packet now treats the EH operator as conditionally derived but separates it from K2 source ownership. The next target is not another operator theorem; it is `partial_sigma(T_H,E_res,B_l2,g_readout_extra)`: prove K2 source silence or compute a finite source-backed `A_surface_K2`.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        EH_WEAK_FIELD_CSV,
        PIJ2_CSV,
        K2_OWNER_CSV,
        RESIDUAL_INTERFACE_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, eh_rows, pi_rows, owner_rows, residual_rows, gates, decisions, statuses, next_targets, csv_paths)
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
