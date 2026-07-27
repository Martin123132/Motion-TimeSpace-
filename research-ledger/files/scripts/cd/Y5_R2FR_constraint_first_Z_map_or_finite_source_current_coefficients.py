from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUARANTINE = MICROSCOPE / "quarantine" / "1621"
INPUT_1621 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1621-Y5-R2FR-constraint-first-Z-map-or-finite-source-current-coefficients.md"

SOURCE_FILES = {
    "1620_doc": ROOT / "1620-Y5-R2FR-parent-signature-map-and-source-current-zero-or-q_loc-bound-fill.md",
    "1620_validation": OUT / "P8_Y5_BRR545_1620_VALIDATION.csv",
    "1620_next": OUT / "P8_Y5_PARENT_QLOC_1620_NEXT_TARGET.csv",
    "1620_verticality": OUT / "P8_Y5_PARENT_QLOC_1620_QUOTIENT_VERTICALITY_MAP_AUDIT.csv",
    "1620_bounds": OUT / "P8_Y5_PARENT_QLOC_1620_SOURCE_CURRENT_BOUND_FILL_ROWS.csv",
    "1562_origin": OUT / "P8_Y5_PARENT_QLOC_1562_LAMBDAR_ORIGIN_AUDIT.csv",
    "1562_class": OUT / "P8_Y5_PARENT_QLOC_1562_CONSTRAINT_CLASS_GATE.csv",
    "1576_constraint": OUT / "P8_Y5_PARENT_QLOC_1576_RAB_CONSTRAINT_NO_POLE_TEST.csv",
    "1576_nopole": OUT / "P8_Y5_PARENT_QLOC_1576_RAB_NO_POLE_THEOREM_ATTEMPT.csv",
    "1576_qmap": OUT / "P8_Y5_PARENT_QLOC_1576_RAB_QUOTIENT_MAP_CONSTRUCTION_ATTEMPT.csv",
    "1575_vertical": OUT / "P8_Y5_PARENT_QLOC_1575_RAB_VERTICAL_GENERATOR_SIGNATURE_ATTEMPT.csv",
    "1575_descent": OUT / "P8_Y5_PARENT_QLOC_1575_RAB_MATTER_DESCENT_SIGNATURE.csv",
    "1415_owner": OUT / "P8_Y5_R10_1415_SOURCE_CURRENT_OWNER_ATTEMPT.csv",
    "1416_ban": OUT / "P8_Y5_R10_1416_SOURCE_SLOT_CURRENT_RESCALING_BAN_ATTEMPT.csv",
}

NEEDLES = {
    "1620_doc": ["BEST_NEXT_DERIVATION_ROUTE", "VAL1620_OVERALL"],
    "1620_validation": ["VAL1620_OVERALL", "PASS"],
    "1620_next": ["1621-Y5-R2FR-constraint-first-Z-map-or-finite-source-current-coefficients.md", "constraint-first"],
    "1620_verticality": ["QVM1620_2_constraint_first", "BEST_NEXT_DERIVATION_ROUTE"],
    "1620_bounds": ["SCB1620_0_JZ_bulk", "MISSING_JZ_BOUND"],
    "1562_origin": ["ORG1562_3_second_class_auxiliary", "BEST_CONDITIONAL_ROUTE"],
    "1562_class": ["CLASS1562_5_second_class", "BETTER_CONDITIONAL_THAN_FIRST_CLASS"],
    "1576_constraint": ["CNP1576_5_verdict", "FAIL_CURRENT_CLAIM_CONSTRAINT_NO_POLE_NOT_DERIVED"],
    "1576_nopole": ["NPT1576_3_verdict", "FAIL_CURRENT_CLAIM_NO_POLE_NOT_DERIVED"],
    "1576_qmap": ["QMAP1576_2_constraint_first", "POSSIBLE_IF_CONSTRAINT_SIGNED"],
    "1575_vertical": ["VERT1575_5_verdict", "FAIL_CURRENT_CLAIM_VERTICALITY_NOT_SIGNED"],
    "1575_descent": ["MDS1575_5_verdict", "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED"],
    "1415_owner": ["SCO1415_6_verdict", "SOURCE_CURRENT_OWNER_NOT_DERIVED_RSOURCE_TEMPLATE_REQUIRED"],
    "1416_ban": ["BAN1416_6_verdict", "BAN_NOT_PROVED_FIRST_RSOURCE_ROW_REQUIRED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1621_SOURCE_REGISTER.csv"
CONSTRAINT_GATE = OUT / "P8_Y5_PARENT_QLOC_1621_CONSTRAINT_FIRST_ZMAP_GATE.csv"
NO_POLE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1621_NO_POLE_THEOREM_AUDIT.csv"
FINITE_COEFFS = OUT / "P8_Y5_PARENT_QLOC_1621_FINITE_SOURCE_CURRENT_COEFFICIENT_ROWS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1621_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1621_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1621_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1621_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1621_VALIDATION.csv"

COPY_TARGETS = {
    CONSTRAINT_GATE: [
        QUARANTINE / "CONSTRAINT_FIRST_ZMAP_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_constraint_first_zmap_gate_nonclaim_1621.csv",
    ],
    NO_POLE_AUDIT: [
        QUARANTINE / "NO_POLE_THEOREM_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_no_pole_theorem_audit_nonclaim_1621.csv",
    ],
    FINITE_COEFFS: [
        QUARANTINE / "FINITE_SOURCE_CURRENT_COEFFICIENT_ROWS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_finite_source_current_coefficient_rows_nonclaim_1621.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1621.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1621.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1621_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1621_constraint_first_zmap_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def constraint_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CFG1621_0_target", "constraint-first Z/R_AB map", "remove Z/R_AB before matter coupling rather than quotienting it after readout", "TARGET_DEFINED", "best route from 1620 because it avoids posthoc gauge deletion"),
        ("CFG1621_1_multiplier_origin", "parent origin of lambda_R or equivalent algebraic auxiliary", "lambda_R C_R must arise from parent phase-cell/current-chain/object-language identity", "MOTIVATED_NOT_DERIVED", "bare insertion formally works but is not a derivation"),
        ("CFG1621_2_algebraic_elimination", "second-class/algebraic auxiliary route", "E_Lambda:C_R=0 and E_R fixes Lambda_R without a propagating Z/R_AB Green kernel", "BEST_CONDITIONAL_ROUTE_NOT_SIGNED", "most plausible route but parent sort/no-derivative/matter/readout gates are open"),
        ("CFG1621_3_first_class_route", "first-class/no-pole route", "Omega_flat(v_R)=delta C_R, closed brackets, proper boundary charge, and degree-count certificate", "POSSIBLE_BUT_BLOCKED", "generator/brackets/degree count/boundary charge not supplied"),
        ("CFG1621_4_no_kinetic_pole", "no independent Z/R_AB kinetic residue", "Hessian/symplectic degeneracy or no-derivative grammar excludes inverse Green kernel", "NOT_PARENT_SIGNED", "finite Yukawa/source-current branch remains live if a kinetic pole exists"),
        ("CFG1621_5_matter_before_readout", "ordinary matter sees quotient after constraint elimination", "S_matter[e_obs(q(Phi_constraint)),theta] with no Z slot", "MATTER_DESCENT_NOT_SIGNED", "without this, source-current zero still fails"),
        ("CFG1621_6_boundary_readout", "boundary/readout stability", "constraint elimination adds no edge charge, corner term, or readout re-entry", "BOUNDARY_READOUT_OPEN", "hidden alpha_tail/source-mass leakage remains possible"),
        ("CFG1621_7_verdict", "constraint-first Z-map closes verticality", "CFG1621_1 through CFG1621_6 all pass", "CONSTRAINT_FIRST_ZMAP_NOT_DERIVED", "finite source-current coefficients must remain live"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "mathematical_requirement": requirement,
            "status": status,
            "effect": effect,
            "source_anchors": "P8_Y5_PARENT_QLOC_1562_LAMBDAR_ORIGIN_AUDIT.csv; P8_Y5_PARENT_QLOC_1562_CONSTRAINT_CLASS_GATE.csv; P8_Y5_PARENT_QLOC_1576_RAB_CONSTRAINT_NO_POLE_TEST.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, requirement, status, effect in rows
    ]


def no_pole_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NPA1621_0_conditional_theorem",
            "If Z/R_AB is algebraically constrained before matter coupling, has no kinetic pole, has no proper boundary charge, and matter descends through the reduced quotient, then no local Yukawa/source-current pole is present.",
            "CONDITIONAL_NO_POLE_THEOREM_RECORDED",
            "this is the exact route that would let the 1619 normal form become a parent branch",
        ),
        (
            "NPA1621_1_multiplier_insertion_refusal",
            "S_lambda=int sqrt(-g) lambda_R R_AB by itself only proves that an inserted multiplier can impose R_AB=0.",
            "REJECT_MAGIC_MULTIPLIER_AS_DERIVATION",
            "parent origin must be derived, not chosen to force GR",
        ),
        (
            "NPA1621_2_second_class_preference",
            "Second-class/algebraic auxiliary route is cleaner than first-class here because it removes the visible residual rather than calling it gauge.",
            "PREFERRED_CONDITIONAL_ROUTE",
            "still requires parent sort, no-derivative grammar, matter descent, boundary silence, and readout stability",
        ),
        (
            "NPA1621_3_positive_nohair_fallback",
            "If Z/R_AB is physical but positive/source-free, a no-hair theorem may set it to zero in local exterior.",
            "VALUES_AND_SOURCE_ZERO_MISSING",
            "requires Z_R, M_R^2, J_R=0, and boundary flux=0; not ready",
        ),
        (
            "NPA1621_4_absent_nonprimitive",
            "If R_AB is not a primitive parent field, it has no variation slot and no beta/source charge.",
            "NOT_PARENT_PROVED",
            "promising but needs parent field grammar/readout derivation",
        ),
        (
            "NPA1621_5_verdict",
            "No-pole import is not currently derived for MTS.",
            "NO_POLE_NOT_DERIVED_CURRENT_MTS",
            "fall back to finite residual coefficient rows until origin closes",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "claim_piece": claim_piece,
            "status": status,
            "effect": effect,
            "source_anchors": "P8_Y5_PARENT_QLOC_1576_RAB_NO_POLE_THEOREM_ATTEMPT.csv; P8_Y5_PARENT_QLOC_1576_RAB_CONSTRAINT_NO_POLE_TEST.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, claim_piece, status, effect in rows
    ]


def finite_coeff_rows() -> list[dict[str, Any]]:
    rows = [
        ("FCR1621_0_lambda_origin", "lambda_R parent-origin coefficient", "C_lambda_origin", "MISSING_PARENT_ORIGIN", "dimensionless_or_action-density scale; undeclared", "P8_Y5_PARENT_QLOC_1562_LAMBDAR_ORIGIN_AUDIT.csv", "no magic multiplier allowed"),
        ("FCR1621_1_Z_kinetic_residue", "Z/R_AB kinetic pole residue", "Z_R", "MISSING_NO_POLE_OR_FINITE_RESIDUE", "kinetic normalization", "P8_Y5_PARENT_QLOC_1576_RAB_CONSTRAINT_NO_POLE_TEST.csv", "finite pole implies Yukawa/source branch remains"),
        ("FCR1621_2_Z_mass", "Z/R_AB mass/range parameter", "M_R^2 or lambda_Range", "MISSING_MASS_OR_RANGE", "mass^2 or length", "P8_Y5_PARENT_QLOC_1576_RAB_NO_POLE_THEOREM_ATTEMPT.csv", "needed for any finite R10/local residual comparison"),
        ("FCR1621_3_JZ_source", "Z source current", "J_Z or beta_source^Z", "MISSING_SOURCE_CURRENT_BOUND", "source-current units", "P8_Y5_PARENT_QLOC_1620_SOURCE_CURRENT_BOUND_FILL_ROWS.csv", "source-current zero not derived"),
        ("FCR1621_4_Dq_leak", "quotient derivative leakage", "Dq[Z]", "MISSING_DQ_BOUND", "map derivative units", "P8_Y5_PARENT_QLOC_1620_SOURCE_CURRENT_BOUND_FILL_ROWS.csv", "verticality not proved"),
        ("FCR1621_5_source_weight", "source/species/current rescaling residual", "w_A or c_A", "MISSING_WEIGHT_BOUND", "dimensionless", "P8_Y5_R10_1416_SOURCE_SLOT_CURRENT_RESCALING_BAN_ATTEMPT.csv", "pre-action/current-weight countermodel remains"),
        ("FCR1621_6_boundary_tail", "boundary/readout tail", "B_Z or alpha_tail", "MISSING_BOUNDARY_BOUND", "stress flux or dimensionless alpha tail", "P8_Y5_PARENT_QLOC_1575_RAB_MATTER_DESCENT_SIGNATURE.csv", "bulk no-pole can fail through edge charge"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "coefficient_row_id": row_id,
            "residual_channel": channel,
            "coefficient": coefficient,
            "status": status,
            "units": units,
            "source_path": source_path,
            "blocker": blocker,
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, channel, coefficient, status, units, source_path, blocker in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1621_0_sources", "1620 route plus lambda/constraint/no-pole inputs imported", "SOURCE_CONTEXT_READY", "constraint-first gate is source anchored"),
        ("RUN1621_1_constraint_first", "second-class/algebraic auxiliary route identified", "BEST_CONDITIONAL_ROUTE_NOT_SIGNED", "formal route exists but parent origin is absent"),
        ("RUN1621_2_no_pole", "no-pole theorem conditions recorded", "NO_POLE_NOT_DERIVED_CURRENT_MTS", "cannot import no local pole/source charge"),
        ("RUN1621_3_finite_coeffs", "finite coefficient rows staged for lambda origin, kinetic residue, mass/range, source, Dq, weights, boundary", "FINITE_SOURCE_CURRENT_COEFFICIENT_ROWS_STAGED_NONCLAIM", "fallback route replaces theorem-zero wording"),
        ("RUN1621_4_local_GR", "constraint-first gate not closed", "DO_NOT_REOPEN_LOCAL_GR", "local GR/Newton recovery remains blocked"),
        ("RUN1621_5_next", "next obstruction is lambda_R parent origin/no-derivative grammar", "SELECT_1622_LAMBDAR_PARENT_ORIGIN_OR_FINITE_ZR_ROW", "derive origin or fill finite Z_R/M_R/J_Z coefficients"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "input_state": input_state,
            "runner_result": result,
            "effect": effect,
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, input_state, result, effect in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG1621_0_constraint_route", "constraint-first Z/R_AB route", "OPEN_CONDITIONAL", "best route but parent origin not derived"),
        ("CG1621_1_lambda_origin", "lambda_R parent origin", "BLOCKED", "multiplier insertion is formal only"),
        ("CG1621_2_no_pole", "no physical Z/R_AB pole", "BLOCKED", "no-kinetic-pole/no-primitive proof not parent-signed"),
        ("CG1621_3_verticality", "Z/R_AB removed before matter coupling or in ker(Dq)", "BLOCKED", "constraint/no-pole not derived"),
        ("CG1621_4_source_current", "J_Z=0", "BLOCKED", "needs descent after constraint/reduction"),
        ("CG1621_5_finite_rows", "finite source-current coefficients claim-ready", "BLOCKED", "rows are placeholders with missing bounds/units"),
        ("CG1621_6_local_GR", "derived local GR/Newton recovery", "BLOCKED", "constraint-first gate did not close"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1621_0_route", "CONSTRAINT_FIRST_ROUTE_IS_STILL_BEST_BUT_UNSIGNED", "second-class/algebraic auxiliary route avoids posthoc deletion and first-class gauge overreach", "keep as preferred derivation target"),
        ("DEC1621_1_no_claim", "NO_POLE_NOT_DERIVED_CURRENT_MTS", "lambda origin, no kinetic pole, matter descent, boundary/readout stability are not parent-signed", "no local-GR/R10/source-current zero claim"),
        ("DEC1621_2_fallback", "FINITE_SOURCE_CURRENT_COEFFICIENT_ROWS_STAGED_NONCLAIM", "finite rows now exist for all live failure channels", "use if lambda/no-pole derivation fails"),
        ("DEC1621_3_next", "NEXT_1622_LAMBDAR_PARENT_ORIGIN_OR_FINITE_ZR_ROW", "the narrowest missing proof is the parent origin/no-derivative grammar for lambda_R/Z_R", "derive lambda_R from parent phase-volume/current grammar or fill finite Z_R/M_R/J_Z rows"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1622-Y5-R2FR-lambdaR-parent-origin-and-no-derivative-grammar-or-finite-ZR-row.md",
            "script": "scripts/Y5_R2FR_lambdaR_parent_origin_and_no_derivative_grammar_or_finite_ZR_row.py",
            "objective": "try to derive lambda_R/Z_R as a parent-owned algebraic constraint with no derivative/kinetic pole from phase-volume/current grammar; if this fails, make finite Z_R, M_R, J_Z, and boundary rows explicit",
            "success_condition": "either the parent origin/no-derivative grammar closes for the constraint-first branch, or finite residual coefficient rows replace no-pole language",
            "do_not": "do not insert lambda_R by hand as a derivation, do not call formal Dirac closure parent-signed, do not hide kinetic residue, do not promote local GR",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("reopens_local_claim", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if truthy(row.get(field, "")):
                    return False
    return True


def no_formalization_1621() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1621-Y5",
        "P8_Y5_PARENT_QLOC_1621",
        "P8_Y5_BRR545_1621",
        "Y5_R2FR_constraint_first_Z_map",
        "R2FR_constraint_first_zmap_gate_nonclaim_1621",
        "R2FR_finite_source_current_coefficient_rows_nonclaim_1621",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    constraint = read_csv(CONSTRAINT_GATE)
    nopole = read_csv(NO_POLE_AUDIT)
    coeffs = read_csv(FINITE_COEFFS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1621_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1621 local source paths exist"),
        ("VAL1621_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1621 source needles found"),
        ("VAL1621_2_input_dir_ready", INPUT_1621.exists(), "1621 quarantine input directory exists"),
        ("VAL1621_3_constraint_not_derived", any(row["status"] == "CONSTRAINT_FIRST_ZMAP_NOT_DERIVED" for row in constraint), "constraint-first Z-map blocks promotion"),
        ("VAL1621_4_no_pole_not_derived", any(row["status"] == "NO_POLE_NOT_DERIVED_CURRENT_MTS" for row in nopole), "no-pole theorem is not imported"),
        ("VAL1621_5_reject_magic_multiplier", any(row["status"] == "REJECT_MAGIC_MULTIPLIER_AS_DERIVATION" for row in nopole), "bare lambda insertion refused as derivation"),
        ("VAL1621_6_coeff_rows_nonclaim", all(not truthy(row["valid_for_claim"]) and not truthy(row["claim_allowed"]) for row in coeffs), "finite coefficient rows remain nonclaim"),
        ("VAL1621_7_runner_blocks_local_gr", any(row["runner_result"] == "DO_NOT_REOPEN_LOCAL_GR" for row in runner), "runner refuses local-GR reopening"),
        ("VAL1621_8_claim_gates_closed", all(not truthy(row["claim_allowed"]) and row["status"] != "CLAIM_READY" for row in gates), "all claim gates remain closed/nonclaim"),
        ("VAL1621_9_decision_next", any(row["decision"] == "NEXT_1622_LAMBDAR_PARENT_ORIGIN_OR_FINITE_ZR_ROW" for row in decisions), "decision selects lambdaR parent-origin next target"),
        ("VAL1621_10_next_target_selected", any("1622-Y5-R2FR-lambdaR-parent-origin-and-no-derivative-grammar-or-finite-ZR-row.md" in row["next_target"] for row in next_rows), "next target selected"),
        ("VAL1621_11_csv_parse", csv_parses(generated_csvs), "all generated 1621 CSVs parse"),
        ("VAL1621_12_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1621 rows reopen local claims, score-ready rows, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1621_13_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1621_14_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1621_15_formalization_untouched", no_formalization_1621(), "no 1621 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1621_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1621 constraint-first Z-map or finite source-current coefficients validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    columns = columns or list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "/").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    source_rows = read_csv(SOURCE_REGISTER)
    constraint_rows = read_csv(CONSTRAINT_GATE)
    nopole_rows = read_csv(NO_POLE_AUDIT)
    coeff_rows = read_csv(FINITE_COEFFS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    validation = read_csv(VALIDATION)
    content = f"""# 1621 - R2/fR Constraint-First Z Map Or Finite Source-Current Coefficients

## Verdict
- 1621 keeps the constraint-first/no-pole route as the cleanest derivation path, but refuses to claim it: inserting `lambda_R` by hand is a formal device, not a parent-origin proof.
- The preferred conditional route is second-class/algebraic auxiliary elimination: remove `Z/R_AB` before matter coupling and avoid treating a coframe-visible residual as gauge after readout.
- Current MTS does not yet derive the required parent origin, no-derivative grammar, no kinetic pole, matter descent, boundary silence, or readout stability.
- Finite nonclaim coefficient rows are staged for `lambda_R` origin, `Z_R`, `M_R^2`, `J_Z`, `Dq[Z]`, source weights, and boundary tail.
- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "needles"])}

## Constraint-First Z Map Gate

{md_table(constraint_rows, ["gate_id", "gate", "mathematical_requirement", "status", "effect"])}

## No-Pole Theorem Audit

{md_table(nopole_rows, ["audit_id", "claim_piece", "status", "effect"])}

## Finite Source-Current Coefficient Rows

{md_table(coeff_rows, ["coefficient_row_id", "residual_channel", "coefficient", "status", "units", "source_path", "blocker"])}

## Runner

{md_table(runner, ["runner_id", "input_state", "runner_result", "effect"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim", "status", "reason"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"])}

## Validation

{md_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    INPUT_1621.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)

    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        CONSTRAINT_GATE: constraint_gate_rows(),
        NO_POLE_AUDIT: no_pole_audit_rows(),
        FINITE_COEFFS: finite_coeff_rows(),
        RUNNER: runner_rows(),
        CLAIM_GATE: claim_gate_rows(),
        DECISION: decision_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    copy_outputs()
    generated_csvs = list(outputs.keys())
    remove_pycache()
    write_csv(VALIDATION, validation_rows(generated_csvs))
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
