#!/usr/bin/env python3
"""Checkpoint 209: derive or demote the L_cg domain-scale rule."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_209_NAME = "Lcg-domain-scale-parent-derivation-or-demotion"
CHECKPOINT_208_RUN = RUNS_ROOT / "20260601-000025-domain-representative-selection-law"
CHECKPOINT_207_RUN = RUNS_ROOT / "20260601-000024-domain-projector-action-and-Bianchi-identity"
CHECKPOINT_205_RUN = RUNS_ROOT / "20260601-000022-C-silence-source-bound-for-BAO-and-local-rulers"

STATUS = "Lcg_rule_formal_inverse_coherence_scale_parent_GK_alpha_missing_closure_retained"
CLAIM_CEILING = "Lcg_rule_conditional_closure_no_parent_scale_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

H0_KM_S_MPC = 67.50994528839665
LIGHT_SPEED_KM_S = 299_792.458
HUBBLE_RADIUS_MPC = LIGHT_SPEED_KM_S / H0_KM_S_MPC
LOCKED_B_MEM = 2.0 / 27.0


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
        (Path(__file__).resolve(), "checkpoint 209 L_cg scale script"),
        (WORK_DIR / "208-domain-representative-selection-law.md", "previous domain representative checkpoint"),
        (CHECKPOINT_208_RUN / "status.json", "checkpoint 208 machine status"),
        (CHECKPOINT_208_RUN / "results" / "domain_scale_precommitment.csv", "checkpoint 208 domain scale precommitment"),
        (WORK_DIR / "93-Lcg-trace-contrast-owner-gate.md", "earlier L_cg eta gate"),
        (WORK_DIR / "92-memory-stress-amplitude-prediction-attempt.md", "memory stress amplitude/L_cg target"),
        (WORK_DIR / "96-parent-R-normalization-contract.md", "parent normalization and L_cg^-2 contract"),
        (WORK_DIR / "97-canonical-R-theorem-attempt.md", "canonical R theorem attempt"),
        (WORK_DIR / "207-domain-projector-action-and-Bianchi-identity.md", "domain projector/Bianchi checkpoint"),
        (CHECKPOINT_207_RUN / "status.json", "checkpoint 207 machine status"),
        (WORK_DIR / "205-C-silence-source-bound-for-BAO-and-local-rulers.md", "C-silence source/bound checkpoint"),
        (CHECKPOINT_205_RUN / "results" / "BAO_spatial_gradient_bounds.csv", "checkpoint 205 BAO spatial bounds"),
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


def L_cg(alpha_k: float, g_k_per_mpc: float) -> float:
    return 1.0 / math.sqrt(HUBBLE_RADIUS_MPC ** -2 + alpha_k * g_k_per_mpc * g_k_per_mpc)


def derivation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "claim": "A coherent averaging/domain scale must not exceed the causal/background Hubble length.",
            "equation": "L_D <= L_H = c/H",
            "status": "physical_cap_condition",
            "gap": "causal cap alone does not set the response to inhomogeneous domains",
        },
        {
            "step": 2,
            "claim": "Inhomogeneous or high-gradient domains need an additional coherence-breaking inverse length.",
            "equation": "G_K^2 >= 0",
            "status": "formal_hazard_term",
            "gap": "G_K is not yet parent-derived from Q, chi_D, J_rel, or curvature invariants",
        },
        {
            "step": 3,
            "claim": "If independent coherence-breaking rates add quadratically, the inverse length adds as a mass-squared sum.",
            "equation": "L_cg^-2 = L_H^-2 + alpha_K G_K^2",
            "status": "formal_inverse_mass_sum_derivation",
            "gap": "the quadratic addition is a plausible EFT/action form, not a derived Ward identity",
        },
        {
            "step": 4,
            "claim": "The homogeneous FLRW limit conditionally locks the scale.",
            "equation": "G_K=0 -> L_cg=L_H=c/H and eta=H0 L_cg/c=1 today",
            "status": "conditional_pass",
            "gap": "does not predict B_mem; only removes eta as a free fit knob in FLRW",
        },
        {
            "step": 5,
            "claim": "Local or transition domains can be suppressed by large G_K without changing the FLRW Hubble cap.",
            "equation": "G_K >> L_H^-1 -> L_cg ~= 1/(sqrt(alpha_K) G_K)",
            "status": "conditional_local_suppression_route",
            "gap": "the parent theory must define G_K and alpha_K before local/BAO scoring",
        },
        {
            "step": 6,
            "claim": "The parent theorem would require an action or Ward identity fixing the normalization.",
            "equation": "delta S_parent -> L_cg^-2 - L_H^-2 - alpha_K G_K^2 = 0",
            "status": "contract_not_derived",
            "gap": "no current source derives this Euler equation or fixes alpha_K",
        },
    ]


def action_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "constraint_multiplier",
            "schematic_term": "S_L = integral sqrt(-g) lambda_L (L_cg^-2 - L_H^-2 - alpha_K G_K^2)",
            "what_it_derives": "the algebraic L_cg rule if L_H, G_K, alpha_K are already owned",
            "status": "formal_contract_only",
            "failure_mode": "multiplier imposes the desired rule but does not derive G_K or alpha_K",
        },
        {
            "candidate": "positive_coherence_potential",
            "schematic_term": "V_L = mu_L^4 [L_cg^-2 - L_H^-2 - alpha_K G_K^2]^2",
            "what_it_derives": "stable extremum at the L_cg rule",
            "status": "formal_extremum",
            "failure_mode": "potential is engineered unless its square comes from a symmetry/current norm",
        },
        {
            "candidate": "Ward_identity_normalization",
            "schematic_term": "trace/coherent Ward identity fixes partial Gamma_eff/partial R = L_cg^-2",
            "what_it_derives": "normalization of L_cg^-2 in field equations",
            "status": "best_parent_route_missing",
            "failure_mode": "checkpoint 96/97 already flagged the Ward identity as absent",
        },
        {
            "candidate": "relative_current_norm",
            "schematic_term": "||J_rel||_D^2 supplies G_K^2 and domain class penalty",
            "what_it_derives": "links scale to topological/coherent boundary data",
            "status": "candidate_missing_representative",
            "failure_mode": "physical J_rel representative not derived",
        },
        {
            "candidate": "external_empirical_domain_length",
            "schematic_term": "set L_cg to whatever BAO/local tests prefer",
            "what_it_derives": "nothing",
            "status": "rejected",
            "failure_mode": "data-tuned rescue knob",
        },
    ]


def branch_limit_rows() -> list[dict[str, Any]]:
    cases = [
        ("homogeneous_FLRW", 0.0, "G_K=0 by symmetry; Hubble cap active"),
        ("very_smooth_late_BAO_domain", 1.0 / 10_000.0, "coherence length longer than Hubble; near-FLRW"),
        ("Gpc_gradient_domain", 1.0 / 1_000.0, "sharp enough to pressure BAO if endpoint memory varies across it"),
        ("BAO_scale_gradient_domain", 1.0 / 150.0, "BAO-sized inhomogeneity/transition scale"),
        ("galactic_1Mpc_environment", 1.0, "local/cosmic environment scale"),
        ("local_high_gradient_limit", 1000.0, "formal local suppression limit"),
    ]
    rows: list[dict[str, Any]] = []
    for case, g_k, meaning in cases:
        scale = L_cg(1.0, g_k)
        rows.append(
            {
                "case": case,
                "alpha_K": 1.0,
                "G_K_per_Mpc": g_k,
                "L_cg_Mpc": scale,
                "L_cg_over_Hubble": scale / HUBBLE_RADIUS_MPC,
                "eta_today_if_used_as_FLRW_scale": H0_KM_S_MPC * scale / LIGHT_SPEED_KM_S,
                "meaning": meaning,
                "status": "branch_limit_check",
            }
        )
    return rows


def bao_safety_rows() -> list[dict[str, Any]]:
    bao_bound_row = next(
        row
        for row in read_csv_rows(CHECKPOINT_205_RUN / "results" / "BAO_spatial_gradient_bounds.csv")
        if row["delta_chi2_threshold"] == "1.0" and row["coherence_length_Mpc"] == "150.0"
    )
    max_delta_c = float(bao_bound_row["max_abs_delta_C_across_length"])
    candidates = [
        ("FLRW_Hubble_cap", HUBBLE_RADIUS_MPC),
        ("two_Hubble_cap", 2.0 * HUBBLE_RADIUS_MPC),
        ("one_Gpc_domain", 1000.0),
        ("five_hundred_Mpc_domain", 500.0),
        ("BAO_150Mpc_domain", 150.0),
    ]
    rows: list[dict[str, Any]] = []
    for name, length in candidates:
        delta_c_across_150 = LOCKED_B_MEM * 150.0 / length
        half_shift = 0.5 * delta_c_across_150
        rows.append(
            {
                "candidate_domain": name,
                "domain_length_Mpc": length,
                "DeltaC_across_150Mpc_if_full_B_spread_linearly": delta_c_across_150,
                "half_DeltaC_ratio_shift": half_shift,
                "max_allowed_DeltaC_chi2_lt1": max_delta_c,
                "safe_vs_BAO_spatial_chi2_lt1": "yes" if delta_c_across_150 < max_delta_c else "no",
                "interpretation": "Hubble-cap is safe; smaller ad-hoc scales can become BAO-pressure",
            }
        )
    return rows


def closure_demotion_scorecard_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement": "FLRW eta=1",
            "current_evidence": "G_K=0 gives L_cg=c/H and eta=1",
            "verdict": "conditional_pass",
            "allowed_claim": "eta is conditionally fixed in homogeneous FLRW if the rule is accepted",
        },
        {
            "requirement": "no BAO data tuning",
            "current_evidence": "Hubble-cap scale is predeclared and independent of BAO 150 Mpc",
            "verdict": "conditional_pass",
            "allowed_claim": "BAO can be tested as subdomain of the predeclared cap",
        },
        {
            "requirement": "parent derivation of G_K",
            "current_evidence": "no current action defines the coherence-breaking invariant",
            "verdict": "fail",
            "allowed_claim": "G_K is a theorem target, not derived",
        },
        {
            "requirement": "parent derivation/fixing of alpha_K",
            "current_evidence": "alpha_K is not fixed by Ward identity, normalization, or boundary charge",
            "verdict": "fail",
            "allowed_claim": "alpha_K must not become a rescue knob",
        },
        {
            "requirement": "Euler equation for L_cg",
            "current_evidence": "can be imposed by multiplier or potential but not derived from existing parent action",
            "verdict": "fail",
            "allowed_claim": "formal action contract only",
        },
        {
            "requirement": "theory promotion",
            "current_evidence": CLAIM_CEILING,
            "verdict": "fail",
            "allowed_claim": "no local-GR/BAO promotion",
        },
    ]


def forbidden_shortcut_rows() -> list[dict[str, Any]]:
    return [
        {
            "shortcut": "choose L_cg from BAO residuals",
            "why_forbidden": "turns the domain scale into a fit rescue knob",
            "allowed_replacement": "predeclare L_cg from parent variables before scoring",
        },
        {
            "shortcut": "call the inverse-sum rule derived because it is natural",
            "why_forbidden": "natural EFT structure is not a parent theorem",
            "allowed_replacement": "label it formal inverse-coherence contract until G_K and alpha_K are derived",
        },
        {
            "shortcut": "hide alpha_K as order-one",
            "why_forbidden": "order-one constants still need normalization if they affect domain selection",
            "allowed_replacement": "derive alpha_K from Ward identity, current norm, or set a predeclared fixed value as closure",
        },
        {
            "shortcut": "use eta=1 to claim B_mem prediction",
            "why_forbidden": "eta=1 only removes one factor; a_F DeltaR and amplitude remain open",
            "allowed_replacement": "state eta lock as conditional narrowing only",
        },
        {
            "shortcut": "reuse local C_coh as derived local GR route",
            "why_forbidden": "earlier checkpoints demoted that parent-action route",
            "allowed_replacement": "keep local branch screened/conditional until full parent derivation exists",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal scale audit",
        },
        {
            "gate": "inverse-coherence rule formalized",
            "status": "pass",
            "evidence": "L_cg^-2=L_H^-2+alpha_K G_K^2 as positive inverse-length sum",
            "claim_allowed": "formal contract",
        },
        {
            "gate": "FLRW Hubble-cap limit recovered",
            "status": "conditional_pass",
            "evidence": "G_K=0 -> L_cg=L_H and eta=1",
            "claim_allowed": "conditional branch result",
        },
        {
            "gate": "BAO subdomain safety checked",
            "status": "conditional_pass",
            "evidence": "Hubble-cap spread of B_mem across 150 Mpc is below checkpoint 205 bound",
            "claim_allowed": "conditional consistency",
        },
        {
            "gate": "G_K parent-derived",
            "status": "fail",
            "evidence": "no parent invariant/equation fixes G_K",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "alpha_K parent-normalized",
            "status": "fail",
            "evidence": "no Ward/current normalization fixes alpha_K",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "L_cg promoted as theorem",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The L_cg rule has a clean formal interpretation as an inverse-coherence length: independent positive coherence-breaking rates add in L^-2, giving L_cg^-2=L_H^-2+alpha_K G_K^2. This conditionally recovers the FLRW Hubble cap and keeps the BAO Hubble-domain route predeclared. But G_K, alpha_K, and the Euler/Ward identity that would make this a parent theorem are missing.",
            "main_gain": "L_cg is now a formal inverse-coherence contract, not an arbitrary BAO-selected length",
            "demotion": "not parent-derived; retain as closure/theorem target",
            "main_blocker": "derive G_K and alpha_K normalization from parent action or Ward/current identity",
            "next_target": "210-GK-alphaK-parent-invariant-or-fixed-closure.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_209_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    chain_rows = derivation_chain_rows()
    action_rows = action_contract_rows()
    limit_rows = branch_limit_rows()
    bao_rows = bao_safety_rows()
    scorecard_rows = closure_demotion_scorecard_rows()
    forbidden_rows = forbidden_shortcut_rows()
    gates = claim_gate_rows(source_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "Lcg_derivation_chain.csv": (
            chain_rows,
            ["step", "claim", "equation", "status", "gap"],
        ),
        "action_contract_options.csv": (
            action_rows,
            ["candidate", "schematic_term", "what_it_derives", "status", "failure_mode"],
        ),
        "branch_limit_table.csv": (
            limit_rows,
            ["case", "alpha_K", "G_K_per_Mpc", "L_cg_Mpc", "L_cg_over_Hubble", "eta_today_if_used_as_FLRW_scale", "meaning", "status"],
        ),
        "BAO_Hubble_domain_safety.csv": (
            bao_rows,
            [
                "candidate_domain",
                "domain_length_Mpc",
                "DeltaC_across_150Mpc_if_full_B_spread_linearly",
                "half_DeltaC_ratio_shift",
                "max_allowed_DeltaC_chi2_lt1",
                "safe_vs_BAO_spatial_chi2_lt1",
                "interpretation",
            ],
        ),
        "closure_vs_derivation_scorecard.csv": (
            scorecard_rows,
            ["requirement", "current_evidence", "verdict", "allowed_claim"],
        ),
        "forbidden_shortcuts.csv": (
            forbidden_rows,
            ["shortcut", "why_forbidden", "allowed_replacement"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            ["decision", "meaning", "main_gain", "demotion", "main_blocker", "next_target", "promotion_allowed", "claim_ceiling"],
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
        "inverse_coherence_rule_formalized": True,
        "FLRW_Hubble_cap_recovered_conditionally": True,
        "BAO_Hubble_domain_safety_checked": True,
        "G_K_parent_derived": False,
        "alpha_K_parent_normalized": False,
        "Lcg_theorem_promoted": False,
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
