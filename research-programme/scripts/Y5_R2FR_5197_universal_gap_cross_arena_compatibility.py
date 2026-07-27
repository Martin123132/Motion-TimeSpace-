from __future__ import annotations

import argparse
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

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5197"
DOCUMENT = (
    POST
    / "5197-Y5-R2FR-universal-gap-cross-arena-compatibility-and-route-"
    "separation-theorem.md"
)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5197_VALIDATION.csv"
)
PUBLIC_WORKTREE = Path(
    r"C:\Users\ollet\OneDrive\Documents\Motion-TimeSpace-public-update-2026-07-22"
)
GALAXY_REPO = Path(r"D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo")
CHECKPOINT_5176 = POST / "source-intake" / "functional_rg" / "5176"
CHECKPOINT_5195_OUT = POST / "source-intake" / "functional_rg" / "5195"
CHECKPOINT_5196_OUT = POST / "source-intake" / "functional_rg" / "5196"

MARKER = "MTS_5197_UNIVERSAL_GAP_CROSS_ARENA_ROUTE_SEPARATION"
CHECKED_DATE = "2026-07-24"
FORMAL_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
CHECKPOINT_5195_OUT_LOCK = (
    "7aa855d3f75b9d2eb52fdc73f903c77a2e8e8b9e3be0f9496c4f9e15c5d6a810"
)
CHECKPOINT_5196_OUT_LOCK = (
    "fc16f376470ac834daa8c89abe930254a456d67bd677d4c0290ebe8719b62c28"
)
PUBLIC_HEAD_LOCK = "8913c00b77d98e457ddb0c48e9aeec9cc5f309fd"
GALAXY_HEAD_LOCK = "f850e4997657f457dddc05cbe50f21186588dcc7"

HBAR_C_EV_METRES = 1.973269804593025e-7
PARSEC_METRES = 3.085677581491367e16
MPC_METRES = 3.0856775814913673e22

SOURCE_LOCKS = {
    "4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-two-scale-theory-gate.md": (
        "b30394a62c6a22af5da315b92a2823f44aa34cd914b6bab813136b0926aa0ca4"
    ),
    "5152-Y5-R2FR-primordial-motion-occupation-dust-limit-Jeans-window-and-formation-source-arbitration.md": (
        "a62af8bc11dc0e5130e681386bb64ac4a56fb21105540581f91ab452473b0167"
    ),
    "5163-Y5-R2FR-parent-wave-stress-and-visible-source-response-gate.md": (
        "babc8ade1bc3b15f27f8ca9a25ba19417b959b823a2aea6574ce0ca3148865bb"
    ),
    "5174-Y5-R2FR-mass-gap-continuation-and-spherical-cutoff-discrimination-gate.md": (
        "4ec6bbfb252fabb66b8543cf54204ac25a864a64a3918a66bec81fb49924c2a3"
    ),
    "5176-Y5-R2FR-predeclared-paired-high-mode-seed-ensemble.md": (
        "d9214a06853d9611538a5bb1fbe6b2bc12afe5ba48e2ea74794d95340252d6d5"
    ),
    "5177-Y5-R2FR-locked-ensemble-metric-split-and-no-retuning-theorem.md": (
        "abe635ca81992660c7e9bb834eed765626bf63cfc2564f3f4b23b759a3a0fd90"
    ),
    "5180-Y5-R2FR-interacting-retarded-2PI-kernel-Vlasov-subtraction-and-infrared-gap-closure-gate.md": (
        "1df0b686a815496b143f5397aebf4b55d16058cd8bbca3910fb7993e980c0c10"
    ),
    "5181-Y5-R2FR-critical-pair-bubble-positive-Hessian-and-parent-ownership-gate.md": (
        "54a35ad66744f9e1f5ab6fdd15e66bc6f87a93330a999aae2235ea5cf98b3657"
    ),
    "5186-Y5-R2FR-FLRW-Bogoliubov-neutral-vacuum-production-and-abundance-no-go.md": (
        "b3846c2e4bc1270b4c2f50d431fc5d812944f648ebec36f3250a95916101c05a"
    ),
    "5195-Y5-R2FR-matched-joint-CMB-informed-parent-refit-and-physical-sound-horizon-gate.md": (
        "217fdc07f94e18a21fe996f7592930f69c21ba16b3fe44b1fd1a2518d9d54737"
    ),
    "5196-Y5-R2FR-invariant-mass-gap-Hessian-and-homogeneous-state-selection-theorem.md": (
        "a3495f713d22fea38ebd010a1d0f14d2ff266180fa358ee8a89492a55ea57974"
    ),
    "source-intake/functional_rg/4938/motion_scale_bound_translation.csv": (
        "e62cabda4191eeae491d5f6849e8a5992eff1278b9b5286468dbfe15ff56e4bc"
    ),
    "source-intake/functional_rg/5152/galaxy_mass_window.csv": (
        "89c454b407e2af7fdf658de371de2e6096436882838f3c868e0fe2dcd3ca2baa"
    ),
    "source-intake/functional_rg/5152/primordial_motion_background.csv": (
        "01fce81188fb2c6cf1d982cb7ffe8d2896668f100878a0d1ba11462426a1e338"
    ),
    "source-intake/functional_rg/5152/source_route_arbitration.csv": (
        "b35ef21e8c7bb5ca6a4366537f2e3434a774903d8042d275ef4088284ecd72ef"
    ),
    "source-intake/functional_rg/5163/universal_wave_mass_overlap_gate.csv": (
        "b6c0311af9d1f525ded3fd450f26895921499d91794a09850889df84b9a3f96f"
    ),
    "source-intake/functional_rg/5163/route_decision.csv": (
        "02e2ab0bf7f891c6f7c765ac6e2acd6bb6e68626f2c16c9f6dae8912a0f0e47e"
    ),
    "source-intake/functional_rg/5174/conditional_mass_gap_bound.csv": (
        "70efef334540d5ccb2f78327e7eccab8636cd6dce8a04e66c9a63af75477e5bf"
    ),
    "source-intake/functional_rg/5174/route_decision.csv": (
        "8bbf8d87eb02576e8c67a21bb0daf0d4a0618c43ce5253aa323990f57b55afd8"
    ),
    "source-intake/functional_rg/5176/paired_ensemble_results.json": (
        "8ba10e25f63de01e8f05dde485ae998c190a97ae2f955ead07eaa1778644e79f"
    ),
    "source-intake/functional_rg/5176/route_decision.csv": (
        "6da3edcd8ef84a5ad3de95d639951aee5dd79da504eefc1953b6b869f81c7af7"
    ),
    "source-intake/functional_rg/5177/route_decision.csv": (
        "b1d13253e193939168cb0eecdfb30e2fac1443cc0bca16de26331043527807f2"
    ),
    "source-intake/functional_rg/5180/interaction_state_route_decision.csv": (
        "aeb0aa5664f7af339d9dac1b068cf1b650283933ced1e8da9cc1f50c516ec3aa"
    ),
    "source-intake/functional_rg/5181/critical_continuum_route_decision.csv": (
        "ec02816a626ec77079e91f3d752698a36fbb2917a6db127db682407403242628"
    ),
    "source-intake/functional_rg/5186/neutral_source_selection_route_decision.csv": (
        "f8d1b2903c622d1895750b48283976cacd8cb33d8ac080bd81fb5170bdb37764"
    ),
    "source-intake/functional_rg/5186/three_mass_vacuum_abundance_gate.csv": (
        "bf7a9ffa7cc4f6ff69364bebf8dc93ef2567adc42ed23b3e4ba843d39061b7c3"
    ),
    "source-intake/functional_rg/5192/massive_parent_scalar_scan.csv": (
        "8acf76294afb64341a9f77ff707e4ecb467cd980ae9ac57ecd18c286bcb0d652"
    ),
    "source-intake/functional_rg/5196/fitted_5195_mass_and_state_match.csv": (
        "1f8ed5a55fd7662df8a5fbb3030421565e95d58db634c98747c7fbf4010f32da"
    ),
    "source-intake/functional_rg/5196/invariant_mass_gap_Hessian.csv": (
        "0505d61d85add828f9544fd932acb6fb89edb72fe82adc2cde1c2c7097c02152"
    ),
}

GALAXY_SOURCE_LOCKS = {
    "scripts/mts_phase_flow_closure.py": (
        "d9268e84a0dea1c2774d9243333d4a16417b0855e23df7c8bb67eaf89271b516"
    ),
    "scripts/mts_self_similar_phase_disk.py": (
        "5fb668362ebf509b7f29358c455fd9b2abef2c9b4f5eb86a042e74089622cf3d"
    ),
    "scripts/mts_phase_lensing_gate.py": (
        "10cb186bffcd182537ebf950a752502d066ede762b0523278ed0b0a1ee8e23b7"
    ),
    "scripts/mts_nonanalytic_phase.py": (
        "f70c8cd99d9736af45ff5b725ca5d824be1c508e2288782ddd8b5b933342de6c"
    ),
    "scripts/mts_axisymmetric_phase.py": (
        "afc63bfaf4117897e52e5684f359c6401602cb4a312971a8c90310e50baf949d"
    ),
}


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(file_digest(item).encode("ascii"))
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_cosmology_support_claim": False,
            "valid_for_galaxy_claim": False,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def row_with(
    rows: list[dict[str, str]],
    key: str,
    value: str,
) -> dict[str, str]:
    matches = [row for row in rows if row.get(key) == value]
    if len(matches) != 1:
        raise ValueError(f"expected one {key}={value}, found {len(matches)}")
    return matches[0]


def relative_residual(value: float, target: float) -> float:
    return abs(value - target) / max(abs(target), 1.0e-300)


def compton_rows(mass_eV: float) -> dict[str, float]:
    length_metres = HBAR_C_EV_METRES / mass_eV
    return {
        "reduced_Compton_metres": length_metres,
        "reduced_Compton_parsec": length_metres / PARSEC_METRES,
        "reduced_Compton_Mpc": length_metres / MPC_METRES,
    }


def git_state(repository: Path) -> tuple[str, str]:
    safe_path = repository.as_posix()
    head = subprocess.run(
        [
            "git",
            "-c",
            f"safe.directory={safe_path}",
            "-C",
            str(repository),
            "rev-parse",
            "HEAD",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        [
            "git",
            "-c",
            f"safe.directory={safe_path}",
            "-C",
            str(repository),
            "status",
            "--porcelain=v1",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.rstrip()
    return head, status


def infer_newton_constant(
    cosmology_rows: list[dict[str, str]],
) -> tuple[float, float]:
    values = [
        float(row["J_gap_mgap2_GN"]) / float(row["m_gap_eV"]) ** 2
        for row in cosmology_rows
    ]
    mean_value = sum(values) / len(values)
    spread = max(relative_residual(value, mean_value) for value in values)
    return mean_value, spread


def equality_hubble(
    background_rows: list[dict[str, str]],
) -> tuple[float, float]:
    values = [
        float(row["m_gap_eV"])
        * float(row["H_equality_eV_over_m_gap"])
        for row in background_rows
    ]
    mean_value = sum(values) / len(values)
    spread = max(relative_residual(value, mean_value) for value in values)
    return mean_value, spread


def mass_inventory_rows(
    newton_eV_minus2: float,
    cosmology_rows: list[dict[str, str]],
    mass_window_rows: list[dict[str, str]],
    wave_rows: list[dict[str, str]],
    compact_rows: list[dict[str, str]],
    scan_5192_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(
        usage_id: str,
        arena: str,
        object_name: str,
        mass_min_eV: float | str,
        mass_max_eV: float | str,
        j_min: float | str,
        j_max: float | str,
        numerical_role: str,
        route_status: str,
        parent_selected: bool,
        same_elementary_pole_candidate: bool,
        source_path: str,
        interpretation: str,
    ) -> None:
        rows.append(
            {
                "usage_id": usage_id,
                "arena": arena,
                "object": object_name,
                "mass_min_eV": mass_min_eV,
                "mass_max_eV": mass_max_eV,
                "J_gap_min": j_min,
                "J_gap_max": j_max,
                "numerical_role": numerical_role,
                "route_status": route_status,
                "parent_selected": parent_selected,
                "same_elementary_pole_candidate": same_elementary_pole_candidate,
                "source_path": source_path,
                "interpretation": interpretation,
            }
        )

    add(
        "parent_invariant_relation",
        "all",
        "canonical elementary motion pole",
        "",
        "",
        "",
        "",
        "relation_only",
        "RETAINED",
        False,
        True,
        "source-intake/functional_rg/5196/invariant_mass_gap_Hessian.csv",
        "m_pole^2=V_eff''(0)/Z_psi and J_gap=G_N m_pole^2; one universal "
        "numerical calibration remains",
    )

    compact_min_j = min(float(row["J_gap_floor"]) for row in compact_rows)
    compact_max_j = max(float(row["J_gap_floor"]) for row in compact_rows)
    add(
        "compact_safety_floor_4938",
        "local_compact_object",
        "conditional one-percent Weyl-cubic safety floor",
        math.sqrt(compact_min_j / newton_eV_minus2),
        math.sqrt(compact_max_j / newton_eV_minus2),
        compact_min_j,
        compact_max_j,
        "conditional_lower_floor",
        "NONCLAIM_SAFETY_ENVELOPE",
        False,
        True,
        "source-intake/functional_rg/4938/motion_scale_bound_translation.csv",
        "weak local lower floor; it neither selects the pole nor conflicts with "
        "the cosmological values",
    )

    scan_masses = [
        float(row["mass_eV_for_H0_70"])
        for row in scan_5192_rows
        if row["mass_eV_for_H0_70"].strip()
        and float(row["mass_eV_for_H0_70"]) > 0.0
    ]
    add(
        "parent_cosmology_scan_5192",
        "cosmology",
        "massive parent scalar exploratory scan",
        min(scan_masses),
        max(scan_masses),
        newton_eV_minus2 * min(scan_masses) ** 2,
        newton_eV_minus2 * max(scan_masses) ** 2,
        "superseded_scan_range",
        "SUPERSEDED_BY_MATCHED_5195_REFIT",
        False,
        True,
        "source-intake/functional_rg/5192/massive_parent_scalar_scan.csv",
        "historical scan range; retained for provenance rather than as a second "
        "mass requirement",
    )

    for row in cosmology_rows:
        mass = float(row["m_gap_eV"])
        add(
            f"cosmology_{row['model']}",
            "cosmology",
            "5195 matched homogeneous parent scalar",
            mass,
            mass,
            float(row["J_gap_mgap2_GN"]),
            float(row["J_gap_mgap2_GN"]),
            "matched_fit_target",
            "LIVE_NONCLAIM_COSMOLOGY_BRANCH",
            False,
            True,
            "source-intake/functional_rg/5196/fitted_5195_mass_and_state_match.csv",
            "finite late-time branch; empirical target but not action-selected",
        )

    selected_mass_labels = {
        "WKB_floor_all_175": (
            "galaxy_WKB_floor_all_175",
            "de_Broglie_at_or_below_Rn_floor",
            "CONDITIONAL_ENGINEERING_FLOOR",
        ),
        "ten_times_WKB_floor": (
            "galaxy_WKB_floor_0p1Rn",
            "de_Broglie_at_or_below_0p1Rn_floor",
            "CONDITIONAL_ENGINEERING_FLOOR",
        ),
        "benchmark_1e_minus20_eV": (
            "galaxy_locked_comparator_1e_minus20",
            "frozen_formation_comparator",
            "CONDITIONAL_COMPARATOR",
        ),
        "benchmark_1e_minus18_eV": (
            "galaxy_upper_scan_1e_minus18",
            "upper_internal_scan_value",
            "CONDITIONAL_COMPARATOR",
        ),
        "lambdaJ_eq_le_0.1_Mpc": (
            "galaxy_Jeans_100kpc_floor",
            "instantaneous_equality_Jeans_engineering_floor",
            "CONDITIONAL_ENGINEERING_FLOOR",
        ),
    }
    for label, (usage_id, role, status) in selected_mass_labels.items():
        source_row = row_with(mass_window_rows, "mass_label", label)
        mass = float(source_row["m_gap_eV"])
        add(
            usage_id,
            "galaxy_occupied_particle",
            label,
            mass,
            mass,
            newton_eV_minus2 * mass**2,
            newton_eV_minus2 * mass**2,
            role,
            status,
            False,
            True,
            "source-intake/functional_rg/5152/galaxy_mass_window.csv",
            "massive-dust/FDM construction; no row is a parent-selected or "
            "claim-valid mass",
        )

    wave_floor = row_with(
        wave_rows,
        "row_type",
        "all_patch_Jeans_floor",
    )
    wave_mass = float(wave_floor["required_universal_m_gap_eV"])
    add(
        "galaxy_wave_population_floor_5163",
        "galaxy_occupied_particle",
        "all-patch Jeans floor used in wave-stress no-go",
        wave_mass,
        wave_mass,
        newton_eV_minus2 * wave_mass**2,
        newton_eV_minus2 * wave_mass**2,
        "conditional_population_floor",
        "WAVE_STRESS_REJECTED_AS_ORDER_ONE_OWNER",
        False,
        True,
        "source-intake/functional_rg/5163/universal_wave_mass_overlap_gate.csv",
        "used to make the canonical wave-pressure rejection conservative; not "
        "a selected universal mass",
    )

    add(
        "galaxy_unstable_crossing_5174",
        "galaxy_occupied_particle",
        "nonmonotone q-band crossing",
        1.0e-20,
        1.7782794100389228e-20,
        newton_eV_minus2 * 1.0e-40,
        newton_eV_minus2 * 1.7782794100389228e-20**2,
        "unstable_numeric_crossing",
        "NO_STABLE_MASS_BOUND",
        False,
        True,
        "source-intake/functional_rg/5174/conditional_mass_gap_bound.csv",
        "pipeline-sensitive nonmonotone crossing; explicitly not a universal "
        "galaxy limit",
    )

    add(
        "galaxy_ensemble_5176",
        "galaxy_occupied_particle",
        "locked 12-seed MTS comparator",
        1.0e-20,
        1.0e-20,
        newton_eV_minus2 * 1.0e-40,
        newton_eV_minus2 * 1.0e-40,
        "predeclared_comparator",
        "STATISTICAL_DRAW_OR_METRIC_SPLIT",
        False,
        True,
        "source-intake/functional_rg/5176/paired_ensemble_results.json",
        "the q metric favors MTS but RMSE does not; the mass remains a frozen "
        "comparator rather than a measured value",
    )

    add(
        "critical_pair_endpoint_5181",
        "galaxy_collective",
        "massless composite pair branch point",
        0.0,
        0.0,
        0.0,
        0.0,
        "collective_gap_endpoint",
        "KINEMATIC_CARRIER_PARENT_OWNERSHIP_OPEN",
        False,
        False,
        "source-intake/functional_rg/5181/critical_continuum_route_decision.csv",
        "zero composite gap is not a second fitted elementary pole; the "
        "environmental state and normalization remain underived",
    )

    add(
        "current_galaxy_phase_L_eff",
        "galaxy_collective",
        "environmental phase domain scale L_eff",
        "",
        "",
        "",
        "",
        "collective_environmental_length",
        "LIVE_RESEARCH_CANDIDATE_ACTION_MAP_OPEN",
        False,
        False,
        str(GALAXY_REPO / "scripts" / "mts_phase_flow_closure.py"),
        "L_eff is a radial similarity/domain coordinate; no source identifies "
        "it with the inverse elementary pole",
    )
    return tagged(rows)


def route_classification_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "route": "local_GR_Newton_Maxwell",
                "mass_semantics": "same calibrated G_N; scalar vacuum at psi=0",
                "status": "RETAINED",
                "same_elementary_pole_required": True,
                "source_or_selection_gap": "none introduced by this checkpoint",
                "next_action": "preserve local branch in every extension",
            },
            {
                "route": "5195_homogeneous_parent_scalar",
                "mass_semantics": "elementary pole m_pole around H0",
                "status": "LIVE_NONCLAIM_COSMOLOGY_BRANCH",
                "same_elementary_pole_required": True,
                "source_or_selection_gap": "J_gap and one regular state amplitude "
                "remain calibrated rather than parent-selected",
                "next_action": "retain as the one-pole core target",
            },
            {
                "route": "5152_to_5186_massive_occupied_particle",
                "mass_semantics": "same elementary pole treated as oscillating "
                "dust/FDM at 10^-21 to 10^-20 eV",
                "status": "CONDITIONAL_INITIAL_STATE_EXTENSION",
                "same_elementary_pole_required": True,
                "source_or_selection_gap": "abundance and covariance are initial "
                "data; one-pole cosmology compatibility fails",
                "next_action": "demote as unification owner; retain only as a "
                "separate-component comparator",
            },
            {
                "route": "current_v19_environmental_phase",
                "mass_semantics": "collective L_eff, n and b; no elementary mass "
                "appears",
                "status": "LIVE_RESEARCH_CANDIDATE",
                "same_elementary_pole_required": False,
                "source_or_selection_gap": "covariant action, activation, boundary "
                "and Hilbert stress remain underived",
                "next_action": "derive a composite/environmental Hessian map without "
                "setting L_eff=1/m_pole by hand",
            },
            {
                "route": "5181_critical_pair_continuum",
                "mass_semantics": "massless composite branch point and power-law "
                "correlation tail",
                "status": "KINEMATIC_CARRIER_DERIVED_PARENT_OWNERSHIP_OPEN",
                "same_elementary_pole_required": False,
                "source_or_selection_gap": "state, logistic filter, normalization "
                "and tensor sign are not parent-derived",
                "next_action": "compute the composite 2PI/Bethe-Salpeter Hessian on "
                "the environmental background",
            },
            {
                "route": "weak_loop_stationary_pair_and_vacuum_production_repairs",
                "mass_semantics": "regular gapped elementary or passive pair "
                "response",
                "status": "REJECTED_AS_GALAXY_OR_ABUNDANCE_OWNER",
                "same_elementary_pole_required": True,
                "source_or_selection_gap": "exact analyticity, sign, magnitude or "
                "abundance no-go",
                "next_action": "do not reopen without a new parent operator or "
                "state law",
            },
        ]
    )


def comparison_rows(
    newton_eV_minus2: float,
    cosmology_rows: list[dict[str, str]],
    mass_window_rows: list[dict[str, str]],
    wave_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    galaxy_targets = [
        (
            "5163_all_patch_Jeans_floor",
            float(
                row_with(
                    wave_rows,
                    "row_type",
                    "all_patch_Jeans_floor",
                )["required_universal_m_gap_eV"]
            ),
            "conditional_lower_floor",
        ),
        (
            "5152_de_Broglie_0p1Rn_floor",
            float(
                row_with(
                    mass_window_rows,
                    "mass_label",
                    "ten_times_WKB_floor",
                )["m_gap_eV"]
            ),
            "conditional_lower_floor",
        ),
        (
            "5152_equality_Jeans_100kpc_floor",
            float(
                row_with(
                    mass_window_rows,
                    "mass_label",
                    "lambdaJ_eq_le_0.1_Mpc",
                )["m_gap_eV"]
            ),
            "conditional_lower_floor",
        ),
        (
            "5176_locked_1e_minus20_comparator",
            1.0e-20,
            "frozen_comparator",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for cosmology in cosmology_rows:
        cosmology_mass = float(cosmology["m_gap_eV"])
        cosmology_j = float(cosmology["J_gap_mgap2_GN"])
        for galaxy_label, galaxy_mass, target_role in galaxy_targets:
            galaxy_j = newton_eV_minus2 * galaxy_mass**2
            mass_ratio = galaxy_mass / cosmology_mass
            j_ratio = galaxy_j / cosmology_j
            rows.append(
                {
                    "cosmology_model": cosmology["model"],
                    "galaxy_target": galaxy_label,
                    "galaxy_target_role": target_role,
                    "cosmology_mass_eV": cosmology_mass,
                    "galaxy_mass_eV": galaxy_mass,
                    "mass_ratio_galaxy_over_cosmology": mass_ratio,
                    "mass_decade_separation": math.log10(mass_ratio),
                    "cosmology_J_gap": cosmology_j,
                    "galaxy_J_gap": galaxy_j,
                    "J_ratio_galaxy_over_cosmology": j_ratio,
                    "J_decade_separation": math.log10(j_ratio),
                    "J_ratio_minus_mass_ratio_squared_fractional": (
                        relative_residual(j_ratio, mass_ratio**2)
                    ),
                    "one_constant_pole_compatible": False,
                    "reason": "cosmological pole is strictly below the galaxy "
                    "floor or unequal to the frozen comparator",
                    **{
                        f"cosmology_{key}": value
                        for key, value in compton_rows(cosmology_mass).items()
                    },
                    **{
                        f"galaxy_{key}": value
                        for key, value in compton_rows(galaxy_mass).items()
                    },
                }
            )
    return tagged(rows)


def dust_and_thaw_rows(
    cosmology_rows: list[dict[str, str]],
    mass_window_rows: list[dict[str, str]],
    h_equality_eV: float,
) -> list[dict[str, Any]]:
    h0_values = [
        float(row["m_gap_eV"]) / float(row["mu_mgap_over_H0"])
        for row in cosmology_rows
    ]
    h0_reference = sum(h0_values) / len(h0_values)
    cases: list[tuple[str, str, float, float]] = []
    for row in cosmology_rows:
        cases.append(
            (
                row["model"],
                "cosmology_fitted_elementary_pole",
                float(row["m_gap_eV"]),
                float(row["m_gap_eV"]) / float(row["mu_mgap_over_H0"]),
            )
        )
    for label in (
        "ten_times_WKB_floor",
        "lambdaJ_eq_le_0.1_Mpc",
        "benchmark_1e_minus20_eV",
    ):
        source_row = row_with(mass_window_rows, "mass_label", label)
        cases.append(
            (
                label,
                "galaxy_massive_dust_engineering_value",
                float(source_row["m_gap_eV"]),
                h0_reference,
            )
        )
    rows: list[dict[str, Any]] = []
    for label, role, mass, h0_value in cases:
        mass_over_equality = mass / h_equality_eV
        mass_over_h0 = mass / h0_value
        rows.append(
            {
                "case": label,
                "role": role,
                "mass_eV": mass,
                "H_equality_eV": h_equality_eV,
                "mass_over_H_equality": mass_over_equality,
                "oscillates_before_equality": mass_over_equality > 1.0,
                "deep_dust_averaging_at_equality": mass_over_equality >= 10.0,
                "H0_reference_eV": h0_value,
                "mass_over_H0": mass_over_h0,
                "order_H0_late_thaw_scale": 0.1 <= mass_over_h0 <= 10.0,
                "same_quadratic_mode_can_be_both_roles": False,
                "interpretation": (
                    "late-time thawing and not equality-era dust"
                    if role == "cosmology_fitted_elementary_pole"
                    else "equality-era dust-capable and far too rapid for "
                    "order-H0 thawing"
                ),
            }
        )
    return tagged(rows)


def collective_scale_gate_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source_text = {
        relative: (GALAXY_REPO / relative).read_text(encoding="utf-8")
        for relative in GALAXY_SOURCE_LOCKS
    }
    combined = "\n".join(source_text.values())
    mass_tokens = re.findall(
        r"(?i)\bm_gap\b|\bJ_gap\b|\bCompton\b|\bpole mass\b|\bparticle mass\b",
        combined,
    )
    required_false_flags = {
        "covariantFourDimensionalActionDerived": (
            '"covariantFourDimensionalActionDerived": False' in combined
        ),
        "environmentalBoundaryDerived": (
            '"environmentalBoundaryDerived": False' in combined
        ),
        "stressTensorDerived": '"stressTensorDerived": False' in combined,
        "phaseActivationDerived": '"phaseActivationDerived": False' in combined,
        "phaseBoundaryDerived": '"phaseBoundaryDerived": False' in combined,
        "phaseStressTensorDerivedFromAction": (
            '"phaseStressTensorDerivedFromAction": False' in combined
        ),
    }
    rows = [
        {
            "gate": "no_elementary_mass_token",
            "test": "m_gap, J_gap, Compton, pole mass and particle mass absent "
            "from the five current phase scripts",
            "result": len(mass_tokens) == 0,
            "detail": f"token_count={len(mass_tokens)}",
            "consequence": "the current phase route has no numerical elementary "
            "pole conflict",
        },
        {
            "gate": "collective_radial_coordinate",
            "test": "u=ln(R/L_eff) appears in the phase-flow source",
            "result": "u=ln(R/L_eff)" in combined,
            "detail": "environmental similarity coordinate",
            "consequence": "L_eff labels a collective domain/profile scale",
        },
        {
            "gate": "not_particle_dark_disk",
            "test": "the source explicitly denies a particle dark-disk fit",
            "result": "not a particle dark-disk fit" in combined,
            "detail": "source-owned interpretation",
            "consequence": "do not inherit the 1e-20 eV comparator silently",
        },
        {
            "gate": "missing_parent_derivation_flags",
            "test": "all six action, activation, boundary and stress flags are false",
            "result": all(required_false_flags.values()),
            "detail": json.dumps(required_false_flags, sort_keys=True),
            "consequence": "the collective route remains an open derivation, not "
            "a claimed solution",
        },
        {
            "gate": "inverse_pole_identification",
            "test": "a parent equation m_pole=hbar/(c L_eff) is present",
            "result": False,
            "detail": "no such source equation exists",
            "consequence": "translation of L_eff into J_gap is forbidden until a "
            "covariant Hessian/dispersion map is derived",
        },
        {
            "gate": "one_pole_route_survives_collective_option",
            "test": "a collective Hessian eigenvalue need not equal the elementary "
            "zero-field pole",
            "result": True,
            "detail": "elementary and composite two-point operators are distinct",
            "consequence": "the cosmological one-pole core is not rejected by the "
            "current phase candidate",
        },
    ]
    diagnostics = {
        "mass_token_count": len(mass_tokens),
        "false_flags": required_false_flags,
        "all_false_flags_present": all(required_false_flags.values()),
    }
    return tagged(rows), diagnostics


def resolution_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "option": "same_constant_pole_for_5195_and_5176",
                "new_elementary_fields": 0,
                "new_mass_calibrations": 0,
                "new_state_or_collective_inputs": 0,
                "status": "REJECTED_BY_DISJOINT_SCALE_AND_EPOCH_GATE",
                "scientific_cost": "mathematically incompatible",
                "next_requirement": "none; do not retune by arena",
            },
            {
                "option": "one_elementary_pole_plus_collective_environmental_phase",
                "new_elementary_fields": 0,
                "new_mass_calibrations": 0,
                "new_state_or_collective_inputs": 1,
                "status": "SELECTED_DERIVATION_ROUTE",
                "scientific_cost": "must derive a composite/environmental Hessian, "
                "activation, boundary and Hilbert stress",
                "next_requirement": "derive the stationary composite eigenproblem "
                "and its map to L_eff, n and b",
            },
            {
                "option": "second_elementary_motion_pole",
                "new_elementary_fields": 1,
                "new_mass_calibrations": 1,
                "new_state_or_collective_inputs": 1,
                "status": "CONSISTENT_BUT_NOT_CURRENT_MINIMAL_PARENT",
                "scientific_cost": "adds a field, a mass and state preparation",
                "next_requirement": "write and test the extended action and local "
                "decoupling theorem",
            },
            {
                "option": "environment_dependent_elementary_pole",
                "new_elementary_fields": 0,
                "new_mass_calibrations": 0,
                "new_state_or_collective_inputs": 1,
                "status": "OPEN_ONLY_WITH_EXPLICIT_PARENT_OPERATOR",
                "scientific_cost": "requires a covariant environmental operator "
                "that changes the Hessian by over ten mass decades without local "
                "instability or fifth force",
                "next_requirement": "derive the operator and its local/cosmological "
                "limits; phenomenological running is forbidden",
            },
            {
                "option": "gapless_critical_composite_pair",
                "new_elementary_fields": 0,
                "new_mass_calibrations": 0,
                "new_state_or_collective_inputs": 1,
                "status": "KINEMATICALLY_OPEN_NOT_PARENT_OWNED",
                "scientific_cost": "requires a positive composite spectrum, state "
                "selection, normalization and tensor projection",
                "next_requirement": "solve the 2PI/Bethe-Salpeter environmental "
                "Hessian rather than insert a logistic filter",
            },
        ]
    )


def decision_rows(
    comparison: list[dict[str, Any]],
    collective_diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    maximum_cosmology_mass = max(
        float(row["cosmology_mass_eV"]) for row in comparison
    )
    minimum_galaxy_mass = min(float(row["galaxy_mass_eV"]) for row in comparison)
    return tagged(
        [
            {
                "question": "Can the 5195 late-time scalar and the 5152-5176 "
                "massive occupied galaxy state be the same constant pole?",
                "answer": "NO",
                "status": "PROVED_BY_DISJOINT_MASS_AND_EPOCH_GATES",
                "consequence": f"max cosmology mass={maximum_cosmology_mass}; "
                f"min tested galaxy floor={minimum_galaxy_mass}",
            },
            {
                "question": "Does this reject the current MTS galaxy phase route?",
                "answer": "NO",
                "status": "SEMANTICALLY_DISTINCT_COLLECTIVE_SCALE",
                "consequence": "the current phase scripts contain no elementary "
                "mass token and do not identify L_eff with a pole",
            },
            {
                "question": "May L_eff be translated into J_gap now?",
                "answer": "NO",
                "status": "MAP_NOT_DERIVED",
                "consequence": "L_eff-to-pole conversion would be a hidden "
                "arena-dependent mass retuning",
            },
            {
                "question": "What happens to the 1e-20 eV occupied-state route?",
                "answer": "DEMOTE_TO_CONDITIONAL_SEPARATE_COMPONENT_COMPARATOR",
                "status": "NOT_THE_ONE_POLE_UNIFICATION_OWNER",
                "consequence": "retain its calculations as conditional evidence, "
                "not as the mass of the 5195 scalar",
            },
            {
                "question": "What route is selected next?",
                "answer": "DERIVE_COMPOSITE_ENVIRONMENTAL_HESSIAN_AND_SCALE_MAP",
                "status": "NEXT_TARGET_FIXED",
                "consequence": "derive a parent-owned collective eigenvalue, "
                "activation, finite wall and Hilbert stress while the elementary "
                "cosmological pole remains universal",
            },
            {
                "question": "Is the local GR/Newton/Maxwell branch modified?",
                "answer": "NO",
                "status": "SOURCE_AND_COUPLING_UNCHANGED",
                "consequence": "no new local charge, force normalization or "
                "arena switch is added",
            },
            {
                "question": "Does checkpoint 5197 establish galaxy or full MTS?",
                "answer": "NO",
                "status": "NONCLAIM",
                "consequence": "it removes a false one-pole identification and "
                "fixes the next constructive derivation",
            },
            {
                "question": "Were all current collective missing-derivation flags "
                "confirmed?",
                "answer": "YES",
                "status": "SOURCE_AUDITED",
                "consequence": json.dumps(
                    collective_diagnostics["false_flags"],
                    sort_keys=True,
                ),
            },
        ]
    )


def source_provenance_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for relative, expected_hash in SOURCE_LOCKS.items():
        path = POST / relative
        rows.append(
            {
                "scope": "parent_private_checkpoint",
                "source_path": relative,
                "expected_sha256": expected_hash,
                "actual_sha256": file_digest(path) if path.exists() else "",
                "exists": path.exists(),
                "lock_matches": (
                    path.exists() and file_digest(path) == expected_hash
                ),
                "role": "mass semantics, route status or fitted target",
            }
        )
    for relative, expected_hash in GALAXY_SOURCE_LOCKS.items():
        path = GALAXY_REPO / relative
        rows.append(
            {
                "scope": "galaxy_repo_read_only",
                "source_path": str(path),
                "expected_sha256": expected_hash,
                "actual_sha256": file_digest(path) if path.exists() else "",
                "exists": path.exists(),
                "lock_matches": (
                    path.exists() and file_digest(path) == expected_hash
                ),
                "role": "current collective phase semantics",
            }
        )
    return tagged(rows)


def validation_rows(
    newton_eV_minus2: float,
    newton_spread: float,
    h_equality_eV: float,
    equality_spread: float,
    inventory: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    comparison: list[dict[str, Any]],
    dust: list[dict[str, Any]],
    collective: list[dict[str, Any]],
    resolutions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    provenance: list[dict[str, Any]],
    output_files: list[Path],
    galaxy_before: tuple[str, str],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, Any]] = []

    def add(name: str, passed: bool, detail: Any) -> None:
        checks.append((name, bool(passed), detail))

    add(
        "document_exists",
        DOCUMENT.exists(),
        DOCUMENT,
    )
    add(
        "script_compiles_without_bytecode",
        bool(compile(SCRIPT.read_text(encoding="utf-8"), str(SCRIPT), "exec")),
        SCRIPT,
    )
    add(
        "formalization_workbench_unchanged",
        tree_digest(FORMAL) == FORMAL_LOCK,
        f"expected={FORMAL_LOCK};actual={tree_digest(FORMAL)}",
    )
    add(
        "checkpoint_5176_unchanged",
        tree_digest(CHECKPOINT_5176) == CHECKPOINT_5176_LOCK,
        f"expected={CHECKPOINT_5176_LOCK};actual={tree_digest(CHECKPOINT_5176)}",
    )
    add(
        "checkpoint_5195_output_unchanged",
        tree_digest(CHECKPOINT_5195_OUT) == CHECKPOINT_5195_OUT_LOCK,
        f"expected={CHECKPOINT_5195_OUT_LOCK};"
        f"actual={tree_digest(CHECKPOINT_5195_OUT)}",
    )
    add(
        "checkpoint_5196_output_unchanged",
        tree_digest(CHECKPOINT_5196_OUT) == CHECKPOINT_5196_OUT_LOCK,
        f"expected={CHECKPOINT_5196_OUT_LOCK};"
        f"actual={tree_digest(CHECKPOINT_5196_OUT)}",
    )
    add(
        "all_source_locks_match",
        all(row["lock_matches"] for row in provenance),
        f"{sum(bool(row['lock_matches']) for row in provenance)}/"
        f"{len(provenance)}",
    )
    add(
        "Newton_constant_reconstruction_consistent",
        newton_spread < 1.0e-12 and 6.0e-57 < newton_eV_minus2 < 7.5e-57,
        f"G_N={newton_eV_minus2};spread={newton_spread}",
    )
    add(
        "equality_Hubble_reconstruction_consistent",
        equality_spread < 1.0e-12 and 1.0e-28 < h_equality_eV < 5.0e-28,
        f"H_eq={h_equality_eV};spread={equality_spread}",
    )
    add(
        "all_one_pole_comparisons_incompatible",
        all(not row["one_constant_pole_compatible"] for row in comparison),
        f"rows={len(comparison)}",
    )
    add(
        "J_ratio_is_mass_ratio_squared",
        max(
            float(row["J_ratio_minus_mass_ratio_squared_fractional"])
            for row in comparison
        )
        < 1.0e-12,
        max(
            float(row["J_ratio_minus_mass_ratio_squared_fractional"])
            for row in comparison
        ),
    )
    cosmology_dust = [
        row for row in dust if row["role"] == "cosmology_fitted_elementary_pole"
    ]
    galaxy_dust = [
        row
        for row in dust
        if row["role"] == "galaxy_massive_dust_engineering_value"
    ]
    add(
        "cosmology_poles_are_not_equality_dust",
        all(
            not row["oscillates_before_equality"]
            and not row["deep_dust_averaging_at_equality"]
            and row["order_H0_late_thaw_scale"]
            for row in cosmology_dust
        ),
        f"rows={len(cosmology_dust)}",
    )
    add(
        "galaxy_particle_values_are_not_late_thaw_scales",
        all(
            row["deep_dust_averaging_at_equality"]
            and not row["order_H0_late_thaw_scale"]
            for row in galaxy_dust
        ),
        f"rows={len(galaxy_dust)}",
    )
    collective_by_gate = {row["gate"]: row for row in collective}
    add(
        "current_galaxy_phase_has_no_mass_token",
        collective_by_gate["no_elementary_mass_token"]["result"],
        collective_by_gate["no_elementary_mass_token"]["detail"],
    )
    add(
        "current_galaxy_missing_derivation_flags_confirmed",
        collective_by_gate["missing_parent_derivation_flags"]["result"],
        collective_by_gate["missing_parent_derivation_flags"]["detail"],
    )
    add(
        "L_eff_to_J_gap_translation_blocked",
        not collective_by_gate["inverse_pole_identification"]["result"],
        collective_by_gate["inverse_pole_identification"]["consequence"],
    )
    add(
        "selected_route_is_collective_Hessian_derivation",
        any(
            row["answer"]
            == "DERIVE_COMPOSITE_ENVIRONMENTAL_HESSIAN_AND_SCALE_MAP"
            for row in decisions
        ),
        "route decision",
    )
    add(
        "same_constant_pole_option_rejected",
        any(
            row["option"] == "same_constant_pole_for_5195_and_5176"
            and row["status"] == "REJECTED_BY_DISJOINT_SCALE_AND_EPOCH_GATE"
            for row in resolutions
        ),
        "resolution table",
    )
    add(
        "occupied_particle_route_demoted_not_erased",
        any(
            row["route"] == "5152_to_5186_massive_occupied_particle"
            and row["status"] == "CONDITIONAL_INITIAL_STATE_EXTENSION"
            for row in routes
        )
        and any(
            row["answer"]
            == "DEMOTE_TO_CONDITIONAL_SEPARATE_COMPONENT_COMPARATOR"
            for row in decisions
        ),
        "route classification and decision",
    )
    add(
        "inventory_contains_local_cosmology_particle_and_collective",
        {
            "local_compact_object",
            "cosmology",
            "galaxy_occupied_particle",
            "galaxy_collective",
        }.issubset({row["arena"] for row in inventory}),
        sorted({row["arena"] for row in inventory}),
    )
    parse_ok = True
    missing_marker = False
    for path in output_files:
        if path.suffix == ".csv":
            parsed = read_csv(path)
            parse_ok = parse_ok and bool(parsed)
            missing_marker = missing_marker or any(
                "MISSING_" in str(value)
                for row in parsed
                for value in row.values()
            )
        elif path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
    add("all_machine_outputs_parse", parse_ok, len(output_files))
    add("no_MISSING_markers", not missing_marker, missing_marker)
    all_collections = (
        inventory,
        routes,
        comparison,
        dust,
        collective,
        resolutions,
        decisions,
        provenance,
    )
    add(
        "all_rows_are_nonclaim",
        all(
            row["valid_for_cosmology_support_claim"] is False
            and row["valid_for_galaxy_claim"] is False
            and row["valid_for_full_MTS_claim"] is False
            for collection in all_collections
            for row in collection
        ),
        "all generated rows",
    )
    galaxy_after = git_state(GALAXY_REPO)
    add(
        "galaxy_repo_head_unchanged",
        galaxy_after[0] == GALAXY_HEAD_LOCK == galaxy_before[0],
        f"before={galaxy_before[0]};after={galaxy_after[0]}",
    )
    add(
        "galaxy_repo_status_unchanged",
        galaxy_after[1] == galaxy_before[1],
        galaxy_after[1] if galaxy_after[1] else "clean",
    )
    public_head, public_status = git_state(PUBLIC_WORKTREE)
    add(
        "public_worktree_head_unchanged",
        public_head == PUBLIC_HEAD_LOCK,
        f"expected={PUBLIC_HEAD_LOCK};actual={public_head}",
    )
    add(
        "public_worktree_clean",
        public_status == "",
        public_status if public_status else "clean",
    )
    pycache = POST / "scripts" / "__pycache__"
    add("no_scripts_pycache", not pycache.exists(), pycache)
    return tagged(
        [
            {
                "check": name,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
            }
            for name, passed, detail in checks
        ]
    )


def build_payload(
    newton_eV_minus2: float,
    newton_spread: float,
    h_equality_eV: float,
    equality_spread: float,
    inventory: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    comparison: list[dict[str, Any]],
    dust: list[dict[str, Any]],
    collective: list[dict[str, Any]],
    resolutions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    provenance: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "checkpoint": 5197,
        "marker": MARKER,
        "claim_status": {
            "one_pole_particle_unification": "REJECTED",
            "current_collective_galaxy_phase": "OPEN_NOT_REJECTED",
            "local_GR_Newton_Maxwell_branch": "UNCHANGED",
            "galaxy_claim": False,
            "cosmology_support_claim": False,
            "full_MTS_claim": False,
        },
        "theorem": (
            "A single constant elementary pole cannot simultaneously be the "
            "order-H0 scalar reconstructed by checkpoint 5195 and the "
            "equality-era oscillating massive-dust pole used by checkpoints "
            "5152-5176. Their mass and J_gap intervals are disjoint and their "
            "epoch requirements are opposite. The current galaxy phase route "
            "is not thereby rejected because its L_eff is a collective "
            "environmental scale with no derived identification to m_pole."
        ),
        "constants": {
            "G_N_eV_minus2_reconstructed": newton_eV_minus2,
            "G_N_branch_spread": newton_spread,
            "H_equality_eV_reconstructed": h_equality_eV,
            "H_equality_row_spread": equality_spread,
        },
        "mass_usage_classification": inventory,
        "route_classification": routes,
        "universal_gap_comparisons": comparison,
        "dust_and_thaw_gate": dust,
        "collective_scale_gate": collective,
        "resolution_options": resolutions,
        "route_decision": decisions,
        "source_provenance": provenance,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="derive and print the checkpoint decision without writing files",
    )
    arguments = parser.parse_args()

    galaxy_before = git_state(GALAXY_REPO)
    cosmology_rows = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "5196"
        / "fitted_5195_mass_and_state_match.csv"
    )
    mass_window_rows = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "5152"
        / "galaxy_mass_window.csv"
    )
    background_rows = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "5152"
        / "primordial_motion_background.csv"
    )
    wave_rows = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "5163"
        / "universal_wave_mass_overlap_gate.csv"
    )
    compact_rows = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "4938"
        / "motion_scale_bound_translation.csv"
    )
    scan_5192_rows = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "5192"
        / "massive_parent_scalar_scan.csv"
    )
    newton_eV_minus2, newton_spread = infer_newton_constant(cosmology_rows)
    h_equality_eV, equality_spread = equality_hubble(background_rows)

    inventory = mass_inventory_rows(
        newton_eV_minus2,
        cosmology_rows,
        mass_window_rows,
        wave_rows,
        compact_rows,
        scan_5192_rows,
    )
    routes = route_classification_rows()
    comparison = comparison_rows(
        newton_eV_minus2,
        cosmology_rows,
        mass_window_rows,
        wave_rows,
    )
    dust = dust_and_thaw_rows(
        cosmology_rows,
        mass_window_rows,
        h_equality_eV,
    )
    collective, collective_diagnostics = collective_scale_gate_rows()
    resolutions = resolution_rows()
    decisions = decision_rows(comparison, collective_diagnostics)
    provenance = source_provenance_rows()
    payload = build_payload(
        newton_eV_minus2,
        newton_spread,
        h_equality_eV,
        equality_spread,
        inventory,
        routes,
        comparison,
        dust,
        collective,
        resolutions,
        decisions,
        provenance,
    )

    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "marker": MARKER,
                    "constants": payload["constants"],
                    "comparison": comparison,
                    "collective_scale_gate": collective,
                    "decision": decisions,
                },
                indent=2,
                default=str,
            )
        )
        return

    OUT.mkdir(parents=True, exist_ok=True)
    output_map = {
        "all_mass_usage_classification.csv": inventory,
        "live_route_mass_semantics.csv": routes,
        "universal_gap_numeric_comparison.csv": comparison,
        "dust_WKB_equality_gate.csv": dust,
        "galaxy_collective_scale_not_pole_gate.csv": collective,
        "resolution_options_and_parameter_cost.csv": resolutions,
        "route_decision.csv": decisions,
        "source_provenance.csv": provenance,
    }
    for name, rows in output_map.items():
        write_csv(OUT / name, rows)
    result_path = OUT / "universal_gap_cross_arena_results.json"
    result_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    output_files = [OUT / name for name in output_map] + [result_path]
    validations = validation_rows(
        newton_eV_minus2,
        newton_spread,
        h_equality_eV,
        equality_spread,
        inventory,
        routes,
        comparison,
        dust,
        collective,
        resolutions,
        decisions,
        provenance,
        output_files,
        galaxy_before,
    )
    write_csv(VALIDATION, validations)
    failed = [row for row in validations if row["status"] != "PASS"]
    if failed:
        raise RuntimeError(
            "checkpoint 5197 validation failed: "
            + "; ".join(f"{row['check']}={row['detail']}" for row in failed)
        )
    print(
        json.dumps(
            {
                "marker": MARKER,
                "validation": f"{len(validations)}/{len(validations)} PASS",
                "output_files": len(output_files),
                "output_bytes": sum(path.stat().st_size for path in output_files),
                "formalization_workbench": tree_digest(FORMAL),
                "checkpoint_5176": tree_digest(CHECKPOINT_5176),
                "checkpoint_5195_output": tree_digest(CHECKPOINT_5195_OUT),
                "checkpoint_5196_output": tree_digest(CHECKPOINT_5196_OUT),
                "maximum_mass_decade_separation": max(
                    float(row["mass_decade_separation"]) for row in comparison
                ),
                "selected_next_route": "DERIVE_COMPOSITE_ENVIRONMENTAL_HESSIAN_AND_SCALE_MAP",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
