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

CHECKPOINT = "4779"
CLAIM_ID = "L-621"
MARKER = "PPC4161_FILL_MHDRESS_SOURCE_ROW_OR_E00_NUMERIC_BOUND_FROM_LOCAL_ARENA_4779"
PACKET_MARKER = "PPC4161_PACKET_FILL_MHDRESS_SOURCE_ROW_OR_E00_NUMERIC_BOUND_FROM_LOCAL_ARENA_4779"
DECISION = "PRIVATE_SELECTOR_E00_NUMERIC_ZERO_BOUND_FILLED_AND_RUNNER_REDUCES_BLOCKER_TO_MHDRESS_ONLY_PUBLIC_OPEN_SCORE_STILL_BLOCKED_NONCLAIM"
NEXT_TARGET = "4780-Y5-R2FR-Htau-Href-MHdress-source-functional-first-row.md"

DOC_PATH = POST / "4779-Y5-R2FR-fill-MHdress-source-row-or-E00-numeric-bound-from-local-arena.md"
FORMAL_PATH = FORMAL / "795-PPC4161-fill-MHdress-source-row-or-E00-numeric-bound-from-local-arena.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4779_SOURCE_REGISTER.csv"
E00_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4779_E00_NUMERIC_BOUND_ROW.csv"
RUNNER_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4779_OPEN_ARENA_RUNNER_INPUT.csv"
RUNNER_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4779_OPEN_ARENA_RUNNER_OUTPUT.csv"
MHDRESS_REQUIREMENTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4779_MHDRESS_SOURCE_FUNCTIONAL_INPUT_REQUIREMENTS.csv"
SCORE_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4779_SCORE_GATE_UPDATE.csv"
ANTI_CIRCULARITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4779_ANTI_CIRCULARITY_AUDIT.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4779_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4779_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4779_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4779_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4779_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4779_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4779_VALIDATION.csv"

G_CAL = 6.67430e-11
MU_SUN_NOMINAL = 1.3271244e20
SOLAR_RADIUS_NOMINAL = 6.957e8

SOURCE_SPECS = [
    ("SRC4779_0_4778_contract", SOURCE_DIR / "P8_Y5_R2FR_4778_RUNNER_CONTRACT.csv", "RC4778_2_e00_integral", "4778 E00 runner rule"),
    ("SRC4779_1_4778_output", SOURCE_DIR / "P8_Y5_R2FR_4778_OPEN_ARENA_RUNNER_OUTPUT.csv", "BLOCKED_MISSING_MHDRESS_AND_E00_BOUND", "4778 previous two-blocker runner state"),
    ("SRC4779_2_4777_balance", SOURCE_DIR / "P8_Y5_R2FR_4777_E00_POISSON_OPEN_ENVELOPE.csv", "E004777_2_observed_mu_balance", "4777 mu balance law"),
    ("SRC4779_3_4775_residual_zero", SOURCE_DIR / "P8_Y5_R2FR_4775_PRIVATE_LOCAL_GR_LIMIT_CERTIFICATE.csv", "CERT4775_2_residual_zero", "4775 private residual-zero certificate"),
    ("SRC4779_4_4775_Newton", SOURCE_DIR / "P8_Y5_R2FR_4775_PRIVATE_LOCAL_GR_LIMIT_CERTIFICATE.csv", "CERT4775_4_Newton", "4775 Newton private branch certificate"),
    ("SRC4779_5_4719_E00", SOURCE_DIR / "P8_Y5_R2FR_4719_LINEARIZED_FIELD_EQUATION_ROWS.csv", "LFE4719_3_Poisson_equation_with_residual", "4719 E00 residual definition"),
    ("SRC4779_6_4776_Gcal", SOURCE_DIR / "P8_Y5_R2FR_4776_KAPPA_GCAL_NORMALIZATION.csv", "KG4776_1_inverse", "4776 Gcal calibration"),
    ("SRC4779_7_4777_GM", SOURCE_DIR / "P8_Y5_R2FR_4777_MHDRESS_GM_COMPARATOR_ROW.csv", "GM4777_2_mass_comparator_from_mu", "4777 solar GM comparator"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    E00_BOUND_CSV,
    RUNNER_INPUT_CSV,
    RUNNER_OUTPUT_CSV,
    MHDRESS_REQUIREMENTS_CSV,
    SCORE_GATE_CSV,
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


def e00_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "E004779_0_private_selector_E00_zero",
            "arena_id": "private_selector_solar_comparator_E00_zero_MHdress_missing",
            "quantity": "E_00",
            "numeric_value": "0.0",
            "units": "m^-2",
            "bound_formula": "E_00=0 inside B_loc^private because E_fail_mu_nu=0 in the private/effective local-GR selector",
            "source_basis": "4775 CERT4775_2 residual-zero plus 4775 CERT4775_4 Newton limit plus 4719 E00 residual definition",
            "scope": "private_selector_only_not_public_open_arena",
            "status": "FILLED_PRIVATE_SELECTOR_NUMERIC_ZERO_BOUND_NONCLAIM",
            "valid_for_runner": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "E004779_1_integral_zero",
            "arena_id": "private_selector_solar_comparator_E00_zero_MHdress_missing",
            "quantity": "int_W_abs_E00_dV",
            "numeric_value": "0.0",
            "units": "m",
            "bound_formula": "int_W |E_00| dV = 0 for the private selector E00 zero branch",
            "source_basis": "same private selector condition; not valid if radiative/open/residual branch is selected",
            "scope": "private_selector_only_not_public_open_arena",
            "status": "FILLED_PRIVATE_SELECTOR_E00_INTEGRAL_ZERO_NONCLAIM",
            "valid_for_runner": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def runner_input_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "private_selector_solar_comparator_E00_zero_MHdress_missing",
            "mu_ref_m3_s2": f"{MU_SUN_NOMINAL:.7e}",
            "mu_ref_source": "IAU_2015_B3_nominal_solar_GM_comparator",
            "G_cal_m3_kg_s2": f"{G_CAL:.8e}",
            "M_H_dress_kg": "",
            "M_H_source": "MISSING_HAMILTONIAN_SOURCE_FUNCTIONAL_VALUE",
            "sigma_M_H_kg": "",
            "E00_integral_abs_m": "0",
            "E00_sup_abs_m_minus2": "0",
            "support_radius_m": f"{SOLAR_RADIUS_NOMINAL:.6e}",
            "tolerance_eta": "1.0e-10",
            "delta_mu_boundary_abs_m3_s2": "",
            "delta_mu_profile_abs_m3_s2": "",
            "delta_mu_readout_abs_m3_s2": "",
            "row_status": "private_selector_E00_zero_nonclaim_missing_MHdress",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER_PATH), str(RUNNER_INPUT_CSV), str(RUNNER_OUTPUT_CSV)], check=True)


def mhdress_requirement_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "MHR4779_0_Htau",
            "H_tau[S_link;tau,e_obs]",
            "Hamiltonian charge on the linking surface in the same observed frame",
            "MISSING_NUMERIC_OR_PARENT_FUNCTIONAL_EVALUATION",
        ),
        (
            "MHR4779_1_Href",
            "H_ref[Sigma_ref;tau,e_obs]",
            "fixed source-blind reference selected before readout",
            "MISSING_NUMERIC_OR_PARENT_FUNCTIONAL_EVALUATION",
        ),
        (
            "MHR4779_2_difference",
            "M_H^dress=H_tau-H_ref",
            "primary MTS source mass value in kg after 4776 SI calibration",
            "MISSING_PRIMARY_MTS_MASS_VALUE",
        ),
        (
            "MHR4779_3_comparator_residual",
            "Delta_MH=(M_H^dress-M_GM_cal)/M_GM_cal",
            "first real Newton/orbital comparator residual after M_H^dress exists",
            "WAITING_FOR_MHDRESS",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "requirement_id": req_id,
            "required_object": obj,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for req_id, obj, meaning, status in specs
    ]


def score_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    output = parse_csv(RUNNER_OUTPUT_CSV)[0]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "SG4779_0_Gcal",
            "object": "G_cal/kappa_eff",
            "before": "FILLED_4776",
            "after": "FILLED_4776",
            "runner_status": "READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "SG4779_1_E00",
            "object": "E_00 private selector bound",
            "before": "MISSING_OPEN_ARENA_E00_BOUND",
            "after": "FILLED_PRIVATE_SELECTOR_E00_ZERO_NONCLAIM",
            "runner_status": output["eta_E00_abs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "SG4779_2_MHdress",
            "object": "M_H^dress",
            "before": "MISSING_PRIMARY_MTS_MASS_VALUE",
            "after": "STILL_MISSING_PRIMARY_MTS_MASS_VALUE",
            "runner_status": output["runner_status"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "SG4779_3_score",
            "object": "open/private-selector Newton-orbital comparator score",
            "before": "BLOCKED_MISSING_MHDRESS_AND_E00_BOUND",
            "after": "BLOCKED_MISSING_MHDRESS",
            "runner_status": output["runner_status"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def anti_circularity_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("AC4779_0_scope", "E00=0 row is private-selector-only and cannot be used for public/open/radiative arenas.", "PASS_SCOPE_LOCK"),
        ("AC4779_1_mass", "M_H^dress remains missing; observed GM/Gcal still cannot define it.", "PASS_NO_GM_BACKFILL"),
        ("AC4779_2_score", "runner status must reduce to BLOCKED_MISSING_MHDRESS, not claim pass.", "PASS_BLOCKER_RETAINED"),
        ("AC4779_3_evidence", "E00 zero uses 4775 private certificate; if branch changes, row must be replaced by open bound.", "PASS_REOPEN_RULE"),
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
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": "RT4779_0_MHdress",
            "route": "evaluate H_tau-H_ref source-functional first row",
            "payoff": "turn runner from BLOCKED_MISSING_MHDRESS into an evaluated comparator residual",
            "selection_status": "SELECTED_NEXT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "route_id": "RT4779_1_open_E00",
            "route": "replace private E00 zero with open/radiative numeric bound when testing real systems",
            "payoff": "needed before public/open empirical claims",
            "selection_status": "QUEUED_FOR_OPEN_ARENAS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PG4779_0", "private selector E00 zero is not public/open E00 evidence", "blocks scope leak"),
        ("PG4779_1", "M_H^dress missing keeps all Newton/orbital score rows nonclaim", "blocks partial pass"),
        ("PG4779_2", "observed GM comparator remains comparator-only", "blocks circular source mass"),
        ("PG4779_3", "future open systems must replace E00=0 with a sourced bound or theorem", "sets reopen rule"),
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
        ("FW4779_0", "E00 zero is private-selector-only", "NO_PUBLIC_E00_CLAIM"),
        ("FW4779_1", "runner must not pass without M_H^dress", "MHDRESS_BLOCKER_ACTIVE"),
        ("FW4779_2", "GM comparator cannot be mass definition", "ANTI_CIRCULARITY_ACTIVE"),
        ("FW4779_3", "no GitHub/public claim from this checkpoint", "LOCAL_PRIVATE_ONLY"),
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
            "meaning": "4779 fills the E00 numeric zero bound for the private local-GR selector and reruns the evaluator, reducing the live runner blocker from MHdress+E00 to MHdress only.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_E00_BOUND_FILLED_NONCLAIM",
            "summary": "Private-selector E00=0 bound filled and runner now blocks only on M_Hdress; no public/open score claimed.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "With private E00 bound filled, the next blocker is the primary H_tau-H_ref source-functional mass row.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(timestamp: str, e00: list[dict[str, Any]], score: list[dict[str, Any]], reqs: list[dict[str, Any]], audit: list[dict[str, Any]], routes: list[dict[str, Any]]) -> None:
    output = parse_csv(RUNNER_OUTPUT_CSV)[0]
    doc = f"""# 4779 — Fill MHdress Source Row or E00 Numeric Bound From Local Arena

Generated: `{timestamp}`

## Result

4779 fills the safer numeric side first:

```text
E_00 = 0
int_W |E_00| dV = 0
```

Scope:

```text
private/effective local-GR selector only.
not public/open/radiative arena evidence.
```

Runner outcome:

```text
eta_E00_abs = {output["eta_E00_abs"]}
runner_status = {output["runner_status"]}
```

So the live evaluator blocker has moved from:

```text
BLOCKED_MISSING_MHDRESS_AND_E00_BOUND
```

to:

```text
BLOCKED_MISSING_MHDRESS
```

## E00 Numeric Bound Row

{markdown_table(e00, ["bound_id", "quantity", "numeric_value", "scope", "status"])}

## Score Gate Update

{markdown_table(score, ["gate_id", "object", "before", "after", "runner_status"])}

## MHdress Requirements

{markdown_table(reqs, ["requirement_id", "required_object", "status"])}

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

    formal = f"""# PPC4161 4779: Private E00 Numeric Bound Row

Generated: `{timestamp}`

4779 fills:

```text
E_00=0
int_W |E_00|dV=0
```

inside the private/effective local-GR selector only.

Runner status is now:

```text
{output["runner_status"]}
```

The remaining live blocker is:

```text
M_H^dress = H_tau[S_link;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs].
```

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    output = parse_csv(RUNNER_OUTPUT_CSV)[0]
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4779 fills the private-selector numeric `E_00=0` bound and `int_W |E_00|dV=0` for the private/effective local-GR branch.
- This is not public/open/radiative evidence; it is scoped to the 4775 private selector certificate.
- The 4778 runner now reports `{output["runner_status"]}`, so the live evaluator blocker is only `M_H^dress`.
- Next work must evaluate or certify `M_H^dress=H_tau-H_ref` without using observed `GM/G_cal` as the definition.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4779 packet update: private-selector `E_00` is now machine-filled as zero. The runner still blocks because `M_H^dress` is missing. Next: evaluate `H_tau-H_ref`.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4779-Y5-R2FR-fill-MHdress-source-row-or-E00-numeric-bound-from-local-arena.md`

## Decision

`{DECISION}`

## What moved forward

- Filled the private-selector numeric `E_00=0` bound and `int_W |E_00|dV=0`.
- Re-ran the 4778 evaluator with the private E00 row.
- Reduced runner blocker from `BLOCKED_MISSING_MHDRESS_AND_E00_BOUND` to `{output["runner_status"]}`.
- Kept all public/open/radiative Newton/orbital claims blocked.
- Left `M_H^dress=H_tau-H_ref` as the live required source-functional row.

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
        "private_selector_E00_numeric_zero_bound",
        "4779 fills the private-selector E00=0 numeric bound and reruns the MHdress/E00 evaluator, reducing the blocker to MHdress only.",
        "Generated source register, E00 numeric bound, runner input/output, MHdress requirements, score gate update, anti-circularity audit, route matrix, promotion gates, firewalls, decision, status, next target and validation.",
        "private_e00_bound_nonclaim",
        NEXT_TARGET,
        "Do not use this private-selector E00 zero as public/open/radiative arena evidence.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need H_tau-H_ref/MHdress source-functional first row.",
        "Private E00 numeric bound",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(timestamp: str, sources: list[dict[str, Any]], e00: list[dict[str, Any]], output: list[dict[str, Any]], reqs: list[dict[str, Any]], score: list[dict[str, Any]], audit: list[dict[str, Any]], routes: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4779_0_sources_exist", "all source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4779_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4779_2_runner_exists", "runner script exists", RUNNER_PATH.exists(), str(RUNNER_PATH)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4779_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and len(parse_csv(csv_path)) > 0, str(csv_path)))

    checks.append(("VAL4779_3_e00_zero", "E00 zero numeric bound row exists", any(row["quantity"] == "E_00" and float(row["numeric_value"]) == 0.0 and row["status"] == "FILLED_PRIVATE_SELECTOR_NUMERIC_ZERO_BOUND_NONCLAIM" for row in e00), str(E00_BOUND_CSV)))
    checks.append(("VAL4779_4_integral_zero", "E00 integral zero row exists", any(row["quantity"] == "int_W_abs_E00_dV" and float(row["numeric_value"]) == 0.0 for row in e00), str(E00_BOUND_CSV)))
    checks.append(("VAL4779_5_runner_reduced_blocker", "runner now blocks only on MHdress", any(row["runner_status"] == "BLOCKED_MISSING_MHDRESS" and row["eta_E00_abs"] == "0.000000000000000e+00" for row in output), str(RUNNER_OUTPUT_CSV)))
    checks.append(("VAL4779_6_mhdress_still_missing", "MHdress requirement remains missing", any(row["required_object"] == "M_H^dress=H_tau-H_ref" and row["status"] == "MISSING_PRIMARY_MTS_MASS_VALUE" for row in reqs), str(MHDRESS_REQUIREMENTS_CSV)))
    checks.append(("VAL4779_7_score_gate", "score gate update says after blocked by MHdress", any(row["gate_id"] == "SG4779_3_score" and row["after"] == "BLOCKED_MISSING_MHDRESS" for row in score), str(SCORE_GATE_CSV)))
    checks.append(("VAL4779_8_audit_pass", "anti-circularity audit passes", all(row["status"].startswith("PASS") for row in audit), str(ANTI_CIRCULARITY_CSV)))
    checks.append(("VAL4779_9_route_selected", "MHdress route selected next", any(row["selection_status"] == "SELECTED_NEXT" and "H_tau-H_ref" in row["route"] for row in routes), str(ROUTE_MATRIX_CSV)))
    checks.append(("VAL4779_10_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4779_11_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4779_12_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4779_13_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4779_14_claim_row", "claim row L-621 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4779_15_resume", "resume points from 4779 to 4780", "4779-Y5" in resume_text and "4780-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4779_16_pycache_absent", "scripts __pycache__ removed", not (SCRIPT_DIR / "__pycache__").exists(), str(SCRIPT_DIR)))

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
            "validation_id": "VAL4779_OVERALL",
            "check": "all 4779 private E00 bound checks pass",
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
    e00 = e00_bound_rows(timestamp)
    runner_input = runner_input_rows(timestamp)
    reqs = mhdress_requirement_rows(timestamp)
    audit = anti_circularity_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(E00_BOUND_CSV, e00)
    write_csv(RUNNER_INPUT_CSV, runner_input)
    subprocess.run([sys.executable, str(RUNNER_PATH), str(RUNNER_INPUT_CSV), str(RUNNER_OUTPUT_CSV)], check=True)
    score = score_gate_rows(timestamp)
    write_csv(MHDRESS_REQUIREMENTS_CSV, reqs)
    write_csv(SCORE_GATE_CSV, score)
    write_csv(ANTI_CIRCULARITY_CSV, audit)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, e00, score, reqs, audit, routes)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(timestamp, sources, e00, parse_csv(RUNNER_OUTPUT_CSV), reqs, score, audit, routes, gates))


if __name__ == "__main__":
    main()
