from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_BREF_Q_AND_SOURCE_BLINDNESS_OR_DELTA_REF_COMPONENT_ROW_2450"
CHECKPOINT_ID = "2450"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2450-Y5-R2FR-Bref-q-and-source-blindness-theorem-or-Delta-ref-component-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2450_SOURCE_REGISTER.csv",
    "blindness_attempt": OUT / "P8_Y5_PARENT_QLOC_2450_BREF_Q_SOURCE_BLINDNESS_THEOREM_ATTEMPT.csv",
    "leakage_audit": OUT / "P8_Y5_PARENT_QLOC_2450_Q_SOURCE_LEAKAGE_CHANNEL_AUDIT.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2450_BREF_Q_SOURCE_COUNTERMODEL_LEDGER.csv",
    "component_rows": OUT / "P8_Y5_PARENT_QLOC_2450_DELTA_REF_Q_SOURCE_COMPONENT_TEMPLATES.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2450_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2450_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2450_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2450_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2450_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_blindness": QUEUE / "JR2450_BREF_Q_SOURCE_BLINDNESS_NONCLAIM.csv",
    "queue_components": QUEUE / "JR2450_DELTA_REF_Q_SOURCE_COMPONENT_TEMPLATES_NONCLAIM.csv",
    "hamiltonian_components": HAMILTONIAN / "Delta_ref_q_source_components_2450_NONCLAIM.csv",
    "local_components": LOCAL_BOUNDS / "Delta_ref_q_source_components_2450_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2450_00_2449_doc",
        "source_path": ROOT / "2449-Y5-R2FR-Bref-derivative-vector-theorem-or-Delta-ref-source-row-for-S-Eq.md",
        "needles": ["NEXT2449_0_selected", "DVC2449_0_q", "DVC2449_1_source", "VAL2449_OVERALL"],
        "role": "fresh handoff selecting q/source B_ref blindness",
    },
    {
        "source_id": "SRC2450_01_2449_components",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2449_BREF_DERIVATIVE_COMPONENT_AUDIT.csv",
        "needles": ["DVC2449_0_q", "DVC2449_1_source", "MISSING_PARENT_BREF_RULE"],
        "role": "current q/source derivative component blockers",
    },
    {
        "source_id": "SRC2450_02_998_doc",
        "source_path": ROOT / "998-Y5-R10-Bref-source-blindness-theorem-or-Delta-ref-source-component-row.md",
        "needles": ["SBT998_6_verdict", "SLC998_5_source_current_weight", "DSC998_0_component_schema"],
        "role": "older source-blindness theorem attempt",
    },
    {
        "source_id": "SRC2450_03_998_theorem_csv",
        "source_path": OUT / "P8_Y5_R10_998_BREF_SOURCE_BLIND_THEOREM_ATTEMPT.csv",
        "needles": ["SBT998_0_target", "SBT998_6_verdict", "fail_current_claim"],
        "role": "machine-readable source-blindness attempt",
    },
    {
        "source_id": "SRC2450_04_998_leakage_csv",
        "source_path": OUT / "P8_Y5_R10_998_SOURCE_LEAKAGE_CHANNEL_AUDIT.csv",
        "needles": ["SLC998_0_explicit_source_fields", "SLC998_5_source_current_weight", "not_parent_excluded"],
        "role": "machine-readable source leakage channels",
    },
    {
        "source_id": "SRC2450_05_998_countermodels",
        "source_path": OUT / "P8_Y5_R10_998_COUNTERMODEL_LEDGER.csv",
        "needles": ["CM998_0_source_weighted_reference", "CM998_2_material_marker_counterterm", "blocks_theorem"],
        "role": "source-dependent reference countermodels",
    },
    {
        "source_id": "SRC2450_06_2449_delta_ref",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2449_DELTA_REF_SOURCE_ROW_TEMPLATE_FOR_S_EQ.csv",
        "needles": ["DRS2449_0_claim_ready_schema", "DRS2449_2_derivative_vector_sidecar", "MISSING_SOURCE_FILE"],
        "role": "current Delta_ref row template",
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


def blindness_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        ("QSB2450_0_target", "B_ref is q-blind and source-blind before readout", "partial_q B_ref=partial_source B_ref=0", "TARGET_DEFINED", "partial_q/source Delta_ref zero", "target definition is not a parent proof", False),
        ("QSB2450_1_argument_absence", "candidate notation has no explicit q/source argument", "B_ref=B_ref[gamma_ref,tau_ref,C_top]+B_ct[fixed_branch]", "USEFUL_BUT_INSUFFICIENT", "exclude explicit q/source fields", "absence of symbols in ansatz does not prove fixed branch is q/source independent", False),
        ("QSB2450_2_fixed_branch_selector", "fixed branch data selected without q/source labels or fitted calibration", "D_q gamma_ref=D_source gamma_ref=D_q C_top=D_source C_top=D_q B_ct=D_source B_ct=0", "NOT_SIGNED", "chain-rule zero of partial_q/source H_ref", "parent-selected reference branch is missing", False),
        ("QSB2450_3_no_q_source_slot", "B_ref contains no q-source-current or motion-field branch selector", "delta B_ref/delta q=delta B_ref/delta X_q=0", "NOT_SIGNED", "prevent B_ref from feeding S_Eq directly", "q is not proven absent from reference/counterterm/readout slots", False),
        ("QSB2450_4_no_material_marker", "B_ref contains no matter/material/species/source marker", "delta B_ref/delta m_A=delta B_ref/delta theta_A=delta B_ref/delta kappa_A=0", "NOT_SIGNED", "prevent source-composition leakage", "source weights/material markers remain legal unless parent-forbidden", False),
        ("QSB2450_5_no_measured_GM_calibration", "B_ref cannot depend on observed GM/source amplitude/post-fit calibration", "partial_{GM_obs,M_source,calibration} B_ref=0", "NOT_SIGNED", "prevent reference from absorbing source mass normalization", "same-frame source-current equality remains missing", False),
        ("QSB2450_6_verdict", "partial_q Delta_ref=partial_source Delta_ref=0 closes as current MTS theorem", "partial_q/source int_S B_ref - partial_q/source int_S0 B_ref=0", "FAIL_CURRENT_CLAIM", "Delta_ref q/source components theorem-zero", "fixed branch, no-q-source, no-marker, no-GM-calibration and counterterm rules are unsigned", False),
    ]
    return [
        base_row(step_id=step_id, statement=statement, mathematical_form=form, proof_status=status, needed_for=needed_for, blocker=blocker, accepted_for_claim=accepted)
        for step_id, statement, form, status, needed_for, blocker, accepted in rows
    ]


def leakage_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("QSL2450_0_explicit_q_slot", "B_ref directly depends on q or q-sector field", "B_ref[...,q,X_q,Phi_q]", "NOT_PARENT_EXCLUDED", "lets reference term feed S_Eq directly", "parent B_ref argument list proving delta B_ref/delta q=0"),
        ("QSL2450_1_explicit_source_fields", "B_ref directly depends on matter/source fields", "B_ref[...,psi_A,T_A,J_source]", "NOT_PARENT_EXCLUDED", "lets reference subtraction track source distribution", "parent B_ref argument list proving delta B_ref/delta psi_A=0"),
        ("QSL2450_2_material_species_labels", "B_ref depends on material/species labels", "B_ref[...,m_A,theta_A,kappa_A,composition_A]", "NOT_PARENT_EXCLUDED", "turns WEP/source-normalization markers into reference drift", "no-marker/source-universality clause signed by parent action"),
        ("QSL2450_3_measured_GM_or_mass_fit", "B_ref depends on observed GM or fitted source mass", "B_ref[...,GM_obs,M_fit,M_H_ref]", "NOT_PARENT_EXCLUDED", "reference can absorb mass normalization to be derived", "source-current equality and Gauss/readout theorem before GM input"),
        ("QSL2450_4_q_or_source_dependent_surface", "reference surface/fixed branch moves with q/source choice", "S0=S0[q,source] or gamma_ref=gamma_ref[q,source]", "NOT_PARENT_EXCLUDED", "derivative re-enters through domain rather than integrand", "fixed branch selector and linking-surface rule independent of q/source labels"),
        ("QSL2450_5_counterterm_calibration", "counterterm normalization chosen after q/source/readout", "B_ct=B_ct[q,source,fit,calibration]", "NOT_PARENT_EXCLUDED", "can fake zero by subtraction", "counterterm convention fixed in parent action with source/equation reference"),
        ("QSL2450_6_source_current_weight", "species-weighted source current countermodel", "J_source=sum_A kappa_A(source)T_A with B_ref or N_E tracking kappa_A", "COUNTERMODEL_RETAINED", "metric/descent language alone does not exclude source weights", "parent source-current Ward/no-marker theorem"),
    ]
    return [
        base_row(channel_id=channel_id, leakage_channel=channel, forbidden_form=form, current_status=status, why_dangerous=danger, required_exit=exit_needed)
        for channel_id, channel, form, status, danger, exit_needed in rows
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        ("CM2450_0_q_reference", "B_ref=B_ref0+epsilon f(q) omega_S", "formal boundary covariance and fixed-looking expression", "q-blindness and S_Eq silence", "no parent rule forbids q labels in B_ref/counterterms", "partial_q Delta_ref theorem-zero"),
        ("CM2450_1_source_weighted_reference", "B_ref=B_ref0+epsilon f(source_label) omega_S", "formal boundary covariance and fixed-looking reference expression", "source-blindness and partial_source Delta_ref=0", "no parent rule forbids source labels in B_ref/counterterms", "partial_source Delta_ref theorem-zero"),
        ("CM2450_2_GM_calibrated_reference", "H_ref[S]=H_ref0[S]+epsilon GM_obs(source)", "same symbolic H_ref form if GM_obs hidden as calibration data", "source-mass derivation", "N_E/source-current equality and no-orbital-import guard are not theorem-owned", "Delta_ref_over_N_E zero or bound"),
        ("CM2450_3_material_marker_counterterm", "B_ct=B_ct0+epsilon theta_A b_ct on material-labelled branch", "local covariance if theta_A treated as branch data", "no material/source marker rule", "source-weight/material marker countermodels remain retained", "source-blind B_ref"),
    ]
    return [
        base_row(countermodel_id=countermodel_id, construction=construction, preserves=preserves, violates=violates, why_allowed_now=allowed, blocks_theorem=blocks)
        for countermodel_id, construction, preserves, violates, allowed, blocks in rows
    ]


def component_row_rows() -> list[dict[str, Any]]:
    rows = [
        ("DQC2450_0_q_component_schema", "Delta_ref_q_component_over_N_E", "abs(partial_q Delta_ref * Delta_q_scale)/N_E", "system_id;q_parameter;Delta_q_scale;partial_q_Delta_ref;Delta_ref_units;N_E;N_E_units;B_ref_rule;fixed_branch_id;source_path;equation_ref;valid_for_claim", "numeric finite same-frame ratio or theorem_zero=true; source path exists; no MISSING markers", "SCHEMA_ONLY_MISSING_VALUES", "MISSING_SOURCE_FILE"),
        ("DQC2450_1_source_component_schema", "Delta_ref_source_component_over_N_E", "abs(partial_source Delta_ref * Delta_source_scale)/N_E", "system_id;source_parameter;Delta_source_scale;partial_source_Delta_ref;Delta_ref_units;N_E;N_E_units;B_ref_rule;fixed_branch_id;source_path;equation_ref;valid_for_claim", "numeric finite same-frame ratio or theorem_zero=true; source path exists; no MISSING markers", "SCHEMA_ONLY_MISSING_VALUES", "MISSING_SOURCE_FILE"),
        ("DQC2450_2_theorem_zero_switch", "partial_q/source Delta_ref", "partial_q Delta_ref=partial_source Delta_ref=0", "B_ref_q_source_blind_theorem;fixed_branch_selector;no_q_source_slot;no_marker_clause;no_GM_calibration;counterterm_rule;source_path;equation_ref;valid_for_claim", "all blindness theorem clauses parent-signed true", "MISSING_PARENT_BREF_Q_SOURCE_BLIND_THEOREM", "MISSING_SOURCE_FILE"),
        ("DQC2450_3_finite_bound_row", "q/source finite derivative bound", "abs(partial_q Delta_ref)+abs(partial_source Delta_ref)<=bound", "derivative_value;bound;units;q_parameter;source_parameter;source_path;equation_ref;extraction_method;valid_for_claim", "sourced derivative or bounded finite-difference profile with units", "MISSING_NUMERIC_DERIVATIVE_AND_BOUND", "MISSING_SOURCE_FILE"),
        ("DQC2450_4_denominator_sidecar", "N_E for q/source components", "N_E>0 in same frame as Delta_ref", "N_E;units;tau_id;frame_id;source_path;equation_ref;valid_for_claim", "same-frame positive Hamiltonian/source denominator; no orbital GM substitution", "MISSING_SAME_FRAME_N_E", "MISSING_SOURCE_FILE"),
    ]
    return [
        base_row(row_id=row_id, target=target, formula=formula, required_columns=columns, acceptance_rule=rule, current_fill=current_fill, source_path=source_path)
        for row_id, target, formula, columns, rule, current_fill, source_path in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2450_0_Bref_q_blind", "B_ref is q-blind", "BLOCKED", "fixed-branch selector and no-q-source slot are unsigned", False),
        ("CG2450_1_Bref_source_blind", "B_ref is source-blind", "BLOCKED", "no-marker/no-GM-calibration/counterterm rules are unsigned", False),
        ("CG2450_2_partial_q_source_zero", "partial_q/source Delta_ref=0", "BLOCKED", "blindness theorem is conditional only", False),
        ("CG2450_3_component_bound", "q/source Delta_ref components have source-backed bounds", "BLOCKED", "component rows are schema-only with MISSING values/source path/N_E", False),
        ("CG2450_4_downstream", "Delta_ref, RCS2446_0, S_Eq, deltaH, WEP/PPN/local GR pass", "BLOCKED", "2450 covers two derivative components only", False),
    ]
    return [
        base_row(claim_id=claim_id, claim=claim, gate_status=status, reason=reason, gate_pass=gate_pass)
        for claim_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2450_0_q_source_blind_theorem", "DO_NOT_PROMOTE_BREF_Q_SOURCE_BLINDNESS", "the theorem is conditional on parent-owned fixed-branch/no-q-source/no-marker/counterterm rules that are not present", "partial_q/source Delta_ref remain retained"),
        ("DEC2450_1_countermodels", "RETAIN_Q_AND_SOURCE_WEIGHTED_REFERENCE_COUNTERMODELS", "they show notation-level q/source absence is not enough", "future proof must explicitly forbid q/source labels and GM calibration in B_ref/B_ct/fixed branch"),
        ("DEC2450_2_next_route", "TARGET_FIXED_BRANCH_SELECTOR", "without the selector, every B_ref derivative component remains an imposed reference condition", "select 2451"),
        ("DEC2450_3_public", "NO_GITHUB_ACTION", "private nonclaim derivation checkpoint", "continue privately"),
    ]
    return [
        base_row(decision_id=decision_id, decision=decision, rationale=rationale, consequence=consequence)
        for decision_id, decision, rationale, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    row = {
        "route_id": "NEXT2450_0_selected",
        "selection_status": "selected",
        "target_file": "2451-Y5-R2FR-Bref-fixed-branch-selector-or-Delta-ref-q-source-provenance-pack.md",
        "target_script": "scripts/Y5_R2FR_Bref_fixed_branch_selector_or_Delta_ref_q_source_provenance_pack_2451.py",
        "task": "derive the fixed-branch selector that makes B_ref q/source-blind, or require provenance for finite q/source components of Delta_ref",
        "acceptance_target": "fixed branch data are parent-selected without q/source/material/GM calibration labels, or q/source Delta_ref rows remain explicit nonclaim with source/value/normalization blockers",
        "guardrails": "do not tune B_ref to source mass; do not import EH/GHY as proof; do not set N_E by convention; do not claim Delta_ref/S_Eq/deltaH/WEP/PPN/local GR; do not edit formalization-workbench; do not push GitHub",
    }
    return [base_row(**row)]


def copy_outputs() -> list[dict[str, Any]]:
    copy_specs = {
        "queue_blindness": (OUTPUTS["blindness_attempt"], COPY_TARGETS["queue_blindness"], "B_ref q/source blindness queue"),
        "queue_components": (OUTPUTS["component_rows"], COPY_TARGETS["queue_components"], "Delta_ref q/source component templates queue"),
        "hamiltonian_components": (OUTPUTS["component_rows"], COPY_TARGETS["hamiltonian_components"], "Hamiltonian Delta_ref q/source components"),
        "local_components": (OUTPUTS["component_rows"], COPY_TARGETS["local_components"], "local Delta_ref q/source components"),
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

    add("VAL2450_00_sources_exist", all(row["path_exists"] for row in data["source_register"]), "all cited source paths exist")
    add("VAL2450_01_source_needles", all(row["needles_found"] for row in data["source_register"]), "all cited source needles are present")
    add(
        "VAL2450_02_blindness_not_promoted",
        any(row["step_id"] == "QSB2450_6_verdict" and row["proof_status"] == "FAIL_CURRENT_CLAIM" for row in data["blindness_attempt"]),
        "B_ref q/source blindness is not promoted",
    )
    add(
        "VAL2450_03_q_source_leaks_present",
        {"QSL2450_0_explicit_q_slot", "QSL2450_1_explicit_source_fields", "QSL2450_6_source_current_weight"} <= {row["channel_id"] for row in data["leakage_audit"]},
        "q/source leakage channels are explicit",
    )
    add(
        "VAL2450_04_countermodels_retained",
        {"CM2450_0_q_reference", "CM2450_1_source_weighted_reference"} <= {row["countermodel_id"] for row in data["countermodels"]},
        "q/source countermodels are retained",
    )
    add(
        "VAL2450_05_component_rows_fail_closed",
        all(row["source_path"] == "MISSING_SOURCE_FILE" and not row["valid_for_claim"] for row in data["component_rows"]),
        "component rows are source-ready but missing/nonclaim",
    )
    add(
        "VAL2450_06_claim_gates_blocked",
        all(row["gate_status"] == "BLOCKED" and not row["valid_for_claim"] for row in data["claim_gates"]),
        "all claim gates are blocked",
    )
    add(
        "VAL2450_07_next_target_written",
        len(data["next_target"]) == 1 and data["next_target"][0]["route_id"] == "NEXT2450_0_selected",
        "2451 fixed-branch selector target selected",
    )
    add(
        "VAL2450_08_branch_copies",
        all(row["source_exists"] and row["target_exists"] for row in data["branch_copies"]),
        "branch copies exist",
    )
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            name = path.name
            if any(marker in name for marker in ("2450-", "_2450", "2450_", "P8_Y5_PARENT_QLOC_2450", "P8_Y5_BRR545_2450")):
                formalization_hits.append(path)
    add("VAL2450_09_no_formalization_artifacts", len(formalization_hits) == 0, "no 2450 artifacts were written to formalization-workbench", "; ".join(str(path) for path in formalization_hits))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parses(path)
        add(f"VAL2450_CSV_{path.stem}", ok, f"CSV parses with {count} rows", detail)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2450_OVERALL",
        overall,
        "2450 refuses B_ref q/source blindness as current theorem, stages q/source component rows, and selects fixed-branch selector next",
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2450 - Y5/R2FR B_ref Q And Source Blindness Theorem Or Delta_ref Component Row

## Result
- 2450 attacks the two dangerous `B_ref` derivative horns: `partial_q Delta_ref` and `partial_source Delta_ref`.
- The q/source-blindness theorem is clean conditionally, but not parent-signed.
- Notation is not proof: writing `B_ref[gamma_ref,tau_ref,C_top]` does not exclude q/source labels hidden in the fixed branch, counterterms, material markers, or GM calibration.
- q/source component rows are staged for `Delta_ref_over_N_E`, but remain `MISSING_SOURCE_FILE` and `valid_for_claim=false`.
- Next target is `2451`: derive the fixed-branch selector or keep q/source provenance rows explicit.

## Source Register
{table(["source_id", "source_path", "path_exists", "needles_found", "role"], data["source_register"])}

## B_ref Q/Source Blindness Theorem Attempt
{table(["step_id", "statement", "mathematical_form", "proof_status", "needed_for", "blocker", "accepted_for_claim", "valid_for_claim"], data["blindness_attempt"])}

## Q/Source Leakage Channel Audit
{table(["channel_id", "leakage_channel", "forbidden_form", "current_status", "why_dangerous", "required_exit", "valid_for_claim"], data["leakage_audit"])}

## B_ref Q/Source Countermodel Ledger
{table(["countermodel_id", "construction", "preserves", "violates", "why_allowed_now", "blocks_theorem", "valid_for_claim"], data["countermodels"])}

## Delta_ref Q/Source Component Templates
{table(["row_id", "target", "formula", "required_columns", "acceptance_rule", "current_fill", "source_path", "valid_for_claim"], data["component_rows"])}

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
        "blindness_attempt": blindness_attempt_rows(),
        "leakage_audit": leakage_audit_rows(),
        "countermodels": countermodel_rows(),
        "component_rows": component_row_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key in ["source_register", "blindness_attempt", "leakage_audit", "countermodels", "component_rows", "claim_gates", "decisions", "next_target"]:
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
