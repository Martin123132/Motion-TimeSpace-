from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4948"

RESULT_JSON = SOURCE / "motion_Hessian_galaxy_phase_results.json"
LOGISTIC_CSV = SOURCE / "projective_logistic_derivation.csv"
EXPONENT_CSV = SOURCE / "parent_exponent_to_galaxy_gate.csv"
SOURCE_GATE_CSV = SOURCE / "source_amplitude_and_stress_gate.csv"
COMPOSITE_CSV = SOURCE / "composite_2PI_survivor_contract.csv"
GALAXY_SNAPSHOT_CSV = SOURCE / "galaxy_readonly_snapshot.csv"

FREEZE_4907 = POST / "4907-Y5-R2FR-parent-derived-environmental-bi-response-action-or-galaxy-residual-freeze.md"
INTERFACE_4936 = POST / "4936-Y5-R2FR-motion-1PI-mass-and-O4-functional-trace-projection-or-two-scale-predictivity-gate.md"
SCALE_4938 = POST / "4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-two-scale-theory-gate.md"
O4_4940 = POST / "4940-Y5-R2FR-metric-kernel-O4-nonzero-source-self-backreacted-fixed-point-and-direct-trace-cancellation-gate.md"
LOCAL_4942 = POST / "4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-branch-and-C3-CFF-PPN-residual-gate.md"
SOURCE_4943 = POST / "4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md"
LOCAL_4947 = POST / "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md"
SPECTRUM_4940 = POST / "source-intake" / "functional_rg" / "4940" / "O4_kernel_augmented_spectrum.csv"

GALAXY_REPO = Path(r"D:\g4948")
GALAXY_README = GALAXY_REPO / "README.md"
GALAXY_SCRIPT = GALAXY_REPO / "scripts" / "mts-failure-lab.py"
PHASE_FORMULA = Path(r"D:\Users\ollet\Desktop\Galaxy Work\mts-output-packs\mts-v19-phase-field-bridge-v1\mts_v19_phase_field_bridge_formula.json")
MOTION_FORMULA = Path(r"D:\Users\ollet\Desktop\Galaxy Work\mts-output-packs\mts-v19-motion-field-kernel-v1\mts_v19_motion_field_kernel_formula.json")
NORMALIZATION_FORMULA = Path(r"D:\Users\ollet\Desktop\Galaxy Work\mts-output-packs\mts-v19-motion-field-normalization-v1\mts_v19_motion_field_normalization_formula.json")
TWO_PI_PDF = SOURCE / "hep-ph-0409233.pdf"
TWO_PI_TAR = SOURCE / "hep-ph-0409233-source.tar"
TWO_PI_TEX = SOURCE / "riolecture.tex"

EXPECTED_HASHES = {
    FREEZE_4907: "a061a4257b3e9a81467c3d8a96dd37754e8de1dc9fc580fc350949f1accb0eae",
    INTERFACE_4936: "d24db400f3fb2fec75883bb078a37eec15b101e09c119f2a6ff43063d604c971",
    SCALE_4938: "b30394a62c6a22af5da315b92a2823f44aa34cd914b6bab813136b0926aa0ca4",
    O4_4940: "3fac7373e840f707d855758ca3053e4315411058264782bcf51f49643d99dfef",
    LOCAL_4942: "64b96ca4e19a058ced85c0c4b800ae7a237408606799dd8c4a5b58935f635c5f",
    SOURCE_4943: "a90da0e9ad0457fc3dbdb389d7bf2715cb9d707cbffa094a987b0b0553e257b5",
    LOCAL_4947: "0b71f50c85ab4c5761755aa11544910a1a1e4fcacc901236432705a5ba36563f",
    SPECTRUM_4940: "92493e8ecb238fd718a1928d01b7f5e788124f8e255a72beed1f0a8f2a7cae3a",
    GALAXY_README: "e9acb4d72fc6fdd7f39ba62e18357746ae423e61c7e6932cf8b5b8f45265e402",
    GALAXY_SCRIPT: "913cb3f624814d970030b7f0e3446cd63894f94d86d688e2ff46412da316476e",
    PHASE_FORMULA: "f31b2ebeba07d519d8dc1ee4a47cb65642e201be462a88ae35b108de1da5979e",
    MOTION_FORMULA: "161b2a2da5f6f5259dc8a63cb9c637178a91732698fac40df250fa57f696fcf0",
    NORMALIZATION_FORMULA: "471dfe7b08f323e0b60f38fda31acff68ae96d5b363955c44ad421b3fdd28451",
    TWO_PI_PDF: "1d36d409510711e21f69ba6fb222d79f031d0392fa1484f855ce274c9f19fe49",
    TWO_PI_TAR: "d4e12d76e8ded4bc955e51462047c113911f4376a28c5ddb2bb82076212d39ab",
    TWO_PI_TEX: "de16f5e4f6e8b10e6880a18b130a4923952556e6fead9fda7a7e162e3282128d",
}

EXPECTED_GALAXY_HEAD = "5c2fc082adcc67d779cfd99d5b6e9a9c9ac5fcbd"
MARKER = "MTS_4948_MOTION_HESSIAN_GALAXY_PHASE_INTERFACE"
CHECKED_DATE = "2026-07-13"
NATURAL_RADIAL_SCALE_EXPONENT = 1.0


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def source_key(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty table {path.name}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
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


def git_output(*args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(GALAXY_REPO), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def logistic_up(log_radius: float, exponent: float) -> float:
    argument = exponent * log_radius
    if argument >= 0.0:
        return 1.0 / (1.0 + math.exp(-argument))
    exp_argument = math.exp(argument)
    return exp_argument / (1.0 + exp_argument)


def logistic_down(log_radius: float, exponent: float) -> float:
    return logistic_up(-log_radius, exponent)


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)
    source_hashes = {
        source_key(path): digest(path) if path.exists() else "MISSING"
        for path in EXPECTED_HASHES
    }
    hash_failures = [
        source_key(path)
        for path, expected in EXPECTED_HASHES.items()
        if source_hashes[source_key(path)] != expected
    ]
    if hash_failures:
        raise RuntimeError(f"source hash mismatch: {hash_failures}")

    galaxy_head = git_output("rev-parse", "HEAD")
    galaxy_status = git_output("status", "--porcelain=v1")
    if galaxy_head != EXPECTED_GALAXY_HEAD or galaxy_status:
        raise RuntimeError(f"galaxy read-only snapshot changed: head={galaxy_head}, status={galaxy_status!r}")

    freeze_text = FREEZE_4907.read_text(encoding="utf-8-sig")
    interface_text = INTERFACE_4936.read_text(encoding="utf-8-sig")
    scale_text = SCALE_4938.read_text(encoding="utf-8-sig")
    o4_text = O4_4940.read_text(encoding="utf-8-sig")
    local_text = LOCAL_4942.read_text(encoding="utf-8-sig")
    source_text = SOURCE_4943.read_text(encoding="utf-8-sig")
    correspondence_text = LOCAL_4947.read_text(encoding="utf-8-sig")
    galaxy_readme = GALAXY_README.read_text(encoding="utf-8-sig")
    two_pi_text = TWO_PI_TEX.read_text(encoding="utf-8-sig")
    phase_formula = json.loads(PHASE_FORMULA.read_text(encoding="utf-8-sig"))
    motion_formula = json.loads(MOTION_FORMULA.read_text(encoding="utf-8-sig"))
    normalization_formula = json.loads(NORMALIZATION_FORMULA.read_text(encoding="utf-8-sig"))

    q_match = re.search(r"q\s*=\s*([0-9.]+)\s+for ROTMOD mode", galaxy_readme)
    if q_match is None:
        raise RuntimeError("locked galaxy q was not found")
    q_galaxy = float(q_match.group(1))
    source_clause_checks = {
        "prior_logistic_equations_present": "dn/d ln R=q n(1-n)" in interface_text and "db/d ln R=-s b(1-b)" in interface_text,
        "one_universal_Jgap": "Every empirical sector must share one `J_gap`" in scale_text,
        "O4_irrelevant_mode_identified": "O4 mode is strongly irrelevant" in o4_text and "3.99602545229438" in o4_text,
        "local_psi_zero_exact": "psi=0" in local_text and "O4 tree stress on psi=0" in local_text,
        "matter_tadpole_zero": "delta S_SM/delta psi=0" in source_text,
        "galaxy_parent_carrier_previously_absent": "GALAXY LAW INSIDE Gamma_MTS,res" in freeze_text and "FROZEN" in freeze_text,
        "local_metric_source_rank_one": "rank one" in correspondence_text and "G_Newton" in correspondence_text,
        "galaxy_q_locked": "q = 0.77 for ROTMOD mode" in galaxy_readme,
        "galaxy_canonical_exponential_support": "1 - exp(-(r / L_eff)^q)" in galaxy_readme,
        "phase_formula_is_candidate": phase_formula["status"] == "buffered phase field weak but safe",
        "motion_kernel_is_not_canonical": motion_formula["status"] == "motion-field kernel plausible but null margin narrow",
        "normalization_is_candidate": normalization_formula["status"] == "state-derived normalization candidate for field equation",
        "two_PI_stationarity_source": "stationarity conditions:" in two_pi_text and "\\delta \\Gamma[\\phi,G]" in two_pi_text,
        "two_PI_self_energy_source": "\\delta \\Gamma_2[\\phi,G]" in two_pi_text,
    }
    failed_clauses = [name for name, passed in source_clause_checks.items() if not passed]
    if failed_clauses:
        raise RuntimeError(f"source clause mismatch: {failed_clauses}")

    spectrum = read_csv(SPECTRUM_4940)
    mappings = sorted({row["mapping"] for row in spectrum})
    exponent_rows: list[dict[str, Any]] = []
    mass_exponents: dict[str, float] = {}
    o4_exponents: dict[str, float] = {}
    for mapping in mappings:
        mapping_rows = [row for row in spectrum if row["mapping"] == mapping]
        mass_row = next(row for row in mapping_rows if row["motion_mass_mode"] == "True")
        o4_row = max(mapping_rows, key=lambda row: float(row["beta_eigenvalue_real"]))
        theta_mass = float(mass_row["critical_exponent_real"])
        lambda_o4 = float(o4_row["beta_eigenvalue_real"])
        q_prediction = NATURAL_RADIAL_SCALE_EXPONENT * theta_mass
        s_prediction = NATURAL_RADIAL_SCALE_EXPONENT * lambda_o4
        required_scale_exponent = q_galaxy / theta_mass
        mass_exponents[mapping] = theta_mass
        o4_exponents[mapping] = lambda_o4
        exponent_rows.append(
            {
                "mapping": mapping,
                "galaxy_locked_q": q_galaxy,
                "phase_q_equals_locked_q_assumption": "COMPARISON_ONLY_NOT_DERIVED",
                "theta_mass_parent": theta_mass,
                "natural_scale_exponent_zeta": NATURAL_RADIAL_SCALE_EXPONENT,
                "q_parent_zeta_theta": q_prediction,
                "q_parent_over_locked_q": q_prediction / q_galaxy,
                "relative_gap_over_parent": abs(q_prediction - q_galaxy) / q_prediction,
                "zeta_required_to_force_locked_q": required_scale_exponent,
                "zeta_required_differs_from_spectral_shell": not math.isclose(required_scale_exponent, 1.0, rel_tol=0.05),
                "lambda_O4_parent": lambda_o4,
                "s_parent_if_boundary_is_O4": s_prediction,
                "direct_locked_q_match_within_5_percent": math.isclose(q_prediction, q_galaxy, rel_tol=0.05),
                "status": "LOGISTIC_FORM_DERIVED_NUMERIC_LOCKED_Q_MISMATCH",
                "passed": True,
                "checkpoint_marker": MARKER,
                "valid_for_full_MTS_claim": False,
                "source_checked_date": CHECKED_DATE,
            }
        )

    representative_q = sum(mass_exponents.values()) / len(mass_exponents)
    representative_s = sum(o4_exponents.values()) / len(o4_exponents)
    derivative_step = 1.0e-5
    sample_logs = [-8.0 + 0.1 * index for index in range(161)]
    n_errors: list[float] = []
    b_errors: list[float] = []
    exponential_residuals: list[float] = []
    for log_radius in sample_logs:
        n_value = logistic_up(log_radius, representative_q)
        n_derivative = (
            logistic_up(log_radius + derivative_step, representative_q)
            - logistic_up(log_radius - derivative_step, representative_q)
        ) / (2.0 * derivative_step)
        n_errors.append(abs(n_derivative - representative_q * n_value * (1.0 - n_value)))
        b_value = logistic_down(log_radius, representative_s)
        b_derivative = (
            logistic_down(log_radius + derivative_step, representative_s)
            - logistic_down(log_radius - derivative_step, representative_s)
        ) / (2.0 * derivative_step)
        b_errors.append(abs(b_derivative + representative_s * b_value * (1.0 - b_value)))

        x_to_q = math.exp(q_galaxy * log_radius)
        exponential_tail = math.exp(-x_to_q)
        canonical_support = 1.0 - exponential_tail
        canonical_derivative = q_galaxy * x_to_q * exponential_tail
        logistic_derivative = q_galaxy * canonical_support * (1.0 - canonical_support)
        exponential_residuals.append(abs(canonical_derivative - logistic_derivative))

    logistic_rows = tagged(
        [
            {
                "derivation_id": "LOG4948_00_shell_map",
                "object": "covariant spectral shell at physical radius R",
                "definition": "k(R)=xi/R so d ln k/d ln R=-1",
                "derived_equation": "constant xi changes transition radius but not exponent",
                "condition_or_boundary": "shell/Laplacian mode identification; not a dynamical source-amplitude law",
                "status": "RADIAL_LOG_DERIVATIVE_DERIVED",
                "passed": True,
            },
            {
                "derivation_id": "LOG4948_01_growing_ratio",
                "object": "relevant motion-mass eigenmode ratio r_n",
                "definition": "r_n=C_n(m_gap/k)^theta_mass",
                "derived_equation": "d ln r_n/d ln R=theta_mass",
                "condition_or_boundary": "C_n positive and independent of R after source matching",
                "status": "PARENT_EIGENMODE_SCALING_DERIVED",
                "passed": True,
            },
            {
                "derivation_id": "LOG4948_02_growing_occupation",
                "object": "n=r_n/(1+r_n)",
                "definition": "projective positive spectral occupation",
                "derived_equation": "dn/d ln R=theta_mass n(1-n)",
                "condition_or_boundary": "0<=n<=1 and positive projected weight",
                "status": "LOGISTIC_FORM_EXACT",
                "passed": max(n_errors) < 1.0e-9,
            },
            {
                "derivation_id": "LOG4948_03_decaying_ratio",
                "object": "irrelevant O4 eigenmode ratio r_b",
                "definition": "r_b=C_b(k/m_gap)^lambda_O4",
                "derived_equation": "d ln r_b/d ln R=-lambda_O4",
                "condition_or_boundary": "identifying the only motion-tagged irrelevant direction with boundary occupation",
                "status": "CONDITIONAL_O4_BOUNDARY_SCALING",
                "passed": True,
            },
            {
                "derivation_id": "LOG4948_04_decaying_occupation",
                "object": "b=r_b/(1+r_b)",
                "definition": "projective positive boundary spectral weight",
                "derived_equation": "db/d ln R=-lambda_O4 b(1-b)",
                "condition_or_boundary": "O4 amplitude and stress must survive the physical galaxy background",
                "status": "LOGISTIC_FORM_EXACT_AMPLITUDE_GATE_OPEN",
                "passed": max(b_errors) < 1.0e-9,
            },
            {
                "derivation_id": "LOG4948_05_single_mode_complement",
                "object": "b=1-n",
                "definition": "one two-state occupation rather than two eigenmodes",
                "derived_equation": "db/d ln R=-q b(1-b) so s=q and R_b=R_n",
                "condition_or_boundary": "cannot represent independent q,s or independent transition radii",
                "status": "EXACT_RESTRICTION",
                "passed": True,
            },
            {
                "derivation_id": "LOG4948_06_canonical_support",
                "object": "f=1-exp[-(R/L_eff)^q_locked]",
                "definition": "current canonical galaxy support saturation",
                "derived_equation": "df/d ln R=q x^q exp(-x^q) != q f(1-f)",
                "condition_or_boundary": "the logistic occupation may multiply/source f but is not algebraically identical to f",
                "status": "CANONICAL_EXPONENTIAL_IS_NOT_LOGISTIC",
                "passed": max(exponential_residuals) > 1.0e-3,
            },
        ]
    )

    source_gate_rows = tagged(
        [
            {
                "gate_id": "SRCG4948_00_universal_length",
                "question": "does one J_gap define the motion length without arena retuning",
                "parent_result": "ell_gap=1/m_gap=sqrt(G_N/J_gap)",
                "galaxy_requirement": "transition radii may vary by source but J_gap must not",
                "decision": "PASS_SYMBOLIC_UNIVERSAL_SCALE",
                "derivation": "R_n=xi ell_gap C_n^(-1/theta); R_b=xi ell_gap C_b^(1/lambda)",
                "passed": True,
            },
            {
                "gate_id": "SRCG4948_01_source_amplitude",
                "question": "does visible matter linearly source the motion eigenmode",
                "parent_result": "delta S_matter/delta psi=0 and Gamma_eff^(1,n)|psi=0=0",
                "galaxy_requirement": "nonzero source-dependent C_n and C_b",
                "decision": "DIRECT_CLASSICAL_SOURCE_REJECTED",
                "derivation": "with vacuum boundary data the exact psi=0 solution sets the classical mode amplitude to zero",
                "passed": True,
            },
            {
                "gate_id": "SRCG4948_02_O4_boundary",
                "question": "can the irrelevant O4 mode own the boundary occupation amplitude",
                "parent_result": "lambda_O4 approximately 3.996 but O4 tree stress is zero on psi=0 and curvature correction is derivative suppressed",
                "galaxy_requirement": "order-relevant disk boundary support",
                "decision": "EXPONENT_EXISTS_PHYSICAL_AMPLITUDE_NOT_DERIVED",
                "derivation": "an eigenvalue does not create a populated eigenmode or its stress",
                "passed": True,
            },
            {
                "gate_id": "SRCG4948_03_locked_q",
                "question": "does the natural k proportional 1/R map reproduce the only locked galaxy q",
                "parent_result": f"theta_mass in [{min(mass_exponents.values()):.15g},{max(mass_exponents.values()):.15g}]",
                "galaxy_requirement": f"q_locked={q_galaxy}",
                "decision": "NUMERIC_DIRECT_IDENTIFICATION_REJECTED",
                "derivation": "forcing q_locked requires k proportional R^-zeta with zeta about 0.415 rather than the spectral-shell value one",
                "passed": True,
            },
            {
                "gate_id": "SRCG4948_04_phase_candidate",
                "question": "is the v19 Theta phase field already parent-owned",
                "parent_result": "no Theta field or beta=1.10 coefficient occurs in the parent Hessian",
                "galaxy_requirement": phase_formula["thirdField"]["equation"],
                "decision": "EMPIRICAL_CANDIDATE_NOT_IMPORTED_AS_ACTION",
                "derivation": "the galaxy artifact labels itself weak but safe and keeps the locked law unchanged",
                "passed": True,
            },
            {
                "gate_id": "SRCG4948_05_motion_kernel",
                "question": "is the v19 Xi source/sink kernel already parent-owned",
                "parent_result": "no derived A_source A_sink beta_add beta_sink projection",
                "galaxy_requirement": motion_formula["fieldEquationSketch"],
                "decision": "PLAUSIBLE_NULL_NARROW_CANDIDATE_NOT_IMPORTED",
                "derivation": "N_RC remains external admissibility and the physical normalization is still candidate-level",
                "passed": True,
            },
            {
                "gate_id": "SRCG4948_06_stress",
                "question": "does substituting n or b into the rotation support define a conserved stress tensor",
                "parent_result": "no because n and b are coordinates on spectral weights until varied through an action",
                "galaxy_requirement": "metric source for dynamics and lensing with Bianchi-compatible conservation",
                "decision": "ACTIVATION_STRESS_NOT_DERIVED",
                "derivation": "support-law insertion cannot replace delta Gamma/delta g",
                "passed": True,
            },
            {
                "gate_id": "SRCG4948_07_direct_map",
                "question": "does the current one-point parent Hessian derive the galaxy phase law end to end",
                "parent_result": "logistic coordinate form yes; exponent source amplitude transition radius and stress no",
                "galaxy_requirement": "one universal action-level response",
                "decision": "DIRECT_ONE_POINT_HESSIAN_MAP_REJECTED",
                "derivation": "failure is localized to state/source/stress ownership rather than the logistic algebra",
                "passed": True,
            },
            {
                "gate_id": "SRCG4948_08_composite_route",
                "question": "is there a parent route compatible with psi tadpole zero",
                "parent_result": "the two-point function G=<psi psi> is reflection even and can carry occupation while <psi>=0",
                "galaxy_requirement": "nonzero environmental state with metric stress and no direct scalar charge",
                "decision": "TWO_PI_COMPOSITE_ROUTE_SELECTED_FOR_DERIVATION",
                "derivation": "derive a stationary covariant 2PI state and vary its stress before empirical matching",
                "passed": True,
            },
        ]
    )

    composite_rows = tagged(
        [
            {
                "contract_id": "2PI4948_00_variables",
                "object": "bar_psi=0; G(x,y)=<psi(x)psi(y)>",
                "required_derivation": "retain reflection symmetry while allowing an even motion occupation",
                "acceptance_gate": "G is positive-type after renormalization and bar_psi remains zero",
                "current_status": "PARENT_COMPATIBLE_VARIABLES_DEFINED",
                "passed": True,
            },
            {
                "contract_id": "2PI4948_01_action",
                "object": "Gamma_2PI[g,G]=S_g+S_m+1/2 Tr ln G^-1+1/2 Tr(D^-1[g]G-1)+Gamma_2[g,G]",
                "required_derivation": "construct in the same regulator and Wilson convention as the 4935-4942 parent",
                "acceptance_gate": "no new arena-dependent coupling or unvaried support function",
                "current_status": "STANDARD_VARIATIONAL_CONTRACT_DEFINED",
                "passed": True,
            },
            {
                "contract_id": "2PI4948_02_Dyson",
                "object": "delta Gamma_2PI/delta G=0 -> G^-1=D^-1[g]+2 delta Gamma_2/delta G",
                "required_derivation": "solve on an axisymmetric disk metric with the universal J_gap",
                "acceptance_gate": "vacuum subtraction convergence and stable spectrum",
                "current_status": "EQUATION_DEFINED_NOT_SOLVED",
                "passed": True,
            },
            {
                "contract_id": "2PI4948_03_state",
                "object": "Delta G_state=G_state-G_vac",
                "required_derivation": "select the state from universal initial/boundary data or a parent instability",
                "acceptance_gate": "Delta G_state=0 in the declared local vacuum branch",
                "current_status": "STATE_SELECTION_OPEN",
                "passed": True,
            },
            {
                "contract_id": "2PI4948_04_source",
                "object": "D^-1[g(T_b)] and Sigma[g,G] provide the only current source dependence",
                "required_derivation": "calculate C_n[T_b] and C_b[T_b] from Green-function matching",
                "acceptance_gate": "no galaxy name residual RMSE NFW MOND or N_RC in the physical source",
                "current_status": "SOURCE_AMPLITUDE_CALCULATION_OPEN",
                "passed": True,
            },
            {
                "contract_id": "2PI4948_05_occupation",
                "object": "n=P_n DeltaG/(W_n+P_n DeltaG); b=P_b DeltaG/(W_b+P_b DeltaG)",
                "required_derivation": "define positive projectors P_n P_b and reference weights W_n W_b",
                "acceptance_gate": "0<=n,b<=1 and projectors correspond to parent Hessian modes",
                "current_status": "PROJECTIVE_MAP_DEFINED_PROJECTORS_OPEN",
                "passed": True,
            },
            {
                "contract_id": "2PI4948_06_transitions",
                "object": "R_n=xi sqrt(G_N/J_gap) C_n^(-1/theta); R_b=xi sqrt(G_N/J_gap) C_b^(1/lambda)",
                "required_derivation": "show source amplitudes generate observed source-dependent scales with one J_gap",
                "acceptance_gate": "same J_gap and xi convention for every galaxy",
                "current_status": "UNIVERSAL_SCALE_SOURCE_AMPLITUDE_FACTORISATION_DERIVED",
                "passed": True,
            },
            {
                "contract_id": "2PI4948_07_stress",
                "object": "T_occ,mn=-2/sqrt(-g) delta(Gamma_2PI-S_g)/delta g^mn at stationary G",
                "required_derivation": "include explicit metric dependence of D^-1 Gamma_2 and regulator counterterms",
                "acceptance_gate": "finite stress sources both rotation and lensing",
                "current_status": "VARIATIONAL_STRESS_DEFINITION_DERIVED_NUMERIC_PROFILE_OPEN",
                "passed": True,
            },
            {
                "contract_id": "2PI4948_08_Ward",
                "object": "nabla^m(T_matter+T_occ)_mn=0 on metric and Dyson equations",
                "required_derivation": "use a diffeomorphism-covariant truncation and counterterm basis",
                "acceptance_gate": "Bianchi residual zero before rotation-curve fitting",
                "current_status": "WARD_CONTRACT_DEFINED",
                "passed": True,
            },
            {
                "contract_id": "2PI4948_09_local_limit",
                "object": "Delta G_state -> 0 implies T_occ -> 0 and returns checkpoint 4947",
                "required_derivation": "prove local vacuum is stable under the chosen 2PI truncation",
                "acceptance_gate": "no scalar charge and no standard PPN shift",
                "current_status": "REQUIRED_CORRESPONDENCE_LIMIT_DEFINED",
                "passed": True,
            },
            {
                "contract_id": "2PI4948_10_empirical",
                "object": "derive native disk support and compare to canonical/v18 held-out curves",
                "required_derivation": "freeze parent parameters before SPARC/ETG scoring",
                "acceptance_gate": "same-action lensing and no per-galaxy J_gap or Wilson retuning",
                "current_status": "EMPIRICAL_EXECUTION_DEFERRED_UNTIL_STRESS_EXISTS",
                "passed": True,
            },
        ]
    )

    galaxy_snapshot_rows = tagged(
        [
            {
                "snapshot_id": "GAL4948_00_public_repo",
                "repository": "https://github.com/Martin123132/MTS-Galaxy-Lab-",
                "local_readonly_clone": str(GALAXY_REPO),
                "head": galaxy_head,
                "expected_head": EXPECTED_GALAXY_HEAD,
                "working_tree_clean": not bool(galaxy_status),
                "README_sha256": digest(GALAXY_README),
                "failure_lab_sha256": digest(GALAXY_SCRIPT),
                "locked_q": q_galaxy,
                "canonical_support": "Gamma0 L_eff [1-exp(-(R/L_eff)^q)]",
                "phase_formula_sha256": digest(PHASE_FORMULA),
                "motion_formula_sha256": digest(MOTION_FORMULA),
                "normalization_formula_sha256": digest(NORMALIZATION_FORMULA),
                "repository_modified_by_checkpoint": False,
                "status": "READ_ONLY_SOURCE_SNAPSHOT",
                "passed": True,
            }
        ]
    )

    checks = {
        "source_hashes_match": not hash_failures,
        "authoritative_clauses_match": not failed_clauses,
        "galaxy_head_locked": galaxy_head == EXPECTED_GALAXY_HEAD,
        "galaxy_worktree_clean": not bool(galaxy_status),
        "two_parent_mappings": len(mappings) == 2,
        "mass_exponents_positive": all(value > 0.0 for value in mass_exponents.values()),
        "O4_exponents_near_four": all(math.isclose(value, 4.0, rel_tol=0.01) for value in o4_exponents.values()),
        "projective_n_logistic_numeric": max(n_errors) < 1.0e-9,
        "projective_b_logistic_numeric": max(b_errors) < 1.0e-9,
        "canonical_exponential_not_logistic": max(exponential_residuals) > 1.0e-3,
        "natural_parent_q_does_not_match_locked_q": all(not row["direct_locked_q_match_within_5_percent"] for row in exponent_rows),
        "forcing_locked_q_requires_non_shell_zeta": all(row["zeta_required_differs_from_spectral_shell"] for row in exponent_rows),
        "all_logistic_derivation_rows_pass": all(row["passed"] for row in logistic_rows),
        "all_source_gate_decisions_recorded": all(row["passed"] for row in source_gate_rows),
        "direct_one_point_map_rejected": any(row["decision"] == "DIRECT_ONE_POINT_HESSIAN_MAP_REJECTED" for row in source_gate_rows),
        "composite_route_selected": any(row["decision"] == "TWO_PI_COMPOSITE_ROUTE_SELECTED_FOR_DERIVATION" for row in source_gate_rows),
        "all_2PI_contract_rows_recorded": all(row["passed"] for row in composite_rows),
        "all_rows_full_MTS_nonclaim": all(not row["valid_for_full_MTS_claim"] for table in (logistic_rows, exponent_rows, source_gate_rows, composite_rows, galaxy_snapshot_rows) for row in table),
    }

    result = {
        "marker": MARKER,
        "source_hashes": source_hashes,
        "source_clause_checks": source_clause_checks,
        "galaxy_snapshot": {
            "repository": "https://github.com/Martin123132/MTS-Galaxy-Lab-",
            "head": galaxy_head,
            "working_tree_clean": not bool(galaxy_status),
            "locked_q": q_galaxy,
            "canonical_support_is_logistic_occupation": False,
        },
        "projective_theorem": {
            "spectral_shell": "k=xi/R",
            "growing_ratio": "r_n=C_n(m_gap/k)^theta",
            "growing_occupation": "n=r_n/(1+r_n) -> dn/dlnR=theta n(1-n)",
            "decaying_ratio": "r_b=C_b(k/m_gap)^lambda",
            "decaying_occupation": "b=r_b/(1+r_b) -> db/dlnR=-lambda b(1-b)",
            "single_mode_complement": "b=1-n requires s=q and R_b=R_n",
            "transition_scales": "R_n=xi sqrt(G_N/J_gap) C_n^(-1/theta); R_b=xi sqrt(G_N/J_gap) C_b^(1/lambda)",
            "max_numeric_n_residual": max(n_errors),
            "max_numeric_b_residual": max(b_errors),
        },
        "parent_exponents": {
            "theta_mass_by_mapping": mass_exponents,
            "lambda_O4_by_mapping": o4_exponents,
            "locked_q_comparison_only": q_galaxy,
            "required_zeta_by_mapping": {row["mapping"]: row["zeta_required_to_force_locked_q"] for row in exponent_rows},
            "direct_locked_q_match": False,
        },
        "source_and_stress": {
            "visible_linear_psi_source": False,
            "vacuum_boundary_classical_psi_amplitude": 0.0,
            "O4_tree_stress_on_psi_zero": 0.0,
            "source_dependent_transition_requires_Cn_Cb": True,
            "Cn_Cb_derived_from_current_parent": False,
            "activation_stress_derived_from_current_one_point_Hessian": False,
        },
        "selected_survivor": {
            "route": "reflection-even composite two-point occupation G=<psi psi> in a covariant 2PI action",
            "reason": "can remain nonzero with bar_psi=0 and can be varied for a conserved metric stress",
            "current_status": "contract defined; state source projectors stress profile and empirical calculation open",
        },
        "checks": checks,
        "claim_boundary": {
            "projective_logistic_shape_from_parent_eigenmode_derived": True,
            "natural_radial_shell_log_derivative_derived": True,
            "locked_galaxy_q_predicted_by_parent_mass_mode": False,
            "galaxy_phase_q_proved_identical_to_locked_support_q": False,
            "source_dependent_Cn_Cb_derived": False,
            "O4_boundary_stress_large_enough_for_galaxies": False,
            "activation_stress_tensor_calculated": False,
            "direct_one_point_Hessian_to_galaxy_map": False,
            "two_PI_composite_contract_defined": True,
            "two_PI_composite_disk_solution_calculated": False,
            "galaxy_repository_modified": False,
            "full_MTS_galaxy_unification": False,
        },
    }

    write_csv(LOGISTIC_CSV, logistic_rows)
    write_csv(EXPONENT_CSV, exponent_rows)
    write_csv(SOURCE_GATE_CSV, source_gate_rows)
    write_csv(COMPOSITE_CSV, composite_rows)
    write_csv(GALAXY_SNAPSHOT_CSV, galaxy_snapshot_rows)
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    failed_checks = [name for name, passed in checks.items() if not passed]
    print(f"{MARKER}_THETA_MIN={min(mass_exponents.values()):.15g}", flush=True)
    print(f"{MARKER}_THETA_MAX={max(mass_exponents.values()):.15g}", flush=True)
    print(f"{MARKER}_O4_LAMBDA={representative_s:.15g}", flush=True)
    print(f"{MARKER}_LOCKED_Q={q_galaxy:.15g}", flush=True)
    print(f"{MARKER}_FAILED={len(failed_checks)}", flush=True)
    print(f"{MARKER}_RESULT_SHA256={digest(RESULT_JSON)}", flush=True)
    if failed_checks:
        for failure in failed_checks:
            print(f"{MARKER}_FAIL={failure}", flush=True)
        return 1
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
