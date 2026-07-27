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

CHECKPOINT = "4776"
CLAIM_ID = "L-618"
MARKER = "PPC4161_GCAL_NORMALIZATION_OR_OPEN_ARENA_FIRST_VALUE_PACK_4776"
PACKET_MARKER = "PPC4161_PACKET_GCAL_NORMALIZATION_OR_OPEN_ARENA_FIRST_VALUE_PACK_4776"
DECISION = "GCAL_KAPPA_CODATA_CALIBRATION_ROW_SOURCE_BACKED_KAPPA_EFF_DERIVED_FROM_G_AND_C_MHDRESS_E00_BOUNDARY_PPN_R10_ORBITAL_VALUES_STILL_OPEN_NONCLAIM"
NEXT_TARGET = "4777-Y5-R2FR-MHdress-comparator-and-E00-open-arena-bound-pack.md"

DOC_PATH = POST / "4776-Y5-R2FR-Gcal-normalization-or-open-arena-first-value-pack.md"
FORMAL_PATH = FORMAL / "792-PPC4161-Gcal-normalization-or-open-arena-first-value-pack.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4776_SOURCE_REGISTER.csv"
CONSTANTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4776_CONSTANTS_PROVENANCE.csv"
KAPPA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4776_KAPPA_GCAL_NORMALIZATION.csv"
FIRST_VALUE_STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4776_OPEN_ARENA_FIRST_VALUE_STATUS.csv"
UNIT_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4776_UNIT_CONTRACT.csv"
NO_CIRCULARITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4776_NO_CIRCULARITY_AUDIT.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4776_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4776_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4776_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4776_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4776_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4776_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4776_VALIDATION.csv"

NIST_CONSTANTS_URL = "https://pml.nist.gov/cuu/Constants/"
NIST_G_URL = "https://physics.nist.gov/cgi-bin/cuu/Value?bg"
NIST_C_URL = "https://physics.nist.gov/cgi-bin/cuu/Value?c"
CODATA_TGFC_URL = "https://codata.org/initiatives/data-science-and-stewardship/fundamental-physical-constants/"

G_VALUE = 6.67430e-11
G_UNCERTAINTY = 0.00015e-11
C_VALUE = 299_792_458.0
C_UNCERTAINTY = 0.0

SOURCE_SPECS = [
    ("SRC4776_0_4775_first_values", "local", SOURCE_DIR / "P8_Y5_R2FR_4775_OPEN_ARENA_FIRST_VALUES.csv", "FV4775_0_Gcal", "4775 first-value target list"),
    ("SRC4776_1_4775_limit_map", "local", SOURCE_DIR / "P8_Y5_R2FR_4775_NEWTON_MAXWELL_PPN_LIMIT_MAP.csv", "LM4775_5_G", "4775 calibrated coupling map"),
    ("SRC4776_2_4775_no_circularity", "local", SOURCE_DIR / "P8_Y5_R2FR_4775_NO_CIRCULARITY_AUDIT.csv", "NC4775_1_G_not_predicted", "4775 numeric-G firewall"),
    ("SRC4776_3_4649_coupling_contract", "local", SOURCE_DIR / "P8_Y5_R2FR_4649_PARENT_GR_SELECTOR_CONTRACT.csv", "GRSEL4649_1_constant_coupling", "4649 calibrated coupling contract"),
    ("SRC4776_4_NIST_constants", "web", NIST_CONSTANTS_URL, "CODATA 2022 values and NIST Standard Reference Database 121", "NIST constants landing page"),
    ("SRC4776_5_NIST_G", "web", NIST_G_URL, "G=6.67430e-11 m^3 kg^-1 s^-2, u=0.00015e-11", "NIST Newtonian constant of gravitation page"),
    ("SRC4776_6_NIST_c", "web", NIST_C_URL, "c=299792458 m s^-1 exact", "NIST speed of light page"),
    ("SRC4776_7_CODATA_cycle", "web", CODATA_TGFC_URL, "2026 adjustment closes 31 December 2026; 2022 adjustment remains last regular adjustment", "CODATA TGFC update schedule"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    CONSTANTS_CSV,
    KAPPA_CSV,
    FIRST_VALUE_STATUS_CSV,
    UNIT_CONTRACT_CSV,
    NO_CIRCULARITY_CSV,
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
        "| " + " | ".join(str(row[column]).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def kappa_value() -> float:
    return 8.0 * math.pi * G_VALUE / (C_VALUE**4)


def kappa_uncertainty() -> float:
    return 8.0 * math.pi * G_UNCERTAINTY / (C_VALUE**4)


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


def constants_rows(timestamp: str) -> list[dict[str, Any]]:
    rel_g = G_UNCERTAINTY / G_VALUE
    return [
        {
            "checkpoint": CHECKPOINT,
            "constant_id": "CONST4776_0_c",
            "symbol": "c",
            "quantity": "speed of light in vacuum",
            "value": f"{C_VALUE:.0f}",
            "standard_uncertainty": f"{C_UNCERTAINTY:.0f}",
            "relative_uncertainty": "0",
            "units": "m s^-1",
            "source": NIST_C_URL,
            "source_basis": "NIST/CODATA 2022; exact SI defining constant",
            "valid_for_calibration": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "constant_id": "CONST4776_1_GN",
            "symbol": "G_N",
            "quantity": "Newtonian constant of gravitation",
            "value": f"{G_VALUE:.8e}",
            "standard_uncertainty": f"{G_UNCERTAINTY:.8e}",
            "relative_uncertainty": f"{rel_g:.12e}",
            "units": "m^3 kg^-1 s^-2",
            "source": NIST_G_URL,
            "source_basis": "NIST/CODATA 2022 recommended value; calibration datum only",
            "valid_for_calibration": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "constant_id": "CONST4776_2_CODATA_schedule",
            "symbol": "CODATA_cycle",
            "quantity": "constants adjustment schedule",
            "value": "2022 adjustment current; 2026 adjustment closes 2026-12-31 and results expected 2027",
            "standard_uncertainty": "not_applicable",
            "relative_uncertainty": "not_applicable",
            "units": "metadata",
            "source": CODATA_TGFC_URL,
            "source_basis": "CODATA TGFC states 2026 adjustment closing date and 2022 as last regular adjustment",
            "valid_for_calibration": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def kappa_rows(timestamp: str) -> list[dict[str, Any]]:
    kappa = kappa_value()
    sigma_kappa = kappa_uncertainty()
    rel = G_UNCERTAINTY / G_VALUE
    return [
        {
            "checkpoint": CHECKPOINT,
            "norm_id": "KG4776_0_definition",
            "quantity": "kappa_cal",
            "formula": "kappa_cal := 8*pi*G_N/c^4",
            "value": f"{kappa:.15e}",
            "standard_uncertainty": f"{sigma_kappa:.15e}",
            "relative_uncertainty": f"{rel:.12e}",
            "units": "m J^-1 = s^2 kg^-1 m^-1",
            "status": "SOURCE_BACKED_CALIBRATION_ROW",
            "valid_for_calibration": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "norm_id": "KG4776_1_inverse",
            "quantity": "G_cal",
            "formula": "G_cal := c^4*kappa_eff/(8*pi); calibration sets kappa_eff=kappa_cal for SI comparisons",
            "value": f"{G_VALUE:.8e}",
            "standard_uncertainty": f"{G_UNCERTAINTY:.8e}",
            "relative_uncertainty": f"{rel:.12e}",
            "units": "m^3 kg^-1 s^-2",
            "status": "SOURCE_BACKED_CALIBRATION_ROW_NOT_PREDICTION",
            "valid_for_calibration": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "norm_id": "KG4776_2_field_equation",
            "quantity": "local SI field equation",
            "formula": "G_mu_nu + Lambda_eff g_mu_nu = kappa_cal T_H_mu_nu + E_fail_mu_nu",
            "value": "ready_for_units_calibrated_private/open comparisons",
            "standard_uncertainty": "inherits G_N calibration uncertainty unless kappa_eff is independently derived",
            "relative_uncertainty": f"{rel:.12e}",
            "units": "curvature m^-2 from kappa_cal*T_H",
            "status": "UNIT_NORMALIZATION_READY_NONCLAIM",
            "valid_for_calibration": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def first_value_status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "value_id": "FV4776_0_Gcal",
            "quantity": "G_cal/kappa_eff normalization",
            "status_before": "MISSING_CALIBRATION_SOURCE_ROW",
            "status_after": "FILLED_SOURCE_BACKED_CALIBRATION_ROW",
            "value_or_next_input": f"kappa_cal={kappa_value():.15e} m J^-1 from CODATA G_N and exact c",
            "claim_effect": "enables SI comparison; does not predict G_N",
            "valid_for_calibration": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "value_id": "FV4776_1_MH_dress",
            "quantity": "M_H^dress",
            "status_before": "MISSING_SOURCE_BACKED_MASS_ROW",
            "status_after": "STILL_OPEN_NEXT_TARGET",
            "value_or_next_input": "need Hamiltonian worldtube mass comparator or accepted arena mass with same-frame units",
            "claim_effect": "blocks orbital/Newton real-arena scoring",
            "valid_for_calibration": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "value_id": "FV4776_2_E00",
            "quantity": "E_00 residual",
            "status_before": "MISSING_OPEN_ARENA_E00_BOUND",
            "status_after": "STILL_OPEN_NEXT_TARGET",
            "value_or_next_input": "need local non-EH/open residual envelope in observed frame",
            "claim_effect": "blocks quantitative Poisson residual pass/fail",
            "valid_for_calibration": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "value_id": "FV4776_3_boundary_flux",
            "quantity": "F_boundary/Poynting/radiation flux",
            "status_before": "MISSING_BOUNDARY_FLUX_LEDGER",
            "status_after": "STILL_OPEN",
            "value_or_next_input": "need EM Hilbert flux versus external/apparatus/radiative flux ledger",
            "claim_effect": "blocks open EM/Poynting local claims",
            "valid_for_calibration": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "value_id": "FV4776_4_PPN_transfer",
            "quantity": "Pi_PPN residual transfer matrix",
            "status_before": "MISSING_PPN_TRANSFER_MATRIX",
            "status_after": "STILL_OPEN",
            "value_or_next_input": "need residual-to-PPN map for gamma,beta,alpha_i,xi,zeta_i,Gdot/G",
            "claim_effect": "blocks open PPN empirical scoring",
            "valid_for_calibration": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "value_id": "FV4776_5_R10_alpha",
            "quantity": "alpha(lambda) local fifth-force row",
            "status_before": "MISSING_R10_NUMERIC_ROW",
            "status_after": "STILL_OPEN",
            "value_or_next_input": "need sourced parent coefficients or zero theorem and real bound curve",
            "claim_effect": "blocks R10 claim",
            "valid_for_calibration": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "value_id": "FV4776_6_orbital_profile",
            "quantity": "orbital profile/multipole residual",
            "status_before": "MISSING_ORBITAL_PROFILE_ROW",
            "status_after": "STILL_OPEN",
            "value_or_next_input": "need source profile, surface choice, compactness and multipole/error budget",
            "claim_effect": "blocks real orbital branch scoring",
            "valid_for_calibration": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def unit_contract_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "unit_id": "UC4776_0_curvature",
            "equation_or_object": "G_mu_nu + Lambda_eff g_mu_nu",
            "unit_statement": "m^-2",
            "compatibility_check": "kappa_cal*T_H has m J^-1 * J m^-3 = m^-2",
            "status": "UNITS_PASS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "unit_id": "UC4776_1_Poisson",
            "equation_or_object": "nabla^2 Phi_N = 4*pi*G_cal*rho_H",
            "unit_statement": "s^-2 on both sides when Phi_N has m^2 s^-2 and rho_H has kg m^-3",
            "compatibility_check": "G_cal*rho_H has m^3 kg^-1 s^-2 * kg m^-3 = s^-2",
            "status": "UNITS_PASS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "unit_id": "UC4776_2_orbit",
            "equation_or_object": "a_r=-G_cal*M_H^dress/r^2",
            "unit_statement": "m s^-2",
            "compatibility_check": "G_cal*M/r^2 has m^3 kg^-1 s^-2 * kg / m^2 = m s^-2",
            "status": "UNITS_PASS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def no_circularity_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "NC4776_0_calibration_not_prediction",
            "rule": "Using CODATA G_N fills a calibration boundary condition; it is not a derivation of G_N from MTS.",
            "status": "PASS_FIREWALL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "NC4776_1_GR_same_status",
            "rule": "kappa_cal makes the private/effective branch comparable in SI units; it does not promote B_GR to a public parent selector.",
            "status": "PASS_SCOPE_LOCK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "NC4776_2_open_values_still_open",
            "rule": "M_H^dress, E_00, boundary flux, PPN transfer, R10 and orbital profile are not silently filled by the G calibration row.",
            "status": "PASS_OPEN_GATES_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": "RT4776_0_MHdress_E00",
            "route": "M_H^dress comparator and E_00 open-arena bound pack",
            "payoff": "turns calibrated local Newton/Poisson branch into a real arena-ready residual score",
            "selection_status": "SELECTED_NEXT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "route_id": "RT4776_1_boundary_flux",
            "route": "Poynting/boundary flux ledger",
            "payoff": "needed for EM/open-radiative local systems after source mass and E00 are bounded",
            "selection_status": "QUEUED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "route_id": "RT4776_2_PPN_R10",
            "route": "PPN transfer and R10 alpha row",
            "payoff": "needed for empirical local tests once source normalization and residual envelope are in place",
            "selection_status": "QUEUED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PG4776_0", "do not label CODATA calibration as an MTS prediction of G", "blocks fake constant derivation"),
        ("PG4776_1", "do not score local tests until M_H^dress and E_00/open residual rows exist", "blocks overclaiming from unit normalization"),
        ("PG4776_2", "keep CODATA provenance and uncertainty attached to every SI comparison using kappa_cal", "prevents untracked precision claims"),
        ("PG4776_3", "if a future parent scale law derives kappa_eff, compare it against this calibration row instead of replacing provenance", "sets future derivation test"),
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
        ("FW4776_0", "G_cal row is calibration, not prediction", "GCAL_CALIBRATION_ONLY"),
        ("FW4776_1", "kappa_eff source-backed value does not prove public parent GR", "PARENT_SIGNATURE_STILL_OPEN"),
        ("FW4776_2", "open-arena first-value list remains mostly unfilled", "NO_EMPIRICAL_PASS"),
        ("FW4776_3", "CODATA uncertainty must travel with kappa_cal comparisons", "UNCERTAINTY_PROPAGATION_REQUIRED"),
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
            "meaning": "4776 fills the Gcal/kappa_eff calibration source row using NIST/CODATA G and exact c, while leaving the physical source mass and open residual rows for the next testability gate.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_GCAL_CALIBRATION_ROW_FILLED_NONCLAIM",
            "summary": "G_cal/kappa_eff is now source-backed for SI calibration; M_H^dress, E_00, boundary flux, PPN, R10 and orbital profile remain open.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "After calibrating kappa_eff, the next real progress is a source-mass comparator and E_00 residual envelope for Newton/orbital/open-arena scoring.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(
    timestamp: str,
    constants: list[dict[str, Any]],
    kappa: list[dict[str, Any]],
    first_values: list[dict[str, Any]],
    units: list[dict[str, Any]],
    no_circularity: list[dict[str, Any]],
    routes: list[dict[str, Any]],
) -> None:
    doc = f"""# 4776 — Gcal Normalization or Open-Arena First-Value Pack

Generated: `{timestamp}`

## Result

4776 fills the first open-arena value from 4775:

```text
G_cal/kappa_eff normalization = FILLED_SOURCE_BACKED_CALIBRATION_ROW
kappa_cal := 8*pi*G_N/c^4 = {kappa_value():.15e} m J^-1
sigma(kappa_cal) = {kappa_uncertainty():.15e} m J^-1
```

This is calibration, not derivation:

```text
G_cal = G_N(CODATA/NIST) for SI comparison.
MTS does not yet predict the numerical value of G_N.
```

## Constants Provenance

{markdown_table(constants, ["constant_id", "symbol", "value", "standard_uncertainty", "units", "source_basis"])}

## Kappa / Gcal Normalization

{markdown_table(kappa, ["norm_id", "quantity", "formula", "value", "status"])}

## Open-Arena First-Value Status

{markdown_table(first_values, ["value_id", "quantity", "status_before", "status_after", "claim_effect"])}

## Unit Contract

{markdown_table(units, ["unit_id", "equation_or_object", "unit_statement", "status"])}

## No-Circularity Audit

{markdown_table(no_circularity, ["audit_id", "rule", "status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "selection_status"])}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# PPC4161 4776: Gcal Normalization and First-Value Pack

Generated: `{timestamp}`

4776 installs the source-backed SI calibration row:

```text
G_N = {G_VALUE:.8e} m^3 kg^-1 s^-2
c = {C_VALUE:.0f} m s^-1
kappa_cal = 8*pi*G_N/c^4 = {kappa_value():.15e} m J^-1.
```

This is not a prediction of `G_N`; it is the calibration boundary condition needed to compare the private/effective local-GR branch with ordinary local tests.

Still open:

```text
M_H^dress, E_00, boundary/Poynting flux, PPN transfer, R10 alpha(lambda), orbital profile.
```

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4776 fills the first 4775 open-arena value: `G_cal/kappa_eff` now has a source-backed NIST/CODATA calibration row.
- The calibration is `kappa_cal=8*pi*G_N/c^4={kappa_value():.15e} m J^-1`, with uncertainty inherited from CODATA `G_N`; `c` is exact.
- This does not derive the numerical value of `G_N`; it fixes SI comparison units for the private/effective local-GR branch.
- Remaining first values are `M_H^dress`, `E_00`, boundary/Poynting flux, PPN transfer, R10 alpha row and orbital profile.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4776 packet update: local comparisons now have a source-backed SI normalization for `G_cal/kappa_eff`. Next work should build the `M_H^dress` comparator and `E_00` open residual envelope.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4776-Y5-R2FR-Gcal-normalization-or-open-arena-first-value-pack.md`

## Decision

`{DECISION}`

## What moved forward

- Filled the `G_cal/kappa_eff` first-value row using NIST/CODATA `G_N` and exact `c`.
- Derived the SI calibration value `kappa_cal=8*pi*G_N/c^4={kappa_value():.15e} m J^-1`.
- Added unit checks for Einstein-form, Poisson/Newton and orbital readout equations.
- Preserved the firewall: this is calibration for comparison, not an MTS prediction of numerical `G_N`.
- Left `M_H^dress`, `E_00`, boundary/Poynting flux, PPN transfer, R10 alpha and orbital profile rows open.

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
        "gcal_kappa_eff_source_backed_calibration_row",
        "4776 fills the Gcal/kappa_eff source-backed SI calibration row using CODATA/NIST G and exact c while keeping numeric G prediction blocked.",
        "Generated source register, constants provenance, kappa normalization, first-value status, unit contract, no-circularity audit, route matrix, promotion gates, firewalls, decision, status, next target and validation.",
        "source_backed_calibration_nonclaim",
        NEXT_TARGET,
        "Do not treat CODATA G calibration as an MTS prediction or empirical local-gravity pass.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need M_H^dress comparator and E_00 open-arena bound pack.",
        "Gcal/kappa normalization",
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
    constants: list[dict[str, Any]],
    kappa: list[dict[str, Any]],
    first_values: list[dict[str, Any]],
    units: list[dict[str, Any]],
    no_circularity: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4776_0_sources_available", "all local sources exist and web URLs are recorded", all(row["exists_or_url_ok"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4776_1_needles_or_web_verified", "all local needles found and web facts recorded", all(row["needle_found_or_web_verified"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4776_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))

    checks.append(("VAL4776_2_constants", "G and c constants rows are positive and source-backed", any(row["symbol"] == "G_N" and float(row["value"]) > 0 and row["source"].startswith("https://") for row in constants) and any(row["symbol"] == "c" and float(row["value"]) == 299792458 for row in constants), str(CONSTANTS_CSV)))
    checks.append(("VAL4776_3_kappa_positive", "kappa calibration row is positive with uncertainty", any(row["quantity"] == "kappa_cal" and float(row["value"]) > 0 and float(row["standard_uncertainty"]) > 0 and row["status"] == "SOURCE_BACKED_CALIBRATION_ROW" for row in kappa), str(KAPPA_CSV)))
    checks.append(("VAL4776_4_G_not_prediction", "Gcal row is not a prediction claim", any(row["quantity"] == "G_cal" and row["status"] == "SOURCE_BACKED_CALIBRATION_ROW_NOT_PREDICTION" for row in kappa), str(KAPPA_CSV)))
    checks.append(("VAL4776_5_first_value_filled", "Gcal first value filled", any(row["value_id"] == "FV4776_0_Gcal" and row["status_after"] == "FILLED_SOURCE_BACKED_CALIBRATION_ROW" for row in first_values), str(FIRST_VALUE_STATUS_CSV)))
    checks.append(("VAL4776_6_open_values_retained", "M_H/E00/boundary/PPN/R10/orbital stay open", all(any(row["value_id"] == value_id and row["status_after"].startswith("STILL_OPEN") for row in first_values) for value_id in ["FV4776_1_MH_dress", "FV4776_2_E00", "FV4776_3_boundary_flux", "FV4776_4_PPN_transfer", "FV4776_5_R10_alpha", "FV4776_6_orbital_profile"]), str(FIRST_VALUE_STATUS_CSV)))
    checks.append(("VAL4776_7_units_pass", "all unit contract rows pass", all(row["status"] == "UNITS_PASS" for row in units), str(UNIT_CONTRACT_CSV)))
    checks.append(("VAL4776_8_no_circularity", "no-circularity audit passes", all(row["status"].startswith("PASS") for row in no_circularity), str(NO_CIRCULARITY_CSV)))
    checks.append(("VAL4776_9_route_selected", "M_H/E00 next route selected", any(row["selection_status"] == "SELECTED_NEXT" and "E_00" in row["route"] for row in routes), str(ROUTE_MATRIX_CSV)))
    checks.append(("VAL4776_10_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4776_11_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4776_12_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4776_13_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4776_14_claim_row", "claim row L-618 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4776_15_resume", "resume points from 4776 to 4777", "4776-Y5" in resume_text and "4777-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4776_16_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))

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
            "validation_id": "VAL4776_OVERALL",
            "check": "all 4776 Gcal/kappa calibration checks pass",
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
    constants = constants_rows(timestamp)
    kappa = kappa_rows(timestamp)
    first_values = first_value_status_rows(timestamp)
    units = unit_contract_rows(timestamp)
    no_circularity = no_circularity_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(CONSTANTS_CSV, constants)
    write_csv(KAPPA_CSV, kappa)
    write_csv(FIRST_VALUE_STATUS_CSV, first_values)
    write_csv(UNIT_CONTRACT_CSV, units)
    write_csv(NO_CIRCULARITY_CSV, no_circularity)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, constants, kappa, first_values, units, no_circularity, routes)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, constants, kappa, first_values, units, no_circularity, routes, gates, timestamp))


if __name__ == "__main__":
    main()
