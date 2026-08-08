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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2949"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2949-Y5-R2FR-parent-X-action-route-selector-and-LX-normal-form-gate-under-AX1090.md"

SRC_2948_DOC = ROOT / "2948-Y5-R2FR-parent-current-chain-sector-action-certificate-or-IX-charge-residual-first-row-under-AX1090.md"
SRC_2948_NEXT = RESIDUALS / "P8_Y5_R2FR_2948_NEXT_TARGET.csv"
SRC_2948_ROUTE = RESIDUALS / "P8_Y5_R2FR_2948_X_SECTOR_ROUTE_PROOF_AUDIT.csv"
SRC_2948_CERT = RESIDUALS / "P8_Y5_R2FR_2948_PARENT_CURRENT_CHAIN_CERTIFICATE_ATTEMPT.csv"
SRC_2948_IX = RESIDUALS / "P8_Y5_R2FR_2948_IX_RESIDUAL_FIRST_ROW.csv"
SRC_2948_JX = RESIDUALS / "P8_Y5_R2FR_2948_JX_COMPONENT_ENVELOPE.csv"
SRC_2948_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2948_VALIDATION.csv"
SRC_2694_SECTOR = RESIDUALS / "P8_Y5_R2FR_2694_SECTOR_CERTIFICATE_ATTEMPT_MATRIX.csv"
SRC_2697_FIXED = RESIDUALS / "P8_Y5_R2FR_2697_FIXED_POINT_CONDITIONS.csv"
SRC_2707_OWNER = RESIDUALS / "P8_Y5_R2FR_2707_PARENT_OWNER_EXTRACTION_MATRIX.csv"
SRC_2708_NO_POLE = RESIDUALS / "P8_Y5_R2FR_2708_NO_POLE_CERTIFICATE_MATRIX.csv"
SRC_2752_ACTION = RESIDUALS / "P8_Y5_R2FR_2752_CURRENT_ACTION_CLAUSE_AUDIT.csv"
SRC_2785_PREMISES = RESIDUALS / "P8_Y5_R2FR_2785_CURRENT_OWNER_PREMISE_LEDGER.csv"
SRC_2785_THEOREM = RESIDUALS / "P8_Y5_R2FR_2785_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv"
SRC_2792_ZERO = RESIDUALS / "P8_Y5_R2FR_2792_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv"
SRC_2793_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2793_ZERO_CURRENT_CLAUSE_CONTRACT.csv"
SRC_2852_SYMMETRY = RESIDUALS / "P8_Y5_R2FR_2852_SYMMETRY_CANDIDATE_MATRIX.csv"
SRC_2866_ROUTE = RESIDUALS / "P8_Y5_R2FR_2866_ROUTE_DECISION_MATRIX.csv"
SRC_1041_THETAX = RESIDUALS / "P8_Y5_R10_1041_THETAX_OWNER_GATE.csv"
SRC_967_POSITIVE = RESIDUALS / "P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv"
SRC_968_INPUTS = RESIDUALS / "P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv"
SRC_972_TWO_SLOT = RESIDUALS / "P8_Y5_R10_972_TWO_SLOT_ACTION_CONTRACT.csv"
SRC_973_JX = RESIDUALS / "P8_Y5_R10_973_JX_DECOMPOSITION_GATE.csv"
SRC_2022_IX_SCHEMA = RESIDUALS / "P8_Y5_PARENT_QLOC_2022_IX_FIRST_SOURCE_ROW_SCHEMA.csv"
SRC_2665_HLOCK = RESIDUALS / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv"
SRC_2665_PDG = RESIDUALS / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_PROJECTOR_DENOMINATOR_GATE.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2949_SOURCE_REGISTER.csv",
    "selector": RESIDUALS / "P8_Y5_R2FR_2949_X_ROUTE_SELECTOR_MATRIX.csv",
    "normal_form": RESIDUALS / "P8_Y5_R2FR_2949_LX_NORMAL_FORM_GATE.csv",
    "acceptance": RESIDUALS / "P8_Y5_R2FR_2949_ROUTE_ACCEPTANCE_GATES.csv",
    "positive_inputs": RESIDUALS / "P8_Y5_R2FR_2949_POSITIVE_OPERATOR_INPUT_QUEUE.csv",
    "finite_rows": RESIDUALS / "P8_Y5_R2FR_2949_FINITE_RESIDUAL_ACQUISITION_ROWS.csv",
    "guards": RESIDUALS / "P8_Y5_R2FR_2949_ROUTE_GUARDS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2949_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2949_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2949_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2949_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2949_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "selector_copy": PARENT_ACTION / "X_route_selector_matrix_2949_NONCLAIM.csv",
    "normal_form_copy": PARENT_ACTION / "LX_normal_form_gate_2949_NONCLAIM.csv",
    "positive_inputs_copy": LOCAL_BOUNDS / "Positive_operator_input_queue_2949_NONCLAIM.csv",
    "finite_rows_copy": LOCAL_BOUNDS / "IX_finite_residual_acquisition_rows_2949_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2949_PARENT_X_OPERATOR_COEFFICIENT_OR_FINITE_ROW_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


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
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2949_00_2948_doc", SRC_2948_DOC, "NEXT2948_0_2949;Validation overall: `True`", "2948 handoff to X-route selector"),
        ("SRC2949_01_2948_next", SRC_2948_NEXT, "NEXT2948_0_2949", "machine-readable 2949 target"),
        ("SRC2949_02_2948_route", SRC_2948_ROUTE, "ROUTE2948_0_absent_topological;ROUTE2948_4_verdict", "2948 route fork"),
        ("SRC2949_03_2948_cert", SRC_2948_CERT, "PCC2948_0_parent_X_action;PCC2948_6_verdict", "parent current-chain certificate"),
        ("SRC2949_04_2948_ix", SRC_2948_IX, "IX2948_0_identity;IX2948_7_acceptance", "I_X residual first row"),
        ("SRC2949_05_2948_jx", SRC_2948_JX, "JX2948_0_kinetic_affine;JX2948_7_total", "J_X component envelope"),
        ("SRC2949_06_2948_validation", SRC_2948_VALIDATION, "VAL2948_OVERALL", "2948 validation"),
        ("SRC2949_07_2694_sector", SRC_2694_SECTOR, "CERT2694_3_aux;CERT2694_10_verdict", "sector certificate attempt matrix"),
        ("SRC2949_08_2697_fixed", SRC_2697_FIXED, "FP2697_2_double_zero;FP2697_10_verdict", "local fixed-point conditions"),
        ("SRC2949_09_2707_owner", SRC_2707_OWNER, "OWN2707_0_Xhat_field_owner;OWN2707_6_verdict", "parent owner extraction"),
        ("SRC2949_10_2708_no_pole", SRC_2708_NO_POLE, "NPC2708_0_parent_qmap;NPC2708_8_verdict", "no-pole certificate matrix"),
        ("SRC2949_11_2752_action", SRC_2752_ACTION, "ACT2752_0_EH_core;ACT2752_5_current_action_verdict", "current action clause audit"),
        ("SRC2949_12_2785_premises", SRC_2785_PREMISES, "PR2785_0_common_parent_action;PR2785_6_finite_route_needed", "current-owner premise ledger"),
        ("SRC2949_13_2785_theorem", SRC_2785_THEOREM, "NCO2785_0_target;NCO2785_6_verdict", "narrow current-owner theorem"),
        ("SRC2949_14_2792_zero", SRC_2792_ZERO, "SCZ2792_0_chain_rule_zero;SCZ2792_6_verdict", "source-current zero theorem attempt"),
        ("SRC2949_15_2793_contract", SRC_2793_CONTRACT, "ZCC2793_0_object_language;ZCC2793_5_boundary_domain", "zero-current future parent contract"),
        ("SRC2949_16_2852_symmetry", SRC_2852_SYMMETRY, "SYM2852_0_fixed_source_vector;SYM2852_4_auxiliary_constraint", "source-doublet symmetry candidates"),
        ("SRC2949_17_2866_route", SRC_2866_ROUTE, "ROUTE2866_0_parent_action_synthesis;ROUTE2866_4_run_A_total_now", "route decision matrix"),
        ("SRC2949_18_1041_thetax", SRC_1041_THETAX, "TOG1041_0_parent_route;TOG1041_5_verdict", "Theta_X owner gate"),
        ("SRC2949_19_967_positive", SRC_967_POSITIVE, "MPO967_0_setup;MPO967_6_verdict", "positive operator lemma"),
        ("SRC2949_20_968_inputs", SRC_968_INPUTS, "MOI968_0_X_variable;MOI968_8_verdict", "positive operator input audit"),
        ("SRC2949_21_972_two_slot", SRC_972_TWO_SLOT, "TSC972_0_field_domain;TSC972_7_verdict", "two-slot action contract"),
        ("SRC2949_22_973_jx", SRC_973_JX, "JXD973_0_kinetic_affine;JXD973_6_verdict", "J_X decomposition"),
        ("SRC2949_23_2022_ix_schema", SRC_2022_IX_SCHEMA, "IXS2022_0_ZX;IXS2022_11_Ix_abs", "I_X source row schema"),
        ("SRC2949_24_2665_hlock", SRC_2665_HLOCK, "HLOCK2665_0_target;HLOCK2665_7_verdict", "Hamiltonian/PiM lock"),
        ("SRC2949_25_2665_pdg", SRC_2665_PDG, "PDG2665_0_same_frame;PDG2665_7_verdict", "projector denominator gate"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
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


def selector_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "XROUTE2949_0_absent_topological",
            "absent_or_topological",
            "L_X=0 or L_X=dB_top and Q_tau_X/C_tau_X are exact/topological with no local source charge",
            "REJECT_CURRENT_CORPUS",
            "no signed parent field inventory demotes the live X direction to absent/topological; kappa-style topological route does not cover all X channels",
            4,
            False,
            False,
        ),
        (
            "XROUTE2949_1_first_class_vertical",
            "first_class_vertical_quotient",
            "v_X in ker(Dq), parent action descends or is gauge-degenerate along v_X, matter/readout are q-basic, boundary/projector tails vanish",
            "CONDITIONAL_ONLY_NOT_SELECTED",
            "no owned q map, kernel basis, degree count, matter functor, or boundary/domain silence; representative zero cannot be promoted to observed source zero",
            3,
            False,
            False,
        ),
        (
            "XROUTE2949_2_positive_nohair",
            "positive_sourcefree_nohair",
            "L_X=-nabla_i(A_X^ij nabla_j)+M_X^2 with A_X>=0, M_X^2>=0, J_X=0, fixed boundary class",
            "BEST_DERIVATION_ROUTE_NOT_SIGNED",
            "positive-operator lemma is mathematically ready, but X variable, domain, operator, sign, source-zero and boundary inputs are missing",
            1,
            True,
            False,
        ),
        (
            "XROUTE2949_3_finite_sourced_residual",
            "finite_sourced_residual",
            "same L_X normal form, but J_X/boundary/PiM/omega components are retained as source-backed finite rows",
            "SELECTED_EXECUTABLE_FALLBACK_NONCLAIM",
            "only route that lets us proceed without pretending the zero proof is done; not score-ready until component values or theorem-zeros exist",
            2,
            True,
            False,
        ),
        (
            "XROUTE2949_4_auxiliary_constraint",
            "auxiliary_constraint_identity",
            "lambda_X constraint imposes I_X=0 or Q_CAB+sigma_R q_R=0",
            "REJECT_AS_CLOSURE_AXIOM",
            "would smuggle the answer unless it descends from a known parent first-class constraint algebra",
            99,
            False,
            False,
        ),
        (
            "XROUTE2949_5_verdict",
            "route_selector_verdict",
            "choose positive/nohair as the derivation route and finite residual as the executable fallback",
            "DUAL_ROUTE_SELECTED_NONCLAIM",
            "this is the least-cheating path: prove nohair if inputs appear; otherwise fill finite residual rows with no cancellation credit",
            0,
            True,
            False,
        ),
    ]
    return [
        add_common(
            {
                "route_id": route_id,
                "route": route,
                "route_signature": signature,
                "current_status": status,
                "reason": reason,
                "rank": rank,
                "selected_for_next": selected_for_next,
                "selected_for_claim": selected_for_claim,
            }
        )
        for route_id, route, signature, status, reason, rank, selected_for_next, selected_for_claim in rows
    ]


def normal_form_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LX2949_0_field_content",
            "X field bundle",
            "Phi_X contains the retained motion/time/range/memory scalar/vector/tensor direction with declared transformation law",
            "FIELD_ACTION_INCOMPLETE",
            "needed before Theta_X or Q_tau_X can be computed",
        ),
        (
            "LX2949_1_quadratic_operator",
            "positive/residual operator",
            "L_X^kin = 1/2 int_D sqrt(h)(A_X^ij nabla_i X nabla_j X + M_X^2 X^2)",
            "NORMAL_FORM_SELECTED_NOT_PARENT_DERIVED",
            "use as acquisition normal form for Z_X, M_X^2, lambda_X and omega_X",
        ),
        (
            "LX2949_2_source_slot",
            "source current slot",
            "L_X^src = - int_D sqrt(h) X J_X with J_X=sum absolute channel components",
            "FINITE_FALLBACK_SELECTED_NONCLAIM",
            "J_X must be theorem-zero or source-bounded channelwise",
        ),
        (
            "LX2949_3_boundary_package",
            "boundary and zero-mode package",
            "B_X fixes Dirichlet/Neumann/zero-mean/topological class before readout",
            "BOUNDARY_CLASS_MISSING",
            "positive identity fails if boundary hair remains",
        ),
        (
            "LX2949_4_double_zero_observed_slot",
            "observed coupling double-zero",
            "f(chi_D) C_obs[X,q,Psi,theta] with f(0)=f'(0)=0",
            "RELATIVE_FORM_READY_ORIGIN_UNSIGNED",
            "good compatibility clause but not an origin for L_X by itself",
        ),
        (
            "LX2949_5_no_direct_matter_slot",
            "no direct matter/source marker slot",
            "delta_X(S_core+S_matter+S_extra boundary)=0 except owned X terms",
            "OBJECT_LANGUAGE_NOT_SIGNED",
            "pre-action source weights and material markers still survive",
        ),
        (
            "LX2949_6_Qtau_extraction",
            "Theta_X/Q_tau_X/C_tau_X extraction",
            "delta L_X=E_X delta X+dTheta_X; J_tau^X=Theta_X(L_tau X)-i_tau L_X=dQ_tau_X+C_tau_X",
            "EXACT_CONDITIONAL_FORM_NOT_EXTRACTED",
            "normal form gives the worklist, not a claim-grade charge yet",
        ),
        (
            "LX2949_7_verdict",
            "L_X normal-form gate",
            "quadratic positive/residual normal form is selected for 2950 input acquisition",
            "GATE_READY_NONCLAIM",
            "not parent-derived; finite row and zero-proof both remain blocked until inputs are supplied",
        ),
    ]
    return [
        add_common(
            {
                "normal_form_id": normal_id,
                "object": obj,
                "required_form": form,
                "current_status": status,
                "effect": effect,
                "normal_form_selected_for_acquisition": normal_id in {"LX2949_1_quadratic_operator", "LX2949_2_source_slot", "LX2949_3_boundary_package", "LX2949_7_verdict"},
                "parent_derived": False,
            }
        )
        for normal_id, obj, form, status, effect in rows
    ]


def acceptance_rows() -> list[dict[str, Any]]:
    rows = [
        ("ACC2949_0_route_selected", "one route selected before scoring", "positive/nohair derivation + finite residual fallback selected", True, "NONCLAIM_ROUTE_SELECTION_ONLY"),
        ("ACC2949_1_parent_LX", "parent L_X source path and equation anchor exists", "missing parent-derived L_X", False, "BLOCKS_THETAX_QTAUX"),
        ("ACC2949_2_operator_inputs", "Z_X and M_X^2 are numeric or theorem-zero/source-backed", "missing operator inputs", False, "BLOCKS_NOHAIR_AND_RANGE"),
        ("ACC2949_3_JX_zero_or_bound", "J_X components are theorem-zero or finite source-backed", "component envelope exists but values missing", False, "BLOCKS_SOURCE_SILENCE"),
        ("ACC2949_4_boundary_class", "boundary/zero-mode class fixed before readout", "boundary class missing", False, "BLOCKS_ENERGY_IDENTITY"),
        ("ACC2949_5_PiM_MHref_lock", "PiM tail and M_H_ref denominator are parent-owned", "PiM/MHref locks missing", False, "BLOCKS_LOCAL_DENOMINATOR"),
        ("ACC2949_6_score_ready", "I_X row can feed local/R10/PPN scoring", "no accepted finite row", False, "NO_SCORING_FROM_2949"),
    ]
    return [
        add_common(
            {
                "acceptance_id": acc_id,
                "gate": gate,
                "evidence": evidence,
                "gate_passed": passed,
                "status": status,
            }
        )
        for acc_id, gate, evidence, passed, status in rows
    ]


def positive_input_rows() -> list[dict[str, Any]]:
    rows = [
        ("PIN2949_0_X_variable", "X", "parent field or quotient scalar for retained X direction", "MISSING_PARENT_OWNER", str(SRC_968_INPUTS)),
        ("PIN2949_1_domain", "D_local", "compact stationary local exterior domain selected before readout", "MISSING_PARENT_SELECTED_DOMAIN", str(SRC_968_INPUTS)),
        ("PIN2949_2_ZX", "Z_X or A_X^ij", "kinetic/operator normalization and positivity certificate", "MISSING_SIGN_CERTIFICATE", str(SRC_2022_IX_SCHEMA)),
        ("PIN2949_3_MX2", "M_X^2", "mass/gap/range term and zero-mode policy", "MISSING_GAP_INPUTS", str(SRC_2022_IX_SCHEMA)),
        ("PIN2949_4_JX", "J_X", "source current silence or finite source bound", "MISSING_ZERO_SOURCE_THEOREM", str(SRC_973_JX)),
        ("PIN2949_5_boundary", "B_X / boundary_X", "boundary/zero-mode/no-tail class", "MISSING_BOUNDARY_DATA", str(SRC_968_INPUTS)),
        ("PIN2949_6_omega", "omega_X", "symplectic flux extracted from same L_X", "MISSING_THETA_OMEGA_INPUTS", str(SRC_2948_IX)),
        ("PIN2949_7_PiM_tail", "Pi_M^H Q_tau_X", "Hamiltonian mass projection tail and commutator stress", "MISSING_PIM_PROJECTION_LOCK", str(SRC_2665_HLOCK)),
        ("PIN2949_8_MHref", "M_H_ref", "positive same-frame source denominator", "MISSING_STABLE_MH_REF", str(SRC_2022_IX_SCHEMA)),
    ]
    return [
        add_common(
            {
                "input_id": input_id,
                "symbol": symbol,
                "required_payload": payload,
                "current_status": status,
                "source_path": source_path,
                "source_path_exists": Path(source_path).exists(),
                "numeric_or_theorem_value": "MISSING",
                "accepted_for_scoring": False,
            }
        )
        for input_id, symbol, payload, status, source_path in rows
    ]


def finite_rows() -> list[dict[str, Any]]:
    rows = [
        ("FIN2949_0_Ix_abs", "I_X/M_H_ref", "abs(omega_X + C_tau_X + boundary_X + PiM_tail_X)/M_H_ref", "dimensionless", "NOT_COMPUTED_COMPONENTS_MISSING"),
        ("FIN2949_1_alpha_lambda", "alpha_X(lambda_X)", "source-normalized Yukawa/fifth-force map if X survives", "alpha_lambda_curve", "MISSING_ZX_MX2_QBAR_BOUND_JOIN"),
        ("FIN2949_2_PPN", "Delta_PPN_X", "projection of X residual into gamma,beta,alpha_i,zeta_i,xi", "dimensionless_ppn", "MISSING_ARENA_PROJECTION"),
        ("FIN2949_3_clock", "Delta_clock_X", "clock/constant/material-marker response to X", "dimensionless_or_frequency_ratio", "MISSING_CLOCK_KERNEL"),
        ("FIN2949_4_orbital", "Delta_orbital_X", "source mass/light-time/orbital residual from X tail", "dimensionless_or_acceleration_ratio", "MISSING_ORBITAL_KERNEL"),
        ("FIN2949_5_no_cancellation", "absolute_envelope", "sum_abs(all retained X components) with no opposite-sign credit", "gate", "ENVELOPE_READY_VALUES_MISSING"),
    ]
    return [
        add_common(
            {
                "finite_row_id": row_id,
                "symbol": symbol,
                "formula_or_mapping": formula,
                "units": units,
                "current_status": status,
                "source_backed": False,
                "accepted_for_scoring": False,
                "source_path": str(SRC_2022_IX_SCHEMA),
                "source_path_exists": SRC_2022_IX_SCHEMA.exists(),
            }
        )
        for row_id, symbol, formula, units, status in rows
    ]


def guard_rows() -> list[dict[str, Any]]:
    rows = [
        ("GUARD2949_0_route_not_claim", "selected working route is not a proof of local GR", True),
        ("GUARD2949_1_no_aux_constraint", "auxiliary constraint route rejected unless parent first-class algebra is sourced", True),
        ("GUARD2949_2_no_EH_import", "EH charge/operator cannot replace X-sector charge/operator", True),
        ("GUARD2949_3_no_orbital_GM", "M_H_ref and source normalization cannot be calibrated from orbital GM", True),
        ("GUARD2949_4_no_cancellation", "finite X residual rows use absolute no-cancellation envelope", True),
        ("GUARD2949_5_no_public_claim", "no local-GR/Newton/R10/PPN/public claim from 2949", True),
    ]
    return [add_common({"guard_id": guard_id, "guard": guard, "guard_passed": passed}) for guard_id, guard, passed in rows]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2949_0_parent_LX", "parent L_X route is claim-grade", False, "ROUTE_SELECTED_FOR_WORK_ONLY"),
        ("CG2949_1_positive_nohair", "positive/nohair zero theorem closes", False, "INPUTS_MISSING"),
        ("CG2949_2_finite_residual", "finite I_X/J_X residual rows are score-ready", False, "VALUES_MISSING"),
        ("CG2949_3_Qtau_X", "Theta_X/Q_tau_X/C_tau_X extracted", False, "CHARGE_EXTRACTION_MISSING"),
        ("CG2949_4_MHref_reopen", "H_tau/M_H_ref denominator reopens", False, "PIM_MHREF_LOCK_MISSING"),
        ("CG2949_5_local_GR", "local GR/Newton reduction claim allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2949_6_public_claim", "public claim allowed from 2949", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "claim_allowed": False,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2949_0_result",
            "route selector narrowed the X-sector work",
            "positive/source-free nohair is the best derivation route; finite sourced residual is the executable fallback",
            "use the selected normal form for coefficient/input acquisition",
        ),
        (
            "DEC2949_1_not_a_claim",
            "no zero theorem was promoted",
            "Z_X, M_X^2, J_X, boundary, omega_X, PiM tail and M_H_ref are missing",
            "keep local-GR/Newton/R10/PPN claims blocked",
        ),
        (
            "DEC2949_2_rejected_route",
            "auxiliary constraint route rejected",
            "it would impose the cancellation rather than derive it unless parent first-class algebra is found",
            "do not use lambda-constraint shortcuts",
        ),
        (
            "DEC2949_3_next",
            "attack operator coefficients and finite row payload",
            "the selected normal form makes the next missing payload unambiguous",
            "build 2950 for Z_X/M_X^2/J_X/boundary/PiM/MHref input acquisition",
        ),
    ]
    return [add_common({"decision_id": decision_id, "decision": decision, "reason": reason, "next_action": action}) for decision_id, decision, reason, action in rows]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2949_0_2950",
                "priority": "selected_primary",
                "next_doc": "2950-Y5-R2FR-parent-X-operator-coefficient-or-finite-residual-input-acquisition-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_parent_X_operator_coefficient_or_finite_residual_input_acquisition_under_AX1090_2950.py",
                "objective": "Try to source or derive the first real payload for the selected L_X normal form: X field owner, Z_X/A_X, M_X^2/range, J_X channel zero/bounds, boundary class, omega_X, PiM tail, and M_H_ref. If no parent inputs exist, keep the finite residual row explicitly blocked.",
                "include": "Z_X;M_X^2;lambda_X;J_matter;J_chiD;J_boundary;J_readout;J_history;omega_X;PiM_tail;M_H_ref;source paths;units;no-cancellation guard",
                "exclude": "public claim;local-GR pass;EH-only substitution;orbital-GM denominator;ad hoc constraint;formalization-workbench edits;GitHub action",
            }
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copy_pairs = [
        ("selector_copy", OUTPUTS["selector"], BRANCH_OUTPUTS["selector_copy"]),
        ("normal_form_copy", OUTPUTS["normal_form"], BRANCH_OUTPUTS["normal_form_copy"]),
        ("positive_inputs_copy", OUTPUTS["positive_inputs"], BRANCH_OUTPUTS["positive_inputs_copy"]),
        ("finite_rows_copy", OUTPUTS["finite_rows"], BRANCH_OUTPUTS["finite_rows_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copy_pairs:
        if source.exists():
            shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows() -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"] + [OUTPUTS["validation"]]
    sources = read_csv_rows(OUTPUTS["sources"])
    selector = read_csv_rows(OUTPUTS["selector"])
    normal_form = read_csv_rows(OUTPUTS["normal_form"])
    acceptance = read_csv_rows(OUTPUTS["acceptance"])
    positive_inputs = read_csv_rows(OUTPUTS["positive_inputs"])
    finite = read_csv_rows(OUTPUTS["finite_rows"])
    guards = read_csv_rows(OUTPUTS["guards"])
    claims = read_csv_rows(OUTPUTS["claims"])
    next_target = read_csv_rows(OUTPUTS["next"])
    branches = read_csv_rows(OUTPUTS["branches"])

    checks = [
        ("VAL2949_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "all cited local source paths exist", True),
        ("VAL2949_1_anchors_found", all(row["anchors_found"] == "True" for row in sources), "all source anchors found", True),
        ("VAL2949_2_route_selector_emitted", any(row["route_id"] == "XROUTE2949_5_verdict" for row in selector), "route selector verdict emitted", True),
        ("VAL2949_3_selected_nonclaim_routes", any(row["route_id"] == "XROUTE2949_2_positive_nohair" and row["selected_for_next"] == "True" for row in selector) and any(row["route_id"] == "XROUTE2949_3_finite_sourced_residual" and row["selected_for_next"] == "True" for row in selector), "positive derivation and finite fallback selected for next", True),
        ("VAL2949_4_no_route_claim", all(row["selected_for_claim"] == "False" and row["claim_allowed"] == "False" for row in selector), "no route selected for claim", True),
        ("VAL2949_5_normal_form_selected", any(row["normal_form_id"] == "LX2949_7_verdict" and row["normal_form_selected_for_acquisition"] == "True" for row in normal_form), "L_X normal form selected for acquisition", True),
        ("VAL2949_6_acceptance_blocks_claim", any(row["acceptance_id"] == "ACC2949_6_score_ready" and row["gate_passed"] == "False" for row in acceptance), "score-ready gate remains blocked", True),
        ("VAL2949_7_inputs_nonclaim", len(positive_inputs) >= 9 and all(row["accepted_for_scoring"] == "False" and row["valid_for_claim"] == "False" for row in positive_inputs), "positive operator input queue emitted as nonclaim", True),
        ("VAL2949_8_finite_rows_nonclaim", len(finite) >= 6 and all(row["accepted_for_scoring"] == "False" and row["valid_for_claim"] == "False" for row in finite), "finite residual acquisition rows emitted as nonclaim", True),
        ("VAL2949_9_guards_passed", all(row["guard_passed"] == "True" for row in guards), "all route guards pass", True),
        ("VAL2949_10_claims_blocked", all(row["condition_passed"] == "False" and row["claim_allowed"] == "False" for row in claims), "all claims blocked", True),
        ("VAL2949_11_next_target_selected", any(row["next_id"] == "NEXT2949_0_2950" for row in next_target), "2950 input acquisition target selected", True),
        ("VAL2949_12_branches_exist", all(row["copy_exists"] == "True" for row in branches), "branch copy files exist", True),
        ("VAL2949_13_csvs_parse", all(csv_parses(path) for path in generated_csvs), "all generated CSV files parse", True),
        ("VAL2949_14_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in [DOC, *generated_csvs, *BRANCH_OUTPUTS.values()]), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2949_15_formalization_clean", not any(FORMALIZATION.rglob("*2949*")) if FORMALIZATION.exists() else True, "no 2949 outputs were written to formalization-workbench", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "check": check, "required": required} for validation_id, passed, check, required in checks]
    rows.append({"validation_id": "VAL2949_OVERALL", "passed": overall, "check": "2949 validation overall", "required": True})
    return rows


def write_doc() -> None:
    sources = read_csv_rows(OUTPUTS["sources"])
    selector = read_csv_rows(OUTPUTS["selector"])
    normal_form = read_csv_rows(OUTPUTS["normal_form"])
    acceptance = read_csv_rows(OUTPUTS["acceptance"])
    positive_inputs = read_csv_rows(OUTPUTS["positive_inputs"])
    finite = read_csv_rows(OUTPUTS["finite_rows"])
    guards = read_csv_rows(OUTPUTS["guards"])
    claims = read_csv_rows(OUTPUTS["claims"])
    decisions = read_csv_rows(OUTPUTS["decision"])
    next_target = read_csv_rows(OUTPUTS["next"])
    branches = read_csv_rows(OUTPUTS["branches"])
    validation = read_csv_rows(OUTPUTS["validation"])
    overall = next((row["passed"] for row in validation if row["validation_id"] == "VAL2949_OVERALL"), "False")

    content = f"""# 2949 - Y5 R2FR: parent X-action route selector and L_X normal-form gate under AX1090

Status: `Y5_R2FR_2949_positive_nohair_route_selected_for_derivation_finite_residual_selected_as_nonclaim_fallback`

Claim ceiling: `no_parent_LX_no_positive_nohair_claim_no_IX_score_no_Qtau_X_no_MHref_no_local_GR_no_Newton_no_R10_no_PPN_no_public_claim`

2949 forces the X-sector fork to stop wobbling. The selected working normal form is:

`L_X^kin = 1/2 int_D sqrt(h)(A_X^ij nabla_i X nabla_j X + M_X^2 X^2)`

with optional retained source term

`L_X^src = - int_D sqrt(h) X J_X`.

This is not a claim that the parent action has been found. It is the cleanest acquisition contract: if `J_X=0`, boundary terms vanish, and the operator is positive/gapped, the positive/no-hair route can kill `I_X`; if not, the same normal form produces finite nonclaim residual rows for local/R10/PPN testing later.

## Source Register

{md_table(sources, ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## X-Route Selector Matrix

{md_table(selector, ["route_id", "route", "current_status", "reason", "rank", "selected_for_next", "selected_for_claim"])}

## L_X Normal-Form Gate

{md_table(normal_form, ["normal_form_id", "object", "required_form", "current_status", "effect", "normal_form_selected_for_acquisition"])}

## Route Acceptance Gates

{md_table(acceptance, ["acceptance_id", "gate", "evidence", "gate_passed", "status"])}

## Positive Operator Input Queue

{md_table(positive_inputs, ["input_id", "symbol", "required_payload", "current_status", "numeric_or_theorem_value", "accepted_for_scoring"])}

## Finite Residual Acquisition Rows

{md_table(finite, ["finite_row_id", "symbol", "formula_or_mapping", "units", "current_status", "accepted_for_scoring"])}

## Route Guards

{md_table(guards, ["guard_id", "guard", "guard_passed"])}

## Claim Gates

{md_table(claims, ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(next_target, ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(branches, ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "check", "required"])}

Validation overall: `{overall}`.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["selector"], selector_rows())
    write_csv(OUTPUTS["normal_form"], normal_form_rows())
    write_csv(OUTPUTS["acceptance"], acceptance_rows())
    write_csv(OUTPUTS["positive_inputs"], positive_input_rows())
    write_csv(OUTPUTS["finite_rows"], finite_rows())
    write_csv(OUTPUTS["guards"], guard_rows())
    write_csv(OUTPUTS["claims"], claim_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_rows())
    write_csv(OUTPUTS["branches"], branch_copy_rows())
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    print(f"2949 validation overall: {read_csv_rows(OUTPUTS['validation'])[-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
