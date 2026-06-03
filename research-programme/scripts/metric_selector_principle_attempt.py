from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "metric-selector-principle-attempt"
STATUS = "metric_selector_conditionally_derived_from_residual_gauge_redundancy_parent_gauge_principle_open"
CLAIM_CEILING = "metric_selector_internal_theorem_target_no_local_GR_or_unification_promotion"

B_MEM = 2.0 / 27.0
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
        (ROOT / "60-relative-cohomology-boundary-contract.md", "relative local-zero / FLRW-nonzero boundary contract"),
        (ROOT / "207-domain-projector-action-and-Bianchi-identity.md", "action-level projector and Bianchi accounting"),
        (ROOT / "208-domain-representative-selection-law.md", "representative selector law"),
        (ROOT / "231-Jrel-cohomology-projector-or-local-EH-limit.md", "cohomology projector precedent for local exactness"),
        (ROOT / "267-projected-matter-metric-Cperp-decoupling-attempt.md", "projected matter metric decoupling"),
        (ROOT / "268-projected-matter-metric-parent-action-or-closure.md", "projected matter metric parent-action skeleton"),
        (ROOT / "scripts" / "metric_selector_principle_attempt.py", "this selector principle attempt"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": "yes" if path.exists() else "no",
        }
        for path, role in sources
    ]


def selector_axiom_rows() -> list[dict[str, Any]]:
    return [
        {
            "axiom": "M1_residual_redundancy",
            "statement": "Cperp shifts by eta_perp with P_D eta_perp = 0 are gauge/representative changes, not matter observables",
            "status": "not_parent_derived",
            "why_needed": "without this, raw exp(C)g is the ordinary local metric and Cperp is physical",
        },
        {
            "axiom": "M2_universal_matter_metric",
            "statement": "all late matter species couple to one metric bar_g_munu in the conformal family",
            "status": "contract",
            "why_needed": "protects WEP/clocks/rulers from composition-dependent projector choices",
        },
        {
            "axiom": "M3_residual_gauge_invariance",
            "statement": "S_matter is invariant under Cperp -> Cperp + eta_perp",
            "status": "conditional_if_M1",
            "why_needed": "forbids matter dependence on the nonzero residual representative",
        },
        {
            "axiom": "M4_coherent_limit_recovery",
            "statement": "for Cperp=0, matter metric reduces to exp(C_D)g",
            "status": "required",
            "why_needed": "keeps the half-factor, BAO cancellation, and CMB endpoint bridge structure",
        },
        {
            "axiom": "M5_no_species_Weyl_compensation",
            "statement": "massive matter fields do not transform species-by-species to hide local Cperp dependence",
            "status": "required",
            "why_needed": "avoids fake invariance and composition dependence",
        },
        {
            "axiom": "M6_Bianchi_stress_retention",
            "statement": "projector, selector, domain, auxiliary, and boundary stresses remain in T_total",
            "status": "conditional_previous",
            "why_needed": "prevents an external nonlocal force from being hidden",
        },
    ]


def uniqueness_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "claim": "Let the matter metric be bar_g_munu = exp(F[C]) g_munu.",
            "condition": "universal conformal matter metric ansatz",
            "result": "reduces selector problem to finding gauge-invariant scalar F[C]",
        },
        {
            "step": 2,
            "claim": "Residual shift: C -> C + eta_perp, with P_D eta_perp = 0.",
            "condition": "M1 residual representative redundancy",
            "result": "P_D C is invariant, Cperp is not",
        },
        {
            "step": 3,
            "claim": "Matter invariance requires F[C + eta_perp] = F[C].",
            "condition": "M3 residual gauge invariance and no species-specific compensation",
            "result": "F cannot depend on Cperp",
        },
        {
            "step": 4,
            "claim": "Therefore F[C] = f(P_D C).",
            "condition": "P_D is the only retained scalar representative in this sector",
            "result": "matter metric must be projected",
        },
        {
            "step": 5,
            "claim": "Coherent limit requires f(C_D)=C_D.",
            "condition": "M4 coherent limit recovery",
            "result": "F[C]=P_D C=C_D",
        },
        {
            "step": 6,
            "claim": "Thus bar_g_munu = exp(P_D C) g_munu.",
            "condition": "M1-M6 all hold",
            "result": "projected matter metric is conditionally selected",
        },
        {
            "step": 7,
            "claim": "Then delta S_matter/delta Cperp = 0.",
            "condition": "matter depends only on P_D C",
            "result": "local trace-source obstruction is removed conditionally",
        },
    ]


def route_comparison_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "quotient_gauge_representative",
            "selector": "matter couples only to gauge-invariant quotient variable P_D C",
            "result": "conditional_best",
            "open_burden": "derive residual Cperp shift redundancy from parent action",
        },
        {
            "route": "relative_cohomology_class",
            "selector": "compact local Cperp is exact/trivial; C_D is the observable relative class",
            "result": "conditional_supporting_route",
            "open_burden": "prove matter observables depend only on the class and not local representative",
        },
        {
            "route": "boundary_clock_normalization",
            "selector": "matter clocks are normalized to domain boundary time carrying C_D",
            "result": "plausible_side_route",
            "open_burden": "derive boundary clock from parent canonical variables",
        },
        {
            "route": "ordinary_local_metric",
            "selector": "matter couples to exp(C)g",
            "result": "rejected_as_lead",
            "open_burden": "would require huge Cperp screening or epsilon below local bound",
        },
        {
            "route": "hard_projected_metric_closure",
            "selector": "impose exp(P_D C)g as an effective coupling",
            "result": "allowed_closure_if_labelled",
            "open_burden": "not a parent derivation; must be demoted if M1 is not derived",
        },
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "obstruction": "residual_gauge_principle_missing",
            "why_it_matters": "conditional uniqueness proof starts by assuming Cperp is not matter-observable",
            "status": "main_open_burden",
            "next_test": "derive Cperp shift as a first-class constraint or relative exact redundancy",
        },
        {
            "obstruction": "projector_parent_origin",
            "why_it_matters": "P_D cannot be an external average chosen after solving",
            "status": "open",
            "next_test": "close action-level domain/projector algebra with retained stresses",
        },
        {
            "obstruction": "domain_scale_selector",
            "why_it_matters": "the quotient domain cannot be tuned to local/BAO tests",
            "status": "open",
            "next_test": "derive L_D or L_cg rule from parent domain variables",
        },
        {
            "obstruction": "local_microcausality",
            "why_it_matters": "domain zero mode must not act as an instantaneous propagating signal",
            "status": "open",
            "next_test": "show C_D is a boundary/constraint datum rather than a retarded local field",
        },
        {
            "obstruction": "late_drift_saturation",
            "why_it_matters": "selector does not derive |dot_C_D/H| safety",
            "status": "open",
            "next_test": "derive saturation or residual drift law",
        },
        {
            "obstruction": "amplitude_scale_lock",
            "why_it_matters": "B_mem=2/27 and Hstar=H0 remain closure/theorem targets",
            "status": "not_derived",
            "next_test": "boundary/noether amplitude theorem still required",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "conditional_selector_uniqueness",
            "result": "pass_if_M1_M6",
            "evidence": "residual gauge invariance plus coherent limit selects F[C]=P_D C",
            "claim_effect": "metric selector has a real conditional theorem form",
        },
        {
            "gate": "residual_gauge_principle",
            "result": "not_derived",
            "evidence": "Cperp shift redundancy is assumed, not parent-owned",
            "claim_effect": "no promotion; theorem target only",
        },
        {
            "gate": "cohomology_support",
            "result": "partial",
            "evidence": "previous relative-class ledgers support local exact / FLRW nonzero split as contract",
            "claim_effect": "helps justify route but does not prove matter selector",
        },
        {
            "gate": "ordinary_local_metric",
            "result": "rejected_as_lead",
            "evidence": "breaks residual gauge invariance and sources Cperp",
            "claim_effect": "do not return to exp(C)g as local lead branch",
        },
        {
            "gate": "epsilon_leak_tolerance",
            "result": "strict",
            "evidence": f"local epsilon max = {LOCAL_QR_GATE / B_MEM}",
            "claim_effect": "any residual Cperp matter coupling must be almost zero",
        },
        {
            "gate": "support_claim_allowed",
            "result": "no",
            "evidence": "residual gauge principle, domain scale, drift, and amplitude remain open",
            "claim_effect": "no local-GR or unification promotion",
        },
    ]


def numeric_rows() -> list[dict[str, Any]]:
    return [
        {
            "quantity": "B_mem",
            "value": B_MEM,
            "meaning": "fixed closure/theorem target carried forward",
        },
        {
            "quantity": "epsilon_local_DeltaC_max",
            "value": LOCAL_DELTA_C_GATE / B_MEM,
            "meaning": "residual matter coupling fraction allowed by local Delta C gate",
        },
        {
            "quantity": "epsilon_local_qR_max",
            "value": LOCAL_QR_GATE / B_MEM,
            "meaning": "stricter qR-like allowed residual coupling fraction",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The projected matter metric is conditionally derivable from a clean selector principle: "
                "if Cperp is a residual gauge/exact representative and matter must be invariant under residual shifts, "
                "then the unique coherent-limit conformal metric is exp(P_D C)g. The remaining open burden is deriving "
                "that residual gauge/cohomology principle from the parent action rather than assuming it."
            ),
            "next_target": "derive_Cperp_residual_shift_first_class_constraint_or_demote_metric_selector_to_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "selector_axioms.csv": (selector_axiom_rows(), ["axiom", "statement", "status", "why_needed"]),
        "conditional_uniqueness_proof.csv": (uniqueness_proof_rows(), ["step", "claim", "condition", "result"]),
        "route_comparison.csv": (route_comparison_rows(), ["route", "selector", "result", "open_burden"]),
        "obstruction_ledger.csv": (obstruction_rows(), ["obstruction", "why_it_matters", "status", "next_test"]),
        "gate_results.csv": (gate_rows(), ["gate", "result", "evidence", "claim_effect"]),
        "numeric_bounds.csv": (numeric_rows(), ["quantity", "value", "meaning"]),
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
        "conditional_selector_uniqueness_derived": True,
        "residual_gauge_principle_parent_derived": False,
        "projected_metric_parent_promoted": False,
        "ordinary_expC_metric_rejected_as_lead": True,
        "local_GR_or_unification_claim_allowed": False,
        "next_target": "derive_Cperp_residual_shift_first_class_constraint_or_demote_metric_selector_to_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(status + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Metric selector principle attempt for projected matter metric.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
