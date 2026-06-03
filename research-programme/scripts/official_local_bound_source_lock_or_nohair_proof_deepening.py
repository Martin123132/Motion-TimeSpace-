from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "official-local-bound-source-lock-or-nohair-proof-deepening"
STATUS = "local_bound_source_lock_partial_gamma_beta_WEP_redshift_locked_nohair_deepened_no_local_GR_promotion"
CLAIM_CEILING = "source_locked_targets_for_internal_runner_only_no_official_PPN_or_local_GR_pass_claim"
NEXT_TARGET = "355-source-locked-local-bound-runner-with-open-sector-quarantine.md"


SOURCE_DOCS = [
    (
        "179-local-GR-PPN-silence-contract.md",
        "earlier screened local PPN proxy; explicitly not a derivation",
    ),
    (
        "250-local-GR-gate-scorecard-and-test-readiness.md",
        "local GR gate scorecard and proxy/official distinction",
    ),
    (
        "348-N5-projector-stress-conservation-theorem.md",
        "conditional quotient/topological P_D local bulk silence",
    ),
    (
        "352-boundary-nohair-and-PPN-residual-vector-gate.md",
        "symbolic PPN residual vector and boundary residual decomposition",
    ),
    (
        "353-boundary-nohair-theorem-attempt-or-PPN-bound-runner.md",
        "proxy bound runner and no-hair contract A1-A7",
    ),
]


EXTERNAL_SOURCES = [
    {
        "source_id": "will_living_reviews_2014",
        "title": "The Confrontation between General Relativity and Experiment",
        "url": "https://link.springer.com/article/10.12942/lrr-2014-4",
        "use": "solar-system PPN gamma/beta, Nordtvedt, preferred-frame sector definitions",
        "source_status": "review_source_locked_for_internal_targets",
    },
    {
        "source_id": "pdg_gravity_tests_2018",
        "title": "PDG 2018 Experimental Tests of Gravitational Theory",
        "url": "https://pdg.lbl.gov/2018/reviews/rpp2018-rev-gravity-tests.pdf",
        "use": "compact cross-check of gamma, beta, WEP, redshift, and metric-coupling statements",
        "source_status": "review_source_locked_for_internal_targets",
    },
    {
        "source_id": "microscope_final_2022",
        "title": "MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36179190/",
        "use": "final Ti-Pt WEP/Eotvos parameter scale",
        "source_status": "primary_source_locked",
    },
    {
        "source_id": "galileo_redshift_2018",
        "title": "Test of the Gravitational Redshift with Galileo Satellites in an Eccentric Orbit",
        "url": "https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.121.231102/fulltext",
        "use": "clock/redshift violation parameter scale",
        "source_status": "primary_source_locked",
    },
]


BOUND_TARGETS = [
    {
        "residual": "gamma_minus_1",
        "source_locked_scale_abs": 2.3e-5,
        "confidence_note": "Cassini one-sigma scale for gamma-1; use as internal target, not public pass threshold",
        "source_id": "will_living_reviews_2014; pdg_gravity_tests_2018",
        "MTS_mapping": "epsilon_TF + epsilon_rad + epsilon_bulk contributes to gamma residual",
        "runner_status": "source_locked_ready",
    },
    {
        "residual": "beta_minus_1",
        "source_locked_scale_abs": 7.8e-5,
        "confidence_note": "Mercury/Messenger beta-1 one-sigma scale from Will review; PDG gives comparable 7e-5 summary",
        "source_id": "will_living_reviews_2014; pdg_gravity_tests_2018",
        "MTS_mapping": "epsilon_rad + epsilon_nonlinear_boundary contributes to beta residual",
        "runner_status": "source_locked_ready",
    },
    {
        "residual": "eta_WEP",
        "source_locked_scale_abs": 2.8e-15,
        "confidence_note": "MICROSCOPE Ti-Pt combined one-sigma scale from stat/syst quadrature, rounded",
        "source_id": "microscope_final_2022",
        "MTS_mapping": "epsilon_WEP or composition-dependent MTS charge",
        "runner_status": "source_locked_ready",
    },
    {
        "residual": "alpha_clock_redshift",
        "source_locked_scale_abs": 3.1e-5,
        "confidence_note": "Galileo redshift-only alpha_rs one-sigma uncertainty; use for clock redshift residual only",
        "source_id": "galileo_redshift_2018",
        "MTS_mapping": "epsilon_clock / nonmetric clock coupling",
        "runner_status": "source_locked_ready",
    },
    {
        "residual": "preferred_frame_alpha1_alpha2",
        "source_locked_scale_abs": "",
        "confidence_note": "Will review identifies alpha1/alpha2 preferred-frame sector; numeric bound not ingested in this pass",
        "source_id": "will_living_reviews_2014",
        "MTS_mapping": "epsilon_vec / local preferred frame",
        "runner_status": "quarantined_until_numeric_source_lock",
    },
    {
        "residual": "xi_preferred_location_anisotropy",
        "source_locked_scale_abs": "",
        "confidence_note": "Will review identifies xi/preferred-location sector; numeric bound not ingested in this pass",
        "source_id": "will_living_reviews_2014",
        "MTS_mapping": "epsilon_TF,l>=2 and external-domain anisotropy",
        "runner_status": "quarantined_until_numeric_source_lock",
    },
    {
        "residual": "delta_G_or_fifth_force",
        "source_locked_scale_abs": "",
        "confidence_note": "needs dedicated fifth-force / inverse-square-law source lock, not substituted by PPN gamma/beta",
        "source_id": "not_source_locked",
        "MTS_mapping": "epsilon_bulk + epsilon_rad fifth-force residual",
        "runner_status": "quarantined_until_numeric_source_lock",
    },
]


PROXY_COMPARISON = {
    "gamma_minus_1": 2.3e-5,
    "beta_minus_1": 8.0e-5,
    "eta_WEP": 1.0e-14,
    "alpha_clock_redshift": 1.0e-6,
    "preferred_frame_alpha1_alpha2": 4.0e-7,
    "xi_preferred_location_anisotropy": 1.0e-3,
    "delta_G_or_fifth_force": 1.0e-10,
}


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for filename, role in SOURCE_DOCS:
        path = ROOT / filename
        rows.append(
            {
                "source_path": relpath(path),
                "role": role,
                "exists": "yes" if path.exists() else "no",
                "issue": "" if path.exists() else "missing",
            }
        )
    script_path = Path(__file__).resolve()
    rows.append(
        {
            "source_path": relpath(script_path),
            "role": "this source-lock and no-hair deepening builder",
            "exists": "yes" if script_path.exists() else "no",
            "issue": "" if script_path.exists() else "missing",
        }
    )
    return rows


def external_source_rows() -> list[dict[str, Any]]:
    return [
        {
            **source,
            "accessed_date": "2026-06-01",
            "claim_use": "internal local-bound source lock only",
        }
        for source in EXTERNAL_SOURCES
    ]


def bound_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual": row["residual"],
            "source_locked_scale_abs": row["source_locked_scale_abs"],
            "confidence_note": row["confidence_note"],
            "source_id": row["source_id"],
            "MTS_mapping": row["MTS_mapping"],
            "runner_status": row["runner_status"],
            "public_claim_allowed": "no",
        }
        for row in BOUND_TARGETS
    ]


def proxy_delta_rows() -> list[dict[str, Any]]:
    rows = []
    for row in BOUND_TARGETS:
        residual = str(row["residual"])
        proxy = PROXY_COMPARISON.get(residual, "")
        source_locked = row["source_locked_scale_abs"]
        if isinstance(source_locked, float) and isinstance(proxy, float):
            ratio = proxy / source_locked
            status = "proxy_matches" if 0.5 <= ratio <= 2.0 else "proxy_replaced"
            note = f"proxy/source_locked={ratio:.3g}"
        else:
            ratio = ""
            status = "proxy_quarantined"
            note = "no numeric source-locked scale in this pass"
        rows.append(
            {
                "residual": residual,
                "old_proxy_abs": proxy,
                "source_locked_abs": source_locked,
                "ratio_proxy_to_source_locked": ratio,
                "update_status": status,
                "note": note,
            }
        )
    return rows


def nohair_deepening_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "A3_class_only_boundary_action",
            "deepening_attempt": "If S_boundary depends only on total relative class/charge and induced scalar volume, angular representative data are absent.",
            "what_it_would_kill": "trace-free shear and l>=2 boundary multipoles",
            "status_after_354": "conditional_template_not_parent_derived",
            "next_required_move": "derive class-only boundary action from parent variational principle",
        },
        {
            "condition": "A4_no_marker_fields",
            "deepening_attempt": "Forbid material boundary markers, active patch labels, and preferred-frame normals as independent EFT fields.",
            "what_it_would_kill": "B_0i preferred-frame residuals and marker-local counterterms",
            "status_after_354": "open",
            "next_required_move": "prove marker fields are gauge choices, not physical sectors",
        },
        {
            "condition": "A5_no_radial_scalar_hair",
            "deepening_attempt": "Regular isolated exterior permits monopole 1/r charge; safe only if universal and absorbed into measured GM.",
            "what_it_would_kill": "radius-dependent scalar potential residuals",
            "status_after_354": "partly_sharpened_not_closed",
            "next_required_move": "prove any radial term is exactly universal mass renormalization or bound epsilon_rad",
        },
        {
            "condition": "A6_single_metric_coupling",
            "deepening_attempt": "All clocks, rods, matter, and photons must see the same physical metric/coframe before local PPN can be claimed.",
            "what_it_would_kill": "clock/redshift, WEP, and lensing/ruler mismatch residuals",
            "status_after_354": "open_hard_gate",
            "next_required_move": "derive matter coupling from parent action instead of calibrating it",
        },
        {
            "condition": "A7_boundary_Ward_Bianchi_closure",
            "deepening_attempt": "Boundary flux must vanish or be exactly balanced by an owned conserved charge.",
            "what_it_would_kill": "fake conservation and secular local dynamics",
            "status_after_354": "open_hard_gate",
            "next_required_move": "derive boundary Ward identity from diffeomorphism/relative-chain invariance",
        },
    ]


def runner_readiness_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_sector": "gamma_beta_scalar_metric",
            "readiness": "ready_internal",
            "usable_bounds": "gamma_minus_1, beta_minus_1",
            "quarantine": "requires model coefficients before pass/fail",
        },
        {
            "runner_sector": "WEP_clock",
            "readiness": "ready_internal",
            "usable_bounds": "eta_WEP, alpha_clock_redshift",
            "quarantine": "single-metric coupling still not derived",
        },
        {
            "runner_sector": "preferred_frame_anisotropy",
            "readiness": "not_ready",
            "usable_bounds": "none numeric source-locked in this pass",
            "quarantine": "do not score epsilon_vec or xi until numeric source lock",
        },
        {
            "runner_sector": "fifth_force_delta_G",
            "readiness": "not_ready",
            "usable_bounds": "none numeric source-locked in this pass",
            "quarantine": "needs dedicated inverse-square/fifth-force source lock",
        },
    ]


def gate_result_rows(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in sources)
    numeric_locked = sum(1 for row in BOUND_TARGETS if isinstance(row["source_locked_scale_abs"], float))
    quarantined = sum(1 for row in BOUND_TARGETS if row["runner_status"].startswith("quarantined"))
    return [
        {
            "gate": "local_source_paths_exist",
            "status": "pass" if sources_ok else "fail",
            "evidence": "all cited local checkpoints and this script exist" if sources_ok else "missing cited source",
        },
        {
            "gate": "external_sources_recorded",
            "status": "pass",
            "evidence": f"{len(EXTERNAL_SOURCES)} external sources recorded with URLs",
        },
        {
            "gate": "numeric_bounds_source_locked",
            "status": "partial_pass",
            "evidence": f"{numeric_locked} numeric target scales locked; {quarantined} residual sectors quarantined",
        },
        {
            "gate": "proxy_values_replaced_or_quarantined",
            "status": "pass",
            "evidence": "old proxy rows compared against source-locked rows",
        },
        {
            "gate": "nohair_proof_deepened",
            "status": "partial_pass",
            "evidence": "A3-A7 sharpened but not derived",
        },
        {
            "gate": "official_PPN_pass_allowed",
            "status": "fail",
            "evidence": "bounds are internal targets and no MTS residual coefficients have been derived",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "A3-A7 and single-metric coupling remain open",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The local-bound runner is no longer purely proxy for gamma, beta, WEP, and clock/redshift sectors: "
                "those target scales now have explicit source URLs and confidence notes. Preferred-frame, anisotropy, "
                "and fifth-force sectors remain quarantined until numeric sources are locked. The no-hair proof also "
                "deepened: class-only boundary action, no marker fields, no radial scalar hair, single-metric coupling, "
                "and boundary Ward closure are now the exact remaining theorem debts. No official local-bound pass or "
                "local-GR promotion is allowed."
            ),
            "next_target": NEXT_TARGET,
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    outputs = {
        "source_register.csv": (
            sources,
            ["source_path", "role", "exists", "issue"],
        ),
        "external_source_lock.csv": (
            external_source_rows(),
            ["source_id", "title", "url", "use", "source_status", "accessed_date", "claim_use"],
        ),
        "source_locked_bound_manifest.csv": (
            bound_manifest_rows(),
            [
                "residual",
                "source_locked_scale_abs",
                "confidence_note",
                "source_id",
                "MTS_mapping",
                "runner_status",
                "public_claim_allowed",
            ],
        ),
        "proxy_to_source_locked_delta.csv": (
            proxy_delta_rows(),
            [
                "residual",
                "old_proxy_abs",
                "source_locked_abs",
                "ratio_proxy_to_source_locked",
                "update_status",
                "note",
            ],
        ),
        "nohair_proof_deepening.csv": (
            nohair_deepening_rows(),
            ["condition", "deepening_attempt", "what_it_would_kill", "status_after_354", "next_required_move"],
        ),
        "runner_readiness_after_source_lock.csv": (
            runner_readiness_rows(),
            ["runner_sector", "readiness", "usable_bounds", "quarantine"],
        ),
        "gate_results.csv": (
            gate_result_rows(sources),
            ["gate", "status", "evidence"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "meaning", "next_target"],
        ),
    }

    for filename, (rows, fieldnames) in outputs.items():
        write_csv(result_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(result_dir),
        "generated": list(outputs),
        "missing_local_sources": sum(row["exists"] != "yes" for row in sources),
        "external_sources_recorded": len(EXTERNAL_SOURCES),
        "numeric_bounds_source_locked": sum(1 for row in BOUND_TARGETS if isinstance(row["source_locked_scale_abs"], float)),
        "quarantined_bound_sectors": sum(1 for row in BOUND_TARGETS if row["runner_status"].startswith("quarantined")),
        "nohair_proof_deepened": True,
        "official_PPN_pass_allowed": False,
        "local_GR_promoted": False,
        "next_target": NEXT_TARGET,
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build checkpoint 354: official local-bound source lock or no-hair proof deepening.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
