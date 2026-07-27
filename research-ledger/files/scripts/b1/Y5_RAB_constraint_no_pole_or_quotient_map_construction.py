from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1576"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1576-Y5-RAB-constraint-no-pole-or-quotient-map-construction.md"

SOURCE_FILES = {
    "1575_doc": ROOT / "1575-Y5-RAB-parent-RAB-vertical-generator-and-matter-descent-signature.md",
    "1575_validation": OUT / "P8_Y5_BRR545_1575_VALIDATION.csv",
    "1575_vertical": OUT / "P8_Y5_PARENT_QLOC_1575_RAB_VERTICAL_GENERATOR_SIGNATURE_ATTEMPT.csv",
    "1575_trilemma": OUT / "P8_Y5_PARENT_QLOC_1575_RAB_COFAME_VISIBILITY_TRILEMMA.csv",
    "06_source_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "07_constraint": ROOT / "07-nonpropagating-reciprocity-constraint.md",
    "08_phase_volume": ROOT / "08-phase-volume-reciprocity-origin.md",
    "10_observer": ROOT / "10-observer-map-symplectic-contract.md",
    "1041_no_pole": ROOT / "1041-Y5-R10-parent-X-sector-ThetaX-PX-owner-or-boundary-coefficient-prior.md",
}

NEEDLES = {
    "1575_doc": ["NEXT_1576_RAB_CONSTRAINT_NO_POLE_OR_QUOTIENT_MAP_CONSTRUCTION", "Closure-only verticality is refused"],
    "1575_validation": ["VAL1575_OVERALL", "PASS"],
    "1575_vertical": ["VERT1575_3_constraint_escape", "BEST_ROUTE_BUT_PARENT_ORIGIN_UNSIGNED"],
    "1575_trilemma": ["TRI1575_2_constraint_no_pole", "BEST_LOCAL_GR_ROUTE_UNSIGNED"],
    "06_source_neutrality": ["Pi_R = 0 -> Q_R = 0 -> R_AB = 0 -> AB = 1.", "constraint mode"],
    "07_constraint": ["S_constraint = integral lambda_R R_AB.", "parent origin is still open"],
    "08_phase_volume": ["phase_volume_reciprocity_motivated_not_parent_derived", "lambda_R parent origin"],
    "10_observer": ["a genuine constraint whose multiplier has a parent origin", "derive R_AB=0 from the parent theory"],
    "1041_no_pole": ["first-class vertical constraint", "ROUTE_OPEN_NOT_CLOSED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1576_SOURCE_REGISTER.csv"
CONSTRAINT_TEST = OUT / "P8_Y5_PARENT_QLOC_1576_RAB_CONSTRAINT_NO_POLE_TEST.csv"
QUOTIENT_MAP = OUT / "P8_Y5_PARENT_QLOC_1576_RAB_QUOTIENT_MAP_CONSTRUCTION_ATTEMPT.csv"
NO_POLE_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1576_RAB_NO_POLE_THEOREM_ATTEMPT.csv"
FINITE_FALLBACK = OUT / "P8_Y5_PARENT_QLOC_1576_RAB_FINITE_FALLBACK_COMPONENT_ROWS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1576_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1576_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1576_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1576_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1576_VALIDATION.csv"

COPY_TARGETS = {
    CONSTRAINT_TEST: [
        QUARANTINE / "RAB_CONSTRAINT_NO_POLE_TEST_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_constraint_no_pole_test_nonclaim_1576.csv",
    ],
    QUOTIENT_MAP: [
        QUARANTINE / "RAB_QUOTIENT_MAP_CONSTRUCTION_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_quotient_map_construction_attempt_nonclaim_1576.csv",
    ],
    NO_POLE_THEOREM: [
        QUARANTINE / "RAB_NO_POLE_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_no_pole_theorem_attempt_nonclaim_1576.csv",
    ],
    FINITE_FALLBACK: [
        QUARANTINE / "RAB_FINITE_FALLBACK_COMPONENT_ROWS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_finite_fallback_component_rows_nonclaim_1576.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_constraint_no_pole_decision_nonclaim_1576.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "parent_signed": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "parent_signed",
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1576_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, NEEDLES[key]),
                "needles": "; ".join(NEEDLES[key]),
                "purpose": "R_AB constraint/no-pole or quotient-map construction attempt",
                **flags(),
            }
        )
    return rows


def constraint_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "test_id": "CNP1576_0_multiplier_origin",
            "test": "lambda_R must be generated by a parent constraint/current, not inserted to force GR",
            "needed_signature": "parent action contains lambda_R C_R with C_R=R_AB from a derived phase-cell/current-chain identity",
            "current_evidence": "07 writes lambda_R R_AB; 08 motivates radial phase-cell balance",
            "current_status": "MOTIVATED_NOT_PARENT_DERIVED",
            "failure_effect": "constraint route cannot be claimed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "test_id": "CNP1576_1_no_kinetic_pole",
            "test": "R_AB has no independent invertible local Green kernel",
            "needed_signature": "no Z_R kinetic residue, or first-class degeneracy of the Hessian/symplectic form",
            "current_evidence": "1041 ranks first-class/absent quotient as best but not parent-selected",
            "current_status": "NOT_PARENT_SIGNED",
            "failure_effect": "finite Yukawa branch remains live",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "test_id": "CNP1576_2_first_class",
            "test": "v_R is a first-class vertical direction",
            "needed_signature": "Omega_flat(v_R)=delta C_R, bracket closure, degree count, and proper gauge generators",
            "current_evidence": "1041 gives the template only",
            "current_status": "NOT_PARENT_SIGNED",
            "failure_effect": "v_R cannot be treated as pure gauge",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "test_id": "CNP1576_3_boundary_charge",
            "test": "Q_R/Pi_R/B_R boundary charge vanishes or is proper/exact",
            "needed_signature": "source-boundary variation gives no reciprocal charge and no edge alpha_tail",
            "current_evidence": "06 identifies Pi_R=0 as sufficient; not parent-derived",
            "current_status": "BOUNDARY_SILENCE_NOT_PARENT_SIGNED",
            "failure_effect": "boundary/readout tail remains in alpha_MTS",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "test_id": "CNP1576_4_matter_descent",
            "test": "matter sees only quotient-owned observed geometry and fixed constants",
            "needed_signature": "1575 matter descent signature clauses all parent-signed",
            "current_evidence": "1575 writes the exact signature but marks it unsigned",
            "current_status": "MATTER_DESCENT_NOT_PARENT_SIGNED",
            "failure_effect": "beta source/test charges remain live",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "test_id": "CNP1576_5_verdict",
            "test": "R_AB removed as physical local pole/source",
            "needed_signature": "CNP1576_0 through CNP1576_4 all pass together",
            "current_evidence": "current corpus closes none of the parent-origin signatures",
            "current_status": "FAIL_CURRENT_CLAIM_CONSTRAINT_NO_POLE_NOT_DERIVED",
            "failure_effect": "fall back to finite residual component rows",
            **flags(),
        },
    ]


def quotient_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "map_id": "QMAP1576_0_observer_jacobian",
            "candidate_q": "q includes the observer radial phase-cell/J_q data",
            "Dq_vR_status": "NONZERO_OR_UNPROVED",
            "reason": "10 states R_AB=ln(T^2 S)=2 ln(J_q), so changing R_AB changes the observer cell unless constrained",
            "claim_effect": "cannot call R_AB vertical in this map",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "map_id": "QMAP1576_1_shape_only_quotient",
            "candidate_q": "q keeps physical shape/orientation but quotients reciprocal cell-volume R_AB",
            "Dq_vR_status": "POSSIBLE_CONTRACT_NOT_CONSTRUCTED",
            "reason": "requires an independent unit/cell normalization so matter rods/clocks do not see R_AB",
            "claim_effect": "best quotient route but needs explicit q and Obs_e",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "map_id": "QMAP1576_2_constraint_first",
            "candidate_q": "impose R_AB=0 as a parent constraint, then q has no R_AB fibre",
            "Dq_vR_status": "POSSIBLE_IF_CONSTRAINT_SIGNED",
            "reason": "constraint route avoids making coframe-visible R_AB a gauge direction",
            "claim_effect": "best local-GR route if lambda_R parent origin closes",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "map_id": "QMAP1576_3_posthoc_delete",
            "candidate_q": "delete R_AB after deriving/readout because it is inconvenient",
            "Dq_vR_status": "REFUSED",
            "reason": "post-readout quotient would hide a real source charge and violates 1575 closure refusal",
            "claim_effect": "no use allowed",
            **flags(),
        },
    ]


def no_pole_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NPT1576_0_first_class",
            "route": "first-class constraint/no physical pole",
            "sufficient_conditions": "Omega_flat(v_R)=delta C_R, C_R=R_AB, closed constraint algebra, Q_R=0/proper, matter descent",
            "current_status": "ROUTE_OPEN_NOT_CLOSED",
            "if_closed": "no local R_AB Green kernel and no bulk R10 Yukawa exchange",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NPT1576_1_positive_sourcefree",
            "route": "positive source-free no-hair",
            "sufficient_conditions": "Z_R>0, M_R^2>0, J_R=0, boundary flux=0 and allowed topology",
            "current_status": "VALUES_AND_SOURCE_ZERO_MISSING",
            "if_closed": "R_AB=0 in local exterior without setting it by axiom",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NPT1576_2_absent_nonprimitive",
            "route": "R_AB is not a primitive parent field",
            "sufficient_conditions": "R_AB is a derived/readout artefact eliminated before variation and never appears in S_matter",
            "current_status": "NOT_PARENT_PROVED",
            "if_closed": "Theta_R=P_R=0 and beta_i^R has no variation slot",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NPT1576_3_verdict",
            "route": "no-pole import",
            "sufficient_conditions": "one route above parent-signed with boundary/matter clauses",
            "current_status": "FAIL_CURRENT_CLAIM_NO_POLE_NOT_DERIVED",
            "if_closed": "move to raw theorem-zero row only after independent validation",
            **flags(),
        },
    ]


def finite_fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "fallback_id": "FF1576_0_constraint_origin",
            "quantity": "lambda_R parent origin / C_R",
            "required_resolution": "derive phase-cell/current constraint or mark absent",
            "current_status": "MISSING_PARENT_CONSTRAINT_ORIGIN",
            "score_effect": "decides constraint route versus finite residual",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "fallback_id": "FF1576_1_operator",
            "quantity": "Z_R, M_R^2, Hessian rank",
            "required_resolution": "first-class degeneracy/no-pole theorem or positive finite operator values",
            "current_status": "MISSING_OPERATOR_SIGNATURE",
            "score_effect": "sets no-pole or lambda_R",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "fallback_id": "FF1576_2_source",
            "quantity": "J_R, beta_S^R, beta_T^R",
            "required_resolution": "matter descent zero theorem or source-backed finite charges",
            "current_status": "MISSING_SOURCE_CHARGE_RESOLUTION",
            "score_effect": "sets R10 bulk alpha amplitude",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "fallback_id": "FF1576_3_boundary",
            "quantity": "Q_R/Pi_R/B_R/alpha_boundary_tail",
            "required_resolution": "boundary zero/proper/exact theorem or absolute bound",
            "current_status": "MISSING_BOUNDARY_RESOLUTION",
            "score_effect": "sets tail envelope",
            **flags(),
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1576_0_sources",
            "object": "1575 plus source-neutrality/constraint/phase-volume/no-pole evidence",
            "status": "PASS_IF_VALIDATION_PASS",
            "detail": "source register confirms all needles",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1576_1_constraint",
            "object": "parent-origin lambda_R R_AB constraint",
            "status": "MOTIVATED_NOT_PARENT_DERIVED",
            "detail": "phase-cell route motivates but does not derive the multiplier/current-chain owner",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1576_2_quotient",
            "object": "R_AB quotient map",
            "status": "NOT_CONSTRUCTED",
            "detail": "observer Jacobian visibility blocks cheap verticality",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1576_3_no_pole",
            "object": "no physical R_AB pole",
            "status": "FAIL_CURRENT_CLAIM_NO_POLE_NOT_DERIVED",
            "detail": "first-class/positive/absent routes are open but unsigned",
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1576_0_constraint",
            "claim": "R_AB constraint has parent origin",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "lambda_R origin/current-chain owner not derived",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1576_1_quotient",
            "claim": "R_AB is quotient/fibre vertical",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "observer Jacobian visibility requires explicit q/Obs_e or constraint-first route",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1576_2_no_pole",
            "claim": "no physical R_AB pole",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "first-class/positive/no-hair/absent route not parent-signed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1576_3_R10",
            "claim": "R10/local fifth-force branch safe",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "finite fallback components remain unresolved",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1576_4_local_GR",
            "claim": "derived local GR/Newton",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "R_AB removal is not enough without source denominator, PPN and boundary followthrough",
            **flags(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1576_0_constraint_status",
            "decision": "CONSTRAINT_ROUTE_MOTIVATED_NOT_DERIVED",
            "reason": "lambda_R R_AB is clean but parent-origin proof is still missing",
            "consequence": "do not import R_AB=0 or no-pole",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1576_1_quotient_status",
            "decision": "QUOTIENT_MAP_CONFLICT_IDENTIFIED",
            "reason": "R_AB=2 ln(J_q) means observer-cell visibility blocks cheap Dq[v_R]=0",
            "consequence": "q must be explicitly constructed or constraint-first route must remove R_AB",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1576_2_next",
            "decision": "NEXT_1577_RADIAL_OBSERVER_CELL_CURRENT_OR_FINITE_COMPONENT_BOUND_FILL",
            "reason": "the only derivation route left inside this fork is the conserved radial observer-cell/current no-charge theorem",
            "consequence": "try current/no-charge derivation once; if it fails, start finite component bound fill",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md",
            "script": "scripts/Y5_RAB_radial_observer_cell_current_or_finite_component_bound_fill.py",
            "objective": "try to derive a conserved radial observer-cell current with zero reciprocal charge Q_R, giving a parent-origin R_AB constraint/no-pole; if it fails, begin finite component bound fill for operator/source/boundary rows",
            "do_not": "do not insert lambda_R by hand; do not set Q_R=0 by boundary choice; do not score R10; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count() -> int:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def has_1576_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1576" in path.name for path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    constraints = read_csv(CONSTRAINT_TEST)
    qmap = read_csv(QUOTIENT_MAP)
    no_pole = read_csv(NO_POLE_THEOREM)
    fallback = read_csv(FINITE_FALLBACK)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    checks = [
        ("VAL1576_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist"),
        ("VAL1576_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL1576_2_constraint_not_derived",
            any(row["test_id"] == "CNP1576_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_CONSTRAINT_NO_POLE_NOT_DERIVED" for row in constraints),
            "constraint/no-pole not falsely promoted",
        ),
        (
            "VAL1576_3_quotient_conflict",
            any(row["map_id"] == "QMAP1576_0_observer_jacobian" and row["Dq_vR_status"] == "NONZERO_OR_UNPROVED" for row in qmap),
            "observer Jacobian conflict recorded",
        ),
        (
            "VAL1576_4_no_pole_not_imported",
            any(row["theorem_id"] == "NPT1576_3_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_NO_POLE_NOT_DERIVED" for row in no_pole),
            "no-pole import refused",
        ),
        (
            "VAL1576_5_fallback_missing",
            all(row["current_status"].startswith("MISSING") for row in fallback),
            "finite fallback rows remain missing-valued",
        ),
        (
            "VAL1576_6_runner_blocks",
            any(row["runner_id"] == "RUN1576_3_no_pole" and row["status"] == "FAIL_CURRENT_CLAIM_NO_POLE_NOT_DERIVED" for row in runner),
            "runner blocks no-pole/R10 claim",
        ),
        (
            "VAL1576_7_claim_gates_closed",
            all(row["claim_allowed"] == "False" for row in gates),
            "claim gates remain closed",
        ),
        (
            "VAL1576_8_decision_next",
            any(row["decision"] == "NEXT_1577_RADIAL_OBSERVER_CELL_CURRENT_OR_FINITE_COMPONENT_BOUND_FILL" for row in decisions),
            "decision selects radial observer-cell current or finite fill target",
        ),
        ("VAL1576_9_csv_parse", all(len(read_csv(path)) > 0 for path in generated_csvs), "all generated 1576 CSVs parse cleanly"),
        ("VAL1576_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1576_11_no_raw_accepted", not has_1576_rows(RAB_RAW) and not has_1576_rows(RAB_ACCEPTED), "no 1576 rows written to raw/accepted finite directories"),
        ("VAL1576_12_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets), "branch/quarantine nonclaim copies written"),
        ("VAL1576_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1576_14_formalization_untouched", formalization_modified_count() == 0, "formalization-workbench modified-file count is 0"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1576_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1576 R_AB constraint/no-pole or quotient map validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")) for col in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    constraints: list[dict[str, Any]],
    qmap: list[dict[str, Any]],
    no_pole: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1576 - R_AB Constraint No-Pole Or Quotient Map Construction",
                "## Verdict\n"
                "- The clean local-GR route remains a parent-origin constraint/no-pole or explicit quotient map, not a fitted finite fifth-force residual.\n"
                "- The constraint route is still only motivated: `lambda_R R_AB` is algebraically clean, but `lambda_R` has not been derived from a parent current, phase-cell identity, first-class constraint, or total action owner.\n"
                "- The quotient route has a real conflict to solve: earlier observer-map work has `R_AB=ln(T^2 S)=2 ln(J_q)`, so `R_AB` is not automatically fibre-vertical unless a constraint-first or explicit shape-only quotient map is constructed.\n"
                "- Therefore no no-pole, beta-zero, R10, PPN, local GR/Newton, WEP, clock, orbital, `Z_R=0`, `tau_R10=0`, or `q_R=0` claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Constraint No-Pole Test",
                md_table(constraints, ["test_id", "test", "needed_signature", "current_status", "failure_effect"]),
                "## Quotient Map Construction Attempt",
                md_table(qmap, ["map_id", "candidate_q", "Dq_vR_status", "reason", "claim_effect"]),
                "## No-Pole Theorem Attempt",
                md_table(no_pole, ["theorem_id", "route", "sufficient_conditions", "current_status", "if_closed"]),
                "## Finite Fallback Components",
                md_table(fallback, ["fallback_id", "quantity", "required_resolution", "current_status", "score_effect"]),
                "## Runner Nonclaim",
                md_table(runner, ["runner_id", "object", "status", "detail"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "consequence"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    constraints = constraint_test_rows()
    qmap = quotient_map_rows()
    no_pole = no_pole_theorem_rows()
    fallback = finite_fallback_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        CONSTRAINT_TEST,
        QUOTIENT_MAP,
        NO_POLE_THEOREM,
        FINITE_FALLBACK,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(CONSTRAINT_TEST, constraints)
    write_csv(QUOTIENT_MAP, qmap)
    write_csv(NO_POLE_THEOREM, no_pole)
    write_csv(FINITE_FALLBACK, fallback)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, constraints, qmap, no_pole, fallback, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
