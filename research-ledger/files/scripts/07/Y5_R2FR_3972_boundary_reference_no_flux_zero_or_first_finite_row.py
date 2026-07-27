from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3972"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3972-Y5-R2FR-boundary-reference-no-flux-zero-or-first-finite-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3972_SOURCE_REGISTER.csv",
    "zero_attempt": SRC / "P8_Y5_R2FR_3972_BOUNDARY_REFERENCE_ZERO_ATTEMPT.csv",
    "finite_row": SRC / "P8_Y5_R2FR_3972_BOUNDARY_FIRST_FINITE_ROW.csv",
    "feed": SRC / "P8_Y5_R2FR_3972_BOUNDARY_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3972_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3972_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3972_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3972_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3972_VALIDATION.csv",
}

NEXT_DOC = "3973-Y5-R2FR-boundary-vector-tensor-normal-flux-zero-or-coefficient-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3973_boundary_vector_tensor_normal_flux_zero_or_coefficient_row.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3972_00_3971_next", SRC / "P8_Y5_R2FR_3971_NEXT_TARGET.csv", "NEXT3971_0", "3971 handoff"),
        ("SRC3972_01_3971_boundary_input", SRC / "P8_Y5_R2FR_3971_TRIAD_FINITE_INPUT_ROWS.csv", "FIN3971_0_boundary", "boundary finite input"),
        ("SRC3972_02_3971_boundary_zero", SRC / "P8_Y5_R2FR_3971_TRIAD_ZERO_TESTS.csv", "ZT3971_0_boundary_flux", "boundary zero test"),
        ("SRC3972_03_3971_feed", SRC / "P8_Y5_R2FR_3971_EXTRA_MONOPOLE_FEED_UPDATE.csv", "TRF3971_3_next", "boundary priority feed"),
        ("SRC3972_04_boundary_residual", SRC / "P8_Y5_BOUNDARY_REFERENCE_RESIDUAL_ROW.csv", "BRR545_0_boundary_reference_retained", "boundary reference residual"),
        ("SRC3972_05_first_fill_current", SRC / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_FILL_PACK.csv", "BRF543_0_boundary_reference_current", "current first row fill pack"),
        ("SRC3972_06_reference_zero_control", SRC / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_FILL_PACK.csv", "BRF543_1_reference_zero", "reference-only zero control"),
        ("SRC3972_07_first_eval", SRC / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_EVALUATOR.csv", "BRF543_0_boundary_reference_current", "first row evaluator"),
        ("SRC3972_08_zero_theorem_attempt", SRC / "P8_Y5_BOUNDARY_REFERENCE_ZERO_THEOREM_ATTEMPT.csv", "BRT543_4_first_row_theorem_zero", "zero theorem rejection"),
        ("SRC3972_09_reference_shift", SRC / "P8_Y5_BOUNDARY_REFERENCE_OBSTRUCTION_LEDGER.csv", "BRO543_0_reference_shift", "reference shift obstruction"),
        ("SRC3972_10_boundary_improvement", SRC / "P8_Y5_BOUNDARY_REFERENCE_OBSTRUCTION_LEDGER.csv", "BRO543_1_boundary_improvement_flux", "improvement flux obstruction"),
        ("SRC3972_11_vector_tensor", SRC / "P8_Y5_BOUNDARY_REFERENCE_OBSTRUCTION_LEDGER.csv", "BRO543_2_vector_tensor_boundary_hair", "vector/tensor boundary obstruction"),
        ("SRC3972_12_zero_audit", SRC / "P8_Y5_BOUNDARY_REFERENCE_THEOREM_ZERO_AUDIT.csv", "TZA544_0", "zero audit"),
        ("SRC3972_13_parent_owner", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T5_parent_owner_audit", "boundary alpha3 parent ownership"),
        ("SRC3972_14_alpha3_conclusion", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T7_conclusion", "boundary alpha3 conclusion"),
        ("SRC3972_15_cohom_verdict", SRC / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv", "BCT549_6_certificate_verdict", "boundary cohomology verdict"),
        ("SRC3972_16_flux_fill", SRC / "P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv", "FB549_0_boundary_flux_bound", "boundary flux bound row"),
        ("SRC3972_17_flux_eval", SRC / "P8_Y5_BRR545_BOUNDARY_FLUX_EVALUATOR.csv", "FB549_0_boundary_flux_bound", "boundary flux evaluator"),
        ("SRC3972_18_reference_lock_contract", SRC / "P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv", "MAC545_2_reference_lock", "reference lock contract"),
        ("SRC3972_19_cohom_contract", SRC / "P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv", "MAC545_3_boundary_exact_cohomology_zero", "cohomology zero contract"),
        ("SRC3972_20_nohair_contract", SRC / "P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv", "MAC545_4_boundary_no_vector_tensor_hair", "boundary no-hair contract"),
        ("SRC3972_21_reference_ownership", SRC / "P8_Y5_BOUNDARY_REFERENCE_PARENT_OWNERSHIP_AUDIT.csv", "POA545_2_reference", "reference ownership audit"),
        ("SRC3972_22_boundary_ownership", SRC / "P8_Y5_BOUNDARY_REFERENCE_PARENT_OWNERSHIP_AUDIT.csv", "POA545_3_boundary", "boundary ownership audit"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": exists,
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def zero_attempt_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "BRZ3972_0_target",
            "claim_piece": "boundary reference/no-flux zero target",
            "mathematical_form": "B_zero_flux=0 and Delta_symp=0 with M_H_ref fixed in the same observed frame",
            "why_needed": "this is the first scalar boundary contribution to epsilon_boundary and the hidden exterior monopole budget",
            "current_result": "TARGET_DEFINED",
            "blocks_if_unsigned": "epsilon_boundary_reference_abs remains nonzero or unknown",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BRZ3972_1_reference_lock_route",
            "claim_piece": "reference subtraction silence",
            "mathematical_form": "partial_t Delta_ref=partial_r Delta_ref=partial_source Delta_ref=partial_frame Delta_ref=0 => Delta_symp=0",
            "why_needed": "a movable Hamiltonian reference can masquerade as mass normalization, radial drift, Gdot, xi, or beta leakage",
            "current_result": "CONDITIONAL_ROUTE_NOT_PARENT_OWNED",
            "blocks_if_unsigned": "Delta_symp must stay as a finite input term",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BRZ3972_2_exact_flux_route",
            "claim_piece": "exact/improvement flux silence",
            "mathematical_form": "B_imp=dC and int_S2 B_imp-int_S1 B_imp=int_A dB_imp=0 => B_zero_flux=0",
            "why_needed": "calling a term exact is not enough if the relative class or reference can carry a finite linked-surface charge",
            "current_result": "CONDITIONAL_ROUTE_NOT_PARENT_OWNED",
            "blocks_if_unsigned": "B_zero_flux must stay as a finite input term",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BRZ3972_3_nohair_caveat",
            "claim_piece": "scalar boundary zero is not full local-GR boundary zero",
            "mathematical_form": "B_zero_flux=Delta_symp=0 does not imply boundary_flux_vector=0, T_B^TF=0, n_mu P_loc_nu K_B^{mu nu}=0, or derivative silence",
            "why_needed": "the scalar/reference row can close only one boundary component; vector/tensor/normal exchange can still hit alpha_i, xi, beta, and Gdot",
            "current_result": "CAVEAT_ACTIVE",
            "blocks_if_unsigned": "boundary vector/tensor/normal rows remain in the local-GR residual vector",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BRZ3972_4_current_verdict",
            "claim_piece": "current MTS boundary reference zero",
            "mathematical_form": "current corpus supplies reference/template zero rows but no parent-owned B_zero_flux=Delta_symp=0 theorem for the current branch",
            "why_needed": "prevents converting the reference-only zero control into an MTS local-GR claim",
            "current_result": "ZERO_CLAIM_REJECTED_FOR_NOW",
            "blocks_if_unsigned": "use finite nonclaim row epsilon_boundary_reference_abs instead",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def finite_row_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "input_id": "BFR3972_0_epsilon_boundary_reference_abs",
            "symbol": "epsilon_boundary_reference_abs",
            "units": "dimensionless",
            "formula": "(|B_zero_flux|+|Delta_symp|)/M_H_ref",
            "numerator_terms": "B_zero_flux;Delta_symp",
            "denominator": "M_H_ref",
            "required_inputs": "B_zero_flux_value;Delta_symp_value;M_H_ref;same_frame_normalization;source_path;units;sign/no_cancellation",
            "source_status": "source-backed symbolic row only; numeric numerator and denominator values missing",
            "current_status": "FINITE_INPUT_ROW_READY_VALUES_MISSING",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "BFR3972_1_B_zero_flux",
            "symbol": "B_zero_flux",
            "units": "mass_or_GM_charge_units_matching_M_H_ref",
            "formula": "linked-surface exact/improvement flux or theorem-zero",
            "numerator_terms": "int_S2 B_imp-int_S1 B_imp",
            "denominator": "none",
            "required_inputs": "parent boundary form;relative cohomology class;surface pair;falloff;normalization;source_path",
            "source_status": "missing parent-owned theorem or numeric/source row",
            "current_status": "VALUE_MISSING",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "BFR3972_2_Delta_symp",
            "symbol": "Delta_symp",
            "units": "mass_or_GM_charge_units_matching_M_H_ref",
            "formula": "reference/symplectic subtraction drift between linked surfaces",
            "numerator_terms": "Delta_ref(S2)-Delta_ref(S1)",
            "denominator": "none",
            "required_inputs": "fixed reference prescription;charge variation ledger;surface pair;frame/source independence;source_path",
            "source_status": "missing parent-owned theorem or numeric/source row",
            "current_status": "VALUE_MISSING",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "BFR3972_3_M_H_ref",
            "symbol": "M_H_ref",
            "units": "same_mass_or_GM_charge_units",
            "formula": "same-frame Hilbert/source mass denominator for the boundary comparison",
            "numerator_terms": "none",
            "denominator": "M_H_ref",
            "required_inputs": "same-frame measured or parent-calibrated denominator;positive value;source_path",
            "source_status": "missing same-frame denominator value",
            "current_status": "VALUE_MISSING",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "BFR3972_4_boundary_lower_block",
            "symbol": "epsilon_boundary",
            "units": "dimensionless",
            "formula": "epsilon_boundary >= epsilon_boundary_reference_abs",
            "numerator_terms": "epsilon_boundary_reference_abs;boundary_flux_vector;boundary_derivative_terms",
            "denominator": "dimensionless budget",
            "required_inputs": "BFR3972_0 plus vector/tensor/normal boundary rows",
            "source_status": "first scalar/reference row ready; vector/tensor/normal pieces not yet closed",
            "current_status": "LOWER_BLOCK_READY_NONCLAIM",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "BRF3972_0_boundary",
            "target": "epsilon_boundary",
            "update_formula": "epsilon_boundary = epsilon_boundary_reference_abs + epsilon_boundary_vector_tensor_normal_abs + epsilon_boundary_derivative_abs + ...",
            "meaning": "the boundary channel now has a first explicit scalar/reference subrow instead of a bare missing symbol",
            "status": "BOUNDARY_SUBROW_FEED_READY_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BRF3972_1_extra_monopole",
            "target": "epsilon_mu_extra_total",
            "update_formula": "epsilon_mu_extra_total <= epsilon_boundary_reference_abs + epsilon_boundary_vector_tensor_normal_abs + |Delta_PiM| + |epsilon_domain_projector| + remaining_channels_abs",
            "meaning": "the scalar/reference boundary row now enters the hidden exterior monopole budget explicitly",
            "status": "EXTRA_MONOPOLE_FEED_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BRF3972_2_single_mass",
            "target": "Delta_B_single_mass",
            "update_formula": "|Delta_B_single_mass|/A_source^2 <= C_mu (epsilon_boundary_reference_abs + epsilon_boundary_vector_tensor_normal_abs + |Delta_PiM| + |epsilon_domain_projector| + remaining_channels_abs)",
            "meaning": "this is the route from boundary reference leakage to beta/source-square-law failure",
            "status": "BETA_FEED_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BRF3972_3_local_PPN",
            "target": "Delta_PPN_source_abs",
            "update_formula": "boundary reference leakage feeds beta/source normalization; vector/tensor/normal boundary leakage still feeds alpha_i, xi, and Gdot",
            "meaning": "closing the scalar/reference row alone is not enough for local GR",
            "status": "PPN_CAVEAT_EXPLICIT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BRF3972_4_next",
            "target": "boundary_vector_tensor_normal",
            "update_formula": "attempt boundary_flux_vector=T_B^TF=n_mu P_loc_nu K_B^{mu nu}=0 or create coefficient rows W_boundary_alpha3,W_boundary_xi,boundary_normal_exchange",
            "meaning": "after the scalar/reference row, the next real boundary obstacle is vector/tensor/normal leakage",
            "status": "NEXT_GATE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D3972_0_zero_attempt",
            "status": "BOUNDARY_REFERENCE_ZERO_ATTEMPT_REJECTED_FOR_NOW",
            "meaning": "B_zero_flux=Delta_symp=0 has conditional routes but is not parent-owned by the current corpus",
            "claim_status": "blocks_boundary_zero_claim",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3972_1_first_finite_row",
            "status": "FIRST_BOUNDARY_FINITE_ROW_CREATED",
            "meaning": "epsilon_boundary_reference_abs=(|B_zero_flux|+|Delta_symp|)/M_H_ref is now the scalar/reference boundary score row",
            "claim_status": "symbolic_nonclaim_values_missing",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3972_2_next_boundary_hair",
            "status": "BOUNDARY_VECTOR_TENSOR_NORMAL_NEXT",
            "meaning": "reference/no-flux is only the scalar/reference subchannel; vector/tensor/normal boundary leakage remains the sharper local-GR obstacle",
            "claim_status": "private_derivation_continues",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3972_0_sources",
            "gate": "source register",
            "requirement": "all cited source paths and needles found",
            "status": "PASS_PRIVATE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3972_1_zero",
            "gate": "boundary reference zero promotion",
            "requirement": "B_zero_flux=0 and Delta_symp=0 parent-signed for the current branch",
            "status": "BLOCKED_ZERO_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3972_2_finite_row",
            "gate": "finite scalar/reference boundary score",
            "requirement": "numeric/source-backed B_zero_flux, Delta_symp, positive M_H_ref, units, and no-cancellation normalization",
            "status": "ROW_READY_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3972_3_local_GR",
            "gate": "local-GR boundary clearance",
            "requirement": "scalar/reference plus vector/tensor/normal and derivative boundary channels closed or bounded below locks",
            "status": "BLOCKED_BOUNDARY_VECTOR_TENSOR_NORMAL_REMAINS",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3972_4_next",
            "gate": "next target",
            "requirement": "boundary vector/tensor/normal flux zero proof or coefficient rows",
            "status": "NEXT_TARGET_REQUIRED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3972_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "attempt boundary vector/tensor/normal no-hair zero; if it fails, create coefficient rows for W_boundary_alpha3, W_boundary_xi, boundary_normal_exchange, and derivative-silence terms",
            "success_condition": "boundary vector/tensor/normal leakage is theorem-zero, or it becomes a finite nonclaim vector feeding alpha_i, xi, beta, Gdot, and epsilon_mu_extra_total",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "BOUNDARY_REFERENCE_FIRST_FINITE_ROW_READY_ZERO_NOT_CLAIMED",
            "sources_found": found,
            "sources_total": len(sources),
            "main_result": "boundary reference/no-flux zero was attempted and rejected for now; epsilon_boundary_reference_abs is now a score-ready finite nonclaim row feeding local-GR source stability",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return f"""# 3972 - Boundary Reference No-Flux Zero Or First Finite Row

Timestamp: `{timestamp}`

## Result

3972 tried the clean route first:

```text
B_zero_flux = 0
Delta_symp = 0
```

That would close the scalar/reference boundary contribution:

```text
epsilon_boundary_reference_abs = (|B_zero_flux| + |Delta_symp|)/M_H_ref = 0
```

The current corpus does not parent-sign that zero. The reference lock and exact/improvement no-flux arguments remain conditional, so this checkpoint promotes the finite nonclaim row instead:

```text
epsilon_boundary_reference_abs = (|B_zero_flux| + |Delta_symp|)/M_H_ref
```

## Why This Moves The Framework

This is not another vague missing-item ledger. It turns one concrete boundary obstruction into a scoreable object with numerator terms, denominator, units, source requirements, and local-GR feed-through:

```text
epsilon_mu_extra_total <= epsilon_boundary_reference_abs
                        + epsilon_boundary_vector_tensor_normal_abs
                        + |Delta_PiM|
                        + |epsilon_domain_projector|
                        + remaining_channels_abs
```

## Decision

No local-GR claim is made. The scalar/reference boundary row is now ready to be filled or theorem-zeroed later.

Next target:

```text
{NEXT_DOC}
```

That step should attack the remaining boundary hair: vector, trace-free tensor, normal exchange, and derivative-silence terms.

Source needles found: `{found}/{len(sources)}`.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3972 - Boundary Reference No-Flux First Row

- Timestamp: `{timestamp}`
- Status: `BOUNDARY_REFERENCE_FIRST_FINITE_ROW_READY_ZERO_NOT_CLAIMED`
- Zero attempt:
  `B_zero_flux=Delta_symp=0` remains conditional, not parent-owned.
- Finite scalar/reference row:
  `epsilon_boundary_reference_abs=(|B_zero_flux|+|Delta_symp|)/M_H_ref`.
- Feed:
  `epsilon_mu_extra_total <= epsilon_boundary_reference_abs + epsilon_boundary_vector_tensor_normal_abs + |Delta_PiM| + |epsilon_domain_projector| + remaining_channels_abs`.
- Claim status: nonclaim. Values/source rows are missing and boundary vector/tensor/normal hair still remains.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3972 - Boundary Reference No-Flux First Row"
    block = spine_block(timestamp)
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def all_rows(timestamp: str) -> dict[str, list[dict[str, Any]]]:
    sources = source_register_rows(timestamp)
    return {
        "sources": sources,
        "zero_attempt": zero_attempt_rows(timestamp),
        "finite_row": finite_row_rows(timestamp),
        "feed": feed_rows(timestamp),
        "decision": decision_rows(timestamp),
        "claim_gate": claim_gate_rows(timestamp),
        "next": next_rows(timestamp),
        "status": status_rows(timestamp, sources),
    }


def validation_rows(timestamp: str, rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = rows["sources"]
    zero_attempt = rows["zero_attempt"]
    finite = rows["finite_row"]
    feed = rows["feed"]
    decisions = rows["decision"]
    claims = rows["claim_gate"]
    next_target = rows["next"]

    def val(validation_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }

    parsed = True
    parse_detail = "generated CSV files parse cleanly"
    for path in generated_csvs:
        try:
            read_csv(path)
        except Exception as exc:
            parsed = False
            parse_detail = f"{path} failed to parse: {exc}"
            break

    finite_symbols = {row["symbol"] for row in finite}
    feed_targets = {row["target"] for row in feed}

    return [
        val("VAL3972_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3972_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3972_02_zero_attempt", any(row["row_id"] == "BRZ3972_4_current_verdict" and row["current_result"] == "ZERO_CLAIM_REJECTED_FOR_NOW" for row in zero_attempt), "zero attempt includes explicit rejection verdict"),
        val("VAL3972_03_formula", any(row["symbol"] == "epsilon_boundary_reference_abs" and row["formula"] == "(|B_zero_flux|+|Delta_symp|)/M_H_ref" for row in finite), "finite scalar/reference formula is exact"),
        val("VAL3972_04_components", {"epsilon_boundary_reference_abs", "B_zero_flux", "Delta_symp", "M_H_ref", "epsilon_boundary"} <= finite_symbols, "finite row includes numerator, denominator, and boundary feed components"),
        val("VAL3972_05_score_ready", all(row["score_ready"] for row in finite), "all finite rows are score-ready symbolic forms"),
        val("VAL3972_06_feed", {"epsilon_boundary", "epsilon_mu_extra_total", "Delta_B_single_mass", "Delta_PPN_source_abs", "boundary_vector_tensor_normal"} <= feed_targets, "boundary feed reaches extra monopole, beta, and PPN vector"),
        val("VAL3972_07_decision", any(row["status"] == "FIRST_BOUNDARY_FINITE_ROW_CREATED" for row in decisions), "decision creates first boundary finite row"),
        val("VAL3972_08_claim_gate_zero", any(row["status"] == "BLOCKED_ZERO_NOT_PARENT_SIGNED" for row in claims), "claim gate blocks zero promotion"),
        val("VAL3972_09_claim_gate_local", any(row["status"] == "BLOCKED_BOUNDARY_VECTOR_TENSOR_NORMAL_REMAINS" for row in claims), "claim gate keeps local GR blocked by remaining boundary hair"),
        val("VAL3972_10_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to boundary vector/tensor/normal flux"),
        val("VAL3972_11_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3972_12_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3972_13_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3972_14_spine_updated", SPINE_PATH.exists() and "3972 - Boundary Reference No-Flux First Row" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3972_15_csv_parse", parsed, parse_detail),
        val("VAL3972_16_script_compile", True, "script compiled before validation write"),
        val("VAL3972_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["zero_attempt"], rows["zero_attempt"])
    write_csv(OUTPUTS["finite_row"], rows["finite_row"])
    write_csv(OUTPUTS["feed"], rows["feed"])
    write_csv(OUTPUTS["decision"], rows["decision"])
    write_csv(OUTPUTS["claim_gate"], rows["claim_gate"])
    write_csv(OUTPUTS["next"], rows["next"])
    write_csv(OUTPUTS["status"], rows["status"])

    DOC_PATH.write_text(doc_text(timestamp, rows["sources"]), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3972 validation failed: {failed}")

    print(f"3972 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Boundary reference zero attempt rejected; first finite nonclaim row assembled")


if __name__ == "__main__":
    run()
