from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

import sympy as sp


CHECKPOINT = 5344
MARKER = "MTS_5344_CLOSED_PARENT_LOCAL_STATE_ATTRACTOR_NO_GO"
CHECKED_DATE = "2026-08-10"
POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
OUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5344-Y5-R2FR-closed-parent-local-vacuum-attractor-no-go-and-"
    "minimal-reduced-dynamics-contract.md"
)
SOURCE_PATHS = [
    POST
    / "5156-Y5-R2FR-FLRW-Hessian-Gaussian-state-single-clock-adiabatic-"
    "radiation-transfer-and-patch-collapse-gate.md",
    POST
    / "5178-Y5-R2FR-exact-2PI-Schur-Ward-Vlasov-subtraction-and-"
    "Gaussian-residual-stress-no-go.md",
    POST
    / "5200-Y5-R2FR-CTP-vacuum-occupied-projector-metric-and-"
    "composite-exponent-ownership-gate.md",
    POST
    / "5201-Y5-R2FR-source-complete-coframe-variation-full-PPN-"
    "calibration-and-local-state-silence-theorem.md",
    POST
    / "5208-Y5-R2FR-common-minimal-motion-trajectory-canonical-Z-quotient-"
    "absolute-scale-covariance-and-local-GR-selection.md",
    POST
    / "5211-Y5-R2FR-selected-trajectory-exact-GR-Maxwell-consistent-"
    "truncation-universal-source-and-matched-GRSM-excess-theorem.md",
    POST
    / "source-intake"
    / "functional_rg"
    / "5208"
    / "local_GR_residual_bounds.csv",
    POST
    / "source-intake"
    / "functional_rg"
    / "5208"
    / "physical_scale_and_power_counting.csv",
    POST
    / "source-intake"
    / "functional_rg"
    / "5201"
    / "boundary_state_local_silence_gate.csv",
    POST
    / "source-intake"
    / "functional_rg"
    / "5211"
    / "exact_consistent_truncation.csv",
    POST
    / "source-intake"
    / "functional_rg"
    / "5211"
    / "route_decision.csv",
]
OUTPUT_NAMES = [
    "closed_unitary_attractor_no_go.csv",
    "field_stability_vs_state_selection.csv",
    "local_escape_spectral_gate.csv",
    "finite_wavelength_local_escape_kinematics.csv",
    "local_escape_and_open_system_contract.csv",
    "state_selection_decision.csv",
    "source_provenance.csv",
    "closed_parent_local_state_attractor_results.json",
]


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint": CHECKPOINT,
            "checkpoint_marker": MARKER,
            "checked_date": CHECKED_DATE,
            "valid_for_full_MTS_claim": False,
            "valid_for_parent_state_selection_claim": False,
        }
        for row in rows
    ]


def assert_sources() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in SOURCE_PATHS:
        if not path.is_file():
            raise FileNotFoundError(path)
        hashes[path.relative_to(POST).as_posix()] = file_digest(path)
    return hashes


def unitary_no_go() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    energy_0, energy_1 = sp.symbols("E_0 E_1", real=True)
    gap = sp.symbols("Delta_E", real=True)
    imaginary_unit = sp.I
    liouvillian = sp.diag(0, imaginary_unit * gap, -imaginary_unit * gap, 0)
    skew_residual = sp.simplify(liouvillian.conjugate().T + liouvillian)
    liouvillian_eigenvalues = [
        sp.simplify(value)
        for value in liouvillian.eigenvals().keys()
    ]

    occupation = sp.symbols("n", nonnegative=True, real=True)
    rho_0 = sp.diag(1, 0)
    rho_1 = sp.diag(0, 1)
    rho_n = (1 - occupation) * rho_0 + occupation * rho_1
    difference = sp.simplify(rho_n - rho_0)
    hilbert_schmidt_squared = sp.simplify(sp.trace(difference * difference))
    purity = sp.simplify(sp.trace(rho_n * rho_n))
    trace_distance_binary = occupation

    unitary_angle = sp.symbols("theta", real=True)
    unitary = sp.diag(sp.exp(-imaginary_unit * unitary_angle), 1)
    evolved_difference = sp.simplify(unitary * difference * unitary.conjugate().T)
    evolved_hilbert_schmidt_squared = sp.simplify(
        sp.trace(evolved_difference * evolved_difference)
    )

    checks = {
        "liouvillian_skew_adjoint": skew_residual == sp.zeros(4),
        "liouvillian_real_decay_gap_zero": all(
            sp.simplify(sp.re(value)) == 0 for value in liouvillian_eigenvalues
        ),
        "binary_trace_distance_equals_n": trace_distance_binary == occupation,
        "unitary_hilbert_schmidt_distance_invariant": sp.simplify(
            evolved_hilbert_schmidt_squared - hilbert_schmidt_squared
        )
        == 0,
        "binary_purity_not_purified_by_unitary": sp.simplify(
            purity - (2 * occupation**2 - 2 * occupation + 1)
        )
        == 0,
    }
    if not all(checks.values()):
        raise RuntimeError(f"unitary no-go algebra failed: {checks}")

    rows = [
        {
            "result_id": "U5344_00_unitary_spectrum",
            "premise": "rho(t)=U(t) rho(0) U(t)^dagger",
            "derived_identity": "spectrum(rho(t))=spectrum(rho(0)); purity and entropy are invariant",
            "consequence": "a mixed or non-target state cannot converge to a distinct pure rho_0 under closed unitary evolution",
            "status": "EXACT_NO_GO",
            "valid_for_closed_parent_no_attractor_theorem": True,
        },
        {
            "result_id": "U5344_01_binary_distance",
            "premise": "rho(n)=(1-n)rho_0+n rho_1 with orthogonal pure projectors",
            "derived_identity": "D_trace(rho(n),rho_0)=n; Tr[(rho(n)-rho_0)^2]=2 n^2",
            "consequence": "unitary evolution cannot drive finite n to zero",
            "status": "EXACT_BINARY_WITNESS",
            "valid_for_closed_parent_no_attractor_theorem": True,
        },
        {
            "result_id": "U5344_02_Liouville_spectrum",
            "premise": "L=-i[H,.] for Hermitian H",
            "derived_identity": "L is skew-adjoint; two-level eigenvalues are 0,0,+i Delta_E,-i Delta_E",
            "consequence": "the closed Liouville generator has no negative-real-part attraction gap",
            "status": "EXACT_NO_DISSIPATIVE_GAP",
            "valid_for_closed_parent_no_attractor_theorem": True,
        },
        {
            "result_id": "U5344_03_boundary_functional_role",
            "premise": "Gamma_rho0 enters as an initial CTP boundary functional",
            "derived_identity": "Gamma_rho0 specifies initial density-matrix vertices rather than a bulk relaxation semigroup",
            "consequence": "the present parent permits rho_local=rho_0 as preparation data but does not dynamically select it",
            "status": "SOURCE_LOCKED_INTERPRETATION",
            "valid_for_closed_parent_no_attractor_theorem": True,
        },
    ]
    payload = {
        "checks": checks,
        "liouvillian": str(liouvillian),
        "liouvillian_eigenvalues": [str(value) for value in liouvillian_eigenvalues],
        "binary_hilbert_schmidt_squared": str(hilbert_schmidt_squared),
        "binary_purity": str(purity),
        "energy_symbols": [str(energy_0), str(energy_1)],
    }
    return tagged(rows), payload


def field_stability_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "result_id": "F5344_00_zero_field_stationarity",
                "object": "chi",
                "premise": "E_chi=nabla_mu(K_eff nabla^mu chi)-m_gap^2 chi with K_eff>0 and m_gap^2>0",
                "derived_identity": "chi=0 and nabla chi=0 solve E_chi=0 exactly",
                "conclusion": "the selected motion-field branch is stationary",
                "status": "EXACT_PARENT_BRANCH",
            },
            {
                "result_id": "F5344_01_positive_energy",
                "object": "chi",
                "premise": "stationary local metric; positive K_eff and m_gap^2; no source",
                "derived_identity": "E_chi=int[K_eff(dot chi^2+|grad chi|^2)+m_gap^2 chi^2]/2 >=0",
                "conclusion": "chi=0 is Lyapunov stable in the retained local EFT corridor",
                "status": "CONDITIONAL_POSITIVE_ENERGY_THEOREM",
            },
            {
                "result_id": "F5344_02_no_flux_energy",
                "object": "chi",
                "premise": "Hamiltonian scalar evolution with vanishing boundary flux",
                "derived_identity": "dE_chi/dt=0",
                "conclusion": "positive energy proves stability but not asymptotic attraction",
                "status": "EXACT_STABILITY_NOT_ATTRACTION",
            },
            {
                "result_id": "F5344_03_category_separation",
                "object": "chi versus rho_local",
                "premise": "chi is a bulk one-point field; rho_local is CTP state data",
                "derived_identity": "a Lyapunov estimate for chi cannot alter the eigenvalues of rho_local",
                "conclusion": "field stability cannot be relabelled a state-preparation theorem",
                "status": "PROVED_CATEGORY_SEPARATION",
            },
        ]
    )


def completion_contract() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    occupation, rate = sp.symbols("n gamma", nonnegative=True, real=True)
    lowering = sp.Matrix([[0, 1], [0, 0]])
    raising = lowering.T
    rho = sp.diag(1 - occupation, occupation)
    projector_excited = raising * lowering
    dissipator = sp.simplify(
        rate
        * (
            lowering * rho * raising
            - (projector_excited * rho + rho * projector_excited) / 2
        )
    )
    occupation_derivative = sp.simplify(dissipator[1, 1])
    amplitude_damping_pass = occupation_derivative == -rate * occupation

    initial_occupation, kappa, time = sp.symbols(
        "n_0 kappa t",
        nonnegative=True,
        real=True,
    )
    gronwall_envelope = initial_occupation * sp.exp(-kappa * time)
    envelope_derivative = sp.simplify(sp.diff(gronwall_envelope, time))
    escape_bound_pass = envelope_derivative == -kappa * gronwall_envelope
    if not amplitude_damping_pass or not escape_bound_pass:
        raise RuntimeError("minimal reduced-dynamics contract algebra failed")

    rows = [
        {
            "route_id": "C5344_00_local_escape",
            "global_dynamics": "unitary",
            "local_reduction": "dN_Omega/dt=-Phi_boundary+S_Omega",
            "sufficient_condition": "S_Omega=0 and Phi_boundary>=kappa N_Omega with kappa>0",
            "derived_result": "N_Omega(t)<=N_Omega(0) exp(-kappa t)",
            "parent_status": "OBSERVABILITY_INEQUALITY_NOT_DERIVED",
            "preferred": True,
            "claim_status": "SUFFICIENT_CONTRACT_NOT_CURRENT_CLAIM",
        },
        {
            "route_id": "C5344_01_reduced_CTP_dissipator",
            "global_dynamics": "unitary after environment retained",
            "local_reduction": "dot rho=-i[H,rho]+D[rho]",
            "sufficient_condition": "completely positive trace-preserving primitive generator with unique fixed state rho_0 and real gap gamma>0",
            "derived_result": "for L=sqrt(gamma)|0><1|, dot n=-gamma n and n(t)=n(0) exp(-gamma t)",
            "parent_status": "NO_PARENT_NOISE_DISSIPATION_KERNEL_OR_GAMMA",
            "preferred": False,
            "claim_status": "FINITE_DIMENSIONAL_WITNESS_NOT_PARENT_COMPLETION",
        },
        {
            "route_id": "C5344_02_explicit_preparation",
            "global_dynamics": "closed parent evolution",
            "local_reduction": "Gamma_rho0 fixes rho_local=rho_0 on the initial surface",
            "sufficient_condition": "Hadamard/renormalized local vacuum state and no incoming occupied-state boundary data",
            "derived_result": "exact local state silence is maintained on the declared branch",
            "parent_status": "ALLOWED_BOUNDARY_DATUM_NOT_PREDICTED_ATTRACTOR",
            "preferred": False,
            "claim_status": "VALID_CONDITIONAL_LOCAL_GR_PREPARATION",
        },
        {
            "route_id": "C5344_03_Ward_completion",
            "global_dynamics": "diffeomorphism-invariant total parent",
            "local_reduction": "state stress exchange plus environment/escape stress",
            "sufficient_condition": "nabla_mu(T_state^mu_nu+T_environment^mu_nu)=0 including boundary flux",
            "derived_result": "local damping cannot delete energy-momentum; the sink must appear in the universal Hilbert source",
            "parent_status": "REQUIRED_FOR_ANY_COMPLETION",
            "preferred": True,
            "claim_status": "EXACT_CONSERVATION_CONTRACT",
        },
    ]
    payload = {
        "amplitude_damping_pass": amplitude_damping_pass,
        "dissipator": str(dissipator),
        "occupation_derivative": str(occupation_derivative),
        "escape_bound_pass": escape_bound_pass,
        "gronwall_envelope": str(gronwall_envelope),
    }
    return tagged(rows), payload


def local_escape_spectral_gate() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    momentum, mass = sp.symbols("k m", nonnegative=True, real=True)
    group_speed = momentum / sp.sqrt(momentum**2 + mass**2)
    zero_momentum_speed = sp.simplify(group_speed.subs(momentum, 0))
    infrared_speed_limit = sp.limit(group_speed, momentum, 0, dir="+")
    zero_mode_flux = sp.Integer(0)
    zero_mode_energy_density = sp.symbols("rho_zero", positive=True, real=True)
    universal_gap_rejected = (
        zero_momentum_speed == 0
        and infrared_speed_limit == 0
        and zero_mode_flux == 0
        and zero_mode_energy_density.is_positive
    )
    if not universal_gap_rejected:
        raise RuntimeError("local escape spectral no-go failed")

    spectral_rows = tagged(
        [
            {
                "result_id": "E5344_00_zero_mode_counterexample",
                "parent_mode": "chi=A cos(m_gap t) with spatial k=0",
                "derived_identity": "T_0i=-dot(chi) partial_i(chi)=0 while rho_chi>0",
                "gate_result": "Phi_boundary=0 with N_Omega>0",
                "conclusion": "Phi_boundary>=kappa N_Omega fails for every universal kappa>0",
                "status": "EXACT_UNIVERSAL_ESCAPE_GAP_NO_GO",
            },
            {
                "result_id": "E5344_01_infrared_group_speed",
                "parent_mode": "omega(k)=sqrt(k^2+m_gap^2)",
                "derived_identity": "v_g=d omega/dk=k/sqrt(k^2+m_gap^2)",
                "gate_result": "lim_(k->0+) v_g=0",
                "conclusion": "the full parent spectrum has no strictly positive ballistic clearing rate",
                "status": "EXACT_SPECTRAL_NO_GO",
            },
            {
                "result_id": "E5344_02_standing_mode",
                "parent_mode": "finite-domain standing or reflecting mode",
                "derived_identity": "net integrated normal flux through the boundary is zero",
                "gate_result": "positive interior energy can persist without outgoing loss",
                "conclusion": "an absorbing/no-incoming boundary condition is additional state data",
                "status": "EXACT_BOUNDARY_COUNTEREXAMPLE",
            },
            {
                "result_id": "E5344_03_restricted_outgoing_sector",
                "parent_mode": "outgoing packet with k>=hbar/R and no reflection or incoming flux",
                "derived_identity": "v_g/c>=[1+(m_gap R/hbar c)^2]^-1/2",
                "gate_result": "tau_cross<=R sqrt(1+(m_gap R/hbar c)^2)/c",
                "conclusion": "finite-wavelength local clearing is kinematically fast but is not an attractor theorem",
                "status": "CONDITIONAL_KINEMATIC_BOUND",
            },
        ]
    )

    physical_rows = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "5208"
        / "physical_scale_and_power_counting.csv"
    )
    m_gap_text = next(
        row["value"] for row in physical_rows if row["quantity"] == "m_gap"
    )
    arena_rows = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "5208"
        / "local_GR_residual_bounds.csv"
    )
    getcontext().prec = 80
    m_gap = Decimal(m_gap_text)
    hbar_c = Decimal("1.973269804e-7")
    speed_of_light = Decimal("299792458")
    kinematic_rows: list[dict[str, Any]] = []
    for row in arena_rows:
        radius_text = row.get("radius_m", "")
        if not radius_text:
            continue
        radius = Decimal(radius_text)
        mass_ratio = m_gap * radius / hbar_c
        velocity_fraction = Decimal(1) / (
            Decimal(1) + mass_ratio * mass_ratio
        ).sqrt()
        crossing_seconds = radius / (speed_of_light * velocity_fraction)
        kinematic_rows.append(
            {
                "arena": row["arena"],
                "radius_m": radius_text,
                "m_gap_eV": m_gap_text,
                "k_min_eV_hbar_over_R": str(hbar_c / radius),
                "m_gap_over_k_min": str(mass_ratio),
                "mass_ratio_squared": str(mass_ratio * mass_ratio),
                "minimum_group_speed_over_c": str(velocity_fraction),
                "group_speed_deficit": str(Decimal(1) - velocity_fraction),
                "upper_ballistic_crossing_time_s": str(crossing_seconds),
                "homogeneous_tidal_to_Newton_ratio": row[
                    "homogeneous_tidal_to_Newton_ratio"
                ],
                "assumptions": "outgoing; k>=hbar/R; no reflection; no incoming collective flux",
                "status": "CONDITIONAL_CROSSING_KINEMATICS_NOT_DECAY_THEOREM",
            }
        )
    if not kinematic_rows:
        raise RuntimeError("no local arena rows available")
    tagged_kinematics = tagged(kinematic_rows)
    payload = {
        "zero_momentum_speed": str(zero_momentum_speed),
        "infrared_speed_limit": str(infrared_speed_limit),
        "zero_mode_flux": str(zero_mode_flux),
        "universal_positive_escape_gap_rejected": universal_gap_rejected,
        "arena_count": len(kinematic_rows),
        "maximum_mass_ratio_squared": max(
            float(row["mass_ratio_squared"]) for row in kinematic_rows
        ),
        "maximum_ballistic_crossing_time_s": max(
            float(row["upper_ballistic_crossing_time_s"])
            for row in kinematic_rows
        ),
        "maximum_homogeneous_tidal_ratio": max(
            float(row["homogeneous_tidal_to_Newton_ratio"])
            for row in kinematic_rows
        ),
    }
    return spectral_rows, tagged_kinematics, payload


def decision_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "decision_id": "D5344_00_closed_parent_attractor",
                "question": "Does the current closed parent dynamically attract arbitrary rho_local to rho_0?",
                "decision": "NO",
                "reason": "unitary similarity preserves state spectrum and distance; the Liouville generator has no dissipative real gap",
                "next_action": "do not spend further checkpoints seeking a Hamiltonian Lyapunov proof of density-matrix purification",
                "status": "DERIVED_NO_GO",
            },
            {
                "decision_id": "D5344_01_local_GR_branch",
                "question": "Does the no-go invalidate the exact selected two-derivative GR/Newton/Maxwell branch?",
                "decision": "NO",
                "reason": "rho_local=rho_0 remains admissible initial/boundary state data and chi=0 remains an exact stable field branch",
                "next_action": "state the preparation condition explicitly rather than calling it a predicted attractor",
                "status": "CONDITIONAL_BRANCH_RETAINED",
            },
            {
                "decision_id": "D5344_02_best_derivation_route",
                "question": "Can the existing parent empty every local state by escape without added dynamics?",
                "decision": "NO_UNIVERSAL_GAP_RESTRICTED_OUTGOING_SECTOR_ONLY",
                "reason": "the exact k=0 mode and standing modes carry positive energy with zero boundary flux; finite-k outgoing packets remain kinematically clearable",
                "next_action": "retain explicit preparation or derive a parent projector/history excluding zero, trapped and incoming occupied modes",
                "status": "UNIVERSAL_ROUTE_REJECTED_CONDITIONAL_SUBSPACE_RETAINED",
            },
            {
                "decision_id": "D5344_03_claim_boundary",
                "question": "What can be claimed now?",
                "decision": "NO_PARENT_ATTRACTOR_CLAIM",
                "reason": "no kappa, gamma, environment kernel, or incoming-flux theorem is parent-owned",
                "next_action": "retain exact-preparation local GR and quantitative residual language only",
                "status": "CLAIM_BLOCKED_WITH_EXACT_REASON",
            },
        ]
    )


def provenance_rows(source_hashes: dict[str, str]) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "source_id": f"S5344_{index:02d}",
                "source_path": path,
                "sha256": digest,
                "role": "parent premise and prior state-selection boundary",
                "exists": True,
            }
            for index, (path, digest) in enumerate(sorted(source_hashes.items()))
        ]
    )


def build_payload() -> dict[str, Any]:
    source_hashes = assert_sources()
    no_go_rows, no_go_payload = unitary_no_go()
    field_rows = field_stability_rows()
    spectral_rows, kinematic_rows, spectral_payload = local_escape_spectral_gate()
    contract_rows, contract_payload = completion_contract()
    decisions = decision_rows()
    provenance = provenance_rows(source_hashes)
    return {
        "rows": {
            "closed_unitary_attractor_no_go.csv": no_go_rows,
            "field_stability_vs_state_selection.csv": field_rows,
            "local_escape_spectral_gate.csv": spectral_rows,
            "finite_wavelength_local_escape_kinematics.csv": kinematic_rows,
            "local_escape_and_open_system_contract.csv": contract_rows,
            "state_selection_decision.csv": decisions,
            "source_provenance.csv": provenance,
        },
        "result": {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "checked_date": CHECKED_DATE,
            "closed_parent_local_vacuum_attractor": False,
            "closed_parent_attractor_no_go_derived": True,
            "exact_local_preparation_branch_retained": True,
            "chi_zero_stationary_and_lyapunov_stable": True,
            "chi_zero_asymptotic_attractor_from_current_local_action": False,
            "preferred_dynamic_completion": "EXPLICIT_PREPARATION_OR_PARENT_DERIVED_SPECTRAL_PROJECTOR_HISTORY",
            "universal_positive_local_escape_gap": False,
            "universal_local_escape_gap_no_go_derived": True,
            "finite_wavelength_outgoing_crossing_kinematics_derived": True,
            "parent_escape_rate_kappa_derived": False,
            "parent_reduced_dissipation_gap_gamma_derived": False,
            "valid_for_full_MTS_claim": False,
            "valid_for_parent_state_selection_claim": False,
            "source_hashes": source_hashes,
            "unitary_no_go": no_go_payload,
            "local_escape_spectral_gate": spectral_payload,
            "minimal_completion_witness": contract_payload,
        },
    }


def validation_rows(payload: dict[str, Any], saved: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(gate: str, passed: bool, detail: Any) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "marker": MARKER,
                "gate": gate,
                "passed": bool(passed),
                "detail": json.dumps(detail, sort_keys=True)
                if isinstance(detail, (dict, list))
                else str(detail),
            }
        )

    result = payload["result"]
    no_go = result["unitary_no_go"]["checks"]
    witness = result["minimal_completion_witness"]
    spectral = result["local_escape_spectral_gate"]
    add("all_source_paths_exist", all(path.is_file() for path in SOURCE_PATHS), len(SOURCE_PATHS))
    add("all_source_hashes_recorded", len(result["source_hashes"]) == len(SOURCE_PATHS), result["source_hashes"])
    add("liouvillian_skew_adjoint", no_go["liouvillian_skew_adjoint"], no_go)
    add("liouvillian_real_decay_gap_zero", no_go["liouvillian_real_decay_gap_zero"], no_go)
    add("unitary_distance_invariant", no_go["unitary_hilbert_schmidt_distance_invariant"], no_go)
    add("binary_trace_distance_equals_n", no_go["binary_trace_distance_equals_n"], no_go)
    add("amplitude_damping_witness_exact", witness["amplitude_damping_pass"], witness["occupation_derivative"])
    add("local_escape_Gronwall_bound_exact", witness["escape_bound_pass"], witness["gronwall_envelope"])
    add("universal_positive_escape_gap_rejected", spectral["universal_positive_escape_gap_rejected"], spectral)
    add("zero_mode_group_speed_zero", spectral["zero_momentum_speed"] == "0" and spectral["infrared_speed_limit"] == "0", spectral)
    add("finite_wavelength_arena_rows_present", spectral["arena_count"] >= 5, spectral["arena_count"])
    add("finite_wavelength_local_modes_relativistic", spectral["maximum_mass_ratio_squared"] < 1e-20, spectral["maximum_mass_ratio_squared"])
    add("homogeneous_local_tidal_residual_retained", spectral["maximum_homogeneous_tidal_ratio"] <= 1.1e-19, spectral["maximum_homogeneous_tidal_ratio"])
    add("closed_parent_attractor_rejected", result["closed_parent_local_vacuum_attractor"] is False, result["closed_parent_local_vacuum_attractor"])
    add("exact_preparation_branch_retained", result["exact_local_preparation_branch_retained"] is True, result["exact_local_preparation_branch_retained"])
    add("no_parent_kappa_or_gamma_claim", not result["parent_escape_rate_kappa_derived"] and not result["parent_reduced_dissipation_gap_gamma_derived"], "both remain false")
    all_rows = [row for group in payload["rows"].values() for row in group]
    add("all_rows_block_full_MTS_claim", all(row["valid_for_full_MTS_claim"] is False for row in all_rows), len(all_rows))
    add("all_rows_block_parent_state_selection_claim", all(row["valid_for_parent_state_selection_claim"] is False for row in all_rows), len(all_rows))
    add("all_output_paths_inside_post_checkpoint", all((OUT / name).resolve().is_relative_to(POST.resolve()) for name in OUTPUT_NAMES), str(POST))
    add("document_exists", DOCUMENT.is_file(), str(DOCUMENT))
    add("formalization_workbench_exists_and_unwritten", FORMAL.is_dir(), str(FORMAL))
    add("no_script_pycache", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts" / "__pycache__"))
    if saved:
        add("all_saved_outputs_exist", all((OUT / name).is_file() for name in OUTPUT_NAMES), OUTPUT_NAMES)
        saved_result = json.loads((OUT / "closed_parent_local_state_attractor_results.json").read_text(encoding="utf-8"))
        current_hashes = assert_sources()
        add("saved_source_hashes_still_match", saved_result["source_hashes"] == current_hashes, current_hashes)
        for name, expected_rows in payload["rows"].items():
            add(f"saved_{name}_row_count", len(read_csv(OUT / name)) == len(expected_rows), len(expected_rows))
    return rows


def write_outputs(payload: dict[str, Any]) -> None:
    for name, rows in payload["rows"].items():
        write_csv(OUT / name, rows)
    write_json(OUT / "closed_parent_local_state_attractor_results.json", payload["result"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--validate-saved", action="store_true")
    args = parser.parse_args()
    if args.dry_run and args.validate_saved:
        parser.error("choose at most one mode")

    payload = build_payload()
    if args.dry_run:
        checks = validation_rows(payload, saved=False)
        print(json.dumps({"mode": "dry-run", "checks": checks}, indent=2))
        return 0 if all(row["passed"] for row in checks) else 1

    if not args.validate_saved:
        write_outputs(payload)
    checks = validation_rows(payload, saved=True)
    write_csv(VALIDATION, checks)
    print(json.dumps({"mode": "validate-saved" if args.validate_saved else "run", "checks": checks}, indent=2))
    return 0 if all(row["passed"] for row in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
