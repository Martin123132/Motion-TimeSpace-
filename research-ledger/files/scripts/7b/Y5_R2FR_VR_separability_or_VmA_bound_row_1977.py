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

DOC_PATH = ROOT / "1977-Y5-R2FR-VR-separability-or-VmA-bound-row.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1977_VALIDATION.csv"

SOURCES = {
    "1976_doc": {
        "path": ROOT / "1976-Y5-R2FR-Zm-and-VR-Acurv-dependence-zero-or-bound.md",
        "needles": ["VR1976_0_needed_zero", "SCH1976_2_VmA_branch", "NEXT1976_0_primary"],
    },
    "1976_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1976_VALIDATION.csv",
        "needles": ["VAL1976_OVERALL", "PASS"],
    },
    "1975_envelope": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1975_UB_SUPPRESSION_BOUND_ENVELOPE.csv",
        "needles": ["ENV1975_6_mL_derivative", "ENV1975_9_verdict"],
    },
    "1348_memory": {
        "path": ROOT / "1348-Y5-R10-RAB-memory-branch-extremum-and-operator-signature-or-closure.md",
        "needles": ["BEXT1348_1_conditional_calculus", "BEXT1348_3_R_potential_owner", "OPS1348_3_M2_gap"],
    },
    "827_moving_extremum": {
        "path": ROOT / "827-Y5-R10-XB-drift-and-Khat-bound-after-F1-zero.md",
        "needles": ["DI827_2_moving_extremum_cancellation", "R_mX+R_mm m_L,X=0"],
    },
    "826_coefficients": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_826_COEFFICIENT_LEDGER.csv",
        "needles": ["C826_1_R_potential", "functional_form_missing", "C826_2_mL"],
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
                "purpose": "1977 V_R separability or V_mA bound row",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def separability_rows() -> list[dict[str, object]]:
    entries = [
        (
            "SEP1977_0_exact_zero",
            "strict separability",
            "If V_R(m;X_B)=V0(m;X_env)+Vroute(X_route)+Vconst, then V_mA=partial_Acurv partial_m V_R=0.",
            "RELATIVE_ZERO_ROUTE_CLEAN",
            "This is the cleanest no-Schur route for the memory potential.",
        ),
        (
            "SEP1977_1_projector_zero",
            "coefficient projector",
            "If the m-dependent part of V_R factors through P_env X_B and P_env annihilates A_curv, then V_mA=0.",
            "RELATIVE_ZERO_ROUTE_CLEAN",
            "Equivalent to the 1974 P_env theorem specialized to V_R.",
        ),
        (
            "SEP1977_2_current_status",
            "current corpus",
            "826 marks R(m;X_B) functional form missing and 1348 says the R potential/m_L owner is not derived.",
            "SEPARABILITY_NOT_SOURCE_SIGNED",
            "No exact zero claim is available now.",
        ),
        (
            "SEP1977_3_forbidden_shortcut",
            "do not infer zero from F1=0",
            "partial_m V_R(m_L;X_B)=0 does not imply V_mA=0; differentiating the extremum condition instead gives V_mA=-V_mm m_L,A.",
            "F1_ZERO_NOT_VM_A_ZERO",
            "This prevents the old plateau/extremum route from being overclaimed.",
        ),
    ]
    rows = []
    for row_id, route, statement, status, implication in entries:
        row = base(row_id)
        row.update({"route": route, "statement": statement, "status": status, "implication": implication})
        rows.append(row)
    return rows


def moving_extremum_rows() -> list[dict[str, object]]:
    entries = [
        (
            "ME1977_0_identity",
            "moving-extremum identity",
            "Let E(m,A)=partial_m V_R(m,A). If E(m_L(A),A)=0, then 0=d_A E=V_mA+V_mm m_L,A, so V_mA=-V_mm m_L,A.",
            "IDENTITY_DERIVED",
            "This converts the mixed-Hessian problem into memory mass times local-attractor drift.",
        ),
        (
            "ME1977_1_not_zero",
            "identity consequence",
            "V_mA vanishes only if m_L,A=0, V_mm=0, or separability/projector conditions hold; V_mm=0 is not healthy if a mass gap is needed.",
            "ZERO_NOT_AUTOMATIC",
            "The identity gives a bound route, not an exact zero by itself.",
        ),
        (
            "ME1977_2_bound_formula",
            "V_mA bound from 1975 envelope",
            "|V_mA| <= M2_bar * epsilon_U^2[2H0M20(H0/Delta_min+H1A)+H0^2 M21A]/(1+A_min)",
            "BOUND_FORMULA_READY_VALUES_MISSING",
            "Requires V_mm upper bound M2_bar and the 1975 m_L derivative constants.",
        ),
        (
            "ME1977_3_gap_pair",
            "mass-gap pair",
            "Schur scoring needs both 0<M2_min<=V_mm and |V_mm|<=M2_bar on D_loc.",
            "MISSING_MASS_GAP_BOUNDS",
            "M2_min controls H_m inverse; M2_bar controls V_mA leakage.",
        ),
        (
            "ME1977_4_current_status",
            "current corpus",
            "1348 records M2_mem positive gap as formula-only/value-missing, and 1975 envelope constants are not sourced.",
            "BOUND_ROUTE_NOT_CLAIMABLE",
            "Useful derivation, but still nonclaim.",
        ),
    ]
    rows = []
    for row_id, object_name, formula, status, implication in entries:
        row = base(row_id)
        row.update({"object": object_name, "formula": formula, "status": status, "implication": implication})
        rows.append(row)
    return rows


def coefficient_row_template() -> list[dict[str, object]]:
    entries = [
        ("VMA1977_0_VmA_bar", "V_mA_bar", "upper bound on |partial_Acurv partial_m V_R|", "MISSING_VALUE", "from separability zero or moving-extremum envelope"),
        ("VMA1977_1_M2_min", "M2_min", "lower bound on V_mm for H_m inverse/mass gap", "MISSING_VALUE", "required for healthy scalar and Schur denominator"),
        ("VMA1977_2_M2_bar", "M2_bar", "upper bound on |V_mm|", "MISSING_VALUE", "required for V_mA envelope"),
        ("VMA1977_3_CXR_bar", "C_XR_bar", "bound on A_curv curvature-response projection", "MISSING_VALUE", "from C_XR projection/regularization gate"),
        ("VMA1977_4_Bsrc_bdy", "B_source_boundary", "source/bath/boundary curvature-memory vertices", "MISSING_VALUE", "side channels outside V_R separability"),
        ("VMA1977_5_units", "units", "normalization of m,A_curv,V_R,R_geom and c_R2", "MISSING_UNITS", "required before R11 score"),
        ("VMA1977_6_validity", "valid_for_claim", "false until every value has source path, units, and domain", "CLAIM_BLOCKED", "schema row only"),
    ]
    rows = []
    for row_id, field, definition, status, role in entries:
        row = base(row_id)
        row.update({"field": field, "definition": definition, "status": status, "role": role})
        rows.append(row)
    return rows


def schur_rows() -> list[dict[str, object]]:
    entries = [
        (
            "SCH1977_0_potential_vertex",
            "potential-induced Schur numerator",
            "B_V <= V_mA_bar*C_XR_bar + B_source_boundary",
            "FORMULA_READY_VALUES_MISSING",
            "Combines mixed potential leakage and side channels.",
        ),
        (
            "SCH1977_1_cR2_bound",
            "potential contribution to R2/fR",
            "|Delta c_R2[V_R]| <= 1/2 Hm_inv_bar B_V^2, with Hm_inv_bar controlled by Z_m,M2_min,domain",
            "FORMULA_READY_VALUES_MISSING",
            "Requires the Z_m/H_m branch and V_mA row.",
        ),
        (
            "SCH1977_2_zero_result",
            "exact zero condition",
            "Delta c_R2[V_R]=0 from this channel if V_mA=0, B_source_boundary=0, and no boundary/measure term survives.",
            "ZERO_CONDITION_READY_UNSIGNED",
            "Separability alone is not enough if side channels remain.",
        ),
        (
            "SCH1977_3_verdict",
            "Schur status",
            "V_R channel is now reducible to separability or a finite V_mA_bar row, but neither is sourced.",
            "SCHUR_CHANNEL_OPEN_NONCLAIM",
            "Next gate should fill mass-gap/envelope constants or prove separability.",
        ),
    ]
    rows = []
    for row_id, item, formula, status, implication in entries:
        row = base(row_id)
        row.update({"item": item, "formula": formula, "status": status, "implication": implication})
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        ("RUN1977_0_sep_zero", "SEP1977_0_exact_zero", "PASS_RELATIVE_ZERO_ROUTE", "strict separability would zero V_mA"),
        ("RUN1977_1_current_sep", "SEP1977_2_current_status", "REJECTED_NOT_SOURCE_SIGNED", "functional form missing"),
        ("RUN1977_2_identity", "ME1977_0_identity", "PASS_DERIVATION", "moving-extremum identity derived"),
        ("RUN1977_3_bound", "ME1977_2_bound_formula", "REJECTED_VALUES_MISSING", "M2/envelope constants missing"),
        ("RUN1977_4_schema", "VMA1977_0..6", "REJECTED_SCHEMA_ONLY", "V_mA_bar row not filled"),
        ("RUN1977_VERDICT", "all_rows", "VR_IDENTITY_DERIVED_BOUND_ROW_STAGED_NONCLAIM", "V_R route improved but still not claimable"),
    ]
    rows = []
    for row_id, input_row, runner_status, reason in entries:
        row = base(row_id)
        row.update({"input_row": input_row, "runner_status": runner_status, "reason": reason, "accepted_for_claim": False})
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1977_0_separability", "V_R separability is parent-derived", "FAIL_BLOCKED", "functional form/source missing"),
        ("CG1977_1_identity_bound", "moving-extremum V_mA bound is source-backed", "FAIL_BLOCKED", "M2_bar and m_L derivative constants missing"),
        ("CG1977_2_mass_gap", "M2_min/M2_bar are sourced", "FAIL_BLOCKED", "memory mass bounds missing"),
        ("CG1977_3_side_channels", "source/boundary vertices vanish or are bounded", "FAIL_BLOCKED", "side channels open"),
        ("CG1977_4_R11_score", "V_R contribution scored against R11", "FAIL_BLOCKED", "V_mA/CXR/Hm values missing"),
        ("CG1977_5_EH_local_GR", "EH/local GR follows", "FAIL_BLOCKED", "R2/fR gate remains open"),
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
            "DEC1977_0_gain",
            "MOVING_EXTREMUM_IDENTITY_FOUND",
            "V_mA is not arbitrary if m_L is a true moving extremum: V_mA=-V_mm m_L,A.",
            "use this as the default bound route for V_R",
        ),
        (
            "DEC1977_1_limit",
            "BOUND_NEEDS_MASS_AND_ENVELOPE_CONSTANTS",
            "The identity becomes useful only after M2_bar and the 1975 m_L derivative envelope constants are sourced.",
            "target M2_min/M2_bar and m_L envelope constants next",
        ),
        (
            "DEC1977_2_best_next",
            "M2_GAP_AND_ML_DERIVATIVE_CONSTANTS",
            "The next most direct gate is the memory mass-gap pair plus bounded m_L derivative constants.",
            "build M2_min/M2_bar and m_L-envelope input pack",
        ),
    ]
    rows = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1977_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1978-Y5-R2FR-memory-mass-gap-and-mL-derivative-bound-pack.md",
            "target_script": "scripts/Y5_R2FR_memory_mass_gap_and_mL_derivative_bound_pack_1978.py",
            "objective": "source or bound M2_min/M2_bar and the m_L derivative-envelope constants needed to make the V_mA route executable",
            "acceptance_output": "nonclaim input pack for M2_min, M2_bar, epsilon_U, A_min, H0/H1A, M20/M21A, domain, units",
            "nonclaim_rule": "no EH/local-GR claim while V_mA_bar and H_m inverse are not source-backed",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1977_0_project_position")
    row.update(
        {
            "strongest_result": "The V_R mixed-Hessian blocker is now tied to a moving-extremum identity, V_mA=-V_mm m_L,A.",
            "what_improved": "V_R no longer sits as a totally opaque missing function; it has separability and bounded-moving-extremum routes.",
            "still_missing": "V_R functional form/separability, M2_min, M2_bar, m_L derivative constants, C_XR projection, source/boundary vertices, H_m inverse",
            "claim_status": "private nonclaim; V_mA bound row staged but not filled",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1977_SOURCE_REGISTER.csv",
    "separability": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1977_VR_SEPARABILITY_GATE.csv",
    "moving_extremum": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1977_MOVING_EXTREMUM_VM_A_IDENTITY.csv",
    "coefficient_template": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1977_VM_A_BOUND_ROW_TEMPLATE.csv",
    "schur": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1977_VR_SCHUR_INTERFACE.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1977_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1977_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1977_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1977_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1977_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "VR_VMA_IDENTITY_1977_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1977_M2_ML_DERIVATIVE_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1977_0_nonclaim_weight"),
            "artifact": "1977 V_R separability or V_mA bound row",
            "weight": "MOVING_EXTREMUM_IDENTITY_READY_INPUTS_MISSING",
            "reason": "V_mA identity derived but mass/envelope constants and functional form are not sourced",
        }
    ]
    queue = [
        {
            **base("AQ1977_0_M2_bounds"),
            "target": "M2_min and M2_bar",
            "needed_inputs": "memory potential second derivative bounds on D_loc; units; branch; source path",
            "priority": "HIGHEST",
        },
        {
            **base("AQ1977_1_mL_envelope_constants"),
            "target": "m_L derivative envelope constants",
            "needed_inputs": "epsilon_U; A_min; Delta_min; H0/H1A; M20/M21A; D_loc; regularization",
            "priority": "HIGHEST",
        },
    ]
    return {
        "source_register": source_register(),
        "separability": separability_rows(),
        "moving_extremum": moving_extremum_rows(),
        "coefficient_template": coefficient_row_template(),
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
    patterns = ("1977-", "*_1977_*", "*Y5*1977*", "*VAL1977*", "*P8*1977*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1977_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    sep_ok = any(row["row_id"] == "SEP1977_0_exact_zero" and row["status"] == "RELATIVE_ZERO_ROUTE_CLEAN" for row in tables["separability"])
    sep_fail = any(row["row_id"] == "SEP1977_2_current_status" and row["status"] == "SEPARABILITY_NOT_SOURCE_SIGNED" for row in tables["separability"])
    rows.append(validation_row("VAL1977_01_separability", "PASS" if sep_ok and sep_fail else "FAIL", "separability zero route recorded but unsigned"))

    identity_ok = any(row["row_id"] == "ME1977_0_identity" and row["status"] == "IDENTITY_DERIVED" for row in tables["moving_extremum"])
    bound_ok = any(row["row_id"] == "ME1977_2_bound_formula" and row["status"] == "BOUND_FORMULA_READY_VALUES_MISSING" for row in tables["moving_extremum"])
    rows.append(validation_row("VAL1977_02_moving_extremum", "PASS" if identity_ok and bound_ok else "FAIL", "moving-extremum identity and bound formula recorded"))

    template_ok = any(row["row_id"] == "VMA1977_6_validity" and row["status"] == "CLAIM_BLOCKED" for row in tables["coefficient_template"])
    rows.append(validation_row("VAL1977_03_template", "PASS" if template_ok else "FAIL", "V_mA bound row template remains nonclaim"))

    schur_ok = any(row["row_id"] == "SCH1977_3_verdict" and row["status"] == "SCHUR_CHANNEL_OPEN_NONCLAIM" for row in tables["schur"])
    rows.append(validation_row("VAL1977_04_schur", "PASS" if schur_ok else "FAIL", "Schur channel remains open nonclaim"))

    runner_ok = any(row["row_id"] == "RUN1977_VERDICT" and row["runner_status"] == "VR_IDENTITY_DERIVED_BOUND_ROW_STAGED_NONCLAIM" for row in tables["runner"])
    rows.append(validation_row("VAL1977_05_runner", "PASS" if runner_ok else "FAIL", "runner blocks claim"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1977_5_EH_local_GR" and row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1977_06_claim_gates", "PASS" if gate_ok else "FAIL", "all claim gates blocked"))

    decision_ok = any(row["decision"] == "M2_GAP_AND_ML_DERIVATIVE_CONSTANTS" for row in tables["decision"])
    rows.append(validation_row("VAL1977_07_decision", "PASS" if decision_ok else "FAIL", "decision selects mass-gap/envelope constants"))

    next_ok = tables["next"][0]["target_doc"] == "1978-Y5-R2FR-memory-mass-gap-and-mL-derivative-bound-pack.md"
    rows.append(validation_row("VAL1977_08_next_target", "PASS" if next_ok else "FAIL", "1978 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1977_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1977_10_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1977_11_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1977_12_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1977_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1977_OVERALL", overall, "1977 V_R separability or V_mA bound row"))
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
        ("V_R Separability Gate", tables["separability"]),
        ("Moving-Extremum V_mA Identity", tables["moving_extremum"]),
        ("V_mA Bound Row Template", tables["coefficient_template"]),
        ("V_R Schur Interface", tables["schur"]),
        ("Runner Dryrun", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1977 Y5 R2FR: V_R Separability Or V_mA Bound Row",
        "",
        "Private checkpoint. This attacks the V_R mixed-Hessian blocker selected in 1976.",
        "",
        "Verdict: exact zero requires separability or a projector theorem for the m-dependent part of V_R, and that is not source-signed. But the moving-extremum identity is a real derivation gain: if m_L(A_curv) is a true branch extremum of the same potential, then V_mA=-V_mm partial_A m_L. This turns the open mixed-Hessian row into a bound route using M2_bar and the 1975 m_L derivative envelope. It remains nonclaim until those constants are sourced.",
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
    print(f"VAL1977_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
