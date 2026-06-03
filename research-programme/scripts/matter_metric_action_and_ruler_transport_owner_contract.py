#!/usr/bin/env python3
"""Checkpoint 204: test whether a parent matter action can own BAO ruler transport."""

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

CHECKPOINT_204_NAME = "matter-metric-action-and-ruler-transport-owner-contract"
CHECKPOINT_203_RUN = RUNS_ROOT / "20260601-000020-fossil-ruler-transport-equation-attempt"
CHECKPOINT_194_RUN = RUNS_ROOT / "20260601-000011-half-memory-clock-map-derivation-attempt"
CHECKPOINT_177_RUN = RUNS_ROOT / "20260531-235959-parent-action-perturbation-local-GR-contract"

STATUS = "matter_metric_action_derives_label_transport_MTS_source_zero_conditionally_C_silence_missing"
CLAIM_CEILING = "parent_matter_action_candidate_internal_only_C_silence_and_full_parent_missing"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"


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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 204 matter-action owner script"),
        (WORK_DIR / "203-fossil-ruler-transport-equation-attempt.md", "previous fossil-ruler transport checkpoint"),
        (CHECKPOINT_203_RUN / "status.json", "checkpoint 203 machine status"),
        (CHECKPOINT_203_RUN / "results" / "transport_equation_chain.csv", "checkpoint 203 transport chain"),
        (CHECKPOINT_203_RUN / "results" / "parent_matter_action_contract.csv", "checkpoint 203 parent matter action contract"),
        (WORK_DIR / "194-half-memory-clock-map-derivation-attempt.md", "matter metric clock-map checkpoint"),
        (CHECKPOINT_194_RUN / "status.json", "checkpoint 194 machine status"),
        (WORK_DIR / "177-parent-action-perturbation-local-GR-contract.md", "broader parent-action contract"),
        (CHECKPOINT_177_RUN / "status.json", "checkpoint 177 machine status"),
        (WORK_DIR / "19-constrained-parent-action-skeleton.md", "early constrained parent-action skeleton"),
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


def candidate_parent_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector": "metric_and_memory",
            "candidate_term": "S_geom[g] + S_C[g,C,...]",
            "role": "owns gravitational field equations and the memory/conformal scalar sector",
            "variation_target": "delta_g, delta_C",
            "derived_here": "no",
            "issue": "C dynamics, amplitude B_mem=2/27, and saturation/local silence remain outside this checkpoint",
        },
        {
            "sector": "matter_metric",
            "candidate_term": "tilde_g_mn = exp(C) g_mn",
            "role": "defines the matter-observer metric used by late rulers and clocks",
            "variation_target": "algebraic metric map",
            "derived_here": "conditional",
            "issue": "the map is usable only if the parent action selects universal matter coupling",
        },
        {
            "sector": "universal_matter",
            "candidate_term": "S_m[psi_m, tilde_g_mn] = integral sqrt(-tilde_g) L_m(psi_m, tilde_g_mn)",
            "role": "forces all late matter tracers to share the same ruler/clock metric",
            "variation_target": "delta_psi_m, delta_tilde_g",
            "derived_here": "yes_as_candidate_action_contract",
            "issue": "does not by itself derive why this sector is the unique MTS coupling",
        },
        {
            "sector": "post_drag_dust_labels",
            "candidate_term": "S_dust = integral[-sqrt(-tilde_g) rho(n) + J^m(partial_m phi + alpha_A partial_m X^A)] d^4x",
            "role": "gives conserved matter current and convected labels after drag",
            "variation_target": "delta_phi, delta_alpha_A, delta_X_A, delta_J",
            "derived_here": "yes_conditionally",
            "issue": "dust limit is valid only after pressure/slip/reconstruction terms are treated as shared corrections",
        },
        {
            "sector": "two_point_ruler",
            "candidate_term": "xi_BAO[X^A_1-X^A_2,t] with post-drag source S_xi",
            "role": "turns label transport into BAO-peak transport",
            "variation_target": "effective two-point transport equation",
            "derived_here": "partial",
            "issue": "action gives labels but not a full nonlinear two-point closure; S_xi must be zero or bounded",
        },
        {
            "sector": "domain_selector",
            "candidate_term": "O -> {photon_endpoint, late_matter_ruler, perturbation_path}",
            "role": "prevents post-hoc switching between CMB and BAO projection rules",
            "variation_target": "observable map from parent coupling class",
            "derived_here": "no",
            "issue": "domain rule remains a contract, not a variational theorem",
        },
    ]


def noether_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Assume all late matter fields couple only to the matter metric.",
            "equation": "S_m = S_m[psi_m, tilde_g_mn], tilde_g_mn=exp(C)g_mn",
            "status": "candidate_parent_contract",
            "remaining_gap": "parent theory must justify universal coupling",
        },
        {
            "step": 2,
            "statement": "Define the matter-frame stress tensor by variation with respect to tilde_g_mn.",
            "equation": "T_tilde^{mn} = (2/sqrt(-tilde_g)) delta S_m / delta tilde_g_mn",
            "status": "standard_variational_definition",
            "remaining_gap": "none inside the candidate matter sector",
        },
        {
            "step": 3,
            "statement": "Diffeomorphism invariance of the on-shell matter sector gives matter-frame conservation.",
            "equation": "tilde_nabla_m T_tilde^{mn}=0",
            "status": "derived_conditionally",
            "remaining_gap": "fails if matter has explicit nonmetric C couplings or nonuniversal tracer metrics",
        },
        {
            "step": 4,
            "statement": "The same conservation looks like an exchange term in the Einstein g-frame.",
            "equation": "nabla_m T_g^{mn} = source[C,T] rather than zero for the matter sector alone",
            "status": "frame_warning",
            "remaining_gap": "total stress must still satisfy the full Bianchi identity",
        },
        {
            "step": 5,
            "statement": "For BAO ruler transport, the relevant no-fifth-force statement is matter-frame geodesic motion.",
            "equation": "u^m tilde_nabla_m u^n=0 for post-drag dust",
            "status": "derived_if_dust_action_holds",
            "remaining_gap": "C gradients can reappear as apparent forces in the g-frame; local/BAO silence still needed",
        },
    ]


def dust_label_variation_rows() -> list[dict[str, Any]]:
    return [
        {
            "variation": "delta_phi",
            "action_piece": "J^m partial_m phi",
            "euler_lagrange_result": "partial_m J^m = 0",
            "transport_result": "matter number current is conserved",
            "status": "derived_from_candidate_dust_action",
        },
        {
            "variation": "delta_alpha_A",
            "action_piece": "J^m alpha_A partial_m X^A",
            "euler_lagrange_result": "J^m partial_m X^A = 0",
            "transport_result": "u^m partial_m X^A = 0 when J^m=n u^m sqrt(-tilde_g)",
            "status": "derived_from_candidate_dust_action",
        },
        {
            "variation": "delta_X^A",
            "action_piece": "J^m alpha_A partial_m X^A",
            "euler_lagrange_result": "partial_m(J^m alpha_A)=0",
            "transport_result": "label momenta are advected with the flow",
            "status": "derived_from_candidate_dust_action",
        },
        {
            "variation": "delta_J^m",
            "action_piece": "-sqrt(-tilde_g)rho(n)+J^m(partial_m phi+alpha_A partial_m X^A)",
            "euler_lagrange_result": "flow momentum is a gradient/label one-form",
            "transport_result": "post-drag dust four-velocity is determined by the matter action",
            "status": "derived_conditionally",
        },
        {
            "variation": "delta_tilde_g_mn",
            "action_piece": "-sqrt(-tilde_g)rho(n)",
            "euler_lagrange_result": "T_tilde^{mn}=rho u^m u^n for pressureless dust",
            "transport_result": "u^m tilde_nabla_m u^n=0 follows with tilde_nabla_m T_tilde^{mn}=0",
            "status": "derived_in_pressureless_limit",
        },
        {
            "variation": "pair_label_subtraction",
            "action_piece": "two solutions X^A_1 and X^A_2 of the same advection equation",
            "euler_lagrange_result": "D_t(X^A_1-X^A_2)=0",
            "transport_result": "D_t Delta X^A = 0",
            "status": "derived_after_label_equation",
        },
    ]


def source_term_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_term": "S_xi_standard_nonlinear",
            "origin": "standard gravity, mode coupling, reconstruction, bias, and shell crossing",
            "does_candidate_action_remove_it": "no",
            "MTS_specific_or_shared": "shared_with_baselines",
            "required_policy": "model symmetrically for LCDM/wCDM/CPL/MTS; do not count as MTS-only failure",
            "status": "shared_nuisance_not_parent_proof",
        },
        {
            "source_term": "S_xi_pressure_slip",
            "origin": "baryon pressure or baryon-CDM relative velocity after drag",
            "does_candidate_action_remove_it": "only in ideal post-drag dust limit",
            "MTS_specific_or_shared": "mostly_shared_standard_correction",
            "required_policy": "show correction is below BAO tolerance or included in shared modeling",
            "status": "bounded_not_eliminated",
        },
        {
            "source_term": "S_xi_C_spatial_gradient",
            "origin": "spatial variation of C creates non-common-mode matter metric distortions",
            "does_candidate_action_remove_it": "no",
            "MTS_specific_or_shared": "MTS_specific",
            "required_policy": "derive partial_i C approx 0 in BAO domain or bound anisotropic source",
            "status": "main_open_MTS_source",
        },
        {
            "source_term": "S_xi_C_time_drift",
            "origin": "dot_C/H leakage changes radial D_H/r_d projection",
            "does_candidate_action_remove_it": "no",
            "MTS_specific_or_shared": "MTS_specific",
            "required_policy": "derive saturation or use DESI radial bound from checkpoint 198",
            "status": "empirically_bounded_not_parent_derived",
        },
        {
            "source_term": "S_xi_nonuniversal_tracer_metric",
            "origin": "different galaxies/matter species couple to different effective metrics",
            "does_candidate_action_remove_it": "yes_if_universal_matter_metric_is_enforced",
            "MTS_specific_or_shared": "MTS_specific_if_present",
            "required_policy": "universal coupling is mandatory; otherwise BAO common-mode theorem fails",
            "status": "closed_conditionally_by_action_contract",
        },
        {
            "source_term": "S_xi_photon_endpoint_memory",
            "origin": "incorrectly treating BAO as direct early photon endpoint like CMB",
            "does_candidate_action_remove_it": "yes_if_domain_selector_is accepted",
            "MTS_specific_or_shared": "MTS_projection_error",
            "required_policy": "derive domain selector from couplings, not from fit preference",
            "status": "rule_written_not_action_derived",
        },
    ]


def frame_hazard_rows() -> list[dict[str, Any]]:
    return [
        {
            "hazard": "Einstein-frame fifth-force misread",
            "mathematical_form": "a_g^n includes projected gradients of C when written in g variables",
            "why_it_matters": "could be mistaken for violation of dust/geodesic transport",
            "resolution_if_any": "matter-frame geodesic motion is fine, but spatial C gradients still create observable distortions",
            "status": "requires_C_gradient_bound",
        },
        {
            "hazard": "universal conformal scaling becomes invisible locally",
            "mathematical_form": "tilde_D_X and tilde_r_BAO both scale by exp(C_obs/2)",
            "why_it_matters": "late BAO common-mode cancellation works only for shared C",
            "resolution_if_any": "derive homogeneous/saturated C in late BAO bins",
            "status": "conditional_strength",
        },
        {
            "hazard": "Bianchi identity accounting",
            "mathematical_form": "nabla_m(E_geom^{mn}+E_C^{mn}+T_g^{mn})=0",
            "why_it_matters": "matter-frame conservation cannot violate total conservation",
            "resolution_if_any": "full parent action must include C stress/exchange",
            "status": "full_parent_action_missing",
        },
        {
            "hazard": "using BAO action owner as CMB proof",
            "mathematical_form": "late fossil-ruler transport does not derive theta_* or acoustic spectra",
            "why_it_matters": "would overclaim the CMB bridge",
            "resolution_if_any": "keep CMB endpoint branch separate",
            "status": "guardrail",
        },
        {
            "hazard": "exact peak conservation overclaim",
            "mathematical_form": "D_t r_BAO^comoving=0 only for source-free label-space xi",
            "why_it_matters": "real BAO analyses include nonlinear peak shifts",
            "resolution_if_any": "claim only no extra MTS-specific source under action conditions",
            "status": "claim_ceiling_enforced",
        },
    ]


def owner_scorecard_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement": "universal late matter metric",
            "owned_by_candidate_action": "yes_conditionally",
            "evidence": "single S_m[psi_m, tilde_g_mn] for all late matter tracers",
            "remaining_gap": "why this coupling is selected by the full MTS parent theory",
            "promotion_status": "partial_pass",
        },
        {
            "requirement": "matter-frame Noether conservation",
            "owned_by_candidate_action": "yes_conditionally",
            "evidence": "diffeomorphism-invariant S_m gives tilde_nabla_m T_tilde^{mn}=0",
            "remaining_gap": "full g-frame Bianchi accounting still needs C sector",
            "promotion_status": "partial_pass",
        },
        {
            "requirement": "convected post-drag labels",
            "owned_by_candidate_action": "yes_conditionally",
            "evidence": "dust-label action gives J^m partial_m X^A=0",
            "remaining_gap": "pressure/slip/nonlinear corrections must be shared and bounded",
            "promotion_status": "partial_pass",
        },
        {
            "requirement": "no MTS-specific post-drag BAO peak source",
            "owned_by_candidate_action": "conditional_only",
            "evidence": "universal homogeneous matter metric introduces no species-dependent ruler source",
            "remaining_gap": "spatial/time C gradients and source term S_xi are not derived zero",
            "promotion_status": "not_promoted",
        },
        {
            "requirement": "late common-mode BAO ratio",
            "owned_by_candidate_action": "conditional_only",
            "evidence": "same tilde metric scales late distance and fossil ruler by exp(C_obs/2)",
            "remaining_gap": "C saturation/local silence and domain selector still missing",
            "promotion_status": "strengthened_not_promoted",
        },
        {
            "requirement": "full field-theory promotion",
            "owned_by_candidate_action": "no",
            "evidence": "this only handles the matter/ruler transport subproblem",
            "remaining_gap": "B_mem amplitude, perturbations, CMB, local PPN, full parent action",
            "promotion_status": "blocked",
        },
    ]


def acceptance_gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal derivation audit",
        },
        {
            "gate": "candidate matter action written",
            "status": "pass",
            "evidence": "S_m[psi_m,tilde_g] plus dust-label action specified",
            "claim_allowed": "candidate owner",
        },
        {
            "gate": "matter-frame conservation derived",
            "status": "conditional_pass",
            "evidence": "diffeomorphism identity gives tilde_nabla T=0 if coupling is universal and metric-only",
            "claim_allowed": "conditional theorem piece",
        },
        {
            "gate": "label transport derived from variation",
            "status": "conditional_pass",
            "evidence": "delta_alpha_A gives J^m partial_m X^A=0",
            "claim_allowed": "conditional theorem piece",
        },
        {
            "gate": "MTS-specific BAO source eliminated",
            "status": "conditional_pass",
            "evidence": "universal homogeneous matter metric gives no species-dependent post-drag source",
            "claim_allowed": "only if C gradients/drift are separately silent",
        },
        {
            "gate": "C silence derived",
            "status": "fail",
            "evidence": "partial_i C approx 0 and dot_C/H small remain separate parent/local-domain burdens",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "full BAO support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "A concrete matter-action route can own the conserved-label half of fossil-ruler transport. A universal matter metric plus dust-label action derives matter-frame conservation and u^m partial_m X^A=0. It conditionally removes MTS-specific nonuniversal ruler sources, but it does not derive C spatial silence, C time-drift silence, the full two-point source S_xi, or the full MTS parent action.",
            "derived_piece": "S_m[psi,tilde_g] and dust-label variation derive tilde_nabla_m T_tilde^{mn}=0 and u^m partial_m X^A=0",
            "conditional_gain": "late BAO common-mode route now has a candidate action owner for matter labels and universal ruler coupling",
            "main_blocker": "C_gradient_time_drift_silence_and_full_two_point_source_owner",
            "next_target": "205-C-silence-source-bound-for-BAO-and-local-rulers.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_204_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    action_rows = candidate_parent_action_rows()
    noether_rows = noether_derivation_rows()
    label_rows = dust_label_variation_rows()
    source_rows_audit = source_term_audit_rows()
    hazard_rows = frame_hazard_rows()
    owner_rows = owner_scorecard_rows()
    gates = acceptance_gate_rows(source_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "candidate_parent_action.csv": (
            action_rows,
            ["sector", "candidate_term", "role", "variation_target", "derived_here", "issue"],
        ),
        "noether_conservation_derivation.csv": (
            noether_rows,
            ["step", "statement", "equation", "status", "remaining_gap"],
        ),
        "dust_label_variation_derivation.csv": (
            label_rows,
            ["variation", "action_piece", "euler_lagrange_result", "transport_result", "status"],
        ),
        "BAO_source_term_audit.csv": (
            source_rows_audit,
            ["source_term", "origin", "does_candidate_action_remove_it", "MTS_specific_or_shared", "required_policy", "status"],
        ),
        "frame_and_fifth_force_hazards.csv": (
            hazard_rows,
            ["hazard", "mathematical_form", "why_it_matters", "resolution_if_any", "status"],
        ),
        "ruler_transport_owner_scorecard.csv": (
            owner_rows,
            ["requirement", "owned_by_candidate_action", "evidence", "remaining_gap", "promotion_status"],
        ),
        "acceptance_gates.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "derived_piece",
                "conditional_gain",
                "main_blocker",
                "next_target",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, (rows, fieldnames) in files.items():
        write_csv(results_dir / filename, rows, fieldnames)

    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "candidate_matter_action_written": True,
        "matter_frame_conservation_derived_conditionally": True,
        "dust_label_transport_derived_conditionally": True,
        "MTS_specific_nonuniversal_ruler_source_removed_conditionally": True,
        "C_silence_derived": False,
        "full_two_point_source_owner_derived": False,
        "full_parent_action_derived": False,
        "promotion_allowed": False,
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    payload = run(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
