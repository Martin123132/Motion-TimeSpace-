#!/usr/bin/env python3
"""Checkpoint 221: source identity derivation route or compact PPN closure map."""

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

CHECKPOINT_221_NAME = "Noether-source-identity-or-compact-PPN-closure-map"
CHECKPOINT_220_RUN = RUNS_ROOT / "20260601-000037-Jrel-local-trivial-representative-or-closure-bound"

STATUS = "source_identity_parent_displacement_route_written_not_derived_PPN_closure_map_retained"
CLAIM_CEILING = "conditional_source_identity_contract_no_local_GR_or_PPN_promotion"
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
        (Path(__file__).resolve(), "checkpoint 221 source identity / PPN closure script"),
        (WORK_DIR / "19-constrained-parent-action-skeleton.md", "early constrained parent-action skeleton"),
        (WORK_DIR / "177-parent-action-perturbation-local-GR-contract.md", "parent action and local-GR contract"),
        (WORK_DIR / "179-local-GR-PPN-silence-contract.md", "local PPN silence contract and residual vector"),
        (WORK_DIR / "207-domain-projector-action-and-Bianchi-identity.md", "Bianchi/projector stress accounting"),
        (WORK_DIR / "219-compact-shell-q_loc-source-projection-attempt.md", "q_loc source projection target"),
        (WORK_DIR / "220-Jrel-local-trivial-representative-or-closure-bound.md", "J_rel exactness/local closure checkpoint"),
        (CHECKPOINT_220_RUN / "status.json", "checkpoint 220 machine status"),
        (CHECKPOINT_220_RUN / "results" / "Jrel_closure_bound_table.csv", "compact J_rel leakage bounds"),
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


def parent_variation_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "V0_parent_response_field",
            "required_structure": "introduce a genuine parent response/embedding field X^nu whose variation is physical or constrained, not a decorative multiplier",
            "mathematical_role": "delta_X S_parent supplies the local source identity",
            "status": "candidate_route_written",
            "failure_mode": "without X^nu or an equivalent field, nabla K - nabla Gamma is only an assumed identity",
        },
        {
            "clause": "V1_conjugate_Khat",
            "required_structure": "delta L_X contains Khat^{mu nu} nabla_mu delta X_nu",
            "mathematical_role": "defines Khat as the conjugate to local response gradients",
            "status": "contract",
            "failure_mode": "Khat remains a named tensor with no variational owner",
        },
        {
            "clause": "V2_conjugate_Gamma",
            "required_structure": "delta L_X contains -Gamma_eff nabla_nu delta X^nu",
            "mathematical_role": "defines Gamma_eff as the conjugate scalar trace/divergence response",
            "status": "contract",
            "failure_mode": "Gamma_eff can be tuned independently of Khat",
        },
        {
            "clause": "V3_source_coupling",
            "required_structure": "delta L_source contains +(S_L^nu + d_rel J_rel^nu) delta X_nu",
            "mathematical_role": "identifies load support and relative memory exchange as the only local source terms",
            "status": "contract",
            "failure_mode": "extra hidden sources can fake or spoil local silence",
        },
        {
            "clause": "V4_boundary_accounting",
            "required_structure": "n_mu(Khat^{mu nu}-Gamma_eff g^{mu nu}) delta X_nu is cancelled, fixed, or carried by explicit relative boundary terms",
            "mathematical_role": "prevents the source identity from leaking an untracked surface force",
            "status": "not_derived",
            "failure_mode": "boundary leakage reappears as PPN-scale q_loc^nu",
        },
        {
            "clause": "V5_metric_stress_retained",
            "required_structure": "metric variation retains T_X, T_source, T_rel, T_projector, and T_boundary",
            "mathematical_role": "Bianchi conservation belongs to the full action, not a truncated field equation",
            "status": "contract",
            "failure_mode": "dropping auxiliary stress hides an external force",
        },
        {
            "clause": "V6_nonpropagating_or_screened_X",
            "required_structure": "X^nu must be constrained, gauge, auxiliary, high-mass, or otherwise locally non-hairy",
            "mathematical_role": "avoids adding a new PPN vector/fifth-force degree of freedom",
            "status": "not_derived",
            "failure_mode": "the cure for q_loc becomes a new local PPN problem",
        },
    ]


def derivation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Assume a parent sector whose X^nu variation has delta S_X = integral sqrt(-g)[Khat^{mu nu} nabla_mu delta X_nu - Gamma_eff nabla_nu delta X^nu + (S_L^nu+d_rel J_rel^nu) delta X_nu] plus boundary.",
            "result": "candidate_parent_variation",
            "gap": "the present corpus has not yet supplied this X^nu sector",
        },
        {
            "step": 2,
            "statement": "Integrate by parts in the bulk.",
            "result": "delta S_X = integral sqrt(-g)[-nabla_mu Khat^{mu nu}+nabla^nu Gamma_eff+S_L^nu+d_rel J_rel^nu] delta X_nu plus boundary",
            "gap": "",
        },
        {
            "step": 3,
            "statement": "Demand the boundary term is fixed, cancelled, or explicitly carried by the relative boundary current.",
            "result": "boundary_safe_Euler_equation_conditional",
            "gap": "boundary primitive selection not derived",
        },
        {
            "step": 4,
            "statement": "Set the X^nu Euler equation to zero.",
            "result": "nabla_mu Khat^{mu nu}-nabla^nu Gamma_eff = S_L^nu + d_rel J_rel^nu",
            "gap": "identity derived only inside this candidate action class",
        },
        {
            "step": 5,
            "statement": "In a compact vacuum collar S_L^nu=0 and, if checkpoint 220 exactness holds, P_loc d_rel J_rel^nu=0.",
            "result": "conditional q_loc^nu=0",
            "gap": "exact J_rel representative and pointwise projector annihilation not derived",
        },
        {
            "step": 6,
            "statement": "Without those parent clauses, retain an explicit compact PPN closure vector.",
            "result": "PPN_closure_map_required",
            "gap": "local GR not promoted",
        },
    ]


def boundary_and_bianchi_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "bulk_Euler_identity",
            "requirement": "the source identity must come from delta_X S_parent, not from imposing q_loc=0 after solving",
            "status": "candidate_written_not_owned",
            "risk_if_missing": "local silence is a rescue equation",
        },
        {
            "item": "X_boundary_term",
            "requirement": "n_mu(Khat^{mu nu}-Gamma_eff g^{mu nu}) delta X_nu must vanish, be fixed, or be matched by b_2/A_rel",
            "status": "not_derived",
            "risk_if_missing": "surface leakage acts like an unmodelled local force",
        },
        {
            "item": "relative_current_boundary",
            "requirement": "J_rel boundary primitive must be exact/pure gauge in compact shells",
            "status": "not_derived",
            "risk_if_missing": "closed non-exact memory charge survives",
        },
        {
            "item": "total_metric_stress",
            "requirement": "retain T_X + T_source + T_rel + T_projector + T_boundary in delta_g S",
            "status": "contract",
            "risk_if_missing": "Bianchi identity is faked by dropping auxiliary stress",
        },
        {
            "item": "local_degree_count",
            "requirement": "X^nu must not introduce unscreened vector/scalar local hair",
            "status": "not_derived",
            "risk_if_missing": "PPN gamma/beta/slip can fail even if q_loc algebra closes",
        },
    ]


def compact_ppn_closure_rows() -> list[dict[str, Any]]:
    source_bounds = read_csv_rows(CHECKPOINT_220_RUN / "results" / "Jrel_closure_bound_table.csv")
    residual_components = [
        (
            "q_loc_source",
            "q_proxy_before_Jrel_leakage + epsilon_J",
            "direct q-like source gate; coefficient fixed to one by the closure definition",
            "bounded_if_epsilon_J_below_case_budget",
        ),
        (
            "gamma_minus_1",
            "c_gamma epsilon_J + higher_order_terms",
            "response coefficient c_gamma not parent-derived",
            "closure_only",
        ),
        (
            "beta_minus_1",
            "c_beta epsilon_J + higher_order_terms",
            "response coefficient c_beta not parent-derived",
            "closure_only",
        ),
        (
            "Phi_minus_Psi",
            "c_slip epsilon_J + anisotropic_boundary_terms",
            "slip coefficient and boundary anisotropic stress not parent-derived",
            "closure_only",
        ),
        (
            "G_eff_over_G_minus_1",
            "c_G epsilon_J + source_renormalization_terms",
            "effective coupling response not parent-derived",
            "closure_only",
        ),
        (
            "alpha_clock",
            "c_clock epsilon_J + matter_clock_coupling_terms",
            "clock coupling must remain universal/minimal",
            "closure_only",
        ),
        (
            "epsilon_matter",
            "c_matter epsilon_J + nonuniversal_matter_coupling_terms",
            "composition dependence forbidden but not parent-derived",
            "closure_only",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for bound in source_bounds:
        q_gate = float(bound["q_R_like_gate"])
        base_proxy = float(bound["q_proxy_before_Jrel_leakage"])
        epsilon_budget = float(bound["max_allowed_abs_Ploc_drel_Jrel_leakage"])
        for component, model_form, caveat, status in residual_components:
            if component == "q_loc_source":
                unit_response_total = base_proxy + epsilon_budget
                unit_response_ratio = unit_response_total / q_gate
                max_unit_coefficient_before_q_gate = 1.0
            else:
                unit_response_total = epsilon_budget
                unit_response_ratio = epsilon_budget / q_gate
                max_unit_coefficient_before_q_gate = q_gate / epsilon_budget if epsilon_budget > 0 else 0.0
            rows.append(
                {
                    "case": bound["case"],
                    "use_in_gate": bound["use_in_gate"],
                    "residual_component": component,
                    "closure_model_form": model_form,
                    "q_like_gate": q_gate,
                    "base_q_proxy": base_proxy,
                    "max_allowed_epsilon_J": epsilon_budget,
                    "unit_response_value_at_bound": unit_response_total,
                    "unit_response_ratio_to_q_gate": unit_response_ratio,
                    "max_unit_coefficient_before_q_gate_proxy": max_unit_coefficient_before_q_gate,
                    "coefficient_status": caveat,
                    "status": status,
                }
            )
    return rows


def claim_gate_rows(
    source_rows: list[dict[str, Any]],
    ppn_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = sum(source["exists"] != "yes" for source in source_rows)
    compact_q_rows = [
        row
        for row in ppn_rows
        if row["use_in_gate"] == "yes" and row["residual_component"] == "q_loc_source"
    ]
    compact_q_failures = sum(float(row["unit_response_ratio_to_q_gate"]) > 1.0 + 1e-12 for row in compact_q_rows)
    worst_compact_epsilon = min(float(row["max_allowed_epsilon_J"]) for row in compact_q_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "source identity derivation route written",
            "status": "conditional_pass",
            "evidence": "delta_X parent variation yields nabla K - nabla Gamma = S_L + d_rel J_rel if X-sector exists",
            "claim_allowed": "candidate action-class contract",
        },
        {
            "gate": "source identity derived in current parent theory",
            "status": "fail",
            "evidence": "X^nu sector, constitutive L_X, boundary primitive, and local degree count are not owned",
            "claim_allowed": "no theorem",
        },
        {
            "gate": "boundary leakage removed",
            "status": "fail",
            "evidence": "boundary term and compact A_rel primitive are not parent-selected",
            "claim_allowed": "no local-GR promotion",
        },
        {
            "gate": "Bianchi-safe stress accounting stated",
            "status": "conditional_pass",
            "evidence": "must retain T_X, T_source, T_rel, T_projector, and T_boundary",
            "claim_allowed": "contract",
        },
        {
            "gate": "new local vector/scalar hair excluded",
            "status": "fail",
            "evidence": "X^nu nonpropagating/screened/gauge nature not derived",
            "claim_allowed": "no PPN promotion",
        },
        {
            "gate": "compact q-like closure map positive",
            "status": "pass" if compact_q_failures == 0 else "fail",
            "evidence": f"compact_q_failures={compact_q_failures}; worst_compact_epsilon_J_budget={worst_compact_epsilon}",
            "claim_allowed": "bounded closure only",
        },
        {
            "gate": "gamma beta slip G_eff clock matter residuals derived",
            "status": "fail",
            "evidence": "response coefficients c_gamma,c_beta,c_slip,c_G,c_clock,c_matter are placeholders",
            "claim_allowed": "closure vector only",
        },
        {
            "gate": "local GR or PPN promoted",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(worst_compact_epsilon: float) -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "A clean parent-variation route exists in principle: introduce a genuine response/embedding field X^nu whose variation defines Khat and Gamma_eff as conjugates and sources only S_L plus d_rel J_rel. That would derive the desired source identity inside this action class. The current corpus does not yet own the X-sector, boundary primitive, local degree count, or PPN response coefficients, so this remains a contract plus explicit compact PPN closure map.",
            "main_gain": "the source identity is no longer a naked assumption; it has an exact parent-variation template",
            "main_failure": "the required parent X-sector and boundary/degree-count clauses are not derived",
            "worst_compact_epsilon_J_budget": worst_compact_epsilon,
            "next_target": "222-parent-X-sector-degree-count-and-boundary-action.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_221_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    variation_rows = parent_variation_contract_rows()
    derivation_rows = derivation_chain_rows()
    bianchi_rows = boundary_and_bianchi_rows()
    ppn_rows = compact_ppn_closure_rows()
    gates = claim_gate_rows(source_rows, ppn_rows)
    compact_q_rows = [
        row
        for row in ppn_rows
        if row["use_in_gate"] == "yes" and row["residual_component"] == "q_loc_source"
    ]
    worst_compact_epsilon = min(float(row["max_allowed_epsilon_J"]) for row in compact_q_rows)
    decision = decision_rows(worst_compact_epsilon)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "parent_variation_contract.csv": (
            variation_rows,
            ["clause", "required_structure", "mathematical_role", "status", "failure_mode"],
        ),
        "derivation_chain.csv": (
            derivation_rows,
            ["step", "statement", "result", "gap"],
        ),
        "boundary_and_Bianchi_accounting.csv": (
            bianchi_rows,
            ["item", "requirement", "status", "risk_if_missing"],
        ),
        "compact_PPN_closure_vector.csv": (
            ppn_rows,
            [
                "case",
                "use_in_gate",
                "residual_component",
                "closure_model_form",
                "q_like_gate",
                "base_q_proxy",
                "max_allowed_epsilon_J",
                "unit_response_value_at_bound",
                "unit_response_ratio_to_q_gate",
                "max_unit_coefficient_before_q_gate_proxy",
                "coefficient_status",
                "status",
            ],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "main_gain",
                "main_failure",
                "worst_compact_epsilon_J_budget",
                "next_target",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, file_data in files.items():
        rows, fieldnames = file_data
        write_csv(results_dir / filename, rows, fieldnames)

    missing_sources = sum(source["exists"] != "yes" for source in source_rows)
    compact_q_failures = sum(float(row["unit_response_ratio_to_q_gate"]) > 1.0 + 1e-12 for row in compact_q_rows)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "source_identity_route_written": True,
        "source_identity_derived_in_current_parent": False,
        "parent_X_sector_owned": False,
        "boundary_primitive_owned": False,
        "local_degree_count_safe": False,
        "Bianchi_stress_accounting_stated": True,
        "compact_q_like_closure_failures": compact_q_failures,
        "worst_compact_epsilon_J_budget": worst_compact_epsilon,
        "PPN_response_coefficients_derived": False,
        "q_loc_pointwise_zero_promoted": False,
        "PPN_promoted": False,
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
