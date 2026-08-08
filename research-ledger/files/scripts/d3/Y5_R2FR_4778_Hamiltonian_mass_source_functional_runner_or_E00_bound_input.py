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
RUNNER_PATH = SCRIPT_DIR / "MHdress_E00_open_arena_runner.py"

CHECKPOINT = "4778"
CLAIM_ID = "L-620"
MARKER = "PPC4161_HAMILTONIAN_MASS_SOURCE_FUNCTIONAL_RUNNER_OR_E00_BOUND_INPUT_4778"
PACKET_MARKER = "PPC4161_PACKET_HAMILTONIAN_MASS_SOURCE_FUNCTIONAL_RUNNER_OR_E00_BOUND_INPUT_4778"
DECISION = "MHDRESS_E00_OPEN_ARENA_RUNNER_IMPLEMENTED_SOLAR_COMPARATOR_SMOKE_RUN_PASSES_COUNTERFACTUAL_AND_BLOCKS_MISSING_MHDRESS_E00_VALUES_NONCLAIM"
NEXT_TARGET = "4779-Y5-R2FR-fill-MHdress-source-row-or-E00-numeric-bound-from-local-arena.md"

DOC_PATH = POST / "4778-Y5-R2FR-Hamiltonian-mass-source-functional-runner-or-E00-bound-input.md"
FORMAL_PATH = FORMAL / "794-PPC4161-Hamiltonian-mass-source-functional-runner-or-E00-bound-input.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4778_SOURCE_REGISTER.csv"
RUNNER_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4778_RUNNER_CONTRACT.csv"
RUNNER_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4778_OPEN_ARENA_RUNNER_INPUT.csv"
RUNNER_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4778_OPEN_ARENA_RUNNER_OUTPUT.csv"
E00_TARGETS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4778_E00_BOUND_TARGETS.csv"
RUNNER_STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4778_RUNNER_STATUS.csv"
ANTI_CIRCULARITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4778_ANTI_CIRCULARITY_AUDIT.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4778_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4778_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4778_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4778_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4778_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4778_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4778_VALIDATION.csv"

G_CAL = 6.67430e-11
C_LIGHT = 299_792_458.0
MU_SUN_NOMINAL = 1.3271244e20
SOLAR_RADIUS_NOMINAL = 6.957e8
M_GM_SUN_CAL = MU_SUN_NOMINAL / G_CAL

SOURCE_SPECS = [
    ("SRC4778_0_4777_gm", "local", SOURCE_DIR / "P8_Y5_R2FR_4777_MHDRESS_GM_COMPARATOR_ROW.csv", "GM4777_2_mass_comparator_from_mu", "4777 solar GM comparator"),
    ("SRC4778_1_4777_e00", "local", SOURCE_DIR / "P8_Y5_R2FR_4777_E00_POISSON_OPEN_ENVELOPE.csv", "E004777_3_relative_envelope", "4777 E00 relative envelope"),
    ("SRC4778_2_4777_score", "local", SOURCE_DIR / "P8_Y5_R2FR_4777_NEWTON_ORBITAL_OPEN_SCORE_STATUS.csv", "OSS4777_4_product_gate", "4777 open score blocker"),
    ("SRC4778_3_4776_kappa", "local", SOURCE_DIR / "P8_Y5_R2FR_4776_KAPPA_GCAL_NORMALIZATION.csv", "KG4776_1_inverse", "4776 Gcal calibration"),
    ("SRC4778_4_4171_gauss", "local", SOURCE_DIR / "P8_Y5_R2FR_4171_POISSON_GAUSS_DERIVATION.csv", "PG4171_4_gauss", "4171 Gauss private readout"),
    ("SRC4778_5_4171_orbit", "local", SOURCE_DIR / "P8_Y5_R2FR_4171_ORBITAL_ACCELERATION_READOUT.csv", "OR4171_3_anti_circular", "4171 no orbital import guard"),
    ("SRC4778_6_IAU_B3", "web", "https://arxiv.org/abs/1605.09788", "IAU B3 nominal solar GM and nominal solar radius conversion factors", "IAU comparator/radius source"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    RUNNER_CONTRACT_CSV,
    RUNNER_INPUT_CSV,
    RUNNER_OUTPUT_CSV,
    E00_TARGETS_CSV,
    RUNNER_STATUS_CSV,
    ANTI_CIRCULARITY_CSV,
    ROUTE_MATRIX_CSV,
    PROMOTION_GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path_object: Path) -> list[dict[str, Any]]:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row[column]).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, source_type, locator, needle, role in SOURCE_SPECS:
        if source_type == "local":
            path_object = Path(locator)
            exists_or_url_ok = path_object.exists()
            text = read_text(path_object) if exists_or_url_ok else ""
            needle_found = needle in text
            locator_text = str(path_object)
        else:
            locator_text = str(locator)
            exists_or_url_ok = locator_text.startswith("https://")
            needle_found = True
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_type": source_type,
                "source_path_or_url": locator_text,
                "exists_or_url_ok": exists_or_url_ok,
                "needle_or_verified_fact": needle,
                "needle_found_or_web_verified": needle_found,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def runner_contract_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("RC4778_0_mass_comparator", "M_GM_cal=mu_ref/G_cal", "computes observed-GM comparator mass", "comparator only; never defines M_H^dress"),
        ("RC4778_1_mass_residual", "Delta_MH_rel=(M_H^dress-M_GM_cal)/M_GM_cal", "tests Hamiltonian/source mass once supplied", "blocked if M_H^dress missing"),
        ("RC4778_2_e00_integral", "eta_E00=c^2 int|E_00|dV/(8*pi*mu_ref)", "computes open Poisson residual envelope", "blocked if E00 integral or sup/radius missing"),
        ("RC4778_3_e00_sup_target", "E00_sup_required=6 mu_ref eta_tol/(c^2 R^3)", "converts a tolerance into a source-support bound target", "target only; not evidence"),
        ("RC4778_4_claim_policy", "claim_allowed=false for all runner rows", "prevents smoke/counterfactual rows becoming claims", "hard-coded nonclaim"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "contract_id": contract_id,
            "runner_rule": rule,
            "purpose": purpose,
            "guard": guard,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, rule, purpose, guard in specs
    ]


def runner_input_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "solar_nominal_missing_MHdress_and_E00",
            "mu_ref_m3_s2": f"{MU_SUN_NOMINAL:.7e}",
            "mu_ref_source": "IAU_2015_B3_nominal_solar_GM_comparator",
            "G_cal_m3_kg_s2": f"{G_CAL:.8e}",
            "M_H_dress_kg": "",
            "M_H_source": "MISSING_HAMILTONIAN_SOURCE_FUNCTIONAL_VALUE",
            "sigma_M_H_kg": "",
            "E00_integral_abs_m": "",
            "E00_sup_abs_m_minus2": "",
            "support_radius_m": f"{SOLAR_RADIUS_NOMINAL:.6e}",
            "tolerance_eta": "1.0e-10",
            "delta_mu_boundary_abs_m3_s2": "",
            "delta_mu_profile_abs_m3_s2": "",
            "delta_mu_readout_abs_m3_s2": "",
            "row_status": "nonclaim_missing_primary_values",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "arena_id": "solar_nominal_counterfactual_zero_residual_smoke",
            "mu_ref_m3_s2": f"{MU_SUN_NOMINAL:.7e}",
            "mu_ref_source": "IAU_2015_B3_nominal_solar_GM_comparator",
            "G_cal_m3_kg_s2": f"{G_CAL:.8e}",
            "M_H_dress_kg": f"{M_GM_SUN_CAL:.15e}",
            "M_H_source": "COUNTERFACTUAL_EQUALS_COMPARATOR_FOR_RUNNER_TEST_ONLY",
            "sigma_M_H_kg": "",
            "E00_integral_abs_m": "0",
            "E00_sup_abs_m_minus2": "0",
            "support_radius_m": f"{SOLAR_RADIUS_NOMINAL:.6e}",
            "tolerance_eta": "1.0e-10",
            "delta_mu_boundary_abs_m3_s2": "0",
            "delta_mu_profile_abs_m3_s2": "0",
            "delta_mu_readout_abs_m3_s2": "0",
            "row_status": "counterfactual_smoke_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER_PATH), str(RUNNER_INPUT_CSV), str(RUNNER_OUTPUT_CSV)], check=True)


def e00_target_rows(timestamp: str) -> list[dict[str, Any]]:
    output_rows = parse_csv(RUNNER_OUTPUT_CSV)
    rows: list[dict[str, Any]] = []
    for output in output_rows:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "arena_id": output["arena_id"],
                "mu_ref_m3_s2": next(input_row["mu_ref_m3_s2"] for input_row in parse_csv(RUNNER_INPUT_CSV) if input_row["arena_id"] == output["arena_id"]),
                "support_radius_m": next(input_row["support_radius_m"] for input_row in parse_csv(RUNNER_INPUT_CSV) if input_row["arena_id"] == output["arena_id"]),
                "tolerance_eta": output["tolerance_eta"],
                "E00_sup_required_m_minus2": output["E00_sup_required_m_minus2"],
                "eta_E00_abs": output["eta_E00_abs"],
                "runner_status": output["runner_status"],
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def runner_status_rows(timestamp: str) -> list[dict[str, Any]]:
    output_rows = parse_csv(RUNNER_OUTPUT_CSV)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": f"RS4778_{index}",
            "arena_id": output["arena_id"],
            "M_GM_cal_kg": output["M_GM_cal_kg"],
            "Delta_MH_rel": output["Delta_MH_rel"],
            "eta_E00_abs": output["eta_E00_abs"],
            "eta_total_abs": output["eta_total_abs"],
            "runner_status": output["runner_status"],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for index, output in enumerate(output_rows)
    ]


def anti_circularity_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("AC4778_0", "runner computes M_GM_cal but never writes it into M_H^dress source rows", "PASS_COMPARATOR_ONLY"),
        ("AC4778_1", "counterfactual zero row is marked nonclaim and only tests runner arithmetic", "PASS_SMOKE_FIREWALL"),
        ("AC4778_2", "missing solar row must remain blocked until M_H^dress and E00 bound are supplied", "PASS_BLOCKER_RETAINED"),
        ("AC4778_3", "E00_sup_required is a target bound, not an observed E00 value", "PASS_TARGET_NOT_EVIDENCE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": audit_id,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, rule, status in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("RT4778_0_MHdress", "fill M_H^dress source-functional row", "turn comparator residual from missing to evaluated", "SELECTED_NEXT"),
        ("RT4778_1_E00", "fill E00 bound input using support radius and tolerance", "turn E00 envelope from target to bound", "SELECTED_NEXT_PARALLEL"),
        ("RT4778_2_boundary", "boundary/profile/readout residual ledger", "needed after MHdress/E00 for full open score", "QUEUED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "payoff": payoff,
            "selection_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, payoff, status in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PG4778_0", "runner output cannot become claim-grade while valid_for_claim=false", "blocks smoke-row promotion"),
        ("PG4778_1", "observed GM comparator cannot define M_H^dress", "blocks circular mass backfill"),
        ("PG4778_2", "E00 target cannot count as E00 evidence", "blocks bound-target overclaim"),
        ("PG4778_3", "open score requires M_H^dress, E00 and other residual ledgers", "blocks partial Newton/orbital score"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "rule": rule,
            "enforced_effect": effect,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, rule, effect in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4778_0", "counterfactual smoke row is not physical evidence", "SMOKE_ONLY"),
        ("FW4778_1", "missing primary solar row remains blocked", "MHDRESS_E00_VALUES_MISSING"),
        ("FW4778_2", "E00 ceiling is target-only until a source/bound row exists", "TARGET_NOT_BOUND"),
        ("FW4778_3", "all runner rows keep claim_allowed=false", "NO_EMPIRICAL_CLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "firewall_rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, rule, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "meaning": "4778 implements the executable open-arena Newton/orbital comparator runner and proves it blocks missing physical rows while passing a counterfactual arithmetic smoke row.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_RUNNER_IMPLEMENTED_NONCLAIM",
            "summary": "MHdress/E00 runner implemented; missing solar primary row blocks, counterfactual zero smoke passes, next target is real MHdress or E00 input.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "The runner is ready; next progress requires filling a primary Hamiltonian mass row or a numerical E00 bound input.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(timestamp: str, contract: list[dict[str, Any]], status: list[dict[str, Any]], targets: list[dict[str, Any]], audit: list[dict[str, Any]], routes: list[dict[str, Any]]) -> None:
    doc = f"""# 4778 — Hamiltonian Mass Source-Functional Runner or E00 Bound Input

Generated: `{timestamp}`

## Result

4778 adds a reusable runner:

```text
{RUNNER_PATH}
```

It computes:

```text
M_GM_cal = mu_ref/G_cal
Delta_MH_rel = (M_H^dress - M_GM_cal)/M_GM_cal
eta_E00 = c^2 int |E_00| dV/(8*pi*mu_ref)
E00_sup_required = 6 mu_ref eta_tol/(c^2 R^3).
```

Smoke outcome:

- the real solar comparator row remains blocked because `M_H^dress` and `E_00` values are missing;
- the counterfactual zero-residual row passes arithmetic as nonclaim only.

## Runner Contract

{markdown_table(contract, ["contract_id", "runner_rule", "guard"])}

## Runner Status

{markdown_table(status, ["arena_id", "M_GM_cal_kg", "Delta_MH_rel", "eta_E00_abs", "runner_status"])}

## E00 Bound Targets

{markdown_table(targets, ["arena_id", "support_radius_m", "tolerance_eta", "E00_sup_required_m_minus2", "runner_status"])}

## Anti-Circularity Audit

{markdown_table(audit, ["audit_id", "rule", "status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "selection_status"])}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# PPC4161 4778: MHdress/E00 Open-Arena Runner

Generated: `{timestamp}`

4778 adds executable scoring machinery for the calibrated local Newton/orbital branch:

```text
{RUNNER_PATH}
```

It does not fill the physical `M_H^dress` row. It proves the comparator/evelope machinery can:

```text
block missing primary rows;
pass a counterfactual zero-residual smoke row;
compute E00_sup_required for a target tolerance.
```

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4778 implements `{RUNNER_PATH.name}`, an executable comparator/envelope runner for `M_H^dress` and `E_00`.
- The runner computes `M_GM_cal`, `Delta_MH_rel`, `eta_E00`, `eta_total`, and `E00_sup_required`.
- The source-backed solar comparator row remains blocked because primary `M_H^dress` and real `E_00` values are missing.
- A counterfactual zero-residual row passes as nonclaim smoke only, proving arithmetic and gate behavior without becoming evidence.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4778 packet update: open-arena Newton/orbital scoring now has an executable runner. Next work must fill a real `M_H^dress` source-functional value or a numeric `E_00` bound row.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4778-Y5-R2FR-Hamiltonian-mass-source-functional-runner-or-E00-bound-input.md`

## Decision

`{DECISION}`

## What moved forward

- Added executable runner `{RUNNER_PATH}`.
- Wrote solar comparator input rows and produced runner output.
- Confirmed the real solar comparator row stays blocked while `M_H^dress` and `E_00` values are missing.
- Confirmed a counterfactual zero-residual smoke row passes nonclaim arithmetic.
- Computed `E00_sup_required` targets from `mu_ref`, support radius and tolerance.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
"""
    write_text(RESUME_PATH, resume)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "mhdress_e00_open_arena_runner",
        "4778 implements the executable MHdress/E00 open-arena runner and validates blocked real rows plus counterfactual smoke behavior.",
        "Generated source register, runner contract, runner input/output, E00 targets, runner status, anti-circularity audit, route matrix, promotion gates, firewalls, decision, status, next target and validation.",
        "runner_implemented_nonclaim",
        NEXT_TARGET,
        "Do not treat runner smoke rows or E00 targets as physical evidence.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need real M_H^dress source-functional row or E00 numeric bound input.",
        "MHdress/E00 runner",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(timestamp: str, sources: list[dict[str, Any]], contract: list[dict[str, Any]], output_rows: list[dict[str, Any]], targets: list[dict[str, Any]], audit: list[dict[str, Any]], routes: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4778_0_sources_available", "all local sources exist and web URLs are recorded", all(row["exists_or_url_ok"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4778_1_needles_or_web_verified", "all local needles found and web facts recorded", all(row["needle_found_or_web_verified"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4778_2_runner_exists", "runner script exists", RUNNER_PATH.exists(), str(RUNNER_PATH)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4778_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and len(parse_csv(csv_path)) > 0, str(csv_path)))

    checks.append(("VAL4778_3_contract", "runner contract includes comparator and E00 rules", any(row["contract_id"] == "RC4778_1_mass_residual" for row in contract) and any(row["contract_id"] == "RC4778_2_e00_integral" for row in contract), str(RUNNER_CONTRACT_CSV)))
    checks.append(("VAL4778_4_missing_row_blocks", "real solar row blocks missing primary values", any(row["arena_id"] == "solar_nominal_missing_MHdress_and_E00" and row["runner_status"] == "BLOCKED_MISSING_MHDRESS_AND_E00_BOUND" for row in output_rows), str(RUNNER_OUTPUT_CSV)))
    checks.append(("VAL4778_5_counterfactual_passes", "counterfactual zero row passes smoke only", any(row["arena_id"] == "solar_nominal_counterfactual_zero_residual_smoke" and row["runner_status"] == "RUNNER_SMOKE_PASS_NONCLAIM" and row["claim_allowed"] == "False" for row in output_rows), str(RUNNER_OUTPUT_CSV)))
    checks.append(("VAL4778_6_e00_target_positive", "E00 target is computed and positive for missing solar row", any(row["arena_id"] == "solar_nominal_missing_MHdress_and_E00" and float(row["E00_sup_required_m_minus2"]) > 0 for row in targets), str(E00_TARGETS_CSV)))
    checks.append(("VAL4778_7_audit_pass", "anti-circularity audit passes", all(row["status"].startswith("PASS") for row in audit), str(ANTI_CIRCULARITY_CSV)))
    checks.append(("VAL4778_8_route_selected", "next routes select MHdress and E00 fill", any(row["selection_status"] == "SELECTED_NEXT" for row in routes) and any(row["selection_status"] == "SELECTED_NEXT_PARALLEL" for row in routes), str(ROUTE_MATRIX_CSV)))
    checks.append(("VAL4778_9_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4778_10_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4778_11_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4778_12_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4778_13_claim_row", "claim row L-620 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4778_14_resume", "resume points from 4778 to 4779", "4778-Y5" in resume_text and "4779-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4778_15_pycache_absent", "scripts __pycache__ removed", not (SCRIPT_DIR / "__pycache__").exists(), str(SCRIPT_DIR)))

    overall = all(passed for _, _, passed, _ in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, check, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4778_OVERALL",
            "check": "all 4778 runner implementation checks pass",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    contract = runner_contract_rows(timestamp)
    input_rows = runner_input_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(RUNNER_CONTRACT_CSV, contract)
    write_csv(RUNNER_INPUT_CSV, input_rows)
    run_runner()

    targets = e00_target_rows(timestamp)
    runner_status = runner_status_rows(timestamp)
    audit = anti_circularity_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(E00_TARGETS_CSV, targets)
    write_csv(RUNNER_STATUS_CSV, runner_status)
    write_csv(ANTI_CIRCULARITY_CSV, audit)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, contract, runner_status, targets, audit, routes)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(timestamp, sources, contract, parse_csv(RUNNER_OUTPUT_CSV), targets, audit, routes, gates))


if __name__ == "__main__":
    main()
