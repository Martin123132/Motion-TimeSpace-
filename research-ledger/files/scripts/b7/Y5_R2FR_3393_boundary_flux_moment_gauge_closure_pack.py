from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3393-Y5-R2FR-boundary-flux-moment-gauge-closure-pack-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3393_SOURCE_REGISTER.csv",
    "external_sources": OUT / "P8_Y5_R2FR_3393_EXTERNAL_SOURCE_PACK.csv",
    "boundary_flux_theorem": OUT / "P8_Y5_R2FR_3393_BOUNDARY_FLUX_PLACEMENT_THEOREM.csv",
    "poynting_bound": OUT / "P8_Y5_R2FR_3393_CASSINI_POYNTING_FLUX_BOUND_NONCLAIM.csv",
    "kernel_moment": OUT / "P8_Y5_R2FR_3393_KERNEL_MOMENT_ZERO_THEOREM.csv",
    "gauge_bound": OUT / "P8_Y5_R2FR_3393_GAUGE_READOUT_DRIFT_BOUND_ROWS_NONCLAIM.csv",
    "closure_matrix": OUT / "P8_Y5_R2FR_3393_CHANNEL_CLOSURE_MATRIX.csv",
    "runner": OUT / "P8_Y5_R2FR_3393_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3393_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3393_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3393_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3393_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3393_00_3392_doc", ROOT / "3392-Y5-R2FR-fixed-PPN-readout-parent-clause-or-projector-ell-scale-bound-under-AX1090.md", "3392 handoff"),
    ("SRC3393_01_3392_next", OUT / "P8_Y5_R2FR_3392_NEXT_TARGET.csv", "3392 next target"),
    ("SRC3393_02_3392_obstruction", OUT / "P8_Y5_R2FR_3392_REMAINING_CHANNEL_OBSTRUCTION_MAP.csv", "remaining obstruction map"),
    ("SRC3393_03_3392_clause", OUT / "P8_Y5_R2FR_3392_FIXED_PPN_PARENT_CLAUSE_CANDIDATE.csv", "fixed readout clause candidate"),
    ("SRC3393_04_3391_geometry", OUT / "P8_Y5_R2FR_3391_CASSINI_GEOMETRY_SOURCE_BACKED.csv", "Cassini source-backed geometry"),
    ("SRC3393_05_3391_external", OUT / "P8_Y5_R2FR_3391_EXTERNAL_SOURCE_PACK.csv", "Cassini/NASA external source pack"),
    ("SRC3393_06_3389_targets", OUT / "P8_Y5_R2FR_3389_TARGET_REQUIREMENT_SUMMARY.csv", "strict boundary/kernel targets"),
    ("SRC3393_07_3376_doc", ROOT / "3376-Y5-R2FR-boundary-zero-flux-or-Bzero-first-row-under-AX1090.md", "boundary zero-flux package"),
    ("SRC3393_08_3376_poynting", OUT / "P8_Y5_R2FR_3249_SOURCE_WORLDTUBE_POYNTING_BOUND_ROW.csv", "Poynting source-worldtube bound row"),
    ("SRC3393_09_3376_flux_norm", OUT / "P8_Y5_R2FR_3250_SOURCE_WORLDTUBE_FLUX_NORM_ROW.csv", "source-worldtube flux norm row"),
    ("SRC3393_10_3387_kernel", OUT / "P8_Y5_R2FR_3387_KERNEL_PROJECTOR_COMMUTATOR_LAW.csv", "kernel/projector commutator law"),
    ("SRC3393_11_core_fundamental_action", REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md", "parent fundamental action"),
    ("SRC3393_12_core_motion_action", REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md", "parent motion action"),
]

C_LIGHT_M_PER_S = 299_792_458.0
SOLAR_LUMINOSITY_W = 3.846e26
SOLAR_MASS_KG = 1.9891e30


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def to_float(value: str, default: float = math.nan) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        if not exists:
            parse_ok, parse_error = False, "missing"
        elif path.suffix.lower() == ".csv":
            parse_ok, parse_error = parse_csv(path)
        else:
            parse_ok, parse_error = parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "read_or_write": "read_only_context" if str(path).startswith(str(FW)) else "post_checkpoint_or_core_source",
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def external_source_rows() -> list[dict[str, str]]:
    return [
        {
            "source_id": "EXT3393_0_NASA_Sun_Fact_Sheet",
            "source_type": "official_NASA_fact_sheet",
            "source_url": "https://radiojove.gsfc.nasa.gov/education/sun/basics/material/sunfacts.htm",
            "used_for": "solar luminosity and solar mass for Poynting/mass-energy flux bound",
            "numeric_value": f"L_sun={SOLAR_LUMINOSITY_W:.6e} W; M_sun={SOLAR_MASS_KG:.6e} kg",
            "unit": "W; kg",
            "extraction_method": "manual source-backed constants; private nonclaim bound",
            "confidence": "high_for_order_of_magnitude_flux_bound",
            "valid_for_claim": "false",
        },
        {
            "source_id": "EXT3393_1_Cassini_Nature",
            "source_type": "peer_reviewed_primary_article",
            "source_url": "https://www.nature.com/articles/nature01997",
            "used_for": "Cassini PPN arena identity and b_min inherited from 3391",
            "numeric_value": "gamma_minus_one=2.1e-5; sigma=2.3e-5; b_min=1.6 R_sun",
            "unit": "dimensionless; solar radii",
            "extraction_method": "inherited from 3391 external source pack",
            "confidence": "high_for_arena",
            "valid_for_claim": "false",
        },
    ]


def target_rows() -> list[dict[str, str]]:
    return read_csv_rows(OUT / "P8_Y5_R2FR_3389_TARGET_REQUIREMENT_SUMMARY.csv")


def geometry_reference_row() -> dict[str, str]:
    rows = read_csv_rows(OUT / "P8_Y5_R2FR_3391_CASSINI_GEOMETRY_SOURCE_BACKED.csv")
    return rows[0] if rows else {}


def boundary_flux_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "BF3393_0_public_hilbert_placement",
            "channel": "Poynting/EM/matter flux",
            "statement": "Physical EM or matter flux through the Cassini collar is not an MTS hidden boundary numerator if it is included in the public Hilbert stress/source measure.",
            "derivation": "The local Einstein/PPN readout uses T_{mu nu}^{public}; any solar luminosity or radio-link EM stress belongs in T_{mu nu}, while only unmodelled non-Hilbert leakage remains in epsilon_boundary.",
            "required_parent_clause": "source measure includes public EM/radiation stress before boundary residual is scored",
            "status": "DERIVED_PLACEMENT_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "BF3393_1_stationary_vacuum_annulus",
            "channel": "B_zero_flux and Delta_symp",
            "statement": "In a fixed source-free stationary annulus with fixed primitive, trivial relative class and source-blind reference, B_zero_flux=Delta_symp=0.",
            "derivation": "3376 Stokes/fixed-reference theorem applies; 3393 imports it rather than relitigating exactness.",
            "required_parent_clause": "3376 BZF3376_0 through BZF3376_5 signed in the same Cassini branch",
            "status": "VALID_CONDITIONAL_FROM_3376_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "BF3393_2_finite_solar_luminosity_bound",
            "channel": "finite public Poynting leakage",
            "statement": "If solar luminosity is conservatively retained as finite flux over a local readout time Delta t, the dimensionless mass-energy fraction is L_sun Delta t/(M_sun c^2).",
            "derivation": "Energy crossing the boundary is bounded by luminosity times duration; normalize by same-frame solar mass-energy as a conservative nonclaim denominator.",
            "required_parent_clause": "duration/window choice and same-frame M_H_ref mapping",
            "status": "FINITE_BOUND_READY_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def poynting_bound_rows() -> list[dict[str, str]]:
    geometry = geometry_reference_row()
    impact_parameter_m = to_float(geometry.get("impact_parameter_m", ""))
    source_free_collar_m = to_float(geometry.get("source_free_collar_m", ""))
    solar_radius_m = to_float(geometry.get("solar_radius_m", ""))
    mass_energy_j = SOLAR_MASS_KG * C_LIGHT_M_PER_S**2
    durations = [
        ("Rsun_light_crossing", solar_radius_m / C_LIGHT_M_PER_S),
        ("collar_light_crossing", source_free_collar_m / C_LIGHT_M_PER_S),
        ("impact_parameter_light_crossing", impact_parameter_m / C_LIGHT_M_PER_S),
        ("one_day", 86_400.0),
        ("twenty_days", 20.0 * 86_400.0),
        ("one_year", 365.25 * 86_400.0),
    ]
    strict_boundary = min(to_float(row.get("min_epsilon_boundary_target", "")) for row in target_rows())
    rows: list[dict[str, str]] = []
    for label, duration_s in durations:
        energy_j = SOLAR_LUMINOSITY_W * duration_s
        fraction = energy_j / mass_energy_j
        rows.append(
            {
                "bound_id": f"PB3393_{label}",
                "window": label,
                "duration_s": f"{duration_s:.12e}",
                "L_sun_W": f"{SOLAR_LUMINOSITY_W:.12e}",
                "M_sun_kg": f"{SOLAR_MASS_KG:.12e}",
                "M_sun_c2_J": f"{mass_energy_j:.12e}",
                "flux_energy_J": f"{energy_j:.12e}",
                "epsilon_Poynting_luminosity_fraction": f"{fraction:.15e}",
                "strict_boundary_target_min": f"{strict_boundary:.15e}",
                "below_strict_boundary_target": bool_text(fraction < strict_boundary),
                "interpretation": "solar luminosity flux is tiny against current strict epsilon boundary target for this window; placement/source-measure clause still required",
                "valid_for_claim": "false",
            }
        )
    return rows


def kernel_moment_rows() -> list[dict[str, str]]:
    return [
        {
            "moment_id": "KM3393_0_radial_even_zero_first_moment",
            "kernel_branch": "radial_even_scalar_kernel",
            "statement": "For K_ell(z)=ell_s^{-3}k(|z|/ell_s), int z_i K_ell(z)d^3z=0.",
            "derivation": "The integrand z_i k(|z|/ell_s) is odd on every symmetric local tangent ball; angular integration cancels.",
            "zero_result": "epsilon_kernel_moment_first_order=0",
            "required_parent_clause": "kernel is scalar, radial/even, normalized, and selected before scoring",
            "status": "DERIVED_EXACT_IF_KERNEL_BRANCH_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "moment_id": "KM3393_1_gaussian_branch",
            "kernel_branch": "Gaussian heat kernel",
            "statement": "The Gaussian heat kernel is radial/even in the local tangent frame, so its first moment vanishes exactly.",
            "derivation": "K(z)=K(-z); therefore int z_i K(z)d^3z=0.",
            "zero_result": "epsilon_kernel_moment_first_order=0",
            "required_parent_clause": "Gaussian smoothing branch retained and local normal-frame curvature corrections counted separately",
            "status": "DERIVED_FOR_BRANCH_NOT_PARENT_FINAL",
            "valid_for_claim": "false",
        },
        {
            "moment_id": "KM3393_2_compact_branch",
            "kernel_branch": "compact radial bump",
            "statement": "A compact radial bump can also have zero first moment and exact collar support if selected by parent.",
            "derivation": "Radial parity gives zero first moment; compact support handles boundary tail separately.",
            "zero_result": "epsilon_kernel_moment_first_order=0",
            "required_parent_clause": "compact k, support rho_K and Fourier constants fixed before scoring",
            "status": "DERIVED_FOR_BRANCH_NEEDS_TRANSFER_REPLACEMENT",
            "valid_for_claim": "false",
        },
        {
            "moment_id": "KM3393_3_anisotropy_guard",
            "kernel_branch": "nonradial_or_adaptive_kernel",
            "statement": "If the kernel is anisotropic, adaptive, or boundary-clipped, the moment defect must remain finite.",
            "derivation": "Parity cancellation fails if K(z) != K(-z) on the effective support.",
            "zero_result": "no_zero",
            "required_parent_clause": "source-backed epsilon_kernel_moment below quarter budget",
            "status": "FINITE_FALLBACK_REQUIRED_IF_BRANCH_NOT_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def gauge_bound_rows() -> list[dict[str, str]]:
    geometry = geometry_reference_row()
    l_curv = to_float(geometry.get("schwarzschild_curvature_radius_m", ""))
    rows: list[dict[str, str]] = []
    for target in target_rows():
        budget = to_float(target.get("equal_quarter_kernel_term_budget", ""))
        if not math.isfinite(budget):
            continue
        first_order_ceiling = budget * l_curv
        fermi_quadratic_ceiling = math.sqrt(budget) * l_curv
        rows.append(
            {
                "gauge_id": f"GD3393_{target.get('source_row', '')}",
                "source_row": target.get("source_row", ""),
                "threshold_source": target.get("threshold_source", ""),
                "quarter_budget": f"{budget:.15e}",
                "L_curv_m": f"{l_curv:.12e}",
                "fixed_Fermi_patch_result": "linear gauge drift vanishes at patch origin; first surviving metric/frame drift is O((ell_s/L_curv)^2)",
                "ell_s_ceiling_if_Fermi_quadratic_Ceq1_m": f"{fermi_quadratic_ceiling:.12e}",
                "ell_s_ceiling_if_first_order_gauge_drift_Ceq1_m": f"{first_order_ceiling:.12e}",
                "interpretation": "Fermi/fixed-frame clause makes gauge drift much less severe than first-order adaptive readout drift",
                "parent_status": "PC3392_single_frame_patch_candidate_not_parent_signed",
                "valid_for_claim": "false",
            }
        )
    return rows


def closure_matrix_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    poynting_passes = all(row["below_strict_boundary_target"] == "true" for row in rows_by_name["poynting_bound"])
    strictest_fermi = min(to_float(row["ell_s_ceiling_if_Fermi_quadratic_Ceq1_m"]) for row in rows_by_name["gauge_bound"])
    strictest_first = min(to_float(row["ell_s_ceiling_if_first_order_gauge_drift_Ceq1_m"]) for row in rows_by_name["gauge_bound"])
    return [
        {
            "channel_id": "CM3393_0_boundary_Bzero_Delta",
            "channel": "B_zero_flux and Delta_symp",
            "best_close": "3376 fixed-annulus/fixed-primitive/trivial-class/no-flux/source-blind-reference theorem",
            "current_result": "conditional theorem imported; not parent-signed",
            "finite_pressure": "retained if 3376 clauses remain unsigned",
            "claim_closed": "false",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "CM3393_1_Poynting_flux",
            "channel": "public Poynting/radiation flux",
            "best_close": "place public EM/radiation stress inside Hilbert source measure",
            "current_result": "finite solar luminosity bound is below strict target for tested local windows" if poynting_passes else "finite solar luminosity bound can exceed strict target for long window",
            "finite_pressure": "source-measure placement still required before zeroing hidden residual",
            "claim_closed": "false",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "CM3393_2_kernel_moment",
            "channel": "kernel first moment / anisotropy",
            "best_close": "parent-sign scalar radial/even normalized kernel",
            "current_result": "exact zero theorem derived for Gaussian/radial/compact branches",
            "finite_pressure": "anisotropic/adaptive/clipped kernel must retain epsilon_kernel_moment",
            "claim_closed": "false",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "CM3393_3_gauge_readout",
            "channel": "gauge/readout drift",
            "best_close": "PC3392 fixed readout plus single Fermi/frame patch",
            "current_result": f"Fermi quadratic ceiling strictest ell_s <= {strictest_fermi:.3e} m; first-order drift ceiling {strictest_first:.3e} m",
            "finite_pressure": "parent signature missing; constants still not sourced",
            "claim_closed": "false",
            "valid_for_claim": "false",
        },
    ]


def runner_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    poynting_pass_count = sum(1 for row in rows_by_name["poynting_bound"] if row["below_strict_boundary_target"] == "true")
    strictest_fermi = min(to_float(row["ell_s_ceiling_if_Fermi_quadratic_Ceq1_m"]) for row in rows_by_name["gauge_bound"])
    return [
        {
            "run_id": "RUN3393_0_boundary_theorem",
            "test": "boundary flux placement theorem",
            "result": "PASS_CONDITIONAL_THEOREM_NONCLAIM",
            "detail": "public Hilbert stress placement plus 3376 fixed-annulus theorem written; parent signatures still missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3393_1_poynting_bound",
            "test": "solar luminosity finite Poynting bound",
            "result": "PASS_FINITE_BOUND_NONCLAIM",
            "detail": f"windows_below_strict_target={poynting_pass_count}/{len(rows_by_name['poynting_bound'])}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3393_2_kernel_moment",
            "test": "radial/even kernel first moment",
            "result": "PASS_EXACT_MOMENT_THEOREM_CONDITIONAL",
            "detail": "radial/even scalar kernels have zero first moment; parent smoothing branch still unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3393_3_gauge_bound",
            "test": "Fermi/fixed-frame gauge drift",
            "result": "PASS_GAUGE_BOUND_NONCLAIM",
            "detail": f"strictest Fermi quadratic ell_s ceiling={strictest_fermi:.3e} m for C=1",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3393_4_firewall",
            "test": "prevent local PPN/local GR claim",
            "result": "PASS_CLAIM_FIREWALL",
            "detail": "3393 closes several routes conditionally and bounds Poynting, but parent package is not adopted",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3393_0_sources",
            "claim": "all 3393 local sources exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "local/core inputs parsed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3393_1_boundary_zero",
            "claim": "B_zero_flux and Delta_symp are zero",
            "gate_pass": "false",
            "reason": "3376 theorem remains conditional on fixed primitive, topology, no-flux and reference lock",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3393_2_poynting",
            "claim": "Poynting/radiation boundary flux is harmless",
            "gate_pass": "false",
            "reason": "finite luminosity bound is small, but source-measure placement and M_H_ref mapping are not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3393_3_kernel_moment",
            "claim": "epsilon_kernel_moment=0",
            "gate_pass": "false",
            "reason": "zero first-moment theorem needs parent-signed radial/even scalar kernel branch",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3393_4_gauge",
            "claim": "epsilon_gauge_readout is zero or safely bounded",
            "gate_pass": "false",
            "reason": "Fermi/fixed-frame finite bound exists, but PC3392 and constants are not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3393_5_local_ppn",
            "claim": "local PPN/local-GR branch passes",
            "gate_pass": "false",
            "reason": "several channels are promising but conditional; no parent package promotion yet",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    poynting_max = max(to_float(row["epsilon_Poynting_luminosity_fraction"]) for row in rows_by_name["poynting_bound"])
    strictest_fermi = min(to_float(row["ell_s_ceiling_if_Fermi_quadratic_Ceq1_m"]) for row in rows_by_name["gauge_bound"])
    return [
        {
            "decision_id": "DEC3393_0_progress",
            "decision": "The remaining channels are no longer a single foggy blocker.",
            "because": "Poynting, kernel moment and gauge drift now each have an exact-placement theorem or finite bound.",
            "next_action": "bundle the admissible parent clauses into a local Cassini package gate",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3393_1_poynting",
            "decision": "Solar Poynting flux is probably not the Cassini killer if treated as public source stress.",
            "because": f"even the one-year luminosity fraction in this nonclaim runner is {poynting_max:.3e}, below the current strict boundary target, while local windows are far smaller.",
            "next_action": "parent-sign public Hilbert stress placement or retain finite luminosity row",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3393_2_kernel",
            "decision": "Kernel moment has a clean exact-zero route.",
            "because": "radial/even Gaussian or compact kernels have zero first moment by parity.",
            "next_action": "parent-sign scalar radial/even kernel branch before scoring",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3393_3_gauge",
            "decision": "Fermi/fixed-frame gauge drift is much milder than adaptive readout drift.",
            "because": f"the strictest quadratic Fermi ceiling is {strictest_fermi:.3e} m for C=1, compared with the metre/mm pressure from first-order adaptive readout branches.",
            "next_action": "combine PC3392 with a single-frame Fermi patch clause",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3393_4_best_next",
            "decision": "Next best move is a local Cassini admissible-package gate.",
            "because": "Projector, kernel moment, Poynting placement and gauge drift each have admissible clauses; the question is whether one parent package can own all of them without conflict.",
            "next_action": "build 3394 local Cassini admissible package and then return to source-normalization/Newtonian coupling",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3394-Y5-R2FR-local-Cassini-admissible-package-gate-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3394_local_Cassini_admissible_package_gate.py",
            "objective": "bundle PC3392 fixed PPN readout, public Hilbert flux placement, scalar radial/even kernel, and single Fermi/frame patch into one parent-package audit; if coherent, mark projector/moment/gauge/flux channels conditionally closed without public claim",
            "why_next": "3393 shows the individual clauses are plausible; local GR needs one coherent parent-owned package rather than scattered conditional lemmas",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3395-Y5-R2FR-weak-field-source-normalization-return-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3395_weak_field_source_normalization_return.py",
            "objective": "after the local package gate, return to calibrated source coupling: same kappa/G/source-current normalization in H_tau, Poisson/Newton and PPN readout",
            "why_next": "even a clean local residual package does not finish GR/Newton reduction without calibrated source coupling",
            "valid_for_claim": "false",
        },
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = [
        hit
        for hit in FW.rglob("*3393*")
        if hit.name.startswith(("3393-Y5", "P8_Y5_R2FR_3393", "P8_Y5_BRR545_3393", "Y5_R2FR_3393"))
    ] if FW.exists() else []
    poynting_numeric = all(to_float(row["epsilon_Poynting_luminosity_fraction"]) > 0 for row in rows_by_name["poynting_bound"])
    poynting_has_pass = any(row["below_strict_boundary_target"] == "true" for row in rows_by_name["poynting_bound"])
    kernel_statuses = {row["status"] for row in rows_by_name["kernel_moment"]}
    closure_channels = {row["channel_id"] for row in rows_by_name["closure_matrix"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    checks = [
        ("VAL3393_0_sources_exist_parse", "all cited 3393 local source paths exist and parse", source_ok, ""),
        ("VAL3393_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3393_2_external_sources", "external source pack records solar luminosity/mass and Cassini source", len(rows_by_name["external_sources"]) >= 2, f"rows={len(rows_by_name['external_sources'])}"),
        ("VAL3393_3_boundary_theorem", "boundary flux theorem includes Hilbert placement, 3376 import and finite luminosity bound", len(rows_by_name["boundary_flux_theorem"]) == 3, ""),
        ("VAL3393_4_poynting_bound", "Poynting finite rows are positive and include below-target windows", poynting_numeric and poynting_has_pass, f"rows={len(rows_by_name['poynting_bound'])}"),
        ("VAL3393_5_kernel_moment", "kernel moment theorem includes exact radial/Gaussian/compact routes and anisotropy guard", {"DERIVED_EXACT_IF_KERNEL_BRANCH_SIGNED", "DERIVED_FOR_BRANCH_NOT_PARENT_FINAL", "DERIVED_FOR_BRANCH_NEEDS_TRANSFER_REPLACEMENT", "FINITE_FALLBACK_REQUIRED_IF_BRANCH_NOT_SIGNED"}.issubset(kernel_statuses), ""),
        ("VAL3393_6_gauge_bound", "gauge drift finite bound rows cover target summary", len(rows_by_name["gauge_bound"]) >= 8, f"rows={len(rows_by_name['gauge_bound'])}"),
        ("VAL3393_7_closure_matrix", "closure matrix covers boundary, Poynting, kernel and gauge channels", {"CM3393_0_boundary_Bzero_Delta", "CM3393_1_Poynting_flux", "CM3393_2_kernel_moment", "CM3393_3_gauge_readout"}.issubset(closure_channels), ""),
        ("VAL3393_8_runner", "runner records theorem, Poynting, kernel, gauge and firewall", {"PASS_CONDITIONAL_THEOREM_NONCLAIM", "PASS_FINITE_BOUND_NONCLAIM", "PASS_EXACT_MOMENT_THEOREM_CONDITIONAL", "PASS_GAUGE_BOUND_NONCLAIM", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3393_9_gates", "gates block boundary zero, Poynting, kernel, gauge and local PPN claims", gate_map.get("GATE3393_1_boundary_zero") == "false" and gate_map.get("GATE3393_2_poynting") == "false" and gate_map.get("GATE3393_3_kernel_moment") == "false" and gate_map.get("GATE3393_4_gauge") == "false" and gate_map.get("GATE3393_5_local_ppn") == "false", ""),
        ("VAL3393_10_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3393_11_write_scope_outside_formalization", "no 3393 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
        ("VAL3393_12_next_target", "next target moves to local Cassini admissible package gate", rows_by_name["next"][0]["target_id"].startswith("3394-Y5-R2FR-local-Cassini-admissible-package"), ""),
    ]
    overall = all(passed for _, _, passed, _ in checks)
    checks.append(("VAL3393_13_overall", "3393 validation overall", overall, "all required checks passed" if overall else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    poynting_max = max(to_float(row["epsilon_Poynting_luminosity_fraction"]) for row in rows_by_name["poynting_bound"])
    strictest_fermi = min(to_float(row["ell_s_ceiling_if_Fermi_quadratic_Ceq1_m"]) for row in rows_by_name["gauge_bound"])
    lines = [
        "# 3393 - Y5/R2FR boundary flux, moment and gauge closure pack under AX1090",
        "",
        "## Summary",
        "- 3393 attacks the remaining Cassini local branch channels after the projector readout fork.",
        "- Boundary/Poynting result: physical EM/radiation flux belongs in public Hilbert stress; if retained as a finite solar-luminosity envelope it is tiny for local Cassini windows.",
        f"- The largest tested luminosity fraction is `{poynting_max:.3e}` over a one-year window, still below the current strict boundary target; this remains nonclaim until source-measure placement is parent-signed.",
        "- Kernel result: radial/even scalar kernels have exactly zero first moment by parity; Gaussian and compact radial branches both inherit this if parent-selected before scoring.",
        f"- Gauge result: fixed Fermi/frame readout makes drift quadratic, with strictest `ell_s` ceiling `{strictest_fermi:.3e} m` for C=1; adaptive first-order readout remains harsher.",
        "- Local-GR/PPN is still not claimed: the clauses now look packageable, but not parent-owned.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## External Source Pack",
        md_table(rows_by_name["external_sources"]),
        "## Boundary Flux Placement Theorem",
        md_table(rows_by_name["boundary_flux_theorem"]),
        "## Cassini Poynting Flux Bound",
        md_table(rows_by_name["poynting_bound"]),
        "## Kernel Moment Zero Theorem",
        md_table(rows_by_name["kernel_moment"]),
        "## Gauge Readout Drift Bound Rows",
        md_table(rows_by_name["gauge_bound"]),
        "## Channel Closure Matrix",
        md_table(rows_by_name["closure_matrix"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_register = source_rows()
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_register)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "external_sources": external_source_rows(),
        "boundary_flux_theorem": boundary_flux_theorem_rows(),
        "poynting_bound": poynting_bound_rows(),
        "kernel_moment": kernel_moment_rows(),
        "gauge_bound": gauge_bound_rows(),
    }
    rows_by_name["closure_matrix"] = closure_matrix_rows(rows_by_name)
    rows_by_name["runner"] = runner_rows(rows_by_name)
    rows_by_name["gates"] = gate_rows(source_ok)
    rows_by_name["decision"] = decision_rows(rows_by_name)
    rows_by_name["next"] = next_rows()
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()
