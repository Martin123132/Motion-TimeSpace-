from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_BREF_FIXED_BRANCH_SELECTOR_OR_DELTA_REF_Q_SOURCE_PROVENANCE_PACK_2451"
CHECKPOINT_ID = "2451"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2451-Y5-R2FR-Bref-fixed-branch-selector-or-Delta-ref-q-source-provenance-pack.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2451_SOURCE_REGISTER.csv",
    "selector_attempt": OUT / "P8_Y5_PARENT_QLOC_2451_BREF_FIXED_BRANCH_SELECTOR_ATTEMPT.csv",
    "parent_contract": OUT / "P8_Y5_PARENT_QLOC_2451_PARENT_SELECTOR_CONTRACT.csv",
    "provenance_pack": OUT / "P8_Y5_PARENT_QLOC_2451_DELTA_REF_Q_SOURCE_PROVENANCE_PACK.csv",
    "runner_readiness": OUT / "P8_Y5_PARENT_QLOC_2451_PROVENANCE_RUNNER_READINESS.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2451_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2451_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2451_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2451_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2451_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_selector": QUEUE / "JR2451_BREF_FIXED_BRANCH_SELECTOR_ATTEMPT_NONCLAIM.csv",
    "queue_provenance": QUEUE / "JR2451_DELTA_REF_Q_SOURCE_PROVENANCE_PACK_NONCLAIM.csv",
    "hamiltonian_provenance": HAMILTONIAN / "Delta_ref_q_source_provenance_pack_2451_NONCLAIM.csv",
    "local_provenance": LOCAL_BOUNDS / "Delta_ref_q_source_provenance_pack_2451_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2451_00_2450_doc",
        "source_path": ROOT / "2450-Y5-R2FR-Bref-q-and-source-blindness-theorem-or-Delta-ref-component-row.md",
        "needles": ["NEXT2450_0_selected", "QSB2450_6_verdict", "DQC2450_0_q_component_schema", "VAL2450_OVERALL"],
        "role": "fresh handoff selecting fixed-branch selector or q/source provenance pack",
    },
    {
        "source_id": "SRC2451_01_2450_components",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2450_DELTA_REF_Q_SOURCE_COMPONENT_TEMPLATES.csv",
        "needles": ["DQC2450_0_q_component_schema", "DQC2450_1_source_component_schema", "MISSING_SOURCE_FILE"],
        "role": "current q/source Delta_ref component templates",
    },
    {
        "source_id": "SRC2451_02_999_doc",
        "source_path": ROOT / "999-Y5-R10-Bref-fixed-branch-selector-or-Delta-ref-source-coefficient-provenance.md",
        "needles": ["FBS999_7_verdict", "DCP999_0_partial_source_derivative", "DEC999_2_next_target"],
        "role": "older fixed-branch selector/provenance gate",
    },
    {
        "source_id": "SRC2451_03_999_selector_csv",
        "source_path": OUT / "P8_Y5_R10_999_FIXED_BRANCH_SELECTOR_ATTEMPT.csv",
        "needles": ["FBS999_0_selector_definition", "FBS999_7_verdict", "fail_current_claim"],
        "role": "machine-readable old selector attempt",
    },
    {
        "source_id": "SRC2451_04_999_contract_csv",
        "source_path": OUT / "P8_Y5_R10_999_PARENT_SELECTOR_CONTRACT.csv",
        "needles": ["FBC999_0_selector_function", "FBC999_6_MHref_sidecar", "MISSING_PARENT_SELECTOR"],
        "role": "machine-readable parent selector contract",
    },
    {
        "source_id": "SRC2451_05_999_provenance_csv",
        "source_path": OUT / "P8_Y5_R10_999_DELTA_REF_SOURCE_COEFFICIENT_PROVENANCE.csv",
        "needles": ["DCP999_0_partial_source_derivative", "DCP999_4_component_bound", "MISSING_COMPONENT_INPUTS"],
        "role": "machine-readable source coefficient provenance gate",
    },
    {
        "source_id": "SRC2451_06_999_runner_csv",
        "source_path": OUT / "P8_Y5_R10_999_COEFFICIENT_RUNNER_READINESS.csv",
        "needles": ["DCR999_0_schema_ready", "DCR999_1_values_ready", "false"],
        "role": "machine-readable runner readiness",
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


def selector_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        ("FBS2451_0_selector_definition", "fixed-branch selector Sigma_ref exists before q/source/readout", "Sigma_ref(Phi_parent)->(gamma_ref,tau_ref,C_top,B_ct,S0) and B_ref=B_ref[Sigma_ref]", "q/source B_ref blindness and Delta_ref component theorem-zero", "DEFINITION_LEVEL_ONLY", "parent action/constraint uniquely selecting Sigma_ref", False),
        ("FBS2451_1_parent_variational_owner", "Sigma_ref selected by parent Euler/Ward/topological conditions", "delta S_parent/delta Sigma_ref=0 or C_top/topology/stationarity fixes Sigma_ref", "prevents post-fit reference selection", "NOT_SIGNED", "explicit selector equation and boundary condition from parent action", False),
        ("FBS2451_2_q_independence", "selector is independent of q-source leg and q-sector labels", "D_q Sigma_ref=0; D_q gamma_ref=D_q tau_ref=D_q C_top=D_q B_ct=D_q S0=0", "partial_q Delta_ref=0 by chain rule", "NOT_SIGNED", "no q labels or q-source-current slots in selector inputs", False),
        ("FBS2451_3_source_independence", "selector is independent of matter/source labels and fitted source parameters", "D_source Sigma_ref=0; D_source gamma_ref=D_source tau_ref=D_source C_top=D_source B_ct=D_source S0=0", "partial_source Delta_ref=0 by chain rule", "NOT_SIGNED", "no source/material/GM calibration labels in selector inputs", False),
        ("FBS2451_4_surface_domain_lock", "reference surface/domain fixed independently of q/source choice", "D_q S0=D_source S0=0 and linked surfaces selected by same parent domain rule", "blocks derivative through moving surfaces", "NOT_SIGNED", "q/source-blind linking-surface/domain selector", False),
        ("FBS2451_5_no_GM_calibration", "selector cannot use observed GM, fitted mass, or source-current normalization", "partial_{GM_obs,M_fit,kappa_A,N_E} Sigma_ref=0", "prevents reference subtraction absorbing source mass", "NOT_SIGNED", "source-current equality/Gauss readout downstream of selector", False),
        ("FBS2451_6_counterterm_convention", "counterterm convention fixed before readout", "B_ct=B_ct[Sigma_ref] and D_q B_ct=D_source B_ct=0", "prevents q/source counterterm cancellation", "NOT_SIGNED", "counterterm convention with source path and equation reference", False),
        ("FBS2451_7_same_frame_denominator", "selector and denominator use same tau/coframe/frame", "tau_ref=tau_Q=tau_source and N_E>0 in that same frame", "makes Delta_ref q/source components meaningful", "NOT_SIGNED", "same-frame Hamiltonian/source mass owner", False),
        ("FBS2451_8_verdict", "fixed-branch selector makes B_ref q/source-blind for current MTS", "FBS2451_0 through FBS2451_7 signed => partial_q Delta_ref=partial_source Delta_ref=0", "q/source Delta_ref components theorem-zero", "FAIL_CURRENT_CLAIM", "parent-owned Sigma_ref and same-frame denominator", False),
    ]
    return [
        base_row(selector_id=selector_id, claim=claim, mathematical_form=form, would_close=would_close, current_status=status, missing_signature=missing, accepted_for_claim=accepted)
        for selector_id, claim, form, would_close, status, missing, accepted in rows
    ]


def parent_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("FBC2451_0_selector_function", "a named selector function Sigma_ref", "Sigma_ref: boundary/topology/stationarity data -> gamma_ref,tau_ref,C_top,B_ct,S0", "selector inputs contain no q/source/material/GM/calibration labels", "MISSING_PARENT_SELECTOR"),
        ("FBC2451_1_variation_or_constraint", "variation/constraint equation fixing Sigma_ref", "E_Sigma=0, Ward condition, topological class, or stationarity condition", "equation written in parent variables with source path/equation reference", "MISSING_SELECTOR_EQUATION"),
        ("FBC2451_2_q_source_blind_derivatives", "componentwise q/source derivative-zero certificate", "D_q Sigma_ref=D_source Sigma_ref=0 componentwise", "each component is theorem-zero or source-backed bounded", "MISSING_Q_SOURCE_BLIND_COMPONENT_CERTIFICATE"),
        ("FBC2451_3_no_marker_clause", "no material/source marker clause", "delta Sigma_ref/delta(m_A,theta_A,kappa_A,composition_A)=0", "excludes source-weight/material marker countermodels", "MISSING_NO_MARKER_SELECTOR_CLAUSE"),
        ("FBC2451_4_no_GM_calibration", "no measured-GM/fitted-source calibration in selector", "partial_{GM_obs,M_fit,N_E} Sigma_ref=0 before source-current equality", "no orbital/observed GM appears in B_ref/B_ct provenance", "MISSING_NO_GM_CALIBRATION_CERTIFICATE"),
        ("FBC2451_5_counterterm_provenance", "counterterm convention fixed before readout", "B_ct formula, units, boundary convention, source path, equation reference", "D_q/source B_ct=0 or finite sourced q/source residual", "MISSING_COUNTERTERM_CONVENTION"),
        ("FBC2451_6_N_E_sidecar", "same-frame positive N_E sidecar", "N_E;units;tau_id;frame_id;source_path;equation_ref", "positive Hamiltonian/source denominator; no orbital GM substitution", "MISSING_SAME_FRAME_N_E"),
    ]
    return [
        base_row(contract_id=contract_id, future_parent_action_must_supply=supply, minimum_form=form, acceptance_test=test, current_fill=current_fill)
        for contract_id, supply, form, test, current_fill in rows
    ]


def provenance_pack_rows() -> list[dict[str, Any]]:
    rows = [
        ("DCP2451_0_partial_q_derivative", "partial_q_Delta_ref", "Delta_ref_q_component_over_N_E", "q_parameter;derivative_value;units;source_path;equation_ref;extraction_method;valid_for_claim", "numeric derivative or theorem_zero=true with parent-signed selector", "MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO", False),
        ("DCP2451_1_partial_source_derivative", "partial_source_Delta_ref", "Delta_ref_source_component_over_N_E", "source_parameter;derivative_value;units;source_path;equation_ref;extraction_method;valid_for_claim", "numeric derivative or theorem_zero=true with parent-signed selector", "MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO", False),
        ("DCP2451_2_q_source_scales", "Delta_q_scale;Delta_source_scale", "q/source component products", "definition of q/source variation scale; units; source_path;equation_ref", "source parameters physically defined, not chosen to shrink residual", "MISSING_Q_SOURCE_SCALE", False),
        ("DCP2451_3_Bref_rule", "B_ref_rule", "Delta_ref q/source components", "B_ref formula; boundary convention; counterterm convention; source_path;equation_ref", "formula fixed before q/source/readout and contains no hidden GM/source labels", "MISSING_PARENT_BREF_RULE", False),
        ("DCP2451_4_N_E", "N_E", "Delta_ref q/source components", "positive same-frame Hamiltonian/source normalization; units; tau/frame ids; source_path;equation_ref", "same-frame and not orbital GM imported before source-current proof", "MISSING_SAME_FRAME_N_E", False),
        ("DCP2451_5_component_bound", "Delta_ref_q_source_component_over_N_E", "q/source component bound", "partial_q_Delta_ref;partial_source_Delta_ref;Delta_q_scale;Delta_source_scale;N_E;absolute-value rule;source_path;valid_for_claim", "absolute component sum with no cancellation credit", "MISSING_COMPONENT_INPUTS", False),
    ]
    return [
        base_row(provenance_id=provenance_id, coefficient=coefficient, target_row=target, required_provenance=provenance, acceptance_rule=rule, current_value=value, score_ready=score_ready)
        for provenance_id, coefficient, target, provenance, rule, value, score_ready in rows
    ]


def runner_readiness_rows() -> list[dict[str, Any]]:
    rows = [
        ("DCR2451_0_schema_ready", "Delta_ref q/source finite rows", True, "required fields and absolute-value rule are specified", False),
        ("DCR2451_1_values_ready", "numeric/theorem-zero inputs", False, "partial_q/source Delta_ref, q/source scales, B_ref rule and N_E are missing", False),
        ("DCR2451_2_no_silent_zero", "zero-theorem switch", False, "selector theorem not parent-signed", False),
        ("DCR2451_3_no_downstream_score", "Delta_ref/RCS2446_0/local-GR score", False, "this is q/source provenance only and residual envelope remains open", False),
    ]
    return [
        base_row(runner_id=runner_id, object=object_name, ready=ready, reason=reason, claim_allowed=claim_allowed)
        for runner_id, object_name, ready, reason, claim_allowed in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2451_0_fixed_branch_selector", "B_ref fixed-branch selector is parent-owned", "BLOCKED", "selector equation, no-marker clause, no-GM calibration, counterterm convention and N_E sidecar are missing", False),
        ("CG2451_1_q_source_blind_Bref", "B_ref is q/source-blind", "BLOCKED", "q/source blindness depends on unsigned selector", False),
        ("CG2451_2_q_source_component_score", "Delta_ref q/source components are score-ready", "BLOCKED", "coefficient provenance rows are MISSING and score_ready=false", False),
        ("CG2451_3_downstream", "Delta_ref, RCS2446_0, S_Eq, deltaH, WEP/PPN/local GR pass", "BLOCKED", "2451 only locks selector/provenance requirements", False),
    ]
    return [
        base_row(claim_id=claim_id, claim=claim, gate_status=status, reason=reason, gate_pass=gate_pass)
        for claim_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2451_0_selector_attempt", "DO_NOT_PROMOTE_FIXED_BRANCH_SELECTOR", "current corpus has B_ref scaffold but not parent selector equation/no-marker/GM/counterterm sidecars", "B_ref q/source blindness remains unclaimed"),
        ("DEC2451_1_provenance_gate", "STAGE_Q_SOURCE_COMPONENT_PROVENANCE_REQUIREMENTS", "if selector cannot be signed, q/source components must be bounded from sourced inputs", "future numeric rows cannot score without exact provenance"),
        ("DEC2451_2_next_target", "BUILD_STRICT_PROVENANCE_RUNNER_NEXT", "schema is explicit enough to automatically refuse bad q/source Delta_ref rows", "select 2452"),
        ("DEC2451_3_public", "NO_GITHUB_ACTION", "private nonclaim checkpoint", "continue privately"),
    ]
    return [
        base_row(decision_id=decision_id, decision=decision, rationale=rationale, consequence=consequence)
        for decision_id, decision, rationale, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    row = {
        "route_id": "NEXT2451_0_selected",
        "selection_status": "selected",
        "target_file": "2452-Y5-R2FR-Delta-ref-q-source-strict-provenance-runner.md",
        "target_script": "scripts/Y5_R2FR_Delta_ref_q_source_strict_provenance_runner_2452.py",
        "task": "build a strict runner that refuses Delta_ref q/source component rows unless selector theorem or finite coefficient provenance is complete",
        "acceptance_target": "runner rejects MISSING/unity/orbital-GM/cancellation rows and only allows theorem-zero or fully sourced numeric q/source components",
        "guardrails": "do not invent coefficients; do not allow zero-by-closure; do not claim Delta_ref/RCS2446_0/S_Eq/local GR; do not edit formalization-workbench; do not push GitHub",
    }
    return [base_row(**row)]


def copy_outputs() -> list[dict[str, Any]]:
    copy_specs = {
        "queue_selector": (OUTPUTS["selector_attempt"], COPY_TARGETS["queue_selector"], "B_ref fixed-branch selector attempt queue"),
        "queue_provenance": (OUTPUTS["provenance_pack"], COPY_TARGETS["queue_provenance"], "Delta_ref q/source provenance pack queue"),
        "hamiltonian_provenance": (OUTPUTS["provenance_pack"], COPY_TARGETS["hamiltonian_provenance"], "Hamiltonian Delta_ref q/source provenance pack"),
        "local_provenance": (OUTPUTS["provenance_pack"], COPY_TARGETS["local_provenance"], "local Delta_ref q/source provenance pack"),
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

    add("VAL2451_00_sources_exist", all(row["path_exists"] for row in data["source_register"]), "all cited source paths exist")
    add("VAL2451_01_source_needles", all(row["needles_found"] for row in data["source_register"]), "all cited source needles are present")
    add(
        "VAL2451_02_selector_not_promoted",
        any(row["selector_id"] == "FBS2451_8_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in data["selector_attempt"]),
        "fixed-branch selector theorem is not promoted",
    )
    add(
        "VAL2451_03_contract_missing_marked",
        all("MISSING" in row["current_fill"] and not row["valid_for_claim"] for row in data["parent_contract"]),
        "parent selector contract rows are missing-marked and nonclaim",
    )
    add(
        "VAL2451_04_provenance_missing",
        all("MISSING" in row["current_value"] and not row["score_ready"] for row in data["provenance_pack"]),
        "q/source provenance rows are missing and score_ready=false",
    )
    add(
        "VAL2451_05_runner_readiness_safe",
        any(row["runner_id"] == "DCR2451_0_schema_ready" and row["ready"] for row in data["runner_readiness"]) and all(not row["claim_allowed"] for row in data["runner_readiness"]),
        "schema is ready but claims are refused",
    )
    add(
        "VAL2451_06_claim_gates_blocked",
        all(row["gate_status"] == "BLOCKED" and not row["valid_for_claim"] for row in data["claim_gates"]),
        "all claim gates are blocked",
    )
    add(
        "VAL2451_07_next_target_written",
        len(data["next_target"]) == 1 and data["next_target"][0]["route_id"] == "NEXT2451_0_selected",
        "2452 strict provenance runner target selected",
    )
    add(
        "VAL2451_08_branch_copies",
        all(row["source_exists"] and row["target_exists"] for row in data["branch_copies"]),
        "branch copies exist",
    )
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            name = path.name
            if any(marker in name for marker in ("2451-", "_2451", "2451_", "P8_Y5_PARENT_QLOC_2451", "P8_Y5_BRR545_2451")):
                formalization_hits.append(path)
    add("VAL2451_09_no_formalization_artifacts", len(formalization_hits) == 0, "no 2451 artifacts were written to formalization-workbench", "; ".join(str(path) for path in formalization_hits))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parses(path)
        add(f"VAL2451_CSV_{path.stem}", ok, f"CSV parses with {count} rows", detail)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2451_OVERALL",
        overall,
        "2451 keeps fixed-branch selector nonclaim, stages q/source provenance requirements, and selects strict provenance runner next",
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2451 - Y5/R2FR B_ref Fixed-Branch Selector Or Delta_ref Q/Source Provenance Pack

## Result
- 2451 asks the selector question directly: what parent rule fixes `Sigma_ref` before q/source/readout exists?
- The current corpus has a useful `B_ref` scaffold, but not a parent-owned selector equation.
- Therefore `B_ref` q/source-blindness is still conditional, not a current theorem.
- The q/source provenance gate is now explicit: `partial_q_Delta_ref`, `partial_source_Delta_ref`, q/source scales, `B_ref_rule`, and same-frame `N_E` must be sourced or theorem-zero before scoring.
- Next target is `2452`: a strict provenance runner that rejects bad `Delta_ref` q/source component rows automatically.

## Source Register
{table(["source_id", "source_path", "path_exists", "needles_found", "role"], data["source_register"])}

## B_ref Fixed-Branch Selector Attempt
{table(["selector_id", "claim", "mathematical_form", "would_close", "current_status", "missing_signature", "accepted_for_claim", "valid_for_claim"], data["selector_attempt"])}

## Parent Selector Contract
{table(["contract_id", "future_parent_action_must_supply", "minimum_form", "acceptance_test", "current_fill", "valid_for_claim"], data["parent_contract"])}

## Delta_ref Q/Source Provenance Pack
{table(["provenance_id", "coefficient", "target_row", "required_provenance", "acceptance_rule", "current_value", "score_ready", "valid_for_claim"], data["provenance_pack"])}

## Provenance Runner Readiness
{table(["runner_id", "object", "ready", "reason", "claim_allowed", "valid_for_claim"], data["runner_readiness"])}

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
        "selector_attempt": selector_attempt_rows(),
        "parent_contract": parent_contract_rows(),
        "provenance_pack": provenance_pack_rows(),
        "runner_readiness": runner_readiness_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key in ["source_register", "selector_attempt", "parent_contract", "provenance_pack", "runner_readiness", "claim_gates", "decisions", "next_target"]:
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
