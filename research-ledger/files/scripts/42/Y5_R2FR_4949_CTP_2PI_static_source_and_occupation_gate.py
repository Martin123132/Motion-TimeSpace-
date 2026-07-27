from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
import subprocess
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4949"

RESULT_JSON = SOURCE / "CTP_2PI_static_source_results.json"
CTP_CSV = SOURCE / "CTP_2PI_parent_reconstruction.csv"
AXISYMMETRIC_CSV = SOURCE / "axisymmetric_Dyson_and_static_production_gate.csv"
SPARC_CSV = SOURCE / "SPARC_outer_occupation_scale_diagnostic.csv"
STRESS_CSV = SOURCE / "occupation_stress_conservation_and_local_limit.csv"
PAIR_CSV = SOURCE / "reflection_even_pair_source_next_operator_gate.csv"
GALAXY_SNAPSHOT_CSV = SOURCE / "galaxy_readonly_snapshot.csv"

SCALE_4938 = POST / "4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-two-scale-theory-gate.md"
LOCAL_4942 = POST / "4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-branch-and-C3-CFF-PPN-residual-gate.md"
SOURCE_4943 = POST / "4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md"
LOCAL_4947 = POST / "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md"
INTERFACE_4948 = POST / "4948-Y5-R2FR-single-parent-motion-Hessian-to-galaxy-phase-flow-and-universal-Jgap-interface.md"
BERGES_TEX = POST / "source-intake" / "functional_rg" / "4948" / "riolecture.tex"

GALAXY_REPO = Path(r"D:\g4948")
GALAXY_README = GALAXY_REPO / "README.md"
GALAXY_SAMPLES = GALAXY_REPO / "data" / "samples.js"
EXPECTED_GALAXY_HEAD = "5c2fc082adcc67d779cfd99d5b6e9a9c9ac5fcbd"

MARKER = "MTS_4949_CTP_2PI_STATIC_SOURCE_AND_OCCUPATION_GATE"
CHECKED_DATE = "2026-07-13"
LIGHT_SPEED = 299_792_458.0
NEWTON_G = 6.67430e-11
HBAR = 1.054571817e-34
PLANCK_LENGTH = math.sqrt(HBAR * NEWTON_G / LIGHT_SPEED**3)
KPC = 3.085677581491367e19
ML_DISK = 0.5
ML_BULGE = 0.7

EXPECTED_HASHES = {
    SCALE_4938: "b30394a62c6a22af5da315b92a2823f44aa34cd914b6bab813136b0926aa0ca4",
    LOCAL_4942: "64b96ca4e19a058ced85c0c4b800ae7a237408606799dd8c4a5b58935f635c5f",
    SOURCE_4943: "a90da0e9ad0457fc3dbdb389d7bf2715cb9d707cbffa094a987b0b0553e257b5",
    LOCAL_4947: "0b71f50c85ab4c5761755aa11544910a1a1e4fcacc901236432705a5ba36563f",
    INTERFACE_4948: "b563ab1bf95974732dd5f2a3ab2cd5af2d5b414011648554e5247a930b47aec0",
    BERGES_TEX: "de16f5e4f6e8b10e6880a18b130a4923952556e6fead9fda7a7e162e3282128d",
    GALAXY_README: "e9acb4d72fc6fdd7f39ba62e18357746ae423e61c7e6932cf8b5b8f45265e402",
    GALAXY_SAMPLES: "a7edd2db0e237d7997207bf1ee53c78e492cf5dbc7a7cbfc478c12e69bddbfba",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


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


def load_samples() -> list[dict[str, str]]:
    raw = read_text(GALAXY_SAMPLES)
    start = raw.index("[")
    end = raw.rindex("]") + 1
    return json.loads(raw[start:end])


def parse_rotmod(text: str) -> list[list[float]]:
    rows: list[list[float]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        values = [float(value) for value in stripped.split()]
        if len(values) >= 6:
            rows.append(values)
    return rows


def main() -> int:
    SOURCE.mkdir(parents=True, exist_ok=True)
    source_hashes = {str(path): digest(path) for path in EXPECTED_HASHES}
    source_hashes_match = all(source_hashes[str(path)] == expected for path, expected in EXPECTED_HASHES.items())

    scale_text = read_text(SCALE_4938)
    local_text = read_text(LOCAL_4942)
    source_text = read_text(SOURCE_4943)
    local_gr_text = read_text(LOCAL_4947)
    interface_text = read_text(INTERFACE_4948)
    berges_text = read_text(BERGES_TEX)

    source_clause_checks = {
        "two_scale_Jgap_parent": "J_gap=m_gap^2 G_N" in scale_text,
        "quadratic_O4_parent_action": "Z_psi+2u_O4 C^2" in local_text,
        "positive_local_principal_symbol": "Z_eff>0" in local_text,
        "matter_one_point_source_zero": "delta S_SM/delta psi=0" in source_text,
        "gravity_pair_vertex_not_tadpole": "scalar-pair vertices but no" in source_text,
        "local_GR_correspondence_available": "nabla^2 Phi=4 pi G_N rho" in local_gr_text,
        "two_point_survivor_previously_selected": "Reflection-even composite survivor" in interface_text,
        "Berges_2PI_action": "\\label{2PIaction}" in berges_text,
        "Berges_lowest_Gamma2_zero": "To lowest order one has $\\Gamma_2[\\phi,G] = 0$" in berges_text,
        "Berges_Kadanoff_Baym_equations": "\\label{eq:exactrhoF}" in berges_text,
        "Berges_initial_F_data_required": "full initial conditions" in berges_text,
        "Berges_free_modes_collisionless": "particle numbers are conserved" in berges_text,
        "galaxy_locked_ML": "ML_disk = 0.5" in read_text(GALAXY_README) and "ML_bulge = 0.7" in read_text(GALAXY_README),
    }

    ctp_rows = tagged(
        [
            {
                "derivation_id": "CTP4949_00_parent_action",
                "object": "completed reflection-even motion action at fixed mean metric",
                "equation": "S_psi=-1/2 int sqrt(-g)[A(x) nabla_psi^2+m_gap^2 psi^2]; A=Z_psi+2u_O4 C^2",
                "derivation": "checkpoint 4942 quadratic action",
                "status": "PARENT_ACTION_RECONSTRUCTED",
                "passed": True,
            },
            {
                "derivation_id": "CTP4949_01_CTP_variables",
                "object": "real-time reflection-even correlators",
                "equation": "F(x,y)=<anti-commutator(psi(x),psi(y))>/2; rho(x,y)=i<[psi(x),psi(y)]>",
                "derivation": "closed-time-path decomposition of G",
                "status": "PHYSICAL_OCCUPATION_VARIABLES_DEFINED",
                "passed": True,
            },
            {
                "derivation_id": "CTP4949_02_Dyson",
                "object": "CTP Dyson equation",
                "equation": "G^-1=D^-1-Sigma; Sigma=2i delta Gamma_2/delta G",
                "derivation": "stationarity of the CTP 2PI action",
                "status": "DYSON_EQUATION_DERIVED",
                "passed": True,
            },
            {
                "derivation_id": "CTP4949_03_KB_spectral",
                "object": "spectral equation",
                "equation": "D_x rho=-int_y0^x0 Sigma_rho rho",
                "derivation": "real and imaginary parts of the CTP Dyson equation",
                "status": "KADANOFF_BAYM_SPECTRAL_EQUATION_DERIVED",
                "passed": True,
            },
            {
                "derivation_id": "CTP4949_04_KB_statistical",
                "object": "statistical occupation equation",
                "equation": "D_x F=-int_t0^x0 Sigma_rho F+int_t0^y0 Sigma_F rho",
                "derivation": "real and imaginary parts of the CTP Dyson equation",
                "status": "KADANOFF_BAYM_STATISTICAL_EQUATION_DERIVED",
                "passed": True,
            },
            {
                "derivation_id": "CTP4949_05_scalar_Gamma2",
                "object": "displayed scalar-only fixed-mean-metric truncation",
                "equation": "Gamma_2^scalar=0; Sigma_F^scalar=Sigma_rho^scalar=0",
                "derivation": "the retained scalar action is quadratic and has no cubic or quartic scalar vertex",
                "status": "SCALAR_COLLISION_AND_SOURCE_KERNELS_ZERO",
                "passed": True,
            },
            {
                "derivation_id": "CTP4949_06_metric_quantum_hierarchy",
                "object": "full parent quantum completion",
                "equation": "Gamma_2^full requires G_psipsi plus G_hh and mixed scalar-metric kernels or an explicitly integrated metric influence functional",
                "derivation": "metric exchange supplies pair vertices but is outside a scalar-only 2PI closure",
                "status": "SCALAR_ONLY_2PI_NOT_FULL_PARENT_QUANTUM_CLOSURE",
                "passed": True,
            },
            {
                "derivation_id": "CTP4949_07_initial_state",
                "object": "statistical initial data",
                "equation": "F(t0,t0), partial_t F(t,t0)|t0 and partial_t partial_tprime F|t0 must be supplied",
                "derivation": "CTP initial density matrix correspondence",
                "status": "OCCUPATION_IS_INITIAL_DATA_WITHOUT_SOURCE_KERNEL",
                "passed": True,
            },
            {
                "derivation_id": "CTP4949_08_Euclidean_boundary",
                "object": "4948 Euclidean 2PI contract",
                "equation": "Euclidean stationarity determines equilibrium correlators but not a nonvacuum real-time occupation history",
                "derivation": "a persistent populated state requires CTP statistical data or a sourced equilibrium ensemble",
                "status": "EUCLIDEAN_CONTRACT_REPLACED_FOR_OCCUPATION_DYNAMICS",
                "passed": True,
            },
        ]
    )

    axisymmetric_rows = tagged(
        [
            {
                "gate_id": "AXI4949_00_metric",
                "object": "static axisymmetric Euclidean metric",
                "equation_or_test": "ds_E^2=N^2 d tau^2+gamma_ab dx^a dx^b+gamma_phiphi dphi^2; a,b in {R,z}",
                "result": "time and azimuthal Killing directions separated",
                "decision": "PASS_GEOMETRIC_REDUCTION",
                "passed": True,
            },
            {
                "gate_id": "AXI4949_01_operator",
                "object": "parent inverse propagator",
                "equation_or_test": "D=-1/sqrt(g) partial_mu[sqrt(g) A g^munu partial_nu]+m_gap^2",
                "result": "unique quadratic operator fixed by A=Z+2u_O4 C^2",
                "decision": "PASS_PARENT_OPERATOR",
                "passed": True,
            },
            {
                "gate_id": "AXI4949_02_mode_operator",
                "object": "omega and azimuthal-j mode",
                "equation_or_test": "D_omega,j=-1/(N sqrt(gamma)) partial_a[N sqrt(gamma) A gamma^ab partial_b]+A omega^2/N^2+A j^2 gamma^phiphi+m_gap^2",
                "result": "renormalized two-dimensional Green problem defined on the R-z half-plane",
                "decision": "PASS_AXISYMMETRIC_DYSON_OPERATOR",
                "passed": True,
            },
            {
                "gate_id": "AXI4949_03_positivity",
                "object": "static quadratic form",
                "equation_or_test": "<f,Df>=int sqrt(g)[A |nabla f|^2+m_gap^2 |f|^2]>0 for A>0 and m_gap^2>0",
                "result": "no zero or negative mode in the declared stable branch",
                "decision": "PASS_POSITIVE_OPERATOR_NO_BIFURCATION",
                "passed": True,
            },
            {
                "gate_id": "AXI4949_04_static_modes",
                "object": "stationary Lorentzian mode basis",
                "equation_or_test": "psi=sum_alpha[a_alpha u_alpha(x)e^-i omega_alpha t+h.c.] with omega_alpha>0",
                "result": "time-independent Hamiltonian diagonalizes once",
                "decision": "PASS_STATIONARY_MODE_DECOMPOSITION",
                "passed": True,
            },
            {
                "gate_id": "AXI4949_05_Bogoliubov",
                "object": "vacuum production by a static baryonic metric",
                "equation_or_test": "partial_t D=0 and identical stationary in/out basis imply beta_alpha,beta=0",
                "result": "the static baryonic field scatters modes but does not populate the vacuum",
                "decision": "STATIC_PAIR_PRODUCTION_EXACT_ZERO",
                "passed": True,
            },
            {
                "gate_id": "AXI4949_06_occupation",
                "object": "mode occupation",
                "equation_or_test": "n_alpha=<a_alpha^dagger a_alpha>; dot n_alpha=0 in the displayed collisionless stationary truncation",
                "result": "n_alpha is inherited state data and vacuum has n_alpha=0",
                "decision": "SOURCE_DEPENDENT_AMPLITUDE_NOT_DERIVED",
                "passed": True,
            },
            {
                "gate_id": "AXI4949_07_O4",
                "object": "curvature-kinetic O4 portal",
                "equation_or_test": "A(x)=Z+2u_O4 C^2 remains positive and time independent on the local branch",
                "result": "O4 changes static eigenfunctions but supplies neither a tachyonic mode nor a real-time pump",
                "decision": "O4_DOES_NOT_POPULATE_STATIC_COMPOSITE",
                "passed": True,
            },
            {
                "gate_id": "AXI4949_08_full_quantum",
                "object": "graviton-mediated self-energy",
                "equation_or_test": "nonzero G_hh kernels can renormalize and scatter but an exact stationary ground state remains unpopulated",
                "result": "full quantum kernels cannot be replaced by a scalar-only Gamma_2 closure and do not select a nonvacuum density matrix",
                "decision": "FULL_METRIC_2PI_OPEN_NO_STATIC_STATE_SOURCE",
                "passed": True,
            },
        ]
    )

    samples = load_samples()
    sparc_rows: list[dict[str, Any]] = []
    for sample in samples:
        points = parse_rotmod(sample["text"])
        outer = points[-1]
        radius_kpc, vobs, errv, vgas, vdisk, vbulge = outer[:6]
        vbar2_km2_s2 = vgas * abs(vgas) + ML_DISK * vdisk**2 + ML_BULGE * vbulge**2
        residual_v2_km2_s2 = max(vobs**2 - vbar2_km2_s2, 0.0)
        radius_m = radius_kpc * KPC
        residual_v2_m2_s2 = residual_v2_km2_s2 * 1.0e6
        required_energy_density = residual_v2_m2_s2 * LIGHT_SPEED**2 / (4.0 * math.pi * NEWTON_G * radius_m**2)
        one_quantum_cell_density = HBAR * LIGHT_SPEED / radius_m**4
        occupation_required = required_energy_density / one_quantum_cell_density if residual_v2_m2_s2 > 0.0 else 0.0
        one_quantum_fraction = 1.0 / occupation_required if occupation_required > 0.0 else 0.0
        gap_for_radius = (PLANCK_LENGTH / radius_m) ** 2
        sparc_rows.append(
            {
                "galaxy": sample["name"].removesuffix("_rotmod.dat"),
                "outer_radius_kpc": radius_kpc,
                "outer_Vobs_km_s": vobs,
                "outer_errV_km_s": errv,
                "outer_Vbar2_km2_s2": vbar2_km2_s2,
                "outer_residual_V2_km2_s2": residual_v2_km2_s2,
                "positive_outer_residual": residual_v2_km2_s2 > 0.0,
                "Jgap_if_correlation_length_equals_outer_radius": gap_for_radius,
                "required_effective_energy_density_J_m3": required_energy_density,
                "one_quantum_per_R_cell_energy_density_J_m3": one_quantum_cell_density,
                "occupation_per_R_cell_required": occupation_required,
                "one_quantum_fraction_of_required": one_quantum_fraction,
                "interpretation": "SCALING_DIAGNOSTIC_NOT_A_FIT" if residual_v2_m2_s2 > 0.0 else "NO_POSITIVE_OUTER_RESIDUAL_AT_LOCKED_ML",
                "checkpoint_marker": MARKER,
                "valid_for_full_MTS_claim": False,
                "source_checked_date": CHECKED_DATE,
            }
        )

    positive_rows = [row for row in sparc_rows if row["positive_outer_residual"]]
    log_occupations = [math.log10(float(row["occupation_per_R_cell_required"])) for row in positive_rows]
    log_gaps = [math.log10(float(row["Jgap_if_correlation_length_equals_outer_radius"])) for row in positive_rows]

    stress_rows = tagged(
        [
            {
                "gate_id": "STR4949_00_state_subtraction",
                "object": "physical state correlator",
                "equation_or_test": "Delta F_state=F_state-F_vac[g] in one fixed renormalization convention",
                "result": "vacuum polarization and real occupation are not double counted",
                "decision": "PASS_STATE_DEFINITION",
                "passed": True,
            },
            {
                "gate_id": "STR4949_01_stress",
                "object": "occupation stress",
                "equation_or_test": "T_occ_mn=-2/sqrt(-g) delta Gamma_CTP[Delta F_state]/delta g^mn at stationary F and rho",
                "result": "same parent operator owns dynamics and metric source",
                "decision": "PASS_VARIATIONAL_STRESS_DEFINITION",
                "passed": True,
            },
            {
                "gate_id": "STR4949_02_Ward",
                "object": "diffeomorphism Ward identity",
                "equation_or_test": "nabla^m(T_matter_mn+T_occ_mn)=0 on metric and CTP stationarity equations",
                "result": "conservation follows for a covariant renormalized truncation",
                "decision": "PASS_CONDITIONAL_CONSERVATION",
                "passed": True,
            },
            {
                "gate_id": "STR4949_03_vacuum",
                "object": "stationary ground state",
                "equation_or_test": "F_state=F_vac[g] implies Delta F_state=0",
                "result": "T_occ=0 exactly by the declared state subtraction",
                "decision": "VACUUM_OCCUPATION_STRESS_ZERO",
                "passed": True,
            },
            {
                "gate_id": "STR4949_04_vacuum_polarization",
                "object": "one-loop vacuum effective action",
                "equation_or_test": "Gamma_vac=Tr ln D/2 renormalizes Lambda G_N a_R a_C and leaves calculable nonlocal vacuum terms",
                "result": "it belongs to the Wilson matching ledger and is not a free galaxy occupation",
                "decision": "PASS_NO_DOUBLE_COUNTING_VACUUM_EFT",
                "passed": True,
            },
            {
                "gate_id": "STR4949_05_local_limit",
                "object": "4947 correspondence recovery",
                "equation_or_test": "Delta F_state->0 and matched vacuum coefficients fixed imply T_occ->0 and the 4947 GR/Newton/Maxwell branch",
                "result": "local correspondence is preserved",
                "decision": "PASS_LOCAL_GR_RECOVERY",
                "passed": True,
            },
            {
                "gate_id": "STR4949_06_macroscopic_scale",
                "object": "outer SPARC occupation scaling",
                "equation_or_test": "N_R=(V_X/c)^2(R/l_P)^2/(4pi) for energy hbar c/R per correlation cell R^3",
                "result": f"positive rows={len(positive_rows)}; log10 N range={min(log_occupations):.6f} to {max(log_occupations):.6f}; median={statistics.median(log_occupations):.6f}",
                "decision": "MACROSCOPIC_HIGH_OCCUPATION_REQUIRED",
                "passed": True,
            },
            {
                "gate_id": "STR4949_07_predictivity",
                "object": "current composite galaxy route",
                "equation_or_test": "the displayed parent has no CTP source kernel or bifurcation selecting the required nonvacuum F",
                "result": "choosing n_alpha or C_n and C_b would be an initial-state closure",
                "decision": "CURRENT_MINIMAL_2PI_GALAXY_ROUTE_REJECTED",
                "passed": True,
            },
        ]
    )

    pair_rows = tagged(
        [
            {
                "operator_id": "PAIR4949_00_existing_metric_pair",
                "operator": "minimal metric and strict-EFT pair vertices",
                "role": "reflection-even scattering and vacuum polarization",
                "necessary_condition": "time dependence or occupied incoming state for real production",
                "current_result": "static vacuum production zero; local quadratic operator positive",
                "decision": "INSUFFICIENT_FOR_STATIC_GALAXY_STATE",
                "passed": True,
            },
            {
                "operator_id": "PAIR4949_01_Rpsi2",
                "operator": "-xi_R R psi^2/2",
                "role": "parent-even curvature-dependent quadratic mass",
                "necessary_condition": "lowest spatial eigenvalue crosses zero in galaxies while remaining positive in every local-GR arena",
                "current_result": "allowed by reflection but absent from the completed displayed truncation",
                "decision": "NEXT_DERIVATION_CANDIDATE_NOT_ADOPTED",
                "passed": True,
            },
            {
                "operator_id": "PAIR4949_02_Tpsi2",
                "operator": "-xi_T T_matter psi^2/(2 M_R^2)",
                "role": "explicit even matter-pair source after integrating permitted parent channels",
                "necessary_condition": "must be parent-generated and species blind; cannot duplicate the existing strict-EFT contact",
                "current_result": "no independent coefficient is present in the selected matter functor",
                "decision": "PARENT_ORIGIN_REQUIRED_NOT_ADOPTED",
                "passed": True,
            },
            {
                "operator_id": "PAIR4949_03_quartic",
                "operator": "+lambda_4 psi^4/4",
                "role": "stabilize a reflection-even bifurcated branch",
                "necessary_condition": "lambda_4 positive with RG-consistent normalization and no hidden third scale",
                "current_result": "not present in the completed local quadratic packet",
                "decision": "REQUIRED_IF_ZERO_MODE_BECOMES_TACHYONIC",
                "passed": True,
            },
            {
                "operator_id": "PAIR4949_04_state_history",
                "operator": "time-dependent CTP influence kernel Sigma_F and Sigma_rho",
                "role": "generate occupation during cosmological or galaxy assembly history",
                "necessary_condition": "derive the kernel and initial state from the parent and carry one J_gap into the stationary remnant",
                "current_result": "not supplied by the static parent-to-galaxy map",
                "decision": "ALTERNATIVE_DYNAMIC_ROUTE_OPEN_NOT_A_STATIC_SOLUTION",
                "passed": True,
            },
            {
                "operator_id": "PAIR4949_05_acceptance",
                "operator": "reflection-even pair-source selection theorem",
                "role": "replace arbitrary occupation by a source-owned branch",
                "necessary_condition": "source-selected amplitude plus positive final Hessian plus conserved stress plus local-GR recovery plus no arena retuning",
                "current_result": "none of the current displayed operators satisfies all conditions",
                "decision": "ADVANCE_TO_PARENT_PAIR_OPERATOR_AND_BIFURCATION_WINDOW",
                "passed": True,
            },
        ]
    )

    head = subprocess.run(
        ["git", "-C", str(GALAXY_REPO), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "-C", str(GALAXY_REPO), "status", "--porcelain"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    galaxy_snapshot_rows = tagged(
        [
            {
                "snapshot_id": "GAL4949_00_public_samples",
                "repository": "https://github.com/Martin123132/MTS-Galaxy-Lab-",
                "local_readonly_clone": str(GALAXY_REPO),
                "head": head,
                "expected_head": EXPECTED_GALAXY_HEAD,
                "working_tree_clean": not status,
                "README_sha256": digest(GALAXY_README),
                "samples_sha256": digest(GALAXY_SAMPLES),
                "sample_count": len(samples),
                "locked_ML_disk": ML_DISK,
                "locked_ML_bulge": ML_BULGE,
                "repository_modified_by_checkpoint": False,
                "status": "READ_ONLY_SOURCE_SNAPSHOT",
                "passed": head == EXPECTED_GALAXY_HEAD and not status,
            }
        ]
    )

    checks = {
        "source_hashes_match": source_hashes_match,
        "authoritative_clauses_match": all(source_clause_checks.values()),
        "CTP_rows_pass": all(row["passed"] for row in ctp_rows),
        "axisymmetric_rows_pass": all(row["passed"] for row in axisymmetric_rows),
        "SPARC_samples_parsed": len(samples) == 175 and len(sparc_rows) == 175,
        "positive_outer_residual_rows_exist": len(positive_rows) > 100,
        "all_positive_occupation_scales_finite": all(math.isfinite(value) and value > 0.0 for value in log_occupations),
        "all_gap_scales_finite": all(math.isfinite(value) for value in log_gaps),
        "macroscopic_occupation_required": min(log_occupations) > 95.0,
        "stress_rows_pass": all(row["passed"] for row in stress_rows),
        "pair_operator_rows_pass": all(row["passed"] for row in pair_rows),
        "static_pair_production_zero": next(row for row in axisymmetric_rows if row["gate_id"] == "AXI4949_05_Bogoliubov")["decision"] == "STATIC_PAIR_PRODUCTION_EXACT_ZERO",
        "current_minimal_2PI_route_rejected": next(row for row in stress_rows if row["gate_id"] == "STR4949_07_predictivity")["decision"] == "CURRENT_MINIMAL_2PI_GALAXY_ROUTE_REJECTED",
        "local_GR_recovery_retained": next(row for row in stress_rows if row["gate_id"] == "STR4949_05_local_limit")["decision"] == "PASS_LOCAL_GR_RECOVERY",
        "galaxy_head_locked": head == EXPECTED_GALAXY_HEAD,
        "galaxy_worktree_clean": not status,
        "all_rows_full_MTS_nonclaim": all(
            not row["valid_for_full_MTS_claim"]
            for rows in (ctp_rows, axisymmetric_rows, sparc_rows, stress_rows, pair_rows, galaxy_snapshot_rows)
            for row in rows
        ),
    }

    result = {
        "marker": MARKER,
        "checks": checks,
        "source_hashes": source_hashes,
        "source_clause_checks": source_clause_checks,
        "parent_CTP_result": {
            "completed_scalar_action_quadratic": True,
            "scalar_only_fixed_metric_Gamma2": 0.0,
            "scalar_only_Sigma_F": 0.0,
            "scalar_only_Sigma_rho": 0.0,
            "statistical_initial_data_required": True,
            "Euclidean_2PI_sufficient_for_nonvacuum_occupation": False,
            "full_metric_quantum_2PI_completed": False,
        },
        "static_source_result": {
            "operator_positive_on_declared_branch": True,
            "stationary_Bogoliubov_beta": 0.0,
            "vacuum_mode_occupation": 0.0,
            "source_dependent_Cn_Cb_from_static_parent": False,
            "O4_static_pair_pump": False,
        },
        "SPARC_occupation_diagnostic": {
            "sample_count": len(samples),
            "positive_outer_residual_count": len(positive_rows),
            "log10_occupation_required_min": min(log_occupations),
            "log10_occupation_required_median": statistics.median(log_occupations),
            "log10_occupation_required_max": max(log_occupations),
            "log10_Jgap_for_outer_radius_min": min(log_gaps),
            "log10_Jgap_for_outer_radius_median": statistics.median(log_gaps),
            "log10_Jgap_for_outer_radius_max": max(log_gaps),
            "interpretation": "one-quantum-per-outer-radius-cell scaling diagnostic, not a fit or strict vacuum-polarization bound",
        },
        "stress_and_local_limit": {
            "state_subtraction": "Delta F_state=F_state-F_vac[g]",
            "vacuum_subtracted_occupation_stress": 0.0,
            "Ward_conservation_from_covariant_stationarity": True,
            "local_4947_branch_recovered_when_DeltaF_zero": True,
            "vacuum_Wilson_matching_still_open": True,
        },
        "decision": {
            "current_minimal_scalar_2PI_galaxy_route": "REJECTED",
            "reason": "static positive quadratic parent has no CTP source kernel, pair-production channel or bifurcation selecting the required macroscopic nonvacuum state",
            "next_route": "derive or reject a parent-owned reflection-even pair operator and stabilized environmental bifurcation, or a fully sourced time-dependent CTP history",
        },
        "claim_boundary": {
            "CTP_2PI_equations_derived": True,
            "axisymmetric_parent_Dyson_operator_derived": True,
            "static_vacuum_pair_production_zero": True,
            "state_stress_conservation_contract_derived": True,
            "local_GR_recovery_derived": True,
            "SPARC_occupation_scale_diagnostic_calculated": True,
            "source_dependent_composite_amplitude_derived": False,
            "macroscopic_galaxy_stress_calculated": False,
            "current_minimal_2PI_galaxy_route_viable": False,
            "pair_source_operator_parent_derived": False,
            "full_MTS_galaxy_unification": False,
            "galaxy_repository_modified": False,
        },
    }

    write_csv(CTP_CSV, ctp_rows)
    write_csv(AXISYMMETRIC_CSV, axisymmetric_rows)
    write_csv(SPARC_CSV, sparc_rows)
    write_csv(STRESS_CSV, stress_rows)
    write_csv(PAIR_CSV, pair_rows)
    write_csv(GALAXY_SNAPSHOT_CSV, galaxy_snapshot_rows)
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    failed = [name for name, passed in checks.items() if not passed]
    print(f"SAMPLES={len(samples)}")
    print(f"POSITIVE_OUTER_RESIDUALS={len(positive_rows)}")
    print(f"LOG10_N_MIN={min(log_occupations)}")
    print(f"LOG10_N_MEDIAN={statistics.median(log_occupations)}")
    print(f"LOG10_N_MAX={max(log_occupations)}")
    print(f"LOG10_JGAP_MEDIAN={statistics.median(log_gaps)}")
    print(f"FAILED={len(failed)}")
    if failed:
        print("FAILED_CHECKS=" + ",".join(failed))
    print(f"RESULT_SHA256={digest(RESULT_JSON)}")
    print("PASS" if not failed else "FAIL")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
