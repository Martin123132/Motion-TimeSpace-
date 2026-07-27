from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4964"

RESULT_JSON = SOURCE / "four_derivative_quotient_CFF_p8_results.json"
QUOTIENT_CSV = SOURCE / "four_derivative_field_redefinition_quotient.csv"
PARAMETER_CSV = SOURCE / "finite_matching_parameter_count.csv"
CFF_CSV = SOURCE / "CFF_one_LEC_calibration_contract.csv"
P8_CSV = SOURCE / "p8plus_tail_norm_gate.csv"
DECISION_CSV = SOURCE / "compact_all_operator_decision.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4964_R2C2_QUOTIENT_CFF_LEC_P8_TAIL"
CHECKED_DATE = "2026-07-13"

C_LIGHT = 299_792_458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054_571_817e-34
M_SUN_KG = 1.98847e30
PLANCK_LENGTH_M = math.sqrt(HBAR * G_NEWTON / C_LIGHT**3)
SOLAR_MASS_LENGTH_M = G_NEWTON * M_SUN_KG / C_LIGHT**2
COMPACT_RESIDUAL_GATE = 0.01

SOURCE_PATHS = {
    "parent_action_4876": POST
    / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
    "strict_EFT_4878": POST
    / "4878-Y5-R2FR-renormalized-EFT-local-limit-and-arena-specific-nonlocal-residual-bounds-to-R10-PPN-clocks-orbit-and-Maxwell.md",
    "Einstein_branch_4880": POST
    / "4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-domain-of-validity-and-strong-field-entry-gate.md",
    "contact_ownership_4884": POST
    / "4884-Y5-R2FR-strong-matter-contact-coefficient-parent-ownership-or-observational-bound-projection-gate.md",
    "closed_bath_4918": POST
    / "4918-Y5-R2FR-closed-bath-state-enthalpy-trace-profile-and-renormalized-aC-aR-matching-or-multiarena-bound.md",
    "photon_coordinates_4932": POST
    / "4932-Y5-R2FR-MTS-gauge-portal-functional-trace-projection-or-two-sided-polarization-likelihood.md",
    "CFF_matching_4944": POST
    / "4944-Y5-R2FR-complete-electroweak-spin1-and-hadronic-CFF-matching-or-total-photon-residual-bound.md",
    "CFF_geometry_4945": POST
    / "4945-Y5-R2FR-primary-two-sided-CFF-likelihood-or-QCD-TJJ-dispersion-bound-and-local-Maxwell-certificate.md",
    "CFF_no_go_4946": POST
    / "4946-Y5-R2FR-QCD-TJJ-dispersive-matching-and-weak-local-Maxwell-action-certificate.md",
    "CFF_geometry_table_4945": POST
    / "source-intake"
    / "functional_rg"
    / "4945"
    / "geometry_corrected_local_CFF_projection.csv",
    "CFF_no_go_table_4946": POST
    / "source-intake"
    / "functional_rg"
    / "4946"
    / "QCD_TJJ_observable_nonidentifiability_gate.csv",
    "CFF_Maxwell_table_4946": POST
    / "source-intake"
    / "functional_rg"
    / "4946"
    / "local_Maxwell_action_stress_and_calibration_certificate.csv",
    "CFF_transfer_4946": POST
    / "source-intake"
    / "functional_rg"
    / "4946"
    / "universal_CFF_calibration_transfer_functions.csv",
    "CFF_results_4946": POST
    / "source-intake"
    / "functional_rg"
    / "4946"
    / "QCD_TJJ_no_go_lattice_and_Maxwell_results.json",
    "EOS_4962": POST
    / "source-intake"
    / "functional_rg"
    / "4962"
    / "realistic_EOS_scalar_stability_transfer.csv",
    "response_benchmarks_4883": POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_R2FR_4883_RESPONSE_BENCHMARKS.csv",
    "C3_results_4963": POST
    / "source-intake"
    / "functional_rg"
    / "4963"
    / "strong_field_C3_and_scalar_branch_results.json",
    "C3_checkpoint_4963": POST
    / "4963-Y5-R2FR-strong-field-C3-Wilson-selection-and-global-scalar-branch-exclusion-or-compact-GR-finite-residual.md",
}

EXPECTED_HASHES = {
    "parent_action_4876": "8798d2de8c48ccd4fcc22d676aa1ae37cb6ac7691a579f9444095a8302832780",
    "strict_EFT_4878": "f60ee9ddb790b0501b161243ad348a405f0d8c4a55d5029349c544c5e00834b2",
    "Einstein_branch_4880": "b4966159301e6c6c7fac6d618c509be5ad04d1a7ff83522eb3b3b0899cb14df0",
    "contact_ownership_4884": "78c179fe6419ba25d7568d8fc5eedd843f5837133eb8a2903ef2036444e878cc",
    "closed_bath_4918": "b7e5c191e4e08f07500f091a8d78383306c9b1a835cf115491789f4a0ea9a53e",
    "photon_coordinates_4932": "258bbd44e21791089db5fdebdb8ce100772ef1b2e5c626834a1a3c655bac0081",
    "CFF_matching_4944": "0082f96830d4a3cdb75a27b55a8382ac4ba6bb75811eea655723629e4a523dd9",
    "CFF_geometry_4945": "296c5567169674d953dd44782cf2b21ce7f2bae9f9651cef6e7ced7d483e961e",
    "CFF_no_go_4946": "4985b31aa5d5253ec64fd1575bbd0f844c1b5c0924a11482fb77374ddee477b6",
    "CFF_geometry_table_4945": "89d425abb47dbfda188f8fdb470a205bb46a00518a1ea48c01822f0ade67825a",
    "CFF_no_go_table_4946": "c570dbef06650bfc04a80f5eb8ddb52b1832078cf58e68a5838b5a6e271f2f84",
    "CFF_Maxwell_table_4946": "8b80ddf7b5cb469fa7c580b24f6b0d759322871bfb7064111839565ba290799a",
    "CFF_transfer_4946": "8707daa86fac5daf0bd6859bf8d8c29f18777349c9dbac24e259f729facd15a8",
    "CFF_results_4946": "e0e0f3578574b191ab389edfda6f8a3e09937053aaa945147fb4dd1fbd410041",
    "EOS_4962": "df86b26581b523dcbfa0936c2af65f5d6e10ca4c5d75ac0bbc1b1196fa26a179",
    "response_benchmarks_4883": "8f7a0625d8618bbabecd1b990763dd32018ea34642c2867913c136fd5cbf1454",
    "C3_results_4963": "059b52fe849ea13082f5ad86221c85009a7595637e0ad0415b3ea59cbb37a791",
    "C3_checkpoint_4963": "ea2df6892c729fc3c49eb00074eb2d999c426c18046db60aa1f963b8cc9fcc48",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        fields.extend(key for key in row if key not in fields)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def truth(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def derive_four_derivative_quotient() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    a_R, a_C, M_R2 = sp.symbols("a_R a_C M_R2", nonzero=True)
    ricci_squared, scalar_squared, euler_4 = sp.symbols(
        "Ricci2 R2 E4"
    )
    stress_squared, trace_squared = sp.symbols("Tmn2 T2")

    c_squared = euler_4 + 2 * ricci_squared - sp.Rational(2, 3) * scalar_squared
    local_non_topological = sp.expand(a_R * scalar_squared + a_C * (c_squared - euler_4))

    alpha = -2 * a_C
    beta = a_R + sp.Rational(1, 3) * a_C
    delta_eh = sp.expand(
        alpha * (ricci_squared - scalar_squared / 2) - beta * scalar_squared
    )
    cancellation = sp.simplify(local_non_topological + delta_eh)

    stress_ricci = (stress_squared - trace_squared / 2) / M_R2
    scalar_curvature = -sp.Symbol("T") / M_R2
    stress_trace = sp.Symbol("T")
    delta_matter = sp.expand(
        -(alpha * stress_ricci + beta * stress_trace * scalar_curvature) / M_R2
    ).subs(sp.Symbol("T") ** 2, trace_squared)
    expected_contact = (
        2 * a_C * stress_squared
        + (a_R - sp.Rational(2, 3) * a_C) * trace_squared
    ) / M_R2**2
    contact_difference = sp.simplify(delta_matter - expected_contact)

    rows = tagged(
        [
            {
                "quotient_id": "Q4964_00_4D_identity",
                "statement": "C_mnrs C^mnrs=E4+2 R_mn R^mn-(2/3)R^2",
                "calculation": str(c_squared),
                "scope": "four dimensions; local bulk action",
                "passed": True,
                "status": "EXACT_4D_CURVATURE_IDENTITY",
            },
            {
                "quotient_id": "Q4964_01_inverse_metric_shift",
                "statement": "delta g^mn=(2/M_R^2)[-2a_C R^mn+(a_R+a_C/3)R g^mn]",
                "calculation": f"alpha={alpha}; beta={beta}",
                "scope": "local perturbatively invertible field redefinition at first EFT order",
                "passed": True,
                "status": "FIELD_REDEFINITION_CONSTRUCTED",
            },
            {
                "quotient_id": "Q4964_02_EH_cancellation",
                "statement": "delta S_EH cancels a_R R^2+a_C C^2 modulo E4 and boundary terms",
                "calculation": f"non_topological={local_non_topological}; delta_EH={delta_eh}; sum={cancellation}",
                "scope": "O(a_R,a_C); p4 local pure-gravity bulk sector",
                "passed": cancellation == 0,
                "status": "EXACT_SYMBOLIC_CANCELLATION",
            },
            {
                "quotient_id": "Q4964_03_matter_contact",
                "statement": "Delta L_contact=[2a_C T_mnT^mn+(a_R-2a_C/3)T^2]/M_R^4",
                "calculation": f"difference_from_expected={contact_difference}",
                "scope": "leading Einstein equation; local matter support; first EFT order",
                "passed": contact_difference == 0,
                "status": "INVARIANT_CONTACT_PACKET_DERIVED",
            },
            {
                "quotient_id": "Q4964_04_vacuum_observable_count",
                "statement": "a_R and a_C supply zero independent on-shell neutral-vacuum p4 observables at first EFT order",
                "calculation": "two basis coefficients map to EOM-redundant terms plus E4/boundary",
                "scope": "positive-gap scattering and exterior vacuum; not resummed quadratic gravity",
                "passed": cancellation == 0,
                "status": "PURE_VACUUM_PARAMETER_COUNT_REDUCED_2_TO_0",
            },
            {
                "quotient_id": "Q4964_05_matter_guardrail",
                "statement": "the contact packet must be combined with independent matter/EOS/worldline counterterms before compact observables are predicted",
                "calculation": "field redefinitions preserve observables but redistribute coefficients between gravity and matter bases",
                "scope": "compact interiors, tides, junctions and finite-size worldlines",
                "passed": True,
                "status": "NO_STANDALONE_AR_AC_COMPACT_CLAIM",
            },
            {
                "quotient_id": "Q4964_06_higher_order_guardrail",
                "statement": "the redefinition generates O(a^2), p6-plus and boundary terms and does not remove nonlocal logarithms",
                "calculation": "first-order equivalence theorem only",
                "scope": "strict EFT; not an exact all-operator change of theory",
                "passed": True,
                "status": "HIGHER_ORDER_AND_NONLOCAL_REMAINDER_RETAINED",
            },
        ]
    )

    summary = {
        "C2_identity": str(c_squared),
        "metric_shift_alpha": str(alpha),
        "metric_shift_beta": str(beta),
        "EH_cancellation_remainder": str(cancellation),
        "matter_contact": str(expected_contact),
        "matter_contact_difference": str(contact_difference),
        "independent_neutral_vacuum_p4_parameters": 0,
        "independent_matter_contact_combinations_before_matter_basis_matching": 2,
        "valid_only_at_first_EFT_order": True,
    }
    return rows, summary


def matching_parameter_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "parameter_id": "PAR4964_00_MR2",
                "symbol": "M_R^2",
                "sector": "two-derivative gravity",
                "independent_empirical_inputs": 1,
                "physical_role": "one massless spin-two residue; fixes G_N",
                "ownership": "parent coefficient matched once",
                "current_status": "UNIVERSAL_RESIDUE_DERIVED_VALUE_CALIBRATED",
                "next_action": "none for local universality",
            },
            {
                "parameter_id": "PAR4964_01_R2C2_vacuum",
                "symbol": "a_R,a_C",
                "sector": "four-derivative neutral vacuum gravity",
                "independent_empirical_inputs": 0,
                "physical_role": "EOM-redundant at first EFT order; E4/boundary aside",
                "ownership": "basis coordinates, not two vacuum observables",
                "current_status": "QUOTIENTED_FROM_P4_VACUUM_MATCHING",
                "next_action": "match full matter contact basis only when compact EOS/tidal precision requires it",
            },
            {
                "parameter_id": "PAR4964_02_R2C2_matter",
                "symbol": "2a_C; a_R-2a_C/3 plus matter counterterms",
                "sector": "matter contact/worldline EFT",
                "independent_empirical_inputs": 2,
                "physical_role": "stress-square and trace-square contact directions before independent matter-basis reduction",
                "ownership": "not fixed by pure-gravity matching",
                "current_status": "CONTACT_PACKET_DERIVED_FULL_PHYSICAL_MATCH_OPEN",
                "next_action": "match invariant EOS/worldline combinations rather than a_R and a_C separately",
            },
            {
                "parameter_id": "PAR4964_03_CFF",
                "symbol": "c_IR",
                "sector": "curvature-photon EFT",
                "independent_empirical_inputs": 1,
                "physical_role": "unique retained CP-even Ricci-flat CFF response",
                "ownership": "c_nonQCD+c_QCD^r in one scheme",
                "current_status": "ONE_LEC_CONTRACT_DEFINED_NUMERIC_CALIBRATION_OPEN",
                "next_action": "one TJJ lattice match or one robust curved-photon calibration; never arena retune",
            },
            {
                "parameter_id": "PAR4964_04_C3",
                "symbol": "A_C3^S",
                "sector": "six-derivative vacuum gravity",
                "independent_empirical_inputs": 0,
                "physical_role": "selected local source-scheme coordinate with nonlocal completion required",
                "ownership": "4963 trajectory selection",
                "current_status": "P6_LOCAL_COORDINATE_SELECTED_COMPACT_SAFE",
                "next_action": "combine local running with the physical nonlocal amplitude",
            },
            {
                "parameter_id": "PAR4964_05_p8plus",
                "symbol": "C_8,R_tail",
                "sector": "eight-derivative and higher on-shell gravity",
                "independent_empirical_inputs": 2,
                "physical_role": "aggregate first omitted response norm and coefficient-growth ratio",
                "ownership": "no parent p8 projection or analyticity radius yet",
                "current_status": "CONDITIONAL_NORM_GATE_DERIVED_PARENT_BOUND_OPEN",
                "next_action": "project a minimal Ricci-flat p8 basis and extend the fixed-point trajectory",
            },
            {
                "parameter_id": "PAR4964_06_Wplus_Wminus",
                "symbol": "W_plus,W_minus",
                "sector": "photon quartic F4",
                "independent_empirical_inputs": 0,
                "physical_role": "limits of g_plus/g_minus built from g_F2sq and g_F4",
                "ownership": "4932/4935 photon sector",
                "current_status": "NOT_GRAVITATIONAL_AR_AC",
                "next_action": "do not use these coordinates as finite R2/C2 matching data",
            },
        ]
    )


def CFF_contract_rows(
    no_go_rows: list[dict[str, str]],
    Maxwell_rows: list[dict[str, str]],
    transfer_rows: list[dict[str, str]],
    geometry_rows: list[dict[str, str]],
    CFF_results: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    no_go = next(row for row in no_go_rows if row["gate_id"] == "NG4946_07_no_go")
    action = next(row for row in Maxwell_rows if row["certificate_id"] == "MAX4946_00_action")
    field_equation = next(
        row for row in Maxwell_rows if row["certificate_id"] == "MAX4946_02_field_equation"
    )
    stress = next(row for row in Maxwell_rows if row["certificate_id"] == "MAX4946_04_stress")
    flat_limit = next(row for row in Maxwell_rows if row["certificate_id"] == "MAX4946_06_flat_limit")
    calibration = next(row for row in Maxwell_rows if row["certificate_id"] == "MAX4946_08_calibration")
    transfer = {row["system"]: row for row in transfer_rows}
    geometry = {row["system"]: row for row in geometry_rows}
    non_QCD = CFF_results["matching"]["non_QCD_interval_m2"]

    historical_bound = float(
        geometry["Earth"]["geometry_corrected_historical_abs_cgamma_bound_m2"]
    )
    NS_threshold = float(
        transfer["1.4_solar_mass_12km_neutron_star"][
            "abs_cIR_for_1e_minus_6_split_m2"
        ]
    )
    BH_threshold = float(
        transfer["10_solar_mass_Schwarzschild_horizon"][
            "abs_cIR_for_1e_minus_6_split_m2"
        ]
    )

    rows = tagged(
        [
            {
                "contract_id": "CFF4964_00_basis",
                "statement": action["statement"],
                "numeric_value": "",
                "units": "",
                "valid_for_declared_structure": truth(action["passed"]),
                "valid_for_numeric_CFF_claim": False,
                "status": "ONE_NONREDUNDANT_RICCI_FLAT_CFF_LEC",
                "source_path": str(SOURCE_PATHS["CFF_Maxwell_table_4946"].relative_to(ROOT)),
            },
            {
                "contract_id": "CFF4964_01_no_go",
                "statement": no_go["derivation"],
                "numeric_value": "",
                "units": "",
                "valid_for_declared_structure": truth(no_go["passed"]),
                "valid_for_numeric_CFF_claim": False,
                "status": "LOWER_DATA_CANNOT_IDENTIFY_FINITE_QCD_CONTACT",
                "source_path": str(SOURCE_PATHS["CFF_no_go_table_4946"].relative_to(ROOT)),
            },
            {
                "contract_id": "CFF4964_02_nonQCD_interval",
                "statement": "c_nonQCD interval in the locked 4946 convention",
                "numeric_value": f"[{non_QCD[0]:.16e},{non_QCD[1]:.16e}]",
                "units": "m^2",
                "valid_for_declared_structure": True,
                "valid_for_numeric_CFF_claim": False,
                "status": "NON_QCD_COMPONENT_ASSEMBLED_QCD_REMAINDER_OPEN",
                "source_path": str(SOURCE_PATHS["CFF_results_4946"].relative_to(ROOT)),
            },
            {
                "contract_id": "CFF4964_03_equation_stress",
                "statement": f"{field_equation['statement']}; {stress['statement']}",
                "numeric_value": "one shared c_IR",
                "units": "m^2",
                "valid_for_declared_structure": truth(field_equation["passed"]) and truth(stress["passed"]),
                "valid_for_numeric_CFF_claim": False,
                "status": "PROPAGATION_AND_STRESS_SHARE_ONE_LEC",
                "source_path": str(SOURCE_PATHS["CFF_Maxwell_table_4946"].relative_to(ROOT)),
            },
            {
                "contract_id": "CFF4964_04_flat_Maxwell",
                "statement": flat_limit["statement"],
                "numeric_value": "exact for arbitrary c_IR",
                "units": "",
                "valid_for_declared_structure": truth(flat_limit["passed"]),
                "valid_for_numeric_CFF_claim": True,
                "status": "EXACT_FLAT_MAXWELL_LIMIT",
                "source_path": str(SOURCE_PATHS["CFF_Maxwell_table_4946"].relative_to(ROOT)),
            },
            {
                "contract_id": "CFF4964_05_calibration",
                "statement": calibration["statement"],
                "numeric_value": "not executed",
                "units": "",
                "valid_for_declared_structure": truth(calibration["passed"]),
                "valid_for_numeric_CFF_claim": False,
                "status": "ONE_DATUM_CALIBRATION_CONTRACT_OPEN",
                "source_path": str(SOURCE_PATHS["CFF_Maxwell_table_4946"].relative_to(ROOT)),
            },
            {
                "contract_id": "CFF4964_06_historical_weak_bound",
                "statement": "geometry-corrected historical Earth/Sun envelope; not a physical QCD match",
                "numeric_value": historical_bound,
                "units": "m^2",
                "valid_for_declared_structure": True,
                "valid_for_numeric_CFF_claim": False,
                "status": "CONDITIONAL_WEAK_GEOMETRY_ENVELOPE_ONLY",
                "source_path": str(SOURCE_PATHS["CFF_geometry_table_4945"].relative_to(ROOT)),
            },
            {
                "contract_id": "CFF4964_07_compact_sensitivity",
                "statement": "absolute c_IR producing a 1e-6 polarization split in declared compact transfer functions",
                "numeric_value": f"NS={NS_threshold:.16e};BH={BH_threshold:.16e}",
                "units": "m^2",
                "valid_for_declared_structure": True,
                "valid_for_numeric_CFF_claim": False,
                "status": "TRANSFER_SLOPES_DEFINED_PHYSICAL_COEFFICIENT_OPEN",
                "source_path": str(SOURCE_PATHS["CFF_transfer_4946"].relative_to(ROOT)),
            },
        ]
    )

    summary = {
        "retained_independent_CFF_LECs": 1,
        "non_QCD_interval_m2": non_QCD,
        "physical_cIR_calibrated": CFF_results["local_Maxwell"][
            "physical_CFF_coefficient_calibrated"
        ],
        "flat_Maxwell_exact": CFF_results["local_Maxwell"]["flat_Maxwell_limit_exact"],
        "historical_weak_geometry_bound_m2": historical_bound,
        "NS_cIR_for_1e_minus_6_split_m2": NS_threshold,
        "BH_cIR_for_1e_minus_6_split_m2": BH_threshold,
    }
    return rows, summary


def p8_tail_rows(
    EOS_rows: list[dict[str, str]],
    response_rows: list[dict[str, str]],
    C3_results: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    response_map = {(row["eos_id"], row["model_id"]): row for row in response_rows}
    objects: list[dict[str, Any]] = []
    for row in EOS_rows:
        key = (row["eos_id"], row["model_id"])
        if key not in response_map:
            raise RuntimeError(f"missing 4883 response benchmark for {key}")
        response = response_map[key]
        if not math.isclose(
            float(row["mass_Msun"]), float(response["mass"]), rel_tol=1.0e-12
        ) or not math.isclose(
            float(row["radius_km"]), float(response["radius_km"]), rel_tol=1.0e-12
        ):
            raise RuntimeError(f"4962/4883 compact benchmark mismatch for {key}")
        objects.append(
            {
                "object_id": f"{row['eos_id']}_{row['model_id']}",
                "source_class": "realistic_EOS_star",
                "mass_Msun": float(row["mass_Msun"]),
                "radius_m": 1000.0 * float(row["radius_km"]),
                "source_path": str(SOURCE_PATHS["EOS_4962"].relative_to(ROOT)),
            }
        )

    objects.extend(
        [
            {
                "object_id": "declared_1p4_Msun_12km",
                "source_class": "declared_compact_benchmark",
                "mass_Msun": 1.4,
                "radius_m": 12_000.0,
                "source_path": str(SOURCE_PATHS["C3_checkpoint_4963"].relative_to(ROOT)),
            },
            {
                "object_id": "10_Msun_Schwarzschild_horizon",
                "source_class": "vacuum_black_hole_proxy",
                "mass_Msun": 10.0,
                "radius_m": 2.0 * 10.0 * SOLAR_MASS_LENGTH_M,
                "source_path": str(SOURCE_PATHS["C3_checkpoint_4963"].relative_to(ROOT)),
            },
        ]
    )

    selected_A_abs = float(C3_results["C3_selection"]["selected_A_C3_abs_max"])
    C6_response = 140.0 * 16.0 * math.pi * selected_A_abs
    rows: list[dict[str, Any]] = []
    numeric_rows: list[dict[str, Any]] = []
    for obj in objects:
        mass_length = obj["mass_Msun"] * SOLAR_MASS_LENGTH_M
        chi = PLANCK_LENGTH_M**2 * mass_length / obj["radius_m"] ** 3
        C8_budget_unit_growth = COMPACT_RESIDUAL_GATE * (1.0 - chi) / chi**3
        C8_budget_half_radius = (
            COMPACT_RESIDUAL_GATE * (1.0 - 0.5) / chi**3
        )
        response_length = PLANCK_LENGTH_M * C8_budget_unit_growth ** (1.0 / 6.0)
        row = {
            "row_type": "compact_object_gate",
            "object_id": obj["object_id"],
            "source_class": obj["source_class"],
            "mass_Msun": obj["mass_Msun"],
            "radius_m": obj["radius_m"],
            "mass_length_m": mass_length,
            "chi_lP2_curvature": chi,
            "epsilon_gate": COMPACT_RESIDUAL_GATE,
            "C8_max_if_R_equals_1": C8_budget_unit_growth,
            "C8_max_if_Rchi_equals_half": C8_budget_half_radius,
            "response_equivalent_length_at_R1_m": response_length,
            "selected_C6_response_norm": C6_response,
            "C8_budget_to_selected_C6_ratio": C8_budget_unit_growth / C6_response,
            "conditional_tail_formula": "epsilon_p8plus<=C8*chi^3/(1-R*chi), R*chi<1",
            "parent_C8_bound_available": False,
            "parent_R_bound_available": False,
            "valid_for_conditional_tail_gate": True,
            "valid_for_all_operator_compact_GR": False,
            "status": "P8_COEFFICIENT_BUDGET_DERIVED_PARENT_NORM_OPEN",
            "source_path": obj["source_path"],
        }
        numeric_rows.append(row)
        rows.append(row)

    rows.extend(
        [
            {
                "row_type": "tail_theorem",
                "object_id": "geometric_response_norm",
                "conditional_tail_formula": "if C_n<=C8 R^(n-4), then sum_(n>=4) C_n chi^(n-1)<=C8 chi^3/(1-R chi)",
                "parent_C8_bound_available": False,
                "parent_R_bound_available": False,
                "valid_for_conditional_tail_gate": True,
                "valid_for_all_operator_compact_GR": False,
                "status": "EXACT_CONDITIONAL_GEOMETRIC_SERIES_BOUND",
                "source_path": str(SOURCE_PATHS["C3_checkpoint_4963"].relative_to(ROOT)),
            },
            {
                "row_type": "nonidentifiability_theorem",
                "object_id": "finite_truncation_firewall",
                "conditional_tail_formula": "Gamma_p6 and Gamma_p6+delta c8 O8 have identical p<=6 projections but different p8 observables",
                "parent_C8_bound_available": False,
                "parent_R_bound_available": False,
                "valid_for_conditional_tail_gate": True,
                "valid_for_all_operator_compact_GR": False,
                "status": "P6_DATA_CANNOT_PROVE_P8_TAIL_WITHOUT_UV_INPUT",
                "source_path": str(SOURCE_PATHS["C3_checkpoint_4963"].relative_to(ROOT)),
            },
        ]
    )

    rows = tagged(rows)
    largest_chi_row = max(numeric_rows, key=lambda row: row["chi_lP2_curvature"])
    smallest_budget_row = min(numeric_rows, key=lambda row: row["C8_max_if_R_equals_1"])
    summary = {
        "compact_object_count": len(numeric_rows),
        "largest_chi": largest_chi_row["chi_lP2_curvature"],
        "largest_chi_object": largest_chi_row["object_id"],
        "smallest_C8_budget_R1": smallest_budget_row["C8_max_if_R_equals_1"],
        "smallest_C8_budget_object": smallest_budget_row["object_id"],
        "smallest_response_equivalent_length_R1_m": min(
            row["response_equivalent_length_at_R1_m"] for row in numeric_rows
        ),
        "selected_C6_response_norm": C6_response,
        "tail_formula": "epsilon_p8plus<=C8 chi^3/(1-R chi)",
        "finite_p6_data_identify_p8": False,
        "parent_C8_bound_available": False,
        "parent_R_bound_available": False,
        "all_operator_compact_GR": False,
    }
    return rows, summary


def decision_rows(
    quotient: dict[str, Any], CFF: dict[str, Any], p8: dict[str, Any]
) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "decision_id": "DEC4964_00_R2C2_quotient",
                "question": "Do finite local R2/C2 coefficients remain two independent neutral-vacuum p4 observables?",
                "decision": "NO",
                "reason": "exact first-order local metric redefinition removes them modulo E4/boundary and matter contacts",
                "claim_allowed": True,
            },
            {
                "decision_id": "DEC4964_01_R2C2_vacuum_obstruction",
                "question": "Does unknown finite a_R/a_C matching still block the selected p4 exterior-vacuum GR branch?",
                "decision": "NO_AT_FIRST_EFT_ORDER",
                "reason": "zero independent vacuum quotient parameters; resummed quadratic gravity is a different branch",
                "claim_allowed": quotient["independent_neutral_vacuum_p4_parameters"] == 0,
            },
            {
                "decision_id": "DEC4964_02_matter_contact_matching",
                "question": "Is the full physical compact-matter contact basis numerically matched?",
                "decision": "NO",
                "reason": "the invariant stress contact packet is derived but independent EOS/worldline counterterms remain",
                "claim_allowed": False,
            },
            {
                "decision_id": "DEC4964_03_CFF_count",
                "question": "Is curved-photon propagation/stress governed by one retained universal CFF LEC?",
                "decision": "YES",
                "reason": "one c_IR appears in the action, field equation and Hilbert stress without arena retuning",
                "claim_allowed": CFF["retained_independent_CFF_LECs"] == 1,
            },
            {
                "decision_id": "DEC4964_04_CFF_numeric",
                "question": "Has the physical c_IR including the finite QCD contact been numerically calibrated?",
                "decision": "NO",
                "reason": "4946 proves lower-data nonidentifiability; TJJ lattice or one curved-photon datum is still required",
                "claim_allowed": False,
            },
            {
                "decision_id": "DEC4964_05_p8_tail_formula",
                "question": "Is there an exact conditional norm bound for the p8-plus compact tail?",
                "decision": "YES_CONDITIONAL",
                "reason": p8["tail_formula"],
                "claim_allowed": True,
            },
            {
                "decision_id": "DEC4964_06_p8_parent_bound",
                "question": "Does the current parent supply C8 and convergence-radius bounds?",
                "decision": "NO",
                "reason": "a finite p6 projection cannot identify an independently addable p8 operator",
                "claim_allowed": False,
            },
            {
                "decision_id": "DEC4964_07_order_by_order_compact_GR",
                "question": "Is the selected compact GR branch controlled through the declared local p6 truncation?",
                "decision": "YES_WITHIN_DECLARED_STATIC_P6_DOMAIN",
                "reason": "4962 compact branch plus 4963 C3/scalar gates; R2/C2 vacuum quotient removes the spurious p4 matching obstruction",
                "claim_allowed": True,
            },
            {
                "decision_id": "DEC4964_08_all_operator_compact_GR",
                "question": "Is exact all-operator compact GR proved?",
                "decision": "NO",
                "reason": "p8-plus parent norm, nonlocal completion, rotating/dynamical scalar domain and compact curved-EM calibration remain open",
                "claim_allowed": False,
            },
            {
                "decision_id": "DEC4964_09_full_MTS",
                "question": "Is full MTS established?",
                "decision": "NO",
                "reason": "integrated metric/Diff origin and cross-arena completion remain open",
                "claim_allowed": False,
            },
            {
                "decision_id": "DEC4964_10_next_target",
                "question": "What is the next derivation target?",
                "decision": "P8_RICCI_FLAT_ON_SHELL_BASIS_AND_FLOW_PROJECTION",
                "reason": "CFF is now isolated as one honest calibration LEC; p8 is the remaining derivable compact vacuum tail",
                "claim_allowed": False,
            },
        ]
    )


def provenance_text(
    source_hashes: dict[str, str],
    quotient: dict[str, Any],
    CFF: dict[str, Any],
    p8: dict[str, Any],
) -> str:
    lines = [
        "# 4964 provenance",
        "",
        f"Marker: `{MARKER}`.",
        "",
        "## Method",
        "",
        "- Re-derived the four-dimensional curvature identity and the local inverse-metric field redefinition with exact SymPy rational algebra.",
        "- Used the leading Einstein equation only after the pure-gravity cancellation to derive the invariant matter contact packet.",
        "- Re-read the 4945/4946 CFF no-go, action/stress and universal transfer tables without inventing a QCD matching value.",
        "- Cross-checked all nine 4962 EOS masses/radii against the independent 4883 response table.",
        "- Converted the p8-plus obstruction into an aggregate response-norm theorem and per-object coefficient budgets; no naturalness prior was imposed.",
        "",
        "## Main results",
        "",
        f"- Neutral-vacuum p4 parameter count after the field-redefinition quotient: `{quotient['independent_neutral_vacuum_p4_parameters']}`.",
        f"- Matter contact packet: `{quotient['matter_contact']}`.",
        f"- Retained curved-photon LEC count: `{CFF['retained_independent_CFF_LECs']}`; physical numeric calibration: `{CFF['physical_cIR_calibrated']}`.",
        f"- Compact rows: `{p8['compact_object_count']}`; largest chi: `{p8['largest_chi']:.16e}` at `{p8['largest_chi_object']}`.",
        f"- Tightest unit-growth p8 response budget: `{p8['smallest_C8_budget_R1']:.16e}`.",
        "- The p8 bound is conditional because neither C8 nor the growth radius R is supplied by the current parent trajectory.",
        "",
        "## Source locks",
        "",
    ]
    for name, path in SOURCE_PATHS.items():
        lines.append(
            f"- `{path.relative_to(ROOT)}` — SHA256 `{source_hashes[name]}`"
        )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "This checkpoint removes basis-dependent finite `a_R,a_C` values from the neutral-vacuum first-order matching count. It does not erase matter contact physics, nonlocal form factors, higher-order terms or the resummed quadratic-gravity spectrum. `c_IR` remains one uncalibrated physical LEC. The p8-plus coefficient budget is a conditional theorem, not a parent prediction. Exact all-operator compact GR and full MTS remain false.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    SOURCE.mkdir(parents=True, exist_ok=True)
    missing = [name for name, path in SOURCE_PATHS.items() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source paths: {missing}")

    source_hashes = {name: digest(path) for name, path in SOURCE_PATHS.items()}
    bad_hashes = {
        name: {"expected": EXPECTED_HASHES[name], "actual": actual}
        for name, actual in source_hashes.items()
        if EXPECTED_HASHES.get(name) != actual
    }
    if bad_hashes:
        raise RuntimeError(f"source hash mismatch: {bad_hashes}")

    source_text = {
        name: path.read_text(encoding="utf-8-sig")
        for name, path in SOURCE_PATHS.items()
        if path.suffix.lower() == ".md"
    }
    source_clause_checks = {
        "4878_strict_EFT_contact": all(
            token in source_text["strict_EFT_4878"]
            for token in ("Strict EFT", "contact support", "exterior Yukawa")
        ),
        "4880_Einstein_Bach_flat": all(
            token in source_text["Einstein_branch_4880"]
            for token in ("Every four-dimensional Einstein metric", "Bach tensor", "Euler density")
        ),
        "4884_total_matching_open": all(
            token in source_text["contact_ownership_4884"]
            for token in ("Total renormalized `a_R,a_C`: **not derived**", "contact")
        ),
        "4918_loop_ray_not_total": all(
            token in source_text["closed_bath_4918"]
            for token in ("a_R}{a_C}=\\frac13", "total coefficients remain unknown")
        ),
        "4932_W_coordinates_are_photon_F4": all(
            token in source_text["photon_coordinates_4932"]
            for token in ("g_F2sq", "g_F4", "g_plus =(g_F2sq+g_F4)/2")
        ),
        "4946_CFF_subtraction_and_one_calibration": all(
            token in source_text["CFF_no_go_4946"]
            for token in ("local coefficient is the subtraction constant", "fit c_IR once", "`c_IR` controls propagation and stress")
        ),
        "4963_p8_open": all(
            token in source_text["C3_checkpoint_4963"]
            for token in ("p>=8", "exact all-operator compact GR")
        ),
    }
    if not all(source_clause_checks.values()):
        raise RuntimeError(f"source clause mismatch: {source_clause_checks}")

    no_go_rows = read_csv(SOURCE_PATHS["CFF_no_go_table_4946"])
    Maxwell_rows = read_csv(SOURCE_PATHS["CFF_Maxwell_table_4946"])
    transfer_rows = read_csv(SOURCE_PATHS["CFF_transfer_4946"])
    geometry_rows = read_csv(SOURCE_PATHS["CFF_geometry_table_4945"])
    EOS_rows = read_csv(SOURCE_PATHS["EOS_4962"])
    response_rows = read_csv(SOURCE_PATHS["response_benchmarks_4883"])
    CFF_results = json.loads(SOURCE_PATHS["CFF_results_4946"].read_text(encoding="utf-8"))
    C3_results = json.loads(SOURCE_PATHS["C3_results_4963"].read_text(encoding="utf-8"))

    quotient_rows, quotient_summary = derive_four_derivative_quotient()
    parameter_rows = matching_parameter_rows()
    CFF_rows, CFF_summary = CFF_contract_rows(
        no_go_rows, Maxwell_rows, transfer_rows, geometry_rows, CFF_results
    )
    p8_rows, p8_summary = p8_tail_rows(EOS_rows, response_rows, C3_results)
    decisions = decision_rows(quotient_summary, CFF_summary, p8_summary)

    checks = {
        "all_source_hashes_match": not bad_hashes,
        "all_source_clauses_match": all(source_clause_checks.values()),
        "four_derivative_symbolic_cancellation_exact": quotient_summary[
            "EH_cancellation_remainder"
        ]
        == "0",
        "matter_contact_symbolic_identity_exact": quotient_summary[
            "matter_contact_difference"
        ]
        == "0",
        "neutral_vacuum_p4_parameter_count_zero": quotient_summary[
            "independent_neutral_vacuum_p4_parameters"
        ]
        == 0,
        "Wplus_Wminus_not_misidentified_as_R2C2": next(
            row for row in parameter_rows if row["parameter_id"] == "PAR4964_06_Wplus_Wminus"
        )["current_status"]
        == "NOT_GRAVITATIONAL_AR_AC",
        "CFF_one_LEC": CFF_summary["retained_independent_CFF_LECs"] == 1,
        "CFF_flat_Maxwell_exact": CFF_summary["flat_Maxwell_exact"],
        "CFF_numeric_calibration_remains_false": not CFF_summary[
            "physical_cIR_calibrated"
        ],
        "nine_EOS_rows_cross_checked": len(EOS_rows) == 9,
        "eleven_compact_tail_rows": p8_summary["compact_object_count"] == 11,
        "all_compact_chi_positive_and_subunit": all(
            0.0 < float(row["chi_lP2_curvature"]) < 1.0
            for row in p8_rows
            if row["row_type"] == "compact_object_gate"
        ),
        "p8_budget_is_finite_and_positive": math.isfinite(
            p8_summary["smallest_C8_budget_R1"]
        )
        and p8_summary["smallest_C8_budget_R1"] > 0.0,
        "p8_parent_norm_not_claimed": not p8_summary["parent_C8_bound_available"]
        and not p8_summary["parent_R_bound_available"],
        "all_operator_compact_GR_false": next(
            row for row in decisions if row["decision_id"] == "DEC4964_08_all_operator_compact_GR"
        )["decision"]
        == "NO",
        "full_MTS_false": next(
            row for row in decisions if row["decision_id"] == "DEC4964_09_full_MTS"
        )["decision"]
        == "NO",
    }
    if not all(checks.values()):
        raise RuntimeError(
            f"internal checkpoint checks failed: {[name for name, passed in checks.items() if not passed]}"
        )

    write_csv(QUOTIENT_CSV, quotient_rows)
    write_csv(PARAMETER_CSV, parameter_rows)
    write_csv(CFF_CSV, CFF_rows)
    write_csv(P8_CSV, p8_rows)
    write_csv(DECISION_CSV, decisions)

    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_hashes": source_hashes,
        "source_clause_checks": source_clause_checks,
        "four_derivative_quotient": quotient_summary,
        "CFF_one_LEC_contract": CFF_summary,
        "p8plus_tail_gate": p8_summary,
        "checks": checks,
        "decisions": {
            row["decision_id"]: row["decision"] for row in decisions
        },
        "claim_scope": {
            "R2C2_independent_vacuum_p4_obstruction": False,
            "R2C2_full_matter_contact_matching": False,
            "CFF_one_LEC_structure": True,
            "CFF_numeric_calibration": False,
            "compact_GR_through_declared_static_p6_domain": True,
            "p8plus_parent_bound": False,
            "all_operator_compact_GR": False,
            "full_MTS": False,
        },
    }
    RESULT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    PROVENANCE.write_text(
        provenance_text(source_hashes, quotient_summary, CFF_summary, p8_summary),
        encoding="utf-8",
    )

    print(f"{MARKER}_CHECKS={sum(checks.values())}/{len(checks)}", flush=True)
    print(
        f"{MARKER}_VACUUM_P4_PARAMETERS={quotient_summary['independent_neutral_vacuum_p4_parameters']}",
        flush=True,
    )
    print(
        f"{MARKER}_TIGHTEST_C8_R1_BUDGET={p8_summary['smallest_C8_budget_R1']:.16e}",
        flush=True,
    )
    print(f"{MARKER}_CFF_NUMERIC_CALIBRATION=False", flush=True)
    print(f"{MARKER}_ALL_OPERATOR_COMPACT_GR=False", flush=True)
    print(f"{MARKER}_FULL_MTS=False", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
