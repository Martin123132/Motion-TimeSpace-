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
from Y5_R2FR_4787_physical_Ttotal_profile_row_or_minimal_controlled_source_model import (  # noqa: E402
    CONTROLLED_RUNNER,
    controlled_clauses,
    controlled_row,
    profile_mass_component_from_controlled,
)


CLOSURE_RUNNER = SCRIPT_DIR / "controlled_residual_closure_testbench_runner.py"

CHECKPOINT = "4788"
CLAIM_ID = "L-630"
MARKER = "PPC4161_CLOSE_REQ_BZERO_BOUNDARY_PROJECTOR_DOMAIN_OR_CONTROLLED_SOURCE_TESTBENCH_4788"
PACKET_MARKER = "PPC4161_PACKET_CLOSE_REQ_BZERO_BOUNDARY_PROJECTOR_DOMAIN_OR_CONTROLLED_SOURCE_TESTBENCH_4788"
DECISION = "CONTROLLED_RESIDUAL_CLOSURE_TESTBENCH_INSTALLED_PHYSICAL_SIX_COMPONENTS_STILL_UNSIGNED_PRIVATE_TESTBENCH_ZERO_WORKS_NONCLAIM"
NEXT_TARGET = "4789-Y5-R2FR-derive-Req-Bzero-same-current-identity-or-source-testbench-bound.md"

DOC_PATH = POST / "4788-Y5-R2FR-close-Req-Bzero-boundary-projector-domain-or-controlled-source-testbench.md"
FORMAL_PATH = FORMAL / "804-PPC4161-close-Req-Bzero-boundary-projector-domain-or-controlled-source-testbench.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_SOURCE_REGISTER.csv"
CLOSURE_LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_CONTROLLED_RESIDUAL_CLOSURE_LAW.csv"
CLOSURE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_CONTROLLED_RESIDUAL_CLOSURE_INPUT.csv"
CLOSURE_COMPONENT_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_CONTROLLED_RESIDUAL_CLOSURE_COMPONENT_OUTPUT.csv"
CLOSURE_AGGREGATE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_CONTROLLED_RESIDUAL_CLOSURE_AGGREGATE_OUTPUT.csv"
CONTROLLED_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_CONTROLLED_TTOTAL_INPUT.csv"
CONTROLLED_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_CONTROLLED_TTOTAL_OUTPUT.csv"
PROFILE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_SOURCE_PROFILE_INPUT_FROM_CLOSURE.csv"
PROFILE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_SOURCE_PROFILE_OUTPUT_FROM_CLOSURE.csv"
RHOH_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_RHOH_INPUT_FROM_CLOSURE_PROFILE.csv"
RHOH_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_RHOH_OUTPUT_FROM_CLOSURE_PROFILE.csv"
DENSITY_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_DENSITY_INPUT_FROM_CLOSURE_PROFILE.csv"
DENSITY_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_DENSITY_OUTPUT_FROM_CLOSURE_PROFILE.csv"
PARENT_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_PARENT_CHARGE_INPUT_FROM_CLOSURE_PROFILE.csv"
PARENT_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_PARENT_CHARGE_OUTPUT_FROM_CLOSURE_PROFILE.csv"
SOURCE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_HTAU_HREF_SOURCE_INPUT.csv"
SOURCE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_HTAU_HREF_SOURCE_OUTPUT.csv"
OPEN_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_OPEN_ARENA_INPUT.csv"
OPEN_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_OPEN_ARENA_OUTPUT.csv"
SCORE_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_SCORE_GATE_UPDATE.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_FIREWALL_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_ROUTE_SELECTION_MATRIX.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4788_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4788_VALIDATION.csv"

RESIDUAL_SYMBOLS = (
    "R_eq",
    "B_zero",
    "boundary_flux",
    "open_EM",
    "nonEM_owner_gap",
    "projector_comm",
    "domain_shadow",
    "kappa_drift",
)

ALL_CLOSURE_CLAUSES = (
    "same_parent_branch_signed",
    "controlled_Ttotal_profile_signed",
    "variation_before_readout_signed",
    "same_frame_signed",
    "no_postfit_signed",
    "same_current_identity_signed",
    "Bzero_primitive_signed",
    "compact_test_support_signed",
    "boundary_collar_silent_signed",
    "no_wall_stress_signed",
    "fixed_boundary_data_signed",
    "poynting_once_signed",
    "fixed_EM_hodge_signed",
    "no_radiative_collar_flux_signed",
    "hilbert_only_source_signed",
    "no_spin_torsion_nonhilbert_signed",
    "no_decoupled_source_block_signed",
    "projector_commutes_signed",
    "readout_postprocess_signed",
    "no_source_worldtube_reentry_signed",
    "fixed_domain_signed",
    "qbasic_support_signed",
    "no_birth_death_shell_signed",
    "kappa_lock_signed",
    "source_measure_lock_signed",
    "no_running_kappa_signed",
)

SOURCE_SPECS = [
    ("SRC4788_00_4787_doc", POST / "4787-Y5-R2FR-physical-Ttotal-profile-row-or-minimal-controlled-source-model.md", "six residual components", "4787 selected residual closure target"),
    ("SRC4788_01_4678_tail", SOURCE_DIR / "P8_Y5_R2FR_4678_REQ_BZERO_HTAU_TAIL_CONTRACTS.csv", "TAIL4678_0_R_eq", "R_eq/B_zero tail contracts"),
    ("SRC4788_02_4688_boundary", SOURCE_DIR / "P8_Y5_R2FR_4688_BOUNDARY_NONHILBERT_ZERO_THEOREM.csv", "BNH4688_1_nonHilbert_decomposition", "boundary and non-Hilbert zero theorem"),
    ("SRC4788_03_4687_lhrs", SOURCE_DIR / "P8_Y5_R2FR_4687_LABEL_HODGE_SUPPORT_READOUT_ZERO_THEOREM.csv", "LHRS4687_2_support", "support/readout/projector/domain theorem"),
    ("SRC4788_04_4787_rhoh", SOURCE_DIR / "P8_Y5_R2FR_4787_RHOH_OUTPUT_FROM_CONTROLLED_PROFILE.csv", "controlled_uniform_partial_zero_model", "controlled source partial-zero blocker"),
    ("SRC4788_05_closure_runner", CLOSURE_RUNNER, "def aggregate_closure", "4788 controlled residual closure runner"),
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


def closure_law_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("CRL4788_0_Req", "R_eq=0 requires Pi_M J_H = J_M_top+dB_zero on compact tests", "same-current identity is the first hard algebraic gate"),
        ("CRL4788_1_Bzero", "B_zero=0 requires exact primitive plus collar/boundary silence", "boundary primitive cannot be post-fit"),
        ("CRL4788_2_boundary", "boundary_flux=0 requires no wall stress, fixed boundary data and no normal flux", "prevents hidden source leakage"),
        ("CRL4788_3_nonHilbert", "nonEM_owner_gap=0 requires Hilbert-only source and no spin/torsion/decoupled blocks", "keeps non-Hilbert source channels explicit"),
        ("CRL4788_4_projector_domain", "projector/domain vanish only if readout is postprocessing and W_H is fixed q-basic with no birth shell", "blocks domain/readout masks"),
        ("CRL4788_5_testbench", "if all eight residuals close in one controlled branch, the private testbench opens; physical claim remains false", "separates executable reduction from public evidence"),
    ]
    return [{"checkpoint": CHECKPOINT, "law_id": law_id, "rule": rule, "meaning": meaning, "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp} for law_id, rule, meaning in specs]


def closure_clauses(value: bool) -> dict[str, bool]:
    return {clause: value for clause in ALL_CLOSURE_CLAUSES}


def closure_row(closure_id: str, symbol: str, status: str, source: str, timestamp: str, clauses: dict[str, bool], bound: str = "") -> dict[str, Any]:
    return {
        "closure_id": closure_id,
        "component_symbol": symbol,
        "residual_bound_abs_kg": bound,
        "closure_source": source,
        "bound_source": source,
        "component_source": source,
        "provenance": source,
        "notes": "",
        "row_status": status,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
        **clauses,
    }


def closure_input_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    signed = closure_clauses(True)
    unsigned = closure_clauses(False)
    finite_bound = 0.001 * M_GM_SUN_CAL

    partial_base = closure_clauses(False)
    for clause in ("same_parent_branch_signed", "controlled_Ttotal_profile_signed", "variation_before_readout_signed", "same_frame_signed", "no_postfit_signed"):
        partial_base[clause] = True
    for clause in ("poynting_once_signed", "fixed_EM_hodge_signed", "no_radiative_collar_flux_signed", "kappa_lock_signed", "source_measure_lock_signed", "no_running_kappa_signed"):
        partial_base[clause] = True
    for symbol in RESIDUAL_SYMBOLS:
        rows.append(closure_row("physical_controlled_partial_closure_attempt", symbol, "physical_partial_controlled_closure_nonclaim", "4787_CONTROLLED_SOURCE_PLUS_4786_PARTIAL_ZERO", timestamp, partial_base))

    for symbol in RESIDUAL_SYMBOLS:
        rows.append(closure_row("private_controlled_source_testbench_zero", symbol, "private_controlled_testbench_nonclaim", "PRIVATE_CONTROLLED_SOURCE_TESTBENCH_ALL_CLAUSES_SIGNED", timestamp, signed))

    for symbol in RESIDUAL_SYMBOLS:
        bound = format_float(finite_bound) if symbol in {"R_eq", "B_zero", "boundary_flux", "nonEM_owner_gap", "projector_comm", "domain_shadow"} else "0"
        rows.append(closure_row("finite_controlled_bound_testbench", symbol, "finite_controlled_bound_testbench_nonclaim", "SMOKE_CONTROLLED_RESIDUAL_BOUND_NOT_PHYSICAL", timestamp, unsigned, bound=bound))

    for symbol in RESIDUAL_SYMBOLS:
        rows.append(closure_row("forbidden_postfit_controlled_closure", symbol, "physical_forbidden_postfit_closure_nonclaim", "OBSERVED_RESIDUAL_CANCEL_POSTFIT_REFERENCE_CONTROL", timestamp, signed))

    for symbol in RESIDUAL_SYMBOLS:
        rows.append(closure_row("counterfactual_controlled_testbench_zero", symbol, "counterfactual_smoke_nonclaim", "COUNTERFACTUAL_RUNNER_SMOKE_ONLY", timestamp, signed))

    return rows


def controlled_input_rows(timestamp: str) -> list[dict[str, Any]]:
    signed = controlled_clauses(True)
    return [
        controlled_row("physical_controlled_partial_closure_attempt", "physical_controlled_partial_closure_attempt", "1", "0", "0", "0", "1", "physical_partial_controlled_closure_nonclaim", "CONTROLLED_UNIT_PROFILE_PHYSICAL_CLAUSES_PARTIAL", timestamp, signed),
        controlled_row("private_controlled_source_testbench_zero", "private_controlled_source_testbench_zero", "1", "0", "0", "0", "1", "private_controlled_testbench_nonclaim", "PRIVATE_CONTROLLED_SOURCE_TESTBENCH_PROFILE", timestamp, signed),
        controlled_row("finite_controlled_bound_testbench", "finite_controlled_bound_testbench", "3.0e30", "0", "0", "0", "1", "finite_controlled_bound_testbench_nonclaim", "SMOKE_CONTROLLED_BOUND_PROFILE_NOT_PHYSICAL", timestamp, signed),
        controlled_row("forbidden_postfit_controlled_closure", "forbidden_postfit_controlled_closure", "1", "0", "0", "0", "1", "physical_forbidden_postfit_closure_nonclaim", "OBSERVED_RESIDUAL_CANCEL_POSTFIT_REFERENCE_CONTROL", timestamp, signed),
        controlled_row("counterfactual_controlled_testbench_zero", "counterfactual_controlled_testbench_zero", format_float(M_GM_SUN_CAL), "0", "0", "0", "1", "counterfactual_smoke_nonclaim", "COUNTERFACTUAL_RUNNER_SMOKE_ONLY", timestamp, signed),
    ]


def add_available_residuals(rows: list[dict[str, Any]], profile_id: str, aggregate: dict[str, Any], row_status: str, timestamp: str, source: str) -> None:
    signed = signed_profile_clauses(True)
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
        rows.append(residual_row(profile_id, f"{profile_id}_{field}", field_to_symbol[field], value, row_status, timestamp, source, signed))


def profile_input_from_controlled_and_closure(timestamp: str, controlled_output: list[dict[str, Any]], closure_aggregate: list[dict[str, Any]]) -> list[dict[str, Any]]:
    closure_by_id = {row["closure_id"]: row for row in closure_aggregate}
    rows: list[dict[str, Any]] = []
    for output in controlled_output:
        rows.append(profile_mass_component_from_controlled(output, timestamp))
        closure = closure_by_id[output["profile_id"]]
        add_available_residuals(rows, output["profile_id"], closure, output["row_status_input"], timestamp, "controlled_residual_closure_testbench_runner.py")
    return rows


def simple_rows(timestamp: str, kind: str) -> list[dict[str, Any]]:
    if kind == "gates":
        specs = [
            ("PG4788_0", "R_eq/B_zero require same-current identity plus boundary primitive"),
            ("PG4788_1", "boundary/nonHilbert/projector/domain require their own closure clauses"),
            ("PG4788_2", "partial closure remains blocked even with controlled Ttotal source"),
            ("PG4788_3", "private controlled source testbench may open only as nonclaim"),
            ("PG4788_4", "post-fit residual cancellation fails"),
        ]
        return [{"checkpoint": CHECKPOINT, "gate_id": row_id, "rule": text, "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text in specs]
    if kind == "firewalls":
        specs = [
            ("FW4788_0", "no observed-GM/Gcal residual closure", "ACTIVE"),
            ("FW4788_1", "no branch mixing for residual closure", "ACTIVE"),
            ("FW4788_2", "no public/local-GR claim from private testbench", "LOCAL_PRIVATE_ONLY"),
            ("FW4788_3", "no post-fit boundary or projector cancellation", "ACTIVE"),
        ]
        return [{"checkpoint": CHECKPOINT, "firewall_id": row_id, "firewall_rule": text, "status": status, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text, status in specs]
    if kind == "routes":
        specs = [
            ("RT4788_0_Req_Bzero", "derive R_eq/B_zero same-current identity first", "SELECTED_NEXT"),
            ("RT4788_1_boundary_projector_domain", "then close boundary/projector/domain in the same controlled branch", "SELECTED_NEXT_PARALLEL"),
            ("RT4788_2_testbench", "use private zero testbench only for internal local-GR/Newton pipeline tests", "READY_PRIVATE_NONCLAIM"),
        ]
        return [{"checkpoint": CHECKPOINT, "route_id": row_id, "route": text, "selection_status": status, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text, status in specs]
    raise ValueError(kind)


def write_docs(timestamp: str, law: list[dict[str, Any]], closure_aggregate: list[dict[str, Any]], profile_output: list[dict[str, Any]], rhoh_output: list[dict[str, Any]], score: list[dict[str, Any]], routes: list[dict[str, Any]]) -> None:
    content = f"""# 4788 - Close Req/Bzero/boundary/projector/domain or controlled-source testbench

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4788 installs a controlled residual-closure testbench. The six live residuals are no longer generic:

```text
R_eq=0        needs same-current identity Pi_M J_H = J_M_top + dB_zero
B_zero=0     needs exact boundary primitive and silent collar
boundary=0   needs no wall stress, fixed boundary data and no normal flux
nonHilbert=0 needs Hilbert-only source and no spin/torsion/decoupled source block
projector=0  needs source projector commuting with readout/variation
domain=0     needs fixed q-basic support with no birth/death shell
```

The private controlled source testbench can now traverse the source-mass chain as a nonclaim internal check. The physical branch remains blocked exactly where it should: same-current and boundary/projector/domain clauses are not parent-signed.

## Closure Law

{markdown_table(law, ["law_id", "rule", "meaning"])}

## Closure Aggregate

{markdown_table(closure_aggregate, ["closure_id", "Delta_H_abs_kg", "zero_component_count", "bound_component_count", "missing_component_count", "failed_component_count", "runner_status"])}

## Profile Runner Output

{markdown_table(profile_output, ["profile_id", "rho_H_integral_kg", "Delta_H_abs_kg", "residual_radius_mode", "runner_status"])}

## rhoH Runner Output

{markdown_table(rhoh_output, ["density_id", "rho_H_integral_kg", "H_tau_bulk_kg", "M0_kg", "epsilon_abs", "M_lower_kg", "runner_status"])}

## Chain Score

{markdown_table(score, ["profile_id", "profile_runner_status", "rhoh_runner_status", "density_runner_status", "parent_runner_status", "source_runner_status", "open_runner_status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "selection_status"])}

## Conclusion

This is the first clean private local-source testbench: controlled `T_total(n,n)` plus same-branch residual zero certificate can run through the chain. It is not public evidence. The next derivation target is the hardest pair: `R_eq` and `B_zero`, because they express the same-current/Hamiltonian-Hilbert identity rather than a simple support or EM silence condition.

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, content)

    formal = f"""# PPC4161 4788: Close Req/Bzero/Boundary/Projector/Domain Or Controlled-Source Testbench

Generated: `{timestamp}`

4788 installs the controlled residual-closure testbench runner. It makes the six live residual closures component-specific, opens a private nonclaim controlled source testbench, and keeps the physical branch blocked until same-current, Bzero, boundary, non-Hilbert, projector and domain clauses are parent-signed.

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def append_outputs(timestamp: str) -> None:
    decision = [{"checkpoint": CHECKPOINT, "decision": DECISION, "meaning": "Private controlled testbench opens; physical residual closure still unsigned.", "next_target": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp}]
    status = [{"checkpoint": CHECKPOINT, "status": "PASS_CONTROLLED_RESIDUAL_CLOSURE_TESTBENCH_INSTALLED_NONCLAIM", "summary": "Partial physical closure blocks; private testbench zero and finite bounds compute; forbidden postfit fails.", "valid_for_claim": False, "timestamp_utc": timestamp}]
    next_target = [{"checkpoint": CHECKPOINT, "next_target": NEXT_TARGET, "reason": "R_eq/B_zero same-current identity is the next hardest derivation.", "valid_for_claim": False, "timestamp_utc": timestamp}]
    write_csv(DECISION_CSV, decision)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_target)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "controlled_residual_closure_testbench_runner",
        "4788 installs a controlled residual-closure testbench for R_eq/B_zero/boundary/nonHilbert/projector/domain.",
        "Generated source register, closure law, closure input-output, controlled/profile/rhoH/density/parent/source/open chain outputs, score gates, firewalls, routes, decision, status, next target and validation.",
        "controlled_source_testbench_private_nonclaim",
        NEXT_TARGET,
        "Do not treat private testbench closure as physical local-GR evidence.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need parent-signed same-current R_eq/B_zero identity and same-branch boundary/projector/domain closures.",
        "controlled residual closure testbench",
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

The private controlled source testbench now runs: controlled `T_total(n,n)` plus same-branch zero residual certificate passes the source-mass chain as a nonclaim internal check. The physical branch is still blocked by unsigned same-current and boundary closure clauses, especially `R_eq=0` and `B_zero=0`: `Pi_M J_H = J_M_top+dB_zero`, exact boundary primitive, silent collar, Hilbert-only source, commuting projector and fixed q-basic domain must all be parent-signed in one branch.

## Firewalls

- No GitHub/public action from this checkpoint.
- No observed-GM/Gcal, PPN, clock, R10, or post-fit residual backfill into source or residual rows.
- Private controlled testbench success is not physical/local-GR evidence.
""",
    )


def append_spine_and_packet(timestamp: str) -> None:
    append_once(SPINE_PATH, MARKER, f"\n\n## {MARKER}\n\n4788 installs `controlled_residual_closure_testbench_runner.py`. Controlled source + same-branch residual-zero certificate now forms a private local-source testbench. Physical promotion remains blocked by parent-signing `R_eq/B_zero` same-current identity and boundary/projector/domain clauses. Decision: `{DECISION}`. Next: `{NEXT_TARGET}`.\n")
    append_once(PACKET_PATH, PACKET_MARKER, f"\n\n## {PACKET_MARKER}\n\nRunner: `{CLOSURE_RUNNER}`. Private controlled source testbench opens as nonclaim; physical residual closure remains unsigned. Generated `{timestamp}`.\n")


def validate(timestamp: str, sources: list[dict[str, Any]], closure_aggregate: list[dict[str, Any]], rhoh_output: list[dict[str, Any]], density_output: list[dict[str, Any]], open_output: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks = [
        ("VAL4788_0_sources", "source paths and needles exist", all(row["exists"] is True and row["needle_found"] is True for row in sources), str(SOURCE_REGISTER_CSV)),
        ("VAL4788_1_physical_partial_blocks", "physical partial closure blocks", any(row["closure_id"] == "physical_controlled_partial_closure_attempt" and row["runner_status"] == "CONTROLLED_RESIDUAL_CLOSURE_PARTIAL_BLOCKED" for row in closure_aggregate), str(CLOSURE_AGGREGATE_OUTPUT_CSV)),
        ("VAL4788_2_private_testbench_zero", "private controlled source testbench zero opens", any(row["closure_id"] == "private_controlled_source_testbench_zero" and row["runner_status"] == "CONTROLLED_SOURCE_TESTBENCH_ZERO_PRIVATE_NONCLAIM" for row in closure_aggregate), str(CLOSURE_AGGREGATE_OUTPUT_CSV)),
        ("VAL4788_3_partial_rhoh_blocks", "partial controlled source still blocks rhoH", any(row["density_id"] == "physical_controlled_partial_closure_attempt" and row["runner_status"] == "BLOCKED_MISSING_RHOH_RESIDUAL_RADIUS" for row in rhoh_output), str(RHOH_OUTPUT_CSV)),
        ("VAL4788_4_private_testbench_rhoh", "private testbench computes exact rhoH", any(row["density_id"] == "private_controlled_source_testbench_zero" and row["runner_status"] == "RHOH_SELF_DENOMINATOR_EXACT_PRIVATE_NONCLAIM" for row in rhoh_output), str(RHOH_OUTPUT_CSV)),
        ("VAL4788_5_finite_bound_interval", "finite controlled bound computes interval", any(row["density_id"] == "finite_controlled_bound_testbench" and row["runner_status"] == "RHOH_PARENT_INTEGRAL_INTERVAL_COMPUTED_NONCLAIM" for row in rhoh_output), str(RHOH_OUTPUT_CSV)),
        ("VAL4788_6_forbidden_postfit_fails", "forbidden postfit closure fails", any(row["closure_id"] == "forbidden_postfit_controlled_closure" and row["runner_status"] == "FAILED_CONTROLLED_RESIDUAL_CLOSURE" for row in closure_aggregate), str(CLOSURE_AGGREGATE_OUTPUT_CSV)),
        ("VAL4788_7_counterfactual_open", "counterfactual reaches open runner", any(row["arena_id"] == "counterfactual_controlled_testbench_zero" and row["runner_status"] == "RUNNER_SMOKE_PASS_NONCLAIM" for row in open_output), str(OPEN_OUTPUT_CSV)),
        ("VAL4788_8_gates", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)),
        ("VAL4788_9_claim", "claim row L-630 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)),
        ("VAL4788_10_resume", "resume points to next target", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH)),
    ]
    rows: list[dict[str, Any]] = []
    for validation_id, check, passed, detail in checks:
        rows.append({"checkpoint": CHECKPOINT, "validation_id": validation_id, "check": check, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "timestamp_utc": timestamp})
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"checkpoint": CHECKPOINT, "validation_id": "VAL4788_OVERALL", "check": "all 4788 controlled residual closure testbench checks pass", "status": "PASS" if overall else "FAIL", "detail": DECISION, "valid_for_claim": False, "timestamp_utc": timestamp})
    return rows


def main() -> None:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_register(timestamp)
    law = closure_law_rows(timestamp)
    closure_input = closure_input_rows(timestamp)
    controlled_input = controlled_input_rows(timestamp)
    gates = simple_rows(timestamp, "gates")
    firewalls = simple_rows(timestamp, "firewalls")
    routes = simple_rows(timestamp, "routes")

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(CLOSURE_LAW_CSV, law)
    write_csv(CLOSURE_INPUT_CSV, closure_input)
    write_csv(CONTROLLED_INPUT_CSV, controlled_input)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(ROUTE_MATRIX_CSV, routes)

    run_command([sys.executable, str(CLOSURE_RUNNER), str(CLOSURE_INPUT_CSV), str(CLOSURE_COMPONENT_OUTPUT_CSV), str(CLOSURE_AGGREGATE_OUTPUT_CSV)])
    closure_aggregate = parse_csv(CLOSURE_AGGREGATE_OUTPUT_CSV)

    run_command([sys.executable, str(CONTROLLED_RUNNER), str(CONTROLLED_INPUT_CSV), str(CONTROLLED_OUTPUT_CSV)])
    controlled_output = parse_csv(CONTROLLED_OUTPUT_CSV)

    profile_input = profile_input_from_controlled_and_closure(timestamp, controlled_output, closure_aggregate)
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

    write_docs(timestamp, law, closure_aggregate, profile_output, rhoh_output, score, routes)
    append_outputs(timestamp)
    add_claim_once(timestamp)
    append_spine_and_packet(timestamp)
    update_resume(timestamp)

    validation = validate(timestamp, sources, closure_aggregate, rhoh_output, density_output, open_output, gates)
    write_csv(VALIDATION_CSV, validation)

    cache_dir = SCRIPT_DIR / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)


if __name__ == "__main__":
    main()
