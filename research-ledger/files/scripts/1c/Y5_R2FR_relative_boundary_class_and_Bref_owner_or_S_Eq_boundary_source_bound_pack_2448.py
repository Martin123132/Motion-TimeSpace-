from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_RELATIVE_BOUNDARY_CLASS_AND_BREF_OWNER_OR_S_EQ_BOUNDARY_SOURCE_PACK_2448"
CHECKPOINT_ID = "2448"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2448-Y5-R2FR-relative-boundary-class-and-Bref-owner-or-S-Eq-boundary-source-bound-pack.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2448_SOURCE_REGISTER.csv",
    "owner_contract": OUT / "P8_Y5_PARENT_QLOC_2448_BREF_RELATIVE_BOUNDARY_OWNER_CONTRACT.csv",
    "bref_derivative": OUT / "P8_Y5_PARENT_QLOC_2448_BREF_QBLIND_DERIVATIVE_VECTOR.csv",
    "silence_stack": OUT / "P8_Y5_PARENT_QLOC_2448_BOUNDARY_SILENCE_STACK_FOR_S_EQ.csv",
    "source_pack": OUT / "P8_Y5_PARENT_QLOC_2448_S_EQ_BOUNDARY_SOURCE_BOUND_INPUT_PACK.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2448_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2448_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2448_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2448_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2448_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_owner_contract": QUEUE / "JR2448_BREF_RELATIVE_BOUNDARY_OWNER_CONTRACT_NONCLAIM.csv",
    "queue_source_pack": QUEUE / "JR2448_S_EQ_BOUNDARY_SOURCE_BOUND_INPUT_PACK_NONCLAIM.csv",
    "hamiltonian_source_pack": HAMILTONIAN / "S_Eq_boundary_source_bound_input_pack_2448_NONCLAIM.csv",
    "local_source_pack": LOCAL_BOUNDS / "S_Eq_boundary_source_bound_input_pack_2448_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2448_00_2447_doc",
        "source_path": ROOT / "2447-Y5-R2FR-boundary-reference-source-current-zero-theorem-or-S-Eq-residual-bound-row.md",
        "needles": ["NEXT2447_0_selected", "BZ2447_7_verdict", "SBR2447_5_RCS2446_0_total_abs", "VAL2447_OVERALL"],
        "role": "fresh handoff selecting B_ref/relative boundary owner or source pack",
    },
    {
        "source_id": "SRC2448_01_2447_bound_schema",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2447_S_EQ_BOUNDARY_RESIDUAL_BOUND_ROW_SCHEMA.csv",
        "needles": ["SBR2447_0_partial_q_Bref", "SBR2447_5_RCS2446_0_total_abs", "MISSING_SOURCE_FILE"],
        "role": "current S_Eq boundary residual schema",
    },
    {
        "source_id": "SRC2448_02_996_doc",
        "source_path": ROOT / "996-Y5-R10-relative-boundary-class-owner-or-Bref-source-bound-pack.md",
        "needles": ["RBO996_7_verdict", "BST996_5_Bref_vector_verdict", "SBI996_5_RC9940_total_abs"],
        "role": "older relative boundary/B_ref owner attempt and source pack",
    },
    {
        "source_id": "SRC2448_03_996_owner_csv",
        "source_path": OUT / "P8_Y5_R10_996_RELATIVE_BOUNDARY_OWNER_ATTEMPT.csv",
        "needles": ["RBO996_0_parent_boundary_action", "RBO996_6_Bref_derivative_vector", "RBO996_7_verdict"],
        "role": "machine-readable old owner attempt",
    },
    {
        "source_id": "SRC2448_04_996_bref_csv",
        "source_path": OUT / "P8_Y5_R10_996_BREF_SUPERSELECTION_DERIVATIVE_TEST.csv",
        "needles": ["BST996_0_source", "BST996_4_range", "BST996_5_Bref_vector_verdict"],
        "role": "machine-readable B_ref derivative vector tests",
    },
    {
        "source_id": "SRC2448_05_996_silence_csv",
        "source_path": OUT / "P8_Y5_R10_996_SILENCE_STACK_BRIDGE.csv",
        "needles": ["SSB996_0_exactness", "SSB996_3_projector_stress", "SSB996_5_stack_verdict"],
        "role": "machine-readable silence-stack bridge",
    },
    {
        "source_id": "SRC2448_06_996_source_pack",
        "source_path": OUT / "P8_Y5_R10_996_RC9940_SOURCE_BOUND_INPUT_PACK.csv",
        "needles": ["SBI996_0_Delta_ref", "SBI996_5_RC9940_total_abs", "MISSING_COMPONENT_VALUES"],
        "role": "machine-readable old RC9940 source-bound input pack",
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


def owner_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("RBO2448_0_parent_boundary_action", "parent boundary action owns B_ref and relative class", "B_total=B_GHY[g]+B_ref[gamma_ref,tau_ref,C_top]+B_class[chi_B,C_top]+B_ct[fixed_branch]", "SCAFFOLD_ONLY", "unique parent principle selecting B_ref, B_class, C_top, and allowed variations", False),
        ("RBO2448_1_Ctop_superselection", "relative/topological class C_top is fixed before readout", "delta C_top=0 and partial_source,r,t,frame,lambda C_top=0 on the local branch", "NOT_SIGNED", "parent Euler/Ward/topological selector fixing C_top before fitting", False),
        ("RBO2448_2_exact_proper_boundary", "proper exact boundary sector is q-flux silent", "B_imp=d_partial b with [B_imp]_{H_rel}=0 and partial_q(int_S2 B_imp-int_S1 B_imp)=0", "CONDITIONAL_NOT_OWNED", "proof MTS boundary representative is exact in parent-selected relative class", False),
        ("RBO2448_3_no_improper_charge_guard", "proper zero does not erase H_tau or source mass", "exact boundary zero applies only to proper-gauge/topological edge data", "NOT_SIGNED", "same-frame Hamiltonian/source-mass equality plus fixed reference branch", False),
        ("RBO2448_4_boundary_nohair", "boundary nohair kills vector/tensor/radial/frame q-hair", "T_B^TF=T_B^vector=T_B^shear=T_B^radial=T_B^time=T_B^frame=0", "NOT_DERIVED", "parent-owned homogeneous marker-free boundary action or coefficient vector", False),
        ("RBO2448_5_projector_same_domain", "same boundary domain for q, Pi_M, Q_tau and readout", "Dq[v_B]=0 and Pi_M^H[d_partial b]=0 on the same domain", "NOT_SIGNED", "single parent-owned boundary domain for quotient/projector/Hamiltonian/readout", False),
        ("RBO2448_6_Bref_derivative_vector", "B_ref derivative vector vanishes", "partial_source Delta_ref=partial_r Delta_ref=partial_t Delta_ref=partial_frame Delta_ref=partial_lambda Delta_ref=partial_q Delta_ref=0", "NOT_SIGNED", "B_ref normalization rule from parent action/topology/stationarity", False),
        ("RBO2448_7_verdict", "relative boundary class plus B_ref owner theorem", "RBO2448_0 through RBO2448_6 all pass before readout", "FAILED_CURRENT_CLAIM", "unique parent boundary action and signed silence stack", False),
    ]
    return [
        base_row(owner_id=owner_id, candidate_owner=owner, mathematical_contract=contract, owner_status=status, missing_signature=missing, accepted_for_claim=accepted)
        for owner_id, owner, contract, status, missing, accepted in rows
    ]


def bref_derivative_rows() -> list[dict[str, Any]]:
    tests = [
        ("BDV2448_0_q", "partial_q Delta_ref", "q-dependent reference drift"),
        ("BDV2448_1_source", "partial_source Delta_ref", "source-dependent reference drift"),
        ("BDV2448_2_radius", "partial_r Delta_ref", "surface/radius-dependent reference drift"),
        ("BDV2448_3_time", "partial_t Delta_ref", "clock/time-dependent reference drift"),
        ("BDV2448_4_frame", "partial_frame Delta_ref", "frame/coframe-dependent reference drift"),
        ("BDV2448_5_range", "partial_lambda Delta_ref", "range/scale-dependent reference drift"),
        ("BDV2448_6_verdict", "all B_ref derivative channels", "Delta_ref cannot be zeroed by reference choice"),
    ]
    rows = []
    for test_id, derivative, failure in tests:
        rows.append(
            base_row(
                test_id=test_id,
                derivative_test=derivative,
                needed_zero="0",
                current_value="MISSING_PARENT_BREF_RULE",
                failure_mode=failure,
                source_requirement="B_ref rule plus equation/source path or theorem_zero certificate",
                status="BLOCKED_NONCLAIM" if test_id != "BDV2448_6_verdict" else "FAIL_CURRENT_CLAIM",
            )
        )
    return rows


def silence_stack_rows() -> list[dict[str, Any]]:
    rows = [
        ("SSB2448_0_exactness", "boundary primitive exactness", "relative_boundary_qflux_over_N", "CANDIDATE_FORMULA_NOT_PRIMITIVE", "boundary representative is not parent-owned as exact primitive"),
        ("SSB2448_1_relative_class", "relative boundary class", "relative_boundary_qflux_over_N", "NOT_SIGNED", "C_top is still selectable, not parent-selected"),
        ("SSB2448_2_nohair", "boundary no vector/tensor/radial hair", "boundary_qhair_over_N", "NOT_DERIVED", "scalar/trace no-flux does not kill vector/tensor/derivative hair"),
        ("SSB2448_3_projector_stress", "projector boundary stress silence", "projector_boundary_qcurrent_over_N", "CONDITIONS_WRITTEN_NOT_CLOSED", "projector stress may still live on boundary"),
        ("SSB2448_4_proper_charge_guard", "proper-charge guard", "do not erase H_tau/N_E", "NOT_SIGNED", "same-frame source-mass equality and reference branch are still open"),
        ("SSB2448_5_stack_verdict", "silence stack closes RCS2446_0", "RCS2446_0 theorem-zero route", "NOT_DERIVED_NONCLAIM", "all silence stack clauses are useful but unsigned"),
    ]
    return [
        base_row(stack_id=stack_id, borrowed_clause=clause, applies_to=target, current_status=status, nonclaim_reason=reason)
        for stack_id, clause, target, status, reason in rows
    ]


def source_pack_rows() -> list[dict[str, Any]]:
    rows = [
        ("SBI2448_0_Delta_ref", "partial_q_Bref_over_N", "system_id;surface_pair;partial_q_Bref;Delta_ref;N_E;units;B_ref_rule;derivative_vector;source_path;equation_ref;valid_for_claim", "numeric finite dimensionless bound or theorem_zero=true; all B_ref derivative channels sourced; N_E same-frame positive", "MISSING_DELTA_REF_VALUE_AND_BREF_RULE", "RCS2446_0;S_Eq;deltaH"),
        ("SBI2448_1_relative_qflux", "relative_boundary_qflux_over_N", "system_id;surface_pair;relative_class_rule;boundary_primitive;qflux_profile;N_E;units;source_path;equation_ref;valid_for_claim", "relative class theorem-zero or sourced q-flux profile with no MISSING markers", "MISSING_RELATIVE_CLASS_OR_QFLUX_VALUE", "RCS2446_0;boundary flux"),
        ("SBI2448_2_boundary_qhair", "boundary_qhair_over_N", "system_id;hair_channel;coefficient;profile;bound;N_E;mapped_lock_row;source_path;equation_ref;valid_for_claim", "each vector/tensor/shear/time/radial/frame channel theorem-zero or sourced; no cancellation credit", "MISSING_BOUNDARY_QHAIR_COEFFICIENTS", "PPN preferred-frame/source-normalization safety"),
        ("SBI2448_3_projector_boundary", "projector_boundary_qcurrent_over_N", "system_id;surface_pair;projector_commutator;deltaPiM_boundary;domain_rule;N_E;source_path;equation_ref;valid_for_claim", "same boundary domain and Hamiltonian Pi_M projector owned, or finite sourced commutator value", "MISSING_PROJECTOR_BOUNDARY_QCURRENT", "Delta_symp_boundary;Hamiltonian integrability"),
        ("SBI2448_4_boundary_symplectic", "boundary_symplectic_qflux_over_N", "system_id;surface_pair;Delta_symp_boundary;Theta_rule;B_ref_rule;projector_rule;N_E;source_path;equation_ref;valid_for_claim", "theta/B_ref/projector boundary terms all theorem-zero or numeric, sourced, same-frame", "MISSING_SYMPLECTIC_BOUNDARY_VALUE", "RCS2446_0;deltaH curl"),
        ("SBI2448_5_RCS2446_0_total_abs", "RCS2446_0_reference_boundary_over_N", "SBI2448_0 through SBI2448_4 valid, numeric/theorem-zero, same-frame, no MISSING markers", "sum absolute component bounds; no cancellation allowed", "MISSING_COMPONENT_VALUES", "S_Eq boundary envelope; local source leg closure"),
    ]
    return [
        base_row(input_id=input_id, target=target, required_columns=columns, acceptance_rule=rule, current_fill=current_fill, blocks=blocks)
        for input_id, target, columns, rule, current_fill, blocks in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2448_0_relative_boundary_owner", "relative boundary class is parent-owned and q-flux silent", "BLOCKED", "C_top selector, exact primitive, nohair, proper-charge guard and same-domain projector remain unsigned", False),
        ("CG2448_1_Bref_superselection", "B_ref derivative vector vanishes", "BLOCKED", "B_ref rule is named by scaffold but not parent-derived", False),
        ("CG2448_2_boundary_source_bound", "S_Eq boundary/reference residual has a source-backed bound", "BLOCKED", "source pack rows are schema-only and contain MISSING rows", False),
        ("CG2448_3_RCS2446_0_zero", "RCS2446_0 is zero or bounded", "BLOCKED", "owner theorem and source pack both fail current claim", False),
        ("CG2448_4_local_GR", "deltaH, FB5540, WEP/R10/PPN/local GR pass", "BLOCKED", "2448 only contracts the first boundary residual family", False),
    ]
    return [
        base_row(claim_id=claim_id, claim=claim, gate_status=status, reason=reason, gate_pass=gate_pass)
        for claim_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2448_0_owner_attempt", "DO_NOT_PROMOTE_BREF_RELATIVE_BOUNDARY_OWNER", "the scaffold exists but parent action does not uniquely select C_top/B_ref/nohair/projector silence", "RCS2446_0 remains retained"),
        ("DEC2448_1_contract_gain", "KEEP_EXACT_BOUNDARY_OWNER_CONTRACT", "RBO2448 clauses specify exactly what a future parent action must sign", "future derivation can sign clauses rather than debate language"),
        ("DEC2448_2_source_pack", "STAGE_S_EQ_BOUNDARY_SOURCE_PACK", "if theorem stays unsigned, componentwise sourced bounds are the only honest fallback", "next checkpoint can target first component row"),
        ("DEC2448_3_next", "TARGET_BREF_DERIVATIVE_VECTOR_FIRST", "Delta_ref/B_ref drift is the first component in the boundary residual pack", "select 2449"),
        ("DEC2448_4_public", "NO_GITHUB_ACTION", "private nonclaim derivation checkpoint", "continue privately"),
    ]
    return [
        base_row(decision_id=decision_id, decision=decision, rationale=rationale, consequence=consequence)
        for decision_id, decision, rationale, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    row = {
        "route_id": "NEXT2448_0_selected",
        "selection_status": "selected",
        "target_file": "2449-Y5-R2FR-Bref-derivative-vector-theorem-or-Delta-ref-source-row-for-S-Eq.md",
        "target_script": "scripts/Y5_R2FR_Bref_derivative_vector_theorem_or_Delta_ref_source_row_for_S_Eq_2449.py",
        "task": "either derive the B_ref derivative-vector zero theorem, including partial_q/source/r/t/frame/lambda Delta_ref, or stage the first source-backed Delta_ref_over_N_E row",
        "acceptance_target": "B_ref drift is theorem-zero under parent-signed rule, or Delta_ref remains explicit nonclaim with source/value/normalization blockers",
        "guardrails": "do not tune B_ref to source mass; do not import EH/GHY as proof; do not set N_E by convention; do not claim S_Eq/deltaH/WEP/PPN/local GR; do not edit formalization-workbench; do not push GitHub",
    }
    return [base_row(**row)]


def copy_outputs() -> list[dict[str, Any]]:
    copy_specs = {
        "queue_owner_contract": (OUTPUTS["owner_contract"], COPY_TARGETS["queue_owner_contract"], "B_ref/relative boundary owner contract queue"),
        "queue_source_pack": (OUTPUTS["source_pack"], COPY_TARGETS["queue_source_pack"], "S_Eq boundary source-bound pack queue"),
        "hamiltonian_source_pack": (OUTPUTS["source_pack"], COPY_TARGETS["hamiltonian_source_pack"], "Hamiltonian source boundary pack"),
        "local_source_pack": (OUTPUTS["source_pack"], COPY_TARGETS["local_source_pack"], "local S_Eq boundary source-bound pack"),
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

    add("VAL2448_00_sources_exist", all(row["path_exists"] for row in data["source_register"]), "all cited source paths exist")
    add("VAL2448_01_source_needles", all(row["needles_found"] for row in data["source_register"]), "all cited source needles are present")
    add(
        "VAL2448_02_owner_not_promoted",
        any(row["owner_id"] == "RBO2448_7_verdict" and row["owner_status"] == "FAILED_CURRENT_CLAIM" for row in data["owner_contract"]),
        "B_ref/relative boundary owner theorem is not promoted",
    )
    add(
        "VAL2448_03_Bref_vector_blocked",
        any(row["test_id"] == "BDV2448_6_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in data["bref_derivative"]),
        "B_ref derivative vector remains blocked",
    )
    add(
        "VAL2448_04_silence_stack_nonclaim",
        any(row["stack_id"] == "SSB2448_5_stack_verdict" and row["current_status"] == "NOT_DERIVED_NONCLAIM" for row in data["silence_stack"]),
        "silence stack remains nonclaim",
    )
    add(
        "VAL2448_05_source_pack_fail_closed",
        all("MISSING" in row["current_fill"] and not row["valid_for_claim"] for row in data["source_pack"]),
        "S_Eq boundary source pack is source-ready but missing/nonclaim",
    )
    add(
        "VAL2448_06_claim_gates_blocked",
        all(row["gate_status"] == "BLOCKED" and not row["valid_for_claim"] for row in data["claim_gates"]),
        "all claim gates are blocked",
    )
    add(
        "VAL2448_07_next_target_written",
        len(data["next_target"]) == 1 and data["next_target"][0]["route_id"] == "NEXT2448_0_selected",
        "2449 B_ref derivative-vector target selected",
    )
    add(
        "VAL2448_08_branch_copies",
        all(row["source_exists"] and row["target_exists"] for row in data["branch_copies"]),
        "branch copies exist",
    )
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            name = path.name
            if any(marker in name for marker in ("2448-", "_2448", "2448_", "P8_Y5_PARENT_QLOC_2448", "P8_Y5_BRR545_2448")):
                formalization_hits.append(path)
    add("VAL2448_09_no_formalization_artifacts", len(formalization_hits) == 0, "no 2448 artifacts were written to formalization-workbench", "; ".join(str(path) for path in formalization_hits))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parses(path)
        add(f"VAL2448_CSV_{path.stem}", ok, f"CSV parses with {count} rows", detail)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2448_OVERALL",
        overall,
        "2448 keeps B_ref/relative boundary owner theorem nonclaim, stages S_Eq boundary source pack, and selects B_ref derivative vector next",
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2448 - Y5/R2FR Relative Boundary Class And B_ref Owner Or S_Eq Boundary Source Bound Pack

## Result
- 2448 tries the proper owner route for `RCS2446_0`: parent-own `B_ref`, the relative boundary class, no-hair, projector silence, and same-frame normalization.
- The scaffold exists, but the owner theorem still does not close. `B_ref` and `C_top` are not parent-selected in the current corpus.
- The useful gain is precision: the `B_ref` derivative vector now includes `partial_q`, `partial_source`, `partial_r`, `partial_t`, `partial_frame`, and `partial_lambda` channels.
- The fallback `S_E^q` boundary source-bound pack is staged, but every row remains `MISSING` and `valid_for_claim=false`.
- Next target is `2449`: attack the `B_ref` derivative vector directly or fill the first `Delta_ref` source row.

## Source Register
{table(["source_id", "source_path", "path_exists", "needles_found", "role"], data["source_register"])}

## B_ref / Relative Boundary Owner Contract
{table(["owner_id", "candidate_owner", "mathematical_contract", "owner_status", "missing_signature", "accepted_for_claim", "valid_for_claim"], data["owner_contract"])}

## B_ref Q-Blind Derivative Vector
{table(["test_id", "derivative_test", "needed_zero", "current_value", "failure_mode", "source_requirement", "status", "valid_for_claim"], data["bref_derivative"])}

## Boundary Silence Stack For S_Eq
{table(["stack_id", "borrowed_clause", "applies_to", "current_status", "nonclaim_reason", "valid_for_claim"], data["silence_stack"])}

## S_Eq Boundary Source Bound Input Pack
{table(["input_id", "target", "required_columns", "acceptance_rule", "current_fill", "blocks", "valid_for_claim"], data["source_pack"])}

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
        "owner_contract": owner_contract_rows(),
        "bref_derivative": bref_derivative_rows(),
        "silence_stack": silence_stack_rows(),
        "source_pack": source_pack_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key in ["source_register", "owner_contract", "bref_derivative", "silence_stack", "source_pack", "claim_gates", "decisions", "next_target"]:
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
