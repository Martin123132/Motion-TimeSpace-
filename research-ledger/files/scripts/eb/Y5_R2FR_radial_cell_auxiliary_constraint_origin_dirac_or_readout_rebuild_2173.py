from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2173"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2173-Y5-R2FR-radial-cell-auxiliary-constraint-origin-dirac-or-readout-rebuild.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2173_SOURCE_REGISTER.csv",
    "auxiliary_audit": OUT / "P8_Y5_PARENT_QLOC_2173_AUXILIARY_CONSTRAINT_AUDIT.csv",
    "dirac_chain": OUT / "P8_Y5_PARENT_QLOC_2173_DIRAC_CHAIN_LEDGER.csv",
    "bracket_contract": OUT / "P8_Y5_PARENT_QLOC_2173_HCORE_BRACKET_CONTRACT.csv",
    "readout_rebuild": OUT / "P8_Y5_PARENT_QLOC_2173_READOUT_REBUILD_OR_CLOSURE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2173_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2173_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2173_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2173_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2173_HCORE_BRACKET_CONTRACT_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2173_AUXILIARY_DIRAC_LEDGER_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "AUXILIARY_CONSTRAINT_ORIGIN_2173_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


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
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2173_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2173-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2173*",
        "*P8_Y5_BRR545_2173*",
        "*Y5_R2FR_radial_cell_auxiliary_constraint_origin_dirac_or_readout_rebuild_2173*",
        "*JR2173*",
        "*AUXILIARY_CONSTRAINT_ORIGIN_2173*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2172_handoff",
            ROOT / "2172-Y5-R2FR-radial-cell-vertical-gauge-noether-identity-or-coefficient-basis.md",
            ["NEXT2172_0_2173", "AUXILIARY_CONSTRAINT_OR_READOUT_REBUILD_NEXT"],
            "2172 rejects current-readout vertical gauge and selects auxiliary constraint/readout rebuild.",
        ),
        (
            "2172_validation",
            OUT / "P8_Y5_BRR545_2172_VALIDATION.csv",
            ["VAL2172_OVERALL,PASS"],
            "2172 validation passed.",
        ),
        (
            "1248_lambda_ansatz",
            ROOT / "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md",
            ["minimal `lambda_R C_R` parent-action ansatz", "H_core and canonical brackets for T,S are not supplied"],
            "1248 supplies the earlier minimal lambda ansatz and its Dirac blockers.",
        ),
        (
            "07_nonprop_constraint",
            ROOT / "07-nonpropagating-reciprocity-constraint.md",
            ["S_constraint = integral lambda_R R_AB", "constraint parent origin"],
            "07 supplies the algebraic hard-constraint idea and says parent origin is open.",
        ),
        (
            "1576_constraint_no_pole",
            ROOT / "1576-Y5-RAB-constraint-no-pole-or-quotient-map-construction.md",
            ["constraint route is still only motivated", "lambda_R"],
            "1576 refuses the no-pole/constraint route as derived.",
        ),
        (
            "1873_boundary_contract",
            ROOT / "1873-Y5-R2FR-boundary-silence-parent-contract-for-CR-zero-or-residual-closure.md",
            ["BOUNDARY_SILENCE_PARENT_CONTRACT_EXACTLY_STATED", "CURRENT_LOCAL_CR_ZERO_ROUTE_DEMOTED_TO_RESIDUAL_CLOSURE"],
            "1873 gives the matter/boundary/readout clauses needed after any C_R constraint.",
        ),
        (
            "2168_category_constraint",
            ROOT / "2168-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md",
            ["Lambda_R C_R route", "AUXILIARY_ORIGIN_UNSIGNED"],
            "2168 keeps the Lambda_R route exact but unsigned.",
        ),
    ]
    rows = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def auxiliary_audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "AUX2173_0_action_form",
            "minimal constrained action",
            "S_min = integral sqrt(-g)[L_MTS_core + Lambda_R C_R + L_matter]",
            "FORMAL_ACTION_TEMPLATE_EXISTS",
            "delta_Lambda_R gives C_R=0 inside the template",
        ),
        (
            "AUX2173_1_origin",
            "multiplier origin",
            "Lambda_R is forced by parent motion/time/space principles rather than inserted to close the branch",
            "MISSING_PARENT_ORIGIN",
            "without this, Lambda_R C_R is a closure axiom",
        ),
        (
            "AUX2173_2_no_kinetic_permission",
            "operator exclusion",
            "parent grammar forbids kinetic/potential R_AB terms alongside the hard constraint",
            "MISSING_OPERATOR_EXCLUSION",
            "otherwise finite Z_R/M_R^2 countermodels coexist with the ansatz",
        ),
        (
            "AUX2173_3_matter_descent",
            "matter/source descent",
            "ordinary matter couples only to terminal public coframe/readout and has no C_R/source-weight slot",
            "MISSING_MATTER_DESCENT",
            "otherwise J_R, w_R and beta_source remain live",
        ),
        (
            "AUX2173_4_boundary_silence",
            "boundary/corner silence",
            "admissible boundary terms carry no reciprocal C_R/Pi_R/Q_R charge after constraint",
            "MISSING_BOUNDARY_NO_CHARGE",
            "otherwise exterior reciprocal hair can reappear",
        ),
        (
            "AUX2173_5_readout_silence",
            "readout after constraint",
            "coframe, clocks, tau, endpoints and source support do not reinsert C_R after C_R=0",
            "MISSING_READOUT_TAU_DESCENT",
            "otherwise common-frame/local residual rows remain live",
        ),
        (
            "AUX2173_6_verdict",
            "parent-owned auxiliary constraint",
            "current corpus derives Lambda_R C_R as a necessary parent constraint with preserved local GR reduction",
            "NOT_DERIVED_CURRENT_CORPUS",
            "formal ansatz is useful, but still closure-only until H_core/brackets/descent close",
        ),
    ]
    return [
        base_row(
            audit_id=audit_id,
            clause=clause,
            required_statement=required_statement,
            status=status,
            implication=implication,
        )
        for audit_id, clause, required_statement, status, implication in specs
    ]


def dirac_chain_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DIR2173_0_primary",
            "primary constraint",
            "pi_Lambda ≈ 0 because Lambda_R has no time derivative in the ansatz",
            "FORMAL_PASS_WITHIN_ANSATZ",
            "valid only after the ansatz is accepted",
        ),
        (
            "DIR2173_1_secondary",
            "secondary constraint",
            "dot(pi_Lambda) = -delta H/delta Lambda_R = -C_R ≈ 0",
            "FORMAL_PASS_WITHIN_ANSATZ",
            "this is the desired C_R=0 step but not yet a parent theorem",
        ),
        (
            "DIR2173_2_preservation",
            "secondary preservation",
            "dot(C_R) = {C_R,H_core} + Lambda_R{C_R,C_R}; since {C_R,C_R}=0, need {C_R,H_core}≈0 or controlled tertiary chain",
            "BLOCKED_HCORE_BRACKET_MISSING",
            "Lambda_R does not by itself preserve the constraint",
        ),
        (
            "DIR2173_3_constraint_class",
            "constraint class and DOF count",
            "classify pi_Lambda, C_R, any tertiary constraints, and their brackets with Hamiltonian/momentum constraints",
            "BLOCKED_CANONICAL_ALGEBRA_MISSING",
            "cannot know if the branch removes a mode consistently or overconstrains it",
        ),
        (
            "DIR2173_4_boundary",
            "differentiability and boundary charge",
            "H_core+Lambda_R C_R must be differentiable on the chosen worldtube/domain and have no reciprocal boundary charge",
            "BLOCKED_BOUNDARY_CLASS_MISSING",
            "Q_R can reappear even if bulk C_R=0 is formal",
        ),
        (
            "DIR2173_5_matter",
            "matter compatibility",
            "matter Hamiltonian and source normalization preserve C_R=0 and do not generate J_R/w_R/beta_source terms",
            "BLOCKED_MATTER_SOURCE_DESCENT_MISSING",
            "local GR still fails if source coupling leaks",
        ),
        (
            "DIR2173_6_result",
            "Dirac theorem status",
            "full auxiliary constraint chain closes from parent action",
            "DIRAC_THEOREM_NOT_CLOSED_CURRENT_CORPUS",
            "need H_core/bracket closure next, not more Lambda_R notation",
        ),
    ]
    return [
        base_row(
            dirac_id=dirac_id,
            step=step,
            statement=statement,
            status=status,
            implication=implication,
        )
        for dirac_id, step, statement, status, implication in specs
    ]


def bracket_contract_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "HBC2173_0_variables",
            "canonical variable declaration",
            "declare canonical coordinates/momenta for T,S or u=ln(T sqrt(S)), public coframe, connection/load fields and Lambda_R",
            "MISSING_CANONICAL_VARIABLES",
            "needed before any bracket claim",
        ),
        (
            "HBC2173_1_C_definition",
            "constraint target",
            "C_R=ln(T^2 S)=2u with explicit functional derivative on phase space",
            "EXACT_DEFINITION_BUT_NEEDS_PHASE_SPACE",
            "target is clear, phase-space embedding is not",
        ),
        (
            "HBC2173_2_Hcore",
            "parent core Hamiltonian",
            "H_core[T,S,e_pub,theta,chi_load,pi_*] is supplied from MTS primitives without importing GR exterior",
            "MISSING_HCORE",
            "the main blocker from 1248 remains live",
        ),
        (
            "HBC2173_3_tangency",
            "constraint-surface tangency",
            "{C_R,H_core}|_{C_R=0}=0 or produces a controlled tertiary constraint with closed algebra",
            "MISSING_BRACKET_CLOSURE",
            "this is the exact mathematical condition for preservation",
        ),
        (
            "HBC2173_4_operator_exclusion",
            "no finite residual operator re-entry",
            "H_core contains no independent Z_R, M_R^2, J_R, Q_R, b_R, w_R or beta_source channel after imposing C_R",
            "MISSING_NO_REENTRY_THEOREM",
            "otherwise local GR is not a theorem but a constrained-plus-residual theory",
        ),
        (
            "HBC2173_5_boundary",
            "differentiable generator",
            "Hamiltonian variation has admissible boundary term with no reciprocal charge and no hidden corner source",
            "MISSING_BOUNDARY_DIFFERENTIABILITY",
            "needed for Q_R=0 beyond the bulk equation",
        ),
        (
            "HBC2173_6_success",
            "auxiliary theorem success criterion",
            "HBC2173_0 through HBC2173_5 close in one parent action/source package",
            "NOT_SATISFIED_CURRENT_CORPUS",
            "select 2174 H_core/bracket closure attempt",
        ),
    ]
    return [
        base_row(
            contract_id=contract_id,
            requirement=requirement,
            required_statement=required_statement,
            status=status,
            implication=implication,
        )
        for contract_id, requirement, required_statement, status, implication in specs
    ]


def readout_rebuild_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "RR2173_0_current_readout",
            "current coframe readout",
            "theta_0=T cdt and theta_1=sqrt(S)dr see C_R through x+y",
            "VISIBLE_CURRENT_READOUT",
            "2172 obstruction applies",
        ),
        (
            "RR2173_1_rebuild_option",
            "new Q_vis/E readout functor",
            "observed clocks/rulers depend on a parent Q_vis that excludes or quotient-removes C_R before readout",
            "POSSIBLE_ONLY_IF_PARENT_OWNED",
            "would need a replacement observer contract, not a post-hoc deletion",
        ),
        (
            "RR2173_2_rebuild_cost",
            "empirical continuity cost",
            "new readout must still recover Newtonian potential, PPN gamma/beta, clocks, orbits and source mass conventions",
            "HIGH_SCRUTINY_ROUTE",
            "readout rebuild may solve C_R but can break existing empirical pillars",
        ),
        (
            "RR2173_3_current_selection",
            "route priority",
            "try H_core/Dirac preservation before readout rebuild because current readout already matches the live local observables",
            "HCORE_FIRST_SELECTED",
            "readout rebuild held as fallback if H_core fails cleanly",
        ),
    ]
    return [
        base_row(
            rebuild_id=rebuild_id,
            route=route,
            statement=statement,
            status=status,
            implication=implication,
        )
        for rebuild_id, route, statement, status, implication in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2173_0_formal_gain", "PRIMARY_SECONDARY_FORMAL_PASS_RETAINED", "Lambda_R C_R formally gives pi_Lambda≈0 and C_R≈0 inside the ansatz", "selected"),
        ("DEC2173_1_no_claim", "AUXILIARY_ROUTE_NOT_PARENT_DERIVED", "origin, H_core preservation, constraint class, matter descent and boundary silence are still unsigned", "selected"),
        ("DEC2173_2_key_equation", "PRESERVATION_REQUIRES_HCORE_TANGENCY", "because {C_R,C_R}=0, Lambda_R does not preserve C_R; need {C_R,H_core}≈0 or closed tertiary algebra", "selected"),
        ("DEC2173_3_readout", "READOUT_REBUILD_HELD_SECOND", "readout rebuild is possible only with a new parent observer contract and high empirical continuity burden", "held"),
        ("DEC2173_4_next", "HCORE_BRACKET_CLOSURE_NEXT", "the least-circular next move is to write/test the minimal H_core/canonical bracket skeleton", "selected"),
    ]
    return [
        base_row(
            decision_id=decision_id,
            decision=decision,
            rationale=rationale,
            selection_status=status,
        )
        for decision_id, decision, rationale, status in specs
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2173_0_2174",
            selection_status="selected",
            target_file="2174-Y5-R2FR-Hcore-canonical-bracket-closure-or-auxiliary-route-demotion.md",
            target_script="scripts/Y5_R2FR_Hcore_canonical_bracket_closure_or_auxiliary_route_demotion_2174.py",
            objective="construct the minimal parent H_core/canonical bracket skeleton for T,S/u, coframe, load and Lambda_R, then test whether {C_R,H_core}≈0 closes without GR import",
            success_condition="constraint preservation, class/DOF count, boundary differentiability and matter/source descent close, or auxiliary route is explicitly demoted to closure-only",
            do_not_do="do not treat Lambda_R insertion as origin, do not skip H_core, do not use GR exterior or readout rebuild as a hidden shortcut",
        ),
        base_row(
            route_id="NEXT2173_1_readout_fallback",
            selection_status="held_fallback",
            target_file="2174b-Y5-R2FR-parent-readout-functor-rebuild-or-current-readout-lock.md",
            target_script="scripts/Y5_R2FR_parent_readout_functor_rebuild_or_current_readout_lock_2174b.py",
            objective="if H_core fails, test whether a parent-owned Q_vis/E readout rebuild can remove C_R while preserving empirical local observables",
            success_condition="new readout contract recovers clocks, PPN, Newtonian source mass and orbital observables, or current readout is locked and finite rows become primary",
            do_not_do="do not erase C_R from readout after using T and sqrt(S) in the observable map",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["bracket_contract"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["dirac_chain"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["decision"], BRANCH_COPIES["source_weight"]),
    ]
    rows = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
            if str(row.get("valid_for_claim", "")).lower() == "true":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    source_rows = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2173_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2173_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    aux_statuses = {row["status"] for row in rows_by_name["auxiliary_audit"]}
    validations.append(base_row(validation_id="VAL2173_02_auxiliary_not_claimed", status="PASS" if "NOT_DERIVED_CURRENT_CORPUS" in aux_statuses and "FORMAL_ACTION_TEMPLATE_EXISTS" in aux_statuses else "FAIL", detail="formal action template retained but parent theorem not claimed"))

    dirac_statuses = {row["status"] for row in rows_by_name["dirac_chain"]}
    validations.append(base_row(validation_id="VAL2173_03_dirac_chain", status="PASS" if "BLOCKED_HCORE_BRACKET_MISSING" in dirac_statuses and "DIRAC_THEOREM_NOT_CLOSED_CURRENT_CORPUS" in dirac_statuses else "FAIL", detail="primary/secondary pass; preservation/class/boundary/matter blocked"))

    bracket_text = " ".join(str(row.get("required_statement", "")) + " " + str(row.get("status", "")) for row in rows_by_name["bracket_contract"])
    validations.append(base_row(validation_id="VAL2173_04_bracket_contract", status="PASS" if "{C_R,H_core}|_{C_R=0}=0" in bracket_text and "MISSING_HCORE" in bracket_text else "FAIL", detail="H_core tangency contract is explicit"))

    readout_statuses = {row["status"] for row in rows_by_name["readout_rebuild"]}
    validations.append(base_row(validation_id="VAL2173_05_readout_rebuild_held", status="PASS" if "HCORE_FIRST_SELECTED" in readout_statuses else "FAIL", detail="readout rebuild is held behind H_core attempt"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2173_06_decision", status="PASS" if "HCORE_BRACKET_CLOSURE_NEXT" in decision_text else "FAIL", detail="decision selects H_core bracket closure next"))

    validations.append(base_row(validation_id="VAL2173_07_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2174" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2174 Hcore bracket closure target selected"))

    validations.append(base_row(validation_id="VAL2173_08_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2173_09_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2173_10_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2173_artifacts()
    validations.append(base_row(validation_id="VAL2173_11_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2173 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2173_12_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2173_OVERALL", status="PASS" if overall else "FAIL", detail="2173 keeps Lambda_R C_R as formal ansatz only and selects H_core bracket closure as the next derivation test"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2173 - Y5/R2FR Radial-Cell Auxiliary Constraint Origin, Dirac Preservation, Or Readout Rebuild

## Current Verdict

2173 does **not** derive local GR/Newton and does **not** accept `Lambda_R C_R` as a parent theorem.

It preserves the useful part: inside the minimal constrained ansatz, `pi_Lambda≈0` and `C_R≈0` are formal primary/secondary Dirac steps. But that is still not enough.

The decisive equation is:

`dot(C_R) = {{C_R,H_core}} + Lambda_R {{C_R,C_R}}`.

Because `{{C_R,C_R}}=0`, the multiplier does **not** preserve the constraint for free. Preservation requires:

`{{C_R,H_core}} |_(C_R=0) = 0`

or a controlled tertiary constraint chain with closed algebra, boundary differentiability, matter descent and readout silence.

That means the next real derivation target is not another `Lambda_R` notation pass. It is the missing `H_core`/canonical bracket closure.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## Auxiliary Constraint Audit

{md_table(rows_by_name["auxiliary_audit"], ["audit_id", "clause", "required_statement", "status", "implication", "valid_for_claim"])}

## Dirac Chain Ledger

{md_table(rows_by_name["dirac_chain"], ["dirac_id", "step", "statement", "status", "implication", "valid_for_claim"])}

## H_core Bracket Contract

{md_table(rows_by_name["bracket_contract"], ["contract_id", "requirement", "required_statement", "status", "implication", "valid_for_claim"])}

## Readout Rebuild Or Closure

{md_table(rows_by_name["readout_rebuild"], ["rebuild_id", "route", "statement", "status", "implication", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Working Interpretation

The auxiliary route is still alive, but only as a precise theorem target. The ansatz gives the right shape, yet the parent theory must now earn it by supplying `H_core`, canonical variables, bracket closure, boundary differentiability and matter/source descent.

If `H_core` is tangent to the `C_R=0` surface, the local branch becomes much more serious. If it is not, then `Lambda_R C_R` is closure-only and the project should stop trying to smuggle local GR through it.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "auxiliary_audit": auxiliary_audit_rows(),
        "dirac_chain": dirac_chain_rows(),
        "bracket_contract": bracket_contract_rows(),
        "readout_rebuild": readout_rebuild_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in ["source_register", "auxiliary_audit", "dirac_chain", "bracket_contract", "readout_rebuild", "decision", "next_target"]:
        write_csv(OUTPUTS[name], rows_by_name[name])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()
