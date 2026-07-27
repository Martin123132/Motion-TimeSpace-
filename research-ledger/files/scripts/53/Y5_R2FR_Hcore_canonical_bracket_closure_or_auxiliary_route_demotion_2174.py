from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2174"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2174-Y5-R2FR-Hcore-canonical-bracket-closure-or-auxiliary-route-demotion.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2174_SOURCE_REGISTER.csv",
    "canonical_skeleton": OUT / "P8_Y5_PARENT_QLOC_2174_CANONICAL_U_SECTOR_SKELETON.csv",
    "dirac_flow": OUT / "P8_Y5_PARENT_QLOC_2174_DIRAC_FLOW_CASES.csv",
    "closure_conditions": OUT / "P8_Y5_PARENT_QLOC_2174_CLOSURE_CONDITIONS.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2174_HCORE_COUNTERMODEL_LEDGER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2174_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2174_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2174_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2174_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2174_CANONICAL_U_SECTOR_CONDITIONS_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2174_DIRAC_FLOW_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "HCORE_U_SECTOR_SOURCE_FREE_CONDITIONS_2174_NONCLAIM.csv",
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


def formalization_has_2174_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2174-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2174*",
        "*P8_Y5_BRR545_2174*",
        "*Y5_R2FR_Hcore_canonical_bracket_closure_or_auxiliary_route_demotion_2174*",
        "*JR2174*",
        "*HCORE_U_SECTOR_SOURCE_FREE_CONDITIONS_2174*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2173_handoff",
            ROOT / "2173-Y5-R2FR-radial-cell-auxiliary-constraint-origin-dirac-or-readout-rebuild.md",
            ["NEXT2173_0_2174", "PRESERVATION_REQUIRES_HCORE_TANGENCY"],
            "2173 selects H_core/canonical bracket closure.",
        ),
        (
            "2173_validation",
            OUT / "P8_Y5_BRR545_2173_VALIDATION.csv",
            ["VAL2173_OVERALL,PASS"],
            "2173 validation passed.",
        ),
        (
            "1248_ansatz",
            ROOT / "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md",
            ["DIR1248_2_preservation", "H_core and canonical brackets for T,S are not supplied"],
            "1248 gives the precise missing H_core/bracket blocker.",
        ),
        (
            "2172_obstruction",
            ROOT / "2172-Y5-R2FR-radial-cell-vertical-gauge-noether-identity-or-coefficient-basis.md",
            ["NO_NONTRIVIAL_VERTICAL_GENERATOR_CURRENT_READOUT", "AUXILIARY_CONSTRAINT_OR_READOUT_REBUILD_NEXT"],
            "2172 rules out current-readout vertical gauge, motivating auxiliary closure.",
        ),
        (
            "1873_contract",
            ROOT / "1873-Y5-R2FR-boundary-silence-parent-contract-for-CR-zero-or-residual-closure.md",
            ["UNSIGNED_MATTER_DESCENT", "UNSIGNED_BOUNDARY_SILENCE"],
            "1873 supplies matter/boundary/readout clauses still required after bracket closure.",
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


def canonical_skeleton_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CUS2174_0_u_definition",
            "radial-cell coordinate",
            "u := ln(T sqrt(S)) = C_R/2",
            "EXACT_DEFINITION",
            "turns the reciprocal constraint into u≈0",
        ),
        (
            "CUS2174_1_canonical_pair",
            "canonical pair",
            "{u(x),p_u(y)} = delta(x-y)",
            "CANONICAL_SKELETON_ASSUMPTION",
            "not yet parent-derived; used to expose the required closure conditions",
        ),
        (
            "CUS2174_2_constraint_term",
            "auxiliary constraint",
            "H_constraint = integral 2 Lambda_R u",
            "FORMAL_TEMPLATE",
            "pi_Lambda≈0 and u≈0 follow inside the template",
        ),
        (
            "CUS2174_3_core_expansion",
            "minimal local H_core expansion",
            "H_core = H_vis + 1/2 A_u^{-1} p_u^2 + 1/2 K_u u^2 + I_u p_u + J_u u + higher",
            "SKELETON_NOT_PARENT_SIGNED",
            "I_u and J_u are the dangerous source/readout/momentum leakage channels",
        ),
        (
            "CUS2174_4_no_claim",
            "parent status",
            "the current corpus does not derive A_u,K_u,I_u,J_u or H_vis from a parent action",
            "MISSING_PARENT_HCORE",
            "skeleton is a theorem target, not evidence",
        ),
    ]
    return [
        base_row(
            skeleton_id=skeleton_id,
            object=object_name,
            statement=statement,
            status=status,
            implication=implication,
        )
        for skeleton_id, object_name, statement, status, implication in specs
    ]


def dirac_flow_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DF2174_0_primary",
            "pi_Lambda≈0",
            "primary constraint from no Lambda_R velocity",
            "FORMAL_PASS_IN_TEMPLATE",
            "same formal gain as 1248",
        ),
        (
            "DF2174_1_secondary",
            "u≈0",
            "dot(pi_Lambda)=-2u≈0",
            "FORMAL_PASS_IN_TEMPLATE",
            "equivalent to C_R=0",
        ),
        (
            "DF2174_2_tertiary",
            "p_u + A_u I_u≈0",
            "dot(u)=delta H_core/delta p_u=A_u^{-1}p_u+I_u+...≈0",
            "CONTROLLED_TERTIARY_IF_AU_NONZERO",
            "the mode can be eliminated as second-class only if I_u is zero or source-owned",
        ),
        (
            "DF2174_3_multiplier",
            "Lambda_R fixed by p_u preservation",
            "dot(p_u)=-delta H_core/delta u-2 Lambda_R≈0 fixes Lambda_R up to source terms",
            "FORMAL_CLOSURE_IF_SOURCE_TERMS_CONTROLLED",
            "J_u or readout/boundary terms can make Lambda_R reaction physical",
        ),
        (
            "DF2174_4_second_class",
            "u,p_u removal",
            "u≈0 and p_u≈0 form a controlled second-class elimination in the clean I_u=J_u=0 branch",
            "EXACT_CONDITIONAL",
            "this is the first non-handwave auxiliary closure pattern",
        ),
        (
            "DF2174_5_status",
            "current theorem status",
            "current MTS parent derives the clean I_u=J_u=0 H_core branch",
            "NOT_DERIVED_CURRENT_CORPUS",
            "next proof must target source-free/even u-sector ownership",
        ),
    ]
    return [
        base_row(
            flow_id=flow_id,
            constraint=constraint,
            calculation=calculation,
            status=status,
            implication=implication,
        )
        for flow_id, constraint, calculation, status, implication in specs
    ]


def closure_condition_rows() -> list[dict[str, Any]]:
    specs = [
        ("CC2174_0_Au", "A_u", "nonzero finite kinetic inverse or declared degenerate alternative", "MISSING_PARENT_VALUE_OR_DEGENERATE_CASE", "needed for controlled p_u tertiary or tangent core"),
        ("CC2174_1_Iu", "I_u", "linear p_u/motion-load leakage vanishes or is source-backed and projected", "MISSING_ZERO_THEOREM", "I_u shifts p_u and can reintroduce a hidden flow channel"),
        ("CC2174_2_Ju", "J_u", "linear u source/readout/matter coupling vanishes or Lambda_R reaction is proven invisible", "MISSING_NO_SOURCE_THEOREM", "J_u is the direct active-source leak"),
        ("CC2174_3_boundary", "boundary class", "Hamiltonian is differentiable and no reciprocal boundary charge survives on u=p_u=0", "MISSING_BOUNDARY_DIFFERENTIABILITY", "needed for Q_R=0"),
        ("CC2174_4_matter", "matter descent", "ordinary matter and source normalization do not depend on u or Lambda_R reaction", "MISSING_MATTER_DESCENT", "needed for WEP/PPN/beta/source safety"),
        ("CC2174_5_readout", "readout/tau endpoints", "coframe, clocks, tau, endpoints and support maps are silent after u=0", "MISSING_READOUT_TAU_SILENCE", "needed for local observables"),
        ("CC2174_6_success", "clean auxiliary closure", "A_u branch closes and I_u=J_u=boundary=matter=readout leaks vanish", "NOT_SATISFIED_CURRENT_CORPUS", "conditional pattern ready, theorem not claimed"),
    ]
    return [
        base_row(
            condition_id=condition_id,
            symbol=symbol,
            required_statement=required_statement,
            status=status,
            implication=implication,
        )
        for condition_id, symbol, required_statement, status, implication in specs
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "HCM2174_0_linear_pu",
            "I_u p_u term",
            "dot(u)=A_u^{-1}p_u+I_u shifts the tertiary constraint",
            "hidden motion-load/source-flow leak unless I_u=0 theorem exists",
        ),
        (
            "HCM2174_1_linear_u",
            "J_u u term",
            "Lambda_R fixes against J_u, but the reaction can enter visible T/S/coframe equations",
            "active source coupling leak unless J_u and Lambda projection are silent",
        ),
        (
            "HCM2174_2_boundary",
            "boundary charge",
            "bulk u=0 does not by itself kill a corner/symplectic reciprocal charge",
            "Q_R hair can survive through the boundary class",
        ),
        (
            "HCM2174_3_readout",
            "post-constraint readout leak",
            "readout can reinsert u-dependence through endpoints, tau or common Weyl/disformal factors",
            "local tests remain live despite bulk constraint",
        ),
        (
            "HCM2174_4_GR_import",
            "EH benchmark import",
            "choosing H_vis to be GR gives a clean branch but imports the desired limit",
            "not a parent derivation unless MTS derives H_vis/operator ownership",
        ),
    ]
    return [
        base_row(
            countermodel_id=countermodel_id,
            countermodel=countermodel,
            construction=construction,
            live_effect=live_effect,
        )
        for countermodel_id, countermodel, construction, live_effect in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2174_0_gain", "CONTROLLED_SECOND_CLASS_PATTERN_FOUND", "u=C_R/2 with p_u can be eliminated conditionally via u≈0 and p_u≈0 rather than vague closure language", "selected"),
        ("DEC2174_1_no_claim", "PATTERN_NOT_PARENT_DERIVED", "A_u, I_u, J_u, boundary, matter and readout ownership remain missing", "selected"),
        ("DEC2174_2_core_bottleneck", "SOURCE_FREE_U_SECTOR_IS_NEXT", "the decisive missing theorem is I_u=J_u=0 plus invisible Lambda_R reaction", "selected"),
        ("DEC2174_3_empirical_guard", "FINITE_ROWS_REMAIN_PRIMARY_IF_SOURCE_FREE_FAILS", "if I_u/J_u survive, they become finite residual coefficients for PPN/WEP/R10/clock/orbital arenas", "selected"),
        ("DEC2174_4_next", "PARENT_EVENNESS_NO_SOURCE_U_SECTOR_NEXT", "attack source-free/even u-sector ownership before more data scoring", "selected"),
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
            route_id="NEXT2174_0_2175",
            selection_status="selected",
            target_file="2175-Y5-R2FR-parent-even-u-sector-no-source-theorem-or-Iu-Ju-residuals.md",
            target_script="scripts/Y5_R2FR_parent_even_u_sector_no_source_theorem_or_Iu_Ju_residuals_2175.py",
            objective="prove the parent H_core is even/source-free in the radial-cell coordinate u so I_u=0 and J_u=0, or emit finite I_u/J_u residual rows with arena projections",
            success_condition="I_u and J_u are theorem-zero with matter/boundary/readout silence, or the auxiliary route is demoted to finite residual coefficients",
            do_not_do="do not claim local GR from the second-class pattern alone, do not hide source terms in Lambda_R, do not import GR H_core",
        ),
        base_row(
            route_id="NEXT2174_1_parallel_boundary",
            selection_status="held_parallel",
            target_file="2175b-Y5-R2FR-boundary-differentiability-for-u-constraint-or-QR-row.md",
            target_script="scripts/Y5_R2FR_boundary_differentiability_for_u_constraint_or_QR_row_2175b.py",
            objective="after or alongside I_u/J_u, prove the boundary differentiability/no-charge theorem for the u-constraint branch",
            success_condition="no reciprocal boundary charge survives, or Q_R becomes a finite source-backed row",
            do_not_do="do not assume bulk u=0 kills boundary hair",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["closure_conditions"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["dirac_flow"], BRANCH_COPIES["branch_wep"]),
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
    validations.append(base_row(validation_id="VAL2174_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2174_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    skeleton_text = " ".join(str(row.get("statement", "")) for row in rows_by_name["canonical_skeleton"])
    validations.append(base_row(validation_id="VAL2174_02_canonical_skeleton", status="PASS" if "u := ln(T sqrt(S)) = C_R/2" in skeleton_text and "I_u p_u + J_u u" in skeleton_text else "FAIL", detail="u-sector canonical skeleton recorded"))

    flow_statuses = {row["status"] for row in rows_by_name["dirac_flow"]}
    validations.append(base_row(validation_id="VAL2174_03_dirac_flow", status="PASS" if "CONTROLLED_TERTIARY_IF_AU_NONZERO" in flow_statuses and "EXACT_CONDITIONAL" in flow_statuses else "FAIL", detail="controlled second-class pattern identified only conditionally"))

    conditions = " ".join(str(row.get("symbol", "")) + str(row.get("status", "")) for row in rows_by_name["closure_conditions"])
    validations.append(base_row(validation_id="VAL2174_04_closure_conditions", status="PASS" if "I_uMISSING_ZERO_THEOREM" in conditions and "J_uMISSING_NO_SOURCE_THEOREM" in conditions else "FAIL", detail="I_u/J_u source-free conditions remain missing"))

    validations.append(base_row(validation_id="VAL2174_05_countermodels", status="PASS" if len(rows_by_name["countermodels"]) >= 5 else "FAIL", detail=f"countermodels={len(rows_by_name['countermodels'])}"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2174_06_decision", status="PASS" if "PARENT_EVENNESS_NO_SOURCE_U_SECTOR_NEXT" in decision_text else "FAIL", detail="decision selects source-free/even u-sector next"))

    validations.append(base_row(validation_id="VAL2174_07_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2175" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2175 Iu/Ju residual target selected"))

    validations.append(base_row(validation_id="VAL2174_08_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2174_09_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2174_10_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2174_artifacts()
    validations.append(base_row(validation_id="VAL2174_11_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2174 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2174_12_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2174_OVERALL", status="PASS" if overall else "FAIL", detail="2174 identifies a conditional second-class u-sector closure pattern and selects I_u/J_u source-free theorem next"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2174 - Y5/R2FR H_core Canonical Bracket Closure Or Auxiliary Route Demotion

## Current Verdict

2174 finds a real conditional closure pattern, but **does not** claim local GR/Newton.

Let

`u := ln(T sqrt(S)) = C_R/2`, with `{{u(x),p_u(y)}}=delta(x-y)`.

Use the minimal local skeleton:

`H_core = H_vis + 1/2 A_u^-1 p_u^2 + 1/2 K_u u^2 + I_u p_u + J_u u + ...`

Then `Lambda_R C_R = 2 Lambda_R u` gives:

`pi_Lambda≈0`, then `u≈0`, then `dot(u)=A_u^-1 p_u + I_u + ...≈0`.

So a clean branch can eliminate the radial-cell mode as a controlled second-class pair only if the parent theory proves the dangerous linear channels vanish:

`I_u=0`, `J_u=0`, plus boundary, matter/source and readout silence.

That is the first genuinely constructive auxiliary route we have had. It is not a proof yet, but it tells us exactly what to prove next.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## Canonical U-Sector Skeleton

{md_table(rows_by_name["canonical_skeleton"], ["skeleton_id", "object", "statement", "status", "implication", "valid_for_claim"])}

## Dirac Flow Cases

{md_table(rows_by_name["dirac_flow"], ["flow_id", "constraint", "calculation", "status", "implication", "valid_for_claim"])}

## Closure Conditions

{md_table(rows_by_name["closure_conditions"], ["condition_id", "symbol", "required_statement", "status", "implication", "valid_for_claim"])}

## H_core Countermodels

{md_table(rows_by_name["countermodels"], ["countermodel_id", "countermodel", "construction", "live_effect", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Working Interpretation

This is better than another failure ledger. We now have a concrete conditional mechanism: the auxiliary constraint can work as a second-class elimination of the radial-cell mode, but only in a parent-owned source-free/even `u` sector.

The decisive next question is whether MTS primitives force `I_u=0` and `J_u=0`. If yes, the local-GR route gets much stronger. If no, those symbols become finite residual couplings that must be tested rather than wished away.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "canonical_skeleton": canonical_skeleton_rows(),
        "dirac_flow": dirac_flow_rows(),
        "closure_conditions": closure_condition_rows(),
        "countermodels": countermodel_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in ["source_register", "canonical_skeleton", "dirac_flow", "closure_conditions", "countermodels", "decision", "next_target"]:
        write_csv(OUTPUTS[name], rows_by_name[name])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()
