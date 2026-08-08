from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2912"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2912-Y5-R2FR-constraint-first-Z-elimination-or-first-DqZ-component-bound-under-AX1090.md"

SRC_2911_DOC = ROOT / "2911-Y5-R2FR-parent-field-chart-q-map-kernel-basis-or-finite-DqZ-norm-under-AX1090.md"
SRC_2911_NEXT = RESIDUALS / "P8_Y5_R2FR_2911_NEXT_TARGET.csv"
SRC_2911_QMAP = RESIDUALS / "P8_Y5_R2FR_2911_Q_MAP_DERIVATIVE_AUDIT.csv"
SRC_2911_DQZ = RESIDUALS / "P8_Y5_R2FR_2911_FINITE_DQZ_NORM_VECTOR.csv"
SRC_1674_CONSTRAINT = RESIDUALS / "P8_Y5_PARENT_QLOC_1674_CONSTRAINT_FIRST_ZERO_LEDGER.csv"
SRC_1674_DERIV = RESIDUALS / "P8_Y5_PARENT_QLOC_1674_DQZ_COMPONENT_DERIVATIVE_MATRIX.csv"
SRC_2883_SYNTH = RESIDUALS / "P8_Y5_R2FR_2883_CONSTRAINT_FIRST_SYNTHESIS.csv"
SRC_2838_CALC = RESIDUALS / "P8_Y5_R2FR_2838_AUXILIARY_ELIMINATION_CALCULUS.csv"
SRC_2751_ELIM = RESIDUALS / "P8_Y5_R2FR_2751_AUXILIARY_ELIMINATION_GATE.csv"
SRC_2743_FCC = RESIDUALS / "P8_Y5_R2FR_2743_FIRST_CLASS_CONSTRAINT_CONTRACT.csv"
SRC_2671_CERT = RESIDUALS / "P8_Y5_R2FR_VERTICAL_FIRST_CLASS_2671_CERTIFICATE_AUDIT.csv"
SRC_2671_OMEGA = RESIDUALS / "P8_Y5_R2FR_VERTICAL_FIRST_CLASS_2671_OMEGA_BRIDGE_AUDIT.csv"
SRC_2671_DEMOTE = RESIDUALS / "P8_Y5_R2FR_VERTICAL_FIRST_CLASS_2671_THEOREM_ZERO_DEMOTION_LEDGER.csv"
SRC_2213_RANK = RESIDUALS / "P8_Y5_PARENT_QLOC_2213_RANK_ZERO_SOURCE_CURRENT_THEOREM_ATTEMPT.csv"
SRC_2213_CLAUSE = RESIDUALS / "P8_Y5_PARENT_QLOC_2213_JA_BA_DQZ_CLAUSE_AUDIT.csv"
SRC_2214_DESCENT = RESIDUALS / "P8_Y5_PARENT_QLOC_2214_DQZ_SOURCE_DESCENT_PROOF_ATTEMPT.csv"
SRC_2214_COEFF = RESIDUALS / "P8_Y5_PARENT_QLOC_2214_ALGEBRAIC_RESIDUAL_COEFFICIENT_MAP.csv"
SRC_2214_ACQ = RESIDUALS / "P8_Y5_PARENT_QLOC_2214_NONCLAIM_COEFFICIENT_ACQUISITION_ROWS.csv"
SRC_2885_FACTOR = RESIDUALS / "P8_Y5_R2FR_2885_DQZ_FACTOR_VALUE_OR_BLOCKER_LEDGER.csv"
SRC_2886_COMPONENT = RESIDUALS / "P8_Y5_R2FR_2886_FIRST_FINITE_DQZ_COMPONENT_ROW_NONCLAIM.csv"
SRC_2611_PREMISE = RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2912_SOURCE_REGISTER.csv",
    "proof": RESIDUALS / "P8_Y5_R2FR_2912_CONSTRAINT_FIRST_PROOF_ATTEMPT.csv",
    "auxiliary": RESIDUALS / "P8_Y5_R2FR_2912_AUXILIARY_ELIMINATION_SIGNATURE_AUDIT.csv",
    "tangent": RESIDUALS / "P8_Y5_R2FR_2912_TANGENT_Q_FACTORIZATION_GATE.csv",
    "first_bound": RESIDUALS / "P8_Y5_R2FR_2912_FIRST_DQZ_COMPONENT_BOUND_INPUT_ROW.csv",
    "arenas": RESIDUALS / "P8_Y5_R2FR_2912_ARENA_IMPACT_MAP.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2912_RUNNER_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2912_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2912_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2912_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2912_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2912_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "proof_copy": PARENT_ACTION / "Constraint_first_Z_elimination_2912_NONCLAIM.csv",
    "bound_copy": LOCAL_BOUNDS / "DqZ_geometry_bound_input_2912_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2912_PARENT_AUX_CONSTRAINT_ORIGIN_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2912_00_2911_doc", SRC_2911_DOC, "NEXT2911_0_2912;constraint-first", "2911 handoff to constraint-first Z elimination"),
        ("SRC2912_01_2911_next", SRC_2911_NEXT, "NEXT2911_0_2912;C_Z(Phi)=0", "machine-readable 2912 target"),
        ("SRC2912_02_2911_qmap", SRC_2911_QMAP, "QMAP2911_7_verdict;Dq_Z_norm", "q/Dq blocker map"),
        ("SRC2912_03_2911_dqz", SRC_2911_DQZ, "DQZ2911_1_DqZ_geometry;DQZ2911_TOTAL", "finite DqZ vector"),
        ("SRC2912_04_1674_constraint", SRC_1674_CONSTRAINT, "CFZ1674_0_parent_constraint;CFZ1674_5_verdict", "constraint-first zero ledger"),
        ("SRC2912_05_1674_deriv", SRC_1674_DERIV, "DQM1674_0_coframe_metric;DQM1674_5_operator_norm", "Dq derivative matrix"),
        ("SRC2912_06_2883_synth", SRC_2883_SYNTH, "SYN2883_0_exact_constraint_law;SYN2883_5_current_verdict", "constraint-first synthesis"),
        ("SRC2912_07_2838_calc", SRC_2838_CALC, "CALC2838_0_aux_action;CALC2838_4_finite_case", "auxiliary elimination calculus"),
        ("SRC2912_08_2751_elim", SRC_2751_ELIM, "ELIM2751_0_E_Lambda;ELIM2751_4_current_verdict", "auxiliary elimination gate"),
        ("SRC2912_09_2743_fcc", SRC_2743_FCC, "FCC2743_0_parent_phase_space;FCC2743_8_no_GR_import", "first-class constraint contract"),
        ("SRC2912_10_2671_cert", SRC_2671_CERT, "VFC2671_1_parent_symplectic_package;VFC2671_9_verdict", "vertical first-class demotion"),
        ("SRC2912_11_2671_omega", SRC_2671_OMEGA, "OMB2671_0_category_rule;OMB2671_3_verdict", "Omega bridge guard"),
        ("SRC2912_12_2671_demote", SRC_2671_DEMOTE, "DEM2671_0_vertical;DEM2671_1_theorem_zero_routes", "theorem-zero demotion ledger"),
        ("SRC2912_13_2213_rank", SRC_2213_RANK, "RZS2213_0_strict_euler_identity;RZS2213_4_verdict", "rank-zero algebraic route"),
        ("SRC2912_14_2213_clause", SRC_2213_CLAUSE, "JBD2213_1_J_zero;JBD2213_6_verdict", "J/B/DqZ clause audit"),
        ("SRC2912_15_2214_descent", SRC_2214_DESCENT, "DSD2214_0_exact_chain_rule;DSD2214_5_verdict", "DqZ source descent proof attempt"),
        ("SRC2912_16_2214_coeff", SRC_2214_COEFF, "CM2214_5_E_DqZ;CM2214_7_verdict", "algebraic residual coefficient map"),
        ("SRC2912_17_2214_acq", SRC_2214_ACQ, "ACQ2214_5_EDqZ;ACQ2214_7_LPPN", "coefficient acquisition rows"),
        ("SRC2912_18_2885_factor", SRC_2885_FACTOR, "DQZF2885_0_Dq_Z_norm;DQZF2885_2_C_Obs_e", "DqZ factor blocker rows"),
        ("SRC2912_19_2886_component", SRC_2886_COMPONENT, "DQC2886_0_E_DqZ_coframe;MISSING_COMPONENT_VALUES", "first finite DqZ component"),
        ("SRC2912_20_2611_premise", SRC_2611_PREMISE, "PRE2611_0_q_map;PRE2611_8_verdict", "matter descent q-map premise"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def proof_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CFP2912_0_exact_conditional",
            "constraint-first Z elimination theorem",
            "If parent equations impose C_Z(Phi)=0 before q/matter/readout, allowed variations satisfy delta C_Z=0, q|C_Z=qbar(Q_vis), and source/readout/boundary terms are Q_vis-basic or zero, then Dq_Z_norm=0 by absence.",
            "EXACT_CONDITIONAL_THEOREM",
            "would set Dq_Z_norm, E_DqZ_geometry/source/readout and the Z-side source residual to theorem-zero",
            "all premise rows must close in one parent branch",
        ),
        (
            "CFP2912_1_magic_multiplier_guard",
            "lambda_Z insertion is not a derivation",
            "Adding lambda_Z Z or lambda_Z C_Z by hand only proves an inserted multiplier can impose zero; it does not prove MTS parent dynamics require it.",
            "GUARDRAIL_ACTIVE",
            "prevents closure-only plateau axiom in new clothing",
            "parent action origin/signature of C_Z is missing",
        ),
        (
            "CFP2912_2_second_class_route",
            "second-class/algebraic auxiliary route",
            "S_Z=int mu lambda_A (Z^A-C^A[Q_vis,theta,top]) eliminates Z algebraically before q if the block is parent-owned and non-derivative.",
            "BEST_CONDITIONAL_ROUTE_UNSIGNED",
            "least-scrutiny route because no hidden propagating pole is introduced",
            "parent action image, units, multiplier stress and compatibility source terms are unsigned",
        ),
        (
            "CFP2912_3_first_class_route",
            "first-class/gauge route",
            "A first-class route requires parent Omega, C_Z, DC_Z, v_Z=Omega^{-1}(DC_Z)^dagger, bracket closure, zero/proper boundary charge and degree count.",
            "ROUTE_DEMOTED_FOR_CURRENT_MTS",
            "would make Z a gauge/constraint direction rather than a physical residual",
            "2671 shows the symplectic package and boundary/bracket/degree proofs are missing",
        ),
        (
            "CFP2912_4_rank_zero_algebraic",
            "rank-zero algebraic identity",
            "M_AB Z^B = J_A + B_A + C_A^CDB + R_A^src/readout/projector can replace a plateau axiom if M_AB and all forcing terms are parent-owned.",
            "CONDITIONAL_ROUTE_RETAINED",
            "turns local silence into algebraic elimination plus finite residual coefficients",
            "M_AB lock, J_A, B_A, CDB, Dq_Z and arena projections remain unsigned",
        ),
        (
            "CFP2912_5_current_verdict",
            "constraint-first theorem for current MTS",
            "current MTS proves C_Z eliminates Z before q/matter/readout in a parent-owned branch",
            "NOT_DERIVED_CURRENT_MTS",
            "no local GR/Newton claim",
            "parent constraint origin, tangent proof, q factorization, source/readout descent and boundary no-flux do not close",
        ),
    ]
    return [
        add_common(
            {
                "proof_id": proof_id,
                "target": target,
                "statement": statement,
                "current_status": status,
                "would_prove": effect,
                "blocking_gap": blocker,
                "theorem_zero_adopted": False,
            }
        )
        for proof_id, target, statement, status, effect, blocker in specs
    ]


def auxiliary_rows() -> list[dict[str, Any]]:
    specs = [
        ("AUX2912_0_parent_origin", "parent action image contains S_Z", "S_parent includes S_Z from MTS primitives, not from a late closure addition", "MISSING_PARENT_CONSTRAINT_ORIGIN", "magic multiplier guard keeps zero unclaimed"),
        ("AUX2912_1_multiplier_equation", "delta_lambda S_Z", "delta S/delta lambda_A = Z^A-C^A[Q_vis,theta,top]=0", "FORMAL_PASS_WITHIN_CANDIDATE", "only useful if AUX2912_0 signs"),
        ("AUX2912_2_Z_equation", "delta_Z S_total", "lambda_A + J_A + B_A + C_A^CDB + R_A^src/readout/projector = 0", "PASS_ONLY_IF_FORCING_ZERO_OR_BOUNDED", "surviving forcing makes finite lambda/Z-source residual"),
        ("AUX2912_3_multiplier_stress", "constraint stress silence", "constraint block contributes no local stress/source after elimination only if lambda_A=0 or common q-basic/proper", "UNSIGNED", "otherwise the constraint itself sources metric/source equations"),
        ("AUX2912_4_non_derivative", "no hidden principal symbol", "S_Z has no kinetic/derivative Z operator outside the declared algebraic block", "CDB_PARALLEL_BLOCKER_LIVE", "derivative/domain/boundary commutator can reopen finite range"),
        ("AUX2912_5_units_rank", "rank/units/eigenbasis", "M_AB or compatibility Jacobian has declared units, rank and null projector", "MISSING_PARENT_SIGNATURE", "no source-ready numeric bound without this"),
        ("AUX2912_6_verdict", "auxiliary elimination for current MTS", "Z is eliminated by a parent-owned second-class auxiliary block before q", "AUXILIARY_ELIMINATION_NOT_PARENT_SIGNED", "use bound-input rows; do not claim theorem zero"),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "clause": clause,
                "required_statement": statement,
                "current_status": status,
                "if_open": if_open,
                "parent_signed": False,
                "valid_zero_credit": False,
            }
        )
        for audit_id, clause, statement, status, if_open in specs
    ]


def tangent_rows() -> list[dict[str, Any]]:
    specs = [
        ("TQF2912_0_tangent_space", "allowed variations satisfy delta C_Z=0", "MISSING_TANGENT_SPACE_PROOF", "without this, variations can move the allegedly eliminated coordinate"),
        ("TQF2912_1_q_factorization", "q(Phi)|C_Z=0=qbar(Q_vis) with no Z argument", "MISSING_Q_FACTORISATION_PROOF", "without this, Z can leak through q despite constraint notation"),
        ("TQF2912_2_matter_source", "S_matter, J_H, source normalization and worldtube use Q_vis only after restriction", "MISSING_MATTER_SOURCE_READOUT_DESCENT", "without this, J_A can source eliminated Z"),
        ("TQF2912_3_readout_marker", "clocks, EM, photons, PPN/orbit readouts and markers are Q_vis-basic or fixed", "NO_MARKER_READOUT_CLOSURE_UNSIGNED", "without this, DqZ_readout remains live"),
        ("TQF2912_4_boundary_projector", "boundary/projector/source support is proper, zero, bounded or included in Q_vis before Dq_Z is evaluated", "MISSING_BOUNDARY_NO_FLUX", "without this, edge/projector terms source local tests"),
        ("TQF2912_5_norm_order", "q/Z norms and tangent normalization are declared before any bound", "MISSING_NORM_CONVENTIONS", "without this, Dq_Z_norm is a symbolic label not an operator bound"),
        ("TQF2912_6_verdict", "constraint-first Dq_Z zero application", "CONSTRAINT_FIRST_APPLICATION_BLOCKED", "Dq_Z_norm remains finite nonclaim input"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "gate": gate,
                "current_status": status,
                "failure_if_open": failure,
                "clause_met": False,
                "theorem_zero_adopted": False,
            }
        )
        for gate_id, gate, status, failure in specs
    ]


def first_bound_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "BDQZ2912_0_DqZ_geometry",
            "DqZ_geometry",
            "first DqZ component bound input row: geometry/coframe/metric/measure derivative leakage",
            "dimensionless_frame_or_metric_response",
            "E_DqZ_geometry <= Pi_geom*C_Obs_e*Dq_Z_norm*N_Z + E_shadow + E_boundary_geom + E_readout_geom",
            "C_Obs_e;Dq_Z_norm;N_Z;Pi_geom;q/e/Z norms;observed coframe functor;no-shadow-frame certificate;boundary/readout tails",
            "PPN;clock;orbital;local_GR",
        ),
        (
            "BDQZ2912_1_DqZ_source",
            "DqZ_source",
            "source-current/worldtube derivative leakage input row",
            "source-current-normalized",
            "E_DqZ_source <= Pi_source*(Dq_Z_norm*N_Z + Delta_w_abs + epsilon_JM_descent_abs + boundary_source)",
            "source-current owner;Pi_M equality;worldtube support;no-source-slot;source projection units",
            "Newton;WEP;R10;orbital",
        ),
        (
            "BDQZ2912_2_DqZ_readout",
            "DqZ_readout",
            "clock/EM/photon/orbit readout derivative leakage input row",
            "arena_specific_readout_units",
            "E_DqZ_readout <= Pi_readout*(Dq_Z_norm*N_Z + epsilon_theta_marker + readout_radiative_tail)",
            "readout functor;theta/no-marker theorem;clock/EM standards;arena units",
            "clock;EM;WEP;PPN;orbital",
        ),
        (
            "BDQZ2912_3_DqZ_boundary",
            "DqZ_boundary_projector",
            "boundary/projector/source-support leakage input row",
            "boundary_or_projector_units",
            "E_DqZ_boundary <= Pi_boundary*(boundary_flux_Z + projector_commutator_Z + source_support_tail)",
            "boundary primitive;proper collar proof;projector commutator;source support map;units",
            "R10;orbital;PPN;local_GR",
        ),
    ]
    return [
        add_common(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "formula_or_bound": formula,
                "required_inputs": required,
                "current_value": "MISSING_PARENT_INPUT",
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "source_paths": ";".join(str(p) for p in [SRC_2911_DQZ, SRC_2885_FACTOR, SRC_2886_COMPONENT, SRC_2214_ACQ]),
                "arena_targets": arenas,
                "status": "BOUND_INPUT_ROW_STAGED_NONCLAIM",
                "valid_for_claim_rule": "only true after all required inputs are sourced, numeric/unit-locked, and no MISSING markers remain",
            }
        )
        for bound_id, symbol, definition, units, formula, required, arenas in specs
    ]


def arena_rows() -> list[dict[str, Any]]:
    specs = [
        ("ARENA2912_0_Newton", "Newton/local GM", "constraint-first would remove Z before source normalization; otherwise DqZ_source and algebraic forcing enter", "BLOCKED_NONCLAIM", "no GM/G_N absorption"),
        ("ARENA2912_1_PPN", "PPN", "DqZ_geometry is first local metric/coframe bound row; PPN still needs projection units", "BOUND_INPUT_STAGED", "not a prediction row"),
        ("ARENA2912_2_WEP", "WEP", "DqZ_source/readout plus no-source-slot/marker tails remain composition-sensitive", "SOURCE_LANGUAGE_OPEN", "coupling throat remains explicit"),
        ("ARENA2912_3_R10", "R10", "boundary/projector and source/test split must be sourced before alpha(lambda)", "HELD_NONCLAIM", "no bound anchor shortcut"),
        ("ARENA2912_4_clock_EM", "clock/EM", "readout/theta marker row is required before charge/clock claims", "READOUT_MARKER_OPEN", "cite/source later"),
        ("ARENA2912_5_orbital", "orbital", "geometry/source/boundary components must share same compact source/worldtube branch", "SOURCE_SUPPORT_OPEN", "no orbit score yet"),
        ("ARENA2912_6_local_GR", "local GR/Newton reduction", "local GR requires constraint-first theorem or all finite DqZ/source/Y5/Y6 rows bounded below tolerance", "BLOCKED_NONCLAIM", "2912 does not prove GR reduction"),
    ]
    return [
        add_common(
            {
                "arena_id": arena_id,
                "arena": arena,
                "effect": effect,
                "current_status": status,
                "guardrail": guardrail,
            }
        )
        for arena_id, arena, effect, status, guardrail in specs
    ]


def runner_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_sources_ready = all(bool(row["path_exists"]) and bool(row["anchors_found"]) for row in source_rows)
    specs = [
        ("RUN2912_0_sources", "SOURCE_AUDIT_COMPLETE" if all_sources_ready else "SOURCE_AUDIT_HAS_BLOCKERS", "all cited source paths and anchors", all_sources_ready, "source evidence checked"),
        ("RUN2912_1_constraint_theorem", "CONSTRAINT_FIRST_THEOREM_ATTEMPTED_NOT_SIGNED", "C_Z origin, tangent condition, q factorization, source/readout/boundary silence", False, "premises do not close in one parent branch"),
        ("RUN2912_2_magic_guard", "MAGIC_MULTIPLIER_REJECTED", "lambda_Z insertion test", True, "adding a multiplier is not accepted as derivation"),
        ("RUN2912_3_auxiliary_route", "SECOND_CLASS_ROUTE_RETAINED_CONDITIONAL", "parent-owned algebraic auxiliary block", False, "best route but parent action image unsigned"),
        ("RUN2912_4_bound_rows", "FIRST_DQZ_BOUND_ROWS_STAGED_NONCLAIM", "DqZ_geometry/source/readout/boundary inputs", False, "required numeric/source inputs missing"),
        ("RUN2912_5_next", "PARENT_AUX_CONSTRAINT_ORIGIN_SELECTED", "2913 target", False, "next proof must source C_Z rather than re-state it"),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "status": status,
                "required_components": required,
                "components_evaluable": evaluable,
                "reason": reason,
            }
        )
        for runner_id, status, required, evaluable, reason in specs
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2912_0_conditional_constraint", "constraint-first theorem statement is mathematically valid", "PASS_CONDITIONAL_ONLY", "if all premises close, Z is absent before q/matter/readout", True),
        ("CG2912_1_parent_CZ", "current MTS derives C_Z(Phi)=0 from parent action", "BLOCKED_NONCLAIM", "parent constraint origin/signature missing", False),
        ("CG2912_2_second_class_aux", "second-class auxiliary block is parent-owned", "BLOCKED_NONCLAIM", "S_Z block is candidate/contract only", False),
        ("CG2912_3_tangent_q", "allowed variations satisfy delta C_Z=0 and q factorizes", "BLOCKED_NONCLAIM", "tangent-space and q-factorization proofs missing", False),
        ("CG2912_4_source_readout", "matter/source/readout/boundary are silent after restriction", "BLOCKED_NONCLAIM", "source/readout descent and boundary no-flux remain unsigned", False),
        ("CG2912_5_DqZ_zero", "Dq_Z_norm=0 from constraint-first branch", "BLOCKED_NONCLAIM", "constraint-first application fails current corpus", False),
        ("CG2912_6_bound_score", "first DqZ bound row is score-ready", "BLOCKED_NONCLAIM", "no numeric/source-backed upper bound", False),
        ("CG2912_7_local_GR_Newton", "local GR/Newton follows after 2912", "BLOCKED_NONCLAIM", "2912 stages proof contract and bound rows only", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": status,
                "reason": reason,
                "gate_pass": gate_pass,
            }
        )
        for gate_id, claim, status, reason, gate_pass in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2912_0_result", "CONSTRAINT_FIRST_NOT_DERIVED", "The theorem route is clean but current MTS does not source C_Z, tangent restriction, q factorization, source/readout descent and boundary silence together.", "do not promote Dq_Z_norm=0"),
        ("DEC2912_1_best_route", "SECOND_CLASS_AUXILIARY_ROUTE_BEST", "A parent-owned algebraic auxiliary block is less vulnerable to gauge/first-class objections than calling a visible residual gauge.", "derive parent origin of S_Z next"),
        ("DEC2912_2_guard", "MAGIC_MULTIPLIER_REFUSED", "lambda_Z C_Z is only evidence if it is generated by the parent action, not appended to win the proof.", "keep closure-only status until parent origin is shown"),
        ("DEC2912_3_fallback", "FIRST_DQZ_GEOMETRY_BOUND_STAGED", "If the constraint origin does not close, the first local metric/coframe component now has explicit coefficient/source requirements.", "fill or source DqZ_geometry later"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2912_0_2913",
                "selection_status": "selected_primary",
                "target_file": "2913-Y5-R2FR-parent-auxiliary-constraint-origin-or-DqZ-geometry-bound-fill-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_parent_auxiliary_constraint_origin_or_DqZ_geometry_bound_fill_under_AX1090_2913.py",
                "task": "try to derive the parent origin/signature of the second-class auxiliary constraint block S_Z; if it fails, convert DqZ_geometry into a stricter source-acquisition row",
                "success_condition": "parent action image supplies S_Z, multiplier units, compatibility map C^A[Q_vis], no-derivative grammar, zero multiplier stress condition and boundary/source protection",
                "fallback_condition": "DqZ_geometry bound row gets a complete acquisition contract for C_Obs_e, Dq_Z_norm, N_Z, Pi_geom, q/e/Z norms and source paths",
                "guardrails": "no magic multiplier; no post-readout deletion; no closure axiom; no plateau axiom; no empirical scoring; no GM/G_N absorption; no GitHub; no formalization-workbench edits",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("proof_copy", OUTPUTS["proof"], BRANCH_OUTPUTS["proof_copy"]),
        ("bound_copy", OUTPUTS["first_bound"], BRANCH_OUTPUTS["bound_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination in specs:
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "destination_path": str(destination),
                    "source_exists": source.exists(),
                    "destination_exists": destination.exists(),
                    "destination_parses": csv_parses(destination),
                }
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    proof_rows_: list[dict[str, Any]],
    auxiliary_rows_: list[dict[str, Any]],
    tangent_rows_: list[dict[str, Any]],
    bound_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    include_doc_check: bool,
) -> list[dict[str, Any]]:
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_outputs_with_validation = [*csv_outputs, OUTPUTS["validation"]]
    proof_verdict = next(row for row in proof_rows_ if row["proof_id"] == "CFP2912_5_current_verdict")
    aux_verdict = next(row for row in auxiliary_rows_ if row["audit_id"] == "AUX2912_6_verdict")
    tangent_verdict = next(row for row in tangent_rows_ if row["gate_id"] == "TQF2912_6_verdict")
    local_claim = next(row for row in claim_rows_ if row["gate_id"] == "CG2912_7_local_GR_Newton")
    required_bound_symbols = {"DqZ_geometry", "DqZ_source", "DqZ_readout", "DqZ_boundary_projector"}
    bound_symbols = {str(row["symbol"]) for row in bound_rows_}
    checks = [
        ("VAL2912_0_source_paths_exist", all(bool(row["path_exists"]) for row in source_rows), "all cited source paths exist"),
        ("VAL2912_1_source_anchors_found", all(bool(row["anchors_found"]) for row in source_rows), "all source anchors found"),
        ("VAL2912_2_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs_with_validation if path.exists()), "generated CSV outputs parse cleanly"),
        ("VAL2912_3_constraint_not_promoted", proof_verdict["current_status"] == "NOT_DERIVED_CURRENT_MTS" and not bool(proof_verdict["theorem_zero_adopted"]), "constraint-first theorem remains unpromoted"),
        ("VAL2912_4_auxiliary_not_promoted", aux_verdict["current_status"] == "AUXILIARY_ELIMINATION_NOT_PARENT_SIGNED" and not bool(aux_verdict["parent_signed"]), "auxiliary block remains parent-unsigned"),
        ("VAL2912_5_tangent_blocked", tangent_verdict["current_status"] == "CONSTRAINT_FIRST_APPLICATION_BLOCKED", "tangent/q-factorization gate remains blocked"),
        ("VAL2912_6_bound_rows_complete", required_bound_symbols.issubset(bound_symbols), "first DqZ bound-input rows staged"),
        (
            "VAL2912_7_claim_gates_safe",
            local_claim["gate_status"] == "BLOCKED_NONCLAIM"
            and all(not bool(row["claim_allowed"]) and not bool(row["valid_for_claim"]) for row in claim_rows_),
            "local GR/Newton and empirical claims remain blocked",
        ),
        ("VAL2912_8_next_target_selected", next_rows_[0]["route_id"] == "NEXT2912_0_2913" and bool(next_rows_[0]["selected"]), "2913 parent auxiliary constraint origin target selected"),
        ("VAL2912_9_branch_copies_parse", all(bool(row["destination_exists"]) and bool(row["destination_parses"]) for row in branch_rows_), "branch copies exist and parse"),
        ("VAL2912_10_no_formalization_outputs", not any(is_under(path, FORMALIZATION) for path in [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC]), "no generated output path is inside formalization-workbench"),
        ("VAL2912_11_doc_written", DOC.exists() if include_doc_check else True, "markdown checkpoint exists"),
    ]
    rows: list[dict[str, Any]] = [
        {
            "validation_id": validation_id,
            "status": bool(status),
            "detail": detail,
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
        for validation_id, status, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2912_OVERALL",
            "status": all(bool(row["status"]) for row in rows),
            "detail": "2912 validation overall",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    proof_rows_: list[dict[str, Any]],
    auxiliary_rows_: list[dict[str, Any]],
    tangent_rows_: list[dict[str, Any]],
    bound_rows_: list[dict[str, Any]],
    arena_rows_: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2912_OVERALL")
    text = f"""# 2912 - Y5/R2FR Constraint-First Z Elimination Or First DqZ Component Bound Under AX1090

Status: `Y5_R2FR_2912_constraint_first_not_derived_magic_multiplier_refused_DqZ_bound_rows_staged_2913_next`

Claim ceiling: `constraint_first_elimination_nonclaim_only_no_parent_CZ_no_DqZ_zero_no_local_GR_no_Newton_no_PPN_no_R10_no_GitHub_claim`

Generated UTC: `{RUN_UTC}`

## Summary

2912 attacks the cleanest possible route out of the `Dq_Z_norm` bottleneck: eliminate `Z` before the visible quotient, matter action, source normalization and readouts are formed. If a parent-owned constraint `C_Z(Phi)=0` really removes `Z` first, then `Dq_Z_norm=0` follows by absence, not by a plateau axiom.

The exact conditional theorem is valid. But current MTS does not yet derive the parent origin of `C_Z`, the allowed tangent-space restriction `delta C_Z=0`, q-factorization on the constraint surface, source/readout descent, or boundary/projector silence in one branch.

The important guard is this: inserting `lambda_Z C_Z` by hand is not a derivation. A multiplier is only evidence if it comes from the parent action. Therefore 2912 keeps the second-class auxiliary route as the best route, but nonclaim, and stages the first `DqZ_geometry` bound-input row for later source acquisition.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "anchors_found", "role", "missing_anchors"])}

## Constraint-First Proof Attempt

{md_table(proof_rows_, ["proof_id", "target", "current_status", "statement", "would_prove", "blocking_gap", "theorem_zero_adopted", "valid_for_claim"])}

## Auxiliary Elimination Signature Audit

{md_table(auxiliary_rows_, ["audit_id", "clause", "current_status", "required_statement", "if_open", "parent_signed", "valid_zero_credit", "valid_for_claim"])}

## Tangent/q-Factorization Gate

{md_table(tangent_rows_, ["gate_id", "gate", "current_status", "failure_if_open", "clause_met", "theorem_zero_adopted", "valid_for_claim"])}

## First DqZ Component Bound Input Rows

{md_table(bound_rows_, ["bound_id", "symbol", "definition", "units", "formula_or_bound", "required_inputs", "current_value", "upper_bound", "arena_targets", "status", "valid_for_claim"])}

## Arena Impact Map

{md_table(arena_rows_, ["arena_id", "arena", "effect", "current_status", "guardrail", "valid_for_claim"])}

## Runner Status

{md_table(runner_rows_, ["runner_id", "status", "required_components", "components_evaluable", "reason", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows_, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"])}

## Decision Ledger

{md_table(decision_rows_, ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(next_rows_, ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows_, ["copy_id", "source_path", "destination_path", "destination_exists", "destination_parses", "valid_for_claim"])}

## Validation

{md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim"])}

Validation overall: `{overall["status"]}`.

## Interpretation

This narrows the GR-reduction problem again. The question is no longer "can we set the local residual to zero?" It is "does the parent action generate the auxiliary constraint block that removes the residual before visible physics is built?"

That is the right sort of hard problem. If the answer becomes yes, `Dq_Z_norm=0` is not a fitted empirical patch. If the answer stays no, the first metric/coframe leak row is now ready to be sourced as a finite bound input.

## Not Claimed

- `C_Z(Phi)=0` is not derived from the current MTS parent action.
- `lambda_Z C_Z` is not accepted as proof unless parent-origin is supplied.
- `Dq_Z_norm=0`, `DqZ_geometry=0`, source/readout descent and boundary silence are not proved.
- Newton, PPN, R10, WEP, clock/EM, orbital or local-GR reduction is not claimed.
- No public/GitHub action is implied.
- No file in `formalization-workbench` is modified by this checkpoint.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    proof_rows_ = proof_rows()
    auxiliary_rows_ = auxiliary_rows()
    tangent_rows_ = tangent_rows()
    bound_rows_ = first_bound_rows()
    arena_rows_ = arena_rows()
    runner_rows_ = runner_rows(source_rows)
    claim_rows_ = claim_rows()
    decision_rows_ = decision_rows()
    next_rows_ = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["proof"], proof_rows_)
    write_csv(OUTPUTS["auxiliary"], auxiliary_rows_)
    write_csv(OUTPUTS["tangent"], tangent_rows_)
    write_csv(OUTPUTS["first_bound"], bound_rows_)
    write_csv(OUTPUTS["arenas"], arena_rows_)
    write_csv(OUTPUTS["runner"], runner_rows_)
    write_csv(OUTPUTS["claims"], claim_rows_)
    write_csv(OUTPUTS["decision"], decision_rows_)
    write_csv(OUTPUTS["next"], next_rows_)

    branch_rows_ = branch_rows()
    write_csv(OUTPUTS["branches"], branch_rows_)

    validation_rows_ = validation_rows(
        source_rows,
        proof_rows_,
        auxiliary_rows_,
        tangent_rows_,
        bound_rows_,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=False,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        proof_rows_,
        auxiliary_rows_,
        tangent_rows_,
        bound_rows_,
        arena_rows_,
        runner_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    validation_rows_ = validation_rows(
        source_rows,
        proof_rows_,
        auxiliary_rows_,
        tangent_rows_,
        bound_rows_,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=True,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        proof_rows_,
        auxiliary_rows_,
        tangent_rows_,
        bound_rows_,
        arena_rows_,
        runner_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2912_OVERALL")
    if not bool(overall["status"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
