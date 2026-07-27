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

DOC_PATH = ROOT / "1976-Y5-R2FR-Zm-and-VR-Acurv-dependence-zero-or-bound.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1976_VALIDATION.csv"

SOURCES = {
    "1975_doc": {
        "path": ROOT / "1975-Y5-R2FR-Ub-suppression-bound-envelope-and-unsuppressed-coefficient-rows.md",
        "needles": ["UNSUP1975_0_Zm", "UNSUP1975_1_Rpotential", "NEXT1975_0_primary"],
    },
    "1975_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1975_VALIDATION.csv",
        "needles": ["VAL1975_OVERALL", "PASS"],
    },
    "826_coefficients": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_826_COEFFICIENT_LEDGER.csv",
        "needles": ["C826_0_Zm", "C826_1_R_potential", "functional_form_missing"],
    },
    "826_action": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
        "needles": ["AA826_1_memory_sector", "Z_m(X_B)", "V_R(m;X_B)"],
    },
    "1306_Zm": {
        "path": ROOT / "1306-Y5-R10-RAB-Zm-parent-function-or-XB-domain-range.md",
        "needles": ["CONSTANT_CANONICAL_CLOSURE_ALLOWED_FOR_PRIVATE_SENSITIVITY_ONLY", "CANNOT_ABSORB_VARIABLE_ZM_WITHOUT_NEW_RESIDUALS"],
    },
    "1348_memory": {
        "path": ROOT / "1348-Y5-R10-RAB-memory-branch-extremum-and-operator-signature-or-closure.md",
        "needles": ["R_potential_owner", "M2_mem positive gap", "Z_mem/M2_mem parent-owned"],
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
                "purpose": "1976 Z_m and V_R A_curv dependence zero or bound",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def zm_gate_rows() -> list[dict[str, object]]:
    entries = [
        (
            "ZM1976_0_constant_canonical_route",
            "partial_Acurv Z_m=0",
            "If the parent action adopts constant positive Z_m=Z0 and the field is globally canonicalized with all transfer couplings audited, then partial_Acurv Z_m=0.",
            "RELATIVE_ZERO_ROUTE_CLEAN",
            "Best possible Z_m route, but still private/nonclaim unless parent adopted and transfer audit closes.",
        ),
        (
            "ZM1976_1_variable_route_rejected_as_zero",
            "Z_m=Z_m(X_B)",
            "A variable X_B-dependent kinetic coefficient cannot be absorbed without derivative, metric-response, and source/test transfer residuals.",
            "ZERO_ROUTE_REJECTED_IF_VARIABLE",
            "Matches 1306: variable Z_m keeps A_curv response live.",
        ),
        (
            "ZM1976_2_parent_status",
            "parent source for Z_m",
            "826 names Z_m(X_B) but marks parent value missing; 1306 found no parent function or theorem-bound.",
            "PARENT_SOURCE_MISSING",
            "No claim-valid zero or finite value exists now.",
        ),
        (
            "ZM1976_3_bound_row",
            "finite derivative bound",
            "|partial_Acurv Z_m| <= Z_A over D_loc with Z_m>=Z_min>0",
            "BOUND_TEMPLATE_READY_VALUES_MISSING",
            "Needed if constant-canonical parent route is not adopted.",
        ),
        (
            "ZM1976_4_stress_transfer",
            "canonical transfer debt",
            "Even if Z_m=Z0 is canonicalized, V_R, J_m, source/test charges, alpha numerator, and PPN normalization inherit the field rescaling.",
            "TRANSFER_AUDIT_REQUIRED",
            "Z_m can move the coupling rather than kill it.",
        ),
        (
            "ZM1976_5_verdict",
            "Z_m A_curv gate",
            "Z_m has a clean conditional zero route but it is not current-parent-signed; otherwise a finite derivative row is required.",
            "ZM_GATE_PARTIAL_ROUTE_NOT_CLOSED",
            "Do not let the constant closure become a public local-GR proof.",
        ),
    ]
    rows = []
    for row_id, object_name, statement, status, implication in entries:
        row = base(row_id)
        row.update({"object": object_name, "statement": statement, "status": status, "implication": implication})
        rows.append(row)
    return rows


def vr_gate_rows() -> list[dict[str, object]]:
    entries = [
        (
            "VR1976_0_needed_zero",
            "V_mA := partial_Acurv partial_m V_R or partial_Acurv partial_m R",
            "For the memory/environment Schur vertex to vanish, the branch must satisfy V_mA=0 at m=m_L or the active Acurv component must be projected out of V_R.",
            "ZERO_CONDITION_DERIVED",
            "This is the actual mixed-Hessian bottleneck.",
        ),
        (
            "VR1976_1_separable_route",
            "V_R(m;X_B)=V0(m;X_env)+Vroute(X_route)+constant",
            "If the m-dependent part of V_R is independent of A_curv/X_route, then V_mA=0.",
            "RELATIVE_ZERO_ROUTE_CLEAN",
            "Least-scrutiny route, but no current source signs this separability.",
        ),
        (
            "VR1976_2_Dl_powered_route",
            "V_R branch coefficients depend on D_L^2 only",
            "If the only Acurv dependence of V_mA is D_L^2-powered, it may be bounded by the 1975 U_B^2 envelope, not zeroed.",
            "SUPPRESSION_ROUTE_POSSIBLE_UNSIGNED",
            "Would connect V_R to the bound route, but functional form is missing.",
        ),
        (
            "VR1976_3_parent_status",
            "parent source for R/V_R",
            "826 marks R(m;X_B) functional form missing; 1348 marks R potential and M2_mem owner not derived.",
            "FUNCTIONAL_FORM_MISSING",
            "No zero theorem or finite derivative bound can be claimed now.",
        ),
        (
            "VR1976_4_bound_row",
            "finite mixed-Hessian bound",
            "|V_mA| <= V_mA_bar over D_loc with V_mm>=M2_min>0 and units fixed",
            "BOUND_TEMPLATE_READY_VALUES_MISSING",
            "Required for Schur/R11 scoring if separability is not proved.",
        ),
        (
            "VR1976_5_schur_vertex",
            "memory Schur numerator",
            "B_mR^Acurv includes V_mA C_XR[Acurv] plus source/boundary corrections.",
            "SCHUR_VERTEX_FORMULA_READY_VALUES_MISSING",
            "This is the first honest coefficient to carry forward.",
        ),
        (
            "VR1976_6_verdict",
            "V_R/R Acurv gate",
            "V_R remains the sharper open blocker: separability would close it, but current corpus has no functional form.",
            "VR_GATE_OPEN_BLOCKS_EH",
            "Next work should attack separability or instantiate the V_mA bound row.",
        ),
    ]
    rows = []
    for row_id, object_name, statement, status, implication in entries:
        row = base(row_id)
        row.update({"object": object_name, "statement": statement, "status": status, "implication": implication})
        rows.append(row)
    return rows


def schur_rows() -> list[dict[str, object]]:
    entries = [
        (
            "SCH1976_0_reduced_vector",
            "reduced B_YR after 1976",
            "B_YR = (B_mR_direct + V_mA*C_XR + B_source + B_boundary, B_XR) with Z_m derivative entering H_m/stress/normalization rather than V_mA directly.",
            "REDUCED_FORMULA_NONCLAIM",
            "Separates kinetic normalization risk from mixed-potential Schur vertex.",
        ),
        (
            "SCH1976_1_constant_Zm_branch",
            "if Z_m constant parent branch is adopted",
            "Z_A=0, but H_m still needs Z0, V_mm, domain, source, boundary, and transfer audit.",
            "CONDITIONAL_SIMPLIFICATION",
            "Does not by itself prove no R2/fR scalar tower.",
        ),
        (
            "SCH1976_2_VmA_branch",
            "if V_mA is finite",
            "|Delta c_R2[V]| <= 1/2 ||H_m^{-1}|| (V_mA_bar*C_XR_bar + source/boundary)^2",
            "FORMULA_READY_VALUES_MISSING",
            "Needs C_XR projection, V_mA_bar, H_m lower bound, and units.",
        ),
        (
            "SCH1976_3_claim_gate",
            "claim eligibility",
            "No Schur/R11 score until Z_m route and V_R route are both either zeroed or bounded.",
            "SCHUR_SCORE_BLOCKED",
            "Prevents partial win from being misread as local EH derivation.",
        ),
    ]
    rows = []
    for row_id, item, formula, status, blocker in entries:
        row = base(row_id)
        row.update({"item": item, "formula": formula, "status": status, "blocker": blocker})
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        ("RUN1976_0_Zm_zero", "ZM1976_0_constant_canonical_route", "PASS_RELATIVE_ZERO_ROUTE", "constant parent Z_m would zero partial_Acurv Z_m"),
        ("RUN1976_1_Zm_current", "ZM1976_5_verdict", "REJECTED_NOT_PARENT_SIGNED", "current corpus has only closure/private route"),
        ("RUN1976_2_VR_zero", "VR1976_1_separable_route", "PASS_RELATIVE_ZERO_ROUTE", "separable V_R would zero V_mA"),
        ("RUN1976_3_VR_current", "VR1976_6_verdict", "REJECTED_FUNCTIONAL_FORM_MISSING", "V_R/R functional form not sourced"),
        ("RUN1976_4_schur", "SCH1976_3_claim_gate", "REJECTED_SCHUR_SCORE_BLOCKED", "Z_m and V_R are not both zeroed/bounded"),
        ("RUN1976_VERDICT", "all_rows", "ZM_PARTIAL_ROUTE_VR_OPEN_NONCLAIM", "Z_m has a conditional escape; V_R mixed Hessian is the main live blocker"),
    ]
    rows = []
    for row_id, input_row, runner_status, reason in entries:
        row = base(row_id)
        row.update({"input_row": input_row, "runner_status": runner_status, "reason": reason, "accepted_for_claim": False})
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1976_0_Zm_zero", "partial_Acurv Z_m=0 is parent-derived", "FAIL_BLOCKED", "constant canonical route is not parent-signed/current-claim valid"),
        ("CG1976_1_Zm_bound", "finite Z_m derivative bound exists", "FAIL_BLOCKED", "Z_A/Z_min/domain/units missing"),
        ("CG1976_2_VmA_zero", "V_mA=0 is parent-derived", "FAIL_BLOCKED", "V_R separability not sourced"),
        ("CG1976_3_VmA_bound", "finite V_mA bound exists", "FAIL_BLOCKED", "V_mA_bar/M2_min/domain/units missing"),
        ("CG1976_4_R11_score", "Z_m/V_R contribution scored against R11", "FAIL_BLOCKED", "C_XR/H_m/source/boundary rows incomplete"),
        ("CG1976_5_EH_local_GR", "EH/local GR follows", "FAIL_BLOCKED", "R2/fR gate remains open"),
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
            "DEC1976_0_Zm",
            "ZM_HAS_CONDITIONAL_ESCAPE_NOT_CLAIM",
            "Z_m can be made harmless only by parent-adopted constant positive normalization plus transfer audit; current work has not signed that.",
            "keep Z_m as partial route and do not use it as proof",
        ),
        (
            "DEC1976_1_VR",
            "VR_MIXED_HESSIAN_IS_MAIN_BLOCKER",
            "Without a functional form or separability theorem for V_R/R(m;X_B), V_mA is the closest object to the actual Schur numerator.",
            "target V_R separability / V_mA bound next",
        ),
        (
            "DEC1976_2_best_next",
            "VR_SEPARABILITY_OR_VMABAR",
            "The best route is to prove V_R's m-dependent part ignores A_curv; failing that, define V_mA_bar and feed it into the Schur/R11 interface.",
            "build V_R separability theorem attempt or finite V_mA coefficient row",
        ),
    ]
    rows = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1976_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1977-Y5-R2FR-VR-separability-or-VmA-bound-row.md",
            "target_script": "scripts/Y5_R2FR_VR_separability_or_VmA_bound_row_1977.py",
            "objective": "try to prove the m-dependent memory potential is independent of A_curv, or instantiate a finite V_mA bound row for Schur/R11 scoring",
            "acceptance_output": "V_R separability theorem checklist or V_mA_bar nonclaim coefficient row",
            "nonclaim_rule": "no EH/local-GR claim while V_R mixed A_curv Hessian is unsigned",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1976_0_project_position")
    row.update(
        {
            "strongest_result": "Z_m has a clean conditional constant-canonical escape, while V_R/R remains the main mixed-Hessian blocker.",
            "what_improved": "The unsuppressed coefficient problem split into kinetic normalization transfer debt versus true potential Schur vertex.",
            "still_missing": "parent-adopted Z_m normalization, transfer audit, V_R functional form/separability, V_mA bound, H_m lower bound, C_XR projection, source/boundary rows",
            "claim_status": "private nonclaim; local EH still blocked by V_R mixed A_curv gate",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1976_SOURCE_REGISTER.csv",
    "zm_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1976_ZM_ACURV_GATE.csv",
    "vr_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1976_VR_ACURV_GATE.csv",
    "schur": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1976_ZM_VR_SCHUR_INTERFACE.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1976_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1976_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1976_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1976_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1976_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "ZM_VR_ACURV_1976_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1976_VR_SEPARABILITY_VMABAR_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1976_0_nonclaim_weight"),
            "artifact": "1976 Z_m and V_R A_curv dependence zero or bound",
            "weight": "ZM_CONDITIONAL_VR_BLOCKER",
            "reason": "Z_m has conditional constant route; V_R mixed Hessian remains unsourced",
        }
    ]
    queue = [
        {
            **base("AQ1976_0_VR_separability"),
            "target": "V_R separability / V_mA zero theorem",
            "needed_inputs": "functional form or parent theorem: V_R(m;X_B)=V0(m;X_env)+Vroute(X_route); stability; source path",
            "priority": "HIGHEST",
        },
        {
            **base("AQ1976_1_VmA_bound"),
            "target": "finite V_mA_bar row",
            "needed_inputs": "V_mA_bar; D_loc; units; V_mm lower bound; C_XR projection; source/boundary corrections",
            "priority": "FALLBACK",
        },
    ]
    return {
        "source_register": source_register(),
        "zm_gate": zm_gate_rows(),
        "vr_gate": vr_gate_rows(),
        "schur": schur_rows(),
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
    patterns = ("1976-", "*_1976_*", "*Y5*1976*", "*VAL1976*", "*P8*1976*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1976_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    zm_route_ok = any(row["row_id"] == "ZM1976_0_constant_canonical_route" and row["status"] == "RELATIVE_ZERO_ROUTE_CLEAN" for row in tables["zm_gate"])
    zm_fail_ok = any(row["row_id"] == "ZM1976_5_verdict" and row["status"] == "ZM_GATE_PARTIAL_ROUTE_NOT_CLOSED" for row in tables["zm_gate"])
    rows.append(validation_row("VAL1976_01_zm_gate", "PASS" if zm_route_ok and zm_fail_ok else "FAIL", "Z_m conditional route recorded but not closed"))

    vr_zero_ok = any(row["row_id"] == "VR1976_0_needed_zero" and row["status"] == "ZERO_CONDITION_DERIVED" for row in tables["vr_gate"])
    vr_fail_ok = any(row["row_id"] == "VR1976_6_verdict" and row["status"] == "VR_GATE_OPEN_BLOCKS_EH" for row in tables["vr_gate"])
    rows.append(validation_row("VAL1976_02_vr_gate", "PASS" if vr_zero_ok and vr_fail_ok else "FAIL", "V_R mixed-Hessian gate derived and remains open"))

    schur_ok = any(row["row_id"] == "SCH1976_2_VmA_branch" and row["status"] == "FORMULA_READY_VALUES_MISSING" for row in tables["schur"])
    rows.append(validation_row("VAL1976_03_schur_interface", "PASS" if schur_ok else "FAIL", "Schur interface retains V_mA branch"))

    runner_ok = any(row["row_id"] == "RUN1976_VERDICT" and row["runner_status"] == "ZM_PARTIAL_ROUTE_VR_OPEN_NONCLAIM" for row in tables["runner"])
    rows.append(validation_row("VAL1976_04_runner", "PASS" if runner_ok else "FAIL", "runner blocks claim"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1976_5_EH_local_GR" and row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1976_05_claim_gates", "PASS" if gate_ok else "FAIL", "all claim gates blocked"))

    decision_ok = any(row["decision"] == "VR_SEPARABILITY_OR_VMABAR" for row in tables["decision"])
    rows.append(validation_row("VAL1976_06_decision", "PASS" if decision_ok else "FAIL", "decision selects V_R separability or V_mA bound"))

    next_ok = tables["next"][0]["target_doc"] == "1977-Y5-R2FR-VR-separability-or-VmA-bound-row.md"
    rows.append(validation_row("VAL1976_07_next_target", "PASS" if next_ok else "FAIL", "1977 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1976_08_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1976_09_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1976_10_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1976_11_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1976_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1976_OVERALL", overall, "1976 Z_m and V_R Acurv dependence zero or bound"))
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
        ("Z_m A_curv Gate", tables["zm_gate"]),
        ("V_R A_curv Gate", tables["vr_gate"]),
        ("Z_m/V_R Schur Interface", tables["schur"]),
        ("Runner Dryrun", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1976 Y5 R2FR: Z_m And V_R A_curv Dependence Zero Or Bound",
        "",
        "Private checkpoint. This attacks the first unsuppressed `A_curv` coefficient rows selected in 1975.",
        "",
        "Verdict: `Z_m` has a clean conditional escape if a future parent action adopts constant positive canonical normalization and the transfer audit closes. That is not current theorem credit. `V_R/R(m;X_B)` is the sharper blocker: the mixed Hessian `V_mA := partial_Acurv partial_m V_R` must either vanish by separability or be carried as a finite Schur/R11 coefficient row. Current sources do not give the functional form.",
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
    print(f"VAL1976_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
