from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_VERTICAL_KERNEL_NULLNESS_2589"
CHECKPOINT_ID = "2589"

DOC = ROOT / "2589-Y5-R2FR-vertical-kernel-presymplectic-null-and-matter-invisible-or-kernel-charge-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_VERTICAL_KERNEL_2589_SOURCE_REGISTER.csv",
    "nullness_audit": OUT / "P8_Y5_VERTICAL_KERNEL_2589_NULLNESS_AUDIT.csv",
    "certificate_gate": OUT / "P8_Y5_VERTICAL_KERNEL_2589_CERTIFICATE_GATE.csv",
    "kernel_leak_rows": OUT / "P8_Y5_VERTICAL_KERNEL_2589_KERNEL_LEAK_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_VERTICAL_KERNEL_2589_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_VERTICAL_KERNEL_2589_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_VERTICAL_KERNEL_2589_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_VERTICAL_KERNEL_2589_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_VERTICAL_KERNEL_2589_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2589_VALIDATION.csv",
}

COPY_TARGETS = {
    "nullness_audit": QUEUE / "JR2589_VERTICAL_KERNEL_NULLNESS_AUDIT_NONCLAIM.csv",
    "certificate_gate": QUEUE / "JR2589_VERTICAL_KERNEL_CERTIFICATE_GATE_NONCLAIM.csv",
    "kernel_leak_rows": LOCAL_BOUNDS / "Vertical_kernel_leak_rows_2589_NONCLAIM.csv",
    "next_target": QUEUE / "JR2589_VERTICAL_NOETHER_CHARGE_QV_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:  # pragma: no cover - validation reports the error.
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    source_specs = [
        {
            "source_id": "SRC2589_00_2588_handoff",
            "source_path": ROOT / "2588-Y5-R2FR-observed-stack-q-eobs-tau-parent-owner-or-source-leak-fill.md",
            "needles": ["NEXT2588_0_selected", "OSC2588_1_vertical_kernel", "VAL2588_OVERALL"],
            "role": "active handoff selecting vertical-kernel nullness after observed-stack owner block",
        },
        {
            "source_id": "SRC2589_01_2588_next_queue",
            "source_path": QUEUE / "JR2588_VERTICAL_KERNEL_NULLNESS_NEXT.csv",
            "needles": ["NEXT2588_0_selected", "2589-Y5-R2FR-vertical-kernel-presymplectic-null-and-matter-invisible-or-kernel-charge-row.md"],
            "role": "machine-readable 2589 task and guardrails",
        },
        {
            "source_id": "SRC2589_02_2392_kernel_doc",
            "source_path": ROOT / "2392-Y5-R2FR-vertical-kernel-presymplectic-null-and-matter-invisible-or-kernel-charge-row.md",
            "needles": ["VKN2392_1_presymplectic_null", "VKL2392_1_kernel_charge", "NEXT2392_0_selected"],
            "role": "earlier exact vertical-kernel contract and kernel-charge rows",
        },
        {
            "source_id": "SRC2589_03_2392_certificate",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_2392_VERTICAL_KERNEL_CERTIFICATE.csv",
            "needles": ["VKC2392_2_theta_Qv", "VKC2392_4_matter_descent"],
            "role": "prior certificate gate: theta/Qv, matter descent, boundary and M_H_ref gaps",
        },
        {
            "source_id": "SRC2589_04_2392_leaks",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_2392_KERNEL_CHARGE_LEAK_VALUES.csv",
            "needles": ["VKL2392_1_kernel_charge", "VKL2392_6_total"],
            "role": "prior kernel-charge and total vertical-kernel residual rows",
        },
        {
            "source_id": "SRC2589_05_1737_q_Dq",
            "source_path": ROOT / "1737-Y5-R2FR-q-map-Dq-vertical-basis-source-row-or-coframe-functor-zero.md",
            "needles": ["DQM1737_5_Dq_total_kernel", "CFZ1737_0_exact_conditional", "VAL1737_OVERALL"],
            "role": "q/Dq vertical-basis and coframe-functor conditional zero source",
        },
        {
            "source_id": "SRC2589_06_2529_q_vertical",
            "source_path": ROOT / "2529-Y5-R2FR-psi-determinant-quotient-map-or-finite-qR-coefficients.md",
            "needles": ["DQG2529_3_vertical_q", "VAL2529_OVERALL"],
            "role": "psi determinant quotient-vertical route retains missing quotient map",
        },
        {
            "source_id": "SRC2589_07_1008_theta_charge",
            "source_path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            "needles": ["PVA1008_1_theta_MTS", "QTA1008_1_theta_total", "CG1008_0_parent_theta"],
            "role": "parent theta/Noether charge extraction is still contract-only",
        },
        {
            "source_id": "SRC2589_08_1760_matter_descent",
            "source_path": ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
            "needles": ["MWD1760_1_conditional_theorem", "AM1760_8_A_matter", "VAL1760_OVERALL"],
            "role": "matter/worldtube descent exact conditional theorem and A_matter nonclaim interface",
        },
        {
            "source_id": "SRC2589_09_1756_hidden_source",
            "source_path": ROOT / "1756-Y5-R2FR-two-slot-source-free-owner-or-hidden-source-counterexample-ledger.md",
            "needles": ["HSC1756_9_verdict", "HSR1756_9_total", "VAL1756_OVERALL"],
            "role": "hidden source/direct-slot counterexample ledger",
        },
    ]
    rows: list[dict[str, Any]] = []
    for source in source_specs:
        source_path = source["source_path"]
        missing_needles = path_has_needles(source_path, source["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": source_path,
                    "exists": source_path.exists(),
                    "missing_needles": missing_needles,
                    "source_pass": source_path.exists() and not missing_needles,
                    "role": source["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def nullness_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "VKN2589_0_kernel_definition",
            "test_piece": "parent vertical distribution",
            "formal_statement": "V=ker(Dq) must be a parent-defined distribution with explicit basis v_i, not a name for variables hidden from the readout.",
            "derivation_status": "TARGET_CONTRACT_RESTATED",
            "current_gain": "turns q ownership into a geometry problem with basis, rank and bracket tests",
            "remaining_gap": "q, Dq, v_i and target Q_vis are still not parent-action owned in one branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "VKN2589_1_presymplectic_null",
            "test_piece": "covariant phase-space nullness",
            "formal_statement": "For every v_i in V, delta L_parent = E delta Phi + dTheta_parent and J_v = Theta_parent(v_i) - i_v L_parent = dQ_v + C_v + dB_v; the linked compact-surface integral int_S(delta Q_v - i_v Theta_parent + delta B_v) must vanish or have a source-backed bound.",
            "derivation_status": "EXACT_CPS_CHARGE_TEST_NOT_CLOSED",
            "current_gain": "gauge-by-name is replaced by a Noether charge calculation",
            "remaining_gap": "Theta_parent, Q_v, C_v, B_v, improvement convention, surface class and M_H_ref are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "VKN2589_2_matter_invisible",
            "test_piece": "matter invisibility",
            "formal_statement": "delta_v S_matter=0 follows only if ordinary matter, constants, lifts, worldtubes, source currents and boundary terms all descend through q/e_obs or are separately bounded.",
            "derivation_status": "EXACT_CONDITIONAL_CHAIN_RULE_PARENT_UNSIGNED",
            "current_gain": "separates a real quotient theorem from a hidden source coupling",
            "remaining_gap": "parent matter functor, no direct V_m[v,rho_A,W_source], fixed constants, source support and boundary silence are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "VKN2589_3_boundary_history_silence",
            "test_piece": "boundary/history/source-support silence",
            "formal_statement": "Bulk nullness is insufficient unless compact boundary flux, reference terms, history tails and local projection/support terms also vanish or enter an absolute source envelope.",
            "derivation_status": "OBSTRUCTION_RETAINED",
            "current_gain": "prevents a kernel charge from being moved into an edge term",
            "remaining_gap": "zero compact boundary flux, history-tail silence and source-support invariance are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "VKN2589_4_rank_integrability",
            "test_piece": "quotient geometry",
            "formal_statement": "V must have constant rank and be involutive, with brackets [v_i,v_j] lying in span(V), before q can be a stable local quotient chart.",
            "derivation_status": "CONDITIONAL_GEOMETRY_TEST_NOT_CLOSED",
            "current_gain": "blocks chart-dependent cancellation or pole-selector tricks",
            "remaining_gap": "vertical basis, bracket table, rank audit, norms and branch domain are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "VKN2589_5_no_tautological_q",
            "test_piece": "projection-by-declaration guard",
            "formal_statement": "A q_candidate that includes e_obs or the observed stack as a component is not a proof unless its kernel is independently presymplectic-null and matter-invisible.",
            "derivation_status": "ANTI_TAUTOLOGY_GUARD_ACTIVE",
            "current_gain": "keeps the route honest: q/Obs_e cannot be smuggled in by definition",
            "remaining_gap": "null kernel and matter-invisible certificates are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "VKN2589_6_verdict",
            "test_piece": "2589 verdict",
            "formal_statement": "2589 constructs the exact kernel-nullness contract but does not prove it for current MTS. The next non-cheatable target is vertical Noether charge extraction: derive Theta_parent and Q_v, or keep epsilon_kernel_charge as a sourced nonclaim residual.",
            "derivation_status": "ROUTE_EXACT_NOT_CLAIMED",
            "current_gain": "the q/Obs_e route now has a precise charge test instead of a philosophical gap",
            "remaining_gap": "epsilon_kernel_charge, epsilon_q_rank_or_integrability, epsilon_matter_kernel, epsilon_boundary_history and epsilon_projection_declaration remain live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def certificate_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "certificate_id": "VKC2589_0_vertical_basis",
            "certificate": "parent vertical basis",
            "required_test": "list every v_i as a variation of parent fields and prove Dq[v_i]=0 before readout",
            "status": "MISSING_PARENT_VERTICAL_BASIS",
            "residual_if_missing": "epsilon_q_rank_or_integrability",
        },
        {
            "certificate_id": "VKC2589_1_rank_involutive",
            "certificate": "constant-rank involutive distribution",
            "required_test": "rank(Dq) constant on the branch and [v_i,v_j] in span(V) with sourced structure functions",
            "status": "MISSING_RANK_AND_BRACKET_AUDIT",
            "residual_if_missing": "epsilon_q_rank_or_integrability",
        },
        {
            "certificate_id": "VKC2589_2_theta_Qv",
            "certificate": "parent Theta_parent and vertical Q_v extraction",
            "required_test": "derive delta L_parent = E delta Phi + dTheta_parent and J_v = Theta_parent(v)-i_v L_parent = dQ_v + constraints + improvements",
            "status": "MISSING_THETA_PARENT_AND_QV",
            "residual_if_missing": "epsilon_kernel_charge",
        },
        {
            "certificate_id": "VKC2589_3_zero_compact_flux",
            "certificate": "zero compact local flux",
            "required_test": "prove int_S(delta Q_v - i_v Theta_parent + boundary improvements)=0 on linked local surfaces",
            "status": "MISSING_ZERO_COMPACT_FLUX_CERTIFICATE",
            "residual_if_missing": "epsilon_kernel_charge",
        },
        {
            "certificate_id": "VKC2589_4_matter_descent",
            "certificate": "matter-invisible kernel",
            "required_test": "S_matter, constants, matter lifts, worldtube support and Hilbert current descend through q/e_obs for every v_i",
            "status": "MISSING_MATTER_DESCENT_SIGNATURE",
            "residual_if_missing": "epsilon_matter_kernel",
        },
        {
            "certificate_id": "VKC2589_5_no_hidden_source_slot",
            "certificate": "no hidden direct source slot",
            "required_test": "exclude direct V_m[v,rho_A,W_source,C_top], source prefactors, material markers, species weights and support selectors outside q",
            "status": "MISSING_NO_DIRECT_SOURCE_SLOT_PROOF",
            "residual_if_missing": "epsilon_hidden_source_slot",
        },
        {
            "certificate_id": "VKC2589_6_boundary_history",
            "certificate": "boundary/history/reference silence",
            "required_test": "Pi_local dB_v=0 and J_history[v]=0, or provide an absolute source-backed boundary/history envelope",
            "status": "MISSING_BOUNDARY_HISTORY_SILENCE",
            "residual_if_missing": "epsilon_boundary_history",
        },
        {
            "certificate_id": "VKC2589_7_MHref",
            "certificate": "positive same-frame M_H_ref",
            "required_test": "derive H_tau-H_ref in the same q/e_obs/tau branch before normalizing kernel leakage",
            "status": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "residual_if_missing": "all normalized rows remain non-score-ready",
        },
        {
            "certificate_id": "VKC2589_8_no_tautology",
            "certificate": "non-tautological q promotion",
            "required_test": "q/Obs_e may not be promoted by including observed variables as q components unless VKC2589_0 through VKC2589_7 pass",
            "status": "PROJECTION_BY_DECLARATION_BLOCK_ACTIVE",
            "residual_if_missing": "epsilon_projection_declaration",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def kernel_leak_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "VKL2589_0_rank_integrability",
            "symbol": "epsilon_q_rank_or_integrability",
            "definition": "norm([v_i,v_j] mod V) + norm(rank(Dq)-rank_expected)",
            "units": "field-space quotient defect",
            "current_value": "MISSING_VERTICAL_BASIS;MISSING_BRACKET_TABLE;MISSING_RANK_AUDIT",
            "source_path": "MISSING_SOURCE_PATH",
            "observable_link": "q_owner;Obs_e;local_GR;PPN",
        },
        {
            "row_id": "VKL2589_1_kernel_charge",
            "symbol": "epsilon_kernel_charge",
            "definition": "abs(int_S(delta Q_v - i_v Theta_parent + boundary_improvements))/M_H_ref",
            "units": "dimensionless Hamiltonian charge leakage",
            "current_value": "MISSING_THETA_PARENT;MISSING_Q_V;MISSING_BOUNDARY_IMPROVEMENTS;MISSING_ZERO_FLUX_CERTIFICATE;MISSING_M_H_REF",
            "source_path": "MISSING_SOURCE_PATH",
            "observable_link": "local_GR;Newton;PPN;R10;clock;orbital",
        },
        {
            "row_id": "VKL2589_2_matter_kernel",
            "symbol": "epsilon_matter_kernel",
            "definition": "abs(delta_v S_matter_on_shell)/M_H_ref",
            "units": "dimensionless matter-source leakage",
            "current_value": "MISSING_MATTER_DESCENT;MISSING_MATTER_LIFT;MISSING_WORLDTUBE_SUPPORT;MISSING_M_H_REF",
            "source_path": "MISSING_SOURCE_PATH",
            "observable_link": "WEP;source_normalization;PPN;orbital",
        },
        {
            "row_id": "VKL2589_3_hidden_source_slot",
            "symbol": "epsilon_hidden_source_slot",
            "definition": "abs(partial_v V_m[v,rho_A,W_source,C_top])/M_H_ref plus species/source-prefactor leakage",
            "units": "dimensionless hidden-source leakage",
            "current_value": "MISSING_NO_DIRECT_SLOT_PROOF;MISSING_VM_DENSITY;MISSING_SOURCE_PREFACTOR_RULE;MISSING_M_H_REF",
            "source_path": "MISSING_SOURCE_PATH",
            "observable_link": "WEP;R10;R11;clock;source_mass",
        },
        {
            "row_id": "VKL2589_4_boundary_history",
            "symbol": "epsilon_boundary_history",
            "definition": "abs(int_S Pi_local dB_v + int_history J_history[v])/M_H_ref",
            "units": "dimensionless boundary/history leakage",
            "current_value": "MISSING_BOUNDARY_FLUX;MISSING_HISTORY_TAIL;MISSING_REFERENCE_SILENCE;MISSING_M_H_REF",
            "source_path": "MISSING_SOURCE_PATH",
            "observable_link": "clock;orbital;PPN;local_GR",
        },
        {
            "row_id": "VKL2589_5_projection_declaration",
            "symbol": "epsilon_projection_declaration",
            "definition": "1 if q/Obs_e relies on observed variables inside q before null-kernel proof else 0",
            "units": "boolean guard",
            "current_value": "MISSING_NULL_KERNEL_PROOF",
            "source_path": "THIS_CHECKPOINT_GUARD_ROW",
            "observable_link": "q_owner;Obs_e;same_frame",
        },
        {
            "row_id": "VKL2589_TOTAL",
            "symbol": "Delta_vertical_kernel_total_over_MH",
            "definition": "epsilon_q_rank_or_integrability + epsilon_kernel_charge + epsilon_matter_kernel + epsilon_hidden_source_slot + epsilon_boundary_history + epsilon_projection_declaration",
            "units": "dimensionless after M_H_ref",
            "current_value": "COMPONENTS_MISSING",
            "source_path": "THIS_CHECKPOINT_SYMBOLIC_LEDGER_ONLY",
            "observable_link": "q_owner;Newton;local_GR;PPN;R10;clock;orbital",
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def runner_refusal_rows(leak_rows_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in leak_rows_data:
        failure_reasons = ["VALID_FOR_CLAIM_FALSE"]
        current_value = row_value(row["current_value"])
        source_path = row_value(row["source_path"])
        if "MISSING" in current_value or row["row_id"] == "VKL2589_TOTAL":
            failure_reasons.append("MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE")
        if source_path == "MISSING_SOURCE_PATH":
            failure_reasons.append("MISSING_SOURCE_PATH")
        if row["symbol"] == "epsilon_projection_declaration":
            failure_reasons.append("NULL_KERNEL_CERTIFICATE_REQUIRED_BEFORE_Q_OBSE_PROMOTION")
        rows.append(
            with_stamp(
                {
                    "runner_id": f"VKR2589_{row['row_id']}",
                    "target_id": row["row_id"],
                    "symbol": row["symbol"],
                    "verdict": "REFUSED_NONCLAIM_KERNEL_RESIDUAL",
                    "failure_reasons": failure_reasons,
                    "score_ready": False,
                    "claim_allowed": False,
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CG2589_0_contract_shape",
            "claim": "vertical kernel nullness has a precise covariant phase-space contract",
            "gate_status": "PASS_NONCLAIM_THEOREM_SHAPE_ONLY",
            "reason": "the required Theta_parent/Q_v/matter/boundary/rank tests are written",
            "gate_pass": True,
        },
        {
            "gate_id": "CG2589_1_vertical_basis",
            "claim": "V=ker(Dq) is parent-owned with constant rank and involutive brackets",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "v_i, Dq matrix, bracket table and rank audit are not parent-signed",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2589_2_presymplectic_charge",
            "claim": "every vertical v_i is presymplectic-null with zero compact flux",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "Theta_parent, Q_v, constraints, improvements and compact-surface zero are missing",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2589_3_matter_invisible",
            "claim": "vertical kernel is invisible to matter/source/readout",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "matter descent, no direct source slot, constants, lifts and worldtube support are not jointly signed",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2589_4_boundary_history",
            "claim": "boundary, reference and history terms do not carry kernel charge",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "Pi_local dB_v, J_history[v], source support and reference terms lack zero/bound certificates",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2589_5_q_obse_promotion",
            "claim": "q/Obs_e can be promoted as parent-owned observed stack",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "projection-by-declaration guard remains active until null-kernel certificates pass",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2589_6_Newton_local_GR",
            "claim": "Newton/local-GR follows from the vertical-kernel route",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "kernel nullness is necessary but not sufficient; EH exterior, source charge, M_H_ref, Poisson/Gauss, PPN and boundary locks remain open",
            "gate_pass": False,
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2589_0_accept_charge_gate",
            "decision": "COVARIANT_PHASE_SPACE_KERNEL_GATE_ACCEPTED",
            "reason": "vertical directions are harmless only when their Noether charge and matter/readout response vanish or are bounded",
            "effect": "q/Obs_e promotion now depends on Theta_parent/Q_v plus matter/boundary certificates",
        },
        {
            "decision_id": "DEC2589_1_no_kernel_claim",
            "decision": "VERTICAL_KERNEL_NULLNESS_NOT_CLAIMED",
            "reason": "basis, rank, Theta_parent, Q_v, zero flux, matter descent, hidden-source exclusion, boundary silence and M_H_ref are unsigned",
            "effect": "epsilon_kernel_charge and sibling rows remain nonclaim",
        },
        {
            "decision_id": "DEC2589_2_no_q_promotion",
            "decision": "Q_OBS_E_PROMOTION_REMAINS_BLOCKED",
            "reason": "observed variables cannot be included in q as proof objects before the independent kernel test passes",
            "effect": "same-frame, source-current, Newton and local-GR gates remain closed",
        },
        {
            "decision_id": "DEC2589_3_next",
            "decision": "VERTICAL_NOETHER_CHARGE_QV_SELECTED_NEXT",
            "reason": "the least-cheatable next derivation is to extract Theta_parent and Q_v for vertical variations",
            "effect": "2590 should prove int_S(delta Q_v - i_v Theta_parent)=0 or fill epsilon_kernel_charge rows with sources, units and valid_for_claim=false",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2589_0_selected",
            "selection_status": "selected",
            "target_file": "2590-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md",
            "target_script": "scripts/Y5_R2FR_vertical_Noether_charge_Qv_extraction_or_kernel_charge_source_row_2590.py",
            "task": "derive Theta_parent and Q_v for vertical variations and prove int_S(delta Q_v - i_v Theta_parent)=0 on compact linked local surfaces, or fill epsilon_kernel_charge with source paths, units, boundary-improvement terms, denominator status and valid_for_claim=false",
            "acceptance_target": "a parent-signed zero compact-flux theorem for every v_i, or a source-ready nonclaim kernel-charge residual interface",
            "guardrails": "no EH-only charge import as MTS total; no q=(e_obs,...) tautology; no fitted M_H_ref; no post-readout counterterm; no Newton/local-GR claim; no GitHub; no formalization-workbench edits",
            "valid_for_claim": False,
        },
        {
            "route_id": "NEXT2589_1_parallel",
            "selection_status": "held_parallel",
            "target_file": "2590b-Y5-R2FR-vertical-basis-rank-bracket-audit-or-epsilon-q-integrability-row.md",
            "target_script": "scripts/Y5_R2FR_vertical_basis_rank_bracket_audit_or_epsilon_q_integrability_row_2590b.py",
            "task": "list v_i, prove v_i in ker(Dq), constant rank, and [v_i,v_j] in V, or fill epsilon_q_rank_or_integrability rows",
            "acceptance_target": "q quotient geometry becomes branch-stable or a finite nonclaim quotient-defect interface is staged",
            "guardrails": "do not use observed-frame variables as the defining vertical basis without an independent nullness certificate",
            "valid_for_claim": False,
        },
        {
            "route_id": "NEXT2589_2_parallel",
            "selection_status": "held_parallel",
            "target_file": "2590c-Y5-R2FR-matter-boundary-invisibility-or-hidden-source-kernel-bound.md",
            "target_script": "scripts/Y5_R2FR_matter_boundary_invisibility_or_hidden_source_kernel_bound_2590c.py",
            "task": "prove delta_v S_matter=0 plus boundary/history/source-support silence for each v_i, or fill epsilon_matter_kernel, epsilon_hidden_source_slot and epsilon_boundary_history",
            "acceptance_target": "matter/readout invisibility becomes parent-signed or source-ready residual rows remain nonclaim",
            "guardrails": "no source-prefactor, material-marker, worldtube-support or boundary-tail silence by naming",
            "valid_for_claim": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target_path in COPY_TARGETS.items():
        source_path = OUTPUTS[copy_id]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2589_{copy_id}",
                    "source_path": source_path,
                    "target_path": target_path,
                    "source_exists": source_path.exists(),
                    "target_exists": target_path.exists(),
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(data: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in data.values():
        for row in rows:
            if row.get("valid_for_claim") is True or row.get("claim_allowed") is True:
                return False
    return True


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if condition else "FAIL",
                    "notes": notes,
                    "detail": detail,
                    "valid_for_claim": False,
                }
            )
        )

    add("VAL2589_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2589_01_kernel_contract_written",
        any(row["audit_id"] == "VKN2589_0_kernel_definition" for row in data["nullness_audit"]),
        "V=ker(Dq) target is explicit and parent-owned basis/rank tests are required",
    )
    add(
        "VAL2589_02_presymplectic_test_present",
        any(row["audit_id"] == "VKN2589_1_presymplectic_null" and "delta L_parent" in row["formal_statement"] and "Q_v" in row["formal_statement"] for row in data["nullness_audit"]),
        "Theta_parent/Q_v covariant phase-space charge test is present",
    )
    add(
        "VAL2589_03_matter_invisible_present",
        any(row["audit_id"] == "VKN2589_2_matter_invisible" and "delta_v S_matter=0" in row["formal_statement"] for row in data["nullness_audit"]),
        "matter-invisibility chain-rule test is present",
    )
    add(
        "VAL2589_04_boundary_guard_present",
        any(row["audit_id"] == "VKN2589_3_boundary_history_silence" for row in data["nullness_audit"]),
        "boundary/history silence guard is present",
    )
    add(
        "VAL2589_05_certificate_gates_blocked",
        all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["certificate_gate"]),
        "all vertical-kernel certificates remain nonclaim",
    )
    leak_symbols = {row["symbol"] for row in data["kernel_leak_rows"]}
    required_symbols = {
        "epsilon_q_rank_or_integrability",
        "epsilon_kernel_charge",
        "epsilon_matter_kernel",
        "epsilon_hidden_source_slot",
        "epsilon_boundary_history",
        "epsilon_projection_declaration",
        "Delta_vertical_kernel_total_over_MH",
    }
    add("VAL2589_06_required_leak_rows_present", required_symbols.issubset(leak_symbols), "all required kernel leak rows are present")
    add(
        "VAL2589_07_kernel_charge_nonclaim",
        any(row["symbol"] == "epsilon_kernel_charge" and row["score_ready"] is False and row["valid_for_claim"] is False for row in data["kernel_leak_rows"]),
        "epsilon_kernel_charge row is present and nonclaim",
    )
    add(
        "VAL2589_08_runner_refuses",
        all(row["score_ready"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]),
        "runner refuses all unfilled kernel residual rows",
    )
    add(
        "VAL2589_09_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"])
        and any(row["gate_id"] == "CG2589_6_Newton_local_GR" and row["gate_pass"] is False for row in data["claim_gates"]),
        "q/Obs_e, Newton and local-GR claims remain blocked",
    )
    add(
        "VAL2589_10_no_claim_flags",
        generated_rows_have_no_claim_flags(data),
        "no generated row sets valid_for_claim=true or claim_allowed=true",
    )

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2589-Y5-R2FR-vertical-kernel*",
            "*Y5_R2FR_vertical_kernel_presymplectic*",
            "*P8_Y5_VERTICAL_KERNEL_2589*",
            "*JR2589*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2589_11_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2589 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )
    add(
        "VAL2589_12_next_selected",
        any(row["route_id"] == "NEXT2589_0_selected" and "2590-Y5-R2FR-vertical-Noether-charge-Qv" in row["target_file"] for row in data["next"]),
        "2590 vertical Noether charge extraction selected next",
    )
    add(
        "VAL2589_13_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2589_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2589_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2589_OVERALL",
        overall,
        "2589 installs the covariant phase-space vertical-kernel nullness contract, refuses gauge-by-name and q/Obs_e promotion, keeps kernel rows nonclaim, and selects vertical Noether charge Q_v extraction next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [row_value(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2589 Y5 R2FR vertical-kernel presymplectic-null and matter-invisible or kernel-charge row",
        "",
        "**Status:** private nonclaim derivation checkpoint. The vertical-kernel route is now an exact covariant phase-space charge test, but current MTS has not yet supplied the parent `Theta_parent`, `Q_v`, matter-invisibility, boundary-silence or rank/integrability certificates.",
        "",
        "**Main result:** `V=ker(Dq)` can only be treated as harmless gauge if every vertical representative `v_i` is parent-owned, constant-rank/involutive, presymplectic-null, matter/readout-invisible and boundary/history silent. In formulas, the core test is `delta L_parent = E delta Phi + dTheta_parent`, `J_v = Theta_parent(v)-i_v L_parent = dQ_v + C_v + dB_v`, and `int_S(delta Q_v - i_v Theta_parent + delta B_v)=0` or source-bounded on linked local surfaces. Current MTS does not prove this, so `epsilon_kernel_charge` and the sibling kernel rows remain live nonclaim residuals.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Nullness Audit",
        markdown_table(data["nullness_audit"], ["audit_id", "test_piece", "formal_statement", "derivation_status", "current_gain", "remaining_gap", "valid_for_claim", "claim_allowed"]),
        "",
        "## Certificate Gate",
        markdown_table(data["certificate_gate"], ["certificate_id", "certificate", "required_test", "status", "residual_if_missing", "valid_for_claim", "claim_allowed"]),
        "",
        "## Kernel Leak Rows",
        markdown_table(data["kernel_leak_rows"], ["row_id", "symbol", "definition", "units", "current_value", "source_path", "observable_link", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "target_id", "symbol", "verdict", "failure_reasons", "score_ready", "claim_allowed", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
        "## Practical Status",
        "",
        "This is not circling. It is the boxing footwork version of rigor: the local-GR route cannot win by saying the invisible directions are gauge; it has to show they carry zero parent charge. The next punch is `Q_v` extraction. If that closes, the q/Obs_e route becomes much more serious. If it fails, the failure becomes a physical residual with a name, units and source path instead of a fog bank.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    leak_rows_data = kernel_leak_rows()
    data = {
        "sources": source_register_rows(),
        "nullness_audit": nullness_audit_rows(),
        "certificate_gate": certificate_gate_rows(),
        "kernel_leak_rows": leak_rows_data,
        "runner_refusal": runner_refusal_rows(leak_rows_data),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["nullness_audit"], data["nullness_audit"])
    write_csv(OUTPUTS["certificate_gate"], data["certificate_gate"])
    write_csv(OUTPUTS["kernel_leak_rows"], data["kernel_leak_rows"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2589_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
