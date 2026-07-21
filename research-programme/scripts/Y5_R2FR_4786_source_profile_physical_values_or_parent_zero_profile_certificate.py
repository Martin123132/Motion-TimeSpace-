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
    G_CAL,
    M_GM_SUN_CAL,
    MU_SUN_NOMINAL,
    OPEN_RUNNER,
    PARENT_CHARGE_RUNNER,
    PROFILE_RUNNER,
    RHOH_RUNNER,
    SOLAR_RADIUS_NOMINAL,
    SOURCE_RUNNER,
    DENSITY_RUNNER,
    RESIDUAL_FIELDS,
    RESIDUAL_SYMBOLS,
    density_input_from_rhoh,
    format_float,
    markdown_table,
    open_input_from_source,
    parent_input_from_density,
    parse_csv,
    profile_mass_row,
    residual_row,
    rhoh_input_from_profile,
    score_rows,
    signed_profile_clauses,
    source_input_from_parent,
    write_csv,
)


ZERO_RUNNER = SCRIPT_DIR / "residual_radius_zero_certificate_runner.py"

CHECKPOINT = "4786"
CLAIM_ID = "L-628"
MARKER = "PPC4161_SOURCE_PROFILE_PHYSICAL_VALUES_OR_PARENT_ZERO_PROFILE_CERTIFICATE_4786"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_PROFILE_PHYSICAL_VALUES_OR_PARENT_ZERO_PROFILE_CERTIFICATE_4786"
DECISION = "RESIDUAL_ZERO_CERTIFICATE_RUNNER_INSTALLED_PARTIAL_ZERO_DOES_NOT_UNLOCK_PROFILE_REAL_PHYSICAL_SOURCE_PROFILE_STILL_MISSING_NONCLAIM"
NEXT_TARGET = "4787-Y5-R2FR-physical-Ttotal-profile-row-or-minimal-controlled-source-model.md"

DOC_PATH = POST / "4786-Y5-R2FR-source-profile-physical-values-or-parent-zero-profile-certificate.md"
FORMAL_PATH = FORMAL / "802-PPC4161-source-profile-physical-values-or-parent-zero-profile-certificate.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_SOURCE_REGISTER.csv"
ZERO_LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_RESIDUAL_ZERO_CERTIFICATE_LAW.csv"
ZERO_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_RESIDUAL_ZERO_INPUT.csv"
ZERO_COMPONENT_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_RESIDUAL_ZERO_COMPONENT_OUTPUT.csv"
ZERO_AGGREGATE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_RESIDUAL_ZERO_AGGREGATE_OUTPUT.csv"
PROFILE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_SOURCE_PROFILE_INPUT_FROM_ZERO.csv"
PROFILE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_SOURCE_PROFILE_OUTPUT_FROM_ZERO.csv"
RHOH_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_RHOH_INPUT_FROM_ZERO_PROFILE.csv"
RHOH_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_RHOH_OUTPUT_FROM_ZERO_PROFILE.csv"
DENSITY_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_DENSITY_INPUT_FROM_ZERO_PROFILE.csv"
DENSITY_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_DENSITY_OUTPUT_FROM_ZERO_PROFILE.csv"
PARENT_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_PARENT_CHARGE_INPUT_FROM_ZERO_PROFILE.csv"
PARENT_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_PARENT_CHARGE_OUTPUT_FROM_ZERO_PROFILE.csv"
SOURCE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_HTAU_HREF_SOURCE_INPUT.csv"
SOURCE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_HTAU_HREF_SOURCE_OUTPUT.csv"
OPEN_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_OPEN_ARENA_INPUT.csv"
OPEN_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_OPEN_ARENA_OUTPUT.csv"
SCORE_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_SCORE_GATE_UPDATE.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_FIREWALL_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_ROUTE_SELECTION_MATRIX.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4786_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4786_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4786_00_4785_doc", POST / "4785-Y5-R2FR-real-source-profile-integral-and-residual-radius-row.md", "try a parent zero-profile certificate", "4785 selected zero-certificate route"),
    ("SRC4786_01_4785_output", SOURCE_DIR / "P8_Y5_R2FR_4785_SOURCE_PROFILE_OUTPUT.csv", "profile_without_residual_radius_control", "4785 residual-radius blocker"),
    ("SRC4786_02_4678_tail", SOURCE_DIR / "P8_Y5_R2FR_4678_REQ_BZERO_HTAU_TAIL_CONTRACTS.csv", "TAIL4678_0_R_eq", "R_eq and B_zero tail contracts"),
    ("SRC4786_03_4677_em", SOURCE_DIR / "P8_Y5_R2FR_4677_FIXED_EM_ZERO_INTO_SOURCE_WEIGHT_VECTOR.csv", "ZERO4677_2_poynting_extra_source", "fixed EM/Poynting zero precedent"),
    ("SRC4786_04_4687_lhrs", SOURCE_DIR / "P8_Y5_R2FR_4687_LABEL_HODGE_SUPPORT_READOUT_ZERO_THEOREM.csv", "LHRS4687_2_support", "support/readout/domain zero theorem"),
    ("SRC4786_05_4688_boundary", SOURCE_DIR / "P8_Y5_R2FR_4688_BOUNDARY_NONHILBERT_ZERO_THEOREM.csv", "BNH4688_0_boundary_variation", "boundary/non-Hilbert zero theorem"),
    ("SRC4786_06_4654_kappa", SOURCE_DIR / "P8_Y5_R2FR_4654_DELTAKAPPA_ZERO_THEOREM.csv", "DKZ4654_3_result", "kappa drift private zero theorem"),
    ("SRC4786_07_zero_runner", ZERO_RUNNER, "def aggregate_certificate", "4786 residual zero certificate runner"),
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


def zero_law_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ZPL4786_0_same_branch", "all zero components must live in the same parent/source-profile branch", "prevents mixing private EM zero with unrelated boundary assumptions"),
        ("ZPL4786_1_exact_or_bound", "each residual component is either zero-certified, numerically bounded, or explicitly missing", "no silent closure of the residual radius"),
        ("ZPL4786_2_partial_blocks", "a partial zero certificate does not unlock rho_H/M_lower", "profile integral plus missing residual components still blocks"),
        ("ZPL4786_3_openEM_kappa", "fixed EM/Poynting and private kappa drift can zero their own components only inside their signed branch", "keeps useful partial progress without overclaiming"),
        ("ZPL4786_4_firewall", "post-fit residual cancellation cannot be used as a zero certificate", "blocks fitted-GM/readout laundering"),
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


def signed_zero_clauses(value: bool) -> dict[str, bool]:
    return {
        "same_parent_branch_signed": value,
        "parent_action_signed": value,
        "same_frame_signed": value,
        "qbasic_support_signed": value,
        "boundary_silent_signed": value,
        "poynting_accounted_signed": value,
        "readout_postprocess_signed": value,
        "no_species_prefactor_signed": value,
        "no_postfit_signed": value,
        "component_specific_zero_signed": value,
    }


def zero_input_row(certificate_id: str, component_symbol: str, zero_anchor: str, bound: str, status: str, source: str, timestamp: str, clauses: dict[str, bool]) -> dict[str, Any]:
    return {
        "certificate_id": certificate_id,
        "component_symbol": component_symbol,
        "zero_anchor_abs_kg": zero_anchor,
        "residual_bound_abs_kg": bound,
        "zero_source": source,
        "bound_source": source,
        "component_source": source,
        "provenance": source,
        "notes": "",
        "row_status": status,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
        **clauses,
    }


def zero_input_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    signed = signed_zero_clauses(True)
    unsigned = signed_zero_clauses(False)
    finite_component = 0.0025 * M_GM_SUN_CAL

    partial_zero_sources = {
        "open_EM": "P8_Y5_R2FR_4677_FIXED_EM_ZERO_INTO_SOURCE_WEIGHT_VECTOR.csv",
        "kappa_drift": "P8_Y5_R2FR_4654_DELTAKAPPA_ZERO_THEOREM.csv",
    }
    for symbol in RESIDUAL_SYMBOLS:
        if symbol in partial_zero_sources:
            rows.append(zero_input_row("physical_partial_parent_zero_attempt", symbol, "0", "", "physical_partial_zero_nonclaim", partial_zero_sources[symbol], timestamp, signed))
        else:
            rows.append(zero_input_row("physical_partial_parent_zero_attempt", symbol, "", "", "physical_partial_zero_nonclaim", "MISSING_PARENT_ZERO_OR_BOUND_FOR_" + symbol, timestamp, unsigned))

    for symbol in RESIDUAL_SYMBOLS:
        rows.append(zero_input_row("private_full_zero_certificate_control", symbol, "0", "", "private_full_zero_certificate_nonclaim", "PRIVATE_SAME_BRANCH_ZERO_CERTIFICATE_CONTROL", timestamp, signed))

    for symbol in RESIDUAL_SYMBOLS:
        value = format_float(finite_component) if symbol in {"R_eq", "boundary_flux"} else "0"
        rows.append(zero_input_row("finite_residual_bound_smoke_nonclaim", symbol, "", value, "finite_residual_bound_smoke_nonclaim", "SMOKE_RESIDUAL_BOUND_NOT_PHYSICAL", timestamp, unsigned))

    for symbol in RESIDUAL_SYMBOLS:
        rows.append(zero_input_row("forbidden_postfit_zero_control", symbol, "0", "", "physical_forbidden_postfit_zero_control_nonclaim", "OBSERVED_RESIDUAL_CANCEL_POSTFIT_REFERENCE_CONTROL", timestamp, signed))

    for symbol in RESIDUAL_SYMBOLS:
        rows.append(zero_input_row("counterfactual_full_zero_certificate", symbol, "0", "", "counterfactual_smoke_nonclaim", "COUNTERFACTUAL_RUNNER_SMOKE_ONLY", timestamp, signed))

    return rows


def add_available_residuals(rows: list[dict[str, Any]], profile_id: str, aggregate: dict[str, Any], row_status: str, timestamp: str, source: str, clauses: dict[str, bool]) -> None:
    field_to_symbol = dict(zip(RESIDUAL_FIELDS, RESIDUAL_SYMBOLS))
    for field, symbol in field_to_symbol.items():
        value = aggregate.get(field, "MISSING_NUMERIC_VALUE")
        if str(value).startswith("MISSING"):
            continue
        rows.append(residual_row(profile_id, f"{profile_id}_{symbol}", symbol, value, row_status, timestamp, source, clauses))


def profile_input_from_zero(timestamp: str, zero_aggregate: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {row["certificate_id"]: row for row in zero_aggregate}
    rows: list[dict[str, Any]] = []
    signed = signed_profile_clauses(True)
    unsigned = signed_profile_clauses(False)

    partial = by_id["physical_partial_parent_zero_attempt"]
    rows.append(profile_mass_row("physical_profile_values_missing_partial_zero_certificate", "missing_mass", "", "physical_values_missing_partial_zero_nonclaim", timestamp, "MISSING_PARENT_TTOTAL_PROFILE", unsigned))
    add_available_residuals(rows, "physical_profile_values_missing_partial_zero_certificate", partial, "physical_values_missing_partial_zero_nonclaim", timestamp, "partial_zero_certificate_4786", signed)

    rows.append(profile_mass_row("profile_with_partial_zero_mass_smoke_nonclaim", "partial_mass_smoke", "1", "partial_zero_mass_smoke_nonclaim", timestamp, "SMOKE_MASS_WITH_PARTIAL_ZERO", signed))
    add_available_residuals(rows, "profile_with_partial_zero_mass_smoke_nonclaim", partial, "partial_zero_mass_smoke_nonclaim", timestamp, "partial_zero_certificate_4786", signed)

    private_full = by_id["private_full_zero_certificate_control"]
    rows.append(profile_mass_row("private_unit_profile_parent_zero_certificate", "private_mass", "1", "private_zero_profile_certificate_nonclaim", timestamp, "PRIVATE_UNIT_PROFILE_WITH_ZERO_CERTIFICATE", signed))
    add_available_residuals(rows, "private_unit_profile_parent_zero_certificate", private_full, "private_zero_profile_certificate_nonclaim", timestamp, "private_full_zero_certificate_4786", signed)

    finite = by_id["finite_residual_bound_smoke_nonclaim"]
    rows.append(profile_mass_row("finite_bound_profile_from_certificate_smoke", "finite_mass", format_float(M_GM_SUN_CAL), "finite_residual_bound_profile_smoke_nonclaim", timestamp, "SMOKE_PROFILE_NOT_PHYSICAL", signed))
    add_available_residuals(rows, "finite_bound_profile_from_certificate_smoke", finite, "finite_residual_bound_profile_smoke_nonclaim", timestamp, "finite_residual_bound_certificate_4786", signed)

    forbidden = by_id["forbidden_postfit_zero_control"]
    rows.append(profile_mass_row("forbidden_postfit_zero_profile_control", "forbidden_mass", "1", "physical_forbidden_postfit_zero_control_nonclaim", timestamp, "OBSERVED_RESIDUAL_CANCEL_POSTFIT_REFERENCE_CONTROL", signed))
    add_available_residuals(rows, "forbidden_postfit_zero_profile_control", forbidden, "physical_forbidden_postfit_zero_control_nonclaim", timestamp, "OBSERVED_RESIDUAL_CANCEL_POSTFIT_REFERENCE_CONTROL", signed)

    counterfactual = by_id["counterfactual_full_zero_certificate"]
    rows.append(profile_mass_row("counterfactual_profile_zero_certificate", "counterfactual_mass", format_float(M_GM_SUN_CAL), "counterfactual_smoke_nonclaim", timestamp, "COUNTERFACTUAL_RUNNER_SMOKE_ONLY", signed))
    add_available_residuals(rows, "counterfactual_profile_zero_certificate", counterfactual, "counterfactual_smoke_nonclaim", timestamp, "COUNTERFACTUAL_RUNNER_SMOKE_ONLY", signed)

    return rows


def simple_rows(timestamp: str, kind: str) -> list[dict[str, Any]]:
    if kind == "gates":
        specs = [
            ("PG4786_0", "all eight residual components must be zero/bound in one branch"),
            ("PG4786_1", "partial zero certificate cannot unlock rhoH/Mlower"),
            ("PG4786_2", "private full zero certificate is nonclaim control only"),
            ("PG4786_3", "post-fit residual cancellation fails"),
            ("PG4786_4", "physical source profile values remain independent of residual zero certificate"),
        ]
        return [{"checkpoint": CHECKPOINT, "gate_id": row_id, "rule": text, "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text in specs]
    if kind == "firewalls":
        specs = [
            ("FW4786_0", "no observed-GM/Gcal residual zero source", "ACTIVE"),
            ("FW4786_1", "no post-fit reference cancellation", "ACTIVE"),
            ("FW4786_2", "no mixing zero clauses from different branches as a claim", "ACTIVE"),
            ("FW4786_3", "no GitHub/public action", "LOCAL_PRIVATE_ONLY"),
        ]
        return [{"checkpoint": CHECKPOINT, "firewall_id": row_id, "firewall_rule": text, "status": status, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text, status in specs]
    if kind == "routes":
        specs = [
            ("RT4786_0_physical_profile", "fill a controlled physical T_total(n,n) profile row", "SELECTED_NEXT"),
            ("RT4786_1_complete_zero", "try to close R_eq/B_zero/boundary/nonEM/projector/domain residual zeros in the same branch", "SELECTED_NEXT_PARALLEL"),
            ("RT4786_2_numeric_bounds", "if zeros fail, source numerical bounds for the missing residual components", "SELECTED_NEXT_PARALLEL"),
        ]
        return [{"checkpoint": CHECKPOINT, "route_id": row_id, "route": text, "selection_status": status, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text, status in specs]
    raise ValueError(kind)


def write_docs(timestamp: str, law: list[dict[str, Any]], zero_aggregate: list[dict[str, Any]], profile_output: list[dict[str, Any]], rhoh_output: list[dict[str, Any]], score: list[dict[str, Any]], routes: list[dict[str, Any]]) -> None:
    content = f"""# 4786 - Source-profile physical values or parent zero-profile certificate

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4786 tries the zero-certificate path before demanding new data. Each residual component must be independently zero-certified or bounded:

```text
Delta_H_abs = |R_eq|+|B_zero|+|boundary_flux|+|open_EM|
            + |nonEM_owner_gap|+|projector_comm|+|domain_shadow|+|kappa_drift|.
```

Partial success is retained but does not unlock the chain. In the current physical attempt, fixed-EM/open-EM and kappa drift can be routed to existing private/conditional zero packets, but `R_eq`, `B_zero`, boundary, non-Hilbert owner gap, projector and domain components remain unclosed in the same parent branch.

## Zero-Certificate Law

{markdown_table(law, ["law_id", "rule", "meaning"])}

## Residual Zero Aggregate

{markdown_table(zero_aggregate, ["certificate_id", "Delta_H_abs_kg", "zero_component_count", "bound_component_count", "missing_component_count", "failed_component_count", "runner_status"])}

## Profile Runner Output

{markdown_table(profile_output, ["profile_id", "rho_H_integral_kg", "Delta_H_abs_kg", "residual_radius_mode", "runner_status"])}

## rhoH Runner Output

{markdown_table(rhoh_output, ["density_id", "rho_H_integral_kg", "H_tau_bulk_kg", "M0_kg", "epsilon_abs", "M_lower_kg", "runner_status"])}

## Chain Score

{markdown_table(score, ["profile_id", "profile_runner_status", "rhoh_runner_status", "density_runner_status", "parent_runner_status", "source_runner_status", "open_runner_status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "selection_status"])}

## Conclusion

The branch did move: residual closure is now component-wise executable, and partial zero results cannot masquerade as a full local-GR source certificate. The next best target is a controlled physical `T_total(n,n)` profile row, while continuing to attack the unclosed residual components.

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, content)

    formal = f"""# PPC4161 4786: Source-Profile Physical Values Or Parent Zero-Profile Certificate

Generated: `{timestamp}`

4786 installs the residual-radius zero-certificate runner. It allows component-wise zero or bound rows, rejects post-fit residual cancellation, and proves that partial residual zero certificates still block `rho_H/M_lower`.

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def append_outputs(timestamp: str) -> None:
    decision = [{"checkpoint": CHECKPOINT, "decision": DECISION, "meaning": "Component-wise residual zero certificates are executable; partial zero does not unlock local source mass.", "next_target": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp}]
    status = [{"checkpoint": CHECKPOINT, "status": "PASS_RESIDUAL_ZERO_CERTIFICATE_RUNNER_INSTALLED_NONCLAIM", "summary": "Partial physical zero stays blocked; private/counterfactual full zero controls pass.", "valid_for_claim": False, "timestamp_utc": timestamp}]
    next_target = [{"checkpoint": CHECKPOINT, "next_target": NEXT_TARGET, "reason": "Need controlled physical Ttotal/rhoH profile values and remaining residual zeros/bounds.", "valid_for_claim": False, "timestamp_utc": timestamp}]
    write_csv(DECISION_CSV, decision)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_target)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "residual_radius_zero_certificate_runner",
        "4786 installs a component-wise residual zero/bound certificate runner and proves partial zero certificates do not unlock rhoH/Mlower.",
        "Generated source register, zero law, zero input-output, profile/rhoH/density/parent/source/open chain outputs, score gates, firewalls, routes, decision, status, next target and validation.",
        "residual_zero_certificate_private_nonclaim",
        NEXT_TARGET,
        "Do not treat partial zero or private full-zero controls as local-GR evidence.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need real physical T_total(n,n) source profile values plus same-branch residual zeros or bounds.",
        "residual-radius zero certificate",
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

The source-profile/residual-radius gate is now component-wise executable. Partial zero evidence exists for the fixed-EM/open-EM and private kappa-drift pieces, but the physical branch still lacks a real parent/source-backed `T_total(n,n)` or `rho_H` profile row and same-branch closure/bounds for `R_eq`, `B_zero`, boundary flux, non-Hilbert owner gap, projector commutator and domain shadow.

## Firewalls

- No GitHub/public action from this checkpoint.
- No observed-GM/Gcal, PPN, clock, R10, or post-fit residual backfill into source or residual rows.
- No branch-mixing: partial private zero packets cannot be treated as a full physical local-GR certificate.
""",
    )


def append_spine_and_packet(timestamp: str) -> None:
    append_once(SPINE_PATH, MARKER, f"\n\n## {MARKER}\n\n4786 installs `residual_radius_zero_certificate_runner.py`. It makes the residual-radius certificate component-wise and executable. Partial zero evidence is retained but does not unlock `rho_H/M_lower`; the physical branch still needs a real `T_total(n,n)` profile and same-branch closure/bounds for the unclosed residual components. Decision: `{DECISION}`. Next: `{NEXT_TARGET}`.\n")
    append_once(PACKET_PATH, PACKET_MARKER, f"\n\n## {PACKET_MARKER}\n\nRunner: `{ZERO_RUNNER}`. Partial zero certificates block as intended; private/counterfactual controls pass only as nonclaim. Generated `{timestamp}`.\n")


def validate(timestamp: str, sources: list[dict[str, Any]], zero_aggregate: list[dict[str, Any]], profile_output: list[dict[str, Any]], rhoh_output: list[dict[str, Any]], density_output: list[dict[str, Any]], open_output: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks = [
        ("VAL4786_0_sources", "source paths and needles exist", all(row["exists"] is True and row["needle_found"] is True for row in sources), str(SOURCE_REGISTER_CSV)),
        ("VAL4786_1_partial_zero_blocks", "physical partial zero certificate blocks", any(row["certificate_id"] == "physical_partial_parent_zero_attempt" and row["runner_status"] == "RESIDUAL_ZERO_CERTIFICATE_PARTIAL_BLOCKED" and "R_eq_abs_kg" in row["missing_components"] for row in zero_aggregate), str(ZERO_AGGREGATE_OUTPUT_CSV)),
        ("VAL4786_2_private_full_zero", "private full zero certificate passes nonclaim", any(row["certificate_id"] == "private_full_zero_certificate_control" and row["runner_status"] == "RESIDUAL_ZERO_CERTIFICATE_PRIVATE_NONCLAIM" for row in zero_aggregate), str(ZERO_AGGREGATE_OUTPUT_CSV)),
        ("VAL4786_3_partial_profile_blocks_downstream", "mass smoke with partial zero blocks rhoH radius", any(row["density_id"] == "profile_with_partial_zero_mass_smoke_nonclaim" and row["runner_status"] == "BLOCKED_MISSING_RHOH_RESIDUAL_RADIUS" for row in rhoh_output), str(RHOH_OUTPUT_CSV)),
        ("VAL4786_4_private_profile_zero", "private profile zero certificate computes", any(row["profile_id"] == "private_unit_profile_parent_zero_certificate" and row["runner_status"] == "PROFILE_INTEGRAL_AND_RADIUS_EXACT_PRIVATE_NONCLAIM" for row in profile_output), str(PROFILE_OUTPUT_CSV)),
        ("VAL4786_5_forbidden_postfit_fails", "forbidden postfit zero control fails", any(row["certificate_id"] == "forbidden_postfit_zero_control" and row["runner_status"] == "FAILED_RESIDUAL_ZERO_CERTIFICATE" for row in zero_aggregate), str(ZERO_AGGREGATE_OUTPUT_CSV)),
        ("VAL4786_6_counterfactual_density", "counterfactual reaches density runner", any(row["density_id"] == "counterfactual_profile_zero_certificate" and row["runner_status"] == "DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM" for row in density_output), str(DENSITY_OUTPUT_CSV)),
        ("VAL4786_7_open_counterfactual", "counterfactual reaches open runner", any(row["arena_id"] == "counterfactual_profile_zero_certificate" and row["runner_status"] == "RUNNER_SMOKE_PASS_NONCLAIM" for row in open_output), str(OPEN_OUTPUT_CSV)),
        ("VAL4786_8_gates", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)),
        ("VAL4786_9_claim", "claim row L-628 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)),
        ("VAL4786_10_resume", "resume points to next target", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH)),
    ]
    rows: list[dict[str, Any]] = []
    for validation_id, check, passed, detail in checks:
        rows.append({"checkpoint": CHECKPOINT, "validation_id": validation_id, "check": check, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "timestamp_utc": timestamp})
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"checkpoint": CHECKPOINT, "validation_id": "VAL4786_OVERALL", "check": "all 4786 residual zero certificate checks pass", "status": "PASS" if overall else "FAIL", "detail": DECISION, "valid_for_claim": False, "timestamp_utc": timestamp})
    return rows


def main() -> None:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_register(timestamp)
    law = zero_law_rows(timestamp)
    zero_input = zero_input_rows(timestamp)
    gates = simple_rows(timestamp, "gates")
    firewalls = simple_rows(timestamp, "firewalls")
    routes = simple_rows(timestamp, "routes")

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(ZERO_LAW_CSV, law)
    write_csv(ZERO_INPUT_CSV, zero_input)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(ROUTE_MATRIX_CSV, routes)

    run_command([sys.executable, str(ZERO_RUNNER), str(ZERO_INPUT_CSV), str(ZERO_COMPONENT_OUTPUT_CSV), str(ZERO_AGGREGATE_OUTPUT_CSV)])
    zero_aggregate = parse_csv(ZERO_AGGREGATE_OUTPUT_CSV)

    profile_input = profile_input_from_zero(timestamp, zero_aggregate)
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

    write_docs(timestamp, law, zero_aggregate, profile_output, rhoh_output, score, routes)
    append_outputs(timestamp)
    add_claim_once(timestamp)
    append_spine_and_packet(timestamp)
    update_resume(timestamp)

    validation = validate(timestamp, sources, zero_aggregate, profile_output, rhoh_output, density_output, open_output, gates)
    write_csv(VALIDATION_CSV, validation)

    cache_dir = SCRIPT_DIR / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)


if __name__ == "__main__":
    main()
