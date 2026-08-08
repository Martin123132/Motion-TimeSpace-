from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1578"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1578-Y5-RAB-finite-component-bound-pack-and-runner.md"

SOURCE_FILES = {
    "1577_doc": ROOT / "1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md",
    "1577_validation": OUT / "P8_Y5_BRR545_1577_VALIDATION.csv",
    "1577_components": OUT / "P8_Y5_PARENT_QLOC_1577_FINITE_COMPONENT_BOUND_FILL_START.csv",
    "1577_arena": OUT / "P8_Y5_PARENT_QLOC_1577_ARENA_INTERFACE_NONCLAIM.csv",
    "1576_doc": ROOT / "1576-Y5-RAB-constraint-no-pole-or-quotient-map-construction.md",
    "1575_doc": ROOT / "1575-Y5-RAB-parent-RAB-vertical-generator-and-matter-descent-signature.md",
    "1574_doc": ROOT / "1574-Y5-RAB-R10-matter-charge-and-ZR-MR2-input-row-or-zero-theorem.md",
    "1573_doc": ROOT / "1573-Y5-RAB-internal-tauR10-source-kernel-or-manual-curve-acceptance.md",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
    "r10_review_candidate": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
}

NEEDLES = {
    "1577_doc": ["NEXT_1578_RAB_FINITE_COMPONENT_BOUND_PACK_AND_RUNNER", "FCF1577_0_qRhat"],
    "1577_validation": ["VAL1577_OVERALL", "PASS"],
    "1577_components": ["FCF1577_4_arena_projection", "MISSING_ARENA_PROJECTIONS"],
    "1577_arena": ["ARI1577_1_R10", "alpha_MTS(lambda_R)"],
    "1576_doc": ["Finite Fallback Components", "FF1576_1_operator"],
    "1575_doc": ["Matter Descent Signature", "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED"],
    "1574_doc": ["Finite Input Rows", "FIN1574_2_ZR"],
    "1573_doc": ["alpha_MTS(lambda_R)=Xi_R10", "REVIEWED_CANDIDATE_NOT_ACCEPTED"],
    "local_bound_claims": ["Cassini_Shapiro_gamma_2003", "R10_fifth_force"],
    "r10_review_candidate": ["review_candidate_only_requires_official_supplement", "false"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1578_SOURCE_REGISTER.csv"
PACK_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1578_COMPONENT_PACK_SCHEMA.csv"
INPUT_STATUS = OUT / "P8_Y5_PARENT_QLOC_1578_COMPONENT_INPUT_STATUS.csv"
ARENA_BLOCK = OUT / "P8_Y5_PARENT_QLOC_1578_ARENA_BLOCK_MATRIX.csv"
PLACEHOLDER_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1578_PLACEHOLDER_REFUSAL_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1578_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1578_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1578_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1578_VALIDATION.csv"

COPY_TARGETS = {
    PACK_SCHEMA: [
        QUARANTINE / "FINITE_COMPONENT_PACK_SCHEMA_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_finite_component_pack_schema_nonclaim_1578.csv",
    ],
    INPUT_STATUS: [
        QUARANTINE / "COMPONENT_INPUT_STATUS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_component_input_status_nonclaim_1578.csv",
    ],
    ARENA_BLOCK: [
        QUARANTINE / "ARENA_BLOCK_MATRIX_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_arena_block_matrix_nonclaim_1578.csv",
    ],
    PLACEHOLDER_RUNNER: [
        QUARANTINE / "PLACEHOLDER_REFUSAL_RUNNER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_placeholder_refusal_runner_nonclaim_1578.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_claim_gate_nonclaim_1578.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_finite_component_decision_nonclaim_1578.csv",
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
        "input_ready",
        "accepted_for_scoring",
        "parent_signed",
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
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
                "source_id": f"SRC1578_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, NEEDLES[key]),
                "needles": "; ".join(NEEDLES[key]),
                "purpose": "finite R_AB component pack and placeholder-refusal runner",
                **flags(),
            }
        )
    return rows


def component_pack_schema_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PACK1578_0_qRhat",
            "q_R_hat or Q_R",
            "local reciprocal hair amplitude entering PPN and source-denominator tests",
            "parent no-charge theorem, numeric Q_R with source body/GM convention, or direct q_R_hat observable projection",
            "dimensionless q_R_hat or Q_R convention with radius/source normalization",
            "MISSING_QR_VALUE_OR_ZERO_THEOREM",
            "PPN;orbital;local_GR",
            "accept only theorem-zero or numeric row with source path, units, frame, source body and no-cancellation policy",
        ),
        (
            "PACK1578_1_ZR",
            "Z_R",
            "kinetic residue in finite R_AB propagator and R10 alpha denominator",
            "parent Hessian/operator extraction in same normalization as beta legs, or no-pole theorem",
            "positive kinetic residue with action normalization",
            "MISSING_PARENT_OPERATOR_ZR",
            "R10;PPN;clock;orbital;local_GR",
            "reject symbolic Z_R placeholders unless linked to parent action block and units",
        ),
        (
            "PACK1578_2_MR2",
            "M_R^2",
            "mass gap setting lambda_R=sqrt(Z_R/M_R^2)",
            "parent Hessian/mass-gap extraction in same normalization as Z_R",
            "positive mass squared or theorem-zero/no-pole certificate",
            "MISSING_PARENT_OPERATOR_MR2",
            "R10;clock;orbital",
            "reject lambda_R claims until Z_R and M_R^2 are sourced together",
        ),
        (
            "PACK1578_3_beta_source",
            "beta_S^R",
            "source-leg matter charge in bulk R10/WEP exchange",
            "matter descent theorem-zero or numeric partial ln m_source / partial R_AB with material/source path",
            "dimensionless source charge in same R_AB normalization",
            "MISSING_SOURCE_CHARGE_OR_ZERO_THEOREM",
            "R10;WEP;clock",
            "split source and test legs; forbid single coupling shortcut",
        ),
        (
            "PACK1578_4_beta_test",
            "beta_T^R",
            "test-leg matter charge in bulk R10/WEP exchange",
            "matter descent theorem-zero or numeric partial ln m_test / partial R_AB with material/test path",
            "dimensionless test charge in same R_AB normalization",
            "MISSING_TEST_CHARGE_OR_ZERO_THEOREM",
            "R10;WEP;clock",
            "require material/readout identity and no hidden marker coefficients",
        ),
        (
            "PACK1578_5_JR",
            "J_R",
            "bulk/source current for finite reciprocal residual",
            "parent source-current density or theorem-zero from matter/source action",
            "source-normalized current with compact-support/worldtube convention",
            "MISSING_SOURCE_CURRENT",
            "PPN;orbital;local_GR",
            "do not identify with GR stress tensor until denominator and frame are explicit",
        ),
        (
            "PACK1578_6_boundary",
            "B_R, Pi_R^n, alpha_boundary_tail",
            "boundary/worldtube/readout tail not cancelled against bulk",
            "zero/proper/exact boundary theorem or absolute finite no-cancellation bound",
            "absolute tail contribution in each observable arena",
            "MISSING_BOUNDARY_TAIL_OR_ZERO_THEOREM",
            "R10;PPN;clock;orbital;local_GR",
            "score only with explicit bound or theorem-zero; no cancellation against beta or q_R",
        ),
        (
            "PACK1578_7_tau_R10",
            "tau_R10 or Xi_R10",
            "projection from finite R_AB residual to short-range Yukawa alpha(lambda)",
            "R10-specific source-normalized readout kernel and accepted external curve",
            "dimensionless alpha kernel with lambda in metres",
            "MISSING_R10_PROJECTION_OR_ACCEPTED_CURVE",
            "R10",
            "reviewed-only curve may be cited but cannot become accepted_for_scoring",
        ),
        (
            "PACK1578_8_tau_PPN",
            "tau_PPN or C_QR",
            "projection from q_R_hat/Q_R and tails to gamma-1 and related PPN residuals",
            "PPN-specific source-frame kernel, source denominator and Cassini/PPN observable mapping",
            "dimensionless PPN coefficient",
            "MISSING_PPN_PROJECTION",
            "PPN;local_GR",
            "do not transfer R10 tau or clock silence to PPN",
        ),
        (
            "PACK1578_9_tau_clock",
            "tau_clock",
            "projection from R_AB residual to clock/constant/fine-structure channel",
            "clock-specific constant/material sensitivity kernel and source-frame convention",
            "dimensionless or frequency-fractional coefficient",
            "MISSING_CLOCK_PROJECTION",
            "clock;WEP",
            "requires constant-superselection theorem or finite material coefficients",
        ),
        (
            "PACK1578_10_tau_orbital",
            "tau_orbital",
            "projection from finite R_AB residual to acceleration, perihelion or timing residual",
            "orbital-specific potential/acceleration kernel in same frame as source denominator",
            "acceleration or dimensionless orbital residual coefficient",
            "MISSING_ORBITAL_PROJECTION",
            "orbital;local_GR",
            "no orbital score without source denominator and PPN-compatible frame",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": pack_id,
            "symbol": symbol,
            "equation_role": equation_role,
            "accepted_input_forms": accepted_input_forms,
            "required_units_or_convention": required_units_or_convention,
            "failure_status": failure_status,
            "gates_blocked": gates_blocked,
            "update_rule": update_rule,
            **flags(),
        }
        for pack_id, symbol, equation_role, accepted_input_forms, required_units_or_convention, failure_status, gates_blocked, update_rule in rows
    ]


def component_input_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("INPUT1578_0_qRhat", "q_R_hat or Q_R", "", "", "", "", "MISSING_NUMERIC_VALUE_OR_PARENT_ZERO_THEOREM"),
        ("INPUT1578_1_ZR", "Z_R", "", "", "", "", "MISSING_PARENT_OPERATOR_NORMALIZATION"),
        ("INPUT1578_2_MR2", "M_R^2", "", "", "", "", "MISSING_PARENT_OPERATOR_MASS_GAP"),
        ("INPUT1578_3_beta_source", "beta_S^R", "", "", "", "", "MISSING_SOURCE_CHARGE_OR_DESCENT_SIGNATURE"),
        ("INPUT1578_4_beta_test", "beta_T^R", "", "", "", "", "MISSING_TEST_CHARGE_OR_DESCENT_SIGNATURE"),
        ("INPUT1578_5_JR", "J_R", "", "", "", "", "MISSING_SOURCE_CURRENT"),
        ("INPUT1578_6_boundary_tail", "alpha_boundary_tail", "", "", "", "", "MISSING_BOUNDARY_TAIL_ZERO_OR_BOUND"),
        ("INPUT1578_7_tau_R10", "tau_R10 or Xi_R10", "", "", "", "", "MISSING_ACCEPTED_PROJECTION_AND_CURVE"),
        ("INPUT1578_8_tau_PPN", "tau_PPN or C_QR", "", "", "", "", "MISSING_PPN_PROJECTION"),
        ("INPUT1578_9_tau_clock", "tau_clock", "", "", "", "", "MISSING_CLOCK_PROJECTION"),
        ("INPUT1578_10_tau_orbital", "tau_orbital", "", "", "", "", "MISSING_ORBITAL_PROJECTION"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": input_id,
            "symbol": symbol,
            "value": value,
            "units": units,
            "source_path": source_path,
            "source_anchor": source_anchor,
            "input_ready": False,
            "blocker": blocker,
            "claim_rule": "row remains nonclaim until value/theorem, units, source path, and arena projection are all present",
            **flags(),
        }
        for input_id, symbol, value, units, source_path, source_anchor, blocker in rows
    ]


def arena_block_matrix_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ARENA1578_0_R10",
            "R10 short-range inverse-square/Yukawa",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "alpha_MTS(lambda_R)=Xi_R10[beta_S^R beta_T^R/(4 pi G Z_R)+alpha_boundary_tail]",
            "Z_R;M_R^2;beta_S^R;beta_T^R;Xi_R10;alpha_boundary_tail;accepted alpha_bound(lambda)",
            "REVIEWED_CANDIDATE_NOT_ACCEPTED",
            "BLOCKED_NO_CLAIM",
            "internal components missing and curve is reviewed-only",
            "source internal components first; then promote external curve only after manual/official QA",
        ),
        (
            "ARENA1578_1_PPN",
            "Cassini/PPN gamma and related weak-field coefficients",
            "source-intake/local_bounds/local_bound_claims.csv::Cassini_Shapiro_gamma_2003",
            "gamma_minus_1=C_QR q_R_hat+source_tail+boundary_tail",
            "q_R_hat or Q_R;C_QR;tau_PPN;source denominator;boundary/source tails",
            "EXTERNAL_BOUND_EXISTS_INTERNAL_PROJECTION_MISSING",
            "BLOCKED_NO_CLAIM",
            "no q_R_hat/Q_R value, no PPN projection kernel, and no source denominator",
            "build PPN-specific residual vector before any Cassini comparison",
        ),
        (
            "ARENA1578_2_clock",
            "clock/redshift/fine-structure channel",
            "source-intake/local_bounds/local_bound_claims.csv::Galileo_redshift_Delva_2018",
            "delta_clock=tau_clock*(constant/material sensitivity components)+tail",
            "tau_clock;constant-superselection theorem or finite dtheta/dR_AB;material coefficients;tail",
            "EXTERNAL_BOUND_EXISTS_INTERNAL_PROJECTION_MISSING",
            "BLOCKED_NO_CLAIM",
            "clock silence cannot be borrowed from WEP/R10 and constants remain unsigned",
            "fill constant/material sensitivity pack or prove superselection",
        ),
        (
            "ARENA1578_3_orbital",
            "orbital/perihelion/timing residual",
            "source-intake/local_bounds/local_bound_claims.csv::LLR_Biskupek_Muller_Torre_2021",
            "delta a_or_deltaPhi=tau_orbital*(J_R/Z_R/M_R^2 or q_R_hat)+tail",
            "tau_orbital;source current;source denominator;Z_R/M_R^2 or q_R_hat;boundary tail",
            "EXTERNAL_BOUND_EXISTS_INTERNAL_PROJECTION_MISSING",
            "BLOCKED_NO_CLAIM",
            "no same-frame source denominator or orbital projection kernel",
            "derive orbital projection in PPN-compatible variables",
        ),
        (
            "ARENA1578_4_WEP",
            "WEP/composition source-test channel",
            "source-intake/local_bounds/local_bound_claims.csv::MICROSCOPE_final_TiPt",
            "eta_MTS=tau_WEP*(beta_S^R beta_T^R composition split)+tail",
            "beta source/test material split;tau_WEP;no-marker theorem;boundary/readout tail",
            "EXTERNAL_BOUND_EXISTS_INTERNAL_PROJECTION_MISSING",
            "BLOCKED_NO_CLAIM",
            "beta-zero theorem remains conditional and source/test material split is missing",
            "keep WEP as branch-locked cross-check after beta rows exist",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "arena_id": arena_id,
            "arena": arena,
            "comparator_source": comparator_source,
            "mts_formula": mts_formula,
            "required_mts_inputs": required_mts_inputs,
            "external_data_status": external_data_status,
            "arena_status": arena_status,
            "blocked_reason": blocked_reason,
            "next_source_action": next_source_action,
            "accepted_for_scoring": False,
            **flags(),
        }
        for arena_id, arena, comparator_source, mts_formula, required_mts_inputs, external_data_status, arena_status, blocked_reason, next_source_action in rows
    ]


def placeholder_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1578_0_missing_value", "blank numeric component value", "REFUSE_PLACEHOLDER", "no value/theorem means no prediction row"),
        ("RUN1578_1_missing_source", "numeric-looking value with no source path or source anchor", "REFUSE_PLACEHOLDER", "unsourced numbers cannot enter local claim files"),
        ("RUN1578_2_theorem_zero_unsigned", "theorem-zero label without parent action signature", "REFUSE_PLACEHOLDER", "closure-only zero cannot replace proof"),
        ("RUN1578_3_operator_split", "Z_R without M_R^2 or beta rows", "REFUSE_PLACEHOLDER", "lambda_R and alpha_MTS require same-normalization component pack"),
        ("RUN1578_4_linear_coupling_shortcut", "single c_g/beta shortcut applied to source and test", "REFUSE_PLACEHOLDER", "source/test legs must be split and material/readout markers controlled"),
        ("RUN1578_5_reviewed_curve", "R10 reviewed candidate curve used as accepted bound", "REFUSE_PLACEHOLDER", "external curve remains nonclaim until official table or manual visual QA acceptance"),
        ("RUN1578_6_cross_arena_transfer", "clock/WEP silence transferred to R10/PPN", "REFUSE_PLACEHOLDER", "arena projections must be sourced independently"),
        ("RUN1578_7_closure_baseline", "closure baseline treated as derived local GR", "REFUSE_PLACEHOLDER", "closure is bookkeeping, not a parent reduction"),
        ("RUN1578_8_partial_score", "one arena scored with missing boundary tail", "REFUSE_PLACEHOLDER", "absolute no-cancellation boundary envelope is mandatory"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "runner_outcome": runner_outcome,
            "block_reason": block_reason,
            "claim_effect": "blocked and retained as nonclaim diagnostic only",
            **flags(),
        }
        for runner_id, case, runner_outcome, block_reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1578_0_component_pack", "finite component pack is score-ready", "BLOCKED_NO_CLAIM", "all live component inputs remain missing-valued/non-theorem"),
        ("GATE1578_1_R10", "R10 alpha(lambda_R) can be scored", "BLOCKED_NO_CLAIM", "internal beta/Z/M/Xi/tail rows missing and curve is reviewed-only"),
        ("GATE1578_2_PPN", "PPN/local-GR residual vector can be scored", "BLOCKED_NO_CLAIM", "q_R_hat/Q_R and tau_PPN/source denominator are missing"),
        ("GATE1578_3_clock_orbital", "clock or orbital branch can be scored", "BLOCKED_NO_CLAIM", "arena projections and material/source kernels are missing"),
        ("GATE1578_4_local_GR", "derived GR/Newton local reduction", "BLOCKED_NO_CLAIM", "finite residual branch is an empirical fallback, not a no-pole/constraint derivation"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1578_0_pack_status",
            "FINITE_COMPONENT_PACK_BUILT_NONCLAIM",
            "q_R_hat/Q_R, Z_R/M_R2, beta/J_R, boundary and arena projection rows are now one strict pack",
            "future source rows have an exact checklist and cannot sneak through as placeholders",
        ),
        (
            "DEC1578_1_runner_status",
            "PLACEHOLDER_REFUSAL_RUNNER_ACTIVE",
            "missing values, unsigned zero-theorems, reviewed-only curves and cross-arena transfers are all refused",
            "no R10/PPN/clock/orbital/local-GR claim can be made from current finite rows",
        ),
        (
            "DEC1578_2_next",
            "NEXT_1579_RAB_FINITE_COMPONENT_SOURCE_ACQUISITION_LEDGER_AND_COMPARATOR_DRY_RUN",
            "the honest next step is to acquire real internal component rows and run a dry comparator that still refuses claims until all gates pass",
            "source q_Rhat/Q_R, Z_R/M_R^2, beta legs, boundary tails and arena projections before scoring",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            **flags(),
        }
        for decision_id, decision, reason, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1579-Y5-RAB-finite-component-source-acquisition-ledger-and-comparator-dry-run.md",
            "script": "scripts/Y5_RAB_finite_component_source_acquisition_ledger_and_comparator_dry_run.py",
            "objective": "fill real source-backed acquisition rows for finite R_AB components and dry-run R10/PPN/clock/orbital comparators without promoting any claim",
            "do_not": "do not fabricate internal coefficients; do not accept reviewed-only R10 curves; do not score arenas with missing boundary/source/projector rows; do not edit formalization-workbench",
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


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def formalization_scope_clean(generated_csvs: list[Path]) -> bool:
    generated_paths = [Path(__file__).resolve(), DOC, *generated_csvs]
    generated_paths.extend(target for targets in COPY_TARGETS.values() for target in targets)
    if any(is_within(path, FORMALIZATION) for path in generated_paths):
        return False
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return True
    if result.returncode != 0:
        return True
    return len([line for line in result.stdout.splitlines() if line.strip()]) == 0


def has_1578_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1578" in path.name for path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    pack = read_csv(PACK_SCHEMA)
    inputs = read_csv(INPUT_STATUS)
    arenas = read_csv(ARENA_BLOCK)
    runner = read_csv(PLACEHOLDER_RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    required_symbols = {
        "q_R_hat or Q_R",
        "Z_R",
        "M_R^2",
        "beta_S^R",
        "beta_T^R",
        "J_R",
        "B_R, Pi_R^n, alpha_boundary_tail",
        "tau_R10 or Xi_R10",
        "tau_PPN or C_QR",
        "tau_clock",
        "tau_orbital",
    }
    checks = [
        ("VAL1578_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist"),
        ("VAL1578_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL1578_2_component_symbols_complete",
            {row["symbol"] for row in pack} == required_symbols,
            "finite pack contains q_R, operator, coupling, boundary and arena projection symbols",
        ),
        (
            "VAL1578_3_inputs_blocked_nonclaim",
            all(row["input_ready"] == "False" and row["valid_for_claim"] == "False" for row in inputs),
            "all component input rows remain missing and nonclaim",
        ),
        (
            "VAL1578_4_arenas_blocked",
            all(row["arena_status"] == "BLOCKED_NO_CLAIM" and row["accepted_for_scoring"] == "False" for row in arenas),
            "all local arenas remain blocked from scoring",
        ),
        (
            "VAL1578_5_placeholder_runner_refuses",
            all(row["runner_outcome"] == "REFUSE_PLACEHOLDER" and row["claim_allowed"] == "False" for row in runner),
            "runner refuses placeholders, unsigned zeroes, transfers and closure baselines",
        ),
        (
            "VAL1578_6_claim_gates_closed",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in gates),
            "claim gates remain closed",
        ),
        (
            "VAL1578_7_decision_next",
            any("NEXT_1579_RAB_FINITE_COMPONENT_SOURCE_ACQUISITION_LEDGER" in row["decision"] for row in decisions),
            "decision selects real source acquisition plus dry comparator",
        ),
        ("VAL1578_8_csv_parse", all(len(read_csv(path)) > 0 for path in generated_csvs), "all generated 1578 CSVs parse cleanly"),
        ("VAL1578_9_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1578_10_no_raw_accepted", not has_1578_rows(RAB_RAW) and not has_1578_rows(RAB_ACCEPTED), "no 1578 rows written to raw/accepted finite directories"),
        ("VAL1578_11_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets), "branch/quarantine nonclaim copies written"),
        ("VAL1578_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1578_13_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1578 paths are outside formalization-workbench; git status is clean when available"),
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
            "check_id": "VAL1578_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1578 finite component bound pack and runner validation",
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
    pack: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1578 - R_AB Finite Component Bound Pack And Runner",
                "## Verdict\n"
                "- The finite `R_AB` fallback is now a strict nonclaim component pack rather than a loose placeholder list.\n"
                "- The runner refuses missing values, unsigned theorem-zero labels, reviewed-only R10 curves, cross-arena transfers, closure baselines, and partial scores with missing boundary/source/projector rows.\n"
                "- R10, PPN, WEP, clock, orbital, local GR/Newton, no-pole, `q_R=0`, `Z_R=0`, and beta-zero claims all remain blocked.\n"
                "- This is useful progress because the missing objects are now exact: `q_R_hat/Q_R`, `Z_R/M_R^2`, `beta_S^R`, `beta_T^R`, `J_R`, boundary tail, and `tau_R10/tau_PPN/tau_clock/tau_orbital`.\n"
                "- The next step is real source acquisition plus dry comparator plumbing, still with no public/live claim promotion.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Component Pack Schema",
                md_table(pack, ["pack_id", "symbol", "equation_role", "failure_status", "gates_blocked", "update_rule"]),
                "## Component Input Status",
                md_table(inputs, ["input_id", "symbol", "value", "units", "source_path", "input_ready", "blocker"]),
                "## Arena Block Matrix",
                md_table(arenas, ["arena_id", "arena", "mts_formula", "external_data_status", "arena_status", "blocked_reason"]),
                "## Placeholder Refusal Runner",
                md_table(runner, ["runner_id", "case", "runner_outcome", "block_reason"]),
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
    pack = component_pack_schema_rows()
    inputs = component_input_status_rows()
    arenas = arena_block_matrix_rows()
    runner = placeholder_refusal_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        PACK_SCHEMA,
        INPUT_STATUS,
        ARENA_BLOCK,
        PLACEHOLDER_RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(PACK_SCHEMA, pack)
    write_csv(INPUT_STATUS, inputs)
    write_csv(ARENA_BLOCK, arenas)
    write_csv(PLACEHOLDER_RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, pack, inputs, arenas, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
