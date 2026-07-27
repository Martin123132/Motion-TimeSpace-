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

PARENT_RUNNER = SCRIPT_DIR / "parent_charge_Htau_Href_bound_runner.py"
SOURCE_RUNNER = SCRIPT_DIR / "Htau_Href_MHdress_source_runner.py"
OPEN_RUNNER = SCRIPT_DIR / "MHdress_E00_open_arena_runner.py"

CHECKPOINT = "4781"
CLAIM_ID = "L-623"
MARKER = "PPC4161_HTAU_HREF_PARENT_CHARGE_EVALUATION_OR_REFERENCE_BOUND_4781"
PACKET_MARKER = "PPC4161_PACKET_HTAU_HREF_PARENT_CHARGE_EVALUATION_OR_REFERENCE_BOUND_4781"
DECISION = "PARENT_CHARGE_EVALUATOR_AND_NO_CANCELLATION_BOUND_INTERFACE_INSTALLED_REAL_ROW_BLOCKS_COUNTERFACTUAL_SMOKES_NONCLAIM"
NEXT_TARGET = "4782-Y5-R2FR-parent-Htau-density-current-first-source-row-or-Mlower-bound-fill.md"

DOC_PATH = POST / "4781-Y5-R2FR-Htau-Href-parent-charge-evaluation-or-reference-bound.md"
FORMAL_PATH = FORMAL / "797-PPC4161-Htau-Href-parent-charge-evaluation-or-reference-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4781_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4781_PARENT_CHARGE_THEOREM.csv"
CHARGE_BOUND_LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4781_CHARGE_BOUND_LAW.csv"
PARENT_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4781_PARENT_CHARGE_INPUT.csv"
PARENT_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4781_PARENT_CHARGE_OUTPUT.csv"
SOURCE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4781_HTAU_HREF_SOURCE_INPUT_FROM_PARENT_CHARGE.csv"
SOURCE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4781_HTAU_HREF_SOURCE_OUTPUT_FROM_PARENT_CHARGE.csv"
OPEN_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4781_OPEN_ARENA_INPUT_FROM_PARENT_CHARGE.csv"
OPEN_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4781_OPEN_ARENA_OUTPUT_FROM_PARENT_CHARGE.csv"
SCORE_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4781_SCORE_GATE_UPDATE.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4781_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4781_FIREWALL_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4781_ROUTE_SELECTION_MATRIX.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4781_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4781_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4781_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4781_VALIDATION.csv"

G_CAL = 6.67430e-11
MU_SUN_NOMINAL = 1.3271244e20
SOLAR_RADIUS_NOMINAL = 6.957e8
M_GM_SUN_CAL = MU_SUN_NOMINAL / G_CAL

SOURCE_SPECS = [
    ("SRC4781_00_4780_doc", DOC_PATH.with_name("4780-Y5-R2FR-Htau-Href-MHdress-source-functional-first-row.md"), "M_H^dress = H_tau", "4780 source-functional runner target"),
    ("SRC4781_01_4780_contract", SOURCE_DIR / "P8_Y5_R2FR_4780_HTAU_HREF_SOURCE_CONTRACT.csv", "HC4780_2_Htau_input", "4780 Htau/Href missing input contract"),
    ("SRC4781_02_formal_227", FORMAL / "227-PPC4161-Htau-MHsource-parent-charge-owner.md", "M_H^dress[W_H;tau] = H_tau[S_link] - H_ref", "4211 parent charge owner contract"),
    ("SRC4781_03_formal_228", FORMAL / "228-PPC4161-Htau-integrability-operator-and-curl-bound.md", "H_tau exists on the allowed local branch", "4212 field-space curl integrability operator"),
    ("SRC4781_04_formal_236", FORMAL / "236-PPC4161-MHref-positive-source-denominator-stability-or-bound-pack.md", "M_H_ref >= M_EH", "4220 positive denominator guard"),
    ("SRC4781_05_4589_doc", POST / "4589-Y5-R2FR-MHref-source-blind-reference-and-Htau-normalization-zero-or-bound.md", "M_H_ref := H_tau[S_link;tau,e_obs] - H_ref", "4589 q-basic reference theorem"),
    ("SRC4781_06_4589_theorem", SOURCE_DIR / "P8_Y5_R2FR_4589_MHREF_QBASIC_THEOREM.csv", "MHR4589_2_no_cancellation_bound", "4589 no-cancellation denominator drift bound"),
    ("SRC4781_07_4756_source_lock", SOURCE_DIR / "P8_Y5_R2FR_4756_SOURCE_CHARGE_LOCK_ROWS.csv", "SCL4756_2_integrability", "4756 structural Newton source-charge lock"),
    ("SRC4781_08_parent_runner", PARENT_RUNNER, "def compute_row", "4781 executable parent charge/bound runner"),
    ("SRC4781_09_source_runner", SOURCE_RUNNER, "BLOCKED_MISSING_HTAU_OR_HREF", "4780 Htau-Href arithmetic runner"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    THEOREM_CSV,
    CHARGE_BOUND_LAW_CSV,
    PARENT_INPUT_CSV,
    PARENT_OUTPUT_CSV,
    SOURCE_INPUT_CSV,
    SOURCE_OUTPUT_CSV,
    OPEN_INPUT_CSV,
    OPEN_OUTPUT_CSV,
    SCORE_GATE_CSV,
    PROMOTION_GATES_CSV,
    FIREWALL_CSV,
    ROUTE_MATRIX_CSV,
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


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


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


def format_float(value: float) -> str:
    return f"{value:.15e}"


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row[column]).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


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


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "PCT4781_0_variational_charge",
            "delta H_tau[S]=int_S(delta Q_tau-i_tau theta_total(delta))",
            "The parent charge must come from the local-packet covariant phase-space current, not from observed orbital GM.",
            "definition/imported from 4211/4212",
        ),
        (
            "PCT4781_1_integrability",
            "I_tau,S=d_field alpha_tau,S=int_S i_tau omega_total+I_ref+I_tau+I_corner",
            "H_tau exists as a number only when the field-space curl is zero or bounded on the chosen surface family.",
            "operator derived; full zero still conditional",
        ),
        (
            "PCT4781_2_reference",
            "H_ref=Hbar_ref(q(Phi)) selected before readout",
            "A source-blind q-basic reference gives D_v H_ref=0; otherwise its drift is a retained no-cancellation term.",
            "conditional zero or bound",
        ),
        (
            "PCT4781_3_bound",
            "M_H^dress in [H0-H_ref-Delta_H_abs, H0-H_ref+Delta_H_abs]",
            "Unsigned charge pieces produce an interval, not a fitted mass.",
            "new executable bound interface",
        ),
        (
            "PCT4781_4_positive_lower",
            "epsilon_Hcharge <= Delta_H_abs/M_lower, M_lower=M_EH(1-epsilon_abs)>0",
            "No normalized local-GR, PPN, R10, clock or orbital claim can divide by a missing denominator.",
            "positive guard retained",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for theorem_id, formula, meaning, status in specs
    ]


def charge_bound_law_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("CBL4781_0_center", "H_tau_center", "H_tau_bulk+H_tau_surface", "parent charge center before retained residual radius"),
        ("CBL4781_1_radius", "Delta_H_abs", "abs(H_tau_curl)+abs(H_tau_flux)+abs(H_tau_sector)+abs(H_tau_surface_residual)+abs(H_ref_drift)+abs(H_ref_selector)", "no-cancellation charge uncertainty radius"),
        ("CBL4781_2_interval_low", "M_low", "H_tau_center-H_ref-Delta_H_abs", "lower allowed Hamiltonian source mass"),
        ("CBL4781_3_interval_high", "M_high", "H_tau_center-H_ref+Delta_H_abs", "upper allowed Hamiltonian source mass"),
        ("CBL4781_4_normalized", "epsilon_Hcharge", "Delta_H_abs/M_lower", "dimensionless source-charge uncertainty if M_lower>0"),
        ("CBL4781_5_exact_zero", "exact pass", "Delta_H_abs=0 and M_low>0", "only then may a computed parent charge be fed as exact M_Hdress"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "law_id": law_id,
            "symbol": symbol,
            "formula": formula,
            "meaning": meaning,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for law_id, symbol, formula, meaning in specs
    ]


def parent_charge_input_rows(timestamp: str) -> list[dict[str, Any]]:
    residual = 0.01 * M_GM_SUN_CAL
    return [
        {
            "charge_id": "private_selector_missing_parent_charge_components",
            "H_tau_bulk_kg": "",
            "H_tau_surface_kg": "",
            "H_tau_source": "MISSING_PARENT_DENSITY_CURRENT_INTEGRAL",
            "H_ref_kg": "",
            "H_ref_source": "MISSING_SOURCE_BLIND_REFERENCE_VALUE",
            "H_tau_curl_abs_kg": "",
            "H_tau_flux_abs_kg": "",
            "H_tau_sector_abs_kg": "",
            "H_tau_surface_abs_kg": "",
            "H_ref_drift_abs_kg": "",
            "H_ref_selector_abs_kg": "",
            "M_lower_kg": "",
            "M_lower_source": "MISSING_POSITIVE_MLOWER",
            "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
            "row_status": "physical_missing_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "charge_id": "private_parent_charge_interval_smoke_nonclaim",
            "H_tau_bulk_kg": format_float(M_GM_SUN_CAL),
            "H_tau_surface_kg": "0",
            "H_tau_source": "SMOKE_PARENT_COMPONENTS_NOT_PHYSICAL",
            "H_ref_kg": "0",
            "H_ref_source": "SMOKE_SOURCE_BLIND_REFERENCE_NOT_PHYSICAL",
            "H_tau_curl_abs_kg": format_float(residual),
            "H_tau_flux_abs_kg": format_float(residual),
            "H_tau_sector_abs_kg": "0",
            "H_tau_surface_abs_kg": "0",
            "H_ref_drift_abs_kg": "0",
            "H_ref_selector_abs_kg": "0",
            "M_lower_kg": format_float(0.9 * M_GM_SUN_CAL),
            "M_lower_source": "SMOKE_POSITIVE_LOWER_BOUND_NOT_PHYSICAL",
            "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
            "row_status": "interval_smoke_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "charge_id": "counterfactual_parent_charge_equals_comparator",
            "H_tau_bulk_kg": format_float(M_GM_SUN_CAL),
            "H_tau_surface_kg": "0",
            "H_tau_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            "H_ref_kg": "0",
            "H_ref_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            "H_tau_curl_abs_kg": "0",
            "H_tau_flux_abs_kg": "0",
            "H_tau_sector_abs_kg": "0",
            "H_tau_surface_abs_kg": "0",
            "H_ref_drift_abs_kg": "0",
            "H_ref_selector_abs_kg": "0",
            "M_lower_kg": format_float(M_GM_SUN_CAL),
            "M_lower_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
            "row_status": "counterfactual_smoke_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "charge_id": "forbidden_orbital_GM_as_parent_charge_control",
            "H_tau_bulk_kg": format_float(M_GM_SUN_CAL),
            "H_tau_surface_kg": "0",
            "H_tau_source": "ORBITAL_GM_DEFINITION_CONTROL_SHOULD_FAIL",
            "H_ref_kg": "0",
            "H_ref_source": "CONTROL",
            "H_tau_curl_abs_kg": "0",
            "H_tau_flux_abs_kg": "0",
            "H_tau_sector_abs_kg": "0",
            "H_tau_surface_abs_kg": "0",
            "H_ref_drift_abs_kg": "0",
            "H_ref_selector_abs_kg": "0",
            "M_lower_kg": format_float(M_GM_SUN_CAL),
            "M_lower_source": "CONTROL",
            "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
            "row_status": "physical_circular_control_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def source_input_from_parent(timestamp: str, parent_input: list[dict[str, Any]], parent_output: list[dict[str, Any]]) -> list[dict[str, Any]]:
    input_by_id = {row["charge_id"]: row for row in parent_input}
    rows: list[dict[str, Any]] = []
    for output in parent_output:
        charge_id = output["charge_id"]
        source = input_by_id[charge_id]
        exact_counterfactual = output["runner_status"] == "PARENT_CHARGE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"
        if exact_counterfactual:
            h_tau = output["H_tau_center_kg"]
            h_ref = source["H_ref_kg"]
            row_status = "counterfactual_smoke_nonclaim"
        else:
            h_tau = ""
            h_ref = ""
            row_status = "parent_charge_bound_not_exact_or_blocked_nonclaim"
        rows.append(
            {
                "source_id": charge_id,
                "H_tau_kg": h_tau,
                "H_tau_source": "parent_charge_Htau_Href_bound_runner.py",
                "H_ref_kg": h_ref,
                "H_ref_source": "parent_charge_Htau_Href_bound_runner.py",
                "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
                "row_status": row_status,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def open_input_from_source(timestamp: str, source_output: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for output in source_output:
        exact_counterfactual = output["runner_status"] == "MHDRESS_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"
        rows.append(
            {
                "arena_id": output["source_id"],
                "mu_ref_m3_s2": f"{MU_SUN_NOMINAL:.8e}",
                "mu_ref_source": "IAU_2015_B3_nominal_solar_GM_comparator",
                "G_cal_m3_kg_s2": f"{G_CAL:.8e}",
                "M_H_dress_kg": output["M_H_dress_kg"] if exact_counterfactual else "",
                "M_H_source": "Htau_Href_source_runner_after_parent_charge_runner",
                "sigma_M_H_kg": "",
                "E00_integral_abs_m": "0",
                "E00_sup_abs_m_minus2": "0",
                "support_radius_m": f"{SOLAR_RADIUS_NOMINAL:.6e}",
                "tolerance_eta": "1.0e-10",
                "delta_mu_boundary_abs_m3_s2": "0",
                "delta_mu_profile_abs_m3_s2": "0",
                "delta_mu_readout_abs_m3_s2": "0",
                "row_status": "counterfactual_smoke_nonclaim" if exact_counterfactual else "parent_charge_bound_not_exact_or_blocked_nonclaim",
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def score_gate_rows(timestamp: str, parent_output: list[dict[str, Any]], source_output: list[dict[str, Any]], open_output: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_by_id = {row["source_id"]: row for row in source_output}
    open_by_id = {row["arena_id"]: row for row in open_output}
    rows: list[dict[str, Any]] = []
    for parent in parent_output:
        charge_id = parent["charge_id"]
        source = source_by_id.get(charge_id, {})
        arena = open_by_id.get(charge_id, {})
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "gate_id": f"SG4781_{charge_id}",
                "charge_id": charge_id,
                "parent_runner_status": parent["runner_status"],
                "source_runner_status": source.get("runner_status", "MISSING_SOURCE_RUNNER_OUTPUT"),
                "open_runner_status": arena.get("runner_status", "MISSING_OPEN_RUNNER_OUTPUT"),
                "epsilon_Hcharge_abs": parent["epsilon_Hcharge_abs"],
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PG4781_0", "parent charge exactness", "blocks exact M_Hdress unless H_tau/H_ref components and residual radius are source-backed"),
        ("PG4781_1", "interval branch", "interval/bound rows are not exact Newton/orbital source masses"),
        ("PG4781_2", "positive lower bound", "normalized local bounds blocked if M_lower is missing or nonpositive"),
        ("PG4781_3", "anti-circularity", "observed GM/Gcal cannot define H_tau, H_ref or M_lower"),
        ("PG4781_4", "counterfactual smoke", "counterfactual pass only proves runner arithmetic and chaining"),
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
        ("FW4781_0", "no observed-GM backfill", "ACTIVE"),
        ("FW4781_1", "no exact claim from interval bounds", "ACTIVE"),
        ("FW4781_2", "no public/local-GR claim from private selector smoke", "ACTIVE"),
        ("FW4781_3", "no GitHub/public action from this checkpoint", "LOCAL_PRIVATE_ONLY"),
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


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("RT4781_0_density_current", "fill H_tau_bulk from parent density/current integral on W_H", "highest value; fills real source charge center", "SELECTED_NEXT"),
        ("RT4781_1_reference", "derive H_ref=0 or fixed source-blind reference value in the same branch", "closes subtraction ambiguity", "SELECTED_NEXT_PARALLEL"),
        ("RT4781_2_Mlower", "source or derive positive M_lower=M_EH(1-epsilon_abs)", "lets interval rows become normalized bounds", "SELECTED_NEXT_PARALLEL"),
        ("RT4781_3_residual_radius", "fill curl/flux/sector/reference residual radius components", "turns symbolic bound into scoreable local residual", "SELECTED_NEXT_PARALLEL"),
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


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "meaning": "4781 converts H_tau/H_ref into an executable parent-charge and no-cancellation bound interface. Real rows remain blocked without parent density/current, reference, residual radius and M_lower inputs; counterfactual rows only smoke-test the chain.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PARENT_CHARGE_BOUND_RUNNER_INSTALLED_NONCLAIM",
            "summary": "Parent charge evaluator installed; exact, interval, missing and circular-control branches validate; real Htau/Href source values remain missing.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "The charge interface is now executable; the next physical move is to fill H_tau_bulk/H_ref/M_lower/residual-radius from parent density-current or theorem-zero rows.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(
    timestamp: str,
    theorem: list[dict[str, Any]],
    bound_law: list[dict[str, Any]],
    parent_output: list[dict[str, Any]],
    score: list[dict[str, Any]],
    routes: list[dict[str, Any]],
) -> None:
    content = f"""# 4781 - Htau/Href parent charge evaluation or reference bound

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4781 turns the live 4780 blocker into an executable parent-charge interface. The exact source mass is still:

```text
M_H^dress[W_H;tau,e_obs] = H_tau[S_link;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs].
```

But now the branch has a strict evaluation rule:

```text
delta H_tau[S] = int_S(delta Q_tau - i_tau theta_total(delta))
I_tau,S = d_field alpha_tau,S = int_S i_tau omega_total + I_ref + I_tau + I_corner.
```

If the curl/residual terms vanish and `H_ref` is fixed source-blind before readout, the parent charge is exact. If not, the legal fallback is an interval:

```text
M_H^dress in [H_tau_center - H_ref - Delta_H_abs,
              H_tau_center - H_ref + Delta_H_abs]
epsilon_Hcharge <= Delta_H_abs/M_lower.
```

No row may use observed orbital `GM/G_cal` to define `H_tau`, `H_ref`, `M_lower`, or `M_H^dress`.

## Parent Charge Theorem Rows

{markdown_table(theorem, ["theorem_id", "formula", "status"])}

## Bound Law

{markdown_table(bound_law, ["law_id", "symbol", "formula"])}

## Parent Runner Output

{markdown_table(parent_output, ["charge_id", "M_H_dress_center_kg", "M_H_dress_low_kg", "M_H_dress_high_kg", "epsilon_Hcharge_abs", "runner_status"])}

## Chain Score

{markdown_table(score, ["charge_id", "parent_runner_status", "source_runner_status", "open_runner_status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "selection_status"])}

## Conclusion

This is a forward move but not a public local-GR/Newton claim. The real row blocks until the parent supplies one of:

1. a source-backed `H_tau_bulk` density/current integral plus fixed `H_ref`;
2. a theorem-zero residual radius with positive `M_lower`;
3. or finite residual components strong enough to bound `epsilon_Hcharge`.

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, content)

    formal = f"""# PPC4161 4781: Htau/Href Parent Charge Evaluation Or Reference Bound

Generated: `{timestamp}`

4781 installs the parent charge/bound interface:

```text
delta H_tau[S] = int_S(delta Q_tau - i_tau theta_total(delta))
I_tau,S = int_S i_tau omega_total + I_ref + I_tau + I_corner
M_H^dress = H_tau - H_ref
```

Exact charge use requires zero/bounded curl, a fixed source-blind reference, the same tau/coframe/worldtube branch and positive `M_lower`. Otherwise the legal result is the interval:

```text
M_H^dress in [H_tau_center-H_ref-Delta_H_abs, H_tau_center-H_ref+Delta_H_abs].
```

The physical row remains blocked; the counterfactual row only validates the runner chain.

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "htau_href_parent_charge_bound_interface",
        "4781 installs an executable parent-charge evaluator and no-cancellation interval bound for H_tau/H_ref before M_Hdress is allowed into Newton/orbital scoring.",
        "Generated source register, theorem rows, bound law, parent-charge input/output, chained source/open runner outputs, score gates, firewalls, route matrix, decision, status, next target and validation.",
        "parent_charge_bound_interface_nonclaim",
        NEXT_TARGET,
        "Do not treat interval or counterfactual rows as an exact source mass; do not use observed GM/Gcal as a parent charge source.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need real parent density/current H_tau, fixed source-blind H_ref, positive M_lower and residual-radius components.",
        "Htau/Href parent charge evaluation",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(row)


def update_resume(timestamp: str) -> None:
    content = f"""# Current Local Resume

Last checkpoint: `{DOC_PATH.name}`
Generated: `{timestamp}`

## Current target

`{NEXT_TARGET}`

## Live blocker

The parent charge interface now exists. The live physical gap is source-backed values or theorem-zero rows for `H_tau_bulk`, fixed `H_ref`, positive `M_lower`, and the no-cancellation residual radius `Delta_H_abs`.

## Firewalls

- No GitHub/public action from this checkpoint.
- No observed-GM/Gcal backfill into parent charge rows.
- Counterfactual rows are runner smoke only.
"""
    write_text(RESUME_PATH, content)


def append_spine_and_packet(timestamp: str) -> None:
    block = f"""

## {MARKER}

4781 installs the Htau/Href parent-charge evaluator: exact `M_H^dress=H_tau-H_ref` requires parent charge components plus zero/bounded curl, fixed source-blind reference and positive `M_lower`; otherwise the branch emits only a no-cancellation interval. Decision: `{DECISION}`. Next: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)

    packet = f"""

## {PACKET_MARKER}

Parent charge/bound runner: `{PARENT_RUNNER}`

Real source rows still block until `H_tau_bulk`, `H_ref`, `M_lower` and `Delta_H_abs` are parent-owned or source-backed. Counterfactual rows validate the chain only. Generated `{timestamp}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def validate(
    timestamp: str,
    sources: list[dict[str, Any]],
    parent_output: list[dict[str, Any]],
    source_output: list[dict[str, Any]],
    open_output: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4781_0_sources", "source paths and needles exist", all(row["exists"] is True and row["needle_found"] is True for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4781_1_parent_missing_blocks", "missing parent charge blocks", any(row["charge_id"] == "private_selector_missing_parent_charge_components" and row["runner_status"] == "BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS" for row in parent_output), str(PARENT_OUTPUT_CSV)))
    checks.append(("VAL4781_2_interval_smoke", "interval smoke computes nonclaim interval", any(row["charge_id"] == "private_parent_charge_interval_smoke_nonclaim" and row["runner_status"] == "PARENT_CHARGE_INTERVAL_COMPUTED_NONCLAIM" for row in parent_output), str(PARENT_OUTPUT_CSV)))
    checks.append(("VAL4781_3_counterfactual_parent", "counterfactual parent charge smokes", any(row["charge_id"] == "counterfactual_parent_charge_equals_comparator" and row["runner_status"] == "PARENT_CHARGE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM" for row in parent_output), str(PARENT_OUTPUT_CSV)))
    checks.append(("VAL4781_4_forbidden_control", "orbital GM source control fails", any(row["charge_id"] == "forbidden_orbital_GM_as_parent_charge_control" and row["runner_status"] == "FAILED_CIRCULAR_PARENT_CHARGE_SOURCE" for row in parent_output), str(PARENT_OUTPUT_CSV)))
    checks.append(("VAL4781_5_source_missing_blocks", "source runner still blocks real missing row", any(row["source_id"] == "private_selector_missing_parent_charge_components" and row["runner_status"] == "BLOCKED_MISSING_HTAU_OR_HREF" for row in source_output), str(SOURCE_OUTPUT_CSV)))
    checks.append(("VAL4781_6_source_counterfactual", "source runner smokes counterfactual exact row", any(row["source_id"] == "counterfactual_parent_charge_equals_comparator" and row["runner_status"] == "MHDRESS_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM" for row in source_output), str(SOURCE_OUTPUT_CSV)))
    checks.append(("VAL4781_7_open_counterfactual", "open arena runner smokes counterfactual exact row", any(row["arena_id"] == "counterfactual_parent_charge_equals_comparator" and row["runner_status"] == "RUNNER_SMOKE_PASS_NONCLAIM" for row in open_output), str(OPEN_OUTPUT_CSV)))
    checks.append(("VAL4781_8_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4781_9_formal_doc", "formal doc marker present", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), str(FORMAL_PATH)))
    checks.append(("VAL4781_10_claim_row", "claim row L-623 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    checks.append(("VAL4781_11_resume", "resume points to next target", RESUME_PATH.exists() and NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH)))

    rows: list[dict[str, Any]] = []
    for check_id, check, passed, detail in checks:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "validation_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4781_OVERALL",
            "check": "all 4781 parent charge evaluator checks pass",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_register(timestamp)
    theorem = theorem_rows(timestamp)
    bound_law = charge_bound_law_rows(timestamp)
    parent_input = parent_charge_input_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    routes = route_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(THEOREM_CSV, theorem)
    write_csv(CHARGE_BOUND_LAW_CSV, bound_law)
    write_csv(PARENT_INPUT_CSV, parent_input)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)

    run_command([sys.executable, str(PARENT_RUNNER), str(PARENT_INPUT_CSV), str(PARENT_OUTPUT_CSV)])
    parent_output = parse_csv(PARENT_OUTPUT_CSV)

    source_input = source_input_from_parent(timestamp, parent_input, parent_output)
    write_csv(SOURCE_INPUT_CSV, source_input)
    run_command([sys.executable, str(SOURCE_RUNNER), str(SOURCE_INPUT_CSV), str(SOURCE_OUTPUT_CSV)])
    source_output = parse_csv(SOURCE_OUTPUT_CSV)

    open_input = open_input_from_source(timestamp, source_output)
    write_csv(OPEN_INPUT_CSV, open_input)
    run_command([sys.executable, str(OPEN_RUNNER), str(OPEN_INPUT_CSV), str(OPEN_OUTPUT_CSV)])
    open_output = parse_csv(OPEN_OUTPUT_CSV)

    score = score_gate_rows(timestamp, parent_output, source_output, open_output)
    write_csv(SCORE_GATE_CSV, score)

    write_docs(timestamp, theorem, bound_law, parent_output, score, routes)
    add_claim_once(timestamp)
    append_spine_and_packet(timestamp)
    update_resume(timestamp)

    validation = validate(timestamp, sources, parent_output, source_output, open_output, gates)
    write_csv(VALIDATION_CSV, validation)

    cache_dir = SCRIPT_DIR / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)


if __name__ == "__main__":
    main()
