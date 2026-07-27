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

CHECKPOINT = "4767"
CLAIM_ID = "L-609"
MARKER = "PPC4161_PARENT_SOURCE_QBASIC_SIGNATURE_OR_POYNTING_WALL_NUMERIC_BOUND_4767"
PACKET_MARKER = "PPC4161_PACKET_PARENT_SOURCE_QBASIC_SIGNATURE_OR_POYNTING_WALL_NUMERIC_BOUND_4767"
DECISION = "PARENT_SOURCE_QBASIC_CONTRACT_DERIVED_PRIVATE_BRANCH_SUPPORT_FOUND_NOT_SINGLE_PARENT_SIGNED_POYNTING_NUMERIC_BOUND_STAGED_NONCLAIM"
NEXT_TARGET = "4768-Y5-R2FR-source-action-operator-inventory-no-prefactor-or-Poynting-wall-first-value.md"

DOC_PATH = POST / "4767-Y5-R2FR-parent-source-qbasic-signature-or-Poynting-wall-numeric-bound.md"
FORMAL_PATH = FORMAL / "783-PPC4161-parent-source-qbasic-signature-or-Poynting-wall-numeric-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4767_SOURCE_REGISTER.csv"
CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4767_PARENT_SOURCE_QBASIC_CONTRACT.csv"
SIGNATURE_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4767_SINGLE_PARENT_SIGNATURE_AUDIT.csv"
PROOF_CHAIN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4767_MEASURE_SUPPORT_PROOF_CHAIN.csv"
POYNTING_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4767_POYNTING_WALL_NUMERIC_BOUND_PACK.csv"
RESIDUAL_VECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4767_SOURCE_QBASIC_RESIDUAL_VECTOR.csv"
QEDGE_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4767_QEDGE_SHELL_AND_QBAR_UPDATE.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4767_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4767_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4767_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4767_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4767_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4767_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4767_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4767_0_4766_decision", SOURCE_DIR / "P8_Y5_R2FR_4766_DECISION.csv", "SOURCE_SUPPORT_INVARIANCE_LEMMA_DERIVED", "4766 handoff decision"),
    ("SRC4767_1_4766_support", SOURCE_DIR / "P8_Y5_R2FR_4766_SUPPORT_INVARIANCE_THEOREM.csv", "SIT4766_1_exact_qbasic_measure", "4766 q-basic measure support route"),
    ("SRC4767_2_4766_signature", SOURCE_DIR / "P8_Y5_R2FR_4766_PARENT_SOURCE_QBASIC_SIGNATURE_PACK.csv", "PSQ4766_0_source_action", "4766 source-qbasic signature pack"),
    ("SRC4767_3_3560_support", SOURCE_DIR / "P8_Y5_R2FR_3560_SOURCE_SUPPORT_QBASIC_THEOREM.csv", "SWT3560_1_qbasic_support_lemma", "3560 source-support q-basic theorem"),
    ("SRC4767_4_density_status", SOURCE_DIR / "P8_Y5_Hilbert_source_density_qbasic_status.csv", "conditional pullback theorem", "3561 Hilbert density q-basic status"),
    ("SRC4767_5_4587_density", SOURCE_DIR / "P8_Y5_R2FR_4587_DENSITY_QBASIC_THEOREM.csv", "DQT4587_1_qbasic_density_zero", "4587 Hilbert density theorem"),
    ("SRC4767_6_4277_matter", SOURCE_DIR / "P8_Y5_R2FR_4277_MATTER_INTERFACE_DESCENT_THEOREM.csv", "AD4277_1_action_factorization", "4277 matter action factorization"),
    ("SRC4767_7_3989_no_prefactor", SOURCE_DIR / "P8_Y5_R2FR_3989_MATTER_DESCENT_NO_SOURCE_PREFACTOR_THEOREM.csv", "NP3989_0_no_prefactor_criterion", "3989 no source-prefactor theorem"),
    ("SRC4767_8_4322_hidden", SOURCE_DIR / "P8_Y5_R2FR_4322_MATTER_DESCENT_AUDIT.csv", "AUD4322_3_hidden_tax", "4322 hidden-tail audit"),
    ("SRC4767_9_4649_selector", SOURCE_DIR / "P8_Y5_R2FR_4649_PARENT_GR_SELECTOR_CONTRACT.csv", "GRSEL4649_3_Hilbert_source", "4649 GR selector source contract"),
    ("SRC4767_10_4650_signature", SOURCE_DIR / "P8_Y5_R2FR_4650_SELECTOR_SIGNATURE_AUDIT.csv", "SIG4650_2_Hilbert_source_owner", "4650 single selector audit"),
    ("SRC4767_11_4714_poynting", SOURCE_DIR / "P8_Y5_R2FR_4714_EM_STRESS_POYNTING_OWNER_THEOREM.csv", "EMP4714_2_Poynting_identity", "4714 Poynting stress identity"),
    ("SRC4767_12_4695_poynting_bound", SOURCE_DIR / "P8_Y5_R2FR_4695_POYNTING_FLUX_ROWS.csv", "FX4695_1_wall_flux_bound", "4695 Poynting wall bound"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    CONTRACT_CSV,
    SIGNATURE_AUDIT_CSV,
    PROOF_CHAIN_CSV,
    POYNTING_BOUND_CSV,
    RESIDUAL_VECTOR_CSV,
    QEDGE_UPDATE_CSV,
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


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| "
        + " | ".join(str(row[column]).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ") for column in columns)
        + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


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


def contract_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "PSC4767_0_parent_action_form",
            "S_src = Sbar_src[q(Phi),Psi,A,theta_bar(q)] + dB_proper + S_top_silent",
            "source action has no direct vertical parent-field leg, no source-only weight, and no post-readout re-entry",
            "CONTRACT_DERIVED_NOT_PARENT_SIGNED",
        ),
        (
            "PSC4767_1_observed_geometry",
            "g_obs,e_obs,tau,star_obs = Obs(q(Phi))",
            "matter, clocks, EM Hodge, support, Hamiltonian mass and readout use one quotient-owned observed branch",
            "CONTRACT_DERIVED_NOT_PARENT_SIGNED",
        ),
        (
            "PSC4767_2_Hilbert_stress",
            "T_total = -2/sqrt(-g_obs) delta S_src/delta g_obs",
            "Hilbert stress is a quotient-owned functional if the parent action and observed branch above are signed",
            "CONDITIONAL_THEOREM_DERIVED",
        ),
        (
            "PSC4767_3_measure_qbasic",
            "mu_H = c^-2 T_total(n,n) dV_obs = mu_bar_H[q(Phi)]",
            "exact Radon-measure q-basicity follows from action descent, not from fitting local mass",
            "CONDITIONAL_MEASURE_THEOREM_DERIVED",
        ),
        (
            "PSC4767_4_support_invariance",
            "W_H=closure(supp mu_H) before readout",
            "if mu_H is q-basic, support is invariant and Q_edge_shell_abs=0 through V_n_bound=0 and mu_birth_TV=0",
            "CONDITIONAL_SUPPORT_INSERT",
        ),
        (
            "PSC4767_5_Poynting_owner",
            "S_i=-T_EM(n,e_i) on the public Maxwell-Hodge Hilbert branch",
            "Poynting is counted once in T_total; open/radiative wall flux is retained as Phi_wall_Poynting_abs",
            "POYNTING_CONTRACT_DERIVED_BOUND_RETAINED",
        ),
        (
            "PSC4767_6_current_verdict",
            "one-parent signature check",
            "private standard-branch support exists, but the corpus still lacks one parent action line signing every clause together",
            "NOT_SINGLE_PARENT_SIGNED_NONCLAIM",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "contract_id": contract_id,
            "required_statement": statement,
            "deduction_role": role,
            "status": status,
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, statement, role, status in specs
    ]


def signature_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SIG4767_0_action_factorization", "source action factors through q", "4277 and 4587 support the standard branch", "PRIVATE_BRANCH_SUPPORT_NOT_GLOBAL"),
        ("SIG4767_1_common_readout", "one g_obs/e_obs/Hodge/tau branch", "4591/4649/4650 support the contract but selector remains unsigned", "UNSIGNED_PARENT_SELECTOR"),
        ("SIG4767_2_constants_labels", "theta, masses, charges, alpha_EM, standards fixed or quotient-owned", "1575/3646 identify this as essential", "UNSIGNED_CONSTANT_MARKER_GATE"),
        ("SIG4767_3_no_prefactor", "no source/species/material label to active-mass weight Hom", "3989 derives exact no-prefactor criterion and countermodel", "UNSIGNED_NO_HOM_GATE"),
        ("SIG4767_4_matter_lift", "matter field lift is gauge/on-shell/proper-boundary silent", "1575 and 3646 retain physical lift as a live gate", "UNSIGNED_MATTER_LIFT_GATE"),
        ("SIG4767_5_Maxwell_Hodge", "same observed Hodge/current owner for EM", "4714 proves Poynting identity conditionally", "UNSIGNED_EM_HODGE_CURRENT_GATE"),
        ("SIG4767_6_support_selector", "W_H chosen as closure(supp mu_H) before readout", "3560/4766 support this if mu_H is parent-owned", "UNSIGNED_SELECTOR_GATE"),
        ("SIG4767_7_boundary_flux", "radiative/Poynting/boundary flux routed explicitly", "4695/4714 supply theorem-or-bound rows", "UNSIGNED_BOUNDARY_FLUX_GATE"),
        ("SIG4767_8_verdict", "all clauses in one parent branch", "not found as a single globally adopted parent action selector", "FAIL_CURRENT_CLAIM_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "signature_id": signature_id,
            "clause": clause,
            "support_found": support,
            "signature_status": status,
            "parent_signed_as_one_branch": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for signature_id, clause, support, status in specs
    ]


def proof_chain_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("MPC4767_0_action", "S_src descends through q", "delta_v S_src=0 for v in ker(Dq)", "requires parent source action form"),
        ("MPC4767_1_Hilbert", "Hilbert variation is with respect to g_obs(q)", "delta_v T_total=0 in the same branch", "requires no hidden Hodge/constant/source marker"),
        ("MPC4767_2_measure", "mu_H=c^-2 T_total(n,n)dV_obs", "mu_H(Phi_s)=mu_H(Phi_0) as a Radon measure", "requires same n,dV,tau/e_obs branch"),
        ("MPC4767_3_support", "W_H=closure(supp mu_H)", "supp mu_H is invariant on vertical fibres", "requires no readout threshold/mask"),
        ("MPC4767_4_shell", "V_n_bound=0 and mu_birth_TV=0", "Q_edge_shell_abs=0 for finite test/kernel ceilings", "requires exact q-basic measure"),
        ("MPC4767_5_Qbar", "Qedge shell is removed from numerator", "Qbar_XH still waits for boundary, shadow, denominator and projector gates", "prevents premature scoring"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "chain_id": chain_id,
            "input_or_step": step,
            "deduction": deduction,
            "remaining_condition": condition,
            "status": "CONDITIONAL_PROOF_CHAIN_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for chain_id, step, deduction, condition in specs
    ]


def poynting_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PWB4767_0_stationary_zero", "Phi_wall_Poynting", "Phi_wall_Poynting=0", "stationary isolated collar, no incoming/apparatus/radiative flux and no net dU_EM/dt or int J.E", "CONDITIONAL_ZERO_UNSIGNED"),
        ("PWB4767_1_dUdt", "dU_EM_dt_abs", "|dU_EM/dt| over declared local collar/time window", "source/model/measurement row with units", "MISSING_NUMERIC_VALUE"),
        ("PWB4767_2_JdotE", "JdotE_abs", "|int_W J.E dV|", "current and field model or stationary zero certificate", "MISSING_NUMERIC_VALUE"),
        ("PWB4767_3_incoming", "Phi_incoming_abs", "incoming/background radiation flux through collar", "environment/radiation bound or zero certificate", "MISSING_NUMERIC_VALUE"),
        ("PWB4767_4_apparatus", "Phi_apparatus_abs", "apparatus/external support flux through collar", "experimental/source collar bound or zero certificate", "MISSING_NUMERIC_VALUE"),
        ("PWB4767_5_total", "Phi_wall_Poynting_abs", "|Phi_wall_Poynting| <= |dU_EM/dt| + |int_W J.E dV| + |Phi_incoming| + |Phi_apparatus|", "all numeric/zero rows PWB4767_1..4", "BOUND_TEMPLATE_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": bound_id,
            "quantity": quantity,
            "formula_or_zero": formula,
            "required_evidence": required,
            "current_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for bound_id, quantity, formula, required, status in specs
    ]


def residual_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRV4767_0_action_vertical", "E_action_vertical", "direct source action dependence not mediated by q", "zero if PSC4767_0 is parent signed"),
        ("SRV4767_1_constant_marker", "E_constant_marker", "vertical masses/charges/alpha/standards/material labels", "zero if theta is fixed or quotient-owned"),
        ("SRV4767_2_source_prefactor", "E_source_prefactor", "source/species/material active-mass weight", "zero if no-Hom/no-prefactor grammar is signed"),
        ("SRV4767_3_matter_lift", "E_matter_lift", "physical matter lift rather than gauge/on-shell silence", "zero if lift is owned/gauge/proper-boundary"),
        ("SRV4767_4_Hodge_EM", "E_Hodge_EM", "independent Hodge/constitutive/current owner", "zero if same Maxwell-Hodge current branch signed"),
        ("SRV4767_5_Poynting_wall", "E_Poynting_wall", "open/radiative EM flux crossing collar", "zero if stationary/no-flux; otherwise Phi_wall_Poynting_abs"),
        ("SRV4767_6_support_selector", "E_support_selector", "support chosen after readout or by fitted threshold", "zero if W_H=closure(supp mu_H) before readout"),
        ("SRV4767_7_boundary_flux", "E_boundary_flux", "Hamiltonian/corner/radiative boundary leak", "zero or source-bound as Q_edge_boundary_abs"),
        ("SRV4767_8_total", "E_source_qbasic_open", "no-cancellation envelope for unsigned source-qbasic signature", "sum of absolute SRV4767_0..7 components"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "residual_id": residual_id,
            "symbol": symbol,
            "meaning": meaning,
            "zero_or_bound_route": route,
            "status": "RESIDUAL_RETAINED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for residual_id, symbol, meaning, route in specs
    ]


def qedge_update_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("QEQ4767_0_exact_branch", "If PSC4767_0..5 are parent-signed, then mu_H is q-basic, W_H is invariant, and Q_edge_shell_abs=0.", "support-invariance shell zero promoted only after one-parent signature", "CONDITIONAL_BRANCH_READY"),
        ("QEQ4767_1_unsigned_branch", "If the parent signature is unsigned, Q_edge_shell_abs stays bounded by the 4765 Reynolds shell law plus E_source_qbasic_open.", "no cancellation across residual components", "BOUND_BRANCH_RETAINED"),
        ("QEQ4767_2_poynting_boundary", "Phi_wall_Poynting_abs feeds Q_edge_boundary_abs or Q_bulk_EM/Poynting, not Q_edge_shell zero.", "keeps waves/Poynting visible", "POYNTING_BOUNDARY_VISIBLE"),
        ("QEQ4767_3_qbar_product", "|Qbar_XH| <= [P_M_bound(|Q_bulk|+Q_edge_boundary_abs+|Q_shadow|)+|E_PiM_comm|]/[M_0(1-epsilon_abs)] only after shell zero plus denominator/projector gates.", "score remains closed", "PRODUCT_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": update_id,
            "rule": rule,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for update_id, rule, meaning, status in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4767_0_contract", "derive parent source-qbasic contract", "done conditionally; the math path is clear", "COMPLETED_CONDITIONAL"),
        ("ROUTE4767_1_signature", "find one parent action line signing all source clauses", "not found; private support is assembled but not global", "FAILED_TO_PROMOTE_NONCLAIM"),
        ("ROUTE4767_2_operator_inventory", "audit actual source action/operator inventory for hidden prefactors and Hodge/current forks", "next best route to promote or reject the contract", "SELECTED_NEXT"),
        ("ROUTE4767_3_Poynting_values", "fill dUdt/JdotE/incoming/apparatus wall-flux rows", "parallel empirical/source-bound route for open collars", "PARALLEL_REQUIRED"),
        ("ROUTE4767_4_denominator", "M0 epsilon PiM Ecomm denominator/projector values", "still required before any Qbar/local score", "PARALLEL_REQUIRED"),
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
        ("PG4767_0_one_parent", "All source-qbasic clauses must be signed by one parent action/readout branch.", "blocks patchwork promotion"),
        ("PG4767_1_no_prefactor", "No source/species/material active-mass weight may survive outside q.", "blocks hidden coupling cheat"),
        ("PG4767_2_no_poynting_double_count", "Poynting is Hilbert stress once or an explicit wall flux, never both.", "blocks EM double count"),
        ("PG4767_3_no_support_mask", "W_H must be source support before readout, not a fitted threshold.", "blocks circular collar"),
        ("PG4767_4_no_score", "No local-GR/Newton/R10/PPN/WEP/clock/orbital/Maxwell claim from 4767.", "keeps checkpoint private/nonclaim"),
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
        ("FW4767_0_no_global_signature", "Do not claim global parent source-qbasicness; one-parent signature is not found.", "NONCLAIM"),
        ("FW4767_1_no_piece_mixing", "Do not mix 4277, 3989, 4650 and 4714 as if they already form one branch.", "NONCLAIM"),
        ("FW4767_2_no_poynting_erasure", "Do not erase open/radiative Poynting wall flux.", "SOURCE_DISCIPLINE"),
        ("FW4767_3_no_Qbar_score", "Do not score QbarXH without denominator/projector/boundary/shadow values.", "NONCLAIM"),
        ("FW4767_4_local_only", "No GitHub action from this checkpoint.", "LOCAL_ONLY"),
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
            "decision_id": "DEC4767_0",
            "decision": DECISION,
            "summary": "4767 derives the exact parent source-qbasic contract that would promote the 4766 support-invariance route: quotient-owned source action, common observed readout, Hilbert stress, no source prefactor, Maxwell-Hodge/Poynting ownership and pre-readout support selector. The corpus has strong private standard-branch pieces but not one globally signed parent action branch. Poynting wall numeric rows are staged for open/radiative collars.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4767_0",
            "state": "completed_nonclaim",
            "meaning": "The theorem route is sharp, but promotion now depends on source action/operator inventory or first Poynting wall values.",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "Audit the actual source action/operator inventory for hidden prefactors, constants, Hodge/current forks and readout re-entry; in parallel, fill first Poynting wall value rows if the collar is open.",
            "route_priority": "source_action_operator_inventory_no_prefactor_first_Poynting_wall_values_parallel_denominator_pack",
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(
    timestamp: str,
    contract: list[dict[str, Any]],
    signature: list[dict[str, Any]],
    chain: list[dict[str, Any]],
    poynting: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    qedge: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4767: Parent Source-Qbasic Signature or Poynting Wall Numeric Bound

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

4767 writes the exact parent contract that would make the 4766 support-invariance route live.

- If `S_src` is a quotient-owned source action, `T_total` is the Hilbert variation of the same observed branch, and no source-only prefactor/readout tail survives, then `mu_H=c^-2 T_total(n,n)dV_obs` is q-basic as a Radon measure.
- That would promote the 4766 chain: q-basic `mu_H` fixes `W_H=closure(supp mu_H)`, gives `V_n_bound=0`, gives `mu_birth_TV=0`, and kills `Q_edge_shell_abs`.
- The corpus has strong private standard-branch support, but not one globally signed parent action selector that signs all clauses together.
- Poynting remains disciplined: same-Hodge stationary EM is already in `T_total`; open/radiative collars need numeric or zero rows for `dU_EM_dt`, `JdotE`, `Phi_incoming`, and `Phi_apparatus`.
- No local-GR, Newton, R10, PPN, WEP, clock, orbital or Maxwell pass is claimed.

## Parent Source-Qbasic Contract

{markdown_table(contract, ["contract_id", "required_statement", "status"])}

## Single Parent Signature Audit

{markdown_table(signature, ["signature_id", "clause", "support_found", "signature_status"])}

## Measure-Support Proof Chain

{markdown_table(chain, ["chain_id", "input_or_step", "deduction", "remaining_condition"])}

## Poynting Wall Numeric Bound Pack

{markdown_table(poynting, ["bound_id", "quantity", "formula_or_zero", "current_status"])}

## Source-Qbasic Residual Vector

{markdown_table(residuals, ["residual_id", "symbol", "meaning", "zero_or_bound_route"])}

## Qedge/Qbar Update

{markdown_table(qedge, ["update_id", "rule", "status"])}

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

    formal = f"""# PPC4161 4767: Parent Source-Qbasic Contract

Generated: `{timestamp}`

## Core Contract

```text
S_src = Sbar_src[q(Phi),Psi,A,theta_bar(q)] + dB_proper + S_top_silent
g_obs,e_obs,tau,star_obs = Obs(q(Phi))
T_total = -2/sqrt(-g_obs) delta S_src/delta g_obs
mu_H = c^-2 T_total(n,n)dV_obs
```

If the contract is signed by one parent branch, then:

```text
mu_H(Phi_s)=mu_H(Phi_0)
W_H=closure(supp mu_H) is invariant
V_n_bound=0
mu_birth_TV=0
Q_edge_shell_abs=0
```

Promotion failed here only because the one-parent signature is not found; the private standard-branch pieces are compatible but not enough for a global claim.

Poynting fallback:

```text
|Phi_wall_Poynting| <= |dU_EM/dt| + |int_W J.E dV|
                       + |Phi_incoming| + |Phi_apparatus|.
```

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4767 derives the parent source-qbasic contract that would promote support invariance: quotient-owned `S_src`, common observed branch, Hilbert stress, no source-prefactor, Maxwell-Hodge/Poynting ownership and pre-readout support selector.
- The exact chain is `S_src` descent -> q-basic `T_total` -> q-basic Radon measure `mu_H` -> invariant support -> `V_n_bound=0`, `mu_birth_TV=0` -> `Q_edge_shell_abs=0`.
- The current corpus has strong private standard-branch support but not one globally signed parent action line, so no claim is promoted.
- The Poynting wall fallback is staged as `|Phi_wall_Poynting| <= |dU_EM/dt| + |int_W J.E dV| + |Phi_incoming| + |Phi_apparatus|`.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4767 packet update: the q-basic source-measure theorem is now an explicit parent action contract, not a vibe. Promotion needs an actual source action/operator inventory excluding hidden source weights, constants, Hodge/current forks and readout re-entry; open Poynting collars need first numeric/zero rows.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4767-Y5-R2FR-parent-source-qbasic-signature-or-Poynting-wall-numeric-bound.md`

## Decision

`{DECISION}`

## What moved forward

- Wrote the exact parent source-qbasic action contract needed to promote the 4766 support-invariance route.
- Proved the conditional chain from source-action descent to q-basic Hilbert measure to `Q_edge_shell_abs=0`.
- Found private standard-branch support but not a single globally signed parent action selector.
- Staged the Poynting wall numeric/zero rows for open or radiative collars.

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
        "local_gr_parent_source_qbasic_contract",
        "4767 derives the parent source-qbasic contract needed to promote source support invariance, but finds no single globally signed parent selector.",
        "Generated source register, parent source-qbasic contract, signature audit, measure-support proof chain, Poynting numeric bound pack, source-qbasic residual vector, Qedge/Qbar update, route matrix, gates, firewalls, decision, status, next target and validation.",
        "parent_source_qbasic_contract_derived_single_parent_signature_missing_nonclaim",
        NEXT_TARGET,
        "Mixing private branch pieces as if they were one parent signature, or hiding Poynting wall flux.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need source action/operator inventory or first Poynting wall value rows.",
        "Parent source-qbasic signature or Poynting wall numeric bound",
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
    contract: list[dict[str, Any]],
    signature: list[dict[str, Any]],
    chain: list[dict[str, Any]],
    poynting: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    qedge: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4767_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4767_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4767_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4767_2_contract", "contract includes qbasic measure theorem and nonclaim verdict", any(row["status"] == "CONDITIONAL_MEASURE_THEOREM_DERIVED" for row in contract) and any(row["status"] == "NOT_SINGLE_PARENT_SIGNED_NONCLAIM" for row in contract), str(CONTRACT_CSV)))
    checks.append(("VAL4767_3_signature", "signature audit fails promotion as one parent branch", any(row["signature_status"] == "FAIL_CURRENT_CLAIM_NONCLAIM" for row in signature) and all(row["parent_signed_as_one_branch"] is False for row in signature), str(SIGNATURE_AUDIT_CSV)))
    checks.append(("VAL4767_4_proof_chain", "proof chain reaches support and Qedge shell", any(row["input_or_step"] == "W_H=closure(supp mu_H)" for row in chain) and any("Q_edge_shell_abs=0" in row["deduction"] for row in chain), str(PROOF_CHAIN_CSV)))
    checks.append(("VAL4767_5_poynting_bound", "Poynting pack has stationary zero and numeric placeholders", any(row["quantity"] == "Phi_wall_Poynting" for row in poynting) and any(row["current_status"] == "BOUND_TEMPLATE_READY_VALUES_MISSING" for row in poynting), str(POYNTING_BOUND_CSV)))
    checks.append(("VAL4767_6_residual_vector", "residual vector retains source prefactor and Poynting wall", any(row["symbol"] == "E_source_prefactor" for row in residuals) and any(row["symbol"] == "E_Poynting_wall" for row in residuals), str(RESIDUAL_VECTOR_CSV)))
    checks.append(("VAL4767_7_qedge_nonclaim", "Qedge update has exact and unsigned branches", any(row["status"] == "CONDITIONAL_BRANCH_READY" for row in qedge) and any(row["status"] == "PRODUCT_NONCLAIM" for row in qedge), str(QEDGE_UPDATE_CSV)))
    checks.append(("VAL4767_8_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4767_9_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4767_10_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4767_11_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4767_12_claim_row", "claim row L-609 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4767_13_resume", "resume points from 4767 to 4768", "4767-Y5" in resume_text and "4768-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4767_14_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
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
            "validation_id": "VAL4767_OVERALL",
            "check": "all 4767 parent source-qbasic/Poynting checks pass",
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
    contract = contract_rows(timestamp)
    signature = signature_audit_rows(timestamp)
    chain = proof_chain_rows(timestamp)
    poynting = poynting_bound_rows(timestamp)
    residuals = residual_rows(timestamp)
    qedge = qedge_update_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(CONTRACT_CSV, contract)
    write_csv(SIGNATURE_AUDIT_CSV, signature)
    write_csv(PROOF_CHAIN_CSV, chain)
    write_csv(POYNTING_BOUND_CSV, poynting)
    write_csv(RESIDUAL_VECTOR_CSV, residuals)
    write_csv(QEDGE_UPDATE_CSV, qedge)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, contract, signature, chain, poynting, residuals, qedge, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, contract, signature, chain, poynting, residuals, qedge, gates, timestamp))


if __name__ == "__main__":
    main()
