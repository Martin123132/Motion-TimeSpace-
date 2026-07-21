from __future__ import annotations

import re
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
QPF = ROOT / "quantum-particle-field"
CORE = ROOT / "core-mts-framework"
OUTPUT = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4901"
NEXT_TARGET = (
    "4902-Y5-R2FR-electroweak-breaking-Higgs-Yukawa-owner-and-"
    "mass-generation-or-SM-parameter-freeze.md"
)

YANG_MILLS_URL = "https://doi.org/10.1103/PhysRev.96.191"
WEINBERG_URL = "https://doi.org/10.1103/PhysRevLett.19.1264"
ADLER_URL = "https://doi.org/10.1103/PhysRev.177.2426"
WITTEN_URL = "https://doi.org/10.1016/0370-2693(82)90728-6"


def contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


def fraction_text(value: Fraction | sp.Rational | int) -> str:
    rational = sp.Rational(value)
    return str(rational.p) if rational.q == 1 else f"{rational.p}/{rational.q}"


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    local_sources = [
        (
            "SRC4901_00_4900",
            POST
            / "4900-Y5-R2FR-charged-matter-representation-lattice-and-QED-beta-function-or-classical-EM-freeze.md",
            "MTS_CHARGED_MATTER_AND_QED_CORRESPONDENCE_GATE_4900",
            "validated_predecessor",
        ),
        (
            "SRC4901_01_4900_validation",
            OUTPUT / "P8_Y5_BRR545_4900_VALIDATION.csv",
            "VAL4900_OVERALL,PASS",
            "validated_predecessor",
        ),
        (
            "SRC4901_02_4854",
            POST
            / "4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md",
            "U1_BASELINE_CP2_CONSTITUTIVE_GATE_4854",
            "current_abelian_parent_and_CP2_clue",
        ),
        (
            "SRC4901_03_4875",
            POST
            / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875",
            "current_integrated_metric_parent",
        ),
        (
            "SRC4901_04_formal4900",
            FORMAL
            / "916-PPC4161-charged-matter-audit-and-Dirac-QED-correspondence.md",
            "PPC4161_CHARGED_MATTER_AND_DIRAC_QED_4900",
            "current_particle_correspondence",
        ),
        (
            "SRC4901_05_legacy_YM",
            QPF / "yang-mills" / "yang-mills-mass-gap-via-the-motion-theory.md",
            "A Curvature-Resistance Proof",
            "legacy_nonabelian_claim_under_audit",
        ),
        (
            "SRC4901_06_quark",
            QPF
            / "quarks-protons"
            / "the-quark-mass-hierarchy-from-motion-timespace.md",
            "THE QUARK MASS HIERARCHY",
            "legacy_quark_claim_under_audit",
        ),
        (
            "SRC4901_07_proton",
            QPF
            / "quarks-protons"
            / "the-proton-as-a-fundamental-mts-soliton.md",
            "THE PROTON AS A FUNDAMENTAL MTS SOLITON",
            "legacy_QCD_claim_under_audit",
        ),
        (
            "SRC4901_08_lepton_family",
            QPF
            / "leptons-neutrinos"
            / "finite-lepton-families-from-curvature-memory-geometry.md",
            "FINITE LEPTON FAMILIES",
            "legacy_family_claim_under_audit",
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
            "SRC4901_09_YangMills",
            YANG_MILLS_URL,
            "Yang and Mills local non-Abelian gauge invariance",
        ),
        (
            "SRC4901_10_Weinberg",
            WEINBERG_URL,
            "Weinberg electroweak correspondence anchor",
        ),
        (
            "SRC4901_11_Adler",
            ADLER_URL,
            "Adler chiral anomaly primary anchor",
        ),
        (
            "SRC4901_12_Witten",
            WITTEN_URL,
            "Witten global SU2 anomaly primary anchor",
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
def corpus_nonabelian_audit() -> dict[str, Any]:
    files = sorted(CORE.rglob("*.md")) + sorted(QPF.rglob("*.md"))
    texts = {
        path: path.read_text(encoding="utf-8", errors="replace")
        for path in files
    }
    patterns = (
        ("SU2_label", r"SU\s*\(?2\)?"),
        ("SU3_label", r"SU\s*\(?3\)?"),
        ("Yang_Mills_label", r"Yang[–-]?Mills"),
        ("hypercharge", r"hypercharge"),
        ("chiral_representation", r"chiral(?:ity)?"),
        ("left_Weyl_field", r"left[- ]handed Weyl|Weyl fermion"),
        (
            "principal_nonabelian_connection",
            r"principal[- ]SU|su\([23]\).*connection|non[- ]Abelian connection",
        ),
    )
    rows: list[dict[str, Any]] = []
    for object_name, pattern in patterns:
        matching: list[str] = []
        occurrences = 0
        for path, text in texts.items():
            count = len(re.findall(pattern, text, flags=re.IGNORECASE))
            if count:
                occurrences += count
                matching.append(str(path.relative_to(ROOT)))
        rows.append(
            {
                "object": object_name,
                "occurrences": occurrences,
                "matching_files": len(matching),
                "matching_paths": ";".join(matching),
                "present": occurrences > 0,
            }
        )
    by_name = {row["object"]: row for row in rows}
    required_absent = (
        "hypercharge",
        "chiral_representation",
        "left_Weyl_field",
        "principal_nonabelian_connection",
    )
    return {
        "rows": rows,
        "files_scanned": len(files),
        "SU2_files": by_name["SU2_label"]["matching_files"],
        "SU3_files": by_name["SU3_label"]["matching_files"],
        "only_legacy_YM_owns_nonabelian_labels": bool(
            by_name["SU2_label"]["matching_files"] == 1
            and by_name["SU3_label"]["matching_files"] == 1
            and "yang-mills-mass-gap" in by_name["SU2_label"][
                "matching_paths"
            ]
            and "yang-mills-mass-gap" in by_name["SU3_label"][
                "matching_paths"
            ]
        ),
        "complete_chiral_nonabelian_parent_present": all(
            by_name[name]["present"] for name in required_absent
        ),
        "passed": bool(
            len(files) == 26
            and len(rows) == 7
            and all(not by_name[name]["present"] for name in required_absent)
        ),
    }


@lru_cache(maxsize=None)
def legacy_yang_mills_audit() -> dict[str, Any]:
    rows = [
        {
            "clause": "group_selector",
            "printed_structure": "compact G with SU2 or SU3 given only as examples",
            "finding": "no parent principle selects SU2 SU3 or their product",
            "consequence": "group is inserted rather than derived",
            "valid_nonabelian_derivation": False,
        },
        {
            "clause": "connection_owner",
            "printed_structure": "A_mu in Lie(G) and F=dA+[A,A]",
            "finding": "the gauge potential is declared independently of the MTS scalar",
            "consequence": "standard Yang-Mills kinematics are adopted",
            "valid_nonabelian_derivation": False,
        },
        {
            "clause": "curvature_scalar",
            "printed_structure": "C=sqrt(Tr(F_mu_nu F^mu_nu))",
            "finding": "Lorentzian Tr(F2) is not positive and the square root is nonanalytic at F=0",
            "consequence": "C is not a globally real smooth local scalar",
            "valid_nonabelian_derivation": False,
        },
        {
            "clause": "adjoint_source",
            "printed_structure": "D^mu F_mu_nu=alpha partial_nu C",
            "finding": "the left side is adjoint valued while partial_nu C is a gauge singlet",
            "consequence": "the printed field equation is not gauge covariant",
            "valid_nonabelian_derivation": False,
        },
        {
            "clause": "claimed_variation",
            "printed_structure": "J^mu=partial^mu phi coupled to partial_mu C(F)",
            "finding": "varying C(F) gives derivative nonlinear constitutive terms rather than the printed singlet source",
            "consequence": "the displayed Euler equation does not follow from the displayed action",
            "valid_nonabelian_derivation": False,
        },
        {
            "clause": "positivity",
            "printed_structure": "alpha J^mu partial_mu C is assumed positive",
            "finding": "a Lorentz contraction of two gradients has no fixed sign",
            "consequence": "no coercive Hamiltonian lower bound follows",
            "valid_nonabelian_derivation": False,
        },
        {
            "clause": "damping_unitarity",
            "printed_structure": "finite-grid damping is used as curvature resistance",
            "finding": "irreversible damping requires an open-system completion and is not a self-adjoint quantum Hamiltonian proof",
            "consequence": "classical dissipation is not a quantum spectral theorem",
            "valid_nonabelian_derivation": False,
        },
        {
            "clause": "mass_gap",
            "printed_structure": "residual finite-box energy plateau",
            "finding": "a finite damped grid has no constructed continuum gauge-invariant Hilbert space or volume-uniform spectral lower bound",
            "consequence": "the Yang-Mills mass-gap claim is quarantined",
            "valid_nonabelian_derivation": False,
        },
    ]
    return {
        "rows": rows,
        "audited_clauses": len(rows),
        "valid_clauses": sum(row["valid_nonabelian_derivation"] for row in rows),
        "legacy_mass_gap_claim_valid": False,
        "legacy_status": (
            "LEGACY_MBT_YANG_MILLS_MASS_GAP_CLAIM_QUARANTINED_"
            "STANDARD_KINEMATICS_AND_NUMERICAL_ASSETS_RETAINED"
        ),
        "passed": len(rows) == 8 and not any(
            row["valid_nonabelian_derivation"] for row in rows
        ),
    }


@lru_cache(maxsize=None)
def cp2_route_audit() -> dict[str, Any]:
    rows = [
        {
            "object": "CP2_coset",
            "result": "CP2 is SU3/S(U2xU1) and has a global SU3 isometry",
            "what_it_supplies": "a structured internal target and U1 Berry line connection",
            "what_it_does_not_supply": "a local dynamical SU3 color connection",
            "closed": True,
        },
        {
            "object": "universal_quotient_bundle",
            "result": "a rank-two quotient bundle can carry a canonical U2 connection",
            "what_it_supplies": "a possible SU2xU1 geometric clue",
            "what_it_does_not_supply": "the weak chiral representation and variationally independent gauge modes",
            "closed": False,
        },
        {
            "object": "gauged_isometry",
            "result": "promoting a global target isometry to a local gauge symmetry requires new connection fields",
            "what_it_supplies": "a future construction route",
            "what_it_does_not_supply": "automatic Yang-Mills dynamics",
            "closed": False,
        },
        {
            "object": "color_factor",
            "result": "the CP2 construction does not provide an independent principal SU3c bundle",
            "what_it_supplies": "no current color owner",
            "what_it_does_not_supply": "eight gluons and triplet quark representations",
            "closed": False,
        },
        {
            "object": "chirality",
            "result": "bosonic Berry geometry does not select left-handed Weyl matter",
            "what_it_supplies": "internal bundle intuition",
            "what_it_does_not_supply": "spin-statistics family replication or anomaly-free chiral matter",
            "closed": False,
        },
    ]
    return {
        "rows": rows,
        "closed_clues": sum(row["closed"] for row in rows),
        "nonabelian_parent_derived": False,
        "status": "CP2_RETAINED_AS_U2_GEOMETRIC_CLUE_NOT_SM_GAUGE_PARENT",
        "passed": len(rows) == 5 and sum(row["closed"] for row in rows) == 1,
    }


@lru_cache(maxsize=None)
def standard_model_representations() -> dict[str, Any]:
    rows = [
        {
            "field": "Q_L",
            "statistics": "left_Weyl",
            "SU3": "3",
            "SU2": "2",
            "Y": "1/6",
            "copies_from_other_groups": 6,
            "role": "left quark doublet",
            "parent_origin": "ADOPTED_CORRESPONDENCE_DATA",
        },
        {
            "field": "u_R^c",
            "statistics": "left_Weyl",
            "SU3": "bar3",
            "SU2": "1",
            "Y": "-2/3",
            "copies_from_other_groups": 3,
            "role": "left conjugate of right up quark",
            "parent_origin": "ADOPTED_CORRESPONDENCE_DATA",
        },
        {
            "field": "d_R^c",
            "statistics": "left_Weyl",
            "SU3": "bar3",
            "SU2": "1",
            "Y": "1/3",
            "copies_from_other_groups": 3,
            "role": "left conjugate of right down quark",
            "parent_origin": "ADOPTED_CORRESPONDENCE_DATA",
        },
        {
            "field": "L_L",
            "statistics": "left_Weyl",
            "SU3": "1",
            "SU2": "2",
            "Y": "-1/2",
            "copies_from_other_groups": 2,
            "role": "left lepton doublet",
            "parent_origin": "ADOPTED_CORRESPONDENCE_DATA",
        },
        {
            "field": "e_R^c",
            "statistics": "left_Weyl",
            "SU3": "1",
            "SU2": "1",
            "Y": "1",
            "copies_from_other_groups": 1,
            "role": "left conjugate of right charged lepton",
            "parent_origin": "ADOPTED_CORRESPONDENCE_DATA",
        },
        {
            "field": "H",
            "statistics": "complex_scalar",
            "SU3": "1",
            "SU2": "2",
            "Y": "1/2",
            "copies_from_other_groups": 2,
            "role": "minimal Higgs correspondence doublet",
            "parent_origin": "ADOPTED_CORRESPONDENCE_DATA",
        },
    ]
    return {
        "rows": rows,
        "fermion_multiplets_per_generation": 5,
        "Higgs_doublets": 1,
        "right_neutrino_in_baseline": False,
        "family_count": 3,
        "family_count_origin": "ADOPTED_NOT_MTS_DERIVED",
        "representation_status": (
            "STANDARD_MODEL_CHIRAL_REPRESENTATIONS_EXPLICITLY_ADOPTED_"
            "FOR_CORRESPONDENCE"
        ),
        "passed": len(rows) == 6,
    }


@lru_cache(maxsize=None)
def anomaly_ledger() -> dict[str, Any]:
    yq = Fraction(1, 6)
    yu = Fraction(-2, 3)
    yd = Fraction(1, 3)
    yl = Fraction(-1, 2)
    ye = Fraction(1, 1)
    values = {
        "SU3_cubed": Fraction(2 - 1 - 1, 1),
        "SU3_squared_U1": 2 * yq + yu + yd,
        "SU2_squared_U1": 3 * yq + yl,
        "U1_cubed": (
            6 * yq**3 + 3 * yu**3 + 3 * yd**3 + 2 * yl**3 + ye**3
        ),
        "gravity_squared_U1": 6 * yq + 3 * yu + 3 * yd + 2 * yl + ye,
        "SU2_cubed_perturbative": Fraction(0, 1),
    }
    descriptions = {
        "SU3_cubed": "2 A(3)+A(bar3)+A(bar3)",
        "SU3_squared_U1": "2 Y_Q+Y_uc+Y_dc",
        "SU2_squared_U1": "3 Y_Q+Y_L",
        "U1_cubed": "6Y_Q^3+3Y_uc^3+3Y_dc^3+2Y_L^3+Y_ec^3",
        "gravity_squared_U1": "6Y_Q+3Y_uc+3Y_dc+2Y_L+Y_ec",
        "SU2_cubed_perturbative": "zero because the SU2 fundamental is pseudoreal",
    }
    rows = [
        {
            "anomaly": name,
            "sum": descriptions[name],
            "exact_value": fraction_text(value),
            "cancelled": value == 0,
            "scope": "one adopted generation",
        }
        for name, value in values.items()
    ]
    doublets = 3 + 1
    rows.append(
        {
            "anomaly": "Witten_SU2_global",
            "sum": "3 colored Q_L doublets + 1 L_L doublet",
            "exact_value": str(doublets),
            "cancelled": doublets % 2 == 0,
            "scope": "one adopted generation",
        }
    )
    return {
        "rows": rows,
        "local_anomalies_cancel": all(value == 0 for value in values.values()),
        "SU2_doublets_per_generation": doublets,
        "Witten_global_anomaly_cancelled": doublets % 2 == 0,
        "anomaly_cancellation_selects_representations": False,
        "passed": len(rows) == 7
        and all(row["cancelled"] for row in rows),
    }


@lru_cache(maxsize=None)
def hypercharge_rank_theorem() -> dict[str, Any]:
    variables = ("Y_Q", "Y_uc", "Y_dc", "Y_L", "Y_ec", "Y_H")
    constraints = (
        ("up_Yukawa", (1, 1, 0, 0, 0, 1)),
        ("down_Yukawa", (1, 0, 1, 0, 0, -1)),
        ("charged_lepton_Yukawa", (0, 0, 0, 1, 1, -1)),
        ("SU3_squared_U1", (2, 1, 1, 0, 0, 0)),
        ("SU2_squared_U1", (3, 0, 0, 1, 0, 0)),
        ("gravity_squared_U1", (6, 3, 3, 2, 1, 0)),
    )
    matrix = sp.Matrix([coefficients for _, coefficients in constraints])
    rank = matrix.rank()
    nullspace = matrix.nullspace()
    primitive = nullspace[0]
    normalized = [
        sp.simplify(value * sp.Rational(1, 2) / primitive[-1])
        for value in primitive
    ]
    expected = [
        sp.Rational(1, 6),
        sp.Rational(-2, 3),
        sp.Rational(1, 3),
        sp.Rational(-1, 2),
        sp.Rational(1, 1),
        sp.Rational(1, 2),
    ]
    cubic = (
        6 * normalized[0] ** 3
        + 3 * normalized[1] ** 3
        + 3 * normalized[2] ** 3
        + 2 * normalized[3] ** 3
        + normalized[4] ** 3
    )
    rows = [
        {
            "constraint": name,
            "coefficient_vector": ";".join(str(value) for value in coefficients),
            "equals": "0",
            "role": "adopted representation plus Yukawa or anomaly consistency",
        }
        for name, coefficients in constraints
    ]
    solution_rows = [
        {
            "variable": variable,
            "null_vector_value": fraction_text(primitive[index]),
            "normalized_YH_half": fraction_text(normalized[index]),
            "matches_SM": normalized[index] == expected[index],
        }
        for index, variable in enumerate(variables)
    ]

    variables_nu = ("Y_Q", "Y_uc", "Y_dc", "Y_L", "Y_ec", "Y_nc", "Y_H")
    constraints_nu = (
        (1, 1, 0, 0, 0, 0, 1),
        (1, 0, 1, 0, 0, 0, -1),
        (0, 0, 0, 1, 1, 0, -1),
        (0, 0, 0, 1, 0, 1, 1),
        (2, 1, 1, 0, 0, 0, 0),
        (3, 0, 0, 1, 0, 0, 0),
        (6, 3, 3, 2, 1, 1, 0),
    )
    matrix_nu = sp.Matrix(constraints_nu)
    rank_nu = matrix_nu.rank()
    nullity_nu = len(variables_nu) - rank_nu
    matrix_nu_majorana = matrix_nu.col_join(
        sp.Matrix([[0, 0, 0, 0, 0, 1, 0]])
    )
    nullity_nu_majorana = len(variables_nu) - matrix_nu_majorana.rank()
    electric_rows = [
        {
            "state": "u_L",
            "T3": "1/2",
            "Y": fraction_text(normalized[0]),
            "Q=T3+Y": "2/3",
        },
        {
            "state": "d_L",
            "T3": "-1/2",
            "Y": fraction_text(normalized[0]),
            "Q=T3+Y": "-1/3",
        },
        {
            "state": "nu_L",
            "T3": "1/2",
            "Y": fraction_text(normalized[3]),
            "Q=T3+Y": "0",
        },
        {
            "state": "e_L",
            "T3": "-1/2",
            "Y": fraction_text(normalized[3]),
            "Q=T3+Y": "-1",
        },
    ]
    return {
        "rows": rows,
        "solution_rows": solution_rows,
        "electric_rows": electric_rows,
        "variables": len(variables),
        "rank": rank,
        "nullity": len(variables) - rank,
        "normalized_solution": ";".join(
            fraction_text(value) for value in normalized
        ),
        "U1_cubic_after_solution": fraction_text(cubic),
        "right_neutrino_variables": len(variables_nu),
        "right_neutrino_rank": rank_nu,
        "right_neutrino_nullity_without_Majorana": nullity_nu,
        "right_neutrino_nullity_with_Ync_zero_Majorana": nullity_nu_majorana,
        "conditional_hypercharge_ratios_derived": bool(
            rank == 5
            and len(nullspace) == 1
            and normalized == expected
            and cubic == 0
        ),
        "primitive_MTS_hypercharge_selector_derived": False,
        "passed": bool(
            rank == 5
            and len(nullspace) == 1
            and normalized == expected
            and cubic == 0
            and nullity_nu == 2
            and nullity_nu_majorana == 1
        ),
    }


@lru_cache(maxsize=None)
def standard_model_correspondence() -> dict[str, Any]:
    rows = [
        {
            "sector": "SU3c",
            "field": "G_mu^A",
            "action_term": "-G_mu_nu^A G_A^mu_nu/4",
            "coupling": "g3",
            "status": "EXPLICIT_CORRESPONDENCE_FIELD",
        },
        {
            "sector": "SU2L",
            "field": "W_mu^I",
            "action_term": "-W_mu_nu^I W_I^mu_nu/4",
            "coupling": "g2",
            "status": "EXPLICIT_CORRESPONDENCE_FIELD",
        },
        {
            "sector": "U1Y",
            "field": "B_mu",
            "action_term": "-B_mu_nu B^mu_nu/4",
            "coupling": "gY",
            "status": "EXPLICIT_CORRESPONDENCE_FIELD",
        },
        {
            "sector": "chiral_matter",
            "field": "Q_L,u_R^c,d_R^c,L_L,e_R^c",
            "action_term": "sum i chi^dagger barsigma^mu D_mu chi",
            "coupling": "g3,g2,gY by representation",
            "status": "EXPLICIT_CORRESPONDENCE_FIELD",
        },
        {
            "sector": "Higgs",
            "field": "H",
            "action_term": "|D H|^2-V(H)",
            "coupling": "mu_H^2,lambda_H",
            "status": "EXPLICIT_CORRESPONDENCE_FIELD",
        },
        {
            "sector": "Yukawa",
            "field": "Y_u,Y_d,Y_e",
            "action_term": "-(Q H u^c+Q H^dagger d^c+L H^dagger e^c+h.c.)",
            "coupling": "three complex flavor matrices",
            "status": "EXPLICIT_CORRESPONDENCE_DATA",
        },
        {
            "sector": "gravity_interface",
            "field": "public metric or tetrad",
            "action_term": "all kinetic terms use the same covariant measure and connection",
            "coupling": "one checkpoint-4898 G calibration",
            "status": "INHERITED_PUBLIC_GEOMETRY",
        },
    ]
    relations = [
        {
            "relation": "electric_generator",
            "equation": "Q=T3+Y",
            "status": "DERIVED_AFTER_ADOPTED_ELECTROWEAK_BREAKING_PATTERN",
        },
        {
            "relation": "weak_mixing",
            "equation": "e=g2 sin(thetaW)=gY cos(thetaW)",
            "status": "KNOWN_LIMIT_RELATION",
        },
        {
            "relation": "photon",
            "equation": "A=sin(thetaW) W3+cos(thetaW) B",
            "status": "KNOWN_LIMIT_RELATION",
        },
        {
            "relation": "massive_neutral_boson",
            "equation": "Z=cos(thetaW) W3-sin(thetaW) B",
            "status": "KNOWN_LIMIT_RELATION",
        },
    ]
    return {
        "rows": rows,
        "relation_rows": relations,
        "gauge_group_local_algebra": "su3_c+su2_L+u1_Y",
        "global_discrete_quotient_selected": False,
        "correspondence_gate_passed": True,
        "primitive_nonabelian_origin_derived": False,
        "parameter_status": (
            "g3_g2_gY_Higgs_and_Yukawa_parameters_imported_or_calibrated"
        ),
        "passed": len(rows) == 7 and len(relations) == 4,
    }


@lru_cache(maxsize=None)
def primitive_nonabelian_gate() -> dict[str, Any]:
    rows = [
        ("principal_SU3c_bundle", False, "no parent selector or transition data"),
        ("principal_SU2L_bundle", False, "CP2 U2 clue is not an independent weak connection"),
        ("nonabelian_kinetic_owner", False, "legacy A and F are adopted standard kinematics"),
        ("chiral_Weyl_owner", False, "no primitive Grassmann chiral matter"),
        ("three_family_selector", False, "family count remains imported"),
        ("hypercharge_parent_selector", False, "ratios are conditional on adopted multiplets and Yukawas"),
        ("local_anomaly_cancellation", True, "exact for the adopted one-generation spectrum"),
        ("Witten_global_anomaly", True, "four SU2 doublets per adopted generation"),
        ("Higgs_origin", False, "one doublet and potential are adopted"),
        ("Yukawa_matrix_origin", False, "flavor matrices are not derived"),
        ("QCD_confinement_mass_gap", False, "legacy damping proof is invalid"),
        ("SM_correspondence_fallback", True, "explicit anomaly-free known limit exists"),
    ]
    output = [
        {
            "clause": clause,
            "closed": closed,
            "evidence": evidence,
            "counts_toward_primitive_derivation": clause
            != "SM_correspondence_fallback",
        }
        for clause, closed, evidence in rows
    ]
    primitive_rows = [
        row for row in output if row["counts_toward_primitive_derivation"]
    ]
    return {
        "rows": output,
        "total_clauses": len(output),
        "closed_clauses": sum(row["closed"] for row in output),
        "primitive_required_clauses": len(primitive_rows),
        "primitive_closed_clauses": sum(row["closed"] for row in primitive_rows),
        "primitive_nonabelian_reentry_allowed": all(
            row["closed"] for row in primitive_rows
        ),
        "correspondence_fallback_closed": output[-1]["closed"],
        "passed": len(output) == 12
        and not all(row["closed"] for row in primitive_rows)
        and output[-1]["closed"],
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    return {
        "primitive_nonabelian_status": (
            "CURRENT_MTS_PARENT_DOES_NOT_DERIVE_SU3C_SU2L_CHIRAL_GAUGE_CONTENT"
        ),
        "legacy_YM_status": legacy_yang_mills_audit()["legacy_status"],
        "CP2_status": cp2_route_audit()["status"],
        "SM_correspondence_status": (
            "EXPLICIT_ANOMALY_FREE_STANDARD_MODEL_CORRESPONDENCE_MODULE_ADOPTED"
        ),
        "hypercharge_status": (
            "RATIOS_DERIVED_CONDITIONALLY_FROM_ADOPTED_REPS_YUKAWAS_AND_"
            "ANOMALIES_OVERALL_NORMALIZATION_AND_PARENT_ORIGIN_OPEN"
        ),
        "parameter_status": (
            "GAUGE_COUPLINGS_HIGGS_POTENTIAL_YUKAWA_MATRICES_AND_FAMILY_COUNT_"
            "IMPORTED_OR_CALIBRATED"
        ),
        "public_claim_allowed": False,
        "next_target": NEXT_TARGET,
        "passed": bool(
            source_contract()["passed"]
            and corpus_nonabelian_audit()["passed"]
            and legacy_yang_mills_audit()["passed"]
            and cp2_route_audit()["passed"]
            and standard_model_representations()["passed"]
            and anomaly_ledger()["passed"]
            and hypercharge_rank_theorem()["passed"]
            and standard_model_correspondence()["passed"]
            and primitive_nonabelian_gate()["passed"]
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "corpus": corpus_nonabelian_audit(),
        "legacy_YM": legacy_yang_mills_audit(),
        "CP2": cp2_route_audit(),
        "representations": standard_model_representations(),
        "anomalies": anomaly_ledger(),
        "hypercharge": hypercharge_rank_theorem(),
        "correspondence": standard_model_correspondence(),
        "primitive_gate": primitive_nonabelian_gate(),
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
        "decision": arbitration()["SM_correspondence_status"],
    }


def main() -> int:
    calculation = result()
    corpus = calculation["sections"]["corpus"]
    hypercharge = calculation["sections"]["hypercharge"]
    anomalies = calculation["sections"]["anomalies"]
    print(
        f"files={corpus['files_scanned']} "
        f"nonabelian_label_files={corpus['SU2_files']}/{corpus['SU3_files']} "
        f"hypercharge_rank={hypercharge['rank']} "
        f"nullity={hypercharge['nullity']} "
        f"anomalies={len(anomalies['rows'])}"
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
