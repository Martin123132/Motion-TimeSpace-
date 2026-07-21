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

CHECKPOINT = "4739"
CLAIM_ID = "L-581"
MARKER = "PPC4161_CDELTAKDIV_PROFILE_ROW_AND_RI_COMMUTATOR_ZERO_OR_QUARANTINE_OWNER_PROOF_4739"
PACKET_MARKER = "PPC4161_PACKET_CDELTAKDIV_PROFILE_ROW_AND_RI_COMMUTATOR_ZERO_OR_QUARANTINE_OWNER_PROOF_4739"
DECISION = "DELTAKDIV_AND_TFRI_COMMUTATOR_ZERO_CONDITIONS_DERIVED_QUARANTINE_OWNER_CONTRACT_RETAINED_NONCLAIM"
NEXT_TARGET = "4740-Y5-R2FR-parent-tracefree-RI-owner-action-block-or-transition-finite-residual-runner.md"

DOC_PATH = POST / "4739-Y5-R2FR-CdeltaKdiv-profile-row-and-RI-commutator-zero-or-quarantine-owner-proof.md"
FORMAL_PATH = FORMAL / "755-PPC4161-CdeltaKdiv-profile-row-and-RI-commutator-zero-or-quarantine-owner-proof.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4739_SOURCE_REGISTER.csv"
CDELTAK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4739_CDELTAKDIV_ZERO_OR_BOUND_LAW.csv"
CTFRI_CSV = SOURCE_DIR / "P8_Y5_R2FR_4739_TFRI_COMMUTATOR_ZERO_OR_BOUND_LAW.csv"
QUARANTINE_PROOF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4739_QUARANTINE_OWNER_PROOF_ATTEMPT.csv"
MATTER_GR_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4739_ORDINARY_MATTER_GR_PRESERVATION_GATE.csv"
FINITE_SCORE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4739_FINITE_RESIDUAL_SCORE_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4739_ROUTE_SELECTION_MATRIX.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4739_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4739_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4739_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4739_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4739_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4739_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4739_0_4738_next", SOURCE_DIR / "P8_Y5_R2FR_4738_NEXT_TARGET.csv", "Try to prove C_DeltaK_div=0 and C_TF_RI=0", "4738 handoff"),
    ("SRC4739_1_4738_finite", SOURCE_DIR / "P8_Y5_R2FR_4738_FINITE_RESIDUAL_ROWS.csv", "FIN4738_1_CDeltaKdiv", "4738 finite residual row"),
    ("SRC4739_2_4738_parent", SOURCE_DIR / "P8_Y5_R2FR_4738_PARENT_ACTION_OWNER_CONTRACT.csv", "PACT4738_4_deltaK_kernel", "DeltaK kernel contract"),
    ("SRC4739_3_4738_quarantine", SOURCE_DIR / "P8_Y5_R2FR_4738_CONSERVATION_QUARANTINE_EQUATIONS.csv", "QUAR4738_3_metric_kernel", "Rloc quarantine kernel"),
    ("SRC4739_4_4738_derivation", SOURCE_DIR / "P8_Y5_R2FR_4738_TRACEFREE_RIGHT_INVERSE_DERIVATION.csv", "TFRI4738_6_deltaK_remainder", "DeltaK remainder law"),
    ("SRC4739_5_357_bound", FORMAL / "357-PPC4161-Khat-right-inverse-parent-signature-or-DeltaK-divergence-bound.md", "C_DeltaK_div :=", "prior CDeltaKdiv definition"),
    ("SRC4739_6_357_CRI", FORMAL / "357-PPC4161-Khat-right-inverse-parent-signature-or-DeltaK-divergence-bound.md", "C_RI         :=", "prior RI commutator definition"),
    ("SRC4739_7_4341_bounds", SOURCE_DIR / "P8_Y5_R2FR_4341_BOUND_ROWS.csv", "BND4341_3_CRI", "4341 bound rows"),
    ("SRC4739_8_4138_shape", SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT.csv", "TF4138_0_tensor_shape", "trace-free Hessian shape precedent"),
    ("SRC4739_9_4138_bound", SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_ZERO_THEOREM_OR_BOUND.csv", "TB4138_2_master_bound", "trace-free residual bound precedent"),
    ("SRC4739_10_4282_kernel", SOURCE_DIR / "P8_Y5_R2FR_4282_PROJECTOR_KERNEL_AUDIT.csv", "PK4282_1_response_kernel_target", "response-kernel target"),
    ("SRC4739_11_4282_not_derived", SOURCE_DIR / "P8_Y5_R2FR_4282_PROJECTOR_KERNEL_AUDIT.csv", "PK4282_2_kernel_not_derived", "kernel not derived status"),
    ("SRC4739_12_134_owner", FORMAL / "134-conservation-owned-quarantine-equations.md", "q_tr^nu + nabla_mu K_own^{mu nu} = 0.", "conservation owner equation"),
    ("SRC4739_13_135_preserve", FORMAL / "135-quarantine-projector-parent-origin.md", "R_loc acting on matter sources must remain nonzero and reduce to GR/Newton.", "ordinary matter preservation"),
    ("SRC4739_14_298_response", FORMAL / "298-PPC4161-transition-shell-cancellation-projector-theorem-or-profile-source-rows.md", "R_loc q_tr = 0,", "Rloc response theorem form"),
    ("SRC4739_15_528_tracefree_limit", FORMAL / "528-PPC4161-Khat-trace-match-or-RKtrace-finite-row.md", "tracefree sector still has nonzero tidal/anisotropic pieces", "tracefree does not solve all components"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    CDELTAK_CSV,
    CTFRI_CSV,
    QUARANTINE_PROOF_CSV,
    MATTER_GR_GATE_CSV,
    FINITE_SCORE_CSV,
    ROUTE_MATRIX_CSV,
    GATES_CSV,
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
    fieldnames = list(rows[0].keys())
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def source_path(source_id: str) -> str:
    for row_id, path_object, _needle, _role in SOURCE_SPECS:
        if row_id == source_id:
            return str(path_object)
    raise KeyError(source_id)


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


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def c_delta_k_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CDK4739_0_definition",
            "C_DeltaK_div",
            "C_DeltaK_div=||P_loc nabla_mu D_v Delta_K^{mu nu}||_obs/a_ref",
            "definition inherited from 4341/4738",
            "DEFINED",
            "SRC4739_1_4738_finite",
        ),
        (
            "CDK4739_1_TT_kernel_zero",
            "TT/projected-kernel zero",
            "If Delta_K=Pi_TT[U] and P_loc div D_v Pi_TT[U]=0 with fixed metric/projector/domain, then C_DeltaK_div=0.",
            "This is the sharp zero condition: not Delta_K=0, but projected transverse divergence zero.",
            "EXACT_CONDITIONAL_ZERO_LAW",
            "SRC4739_2_4738_parent",
        ),
        (
            "CDK4739_2_superpotential_zero",
            "superpotential/boundary zero",
            "If Delta_K^{mu nu}=nabla_alpha nabla_beta U^{mu alpha nu beta} with Riemann symmetries and fixed boundary/collar, then div Delta_K is boundary/curvature commutator only.",
            "Flat/fixed-boundary pieces vanish; curved or moving-boundary pieces become explicit residual rows.",
            "BOUNDARY_TOPOLOGICAL_CONDITIONAL_ROUTE",
            "SRC4739_14_298_response",
        ),
        (
            "CDK4739_3_bound_law",
            "finite bound",
            "C_DeltaK_div <= (||P_loc||/a_ref)(C_TTleak+C_curvU+C_support+C_boundary+C_readout+C_projector)",
            "The first nonclaim score row is a component envelope, not a naked placeholder.",
            "FINITE_COMPONENT_BOUND_DERIVED",
            "SRC4739_5_357_bound",
        ),
        (
            "CDK4739_4_current_status",
            "current branch",
            "No live parent certificate currently proves Delta_K is TT/projected-kernel, superpotential-boundary-null, or finite-source scored.",
            "Zero route is real but unsigned; finite rows remain nonclaim.",
            "ZERO_NOT_CLAIMED",
            "SRC4739_15_528_tracefree_limit",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "source_id": source_id,
            "source_path": source_path(source_id),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, formula, meaning, status, source_id in specs
    ]


def c_tfri_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CTF4739_0_definition",
            "C_TF_RI",
            "C_TF_RI=||P_loc[D_v,nabla_mu R_T]Gamma_eff||_obs/a_ref",
            "right-inverse/domain commutator definition",
            "DEFINED",
            "SRC4739_6_357_CRI",
        ),
        (
            "CTF4739_1_commutator_split",
            "commutator split",
            "[D_v,P_loc nabla R_T]Gamma=P_loc([D_v,nabla]R_T Gamma+nabla[D_v,R_T]Gamma)+[D_v,P_loc]nabla R_T Gamma",
            "The only allowed zero is operator stability, not ignoring D_v.",
            "DERIVED_SPLIT",
            "SRC4739_4_4738_derivation",
        ),
        (
            "CTF4739_2_fixed_data_zero",
            "fixed Green/domain zero",
            "If D_v g=D_v nabla=D_v P_loc=D_v boundary=D_v Green_T=0 and R_T is linear on the same domain, then [D_v,nabla R_T]Gamma_eff=0.",
            "This is the clean theorem-zero clause for the RI commutator.",
            "EXACT_CONDITIONAL_ZERO_LAW",
            "SRC4739_3_4738_quarantine",
        ),
        (
            "CTF4739_3_curved_domain_leak",
            "curved/domain leak",
            "If geometry, support, shell collar, boundary, readout order, or Green zero-mode moves under D_v, C_TF_RI receives those terms.",
            "The commutator is where nonlocal inverse data leaks back into local PPN/R10/clocks.",
            "LEAK_CHANNEL_IDENTIFIED",
            "SRC4739_8_4138_shape",
        ),
        (
            "CTF4739_4_bound_law",
            "finite bound",
            "C_TF_RI <= (||P_loc||/a_ref)(C_DvP+C_conn+C_Green+C_zeroMode+C_curv+C_domain+C_boundary+C_readout)",
            "This is the scoreable fallback if fixed-data zero is not signed.",
            "FINITE_COMPONENT_BOUND_DERIVED",
            "SRC4739_9_4138_bound",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "source_id": source_id,
            "source_path": source_path(source_id),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, formula, meaning, status, source_id in specs
    ]


def quarantine_proof_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "QOP4739_0_define_response",
            "R_loc := Pi_obs L_GR^{-1} Sigma_metric on the local collar.",
            "Response operator must be derived from the same EH/Newton branch, not invented as a label projector.",
            "DEFINITION_TARGET",
            "SRC4739_10_4282_kernel",
        ),
        (
            "QOP4739_1_owner_balance",
            "q_tr^nu+nabla_mu K_own^{mu nu}=0.",
            "The transition current stays conserved/owned; it is not deleted.",
            "EQUATION_STAGED",
            "SRC4739_12_134_owner",
        ),
        (
            "QOP4739_2_metric_null_sufficient_condition",
            "If delta S_tr/delta g_loc=0 up to boundary/topological terms and boundary readout is silent, then Sigma_metric[q_tr]=0 and R_loc q_tr=0.",
            "This is the actual quarantine proof route.",
            "EXACT_CONDITIONAL_THEOREM",
            "SRC4739_14_298_response",
        ),
        (
            "QOP4739_3_kernel_bound_fallback",
            "If metric-null proof fails, C_kernel=||R_loc q_tr||_obs/a_ref must be source-backed and below the imported transition budget.",
            "No closure-pass without a response theorem or finite sourced leakage.",
            "FINITE_KERNEL_BOUND_REQUIRED",
            "SRC4739_11_4282_not_derived",
        ),
        (
            "QOP4739_4_current_status",
            "Current parent material identifies the response-kernel route but does not derive the action block or prove q_tr in Ker(R_loc).",
            "Quarantine remains nonclaim until the parent action block is written or the finite runner scores it.",
            "NOT_PARENT_SIGNED",
            "SRC4739_11_4282_not_derived",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "proof_id": proof_id,
            "statement": statement,
            "meaning": meaning,
            "status": status,
            "source_id": source_id,
            "source_path": source_path(source_id),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for proof_id, statement, meaning, status, source_id in specs
    ]


def matter_gr_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "MGR4739_0_matter_nonzero",
            "R_loc T_matter != 0",
            "ordinary visible matter remains in the metric response channel",
            "REQUIRED_FOR_GR_LIMIT",
        ),
        (
            "MGR4739_1_newton_limit",
            "L_GR^{-1} Sigma_metric[T_matter] -> Poisson/Newton in weak slow local limit",
            "kernel/quarantine theorem cannot switch off Newtonian gravity",
            "REQUIRED_FOR_NEWTON_LIMIT",
        ),
        (
            "MGR4739_2_transition_null_only",
            "R_loc q_tr=0 while R_loc T_matter survives",
            "transition current must be a special response-null direction, not a universal source eraser",
            "REQUIRED_FOR_LOCAL_GR_CLAIM",
        ),
        (
            "MGR4739_3_current_status",
            "No current file proves the above three clauses from one parent action block.",
            "claim remains blocked but the exact acceptance test is now explicit",
            "UNSIGNED_NONCLAIM",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "meaning": meaning,
            "status": status,
            "source_id": "SRC4739_13_135_preserve",
            "source_path": source_path("SRC4739_13_135_preserve"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, meaning, status in specs
    ]


def finite_score_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "FS4739_0_transition_vector",
            "Y_a^transition",
            "Y_a <= Pi_Delta C_DeltaK_div + Pi_RI C_TF_RI + Pi_conn C_conn + Pi_bdry C_boundary + Pi_kernel C_kernel",
            "PPN/R10/clocks/orbital/WEP arena projection norms",
            "SCORE_VECTOR_FORMULA_READY_INPUTS_OPEN",
        ),
        (
            "FS4739_1_CDeltaK_components",
            "C_DeltaK_div",
            "C_DeltaK_div <= (||P_loc||/a_ref)(C_TTleak+C_curvU+C_support+C_boundary+C_readout+C_projector)",
            "component values, units, source paths, fixed-before-scoring flags",
            "SOURCE_ROWS_REQUIRED",
        ),
        (
            "FS4739_2_CTFRI_components",
            "C_TF_RI",
            "C_TF_RI <= (||P_loc||/a_ref)(C_DvP+C_conn+C_Green+C_zeroMode+C_curv+C_domain+C_boundary+C_readout)",
            "operator/domain/Green commutator values",
            "SOURCE_ROWS_REQUIRED",
        ),
        (
            "FS4739_3_Ckernel_components",
            "C_kernel",
            "C_kernel=||Pi_obs L_GR^{-1} Sigma_metric[q_tr]||_obs/a_ref",
            "derived response operator or finite leakage source",
            "SOURCE_ROWS_REQUIRED",
        ),
        (
            "FS4739_4_promotion_budget",
            "transition budget",
            "all finite rows must beat the existing transition suppression target without retuning",
            "arena-specific PPN/R10/clock/orbital/WEP budgets",
            "BUDGET_COMPARISON_REQUIRED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "formula": formula,
            "required_inputs": required_inputs,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, formula, required_inputs, status in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "ROUTE4739_0_exact_DeltaK_TT",
            "DeltaK_projected_TT_kernel",
            "best_weaker_zero_route",
            "Prove Delta_K lies in the projected transverse kernel with fixed geometry/readout.",
            "needs parent projector/adoption certificate",
        ),
        (
            "ROUTE4739_1_fixed_RI_commutator",
            "fixed_tracefree_RI_operator",
            "best_operator_zero_route",
            "Prove fixed same-domain Green/operator data so [D_v,nabla R_T]Gamma_eff=0.",
            "needs parent action/boundary/domain block",
        ),
        (
            "ROUTE4739_2_metric_null_quarantine",
            "metric_null_quarantine_owner",
            "best_conservation_route",
            "Derive delta S_tr/delta g_loc=0 while q_tr+div K_own=0 and matter remains GR/Newton.",
            "needs parent action block",
        ),
        (
            "ROUTE4739_3_finite_runner",
            "finite_transition_residual_score",
            "fallback_if_zero_fails",
            "Source C_DeltaK_div, C_TF_RI, C_conn, C_boundary and C_kernel and compare against arenas.",
            "needs numeric/source-backed rows",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "status": status,
            "detail": detail,
            "next_requirement": next_requirement,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, status, detail, next_requirement in specs
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4739_0_CDeltaK_zero", "Promote C_DeltaK_div=0 only with parent-signed projected TT/superpotential kernel and fixed readout.", "closed_unsigned", False),
        ("GATE4739_1_CTFRI_zero", "Promote C_TF_RI=0 only with fixed geometry/projector/Green/domain data under D_v.", "closed_unsigned", False),
        ("GATE4739_2_quarantine_owner", "Promote quarantine only with metric-null owner action plus q_tr+div K_own=0.", "closed_unsigned", False),
        ("GATE4739_3_matter_GR_preserved", "Promote local GR only if ordinary matter remains in the GR/Newton response channel.", "closed_unsigned", False),
        ("GATE4739_4_finite_score", "If zeros fail, all component rows need numeric units, sources, arena projections and budget comparison.", "closed_inputs_open", False),
        ("GATE4739_5_no_public_claim", "No local-GR, Newton, PPN, R10, clock, orbital or public claim from 4739.", "closed_firewall", False),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "valid_for_claim": valid_for_claim,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, valid_for_claim in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4739_0_no_tracefree_overclaim", "Do not treat trace-free shape as divergence zero; only projected divergence/kernel proof counts."),
        ("FW4739_1_no_fixed_data_assumption", "Do not set RI commutator to zero unless metric, projector, Green data, boundary and domain are fixed under D_v."),
        ("FW4739_2_no_metric_null_erasure", "Do not use a quarantine kernel that also erases ordinary matter gravity."),
        ("FW4739_3_no_symbolic_finite_pass", "Symbolic component rows are source-ready but not score-ready evidence."),
        ("FW4739_4_no_GitHub_action", "No GitHub action is performed by this checkpoint."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "firewall": firewall,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, firewall in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "summary": "4739 derives exact conditional zero laws for C_DeltaK_div and C_TF_RI, plus the metric-null quarantine owner proof contract. The zero routes are mathematically real but parent-unsigned, so finite transition residual scoring remains the fallback.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4739_0_local_only",
            "status": "local_only_private_checkpoint",
            "detail": "Generated local post-checkpoint and formalization files only.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4739_1_science_verdict",
            "status": "zero_conditions_derived_parent_signature_missing",
            "detail": "The transition problem is now reduced to three exact gates: projected DeltaK transverse kernel, fixed trace-free RI commutator, and metric-null owner action preserving ordinary GR/Newton.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "4739 turned vague blockers into exact acceptance clauses; the next step must either write the parent owner action block that signs them or run the finite residual score.",
            "preferred_route": "Attempt a parent trace-free RI/metric-null owner action with multiplier, fixed Green/domain data, TT DeltaK projector and ordinary matter GR/Newton preservation.",
            "fallback_route": "Build a finite transition residual runner for C_DeltaK_div, C_TF_RI, C_conn, C_boundary and C_kernel with arena projections.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    timestamp: str,
    c_delta_k: list[dict[str, Any]],
    c_tfri: list[dict[str, Any]],
    quarantine: list[dict[str, Any]],
    matter_gr: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4739 Y5 R2FR: CdeltaKdiv Profile Row And RI Commutator Zero Or Quarantine Owner Proof

Generated: `{timestamp}`

## Summary

- Work is local-only and private.
- This checkpoint does not merely say "missing": it derives the exact conditions under which the remaining transition residuals vanish.
- `C_DeltaK_div=0` requires `Delta_K` to live in a projected transverse/superpotential kernel with fixed readout.
- `C_TF_RI=0` requires fixed same-domain trace-free right-inverse data under `D_v`.
- The quarantine route becomes a conditional theorem only if the owner action is metric-null while ordinary matter still gives GR/Newton.

## DeltaK Divergence Result

```text
C_DeltaK_div = ||P_loc nabla_mu D_v Delta_K^{{mu nu}}||_obs / a_ref
```

The sharp zero is:

```text
P_loc nabla_mu D_v Delta_K^{{mu nu}} = 0
```

which can happen by a parent-signed transverse/projected kernel or by a superpotential/boundary-null construction. Otherwise:

```text
C_DeltaK_div <= (||P_loc||/a_ref)
  (C_TTleak + C_curvU + C_support + C_boundary + C_readout + C_projector)
```

## Trace-Free RI Commutator Result

```text
C_TF_RI = ||P_loc [D_v,nabla_mu R_T] Gamma_eff||_obs / a_ref
```

The commutator split is:

```text
[D_v,P_loc nabla R_T]Gamma
  = P_loc([D_v,nabla]R_T Gamma + nabla[D_v,R_T]Gamma)
  + [D_v,P_loc]nabla R_T Gamma
```

So `C_TF_RI=0` only if the geometry, projector, Green operator, zero-mode rule, boundary and domain are fixed under the relevant vertical variation.

## CDeltaK Rows

{bullets(c_delta_k, "row_id", "formula")}

## C_TF_RI Rows

{bullets(c_tfri, "row_id", "formula")}

## Quarantine Owner Proof

{bullets(quarantine, "proof_id", "statement")}

## Ordinary Matter GR Gate

{bullets(matter_gr, "gate_id", "gate")}

## Finite Score Rows

{bullets(finite, "row_id", "formula")}

## Route Matrix

{bullets(routes, "route_id", "route")}

## Promotion Gates

{bullets(gates, "gate_id", "gate")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`

No GitHub action was performed.
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 755 PPC4161: CdeltaKdiv Profile Row And RI Commutator Zero Or Quarantine Owner Proof

Generated: `{timestamp}`

## Current Status

`{DECISION}`

## Exact Zero Conditions

For the residual split:

```text
q_tr^nu = -nabla_mu Delta_K^{{mu nu}} + C_TF_RI^nu + C_conn^nu + B_boundary^nu + Q_kernel^nu
```

the non-cheating zero route is:

```text
P_loc div D_v Delta_K = 0
[D_v, P_loc div R_T] Gamma_eff = 0
R_loc q_tr = 0
R_loc T_matter != 0 -> GR/Newton
```

## What This Changes

The next proof is no longer "make Khat cancel". It has three concrete signatures:

1. `Delta_K` is parent-owned as projected transverse/superpotential-null.
2. `R_T` is parent-owned with fixed Green/domain/boundary data.
3. The owner/quarantine action is metric-null for `q_tr` but not for ordinary matter.

## Fallback

If any signature fails, score:

```text
Y_a <= Pi_Delta C_DeltaK_div + Pi_RI C_TF_RI + Pi_conn C_conn + Pi_bdry C_boundary + Pi_kernel C_kernel
```

with source-backed arena rows before any local-GR, Newtonian, PPN, R10, clock or orbital claim.

## Next

`{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""

## {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Result: `C_DeltaK_div=0` now has exact clauses: projected transverse kernel or superpotential/boundary-null `Delta_K` with fixed readout.
- Result: `C_TF_RI=0` now requires fixed geometry/projector/Green/domain data under `D_v`.
- Quarantine result: `R_loc q_tr=0` is promoted only if a metric-null owner action is derived while ordinary matter remains GR/Newton.
- Next local route: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""

## {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet update: transition-shell safety is reduced to three exact parent signatures or to a finite residual score vector.
- Claim status: nonclaim; no local-GR/PPN/R10/Newtonian pass.
""",
    )
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4739-Y5-R2FR-CdeltaKdiv-profile-row-and-RI-commutator-zero-or-quarantine-owner-proof.md`

## Decision

`{DECISION}`

## What moved forward

- `C_DeltaK_div=0` was reduced to a parent-signed projected TT/superpotential-kernel condition.
- `C_TF_RI=0` was reduced to fixed same-domain trace-free right-inverse data under `D_v`.
- The quarantine proof was made exact: metric-null owner action plus `q_tr + div K_own = 0`, while ordinary matter still gives GR/Newton.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def add_claim_once(timestamp: str) -> None:
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_bridge",
        "claim": "4739 derives exact conditional zero conditions for Delta_K projected divergence, trace-free right-inverse commutator silence, and metric-null quarantine ownership preserving ordinary GR/Newton.",
        "current_evidence": "Generated source register, CDeltaKdiv zero/bound law, C_TF_RI commutator law, quarantine owner proof attempt, matter-GR preservation gate, finite score rows, route matrix, gates, firewalls, decision, status, next target and validation.",
        "status": "DeltaKdiv_CTFRI_quarantine_zero_conditions_derived_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating conditional zero clauses as parent-signed, or using a metric-null quarantine that also erases ordinary matter gravity.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Parent action block, fixed Green/domain data, DeltaK TT/superpotential ownership, finite source rows and arena projections remain unsigned.",
        "title": "CdeltaKdiv profile row and RI commutator zero or quarantine owner proof",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    for fieldname in fieldnames:
        new_row.setdefault(fieldname, "")
    rows.append(new_row)
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def cleanup_pycache() -> None:
    pycache_path = POST / "scripts" / "__pycache__"
    if pycache_path.exists():
        shutil.rmtree(pycache_path)


def validation_rows(
    sources: list[dict[str, Any]],
    c_delta_k: list[dict[str, Any]],
    c_tfri: list[dict[str, Any]],
    quarantine: list[dict[str, Any]],
    matter_gr: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    generated_with_validation = GENERATED_CSVS + [VALIDATION_CSV]
    checks = [
        ("VAL4739_0_sources_exist", all(source["exists"] for source in sources), "all cited 4739 source paths exist"),
        ("VAL4739_1_needles_found", all(source["needle_found"] for source in sources), "all cited 4739 source needles found"),
        ("VAL4739_2_CDeltaK_zero_law", any(row["row_id"] == "CDK4739_1_TT_kernel_zero" for row in c_delta_k), "CDeltaK projected-kernel zero law written"),
        ("VAL4739_3_CDeltaK_bound", any(row["row_id"] == "CDK4739_3_bound_law" for row in c_delta_k), "CDeltaK finite component bound written"),
        ("VAL4739_4_CTFRI_split", any(row["row_id"] == "CTF4739_1_commutator_split" for row in c_tfri), "TFRI commutator split written"),
        ("VAL4739_5_CTFRI_zero", any(row["row_id"] == "CTF4739_2_fixed_data_zero" for row in c_tfri), "TFRI fixed-data zero condition written"),
        ("VAL4739_6_quarantine_theorem", any(row["proof_id"] == "QOP4739_2_metric_null_sufficient_condition" for row in quarantine), "metric-null quarantine theorem condition written"),
        ("VAL4739_7_matter_GR_gate", any(row["gate_id"] == "MGR4739_2_transition_null_only" for row in matter_gr), "ordinary matter GR preservation gate written"),
        ("VAL4739_8_finite_vector", any(row["row_id"] == "FS4739_0_transition_vector" for row in finite), "finite transition residual vector written"),
        ("VAL4739_9_routes", len(routes) >= 4 and any(row["route"] == "finite_transition_residual_score" for row in routes), "route matrix includes finite fallback"),
        ("VAL4739_10_claim_gates_closed", all(row["valid_for_claim"] is False for row in gates), "all claim gates remain closed"),
        ("VAL4739_11_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4739_12_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4739_13_claim_row_added", CLAIM_ID in read_text(CLAIMS_PATH), "claims register contains L-581"),
        ("VAL4739_14_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4740 next target"),
        ("VAL4739_15_csv_parse", all(parse_csv(csv_path) for csv_path in generated_with_validation if csv_path.exists()), "all generated 4739 CSV files parse cleanly"),
        ("VAL4739_16_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4739_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "4739 CDeltaKdiv profile row and RI commutator zero or quarantine owner proof validation",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    c_delta_k = c_delta_k_rows(timestamp)
    c_tfri = c_tfri_rows(timestamp)
    quarantine = quarantine_proof_rows(timestamp)
    matter_gr = matter_gr_gate_rows(timestamp)
    finite = finite_score_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(CDELTAK_CSV, c_delta_k)
    write_csv(CTFRI_CSV, c_tfri)
    write_csv(QUARANTINE_PROOF_CSV, quarantine)
    write_csv(MATTER_GR_GATE_CSV, matter_gr)
    write_csv(FINITE_SCORE_CSV, finite)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, c_delta_k, c_tfri, quarantine, matter_gr, finite, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, c_delta_k, c_tfri, quarantine, matter_gr, finite, routes, gates, timestamp))


if __name__ == "__main__":
    main()
