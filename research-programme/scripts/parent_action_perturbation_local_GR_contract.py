#!/usr/bin/env python3
"""Exact contract for a future MTS parent action."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

DECISION_RUN = RUNS_ROOT / "20260531-235959-official-refresh-decision-gate"
PROMOTION_RUN = RUNS_ROOT / "20260531-234500-promotion-contract-audit"
STATUS_PASS = "parent_action_perturbation_local_GR_contract_written_not_derived"
STATUS_FAIL = "parent_action_perturbation_local_GR_contract_incomplete"
CLAIM_CEILING = "parent_action_contract_only_no_derivation_or_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 177 parent-action contract script"),
        (WORK_DIR / "176-official-refresh-decision-gate.md", "decision to pivot from scoring to derivation"),
        (WORK_DIR / "148-perturbation-CMB-local-GR-promotion-contract.md", "promotion blockers"),
        (WORK_DIR / "141-consolidated-locked-memory-branch-contract.md", "locked branch status stack"),
        (WORK_DIR / "149-smooth-memory-or-controlled-growth-theorem.md", "growth/smooth-memory theorem target"),
        (WORK_DIR / "150-Boltzmann-interface-contract.md", "Boltzmann/CMB interface contract"),
        (WORK_DIR / "159-ruler-only-projection-theorem-contract.md", "two-point ruler no-smuggling contract"),
        (WORK_DIR / "160-ruler-projection-parent-tensor-attempt.md", "ruler tensor source-law target"),
        (WORK_DIR / "168-pair-half-kernel-parent-ownership-gate.md", "pair sidecar non-promotion gate"),
        (WORK_DIR / "143-domain-selector-variational-action-attempt.md", "domain selector failure"),
        (WORK_DIR / "140-boundary-charge-amplitude-decision-gate.md", "2/27 amplitude blocker"),
        (WORK_DIR / "13-local-closure-PPN-benchmark.md", "local GR closure benchmark"),
        (WORK_DIR / "14-closure-deviation-PPN-sensitivity.md", "local PPN leak budget"),
        (DECISION_RUN / "status.json", "checkpoint 176 machine status"),
        (DECISION_RUN / "results" / "promotion_requirement_matrix.csv", "active blocker matrix"),
    ]
    rows: list[dict[str, Any]] = []
    for path, role in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": role,
                "issue": "" if exists else "missing",
            }
        )
    return rows


def blocker_contract_rows() -> list[dict[str, Any]]:
    source = DECISION_RUN / "results" / "promotion_requirement_matrix.csv"
    rows: list[dict[str, Any]] = []
    for row in read_csv_rows(source):
        if row["class_status"] != "blocking":
            continue
        gate_id = row["gate_id"]
        contract_target = {
            "P04": "parent_action_variation_contract",
            "P06": "perturbation_output_contract",
            "P07": "Boltzmann_interface_contract",
            "P08": "local_GR_PPN_silence_contract",
            "P09": "domain_selector_contract",
            "P10": "amplitude_owner_contract",
        }.get(gate_id, "general_contract")
        rows.append(
            {
                "gate_id": gate_id,
                "blocker": row["requirement"],
                "current_status": row["current_status"],
                "contract_target": contract_target,
                "minimum_success_condition": minimum_success_condition(gate_id),
                "demotion_if_failed": demotion_if_failed(gate_id),
            }
        )
    return rows


def minimum_success_condition(gate_id: str) -> str:
    return {
        "P04": "one covariant action gives metric, matter, memory, selector, and perturbation Euler-Lagrange equations",
        "P06": "linearized equations derive F_fric(a,k), mu(a,k), slip/Sigma(a,k), and S_mem(a,k), including GR-proxy limit",
        "P07": "Boltzmann-ready variables and closure equations are defined without denominator singularities or hidden calibration fitting",
        "P08": "weak-field/local limit derives q_loc^nu -> 0, G_eff/G -> 1, gamma=beta=1, and Phi=Psi to allowed order",
        "P09": "domain D or chi_D is selected by zero-knob variational mechanism with no empirical threshold or imported local-GR closure",
        "P10": "B_mem=2/27 follows from parent-normalized boundary charge before data scoring",
    }[gate_id]


def demotion_if_failed(gate_id: str) -> str:
    return {
        "P04": "locked branch remains empirical EFT closure, not parent field theory",
        "P06": "growth/RSD support remains conditional GR-proxy stress only",
        "P07": "CMB route remains kill-screen/interface only, no CMB support claim",
        "P08": "local branch remains GR-equivalent closure benchmark, not derived local GR",
        "P09": "domain/coherence remains selected closure, not parent-owned object",
        "P10": "2/27 remains empirical theorem target, not a prediction",
    }[gate_id]


def parent_action_skeleton_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector": "Einstein_metric",
            "symbol": "S_GR[g]",
            "required_action_term": "integral sqrt(-g) R/(16 pi G)",
            "variation_target": "delta_g S_GR gives Einstein tensor",
            "current_status": "standard_baseline",
            "forbidden_shortcut": "changing metric equations only after fitting observables",
        },
        {
            "sector": "matter",
            "symbol": "S_m[g,psi_m]",
            "required_action_term": "universal matter coupling to the same metric/coframe",
            "variation_target": "T_m^{mu nu}; covariant conservation/exchange law",
            "current_status": "required",
            "forbidden_shortcut": "matter-sector coupling spread hidden in epsilon_matter",
        },
        {
            "sector": "domain_selector",
            "symbol": "S_D[g,D,chi_D,lambda_D]",
            "required_action_term": "zero-knob coherent-domain selector or algebraic auxiliary constraint",
            "variation_target": "delta_D S=0 selects D; delta_lambda S=0 enforces chi_D=C_coh[D]",
            "current_status": "missing_derivation",
            "forbidden_shortcut": "external threshold, smoothing length, or outcome-selected domain",
        },
        {
            "sector": "load_tensor",
            "symbol": "S_Q[g,D,Q,lambda_Q]",
            "required_action_term": "coherent-volume load tensor owner",
            "variation_target": "delta_Q S=0 gives Q^A_B and FLRW Q^i_j=X_D delta^i_j",
            "current_status": "conditional_target",
            "forbidden_shortcut": "inserting X_D=N/u3 only after assuming FLRW",
        },
        {
            "sector": "memory",
            "symbol": "S_mem[g,Q,D,M,lambda_M]",
            "required_action_term": "auxiliary or high-sound-speed memory owner with activation exposure",
            "variation_target": "rho_mem, p_mem, E_mem^{mu nu}, and perturbation constraints",
            "current_status": "effective_not_parent",
            "forbidden_shortcut": "using rho_mem(a) as a fitted background fluid without stress/perturbation owner",
        },
        {
            "sector": "boundary_charge",
            "symbol": "S_R[g,D,Q,R,lambda_R]",
            "required_action_term": "normalized boundary-charge endpoint law",
            "variation_target": "endpoint equations with R_early=1/3, R_today=1/9, DeltaR=2/9",
            "current_status": "theorem_target",
            "forbidden_shortcut": "post-hoc rationalizing B_mem=2/27 from fitted amplitude",
        },
        {
            "sector": "optional_two_point_ruler",
            "symbol": "S_pair[g,D,K_c,ell]",
            "required_action_term": "sidecar only: connected pair current with no one-point metric deformation",
            "variation_target": "two-point ruler transport source law if ever used",
            "current_status": "excluded_from_no_clock_lead",
            "forbidden_shortcut": "using pair-ruler half-kernel to improve lead branch before parent ownership",
        },
    ]


def field_variable_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "metric",
            "symbol": "g_mu_nu",
            "type": "fundamental",
            "must_define": "background, weak-field, and scalar perturbations",
            "observable_owner": "SN, BAO background, local PPN, lensing/CMB",
            "status": "required",
        },
        {
            "object": "matter fields",
            "symbol": "psi_m",
            "type": "fundamental_or_standard",
            "must_define": "universal coupling and stress tensor",
            "observable_owner": "equivalence principle, growth source",
            "status": "required",
        },
        {
            "object": "observer/coframe",
            "symbol": "u^mu or e^A_mu",
            "type": "auxiliary/geometric",
            "must_define": "screen/radial projectors without universal clock deformation",
            "observable_owner": "ruler-only route if used; local clock safety",
            "status": "required_if_projection_used",
        },
        {
            "object": "domain selector",
            "symbol": "D or chi_D",
            "type": "auxiliary/variational",
            "must_define": "coherent domains with zero empirical knobs",
            "observable_owner": "FLRW vs local silence split",
            "status": "missing_derivation",
        },
        {
            "object": "load tensor",
            "symbol": "Q^A_B",
            "type": "memory source",
            "must_define": "FLRW limit Q^i_j=X_D delta^i_j and local/bound limit",
            "observable_owner": "activation exposure I_M=det(Q)",
            "status": "conditional_target",
        },
        {
            "object": "memory exposure",
            "symbol": "I_M",
            "type": "emergent_from_Q",
            "must_define": "I_M=det(Q) and additive hazard activation A=1-exp(-I_M)",
            "observable_owner": "rho_mem(a)",
            "status": "conditional_mechanics",
        },
        {
            "object": "memory stress",
            "symbol": "E_mem^{mu nu}",
            "type": "variation_output",
            "must_define": "conserved/equilibrium stress with perturbation source terms",
            "observable_owner": "growth, CMB, local GR",
            "status": "missing_parent_owner",
        },
        {
            "object": "boundary charge",
            "symbol": "R, Q_boundary/Q_*",
            "type": "amplitude_owner_target",
            "must_define": "normalized endpoint equation and direction 1/3 -> 1/9",
            "observable_owner": "B_mem=DeltaR/3=2/27",
            "status": "blocked_for_promotion",
        },
    ]


def variation_equation_rows() -> list[dict[str, Any]]:
    return [
        {
            "variation": "delta_g S_parent=0",
            "required_equation": "G^{mu nu}=8 pi G (T_m^{mu nu}+E_mem^{mu nu}+E_D^{mu nu}+E_Q^{mu nu})",
            "must_reduce_to": "FLRW locked background and local Schwarzschild/PPN silence",
            "current_gap": "memory/domain stress not parent-derived",
            "pass_condition": "Bianchi identity gives consistent exchange or separate conservation without q_loc leakage",
        },
        {
            "variation": "nabla_mu total E^{mu nu}=0",
            "required_equation": "q^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}) derived or identically zero",
            "must_reduce_to": "q_loc^nu -> 0 in local bound/vacuum systems",
            "current_gap": "local silence remains theorem target",
            "pass_condition": "no plateau axiom; cancellation follows from action/constraint",
        },
        {
            "variation": "delta_Q S_parent=0",
            "required_equation": "source law for Q^A_B, including FLRW Q^i_j=X_D delta^i_j",
            "must_reduce_to": "I_M=X_D^3 and A=1-exp(-X_D^3)",
            "current_gap": "Q inserted conditionally",
            "pass_condition": "Q exists before FLRW reduction and before data scoring",
        },
        {
            "variation": "delta_D S_parent=0",
            "required_equation": "zero-knob coherent domain selector",
            "must_reduce_to": "homogeneous FLRW domain active, local stationary domain silent",
            "current_gap": "boundary terms and selector ownership open",
            "pass_condition": "no empirical threshold, no transition length, no local-GR import",
        },
        {
            "variation": "delta_M S_parent=0",
            "required_equation": "exact auxiliary smooth memory or high-c_s stress law",
            "must_reduce_to": "delta_mem suppression or exact delta_mem=0",
            "current_gap": "effective high-c_s law exists, parent owner missing",
            "pass_condition": "linear perturbations derive source terms and GR-proxy limit",
        },
        {
            "variation": "delta_R S_parent=0",
            "required_equation": "endpoint boundary-charge equation with Ward-fixed coefficients",
            "must_reduce_to": "R_early=1/3, R_today=1/9, DeltaR=2/9, B_mem=2/27",
            "current_gap": "formal quadratic exists, endpoint arrow and normalization not derived",
            "pass_condition": "amplitude fixed before scoring and not refit branch-by-branch",
        },
    ]


def perturbation_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "output": "friction correction",
            "symbol": "F_fric(a,k)",
            "required_derivation": "from linearized total stress/conservation, not fit function",
            "GR_limit": "F_fric -> 0",
            "current_status": "missing_derivation",
            "acceptance_test": "source-locked growth remains reproduced when derived term inserted",
        },
        {
            "output": "effective Newton function",
            "symbol": "mu(a,k)",
            "required_derivation": "modified Poisson equation from delta_g/delta_M variation",
            "GR_limit": "mu -> 1 or bounded |mu-1| by high-c_s law",
            "current_status": "effective_bound_only",
            "acceptance_test": "recovers checkpoint-149 bound or predicts controlled growth deviation",
        },
        {
            "output": "lensing/slip",
            "symbol": "eta_slip(a,k), Sigma(a,k)",
            "required_derivation": "anisotropic stress/slip from E_mem^{mu nu}",
            "GR_limit": "Phi=Psi and Sigma -> 1",
            "current_status": "missing_derivation",
            "acceptance_test": "no hidden lensing/CMB source appears",
        },
        {
            "output": "memory source",
            "symbol": "S_mem(a,k)",
            "required_derivation": "source term in growth/continuity/Euler equations",
            "GR_limit": "S_mem -> 0 for exact auxiliary or suppressed high-c_s memory",
            "current_status": "missing_derivation",
            "acceptance_test": "does not spoil growth/RSD reproduction or local PPN",
        },
        {
            "output": "sound-speed/constraint owner",
            "symbol": "c_s_eff^2 or lambda_M",
            "required_derivation": "from parent auxiliary/scalar sector",
            "GR_limit": "exact smooth memory or high-c_s subhorizon suppression",
            "current_status": "effective_route_only",
            "acceptance_test": "Boltzmann implementation avoids 1+w denominator instability",
        },
    ]


def local_gr_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "local_requirement": "local source silence",
            "symbol": "q_loc^nu -> 0",
            "must_prove": "local projection of memory/domain exchange vanishes or is bounded below PPN limits",
            "forbidden": "impose plateau/local vacuum axiom by hand",
            "failure_mode": "gamma-like q_R leak appears",
        },
        {
            "local_requirement": "Newton/GR potential limit",
            "symbol": "G_eff/G -> 1",
            "must_prove": "modified Poisson equation reduces to Newtonian/GR in weak bound systems",
            "forbidden": "assume R_AB=0 without parent variation",
            "failure_mode": "local closure remains benchmark only",
        },
        {
            "local_requirement": "PPN curvature",
            "symbol": "gamma=1, beta=1",
            "must_prove": "metric expansion yields Schwarzschild-equivalent exterior to tested order",
            "forbidden": "declare S=1/T^2 as derivation",
            "failure_mode": "q_R or delta_beta residual",
        },
        {
            "local_requirement": "clock/matter universality",
            "symbol": "alpha_clock=0, epsilon_matter=0",
            "must_prove": "universal coframe coupling and no local clock anomaly",
            "forbidden": "hide clock drift in calibration nuisance",
            "failure_mode": "redshift/equivalence-principle violation",
        },
        {
            "local_requirement": "weak-field lensing equality",
            "symbol": "Phi=Psi",
            "must_prove": "no local anisotropic memory stress or compensated stress cancellation",
            "forbidden": "ignore slip while using growth/CMB stress",
            "failure_mode": "lensing/PPN inconsistency",
        },
    ]


def cmb_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "interface_item": "background functions",
            "required_output": "rho_mem(a), w_mem(a), dw/dln a, Omega_mem(a)",
            "current_status": "contract_defined",
            "promotion_rule": "background safety is not CMB pass",
        },
        {
            "interface_item": "perturbation variables",
            "required_output": "delta_mem^GI, theta_mem, delta_p_mem^GI, pi_mem or exact auxiliary constraints",
            "current_status": "conditional_modes_only",
            "promotion_rule": "must be parent-derived before spectra claim",
        },
        {
            "interface_item": "Boltzmann implementation",
            "required_output": "CLASS/CAMB-ready closure avoiding 1+w singularity",
            "current_status": "future_kill_screen",
            "promotion_rule": "TT/TE/EE/lensing must be run without refitting bridge by hand",
        },
        {
            "interface_item": "calibration bridge",
            "required_output": "consistent late/CMB parameter map and sound-horizon treatment",
            "current_status": "unresolved_mixed",
            "promotion_rule": "compressed-distance or joint-calibration stress is not a CMB support claim",
        },
        {
            "interface_item": "late ISW/lensing",
            "required_output": "predicted spectra/kernels from same perturbation sector",
            "current_status": "not_run",
            "promotion_rule": "cannot be ignored once claiming perturbation theory",
        },
    ]


def amplitude_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "factor": "activation shape",
            "target": "A=1-exp(-I_M)",
            "current_status": "conditional_mechanics",
            "owner_required": "additive exposure/survival composition from parent load tensor",
            "demotion_if_missing": "shape remains closure grammar",
        },
        {
            "factor": "cubic exposure",
            "target": "I_M=X_D^3",
            "current_status": "conditional_mechanics",
            "owner_required": "Q^i_j=X_D delta^i_j from load-tensor variation",
            "demotion_if_missing": "FLRW-only insertion",
        },
        {
            "factor": "quarter scale",
            "target": "u3=1/4",
            "current_status": "conditional_cell_target",
            "owner_required": "3+1 cell theorem or equivalent parent normalization",
            "demotion_if_missing": "fixed empirical/theorem target",
        },
        {
            "factor": "boundary contrast",
            "target": "DeltaR=2/9",
            "current_status": "not_derived",
            "owner_required": "normalized endpoint law R_early=1/3 -> R_today=1/9",
            "demotion_if_missing": "2/27 remains empirical locked amplitude",
        },
        {
            "factor": "memory amplitude",
            "target": "B_mem=DeltaR/3=2/27",
            "current_status": "blocked_for_promotion",
            "owner_required": "parent map from boundary contrast to density amplitude",
            "demotion_if_missing": "no claim that MTS predicts B_mem",
        },
        {
            "factor": "coherent domain selector",
            "target": "D or chi_D selected without knobs",
            "current_status": "missing_derivation",
            "owner_required": "zero-knob variational selector that separates FLRW activity from local/bound silence",
            "demotion_if_missing": "domain choice remains closure-level and cannot promote local GR",
        },
    ]


def no_smuggling_rows() -> list[dict[str, Any]]:
    return [
        {
            "forbidden_move": "use empirical scorecard as derivation",
            "why_forbidden": "170-175 reproduce data lanes but do not vary an action",
            "allowed_replacement": "empirical branch motivates derivation work",
        },
        {
            "forbidden_move": "insert q_loc^nu -> 0 as plateau axiom",
            "why_forbidden": "local GR must reduce like GR to Newton, not by declaration",
            "allowed_replacement": "derive q_loc^nu from Bianchi-compatible parent stress",
        },
        {
            "forbidden_move": "fit BAO-only projection and call it two-point physics",
            "why_forbidden": "SN/H(z)/lensing null response must be theorem, not exemption",
            "allowed_replacement": "derive two-point ruler transport operator before use",
        },
        {
            "forbidden_move": "use pair-ruler sidecar in no-clock lead",
            "why_forbidden": "half-kernel parent ownership not proven",
            "allowed_replacement": "keep pair branch sidecar until single-pair source equation is derived",
        },
        {
            "forbidden_move": "claim CMB support from background safety",
            "why_forbidden": "primary memory fraction small does not run TT/TE/EE/lensing",
            "allowed_replacement": "future Boltzmann kill-screen with fixed branch",
        },
        {
            "forbidden_move": "declare B_mem=2/27 predicted",
            "why_forbidden": "endpoint quadratic and boundary charge not parent-derived",
            "allowed_replacement": "call 2/27 a locked empirical theorem target",
        },
    ]


def acceptance_gate_rows(
    sources: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    action_rows: list[dict[str, Any]],
    perturbation_rows: list[dict[str, Any]],
    local_rows: list[dict[str, Any]],
    cmb_rows: list[dict[str, Any]],
    amplitude_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row["path"] for row in sources if row["exists"] != "yes"]
    return [
        {
            "gate": "all_cited_sources_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": "all registered paths found" if not missing_sources else "; ".join(missing_sources),
        },
        {
            "gate": "active_blockers_mapped",
            "status": "pass" if len(blockers) == 6 else "fail",
            "evidence": f"blocker_rows={len(blockers)}",
        },
        {
            "gate": "parent_action_terms_specified",
            "status": "pass" if len(action_rows) >= 6 else "fail",
            "evidence": f"action_terms={len(action_rows)}",
        },
        {
            "gate": "perturbation_outputs_specified",
            "status": "pass" if len(perturbation_rows) >= 5 else "fail",
            "evidence": f"perturbation_outputs={len(perturbation_rows)}",
        },
        {
            "gate": "local_GR_silence_specified",
            "status": "pass" if len(local_rows) >= 5 else "fail",
            "evidence": f"local_requirements={len(local_rows)}",
        },
        {
            "gate": "CMB_interface_requirements_specified",
            "status": "pass" if len(cmb_rows) >= 5 else "fail",
            "evidence": f"CMB_requirements={len(cmb_rows)}",
        },
        {
            "gate": "amplitude_owner_specified",
            "status": "pass" if len(amplitude_rows) >= 5 else "fail",
            "evidence": f"amplitude_factors={len(amplitude_rows)}",
        },
        {
            "gate": "theory_promotion_blocked",
            "status": "pass",
            "evidence": "contract written, derivation not yet supplied",
        },
        {
            "gate": "claim_ceiling_preserved",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(gates: list[dict[str, Any]], blockers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failed = [row for row in gates if row["status"] != "pass"]
    status = STATUS_PASS if not failed else STATUS_FAIL
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"failed_gates={len(failed)}",
        },
        {
            "item": "contract_status",
            "verdict": "written_not_satisfied",
            "evidence": "exact pass/fail targets now stated; no action variation performed",
        },
        {
            "item": "active_blockers",
            "verdict": len(blockers),
            "evidence": "; ".join(row["gate_id"] for row in blockers),
        },
        {
            "item": "lead_branch",
            "verdict": LEAD_BRANCH,
            "evidence": "no-clock locked 2/27 remains empirical lead",
        },
        {
            "item": "promotion_allowed",
            "verdict": False,
            "evidence": "contract only; parent action, perturbations, local GR, CMB, domain, amplitude still unsatisfied",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "no derivation or public theory claim",
        },
        {
            "item": "next_target",
            "verdict": "178-memory-perturbation-owner-attempt.md",
            "evidence": "attempt the perturbation owner first because growth/CMB/local blockers depend on it",
        },
    ]


def run_contract(output_root: Path, timestamp: str | None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-parent-action-perturbation-local-GR-contract"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    blockers = blocker_contract_rows()
    action = parent_action_skeleton_rows()
    fields = field_variable_rows()
    variations = variation_equation_rows()
    perturbations = perturbation_contract_rows()
    local = local_gr_contract_rows()
    cmb = cmb_contract_rows()
    amplitude = amplitude_contract_rows()
    no_smuggling = no_smuggling_rows()
    gates = acceptance_gate_rows(sources, blockers, action, perturbations, local, cmb, amplitude)
    decisions = decision_rows(gates, blockers)
    status = decisions[0]["verdict"]

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "decision_run": str(DECISION_RUN),
            "promotion_run": str(PROMOTION_RUN),
            "purpose": "write exact parent-action contract; do not derive or promote",
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "promotion_blocker_map.csv", blockers, ["gate_id", "blocker", "current_status", "contract_target", "minimum_success_condition", "demotion_if_failed"])
    write_csv(results_dir / "minimal_parent_action_contract.csv", action, ["sector", "symbol", "required_action_term", "variation_target", "current_status", "forbidden_shortcut"])
    write_csv(results_dir / "field_variable_contract.csv", fields, ["object", "symbol", "type", "must_define", "observable_owner", "status"])
    write_csv(results_dir / "variation_requirement_contract.csv", variations, ["variation", "required_equation", "must_reduce_to", "current_gap", "pass_condition"])
    write_csv(results_dir / "perturbation_output_contract.csv", perturbations, ["output", "symbol", "required_derivation", "GR_limit", "current_status", "acceptance_test"])
    write_csv(results_dir / "local_GR_silence_contract.csv", local, ["local_requirement", "symbol", "must_prove", "forbidden", "failure_mode"])
    write_csv(results_dir / "CMB_interface_contract.csv", cmb, ["interface_item", "required_output", "current_status", "promotion_rule"])
    write_csv(results_dir / "amplitude_and_domain_ownership_contract.csv", amplitude, ["factor", "target", "current_status", "owner_required", "demotion_if_missing"])
    write_csv(results_dir / "forbidden_closure_ledger.csv", no_smuggling, ["forbidden_move", "why_forbidden", "allowed_replacement"])
    write_csv(results_dir / "acceptance_gates.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])
    write_json(
        run_dir / "status.json",
        {
            "status": status,
            "run_dir": str(run_dir),
            "results_dir": str(results_dir),
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "active_blockers": [row["gate_id"] for row in blockers],
            "promotion_allowed": False,
            "contract_written": status == STATUS_PASS,
            "derivation_performed": False,
            "next_target": "178-memory-perturbation-owner-attempt.md",
            "generated": [
                "source_register.csv",
                "promotion_blocker_map.csv",
                "minimal_parent_action_contract.csv",
                "field_variable_contract.csv",
                "variation_requirement_contract.csv",
                "perturbation_output_contract.csv",
                "local_GR_silence_contract.csv",
                "CMB_interface_contract.csv",
                "amplitude_and_domain_ownership_contract.csv",
                "forbidden_closure_ledger.csv",
                "acceptance_gates.csv",
                "decision.csv",
            ],
        },
    )
    marker = "DONE.txt" if status == STATUS_PASS else "FAILED.txt"
    (run_dir / marker).write_text(f"{status}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_contract(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
