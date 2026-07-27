from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_BOUNDARY_REFERENCE_SOURCE_CURRENT_ZERO_OR_S_EQ_RESIDUAL_BOUND_2447"
CHECKPOINT_ID = "2447"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2447-Y5-R2FR-boundary-reference-source-current-zero-theorem-or-S-Eq-residual-bound-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2447_SOURCE_REGISTER.csv",
    "zero_theorem": OUT / "P8_Y5_PARENT_QLOC_2447_BOUNDARY_REFERENCE_S_EQ_ZERO_THEOREM_GATE.csv",
    "clause_audit": OUT / "P8_Y5_PARENT_QLOC_2447_BOUNDARY_REFERENCE_CLAUSE_AUDIT.csv",
    "eh_comparator": OUT / "P8_Y5_PARENT_QLOC_2447_EH_GHY_COMPARATOR_LEDGER.csv",
    "residual_bound": OUT / "P8_Y5_PARENT_QLOC_2447_S_EQ_BOUNDARY_RESIDUAL_BOUND_ROW_SCHEMA.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2447_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2447_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2447_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2447_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2447_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_zero_theorem": QUEUE / "JR2447_BOUNDARY_REFERENCE_S_EQ_ZERO_THEOREM_NONCLAIM.csv",
    "queue_residual_bound": QUEUE / "JR2447_S_EQ_BOUNDARY_RESIDUAL_BOUND_SCHEMA_NONCLAIM.csv",
    "hamiltonian_boundary": HAMILTONIAN / "boundary_reference_S_Eq_residual_2447_NONCLAIM.csv",
    "local_boundary": LOCAL_BOUNDS / "S_Eq_boundary_reference_residual_schema_2447_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2447_00_2446_doc",
        "source_path": ROOT / "2446-Y5-R2FR-EH-baseline-plus-MTS-residual-current-pack-for-S-Eq.md",
        "needles": ["NEXT2446_0_selected", "RCS2446_0_reference_boundary", "VAL2446_OVERALL"],
        "role": "fresh handoff selecting boundary/reference source-current residual",
    },
    {
        "source_id": "SRC2447_01_2446_residual_csv",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2446_MTS_RESIDUAL_CURRENT_PACK_FOR_S_EQ.csv",
        "needles": ["RCS2446_0_reference_boundary", "J_q^boundary", "NOT_PARENT_FIXED"],
        "role": "current S_Eq residual-current pack",
    },
    {
        "source_id": "SRC2447_02_995_doc",
        "source_path": ROOT / "995-Y5-R10-boundary-reference-current-zero-theorem-or-residual-bound-row.md",
        "needles": ["ZT995_7_zero_theorem_verdict", "BR995_5_RC9940_total_abs", "DEC995_0_zero_attempt"],
        "role": "older boundary/reference zero theorem and bound row attempt",
    },
    {
        "source_id": "SRC2447_03_995_zero_csv",
        "source_path": OUT / "P8_Y5_R10_995_BOUNDARY_REFERENCE_ZERO_THEOREM_GATE.csv",
        "needles": ["ZT995_0_parent_boundary_phase_space", "ZT995_7_zero_theorem_verdict", "fail_current_claim"],
        "role": "machine-readable old zero theorem gate",
    },
    {
        "source_id": "SRC2447_04_995_bound_csv",
        "source_path": OUT / "P8_Y5_R10_995_RC9940_RESIDUAL_BOUND_ROW_SCHEMA.csv",
        "needles": ["BR995_0_Delta_ref", "BR995_5_RC9940_total_abs", "MISSING_SOURCE_FILE"],
        "role": "machine-readable old boundary residual bound schema",
    },
    {
        "source_id": "SRC2447_05_995_clause_csv",
        "source_path": OUT / "P8_Y5_R10_995_CLAUSE_AUDIT.csv",
        "needles": ["CA995_0_Bref_lock", "CA995_4_projector_silence", "CA995_5_denominator"],
        "role": "machine-readable old clause audit",
    },
    {
        "source_id": "SRC2447_06_995_comparator_csv",
        "source_path": OUT / "P8_Y5_R10_995_EH_GHY_COMPARATOR_LEDGER.csv",
        "needles": ["EHG995_0_GHY_variation", "comparator_only", "forbidden_use"],
        "role": "EH/GHY comparator guard",
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


def zero_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        ("BZ2447_0_parent_boundary_phase_space", "parent boundary phase space owns q-sensitive boundary current", "S=int_M L[Phi]+int_dM B_ref; delta L=E deltaPhi+dTheta; J_q^boundary and Q_tau are obtained by variation", "BLOCKED", "full MTS parent Lagrangian and boundary term not varied", False),
        ("BZ2447_1_Bref_qblind_superselection", "B_ref is q-blind and source/frame/surface independent", "partial_q B_ref=partial_source B_ref=partial_frame B_ref=partial_surface B_ref=0", "BLOCKED", "reference subtraction is a contract, not parent-selected", False),
        ("BZ2447_2_EH_GHY_comparator_limit", "EH/GHY boundary pair is comparator only", "B_ref^MTS must be derived from MTS parent variation, not copied from GR", "COMPARATOR_ONLY", "EH import would hide the source mass in GR machinery", False),
        ("BZ2447_3_relative_cohomology_no_flux", "relative boundary class has no q-sensitive linked-sphere flux", "B_imp=dC and partial_q int_S B_imp=0 in parent-selected relative class", "BLOCKED", "exact/topological labels can still carry finite charges unless class is owned", False),
        ("BZ2447_4_boundary_nohair", "no vector/tensor/radial/frame q-hair on boundary", "partial_q T_B^TF=partial_q T_B^vector=partial_q partial_r B=partial_q partial_frame B=0", "BLOCKED", "scalar/trace no-flux is insufficient without boundary action owner", False),
        ("BZ2447_5_projector_symplectic_silence", "projector variation contributes no boundary q-current", "partial_q(delta Pi_M boundary + [d,Pi_M]J_H boundary)=0", "BLOCKED", "Pi_M/projector boundary stress remains retained", False),
        ("BZ2447_6_positive_same_frame_normalization", "N_E or M_H_ref is positive and same-frame", "N_E>0 tied to same source frame used by Q_tau, WEP/R10 and observed coframe", "BLOCKED", "same-frame measured-GM/worldtube denominator glue remains conditional", False),
        ("BZ2447_7_verdict", "RCS2446_0 boundary/reference residual vanishes", "all BZ2447_0 through BZ2447_6 clauses pass", "FAIL_CURRENT_CLAIM_RETAIN_BOUNDARY_RESIDUAL", "multiple parent ownership clauses are unsigned", False),
    ]
    return [
        base_row(gate_id=gate_id, zero_clause=clause, mathematical_requirement=requirement, current_result=result, blocker=blocker, accepted_for_zero=accepted)
        for gate_id, clause, requirement, result, blocker, accepted in rows
    ]


def clause_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("BCA2447_0_Bref_lock", "B_ref lock", "is the reference subtraction parent-selected and q-blind?", "NO", "derive B_ref rule with partial_q/source/surface/frame silence", "partial_q_Bref_over_N"),
        ("BCA2447_1_GHY_pair", "GHY/reference pair", "can EH boundary machinery be reused as MTS proof?", "NO_COMPARATOR_ONLY", "derive the MTS boundary pair or source-backed difference", "boundary_pair_difference_over_N"),
        ("BCA2447_2_relative_class", "relative cohomology class", "does exact/cohomology language itself kill q-flux?", "NO", "own relative class and linked-sphere flux theorem or bound", "q_boundary_flux_over_N"),
        ("BCA2447_3_boundary_hair", "boundary hair", "are vector/tensor/radial/frame/source hair channels eliminated?", "NO", "parent-owned marker-free homogeneous boundary action or source-backed hair rows", "q_boundary_hair_over_N"),
        ("BCA2447_4_projector_silence", "projector boundary silence", "does boundary route silence Pi_M/projector symplectic stress?", "NO", "Pi_M chain-map proof or boundary commutator row", "q_projector_boundary_over_N"),
        ("BCA2447_5_denominator", "same-frame normalization", "is denominator positive and calibrated before readout?", "NO", "N_E/M_H_ref owner tied to same-frame source worldtube", "all_RCS2446_0_ratios"),
    ]
    return [
        base_row(audit_id=audit_id, source_clause=clause, question=question, answer=answer, needed_exit=exit_needed, residual_if_open=residual)
        for audit_id, clause, question, answer, exit_needed, residual in rows
    ]


def eh_comparator_rows() -> list[dict[str, Any]]:
    rows = [
        ("EHG2447_0_GHY_variation", "EH plus GHY/reference boundary pair", "well-posed GR comparator for owned local-GR boundary current", "declare MTS B_ref=B_GHY without deriving it", "COMPARATOR_ONLY"),
        ("EHG2447_1_reference_background", "GR reference subtraction/background choice", "name the fixed-reference target", "choose reference after seeing source/readout residual", "COMPARATOR_ONLY"),
        ("EHG2447_2_Komar_ADM_shape", "standard GR boundary mass-charge shape", "downstream target for Q_tau after parent current and denominator are owned", "replace missing MTS source current by EH charge or orbital GM", "COMPARATOR_ONLY"),
        ("EHG2447_3_qblind_EH", "pure EH q-blind source comparator", "target zero q-source boundary current in the comparator branch", "claim MTS q-boundary current is zero", "COMPARATOR_ONLY"),
    ]
    return [
        base_row(comparator_id=comparator_id, object=object_name, allowed_use=allowed, forbidden_use=forbidden, status=status)
        for comparator_id, object_name, allowed, forbidden, status in rows
    ]


def residual_bound_rows() -> list[dict[str, Any]]:
    rows = [
        ("SBR2447_0_partial_q_Bref", "partial_q_Bref_over_N", "abs(partial_q B_ref)/N_E", "MISSING_BREF_QBLIND_SUPERSELECTION_OR_VALUE", "MISSING_POSITIVE_SAME_FRAME_N_E", "dimensionless", "system_id;surface_pair;partial_q_Bref;N_E;B_ref_rule;source_path;valid_for_claim"),
        ("SBR2447_1_boundary_symplectic_qflux", "boundary_symplectic_qflux_over_N", "abs(i_q omega_boundary + q_reference_flux)/N_E", "MISSING_BOUNDARY_SYMPLECTIC_QFLUX_VALUE", "MISSING_POSITIVE_SAME_FRAME_N_E", "dimensionless", "system_id;surface_pair;Theta_rule;omega_boundary_q;N_E;source_path;valid_for_claim"),
        ("SBR2447_2_relative_boundary_flux", "relative_boundary_qflux_over_N", "abs(partial_q(int_S2 B_imp-int_S1 B_imp))/N_E", "MISSING_RELATIVE_CLASS_OR_QFLUX_PROFILE", "MISSING_POSITIVE_SAME_FRAME_N_E", "dimensionless", "system_id;surface_pair;relative_class_rule;qflux_profile;N_E;source_path;valid_for_claim"),
        ("SBR2447_3_boundary_hair", "boundary_qhair_over_N", "sum_abs(q_TF,q_vector,q_shear,q_radial,q_frame_hair)/N_E", "MISSING_BOUNDARY_QHAIR_COEFFICIENTS", "MISSING_POSITIVE_SAME_FRAME_N_E", "dimensionless", "system_id;hair_channel;coefficient;profile;bound;N_E;source_path;valid_for_claim"),
        ("SBR2447_4_projector_boundary", "projector_boundary_qcurrent_over_N", "abs(partial_q(Delta_PiM_boundary+[d,Pi_M]J_H_boundary+deltaPi_M_boundary))/N_E", "MISSING_PROJECTOR_BOUNDARY_QCURRENT", "MISSING_POSITIVE_SAME_FRAME_N_E", "dimensionless", "system_id;surface_pair;projector_commutator;deltaPiM_boundary;N_E;source_path;valid_for_claim"),
        ("SBR2447_5_RCS2446_0_total_abs", "RCS2446_0_reference_boundary_over_N", "SBR2447_0+SBR2447_1+SBR2447_2+SBR2447_3+SBR2447_4", "MISSING_COMPONENT_VALUES_NO_CANCELLATION_ALLOWED", "MISSING_POSITIVE_SAME_FRAME_N_E", "dimensionless", "all component rows valid, numeric, sourced, same-frame, no MISSING markers"),
    ]
    return [
        base_row(bound_id=bound_id, target=target, formula=formula, numerator_status=num_status, denominator_status=den_status, units=units, required_source_columns=columns, source_path="MISSING_SOURCE_FILE", status="BLOCKED_NONCLAIM")
        for bound_id, target, formula, num_status, den_status, units, columns in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2447_0_RCS2446_0_zero", "RCS2446_0 boundary/reference source-current residual is zero", "BLOCKED", "B_ref, boundary class, nohair, projector silence and denominator clauses remain unsigned", False),
        ("CG2447_1_RCS2446_0_bound", "RCS2446_0 has a source-backed finite bound", "BLOCKED", "bound rows are schema-only with MISSING source/value markers", False),
        ("CG2447_2_SEq_envelope", "S_Eq no-cancellation envelope can be evaluated", "BLOCKED", "first residual family remains unvalued", False),
        ("CG2447_3_Htau_FB5540", "H_tau source charge or FB5540 closes through boundary route", "BLOCKED", "boundary/reference route remains nonclaim", False),
        ("CG2447_4_local_GR", "WEP/R10/PPN/local GR claim", "BLOCKED", "this only audits one residual-current family", False),
    ]
    return [
        base_row(claim_id=claim_id, claim=claim, gate_status=status, reason=reason, gate_pass=gate_pass)
        for claim_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2447_0_zero_attempt", "DO_NOT_PROMOTE_BOUNDARY_REFERENCE_ZERO", "the required B_ref lock, relative class, boundary nohair, projector silence and denominator clauses are not parent-owned", "RCS2446_0 remains live"),
        ("DEC2447_1_EH_comparator", "EH_GHY_COMPARATOR_ONLY", "using EH boundary machinery directly would smuggle GR into MTS", "target shape useful but no claim credit"),
        ("DEC2447_2_bound_schema", "STAGE_S_EQ_BOUNDARY_RESIDUAL_BOUND_ROWS", "if theorem-zero fails, the honest fallback is source-backed residual rows", "future work has exact columns and no-cancellation bookkeeping"),
        ("DEC2447_3_next", "TARGET_RELATIVE_BOUNDARY_CLASS_AND_BREF_OWNER", "the first concrete repair is owning B_ref and relative boundary class, or sourcing residual bound inputs", "select 2448"),
        ("DEC2447_4_public", "NO_GITHUB_ACTION", "private nonclaim checkpoint", "continue privately"),
    ]
    return [
        base_row(decision_id=decision_id, decision=decision, rationale=rationale, consequence=consequence)
        for decision_id, decision, rationale, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    row = {
        "route_id": "NEXT2447_0_selected",
        "selection_status": "selected",
        "target_file": "2448-Y5-R2FR-relative-boundary-class-and-Bref-owner-or-S-Eq-boundary-source-bound-pack.md",
        "target_script": "scripts/Y5_R2FR_relative_boundary_class_and_Bref_owner_or_S_Eq_boundary_source_bound_pack_2448.py",
        "task": "either parent-own the relative boundary class and B_ref q-blind superselection, or fill source-ready S_Eq boundary/reference residual bound inputs",
        "acceptance_target": "B_ref and relative boundary q-flux are theorem-zero under parent-signed boundary/reference ownership, or remain explicit nonclaim bound rows with units/source/projection blockers",
        "guardrails": "do not import EH/GHY as proof; do not tune B_ref to source mass; do not set boundary flux or denominator by convention; do not claim S_Eq/WEP/PPN/local GR; do not edit formalization-workbench; do not push GitHub",
    }
    return [base_row(**row)]


def copy_outputs() -> list[dict[str, Any]]:
    copy_specs = {
        "queue_zero_theorem": (OUTPUTS["zero_theorem"], COPY_TARGETS["queue_zero_theorem"], "boundary/reference S_Eq zero theorem queue"),
        "queue_residual_bound": (OUTPUTS["residual_bound"], COPY_TARGETS["queue_residual_bound"], "S_Eq boundary residual bound schema queue"),
        "hamiltonian_boundary": (OUTPUTS["residual_bound"], COPY_TARGETS["hamiltonian_boundary"], "Hamiltonian boundary/reference S_Eq residual"),
        "local_boundary": (OUTPUTS["residual_bound"], COPY_TARGETS["local_boundary"], "local S_Eq boundary residual schema"),
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

    add("VAL2447_00_sources_exist", all(row["path_exists"] for row in data["source_register"]), "all cited source paths exist")
    add("VAL2447_01_source_needles", all(row["needles_found"] for row in data["source_register"]), "all cited source needles are present")
    add(
        "VAL2447_02_zero_not_promoted",
        any(row["gate_id"] == "BZ2447_7_verdict" and "FAIL_CURRENT_CLAIM" in row["current_result"] for row in data["zero_theorem"]),
        "boundary/reference zero theorem is not promoted",
    )
    add(
        "VAL2447_03_clause_audit_complete",
        {"BCA2447_0_Bref_lock", "BCA2447_4_projector_silence", "BCA2447_5_denominator"} <= {row["audit_id"] for row in data["clause_audit"]},
        "B_ref, projector and denominator clauses are audited",
    )
    add(
        "VAL2447_04_EH_comparator_limited",
        all(row["status"] == "COMPARATOR_ONLY" for row in data["eh_comparator"]),
        "EH/GHY rows are comparator-only",
    )
    add(
        "VAL2447_05_bound_rows_fail_closed",
        all(row["source_path"] == "MISSING_SOURCE_FILE" and not row["valid_for_claim"] for row in data["residual_bound"]),
        "residual bound rows are source-ready but nonclaim/missing",
    )
    add(
        "VAL2447_06_claim_gates_blocked",
        all(row["gate_status"] == "BLOCKED" and not row["valid_for_claim"] for row in data["claim_gates"]),
        "all claim gates are blocked",
    )
    add(
        "VAL2447_07_next_target_written",
        len(data["next_target"]) == 1 and data["next_target"][0]["route_id"] == "NEXT2447_0_selected",
        "2448 B_ref/relative-boundary target selected",
    )
    add(
        "VAL2447_08_branch_copies",
        all(row["source_exists"] and row["target_exists"] for row in data["branch_copies"]),
        "branch copies exist",
    )
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            name = path.name
            if any(marker in name for marker in ("2447-", "_2447", "2447_", "P8_Y5_PARENT_QLOC_2447", "P8_Y5_BRR545_2447")):
                formalization_hits.append(path)
    add("VAL2447_09_no_formalization_artifacts", len(formalization_hits) == 0, "no 2447 artifacts were written to formalization-workbench", "; ".join(str(path) for path in formalization_hits))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parses(path)
        add(f"VAL2447_CSV_{path.stem}", ok, f"CSV parses with {count} rows", detail)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2447_OVERALL",
        overall,
        "2447 refuses boundary/reference source-current zero, stages S_Eq residual bound rows, and selects B_ref/relative boundary owner next",
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2447 - Y5/R2FR Boundary Reference Source Current Zero Theorem Or S_Eq Residual Bound Row

## Result
- 2447 attacks the first `S_E^q` residual-current family: `RCS2446_0_reference_boundary`.
- The zero route would require q-blind `B_ref`, parent-owned relative boundary class, boundary no-hair, projector symplectic silence, and a positive same-frame normalization.
- That theorem does not close in the current corpus. EH/GHY remains a comparator only.
- The fallback is now source-ready: `partial_q B_ref`, boundary symplectic q-flux, relative boundary q-flux, boundary q-hair, projector boundary q-current, and total `RCS2446_0` bound rows are staged as nonclaim.
- Next target is `2448`: own `B_ref` and the relative boundary class, or fill the first real boundary/source residual bound inputs.

## Source Register
{table(["source_id", "source_path", "path_exists", "needles_found", "role"], data["source_register"])}

## Boundary Reference S_Eq Zero Theorem Gate
{table(["gate_id", "zero_clause", "mathematical_requirement", "current_result", "blocker", "accepted_for_zero", "valid_for_claim"], data["zero_theorem"])}

## Boundary Reference Clause Audit
{table(["audit_id", "source_clause", "question", "answer", "needed_exit", "residual_if_open", "valid_for_claim"], data["clause_audit"])}

## EH/GHY Comparator Ledger
{table(["comparator_id", "object", "allowed_use", "forbidden_use", "status", "valid_for_claim"], data["eh_comparator"])}

## S_Eq Boundary Residual Bound Row Schema
{table(["bound_id", "target", "formula", "numerator_status", "denominator_status", "units", "required_source_columns", "source_path", "status", "valid_for_claim"], data["residual_bound"])}

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
        "zero_theorem": zero_theorem_rows(),
        "clause_audit": clause_audit_rows(),
        "eh_comparator": eh_comparator_rows(),
        "residual_bound": residual_bound_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key in ["source_register", "zero_theorem", "clause_audit", "eh_comparator", "residual_bound", "claim_gates", "decisions", "next_target"]:
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
