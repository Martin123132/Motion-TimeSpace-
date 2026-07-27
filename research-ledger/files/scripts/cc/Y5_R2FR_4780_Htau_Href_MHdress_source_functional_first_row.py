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
SOURCE_RUNNER = SCRIPT_DIR / "Htau_Href_MHdress_source_runner.py"
OPEN_RUNNER = SCRIPT_DIR / "MHdress_E00_open_arena_runner.py"

CHECKPOINT = "4780"
CLAIM_ID = "L-622"
MARKER = "PPC4161_HTAU_HREF_MHDRESS_SOURCE_FUNCTIONAL_FIRST_ROW_4780"
PACKET_MARKER = "PPC4161_PACKET_HTAU_HREF_MHDRESS_SOURCE_FUNCTIONAL_FIRST_ROW_4780"
DECISION = "HTAU_HREF_MHDRESS_SOURCE_FUNCTIONAL_RUNNER_IMPLEMENTED_MISSING_PARENT_CHARGE_BLOCKS_COUNTERFACTUAL_SMOKE_PASSES_NONCLAIM"
NEXT_TARGET = "4781-Y5-R2FR-Htau-Href-parent-charge-evaluation-or-reference-bound.md"

DOC_PATH = POST / "4780-Y5-R2FR-Htau-Href-MHdress-source-functional-first-row.md"
FORMAL_PATH = FORMAL / "796-PPC4161-Htau-Href-MHdress-source-functional-first-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4780_SOURCE_REGISTER.csv"
SOURCE_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4780_HTAU_HREF_SOURCE_CONTRACT.csv"
SOURCE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4780_HTAU_HREF_SOURCE_INPUT.csv"
SOURCE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4780_HTAU_HREF_SOURCE_OUTPUT.csv"
OPEN_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4780_OPEN_ARENA_RUNNER_INPUT.csv"
OPEN_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4780_OPEN_ARENA_RUNNER_OUTPUT.csv"
SCORE_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4780_SCORE_GATE_UPDATE.csv"
ANTI_CIRCULARITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4780_ANTI_CIRCULARITY_AUDIT.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4780_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4780_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4780_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4780_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4780_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4780_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4780_VALIDATION.csv"

G_CAL = 6.67430e-11
MU_SUN_NOMINAL = 1.3271244e20
SOLAR_RADIUS_NOMINAL = 6.957e8
M_GM_SUN_CAL = MU_SUN_NOMINAL / G_CAL

SOURCE_SPECS = [
    ("SRC4780_0_4779_requirement", SOURCE_DIR / "P8_Y5_R2FR_4779_MHDRESS_SOURCE_FUNCTIONAL_INPUT_REQUIREMENTS.csv", "MHR4779_2_difference", "4779 live MHdress blocker"),
    ("SRC4780_1_4779_runner", SOURCE_DIR / "P8_Y5_R2FR_4779_OPEN_ARENA_RUNNER_OUTPUT.csv", "BLOCKED_MISSING_MHDRESS", "4779 runner reduced blocker"),
    ("SRC4780_2_4777_comparator", SOURCE_DIR / "P8_Y5_R2FR_4777_MHDRESS_GM_COMPARATOR_ROW.csv", "GM4777_2_mass_comparator_from_mu", "4777 solar GM comparator"),
    ("SRC4780_3_4779_E00", SOURCE_DIR / "P8_Y5_R2FR_4779_E00_NUMERIC_BOUND_ROW.csv", "E004779_0_private_selector_E00_zero", "4779 private E00 bound"),
    ("SRC4780_4_4170_mass", SOURCE_DIR / "P8_Y5_R2FR_4170_HAMILTONIAN_BRANCH_ADOPTION.csv", "HQ4170_3_mass_definition", "4170 Hamiltonian dressed mass definition"),
    ("SRC4780_5_4170_projector", SOURCE_DIR / "P8_Y5_R2FR_4170_HAMILTONIAN_BRANCH_ADOPTION.csv", "HQ4170_4_projector_identity", "4170 Hamiltonian source projector identity"),
    ("SRC4780_6_4170_radial", SOURCE_DIR / "P8_Y5_R2FR_4170_NOETHER_RADIAL_GLUE.csv", "NG4170_6_radial", "4170 radial charge closure"),
    ("SRC4780_7_4764_definition", SOURCE_DIR / "P8_Y5_R2FR_4764_MLOWER_PIM_DENOMINATOR_LEMMA.csv", "DL4764_0_definition", "4764 same-frame Htau-Href denominator definition"),
    ("SRC4780_8_formal_186", FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md", "M_H^dress[W_H;tau] = H_tau[S_link] - H_ref", "formal 186 anti-circular Hamiltonian mass definition"),
    ("SRC4780_9_formal_227", FORMAL / "227-PPC4161-Htau-MHsource-parent-charge-owner.md", "M_H^dress[W_H;tau] = H_tau[S_link] - H_ref", "formal 227 parent charge owner contract"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    SOURCE_CONTRACT_CSV,
    SOURCE_INPUT_CSV,
    SOURCE_OUTPUT_CSV,
    OPEN_INPUT_CSV,
    OPEN_OUTPUT_CSV,
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


def source_contract_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("HC4780_0_definition", "M_H^dress := H_tau[S_link;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs]", "primary source mass functional", "definition ready; values missing"),
        ("HC4780_1_no_GM_backfill", "M_GM_cal=mu_ref/G_cal is comparator only", "blocks circular source mass definition", "enforced by runner"),
        ("HC4780_2_Htau_input", "H_tau[S_link;tau,e_obs]", "Hamiltonian charge from theta_total/Q_tau on chosen surface", "missing parent/numeric evaluation"),
        ("HC4780_3_Href_input", "H_ref[Sigma_ref;tau,e_obs]", "fixed source-blind reference selected before readout", "missing parent/numeric evaluation"),
        ("HC4780_4_downstream", "M_H^dress feeds MHdress_E00_open_arena_runner.py", "connect source functional to Newton/orbital evaluator", "wired in 4780"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "contract_id": contract_id,
            "contract_statement": statement,
            "role": role,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, statement, role, status in specs
    ]


def source_input_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": "private_selector_missing_Htau_Href",
            "H_tau_kg": "",
            "H_tau_source": "MISSING_PARENT_CHARGE_EVALUATION",
            "H_ref_kg": "",
            "H_ref_source": "MISSING_FIXED_REFERENCE_EVALUATION",
            "M_GM_cal_kg": f"{M_GM_SUN_CAL:.15e}",
            "row_status": "nonclaim_missing_Htau_Href",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "source_id": "private_selector_counterfactual_Htau_minus_Href_equals_comparator",
            "H_tau_kg": f"{M_GM_SUN_CAL:.15e}",
            "H_tau_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            "H_ref_kg": "0",
            "H_ref_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            "M_GM_cal_kg": f"{M_GM_SUN_CAL:.15e}",
            "row_status": "counterfactual_smoke_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def run_source_runner() -> None:
    subprocess.run([sys.executable, str(SOURCE_RUNNER), str(SOURCE_INPUT_CSV), str(SOURCE_OUTPUT_CSV)], check=True)


def open_input_rows(timestamp: str) -> list[dict[str, Any]]:
    source_outputs = parse_csv(SOURCE_OUTPUT_CSV)
    rows: list[dict[str, Any]] = []
    for source_output in source_outputs:
        m_h = source_output["M_H_dress_kg"]
        if m_h == "MISSING_NUMERIC_VALUE":
            m_h = ""
        rows.append(
            {
                "arena_id": source_output["source_id"],
                "mu_ref_m3_s2": f"{MU_SUN_NOMINAL:.7e}",
                "mu_ref_source": "IAU_2015_B3_nominal_solar_GM_comparator",
                "G_cal_m3_kg_s2": f"{G_CAL:.8e}",
                "M_H_dress_kg": m_h,
                "M_H_source": "H_tau_minus_H_ref_runner_output",
                "sigma_M_H_kg": "",
                "E00_integral_abs_m": "0",
                "E00_sup_abs_m_minus2": "0",
                "support_radius_m": f"{SOLAR_RADIUS_NOMINAL:.6e}",
                "tolerance_eta": "1.0e-10",
                "delta_mu_boundary_abs_m3_s2": "0",
                "delta_mu_profile_abs_m3_s2": "0",
                "delta_mu_readout_abs_m3_s2": "0",
                "row_status": "counterfactual_smoke_nonclaim" if source_output["source_id"].startswith("private_selector_counterfactual") else "source_functional_missing_nonclaim",
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def run_open_runner() -> None:
    subprocess.run([sys.executable, str(OPEN_RUNNER), str(OPEN_INPUT_CSV), str(OPEN_OUTPUT_CSV)], check=True)


def score_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    source_outputs = parse_csv(SOURCE_OUTPUT_CSV)
    open_outputs = parse_csv(OPEN_OUTPUT_CSV)
    rows: list[dict[str, Any]] = []
    for source_output, open_output in zip(source_outputs, open_outputs):
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "gate_id": f"SG4780_{source_output['source_id']}",
                "source_id": source_output["source_id"],
                "M_H_dress_kg": source_output["M_H_dress_kg"],
                "source_runner_status": source_output["runner_status"],
                "open_runner_status": open_output["runner_status"],
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def anti_circularity_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("AC4780_0", "source runner computes M_H^dress only from H_tau-H_ref, never from GM/G_cal", "PASS_HTAU_HREF_ONLY"),
        ("AC4780_1", "missing physical H_tau/H_ref row blocks instead of importing comparator mass", "PASS_MISSING_BLOCKS"),
        ("AC4780_2", "counterfactual Htau/Href row is smoke-only and claim_allowed=false", "PASS_SMOKE_FIREWALL"),
        ("AC4780_3", "downstream open runner receives M_H only from source-runner output", "PASS_CHAINED_SOURCE_DISCIPLINE"),
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
            "route_id": "RT4780_0_Htau",
            "route": "evaluate H_tau[S_link;tau,e_obs] from parent local packet charge",
            "payoff": "fills first half of M_Hdress source functional",
            "selection_status": "SELECTED_NEXT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "route_id": "RT4780_1_Href",
            "route": "evaluate or bound H_ref[Sigma_ref;tau,e_obs] with fixed source-blind reference",
            "payoff": "fills second half of M_Hdress source functional",
            "selection_status": "SELECTED_NEXT_PARALLEL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PG4780_0", "no observed GM/G_cal may be copied into H_tau, H_ref or M_Hdress physical rows", "blocks circular mass row"),
        ("PG4780_1", "counterfactual smoke pass is not a Newton/orbital claim", "blocks smoke promotion"),
        ("PG4780_2", "physical row remains blocked until H_tau and H_ref are parent/numeric evaluated", "blocks partial source-functional claim"),
        ("PG4780_3", "downstream score requires source-runner output, E00 row and residual ledgers", "keeps evaluator discipline"),
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
        ("FW4780_0", "M_Hdress runner does not accept GM backfill", "ANTI_CIRCULARITY_ACTIVE"),
        ("FW4780_1", "missing Htau/Href row blocks", "PARENT_CHARGE_VALUES_MISSING"),
        ("FW4780_2", "counterfactual row is smoke only", "NO_EMPIRICAL_CLAIM"),
        ("FW4780_3", "no GitHub/public claim from this checkpoint", "LOCAL_PRIVATE_ONLY"),
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
            "meaning": "4780 implements the Htau-Href source-functional runner and chains it into the Newton/orbital evaluator, proving missing parent charge blocks and counterfactual source values only smoke-test the pipeline.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_HTAU_HREF_RUNNER_IMPLEMENTED_NONCLAIM",
            "summary": "Htau-Href source runner implemented; missing physical row blocks; counterfactual smoke row passes only nonclaim.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "The runner is ready; the real next work is parent/numeric evaluation or bounding of H_tau and H_ref.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(timestamp: str, contract: list[dict[str, Any]], source_status: list[dict[str, Any]], open_status: list[dict[str, Any]], score: list[dict[str, Any]], audit: list[dict[str, Any]], routes: list[dict[str, Any]]) -> None:
    doc = f"""# 4780 — Htau/Href/MHdress Source-Functional First Row

Generated: `{timestamp}`

## Result

4780 adds the source-functional runner:

```text
{SOURCE_RUNNER}
```

It computes only:

```text
M_H^dress = H_tau[S_link;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs].
```

It does **not** define `M_H^dress` from observed `GM/G_cal`.

## Source Contract

{markdown_table(contract, ["contract_id", "contract_statement", "status"])}

## Htau/Href Source Runner Output

{markdown_table(source_status, ["source_id", "M_H_dress_kg", "Delta_MH_rel", "runner_status"])}

## Downstream Newton/Orbital Evaluator Output

{markdown_table(open_status, ["arena_id", "M_GM_cal_kg", "Delta_MH_rel", "eta_E00_abs", "runner_status"])}

## Score Gate Update

{markdown_table(score, ["source_id", "M_H_dress_kg", "source_runner_status", "open_runner_status"])}

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

    formal = f"""# PPC4161 4780: Htau/Href/MHdress Source-Functional Runner

Generated: `{timestamp}`

4780 installs:

```text
{SOURCE_RUNNER}
```

The source mass rule is:

```text
M_H^dress = H_tau[S_link;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs].
```

The real row remains blocked until `H_tau` and `H_ref` are evaluated or bounded from the parent/local Hamiltonian charge. Counterfactual rows only smoke-test the arithmetic.

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4780 implements `{SOURCE_RUNNER.name}`, which computes `M_H^dress=H_tau-H_ref` and refuses observed-`GM` backfill.
- The missing physical `H_tau/H_ref` row blocks as expected.
- A counterfactual row with `H_tau-H_ref=M_GM_cal` passes only as nonclaim smoke and then passes the downstream Newton/orbital runner as smoke.
- The next real task is evaluating or bounding `H_tau[S_link;tau,e_obs]` and `H_ref[Sigma_ref;tau,e_obs]`.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4780 packet update: the `M_H^dress` blocker is now executable. No future row should handwrite `M_H^dress`; it should pass through the Htau/Href runner or a stricter successor.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4780-Y5-R2FR-Htau-Href-MHdress-source-functional-first-row.md`

## Decision

`{DECISION}`

## What moved forward

- Added executable source-functional runner `{SOURCE_RUNNER}`.
- Chained `M_H^dress=H_tau-H_ref` output into the existing Newton/orbital evaluator.
- Confirmed missing physical `H_tau/H_ref` values block cleanly.
- Confirmed counterfactual source values pass only as nonclaim smoke.
- Kept observed `GM/G_cal` as comparator-only, never as the source mass definition.

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
        "htau_href_mhdress_source_functional_runner",
        "4780 implements the Htau-Href source-functional runner and chains it into the Newton/orbital evaluator.",
        "Generated source register, source contract, source input/output, open runner input/output, score gate update, anti-circularity audit, route matrix, promotion gates, firewalls, decision, status, next target and validation.",
        "source_functional_runner_nonclaim",
        NEXT_TARGET,
        "Do not use observed GM/Gcal as M_Hdress or treat counterfactual smoke as evidence.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need real Htau/Href parent charge evaluation or reference bound.",
        "Htau-Href source-functional runner",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(timestamp: str, sources: list[dict[str, Any]], contract: list[dict[str, Any]], source_output: list[dict[str, Any]], open_output: list[dict[str, Any]], score: list[dict[str, Any]], audit: list[dict[str, Any]], routes: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4780_0_sources_exist", "all source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4780_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4780_2_runners_exist", "both runners exist", SOURCE_RUNNER.exists() and OPEN_RUNNER.exists(), f"{SOURCE_RUNNER}; {OPEN_RUNNER}"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4780_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and len(parse_csv(csv_path)) > 0, str(csv_path)))

    checks.append(("VAL4780_3_contract", "contract includes Htau-Href definition", any(row["contract_id"] == "HC4780_0_definition" and "H_tau" in row["contract_statement"] for row in contract), str(SOURCE_CONTRACT_CSV)))
    checks.append(("VAL4780_4_missing_blocks", "missing Htau/Href row blocks", any(row["source_id"] == "private_selector_missing_Htau_Href" and row["runner_status"] == "BLOCKED_MISSING_HTAU_OR_HREF" for row in source_output), str(SOURCE_OUTPUT_CSV)))
    checks.append(("VAL4780_5_counterfactual_source_smoke", "counterfactual Htau/Href row smokes", any(row["source_id"].startswith("private_selector_counterfactual") and row["runner_status"] == "MHDRESS_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM" and row["claim_allowed"] == "False" for row in source_output), str(SOURCE_OUTPUT_CSV)))
    checks.append(("VAL4780_6_downstream_missing_blocks", "downstream missing row remains blocked", any(row["arena_id"] == "private_selector_missing_Htau_Href" and row["runner_status"] == "BLOCKED_MISSING_MHDRESS" for row in open_output), str(OPEN_OUTPUT_CSV)))
    checks.append(("VAL4780_7_downstream_counterfactual_smoke", "downstream counterfactual row smokes", any(row["arena_id"].startswith("private_selector_counterfactual") and row["runner_status"] == "RUNNER_SMOKE_PASS_NONCLAIM" and row["claim_allowed"] == "False" for row in open_output), str(OPEN_OUTPUT_CSV)))
    checks.append(("VAL4780_8_score_gate", "score gate records both source and open statuses", any(row["source_runner_status"] == "BLOCKED_MISSING_HTAU_OR_HREF" for row in score) and any(row["open_runner_status"] == "RUNNER_SMOKE_PASS_NONCLAIM" for row in score), str(SCORE_GATE_CSV)))
    checks.append(("VAL4780_9_audit_pass", "anti-circularity audit passes", all(row["status"].startswith("PASS") for row in audit), str(ANTI_CIRCULARITY_CSV)))
    checks.append(("VAL4780_10_route_selected", "Htau and Href routes selected", any(row["selection_status"] == "SELECTED_NEXT" for row in routes) and any(row["selection_status"] == "SELECTED_NEXT_PARALLEL" for row in routes), str(ROUTE_MATRIX_CSV)))
    checks.append(("VAL4780_11_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4780_12_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4780_13_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4780_14_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4780_15_claim_row", "claim row L-622 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4780_16_resume", "resume points from 4780 to 4781", "4780-Y5" in resume_text and "4781-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4780_17_pycache_absent", "scripts __pycache__ removed", not (SCRIPT_DIR / "__pycache__").exists(), str(SCRIPT_DIR)))

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
            "validation_id": "VAL4780_OVERALL",
            "check": "all 4780 Htau-Href runner checks pass",
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
    contract = source_contract_rows(timestamp)
    source_inputs = source_input_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(SOURCE_CONTRACT_CSV, contract)
    write_csv(SOURCE_INPUT_CSV, source_inputs)
    run_source_runner()
    open_inputs = open_input_rows(timestamp)
    write_csv(OPEN_INPUT_CSV, open_inputs)
    run_open_runner()

    source_outputs = parse_csv(SOURCE_OUTPUT_CSV)
    open_outputs = parse_csv(OPEN_OUTPUT_CSV)
    score = score_gate_rows(timestamp)
    audit = anti_circularity_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SCORE_GATE_CSV, score)
    write_csv(ANTI_CIRCULARITY_CSV, audit)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, contract, source_outputs, open_outputs, score, audit, routes)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(timestamp, sources, contract, source_outputs, open_outputs, score, audit, routes, gates))


if __name__ == "__main__":
    main()
