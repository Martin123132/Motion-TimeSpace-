from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4763"
CLAIM_ID = "L-605"
MARKER = "PPC4161_QBARXH_SOURCE_NUMERATOR_FIRST_FILL_OR_QBARXT_HARD_BLOCKER_4763"
PACKET_MARKER = "PPC4161_PACKET_QBARXH_SOURCE_NUMERATOR_FIRST_FILL_OR_QBARXT_HARD_BLOCKER_4763"
DECISION = "QBARXH_NUMERATOR_FIRST_FILL_SELECTS_QEDGE_SHELL_WITH_MLOWER_PIM_GATE_QBARXT_EMF2_HARDBLOCKER_RETAINED_NONCLAIM"
NEXT_TARGET = "4764-Y5-R2FR-Mlower-PiM-denominator-lock-or-Qedge-shell-source-row.md"

DOC_PATH = POST / "4763-Y5-R2FR-QbarXH-source-numerator-first-fill-or-qbarXT-hard-blocker.md"
FORMAL_PATH = FORMAL / "779-PPC4161-QbarXH-source-numerator-first-fill-or-qbarXT-hard-blocker.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4763_SOURCE_REGISTER.csv"
NUMERATOR_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4763_QBARXH_NUMERATOR_AUDIT.csv"
FIRST_FILL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4763_FIRST_FILL_SELECTION.csv"
QEDGE_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4763_QEDGE_SHELL_SOURCE_ROW_CONTRACT.csv"
DENOMINATOR_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4763_DENOMINATOR_PROJECTOR_GATE.csv"
QBARXT_BLOCKER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4763_QBARXT_EMF2_HARDBLOCKER_ROWS.csv"
PRODUCT_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4763_PRODUCT_GATE_UPDATE.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4763_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4763_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4763_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4763_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4763_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4763_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4763_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4763_0_4762_decision", SOURCE_DIR / "P8_Y5_R2FR_4762_DECISION.csv", "QBARXT_ZERO_CONTRACT_ASSEMBLED_BUT_EM_F2", "4762 handoff decision"),
    ("SRC4763_1_4762_qbarxh", SOURCE_DIR / "P8_Y5_R2FR_4762_QBARXH_FIRST_SOURCE_ROW.csv", "QXH4762_1_absolute_bound", "4762 QbarXH source row"),
    ("SRC4763_2_4699_envelope", SOURCE_DIR / "P8_Y5_R2FR_4699_QBARXH_SOURCE_ENVELOPE_THEOREM.csv", "QBAR4699_3_first_source_backed_queue", "4699 source envelope theorem"),
    ("SRC4763_3_4699_rollup", SOURCE_DIR / "P8_Y5_R2FR_4699_CURRENT_BRANCH_QBARXH_ROLLUP_ROWS.csv", "QBC4699_1_first_fill_order", "4699 current branch rollup"),
    ("SRC4763_4_4699_priority", SOURCE_DIR / "P8_Y5_R2FR_4699_FIRST_SOURCE_BACKED_PRIORITY_QUEUE.csv", "M_lower, ||Pi_M^H||, E_PiM_comm", "4699 first source-backed queue"),
    ("SRC4763_5_4699_bulk", SOURCE_DIR / "P8_Y5_R2FR_4699_QBULK_ROLLUP_ROWS.csv", "BROLL4699_2_EM_Poynting", "bulk/Poynting rollup"),
    ("SRC4763_6_4699_edge", SOURCE_DIR / "P8_Y5_R2FR_4699_QEDGE_ROLLUP_ROWS.csv", "EROLL4699_1_shell", "edge shell rollup"),
    ("SRC4763_7_4699_shadow", SOURCE_DIR / "P8_Y5_R2FR_4699_QSHADOW_ROLLUP_ROWS.csv", "SROLL4699_2_projector", "shadow/projector rollup"),
    ("SRC4763_8_4699_denominator", SOURCE_DIR / "P8_Y5_R2FR_4699_QBARXH_DENOMINATOR_PROJECTOR_ROWS.csv", "DPROJ4699_0_M_lower", "denominator/projector gate"),
    ("SRC4763_9_4697_edge_theorem", SOURCE_DIR / "P8_Y5_R2FR_4697_QEDGE_WORLDTUBE_BOUNDARY_THEOREM.csv", "QE4697_1_reynolds_shell_zero", "Qedge Reynolds shell theorem"),
    ("SRC4763_10_4697_shell", SOURCE_DIR / "P8_Y5_R2FR_4697_QEDGE_REYNOLDS_SHELL_ROWS.csv", "QES4697_5_total", "Qedge shell source row"),
    ("SRC4763_11_4694_bulk", SOURCE_DIR / "P8_Y5_R2FR_4694_QBULK_SOURCE_CURRENT_THEOREM.csv", "QBH4694_3_EM_Poynting_zero_or_flux", "Qbulk EM/Poynting theorem"),
    ("SRC4763_12_4703_f2", SOURCE_DIR / "P8_Y5_R2FR_4703_NO_EXTRA_F2_THEOREM.csv", "NEF4703_4_current_verdict", "qbarXT no-extra-F2 hard blocker"),
    ("SRC4763_13_4704_image", SOURCE_DIR / "P8_Y5_R2FR_4704_VISIBLE_IMAGE_PROOF_ATTEMPT.csv", "VIP4704_3_reduced_exact_bottleneck", "visible image/hidden Hom hard blocker"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    NUMERATOR_AUDIT_CSV,
    FIRST_FILL_CSV,
    QEDGE_CONTRACT_CSV,
    DENOMINATOR_GATE_CSV,
    QBARXT_BLOCKER_CSV,
    PRODUCT_UPDATE_CSV,
    ROUTE_MATRIX_CSV,
    PROMOTION_GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def numerator_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "NA4763_0_QbarXH_master",
            "Qbar_XH_abs",
            "|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/M_lower",
            "The source coupling problem is a named numerator plus denominator/projector gate, not an undefined parameter.",
            "MASTER_FORMULA_READY_VALUES_MISSING",
        ),
        (
            "NA4763_1_bulk",
            "Q_bulk_abs",
            "|Q_bulk| <= |Q_bulk_Hilbert|+|Q_bulk_EM/Poynting|+|Q_bulk_retained|",
            "Bulk is physically rich but touches the same EM/F2/Poynting hard blocker as qbarXT.",
            "FORMULA_READY_HARDER_FIRST_FILL",
        ),
        (
            "NA4763_2_edge_shell",
            "Q_edge_shell_abs",
            "|Q_edge_shell| <= W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV)",
            "Cleanest first numerator fill: worldtube geometry and source support quantities are named and measurable/boundable.",
            "SELECTED_FIRST_NUMERATOR_FILL",
        ),
        (
            "NA4763_3_edge_boundary",
            "Q_edge_boundary_abs",
            "|Q_edge_boundary| <= |B_X_flux|+|C_corner|+|E_reference_edge|+|F_side_source|+|F_rad|+|E_projector_edge|",
            "Important but mixes Hamiltonian boundary, radiative and reference pieces.",
            "SECOND_EDGE_FILL_AFTER_SHELL",
        ),
        (
            "NA4763_4_shadow",
            "Q_shadow_abs",
            "|Q_shadow| <= |Q_shadow_action|+|Q_shadow_projector|+|Q_shadow_nonvariational|",
            "Sensitive to parent-action inventory and projector/source-map normal form.",
            "DEFERRED_ACTION_INVENTORY_RISK",
        ),
        (
            "NA4763_5_denominator",
            "M_lower, ||Pi_M^H||, E_PiM_comm",
            "M_lower=M_0(1-epsilon_abs); E_PiM_comm bounds projector/source commutator",
            "Even a filled numerator cannot score unless this gate is positive and source-backed.",
            "PRECONDITION_FOR_QBAR_SCORE",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": audit_id,
            "quantity": quantity,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, quantity, formula, meaning, status in specs
    ]


def first_fill_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "FF4763_0_denominator_precheck",
            "M_lower, ||Pi_M^H||, E_PiM_comm",
            "positive denominator and fixed projector commute/bound",
            "This is the first gate before any Qbar_XH score; it prevents division by a symbolic source mass.",
            "GATE_BEFORE_SCORING",
            "M_0, epsilon_abs, source vector norm, projector definition, commutator zero-or-bound, units",
        ),
        (
            "FF4763_1_Qedge_shell",
            "Q_edge_shell_abs",
            "|Q_edge_shell| <= W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV)",
            "Selected first numerator fill because it is the cleanest support/worldtube row and does not require the full EM/F2 hard blocker.",
            "SELECTED_FIRST_NUMERATOR_ROW",
            "rho_H_trace_norm, V_n_bound, mu_birth_TV, Phi_edge, W_lambda_edge_max, source collar path",
        ),
        (
            "FF4763_2_Poynting_wall",
            "Phi_wall_Poynting_abs",
            "|Q_EM_flux| <= W_lambda_max |int_boundary T_EM(tau,n) dSigma dt|",
            "Keeps the Poynting hunch alive as a real row, but it is third because it couples to EM/Hodge/no-extra-F2.",
            "PHYSICALLY_INTERESTING_SECONDARY",
            "same-Hodge, tau, boundary normal, EM stress flux, time window",
        ),
        (
            "FF4763_3_shadow_projector",
            "epsilon_source_shadow",
            "|Q_shadow_projector| <= |C0_common_unowned| ||T_H|| + epsilon_source_shadow ||T_H|| + |E_projector_source| + |E_readout_return|",
            "Needed eventually for WEP/PPN safety, but source-map inventory risk is high.",
            "DEFERRED_SHADOW_ROW",
            "projector norm, source-map identity, readout-return bound",
        ),
        (
            "FF4763_4_qbarXT_hardblocker",
            "no-extra-F2 / hidden-Hom",
            "visible EM coefficient image contains only q-basic parent data and fixed representation constants",
            "Would reopen the derivation route and close the hardest qbarXT component.",
            "PARALLEL_DERIVATION_SUBTARGET",
            "parent scalar-functional exhaustion, no hidden Hom into Coeff(F_Q^2), same current owner",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "fill_id": fill_id,
            "target_quantity": quantity,
            "formula_or_task": formula,
            "why_this_order": why,
            "selection_status": status,
            "required_inputs": inputs,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for fill_id, quantity, formula, why, status, inputs in specs
    ]


def qedge_contract_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("QE4763_0_system", "system_id", "named local source/worldtube/collar", "nonempty local arena identifier and source path", "required"),
        ("QE4763_1_worldtube", "W_H", "closure(supp J_H,total) before readout", "explicit worldtube definition and boundary surface", "required"),
        ("QE4763_2_trace", "rho_H_trace_norm", "int_partialW |rho_H^tr| dSigma", "zero trace certificate or finite source-backed trace norm", "required"),
        ("QE4763_3_velocity", "V_n_bound", "sup_partialW |V_n| under source-vertical probe", "fixed boundary certificate or finite support variation bound", "required"),
        ("QE4763_4_birth", "mu_birth_TV", "total variation norm of distributional source birth/death shell", "no-shell certificate or finite total variation value", "required"),
        ("QE4763_5_test", "Phi_edge", "sup_partialW |phi_edge| for declared arena", "finite arena test ceiling and units", "required"),
        ("QE4763_6_kernel", "W_lambda_edge_max", "sup_partialW |W_lambda|", "finite-range kernel ceiling for lambda branch", "required"),
        ("QE4763_7_total", "Q_edge_shell_abs", "|Q_edge_shell| <= W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV)", "claim-ready only with all required fields zero/sourced and no MISSING markers", "false_now"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "contract_id": contract_id,
            "field": field,
            "definition_or_formula": definition,
            "claim_grade_requirement": requirement,
            "status": status,
            "example_value": "MISSING_NOT_ALLOWED_FOR_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, field, definition, requirement, status in specs
    ]


def denominator_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("DG4763_0_Mlower", "M_lower", "M_lower=M_0(1-epsilon_abs), M_0>0, 0<=epsilon_abs<1", "MISSING_POSITIVE_LOWER_BOUND"),
        ("DG4763_1_PiM_norm", "||Pi_M^H||", "operator norm of fixed mass/source projector on Q_tot vector space", "MISSING_PROJECTOR_OPERATOR_NORM"),
        ("DG4763_2_commutator", "E_PiM_comm", "bounds [D_v,Pi_M]Q_tot or [d,Pi_M]J_H", "MISSING_PROJECTOR_COMMUTATOR_ZERO_OR_BOUND"),
        ("DG4763_3_firewall", "Qbar_XH_claim_firewall", "no division by symbolic M_lower and no measured-G absorption", "ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "quantity": quantity,
            "formula_or_rule": formula,
            "current_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, quantity, formula, status in specs
    ]


def qbarxt_blocker_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "QBXT4763_0_no_extra_F2",
            "F_Q^2 coefficient throat",
            "No-extra-F2 is exact only if visible operator domain is the parent-generated image and contains no independent Coeff(F_Q^2).",
            "CURRENT_VERDICT_UNSIGNED",
        ),
        (
            "QBXT4763_1_hidden_Hom",
            "hidden Hom into Coeff(F_Q^2)",
            "Hidden scalar coefficient lambda_F2=lambda_0+epsilon I_hid remains a legal countermodel unless parent object language forbids the target.",
            "COUNTERMODEL_ACTIVE",
        ),
        (
            "QBXT4763_2_balpha",
            "b_alpha_EM",
            "b_alpha_EM=2 z_g-z_lambda-z_readout-z_rad; zero only with gauge object, charge lattice, unique F2, same current owner and readout/radiative closure.",
            "BOUND_BRANCH_READY_VALUES_MISSING",
        ),
        (
            "QBXT4763_3_payoff",
            "qbarXT EM component",
            "Closing this hard blocker would remove the most scrutinized qbarXT component and reopen product-zero route.",
            "PARALLEL_DERIVATION_TARGET",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": blocker_id,
            "object": obj,
            "statement": statement,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for blocker_id, obj, statement, status in specs
    ]


def product_update_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PU4763_0_source_insert", "|I_mem^ST| <= |Qbar_XH|_abs |qbar_XT|_abs/(4*pi |Z_mem| G_N M_H_ref m_T)", "absolute product still nonclaim"),
        ("PU4763_1_QbarXH_decomp", "|Qbar_XH|_abs uses Q_bulk+Q_edge+Q_shadow plus denominator/projector terms", "source-side formula staged"),
        ("PU4763_2_Qedge_shell_insert", "Q_edge_shell_abs is selected as first numerator component row", "first fill target selected"),
        ("PU4763_3_denominator_block", "Qbar score blocked until M_lower, Pi_M norm and E_PiM_comm are zero/sourced", "precondition active"),
        ("PU4763_4_qbarXT_parallel", "qbarXT EM/F2 blocker remains a derivation target but not a result", "test-side zero retained as parallel route"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "product_update_id": update_id,
            "formula_or_rule": formula,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for update_id, formula, status in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4763_0_Qedge_shell", "fill or zero Q_edge_shell_abs", "cleanest source-numerator first fill; selected", "SELECTED_NEXT_NUMERATOR"),
        ("ROUTE4763_1_Mlower_PiM", "lock M_lower/Pi_M denominator-projector gate", "needed before QbarXH can be score-ready", "SELECTED_NEXT_GATE"),
        ("ROUTE4763_2_Poynting_wall", "fill Phi_wall_Poynting_abs/EM-Hodge row", "physically interesting and user-motivated, but after denominator/shell", "SECONDARY"),
        ("ROUTE4763_3_qbarXT_EMF2", "derive no-extra-F2/hidden-Hom hard blocker", "could reopen exact product-zero route", "PARALLEL_DERIVATION"),
        ("ROUTE4763_4_R10_score", "score local tests", "deferred until product factors/range are source-backed", "DEFERRED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "payoff": payoff,
            "selection_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, payoff, status in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PG4763_0_no_symbolic_division", "QbarXH cannot be scored with symbolic M_lower or projector norm.", "blocks denominator shortcut"),
        ("PG4763_1_no_edge_slogan", "Compact source support does not imply Q_edge_shell=0; need trace/velocity/birth-shell proof or bound.", "blocks compact-source slogan"),
        ("PG4763_2_no_poynting_double_count", "Poynting is either Hilbert EM stress/edge flux or explicit coefficient, never both.", "blocks EM double count"),
        ("PG4763_3_no_shadow_absorption", "Q_shadow cannot be absorbed into source definition, G_N or GM.", "blocks RHS knob"),
        ("PG4763_4_no_product_claim", "No local test score until QbarXH, qbarXT, Z/range and tau rows are zero/sourced.", "blocks premature scoring"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "rule": rule,
            "enforced_effect": effect,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, rule, effect in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4763_0_no_qbar_claim", "Do not claim QbarXH numeric/source-backed value from 4763.", "NONCLAIM"),
        ("FW4763_1_no_edge_claim", "Do not claim Q_edge_shell=0 or bounded without trace/velocity/birth/kernel inputs.", "NONCLAIM"),
        ("FW4763_2_no_qbarxt_claim", "Do not claim qbarXT EM/F2 hard blocker is closed.", "NONCLAIM"),
        ("FW4763_3_no_github", "No GitHub action from this checkpoint.", "LOCAL_ONLY"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, rule, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4763_0",
            "decision": DECISION,
            "summary": "4763 turns QbarXH from a staged formula into an ordered source-side work plan. The first numerator fill is Q_edge_shell_abs, but the M_lower/Pi_M denominator-projector gate must be locked before any QbarXH score. The qbarXT EM/F2 hard blocker remains a parallel derivation target.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4763_0",
            "state": "completed_nonclaim",
            "meaning": "QbarXH now has a selected first numerator row and denominator gate; the next work is source-row filling rather than another generic coupling audit.",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "Before QbarXH can be scored, lock M_lower/Pi_M or fill the cleanest numerator row Q_edge_shell_abs with real source/collar inputs.",
            "route_priority": "denominator_projector_gate_then_Qedge_shell_source_row",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row[column]).replace("\n", " ") for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def write_docs(
    timestamp: str,
    numerator_rows: list[dict[str, Any]],
    fill_rows: list[dict[str, Any]],
    qedge_rows: list[dict[str, Any]],
    denom_rows: list[dict[str, Any]],
    blocker_rows: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4763: QbarXH Source Numerator First Fill or qbarXT Hard Blocker

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

4763 converts the source-side coupling route into an ordered fill plan.

- `Qbar_XH_abs` is now an explicit denominator/projector-gated source envelope, not a vague coupling gap.
- The first selected numerator fill is `Q_edge_shell_abs` because it has the cleanest source-support formula: trace density, normal support velocity, birth/death shell, arena test ceiling and kernel ceiling.
- The denominator/projector gate remains a precondition: `M_lower`, `||Pi_M^H||` and `E_PiM_comm` must be parent-locked or source-backed before a Qbar score is meaningful.
- The Poynting route is retained as a real secondary source row, not ignored: `Phi_wall_Poynting_abs` belongs in the EM/Hodge/no-flux branch.
- The `qbar_XT` EM/F2 hard blocker remains a parallel derivation route, but is not closed here.
- No local-GR, Newton, PPN, WEP, R10, clock, orbital or Maxwell pass is claimed.

## QbarXH Numerator Audit

{markdown_table(numerator_rows, ["audit_id", "quantity", "formula", "status"])}

## First-Fill Selection

{markdown_table(fill_rows, ["fill_id", "target_quantity", "formula_or_task", "selection_status"])}

## Qedge Shell Source Row Contract

{markdown_table(qedge_rows, ["contract_id", "field", "definition_or_formula", "status"])}

## Denominator / Projector Gate

{markdown_table(denom_rows, ["gate_id", "quantity", "formula_or_rule", "current_status"])}

## qbarXT EM/F2 Hard Blocker

{markdown_table(blocker_rows, ["blocker_id", "object", "status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "payoff", "selection_status"])}

## Promotion Gates

{markdown_table(gates, ["gate_id", "rule", "enforced_effect"])}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# PPC4161 4763: QbarXH Source Numerator First Fill

Generated: `{timestamp}`

## Core Result

The source-side product route now has an ordered target:

```text
|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)
              + |E_PiM_comm|)/M_lower.
```

First numerator fill:

```text
|Q_edge_shell| <= W_lambda_edge_max Phi_edge
                  (rho_H_trace_norm V_n_bound + mu_birth_TV).
```

But Qbar scoring is still blocked until:

```text
M_lower > 0,  ||Pi_M^H|| < infinity,  E_PiM_comm = 0 or bounded.
```

Parallel derivation route remains the `qbar_XT` EM/F2 hard blocker:

```text
no independent Coeff(F_Q^2), no hidden Hom into F_Q^2,
same-current owner, readout/radiative closure.
```

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4763 orders the `Qbar_XH_abs` source-side route around the denominator/projector gate and the numerator split `Q_bulk+Q_edge+Q_shadow`.
- The first selected numerator fill is `Q_edge_shell_abs = W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV)`.
- `M_lower`, `||Pi_M^H||` and `E_PiM_comm` remain mandatory before any Qbar score.
- The Poynting hunch is preserved as `Phi_wall_Poynting_abs` under EM/Hodge/no-flux rows, not as an extra hidden source.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4763 packet update: `Qbar_XH` now has a concrete first-fill queue. Go after denominator/projector lock and `Q_edge_shell_abs`; keep qbarXT EM/F2 as the parallel derivation hard blocker.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4763-Y5-R2FR-QbarXH-source-numerator-first-fill-or-qbarXT-hard-blocker.md`

## Decision

`{DECISION}`

## What moved forward

- Ordered `Qbar_XH_abs` into denominator/projector gate plus bulk/edge/shadow numerator families.
- Selected `Q_edge_shell_abs` as the cleanest first source-numerator fill row.
- Kept `M_lower`, `||Pi_M^H||` and `E_PiM_comm` as mandatory pre-score gates.
- Preserved qbarXT EM/F2 as a parallel derivation hard blocker.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
"""
    write_text(RESUME_PATH, resume)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr_source_numerator_fill_queue",
        "4763 selects Qedge shell as the first QbarXH source-numerator fill and identifies Mlower/PiM as the mandatory score gate.",
        "Generated source register, numerator audit, first-fill selection, Qedge shell contract, denominator/projector gate, qbarXT blocker rows, product update, route matrix, gates, firewalls, decision, status, next target and validation.",
        "QbarXH_source_numerator_first_fill_Qedge_shell_Mlower_PiM_gate_nonclaim",
        NEXT_TARGET,
        "Scoring QbarXH with symbolic denominator/projector terms or claiming compact support kills edge shell without trace/velocity/birth proof.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need denominator/projector lock or Qedge shell source-row values/zero certificates.",
        "QbarXH source numerator first fill or qbarXT hard blocker",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    numerator_rows: list[dict[str, Any]],
    fill_rows: list[dict[str, Any]],
    qedge_rows: list[dict[str, Any]],
    denom_rows: list[dict[str, Any]],
    blocker_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4763_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4763_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4763_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4763_2_numerator_order", "numerator audit selects Qedge shell and keeps denominator gate", any(row["quantity"] == "Q_edge_shell_abs" and "SELECTED" in row["status"] for row in numerator_rows) and any(row["quantity"].startswith("M_lower") or row["quantity"] == "M_lower, ||Pi_M^H||, E_PiM_comm" for row in numerator_rows), str(NUMERATOR_AUDIT_CSV)))
    checks.append(("VAL4763_3_first_fill", "first-fill selector chooses denominator gate and Qedge shell", any(row["target_quantity"] == "Q_edge_shell_abs" and row["selection_status"] == "SELECTED_FIRST_NUMERATOR_ROW" for row in fill_rows) and any(row["target_quantity"].startswith("M_lower") and row["selection_status"] == "GATE_BEFORE_SCORING" for row in fill_rows), str(FIRST_FILL_CSV)))
    checks.append(("VAL4763_4_qedge_contract", "Qedge shell contract includes trace velocity birth test kernel total", all(any(field in row["field"] for row in qedge_rows) for field in ["rho_H_trace_norm", "V_n_bound", "mu_birth_TV", "Phi_edge", "W_lambda_edge_max", "Q_edge_shell_abs"]), str(QEDGE_CONTRACT_CSV)))
    checks.append(("VAL4763_5_denominator_gate", "denominator gate keeps Mlower PiM commutator missing/active", any(row["quantity"] == "M_lower" and "MISSING" in row["current_status"] for row in denom_rows) and any(row["quantity"] == "E_PiM_comm" and "MISSING" in row["current_status"] for row in denom_rows), str(DENOMINATOR_GATE_CSV)))
    checks.append(("VAL4763_6_qbarxt_blocker", "qbarXT EM/F2 hard blocker retained", any(row["object"] == "F_Q^2 coefficient throat" and "UNSIGNED" in row["status"] for row in blocker_rows) and any(row["object"] == "hidden Hom into Coeff(F_Q^2)" and "COUNTERMODEL" in row["status"] for row in blocker_rows), str(QBARXT_BLOCKER_CSV)))
    checks.append(("VAL4763_7_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4763_8_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4763_9_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4763_10_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4763_11_claim_row", "claim row L-605 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4763_12_resume", "resume points from 4763 to 4764", "4763-Y5" in resume_text and "4764-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4763_13_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
    overall = all(passed for _, _, passed, _ in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, check, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4763_OVERALL",
            "check": "all 4763 QbarXH numerator first-fill checks pass",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    numerator_rows = numerator_audit_rows(timestamp)
    fill_rows = first_fill_rows(timestamp)
    qedge_rows = qedge_contract_rows(timestamp)
    denom_rows = denominator_gate_rows(timestamp)
    blocker_rows = qbarxt_blocker_rows(timestamp)
    product_rows = product_update_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(NUMERATOR_AUDIT_CSV, numerator_rows)
    write_csv(FIRST_FILL_CSV, fill_rows)
    write_csv(QEDGE_CONTRACT_CSV, qedge_rows)
    write_csv(DENOMINATOR_GATE_CSV, denom_rows)
    write_csv(QBARXT_BLOCKER_CSV, blocker_rows)
    write_csv(PRODUCT_UPDATE_CSV, product_rows)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, numerator_rows, fill_rows, qedge_rows, denom_rows, blocker_rows, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, numerator_rows, fill_rows, qedge_rows, denom_rows, blocker_rows, gates, timestamp))


if __name__ == "__main__":
    main()
