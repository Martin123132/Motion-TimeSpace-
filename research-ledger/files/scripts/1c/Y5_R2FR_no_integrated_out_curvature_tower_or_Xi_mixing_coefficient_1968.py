from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1968-Y5-R2FR-no-integrated-out-curvature-tower-or-Xi-mixing-coefficient.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1968_VALIDATION.csv"

SOURCES = {
    "1967_doc": {
        "path": ROOT / "1967-Y5-R2FR-parent-minimality-or-R2FR-coefficient-origin.md",
        "needles": ["MIN1967_4_no_integrated_out_tower", "COEF1967_3_formula_template", "NEXT1967_0_primary"],
    },
    "1967_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1967_VALIDATION.csv",
        "needles": ["VAL1967_OVERALL", "PASS"],
    },
    "826_parent_action": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
        "needles": ["AA826_0_closed_parent_template", "AA826_1_memory_sector", "AA826_2_trace_projection_lock"],
    },
    "1302_memory_stress": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
        "needles": ["MSR1302_0_canonical_scalar_stress_form", "MSR1302_2_constant_nohair_safe_case"],
    },
    "967_positive_operator": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
        "needles": ["MPO967_4_energy_identity", "MPO967_6_verdict"],
    },
    "963_derivative_order": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_963_DERIVATIVE_ORDER_AUDIT.csv",
        "needles": ["DO963_2_440_sector_reduction", "DO963_6_verdict"],
    },
    "964_minimality": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
        "needles": ["MIN964_2_no_integrated_out_tower", "MIN964_5_verdict"],
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def base(row_id: str) -> dict[str, object]:
    return {
        "branch": BRANCH,
        "row_id": row_id,
        "valid_for_claim": False,
        "public_claim": False,
        "created_utc": stamp(),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_spec in SOURCES.items():
        path = source_spec["path"]
        needles = source_spec["needles"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base(source_id)
        row.update(
            {
                "source_path": str(path),
                "purpose": "1968 no integrated-out curvature tower or Xi mixing coefficient",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def no_tower_rows() -> list[dict[str, object]]:
    entries = [
        (
            "NT1968_0_target",
            "prove eliminated hidden MTS sectors cannot generate R2/fR after reduction",
            "S_eff[e]=S_vis[e]-1/2 J_R[e]^T H_X^{-1} J_R[e]+...; require no local R^2/f(R) term",
            "TARGET_EXACT",
            "This is the real coefficient-origin gate behind the EH second-order premise.",
            "need hidden-sector Hessian, mixing current, and source/readout silence",
        ),
        (
            "NT1968_1_schur_formula",
            "If a hidden scalar block X has quadratic operator H_X and linear curvature mixing J_R=B_X R, integrating it out produces a curvature-square coefficient.",
            "Delta c_R2 ~ -1/2 B_X^T H_X^{-1} B_X, sign and factor set by action convention",
            "FORMULA_DERIVED_AS_TEMPLATE",
            "R2/fR is not mysterious: it is generated exactly by hidden scalar curvature mixing.",
            "derive B_X and H_X from parent action",
        ),
        (
            "NT1968_2_zero_conditions",
            "The generated coefficient is zero only if the curvature-mixing vector vanishes, is pure gauge/topological, is projected out, or the inverse propagator has no scalar pole in the local regime.",
            "B_X=0 or P_scalar H_X^{-1} B_X=0 or boundary/topological-only",
            "ZERO_CONDITIONS_EXPLICIT",
            "This replaces vague minimality with checkable algebra.",
            "need parent-signed B_X=0/no-pole/no-boundary-hair certificate",
        ),
        (
            "NT1968_3_memory_scalar",
            "The 826/1302 memory scalar branch is a live possible generator unless nohair/source-silence/boundary and curvature-mixing zero are signed.",
            "m sector with Z_m,V_R,X_B can contribute via metric response, potential curvature dependence, or source/bath terms",
            "MEMORY_TOWER_NOT_EXCLUDED",
            "Positive-operator silence is available only as a relative lemma with unsigned inputs.",
            "derive m operator, J_m=0, boundary zero, and B_mR=0",
        ),
        (
            "NT1968_4_bath_open_system",
            "Bath/open-system variables can generate nonlocal kernels or dissipative effective terms if not explicitly retained or shown silent.",
            "Delta S_eff may include R K^{-1}(x,y) R or time-nonlocal memory kernels",
            "NONLOCAL_TOWER_NOT_EXCLUDED",
            "A closed template is not enough where irreversible dynamics is admitted.",
            "retain bath variables or prove Markov/local no-kernel limit",
        ),
        (
            "NT1968_5_positive_operator_route",
            "A positive elliptic operator plus zero source and boundary/zero-mode removal can silence a scalar locally.",
            "0=int X L_X X => grad X=0 and X=0 under signed premises",
            "RELATIVE_ZERO_ROUTE_AVAILABLE",
            "Useful route, but it silences X only after parent signs operator/source/boundary and curvature-mixing conditions.",
            "sign MPO967 premises for the actual MTS field",
        ),
        (
            "NT1968_6_verdict",
            "No integrated-out curvature tower is not proven at 1968.",
            "hidden-sector Schur complement remains live because B_X,H_X and silence premises are missing",
            "NO_TOWER_PROOF_FAILED_CLEANLY",
            "EH second-order remains blocked; coefficient-origin fallback must now request B_X/H_X rows.",
            "stage explicit Xi/memory mixing coefficient schema",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, math_form, status, implication, required_fix in entries:
        row = base(row_id)
        row.update(
            {
                "clause": clause,
                "math_form": math_form,
                "status": status,
                "implication": implication,
                "required_fix": required_fix,
            }
        )
        rows.append(row)
    return rows


def xi_mixing_rows() -> list[dict[str, object]]:
    entries = [
        (
            "XI1968_0_generic_scalar",
            "generic hidden scalar Xi",
            "Delta c_R2 ~ -1/2 beta_Xi^2/M_Xi^2",
            "beta_Xi; M_Xi; sign; normalization; local validity regime",
            "MISSING_PARENT_BETA_AND_MASS",
            "template only; not a value",
        ),
        (
            "XI1968_1_memory_m",
            "memory scalar m",
            "Delta c_R2[m] ~ -1/2 B_mR^2/H_m in the local quadratic approximation",
            "B_mR=delta^2 S/(delta m delta R); H_m=delta^2 S/delta m^2; Z_m; V_R''; boundary/source terms",
            "MISSING_MEMORY_HESSIAN_AND_MIXING",
            "826/1302 identify the branch but not the coefficient",
        ),
        (
            "XI1968_2_trace_projection",
            "trace projection Gamma_eff/m channel",
            "linear channel can vanish if m_L is an extremum and F1=0, otherwise it can feed scalar residuals",
            "F1 certificate; extremum law; projection owner; K_MTS derivation",
            "CONDITIONAL_ZERO_ROUTE_NOT_COEFFICIENT",
            "connects prior local-extremum work to the R2/fR gate",
        ),
        (
            "XI1968_3_bath_kernel",
            "bath/open-system kernel",
            "Delta S_eff ~ R K_bath^{-1} R or nonlocal R K(x,y) R",
            "bath variables; kernel norm; locality limit; dissipation convention; source/readout map",
            "MISSING_BATH_KERNEL_OR_SILENCE_PROOF",
            "must be retained or bounded if irreversible sector remains",
        ),
        (
            "XI1968_4_zero_by_positive_operator",
            "positive-operator scalar silence",
            "if L_X positive, J_X=0, boundary removes zero modes, and B_XR=0, then X generates no R2/fR",
            "operator owner; source silence; boundary zero; curvature-mixing zero",
            "RELATIVE_ROUTE_NOT_PARENT_SIGNED",
            "best theorem path for memory/class scalars",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, field_family, coefficient_form, required_inputs, status, note in entries:
        row = base(row_id)
        row.update(
            {
                "field_family": field_family,
                "coefficient_form": coefficient_form,
                "required_inputs": required_inputs,
                "status": status,
                "note": note,
            }
        )
        rows.append(row)
    return rows


def coefficient_schema_rows() -> list[dict[str, object]]:
    entries = [
        (
            "XCS1968_0_field_list",
            "hidden_sector_inventory",
            "field_id;field_type;kept_or_integrated_out;source_path;valid_for_claim",
            "MISSING_COMPLETE_FIELD_LIST",
            "REJECT_FOR_CLAIM",
        ),
        (
            "XCS1968_1_hessian",
            "hidden_sector_hessian",
            "field_id;H_X_operator;mass_or_gap;units;positivity;zero_modes;boundary_conditions;source_path",
            "MISSING_H_X",
            "REJECT_FOR_CLAIM",
        ),
        (
            "XCS1968_2_curvature_mixing",
            "curvature_mixing",
            "field_id;B_XR;B_units;normalization;projection;source_equation",
            "MISSING_B_XR",
            "REJECT_FOR_CLAIM",
        ),
        (
            "XCS1968_3_coefficient",
            "generated_c_R2",
            "field_id;c_R2_eff;c_R2_units;sign;approximation_regime;validity_scale;source_equation",
            "MISSING_C_R2_EFF",
            "REJECT_FOR_CLAIM",
        ),
        (
            "XCS1968_4_zero_certificate",
            "no_tower_zero",
            "field_id;B_XR_zero_certificate;no_scalar_pole_certificate;boundary_silence;source_silence;valid_for_claim",
            "MISSING_ZERO_CERTIFICATE",
            "REJECT_FOR_CLAIM",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, row_type, required_fields, missing_now, runner_status in entries:
        row = base(row_id)
        row.update(
            {
                "row_type": row_type,
                "required_fields": required_fields,
                "missing_now": missing_now,
                "runner_status": runner_status,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        ("XRUN1968_0_no_tower", "XCS1968_4_zero_certificate", "REJECTED_MISSING_ZERO_CERTIFICATE", "B_XR/no-pole/source/boundary certificates missing"),
        ("XRUN1968_1_coefficient", "XCS1968_3_coefficient", "REJECTED_MISSING_C_R2_EFF", "H_X and B_XR not sourced"),
        ("XRUN1968_2_memory", "XI1968_1_memory_m", "REJECTED_MISSING_MEMORY_HESSIAN_AND_MIXING", "Z_m,V_R'',B_mR,boundary/source terms missing"),
        ("XRUN1968_3_positive_operator", "XI1968_4_zero_by_positive_operator", "REJECTED_RELATIVE_ROUTE_UNSIGNED", "MPO967 premises not parent-signed for actual field"),
        ("XRUN1968_VERDICT", "all_rows", "NO_TOWER_OR_XI_COEFFICIENT_BLOCKED_NONCLAIM", "neither no-tower proof nor generated coefficient is available"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, input_row, runner_status, reason in entries:
        row = base(row_id)
        row.update(
            {
                "input_row": input_row,
                "runner_status": runner_status,
                "reason": reason,
                "accepted_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1968_0_schur_gate", "Schur-complement coefficient gate exists.", "PASS_NONCLAIM", "formula/schema only"),
        ("CG1968_1_no_tower", "No integrated-out curvature tower is proven.", "FAIL_BLOCKED", "hidden-sector Hessian/mixing data missing"),
        ("CG1968_2_cR2_value", "Generated c_R2 has a parent-sourced value.", "FAIL_BLOCKED", "B_XR and H_X missing"),
        ("CG1968_3_memory_silence", "Memory scalar cannot generate R2/fR.", "FAIL_BLOCKED", "positive-operator/source/boundary/mixing premises unsigned"),
        ("CG1968_4_EH_second_order", "EH second-order premise cleared.", "FAIL_BLOCKED", "R2/fR tower unresolved"),
        ("CG1968_5_local_GR", "local GR/Newton derived.", "FAIL_BLOCKED", "EH/GM/PPN gates remain"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, claim, status, reason in entries:
        row = base(row_id)
        row.update({"claim": claim, "status": status, "reason": reason})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    entries = [
        (
            "DEC1968_0_verdict",
            "NO_TOWER_PROOF_FAILED_COEFFICIENT_SCHEMA_READY",
            "The hidden-sector route is now algebraic: c_R2 is controlled by curvature mixing B_XR and Hessian H_X. Neither is parent-sourced yet.",
            "do not claim EH; target memory scalar H_m/B_mR first",
        ),
        (
            "DEC1968_1_next",
            "MEMORY_SCALAR_MIXING_IS_FIRST_CONCRETE_COEFFICIENT_TARGET",
            "826 and 1302 give the most concrete hidden scalar branch, while 967 gives a relative silence lemma.",
            "derive B_mR and H_m or sign positive-operator/source/boundary/mixing-zero premises",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1968_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1969-Y5-R2FR-memory-scalar-curvature-mixing-or-positive-operator-silence.md",
            "target_script": "scripts/Y5_R2FR_memory_scalar_curvature_mixing_or_positive_operator_silence_1969.py",
            "objective": "derive B_mR and H_m for the memory scalar or prove positive-operator/source/boundary/mixing-zero silence",
            "acceptance_output": "memory scalar coefficient-origin row or parent-signed no-mixing/nohair theorem attempt",
            "nonclaim_rule": "no R2/fR/EH pass unless memory scalar mixing is zeroed or coefficient is parent-sourced",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1968_0_project_position")
    row.update(
        {
            "strongest_result": "The hidden-sector R2/fR coefficient is now reduced to B_XR and H_X via a Schur-complement gate.",
            "what_improved": "We have a calculational target instead of a vague higher-curvature worry.",
            "still_missing": "hidden field inventory, H_X, B_XR, memory Hessian/mixing, positive-operator premises, full bound curve, GM/PPN completion",
            "claim_status": "no no-tower proof, no c_R2 value, no EH/Newton/local-GR claim",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1968_SOURCE_REGISTER.csv",
    "no_tower": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1968_NO_TOWER_ATTEMPT.csv",
    "xi_mixing": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1968_XI_MIXING_LEDGER.csv",
    "coefficient_schema": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1968_XI_COEFFICIENT_SCHEMA.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1968_XI_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1968_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1968_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1968_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1968_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "NO_TOWER_XI_MIXING_1968_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1968_MEMORY_SCALAR_MIXING_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1968_0_nonclaim_weight"),
            "artifact": "1968 no integrated-out curvature tower or Xi mixing coefficient",
            "weight": "SCHUR_GATE_READY_INPUTS_MISSING",
            "reason": "B_XR/H_X target is explicit but unsourced",
        }
    ]
    queue = [
        {
            **base("AQ1968_0_memory_mixing"),
            "target": "memory scalar B_mR and H_m",
            "needed_inputs": "Z_m;V_R'';curvature dependence;source/bath terms;boundary data;normalization",
            "priority": "HIGHEST",
        },
        {
            **base("AQ1968_1_positive_operator"),
            "target": "parent-sign MPO967 for actual memory scalar",
            "needed_inputs": "operator owner;positivity;J_m=0;boundary zero;zero-mode removal;B_mR=0",
            "priority": "PARALLEL_HIGH",
        },
    ]
    return {
        "source_register": source_register(),
        "no_tower": no_tower_rows(),
        "xi_mixing": xi_mixing_rows(),
        "coefficient_schema": coefficient_schema_rows(),
        "runner": runner_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
        "snapshot": snapshot_rows(),
        "source_weight": source_weight,
        "queue": queue,
    }


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, object]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": False,
        "public_claim": False,
    }


def formalization_hits() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = ("1968-", "*_1968_*", "*Y5*1968*", "*VAL1968*", "*P8*1968*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1968_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    schur_ok = any(row["row_id"] == "NT1968_1_schur_formula" and row["status"] == "FORMULA_DERIVED_AS_TEMPLATE" for row in tables["no_tower"])
    no_tower_fail_ok = any(row["row_id"] == "NT1968_6_verdict" and row["status"] == "NO_TOWER_PROOF_FAILED_CLEANLY" for row in tables["no_tower"])
    rows.append(validation_row("VAL1968_01_no_tower_attempt", "PASS" if schur_ok and no_tower_fail_ok else "FAIL", "Schur formula written and no-tower proof not claimed"))

    memory_ok = any(row["row_id"] == "XI1968_1_memory_m" and row["status"] == "MISSING_MEMORY_HESSIAN_AND_MIXING" for row in tables["xi_mixing"])
    positive_ok = any(row["row_id"] == "XI1968_4_zero_by_positive_operator" and row["status"] == "RELATIVE_ROUTE_NOT_PARENT_SIGNED" for row in tables["xi_mixing"])
    rows.append(validation_row("VAL1968_02_memory_routes", "PASS" if memory_ok and positive_ok else "FAIL", "memory coefficient and positive-operator routes retained"))

    schema_ok = any(row["row_id"] == "XCS1968_2_curvature_mixing" and row["runner_status"] == "REJECT_FOR_CLAIM" for row in tables["coefficient_schema"])
    rows.append(validation_row("VAL1968_03_schema", "PASS" if schema_ok else "FAIL", "coefficient schema rejects missing B_XR"))

    runner_ok = any(row["row_id"] == "XRUN1968_VERDICT" and row["runner_status"] == "NO_TOWER_OR_XI_COEFFICIENT_BLOCKED_NONCLAIM" for row in tables["runner"])
    rows.append(validation_row("VAL1968_04_runner", "PASS" if runner_ok else "FAIL", "runner blocks no-tower/coefficient claim"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1968_4_EH_second_order" and row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1968_05_claim_gates", "PASS" if gate_ok else "FAIL", "EH/local-GR claims remain blocked"))

    decision_ok = any(row["decision"] == "MEMORY_SCALAR_MIXING_IS_FIRST_CONCRETE_COEFFICIENT_TARGET" for row in tables["decision"])
    rows.append(validation_row("VAL1968_06_decision", "PASS" if decision_ok else "FAIL", "memory scalar mixing selected"))

    next_ok = tables["next"][0]["target_doc"] == "1969-Y5-R2FR-memory-scalar-curvature-mixing-or-positive-operator-silence.md"
    rows.append(validation_row("VAL1968_07_next_target", "PASS" if next_ok else "FAIL", "1969 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1968_08_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1968_09_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1968_10_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1968_11_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1968_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1968_OVERALL", overall, "1968 no integrated-out curvature tower or Xi mixing coefficient"))
    return rows


def markdown_table(rows: list[dict[str, object]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, object]]], validation_rows: list[dict[str, object]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("No Integrated-Out Tower Attempt", tables["no_tower"]),
        ("Xi Mixing Ledger", tables["xi_mixing"]),
        ("Coefficient Schema", tables["coefficient_schema"]),
        ("Runner Dryrun", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1968 Y5 R2FR: No Integrated-Out Curvature Tower Or Xi Mixing Coefficient",
        "",
        "Private checkpoint. This turns the hidden-sector R2/fR problem into a calculational gate: if hidden MTS fields mix with curvature, integrating them out generates a Schur-complement R2 coefficient.",
        "",
        "Verdict: the no-tower proof is not closed. The exact missing data are now `B_XR` and `H_X`, especially for the memory scalar branch. The positive-operator silence lemma is useful but remains relative to unsigned parent inputs.",
        "",
        "No R2/fR, EH, Newton, or local-GR claim follows from this checkpoint.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1968_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
