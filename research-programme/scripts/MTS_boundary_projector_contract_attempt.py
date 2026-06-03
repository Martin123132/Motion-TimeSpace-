from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "MTS-boundary-projector-contract-attempt"
STATUS = "P_MTS_projector_contract_constructed_conditional_not_parent_derived"
CLAIM_CEILING = "conditional_boundary_projector_contract_no_selector_local_GR_or_Bmem_promotion"


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
        (ROOT / "207-domain-projector-action-and-Bianchi-identity.md", "variational projector and Bianchi accounting"),
        (ROOT / "231-Jrel-cohomology-projector-or-local-EH-limit.md", "relative cohomology gate for local J_rel exactness"),
        (ROOT / "276-coherent-domain-projector-from-parent-variables.md", "fixed-D coherent scalar projector"),
        (ROOT / "278-admissible-domain-class-boundary-current-owner.md", "relative class preserving boundary variations"),
        (ROOT / "287-boundary-current-charge-owner-attempt.md", "formal relative boundary-current owner"),
        (ROOT / "308-selector-parent-theorem-attempt.md", "P_MTS projector target from selector theorem"),
        (ROOT / "runs" / "20260601-000094-coherent-domain-projector-from-parent-variables" / "results" / "gate_results.csv", "coherent projector gates"),
        (ROOT / "runs" / "20260601-000096-admissible-domain-class-boundary-current-owner" / "results" / "gate_results.csv", "admissible boundary-current gates"),
        (ROOT / "runs" / "20260601-000110-boundary-current-charge-owner-attempt" / "results" / "gate_results.csv", "boundary-current owner gates"),
        (ROOT / "runs" / "20260601-000131-selector-parent-theorem-attempt" / "results" / "promotion_gates.csv", "selector theorem gates"),
        (ROOT / "scripts" / "MTS_boundary_projector_contract_attempt.py", "this projector contract runner"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def projector_component_rows() -> list[dict[str, Any]]:
    return [
        {
            "component": "P_ord_perp",
            "definition": "orthogonal complement to ordinary EM/matter/environmental boundary operators",
            "mathematical_role": "kills generic local baths before rho_D is formed",
            "source_support": "selector checkpoint 308 generic bath no-go",
            "status": "required_contract_not_parent_derived",
        },
        {
            "component": "P_rel",
            "definition": "relative cohomology / harmonic class projector Pi_rel on [J_B]_D",
            "mathematical_role": "kills exact/no-flux local boundary currents and keeps nontrivial relative memory classes",
            "source_support": "checkpoints 231, 278, 287",
            "status": "cohomology_gate_constructed_parent_selection_open",
        },
        {
            "component": "P_IR",
            "definition": "IR spectral projector onto the MTS boundary channel relevant to b_D=lim rho/omega",
            "mathematical_role": "separates gapless Ohmic FLRW memory bath from gapped local projected channel",
            "source_support": "checkpoint 308",
            "status": "selector_factor_contract",
        },
        {
            "component": "P_coh",
            "definition": "coherent scalar/isotropic trace projector for fixed domain D",
            "mathematical_role": "keeps FLRW scalar coherent mode and removes tracefree shear/local noncoherent hair",
            "source_support": "checkpoint 276",
            "status": "fixed_D_projection_derived_domain_selection_open",
        },
        {
            "component": "P_Ward",
            "definition": "Ward-safe projection retaining only boundary/memory modes with explicit stress accounting",
            "mathematical_role": "prevents projector from hiding Bianchi/conservation leakage",
            "source_support": "checkpoint 207",
            "status": "formal_Bianchi_contract_conditional",
        },
    ]


def projector_algebra_rows() -> list[dict[str, Any]]:
    return [
        {
            "algebra_item": "projector_definition",
            "formula": "P_MTS,D = P_Ward P_coh P_IR P_rel P_ord_perp",
            "condition": "component maps act on the same boundary Hilbert/symplectic space",
            "result": "candidate MTS boundary projector",
            "status": "contract_constructed",
        },
        {
            "algebra_item": "idempotence",
            "formula": "P_MTS^2=P_MTS",
            "condition": "each component is idempotent and the relevant components commute on the admissible subspace",
            "result": "true under commuting-projector contract",
            "status": "conditional_pass",
        },
        {
            "algebra_item": "self_adjointness",
            "formula": "<P_MTS A,B>_D=<A,P_MTS B>_D",
            "condition": "the parent action supplies the boundary inner product and each component is orthogonal/self-adjoint",
            "result": "needed for a spectral density rho[P_MTS B,P_MTS B]",
            "status": "not_parent_derived",
        },
        {
            "algebra_item": "ordinary_bath_annihilation",
            "formula": "P_MTS B_ord=0",
            "condition": "B_ord lies in ordinary EM/matter/environmental subspace killed by P_ord_perp",
            "result": "ordinary warm local baths do not activate sigma_D",
            "status": "conditional_pass",
        },
        {
            "algebra_item": "local_exact_current_annihilation",
            "formula": "P_MTS d_rel chi=0",
            "condition": "relative exact/no-flux local current has no harmonic relative class",
            "result": "local trivial class gives c_D=0",
            "status": "conditional_pass",
        },
        {
            "algebra_item": "FLRW_memory_retention",
            "formula": "P_MTS B_FLRW=B_FLRW^coh,rel,IR",
            "condition": "FLRW domain has coherent scalar, nontrivial relative class, and gapless projected IR bath",
            "result": "cosmological branch is not killed",
            "status": "conditional_pass",
        },
        {
            "algebra_item": "Bianchi_safe_variation",
            "formula": "nabla_mu T_total^{mu nu}=0 with T_projector+T_boundary retained",
            "condition": "P_MTS is varied as an action-level/domain object, not inserted after solving",
            "result": "no hidden conservation cheat",
            "status": "conditional_pass",
        },
    ]


def domain_projection_rows() -> list[dict[str, Any]]:
    cases = [
        {
            "domain": "ordinary_warm_laboratory",
            "ordinary_bath": True,
            "relative_class_nonzero": False,
            "IR_gapless_MTS": False,
            "coherent_scalar": False,
            "Ward_safe": True,
            "interpretation": "ordinary baths must be killed by P_ord_perp",
        },
        {
            "domain": "stationary_solar_system_exterior",
            "ordinary_bath": False,
            "relative_class_nonzero": False,
            "IR_gapless_MTS": False,
            "coherent_scalar": False,
            "Ward_safe": True,
            "interpretation": "local silence if relative class and MTS IR bath vanish",
        },
        {
            "domain": "time_dependent_local_radiator",
            "ordinary_bath": True,
            "relative_class_nonzero": False,
            "IR_gapless_MTS": "uncertain",
            "coherent_scalar": False,
            "Ward_safe": True,
            "interpretation": "safe only if ordinary radiation is projected out and no MTS relative class appears",
        },
        {
            "domain": "black_hole_or_horizon_edge",
            "ordinary_bath": False,
            "relative_class_nonzero": "possible",
            "IR_gapless_MTS": "possible",
            "coherent_scalar": "possible",
            "Ward_safe": "unknown",
            "interpretation": "separate horizon branch, not covered by lab local silence",
        },
        {
            "domain": "galaxy_or_cluster_extended_bound",
            "ordinary_bath": False,
            "relative_class_nonzero": "possible",
            "IR_gapless_MTS": "mixed",
            "coherent_scalar": "mixed",
            "Ward_safe": "unknown",
            "interpretation": "empirical pillar/domain branch, must not be erased by lab theorem",
        },
        {
            "domain": "FLRW_coherent_domain",
            "ordinary_bath": False,
            "relative_class_nonzero": True,
            "IR_gapless_MTS": True,
            "coherent_scalar": True,
            "Ward_safe": True,
            "interpretation": "projector keeps cosmological memory channel if contracts are parent-owned",
        },
    ]
    rows: list[dict[str, Any]] = []
    for case in cases:
        ordinary_bath = case["ordinary_bath"]
        relative_class_nonzero = case["relative_class_nonzero"]
        IR_gapless_MTS = case["IR_gapless_MTS"]
        coherent_scalar = case["coherent_scalar"]
        Ward_safe = case["Ward_safe"]

        if ordinary_bath is True:
            ordinary_projection = "killed_if_P_ord_perp_derived"
        else:
            ordinary_projection = "not_ordinary_bath_control"

        strict_active = (
            ordinary_bath is False
            and relative_class_nonzero is True
            and IR_gapless_MTS is True
            and coherent_scalar is True
            and Ward_safe is True
        )
        strict_silent = (
            relative_class_nonzero is False
            or IR_gapless_MTS is False
            or coherent_scalar is False
        )

        if strict_active:
            status = "MTS_channel_retained_conditional"
            projected_sigma = "nonzero_if_parent_contracts_hold"
        elif strict_silent:
            status = "MTS_channel_silent_conditional"
            projected_sigma = "zero_if_parent_contracts_hold"
        else:
            status = "edge_case_unresolved"
            projected_sigma = "requires_domain_specific_branch"

        rows.append(
            {
                **case,
                "ordinary_projection": ordinary_projection,
                "projected_sigma": projected_sigma,
                "status": status,
            }
        )
    return rows


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "P_MTS can be any filter that makes local tests pass",
            "result": "fail",
            "reason": "external filters were already rejected; projector must be variational and Bianchi-accounted",
            "repair": "derive P_MTS from boundary operator decomposition and include projector stress",
        },
        {
            "claim": "ordinary bath projection is automatic",
            "result": "fail",
            "reason": "without P_ord_perp, ordinary EM/matter baths contaminate rho_D",
            "repair": "derive the ordinary/MTS boundary-sector split from parent variables or symmetries",
        },
        {
            "claim": "relative cohomology alone defines P_MTS",
            "result": "partial",
            "reason": "relative class kills exact memory currents but does not by itself remove generic bath spectra or guarantee FLRW IR activity",
            "repair": "combine P_rel with P_ord_perp, P_IR, P_coh, and Ward stress accounting",
        },
        {
            "claim": "fixed-D coherent projection is enough",
            "result": "partial",
            "reason": "it removes tracefree/noncoherent modes only after D is supplied",
            "repair": "derive domain selection/free-boundary rule and couple it to P_MTS",
        },
        {
            "claim": "projector stress can be omitted",
            "result": "fail",
            "reason": "omitting projector/domain/boundary stress can fake Bianchi conservation",
            "repair": "retain T_projector, T_boundary, and domain variation in the parent action",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    source_missing = [source for source in source_register_rows() if source["exists"] != "yes"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all cited projector/current/selector sources exist" if not source_missing else ";".join(source["source"] for source in source_missing),
            "claim_effect": "attempt traceable",
        },
        {
            "gate": "P_MTS_contract_written",
            "status": "pass",
            "evidence": "P_MTS,D = P_Ward P_coh P_IR P_rel P_ord_perp",
            "claim_effect": "projector target is no longer vague",
        },
        {
            "gate": "ordinary_bath_annihilation_defined",
            "status": "conditional_pass",
            "evidence": "P_ord_perp B_ord=0 by contract",
            "claim_effect": "generic local EM/environmental baths have a non-cheating exclusion condition",
        },
        {
            "gate": "relative_exact_current_annihilation_defined",
            "status": "conditional_pass",
            "evidence": "P_rel d_rel chi=0",
            "claim_effect": "local trivial class can silence trace-source memory activation",
        },
        {
            "gate": "FLRW_retention_defined",
            "status": "conditional_pass",
            "evidence": "P_MTS keeps coherent scalar, IR, nontrivial relative FLRW channel",
            "claim_effect": "projector does not automatically kill cosmology",
        },
        {
            "gate": "projector_idempotence_parent_owned",
            "status": "fail",
            "evidence": "commuting self-adjoint component projectors and inner product are contracts",
            "claim_effect": "projector algebra not parent-derived",
        },
        {
            "gate": "ordinary_MTS_sector_split_parent_derived",
            "status": "fail",
            "evidence": "no parent theorem derives P_ord_perp from variables/symmetry",
            "claim_effect": "generic bath problem not fully closed",
        },
        {
            "gate": "domain_selection_parent_derived",
            "status": "fail",
            "evidence": "fixed-D projection exists but physical domain D is still not selected",
            "claim_effect": "local/FLRW split not promoted",
        },
        {
            "gate": "Bianchi_projector_stress_parent_closed",
            "status": "conditional_pass",
            "evidence": "formal route exists if T_projector+T_boundary+domain variation retained",
            "claim_effect": "conservation can be honest but is not fully derived",
        },
        {
            "gate": "selector_parent_derived",
            "status": "fail",
            "evidence": "P_MTS components remain conditional contracts",
            "claim_effect": "sigma_D selector remains theorem target",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "projector, domain, beta, profile, and official PPN manifest are not parent-owned",
            "claim_effect": "no local-GR or PPN promotion",
        },
        {
            "gate": "B_mem_parent_derived",
            "status": "fail",
            "evidence": "projector contract does not derive charge unit, k=9, endpoint occupancies, or arrow",
            "claim_effect": "2/27 remains empirical closure/theorem target",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "target": "ordinary_MTS_sector_split",
            "task": "derive P_ord_perp from parent variables, symmetries, or block-diagonal boundary kinetic kernel",
            "success_gate": "ordinary EM/matter baths are orthogonal to the MTS memory boundary operator",
        },
        {
            "priority": 2,
            "target": "projector_inner_product_and_commutation",
            "task": "derive the boundary inner product and show P_ord_perp, P_rel, P_IR, P_coh, P_Ward commute on admissible states",
            "success_gate": "P_MTS^2=P_MTS and P_MTS is self-adjoint by theorem",
        },
        {
            "priority": 3,
            "target": "domain_selection_rule",
            "task": "derive the physical domain D/free-boundary rule for stationary local and FLRW coherent domains",
            "success_gate": "lab-local D maps to silent projected channel while FLRW maps to active projected channel without empirical threshold tuning",
        },
        {
            "priority": 4,
            "target": "Bianchi_stress_ledger",
            "task": "write the explicit T_projector and T_boundary terms required by varying P_MTS and D",
            "success_gate": "nabla_mu T_total^{mu nu}=0 closes without hiding projector forces",
        },
        {
            "priority": 5,
            "target": "empirical_holdout_pivot",
            "task": "keep local projector as conditional and test cosmology/galaxy branches against stricter holdouts",
            "success_gate": "no unresolved projector theorem is used as evidence",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "decision": "P_MTS has a precise component contract but remains conditional",
            "recommended_next": "derive the ordinary/MTS sector split or pivot to empirical holdout testing",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    outputs = {
        "source_register": source_register_rows(),
        "projector_components": projector_component_rows(),
        "projector_algebra": projector_algebra_rows(),
        "domain_projection_tests": domain_projection_rows(),
        "no_go_tests": no_go_rows(),
        "promotion_gates": promotion_gate_rows(),
        "next_targets": next_target_rows(),
        "decision": decision_rows(),
    }

    write_csv(results_dir / "source_register.csv", outputs["source_register"], ["source", "role", "exists"])
    write_csv(
        results_dir / "projector_components.csv",
        outputs["projector_components"],
        ["component", "definition", "mathematical_role", "source_support", "status"],
    )
    write_csv(
        results_dir / "projector_algebra.csv",
        outputs["projector_algebra"],
        ["algebra_item", "formula", "condition", "result", "status"],
    )
    write_csv(
        results_dir / "domain_projection_tests.csv",
        outputs["domain_projection_tests"],
        [
            "domain",
            "ordinary_bath",
            "relative_class_nonzero",
            "IR_gapless_MTS",
            "coherent_scalar",
            "Ward_safe",
            "interpretation",
            "ordinary_projection",
            "projected_sigma",
            "status",
        ],
    )
    write_csv(results_dir / "no_go_tests.csv", outputs["no_go_tests"], ["claim", "result", "reason", "repair"])
    write_csv(results_dir / "promotion_gates.csv", outputs["promotion_gates"], ["gate", "status", "evidence", "claim_effect"])
    write_csv(results_dir / "next_targets.csv", outputs["next_targets"], ["priority", "target", "task", "success_gate"])
    write_csv(results_dir / "decision.csv", outputs["decision"], ["status", "claim_ceiling", "decision", "recommended_next"])

    payload = {
        "run_slug": RUN_SLUG,
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": relpath(run_dir),
        "outputs": {name: len(rows) for name, rows in outputs.items()},
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "COMPLETE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Construct and gate the P_MTS boundary projector contract.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
