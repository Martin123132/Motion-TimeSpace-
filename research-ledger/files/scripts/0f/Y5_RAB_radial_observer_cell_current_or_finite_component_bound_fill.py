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
QUARANTINE = MICROSCOPE / "quarantine" / "1577"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md"

SOURCE_FILES = {
    "1576_doc": ROOT / "1576-Y5-RAB-constraint-no-pole-or-quotient-map-construction.md",
    "1576_validation": OUT / "P8_Y5_BRR545_1576_VALIDATION.csv",
    "1576_constraint": OUT / "P8_Y5_PARENT_QLOC_1576_RAB_CONSTRAINT_NO_POLE_TEST.csv",
    "1576_fallback": OUT / "P8_Y5_PARENT_QLOC_1576_RAB_FINITE_FALLBACK_COMPONENT_ROWS.csv",
    "05_reciprocity": ROOT / "05-reciprocity-theorem-attempt.md",
    "06_source_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "09_radial_cell": ROOT / "09-hamiltonian-radial-cell-derivation.md",
    "10_observer": ROOT / "10-observer-map-symplectic-contract.md",
    "11_cell_current": ROOT / "11-cell-current-origin-attempt.md",
    "12_noether": ROOT / "12-gauge-noether-origin-audit.md",
    "1267_first_class": ROOT / "1267-Y5-R10-first-class-RAB-parent-constraint-synthesis-or-finite-ZR-source-acquisition.md",
    "1274_unimodular": ROOT / "1274-Y5-R10-RAB-unimodular-radial-cell-constraint-origin-or-finite-residual-intake.md",
}

NEEDLES = {
    "1576_doc": ["NEXT_1577_RADIAL_OBSERVER_CELL_CURRENT_OR_FINITE_COMPONENT_BOUND_FILL", "conserved radial observer-cell/current no-charge theorem"],
    "1576_validation": ["VAL1576_OVERALL", "PASS"],
    "1576_constraint": ["CNP1576_5_verdict", "FAIL_CURRENT_CLAIM_CONSTRAINT_NO_POLE_NOT_DERIVED"],
    "1576_fallback": ["FF1576_0_constraint_origin", "MISSING_PARENT_CONSTRAINT_ORIGIN"],
    "05_reciprocity": ["W R_AB' = Q_R.", "hidden obstruction = Q_R reciprocal hair"],
    "06_source_neutrality": ["Pi_R = 0 -> Q_R = 0 -> R_AB = 0 -> AB = 1.", "Q_R neutrality is the missing source theorem"],
    "09_radial_cell": ["hamiltonian_radial_cell_sharpened_not_parent_derived", "separate radial cell gives p=1 exactly"],
    "10_observer": ["a conserved cell current with a no-charge theorem", "derive R_AB=0 from the parent theory"],
    "11_cell_current": ["cell_current_origin_no_charge_obstruction", "Q_R = constant."],
    "12_noether": ["gauge_noether_origin_not_derived_closure_only", "Noether structure can explain a constraint only after"],
    "1267_first_class": ["ordinary current gives Q_R hair", "SECOND_CLASS_OR_HOLONOMIC_NOT_FIRST_CLASS"],
    "1274_unimodular": ["does not derive the unimodular radial observer-cell condition", "GR_STYLE_DIFFERENCE_SELECTED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1577_SOURCE_REGISTER.csv"
CELL_CURRENT_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1577_RADIAL_CELL_CURRENT_ATTEMPT.csv"
NO_CHARGE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1577_QR_NO_CHARGE_THEOREM_AUDIT.csv"
FINITE_COMPONENTS = OUT / "P8_Y5_PARENT_QLOC_1577_FINITE_COMPONENT_BOUND_FILL_START.csv"
ARENA_INTERFACE = OUT / "P8_Y5_PARENT_QLOC_1577_ARENA_INTERFACE_NONCLAIM.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1577_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1577_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1577_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1577_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1577_VALIDATION.csv"

COPY_TARGETS = {
    CELL_CURRENT_ATTEMPT: [
        QUARANTINE / "RADIAL_CELL_CURRENT_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_radial_cell_current_attempt_nonclaim_1577.csv",
    ],
    NO_CHARGE_AUDIT: [
        QUARANTINE / "QR_NO_CHARGE_THEOREM_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "QR_no_charge_theorem_audit_nonclaim_1577.csv",
    ],
    FINITE_COMPONENTS: [
        QUARANTINE / "FINITE_COMPONENT_BOUND_FILL_START_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_finite_component_bound_fill_start_nonclaim_1577.csv",
    ],
    ARENA_INTERFACE: [
        QUARANTINE / "ARENA_INTERFACE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_arena_interface_nonclaim_1577.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_radial_current_decision_nonclaim_1577.csv",
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
                "source_id": f"SRC1577_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, NEEDLES[key]),
                "needles": "; ".join(NEEDLES[key]),
                "purpose": "radial observer-cell current no-charge attempt or finite component fill",
                **flags(),
            }
        )
    return rows


def cell_current_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "RCC1577_0_current_equation",
            "candidate": "conserved radial observer-cell current",
            "equation": "partial_r(W_R partial_r R_AB)=0 -> W_R partial_r R_AB = Q_R",
            "result": "DERIVES_CONSERVED_CHARGE_ONLY",
            "blocking_gap": "conservation gives Q_R constant, not Q_R=0",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "RCC1577_1_boundary",
            "candidate": "asymptotic or outer-boundary normalization",
            "equation": "R_AB(infinity)=0 with Q_R != 0 gives R_AB ~ -Q_R/r",
            "result": "DOES_NOT_KILL_HAIR",
            "blocking_gap": "needs no-charge boundary/source theorem, not only asymptotic flatness",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "RCC1577_2_source_neutrality",
            "candidate": "source reciprocal neutrality",
            "equation": "Pi_R=0 -> Q_R=0 -> R_AB=0",
            "result": "SUFFICIENT_CONDITIONAL_NOT_PARENT_SIGNED",
            "blocking_gap": "source boundary momentum Pi_R=0 is not derived from matter/source action",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "RCC1577_3_noether",
            "candidate": "Noether/gauge identity",
            "equation": "Noether identity relates E_R and constraints but does not set R_AB=0 unless C_R=R_AB is already a constraint",
            "result": "NOETHER_DOES_NOT_CONJURE_CONSTRAINT",
            "blocking_gap": "requires parent-owned constrained variable or first/second-class auxiliary block",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "RCC1577_4_verdict",
            "candidate": "current-derived no-charge theorem",
            "equation": "Q_R=0 from radial observer-cell current alone",
            "result": "FAIL_CURRENT_CLAIM_NO_CHARGE_NOT_DERIVED",
            "blocking_gap": "finite component bound fill is now mandatory unless a new parent action block appears",
            **flags(),
        },
    ]


def no_charge_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "NCA1577_0_charge_definition",
            "quantity": "Q_R",
            "zero_route": "source-neutral boundary class or auxiliary elimination before current formation",
            "current_status": "MISSING_PARENT_NO_CHARGE_THEOREM",
            "why_not_claim": "ordinary current preserves Q_R rather than killing it",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "NCA1577_1_boundary_momentum",
            "quantity": "Pi_R or B_R",
            "zero_route": "free/proper/exact boundary variation with Pi_R=0",
            "current_status": "MISSING_BOUNDARY_VARIATION_CLASS",
            "why_not_claim": "source-boundary class not derived",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "NCA1577_2_auxiliary",
            "quantity": "lambda_R C_R auxiliary block",
            "zero_route": "second-class/algebraic compatibility with no R_AB derivatives, sources, boundary, or readout regeneration",
            "current_status": "CONDITIONAL_ROUTE_NOT_PARENT_SIGNED",
            "why_not_claim": "1267/1268 keep AP1265 clauses unsigned",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "NCA1577_3_unimodular_cell",
            "quantity": "J_q=1 or R_AB=0",
            "zero_route": "parent unimodular radial-cell grammar",
            "current_status": "CLOSURE_ONLY_NOT_DERIVED",
            "why_not_claim": "1274 says cell condition works if imposed but lacks parent dynamics",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "NCA1577_4_verdict",
            "quantity": "Q_R=0",
            "zero_route": "any noncircular parent-signed no-charge theorem",
            "current_status": "NOT_DERIVED_CURRENT_CORPUS",
            "why_not_claim": "no available route closes without adding a closure axiom",
            **flags(),
        },
    ]


def finite_component_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "FCF1577_0_qRhat",
            "quantity": "q_R_hat or Q_R",
            "role": "PPN/local hair amplitude if current branch survives",
            "required_source": "parent no-charge theorem, source-backed Q_R value, or direct q_R_hat bound/projection",
            "current_status": "MISSING_QR_VALUE_OR_ZERO_THEOREM",
            "next_fill_action": "build source row with source path, units, source body, GM convention and no-cancellation policy",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "FCF1577_1_operator",
            "quantity": "Z_R, M_R^2",
            "role": "finite Yukawa/range branch if no-pole fails",
            "required_source": "parent kinetic/Hessian residue or theorem-zero/no-pole certificate",
            "current_status": "MISSING_OPERATOR_SIGNATURE",
            "next_fill_action": "stage row with normalization convention and parent action block",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "FCF1577_2_bulk_source",
            "quantity": "J_R, beta_S^R, beta_T^R",
            "role": "bulk R10/WEP/source-test coupling",
            "required_source": "matter descent theorem-zero or finite source/test charge coefficients",
            "current_status": "MISSING_SOURCE_CHARGE_RESOLUTION",
            "next_fill_action": "split source and test legs; forbid linear-c_g shortcut",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "FCF1577_3_boundary_tail",
            "quantity": "B_R, Pi_R^n, alpha_boundary_tail",
            "role": "boundary/readout/domain tail in local tests",
            "required_source": "boundary zero/proper/exact theorem or absolute finite bound",
            "current_status": "MISSING_BOUNDARY_RESOLUTION",
            "next_fill_action": "absolute no-cancellation envelope; no cancellation against bulk",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "FCF1577_4_arena_projection",
            "quantity": "tau_R10, tau_PPN, tau_clock, tau_orbital",
            "role": "projection from finite R_AB residual to observable arenas",
            "required_source": "arena-specific readout kernels and units",
            "current_status": "MISSING_ARENA_PROJECTIONS",
            "next_fill_action": "separate R10, PPN, clock and orbital projections; no cross-arena transfer",
            **flags(),
        },
    ]


def arena_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "arena_id": "ARI1577_0_PPN",
            "observable": "gamma_minus_1 or q_R_hat residual",
            "formula_contract": "gamma_minus_1 = C_QR q_R_hat + boundary/source tails",
            "current_status": "SCHEMA_ONLY_COMPONENTS_MISSING",
            "claim_rule": "no PPN score without q_R_hat/Q_R value or theorem-zero",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "arena_id": "ARI1577_1_R10",
            "observable": "alpha_MTS(lambda_R)",
            "formula_contract": "Xi_R10[beta_S^R beta_T^R/(4 pi G Z_R)+alpha_boundary_tail]",
            "current_status": "SCHEMA_ONLY_COMPONENTS_MISSING",
            "claim_rule": "no R10 score without accepted curve plus internal components",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "arena_id": "ARI1577_2_clock",
            "observable": "clock/fine-structure residual",
            "formula_contract": "tau_clock times constant/material sensitivity components",
            "current_status": "SCHEMA_ONLY_COMPONENTS_MISSING",
            "claim_rule": "clock rows cannot transfer to R10/PPN without parent theorem",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "arena_id": "ARI1577_3_orbital",
            "observable": "local orbital/perihelion/timing residual",
            "formula_contract": "tau_orbital projected acceleration or potential residual",
            "current_status": "SCHEMA_ONLY_COMPONENTS_MISSING",
            "claim_rule": "no orbital claim without same-frame source denominator and projection",
            **flags(),
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1577_0_sources",
            "object": "1576 handoff plus current/no-charge precedents",
            "status": "PASS_IF_VALIDATION_PASS",
            "detail": "source register confirms all current/no-charge evidence",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1577_1_current",
            "object": "radial cell current",
            "status": "DERIVES_QR_CONSTANT_NOT_ZERO",
            "detail": "current conservation alone leaves reciprocal hair",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1577_2_no_charge",
            "object": "Q_R=0 theorem",
            "status": "NOT_DERIVED_CURRENT_CORPUS",
            "detail": "requires source-neutral boundary, auxiliary elimination, or parent cell grammar",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1577_3_finite_fill",
            "object": "finite component bound fill",
            "status": "STARTED_NONCLAIM",
            "detail": "component rows are staged but missing values/sources",
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1577_0_current",
            "claim": "radial cell current derives R_AB=0",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "conservation gives Q_R constant, not zero",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1577_1_no_charge",
            "claim": "Q_R=0 theorem exists",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "no parent source-neutral, auxiliary, or cell-grammar theorem is signed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1577_2_finite_rows",
            "claim": "finite component rows are scoreable",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "all component rows are missing-valued nonclaim scaffolds",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1577_3_local_GR",
            "claim": "derived local GR/Newton branch",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "current/no-charge route failed and finite branch is not source-filled",
            **flags(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1577_0_current_status",
            "decision": "RADIAL_CURRENT_NO_CHARGE_THEOREM_FAILS_CURRENT_CORPUS",
            "reason": "ordinary radial cell-current conservation preserves Q_R but does not set it to zero",
            "consequence": "do not claim R_AB constraint/no-pole from current conservation",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1577_1_fallback",
            "decision": "FINITE_COMPONENT_BOUND_FILL_STARTED_NONCLAIM",
            "reason": "the derivation route in this fork has exhausted without parent-signed no-charge",
            "consequence": "operator, source, boundary and arena projection rows must now be filled from source-backed inputs or theorem-zeroes",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1577_2_next",
            "decision": "NEXT_1578_RAB_FINITE_COMPONENT_BOUND_PACK_AND_RUNNER",
            "reason": "finite branch is now the honest local-test path until a new parent action block appears",
            "consequence": "create a strict component pack/runner that refuses placeholders and maps missing rows to PPN/R10/clock/orbital gates",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1578-Y5-RAB-finite-component-bound-pack-and-runner.md",
            "script": "scripts/Y5_RAB_finite_component_bound_pack_and_runner.py",
            "objective": "build a strict nonclaim finite-component pack for q_R_hat/Q_R, Z_R/M_R2, beta source/test, boundary tail, and arena projections; runner must refuse placeholders and report which empirical arenas remain blocked",
            "do_not": "do not fabricate component values; do not score R10/PPN/clock/orbital; do not treat closure baseline as derivation; do not edit formalization-workbench",
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


def has_1577_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1577" in path.name for path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    current = read_csv(CELL_CURRENT_ATTEMPT)
    no_charge = read_csv(NO_CHARGE_AUDIT)
    finite = read_csv(FINITE_COMPONENTS)
    arena = read_csv(ARENA_INTERFACE)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    checks = [
        ("VAL1577_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist"),
        ("VAL1577_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL1577_2_current_fails_nocharge",
            any(row["attempt_id"] == "RCC1577_4_verdict" and row["result"] == "FAIL_CURRENT_CLAIM_NO_CHARGE_NOT_DERIVED" for row in current),
            "radial current no-charge theorem is not promoted",
        ),
        (
            "VAL1577_3_nocharge_not_derived",
            any(row["audit_id"] == "NCA1577_4_verdict" and row["current_status"] == "NOT_DERIVED_CURRENT_CORPUS" for row in no_charge),
            "Q_R=0 theorem remains missing",
        ),
        (
            "VAL1577_4_finite_components_started",
            all(row["current_status"].startswith("MISSING") for row in finite),
            "finite component rows started with missing statuses",
        ),
        (
            "VAL1577_5_arena_interface_nonclaim",
            all(row["current_status"] == "SCHEMA_ONLY_COMPONENTS_MISSING" for row in arena),
            "arena interfaces are schema-only nonclaim rows",
        ),
        (
            "VAL1577_6_runner_blocks_claim",
            any(row["runner_id"] == "RUN1577_2_no_charge" and row["status"] == "NOT_DERIVED_CURRENT_CORPUS" for row in runner),
            "runner blocks no-charge/local claim",
        ),
        (
            "VAL1577_7_claim_gates_closed",
            all(row["claim_allowed"] == "False" for row in gates),
            "claim gates remain closed",
        ),
        (
            "VAL1577_8_decision_next",
            any(row["decision"] == "NEXT_1578_RAB_FINITE_COMPONENT_BOUND_PACK_AND_RUNNER" for row in decisions),
            "decision selects finite component pack and runner",
        ),
        ("VAL1577_9_csv_parse", all(len(read_csv(path)) > 0 for path in generated_csvs), "all generated 1577 CSVs parse cleanly"),
        ("VAL1577_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1577_11_no_raw_accepted", not has_1577_rows(RAB_RAW) and not has_1577_rows(RAB_ACCEPTED), "no 1577 rows written to raw/accepted finite directories"),
        ("VAL1577_12_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets), "branch/quarantine nonclaim copies written"),
        ("VAL1577_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1577_14_formalization_untouched", formalization_modified_count() == 0, "formalization-workbench modified-file count is 0"),
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
            "check_id": "VAL1577_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1577 radial observer-cell current or finite component fill validation",
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
    current: list[dict[str, Any]],
    no_charge: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    arena: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1577 - R_AB Radial Observer-Cell Current Or Finite Component Bound Fill",
                "## Verdict\n"
                "- The conserved radial observer-cell current route fails as a derivation of local GR: it gives `W_R partial_r R_AB=Q_R`, so it preserves reciprocal hair unless a separate no-charge theorem sets `Q_R=0`.\n"
                "- Source neutrality, Noether/gauge language, auxiliary elimination, and unimodular cell grammar remain useful routes, but none are parent-signed in the current corpus.\n"
                "- This fork is therefore demoted from exact local-GR derivation to finite-component nonclaim filling unless a new parent action block appears.\n"
                "- The finite fallback has now started as strict source-ready scaffolding for `q_R_hat/Q_R`, `Z_R/M_R^2`, `J_R/beta_S^R/beta_T^R`, boundary tails, and arena projections.\n"
                "- No Q_R=0, R_AB=0, no-pole, R10, PPN, local GR/Newton, WEP, clock, orbital, `Z_R=0`, `tau_R10=0`, or `q_R=0` claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Radial Cell Current Attempt",
                md_table(current, ["attempt_id", "candidate", "equation", "result", "blocking_gap"]),
                "## Q_R No-Charge Theorem Audit",
                md_table(no_charge, ["audit_id", "quantity", "zero_route", "current_status", "why_not_claim"]),
                "## Finite Component Bound Fill Start",
                md_table(finite, ["component_id", "quantity", "role", "required_source", "current_status", "next_fill_action"]),
                "## Arena Interface Nonclaim",
                md_table(arena, ["arena_id", "observable", "formula_contract", "current_status", "claim_rule"]),
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
    current = cell_current_attempt_rows()
    no_charge = no_charge_audit_rows()
    finite = finite_component_rows()
    arena = arena_interface_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        CELL_CURRENT_ATTEMPT,
        NO_CHARGE_AUDIT,
        FINITE_COMPONENTS,
        ARENA_INTERFACE,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(CELL_CURRENT_ATTEMPT, current)
    write_csv(NO_CHARGE_AUDIT, no_charge)
    write_csv(FINITE_COMPONENTS, finite)
    write_csv(ARENA_INTERFACE, arena)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, current, no_charge, finite, arena, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
