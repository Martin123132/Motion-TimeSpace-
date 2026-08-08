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

DOC_PATH = ROOT / "1978-Y5-R2FR-memory-mass-gap-and-mL-derivative-bound-pack.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1978_VALIDATION.csv"

SOURCES = {
    "1977_doc": {
        "path": ROOT / "1977-Y5-R2FR-VR-separability-or-VmA-bound-row.md",
        "needles": ["ME1977_2_bound_formula", "VMA1977_1_M2_min", "NEXT1977_0_primary"],
    },
    "1977_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1977_VALIDATION.csv",
        "needles": ["VAL1977_OVERALL", "PASS"],
    },
    "1975_envelope": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1975_UB_SUPPRESSION_BOUND_ENVELOPE.csv",
        "needles": ["ENV1975_6_mL_derivative", "ENV1975_9_verdict"],
    },
    "1304_gap_map": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1304_ZM_POSITIVE_GAP_MAP_NONCLAIM.csv",
        "needles": ["ZPG1304_0_Zm_positive", "ZPG1304_2_mass_gap", "GAP_MAP_ONLY_VALUE_MISSING"],
    },
    "1304_operator": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1304_MEMORY_OPERATOR_OWNER_ATTEMPT.csv",
        "needles": ["OO1304_1_static_local_operator_map", "M_m^2=partial_m^2 V_R"],
    },
    "968_operator_inputs": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
        "needles": ["MOI968_4_mass_gap", "MISSING_GAP_INPUTS", "MOI968_6_boundary_data"],
    },
    "1348_memory": {
        "path": ROOT / "1348-Y5-R10-RAB-memory-branch-extremum-and-operator-signature-or-closure.md",
        "needles": ["OPS1348_3_M2_gap", "FORMULA_ONLY_VALUE_MISSING"],
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(row_id: str) -> dict[str, object]:
    return {
        "branch": BRANCH,
        "row_id": row_id,
        "valid_for_claim": False,
        "public_claim": False,
        "created_utc": stamp(),
    }


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


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
                "purpose": "1978 memory mass-gap and m_L derivative bound pack",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def mass_gap_rows() -> list[dict[str, object]]:
    entries = [
        (
            "MG1978_0_operator",
            "memory Hessian operator",
            "H_m = -nabla_i(Z_m h^{ij} nabla_j) + M_m^2 + Delta_H_source/boundary/XB",
            "OPERATOR_FORM_RELATIVE",
            "source-backed sign/domain data still missing",
        ),
        (
            "MG1978_1_M2_min",
            "M2_min",
            "0 < M2_min <= partial_m^2 V_R(m_L;X_B) on D_loc after zero-mode/boundary correction",
            "MISSING_VALUE_OR_THEOREM",
            "needed for scalar mass gap and H_m inverse",
        ),
        (
            "MG1978_2_M2_bar",
            "M2_bar",
            "|partial_m^2 V_R(m_L;X_B)| <= M2_bar on D_loc",
            "MISSING_VALUE_OR_THEOREM",
            "needed to turn m_L,A into V_mA_bar",
        ),
        (
            "MG1978_3_Z_bounds",
            "Z_min,Z_bar",
            "0 < Z_min <= Z_m <= Z_bar on D_loc",
            "MISSING_VALUE_OR_THEOREM",
            "needed for ellipticity and gradient/stress normalization",
        ),
        (
            "MG1978_4_domain_spectrum",
            "lambda_1(D_loc)",
            "first positive eigenvalue or zero-mode removal for selected local exterior boundary problem",
            "MISSING_DOMAIN_SPECTRUM",
            "needed if mass gap is weak or zero modes survive",
        ),
        (
            "MG1978_5_inverse_bound",
            "H_m inverse envelope",
            "If G_m := Z_min lambda_1(D_loc)+M2_min-Eta_H > 0, then ||H_m^{-1}|| <= 1/G_m",
            "FORMULA_READY_VALUES_MISSING",
            "Eta_H collects source/boundary/X_B correction norms",
        ),
        (
            "MG1978_6_current_status",
            "current corpus",
            "1304/1348/968 provide the operator scaffold but mark mass gap, signs, domain, and boundary data missing",
            "MASS_GAP_PACK_NOT_CLAIMABLE",
            "no H_m inverse or local no-tower claim follows yet",
        ),
    ]
    rows = []
    for row_id, item, formula, status, role in entries:
        row = base(row_id)
        row.update({"item": item, "formula": formula, "status": status, "role": role})
        rows.append(row)
    return rows


def ml_envelope_rows() -> list[dict[str, object]]:
    entries = [
        ("MLE1978_0_epsilon_U", "epsilon_U", "U_B <= epsilon_U on D_loc", "MISSING_LOCAL_RANGE", "screening strength"),
        ("MLE1978_1_Amin", "A_min", "A_curv >= A_min on D_loc", "MISSING_LOCAL_RANGE", "denominator of derivative bounds"),
        ("MLE1978_2_Delta", "Delta_min", "Delta_B >= Delta_min > 0", "MISSING_PARENT_VALUE", "logistic width lower bound"),
        ("MLE1978_3_H", "H0,H1A", "|H_L|<=H0 and |(1+A) partial_A H_L|<=H1A", "MISSING_FUNCTION_BOUND", "D_L derivative envelope"),
        ("MLE1978_4_m2", "M20,M21A", "|m_2|<=M20 and |(1+A) partial_A m_2|<=M21A", "MISSING_FUNCTION_BOUND", "m_L derivative envelope"),
        (
            "MLE1978_5_mL_derivative",
            "mL_A_bar",
            "mL_A_bar := epsilon_U^2[2H0M20(H0/Delta_min+H1A)+H0^2M21A]/(1+A_min)",
            "FORMULA_READY_VALUES_MISSING",
            "upper bound for |partial_Acurv m_L|",
        ),
        (
            "MLE1978_6_current_status",
            "m_L envelope",
            "1975 supplied formulas but none of the constants are sourced",
            "ENVELOPE_INPUTS_MISSING",
            "V_mA route remains nonclaim",
        ),
    ]
    rows = []
    for row_id, item, formula, status, role in entries:
        row = base(row_id)
        row.update({"item": item, "formula": formula, "status": status, "role": role})
        rows.append(row)
    return rows


def vma_executable_rows() -> list[dict[str, object]]:
    entries = [
        (
            "VMA1978_0_identity",
            "mixed Hessian identity",
            "V_mA = -V_mm m_L,A on the moving-extremum branch",
            "CARRIED_FROM_1977",
            "default non-separable V_R route",
        ),
        (
            "VMA1978_1_bound",
            "V_mA_bar",
            "V_mA_bar := M2_bar * mL_A_bar",
            "FORMULA_READY_VALUES_MISSING",
            "requires MG1978_2 and MLE1978_5",
        ),
        (
            "VMA1978_2_full_vertex",
            "B_V",
            "B_V <= V_mA_bar*C_XR_bar + B_source_boundary",
            "FORMULA_READY_VALUES_MISSING",
            "C_XR projection and side channels still open",
        ),
        (
            "VMA1978_3_cR2",
            "Delta c_R2[V_R]",
            "|Delta c_R2[V_R]| <= 1/2 Hm_inv_bar B_V^2",
            "FORMULA_READY_VALUES_MISSING",
            "requires H_m inverse and all numerator bounds",
        ),
        (
            "VMA1978_4_claim_status",
            "claim eligibility",
            "false until M2/Z/domain/mL/CXR/source-boundary/units rows are source-backed",
            "CLAIM_BLOCKED",
            "strict nonclaim interface",
        ),
    ]
    rows = []
    for row_id, item, formula, status, role in entries:
        row = base(row_id)
        row.update({"item": item, "formula": formula, "status": status, "role": role})
        rows.append(row)
    return rows


def acquisition_rows() -> list[dict[str, object]]:
    entries = [
        ("REQ1978_0_M2", "M2_min;M2_bar", "V_R functional form or theorem bounds for partial_m^2 V_R", "HIGHEST", "blocks V_mA_bar and H_m inverse"),
        ("REQ1978_1_Z", "Z_min;Z_bar", "Z_m sign/value or constant-canonical parent adoption with transfer audit", "HIGH", "blocks ellipticity and H_m inverse"),
        ("REQ1978_2_domain", "D_loc;boundary;lambda_1", "parent-selected local exterior and boundary/zero-mode class", "HIGH", "blocks operator inverse"),
        ("REQ1978_3_mL_envelope", "epsilon_U;A_min;Delta_min;H0;H1A;M20;M21A", "local branch range and bounded coefficient functions", "HIGH", "blocks mL_A_bar"),
        ("REQ1978_4_CXR", "C_XR_bar", "projection/regularization for A_curv curvature response", "HIGH", "blocks B_V"),
        ("REQ1978_5_side", "B_source_boundary;Eta_H", "source/bath/boundary correction bounds", "HIGH", "blocks Schur numerator and H_m denominator"),
        ("REQ1978_6_units", "units convention", "m,V_R,A_curv,R_geom,c_R2 normalization", "HIGH", "blocks R11 comparison"),
    ]
    rows = []
    for row_id, required_input, source_needed, priority, blocker in entries:
        row = base(row_id)
        row.update(
            {
                "required_input": required_input,
                "source_needed": source_needed,
                "priority": priority,
                "blocker": blocker,
                "status": "MISSING_SOURCE_BACKED_VALUE_OR_THEOREM",
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        ("RUN1978_0_mass_gap", "MG1978_5_inverse_bound", "PASS_FORMULA_NONCLAIM", "H_m inverse envelope written"),
        ("RUN1978_1_mass_values", "MG1978_1..4", "REJECTED_VALUES_MISSING", "M2/Z/domain values missing"),
        ("RUN1978_2_mL_envelope", "MLE1978_5_mL_derivative", "PASS_FORMULA_NONCLAIM", "m_L derivative envelope carried forward"),
        ("RUN1978_3_vma", "VMA1978_1_bound", "REJECTED_VALUES_MISSING", "V_mA_bar cannot be filled yet"),
        ("RUN1978_4_claim", "VMA1978_4_claim_status", "REJECTED_CLAIM_BLOCKED", "nonclaim interface only"),
        ("RUN1978_VERDICT", "all_rows", "MASS_GAP_ML_PACK_READY_VALUES_MISSING_NONCLAIM", "next gate is sourcing M2/Z/domain constants or theorem zeros"),
    ]
    rows = []
    for row_id, input_row, runner_status, reason in entries:
        row = base(row_id)
        row.update({"input_row": input_row, "runner_status": runner_status, "reason": reason, "accepted_for_claim": False})
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1978_0_M2_bounds", "M2_min/M2_bar are source-backed", "FAIL_BLOCKED", "V_R functional form/bounds missing"),
        ("CG1978_1_Z_domain", "Z_min/domain/lambda_1 are source-backed", "FAIL_BLOCKED", "operator sign/domain missing"),
        ("CG1978_2_mL_envelope", "m_L derivative constants are source-backed", "FAIL_BLOCKED", "local range/function bounds missing"),
        ("CG1978_3_VmA_bar", "V_mA_bar is executable", "FAIL_BLOCKED", "M2_bar and mL_A_bar missing"),
        ("CG1978_4_R11_score", "Delta c_R2[V_R] can be compared to R11", "FAIL_BLOCKED", "CXR/source/Hm/units incomplete"),
        ("CG1978_5_EH_local_GR", "EH/local GR follows", "FAIL_BLOCKED", "R2/fR gate remains open"),
    ]
    rows = []
    for row_id, claim, status, reason in entries:
        row = base(row_id)
        row.update({"claim": claim, "status": status, "reason": reason})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    entries = [
        (
            "DEC1978_0_gain",
            "EXECUTABLE_PACK_FORMULAS_WRITTEN",
            "1978 turns the moving-extremum identity into a full nonclaim execution pack: H_m inverse, mL_A_bar, V_mA_bar, B_V, and Delta c_R2[V_R].",
            "use these formulas as the acceptance contract for future sourcing",
        ),
        (
            "DEC1978_1_limit",
            "VALUES_AND_DOMAIN_MISSING",
            "The pack cannot score because M2, Z, D_loc, m_L envelope constants, C_XR, source/boundary corrections, and units are still missing.",
            "do not claim local EH or no-tower",
        ),
        (
            "DEC1978_2_best_next",
            "M2_Z_DOMAIN_FIRST",
            "The most central missing constants are M2_min/M2_bar and Z_min/domain, because they control both numerator and denominator.",
            "try mass-gap theorem/source row before C_XR numeric scoring",
        ),
    ]
    rows = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1978_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1979-Y5-R2FR-M2-Z-domain-theorem-or-first-finite-row.md",
            "target_script": "scripts/Y5_R2FR_M2_Z_domain_theorem_or_first_finite_row_1979.py",
            "objective": "try to derive/source M2_min, M2_bar, Z_min, and D_loc/lambda_1, or instantiate the first finite nonclaim mass-gap row",
            "acceptance_output": "mass-gap/ellipticity theorem checklist or finite M2/Z/domain row template",
            "nonclaim_rule": "no EH/local-GR claim while H_m inverse and V_mA_bar are not source-backed",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1978_0_project_position")
    row.update(
        {
            "strongest_result": "The V_R bound route is now an explicit execution pack rather than a loose idea.",
            "what_improved": "H_m inverse, m_L derivative, V_mA_bar, and Delta c_R2[V_R] are connected in one audited chain.",
            "still_missing": "M2_min/M2_bar, Z_min/Z_bar, D_loc/lambda_1, envelope constants, C_XR_bar, source/boundary corrections, units",
            "claim_status": "private nonclaim; formulas ready, values missing",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1978_SOURCE_REGISTER.csv",
    "mass_gap": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1978_MEMORY_MASS_GAP_PACK.csv",
    "ml_envelope": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1978_ML_DERIVATIVE_ENVELOPE_INPUTS.csv",
    "vma_executable": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1978_VMA_EXECUTABLE_BOUND_PACK.csv",
    "acquisition": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1978_ACQUISITION_REQUIREMENTS.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1978_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1978_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1978_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1978_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1978_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "MEMORY_MASS_GAP_ML_BOUND_1978_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1978_M2_Z_DOMAIN_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1978_0_nonclaim_weight"),
            "artifact": "1978 memory mass-gap and m_L derivative bound pack",
            "weight": "EXECUTION_PACK_READY_VALUES_MISSING",
            "reason": "bound formulas connect the chain, but no claim-valid constants are sourced",
        }
    ]
    queue = [
        {
            **base("AQ1978_0_M2_Z_domain"),
            "target": "M2/Z/domain constants",
            "needed_inputs": "M2_min;M2_bar;Z_min;Z_bar;D_loc;lambda_1;boundary class;source paths",
            "priority": "HIGHEST",
        },
        {
            **base("AQ1978_1_mL_CXR_side"),
            "target": "mL envelope, CXR, source/boundary side channels",
            "needed_inputs": "epsilon_U;A_min;Delta_min;H0/H1A;M20/M21A;C_XR_bar;B_source_boundary;Eta_H",
            "priority": "HIGH",
        },
    ]
    return {
        "source_register": source_register(),
        "mass_gap": mass_gap_rows(),
        "ml_envelope": ml_envelope_rows(),
        "vma_executable": vma_executable_rows(),
        "acquisition": acquisition_rows(),
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
    patterns = ("1978-", "*_1978_*", "*Y5*1978*", "*VAL1978*", "*P8*1978*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1978_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    gap_ok = any(row["row_id"] == "MG1978_5_inverse_bound" and row["status"] == "FORMULA_READY_VALUES_MISSING" for row in tables["mass_gap"])
    gap_fail = any(row["row_id"] == "MG1978_6_current_status" and row["status"] == "MASS_GAP_PACK_NOT_CLAIMABLE" for row in tables["mass_gap"])
    rows.append(validation_row("VAL1978_01_mass_gap", "PASS" if gap_ok and gap_fail else "FAIL", "mass-gap inverse formula written but values missing"))

    ml_ok = any(row["row_id"] == "MLE1978_5_mL_derivative" and row["status"] == "FORMULA_READY_VALUES_MISSING" for row in tables["ml_envelope"])
    rows.append(validation_row("VAL1978_02_mL_envelope", "PASS" if ml_ok else "FAIL", "m_L derivative envelope carried forward"))

    vma_ok = any(row["row_id"] == "VMA1978_3_cR2" and row["status"] == "FORMULA_READY_VALUES_MISSING" for row in tables["vma_executable"])
    rows.append(validation_row("VAL1978_03_vma_pack", "PASS" if vma_ok else "FAIL", "V_mA executable Schur formulas staged"))

    req_ok = all(row["status"] == "MISSING_SOURCE_BACKED_VALUE_OR_THEOREM" for row in tables["acquisition"])
    rows.append(validation_row("VAL1978_04_acquisition", "PASS" if req_ok else "FAIL", "all acquisition rows remain explicit missing inputs"))

    runner_ok = any(row["row_id"] == "RUN1978_VERDICT" and row["runner_status"] == "MASS_GAP_ML_PACK_READY_VALUES_MISSING_NONCLAIM" for row in tables["runner"])
    rows.append(validation_row("VAL1978_05_runner", "PASS" if runner_ok else "FAIL", "runner blocks claim"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1978_5_EH_local_GR" and row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1978_06_claim_gates", "PASS" if gate_ok else "FAIL", "all claim gates blocked"))

    decision_ok = any(row["decision"] == "M2_Z_DOMAIN_FIRST" for row in tables["decision"])
    rows.append(validation_row("VAL1978_07_decision", "PASS" if decision_ok else "FAIL", "decision selects M2/Z/domain next"))

    next_ok = tables["next"][0]["target_doc"] == "1979-Y5-R2FR-M2-Z-domain-theorem-or-first-finite-row.md"
    rows.append(validation_row("VAL1978_08_next_target", "PASS" if next_ok else "FAIL", "1979 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1978_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1978_10_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1978_11_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1978_12_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1978_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1978_OVERALL", overall, "1978 memory mass-gap and m_L derivative bound pack"))
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
        ("Memory Mass-Gap Pack", tables["mass_gap"]),
        ("m_L Derivative Envelope Inputs", tables["ml_envelope"]),
        ("V_mA Executable Bound Pack", tables["vma_executable"]),
        ("Acquisition Requirements", tables["acquisition"]),
        ("Runner Dryrun", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1978 Y5 R2FR: Memory Mass-Gap And m_L Derivative Bound Pack",
        "",
        "Private checkpoint. This converts the 1977 moving-extremum identity into an executable nonclaim input pack.",
        "",
        "Verdict: the chain is now explicit: `H_m^{-1}` needs `G_m=Z_min lambda_1(D_loc)+M2_min-Eta_H>0`; `V_mA_bar=M2_bar*mL_A_bar`; and `Delta c_R2[V_R]` is bounded by the resulting Schur numerator. The formulas are ready, but all claim-critical values remain missing: `M2_min`, `M2_bar`, `Z_min`, `Z_bar`, `D_loc`, `lambda_1`, m_L envelope constants, `C_XR_bar`, source/boundary corrections, and units.",
        "",
        "No EH/Newton/local-GR claim follows from this checkpoint.",
        "",
    ]
    for title, table_rows in sections:
        lines.extend([f"## {title}", "", markdown_table(table_rows), ""])
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
    print(f"VAL1978_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
