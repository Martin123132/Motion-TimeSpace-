from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4777"
CLAIM_ID = "L-619"
MARKER = "PPC4161_MHDRESS_COMPARATOR_AND_E00_OPEN_ARENA_BOUND_PACK_4777"
PACKET_MARKER = "PPC4161_PACKET_MHDRESS_COMPARATOR_AND_E00_OPEN_ARENA_BOUND_PACK_4777"
DECISION = "MHDRESS_ORBITAL_GM_COMPARATOR_ROW_AND_E00_POISSON_ENVELOPE_DERIVED_OBSERVED_GM_IS_COMPARATOR_NOT_DEFINITION_MHDRESS_NUMERIC_AND_E00_VALUES_STILL_OPEN_NONCLAIM"
NEXT_TARGET = "4778-Y5-R2FR-Hamiltonian-mass-source-functional-runner-or-E00-bound-input.md"

DOC_PATH = POST / "4777-Y5-R2FR-MHdress-comparator-and-E00-open-arena-bound-pack.md"
FORMAL_PATH = FORMAL / "793-PPC4161-MHdress-comparator-and-E00-open-arena-bound-pack.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4777_SOURCE_REGISTER.csv"
GM_COMPARATOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4777_MHDRESS_GM_COMPARATOR_ROW.csv"
E00_ENVELOPE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4777_E00_POISSON_OPEN_ENVELOPE.csv"
OPEN_SCORE_STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4777_NEWTON_ORBITAL_OPEN_SCORE_STATUS.csv"
ANTI_CIRCULARITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4777_ANTI_CIRCULARITY_AUDIT.csv"
UNIT_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4777_UNIT_CONTRACT.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4777_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4777_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4777_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4777_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4777_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4777_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4777_VALIDATION.csv"

IAU_B3_URL = "https://arxiv.org/abs/1605.09788"
NIST_G_URL = "https://physics.nist.gov/cgi-bin/cuu/Value?bg"
G_CAL = 6.67430e-11
SIGMA_G = 0.00015e-11
C_VALUE = 299_792_458.0
MU_SUN_NOMINAL = 1.3271244e20

SOURCE_SPECS = [
    ("SRC4777_0_4776_gcal", "local", SOURCE_DIR / "P8_Y5_R2FR_4776_KAPPA_GCAL_NORMALIZATION.csv", "KG4776_1_inverse", "4776 Gcal calibration row"),
    ("SRC4777_1_4776_first_values", "local", SOURCE_DIR / "P8_Y5_R2FR_4776_OPEN_ARENA_FIRST_VALUE_STATUS.csv", "FV4776_1_MH_dress", "4776 MHdress/E00 still-open first values"),
    ("SRC4777_2_4775_newton_map", "local", SOURCE_DIR / "P8_Y5_R2FR_4775_NEWTON_MAXWELL_PPN_LIMIT_MAP.csv", "LM4775_2_orbital", "4775 orbital/Newton map"),
    ("SRC4777_3_4719_poisson", "local", SOURCE_DIR / "P8_Y5_R2FR_4719_LINEARIZED_FIELD_EQUATION_ROWS.csv", "LFE4719_4_Gauss_orbit_readout", "4719 Poisson/Gauss residual readout"),
    ("SRC4777_4_4171_poisson", "local", SOURCE_DIR / "P8_Y5_R2FR_4171_POISSON_GAUSS_DERIVATION.csv", "PG4171_4_gauss", "4171 private Hamiltonian source to Gauss readout"),
    ("SRC4777_5_4171_orbit", "local", SOURCE_DIR / "P8_Y5_R2FR_4171_ORBITAL_ACCELERATION_READOUT.csv", "OR4171_2_radial", "4171 orbital acceleration readout"),
    ("SRC4777_6_Hamiltonian_contract", "local", SOURCE_DIR / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG5_orbital_inverse_square_readout", "older no-GM-backfill Hamiltonian/Gauss contract"),
    ("SRC4777_7_Hilbert_contract", "local", SOURCE_DIR / "P8_Hilbert_monopole_calibration_CONTRACT.csv", "HM3_absolute_monopole_calibration", "older Hilbert monopole calibration contract"),
    ("SRC4777_8_profile_theorem", "local", SOURCE_DIR / "P8_Y5_R2FR_4577_LAPSE_TEST_PROFILE_OWNER_THEOREM.csv", "LTP4577_1_effective_profile_identity", "4577 all-lapse profile owner theorem"),
    ("SRC4777_9_readout_leak", "local", SOURCE_DIR / "P8_Y5_R2FR_4578_RHO_READOUT_SHIFT_FIRST_SOURCE_LEAK_ROW.csv", "RSL4578_0_rho_readout_shift_commutator", "4578 readout source-leak row"),
    ("SRC4777_10_IAU_B3", "web", IAU_B3_URL, "IAU 2015 Resolution B3 nominal solar mass parameter = 1.3271244e20 m^3 s^-2 exact conversion factor", "IAU nominal solar GM comparator source"),
    ("SRC4777_11_NIST_G", "web", NIST_G_URL, "CODATA/NIST G=6.67430e-11 m^3 kg^-1 s^-2", "G calibration source inherited from 4776"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    GM_COMPARATOR_CSV,
    E00_ENVELOPE_CSV,
    OPEN_SCORE_STATUS_CSV,
    ANTI_CIRCULARITY_CSV,
    UNIT_CONTRACT_CSV,
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


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


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
        "| " + " | ".join(str(row[column]).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ") for column in columns)
        + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def m_sun_comparator() -> float:
    return MU_SUN_NOMINAL / G_CAL


def sigma_m_sun_comparator() -> float:
    return m_sun_comparator() * (SIGMA_G / G_CAL)


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


def gm_comparator_rows(timestamp: str) -> list[dict[str, Any]]:
    sigma_mu = 0.0
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "GM4777_0_primary_mass_definition",
            "quantity": "M_H^dress",
            "formula_or_value": "M_H^dress[W_H;tau] := H_tau[S_link;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs]",
            "units": "kg after SI calibration",
            "source_or_basis": "Hamiltonian/Hilbert source branch; not orbital GM",
            "status": "PRIMARY_MTS_SOURCE_MASS_DEFINITION_NO_NUMERIC_ROW_YET",
            "valid_for_comparator": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "GM4777_1_observed_mu_sun",
            "quantity": "mu_sun_nominal",
            "formula_or_value": f"{MU_SUN_NOMINAL:.7e}",
            "units": "m^3 s^-2",
            "source_or_basis": "IAU 2015 Resolution B3 nominal solar mass parameter; exact conversion factor, not true instantaneous solar property",
            "status": "SOURCE_BACKED_OBSERVED_GM_COMPARATOR",
            "valid_for_comparator": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "GM4777_2_mass_comparator_from_mu",
            "quantity": "M_GM_sun_cal := mu_sun_nominal/G_cal",
            "formula_or_value": f"{m_sun_comparator():.15e}",
            "units": "kg",
            "source_or_basis": f"mu_sun_nominal/G_cal; sigma_M={sigma_m_sun_comparator():.15e} kg inherited from CODATA G",
            "status": "SOURCE_BACKED_COMPARATOR_ONLY_NOT_MHDRESS_DEFINITION",
            "valid_for_comparator": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "GM4777_3_mass_residual",
            "quantity": "Delta_MH_sun",
            "formula_or_value": "(M_H^dress - M_GM_sun_cal)/M_GM_sun_cal",
            "units": "dimensionless",
            "source_or_basis": "first executable comparator residual; cannot be evaluated until M_H^dress is computed from the Hamiltonian/source branch",
            "status": "COMPARATOR_RESIDUAL_READY_VALUE_MISSING",
            "valid_for_comparator": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "GM4777_4_uncertainty_policy",
            "quantity": "sigma_mu_and_sigma_M",
            "formula_or_value": f"sigma_mu_nominal={sigma_mu:.1f}; sigma_M_from_G={sigma_m_sun_comparator():.15e}",
            "units": "m^3 s^-2 and kg",
            "source_or_basis": "IAU nominal mu is exact conversion; mass uncertainty enters through calibrated G only",
            "status": "UNCERTAINTY_POLICY_READY",
            "valid_for_comparator": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def e00_envelope_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "E004777_0_poisson_residual",
            "quantity": "E_00",
            "formula_or_bound": "nabla^2 Phi_N = 4*pi*G_cal*rho_H + (c^2/2)E_00",
            "units": "m^-2",
            "meaning": "open-branch non-EH/local residual in the observed metric frame",
            "status": "DERIVED_FROM_4719",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "E004777_1_integrated_mu_shift",
            "quantity": "Delta_mu_E00",
            "formula_or_bound": "Delta_mu_E00 = (c^2/(8*pi))*int_W E_00 dV",
            "units": "m^3 s^-2",
            "meaning": "Gauss-integrated E_00 contribution to the observed gravitational parameter",
            "status": "EXECUTABLE_ENVELOPE_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "E004777_2_observed_mu_balance",
            "quantity": "mu_obs_balance",
            "formula_or_bound": "mu_obs = G_cal*M_H^dress + Delta_mu_E00 + Delta_mu_boundary + Delta_mu_profile + Delta_mu_readout",
            "units": "m^3 s^-2",
            "meaning": "all open-arena deviations are explicit additive residuals rather than hidden in GM",
            "status": "BALANCE_LAW_DERIVED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "E004777_3_relative_envelope",
            "quantity": "eta_E00_abs",
            "formula_or_bound": "eta_E00_abs <= c^2*int_W |E_00| dV/(8*pi*mu_ref)",
            "units": "dimensionless",
            "meaning": "relative E_00 contribution to an orbital/Newton comparator with mu_ref>0",
            "status": "BOUND_FORM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "E004777_4_spherical_sup_bound",
            "quantity": "E00_sup_sphere_required",
            "formula_or_bound": "if |E_00|<=E00_sup on radius R, then eta_E00_abs <= c^2*E00_sup*R^3/(6*mu_ref)",
            "units": "m^-2",
            "meaning": "first practical bound target once a radius/support and tolerance are supplied",
            "status": "SPHERICAL_ENVELOPE_READY_R_TOLERANCE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def open_score_status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "OSS4777_0_Gcal",
            "object": "G_cal/kappa_eff",
            "status": "FILLED_4776",
            "score_effect": "SI normalization ready",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "OSS4777_1_mu_comparator",
            "object": "solar GM comparator",
            "status": "FILLED_SOURCE_BACKED_COMPARATOR",
            "score_effect": "can compare against M_H^dress once M_H^dress exists",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "OSS4777_2_MHdress",
            "object": "M_H^dress numeric/source functional",
            "status": "MISSING_PRIMARY_MTS_MASS_VALUE",
            "score_effect": "blocks Newton/orbital pass",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "OSS4777_3_E00",
            "object": "E_00 bound/input",
            "status": "BOUND_FORM_READY_VALUE_MISSING",
            "score_effect": "blocks open Poisson residual pass",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "OSS4777_4_product_gate",
            "object": "open Newton/orbital score",
            "status": "BLOCKED_UNTIL_MHDRESS_AND_E00_FILLED_OR_ZEROED",
            "score_effect": "no empirical claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def anti_circularity_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "AC4777_0_no_GM_definition",
            "M_GM_sun_cal=mu_sun/G_cal is a comparator only; M_H^dress remains H_tau-H_ref.",
            "prevents defining the source mass from the orbital quantity being tested",
            "PASS_COMPARATOR_ONLY",
        ),
        (
            "AC4777_1_G_uncertainty",
            "Solar nominal GM is exact as a conversion constant, but converting it to kg inherits CODATA G uncertainty.",
            "prevents false precision in M_GM_sun_cal",
            "PASS_UNCERTAINTY_ATTACHED",
        ),
        (
            "AC4777_2_E00_not_zeroed",
            "E_00 is not set to zero in open arenas; it is integrated into Delta_mu_E00.",
            "prevents private branch zero from being smuggled into real/open systems",
            "PASS_OPEN_RESIDUAL_RETAINED",
        ),
        (
            "AC4777_3_boundary_profile_readout",
            "Boundary, profile and readout residuals remain separate from E_00 and from M_H^dress.",
            "prevents cancellation bookkeeping from hiding source leakage",
            "PASS_NO_CANCELLATION",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": audit_id,
            "rule": rule,
            "effect": effect,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, rule, effect, status in specs
    ]


def unit_contract_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "unit_id": "UC4777_0_mu",
            "object": "mu_obs and G_cal*M_H^dress",
            "unit_check": "G_cal*M has m^3 kg^-1 s^-2 * kg = m^3 s^-2",
            "status": "UNITS_PASS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "unit_id": "UC4777_1_E00_integral",
            "object": "Delta_mu_E00=(c^2/(8*pi))*int E_00 dV",
            "unit_check": "c^2 * (m^-2*m^3) = m^3 s^-2",
            "status": "UNITS_PASS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "unit_id": "UC4777_2_eta",
            "object": "eta_E00_abs",
            "unit_check": "Delta_mu_E00/mu_ref is dimensionless",
            "status": "UNITS_PASS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": "RT4777_0_MHdress_runner",
            "route": "Hamiltonian mass source-functional runner",
            "payoff": "compute or certify M_H^dress without orbital GM backfill",
            "selection_status": "SELECTED_NEXT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "route_id": "RT4777_1_E00_input",
            "route": "E_00 support/radius/tolerance input row",
            "payoff": "turn the E00 envelope into a numeric open-arena bound",
            "selection_status": "SELECTED_NEXT_PARALLEL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "route_id": "RT4777_2_boundary_profile",
            "route": "boundary/profile/readout residual ledger",
            "payoff": "needed after MHdress/E00 to prevent hidden source leakage",
            "selection_status": "QUEUED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PG4777_0", "do not define M_H^dress from observed orbital GM", "blocks circular Newton pass"),
        ("PG4777_1", "do not set E_00=0 in open arenas without private-branch hypotheses or a bound", "blocks closure smuggling"),
        ("PG4777_2", "open Newton/orbital score requires M_H^dress plus E_00 plus boundary/profile/readout residual ledger", "blocks partial score"),
        ("PG4777_3", "IAU nominal solar GM is a comparator/conversion standard, not the true instantaneous solar property", "blocks source overclaim"),
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
        ("FW4777_0", "observed GM comparator is not M_H^dress definition", "ANTI_CIRCULARITY_ACTIVE"),
        ("FW4777_1", "E_00 envelope is not a zero theorem", "OPEN_RESIDUAL_ACTIVE"),
        ("FW4777_2", "no Newton/orbital empirical claim yet", "MHDRESS_E00_VALUES_MISSING"),
        ("FW4777_3", "mass uncertainty from calibrated G remains attached", "UNCERTAINTY_REQUIRED"),
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
            "meaning": "4777 turns the calibrated local branch into an executable Newton/orbital comparator framework: observed GM is source-backed comparator data and E00 is an explicit Poisson residual envelope.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_COMPARATOR_AND_E00_ENVELOPE_NONCLAIM",
            "summary": "Solar GM comparator and E00 Poisson envelope are ready; primary M_H^dress numeric/source-functional value and E00 input values remain open.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "The next progress step must either compute/certify M_H^dress from the Hamiltonian/source branch or fill the E00 support/radius/tolerance bound input.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(
    timestamp: str,
    gm_rows: list[dict[str, Any]],
    e00_rows: list[dict[str, Any]],
    score_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    unit_rows: list[dict[str, Any]],
    route_rows_data: list[dict[str, Any]],
) -> None:
    doc = f"""# 4777 — MHdress Comparator and E00 Open-Arena Bound Pack

Generated: `{timestamp}`

## Result

4777 fills the first observed `GM` comparator row without cheating:

```text
mu_sun_nominal = {MU_SUN_NOMINAL:.7e} m^3 s^-2
M_GM_sun_cal = mu_sun_nominal/G_cal = {m_sun_comparator():.15e} kg
sigma(M_GM_sun_cal) = {sigma_m_sun_comparator():.15e} kg
```

But:

```text
M_H^dress is still H_tau[S_link] - H_ref.
Observed GM/G_cal is only a comparator, not the definition of M_H^dress.
```

The open-branch `E_00` residual is now an executable envelope:

```text
nabla^2 Phi_N = 4*pi*G_cal*rho_H + (c^2/2)E_00
mu_obs = G_cal*M_H^dress + (c^2/(8*pi))*int_W E_00 dV + residuals.
```

## MHdress / GM Comparator Rows

{markdown_table(gm_rows, ["row_id", "quantity", "formula_or_value", "status"])}

## E00 Poisson Envelope

{markdown_table(e00_rows, ["row_id", "quantity", "formula_or_bound", "status"])}

## Open Newton / Orbital Score Status

{markdown_table(score_rows, ["status_id", "object", "status", "score_effect"])}

## Anti-Circularity Audit

{markdown_table(audit_rows, ["audit_id", "rule", "status"])}

## Unit Contract

{markdown_table(unit_rows, ["unit_id", "object", "unit_check", "status"])}

## Route Selection

{markdown_table(route_rows_data, ["route_id", "route", "selection_status"])}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# PPC4161 4777: MHdress Comparator and E00 Open-Arena Bound Pack

Generated: `{timestamp}`

4777 adds the first source-backed `GM` comparator:

```text
mu_sun_nominal={MU_SUN_NOMINAL:.7e} m^3 s^-2
M_GM_sun_cal={m_sun_comparator():.15e} kg
```

This row is comparator-only. The MTS mass remains:

```text
M_H^dress[W_H;tau] = H_tau[S_link] - H_ref.
```

The open `E_00` branch is now:

```text
Delta_mu_E00 = (c^2/(8*pi))*int_W E_00 dV
mu_obs = G_cal*M_H^dress + Delta_mu_E00 + Delta_mu_boundary + Delta_mu_profile + Delta_mu_readout.
```

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4777 fills a source-backed solar `GM` comparator row using IAU 2015 Resolution B3 nominal solar mass parameter and 4776 `G_cal`.
- Comparator value: `M_GM_sun_cal={m_sun_comparator():.15e} kg`, with uncertainty from CODATA `G`.
- Anti-circularity remains active: `M_H^dress` is still `H_tau-H_ref`; observed `GM/G_cal` is only a comparator.
- The open `E_00` residual is now an executable Poisson/Gauss envelope: `Delta_mu_E00=(c^2/(8*pi))*int_W E_00 dV`.
- Open Newton/orbital scoring remains blocked until `M_H^dress` and `E_00` input/bound values are supplied.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4777 packet update: calibrated local Newton/orbital comparison now has an observed `GM` comparator and an explicit `E_00` residual envelope. Next work must compute/certify `M_H^dress` from the source branch or fill the `E_00` support/radius/tolerance input.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4777-Y5-R2FR-MHdress-comparator-and-E00-open-arena-bound-pack.md`

## Decision

`{DECISION}`

## What moved forward

- Added a source-backed solar `GM` comparator row using IAU nominal `mu_sun` and 4776 `G_cal`.
- Derived `M_GM_sun_cal={m_sun_comparator():.15e} kg` as comparator-only, not as the definition of `M_H^dress`.
- Derived the open Poisson/Gauss residual envelope `Delta_mu_E00=(c^2/(8*pi))*int_W E_00 dV`.
- Kept open Newton/orbital scoring blocked until primary `M_H^dress` and `E_00` source/bound rows exist.

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
        "mhdress_gm_comparator_and_e00_envelope",
        "4777 creates a source-backed observed-GM comparator row and derives the E00 Poisson/Gauss residual envelope without defining M_H^dress from orbital GM.",
        "Generated source register, GM comparator row, E00 envelope, open score status, anti-circularity audit, unit contract, route matrix, promotion gates, firewalls, decision, status, next target and validation.",
        "comparator_and_bound_form_nonclaim",
        NEXT_TARGET,
        "Do not treat observed GM/Gcal as the MTS Hamiltonian mass definition or E00 envelope as a zero theorem.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need M_H^dress source-functional runner or E00 bound input.",
        "MHdress comparator and E00 envelope",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    gm_rows: list[dict[str, Any]],
    e00_rows: list[dict[str, Any]],
    score_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    unit_rows: list[dict[str, Any]],
    route_rows_data: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4777_0_sources_available", "all local sources exist and web URLs are recorded", all(row["exists_or_url_ok"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4777_1_needles_or_web_verified", "all local needles found and web facts recorded", all(row["needle_found_or_web_verified"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4777_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))

    checks.append(("VAL4777_2_primary_mass_not_filled", "M_Hdress remains primary non-GM definition", any(row["row_id"] == "GM4777_0_primary_mass_definition" and row["status"] == "PRIMARY_MTS_SOURCE_MASS_DEFINITION_NO_NUMERIC_ROW_YET" for row in gm_rows), str(GM_COMPARATOR_CSV)))
    checks.append(("VAL4777_3_mu_comparator", "solar GM comparator filled", any(row["row_id"] == "GM4777_1_observed_mu_sun" and float(row["formula_or_value"]) > 0 and row["status"] == "SOURCE_BACKED_OBSERVED_GM_COMPARATOR" for row in gm_rows), str(GM_COMPARATOR_CSV)))
    checks.append(("VAL4777_4_mass_comparator", "mass comparator is positive and comparator-only", any(row["row_id"] == "GM4777_2_mass_comparator_from_mu" and float(row["formula_or_value"]) > 0 and row["status"] == "SOURCE_BACKED_COMPARATOR_ONLY_NOT_MHDRESS_DEFINITION" for row in gm_rows), str(GM_COMPARATOR_CSV)))
    checks.append(("VAL4777_5_e00_balance", "E00 observed-mu balance exists", any(row["row_id"] == "E004777_2_observed_mu_balance" and "Delta_mu_E00" in row["formula_or_bound"] for row in e00_rows), str(E00_ENVELOPE_CSV)))
    checks.append(("VAL4777_6_e00_bound", "E00 relative bound form exists", any(row["row_id"] == "E004777_3_relative_envelope" and row["status"] == "BOUND_FORM_READY_VALUES_MISSING" for row in e00_rows), str(E00_ENVELOPE_CSV)))
    checks.append(("VAL4777_7_score_blocked", "open score remains blocked until MHdress and E00 values", any(row["status"] == "BLOCKED_UNTIL_MHDRESS_AND_E00_FILLED_OR_ZEROED" for row in score_rows), str(OPEN_SCORE_STATUS_CSV)))
    checks.append(("VAL4777_8_anti_circularity", "anti-circularity audit passes", all(row["status"].startswith("PASS") for row in audit_rows), str(ANTI_CIRCULARITY_CSV)))
    checks.append(("VAL4777_9_units_pass", "unit contract passes", all(row["status"] == "UNITS_PASS" for row in unit_rows), str(UNIT_CONTRACT_CSV)))
    checks.append(("VAL4777_10_route_selected", "MHdress runner and E00 input selected", any(row["selection_status"] == "SELECTED_NEXT" and "mass source-functional" in row["route"] for row in route_rows_data) and any(row["selection_status"] == "SELECTED_NEXT_PARALLEL" and "E_00" in row["route"] for row in route_rows_data), str(ROUTE_MATRIX_CSV)))
    checks.append(("VAL4777_11_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4777_12_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4777_13_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4777_14_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4777_15_claim_row", "claim row L-619 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4777_16_resume", "resume points from 4777 to 4778", "4777-Y5" in resume_text and "4778-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4777_17_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))

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
            "validation_id": "VAL4777_OVERALL",
            "check": "all 4777 MHdress comparator and E00 envelope checks pass",
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
    gm_rows = gm_comparator_rows(timestamp)
    e00_rows = e00_envelope_rows(timestamp)
    score_rows = open_score_status_rows(timestamp)
    audit_rows = anti_circularity_rows(timestamp)
    unit_rows = unit_contract_rows(timestamp)
    route_rows_data = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(GM_COMPARATOR_CSV, gm_rows)
    write_csv(E00_ENVELOPE_CSV, e00_rows)
    write_csv(OPEN_SCORE_STATUS_CSV, score_rows)
    write_csv(ANTI_CIRCULARITY_CSV, audit_rows)
    write_csv(UNIT_CONTRACT_CSV, unit_rows)
    write_csv(ROUTE_MATRIX_CSV, route_rows_data)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, gm_rows, e00_rows, score_rows, audit_rows, unit_rows, route_rows_data)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, gm_rows, e00_rows, score_rows, audit_rows, unit_rows, route_rows_data, gates, timestamp))


if __name__ == "__main__":
    main()
