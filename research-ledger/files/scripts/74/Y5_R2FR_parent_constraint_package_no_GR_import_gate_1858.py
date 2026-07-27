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
QUARANTINE = MICROSCOPE / "quarantine" / "1858"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1858-Y5-R2FR-parent-constraint-package-no-GR-import-gate.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1858_SOURCE_REGISTER.csv",
    "constraint_package": RESIDUALS / "P8_Y5_PARENT_QLOC_1858_PARENT_CONSTRAINT_PACKAGE_AUDIT.csv",
    "no_gr_import": RESIDUALS / "P8_Y5_PARENT_QLOC_1858_NO_GR_IMPORT_GATE.csv",
    "origin_routes": RESIDUALS / "P8_Y5_PARENT_QLOC_1858_ORIGIN_ROUTE_AUDIT.csv",
    "constraint_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1858_CONSTRAINT_PACKAGE_STATUS.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1858_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1858_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1858_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1858_VALIDATION.csv",
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


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    source_rows = [
        {
            "source_id": "SRC1858_0_1857_handoff",
            "source_path": source_path("1857-Y5-R2FR-auxiliary-constraint-X-local-GR-route.md"),
            "needle": "NEXT1857_0_primary",
            "role": "selected parent constraint package target",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1858_1_first_class_contract",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1555_FIRST_CLASS_CONSTRAINT_CONTRACT.csv"),
            "needle": "FCC1555_7_no_GR_import",
            "role": "first-class constraint contract and no-GR-import guard",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1858_2_constraint_class",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1562_CONSTRAINT_CLASS_GATE.csv"),
            "needle": "CLASS1562_5_second_class",
            "role": "second-class auxiliary route condition",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1858_3_constraint_action_attempt",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1668_CONSTRAINT_FIRST_ACTION_ATTEMPT.csv"),
            "needle": "CFA1668_8_verdict",
            "role": "constraint-first action attempt verdict",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1858_4_overconstraint_guard",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1668_OVERCONSTRAINT_GUARD.csv"),
            "needle": "OCG1668_4_retrofit",
            "role": "guard against retrofitting a GR answer",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1858_5_descent_theorem_attempt",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1675_CONSTRAINT_FIRST_DESCENT_THEOREM_ATTEMPT.csv"),
            "needle": "constraint_first_DqZ_zero_descent_theorem",
            "role": "descent theorem clauses",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1858_6_exclusion_gate",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1783_CONSTRAINT_FIRST_EXCLUSION_GATE.csv"),
            "needle": "CFE1783_7_verdict",
            "role": "constraint-first exclusion theorem verdict",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1858_7_nonprop_constraint",
            "source_path": source_path("07-nonpropagating-reciprocity-constraint.md"),
            "needle": "best route = hard constraint or phase-volume balance",
            "role": "early nonpropagating reciprocity route",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1858_8_phase_volume",
            "source_path": source_path("08-phase-volume-reciprocity-origin.md"),
            "needle": "phase_volume_reciprocity_motivated_not_parent_derived",
            "role": "phase-volume origin status",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1858_9_hamiltonian_cell",
            "source_path": source_path("09-hamiltonian-radial-cell-derivation.md"),
            "needle": "hamiltonian_radial_cell_sharpened_not_parent_derived",
            "role": "Hamiltonian radial-cell derivation status",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1858_10_observer_contract",
            "source_path": source_path("10-observer-map-symplectic-contract.md"),
            "needle": "The acceptable parent routes are narrow",
            "role": "future parent action contract",
            "status": "FOUND",
            "valid_for_claim": False,
        },
    ]

    constraint_rows = [
        {
            "package_id": "PCP1858_0_parent_phase_space",
            "needed_object": "parent phase space and symplectic form",
            "acceptance_requirement": "declare fields, variations, symplectic current and boundary variables before local GR is taken as a reduced branch",
            "current_evidence": "1857/CGA1857_0 and 1555/FCC1555_0 keep this unsigned",
            "current_status": "NOT_PARENT_SIGNED",
            "blocks_local_gr_claim": True,
            "valid_for_claim": False,
        },
        {
            "package_id": "PCP1858_1_constraint_origin",
            "needed_object": "constraint equation C_X=0 or C_R=0",
            "acceptance_requirement": "derive the constraint from MTS motion-load, phase-volume, reciprocity, or parent Euler/Dirac equations without inserting the desired GR lock",
            "current_evidence": "07/08/09 motivate and sharpen the route, but do not derive the parent equation",
            "current_status": "PARENT_ORIGIN_MOTIVATED_NOT_DERIVED",
            "blocks_local_gr_claim": True,
            "valid_for_claim": False,
        },
        {
            "package_id": "PCP1858_2_generator_or_auxiliary_solve",
            "needed_object": "differentiable generator or algebraic auxiliary elimination",
            "acceptance_requirement": "either G_X is differentiable with proper boundary charge, or E_Lambda/E_X solve X algebraically before readout with no nonlocal tail",
            "current_evidence": "1562 marks second-class auxiliary as the better conditional route; 1668 says it is not signed",
            "current_status": "FORMAL_ROUTE_ONLY_NOT_SIGNED",
            "blocks_local_gr_claim": True,
            "valid_for_claim": False,
        },
        {
            "package_id": "PCP1858_3_bracket_degree_count",
            "needed_object": "bracket closure and degree count",
            "acceptance_requirement": "prove the constraint removes exactly the dangerous local residual pair rather than hiding a physical mode",
            "current_evidence": "1555/FCC1555_5 and 1562/CLASS1562_3 remain blocked",
            "current_status": "BRACKET_DEGREE_COUNT_BLOCKED",
            "blocks_local_gr_claim": True,
            "valid_for_claim": False,
        },
        {
            "package_id": "PCP1858_4_boundary_charge",
            "needed_object": "zero, exact, fixed, or retained boundary charge",
            "acceptance_requirement": "show local projection/boundary terms are silent or keep them as explicit finite residual rows",
            "current_evidence": "1555/FCC1555_3, 1562/CLASS1562_4, 1668/OCG1668_2 and 1675/CFD1675_5 remain unsigned",
            "current_status": "BOUNDARY_CHARGE_UNSIGNED",
            "blocks_local_gr_claim": True,
            "valid_for_claim": False,
        },
        {
            "package_id": "PCP1858_5_matter_readout_descent",
            "needed_object": "matter/source/readout descent",
            "acceptance_requirement": "prove clocks, photons, EM, PPN and orbital readouts depend only on reduced quotient variables after elimination",
            "current_evidence": "1675/CFD1675_4 and 1668/OCG1668_3 keep readout maps open",
            "current_status": "MISSING_MATTER_READOUT_DESCENT",
            "blocks_local_gr_claim": True,
            "valid_for_claim": False,
        },
        {
            "package_id": "PCP1858_6_physical_component_lock",
            "needed_object": "physical-component lock",
            "acceptance_requirement": "show the eliminated component is exactly the local c_g/X fifth-force direction and not a galaxy/cosmology/memory sector needed elsewhere",
            "current_evidence": "1783/CFE1783_7 and 1668/OCG1668_1 require component separation",
            "current_status": "COMPONENT_LOCK_UNSIGNED",
            "blocks_local_gr_claim": True,
            "valid_for_claim": False,
        },
        {
            "package_id": "PCP1858_7_no_GR_import_guard",
            "needed_object": "no-GR-import proof discipline",
            "acceptance_requirement": "do not use Schwarzschild AB=1, Einstein vacuum equations, or a GR-matched ansatz as a premise",
            "current_evidence": "1555/FCC1555_7 and 1668/OCG1668_4 explicitly enforce the guard",
            "current_status": "PASS_GUARD_NONCLAIM",
            "blocks_local_gr_claim": False,
            "valid_for_claim": False,
        },
        {
            "package_id": "PCP1858_8_verdict",
            "needed_object": "one parent branch satisfying all package clauses",
            "acceptance_requirement": "PCP1858_0 through PCP1858_7 close together from MTS primitives",
            "current_evidence": "parent-origin, generator/auxiliary, boundary, matter descent, degree count and component lock are not jointly signed",
            "current_status": "CONSTRAINT_PACKAGE_CONDITIONAL_NOT_CLOSED",
            "blocks_local_gr_claim": True,
            "valid_for_claim": False,
        },
    ]

    no_gr_rows = [
        {
            "gate_id": "NGI1858_0_forbidden_shortcut",
            "question": "Was GR imported as the premise?",
            "required_answer": "No Schwarzschild AB=1, Einstein vacuum equation, or fitted GR reciprocity may be used to derive the local branch.",
            "current_answer": "guard is explicit and active",
            "gate_status": "PASS_GUARD_NONCLAIM",
            "blocks_claim": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "NGI1858_1_parent_origin",
            "question": "Is the constraint parent-owned without the forbidden shortcut?",
            "required_answer": "C_X=0/C_R=0 must follow from MTS parent primitives before local GR is mentioned.",
            "current_answer": "not yet; phase-volume and Hamiltonian routes are motivational/sharpening only",
            "gate_status": "FAIL_CURRENT_CLAIM",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "NGI1858_2_phase_volume_status",
            "question": "Does phase-volume balance derive the constraint?",
            "required_answer": "derive the exact radial cell/reciprocity constraint, including multiplier ownership and allowed variations",
            "current_answer": "motivates the route but does not close it",
            "gate_status": "MOTIVATED_NOT_DERIVED",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "NGI1858_3_hamiltonian_status",
            "question": "Does Hamiltonian/mass-shell structure derive the radial cell?",
            "required_answer": "derive T sqrt(S)=1 or equivalent C_R=0 from local mass-shell/observer-map structure",
            "current_answer": "sharpens the missing theorem but does not prove it",
            "gate_status": "SHARPENED_NOT_DERIVED",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "NGI1858_4_verdict",
            "question": "Can local GR be claimed from the no-GR-import package now?",
            "required_answer": "yes only if the parent constraint package closes without forbidden GR premises",
            "current_answer": "no; the route remains live but conditional",
            "gate_status": "NO_GR_IMPORT_ACTIVE_BUT_PARENT_PACKAGE_OPEN",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
    ]

    origin_route_rows = [
        {
            "route_id": "ORG1858_0_magic_multiplier",
            "route": "insert S += int lambda_R R_AB or lambda_X X",
            "strength": "algebraically forces the wanted zero",
            "failure_mode": "magic multiplier unless lambda/constraint has a parent origin",
            "current_status": "REJECT_AS_DERIVATION",
            "next_action": "do not use as proof",
            "valid_for_claim": False,
        },
        {
            "route_id": "ORG1858_1_phase_volume",
            "route": "motion-load or phase-volume reciprocity derives the radial cell",
            "strength": "closest to the MTS primitive language",
            "failure_mode": "currently motivational; does not yet own multiplier, variations, or boundary",
            "current_status": "BEST_PRIMARY_TARGET",
            "next_action": "attempt exact parent-origin derivation in 1859",
            "valid_for_claim": False,
        },
        {
            "route_id": "ORG1858_2_hamiltonian_cell",
            "route": "local mass-shell/Hamiltonian radial cell derives T sqrt(S)=1",
            "strength": "turns reciprocity into a phase-cell theorem if it closes",
            "failure_mode": "generic Liouville/symplectic preservation does not by itself force p=1",
            "current_status": "SHARPENS_1859_TARGET",
            "next_action": "use as supporting clause for phase-volume proof",
            "valid_for_claim": False,
        },
        {
            "route_id": "ORG1858_3_first_class",
            "route": "momentum-map first-class constraint",
            "strength": "cleanest gauge/topological local-GR reduction if full algebra closes",
            "failure_mode": "parent Omega, differentiability, brackets, degree count and boundary are absent",
            "current_status": "HELD_UNTIL_PARENT_ORIGIN",
            "next_action": "return after parent constraint is real",
            "valid_for_claim": False,
        },
        {
            "route_id": "ORG1858_4_second_class_auxiliary",
            "route": "algebraic auxiliary elimination before readout",
            "strength": "less scrutiny than first-class gauge if no physical scalar is intended",
            "failure_mode": "requires no-derivative sort, local algebraic solve, matter descent and boundary control",
            "current_status": "BEST_FALLBACK_CONDITIONAL",
            "next_action": "keep as fallback if first-class proof is too expensive",
            "valid_for_claim": False,
        },
        {
            "route_id": "ORG1858_5_finite_bound_fallback",
            "route": "retain finite c_g/X residual and bound it empirically",
            "strength": "testable even if exact local-GR derivation fails",
            "failure_mode": "does not prove derived GR; needs source-backed coefficients and local arena projections",
            "current_status": "BACKSTOP_ONLY",
            "next_action": "do not promote while derivation route remains live",
            "valid_for_claim": False,
        },
    ]

    status_rows = [
        {
            "status_id": "CPS1858_0_route",
            "branch": "constraint/auxiliary local-GR route",
            "status": "LIVE_CONDITIONAL_ROUTE",
            "reason": "conditional theorem is clean, but parent package is not signed",
            "valid_for_claim": False,
        },
        {
            "status_id": "CPS1858_1_no_gr_import",
            "branch": "no-GR-import discipline",
            "status": "GUARD_ACTIVE",
            "reason": "forbidden GR shortcuts are explicitly rejected",
            "valid_for_claim": False,
        },
        {
            "status_id": "CPS1858_2_local_gr",
            "branch": "local GR/Newton reduction",
            "status": "NOT_CLAIMED",
            "reason": "parent-origin, boundary, matter descent, degree count and component lock remain unsigned",
            "valid_for_claim": False,
        },
        {
            "status_id": "CPS1858_3_derivation_target",
            "branch": "next derivation",
            "status": "MOTION_LOAD_PHASE_VOLUME_PARENT_ORIGIN_SELECTED",
            "reason": "this is the bottleneck upstream of generator/boundary/degree-count cleanup",
            "valid_for_claim": False,
        },
    ]

    claim_gate_rows = [
        {
            "gate_id": "CG1858_0_sources",
            "claim": "1858 source package is present",
            "gate_pass": True,
            "reason": "all local source paths and needles are recorded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1858_1_no_gr_import_guard",
            "claim": "forbidden GR shortcut is not used",
            "gate_pass": True,
            "reason": "AB=1/Einstein-vacuum premises are disallowed by the gate",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1858_2_parent_constraint_origin",
            "claim": "constraint is parent-derived",
            "gate_pass": False,
            "reason": "motion-load/phase-volume/Hamiltonian derivation is not closed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1858_3_full_constraint_package",
            "claim": "constraint package proves local scalar removal",
            "gate_pass": False,
            "reason": "generator/auxiliary solve, boundary, matter descent, degree count and component lock remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1858_4_local_GR_claim",
            "claim": "MTS derives local GR/Newton branch",
            "gate_pass": False,
            "reason": "not until CG1858_2 and CG1858_3 pass in one parent branch",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1858_0_not_demoted_yet",
            "decision": "keep the constraint/auxiliary route alive, but nonclaim",
            "because": "the conditional theorem is mathematically clean and avoids physical scalar hair, but the parent package is unsigned",
            "next_action": "attack parent-origin directly before spending time on empirical local-GR claims",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1858_1_primary_bottleneck",
            "decision": "prioritize motion-load/phase-volume parent origin",
            "because": "generator, boundary and degree-count work is premature if C_X=0 is still inserted by hand",
            "next_action": "derive or reject the exact parent law that yields C_X=0/C_R=0 without importing GR",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1858_2_claim_discipline",
            "decision": "no R10, WEP, PPN, clock, orbital or local-GR pass is allowed from 1858",
            "because": "1858 is a proof-gate and source discipline checkpoint only",
            "next_action": "keep finite-bound files and empirical tests as backstops, not proof substitutes",
            "valid_for_claim": False,
        },
    ]

    next_rows = [
        {
            "route_id": "NEXT1858_0_primary",
            "next_target": "1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation.md",
            "script": "scripts/Y5_R2FR_motion_load_phase_volume_parent_origin_no_GR_import_derivation_1859.py",
            "objective": "derive or reject the parent motion-load/phase-volume law that yields the nonpropagating local reciprocity constraint without importing GR",
            "selection_status": "selected",
            "success_condition": "C_X=0/C_R=0 follows from MTS primitives with allowed variations, multiplier ownership and no forbidden GR premise",
        },
        {
            "route_id": "NEXT1858_1_secondary",
            "next_target": "1859b-Y5-R2FR-constraint-generator-boundary-degree-count.md",
            "script": "scripts/Y5_R2FR_constraint_generator_boundary_degree_count_1859b.py",
            "objective": "prove differentiability, bracket closure, boundary silence and degree count after parent origin is signed",
            "selection_status": "held",
            "success_condition": "generator/auxiliary package closes for the parent-owned constraint",
        },
        {
            "route_id": "NEXT1858_2_backstop",
            "next_target": "1859c-Y5-R2FR-finite-cg-local-bound-backstop.md",
            "script": "scripts/Y5_R2FR_finite_cg_local_bound_backstop_1859c.py",
            "objective": "if derivation fails, source finite local residual coefficients and compare against R10/PPN/clock/orbital bounds",
            "selection_status": "backstop",
            "success_condition": "all local residual rows are source-backed and remain nonclaim unless numerically bounded",
        },
    ]

    return {
        "source_register": source_rows,
        "constraint_package": constraint_rows,
        "no_gr_import": no_gr_rows,
        "origin_routes": origin_route_rows,
        "constraint_status": status_rows,
        "claim_gate": claim_gate_rows,
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
        shutil.copy2(src, RAB_QUEUE / f"JR1858_{src.name}")


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
    return not malformed, "malformed: " + "; ".join(malformed) if malformed else "all generated 1858 CSVs parse"


def check_branch_copies() -> tuple[bool, str]:
    missing: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        expected = [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1858_{path.name}",
        ]
        for item in expected:
            if not item.exists():
                missing.append(str(item))
    return not missing, "missing copies: " + "; ".join(missing) if missing else "branch/quarantine/queue copies exist"


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    ok, detail = check_sources(rows_map["source_register"])
    checks.append(("VAL1858_0_sources_exist", ok, detail))
    ok, detail = check_needles(rows_map["source_register"])
    checks.append(("VAL1858_1_needles_present", ok, detail))
    checks.append(
        (
            "VAL1858_2_package_verdict_blocks",
            any(
                row["package_id"] == "PCP1858_8_verdict"
                and row["current_status"] == "CONSTRAINT_PACKAGE_CONDITIONAL_NOT_CLOSED"
                and boolish(row["blocks_local_gr_claim"])
                for row in rows_map["constraint_package"]
            ),
            "constraint package verdict remains nonclaim",
        )
    )
    checks.append(
        (
            "VAL1858_3_no_gr_import_guard",
            any(row["gate_id"] == "NGI1858_0_forbidden_shortcut" and row["gate_status"] == "PASS_GUARD_NONCLAIM" for row in rows_map["no_gr_import"])
            and any(row["gate_id"] == "NGI1858_1_parent_origin" and row["gate_status"] == "FAIL_CURRENT_CLAIM" for row in rows_map["no_gr_import"]),
            "GR shortcut guard passes but parent-origin gate fails current claim",
        )
    )
    checks.append(
        (
            "VAL1858_4_origin_route_selected",
            any(row["route_id"] == "ORG1858_1_phase_volume" and row["current_status"] == "BEST_PRIMARY_TARGET" for row in rows_map["origin_routes"]),
            "motion-load/phase-volume parent-origin route selected",
        )
    )
    checks.append(
        (
            "VAL1858_5_local_gr_nonclaim",
            any(row["status_id"] == "CPS1858_2_local_gr" and row["status"] == "NOT_CLAIMED" for row in rows_map["constraint_status"]),
            "local GR/Newton reduction is not claimed",
        )
    )
    checks.append(
        (
            "VAL1858_6_claim_gates_safe",
            any(row["gate_id"] == "CG1858_1_no_gr_import_guard" and boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and any(row["gate_id"] == "CG1858_4_local_GR_claim" and not boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and all(not boolish(row["claim_allowed"]) for row in rows_map["claim_gate"]),
            "no claim gate allows local-GR promotion",
        )
    )
    checks.append(
        (
            "VAL1858_7_next_target_selected",
            any(row["route_id"] == "NEXT1858_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "1859 parent-origin target selected",
        )
    )
    checks.append(
        (
            "VAL1858_8_no_claim_flags",
            all(not boolish(row.get("valid_for_claim", False)) for rows in rows_map.values() for row in rows),
            "no valid_for_claim flags are true",
        )
    )
    ok, detail = check_csv_parse()
    checks.append(("VAL1858_9_csv_parse", ok, detail))
    ok, detail = check_branch_copies()
    checks.append(("VAL1858_10_branch_copies", ok, detail))
    pycache_path = ROOT / "scripts" / "__pycache__"
    checks.append(("VAL1858_11_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"))
    formalization_outputs: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in [
            "*P8_Y5*1858*",
            "*1858-Y5-R2FR-parent-constraint-package-no-GR-import-gate*",
            "*Y5_R2FR_parent_constraint_package_no_GR_import_gate_1858.py",
        ]:
            formalization_outputs.extend(FORMALIZATION.rglob(pattern))
    formalization_detail = (
        "found generated outputs: " + "; ".join(str(path) for path in formalization_outputs)
        if formalization_outputs
        else "no generated 1858 outputs found under formalization-workbench"
    )
    checks.append(("VAL1858_12_formalization_untouched", not formalization_outputs, formalization_detail))
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
            "check_id": "VAL1858_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1858 parent constraint package no-GR-import gate",
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
            "# 1858: Parent Constraint Package No-GR-Import Gate",
            "",
            "**Current verdict:** the local-GR route remains alive, but only as a conditional constraint/auxiliary route. The no-GR-import discipline is clean: do not smuggle in Schwarzschild AB=1, Einstein vacuum equations, or a GR-matched ansatz as the proof. The missing move is upstream: derive the nonpropagating local constraint from MTS motion-load/phase-volume/reciprocity primitives, or demote this local transition to closure-only.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_path", "needle", "role", "status", "valid_for_claim"]),
            "",
            "## Parent Constraint Package Audit",
            markdown_table(rows_map["constraint_package"], ["package_id", "needed_object", "acceptance_requirement", "current_status", "blocks_local_gr_claim", "valid_for_claim"]),
            "",
            "## No-GR-Import Gate",
            markdown_table(rows_map["no_gr_import"], ["gate_id", "question", "required_answer", "current_answer", "gate_status", "blocks_claim", "valid_for_claim"]),
            "",
            "## Origin Route Audit",
            markdown_table(rows_map["origin_routes"], ["route_id", "route", "strength", "failure_mode", "current_status", "next_action", "valid_for_claim"]),
            "",
            "## Constraint Package Status",
            markdown_table(rows_map["constraint_status"], ["status_id", "branch", "status", "reason", "valid_for_claim"]),
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
            "This checkpoint does not kill the route. It sharpens it. The problem is not that local GR is impossible in this branch; the problem is that the current corpus has not yet earned the parent constraint. The next honest attack is to derive, from MTS primitives alone, why the local reciprocity/radial-cell constraint is nonpropagating before matter readout. If that fails, this route becomes an explicit closure assumption and the project falls back to finite residual bounds.",
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
    print(f"1858 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
