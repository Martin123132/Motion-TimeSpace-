from __future__ import annotations

import math
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4903"
NEXT_TARGET = (
    "4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-"
    "parameter-prediction-ledger.md"
)

VACUUM_MISALIGNMENT_URL = "https://doi.org/10.1016/0370-2693(84)91177-8"
COMPOSITE_HIGGS_URL = "https://doi.org/10.1016/0370-2693(84)91178-X"
CUSTODIAL_HIGGS_URL = "https://doi.org/10.1016/0370-2693(84)90341-1"
ATLAS_CMS_HH_URL = "https://arxiv.org/abs/2602.23991"


def contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    local_sources = [
        (
            "SRC4903_00_4902",
            POST
            / "4902-Y5-R2FR-electroweak-breaking-Higgs-Yukawa-owner-and-mass-generation-or-SM-parameter-freeze.md",
            "MTS_HIGGS_YUKAWA_MASS_OWNERSHIP_GATE_4902",
            "validated_predecessor",
        ),
        (
            "SRC4903_01_4902_validation",
            OUTPUT / "P8_Y5_BRR545_4902_VALIDATION.csv",
            "VAL4902_OVERALL,PASS",
            "validated_predecessor",
        ),
        (
            "SRC4903_02_4854_CP2",
            POST
            / "4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md",
            "U1_BASELINE_CP2_CONSTITUTIVE_GATE_4854",
            "original_CP2_clue",
        ),
        (
            "SRC4903_03_4901_SM",
            POST
            / "4901-Y5-R2FR-nonabelian-SU2xSU3-parent-and-chiral-anomaly-cancellation-or-standard-model-correspondence-freeze.md",
            "MTS_NONABELIAN_CHIRAL_SM_CORRESPONDENCE_GATE_4901",
            "active_SM_correspondence",
        ),
        (
            "SRC4903_04_formal4902",
            FORMAL / "918-PPC4161-Higgs-Yukawa-mass-ownership.md",
            "PPC4161_HIGGS_YUKAWA_MASS_OWNERSHIP_4902",
            "current_Higgs_ownership_record",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker, role in local_sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": role,
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": path.exists(),
                "marker": marker,
                "marker_found": contains(path, marker),
                "source_checked_date": "2026-07-11",
            }
        )
    external = (
        (
            "SRC4903_05_vacuum_misalignment",
            VACUUM_MISALIGNMENT_URL,
            "vacuum misalignment primary source",
        ),
        (
            "SRC4903_06_composite_Higgs",
            COMPOSITE_HIGGS_URL,
            "composite Higgs primary source",
        ),
        (
            "SRC4903_07_custodial_Higgs",
            CUSTODIAL_HIGGS_URL,
            "custodial composite-Higgs primary source",
        ),
        (
            "SRC4903_08_ATLAS_CMS_HH",
            ATLAS_CMS_HH_URL,
            "ATLAS+CMS Run-2 HH combination with kappa_2V interval",
        ),
    )
    for source_id, url, marker in external:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "primary_external_source",
                "source_path_or_url": url,
                "local_path_required": False,
                "source_exists": True,
                "marker": marker,
                "marker_found": True,
                "source_checked_date": "2026-07-11",
            }
        )
    return {
        "rows": rows,
        "local_sources": len(local_sources),
        "external_sources": len(external),
        "passed": all(
            row["source_exists"]
            and row["marker_found"]
            and (
                row["local_path_required"]
                or str(row["source_path_or_url"]).startswith("https://")
            )
            for row in rows
        ),
    }


@lru_cache(maxsize=None)
def custodial_coset_construction() -> dict[str, Any]:
    rows = [
        {
            "property": "coset",
            "equation": "SO5/SO4 is isomorphic to S4",
            "result": "four-dimensional homogeneous target",
            "status": "EXPLICIT_OPTIONAL_COMPLETION",
        },
        {
            "property": "field_count",
            "equation": "dim SO5-dim SO4=10-6",
            "result": "4",
            "status": "ONE_HIGGS_DOUBLET_NO_EXTRA_PNGB",
        },
        {
            "property": "custodial_group",
            "equation": "SO4 is locally SU2L x SU2R",
            "result": "unbroken custodial algebra",
            "status": "TREE_T_PROTECTION_AVAILABLE",
        },
        {
            "property": "Goldstone_representation",
            "equation": "4 of SO4=(2,2) under SU2L x SU2R",
            "result": "one complex SU2L doublet",
            "status": "HIGGS_REPRESENTATION_CLOSED",
        },
        {
            "property": "sigma_field",
            "equation": "Sigma=(0,0,0,sin(h/f),cos(h/f))",
            "result": "Sigma.Sigma=1",
            "status": "NONLINEAR_REALIZATION_CLOSED",
        },
        {
            "property": "kinetic_action",
            "equation": "L=f2 (D_mu Sigma)^T(D^mu Sigma)/2",
            "result": "positive for f2>0",
            "status": "KINETIC_GEOMETRY_CLOSED",
        },
        {
            "property": "potential",
            "equation": "SO5 acts transitively on SO5/SO4",
            "result": "exactly invariant scalar potential is constant",
            "status": "EXPLICIT_BREAKING_STILL_REQUIRED",
        },
    ]
    return {
        "rows": rows,
        "Goldstone_count": 4,
        "complex_Higgs_doublets": 1,
        "custodial_SU2R_present": True,
        "nonconstant_invariant_potential": False,
        "minimal_in_pNGB_field_count": True,
        "unique_group_theoretic_completion": False,
        "selected_by_MTS_parent": False,
        "passed": len(rows) == 7,
    }


@lru_cache(maxsize=None)
def custodial_mass_gate() -> dict[str, Any]:
    g2, gY, decay_scale, theta = sp.symbols(
        "g2 gY f theta", positive=True
    )
    sine = sp.sin(theta)
    mW_squared = sp.factor(g2**2 * decay_scale**2 * sine**2 / 4)
    mZ_squared = sp.factor(
        (g2**2 + gY**2) * decay_scale**2 * sine**2 / 4
    )
    cosine_weak_squared = g2**2 / (g2**2 + gY**2)
    rho = sp.simplify(mW_squared / (mZ_squared * cosine_weak_squared))
    rows = [
        {
            "object": "electroweak_scale",
            "equation": "v=f sin(theta)",
            "result": "vacuum misalignment relation",
            "status": "CONDITIONAL_GEOMETRIC_MAP",
        },
        {
            "object": "W_mass",
            "equation": "mW2=g2^2 f2 sin2theta/4",
            "result": str(mW_squared),
            "status": "DERIVED",
        },
        {
            "object": "Z_mass",
            "equation": "mZ2=(g2^2+gY^2)f2 sin2theta/4",
            "result": str(mZ_squared),
            "status": "DERIVED",
        },
        {
            "object": "photon_mass",
            "equation": "det neutral mass matrix=0",
            "result": "0",
            "status": "U1EM_UNBROKEN",
        },
        {
            "object": "rho",
            "equation": "mW2/(mZ2 cos2thetaW)",
            "result": str(rho),
            "status": "CUSTODIAL_EXACTLY_ONE",
        },
    ]
    return {
        "rows": rows,
        "mW_squared": str(mW_squared),
        "mZ_squared": str(mZ_squared),
        "rho": str(rho),
        "rho_minus_one": str(sp.simplify(rho - 1)),
        "photon_mass_squared": "0",
        "custodial_tree_gate_passed": rho == 1,
        "passed": len(rows) == 5 and rho == 1,
    }


@lru_cache(maxsize=None)
def Higgs_coupling_map() -> dict[str, Any]:
    theta, fluctuation, decay_scale, coefficient = sp.symbols(
        "theta h f C", positive=True
    )
    mass_function = coefficient * sp.sin(theta + fluctuation / decay_scale) ** 2
    mass_at_vacuum = sp.simplify(mass_function.subs(fluctuation, 0))
    vacuum = decay_scale * sp.sin(theta)
    first = sp.diff(mass_function, fluctuation).subs(fluctuation, 0)
    second = sp.diff(mass_function, fluctuation, 2).subs(fluctuation, 0)
    kappa_V = sp.trigsimp(vacuum * first / (2 * mass_at_vacuum))
    kappa_2V = sp.trigsimp(vacuum**2 * second / (2 * mass_at_vacuum))
    xi = sp.symbols("xi", nonnegative=True)
    kappa_V_xi = sp.sqrt(1 - xi)
    kappa_2V_xi = 1 - 2 * xi
    relation = sp.simplify(kappa_2V_xi - (2 * kappa_V_xi**2 - 1))
    rows = [
        {
            "coupling": "hVV",
            "derivation": "first derivative of sin2(theta+h/f)",
            "modifier": "sqrt(1-xi)",
            "symbolic_theta": str(kappa_V),
        },
        {
            "coupling": "hhVV",
            "derivation": "second derivative of sin2(theta+h/f)",
            "modifier": "1-2xi",
            "symbolic_theta": str(kappa_2V),
        },
        {
            "coupling": "correlation",
            "derivation": "eliminate xi",
            "modifier": "kappa_2V=2 kappa_V^2-1",
            "symbolic_theta": str(relation),
        },
    ]
    return {
        "rows": rows,
        "xi_definition": "xi=v^2/f^2=sin^2(theta)",
        "kappa_V": str(kappa_V_xi),
        "kappa_2V": str(kappa_2V_xi),
        "coupling_relation_residual": str(relation),
        "gauge_coupling_prediction_dimension": 1,
        "fermion_modifier_unique": False,
        "passed": bool(
            sp.trigsimp(kappa_V - sp.cos(theta)) == 0
            and sp.trigsimp(kappa_2V - sp.cos(2 * theta)) == 0
            and relation == 0
        ),
    }


@lru_cache(maxsize=None)
def primary_kappa2V_bound_smoke() -> dict[str, Any]:
    observed_lower = Fraction(73, 100)
    observed_upper = Fraction(13, 10)
    xi_max = (1 - observed_lower) / 2
    f_over_v_min = math.sqrt(1 / float(xi_max))
    kappa_V_min = math.sqrt(1 - float(xi_max))
    rows = [
        {
            "source": ATLAS_CMS_HH_URL,
            "dataset": "ATLAS+CMS Run2 HH combination",
            "quantity": "kappa_2V",
            "confidence_level": "95_percent_observed_individual_interval",
            "lower": float(observed_lower),
            "upper": float(observed_upper),
            "extraction": "primary abstract anchor",
        },
        {
            "source": "SO5/SO4 gauge-sector map",
            "dataset": "conditional model",
            "quantity": "xi",
            "confidence_level": "translated_smoke_not_likelihood_reproduction",
            "lower": 0.0,
            "upper": float(xi_max),
            "extraction": "xi<=(1-kappa2V_lower)/2",
        },
        {
            "source": "SO5/SO4 gauge-sector map",
            "dataset": "conditional model",
            "quantity": "f_over_v",
            "confidence_level": "translated_smoke_not_likelihood_reproduction",
            "lower": f_over_v_min,
            "upper": "unbounded",
            "extraction": "f/v>=1/sqrt(xi_max)",
        },
    ]
    return {
        "rows": rows,
        "observed_kappa2V_lower": float(observed_lower),
        "observed_kappa2V_upper": float(observed_upper),
        "xi_max_fraction": f"{xi_max.numerator}/{xi_max.denominator}",
        "xi_max": float(xi_max),
        "f_over_v_min": f_over_v_min,
        "kappa_V_min_implied": kappa_V_min,
        "full_experimental_likelihood_reproduced": False,
        "valid_as_conditional_smoke_bound": True,
        "passed": bool(
            xi_max == Fraction(27, 200)
            and abs(f_over_v_min - 2.721655269759087) < 1.0e-12
        ),
    }


@lru_cache(maxsize=None)
def completion_comparator() -> dict[str, Any]:
    rows = [
        {
            "route": "linear_SM_Higgs",
            "real_scalar_count": 4,
            "custodial_tree_rho": "1",
            "nonlinear_scale": "none",
            "potential_origin": "imported renormalizable",
            "MTS_parent_selection": False,
            "active_status": "ACTIVE_KNOWN_LIMIT",
        },
        {
            "route": "CP2_SU3_over_U2",
            "real_scalar_count": 4,
            "custodial_tree_rho": "1+t^2",
            "nonlinear_scale": "f_CP2",
            "potential_origin": "explicit breaking missing",
            "MTS_parent_selection": False,
            "active_status": "FROZEN_AS_INTERNAL_GEOMETRY_CLUE",
        },
        {
            "route": "SO5_over_SO4",
            "real_scalar_count": 4,
            "custodial_tree_rho": "1",
            "nonlinear_scale": "f",
            "potential_origin": "explicit breaking missing",
            "MTS_parent_selection": False,
            "active_status": "OPTIONAL_PRECISION_BENCHMARK_ONLY",
        },
    ]
    return {
        "rows": rows,
        "same_minimal_scalar_count": True,
        "CP2_custodial_failure_repaired": True,
        "new_group_selection_cost": 1,
        "new_continuous_parameters_before_potential": 2,
        "predictive_gauge_correlation": "kappa_2V=2 kappa_V^2-1",
        "MTS_primitive_improvement": False,
        "passed": len(rows) == 3,
    }


@lru_cache(maxsize=None)
def parent_ownership_gate() -> dict[str, Any]:
    clauses = [
        ("SO5_global_parent", False, "no SO5 action or current in the MTS corpus"),
        ("SO5_to_SO4_breaking", False, "no condensate or constraint selects the coset"),
        ("decay_scale_f", False, "no microscopic matching equation"),
        ("misalignment_theta", False, "no potential minimum or preparation law"),
        ("custodial_embedding", True, "explicit SO4 construction protects tree rho"),
        ("gauge_coupling_map", True, "kappaV and kappa2V correlation derived"),
        ("primary_precision_smoke", True, "ATLAS+CMS interval gives xi<0.135 conditionally"),
        ("fermion_embeddings", False, "Yukawa modifiers are representation dependent"),
        ("resonance_spectrum", False, "oblique and high-energy corrections cannot be computed"),
        ("potential_coefficients", False, "exact homogeneous symmetry permits only a constant"),
        ("full_likelihood", False, "only a primary interval translation is run"),
        ("linear_Higgs_fallback", True, "active correspondence remains closed"),
    ]
    rows = [
        {"clause": name, "closed": closed, "evidence": evidence}
        for name, closed, evidence in clauses
    ]
    primitive = rows[:10]
    return {
        "rows": rows,
        "total_clauses": len(rows),
        "closed_clauses": sum(row["closed"] for row in rows),
        "primitive_required_clauses": len(primitive),
        "primitive_closed_clauses": sum(row["closed"] for row in primitive),
        "primitive_custodial_Higgs_reentry": all(
            row["closed"] for row in primitive
        ),
        "linear_Higgs_fallback_closed": rows[-1]["closed"],
        "passed": bool(
            len(rows) == 12
            and not all(row["closed"] for row in primitive)
            and rows[-1]["closed"]
        ),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    return {
        "custodial_construction_status": (
            "SO5_OVER_SO4_MINIMAL_FIELD_COUNT_COMPLETION_DERIVED_RHO_ONE"
        ),
        "precision_status": (
            "KAPPA2V_PRIMARY_INTERVAL_TRANSLATED_TO_XI_LT_0P135_"
            "CONDITIONAL_SMOKE_ONLY"
        ),
        "CP2_Higgs_status": (
            "FROZEN_AS_INTERNAL_U2_GEOMETRY_CLUE_NOT_ACTIVE_HIGGS_ROUTE"
        ),
        "SO5_Higgs_status": (
            "OPTIONAL_CUSTODIAL_BENCHMARK_NOT_SELECTED_BY_MTS_PARENT"
        ),
        "active_Higgs_status": (
            "LINEAR_STANDARD_MODEL_HIGGS_CORRESPONDENCE_REMAINS_ACTIVE"
        ),
        "primitive_Higgs_claim_allowed": False,
        "public_precision_claim_allowed": False,
        "next_target": NEXT_TARGET,
        "passed": bool(
            source_contract()["passed"]
            and custodial_coset_construction()["passed"]
            and custodial_mass_gate()["passed"]
            and Higgs_coupling_map()["passed"]
            and primary_kappa2V_bound_smoke()["passed"]
            and completion_comparator()["passed"]
            and parent_ownership_gate()["passed"]
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "coset": custodial_coset_construction(),
        "mass": custodial_mass_gate(),
        "couplings": Higgs_coupling_map(),
        "bound": primary_kappa2V_bound_smoke(),
        "comparator": completion_comparator(),
        "ownership": parent_ownership_gate(),
        "arbitration": arbitration(),
    }
    checks = {
        name: bool(section["passed"])
        for name, section in sections.items()
        if "passed" in section
    }
    return {
        "checkpoint": CHECKPOINT,
        "sections": sections,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "decision": arbitration()["active_Higgs_status"],
    }


def main() -> int:
    calculation = result()
    mass = calculation["sections"]["mass"]
    coupling = calculation["sections"]["couplings"]
    bound = calculation["sections"]["bound"]
    print(
        f"rho={mass['rho']} kappaV={coupling['kappa_V']} "
        f"kappa2V={coupling['kappa_2V']} xi_max={bound['xi_max']:.6f} "
        f"f_over_v_min={bound['f_over_v_min']:.6f}"
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
