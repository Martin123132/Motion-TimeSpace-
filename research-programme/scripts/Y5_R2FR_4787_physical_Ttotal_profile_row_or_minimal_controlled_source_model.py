from __future__ import annotations

import csv
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from Y5_R2FR_4785_real_source_profile_integral_and_residual_radius_row import (  # noqa: E402
    DENSITY_RUNNER,
    G_CAL,
    M_GM_SUN_CAL,
    MU_SUN_NOMINAL,
    OPEN_RUNNER,
    PARENT_CHARGE_RUNNER,
    PROFILE_RUNNER,
    RESIDUAL_FIELDS,
    RHOH_RUNNER,
    SOLAR_RADIUS_NOMINAL,
    SOURCE_RUNNER,
    density_input_from_rhoh,
    format_float,
    markdown_table,
    open_input_from_source,
    parent_input_from_density,
    parse_csv,
    residual_row,
    rhoh_input_from_profile,
    score_rows,
    signed_profile_clauses,
    source_input_from_parent,
    write_csv,
)


CONTROLLED_RUNNER = SCRIPT_DIR / "controlled_Ttotal_profile_runner.py"

CHECKPOINT = "4787"
CLAIM_ID = "L-629"
MARKER = "PPC4161_PHYSICAL_TTOTAL_PROFILE_ROW_OR_MINIMAL_CONTROLLED_SOURCE_MODEL_4787"
PACKET_MARKER = "PPC4161_PACKET_PHYSICAL_TTOTAL_PROFILE_ROW_OR_MINIMAL_CONTROLLED_SOURCE_MODEL_4787"
DECISION = "CONTROLLED_TTOTAL_PROFILE_RUNNER_INSTALLED_MINIMAL_SOURCE_MODEL_COMPUTES_PROFILE_NONCLAIM_RESIDUAL_CERTIFICATE_STILL_GATES_LOCAL_GR"
NEXT_TARGET = "4788-Y5-R2FR-close-Req-Bzero-boundary-projector-domain-or-controlled-source-testbench.md"

DOC_PATH = POST / "4787-Y5-R2FR-physical-Ttotal-profile-row-or-minimal-controlled-source-model.md"
FORMAL_PATH = FORMAL / "803-PPC4161-physical-Ttotal-profile-row-or-minimal-controlled-source-model.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_SOURCE_REGISTER.csv"
LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_CONTROLLED_TTOTAL_LAW.csv"
CONTROLLED_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_CONTROLLED_TTOTAL_INPUT.csv"
CONTROLLED_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_CONTROLLED_TTOTAL_OUTPUT.csv"
PROFILE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_SOURCE_PROFILE_INPUT_FROM_CONTROLLED.csv"
PROFILE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_SOURCE_PROFILE_OUTPUT_FROM_CONTROLLED.csv"
RHOH_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_RHOH_INPUT_FROM_CONTROLLED_PROFILE.csv"
RHOH_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_RHOH_OUTPUT_FROM_CONTROLLED_PROFILE.csv"
DENSITY_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_DENSITY_INPUT_FROM_CONTROLLED_PROFILE.csv"
DENSITY_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_DENSITY_OUTPUT_FROM_CONTROLLED_PROFILE.csv"
PARENT_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_PARENT_CHARGE_INPUT_FROM_CONTROLLED_PROFILE.csv"
PARENT_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_PARENT_CHARGE_OUTPUT_FROM_CONTROLLED_PROFILE.csv"
SOURCE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_HTAU_HREF_SOURCE_INPUT.csv"
SOURCE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_HTAU_HREF_SOURCE_OUTPUT.csv"
OPEN_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_OPEN_ARENA_INPUT.csv"
OPEN_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_OPEN_ARENA_OUTPUT.csv"
SCORE_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_SCORE_GATE_UPDATE.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_FIREWALL_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_ROUTE_SELECTION_MATRIX.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4787_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4787_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4787_00_4786_doc", POST / "4786-Y5-R2FR-source-profile-physical-values-or-parent-zero-profile-certificate.md", "controlled physical `T_total(n,n)` profile row", "4786 selected controlled Ttotal profile target"),
    ("SRC4787_01_4786_zero", SOURCE_DIR / "P8_Y5_R2FR_4786_RESIDUAL_ZERO_AGGREGATE_OUTPUT.csv", "physical_partial_parent_zero_attempt", "4786 zero certificate outputs"),
    ("SRC4787_02_4785_profile_runner", PROFILE_RUNNER, "def compute_profile", "profile integral/radius runner"),
    ("SRC4787_03_4786_zero_runner", SCRIPT_DIR / "residual_radius_zero_certificate_runner.py", "def aggregate_certificate", "residual zero certificate runner"),
    ("SRC4787_04_3883_doc", POST / "3883-Y5-R2FR-Hilbert-source-and-Maxwell-stress-lock-or-residual-vector.md", "T_EM^{mu nu}", "Hilbert/Maxwell stress source rule"),
    ("SRC4787_05_4587_doc", POST / "4587-Y5-R2FR-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md", "Poynting rule is once-only", "Poynting once-only rule"),
    ("SRC4787_06_controlled_runner", CONTROLLED_RUNNER, "def compute_row", "4787 controlled Ttotal profile runner"),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def run_command(args: list[str]) -> None:
    subprocess.run(args, check=True, cwd=str(ROOT))


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def law_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("CTL4787_0_Ttotal", "T_total(n,n)=rho_rest c^2+u_internal+u_EM+u_rad", "minimal controlled profile source density"),
        ("CTL4787_1_volume", "rho_H(W)=int_W T_total(n,n)dV/c^2", "turns controlled local energy density into the profile integral"),
        ("CTL4787_2_pressure", "pressure/stress is reported but not hidden inside rho_H unless it enters T(n,n)", "keeps PPN pressure/stress effects separate"),
        ("CTL4787_3_poynting", "u_EM is Hilbert Maxwell energy; radiative Poynting is boundary/open_EM residual", "prevents double-counting EM flow"),
        ("CTL4787_4_firewall", "GM/PPN/clock/R10 readouts cannot set rho_rest, u_EM, volume, or normalization", "keeps controlled source upstream of tests"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "law_id": law_id,
            "rule": rule,
            "meaning": meaning,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for law_id, rule, meaning in specs
    ]


def controlled_clauses(value: bool) -> dict[str, bool]:
    return {
        "parent_action_signed": value,
        "same_frame_signed": value,
        "variation_before_readout_signed": value,
        "compact_support_signed": value,
        "volume_measure_signed": value,
        "positive_energy_signed": value,
        "poynting_once_signed": value,
        "no_flux_or_residual_signed": value,
        "no_species_prefactor_signed": value,
        "no_postfit_signed": value,
        "shared_profile_signed": value,
    }


def controlled_row(model_id: str, profile_id: str, rest_density: str, internal: str, em: str, radiation: str, volume: str, status: str, source: str, timestamp: str, clauses: dict[str, bool], pressure: str = "") -> dict[str, Any]:
    return {
        "model_id": model_id,
        "profile_id": profile_id,
        "rest_mass_density_kg_m3": rest_density,
        "internal_energy_density_J_m3": internal,
        "EM_energy_density_J_m3": em,
        "radiation_energy_density_J_m3": radiation,
        "pressure_Pa": pressure,
        "T_total_nn_J_m3": "",
        "volume_m3": volume,
        "r_inner_m": "",
        "r_outer_m": "",
        "model_source": source,
        "density_source": source,
        "volume_source": source,
        "EM_source": source,
        "normalization_source": "CONTROLLED_PROFILE_NOT_ARENA_READOUT",
        "provenance": source,
        "notes": "",
        "row_status": status,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
        **clauses,
    }


def controlled_input_rows(timestamp: str) -> list[dict[str, Any]]:
    signed = controlled_clauses(True)
    unsigned = controlled_clauses(False)
    return [
        controlled_row("physical_controlled_profile_values_missing", "physical_controlled_profile_values_missing", "", "", "", "", "", "physical_values_missing_nonclaim", "MISSING_PARENT_DENSITY_AND_VOLUME", timestamp, unsigned),
        controlled_row("controlled_uniform_partial_zero_model", "controlled_uniform_partial_zero_model", "1", "0", "0", "0", "1", "controlled_partial_zero_nonclaim", "CONTROLLED_UNIT_DUST_PROFILE", timestamp, signed),
        controlled_row("private_uniform_dust_full_zero_model", "private_uniform_dust_full_zero_model", "1", "0", "0", "0", "1", "private_controlled_profile_nonclaim", "PRIVATE_CONTROLLED_UNIT_DUST_PROFILE", timestamp, signed),
        controlled_row("controlled_matter_EM_finite_bound_smoke", "controlled_matter_EM_finite_bound_smoke", "1.0e30", "1.0e6", "2.0e6", "0", "3", "finite_controlled_profile_smoke_nonclaim", "SMOKE_CONTROLLED_MATTER_EM_PROFILE_NOT_PHYSICAL", timestamp, signed, pressure="1.0e5"),
        controlled_row("forbidden_orbital_GM_Ttotal_control", "forbidden_orbital_GM_Ttotal_control", format_float(M_GM_SUN_CAL), "0", "0", "0", "1", "physical_forbidden_circular_ttotal_control_nonclaim", "ORBITAL_GM_DEFINITION_FORBIDDEN_CONTROL", timestamp, signed),
        controlled_row("counterfactual_solar_mass_profile", "counterfactual_solar_mass_profile", format_float(M_GM_SUN_CAL), "0", "0", "0", "1", "counterfactual_smoke_nonclaim", "COUNTERFACTUAL_RUNNER_SMOKE_ONLY", timestamp, signed),
    ]


def profile_mass_component_from_controlled(output: dict[str, Any], timestamp: str) -> dict[str, Any]:
    signed = signed_profile_clauses(True)
    valid_mass = not str(output["rho_H_integral_kg"]).startswith("MISSING") and not str(output["runner_status"]).startswith("FAILED")
    source = "controlled_Ttotal_profile_runner.py" if valid_mass else "MISSING_OR_FAILED_CONTROLLED_PROFILE"
    if output["runner_status"] == "FAILED_CIRCULAR_TTOTAL_PROFILE_SOURCE":
        source = "ORBITAL_GM_DEFINITION_FORBIDDEN_CONTROL"
    return {
        "profile_id": output["profile_id"],
        "component_id": output["model_id"] + "_mass",
        "component_kind": "mass",
        "residual_symbol": "",
        "r_inner_m": "",
        "r_outer_m": "",
        "volume_m3": "",
        "rho_H_kg_m3": "",
        "T_total_nn_J_m3": "",
        "component_mass_kg": output["rho_H_integral_kg"] if valid_mass else "",
        "residual_abs_kg": "",
        "c_m_s": "299792458",
        "source_path": source,
        "component_source": source,
        "normalization_source": "CONTROLLED_TTOTAL_PROFILE",
        "residual_source": "",
        "extraction_method": "controlled_Ttotal_profile_runner",
        "confidence": "controlled_nonclaim",
        "notes": "",
        "row_status": output["row_status_input"],
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
        **signed,
    }


def add_available_residuals(rows: list[dict[str, Any]], profile_id: str, aggregate: dict[str, Any], row_status: str, timestamp: str, source: str, clauses: dict[str, bool]) -> None:
    field_to_symbol = {
        "R_eq_abs_kg": "R_eq",
        "B_zero_abs_kg": "B_zero",
        "boundary_flux_abs_kg": "boundary_flux",
        "open_EM_abs_kg": "open_EM",
        "nonEM_owner_gap_abs_kg": "nonEM_owner_gap",
        "projector_comm_abs_kg": "projector_comm",
        "domain_shadow_abs_kg": "domain_shadow",
        "kappa_drift_abs_kg": "kappa_drift",
    }
    for field in RESIDUAL_FIELDS:
        value = aggregate.get(field, "MISSING_NUMERIC_VALUE")
        if str(value).startswith("MISSING"):
            continue
        rows.append(residual_row(profile_id, f"{profile_id}_{field}", field_to_symbol[field], value, row_status, timestamp, source, clauses))


def profile_input_from_controlled(timestamp: str, controlled_output: list[dict[str, Any]], zero_aggregate: list[dict[str, Any]]) -> list[dict[str, Any]]:
    zero_by_id = {row["certificate_id"]: row for row in zero_aggregate}
    controlled_by_profile = {row["profile_id"]: row for row in controlled_output}
    rows: list[dict[str, Any]] = []
    signed = signed_profile_clauses(True)

    for output in controlled_output:
        rows.append(profile_mass_component_from_controlled(output, timestamp))

    add_available_residuals(rows, "controlled_uniform_partial_zero_model", zero_by_id["physical_partial_parent_zero_attempt"], "controlled_partial_zero_nonclaim", timestamp, "partial_zero_certificate_4786", signed)
    add_available_residuals(rows, "private_uniform_dust_full_zero_model", zero_by_id["private_full_zero_certificate_control"], "private_controlled_profile_nonclaim", timestamp, "private_full_zero_certificate_4786", signed)
    add_available_residuals(rows, "controlled_matter_EM_finite_bound_smoke", zero_by_id["finite_residual_bound_smoke_nonclaim"], "finite_controlled_profile_smoke_nonclaim", timestamp, "finite_residual_bound_certificate_4786", signed)
    add_available_residuals(rows, "forbidden_orbital_GM_Ttotal_control", zero_by_id["private_full_zero_certificate_control"], "physical_forbidden_circular_ttotal_control_nonclaim", timestamp, "private_full_zero_certificate_4786", signed)
    add_available_residuals(rows, "counterfactual_solar_mass_profile", zero_by_id["counterfactual_full_zero_certificate"], "counterfactual_smoke_nonclaim", timestamp, "COUNTERFACTUAL_RUNNER_SMOKE_ONLY", signed)

    return rows


def simple_rows(timestamp: str, kind: str) -> list[dict[str, Any]]:
    if kind == "gates":
        specs = [
            ("PG4787_0", "controlled source profile must compute T_total(n,n) from local densities and volume"),
            ("PG4787_1", "controlled mass without complete residual certificate still blocks Mlower"),
            ("PG4787_2", "private full-zero controlled model is nonclaim only"),
            ("PG4787_3", "orbital GM cannot define rest density or Ttotal"),
            ("PG4787_4", "pressure/stress remains visible for later PPN rather than hidden in rhoH"),
        ]
        return [{"checkpoint": CHECKPOINT, "gate_id": row_id, "rule": text, "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text in specs]
    if kind == "firewalls":
        specs = [
            ("FW4787_0", "no observed-GM/Gcal in controlled Ttotal source", "ACTIVE"),
            ("FW4787_1", "no PPN/clock/R10 fitted profile input", "ACTIVE"),
            ("FW4787_2", "no double-counted Poynting source", "ACTIVE"),
            ("FW4787_3", "no public/local-GR claim from controlled smoke models", "LOCAL_PRIVATE_ONLY"),
        ]
        return [{"checkpoint": CHECKPOINT, "firewall_id": row_id, "firewall_rule": text, "status": status, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text, status in specs]
    if kind == "routes":
        specs = [
            ("RT4787_0_missing_residuals", "close or bound R_eq/B_zero/boundary/nonHilbert/projector/domain for controlled source", "SELECTED_NEXT"),
            ("RT4787_1_testbench", "promote the controlled source into a local testbench once residuals close", "SELECTED_NEXT_PARALLEL"),
            ("RT4787_2_physical_values", "replace unit/smoke density with source-backed physical density and volume rows", "SELECTED_NEXT_PARALLEL"),
        ]
        return [{"checkpoint": CHECKPOINT, "route_id": row_id, "route": text, "selection_status": status, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text, status in specs]
    raise ValueError(kind)


def write_docs(timestamp: str, law: list[dict[str, Any]], controlled_output: list[dict[str, Any]], profile_output: list[dict[str, Any]], rhoh_output: list[dict[str, Any]], score: list[dict[str, Any]], routes: list[dict[str, Any]]) -> None:
    content = f"""# 4787 - Physical Ttotal profile row or minimal controlled source model

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4787 builds the minimal controlled-source model needed by the local GR/Newton branch:

```text
T_total(n,n) = rho_rest c^2 + u_internal + u_EM + u_rad
rho_H(W_H) = int_W T_total(n,n)dV / c^2.
```

This is not a solar/planetary claim. It is a controlled upstream source model: density, EM energy and volume are declared before any arena readout. Orbital `GM`, PPN residuals, clock calibration and R10 bounds cannot define the profile.

## Controlled Ttotal Law

{markdown_table(law, ["law_id", "rule", "meaning"])}

## Controlled Runner Output

{markdown_table(controlled_output, ["model_id", "profile_id", "rho_H_integral_kg", "T_total_mode", "pressure_to_energy_ratio", "runner_status"])}

## Profile Runner Output

{markdown_table(profile_output, ["profile_id", "rho_H_integral_kg", "Delta_H_abs_kg", "residual_radius_mode", "runner_status"])}

## rhoH Runner Output

{markdown_table(rhoh_output, ["density_id", "rho_H_integral_kg", "H_tau_bulk_kg", "M0_kg", "epsilon_abs", "M_lower_kg", "runner_status"])}

## Chain Score

{markdown_table(score, ["profile_id", "profile_runner_status", "rhoh_runner_status", "density_runner_status", "parent_runner_status", "source_runner_status", "open_runner_status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "selection_status"])}

## Conclusion

The profile-value blocker is no longer abstract. A controlled `T_total(n,n)` source can be computed from local density/energy/volume rows and passed into the chain. The remaining failure is the same six residual components identified by 4786: `R_eq`, `B_zero`, boundary, non-Hilbert owner gap, projector commutator and domain shadow.

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, content)

    formal = f"""# PPC4161 4787: Physical Ttotal Profile Row Or Minimal Controlled Source Model

Generated: `{timestamp}`

4787 installs the controlled `T_total(n,n)` profile runner. It computes `rho_H(W_H)` from declared local energy density and volume, rejects orbital-GM source import, and demonstrates that controlled source mass still needs the residual-radius certificate before local GR/Newton scoring.

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def append_outputs(timestamp: str) -> None:
    decision = [{"checkpoint": CHECKPOINT, "decision": DECISION, "meaning": "Controlled Ttotal source profile computes without GM backfill; residual certificate remains the live gate.", "next_target": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp}]
    status = [{"checkpoint": CHECKPOINT, "status": "PASS_CONTROLLED_TTOTAL_PROFILE_RUNNER_INSTALLED_NONCLAIM", "summary": "Controlled source model computes; partial residuals still block; forbidden GM source fails.", "valid_for_claim": False, "timestamp_utc": timestamp}]
    next_target = [{"checkpoint": CHECKPOINT, "next_target": NEXT_TARGET, "reason": "Need close/bound residual components or build controlled local testbench.", "valid_for_claim": False, "timestamp_utc": timestamp}]
    write_csv(DECISION_CSV, decision)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_target)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "controlled_Ttotal_profile_runner",
        "4787 installs a minimal controlled source-profile runner that computes rho_H(W_H) from local T_total(n,n) density and volume.",
        "Generated source register, controlled law, controlled/profile/rhoH/density/parent/source/open chain outputs, score gates, firewalls, routes, decision, status, next target and validation.",
        "controlled_Ttotal_profile_private_nonclaim",
        NEXT_TARGET,
        "Do not treat controlled unit/smoke profiles or private zero certificates as local-GR evidence.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need close or bound R_eq/B_zero/boundary/nonHilbert/projector/domain residuals and replace smoke values with source-backed physical rows.",
        "controlled Ttotal source profile",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def update_resume(timestamp: str) -> None:
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Last checkpoint: `{DOC_PATH.name}`
Generated: `{timestamp}`

## Current target

`{NEXT_TARGET}`

## Live blocker

The minimal controlled `T_total(n,n)` source profile is now executable: `rho_H(W_H)=int_W T_total(n,n)dV/c^2` can be computed from declared density/energy/volume rows without orbital-GM backfill. The live gate is now closing or bounding the six same-branch residual components that still block the controlled source from becoming a local-GR/Newton testbench: `R_eq`, `B_zero`, boundary flux, non-Hilbert owner gap, projector commutator and domain shadow.

## Firewalls

- No GitHub/public action from this checkpoint.
- No observed-GM/Gcal, PPN, clock, R10, or post-fit residual backfill into source or residual rows.
- Controlled source models are private/nonclaim until residuals close and physical source values are source-backed.
""",
    )


def append_spine_and_packet(timestamp: str) -> None:
    append_once(SPINE_PATH, MARKER, f"\n\n## {MARKER}\n\n4787 installs `controlled_Ttotal_profile_runner.py`. Controlled local energy-density/volume rows can now compute `rho_H(W_H)` without importing orbital `GM`. The remaining local-GR blocker is the same-branch residual certificate for `R_eq`, `B_zero`, boundary, non-Hilbert owner gap, projector commutator and domain shadow. Decision: `{DECISION}`. Next: `{NEXT_TARGET}`.\n")
    append_once(PACKET_PATH, PACKET_MARKER, f"\n\n## {PACKET_MARKER}\n\nRunner: `{CONTROLLED_RUNNER}`. Minimal controlled source model computes profile mass; residual certificate still gates local-GR/Newton scoring. Generated `{timestamp}`.\n")


def validate(timestamp: str, sources: list[dict[str, Any]], controlled_output: list[dict[str, Any]], profile_output: list[dict[str, Any]], rhoh_output: list[dict[str, Any]], density_output: list[dict[str, Any]], open_output: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks = [
        ("VAL4787_0_sources", "source paths and needles exist", all(row["exists"] is True and row["needle_found"] is True for row in sources), str(SOURCE_REGISTER_CSV)),
        ("VAL4787_1_missing_profile_blocks", "physical missing controlled profile blocks", any(row["model_id"] == "physical_controlled_profile_values_missing" and row["runner_status"] == "BLOCKED_MISSING_CONTROLLED_TTOTAL_PROFILE_INPUTS" for row in controlled_output), str(CONTROLLED_OUTPUT_CSV)),
        ("VAL4787_2_partial_zero_blocks", "controlled profile with partial residuals blocks rhoH", any(row["density_id"] == "controlled_uniform_partial_zero_model" and row["runner_status"] == "BLOCKED_MISSING_RHOH_RESIDUAL_RADIUS" for row in rhoh_output), str(RHOH_OUTPUT_CSV)),
        ("VAL4787_3_private_full_zero_computes", "private controlled profile full-zero computes", any(row["profile_id"] == "private_uniform_dust_full_zero_model" and row["runner_status"] == "PROFILE_INTEGRAL_AND_RADIUS_EXACT_PRIVATE_NONCLAIM" for row in profile_output), str(PROFILE_OUTPUT_CSV)),
        ("VAL4787_4_finite_bound_computes", "controlled matter+EM finite bound computes interval", any(row["density_id"] == "controlled_matter_EM_finite_bound_smoke" and row["runner_status"] == "RHOH_PARENT_INTEGRAL_INTERVAL_COMPUTED_NONCLAIM" for row in rhoh_output), str(RHOH_OUTPUT_CSV)),
        ("VAL4787_5_forbidden_GM_fails", "forbidden orbital GM Ttotal source fails", any(row["model_id"] == "forbidden_orbital_GM_Ttotal_control" and row["runner_status"] == "FAILED_CIRCULAR_TTOTAL_PROFILE_SOURCE" for row in controlled_output), str(CONTROLLED_OUTPUT_CSV)),
        ("VAL4787_6_counterfactual_density", "counterfactual reaches density runner", any(row["density_id"] == "counterfactual_solar_mass_profile" and row["runner_status"] == "DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM" for row in density_output), str(DENSITY_OUTPUT_CSV)),
        ("VAL4787_7_open_counterfactual", "counterfactual reaches open runner", any(row["arena_id"] == "counterfactual_solar_mass_profile" and row["runner_status"] == "RUNNER_SMOKE_PASS_NONCLAIM" for row in open_output), str(OPEN_OUTPUT_CSV)),
        ("VAL4787_8_gates", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)),
        ("VAL4787_9_claim", "claim row L-629 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)),
        ("VAL4787_10_resume", "resume points to next target", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH)),
    ]
    rows: list[dict[str, Any]] = []
    for validation_id, check, passed, detail in checks:
        rows.append({"checkpoint": CHECKPOINT, "validation_id": validation_id, "check": check, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "timestamp_utc": timestamp})
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"checkpoint": CHECKPOINT, "validation_id": "VAL4787_OVERALL", "check": "all 4787 controlled Ttotal profile checks pass", "status": "PASS" if overall else "FAIL", "detail": DECISION, "valid_for_claim": False, "timestamp_utc": timestamp})
    return rows


def main() -> None:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_register(timestamp)
    law = law_rows(timestamp)
    controlled_input = controlled_input_rows(timestamp)
    gates = simple_rows(timestamp, "gates")
    firewalls = simple_rows(timestamp, "firewalls")
    routes = simple_rows(timestamp, "routes")

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(LAW_CSV, law)
    write_csv(CONTROLLED_INPUT_CSV, controlled_input)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(ROUTE_MATRIX_CSV, routes)

    run_command([sys.executable, str(CONTROLLED_RUNNER), str(CONTROLLED_INPUT_CSV), str(CONTROLLED_OUTPUT_CSV)])
    controlled_output = parse_csv(CONTROLLED_OUTPUT_CSV)

    zero_aggregate = parse_csv(SOURCE_DIR / "P8_Y5_R2FR_4786_RESIDUAL_ZERO_AGGREGATE_OUTPUT.csv")
    profile_input = profile_input_from_controlled(timestamp, controlled_output, zero_aggregate)
    write_csv(PROFILE_INPUT_CSV, profile_input)
    run_command([sys.executable, str(PROFILE_RUNNER), str(PROFILE_INPUT_CSV), str(PROFILE_OUTPUT_CSV)])
    profile_output = parse_csv(PROFILE_OUTPUT_CSV)

    rhoh_input = rhoh_input_from_profile(timestamp, profile_output)
    write_csv(RHOH_INPUT_CSV, rhoh_input)
    run_command([sys.executable, str(RHOH_RUNNER), str(RHOH_INPUT_CSV), str(RHOH_OUTPUT_CSV)])
    rhoh_output = parse_csv(RHOH_OUTPUT_CSV)

    density_input = density_input_from_rhoh(timestamp, rhoh_input, rhoh_output)
    write_csv(DENSITY_INPUT_CSV, density_input)
    run_command([sys.executable, str(DENSITY_RUNNER), str(DENSITY_INPUT_CSV), str(DENSITY_OUTPUT_CSV)])
    density_output = parse_csv(DENSITY_OUTPUT_CSV)

    parent_input = parent_input_from_density(timestamp, density_output)
    write_csv(PARENT_INPUT_CSV, parent_input)
    run_command([sys.executable, str(PARENT_CHARGE_RUNNER), str(PARENT_INPUT_CSV), str(PARENT_OUTPUT_CSV)])
    parent_output = parse_csv(PARENT_OUTPUT_CSV)

    source_input = source_input_from_parent(timestamp, parent_input, parent_output)
    write_csv(SOURCE_INPUT_CSV, source_input)
    run_command([sys.executable, str(SOURCE_RUNNER), str(SOURCE_INPUT_CSV), str(SOURCE_OUTPUT_CSV)])
    source_output = parse_csv(SOURCE_OUTPUT_CSV)

    open_input = open_input_from_source(timestamp, source_output)
    write_csv(OPEN_INPUT_CSV, open_input)
    run_command([sys.executable, str(OPEN_RUNNER), str(OPEN_INPUT_CSV), str(OPEN_OUTPUT_CSV)])
    open_output = parse_csv(OPEN_OUTPUT_CSV)

    score = score_rows(timestamp, profile_output, rhoh_output, density_output, parent_output, source_output, open_output)
    write_csv(SCORE_GATE_CSV, score)

    write_docs(timestamp, law, controlled_output, profile_output, rhoh_output, score, routes)
    append_outputs(timestamp)
    add_claim_once(timestamp)
    append_spine_and_packet(timestamp)
    update_resume(timestamp)

    validation = validate(timestamp, sources, controlled_output, profile_output, rhoh_output, density_output, open_output, gates)
    write_csv(VALIDATION_CSV, validation)

    cache_dir = SCRIPT_DIR / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)


if __name__ == "__main__":
    main()
