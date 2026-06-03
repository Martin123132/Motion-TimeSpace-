from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "projected-matter-metric-parent-action-or-closure"
STATUS = "projected_matter_metric_parent_action_skeleton_conditional_nonlocal_selector_not_derived"
CLAIM_CEILING = "projected_matter_metric_parent_skeleton_internal_only_no_local_GR_or_unification_promotion"

B_MEM = 2.0 / 27.0
C_KM_S = 299_792.458
H0_KM_S_MPC = 67.51
L_D_MPC = C_KM_S / H0_KM_S_MPC
LOCAL_DELTA_C_GATE = 4.6e-05
LOCAL_QR_GATE = 2.3e-05


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "204-matter-metric-action-and-ruler-transport-owner-contract.md", "matter metric and label-transport action"),
        (ROOT / "207-domain-projector-action-and-Bianchi-identity.md", "projector action and Bianchi accounting"),
        (ROOT / "208-domain-representative-selection-law.md", "domain representative selector"),
        (ROOT / "266-projected-trace-source-Ward-identity-attempt.md", "trace projection obstruction"),
        (ROOT / "267-projected-matter-metric-Cperp-decoupling-attempt.md", "projected matter metric decoupling"),
        (ROOT / "scripts" / "projected_matter_metric_parent_action_or_closure.py", "this parent-action skeleton gate"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": "yes" if path.exists() else "no",
        }
        for path, role in sources
    ]


def action_skeleton_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector": "metric_gravity",
            "term": "S_g[g] plus ordinary local GR terms",
            "variation_target": "g_munu",
            "derived_effect": "Einstein/EH local limit can be retained if extra stresses are controlled",
            "status": "background_contract",
        },
        {
            "sector": "memory_split",
            "term": "lambda_Pi (C - C_D - Cperp)",
            "variation_target": "lambda_Pi",
            "derived_effect": "C = C_D + Cperp",
            "status": "conditional_projector_skeleton",
        },
        {
            "sector": "domain_average",
            "term": "Lambda_D integral_D sqrt(h) W_D Cperp",
            "variation_target": "Lambda_D",
            "derived_effect": "P_D[Cperp] = 0",
            "status": "conditional_projector_skeleton",
        },
        {
            "sector": "matter_metric_selector",
            "term": "lambda_m (C_m - C_D)",
            "variation_target": "lambda_m",
            "derived_effect": "C_m = C_D = P_D C",
            "status": "new_conditional_skeleton",
        },
        {
            "sector": "auxiliary_matter_metric",
            "term": "Lambda_bar^{munu} (bar_g_munu - exp(C_m) g_munu)",
            "variation_target": "Lambda_bar^{munu}",
            "derived_effect": "bar_g_munu = exp(C_m) g_munu",
            "status": "new_conditional_skeleton",
        },
        {
            "sector": "universal_matter",
            "term": "S_matter[psi, bar_g_munu]",
            "variation_target": "psi and bar_g_munu",
            "derived_effect": "all late matter sees the same projected metric",
            "status": "contract_not_parent_derived",
        },
        {
            "sector": "domain_stress_bookkeeping",
            "term": "S_D[domain labels, W_D, boundaries, multipliers]",
            "variation_target": "domain labels and boundaries",
            "derived_effect": "retains projector/domain stress for Noether identity",
            "status": "required_not_complete",
        },
    ]


def variation_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "variation": "delta_Cperp S_matter",
            "ordinary_expC_metric": "1/2 (1-P_D)[sqrt(-tilde_g)T]",
            "projected_metric_skeleton": "0",
            "pass_condition": "matter metric depends on C_m=C_D only",
            "verdict": "conditional_pass",
        },
        {
            "variation": "delta_CD S_matter",
            "ordinary_expC_metric": "1/2 P_D[sqrt(-tilde_g)T]",
            "projected_metric_skeleton": "1/2 P_D[sqrt(-bar_g)T_bar]",
            "pass_condition": "domain average source is volume-suppressed for compact support",
            "verdict": "conditional_pass",
        },
        {
            "variation": "delta_Cm S",
            "ordinary_expC_metric": "not present",
            "projected_metric_skeleton": "selector equation balances matter trace against lambda_m/Lambda_bar",
            "pass_condition": "selector stress retained",
            "verdict": "bookkeeping_required",
        },
        {
            "variation": "delta_bar_g S",
            "ordinary_expC_metric": "not present",
            "projected_metric_skeleton": "matter stress is defined in bar_g frame",
            "pass_condition": "universal matter coupling",
            "verdict": "conditional_pass",
        },
        {
            "variation": "delta_domain_labels S",
            "ordinary_expC_metric": "optional/absent",
            "projected_metric_skeleton": "domain boundary/projector stress equations",
            "pass_condition": "not frozen during metric variation",
            "verdict": "open",
        },
        {
            "variation": "diffeomorphism Noether identity",
            "ordinary_expC_metric": "standard if all local fields varied",
            "projected_metric_skeleton": "nabla_mu T_total^{mu nu}=0 only with projector/domain/boundary stresses",
            "pass_condition": "no dropped auxiliary stress",
            "verdict": "conditional_previous",
        },
        {
            "variation": "local matter equations",
            "ordinary_expC_metric": "tilde_nabla_mu T^{mu nu}=0 in exp(C)g",
            "projected_metric_skeleton": "bar_nabla_mu T_bar^{mu nu}=0 in exp(C_D)g",
            "pass_condition": "local experiments see constant C_D and no Cperp composition coupling",
            "verdict": "conditional_pass",
        },
    ]


def closure_risk_rows() -> list[dict[str, Any]]:
    return [
        {
            "risk": "nonlocal_matter_coupling",
            "why_it_matters": "S_matter depends on a domain projection, not a purely point-local field",
            "must_show": "P_D is an action-level physical zero mode or quotient/gauge representative",
            "status": "open",
        },
        {
            "risk": "equivalence_principle_composition",
            "why_it_matters": "different species cannot see different projectors or epsilon Cperp leaks",
            "must_show": "single universal bar_g_munu for all late matter",
            "status": "contract",
        },
        {
            "risk": "hidden_conservation_failure",
            "why_it_matters": "nonlocal/projector stress can fake conservation if omitted",
            "must_show": "retain T_matter + T_C + T_projector + T_domain + T_boundary",
            "status": "conditional_previous",
        },
        {
            "risk": "domain_scale_tuning",
            "why_it_matters": "L_D cannot be picked because BAO/local tests like it",
            "must_show": "derive L_D = L_cg or equivalent before empirical scoring",
            "status": "open",
        },
        {
            "risk": "local_microcausality",
            "why_it_matters": "matter responding to a domain zero mode can look acausal if C_D changes locally",
            "must_show": "C_D is a boundary/constraint zero mode, not a propagating instant signal",
            "status": "open",
        },
        {
            "risk": "late_drift",
            "why_it_matters": "projected metric removes Cperp source but not rolling C_D",
            "must_show": "late |dot_C_D/H| below BAO/radial bounds with endpoint memory retained",
            "status": "open",
        },
        {
            "risk": "amplitude_scale_lock",
            "why_it_matters": "B_mem=2/27 and Hstar=H0 remain closure/theorem targets",
            "must_show": "derive amplitude and scale-lock from parent boundary equations",
            "status": "not_derived",
        },
    ]


def theorem_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "action_can_encode_projected_matter_metric",
            "result": "conditional_pass",
            "evidence": "auxiliary C_m and bar_g constraints yield S_matter[psi, exp(C_D)g]",
            "claim_effect": "projected metric is at least action-writeable, not just prose",
        },
        {
            "gate": "Cperp_direct_matter_source",
            "result": "removed_conditionally",
            "evidence": "delta S_matter / delta Cperp = 0 in skeleton",
            "claim_effect": "local trace-source obstruction is moved to parent-origin question",
        },
        {
            "gate": "projected_metric_parent_principle",
            "result": "not_derived",
            "evidence": "skeleton chooses matter to see C_m=P_D C",
            "claim_effect": "not yet a theorem; could still be nonlocal closure",
        },
        {
            "gate": "Bianchi_accounting",
            "result": "conditional_pass",
            "evidence": "Noether safe only if all selector/projector/domain stresses are retained",
            "claim_effect": "no conservation claim unless stress ledger remains explicit",
        },
        {
            "gate": "local_equivalence_principle",
            "result": "conditional_pass",
            "evidence": "universal bar_g and constant C_D avoid composition-dependent local Cperp forces",
            "claim_effect": "local branch improved but not promoted",
        },
        {
            "gate": "domain_selector_and_scale",
            "result": "open",
            "evidence": "physical representative and L_D still imported from previous conditional ledgers",
            "claim_effect": "no empirical support claim",
        },
        {
            "gate": "late_drift_and_amplitude",
            "result": "open",
            "evidence": "no new derivation of saturation, B_mem=2/27, or Hstar=H0",
            "claim_effect": "cosmology bridge remains closure/theorem-target",
        },
        {
            "gate": "unification_promotion_allowed",
            "result": "no",
            "evidence": "projected metric is skeleton/contract, not parent-derived principle",
            "claim_effect": "no local-GR or unified-field promotion",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "A parent-action skeleton can encode the projected matter metric using auxiliary fields C_m and bar_g, "
                "and in that skeleton delta S_matter/delta Cperp is exactly zero. This is stronger than a hand plateau, "
                "but it is not yet a parent derivation because the principle selecting exp(P_D C)g as the universal matter metric is still missing."
            ),
            "next_target": "derive_metric_selector_principle_or_demote_projected_matter_metric_to_explicit_closure",
        }
    ]


def numeric_bounds_rows() -> list[dict[str, Any]]:
    return [
        {
            "quantity": "B_mem",
            "value": B_MEM,
            "meaning": "fixed closure/theorem target carried forward",
        },
        {
            "quantity": "L_D_Mpc",
            "value": L_D_MPC,
            "meaning": "Hubble-cap coherent domain scale used by current bounds",
        },
        {
            "quantity": "local_epsilon_from_DeltaC_gate",
            "value": LOCAL_DELTA_C_GATE / B_MEM,
            "meaning": "if projected metric leaks epsilon Cperp, local Delta C requires epsilon below this",
        },
        {
            "quantity": "local_epsilon_from_qR_gate",
            "value": LOCAL_QR_GATE / B_MEM,
            "meaning": "stricter qR-like local proxy for any residual Cperp matter coupling",
        },
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "action_skeleton.csv": (action_skeleton_rows(), ["sector", "term", "variation_target", "derived_effect", "status"]),
        "variation_audit.csv": (
            variation_audit_rows(),
            ["variation", "ordinary_expC_metric", "projected_metric_skeleton", "pass_condition", "verdict"],
        ),
        "closure_risks.csv": (closure_risk_rows(), ["risk", "why_it_matters", "must_show", "status"]),
        "theorem_gates.csv": (theorem_gate_rows(), ["gate", "result", "evidence", "claim_effect"]),
        "numeric_bounds.csv": (numeric_bounds_rows(), ["quantity", "value", "meaning"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status = decision_rows()[0]["decision"]
    payload = {
        "status": status,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "B_mem": B_MEM,
        "L_D_Mpc": L_D_MPC,
        "projected_metric_action_writeable": True,
        "delta_Smatter_delta_Cperp_zero_in_skeleton": True,
        "metric_selector_principle_derived": False,
        "projected_metric_promoted_to_parent_theorem": False,
        "local_GR_or_unification_claim_allowed": False,
        "next_target": "derive_metric_selector_principle_or_demote_projected_matter_metric_to_explicit_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(status + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Projected matter metric parent-action skeleton or closure gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
