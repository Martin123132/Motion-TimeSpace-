#!/usr/bin/env python3
"""Checkpoint 208: domain representative selection law audit."""

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

CHECKPOINT_208_NAME = "domain-representative-selection-law"
CHECKPOINT_207_RUN = RUNS_ROOT / "20260601-000024-domain-projector-action-and-Bianchi-identity"
CHECKPOINT_206_RUN = RUNS_ROOT / "20260601-000023-parent-C-screening-fixed-point-mechanism"
CHECKPOINT_205_RUN = RUNS_ROOT / "20260601-000022-C-silence-source-bound-for-BAO-and-local-rulers"

STATUS = "domain_representative_law_conditionally_selects_ideal_branches_parent_domain_scale_missing"
CLAIM_CEILING = "representative_selection_law_internal_only_no_domain_or_local_GR_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

LOCKED_B_MEM = 2.0 / 27.0
H0_KM_S_MPC = 67.50994528839665
LIGHT_SPEED_KM_S = 299_792.458
HUBBLE_RADIUS_MPC = LIGHT_SPEED_KM_S / H0_KM_S_MPC


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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 208 representative-selection script"),
        (WORK_DIR / "207-domain-projector-action-and-Bianchi-identity.md", "domain projector/Bianchi checkpoint"),
        (CHECKPOINT_207_RUN / "status.json", "checkpoint 207 machine status"),
        (CHECKPOINT_207_RUN / "results" / "representative_selection_obligations.csv", "checkpoint 207 representative obligations"),
        (WORK_DIR / "206-parent-C-screening-fixed-point-mechanism.md", "zero-mode C-screening checkpoint"),
        (CHECKPOINT_206_RUN / "results" / "zero_mode_domain_dilution.csv", "checkpoint 206 zero-mode dilution"),
        (WORK_DIR / "205-C-silence-source-bound-for-BAO-and-local-rulers.md", "C-silence source/bounds checkpoint"),
        (CHECKPOINT_205_RUN / "results" / "memory_gradient_scenarios.csv", "checkpoint 205 smooth-memory scenarios"),
        (WORK_DIR / "143-domain-selector-variational-action-attempt.md", "domain selector variational attempt"),
        (WORK_DIR / "132-smooth-memory-growth-theorem-attempt.md", "linear C_coh cancellation checkpoint"),
        (WORK_DIR / "93-Lcg-trace-contrast-owner-gate.md", "L_cg Hubble-cap coherence checkpoint"),
        (WORK_DIR / "78-parent-uD-owner-contract.md", "parent u/D owner contract"),
        (WORK_DIR / "80-stress-free-reference-action-gate.md", "demoted local C_coh parent route guardrail"),
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


def ccoh(theta_mean: float, theta2_mean: float, shear2_mean: float, vorticity2_mean: float, eps: float = 0.0) -> float:
    denominator = theta2_mean + shear2_mean + vorticity2_mean + eps
    if denominator == 0.0:
        return 0.0
    return theta_mean * theta_mean / denominator


def coherence_branch_score_rows() -> list[dict[str, Any]]:
    cases = [
        {
            "branch": "stationary_local_bound_bulk",
            "theta_mean": 0.0,
            "theta2_mean": 0.0,
            "shear2_mean": 1.0,
            "vorticity2_mean": 1.0,
            "eps_D": 0.0,
            "expected_representative": "trivial_local_class",
            "interpretation": "no coherent expansion; local bound class should not carry memory zero-mode",
        },
        {
            "branch": "quiet_Minkowski_limit",
            "theta_mean": 0.0,
            "theta2_mean": 0.0,
            "shear2_mean": 0.0,
            "vorticity2_mean": 0.0,
            "eps_D": 1.0e-30,
            "expected_representative": "trivial_local_class",
            "interpretation": "no expansion invariant; eps keeps expression defined but selected memory class is zero",
        },
        {
            "branch": "ideal_FLRW",
            "theta_mean": 1.0,
            "theta2_mean": 1.0,
            "shear2_mean": 0.0,
            "vorticity2_mean": 0.0,
            "eps_D": 0.0,
            "expected_representative": "nontrivial_coherent_FLRW_class",
            "interpretation": "homogeneous expansion selects coherent zero-mode",
        },
        {
            "branch": "linear_FLRW_scalar_perturbed",
            "theta_mean": 1.01,
            "theta2_mean": 1.0201,
            "shear2_mean": 1.0e-4,
            "vorticity2_mean": 0.0,
            "eps_D": 0.0,
            "expected_representative": "nontrivial_coherent_FLRW_class_with_second_order_residual",
            "interpretation": "linear expansion perturbation cancels; only quadratic shear/variance reduces C_coh",
        },
        {
            "branch": "BAO_late_smooth_domain",
            "theta_mean": 1.0,
            "theta2_mean": 1.0005,
            "shear2_mean": 2.0e-4,
            "vorticity2_mean": 0.0,
            "eps_D": 0.0,
            "expected_representative": "late_common_mode_smooth_class",
            "interpretation": "large-scale late domain is close to FLRW but must still satisfy BAO C-gradient bounds",
        },
        {
            "branch": "collapsed_merger_or_wall",
            "theta_mean": 0.2,
            "theta2_mean": 1.0,
            "shear2_mean": 1.0,
            "vorticity2_mean": 0.5,
            "eps_D": 0.0,
            "expected_representative": "transition_boundary_open",
            "interpretation": "mixed/high-shear region requires boundary current; not safe to promote",
        },
    ]
    rows: list[dict[str, Any]] = []
    for case in cases:
        value = ccoh(
            float(case["theta_mean"]),
            float(case["theta2_mean"]),
            float(case["shear2_mean"]),
            float(case["vorticity2_mean"]),
            float(case["eps_D"]),
        )
        rows.append(
            {
                **case,
                "C_coh": value,
                "selector_readout": (
                    "memory_off_or_trivial" if value < 0.1 else "memory_on_or_common_mode" if value > 0.9 else "transition_unpromoted"
                ),
                "promotion_status": "conditional_branch_readout_not_parent_selection",
            }
        )
    return rows


def representative_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_piece": "coherence_invariant",
            "mathematical_form": "C_coh[D]=<theta>_D^2/(<theta^2>_D+<sigma^2>_D+<omega^2>_D+eps_D)",
            "selects": "trivial local class when coherent expansion vanishes; FLRW class when shear/vorticity vanish",
            "status": "conditional_selector_not_domain_owner",
            "failure_mode": "using C_coh as a parent local-GR proof was demoted earlier",
        },
        {
            "law_piece": "linear_FLRW_stability",
            "mathematical_form": "delta C_coh^(1)=0 around FLRW bulk",
            "selects": "smooth memory does not acquire a first-order clustering representative",
            "status": "conditional_pass_from_checkpoint_132",
            "failure_mode": "gauge-invariant stress variation still missing",
        },
        {
            "law_piece": "relative_class_readout",
            "mathematical_form": "[J_rel]=0 for stationary/exact local class; [J_rel]!=0 for coherent expansion class",
            "selects": "local trivial versus FLRW nontrivial topology label",
            "status": "formal_support_not_parent_derived",
            "failure_mode": "representative not forced by action",
        },
        {
            "law_piece": "BAO_late_common_mode_readout",
            "mathematical_form": "BAO readout occurs inside late smooth domain with |Delta C| and |dot_C/H| below bounds",
            "selects": "late matter-ruler common-mode representative",
            "status": "bounded_conditional",
            "failure_mode": "BAO domain could become data-tuned unless L_D is predeclared",
        },
        {
            "law_piece": "domain_scale_precommitment",
            "mathematical_form": "L_D = L_cg = [L_H^-2 + alpha_K G_K^2]^-1/2; FLRW gives L_D=c/H",
            "selects": "Hubble-domain coherent zero-mode in homogeneous cosmology",
            "status": "conditional_from_checkpoint_93",
            "failure_mode": "L_cg remains a closure rule, not a microscopic parent theorem",
        },
    ]


def domain_scale_precommitment_rows() -> list[dict[str, Any]]:
    bao_length_mpc = 150.0
    bao_fraction = bao_length_mpc / HUBBLE_RADIUS_MPC
    delta_c_hubble_150 = LOCKED_B_MEM * bao_fraction
    half_shift = 0.5 * delta_c_hubble_150
    smooth_rows = read_csv_rows(CHECKPOINT_205_RUN / "results" / "memory_gradient_scenarios.csv")
    checkpoint_row = next(
        row
        for row in smooth_rows
        if row["scenario"] == "full_B_over_Hubble_radius" and row["probe_length_Mpc"] == "150.0"
    )
    dilution_rows = read_csv_rows(CHECKPOINT_206_RUN / "results" / "zero_mode_domain_dilution.csv")
    dilution_row = next(
        row
        for row in dilution_rows
        if row["source_region"] == "150 Mpc BAO patch" and row["domain"] == "Hubble domain"
    )
    return [
        {
            "scale_rule": "FLRW_Hubble_cap",
            "mathematical_form": "G_K=0 -> L_D=L_cg=L_H=c/H",
            "length_Mpc": HUBBLE_RADIUS_MPC,
            "data_tuned": "no_if_Lcg_rule_is_predeclared",
            "numeric_check": "eta=H0 L_D/c = 1",
            "status": "conditional_precommitment",
        },
        {
            "scale_rule": "BAO_patch_inside_Hubble_domain",
            "mathematical_form": "L_BAO/L_D",
            "length_Mpc": bao_length_mpc,
            "data_tuned": "no_if_BAO_patch_is_test_scale_not_projector_scale",
            "numeric_check": bao_fraction,
            "status": "BAO_patch_is_subdomain",
        },
        {
            "scale_rule": "smooth_C_over_Hubble_check",
            "mathematical_form": "0.5 B_mem (150 Mpc/L_H)",
            "length_Mpc": bao_length_mpc,
            "data_tuned": "no",
            "numeric_check": half_shift,
            "status": "safe_vs_checkpoint_205_chi2_lt1" if checkpoint_row["verdict"] == "safe_for_chi2_lt_1" else "unsafe",
        },
        {
            "scale_rule": "zero_mode_dilution_check",
            "mathematical_form": "B_mem (150 Mpc/L_H)^3",
            "length_Mpc": bao_length_mpc,
            "data_tuned": "no",
            "numeric_check": dilution_row["Bmem_times_volume_fraction"],
            "status": "safe_vs_local_and_BAO_gates"
            if dilution_row["safe_vs_local_deltaC_gate"] == "yes" and dilution_row["safe_vs_BAO_150_deltaC_gate"] == "yes"
            else "unsafe",
        },
        {
            "scale_rule": "nonFLRW_bound_domain",
            "mathematical_form": "large G_K or low C_coh shortens/suppresses coherent memory representative",
            "length_Mpc": "",
            "data_tuned": "not_yet_proven",
            "numeric_check": "requires parent G_K/domain equation",
            "status": "open",
        },
    ]


def representative_selection_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "representative": "local_stationary_trivial",
            "selection_condition": "theta_mean -> 0 or noncoherent shear/vorticity dominates",
            "result": "C_coh -> 0 and [J_rel] trivial/exact",
            "status": "conditional_pass",
            "remaining_gap": "must be forced by parent domain labels, not by importing GR-bound-system intuition",
        },
        {
            "representative": "FLRW_nontrivial",
            "selection_condition": "homogeneous expansion, sigma=omega=0, G_K=0",
            "result": "C_coh=1, L_D=c/H, coherent zero-mode allowed",
            "status": "conditional_pass",
            "remaining_gap": "B_mem amplitude and transition law not derived",
        },
        {
            "representative": "BAO_late_common_mode",
            "selection_condition": "late smooth domain inside predeclared Hubble-cap coherent mode",
            "result": "BAO C-gradient/drift bounds can be satisfied without choosing L_D from BAO fit",
            "status": "conditional_pass",
            "remaining_gap": "actual parent L_D and C transition law missing",
        },
        {
            "representative": "transition_boundary",
            "selection_condition": "C_coh changes or domain boundary moves",
            "result": "requires J_rel/boundary exchange current",
            "status": "open",
            "remaining_gap": "boundary representative still not parent-derived",
        },
        {
            "representative": "data_tuned_domain",
            "selection_condition": "choose L_D or threshold after BAO/local scoring",
            "result": "rejected",
            "status": "fail_rejected",
            "remaining_gap": "not allowed",
        },
    ]


def promotion_gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal selection-law audit",
        },
        {
            "gate": "ideal local representative selected",
            "status": "conditional_pass",
            "evidence": "C_coh -> 0 for stationary/quiet local branches",
            "claim_allowed": "branch readout only",
        },
        {
            "gate": "ideal FLRW representative selected",
            "status": "conditional_pass",
            "evidence": "C_coh=1 and L_cg=L_H for homogeneous FLRW",
            "claim_allowed": "branch readout only",
        },
        {
            "gate": "linear FLRW perturbation safe",
            "status": "conditional_pass",
            "evidence": "checkpoint 132 gives delta C_coh^(1)=0",
            "claim_allowed": "conditional perturbation support",
        },
        {
            "gate": "BAO late-common-mode representative predeclared",
            "status": "conditional_pass",
            "evidence": "Hubble-cap domain is independent of BAO and passes smooth/dilution checks",
            "claim_allowed": "conditional test route",
        },
        {
            "gate": "domain scale parent-derived",
            "status": "fail",
            "evidence": "L_cg rule remains closure, not microscopic action theorem",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "boundary/transition representative selected",
            "status": "fail",
            "evidence": "J_rel physical representative and moving boundary law remain open",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "local GR or BAO support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "A conditional representative-selection law is now explicit: C_coh selects local trivial versus FLRW coherent branches in ideal limits, linear FLRW perturbations are first-order safe, and the BAO late-common-mode branch can be tied to a predeclared Hubble-cap L_cg domain rather than chosen from BAO success. But L_cg/domain scale, boundary representative, and transition law are not parent-derived.",
            "main_gain": "local/FLRW/BAO representatives are no longer free verbal choices; they have a conditional selection ledger",
            "best_live_law": "C_coh branch readout plus predeclared L_D=L_cg Hubble-cap in FLRW",
            "main_blocker": "derive L_cg/domain scale and J_rel transition representative from parent action",
            "next_target": "209-Lcg-domain-scale-parent-derivation-or-demotion.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_208_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    branch_rows = coherence_branch_score_rows()
    law_rows = representative_law_rows()
    scale_rows = domain_scale_precommitment_rows()
    selection_rows = representative_selection_gate_rows()
    gates = promotion_gate_rows(source_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "coherence_branch_scores.csv": (
            branch_rows,
            [
                "branch",
                "theta_mean",
                "theta2_mean",
                "shear2_mean",
                "vorticity2_mean",
                "eps_D",
                "expected_representative",
                "interpretation",
                "C_coh",
                "selector_readout",
                "promotion_status",
            ],
        ),
        "representative_selection_law.csv": (
            law_rows,
            ["law_piece", "mathematical_form", "selects", "status", "failure_mode"],
        ),
        "domain_scale_precommitment.csv": (
            scale_rows,
            ["scale_rule", "mathematical_form", "length_Mpc", "data_tuned", "numeric_check", "status"],
        ),
        "representative_selection_gates.csv": (
            selection_rows,
            ["representative", "selection_condition", "result", "status", "remaining_gap"],
        ),
        "promotion_gates.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "main_gain",
                "best_live_law",
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
        "ideal_local_representative_conditionally_selected": True,
        "ideal_FLRW_representative_conditionally_selected": True,
        "BAO_late_common_mode_representative_conditionally_predeclared": True,
        "domain_scale_parent_derived": False,
        "boundary_transition_representative_derived": False,
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
