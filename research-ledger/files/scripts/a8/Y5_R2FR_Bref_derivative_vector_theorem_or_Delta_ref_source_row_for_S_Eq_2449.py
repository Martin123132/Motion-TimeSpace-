from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_BREF_DERIVATIVE_VECTOR_OR_DELTA_REF_SOURCE_ROW_FOR_S_EQ_2449"
CHECKPOINT_ID = "2449"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2449-Y5-R2FR-Bref-derivative-vector-theorem-or-Delta-ref-source-row-for-S-Eq.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2449_SOURCE_REGISTER.csv",
    "theorem_attempt": OUT / "P8_Y5_PARENT_QLOC_2449_BREF_DERIVATIVE_VECTOR_THEOREM_ATTEMPT.csv",
    "component_audit": OUT / "P8_Y5_PARENT_QLOC_2449_BREF_DERIVATIVE_COMPONENT_AUDIT.csv",
    "delta_ref_row": OUT / "P8_Y5_PARENT_QLOC_2449_DELTA_REF_SOURCE_ROW_TEMPLATE_FOR_S_EQ.csv",
    "denominator_guard": OUT / "P8_Y5_PARENT_QLOC_2449_N_E_DENOMINATOR_GUARD.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2449_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2449_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2449_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2449_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2449_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_theorem": QUEUE / "JR2449_BREF_DERIVATIVE_VECTOR_THEOREM_ATTEMPT_NONCLAIM.csv",
    "queue_delta_ref": QUEUE / "JR2449_DELTA_REF_SOURCE_ROW_TEMPLATE_NONCLAIM.csv",
    "hamiltonian_delta_ref": HAMILTONIAN / "Delta_ref_source_row_template_for_S_Eq_2449_NONCLAIM.csv",
    "local_delta_ref": LOCAL_BOUNDS / "Delta_ref_source_row_template_for_S_Eq_2449_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2449_00_2448_doc",
        "source_path": ROOT / "2448-Y5-R2FR-relative-boundary-class-and-Bref-owner-or-S-Eq-boundary-source-bound-pack.md",
        "needles": ["NEXT2448_0_selected", "BDV2448_6_verdict", "SBI2448_0_Delta_ref", "VAL2448_OVERALL"],
        "role": "fresh handoff selecting B_ref derivative-vector theorem or Delta_ref row",
    },
    {
        "source_id": "SRC2449_01_2448_bref_csv",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2448_BREF_QBLIND_DERIVATIVE_VECTOR.csv",
        "needles": ["BDV2448_0_q", "BDV2448_6_verdict", "MISSING_PARENT_BREF_RULE"],
        "role": "current B_ref derivative vector status",
    },
    {
        "source_id": "SRC2449_02_997_doc",
        "source_path": ROOT / "997-Y5-R10-Bref-derivative-vector-theorem-or-Delta-ref-source-row.md",
        "needles": ["BDT997_6_verdict", "DVC997_5_vector_norm", "DRS997_0_claim_ready_schema"],
        "role": "older B_ref derivative theorem and Delta_ref row",
    },
    {
        "source_id": "SRC2449_03_997_theorem_csv",
        "source_path": OUT / "P8_Y5_R10_997_BREF_DERIVATIVE_ZERO_THEOREM_ATTEMPT.csv",
        "needles": ["BDT997_0_define_reference_charge", "BDT997_6_verdict", "fail_current_claim"],
        "role": "machine-readable old derivative theorem attempt",
    },
    {
        "source_id": "SRC2449_04_997_component_csv",
        "source_path": OUT / "P8_Y5_R10_997_DERIVATIVE_COMPONENT_AUDIT.csv",
        "needles": ["DVC997_0_source", "DVC997_5_vector_norm", "MISSING_ALL_COMPONENTS_AND_MHREF"],
        "role": "machine-readable derivative component audit",
    },
    {
        "source_id": "SRC2449_05_997_source_row_csv",
        "source_path": OUT / "P8_Y5_R10_997_DELTA_REF_SOURCE_ROW_TEMPLATE.csv",
        "needles": ["DRS997_0_claim_ready_schema", "DRS997_3_no_cancellation_guard", "MISSING_SOURCE_FILE"],
        "role": "machine-readable Delta_ref source row template",
    },
    {
        "source_id": "SRC2449_06_997_denominator_csv",
        "source_path": OUT / "P8_Y5_R10_997_MHREF_DENOMINATOR_GUARD.csv",
        "needles": ["MHG997_0_positive_denominator", "MHG997_2_not_orbital_import", "MISSING_SAME_FRAME_POSITIVE_MHREF"],
        "role": "machine-readable denominator guard",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        found = [needle for needle in needles if needle in text]
        rows.append(base_row(source_id=source["source_id"], source_path=path, path_exists=path.exists(), required_needles="; ".join(needles), found_needles="; ".join(found), needles_found=path.exists() and len(found) == len(needles), role=source["role"]))
    return rows


def theorem_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        ("BDT2449_0_define_reference_charge", "reference charge can be expressed before readout", "H_ref[S,tau]=int_S B_ref[gamma_ref,tau_ref,C_top]; Delta_ref=H_ref[S,tau]-H_ref[S0,tau0]", "B_ref, gamma_ref, tau_ref, C_top and S0 are parent-selected fixed-branch data", "DEFINITION_WRITTEN", "definition exists but unique parent selector is missing", False),
        ("BDT2449_1_chain_rule_zero", "fixed-branch data imply derivative-vector zero", "D_a H_ref=int_S[(delta B_ref/delta gamma_ref)D_a gamma_ref+(delta B_ref/delta tau_ref)D_a tau_ref+(delta B_ref/delta C_top)D_a C_top]+surface_term_a", "D_a gamma_ref=D_a tau_ref=D_a C_top=0 and surface_term_a=0 for a in {q,source,r,t,frame,lambda}", "EXACT_CONDITIONAL_LEMMA", "superselection and surface terms are unsigned", False),
        ("BDT2449_2_q_derivative", "q derivative vanishes if B_ref is not a q-source-current slot", "partial_q Delta_ref=0", "B_ref fixed before q-source variation and no q-dependent reference/readout selector exists", "CONDITIONAL_LEMMA", "this is exactly what is not parent-signed", False),
        ("BDT2449_3_surface_time_frame_range", "surface/time/frame/range derivatives vanish under fixed branch", "partial_r,t,frame,lambda Delta_ref=0", "relative exactness, stationarity, proper-frame covariance, and range independence are parent-owned", "CONDITIONAL_LEMMA", "relative class, tau/coframe and range-independence owners are missing", False),
        ("BDT2449_4_verdict", "B_ref derivative-vector theorem is signed for current MTS", "D_ref Delta_ref=(partial_q,partial_source,partial_r,partial_t,partial_frame,partial_lambda)Delta_ref=0", "BDT2449_0 through BDT2449_3 parent-signed", "FAIL_CURRENT_CLAIM", "valid conditional theorem but not current framework theorem", False),
    ]
    return [
        base_row(step_id=step_id, claim=claim, mathematical_step=math_step, needed_premise=premise, current_status=status, why_not_claim=why, accepted_for_claim=accepted)
        for step_id, claim, math_step, premise, status, why, accepted in rows
    ]


def component_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("DVC2449_0_q", "partial_q Delta_ref", "B_ref contains no q-source variation, q-dependent branch selector, or post-readout calibration constant", "MISSING_PARENT_BREF_RULE", "reference q-current can feed S_Eq", "Delta_ref_q_component_over_N"),
        ("DVC2449_1_source", "partial_source Delta_ref", "B_ref contains no source fields, material labels, fitted source amplitudes, or post-readout calibration constants", "MISSING_PARENT_BREF_RULE", "reference subtraction can absorb source calibration", "Delta_ref_source_component_over_N"),
        ("DVC2449_2_radius", "partial_r Delta_ref", "surface deformation term vanishes by dB_ref=0, fixed corners, or finite radial profile", "MISSING_SURFACE_CLASS_OR_RADIAL_PROFILE", "reference charge changes between linked surfaces", "Delta_ref_radial_profile_over_N"),
        ("DVC2449_3_time", "partial_t Delta_ref", "L_tau B_ref=0 under the same tau used by charge, clocks and readout", "MISSING_STATIONARY_TAU_BREF_RULE", "reference drift can mimic Gdot/clock leakage", "Delta_ref_time_profile_over_N"),
        ("DVC2449_4_frame", "partial_frame Delta_ref", "frame changes are proper gauge for B_ref and do not change physical Hamiltonian reference", "MISSING_COVARIANT_COFRAME_REFERENCE_RULE", "preferred-frame/reference leakage enters PPN and source normalization", "Delta_ref_frame_profile_over_N"),
        ("DVC2449_5_lambda", "partial_lambda Delta_ref", "B_ref is independent of R10 range/memory/domain/sector scale parameters", "MISSING_RANGE_INDEPENDENCE_RULE", "reference subtraction can track R10/local-bound parameters", "Delta_ref_lambda_profile_over_N"),
        ("DVC2449_6_vector_norm", "||D_ref Delta_ref||_1/N_E", "all six derivative components theorem-zero or sourced and bounded; N_E positive same-frame", "MISSING_ALL_COMPONENTS_AND_N_E", "Delta_ref_over_N cannot be stable residual row", "Delta_ref_derivative_vector_norm_over_N"),
    ]
    return [
        base_row(component_id=component_id, component=component, zero_condition=condition, current_value=current_value, failure_if_open=failure, source_row_if_fail=source_row, status="FAIL_CURRENT_CLAIM" if component_id == "DVC2449_6_vector_norm" else "BLOCKED_NONCLAIM")
        for component_id, component, condition, current_value, failure, source_row in rows
    ]


def delta_ref_row_rows() -> list[dict[str, Any]]:
    rows = [
        ("DRS2449_0_claim_ready_schema", "Delta_ref_over_N_E", "abs(Delta_ref)/N_E", "system_id;surface_pair;Delta_ref;Delta_ref_units;N_E;N_E_units;B_ref_rule;derivative_vector;source_path;equation_ref;theorem_zero;valid_for_claim", "numeric finite same-frame ratio or theorem_zero=true; source path exists; no MISSING markers; derivative vector componentwise zero/bounded", "SCHEMA_ONLY", "MISSING_SOURCE_FILE"),
        ("DRS2449_1_current_candidate", "Delta_ref_over_N_E", "abs(H_ref[S,tau]-H_ref[fixed_branch])/N_E", "H_ref_rule;fixed_branch_id;surface_pair;tau_id;N_E;source_path;equation_ref", "B_ref and fixed branch derived before readout, denominator positive and same-frame", "MISSING_BREF_RULE_MISSING_DELTA_REF_VALUE_MISSING_N_E", "MISSING_SOURCE_FILE"),
        ("DRS2449_2_derivative_vector_sidecar", "D_ref_Delta_ref", "(partial_q,partial_source,partial_r,partial_t,partial_frame,partial_lambda)Delta_ref", "component;value;units;zero_theorem;bound;source_path;equation_ref;valid_for_claim", "each derivative component is theorem-zero or source-backed bounded with no MISSING markers", "MISSING_PARENT_BREF_RULE_FOR_ALL_COMPONENTS", "MISSING_SOURCE_FILE"),
        ("DRS2449_3_no_cancellation_guard", "Delta_ref acceptance", "abs(Delta_ref)/N_E and sum_abs derivative sidecar; no sign cancellation credit", "component_abs_values;N_E;source_path;valid_for_claim", "componentwise theorem-zero/source-bound only", "GUARD_ACTIVE_NO_VALUES", "MISSING_SOURCE_FILE"),
    ]
    return [
        base_row(row_id=row_id, target=target, formula=formula, required_columns=columns, acceptance_rule=rule, current_fill=current_fill, source_path=source_path)
        for row_id, target, formula, columns, rule, current_fill, source_path in rows
    ]


def denominator_guard_rows() -> list[dict[str, Any]]:
    rows = [
        ("NEG2449_0_positive_denominator", "N_E>0", "Delta_ref_over_N_E is meaningless or cheat-prone without a positive source normalization", "MISSING_SAME_FRAME_POSITIVE_N_E", False),
        ("NEG2449_1_same_frame", "N_E uses same tau/coframe/source frame as H_ref and Q_tau", "prevents mixing reference subtraction from one frame with source mass from another", "MISSING_TAU_COFRAME_SOURCE_OWNER", False),
        ("NEG2449_2_not_orbital_import", "GM_orbit is not substituted for N_E before source-current equality and Gauss/readout", "prevents circular Newton/local-GR proof", "POLICY_PASS_DENOMINATOR_STILL_MISSING", False),
        ("NEG2449_3_verdict", "N_E denominator is claim-ready", "all denominator guards pass with source paths", "BLOCKED", False),
    ]
    return [
        base_row(guard_id=guard_id, denominator_requirement=requirement, why_needed=why, current_status=status, accepted_for_claim=accepted)
        for guard_id, requirement, why, status, accepted in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2449_0_Bref_derivative_zero", "B_ref derivative vector vanishes", "BLOCKED", "conditional chain-rule proof needs parent-owned B_ref rule and fixed-branch data", False),
        ("CG2449_1_Delta_ref_zero", "Delta_ref_over_N_E=0", "BLOCKED", "Delta_ref value, B_ref rule, derivative vector and N_E are not sourced or theorem-zero", False),
        ("CG2449_2_Delta_ref_bound", "Delta_ref_over_N_E has source-backed bound", "BLOCKED", "source row is template with MISSING_SOURCE_FILE and MISSING values", False),
        ("CG2449_3_RCS2446_0", "RCS2446_0 boundary residual closes", "BLOCKED", "2449 only narrows the first component", False),
        ("CG2449_4_local_GR", "S_Eq/deltaH/WEP/PPN/local GR pass", "BLOCKED", "source-current equality and residual envelope remain open", False),
    ]
    return [
        base_row(claim_id=claim_id, claim=claim, gate_status=status, reason=reason, gate_pass=gate_pass)
        for claim_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2449_0_derivation_attempt", "DO_NOT_PROMOTE_BREF_DERIVATIVE_VECTOR_ZERO", "proof is conditionally valid by chain rule, but its superselection premises are exactly the missing parent B_ref rule", "Delta_ref_over_N_E remains retained"),
        ("DEC2449_1_useful_contract", "KEEP_CHAIN_RULE_THEOREM_AS_PARENT_ACTION_CONTRACT", "it shows precisely how q/source/radius/time/frame/lambda silence would follow if B_ref is fixed branch data", "future work can sign component derivatives one by one"),
        ("DEC2449_2_next_component", "TARGET_Q_AND_SOURCE_DERIVATIVES_FIRST", "partial_q feeds S_Eq directly and partial_source can absorb source calibration", "select 2450"),
        ("DEC2449_3_public", "NO_GITHUB_ACTION", "private nonclaim derivation checkpoint", "continue privately"),
    ]
    return [
        base_row(decision_id=decision_id, decision=decision, rationale=rationale, consequence=consequence)
        for decision_id, decision, rationale, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    row = {
        "route_id": "NEXT2449_0_selected",
        "selection_status": "selected",
        "target_file": "2450-Y5-R2FR-Bref-q-and-source-blindness-theorem-or-Delta-ref-component-row.md",
        "target_script": "scripts/Y5_R2FR_Bref_q_and_source_blindness_theorem_or_Delta_ref_component_row_2450.py",
        "task": "prove B_ref is q-blind and source-blind before readout, or fill q/source derivative components of Delta_ref_over_N_E",
        "acceptance_target": "partial_q Delta_ref and partial_source Delta_ref are theorem-zero under parent-signed B_ref rule, or remain explicit nonclaim component rows with source/value/normalization blockers",
        "guardrails": "do not tune B_ref to source mass; do not import EH/GHY as proof; do not set N_E by convention; do not claim S_Eq/deltaH/WEP/PPN/local GR; do not edit formalization-workbench; do not push GitHub",
    }
    return [base_row(**row)]


def copy_outputs() -> list[dict[str, Any]]:
    copy_specs = {
        "queue_theorem": (OUTPUTS["theorem_attempt"], COPY_TARGETS["queue_theorem"], "B_ref derivative theorem queue"),
        "queue_delta_ref": (OUTPUTS["delta_ref_row"], COPY_TARGETS["queue_delta_ref"], "Delta_ref row template queue"),
        "hamiltonian_delta_ref": (OUTPUTS["delta_ref_row"], COPY_TARGETS["hamiltonian_delta_ref"], "Hamiltonian Delta_ref row template"),
        "local_delta_ref": (OUTPUTS["delta_ref_row"], COPY_TARGETS["local_delta_ref"], "local Delta_ref row template"),
    }
    rows: list[dict[str, Any]] = []
    for copy_id, (source, target, notes) in copy_specs.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=source, target_path=target, source_exists=source.exists(), target_exists=target.exists(), notes=notes))
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, ok: bool, notes: str, detail: str = "") -> None:
        rows.append({"check_id": check_id, "status": "PASS" if ok else "FAIL", "notes": notes, "detail": detail})

    add("VAL2449_00_sources_exist", all(row["path_exists"] for row in data["source_register"]), "all cited source paths exist")
    add("VAL2449_01_source_needles", all(row["needles_found"] for row in data["source_register"]), "all cited source needles are present")
    add(
        "VAL2449_02_theorem_not_promoted",
        any(row["step_id"] == "BDT2449_4_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in data["theorem_attempt"]),
        "B_ref derivative-vector theorem is not promoted",
    )
    add(
        "VAL2449_03_q_source_components_present",
        {"DVC2449_0_q", "DVC2449_1_source", "DVC2449_6_vector_norm"} <= {row["component_id"] for row in data["component_audit"]},
        "q/source derivative components and vector norm are present",
    )
    add(
        "VAL2449_04_delta_ref_rows_fail_closed",
        all(row["source_path"] == "MISSING_SOURCE_FILE" and not row["valid_for_claim"] for row in data["delta_ref_row"]),
        "Delta_ref rows are schema-only and missing source file",
    )
    add(
        "VAL2449_05_denominator_guard_blocked",
        any(row["guard_id"] == "NEG2449_3_verdict" and row["current_status"] == "BLOCKED" for row in data["denominator_guard"]),
        "N_E denominator guard remains blocked",
    )
    add(
        "VAL2449_06_claim_gates_blocked",
        all(row["gate_status"] == "BLOCKED" and not row["valid_for_claim"] for row in data["claim_gates"]),
        "all claim gates are blocked",
    )
    add(
        "VAL2449_07_next_target_written",
        len(data["next_target"]) == 1 and data["next_target"][0]["route_id"] == "NEXT2449_0_selected",
        "2450 q/source blindness target selected",
    )
    add(
        "VAL2449_08_branch_copies",
        all(row["source_exists"] and row["target_exists"] for row in data["branch_copies"]),
        "branch copies exist",
    )
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            name = path.name
            if any(marker in name for marker in ("2449-", "_2449", "2449_", "P8_Y5_PARENT_QLOC_2449", "P8_Y5_BRR545_2449")):
                formalization_hits.append(path)
    add("VAL2449_09_no_formalization_artifacts", len(formalization_hits) == 0, "no 2449 artifacts were written to formalization-workbench", "; ".join(str(path) for path in formalization_hits))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parses(path)
        add(f"VAL2449_CSV_{path.stem}", ok, f"CSV parses with {count} rows", detail)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2449_OVERALL",
        overall,
        "2449 keeps B_ref derivative-vector theorem conditional/nonclaim, stages Delta_ref rows, and selects q/source blindness next",
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2449 - Y5/R2FR B_ref Derivative Vector Theorem Or Delta_ref Source Row For S_Eq

## Result
- 2449 writes the exact conditional theorem: if `B_ref` is fixed-branch data, then the derivative vector vanishes by chain rule.
- The current framework does not parent-sign the fixed-branch selector, so the theorem is not promoted.
- The derivative vector is now explicit in current notation: `partial_q`, `partial_source`, `partial_r`, `partial_t`, `partial_frame`, and `partial_lambda`.
- `Delta_ref_over_N_E` rows are staged, but they remain schema-only with `MISSING_SOURCE_FILE` and `valid_for_claim=false`.
- Next target is `2450`: attack the two nastiest channels first, `partial_q Delta_ref` and `partial_source Delta_ref`.

## Source Register
{table(["source_id", "source_path", "path_exists", "needles_found", "role"], data["source_register"])}

## B_ref Derivative Vector Theorem Attempt
{table(["step_id", "claim", "mathematical_step", "needed_premise", "current_status", "why_not_claim", "accepted_for_claim", "valid_for_claim"], data["theorem_attempt"])}

## B_ref Derivative Component Audit
{table(["component_id", "component", "zero_condition", "current_value", "failure_if_open", "source_row_if_fail", "status", "valid_for_claim"], data["component_audit"])}

## Delta_ref Source Row Template For S_Eq
{table(["row_id", "target", "formula", "required_columns", "acceptance_rule", "current_fill", "source_path", "valid_for_claim"], data["delta_ref_row"])}

## N_E Denominator Guard
{table(["guard_id", "denominator_requirement", "why_needed", "current_status", "accepted_for_claim", "valid_for_claim"], data["denominator_guard"])}

## Claim Gates
{table(["claim_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"], data["claim_gates"])}

## Decision Ledger
{table(["decision_id", "decision", "rationale", "consequence", "valid_for_claim"], data["decisions"])}

## Next Target
{table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], data["next_target"])}

## Branch Copies
{table(["copy_id", "source_path", "target_path", "source_exists", "target_exists", "notes"], data["branch_copies"])}

## Validation
{table(["check_id", "status", "notes", "detail"], data["validation"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "theorem_attempt": theorem_attempt_rows(),
        "component_audit": component_audit_rows(),
        "delta_ref_row": delta_ref_row_rows(),
        "denominator_guard": denominator_guard_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key in ["source_register", "theorem_attempt", "component_audit", "delta_ref_row", "denominator_guard", "claim_gates", "decisions", "next_target"]:
        write_csv(OUTPUTS[key], data[key])

    data["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)


if __name__ == "__main__":
    main()
