from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1856"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1856-Y5-R2FR-derive-X-sector-from-MTS-primitives-or-reject-physical-scalar.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1856_SOURCE_REGISTER.csv",
    "primitive_scan": RESIDUALS / "P8_Y5_PARENT_QLOC_1856_PRIMITIVE_EVIDENCE_SCAN.csv",
    "physical_scalar_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1856_PHYSICAL_SCALAR_PRIMITIVE_DERIVATION_AUDIT.csv",
    "constraint_route": RESIDUALS / "P8_Y5_PARENT_QLOC_1856_CONSTRAINT_AUXILIARY_ROUTE_AUDIT.csv",
    "fork_verdict": RESIDUALS / "P8_Y5_PARENT_QLOC_1856_SCALAR_VS_CONSTRAINT_FORK_VERDICT.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1856_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1856_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1856_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1856_VALIDATION.csv",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def source_path(relative_path: str) -> str:
    return rel(ROOT / relative_path)


def ensure_dirs() -> None:
    for path in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def primitive_scan_rows() -> list[dict[str, Any]]:
    patterns = {
        "primitive": "primitive",
        "motion_load": "motion-load",
        "constraint": "constraint",
        "auxiliary": "auxiliary",
        "quotient": "quotient",
        "physical_scalar": "physical scalar",
        "Xhat": "Xhat",
        "not_derived": "NOT_DERIVED",
        "fail_current_claim": "FAIL_CURRENT_CLAIM",
    }
    files: list[Path] = []
    for glob in ["*.md", "*.csv"]:
        files.extend(path for path in ROOT.rglob(glob) if "1856" not in path.name and "__pycache__" not in path.parts)
    files = sorted(set(files))
    rows: list[dict[str, Any]] = [
        {
            "scan_id": "PES1856_0_scope",
            "pattern": "all_md_csv_excluding_1856",
            "hit_count": len(files),
            "sample_paths": ";".join(rel(path) for path in files[:8]),
            "interpretation": "scan scope for primitive, constraint and physical-scalar evidence",
            "valid_for_claim": False,
        }
    ]
    for index, (label, pattern) in enumerate(patterns.items(), start=1):
        hit_paths: list[Path] = []
        for path in files:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if pattern in text:
                hit_paths.append(path)
        rows.append(
            {
                "scan_id": f"PES1856_{index}_{label}",
                "pattern": pattern,
                "hit_count": len(hit_paths),
                "sample_paths": ";".join(rel(path) for path in hit_paths[:8]),
                "interpretation": "presence evidence only; source rows decide claim status",
                "valid_for_claim": False,
            }
        )
    return rows


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    source_rows = [
        {
            "source_id": "SRC1856_0_1855_handoff",
            "source_path": source_path("1855-Y5-R2FR-minimal-parent-X-sector-action-clause-or-demotion.md"),
            "needle": "NEXT1855_0_primary",
            "use": "selected primitive-derivation-or-reject target",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1856_1_motion_load_contract",
            "source_path": source_path("01-motion-load-route-contract.md"),
            "needle": "more primitive than the earlier motion-field formulation",
            "use": "motion-load primitive route criteria",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1856_2_nonprop_constraint",
            "source_path": source_path("07-nonpropagating-reciprocity-constraint.md"),
            "needle": "nonpropagating_reciprocity_constraint_clean_but_parent_origin_open",
            "use": "clean nonpropagating constraint route with parent-origin gap",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1856_3_qmap_null",
            "source_path": source_path("1157-Y5-R10-parent-q-map-null-generator-proof-or-cg-bound-first-fill.md"),
            "needle": "QMAP1157_7_kinetic_null_guard",
            "use": "quotient/null generator route and guard against calling missing kinetic harmless",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1856_4_primitive_constructor",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1624_PRIMITIVE_CONSTRUCTOR_DERIVATION_AUDIT.csv"),
            "needle": "PCD1624_7_verdict",
            "use": "primitive constructor derivation audit",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1856_5_primitive_deficit",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1823_PRIMITIVE_DEFICIT_ACTION_LAW_ATTEMPT.csv"),
            "needle": "DAL1823_5_verdict",
            "use": "primitive deficit action law attempt",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1856_6_auxiliary_action",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1527_LOCAL_AUXILIARY_ACTION_CONTRACT.csv"),
            "needle": "AUX1527_5_verdict",
            "use": "local auxiliary action route",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1856_7_auxiliary_elimination",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1563_AUXILIARY_ELIMINATION_GATE.csv"),
            "needle": "ELIM1563_4_current",
            "use": "auxiliary elimination theorem/gate",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1856_8_constraint_action",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1668_CONSTRAINT_FIRST_ACTION_ATTEMPT.csv"),
            "needle": "CFA1668_8_verdict",
            "use": "constraint-first action attempt",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1856_9_constraint_descent",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1675_CONSTRAINT_FIRST_DESCENT_THEOREM_ATTEMPT.csv"),
            "needle": "constraint_first_DqZ_zero_descent_theorem",
            "use": "constraint-first descent theorem attempt",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1856_10_constraint_exclusion",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1783_CONSTRAINT_FIRST_EXCLUSION_GATE.csv"),
            "needle": "CFE1783_7_verdict",
            "use": "constraint-first exclusion gate",
            "status": "FOUND",
            "valid_for_claim": False,
        },
    ]

    physical_scalar_rows = [
        {
            "audit_id": "PSD1856_0_required_primitive",
            "claim_piece": "physical scalar Xhat is a primitive MTS degree of freedom",
            "would_need": "a primitive object in motion/time/space whose local tangent is Xhat before adding an EFT action",
            "evidence_found": "NO_DIRECT_PRIMITIVE_OWNER",
            "status": "FAIL_CURRENT_CLAIM",
            "why": "current sources contain closure clauses and constructor attempts, not a primitive scalar owner",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PSD1856_1_kinetic_metric",
            "claim_piece": "Z_X follows from primitive geometry",
            "would_need": "a parent field-space metric or symplectic norm that gives positive Z_X",
            "evidence_found": "FORMULA_CONTRACT_ONLY",
            "status": "FAIL_CURRENT_CLAIM",
            "why": "1854 already found no claim-grade Z_X extraction",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PSD1856_2_mass_gap",
            "claim_piece": "M_X^2 follows from primitive curvature/deficit law",
            "would_need": "primitive potential/eigenvalue law fixing M_X^2 or a protected zero mode",
            "evidence_found": "DEFICIT_ROUTE_NOT_LINKED_TO_XHAT_HESSIAN",
            "status": "FAIL_CURRENT_CLAIM",
            "why": "primitive deficit/action attempts do not currently produce the Xhat Hessian coefficients",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PSD1856_3_source_projection",
            "claim_piece": "ordinary matter source current J_X and projections are primitive-derived",
            "would_need": "matter/readout functor from primitives giving J_X=0 or bounded charges",
            "evidence_found": "NOT_PARENT_SIGNED",
            "status": "FAIL_CURRENT_CLAIM",
            "why": "qbar, no-marker, and source-current gates remain unsigned",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PSD1856_4_verdict",
            "claim_piece": "physical scalar branch is fundamental MTS",
            "would_need": "PSD1856_0 through PSD1856_3 all pass from the same primitive parent branch",
            "evidence_found": "NO_PRIMITIVE_DERIVATION_CHAIN",
            "status": "REJECT_AS_FUNDAMENTAL_CURRENT_BRANCH",
            "why": "a propagating scalar is coherent as closure but not derived from motion/time/space primitives",
            "valid_for_claim": False,
        },
    ]

    constraint_rows = [
        {
            "route_id": "CAR1856_0_nonprop_reciprocity",
            "route": "nonpropagating reciprocity constraint",
            "supporting_evidence": "07 says this is the cleanest route found so far but parent origin is open",
            "local_GR_value": "can enforce AB=1/T^2S style local reciprocity without scalar hair",
            "remaining_gap": "derive the multiplier/constraint from parent motion-load or phase-volume balance",
            "status": "PROMISING_CONDITIONAL_ROUTE",
            "valid_for_claim": False,
        },
        {
            "route_id": "CAR1856_1_auxiliary_elimination",
            "route": "algebraic auxiliary field eliminated before phase space",
            "supporting_evidence": "1527/1563/1265 auxiliary rows give a clean elimination pattern",
            "local_GR_value": "no propagating fifth-force scalar if the auxiliary is solved away",
            "remaining_gap": "show the auxiliary object is already part of MTS primitives and not appended closure",
            "status": "PROMISING_CONDITIONAL_ROUTE",
            "valid_for_claim": False,
        },
        {
            "route_id": "CAR1856_2_constraint_first",
            "route": "constraint-first residual exclusion",
            "supporting_evidence": "1668/1675/1783 define first-class/descent/exclusion gates",
            "local_GR_value": "removes residual before matter/readout so Dq(v_X)=0 is earned rather than asserted",
            "remaining_gap": "constraint algebra, boundary charge, degree count, and physical-component lock still need proof",
            "status": "BEST_NEXT_ROUTE",
            "valid_for_claim": False,
        },
        {
            "route_id": "CAR1856_3_quotient_null",
            "route": "primitive quotient/null-generator route",
            "supporting_evidence": "1157 gives the route shape and guards against q-by-declaration",
            "local_GR_value": "if closed, local X is gauge/null, not physical scalar hair",
            "remaining_gap": "parent q object, exactness, boundary primitive and Xhat identification are unsigned",
            "status": "CONDITIONAL_ROUTE_SHAPE",
            "valid_for_claim": False,
        },
    ]

    fork_rows = [
        {
            "fork_id": "FORK1856_0_physical_scalar",
            "branch": "physical propagating scalar Xhat",
            "result": "REJECT_AS_FUNDAMENTAL_CURRENT_BRANCH",
            "reason": "no primitive owner, Z_X/M_X^2 extraction, matter source projection or same-branch action derivation exists",
            "allowed_use": "private EFT closure/test scaffold only",
            "forbidden_use": "derived local GR, direct c_g, R10 or PPN claim",
            "valid_for_claim": False,
        },
        {
            "fork_id": "FORK1856_1_constraint_auxiliary",
            "branch": "constraint/auxiliary/quotient-first X removal",
            "result": "SELECT_AS_NEXT_LOCAL_GR_ROUTE",
            "reason": "best aligns with motion/time/space primitive minimality and avoids fifth-force scalar hair",
            "allowed_use": "next derivation target for local GR/Newton reduction",
            "forbidden_use": "claiming the constraint before algebra/boundary/degree-count gates close",
            "valid_for_claim": False,
        },
        {
            "fork_id": "FORK1856_2_current_status",
            "branch": "current MTS local branch",
            "result": "NOT_DERIVED_YET_BUT_ROUTE_IS_SHARPER",
            "reason": "we know which route to attack and which route not to overclaim",
            "allowed_use": "continue with constraint-first local-GR route",
            "forbidden_use": "physical scalar as fundamental without new primitive derivation",
            "valid_for_claim": False,
        },
    ]

    claim_rows = [
        {
            "gate_id": "CG1856_0_scalar_rejection",
            "claim": "physical scalar is rejected as a fundamental current-branch derivation",
            "gate_pass": True,
            "reason": "primitive derivation chain fails and 1855 closure remains nonderived",
            "claim_allowed": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1856_1_constraint_route_selected",
            "claim": "constraint/auxiliary route is selected as next derivation target",
            "gate_pass": True,
            "reason": "multiple prior audits support it as the least dangerous local-GR route",
            "claim_allowed": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1856_2_constraint_route_proven",
            "claim": "constraint/auxiliary route already derives local GR",
            "gate_pass": False,
            "reason": "algebra, boundary charge, degree count, matter descent and physical-component lock remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1856_3_local_GR",
            "claim": "local GR/Newton reduction is derived",
            "gate_pass": False,
            "reason": "selected route is promising but not closed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1856_0_physical_scalar",
            "decision": "Demote the physical scalar branch to EFT closure only for the current corpus.",
            "because": "no current primitive derivation supplies Xhat, Z_X, M_X^2, source silence or projections.",
            "next_action": "do not use physical scalar to claim local GR or c_g bounds",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1856_1_best_route",
            "decision": "Move to constraint/auxiliary/quotient-first local-GR route.",
            "because": "it is more native to motion/time/space minimality and avoids introducing a new propagating fifth-force degree.",
            "next_action": "prove or reject the constraint-first local-GR route",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1856_2_next",
            "decision": "Next target is auxiliary/constraint X local-GR route.",
            "because": "the physical scalar branch has been demoted and 1855's parallel route is now primary.",
            "next_action": "1857-Y5-R2FR-auxiliary-constraint-X-local-GR-route.md",
            "valid_for_claim": False,
        },
    ]

    next_rows = [
        {
            "route_id": "NEXT1856_0_primary",
            "next_target": "1857-Y5-R2FR-auxiliary-constraint-X-local-GR-route.md",
            "script": "scripts/Y5_R2FR_auxiliary_constraint_X_local_GR_route_1857.py",
            "objective": "prove or reject the constraint/auxiliary/quotient-first route: X is eliminated before physical phase space and matter readout, so no local scalar hair remains",
            "selection_status": "selected",
            "success_condition": "constraint algebra, boundary charge, degree count, matter descent and physical-component lock close, or the route is demoted",
        },
        {
            "route_id": "NEXT1856_1_parallel",
            "next_target": "1857b-Y5-R2FR-motion-load-phase-volume-parent-origin.md",
            "script": "scripts/Y5_R2FR_motion_load_phase_volume_parent_origin_1857b.py",
            "objective": "derive the parent origin of the nonpropagating reciprocity constraint from motion-load/phase-volume balance",
            "selection_status": "held",
            "success_condition": "the multiplier/constraint is derived from primitive motion-load rather than inserted",
        },
    ]

    return {
        "source_register": source_rows,
        "primitive_scan": primitive_scan_rows(),
        "physical_scalar_audit": physical_scalar_rows,
        "constraint_route": constraint_rows,
        "fork_verdict": fork_rows,
        "claim_gate": claim_rows,
        "decision": decision_rows,
        "next_target": next_rows,
    }


def copy_outputs(include_validation: bool = False) -> None:
    keys = list(OUTPUTS)
    if not include_validation:
        keys = [key for key in keys if key != "validation"]
    for key in keys:
        src = OUTPUTS[key]
        if not src.exists():
            continue
        for dst_dir in [MICROSCOPE_RESIDUALS, QUARANTINE]:
            shutil.copy2(src, dst_dir / src.name)
        shutil.copy2(src, RAB_QUEUE / f"JR1856_{src.name}")


def check_sources(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        path = ROOT / str(row["source_path"])
        if not path.exists():
            missing.append(str(row["source_path"]))
    return not missing, "missing: " + "; ".join(missing) if missing else "all cited source paths exist"


def check_needles(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        path = ROOT / str(row["source_path"])
        needle = str(row["needle"])
        if path.exists() and needle not in path.read_text(encoding="utf-8", errors="ignore"):
            missing.append(f"{row['source_path']}::{needle}")
    return not missing, "missing: " + "; ".join(missing) if missing else "all cited source needles are present"


def check_csv_parse() -> tuple[bool, str]:
    malformed: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover
            malformed.append(f"{path.name}: {exc}")
    return not malformed, "malformed: " + "; ".join(malformed) if malformed else "all generated 1856 CSVs parse"


def check_branch_copies() -> tuple[bool, str]:
    missing: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        expected = [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1856_{path.name}",
        ]
        for item in expected:
            if not item.exists():
                missing.append(str(item))
    return not missing, "missing copies: " + "; ".join(missing) if missing else "branch/quarantine/queue copies exist"


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    ok, detail = check_sources(rows_map["source_register"])
    checks.append(("VAL1856_0_sources_exist", ok, detail))
    ok, detail = check_needles(rows_map["source_register"])
    checks.append(("VAL1856_1_needles_present", ok, detail))
    checks.append(
        (
            "VAL1856_2_scan_has_primitives",
            any(row["pattern"] == "primitive" and int(row["hit_count"]) > 0 for row in rows_map["primitive_scan"])
            and any(row["pattern"] == "constraint" and int(row["hit_count"]) > 0 for row in rows_map["primitive_scan"]),
            "primitive and constraint evidence exists in scan",
        )
    )
    checks.append(
        (
            "VAL1856_3_scalar_rejected",
            any(row["audit_id"] == "PSD1856_4_verdict" and row["status"] == "REJECT_AS_FUNDAMENTAL_CURRENT_BRANCH" for row in rows_map["physical_scalar_audit"]),
            "physical scalar fundamental route is rejected for current corpus",
        )
    )
    checks.append(
        (
            "VAL1856_4_constraint_selected",
            any(row["route_id"] == "CAR1856_2_constraint_first" and row["status"] == "BEST_NEXT_ROUTE" for row in rows_map["constraint_route"]),
            "constraint-first route is selected as best next route",
        )
    )
    checks.append(
        (
            "VAL1856_5_fork_verdict",
            any(row["fork_id"] == "FORK1856_0_physical_scalar" and row["result"] == "REJECT_AS_FUNDAMENTAL_CURRENT_BRANCH" for row in rows_map["fork_verdict"])
            and any(row["fork_id"] == "FORK1856_1_constraint_auxiliary" and row["result"] == "SELECT_AS_NEXT_LOCAL_GR_ROUTE" for row in rows_map["fork_verdict"]),
            "fork verdict rejects scalar and selects constraint/auxiliary route",
        )
    )
    checks.append(
        (
            "VAL1856_6_claim_gates_safe",
            any(row["gate_id"] == "CG1856_0_scalar_rejection" and boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and any(row["gate_id"] == "CG1856_2_constraint_route_proven" and not boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "route selection gates pass but local-GR proof gate remains blocked",
        )
    )
    checks.append(
        (
            "VAL1856_7_next_target_selected",
            any(row["route_id"] == "NEXT1856_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        )
    )
    checks.append(
        (
            "VAL1856_8_no_claim_flags",
            all(not boolish(row.get("valid_for_claim", False)) for rows in rows_map.values() for row in rows),
            "no valid_for_claim flags are true",
        )
    )
    ok, detail = check_csv_parse()
    checks.append(("VAL1856_9_csv_parse", ok, detail))
    ok, detail = check_branch_copies()
    checks.append(("VAL1856_10_branch_copies", ok, detail))
    pycache_path = ROOT / "scripts" / "__pycache__"
    checks.append(("VAL1856_11_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"))
    formalization_outputs = list(FORMALIZATION.rglob("*1856*")) if FORMALIZATION.exists() else []
    checks.append(("VAL1856_12_formalization_untouched", not formalization_outputs, "no 1856 outputs found under formalization-workbench"))
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1856_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1856 derive X sector from MTS primitives or reject physical scalar",
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    lines = [header, sep]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1856: Derive X-Sector From MTS Primitives Or Reject Physical Scalar",
            "",
            "**Current verdict:** the physical propagating `Xhat` scalar is rejected as a fundamental current-branch derivation. It remains useful as an EFT/closure scaffold, but the best route toward derived local GR is now constraint/auxiliary/quotient-first: eliminate the residual before physical phase space and matter readout rather than giving it scalar hair.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_path", "needle", "use", "status", "valid_for_claim"]),
            "",
            "## Primitive Evidence Scan",
            markdown_table(rows_map["primitive_scan"], ["scan_id", "pattern", "hit_count", "sample_paths", "interpretation", "valid_for_claim"]),
            "",
            "## Physical Scalar Primitive Derivation Audit",
            markdown_table(rows_map["physical_scalar_audit"], ["audit_id", "claim_piece", "would_need", "evidence_found", "status", "why", "valid_for_claim"]),
            "",
            "## Constraint/Auxiliary Route Audit",
            markdown_table(rows_map["constraint_route"], ["route_id", "route", "supporting_evidence", "local_GR_value", "remaining_gap", "status", "valid_for_claim"]),
            "",
            "## Scalar vs Constraint Fork Verdict",
            markdown_table(rows_map["fork_verdict"], ["fork_id", "branch", "result", "reason", "allowed_use", "forbidden_use", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a good pivot, not a retreat. A physical scalar is the route that gets murdered by local tests unless every coefficient is derived. The constraint-first route is harder mathematically, but it is closer to the thing we actually want: GR/Newton as the reduced local branch of motion/time/space, not as a new fifth-force field tuned to be quiet.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = build_rows_map()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs(include_validation=False)
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    copy_outputs(include_validation=True)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1856 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
